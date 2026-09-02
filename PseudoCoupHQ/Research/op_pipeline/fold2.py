#!/usr/bin/env python3
"""fold2.py -- fold the compound-assignment lane outputs.

fold.py's `fold(name, outdir)` already keys everything on one name: it
reads `probe_manifest_<name>.json`, globs `op_<name>.txt` (and its
shards) in the Airlock out directory, and writes
`op_units_<name>.json`.  So folding the compound-assignment run is
that same function called with the name `asg_<lang>`.  Nothing about
the folding is re-derived here, and the first run's `op_units_*.json`
are not touched.

usage:
  fold2.py c cpp go rust swift [--out DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fold as F                                              # noqa: E402

LANGS = F.LANGS


def main():
    langs = []
    outdir = F.OUTDIR
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        else:
            langs.append(args[i])
        i = i + 1

    if not langs:
        print(__doc__)
        return 2

    head = ("%-10s %10s %8s %9s %9s %8s %8s %8s"
            % ("lang", "candidates", "refused", "accepted", "anchor-OK",
               "ship-OK", "DWARF", "missing"))
    print(head)
    print("-" * len(head))
    summary = {}
    for lang in langs:
        if lang not in LANGS:
            print("skip %s" % lang)
            continue
        name = "asg_%s" % lang
        tally, path = F.fold(name, outdir)
        summary[lang] = tally
        print("%-10s %10d %8d %9d %9d %8d %8d %8d"
              % (lang, tally["candidates"], tally["refused"],
                 tally["accepted"], tally["anchor_ok"],
                 tally["ship_ok"], tally["dwarf"], tally["missing"]))
        print("           -> %s" % path)

    path = os.path.join(HERE, "asg_acceptance.json")
    doc = dict(
        what_this_is="the acceptance counts of the "
                     "compound-assignment run, per language",
        probe_shape="f(a, b): `a op= b` then `return a`.  The store is "
                    "part of the unit.",
        acceptance_oracle="the compiler's own type checker, in the "
                          "lane.  A refusal is testimony, not a gap.",
        matching="NOT run for this bucket in this lap.  The "
                 "deliverable here is the extraction.",
        per_language=summary)
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("wrote %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
