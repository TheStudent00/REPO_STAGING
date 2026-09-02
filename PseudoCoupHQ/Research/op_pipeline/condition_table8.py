#!/usr/bin/env python3
"""condition_table8.py -- THE INT-TO-FLOAT-CONVERSION EXTENSION OF THE
UCOMISD/UCOMISS FLAGS FAMILY (condition_table4.py's FCEQ/FCNE/FCPAR/
FCNPAR/FCULT/FCUGE/FCUGT/FCULE synthetic ops). condition_table4.py's
own header named the SUBSTITUTION step (`substitute_float_packed`) as
already operand-shape-agnostic -- it matches the OUTER `And64(69:64,
zx64(CmpF64(<P>,<Q>)))` wrapper only, never looks at what P/Q are, so
it already fires on every one of this file's own target units
unmodified. What canon17_float.py's own `classify_float_operand`
leaves unresolved (returns (None, None) for, by its own header's
documented scope) is the OPERAND CLASSIFICATION of P/Q when one or
both is a CONVERTED argument (int-to-float via cvtsi2sd/cvtsi2ss/
cvtss2sd) instead of a native float register or the literal zero --
THIS FILE closes exactly that, reusing condition_table6.
classify_conv_expr UNCHANGED (the SAME five conversion kinds the
packed-mask family's own condition_table7.py already reused for its
own operand slots -- this file is condition_table7.py's own sibling,
built the same way, for the OTHER (scalar ucomisd/ucomiss) family).

SURVEY FIRST (evidence class: forced by construction -- direct scan,
this lap's own script, of every not-yet-converged unit whose stored
refusal is the generic "amd64g_calculate_condition... condition-code
helper call" text, 130 units total, ALL of which already have their
FCxx(CmpF64(P,Q)) atom successfully substituted by condition_table4.py
-- the refusal is entirely canon17_render.py's own operand-whitelist
refusal, never a substitution failure. THE SHAPES, exhaustively
(counts over the 130):

  (A) ex64@0(ins@0(<base>,I32StoF64(ex32@0(inK:64))))          16+16
      ex64@0(ins@0(<base>,I64StoF64(<rm>,inK:64)))              8+8
      -- a compiler-materialized f64 VALUE, VEX's own "write into a
      fresh temp, dead-zero the rest of the register" bookkeeping
      (the SAME `ins@0(u0:256, <conv>)` wrapper condition_table6.py's
      own `classify_operand` already parses for the packed-arithmetic
      family, and condition_table7.py's own `parse_maskexpr7` already
      generalizes to an ARBITRARY base, not just a literal zero base
      -- reused here at the SCALAR extraction width (`ex64@0`, not
      `ex32@0`/`ex8@0`) since a scalar f64 compare operand is 64 bits,
      not 32/8). classify_conv_expr resolves the inner conversion to
      kind i32_to_f64/i64_to_f64, compare width 64 (ucomisd).

  (B) ex64@0(ins@0(<base>,F32toF64(ex32@0(inK:256))))           8+8
      -- the SAME wrapper, around the ALREADY-whitelisted plain
      f32_to_f64 widen (canon17_float.py's own sixth shape) -- this
      file resolves it by unwrapping to the SAME text canon17_float
      already classifies, not by adding new vocabulary for it.

  (C) F32toF64(F64toF32(<rm>,I32StoF64(ex32@0(inK:64))))       32
      F32toF64(F64toF32(<rm>,I64StoF64(<rm>,inK:64)))          16
      -- ucomiss's own case: VEX widens ucomiss's f32 operands to f64
      for the SAME CmpF64 helper both instructions share (condition_
      table4.py's own header states this explicitly), so an int
      argument converted to f32 (condition_table6.classify_conv_expr's
      own i32_to_f32/i64_to_f32, `F64toF32(<rm>,I32/64StoF64(...))`)
      is then wrapped in ONE MORE `F32toF64` for the compare -- this
      file unwraps that outer widen and classifies the INNER
      conversion, recording the REAL (pre-widen) compare width, 32
      (ucomiss), not 64 -- the outer F32toF64 is VEX's own compare-
      helper plumbing, not part of what real ship code executes.

  (D) ex64@0(Add64F0x2(64HLtoV128(...Interleave...)))          16
      -- the u64/i64->double "magic bit-pattern constant" idiom
      condition_table6.py's own header ALREADY named and left OUT OF
      SCOPE for the packed-arithmetic family ("two DIFFERENT .rodata
      constants would need resolving, not one, and the arithmetic
      itself is a 2-instruction SEQUENCE standing in for one
      conversion, not a single op this grammar's own ('conv', ...)
      shape can name"). The SAME idiom recurs here as a comparison
      operand -- this file does NOT model it (classify_operand8
      returns (None, None), an honest, silent, unchanged refusal;
      real ship's own text for this shape is `punpckldq`/`subpd`/
      `unpckhpd`, a genuinely different lowering, not cvtsi2sd/
      cvtsi2ss under a different name).

  2 units (go/477, go/484) have BOTH operands already fully
  whitelisted by canon17_float.py's own UNEXTENDED classifier --
  their refusal is NOT an operand-classification gap at all (see
  canon22.py's own report for the actual cause: two And32-combined
  fcond atoms, condition_table4/canon17_float's own JOB, never this
  file's).

THE SPELLING BAN: this table is keyed by VEX op names (I32StoF64,
I64StoF64, F32toF64, F64toF32, ex64@0, ins@0, ...) and by structural
operand identity, never by the source-language operator token; it
classifies ONE operand's own expression tree and never groups or
pairs units.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table6 as CT6                                  # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize

# the PRE-EXISTING six-shape whitelist (canon17_float.py's own
# FLOAT_ARG_WHITELIST, transcribed verbatim -- this file does not
# import canon17_float.py, staying at the condition_table layer, the
# same discipline condition_table7.py follows relative to condition_
# table5.py's own PACKED_CMP_NAMES/LEAF_ZERO_128).
PLAIN_WHITELIST = {
    "ex64@0(in0:256)": ("a", 64),
    "ex64@0(in1:256)": ("b", 64),
    "F32toF64(ex32@0(in0:256))": ("a", 32),
    "F32toF64(ex32@0(in1:256))": ("b", 32),
    "F32toF64(0:32)": ("zero", 32),
    "0:64": ("zero", 64),
}

# conversion kinds that produce a NATIVE f64 value directly (cases A
# and B) -- the compare is at 64-bit width (ucomisd). f32_to_f64 is
# INCLUDED here (unlike canon17_float.py's own plain whitelist, where
# a BARE, unwrapped `F32toF64(ex32@0(inK:256))` means something
# different -- VEX's own artificial ucomiss-compare widening, no real
# instruction, operand width stays 32): once `F32toF64(ex32@0(...))`
# is found WRAPPED in this file's own `ex64@0(ins@0(base, val))` dead-
# write shape, that wrapper is real ship's own evidence of an ACTUAL
# `cvtss2sd` (a mixed float/double comparison -- e.g. `a:float ==
# b:double`, C's own usual-arithmetic-conversion rule promoting `a`),
# not a helper-argument artifact -- measured directly (c/op_556, this
# lap's own survey): P's own dead-write-wrapped `F32toF64(ex32@0(
# in0:256))` paired against Q's own PLAIN (unwrapped) `ex64@0(in1:
# 256))` (native f64, width 64) -- treating the wrapped P as width 32
# produced a width-mismatch refusal against Q's own genuine 64, the
# renderer correctly refusing rather than guessing; the fix is
# classifying the WRAPPED shape as a real f32_to_f64 CONVERSION
# (rendered via `cvtss2sd`, canon22_render.py's own existing case),
# width 64, not a bare direct tag.
F64_PRODUCING_KINDS = frozenset(["i32_to_f64", "i64_to_f64",
                                  "f32_to_f64"])

# conversion kinds that produce a NATIVE f32 value (case C) -- the
# compare is at 32-bit width (ucomiss), even though VEX's own text
# widens the compare's own operand to f64 via an outer F32toF64.
F32_PRODUCING_KINDS = frozenset(["i32_to_f32", "i64_to_f32"])


def _unwrap_dead_write_ex64(tree):
    """`ex64@0(ins@0(<base>, <val>))` -> `<val>`, or None. Same
    reasoning as condition_table7.py's own generalized `ins@0` case
    (file header there, quoted): the `ins@0` offset is always 0, so
    `val`'s own low bits fully overwrite `base`'s, and this file's own
    grammar never reads past `val`'s own width (64 bits, matching
    `ex64@0`'s own extraction width) -- so `base` is provably
    unreachable through this extraction point, whatever `base` is."""
    if tree[0] != "node":
        return None
    if tree[1] != "ex64@0":
        return None
    args = tree[2]
    if len(args) != 1:
        return None
    inner = args[0]
    if inner[0] != "node" or inner[1] != "ins@0":
        return None
    inner_args = inner[2]
    if len(inner_args) != 2:
        return None
    return inner_args[1]


def _unwrap_outer_widen(tree):
    """`F32toF64(<X>)` -> `<X>`, or None -- case C's own outer VEX
    compare-widen, distinct from the ALREADY-whitelisted plain
    `F32toF64(ex32@0(inK:256))` shape (that shape is handled first, by
    PLAIN_WHITELIST, before this function is ever tried)."""
    if tree[0] != "node":
        return None
    if tree[1] != "F32toF64":
        return None
    args = tree[2]
    if len(args) != 1:
        return None
    return args[0]


def classify_float_operand8(tree):
    """(tag, width) -- tag in {"a","b","zero"} or a `("conv", tag,
    kind)` tuple, or (None, None) if `tree` is outside every shape
    this file (or canon17_float.py's own unextended classifier)
    recognizes. Drop-in extension of canon17_float.classify_float_
    operand -- same return contract, tree-typed instead of text-typed
    so the conversion cases can recurse structurally."""
    text = serialize(tree)
    plain = PLAIN_WHITELIST.get(text)
    if plain is not None:
        return plain

    # case C: outer VEX compare-widen around an f32-producing
    # conversion (ucomiss of a converted int argument).
    widen_inner = _unwrap_outer_widen(tree)
    if widen_inner is not None:
        conv = CT6.classify_conv_expr(widen_inner)
        if conv is not None:
            tag, kind = conv
            if kind in F32_PRODUCING_KINDS:
                return (("conv", tag, kind), 32)

    # cases A/B: the dead-write `ex64@0(ins@0(base, val))` wrapper --
    # `val` is ALWAYS a real conversion once wrapped this way (see
    # F64_PRODUCING_KINDS's own comment, above, for why the bare
    # f32_to_f64 shape is handled separately, by PLAIN_WHITELIST,
    # before this branch is ever tried).
    val = _unwrap_dead_write_ex64(tree)
    if val is not None:
        conv = CT6.classify_conv_expr(val)
        if conv is not None:
            tag, kind = conv
            if kind in F64_PRODUCING_KINDS:
                return (("conv", tag, kind), 64)

    return (None, None)
