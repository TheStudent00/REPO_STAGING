#!/usr/bin/env python3
"""reference.py -- THE ONE SYMBOLIC SIMULATOR OF THE MACHINE.

The code of node `hq.research.compiler_graph.reference`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_4_reference/CORE_0_3_5_4_reference.md`).
Its class is `Reference`; its methods are the CORE's `methods:`
(`simulate`, `answer_of`); its sub-nodes are its attribute
`opcode_table` and its class `MachineState`.

WHY IT EXISTS.  The pipeline carried FOUR reference simulators --
`canon9_behaviour_check.Sim9`, `canon10_behaviour_check.Sim10`,
`canon12_behaviour_check.Sim10`, and the one `gate48.py` reaches
through `canon10` -- and the 415-unit remainder withdrawal of log 153
was two of them disagreeing about one opcode.  There is exactly one
here.  `canon9`, `canon10` and `canon12` become superseded records and
are not edited beyond one header line each saying so.

WHAT THE ONE TABLE FOLDS IN, each named with the file it came from:

  * `layer4.py`'s producer table -- the integer, move, extension,
    shift and flag families, and its own `full64` / `cut` write rule.
  * `condition_table.py`'s condition route -- `SUFFIX_TO_COND` and
    `cond_to_z3` for every `set`/`cmov`/`j` suffix, and
    `layer4.float_condition` for the same suffixes read off a float
    or x87 comparison.
  * `vex_names.py`'s lane builders -- real IEEE terms under
    round-to-nearest-even, lane 0 written and the upper lanes kept
    (`build_lane_arith`'s own rule), NOT the uninterpreted functions
    `canon10_behaviour_check.py` carried.
  * `canon12_behaviour_check.py`'s division -- quotient `SDiv`/`UDiv`,
    remainder `SRem`/`URem`.  z3py's `%` on a bit vector is `bvsmod`,
    whose remainder follows the DIVISOR; x86's `idiv` leaves a
    remainder whose sign follows the DIVIDEND, which is `bvsrem`.
    `7, -3` gives `1` here and `-2` under `%` (log_153 section 5).

There is no second meanings table anywhere in this file.  Every
opcode's meaning is one `Entry` in `Reference.opcode_table.entries`,
and `builder_for` returns nothing for an opcode with no model -- that
"nothing" is what the census counts, never a silent gap.

THE HONEST LIMITS, named rather than hidden.

  * `simulate` walks the body in TEXT ORDER, which is exactly what the
    route the gate calls does today (`gate48.reference_answer` calls
    `answer_value` on the body's own lines).  A conditional transfer
    is refused by name, not guessed.  No branch-merging walk is added
    here: the CORE's `simulate` returns one `MachineState`, and a
    walk the tree does not state is not coded.
  * `call` is a transfer into a routine whose body is not in the unit.
    Where that routine is a compiler support routine (`__divti3` and
    its family) the owner's round-12 ruling (log_158, TASK 59(b)) is that
    the callee's body is EXTRACTED from the toolchain's libgcc /
    compiler-rt archive and attached as an ArchUnit the caller
    references, with the producer
    `{"kind": "runtime_callee", "callee": "__divti3"}`.  Task 59
    delivers that attachment (node 0_3_5_1_8 runtime_callee).  Until
    it lands the table carries `call` as an entry with NO builder and
    the honest refusal is "runtime callee not yet attached", NOT "out
    of scope" -- that earlier framing is superseded, and the
    superseded `out_of_scope_library_calls.json` keeps its list while
    its verdict is withdrawn.
  * `adc` and `sbb` set the flags from their own arithmetic, and this
    file records the triple they leave; the CARRY THEY READ ON THE WAY
    IN is taken as the carry the previous flag-setting opcode left,
    and is refused by name when there is no previous setter.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.  The table is keyed by ARCH
MNEMONIC, which is machine-form evidence read off the unit's own
disassembled body, never by the source spelling a probe was generated
from.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements.

usage:
  reference.py (library; `acceptance57.py` is this lap's driver)
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                  # noqa: E402
import condition_table as CT                                  # noqa: E402
import ledger as LEDGER                                       # noqa: E402
import ledger48 as L48                                        # noqa: E402
import z3                                                     # noqa: E402


class NotModeled(Exception):
    """the reference refuses this body by name, and says why."""


class LeavesTheUnit(Exception):
    """this line transfers OUT of the unit -- a panic path, a trap, or
    a `call` whose callee is not attached.  The side that takes it is
    unreachable and its condition becomes a guard row (reference CORE,
    2026-09-03, task 64)."""

    def __init__(self, line, target):
        Exception.__init__(self, "%s -> %s" % (line, target))
        self.line = line
        self.target = target


# ------------------------------------------------------------------
# section 1: the widths, the sorts, and the two name manglers
# ------------------------------------------------------------------

WIDTH_BITS = {0: 64, 1: 32, 2: 16, 3: 8}

XMM_NAMES = frozenset(["xmm%d" % i for i in range(16)])

FLOAT_SORT = {32: z3.Float32(), 64: z3.Float64()}

# an x87 register holds the 80-bit extended form: 15 exponent bits and
# a 64-bit significand.  THE SAME SORT `layer4c.X87_SORT` uses, so a
# reference term and a ledger term are comparable at all.
X87_SORT = z3.FPSort(15, 64)

X87_POSITIONS = L48.X87_POSITIONS

ROUNDING = z3.RNE()


def mangle(text):
    """`layer4c.mangle`, the same spelling, so `fldt 0x18(%rsp)` names
    `x87_0x18_rsp_` on both routes."""
    out = text.replace("%", "").replace("(", "_").replace(")", "_")
    out = out.replace(",", "_").replace("-", "m").replace("$", "i")
    out = out.replace("*", "s").replace("+", "p").replace(":", "_")
    return out


def memory_symbol_name(text):
    """the symbol a literal memory operand reads to.  `layer4.
    memory_load_term` writes `seed_MEM_<mangled>`; this spelling
    reproduces it character for character."""
    return "seed_MEM_%s" % mangle(text)


def x87_symbol(text):
    return z3.FP("x87_%s" % mangle(text), X87_SORT)


# THE BASE REGISTER IS OPTIONAL, task ap2, 2026-09-09.  `0x0(,%rdi,8)`
# is the same (displacement, base, index, scale) shape with the base
# slot EMPTY, which the machine reads as a base of zero: the address is
# displacement + index * scale.  Task ap1's loop met it 6 times, in
# bodies a compiler emitted for a shift-by-a-constant emulation, and
# `build_lea` refused the whole form because this expression required
# the base (log_243 section 6).  Nothing else about the shape changed:
# a form with neither a base nor an index is still not this shape.
LEA_RE = re.compile(
    r"^(-?0x[0-9a-f]+)?\((%\w+)?(?:,(%\w+),(\d+))?\)$")


def split_operands(rest):
    """split an AT&T operand list on top-level commas only."""
    out = []
    depth = 0
    cur = ""
    for ch in rest:
        if ch == "(":
            depth = depth + 1
            cur = cur + ch
            continue
        if ch == ")":
            depth = depth - 1
            cur = cur + ch
            continue
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
            continue
        cur = cur + ch
    if cur:
        out.append(cur)
    return [o.strip() for o in out]


def full64(value):
    """the machine's own write rule, `layer4.full64`: a sub-64-bit
    write into a general register zero-extends; a 64-bit write
    replaces."""
    if value.size() == 64:
        return value
    if value.size() > 64:
        return z3.Extract(63, 0, value)
    return z3.ZeroExt(64 - value.size(), value)


def cut(value, width):
    """`layer4.cut`."""
    if value.size() == width:
        return value
    if value.size() > width:
        return z3.Extract(width - 1, 0, value)
    return z3.ZeroExt(width - value.size(), value)


def as_float(bits, width):
    return z3.fpBVToFP(cut(bits, width), FLOAT_SORT[width])


def from_float(value):
    return z3.fpToIEEEBV(value)


# ------------------------------------------------------------------
# section 2: MachineState -- the sub-node
# ------------------------------------------------------------------

class MachineState(object):
    """the symbolic machine the reference walks a body over.

    Its five attributes are the five sub-nodes of
    `node_0_3_5_4_1_machine_state`:

      registers -- family -> term, seeded as `seed_<family>` free
                   symbols (128 bits for a vector family, 64 for the
                   rest), so a proof is about every input at once.
      flags     -- the (setter opcode, L, R) triple the last
                   flag-setting instruction left, or None.
      memory    -- literal operand text -> 128-bit term; an unwritten
                   cell reads one fixed unknown named
                   `seed_MEM_<mangled>`, a rip-relative read the k-th
                   `ripconst_<k>`.
      stack     -- the machine stack as (rsp term -> array): a
                   pointer term and cells keyed by the byte offset
                   from the rsp the unit was entered with, so a push
                   and its pop round trip.
      x87       -- eight positions and a top index, each position an
                   `FPSort(15, 64)` term.
    """

    def __init__(self, shared_seed=None):
        if shared_seed is None:
            shared_seed = {}
        self.shared_seed = shared_seed
        self.registers = {}
        self.flags = None
        self.memory = {}
        self.stack = {
            "pointer": self.seed("rsp"),
            "offset": 0,
            "cells": {},
        }
        self.x87 = {
            "slots": [None] * X87_POSITIONS,
            "top": 0,
            "depth": 0,
        }
        self.rip_reads = 0
        self.refusals = []
        self.branch_condition = None
        """the condition term the last `j<cc>` this walk stepped left
        behind.  A conditional transfer READS the flags and writes
        nothing; what the walk does with the condition is the
        control-flow rule, not the table's (opcode_table CORE,
        2026-09-03)."""
        self.guard_rows = []
        """one row per side of this body that transferred OUT of the
        unit: the condition under which it would have been taken, the
        line, and where it went.  The reference CORE's own words: "a
        transfer OUT of the unit on one side (a panic/trap) makes that
        side's state unreachable and the guard row records it"."""
        self.path_condition = z3.BoolVal(True)
        """the conjunction of the branch conditions this state was
        reached under.  Entry is True; a fork puts the condition on one
        side and its negation on the other; a merge folds the sides
        with `If(path condition, this side, the rest)`, which is sound
        because the sides out of one fork are disjoint and cover."""

    # -- forking and merging -----------------------------------------

    def fork(self):
        """a second state that starts where this one stands.  The
        SHARED SEED is shared, not copied: `seed_rdi` must be one
        symbol on both sides or the merge would compare two different
        unknowns."""
        other = MachineState(self.shared_seed)
        other.registers = dict(self.registers)
        other.flags = self.flags
        other.memory = dict(self.memory)
        other.stack = {
            "pointer": self.stack["pointer"],
            "offset": self.stack["offset"],
            "cells": dict(self.stack["cells"]),
        }
        other.x87 = {
            "slots": list(self.x87["slots"]),
            "top": self.x87["top"],
            "depth": self.x87["depth"],
        }
        other.rip_reads = self.rip_reads
        other.refusals = list(self.refusals)
        other.guard_rows = list(self.guard_rows)
        other.path_condition = self.path_condition
        return other

    # -- registers ---------------------------------------------------

    def seed(self, family):
        bits = 128 if family in XMM_NAMES else 64
        if family not in self.shared_seed:
            self.shared_seed[family] = z3.BitVec(
                "seed_%s" % family, bits)
        return self.shared_seed[family]

    def bind(self, family, term):
        """pre-bind a family to somebody else's symbol -- the arrival
        contract's job when a language's own calling rule parks an
        argument somewhere other than the designated register."""
        self.shared_seed[family] = term

    def family_value(self, family):
        if family in self.registers:
            return self.registers[family]
        value = self.seed(family)
        self.registers[family] = value
        return value

    def set_family(self, family, term):
        self.registers[family] = term

    # -- memory ------------------------------------------------------

    def memory_cell(self, text):
        if text in self.memory:
            return self.memory[text]
        name = memory_symbol_name(text)
        if name not in self.shared_seed:
            self.shared_seed[name] = z3.BitVec(name, 128)
        cell = self.shared_seed[name]
        self.memory[text] = cell
        return cell

    def set_memory_cell(self, text, term):
        self.memory[text] = cut(term, 128)

    def rip_constant(self, width):
        """the k-th rip-relative READ in this body gets the k-th fresh
        constant symbol -- the same positional keying `layer4.
        memory_load_term` uses, so the two routes name one constant."""
        name = "ripconst_%d" % self.rip_reads
        self.rip_reads = self.rip_reads + 1
        if name not in self.shared_seed:
            self.shared_seed[name] = z3.BitVec(name, 128)
        return cut(self.shared_seed[name], width)

    # -- the machine stack -------------------------------------------

    def push_value(self, term, size=8):
        self.stack["offset"] = self.stack["offset"] - size
        self.stack["pointer"] = self.stack["pointer"] - size
        self.stack["cells"][self.stack["offset"]] = cut(term, size * 8)

    def pop_value(self, size=8):
        offset = self.stack["offset"]
        if offset not in self.stack["cells"]:
            raise NotModeled(
                "a pop at stack offset %d that this body never wrote "
                "-- the value came from outside the unit" % offset)
        term = self.stack["cells"][offset]
        self.stack["offset"] = offset + size
        self.stack["pointer"] = self.stack["pointer"] + size
        return term

    # -- the x87 stack -----------------------------------------------

    def x87_at(self, position):
        index = (self.x87["top"] + position) % X87_POSITIONS
        value = self.x87["slots"][index]
        if value is None:
            raise NotModeled(
                "this body reads x87 stack position %d without having "
                "loaded it inside the body" % position)
        return value

    def x87_set(self, position, term):
        index = (self.x87["top"] + position) % X87_POSITIONS
        self.x87["slots"][index] = term

    def x87_push(self, term):
        if self.x87["depth"] >= X87_POSITIONS:
            raise NotModeled(
                "this body pushes a ninth value onto the x87 register "
                "stack, which has eight positions")
        self.x87["top"] = (self.x87["top"] - 1) % X87_POSITIONS
        self.x87["slots"][self.x87["top"]] = term
        self.x87["depth"] = self.x87["depth"] + 1

    def x87_pop(self):
        value = self.x87_at(0)
        self.x87["slots"][self.x87["top"]] = None
        self.x87["top"] = (self.x87["top"] + 1) % X87_POSITIONS
        self.x87["depth"] = self.x87["depth"] - 1
        return value


# ------------------------------------------------------------------
# section 3: the operand reader -- one place, used by every builder
# ------------------------------------------------------------------

IMMEDIATE_RE = re.compile(r"^\$(-?(?:0x[0-9a-fA-F]+|\d+))$")

# THE HIGH-BYTE REGISTERS.  `%ah` is bits 15..8 of the `%rax` family --
# not the low byte, and not a family of its own.  `canon.FAMILY_OF`
# holds no entry for them because no CANONICAL text names one; a body
# that divides at width 8 does, because the machine puts the remainder
# there (destination_rules CORE, 2026-09-03).  Five canon39 units
# stopped on `%ah` after task 64 modelled the division itself:
# `c/regen_15263`, `cpp/regen_14486`, `cpp/regen_14502`,
# `cpp/regen_15238`, `cpp/regen_15254`.
HIGH_BYTE_OF = {"ah": "rax", "bh": "rbx", "ch": "rcx", "dh": "rdx"}


class Operands(object):
    """the resolved operand slots of one body line, in the arch text's
    own order (AT&T: source first, destination last).  Every builder
    in the table reads its inputs through this object and through
    nothing else."""

    def __init__(self, state, mnemonic, texts):
        self.state = state
        self.mnemonic = mnemonic
        self.texts = texts

    # -- classification ----------------------------------------------

    def is_immediate(self, text):
        return IMMEDIATE_RE.match(text) is not None

    def is_register(self, text):
        if not text.startswith("%"):
            return False
        if text[1:] in HIGH_BYTE_OF:
            return True
        return canon.FAMILY_OF.get(text[1:]) is not None

    def is_high_byte(self, text):
        if not text.startswith("%"):
            return False
        return text[1:] in HIGH_BYTE_OF

    def is_vector(self, text):
        if not text.startswith("%"):
            return False
        return text[1:] in XMM_NAMES

    def is_memory(self, text):
        if self.is_segment_relative(text):
            return True
        if text.startswith("%"):
            return False
        if text.startswith("$"):
            return False
        return text.endswith(")")

    def is_segment_relative(self, text):
        """`%fs:0x28` is a read through a segment base, which is where
        the stack-protector cookie lives.  It is a MEMORY operand: a
        place, holding a value this reference does not otherwise
        know.  Reading it as an unconstrained memory cell is the same
        model every other memory operand gets, and it is the
        conservative one -- nothing is claimed about the value.

        Added 2026-09-03 (task 63) after eight attached archive bodies
        stopped on it: `__modti3`, `__umodti3`, `__floattixf`,
        `__floatuntixf` in clang's and clang++'s archives all begin by
        loading the cookie.
        """
        if not text.startswith("%"):
            return False
        if ":" not in text:
            return False
        segment = text.split(":", 1)[0]
        return segment in ("%fs", "%gs")

    def is_rip(self, text):
        return "(%rip)" in text

    def family_of(self, text):
        if text[1:] in HIGH_BYTE_OF:
            return HIGH_BYTE_OF[text[1:]]
        family = canon.FAMILY_OF.get(text[1:])
        if family is None:
            raise NotModeled(
                "register spelling %r is not in canon.py's FAMILY_OF "
                "table" % text)
        return family

    def width_of(self, text):
        if self.is_high_byte(text):
            return 8
        if self.is_vector(text):
            return 128
        code = canon.WIDTH_OF.get(text[1:])
        if code is None:
            raise NotModeled(
                "register spelling %r is not in canon.py's WIDTH_OF "
                "table" % text)
        return WIDTH_BITS[code]

    # -- reading ------------------------------------------------------

    def read(self, index, width=None):
        return self.read_text(self.texts[index], width)

    def read_text(self, text, width=None):
        if self.is_immediate(text):
            value = int(IMMEDIATE_RE.match(text).group(1), 0)
            if width is None:
                width = 64
            value = value & ((1 << width) - 1)
            return z3.BitVecVal(value, width)
        if self.is_high_byte(text):
            whole = self.state.family_value(HIGH_BYTE_OF[text[1:]])
            return cut(z3.Extract(15, 8, whole), width or 8)
        if self.is_register(text):
            own = self.width_of(text)
            if width is None:
                width = own
            family = self.family_of(text)
            return cut(self.state.family_value(family), width)
        if self.is_rip(text):
            if width is None:
                width = 64
            return self.state.rip_constant(width)
        if self.is_memory(text):
            if width is None:
                width = 64
            return cut(self.state.memory_cell(text), width)
        raise NotModeled(
            "operand %r is neither an immediate, a register nor a "
            "memory operand this file reads" % text)

    def read_128(self, index):
        text = self.texts[index]
        if self.is_vector(text):
            return self.state.family_value(self.family_of(text))
        if self.is_rip(text):
            return self.state.rip_constant(128)
        if self.is_memory(text):
            return self.state.memory_cell(text)
        raise NotModeled(
            "a 128-bit read of operand %r is not modeled" % text)

    # -- writing ------------------------------------------------------

    def write(self, index, term):
        self.write_text(self.texts[index], term)

    def write_text(self, text, term):
        if self.is_high_byte(text):
            family = HIGH_BYTE_OF[text[1:]]
            whole = self.state.family_value(family)
            self.state.set_family(
                family, place_bits(whole, cut(term, 8), 8))
            return
        if self.is_vector(text):
            self.state.set_family(self.family_of(text), cut(term, 128))
            return
        if self.is_register(text):
            self.state.set_family(self.family_of(text), full64(term))
            return
        if self.is_memory(text):
            self.state.set_memory_cell(text, term)
            return
        raise NotModeled(
            "operand %r is not a place this file can write" % text)

    @property
    def destination(self):
        return self.texts[-1]

    def destination_width(self):
        return self.width_at(len(self.texts) - 1)

    def width_at(self, index):
        """the width of one operand slot.  A register states its own
        width; a MEMORY operand states none, so the width comes from
        the mnemonic's own AT&T size letter, and failing that from
        another operand that does state one."""
        text = self.texts[index]
        if self.is_register(text):
            return self.width_of(text)
        if not self.is_memory(text):
            raise NotModeled(
                "operand %r states no width" % text)
        suffixed = SIZE_LETTER.get(self.mnemonic[-1:])
        if suffixed is not None and self.mnemonic not in \
                WIDTH_IS_NOT_A_SUFFIX:
            return suffixed
        for other in self.texts:
            if other is text:
                continue
            if self.is_register(other):
                return self.width_of(other)
        raise NotModeled(
            "the memory operand %r of %r states no width, and no "
            "other operand of the line states one"
            % (text, self.mnemonic))


# ------------------------------------------------------------------
# section 4: the term builders -- one per family, no second table
# ------------------------------------------------------------------
#
# Every builder has the same shape: it takes the resolved `Operands`
# of one body line and applies that line's own meaning to the machine
# state.  The families are the four the opcode_table CORE names --
# integer arithmetic and logic, conditions, floating point, vector
# lanes -- plus the machine stack and the x87 stack the machine_state
# CORE names.

SIZE_LETTER = {"b": 8, "w": 16, "l": 32, "q": 64}

# mnemonics whose final letter is NOT an operand-size letter, listed so
# the width rule above never reads one as a size.
WIDTH_IS_NOT_A_SUFFIX = frozenset([
    "mul", "imul", "idiv", "div", "call", "sal", "shl", "cmovl",
    "cmovbe", "cmovb", "cmovle", "cmovge", "cmovae", "setl", "setb",
    "setbe", "setle", "setge", "setae", "jl", "jb", "jbe", "jle",
    "jge", "jae", "pand", "por", "movsbw", "movzbw",
])

LOW_REGISTER = {8: "%al", 16: "%ax", 32: "%eax", 64: "%rax"}
HIGH_REGISTER = {8: "%ah", 16: "%dx", 32: "%edx", 64: "%rdx"}

SIGN_EXTEND = {
    "movslq": (32, 64), "movsbl": (8, 32), "movsbq": (8, 64),
    "movswl": (16, 32), "movswq": (16, 64), "movsbw": (8, 16),
    "movsl": (32, 64), "movsx": None, "movsxd": (32, 64),
}
ZERO_EXTEND = {
    "movzbl": (8, 32), "movzbq": (8, 64), "movzwl": (16, 32),
    "movzwq": (16, 64), "movzbw": (8, 16), "movzx": None,
}
ACCUMULATOR_WIDEN = {"cltq": (32, 64), "cwtl": (16, 32),
                     "cbtw": (8, 16)}
SPREAD_SIGN = {"cltd": 32, "cqto": 64, "cqo": 64, "cwtd": 16}
PLAIN_MOVE = frozenset(["mov", "movl", "movq", "movb", "movw",
                        "movabs"])
BINARY = frozenset(["add", "sub", "and", "or", "xor", "imul"])
UNARY = frozenset(["not", "neg"])
SHIFT = frozenset(["shl", "shr", "sar", "sal"])
DOUBLE_SHIFT = frozenset(["shld", "shrd"])
CARRY_BINARY = frozenset(["adc", "sbb"])
FLAG_ONLY = frozenset(["cmp", "test"])
DIVISION = frozenset(["idiv", "div"])
WIDE_MULTIPLY = frozenset(["imul", "mul"])
FLOAT_FLAG_ONLY = frozenset(["ucomiss", "ucomisd", "comiss",
                             "comisd"])
FLOAT_BINARY = {
    "addss": ("add", 32), "addsd": ("add", 64),
    "subss": ("sub", 32), "subsd": ("sub", 64),
    "mulss": ("mul", 32), "mulsd": ("mul", 64),
    "divss": ("div", 32), "divsd": ("div", 64),
}
PACKED_FLOAT = {
    "addps": ("add", 32), "addpd": ("add", 64),
    "subps": ("sub", 32), "subpd": ("sub", 64),
    "mulps": ("mul", 32), "mulpd": ("mul", 64),
    "divps": ("div", 32), "divpd": ("div", 64),
}
FLOAT_COMPARE_MASK = {
    "cmpeqss": ("eq", 32), "cmpeqsd": ("eq", 64),
    "cmpneqss": ("ne", 32), "cmpneqsd": ("ne", 64),
}
BITWISE_128 = {
    "xorps": "xor", "xorpd": "xor", "pxor": "xor",
    "orps": "or", "orpd": "or", "por": "or",
    "andps": "and", "andpd": "and", "pand": "and",
}
LANE_MOVE = {"movss": 32, "movsd": 64, "movd": 32, "movq128": 64}
WHOLE_MOVE = frozenset(["movaps", "movapd", "movups", "movupd",
                        "movdqa", "movdqu"])
CONVERT_TO_FLOAT = {
    "cvtsi2ss": 32, "cvtsi2sd": 64, "cvtsi2ssl": 32,
    "cvtsi2sdl": 64, "cvtsi2ssq": 32, "cvtsi2sdq": 64,
}
NO_OPERATION = frozenset(["nop", "nopl", "nopw", "ret", "endbr64",
                          "cs"])
TRANSFER = frozenset(["call", "jmp", "ud2"])


def shift_mask(width):
    if width == 64:
        return 0x3F
    return 0x1F


def build_plain_move(ops):
    if ops.is_vector(ops.texts[0]) or ops.is_vector(ops.texts[1]):
        build_lane_move(ops)
        return
    width = ops.destination_width()
    ops.write(1, ops.read(0, width))
    return


def build_lea(ops):
    text = ops.texts[0]
    hit = LEA_RE.match(text)
    if hit is None:
        raise NotModeled(
            "lea addressing form %r is not the (displacement, base, "
            "index, scale) shape this file models" % text)
    displacement, base, index, scale = hit.groups()
    if base is None and index is None:
        raise NotModeled(
            "lea addressing form %r names neither a base register nor "
            "an index register, so there is no address to compute"
            % text)
    if base == "%rip":
        # A RIP-RELATIVE ADDRESS COMPUTATION IS THE BODY'S NEXT
        # `ripconst_<k>` (machine_state CORE, 2026-09-03, task 64).
        # `lea 0x2e57(%rip),%rax` computes an address this artifact
        # does not hold, exactly as a rip-relative READ returns a value
        # it does not hold; both are keyed by their position in the
        # body, off the ONE counter, so this file and the ledger
        # transcription name one constant.
        ops.write(1, cut(ops.state.rip_constant(64),
                         ops.destination_width()))
        return
    if base is None:
        # THE EMPTY BASE SLOT IS A BASE OF ZERO (task ap2): the form
        # `0x0(,%rdi,8)` computes displacement + index * scale, and
        # this is the one line that says so.
        address = z3.BitVecVal(0, 64)
    else:
        base_family = canon.FAMILY_OF.get(base[1:])
        if base_family is None:
            raise NotModeled(
                "an address computation over base register %r: this "
                "reference has no model for the address that register "
                "holds, only for the value a read through it returns"
                % base)
        address = ops.state.family_value(base_family)
    if index is not None:
        index_value = ops.state.family_value(
            canon.FAMILY_OF[index[1:]])
        address = address + index_value * int(scale)
    if displacement is not None:
        address = address + z3.BitVecVal(int(displacement, 16), 64)
    ops.write(1, cut(address, ops.destination_width()))


def build_extension(ops, table, signed):
    text = ops.texts[0]
    pair = table[ops.mnemonic]
    if pair is None:
        source_width = ops.width_of(text)
        destination_width = ops.destination_width()
    else:
        source_width, destination_width = pair
    value = ops.read(0, source_width)
    if signed:
        grown = z3.SignExt(destination_width - source_width, value)
    else:
        grown = z3.ZeroExt(destination_width - source_width, value)
    ops.write(1, grown)


def build_accumulator_widen(ops):
    source_width, destination_width = ACCUMULATOR_WIDEN[ops.mnemonic]
    value = ops.read_text(LOW_REGISTER[source_width], source_width)
    grown = z3.SignExt(destination_width - source_width, value)
    ops.write_text(LOW_REGISTER[destination_width], grown)


def build_spread_sign(ops):
    """`cltd`/`cqto`/`cqo`/`cwtd`: the data register becomes the
    accumulator's sign bits, an arithmetic right shift by width-1."""
    width = SPREAD_SIGN[ops.mnemonic]
    value = ops.read_text(LOW_REGISTER[width], width)
    ops.write_text(HIGH_REGISTER[width],
                   value >> z3.BitVecVal(width - 1, width))


def build_binary(ops):
    if len(ops.texts) == 1:
        # CORRECTED 2026-09-08 by task m1b (log_236 section 9, second
        # item).  This branch used to send EVERY one-operand line of
        # the binary family to the widening multiply, so `add %edi`
        # was modelled as `%eax = %edi * %eax`, and the same for
        # `and`, `or`, `sub` and `xor` -- 24 table rows the corpus
        # attests zero times.  The one-operand form is the
        # accumulator-pair widening multiply and belongs to the two
        # mnemonics that spell it.
        if ops.mnemonic in WIDE_MULTIPLY:
            build_wide_multiply(ops)
            return
        raise NotModeled(
            "a one-operand line of %r is not modeled: the one-operand "
            "form is the accumulator-pair widening multiply, which is "
            "not this mnemonic's" % ops.mnemonic)
    width = ops.destination_width()
    left = ops.read(1, width)
    right = ops.read(0, width)
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
    else:
        result = left * right
    ops.write(1, result)
    if mnemonic in ("and", "or", "xor"):
        # CORRECTED 2026-09-03 by task 58's gate (log_160 section 3).
        # The logic family leaves ZF and SF from its RESULT and clears
        # the carry and the overflow; it does not leave a comparison
        # of its two operands.  Recording `(mnemonic, left, right)`
        # here made `setne` after `or %rsi,%rdi` read
        # `seed_rdi != seed_rsi` where the machine reads
        # `(seed_rdi | seed_rsi) != 0` -- 1,338 units on which route
        # one disproved a term route two proved.  The shape is the one
        # this file already uses for `test`
        # (`("test", left & right, 0)`), and `carry_bit` /
        # `overflow_bit` already answer False for this family by
        # setter name, so nothing else moves.
        ops.state.flags = (mnemonic, result,
                           z3.BitVecVal(0, result.size()))
        return
    ops.state.flags = (mnemonic, left, right)


def build_unary(ops):
    width = ops.destination_width()
    value = ops.read(0, width)
    if ops.mnemonic == "not":
        result = ~value
    else:
        result = -value
    ops.write(0, result)
    if ops.mnemonic == "neg":
        ops.state.flags = ("neg", value, z3.BitVecVal(0, width))


def build_increment(ops):
    """`inc` adds one to its one named operand.

    THE CARRY IS THE POINT.  `inc` leaves the carry flag EXACTLY as it
    found it -- that is the one way it differs from `add $1`.  So the
    flag triple it records names itself, `("inc", result, 0)`, which
    answers the zero and sign readings from the result the way the
    logic family does, and makes `carry_bit` refuse: a carry read
    after `inc` is a carry this body's earlier opcode set, and this
    reference does not carry flag state across opcodes.
    """
    width = ops.destination_width()
    value = ops.read(0, width)
    result = value + z3.BitVecVal(1, width)
    ops.write(0, result)
    ops.state.flags = ("inc", result, z3.BitVecVal(0, width))


def build_exchange(ops):
    """`xchg a,b` swaps the two places it names.  Read both before
    either is written, or the second write reads the first's result.

    `xchg %ax,%ax` is the two-byte no-operation the assembler emits
    for alignment; it falls out of the same rule with no special
    case."""
    width = ops.destination_width()
    left = ops.read(0, width)
    right = ops.read(1, width)
    ops.write(0, right)
    ops.write(1, left)


def build_bit_test(ops):
    """`bt $n,%r` copies bit n of its second operand into the carry
    flag and touches nothing else.

    The flag triple records `("bt", value, index)` and `carry_bit`
    reads the bit out of it.  A reading OTHER than the carry after a
    `bt` is refused rather than guessed: `bt` leaves the zero and sign
    flags undefined."""
    index_text = ops.texts[0]
    if not ops.is_immediate(index_text):
        raise NotModeled(
            "a bit test whose index %r is not an immediate is not "
            "modeled" % index_text)
    width = ops.width_at(1)
    value = ops.read(1, width)
    index = int(IMMEDIATE_RE.match(index_text).group(1), 0)
    index = index % width
    ops.state.flags = ("bt", value, z3.BitVecVal(index, width))


def build_bit_scan_reverse(ops):
    """`bsr source,destination` writes the POSITION of the highest set
    bit of the source, counting from zero at the low end.

    A source of zero leaves the destination undefined on the machine,
    so this builder leaves the destination's own previous value there
    and records `("bsr", source, 0)` as the flag triple -- which is
    exactly the zero test the bodies that use it perform before they
    read the destination (`test %eax,%eax` / `je` guards every
    `bsr` in the attached bodies).
    """
    width = ops.width_at(0)
    source = ops.read(0, width)
    destination_width = ops.destination_width()
    result = ops.read(1, destination_width)
    zero = z3.BitVecVal(0, width)
    for position in range(width):
        bit = z3.Extract(position, position, source)
        result = z3.If(bit == z3.BitVecVal(1, 1),
                       z3.BitVecVal(position, destination_width),
                       result)
    ops.write(1, result)
    ops.state.flags = ("bsr", source, zero)


def build_insert_word(ops):
    """`pinsrw $n,source,%xmm` writes the low 16 bits of the source
    into lane n of the vector, leaving the other seven lanes."""
    index_text, source_text, destination_text = ops.texts
    if not ops.is_immediate(index_text):
        raise NotModeled(
            "a word insertion whose index %r is not an immediate is "
            "not modeled" % index_text)
    index = int(IMMEDIATE_RE.match(index_text).group(1), 0) % 8
    old = ops.read_128(2)
    fresh = ops.read_text(source_text, 16)
    pieces = []
    for position in range(8):
        if position == index:
            pieces.append(fresh)
            continue
        pieces.append(lane(old, position, 16))
    pieces.reverse()
    ops.write(2, z3.Concat(*pieces))


def build_carry_binary(ops):
    """`adc`/`sbb` read the carry the previous flag-setting opcode
    left, and set the flags from their own arithmetic."""
    width = ops.destination_width()
    left = ops.read(1, width)
    right = ops.read(0, width)
    carry_in = carry_bit(ops.state.flags)
    carry_value = z3.If(carry_in, z3.BitVecVal(1, width),
                        z3.BitVecVal(0, width))
    if ops.mnemonic == "adc":
        result = left + right + carry_value
    else:
        result = left - right - carry_value
    ops.write(1, result)
    ops.state.flags = (ops.mnemonic, left, right)


def build_shift(ops):
    width = ops.destination_width()
    count_text = ops.texts[0]
    if count_text == "%cl":
        count = ops.read_text("%cl", 8)
    elif ops.is_immediate(count_text):
        count = cut(ops.read_text(count_text, 8), 8)
    else:
        raise NotModeled(
            "a shift count operand %r that is neither %%cl nor an "
            "immediate is not modeled" % count_text)
    masked = count & z3.BitVecVal(shift_mask(width), 8)
    if width > 8:
        amount = z3.ZeroExt(width - 8, masked)
    else:
        amount = masked
    value = ops.read(1, width)
    if ops.mnemonic in ("shl", "sal"):
        result = value << amount
    elif ops.mnemonic == "shr":
        result = z3.LShR(value, amount)
    else:
        result = value >> amount
    ops.write(1, result)


def build_double_shift(ops):
    """`shld`/`shrd count, source, destination`: the destination
    shifted, with the vacated bits filled from the source."""
    width = ops.destination_width()
    count_text = ops.texts[0]
    if count_text == "%cl":
        count = ops.read_text("%cl", 8)
    elif ops.is_immediate(count_text):
        count = cut(ops.read_text(count_text, 8), 8)
    else:
        raise NotModeled(
            "a double-shift count operand %r that is neither %%cl nor "
            "an immediate is not modeled" % count_text)
    masked = count & z3.BitVecVal(shift_mask(width), 8)
    amount = z3.ZeroExt(2 * width - 8, masked)
    source = ops.read(1, width)
    destination = ops.read(2, width)
    if ops.mnemonic == "shld":
        wide = z3.Concat(destination, source)
        result = z3.Extract(2 * width - 1, width, wide << amount)
    else:
        wide = z3.Concat(source, destination)
        result = z3.Extract(width - 1, 0, z3.LShR(wide, amount))
    ops.write(2, result)


def build_flag_only(ops):
    width = ops.destination_width()
    left = ops.read(1, width)
    right = ops.read(0, width)
    if ops.mnemonic == "test":
        ops.state.flags = ("test", left & right,
                           z3.BitVecVal(0, width))
        return
    ops.state.flags = ("cmp", left, right)


def build_division(ops):
    """THE CAREFUL CASE.  Quotient `SDiv`/`UDiv`; remainder
    `SRem`/`URem`, whose sign follows the DIVIDEND.  Never z3's `%`
    (`bvsmod`), whose sign follows the divisor -- log_153 section 5,
    counterexample `7 % -3`."""
    width = ops.width_at(0)
    if width in (8, 16):
        build_narrow_division(ops, width)
        return
    if width not in (32, 64):
        raise NotModeled(
            "a division at width %d is not modeled" % width)
    low = ops.read_text(LOW_REGISTER[width], width)
    high = ops.read_text(HIGH_REGISTER[width], width)
    dividend = z3.Concat(high, low)
    divisor = ops.read(0, width)
    if ops.mnemonic == "idiv":
        wide = z3.SignExt(width, divisor)
        quotient = dividend / wide
        remainder = z3.SRem(dividend, wide)
    else:
        wide = z3.ZeroExt(width, divisor)
        quotient = z3.UDiv(dividend, wide)
        remainder = z3.URem(dividend, wide)
    ops.write_text(LOW_REGISTER[width],
                   z3.Extract(width - 1, 0, quotient))
    ops.write_text(HIGH_REGISTER[width],
                   z3.Extract(width - 1, 0, remainder))


def place_bits(old, value, offset):
    """`value` placed at bit `offset` of `old`, every other bit of
    `old` kept.

    THE MACHINE'S OWN DESTINATION-WIDTH RULE, and the reason this
    function exists rather than `full64`: a 64-bit write replaces and a
    32-bit write zero-extends, but an 8- or 16-bit write LEAVES THE
    UPPER BITS ALONE (`mov $1,%al` does not clear `%rax`).  Only the
    narrow division and widening-multiply forms below write at those
    widths into a register they do not name, so only they use this;
    `full64` is untouched for every other opcode.  Rule:
    machine_state CORE, 2026-09-03 (task 64).
    """
    width = value.size()
    pieces = []
    if offset + width < old.size():
        pieces.append(z3.Extract(old.size() - 1, offset + width, old))
    pieces.append(value)
    if offset > 0:
        pieces.append(z3.Extract(offset - 1, 0, old))
    if len(pieces) == 1:
        return pieces[0]
    return z3.Concat(*pieces)


def build_narrow_division(ops, width):
    """DIVISION AT WIDTH 8 AND 16, whose answers land in two parts of
    ONE register rather than in two register families.

    At width 8 the dividend is `AX` -- the whole 16-bit accumulator,
    not a pair -- and the quotient goes to `AL` while the remainder
    goes to `AH`.  At width 16 the dividend is `DX:AX` and the answers
    are `AX` and `DX`.  Rows: the destination_rules CORE's own table,
    2026-09-03 (task 64); 15 of the 20 units of log_160 section 1.7.
    """
    signed = ops.mnemonic == "idiv"
    divisor = ops.read(0, width)
    accumulator = ops.state.family_value("rax")
    if width == 8:
        dividend = z3.Extract(15, 0, accumulator)
        wide = 16
    else:
        low = z3.Extract(15, 0, accumulator)
        high = z3.Extract(15, 0, ops.state.family_value("rdx"))
        dividend = z3.Concat(high, low)
        wide = 32
    if signed:
        grown = z3.SignExt(wide - width, divisor)
        quotient = dividend / grown
        remainder = z3.SRem(dividend, grown)
    else:
        grown = z3.ZeroExt(wide - width, divisor)
        quotient = z3.UDiv(dividend, grown)
        remainder = z3.URem(dividend, grown)
    quotient = z3.Extract(width - 1, 0, quotient)
    remainder = z3.Extract(width - 1, 0, remainder)
    if width == 8:
        ops.state.set_family(
            "rax", place_bits(accumulator,
                              z3.Concat(remainder, quotient), 0))
        return
    ops.state.set_family("rax", place_bits(accumulator, quotient, 0))
    ops.state.set_family(
        "rdx", place_bits(ops.state.family_value("rdx"), remainder, 0))


def build_narrow_wide_multiply(ops, width):
    """A ONE-OPERAND WIDENING MULTIPLY AT WIDTH 8 AND 16.

    At width 8 the whole product IS `AX` -- there is no high half to
    put anywhere.  At width 16 it is `DX:AX`.  Rows: the
    destination_rules CORE's table, 2026-09-03 (task 64); 5 of the 20
    units of log_160 section 1.7.
    """
    signed = ops.mnemonic == "imul"
    accumulator = ops.state.family_value("rax")
    low = z3.Extract(width - 1, 0, accumulator)
    other = ops.read(0, width)
    if signed:
        product = z3.SignExt(width, low) * z3.SignExt(width, other)
    else:
        product = z3.ZeroExt(width, low) * z3.ZeroExt(width, other)
    if width == 8:
        ops.state.set_family("rax", place_bits(accumulator, product, 0))
        return
    ops.state.set_family(
        "rax", place_bits(accumulator,
                          z3.Extract(width - 1, 0, product), 0))
    ops.state.set_family(
        "rdx", place_bits(ops.state.family_value("rdx"),
                          z3.Extract(2 * width - 1, width, product), 0))


def build_wide_multiply(ops):
    width = ops.width_at(0)
    if width in (8, 16):
        build_narrow_wide_multiply(ops, width)
        return
    if width not in (32, 64):
        raise NotModeled(
            "a widening multiply at width %d is not modeled: its "
            "destination pair is the accumulator's own two halves, "
            "which are not two families" % width)
    low = ops.read_text(LOW_REGISTER[width], width)
    other = ops.read(0, width)
    if ops.mnemonic == "imul":
        product = z3.SignExt(width, low) * z3.SignExt(width, other)
    else:
        product = z3.ZeroExt(width, low) * z3.ZeroExt(width, other)
    ops.write_text(LOW_REGISTER[width],
                   z3.Extract(width - 1, 0, product))
    ops.write_text(HIGH_REGISTER[width],
                   z3.Extract(2 * width - 1, width, product))


def build_push(ops):
    ops.state.push_value(ops.read(0, ops.width_at(0)), 8)


def build_pop(ops):
    value = ops.state.pop_value(8)
    ops.write(0, value)


# -- conditions ----------------------------------------------------

def carry_bit(flags):
    """the carry the flag triple leaves, rebuilt from the setter and
    its two sides -- never remembered as a separate bit."""
    if flags is None:
        raise NotModeled(
            "this opcode reads the carry bit and no flag-setting arch "
            "opcode precedes it in this body")
    setter, left, right = flags
    if setter == MERGED_SETTER:
        raise NotModeled(MERGED_FLAG_REFUSAL)
    if setter in ("sub", "cmp", "sbb"):
        return z3.ULT(left, right)
    if setter in ("add", "adc"):
        width = left.size()
        wide = z3.ZeroExt(1, left) + z3.ZeroExt(1, right)
        return z3.Extract(width, width, wide) == z3.BitVecVal(1, 1)
    if setter in ("and", "or", "xor", "test"):
        return z3.BoolVal(False)
    if setter == "neg":
        return left != z3.BitVecVal(0, left.size())
    if setter == "bt":
        # `bt` put ONE bit of `left` into the carry, and `right` holds
        # which bit.  The index is an immediate, so it is a literal
        # here and `Extract` takes it directly.
        index = right.as_long()
        return z3.Extract(index, index, left) == z3.BitVecVal(1, 1)
    raise NotModeled(
        "this opcode reads the carry bit and the flag-setting arch "
        "opcode %r has no carry model in this file" % setter)


def overflow_bit(flags):
    if flags is None:
        raise NotModeled(
            "this opcode reads the signed-overflow bit and no "
            "flag-setting arch opcode precedes it in this body")
    setter, left, right = flags
    if setter == MERGED_SETTER:
        raise NotModeled(MERGED_FLAG_REFUSAL)
    width = left.size()
    if setter == "neg":
        return left == z3.BitVecVal(1 << (width - 1), width)
    if setter in ("add", "adc"):
        wide = z3.SignExt(1, left) + z3.SignExt(1, right)
    elif setter in ("sub", "cmp", "sbb"):
        wide = z3.SignExt(1, left) - z3.SignExt(1, right)
    elif setter in ("and", "or", "xor", "test"):
        return z3.BoolVal(False)
    else:
        raise NotModeled(
            "this opcode reads the signed-overflow bit and the "
            "flag-setting arch opcode %r has no overflow model in "
            "this file" % setter)
    return z3.Extract(width, width, wide) != \
        z3.Extract(width - 1, width - 1, wide)


FLOAT_SETTERS = frozenset(
    list(FLOAT_FLAG_ONLY) + list(L48.X87_COMPARE_POP) +
    list(L48.X87_COMPARE_KEEP))


def predicate_of(state, suffix):
    """THE CONDITION ROUTE, `condition_table.py`'s own: the suffix
    names a synthetic condition, and the condition is read off the
    (setter, L, R) triple the last flag-setting opcode left."""
    if suffix in ("o", "no"):
        overflow = overflow_bit(state.flags)
        if suffix == "o":
            return overflow
        return z3.Not(overflow)
    if state.flags is None:
        raise NotModeled(
            "a flag-reading arch opcode with no flag-setting arch "
            "opcode before it in this body")
    setter, left, right = state.flags
    if setter == MERGED_SETTER:
        raise NotModeled(MERGED_FLAG_REFUSAL)
    if suffix not in CT.SUFFIX_TO_COND:
        raise NotModeled(
            "condition suffix %r is not in condition_table.py's "
            "SUFFIX_TO_COND" % suffix)
    condition = CT.SUFFIX_TO_COND[suffix]
    if setter in FLOAT_SETTERS:
        return float_condition(condition, left, right)
    if setter not in ("cmp", "test") and \
            suffix in ("b", "c", "nae", "ae", "nb", "nc"):
        carry = carry_bit(state.flags)
        if suffix in ("b", "c", "nae"):
            return carry
        return z3.Not(carry)
    if setter == "bt":
        raise NotModeled(
            "the condition %r is read after `bt`, which sets only the "
            "carry flag and leaves the zero and sign flags undefined"
            % suffix)
    return CT.cond_to_z3(condition, left, right, z3)


def float_condition(condition, left, right):
    """the x86 unordered-compare flag rule, the same one
    `layer4.float_condition` writes: ZF, PF and CF are all set when
    either side is NaN."""
    unordered = z3.Or(z3.fpIsNaN(left), z3.fpIsNaN(right))
    equal = z3.fpEQ(left, right)
    below = z3.fpLT(left, right)
    if condition == "CondEQ":
        return z3.And(equal, z3.Not(unordered))
    if condition == "CondNE":
        return z3.Or(z3.Not(equal), unordered)
    if condition == "CondULT":
        return z3.Or(below, unordered)
    if condition == "CondUGE":
        return z3.And(z3.Not(below), z3.Not(unordered))
    if condition == "CondUGT":
        return z3.And(z3.Not(below), z3.Not(equal),
                      z3.Not(unordered))
    if condition == "CondULE":
        return z3.Or(below, equal, unordered)
    if condition == "CondPAR":
        return unordered
    if condition == "CondNPAR":
        return z3.Not(unordered)
    raise NotModeled(
        "condition %r has no float-flag reading written for it"
        % condition)


def build_set_condition(ops):
    suffix = ops.mnemonic[3:]
    predicate = predicate_of(ops.state, suffix)
    ops.write(0, z3.If(predicate, z3.BitVecVal(1, 8),
                       z3.BitVecVal(0, 8)))


def build_move_condition(ops):
    suffix = ops.mnemonic[4:]
    predicate = predicate_of(ops.state, suffix)
    width = ops.destination_width()
    old = ops.read(1, width)
    new = ops.read(0, width)
    ops.write(1, z3.If(predicate, new, old))


def build_branch_condition(ops):
    """`j<cc>` READS the flags and writes no place.  It leaves the
    condition term on the state, and the walk decides what to do with
    it -- fork, or drop the side that leaves the unit.

    THE BUILDER IS THE SAME ONE `set<cc>` AND `cmov<cc>` USE
    (`predicate_of`, through `condition_table.py`), which is the
    opcode_table CORE's rule of 2026-09-03: a conditional transfer is
    an entry with a condition builder, not a census row.  Before task
    64 this function raised "this reference walks a body in text order
    and refuses a branch rather than guessing which side runs", and
    499 units stopped on it (log_160 section 1.7).
    """
    suffix = ops.mnemonic[1:]
    ops.state.branch_condition = predicate_of(ops.state, suffix)


def build_transfer(ops):
    raise NotModeled(
        "an unconditional transfer or trap (%r): this reference walks "
        "a body in text order" % ops.mnemonic)


# -- floating point and vector lanes --------------------------------

def lane(value128, index, width):
    low = index * width
    return z3.Extract(low + width - 1, low, value128)


def set_low_lane(old128, value, width):
    """the merge rule `vex_names.build_lane_arith` follows: lane 0 is
    written and the upper lanes are kept."""
    if width == 128:
        return value
    return z3.Concat(z3.Extract(127, width, old128), value)


def float_arithmetic(kind, left, right):
    if kind == "add":
        return z3.fpAdd(ROUNDING, left, right)
    if kind == "sub":
        return z3.fpSub(ROUNDING, left, right)
    if kind == "mul":
        return z3.fpMul(ROUNDING, left, right)
    if kind == "div":
        return z3.fpDiv(ROUNDING, left, right)
    raise NotModeled(
        "no float arithmetic is written for %r" % kind)


def build_float_binary(ops):
    kind, width = FLOAT_BINARY[ops.mnemonic]
    destination = ops.read_128(1)
    left = as_float(lane(destination, 0, width), width)
    right = as_float(ops.read(0, width), width)
    result = from_float(float_arithmetic(kind, left, right))
    ops.write(1, set_low_lane(destination, result, width))


def build_packed_float(ops):
    kind, width = PACKED_FLOAT[ops.mnemonic]
    destination = ops.read_128(1)
    source = ops.read_128(0)
    lanes = []
    for index in range(128 // width):
        left = as_float(lane(destination, index, width), width)
        right = as_float(lane(source, index, width), width)
        lanes.append(from_float(float_arithmetic(kind, left, right)))
    lanes.reverse()
    ops.write(1, z3.Concat(*lanes))


def build_float_compare_mask(ops):
    kind, width = FLOAT_COMPARE_MASK[ops.mnemonic]
    destination = ops.read_128(1)
    left = as_float(lane(destination, 0, width), width)
    right = as_float(ops.read(0, width), width)
    unordered = z3.Or(z3.fpIsNaN(left), z3.fpIsNaN(right))
    equal = z3.And(z3.fpEQ(left, right), z3.Not(unordered))
    if kind == "eq":
        taken = equal
    else:
        taken = z3.Not(equal)
    mask = z3.If(taken, z3.BitVecVal(-1, width),
                 z3.BitVecVal(0, width))
    ops.write(1, set_low_lane(destination, mask, width))


def build_float_flag_only(ops):
    width = 32 if ops.mnemonic.endswith("ss") else 64
    left = as_float(lane(ops.read_128(1), 0, width), width)
    right = as_float(ops.read(0, width), width)
    ops.state.flags = (ops.mnemonic, left, right)


def build_bitwise_128(ops):
    kind = BITWISE_128[ops.mnemonic]
    destination = ops.read_128(1)
    source = ops.read_128(0)
    if kind == "xor":
        result = destination ^ source
    elif kind == "or":
        result = destination | source
    else:
        result = destination & source
    ops.write(1, result)


def build_whole_move(ops):
    value = ops.read_128(0)
    ops.write(1, value)


def build_lane_move(ops):
    """`movss`/`movsd`/`movd`/`movq` between an xmm register and
    anywhere else: an xmm-to-xmm move merges the low lane, every other
    shape zero-extends."""
    mnemonic = ops.mnemonic
    if mnemonic == "movq":
        width = 64
    elif mnemonic == "movd":
        width = 32
    elif mnemonic == "movss":
        width = 32
    else:
        width = 64
    source, destination = ops.texts
    value = ops.read(0, width)
    if ops.is_vector(destination):
        if ops.is_vector(source):
            old = ops.read_128(1)
            ops.write(1, set_low_lane(old, value, width))
            return
        ops.write(1, z3.ZeroExt(128 - width, value))
        return
    ops.write(1, value)


def build_convert_to_float(ops):
    destination_width = CONVERT_TO_FLOAT[ops.mnemonic]
    source_text = ops.texts[0]
    if ops.is_register(source_text):
        source_width = ops.width_of(source_text)
    else:
        source_width = 32 if ops.mnemonic.endswith("l") else 64
    value = ops.read(0, source_width)
    converted = z3.fpSignedToFP(ROUNDING, value,
                                FLOAT_SORT[destination_width])
    old = ops.read_128(1)
    ops.write(1, set_low_lane(old, from_float(converted),
                              destination_width))


def build_convert_widen(ops):
    value = as_float(ops.read(0, 32), 32)
    converted = z3.fpToFP(ROUNDING, value, FLOAT_SORT[64])
    old = ops.read_128(1)
    ops.write(1, set_low_lane(old, from_float(converted), 64))


def build_unpack_low_double_words(ops):
    destination = ops.read_128(1)
    source = ops.read_128(0)
    ops.write(1, z3.Concat(lane(source, 1, 32), lane(destination, 1, 32),
                           lane(source, 0, 32),
                           lane(destination, 0, 32)))


def build_unpack_low_quad_words(ops):
    destination = ops.read_128(1)
    source = ops.read_128(0)
    ops.write(1, z3.Concat(lane(source, 0, 64),
                           lane(destination, 0, 64)))


def build_unpack_high_pairs(ops):
    destination = ops.read_128(1)
    source = ops.read_128(0)
    ops.write(1, z3.Concat(lane(source, 1, 64),
                           lane(destination, 1, 64)))


def build_unpack_low_pairs(ops):
    destination = ops.read_128(1)
    source = ops.read_128(0)
    ops.write(1, z3.Concat(lane(source, 0, 64),
                           lane(destination, 0, 64)))


def build_extract_word(ops):
    index_text, source_text, destination_text = ops.texts
    if not ops.is_immediate(index_text):
        raise NotModeled(
            "a word extraction whose index %r is not an immediate is "
            "not modeled" % index_text)
    index = int(IMMEDIATE_RE.match(index_text).group(1), 0)
    source = ops.read_128(1)
    ops.write(2, z3.ZeroExt(16, lane(source, index % 8, 16)))


# -- the x87 register stack -----------------------------------------

def x87_named_positions(ops):
    out = []
    for text in ops.texts:
        position = L48.x87_position_of(text)
        if position is not None:
            out.append(position)
    return out


def build_x87_load(ops):
    base = L48.x87_base(ops.mnemonic)
    if base == "fldz":
        ops.state.x87_push(z3.FPVal(0.0, X87_SORT))
        return
    if base == "fld1":
        ops.state.x87_push(z3.FPVal(1.0, X87_SORT))
        return
    named = x87_named_positions(ops)
    if named:
        ops.state.x87_push(ops.state.x87_at(named[0]))
        return
    memory = None
    for text in ops.texts:
        if ops.is_memory(text):
            memory = text
            break
    if memory is None:
        raise NotModeled(
            "the x87 load %r names no memory operand this file can "
            "read" % ops.mnemonic)
    ops.state.x87_push(x87_symbol(memory))


def build_x87_store(ops):
    base = L48.x87_base(ops.mnemonic)
    named = x87_named_positions(ops)
    value = ops.state.x87_at(0)
    for text in ops.texts:
        if ops.is_memory(text):
            ops.state.set_memory_cell(text, from_float(value))
            break
    if not named and not ops.texts:
        pass
    if base in L48.X87_STORES_POP:
        ops.state.x87_pop()


def build_x87_exchange(ops):
    named = x87_named_positions(ops)
    other = named[0] if named else 1
    top = ops.state.x87_at(0)
    swapped = ops.state.x87_at(other)
    ops.state.x87_set(0, swapped)
    ops.state.x87_set(other, top)


X87_ARITHMETIC_KIND = {
    "fadd": "add", "fsub": "sub", "fsubr": "rsub", "fmul": "mul",
    "fdiv": "div", "fdivr": "rdiv",
    "fiadd": "add", "fisub": "sub", "fisubr": "rsub",
    "fimul": "mul", "fidiv": "div", "fidivr": "rdiv",
    "faddp": "add", "fsubp": "sub", "fsubrp": "rsub",
    "fmulp": "mul", "fdivp": "div", "fdivrp": "rdiv",
}


def build_x87_arithmetic(ops):
    base = L48.x87_base(ops.mnemonic)
    kind = X87_ARITHMETIC_KIND[base]
    named = x87_named_positions(ops)
    memory = None
    for text in ops.texts:
        if ops.is_memory(text):
            memory = text
            break
    if memory is not None:
        left = ops.state.x87_at(0)
        right = x87_symbol(memory)
        destination = 0
    elif len(named) == 2:
        right = ops.state.x87_at(named[0])
        left = ops.state.x87_at(named[1])
        destination = named[1]
    elif base in L48.X87_ARITH_POP:
        right = ops.state.x87_at(0)
        left = ops.state.x87_at(1)
        destination = 1
    else:
        left = ops.state.x87_at(0)
        right = ops.state.x87_at(1)
        destination = 0
    if kind == "rsub":
        result = z3.fpSub(ROUNDING, right, left)
    elif kind == "rdiv":
        result = z3.fpDiv(ROUNDING, right, left)
    else:
        result = float_arithmetic(kind, left, right)
    ops.state.x87_set(destination, result)
    if base in L48.X87_ARITH_POP:
        ops.state.x87_pop()


def build_x87_one_place(ops):
    base = L48.x87_base(ops.mnemonic)
    value = ops.state.x87_at(0)
    if base == "fchs":
        ops.state.x87_set(0, -value)
        return
    if base == "fabs":
        ops.state.x87_set(0, z3.fpAbs(value))
        return
    if base == "fsqrt":
        ops.state.x87_set(0, z3.fpSqrt(ROUNDING, value))
        return
    raise NotModeled(
        "no z3 term is written for the x87 arch opcode %r"
        % ops.mnemonic)


def build_x87_compare(ops):
    """`fucomip %st(1),%st` is AT&T order: the source is the position
    named first, the destination is `%st`, the top.  The triple is
    (setter, destination, source)."""
    base = L48.x87_base(ops.mnemonic)
    named = x87_named_positions(ops)
    if len(named) >= 2:
        source = ops.state.x87_at(named[0])
        destination = ops.state.x87_at(named[1])
    elif len(named) == 1:
        source = ops.state.x87_at(named[0])
        destination = ops.state.x87_at(0)
    else:
        source = ops.state.x87_at(1)
        destination = ops.state.x87_at(0)
    ops.state.flags = (base, destination, source)
    if base in L48.X87_COMPARE_POP:
        ops.state.x87_pop()


def build_no_operation(ops):
    return


# ------------------------------------------------------------------
# section 4b: the merge, and the body's own control-flow graph
# ------------------------------------------------------------------
#
# THE SHAPE, from the reference CORE's settled rules of 2026-09-03
# (task 64):
#
#   * a body is walked as its own control-flow graph -- blocks cut at
#     the positional labels and after every transfer, visited in
#     reverse postorder, a join entered on the MERGE of its incoming
#     states; a body whose control flow has a CYCLE is refused by name.
#   * a transfer whose target is not a label DEFINED IN THIS BODY
#     leaves the unit; that side is unreachable, contributes nothing to
#     the merge, and its condition becomes a guard row.
#   * registers, memory cells, stack cells and x87 positions merge as
#     `If(path condition, this side, the rest)`.  The flag TRIPLE
#     merges only when both sides' setter carries one name; otherwise
#     the triple is ("merged", ...) and a later condition read refuses.
#   * a `call` with an attached callee is not a transfer: the walk
#     enters that body with the callee's own arrival contract and
#     returns through its answer register.

MERGED_SETTER = "merged"

MERGED_FLAG_REFUSAL = (
    "a condition is read after two sides of a branch left DIFFERENT "
    "flag-setting arch opcodes, so there is no one setter whose rule "
    "rebuilds it")


def same_term(left, right):
    """two z3 terms that are the same object or structurally equal.

    Used to keep a merge from wrapping `If` around a value neither side
    changed -- without it a body with five forks multiplies every
    untouched register by two on each one."""
    if left is right:
        return True
    try:
        return left.eq(right)
    except Exception:
        return False


def choose(condition, taken, otherwise):
    if same_term(taken, otherwise):
        return taken
    if taken.sort() != otherwise.sort():
        raise NotModeled(
            "the two sides of a branch leave a place holding values of "
            "different z3 sorts (%s against %s), so there is no one "
            "value the merge could name"
            % (taken.sort(), otherwise.sort()))
    return z3.If(condition, taken, otherwise)


def merge_two(condition, taken, otherwise):
    """(condition, the state on the taken side, the state on the other)
    -> one state.  `condition` is the TAKEN side's path condition."""
    if taken is None:
        return otherwise
    if otherwise is None:
        return taken
    if taken.rip_reads != otherwise.rip_reads:
        raise NotModeled(
            "the two sides of a branch made different numbers of "
            "rip-relative reads (%d against %d), so the k-th constant "
            "of this body has two different meanings"
            % (taken.rip_reads, otherwise.rip_reads))
    if taken.stack["offset"] != otherwise.stack["offset"]:
        raise NotModeled(
            "the two sides of a branch leave the machine stack at "
            "different depths (%d against %d)"
            % (taken.stack["offset"], otherwise.stack["offset"]))
    if taken.x87["depth"] != otherwise.x87["depth"] or \
            taken.x87["top"] != otherwise.x87["top"]:
        raise NotModeled(
            "the two sides of a branch leave the x87 register stack at "
            "different depths")
    out = taken.fork()
    out.registers = {}
    families = set(taken.registers) | set(otherwise.registers)
    for family in sorted(families):
        out.registers[family] = choose(
            condition, taken.family_value(family),
            otherwise.family_value(family))
    out.memory = {}
    cells = set(taken.memory) | set(otherwise.memory)
    for text in sorted(cells):
        out.memory[text] = choose(condition, taken.memory_cell(text),
                                  otherwise.memory_cell(text))
    out.stack = {
        "pointer": taken.stack["pointer"],
        "offset": taken.stack["offset"],
        "cells": {},
    }
    offsets = set(taken.stack["cells"]) | set(otherwise.stack["cells"])
    for offset in sorted(offsets):
        left = taken.stack["cells"].get(offset)
        right = otherwise.stack["cells"].get(offset)
        if left is None:
            out.stack["cells"][offset] = right
            continue
        if right is None:
            out.stack["cells"][offset] = left
            continue
        out.stack["cells"][offset] = choose(condition, left, right)
    out.x87 = {
        "slots": [],
        "top": taken.x87["top"],
        "depth": taken.x87["depth"],
    }
    for index in range(X87_POSITIONS):
        left = taken.x87["slots"][index]
        right = otherwise.x87["slots"][index]
        if left is None or right is None:
            out.x87["slots"].append(left if right is None else right)
            continue
        out.x87["slots"].append(choose(condition, left, right))
    out.flags = merge_flags(condition, taken.flags, otherwise.flags)
    out.guard_rows = merge_guard_rows(taken, otherwise)
    out.path_condition = z3.Or(taken.path_condition,
                               otherwise.path_condition)
    out.branch_condition = None
    return out


def merge_flags(condition, taken, otherwise):
    """THE FLAG TRIPLE IS NOT A VALUE and does not merge as one.

    `predicate_of` reads the SETTER'S NAME to choose between the
    integer route, the float route and the carry route, so two sides
    that left different setters have no one name to read.  When the
    names agree the two sides' L and R merge as ordinary terms; when
    they do not, the triple says so and a later condition read is
    refused rather than answered by the wrong rule.  Rule:
    machine_state CORE, 2026-09-03 (task 64)."""
    if taken is None:
        return otherwise
    if otherwise is None:
        return taken
    if taken[0] != otherwise[0]:
        return (MERGED_SETTER, None, None)
    if taken[0] == MERGED_SETTER:
        return taken
    try:
        left = choose(condition, taken[1], otherwise[1])
        right = choose(condition, taken[2], otherwise[2])
    except NotModeled:
        # ONE SETTER NAME, TWO WIDTHS.  `cmp %al,%cl` on one side and
        # `cmp %edx,%esi` on the other carry the same rule and
        # different sorts, so there is no one pair of sides to read the
        # condition off.  The triple says so and a later condition read
        # refuses, which is the same posture as two different setters.
        return (MERGED_SETTER, None, None)
    return (taken[0], left, right)


def unique_guard_rows(rows):
    out = []
    seen = []
    for row in rows:
        key = (row["line"], row["condition"])
        if key in seen:
            continue
        seen.append(key)
        out.append(row)
    return out


def merge_guard_rows(taken, otherwise):
    out = list(taken.guard_rows)
    seen = [row["condition"] for row in out]
    for row in otherwise.guard_rows:
        if row["condition"] in seen:
            continue
        out.append(row)
        seen.append(row["condition"])
    return out


class Block(object):
    """one straight-line run of the body: the instructions it holds,
    and where control goes when they are done."""

    def __init__(self, index, start):
        self.index = index
        self.start = start
        self.lines = []
        self.successors = []
        """(successor block index or None for OUT OF THE UNIT,
        'taken' / 'not taken' / 'always')."""
        self.terminator = None
        self.leaves_the_unit = False
        self.returns = False


TRANSFER_STEMS = ("jmp", "ud2")


def is_conditional_transfer(mnemonic):
    if not mnemonic.startswith("j"):
        return False
    if mnemonic == "jmp":
        return False
    suffix = mnemonic[1:]
    if suffix in CT.SUFFIX_TO_COND:
        return True
    return suffix in ("o", "no")


def transfer_target(line):
    parts = line.split(" ", 1)
    if len(parts) != 2:
        return None
    return parts[1].strip()


class Body(object):
    """a body's own control-flow graph, read off its own text.

    `lines` are the body's lines WITH their `!!` annotations, because
    the relocation on a `call` is the only place an unlinked transfer's
    callee name survives (log_161; `ledger.transfer_callee`)."""

    def __init__(self, lines):
        self.raw = lines
        self.instructions = []
        self.label_at = {}
        self.blocks = []
        self.read_lines()
        self.cut_blocks()
        self.wire()

    def read_lines(self):
        for raw in self.raw:
            text = raw.strip()
            if text == "":
                continue
            if text.endswith(":") and " " not in text:
                self.label_at[text[:-1]] = len(self.instructions)
                continue
            self.instructions.append(text)

    def cut_blocks(self):
        leaders = set()
        if self.instructions:
            leaders.add(0)
        for position in self.label_at.values():
            leaders.add(position)
        for index, raw in enumerate(self.instructions):
            mnemonic = raw.split("!!")[0].strip().split(" ", 1)[0]
            if mnemonic == "ret":
                leaders.add(index + 1)
                continue
            if mnemonic in TRANSFER_STEMS:
                leaders.add(index + 1)
                continue
            if is_conditional_transfer(mnemonic):
                leaders.add(index + 1)
        starts = sorted(position for position in leaders
                        if position < len(self.instructions))
        self.starts = starts
        for order, start in enumerate(starts):
            block = Block(order, start)
            if order + 1 < len(starts):
                stop = starts[order + 1]
            else:
                stop = len(self.instructions)
            block.lines = self.instructions[start:stop]
            self.blocks.append(block)

    def block_at(self, position):
        for block in self.blocks:
            if block.start == position:
                return block.index
        return None

    def wire(self):
        for block in self.blocks:
            if not block.lines:
                continue
            last = block.lines[-1]
            text = last.split("!!")[0].strip()
            mnemonic = text.split(" ", 1)[0]
            block.terminator = text
            if mnemonic == "ret":
                block.returns = True
                continue
            if mnemonic == "ud2":
                block.leaves_the_unit = True
                continue
            if mnemonic == "jmp":
                target = self.resolve(transfer_target(text))
                if target is None:
                    block.leaves_the_unit = True
                    continue
                block.successors.append((target, "always"))
                continue
            if is_conditional_transfer(mnemonic):
                target = self.resolve(transfer_target(text))
                block.successors.append((target, "taken"))
                block.successors.append((self.next_block(block),
                                         "not taken"))
                continue
            block.successors.append((self.next_block(block), "always"))

    def resolve(self, target):
        """a target that is a positional label DEFINED IN THIS BODY is
        an edge; anything else leaves the unit and is `None`."""
        if target is None:
            return None
        if target not in self.label_at:
            return None
        return self.block_at(self.label_at[target])

    def next_block(self, block):
        if block.index + 1 < len(self.blocks):
            return block.index + 1
        return None

    # -- order, and the cycle refusal ---------------------------------

    def reverse_postorder(self):
        order = []
        colour = {}
        self.walk_from(0, colour, order)
        order.reverse()
        return order

    def walk_from(self, index, colour, order):
        pending = [(index, iter(self.edge_targets(index)))]
        colour[index] = "open"
        while pending:
            here, edges = pending[-1]
            moved = False
            for target in edges:
                state = colour.get(target)
                if state == "open":
                    raise NotModeled(
                        "this body's control flow has a cycle (a "
                        "transfer back to a block already on the walk), "
                        "and no loop invariant is invented here")
                if state == "done":
                    continue
                colour[target] = "open"
                pending.append((target, iter(self.edge_targets(target))))
                moved = True
                break
            if moved:
                continue
            colour[here] = "done"
            order.append(here)
            pending.pop()

    def edge_targets(self, index):
        out = []
        for target, _side in self.blocks[index].successors:
            if target is None:
                continue
            out.append(target)
        return out

    def predecessors(self):
        out = {}
        for block in self.blocks:
            for target, side in block.successors:
                if target is None:
                    continue
                out.setdefault(target, []).append((block.index, side))
        return out


# ------------------------------------------------------------------
# section 5: opcode_table -- THE ONE TABLE (the sub-node)
# ------------------------------------------------------------------

class Entry(object):
    """one arch opcode's meaning: which places it reads, which places
    it writes, and the builder that turns its operands into a z3
    term."""

    def __init__(self, mnemonic, reads, writes, build, cause=None):
        self.mnemonic = mnemonic
        self.reads = tuple(reads)
        self.writes = tuple(writes)
        self.build = build
        self.cause = cause

    def __repr__(self):
        return "Entry(%r, reads=%r, writes=%r, modelled=%r)" % (
            self.mnemonic, self.reads, self.writes,
            self.build is not None)


TRANSFER_CAUSE = (
    "a transfer or trap, and this reference walks a body in text "
    "order")
RUNTIME_CALLEE_CAUSE = (
    "runtime callee not yet attached (Task 59, node 0_3_5_1_8): the "
    "callee's body is to be extracted from the toolchain's libgcc / "
    "compiler-rt archive and attached as an ArchUnit this caller "
    "references, with the producer {\"kind\": \"runtime_callee\"}")

NO_TERM_CAUSE = (
    "no z3 term is written for this arch opcode yet")

NAMED = "the operands the opcode names"
DESTINATION = "the last named operand"
FLAGS = "the flags"
ACCUMULATOR_PAIR = "the accumulator and the data register"
MACHINE_STACK = "the machine stack"
X87_STACK = "the x87 stack"
MEMORY = "memory"
THE_BRANCH_CONDITION = "the branch condition the walk forks on"


# The inventory this table is built over: EVERY arch mnemonic the
# corpus's own bodies spell, counted directly off
# canon38_wrapped_<lang>.json, canon38_interp.json and
# canon38_regen_store/*.json -- 162 distinct mnemonics over 181,125
# body lines (computed, not typed: see acceptance57.py part 0).  No entry is invented for an opcode no body contains.
CORPUS_MNEMONICS = (
    "adc add addsd addss and andpd andps call cltd cmovae cmovb cmovbe "
    "cmove cmovge cmovl cmovle cmovne cmovns cmovs cmp cmpeqsd cmpeqss "
    "cmpneqsd cmpneqss cqto cvtsi2sd cvtsi2ss cvtss2sd cwtd cwtl div "
    "divsd divss faddl faddp fadds fdivl fdivp fdivrl fdivrp fdivrs "
    "fdivs fiaddl fiadds fidivl fidivrl fidivrs fidivs fildl fildll "
    "filds fimull fimuls fisubl fisubrl fisubrs fisubs fldl flds fldt "
    "fldz fmull fmulp fmuls fstp fstpt fsubl fsubp fsubrl fsubrp fsubrs "
    "fsubs fucomi fucomip fxch idiv imul ja jae jb jbe je jg jge jl jle "
    "jmp jne jns jo js lea mov movabs movapd movaps movb movd movdqa "
    "movq movsbl movsbq movsd movslq movss movswl movzbl movzwl mul "
    "mulsd mulss neg nop nopl not or orpd orps pand pcmpeqb pcmpeqd "
    "pextrw pmovmskb pop punpckldq punpcklqdq push pxor ret sar sbb "
    "seta setae setb setbe sete setg setge setl setle setne setnp setns "
    "seto setp sets shl shld shr shrd sub subpd subsd subss test "
    "ucomisd ucomiss ud2 unpckhpd xor xorpd xorps"
).split()


# THE SECOND HALF OF THE INVENTORY, added 2026-09-03 by task 63.  The
# corpus grew: a routine of a toolchain's own builtins archive,
# attached to the body that transfers into it, is an arch unit like
# any other, so the opcodes ITS body spells are entries in THIS table.
# Computed off `canon39_callee_units.json` -- 76 attached bodies,
# 4,002 lines, 73 distinct mnemonics, of which these nine were the
# ones this table lacked (see `canon39_callee_opcodes.json`).  The
# opcode_table CORE's rule is unchanged: no entry is invented for an
# opcode no body contains.
ARCHIVE_MNEMONICS = (
    "endbr64 bsr inc bt cmova pinsrw cs fld xchg"
).split()

CORPUS_MNEMONICS = CORPUS_MNEMONICS + ARCHIVE_MNEMONICS


# THE THIRD HALF OF THE INVENTORY, added 2026-09-09 by task ap2.  The
# bodies this reference is asked to walk are no longer only the
# corpus's own: task h1's route COMPILES an emulation of a cell at the
# corpus's ship flags and hands the carved body back to this file, and
# a compiler emits, in that body, mnemonics no corpus body happens to
# spell.  Task ap1's loop met three of them over 1,012 runs and
# recorded each as a cause (log_243 section 6): `cmovg` 7 runs,
# `movswq` 2 runs, and the `lea` form with no base register 6 runs.
#
# These two mnemonics ARE ALREADY BUILT ABOVE and are then removed by
# `_prune`: `cmovg` by the `for suffix in CT.SUFFIX_TO_COND` loop with
# `build_move_condition`, `movswq` by the `for mnemonic in SIGN_EXTEND`
# loop with `build_extension` -- the same builder, the same table, the
# condition and the two widths read from the mnemonic, exactly as their
# siblings `cmovl` and `movslq` are.  So this list REGISTERS them; it
# invents no meaning.
#
# It is a SEPARATE list and is never folded into `CORPUS_MNEMONICS`,
# which is the corpus's own census (`acceptance57` reads its length as
# `arch_opcodes_the_corpus_spells`) and must keep saying what the
# corpus spells.  The opcode_table CORE's rule -- no entry is invented
# for an opcode no body contains -- is unchanged and is what this list
# satisfies: a body DOES contain them, and it is a compiled body of
# this line's own emulation route.
EMULATION_MNEMONICS = (
    "cmovg movswq"
).split()

KEPT_MNEMONICS = CORPUS_MNEMONICS + EMULATION_MNEMONICS


class OpcodeTable(object):
    """THE one table from mnemonic to meaning.  `Reference.simulate`
    reads it, and `term.transcribe` is meant to read the SAME object,
    which is what keeps the two gate routes from drifting apart on
    what an opcode means."""

    def __init__(self):
        self.entries = {}
        self._install()

    # -- construction -------------------------------------------------

    def add(self, mnemonic, reads, writes, build, cause=None):
        self.entries[mnemonic] = Entry(mnemonic, reads, writes, build,
                                       cause)

    def add_many(self, mnemonics, reads, writes, build, cause=None):
        for mnemonic in mnemonics:
            self.add(mnemonic, reads, writes, build, cause)

    def _install(self):
        self.add_many(NO_OPERATION, (), (), build_no_operation)
        self.add_many(TRANSFER, (), (), None, TRANSFER_CAUSE)
        self.add("call", (), (), None, RUNTIME_CALLEE_CAUSE)
        self.add_many(PLAIN_MOVE, (NAMED,), (DESTINATION,),
                      build_plain_move)
        self.add("lea", (NAMED,), (DESTINATION,), build_lea)
        for mnemonic in SIGN_EXTEND:
            self.add(mnemonic, (NAMED,), (DESTINATION,),
                     lambda ops: build_extension(ops, SIGN_EXTEND,
                                                 True))
        for mnemonic in ZERO_EXTEND:
            self.add(mnemonic, (NAMED,), (DESTINATION,),
                     lambda ops: build_extension(ops, ZERO_EXTEND,
                                                 False))
        self.add_many(ACCUMULATOR_WIDEN, (ACCUMULATOR_PAIR,),
                      (ACCUMULATOR_PAIR,), build_accumulator_widen)
        self.add_many(SPREAD_SIGN, (ACCUMULATOR_PAIR,),
                      (ACCUMULATOR_PAIR,), build_spread_sign)
        self.add_many(BINARY, (NAMED,), (DESTINATION, FLAGS),
                      build_binary)
        self.add_many(UNARY, (NAMED,), (DESTINATION, FLAGS),
                      build_unary)
        self.add_many(CARRY_BINARY, (NAMED, FLAGS),
                      (DESTINATION, FLAGS), build_carry_binary)
        self.add_many(SHIFT, (NAMED,), (DESTINATION,), build_shift)
        self.add_many(DOUBLE_SHIFT, (NAMED,), (DESTINATION,),
                      build_double_shift)
        self.add_many(FLAG_ONLY, (NAMED,), (FLAGS,), build_flag_only)
        self.add_many(DIVISION, (NAMED, ACCUMULATOR_PAIR),
                      (ACCUMULATOR_PAIR,), build_division)
        self.add("mul", (NAMED, ACCUMULATOR_PAIR),
                 (ACCUMULATOR_PAIR,), build_wide_multiply)
        # the nine the attached archive bodies added (task 63)
        self.add("inc", (NAMED,), (DESTINATION, FLAGS),
                 build_increment)
        self.add("xchg", (NAMED,), (NAMED,), build_exchange)
        self.add("bt", (NAMED,), (FLAGS,), build_bit_test)
        self.add("bsr", (NAMED,), (DESTINATION, FLAGS),
                 build_bit_scan_reverse)
        self.add("pinsrw", (NAMED,), (DESTINATION,), build_insert_word)
        self.add("push", (NAMED,), (MACHINE_STACK,), build_push)
        self.add("pop", (MACHINE_STACK,), (DESTINATION,), build_pop)
        for suffix in CT.SUFFIX_TO_COND:
            self.add("set" + suffix, (FLAGS,), (DESTINATION,),
                     build_set_condition)
            self.add("cmov" + suffix, (FLAGS, NAMED), (DESTINATION,),
                     build_move_condition)
            self.add("j" + suffix, (FLAGS,), (THE_BRANCH_CONDITION,),
                     build_branch_condition)
        self.add("seto", (FLAGS,), (DESTINATION,), build_set_condition)
        self.add("setno", (FLAGS,), (DESTINATION,),
                 build_set_condition)
        self.add("jo", (FLAGS,), (THE_BRANCH_CONDITION,),
                 build_branch_condition)
        self.add("jno", (FLAGS,), (THE_BRANCH_CONDITION,),
                 build_branch_condition)
        self.add_many(FLOAT_BINARY, (NAMED,), (DESTINATION,),
                      build_float_binary)
        self.add_many(PACKED_FLOAT, (NAMED,), (DESTINATION,),
                      build_packed_float)
        self.add_many(FLOAT_COMPARE_MASK, (NAMED,), (DESTINATION,),
                      build_float_compare_mask)
        self.add_many(FLOAT_FLAG_ONLY, (NAMED,), (FLAGS,),
                      build_float_flag_only)
        self.add_many(BITWISE_128, (NAMED,), (DESTINATION,),
                      build_bitwise_128)
        self.add_many(WHOLE_MOVE, (NAMED,), (DESTINATION,),
                      build_whole_move)
        self.add_many(("movss", "movsd", "movd"), (NAMED,),
                      (DESTINATION,), build_lane_move)
        self.add_many(CONVERT_TO_FLOAT, (NAMED,), (DESTINATION,),
                      build_convert_to_float)
        self.add("cvtss2sd", (NAMED,), (DESTINATION,),
                 build_convert_widen)
        self.add("punpckldq", (NAMED,), (DESTINATION,),
                 build_unpack_low_double_words)
        self.add("punpcklqdq", (NAMED,), (DESTINATION,),
                 build_unpack_low_quad_words)
        self.add("unpckhpd", (NAMED,), (DESTINATION,),
                 build_unpack_high_pairs)
        self.add("unpcklpd", (NAMED,), (DESTINATION,),
                 build_unpack_low_pairs)
        self.add("pextrw", (NAMED,), (DESTINATION,),
                 build_extract_word)
        self.add("pcmpeqb", (NAMED,), (DESTINATION,), None,
                 NO_TERM_CAUSE)
        self.add("pcmpeqd", (NAMED,), (DESTINATION,), None,
                 NO_TERM_CAUSE)
        self.add("pmovmskb", (NAMED,), (DESTINATION,), None,
                 NO_TERM_CAUSE)
        self._install_x87()
        self._prune()
        self._install_missing()

    def _prune(self):
        """no entry is kept for an opcode no body in the corpus
        spells -- the opcode_table CORE's own rule.  `KEPT_MNEMONICS`
        is that list plus the two mnemonics a COMPILED body of this
        line's own emulation route spells (task ap2, section above)."""
        allowed = set(KEPT_MNEMONICS)
        for mnemonic in list(self.entries):
            if mnemonic not in allowed:
                del self.entries[mnemonic]

    def _install_x87(self):
        for mnemonic in CORPUS_MNEMONICS:
            base = L48.x87_base(mnemonic)
            if base is None:
                continue
            if base in L48.X87_LOADS:
                self.add(mnemonic, (NAMED,), (X87_STACK,),
                         build_x87_load)
                continue
            if base in L48.X87_STORES_POP or base in \
                    L48.X87_STORES_KEEP:
                self.add(mnemonic, (X87_STACK,), (MEMORY, X87_STACK),
                         build_x87_store)
                continue
            if base in L48.X87_EXCHANGE:
                self.add(mnemonic, (X87_STACK,), (X87_STACK,),
                         build_x87_exchange)
                continue
            if base in L48.X87_ARITH_POP or base in \
                    L48.X87_ARITH_KEEP:
                self.add(mnemonic, (X87_STACK, NAMED), (X87_STACK,),
                         build_x87_arithmetic)
                continue
            if base in L48.X87_ONE_PLACE:
                self.add(mnemonic, (X87_STACK,), (X87_STACK,),
                         build_x87_one_place)
                continue
            if base in L48.X87_COMPARE_POP or base in \
                    L48.X87_COMPARE_KEEP:
                self.add(mnemonic, (X87_STACK,), (FLAGS, X87_STACK),
                         build_x87_compare)
                continue

    def _install_missing(self):
        """every corpus mnemonic with no family above becomes an entry
        with NO builder -- a census row, never a silent gap."""
        for mnemonic in CORPUS_MNEMONICS:
            if mnemonic in self.entries:
                continue
            self.add(mnemonic, (NAMED,), (), None)

    # -- reading ------------------------------------------------------

    def entry_for(self, mnemonic):
        return self.entries.get(mnemonic)

    def builder_for(self, producer):
        """producer -> the term builder, or nothing when the opcode
        has no model.  `producer` is a mnemonic, or the typed producer
        object the ledger carries."""
        mnemonic = producer
        if isinstance(producer, dict):
            mnemonic = producer.get("mnem")
        if isinstance(mnemonic, list):
            if not mnemonic:
                return None
            mnemonic = mnemonic[-1]
        if not isinstance(mnemonic, str):
            return None
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
# section 6: Reference -- the node's own class
# ------------------------------------------------------------------

ANNOTATION = "!!"


class Reference(object):
    """THE one symbolic simulator of the machine that every proof in
    this research is made against."""

    def __init__(self, runtime_units=None):
        self.opcode_table = OpcodeTable()
        self.runtime_units = runtime_units or {}
        """toolchain -> routine name -> the attached callee arch unit
        (`canon39_callee_units.json`), so a caller with no
        `runtime_callee_bodies` of its own still finds the bodies of
        its own toolchain."""

    # -- the CORE's methods -------------------------------------------

    def simulate(self, body_text, arrival_contract=None,
                 shared_seed=None, callees=None):
        """(body_text, arrival_contract) -> MachineState after the
        body.  `body_text` is the unit's own verbatim body: a list of
        lines, or one string with `; ` between them.

        The walk is `walk_body`: the body's OWN CONTROL-FLOW GRAPH,
        forked at each `j<cc>` and merged at each join.  Before task 64
        this method walked the lines in text order and refused at the
        first conditional transfer."""
        state = MachineState(shared_seed)
        self.apply_arrival_contract(state, arrival_contract)
        return self.walk_body(state, body_text, callees)

    # -- the walk over the graph ---------------------------------------

    def walk_body(self, state, body_text, callees=None, entered=None):
        """(MachineState, body lines, attached callees) -> the state
        after the whole graph.

        THE ONE ENTRY POINT every caller uses: `simulate`, the gate's
        wrapped route, and `term.runtime_row`'s step into an attached
        callee.  `callees` maps a routine name to its attached arch
        unit; `entered` is the cycle guard, the names already on the
        walk.
        """
        lines = self.annotated_lines(body_text)
        body = Body(lines)
        if not body.blocks:
            raise NotModeled(
                "this unit's body has no instruction line, so there "
                "is no ship code to walk")
        order = body.reverse_postorder()
        predecessors = body.predecessors()
        arriving = {0: [(state, state.path_condition)]}
        leaving = {}
        collected = list(state.guard_rows)
        for index in order:
            incoming = arriving.get(index)
            if not incoming:
                continue
            here = self.merge_incoming(incoming)
            try:
                after = self.walk_block(here, body.blocks[index],
                                        callees, entered)
            except LeavesTheUnit as departure:
                self.record_guard(here, departure.line,
                                  departure.target,
                                  here.path_condition)
                collected.extend(here.guard_rows)
                leaving[index] = None
                continue
            if after is None:
                leaving[index] = None
                continue
            leaving[index] = after
            self.hand_on(body, index, after, arriving)
            collected.extend(after.guard_rows)
        answers = []
        for block in body.blocks:
            if not block.returns:
                continue
            after = leaving.get(block.index)
            if after is None:
                continue
            answers.append(after)
        if not answers:
            raise NotModeled(
                "every path through this body leaves the unit or is "
                "unreachable, so the body leaves no answer to read")
        out = self.merge_incoming(
            [(one, one.path_condition) for one in answers])
        out.guard_rows = unique_guard_rows(collected)
        return out

    def merge_incoming(self, incoming):
        """fold the states arriving at one block, newest last:
        `If(path condition, this side, the rest)`.

        The path conditions out of one fork are disjoint and cover, so
        the fold is the state the machine is in whichever side ran."""
        merged = None
        for state, condition in reversed(incoming):
            if merged is None:
                merged = state
                continue
            merged = merge_two(condition, state, merged)
        return merged

    def hand_on(self, body, index, after, arriving):
        block = body.blocks[index]
        condition = after.branch_condition
        for target, side in block.successors:
            if target is None:
                if side == "taken" and condition is not None:
                    self.record_guard(after, block.terminator,
                                      transfer_target(block.terminator),
                                      condition)
                elif side == "not taken" and condition is not None:
                    self.record_guard(after, block.terminator,
                                      "the fall-through",
                                      z3.Not(condition))
                else:
                    self.record_guard(after, block.terminator,
                                      transfer_target(block.terminator))
                continue
            forked = after.fork()
            forked.branch_condition = None
            if side == "taken":
                if condition is None:
                    raise NotModeled(
                        "a conditional transfer left no condition on "
                        "the state: %r" % block.terminator)
                reaching = z3.And(after.path_condition, condition)
            elif side == "not taken":
                reaching = z3.And(after.path_condition,
                                  z3.Not(condition))
            else:
                reaching = after.path_condition
            forked.path_condition = reaching
            arriving.setdefault(target, []).append((forked, reaching))

    def record_guard(self, state, line, target, condition=None):
        row = {
            "line": line,
            "went_to": target,
            "condition": "always" if condition is None
                         else "%s" % condition,
        }
        state.guard_rows.append(row)

    def walk_block(self, state, block, callees, entered):
        """one straight-line run.  Returns the state after it, or
        raises `LeavesTheUnit` when a line in it transfers out."""
        for raw in block.lines:
            text = raw.split(ANNOTATION)[0].strip()
            annotation = ""
            if ANNOTATION in raw:
                annotation = ANNOTATION + raw.split(ANNOTATION, 1)[1]
            if text == "":
                continue
            mnemonic = text.split(" ", 1)[0]
            if mnemonic == "ret":
                continue
            if mnemonic == "jmp":
                continue
            if mnemonic == "ud2":
                raise LeavesTheUnit(text, "a trap")
            if mnemonic == "call":
                self.enter_callee(state, text, annotation, callees,
                                  entered)
                continue
            self.step(state, text)
        return state

    # -- the step into an attached callee ------------------------------

    TOOLCHAIN_OF = {"c": "clang", "cpp": "clang++", "rust": "rustc",
                    "swift": "swiftc"}

    def enter_callee(self, state, text, annotation, callees, entered):
        """A `call` WITH AN ATTACHED CALLEE IS NOT A TRANSFER.

        The walk enters the callee's own body -- itself a control-flow
        graph, walked by the same rule -- and returns through the
        callee's ANSWER REGISTER.  Nothing about a calling rule is
        assumed on the way in: the callee's arrival contract is the
        families ITS OWN TEXT reads before it writes them, and the
        caller's registers already hold those values, so the shared
        state IS the hand-over.  Rule: reference CORE, 2026-09-03
        (task 64).
        """
        operands = split_operands(text.split(" ", 1)[1]
                                  if " " in text else "")
        name = LEDGER.transfer_callee("call", operands, annotation)
        unit = None
        if name is not None and callees:
            unit = callees.get(name)
        if unit is None:
            raise LeavesTheUnit(
                text,
                name if name is not None else "a routine this body "
                "does not name")
        if entered is None:
            entered = ()
        if name in entered:
            raise NotModeled(
                "the attached runtime callee %r reaches itself, and no "
                "loop invariant is invented here" % name)
        body = unit.get("body_verbatim") or unit.get("body_as_read")
        if not body:
            raise NotModeled(
                "the attached body of the runtime callee %r is empty"
                % name)
        after = self.walk_body(state, body, callees,
                               tuple(entered) + (name,))
        home = self.answer_register_of(unit)
        state.registers = dict(after.registers)
        state.memory = dict(after.memory)
        state.stack = after.stack
        state.x87 = after.x87
        state.flags = after.flags
        state.rip_reads = after.rip_reads
        state.guard_rows = list(after.guard_rows)
        if home not in state.registers:
            raise NotModeled(
                "the attached runtime callee %r wrote neither %%xmm0 "
                "nor %%rax, so it left no answer where the machine's "
                "return rule reads one" % name)
        return state

    def callees_for(self, unit):
        """the attached callee bodies this caller may step into: the
        archive of the toolchain that compiled THIS caller, and no
        other.  The four archives do not agree -- clang's `__udivti3`
        is three instructions and rustc's is sixty-seven -- so handing
        a rust caller clang's body would be a different artifact
        (runtime_callee CORE)."""
        attached = unit.get("runtime_callee_bodies")
        if attached is not None:
            return attached
        name = unit.get("unit") or ""
        lang = name.split("/", 1)[0]
        toolchain = self.TOOLCHAIN_OF.get(lang)
        if toolchain is None:
            return {}
        return self.runtime_units.get(toolchain, {})

    def answer_register_of(self, unit):
        """`xmm0` when the callee's body writes `xmm0`, `rax`
        otherwise -- COMPUTED off the callee's own body rather than
        declared, because the callee record states no answer home and
        inventing one would be an unruled rule."""
        for raw in unit.get("body_verbatim") or []:
            text = raw.split(ANNOTATION)[0].strip()
            if "%xmm0" not in text:
                continue
            parts = split_operands(text.split(" ", 1)[1]
                                   if " " in text else "")
            if parts and parts[-1].strip() == "%xmm0":
                return "xmm0"
        return "rax"

    def annotated_lines(self, body_text):
        """the body's lines WITH their annotations kept, because the
        relocation on a `call` is the only place an unlinked transfer's
        callee name survives."""
        if body_text is None:
            raise NotModeled(
                "this unit record carries no body, so there is no "
                "ship code to walk")
        if isinstance(body_text, str):
            raw = body_text.split(";")
        else:
            raw = list(body_text)
        out = []
        for line in raw:
            line = line.strip()
            if line == "":
                continue
            out.append(line)
        return out

    def answer_of(self, state, answer_home):
        """MachineState + answer_home -> z3 term.  `answer_home` is
        (family, width), or the unit's own `result_family` /
        `result_width` pair as a mapping."""
        family, width = self.read_answer_home(answer_home)
        if family in XMM_NAMES:
            return cut(state.family_value(family), width)
        return z3.Extract(width - 1, 0, state.family_value(family))

    # -- the pieces the two methods stand on ---------------------------

    def read_answer_home(self, answer_home):
        if isinstance(answer_home, dict):
            family = answer_home.get("result_family")
            width = answer_home.get("result_width")
        else:
            family, width = answer_home
        if family is None or width is None:
            raise NotModeled(
                "this unit records no answer home, so there is no "
                "value to read")
        return family, width

    def body_lines(self, body_text):
        if body_text is None:
            raise NotModeled(
                "this unit record carries no body, so there is no "
                "ship code to walk")
        if isinstance(body_text, str):
            raw = body_text.split(";")
        else:
            raw = list(body_text)
        out = []
        for line in raw:
            line = line.split(ANNOTATION)[0].strip()
            if line == "":
                continue
            if line.endswith(":"):
                continue
            out.append(line)
        if not out:
            raise NotModeled(
                "this unit's body has no instruction line, so there "
                "is no ship code to walk")
        return out

    def apply_arrival_contract(self, state, arrival_contract):
        """bind the families the unit's own arrival contract names to
        the designated registers' symbols, so a language whose calling
        rule parks an argument elsewhere starts from one shared
        unconstrained state with the canonical form."""
        if not arrival_contract:
            return
        if isinstance(arrival_contract, dict):
            order = ["a", "b", "c", "d", "e", "f", "g", "h"]
            designated = ["rdi", "rsi", "rdx", "rcx", "r8", "r9",
                          "r10", "r11"]
            for index, name in enumerate(order):
                family = arrival_contract.get(name)
                if family is None:
                    continue
                if family == designated[index]:
                    continue
                state.bind(family, state.seed(designated[index]))
            return
        for binding in arrival_contract:
            spelling = binding.get("bound_to_the_same_symbol_as")
            if spelling is None:
                continue
            family = canon.FAMILY_OF.get(spelling[1:])
            if family is None:
                continue
            state.family_value(family)

    def step(self, state, line):
        mnemonic, rest = self.split_line(line)
        entry = self.opcode_table.entry_for(mnemonic)
        if entry is None:
            raise NotModeled(
                "arch opcode %r has no entry in the opcode table -- "
                "no body in the corpus this table was built over "
                "spells it" % mnemonic)
        if entry.build is None:
            if entry.cause is None:
                raise NotModeled(
                    "arch opcode %r has an entry in the opcode table "
                    "and no builder: it is a census row, not a "
                    "silent gap" % mnemonic)
            raise NotModeled(
                "arch opcode %r is a census row, not a silent gap: %s"
                % (mnemonic, entry.cause))
        operands = Operands(state, mnemonic, split_operands(rest))
        entry.build(operands)

    def split_line(self, line):
        parts = line.split(" ", 1)
        mnemonic = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        return mnemonic, rest

    # -- what the reference cannot do, said in one place ---------------

    def answer_for_unit(self, unit):
        """(term, width) for one canon38 unit record, or a refusal.
        The shape `gate48.reference_answer` asks for, with THIS
        object behind it."""
        state = self.simulate(unit.get("body_verbatim"),
                              unit.get("arrival_contract_bindings"),
                              callees=self.callees_for(unit))
        width = unit.get("result_width")
        term = self.answer_of(state, (unit.get("result_family"),
                                      width))
        return term, width


REFERENCE = Reference()
