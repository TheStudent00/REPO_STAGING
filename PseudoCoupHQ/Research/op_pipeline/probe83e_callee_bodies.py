#!/usr/bin/env python3
"""probe83e_callee_bodies.py -- WHICH attached runtime-callee bodies
can be walked at all, measured one body per FORKED CHILD so each
body's own peak resident size and wall time are its own.

WHY.  `term.Term.runtime_row` steps into an attached callee by calling
`Reference.walk_body`, which forks the state at every conditional
transfer and merges the arms at every join with `If(condition, this
side, the rest)` over the whole register file.  A body with many forks
multiplies those merges.  `probe83b_memory.py` measured ONE unit,
`c/regen_1859`, growing +4,883,500 kB inside that walk.  A flag has to
say WHICH bodies do it, not which units happened to be walked first.

THE MEASUREMENT, and its bounds.  Each body is walked in a child
process of its own, so:
  * the child's `ru_maxrss` is that body's peak and nothing else's;
  * a runaway child is bounded twice -- RLIMIT_AS at 4 GB (an
    allocation past it raises MemoryError, reported as ABORT_MEMORY)
    and SIGALRM at 120 s (reported as ABORT_TIME);
  * a child that dies anyway is reported by its signal, and the parent
    walks on.
The parent holds counters and the callee index only, so the parent's
bound is trivial and is checked at the end.

NOTHING IS TRANSCRIBED: no term is built for any unit and nothing is
written into any store.

WRITES:
  probe83e_callee_bodies.json

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

The rows here are keyed by the TYPED producer object's own callee name
and by the toolchain that defines it -- machine-form evidence read off
`canon39_callee_units.json`.  No operator token appears in this file.
"""

import json
import os
import resource
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402

ADDRESS_SPACE_CAP = 4 * 1024 * 1024 * 1024
SECONDS_CAP = 120


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


class OutOfTime(Exception):
    pass


def alarm(signum, frame):
    raise OutOfTime()


def walk_in_child(reference, body, beside):
    """walk ONE body in a forked child.  Returns the child's report."""
    read_end, write_end = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(read_end)
        report = {}
        started = time.time()
        try:
            resource.setrlimit(resource.RLIMIT_AS,
                               (ADDRESS_SPACE_CAP, ADDRESS_SPACE_CAP))
            signal.signal(signal.SIGALRM, alarm)
            signal.alarm(SECONDS_CAP)
            state = R.MachineState(None)
            after = reference.walk_body(state, body, beside)
            signal.alarm(0)
            report["outcome"] = "walked"
            report["registers_after"] = len(after.registers)
        except OutOfTime:
            report["outcome"] = "ABORT_TIME"
        except MemoryError:
            report["outcome"] = "ABORT_MEMORY"
        except R.NotModeled as problem:
            report["outcome"] = "NotModeled"
            report["why"] = str(problem)[:300]
        except R.LeavesTheUnit as problem:
            report["outcome"] = "LeavesTheUnit"
            report["why"] = str(problem)[:300]
        except Exception as problem:
            report["outcome"] = type(problem).__name__
            report["why"] = str(problem)[:300]
        report["seconds"] = round(time.time() - started, 2)
        report["peak_kb"] = resource.getrusage(
            resource.RUSAGE_SELF).ru_maxrss
        try:
            os.write(write_end, json.dumps(report).encode())
        except Exception:
            pass
        os.close(write_end)
        os._exit(0)
    os.close(write_end)
    chunks = []
    while True:
        piece = os.read(read_end, 65536)
        if not piece:
            break
        chunks.append(piece)
    os.close(read_end)
    _done, status = os.waitpid(pid, 0)
    text = b"".join(chunks)
    if not text:
        killed = "died"
        if os.WIFSIGNALED(status):
            killed = "killed by signal %d" % os.WTERMSIG(status)
        return {"outcome": "CHILD_" + killed.upper().replace(" ", "_"),
                "seconds": None, "peak_kb": None}
    return json.loads(text.decode())


def count_transfers(body):
    """how many lines of this body are a conditional transfer, read off
    the body's own text.  Machine form: the mnemonic only."""
    forks = 0
    calls = 0
    for raw in body:
        text = raw.split("!!")[0].strip()
        if text == "":
            continue
        head = text.split(" ", 1)[0]
        if head == "call":
            calls = calls + 1
            continue
        if head.startswith("j") and head != "jmp":
            forks = forks + 1
    return forks, calls


def main():
    attached = RG.callee_units()
    reference = R.Reference(runtime_units=attached)
    total = 0
    for toolchain in attached:
        total = total + len(attached[toolchain])
    say("-- the population")
    say("   toolchains %d, attached callee bodies %d"
        % (len(attached), total))
    say("   each body walked in a forked child, bounded at %d bytes "
        "of address space and %d s"
        % (ADDRESS_SPACE_CAP, SECONDS_CAP))
    say("")
    say("   %-10s %-18s %6s %6s %6s %10s %12s  %s"
        % ("toolchain", "callee", "lines", "forks", "calls",
           "seconds", "peak kB", "outcome"))
    rows = []
    index = 0
    for toolchain in sorted(attached):
        beside = attached[toolchain]
        for callee in sorted(beside):
            index = index + 1
            unit = beside[callee]
            body = unit.get("body_verbatim") or unit.get("body_as_read")
            if not body:
                rows.append({"toolchain": toolchain, "callee": callee,
                             "lines": 0, "outcome": "EMPTY_BODY"})
                say("   %-10s %-18s %6d %6s %6s %10s %12s  %s"
                    % (toolchain, callee, 0, "-", "-", "-", "-",
                       "EMPTY_BODY"))
                continue
            forks, calls = count_transfers(body)
            report = walk_in_child(reference, body, beside)
            row = {"toolchain": toolchain, "callee": callee,
                   "lines": len(body), "conditional_transfers": forks,
                   "calls": calls}
            row.update(report)
            rows.append(row)
            say("   %-10s %-18s %6d %6d %6d %10s %12s  %s"
                % (toolchain, callee, len(body), forks, calls,
                   row.get("seconds"), row.get("peak_kb"),
                   row.get("outcome")))
            if index % 10 == 0:
                say("[%d/%d] bodies walked" % (index, total))
    say("[%d/%d] bodies walked" % (index, total))

    by_outcome = {}
    for row in rows:
        key = row.get("outcome")
        by_outcome[key] = by_outcome.get(key, 0) + 1
    say("")
    say("-- outcomes over the %d attached bodies" % len(rows))
    for key in sorted(by_outcome):
        say("   %-24s %d" % (key, by_outcome[key]))

    worst = []
    for row in rows:
        if row.get("peak_kb") is None:
            continue
        worst.append(row)
    worst.sort(key=lambda one: -one["peak_kb"])
    say("")
    say("-- the ten hungriest bodies")
    for row in worst[:10]:
        say("   %-10s %-18s %8d kB  %6s s  %s"
            % (row["toolchain"], row["callee"], row["peak_kb"],
               row.get("seconds"), row.get("outcome")))

    out = {
        "meta": {
            "produced_by": "probe83e_callee_bodies.py",
            "what_it_is": "every attached runtime-callee body walked "
                          "through Reference.walk_body in a forked "
                          "child of its own, with that child's peak "
                          "resident size and wall time",
            "bounds": "RLIMIT_AS %d bytes (ABORT_MEMORY) and SIGALRM "
                      "%d s (ABORT_TIME) per child"
                      % (ADDRESS_SPACE_CAP, SECONDS_CAP),
            "source": "canon39_callee_units.json, through "
                      "regate64_run.callee_units",
            "why": "term.Term.runtime_row steps into these bodies; "
                   "the t83 sample lane was killed by the container's "
                   "8 GB cgroup inside one such step",
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed",
        },
        "tally": {"bodies": len(rows), "by_outcome": by_outcome},
        "bodies": rows,
    }
    handle = open(os.path.join(HERE,
                               "probe83e_callee_bodies.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    say("")
    say("-- wrote probe83e_callee_bodies.json")
    say("   the PARENT's own peak resident %d kB"
        % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return 0


if __name__ == "__main__":
    sys.exit(main())
