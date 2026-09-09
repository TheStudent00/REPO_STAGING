#!/usr/bin/env python3
"""term66_bounded.py -- `term66_run.py`'s own run, under the hard
address-space bound the round's memory rule asks for, plus a mechanical
refusal if that bound ever touched an answer.

WHY THIS FILE EXISTS, measured rather than asserted.

`term66_run.py` checks its 6 GB bound with `resource.getrusage` AFTER
each shard.  Resumed inside the t83 sandbox the process was SIGKILLed
by the container's 8 GB cgroup in 11 seconds, inside a single shard,
so that check never ran (`t83_l2_sample.sh`, peak 8,391,436 kB, exit
-9).  The round's rule says the cap must be a NAMED abort; a cgroup
kill is not one.  This file puts the bound where the process cannot
step over it: `RLIMIT_AS`, set before the first shard.

THAT THE BOUND CHANGES NO ANSWER IS MEASURED, not assumed.
`probe83g_ceiling.py` transcribed and gated `c/regen_1859` -- the unit
the sample died in -- at 512, 1024, 2048, 3072 and 5120 MB.  The peak
followed the ceiling every time (464,828 / 971,144 / 2,031,888 /
3,068,796 / 5,178,796 kB) and the record was identical at all five:
TERM, proved, no holes, the same layer-5 text.  The appetite is the
allocator taking what is there, not a computation that needs it.  The
`--check` mode below re-transcribes shards already in `term66_store`
under the bound and compares them to what is stored, so the claim is
tested against this corpus's own records and not only against one
unit.

THE REFUSAL.  A `MemoryError` raised inside `Term.transcribe`'s row
loop is caught there as a hole, and a hole is a written reason on a
record -- which means a bound that ever fired could quietly change a
unit's state.  So after the walk this file SCANS every record it
wrote for any mention of `MemoryError`, in a hole, in a no-term
reason or in a layer-5 refusal, and REFUSES ITS OWN OUTPUT if it finds
one.

WHAT IS REUSED RATHER THAN COPIED.  `term66_run.run` is the walk and
is called, not re-typed.  `term66_run.py` is not edited: this file
only sets the module's STORE and STATE constants in `--check` mode, so
a check writes into scratch and never into the corpus.

WRITES (default mode):
  term66_store/*.json, term66_state.json   -- through term66_run.run
  term66_bounded_scan.json                 -- the refusal scan

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
  term66_bounded.py <ceiling MB> <budget seconds>
  term66_bounded.py <ceiling MB> <budget seconds> --check <shard key>...
"""

import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import term66_run as TR                                          # noqa: E402

SCRATCH_STORE = "/work/t83_check_store"
SCRATCH_STATE = "/work/t83_check_state.json"


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def set_bound(megabytes):
    cap = megabytes * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    say("-- THE BOUND")
    say("   RLIMIT_AS %d bytes (%d MB), set before the first shard."
        % (cap, megabytes))
    say("   An allocation past it raises MemoryError; every record "
        "written is then scanned for it and the output is refused if "
        "it appears.")
    say("   term66_run.py's own between-shard check at 6 GB stays in "
        "force underneath this one.")


def scan_store(store):
    """every record in `store` searched for a memory failure that
    became a written reason.  Returns the offending units."""
    found = []
    records = 0
    for path in sorted(glob.glob(os.path.join(store, "*.json"))):
        document = json.load(open(path))
        for name in sorted(document.get("units", {})):
            record = document["units"][name]
            records = records + 1
            text = json.dumps(record)
            if "MemoryError" not in text:
                continue
            found.append({"shard": document.get("shard"),
                          "unit": name})
    return records, found


def check(shard_keys):
    """re-transcribe shards ALREADY in term66_store, under the bound,
    into scratch, and compare record for record."""
    every = TR.shards()
    keys = []
    for path in every:
        keys.append(os.path.relpath(path, HERE))
    pretend_done = []
    for key in keys:
        if key in shard_keys:
            continue
        pretend_done.append(key)
    if not os.path.isdir(SCRATCH_STORE):
        os.makedirs(SCRATCH_STORE)
    handle = open(SCRATCH_STATE, "w")
    json.dump({"done": sorted(pretend_done), "started": 0}, handle)
    handle.close()
    TR.STORE = SCRATCH_STORE
    TR.STATE = SCRATCH_STATE
    say("-- the check: %d shard(s) re-transcribed under the bound"
        % len(shard_keys))
    TR.run(100000)
    same = 0
    differ = []
    units = 0
    for key in shard_keys:
        name = key.replace("/", "__")
        fresh = json.load(open(os.path.join(SCRATCH_STORE, name)))
        stored = json.load(open(os.path.join(HERE, "term66_store",
                                             name)))
        for unit in sorted(set(fresh["units"]) | set(stored["units"])):
            units = units + 1
            if fresh["units"].get(unit) == stored["units"].get(unit):
                same = same + 1
                continue
            differ.append("%s/%s" % (key, unit))
    say("")
    say("-- ZERO REGRESSION, in the ruled sense: record for record")
    say("   shards compared %d" % len(shard_keys))
    say("   records compared %d" % units)
    say("   records identical %d" % same)
    say("   records that differ %d" % len(differ))
    for one in differ[:20]:
        say("       %s" % one)
    if differ:
        say("REFUSED OWN OUTPUT: the bound changed a record, so it is "
            "not a bound")
        return 1
    say("   the bound changed nothing on this corpus's own records")
    return 0


def main(argv):
    megabytes = int(argv[1])
    budget = int(argv[2])
    set_bound(megabytes)
    if len(argv) > 3 and argv[3] == "--check":
        return check(argv[4:])
    say("-- the walk, resuming from term66_state.json")
    finished = TR.run(budget)
    records, found = scan_store(os.path.join(HERE, "term66_store"))
    out = {
        "meta": {
            "produced_by": "term66_bounded.py",
            "bound": "RLIMIT_AS %d MB" % megabytes,
            "what_the_scan_is": "every record written into "
                                "term66_store searched for a memory "
                                "failure that became a written reason "
                                "-- a hole, a no-term reason or a "
                                "layer-5 refusal",
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed",
        },
        "records_scanned": records,
        "records_naming_a_memory_failure": len(found),
        "offending": found[:200],
        "walk_finished": finished,
    }
    handle = open(os.path.join(HERE, "term66_bounded_scan.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    say("")
    say("-- the refusal scan")
    say("   records scanned %d" % records)
    say("   records naming a memory failure %d" % len(found))
    if found:
        say("REFUSED OWN OUTPUT: the bound fired and became a written "
            "reason on %d record(s); the first is %s"
            % (len(found), found[0]))
        return 1
    say("   the bound never fired")
    if not finished:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
