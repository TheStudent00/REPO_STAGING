#!/usr/bin/env python3
"""probe97a_unit_cost.py -- the SAMPLE the round's memory rule asks
for, before any walk: what one canon40 unit costs, unit by unit, with
the peak resident size pasted.

WHY IT EXISTS.  Task 83 measured the transcription's cost as wildly
uneven -- `op_units2_c_c0004` walked 24 records in 1,112 s while
`c0005` walked 94 in 2 s (log_189 section 3.1) -- and measured the
appetite as OPPORTUNISTIC: the peak follows whatever ceiling it is
given and the record does not change (log_189 section 2.6).  Both were
measured over a process that builds ONE `Term`, ONE `Gate` and ONE
`Reference` and then walks every unit of every shard through them, so
the z3 context accumulates for the whole run.  This probe measures the
other arrangement: a pristine parent that builds those three objects
and then FORKS one sub-process per unit, so each unit is answered in a
context that holds that unit and nothing else.

WHAT IT MEASURES, per unit:
  wall seconds, peak resident kB (ru_maxrss of the child, read by the
  parent through wait4), the record's term state, its outcome, its
  hole count, and whether a memory failure became a written reason.

THE BOUND.  Each child gets `RLIMIT_AS` at the stated ceiling and a
wall-clock alarm enforced by the PARENT with SIGKILL, so a child that
overruns is stopped from outside and cannot write a reason of its own.
The parent's own peak is printed at the end.  The named abort is
ABORT_MEMORY_T97.

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

No operator token appears in this file.  A unit's `operator` field is
carried onto its record as a DISPLAY LABEL and is never read for
grouping, pairing or candidate selection.

usage:
  probe97a_unit_cost.py <ceiling MB> <per-unit seconds> <shard key>...
"""

import json
import os
import resource
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import term66_run as TR                                          # noqa: E402
import regate64_run as RG                                        # noqa: E402

MEMORY_TOKENS = ["MemoryError", "out of memory", "out-of-memory",
                 "canceled", "max. memory exceeded"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_reason_in(record):
    """does this record carry a RUNNER limit as a term's own stated
    reason?  A record that does is a record about the sandbox, not
    about the compiler, and it is never stored."""
    text = json.dumps(record)
    for token in MEMORY_TOKENS:
        if token in text:
            return token
    return None


def runtime_rows_of_count(unit):
    """how many ledger rows name a runtime callee.  Reused by
    `probe97b_flag_reason.py` so the count is read from one place."""
    return TR.runtime_rows_of(unit)[0]


def build():
    """the three objects `term66_run.run` builds, built once in the
    parent so every forked child inherits them and pays no setup."""
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    gate = G.Gate(reference=reference)
    return maker, gate, attached, readings


def one_unit_forked(maker, gate, name, unit, ceiling_mb, seconds):
    """one unit answered in a forked sub-process of its own.

    Returns (outcome_word, record_or_None, wall_seconds, peak_kb).
    `outcome_word` is one of: walked, TIMED_OUT, ABORTED, RAISED,
    MEMORY_REASON."""
    read_end, write_end = os.pipe()
    started = time.time()
    child = os.fork()
    if child == 0:
        os.close(read_end)
        try:
            cap = ceiling_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            record = TR.one_unit(maker, gate, name, unit)
            payload = json.dumps({"ok": True, "record": record})
        except BaseException as problem:
            payload = json.dumps({"ok": False,
                                  "raised": "%s: %s"
                                  % (type(problem).__name__, problem)})
        handle = os.fdopen(write_end, "w")
        handle.write(payload)
        handle.close()
        os._exit(0)
    os.close(write_end)
    handle = os.fdopen(read_end, "r")
    text = ""
    timed_out = False
    # the parent enforces the wall clock; the child never sees it, so
    # a spent budget can never become a written reason on a record.
    signal.signal(signal.SIGALRM, lambda a, b: (_ for _ in ()).throw(
        TimeoutError()))
    signal.alarm(int(seconds) + 1)
    try:
        text = handle.read()
    except TimeoutError:
        timed_out = True
    signal.alarm(0)
    handle.close()
    if timed_out:
        os.kill(child, signal.SIGKILL)
    stamp = os.wait4(child, 0)
    wall = time.time() - started
    child_peak = stamp[2].ru_maxrss
    if timed_out:
        return "TIMED_OUT", None, wall, child_peak
    if text == "":
        return "ABORTED", None, wall, child_peak
    answer = json.loads(text)
    if not answer["ok"]:
        return "RAISED", {"raised": answer["raised"]}, wall, child_peak
    record = answer["record"]
    token = memory_reason_in(record)
    if token is not None:
        return "MEMORY_REASON", record, wall, child_peak
    return "walked", record, wall, child_peak


def main():
    ceiling = int(sys.argv[1])
    seconds = float(sys.argv[2])
    keys = sys.argv[3:]
    say("-- the sample's own bound")
    say("   per-unit address-space ceiling %d MB" % ceiling)
    say("   per-unit wall clock %.0f s, enforced by the parent with "
        "SIGKILL" % seconds)
    say("   named abort if the PARENT passes 6 GB: ABORT_MEMORY_T97")
    say("-- setup: the three objects, built once in the parent")
    before = peak_kb()
    started = time.time()
    maker, gate, attached, readings = build()
    say("   attached callee units %d" % len(attached))
    say("   runtime answer readings %d" % len(readings))
    say("   setup %.1f s, parent peak %d kB (was %d kB)"
        % (time.time() - started, peak_kb(), before))
    results = {}
    for key in keys:
        path = os.path.join(HERE, key)
        document = json.load(open(path))
        rows = []
        say("")
        say("======== %s ========" % key)
        names = sorted(document.get("units", {}))
        proved = []
        for name in names:
            if document["units"][name].get("outcome") != TR.PROVED:
                continue
            proved.append(name)
        say("   units in the shard %d, canon40-proved %d"
            % (len(names), len(proved)))
        for name in proved:
            unit = document["units"][name]
            outcome, record, wall, child = one_unit_forked(
                maker, gate, name, unit, ceiling, seconds)
            row = {"unit": name,
                   "outcome": outcome,
                   "wall_seconds": round(wall, 3),
                   "child_peak_kb": child,
                   "runtime_callee_rows": TR.runtime_rows_of(unit)[0]}
            if record is not None and "term_state" in record:
                row["term_state"] = record.get("term_state")
                row["verdict"] = record.get("outcome")
                row["holes"] = len(record.get("holes") or [])
            rows.append(row)
            if outcome != "walked" or wall > 5.0:
                say("   %-24s %-14s %8.2f s  %9d kB  runtime rows %d"
                    % (name, outcome, wall, child,
                       row["runtime_callee_rows"]))
            if peak_kb() > 6 * 1024 * 1024:
                raise SystemExit(
                    "ABORT_MEMORY_T97: parent peak %d kB passed 6 GB"
                    % peak_kb())
        results[key] = rows
        walls = [r["wall_seconds"] for r in rows]
        peaks = [r["child_peak_kb"] for r in rows]
        states = {}
        for r in rows:
            states[r["outcome"]] = states.get(r["outcome"], 0) + 1
        walls_sorted = sorted(walls)
        say("   -- over %d proved units of this shard" % len(rows))
        say("      outcomes %s" % json.dumps(states, sort_keys=True))
        say("      wall seconds  total %.1f  median %.2f  max %.2f"
            % (sum(walls),
               walls_sorted[len(walls_sorted) // 2] if walls else 0.0,
               max(walls) if walls else 0.0))
        say("      child peak kB  median %d  max %d"
            % (sorted(peaks)[len(peaks) // 2] if peaks else 0,
               max(peaks) if peaks else 0))
    say("")
    say("-- THE PARENT'S OWN PEAK RESIDENT SIZE %d kB" % peak_kb())
    out = os.path.join(HERE, "probe97a_unit_cost.json")
    handle = open(out, "w")
    json.dump({"ceiling_mb": ceiling,
               "per_unit_seconds": seconds,
               "parent_peak_kb": peak_kb(),
               "shards": results}, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- wrote probe97a_unit_cost.json")


if __name__ == "__main__":
    main()
