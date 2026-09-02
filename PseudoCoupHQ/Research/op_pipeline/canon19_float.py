#!/usr/bin/env python3
"""canon19_float.py -- JOB 1's z3 MODEL for the packed-mask float
compare family (condition_table5.py's FPACKMASK32 synthetic op),
plumbed into the SAME small rewrite table canon12_normalize.py/canon17
_float.py already extended -- a faithful RE-PORT of canon17_float.py's
own to_z3_v2b/to_z3_with_prov_v2b/_fallback_* (same reason those files
re-port instead of calling one another: each new synthetic op needs a
case checked BEFORE the generic recursion, at every nesting depth, so
a plain function call to an outer file's entry point would never see
it below the top).

THE NEW CASE, ONE ADDITION: `name == "FPACKMASK32"`.  Like JOB 1's own
`FCxx(CmpF64(...))` atom, this file does NOT need the packed mask's
own VALUE (no z3 FPA) -- it only needs the node's own STABLE IDENTITY
(the SAME `FPACKMASK32(<text>)` -> the SAME 32-bit atom, matching the
`atoms` dict's existing text-keyed-cache behaviour) plus, in the
provenance build, condition_table5.parse_maskexpr's own AST (re-parsed
from the stored argument text -- idempotent, already proven to parse
once at substitution time) so canon19_render.py can walk it and emit
real cmpeqsd/cmpneqsd/andps/orps instructions.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table4 as CT4                                  # noqa: E402
import condition_table5 as CT5                                  # noqa: E402
import canon12_normalize as C12N                                 # noqa: E402
import canon17_float as CF17                                     # noqa: E402
import z3                                                        # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize
leaf_width = TM.leaf_width

WIDE_MUL_OPS = C12N.WIDE_MUL_OPS
WIDE_DIVMOD_OPS = C12N.WIDE_DIVMOD_OPS
_wide_divmod = C12N._wide_divmod
FLOAT_COND_OPS = CT4.FLOAT_COND_OPS

# condition_table5.MASKEXPR_EXTRACT_NAMES's own codomain, with the
# DECLARED z3 width each synthetic op's atom must carry so it type-
# checks against whichever generic bitwise op (And32/And8/...) wraps
# it in the unit's own text -- see condition_table5.py's own header
# for why one MASKEXPR can need two different atom widths.
PACKMASK_WIDTH = {
    "FPACKMASK32": 32,
    "FPACKMASK8": 8,
}


def to_z3_v2c(tree, atoms, widen_cache=None):
    """canon17_float.to_z3_v2b, plus FPACKMASK32 -- used to compute the
    FRESH stored `normal_path_root` text (no provenance needed) after
    condition_table5.substitute_packed_mask() has already rewritten
    the raw text (condition_table4.substitute_float_packed() may ALSO
    have run first on the same text -- the two families never overlap
    in one call span, see canon19.py's own driver)."""
    if widen_cache is None:
        widen_cache = {}
    kind = tree[0]
    if kind == "leaf":
        text = tree[1]
        w = leaf_width(text)
        key = text
        if key not in atoms:
            atoms[key] = z3.BitVec("atom_%d" % len(atoms), w)
        return atoms[key]

    name, args = tree[1], tree[2]

    if name in PACKMASK_WIDTH:
        text = serialize(tree)
        if text not in atoms:
            w = PACKMASK_WIDTH[name]
            atoms[text] = z3.BitVec("fpm_%d" % len(atoms), w)
        return atoms[text]

    if name in FLOAT_COND_OPS:
        text = serialize(tree)
        if text not in atoms:
            atoms[text] = z3.BitVec("fc_%d" % len(atoms), 1)
        return atoms[text]

    kids = [to_z3_v2c(a, atoms, widen_cache) for a in args]

    if name in WIDE_MUL_OPS:
        return kids[0] * kids[1]
    if name == "64HLto128":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name in WIDE_DIVMOD_OPS:
        return _wide_divmod(name, kids)

    prov = {}
    return CF17._fallback_no_prov(tree, name, kids, atoms, prov,
                                   widen_cache)


def to_z3_with_prov_v2c(tree, atoms, prov, widen_cache=None):
    """canon17_float.to_z3_with_prov_v2b, plus FPACKMASK32 -- used by
    canon19_render.py's own self-consistency re-derivation."""
    if widen_cache is None:
        widen_cache = {}
    kind = tree[0]
    if kind == "leaf":
        text = tree[1]
        w = leaf_width(text)
        key = text
        if key not in atoms:
            name = "atom_%d" % len(atoms)
            atoms[key] = z3.BitVec(name, w)
            prov[name] = ("leaf", key)
        return atoms[key]

    name, args = tree[1], tree[2]

    if name in PACKMASK_WIDTH:
        text = serialize(tree)
        if text not in atoms:
            nm = "fpm_%d" % len(atoms)
            w = PACKMASK_WIDTH[name]
            atoms[text] = z3.BitVec(nm, w)
            maskexpr = CT5.parse_maskexpr(args[0])
            prov[nm] = ("packmask", dict(
                maskexpr=maskexpr,
                text=serialize(args[0]),
            ))
        return atoms[text]

    if name in FLOAT_COND_OPS:
        text = serialize(tree)
        if text not in atoms:
            nm = "fc_%d" % len(atoms)
            atoms[text] = z3.BitVec(nm, 1)
            fcond, p_tag, p_w, q_tag, q_w, p_text, q_text = \
                CF17._float_cond_payload(tree)
            prov[nm] = ("fcond", dict(
                fcond=fcond,
                p_tag=p_tag, p_width=p_w, p_text=p_text,
                q_tag=q_tag, q_width=q_w, q_text=q_text,
            ))
        return atoms[text]

    kids = [to_z3_with_prov_v2c(a, atoms, prov, widen_cache)
            for a in args]

    if name in WIDE_MUL_OPS:
        return kids[0] * kids[1]
    if name == "64HLto128":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name in WIDE_DIVMOD_OPS:
        return _wide_divmod(name, kids)

    return CF17._fallback_with_prov(tree, name, kids, atoms, prov,
                                     widen_cache)


def normalize_v2c(expr_text):
    """(normalized_text, ok, note), pointed at to_z3_v2c."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        e = to_z3_v2c(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (JOB 1 packed-mask float compare model)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc
