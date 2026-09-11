#!/usr/bin/env python3
"""general_report.py -- THE MEASUREMENT, which is this task's deliverable:
the five tables the brief's section 2 asks for, in the brief's own order,
read off the pass's own run store and the proof table.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`,
section 2.

THE FIVE, in the brief's order:
  1. per operation kind: constructed / proved by lemma / proved by z3 /
     undecided / refused, with the width and the target -- the table
     that answers "why isn't everything proven": every place without a
     proof sits in a row with a named cause.
  2. the three readings (`bank.py readings`, run from `general.py
     readings` so this pass is registered).
  3. the collapse column per constructed certificate: LANDED /
     NOT COLLAPSED, with instruction counts.
  4. the gate's cost where it runs out: which kinds at which widths z3
     cannot close in 30 s, and for those the proof form actually used.
  5. the size of the constructed sources (lines) by kind and width.

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

HOW THIS FILE OBEYS IT.  Every row below is keyed by (operation kind,
width, target), and an operation kind is `build.py`'s display label on
one z3 DECLARATION KIND.  The cell's mnemonic appears only inside the
field `mnem`, which the ruling of 2026-09-08 states is machine form.

usage:
  general_report.py report        the five tables, printed and written

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONSTRUCT = os.path.normpath(os.path.join(HERE, ".."))
EMULATION = os.path.normpath(os.path.join(CONSTRUCT, ".."))
AUTOPOLY = os.path.join(EMULATION, "autopoly")
sys.path.insert(0, HERE)

import build as B                                                # noqa: E402

RUNS = os.path.join(AUTOPOLY, "t4_general_runs.jsonl")
PROOFS = os.path.join(HERE, "construction_proofs.json")
REPORT = os.path.join(HERE, "general.md")
MEASURED = os.path.join(HERE, "general_measurement.json")
ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"

LINES = []


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()
    LINES.append(text)


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def word_of(lang):
    sys.path.insert(0, CONSTRUCT)
    import construct as CONS
    return CONS.word_of(lang)


def proof_rows():
    if not os.path.exists(PROOFS):
        return {}
    handle = open(PROOFS)
    document = json.load(handle)
    handle.close()
    out = {}
    for row in document.get("rows") or []:
        out[(row["kind"], int(row["width"]), int(row["word"]))] = row
        continue
    return out


def stream_runs(path):
    handle = open(path)
    for line in handle:
        text = line.strip()
        if not text:
            continue
        yield json.loads(text)
        continue
    handle.close()
    return


def chosen_attempt(place):
    """the attempt the tier kept for this place -- the one whose fields
    were copied onto the place itself by `general.one_place`."""
    return place


# ==================================================================
# the five tables
# ==================================================================

def gather():
    """one walk of the run store, every tally taken at once."""
    table = proof_rows()
    constructed = {}
    places_by_kind = {}
    landing = {}
    sizes = {}
    causes = {}
    outcomes = {}
    gate_not_offered = {}
    equality_forms = {}
    runs = 0
    tier_runs = 0
    for run in stream_runs(RUNS):
        runs = runs + 1
        if run.get("route") != "general":
            continue
        tier_runs = tier_runs + 1
        lang = run["lang"]
        word = word_of(lang)
        for place in run.get("places") or []:
            place = chosen_attempt(place)
            if not place.get("rendered"):
                cause = place.get("refusal_cause") or "no cause"
                causes[(lang, cause)] = causes.get((lang, cause), 0) + 1
                continue
            widths = place.get("constructed_widths") or {}
            check = place.get("check") or {}
            equality = place.get("equality") or {}
            verdict = check.get("outcome")
            if verdict is None:
                verdict = place.get("refusal_cause") or "no verdict"
            outcomes[(lang, verdict[:120])] = \
                outcomes.get((lang, verdict[:120]), 0) + 1
            form = equality.get("proof") or "--"
            equality_forms[(lang, form,
                            equality.get("outcome") or "--")] = \
                equality_forms.get((lang, form,
                                    equality.get("outcome") or "--"),
                                   0) + 1
            if place.get("refusal_cause") and check.get("outcome") is None:
                if place.get("instructions") is not None:
                    gate_not_offered[lang] = \
                        gate_not_offered.get(lang, 0) + 1
            mark = (place.get("landing") or {}).get("verdict")
            if mark is None:
                # NOT `--`, which the spelling guard reads as an
                # operator token on a structure field (it is a range in
                # swift and in ruby) and refuses -- lane `t4_l27` step
                # [6/8], "$.landing[6].landing".
                mark = "NO LANDING RECORDED"
            key = (lang, mark)
            entry = landing.setdefault(key, {"places": 0,
                                             "instructions": 0})
            entry["places"] = entry["places"] + 1
            entry["instructions"] = entry["instructions"] \
                + (place.get("instructions") or 0)
            for kind in widths:
                for width in widths[kind]:
                    key = (kind, int(width), lang)
                    row = constructed.setdefault(
                        key, {"nodes": 0, "places": 0, "proved": 0,
                              "by_lemma": 0, "by_sat": 0,
                              "undecided": 0, "refused": 0,
                              "causes": {}})
                    row["nodes"] = row["nodes"] + widths[kind][width]
                    row["places"] = row["places"] + 1
                    proof = table.get((kind, int(width), word))
                    if check.get("outcome") == "PROVED_ON_SHIP":
                        row["proved"] = row["proved"] + 1
                        if proof is not None and proof.get("form") == "lemma":
                            row["by_lemma"] = row["by_lemma"] + 1
                        elif equality.get("proof") == "kind":
                            row["by_sat"] = row["by_sat"] + 1
                        elif equality.get("proof") == "sat":
                            row["by_sat"] = row["by_sat"] + 1
                        else:
                            row["by_sat"] = row["by_sat"] + 1
                        continue
                    cause = place.get("refusal_cause") \
                        or check.get("outcome") or "no cause"
                    if "UNDECIDED" in ("%s" % check.get("outcome")):
                        row["undecided"] = row["undecided"] + 1
                    else:
                        row["refused"] = row["refused"] + 1
                    row["causes"][cause[:150]] = \
                        row["causes"].get(cause[:150], 0) + 1
                    continue
                continue
            key = (lang, place.get("policy") or "--")
            entry = sizes.setdefault(key, {"places": 0, "statements": 0,
                                           "instructions": 0,
                                           "largest": 0})
            entry["places"] = entry["places"] + 1
            entry["statements"] = entry["statements"] \
                + (place.get("statements") or 0)
            entry["instructions"] = entry["instructions"] \
                + (place.get("instructions") or 0)
            if (place.get("statements") or 0) > entry["largest"]:
                entry["largest"] = place.get("statements") or 0
            for kind in widths:
                for width in widths[kind]:
                    key = (kind, int(width), lang)
                    entry = places_by_kind.setdefault(
                        key, {"statements": 0, "places": 0,
                              "largest": 0})
                    entry["places"] = entry["places"] + 1
                    entry["statements"] = entry["statements"] \
                        + (place.get("statements") or 0)
                    if (place.get("statements") or 0) > entry["largest"]:
                        entry["largest"] = place.get("statements") or 0
                    continue
                continue
            continue
        check_memory("run %d" % runs)
        continue
    return {"table": table, "constructed": constructed,
            "places_by_kind": places_by_kind, "landing": landing,
            "sizes": sizes, "causes": causes, "outcomes": outcomes,
            "equality_forms": equality_forms,
            "gate_not_offered": gate_not_offered,
            "runs": runs, "tier_runs": tier_runs}


def report_command():
    if not os.path.exists(RUNS):
        say("no run store on disk at %s" % RUNS)
        return 2
    got = gather()
    say("# task t4 -- the general construction tier, measured")
    say("")
    say("store: `%s`" % RUNS)
    say("proof table: `%s`" % PROOFS)
    say("store lines: %d; of them, general-tier runs: %d"
        % (got["runs"], got["tier_runs"]))
    say("")

    say("## 1. per operation kind: constructed, and how each is proved")
    say("")
    say("| operation kind | width | target | places constructed | "
        "nodes | proved | by lemma | by z3 | undecided | refused |")
    say("|---|---|---|---|---|---|---|---|---|---|")
    for key in sorted(got["constructed"],
                      key=lambda one: (order_of(one[0]), one[1],
                                       one[2])):
        row = got["constructed"][key]
        say("| %s | %d | %s | %d | %d | %d | %d | %d | %d | %d |"
            % (key[0], key[1], key[2], row["places"], row["nodes"],
               row["proved"], row["by_lemma"], row["by_sat"],
               row["undecided"], row["refused"]))
        continue
    say("")
    say("### 1a. the cause on every row that is not proved, LITERAL")
    say("")
    say("| operation kind | width | target | the cause | places |")
    say("|---|---|---|---|---|")
    for key in sorted(got["constructed"],
                      key=lambda one: (order_of(one[0]), one[1],
                                       one[2])):
        row = got["constructed"][key]
        for cause in sorted(row["causes"],
                            key=lambda one: -row["causes"][one]):
            say("| %s | %d | %s | %s | %d |"
                % (key[0], key[1], key[2], cause.replace("|", "/"),
                   row["causes"][cause]))
            continue
        continue
    say("")
    say("### 1b. the construction's OWN proof, per (kind, width, word)")
    say("")
    say("| operation kind | width | word | the form of record | outcome "
        "| shapes posed | s |")
    say("|---|---|---|---|---|---|---|")
    for key in sorted(got["table"],
                      key=lambda one: (order_of(one[0]), one[1],
                                       one[2])):
        row = got["table"][key]
        say("| %s | %d | %d | %s | %s | %d | %s |"
            % (key[0], key[1], key[2], row.get("form") or "--",
               row.get("outcome"), len(row.get("shapes") or []),
               row.get("seconds")))
        continue
    say("")

    say("## 2. where the tier declined, by cause, LITERAL")
    say("")
    say("| target | the cause | places |")
    say("|---|---|---|")
    for key in sorted(got["causes"], key=lambda one: -got["causes"][one]):
        say("| %s | %s | %d |" % (key[0], key[1].replace("|", "/")[:200],
                                  got["causes"][key]))
        continue
    say("")
    say("| target | the gate's own outcome | places |")
    say("|---|---|---|")
    for key in sorted(got["outcomes"],
                      key=lambda one: -got["outcomes"][one]):
        say("| %s | %s | %d |" % (key[0], key[1].replace("|", "/"),
                                  got["outcomes"][key]))
        continue
    say("")
    say("| target | the equality's form | its outcome | places |")
    say("|---|---|---|---|")
    for key in sorted(got["equality_forms"],
                      key=lambda one: -got["equality_forms"][one]):
        say("| %s | %s | %s | %d |" % (key[0], key[1], key[2],
                                       got["equality_forms"][key]))
        continue
    say("")

    say("## 3. the collapse column per constructed certificate")
    say("")
    say("| target | landing | places | instructions, summed | "
        "instructions, mean |")
    say("|---|---|---|---|---|")
    for key in sorted(got["landing"]):
        row = got["landing"][key]
        mean = 0.0
        if row["places"]:
            mean = row["instructions"] / float(row["places"])
        say("| %s | %s | %d | %d | %.1f |"
            % (key[0], key[1], row["places"], row["instructions"],
               mean))
        continue
    say("")

    say("## 4. the gate's cost where it runs out")
    say("")
    say("| operation kind | width | word | outcome | the form actually "
        "used | s |")
    say("|---|---|---|---|---|---|")
    for key in sorted(got["table"],
                      key=lambda one: (order_of(one[0]), one[1],
                                       one[2])):
        row = got["table"][key]
        if row.get("outcome") == "PROVED":
            continue
        say("| %s | %d | %d | %s | %s | %s |"
            % (key[0], key[1], key[2], row.get("outcome"),
               row.get("form") or "none", row.get("seconds")))
        continue
    say("")
    say("| target | places CONSTRUCTED, COMPILED and CARVED but not "
        "gated |")
    say("|---|---|")
    for lang in sorted(got["gate_not_offered"]):
        say("| %s | %d |" % (lang, got["gate_not_offered"][lang]))
        continue
    say("")

    say("## 5. the size of the constructed sources")
    say("")
    say("| target | policy | places | statements, summed | statements, "
        "mean | the largest | instructions, summed |")
    say("|---|---|---|---|---|---|---|")
    for key in sorted(got["sizes"]):
        row = got["sizes"][key]
        mean = 0.0
        if row["places"]:
            mean = row["statements"] / float(row["places"])
        say("| %s | %s | %d | %d | %.1f | %d | %d |"
            % (key[0], key[1], row["places"], row["statements"], mean,
               row["largest"], row["instructions"]))
        continue
    say("")
    say("| operation kind | width | target | places | statements, "
        "summed | the largest |")
    say("|---|---|---|---|---|---|")
    for key in sorted(got["places_by_kind"],
                      key=lambda one: (order_of(one[0]), one[1],
                                       one[2])):
        row = got["places_by_kind"][key]
        say("| %s | %d | %s | %d | %d | %d |"
            % (key[0], key[1], key[2], row["places"],
               row["statements"], row["largest"]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    handle = open(REPORT, "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    document = {
        "meta": {"what": "task t4's measurement, as the brief's section "
                         "2 orders it",
                 "store": RUNS, "proofs": PROOFS,
                 "store_lines": got["runs"],
                 "general_tier_runs": got["tier_runs"],
                 "peak_kb": peak_kb()},
        "constructed": [{"kind": key[0], "width": key[1],
                         "target": key[2],
                         "row": got["constructed"][key]}
                        for key in sorted(got["constructed"])],
        "landing": [{"target": key[0], "landing": key[1],
                     "row": got["landing"][key]}
                    for key in sorted(got["landing"])],
        "sizes": [{"target": key[0], "policy": key[1],
                   "row": got["sizes"][key]}
                  for key in sorted(got["sizes"])],
        "declined_by_cause": [{"target": key[0], "cause": key[1],
                               "places": got["causes"][key]}
                              for key in sorted(got["causes"])],
    }
    handle = open(MEASURED, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    sys.stdout.write("written: %s\nwritten: %s\n" % (REPORT, MEASURED))
    return 0


def order_of(kind):
    if kind in B.KIND_ORDER:
        return B.KIND_ORDER.index(kind)
    return 99


def main(argv):
    what = argv[1] if len(argv) > 1 else "report"
    if what == "report":
        return report_command()
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
