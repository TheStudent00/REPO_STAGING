#!/usr/bin/env python3
"""probe83f_one_unit_trace.py -- WHERE inside one unit's transcription
the memory goes, row by row.

WHAT IS ALREADY MEASURED, and why this probe is the next question.
`probe83e_callee_bodies.py` walked all 76 attached runtime-callee
bodies, each in a forked child from a FRESH machine state: 60 walked,
16 were refused by the opcode table, and the hungriest body in the set
took 56,676 kB and 0.21 s.  So no single attached body is the runaway.
`probe83b_memory.py` measured the unit `c/regen_1859` -- sixteen body
lines, whose ledger rows name `__floattisf` and `__truncsfbf2` --
growing +4,883,500 kB inside `term.Term.transcribe`.  The difference
between those two measurements is the CALLER's state: `runtime_row`
does not walk the callee from a fresh state, it walks it from the
state the caller's own rows have already built, and the walk merges
its arms with `If(condition, this side, the rest)` over that state.
This probe measures the size of the thing being carried, per row.

THE MEASUREMENT.  `Reference.walk_body` and `Term.runtime_row` are
wrapped -- IN THIS PROBE ONLY, by assignment on the imported class,
never on disk -- with a recorder that prints, for each call: the
body's line count, the current resident size before and after (read
from /proc/self/statm, so it falls as well as rises), the wall time,
and the AST NODE COUNT of the register the row reads.  The node count
is an iterative walk with a visited set and a hard cap, so counting
cannot itself run away.

THE BOUNDS.  The whole probe runs in a forked child with RLIMIT_AS at
3 GB and SIGALRM at 300 s, so a runaway is named -- ABORT_MEMORY or
ABORT_TIME -- instead of being killed by the container's cgroup.

NOTHING IS TRANSCRIBED and nothing is written into any store.

WRITES:
  probe83f_one_unit_trace.json

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

No operator token appears in this file.

usage:
  probe83f_one_unit_trace.py <shard path> <unit name>
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
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402
import term66_run as TR                                          # noqa: E402

ADDRESS_SPACE_CAP = 3 * 1024 * 1024 * 1024
SECONDS_CAP = 300
NODE_CAP = 4000000

TRACE = []


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


class OutOfTime(Exception):
    pass


def alarm(signum, frame):
    raise OutOfTime()


def resident_kb():
    """the CURRENT resident size, which falls as well as rises --
    ru_maxrss is a high-water mark and would hide a release."""
    handle = open("/proc/self/statm")
    fields = handle.read().split()
    handle.close()
    pages = int(fields[1])
    return pages * (os.sysconf("SC_PAGE_SIZE") // 1024)


def node_count(term):
    """the number of DISTINCT AST nodes under `term`, counted
    iteratively with a visited set and a hard cap so the counting
    cannot run away either."""
    if term is None:
        return 0
    seen = set()
    stack = [term]
    while stack:
        if len(seen) >= NODE_CAP:
            return NODE_CAP
        here = stack.pop()
        try:
            key = here.get_id()
        except Exception:
            continue
        if key in seen:
            continue
        seen.add(key)
        try:
            children = here.children()
        except Exception:
            continue
        for child in children:
            stack.append(child)
    return len(seen)


def install_recorders():
    original_walk = R.Reference.walk_body
    original_row = T.Term.runtime_row

    def recorded_walk(self, state, body_text, callees=None,
                      entered=None):
        lines = 0
        if isinstance(body_text, list):
            lines = len(body_text)
        before = resident_kb()
        started = time.time()
        entry = {"what": "walk_body", "body_lines": lines,
                 "resident_before_kb": before}
        TRACE.append(entry)
        try:
            after_state = original_walk(self, state, body_text,
                                        callees, entered)
        except Exception as problem:
            entry["outcome"] = type(problem).__name__
            entry["seconds"] = round(time.time() - started, 2)
            entry["resident_after_kb"] = resident_kb()
            say("   walk_body  %3d lines  %8d -> %8d kB  %6.2f s  %s"
                % (lines, before, entry["resident_after_kb"],
                   entry["seconds"], entry["outcome"]))
            raise
        entry["outcome"] = "walked"
        entry["seconds"] = round(time.time() - started, 2)
        entry["resident_after_kb"] = resident_kb()
        biggest = 0
        for family in after_state.registers:
            size = node_count(after_state.registers[family])
            if size > biggest:
                biggest = size
        entry["largest_register_ast_nodes"] = biggest
        say("   walk_body  %3d lines  %8d -> %8d kB  %6.2f s  "
            "largest register %d AST nodes"
            % (lines, before, entry["resident_after_kb"],
               entry["seconds"], biggest))
        return after_state

    def recorded_row(self, record, row, producer, line, shared, holder,
                     stack_rows, x87_rows):
        callee = producer.get("callee")
        before = resident_kb()
        started = time.time()
        entry = {"what": "runtime_row", "callee": callee,
                 "resident_before_kb": before}
        TRACE.append(entry)
        say("-- runtime_row into %s (resident %d kB)"
            % (callee, before))
        try:
            out = original_row(self, record, row, producer, line,
                               shared, holder, stack_rows, x87_rows)
        except Exception as problem:
            entry["outcome"] = type(problem).__name__
            entry["why"] = str(problem)[:300]
            entry["seconds"] = round(time.time() - started, 2)
            entry["resident_after_kb"] = resident_kb()
            say("   runtime_row %s -> %s (%d kB, %.2f s)"
                % (callee, entry["outcome"],
                   entry["resident_after_kb"], entry["seconds"]))
            raise
        entry["outcome"] = "built"
        entry["seconds"] = round(time.time() - started, 2)
        entry["resident_after_kb"] = resident_kb()
        entry["row_ast_nodes"] = node_count(record.terms.get(row["row"]))
        say("   runtime_row %s built: %d kB, %.2f s, row term %d AST "
            "nodes"
            % (callee, entry["resident_after_kb"], entry["seconds"],
               entry["row_ast_nodes"]))
        return out

    R.Reference.walk_body = recorded_walk
    T.Term.runtime_row = recorded_row


def child(shard, name):
    resource.setrlimit(resource.RLIMIT_AS,
                       (ADDRESS_SPACE_CAP, ADDRESS_SPACE_CAP))
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(SECONDS_CAP)
    attached = RG.callee_units()
    readings = CF.runtime_answer_readings()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    gate = G.Gate(reference=reference)
    say("-- setup done, resident %d kB" % resident_kb())
    document = json.load(open(os.path.join(HERE, shard)))
    unit = document["units"][name]
    say("-- the unit %s: %d body lines, %d ledger rows"
        % (name, len(unit.get("body_verbatim") or []),
           len(unit.get("ledger") or [])))
    runtime_rows = 0
    for row in unit.get("ledger") or []:
        producer = row.get("produced_by") or {}
        if producer.get("kind") == "runtime_callee":
            runtime_rows = runtime_rows + 1
    say("   of those, runtime-callee rows: %d" % runtime_rows)
    install_recorders()
    outcome = "walked"
    started = time.time()
    try:
        record = TR.one_unit(maker, gate, name, unit)
        say("-- the record: term_state %s, proved %s"
            % (record.get("term_state"), record.get("proved")))
    except MemoryError:
        outcome = "ABORT_MEMORY"
        say("ABORT_MEMORY: the 3 GB address-space bound was reached "
            "inside the transcription of %s" % name)
    except OutOfTime:
        outcome = "ABORT_TIME"
        say("ABORT_TIME: the %d s bound was reached inside the "
            "transcription of %s" % (SECONDS_CAP, name))
    signal.alarm(0)
    seconds = round(time.time() - started, 2)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    say("")
    say("-- the result for %s" % name)
    say("   outcome %s" % outcome)
    say("   wall time %s s" % seconds)
    say("   peak resident %d kB" % peak)
    out = {
        "meta": {
            "produced_by": "probe83f_one_unit_trace.py",
            "what_it_is": "one unit's transcription traced row by row, "
                          "with the resident size and the AST node "
                          "count at each step into an attached "
                          "runtime callee",
            "bounds": "RLIMIT_AS %d bytes and SIGALRM %d s in a forked "
                      "child" % (ADDRESS_SPACE_CAP, SECONDS_CAP),
            "unit": name,
            "shard": shard,
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed",
        },
        "result": {"outcome": outcome, "seconds": seconds,
                   "peak_kb": peak,
                   "runtime_callee_rows": runtime_rows},
        "trace": TRACE,
    }
    handle = open(os.path.join(HERE,
                               "probe83f_one_unit_trace.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- wrote probe83f_one_unit_trace.json")
    return 0


def main(argv):
    shard = argv[1]
    name = argv[2]
    pid = os.fork()
    if pid == 0:
        code = 0
        try:
            code = child(shard, name)
        except Exception as problem:
            sys.stdout.write("the probe raised %s: %s\n"
                             % (type(problem).__name__, problem))
            code = 1
        sys.stdout.flush()
        os._exit(code)
    _done, status = os.waitpid(pid, 0)
    if os.WIFSIGNALED(status):
        say("the probe child was killed by signal %d"
            % os.WTERMSIG(status))
        return 9
    return os.WEXITSTATUS(status)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
