#!/usr/bin/env python3
"""check_schemas.py -- the schemas put to z3 on their own, before any of
them touches a cell.

WHAT THIS IS.  Every schema in `schemas.py` claims one thing: the term
it builds out of limbs of the word computes the SAME mapping as the
operation it replaces.  This file asks the solver that question directly,
at several (width, word) pairs, over free symbols -- so a schema that is
wrong is wrong here, in one line naming the operation and the width, and
not two hundred runs later inside a verdict about a cell.

It reads nothing off disk, names no cell and no target, and its
population is a list of (width, word) pairs and z3 declaration kinds.

MEMORY: one process, no forked workers; the caller states the bound and
the named abort.  Every obligation is put at a stated ceiling.

Coding discipline: no compound one-liner statements.
"""

import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import schemas as S                                              # noqa: E402

ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T2"
CEILING_MS = 30000
"""the brief's hard ceiling: z3 is the audit and never the workhorse."""


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))
    return peak


def built_from_limbs(name, width, word):
    """one operand of `width` bits, BUILT OUT OF free symbols no wider
    than the word -- which is how every wide value in this pipeline
    arrives: a register pair, an extension, a concatenation.  A free
    symbol wider than the word is a question about the arrival contract
    and the tier refuses it by cause, so posing one here would test the
    refusal and not the schema."""
    count = S.limb_count(width, word)
    top = S.top_bits(width, word)
    pieces = []
    for index in range(count):
        bits = word
        if index == count - 1:
            bits = top
        pieces.append(z3.BitVec("%s%d" % (name, index), bits))
        continue
    if count == 1:
        return pieces[0]
    pieces.reverse()
    return z3.Concat(*pieces)


def a_and_b(width, word):
    return (built_from_limbs("a", width, word),
            built_from_limbs("b", width, word))


def obligations(width, word, with_divider):
    """one entry per operation: its name for the report, the term as z3
    spells it, and nothing else.  The names are the SCHEMA names of
    `schemas.py` plus the z3 declaration kind, never an opcode."""
    left, right = a_and_b(width, word)
    narrow = z3.BitVec("c", word)
    rows = [
        ("BADD", S.ADD_SUB, left + right),
        ("BSUB", S.ADD_SUB, left - right),
        ("BNEG", S.ADD_SUB, -left),
        ("BMUL", S.MULTIPLY, left * right),
        ("BMUL_high", S.MULTIPLY,
         z3.Extract(width - 1, width - word, left * right)),
        ("BMUL_high_ext", S.MULTIPLY,
         z3.Extract(width - 1, width - word,
                    z3.ZeroExt(width - word, z3.Extract(word - 1, 0, left))
                    * z3.ZeroExt(width - word,
                                 z3.Extract(word - 1, 0, right)))),
        ("BAND", S.BITWISE, left & right),
        ("BOR", S.BITWISE, left | right),
        ("BXOR", S.BITWISE, left ^ right),
        ("BNOT", S.BITWISE, ~left),
        ("BSHL", S.SHIFT_ROTATE, left << right),
        ("BLSHR", S.SHIFT_ROTATE, z3.LShR(left, right)),
        ("BASHR", S.SHIFT_ROTATE, left >> right),
        ("ROTATE_LEFT", S.SHIFT_ROTATE, z3.RotateLeft(left, 3)),
        ("ROTATE_RIGHT", S.SHIFT_ROTATE, z3.RotateRight(left, 3)),
        ("EXT_ROTATE_LEFT", S.SHIFT_ROTATE,
         z3.RotateLeft(left, right)),
        ("ULT", S.COMPARE, z3.If(z3.ULT(left, right),
                                 z3.BitVecVal(1, 8),
                                 z3.BitVecVal(0, 8))),
        ("ULEQ", S.COMPARE, z3.If(z3.ULE(left, right),
                                  z3.BitVecVal(1, 8),
                                  z3.BitVecVal(0, 8))),
        ("UGT", S.COMPARE, z3.If(z3.UGT(left, right),
                                 z3.BitVecVal(1, 8),
                                 z3.BitVecVal(0, 8))),
        ("SLT", S.COMPARE, z3.If(left < right, z3.BitVecVal(1, 8),
                                 z3.BitVecVal(0, 8))),
        ("SLEQ", S.COMPARE, z3.If(left <= right, z3.BitVecVal(1, 8),
                                  z3.BitVecVal(0, 8))),
        ("SGT", S.COMPARE, z3.If(left > right, z3.BitVecVal(1, 8),
                                 z3.BitVecVal(0, 8))),
        ("EQ", S.COMPARE, z3.If(left == right, z3.BitVecVal(1, 8),
                                z3.BitVecVal(0, 8))),
        ("ITE", S.BITWISE,
         z3.Extract(word - 1, 0, z3.If(narrow == z3.BitVecVal(0, word),
                                       left, right))),
        ("EXTRACT_low", S.WIDEN, z3.Extract(word - 1, 0, left)),
        ("EXTRACT_high", S.WIDEN,
         z3.Extract(width - 1, width - word, left)),
        ("ZERO_EXT", S.WIDEN,
         z3.Extract(word - 1, 0, z3.ZeroExt(width, left))),
        ("SIGN_EXT", S.WIDEN,
         z3.Extract(width - 1, width - word,
                    z3.SignExt(width, left))),
        ("CONCAT", S.WIDEN,
         z3.Extract(width - 1, width - word,
                    z3.Concat(narrow, left))),
    ]
    if with_divider:
        rows.append(("BUDIV", S.DIVIDE, z3.UDiv(left, right)))
        rows.append(("BUREM", S.DIVIDE, z3.URem(left, right)))
        rows.append(("BSDIV", S.DIVIDE, left / right))
        rows.append(("BSREM", S.DIVIDE, z3.SRem(left, right)))
    return rows


def narrowed(term, word):
    """the obligation is posed at the ANSWER the target could hold: a
    term wider than the word is compared on its low word, because a
    wider answer is a question about the arrival contract and not about
    the schema."""
    if not z3.is_bv(term):
        return term
    if term.size() <= word:
        return term
    return z3.Extract(word - 1, 0, term)


def one_row(name, schema, term, word):
    posed = narrowed(term, word)
    started = time.time()
    try:
        built, used, instances = S.lower(posed, word)
    except S.Refused as refusal:
        return {"name": name, "schema": schema, "outcome": "REFUSED",
                "detail": "%s: %s" % (refusal.cause, refusal.detail),
                "seconds": round(time.time() - started, 3),
                "schemas": [], "dag": None, "unfolded": None}
    dag = len(set(walk_ids(built)))
    unfolded = S.unfolded_size(built, 4000000)
    solver = z3.Solver()
    solver.set("timeout", CEILING_MS)
    solver.add(posed != built)
    answer = solver.check()
    outcome = "UNDECIDED"
    detail = str(answer)
    if answer == z3.unsat:
        outcome = "PROVED"
        detail = "z3 found no input at which the two differ"
    elif answer == z3.sat:
        outcome = "DISPROVED"
        detail = str(solver.model())[:200]
    return {"name": name, "schema": schema, "outcome": outcome,
            "detail": detail, "seconds": round(time.time() - started, 3),
            "schemas": used, "dag": dag, "unfolded": unfolded}


def walk_ids(term, seen=None):
    if seen is None:
        seen = []
    stack = [term]
    visited = set()
    while stack:
        here = stack.pop()
        key = here.get_id()
        if key in visited:
            continue
        visited.add(key)
        seen.append(key)
        for index in range(here.num_args()):
            stack.append(here.arg(index))
            continue
        continue
    return seen


def run(pairs, with_divider):
    say("| width | word | z3 kind | schema | outcome | DAG | unfolded | s |")
    say("|---|---|---|---|---|---|---|---|")
    tally = {}
    failures = []
    for width, word in pairs:
        for name, schema, term in obligations(width, word, with_divider):
            row = one_row(name, schema, term, word)
            tally[row["outcome"]] = tally.get(row["outcome"], 0) + 1
            say("| %d | %d | %s | %s | %s | %s | %s | %s |"
                % (width, word, name, schema, row["outcome"],
                   row["dag"], row["unfolded"], row["seconds"]))
            if row["outcome"] not in ("PROVED",):
                failures.append((width, word, row))
            check_memory("%s at %d/%d" % (name, width, word))
            continue
        continue
    say("")
    say("| outcome | rows |")
    say("|---|---|")
    for outcome in sorted(tally):
        say("| %s | %d |" % (outcome, tally[outcome]))
        continue
    if failures:
        say("")
        say("the rows that did not prove, LITERAL:")
        for width, word, row in failures:
            say("  %d/%d %s (%s): %s -- %s"
                % (width, word, row["name"], row["schema"],
                   row["outcome"], row["detail"]))
            continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    return len(failures)


def main(argv):
    what = "narrow"
    if len(argv) > 1:
        what = argv[1]
    if what == "narrow":
        # the schemas at widths a solver can answer whole, so a defect
        # in one shows as a counterexample and not as a timeout
        return run([(8, 4), (12, 4), (16, 8), (24, 8)], True)
    if what == "wide":
        # the widths this pipeline actually meets, divider excluded:
        # its term is measured in `size`, not put to a solver
        return run([(65, 64), (96, 64), (128, 64)], False)
    if what == "divider":
        return run([(32, 16), (32, 8)], True)
    if what == "size":
        say("| width | word | the divider's DAG | its UNFOLDED size |")
        say("|---|---|---|---|")
        for width, word in [(8, 4), (16, 8), (24, 8), (32, 16),
                            (65, 64), (128, 64)]:
            left, right = a_and_b(width, word)
            built, _used, _rows = S.lower(
                narrowed(z3.UDiv(left, right), word), word)
            dag = len(set(walk_ids(built)))
            unfolded = S.unfolded_size(built, None)
            say("| %d | %d | %d | %d |" % (width, word, dag, unfolded))
            check_memory("divider at %d/%d" % (width, word))
            continue
        say("")
        say("peak resident: %d kB" % peak_kb())
        return 0
    raise SystemExit("unknown: %s" % what)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
