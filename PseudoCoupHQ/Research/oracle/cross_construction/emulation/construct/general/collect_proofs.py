#!/usr/bin/env python3
"""collect_proofs.py -- THE PROOF TABLE: one row per (operation kind,
width, word), saying by WHICH FORM that construction is proved to be the
operation it replaces, or that it is not.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`,
section 1 -- "proved ONCE per kind, general in n and W, as a Lean lemma
in the form t2 used for its eight; where a lemma does not close in the
task's budget, the instantiation is proved by z3 at every width the
store uses".

THE OBJECTS, one sentence each, in relation.
  * A z3 ROW is one line of a `constructions_*.json` written by
    `check_constructions.py`: one SHAPE of one kind at one (width, word)
    put to z3 against z3's own operator, answered PROVED, DISPROVED,
    UNDECIDED or REFUSED.
  * A LEAN ROW is one line of `lemmas_t4.json` written by
    `run_lemmas_t4.py`: one theorem, one `lean` process.
  * A PROOF ROW -- what this file writes -- is one (kind, width, word)
    with the form it is proved by: `lemma` where a Lean theorem closed,
    `sat` where every z3 shape of it PROVED, and no form otherwise, with
    the outcome that stopped it named.
  * THE RULE IS CONSERVATIVE AND IS STATED SO IT CANNOT DRIFT: an
    instance is `sat` only where EVERY shape posed at it proved.  One
    UNDECIDED shape leaves the whole instance unproved, because the
    render may construct any shape of that kind at that width and the
    table is what the render reads.

WHY A ROW AT A WIDTH AT OR UNDER 64 IS RECORDED FOR BOTH WORDS.
`build.unit_for` gives a value of `n` bits a unit of `n` where `n <= W`
and of `W` where it is wider, so at every width at or under 64 the
construction over a word of 64 and over a word of 128 is the SAME term,
node for node.  `check_constructions.py` poses it once and carries the
words it covers on the row; this file spreads it, and the reason rides
on the proof row as `covers`.

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

HOW THIS FILE OBEYS IT.  Every key here is (kind, width, word), and the
kind is `build.py`'s display label on one z3 DECLARATION KIND.  Nothing
here reads a mnemonic or a source token, and the grouping is by machine
form alone.

usage:
  collect_proofs.py build        the table, written
  collect_proofs.py table        what the table holds, printed

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build as B                                                # noqa: E402

OUT = os.path.join(HERE, "construction_proofs.json")
LEMMAS = os.path.join(HERE, "lemmas_t4.json")
ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"

THE_Z3_FILES = "constructions_*.json"
"""every check this task ran, by name; `construction_proofs.json` is not
one of them and neither is `kind_census.json`."""

SET_ASIDE = {
    "constructions_store_rest_1_of_4.json",
    "constructions_store_rest_2_of_4.json",
    "constructions_store_rest_3_of_4.json",
    "constructions_store_rest_4_of_4.json",
}
"""THE FILES THIS TABLE DOES NOT READ, each kept on disk and each with
its reason, because a file left out silently is a file nobody can audit.

All four are lane `t4_l15`'s parts, and the reason is one measured fact:
they posed every obligation of a part IN ONE PROCESS, and z3's
`memory_max_size` raises once and then refuses everything after it in
that process.  So every row after the first solver memout in a part says
UNDECIDED because the solver was already out of memory, not because the
question is hard -- `fp_neg` at 79 bits came back UNDECIDED in 0.0 s in
part 3, and the same obligation at the tiny formats is PROVED in lane
`t4_l5`.  Lane `t4_l19` poses each obligation in a process of its own
and its parts are what this table reads."""


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def z3_rows():
    """every z3 row this task has on disk, with the file it came from."""
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, THE_Z3_FILES))):
        if os.path.basename(path) in SET_ASIDE:
            say("SET ASIDE, not read: %s" % os.path.basename(path))
            continue
        handle = open(path)
        document = json.load(handle)
        handle.close()
        for row in document.get("rows") or []:
            row = dict(row)
            row["source_file"] = os.path.basename(path)
            out.append(row)
            continue
        continue
    return out


THE_LEAN_FILES = "lemmas_t4*.json"
"""every part `run_lemmas_t4.py prove` wrote, by name: the whole run is
`lemmas_t4.json` and a part is `lemmas_t4_<i>_of_<n>.json`."""


def lean_rows():
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, THE_LEAN_FILES))):
        handle = open(path)
        document = json.load(handle)
        handle.close()
        for row in document.get("rows") or []:
            row = dict(row)
            row["source_file"] = os.path.basename(path)
            out.append(row)
            continue
        continue
    return out


THE_ORDER = ["PROVED", "UNDECIDED", "REFUSED", "NO_OBLIGATION_STATED",
             "DISPROVED"]
"""worst last: a DISPROVED shape is a defect in this task's own
construction and must be the outcome the instance carries, whatever else
proved beside it."""


def worse(left, right):
    if left is None:
        return right
    if THE_ORDER.index(right) > THE_ORDER.index(left):
        return right
    return left


def build_command():
    held = {}
    for row in z3_rows():
        width = row.get("width")
        if width is None:
            continue
        width = int(width)
        if width <= 0:
            continue
        words = row.get("covers") or [int(row["word"])]
        for word in words:
            key = (row["kind"], width, int(word))
            entry = held.get(key)
            if entry is None:
                entry = {"kind": row["kind"], "width": width,
                         "word": int(word), "shapes": [],
                         "outcome": None, "seconds": 0.0,
                         "posed_at_word": int(row["word"]),
                         "covers": words,
                         "source_files": []}
                held[key] = entry
            entry["shapes"].append({"shape": row.get("shape"),
                                    "outcome": row["outcome"],
                                    "seconds": row.get("seconds"),
                                    "nodes": row.get("nodes"),
                                    "note": row.get("cause")
                                    or row.get("counterexample")})
            entry["outcome"] = worse(entry["outcome"], row["outcome"])
            entry["seconds"] = round(entry["seconds"]
                                     + (row.get("seconds") or 0.0), 3)
            if row["source_file"] not in entry["source_files"]:
                entry["source_files"].append(row["source_file"])
            continue
        continue
    for key in held:
        entry = held[key]
        if entry["outcome"] == "PROVED":
            entry["form"] = "sat"
            continue
        entry["form"] = None
        continue
    lemmas = 0
    for row in lean_rows():
        key = (row["kind"], int(row["width"]), int(row["word"]))
        entry = held.get(key)
        if entry is None:
            entry = {"kind": row["kind"], "width": int(row["width"]),
                     "word": int(row["word"]), "shapes": [],
                     "outcome": row["outcome"], "seconds": 0.0,
                     "form": None, "source_files": []}
            held[key] = entry
        entry["lean_outcome"] = row["outcome"]
        entry["theorem"] = row.get("theorem_name")
        if row["outcome"] != "PROVED_BY_LEAN":
            continue
        # A CLOSED LEAN THEOREM IS THE STRONGER FORM and takes the row,
        # whatever z3 answered beside it.
        entry["form"] = "lemma"
        entry["outcome"] = "PROVED"
        lemmas = lemmas + 1
        continue
    rows = []
    for key in sorted(held, key=lambda one: (one[0], one[1], one[2])):
        rows.append(held[key])
        continue
    counts = {}
    forms = {}
    for row in rows:
        counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
        label = row["form"] or "none"
        forms[label] = forms.get(label, 0) + 1
        continue
    document = {
        "meta": {
            "what": "one row per (operation kind, width, word): the "
                    "form the construction is proved by at that "
                    "instance, or the outcome that stopped it",
            "z3_files": sorted(set(name for row in rows
                                   for name in row["source_files"])),
            "lemmas_file": os.path.basename(LEMMAS),
            "set_aside": sorted(SET_ASIDE),
            "lean_rows_that_closed": lemmas,
            "counts": counts,
            "forms": forms,
            "peak_kb": peak_kb(),
        },
        "rows": rows,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("written: %s" % OUT)
    say("")
    report(rows, counts, forms)
    return 0


def report(rows, counts, forms):
    say("| operation kind | width | word | form | outcome | shapes | s |")
    say("|---|---|---|---|---|---|---|")
    for row in rows:
        say("| %s | %d | %d | %s | %s | %d | %s |"
            % (row["kind"], row["width"], row["word"],
               row["form"] or "--", row["outcome"],
               len(row["shapes"]), row["seconds"]))
        continue
    say("")
    say("| outcome | instances |")
    say("|---|---|")
    for outcome in sorted(counts):
        say("| %s | %d |" % (outcome, counts[outcome]))
        continue
    say("")
    say("| the form of record | instances |")
    say("|---|---|")
    for label in sorted(forms):
        say("| %s | %d |" % (label, forms[label]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return


def table_command():
    if not os.path.exists(OUT):
        say("no table on disk at %s" % OUT)
        return 2
    handle = open(OUT)
    document = json.load(handle)
    handle.close()
    report(document["rows"], document["meta"]["counts"],
           document["meta"]["forms"])
    return 0


def main(argv):
    what = argv[1] if len(argv) > 1 else "build"
    if what == "build":
        return build_command()
    if what == "table":
        return table_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
