#!/usr/bin/env python3
"""tree_match_extended.py -- task 5(b): re-run java + cpython through
the ADOPTED pipeline (tree_match3's ret-block-first selection, its
current normalizer), reading java's real sem file and cpython's
FIXED type-keyed sem file (fix_cpython_type_key.py, task 5(a)).

WHY A NEW FILE INSTEAD OF RE-RUNNING tree_match3.py ITSELF.
`tree_match3.py`'s own `LANGS = SAS.LANGS` already chains through
`sem_anchored_spill.py` -> `sem_anchored.py`, whose `LANGS` list
already names java and cpython (log_082's finding 1 is about
DOWNSTREAM stages that hardcode their OWN five-language list, not
about this chain).  `tree_units3.json` / `tree_matches3.json` on disk
predate `sem_anchored_spill_java.json` / `_cpython.json` by about two
hours (2026-08-30 15:20 vs 17:04) -- they were simply never
re-run after those files were written.  Re-running `tree_match3.py`
in place would overwrite them, which the brief for this line forbids
("new files only -- never modify or delete existing artifacts").  So
this script re-implements `tree_match3.py`'s `load_all_units()` loop
(reusing every actual matching function -- `normal_path_value`,
`normalize`, `parse_expr`, `serialize`, `candidate_values`,
`build_matches` -- by import, unchanged) but:

  1. reads languages from `langs.py`'s `LANGS_COMPILED + LANGS_INTERP`
     (task 5(b)'s "one LANGS source of truth"), not a local hardcode;
  2. reads cpython from `sem_anchored_spill_cpython_fixed.json` (the
     machine-fact-keyed file) instead of the original
     `sem_anchored_spill_cpython.json`;
  3. writes to NEW files -- `tree_units_extended.json`,
     `tree_matches_extended.json` -- so the existing five-language
     artifacts are untouched, per the no-edit rule.

THE SPELLING BAN: unchanged from tree_match3.py -- `operator` is a
display label; `build_matches` (imported, untouched) groups on
normalized-root text and containment, never on the token.
check_no_spelling_keys.py is run on both outputs by this script's
__main__ block.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match3 as TM3                                     # noqa: E402
import langs as LANGS_MOD                                      # noqa: E402

normal_path_value = TM3.normal_path_value
normalize = TM3.normalize
parse_expr = TM3.parse_expr
serialize = TM3.serialize
build_matches = TM3.build_matches

LANGS = LANGS_MOD.LANGS_COMPILED + LANGS_MOD.LANGS_INTERP

FILE_OVERRIDE = {
    "cpython": "sem_anchored_spill_cpython_fixed.json",
}


def sem_file_for(lang):
    name = FILE_OVERRIDE.get(lang, "sem_anchored_spill_%s.json" % lang)
    return os.path.join(HERE, name)


def load_all_units():
    out = []
    for lang in LANGS:
        path = sem_file_for(lang)
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
        source_note="tree_match_extended.py: tree_match3.py's own "
                     "matching functions, reused by import unchanged; "
                     "LANGS from langs.LANGS_COMPILED + langs.LANGS_INTERP "
                     "instead of a local hardcode; cpython read from "
                     "sem_anchored_spill_cpython_fixed.json (the "
                     "machine-fact type key, fix_cpython_type_key.py) "
                     "instead of the original i32,i32 file.",
        normalizer="z3 simplify (bitvector), opaque atoms for helper "
                   "calls -- tree_match3.py's normalize(), unchanged",
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

    units_path = "/persist/tree_units_extended.json"
    matches_path = "/persist/tree_matches_extended.json"
    json.dump(units_doc, open(units_path, "w"), indent=1)
    json.dump(matches_doc, open(matches_path, "w"), indent=1)

    print("languages:", LANGS)
    print("units total:", len(units))
    print("units with normal-path root:", sum(1 for u in units
                                                if u.get("normal_path_root")))
    print("exact normalized-root clusters:", len(exact))
    print("  cross-language:", sum(1 for c in exact if c["cross_language"]))
    print("containment edges:", len(containment))

    # zero-regression check: every c/cpp/go/rust/swift unit's newest
    # normal_path_root must be byte-identical to tree_units3.json's.
    prior_path = os.path.join(HERE, "tree_units3.json")
    prior = json.load(open(prior_path))
    prior_by_key = {(u["lang"], u["n"]): u.get("normal_path_root")
                     for u in prior["units"]}
    regressions = []
    for u in units_doc["units"]:
        if u["lang"] not in ("c", "cpp", "go", "rust", "swift"):
            continue
        key = (u["lang"], u["n"])
        if key in prior_by_key:
            if prior_by_key[key] != u.get("normal_path_root"):
                regressions.append(key)
    print("zero-regression check (core five vs tree_units3.json): "
          "%d units compared, %d regressions"
          % (len(prior_by_key), len(regressions)))
    if regressions:
        print("REGRESSIONS:", regressions[:20])

    print()
    print("spelling guard:")
    rc1 = subprocess.call([sys.executable,
                            os.path.join(HERE, "check_no_spelling_keys.py"),
                            units_path])
    rc2 = subprocess.call([sys.executable,
                            os.path.join(HERE, "check_no_spelling_keys.py"),
                            matches_path])
    if rc1 or rc2:
        print("SPELLING GUARD FAILED -- refusing this output per THE "
              "SPELLING BAN's mechanical-guard requirement.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
