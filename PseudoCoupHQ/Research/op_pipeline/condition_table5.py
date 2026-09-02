#!/usr/bin/env python3
"""condition_table5.py -- JOB 1: THE PACKED-MASK FLOAT COMPARE FAMILY
(cmpeqsd/cmpneqsd/cmpeqss/cmpneqss -- condition_table4.py's own header
named this family and explicitly did NOT model it: "126 not-yet-
converged units... a tractable follow-on, using the SAME is_nan/is_eq
predicate model... plus AndV128/OrV128/XorV128 128-bit bitwise support
and CmpEQ64F0x2/CmpEQ32F0x4's own mask formula -- diagnosed, not
built"). THIS FILE builds it.

THE SHAPE (evidence class: forced by construction, direct read of
tree_units2.json's own normal_path_raw for every not-yet-converged
unit containing CmpEQ64F0x2(/CmpEQ32F0x4(; see this lap's own survey
script): a packed SSE compare produces a 128-bit lane mask (all-ones
in a lane if that lane's operands compare equal, all-zeros otherwise);
this corpus's own real ship code only ever CONSUMES the mask's LOW
LANE (bits [63:0] for CmpEQ64F0x2, bits [31:0] for CmpEQ32F0x4) --
read off via `ex32@0(...)` at the outermost extraction, matching real
ship's own `movd %xmmN,%r10d; mov %r10d,%eax; and $0x1,%eax` (or
`movq` for the 64-bit case) idiom.  The MASK EXPRESSION itself is one
of a small closed grammar this corpus actually uses:

    CMP        := CmpEQ64F0x2(P, Q) | CmpEQ32F0x4(P, Q)
    EQWRAP      := ins@0(ins@0(<anything>, 0:128), CMP)      -- == mask
                    (the ins@0(<anything>,0:128) is VEX's own AVX
                    "upper-128-of-YMM zeroed" bookkeeping, immediately
                    overwritten -- dead, not consulted)
    NOTWRAP     := XorV128(<all-ones at CMP's own lane width>, CMP)
                    -- != mask (hardware CMPNEQSD/CMPNEQSS collapsed
                    into "NOT of the EQ mask" by this corpus's own
                    lift, exactly condition_table4.py's header already
                    established for the ucomisd family's own CondNE)
    MASKEXPR    := CMP | EQWRAP | NOTWRAP
                    | AndV128(MASKEXPR, MASKEXPR)
                    | OrV128(MASKEXPR, MASKEXPR)

    P, Q (each CMP's own two operands) -- THE OPERAND WHITELIST,
    measured directly (this file's own survey, 66 "clean-extraction"
    units -- see canon19.py's own header for the OTHER 50, a
    DIFFERENT, NOT-THIS-FILE'S-OWN defect):

        0:128                -- literal 0.0 (any precision; IEEE754
                                 +0.0's bit pattern is all-zero, so the
                                 bare 128-bit zero leaf IS the literal
                                 at either lane width)
        ex128@0(in0:256)     -- a, direct (no int/float conversion)
        ex128@0(in1:256)     -- b, direct

    Anything else (an int-to-float conversion atom, or a float
    constant materialized via a compile-time SIMD splice -- measured,
    38 of the 66 clean-extraction units) is OUT OF SCOPE for this
    file's own substitution -- `parse_maskexpr` returns None and the
    unit is left completely untouched, an honest, silent skip (same
    shape as condition_table4.substitute_float_packed's own "no
    packed-flags call in this text" no-op), never a guess.

THE SUBSTITUTION: unlike condition_table4.py (splices RAW TEXT
directly), this file parses the WHOLE unit expression into
tree_match.parse_expr's own tree, walks it, and re-serializes --
simpler and exactly as safe, since the grammar above is a strict
sub-tree match, never a text-position guess. Every `ex32@0(MASKEXPR)`
subtree (MASKEXPR parsing successfully per the grammar above) is
replaced by `FPACKMASK32(<the ORIGINAL MASKEXPR subtree, verbatim>)`
-- a single new opaque call node, carrying its own uniqueness via the
ORIGINAL text (so two occurrences of the textually-identical MASKEXPR
in one unit collapse onto the SAME atom downstream, matching every
other synthetic op in this lineage). canon19_float.py's own z3 model
re-parses that SAME argument text with `parse_maskexpr` (idempotent --
already proven to succeed once, at substitution time) to build the
renderer's provenance.

THE SPELLING BAN: this table is keyed by VEX op names (CmpEQ64F0x2,
XorV128, AndV128, OrV128, ins@0) and by STRUCTURAL operand identity
(ex128@0(in0:256) vs ex128@0(in1:256) vs the literal 0:128), never by
the source-language operator token; it substitutes inside ONE unit's
own expression tree and never groups or pairs units.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize

PACKED_CMP_NAMES = {
    "CmpEQ64F0x2": 64,
    "CmpEQ32F0x4": 32,
}

LEAF_ZERO_128 = ("leaf", "0:128")


def _leaf_int(tree):
    """the integer value of a leaf like '4294967295:128', or None if
    `tree` is not a leaf of that shape."""
    if tree[0] != "leaf":
        return None
    text = tree[1]
    if ":" not in text:
        return None
    num_text, _, width_text = text.rpartition(":")
    try:
        return int(num_text)
    except ValueError:
        return None


def classify_operand(tree):
    """(tag) in {"a", "b", "zero"}, or None -- see file header's own
    THE OPERAND WHITELIST."""
    if tree == LEAF_ZERO_128:
        return "zero"
    if tree[0] != "node":
        return None
    if tree[1] != "ex128@0":
        return None
    args = tree[2]
    if len(args) != 1:
        return None
    inner = args[0]
    if inner == ("leaf", "in0:256"):
        return "a"
    if inner == ("leaf", "in1:256"):
        return "b"
    return None


def parse_maskexpr(tree):
    """the MASKEXPR grammar (file header) -> a small AST:
        ("cmp", precision, is_ne, p_tag, q_tag)
        ("and", L, R)
        ("or", L, R)
    or None if `tree` does not match the grammar at all (out of
    scope, refused silently -- see file header)."""
    if tree[0] != "node":
        return None
    name, args = tree[1], tree[2]

    if name in PACKED_CMP_NAMES:
        if len(args) != 2:
            return None
        precision = PACKED_CMP_NAMES[name]
        p_tag = classify_operand(args[0])
        q_tag = classify_operand(args[1])
        if p_tag is None or q_tag is None:
            return None
        return ("cmp", precision, False, p_tag, q_tag)

    if name == "XorV128":
        if len(args) != 2:
            return None
        mask_leaf, inner = args[0], args[1]
        inner_parsed = parse_maskexpr(inner)
        if inner_parsed is None or inner_parsed[0] != "cmp":
            return None
        mask_val = _leaf_int(mask_leaf)
        if mask_val is None:
            return None
        _, precision, is_ne, p_tag, q_tag = inner_parsed
        expected = (1 << precision) - 1
        if mask_val != expected:
            return None
        return ("cmp", precision, not is_ne, p_tag, q_tag)

    if name == "ins@0":
        # ONLY the specific dead-zero-write idiom (see file header's
        # own EQWRAP) -- a general ins@0 is a real partial-register
        # write and must NOT be treated as pass-through.
        if len(args) != 2:
            return None
        base, val = args
        if base[0] != "node" or base[1] != "ins@0":
            return None
        if len(base[2]) != 2:
            return None
        if base[2][1] != LEAF_ZERO_128:
            return None
        return parse_maskexpr(val)

    if name in ("AndV128", "OrV128"):
        if len(args) != 2:
            return None
        left = parse_maskexpr(args[0])
        right = parse_maskexpr(args[1])
        if left is None or right is None:
            return None
        kind = "and" if name == "AndV128" else "or"
        return (kind, left, right)

    return None


# the SAME MASKEXPR is sometimes read back at more than one width in
# one unit's own text (measured: cpp's `||`/`&&` units carry BOTH an
# `ex32@0(MASKEXPR)` -- feeding a wider zx64(...) write -- AND an
# `ex8@0(MASKEXPR)` of the textually-IDENTICAL MASKEXPR -- feeding an
# `And8(1:8,...)` truthy write, tree_match2's own two recorded paths
# for the same boolean). Both extraction widths read the SAME 0/1
# answer out of the SAME mask (the real value only ever occupies bit
# 0 once the caller ANDs with 1). z3's own bitwise ops (`And8`'s own
# generic `kids[0] & kids[1]`, unlike COND_OPS, does NOT reconcile
# mismatched widths -- measured directly, `Z3Exception('...does not
# match declaration bvand...')` on cpp's own `||`/`&&` units), so EACH
# extraction width gets its OWN atom name/declared width
# (`FPACKMASK32` / `FPACKMASK8`) even though both share the SAME
# provenance kind ("packmask") and the SAME underlying MASKEXPR --
# canon19_render.py's own dispatch is keyed on provenance KIND, never
# on the atom's declared width, so both render identically (the SAME
# instruction sequence, ending in one `movd` into a 32-bit GP view --
# there is no narrower `movd` form, and none is needed: the outer
# ex8@0/And8 wrapping already narrows the SAME physical register via
# the EXISTING generic renderer, unchanged).
MASKEXPR_EXTRACT_NAMES = {
    "ex32@0": "FPACKMASK32",
    "ex8@0": "FPACKMASK8",
}


def _rewrite_tree(tree):
    """(new_tree, applied_count) -- see file header's own THE
    SUBSTITUTION."""
    if tree[0] == "leaf":
        return tree, 0
    name, args = tree[1], tree[2]
    op_name = MASKEXPR_EXTRACT_NAMES.get(name)
    if op_name is not None and len(args) == 1:
        parsed = parse_maskexpr(args[0])
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


def substitute_packed_mask(raw_text):
    """(new_text, applied, note) -- same shape as condition_table4.
    substitute_float_packed. `applied` is the count of ex32@0(MASKEXPR)
    spans folded into FPACKMASK32(...); 0 means this unit's own
    CmpEQ64F0x2/CmpEQ32F0x4 use (if any) is outside this file's own
    scope (see file header), left COMPLETELY untouched."""
    tree = parse_expr(raw_text)
    new_tree, applied = _rewrite_tree(tree)
    if applied == 0:
        return raw_text, 0, "no in-scope packed-mask compare " \
            "(ex32@0(MASKEXPR), MASKEXPR per this file's own grammar) " \
            "found in this unit's own text"
    return serialize(new_tree), applied, None
