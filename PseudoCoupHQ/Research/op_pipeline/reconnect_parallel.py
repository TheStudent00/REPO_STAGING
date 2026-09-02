#!/usr/bin/env python3
"""reconnect_parallel.py -- Task 5(b): re-run java + cpython through
the ADOPTED pipeline (tree_match3.py's ret-block-first selection, the
current sem_anchored/sem_anchored_spill normalizer), fixing FINDING 3
(log_082 PART 2: `run_java_pipeline.sh` stopped at tree_match2.py,
and `tree_units3.json` was written before java/cpython existed).

NEW FILES ONLY (standing requirement). Every output of this script
carries the suffix `2` on its language tag (`java2`, `cpython2`) so it
writes NEW files (`sem_anchored_java2.json`, `sem_anchored_spill_
java2.json`, ...) and never touches `sem_anchored_java.json` or any
other existing artifact. The suffix is a FILENAME device only: the
`meta.language` field inside each output still reads the language's
real name, so a reader is never told these are a different language.

WHY THE SUFFIX WORKS SAFELY: `sem_anchored.py`'s ABI classification
(`ABI = {...}`, read 2026-08-31) is keyed by a literal language
string and already carries entries for "java" and "cpython" -- this
line's ABI facts were never the gap; the gap was the LANGS lists
downstream (langs.py's docstring) and the tree_match2 stopping point
(this file's fix). So this script borrows the real "java"/"cpython"
ABI rows for the "java2"/"cpython2" tags in memory only (never
writing to sem_anchored.py), which is sound because the ABI fact
("java's JIT ABI puts int args in rsi/rdx/rcx/r8/r9") is a fact about
the language, unaffected by the filename tag this run uses to avoid
overwriting the prior artifact.

STEPS
-----
1. op_units_java2.json  -- byte-identical copy of op_units_java.json
   (no defect was found in java's feeder output; FINDING 2 is
   cpython-only).
2. op_units_cpython2.json -- REBUILT from interp_cpython.json using
   interp_feeder.format_cpython(), which now carries the FIXED
   pointer type key (interp_feeder.cpython_type_key()).
3. sem_anchored_java2.json / sem_anchored_cpython2.json -- via
   sem_anchored.annotate(), unchanged logic, new language tag.
4. sem_anchored_spill_java2.json / sem_anchored_spill_cpython2.json --
   via sem_anchored_spill.annotate(), unchanged logic, new tag.
5. tree_units3_parallel.json / tree_matches3_parallel.json -- the
   FIVE compiled languages' existing sem_anchored_spill_<lang>.json
   (untouched, read only) PLUS java2/cpython2, run through
   tree_match3.py's own `normal_path_value` (ret-block-first) and
   `build_matches` (imported, unmodified) -- i.e. THE SAME selection
   rule the five-language line runs today, not a re-implementation.

THE SPELLING BAN: `operator` here is read only as the per-unit label
tree_match3.build_matches already treats it as (imported unchanged);
nothing in this file adds a new key, grouping, or candidate scope.
Run `check_no_spelling_keys.py tree_units3_parallel.json
tree_matches3_parallel.json op_units_cpython2.json` after this.

usage:
  reconnect_parallel.py
"""

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interp_feeder as FEED                                    # noqa: E402
import sem_anchored as SA                                        # noqa: E402
import sem_anchored_spill as SAS                                 # noqa: E402
import tree_match3 as TM3                                        # noqa: E402

import langs as L                                                # noqa: E402


def step1_java_units():
    src = os.path.join(HERE, "op_units_java.json")
    dst = os.path.join(HERE, "op_units_java2.json")
    shutil.copyfile(src, dst)
    print("wrote %s (byte copy of op_units_java.json)" % dst)


def step2_cpython_units():
    interp = FEED.parse_interp_log(os.path.join(HERE,
                                                  "interp_cpython.json"))
    op_units = FEED.format_cpython(interp)
    dst = os.path.join(HERE, "op_units_cpython2.json")
    json.dump(op_units, open(dst, "w"), indent=2)
    print("wrote %s (rebuilt with the fixed pointer type key)" % dst)
    key = op_units["probes"]["1"]["meta"]
    print("  lhs_rep=%r rhs_rep=%r (was i32,i32)"
          % (key["lhs_rep"], key["rhs_rep"]))


def step3_step4_lift(tag, real_lang):
    """steps 3+4: sem_anchored then sem_anchored_spill, for one
    `tag2`-suffixed language, borrowing `real_lang`'s ABI row."""
    SA.ABI[tag] = SA.ABI[real_lang]
    SA.annotate(tag)
    SAS.annotate(tag)


def load_tree3_units_for(tag):
    """the same per-unit record shape TM3.load_all_units() builds,
    for exactly one language tag, reading sem_anchored_spill_<tag>.json."""
    out = []
    path = os.path.join(HERE, "sem_anchored_spill_%s.json" % tag)
    doc = json.load(open(path))
    for n, u in doc["units"].items():
        meta = u["meta"]
        sem = u["sem"]
        rec = dict(lang=tag, n=n, operator=meta.get("operator"),
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
        root_text, rule = TM3.normal_path_value(blocks)
        rec["normal_path_block_rule"] = rule
        rec["carried"] = sem.get("carried", False)
        if root_text is None:
            rec["normal_path_root"] = None
            rec["note"] = "no return-bearing block with a value"
        else:
            norm, ok, note = TM3.normalize(root_text)
            rec["normal_path_raw"] = root_text
            rec["normal_path_root"] = norm
            rec["normalize_ok"] = ok
            rec["normalize_note"] = note
            tree = TM3.parse_expr(root_text)
            if tree[0] == "node":
                rec["subexp1_root_op"] = tree[1]
                rec["subexp2_children"] = [TM3.serialize(a)
                                            for a in tree[2]]
            else:
                rec["subexp1_root_op"] = None
                rec["subexp2_children"] = []
        out.append(rec)
    return out


def step5_match():
    units = []
    for lang in L.LANGS_COMPILED:
        units.extend(load_tree3_units_for(lang))
    units.extend(load_tree3_units_for("java2"))
    units.extend(load_tree3_units_for("cpython2"))

    exact, containment = TM3.build_matches(units)

    languages_out = L.LANGS_COMPILED + ["java2", "cpython2"]

    units_doc = dict(
        languages=languages_out,
        normalizer="z3 simplify (bitvector), opaque atoms for helper "
                   "calls -- identical to tree_units3.json",
        source="sem_anchored_spill_<lang>.json for the five compiled "
               "languages (read only, unchanged); sem_anchored_spill_"
               "java2.json / sem_anchored_spill_cpython2.json (built "
               "by this file) for the parallel branch. Ret-block-"
               "first value selection (tree_match3.py, imported "
               "unmodified).",
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
        languages=languages_out,
        exact_normalized_root=exact,
        containment=containment,
    )

    up = os.path.join(HERE, "tree_units3_parallel.json")
    mp = os.path.join(HERE, "tree_matches3_parallel.json")
    json.dump(units_doc, open(up, "w"), indent=1)
    json.dump(matches_doc, open(mp, "w"), indent=1)

    print("wrote %s (%d units)" % (up, len(units)))
    print("wrote %s" % mp)
    print("exact normalized-root clusters:", len(exact))
    print("  cross-language:", sum(1 for c in exact if c["cross_language"]))
    java_in = [c for c in exact
               if any(m["lang"] == "java2" for m in c["members"])]
    cpy_in = [c for c in exact
              if any(m["lang"] == "cpython2" for m in c["members"])]
    print("  clusters containing a java2 member:", len(java_in))
    print("  clusters containing a cpython2 member:", len(cpy_in))
    for c in java_in:
        langs_here = sorted(set(m["lang"] for m in c["members"]))
        print("    java2 cluster, langs=%s, root=%r"
              % (langs_here, c.get("normalized_root")))
    return units_doc, matches_doc


def main():
    step1_java_units()
    step2_cpython_units()
    step3_step4_lift("java2", "java")
    step3_step4_lift("cpython2", "cpython")
    step5_match()
    return 0


if __name__ == "__main__":
    sys.exit(main())
