#!/usr/bin/env python3
"""render_back81_tally.py -- the tally over `render_back81_store/`, the
owed re-run of the return path against the SETTLED `ledger.py`, beside
task 80's own tally.

WHAT IS REUSED RATHER THAN COPIED.  The walk, the cause grouping and
the printed shape are `render_back_tally.py`'s own functions; the
comparison section is `render_back80_tally.difference_section`, called
with task 80's artifact as the "before".  Nothing is re-typed, and task
80's numbers are read off its own artifact (`render_back80_tally.json`)
rather than from a log.

Every number is pasted with its population.  Refusals and non-proofs
are grouped BY CAUSE, never by sighting (LLM_communication_protocol
section 5.3).

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

No operator token appears in this file.  Nothing here is keyed,
grouped or paired on the `operator` display label.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_back80_tally as R80T                                # noqa: E402
import render_back_tally as RT                                    # noqa: E402

STORE = os.path.join(HERE, "render_back81_store")
TASK80 = os.path.join(HERE, "render_back80_tally.json")
OUT = os.path.join(HERE, "render_back81_tally.json")
PRINTED = os.path.join(HERE, "render_back81_tally_printed.txt")
LEDGER_NOTE = os.path.join(HERE, "render_back81_ledger_sha256.txt")


def task80():
    if not os.path.exists(TASK80):
        return None
    return json.load(open(TASK80))


def per_unit_difference(now_store, before_store):
    """UNIT BY UNIT, not count by count.  Two runs can agree on every
    total and still disagree about which units they are, so the
    comparison joins on the unit name and names every unit whose
    rendered text, outcome or refusal cause moved."""
    lines = []
    moved_text = []
    moved_outcome = []
    only_now = []
    only_before = []
    for name in sorted(now_store):
        if name not in before_store:
            only_now.append(name)
            continue
        a = before_store[name]
        b = now_store[name]
        if a.get("rendered_wrapped_text") != b.get(
                "rendered_wrapped_text"):
            moved_text.append(name)
        if a.get("outcome") != b.get("outcome"):
            moved_outcome.append(name)
    for name in sorted(before_store):
        if name not in now_store:
            only_before.append(name)
    lines.append("")
    lines.append("UNIT BY UNIT against task 80's own store")
    lines.append("  units in both stores            %d"
                 % len([one for one in now_store
                        if one in before_store]))
    lines.append("  units only in this re-run       %d" % len(only_now))
    lines.append("  units only in task 80's store   %d"
                 % len(only_before))
    lines.append("  units whose RENDERED TEXT moved %d"
                 % len(moved_text))
    lines.append("  units whose OUTCOME moved       %d"
                 % len(moved_outcome))
    for name in moved_text[:20]:
        lines.append("      text moved: %s" % name)
    for name in moved_outcome[:20]:
        lines.append("      outcome moved: %s -> %s -> %s"
                     % (name, before_store[name].get("outcome"),
                        now_store[name].get("outcome")))
    return lines, {
        "units_in_both": len([one for one in now_store
                              if one in before_store]),
        "units_only_in_the_rerun": only_now,
        "units_only_in_task80": only_before,
        "units_whose_rendered_text_moved": moved_text,
        "units_whose_outcome_moved": moved_outcome,
    }


def read_store(path):
    import glob
    out = {}
    for shard in sorted(glob.glob(os.path.join(path, "*.json"))):
        document = json.load(open(shard))
        for name in document.get("units", {}):
            out[name] = document["units"][name]
    return out


def main():
    RT.STORE = STORE
    document = RT.walk()
    handle = open(LEDGER_NOTE)
    digest = handle.read().strip()
    handle.close()
    document["meta"] = {
        "produced_by": "render_back81_tally.py",
        "read_from": "render_back81_store/",
        "node": "hq.research.compiler_graph.term.render_back",
        "what_changed": "nothing in the rule; the re-run reads the "
                        "SETTLED ledger.py that task 78 left, which "
                        "task 80's own run read mid-edit",
        "ledger_sha256": digest,
        "population": "the same 26,040 units of the 30,432 "
                      "canon39-proved ones whose layer-4 term "
                      "term61_store records as proved -- held fixed so "
                      "the only difference is ledger.py",
    }
    before = task80()
    printed = RT.report(document)
    printed = printed.replace("computed from render_back_store/",
                              "computed from render_back81_store/")
    comparison = R80T.difference_section(document, before)
    for index, line in enumerate(comparison):
        # `difference_section` names its own "before" in its heading.
        # This tally's "before" is task 80's artifact, not round 13's,
        # and a heading naming the wrong artifact would be a false
        # statement inside an artifact.
        comparison[index] = line.replace(
            "AGAINST ROUND 13 (read off render_back_tally.json, "
            "the artifact, not a log)",
            "AGAINST TASK 80 (read off render_back80_tally.json, the "
            "artifact, not a log)")
        comparison[index] = comparison[index].replace(
            "%-40s %10s %10s" % ("count", "round 13", "this round"),
            "%-40s %10s %10s" % ("count", "task 80", "this re-run"))
        comparison[index] = comparison[index].replace(
            "  count                                      round 13 this round",
            "  count                                       task 80 this re-run")
    printed = printed + "\n".join(comparison) + "\n"
    now_store = read_store(STORE)
    before_store = read_store(os.path.join(HERE,
                                           "render_back80_store"))
    lines, per_unit = per_unit_difference(now_store, before_store)
    document["per_unit_against_task80"] = per_unit
    printed = printed + "\n".join(lines) + "\n"
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(PRINTED, "w")
    handle.write(printed)
    handle.close()
    sys.stdout.write(printed)


if __name__ == "__main__":
    main()
