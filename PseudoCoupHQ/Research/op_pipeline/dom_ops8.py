#!/usr/bin/env python3
"""dom_ops8.py -- dom_ops7.py's own method, one table later:
dominant_table10.json (dominant_table9 plus the canon-text evidence
ground -- the reassembly-verified canonical runnable instruction text,
character-identical, gated on the same class key).

Nothing about dom_ops.py's own construction changes here.  Same
languages (dom_ops7.py's list plus `java`), same staged inputs, same
run, renamed products so dom_ops7.json is untouched.

THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26).  Dominant operators are
DISCOVERED from machine evidence by matching, never asserted: nodes are
(language, grammar-operator, ARITY) -- provenance of the probe, not a
cross-language token; edges only BETWEEN languages, weighted by shared
equivalence-class count; each node keeps its single STRONGEST
counterpart per foreign language, kept only when MUTUAL; connected
components of the mutual-best graph are the dominant operators.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs are
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.

usage:
  dom_ops8.py [--in DIR] [--out DIR] [--every N]
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO                                          # noqa: E402

RENAME = [
    ("dom_ops.json", "dom_ops8.json"),
    ("dom_ops.md", "dom_ops8.md"),
    ("dom_ops_digest.md", "dom_ops8_digest.md"),
    ("dom_ops_digest_shape.json", "dom_ops8_digest_shape.json"),
]

STAGE_INPUTS = ["verdicts3b.json"]

SOURCE_TABLE = "dominant_table10.json"

SOURCE_BRIDGES = "bridges6.json"

STAGE_MANIFESTS = os.path.join(os.path.dirname(HERE), "stage_asg")


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

    stage = os.path.join(outdir, "stage_dom_ops8")
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
            staged = os.path.join(STAGE_MANIFESTS, name)
            if pattern.startswith("probe_manifest") and \
                    os.path.exists(staged):
                path = staged
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

    doc = json.load(open(os.path.join(outdir, "dom_ops8.json")))
    print("dom_ops           %d" % doc["dom_op_count"])
    print("nodes             %d" % doc["nodes"])
    print("unattached nodes  %d" % doc["nodes_with_no_surviving_edge"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
