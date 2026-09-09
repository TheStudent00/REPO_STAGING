#!/usr/bin/env python3
"""acceptance79.py -- THE ACCEPTANCE TEST for task 79: is the layer-5
text a function of the unit?

WHAT IS COMPARED.  Three walks of the corrected rule, each made by its
own process (`normalize79_walk.py`):

    walk1   forward     units in name order
    walk2   forward     the same order, a second fresh process
    walk3   shuffled    the shards and the units inside them in a
                        deliberately shuffled construction order

THE TEST PASSES when all three print the SAME text for every one of
the 26,594 units whose term the round-13 gate proved.  Any unit whose
three texts are not all equal is named here with its cause and its
count -- never dropped.

WHAT IT ALSO REPORTS: the distinct-text collapse before and after.
BEFORE is the 1,267 distinct texts `term65_store` holds for the same
26,594 units (log_169 section 1.5), which is ONE walk's count under the
uncorrected rule and not a property of the corpus -- log_169 section
5.3 measured a second walk producing 1,294.  AFTER is the distinct
count of the corrected rule, which is the same in all three walks or
the test has already failed.

WRITES:
  acceptance79.json
  acceptance79_printed.txt

ONE PROCESS.

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
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def walk(label):
    path = os.path.join(HERE, "normalize79_walk_%s.json" % label)
    return json.load(open(path))


def stored_texts():
    """unit -> the layer-5 text `term65_run.py` wrote under the
    UNCORRECTED rule, for the units it proved."""
    out = {}
    pattern = os.path.join(HERE, "term65_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            record = document["units"][name]
            if not record.get("proved"):
                continue
            text = record.get("layer5_normalized_text")
            if text is None:
                continue
            out[name] = text
    return out


def main():
    labels = ["walk1", "walk2", "walk3"]
    suffix = ""
    if "--labels" in sys.argv:
        labels = sys.argv[sys.argv.index("--labels") + 1].split(",")
    if "--suffix" in sys.argv:
        suffix = sys.argv[sys.argv.index("--suffix") + 1]
    one = walk(labels[0])
    two = walk(labels[1])
    three = walk(labels[2])
    was = stored_texts()

    first = one["texts"]
    second = two["texts"]
    third = three["texts"]

    log("-- THE POPULATION")
    log("   units with a proved term and a stored layer-5 text %d"
        % len(was))
    log("   units walk1 printed  %d  (refused %d)"
        % (len(first), one["units_refused"]))
    log("   units walk2 printed  %d  (refused %d)"
        % (len(second), two["units_refused"]))
    log("   units walk3 printed  %d  (refused %d)"
        % (len(third), three["units_refused"]))

    everywhere = set(first) & set(second) & set(third)
    stable = []
    unstable = []
    for name in sorted(everywhere):
        if first[name] == second[name] and first[name] == third[name]:
            stable.append(name)
        else:
            unstable.append(name)

    missing = sorted(set(was) - everywhere)

    log("")
    log("-- THE ACCEPTANCE FIGURE")
    log("   units printed by all three walks                 %d"
        % len(everywhere))
    log("   units whose three texts are IDENTICAL            %d of %d"
        % (len(stable), len(was)))
    log("   units whose texts differ between walks           %d"
        % len(unstable))
    log("   units of the population no walk printed          %d"
        % len(missing))

    by_language = {}
    for name in unstable:
        language = name.split("/", 1)[0]
        by_language[language] = by_language.get(language, 0) + 1
    if unstable:
        log("")
        log("   the residue, by language")
        for language in sorted(by_language):
            log("       %-10s %6d" % (language, by_language[language]))
        log("   the residue, named")
        for name in unstable[:40]:
            log("       %s" % name)
            log("         walk1: %s" % first[name][:220])
            log("         walk2: %s" % second[name][:220])
            log("         walk3: %s" % third[name][:220])

    log("")
    log("-- THE DISTINCT-TEXT COLLAPSE, over the same %d units"
        % len(everywhere))
    before = set()
    for name in everywhere:
        before.add(was[name])
    after_one = set(first[name] for name in everywhere)
    after_two = set(second[name] for name in everywhere)
    after_three = set(third[name] for name in everywhere)
    log("   before, the uncorrected rule, one walk (term65_store) %d"
        % len(before))
    log("   after,  walk1                                        %d"
        % len(after_one))
    log("   after,  walk2                                        %d"
        % len(after_two))
    log("   after,  walk3 (shuffled construction order)          %d"
        % len(after_three))
    changed = []
    for name in sorted(everywhere):
        if first[name] != was[name]:
            changed.append(name)
    log("   units whose printed text the correction changes      %d"
        % len(changed))

    log("")
    log("-- THE INSTANCE log_169 printed, before and after")
    for name in ["c/op_105", "c/op_121"]:
        if name not in everywhere:
            continue
        log("   unit %s" % name)
        log("     before (term65_store, uncorrected rule): %s"
            % was[name])
        log("     after  (walk1):                          %s"
            % first[name])
        log("     after  (walk2):                          %s"
            % second[name])
        log("     after  (walk3, shuffled):                %s"
            % third[name])

    verdict = "PASS"
    if unstable:
        verdict = "FAIL"
    if missing:
        verdict = "FAIL"
    log("")
    log("-- VERDICT %s" % verdict)

    document = {
        "meta": {
            "generated_by": "acceptance79.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "the acceptance test for the corrected "
                          "layer-5 rule: three walks in three separate "
                          "processes, one of them with a shuffled "
                          "construction order, compared unit by unit",
            "walks": {
                "walk1": one["meta"],
                "walk2": two["meta"],
                "walk3": three["meta"],
            },
        },
        "population": len(was),
        "units_printed_by_all_three_walks": len(everywhere),
        "units_whose_three_texts_are_identical": len(stable),
        "units_whose_texts_differ_between_walks": len(unstable),
        "units_no_walk_printed": missing,
        "residue_by_language": by_language,
        "residue_named": unstable[:400],
        "distinct_texts_before": len(before),
        "distinct_texts_after_walk1": len(after_one),
        "distinct_texts_after_walk2": len(after_two),
        "distinct_texts_after_walk3": len(after_three),
        "units_whose_text_the_correction_changes": len(changed),
        "verdict": verdict,
    }
    handle = open(os.path.join(HERE, "acceptance79%s.json"
                                       % suffix), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE,
                               "acceptance79%s_printed.txt" % suffix),
                  "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("-- wrote acceptance79%s.json and "
        "acceptance79%s_printed.txt" % (suffix, suffix))
    if verdict != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
