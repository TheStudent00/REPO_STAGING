#!/usr/bin/env python3
"""canon38_interp.py -- TASK 52 (round 11), the INTERPRETER/JIT population (11
units) put through the memory-wrapped form.

THE FORM is ledger48.py's and THE GATE is canon38_gate.py's.

WHAT IS DIFFERENT ABOUT THIS POPULATION.  These units have no ship
text in the compiled corpus's sense; their record in
`interp_canon35.json` carries a prior text (or a core after
substitution).  So the body is that text, and the ONE gate is against
that same recorded text -- stated plainly rather than called a ship
proof it is not.

AN OPERAND THAT ARRIVES IN A DESIGNATED LOCATION.  Round 7's
interpreter form seated some operands in memory locations
(`-0x8(%rsp)`), not registers.  Read literally, this lap would take
such a location for the unit's own stack scratch.  So a location the
record's own directory declares to be an OPERAND SEAT is rewritten to
the next free System V argument register before wrapping, exactly as
canon36_interp.py did, and the rewrite is recorded per unit.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

usage:
  canon38_interp.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import canon10_behaviour_check as BC10                           # noqa: E402
import canon36_universal as U36                                  # noqa: E402
import canon38_gate as GATE                                      # noqa: E402
import ledger48 as L48                                           # noqa: E402

OUT = os.path.join(HERE, "canon38_interp.json")


def run():
    source = json.load(open(os.path.join(HERE, "interp_canon35.json")))
    units = {}
    for entry in source["units_with_no_universal_text"]:
        units[entry["unit"]] = {
            "unit": entry["unit"],
            "lang": entry["language"],
            "population": "interpreter",
            "outcome": "REFUSED",
            "refusal_cause": "no canonical text",
            "refusal": entry["why_not"],
            "refusal_quoted_from": "interp_canon35.json, verbatim",
            "what_would_change_it": entry["what_would_change_it"],
        }
    for rec in source["records"]:
        label = rec["unit"]
        body_text = rec.get("prior_text")
        if body_text is None:
            core = rec.get("core_after_substitution")
            if core:
                body_text = "; ".join(core) + "; ret"
        if body_text is None:
            units[label] = {
                "unit": label,
                "lang": rec.get("language"),
                "population": "interpreter",
                "outcome": "REFUSED",
                "refusal_cause": "no prior text in the record",
                "refusal": "interp_canon35.json's record for this unit "
                           "carries neither a prior text nor a core to "
                           "wrap",
            }
            continue
        record = {
            "unit": label,
            "lang": rec["language"],
            "population": "interpreter",
            "operator": rec.get("operator"),
            "build": rec.get("build"),
            "body_source": "the unit's own recorded interpreter text "
                           "(interp_canon35.json)",
            "arrival_annotation": rec.get("arrival_annotation"),
        }
        operand_slots = []
        for entry in rec.get("designated_location_directory") or []:
            designation = entry.get("designation")
            if designation in (None, "answer"):
                continue
            location = entry.get("designated_location")
            if location is None:
                continue
            if location in body_text:
                operand_slots.append((designation, location))
        seat_rewrites = []
        used = set()
        for token in re.findall(r"%[a-z0-9]+", body_text):
            family = canon.FAMILY_OF.get(token[1:])
            if family is not None:
                used.add(family)
        for designation, location in operand_slots:
            seat = None
            for family in U36.GENERAL_ARRIVAL_SEQUENCE:
                if family in used:
                    continue
                seat = family
                break
            if seat is None:
                continue
            used.add(seat)
            body_text = body_text.replace(location, "%" + seat)
            seat_rewrites.append({
                "designation": designation,
                "was_the_designated_location": location,
                "now_arrives_in": "%" + seat,
                "why": "the record's own directory declares this "
                       "location to be an operand seat, so it is an "
                       "INPUT lineage, not the unit's own scratch",
            })
        if seat_rewrites:
            record["operand_seat_rewrites"] = seat_rewrites
        record["body_text"] = body_text
        entry_contract = GATE.arrival_contract(rec["language"],
                                               body_text)
        record["entry_contract"] = entry_contract
        record["entry_contract_source"] = (
            "read off the unit's own body, in its language's own "
            "argument-register order: a family arrives when the body "
            "reads it before it writes it")
        body_lines = L48.split_lines(body_text)
        home, width = BC10.answer_home_from_real(body_lines)
        if home is None:
            home = entry_contract.get("a")
            width = 64
        record["result_family"] = home
        record["result_width"] = width
        families = GATE.arrival_family_list(entry_contract)
        try:
            fields = L48.wrap_unit(body_text, families, home, width)
        except L48.Refusal as bad:
            record["outcome"] = "REFUSED"
            record["refusal_cause"] = bad.cause
            record["refusal"] = bad.detail
            units[label] = record
            continue
        wrapped_lines = L48.split_lines(fields["wrapped_text_resolved"])
        seed = {}
        bindings = GATE.bind_arrival(seed, fields["ledger"], families)
        verdict, detail = GATE.compare(
            body_lines, wrapped_lines, seed, home, width,
            fields["out_row"],
            "the unit's own recorded interpreter text")
        if verdict == "UNDECIDED":
            ok, note = GATE.structural_route(fields)
            if ok:
                verdict = "PROVED_BY_CONSTRUCTION"
                detail = ("equivalence is forced by construction: the "
                          "wrapped text carries this unit's own body "
                          "character-for-character")
                fields["structural_route_checks"] = note
            else:
                fields["structural_route_refusal"] = note
        record.update(fields)
        record["verdict"] = verdict
        record["verdict_detail"] = detail
        record["arrival_contract_bindings"] = bindings
        if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
            record["outcome"] = "WRAPPED_TEXT_PROVED"
        elif verdict == "DISPROVED":
            record["outcome"] = "GATE_DISPROVED"
        else:
            record["outcome"] = "GATE_UNDECIDED"
        units[label] = record
    tally = {}
    for record in units.values():
        tally[record["outcome"]] = tally.get(record["outcome"], 0) + 1
    document = {
        "meta": {
            "generated_by": "canon38_interp.py",
            "form": "ledger48: the memory-wrapped form",
            "population": "interpreter",
            "note": "the operator field is a display label on the "
                    "member and is read by nothing",
        },
        "tally": tally,
        "units": units,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("interpreter %d units  %s"
          % (len(units), json.dumps(tally, sort_keys=True)))
    return 0


if __name__ == "__main__":
    sys.exit(run())
