#!/usr/bin/env python3
"""t91_timeouts.py -- EVERY UNIT THAT HIT THE WALL CLOCK, FLAGGED AND
RE-RUN WITH MORE ROOM.

DEE'S RULE, 2026-09-04, verbatim: "if it timed out, why not have all
those flagged for things to either have a look at after or just re-run
with the rest of them and give them a longer processing time to see if
it changes the result?"

So this file takes every unit any of task 91's four runs left UNDECIDED
with the solver's own 3,000 ms wall clock named in the reason, plus
every unit whose verdict MOVED between the fix run and the control run
of one configuration (unchanged code, so that movement is the wall
clock and nothing else), and puts each one to the gate again with the
ceiling raised to 120,000 ms -- forty times the room.  Nothing about
what is measured changes: the same ledger, the same transcription, the
same reference, the same obligations.  Only the room changes, and the
report says whether the answer changed with it.

THE MEMORY BOUND: one canon38 source document at a time while the
bodies are collected, then one unit at a time; cap 6000 MB, abort
named T91_MEMORY_ABORT.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim."

No operator token appears in this file.  The candidate set is "the
units whose own recorded verdict named a wall clock" -- evidence off
the artifacts, never a spelling.

Coding discipline (the owner's ruling): no compound one-liner statements.

usage:
  t91_timeouts.py [ceiling milliseconds]
"""

import collections
import glob
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate as GATE                                               # noqa: E402
import layer4c                                                    # noqa: E402
import reference as REF                                           # noqa: E402

LANGS = ("c", "cpp", "go", "rust", "swift")
MEMORY_CAP_MB = 6000
MEMORY_ABORT = "T91_MEMORY_ABORT"
CONFIGURATIONS = ("attached_callees", "no_attached_callees")
OUT = os.path.join(HERE, "t91_timeouts.json")
WALL_CLOCK_WORDS = "did not answer inside its"


def peak_resident_mb():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024.0


def check_memory(stage):
    now = peak_resident_mb()
    if now > MEMORY_CAP_MB:
        raise SystemExit("%s: %.1f MB passed the cap of %d MB during %s"
                         % (MEMORY_ABORT, now, MEMORY_CAP_MB, stage))
    return now


def store_of(configuration, label):
    out = {}
    directory = os.path.join(HERE, "t91_regate_store_%s_%s"
                             % (configuration, label))
    for path in sorted(glob.glob(os.path.join(directory, "*.json"))):
        document = json.load(open(path))
        for name, record in document.get("units", {}).items():
            out[name] = record
    return out


def named_the_wall_clock(record):
    for side in ("ship", "text"):
        verdict = record.get(side) or {}
        reason = verdict.get("reason") or ""
        if WALL_CLOCK_WORDS in reason:
            return True
    return False


def flagged():
    """the two ways a unit reaches this file: its own verdict named the
    wall clock, or it answered differently on two runs of unchanged
    code."""
    why = collections.defaultdict(set)
    stores = {}
    for configuration in CONFIGURATIONS:
        for label in ("fix", "control"):
            store = store_of(configuration, label)
            stores[(configuration, label)] = store
            for name, record in store.items():
                if named_the_wall_clock(record):
                    why[name].add("its own verdict named the 3000 ms "
                                  "wall clock")
    for configuration in CONFIGURATIONS:
        fix = stores[(configuration, "fix")]
        control = stores[(configuration, "control")]
        for name in set(fix) & set(control):
            if fix[name].get("state") == control[name].get("state"):
                continue
            why[name].add("unchanged code answered it two ways")
    return why, stores


def bodies_for(names):
    out = {}
    paths = []
    for lang in LANGS:
        paths.append(os.path.join(HERE, "canon38_wrapped_%s.json"
                                  % lang))
    paths.append(os.path.join(HERE, "canon38_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(
        HERE, "canon38_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name in names:
            if name in out:
                continue
            record = document.get("units", {}).get(name)
            if record is None:
                continue
            if "ledger" not in record:
                continue
            unit = dict(record)
            unit["unit"] = name
            out[name] = unit
        del document
        check_memory("collecting bodies at %s" % os.path.basename(path))
        if len(out) == len(names):
            break
    return out


def state_of(ship, text):
    outcomes = (ship.outcome, text.outcome)
    if "DISPROVED" in outcomes:
        return "withdrawn"
    if "PROVED_ON_SHIP" in outcomes:
        return "proved"
    if "PROVED_BY_CONSTRUCTION" in outcomes:
        return "proved"
    return "undecided"


def callee_units():
    path = os.path.join(HERE, "canon39_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain") or key.split("/", 1)[0]
        callee = unit.get("callee") or key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][callee] = unit
    return out


def main():
    ceiling = 120000
    if len(sys.argv) > 1:
        ceiling = int(sys.argv[1])
    why, stores = flagged()
    print("units flagged for more room: %d" % len(why))
    reasons = collections.Counter()
    for name in why:
        for entry in why[name]:
            reasons[entry] += 1
    for entry, count in reasons.most_common():
        print("  %5d | %s" % (count, entry))
    bodies = bodies_for(set(why))
    print("bodies found in canon38:     %d" % len(bodies))
    print("the ceiling in force:        %d ms (the runs used %d ms)"
          % (ceiling, GATE.SOLVER_MILLISECONDS))

    archives = callee_units()
    rows = {}
    moved = collections.Counter()
    total = len(bodies) * len(CONFIGURATIONS)
    step = 0
    started = time.time()
    for configuration in CONFIGURATIONS:
        runtime_units = None
        if configuration == "attached_callees":
            runtime_units = archives
        reference = REF.Reference(runtime_units=runtime_units)
        gate = GATE.Gate(reference=reference,
                         solver_timeout_ms=ceiling)
        for name in sorted(bodies):
            step = step + 1
            unit = bodies[name]
            transcription = layer4c.transcribe(unit)
            term = transcription.out_term
            ship = gate.prove_term_against_ship(term, unit)
            text = gate.prove_term_against_text(term, unit)
            after = state_of(ship, text)
            before = (stores[(configuration, "fix")].get(name)
                      or {}).get("state")
            rows.setdefault(name, {})
            rows[name][configuration] = {
                "state_at_3000_ms": before,
                "state_at_%d_ms" % ceiling: after,
                "changed": before != after,
                "reason": ship.reason,
                "flagged_because": sorted(why[name]),
            }
            key = "%s: %s at 3000 ms -> %s at %d ms" % (
                configuration, before, after, ceiling)
            moved[key] += 1
            if step % 10 == 0:
                print("[%d/%d] %7.1fs  %s  %s -> %s"
                      % (step, total, time.time() - started, name,
                         before, after))
                sys.stdout.flush()
            check_memory("unit %s" % name)

    print("")
    print("WHAT MORE ROOM CHANGED, per configuration")
    for key, count in sorted(moved.items()):
        print("  %5d | %s" % (count, key))
    changed = 0
    for name in rows:
        for configuration in rows[name]:
            if rows[name][configuration]["changed"]:
                changed = changed + 1
    print("")
    print("verdicts that changed with more room: %d of %d"
          % (changed, total))
    handle = open(OUT, "w")
    json.dump({"meta": {"generated_by": "t91_timeouts.py",
                        "ceiling_ms": ceiling,
                        "run_ceiling_ms": GATE.SOLVER_MILLISECONDS},
               "movement": dict(moved),
               "units": rows}, handle, indent=1, sort_keys=True)
    handle.close()
    print("wrote %s" % OUT)
    print("PEAK RESIDENT SIZE: %.1f MB, cap %d MB"
          % (peak_resident_mb(), MEMORY_CAP_MB))


if __name__ == "__main__":
    main()
