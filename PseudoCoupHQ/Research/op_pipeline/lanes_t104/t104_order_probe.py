#!/usr/bin/env python3
"""t104_order_probe.py -- for every unit the operand-order acceptance
flagged, WHY the two texts differ, and whether ordering the operands
BEFORE the first simplification closes it.

WHAT THE ACCEPTANCE FLAGGED.  `t104_walk.py` builds, for each unit, a
second term that differs from the first only in the order of some
commutative node's operands, normalizes both, and records the unit when
the two texts differ.  A difference there is one of exactly two things,
and this program separates them:

  - MY PERTURBATION IS UNSOUND for that unit -- the permuted term is
    not the same computation.  Then the flag is this task's defect and
    not the normalizer's.  Checked by asking the solver whether the two
    terms are equal for every input.
  - THE NORMALIZER'S TEXT DEPENDS ON OPERAND ORDER for that unit.
    Then it is the gap the brief names.

AND THE CANDIDATE FIX, measured beside the defect rather than after it.
`Term.normalize` as `term.py` stands runs, in order: simplify, order
the commutative operands, rename positionally, simplify, order again,
print.  THE FIRST SIMPLIFICATION THEREFORE SEES AN UNORDERED TERM, and
`z3.simplify` is not itself order-invariant: a term and its
operand-permuted twin can leave the simplifier in shapes that differ by
more than operand order, which the ordering step afterwards cannot
undo.  The candidate is one extra call of the SAME ordering function,
before that first simplification.  This program prints, per unit, the
text pair as `term.py` prints it today and the text pair with the
candidate applied, so the fix is measured on the units that motivate
it.  It does not edit `term.py`.

MEMORY: one forked sub-process per unit, `RLIMIT_AS` at the ceiling
below; the parent forks and collects.  Named abort ABORT_MEMORY_T104.

WRITES: t104_order_probe.json

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

Coding discipline: no compound one-liner statements.

It saves after every unit and takes a whole-lane budget, so a lane
stopped on its ceiling leaves the units it did answer on disk.

usage:
  t104_order_probe.py [ceiling_mb seconds_per_unit limit budget_seconds]
"""

import json
import os
import random
import resource
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
sys.path.insert(0, PIPELINE)
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import term as T                                                 # noqa: E402
import t104_walk as W                                            # noqa: E402

OUT = os.path.join(PIPELINE, "t104_order_probe.json")
EVIDENCE = os.path.join(PIPELINE, "t104_walk_evidence.json")
PARENT_CAP_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    used = peak_kb()
    if used > PARENT_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY_T104: the parent's peak resident %d kB "
            "passed the stated cap of %d kB at %s"
            % (used, PARENT_CAP_KB, where))
    return used


def normalize_with_pre_order(maker, term):
    """THE CANDIDATE: `Term.normalize`'s own steps, with ONE extra call
    of `order_commutative` before the first simplification.

    Everything else is byte-for-byte the method in `term.py`; the copy
    lives here only so the candidate can be measured without editing
    the pipeline before the measurement says it should be edited."""
    simplified = T.order_commutative(term)
    simplified = z3.simplify(simplified)
    simplified = T.order_commutative(simplified)
    symbols = T.ordered_symbols(simplified)
    substitution = []
    for index, symbol in enumerate(symbols):
        if symbol.sort().kind() == z3.Z3_BV_SORT:
            fresh = z3.BitVec("v%d" % index, symbol.size())
        else:
            fresh = z3.Const("v%d" % index, symbol.sort())
        substitution.append((symbol, fresh))
    if substitution:
        simplified = z3.substitute(simplified, *substitution)
    simplified = z3.simplify(simplified)
    simplified = T.order_commutative(simplified)
    return T.one_line(simplified)


def equal_for_every_input(left, right, milliseconds):
    """the solver's answer to 'are these the same computation': unsat
    for `left != right` means equal."""
    solver = z3.Solver()
    solver.set("timeout", milliseconds)
    solver.add(left != right)
    answer = solver.check()
    if answer == z3.unsat:
        return "EQUAL"
    if answer == z3.sat:
        return "DIFFERENT"
    return "UNDECIDED"


def _alarm(signum, frame):
    raise TimeoutError()


def one_unit_forked(maker, name, unit, ceiling_mb, seconds):
    read_end, write_end = os.pipe()
    started = time.time()
    child = os.fork()
    if child == 0:
        os.close(read_end)
        try:
            cap = ceiling_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            transcription = maker.transcribe(unit)
            raw = transcription.out_term
            shuffler = random.Random("t104|%s" % name)
            other, moved = W.permute_commutative(raw, shuffler)
            answer = {
                "ok": True,
                "commutative_nodes_reordered": moved,
                "solver_says": equal_for_every_input(raw, other, 20000),
                "text_today_as_transcribed": maker.normalize(raw),
                "text_today_operand_permuted": maker.normalize(other),
                "text_candidate_as_transcribed":
                    normalize_with_pre_order(maker, raw),
                "text_candidate_operand_permuted":
                    normalize_with_pre_order(maker, other),
            }
            payload = json.dumps(answer)
        except BaseException as problem:
            payload = json.dumps({"ok": False,
                                  "raised": "%s: %s"
                                  % (type(problem).__name__, problem)})
        try:
            handle = os.fdopen(write_end, "w")
            handle.write(payload)
            handle.close()
        except BaseException:
            pass
        os._exit(0)
    os.close(write_end)
    handle = os.fdopen(read_end, "r")
    text = ""
    timed_out = False
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(seconds) + 1)
    try:
        text = handle.read()
    except TimeoutError:
        timed_out = True
    signal.alarm(0)
    handle.close()
    if timed_out:
        os.kill(child, signal.SIGKILL)
    stamp = os.wait4(child, 0)
    wall = time.time() - started
    if timed_out:
        return "TIMED_OUT", None, wall, stamp[2].ru_maxrss
    if text == "":
        return "ABORTED", None, wall, stamp[2].ru_maxrss
    answer = json.loads(text)
    if not answer["ok"]:
        return "RAISED", answer, wall, stamp[2].ru_maxrss
    return "walked", answer, wall, stamp[2].ru_maxrss


def flagged_units():
    document = json.load(open(EVIDENCE))
    out = []
    for row in document["perturbation_disagreements"]:
        out.append(row["unit"])
    return out


def find_units(names):
    left = set(names)
    found = {}
    for path in W.canon40_shards():
        document = json.load(open(path))
        units = document.get("units") or {}
        for name in list(left):
            if name not in units:
                continue
            record = dict(units[name])
            record["unit"] = name
            found[name] = record
            left.discard(name)
        document = None
        if not left:
            break
    return found


def save(rows, counts, total, answered, started, budget):
    document = {
        "summary": dict(counts),
        "population":
            "%d of the %d units the operand-order acceptance flagged, "
            "in the order the acceptance recorded them; the lane "
            "budget was %d s" % (answered, total, budget),
        "seconds_so_far": round(time.time() - started, 1),
        "units": rows,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return document


def main():
    ceiling = 3072
    seconds = 300
    limit = 0
    budget = 5400
    if len(sys.argv) > 2:
        ceiling = int(sys.argv[1])
        seconds = int(sys.argv[2])
    if len(sys.argv) > 3:
        limit = int(sys.argv[3])
    if len(sys.argv) > 4:
        budget = int(sys.argv[4])
    names = flagged_units()
    if limit:
        names = names[:limit]
    total = len(names)
    sys.stdout.write("-- %d units the operand-order acceptance "
                     "flagged, ceiling %d MB, %d s each\n"
                     % (total, ceiling, seconds))
    sys.stdout.flush()
    found = find_units(names)
    maker = W.build_maker()
    rows = []
    counts = {
        "units": total,
        "solver_EQUAL": 0,
        "solver_DIFFERENT": 0,
        "solver_UNDECIDED": 0,
        "text_today_disagrees": 0,
        "text_candidate_disagrees": 0,
        "candidate_changes_the_text_of_the_transcribed_term": 0,
        "not_answered": 0,
    }
    index = 0
    started = time.time()
    for name in names:
        index = index + 1
        sys.stdout.write("[%d/%d] %s\n" % (index, total, name))
        sys.stdout.flush()
        if name not in found:
            counts["not_answered"] = counts["not_answered"] + 1
            rows.append({"unit": name, "word": "NOT_IN_CANON40"})
            continue
        word, answer, wall, child_peak = one_unit_forked(
            maker, name, found[name], ceiling, seconds)
        if word != "walked":
            counts["not_answered"] = counts["not_answered"] + 1
            rows.append({"unit": name, "word": word,
                         "wall_seconds": round(wall, 2)})
            sys.stdout.write("   %s\n" % word)
            sys.stdout.flush()
            continue
        says = answer["solver_says"]
        counts["solver_" + says] = counts.get("solver_" + says, 0) + 1
        today_disagrees = (answer["text_today_as_transcribed"]
                           != answer["text_today_operand_permuted"])
        candidate_disagrees = (
            answer["text_candidate_as_transcribed"]
            != answer["text_candidate_operand_permuted"])
        if today_disagrees:
            counts["text_today_disagrees"] = (
                counts["text_today_disagrees"] + 1)
        if candidate_disagrees:
            counts["text_candidate_disagrees"] = (
                counts["text_candidate_disagrees"] + 1)
        if (answer["text_candidate_as_transcribed"]
                != answer["text_today_as_transcribed"]):
            key = "candidate_changes_the_text_of_the_transcribed_term"
            counts[key] = counts[key] + 1
        row = dict(answer)
        row["unit"] = name
        row["word"] = word
        row["wall_seconds"] = round(wall, 2)
        row["sub_peak_kb"] = child_peak
        row["today_disagrees"] = today_disagrees
        row["candidate_disagrees"] = candidate_disagrees
        rows.append(row)
        sys.stdout.write("   solver %s, today disagrees %s, candidate "
                         "disagrees %s\n"
                         % (says, today_disagrees, candidate_disagrees))
        sys.stdout.flush()
        check_memory(name)
        save(rows, counts, total, index, started, budget)
        if time.time() - started > budget:
            sys.stdout.write("-- the lane budget of %d s is spent "
                             "after %d of %d units; stopping with the "
                             "answers so far on disk\n"
                             % (budget, index, total))
            sys.stdout.flush()
            break
    counts["seconds"] = round(time.time() - started, 1)
    counts["parent_peak_resident_kb"] = peak_kb()
    counts["units_answered"] = len(rows)
    save(rows, counts, total, len(rows), started, budget)
    for key in sorted(counts):
        sys.stdout.write("   %-56s %s\n" % (key, counts[key]))
    sys.stdout.write("-- wrote %s\n" % OUT)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
