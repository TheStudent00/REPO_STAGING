#!/usr/bin/env python3
"""canon17_float.py -- JOB 1's z3 MODEL for the float packed-flags
condition family (condition_table4.py's FCEQ/FCNE/FCPAR/FCNPAR/
FCULT/FCUGE/FCUGT/FCULE synthetic ops), plumbed into the SAME small
rewrite table canon12_normalize.py already extended (Mul64/Mul32/
64HLto128/DivModS128to64/DivModU128to64) -- a faithful RE-PORT of that
file's own `to_z3_v2`/`to_z3_with_prov_v2`/`_fallback_with_prov`
(same reason canon12_normalize.py re-ports expr_to_canon.py's own
function instead of calling it: "that function is not itself callable
as 'everything after the point my new cases would have matched'" --
the same constraint applies one layer up here).

THE NEW CASE, ONE ADDITION: `name in condition_table4.FLOAT_COND_OPS`.
Unlike every other case in this table (which evaluates its children
into real z3 sub-expressions), THIS case does NOT recurse into its own
argument at all -- the argument is `CmpF64(P, Q)`, and this file does
not need P/Q's VALUE (no z3 FPA, no bit-pattern reinterpretation of a
float -- see condition_table4.py's own header for why). It only needs
the WHOLE node's own IDENTITY: the same `FCxx(CmpF64(P,Q))` text,
anywhere it recurs in one unit's own expression, denotes the SAME
1-bit boolean atom (the "uninterpreted-but-consistent" requirement
condition_table4.py's header states) -- exactly the existing `atoms`
dict's own text-keyed-cache behaviour, reused unchanged. The result is
tagged in `prov` with a NEW kind, `"fcond"`, carrying everything
canon17_render.py needs to render it: the condition name, and P/Q's
OWN classification (see `classify_float_operand` below) -- so it is
never confused with a genuine unmodeled call (`kind == "call"`, which
still means "refuse, no return path").

THE OPERAND WHITELIST (`classify_float_operand`) -- measured directly
(condition_table4.py's own report; see the survey script beside this
file), the SIX distinct argument shapes that account for the entire
"pure float-vs-float, no int/float conversion" population:

    ex64@0(in0:256)             -- a, f64, direct
    ex64@0(in1:256)             -- b, f64, direct
    F32toF64(ex32@0(in0:256))   -- a, f32 (VEX widens for the compare)
    F32toF64(ex32@0(in1:256))   -- b, f32
    F32toF64(0:32)              -- literal 0.0f (f32 zero)
    0:64                        -- literal 0.0 (f64 zero, IEEE754 bit
                                    pattern for +0.0 is all-zero, so
                                    the bare 64-bit zero leaf IS the
                                    literal)

Anything else (int-to-float conversion atoms -- I32StoF64, I64StoF64,
F64toF32 -- or a comparison between two DIFFERENT converted values)
is OUT OF SCOPE for this file's own renderer (canon17_render.py) --
the z3 MODEL below still resolves it (the atom is created either way,
so the unit's z3 tree stays call-atom-free and self-consistency still
holds), but classify_float_operand returns (None, None) for it and
the renderer refuses honestly rather than guessing which registers to
compare.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table4 as CT4                                  # noqa: E402
import canon12_normalize as C12N                                 # noqa: E402
import z3                                                        # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize
leaf_width = TM.leaf_width

WIDE_MUL_OPS = C12N.WIDE_MUL_OPS
WIDE_DIVMOD_OPS = C12N.WIDE_DIVMOD_OPS
_wide_divmod = C12N._wide_divmod

FLOAT_COND_OPS = CT4.FLOAT_COND_OPS

FLOAT_ARG_WHITELIST = {
    "ex64@0(in0:256)": ("a", 64),
    "ex64@0(in1:256)": ("b", 64),
    "F32toF64(ex32@0(in0:256))": ("a", 32),
    "F32toF64(ex32@0(in1:256))": ("b", 32),
    "F32toF64(0:32)": ("zero", 32),
    "0:64": ("zero", 64),
}


def classify_float_operand(text):
    """(tag, width) -- tag in {"a", "b", "zero"}, or (None, None) if
    `text` is not one of the six whitelisted shapes (see file
    header)."""
    return FLOAT_ARG_WHITELIST.get(text, (None, None))


def _float_cond_payload(tree):
    """(fcond, p_tag, p_width, q_tag, q_width, p_text, q_text) for an
    `FCxx(CmpF64(P,Q))` tree node. Raises ValueError if the argument
    is not literally a single `CmpF64(P,Q)` call (never measured
    otherwise -- condition_table4.py only ever substitutes this exact
    shape, so a mismatch here means the raw text was hand-edited or
    corrupted, not a real corpus case)."""
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
    p_tag, p_width = classify_float_operand(p_text)
    q_tag, q_width = classify_float_operand(q_text)
    return fcond, p_tag, p_width, q_tag, q_width, p_text, q_text


def to_z3_v2b(tree, atoms, widen_cache=None):
    """canon12_normalize.to_z3_v2, plus FLOAT_COND_OPS -- used to
    compute the FRESH stored `normal_path_root` text (no provenance
    needed) after condition_table4.substitute_float_packed() has
    already rewritten the raw text."""
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

    if name in FLOAT_COND_OPS:
        text = serialize(tree)
        if text not in atoms:
            atoms[text] = z3.BitVec("fc_%d" % len(atoms), 1)
        return atoms[text]

    kids = [to_z3_v2b(a, atoms, widen_cache) for a in args]

    if name in WIDE_MUL_OPS:
        return kids[0] * kids[1]
    if name == "64HLto128":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name in WIDE_DIVMOD_OPS:
        return _wide_divmod(name, kids)

    prov = {}
    return _fallback_no_prov(tree, name, kids, atoms, prov, widen_cache)


def to_z3_with_prov_v2b(tree, atoms, prov, widen_cache=None):
    """canon12_normalize.to_z3_with_prov_v2, plus FLOAT_COND_OPS --
    used by canon17_render.py's own self-consistency re-derivation
    (needs provenance so the renderer can trace an `fcond` atom back
    to its condition name and operand tags)."""
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
                _float_cond_payload(tree)
            prov[nm] = ("fcond", dict(
                fcond=fcond,
                p_tag=p_tag, p_width=p_w, p_text=p_text,
                q_tag=q_tag, q_width=q_w, q_text=q_text,
            ))
        return atoms[text]

    kids = [to_z3_with_prov_v2b(a, atoms, prov, widen_cache)
            for a in args]

    if name in WIDE_MUL_OPS:
        return kids[0] * kids[1]
    if name == "64HLto128":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name in WIDE_DIVMOD_OPS:
        return _wide_divmod(name, kids)

    return _fallback_with_prov(tree, name, kids, atoms, prov,
                                widen_cache)


def normalize_v2b(expr_text):
    """condition_table4.substitute_float_packed()'s own output ->
    (normalized_text, ok, note), pointed at to_z3_v2b."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        e = to_z3_v2b(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (JOB 1 float packed-flags model)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc


# --------------------------------------------------------------------
# the re-ported fallback -- IDENTICAL to canon12_normalize.py's own
# `to_z3_v2`/`_fallback_with_prov` bodies (COND_OPS, And/Or/Xor/Add/
# Sub/Not, shifts, zx/sx/ex, 32HLto64, ite, ins@N, final opaque-call),
# duplicated rather than called because those functions recurse using
# THEIR OWN name, which would never see FLOAT_COND_OPS at any nesting
# depth below the top. See file header.
# --------------------------------------------------------------------

def _fallback_no_prov(tree, name, kids, atoms, prov, widen_cache):
    import condition_table as CT

    if name in CT.COND_OPS:
        L, R = kids[0], kids[1]
        if L.size() != R.size():
            if L.size() < R.size():
                L = z3.ZeroExt(R.size() - L.size(), L)
            else:
                R = z3.ZeroExt(L.size() - R.size(), R)
        pred = CT.cond_to_z3(name, L, R, z3)
        return z3.If(pred, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))
    return _shared_fallback_body(tree, name, kids, atoms, widen_cache,
                                  to_z3_v2b, None)


def _fallback_with_prov(tree, name, kids, atoms, prov, widen_cache):
    import condition_table as CT

    if name in CT.COND_OPS:
        L, R = kids[0], kids[1]
        if L.size() != R.size():
            if L.size() < R.size():
                L = z3.ZeroExt(R.size() - L.size(), L)
            else:
                R = z3.ZeroExt(L.size() - R.size(), R)
        pred = CT.cond_to_z3(name, L, R, z3)
        return z3.If(pred, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))
    return _shared_fallback_body(tree, name, kids, atoms, widen_cache,
                                  to_z3_with_prov_v2b, prov)


def _shared_fallback_body(tree, name, kids, atoms, widen_cache,
                           recurse, prov):
    """the part of expr_to_canon.to_z3_with_prov's rewrite table that
    is IDENTICAL whether or not provenance is being tracked -- And/Or/
    Xor/Add/Sub/Not/shifts/zx/sx/ex/32HLto64/ite/ins@N/final opaque.
    `prov` is None in the no-provenance case; every write to it is
    guarded."""
    if name in ("And32", "And64", "And8"):
        return kids[0] & kids[1]
    if name in ("Or32", "Or64", "Or8"):
        return kids[0] | kids[1]
    if name in ("Xor32", "Xor64", "Xor8"):
        return kids[0] ^ kids[1]
    if name in ("Add32", "Add64"):
        return kids[0] + kids[1]
    if name in ("Sub32", "Sub64", "Sub8"):
        return kids[0] - kids[1]
    if name in ("Not32", "Not64", "Not8"):
        return ~kids[0]
    if name in ("Sar32", "Sar64", "Shr32", "Shr64", "Shl32", "Shl64",
                "Shl8"):
        val, amt = kids[0], kids[1]
        if amt.size() != val.size():
            if val.size() > amt.size():
                amt = z3.ZeroExt(val.size() - amt.size(), amt)
            else:
                amt = z3.Extract(val.size() - 1, 0, amt)
        if name.startswith("Sar"):
            return val >> amt
        if name.startswith("Shr"):
            return z3.LShR(val, amt)
        return val << amt
    if name.startswith("zx"):
        outw = int(name[2:])
        inw = kids[0].size()
        if outw > inw:
            return z3.ZeroExt(outw - inw, kids[0])
        return kids[0]
    if name.startswith("sx"):
        outw = int(name[2:])
        inw = kids[0].size()
        if outw > inw:
            return z3.SignExt(outw - inw, kids[0])
        return kids[0]
    if name.startswith("ex"):
        import re
        m = re.match(r"ex(\d+)@(\d+)$", name)
        width, off = int(m.group(1)), int(m.group(2))
        child = kids[0]
        need = off + width
        if need > child.size():
            ck = (id(child), need)
            if ck not in widen_cache:
                extra = need - child.size()
                nm = "pad_%d" % len(widen_cache)
                pad = z3.BitVec(nm, extra)
                if prov is not None:
                    prov[nm] = ("call", "<width-pad for %r>" %
                                serialize(tree))
                widen_cache[ck] = z3.Concat(pad, child)
            child = widen_cache[ck]
        return z3.Extract(off + width - 1, off, child)
    if name == "32HLto64":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name == "ite":
        cond_bit = kids[0]
        return z3.If(cond_bit == z3.BitVecVal(1, cond_bit.size()),
                      kids[1], kids[2])
    if name.startswith("ins@"):
        import re
        m = re.match(r"ins@(\d+)$", name)
        off = int(m.group(1))
        base, val = kids[0], kids[1]
        w, vw = base.size(), val.size()
        if off + vw > w:
            raise ValueError(
                "ins@%d: inserted value width %d at offset %d "
                "exceeds base width %d" % (off, vw, off, w))
        widened_val = z3.ZeroExt(w - vw, val) if w > vw else val
        if off:
            widened_val = widened_val << off
        mask = ((1 << vw) - 1) << off
        cleared = base & z3.BitVecVal((~mask) & ((1 << w) - 1), w)
        return cleared | widened_val

    text = serialize(tree)
    w = 64
    if text not in atoms:
        nm = "op_%d" % len(atoms)
        atoms[text] = z3.BitVec(nm, w)
        if prov is not None:
            prov[nm] = ("call", text)
    return atoms[text]
