#!/usr/bin/env python3
"""build_interp_join2.py -- TASK 34 part (c): the join between the
interpreter table and the compiled table, rebuilt on THE UNIVERSAL
CANONICAL FORM.

WHAT IS DIFFERENT FROM `build_interp_join1.py`.  The interpreter side
is now `interp_table2.json` -- nine units in the universal form,
every text carrying designated locations and standardized loads.  One
consequence is mechanical and worth stating: EVERY interpreter text now
contains a designated location, so every proof goes to task 30's
Sim33 through `interp_join_prover33.prove_pair_33`, with the
entry-contract binding tying each designated location to the compiled
side's designated register.  Under the register-based form the prover
was chosen per unit; under the universal form there is one path,
which is the point of the ruling.

WHAT IS DELIBERATELY UNCHANGED.  The candidate rule, the relation
vocabulary, the refusal texts and the prover are `build_interp_join1`'s
own, IMPORTED rather than copied, so this file cannot drift from the
rules TASK 32 established.  The candidate set is drawn from the
compiled population by TYPE KEY, never by any token.

`dominant_table24.json` is opened READ-ONLY and is not written.

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
  /tmp/reconnect_venv/bin/python3 build_interp_join2.py
"""

import json
import os
import subprocess
import sys

import cross_unit_prover as CUP
import interp_join_prover33 as P33
import build_interp_join1 as J1

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_join2.json")

INTEGER_64_KEYS = J1.INTEGER_64_KEYS
INTEGER_32_KEYS = J1.INTEGER_32_KEYS


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def class_of_interp_unit(table):
    out = {}
    for row in table["rows"]:
        for member in row["members"]:
            out[member["unit"]] = row
    return out


def main():
    interp = load("interp_table2.json")
    compiled_class_of, compiled_rows = J1.compiled_class_index()
    interp_class_of = class_of_interp_unit(interp)

    rows = J1.relations_on_record(interp_class_of, compiled_class_of)
    already = set([r["interp_unit"] for r in rows])

    text_of, meta_of, class_of = CUP.build_population()
    J1.COMPILED_LABELS = sorted(text_of.keys())

    attempts = []
    for row in interp["rows"]:
        for member in row["members"]:
            if member["unit"] in already:
                continue
            keys, refusal = J1.comparable_keys_for(
                dict(member, type_pair=row["type_pair"]))
            record = {
                "interp_unit": member["unit"],
                "interp_class_id": row["class_id"],
                "interp_universal_text": row["universal_text"],
                "arrival_annotation": member.get("arrival_annotation"),
                "provenance_is_weaker": True,
            }
            seats = member.get("seats_in_the_universal_form")
            if keys is None:
                record["relation"] = "TYPE_INCOMPARABLE"
                record["why"] = refusal
                testimony = member.get("type_pair_testimony")
                observe_keys = None
                if testimony in ("int32,int32",):
                    observe_keys = INTEGER_32_KEYS
                elif str(member.get("arrival_annotation") or "").startswith(
                        "typed-pointer"):
                    observe_keys = INTEGER_64_KEYS
                if observe_keys is not None:
                    (proved, counts, n, refused_detail, prover,
                     bindings) = J1.attempt(
                        text_of, class_of, member["unit"],
                        row["universal_text"], observe_keys, seats)
                    record["observation"] = {
                        "what_it_is": "a proof RUN whose outcome is "
                                      "recorded but which establishes "
                                      "NO relation, because the type "
                                      "key that would license the "
                                      "comparison does not exist",
                        "candidate_class_keys": observe_keys,
                        "candidates_considered": n,
                        "counts": counts,
                        "proved_equal_to": [p["compiled_unit"]
                                            for p in proved],
                        "proved_detail": (proved[0]["detail"]
                                          if proved else None),
                        "first_refusal_detail": refused_detail,
                        "prover": prover,
                        "entry_contract_bindings": bindings,
                    }
                rows.append(record)
                attempts.append(record)
                continue
            (proved, counts, n, refused_detail, prover,
             bindings) = J1.attempt(
                text_of, class_of, member["unit"], row["universal_text"],
                keys, seats)
            record["prover"] = prover
            record["entry_contract_bindings"] = bindings
            record["candidate_class_keys"] = keys
            record["candidates_considered"] = n
            record["counts"] = counts
            record["first_refusal_detail"] = refused_detail
            if proved:
                record["relation"] = "PROVED_EQUAL"
                record["proved_equal_to"] = [
                    {"compiled_unit": p["compiled_unit"],
                     "compiled_class_id":
                         compiled_class_of.get(p["compiled_unit"]),
                     "compiled_text": p["compiled_text"],
                     "detail": p["detail"]}
                    for p in proved]
                record["evidence_class"] = (
                    "forced by construction (solver unsat over the "
                    "universal texts, designated locations bound to the "
                    "compiled side's designated registers)")
            elif counts["undecided"] or counts["refused"]:
                record["relation"] = "UNDECIDED"
                record["why"] = (
                    "the prover neither proved nor refuted this text "
                    "against any of the %d candidates: %d undecided, "
                    "%d refused by the simulator" %
                    (n, counts["undecided"], counts["refused"]))
            else:
                record["relation"] = "NO_MATCH_IN_THE_COMPARABLE_CLASS"
            rows.append(record)
            attempts.append(record)

    # ---- interpreter-to-interpreter edges, same machine-form rule.
    interp_edges = []
    interp_rows = interp["rows"]
    for i in range(len(interp_rows)):
        for j in range(i + 1, len(interp_rows)):
            left, right = interp_rows[i], interp_rows[j]
            if left["type_pair"] is None or right["type_pair"] is None:
                continue
            if left["type_pair"] != right["type_pair"]:
                continue
            if left["result_type"] != right["result_type"]:
                continue
            if left["universal_text"] == right["universal_text"]:
                continue
            keys, refusal = J1.comparable_keys_for(
                {"type_pair": left["type_pair"]})
            if keys is None:
                continue
            left_seats = left["members"][0].get(
                "seats_in_the_universal_form")
            verdict, detail, bindings = P33.prove_pair_33(
                left["universal_text"], left_seats,
                right["universal_text"])
            interp_edges.append({
                "left_class_id": left["class_id"],
                "right_class_id": right["class_id"],
                "left_text": left["universal_text"],
                "right_text": right["universal_text"],
                "relation": ("PROVED_EQUAL" if verdict == "PROVED"
                             else verdict),
                "detail": detail,
                "entry_contract_bindings": bindings,
            })

    # ---- the guard rows, joined by CONDITION, exactly as TASK 32
    # computed them; the universal form does not touch this join.
    guard_join_rows = []
    families = load("exception_families3.json")
    interpreter_families = []
    compiled_families = []
    for family in families["families"]:
        langs = set(family["languages"])
        if langs & set(["cpython", "ruby", "php", "java"]):
            interpreter_families.append(family)
        else:
            compiled_families.append(family)
    for family in interpreter_families:
        matched = []
        for other in compiled_families:
            if other["condition_label"] != family["condition_label"]:
                continue
            matched.append({"family_id": other["family_id"],
                            "response_head": other["response_head"],
                            "languages": other["languages"]})
        guard_row = {
            "interpreter_family_id": family["family_id"],
            "condition_label": family["condition_label"],
            "interpreter_response_head": family["response_head"],
            "interpreter_languages": family["languages"],
            "compiled_families_with_the_same_condition_label": matched,
        }
        if matched:
            guard_row["relation"] = "DIFFERS_BY_DESIGN"
            guard_row["reading"] = ("one condition, two responses: the "
                                    "divergence condition IS the "
                                    "finding")
        else:
            guard_row["relation"] = "UNDECIDED_CONDITION_NOT_COMPARABLE"
            guard_row["why"] = (
                "no compiled family carries this exact condition label, "
                "and the two sides' labels are not one vocabulary: the "
                "compiled labels are solver-localised predicates over "
                "in0/in1, these are measured annotations in the "
                "runtime's own words.  Closing this needs the "
                "interpreter guard conditions put through the same "
                "solver localisation -- named, not attempted this lap.")
        guard_join_rows.append(guard_row)

    out = {
        "meta": {
            "generator": "build_interp_join2.py",
            "role_note": "PAIRING artifact (top-level `rows`, each "
                         "naming two units/classes) -- checked by "
                         "check_no_spelling_keys.py IN FULL, no "
                         "exemption claimed.",
            "task": "TASK 34 part (c) -- the join, on the universal "
                    "canonical form",
            "supersedes": "interp_join1.json (register-based texts)",
            "relation_values": ["PROVED_EQUAL", "UNDECIDED",
                                "TYPE_INCOMPARABLE",
                                "NO_MATCH_IN_THE_COMPARABLE_CLASS",
                                "DIFFERS_BY_DESIGN"],
            "candidate_rule": "a compiled 0-branch unit whose class key "
                              "is comparable with the interpreter "
                              "unit's OWN DWARF-read typed key.  No "
                              "token participates.  Imported from "
                              "build_interp_join1.comparable_keys_for "
                              "so the rule cannot drift.",
            "prover": "interp_join_prover33.prove_pair_33 "
                      "(canon33_gate.Sim33) for every row -- under the "
                      "universal form every interpreter text carries a "
                      "designated location",
            "opens_read_only": ["dominant_table24.json",
                                "interp_table2.json",
                                "exception_families3.json",
                                "prove_interp_computation.json",
                                "canon_interp_units_cpython.json",
                                "canon_interp_units_java.json"],
            "writes_to_the_compiled_table": "NONE",
            "provenance_is_weaker": True,
        },
        "rows": rows,
        "interpreter_to_interpreter_edges": interp_edges,
        "guard_join_rows": guard_join_rows,
        "compiled_classes_referenced": dict(
            [(r["compiled_class_id"], compiled_rows[r["compiled_class_id"]])
             for r in rows
             if r.get("compiled_class_id") in compiled_rows]),
        "route_symbols_not_in_the_nine": [
            {"unit": rec["unit"], "verdict": rec.get("verdict"),
             "note": "sliced by following a call operand (log_113); "
                     "kept out of the ratifiable set on purpose"}
            for rec in load("prove_interp_computation.json")["records"]
            if rec["unit"] not in interp_class_of],
        "summary": {},
    }
    tally = {}
    for row in rows:
        tally[row["relation"]] = tally.get(row["relation"], 0) + 1
    out["summary"] = {
        "join_row_count": len(rows),
        "by_relation": tally,
        "interpreter_to_interpreter_edge_count": len(interp_edges),
        "guard_join_row_count": len(guard_join_rows),
        "guard_join_by_relation": J1._tally(guard_join_rows),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    for row in rows:
        print("%-58s %-22s %s" % (row["interp_unit"], row["relation"],
                                  row.get("compiled_unit")
                                  or row.get("why", "")[:60]))
    for edge in interp_edges:
        print("interp<->interp %s %s %s" % (edge["left_class_id"],
                                            edge["right_class_id"],
                                            edge["relation"]))
    print("summary: %s" % json.dumps(out["summary"]))
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
         OUT], capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % OUT)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
