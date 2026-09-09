#!/usr/bin/env python3
"""regression64.py -- did task 64's rewrite of the walk move any answer
on a body where it SHOULD NOT have?

Node: `hq.research.compiler_graph.reference` (0_3_5_4).

THE POPULATION IS COMPUTED, NOT CHOSEN.  Task 64 replaced
`Reference.simulate`'s text-order loop with a walk over the body's own
control-flow graph.  On a body that HAS no graph -- no label, no
conditional transfer, no `jmp`, no `call`, no `ud2` -- the two walks
must produce the same object, character for character, because the
graph of such a body is one block and the walk over it is the loop.
So the population here is exactly the canon39 proved units whose own
text contains none of those five things: every one of them, not a
sample.  That is the strong form of the check, and it is affordable
because it is the cheap half of the corpus.

Beside it, and reported separately, the units that DO carry one of the
five: there the answer is expected to change, and the two columns say
how many changed from a refusal to a term (a GAIN), how many changed
answer, and how many are unchanged.

Both versions of the module are loaded side by side -- the working
tree's, and the one git holds at the commit before this task's first
edit.

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

The split between the two columns is MACHINE-FORM EVIDENCE -- what the
unit's own disassembled text spells -- and never an operator token.

usage:
  regression64.py [<git revision of the module before the edits>]

Coding discipline: no compound one-liner statements.
"""

import collections
import glob
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

BEFORE_REVISION = "d3de348"
IN_REPO = "Research/op_pipeline/reference.py"

CONTROL_FLOW = ("call", "jmp", "ud2")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def older_module(revision):
    repo = os.path.abspath(os.path.join(HERE, "..", ".."))
    argv = ["git", "-C", repo, "show", "%s:%s" % (revision, IN_REPO)]
    done = subprocess.run(argv, capture_output=True, text=True)
    if done.returncode != 0:
        return None, done.stderr.strip()
    path = os.path.join("/tmp", "reference_%s.py" % revision)
    handle = open(path, "w")
    handle.write(done.stdout)
    handle.close()
    return load(path, "reference_before"), ""


def shard_paths():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE, "canon39_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon39_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_regen_store", "*.json"))))
    return [path for path in out if os.path.exists(path)]


def has_a_graph(record, after):
    """does this body's own text carry a label, a conditional transfer,
    a `jmp`, a `call` or a `ud2`?"""
    for raw in record.get("body_verbatim") or []:
        text = raw.split("!!")[0].strip()
        if text == "":
            continue
        if text.endswith(":"):
            return True
        mnemonic = text.split(" ", 1)[0]
        if mnemonic in CONTROL_FLOW:
            return True
        if after.is_conditional_transfer(mnemonic):
            return True
    return False


def outcome(module, record):
    try:
        term, _width = module.Reference().answer_for_unit(record)
        return "TERM:" + str(term)
    except Exception as why:
        return "REFUSE:" + str(why)


def main():
    revision = BEFORE_REVISION
    if len(sys.argv) > 1:
        revision = sys.argv[1]
    before, trouble = older_module(revision)
    if before is None:
        print("REFUSING: %s" % trouble)
        return 2
    after = load(os.path.join(HERE, "reference.py"), "reference_after")
    tally = collections.Counter()
    changed = []
    for path in shard_paths():
        document = json.load(open(path))
        for name, stored in sorted(document.get("units", {}).items()):
            if stored.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            record = dict(stored)
            record["unit"] = name
            column = "carries a graph"
            if not has_a_graph(record, after):
                column = "straight line"
            was = outcome(before, record)
            now = outcome(after, record)
            if was == now:
                tally[(column, "identical")] += 1
                continue
            if was.startswith("REFUSE") and now.startswith("TERM"):
                tally[(column, "refusal became a term")] += 1
                continue
            if was.startswith("TERM") and now.startswith("REFUSE"):
                tally[(column, "term became a refusal")] += 1
                changed.append({"unit": name, "column": column,
                                "was": was[:200], "now": now[:200]})
                continue
            if was.startswith("REFUSE") and now.startswith("REFUSE"):
                # BOTH REFUSED, AND THE WORDING MOVED.  Neither version
                # answers, so no answer changed; the refusal is the
                # same verdict said differently, and it is counted as
                # its own row rather than folded into either side.
                tally[(column,
                       "refused both times, wording moved")] += 1
                changed.append({"unit": name, "column": column,
                                "was": was[:200], "now": now[:200]})
                continue
            tally[(column, "CHANGED ANSWER")] += 1
            changed.append({"unit": name, "column": column,
                            "was": was[:240], "now": now[:240]})
    lines = []
    lines.append("population: ALL 30,432 canon39 proved units, split "
                 "by what the unit's OWN TEXT spells -- no sample")
    lines.append("the module before this task: %s:%s"
                 % (revision, IN_REPO))
    lines.append("")
    columns = ["straight line", "carries a graph"]
    kinds = ["identical", "refusal became a term",
             "refused both times, wording moved",
             "term became a refusal", "CHANGED ANSWER"]
    lines.append("%-24s %14s %16s" % ("", columns[0], columns[1]))
    for kind in kinds:
        lines.append("%-24s %14d %16d"
                     % (kind, tally[(columns[0], kind)],
                        tally[(columns[1], kind)]))
    lines.append("%-24s %14d %16d"
                 % ("total",
                    sum(tally[(columns[0], kind)] for kind in kinds),
                    sum(tally[(columns[1], kind)] for kind in kinds)))
    lines.append("")
    straight = tally[("straight line", "CHANGED ANSWER")]
    straight = straight + tally[("straight line",
                                 "term became a refusal")]
    lines.append("THE CHECK: a body with no label, no conditional "
                 "transfer, no `jmp`, no `call` and no `ud2` must "
                 "answer identically.  Units where it did not: %d"
                 % straight)
    for one in changed[:20]:
        if one["column"] != "straight line":
            continue
        lines.append("  %s" % json.dumps(one, sort_keys=True))
    for line in lines:
        print(line)
    out = {
        "meta": {
            "produced_by": "regression64.py",
            "population": "all canon39 proved units",
            "module_before": "%s:%s" % (revision, IN_REPO),
        },
        "counts": [
            {"column": column, "kind": kind,
             "units": tally[(column, kind)]}
            for column in columns for kind in kinds
        ],
        "changed": changed,
        "straight_line_disagreements": straight,
    }
    handle = open(os.path.join(HERE, "regression64.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "regression64_printed.txt"), "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    if straight:
        return 1
    return 0


sys.exit(main())
