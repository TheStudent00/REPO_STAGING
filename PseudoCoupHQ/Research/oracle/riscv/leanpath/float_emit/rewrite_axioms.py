#!/usr/bin/env python3
"""rewrite_axioms.py -- Sail's float axioms get their bodies in a WORKING COPY
of the emit. The cache is never written.

The set is the intersection of two texts, nothing named: every line

    axiom NAME : TYPE

of the working copy's RiscvExtras.lean for which Kinds.lean's `namespace
Axioms` has `def NAME : TYPE := ...` with the SAME type text becomes

    def NAME : TYPE := Kinds.Axioms.NAME

and `import Kinds` is added after the file's last import line. The type is
kept, so every caller in the emit sees exactly the constant it saw before.

Before anything is written, the working copy's file is checked to be
byte-identical to the cache's (the working copy starts as the emit). The
unified diff against the cache is written as the record. Undo: copy the
cache's RiscvExtras.lean back over the working copy's.
"""
import argparse
import difflib
import re
import sys


def kinds_types(path):
    text = open(path).read()
    m = re.search(r"^namespace Axioms\s*$(.*?)^end Axioms\s*$", text, re.S | re.M)
    out = {}
    for ln in (m.group(1).split("\n") if m else []):
        mm = re.match(r"^def\s+(\w+)\s*:\s*(.+?)\s*:=\s*(.+)$", ln)
        if mm:
            out[mm.group(1)] = re.sub(r"\s+", " ", mm.group(2).strip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-extras", required=True)
    ap.add_argument("--work-extras", required=True)
    ap.add_argument("--kinds", required=True)
    ap.add_argument("--diff-out", required=True)
    args = ap.parse_args()
    cache = open(args.cache_extras).read()
    work = open(args.work_extras).read()
    if work != cache:
        print("REFUSED: the working copy's RiscvExtras.lean is not the cache's; restore it from the cache first")
        return 3
    kt = kinds_types(args.kinds)
    lines = work.split("\n")
    out, done, last_import = [], [], -1
    for i, ln in enumerate(lines):
        if ln.startswith("import "):
            last_import = len(out)
        mm = re.match(r"^axiom\s+(\w+)\s*:\s*(.+?)\s*$", ln)
        if mm and mm.group(1) in kt and re.sub(r"\s+", " ", mm.group(2)) == kt[mm.group(1)]:
            out.append("def %s : %s := Kinds.Axioms.%s" % (mm.group(1), mm.group(2), mm.group(1)))
            done.append(mm.group(1))
            continue
        out.append(ln)
    if last_import < 0:
        print("REFUSED: no import line in the file")
        return 3
    out.insert(last_import + 1, "import Kinds")
    new = "\n".join(out)
    open(args.work_extras, "w").write(new)
    diff = difflib.unified_diff(cache.split("\n"), new.split("\n"), "cache/RiscvExtras.lean",
                                "working_copy/RiscvExtras.lean", lineterm="")
    open(args.diff_out, "w").write("\n".join(diff) + "\n")
    left = [m.group(1) for m in re.finditer(r"^axiom\s+(\w+)", new, re.M)]
    print("  bodies given: %d (%s)" % (len(done), " ".join(done)))
    print("  axioms left in the working copy's RiscvExtras.lean: %d" % len(left))
    print("  Kinds.Axioms definitions with no axiom of the same name and type: %d" % len(set(kt) - set(done)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
