#!/usr/bin/env python3
"""build.py -- ONE CONSTRUCTION PER OPERATION KIND, general in the width
`n` and the word `W`, built from `& | ^ ~`, shifts by CONSTANTS, a
conditional and variables, and from nothing else.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/PROGRESS.md`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

THE OBJECTS, one sentence each, in relation.
  * AN OPERATION KIND is one node kind of a term -- `bvadd`, `bvmul`,
    `bvudiv`, `bvshl`, `extract`, `ite`, `fp.add`, ... -- named by z3's
    own declaration kind and never by a source token.
  * A WORD, `W`, is the widest integer holder the target has, read off
    that target's own renderer table (128 on c, cpp and rust; 64 on go
    and swift, measured in task t2's lane `t2_l1`).
  * A UNIT, `u`, is the width this file does arithmetic at for a value
    of width `n`: `n` itself where `n <= W`, and `W` where it is wider.
    A value is then `k = ceil(n / u)` LIMBS of `u` bits, the bits of the
    top limb above the value's own width held at zero.
  * A CONSTRUCTION is one function here: the operation of width `n`
    written as a sequence of primitive steps over limbs.  It is
    parameterised by `n` and `W` and by NOTHING else -- there is no case
    per opcode name anywhere in this file, and every branch is on a z3
    declaration kind or on a width.
  * THE PRIMITIVE SET, which is the whole of what a construction may
    emit: `&`, `|`, `^`, `~` at the unit's width; `<<`, `>>` (logical
    and arithmetic) by a CONSTANT, which is wiring and not a gate;
    `Extract` and `Concat`, which are the same wiring written the other
    way; a conditional; and variables.  Everything else is built.

THE RULING THIS CARRIES OUT (the owner, 2026-09-10).  "A language with
`& | ^ ~`, a conditional and variables has every gate a processor is
built from, so every opcode's mapping is constructible from them, as a
GUARANTEE."  Task t2 wrote EIGHT schemas for the eight shapes its own
population refused; that is a set of patterns and not the method.  This
file is the method: one construction per KIND, general in `n` and `W`,
so that a kind at a width nobody has met yet is constructed by the same
function.

THE ALGORITHMS ARE THE ONES THE BRIEF NAMES, each general in `n`:
  * add: carry-lookahead (Kogge-Stone) in ceil(log2 n) prefix rounds.
  * sub, neg: the adder over the complement, carry in.
  * multiply: shift-and-add in n rounds; the high half is the same
    construction at width 2n with the top n bits taken.
  * unsigned divide and remainder: restoring division, n rounds, each
    one shift, one subtraction and one conditional choice.
  * signed divide and remainder: the unsigned construction with the
    signs taken off the operands and put back on the answer, exactly as
    SMT-LIB defines the two.
  * shifts by a symbolic count: a barrel of ceil(log2 n) stages, each
    stage a constant shift chosen by one bit of the count, and one
    comparison for a count at or above the width.
  * comparisons: the borrow out of a subtraction; the signed ones by
    flipping both sign bits first.
  * equality: an or-reduction of the exclusive or, log2(u) rounds.
  * widening, narrowing, sign spread, concatenation: wiring.
  * the float kinds: the softfloat constructions over the integer ones,
    in `softfloat.py` beside this file.

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

HOW THIS FILE OBEYS IT.  Every branch below is on a z3 DECL KIND -- a
machine form of the node itself -- and on widths.  Nothing here reads a
mnemonic, a cell, or any name at all.

Coding discipline: no compound one-liner statements.
"""

import z3


# ==================================================================
# section 0: the kinds, their display names, and the refusal
# ==================================================================

class Refused(Exception):
    """no construction for this node; `cause` is the sentence and
    `detail` names the node."""

    def __init__(self, cause, detail=""):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


CAUSE_NO_CONSTRUCTION = ("no construction is written for a node of this "
                         "kind")
CAUSE_ARRIVAL = ("an arrival wider than the target's widest holder: the "
                 "value cannot be received at all, which is a question "
                 "about the arrival contract and not about the "
                 "operation")
CAUSE_SORT = "a node of a sort no construction here is stated over"

# THE KIND NAMES.  Each is a DISPLAY LABEL on one z3 declaration kind;
# the key everywhere in this file and in every record it writes is the
# declaration kind itself, which is machine form.
ADD = "add"
SUBTRACT = "subtract"
NEGATE = "negate"
MULTIPLY = "multiply"
DIVIDE_UNSIGNED = "divide unsigned"
REMAINDER_UNSIGNED = "remainder unsigned"
DIVIDE_SIGNED = "divide signed"
REMAINDER_SIGNED = "remainder signed"
MODULO_SIGNED = "modulo signed"
SHIFT_LEFT = "shift left"
SHIFT_RIGHT_LOGICAL = "shift right logical"
SHIFT_RIGHT_ARITHMETIC = "shift right arithmetic"
ROTATE = "rotate"
BITWISE = "bitwise over the word"
COMPLEMENT = "complement"
COMPARE_UNSIGNED = "compare unsigned"
COMPARE_SIGNED = "compare signed"
EQUALITY = "equality"
CONDITIONAL = "conditional"
WIRING = "wiring: widen, narrow, spread the sign, join"
FLOAT_ARITHMETIC = "float arithmetic"
FLOAT_COMPARE = "float compare"
FLOAT_CLASS = "float class"
FLOAT_CONVERT = "float convert"
FLOAT_WIRING = "float wiring"

KIND_ORDER = [ADD, SUBTRACT, NEGATE, MULTIPLY, DIVIDE_UNSIGNED,
              REMAINDER_UNSIGNED, DIVIDE_SIGNED, REMAINDER_SIGNED,
              MODULO_SIGNED, SHIFT_LEFT, SHIFT_RIGHT_LOGICAL,
              SHIFT_RIGHT_ARITHMETIC, ROTATE, BITWISE, COMPLEMENT,
              COMPARE_UNSIGNED, COMPARE_SIGNED, EQUALITY, CONDITIONAL,
              WIRING, FLOAT_ARITHMETIC, FLOAT_COMPARE, FLOAT_CLASS,
              FLOAT_CONVERT, FLOAT_WIRING]

# THE TABLE FROM A z3 DECLARATION KIND TO THE OPERATION KIND IT IS.
# This is the whole of "which construction answers this node", and it
# is a mapping from machine form to machine form.
KIND_OF_DECL = {
    z3.Z3_OP_BADD: ADD,
    z3.Z3_OP_BSUB: SUBTRACT,
    z3.Z3_OP_BNEG: NEGATE,
    z3.Z3_OP_BMUL: MULTIPLY,
    z3.Z3_OP_BUDIV: DIVIDE_UNSIGNED,
    z3.Z3_OP_BUDIV_I: DIVIDE_UNSIGNED,
    z3.Z3_OP_BUREM: REMAINDER_UNSIGNED,
    z3.Z3_OP_BUREM_I: REMAINDER_UNSIGNED,
    z3.Z3_OP_BSDIV: DIVIDE_SIGNED,
    z3.Z3_OP_BSDIV_I: DIVIDE_SIGNED,
    z3.Z3_OP_BSREM: REMAINDER_SIGNED,
    z3.Z3_OP_BSREM_I: REMAINDER_SIGNED,
    z3.Z3_OP_BSMOD: MODULO_SIGNED,
    z3.Z3_OP_BSMOD_I: MODULO_SIGNED,
    z3.Z3_OP_BSHL: SHIFT_LEFT,
    z3.Z3_OP_BLSHR: SHIFT_RIGHT_LOGICAL,
    z3.Z3_OP_BASHR: SHIFT_RIGHT_ARITHMETIC,
    z3.Z3_OP_EXT_ROTATE_LEFT: ROTATE,
    z3.Z3_OP_EXT_ROTATE_RIGHT: ROTATE,
    z3.Z3_OP_ROTATE_LEFT: ROTATE,
    z3.Z3_OP_ROTATE_RIGHT: ROTATE,
    z3.Z3_OP_BAND: BITWISE,
    z3.Z3_OP_BOR: BITWISE,
    z3.Z3_OP_BXOR: BITWISE,
    z3.Z3_OP_BNOT: COMPLEMENT,
    z3.Z3_OP_ULT: COMPARE_UNSIGNED,
    z3.Z3_OP_ULEQ: COMPARE_UNSIGNED,
    z3.Z3_OP_UGT: COMPARE_UNSIGNED,
    z3.Z3_OP_UGEQ: COMPARE_UNSIGNED,
    z3.Z3_OP_SLT: COMPARE_SIGNED,
    z3.Z3_OP_SLEQ: COMPARE_SIGNED,
    z3.Z3_OP_SGT: COMPARE_SIGNED,
    z3.Z3_OP_SGEQ: COMPARE_SIGNED,
    z3.Z3_OP_EQ: EQUALITY,
    z3.Z3_OP_DISTINCT: EQUALITY,
    z3.Z3_OP_ITE: CONDITIONAL,
    z3.Z3_OP_EXTRACT: WIRING,
    z3.Z3_OP_CONCAT: WIRING,
    z3.Z3_OP_ZERO_EXT: WIRING,
    z3.Z3_OP_SIGN_EXT: WIRING,
    z3.Z3_OP_AND: BITWISE,
    z3.Z3_OP_OR: BITWISE,
    z3.Z3_OP_NOT: COMPLEMENT,
    z3.Z3_OP_XOR: BITWISE,
    z3.Z3_OP_IFF: EQUALITY,
    z3.Z3_OP_IMPLIES: BITWISE,
}

UNSIGNED_COMPARISONS = (z3.Z3_OP_ULT, z3.Z3_OP_ULEQ, z3.Z3_OP_UGT,
                        z3.Z3_OP_UGEQ)
SIGNED_COMPARISONS = (z3.Z3_OP_SLT, z3.Z3_OP_SLEQ, z3.Z3_OP_SGT,
                      z3.Z3_OP_SGEQ)


def kind_of(node):
    """the OPERATION KIND of one node, off z3's own declaration kind.

    A float node is decided by its declaration NAME, which is what z3
    gives for the `fp.*` family, and the four groups below are the ones
    `softfloat.py` states constructions over."""
    decl = node.decl()
    declkind = decl.kind()
    if declkind in KIND_OF_DECL:
        return KIND_OF_DECL[declkind]
    name = "%s" % decl.name()
    if name in ("fp.add", "fp.sub", "fp.mul", "fp.div", "fp.sqrt",
                "fp.fma", "fp.rem", "fp.roundToIntegral", "fp.min",
                "fp.max"):
        return FLOAT_ARITHMETIC
    if name in ("fp.eq", "fp.lt", "fp.leq", "fp.gt", "fp.geq"):
        return FLOAT_COMPARE
    if name in ("fp.isNaN", "fp.isInfinite", "fp.isZero", "fp.isNormal",
                "fp.isSubnormal", "fp.isNegative", "fp.isPositive"):
        return FLOAT_CLASS
    if name in ("fp.to_ieee_bv", "fp.neg", "fp.abs", "+zero", "-zero",
                "+oo", "-oo", "NaN", "fp"):
        return FLOAT_WIRING
    if name in ("to_fp", "to_fp_unsigned", "fp.to_sbv", "fp.to_ubv",
                "fp.to_real"):
        return FLOAT_CONVERT
    return None


# ==================================================================
# section 1: the value -- limbs of the unit's width
# ==================================================================

class Value(object):
    """one node's value, as this file holds it.

    `sort` is "bv", "bool", "fp_bits" or "other".
      * "bv": `limbs` is `ceil(width / unit)` z3 bit-vectors of `unit`
        bits, the top limb's bits above `width` held at zero.
      * "bool": `truth` is one z3 Bool and nothing else is set.
      * "fp_bits": the same limbs a "bv" carries, holding the float's
        IEEE bit pattern at `width = ebits + sbits` -- a float a target
        has no holder for is carried as its bits and never as a value.
      * "other": the node is passed through untouched (a rounding mode).
    """

    def __init__(self, sort, width=0, unit=0, limbs=None, truth=None,
                 passthrough=None, ebits=0, sbits=0):
        self.sort = sort
        self.width = width
        self.unit = unit
        self.limbs = list(limbs or [])
        self.truth = truth
        self.passthrough = passthrough
        self.ebits = ebits
        self.sbits = sbits

    def native(self):
        """the one z3 term this value is, where it is one term: a value
        that fits a single limb, a float the target holds as a float, a
        truth value, or a passthrough."""
        if self.sort == "bool":
            return self.truth
        if self.sort == "other":
            return self.passthrough
        if self.sort == "fp":
            return self.limbs[0]
        if len(self.limbs) == 1 and self.limbs[0].size() == self.width:
            return self.limbs[0]
        return None

    def is_wide(self):
        return self.native() is None


def unit_for(width, word):
    """the width this file does arithmetic at for a value of `width`
    bits on a target whose widest holder is `word` bits."""
    if width <= word:
        return width
    return word


def limb_count(width, unit):
    return (width + unit - 1) // unit


def split_value(term, word):
    """a z3 bit-vector term of ANY width as the limbs of a value: the
    slices of it the target can hold.  WIRING, and it is what a check of
    a construction on its own needs, where the operand is a symbol wider
    than the word."""
    width = term.size()
    unit = unit_for(width, word)
    count = limb_count(width, unit)
    out = []
    for index in range(count):
        take = min(unit, width - index * unit)
        piece = z3.Extract(index * unit + take - 1, index * unit, term)
        if take < unit:
            piece = z3.ZeroExt(unit - take, piece)
        out.append(piece)
        continue
    return Value("bv", width=width, unit=unit, limbs=out)


def as_bits(value, word):
    """a child the target holds as a FLOAT turned into its IEEE bits, so
    a construction over integers can read it.

    `fp.to_ieee_bv` is the operation that says so, and the target's own
    renderer writes it; where the target has no holder for a value that
    wide the binding refuses, which is the answer this file wants."""
    if value.sort != "fp":
        return value
    term = z3.fpToIEEEBV(value.limbs[0])
    width = term.size()
    unit = unit_for(width, word)
    if unit == width:
        return Value("bv", width=width, unit=width, limbs=[term])
    return relimb([([term], width, width)], width, word)


def all_as_bits(children, word):
    out = []
    for child in children:
        out.append(as_bits(child, word))
        continue
    return out


def value_of_term(term, word):
    """a z3 bit-vector term of at most the word's width, as a Value of
    one limb."""
    width = term.size()
    if width > word:
        raise Refused(CAUSE_ARRIVAL, "%d bits against a word of %d"
                      % (width, word))
    return Value("bv", width=width, unit=width, limbs=[term])


# -- the constants -------------------------------------------------

def zero_word(unit):
    return z3.BitVecVal(0, unit)


def ones_word(unit):
    return z3.BitVecVal((1 << unit) - 1, unit)


def bit_at_word(word_term, offset):
    """one bit of a limb, as a 1-bit bit-vector.  WIRING."""
    return z3.Extract(offset, offset, word_term)


def spread(one_bit, unit):
    """a `unit`-wide word of all ones where the bit is 1 and all zeros
    where it is 0.  THE CONDITIONAL, which is in the primitive set."""
    return z3.If(one_bit == z3.BitVecVal(1, 1), ones_word(unit),
                 zero_word(unit))


def zeros(width, unit):
    count = limb_count(width, unit)
    return [zero_word(unit) for _index in range(count)]


def mask_top(limbs, width, unit):
    """the bits above the value's own width cleared in the top limb, so
    every Value in this file carries the same invariant."""
    out = list(limbs)
    count = len(out)
    used = width - (count - 1) * unit
    if used >= unit:
        return out
    out[count - 1] = out[count - 1] & z3.BitVecVal((1 << used) - 1, unit)
    return out


def constant_limbs(number, width, unit):
    """a python integer as the limbs of a value of `width` bits.  A
    NUMERAL'S LIMBS ARE ITS OWN DIGITS in the unit's base: there is no
    operation here and so no lemma is owed for this step."""
    number = number & ((1 << width) - 1)
    count = limb_count(width, unit)
    out = []
    for index in range(count):
        piece = (number >> (index * unit)) & ((1 << unit) - 1)
        out.append(z3.BitVecVal(piece, unit))
    return out


def constant_value(number, width, word):
    unit = unit_for(width, word)
    return Value("bv", width=width, unit=unit,
                 limbs=constant_limbs(number, width, unit))


# ==================================================================
# section 2: WIRING -- gathering bits, and the shifts by a constant
# ==================================================================

def gather(segments, start, count):
    """`count` bits of one bit string, starting at bit `start`, as a z3
    term of exactly `count` bits.

    `segments` is the bit string as a list of (limbs, unit, width),
    LOWEST FIRST, so that a concatenation and a plain value are the same
    object here.  This is WIRING: `Extract` and `Concat` and nothing
    else."""
    pieces = []
    got = 0
    while got < count:
        position = start + got
        take = count - got
        piece = None
        base = 0
        for limbs, unit, width in segments:
            if position < base + width:
                inside = position - base
                index = inside // unit
                offset = inside % unit
                room = min(unit - offset, width - inside)
                take = min(take, room)
                piece = z3.Extract(offset + take - 1, offset,
                                   limbs[index])
                break
            base = base + width
            continue
        if piece is None:
            # above every segment: the bit string is zero there
            piece = z3.BitVecVal(0, take)
        pieces.insert(0, piece)
        got = got + take
        continue
    if len(pieces) == 1:
        return pieces[0]
    return z3.Concat(*pieces)


def relimb(segments, width, word):
    """one bit string re-cut into the limbs of a value of `width` bits.
    WIRING."""
    unit = unit_for(width, word)
    count = limb_count(width, unit)
    out = []
    for index in range(count):
        take = min(unit, width - index * unit)
        piece = gather(segments, index * unit, take)
        if take < unit:
            piece = z3.ZeroExt(unit - take, piece)
        out.append(piece)
        continue
    return Value("bv", width=width, unit=unit, limbs=out)


def segments_of(value):
    return [(value.limbs, value.unit, value.width)]


def sign_word(value):
    """a word of all the value's sign bits.  Two constant shifts and a
    conditional; no comparison and no arithmetic."""
    unit = value.unit
    index = (value.width - 1) // unit
    offset = (value.width - 1) % unit
    return spread(bit_at_word(value.limbs[index], offset), unit)


def sign_filled(value):
    """the limbs with every bit above the value's own width equal to the
    sign bit, so a logical right shift over them IS the arithmetic
    one."""
    out = list(value.limbs)
    count = len(out)
    used = value.width - (count - 1) * value.unit
    if used >= value.unit:
        return out
    above = z3.BitVecVal(((1 << value.unit) - 1) ^ ((1 << used) - 1),
                         value.unit)
    out[count - 1] = out[count - 1] | (sign_word(value) & above)
    return out


def shift_left_constant(limbs, amount, width, unit):
    """the whole value shifted up by a CONSTANT number of bits.  WIRING:
    two constant shifts and one `|` per limb."""
    count = len(limbs)
    whole = amount // unit
    part = amount % unit
    out = []
    for index in range(count):
        source = index - whole
        if source < 0:
            out.append(zero_word(unit))
            continue
        piece = limbs[source]
        if part:
            piece = piece << z3.BitVecVal(part, unit)
            if source - 1 >= 0:
                piece = piece | z3.LShR(limbs[source - 1],
                                        z3.BitVecVal(unit - part, unit))
        out.append(piece)
        continue
    return mask_top(out, width, unit)


def shift_right_constant(limbs, amount, width, unit, fill=None):
    """the whole value shifted down by a CONSTANT number of bits, the
    vacated top filled with `fill` (a word; zero where none is given).
    WIRING."""
    count = len(limbs)
    whole = amount // unit
    part = amount % unit
    if fill is None:
        fill = zero_word(unit)
    out = []
    for index in range(count):
        source = index + whole
        if source >= count:
            out.append(fill)
            continue
        piece = limbs[source]
        if part:
            piece = z3.LShR(piece, z3.BitVecVal(part, unit))
            if source + 1 < count:
                piece = piece | (limbs[source + 1]
                                 << z3.BitVecVal(unit - part, unit))
            else:
                piece = piece | (fill << z3.BitVecVal(unit - part, unit))
        out.append(piece)
        continue
    return mask_top(out, width, unit)


# ==================================================================
# section 3: the constructions over the integer kinds
# ==================================================================

def bitwise(operation, values, width, unit):
    """`&`, `|` or `^` limb by limb.  The primitive itself, at the word."""
    out = []
    for index in range(limb_count(width, unit)):
        piece = values[0].limbs[index]
        for other in values[1:]:
            if operation == "and":
                piece = piece & other.limbs[index]
            elif operation == "or":
                piece = piece | other.limbs[index]
            else:
                piece = piece ^ other.limbs[index]
            continue
        out.append(piece)
        continue
    return Value("bv", width=width, unit=unit,
                 limbs=mask_top(out, width, unit))


def complement(value):
    out = []
    for limb in value.limbs:
        out.append(~limb)
        continue
    return Value("bv", width=value.width, unit=value.unit,
                 limbs=mask_top(out, value.width, value.unit))


def add_with_carry(left, right, width, unit, carry_in=None):
    """CARRY-LOOKAHEAD, ceil(log2 n) prefix rounds -- the brief's own
    algorithm, and it is Kogge-Stone.

    `propagate` is where a carry passes through and `generate` is where
    one is made; the prefix rounds fold the two along the whole width in
    log rounds instead of n, and the sum is the propagate word against
    the carries.  Every step is `&`, `|`, `^` and a constant shift.

    Returns (the sum's limbs, the carry out of the top bit)."""
    count = limb_count(width, unit)
    propagate = []
    generate = []
    for index in range(count):
        propagate.append(left.limbs[index] ^ right.limbs[index])
        generate.append(left.limbs[index] & right.limbs[index])
        continue
    if carry_in is not None:
        carried = z3.ZeroExt(unit - 1, carry_in)
        generate[0] = generate[0] | (propagate[0] & carried)
    first = list(propagate)
    step = 1
    while step < width:
        moved_generate = shift_left_constant(generate, step, width, unit)
        moved_propagate = shift_left_constant(propagate, step, width,
                                              unit)
        next_generate = []
        next_propagate = []
        for index in range(count):
            next_generate.append(generate[index]
                                 | (propagate[index]
                                    & moved_generate[index]))
            next_propagate.append(propagate[index]
                                  & moved_propagate[index])
            continue
        generate = next_generate
        propagate = next_propagate
        step = step * 2
        continue
    carries = shift_left_constant(generate, 1, width, unit)
    if carry_in is not None:
        carries[0] = carries[0] | z3.ZeroExt(unit - 1, carry_in)
    total = []
    for index in range(count):
        total.append(first[index] ^ carries[index])
        continue
    top_index = (width - 1) // unit
    top_offset = (width - 1) % unit
    carry_out = bit_at_word(generate[top_index], top_offset)
    return mask_top(total, width, unit), carry_out


def add_values(left, right, carry_in=None):
    limbs, _carry = add_with_carry(left, right, left.width, left.unit,
                                   carry_in)
    return Value("bv", width=left.width, unit=left.unit, limbs=limbs)


def subtract_with_borrow(left, right, width, unit):
    """the adder over the complement with a carry in of one; the borrow
    is the carry that did NOT come out."""
    flipped = complement(Value("bv", width=width, unit=unit,
                               limbs=right.limbs))
    limbs, carry_out = add_with_carry(left, flipped, width, unit,
                                      z3.BitVecVal(1, 1))
    return limbs, carry_out


def subtract_values(left, right):
    limbs, _carry = subtract_with_borrow(left, right, left.width,
                                         left.unit)
    return Value("bv", width=left.width, unit=left.unit, limbs=limbs)


def negate_value(value):
    return subtract_values(constant_value_like(0, value), value)


def constant_value_like(number, value):
    return Value("bv", width=value.width, unit=value.unit,
                 limbs=constant_limbs(number, value.width, value.unit))


def or_reduce(value):
    """whether any bit of the value is one, as a z3 Bool: the limbs
    folded with `|`, then the word folded into its own bit 0 in log2(u)
    rounds of a constant shift and an `|`."""
    accumulator = value.limbs[0]
    for limb in value.limbs[1:]:
        accumulator = accumulator | limb
        continue
    step = 1
    while step < value.unit:
        accumulator = accumulator | z3.LShR(accumulator,
                                            z3.BitVecVal(step,
                                                         value.unit))
        step = step * 2
        continue
    return bit_at_word(accumulator, 0) == z3.BitVecVal(1, 1)


def equal_values(left, right):
    difference = bitwise("xor", [left, right], left.width, left.unit)
    return z3.Not(or_reduce(difference))


def below_unsigned(left, right):
    """`left <u right`: the BORROW out of the subtraction, which is the
    carry that did not come out."""
    _limbs, carry_out = subtract_with_borrow(left, right, left.width,
                                            left.unit)
    return carry_out == z3.BitVecVal(0, 1)


def with_sign_flipped(value):
    """the value with its top bit inverted, which turns the signed order
    into the unsigned one."""
    top = constant_value_like(1 << (value.width - 1), value)
    return bitwise("xor", [value, top], value.width, value.unit)


def below_signed(left, right):
    return below_unsigned(with_sign_flipped(left),
                          with_sign_flipped(right))


def choose(condition, left, right):
    """the conditional, limb by limb."""
    out = []
    for index in range(len(left.limbs)):
        out.append(z3.If(condition, left.limbs[index],
                         right.limbs[index]))
        continue
    return Value("bv", width=left.width, unit=left.unit, limbs=out)


def choose_by_mask(one_bit, left, right):
    """the conditional written as a mask, which is smaller than a
    conditional per limb where the same bit chooses every one."""
    mask = spread(one_bit, left.unit)
    out = []
    for index in range(len(left.limbs)):
        out.append((left.limbs[index] & mask)
                   | (right.limbs[index] & ~mask))
        continue
    return Value("bv", width=left.width, unit=left.unit, limbs=out)


def bit_of_value(value, position):
    index = position // value.unit
    offset = position % value.unit
    if index >= len(value.limbs):
        return z3.BitVecVal(0, 1)
    return bit_at_word(value.limbs[index], offset)


def multiply(left, right, width, unit):
    """SHIFT-AND-ADD, n rounds: one round per bit of the right operand,
    each round the left operand shifted up by a CONSTANT and masked by
    that bit, added in.

    "Smallest width first" is literal here: every round's addition is
    the carry-lookahead construction above at the same width, and a
    product wider than the word is the same n rounds over more limbs."""
    accumulator = Value("bv", width=width, unit=unit,
                        limbs=zeros(width, unit))
    for position in range(width):
        chosen = spread(bit_of_value(right, position), unit)
        moved = shift_left_constant(left.limbs, position, width, unit)
        partial = []
        for index in range(len(moved)):
            partial.append(moved[index] & chosen)
            continue
        addend = Value("bv", width=width, unit=unit, limbs=partial)
        accumulator = add_values(accumulator, addend)
        continue
    return accumulator


def divide_unsigned(left, right, width, unit, word):
    """RESTORING DIVISION, n rounds: each round one shift, one
    subtraction and one conditional choice.

    The running remainder is held at `width + 1` bits, because the
    shift of a remainder already below the divisor can reach the bit
    above the width.

    THE ANSWER AT A DIVISOR OF ZERO IS SMT-LIB's: the quotient is all
    ones and the remainder is the dividend.  It is stated here as a
    conditional over the loop's answer rather than left to whatever the
    hardware does.

    Returns (quotient, remainder), both Values of `width` bits."""
    wide_width = width + 1
    wide_unit = unit_for(wide_width, word)
    remainder = Value("bv", width=wide_width, unit=wide_unit,
                      limbs=zeros(wide_width, wide_unit))
    divisor = relimb(segments_of(right), wide_width, word)
    quotient = zeros(width, unit)
    for position in range(width - 1, -1, -1):
        moved = shift_left_constant(remainder.limbs, 1, wide_width,
                                    wide_unit)
        moved[0] = moved[0] | z3.ZeroExt(wide_unit - 1,
                                         bit_of_value(left, position))
        remainder = Value("bv", width=wide_width, unit=wide_unit,
                          limbs=moved)
        difference, carry = subtract_with_borrow(remainder, divisor,
                                                 wide_width, wide_unit)
        taken = Value("bv", width=wide_width, unit=wide_unit,
                      limbs=difference)
        remainder = choose_by_mask(carry, taken, remainder)
        index = position // unit
        offset = position % unit
        quotient[index] = quotient[index] | (
            z3.ZeroExt(unit - 1, carry) << z3.BitVecVal(offset, unit))
        continue
    answer = Value("bv", width=width, unit=unit,
                   limbs=mask_top(quotient, width, unit))
    rest = relimb(segments_of(remainder), width, word)
    divisor_is_zero = z3.Not(or_reduce(right))
    all_ones = constant_value_like((1 << width) - 1, answer)
    answer = choose(divisor_is_zero, all_ones, answer)
    rest = choose(divisor_is_zero, left, rest)
    return answer, rest


def signed_division(left, right, width, unit, word, remainder_wanted):
    """SMT-LIB's own definition, written out: the unsigned construction
    over the magnitudes, and the sign put back on the answer.

    `bvsdiv`'s answer is negative where the two signs differ; `bvsrem`
    takes the sign of the DIVIDEND.  Both are stated here as the four
    cases the standard states, folded into two conditionals."""
    left_negative = bit_of_value(left, width - 1) == z3.BitVecVal(1, 1)
    right_negative = bit_of_value(right, width - 1) == z3.BitVecVal(1, 1)
    left_magnitude = choose(left_negative, negate_value(left), left)
    right_magnitude = choose(right_negative, negate_value(right), right)
    quotient, rest = divide_unsigned(left_magnitude, right_magnitude,
                                     width, unit, word)
    if remainder_wanted:
        flipped = choose(left_negative, negate_value(rest), rest)
        return flipped
    differ = z3.Xor(left_negative, right_negative)
    return choose(differ, negate_value(quotient), quotient)


def signed_modulo(left, right, width, unit, word):
    """`bvsmod`, whose answer takes the sign of the DIVISOR: the signed
    remainder, and the divisor added back where the two disagree and the
    remainder is not zero."""
    rest = signed_division(left, right, width, unit, word, True)
    right_negative = bit_of_value(right, width - 1) == z3.BitVecVal(1, 1)
    rest_negative = bit_of_value(rest, width - 1) == z3.BitVecVal(1, 1)
    rest_is_zero = z3.Not(or_reduce(rest))
    adjusted = add_values(rest, right)
    disagree = z3.And(z3.Not(rest_is_zero),
                      z3.Xor(rest_negative, right_negative))
    return choose(disagree, adjusted, rest)


def rounds_for(width):
    """ceil(log2 width), the number of barrel stages a shift needs."""
    stages = 0
    while (1 << stages) < width:
        stages = stages + 1
        continue
    return stages


def shift_by_count(value, count, width, unit, direction, arithmetic):
    """A BARREL of ceil(log2 n) stages: each stage shifts by a CONSTANT
    power of two or does not, chosen by one bit of the count; then one
    comparison decides a count at or above the width, where the answer
    is the fill.

    `direction` is "up" or "down"; `arithmetic` fills with the sign."""
    stages = rounds_for(width)
    running = value
    for stage in range(stages):
        chosen = bit_of_value(count, stage)
        amount = 1 << stage
        if direction == "up":
            moved = shift_left_constant(running.limbs, amount, width,
                                        unit)
        elif arithmetic:
            fill = sign_word(running)
            moved = shift_right_constant(sign_filled(running), amount,
                                         width, unit, fill)
        else:
            moved = shift_right_constant(running.limbs, amount, width,
                                         unit, None)
        stepped = Value("bv", width=width, unit=unit, limbs=moved)
        running = choose_by_mask(chosen, stepped, running)
        continue
    limit = constant_value_like(width, value)
    too_far = z3.Not(below_unsigned(count, limit))
    if arithmetic:
        filler_limbs = []
        for _index in range(limb_count(width, unit)):
            filler_limbs.append(sign_word(value))
            continue
        filler = Value("bv", width=width, unit=unit,
                       limbs=mask_top(filler_limbs, width, unit))
    else:
        filler = Value("bv", width=width, unit=unit,
                       limbs=zeros(width, unit))
    return choose(too_far, filler, running)


def rotate_by_count(value, count, width, unit, word, leftward):
    """a rotate as the two shifts it is: the count taken modulo the
    width by a remainder construction, then up and down and joined."""
    limit = constant_value_like(width, value)
    _quotient, position = divide_unsigned(count, limit, width, unit,
                                          word)
    other = subtract_values(limit, position)
    if leftward:
        up = shift_by_count(value, position, width, unit, "up", False)
        down = shift_by_count(value, other, width, unit, "down", False)
    else:
        up = shift_by_count(value, other, width, unit, "up", False)
        down = shift_by_count(value, position, width, unit, "down",
                              False)
    return bitwise("or", [up, down], width, unit)


# ==================================================================
# section 4: the one entry -- one node, its children's values, its own
# ==================================================================

def build(node, children, word):
    """THE ONE ENTRY: one z3 node and the Values of its children, as the
    Value the construction gives.

    Every branch is on the node's own z3 declaration kind, and on
    widths.  A node this file has no construction for is REFUSED by
    cause and never guessed at."""
    decl = node.decl()
    declkind = decl.kind()
    sortkind = node.sort().kind()
    children = all_as_bits(children, word)
    if sortkind == z3.Z3_BOOL_SORT:
        return build_truth(node, children, declkind, word)
    if z3.is_fp(node):
        import softfloat as SF
        return SF.build_float(node, children, word)
    if sortkind != z3.Z3_BV_SORT:
        raise Refused(CAUSE_SORT, "%s" % node.sort())
    width = node.size()
    unit = unit_for(width, word)
    if declkind == z3.Z3_OP_BNUM:
        return constant_value(node.as_long(), width, word)
    if declkind in (z3.Z3_OP_BAND, z3.Z3_OP_BOR, z3.Z3_OP_BXOR):
        wide = [at_width(one, width, word) for one in children]
        if declkind == z3.Z3_OP_BAND:
            return bitwise("and", wide, width, unit)
        if declkind == z3.Z3_OP_BOR:
            return bitwise("or", wide, width, unit)
        return bitwise("xor", wide, width, unit)
    if declkind == z3.Z3_OP_BNOT:
        return complement(at_width(children[0], width, word))
    if declkind == z3.Z3_OP_BADD:
        running = at_width(children[0], width, word)
        for other in children[1:]:
            running = add_values(running, at_width(other, width, word))
            continue
        return running
    if declkind == z3.Z3_OP_BSUB:
        running = at_width(children[0], width, word)
        for other in children[1:]:
            running = subtract_values(running,
                                      at_width(other, width, word))
            continue
        return running
    if declkind == z3.Z3_OP_BNEG:
        return negate_value(at_width(children[0], width, word))
    if declkind == z3.Z3_OP_BMUL:
        running = at_width(children[0], width, word)
        for other in children[1:]:
            running = multiply(running, at_width(other, width, word),
                               width, unit)
            continue
        return running
    if declkind in (z3.Z3_OP_BUDIV, z3.Z3_OP_BUDIV_I):
        quotient, _rest = divide_unsigned(at_width(children[0], width,
                                                   word),
                                          at_width(children[1], width,
                                                   word),
                                          width, unit, word)
        return quotient
    if declkind in (z3.Z3_OP_BUREM, z3.Z3_OP_BUREM_I):
        _quotient, rest = divide_unsigned(at_width(children[0], width,
                                                   word),
                                          at_width(children[1], width,
                                                   word),
                                          width, unit, word)
        return rest
    if declkind in (z3.Z3_OP_BSDIV, z3.Z3_OP_BSDIV_I):
        return signed_division(at_width(children[0], width, word),
                               at_width(children[1], width, word),
                               width, unit, word, False)
    if declkind in (z3.Z3_OP_BSREM, z3.Z3_OP_BSREM_I):
        return signed_division(at_width(children[0], width, word),
                               at_width(children[1], width, word),
                               width, unit, word, True)
    if declkind in (z3.Z3_OP_BSMOD, z3.Z3_OP_BSMOD_I):
        return signed_modulo(at_width(children[0], width, word),
                             at_width(children[1], width, word),
                             width, unit, word)
    if declkind == z3.Z3_OP_BSHL:
        return shift_by_count(at_width(children[0], width, word),
                              at_width(children[1], width, word),
                              width, unit, "up", False)
    if declkind == z3.Z3_OP_BLSHR:
        return shift_by_count(at_width(children[0], width, word),
                              at_width(children[1], width, word),
                              width, unit, "down", False)
    if declkind == z3.Z3_OP_BASHR:
        return shift_by_count(at_width(children[0], width, word),
                              at_width(children[1], width, word),
                              width, unit, "down", True)
    if declkind in (z3.Z3_OP_EXT_ROTATE_LEFT, z3.Z3_OP_ROTATE_LEFT):
        return rotate_of(node, children, width, unit, word, True)
    if declkind in (z3.Z3_OP_EXT_ROTATE_RIGHT, z3.Z3_OP_ROTATE_RIGHT):
        return rotate_of(node, children, width, unit, word, False)
    if declkind == z3.Z3_OP_EXTRACT:
        _high, low = node.params()
        source = children[0]
        return relimb_from(source, low, width, word)
    if declkind == z3.Z3_OP_CONCAT:
        segments = []
        for child in reversed(children):
            segments.append((child.limbs, child.unit, child.width))
            continue
        return relimb(segments, width, word)
    if declkind == z3.Z3_OP_ZERO_EXT:
        source = children[0]
        return relimb(segments_of(source), width, word)
    if declkind == z3.Z3_OP_SIGN_EXT:
        source = children[0]
        return sign_spread(source, width, word)
    if declkind == z3.Z3_OP_ITE:
        condition = children[0].truth
        left = at_width(children[1], width, word)
        right = at_width(children[2], width, word)
        return choose(condition, left, right)
    raise Refused(CAUSE_NO_CONSTRUCTION,
                  "%s at %d bits" % (decl.name(), width))


def rotate_of(node, children, width, unit, word, leftward):
    if len(children) > 1:
        return rotate_by_count(at_width(children[0], width, word),
                               at_width(children[1], width, word),
                               width, unit, word, leftward)
    amount = node.params()[0] % width
    value = at_width(children[0], width, word)
    if leftward:
        up = shift_left_constant(value.limbs, amount, width, unit)
        down = shift_right_constant(value.limbs, width - amount, width,
                                    unit)
    else:
        up = shift_left_constant(value.limbs, width - amount, width,
                                 unit)
        down = shift_right_constant(value.limbs, amount, width, unit)
    out = []
    for index in range(len(up)):
        out.append(up[index] | down[index])
        continue
    return Value("bv", width=width, unit=unit,
                 limbs=mask_top(out, width, unit))


def above_mask(from_bit, width, unit):
    """the limbs of a constant that is one at every bit at or above
    `from_bit` and zero below it."""
    number = ((1 << width) - 1) ^ ((1 << from_bit) - 1)
    return constant_limbs(number, width, unit)


def sign_bit_of(value):
    """the value's own sign bit, as a 1-bit bit-vector.  WIRING."""
    index = (value.width - 1) // value.unit
    offset = (value.width - 1) % value.unit
    return bit_at_word(value.limbs[index], offset)


def sign_spread(source, width, word):
    """the source widened to `width` with its sign bit repeated above
    its own width: the widening is wiring and the repetition is one
    conditional."""
    widened = relimb(segments_of(source), width, word)
    above = above_mask(source.width, width, widened.unit)
    spreadword = spread(sign_bit_of(source), widened.unit)
    out = []
    for index in range(len(widened.limbs)):
        out.append(widened.limbs[index] | (spreadword & above[index]))
        continue
    return Value("bv", width=width, unit=widened.unit,
                 limbs=mask_top(out, width, widened.unit))


def relimb_from(source, low, width, word):
    unit = unit_for(width, word)
    count = limb_count(width, unit)
    out = []
    for index in range(count):
        take = min(unit, width - index * unit)
        piece = gather(segments_of(source), low + index * unit, take)
        if take < unit:
            piece = z3.ZeroExt(unit - take, piece)
        out.append(piece)
        continue
    return Value("bv", width=width, unit=unit, limbs=out)


def at_width(value, width, word):
    """a child's value re-cut to the width its consumer reads it at.
    Where the two already agree this is the value itself."""
    if value.sort == "bool":
        return value
    if value.width == width and value.unit == unit_for(width, word):
        return value
    return relimb(segments_of(value), width, word)


def build_truth(node, children, declkind, word):
    """the constructions whose answer is a truth value."""
    if declkind == z3.Z3_OP_EQ:
        left = children[0]
        right = children[1]
        if left.sort == "bool":
            return Value("bool", truth=(left.truth == right.truth))
        width = max(left.width, right.width)
        return Value("bool",
                     truth=equal_values(at_width(left, width, word),
                                        at_width(right, width, word)))
    if declkind == z3.Z3_OP_DISTINCT:
        left = children[0]
        right = children[1]
        width = max(left.width, right.width)
        return Value("bool",
                     truth=z3.Not(equal_values(at_width(left, width,
                                                        word),
                                               at_width(right, width,
                                                        word))))
    if declkind in UNSIGNED_COMPARISONS or declkind in SIGNED_COMPARISONS:
        left = children[0]
        right = children[1]
        width = max(left.width, right.width)
        left = at_width(left, width, word)
        right = at_width(right, width, word)
        signed = declkind in SIGNED_COMPARISONS
        if signed:
            below = below_signed
        else:
            below = below_unsigned
        if declkind in (z3.Z3_OP_ULT, z3.Z3_OP_SLT):
            return Value("bool", truth=below(left, right))
        if declkind in (z3.Z3_OP_UGT, z3.Z3_OP_SGT):
            return Value("bool", truth=below(right, left))
        if declkind in (z3.Z3_OP_ULEQ, z3.Z3_OP_SLEQ):
            return Value("bool", truth=z3.Not(below(right, left)))
        return Value("bool", truth=z3.Not(below(left, right)))
    if declkind == z3.Z3_OP_AND:
        return Value("bool",
                     truth=z3.And(*[one.truth for one in children]))
    if declkind == z3.Z3_OP_OR:
        return Value("bool",
                     truth=z3.Or(*[one.truth for one in children]))
    if declkind == z3.Z3_OP_NOT:
        return Value("bool", truth=z3.Not(children[0].truth))
    if declkind == z3.Z3_OP_XOR:
        return Value("bool", truth=z3.Xor(children[0].truth,
                                          children[1].truth))
    if declkind == z3.Z3_OP_IFF:
        return Value("bool", truth=(children[0].truth
                                    == children[1].truth))
    if declkind == z3.Z3_OP_IMPLIES:
        return Value("bool", truth=z3.Or(z3.Not(children[0].truth),
                                         children[1].truth))
    if declkind == z3.Z3_OP_ITE:
        return Value("bool", truth=z3.If(children[0].truth,
                                         children[1].truth,
                                         children[2].truth))
    if declkind == z3.Z3_OP_TRUE:
        return Value("bool", truth=z3.BoolVal(True))
    if declkind == z3.Z3_OP_FALSE:
        return Value("bool", truth=z3.BoolVal(False))
    import softfloat as SF
    return SF.build_float_truth(node, children, word)


# ==================================================================
# section 5: the value put back together, for the equality
# ==================================================================

def joined(value):
    """the value as ONE z3 term of its own width, so the construction
    can be posed against the operation it replaced.  WIRING."""
    if value.sort == "bool":
        return value.truth
    if value.sort == "other":
        return value.passthrough
    return gather(segments_of(value), 0, value.width)


def node_count(term, ceiling=None, seen=None):
    """the number of DISTINCT nodes of a term -- what the renderer with
    named intermediates writes, one statement per node, and never the
    unfolded count the old renderer wrote."""
    if seen is None:
        seen = set()
    stack = [term]
    while stack:
        node = stack.pop()
        key = node.get_id()
        if key in seen:
            continue
        seen.add(key)
        if ceiling is not None and len(seen) >= ceiling:
            return len(seen)
        for index in range(node.num_args()):
            stack.append(node.arg(index))
            continue
        continue
    return len(seen)
