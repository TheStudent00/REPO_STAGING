#!/usr/bin/env python3
"""condition_table7.py -- THE INT-TO-FLOAT-CONVERSION EXTENSION OF THE
PACKED-MASK FLOAT COMPARE FAMILY (condition_table5.py). condition_
table5.py's own header named its scope precisely and named what it
left out: "an int-to-float conversion atom... is OUT OF SCOPE for this
file's own substitution... 38 of the 66 clean-extraction units" --
THIS FILE builds exactly that follow-on, for the CmpEQ64F0x2/
CmpEQ32F0x4 packed-mask family. condition_table6.py (JOB 3, packed
float ARITHMETIC) already built and proved the conversion-classifier
this file reuses UNCHANGED (`classify_conv_expr` -- i32_to_f64,
i64_to_f64, f32_to_f64, i32_to_f32, i64_to_f32), so this file adds NO
new conversion vocabulary, only a NEW CONSUMER of the existing one: the
packed-mask compare's own P/Q operand slots.

WORKED EXAMPLE (c/op_501, `a != b`, a:i32, b:f32 -- tree_units2.json's
own `normal_path_raw`, verbatim):

    XorV128(4294967295:128,CmpEQ32F0x4(
        ex128@0(ins@0(u0:256,F64toF32(And32(3:32,ex32@0(u1:64)),
                                       I32StoF64(ex32@0(in0:64))))),
        ex128@0(in1:256)))

P (`ex128@0(ins@0(u0:256, F64toF32(<rm>, I32StoF64(ex32@0(in0:64)))))`)
is condition_table5.py's own "an int-to-float conversion atom" case,
now resolved: the SAME `ins@0(u0:256, <conv>)` wrapper condition_
table6.classify_operand already parses for the arithmetic family,
carrying a=i32 converted to f32 (kind "i32_to_f32", VEX's own two-step
int32->f64->f32 lift of a single real CVTSI2SS -- condition_table6.py's
own header already established this is ONE rounding, matching real
ship bit-for-bit). Q (`ex128@0(in1:256)`) is condition_table5's own
plain "b, direct". Real ship code for this exact unit (canon4_units_c.
json's own `mnem`, forced by construction): `cvtsi2ss %edi,%xmm2;
cmpneqss %xmm0,%xmm2; movd %xmm2,%r10d; mov %r10d,%eax; and $0x1,%eax;
ret` -- the conversion instruction IS part of real ship's own text,
confirming the grammar below names a real, not invented, shape.

THE GRAMMAR: IDENTICAL to condition_table5.py's own MASKEXPR grammar
(CMP/EQWRAP/NOTWRAP/AndV128/OrV128), with ONE extension to THE OPERAND
WHITELIST -- P or Q may now ALSO be:

    ex128@0(ins@0(u0:256, <CONV>))   -- a compiler-materialized f32/f64
                                         VALUE, produced by converting
                                         a or b via one of condition_
                                         table6.classify_conv_expr's own
                                         five recognized shapes (i32_to_
                                         f64, i64_to_f64, f32_to_f64,
                                         i32_to_f32, i64_to_f32)

exactly the SAME `ins@0(u0:256, ...)` wrapper condition_table6.py's own
`classify_operand` already parses for the arithmetic family (VEX's own
"write into a fresh temp, dead-zero the rest of the YMM register"
bookkeeping) -- reused verbatim, not re-derived.

THE SUBSTITUTION: unlike condition_table5.py (which this file does NOT
modify -- new file, per this lap's own brief), this file re-implements
`_rewrite_tree`/`substitute_packed_mask` with its OWN grammar
(`parse_maskexpr7`), producing NEW synthetic op names (`FPACKMASK32C`/
`FPACKMASK8C`, the "C" for "conversion-aware") so a unit this file
substitutes can NEVER be silently re-matched by condition_table5's own
(unextended) driver, and vice versa -- the two tables' own outputs stay
textually distinguishable at every downstream stage, never relying on
call order to keep them apart.

THE SPELLING BAN: this table is keyed by VEX op names (CmpEQ64F0x2,
XorV128, I32StoF64, F64toF32, ins@0, ...) and by structural operand
identity, never by the source-language operator token; it substitutes
inside ONE unit's own expression tree and never groups or pairs units.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table5 as CT5                                  # noqa: E402
import condition_table6 as CT6                                  # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize

PACKED_CMP_NAMES = CT5.PACKED_CMP_NAMES
LEAF_ZERO_128 = CT5.LEAF_ZERO_128
_leaf_int = CT5._leaf_int


def classify_operand7(tree):
    """condition_table5.classify_operand, EXTENDED: returns "a" | "b" |
    "zero" | ("conv", tag, kind) | None. Tries the plain direct/zero
    shapes first (condition_table5's own grammar, unchanged), then
    falls back to condition_table6.classify_operand's own `ins@0(u0:
    256, <conv>)` conversion shape, keeping only its ("conv", tag,
    kind) case -- a packed-mask compare's own P/Q slot is never itself
    a `const` (a .rodata literal), so that third CT6 case is not
    reachable here and is left unmatched (returns None), an honest
    narrowing, not a guess."""
    direct = CT5.classify_operand(tree)
    if direct is not None:
        return direct
    ct6_operand = CT6.classify_operand(tree)
    if ct6_operand is not None and ct6_operand[0] == "conv":
        _, tag, kind = ct6_operand
        return ("conv", tag, kind)
    return None


def parse_maskexpr7(tree):
    """condition_table5.parse_maskexpr, EXTENDED with classify_
    operand7 in place of classify_operand -- see file header. Returns
    the SAME small AST shape (("cmp", precision, is_ne, p_operand,
    q_operand), ("and", L, R), ("or", L, R)), with p_operand/q_operand
    now possibly a ("conv", tag, kind) tuple instead of a bare tag
    string."""
    if tree[0] != "node":
        return None
    name, args = tree[1], tree[2]

    if name in PACKED_CMP_NAMES:
        if len(args) != 2:
            return None
        precision = PACKED_CMP_NAMES[name]
        p_operand = classify_operand7(args[0])
        q_operand = classify_operand7(args[1])
        if p_operand is None or q_operand is None:
            return None
        return ("cmp", precision, False, p_operand, q_operand)

    if name == "XorV128":
        if len(args) != 2:
            return None
        mask_leaf, inner = args[0], args[1]
        inner_parsed = parse_maskexpr7(inner)
        if inner_parsed is None or inner_parsed[0] != "cmp":
            return None
        mask_val = _leaf_int(mask_leaf)
        if mask_val is None:
            return None
        _, precision, is_ne, p_operand, q_operand = inner_parsed
        expected = (1 << precision) - 1
        if mask_val != expected:
            return None
        return ("cmp", precision, not is_ne, p_operand, q_operand)

    if name == "ins@0":
        # GENERALIZED EQWRAP: condition_table5.py's own header
        # documents ONE dead-write shape (`ins@0(ins@0(<anything>,
        # 0:128), CMP)`, base a literal zero). This corpus's own
        # conversion-bearing units (measured directly, this file's own
        # survey -- see canon21.py's own report) instead nest a REAL
        # conversion value as the dead write's own base (`ins@0(u0:256,
        # F64toF32(...))`, not `0:128`) -- e.g. c/op_501's own
        # normal_path_raw: `ins@0(ins@0(u0:256, F64toF32(...,
        # I32StoF64(...))), XorV128(...))`. Any `ins@0(base, val)` at
        # offset 0 discards `base` unconditionally, not just when
        # `base` is a literal zero: the offset is always 0 (baked into
        # the node's own name), so `val`'s own bits fully overwrite
        # `base`'s low `val`-width bits, and this file's own grammar
        # NEVER reads past that width (every consumer is `ex32@0`/
        # `ex8@0`, both <= 128 bits, matching `val`'s own minimum
        # width, CmpEQ64F0x2/CmpEQ32F0x4's 128-bit lane output) -- so
        # `base`'s bits are PROVABLY unreachable through this file's
        # own extraction points, whatever `base` is. `parse_maskexpr7`
        # only ever recurses into `val`; a `base` that happened to be
        # semantically load-bearing would simply make `val` itself
        # fail to parse under this grammar (an unrelated real value in
        # `val`'s own position), refusing honestly rather than
        # silently keeping a stale check that never fires on this
        # corpus's own real shape.
        if len(args) != 2:
            return None
        base, val = args
        return parse_maskexpr7(val)

    if name in ("AndV128", "OrV128"):
        if len(args) != 2:
            return None
        left = parse_maskexpr7(args[0])
        right = parse_maskexpr7(args[1])
        if left is None or right is None:
            return None
        kind = "and" if name == "AndV128" else "or"
        return (kind, left, right)

    return None


MASKEXPR_EXTRACT_NAMES = {
    "ex32@0": "FPACKMASK32C",
    "ex8@0": "FPACKMASK8C",
}


def _rewrite_tree(tree):
    """(new_tree, applied_count) -- see file header's own THE
    SUBSTITUTION."""
    if tree[0] == "leaf":
        return tree, 0
    name, args = tree[1], tree[2]
    op_name = MASKEXPR_EXTRACT_NAMES.get(name)
    if op_name is not None and len(args) == 1:
        parsed = parse_maskexpr7(args[0])
        if parsed is not None:
            new_node = ("node", op_name, [args[0]])
            return new_node, 1
    new_args = []
    total = 0
    for a in args:
        new_a, cnt = _rewrite_tree(a)
        new_args.append(new_a)
        total = total + cnt
    return ("node", name, new_args), total


def substitute_packed_mask_conv(raw_text):
    """(new_text, applied, note) -- same shape as condition_table5.
    substitute_packed_mask. `applied` is the count of ex32@0(MASKEXPR)/
    ex8@0(MASKEXPR) spans folded into FPACKMASK32C(...)/FPACKMASK8C(
    ...); 0 means this unit's own packed-mask compare use (if any) is
    outside this file's own (conversion-extended) scope, left
    COMPLETELY untouched.

    THE BARE-TOP-LEVEL CASE, TRIED AND REJECTED (recorded so it is not
    re-attempted): a unit whose entire `normal_path_raw` parses under
    `parse_maskexpr7` with NO ex32@0/ex8@0 wrapper at all (e.g.
    c/op_501) is NOT the same shape as a properly-wrapped unit -- real
    ship code for op_501 ends `movd %xmm2,%r10d; mov %r10d,%eax; and
    $0x1,%eax`, and that final boolean-narrowing AND is genuinely
    ABSENT from this unit's own captured `normal_path_raw` (a
    DIFFERENT, pre-existing gap -- condition_table5.py's own header
    and canon19.py's own header both already name it: "the final
    extraction step missing from normal_path_raw... a DIFFERENT, NOT-
    THIS-FILE'S-OWN defect"). This file tried treating a bare top-level
    match as `FPACKMASK32C(<whole text>)` and canon21_behaviour_check's
    own real-z3-FPA gate correctly DISPROVED the result (c/op_501:
    candidate answered 0xFF instead of 0/1 -- the missing AND, caught,
    not guessed past). So this file, like condition_table5.py before
    it, ONLY substitutes an EXPLICIT ex32@0(MASKEXPR)/ex8@0(MASKEXPR)
    wrapper -- the same evidence-carrying shape that already proves the
    boolean-narrowing AND is present elsewhere in the SAME tree (the
    existing generic GP-side renderer's own job, unchanged, per
    condition_table5.py's own header: "no new GP-side code needed at
    all"). A unit missing that wrapper is left untouched here, same as
    condition_table5.py leaves it untouched -- honestly out of scope,
    not silently mis-rendered."""
    tree = parse_expr(raw_text)
    new_tree, applied = _rewrite_tree(tree)
    if applied == 0:
        return raw_text, 0, "no in-scope conversion-extended " \
            "packed-mask compare found in this unit's own text"
    return serialize(new_tree), applied, None
