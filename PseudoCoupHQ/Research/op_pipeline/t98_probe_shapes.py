#!/usr/bin/env python3
"""t98_probe_shapes.py -- ONE reading pass over each artifact family, to
settle two design questions before the stats pane is written:

  (1) HOW EXPENSIVE is a render-time walk of each family -- wall-clock
      seconds and peak resident size -- so the pane can be honest about
      which figures it counts at render time and which (if any) have to
      come from a stored summary;
  (2) WHICH DEFINITION of "how many arch opcodes a body holds" reproduces
      the figures task 98's brief measured (original corpus peaks at 3
      opcodes, 543 units, 30.5%, median 4, max 23).  Three candidate
      definitions are counted side by side and printed, and the one that
      agrees is the one the pane will use.

It computes nothing that is kept.  It reads, counts, and prints.

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

Nothing here groups, pairs or selects a unit.  Units are counted under
their LANGUAGE and their ARRIVAL POPULATION, both machine-form facts
carried on the record; the operator field is never read at all.

THE MEMORY BOUND.  Every document is parsed, reduced to counters, and
dropped before the next is opened.  No unit record and no body is held.

usage:
    t98_probe_shapes.py corpus     the canonical-form corpus (canon39)
    t98_probe_shapes.py canon40    the canon40 population and its proof
    t98_probe_shapes.py terms      term66_store, the term states
    t98_probe_shapes.py all        each of the three, in order
"""

import glob
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ["c", "cpp", "go", "rust", "swift"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def units_in(document):
    """the unit records of one artifact document, whichever of the two
    shapes it carries."""
    held = document.get("units")
    if isinstance(held, dict):
        return list(held.values())
    if isinstance(held, list):
        return held
    return []


def bump(counter, key):
    counter[key] = counter.get(key, 0) + 1


def ledger_mnems(unit):
    """the arch opcodes the LEDGER names as producers of this unit's
    rows.  Definition (a)."""
    found = set()
    for row in unit.get("ledger") or []:
        producer = row.get("produced_by") or {}
        kind = producer.get("kind")
        if kind == "arch_opcode":
            found.add(producer.get("mnem"))
        elif kind == "flag_pair":
            for one in producer.get("mnem") or []:
                found.add(one)
    found.discard(None)
    return found


def read_mnems(unit):
    """the arch opcodes the BODY spells, read off the head word of every
    instruction line, joined with the ledger's own.  Definition (b) --
    this is `mnems_of` in dashboard_ouro.py, which is the port of
    `mnemsOf` in dashboard_join.js."""
    found = set(ledger_mnems(unit))
    for row in unit.get("ledger") or []:
        producer = row.get("produced_by") or {}
        if producer.get("kind") == "runtime_callee":
            found.add("call")
    for line in unit.get("body_as_read") or []:
        head = str(line).strip().split(" ")[0].strip()
        if head and head[0].isalpha() and head.isalnum():
            found.add(head.lower())
    found.discard(None)
    return found


def body_lines(unit):
    """how many instruction lines the body holds.  Definition (c)."""
    return len(unit.get("body_as_read") or [])


def summarise(name, counter):
    total = 0
    for key in counter:
        total = total + counter[key] * key
    if not counter:
        say("  %-28s (empty)" % name)
        return
    keys = sorted(counter)
    population = sum(counter[key] for key in keys)
    top = max(keys, key=lambda k: (counter[k], -k))
    seen = 0
    median = keys[0]
    for key in keys:
        seen = seen + counter[key]
        if seen >= (population + 1) // 2:
            median = key
            break
    say("  %-28s population %d, peak at %d (%d units, %.1f%%), median %d, "
        "max %d, zero %d"
        % (name, population, top, counter[top],
           100.0 * counter[top] / population, median, keys[-1],
           counter.get(0, 0)))


def corpus():
    started = time.time()
    inputs = []
    for lang in LANGS:
        inputs.append("canon39_wrapped_%s.json" % lang)
    inputs.append("canon39_interp.json")
    shards = sorted(os.path.basename(p) for p in
                    glob.glob(os.path.join(HERE, "canon39_regen_store",
                                           "*.json")))
    for shard in shards:
        inputs.append(os.path.join("canon39_regen_store", shard))

    by_lang = {}
    by_pop = {}
    by_lang_pop = {}
    distinct_bytes = {}
    bytes_by_lang = {}
    ledger_dist = {}
    read_dist = {}
    line_dist = {}
    ledger_dist_pop = {}
    read_dist_pop = {}
    line_dist_pop = {}
    distinct_mnems_pop = {}
    empty_body_pop = {}
    compiled = 0
    total = 0

    for rel in inputs:
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for unit in units_in(document):
            total = total + 1
            lang = unit.get("lang") or "?"
            population = unit.get("population") or "original"
            bump(by_lang, lang)
            bump(by_pop, population)
            bump(by_lang_pop, (lang, population))

            raw = unit.get("body_bytes")
            if raw:
                compiled = compiled + 1
                bump(distinct_bytes, raw)
                if lang not in bytes_by_lang:
                    bytes_by_lang[lang] = {}
                bump(bytes_by_lang[lang], raw)

            one = len(ledger_mnems(unit))
            two = len(read_mnems(unit))
            three = body_lines(unit)
            bump(ledger_dist, one)
            bump(read_dist, two)
            bump(line_dist, three)
            for store, value in ((ledger_dist_pop, one),
                                 (read_dist_pop, two),
                                 (line_dist_pop, three)):
                if population not in store:
                    store[population] = {}
                bump(store[population], value)
            if population not in distinct_mnems_pop:
                distinct_mnems_pop[population] = set()
            distinct_mnems_pop[population].update(read_mnems(unit))
            if three == 0:
                bump(empty_body_pop, population)
        del document

    say("== the canonical-form corpus (canon39), %d inputs" % len(inputs))
    say("units total                    %d" % total)
    say("units carrying body_bytes      %d" % compiled)
    say("distinct body_bytes            %d" % len(distinct_bytes))
    if distinct_bytes:
        worst = max(distinct_bytes, key=lambda b: distinct_bytes[b])
        say("units per distinct body        %.1f"
            % (float(compiled) / len(distinct_bytes)))
        say("the most repeated body appears %d times"
            % distinct_bytes[worst])
    say("")
    say("-- per language")
    for lang in sorted(by_lang):
        say("  %-10s %d" % (lang, by_lang[lang]))
    say("-- per arrival population")
    for population in sorted(by_pop):
        say("  %-14s %d" % (population, by_pop[population]))
    say("-- per language and arrival population")
    for key in sorted(by_lang_pop):
        say("  %-10s %-14s %d" % (key[0], key[1], by_lang_pop[key]))
    say("-- repetition of machine code, per language")
    for lang in sorted(bytes_by_lang):
        held = bytes_by_lang[lang]
        units = sum(held.values())
        worst = max(held, key=lambda b: held[b])
        say("  %-10s %d units, %d distinct bodies, %.1f per distinct, "
            "most repeated %d"
            % (lang, units, len(held), float(units) / len(held),
               held[worst]))
    say("-- empty bodies, per arrival population")
    for population in sorted(empty_body_pop):
        say("  %-14s %d" % (population, empty_body_pop[population]))
    say("-- distinct arch opcodes, per arrival population "
        "(definition b, read_mnems)")
    for population in sorted(distinct_mnems_pop):
        say("  %-14s %d" % (population, len(distinct_mnems_pop[population])))
    say("")
    say("-- THE THREE CANDIDATE DEFINITIONS, whole corpus")
    summarise("(a) ledger arch producers", ledger_dist)
    summarise("(b) ledger + body heads", read_dist)
    summarise("(c) body instruction lines", line_dist)
    for population in sorted(by_pop):
        say("-- the three definitions, population %s" % population)
        summarise("(a) ledger arch producers", ledger_dist_pop[population])
        summarise("(b) ledger + body heads", read_dist_pop[population])
        summarise("(c) body instruction lines", line_dist_pop[population])
    say("")
    say("corpus walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def canon40():
    started = time.time()
    inputs = []
    for lang in LANGS:
        inputs.append("canon40_wrapped_%s.json" % lang)
    inputs.append("canon40_interp.json")
    shards = sorted(os.path.basename(p) for p in
                    glob.glob(os.path.join(HERE, "canon40_regen_store",
                                           "*.json")))
    for shard in shards:
        inputs.append(os.path.join("canon40_regen_store", shard))

    attempted = 0
    proved = 0
    outcomes = {}
    by_lang_proved = {}
    by_lang_not = {}
    for rel in inputs:
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for unit in units_in(document):
            attempted = attempted + 1
            lang = unit.get("lang") or "?"
            outcome = unit.get("outcome")
            bump(outcomes, outcome)
            if outcome == "WRAPPED_TEXT_PROVED":
                proved = proved + 1
                bump(by_lang_proved, lang)
            else:
                bump(by_lang_not, lang)
        del document

    say("== canon40, %d inputs" % len(inputs))
    say("units attempted                %d" % attempted)
    say("units proved                   %d" % proved)
    say("units not proved               %d" % (attempted - proved))
    say("-- every outcome value seen")
    for outcome in sorted(outcomes, key=lambda o: -outcomes[o]):
        say("  %-40s %d" % (outcome, outcomes[outcome]))
    say("-- not proved, per language")
    for lang in sorted(by_lang_not):
        say("  %-10s %d" % (lang, by_lang_not[lang]))
    say("")
    say("canon40 walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def terms():
    started = time.time()
    shards = sorted(glob.glob(os.path.join(HERE, "term66_store", "*.json")))
    records = 0
    by_lang = {}
    states = {}
    by_lang_state = {}
    for path in shards:
        document = json.load(open(path))
        for unit in units_in(document):
            records = records + 1
            lang = unit.get("lang") or "?"
            state = unit.get("term_state")
            bump(by_lang, lang)
            bump(states, state)
            bump(by_lang_state, (lang, state))
        del document

    say("== term66_store, %d shards" % len(shards))
    say("records                        %d" % records)
    say("-- per language")
    for lang in sorted(by_lang):
        say("  %-10s %d" % (lang, by_lang[lang]))
    say("-- every term state value seen")
    for state in sorted(states, key=lambda s: -states[s]):
        say("  %-20s %d" % (state, states[state]))
    say("-- per language and term state")
    for key in sorted(by_lang_state):
        say("  %-10s %-20s %d" % (key[0], key[1], by_lang_state[key]))
    say("")
    say("term walk: %.1f s, peak resident %.1f MB"
        % (time.time() - started, peak_mb()))


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("corpus", "all"):
        corpus()
        say("")
    if which in ("canon40", "all"):
        canon40()
        say("")
    if which in ("terms", "all"):
        terms()
        say("")
    say("whole process peak resident %.1f MB" % peak_mb())


if __name__ == "__main__":
    main()
