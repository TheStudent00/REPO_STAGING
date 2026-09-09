#!/usr/bin/env python3
"""name_census4.py -- THE CENSUS, re-filtered against canon38.

WHAT THE CENSUS IS: the rows of every canon38 ledger whose PRODUCER
has no z3 term, filtered out of layer4c.py's transcriptions of every
unit task 52 proved.  A producer with no term is exactly what
layer4c raises `NoTerm` on, so the census is a filter and not a
survey.

WHAT IS NEW AGAINST name_census3.json (task 48's census, over
canon37): canon38 gave the ledger a STACK block, an X87 block, and a
per-opcode destination table, so the rows that carried log 147
section 4.1's first three causes now have producers with terms.  The
census is rebuilt, not adjusted.

THE `call` CAUSE, kept as a census row rather than fixed.  Log 152
section 5.1 found 305 units whose answer is produced by a library
routine (`__udivti3`, `__divti3`): no opcode in the body writes the
answer register, so OUT-0's producer is a phrase and no term is
built.  The coordinator's ruling for this task is that NO destination
rule for `call` is invented; the units appear here under their own
cause, with the callee names listed, awaiting the owner's ruling on whether
`call` joins the destination table.

TYPED PRODUCERS, NO ROLE KEY.  Every producer written into the
artifact is the typed machine-form object `{kind, mnem}` /
`{kind, phrase}`; no file this task writes declares
`role: generator provenance`, so the unmodified guard walks all of
them in full.

THE SPELLING BAN, pasted verbatim as required:


"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import layer4                                                     # noqa: E402
import ledger48 as L48                                            # noqa: E402


def canon38_paths():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        out.append(os.path.join(HERE, "canon38_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon38_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(HERE,
                                             "canon38_regen_store",
                                             "*.json"))))
    live = []
    for path in out:
        if os.path.exists(path):
            live.append(path)
    return live


def callees_of(unit):
    """the routines a body transfers out to, read off the body's own
    relocation annotation where it has one and off the transfer's own
    operand where it does not.  ledger48.reloc_callee is the same
    reader canon38 used to spell the callee into the text."""
    found = []
    for raw in unit.get("body_verbatim") or []:
        text, annotation = L48.split_off_annotation(raw)
        pieces = text.split()
        if not pieces:
            continue
        if pieces[0] not in ("call", "callq"):
            continue
        name = L48.reloc_callee(annotation)
        if name is None:
            if len(pieces) > 1:
                name = pieces[1]
            else:
                name = "an unnamed transfer out of the unit"
        if name not in found:
            found.append(name)
    return found


REGULAR_FAMILIES = (
    set(layer4.PLAIN_MOVE) | set(layer4.SIGN_EXTEND) |
    set(layer4.ZERO_EXTEND) | set(layer4.BINARY) | set(layer4.UNARY) |
    set(layer4.SHIFT) | set(layer4.FLAG_ONLY) |
    set(layer4.FLOAT_BINARY) | set(layer4.FLOAT_COMPARE) |
    set(layer4.PACKED_FLOAT) | set(layer4.BITWISE_128) |
    set(["lea", "movabs", "cvtsi2sd", "cvtsi2ss", "cvtss2sd",
         "cvtsd2ss", "unpckhpd", "punpckldq", "punpcklqdq", "pextrw",
         "sbb", "adc"])
)


def producer_key(producer):
    """one hashable key per producer, for tallying only.  It is never
    written into the artifact: the artifact carries the typed object."""
    if producer["kind"] == "flag_pair":
        return ("flag_pair", tuple(producer["mnem"]))
    if producer["kind"] == "arch_opcode":
        return ("arch_opcode", producer["mnem"])
    return ("non_opcode_phrase", producer["phrase"])


def producer_text(producer):
    """the producer as one line, FOR PRINTING ONLY -- the printed page
    is prose, not a keyed artifact."""
    if producer["kind"] == "flag_pair":
        return " + ".join(producer["mnem"])
    if producer["kind"] == "arch_opcode":
        return producer["mnem"]
    return producer["phrase"]


def shape_of(entry):
    if entry["producer_shape"] == "pair":
        return "irregular"
    producer = entry["producer"]
    if producer["kind"] != "arch_opcode":
        return "irregular"
    if producer["mnem"] in REGULAR_FAMILIES:
        return "regular"
    return "irregular"


def documents():
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "layer4c_terms_%s.json" % lang)
        if os.path.exists(path):
            out.append(("original", path))
    path = os.path.join(HERE, "layer4c_interp.json")
    if os.path.exists(path):
        out.append(("interpreter", path))
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "layer4c_regen_store",
                                              "*.json"))):
        out.append(("regenerated", path))
    return out


def build():
    rows = collections.Counter()
    units = collections.defaultdict(set)
    langs = collections.defaultdict(set)
    pops = collections.defaultdict(set)
    why = {}
    shapes = {}
    lines = collections.defaultdict(set)
    cascades = collections.Counter()
    cascade_units = collections.defaultdict(set)
    tally = collections.Counter()
    for population, path in documents():
        document = json.load(open(path))
        for name, record in document["units"].items():
            tally["units in the layer-4 population"] += 1
            tally["units, %s" % population] += 1
            if record.get("refused"):
                tally["units refused by the transcription"] += 1
            if record.get("term_built"):
                tally["units with an OUT-0 term"] += 1
            else:
                tally["units with no OUT-0 term"] += 1
            for entry in record.get("holes", []):
                key = producer_key(entry["producer"])
                shapes[key] = entry["producer"]
                rows[key] += 1
                units[key].add(name)
                langs[key].add(record.get("lang"))
                pops[key].add(population)
                why.setdefault(key, entry["why"])
                if entry.get("line"):
                    lines[key].add(entry["line"])
            for entry in record.get("cascades", []):
                key = producer_key(entry["producer"])
                shapes[key] = entry["producer"]
                cascades[key] += 1
                cascade_units[key].add(name)
            for route in ("ship", "textorder"):
                verdict = record.get("gate_%s_verdict" % route)
                tally["gate %s: %s" % (route, verdict)] += 1
    entries = []
    for key in sorted(rows, key=lambda one: (-rows[one], one)):
        entry = {
            "producer": shapes[key],
            "producer_shape": "pair"
                              if shapes[key]["kind"] == "flag_pair"
                              else "single",
            "rows_blocked": rows[key],
            "units_blocked": sorted(units[key]),
            "unit_count": len(units[key]),
            "languages": sorted([one for one in langs[key] if one]),
            "populations": sorted(pops[key]),
            "cannot_model_because": why[key],
            "example_body_lines": sorted(lines[key])[:3],
        }
        entry["regular_or_irregular"] = shape_of(entry)
        entries.append(entry)
    # THE CAUSE, defined the way log 152 section 5.1 defined it: the
    # ANSWER ROW's producer is a recorded phrase rather than an arch
    # opcode, and the body transfers out of the unit.  It is not
    # "every unit with no term", which is a larger set.
    call_units = []
    for population, path in documents():
        document = json.load(open(path))
        for name, record in document["units"].items():
            if record.get("term_built"):
                continue
            if not record.get("body_spells_a_call"):
                continue
            phrase_answer = False
            for entry in record.get("holes", []):
                if entry["row"] != "OUT-0":
                    continue
                if entry["producer"].get("kind") == "non_opcode_phrase":
                    phrase_answer = True
            if not phrase_answer:
                continue
            call_units.append(name)
    wanted = set(call_units)
    callees = collections.Counter()
    for path in canon38_paths():
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if name not in wanted:
                continue
            for callee in callees_of(unit):
                callees[callee] += 1
    call_cause = {
        "unit_count": len(call_units),
        "units": sorted(call_units),
        "callees": [{"callee": one, "unit_count": callees[one]}
                    for one in sorted(callees,
                                      key=lambda x: (-callees[x], x))],
        "cannot_model_because":
            "the answer is produced by a library call -- no opcode in "
            "the body writes OUT-0 -- awaiting the owner's ruling on `call` "
            "as a producer",
    }
    cascade_rows = []
    for key in sorted(cascades, key=lambda one: (-cascades[one], one)):
        cascade_rows.append({
            "producer": shapes[key],
            "rows_blocked": cascades[key],
            "unit_count": len(cascade_units[key]),
        })
    return {
        "meta": {
            "generated_by": "name_census4.py",
            "what_it_is": "the rows whose PRODUCER has no z3 term, "
                          "filtered out of the layer-4 transcriptions "
                          "of every unit task 52 proved",
            "keyed_on": "producer opcodes (machine form): an arch "
                        "opcode, or the pair (flag-setting opcode, "
                        "flag-reading opcode)",
            "supersedes": "name_census3.json, which was filtered over "
                          "canon37 (ledger47) and therefore carried "
                          "the machine stack, the x87 stack and the "
                          "implicit-destination opcodes as census "
                          "rows",
        },
        "tally": dict(tally),
        "entries": entries,
        "cascades_not_census_entries": cascade_rows,
        "answer_produced_by_a_library_call": call_cause,
    }


def print_census(census):
    print("THE CENSUS -- rows whose producer has no z3 term")
    print("population: every unit task 52 proved, all three "
          "populations")
    print("")
    print("%-34s %6s %6s %-10s %s"
          % ("producer", "rows", "units", "kind", "languages"))
    print("-" * 100)
    for entry in census["entries"]:
        print("%-34s %6d %6d %-10s %s"
              % (producer_text(entry["producer"]), entry["rows_blocked"],
                 entry["unit_count"], entry["regular_or_irregular"],
                 ",".join(entry["languages"])))
    print("")
    print("WHY EACH ONE CANNOT BE MODELLED")
    for entry in census["entries"]:
        print("  %s" % producer_text(entry["producer"]))
        print("      %s" % entry["cannot_model_because"])
    print("")
    print("THE ANSWER PRODUCED BY A LIBRARY CALL -- a census row, not "
          "a blocker")
    call_cause = census["answer_produced_by_a_library_call"]
    print("  units: %d" % call_cause["unit_count"])
    print("  cause: %s" % call_cause["cannot_model_because"])
    for one in call_cause["callees"]:
        print("      %-40s %d unit(s)" % (one["callee"],
                                          one["unit_count"]))
    print("")
    print("TALLY")
    for key in sorted(census["tally"]):
        print("  %-44s %d" % (key, census["tally"][key]))


def main():
    census = build()
    path = os.path.join(HERE, "name_census4.json")
    json.dump(census, open(path, "w"), indent=1, sort_keys=True)
    print_census(census)


if __name__ == "__main__":
    main()
