#!/usr/bin/env python3
"""
Measure Berkeley SoftFloat compiled for riscv64, for every float operation the
Sail RISC-V model declares as an external in model/core/softfloat_interface.sail.

Read-only on the sources; every artefact is written under SCRATCH.

Branch targets inside an unlinked .o are held in relocations against local
`.L0` labels (the encoded immediate is 0).  No riscv64 linker is installed, so
targets are resolved from `llvm-readelf -r`, whose "Symbol's Value" column is
exactly the label address.  Result is identical to what a --no-relax link would
produce, without touching anything outside the scratchpad.
"""

import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")   # no machine path is written into this file

SF = HOME + "/Programming/SOURCES/sail-riscv/dependencies/softfloat/berkeley-softfloat-3"
SAIL = HOME + "/Programming/SOURCES/sail-riscv/model/core/softfloat_interface.sail"
SCRATCH = ("/tmp/claude-1000/-home-<user>-Programming/"
           "6fc7a103-e75c-45df-aff2-b85555e7a824/scratchpad")

OBJDUMP = "/usr/lib/llvm-21/bin/llvm-objdump"
READELF = "/usr/lib/llvm-21/bin/llvm-readelf"
CLANG = "clang"

# Defines and include layout taken verbatim from build/Linux-RISCV64-GCC/Makefile
# (SOFTFLOAT_OPTS, -DSOFTFLOAT_FAST_INT64, C_INCLUDES with SPECIALIZE_TYPE=RISCV).
DEFINES = [
    "-DSOFTFLOAT_FAST_INT64",
    "-DSOFTFLOAT_ROUND_ODD",
    "-DINLINE_LEVEL=5",
    "-DSOFTFLOAT_FAST_DIV32TO16",
    "-DSOFTFLOAT_FAST_DIV64TO32",
]
INCLUDES = [
    "-I" + SF + "/build/Linux-RISCV64-GCC",   # platform.h  (the Makefile's -I.)
    "-I" + SF + "/source/RISCV",              # specialize.h
    "-I" + SF + "/source/include",
    # f32_to_bf16.c alone includes <inttypes.h> and <stdio.h> (unused leftovers);
    # the bare-metal riscv64 target has no libc headers, so a last-resort shim
    # directory with two empty headers satisfies them.
    "-idirafter", SCRATCH + "/shim",
]


def compile_one(cfile, out, march):
    cmd = [CLANG, "--target=riscv64-unknown-elf",
           "-march=" + march, "-mabi=lp64", "-O2", "-c",
           "-Werror-implicit-function-declaration"] + DEFINES + INCLUDES + \
          [cfile, "-o", out]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stderr or "").strip(), " ".join(cmd)


# ---------------------------------------------------------------- classify --
BRANCH = {"beq", "bne", "blt", "bge", "bltu", "bgeu", "beqz", "bnez",
          "blez", "bgez", "bltz", "bgtz", "bgt", "ble", "bgtu", "bleu",
          "c.beqz", "c.bnez"}
JUMP = {"j", "jr", "jal", "jalr", "ret", "tail", "call",
        "c.j", "c.jr", "c.jal", "c.jalr", "c.ebreak"}
MEM = {"lb", "lh", "lw", "ld", "lbu", "lhu", "lwu", "sb", "sh", "sw", "sd",
       "c.lw", "c.ld", "c.lwsp", "c.ldsp", "c.sw", "c.sd", "c.swsp", "c.sdsp",
       "lr.w", "lr.d", "sc.w", "sc.d",
       "flw", "fld", "fsw", "fsd", "c.flw", "c.fld", "c.fsw", "c.fsd"}
MULDIV = {"mul", "mulh", "mulhu", "mulhsu", "mulw",
          "div", "divu", "rem", "remu", "divw", "divuw", "remw", "remuw"}

INSN_RE = re.compile(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f ]+\t)?([a-z0-9._]+)\s*(.*)$")
HDR_RE = re.compile(r"^([0-9a-f]+)\s+<([^>]+)>:")
TGT_RE = re.compile(r"0x([0-9a-f]+)\s*<")


def jump_table_targets(obj):
    """R_RISCV_32 entries in .rela.rodata are the switch jump table: .text labels."""
    out = subprocess.run([READELF, "-r", obj], capture_output=True, text=True).stdout
    tgts, insec = [], False
    for line in out.splitlines():
        if line.startswith("Relocation section"):
            insec = ".rela.rodata" in line
            continue
        if not insec:
            continue
        m = re.match(r"^([0-9a-f]{16})\s+[0-9a-f]{16}\s+(\S+)\s+([0-9a-f]{16})\s+(.*)$",
                     line.strip())
        if m and m.group(2) in ("R_RISCV_32", "R_RISCV_64"):
            name = m.group(4).split("+")[0].strip()
            if name.startswith(".L") or name in ("", ".text"):
                tgts.append(int(m.group(3), 16))
    return sorted(set(tgts))


def relocs(obj):
    """offset -> (type, symbol name, resolved value)"""
    out = subprocess.run([READELF, "-r", obj], capture_output=True, text=True).stdout
    r = {}
    for line in out.splitlines():
        m = re.match(r"^([0-9a-f]{16})\s+[0-9a-f]{16}\s+(\S+)\s+([0-9a-f]{16})\s+(.*)$",
                     line.strip())
        if not m:
            continue
        off, typ, val, rest = int(m.group(1), 16), m.group(2), int(m.group(3), 16), m.group(4)
        if typ == "R_RISCV_RELAX":
            continue
        name = rest.split("+")[0].strip()
        add = 0
        if "+" in rest:
            try:
                add = int(rest.split("+")[-1].strip(), 0)
            except ValueError:
                add = 0
        r.setdefault(off, []).append((typ, name, val + add))
    return r


def symbols(obj):
    """name -> (value, size) for FUNC symbols in .text"""
    out = subprocess.run([OBJDUMP, "-t", obj], capture_output=True, text=True).stdout
    # objdump -t: "<16 hex addr> <7-char flags><section>\t<16 hex size> <name>"
    syms = {}
    for line in out.splitlines():
        if "\t" not in line or not re.match(r"^[0-9a-f]{16} ", line):
            continue
        left, right = line.split("\t", 1)
        val = int(left[:16], 16)
        flags = left[17:24]
        sec = left[24:].strip()
        parts = right.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            size = int(parts[0], 16)
        except ValueError:
            continue
        name = parts[1].strip()
        if sec == ".text" and size > 0 and "F" in flags:
            syms[name] = (val, size)
    return syms


def disasm(obj):
    return subprocess.run([OBJDUMP, "-d", "--no-show-raw-insn", obj],
                          capture_output=True, text=True).stdout


def measure(obj, fn, dis_text=None):
    dis = dis_text if dis_text is not None else disasm(obj)
    rel = relocs(obj)
    syms = symbols(obj)
    if fn not in syms:
        return None, None
    lo, size = syms[fn]
    hi = lo + size

    cur = None
    lines = []
    for line in dis.splitlines():
        h = HDR_RE.match(line.strip())
        if h:
            cur = h.group(2)
            continue
        if cur != fn:
            continue
        m = INSN_RE.match(line)
        if m:
            lines.append((int(m.group(1), 16), m.group(2), m.group(3).strip(), line.rstrip()))

    res = dict(instructions=0, branches=0, jumps=0, calls=0, callees=[],
               back_edges=0, back_edge_spans=[], memory=0, loads=0, stores=0,
               multiply_divide=0, muldiv_ops={})
    for off, mn, ops, _raw in lines:
        res["instructions"] += 1
        if mn in MEM:
            res["memory"] += 1
            if mn.replace("c.", "").startswith("s"):
                res["stores"] += 1
            else:
                res["loads"] += 1
        if mn in MULDIV:
            res["multiply_divide"] += 1
            res["muldiv_ops"][mn] = res["muldiv_ops"].get(mn, 0) + 1

        is_br = mn in BRANCH
        is_jp = mn in JUMP and mn != "ret"
        if not (is_br or is_jp):
            continue
        if is_br:
            res["branches"] += 1
        if is_jp:
            res["jumps"] += 1

        # resolve the target
        tgt = None
        callee = None
        for typ, name, val in rel.get(off, []):
            if typ in ("R_RISCV_BRANCH", "R_RISCV_JAL", "R_RISCV_CALL",
                       "R_RISCV_CALL_PLT", "R_RISCV_RVC_BRANCH", "R_RISCV_RVC_JUMP"):
                if name.startswith(".L") or name in ("", ".text"):
                    tgt = val
                else:
                    callee = name
        if tgt is None and callee is None:
            m = TGT_RE.search(ops)
            if m:
                t = int(m.group(1), 16)
                if lo <= t < hi:
                    tgt = t
        # auipc/jalr call pair: the relocation sits on the auipc, one insn earlier
        if callee is None and mn in ("jalr", "jr", "jal"):
            for typ, name, val in rel.get(off - 4, []):
                if typ in ("R_RISCV_CALL", "R_RISCV_CALL_PLT") and not name.startswith(".L"):
                    callee = name
        if callee:
            res["calls"] += 1
            res["callees"].append(callee)
        if tgt is not None and lo <= tgt < hi and tgt <= off:
            res["back_edges"] += 1
            res["back_edge_spans"].append(
                "0x%x->0x%x (%d insns)" % (off, tgt, (off - tgt) // 4 + 1))

    res["callees"] = sorted(set(res["callees"]))
    res["size_bytes"] = size
    other = [s for s in syms if s != fn]
    res["other_symbols_in_object"] = sorted(other)

    # -- real control-flow: a BACKWARD target is not the same thing as a loop. --
    # The compiler lays common join blocks (epilogue, shared return path) ahead
    # of the code that jumps to them, so plenty of backward jumps close no cycle.
    # A natural loop back-edge is an edge u->v where v DOMINATES u.
    res.update(cfg_loops(lines, rel, lo, hi, jump_table_targets(obj)))
    res["backward_targets"] = res["back_edges"]      # literal count, as asked
    return res, dis


def cfg_loops(lines, rel, lo, hi, jtab=()):
    """Instruction-level CFG, dominators, natural-loop back-edges."""
    offs = [o for o, _, _, _ in lines]
    idx = {o: i for i, o in enumerate(offs)}
    succ = {o: [] for o in offs}
    indirect = []
    for i, (off, mn, ops, _raw) in enumerate(lines):
        nxt = offs[i + 1] if i + 1 < len(offs) else None

        def local_target():
            for typ, name, val in rel.get(off, []):
                if typ.startswith("R_RISCV") and "BRANCH" in typ or typ in (
                        "R_RISCV_JAL", "R_RISCV_RVC_JUMP", "R_RISCV_RVC_BRANCH"):
                    if name.startswith(".L") or name in ("", ".text"):
                        return val
            m = TGT_RE.search(ops)
            if m:
                t = int(m.group(1), 16)
                if lo <= t < hi:
                    return t
            return None

        def is_extern_call():
            for typ, name, val in rel.get(off - 4, []):
                if typ in ("R_RISCV_CALL", "R_RISCV_CALL_PLT") and not name.startswith(".L"):
                    return True
            for typ, name, val in rel.get(off, []):
                if typ in ("R_RISCV_CALL", "R_RISCV_CALL_PLT", "R_RISCV_JAL") \
                        and not name.startswith(".L") and name not in ("", ".text"):
                    return True
            return False

        if mn == "ret":
            continue
        if mn in BRANCH:
            t = local_target()
            if nxt is not None:
                succ[off].append(nxt)
            if t is not None:
                succ[off].append(t)
            continue
        if mn in ("j", "jal", "c.j", "c.jal", "jr", "jalr", "c.jr", "c.jalr", "tail", "call"):
            ext = is_extern_call()
            if ext:
                # a call returns to the next instruction; a TAIL call (jr/j via t1)
                # leaves the function and has no in-function successor.
                if mn in ("jal", "jalr", "call") and ("ra" in ops or mn == "call"):
                    if nxt is not None:
                        succ[off].append(nxt)
                continue
            t = local_target()
            if t is not None:
                succ[off].append(t)
            elif mn in ("jr", "jalr", "c.jr", "c.jalr"):
                # switch dispatch: successors are the .rodata jump-table entries
                jt = [t for t in jtab if lo <= t < hi]
                if jt:
                    succ[off].extend(jt)
                    indirect.append({"at": hex(off), "table_targets":
                                     [hex(t) for t in jt]})
                else:
                    indirect.append({"at": hex(off), "table_targets": None})
            elif nxt is not None:
                succ[off].append(nxt)
            continue
        if nxt is not None:
            succ[off].append(nxt)

    # iterative dominators over the reachable subgraph
    entry = offs[0]
    pred = {o: [] for o in offs}
    for u in offs:
        for v in succ[u]:
            if v in pred:
                pred[v].append(u)
    order = []
    seen = {entry}
    stack = [entry]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in succ[u]:
            if v in seen or v not in idx:
                continue
            seen.add(v)
            stack.append(v)
    order.sort(key=lambda o: idx[o])
    allset = frozenset(seen)
    dom = {o: allset for o in seen}
    dom[entry] = frozenset([entry])
    changed = True
    while changed:
        changed = False
        for u in order:
            if u == entry:
                continue
            ps = [p for p in pred[u] if p in seen]
            if not ps:
                continue
            new = frozenset.intersection(*[dom[p] for p in ps]) | {u}
            if new != dom[u]:
                dom[u] = new
                changed = True

    loops = []
    for u in seen:
        for v in succ[u]:
            if v in seen and v in dom[u] and v != u or (v == u and u in succ[u]):
                if v in dom.get(u, ()) :
                    loops.append((u, v))
    loops = sorted(set(loops))
    return {
        "loop_back_edges": len(loops),
        "loop_back_edge_spans": ["0x%x->0x%x (%d insns)" % (u, v, idx[u] - idx[v] + 1)
                                 for u, v in loops],
        "has_loop": len(loops) > 0,
        "unreachable_insns": len(offs) - len(seen),
        "indirect_jumps": indirect,
    }


def main():
    mapping = json.load(open(os.path.join(SCRATCH, "mapping.json")))
    out = {}
    failures = []
    for march, key in (("rv64im", "rv64im"), ("rv64i", "rv64i")):
        odir = os.path.join(SCRATCH, "obj_" + key)
        os.makedirs(odir, exist_ok=True)
        for ent in mapping:
            sf = ent["sf"]
            cfile = os.path.join(SF, "source", sf + ".c")
            obj = os.path.join(odir, sf + ".o")
            if not os.path.exists(cfile):
                failures.append((march, sf, "no source file " + cfile))
                continue
            rc, err, cmd = compile_one(cfile, obj, march)
            if rc != 0:
                failures.append((march, sf, "compile failed: " + err[:300]))
                continue
            r, dis = measure(obj, sf)
            if r is None:
                failures.append((march, sf, "symbol %s not found in object" % sf))
                continue
            e = out.setdefault(sf, {"function": sf,
                                    "sail_externals": [m["sail"] for m in mapping if m["sf"] == sf],
                                    "source": cfile})
            if key == "rv64im":
                e.update(r)
                e["instructions_rv64im"] = r["instructions"]
            else:
                e["instructions_rv64i"] = r["instructions"]
                e["rv64i"] = r
            if sf == "f64_div" and key == "rv64im":
                with open(os.path.join(SCRATCH, "softfloat_f64_div.txt"), "w") as fh:
                    fh.write("# clang command:\n# " + cmd + "\n#\n")
                    fh.write("# Branch/jump targets in an unlinked .o are carried by relocations;\n"
                             "# the resolved targets are listed after the disassembly.\n\n")
                    fh.write(dis)
                    fh.write("\n\n=== resolved relocations (llvm-readelf -r) ===\n")
                    fh.write(subprocess.run([READELF, "-r", obj],
                                            capture_output=True, text=True).stdout)
                    fh.write("\n=== measured ===\n")
                    fh.write(json.dumps(r, indent=2))

    # ---- transitive closure: the internal helpers the 67 entry points call ----
    # f64_add is only 8 instructions because it tail-calls softfloat_addMagsF64.
    # Sizing the Lean work honestly means measuring the callees too.
    def find_source(sym):
        """softfloat_addMagsF64 -> s_addMagsF64.c ; softfloat_raiseFlags -> itself"""
        base = sym[len("softfloat_"):] if sym.startswith("softfloat_") else sym
        for cand in ("s_" + base, sym, base):
            for sub in ("source", "source/RISCV"):
                p = os.path.join(SF, sub, cand + ".c")
                if os.path.exists(p):
                    return p, cand
        return None, None

    entry_names = set(out)
    frontier = set()
    for e in out.values():
        frontier |= set(e["callees"])
    done = set(entry_names)
    closure = {}
    while frontier:
        sym = frontier.pop()
        if sym in done:
            continue
        done.add(sym)
        if sym.startswith("__"):          # libgcc: not part of SoftFloat
            closure[sym] = {"function": sym, "role": "compiler_runtime",
                            "note": "libgcc helper, no SoftFloat source"}
            continue
        cfile, base = find_source(sym)
        if cfile is None:
            failures.append(("rv64im", sym, "no source file found for callee"))
            continue
        ent = {"function": sym, "role": "internal_callee", "source": cfile}
        for march, key in (("rv64im", "rv64im"), ("rv64i", "rv64i")):
            odir = os.path.join(SCRATCH, "obj_" + key)
            obj = os.path.join(odir, base + ".o")
            rc, err, _cmd = compile_one(cfile, obj, march)
            if rc != 0:
                failures.append((march, sym, "compile failed: " + err[:200]))
                break
            r, _ = measure(obj, sym)
            if r is None:
                failures.append((march, sym, "symbol not found in object"))
                break
            if key == "rv64im":
                ent.update(r)
                ent["instructions_rv64im"] = r["instructions"]
                frontier |= set(r["callees"]) - done
            else:
                ent["instructions_rv64i"] = r["instructions"]
                ent["rv64i"] = r
        closure[sym] = ent
    for e in out.values():
        e["role"] = "model_external"
    out.update(closure)

    with open(os.path.join(SCRATCH, "softfloat_measure.json"), "w") as fh:
        json.dump({"compile_command_rv64im":
                   " ".join([CLANG, "--target=riscv64-unknown-elf", "-march=rv64im",
                             "-mabi=lp64", "-O2", "-c",
                             "-Werror-implicit-function-declaration"] + DEFINES +
                            INCLUDES + ["<SOURCE>/source/<fn>.c", "-o", "<fn>.o"]),
                   "n_sail_externals": len(mapping),
                   "n_functions": len(out),
                   "n_model_externals_measured": sum(
                       1 for v in out.values() if v.get("role") == "model_external"),
                   "n_internal_callees_measured": sum(
                       1 for v in out.values() if v.get("role") == "internal_callee"),
                   "failures": [{"march": a, "function": b, "reason": c} for a, b, c in failures],
                   "functions": out}, fh, indent=1)
    print("measured %d functions, %d failures" % (len(out), len(failures)))
    for f in failures:
        print("  FAIL", f)


if __name__ == "__main__":
    main()
