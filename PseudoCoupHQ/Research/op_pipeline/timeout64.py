#!/usr/bin/env python3
"""timeout64.py -- the units whose proof was lost to the SOLVER'S OWN
TIME LIMIT rather than to a counterexample, put to z3 again with a
longer limit.

Node: `hq.research.compiler_graph.gate` (0_3_5_5), sub-node
`zero_regression`.

WHY THIS IS A SEPARATE FILE AND A SEPARATE NUMBER.  The gate CORE fixes
the limit at 3,000 ms and records it on every verdict, precisely so an
UNDECIDED can be re-read later.  `regate64_store` keeps its 3,000 ms
verdicts; this file re-reads them and reports beside the run.  A longer
limit is not folded into the round's counts, because the round's counts
must be the counts one fixed limit produced.

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

The candidate set here is the units whose OWN RECORDED VERDICT says the
solver ran out of time -- machine-form evidence, never a token.

Coding discipline: no compound one-liner statements.

usage:
  timeout64.py [<limit in milliseconds> ...]
"""

import collections
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402

LINES = []


def say(text=""):
    LINES.append(text)
    print(text)
    sys.stdout.flush()


def state_of(record):
    if record.get("term_state") == "NO_TERM":
        return "no term"
    if record.get("proved"):
        return "proved"
    if record.get("outcome") == "DISPROVED":
        return "disproved"
    return "undecided"


def read(folder):
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, folder,
                                              "*.json"))):
        out.update(json.load(open(path))["units"])
    return out


def main():
    limits = [30000]
    if len(sys.argv) > 1:
        limits = [int(one) for one in sys.argv[1:]]
    old = read("term61_store")
    new = read("regate64_store")
    lost = []
    for name in sorted(new):
        if name not in old:
            continue
        if state_of(old[name]) != "proved":
            continue
        if state_of(new[name]) != "undecided":
            continue
        reason = new[name].get("reason") or ""
        if "did not answer inside its" not in reason:
            continue
        lost.append(name)
    say("population: the units task 61 proved and this round's re-gate "
        "left UNDECIDED because the solver ran out of time -- %d of "
        "the 30,432." % len(lost))
    for name in lost:
        say("   %-16s %s" % (name, (new[name].get("reason") or "")[:90]))
    say()
    callees = {}
    document = json.load(open(os.path.join(
        HERE, "canon39_callee_units.json")))
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain") or key.split("/", 1)[0]
        routine = unit.get("callee") or key.split("/", 1)[-1]
        callees.setdefault(toolchain, {})
        callees[toolchain][routine] = unit
    canon = {}
    paths = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        paths.append(os.path.join(HERE, "canon39_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon39_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name, record in document.get("units", {}).items():
            if name in lost:
                canon[name] = record
    answers = {}
    for limit in limits:
        reference = R.Reference(runtime_units=callees)
        maker = T.Term(reference=reference,
                       runtime_routines=CF.runtime_routine_names(),
                       runtime_units=callees)
        gate = G.Gate(reference=reference, solver_timeout_ms=limit)
        found = {}
        started = time.time()
        for name in lost:
            record = dict(canon[name])
            record["unit"] = name
            walked = maker.transcribe(record)
            verdict = gate.prove_term_against_ship(walked.out_term,
                                                   record)
            if not verdict.proved():
                second = gate.prove_term_against_text(walked.out_term,
                                                      record)
                if second.proved():
                    verdict = second
            found[name] = verdict.outcome
        spent = time.time() - started
        answers[limit] = found
        say("at a %d ms limit (%.0f s of wall clock over the %d): %s"
            % (limit, spent, len(lost),
               dict(collections.Counter(found.values()))))
        for name in lost:
            say("   %-16s %s" % (name, found[name]))
        say()
    handle = open(os.path.join(HERE, "timeout64.json"), "w")
    json.dump({
        "meta": {
            "produced_by": "timeout64.py",
            "population": "canon39 units task 61 proved and task 64's "
                          "re-gate left undecided on the solver's own "
                          "time limit",
            "the_run_keeps_its_3000_ms_verdicts": True,
        },
        "units": lost,
        "outcomes": [
            {"limit_ms": limit,
             "verdicts": [{"unit": name, "outcome": found[name]}
                          for name in lost]}
            for limit, found in sorted(answers.items())
        ],
    }, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "timeout64_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    return 0


sys.exit(main())
