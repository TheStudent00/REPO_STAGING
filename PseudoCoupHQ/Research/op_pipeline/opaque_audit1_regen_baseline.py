#!/usr/bin/env python3
"""opaque_audit1_regen_baseline.py -- FIX A CAUSE AT FIRST OBSERVATION.

FINDING (this session, 2026-08-30): comparing tree_units2.json against
tree_units3.json directly is CONFOUNDED. `ls -la` shows tree_units2.json
was written 2026-08-27, but tree_match2.py (the module tree_match3.py
imports its `normalize` from, unchanged) carries a file mtime of
2026-08-28 -- i.e. tree_match2.py's own normalize()/to_z3_fixed() code
was edited (see its own docstring: CAUSE 1/2/3 fixes, all dated
2026-08-28) AFTER tree_units2.json was generated. tree_units3.json was
generated later still (2026-08-30), by tree_match3.py importing the
CURRENT tree_match2.py.

Measured proof: 936 units have IDENTICAL `normal_path_raw` text between
tree_units2.json and tree_units3.json, yet DIFFERENT normalized text
(`normal_path_root`) -- impossible if both ran the same normalize()
function on the same input, since normalize() is a pure function of
its text argument. Example, c/0: raw
`ins@0(0:64,zx8(ex1@0(amd64g_calculate_condition(4:64,19:64,zx64(ex32@0(in0:64)),0:64,u0:64))))`
normalizes to bare `op_6` in tree_units2.json but to
`Concat(Extract(63, 8, atom_0), 0, Extract(0, 0, op_5))` in
tree_units3.json -- same input, different output, because
tree_units2.json's normalize() call predates the CAUSE 1/2/3 fixes and
tree_units3.json's postdates them.

THE FIX (per "fix a cause at first observation," and respecting the
constraint that tree_units2.json/tree_match2.py must not be
overwritten): regenerate a FRESH baseline by running tree_match2.py's
OWN load_all_units()+build_matches() (imported, unmodified,
byte-identical code) against the CURRENT sem_anchored_spill_<lang>.json
files, writing to NEW filenames only. This isolates the ONE variable
the verification task is actually about -- ret-block-first vs
global-largest SELECTION -- from the normalizer bugfixes that landed
in between, by running both selection rules through the SAME (current)
normalize() code. tree_match2.py itself is not edited; this is a
read-only re-run through its own unmodified main()-equivalent, output
redirected to fresh files.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match2 as TM2                                        # noqa: E402


def main():
    units = TM2.load_all_units()
    exact, containment = TM2.build_matches(units)

    units_doc = dict(
        languages=TM2.LANGS,
        normalizer="z3 simplify (bitvector), opaque atoms for helper calls",
        source="sem_anchored_spill_<lang>.json, RE-RUN of tree_match2.py's "
               "own load_all_units()/build_matches() (imported "
               "unmodified) against the CURRENT normalize() code, to "
               "give a same-normalizer baseline for comparison against "
               "tree_units3.json -- see this file's own docstring for "
               "why the original tree_units2.json is stale relative to "
               "the normalizer code and cannot be used for that "
               "comparison directly.",
        total_units=len(units),
        units=[dict(
            lang=u["lang"], n=u["n"], operator=u["operator"],
            type_pair="%s,%s" % (u.get("lhs_rep"), u.get("rhs_rep")),
            sem_ok=u.get("sem_ok"),
            refused=u.get("refused"),
            block_count=u.get("block_count"),
            carried=u.get("carried"),
            normal_path_block_rule=u.get("normal_path_block_rule"),
            normal_path_raw=u.get("normal_path_raw"),
            normal_path_root=u.get("normal_path_root"),
            normalize_ok=u.get("normalize_ok"),
            normalize_note=u.get("normalize_note"),
            subexp1_root_op=u.get("subexp1_root_op"),
            subexp2_children=u.get("subexp2_children"),
        ) for u in units],
    )
    matches_doc = dict(
        languages=TM2.LANGS,
        exact_normalized_root=exact,
        containment=containment,
    )

    json.dump(units_doc, open(
        os.path.join(HERE, "tree_units2_fresh.json"), "w"), indent=1)
    json.dump(matches_doc, open(
        os.path.join(HERE, "tree_matches2_fresh.json"), "w"), indent=1)

    print("units total:", len(units))
    print("exact normalized-root clusters:", len(exact))
    print("  cross-language:", sum(1 for c in exact if c["cross_language"]))
    print("containment edges:", len(containment))
    return 0


if __name__ == "__main__":
    sys.exit(main())
