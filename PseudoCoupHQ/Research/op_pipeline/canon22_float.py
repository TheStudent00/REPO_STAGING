#!/usr/bin/env python3
"""canon22_float.py -- z3 MODEL for condition_table8.py's conversion-
extended ucomisd/ucomiss flags family. A faithful re-port of canon17_
float.py's own `to_z3_v2b`/`to_z3_with_prov_v2b` (same reason every
file in this lineage re-ports rather than calls the file below it --
see canon19_float.py's own header), with condition_table8's
`classify_float_operand8` swapped in for canon17_float's own
`classify_float_operand` in `_float_cond_payload` ONLY -- the atom
IDENTITY (an FCxx(CmpF64(P,Q)) node's own uninterpreted 1-bit z3
symbol, keyed by its WHOLE serialized text) never depended on operand
classification at all (canon17_float.py's own header: "It only needs
the WHOLE node's own IDENTITY"), so `to_z3_v2b` itself (the no-
provenance path, used only to refresh `normal_path_root`) is reused
UNCHANGED from canon17_float.py, not duplicated.

STILL NO NEW z3 THEORY HERE: exactly like canon17_float.py's own
FCxx atom, this file's job is ONLY to give the packed-flags condition
node a stable identity so the unit's z3 tree stays call-atom-free --
the compare's REAL meaning (what a converted int and a native float
actually compare as, including NaN/rounding) is proved separately by
canon22_behaviour_check.py's ground-truth gate, real z3 FPA, the same
division of labour condition_table4.py's own header established and
canon21_behaviour_check.py's own header restated for the packed-mask
sibling family.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table4 as CT4                                  # noqa: E402
import condition_table8 as CT8                                  # noqa: E402
import canon17_float as CF17                                    # noqa: E402
import z3                                                        # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize
leaf_width = TM.leaf_width

FLOAT_COND_OPS = CT4.FLOAT_COND_OPS

# the no-provenance path is IDENTICAL to canon17_float.py's own --
# operand classification is never consulted to build normal_path_root,
# only atom identity is, and that is unchanged. Reused, not
# duplicated.
to_z3_v2e = CF17.to_z3_v2b


def _float_cond_payload8(tree):
    """canon17_float._float_cond_payload, with condition_table8's
    conversion-aware classify_float_operand8 in place of canon17_
    float's own unextended classify_float_operand. Returns the SAME
    7-tuple shape (fcond, p_tag, p_width, q_tag, q_width, p_text,
    q_text) -- p_tag/q_tag may now ALSO be a `("conv", tag, kind)`
    tuple, not just a bare "a"/"b"/"zero" string."""
    fcond = tree[1]
    args = tree[2]
    if len(args) != 1:
        raise ValueError(
            "%s expects exactly one argument, got %d" % (fcond,
                                                           len(args)))
    inner = args[0]
    if inner[0] != "node" or inner[1] != "CmpF64":
        raise ValueError(
            "%s's argument is not a bare CmpF64(...) call: %r"
            % (fcond, serialize(inner)))
    inner_args = inner[2]
    if len(inner_args) != 2:
        raise ValueError(
            "CmpF64 expects exactly two arguments, got %d"
            % len(inner_args))
    p_text = serialize(inner_args[0])
    q_text = serialize(inner_args[1])
    p_tag, p_width = CT8.classify_float_operand8(inner_args[0])
    q_tag, q_width = CT8.classify_float_operand8(inner_args[1])
    return fcond, p_tag, p_width, q_tag, q_width, p_text, q_text


def to_z3_with_prov_v2e(tree, atoms, prov, widen_cache=None):
    """canon17_float.to_z3_with_prov_v2b, plus condition_table8's
    conversion-aware operand classification -- used by canon22_
    render.py's own self-consistency re-derivation."""
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

    if name in FLOAT_COND_OPS:
        text = serialize(tree)
        if text not in atoms:
            nm = "fc_%d" % len(atoms)
            atoms[text] = z3.BitVec(nm, 1)
            fcond, p_tag, p_w, q_tag, q_w, p_text, q_text = \
                _float_cond_payload8(tree)
            prov[nm] = ("fcond", dict(
                fcond=fcond,
                p_tag=p_tag, p_width=p_w, p_text=p_text,
                q_tag=q_tag, q_width=q_w, q_text=q_text,
            ))
        return atoms[text]

    kids = [to_z3_with_prov_v2e(a, atoms, prov, widen_cache)
            for a in args]

    if name in CF17.WIDE_MUL_OPS:
        return kids[0] * kids[1]
    if name == "64HLto128":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name in CF17.WIDE_DIVMOD_OPS:
        return CF17._wide_divmod(name, kids)

    return CF17._fallback_with_prov(tree, name, kids, atoms, prov,
                                     widen_cache)


def normalize_v2e(expr_text):
    """condition_table4.substitute_float_packed()'s own output ->
    (normalized_text, ok, note), pointed at to_z3_v2e (identical to
    canon17_float.py's own to_z3_v2b -- see file header)."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        e = to_z3_v2e(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (conversion-extended float packed-flags " \
            "model)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc
