#!/usr/bin/env python3
"""tree_match4.py -- wraps tree_match3.py the same way tree_match3.py
wrapped tree_match2.py (precedent unchanged: reuse everything about
BLOCK/VALUE SELECTION -- tree_match3.py's own ret-block-first rule,
the ADOPTED baseline this lap was told to build on -- by import; change
exactly one thing).

THE ONE CHANGE: the z3 NORMALIZER. tree_match2.py's `to_z3_fixed` (and
therefore tree_match3.py, which reuses it unchanged) swallows every
SIMD-float lifter name (Add/Sub/Mul/Div/CmpEQ at 32F0x4/64F0x2, Xor/
Or/AndV128) into a single, undifferentiated, 64-bit-defaulted opaque
atom -- the generic "everything else" fallback. vex_names.py's own
`to_z3_v3` (JOB 1's generic name translator, see that file's header)
PARSES those twelve names and builds a real z3 term for each (real FPA
arithmetic/compare for the lane family, plain 128-bit bitwise for the
whole-register family) -- so two units that both, say, add a converted
int to a native float now normalize to the SAME real expression
instead of two independent, indistinguishable opaque atoms, and a unit
that previously threw away its own operand structure keeps it.

MEASURED EFFECT (this lap's own report has the numbers): every unit
whose raw text mentions one of the twelve names now normalizes via a
real term instead of an opaque atom; new exact-match clusters among
those units are reported by main() below, never assumed.

THE SPELLING BAN: unchanged -- `operator` is a display label only,
read by build_matches() (imported, untouched) and never used to key,
group, or select a candidate here.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match3 as TM3                                      # noqa: E402
import sem_anchored_spill as SAS                                 # noqa: E402
import vex_names as VN                                           # noqa: E402

LANGS = SAS.LANGS

parse_expr = TM3.parse_expr
serialize = TM3.serialize
tree_size = TM3.tree_size
build_matches = TM3.build_matches
candidate_values = TM3.candidate_values
normal_path_value = TM3.normal_path_value

normalize = VN.normalize_v3


def load_all_units():
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        if not os.path.exists(path):
            print("!! missing %s" % path)
            continue
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            meta = u["meta"]
            sem = u["sem"]
            rec = dict(lang=lang, n=n, operator=meta.get("operator"),
                       arity=meta.get("arity"),
                       lhs_rep=meta.get("lhs_rep"), rhs_rep=meta.get("rhs_rep"),
                       symbol=meta.get("symbol"), sem_ok=sem.get("ok"))
            if not sem.get("ok"):
                rec["refused"] = sem.get("reason", "sem not ok")
                out.append(rec)
                continue
            blocks = sem.get("blocks", [])
            rec["block_count"] = len(blocks)
            rec["all_block_values"] = [b.get("values", []) for b in blocks]
            rec["all_block_events"] = [b.get("events", []) for b in blocks]
            root_text, rule = normal_path_value(blocks)
            rec["normal_path_block_rule"] = rule
            rec["carried"] = sem.get("carried", False)
            if root_text is None:
                rec["normal_path_root"] = None
                rec["note"] = "no return-bearing block with a value"
            else:
                norm, ok, note = normalize(root_text)
                rec["normal_path_raw"] = root_text
                rec["normal_path_root"] = norm
                rec["normalize_ok"] = ok
                rec["normalize_note"] = note
                tree = parse_expr(root_text)
                if tree[0] == "node":
                    rec["subexp1_root_op"] = tree[1]
                    rec["subexp2_children"] = [serialize(a) for a in tree[2]]
                else:
                    rec["subexp1_root_op"] = None
                    rec["subexp2_children"] = []
            out.append(rec)
    return out


def main():
    units = load_all_units()
    exact, containment = build_matches(units)

    units_doc = dict(
        languages=LANGS,
        normalizer="z3 simplify (vex_names.py: dictionary dispatch, "
                   "generic SIMD-float lane/bitwise name parsing, real "
                   "z3 FPA)",
        source="sem_anchored_spill_<lang>.json, ret-block-first value "
               "selection (tree_match3.py's own adopted baseline, "
               "REUSED UNCHANGED -- only the normalizer changed)",
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
        languages=LANGS,
        exact_normalized_root=exact,
        containment=containment,
    )

    json.dump(units_doc, open(os.path.join(HERE, "tree_units4.json"), "w"),
               indent=1)
    json.dump(matches_doc, open(os.path.join(HERE, "tree_matches4.json"),
                                 "w"), indent=1)

    print("units total:", len(units))
    print("units with normal-path root:", sum(1 for u in units
                                                if u.get("normal_path_root")))
    print("exact normalized-root clusters:", len(exact))
    print("  cross-language:", sum(1 for c in exact if c["cross_language"]))
    print("containment edges:", len(containment))
    return 0


if __name__ == "__main__":
    sys.exit(main())
