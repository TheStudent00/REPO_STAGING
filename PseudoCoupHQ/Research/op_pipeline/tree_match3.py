#!/usr/bin/env python3
"""tree_match3.py -- wraps tree_match2.py the same way tree_match2.py
wrapped tree_match.py (precedent unchanged: reuse everything about
matching -- z3 normalization, containment, type-pair candidate scope --
by import; change exactly one thing).

THE DEFECT THIS FIXES (log_081 item "the missing-extraction defect").
tree_match2.py's `candidate_values` correctly widened the search to
every non-trap non-call-tail block (fixing tree_match.py's two ret-block
bugs), but `normal_path_value` then picks the GLOBALLY largest surviving
tree across ALL of those blocks, and only tie-breaks toward the ret
block among ties at that same max size. That is backwards for a unit
whose real answer is produced by a SHORT final step in the ret block
itself -- e.g. a narrowing `and $0x1,%eax` after a larger computation
that lives, in full or in part, in an earlier block. sem_anchored_spill.py
already carries a written register's expression forward across
single-predecessor edges (see its own docstring), so by the time a unit
reaches sem_anchored_spill_<lang>.json, the ret block's own values are
ALREADY the carried-forward, fully-substituted computation -- there is
no remaining reason to let a bigger tree sitting in some OTHER block
(a stack-alignment restore that survived filtering, or a shortcut path
that merges before the return) outrank the ret block's own answer.

THE FIX: the ret block owns the answer. If the ret block has ANY
non-trivial candidate (tree_size > 1), the largest one FROM THE RET
BLOCK ITSELF wins outright -- other blocks are not even considered.
Only when the ret block has nothing but bare single-leaf values (or no
values at all) does the search fall back to the largest surviving tree
among the other non-trap, non-call-tail blocks -- tree_match2.py's own
rule, kept verbatim as the fallback, because for a unit with no
computation of its own in the ret block that fallback is still the
right answer (the ret block just returns whatever another block
already produced, following the carry).

THE SPELLING BAN: unchanged -- `operator` is a display label only,
read by build_matches() (imported, untouched) and never used to key,
group, or select a candidate here.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match2 as TM2                                     # noqa: E402
import sem_anchored_spill as SAS                                # noqa: E402

LANGS = SAS.LANGS

parse_expr = TM2.parse_expr
serialize = TM2.serialize
tree_size = TM2.tree_size
build_matches = TM2.build_matches
normalize = TM2.normalize
candidate_values = TM2.candidate_values


def normal_path_value(blocks):
    """(value_text, rule_note).  See module docstring: ret-block-first,
    tree_match2.py's global-largest-tree rule kept as the fallback."""
    ret_block_id = None
    for b in blocks:
        if any(ev == "ret" or (isinstance(ev, str) and ev.startswith("ret"))
               for ev in b.get("events", [])):
            ret_block_id = b.get("block")
            break

    cands = candidate_values(blocks, ret_block_id)
    if not cands:
        return None, "no candidate value in any non-trap non-call-tail block"

    ret_cands = [c for c in cands if c[0] == ret_block_id]
    ret_nontrivial = [c for c in ret_cands if c[2] > 1]

    if ret_nontrivial:
        best = max(c[2] for c in ret_nontrivial)
        chosen = next(c for c in ret_nontrivial if c[2] == best)
        return chosen[1], (
            "ret block %s owns the answer, largest surviving tree in "
            "that block (tree_match3 ret-first rule)" % ret_block_id)

    # ret block has nothing but bare leaves (or no values at all) --
    # fall back to tree_match2.py's own global-largest rule, unchanged.
    best_size = max(c[2] for c in cands)
    tied = [c for c in cands if c[2] == best_size]
    chosen = tied[0]
    note = (
        "ret block %s had no non-trivial value of its own; block %s "
        "(non-ret), largest surviving tree (tree_match2 fallback rule)"
        % (ret_block_id, chosen[0])
        if chosen[0] != ret_block_id else
        "ret block %s, largest surviving tree (fallback path, ret-only "
        "leaves)" % ret_block_id)
    return chosen[1], note


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
        normalizer="z3 simplify (bitvector), opaque atoms for helper calls",
        source="sem_anchored_spill_<lang>.json, ret-block-first value "
               "selection (tree_match3.py); tree_match2.py's global-"
               "largest rule kept as fallback for units whose ret block "
               "has no non-trivial value of its own",
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

    json.dump(units_doc, open(os.path.join(HERE, "tree_units3.json"), "w"),
               indent=1)
    json.dump(matches_doc, open(os.path.join(HERE, "tree_matches3.json"),
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
