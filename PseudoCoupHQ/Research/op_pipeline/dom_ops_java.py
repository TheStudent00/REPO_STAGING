#!/usr/bin/env python3
"""dom_ops_java.py -- the dom_op construction with java in the language
list.

dom_ops.py names its five languages in a module-level list and reads
one probe manifest and one core/mode record per language.  This file
adds `java` to that list and runs dom_ops.py unchanged; the manifest
and the core/mode record java needs were written by add_java.py.

dom_ops.py also reads its table under the name `dominant_table3.json`.
That name is NOT changed in dom_ops.py -- the file is left untouched.
This wrapper stages `dominant_table5.json` under that name in a
directory of its own and renames the products afterwards, so the
artifact that ships is `dom_ops3.json` and neither earlier dom_ops file
is overwritten.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.

usage:
  dom_ops_java.py [--in DIR] [--out DIR] [--every N]
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO                                          # noqa: E402

RENAME = [
    ("dom_ops.json", "dom_ops3.json"),
    ("dom_ops.md", "dom_ops3.md"),
    ("dom_ops_digest.md", "dom_ops3_digest.md"),
    ("dom_ops_digest_shape.json", "dom_ops3_digest_shape.json"),
]

STAGE_INPUTS = ["verdicts3b.json"]


def main():
    indir = HERE
    outdir = HERE
    every = 500
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--in":
            i = i + 1
            indir = args[i]
        elif args[i] == "--out":
            i = i + 1
            outdir = args[i]
        elif args[i] == "--every":
            i = i + 1
            every = int(args[i])
        i = i + 1

    if "java" in DO.LANGS:
        print("!! REFUSING: dom_ops.py already names java; this "
              "wrapper would add it twice")
        return 4
    DO.LANGS = DO.LANGS + ["java"]
    print("languages: %s" % ", ".join(DO.LANGS))

    stage = os.path.join(outdir, "stage_dom_ops_java")
    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(stage)

    src = os.path.join(indir, "dominant_table5.json")
    if not os.path.exists(src):
        print("!! REFUSING: %s is not present" % src)
        return 4
    shutil.copy(src, os.path.join(stage, "dominant_table3.json"))
    shutil.copy(os.path.join(indir, "bridges4.json"),
                os.path.join(stage, "bridges.json"))
    for name in STAGE_INPUTS:
        shutil.copy(os.path.join(indir, name),
                    os.path.join(stage, name))
    for lang in DO.LANGS:
        for pattern in ("probe_manifest_%s.json", "core_modes_%s.json"):
            name = pattern % lang
            path = os.path.join(indir, name)
            if not os.path.exists(path):
                print("!! REFUSING: %s is not present" % path)
                return 4
            shutil.copy(path, os.path.join(stage, name))

    DO.main(["--in", stage, "--out", stage, "--every", str(every)])

    for a, b in RENAME:
        one = os.path.join(stage, a)
        two = os.path.join(outdir, b)
        if not os.path.exists(one):
            print("!! the run did not write %s" % a)
            return 5
        shutil.move(one, two)
        print("wrote %s" % two)

    shutil.rmtree(stage)

    doc = json.load(open(os.path.join(outdir, "dom_ops3.json")))
    print("dom_ops           %d" % doc["dom_op_count"])
    print("nodes             %d" % doc["nodes"])
    print("unattached nodes  %d" % doc["nodes_with_no_surviving_edge"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
