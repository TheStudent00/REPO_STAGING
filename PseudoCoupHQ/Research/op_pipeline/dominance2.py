#!/usr/bin/env python3
"""dominance2.py -- dominance.py with the ordering result types given
a MEASURED projection.

What this file changes, and nothing else
----------------------------------------
dominance.py's projection table names a bit width per result type and
refuses to invent one, in its own words:

    "A result type this table does not name gets NO projection.  The
     pair is recorded with the reason and no bridge is claimed.
     Reading, say, `partial_ordering` as "some number of bits" would
     be human interpretation of stated design, the weakest evidence
     class, and this file does not do it."

That refusal is right and it stands.  What changes is that the width
is no longer an interpretation: `lanes/pc_ordering_probe.sh` compiled
a probe and READ the encoding out of the compiler, in two independent
readings that agree, and `ordering_encoding.py` wrote the result to
`ordering_encoding.json`.  This file loads that measurement and adds
one entry per measured ordering family to dominance's own table.

Nothing else is touched.  dominance.py is imported, not copied; the
proof, the adapter table, the candidate set and the run are all its
code.  The one mutation is `dominance.RESULT_PROJECTION[name] = ...`,
made once, before the run, from measured data.

The products are VERSIONED so the earlier ones are records:
  bridges2.json, dominant_table3b.json, dominant_table3b.md,
  table_digest3b.md.

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
  dominance2.py [--in DIR] [--out DIR] [--every N]
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominance as D                                         # noqa: E402


RENAME = [
    ("bridges.json", "bridges2.json"),
    ("dominant_table3.json", "dominant_table3b.json"),
    ("dominant_table3.md", "dominant_table3b.md"),
    ("table_digest3.md", "table_digest3b.md"),
]


def install_measured_projections(indir):
    """add one projection entry per measured ordering family.

    Returns the record of what was added, so the run can print it and
    the product can carry it.
    """
    path = os.path.join(indir, "ordering_encoding.json")
    if not os.path.exists(path):
        return None, ("REFUSING: %s is not present.  The projection "
                      "for an ordering result type is a MEASUREMENT, "
                      "and without it this pass has nothing the "
                      "earlier one did not have." % path)
    doc = json.load(open(path))
    if not doc.get("readings_agree"):
        return None, ("REFUSING: the two readings of the encoding do "
                      "not agree; ordering_encoding.py should not have "
                      "written this file")
    added = {}
    for family in sorted(doc["projection"]):
        rec = doc["projection"][family]
        bits = rec["bits"]
        register = rec["register"]
        promise = rec["promise"]
        if family in D.RESULT_PROJECTION:
            return None, ("REFUSING: dominance.py already names %r; "
                          "this pass will not silently redefine an "
                          "existing projection" % family)
        D.RESULT_PROJECTION[family] = (bits, register, promise)
        if bits not in D.PROJECTION_KIND:
            D.PROJECTION_KIND[bits] = "low-%d" % bits
        added[family] = dict(bits=bits, register=register,
                             promise=promise,
                             measured_values=rec["measured_values"])
    return added, None


def main():
    indir = HERE
    outdir = HERE
    every = 100
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

    added, refusal = install_measured_projections(indir)
    if refusal is not None:
        print("!! %s" % refusal)
        return 4

    print("== dominance2: the ordering result types now have a "
          "MEASURED projection")
    for family in sorted(added):
        print("   %-18s %d bits in %%%s, values %s"
              % (family, added[family]["bits"],
                 added[family]["register"],
                 json.dumps(added[family]["measured_values"])))
    print()
    sys.stdout.flush()

    stage = os.path.join(outdir, "stage_dominance2")
    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(stage)

    rc = D.main(["dominance2.py", "--in", indir, "--out", stage,
                 "--every", str(every)])
    if rc not in (None, 0):
        print("!! the dominance run exited %s" % rc)
        return rc

    for src, dst in RENAME:
        a = os.path.join(stage, src)
        b = os.path.join(outdir, dst)
        if not os.path.exists(a):
            print("!! the run did not write %s" % src)
            return 5
        shutil.move(a, b)
        print("wrote %s" % b)

    # the measurement travels ON the product, so a reader of
    # bridges2.json never has to go looking for where the width came
    # from.
    path = os.path.join(outdir, "bridges2.json")
    doc = json.load(open(path))
    doc["projection_measured_additions"] = added
    doc["projection_measurement_lane"] = "lanes/pc_ordering_probe.sh"
    doc["projection_measurement_record"] = "ordering_encoding.json"
    doc["what_changed_from_bridges_json"] = "the ordering result "\
                                            "types have a projection, "\
                                            "measured from the "\
                                            "compiler.  Nothing else "\
                                            "differs: same inputs, "\
                                            "same proof, same adapter "\
                                            "table, same candidate set."
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()

    shutil.rmtree(stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
