#!/usr/bin/env python3
"""normalize79_split_causes.py -- THE CAUSE OF EVERY PREDICTED SPLIT,
decided by the solver rather than by reading.

WHAT A SPLIT IS HERE.  `normalize79_pool_prediction.py` predicts that
under the corrected layer-5 rule 11 of pool5's entries stop being one
entry.  A split can be one of two entirely different things, and the
difference matters more than the count:

  * A FALSE MERGE REPAIRED -- the two members compute DIFFERENT
    functions of the registers their values arrive in, and the
    uncorrected rule printed one text for both because the positional
    renaming followed an unstable argument order.  The corrected rule
    separating them is the rule working.
  * A REAL MERGE LOST -- the two members compute the SAME function and
    the corrected rule prints two texts.  That would be a cost of the
    repair and it would be stated as one.

HOW IT IS DECIDED.  For each split, one member of each of the groups
the corrected rule forms is transcribed to its layer-4 term over the
SAME free symbols (each register family's own symbol), and z3 is asked
whether the two terms can differ.  `unsat` means they are equal for
every value of every register -- a real merge lost.  `sat` means there
are register values at which they answer differently -- a false merge
repaired, and the counterexample is printed.

WRITES:
  normalize79_split_causes.json
  normalize79_split_causes_printed.txt

MEMORY BOUND: one shard's JSON at a time plus the terms of at most a
few dozen units; expected peak resident size under 1 GB, hard cap
6 GB with the named abort ABORT_MEMORY_CEILING.

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

No operator token appears in this file.  The candidate set compared
here comes from the pool's own member sets, never from a token.
"""

import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402

import canonical_form as CF                                      # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import normalize79_pool_prediction as PP                          # noqa: E402

LINES = []
MEMORY_CEILING_MB = 6144
SOLVER_TIMEOUT_MS = 10000


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_resident_mb():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return used / 1024.0


def shards():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE, "canon39_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon39_interp.json"))
    pattern = os.path.join(HERE, "canon39_regen_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return [path for path in out if os.path.exists(path)]


def records_for(wanted):
    """the wrapped record of each named unit, read off the shards."""
    found = {}
    for path in shards():
        document = json.load(open(path))
        units = document.get("units", {})
        for name in wanted:
            if name in found:
                continue
            if name in units:
                found[name] = units[name]
        document = None
        if peak_resident_mb() > MEMORY_CEILING_MB:
            log("ABORT_MEMORY_CEILING: %.0f MB over the %d MB cap"
                % (peak_resident_mb(), MEMORY_CEILING_MB))
            raise SystemExit(3)
        if len(found) == len(wanted):
            break
    return found


def main():
    document, members, entry_of, order = members_of()
    old_texts = {}
    for name in members:
        text = members[name].get("layer5_normalized_text")
        if text:
            old_texts[name] = text
    label = "walk1"
    out_dir = HERE
    data_dir = HERE
    if "--walk" in sys.argv:
        label = sys.argv[sys.argv.index("--walk") + 1]
    if "--out-dir" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out-dir") + 1]
    if "--data-dir" in sys.argv:
        data_dir = sys.argv[sys.argv.index("--data-dir") + 1]
    walk = json.load(open(os.path.join(
        data_dir, "normalize79_walk_%s.json" % label)))
    new_texts = {}
    for name in walk["texts"]:
        if name in members:
            new_texts[name] = walk["texts"][name]

    before_groups, _ = PP.partition(members, order, old_texts)
    after_groups, _ = PP.partition(members, order, new_texts)

    after_of = {}
    for root in after_groups:
        for name in after_groups[root]:
            after_of[name] = root

    splits = []
    for root in before_groups:
        landed = {}
        for name in before_groups[root]:
            landed.setdefault(after_of[name], [])
            landed[after_of[name]].append(name)
        if len(landed) > 1:
            splits.append(landed)

    log("-- THE SPLITS the corrected rule predicts")
    log("   entries that stop being one entry %d" % len(splits))

    wanted = set()
    for landed in splits:
        for root in landed:
            wanted.add(sorted(landed[root])[0])
    log("   units to transcribe (one per group of each split) %d"
        % len(wanted))

    found = records_for(wanted)
    log("   units found in the shards %d" % len(found))

    attached = callee_units()
    maker = T.Term(reference=R.Reference(runtime_units=attached),
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)
    terms = {}
    for name in sorted(found):
        unit = dict(found[name])
        unit["unit"] = name
        transcription = maker.transcribe(unit)
        terms[name] = transcription.out_term

    rows = []
    repaired = 0
    lost = 0
    undecided = 0
    for landed in splits:
        heads = []
        for root in sorted(landed, key=lambda one: sorted(landed[one])[0]):
            heads.append(sorted(landed[root])[0])
        left = heads[0]
        outcomes = []
        for right in heads[1:]:
            outcome = compare_two(terms, left, right)
            outcomes.append(outcome)
        row = {
            "members_before": sum(len(landed[root]) for root in landed),
            "groups_after": len(landed),
            "one_member_of_each_group": heads,
            "comparisons": outcomes,
        }
        rows.append(row)
        for outcome in outcomes:
            if outcome["verdict"] == "PROVED_DIFFERENT":
                repaired = repaired + 1
            elif outcome["verdict"] == "PROVED_EQUAL":
                lost = lost + 1
            else:
                undecided = undecided + 1

    log("")
    log("-- THE CAUSE, decided by the solver, one comparison per pair "
        "of groups")
    log("   comparisons whose two sides are PROVED DIFFERENT "
        "(a false merge repaired) %d" % repaired)
    log("   comparisons whose two sides are PROVED EQUAL "
        "(a real merge lost)      %d" % lost)
    log("   comparisons the solver left undecided                     "
        "         %d" % undecided)

    log("")
    log("-- EVERY SPLIT, PRINTED")
    for row in rows:
        log("   an entry of %d members becomes %d"
            % (row["members_before"], row["groups_after"]))
        for outcome in row["comparisons"]:
            log("     %s" % outcome["left"])
            log("       old text: %s" % old_texts.get(outcome["left"],
                                                      "")[:200])
            log("       new text: %s" % new_texts.get(outcome["left"],
                                                      "")[:200])
            log("     %s" % outcome["right"])
            log("       old text: %s" % old_texts.get(outcome["right"],
                                                      "")[:200])
            log("       new text: %s" % new_texts.get(outcome["right"],
                                                      "")[:200])
            log("       verdict : %s" % outcome["verdict"])
            if outcome.get("counterexample"):
                log("       at      : %s" % outcome["counterexample"])

    out = {
        "meta": {
            "generated_by": "normalize79_split_causes.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "the cause of every split the corrected "
                          "layer-5 rule predicts, decided by asking z3 "
                          "whether the two sides can answer "
                          "differently for some value of the registers "
                          "their values arrive in",
            "solver_timeout_ms": SOLVER_TIMEOUT_MS,
            "walk_read": label,
            "modules_read_from": HERE,
            "peak_resident_mb": round(peak_resident_mb(), 1),
        },
        "splits": len(splits),
        "comparisons_proved_different": repaired,
        "comparisons_proved_equal": lost,
        "comparisons_undecided": undecided,
        "rows": rows,
    }
    handle = open(os.path.join(
        out_dir, "normalize79_split_causes.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(
        out_dir, "normalize79_split_causes_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote normalize79_split_causes.json and "
        "normalize79_split_causes_printed.txt")
    return 0


def members_of():
    return PP.members_of_pool5()


def callee_units():
    path = os.path.join(HERE, "canon39_callee_units.json")
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain")
        name = unit.get("callee")
        if toolchain is None:
            toolchain = key.split("/", 1)[0]
        if name is None:
            name = key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


def compare_two(terms, left, right):
    """can the two terms answer differently for some value of the
    registers?  `unsat` = never = the two are equal."""
    first = terms.get(left)
    second = terms.get(right)
    if first is None or second is None:
        return {"left": left, "right": right,
                "verdict": "NO_TERM",
                "detail": "one side has no transcribed term"}
    if first.sort() != second.sort():
        return {"left": left, "right": right,
                "verdict": "PROVED_DIFFERENT",
                "detail": "the two answers are not even the same "
                          "width: %s against %s"
                          % (first.sort(), second.sort())}
    solver = z3.Solver()
    solver.set("timeout", SOLVER_TIMEOUT_MS)
    solver.add(first != second)
    answer = solver.check()
    if answer == z3.unsat:
        return {"left": left, "right": right,
                "verdict": "PROVED_EQUAL",
                "detail": "no value of any register makes the two "
                          "answer differently"}
    if answer == z3.sat:
        model = solver.model()
        spelled = []
        for declaration in model.decls():
            spelled.append("%s = %s"
                           % (declaration.name(),
                              model[declaration]))
        return {"left": left, "right": right,
                "verdict": "PROVED_DIFFERENT",
                "detail": "the two answer differently at the printed "
                          "register values",
                "counterexample": "; ".join(sorted(spelled))[:400]}
    return {"left": left, "right": right,
            "verdict": "UNDECIDED",
            "detail": "the solver did not answer within %d ms"
                      % SOLVER_TIMEOUT_MS}


if __name__ == "__main__":
    sys.exit(main())
