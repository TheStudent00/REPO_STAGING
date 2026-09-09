#!/usr/bin/env python3
"""canon38_zero_regression.py -- canon38 against canon37, unit by unit.

THE OBLIGATION (brief, step 4): no unit loses WRAPPED_TEXT_PROVED
without a named, proved cause.  This file computes the comparison
rather than asserting it: every unit present in either lap is looked
up in both, and every difference in outcome is printed with the unit's
own recorded reason on each side.

It also prints the three measurements the round's rulings are supposed
to move, so they are numbers and not adjectives:

  * how many wrapped texts still carry an angle-bracket symbol comment
    (ruling 4 should take this to zero);
  * how many distinct wrapped texts there are (log 148 §4.2.2
    predicted 6,277 -> about 2,999 over the pool's members);
  * how many ledgers carry a STACK row, an X87 row, a `flags only`
    row, and a row made by the per-opcode destination table.

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

import canon38_acceptance as ACC                                 # noqa: E402

OUT = os.path.join(HERE, "canon38_zero_regression.json")


def tally(units, field):
    out = {}
    for record in units.values():
        key = record.get(field)
        if key is None:
            key = "(no %s recorded)" % field
        out[key] = out.get(key, 0) + 1
    return out


def by_population(units):
    out = {}
    for label, record in units.items():
        key = record.get("population")
        if key not in out:
            out[key] = {}
        out[key][label] = record
    return out


def main():
    old = ACC.population("canon37")
    new = ACC.population("canon38")
    report = {}

    print("POPULATIONS, unit counts")
    print("  canon37 %d      canon38 %d" % (len(old), len(new)))
    missing = sorted(set(old) - set(new))
    extra = sorted(set(new) - set(old))
    print("  in canon37 and not canon38: %d %s"
          % (len(missing), missing[:5]))
    print("  in canon38 and not canon37: %d %s"
          % (len(extra), extra[:5]))
    report["units_canon37"] = len(old)
    report["units_canon38"] = len(new)
    report["only_in_canon37"] = missing
    report["only_in_canon38"] = extra

    print("")
    print("OUTCOME, per population")
    old_pop = by_population(old)
    new_pop = by_population(new)
    report["per_population"] = {}
    for name in sorted(set(old_pop) | set(new_pop)):
        was = tally(old_pop.get(name, {}), "outcome")
        now = tally(new_pop.get(name, {}), "outcome")
        print("  %-13s canon37 %s" % (name, json.dumps(was,
                                                       sort_keys=True)))
        print("  %-13s canon38 %s" % ("", json.dumps(now,
                                                     sort_keys=True)))
        report["per_population"][name] = {"canon37": was,
                                          "canon38": now}

    print("")
    print("VERDICT, all populations together")
    was = tally(old, "verdict")
    now = tally(new, "verdict")
    print("  canon37 %s" % json.dumps(was, sort_keys=True))
    print("  canon38 %s" % json.dumps(now, sort_keys=True))
    report["verdict_canon37"] = was
    report["verdict_canon38"] = now

    print("")
    print("EVERY UNIT WHOSE OUTCOME CHANGED")
    changed = []
    lost = []
    for label in sorted(set(old) & set(new)):
        before = old[label].get("outcome")
        after = new[label].get("outcome")
        if before == after:
            continue
        entry = {
            "unit": label,
            "was": before,
            "now": after,
            "canon37_reason": old[label].get("verdict_detail")
                              or old[label].get("refusal"),
            "canon38_reason": new[label].get("verdict_detail")
                              or new[label].get("refusal"),
        }
        changed.append(entry)
        if before == "WRAPPED_TEXT_PROVED":
            lost.append(entry)
    print("  outcome changed: %d" % len(changed))
    print("  lost WRAPPED_TEXT_PROVED: %d" % len(lost))
    for entry in changed[:40]:
        print("    %-22s %s -> %s" % (entry["unit"], entry["was"],
                                      entry["now"]))
        print("        canon38 says: %s" % entry["canon38_reason"])
    report["outcome_changed"] = changed
    report["lost_proved"] = lost

    print("")
    print("VERDICT CHANGES AMONG UNITS PROVED IN BOTH LAPS")
    verdict_moves = {}
    for label in sorted(set(old) & set(new)):
        if old[label].get("outcome") != "WRAPPED_TEXT_PROVED":
            continue
        if new[label].get("outcome") != "WRAPPED_TEXT_PROVED":
            continue
        pair = "%s -> %s" % (old[label].get("verdict"),
                             new[label].get("verdict"))
        verdict_moves[pair] = verdict_moves.get(pair, 0) + 1
    for pair in sorted(verdict_moves):
        print("  %-52s %d" % (pair, verdict_moves[pair]))
    report["verdict_moves"] = verdict_moves

    print("")
    print("RULING 4 -- THE SYMBOL COMMENT IN THE STORED TEXT")
    for name, units in (("canon37", old), ("canon38", new)):
        angle = 0
        texts = {}
        for record in units.values():
            text = record.get("wrapped_text")
            if text is None:
                continue
            texts[text] = texts.get(text, 0) + 1
            if "<" in text:
                angle = angle + 1
        print("  %s: wrapped texts %d, distinct %d, carrying a symbol "
              "comment %d" % (name, sum(texts.values()), len(texts),
                              angle))
        report["%s_texts" % name] = sum(texts.values())
        report["%s_distinct_texts" % name] = len(texts)
        report["%s_texts_with_symbol_comment" % name] = angle

    print("")
    print("RULINGS 2 AND 3 -- THE NEW ROWS")
    counters = {
        "units with a STACK row": 0,
        "units with an X87 row": 0,
        "units with a `flags only` row": 0,
        "units with a row from the destination table": 0,
        "units with a GUARD row whose reader is an unconditional "
        "transfer": 0,
    }
    stack_rows = 0
    x87_rows = 0
    flags_rows = 0
    table_rows = 0
    for record in new.values():
        rows = record.get("ledger")
        if not rows:
            continue
        has_stack = False
        has_x87 = False
        has_flags = False
        has_table = False
        for row in rows:
            if row["block"] == "STACK":
                has_stack = True
                stack_rows = stack_rows + 1
            if row["block"] == "X87":
                has_x87 = True
                x87_rows = x87_rows + 1
            if row["type"] == "flags only":
                has_flags = True
                flags_rows = flags_rows + 1
            if "written_half" in row:
                has_table = True
                table_rows = table_rows + 1
        if has_stack:
            counters["units with a STACK row"] += 1
        if has_x87:
            counters["units with an X87 row"] += 1
        if has_flags:
            counters["units with a `flags only` row"] += 1
        if has_table:
            counters["units with a row from the destination table"] += 1
    for key in sorted(counters):
        print("  %-58s %d" % (key, counters[key]))
    print("  %-58s %d" % ("STACK rows in total", stack_rows))
    print("  %-58s %d" % ("X87 rows in total", x87_rows))
    print("  %-58s %d" % ("`flags only` rows in total", flags_rows))
    print("  %-58s %d" % ("destination-table rows in total", table_rows))
    report["row_counts"] = {
        "units": counters,
        "stack_rows": stack_rows,
        "x87_rows": x87_rows,
        "flags_only_rows": flags_rows,
        "destination_table_rows": table_rows,
    }

    print("")
    print("THE GUARD ROWS AN UNCONDITIONAL TRANSFER USED TO MAKE")
    for name, units in (("canon37", old), ("canon38", new)):
        count = 0
        for record in units.values():
            for row in record.get("ledger") or []:
                produced = row["produced_by"]
                pair = None
                if isinstance(produced, list):
                    pair = produced
                if isinstance(produced, dict):
                    if produced.get("kind") == "flag_pair":
                        pair = produced.get("mnem")
                if not pair:
                    continue
                if pair[-1] in ("jmp", "jmpq"):
                    count = count + 1
        print("  %s: %d" % (name, count))
        report["%s_unconditional_transfer_guard_rows" % name] = count

    print("")
    print("THE ANSWER ROW'S PRODUCER, by kind")
    for name, units in (("canon37", old), ("canon38", new)):
        kinds = {}
        for record in units.values():
            rows = record.get("ledger")
            if not rows:
                continue
            for row in rows:
                if row["row"] != record.get("out_row"):
                    continue
                produced = row["produced_by"]
                if isinstance(produced, dict):
                    key = produced.get("kind")
                elif isinstance(produced, list):
                    key = "flag_pair"
                else:
                    key = "bare string"
                kinds[key] = kinds.get(key, 0) + 1
        print("  %s: %s" % (name, json.dumps(kinds, sort_keys=True)))
        report["%s_out_row_producer_kinds" % name] = kinds

    handle = open(OUT, "w")
    json.dump({"meta": {"generated_by": "canon38_zero_regression.py",
                        "what": "canon38 against canon37, unit by "
                                "unit, computed not asserted"},
               "report": report}, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("")
    print("written %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
