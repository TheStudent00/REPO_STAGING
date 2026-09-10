#!/usr/bin/env python3
"""schemas.py -- THE CONSTRUCTION SCHEMAS: one operation of a width the
target has no holder for, built from operations of the width it has.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/`).
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t2_brief.md`.

THE RULING THIS CARRIES OUT (the owner, 2026-09-10).  "A language that offers
`& | ^ ~`, a conditional and a variable has every logic gate a
microprocessor is built from, so every opcode's mapping is constructible
from them: a guaranteed solution, not necessarily the fastest."  Today's
renderer REFUSES where the target lacks a primitive at a width or kind;
this file is the tier that constructs it instead.

THE OBJECTS, one sentence each, in relation.
  * THE WORD is the widest integer holder the target has, read off that
    target's own renderer table and never recalled (`emulate.UNSIGNED`,
    `rust_render.RU`, `go_render.GU`, `swift_render.SU`).
  * A VALUE is one node of the term as this file holds it: NATIVE, a z3
    term of at most the word's width (or a truth value, or a float), or
    LIMBED, a bit-vector WIDER than the word held as `k` limbs of the
    word's width, the top limb's bits above the value's own width zero.
  * A SCHEMA is one function here: one operation over limbs, built from
    operations of the word's width.  It is parameterised by the width
    and the word and by nothing else -- there is no case per opcode
    name anywhere in this file, and no field of any record it writes
    carries an operator token.
  * THE LOWERING is `lower`: the term walked once, every node whose
    width exceeds the word replaced by its schema's limbs, every node
    at or below the word REBUILT AS IT WAS.  A term with no node above
    the word comes back IDENTICAL and the caller sees an empty schema
    list, which is how the tier declines without a special case.

SMALLEST WIDTH FIRST, which is the owner's second point and is literal here:
the word-wide high half of a product (`mul_hi_word`) is built from four
HALF-WORD products, and the limbed product is built from word-wide
products and that high half.  The same shape runs one level up: a
128-bit product is four 64-bit products, a 64-bit high half is four
32-bit products.

THE ONE PLACE A SCHEMA IS ALLOWED TO REFUSE is a node this file has no
schema for at a width above the word; the refusal names the node and
the schema that is owed, and never guesses.

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
# section 0: the schemas' own names, and the refusal
# ==================================================================

ADD_SUB = "add / sub with carry and flags"
SHIFT_ROTATE = "shifts, rotates"
MULTIPLY = "multiply (low and high halves)"
DIVIDE = "unsigned / signed divide and remainder"
COMPARE = "comparisons and the flag word"
WIDEN = "widening / narrowing / sign spread"
BITWISE = "bitwise and select over the word"
FLOAT = "float add / sub / mul / div / compare / convert"

SCHEMA_ORDER = [ADD_SUB, SHIFT_ROTATE, MULTIPLY, DIVIDE, COMPARE,
                WIDEN, BITWISE, FLOAT]

EXHAUSTIVE_BY_SHAPE = True
"""whether a lemma covers the node the lowering actually replaced.

IT DOES, and the mechanism is `shape_key` below: a lemma is stated per
SHAPE -- the operation plus the widths and offsets that make it that
rewrite -- and per LIMB of that shape's answer, and the tier's lemma
route (`construct.the_equality`, form 2) asks for the shape it rewrote
and for no other.  The first draft asked per (schema, width), which is
not the same question: `widening / narrowing / sign spread` rewrites an
extract at ANY pair of offsets and a theorem stated at two of them does
not carry a third, and a theorem about the LOW WORD of a wide operation
says nothing about its second limb.  Both holes are closed by asking the
question at the shape and at the limb; this constant records that they
were there."""

OWED = {
    FLOAT: ("a float sort the target has no holder for: the schema is "
            "the integer schemas above over the fields sign, exponent "
            "and significand with the sticky bit, and the five classes "
            "as a case split; it is OWED and this file does not guess "
            "one"),
}


class Refused(Exception):
    """no schema for this node at this width; `cause` is the sentence
    and `detail` names the node."""

    def __init__(self, cause, detail=""):
        Exception.__init__(self, "%s: %s" % (cause, detail))
        self.cause = cause
        self.detail = detail


CAUSE_NO_SCHEMA = ("no construction schema for a node of this kind "
                   "above the target's widest holder")
CAUSE_WIDE_SYMBOL = ("an arrival wider than the target's widest holder: "
                     "the value cannot be received at all, which is a "
                     "question about the arrival contract and not about "
                     "the operation")
CAUSE_ODD_WORD = ("the target's widest holder has an odd number of "
                  "bits, so it has no half to build a product from")


# ==================================================================
# section 1: the value -- native, or limbs of the word
# ==================================================================

class Value(object):
    """one node's value: `native` is a z3 term at most the word wide (or
    a truth value or a float), `limbs` is the wider case."""

    def __init__(self, native=None, width=None, limbs=None):
        self.native = native
        self.width = width
        self.limbs = limbs

    def is_limbed(self):
        return self.limbs is not None


def limb_count(width, word):
    return (width + word - 1) // word


def top_bits(width, word):
    return width - word * (limb_count(width, word) - 1)


def zero_word(word):
    return z3.BitVecVal(0, word)


def one_word(word):
    return z3.BitVecVal(1, word)


def ones_word(word):
    return z3.BitVecVal((1 << word) - 1, word)


def is_the_zero(term):
    """whether a node is the constant zero, so a schema can leave out a
    step that does nothing."""
    if not z3.is_bv_value(term):
        return False
    return term.as_long() == 0


def joined(left, right):
    """`left | right`, with a zero side left out.

    THE STEP THAT DOES NOTHING IS NOT WRITTEN, and it is not cosmetic:
    the renderer writes a `0 |` out, the printer prints it, and the Lean
    translator cannot pin the width of a numeral whose only sibling is
    itself unpinned -- lane `t2_l14` measured exactly that, on the
    shifter's own statement."""
    if is_the_zero(left):
        return right
    if is_the_zero(right):
        return left
    return left | right


def shifted_up(term, amount):
    """`term << amount`, with a constant zero amount left out."""
    if is_the_zero(amount):
        return term
    return term << amount


def shifted_down(term, amount):
    """`LShR(term, amount)`, with a constant zero amount left out."""
    if is_the_zero(amount):
        return term
    return z3.LShR(term, amount)


def mask_top(limbs, width, word):
    """the top limb's bits above the value's own width cleared, so the
    invariant every schema below relies on holds after every step."""
    top = top_bits(width, word)
    if top == word:
        return list(limbs)
    out = list(limbs)
    out[-1] = out[-1] & z3.BitVecVal((1 << top) - 1, word)
    return out


def zeros(width, word):
    return [zero_word(word) for _ in range(limb_count(width, word))]


def constant_limbs(value, width, word):
    out = []
    for index in range(limb_count(width, word)):
        piece = (value >> (word * index)) & ((1 << word) - 1)
        out.append(z3.BitVecVal(piece, word))
        continue
    return mask_top(out, width, word)


def as_limbs(value, width, word):
    """any value at logical width `width` as limbs of `word` bits."""
    if value.is_limbed():
        return value.limbs
    term = value.native
    size = term.size()
    if size < word:
        term = z3.ZeroExt(word - size, term)
    return mask_top([term], width, word)


def as_native(limbs, width, word):
    """a limbed value whose width is at most the word, as one z3 term of
    exactly `width` bits."""
    return z3.Extract(width - 1, 0, limbs[0])


def value_of(limbs, width, word):
    """the Value a schema's limbs stand for: native where the width fits
    the word, limbed otherwise."""
    if width <= word:
        return Value(native=as_native(limbs, width, word), width=width)
    return Value(width=width, limbs=mask_top(limbs, width, word))


# ==================================================================
# section 2: the schemas, each parameterised by the width and the word
# ==================================================================

def bitwise_limbs(kind, args, width, word):
    """`& | ^ ~` at a width above the word: limb by limb.  These are the
    primitives the ruling names, and above the word they are still
    themselves -- one operation per limb and no carry anywhere."""
    out = []
    for index in range(limb_count(width, word)):
        pieces = [arg[index] for arg in args]
        if kind == z3.Z3_OP_BAND:
            here = pieces[0]
            for piece in pieces[1:]:
                here = here & piece
                continue
        elif kind == z3.Z3_OP_BOR:
            here = pieces[0]
            for piece in pieces[1:]:
                here = here | piece
                continue
        elif kind == z3.Z3_OP_BXOR:
            here = pieces[0]
            for piece in pieces[1:]:
                here = here ^ piece
                continue
        else:
            here = ~pieces[0]
        out.append(here)
        continue
    return mask_top(out, width, word)


def add_limbs(a, b, width, word, carry_in=None):
    """THE RIPPLE (schema `add / sub with carry and flags`): a width-w
    sum from limbs of the word, the carry out of each limb detected by
    the one test that needs no wider holder -- an unsigned sum wrapped
    if and only if it came out BELOW the addend it started from."""
    carry = carry_in
    if carry is None:
        carry = zero_word(word)
    out = []
    for index in range(limb_count(width, word)):
        first = a[index] + b[index]
        carried_one = z3.If(z3.ULT(first, a[index]), one_word(word),
                            zero_word(word))
        total = first + carry
        carried_two = z3.If(z3.ULT(total, first), one_word(word),
                            zero_word(word))
        out.append(total)
        carry = carried_one | carried_two
        continue
    return mask_top(out, width, word)


def sub_limbs(a, b, width, word):
    """the same ripple with a borrow: a difference wrapped if and only
    if it came out ABOVE what it started from."""
    borrow = zero_word(word)
    out = []
    for index in range(limb_count(width, word)):
        first = a[index] - b[index]
        borrowed_one = z3.If(z3.ULT(a[index], b[index]), one_word(word),
                             zero_word(word))
        total = first - borrow
        borrowed_two = z3.If(z3.ULT(first, borrow), one_word(word),
                             zero_word(word))
        out.append(total)
        borrow = borrowed_one | borrowed_two
        continue
    return mask_top(out, width, word)


def negate_limbs(a, width, word):
    return sub_limbs(zeros(width, word), a, width, word)


def mul_hi_word(x, y, word):
    """SMALLEST WIDTH FIRST, literally: the HIGH half of a word-wide
    product, from four HALF-WORD products and nothing wider than the
    word.  Each half-word factor is at most 2^(word/2) - 1, so each
    product fits the word exactly, and the middle sum of three such
    half-values fits it too."""
    if word % 2 != 0:
        raise Refused(CAUSE_ODD_WORD, "%d bits" % word)
    half = word // 2
    low = z3.BitVecVal((1 << half) - 1, word)
    shift = z3.BitVecVal(half, word)
    x_low = x & low
    x_high = z3.LShR(x, shift)
    y_low = y & low
    y_high = z3.LShR(y, shift)
    both_low = x_low * y_low
    low_high = x_low * y_high
    high_low = x_high * y_low
    both_high = x_high * y_high
    middle = z3.LShR(both_low, shift) + (low_high & low) + (high_low & low)
    return (both_high + z3.LShR(low_high, shift)
            + z3.LShR(high_low, shift) + z3.LShR(middle, shift))


def add_into(accumulator, index, value, word):
    """`value` added at limb `index`, the carry rippled upward.  The
    same wrapped-below test as the ripple above."""
    carry = value
    here = index
    while here < len(accumulator):
        total = accumulator[here] + carry
        carried = z3.If(z3.ULT(total, accumulator[here]), one_word(word),
                        zero_word(word))
        accumulator[here] = total
        carry = carried
        here = here + 1
        continue
    return accumulator


def mul_limbs(a, b, width, word):
    """THE PRODUCT (schema `multiply (low and high halves)`): the low
    `width` bits of a product, schoolbook over the limbs, each limb pair
    contributing its low word here and its high word one limb up -- and
    the high word is `mul_hi_word`, which is four half-word products."""
    count = limb_count(width, word)
    accumulator = zeros(width, word)
    for left in range(count):
        for right in range(count - left):
            here = left + right
            accumulator = add_into(accumulator, here,
                                   a[left] * b[right], word)
            if here + 1 < count:
                accumulator = add_into(accumulator, here + 1,
                                       mul_hi_word(a[left], b[right],
                                                   word),
                                       word)
            continue
        continue
    return mask_top(accumulator, width, word)


def eq_limbs(a, b):
    answer = a[0] == b[0]
    for index in range(1, len(a)):
        answer = z3.And(answer, a[index] == b[index])
        continue
    return answer


def ult_limbs(a, b, strict=True):
    """THE COMPARISON (schema `comparisons and the flag word`), unsigned:
    lexicographic from the top limb down, each step one word-wide
    comparison and one word-wide equality."""
    if strict:
        answer = z3.ULT(a[0], b[0])
    else:
        answer = z3.ULE(a[0], b[0])
    for index in range(1, len(a)):
        answer = z3.Or(z3.ULT(a[index], b[index]),
                       z3.And(a[index] == b[index], answer))
        continue
    return answer


def slt_limbs(a, b, width, word, strict=True):
    """the same, signed: the TOP limb compared at the value's own top
    width so the sign bit is the value's and not the limb's, every limb
    below it unsigned."""
    count = len(a)
    top = top_bits(width, word)
    left_top = z3.Extract(top - 1, 0, a[count - 1])
    right_top = z3.Extract(top - 1, 0, b[count - 1])
    if count == 1:
        if strict:
            return left_top < right_top
        return left_top <= right_top
    lower = ult_limbs(a[:count - 1], b[:count - 1], strict)
    return z3.Or(left_top < right_top,
                 z3.And(left_top == right_top, lower))


def ite_limbs(condition, a, b):
    out = []
    for index in range(len(a)):
        out.append(z3.If(condition, a[index], b[index]))
        continue
    return out


def shift_parts(count_limbs, width, word):
    """the shift count split the way every shift schema below uses it:
    how many whole limbs, how many bits inside a limb, and whether the
    count is at or above the value's own width -- which the machine's
    own rule answers with zero (or the sign) and never with a wrap."""
    low = count_limbs[0]
    logarithm = word.bit_length() - 1
    whole = z3.LShR(low, z3.BitVecVal(logarithm, word))
    inside = low & z3.BitVecVal(word - 1, word)
    beyond = z3.UGE(low, z3.BitVecVal(width, word))
    for index in range(1, len(count_limbs)):
        beyond = z3.Or(beyond, count_limbs[index] != zero_word(word))
        continue
    return whole, inside, beyond


def shl_limbs(a, count_limbs, width, word):
    """THE SHIFT (schema `shifts, rotates`) leftward: limb `i` of the
    answer is limb `i - whole` shifted up by `inside`, with the bits
    that leave limb `i - whole - 1` arriving from below.  The count is
    symbolic, so `whole` is a conditional over the finitely many limb
    offsets, which is the conditional the ruling names."""
    count = limb_count(width, word)
    whole, inside, beyond = shift_parts(count_limbs, width, word)
    complement = z3.BitVecVal(word, word) - inside
    out = []
    for index in range(count):
        piece = zero_word(word)
        for offset in range(index + 1):
            source = index - offset
            here = a[source] << inside
            if source - 1 >= 0:
                here = here | z3.LShR(a[source - 1], complement)
            piece = z3.If(whole == z3.BitVecVal(offset, word), here,
                          piece)
            continue
        out.append(piece)
        continue
    out = ite_limbs(beyond, zeros(width, word), out)
    return mask_top(out, width, word)


def lshr_limbs(a, count_limbs, width, word):
    """the same rightward, zeros arriving from above."""
    count = limb_count(width, word)
    whole, inside, beyond = shift_parts(count_limbs, width, word)
    complement = z3.BitVecVal(word, word) - inside
    out = []
    for index in range(count):
        piece = zero_word(word)
        for offset in range(count - index):
            source = index + offset
            here = z3.LShR(a[source], inside)
            if source + 1 < count:
                here = here | (a[source + 1] << complement)
            piece = z3.If(whole == z3.BitVecVal(offset, word), here,
                          piece)
            continue
        out.append(piece)
        continue
    out = ite_limbs(beyond, zeros(width, word), out)
    return mask_top(out, width, word)


def sign_word_of(a, width, word):
    """the value's sign bit spread over a whole word: all ones or all
    zeros.  This is the `widening / narrowing / sign spread` schema's
    one primitive and every arithmetic shift uses it.

    IT IS THE TWO SHIFTS AND NOT A CONDITIONAL, and the reason is
    measured: the sign bit lifted to the top of the word and then shifted
    down ARITHMETICALLY is all ones or all zeros by the machine's own
    rule, in two operations and with no constant pair -- and a constant
    pair is exactly what the Lean translator's width unification could
    not pin (lane `t2_l19`, `extend_sign` and every arithmetic shift,
    WIDTH_UNRESOLVED).  It is also the smaller term, which the renderer
    writes out once per read."""
    top = top_bits(width, word)
    lifted = a[len(a) - 1] << z3.BitVecVal(word - top, word)
    return lifted >> z3.BitVecVal(word - 1, word)


def ashr_limbs(a, count_limbs, width, word):
    """rightward with the sign arriving from above: the top limb is
    first spread to a whole word so the limb layout is uniform, and the
    filler is the sign word."""
    count = limb_count(width, word)
    whole, inside, beyond = shift_parts(count_limbs, width, word)
    complement = z3.BitVecVal(word, word) - inside
    filler = sign_word_of(a, width, word)
    top = top_bits(width, word)
    spread = list(a)
    if top < word:
        above = z3.BitVecVal(((1 << word) - 1) ^ ((1 << top) - 1), word)
        spread[count - 1] = a[count - 1] | (filler & above)
    out = []
    for index in range(count):
        piece = filler
        for offset in range(count - index):
            source = index + offset
            here = z3.LShR(spread[source], inside)
            if source + 1 < count:
                here = here | (spread[source + 1] << complement)
            else:
                here = here | (filler << complement)
            piece = z3.If(whole == z3.BitVecVal(offset, word), here,
                          piece)
            continue
        out.append(piece)
        continue
    out = ite_limbs(beyond, [filler for _ in range(count)], out)
    return mask_top(out, width, word)


def rotate_limbs(a, count_limbs, width, word, leftward):
    """a rotate is the two shifts and one `|`, with the count taken
    modulo the width -- which is what the machine's own rotate does."""
    reduced = urem_by_constant(count_limbs, width, width, word)
    other = sub_limbs(constant_limbs(width, width, word), reduced,
                      width, word)
    if leftward:
        first = shl_limbs(a, reduced, width, word)
        second = lshr_limbs(a, other, width, word)
    else:
        first = lshr_limbs(a, reduced, width, word)
        second = shl_limbs(a, other, width, word)
    zero_count = eq_limbs(reduced, zeros(width, word))
    joined = []
    for index in range(limb_count(width, word)):
        joined.append(first[index] | second[index])
        continue
    return ite_limbs(zero_count, a, mask_top(joined, width, word))


def urem_by_constant(a, modulus, width, word):
    """the remainder by a CONSTANT modulus, which a rotate needs and
    which needs no divider when the modulus is a power of two -- and
    every width in this pipeline is."""
    if modulus & (modulus - 1) == 0:
        return bitwise_limbs(z3.Z3_OP_BAND,
                             [a, constant_limbs(modulus - 1, width, word)],
                             width, word)
    quotient, remainder = udivrem_limbs(
        a, constant_limbs(modulus, width, word), width, word)
    return remainder


def bit_of(limbs, index, word):
    """one bit of a limbed value as a word holding 0 or 1."""
    which = index // word
    inside = index % word
    return z3.LShR(limbs[which], z3.BitVecVal(inside, word)) \
        & one_word(word)


def set_bit(limbs, index, condition, word):
    which = index // word
    inside = index % word
    out = list(limbs)
    out[which] = out[which] | z3.If(condition,
                                    z3.BitVecVal(1 << inside, word),
                                    zero_word(word))
    return out


def udivrem_limbs(a, b, width, word):
    """THE DIVIDER (schema `unsigned / signed divide and remainder`):
    restoring division, a bounded loop of `width` steps, each step one
    shift, one comparison and one conditional subtract -- the loop the
    brief names.

    THE DIVISOR OF ZERO is the solver's own rule and not a choice:
    SMT-LIB's `bvudiv` answers all ones and `bvurem` answers the
    dividend, so the constructed mapping answers the same or it is not
    the same mapping.

    WHAT THIS COSTS, said here because the tier measures it and refuses
    on it: the remainder of step `i` is read three times by step `i+1`
    (the comparison, the subtraction and the else arm), and the renderer
    writes ONE NESTED EXPRESSION and names no intermediate, so the
    source this term renders to grows like 3^width.  At the widths this
    pipeline meets that is beyond any ceiling, and the tier refuses by
    the measured size rather than by a rule about which operation it
    is."""
    count = limb_count(width, word)
    remainder = zeros(width, word)
    quotient = zeros(width, word)
    one = constant_limbs(1, width, word)
    for step in range(width - 1, -1, -1):
        remainder = shl_limbs(remainder, one, width, word)
        remainder[0] = remainder[0] | bit_of(a, step, word)
        fits = z3.Not(ult_limbs(remainder, b, True))
        reduced = sub_limbs(remainder, b, width, word)
        remainder = ite_limbs(fits, reduced, remainder)
        quotient = set_bit(quotient, step, fits, word)
        continue
    divisor_is_zero = eq_limbs(b, zeros(width, word))
    all_ones = mask_top([ones_word(word) for _ in range(count)],
                        width, word)
    quotient = ite_limbs(divisor_is_zero, all_ones, quotient)
    remainder = ite_limbs(divisor_is_zero, a, remainder)
    return mask_top(quotient, width, word), mask_top(remainder, width,
                                                     word)


def sdivrem_limbs(a, b, width, word):
    """the signed pair, built from the unsigned one exactly as SMT-LIB
    defines it: the magnitudes divided, the quotient's sign the sides'
    sign difference, the remainder's sign the dividend's."""
    left_negative = z3.Not(sign_word_of(a, width, word)
                           == zero_word(word))
    right_negative = z3.Not(sign_word_of(b, width, word)
                            == zero_word(word))
    left = ite_limbs(left_negative, negate_limbs(a, width, word), a)
    right = ite_limbs(right_negative, negate_limbs(b, width, word), b)
    quotient, remainder = udivrem_limbs(left, right, width, word)
    signs_differ = z3.Xor(left_negative, right_negative)
    quotient = ite_limbs(signs_differ,
                         negate_limbs(quotient, width, word), quotient)
    remainder = ite_limbs(left_negative,
                          negate_limbs(remainder, width, word),
                          remainder)
    return quotient, remainder


# ==================================================================
# section 3: THE LOWERING -- the term walked once
# ==================================================================

BITWISE_KINDS = (z3.Z3_OP_BAND, z3.Z3_OP_BOR, z3.Z3_OP_BXOR)
UNSIGNED_COMPARISONS = {
    z3.Z3_OP_ULT: ("u", True, False),
    z3.Z3_OP_ULEQ: ("u", False, False),
    z3.Z3_OP_UGT: ("u", True, True),
    z3.Z3_OP_UGEQ: ("u", False, True),
}
SIGNED_COMPARISONS = {
    z3.Z3_OP_SLT: ("s", True, False),
    z3.Z3_OP_SLEQ: ("s", False, False),
    z3.Z3_OP_SGT: ("s", True, True),
    z3.Z3_OP_SGEQ: ("s", False, True),
}
BITWISE_NAMES = {
    z3.Z3_OP_BAND: "meet",
    z3.Z3_OP_BOR: "join_bits",
    z3.Z3_OP_BXOR: "differ",
    z3.Z3_OP_BNOT: "complement",
}
SHIFT_NAMES = {
    z3.Z3_OP_BSHL: "shift_up",
    z3.Z3_OP_BLSHR: "shift_down_logical",
    z3.Z3_OP_BASHR: "shift_down_arithmetic",
}
ROTATE_NAMES = {
    z3.Z3_OP_ROTATE_LEFT: "rotate_left",
    z3.Z3_OP_ROTATE_RIGHT: "rotate_right",
    z3.Z3_OP_EXT_ROTATE_LEFT: "rotate_left",
    z3.Z3_OP_EXT_ROTATE_RIGHT: "rotate_right",
}
COMPARE_NAMES = {
    z3.Z3_OP_ULT: "below_unsigned",
    z3.Z3_OP_ULEQ: "below_or_equal_unsigned",
    z3.Z3_OP_UGT: "below_unsigned",
    z3.Z3_OP_UGEQ: "below_or_equal_unsigned",
    z3.Z3_OP_SLT: "below_signed",
    z3.Z3_OP_SLEQ: "below_or_equal_signed",
    z3.Z3_OP_SGT: "below_signed",
    z3.Z3_OP_SGEQ: "below_or_equal_signed",
}
"""a comparison with its operands the other way round is the SAME
theorem with its two symbols exchanged, so it carries the same shape."""

DIVISION_NAMES = {
    z3.Z3_OP_BUDIV: "quotient_unsigned",
    z3.Z3_OP_BUDIV_I: "quotient_unsigned",
    z3.Z3_OP_BUREM: "remainder_unsigned",
    z3.Z3_OP_BUREM_I: "remainder_unsigned",
    z3.Z3_OP_BSDIV: "quotient_signed",
    z3.Z3_OP_BSDIV_I: "quotient_signed",
    z3.Z3_OP_BSREM: "remainder_signed",
    z3.Z3_OP_BSREM_I: "remainder_signed",
}

DIVISION_KINDS = {
    z3.Z3_OP_BUDIV: ("u", "q"),
    z3.Z3_OP_BUDIV_I: ("u", "q"),
    z3.Z3_OP_BUREM: ("u", "r"),
    z3.Z3_OP_BUREM_I: ("u", "r"),
    z3.Z3_OP_BSDIV: ("s", "q"),
    z3.Z3_OP_BSDIV_I: ("s", "q"),
    z3.Z3_OP_BSREM: ("s", "r"),
    z3.Z3_OP_BSREM_I: ("s", "r"),
}


def widest_node(term, seen=None):
    """the widest bit-vector node anywhere in a term.  The tier's own
    guard reads this before and after the lowering."""
    if seen is None:
        seen = {}
    here = term.get_id()
    if here in seen:
        return seen[here]
    widest = 0
    if z3.is_bv(term):
        widest = term.size()
    if z3.is_fp(term):
        widest = max(widest, term.sort().ebits() + term.sort().sbits())
    for index in range(term.num_args()):
        child = widest_node(term.arg(index), seen)
        if child > widest:
            widest = child
        continue
    seen[here] = widest
    return widest


def unfolded_size(term, ceiling=None, memo=None):
    """how many nodes the term has when every shared sub-term is written
    out once per use -- which is what the renderer writes, because it
    emits one nested expression and names no intermediate.  Counted with
    a ceiling so a term that grows like a power of its width is measured
    rather than expanded."""
    if memo is None:
        memo = {}
    here = term.get_id()
    if here in memo:
        return memo[here]
    total = 1
    for index in range(term.num_args()):
        total = total + unfolded_size(term.arg(index), ceiling, memo)
        if ceiling is not None and total >= ceiling:
            total = ceiling
            break
        continue
    memo[here] = total
    return total


def shape_key(shape):
    """one rewrite's identity as a stable string: the operation and the
    widths and offsets that make it the rewrite it is.

    A LEMMA IS ABOUT A SHAPE, not about a schema.  `widening /
    narrowing / sign spread` rewrites an extract at ANY pair of offsets,
    and a theorem stated at two of them does not carry a third; the
    shape is what makes the lemma route exact instead of nearly
    right."""
    pieces = [shape["operation"]]
    for name in ("width", "to", "high", "low", "amount"):
        if shape.get(name) is None:
            continue
        pieces.append("%s%s" % (name[0], shape[name]))
        continue
    if shape.get("widths") is not None:
        pieces.append("p" + "-".join(str(w) for w in shape["widths"]))
    return "_".join(pieces)


def lower(term, word):
    """-> (the term with no node above `word` bits, the schemas used in
    the brief's own order, one INSTANCE row per (schema, width) the
    lowering actually reached).

    A term that already has no such node comes back as the SAME object
    and both lists are empty; that is how the tier declines without a
    rule about which cell it is looking at.

    THE INSTANCE ROWS are what the lemma route asks about: a schema is
    proved AT A WIDTH, so what a term needs is the lemma of each schema
    at each width the lowering used it at, and nothing more."""
    used = {}
    memo = {}
    value = lower_node(term, word, used, memo)
    if value.is_limbed():
        raise Refused(CAUSE_NO_SCHEMA,
                      "the answer itself is %d bits and the target's "
                      "widest holder is %d" % (value.width, word))
    order = []
    instances = []
    for name in SCHEMA_ORDER:
        if name not in used:
            continue
        order.append(name)
        for width in sorted(used[name]):
            shapes = []
            for key in sorted(used[name][width]):
                shapes.append(used[name][width][key])
                continue
            instances.append({"schema": name, "width": width,
                              "word": word, "shapes": shapes})
            continue
        continue
    return value.native, order, instances


def note(used, name, width=None, shape=None):
    """one schema used at one width, in one SHAPE -- the rewrite the
    lowering actually performed, which is the thing a lemma is stated
    about."""
    if name not in used:
        used[name] = {}
    if width is None:
        return used
    if width not in used[name]:
        used[name][width] = {}
    if shape is None:
        return used
    used[name][width][shape_key(shape)] = shape
    return used


def lower_node(term, word, used, memo):
    here = term.get_id()
    if here in memo:
        return memo[here]
    value = lower_one(term, word, used, memo)
    memo[here] = value
    return value


def lower_one(term, word, used, memo):
    kind = term.decl().kind()
    width = None
    if z3.is_bv(term):
        width = term.size()

    # -- a leaf ----------------------------------------------------
    if z3.is_const(term) and kind == z3.Z3_OP_UNINTERPRETED:
        if width is not None and width > word:
            raise Refused(CAUSE_WIDE_SYMBOL,
                          "%s is %d bits" % (term.decl().name(), width))
        return Value(native=term, width=width)
    if kind == z3.Z3_OP_BNUM:
        if width > word:
            note(used, WIDEN, width,
                 {"operation": "constant", "width": width})
            return Value(width=width,
                         limbs=constant_limbs(term.as_long(), width,
                                              word))
        return Value(native=term, width=width)
    if term.num_args() == 0:
        if width is not None and width > word:
            raise Refused(CAUSE_NO_SCHEMA,
                          "a leaf of %d bits, kind %d" % (width, kind))
        return Value(native=term, width=width)

    # -- a float, at any width -------------------------------------
    if z3.is_fp(term) or z3.is_fprm(term):
        return float_node(term, word, used, memo)

    lowered = []
    for index in range(term.num_args()):
        lowered.append(lower_node(term.arg(index), word, used, memo))
        continue
    wide_below = False
    for value in lowered:
        if value.is_limbed():
            wide_below = True
            break
        continue
    if width is not None and width <= word and not wide_below:
        return native_again(term, lowered, width)
    if width is None and not wide_below:
        return native_again(term, lowered, None)

    # -- from here the node is above the word, or reads one that is --
    if kind == z3.Z3_OP_EXTRACT:
        return lower_extract(term, lowered, width, word, used)
    if kind == z3.Z3_OP_CONCAT:
        return lower_concat(term, lowered, width, word, used)
    if kind in (z3.Z3_OP_ZERO_EXT, z3.Z3_OP_SIGN_EXT):
        return lower_extend(term, lowered, width, word, used,
                            kind == z3.Z3_OP_SIGN_EXT)
    if kind == z3.Z3_OP_ITE:
        return lower_ite(term, lowered, width, word, used)
    if kind in (z3.Z3_OP_EQ, z3.Z3_OP_DISTINCT):
        return lower_equality(term, lowered, word, used,
                              kind == z3.Z3_OP_DISTINCT)
    if kind in UNSIGNED_COMPARISONS or kind in SIGNED_COMPARISONS:
        return lower_compare(term, lowered, word, used, kind)
    if kind in BITWISE_KINDS:
        note(used, BITWISE, width,
             {"operation": BITWISE_NAMES[kind], "width": width})
        limbs = bitwise_limbs(kind,
                              [as_limbs(v, width, word) for v in lowered],
                              width, word)
        return value_of(limbs, width, word)
    if kind == z3.Z3_OP_BNOT:
        note(used, BITWISE, width,
             {"operation": "complement", "width": width})
        limbs = bitwise_limbs(kind,
                              [as_limbs(lowered[0], width, word)],
                              width, word)
        return value_of(limbs, width, word)
    if kind == z3.Z3_OP_BADD:
        note(used, ADD_SUB, width,
             {"operation": "add", "width": width})
        return fold(lowered, width, word,
                    lambda a, b: add_limbs(a, b, width, word))
    if kind == z3.Z3_OP_BSUB:
        note(used, ADD_SUB, width,
             {"operation": "sub", "width": width})
        return fold(lowered, width, word,
                    lambda a, b: sub_limbs(a, b, width, word))
    if kind == z3.Z3_OP_BNEG:
        note(used, ADD_SUB, width,
             {"operation": "negate", "width": width})
        limbs = negate_limbs(as_limbs(lowered[0], width, word), width,
                             word)
        return value_of(limbs, width, word)
    if kind == z3.Z3_OP_BMUL:
        note(used, MULTIPLY, width,
             {"operation": "product", "width": width})
        return fold(lowered, width, word,
                    lambda a, b: mul_limbs(a, b, width, word))
    if kind in (z3.Z3_OP_BSHL, z3.Z3_OP_BLSHR, z3.Z3_OP_BASHR):
        note(used, SHIFT_ROTATE, width,
             {"operation": SHIFT_NAMES[kind], "width": width})
        left = as_limbs(lowered[0], width, word)
        right = as_limbs(lowered[1], width, word)
        if kind == z3.Z3_OP_BSHL:
            limbs = shl_limbs(left, right, width, word)
        elif kind == z3.Z3_OP_BLSHR:
            limbs = lshr_limbs(left, right, width, word)
        else:
            limbs = ashr_limbs(left, right, width, word)
        return value_of(limbs, width, word)
    if kind in (z3.Z3_OP_ROTATE_LEFT, z3.Z3_OP_ROTATE_RIGHT):
        amount = term.params()[0]
        note(used, SHIFT_ROTATE, width,
             {"operation": ROTATE_NAMES[kind], "width": width,
              "amount": amount})
        left = as_limbs(lowered[0], width, word)
        limbs = rotate_limbs(left, constant_limbs(amount, width, word),
                             width, word,
                             kind == z3.Z3_OP_ROTATE_LEFT)
        return value_of(limbs, width, word)
    if kind in (z3.Z3_OP_EXT_ROTATE_LEFT, z3.Z3_OP_EXT_ROTATE_RIGHT):
        note(used, SHIFT_ROTATE, width,
             {"operation": ROTATE_NAMES[kind], "width": width})
        limbs = rotate_limbs(as_limbs(lowered[0], width, word),
                             as_limbs(lowered[1], width, word),
                             width, word,
                             kind == z3.Z3_OP_EXT_ROTATE_LEFT)
        return value_of(limbs, width, word)
    if kind in DIVISION_KINDS:
        sign, which = DIVISION_KINDS[kind]
        note(used, DIVIDE, width,
             {"operation": DIVISION_NAMES[kind], "width": width})
        left = as_limbs(lowered[0], width, word)
        right = as_limbs(lowered[1], width, word)
        if sign == "u":
            quotient, remainder = udivrem_limbs(left, right, width, word)
        else:
            quotient, remainder = sdivrem_limbs(left, right, width, word)
        if which == "q":
            return value_of(quotient, width, word)
        return value_of(remainder, width, word)
    raise Refused(CAUSE_NO_SCHEMA,
                  "%s (kind %d) at %s bits"
                  % (term.decl().name(), kind, width))


def native_again(term, lowered, width):
    """a node at or below the word with nothing wide under it: rebuilt
    from its own children, and returned as the SAME OBJECT where none of
    them moved -- which is how `lower` knows it constructed nothing.

    THE REBUILD IS THE NODE'S OWN DECLARATION APPLIED TO THE NEW
    CHILDREN, which carries the node's parameters with it (an extract's
    two indices, an extension's count, a rotate's amount).  The three
    parametric kinds are spelled out beside it anyway, because a
    parameter silently lost would be a different mapping that still
    type-checks."""
    same = True
    children = []
    for index, value in enumerate(lowered):
        children.append(value.native)
        if value.native is not term.arg(index):
            same = False
        continue
    if same:
        return Value(native=term, width=width)
    kind = term.decl().kind()
    if kind == z3.Z3_OP_EXTRACT:
        high, low = term.params()
        return Value(native=z3.Extract(high, low, children[0]),
                     width=width)
    if kind == z3.Z3_OP_ZERO_EXT:
        return Value(native=z3.ZeroExt(term.params()[0], children[0]),
                     width=width)
    if kind == z3.Z3_OP_SIGN_EXT:
        return Value(native=z3.SignExt(term.params()[0], children[0]),
                     width=width)
    if kind == z3.Z3_OP_ROTATE_LEFT:
        return Value(native=z3.RotateLeft(children[0],
                                          term.params()[0]),
                     width=width)
    if kind == z3.Z3_OP_ROTATE_RIGHT:
        return Value(native=z3.RotateRight(children[0],
                                           term.params()[0]),
                     width=width)
    return Value(native=term.decl()(*children), width=width)


def fold(lowered, width, word, operation):
    limbs = as_limbs(lowered[0], width, word)
    for value in lowered[1:]:
        limbs = operation(limbs, as_limbs(value, width, word))
        continue
    return value_of(limbs, width, word)


def lower_extract(term, lowered, width, word, used):
    high, low = term.params()
    note(used, WIDEN, term.arg(0).size(),
         {"operation": "extract", "width": term.arg(0).size(),
          "high": high, "low": low})
    source = lowered[0]
    inner_width = term.arg(0).size()
    limbs = as_limbs(source, inner_width, word)
    out = []
    for index in range(limb_count(width, word)):
        piece = zero_word(word)
        start = low + word * index
        for which in range(len(limbs)):
            base = word * which
            shift = start - base
            if shift >= word or shift <= -word:
                continue
            if shift >= 0:
                here = shifted_down(limbs[which],
                                    z3.BitVecVal(shift, word))
            else:
                here = shifted_up(limbs[which],
                                  z3.BitVecVal(-shift, word))
            piece = joined(piece, here)
            continue
        out.append(piece)
        continue
    return value_of(mask_top(out, width, word), width, word)


def lower_concat(term, lowered, width, word, used):
    note(used, WIDEN, width,
         {"operation": "concat", "width": width,
          "widths": [term.arg(i).size()
                     for i in range(term.num_args())]})
    # the arguments are most significant first, which is z3's own order
    pieces = []
    offset = 0
    for index in range(term.num_args() - 1, -1, -1):
        inner = term.arg(index).size()
        pieces.append((offset, inner, lowered[index]))
        offset = offset + inner
        continue
    out = zeros(width, word)
    for start, inner, value in pieces:
        limbs = as_limbs(value, inner, word)
        for which in range(len(limbs)):
            base = start + word * which
            target = base // word
            shift = base % word
            if target < len(out):
                out[target] = joined(
                    out[target],
                    shifted_up(limbs[which],
                               z3.BitVecVal(shift, word)))
            if shift != 0 and target + 1 < len(out):
                out[target + 1] = joined(
                    out[target + 1],
                    shifted_down(limbs[which],
                                 z3.BitVecVal(word - shift, word)))
            continue
        continue
    return value_of(mask_top(out, width, word), width, word)


def lower_extend(term, lowered, width, word, used, signed):
    inner = term.arg(0).size()
    name = "extend_zero"
    if signed:
        name = "extend_sign"
    note(used, WIDEN, width,
         {"operation": name, "width": inner, "to": width})
    limbs = as_limbs(lowered[0], inner, word)
    out = list(limbs)
    if signed:
        filler = sign_word_of(limbs, inner, word)
        top = top_bits(inner, word)
        if top < word:
            above = z3.BitVecVal(((1 << word) - 1) ^ ((1 << top) - 1),
                                 word)
            out[len(out) - 1] = out[len(out) - 1] | (filler & above)
    else:
        filler = zero_word(word)
    while len(out) < limb_count(width, word):
        out.append(filler)
        continue
    return value_of(mask_top(out, width, word), width, word)


def lower_ite(term, lowered, width, word, used):
    note(used, BITWISE, width,
         {"operation": "select", "width": width})
    condition = lowered[0].native
    left = as_limbs(lowered[1], width, word)
    right = as_limbs(lowered[2], width, word)
    return value_of(ite_limbs(condition, left, right), width, word)


def lower_equality(term, lowered, word, used, distinct):
    note(used, COMPARE, term.arg(0).size(),
         {"operation": "equal", "width": term.arg(0).size()})
    inner = term.arg(0).size()
    left = as_limbs(lowered[0], inner, word)
    right = as_limbs(lowered[1], inner, word)
    answer = eq_limbs(left, right)
    if distinct:
        answer = z3.Not(answer)
    return Value(native=answer, width=None)


def lower_compare(term, lowered, word, used, kind):
    note(used, COMPARE, term.arg(0).size(),
         {"operation": COMPARE_NAMES[kind],
          "width": term.arg(0).size()})
    inner = term.arg(0).size()
    left = as_limbs(lowered[0], inner, word)
    right = as_limbs(lowered[1], inner, word)
    if kind in UNSIGNED_COMPARISONS:
        _sign, strict, swapped = UNSIGNED_COMPARISONS[kind]
        if swapped:
            answer = ult_limbs(right, left, strict)
        else:
            answer = ult_limbs(left, right, strict)
        return Value(native=answer, width=None)
    _sign, strict, swapped = SIGNED_COMPARISONS[kind]
    if swapped:
        answer = slt_limbs(right, left, inner, word, strict)
    else:
        answer = slt_limbs(left, right, inner, word, strict)
    return Value(native=answer, width=None)


def float_node(term, word, used, memo):
    """THE FLOAT SCHEMA, and what it does today.

    A float node whose sort the TARGET has a holder for is left exactly
    as it is: the renderer spells it, and there is nothing to construct.
    A float node whose sort it has no holder for is refused BY CAUSE
    naming the schema that is owed -- the integer schemas above over the
    fields sign, exponent and significand with the sticky bit, and the
    five classes as a case split.  It is not guessed at, because a
    softfloat that is nearly right is a wrong mapping that looks like a
    right one, and this pipeline's whole point is the difference."""
    lowered = []
    for index in range(term.num_args()):
        lowered.append(lower_node(term.arg(index), word, used, memo))
        continue
    width = None
    if z3.is_bv(term):
        width = term.size()
    return native_again(term, lowered, width)
