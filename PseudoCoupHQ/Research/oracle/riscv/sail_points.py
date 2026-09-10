#!/usr/bin/env python3
"""sail_points.py -- LEVEL 0 FOR RISC-V, THE TWO READINGS PUT AGAINST EACH
OTHER AT POINTS.

Node: hq.research.arch_unit_oracle.  Task rv1, brief section 3.

WHAT THIS FILE DOES, one sentence: for each instruction of the base
integer set, it runs the RATIFIED Sail model's own C simulator over a bare
metal program that executes that one instruction at many concrete inputs,
and it evaluates `riscv_reference.py`'s term for the same instruction at
the same inputs, so the two readings can be compared value by value.

THIS IS A CHECK AT POINTS, NOT AN EQUALITY.  Agreement at every point
sampled is evidence that the two readings compute the same mapping; it is
not a proof that they do.  The count of points is on every row.

THE HARNESS, exactly.  Per VARIANT -- one instruction text with concrete
registers and, where the form has one, a concrete immediate -- this file
writes an assembly file of this shape and nothing else:

    _start:  la s0, inputs ; la s1, results ; li s2, N
    loop:    ld a0, 0(s0)          the first input
             ld a1, 8(s0)          the second input
             <the instruction>     writing a2
             sd a2, 0(s1)          the output
             addi s0, s0, 16 ; addi s1, s1, 8 ; addi s2, s2, -1
             bnez s2, loop
             store 1 into tohost, then spin

The ELF is linked at 0x80000000, which is the reset address the
simulator's default configuration gives (lane 2 printed it); the
simulator finds `tohost` by symbol and stops when it is written; the
results are read back out of the region between `begin_signature` and
`end_signature` with `--test-signature`, which prints one 32-bit word per
line, low word of each 64-bit result first.

WHAT IS NOT CHECKED THIS WAY, said out loud rather than counted as
agreement:
  * `auipc` -- its second input is the program counter, and the harness
    cannot present a program counter as an input.
  * the loads, the stores, the branches and the jumps -- their effect is
    not a value in a register, so "one instruction between loads of its
    inputs and a store of its outputs" does not state them.  They are in
    the reference because a body needs them; they are refused by name
    here.
  * the floating-point family -- the brief's section 3 names the base
    integer set; the float instructions are in the reference because the
    handful's two float bodies spell them, and their check is a later
    task's.

usage:
  sail_points.py <out prefix> <work dir> [--points N] [--only MNEM,...]
"""

import json
import os
import random
import resource
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                # noqa: E402
import z3                                                   # noqa: E402


# THE MEMORY BOUND, stated as the law requires: this driver holds one
# variant's points and one z3 term at a time and streams the rest, so its
# appetite is the point list of one variant.  The ceiling is the brief's
# 6 GB and the abort is named.
MEMORY_CEILING_MB = 6144
ABORT_NAME = "ABORT_MEMORY_RV1"


def peak_rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check_memory(where):
    peak = peak_rss_mb()
    if peak > MEMORY_CEILING_MB:
        raise SystemExit("%s: peak RSS %.1f MB passed the %d MB ceiling "
                         "at %s" % (ABORT_NAME, peak, MEMORY_CEILING_MB,
                                    where))
    return peak


SIMULATOR = "/usr/local/bin/sail_riscv_sim"
CLANG = "clang"
RESET_ADDRESS = "0x80000000"

# the extensions the harness assembles for: the general set the psABI's
# `lp64d` names, plus Zicond, which is in the model's own default
# configuration (lane 2 printed its ISA string) and which clang 21 emits
# for the handful's select.
MARCH = "rv64gc_zicond"
MASK = (1 << 64) - 1

POINT_CAP = 20000

# `lui` reads no register, so one of its points is one immediate and one
# immediate is one assembled program.  This is the ceiling on how many are
# assembled; the cause is harness cost, and it is stated on the row.
LUI_VARIANTS = 400


# ------------------------------------------------------------------
# the points: the edges first, then random
# ------------------------------------------------------------------

def edge_values():
    """0, 1, -1, the extremes, and every power of two with its two
    neighbours -- the interval's critical points, one on each side."""
    seen = []
    def add(value):
        folded = value & MASK
        if folded not in seen:
            seen.append(folded)
    for base in (0, 1, 2, 3):
        add(base)
        add(-base)
    add((1 << 63))            # the most negative signed value
    add((1 << 63) - 1)        # the largest signed value
    add(MASK)                 # all ones
    for power in range(0, 64):
        value = 1 << power
        add(value - 1)
        add(value)
        add(value + 1)
    return seen


EDGES = edge_values()

IMMEDIATE_EDGES = [0, 1, -1, 2, -2, 4, -4, 8, -8, 15, -16, 255, -256,
                   1023, -1024, 2047, -2048, 1365, -1366, 512]

UPPER_IMMEDIATE_EDGES = [0, 1, 2, 3, 0x7FF, 0x800, 0x801, 0xFFF,
                         0x7FFFF, 0x80000, 0x80001, 0xFFFFF, 0xAAAAA,
                         0x55555, 0xFFFFE, 0x10000, 0x0FFFF]


def paired_points(count, seed):
    """the edge pairs first, then random pairs, up to `count`."""
    out = []
    for left in EDGES:
        for right in EDGES:
            out.append((left, right))
            if len(out) >= count:
                return out
    generator = random.Random(seed)
    while len(out) < count:
        out.append((generator.getrandbits(64), generator.getrandbits(64)))
    return out


def single_points(count, seed):
    out = list(EDGES)[:count]
    generator = random.Random(seed)
    while len(out) < count:
        out.append(generator.getrandbits(64))
    return out


# ------------------------------------------------------------------
# the variants: one instruction text per row of the check
# ------------------------------------------------------------------

DESTINATION = "a2"
FIRST = "a0"
SECOND = "a1"


def variants_of(mnemonic, points_per_mnemonic):
    """[(instruction text, [points])] for one mnemonic.

    A point is a pair (first input, second input); an instruction that
    reads one register gets the second input anyway and ignores it, which
    is what the harness does."""
    if mnemonic in RV.R_TYPE or mnemonic in RV.R_TYPE_W or \
            mnemonic in RV.MULTIPLY or mnemonic in RV.MULTIPLY_W or \
            mnemonic in RV.DIVIDE or mnemonic in RV.DIVIDE_W or \
            mnemonic in RV.CONDITIONAL_ZERO:
        text = "%s %s, %s, %s" % (mnemonic, DESTINATION, FIRST, SECOND)
        return [(text, paired_points(points_per_mnemonic, mnemonic))]
    if mnemonic in RV.I_TYPE or mnemonic in RV.I_TYPE_W:
        each = max(1, points_per_mnemonic // len(IMMEDIATE_EDGES))
        out = []
        for immediate in IMMEDIATE_EDGES:
            text = "%s %s, %s, %d" % (mnemonic, DESTINATION, FIRST,
                                      immediate)
            values = single_points(each, "%s%d" % (mnemonic, immediate))
            out.append((text, [(value, 0) for value in values]))
        return out
    if mnemonic in RV.SHIFT_I:
        each = max(1, points_per_mnemonic // 64)
        out = []
        for shift in range(64):
            text = "%s %s, %s, %d" % (mnemonic, DESTINATION, FIRST, shift)
            values = single_points(each, "%s%d" % (mnemonic, shift))
            out.append((text, [(value, 0) for value in values]))
        return out
    if mnemonic in RV.SHIFT_I_W:
        each = max(1, points_per_mnemonic // 32)
        out = []
        for shift in range(32):
            text = "%s %s, %s, %d" % (mnemonic, DESTINATION, FIRST, shift)
            values = single_points(each, "%s%d" % (mnemonic, shift))
            out.append((text, [(value, 0) for value in values]))
        return out
    if mnemonic == "lui":
        # the only input is the immediate, and the immediate is part of
        # the instruction, so a POINT here is one immediate and each
        # immediate needs its own program.  The edges first, then random
        # 20-bit values, capped at LUI_VARIANTS so the harness does not
        # assemble twenty thousand programs for twenty thousand points.
        immediates = list(UPPER_IMMEDIATE_EDGES)
        generator = random.Random("lui")
        while len(immediates) < min(LUI_VARIANTS, points_per_mnemonic):
            immediates.append(generator.getrandbits(20))
        out = []
        for immediate in immediates:
            text = "lui %s, %d" % (DESTINATION, immediate)
            out.append((text, [(0, 0)]))
        return out
    if mnemonic in RV.ADD_UNSIGNED_WORD or mnemonic in RV.FLOAT_SIGN_INJECT:
        first, second, destination, _mode = homes_of(mnemonic)
        text = "%s %s, %s, %s" % (mnemonic, destination, first, second)
        return [(text, paired_points(points_per_mnemonic, mnemonic))]
    if mnemonic in RV.BIT_SET_I:
        each = max(1, points_per_mnemonic // 64)
        out = []
        for shift in range(64):
            text = "%s %s, %s, %d" % (mnemonic, DESTINATION, FIRST, shift)
            values = single_points(each, "%s%d" % (mnemonic, shift))
            out.append((text, [(value, 0) for value in values]))
        return out
    if mnemonic == "c.mul":
        first, second, _destination, _mode = homes_of(mnemonic)
        text = "c.mul %s, %s" % (first, second)
        return [(text, paired_points(points_per_mnemonic, mnemonic))]
    if mnemonic == "c.zext.w":
        first, _second, _destination, _mode = homes_of(mnemonic)
        text = "c.zext.w %s" % first
        values = single_points(points_per_mnemonic, mnemonic)
        return [(text, [(value, 0) for value in values])]
    return None


CHECKED = (sorted(RV.R_TYPE) + sorted(RV.R_TYPE_W) + sorted(RV.I_TYPE)
           + sorted(RV.SHIFT_I) + sorted(RV.I_TYPE_W)
           + sorted(RV.SHIFT_I_W) + ["lui"] + sorted(RV.MULTIPLY)
           + sorted(RV.MULTIPLY_W) + sorted(RV.DIVIDE)
           + sorted(RV.DIVIDE_W) + sorted(RV.CONDITIONAL_ZERO))

# ------------------------------------------------------------------
# task rv3, section 1 row 1: the five rows the reference gained, and the
# three things the rv1 harness could not say that they need
# ------------------------------------------------------------------
#
# ADDED, not rewritten: every row above keeps the shape, the registers,
# the -march string and the program text task rv1 gave it, and the three
# functions below take their old values as their defaults.  What the five
# new rows need that the old ones did not:
#   1. AN -march STRING THAT NAMES THEIR EXTENSIONS.  Lane rv3_l3 quotes
#      the assembler refusing each of them under rv1's own string, by
#      name: "instruction requires the following: 'Zba' ...".
#   2. A DESTINATION THAT IS ALSO A SOURCE.  A compressed form names two
#      registers, not three, so `c.mul a0, a1` leaves its answer in a0.
#   3. A FLOAT ROUND TRIP.  `fsgnjn.d` reads and writes the FLOAT file,
#      and the harness stores from an integer register, so the two
#      operands are moved in with `fmv.d.x` and the answer out with
#      `fmv.x.d`.  THE ROW IS THEREFORE A COMPOSITE OF THREE
#      INSTRUCTIONS, and it says so on itself: an agreement is an
#      agreement about all three together.
MARCH_RV3 = "rv64gc_zba_zbb_zbs_zcb_zicond"

RV3_ADDED = ["add.uw", "bseti", "c.mul", "c.zext.w", "fsgnjn.d"]

# (where the first input is put, where the second is put, where the answer
# is read from, and whether the harness has to cross into the float file)
HOMES = {
    "c.mul": ("a0", "a1", "a0", "integer"),
    "c.zext.w": ("a0", "a1", "a0", "integer"),
    "fsgnjn.d": ("fa0", "fa1", "fa2", "float"),
}

HARNESS_NOTE = {
    "fsgnjn.d": "a COMPOSITE ROW: the harness moves the two inputs into "
                "the float file with `fmv.d.x` and the answer back out "
                "with `fmv.x.d`, so an agreement here is an agreement "
                "about those two instructions as well",
    "c.mul": "the compressed form names two registers and its "
             "destination is also its first source, so the answer is "
             "read from a0",
    "c.zext.w": "the compressed form names one register, which is both "
                "the destination and the only source; the second input "
                "is presented and ignored",
}

CHECKED_RV3 = CHECKED + RV3_ADDED


def homes_of(mnemonic):
    return HOMES.get(mnemonic, (FIRST, SECOND, DESTINATION, "integer"))


def march_of(mnemonic):
    if mnemonic in RV3_ADDED:
        return MARCH_RV3
    return MARCH

REFUSED_BY_NAME = {
    "auipc": "its second input is the program counter, which this harness "
             "cannot present as an input",
}
for _m in sorted(RV.LOAD) + sorted(RV.STORE) + sorted(RV.BRANCH) + \
        sorted(RV.JUMP):
    REFUSED_BY_NAME[_m] = (
        "its effect is not a value the harness can store from a register: "
        "the brief's shape is one instruction between loads of its inputs "
        "and a store of its outputs")
for _m in sorted(RV.FLOAT_BINARY) + sorted(RV.FLOAT_FROM_INTEGER) + \
        sorted(RV.FLOAT_WIDEN) + sorted(RV.FLOAT_MOVE) + \
        sorted(RV.FLOAT_COMPARE) + sorted(RV.FLOAT_LOAD) + \
        sorted(RV.FLOAT_STORE):
    REFUSED_BY_NAME[_m] = (
        "the brief's section 3 names the base integer set; this "
        "instruction is in the reference because the handful's float "
        "bodies spell it")


# ------------------------------------------------------------------
# the bare-metal program
# ------------------------------------------------------------------

PROGRAM = """    .section .text.init, "ax", @progbits
    .globl _start
_start:
    la    s0, inputs
    la    s1, results
    li    s2, %(count)d
loop:
    ld    %(first)s, 0(s0)
    ld    %(second)s, 8(s0)
    %(instruction)s
    sd    %(destination)s, 0(s1)
    addi  s0, s0, 16
    addi  s1, s1, 8
    addi  s2, s2, -1
    bnez  s2, loop
    la    t0, tohost
    li    t1, 1
    sd    t1, 0(t0)
spin:
    j     spin

    .section .data
    .align 3
inputs:
%(inputs)s
    .align 6
    .globl tohost
tohost:
    .dword 0
    .globl fromhost
fromhost:
    .dword 0
    .align 3
    .globl begin_signature
begin_signature:
results:
    .space %(space)d
    .globl end_signature
end_signature:
"""

# task rv3: the same program with a float round trip around the
# instruction, for a row that reads and writes the FLOAT file.  Nothing
# else differs from the program above -- same loop, same inputs table,
# same signature region -- EXCEPT the two-instruction prologue, and that
# is a fact of the machine rather than a convenience:
#
#   AT RESET THE FLOAT UNIT IS OFF.  `mstatus.FS` holds Off, and every
#   floating-point instruction then raises an illegal-instruction trap.
#   Without the prologue the model's own simulator answers
#   "FAILURE: possible trap loop detected with MEPC=0x80000016" (lane
#   rv3_l5 quotes it) -- which is the model being RIGHT, not a defect.
#   `csrs mstatus, 0x6000` sets FS to Dirty, and the same program then
#   answers.  This reference walks a body inside a function that a
#   running program called, where FS is already on, so the prologue
#   states the condition the walk already assumes.
PROGRAM_FLOAT = """    .section .text.init, "ax", @progbits
    .globl _start
_start:
    li    t0, 0x6000
    csrs  mstatus, t0
    la    s0, inputs
    la    s1, results
    li    s2, %(count)d
loop:
    ld    a0, 0(s0)
    ld    a1, 8(s0)
    fmv.d.x %(first)s, a0
    fmv.d.x %(second)s, a1
    %(instruction)s
    fmv.x.d a2, %(destination)s
    sd    a2, 0(s1)
    addi  s0, s0, 16
    addi  s1, s1, 8
    addi  s2, s2, -1
    bnez  s2, loop
    la    t0, tohost
    li    t1, 1
    sd    t1, 0(t0)
spin:
    j     spin

    .section .data
    .align 3
inputs:
%(inputs)s
    .align 6
    .globl tohost
tohost:
    .dword 0
    .globl fromhost
fromhost:
    .dword 0
    .align 3
    .globl begin_signature
begin_signature:
results:
    .space %(space)d
    .globl end_signature
end_signature:
"""

LINKER = """OUTPUT_ARCH(riscv)
ENTRY(_start)
SECTIONS
{
  . = %(reset)s;
  .text.init : { *(.text.init) }
  .text : { *(.text) }
  . = ALIGN(0x1000);
  .data : { *(.data) }
}
"""


def sh(cmd, timeout=900):
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout)
        return (proc.returncode,
                proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ds" % timeout
    except OSError as exc:
        return 125, "", "OSError %s" % exc


def run_variant(instruction, points, work, homes=None, march=None):
    """[the 64-bit value the model left in the destination, per point], or
    a refusal.

    `homes` and `march` default to exactly what task rv1's rows used, so
    every row of that task's own run is unchanged; task rv3's five rows
    pass their own."""
    if homes is None:
        homes = (FIRST, SECOND, DESTINATION, "integer")
    if march is None:
        march = MARCH
    first, second, destination, mode = homes
    lines = []
    for left, right in points:
        lines.append("    .dword 0x%016x" % (left & MASK))
        lines.append("    .dword 0x%016x" % (right & MASK))
    template = PROGRAM
    if mode == "float":
        template = PROGRAM_FLOAT
    body = template % {
        "count": len(points),
        "first": first,
        "second": second,
        "destination": destination,
        "instruction": instruction,
        "inputs": "\n".join(lines),
        "space": 8 * len(points),
    }
    source = os.path.join(work, "one.S")
    script = os.path.join(work, "link.ld")
    elf = os.path.join(work, "one.elf")
    signature = os.path.join(work, "sig.txt")
    open(source, "w").write(body)
    open(script, "w").write(LINKER % {"reset": RESET_ADDRESS})
    if os.path.exists(signature):
        os.remove(signature)
    rc, out, err = sh([CLANG, "--target=riscv64-unknown-elf",
                       "-march=" + march, "-mabi=lp64d", "-nostdlib",
                       "-fuse-ld=lld", "-T", script, source, "-o", elf])
    if rc != 0:
        return None, "ASSEMBLE_REFUSED: %s" % (err or out).strip()[:400]
    limit = 40 * len(points) + 2000
    rc, out, err = sh([SIMULATOR, "--inst-limit", str(limit),
                       "--test-signature", signature, elf])
    if rc != 0:
        return None, "SIMULATOR_REFUSED: %s" % (err or out).strip()[:400]
    if not os.path.exists(signature):
        return None, "NO_SIGNATURE: %s" % out.strip()[:400]
    words = []
    for line in open(signature):
        text = line.strip()
        if text:
            words.append(int(text, 16))
    if len(words) < 2 * len(points):
        return None, ("SHORT_SIGNATURE: %d words for %d points"
                      % (len(words), len(points)))
    values = []
    for index in range(len(points)):
        low = words[2 * index]
        high = words[2 * index + 1]
        values.append((high << 32) | low)
    return values, None


# ------------------------------------------------------------------
# the reference's own reading, evaluated at the same points
# ------------------------------------------------------------------

def reference_term(instruction, homes=None):
    """the z3 term `riscv_reference.py` puts in the destination for this
    instruction, with the two inputs as free symbols.

    The walk mirrors the harness's own program line for line: where the
    program moves its operands into the float file and its answer back
    out, so does this."""
    if homes is None:
        homes = (FIRST, SECOND, DESTINATION, "integer")
    first_home, second_home, destination, mode = homes
    reference = RV.RiscvReference()
    state = RV.MachineState()
    first = state.read_register(RV.INTEGER_REGISTERS["a0"])
    second = state.read_register(RV.INTEGER_REGISTERS["a1"])
    if mode == "float":
        reference.step(state, "fmv.d.x %s, a0" % first_home)
        reference.step(state, "fmv.d.x %s, a1" % second_home)
        reference.step(state, instruction)
        reference.step(state, "fmv.x.d a2, %s" % destination)
        answer = state.read_register(RV.INTEGER_REGISTERS["a2"])
        return answer, first, second
    reference.step(state, instruction)
    answer = state.read_register(RV.INTEGER_REGISTERS[destination])
    return answer, first, second


def evaluate(term, first_symbol, second_symbol, left, right):
    substituted = z3.substitute(
        term,
        (first_symbol, z3.BitVecVal(left & MASK, 64)),
        (second_symbol, z3.BitVecVal(right & MASK, 64)))
    simplified = z3.simplify(substituted)
    if not z3.is_bv_value(simplified):
        return None
    return simplified.as_long() & MASK


# ------------------------------------------------------------------
# the check
# ------------------------------------------------------------------

def check_mnemonic(mnemonic, points_per_mnemonic, work):
    rows = variants_of(mnemonic, points_per_mnemonic)
    if rows is None:
        return {"mnem": mnemonic, "outcome": "NO_VARIANT_SHAPE",
                "points": 0}
    agree = 0
    disagree = []
    unevaluated = 0
    total = 0
    refusal = None
    homes = homes_of(mnemonic)
    march = march_of(mnemonic)
    for instruction, points in rows:
        try:
            term, first_symbol, second_symbol = reference_term(instruction,
                                                               homes)
        except RV.NotModeled as exc:
            refusal = "REFERENCE_REFUSED: %s" % exc
            break
        values, problem = run_variant(instruction, points, work, homes,
                                      march)
        if problem is not None:
            refusal = problem
            break
        for index, (left, right) in enumerate(points):
            total = total + 1
            ours = evaluate(term, first_symbol, second_symbol, left, right)
            theirs = values[index]
            if ours is None:
                unevaluated = unevaluated + 1
                continue
            if ours == theirs:
                agree = agree + 1
                continue
            if len(disagree) < 8:
                disagree.append({
                    "instruction": instruction,
                    "first_input": "0x%016x" % (left & MASK),
                    "second_input": "0x%016x" % (right & MASK),
                    "our_reading": "0x%016x" % ours,
                    "the_model": "0x%016x" % theirs,
                })
    row = {
        "mnem": mnemonic,
        "variants": 0 if rows is None else len(rows),
        "points": total,
        "agree": agree,
        "disagree": total - agree - unevaluated,
        "unevaluated": unevaluated,
        "examples": disagree,
        "march": march,
        "homes": {"first": homes[0], "second": homes[1],
                  "destination": homes[2], "mode": homes[3]},
    }
    note = HARNESS_NOTE.get(mnemonic)
    if note is not None:
        row["harness_note"] = note
    if refusal is not None:
        row["outcome"] = "REFUSED"
        row["cause"] = refusal
        return row
    if total == 0:
        row["outcome"] = "NO_POINTS"
        return row
    if row["disagree"] == 0 and unevaluated == 0:
        row["outcome"] = "AGREES_AT_EVERY_POINT"
        return row
    row["outcome"] = "DISAGREES"
    return row


def main():
    out_prefix = sys.argv[1]
    work = sys.argv[2]
    points_per_mnemonic = POINT_CAP
    only = None
    args = sys.argv[3:]
    while args:
        if args[0] == "--points":
            points_per_mnemonic = int(args[1])
            args = args[2:]
            continue
        if args[0] == "--only":
            only = args[1].split(",")
            args = args[2:]
            continue
        raise SystemExit("unknown argument %r" % args[0])
    if not os.path.isdir(work):
        os.makedirs(work)

    wanted = CHECKED_RV3
    if only:
        wanted = [m for m in CHECKED_RV3 if m in only]
    rows = []
    total = len(wanted)
    for index, mnemonic in enumerate(wanted, 1):
        print("[%d/%d] %s" % (index, total, mnemonic))
        sys.stdout.flush()
        row = check_mnemonic(mnemonic, points_per_mnemonic, work)
        row["peak_rss_mb"] = round(check_memory(mnemonic), 1)
        rows.append(row)
        print("      %-24s points %6d  agree %6d  disagree %5d"
              % (row["outcome"], row["points"], row.get("agree", 0),
                 row.get("disagree", 0)))
        for example in row.get("examples", [])[:3]:
            print("      %s  first=%s second=%s  ours=%s model=%s"
                  % (example["instruction"], example["first_input"],
                     example["second_input"], example["our_reading"],
                     example["the_model"]))
        sys.stdout.flush()

    refused = []
    for mnemonic in sorted(REFUSED_BY_NAME):
        refused.append({"mnem": mnemonic,
                        "cause": REFUSED_BY_NAME[mnemonic]})

    doc = {
        "meta": {
            "task": "rv1",
            "what": "the RISC-V reference's term for each base-integer "
                    "instruction, evaluated at concrete points, against "
                    "the ratified Sail model's own simulator run over a "
                    "bare-metal program executing that instruction at the "
                    "same points",
            "this_is": "A CHECK AT POINTS, NOT AN EQUALITY",
            "simulator": SIMULATOR,
            "reset_address": RESET_ADDRESS,
            "point_cap_per_mnem": points_per_mnemonic,
            "memory_ceiling_mb": MEMORY_CEILING_MB,
            "abort_name": ABORT_NAME,
            "peak_rss_mb": round(peak_rss_mb(), 1),
            "edge_values": len(EDGES),
            "rows_added_by_task_rv3": list(RV3_ADDED),
            "march_for_the_rv3_rows": MARCH_RV3,
            "march_for_the_rv1_rows": MARCH,
        },
        "rows": rows,
        "refused_by_name": refused,
    }
    fh = open(out_prefix + ".json", "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()

    checked = len([r for r in rows if r["outcome"] ==
                   "AGREES_AT_EVERY_POINT"])
    points = sum(r["points"] for r in rows)
    print("mnemonics checked %d, agreeing at every point %d, points %d"
          % (len(rows), checked, points))
    print("peak RSS: %.1f MB (ceiling %d MB, abort %s)"
          % (peak_rss_mb(), MEMORY_CEILING_MB, ABORT_NAME))


if __name__ == "__main__":
    main()
