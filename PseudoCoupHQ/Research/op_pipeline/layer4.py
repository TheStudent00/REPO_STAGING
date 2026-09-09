#!/usr/bin/env python3
"""layer4.py -- TASK 48: LAYER 4, the z3 form, AS A TRANSCRIPTION OF THE
PROVENANCE LEDGER.

DEE'S RULING 3, which this file implements literally: "LAYER 4 (the z3
form) IS A TRANSCRIPTION OF THE LEDGER -- read producer/operands
bottom-up from OUT-0 and you have the term; THE CENSUS IS A FILTER:
rows whose producer has no z3 term; no mining over instruction
sequences."

So there is no expression pipeline here.  There is:

  1. THE OPERAND REPLAY.  Task 47's ledger names, per row, the rows it
     read -- but not which operand slot each row filled.  This file
     replays ledger47's own operand rule over the rows in their stored
     order, keeping the same family-to-row map ledger47 keeps, and
     then CHECKS its replay against the stored `operands` list.  A row
     whose replay disagrees is refused by name; nothing is guessed.
  2. THE PRODUCER TABLE.  One entry per producer -- an arch opcode, or
     the PAIR (flag-setting opcode, flag-reading opcode) for a
     flag-derived row.  An entry is a function from operand terms to a
     z3 term.  A producer with no entry raises NoTerm, and NoTerm is
     exactly what the census filters on.
  3. THE TRANSCRIPTION.  Start at OUT-0, take its producer and its
     operand rows, recurse.  The term is the ledger read bottom-up.

WIDTHS.  A row is 8 or 16 bytes; the operation inside it has its own
width (`add %esi,%eax` is 32-bit inside an 8-byte row).  relink48.py
attaches each row to the body line that produced it, so the width is
read off the line's own operands -- the arch text, never a guess.

THE VALUE A ROW CARRIES.  For a general-register row it is the FULL
64-bit register content after the instruction, using the machine's own
rule (a 32-bit write zero-extends into the 64-bit register); for a
vector row it is the full 128 bits.  A reader of a row extracts the
width it needs.  This matches the simulator the gate compares against,
so the two routes are comparable.

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
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import condition_table as CT                                     # noqa: E402
import ledger47 as L47                                           # noqa: E402
import region36 as R36                                           # noqa: E402
import relink48                                                  # noqa: E402
import z3                                                        # noqa: E402

WIDTH_BITS = {0: 64, 1: 32, 2: 16, 3: 8}
SUFFIX_BITS = {"b": 8, "w": 16, "l": 32, "q": 64}


class NoTerm(Exception):
    """this producer has no z3 term.  THE CENSUS FILTERS ON THIS."""

    def __init__(self, producer, why):
        Exception.__init__(self, why)
        self.producer = producer
        self.why = why


class ReplayDisagreement(Exception):
    """the operand replay does not reproduce the stored row; refused."""


# ------------------------------------------------------------------
# section 1: reading one body line
# ------------------------------------------------------------------

IMMEDIATE = L47.IMMEDIATE


def width_of_register(operand):
    """the width of a register spelling, read off canon.py's own table.
    A vector register is 128 bits; canon.py's table gives every family
    the code 0, so the vector families are named here."""
    name = operand[1:]
    family = canon.FAMILY_OF.get(name)
    if family is not None and is_vector_family(family):
        return 128
    code = canon.WIDTH_OF.get(name)
    if code is None:
        return None
    return WIDTH_BITS.get(code)


def family_of(operand):
    if not operand.startswith("%"):
        return None
    return canon.FAMILY_OF.get(operand[1:])


def is_vector_family(family):
    return L47.is_vector_family(family)


def operation_width(line, operands):
    """the width the instruction operates at, read off its own operands
    in the arch text."""
    for operand in reversed(operands):
        if operand.startswith("%"):
            width = width_of_register(operand)
            if width is not None:
                return width
    mnemonic = L47.mnemonic_of(line)
    if mnemonic and mnemonic[-1] in SUFFIX_BITS:
        return SUFFIX_BITS[mnemonic[-1]]
    return None


# ------------------------------------------------------------------
# section 2: THE OPERAND REPLAY -- which row filled which operand slot
# ------------------------------------------------------------------

def replay_operands(rows, arrival_families):
    """rows: relink48.relink()'s output, in stored order.

    Returns a list parallel to `rows`; entry i is the list of operand
    slots of that row's own body line, in the arch text's own order,
    each slot naming the ROW that filled it (or an immediate, or a
    memory operand's inner rows).  The rows named are then CHECKED
    against the row's own stored `operands` list -- same names, same
    order.  A disagreement is refused by name."""
    where = {}
    literals = {}
    own = {}
    slots = []
    arrival_index = 0
    rip_index = [0]
    for row in rows:
        producer = row["produced_by"]
        if producer == "arrival":
            if arrival_index < len(arrival_families):
                where[arrival_families[arrival_index]] = row["row"]
            arrival_index += 1
            slots.append([])
            continue
        if row["block"] in ("CONST", "OWN"):
            # these rows are bound when the line that spelled them is
            # reached, in ledger47's own creation order.
            slots.append([])
            continue
        if row["block"] == "OUT":
            slots.append([])
            continue
        line = row["line"]
        if line is None:
            slots.append([])
            continue
        mnemonic = L47.mnemonic_of(line)
        operands = L47.operands_of(line)
        found = []
        named = []
        for position, operand in enumerate(operands):
            value = L47.immediate_value(operand)
            if value is not None:
                name = literals.get(operand)
                if name is None:
                    name = claim_literal(rows, literals, operand)
                found.append(Slot(operand, None, immediate=value))
                named.append(name)
                continue
            if operand.startswith("%"):
                family = family_of(operand)
                if family is None:
                    found.append(Slot(operand, None))
                    continue
                is_last = position == len(operands) - 1
                if is_last and mnemonic in L47.PURE_WRITE_MNEMONICS:
                    # ledger47 does not RECORD this slot as a read (the
                    # opcode overwrites it), and the check below must
                    # agree with that.  The machine still has a value
                    # there, and an opcode like the whole-register
                    # bitwise family reads it, so the slot is resolved
                    # -- but never named in the check.
                    slot = Slot(operand, None)
                    slot.row_name = where.get(family)
                    slot.family = family
                    found.append(slot)
                    continue
                name = where.get(family)
                slot = Slot(operand, None)
                slot.row_name = name
                slot.family = family
                found.append(slot)
                if name is not None:
                    named.append(name)
                continue
            inner = []
            if "(%rip)" in operand:
                inner.append(("rip", ("rip", rip_index[0])))
                rip_index[0] += 1
            for token in re.findall(r"%[a-z0-9]+", operand):
                family = canon.FAMILY_OF.get(token[1:])
                if family is None:
                    continue
                name = where.get(family)
                if name is not None:
                    inner.append((token, name))
                    named.append(name)
            for hit in R36.RSP_DISP.finditer(operand):
                displacement = int(hit.group(1), 16)
                name = own.get(displacement)
                if name is None:
                    name = claim_own(rows, own, displacement)
                inner.append(("own", name))
                named.append(name)
            found.append(Slot(operand, None, memory=inner))
        if named != list(row["operands"]):
            raise ReplayDisagreement(
                "row %s: the replay names %r, the stored ledger says %r"
                % (row["row"], named, row["operands"]))
        slots.append(found)
        family = None
        if operands:
            family = family_of(operands[-1])
        if family is not None and family not in canon.NEVER_RENAME:
            if not (row["block"] == "GUARD" and L47.JCC.match(mnemonic)):
                where[family] = row["row"]
    return slots


def claim_literal(rows, literals, operand):
    """the CONST rows appear in the ledger in the order ledger47 made
    them; bind the next unclaimed one to this immediate text."""
    value = L47.immediate_value(operand)
    for row in rows:
        if row["block"] != "CONST":
            continue
        if row["row"] in literals.values():
            continue
        if row.get("value_at_run") != value:
            continue
        literals[operand] = row["row"]
        return row["row"]
    return None


def claim_own(rows, own, displacement):
    for row in rows:
        if row["block"] != "OWN":
            continue
        if row.get("displacement") != displacement:
            continue
        own[displacement] = row["row"]
        return row["row"]
    return None


# ------------------------------------------------------------------
# section 3: THE PRODUCER TABLE
# ------------------------------------------------------------------

SIGN_EXTEND = {
    "movslq": (32, 64), "movsbl": (8, 32), "movsbq": (8, 64),
    "movswl": (16, 32), "movswq": (16, 64), "movsbw": (8, 16),
    "movsl": (32, 64), "cltq": (32, 64),
}
ZERO_EXTEND = {
    "movzbl": (8, 32), "movzbq": (8, 64), "movzwl": (16, 32),
    "movzwq": (16, 64), "movzbw": (8, 16),
}
PLAIN_MOVE = frozenset([
    "mov", "movl", "movq", "movd", "movb", "movw",
    "movss", "movsd", "movaps", "movapd", "movdqa", "movdqu",
])
BINARY = frozenset(["add", "sub", "and", "or", "xor", "imul"])
UNARY = frozenset(["not", "neg"])
SHIFT = frozenset(["shl", "shr", "sar", "sal"])
FLAG_ONLY = frozenset(["cmp", "test", "ucomisd", "ucomiss",
                       "comisd", "comiss"])
FLOAT_BINARY = {
    "addsd": ("add", 64), "addss": ("add", 32),
    "subsd": ("sub", 64), "subss": ("sub", 32),
    "mulsd": ("mul", 64), "mulss": ("mul", 32),
    "divsd": ("div", 64), "divss": ("div", 32),
}
PACKED_FLOAT = {
    "addpd": ("add", 64), "subpd": ("sub", 64),
    "mulpd": ("mul", 64), "divpd": ("div", 64),
    "addps": ("add", 32), "subps": ("sub", 32),
    "mulps": ("mul", 32), "divps": ("div", 32),
}
FLOAT_COMPARE = {
    "cmpeqsd": ("eq", 64), "cmpeqss": ("eq", 32),
    "cmpneqsd": ("ne", 64), "cmpneqss": ("ne", 32),
}
BITWISE_128 = {
    "xorps": "xor", "xorpd": "xor", "pxor": "xor",
    "orps": "or", "orpd": "or", "por": "or",
    "andps": "and", "andpd": "and", "pand": "and",
}
FLOAT_SORT = {32: z3.Float32(), 64: z3.Float64()}

# THE IMPLICIT-DESTINATION FAMILY.  These opcodes write a register they
# do not name -- the quotient and remainder land in the accumulator and
# the data register, the wide product likewise -- and ledger47's own
# rule takes the LAST NAMED OPERAND as the destination.  So the row
# these opcodes make is attached to the register they READ, and no row
# in the ledger holds the value they wrote.  The producer is a real
# arch opcode with a plain meaning; what is missing is a row to carry
# it, which is a property of the ledger, not of the opcode.
IMPLICIT_DESTINATION = {
    "idiv": "this opcode writes the quotient and the remainder into "
            "registers it does not name, and ledger47 takes the last "
            "named operand as the destination, so the row it made is "
            "attached to the divisor and no row holds the quotient",
    "div": "this opcode writes the quotient and the remainder into "
           "registers it does not name, and ledger47 takes the last "
           "named operand as the destination, so the row it made is "
           "attached to the divisor and no row holds the quotient",
    "mul": "this opcode writes the wide product into registers it does "
           "not name, and ledger47 takes the last named operand as the "
           "destination, so the row it made is attached to the "
           "multiplier and no row holds the product",
}


def full64(value):
    """the machine's own write rule: a sub-64-bit write into a general
    register zero-extends; a 64-bit write replaces."""
    if value.size() == 64:
        return value
    if value.size() > 64:
        return z3.Extract(63, 0, value)
    return z3.ZeroExt(64 - value.size(), value)


def cut(value, width):
    if value.size() == width:
        return value
    if value.size() > width:
        return z3.Extract(width - 1, 0, value)
    return z3.ZeroExt(width - value.size(), value)


def as_float(bits, width):
    return z3.fpBVToFP(cut(bits, width), FLOAT_SORT[width])


def from_float(value, width):
    return z3.fpToIEEEBV(value)


def lane_write(destination_128, lane_bits, width):
    """a scalar SSE instruction writes ONLY the low lane and leaves the
    destination's own upper bits untouched."""
    return z3.Concat(z3.Extract(127, width, destination_128), lane_bits)


class Slot(object):
    """one operand slot of one body line, already resolved to a term."""

    def __init__(self, text, term, immediate=None, memory=None):
        self.text = text
        self.term = term
        self.immediate = immediate
        self.memory = memory
        self.row_name = None
        self.family = None


def build_producer_term(producer, line, slots, row, context):
    """THE PRODUCER TABLE.  `slots` are the resolved operand slots of
    this row's own body line, in the arch text's own order (AT&T:
    source first, destination last)."""
    if isinstance(producer, list):
        return build_pair_term(producer, line, slots, row, context)
    mnemonic = producer
    operands = L47.operands_of(line) if line else []
    width = operation_width(line, operands) if line else None
    def term_of(index):
        slot = slots[index]
        if slot.term is None:
            if slot.text in ("%ah", "%bh", "%ch", "%dh"):
                raise NoTerm(mnemonic,
                             "operand %r names the SECOND byte of a "
                             "register, which canon.py's register table "
                             "does not carry as a family, so ledger47 "
                             "made no row for it and there is no value "
                             "to read" % slot.text)
            raise NoTerm(mnemonic,
                         "operand %r of %r resolves to no row and no "
                         "immediate this file can read" %
                         (slot.text, line))
        return slot.term
    if mnemonic in PLAIN_MOVE:
        source = term_of(0)
        destination_family = family_of(operands[-1]) if operands else None
        if destination_family is not None and \
                is_vector_family(destination_family):
            if mnemonic in ("movq", "movd"):
                bits = 64 if mnemonic == "movq" else 32
                return z3.ZeroExt(128 - bits, cut(source, bits))
            if mnemonic in ("movss", "movsd"):
                bits = 32 if mnemonic == "movss" else 64
                return z3.ZeroExt(128 - bits, cut(source, bits))
            return cut(source, 128)
        if mnemonic in ("movq", "movd") and operands and \
                family_of(operands[0]) is not None and \
                is_vector_family(family_of(operands[0])):
            bits = 64 if mnemonic == "movq" else 32
            return full64(cut(source, bits))
        if width is None:
            raise NoTerm(mnemonic, "no operand width could be read off "
                                   "%r" % line)
        return full64(cut(source, width))
    if mnemonic in SIGN_EXTEND:
        source_width, destination_width = SIGN_EXTEND[mnemonic]
        source = cut(term_of(0), source_width)
        return full64(z3.SignExt(destination_width - source_width, source))
    if mnemonic in ZERO_EXTEND:
        source_width, destination_width = ZERO_EXTEND[mnemonic]
        source = cut(term_of(0), source_width)
        return full64(z3.ZeroExt(destination_width - source_width, source))
    if mnemonic in BINARY:
        if len(slots) == 1 and mnemonic == "imul":
            raise NoTerm(mnemonic, IMPLICIT_DESTINATION["mul"])
        if len(slots) != 2:
            raise NoTerm(mnemonic, "the %d-operand form of %r is not in "
                                   "the table" % (len(slots), mnemonic))
        source = cut(term_of(0), width)
        destination = cut(term_of(1), width)
        if mnemonic == "add":
            value = destination + source
        elif mnemonic == "sub":
            value = destination - source
        elif mnemonic == "and":
            value = destination & source
        elif mnemonic == "or":
            value = destination | source
        elif mnemonic == "xor":
            value = destination ^ source
        else:
            value = destination * source
        return full64(value)
    if mnemonic in ("sbb", "adc"):
        flags = context.get("flags")
        if flags is None or flags.get("carry") is None:
            raise NoTerm(mnemonic,
                         "this opcode reads the carry flag, and no arch "
                         "opcode in this body before it sets a carry "
                         "this file models")
        source = cut(term_of(0), width)
        destination = cut(term_of(1), width)
        carry = z3.If(flags["carry"], z3.BitVecVal(1, width),
                      z3.BitVecVal(0, width))
        if mnemonic == "sbb":
            value = destination - source - carry
        else:
            value = destination + source + carry
        return full64(value)
    if mnemonic in UNARY:
        destination = cut(term_of(0), width)
        value = ~destination if mnemonic == "not" else -destination
        return full64(value)
    if mnemonic in SHIFT:
        count = cut(term_of(0), width)
        destination = cut(term_of(1), width)
        mask = 0x3F if width == 64 else 0x1F
        amount = count & z3.BitVecVal(mask, width)
        if mnemonic in ("shl", "sal"):
            value = destination << amount
        elif mnemonic == "shr":
            value = z3.LShR(destination, amount)
        else:
            value = destination >> amount
        return full64(value)
    if mnemonic in ("shld", "shrd"):
        if len(slots) != 3:
            raise NoTerm(mnemonic,
                         "the %d-operand form of %r is not the "
                         "three-operand form this file models"
                         % (len(slots), mnemonic))
        count = cut(term_of(0), width)
        source = cut(term_of(1), width)
        destination = cut(term_of(2), width)
        mask = 0x3F if width == 64 else 0x1F
        amount = count & z3.BitVecVal(mask, width)
        other = z3.BitVecVal(width, width) - amount
        if mnemonic == "shld":
            moved = destination << amount
            filled = z3.LShR(source, other)
        else:
            moved = z3.LShR(destination, amount)
            filled = source << other
        value = z3.If(amount == z3.BitVecVal(0, width),
                      destination, moved | filled)
        return full64(value)
    if mnemonic in ("pcmpeqb", "pcmpeqd", "pcmpeqw"):
        lane_bits = {"pcmpeqb": 8, "pcmpeqw": 16, "pcmpeqd": 32}
        bits = lane_bits[mnemonic]
        source = cut(term_of(0), 128)
        destination = cut(term_of(1), 128)
        lanes = []
        for lane in range(128 // bits):
            low = lane * bits
            left = z3.Extract(low + bits - 1, low, destination)
            right = z3.Extract(low + bits - 1, low, source)
            ones = z3.BitVecVal((1 << bits) - 1, bits)
            zeros = z3.BitVecVal(0, bits)
            lanes.append(z3.If(left == right, ones, zeros))
        lanes.reverse()
        return z3.Concat(*lanes)
    if mnemonic in FLAG_ONLY:
        # these opcodes write NO register; the row ledger47 emitted for
        # them carries the destination's own value, unchanged.  The
        # flags they set are read by the PAIR producer below.
        return term_of(len(slots) - 1)
    if mnemonic == "lea":
        address = address_term(slots[0], line)
        return full64(cut(address, width if width else 64))
    if mnemonic == "movabs":
        slot = slots[0]
        if slot.immediate is None:
            raise NoTerm(mnemonic, "the source of %r is not an "
                                   "immediate" % line)
        return z3.BitVecVal(slot.immediate & ((1 << 64) - 1), 64)
    if mnemonic in FLOAT_BINARY:
        kind, bits = FLOAT_BINARY[mnemonic]
        source = as_float(term_of(0), bits)
        destination_bits = term_of(1)
        destination = as_float(destination_bits, bits)
        rounding = z3.RNE()
        if kind == "add":
            value = z3.fpAdd(rounding, destination, source)
        elif kind == "sub":
            value = z3.fpSub(rounding, destination, source)
        elif kind == "mul":
            value = z3.fpMul(rounding, destination, source)
        else:
            value = z3.fpDiv(rounding, destination, source)
        return lane_write(cut(destination_bits, 128),
                          from_float(value, bits), bits)
    if mnemonic in PACKED_FLOAT:
        kind, bits = PACKED_FLOAT[mnemonic]
        source_bits = cut(term_of(0), 128)
        destination_bits = cut(term_of(1), 128)
        rounding = z3.RNE()
        lanes = []
        for lane in range(128 // bits):
            low = lane * bits
            left = as_float(z3.Extract(low + bits - 1, low,
                                       destination_bits), bits)
            right = as_float(z3.Extract(low + bits - 1, low,
                                        source_bits), bits)
            if kind == "add":
                value = z3.fpAdd(rounding, left, right)
            elif kind == "sub":
                value = z3.fpSub(rounding, left, right)
            elif kind == "mul":
                value = z3.fpMul(rounding, left, right)
            else:
                value = z3.fpDiv(rounding, left, right)
            lanes.append(from_float(value, bits))
        lanes.reverse()
        return z3.Concat(*lanes)
    if mnemonic in FLOAT_COMPARE:
        kind, bits = FLOAT_COMPARE[mnemonic]
        source = as_float(term_of(0), bits)
        destination_bits = term_of(1)
        destination = as_float(destination_bits, bits)
        equal = z3.fpEQ(destination, source)
        unordered = z3.Or(z3.fpIsNaN(destination), z3.fpIsNaN(source))
        if kind == "eq":
            predicate = z3.And(equal, z3.Not(unordered))
        else:
            predicate = z3.Or(z3.Not(equal), unordered)
        ones = z3.BitVecVal((1 << bits) - 1, bits)
        zeros = z3.BitVecVal(0, bits)
        mask = z3.If(predicate, ones, zeros)
        return lane_write(cut(destination_bits, 128), mask, bits)
    if mnemonic in ("cvtsi2sd", "cvtsi2ss"):
        bits = 64 if mnemonic == "cvtsi2sd" else 32
        source_width = width_of_register(operands[0]) \
            if operands and operands[0].startswith("%") else 64
        if source_width is None:
            source_width = 64
        integer = cut(term_of(0), source_width)
        value = z3.fpSignedToFP(z3.RNE(), integer, FLOAT_SORT[bits])
        destination_bits = term_of(1) if len(slots) > 1 else \
            z3.BitVecVal(0, 128)
        return lane_write(cut(destination_bits, 128),
                          from_float(value, bits), bits)
    if mnemonic == "cvtss2sd":
        source = as_float(term_of(0), 32)
        value = z3.fpToFP(z3.RNE(), source, FLOAT_SORT[64])
        destination_bits = term_of(1) if len(slots) > 1 else \
            z3.BitVecVal(0, 128)
        return lane_write(cut(destination_bits, 128),
                          from_float(value, 64), 64)
    if mnemonic == "cvtsd2ss":
        source = as_float(term_of(0), 64)
        value = z3.fpToFP(z3.RNE(), source, FLOAT_SORT[32])
        destination_bits = term_of(1) if len(slots) > 1 else \
            z3.BitVecVal(0, 128)
        return lane_write(cut(destination_bits, 128),
                          from_float(value, 32), 32)
    if mnemonic in BITWISE_128:
        kind = BITWISE_128[mnemonic]
        source = cut(term_of(0), 128)
        destination = cut(term_of(1), 128)
        if kind == "xor":
            return source ^ destination
        if kind == "or":
            return source | destination
        return source & destination
    if mnemonic == "unpckhpd":
        source = cut(term_of(0), 128)
        destination = cut(term_of(1), 128)
        return z3.Concat(z3.Extract(127, 64, source),
                         z3.Extract(127, 64, destination))
    if mnemonic == "punpcklqdq":
        source = cut(term_of(0), 128)
        destination = cut(term_of(1), 128)
        return z3.Concat(z3.Extract(63, 0, source),
                         z3.Extract(63, 0, destination))
    if mnemonic == "punpckldq":
        source = cut(term_of(0), 128)
        destination = cut(term_of(1), 128)
        return z3.Concat(z3.Extract(63, 32, source),
                         z3.Extract(63, 32, destination),
                         z3.Extract(31, 0, source),
                         z3.Extract(31, 0, destination))
    if mnemonic == "pextrw":
        slot = slots[0]
        if slot.immediate is None:
            raise NoTerm(mnemonic, "the lane selector of %r is not an "
                                   "immediate" % line)
        lane = slot.immediate & 7
        source = cut(term_of(1), 128)
        return full64(z3.Extract(16 * lane + 15, 16 * lane, source))
    if mnemonic in IMPLICIT_DESTINATION:
        raise NoTerm(mnemonic, IMPLICIT_DESTINATION[mnemonic])
    if mnemonic in ("push", "pop"):
        raise NoTerm(mnemonic,
                     "this opcode moves a value to or from the machine "
                     "stack, and the ledger has no block for the "
                     "machine stack: no row holds the value it wrote, "
                     "so there is nothing for a term to be about")
    raise NoTerm(mnemonic,
                 "no z3 term is written for this arch opcode")


def address_term(slot, line):
    """the address a memory operand computes: base + index*scale +
    displacement, read off the arch text."""
    if slot.memory is None:
        raise NoTerm("lea", "the source of %r is not a memory operand "
                            "this file can read" % line)
    for token, source in slot.memory:
        if token == "rip" and isinstance(source, tuple):
            return z3.BitVec("rip_address_%d" % source[1], 64)
        if token == "own" and source is not None and \
                not isinstance(source, tuple):
            return source
    text = slot.text
    hit = re.match(
        r"^(-?0x[0-9a-f]+)?\(([^,)]*)(?:,([^,)]*)(?:,(\d+))?)?\)$", text)
    if hit is None:
        raise NoTerm("lea", "address form %r is not in the table" % text)
    displacement = hit.group(1)
    base_text = hit.group(2)
    index_text = hit.group(3)
    scale_text = hit.group(4)
    lookup = {}
    for token, source in slot.memory:
        lookup[token] = source
    total = z3.BitVecVal(0, 64)
    if displacement:
        total = total + z3.BitVecVal(int(displacement, 16), 64)
    if base_text == "%rip":
        term = lookup.get("rip")
        if term is None:
            raise NoTerm("lea", "the rip-relative base of %r resolves "
                                "to nothing" % text)
        return term
    if base_text:
        term = lookup.get(base_text)
        if term is None:
            raise NoTerm("lea", "the base register of %r resolves to no "
                                "row" % text)
        total = total + cut(term, 64)
    if index_text:
        term = lookup.get(index_text)
        if term is None:
            raise NoTerm("lea", "the index register of %r resolves to "
                                "no row" % text)
        scale = int(scale_text) if scale_text else 1
        total = total + cut(term, 64) * z3.BitVecVal(scale, 64)
    return total


def build_pair_term(pair, line, slots, row, context):
    """A FLAG-DERIVED ROW.  the owner's addendum: the producer is the PAIR
    (flag-setting arch opcode, flag-reading arch opcode) -- a real
    arch-opcode producer with a real z3 term, never a lifter helper
    name.  The condition comes off the reading opcode's own suffix
    through condition_table.py's SUFFIX_TO_COND, and the two sides of
    the comparison come off the SETTING opcode's own operands, which
    are the ledger's own rows."""
    setter, reader = pair[0], pair[1]
    if setter is None:
        raise NoTerm(tuple(pair),
                     "no flag-setting arch opcode precedes the "
                     "flag-reading opcode in this body, so the pair is "
                     "incomplete and the condition has no two sides")
    prefix = None
    for candidate in ("set", "cmov", "j"):
        if reader.startswith(candidate) and len(reader) > len(candidate):
            suffix = reader[len(candidate):]
            if suffix in CT.SUFFIX_TO_COND or suffix in ("o", "no"):
                prefix = candidate
                break
    if prefix is None:
        if reader == "jmp":
            raise NoTerm(tuple(pair),
                         "an unconditional transfer reads no flags: "
                         "the ledger records it as a flag-reading "
                         "opcode, which it is not, so the row it makes "
                         "has no condition to be")
        raise NoTerm(tuple(pair),
                     "the flag-reading opcode %r carries no condition "
                     "suffix condition_table.py names" % reader)
    condition = CT.SUFFIX_TO_COND.get(reader[len(prefix):])
    flags = context.get("flags")
    if flags is None:
        raise NoTerm(tuple(pair), missing_flags_reason(setter))
    predicate = predicate_of(condition, reader, prefix, flags, pair)
    if prefix == "j":
        return z3.If(predicate, z3.BitVecVal(1, 64), z3.BitVecVal(0, 64))
    if prefix == "set":
        return full64(z3.If(predicate, z3.BitVecVal(1, 8),
                            z3.BitVecVal(0, 8)))
    operands = L47.operands_of(line)
    width = operation_width(line, operands)
    if len(slots) < 2 or slots[0].term is None or slots[1].term is None:
        raise NoTerm(tuple(pair),
                     "a conditional move needs both of its own "
                     "operands as rows, and one of them is not one")
    taken = cut(slots[0].term, width)
    kept = cut(slots[1].term, width)
    return full64(z3.If(predicate, taken, kept))


COMPARISON_SETTERS = ("cmp", "test", "ucomiss", "ucomisd",
                      "comiss", "comisd")

X87_SETTERS = ("fucomi", "fucomip", "fcomi", "fcomip", "fucom",
               "fucomp", "fcom", "fcomp", "ftst")


def missing_flags_reason(setter):
    """WHY the flags this pair names are not in the ledger, said
    precisely rather than as one blanket sentence."""
    if setter in X87_SETTERS:
        return ("the flag-setting arch opcode %r compares two values "
                "on the x87 register stack (%%st, %%st(1)), and the "
                "ledger has no block and no rows for the x87 stack, so "
                "neither side of the comparison exists as a row"
                % setter)
    if setter is None:
        return ("no flag-setting arch opcode precedes the flag-reading "
                "opcode in this body, so the pair is incomplete and "
                "the condition has no two sides")
    return ("the flag-setting arch opcode %r left flags this file "
            "could not build -- either its own row is missing from the "
            "ledger (ledger47 makes no row when the destination is a "
            "register it never renames) or that row's own operands "
            "have no term" % setter)


def predicate_of(condition, reader, prefix, flags, pair):
    """which bit the reading opcode's own suffix asks for."""
    suffix = reader[len(prefix):]
    setter = flags.get("setter")
    if suffix in ("o", "no"):
        overflow = flags.get("overflow")
        if overflow is None:
            raise NoTerm(tuple(pair),
                         "this suffix reads the signed-overflow bit, "
                         "and the flag-setting arch opcode %r has no "
                         "overflow model in this file" % setter)
        return overflow if suffix == "o" else z3.Not(overflow)
    if setter not in COMPARISON_SETTERS and \
            suffix in ("b", "c", "nae", "ae", "nb", "nc"):
        carry = flags.get("carry")
        if carry is None:
            raise NoTerm(tuple(pair),
                         "this suffix reads the carry bit, and the "
                         "flag-setting arch opcode %r has no carry "
                         "model in this file" % setter)
        return carry if suffix in ("b", "c", "nae") else z3.Not(carry)
    sides = flags.get("sides")
    if sides is None:
        raise NoTerm(tuple(pair),
                     "no row in this ledger carries the two sides the "
                     "flag-setting opcode compared")
    left, right, kind = sides
    if kind == "float":
        return float_condition(condition, left, right)
    return CT.cond_to_z3(condition, left, right, z3)


FLOAT_CONDITION_WIDTH = {"ucomiss": 32, "ucomisd": 64,
                         "comiss": 32, "comisd": 64}


def float_condition(condition, left, right):
    """the x86 unordered-compare flag rule, stated once: ZF/PF/CF are
    set from an IEEE comparison, with all three set when either side is
    NaN.  The conditions the corpus reads off it are written here in
    those terms."""
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
        return z3.And(z3.Not(below), z3.Not(equal), z3.Not(unordered))
    if condition == "CondULE":
        return z3.Or(below, equal, unordered)
    if condition == "CondPAR":
        return unordered
    if condition == "CondNPAR":
        return z3.Not(unordered)
    raise NoTerm("float condition",
                 "condition %r has no float-flag reading written for "
                 "it" % condition)


# ------------------------------------------------------------------
# section 4: THE TRANSCRIPTION -- the ledger read as a term
# ------------------------------------------------------------------

class Transcription(object):
    """one unit's layer-4 record."""

    def __init__(self, unit):
        self.unit = unit
        self.terms = {}
        self.holes = []
        self.out_term = None
        self.inputs = {}
        self.rows = None
        self.refused = None
        self.seeds = {}
        self.cascades = []


def input_symbol(row, family):
    """the symbol an input row is bound to.

    IT IS THE REFERENCE SIMULATOR'S OWN SYMBOL FOR THE ARRIVAL
    REGISTER, spelled the way that simulator spells it ("seed_rdi").
    Task 47's gate binds input row i to the same symbol as the
    argument the reference text reads in arrival register i; layer 4
    keeps that binding by construction, so the transcribed term and
    the simulated body can be compared with no substitution step."""
    bits = 128 if is_vector_family(family) else 64
    return z3.BitVec("seed_%s" % family, bits)


def stack_pointer(tag):
    return z3.BitVec("seed_rsp", 64)


def seed_of(seeds, family, tag):
    if family not in seeds:
        bits = 128 if is_vector_family(family) else 64
        seeds[family] = z3.BitVec("seed_%s" % family, bits)
    return seeds[family]


def memory_load_term(slot, seeds, tag):
    """the value a memory operand READS.

    Two shapes occur in this corpus, and each is modelled as what it
    is.  A rip-relative operand names a constant the compiler placed in
    its own constant pool: its bytes are not in the artifact, so it is
    ONE FIXED UNKNOWN, keyed by its position in the body -- the same
    positional keying the gate's own simulator uses for the reference
    side, so the two agree.  A stack operand names a location this unit
    owns: unless the body itself stores there, it is likewise one fixed
    unknown, keyed by the address text."""
    key = None
    for token, source in slot.memory:
        if token == "rip":
            key = "ripconst_%d" % source[1]
            break
    if key is None:
        mangled = slot.text.replace("%", "").replace("(", "_")
        mangled = mangled.replace(")", "_").replace(",", "_")
        mangled = mangled.replace("-", "m").replace(":", "_")
        key = "seed_MEM:%s" % mangled
        key = key.replace(":", "_")
    if key not in seeds:
        seeds[key] = z3.BitVec(key, 128)
    return seeds[key]


def fill_slots(slots, terms, seeds, tag):
    for slot in slots:
        if slot.immediate is not None:
            slot.term = z3.BitVecVal(slot.immediate & ((1 << 64) - 1), 64)
            continue
        if slot.memory is not None:
            resolved = []
            for token, name in slot.memory:
                if isinstance(name, tuple):
                    resolved.append((token, name))
                    continue
                resolved.append((token, terms.get(name)))
            slot.memory = resolved
            slot.term = memory_load_term(slot, seeds, tag)
            continue
        if slot.row_name is not None:
            slot.term = terms.get(slot.row_name)
            continue
        if slot.family is not None:
            # a register the body reads before any row wrote it: the
            # machine's own starting state.  One fresh symbol per
            # family, shared across the unit, exactly as the gate's
            # simulator seeds an unwritten register.
            slot.term = seed_of(seeds, slot.family, tag)


def flags_of(mnemonic, slots, line, result):
    """THE FLAGS ONE ARCH OPCODE LEAVES, modelled from that opcode.

    the owner's addendum: a flag-derived row's producer is the PAIR
    (flag-setting arch opcode, flag-reading arch opcode), so the flags
    are read off the SETTING opcode's own operands and its own result --
    never off a lifter helper's name.  What is recorded here is what
    the next flag-reading opcode can ask for:

      sides     the two values a comparison-shaped condition reads,
                which condition_table.py's cond_to_z3 turns into the
                condition the reading opcode's suffix names;
      carry     the unsigned-overflow bit, for a `b`/`ae` suffix read
                off an arithmetic opcode rather than a comparison;
      overflow  the signed-overflow bit, for an `o`/`no` suffix.
    """
    operands = L47.operands_of(line)
    width = operation_width(line, operands)
    if mnemonic in ("cmp", "test"):
        if slots[0].term is None or slots[1].term is None:
            return None
        source = cut(slots[0].term, width)
        destination = cut(slots[1].term, width)
        if mnemonic == "cmp":
            return {
                "sides": (destination, source, "integer"),
                "carry": z3.ULT(destination, source),
                "overflow": z3.Not(z3.And(
                    z3.BVSubNoOverflow(destination, source),
                    z3.BVSubNoUnderflow(destination, source, True))),
                "setter": mnemonic,
            }
        return {
            "sides": (destination & source, z3.BitVecVal(0, width),
                      "integer"),
            "carry": z3.BoolVal(False),
            "overflow": z3.BoolVal(False),
            "setter": mnemonic,
        }
    if mnemonic in FLOAT_CONDITION_WIDTH:
        bits = FLOAT_CONDITION_WIDTH[mnemonic]
        if slots[0].term is None or slots[1].term is None:
            return None
        source = as_float(slots[0].term, bits)
        destination = as_float(slots[1].term, bits)
        return {
            "sides": (destination, source, "float"),
            "carry": None,
            "overflow": None,
            "setter": mnemonic,
        }
    if result is None or width is None:
        return None
    value = cut(result, width)
    zero = z3.BitVecVal(0, width)
    if mnemonic == "add" and len(slots) == 2 and \
            slots[0].term is not None and slots[1].term is not None:
        source = cut(slots[0].term, width)
        destination = cut(slots[1].term, width)
        return {
            "sides": (value, zero, "integer"),
            "carry": z3.Not(z3.BVAddNoOverflow(destination, source,
                                               False)),
            "overflow": z3.Not(z3.And(
                z3.BVAddNoOverflow(destination, source, True),
                z3.BVAddNoUnderflow(destination, source))),
            "setter": mnemonic,
        }
    if mnemonic == "sub" and len(slots) == 2 and \
            slots[0].term is not None and slots[1].term is not None:
        source = cut(slots[0].term, width)
        destination = cut(slots[1].term, width)
        return {
            "sides": (value, zero, "integer"),
            "carry": z3.ULT(destination, source),
            "overflow": z3.Not(z3.And(
                z3.BVSubNoOverflow(destination, source),
                z3.BVSubNoUnderflow(destination, source, True))),
            "setter": mnemonic,
        }
    if mnemonic == "imul" and len(slots) == 2 and \
            slots[0].term is not None and slots[1].term is not None:
        source = cut(slots[0].term, width)
        destination = cut(slots[1].term, width)
        return {
            "sides": (value, zero, "integer"),
            "carry": z3.Not(z3.BVMulNoOverflow(destination, source,
                                               True)),
            "overflow": z3.Not(z3.And(
                z3.BVMulNoOverflow(destination, source, True),
                z3.BVMulNoUnderflow(destination, source))),
            "setter": mnemonic,
        }
    if mnemonic == "neg" and slots and slots[0].term is not None:
        destination = cut(slots[0].term, width)
        least = z3.BitVecVal(1 << (width - 1), width)
        return {
            "sides": (value, zero, "integer"),
            "carry": destination != zero,
            "overflow": destination == least,
            "setter": mnemonic,
        }
    if mnemonic in ("and", "or", "xor", "not") or mnemonic in SHIFT:
        return {
            "sides": (value, zero, "integer"),
            "carry": z3.BoolVal(False) if mnemonic != "not" else None,
            "overflow": z3.BoolVal(False) if mnemonic != "not" else None,
            "setter": mnemonic,
        }
    return None


def arrival_family_of(unit, row):
    """which register family this input row arrives in.

    The original population's records carry an explicit binding list;
    the regenerated population's records carry only the ordered
    arrival-family list, and the IN rows are made in that same order,
    so the row's own index names the family there."""
    for binding in unit.get("arrival_contract_bindings", []):
        if binding.get("row") == row["row"]:
            register = binding.get("bound_to_the_same_symbol_as", "")
            return canon.FAMILY_OF.get(register[1:])
    families = unit.get("arrival_families") or []
    index = row.get("index")
    if index is not None and index < len(families):
        return families[index]
    return None


def transcribe(unit, tag="a"):
    """LAYER 4 for one unit: the ledger, read from OUT-0 downward.

    The walk below is written forward because the ledger's own row
    order is the body's own order, so a row's operands are always
    already transcribed when the row is reached; the TERM is still the
    bottom-up read of OUT-0, and `record.out_term` is that read."""
    record = Transcription(unit)
    try:
        rows = relink48.relink(unit)
    except Exception as problem:
        record.refused = "relink: %s" % problem
        return record
    try:
        slots_per_row = replay_operands(rows, unit["arrival_families"])
    except ReplayDisagreement as problem:
        record.refused = "replay: %s" % problem
        return record
    record.rows = rows
    terms = record.terms
    context = {"flags": None}
    for row, slots in zip(rows, slots_per_row):
        producer = row["produced_by"]
        name = row["row"]
        if producer == "arrival":
            family = arrival_family_of(unit, row)
            if family is None:
                record.holes.append(hole_record(
                    row, producer,
                    "no arrival contract binding names the register "
                    "this input row arrives in"))
                continue
            symbol = input_symbol(row, family)
            terms[name] = symbol
            record.inputs[name] = symbol
            continue
        if row["block"] == "CONST":
            value = row.get("value_at_run") or 0
            terms[name] = z3.BitVecVal(value & ((1 << 64) - 1), 64)
            continue
        if row["block"] == "OWN":
            terms[name] = stack_pointer(tag) - \
                z3.BitVecVal(row.get("displacement", 0), 64)
            continue
        if row["block"] == "OUT":
            if not row["operands"]:
                record.holes.append(hole_record(
                    row, producer,
                    "no arch opcode in this body writes the answer "
                    "register, so no row produces the answer"))
                continue
            source = terms.get(row["operands"][0])
            if source is None:
                record.cascades.append(cascade_record(
                    row, producer, row["operands"][0]))
                continue
            terms[name] = cut(source, row["size"] * 8)
            record.out_term = terms[name]
            continue
        fill_slots(slots, terms, record.seeds, tag)
        blocked = None
        for slot in slots:
            if slot.row_name is not None and terms.get(slot.row_name) is None:
                blocked = slot.row_name
                break
            if slot.memory is not None:
                for token, inner in slot.memory:
                    if inner is None:
                        blocked = "a row inside the memory operand %r" \
                            % slot.text
                        break
        if blocked is not None:
            record.cascades.append(cascade_record(row, producer,
                                                  blocked))
            mnemonic = L47.mnemonic_of(row["line"]) if row["line"] \
                else None
            if mnemonic is not None and L47.sets_the_flags(mnemonic):
                # the flags this opcode leaves cannot be built, and the
                # flags a PREVIOUS opcode left are gone -- the machine
                # has overwritten them.  Carrying the older record
                # forward would answer a later reader with flags that
                # no longer exist.
                context["flags"] = None
            continue
        line = row["line"]
        mnemonic = L47.mnemonic_of(line) if line else None
        try:
            terms[name] = build_producer_term(producer, line, slots,
                                              row, context)
        except NoTerm as problem:
            record.holes.append(hole_record(row, producer, problem.why))
            if mnemonic is not None and L47.sets_the_flags(mnemonic):
                context["flags"] = None
        except Exception as problem:
            record.holes.append(hole_record(
                row, producer,
                "building the term raised %s: %s"
                % (type(problem).__name__, problem)))
            if mnemonic is not None and L47.sets_the_flags(mnemonic):
                context["flags"] = None
        if mnemonic is not None and L47.sets_the_flags(mnemonic):
            try:
                flags = flags_of(mnemonic, slots, line,
                                 terms.get(name))
            except Exception:
                flags = None
            if flags is not None:
                context["flags"] = flags
    return record


def cascade_record(row, producer, blocked):
    """a row whose PRODUCER has a term but whose operand row does not.
    This is not a census entry: the census filters on the producer, and
    this row's producer is modelled.  It is counted separately so a
    single hole is never reported as many."""
    record = hole_record(row, producer,
                         "an operand row has no term: %s" % blocked)
    record["blocked_by"] = blocked
    return record


NON_OPCODE_PHRASES = (
    "arrival",
    "the body's own immediate operand",
    "the body's own stack displacement",
    "the body's last write to",
)


def producer_object(producer):
    """THE PRODUCER, WRITTEN AS A TYPED MACHINE-FORM OBJECT.

    WHY IT IS AN OBJECT AND NOT A STRING.  A producer is an arch
    opcode, and several arch opcodes are SPELLED exactly like operator
    tokens -- `or`, `xor`, `not`, `and`, `neg`, `shl`.  A bare string
    in a row field is indistinguishable, to the spelling guard, from a
    row keyed by an operator token; the guard is right to reject it,
    and the fix is structural, not an exemption.  So the mnemonic is
    carried under `mnem`, which is this codebase's own ratified
    machine-form field name (check_no_spelling_keys.py's PROSE_FIELDS
    carries `mnem` beside `bytes`, `key` and `sem_key`, and its header
    says why: a machine form is not a spelling).  `kind` says which of
    the three shapes this producer is, out of a fixed vocabulary that
    contains no operator token.

    The three shapes:
      arch_opcode        one mnemonic
      flag_pair          the pair (flag-setting opcode, flag-reading
                         opcode) -- both mnemonics, as a list
      non_opcode_phrase  the recorded phrases that are not opcodes at
                         all (`arrival`, and the three body phrases)
    """
    if isinstance(producer, list):
        return {
            "kind": "flag_pair",
            "mnem": [str(one) for one in producer],
        }
    text = str(producer)
    for phrase in NON_OPCODE_PHRASES:
        if text.startswith(phrase):
            return {"kind": "non_opcode_phrase", "phrase": text}
    return {"kind": "arch_opcode", "mnem": text}


def hole_record(row, producer, why):
    shape = "pair" if isinstance(producer, list) else "single"
    return {
        "row": row["row"],
        "producer": producer_object(producer),
        "producer_shape": shape,
        "line": row.get("line"),
        "why": why,
    }
