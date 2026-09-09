#!/usr/bin/env python3
"""probe83b_memory.py -- WHERE the canon40 transcription's memory goes,
measured unit by unit, after the sample lane was killed by the
container's 8 GB cgroup at shard 11 of 332.

WHAT HAPPENED, and why this probe exists.  The part-run of 2026-09-03
walked ten inputs on the host and peaked at 816,136 kB
(`term66_run.log`).  Resumed inside the t83 sandbox on 2026-09-04, the
same program reached 8,391,436 kB and was SIGKILLed in 11 seconds
without finishing one further shard.  `term66_run.py` checks its bound
BETWEEN shards, so a unit that runs away inside a shard is never
caught by it.  This probe puts the bound where the runaway is: a hard
address-space limit, so the allocation itself fails and the UNIT that
asked for it is named.

THE BOUND, stated: RLIMIT_AS of 5 GB, set before any unit is walked.
An allocation past it raises MemoryError inside the unit's own walk,
which is caught, and the abort is printed BY NAME as ABORT_MEMORY with
the unit that asked.  Resident size is read from
`resource.getrusage(RUSAGE_SELF).ru_maxrss` after every unit and the
per-unit growth is printed whenever it passes 50 MB.

NOTHING IS WRITTEN INTO THE STORE by this probe -- it is a
measurement, not a transcription, so a partial or defective walk here
cannot enter the corpus.

WHAT IS REUSED RATHER THAN COPIED.  `term66_run.one_unit` is the walk
and is called, not re-typed, so what is measured is the real thing.

WRITES:
  probe83b_memory_printed.txt   (via the lane log; this file prints)

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
  probe83b_memory.py <shard path> [how many units]
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import regate64_run as RG                                        # noqa: E402
import term as T                                                 # noqa: E402
import term66_run as TR                                          # noqa: E402

ADDRESS_SPACE_CAP = 5 * 1024 * 1024 * 1024
PROVED = "WRAPPED_TEXT_PROVED"


def rss_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main(argv):
    shard = argv[1]
    limit = 100000
    if len(argv) > 2:
        limit = int(argv[2])

    say("-- the bound")
    say("   RLIMIT_AS set to %d bytes (5 GB); an allocation past it "
        "raises MemoryError and the unit is named" % ADDRESS_SPACE_CAP)
    resource.setrlimit(resource.RLIMIT_AS,
                       (ADDRESS_SPACE_CAP, ADDRESS_SPACE_CAP))

    say("-- the setup, the same objects term66_run.run builds")
    before = rss_kb()
    say("   resident before setup %d kB" % before)
    attached = RG.callee_units()
    say("   attached callee units %d, resident %d kB"
        % (len(attached), rss_kb()))
    readings = CF.runtime_answer_readings()
    say("   runtime answer readings %d, resident %d kB"
        % (len(readings), rss_kb()))
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(readings),
                   runtime_units=attached,
                   runtime_answers=readings)
    gate = G.Gate(reference=reference)
    say("   resident after setup %d kB" % rss_kb())

    say("-- the shard")
    say("   %s" % shard)
    document = json.load(open(os.path.join(HERE, shard)))
    say("   units in the shard %d, resident %d kB"
        % (len(document.get("units", {})), rss_kb()))

    walked = 0
    last = rss_kb()
    biggest = ("", 0)
    for name in sorted(document.get("units", {})):
        unit = document["units"][name]
        if unit.get("outcome") != PROVED:
            continue
        if walked >= limit:
            break
        try:
            TR.one_unit(maker, gate, name, unit)
        except MemoryError:
            say("ABORT_MEMORY: the 5 GB address-space bound was "
                "reached inside the walk of unit %s (unit %d of this "
                "shard); resident %d kB"
                % (name, walked + 1, rss_kb()))
            return 5
        walked = walked + 1
        now = rss_kb()
        grew = now - last
        if grew > biggest[1]:
            biggest = (name, grew)
        if grew > 50 * 1024:
            say("   [%4d] %-24s resident %d kB (+%d kB on this unit)"
                % (walked, name, now, grew))
        if walked % 25 == 0:
            say("   [%4d] %-24s resident %d kB" % (walked, name, now))
        last = now

    say("-- the result")
    say("   units walked %d" % walked)
    say("   peak resident %d kB" % rss_kb())
    say("   largest single-unit growth: %s +%d kB"
        % (biggest[0], biggest[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
