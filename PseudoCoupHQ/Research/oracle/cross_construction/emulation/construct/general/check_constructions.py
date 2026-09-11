#!/usr/bin/env python3
"""check_constructions.py -- EVERY CONSTRUCTION PUT TO z3 ON ITS OWN,
before any of them touches a cell: is the construction the operation it
replaces, at this width, over this word?

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`,
section 2 item 1 -- "per operation kind: constructed / proved by lemma /
proved by z3 / undecided / refused, with the width and the target".

THE OBLIGATION, one sentence: for one operation kind at one width `n`
over one word `W`, z3 is asked whether the construction and z3's OWN
operator can differ on any input, and the three answers are PROVED (no
input differs), DISPROVED (here is one) and UNDECIDED (the ceiling ran
out).  A DISPROVED row is a defect in this task's own construction and
is never worked around.

THE CEILING is the brief's hard 30 seconds and is never raised.

usage:
  check_constructions.py smoke              a handful at tiny widths
  check_constructions.py narrow             every kind at widths a solver answers
  check_constructions.py store              every (kind, width) the stores use
  check_constructions.py float <mode>       the float kinds: tiny / store

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import build as B                                                # noqa: E402
import softfloat as SF                                           # noqa: E402

CEILING_MS = 30000
ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_T4"


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


# ==================================================================
# section 1: the obligations, built from z3's own operators
# ==================================================================

BINARY = [
    (B.ADD, lambda a, b: a + b),
    (B.SUBTRACT, lambda a, b: a - b),
    (B.MULTIPLY, lambda a, b: a * b),
    (B.DIVIDE_UNSIGNED, lambda a, b: z3.UDiv(a, b)),
    (B.REMAINDER_UNSIGNED, lambda a, b: z3.URem(a, b)),
    (B.DIVIDE_SIGNED, lambda a, b: a / b),
    (B.REMAINDER_SIGNED, lambda a, b: z3.SRem(a, b)),
    (B.MODULO_SIGNED, lambda a, b: a % b),
    (B.SHIFT_LEFT, lambda a, b: a << b),
    (B.SHIFT_RIGHT_LOGICAL, lambda a, b: z3.LShR(a, b)),
    (B.SHIFT_RIGHT_ARITHMETIC, lambda a, b: a >> b),
    (B.BITWISE, lambda a, b: a & b),
    (B.BITWISE, lambda a, b: a | b),
    (B.BITWISE, lambda a, b: a ^ b),
    (B.ROTATE, lambda a, b: z3.RotateLeft(a, b)),
    (B.ROTATE, lambda a, b: z3.RotateRight(a, b)),
]

UNARY = [
    (B.COMPLEMENT, lambda a: ~a),
    (B.NEGATE, lambda a: -a),
]

TRUTHS = [
    (B.COMPARE_UNSIGNED, lambda a, b: z3.ULT(a, b)),
    (B.COMPARE_UNSIGNED, lambda a, b: z3.ULE(a, b)),
    (B.COMPARE_UNSIGNED, lambda a, b: z3.UGT(a, b)),
    (B.COMPARE_UNSIGNED, lambda a, b: z3.UGE(a, b)),
    (B.COMPARE_SIGNED, lambda a, b: a < b),
    (B.COMPARE_SIGNED, lambda a, b: a <= b),
    (B.COMPARE_SIGNED, lambda a, b: a > b),
    (B.COMPARE_SIGNED, lambda a, b: a >= b),
    (B.EQUALITY, lambda a, b: a == b),
    (B.EQUALITY, lambda a, b: a != b),
]


def wiring_obligations(width, word):
    """the wiring kinds, whose shapes are the offsets they are used
    at."""
    out = []
    left = z3.BitVec("a", width)
    right = z3.BitVec("b", width)
    if width > 1:
        low = width // 2
        out.append((B.WIRING, z3.Extract(width - 1, low, left),
                    "extract_w%d_h%d_l%d" % (width, width - 1, low)))
        out.append((B.WIRING, z3.Extract(low - 1, 0, left),
                    "extract_w%d_h%d_l0" % (width, low - 1)))
    out.append((B.WIRING, z3.Concat(left, right),
                "concat_w%d_w%d" % (width, width)))
    out.append((B.WIRING, z3.ZeroExt(width, left),
                "extend_zero_w%d_t%d" % (width, 2 * width)))
    out.append((B.WIRING, z3.SignExt(width, left),
                "extend_sign_w%d_t%d" % (width, 2 * width)))
    out.append((B.CONDITIONAL, z3.If(z3.Bool("t"), left, right),
                "conditional_w%d" % width))
    return out


def obligations_at(width, word):
    """every obligation this file states at one (width, word)."""
    out = []
    left = z3.BitVec("a", width)
    right = z3.BitVec("b", width)
    for kind, make in BINARY:
        try:
            node = make(left, right)
        except Exception:
            continue
        out.append((kind, node, "%s_w%d" % (node.decl().name(), width)))
        continue
    for kind, make in UNARY:
        node = make(left)
        out.append((kind, node, "%s_w%d" % (node.decl().name(), width)))
        continue
    for kind, make in TRUTHS:
        node = make(left, right)
        out.append((kind, node, "%s_w%d" % (node.decl().name(), width)))
        continue
    out.extend(wiring_obligations(width, word))
    return out


def float_obligations(ebits, sbits):
    """the float kinds at one format, over z3's own float operators.

    THE OPERANDS ARE BIT PATTERNS AND NOT FLOAT SYMBOLS, and the reason
    is a property of z3 and not a convenience: `fp.to_ieee_bv` of a
    not-a-number is left UNSPECIFIED, so an obligation that reads a
    float symbol's bits can be answered `sat` by two not-a-numbers with
    different payloads and says nothing about the construction.  A bit
    pattern read as a float (`fpBVToFP`) is total, and the answer is
    compared AS A FLOAT, where every not-a-number is one value.

    `bindings` says which Value the construction is handed for each
    float operand: the bit pattern itself, which is what it holds."""
    sort = z3.FPSort(ebits, sbits)
    width = ebits + sbits
    left_bits = z3.BitVec("a", width)
    right_bits = z3.BitVec("b", width)
    left = z3.fpBVToFP(left_bits, sort)
    right = z3.fpBVToFP(right_bits, sort)
    rounding = z3.RNE()
    bindings = {left.get_id(): left_bits, right.get_id(): right_bits}
    out = []
    out.append((B.FLOAT_WIRING, z3.fpNeg(left), "fp_neg"))
    out.append((B.FLOAT_WIRING, z3.fpAbs(left), "fp_abs"))
    out.append((B.FLOAT_CLASS, z3.fpIsNaN(left), "fp_isNaN"))
    out.append((B.FLOAT_CLASS, z3.fpIsInf(left), "fp_isInfinite"))
    out.append((B.FLOAT_CLASS, z3.fpIsZero(left), "fp_isZero"))
    out.append((B.FLOAT_CLASS, z3.fpIsNormal(left), "fp_isNormal"))
    out.append((B.FLOAT_CLASS, z3.fpIsSubnormal(left),
                "fp_isSubnormal"))
    out.append((B.FLOAT_COMPARE, z3.fpEQ(left, right), "fp_eq"))
    out.append((B.FLOAT_COMPARE, z3.fpLT(left, right), "fp_lt"))
    out.append((B.FLOAT_COMPARE, z3.fpLEQ(left, right), "fp_leq"))
    out.append((B.FLOAT_COMPARE, z3.fpGT(left, right), "fp_gt"))
    out.append((B.FLOAT_COMPARE, z3.fpGEQ(left, right), "fp_geq"))
    out.append((B.FLOAT_ARITHMETIC, z3.fpAdd(rounding, left, right),
                "fp_add"))
    out.append((B.FLOAT_ARITHMETIC, z3.fpSub(rounding, left, right),
                "fp_sub"))
    out.append((B.FLOAT_ARITHMETIC, z3.fpMul(rounding, left, right),
                "fp_mul"))
    out.append((B.FLOAT_ARITHMETIC, z3.fpDiv(rounding, left, right),
                "fp_div"))
    integer = z3.BitVec("k", ebits + sbits)
    out.append((B.FLOAT_CONVERT, z3.fpSignedToFP(rounding, integer,
                                                 sort),
                "to_fp_signed"))
    out.append((B.FLOAT_CONVERT, z3.fpToFPUnsigned(rounding, integer,
                                                   sort),
                "to_fp_unsigned"))
    made = []
    for kind, node, shape in out:
        made.append((kind, node, shape, bindings))
        continue
    return made


# ==================================================================
# section 2: one obligation, posed
# ==================================================================

def value_for(node, word, bindings):
    """the Value this file hands a construction for one argument of the
    obligation: the bit pattern a float operand stands for, a
    bit-vector split into limbs, a truth value, a rounding mode passed
    through."""
    if z3.is_fprm(node):
        return B.Value("other", passthrough=node)
    found = bindings.get(node.get_id())
    if found is not None:
        return B.split_value(found, word)
    if z3.is_fp(node):
        bits = z3.fpToIEEEBV(node)
        return B.split_value(bits, word)
    if node.sort().kind() == z3.Z3_BOOL_SORT:
        return B.Value("bool", truth=node)
    return B.split_value(node, word)


def constructed(node, word, bindings):
    children = []
    for index in range(node.num_args()):
        children.append(value_for(node.arg(index), word, bindings))
        continue
    return B.build(node, children, word)


def pose(kind, node, shape, word, bindings=None):
    """one obligation put to z3 at the brief's ceiling."""
    if bindings is None:
        bindings = {}
    row = {"kind": kind, "shape": shape, "word": word}
    started = time.time()
    try:
        made = constructed(node, word, bindings)
    except B.Refused as refusal:
        row["outcome"] = "REFUSED"
        row["cause"] = refusal.cause
        row["detail"] = refusal.detail
        row["seconds"] = round(time.time() - started, 3)
        return row
    except Exception as problem:
        row["outcome"] = "REFUSED"
        row["cause"] = "the construction raised"
        row["detail"] = "%s: %s" % (type(problem).__name__, problem)
        row["seconds"] = round(time.time() - started, 3)
        return row
    built = B.joined(made)
    row["nodes"] = B.node_count(built, 400000)
    left = node
    if z3.is_fp(node):
        # THE ANSWER IS COMPARED AS A FLOAT, where z3's own `=` holds
        # every not-a-number to be one value and keeps the two zeros
        # apart -- which is the question "is this the operation", and
        # `fp.to_ieee_bv` is not, because it is unspecified at a
        # not-a-number.
        built = z3.fpBVToFP(built, node.sort())
    solver = z3.Solver()
    solver.set("timeout", CEILING_MS)
    solver.add(left != built)
    answer = solver.check()
    row["seconds"] = round(time.time() - started, 3)
    row["solver_timeout_ms"] = CEILING_MS
    if answer == z3.unsat:
        row["outcome"] = "PROVED"
        return row
    if answer == z3.sat:
        row["outcome"] = "DISPROVED"
        row["counterexample"] = str(solver.model())[:400]
        return row
    row["outcome"] = "UNDECIDED"
    return row


# ==================================================================
# section 3: the runs
# ==================================================================

def run(pairs, floats, label, out_path):
    rows = []
    counts = {}
    total = len(pairs) + len(floats)
    index = 0
    say("| kind | shape | word | outcome | nodes | seconds | note |")
    say("|---|---|---|---|---|---|---|")
    for width, word in pairs:
        for kind, node, shape in obligations_at(width, word):
            index = index + 1
            row = pose(kind, node, shape, word)
            rows.append(row)
            counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
            say("| %s | %s | %d | %s | %s | %s | %s |"
                % (kind, shape, word, row["outcome"],
                   row.get("nodes", "--"), row["seconds"],
                   note_of(row)))
            check_memory(shape)
            continue
        continue
    for ebits, sbits, word in floats:
        for kind, node, shape, bindings in float_obligations(ebits,
                                                             sbits):
            index = index + 1
            name = "%s_e%d_s%d" % (shape, ebits, sbits)
            row = pose(kind, node, name, word, bindings)
            rows.append(row)
            counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
            say("| %s | %s | %d | %s | %s | %s | %s |"
                % (kind, name, word, row["outcome"],
                   row.get("nodes", "--"), row["seconds"],
                   note_of(row)))
            check_memory(name)
            continue
        continue
    say("")
    say("| outcome | rows |")
    say("|---|---|")
    for outcome in sorted(counts):
        say("| %s | %d |" % (outcome, counts[outcome]))
    say("")
    say("peak resident: %d kB" % peak_kb())
    document = {
        "meta": {"what": "every construction put to z3 on its own",
                 "label": label, "ceiling_ms": CEILING_MS,
                 "peak_kb": peak_kb(),
                 "counts": counts},
        "rows": rows,
    }
    handle = open(out_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("written: %s" % out_path)
    return 0


def note_of(row):
    """the row's own cause or counterexample, so a REFUSED or DISPROVED
    row carries WHY on the same line."""
    if row["outcome"] == "REFUSED":
        return ("%s -- %s" % (row.get("cause", ""),
                              row.get("detail", "")))[:150]
    if row["outcome"] == "DISPROVED":
        return (row.get("counterexample") or "").replace("\n", " ")[:150]
    return ""


def widths_from(path):
    """every (kind, width) the stores use, off the census this task's
    lane 1 wrote."""
    handle = open(path)
    document = json.load(handle)
    handle.close()
    out = set()
    for entry in document["kinds"]:
        for width in entry["widths"]:
            number = int(width)
            if number > 0:
                out.add(number)
            continue
        continue
    return sorted(out)


def main(argv):
    what = argv[1] if len(argv) > 1 else "smoke"
    if what == "smoke":
        pairs = [(4, 4), (6, 4), (8, 8)]
        return run(pairs, [], "smoke",
                   os.path.join(HERE, "constructions_smoke.json"))
    if what == "narrow":
        pairs = [(4, 4), (6, 4), (8, 4), (8, 8), (9, 8), (12, 8),
                 (16, 8), (16, 16)]
        return run(pairs, [], "narrow",
                   os.path.join(HERE, "constructions_narrow.json"))
    if what == "store":
        widths = [8, 9, 16, 32, 33, 48, 56, 64, 65, 96, 128]
        pairs = []
        for width in widths:
            pairs.append((width, 64))
            pairs.append((width, 128))
            continue
        return run(pairs, [], "store",
                   os.path.join(HERE, "constructions_store.json"))
    if what == "float":
        mode = argv[2] if len(argv) > 2 else "tiny"
        if mode == "tiny":
            floats = [(3, 4, 64), (4, 5, 64)]
            name = "constructions_float_tiny.json"
        elif mode == "half":
            floats = [(5, 11, 64)]
            name = "constructions_float_half.json"
        else:
            floats = [(8, 24, 64), (11, 53, 64), (15, 64, 64),
                      (15, 64, 128)]
            name = "constructions_float_store.json"
        return run([], floats, "float " + mode,
                   os.path.join(HERE, name))
    say(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
