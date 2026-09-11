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
  check_constructions.py census             every (kind, width) the two stores use
  check_constructions.py store [<i> <n>]    the census posed, part i of n
  check_constructions.py store_rest [<i> <n>]
                                            the instances no Lean lemma closed
  check_constructions.py one <mode> <i> <n> <entry> <shape>
                                            ONE obligation, in a process of
                                            its own, printed as one json line
  check_constructions.py float <mode>       the float kinds: tiny / store

Coding discipline: no compound one-liner statements.
"""

import json
import os
import resource
import subprocess
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

Z3_MEMORY_MB = 4096
"""the solver's OWN memory bound, under this task's 6 GB.

MEASURED, lane `t4_l10` step [5/6]: one obligation -- the multiplier at
128 bits over a word of 128 -- took 218.984 s against a ceiling of
30,000 ms and 1,236,272 kB resident.  z3's `timeout` is checked between
propagations and not during bit-blasting, so a wide multiply overshoots
it; nothing here raises the ceiling, and the seconds ACTUALLY TAKEN are
what the row records.  What this bound does is keep a solver that grows
past the task's own memory from being stopped by the operating system
with no row: z3 answers `unknown` with reason `memout`, which is an
UNDECIDED row with a cause."""

z3.set_param("memory_max_size", Z3_MEMORY_MB)


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


def wiring_producing(width, word):
    """the WIRING obligations whose ANSWER is exactly `width` bits.

    `wiring_obligations` above states its rows by the width of the
    SOURCE, which is the shape a ladder of doubling widths wants; the
    proof table is keyed by the width of the ANSWER, because that is
    what `build.node_width` reads off the node the render constructed.
    So this function states the same mechanism the other way round: a
    narrowing out of twice the width at three offsets (the low slice,
    the high slice and one that lines up with no limb), a joining of two
    halves, the two widenings from a half, and the conditional."""
    out = []
    source = 2 * width
    wide = z3.BitVec("a", source)
    out.append((B.WIRING, z3.Extract(width - 1, 0, wide),
                "extract_from%d_h%d_l0" % (source, width - 1)))
    out.append((B.WIRING, z3.Extract(source - 1, width, wide),
                "extract_from%d_h%d_l%d" % (source, source - 1, width)))
    if width > 2:
        out.append((B.WIRING, z3.Extract(width + 2, 3, wide),
                    "extract_from%d_h%d_l3" % (source, width + 2)))
    half = width // 2
    if half >= 1:
        piece = z3.BitVec("b", half)
        other = z3.BitVec("c", width - half)
        out.append((B.WIRING, z3.Concat(other, piece),
                    "concat_%d_%d" % (width - half, half)))
        out.append((B.WIRING, z3.ZeroExt(width - half, piece),
                    "extend_zero_from%d_t%d" % (half, width)))
        out.append((B.WIRING, z3.SignExt(width - half, piece),
                    "extend_sign_from%d_t%d" % (half, width)))
    left = z3.BitVec("d", width)
    right = z3.BitVec("e", width)
    out.append((B.CONDITIONAL, z3.If(z3.Bool("t"), left, right),
                "conditional_w%d" % width))
    return out


THE_FLOAT_FORMATS = {16: (5, 11), 32: (8, 24), 64: (11, 53),
                     79: (15, 64), 80: (15, 64), 128: (15, 113)}
"""the (exponent bits, significand bits) of each float width the stores
carry.  79 is z3's own `FPSort(15, 64)`, which is what the reference
gives an x87 value -- IEEE's double-extended without its explicit
integer bit."""


def obligations_of_kind(kind, width, word):
    """every obligation of ONE operation kind whose proof row would be
    keyed (kind, width, word) -- which is how the render looks one up."""
    if kind in (B.WIRING, B.CONDITIONAL):
        out = []
        for row in wiring_producing(width, word):
            if row[0] == kind:
                out.append(row)
            continue
        return out
    if kind in (B.FLOAT_ARITHMETIC, B.FLOAT_COMPARE, B.FLOAT_CLASS,
                B.FLOAT_CONVERT, B.FLOAT_WIRING):
        format_of = THE_FLOAT_FORMATS.get(width)
        if format_of is None:
            return []
        out = []
        for row in float_obligations(format_of[0], format_of[1]):
            if row[0] == kind:
                out.append(row)
            continue
        return out
    out = []
    for row in obligations_at(width, word):
        if row[0] == kind:
            out.append(row)
        continue
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
    """one obligation put to z3 at the brief's ceiling.

    THE ROW CARRIES ITS WIDTH, and the width is `build.node_width`'s --
    the same function the render keys what it CONSTRUCTED by -- so the
    proof table can be looked up by (kind, width, word) and answer."""
    if bindings is None:
        bindings = {}
    row = {"kind": kind, "shape": shape, "word": word,
           "width": B.node_width(node)}
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
    try:
        solver.add(left != built)
        answer = solver.check()
    except Exception as problem:                              # noqa: BLE001
        # THE SOLVER'S OWN MEMORY BOUND, ANSWERED.  z3 raises
        # `Z3Exception: out of memory` at `memory_max_size` and its C++
        # side then calls `terminate` if nothing catches it: lane
        # `t4_l15` part 1 was ABORTED that way (exit 134, core dumped)
        # and lost the two rows it had.  Caught, it is an UNDECIDED row
        # with the solver's own sentence on it.
        row["outcome"] = "UNDECIDED"
        row["cause"] = "the solver stopped: %s" % problem
        row["solver_memory_bound_mb"] = Z3_MEMORY_MB
        row["seconds"] = round(time.time() - started, 3)
        row["solver_timeout_ms"] = CEILING_MS
        return row
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
    say("| kind | shape | width | word | outcome | nodes | seconds | "
        "note |")
    say("|---|---|---|---|---|---|---|---|")
    for width, word in pairs:
        for kind, node, shape in obligations_at(width, word):
            index = index + 1
            row = pose(kind, node, shape, word)
            rows.append(row)
            counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
            say("| %s | %s | %d | %d | %s | %s | %s | %s |"
                % (kind, shape, row["width"], word, row["outcome"],
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
            say("| %s | %s | %d | %d | %s | %s | %s | %s |"
                % (kind, name, row["width"], word, row["outcome"],
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


# ==================================================================
# section 3a: the census -- which (kind, width) the stores actually use
# ==================================================================

CENSUS = os.path.join(HERE, "kind_census.json")


def walk_kinds(term, counts, seen):
    """one term walked, every node that HAS a construction counted at
    the width its proof row is keyed by.

    This is the brief's own definition of `operation kind` -- "every
    kind that occurs, with the widths it occurs at, counted" -- read
    through `build.kind_of`, which is a mapping from z3's own
    declaration kind, and `build.node_width`."""
    stack = [term]
    while stack:
        node = stack.pop()
        key = node.get_id()
        if key in seen:
            continue
        seen.add(key)
        kind = B.kind_of(node)
        if kind is not None:
            width = B.node_width(node)
            if width > 0:
                label = "%s|%d" % (kind, width)
                counts[label] = counts.get(label, 0) + 1
        for index in range(node.num_args()):
            stack.append(node.arg(index))
            continue
        continue
    return counts


def census_x86(counts):
    EMULATION = os.path.normpath(os.path.join(HERE, "..", ".."))
    sys.path.insert(0, os.path.join(EMULATION, "handful"))
    sys.path.insert(0, os.path.join(EMULATION, "autopoly"))
    import handful as H
    import model_table as MTAB
    MTAB._install_gpr_widths()
    cells = H.read_json(os.path.join(EMULATION, "autopoly",
                                     "autopoly5_cells.json"))
    places = 0
    for record in cells["asked"]:
        asked = (record["asked"]["mnem"], record["asked"]["shape"],
                 record["asked"]["key_width"])
        try:
            held_list = H.cell_inputs(cells, asked)
        except Exception as problem:                          # noqa: BLE001
            say("  REFUSED at %s: %s: %s"
                % (asked, type(problem).__name__, problem))
            continue
        for held in held_list:
            for place in held.get("places") or []:
                term = place.get("term")
                if term is None:
                    continue
                places = places + 1
                walk_kinds(term, counts, set())
                continue
            continue
        check_memory("%s" % (asked,))
        continue
    return places


def census_riscv(counts):
    REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                         "..", ".."))
    RV = os.path.join(REPO, "Research", "oracle", "riscv")
    sys.path.insert(0, RV)
    sys.path.insert(0, os.path.join(REPO, "Research", "op_pipeline"))
    import rv_loop as RL
    terms, _operands = RL.riscv_terms(os.path.join(RV,
                                                   "model_table_rv.json"))
    for key in terms:
        walk_kinds(terms[key], counts, set())
        continue
    return len(terms)


def census_command():
    """every (operation kind, width) the two architectures' stores use,
    counted.  It is what `store` below poses, so the obligations are the
    population's and not a list somebody chose."""
    counts = {}
    x86_places = census_x86(counts)
    say("x86 written places walked: %d" % x86_places)
    rv_places = census_riscv(counts)
    say("RISC-V written places walked: %d" % rv_places)
    say("")
    rows = []
    for label in sorted(counts):
        kind, width = label.rsplit("|", 1)
        rows.append({"kind": kind, "width": int(width),
                     "nodes": counts[label]})
        continue
    rows.sort(key=lambda row: (B.KIND_ORDER.index(row["kind"])
                               if row["kind"] in B.KIND_ORDER else 99,
                               row["width"]))
    say("| operation kind | width | nodes over both architectures |")
    say("|---|---|---|")
    for row in rows:
        say("| %s | %d | %d |" % (row["kind"], row["width"],
                                  row["nodes"]))
        continue
    say("")
    say("distinct (kind, width): %d" % len(rows))
    document = {
        "meta": {"what": "every (operation kind, width) the x86 and "
                         "riscv64 stores use, keyed as "
                         "`build.node_width` keys a proof row",
                 "x86_places": x86_places, "riscv_places": rv_places,
                 "peak_kb": peak_kb()},
        "rows": rows,
    }
    handle = open(CENSUS, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("written: %s" % CENSUS)
    say("peak resident: %d kB" % check_memory("census"))
    return 0


# ==================================================================
# section 3b: the census posed
# ==================================================================

def instances_the_lemma_closed():
    """every (kind, width, word) a Lean theorem closed, off
    `lemmas_t4*.json`.

    THE BRIEF'S OWN ORDER: "proved ONCE per kind ... as a Lean lemma ...;
    where a lemma does not close in the task's budget, the instantiation
    is proved by z3 at every width the store uses".  So z3 is the
    fallback and is not asked where the lemma already answered."""
    import glob
    out = set()
    for path in sorted(glob.glob(os.path.join(HERE, "lemmas_t4*.json"))):
        handle = open(path)
        document = json.load(handle)
        handle.close()
        for row in document.get("rows") or []:
            if row.get("outcome") != "PROVED_BY_LEAN":
                continue
            out.add((row["kind"], int(row["width"]), int(row["word"])))
            continue
        continue
    return out


def the_plan_for(mode):
    """the plan one mode poses, DETERMINISTIC, so the parent and the
    child derive the same list from the same files."""
    plan = store_plan()
    if mode != "store_rest":
        return plan
    closed = instances_the_lemma_closed()
    kept = []
    for entry in plan:
        key = (entry["kind"], entry["width"], entry["word"])
        if key in closed:
            continue
        kept.append(entry)
        continue
    return kept


def store_plan():
    """one (kind, width, word) per obligation the census names.

    THE WORD IS POSED ONCE WHERE THE CONSTRUCTION DOES NOT DEPEND ON IT.
    `build.unit_for` gives a value of `n` bits a unit of `n` where
    `n <= W` and of `W` where it is wider, so for every width at or
    under 64 the construction over a word of 64 and over a word of 128
    is the SAME term; it is posed once, at 64, and the row it writes is
    recorded for both words with that reason on it.  Above 64 the two
    differ and both are posed."""
    handle = open(CENSUS)
    document = json.load(handle)
    handle.close()
    plan = []
    for row in document["rows"]:
        width = int(row["width"])
        kind = row["kind"]
        words = [64]
        if width > 64:
            words.append(128)
        for word in words:
            plan.append({"kind": kind, "width": width, "word": word,
                         "covers": [64, 128] if width <= 64 else [word]})
            continue
        continue
    return plan


CAUSE_THE_CHILD_STOPPED = ("the solver's own memory bound stopped the "
                           "process posing this obligation, so what the "
                           "row records is the bound and not the "
                           "question")


def one_in_a_child(mode, part, of, entry_index, shape_index):
    """ONE obligation posed in a process of its own.

    WHY EACH OBLIGATION GETS ITS OWN PROCESS, and it is measured rather
    than anticipated: z3's `memory_max_size` raises once and then
    REFUSES EVERYTHING AFTER IT in the same process.  Lane `t4_l15` part
    3 shows what that does to a measurement -- after the divider at 32
    bits exhausted the bound, `fp_neg` at 79 bits came back UNDECIDED in
    0.0 s, and the same obligation at the tiny formats is PROVED (lane
    `t4_l5`).  Those rows would say the solver could not decide when
    what happened is that the solver was already out of memory.  One
    process per obligation is the only way a row means what it says."""
    command = [sys.executable, os.path.abspath(__file__), "one", mode,
               "%d" % part, "%d" % of, "%d" % entry_index,
               "%d" % shape_index]
    started = time.time()
    answer = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    printed = answer.stdout.decode("utf-8", "replace").strip()
    for line in printed.splitlines():
        if not line.startswith("{"):
            continue
        try:
            return json.loads(line)
        except ValueError:
            continue
        continue
    return {"outcome": "UNDECIDED", "cause": CAUSE_THE_CHILD_STOPPED,
            "child_exit": answer.returncode,
            "child_stderr": answer.stderr.decode("utf-8",
                                                 "replace")[-400:],
            "seconds": round(time.time() - started, 3)}


def obligation_rows(plan):
    """(entry index, shape index, entry, kind, shape) for every
    obligation the plan carries, in one deterministic order -- the order
    the child re-derives from the same census."""
    out = []
    for entry_index, entry in enumerate(plan):
        posed = obligations_of_kind(entry["kind"], entry["width"],
                                    entry["word"])
        if not posed:
            out.append((entry_index, -1, entry, entry["kind"], "--"))
            continue
        for shape_index, item in enumerate(posed):
            out.append((entry_index, shape_index, entry, item[0],
                        item[2]))
            continue
        continue
    return out


def one_command(mode, part, of, entry_index, shape_index):
    """the child: ONE obligation, posed, printed as one json line."""
    plan = the_plan_for(mode)
    mine = []
    for index, entry in enumerate(plan):
        if index % of == (part - 1):
            mine.append(entry)
        continue
    entry = mine[entry_index]
    posed = obligations_of_kind(entry["kind"], entry["width"],
                                entry["word"])
    item = posed[shape_index]
    bindings = None
    if len(item) == 4:
        kind, node, shape, bindings = item
    else:
        kind, node, shape = item
    row = pose(kind, node, shape, entry["word"], bindings)
    sys.stdout.write(json.dumps(row, sort_keys=True) + "\n")
    sys.stdout.flush()
    return 0


def run_plan(plan, label, out_path, mode="store", part=1, of=1):
    rows = []
    counts = {}
    total = len(plan)
    say("| kind | shape | width | word | outcome | nodes | seconds | "
        "note |")
    say("|---|---|---|---|---|---|---|---|")
    for entry_index, shape_index, entry, kind, shape in \
            obligation_rows(plan):
        if shape_index < 0:
            row = {"kind": entry["kind"], "width": entry["width"],
                   "word": entry["word"], "shape": "--",
                   "outcome": "NO_OBLIGATION_STATED",
                   "covers": entry["covers"],
                   "cause": "this file states no obligation of this "
                            "kind at this width",
                   "seconds": 0.0}
        else:
            got = one_in_a_child(mode, part, of, entry_index,
                                 shape_index)
            row = dict(got)
            row.setdefault("kind", kind)
            row.setdefault("shape", shape)
            row.setdefault("width", entry["width"])
            row.setdefault("word", entry["word"])
            row["covers"] = entry["covers"]
            row["census_width"] = entry["width"]
        rows.append(row)
        counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
        say("| %s | %s | %s | %s | %s | %s | %s | %s |"
            % (row["kind"], row["shape"], row["width"], row["word"],
               row["outcome"], row.get("nodes", "--"),
               row.get("seconds"), note_of(row)))
        check_memory("%s" % row["shape"])
        # WRITTEN AFTER EVERY OBLIGATION.  One obligation here can take
        # minutes -- the multiplier at 128 bits took 223.29 s against a
        # 30,000 ms ceiling, and a divider at 32 grows to gigabytes
        # before the solver's own memory bound answers -- so a part cut
        # by its lane's wall clock leaves every row it already has.
        write_plan_rows(out_path, rows, label, counts, total)
        continue
    say("")
    say("| outcome | rows |")
    say("|---|---|")
    for outcome in sorted(counts):
        say("| %s | %d |" % (outcome, counts[outcome]))
        continue
    say("")
    say("peak resident: %d kB" % peak_kb())
    write_plan_rows(out_path, rows, label, counts, total)
    say("written: %s" % out_path)
    return 0


def write_plan_rows(out_path, rows, label, counts, total):
    document = {
        "meta": {"what": "every construction the census names, put to "
                         "z3 on its own",
                 "label": label, "ceiling_ms": CEILING_MS,
                 "peak_kb": peak_kb(), "counts": counts,
                 "plan_entries": total},
        "rows": rows,
    }
    handle = open(out_path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    return


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
    if what == "census":
        return census_command()
    if what == "one":
        return one_command(argv[2], int(argv[3]), int(argv[4]),
                           int(argv[5]), int(argv[6]))
    if what in ("store", "store_rest"):
        plan = the_plan_for(what)
        part = 1
        of = 1
        if len(argv) > 3:
            part = int(argv[2])
            of = int(argv[3])
        mine = []
        for index, entry in enumerate(plan):
            if index % of == (part - 1):
                mine.append(entry)
            continue
        say("this run poses %d (kind, width, word) obligations; this "
            "part is %d of %d and carries %d of them"
            % (len(plan), part, of, len(mine)))
        say("")
        return run_plan(mine, "%s %d of %d" % (what, part, of),
                        os.path.join(HERE,
                                     "constructions_%s_%d_of_%d.json"
                                     % (what, part, of)),
                        what, part, of)
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
