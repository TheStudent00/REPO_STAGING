#!/usr/bin/env python3
"""build_proposal_representation_dimension3.py -- TASK 27, part 4.

Writes `proposal_representation_dimension3.json`: task 24's
`proposal_representation_dimension2.json` with the eight ruby and php
rows updated by THIS task's carves and proofs.  The two earlier
proposals stay on disk unchanged as records; nothing existing is
edited.

WHAT CHANGES, per row: `arrival` (REFUSED in round 4 for want of a
slice -- now a real lineage-confluence carve or a real, named
refusal), `computation`, `proof`, and the two would-be family rows that
depend on them.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Run:
  /tmp/reconnect_venv/bin/python3 build_proposal_representation_dimension3.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "proposal_representation_dimension3.json")

NINE = set([
    ("ruby", "vm_opt_plus"),
    ("ruby", "rb_fix_plus"),
    ("ruby", "rb_int_plus"),
    ("ruby", "rb_big_plus"),
    ("php", "add_function"),
    ("php", "ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("php", "ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("php", "ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("cpython", "long_add"),
])


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def carves_for(carves, lang, symbol):
    out = []
    for r in carves["records"]:
        if r["language"] == lang and r["symbol"] == symbol:
            out.append(r)
    return out


def proofs_for(proofs, lang, symbol):
    out = []
    for r in proofs["records"]:
        if r["language"] == lang and r["symbol"] == symbol:
            out.append(r)
    return out


def arrival_block(carve_records):
    """the arrival field for one handler, across its two builds."""
    per_build = []
    for r in carve_records:
        entry = {"build": r["build"], "outcome": r["outcome"]}
        if r["outcome"] == "CARVED":
            entry["boundary_address"] = r["boundary"]["address"]
            entry["boundary_instruction"] = r["boundary"]["instruction"]
            entry["arrival_prefix_instruction_count"] = len(
                r["arrival"]["instruction_indices"])
            entry["arrival_instructions"] = [
                x["mnem"] for x in r["arrival"]["instructions"]]
            entry["lineages_read_at_the_boundary"] = \
                r["boundary"]["lineages_read"]
            entry["seed_policy"] = r["seed_policy"]
        else:
            entry["refusal"] = r["refusal"]
        per_build.append(entry)
    status = "REFUSED at every build"
    for e in per_build:
        if e["outcome"] == "CARVED":
            status = "CARVED at: " + ", ".join(
                x["build"] for x in per_build if x["outcome"] == "CARVED")
    return {
        "status": status,
        "method": "lineage confluence -- the first instruction whose "
                  "super-chain includes both lineages (AgentMemory, "
                  "2026-08-31), computed by lineage_carve.py over the "
                  "task-20 fixed cutter",
        "per_build": per_build,
    }


def computation_block(carve_records):
    per_build = []
    for r in carve_records:
        if r["outcome"] != "CARVED":
            continue
        per_build.append({
            "build": r["build"],
            "computation_core": [x["mnem"]
                                 for x in r["computation_core"]["instructions"]],
            "instructions_after_the_answer": len(
                r["after_the_answer"]["instruction_indices"]),
            "note": r["after_the_answer"]["what"],
        })
    if not per_build:
        return {"status": "not isolated -- the arrival carve refused at "
                          "every build for this handler"}
    return {"status": "isolated", "per_build": per_build}


def proof_block(proof_records):
    per_build = []
    for r in proof_records:
        entry = {
            "build": r["build"],
            "verdict": r["verdict"],
            "dwarf_typed_key": r["dwarf_typed_key"],
            "computation_core": r["computation_core"],
        }
        if r["verdict"] == "PROVED":
            entry["canonical_text"] = r["canonical_text"]
            entry["canonicalization_note"] = r["canonicalization_note"]
            entry["candidates_considered"] = r["candidates_considered"]
            entry["counts"] = r["counts"]
            entry["proved_equal_to"] = [
                {"compiled_unit": p["compiled_unit"],
                 "compiled_text": p["compiled_text"]}
                for p in r["proved_equal_to"]]
        else:
            entry["why"] = r.get("why")
        per_build.append(entry)
    if not per_build:
        return {"attempted": False,
                "reason": "no isolated computation part to test",
                "verdict": "UNDECIDED (honest refusal, not forced)"}
    proved = [e for e in per_build if e["verdict"] == "PROVED"]
    verdict = "PROVED" if proved else per_build[0]["verdict"]
    return {"attempted": True, "verdict": verdict, "per_build": per_build}


def main():
    base = load("proposal_representation_dimension2.json")
    carves = load("lineage_carve.json")
    proofs = load("prove_interp_computation.json")

    handlers = []
    changed = 0
    for rec in base["handlers"]:
        rec = json.loads(json.dumps(rec))
        lang = rec["lang"]
        sym = rec["handler"]
        if lang == "cpython":
            rec["round_5_note"] = (
                "unchanged by task 27: this row's carve and proof were "
                "already real (interp_fastpath.json) and this task did not "
                "re-run them.")
            handlers.append(rec)
            continue
        cs = carves_for(carves, lang, sym)
        ps = proofs_for(proofs, lang, sym)
        rec["round_4_arrival"] = rec.get("arrival")
        rec["arrival"] = arrival_block(cs)
        rec["computation"] = computation_block(cs)
        rec["proof"] = proof_block(ps)
        rec["slice_source"] = (
            "op_units_ruby.json" if lang == "ruby" else "op_units_php.json")
        rec["provenance_is_weaker"] = True
        proved = rec["proof"].get("verdict") == "PROVED"
        if proved:
            rec["would_be_row_option_b_with_a"] = {
                "family_kind": "representation-keyed family whose members "
                               "ALSO carry a proved computation relation to "
                               "the compiled units in the comparable class",
                "row": {
                    "representation": rec.get("representation"),
                    "members": rec["unit"],
                    "computation_relation": "the computation part is z3-proved "
                                            "equal, for every value of every "
                                            "register it reads before writing, "
                                            "to the compiled units listed on "
                                            "this record's proof block",
                },
                "family_key_machine_form": "dwarf_type_pair='%s'"
                                           % rec.get("type_pair_read"),
            }
        else:
            rec["would_be_row_option_b_with_a"] = {
                "family_kind": "CANNOT STATE -- the computation part exists "
                               "but no comparable compiled class key does; the "
                               "reason is on the proof block and is not "
                               "smoothed over",
                "row": None,
                "family_key_machine_form": "dwarf_type_pair=%r"
                                           % rec.get("type_pair_read"),
            }
        changed += 1
        handlers.append(rec)

    extra = []
    for lang, sym in [("ruby", "fix_plus"), ("ruby", "rb_fix_plus_fix")]:
        cs = carves_for(carves, lang, sym)
        ps = proofs_for(proofs, lang, sym)
        extra.append({
            "lang": lang,
            "handler": sym,
            "unit": "%s/%s" % (lang, sym),
            "operator": "+",
            "why_it_is_here": "this symbol was reached by following the call "
                              "operands in the disassembly of the nine, and it "
                              "is where the bounded-width computation actually "
                              "happens at the anchor build.  It is NEW "
                              "material, deliberately kept OUT of the nine so "
                              "the set the owner ratifies does not change shape "
                              "under him.",
            "arrival": arrival_block(cs),
            "computation": computation_block(cs),
            "proof": proof_block(ps),
            "provenance_is_weaker": True,
        })

    out = {
        "meta": {
            "generator": "build_proposal_representation_dimension3.py",
            "task": "TASK 27 -- the ruby and php rows, with real carves and real proofs",
            "supersedes": "proposal_representation_dimension2.json (task 24) "
                          "and proposal_representation_dimension.json (round "
                          "4); both stay on disk unmodified as records",
            "reads": [
                "proposal_representation_dimension2.json (read-only)",
                "lineage_carve.json (this task's carves)",
                "prove_interp_computation.json (this task's proofs)",
            ],
            "what_changed": "the eight ruby and php rows.  In round 4 and "
                            "round 5's task 24 every one of them refused at "
                            "ARRIVAL for want of an op_units-shaped slice.  "
                            "Slices now exist (op_units_ruby.json, "
                            "op_units_php.json), so the carve was attempted "
                            "for real at both builds and the refusals that "
                            "remain are mechanical, not missing-material.",
            "table_membership_changes": "NONE -- dominant_table24.json and "
                                        "dom_ops22.json are not opened by this "
                                        "script.  Membership is the owner's "
                                        "ratification.",
            "php_build_note": "php's rows are now taken from a CLEAN, "
                              "uninstrumented anchor/ship pair built this "
                              "session (zero gcov symbols in each).  Round 2 "
                              "had only a coverage-instrumented single build, "
                              "recorded as a dead end in log_095.",
            "spelling": "the operator token appears exactly once per handler "
                        "record, as the display label on a unit-identifying "
                        "dict.  No key, grouping, pairing, row structure or "
                        "candidate selection uses it.  Checked by "
                        "check_no_spelling_keys.py, which this program runs "
                        "over its own output and refuses on failure.",
            "ready_for": "the owner's ratification of option B / option B-with-A, "
                         "now on nine-handler evidence rather than one",
        },
        "dwarf_cross_checks_at_the_other_build":
            base.get("dwarf_cross_checks_at_the_other_build"),
        "java_units_not_included_and_why":
            base.get("java_units_not_included_and_why"),
        "handlers": handlers,
        "additional_route_symbols_sliced_this_session": extra,
        "diff_against_round_5_task_24": {
            "rows_touched": changed,
            "field_groups_replaced": ["arrival", "computation", "proof",
                                      "would_be_row_option_b_with_a"],
            "round_4_arrival_kept_on_each_row_as": "round_4_arrival",
        },
        "summary": {
            "handlers_considered": len(handlers),
            "handlers_with_a_real_carve_at_some_build": len(
                [h for h in handlers
                 if str(h.get("arrival", {}).get("status", "")).startswith("CARVED")]),
            "handlers_with_a_proved_computation_part": len(
                [h for h in handlers
                 if h.get("proof", {}).get("verdict") == "PROVED"]),
            "handlers_type_incomparable": len(
                [h for h in handlers
                 if h.get("proof", {}).get("verdict") == "TYPE_INCOMPARABLE"]),
            "additional_route_symbols": len(extra),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    print("summary: %s" % json.dumps(out["summary"], indent=1))
    guard_code = refuse_own_output_on_spelling_keys(OUT)
    return guard_code


def refuse_own_output_on_spelling_keys(path):
    """THE MECHANICAL GUARD: run check_no_spelling_keys.py over the file
    just written and refuse this program's own output on failure."""
    import subprocess
    proc = subprocess.run(
        [sys.executable,
         os.path.join(HERE, "check_no_spelling_keys.py"), path],
        capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % path)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
