#!/usr/bin/env python3
"""probe83d_callee_population.py -- HOW BIG the blocker is: over every
unit canon40 proves, how many carry a ledger row whose typed producer
is `{"kind": "runtime_callee", "callee": ...}`, counted per callee.

WHY.  The t83 sample lane was SIGKILLed at the container's 8 GB cgroup
after 11 seconds, and `probe83b_memory.py` located the runaway in the
walk of ONE unit -- `c/regen_1859`, sixteen body lines, whose ledger
rows name the archive-defined routines `__floattisf` and
`__truncsfbf2`.  `term.Term.runtime_row` walks such a callee's whole
body through `Reference.walk_body`.  A flag needs its population, so
this probe counts how many units reach that walk and through which
callee.

THE MEMORY BOUND, stated: one canon40 shard is opened, counted and
dropped before the next.  Nothing is held across shards but integer
counters and the callee names themselves.  The cap is 6 GB resident,
checked after every shard, with the named abort ABORT_MEMORY.

NOTHING IS TRANSCRIBED and no term is built: this probe reads the
stored ledgers' producer objects only.

WRITES:
  probe83d_callee_population.json

Coding discipline: no compound one-liner statements.

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

The grouping key here is the TYPED PRODUCER OBJECT of the unit's own
ledger row -- `{kind, callee}` -- which is machine-form evidence read
off the artifact, exactly the key the census rule names.  No operator
token appears in this file.
"""

import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PROVED = "WRAPPED_TEXT_PROVED"
MEMORY_CAP_KB = 6 * 1024 * 1024


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY: peak resident %d kB passed the stated cap "
            "of %d kB" % (used, MEMORY_CAP_KB))
    return used


def shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE, "canon40_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon40_interp.json"))
    pattern = os.path.join(HERE, "canon40_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main():
    every = shards()
    say("-- the population")
    say("   canon40 inputs %d" % len(every))
    proved = 0
    not_proved = 0
    with_rows = 0
    rows_total = 0
    units_by_callee = {}
    rows_by_callee = {}
    units_by_callee_lang = {}
    already = set()
    done_store = os.path.join(HERE, "term66_store")
    for path in sorted(glob.glob(os.path.join(done_store, "*.json"))):
        document = json.load(open(path))
        already.add(document["shard"])
    say("   inputs already transcribed into term66_store %d"
        % len(already))

    index = 0
    for path in every:
        index = index + 1
        key = os.path.relpath(path, HERE)
        document = json.load(open(path))
        for name, unit in document.get("units", {}).items():
            if unit.get("outcome") != PROVED:
                not_proved = not_proved + 1
                continue
            proved = proved + 1
            seen = []
            for row in unit.get("ledger") or []:
                producer = row.get("produced_by") or {}
                if producer.get("kind") != "runtime_callee":
                    continue
                rows_total = rows_total + 1
                callee = producer.get("callee")
                rows_by_callee[callee] = rows_by_callee.get(callee, 0) + 1
                if callee in seen:
                    continue
                seen.append(callee)
            if not seen:
                continue
            with_rows = with_rows + 1
            for callee in seen:
                units_by_callee[callee] = units_by_callee.get(callee, 0) + 1
                lang = unit.get("lang")
                table = units_by_callee_lang.setdefault(callee, {})
                table[lang] = table.get(lang, 0) + 1
        document = None
        peak = check_memory()
        if index % 25 == 0 or index == len(every):
            say("[%d/%d] inputs read, peak %d kB"
                % (index, len(every), peak))

    say("")
    say("-- canon40, over %d proved units (%d not proved, not counted)"
        % (proved, not_proved))
    say("   units carrying at least one runtime-callee row %d"
        % with_rows)
    say("   runtime-callee rows in total %d" % rows_total)
    say("")
    say("   %-24s %10s %10s  %s"
        % ("callee (typed producer)", "units", "rows", "by language"))
    order = sorted(units_by_callee,
                   key=lambda one: (-units_by_callee[one], one))
    for callee in order:
        say("   %-24s %10d %10d  %s"
            % (callee, units_by_callee[callee], rows_by_callee[callee],
               json.dumps(units_by_callee_lang[callee], sort_keys=True)))

    out = {
        "meta": {
            "produced_by": "probe83d_callee_population.py",
            "what_it_is": "how many canon40-proved units reach "
                          "term.Term.runtime_row, and through which "
                          "attached callee, counted off the stored "
                          "ledgers' TYPED producer objects",
            "why": "the t83 sample lane was killed by the container's "
                   "8 GB cgroup; probe83b_memory.py located the "
                   "runaway inside one such walk, and a flag needs "
                   "its population",
            "population": "%d units canon40 proved of %d attempted "
                          "records read" % (proved, proved + not_proved),
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed",
        },
        "tally": {
            "proved_units_read": proved,
            "records_not_proved_not_counted": not_proved,
            "units_with_a_runtime_callee_row": with_rows,
            "runtime_callee_rows": rows_total,
            "inputs_already_in_term66_store": len(already),
        },
        "units_by_callee": units_by_callee,
        "rows_by_callee": rows_by_callee,
        "units_by_callee_and_language": units_by_callee_lang,
    }
    handle = open(os.path.join(HERE,
                               "probe83d_callee_population.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    say("")
    say("-- wrote probe83d_callee_population.json")
    say("   peak resident %d kB against the stated 6 GB cap"
        % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return 0


if __name__ == "__main__":
    sys.exit(main())
