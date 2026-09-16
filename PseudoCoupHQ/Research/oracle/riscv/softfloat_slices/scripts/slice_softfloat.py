#!/usr/bin/env python3
"""
TRUE SLICE of every RISC-V float operation.

For each of the 67 externals the Sail RISC-V model declares in
model/core/softfloat_interface.sail, build the SMALLEST CORRECT BODY:

  * compile the operation and every transitive callee to LLVM bitcode for
    riscv64 (the RISCV specialisation of Berkeley SoftFloat, vendored in the
    sail-riscv tree),
  * link them,
  * internalize everything except the operation, inline, and dead-code
    eliminate, so paths this caller can never reach disappear,
  * lower the survivor to riscv64 (rv64im) and count it.

This differs from softfloat_measure.json, which measured every function
SEPARATELY: that reports f64_div as 150 own instructions plus 186 in four
helper bodies = 336 upper bound.  The true slice is 302.

Read-only on the sources.  Everything is written under SCRATCH.

Branch and jump targets inside an unlinked .o are carried by relocations (the
encoded immediate is 0) and no riscv64 linker is installed, so control flow is
resolved from `llvm-readelf -r`.  That analysis is shared verbatim with
measure_softfloat.py, which is imported rather than copied.
"""

import json
import os
import re
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")   # no machine path is written into this file

SF = (HOME + "/Programming/SOURCES/sail-riscv/dependencies/softfloat/"
      "berkeley-softfloat-3")
SCRATCH = ("/tmp/claude-1000/-home-<user>-Programming/"
           "6fc7a103-e75c-45df-aff2-b85555e7a824/scratchpad")
B = "/usr/lib/llvm-21/bin"
CLANG = "clang"

sys.path.insert(0, SCRATCH)
import measure_softfloat as M          # noqa: E402  (measure/relocs/cfg_loops)

DEFINES = [
    "-DSOFTFLOAT_FAST_INT64",
    "-DSOFTFLOAT_ROUND_ODD",
    "-DINLINE_LEVEL=5",
    "-DSOFTFLOAT_FAST_DIV32TO16",
    "-DSOFTFLOAT_FAST_DIV64TO32",
]
INCLUDES = [
    "-I" + SF + "/build/Linux-RISCV64-GCC",   # platform.h
    "-I" + SF + "/source/RISCV",              # specialize.h  (RISCV, never 8086)
    "-I" + SF + "/source/include",
    # f32_to_bf16.c includes <inttypes.h> and <stdio.h> it never uses; the
    # bare-metal riscv64 target has no libc headers, so a shim satisfies them.
    "-idirafter", SCRATCH + "/shim",
]

# The only two source directories ever consulted.  Consulting 8086/,
# ARM-VFPv2/, ARM-VFPv2-defaultNaN/ as well would link two specialisations of
# the same function, which is always wrong.
SRC_DIRS = ("source", "source/RISCV")

OPT_PASSES = ("internalize,always-inline,inline,globaldce,"
              "instcombine,simplifycfg,dce,globaldce")
# f64_sqrt alone makes InstCombine need a second iteration, and this LLVM build
# asserts that it converges in one ("did not reach a fixpoint after 1
# iterations").  LLVM's own suggested remedy is to drop that self-check; it
# changes no transform.  Verified: with this variant every one of the other 66
# slices comes out at exactly the same instruction count, f64_div included.
OPT_PASSES_NOFIX = OPT_PASSES.replace("instcombine,",
                                      "instcombine<no-verify-fixpoint>,")

WORK = os.path.join(SCRATCH, "work")
BCDIR = os.path.join(WORK, "bc")
OUTDIR = os.path.join(SCRATCH, "slices")


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, (p.stderr or "").strip()


# ------------------------------------------------------------- bitcode ------
_bc_cache = {}


def to_bitcode(cfile):
    """Compile one SoftFloat .c to riscv64 bitcode at -O1.  Cached by path."""
    if cfile in _bc_cache:
        return _bc_cache[cfile]
    base = os.path.basename(cfile)[:-2]
    # RISCV/s_propagateNaNF64UI.c and a hypothetical source/s_propagateNaNF64UI.c
    # would collide on basename; qualify by directory.
    tag = "RISCV_" + base if "/RISCV/" in cfile else base
    out = os.path.join(BCDIR, tag + ".bc")
    cmd = [CLANG, "--target=riscv64-unknown-elf", "-march=rv64im", "-mabi=lp64",
           "-O1", "-Werror-implicit-function-declaration"] + DEFINES + INCLUDES + \
          ["-emit-llvm", "-c", cfile, "-o", out]
    rc, _, err = run(cmd)
    res = (out if rc == 0 else None, err)
    _bc_cache[cfile] = res
    return res


_nm_cache = {}


def nm(bcfile):
    """-> (defined_text_syms, undefined_syms)"""
    if bcfile in _nm_cache:
        return _nm_cache[bcfile]
    rc, out, _ = run([B + "/llvm-nm", bcfile])
    defined, undef = set(), set()
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        typ, name = parts[-2], parts[-1]
        if typ == "U":
            undef.add(name)
        elif typ in ("T", "t", "W", "w"):
            defined.add(name)
    _nm_cache[bcfile] = (defined, undef)
    return defined, undef


# ------------------------------------------------- symbol -> source file ----
def find_source(sym):
    """softfloat_addMagsF64 -> source/s_addMagsF64.c
       softfloat_raiseFlags -> source/RISCV/softfloat_raiseFlags.c
    Only source/ and source/RISCV/ are consulted, so no two specialisations of
    the same function can ever be linked together.  The candidate must really
    DEFINE the symbol as text, which is what keeps the data globals
    (softfloat_exceptionFlags, softfloat_roundingMode, softfloat_detectTininess)
    from dragging softfloat_state.c into the link."""
    base = sym[len("softfloat_"):] if sym.startswith("softfloat_") else sym
    for cand in ("s_" + base, sym, base):
        for sub in SRC_DIRS:
            p = os.path.join(SF, sub, cand + ".c")
            if not os.path.exists(p):
                continue
            bc, _err = to_bitcode(p)
            if bc is None:
                continue
            defined, _ = nm(bc)
            if sym in defined:
                return p
    return None


# ------------------------------------------------------------- closure ------
def link_closure(op):
    """Fixed point: start from <op>.c, link, look at what is still undefined,
    pull in the file that defines it, repeat.  Returns (files, bcs, unresolved)."""
    entry = os.path.join(SF, "source", op + ".c")
    files = [entry]
    seen = {entry}
    unresolved = set()
    while True:
        bcs = []
        for f in files:
            bc, err = to_bitcode(f)
            if bc is None:
                raise RuntimeError("compile failed for %s: %s" % (f, err[:400]))
            bcs.append(bc)
        undef = set()
        for bc in bcs:
            _, u = nm(bc)
            undef |= u
        defined = set()
        for bc in bcs:
            d, _ = nm(bc)
            defined |= d
        todo = sorted(undef - defined - unresolved)
        added = False
        for sym in todo:
            if sym.startswith("__"):          # libgcc: not part of SoftFloat
                unresolved.add(sym)
                continue
            p = find_source(sym)
            if p is None:
                unresolved.add(sym)           # data global, or genuinely missing
                continue
            if p not in seen:
                seen.add(p)
                files.append(p)
                added = True
        if not added:
            return files, bcs, sorted(unresolved)


# --------------------------------------------------------------- slice ------
def build_slice(op, files, bcs, wdir):
    linked = os.path.join(wdir, "linked.bc")
    rc, _, err = run([B + "/llvm-link"] + bcs + ["-o", linked])
    if rc:
        raise RuntimeError("llvm-link: " + err[:400])
    sbc = os.path.join(wdir, "slice.bc")
    passes = OPT_PASSES
    rc, _, err = run([B + "/opt", "-passes=" + passes,
                      "-internalize-public-api-list=" + op, linked, "-o", sbc])
    if rc and "did not reach a fixpoint" in err:
        passes = OPT_PASSES_NOFIX
        rc, _, err = run([B + "/opt", "-passes=" + passes,
                          "-internalize-public-api-list=" + op, linked, "-o", sbc])
    if rc:
        raise RuntimeError("opt: " + err[:400])
    sobj = os.path.join(wdir, "slice.o")
    rc, _, err = run([B + "/llc", "-march=riscv64", "-mattr=+m", "-O2",
                      "-filetype=obj", sbc, "-o", sobj])
    if rc:
        raise RuntimeError("llc: " + err[:400])
    return linked, sbc, sobj, passes


def build_forced_slice(op, linked, wdir, passes, others):
    """Same pipeline, but every non-entry function is first marked
    `alwaysinline` so the inliner's cost model cannot decline one.  This is the
    number that matters for the symbolic walker: ONE body, no calls, even where
    a helper has several call sites and the ordinary heuristic keeps it out of
    line.  It can exceed the upper bound, because a helper inlined at N sites is
    counted N times."""
    fbc = os.path.join(wdir, "forced.bc")
    fp = passes.replace("internalize,", "internalize,forceattrs,")
    cmd = [B + "/opt", "-passes=" + fp, "-internalize-public-api-list=" + op]
    for s in others:
        cmd.append("-force-attribute=" + s + ":alwaysinline")
    cmd += [linked, "-o", fbc]
    rc, _, err = run(cmd)
    if rc and "did not reach a fixpoint" in err:
        fp = fp.replace("instcombine,", "instcombine<no-verify-fixpoint>,")
        cmd[1] = "-passes=" + fp
        rc, _, err = run(cmd)
    if rc:
        return None, None, "opt(forced): " + err[:300]
    fobj = os.path.join(wdir, "forced.o")
    rc, _, err = run([B + "/llc", "-march=riscv64", "-mattr=+m", "-O2",
                      "-filetype=obj", fbc, "-o", fobj])
    if rc:
        return None, None, "llc(forced): " + err[:300]
    return fbc, fobj, None


def per_symbol_counts(obj, dis):
    """instructions per symbol in the object, so a slice that kept a helper
    out of line can still be totalled honestly."""
    counts, cur = {}, None
    for line in dis.splitlines():
        h = M.HDR_RE.match(line.strip())
        if h:
            cur = h.group(2)
            counts.setdefault(cur, 0)
            continue
        if cur and M.INSN_RE.match(line):
            counts[cur] += 1
    return counts


# ------------------------------------------------------------ upper bound ---
def measured_closure(prev, op):
    """Transitive callees of `op` in the separate-compilation measurement."""
    seen, frontier, res = set(), [op], set()
    while frontier:
        s = frontier.pop()
        if s in seen:
            continue
        seen.add(s)
        if s != op:
            res.add(s)
        for c in prev.get(s, {}).get("callees", []):
            if c not in seen:
                frontier.append(c)
    return res


def main():
    for d in (WORK, BCDIR, OUTDIR):
        os.makedirs(d, exist_ok=True)
    mapping = json.load(open(os.path.join(SCRATCH, "mapping.json")))
    prev = json.load(open(os.path.join(SCRATCH, "softfloat_measure.json")))["functions"]

    results, failures = {}, []
    for ent in mapping:
        op = ent["sf"]
        wdir = os.path.join(WORK, op)
        shutil.rmtree(wdir, ignore_errors=True)
        os.makedirs(wdir, exist_ok=True)
        try:
            files, bcs, unresolved = link_closure(op)
            linked, sbc, sobj, passes = build_slice(op, files, bcs, wdir)
        except Exception as exc:                     # noqa: BLE001
            failures.append({"function": op, "reason": str(exc)[:500]})
            continue

        dis = M.disasm(sobj)
        r, _ = M.measure(sobj, op, dis)
        if r is None:
            failures.append({"function": op,
                             "reason": "entry symbol not found in slice.o"})
            continue

        # every symbol the slice still contains, and every call still in it
        allsyms = sorted(M.symbols(sobj))
        psym = per_symbol_counts(sobj, dis)

        # forced-inline variant: one body, guaranteed
        defined, _u = nm(linked)
        others = sorted(s for s in defined if s != op)
        fbc, fobj, ferr = build_forced_slice(op, linked, wdir, passes, others)
        forced = None
        if fobj:
            fdis = M.disasm(fobj)
            fr, _ = M.measure(fobj, op, fdis)
            if fr:
                fsyms = sorted(M.symbols(fobj))
                forced = {
                    "instructions": fr["instructions"],
                    "all_symbols_instructions": sum(per_symbol_counts(fobj, fdis).values()),
                    "surviving_symbols": fsyms,
                    "calls_remaining": fr["calls"],
                    "calls_remaining_callees": fr["callees"],
                    "branches": fr["branches"], "jumps": fr["jumps"],
                    "back_edges": fr["back_edges"],
                    "loop_back_edges": fr["loop_back_edges"],
                    "loads": fr["loads"], "stores": fr["stores"],
                    "multiply_divide": fr["multiply_divide"],
                    "indirect_jumps": fr["indirect_jumps"],
                }
                with open(os.path.join(OUTDIR, op + ".forced.txt"), "w") as fh:
                    fh.write("# %s, every helper forced inline (one body)\n\n" % op)
                    fh.write(fdis)
                    fh.write("\n=== resolved relocations ===\n")
                    fh.write(run([B + "/llvm-readelf", "-r", fobj])[1])
        tcl = measured_closure(prev, op)
        own = prev.get(op, {}).get("instructions")
        helpers_sum = sum(prev[x]["instructions"] for x in tcl
                          if "instructions" in prev.get(x, {}))
        unmeasured = sorted(x for x in tcl if "instructions" not in prev.get(x, {}))
        upper = (own + helpers_sum) if own is not None else None

        rec = {
            "function": op,
            "sail_externals": [m["sail"] for m in mapping if m["sf"] == op],
            "own_body": own,
            "upper_bound": upper,
            "slice": r["instructions"],
            "slice_all_symbols": sum(psym.values()),
            "per_symbol_instructions": psym,
            "forced_inline": forced,
            "forced_inline_error": ferr,
            "branches": r["branches"],
            "jumps": r["jumps"],
            "back_edges": r["back_edges"],
            "loop_back_edges": r["loop_back_edges"],
            "back_edge_spans": r["back_edge_spans"],
            "loop_back_edge_spans": r["loop_back_edge_spans"],
            "has_loop": r["has_loop"],
            "loads": r["loads"],
            "stores": r["stores"],
            "memory": r["memory"],
            "multiply_divide": r["multiply_divide"],
            "muldiv_ops": r["muldiv_ops"],
            "calls_remaining": r["calls"],
            "calls_remaining_callees": r["callees"],
            "indirect_jumps": r["indirect_jumps"],
            "helpers_inlined": len(files) - 1,
            "source_files_linked": len(files),
            "helper_sources": [os.path.relpath(f, SF) for f in files[1:]],
            "transitive_callees_measured": sorted(tcl),
            "unmeasured_callees": unmeasured,
            "unresolved_externals": unresolved,
            "surviving_symbols": allsyms,
            "extra_surviving_symbols": [s for s in allsyms if s != op],
            "unreachable_insns": r["unreachable_insns"],
            "size_bytes": r["size_bytes"],
            "reduction_vs_upper_bound": (upper - r["instructions"]) if upper else None,
            "larger_than_upper_bound": bool(upper and sum(psym.values()) > upper),
            "forced_larger_than_upper_bound": bool(
                upper and forced and forced["instructions"] > upper),
            "clean": (r["calls"] == 0 and len(allsyms) == 1),
            "opt_passes": passes,
            "used_instcombine_fixpoint_fallback": passes != OPT_PASSES,
        }
        results[op] = rec

        with open(os.path.join(OUTDIR, op + ".txt"), "w") as fh:
            fh.write("# TRUE SLICE of %s  (sail: %s)\n" %
                     (op, ", ".join(rec["sail_externals"])))
            fh.write("# source files linked (%d): %s\n" %
                     (len(files), ", ".join(os.path.relpath(f, SF) for f in files)))
            fh.write("# own body %s, upper bound %s, SLICE %d\n" %
                     (own, upper, r["instructions"]))
            fh.write("# still-undefined externals (data globals / libgcc): %s\n" %
                     (", ".join(unresolved) or "none"))
            fh.write("#\n# Branch/jump targets in an unlinked .o live in the\n"
                     "# relocations; the resolved table follows the disassembly.\n\n")
            fh.write(dis)
            fh.write("\n\n=== resolved relocations (llvm-readelf -r) ===\n")
            fh.write(run([B + "/llvm-readelf", "-r", sobj])[1])
            fh.write("\n=== measured ===\n")
            fh.write(json.dumps(rec, indent=2))
        shutil.copy(os.path.join(wdir, "slice.o"),
                    os.path.join(OUTDIR, op + ".slice.o"))
        shutil.copy(os.path.join(wdir, "slice.bc"),
                    os.path.join(OUTDIR, op + ".slice.bc"))

    slices = [v["slice"] for v in results.values()]
    slices.sort()
    n = len(slices)
    summary = {
        "method": {
            "compile": (CLANG + " --target=riscv64-unknown-elf -march=rv64im "
                        "-mabi=lp64 -O1 " + " ".join(DEFINES) + " " +
                        " ".join(INCLUDES) + " -emit-llvm -c <src>.c -o <src>.bc"),
            "link": B + "/llvm-link *.bc -o linked.bc",
            "slice": (B + "/opt -passes='" + OPT_PASSES +
                      "' -internalize-public-api-list=<op> linked.bc -o slice.bc"),
            "lower": B + "/llc -march=riscv64 -mattr=+m -O2 -filetype=obj "
                     "slice.bc -o slice.o",
            "count": B + "/llvm-objdump -d --no-show-raw-insn slice.o",
            "note": ("own_body and upper_bound come from softfloat_measure.json "
                     "(separate compilation at -O2); slice is this pipeline. "
                     "back_edges is the literal count of backward branch/jump "
                     "targets; loop_back_edges is the dominator-verified natural "
                     "loop count."),
            "unresolved_externals_note": (
                "Only FUNCTION definitions are linked, so the SoftFloat state "
                "globals (softfloat_exceptionFlags, softfloat_roundingMode, "
                "softfloat_detectTininess) and the two sqrt lookup tables "
                "(softfloat_approxRecipSqrt_1k0s/_1k1s, in "
                "source/s_approxRecipSqrt_1Ks.c) stay undefined.  They are data, "
                "not code.  Verified on f64_sqrt: linking "
                "s_approxRecipSqrt_1Ks.c as well leaves the slice at exactly 260 "
                "instructions in one symbol, because the tables are indexed "
                "dynamically and nothing folds.  The symbolic walker will still "
                "need the table CONTENTS for f16/f32/f64_sqrt."),
            "slice_vs_slice_all_symbols": (
                "slice is the entry symbol.  slice_all_symbols adds any helper "
                "the inliner declined to fold in (the six add/sub operations "
                "keep softfloat_roundPackToF<n> out of line because inlining "
                "would duplicate it across two call sites).  forced_inline is "
                "the same pipeline with every helper marked alwaysinline: one "
                "body, zero calls, for all 67."),
        },
        "n_operations": n,
        "n_failures": len(failures),
        "failures": failures,
        "sum_of_slices": sum(slices),
        "sum_of_own_bodies": sum(v["own_body"] for v in results.values()
                                 if v["own_body"] is not None),
        "sum_of_upper_bounds": sum(v["upper_bound"] for v in results.values()
                                   if v["upper_bound"] is not None),
        "largest_slice": max(results.items(), key=lambda kv: kv[1]["slice"])[0] if n else None,
        "largest_slice_insns": slices[-1] if n else None,
        "smallest_slice": min(results.items(), key=lambda kv: kv[1]["slice"])[0] if n else None,
        "smallest_slice_insns": slices[0] if n else None,
        "median_slice_insns": (slices[n // 2] if n % 2 else
                               (slices[n // 2 - 1] + slices[n // 2]) / 2) if n else None,
        "n_with_calls_remaining": sum(1 for v in results.values()
                                      if v["calls_remaining"]),
        "with_calls_remaining": {k: v["calls_remaining_callees"]
                                 for k, v in results.items() if v["calls_remaining"]},
        "n_with_back_edge": sum(1 for v in results.values() if v["back_edges"]),
        "n_with_loop": sum(1 for v in results.values() if v["loop_back_edges"]),
        "with_loop": sorted(k for k, v in results.items() if v["loop_back_edges"]),
        "n_with_indirect_jump": sum(1 for v in results.values()
                                    if v["indirect_jumps"]),
        "with_indirect_jump": sorted(k for k, v in results.items()
                                     if v["indirect_jumps"]),
        "n_clean": sum(1 for v in results.values() if v["clean"]),
        "sum_of_slices_all_symbols": sum(v["slice_all_symbols"]
                                         for v in results.values()),
        "sum_of_forced_inline": sum(v["forced_inline"]["instructions"]
                                    for v in results.values() if v["forced_inline"]),
        "n_forced_inline_clean": sum(
            1 for v in results.values() if v["forced_inline"]
            and v["forced_inline"]["calls_remaining"] == 0
            and len(v["forced_inline"]["surviving_symbols"]) == 1),
        "larger_than_upper_bound": sorted(k for k, v in results.items()
                                          if v["larger_than_upper_bound"]),
        "forced_larger_than_upper_bound": sorted(
            k for k, v in results.items() if v["forced_larger_than_upper_bound"]),
        "operations": results,
    }
    with open(os.path.join(SCRATCH, "softfloat_slices.json"), "w") as fh:
        json.dump(summary, fh, indent=1)

    print("sliced %d/%d operations, %d failures" % (n, len(mapping), len(failures)))
    for f in failures:
        print("  FAIL", f["function"], f["reason"][:200])
    if "f64_div" in results:
        print("f64_div slice =", results["f64_div"]["slice"],
              "(expected 302)", "OK" if results["f64_div"]["slice"] == 302 else "MISMATCH")


if __name__ == "__main__":
    main()
