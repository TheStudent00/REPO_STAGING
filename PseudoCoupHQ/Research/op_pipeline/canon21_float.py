#!/usr/bin/env python3
"""canon21_float.py -- z3 MODEL for condition_table7.py's conversion-
extended packed-mask float compare family (FPACKMASK32C/FPACKMASK8C).
A faithful re-port of canon19_float.py's own to_z3_v2c/to_z3_with_
prov_v2c (same reason every file in this lineage re-ports rather than
calls the file below it -- see canon19_float.py's own header), with
condition_table5 swapped for condition_table7 in the provenance build
(parse_maskexpr7 instead of parse_maskexpr, so a converted operand's
own (tag, kind) survives into the renderer's payload).

STILL NO z3 FPA HERE, and this is not a gap: exactly like canon19_
float.py's own FPACKMASK32 atom, this file's job is ONLY to give the
packed-mask compare node a STABLE IDENTITY (same text -> same opaque
32/8-bit atom) so the unit's z3 tree stays call-atom-free -- the
compare's REAL floating-point meaning (what a converted int and a
native float actually compare as, including NaN/rounding) is proved
separately, with REAL z3 FPA (fpSignedToFP/fpFPToFP/fpToIEEEBV), by
canon21_behaviour_check.py's ground-truth gate -- the same division of
labour condition_table4.py's own header already established: this
layer only needs uninterpreted-but-consistent identity; the PROOF that
the identity is safe to trust is the gate's job, done once, honestly,
against real ship code, not re-litigated inside every z3 tree.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table4 as CT4                                  # noqa: E402
import condition_table7 as CT7                                  # noqa: E402
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

PACKMASK_WIDTH = {
    "FPACKMASK32C": 32,
    "FPACKMASK8C": 8,
}


def to_z3_v2d(tree, atoms, widen_cache=None):
    """canon19_float.to_z3_v2c, plus FPACKMASK32C/FPACKMASK8C -- used
    to compute the FRESH stored `normal_path_root` text after
    condition_table7.substitute_packed_mask_conv() has already
    rewritten the raw text."""
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
            atoms[text] = z3.BitVec("fpmc_%d" % len(atoms), w)
        return atoms[text]

    if name in FLOAT_COND_OPS:
        text = serialize(tree)
        if text not in atoms:
            atoms[text] = z3.BitVec("fc_%d" % len(atoms), 1)
        return atoms[text]

    kids = [to_z3_v2d(a, atoms, widen_cache) for a in args]

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


def to_z3_with_prov_v2d(tree, atoms, prov, widen_cache=None):
    """canon19_float.to_z3_with_prov_v2c, plus FPACKMASK32C/
    FPACKMASK8C -- used by canon21_render.py's own self-consistency
    re-derivation. Builds provenance via condition_table7.
    parse_maskexpr7 (conversion-aware), not condition_table5's own."""
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
            nm = "fpmc_%d" % len(atoms)
            w = PACKMASK_WIDTH[name]
            atoms[text] = z3.BitVec(nm, w)
            maskexpr = CT7.parse_maskexpr7(args[0])
            prov[nm] = ("packmaskconv", dict(
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

    kids = [to_z3_with_prov_v2d(a, atoms, prov, widen_cache)
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


def normalize_v2d(expr_text):
    """(normalized_text, ok, note), pointed at to_z3_v2d."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        e = to_z3_v2d(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (int-to-float conversion packed-mask compare " \
            "model)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc
