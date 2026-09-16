#!/usr/bin/env python3
"""Attest, at the machine level, that the arch-unit emulations carry no float.

`verify_arch_units.py` leaves its build products under AU_SCRATCH.  This walks
them and reports every distinct host instruction the four languages' compiled
arch-unit code actually contains, plus any use of a float register.  A float
instruction or an xmm/ymm (go: X) register anywhere in that code would sink
the claim, so the expected answer is zero of both.

    python3 scripts/verify_arch_units.py      # first, to build
    python3 scripts/nofloat_probe.py
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OUT = os.path.join(BASE, "arch_units")
SCRATCH = os.environ.get(
    "AU_SCRATCH",
    "/tmp/claude-1000/-home-<user>-Programming/"
    "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad/archunits")

# an x86-64 mnemonic that touches a floating point unit: every x87 mnemonic
# starts with `f`, and every SSE/AVX float form ends in ss/sd/ps/pd or starts
# with cvt (integer SSE is p*/movdq*, which none of these match)
FLOATY = re.compile(r"^(f[a-z0-9]*|cvt[a-z0-9]*|v?[a-z0-9]*(ss|sd|ps|pd))$",
                    re.I)
XREG = re.compile(r"\b([xy]mm[0-9]+|X[0-9]+)\b")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw).stdout


def objdump_set(paths):
    mn, xr = set(), 0
    for p in paths:
        text = sh(["objdump", "-d", "--no-show-raw-insn", p])
        for line in text.splitlines():
            m = re.match(r"\s+[0-9a-f]+:\s+([a-z][a-z0-9.]*)", line)
            if m:
                mn.add(m.group(1))
            if XREG.search(line):
                xr += 1
    return mn, xr


def go_set(binary):
    mn, xr = set(), 0
    text = sh(["go", "tool", "objdump", "-s",
               r"^(archunits|softfloat_emul|emul)\.", binary])
    for line in text.splitlines():
        f = line.split()
        if len(f) > 3 and f[1].startswith("0x"):
            mn.add(f[3])
        if XREG.search(line):
            xr += 1
    return mn, xr


def main():
    rep = {}
    oc = os.path.join(SCRATCH, "obj_c")
    op = os.path.join(SCRATCH, "obj_cpp")
    rl = os.path.join(SCRATCH, "rlib")
    checks = {
        "c": [os.path.join(oc, f) for f in sorted(os.listdir(oc))],
        "cpp": [os.path.join(op, f) for f in sorted(os.listdir(op))],
        "rust": [os.path.join(rl, "libarchunits.rlib"),
                 os.path.join(rl, "libsfemul.rlib")],
    }
    for lang, paths in checks.items():
        mn, xr = objdump_set(paths)
        bad = sorted(m for m in mn if FLOATY.match(m))
        rep[lang] = {"objects": len(paths), "distinct_instructions": len(mn),
                     "float_instructions": bad,
                     "float_register_references": xr,
                     "instructions": sorted(mn)}
    mn, xr = go_set(os.path.join(SCRATCH, "h_go"))
    bad = sorted(m for m in mn if FLOATY.match(m))
    rep["go"] = {"objects": 1, "distinct_instructions": len(mn),
                 "float_instructions": bad,
                 "float_register_references": xr,
                 "instructions": sorted(mn)}

    ok = True
    print("| language | objects | distinct host instructions |"
          " float instructions | float register references |")
    print("|---|---:|---:|---:|---:|")
    for lang in ("c", "cpp", "rust", "go"):
        r = rep[lang]
        print("| %s | %d | %d | %d | %d |"
              % (lang, r["objects"], r["distinct_instructions"],
                 len(r["float_instructions"]),
                 r["float_register_references"]))
        if r["float_instructions"] or r["float_register_references"]:
            ok = False
            print("  FLOAT FOUND:", r["float_instructions"])
    path = os.path.join(OUT, "_nofloat.json")
    json.dump(rep, open(path, "w"), indent=1)
    print("\nwritten to", path)
    print("VERDICT:", "no float anywhere" if ok else "FLOAT PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
