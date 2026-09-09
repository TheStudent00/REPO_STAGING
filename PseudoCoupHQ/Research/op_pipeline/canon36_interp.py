#!/usr/bin/env python3
"""canon36_interp.py -- TASK 43, the INTERPRETER / JIT population (the
11 units of log_124) rendered into the region form.

THE FORM is region36.py's; the renderer, rule R and the gate are
canon36_universal.py's, imported so they cannot drift between
populations.

WHAT IS DIFFERENT ABOUT THIS POPULATION.  `interp_canon35.json` holds
9 units with a prior canonical text and 2 with none (ruby/vm_opt_plus
has no ship body at all; ruby/rb_big_plus's two lineages meet inside
callees that are not extracted units).  Those 2 are REFUSED here for
the reasons that file already records, quoted rather than restated.

The reference text for the gate is each unit's OWN PRIOR TEXT, which
is what log_124 gate-proved and what this population has in place of a
separately recorded ship text.  The obligation is the same one: the
value the region form leaves in the RESULT BLOCK equals the value the
prior text leaves in its answer home, for every value of every input
block.

THE ARRIVAL ANNOTATION rides beside the text, never inside it -- which
is what lets a `typed-pointer(PyLongObject*)` arrival and a `plain`
arrival meet on the same memory-based form.

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
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                           # noqa: E402
import canon36_universal as U36                                  # noqa: E402

OUT = os.path.join(HERE, "canon36_interp.json")


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
        _ = label
        prior_text = rec.get("prior_text")
        if prior_text is None:
            # php/add_function carries its text under a different key
            # shape in interp_canon35.json; take whichever it has and
            # RECORD which, rather than guessing a default.
            core = rec.get("core_after_substitution")
            if core:
                prior_text = "; ".join(core) + "; ret"
        if prior_text is None:
            units[label] = {
                "unit": label,
                "lang": rec.get("language"),
                "population": "interpreter",
                "outcome": "REFUSED",
                "refusal_cause": "no prior text in the record",
                "refusal": "interp_canon35.json's record for this unit "
                           "carries neither a prior text nor a core to "
                           "render",
            }
            continue
        entry_contract = U36.infer_entry_contract(prior_text)
        record = {
            "unit": label,
            "lang": rec["language"],
            "population": "interpreter",
            "operator": rec.get("operator"),
            "build": rec.get("build"),
            "prior_text": prior_text,
            "prior_text_source": rec.get("prior_text_source"),
            "arrival_annotation": rec.get("arrival_annotation"),
            "entry_contract": entry_contract,
            "entry_contract_source":
                "inferred from the unit's own prior text: the arrival "
                "lineages are the families the text reads before it "
                "writes them",
        }
        # AN OPERAND THAT ARRIVES IN A DESIGNATED LOCATION.  Round 7's
        # interpreter form seated some operands in memory slots
        # (`-0x8(%rsp)`), not registers.  Read literally, this lap would
        # take such a slot for the unit's OWN stack scratch and place it
        # in a temp block nothing fills -- measured at first
        # observation: the three php handler units.  So a slot the
        # record's own directory declares to be an OPERAND SEAT is
        # rewritten to the next free System V argument register before
        # rendering, and the gate binds that slot in the reference text
        # to the same symbol.  The rewrite is recorded per unit.
        operand_slots = []
        for entry in rec.get("designated_location_directory") or []:
            designation = entry.get("designation")
            if designation in (None, "answer"):
                continue
            location = entry.get("designated_location")
            if location is None:
                continue
            if location in prior_text:
                operand_slots.append((designation, location))
        seat_rewrites = []
        used = set()
        for token in U36.re.findall(r"%[a-z0-9]+", prior_text):
            family = U36.canon.FAMILY_OF.get(token[1:])
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
            prior_text = prior_text.replace(location, "%" + seat)
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
            record["prior_text"] = prior_text
            entry_contract = U36.infer_entry_contract(prior_text)
            record["entry_contract"] = entry_contract

        prior_lines = U36.split_lines(prior_text)
        home, width = BC10.answer_home_from_real(prior_lines)
        if home is None:
            home = entry_contract.get("a")
            width = 64
        record["answer_home"] = home
        attempts = []
        chosen = None
        for materialize in (True, False):
            fields, refusal = U36.render(entry_contract, prior_text, [],
                                         materialize, home, width)
            if refusal is not None:
                record["outcome"] = "REFUSED"
                record["refusal_cause"] = refusal[0]
                record["refusal"] = refusal[1]
                break
            region_lines = U36.split_lines(fields["universal_text"])
            families = U36.arrival_family_list(entry_contract)
            seed = {}
            bindings = U36.bind_region(seed, fields["block_directory"],
                                       families)
            verdict, detail = U36.compare(
                prior_lines, region_lines, seed, home, width,
                "the unit's own prior canonical text")
            if verdict == "UNDECIDED":
                ok, note = U36.structural_route(fields, prior_text)
                if ok:
                    verdict = "PROVED_BY_CONSTRUCTION"
                    detail = ("equivalence is forced by construction: "
                              "the region text executes this unit's own "
                              "core under an injective register "
                              "permutation, on the register state the "
                              "standardized loads establish")
                    fields["structural_route_checks"] = note
            attempts.append({
                "constant_materialization":
                    fields["constant_materialization"],
                "verdict": verdict,
                "detail": detail,
            })
            if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
                chosen = (fields, verdict, detail, bindings)
                break
            if chosen is None:
                chosen = (fields, verdict, detail, bindings)
            if fields["constant_materialization"] == "reduced":
                break
        if record.get("outcome") == "REFUSED":
            units[label] = record
            continue
        fields, verdict, detail, bindings = chosen
        record.update(fields)
        record["gate_attempts"] = attempts
        record["gate_verdict"] = verdict
        record["gate_detail"] = detail
        record["arrival_contract_bindings"] = bindings
        if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
            record["outcome"] = "REGION_TEXT_PROVED"
        elif verdict == "DISPROVED":
            record["outcome"] = "GATE_DISPROVED"
            record["universal_text"] = None
        else:
            record["outcome"] = "GATE_UNDECIDED"
            record["universal_text"] = None
        units[label] = record
    tally = {}
    for record in units.values():
        tally[record["outcome"]] = tally.get(record["outcome"], 0) + 1
    document = {
        "meta": {
            "role": "generator provenance",
            "generated_by": "canon36_interp.py",
            "form": "region36: the ruled virtual region, typed blocks "
                    "per lineage, no designated registers",
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
