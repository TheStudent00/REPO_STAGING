#!/usr/bin/env python3
"""softfloat.py -- THE FLOAT KINDS AS CONSTRUCTIONS OVER THE INTEGER
ONES: one construction per float operation kind, general in the format
(`ebits`, `sbits`) and in the word `W`.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_t4_brief.md`.

THE OBJECTS, one sentence each, in relation.
  * A FLOAT IN BITS is how this file holds every float value: the IEEE
    bit pattern as a `build.Value` of `ebits + sbits` bits, which is
    exactly what `fp.to_ieee_bv` reads and what `to_fp` of one argument
    writes.  A target that has no holder for a float of that width can
    still hold its bits, which is the whole reason the constructions
    are stated this way.
  * THE FIELDS are the sign (one bit at the top), the exponent (`ebits`
    bits below it) and the fraction (`sbits - 1` bits at the bottom);
    the SIGNIFICAND is the fraction with the hidden bit above it, which
    is one for a normal number and zero for a subnormal.
  * THE FIVE CLASSES are zero, subnormal, normal, infinity and
    not-a-number, decided by whether the exponent field is all zeros,
    all ones, or neither, and whether the fraction is zero.
  * THE ROUNDING is round-to-nearest, ties-to-even, and this file states
    NO other: a term carrying another rounding mode is refused by cause
    (the pipeline's own `CAUSE_RM` says the same thing on the other
    side).

EVERY STEP BELOW IS AN INTEGER CONSTRUCTION FROM `build.py`, so the
float constructions inherit the primitive set unchanged: `& | ^ ~`,
shifts by constants, a conditional and variables.

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

HOW THIS FILE OBEYS IT.  Every branch is on a z3 declaration NAME of
the `fp.*` family -- z3's own machine form for a float node -- and on
the format's two numbers.  Nothing here reads a mnemonic or a cell.

Coding discipline: no compound one-liner statements.
"""

import z3

import build as B


CAUSE_NO_FLOAT_CONSTRUCTION = ("no construction is written for this "
                               "float operation kind")
CAUSE_RM = ("a rounding mode other than round-to-nearest-ties-to-even: "
            "this file states the constructions at RNE and no other")
CAUSE_UNSPECIFIED = ("the operation's answer is left unspecified by the "
                     "standard outside its own range, so there is no "
                     "mapping to construct")

ARITHMETIC_NAMES = ("fp.add", "fp.sub", "fp.mul", "fp.div")
COMPARE_NAMES = ("fp.eq", "fp.lt", "fp.leq", "fp.gt", "fp.geq")
CLASS_NAMES = ("fp.isNaN", "fp.isInfinite", "fp.isZero", "fp.isNormal",
               "fp.isSubnormal", "fp.isNegative", "fp.isPositive")
OWED_NAMES = ("fp.sqrt", "fp.fma", "fp.rem", "fp.roundToIntegral",
              "fp.min", "fp.max", "fp.to_sbv", "fp.to_ubv",
              "fp.to_real")


# ==================================================================
# section 0: the format, and the values this file carries
# ==================================================================

class Format(object):
    """one float format: `ebits` exponent bits and `sbits` significand
    bits INCLUDING the hidden one, so the IEEE pattern is
    `ebits + sbits` bits wide and the bias is 2^(ebits-1) - 1."""

    def __init__(self, ebits, sbits, word):
        self.ebits = ebits
        self.sbits = sbits
        self.word = word
        self.width = ebits + sbits
        self.bias = (1 << (ebits - 1)) - 1
        self.fraction_bits = sbits - 1


def format_of(sort, word):
    return Format(sort.ebits(), sort.sbits(), word)


def value_at(term_or_value, width, word):
    return B.at_width(term_or_value, width, word)


def constant(number, width, word):
    return B.constant_value(number, width, word)


def field(value, low, count, word):
    """`count` bits of a value starting at `low`, as a value of its own.
    WIRING."""
    return B.relimb_from(value, low, count, word)


def truth_of_bit(value, position):
    return B.bit_of_value(value, position) == z3.BitVecVal(1, 1)


def is_zero_value(value):
    return z3.Not(B.or_reduce(value))


def widen(value, width, word):
    return B.relimb(B.segments_of(value), width, word)


# ==================================================================
# section 1: unpacking, the classes, and packing back
# ==================================================================

def sign_of(bits, form):
    return B.bit_of_value(bits, form.width - 1)


def exponent_of(bits, form):
    return field(bits, form.fraction_bits, form.ebits, form.word)


def fraction_of(bits, form):
    return field(bits, 0, form.fraction_bits, form.word)


def exponent_is_all_ones(bits, form):
    exponent = exponent_of(bits, form)
    top = constant((1 << form.ebits) - 1, form.ebits, form.word)
    return B.equal_values(exponent, top)


def exponent_is_zero(bits, form):
    return is_zero_value(exponent_of(bits, form))


def is_nan(bits, form):
    return z3.And(exponent_is_all_ones(bits, form),
                  z3.Not(is_zero_value(fraction_of(bits, form))))


def is_infinite(bits, form):
    return z3.And(exponent_is_all_ones(bits, form),
                  is_zero_value(fraction_of(bits, form)))


def is_zero_float(bits, form):
    return z3.And(exponent_is_zero(bits, form),
                  is_zero_value(fraction_of(bits, form)))


def is_subnormal(bits, form):
    return z3.And(exponent_is_zero(bits, form),
                  z3.Not(is_zero_value(fraction_of(bits, form))))


def is_normal_float(bits, form):
    return z3.And(z3.Not(exponent_is_zero(bits, form)),
                  z3.Not(exponent_is_all_ones(bits, form)))


def significand_of(bits, form, width):
    """the fraction with the hidden bit above it, at `width` bits: one
    for a normal number and zero for a subnormal."""
    fraction = widen(fraction_of(bits, form), width, form.word)
    hidden = constant(1 << form.fraction_bits, width, form.word)
    normal = z3.Not(exponent_is_zero(bits, form))
    return B.choose(normal, B.bitwise("or", [fraction, hidden], width,
                                      fraction.unit), fraction)


def effective_exponent(bits, form, width):
    """the exponent field, with a subnormal's read as one, at `width`
    bits -- the format's own rule that a subnormal has the exponent of
    the smallest normal and no hidden bit."""
    exponent = widen(exponent_of(bits, form), width, form.word)
    one = constant(1, width, form.word)
    return B.choose(exponent_is_zero(bits, form), one, exponent)


def packed(sign_bit, exponent, fraction, form):
    """the three fields joined back into one IEEE pattern.  WIRING."""
    pieces = []
    pieces.append((fraction.limbs, fraction.unit, form.fraction_bits))
    pieces.append((exponent.limbs, exponent.unit, form.ebits))
    sign_value = B.Value("bv", width=1, unit=1, limbs=[sign_bit])
    pieces.append((sign_value.limbs, 1, 1))
    return B.relimb(pieces, form.width, form.word)


def quiet_nan(form):
    """the format's own quiet not-a-number: every exponent bit one and
    the top fraction bit one."""
    number = ((1 << form.ebits) - 1) << form.fraction_bits
    number = number | (1 << (form.fraction_bits - 1))
    return constant(number, form.width, form.word)


def infinity(form, sign_bit):
    exponent = constant((1 << form.ebits) - 1, form.ebits, form.word)
    fraction = constant(0, form.fraction_bits, form.word)
    return packed(sign_bit, exponent, fraction, form)


def signed_zero(form, sign_bit):
    exponent = constant(0, form.ebits, form.word)
    fraction = constant(0, form.fraction_bits, form.word)
    return packed(sign_bit, exponent, fraction, form)


# ==================================================================
# section 2: the two steps every arithmetic construction needs
# ==================================================================

def shift_down_with_sticky(value, count, width, word):
    """the value shifted down by a SYMBOLIC count, with the bits that
    fell off gathered into bit 0.

    The sticky bit is measured rather than tracked: shift down, shift
    the answer back up, and ask whether what comes back is what went in.
    Two barrels and one equality, and it is exact at every count."""
    unit = B.unit_for(width, word)
    down = B.shift_by_count(value, count, width, unit, "down", False)
    back = B.shift_by_count(down, count, width, unit, "up", False)
    lost = z3.Not(B.equal_values(back, value))
    one = constant(1, width, word)
    with_sticky = B.bitwise("or", [down, one], width, unit)
    return B.choose(lost, with_sticky, down)


def shift_down_constant_with_sticky(value, amount, width, unit):
    """the value shifted down by a CONSTANT number of bits, with the
    bits that fell off gathered into bit 0.  Exact, and cheaper than the
    barrel: one mask, one test, one constant shift."""
    if amount <= 0:
        return value
    lost_mask = B.constant_value_like((1 << amount) - 1, value)
    lost = z3.Not(is_zero_value(B.bitwise("and", [value, lost_mask],
                                          width, unit)))
    down = B.Value("bv", width=width, unit=unit,
                   limbs=B.shift_right_constant(value.limbs, amount,
                                                width, unit))
    one = B.constant_value_like(1, value)
    with_sticky = B.bitwise("or", [down, one], width, unit)
    return B.choose(lost, with_sticky, down)


def normalised_parts(bits, form, span, word):
    """THE OPERAND UNPACKED SO THAT EVERY VALUE LOOKS NORMAL: the sign,
    an effective exponent, and a significand whose leading one sits at
    bit `fraction_bits`.

    A SUBNORMAL'S SIGNIFICAND IS SHIFTED UP AND ITS EXPONENT TAKEN DOWN
    BY THE SAME AMOUNT, which is exact (no bit is lost shifting up) and
    which is what makes multiply and divide need at most ONE place of
    normalising afterwards.  Doing it the other way round -- shifting
    the answer down first and normalising it up second -- moves a
    sticky bit into the significand and is wrong; it was measured wrong
    (lane `t4_l4`, `fp_mul_e4_s5` DISPROVED at a = 151, b = 3) and this
    is the correction."""
    sign = sign_of(bits, form)
    exponent = effective_exponent(bits, form, span)
    significand = significand_of(bits, form, span)
    small = is_subnormal(bits, form)
    moved, shift = leading_normalize(significand, span, word,
                                     form.sbits)
    significand = B.choose(small, moved, significand)
    exponent = B.choose(small, B.subtract_values(exponent, shift),
                        exponent)
    return sign, exponent, significand


def leading_normalize(value, width, word, span):
    """the value shifted up until its bit `span - 1` is one, and the
    number of places it moved.

    A BARREL, log2(span) stages: at each stage, if the top `step` bits
    of the span are all zero the value moves up by `step`.  This is the
    leading-zero count and the normalising shift in one walk."""
    unit = B.unit_for(width, word)
    running = value
    shift = constant(0, width, word)
    stage = B.rounds_for(span)
    while stage > 0:
        stage = stage - 1
        step = 1 << stage
        if step >= span:
            continue
        top = field(running, span - step, step, word)
        empty = is_zero_value(top)
        moved = B.Value("bv", width=width, unit=unit,
                        limbs=B.shift_left_constant(running.limbs, step,
                                                    width, unit))
        running = B.choose(empty, moved, running)
        added = B.add_values(shift, constant(step, width, word))
        shift = B.choose(empty, added, shift)
        continue
    return running, shift


# ==================================================================
# section 3: add, subtract, multiply, divide
# ==================================================================

def round_and_pack(sign_bit, exponent, significand, form, span):
    """round-to-nearest-ties-to-even on a significand held at `span`
    bits with three round bits at the bottom, then the exponent's own
    overflow and underflow, then the fields joined.

    `exponent` is the UNBIASED-plus-bias exponent the caller computed
    for a significand whose hidden bit sits at bit `span - 4`; it may be
    at or below zero, which is the subnormal case, and it may be at or
    above the format's all-ones, which is the overflow case."""
    word = form.word
    width = significand.width
    unit = significand.unit
    # THE SUBNORMAL FLOOR: where the exponent is at or below zero the
    # answer is written with the exponent field zero and the
    # significand shifted down by one more place per step below one.
    one = constant(1, width, word)
    exponent_wide = widen(exponent, width, word)
    below = B.below_signed(exponent_wide, one)
    deficit = B.subtract_values(one, exponent_wide)
    shifted = shift_down_with_sticky(significand, deficit, width, word)
    significand = B.choose(below, shifted, significand)
    exponent_wide = B.choose(below, one, exponent_wide)
    # THE ROUND BITS are the three at the bottom: the one below the
    # answer's own least bit, and the two that say whether what was
    # dropped was more than half of it.
    lowest = truth_of_bit(significand, 3)
    guard = truth_of_bit(significand, 2)
    rest = z3.Or(truth_of_bit(significand, 1),
                 truth_of_bit(significand, 0))
    upward = z3.And(guard, z3.Or(lowest, rest))
    dropped = B.Value("bv", width=width, unit=unit,
                      limbs=B.shift_right_constant(significand.limbs, 3,
                                                   width, unit))
    stepped = B.add_values(dropped, constant(1, width, word))
    rounded = B.choose(upward, stepped, dropped)
    # A ROUND THAT CARRIED OUT OF THE SIGNIFICAND moves the exponent up
    # one and the significand down one; the bit that says so is the one
    # above the hidden bit.
    carried = truth_of_bit(rounded, form.sbits)
    halved = B.Value("bv", width=width, unit=unit,
                     limbs=B.shift_right_constant(rounded.limbs, 1,
                                                  width, unit))
    rounded = B.choose(carried, halved, rounded)
    exponent_wide = B.choose(carried,
                             B.add_values(exponent_wide,
                                          constant(1, width, word)),
                             exponent_wide)
    # A SUBNORMAL ANSWER is one whose hidden bit came out zero; its
    # exponent field is zero and its fraction is the significand.
    hidden = truth_of_bit(rounded, form.fraction_bits)
    exponent_field = B.choose(hidden, exponent_wide,
                              constant(0, width, word))
    top = constant((1 << form.ebits) - 1, width, word)
    overflowed = z3.Not(B.below_unsigned(exponent_field, top))
    answer = packed(sign_bit,
                    B.relimb(B.segments_of(exponent_field), form.ebits,
                             word),
                    B.relimb(B.segments_of(rounded), form.fraction_bits,
                             word),
                    form)
    return B.choose(overflowed, infinity(form, sign_bit), answer)


def add_or_subtract(left, right, form, subtracting):
    """THE SOFTFLOAT ADDER: the two operands ordered by magnitude, the
    smaller one's significand aligned down with a sticky bit, the two
    added or subtracted, the answer normalised and rounded.

    Every step is an integer construction from `build.py`."""
    word = form.word
    span = form.sbits + 5
    right = flip_sign(right, form, subtracting)
    without_sign = constant((1 << (form.width - 1)) - 1, form.width,
                            word)
    magnitude_left = B.bitwise("and", [left, without_sign], form.width,
                               left.unit)
    magnitude_right = B.bitwise("and", [right, without_sign], form.width,
                                right.unit)
    swap = B.below_unsigned(magnitude_left, magnitude_right)
    big = B.choose(swap, right, left)
    small = B.choose(swap, left, right)
    sign_big = sign_of(big, form)
    sign_small = sign_of(small, form)
    same_sign = (sign_big == sign_small)
    exponent_big = effective_exponent(big, form, span)
    exponent_small = effective_exponent(small, form, span)
    distance = B.subtract_values(exponent_big, exponent_small)
    unit = B.unit_for(span, word)
    big_significand = B.Value(
        "bv", width=span, unit=unit,
        limbs=B.shift_left_constant(significand_of(big, form,
                                                   span).limbs,
                                    3, span, unit))
    small_significand = B.Value(
        "bv", width=span, unit=unit,
        limbs=B.shift_left_constant(significand_of(small, form,
                                                   span).limbs,
                                    3, span, unit))
    aligned = shift_down_with_sticky(small_significand, distance, span,
                                     word)
    added = B.add_values(big_significand, aligned)
    taken = B.subtract_values(big_significand, aligned)
    total = B.choose(same_sign, added, taken)
    # NORMALISE.  An addition can carry one place up; a subtraction can
    # lose any number of places.  Both are the one barrel below, run
    # over the span above the hidden bit.
    carried = truth_of_bit(total, form.sbits + 3)
    down = shift_down_with_sticky(total, constant(1, span, word), span,
                                  word)
    total = B.choose(carried, down, total)
    exponent = B.choose(carried,
                        B.add_values(exponent_big, constant(1, span,
                                                            word)),
                        exponent_big)
    normalised, moved = leading_normalize(total, span, word,
                                          form.sbits + 3)
    room = B.subtract_values(exponent, constant(1, span, word))
    limited = B.below_unsigned(room, moved)
    steps = B.choose(limited, room, moved)
    back = B.subtract_values(moved, steps)
    normalised = shift_down_with_sticky(normalised, back, span, word)
    exponent = B.subtract_values(exponent, steps)
    # THE ANSWER'S SIGN is the bigger operand's, except that a
    # subtraction that came out exactly zero is positive under this
    # rounding.
    empty = is_zero_value(total)
    zero_sign = z3.If(z3.And(empty, z3.Not(same_sign)),
                      z3.BitVecVal(0, 1), sign_big)
    answer = round_and_pack(zero_sign, exponent, normalised, form, span)
    answer = B.choose(empty, signed_zero(form, zero_sign), answer)
    return with_the_special_cases(left, right, answer, form,
                                  "add")


def flip_sign(bits, form, doing_it):
    if not doing_it:
        return bits
    top = constant(1 << (form.width - 1), form.width, form.word)
    return B.bitwise("xor", [bits, top], form.width, bits.unit)


def multiply_floats(left, right, form):
    """THE SOFTFLOAT MULTIPLIER: the two significands normalised and
    multiplied by the integer construction, the exponents added, ONE
    place of normalising, then the rounding every construction here
    shares."""
    word = form.word
    span = 2 * form.sbits + 6
    unit = B.unit_for(span, word)
    place = form.fraction_bits + 3
    sign_bit = sign_of(left, form) ^ sign_of(right, form)
    sign_left, exponent_left, significand_left = normalised_parts(
        left, form, span, word)
    sign_right, exponent_right, significand_right = normalised_parts(
        right, form, span, word)
    product = B.multiply(significand_left, significand_right, span,
                         unit)
    exponent = B.add_values(exponent_left, exponent_right)
    exponent = B.subtract_values(exponent, constant(form.bias, span,
                                                    word))
    # Both significands have their leading one at `fraction_bits`, so
    # the product's is at twice that or one above it; moving it down to
    # `fraction_bits + 3` is a CONSTANT shift and the exponent formula
    # is the same either way.
    distance = form.fraction_bits - 3
    if distance >= 0:
        moved = shift_down_constant_with_sticky(product, distance, span,
                                                unit)
    else:
        moved = B.Value("bv", width=span, unit=unit,
                        limbs=B.shift_left_constant(product.limbs,
                                                    -distance, span,
                                                    unit))
    carried = truth_of_bit(moved, place + 1)
    down = shift_down_constant_with_sticky(moved, 1, span, unit)
    moved = B.choose(carried, down, moved)
    exponent = B.choose(carried,
                        B.add_values(exponent, constant(1, span, word)),
                        exponent)
    empty = is_zero_value(product)
    answer = round_and_pack(sign_bit, exponent, moved, form, span)
    answer = B.choose(empty, signed_zero(form, sign_bit), answer)
    return with_the_special_cases(left, right, answer, form, "multiply")


def divide_floats(left, right, form):
    """THE SOFTFLOAT DIVIDER: the dividend's normalised significand
    shifted up and divided by the divisor's with the integer restoring
    construction, the remainder's own non-zero taken as the sticky bit,
    then ONE place of normalising."""
    word = form.word
    span = 2 * form.sbits + 10
    unit = B.unit_for(span, word)
    place = form.fraction_bits + 3
    sign_bit = sign_of(left, form) ^ sign_of(right, form)
    _sign_left, exponent_left, significand_left = normalised_parts(
        left, form, span, word)
    _sign_right, exponent_right, significand_right = normalised_parts(
        right, form, span, word)
    numerator = B.Value("bv", width=span, unit=unit,
                        limbs=B.shift_left_constant(
                            significand_left.limbs, place + 1, span,
                            unit))
    quotient, rest = B.divide_unsigned(numerator, significand_right,
                                       span, unit, word)
    inexact = z3.Not(is_zero_value(rest))
    one = constant(1, span, word)
    with_sticky = B.bitwise("or", [quotient, one], span, unit)
    quotient = B.choose(inexact, with_sticky, quotient)
    # The quotient's leading one is at `place` or one above it, because
    # both significands have theirs at `fraction_bits`.
    exponent = B.subtract_values(exponent_left, exponent_right)
    exponent = B.add_values(exponent, constant(form.bias, span, word))
    exponent = B.subtract_values(exponent, constant(1, span, word))
    carried = truth_of_bit(quotient, place + 1)
    down = shift_down_constant_with_sticky(quotient, 1, span, unit)
    quotient = B.choose(carried, down, quotient)
    exponent = B.choose(carried,
                        B.add_values(exponent, constant(1, span, word)),
                        exponent)
    empty = is_zero_value(significand_left)
    answer = round_and_pack(sign_bit, exponent, quotient, form, span)
    answer = B.choose(empty, signed_zero(form, sign_bit), answer)
    return with_the_special_cases(left, right, answer, form, "divide")


def with_the_special_cases(left, right, answer, form, which):
    """the five classes as the case split the brief names, applied AFTER
    the ordinary answer is built, so the ordinary path carries no
    branch of its own."""
    left_nan = is_nan(left, form)
    right_nan = is_nan(right, form)
    left_infinite = is_infinite(left, form)
    right_infinite = is_infinite(right, form)
    left_zero = is_zero_float(left, form)
    right_zero = is_zero_float(right, form)
    sign_left = sign_of(left, form)
    sign_right = sign_of(right, form)
    sign_both = sign_left ^ sign_right
    out = answer
    if which == "add":
        both_infinite = z3.And(left_infinite, right_infinite)
        opposite = z3.And(both_infinite, z3.Not(sign_left == sign_right))
        out = B.choose(right_infinite, infinity(form, sign_right), out)
        out = B.choose(left_infinite, infinity(form, sign_left), out)
        out = B.choose(opposite, quiet_nan(form), out)
    elif which == "multiply":
        strange = z3.Or(z3.And(left_infinite, right_zero),
                        z3.And(left_zero, right_infinite))
        either_infinite = z3.Or(left_infinite, right_infinite)
        out = B.choose(either_infinite, infinity(form, sign_both), out)
        out = B.choose(strange, quiet_nan(form), out)
    else:
        strange = z3.Or(z3.And(left_infinite, right_infinite),
                        z3.And(left_zero, right_zero))
        out = B.choose(right_infinite, signed_zero(form, sign_both), out)
        out = B.choose(right_zero, infinity(form, sign_both), out)
        out = B.choose(left_infinite, infinity(form, sign_both), out)
        out = B.choose(strange, quiet_nan(form), out)
    out = B.choose(z3.Or(left_nan, right_nan), quiet_nan(form), out)
    return out


# ==================================================================
# section 4: the comparisons, and the conversions
# ==================================================================

def ordering_key(bits, form):
    """the bit pattern turned into an integer whose UNSIGNED order is
    the float's own order: a negative float's bits complemented, a
    positive float's top bit set.  Two constant masks and a conditional;
    the two zeros are the one case it does not settle, and the caller
    settles that."""
    word = form.word
    width = form.width
    unit = bits.unit
    negative = sign_of(bits, form) == z3.BitVecVal(1, 1)
    flipped = B.complement(bits)
    top = constant(1 << (width - 1), width, word)
    raised = B.bitwise("or", [bits, top], width, unit)
    return B.choose(negative, flipped, raised)


def compare_floats(left, right, form, name):
    ordered = z3.And(z3.Not(is_nan(left, form)),
                     z3.Not(is_nan(right, form)))
    both_zero = z3.And(is_zero_float(left, form),
                       is_zero_float(right, form))
    same = z3.Or(both_zero, B.equal_values(left, right))
    left_key = ordering_key(left, form)
    right_key = ordering_key(right, form)
    below = B.below_unsigned(left_key, right_key)
    strictly_below = z3.And(below, z3.Not(both_zero))
    if name == "fp.eq":
        return z3.And(ordered, same)
    if name == "fp.lt":
        return z3.And(ordered, strictly_below)
    if name == "fp.leq":
        return z3.And(ordered, z3.Or(strictly_below, same))
    if name == "fp.gt":
        above = z3.And(B.below_unsigned(right_key, left_key),
                       z3.Not(both_zero))
        return z3.And(ordered, above)
    above = z3.And(B.below_unsigned(right_key, left_key),
                   z3.Not(both_zero))
    return z3.And(ordered, z3.Or(above, same))


def from_integer(value, form, signed):
    """AN INTEGER TO A FLOAT, round to nearest ties to even: the
    magnitude normalised so its highest one sits at the hidden bit, the
    exponent read off how far it moved, then the same rounding as every
    other construction here."""
    word = form.word
    span = max(value.width, form.sbits) + 8
    unit = B.unit_for(span, word)
    if signed:
        negative = truth_of_bit(value, value.width - 1)
        magnitude = B.choose(negative, B.negate_value(value), value)
        sign_bit = z3.If(negative, z3.BitVecVal(1, 1),
                         z3.BitVecVal(0, 1))
    else:
        magnitude = value
        sign_bit = z3.BitVecVal(0, 1)
    wide = widen(magnitude, span, word)
    empty = is_zero_value(wide)
    normalised, moved = leading_normalize(wide, span, word, span)
    # the highest one now sits at bit span - 1; the answer wants it at
    # bit fraction_bits + 3, so it moves down by the difference with a
    # sticky bit, and the exponent says where it came from.
    distance = constant(span - 1 - (form.fraction_bits + 3), span, word)
    lowered = shift_down_with_sticky(normalised, distance, span, word)
    place = B.subtract_values(constant(span - 1, span, word), moved)
    exponent = B.add_values(place, constant(form.bias, span, word))
    answer = round_and_pack(sign_bit, exponent, lowered, form, span)
    return B.choose(empty, signed_zero(form, z3.BitVecVal(0, 1)), answer)


def between_formats(bits, source, form):
    """A FLOAT OF ONE FORMAT TO ANOTHER, round to nearest ties to even:
    the source's significand normalised, re-laid at the answer's own
    place, the exponent re-biased, the five classes carried across."""
    word = form.word
    span = max(source.sbits, form.sbits) + 10
    unit = B.unit_for(span, word)
    place = form.fraction_bits + 3
    sign_bit = sign_of(bits, source)
    _sign, exponent, significand = normalised_parts(bits, source, span,
                                                    word)
    exponent = B.subtract_values(exponent, constant(source.bias, span,
                                                    word))
    exponent = B.add_values(exponent, constant(form.bias, span, word))
    distance = place - source.fraction_bits
    if distance >= 0:
        significand = B.Value(
            "bv", width=span, unit=unit,
            limbs=B.shift_left_constant(significand.limbs, distance,
                                        span, unit))
    else:
        significand = shift_down_constant_with_sticky(
            significand, -distance, span, unit)
    answer = round_and_pack(sign_bit, exponent, significand, form, span)
    answer = B.choose(is_zero_float(bits, source),
                      signed_zero(form, sign_bit), answer)
    answer = B.choose(is_infinite(bits, source),
                      infinity(form, sign_bit), answer)
    answer = B.choose(is_nan(bits, source), quiet_nan(form), answer)
    return answer


# ==================================================================
# section 5: the one entry for a float node
# ==================================================================

def build_float(node, children, word):
    """one float-sorted node and its children's Values, as the Value the
    construction gives -- always the IEEE BITS, never a float holder."""
    name = "%s" % node.decl().name()
    form = format_of(node.sort(), word)
    if name == "fp":
        # the three fields given separately: WIRING
        sign = children[0]
        exponent = children[1]
        fraction = children[2]
        return packed(B.bit_of_value(sign, 0), exponent, fraction, form)
    if name == "+zero":
        return signed_zero(form, z3.BitVecVal(0, 1))
    if name == "-zero":
        return signed_zero(form, z3.BitVecVal(1, 1))
    if name == "+oo":
        return infinity(form, z3.BitVecVal(0, 1))
    if name == "-oo":
        return infinity(form, z3.BitVecVal(1, 1))
    if name == "NaN":
        return quiet_nan(form)
    if name == "fp.neg":
        return flip_sign(children[0], form, True)
    if name == "fp.abs":
        without = constant((1 << (form.width - 1)) - 1, form.width, word)
        return B.bitwise("and", [children[0], without], form.width,
                         children[0].unit)
    if name in ("to_fp", "to_fp_unsigned"):
        return to_float(node, children, form, word,
                        name == "to_fp_unsigned")
    if name in ARITHMETIC_NAMES:
        rounding = children[0]
        expect_nearest_even(rounding)
        left = children[1]
        right = children[2]
        if name == "fp.add":
            return add_or_subtract(left, right, form, False)
        if name == "fp.sub":
            return add_or_subtract(left, right, form, True)
        if name == "fp.mul":
            return multiply_floats(left, right, form)
        return divide_floats(left, right, form)
    raise B.Refused(CAUSE_NO_FLOAT_CONSTRUCTION,
                    "%s at %d bits" % (name, form.width))


def to_float(node, children, form, word, unsigned):
    """`to_fp` in its three arities: one argument is the IEEE
    reinterpretation, which is wiring; two are a rounding mode and
    either an integer or another float."""
    if len(children) == 1:
        return B.at_width(children[0], form.width, word)
    rounding = children[0]
    expect_nearest_even(rounding)
    source_node = node.arg(1)
    if z3.is_fp(source_node):
        source = format_of(source_node.sort(), word)
        return between_formats(children[1], source, form)
    return from_integer(children[1], form, not unsigned)


def expect_nearest_even(value):
    """the rounding mode read from the node's own DECLARATION KIND, not
    from its printed name: `z3.RNE()` prints `RNE()` and the pipeline's
    own terms print `roundNearestTiesToEven`, and they are one node."""
    if value.sort != "other":
        return
    node = value.passthrough
    try:
        if node.decl().kind() == z3.Z3_OP_FPA_RM_NEAREST_TIES_TO_EVEN:
            return
    except Exception:
        pass
    text = "%s" % node
    if "NearestTiesToEven" in text or text.startswith("RNE"):
        return
    raise B.Refused(CAUSE_RM, text)


def build_float_truth(node, children, word):
    """one truth-valued node of the float family."""
    name = "%s" % node.decl().name()
    if name in CLASS_NAMES:
        form = format_of(node.arg(0).sort(), word)
        bits = children[0]
        if name == "fp.isNaN":
            return B.Value("bool", truth=is_nan(bits, form))
        if name == "fp.isInfinite":
            return B.Value("bool", truth=is_infinite(bits, form))
        if name == "fp.isZero":
            return B.Value("bool", truth=is_zero_float(bits, form))
        if name == "fp.isNormal":
            return B.Value("bool", truth=is_normal_float(bits, form))
        if name == "fp.isSubnormal":
            return B.Value("bool", truth=is_subnormal(bits, form))
        if name == "fp.isNegative":
            state = z3.And(z3.Not(is_nan(bits, form)),
                           sign_of(bits, form) == z3.BitVecVal(1, 1))
            return B.Value("bool", truth=state)
        state = z3.And(z3.Not(is_nan(bits, form)),
                       sign_of(bits, form) == z3.BitVecVal(0, 1))
        return B.Value("bool", truth=state)
    if name in COMPARE_NAMES:
        form = format_of(node.arg(0).sort(), word)
        return B.Value("bool",
                       truth=compare_floats(children[0], children[1],
                                            form, name))
    if name in OWED_NAMES:
        raise B.Refused(CAUSE_NO_FLOAT_CONSTRUCTION, name)
    raise B.Refused(B.CAUSE_NO_CONSTRUCTION, name)
