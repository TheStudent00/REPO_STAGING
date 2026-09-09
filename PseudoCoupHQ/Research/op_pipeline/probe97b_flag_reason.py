#!/usr/bin/env python3
"""probe97b_flag_reason.py -- WHICH token fired, and on WHAT text.

WHY IT EXISTS.  `probe97a_unit_cost.py` flagged 11 of the 24 proved
units of `op_units2_c_c0004` as MEMORY_REASON at a 1,536 MB per-unit
ceiling.  A flag is only as good as the thing it matched, and one of
the tokens in the first list -- `canceled` -- is also z3's own word for
a solver that ran out of WALL CLOCK, which is a legitimate UNDECIDED
verdict and not a runner memory limit at all.  So before any walk uses
that list, this probe prints, for one unit at a stated ceiling, the
exact token that fired and the exact field it fired on.

It also runs the same unit at a ladder of ceilings and prints the whole
record at each, so the question task 83 left open -- does the ceiling
change the ANSWER -- is asked again under the fork-per-unit
arrangement.

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
  probe97b_flag_reason.py <shard key> <unit name> <ceiling MB>...
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import probe97a_unit_cost as P97A                                # noqa: E402

CANDIDATE_TOKENS = ["MemoryError", "out of memory", "out-of-memory",
                    "canceled", "max. memory exceeded"]


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def which_tokens(record):
    text = json.dumps(record)
    found = []
    for token in CANDIDATE_TOKENS:
        if token in text:
            found.append(token)
    return found


def where(record, token):
    """the field paths whose value carries the token."""
    hits = []

    def walk(node, path):
        if isinstance(node, dict):
            for key in sorted(node):
                walk(node[key], path + "." + str(key))
            return
        if isinstance(node, list):
            index = 0
            for item in node:
                walk(item, path + "[%d]" % index)
                index = index + 1
            return
        if isinstance(node, str) and token in node:
            hits.append((path, node))

    walk(record, "")
    return hits


def main():
    key = sys.argv[1]
    name = sys.argv[2]
    ceilings = [int(text) for text in sys.argv[3:]]
    document = json.load(open(os.path.join(HERE, key)))
    unit = document["units"][name]
    say("-- the unit %s of %s" % (name, key))
    say("   body lines %d, ledger rows %d, runtime-callee rows %d"
        % (len(unit.get("body_verbatim") or []),
           len(unit.get("ledger") or []),
           P97A.runtime_rows_of_count(unit)))
    maker, gate, attached, readings = P97A.build()
    say("   setup done, attached callee units %d, readings %d"
        % (len(attached), len(readings)))
    seen = {}
    for ceiling in ceilings:
        outcome, record, wall, peak = P97A.one_unit_forked(
            maker, gate, name, unit, ceiling, 600)
        say("")
        say("======== ceiling %d MB ========" % ceiling)
        say("   outcome %s, wall %.2f s, child peak %d kB"
            % (outcome, wall, peak))
        if record is None:
            continue
        if "term_state" not in record:
            say("   raised: %s" % record.get("raised"))
            continue
        say("   term_state %s, verdict %s, proved %s, holes %d"
            % (record.get("term_state"), record.get("outcome"),
               record.get("proved"), len(record.get("holes") or [])))
        say("   reason: %s" % record.get("reason"))
        for token in which_tokens(record):
            say("   TOKEN %r fired on:" % token)
            for path, value in where(record, token)[:4]:
                say("      %s = %s" % (path, value[:220]))
        seen[ceiling] = json.dumps(record, sort_keys=True)
    say("")
    say("-- does the ceiling change the record?")
    texts = sorted(set(seen.values()))
    say("   ceilings that returned a record %d of %d"
        % (len(seen), len(ceilings)))
    say("   distinct records among them %d" % len(texts))


if __name__ == "__main__":
    main()
