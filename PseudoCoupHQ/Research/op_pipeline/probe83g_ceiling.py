#!/usr/bin/env python3
"""probe83g_ceiling.py -- is the solver's appetite a REQUIREMENT or an
opportunistic allocation that fits whatever ceiling it is given?

WHAT IS ALREADY MEASURED.  `probe83f_one_unit_trace.py` traced the
whole transcription of `c/regen_1859` -- 16 body lines, 32 ledger rows
of which 21 name an attached runtime callee -- and the transcription
itself never passed 50,352 kB resident.  The record came out TERM and
PROVED.  Yet the process's peak was 3,062,572 kB, just under the
3,221,225,472-byte address-space bound that probe was given, and the
peak did not appear at any traced step: it appears in the GATE, where
z3 solves.  `probe83b_memory.py`, given a 5 GB bound, measured
+4,883,500 kB on the same unit.  A peak that tracks the ceiling it is
given is the signature of an allocator taking what is available, not
of a computation that needs it.

THE TEST.  The SAME unit is walked in a forked child at several
address-space ceilings.  If the peak tracks the ceiling and the
verdict is the same every time, the appetite is opportunistic and a
ceiling is a legitimate bound.  If a lower ceiling changes the record
-- a different term state, a different verdict, or an abort -- then
the memory is required and the ceiling is not a bound but a change to
the corpus, which is not this task's to make.

THE VERDICT IS COMPARED, not just the peak: term state, proved, route,
outcome and the layer-5 text are read off each child's record and
checked against the others.  A bound that changes an answer is not a
bound.

WRITES:
  probe83g_ceiling.json

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
  probe83g_ceiling.py <shard path> <unit name> <MB> [<MB> ...]
"""

import json
import os
import resource
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SECONDS_CAP = 600


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


class OutOfTime(Exception):
    pass


def alarm(signum, frame):
    raise OutOfTime()


def one_ceiling(shard, name, megabytes):
    read_end, write_end = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(read_end)
        report = {"ceiling_mb": megabytes}
        started = time.time()
        try:
            cap = megabytes * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            signal.signal(signal.SIGALRM, alarm)
            signal.alarm(SECONDS_CAP)
            import canonical_form as CF
            import gate as G
            import reference as R
            import regate64_run as RG
            import term as T
            import term66_run as TR
            attached = RG.callee_units()
            readings = CF.runtime_answer_readings()
            reference = R.Reference(runtime_units=attached)
            maker = T.Term(
                reference=reference,
                runtime_routines=CF.runtime_routine_names(readings),
                runtime_units=attached,
                runtime_answers=readings)
            gate = G.Gate(reference=reference)
            document = json.load(open(os.path.join(HERE, shard)))
            unit = document["units"][name]
            record = TR.one_unit(maker, gate, name, unit)
            signal.alarm(0)
            report["outcome"] = "walked"
            report["term_state"] = record.get("term_state")
            report["proved"] = record.get("proved")
            report["gate_outcome"] = record.get("outcome")
            report["route"] = record.get("route")
            report["holes"] = len(record.get("holes") or [])
            text = record.get("layer5_normalized_text")
            report["layer5_text"] = text
        except MemoryError:
            report["outcome"] = "ABORT_MEMORY"
        except OutOfTime:
            report["outcome"] = "ABORT_TIME"
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
            killed = "killed_by_signal_%d" % os.WTERMSIG(status)
        return {"ceiling_mb": megabytes,
                "outcome": "CHILD_" + killed.upper()}
    return json.loads(text.decode())


def main(argv):
    shard = argv[1]
    name = argv[2]
    ceilings = [int(one) for one in argv[3:]]
    say("-- the unit")
    say("   %s in %s" % (name, shard))
    say("   ceilings to try, in MB: %s"
        % ", ".join(str(one) for one in ceilings))
    say("")
    say("   %10s %12s %10s %10s %8s %8s  %s"
        % ("ceiling MB", "peak kB", "seconds", "state", "proved",
           "holes", "outcome"))
    rows = []
    index = 0
    for megabytes in ceilings:
        index = index + 1
        row = one_ceiling(shard, name, megabytes)
        rows.append(row)
        say("   %10d %12s %10s %10s %8s %8s  %s"
            % (megabytes, row.get("peak_kb"), row.get("seconds"),
               row.get("term_state"), row.get("proved"),
               row.get("holes"), row.get("outcome")))
        say("[%d/%d] ceilings tried" % (index, len(ceilings)))

    answers = []
    for row in rows:
        if row.get("outcome") != "walked":
            continue
        answers.append((row.get("term_state"), row.get("proved"),
                        row.get("gate_outcome"), row.get("route"),
                        row.get("holes"), row.get("layer5_text")))
    same = len(set(answers)) <= 1
    say("")
    say("-- the verdict")
    say("   ceilings that walked to an answer %d of %d"
        % (len(answers), len(rows)))
    say("   every answer identical: %s" % same)
    if same and len(answers) > 1:
        say("   THE APPETITE IS OPPORTUNISTIC: the peak follows the "
            "ceiling and the record does not change, so a ceiling is "
            "a bound and not a change to the corpus.")
    else:
        say("   THE MEMORY IS REQUIRED, or the record changes with "
            "the ceiling: a ceiling would be a change to the corpus "
            "and is not this task's to make.")

    out = {
        "meta": {
            "produced_by": "probe83g_ceiling.py",
            "what_it_is": "one unit transcribed and gated at several "
                          "address-space ceilings, with the peak and "
                          "the whole record read back at each",
            "unit": name,
            "shard": shard,
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed",
        },
        "every_answer_identical": same,
        "answers_that_walked": len(answers),
        "rows": rows,
    }
    handle = open(os.path.join(HERE, "probe83g_ceiling.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    say("-- wrote probe83g_ceiling.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
