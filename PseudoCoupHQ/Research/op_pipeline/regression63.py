#!/usr/bin/env python3
"""regression63.py -- did task 63's edits to `reference.py` move any
answer that already existed?

Node: `hq.research.compiler_graph.reference.opcode_table`

WHY THIS EXISTS.  Task 63 edited `reference.py`: nine arch opcodes
added, and segment-relative memory operands (`%fs:0x28`) read as
memory cells.  Task 64 re-gates the whole population; this program is
the cheap check that task 63 did not move anything under task 64's
feet.  It is a SAMPLE, and it says so: sampled observation refutes, it
does not prove (the evidence doctrine, AgentMemory).

HOW.  Both versions of the module are loaded side by side -- the one
in the working tree, and the one git holds at the commit before this
task's first edit -- and each is asked for the answer term of the
same canon39 unit.  Three outcomes are counted:

  identical      the two agree, character for character
  refusal->term  the old one refused and the new one answers: a GAIN
  changed        the two answer differently: a REGRESSION, listed

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

usage:
  regression63.py [<git revision of the module before the edits>]

Coding discipline: no compound one-liner statements.
"""

import glob
import importlib.util
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

BEFORE_REVISION = "7a560e5"
IN_REPO = "Research/op_pipeline/reference.py"
SAMPLE = 3000
SEED = 63


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def older_module(revision):
    repo = os.path.abspath(os.path.join(HERE, "..", ".."))
    argv = ["git", "-C", repo, "show",
            "%s:%s" % (revision, IN_REPO)]
    done = subprocess.run(argv, capture_output=True, text=True)
    if done.returncode != 0:
        return None, done.stderr.strip()
    path = os.path.join("/tmp", "reference_%s.py" % revision)
    open(path, "w").write(done.stdout)
    return load(path, "reference_before"), ""


def sampled_units():
    stores = []
    stores.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_regen_store", "*.json"))))
    stores.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_wrapped_*.json"))))
    random.seed(SEED)
    random.shuffle(stores)
    out = []
    for path in stores[:40]:
        doc = json.load(open(path))
        for name, record in doc["units"].items():
            if record.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            out.append(record)
    random.shuffle(out)
    return out[:SAMPLE]


def outcome(module, unit):
    try:
        term, width = module.Reference().answer_for_unit(unit)
        return "TERM:" + str(term)
    except Exception as why:
        return "REFUSE:" + str(why)


def main():
    revision = BEFORE_REVISION
    if len(sys.argv) > 1:
        revision = sys.argv[1]
    before, trouble = older_module(revision)
    lines = []
    if before is None:
        print("REFUSING: %s" % trouble)
        return 2
    after = load(os.path.join(HERE, "reference.py"), "reference_after")
    units = sampled_units()
    identical = 0
    gained = []
    changed = []
    for unit in units:
        old = outcome(before, unit)
        new = outcome(after, unit)
        if old == new:
            identical = identical + 1
            continue
        if old.startswith("REFUSE") and new.startswith("TERM"):
            gained.append({"unit": unit.get("unit"),
                           "was": old[:200]})
            continue
        changed.append({"unit": unit.get("unit"),
                        "was": old[:300],
                        "now": new[:300]})
    lines.append("population: canon39's proved units; SAMPLE of %d "
                 "drawn from 40 stores, seed %d" % (len(units), SEED))
    lines.append("the module before this task: %s:%s"
                 % (revision, IN_REPO))
    lines.append("identical outcome:            %d" % identical)
    lines.append("refusal -> term (a gain):     %d" % len(gained))
    lines.append("CHANGED ANSWER (a regression): %d" % len(changed))
    for one in changed[:20]:
        lines.append("  %s" % json.dumps(one, sort_keys=True))
    for line in lines:
        print(line)
    out = {
        "meta": {
            "produced_by": "regression63.py",
            "population": "canon39's proved units",
            "sample": len(units),
            "seed": SEED,
            "module_before": "%s:%s" % (revision, IN_REPO),
        },
        "identical": identical,
        "refusal_became_a_term": gained,
        "changed_answer": changed,
    }
    json.dump(out, open(os.path.join(HERE, "regression63.json"), "w"),
              indent=1, sort_keys=True)
    open(os.path.join(HERE, "regression63_printed.txt"),
         "w").write("\n".join(lines) + "\n")
    if changed:
        return 1
    return 0


sys.exit(main())
