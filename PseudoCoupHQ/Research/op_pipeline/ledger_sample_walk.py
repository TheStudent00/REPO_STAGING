#!/usr/bin/env python3
"""ledger_sample_walk.py -- the unit test for `ledger.py`.

TASK 59 (c), round 12 (log_158).  Task 59 delivers `ledger.py`; task
60's `canonical_form.py` renders the populations into `canon39_*`.
This file does NOT re-render a population.  It walks a COMPUTED
SAMPLE and prints the rows, so what the module does is visible before
anything consumes it.

THE SAMPLE, computed and never typed in:

  1. EVERY ACCEPTANCE UNIT OF LOGS 152 AND 153.  The names are read
     out of the two logs' own text and out of `acceptance48.py` and
     `acceptance53.py`, by pattern, so the sample follows the record
     rather than a list somebody remembered.
  2. 50 RANDOM UNITS PER POPULATION, at a fixed seed so the sample is
     the same on every run.  The four populations:
       * regenerated -- the units of `canon38_regen_store/`
       * wrapped     -- the units of `canon38_wrapped_<language>.json`
       * carry-in    -- the units whose recorded ledger carries a
                        flag pair whose SETTER is one of FLAG_RULES'
                        carry-in setters (this is the population the
                        (a) repair is about)
       * runtime     -- the units of the recorded caller list (this is
                        the population the (b) repair is about)

Every unit is walked with `ledger.wrap_unit` and its rows printed.
Each print names its population, so no number here stands without one.

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

The sample is drawn from populations and from the recorded logs; no
candidate is selected by an operator token.

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ledger as L                                               # noqa: E402
import runtime_callee as RC                                      # noqa: E402

DEVCOMMS = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                        "DevComms")
UNIT_NAME = re.compile(r"\b((?:c|cpp|go|rust|swift)/(?:op|regen)_\d+)\b")
SEED = 59
PER_POPULATION = 50


def load_all_units():
    """{unit name -> (record, population, store path)} over both
    recorded populations."""
    table = {}
    for path in sorted(glob.glob(os.path.join(
            HERE, "canon38_regen_store", "*.json"))):
        doc = json.load(open(path))
        for name, record in doc["units"].items():
            table[name] = (record, "regenerated", path)
    for path in sorted(glob.glob(os.path.join(
            HERE, "canon38_wrapped_*.json"))):
        doc = json.load(open(path))
        for name, record in doc["units"].items():
            if name in table:
                continue
            table[name] = (record, "wrapped", path)
    return table


def acceptance_names():
    """the unit names logs 152 and 153 and their two acceptance scripts
    name, read by pattern out of those files."""
    sources = []
    for name in ("log_152_task52_ledger_repaired_canon38.md",
                 "log_153_task53_layer4_canon38_census.md"):
        sources.append(os.path.join(DEVCOMMS, name))
    for name in ("acceptance48.py", "acceptance53.py"):
        sources.append(os.path.join(HERE, name))
    found = []
    for path in sources:
        if not os.path.exists(path):
            continue
        text = open(path, errors="replace").read()
        for hit in UNIT_NAME.findall(text):
            if hit in found:
                continue
            found.append(hit)
    return found, [os.path.basename(one) for one in sources]


def carry_in_population(table):
    """the units whose RECORDED ledger carries a flag pair whose setter
    is one of FLAG_RULES' carry-in setters."""
    out = []
    for name in sorted(table):
        record = table[name][0]
        for row in record.get("ledger") or []:
            produced = row.get("produced_by") or {}
            if produced.get("kind") != "flag_pair":
                continue
            mnemonics = produced.get("mnem") or []
            if not mnemonics:
                continue
            if L.carry_in_stem(str(mnemonics[0])) is None:
                continue
            out.append(name)
            break
    return out


def print_rows(say, name, population, record, routines):
    fields = L.wrap_unit(
        record.get("body_text"),
        record.get("arrival_families") or [],
        record.get("result_family"),
        record.get("result_width") or 64,
        body_bytes=record.get("body_bytes"),
        runtime_routines=routines)
    say("  %s   [population: %s]" % (name, population))
    say("    body: %s" % fields["wrapped_text_resolved"])
    say("    %-8s %-26s %-34s %s"
        % ("row", "type", "produced by", "operands"))
    for row in fields["ledger"]:
        produced = row["produced_by"]
        if produced.get("kind") == "flag_pair":
            shown = " + ".join(produced.get("mnem") or [])
        elif produced.get("kind") == "runtime_callee":
            shown = "runtime %s" % produced.get("callee")
        elif produced.get("kind") == "non_opcode_phrase":
            shown = produced.get("phrase")
        else:
            shown = produced.get("mnem")
        half = row.get("written_half")
        if half is not None:
            shown = "%s [%s]" % (shown, half)
        say("    %-8s %-26s %-34s %s"
            % (row["row"], row["type"], shown,
               ",".join(row["operands"])))
    holes = fields["producer_holes"]
    if holes:
        say("    holes: %d" % len(holes))
        for hole in holes[:2]:
            say("      %s -- %s"
                % (hole.get("row_producer_hole"), hole.get("why")))
    say("")
    return fields


def main():
    lines = []

    def say(text):
        print(text)
        lines.append(text)

    table = load_all_units()
    say("== THE POPULATIONS WALKED ==")
    counted = {}
    for name in table:
        population = table[name][1]
        counted[population] = counted.get(population, 0) + 1
    for population in sorted(counted):
        say("  %-12s %d units" % (population, counted[population]))
    say("  %-12s %d units" % ("all", len(table)))
    say("")

    routines = []
    units_path = os.path.join(HERE, "runtime_callee_units.json")
    if os.path.exists(units_path):
        doc = json.load(open(units_path))
        for key, unit in doc["units"].items():
            if unit["callee"] in routines:
                continue
            routines.append(unit["callee"])
    say("runtime routines handed to the ledger (from "
        "runtime_callee_units.json, which reads each toolchain's own "
        "archive index): %s" % ", ".join(sorted(routines)))
    say("")

    accepted, sources = acceptance_names()
    say("== THE SAMPLE, COMPUTED ==")
    say("acceptance names read by pattern out of: %s"
        % ", ".join(sources))
    present = []
    absent = []
    for name in accepted:
        if name in table:
            present.append(name)
        else:
            absent.append(name)
    say("acceptance names found: %d; of those present in the recorded "
        "populations: %d; absent: %d %s"
        % (len(accepted), len(present), len(absent),
           ("(" + ", ".join(absent) + ")") if absent else ""))

    populations = {}
    populations["regenerated"] = []
    populations["wrapped"] = []
    for name in sorted(table):
        populations[table[name][1]].append(name)
    populations["carry-in"] = carry_in_population(table)
    caller_doc = RC.recorded_callers(HERE)
    runtime_names = []
    for one in caller_doc["units"]:
        if one["unit"] in table:
            runtime_names.append(one["unit"])
    populations["runtime"] = runtime_names

    generator = random.Random(SEED)
    sample = list(present)
    for population in sorted(populations):
        members = populations[population]
        say("  population %-12s %d units" % (population, len(members)))
        take = min(PER_POPULATION, len(members))
        drawn = generator.sample(sorted(members), take)
        for name in drawn:
            if name in sample:
                continue
            sample.append(name)
    say("  sample walked: %d units (seed %d)" % (len(sample), SEED))
    say("")

    say("== THE ACCEPTANCE UNITS, ROWS PRINTED ==")
    walked = 0
    refused = []
    for name in present:
        record, population, _ = table[name]
        try:
            print_rows(say, name, population, record, routines)
            walked = walked + 1
        except L.Refusal as trouble:
            refused.append((name, trouble.cause, trouble.detail))
            say("  %s   REFUSED BY NAME: %s -- %s"
                % (name, trouble.cause, trouble.detail))
            say("")

    say("== TWO CARRY-IN UNITS, ROWS PRINTED (the (a) repair) ==")
    shown = 0
    for name in populations["carry-in"]:
        if shown >= 2:
            break
        record, population, _ = table[name]
        try:
            print_rows(say, name, "carry-in", record, routines)
            shown = shown + 1
        except L.Refusal as trouble:
            refused.append((name, trouble.cause, trouble.detail))

    say("== TWO RUNTIME-CALLER UNITS, ROWS PRINTED (the (b) repair) ==")
    shown = 0
    for name in populations["runtime"]:
        if shown >= 2:
            break
        record, population, _ = table[name]
        try:
            print_rows(say, name, "runtime", record, routines)
            shown = shown + 1
        except L.Refusal as trouble:
            refused.append((name, trouble.cause, trouble.detail))

    say("== THE WHOLE SAMPLE, WALKED ==")
    kinds = {}
    types = {}
    holes = 0
    rows_total = 0
    for name in sample:
        entry = table.get(name)
        if entry is None:
            continue
        record, population, _ = entry
        if name not in present:
            walked_here = True
        else:
            walked_here = True
        if not walked_here:
            continue
        try:
            fields = L.wrap_unit(
                record.get("body_text"),
                record.get("arrival_families") or [],
                record.get("result_family"),
                record.get("result_width") or 64,
                body_bytes=record.get("body_bytes"),
                runtime_routines=routines)
        except L.Refusal as trouble:
            refused.append((name, trouble.cause, trouble.detail))
            continue
        if name not in present:
            walked = walked + 1
        for row in fields["ledger"]:
            rows_total = rows_total + 1
            kind = row["produced_by"]["kind"]
            kinds[kind] = kinds.get(kind, 0) + 1
            types[row["type"]] = types.get(row["type"], 0) + 1
        holes = holes + len(fields["producer_holes"])
    say("units in the sample: %d" % len(sample))
    say("units walked without refusal: %d" % walked)
    say("units refused by name: %d" % len(refused))
    for name, cause, detail in refused[:5]:
        say("  %s -- %s: %s" % (name, cause, detail))
    say("rows built over the sample: %d" % rows_total)
    say("rows by producer kind, over the sample of %d units:"
        % len(sample))
    for kind in sorted(kinds):
        say("  %-20s %d" % (kind, kinds[kind]))
    say("rows by type, over the same sample:")
    for one in sorted(types):
        say("  %-34s %d" % (one, types[one]))
    say("producer holes recorded over the sample: %d" % holes)

    path = os.path.join(HERE, "ledger_sample_walk_printed.txt")
    open(path, "w").write("\n".join(lines) + "\n")


main()
