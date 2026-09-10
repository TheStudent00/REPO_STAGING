#!/usr/bin/env python3
"""riscv_carve.py -- COMPILE ONE UNIT'S OWN SOURCE FOR riscv64 AND CARVE ITS
BODY AT THE FUNCTION SYMBOL.

Node: hq.research.arch_unit_oracle.  Task rv1, brief section 2.

WHAT THIS FILE IS, one sentence: the riscv64 twin of `op_pipeline/
lane_gen.py`'s steps 2 and 3 -- the same two acts (compile at the corpus's
own ship optimisation level, then read the function's instructions back out
of the object with a disassembler) aimed at a different architecture.

WHAT CHANGED FROM THE x86 ROUTE, said out loud, because section 5 of the
brief counts exactly this:
  * the compiler is told the target: `--target=riscv64-unknown-linux-gnu`
    for clang, `GOARCH=riscv64 GOOS=linux` for go.  The optimisation level
    is the corpus's own and is NOT touched: clang -O1, go build with no
    flags.
  * the compile line gains `-nostdlibinc`.  The image has no riscv64
    glibc headers, so the probe's own `#include <stdint.h>` reaches
    `/usr/include/stdint.h`, which is the x86-64 build's, and refuses at
    `bits/libc-header-start.h` (lane 4 quotes it).  `-nostdlibinc` sends
    the include to clang's own resource headers, which are per-target.
    The OPTIMISATION LEVEL is untouched.
  * the disassembler is `llvm-objdump`, because the image's binutils
    `objdump` is an x86-64 build with no riscv64 backend.  Its symbol flag
    is `--disassemble-symbols=`, not binutils' `--disassemble=`.
  * `-M no-aliases` is passed so the text carries the ARCHITECTURE's own
    mnemonics and not the assembler's reading aids (`li`, `mv`, `ret`,
    `sext.w`), which would be a second spelling of instructions the model
    already names.  llvm-objdump has no `--no-aliases`; `-M no-aliases`
    is its own spelling (lane 4 quotes the refusal).
  * a go riscv64 binary carries no RISC-V attribute section, so the
    disassembler decodes its compressed halfwords as `<unknown>`;
    `--mattr=+m,+a,+f,+d,+c` names the extensions instead (lane 5).
  * the body is bounded by the SYMBOL'S OWN SIZE, read from the symbol
    table, because a go binary lays the next function's padding inside
    the same disassembly block.

THE CALLING CONVENTION THIS CARVE ASSUMES, stated rather than implied
(the RISC-V psABI, `lp64d`): integer arguments arrive in a0..a7 (x10..x17)
in order, an integer answer leaves in a0; floating-point arguments arrive
in fa0..fa7 (f10..f17) and a floating-point answer leaves in fa0; there is
NO FLAGS REGISTER anywhere in the architecture -- a comparison writes a
general register.

usage:
  riscv_carve.py <units.json> <out carved.json> <work dir>
"""

import json
import os
import re
import subprocess
import sys


CLANG = "clang"
LLVM_OBJDUMP = "llvm-objdump"

# the corpus's own ship optimisation level, per language, with the target
# added and nothing else changed.
SHIP = {
    "c": ["-std=c17", "-O1", "--target=riscv64-unknown-linux-gnu",
          "-nostdlibinc"],
}

# the extensions a go riscv64 binary uses but does not declare
MATTR = "+m,+a,+f,+d,+c"

GO_ENV = {
    "GOARCH": "riscv64",
    "GOOS": "linux",
    "GOTOOLCHAIN": "local",
    "GOPROXY": "off",
    "GOFLAGS": "-mod=mod",
}

GOMOD = "module opprobe\n\ngo 1.26\n"

LABEL = re.compile(r"^([0-9a-f]+)\s+<(.+)>:\s*$")
INSN = re.compile(r"^\s*([0-9a-f]+):\s+([0-9a-f]{4,8})\s+(.*)$")


def sh(cmd, cwd=None, env=None, timeout=300):
    full = dict(os.environ)
    if env:
        full.update(env)
    try:
        p = subprocess.run(cmd, cwd=cwd, env=full, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout)
        return (p.returncode, p.stdout.decode("utf-8", "replace"),
                p.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    except OSError as exc:
        return 125, "", "OSError %s" % exc


def extract(text, symbol, exact):
    """(bytes, instruction texts, byte offsets) for one symbol, in
    llvm-objdump's own text.

    llvm-objdump prints, per instruction:
        80000004: 006283b3     	add	t2, t0, t1
    The columns are separated by tabs; the operand column is joined back to
    the mnemonic with one space so a line reads as one instruction.  A
    trailing `# comment` is objdump's arithmetic for the reader and is
    dropped, exactly as `lane_gen.extract` drops it on the x86 route.
    """
    lines = text.splitlines()
    start = -1
    for index, line in enumerate(lines):
        hit = LABEL.match(line)
        if not hit:
            continue
        label = hit.group(2)
        same = (label == symbol) if exact else (symbol in label)
        if same:
            start = index
            break
    if start < 0:
        return None
    raw = []
    body = []
    offsets = []
    base = None
    for line in lines[start + 1:]:
        if LABEL.match(line):
            break
        hit = INSN.match(line)
        if not hit:
            continue
        address = int(hit.group(1), 16)
        if base is None:
            base = address
        rest = hit.group(3)
        rest = rest.split("#")[0]
        rest = rest.replace("\t", " ")
        rest = " ".join(rest.split())
        if not rest:
            continue
        raw.append(hit.group(2))
        body.append(rest)
        offsets.append(address - base)
    return raw, body, offsets


SYMBOL_ROW = re.compile(
    r"^([0-9a-f]+)\s+\S+\s+\S*\s*\.\S+\s+([0-9a-f]+)\s+(\S+)\s*$")


def symbol_size(obj, symbol, exact):
    """the symbol's own byte length, from the symbol table, or nothing."""
    rc, out, err = sh([LLVM_OBJDUMP, "-t", obj], timeout=600)
    if rc != 0:
        return None
    for line in out.splitlines():
        hit = SYMBOL_ROW.match(line.rstrip())
        if hit is None:
            continue
        name = hit.group(3)
        same = (name == symbol) if exact else (symbol in name)
        if not same:
            continue
        return int(hit.group(2), 16)
    return None


def disassemble(obj, symbol, exact):
    cmd = [LLVM_OBJDUMP, "-dr", "-M", "no-aliases", "--mattr=" + MATTR,
           "--disassemble-symbols=" + symbol, obj]
    rc, out, err = sh(cmd)
    got = extract(out, symbol, exact) if rc == 0 else None
    if got is None:
        rc, out, err = sh([LLVM_OBJDUMP, "-dr", "-M", "no-aliases",
                           "--mattr=" + MATTR, obj], timeout=600)
        got = extract(out, symbol, exact)
    if got is None:
        return None, (err or "")
    size = symbol_size(obj, symbol, exact)
    if size is not None:
        raw, body, offsets = got
        kept_raw = []
        kept_body = []
        for index, offset in enumerate(offsets):
            if offset >= size:
                break
            kept_raw.append(raw[index])
            kept_body.append(body[index])
        return (kept_raw, kept_body), (err or "")
    raw, body, offsets = got
    return (raw, body), (err or "")


def compile_c(source, work):
    src = os.path.join(work, "unit.c")
    obj = os.path.join(work, "unit.o")
    open(src, "w").write(source)
    cmd = [CLANG] + SHIP["c"] + ["-c", src, "-o", obj]
    rc, out, err = sh(cmd)
    return rc, obj, (err or out), " ".join(cmd)


def compile_go(source, work):
    open(os.path.join(work, "go.mod"), "w").write(GOMOD)
    open(os.path.join(work, "main.go"), "w").write(source)
    obj = os.path.join(work, "bin_rv")
    cmd = ["go", "build", "-o", obj, "."]
    rc, out, err = sh(cmd, cwd=work, env=GO_ENV, timeout=600)
    return rc, obj, (err or out), "GOARCH=riscv64 GOOS=linux " + " ".join(cmd)


def carve_one(row, work_root):
    name = row["unit"].replace("/", "_")
    work = os.path.join(work_root, name)
    if not os.path.isdir(work):
        os.makedirs(work)
    if row["lang"] == "c":
        rc, obj, diag, cmdline = compile_c(row["source"], work)
    else:
        rc, obj, diag, cmdline = compile_go(row["source"], work)
    out = {"unit": row["unit"], "lang": row["lang"],
           "compile_command": cmdline, "compile_rc": rc}
    if rc != 0:
        out["outcome"] = "BUILDFAIL"
        out["diagnostic"] = diag.strip()[:600]
        return out
    got, err = disassemble(obj, row["symbol"],
                           row.get("symbol_exact", True))
    if got is None:
        out["outcome"] = "NOSYM"
        out["diagnostic"] = err.strip()[:600]
        return out
    raw, body = got
    out["outcome"] = "CARVED"
    out["bytes"] = raw
    out["body"] = body
    out["instruction_count"] = len(body)
    return out


def main():
    units_path = sys.argv[1]
    out_path = sys.argv[2]
    work_root = sys.argv[3]
    if not os.path.isdir(work_root):
        os.makedirs(work_root)
    rows = json.load(open(units_path))["rows"]
    picked = [r for r in rows if r.get("outcome") == "PICKED"]
    carved = []
    total = len(picked)
    for index, row in enumerate(picked, 1):
        print("[%d/%d] %s (%s)" % (index, total, row["unit"], row["lang"]))
        sys.stdout.flush()
        rec = carve_one(row, work_root)
        rec["mnem"] = row["mnem"]
        rec["shape"] = row["shape"]
        rec["key_width"] = row["key_width"]
        carved.append(rec)
        print("      %s  %d instructions"
              % (rec["outcome"], rec.get("instruction_count", 0)))
        for line in rec.get("body", []):
            print("        %s" % line)
    doc = {
        "meta": {
            "task": "rv1",
            "what": "each unit's own probe source compiled for riscv64 at "
                    "the corpus's own ship optimisation level and carved "
                    "at its function symbol",
            "disassembler": "llvm-objdump -dr -M no-aliases "
                            "--mattr=+m,+a,+f,+d,+c --disassemble-symbols="
                            "<symbol>",
            "calling_convention": "RISC-V psABI lp64d: a0-a7 (x10-x17) "
                                  "carry integer arguments in order and a0 "
                                  "carries the integer answer; fa0-fa7 "
                                  "(f10-f17) carry floating-point "
                                  "arguments and fa0 the floating-point "
                                  "answer; there is no flags register.",
        },
        "rows": carved,
    }
    fh = open(out_path, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    ok = len([r for r in carved if r["outcome"] == "CARVED"])
    print("carved %d of %d" % (ok, total))


if __name__ == "__main__":
    main()
