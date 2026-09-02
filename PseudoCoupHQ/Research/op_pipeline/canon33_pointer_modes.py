#!/usr/bin/env python3
"""canon33_pointer_modes.py -- TASK 30 (c): the arrival-mode dimension
on every unit, the simplification of the pointer units, and the
mode-difference findings.

THREE STEPS, in order.

 1. MEASURE the arrival mode of every one of the 1,779 compiled units
    from its own ship text (arrival_modes.compiled_mode).  The brief
    says compiled units are plain; this run CHECKS that and reports
    every unit that is not, by name.

 2. READ the recorded arrival representation of the interpreter/JIT
    handlers from proposal_representation_dimension3.json (opened
    read-only) and normalize it into the same three-name vocabulary.
    Record, per handler, whether the SIMPLIFICATION the owner's ruling asks
    for has actually happened -- that is, whether the carve isolated a
    computation part and a canonical text was produced for it
    (prove_interp_computation.json, opened read-only) -- or whether it
    refused, with the refusal quoted.

 3. REPORT THE DIFFERENCES.  For every PROVED equality already on
    record between an interpreter computation part and a compiled
    unit, put the two units' arrival modes side by side.  Where they
    differ, that is the finding the owner's ruling names: the two units
    agree on the simplified instructions and differ in the recorded
    mode, and the difference is recorded, never discarded.

WHAT IS NOT DONE HERE, deliberately: no table is rebuilt, no recorded
status is rewritten, and no unit's membership is changed.  This
program only measures, reads and reports.

THE SPELLING BAN.  The candidate set for every comparison in step 3 is
the existing PROVED-equality list -- machine-form evidence.  No
operator token takes part in any key, grouping, pairing, row structure
or candidate selection.  The token appears once per row as a display
label.  The output declares
`"meta": {"role": "generator provenance"}` and is checked by
check_no_spelling_keys.py.

usage:
  canon33_pointer_modes.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arrival_modes as AM  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    handle = open(os.path.join(HERE, name))
    doc = json.load(handle)
    handle.close()
    return doc


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def compiled_modes():
    rows = {}
    tally = {}
    for lang in LANGS:
        units = load("sem_anchored_%s.json" % lang)["units"]
        for n in sorted(units, key=lambda x: int(x)):
            mode, evidence = AM.compiled_mode(units[n])
            row = {}
            row["unit"] = "%s/op_%s" % (lang, n)
            row["lang"] = lang
            row["mode"] = mode
            row["evidence"] = evidence
            row["operator"] = (units[n].get("meta") or {}).get(
                "operator")
            row["simplification"] = (
                "not applicable -- the operands arrive as their own "
                "values, so there is nothing to simplify away")
            if mode != AM.PLAIN:
                row["simplification"] = (
                    "the pointer seats are %s; the value computation "
                    "is what the unit does after the field reads"
                    % ", ".join(evidence["pointing_seats"]))
            rows[row["unit"]] = row
            tally[mode] = tally.get(mode, 0) + 1
    return rows, tally


def interpreter_modes():
    proposal = load("proposal_representation_dimension3.json")
    proofs = load("prove_interp_computation.json")
    simplified = {}
    for record in proofs["records"]:
        unit = record["unit"]
        if record.get("canonical_text") is None:
            continue
        simplified.setdefault(unit, record)
    rows = {}
    tally = {}
    handlers = list(proposal["handlers"])
    known = set()
    for handler in handlers:
        known.add(handler["unit"])
    for record in proofs["records"]:
        if record["unit"] in known:
            continue
        known.add(record["unit"])
        handlers.append({
            "unit": record["unit"],
            "lang": record.get("language"),
            "operator": None,
            "representation": None,
            "no_recorded_row": "this unit is an additional route "
                               "symbol sliced for the proofs; it has "
                               "no row in the recorded representation "
                               "column, so its arrival mode is not "
                               "asserted here",
        })
    for handler in handlers:
        unit = handler["unit"]
        recorded = handler.get("representation")
        mode = AM.normalize_recorded(recorded)
        row = {}
        row["unit"] = unit
        row["lang"] = handler.get("lang")
        row["operator"] = handler.get("operator")
        row["mode"] = mode
        row["recorded_representation"] = recorded
        if mode is None:
            row["mode_note"] = (
                "the recorded representation does not fit the "
                "three-name vocabulary and is NOT forced into it")
        row["evidence"] = {
            "evidence_class": "the tool's own testimony -- the "
                              "recorded representation column, itself "
                              "resting on DWARF reads and the carve",
            "source": "proposal_representation_dimension3.json "
                      "(read-only)",
        }
        proof = simplified.get(unit)
        if proof is None:
            row["simplification"] = "REFUSED"
            row["simplification_detail"] = (
                handler.get("computation") or {}).get(
                    "status", "no computation part isolated")
            row["simplified_text"] = None
        else:
            row["simplification"] = "DONE"
            row["simplified_text"] = proof["canonical_text"]
            row["simplification_detail"] = proof.get(
                "canonicalization_note")
        rows[unit] = row
        tally[str(mode)] = tally.get(str(mode), 0) + 1
    return rows, tally, proofs


def findings(compiled_rows, interp_rows, proofs):
    out = []
    for record in proofs["records"]:
        unit = record["unit"]
        interp_row = interp_rows.get(unit)
        if interp_row is None:
            continue
        for match in record.get("proved_equal_to") or []:
            compiled_unit = match.get("compiled_unit")
            compiled_row = compiled_rows.get(compiled_unit)
            if compiled_row is None:
                continue
            finding = {}
            finding["proved_relation"] = (
                "z3 proved bit-level equality of the simplified "
                "instructions, on record in "
                "prove_interp_computation.json")
            finding["unit_one"] = unit
            finding["unit_one_mode"] = interp_row["mode"]
            finding["unit_one_text"] = interp_row["simplified_text"]
            finding["unit_two"] = compiled_unit
            finding["unit_two_mode"] = compiled_row["mode"]
            finding["unit_two_text"] = match.get("compiled_text")
            finding["modes_differ"] = (
                interp_row["mode"] != compiled_row["mode"])
            # NO DISPLAY LABEL ON A PAIRING ROW.  An earlier draft
            # put the two units' tokens in a dict on this finding.
            # canon33_guard.py refused it by name: a finding is a
            # PAIRING row, and a token on a pairing row is exactly
            # what the spelling ban forbids.  The token stays where it
            # belongs -- once per unit, on that unit's own row in the
            # `compiled` / `interpreter` sections.
            out.append(finding)
    return out


def main(argv):
    log("STEP 1 -- the arrival mode of every compiled unit, measured "
        "on its own ship text")
    compiled_rows, compiled_tally = compiled_modes()
    total = 0
    for mode in sorted(compiled_tally):
        log("   %-40s %d" % (mode, compiled_tally[mode]))
        total = total + compiled_tally[mode]
    log("   %-40s %d" % ("TOTAL", total))
    not_plain = []
    for unit in sorted(compiled_rows):
        if compiled_rows[unit]["mode"] != AM.PLAIN:
            not_plain.append(unit)
    log("   compiled units that are NOT plain: %d %s"
        % (len(not_plain), not_plain))

    log("")
    log("STEP 2 -- the interpreter/JIT handlers' recorded arrival "
        "representation, and whether the simplification happened")
    interp_rows, interp_tally, proofs = interpreter_modes()
    for unit in sorted(interp_rows):
        row = interp_rows[unit]
        log("   %-52s %-34s %s"
            % (unit, row["mode"], row["simplification"]))
    log("   tally: %s" % interp_tally)

    log("")
    log("STEP 3 -- proved-equal pairs, with their arrival modes side "
        "by side")
    found = findings(compiled_rows, interp_rows, proofs)
    differing = []
    for finding in found:
        if finding["modes_differ"]:
            differing.append(finding)
    log("   proved pairs examined: %d" % len(found))
    log("   pairs whose arrival modes DIFFER: %d" % len(differing))
    seen = set()
    for finding in differing:
        key = (finding["unit_one"], finding["unit_one_mode"],
               finding["unit_two_mode"])
        if key in seen:
            continue
        seen.add(key)
        log("      %s [%s]" % (finding["unit_one"],
                               finding["unit_one_mode"]))
        log("         simplified: %s" % finding["unit_one_text"])
        log("      %s [%s]" % (finding["unit_two"],
                               finding["unit_two_mode"]))
        log("         simplified: %s" % finding["unit_two_text"])

    out = {}
    out["meta"] = {}
    out["meta"]["role"] = "generator provenance"
    out["meta"]["produced_by"] = "canon33_pointer_modes.py"
    out["meta"]["vocabulary"] = ["plain", "typed-pointer(T)", "tagged"]
    out["meta"]["compiled_tally"] = compiled_tally
    out["meta"]["interpreter_tally"] = interp_tally
    out["meta"]["proved_pairs_examined"] = len(found)
    out["meta"]["pairs_with_differing_modes"] = len(differing)
    out["meta"]["reads_read_only"] = [
        "sem_anchored_<lang>.json",
        "proposal_representation_dimension3.json",
        "prove_interp_computation.json",
    ]
    out["compiled"] = compiled_rows
    out["interpreter"] = interp_rows
    out["mode_difference_findings"] = found
    handle = open(os.path.join(HERE, "canon33_arrival_modes.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    log("")
    log("wrote canon33_arrival_modes.json -- %d compiled rows, %d "
        "interpreter rows, %d findings"
        % (len(compiled_rows), len(interp_rows), len(found)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
