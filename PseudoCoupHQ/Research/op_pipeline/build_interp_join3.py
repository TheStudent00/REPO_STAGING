#!/usr/bin/env python3
"""build_interp_join3.py -- TASK 39 step 5: the join RE-RUN against
the compiled table's universal-form column.  interp_join3.json.

WHAT CHANGES FROM build_interp_join2.py: TWO INPUTS, nothing else.

  1.  the compiled class index now reads `dominant_table25.json`
      (universal-form texts) instead of `dominant_table24.json`;
  2.  the compiled candidate population's TEXT is now the universal
      text (canon35_universal_<lang>.json) instead of the newest
      register-first canonical text.

Everything else is build_interp_join2.py's own code, IMPORTED and
monkeypatched at exactly those two seams, so the candidate rule, the
relation vocabulary, the prover and the row shape cannot drift.  The
interpreter side is unchanged: interp_table2.json's nine units are
already in the universal form (log_124).

WHY THE JOIN HAS TO BE RE-RUN AT ALL.  Both sides now spell their
values as designated locations, so both sides go through one prover
with one binding convention.  Under the register form the compiled
side's text named registers and the interpreter side's named
locations, and the binding had to bridge them.  That bridge is gone.

`dominant_table24.json` and `dominant_table25.json` are opened
READ-ONLY and neither is written.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Coding discipline: no complex/compound one-liner statements.

usage:
  build_interp_join3.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cross_unit_prover as CUP                                  # noqa: E402
import build_interp_join1 as J1                                  # noqa: E402
import build_interp_join2 as J2                                  # noqa: E402
import dom_ops_0branch as DB                                     # noqa: E402
import result_type_norm as RTN                                   # noqa: E402
import dominant_table17 as DT17                                  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def universal_texts():
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon35_universal_%s.json" % lang)
        for label, rec in json.load(open(path))["units"].items():
            text = rec.get("universal_text")
            if text is None:
                continue
            out[label] = text
    return out


def compiled_class_index_25():
    """compiled unit id -> the dominant_table25 class it sits in.
    Both compiled tables are opened READ-ONLY and neither is written."""
    path = os.path.join(HERE, "dominant_table25.json")
    table = json.load(open(path))
    out = {}
    rows = {}
    for row in table["rows"]:
        rows[row["class_id"]] = {
            "class_id": row["class_id"],
            "type_pair": row["type_pair"],
            "result_type": row["result_type"],
            "canonical_text": row["canonical_text"],
            "arrival_annotations": row.get("arrival_annotations"),
            "member_count": len(row["members"]),
        }
        for member in row["members"]:
            out[member["unit"]] = row["class_id"]
    return out, rows


def build_population_universal():
    """cross_unit_prover.build_population with the universal text."""
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    texts = universal_texts()
    text_of = {}
    meta_of = {}
    class_of = {}
    for lang, n, u, _text, _gen in units:
        label = "%s/op_%s" % (lang, n)
        universal = texts.get(label)
        if universal is None:
            continue
        text_of[label] = universal
        meta_of[label] = u.get("meta")
        pair = DB.type_pair_of(u)
        fam, note = RTN.class_family(lang, n, u.get("meta"))
        if fam is not None:
            rkey = fam
        else:
            rkey = "unknown:%s" % note
        class_of[label] = (pair, rkey)
    return text_of, meta_of, class_of


def main():
    J1.compiled_class_index = compiled_class_index_25
    CUP.build_population = build_population_universal
    J2.OUT = os.path.join(HERE, "interp_join3.json")
    code = J2.main()
    path = J2.OUT
    doc = json.load(open(path))
    doc["meta"]["generator"] = "build_interp_join3.py"
    doc["meta"]["task"] = ("TASK 39 step 5 -- the join re-run against "
                           "the compiled table's universal-form column")
    doc["meta"]["supersedes"] = ("interp_join2.json (the same join "
                                 "against dominant_table24.json's "
                                 "register-first texts)")
    doc["meta"]["opens_read_only"] = [
        "dominant_table25.json", "interp_table2.json",
        "canon35_universal_<lang>.json",
        "exception_families3.json", "prove_interp_computation.json",
        "canon_interp_units_cpython.json",
        "canon_interp_units_java.json"]
    doc["meta"]["two_monkeypatched_seams"] = [
        "build_interp_join1.compiled_class_index -> "
        "dominant_table25.json",
        "cross_unit_prover.build_population -> the universal texts"]
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    return code


if __name__ == "__main__":
    sys.exit(main())
