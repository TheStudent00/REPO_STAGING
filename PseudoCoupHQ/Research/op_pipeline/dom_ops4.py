#!/usr/bin/env python3
"""dom_ops4.py -- the dom_op construction over dominant_table6.

This is dom_ops_java.py's method, one table later.  dom_ops.py names
its languages in a module-level list and reads its table under the
fixed name `dominant_table3.json`.  Neither is changed here: this
wrapper adds `java` to the language list exactly as dom_ops_java.py
does, stages `dominant_table6.json` under the name dom_ops.py expects
in a directory of its own, runs dom_ops.py UNCHANGED, and renames the
products afterwards, so the artifact that ships is `dom_ops4.json` and
no earlier dom_ops file is overwritten.

Why it exists: dom_ops3.json was built over dominant_table5, before
the widened third candidate rule merged six classes.  The dom_op
families are connected components of the mutual-best graph, and that
graph is weighted by SHARED EQUIVALENCE-CLASS COUNT, so a merge can
change which counterpart is strongest and therefore which nodes are in
one family.  Re-running is the only way to find out; predicting it is
not.

THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26).  Dominant operators
are DISCOVERED from machine evidence by matching, never asserted:
nodes are (language, grammar-operator, ARITY) -- provenance of the
probe, not a cross-language token; edges only BETWEEN languages,
weighted by shared equivalence-class count; each node keeps its single
STRONGEST counterpart per foreign language, kept only when MUTUAL;
connected components of the mutual-best graph are the dominant
operators.

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
  dom_ops4.py [--in DIR] [--out DIR] [--every N]
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO                                          # noqa: E402

RENAME = [
    ("dom_ops.json", "dom_ops4.json"),
    ("dom_ops.md", "dom_ops4.md"),
    ("dom_ops_digest.md", "dom_ops4_digest.md"),
    ("dom_ops_digest_shape.json", "dom_ops4_digest_shape.json"),
]

STAGE_INPUTS = ["verdicts3b.json"]

SOURCE_TABLE = "dominant_table6.json"

SOURCE_BRIDGES = "bridges6.json"


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

    stage = os.path.join(outdir, "stage_dom_ops4")
    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(stage)

    src = os.path.join(indir, SOURCE_TABLE)
    if not os.path.exists(src):
        print("!! REFUSING: %s is not present" % src)
        return 4
    shutil.copy(src, os.path.join(stage, "dominant_table3.json"))

    bridges = os.path.join(indir, SOURCE_BRIDGES)
    if not os.path.exists(bridges):
        print("!! REFUSING: %s is not present" % bridges)
        return 4
    shutil.copy(bridges, os.path.join(stage, "bridges.json"))

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

    doc = json.load(open(os.path.join(outdir, "dom_ops4.json")))
    print("dom_ops           %d" % doc["dom_op_count"])
    print("nodes             %d" % doc["nodes"])
    print("unattached nodes  %d" % doc["nodes_with_no_surviving_edge"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
