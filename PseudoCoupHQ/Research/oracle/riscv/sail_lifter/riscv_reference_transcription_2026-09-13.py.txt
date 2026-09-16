#!/usr/bin/env python3
"""riscv_reference.py -- THE ONE SYMBOLIC SIMULATOR OF THE RISC-V MACHINE.

Node: hq.research.arch_unit_oracle
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
Task rv1, brief `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv1_brief.md`
section 3(a).

WHAT THIS FILE IS, one sentence, in relation: the riscv64 twin of
`PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py` -- one z3
term per place an instruction writes, read off the instruction's own
disassembled text, so a carved riscv64 body can be walked into a term the
same way an x86 body is.

IT IS BUILT IN reference.py's OWN SHAPE, section for section, so the two
can be read side by side and so section 5 of the brief can count what had
to be written again:

    section 1  the widths, the sorts, and the register tables
    section 2  MachineState -- the sub-node
    section 3  the operand reader -- one place, used by every builder
    section 4  the term builders -- one per family, no second table
    section 5  opcode_table -- THE ONE TABLE
    section 6  RiscvReference -- the node's own class

THE FOUR THINGS THAT ARE NOT IN THE x86 FILE, each a fact of the
architecture and not a choice of ours:

  * THERE IS NO FLAGS REGISTER.  Nothing here writes one, nothing reads
    one, and `MachineState` has no `flags` attribute.  x86 spends
    `build_flag_only`, `carry_bit`, `overflow_bit`, `predicate_of`,
    `condition_table.py` and the whole `set`/`cmov`/`j` suffix family on
    the flags; RISC-V spends `slt`/`sltu` (a comparison writes a general
    register a 0 or a 1) and the six branches (a comparison is read
    inside the branch itself).

  * EVERY REGISTER WRITE IS THE FULL 64 BITS.  x86's `full64` /
    `place_bits` / `KEEPS_THE_UPPER_BITS` rule -- a 32-bit write
    zero-extends, an 8- or 16-bit write keeps the register's other bits --
    has no counterpart: the architecture has no sub-register names.  The
    32-bit forms (`addw`, `srliw`, `mulw` ...) compute at 32 bits and
    SIGN-EXTEND the result into the whole register, which is one rule
    written once here (`sign_extend_w`).

  * REGISTER x0 IS THE CONSTANT ZERO.  It reads zero and a write to it is
    discarded.  That is what makes the assembler's reading aids (`li`,
    `mv`, `ret`, `nop`, `seqz`) expressible with no new instructions, and
    it is why this file is walked over `llvm-objdump -M no-aliases` text:
    the aids are spellings, and a spelling is not machine form.

  * DIVISION DOES NOT TRAP.  x86's `idiv` raises on a zero divisor and on
    the MIN / -1 overflow, and the corpus's units carry a guard around it.
    RISC-V defines both: `div` by zero is all ones, `rem` by zero is the
    dividend, `divu` by zero is 2^64-1, `remu` by zero is the dividend,
    and `div`(MIN, -1) is MIN with `rem` 0.  The reference states them and
    the Sail model checks them.

THE HONEST LIMITS, named rather than hidden.

  * `simulate` walks the body in TEXT ORDER, exactly as the x86 reference
    does.  A conditional branch is recorded as a guard row and its
    condition is kept; no branch-merging walk is coded here, because the
    ten bodies of this task's handful have none.
  * `auipc` reads the program counter.  Its term carries a `pc` symbol,
    and the point check of section 3(b) cannot present a program counter
    as an input, so `auipc` is REFUSED BY NAME there rather than counted
    as agreeing.
  * The floating-point family here is exactly the instructions the ten
    carved bodies spell -- the same rule the x86 table follows ("no entry
    is invented for an opcode no body contains").  The vector extension is
    absent.
  * A floating-point instruction carries a ROUNDING MODE operand, which
    `llvm-objdump` prints as a trailing `dyn` when the instruction defers
    to the `fcsr` register.  This file reads round-to-nearest-even for
    every rounding, which is what `fcsr` holds at reset and what the ten
    bodies run under; a body that writes `fcsr` first is not modelled and
    none of the ten does.
  * ONE INSTRUCTION OUTSIDE RV64I+M IS IN THE TABLE, and it is here
    because a carved body spells it: `czero.eqz` of the Zicond extension,
    which clang 21 emits for the select the handful's `cmovne` row
    carries.  It is marked as an extension on its own entry.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

No operator token appears in this file.  The table is keyed by ARCH
MNEMONIC, which is machine-form evidence read off the disassembled body,
never by the source spelling a probe was generated from.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  riscv_reference.py (library; `sail_points.py` and `claim_check.py` are
  this task's drivers)
"""

import re

import z3


class NotModeled(Exception):
    """the reference refuses this instruction by name, and says why."""


class LeavesTheUnit(Exception):
    """this line transfers OUT of the unit."""

    def __init__(self, line, target):
        Exception.__init__(self, "%s -> %s" % (line, target))
        self.line = line
        self.target = target


# ------------------------------------------------------------------
# section 1: the widths, the sorts, and the register tables
# ------------------------------------------------------------------

XLEN = 64

FLOAT_SORT = {32: z3.Float32(), 64: z3.Float64()}

ROUNDING = z3.RNE()

# The integer register file, by the ABI names `llvm-objdump` prints.  The
# value is the ARCHITECTURAL index, which is the machine-form key: two ABI
# names for one index (`s0` and `fp`) are one register.
INTEGER_REGISTERS = {
    "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4,
    "t0": 5, "t1": 6, "t2": 7,
    "s0": 8, "fp": 8, "s1": 9,
    "a0": 10, "a1": 11, "a2": 12, "a3": 13,
    "a4": 14, "a5": 15, "a6": 16, "a7": 17,
    "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23,
    "s8": 24, "s9": 25, "s10": 26, "s11": 27,
    "t3": 28, "t4": 29, "t5": 30, "t6": 31,
}
for _i in range(32):
    INTEGER_REGISTERS["x%d" % _i] = _i

FLOAT_REGISTERS = {}
for _i in range(8):
    FLOAT_REGISTERS["ft%d" % _i] = _i
for _i in range(2):
    FLOAT_REGISTERS["fs%d" % _i] = 8 + _i
for _i in range(8):
    FLOAT_REGISTERS["fa%d" % _i] = 10 + _i
for _i in range(10):
    FLOAT_REGISTERS["fs%d" % (_i + 2)] = 18 + _i
for _i in range(4):
    FLOAT_REGISTERS["ft%d" % (_i + 8)] = 28 + _i
for _i in range(32):
    FLOAT_REGISTERS["f%d" % _i] = _i

ZERO_REGISTER = 0

# THE ARGUMENT AND ANSWER PLACES OF THE psABI (`lp64d`), stated once and
# read by the walk, never guessed per unit.
INTEGER_ARGUMENTS = [10, 11, 12, 13, 14, 15, 16, 17]     # a0 .. a7
INTEGER_ANSWER = 10                                      # a0
FLOAT_ARGUMENTS = [10, 11, 12, 13, 14, 15, 16, 17]       # fa0 .. fa7
FLOAT_ANSWER = 10                                        # fa0


def sign_extend_w(value32):
    """THE 32-BIT FORMS' OWN WRITE RULE: compute at 32 bits, then place the
    sign-extension of that result in the whole 64-bit register.  This is
    the whole of what x86 spends `full64` and `place_bits` on."""
    return z3.SignExt(32, value32)


def bits_of(value, width):
    if value.size() == width:
        return value
    if value.size() > width:
        return z3.Extract(width - 1, 0, value)
    return z3.ZeroExt(width - value.size(), value)


def as_float(bits, width):
    return z3.fpBVToFP(bits_of(bits, width), FLOAT_SORT[width])


def from_float(value):
    return z3.fpToIEEEBV(value)


def nan_box(bits32):
    """a 32-bit float value held in a 64-bit float register is NaN-boxed:
    the upper 32 bits are all ones (the RISC-V ISA manual, `Zfinx`-free
    F-in-D rule)."""
    return z3.Concat(z3.BitVecVal((1 << 32) - 1, 32), bits32)


def memory_symbol_name(text):
    """`0x8(sp)` names the cell `MEM_0x8_sp_`, the same mangling
    `reference.memory_symbol_name` does for x86, so a memory operand is one
    fixed unknown per literal text."""
    out = re.sub(r"[^0-9A-Za-z]", "_", text)
    return "MEM_%s" % out


# ------------------------------------------------------------------
# section 2: MachineState -- the sub-node
# ------------------------------------------------------------------

class MachineState(object):
    """the symbolic machine the reference walks a body over.

      registers  -- architectural index -> 64-bit term, seeded as
                    `seed_x<i>` free symbols, so a proof is about every
                    input at once.  Index 0 always reads zero.
      fregisters -- architectural index -> the 64-bit RAW BITS of the
                    floating-point register, seeded as `seed_f<i>`.
      memory     -- literal operand text -> 64-bit term; an unwritten cell
                    reads one fixed unknown named `seed_MEM_<mangled>`.
      pc         -- one symbol; only `auipc` and the transfers read it.

    THERE IS NO FLAGS ATTRIBUTE.  The architecture has no flags register,
    so there is nothing to hold.
    """

    def __init__(self, shared_seed=None):
        if shared_seed is None:
            shared_seed = {}
        self.shared_seed = shared_seed
        self.registers = {}
        self.fregisters = {}
        self.memory = {}
        self.refusals = []
        self.guard_rows = []
        self.branch_condition = None
        self.path_condition = z3.BoolVal(True)

    # -- integer registers -------------------------------------------

    def seed(self, index):
        name = "seed_x%d" % index
        if name not in self.shared_seed:
            self.shared_seed[name] = z3.BitVec(name, XLEN)
        return self.shared_seed[name]

    def bind(self, index, term):
        """pre-bind a register to somebody else's symbol -- the arrival
        contract's job."""
        self.registers[index] = term

    def read_register(self, index):
        if index == ZERO_REGISTER:
            return z3.BitVecVal(0, XLEN)
        if index in self.registers:
            return self.registers[index]
        value = self.seed(index)
        self.registers[index] = value
        return value

    def write_register(self, index, term):
        """EVERY WRITE IS THE FULL 64 BITS, and a write to x0 is
        discarded."""
        if index == ZERO_REGISTER:
            return
        self.registers[index] = bits_of(term, XLEN)

    # -- floating-point registers ------------------------------------

    def seed_float(self, index):
        name = "seed_f%d" % index
        if name not in self.shared_seed:
            self.shared_seed[name] = z3.BitVec(name, XLEN)
        return self.shared_seed[name]

    def read_float(self, index):
        if index in self.fregisters:
            return self.fregisters[index]
        value = self.seed_float(index)
        self.fregisters[index] = value
        return value

    def write_float(self, index, term):
        self.fregisters[index] = bits_of(term, XLEN)

    # -- memory -------------------------------------------------------

    def memory_cell(self, text):
        if text in self.memory:
            return self.memory[text]
        name = memory_symbol_name(text)
        if name not in self.shared_seed:
            self.shared_seed[name] = z3.BitVec("seed_%s" % name, XLEN)
        cell = self.shared_seed[name]
        self.memory[text] = cell
        return cell

    def set_memory_cell(self, text, term):
        self.memory[text] = bits_of(term, XLEN)

    # -- the program counter -----------------------------------------

    def program_counter(self):
        if "pc" not in self.shared_seed:
            self.shared_seed["pc"] = z3.BitVec("pc", XLEN)
        return self.shared_seed["pc"]


# ------------------------------------------------------------------
# section 3: the operand reader -- one place, used by every builder
# ------------------------------------------------------------------

IMMEDIATE_RE = re.compile(r"^-?(?:0x[0-9a-fA-F]+|\d+)$")
MEMORY_RE = re.compile(r"^(-?(?:0x[0-9a-fA-F]+|\d+))\(([a-z0-9]+)\)$")


def split_operands(rest):
    """split an operand list on top-level commas only."""
    out = []
    depth = 0
    current = ""
    for char in rest:
        if char == "(":
            depth = depth + 1
            current = current + char
            continue
        if char == ")":
            depth = depth - 1
            current = current + char
            continue
        if char == "," and depth == 0:
            out.append(current)
            current = ""
            continue
        current = current + char
    if current:
        out.append(current)
    return [item.strip() for item in out]


class Operands(object):
    """the resolved operand slots of one body line, in the disassembler's
    own order (RISC-V: destination first, then the sources).  Every builder
    in the table reads its inputs through this object and through nothing
    else."""

    def __init__(self, state, mnemonic, texts):
        self.state = state
        self.mnemonic = mnemonic
        self.texts = texts

    # -- classification ----------------------------------------------

    def is_immediate(self, text):
        return IMMEDIATE_RE.match(text) is not None

    def is_integer_register(self, text):
        return text in INTEGER_REGISTERS

    def is_float_register(self, text):
        return text in FLOAT_REGISTERS

    def is_memory(self, text):
        return MEMORY_RE.match(text) is not None

    # -- reading ------------------------------------------------------

    def immediate_value(self, text):
        negative = text.startswith("-")
        body = text[1:] if negative else text
        if body.startswith("0x"):
            value = int(body, 16)
        else:
            value = int(body, 10)
        if negative:
            value = -value
        return value

    def immediate(self, index):
        text = self.texts[index]
        if not self.is_immediate(text):
            raise NotModeled(
                "operand %r of %r is not an immediate"
                % (text, self.mnemonic))
        return z3.BitVecVal(self.immediate_value(text) % (1 << XLEN), XLEN)

    def register_index(self, index):
        text = self.texts[index]
        if text not in INTEGER_REGISTERS:
            raise NotModeled(
                "register spelling %r is not an integer register of this "
                "architecture" % text)
        return INTEGER_REGISTERS[text]

    def float_index(self, index):
        text = self.texts[index]
        if text not in FLOAT_REGISTERS:
            raise NotModeled(
                "register spelling %r is not a floating-point register of "
                "this architecture" % text)
        return FLOAT_REGISTERS[text]

    def read(self, index):
        return self.state.read_register(self.register_index(index))

    def read_float(self, index):
        return self.state.read_float(self.float_index(index))

    def write(self, index, term):
        self.state.write_register(self.register_index(index), term)

    def write_float(self, index, term):
        self.state.write_float(self.float_index(index), term)

    def memory_parts(self, index):
        text = self.texts[index]
        hit = MEMORY_RE.match(text)
        if hit is None:
            raise NotModeled(
                "operand %r of %r is not an offset-and-base memory "
                "operand" % (text, self.mnemonic))
        return hit.group(1), hit.group(2)


# ------------------------------------------------------------------
# section 4: the term builders -- one per family, no second table
# ------------------------------------------------------------------
#
# Every builder has the same shape as the x86 file's: it takes the resolved
# `Operands` of one body line and applies that line's own meaning to the
# machine state.

R_TYPE = frozenset(["add", "sub", "sll", "slt", "sltu", "xor", "srl",
                    "sra", "or", "and"])
R_TYPE_W = frozenset(["addw", "subw", "sllw", "srlw", "sraw"])
I_TYPE = frozenset(["addi", "slti", "sltiu", "xori", "ori", "andi"])
SHIFT_I = frozenset(["slli", "srli", "srai"])
I_TYPE_W = frozenset(["addiw"])
SHIFT_I_W = frozenset(["slliw", "srliw", "sraiw"])
UPPER = frozenset(["lui", "auipc"])
MULTIPLY = frozenset(["mul", "mulh", "mulhsu", "mulhu"])
MULTIPLY_W = frozenset(["mulw"])
DIVIDE = frozenset(["div", "divu", "rem", "remu"])
CONDITIONAL_ZERO = frozenset(["czero.eqz", "czero.nez"])
DIVIDE_W = frozenset(["divw", "divuw", "remw", "remuw"])

# -- task rv3, section 1 row 1.  THE ROWS clang 21 WRITES AND THIS TABLE
# -- HAD NO ENTRY FOR, and not one row more.
#
# The x86 table's own rule is that no entry is invented for an opcode no
# body contains.  These five were READ OFF CARVED BODIES: `census_rv3.json`
# counts `c.zext.w`, `add.uw` and `c.mul` over the 244 inherited sources,
# and task rv2's `rv_loop.jsonl` carries `bseti` and `fsgnjn.d` with the
# body line each refused on, quoted in log_260.  Each is checked against
# the ratified Sail model at points before it is used, exactly as task rv1
# checked the base set.
ADD_UNSIGNED_WORD = frozenset(["add.uw"])          # Zba
BIT_SET_I = frozenset(["bseti"])                   # Zbs
FLOAT_SIGN_INJECT = {"fsgnjn.d": ("negate", 64)}   # D, sign-injection
LOAD = {"lb": (8, True), "lh": (16, True), "lw": (32, True),
        "ld": (64, True), "lbu": (8, False), "lhu": (16, False),
        "lwu": (32, False)}
STORE = {"sb": 8, "sh": 16, "sw": 32, "sd": 64}
BRANCH = frozenset(["beq", "bne", "blt", "bge", "bltu", "bgeu"])
JUMP = frozenset(["jal", "jalr"])
NO_OPERATION = frozenset(["fence", "fence.i", "nop", "c.nop", "pause"])
TRAP = frozenset(["ecall", "ebreak", "c.ebreak", "unimp", "c.unimp"])


def shift_amount(value, width):
    """the shift amount is the low bits of the source: six at 64, five at
    32.  The architecture masks; it does not refuse."""
    if width == 64:
        return value & z3.BitVecVal(0x3F, XLEN)
    return value & z3.BitVecVal(0x1F, XLEN)


def build_r_type(ops):
    left = ops.read(1)
    right = ops.read(2)
    mnemonic = ops.mnemonic
    if mnemonic == "add":
        result = left + right
    elif mnemonic == "sub":
        result = left - right
    elif mnemonic == "and":
        result = left & right
    elif mnemonic == "or":
        result = left | right
    elif mnemonic == "xor":
        result = left ^ right
    elif mnemonic == "sll":
        result = left << shift_amount(right, 64)
    elif mnemonic == "srl":
        result = z3.LShR(left, shift_amount(right, 64))
    elif mnemonic == "sra":
        result = left >> shift_amount(right, 64)
    elif mnemonic == "slt":
        result = z3.If(left < right, z3.BitVecVal(1, XLEN),
                       z3.BitVecVal(0, XLEN))
    else:
        result = z3.If(z3.ULT(left, right), z3.BitVecVal(1, XLEN),
                       z3.BitVecVal(0, XLEN))
    ops.write(0, result)


def build_r_type_w(ops):
    left = z3.Extract(31, 0, ops.read(1))
    right = z3.Extract(31, 0, ops.read(2))
    mnemonic = ops.mnemonic
    if mnemonic == "addw":
        result = left + right
    elif mnemonic == "subw":
        result = left - right
    elif mnemonic == "sllw":
        amount = z3.Extract(31, 0, shift_amount(ops.read(2), 32))
        result = left << amount
    elif mnemonic == "srlw":
        amount = z3.Extract(31, 0, shift_amount(ops.read(2), 32))
        result = z3.LShR(left, amount)
    else:
        amount = z3.Extract(31, 0, shift_amount(ops.read(2), 32))
        result = left >> amount
    ops.write(0, sign_extend_w(result))


def build_i_type(ops):
    left = ops.read(1)
    right = ops.immediate(2)
    mnemonic = ops.mnemonic
    if mnemonic == "addi":
        result = left + right
    elif mnemonic == "andi":
        result = left & right
    elif mnemonic == "ori":
        result = left | right
    elif mnemonic == "xori":
        result = left ^ right
    elif mnemonic == "slti":
        result = z3.If(left < right, z3.BitVecVal(1, XLEN),
                       z3.BitVecVal(0, XLEN))
    else:
        result = z3.If(z3.ULT(left, right), z3.BitVecVal(1, XLEN),
                       z3.BitVecVal(0, XLEN))
    ops.write(0, result)


def build_shift_i(ops):
    left = ops.read(1)
    amount = ops.immediate(2) & z3.BitVecVal(0x3F, XLEN)
    mnemonic = ops.mnemonic
    if mnemonic == "slli":
        result = left << amount
    elif mnemonic == "srli":
        result = z3.LShR(left, amount)
    else:
        result = left >> amount
    ops.write(0, result)


def build_i_type_w(ops):
    left = z3.Extract(31, 0, ops.read(1))
    right = z3.Extract(31, 0, ops.immediate(2))
    ops.write(0, sign_extend_w(left + right))


def build_shift_i_w(ops):
    left = z3.Extract(31, 0, ops.read(1))
    amount = z3.Extract(31, 0, ops.immediate(2) & z3.BitVecVal(0x1F, XLEN))
    mnemonic = ops.mnemonic
    if mnemonic == "slliw":
        result = left << amount
    elif mnemonic == "srliw":
        result = z3.LShR(left, amount)
    else:
        result = left >> amount
    ops.write(0, sign_extend_w(result))


def build_upper(ops):
    """`lui rd, imm` places the 20-bit immediate in bits 31..12 and
    sign-extends; `auipc rd, imm` adds that to the program counter.

    `llvm-objdump` prints the immediate ALREADY SHIFTED DOWN -- `lui a0,
    0x1` means the value 0x1000 -- so the builder shifts it back up."""
    raw = ops.immediate(1)
    placed = z3.Extract(31, 0, raw << z3.BitVecVal(12, XLEN))
    value = z3.SignExt(32, placed)
    if ops.mnemonic == "lui":
        ops.write(0, value)
        return
    ops.write(0, ops.state.program_counter() + value)


def build_multiply(ops):
    left = ops.read(1)
    right = ops.read(2)
    mnemonic = ops.mnemonic
    if mnemonic == "mul":
        ops.write(0, left * right)
        return
    if mnemonic == "mulh":
        wide = z3.SignExt(64, left) * z3.SignExt(64, right)
    elif mnemonic == "mulhu":
        wide = z3.ZeroExt(64, left) * z3.ZeroExt(64, right)
    else:
        wide = z3.SignExt(64, left) * z3.ZeroExt(64, right)
    ops.write(0, z3.Extract(127, 64, wide))


def build_multiply_w(ops):
    left = z3.Extract(31, 0, ops.read(1))
    right = z3.Extract(31, 0, ops.read(2))
    ops.write(0, sign_extend_w(left * right))


def build_divide(ops):
    """THE CAREFUL CASE, and the one that most differs from x86.

    The architecture DEFINES every case; nothing traps.  Quotient by zero
    is all ones for the signed form and 2^64-1 for the unsigned form (the
    same bits); remainder by zero is the dividend.  The signed overflow
    (the most negative dividend divided by minus one) gives that dividend
    back, with remainder zero.  Rounding is toward zero, so the remainder's
    sign follows the DIVIDEND -- z3's `SRem`, never its `%`."""
    left = ops.read(1)
    right = ops.read(2)
    mnemonic = ops.mnemonic
    zero = z3.BitVecVal(0, XLEN)
    all_ones = z3.BitVecVal((1 << XLEN) - 1, XLEN)
    most_negative = z3.BitVecVal(1 << (XLEN - 1), XLEN)
    minus_one = all_ones
    if mnemonic == "div":
        overflow = z3.And(left == most_negative, right == minus_one)
        result = z3.If(right == zero, all_ones,
                       z3.If(overflow, most_negative, left / right))
    elif mnemonic == "divu":
        result = z3.If(right == zero, all_ones, z3.UDiv(left, right))
    elif mnemonic == "rem":
        overflow = z3.And(left == most_negative, right == minus_one)
        result = z3.If(right == zero, left,
                       z3.If(overflow, zero, z3.SRem(left, right)))
    else:
        result = z3.If(right == zero, left, z3.URem(left, right))
    ops.write(0, result)


def build_divide_w(ops):
    """the 32-bit forms: the same defined cases, computed at 32 bits, the
    result sign-extended into the whole register."""
    left = z3.Extract(31, 0, ops.read(1))
    right = z3.Extract(31, 0, ops.read(2))
    mnemonic = ops.mnemonic
    zero = z3.BitVecVal(0, 32)
    all_ones = z3.BitVecVal((1 << 32) - 1, 32)
    most_negative = z3.BitVecVal(1 << 31, 32)
    minus_one = all_ones
    if mnemonic == "divw":
        overflow = z3.And(left == most_negative, right == minus_one)
        result = z3.If(right == zero, all_ones,
                       z3.If(overflow, most_negative, left / right))
    elif mnemonic == "divuw":
        result = z3.If(right == zero, all_ones, z3.UDiv(left, right))
    elif mnemonic == "remw":
        overflow = z3.And(left == most_negative, right == minus_one)
        result = z3.If(right == zero, left,
                       z3.If(overflow, zero, z3.SRem(left, right)))
    else:
        result = z3.If(right == zero, left, z3.URem(left, right))
    ops.write(0, sign_extend_w(result))


def build_conditional_zero(ops):
    """Zicond's conditional zero, and the instruction clang 21 reaches for
    where x86 reaches for a conditional move.

    `czero.eqz rd, rs1, rs2` writes zero when rs2 IS zero and rs1
    otherwise; `czero.nez rd, rs1, rs2` writes zero when rs2 is NOT zero
    and rs1 otherwise.  There is no flags register in the reading: the
    condition is the second source register's own value."""
    value = ops.read(1)
    condition = ops.read(2)
    zero = z3.BitVecVal(0, XLEN)
    if ops.mnemonic == "czero.eqz":
        result = z3.If(condition == zero, zero, value)
    else:
        result = z3.If(condition != zero, zero, value)
    ops.write(0, result)


def build_add_unsigned_word(ops):
    """Zba's `add.uw rd, rs1, rs2`, and the one thing about it that is not
    an ordinary add: the FIRST source is cut to its low 32 bits and
    ZERO-extended before the addition, while the second is read whole.

    Everywhere else in this file a 32-bit form sign-extends; this one does
    not, because its purpose is to turn an unsigned 32-bit index into a
    64-bit address.  clang 21 writes it wherever a rendered emulation casts
    a 32-bit value to a wider unsigned one and adds."""
    low = z3.Extract(31, 0, ops.read(1))
    ops.write(0, z3.ZeroExt(32, low) + ops.read(2))


def build_bit_set_immediate(ops):
    """Zbs's `bseti rd, rs1, shamt`: the first source with the single bit
    `shamt` SET.  The shift amount is the low six bits of the immediate at
    64, the same masking rule the shift-immediate forms use; the
    architecture masks, it does not refuse."""
    value = ops.read(1)
    amount = ops.immediate(2) & z3.BitVecVal(0x3F, XLEN)
    one = z3.BitVecVal(1, XLEN)
    ops.write(0, value | (one << amount))


def build_float_sign_inject(ops):
    """`fsgnjn.d rd, rs1, rs2`: the result carries rs1's every bit BUT the
    sign, and the OPPOSITE of rs2's sign bit.

    THIS IS A BIT OPERATION AND IS WRITTEN AS ONE.  Sign injection is
    defined on the encoding, never on the value: it raises no exception,
    it does not canonicalise a NaN, and it moves a signalling NaN through
    unchanged.  Writing it through z3's float sort would lose exactly
    those facts, so the builder works on the bits.  `fsgnjn.d rd, rs, rs`
    is what an assembler spells `fneg.d`, which is why a carved body has
    it."""
    kind, width = FLOAT_SIGN_INJECT[ops.mnemonic]
    left = ops.read_float(1)
    right = ops.read_float(2)
    sign = z3.Extract(width - 1, width - 1, bits_of(right, width))
    if kind == "negate":
        sign = ~sign
    rest = z3.Extract(width - 2, 0, bits_of(left, width))
    placed = z3.Concat(sign, rest)
    if width == 32:
        ops.write_float(0, nan_box(placed))
        return
    ops.write_float(0, placed)


def build_load(ops):
    width, signed = LOAD[ops.mnemonic]
    cell = ops.state.memory_cell(ops.texts[1])
    value = z3.Extract(width - 1, 0, cell)
    if width == XLEN:
        ops.write(0, value)
        return
    if signed:
        ops.write(0, z3.SignExt(XLEN - width, value))
        return
    ops.write(0, z3.ZeroExt(XLEN - width, value))


def build_store(ops):
    width = STORE[ops.mnemonic]
    value = ops.read(0)
    if width == XLEN:
        ops.state.set_memory_cell(ops.texts[1], value)
        return
    kept = ops.state.memory_cell(ops.texts[1])
    low = z3.Extract(width - 1, 0, value)
    high = z3.Extract(XLEN - 1, width, kept)
    ops.state.set_memory_cell(ops.texts[1], z3.Concat(high, low))


def build_branch(ops):
    left = ops.read(0)
    right = ops.read(1)
    mnemonic = ops.mnemonic
    if mnemonic == "beq":
        condition = left == right
    elif mnemonic == "bne":
        condition = left != right
    elif mnemonic == "blt":
        condition = left < right
    elif mnemonic == "bge":
        condition = left >= right
    elif mnemonic == "bltu":
        condition = z3.ULT(left, right)
    else:
        condition = z3.UGE(left, right)
    ops.state.branch_condition = condition


def build_jump(ops):
    """`jal rd, target` and `jalr rd, off(rs1)` write the return address
    into `rd` and transfer.  The transfer itself is the walk's business,
    not the table's; what the table states is the write."""
    index = ops.register_index(0)
    if index != ZERO_REGISTER:
        ops.state.write_register(
            index, ops.state.program_counter() + z3.BitVecVal(4, XLEN))


def build_no_operation(ops):
    return


def build_trap(ops):
    raise LeavesTheUnit(ops.mnemonic, "a trap")


# -- the floating-point family, exactly the instructions the ten carved
# -- bodies spell.

FLOAT_BINARY = {
    "fadd.s": ("add", 32), "fadd.d": ("add", 64),
    "fsub.s": ("sub", 32), "fsub.d": ("sub", 64),
    "fmul.s": ("mul", 32), "fmul.d": ("mul", 64),
    "fdiv.s": ("div", 32), "fdiv.d": ("div", 64),
}
FLOAT_FROM_INTEGER = {
    "fcvt.s.w": (32, 32, True), "fcvt.s.wu": (32, 32, False),
    "fcvt.s.l": (32, 64, True), "fcvt.s.lu": (32, 64, False),
    "fcvt.d.w": (64, 32, True), "fcvt.d.wu": (64, 32, False),
    "fcvt.d.l": (64, 64, True), "fcvt.d.lu": (64, 64, False),
}
FLOAT_WIDEN = {"fcvt.d.s": (32, 64), "fcvt.s.d": (64, 32)}
FLOAT_MOVE = {
    "fmv.w.x": ("to_float", 32), "fmv.x.w": ("to_integer", 32),
    "fmv.d.x": ("to_float", 64), "fmv.x.d": ("to_integer", 64),
    "fmv.s": ("float_to_float", 32), "fmv.d": ("float_to_float", 64),
}
FLOAT_COMPARE = {"feq.s": ("eq", 32), "flt.s": ("lt", 32),
                 "fle.s": ("le", 32), "feq.d": ("eq", 64),
                 "flt.d": ("lt", 64), "fle.d": ("le", 64)}
FLOAT_LOAD = {"flw": 32, "fld": 64}
FLOAT_STORE = {"fsw": 32, "fsd": 64}


def float_of(ops, index, width):
    bits = ops.read_float(index)
    return as_float(bits, width)


def placed_float(value, width):
    bits = from_float(value)
    if width == 32:
        return nan_box(bits)
    return bits


def build_float_binary(ops):
    kind, width = FLOAT_BINARY[ops.mnemonic]
    left = float_of(ops, 1, width)
    right = float_of(ops, 2, width)
    if kind == "add":
        result = z3.fpAdd(ROUNDING, left, right)
    elif kind == "sub":
        result = z3.fpSub(ROUNDING, left, right)
    elif kind == "mul":
        result = z3.fpMul(ROUNDING, left, right)
    else:
        result = z3.fpDiv(ROUNDING, left, right)
    ops.write_float(0, placed_float(result, width))


def build_float_from_integer(ops):
    float_width, integer_width, signed = FLOAT_FROM_INTEGER[ops.mnemonic]
    whole = ops.read(1)
    if integer_width != XLEN:
        whole = z3.Extract(integer_width - 1, 0, whole)
    if signed:
        value = z3.fpSignedToFP(ROUNDING, whole, FLOAT_SORT[float_width])
    else:
        value = z3.fpUnsignedToFP(ROUNDING, whole, FLOAT_SORT[float_width])
    ops.write_float(0, placed_float(value, float_width))


def build_float_widen(ops):
    source_width, target_width = FLOAT_WIDEN[ops.mnemonic]
    value = float_of(ops, 1, source_width)
    widened = z3.fpFPToFP(ROUNDING, value, FLOAT_SORT[target_width])
    ops.write_float(0, placed_float(widened, target_width))


def build_float_move(ops):
    kind, width = FLOAT_MOVE[ops.mnemonic]
    if kind == "to_float":
        bits = ops.read(1)
        if width == 32:
            ops.write_float(0, nan_box(z3.Extract(31, 0, bits)))
            return
        ops.write_float(0, bits)
        return
    if kind == "to_integer":
        bits = ops.read_float(1)
        if width == 32:
            ops.write(0, z3.SignExt(32, z3.Extract(31, 0, bits)))
            return
        ops.write(0, bits)
        return
    ops.write_float(0, ops.read_float(1))


def build_float_compare(ops):
    kind, width = FLOAT_COMPARE[ops.mnemonic]
    left = float_of(ops, 1, width)
    right = float_of(ops, 2, width)
    if kind == "eq":
        condition = z3.fpEQ(left, right)
    elif kind == "lt":
        condition = z3.fpLT(left, right)
    else:
        condition = z3.fpLEQ(left, right)
    ops.write(0, z3.If(condition, z3.BitVecVal(1, XLEN),
                       z3.BitVecVal(0, XLEN)))


def build_float_load(ops):
    width = FLOAT_LOAD[ops.mnemonic]
    cell = ops.state.memory_cell(ops.texts[1])
    if width == 32:
        ops.write_float(0, nan_box(z3.Extract(31, 0, cell)))
        return
    ops.write_float(0, cell)


def build_float_store(ops):
    width = FLOAT_STORE[ops.mnemonic]
    value = ops.read_float(0)
    if width == XLEN:
        ops.state.set_memory_cell(ops.texts[1], value)
        return
    kept = ops.state.memory_cell(ops.texts[1])
    low = z3.Extract(width - 1, 0, value)
    high = z3.Extract(XLEN - 1, width, kept)
    ops.state.set_memory_cell(ops.texts[1], z3.Concat(high, low))


# ------------------------------------------------------------------
# section 4b: the compressed forms -- a spelling, expanded, never a
# second meaning
# ------------------------------------------------------------------
#
# Each 16-bit instruction of the C extension IS one of the instructions
# above with its operands restricted.  The architecture manual defines each
# by its expansion, so this table holds the EXPANSION and the meaning stays
# in one place.  A function takes the compressed operand list and returns
# the base mnemonic's operand list.

def _same(texts):
    return list(texts)


def _destination_is_also_source(texts):
    return [texts[0], texts[0], texts[1]]


def _from_zero(texts):
    return [texts[0], "zero", texts[1]]


def _jump_no_link(texts):
    return ["zero", "0x0(%s)" % texts[0]]


def _jump_and_link(texts):
    return ["ra", "0x0(%s)" % texts[0]]


def _branch_against_zero(texts):
    return [texts[0], "zero", texts[1]]


def _jump_target(texts):
    return ["zero", texts[0]]


def _jump_target_linked(texts):
    return ["ra", texts[0]]


def _one_operand_against_zero(texts):
    """`c.zext.w rd` names ONE register and the manual defines it as
    `add.uw rd, rd, zero`: the register is both the destination and the
    first source, and the second source is the zero register."""
    return [texts[0], texts[0], "zero"]


COMPRESSED = {
    "c.add": ("add", _destination_is_also_source),
    "c.mv": ("add", _from_zero),
    "c.sub": ("sub", _destination_is_also_source),
    "c.and": ("and", _destination_is_also_source),
    "c.or": ("or", _destination_is_also_source),
    "c.xor": ("xor", _destination_is_also_source),
    "c.addw": ("addw", _destination_is_also_source),
    "c.subw": ("subw", _destination_is_also_source),
    "c.addi": ("addi", _destination_is_also_source),
    "c.addiw": ("addiw", _destination_is_also_source),
    "c.andi": ("andi", _destination_is_also_source),
    "c.li": ("addi", _from_zero),
    "c.slli": ("slli", _destination_is_also_source),
    "c.srli": ("srli", _destination_is_also_source),
    "c.srai": ("srai", _destination_is_also_source),
    "c.lui": ("lui", _same),
    "c.addi16sp": ("addi", _destination_is_also_source),
    "c.jr": ("jalr", _jump_no_link),
    "c.jalr": ("jalr", _jump_and_link),
    "c.j": ("jal", _jump_target),
    "c.jal": ("jal", _jump_target_linked),
    "c.beqz": ("beq", _branch_against_zero),
    "c.bnez": ("bne", _branch_against_zero),
    "c.ld": ("ld", _same),
    "c.lw": ("lw", _same),
    "c.sd": ("sd", _same),
    "c.sw": ("sw", _same),
    "c.ldsp": ("ld", _same),
    "c.lwsp": ("lw", _same),
    "c.sdsp": ("sd", _same),
    "c.swsp": ("sw", _same),
    "c.fld": ("fld", _same),
    "c.fsd": ("fsd", _same),
    "c.fldsp": ("fld", _same),
    "c.fsdsp": ("fsd", _same),
    # task rv3: the two Zcb forms clang 21 writes.  Each IS one of the
    # instructions above with its operands restricted, so the meaning
    # stays in one place and only the expansion is new.
    "c.mul": ("mul", _destination_is_also_source),
    "c.zext.w": ("add.uw", _one_operand_against_zero),
}


def expand_compressed(mnemonic, texts):
    """(base mnemonic, base operand list) for a compressed instruction, or
    nothing when the mnemonic is not one."""
    entry = COMPRESSED.get(mnemonic)
    if entry is None:
        return None
    base, rewrite = entry
    return base, rewrite(texts)


# ------------------------------------------------------------------
# section 5: opcode_table -- THE ONE TABLE (the sub-node)
# ------------------------------------------------------------------

NAMED = "the operands the instruction names"
DESTINATION = "the first named operand"
MEMORY = "memory"
THE_BRANCH_CONDITION = "the branch condition the walk forks on"
THE_PROGRAM_COUNTER = "the program counter"

TRAP_CAUSE = "a trap, and this reference walks a body in text order"


class Entry(object):
    """one arch instruction's meaning: which places it reads, which places
    it writes, and the builder that turns its operands into a z3 term."""

    def __init__(self, mnemonic, reads, writes, build, cause=None):
        self.mnemonic = mnemonic
        self.reads = tuple(reads)
        self.writes = tuple(writes)
        self.build = build
        self.cause = cause

    def __repr__(self):
        return "Entry(%r, reads=%r, writes=%r, modelled=%r)" % (
            self.mnemonic, self.reads, self.writes, self.build is not None)


class OpcodeTable(object):
    """THE one table from mnemonic to meaning."""

    def __init__(self):
        self.entries = {}
        self._install()

    def add(self, mnemonic, reads, writes, build, cause=None):
        self.entries[mnemonic] = Entry(mnemonic, reads, writes, build,
                                       cause)

    def add_many(self, mnemonics, reads, writes, build, cause=None):
        for mnemonic in mnemonics:
            self.add(mnemonic, reads, writes, build, cause)

    def _install(self):
        self.add_many(R_TYPE, (NAMED,), (DESTINATION,), build_r_type)
        self.add_many(R_TYPE_W, (NAMED,), (DESTINATION,), build_r_type_w)
        self.add_many(I_TYPE, (NAMED,), (DESTINATION,), build_i_type)
        self.add_many(SHIFT_I, (NAMED,), (DESTINATION,), build_shift_i)
        self.add_many(I_TYPE_W, (NAMED,), (DESTINATION,), build_i_type_w)
        self.add_many(SHIFT_I_W, (NAMED,), (DESTINATION,), build_shift_i_w)
        self.add("lui", (NAMED,), (DESTINATION,), build_upper)
        self.add("auipc", (NAMED, THE_PROGRAM_COUNTER), (DESTINATION,),
                 build_upper)
        self.add_many(MULTIPLY, (NAMED,), (DESTINATION,), build_multiply)
        self.add_many(MULTIPLY_W, (NAMED,), (DESTINATION,),
                      build_multiply_w)
        self.add_many(DIVIDE, (NAMED,), (DESTINATION,), build_divide)
        self.add_many(CONDITIONAL_ZERO, (NAMED,), (DESTINATION,),
                      build_conditional_zero,
                      "the Zicond extension, not RV64I+M; in the table "
                      "because a carved body spells it")
        self.add_many(DIVIDE_W, (NAMED,), (DESTINATION,), build_divide_w)
        self.add_many(ADD_UNSIGNED_WORD, (NAMED,), (DESTINATION,),
                      build_add_unsigned_word,
                      "the Zba extension, not RV64I+M; in the table "
                      "because carved bodies spell it (task rv3)")
        self.add_many(BIT_SET_I, (NAMED,), (DESTINATION,),
                      build_bit_set_immediate,
                      "the Zbs extension, not RV64I+M; in the table "
                      "because carved bodies spell it (task rv3)")
        self.add_many(FLOAT_SIGN_INJECT, (NAMED,), (DESTINATION,),
                      build_float_sign_inject,
                      "sign injection of the D extension; in the table "
                      "because a carved body spells it as the negate "
                      "idiom (task rv3)")
        self.add_many(LOAD, (MEMORY,), (DESTINATION,), build_load)
        self.add_many(STORE, (NAMED,), (MEMORY,), build_store)
        self.add_many(BRANCH, (NAMED,), (THE_BRANCH_CONDITION,),
                      build_branch)
        self.add_many(JUMP, (NAMED,), (DESTINATION,), build_jump)
        self.add_many(NO_OPERATION, (), (), build_no_operation)
        self.add_many(TRAP, (), (), None, TRAP_CAUSE)
        self.add_many(FLOAT_BINARY, (NAMED,), (DESTINATION,),
                      build_float_binary)
        self.add_many(FLOAT_FROM_INTEGER, (NAMED,), (DESTINATION,),
                      build_float_from_integer)
        self.add_many(FLOAT_WIDEN, (NAMED,), (DESTINATION,),
                      build_float_widen)
        self.add_many(FLOAT_MOVE, (NAMED,), (DESTINATION,),
                      build_float_move)
        self.add_many(FLOAT_COMPARE, (NAMED,), (DESTINATION,),
                      build_float_compare)
        self.add_many(FLOAT_LOAD, (MEMORY,), (DESTINATION,),
                      build_float_load)
        self.add_many(FLOAT_STORE, (NAMED,), (MEMORY,), build_float_store)

    def entry_for(self, mnemonic):
        return self.entries.get(mnemonic)

    def builder_for(self, mnemonic):
        entry = self.entries.get(mnemonic)
        if entry is None:
            return None
        return entry.build

    def without_a_builder(self):
        out = []
        for mnemonic in sorted(self.entries):
            if self.entries[mnemonic].build is None:
                out.append(mnemonic)
        return out


# ------------------------------------------------------------------
# section 6: RiscvReference -- the node's own class
# ------------------------------------------------------------------

RETURN_LINES = frozenset(["jalr zero, 0x0(ra)", "c.jr ra", "ret"])


class RiscvReference(object):
    """THE one symbolic simulator of the RISC-V machine."""

    def __init__(self):
        self.opcode_table = OpcodeTable()

    # -- the node's methods -------------------------------------------

    def simulate(self, body_text, arrival_contract=None,
                 shared_seed=None):
        """(body_text, arrival_contract) -> MachineState after the body."""
        state = MachineState(shared_seed)
        if arrival_contract:
            self.apply_arrival_contract(state, arrival_contract)
        self.walk_body(state, self.body_lines(body_text))
        return state

    def walk_body(self, state, lines):
        for line in lines:
            if line in RETURN_LINES:
                break
            self.step(state, line)
        return state

    def step(self, state, line):
        mnemonic, texts = self.split_line(line)
        expansion = expand_compressed(mnemonic, texts)
        if expansion is not None:
            mnemonic, texts = expansion
        entry = self.opcode_table.entry_for(mnemonic)
        if entry is None:
            raise NotModeled(
                "no entry in the riscv opcode table for %r (line %r)"
                % (mnemonic, line))
        if entry.build is None:
            raise NotModeled(
                "%r has no builder: %s (line %r)"
                % (mnemonic, entry.cause, line))
        ops = Operands(state, mnemonic, texts)
        entry.build(ops)

    def split_line(self, line):
        """`add a0, a1, a2` -> ('add', ['a0', 'a1', 'a2']).

        `llvm-objdump` appends a symbolic target to a transfer -- `jal ra,
        0x38 <op_1>` -- and that trailing `<...>` is the reader's aid, not
        an operand."""
        text = line.strip()
        text = re.sub(r"\s*<[^>]*>\s*$", "", text)
        parts = text.split(None, 1)
        if not parts:
            raise NotModeled("an empty body line")
        mnemonic = parts[0]
        if len(parts) == 1:
            return mnemonic, []
        return mnemonic, split_operands(parts[1])

    def body_lines(self, body_text):
        if isinstance(body_text, list):
            return [line for line in body_text if line.strip()]
        out = []
        for line in body_text.split(";"):
            if line.strip():
                out.append(line.strip())
        return out

    def apply_arrival_contract(self, state, arrival_contract):
        """bind each arriving value to the symbol the caller names.

        `arrival_contract` is a list of (place, term): the place is an
        integer register's ABI name or index, or a floating-point
        register's."""
        for place, term in arrival_contract:
            if isinstance(place, str) and place in FLOAT_REGISTERS and \
                    place not in INTEGER_REGISTERS:
                state.write_float(FLOAT_REGISTERS[place], term)
                continue
            if isinstance(place, str):
                if place not in INTEGER_REGISTERS:
                    raise NotModeled(
                        "arrival place %r is not a register of this "
                        "architecture" % place)
                state.bind(INTEGER_REGISTERS[place], term)
                continue
            state.bind(place, term)

    def answer_of(self, state, answer_home="a0"):
        """the term the body left in its answer place."""
        if answer_home in FLOAT_REGISTERS and \
                answer_home not in INTEGER_REGISTERS:
            return state.read_float(FLOAT_REGISTERS[answer_home])
        if answer_home not in INTEGER_REGISTERS:
            raise NotModeled(
                "answer home %r is not a register of this architecture"
                % answer_home)
        return state.read_register(INTEGER_REGISTERS[answer_home])
