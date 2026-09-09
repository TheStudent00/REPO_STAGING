#!/usr/bin/env python3
"""render_back80_tally.py -- the tally over POPULATION TWO after the
conditional template, and the difference from round 13's own tally.

WHAT IS REUSED RATHER THAN COPIED.  The walk, the cause grouping and
the printed shape are `render_back_tally.py`'s own functions, called
with this round's store; only the store path and the two comparison
sections below are new.  Round 13's numbers are READ OFF ITS OWN
ARTIFACT (`render_back_tally.json`), never re-typed from a log.

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

import render_back_tally as RT                                   # noqa: E402

STORE = os.path.join(HERE, "render_back80_store")
ROUND13 = os.path.join(HERE, "render_back_tally.json")
OUT = os.path.join(HERE, "render_back80_tally.json")
PRINTED = os.path.join(HERE, "render_back80_tally_printed.txt")


def round13():
    if not os.path.exists(ROUND13):
        return None
    return json.load(open(ROUND13))


def cause_map(document, key):
    out = {}
    for entry in document[key]:
        out[entry["cause"]] = entry["units"]
    return out


def difference_section(now, before):
    """this round's counts and causes beside round 13's own artifact.

    A cause that is gone is named; a cause that is new is named; a
    cause that changed size is named with both sizes.  Nothing is
    summarised away."""
    lines = []
    lines.append("")
    lines.append("AGAINST ROUND 13 (read off render_back_tally.json, "
                 "the artifact, not a log)")
    lines.append("")
    if before is None:
        lines.append("  round 13's tally is not on disk beside this "
                     "one, so no difference is computed")
        return lines
    lines.append("  %-40s %10s %10s" % ("count", "round 13",
                                        "this round"))
    keys = ["units_with_a_proved_term", "rendered", "assembled_by_as",
            "round_tripped_through_objdump", "proved_on_ship",
            "character_identical_to_layer_3",
            "distinct_rendered_texts",
            "distinct_layer_3_texts_over_the_same_units"]
    for key in keys:
        lines.append("  %-40s %10s %10s"
                     % (key, before["counts"].get(key),
                        now["counts"].get(key)))
    lines.append("")
    was = cause_map(before, "refusal_causes")
    is_now = cause_map(now, "refusal_causes")
    lines.append("  refusal causes that are GONE:")
    gone = []
    for cause in sorted(was):
        if cause in is_now:
            continue
        gone.append(cause)
    if not gone:
        lines.append("    none")
    for cause in gone:
        lines.append("    %6d -> 0   %s" % (was[cause], cause))
    lines.append("")
    lines.append("  refusal causes that are NEW:")
    fresh = []
    for cause in sorted(is_now):
        if cause in was:
            continue
        fresh.append(cause)
    if not fresh:
        lines.append("    none")
    for cause in sorted(fresh, key=lambda one: -is_now[one]):
        lines.append("    0 -> %6d   %s" % (is_now[cause], cause))
    lines.append("")
    lines.append("  refusal causes that CHANGED SIZE:")
    changed = []
    for cause in sorted(is_now):
        if cause not in was:
            continue
        if was[cause] == is_now[cause]:
            continue
        changed.append(cause)
    if not changed:
        lines.append("    none")
    for cause in changed:
        lines.append("    %6d -> %6d   %s"
                     % (was[cause], is_now[cause], cause))
    return lines


def main():
    RT.STORE = STORE
    document = RT.walk()
    document["meta"] = {
        "produced_by": "render_back80_tally.py",
        "read_from": "render_back80_store/",
        "node": "hq.research.compiler_graph.term.render_back",
        "what_changed": "the one fixed rule gained the conditional "
                        "template read off the corpus's own ship "
                        "bodies",
    }
    before = round13()
    printed = RT.report(document)
    # `render_back_tally.report` names its own store in its heading.
    # This tally read a different one, and a heading that named the
    # wrong file would be a false statement in an artifact.
    printed = printed.replace("computed from render_back_store/",
                              "computed from render_back80_store/")
    printed = printed + "\n".join(difference_section(document,
                                                     before)) + "\n"
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(PRINTED, "w")
    handle.write(printed)
    handle.close()
    sys.stdout.write(printed)


if __name__ == "__main__":
    main()
