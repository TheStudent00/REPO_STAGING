#!/usr/bin/env python3
"""vex_names.py -- JOB 1 (log_082 lap): THE GENERIC NAME TRANSLATOR for
VEX's SIMD-float lifter names.

WHY THIS FILE EXISTS. tree_match2.py's `to_z3_fixed` is an IF-CHAIN:
one hand-written branch per VEX op name, and anything not in that small
ratified set falls through to a single opaque, 64-bit-defaulted atom
(tree_match2.py's own generic fallback, unchanged, reused verbatim
below). Twelve of the seventeen names blocking convergence today are
NOT irregular helper calls -- they are a small, closed, PARSEABLE
family: <Op><Width>F0x<Lanes> for Add/Sub/Mul/Div and CmpEQ (add/sub/
mul/div/compare, 32-bit or 64-bit float, lane 0 of 4 or 2), plus the
whole-register bitwise trio Xor/Or/AndV128. This file PARSES the name
pattern once and builds the z3 term generically, instead of adding five
more copy-pasted branches to the if-chain.

THE SEMANTICS, stated once so both builders below can be checked
against it:

  LANE ARITHMETIC / LANE COMPARE (Add/Sub/Mul/Div/CmpEQ at 32F0x4 or
  64F0x2): these are the VEX lift of a SCALAR SSE instruction (addss/
  subss/mulss/divss/cmpeqss and their sd twins) -- the instruction
  writes ONLY lane 0 of the destination and leaves the destination's
  OWN upper lanes untouched. The term is therefore
      Concat(Extract(127, width, first_operand), computed_lane)
  never a full 128-bit recompute. real z3 FPA (fpBVToFP to read a lane
  as a float, fpAdd/fpSub/fpMul/fpDiv at round-nearest-even for
  arithmetic, fpEQ + fpIsNaN for compare, fpToIEEEBV to write the
  result back as raw bits) -- the same approach canon20_behaviour_
  check.py already uses for its own ground-truth gate.

  WHOLE-REGISTER BITWISE (XorV128/OrV128/AndV128): NOT lane ops. Real
  hardware's xorps/orps/andps operate on the FULL 128 bits of both
  operands (the float sign-mask idiom -- XOR against a sign-bit mask
  to negate a float -- and VEX's own "NOT of a packed compare mask via
  XOR with an all-ones constant" idiom, see the CMPNEQ COMPOUND below).

THE DICTIONARY DISPATCH. `to_z3_v3` below is tree_match2.to_z3_fixed's
if-chain, reimplemented as NAME -> BUILDER dispatch (a dict for exact
names, still pattern-parsed for the prefix families that were always
pattern-parsed: zx*/sx*/ex*/ins@*, since those carry a width or offset
IN the name and cannot be dict keys). Every existing behaviour is
IDENTICAL -- same eager kids-first evaluation order, same shift width
coercion, same ex*/ins@* widen-with-fresh-bits discipline (CAUSE 3's
own reasoning, reused verbatim: never zero-extend an under-width
opaque atom, that would fabricate a fact this normalizer does not
know), same CondXX routing through condition_table.py. Only the
generic float-lane/bitwise dispatch and the dict shape are new.

A SECOND WALKER, for rendering (`to_z3_atoms_v3`). Computing the FPA
term directly (as `to_z3_v3` does) is right for NORMALIZATION/matching
(tree_match4.py's own job) but wrong for RENDERING: there is no way to
walk a raw z3 FPA term back into an addss/cmpeqss instruction generically
the way gen7/gen14 walk native BV operators. So `to_z3_atoms_v3` is the
SAME dispatch, except each lane-arith/lane-compare/whole-register-
bitwise node becomes an OPAQUE PROVENANCE ATOM instead of a computed
term -- the SAME "atom now, resolved to instructions only at render
time" discipline condition_table4.py's own FCxx atoms and canon22_
float.py's own to_z3_with_prov_v2e already use for the ucomisd/ucomiss
family. canon24.py's render pipeline consumes this walker's `prov`
dict; canon24.py's own header explains the render side.

THE CMPNEQ COMPOUND. `XorV128(all-ones-at-lane-width, CmpEQ...(P,Q))`
is VEX's OWN lowering of a single real `cmpneqss`/`cmpneqsd`
instruction -- not two operations, one ("NOT of the packed-equal
mask" is how VEX represents a not-equal compare; measured directly,
canon24.py's own report). `to_z3_atoms_v3` recognizes this shape
BEFORE descending, so the whole compound becomes ONE atom, never a
bitwise-xor atom wrapping a separate compare atom.

THE SPELLING BAN: this file parses and builds z3 TERMS from VEX op
NAMES (Add32F0x4, CmpEQ64F0x2, XorV128, ...) -- it does not group,
pair, key, or select UNITS by anything; the "operator" field is never
read here. Nothing here is a matching-shaped file (no grouping/pairing
of units happens in this module), so check_no_spelling_keys.py's own
guard does not apply to its own output (it has none -- see canon24.py
and vex_names_census.py for the artifacts that DO carry candidate rows
and DO run the guard).

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import condition_table as CT                                    # noqa: E402
import condition_table6 as CT6                                  # noqa: E402
import z3                                                        # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize
leaf_width = TM.leaf_width

F32 = z3.Float32()
F64 = z3.Float64()
RM = z3.RNE()

REG_WIDTH = 128     # every lane-arith/lane-compare/whole-bitwise op in
                     # this family lives in a 128-bit xmm register

LANE_ARITH_RE = re.compile(r"^(Add|Sub|Mul|Div)(32|64)F0x(\d+)$")
LANE_CMP_RE = re.compile(r"^Cmp(EQ)(32|64)F0x(\d+)$")
BITWISE_V128 = {
    "XorV128": lambda a, b: a ^ b,
    "OrV128": lambda a, b: a | b,
    "AndV128": lambda a, b: a & b,
}

EX_RE = re.compile(r"ex(\d+)@(\d+)$")
INS_RE = re.compile(r"ins@(\d+)$")
LEAF_INT_RE = re.compile(r"^(\d+):(\d+)$")


# --------------------------------------------------------------------
# operand classification: condition_table6.classify_operand, extended
# with the bare (no zx128 wrapper) 128-bit constant-load shape -- used
# when the enclosing op is already 128-bit wide (e.g. XorV128's own
# sign-mask operand), so the value never needs zero-extending up from
# a narrower load the way the packed-arithmetic family's own 32/64-bit
# consts do.
# --------------------------------------------------------------------

def classify_operand_ext(tree):
    op = CT6.classify_operand(tree)
    if op is not None:
        return op
    if tree[0] == "node" and tree[1].startswith("ld") and \
            "/g0" in tree[1]:
        return ("const", None)
    return None


# --------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------

def ensure_width(bv, need, widen_cache):
    """Widen `bv` up to `need` bits with FRESH, INDEPENDENT,
    uninterpreted high bits when it arrives narrower than the register
    this op lives in -- the SAME discipline tree_match2.py's own CAUSE
    3 fix uses for under-width opaque atoms under an `ex` extraction:
    never zero-extend (that fabricates "the missing bits are 0", a
    fact this normalizer does not know), widen with a fresh atom
    instead, memoized per (child identity, needed width) so the SAME
    sub-tree widened twice gets the SAME extra bits both times."""
    if bv.size() >= need:
        return bv
    key = (id(bv), need)
    if key not in widen_cache:
        extra = need - bv.size()
        pad = z3.BitVec("pad_%d" % len(widen_cache), extra)
        widen_cache[key] = z3.Concat(pad, bv)
    return widen_cache[key]


def _fp_of(raw, width):
    sort = F32 if width == 32 else F64
    return z3.fpBVToFP(z3.Extract(width - 1, 0, raw), sort)


def _leaf_int_value(text):
    m = LEAF_INT_RE.match(text)
    if m is None:
        return None
    return int(m.group(1))


# --------------------------------------------------------------------
# generic term builders -- computed FPA terms (used by to_z3_v3, the
# NORMALIZATION-only walker; see to_z3_atoms_v3 below for the render-
# side atom+provenance twin).
# --------------------------------------------------------------------

def build_lane_arith(op, width, kids, widen_cache):
    a = ensure_width(kids[0], REG_WIDTH, widen_cache)
    b = ensure_width(kids[1], REG_WIDTH, widen_cache)
    a_lane = _fp_of(a, width)
    b_lane = _fp_of(b, width)
    if op == "Add":
        rv = z3.fpAdd(RM, a_lane, b_lane)
    elif op == "Sub":
        rv = z3.fpSub(RM, a_lane, b_lane)
    elif op == "Mul":
        rv = z3.fpMul(RM, a_lane, b_lane)
    else:
        rv = z3.fpDiv(RM, a_lane, b_lane)
    lane_bits = z3.fpToIEEEBV(rv)
    upper = z3.Extract(REG_WIDTH - 1, width, a)
    return z3.Concat(upper, lane_bits)


def build_lane_cmp(width, kids, widen_cache):
    a = ensure_width(kids[0], REG_WIDTH, widen_cache)
    b = ensure_width(kids[1], REG_WIDTH, widen_cache)
    a_lane = _fp_of(a, width)
    b_lane = _fp_of(b, width)
    truth = z3.And(
        z3.Not(z3.Or(z3.fpIsNaN(a_lane), z3.fpIsNaN(b_lane))),
        z3.fpEQ(a_lane, b_lane))
    lane_bits = z3.If(truth, z3.BitVecVal((1 << width) - 1, width),
                       z3.BitVecVal(0, width))
    upper = z3.Extract(REG_WIDTH - 1, width, a)
    return z3.Concat(upper, lane_bits)


def build_bitwise_v128(op, kids, widen_cache):
    a = ensure_width(kids[0], REG_WIDTH, widen_cache)
    b = ensure_width(kids[1], REG_WIDTH, widen_cache)
    return BITWISE_V128[op](a, b)


# --------------------------------------------------------------------
# the pre-existing small ratified rewrite set, reimplemented as
# dictionary dispatch. Every entry here is tree_match2.to_z3_fixed's
# OWN logic, verbatim -- see that file for the CAUSE 1/2/3 history
# each shape carries.
# --------------------------------------------------------------------

def _and(kids, wc):
    return kids[0] & kids[1]


def _or(kids, wc):
    return kids[0] | kids[1]


def _xor(kids, wc):
    return kids[0] ^ kids[1]


def _add(kids, wc):
    return kids[0] + kids[1]


def _sub(kids, wc):
    return kids[0] - kids[1]


def _not(kids, wc):
    return ~kids[0]


def _concat_32hlto64(kids, wc):
    hi, lo = kids
    return z3.Concat(hi, lo)


def _shift_sar(kids, wc):
    return _shift_common(kids, "sar")


def _shift_shr(kids, wc):
    return _shift_common(kids, "shr")


def _shift_shl(kids, wc):
    return _shift_common(kids, "shl")


def _shift_common(kids, kind):
    val, amt = kids[0], kids[1]
    if amt.size() != val.size():
        if val.size() > amt.size():
            amt = z3.ZeroExt(val.size() - amt.size(), amt)
        else:
            amt = z3.Extract(val.size() - 1, 0, amt)
    if kind == "sar":
        return val >> amt
    if kind == "shr":
        return z3.LShR(val, amt)
    return val << amt


EXACT_DISPATCH = {}
for _n in ("And32", "And64", "And8"):
    EXACT_DISPATCH[_n] = _and
for _n in ("Or32", "Or64", "Or8"):
    EXACT_DISPATCH[_n] = _or
for _n in ("Xor32", "Xor64", "Xor8"):
    EXACT_DISPATCH[_n] = _xor
for _n in ("Add32", "Add64"):
    EXACT_DISPATCH[_n] = _add
for _n in ("Sub32", "Sub64", "Sub8"):
    EXACT_DISPATCH[_n] = _sub
for _n in ("Not32", "Not64", "Not8"):
    EXACT_DISPATCH[_n] = _not
EXACT_DISPATCH["32HLto64"] = _concat_32hlto64
for _n in ("Sar32", "Sar64"):
    EXACT_DISPATCH[_n] = _shift_sar
for _n in ("Shr32", "Shr64"):
    EXACT_DISPATCH[_n] = _shift_shr
for _n in ("Shl32", "Shl64", "Shl8"):
    EXACT_DISPATCH[_n] = _shift_shl


def _build_cond(name, kids):
    L, R = kids[0], kids[1]
    if L.size() != R.size():
        if L.size() < R.size():
            L = z3.ZeroExt(R.size() - L.size(), L)
        else:
            R = z3.ZeroExt(L.size() - R.size(), R)
    pred = CT.cond_to_z3(name, L, R, z3)
    return z3.If(pred, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))


def _build_zx(name, kids):
    outw = int(name[2:])
    inw = kids[0].size()
    return z3.ZeroExt(outw - inw, kids[0]) if outw > inw else kids[0]


def _build_sx(name, kids):
    outw = int(name[2:])
    inw = kids[0].size()
    return z3.SignExt(outw - inw, kids[0]) if outw > inw else kids[0]


def _build_ex(name, kids, widen_cache):
    m = EX_RE.match(name)
    width, off = int(m.group(1)), int(m.group(2))
    child = kids[0]
    need = off + width
    if need > child.size():
        ck = (id(child), need)
        if ck not in widen_cache:
            extra = need - child.size()
            pad = z3.BitVec("pad_%d" % len(widen_cache), extra)
            widen_cache[ck] = z3.Concat(pad, child)
        child = widen_cache[ck]
    return z3.Extract(off + width - 1, off, child)


def _build_ite(kids):
    cond_bit = kids[0]
    return z3.If(cond_bit == z3.BitVecVal(1, cond_bit.size()),
                  kids[1], kids[2])


def _build_ins(name, kids):
    m = INS_RE.match(name)
    off = int(m.group(1))
    base, val = kids[0], kids[1]
    w, vw = base.size(), val.size()
    if off + vw > w:
        raise ValueError(
            "ins@%d: inserted value width %d at offset %d exceeds "
            "base width %d" % (off, vw, off, w))
    widened_val = z3.ZeroExt(w - vw, val) if w > vw else val
    if off:
        widened_val = widened_val << off
    mask = ((1 << vw) - 1) << off
    cleared = base & z3.BitVecVal((~mask) & ((1 << w) - 1), w)
    return cleared | widened_val


# --------------------------------------------------------------------
# to_z3_v3: THE GENERIC TRANSLATOR (JOB 1's headline deliverable).
# Dictionary dispatch for the pre-existing set, PLUS name-pattern
# parsing (LANE_ARITH_RE / LANE_CMP_RE / BITWISE_V128) for the twelve
# SIMD-float names, computed as REAL z3 FPA terms. Used for
# normalization (tree_match4.py); see to_z3_atoms_v3 for the render-
# side twin.
# --------------------------------------------------------------------

def to_z3_v3(tree, atoms, widen_cache=None):
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
    kids = [to_z3_v3(a, atoms, widen_cache) for a in args]

    if name in CT.COND_OPS:
        return _build_cond(name, kids)

    builder = EXACT_DISPATCH.get(name)
    if builder is not None:
        return builder(kids, widen_cache)

    m = LANE_ARITH_RE.match(name)
    if m is not None:
        return build_lane_arith(m.group(1), int(m.group(2)), kids,
                                 widen_cache)

    m = LANE_CMP_RE.match(name)
    if m is not None:
        return build_lane_cmp(int(m.group(2)), kids, widen_cache)

    if name in BITWISE_V128:
        return build_bitwise_v128(name, kids, widen_cache)

    if name.startswith("zx"):
        return _build_zx(name, kids)
    if name.startswith("sx"):
        return _build_sx(name, kids)
    if name.startswith("ex"):
        return _build_ex(name, kids, widen_cache)
    if name == "ite":
        return _build_ite(kids)
    if name.startswith("ins@"):
        return _build_ins(name, kids)

    text = serialize(tree)
    w = 64
    if text not in atoms:
        atoms[text] = z3.BitVec("op_%d" % len(atoms), w)
    return atoms[text]


def normalize_v3(expr_text):
    """tree_match2.py's own normalize(), pointed at to_z3_v3."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        e = to_z3_v3(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (vex_names.py: dictionary dispatch, generic " \
            "SIMD-float lane/bitwise name parsing, real z3 FPA)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc


# --------------------------------------------------------------------
# to_z3_atoms_v3: THE RENDER-SIDE TWIN. Same dispatch, except the
# lane-arith / lane-compare / whole-register-bitwise families become
# OPAQUE PROVENANCE ATOMS instead of computed FPA terms (see file
# header for why); canon24.py's render pipeline resolves each atom's
# `prov` payload back into real SSE instructions.
# --------------------------------------------------------------------

def _match_cmpneq_compound(args):
    """args = XorV128(...)'s own two arguments. (cmp_node, match) if
    one side is a bare integer leaf equal to all-ones AT THE OTHER
    SIDE'S OWN LANE WIDTH and the other side is a CmpEQ... node --
    VEX's own not-equal lowering (see file header). Checks both
    argument orders rather than assuming VEX's own measured order is
    the only one."""
    for i, j in ((0, 1), (1, 0)):
        mask_arg, cmp_arg = args[i], args[j]
        if cmp_arg[0] != "node":
            continue
        m = LANE_CMP_RE.match(cmp_arg[1])
        if m is None:
            continue
        if mask_arg[0] != "leaf":
            continue
        lit = _leaf_int_value(mask_arg[1])
        if lit is None:
            continue
        width = int(m.group(2))
        if lit == (1 << width) - 1:
            return cmp_arg, m
    return None


def _fcmpmask_atom(cmp_node, m, cond, atoms, prov):
    text = serialize(cmp_node)
    key = ("fcmpmask", cond, text)
    if key not in atoms:
        width = int(m.group(2))
        nm = "fc_%d" % len(atoms)
        atoms[key] = z3.BitVec(nm, REG_WIDTH)
        p_operand = classify_operand_ext(cmp_node[2][0])
        q_operand = classify_operand_ext(cmp_node[2][1])
        prov[nm] = ("fcmpmask", dict(
            cond=cond, precision=width,
            p_operand=p_operand, q_operand=q_operand,
            p_text=serialize(cmp_node[2][0]),
            q_text=serialize(cmp_node[2][1])))
    return atoms[key]


def _farith_atom(tree, m, atoms, prov):
    text = serialize(tree)
    key = ("farith", text)
    if key not in atoms:
        op, width = m.group(1), int(m.group(2))
        nm = "fa_%d" % len(atoms)
        atoms[key] = z3.BitVec(nm, REG_WIDTH)
        p_operand = classify_operand_ext(tree[2][0])
        q_operand = classify_operand_ext(tree[2][1])
        prov[nm] = ("farith", dict(
            op=op, precision=width,
            p_operand=p_operand, q_operand=q_operand,
            p_text=serialize(tree[2][0]),
            q_text=serialize(tree[2][1])))
    return atoms[key]


def _vbitwise_atom(tree, atoms, prov):
    text = serialize(tree)
    key = ("vbitwise", text)
    if key not in atoms:
        nm = "vb_%d" % len(atoms)
        atoms[key] = z3.BitVec(nm, REG_WIDTH)
        p_operand = classify_operand_ext(tree[2][0])
        q_operand = classify_operand_ext(tree[2][1])
        prov[nm] = ("vbitwise", dict(
            op=tree[1],
            p_operand=p_operand, q_operand=q_operand,
            p_text=serialize(tree[2][0]),
            q_text=serialize(tree[2][1])))
    return atoms[key]


def to_z3_atoms_v3(tree, atoms, prov, widen_cache=None):
    if widen_cache is None:
        widen_cache = {}
    kind = tree[0]
    if kind == "leaf":
        text = tree[1]
        w = leaf_width(text)
        key = text
        if key not in atoms:
            nm = "atom_%d" % len(atoms)
            atoms[key] = z3.BitVec(nm, w)
            prov[nm] = ("leaf", key)
        return atoms[key]

    name, args = tree[1], tree[2]

    if name == "XorV128" and len(args) == 2:
        compound = _match_cmpneq_compound(args)
        if compound is not None:
            cmp_node, cmp_m = compound
            return _fcmpmask_atom(cmp_node, cmp_m, "ne", atoms, prov)

    m = LANE_CMP_RE.match(name)
    if m is not None:
        return _fcmpmask_atom(tree, m, "eq", atoms, prov)

    m = LANE_ARITH_RE.match(name)
    if m is not None:
        return _farith_atom(tree, m, atoms, prov)

    if name in BITWISE_V128:
        return _vbitwise_atom(tree, atoms, prov)

    kids = [to_z3_atoms_v3(a, atoms, prov, widen_cache) for a in args]

    if name in CT.COND_OPS:
        return _build_cond(name, kids)
    builder = EXACT_DISPATCH.get(name)
    if builder is not None:
        return builder(kids, widen_cache)
    if name.startswith("zx"):
        return _build_zx(name, kids)
    if name.startswith("sx"):
        return _build_sx(name, kids)
    if name.startswith("ex"):
        return _build_ex(name, kids, widen_cache)
    if name == "ite":
        return _build_ite(kids)
    if name.startswith("ins@"):
        return _build_ins(name, kids)

    text = serialize(tree)
    w = 64
    if text not in atoms:
        nm = "op_%d" % len(atoms)
        atoms[text] = z3.BitVec(nm, w)
        prov[nm] = ("call", text)
    return atoms[text]


def normalize_atoms_v3(expr_text):
    """Render-side normalizer -- MUST be called before render_unit7
    (canon24.py's own driver does this), since render_unit7 re-derives
    via to_z3_atoms_v3 and refuses if the re-derivation does not match
    the stored normal_path_root text byte-for-byte."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        prov = {}
        e = to_z3_atoms_v3(tree, atoms, prov)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (vex_names.py atom+provenance dispatch, " \
            "render-ready)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc


REGULAR_NAME_PATTERNS = (LANE_ARITH_RE, LANE_CMP_RE)


def is_regular_name(name):
    """True if `name` is parseable by this file's own generic
    dispatch (the lane-arith/lane-compare family by pattern, or the
    whole-register-bitwise trio by exact membership) -- JOB 2's own
    definition of "regular", used by vex_names_census.py."""
    if name in BITWISE_V128:
        return True
    for pat in REGULAR_NAME_PATTERNS:
        if pat.match(name):
            return True
    return False
