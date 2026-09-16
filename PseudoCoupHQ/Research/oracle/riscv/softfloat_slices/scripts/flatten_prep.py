#!/usr/bin/env python3
"""Prototypes and the transitive source closure per operation, computed once.

The closure is a symbol fixed point, so it does not depend on the target or
the rounding mode; doing it here keeps the parallel phase free of races on the
shared bitcode cache.
"""
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")   # no machine path is written into this file

SCRATCH = ("/tmp/claude-1000/-home-<user>-Programming/"
           "88f5a9f5-d844-4f11-895c-c5dafdfde323/scratchpad")
ROOT = os.path.join(SCRATCH, "fl")
SF = (HOME + "/Programming/SOURCES/sail-riscv/dependencies/softfloat/"
      "berkeley-softfloat-3")
B = "/usr/lib/llvm-21/bin"
SRC_DIRS = ("source", "source/RISCV")
ALWAYS = [os.path.join(SF, "source", "s_approxRecipSqrt_1Ks.c"),
          os.path.join(SF, "source", "s_approxRecip_1Ks.c"),
          os.path.join(SF, "source", "softfloat_state.c")]

sys.path.insert(0, ROOT)


def parse_prototypes():
    hdr = open(os.path.join(SF, "source/include/softfloat.h")).read()
    hdr = re.sub(r"/\*.*?\*/", "", hdr, flags=re.S)
    hdr = " ".join(hdr.split())
    protos = {}
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_ ]*?)\s+([A-Za-z_][A-Za-z0-9_]*)"
                         r"\s*\(([^)]*)\)\s*;", hdr):
        protos[m.group(2)] = [m.group(1).strip(),
                              [a.strip() for a in m.group(3).split(",")]]
    return protos


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, (p.stderr or "").strip()


def main():
    os.makedirs(os.path.join(ROOT, "bc"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "gen"), exist_ok=True)
    protos = parse_prototypes()
    json.dump(protos, open(os.path.join(ROOT, "protos.json"), "w"), indent=1)
    import pipe as P                                            # noqa: E402
    P.PROTOS = protos

    bcdir = os.path.join(ROOT, "bc")
    nm_cache = {}

    def nm(bc):
        if bc in nm_cache:
            return nm_cache[bc]
        _, out, _ = run([B + "/llvm-nm", bc])
        d, u = set(), set()
        for line in out.splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            t, n = parts[-2], parts[-1]
            (u if t == "U" else d).add(n)
        nm_cache[bc] = (d, u)
        return d, u

    def find_source(sym):
        base = sym[len("softfloat_"):] if sym.startswith("softfloat_") else sym
        for cand in ("s_" + base, sym, base):
            for sub in SRC_DIRS:
                p = os.path.join(SF, sub, cand + ".c")
                if not os.path.exists(p):
                    continue
                try:
                    bc = P.compile_bc(p, "rv", bcdir)
                except RuntimeError:
                    continue
                if sym in nm(bc)[0]:
                    return p
        return None

    mapping = json.load(open(os.path.join(
        HOME + "/Programming/PRIVATE/PseudoCoupHQ/Research/oracle/riscv/"
        "softfloat_slices/measurements", "mapping.json")))
    ops = [m["sf"] for m in mapping]
    closures, unresolved_all = {}, {}
    for op in ops:
        files = [os.path.join(SF, "source", op + ".c")] + list(ALWAYS)
        seen, unresolved = set(files), set()
        while True:
            bcs = [P.compile_bc(f, "rv", bcdir) for f in files]
            und, dfn = set(), set()
            for bc in bcs:
                d, u = nm(bc)
                und |= u
                dfn |= d
            added = False
            for sym in sorted(und - dfn - unresolved):
                if sym.startswith("__"):
                    unresolved.add(sym)
                    continue
                p = find_source(sym)
                if p is None:
                    unresolved.add(sym)
                    continue
                if p not in seen:
                    seen.add(p)
                    files.append(p)
                    added = True
            if not added:
                break
        closures[op] = files
        unresolved_all[op] = sorted(unresolved)
        print("%-16s %2d files  %s" % (op, len(files),
                                       ",".join(sorted(unresolved)) or ""),
              flush=True)
    json.dump({"ops": ops, "closures": closures,
               "unresolved": unresolved_all},
              open(os.path.join(ROOT, "closures.json"), "w"), indent=1)
    print("%d operations" % len(ops))


if __name__ == "__main__":
    main()
