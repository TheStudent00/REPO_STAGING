#!/usr/bin/env python3
"""name_census3.py -- THE CENSUS, built as a FILTER over the layer-4
transcriptions, and printed.

SUPERSEDES name_census2.py, AND SAYS WHY.  name_census2.json carried
each producer as a BARE STRING in a row field.  Several arch opcodes
are spelled exactly like operator tokens -- `and`, `or`, `xor`, `not`
-- so the spelling guard rejected the file, correctly: a bare token in
a row field is what the ban is about, and no amount of arguing that it
is "really" a mnemonic changes the shape on the page.  The repair is
STRUCTURAL, the same repair the `void` collision got: every producer is
now a TYPED MACHINE-FORM OBJECT (layer4.producer_object), with the
mnemonic under `mnem` -- this codebase's own ratified machine-form
field name.  This file also declares NO generator-provenance role: it
is walked in full by the guard, and it passes.

DEE'S RULING 3: "THE CENSUS IS A FILTER: rows whose producer has no z3
term; no mining over instruction sequences."  So this file does not
look at instructions, does not count recurrences, and does not rank
anything.  It reads the layer-4 records census48.py wrote and collects
the rows whose producer raised NoTerm.

THE CENSUS KEYS ON PRODUCER OPCODES, which are machine form: an arch
opcode, or a PAIR (flag-setting opcode, flag-reading opcode).  It never
keys on an operator token.  guard48.py's CHECK ONE proves that per
entry against the blocked unit's own body.

REGULAR AND IRREGULAR, defined here so the column means something:

  * REGULAR -- the producer is a single arch opcode that the corpus
    spells in a family this file's table can parse generically (the
    move family, the plain binary family, and so on).  A regular hole
    is closed by writing the family's rule once.
  * IRREGULAR -- the producer is a PAIR, or an arch opcode whose
    meaning is not a function of its named operands alone (an implicit
    destination, a machine-stack move).  An irregular hole is closed
    by modelling it FROM ITS ARCH OPCODES, per the round-10 addendum,
    never from a lifter's internal name.

A SEPARATE COLUMN, kept separate on purpose: CASCADES.  A row whose
producer HAS a term but whose operand row does not is not a census
entry -- its producer is modelled.  Counting it as one would report a
single hole many times.  It is tallied beside the census with the row
it was blocked by.

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
        path = os.path.join(HERE, "layer4b_terms_%s.json" % lang)
        if os.path.exists(path):
            out.append(("original", path))
    path = os.path.join(HERE, "layer4b_interp.json")
    if os.path.exists(path):
        out.append(("interpreter", path))
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "layer4b_regen_store",
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
    cascade_rows = []
    for key in sorted(cascades, key=lambda one: (-cascades[one], one)):
        cascade_rows.append({
            "producer": shapes[key],
            "rows_blocked": cascades[key],
            "unit_count": len(cascade_units[key]),
        })
    return {
        "meta": {
            "generated_by": "name_census3.py",
            "what_it_is": "the rows whose PRODUCER has no z3 term, "
                          "filtered out of the layer-4 transcriptions "
                          "of every unit task 47 wrapped",
            "keyed_on": "producer opcodes (machine form): an arch "
                        "opcode, or the pair (flag-setting opcode, "
                        "flag-reading opcode)",
            "supersedes": "name_census.json (keyed to canon24 and to "
                          "lifter names) and name_census2.json (whose "
                          "producer column was a bare string and was "
                          "rejected by the spelling guard)",
        },
        "tally": dict(tally),
        "entries": entries,
        "cascades_not_census_entries": cascade_rows,
    }


def print_census(census):
    print("THE CENSUS -- rows whose producer has no z3 term")
    print("population: every unit task 47 wrapped, all three "
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
    print("TALLY")
    for key in sorted(census["tally"]):
        print("  %-44s %d" % (key, census["tally"][key]))


def main():
    census = build()
    path = os.path.join(HERE, "name_census3.json")
    json.dump(census, open(path, "w"), indent=1, sort_keys=True)
    print_census(census)


if __name__ == "__main__":
    main()
