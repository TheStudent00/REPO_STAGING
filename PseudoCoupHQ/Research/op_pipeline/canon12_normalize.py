#!/usr/bin/env python3
"""canon12_normalize.py -- STAGE 2's z3 MODEL for the wide-arithmetic
VEX call atoms tree_match2/expr_to_canon leave opaque (measured
population, canon11_units_<lang>.json's own reasons: Mul64 20, Mul32
1, DivModU128to64 12, DivModS128to64 8, plus 20 more that show as the
synthetic `<width-pad for ...>` atom -- the REMAINDER half of a
DivModX128to64 call, see below for why).

Per AgentMemory's evidence doctrine ("forced by construction"): every
addition below is checked against this corpus's OWN real ship code
before being trusted, not asserted from the VEX op's name alone (see
this lap's report for the c/op_175, c/op_211/212/217/218/247/248
worked traces).

FOUR ADDITIONS, each to the SAME small rewrite table `to_z3_fixed`/
`to_z3_with_prov` already carry (And32/Or32/.../32HLto64/ite/ins@N):

1. `Mul64(A,B)` / `Mul32(A,B)` -- MEASURED (canon4_units's own `mnem`
   for all 21 units carrying this atom, both langs) to be a PLAIN
   TRUNCATING multiply: real ship code is always the 2-operand
   `imul S,D` form, never the 1-operand `mul`/`imul` (which alone
   needs %rdx) -- e.g. c/op_175 (`a*b`, a:int32_t widened to int64_t,
   b:int64_t): `movslq %edi,%rax; imul %rsi,%rax; ret`. z3's own
   bitvector multiply (`a * b`, decl `bvmul`) truncates to the
   operand width by construction, exactly matching -- so this is a
   ONE-LINE addition, `return kids[0] * kids[1]`, the SAME shape
   Add64/Sub64 already get. gen7/gen11's EXISTING `bvmul` -> `imul`
   ALU_OP entry renders it with NO new codegen at all.

2. `64HLto128(HI, LO)` -- z3 `Concat(HI, LO)`, the 128-bit sibling of
   the ALREADY-PRESENT `32HLto64` rule (same shape, wider).

3. `DivModS128to64(dividend128, divisor64)` -- z3-MODELED as true
   128-bit division: divisor sign-extended to 128 bits
   (`z3.SignExt(64, divisor64)`), quotient = 128-bit signed division
   (z3's `/` on BitVecs, decl `bvsdiv_i`, TRUNCATING toward zero --
   verified: `z3.simplify(BitVecVal(-7,8) / BitVecVal(2,8))` = -3,
   matching x86 `idiv`, not floor), remainder = `z3.SRem` (decl
   `bvsrem_i`, sign-of-dividend, TRUNCATING -- verified:
   `z3.simplify(z3.SRem(BitVecVal(-7,8), BitVecVal(2,8)))` = -1;
   Python's own `%` operator on z3 BitVecs is NOT this -- it maps to
   `bvsmod`, FLOORED, sign-of-divisor, the WRONG remainder for x86
   `idiv` -- caught by direct experiment before use, not assumed).
   Both halves truncated back to 64 bits and re-packed as
   `Concat(remainder64, quotient64)` -- LOW 64 = quotient, HIGH 64 =
   remainder, matching the observed VEX convention (`ex64@0(...)` is
   always `/`'s own callers, `ex64@64(...)` is always `%`'s).

4. `DivModU128to64` -- the same shape, unsigned (`z3.ZeroExt`,
   `z3.UDiv`, `z3.URem`).

WHY THE "<width-pad for ...>" BUCKET (20 units) IS THE SAME DEFECT,
NOT A SEPARATE ONE: `DivModX128to64(...)`, left opaque, is bound to a
z3 atom of the GENERIC DEFAULT WIDTH (64 bits -- `to_z3_with_prov`'s
own fallback for any unrecognized call). `ex64@0(...)` (the quotient
half, `/`) happens to ask for exactly that atom's own 64 bits, so it
reads back correctly BY ACCIDENT -- this is why DivModS128to64/
DivModU128to64 show as clean single-atom refusals today. `ex64@64(...)`
(the remainder half, `%`) asks for bits [127:64] of something z3
believes is only 64 bits wide, so `to_z3_with_prov`'s own CAUSE-3
padding kicks in and manufactures a FRESH, MEANINGLESS, UNCONSTRAINED
64-bit atom (`pad_N`) carrying NONE of the real dividend/divisor
information -- hence the synthetic "<width-pad for ...>" name. Once
DivModX128to64 is modeled as a real 128-bit z3 value (point 3/4
above), both halves read out correctly with no padding involved.

USAGE: this module is a MODEL, imported by canon12_render.py (the
renderer half) and canon12.py (the driver); it does not touch
tree_match2.py, expr_to_canon.py, or canon7_render.py -- new file,
per this lap's brief.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402
import expr_to_canon as EC0                                     # noqa: E402
import z3                                                       # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize
leaf_width = TM.leaf_width

WIDE_MUL_OPS = set(["Mul64", "Mul32"])
WIDE_DIVMOD_OPS = set(["DivModS128to64", "DivModU128to64"])

# JOB 2 FIX (job2_remaining_refusals_report.txt's own PART B diagnosis,
# swift's 8 Int32-vs-UInt64 units, e.g. swift/296): the six SIGNED
# CondXX ops -- these are the only members of CT.COND_OPS whose
# predicate depends on the operand's SIGN, so they are the only ones a
# zero-extension can silently break (CondEQ/CondNE/CondULT/CondUGE/
# CondUGT/CondULE are all preserved exactly under zero-extension --
# zx64(a) == zx64(b) iff a == b, zx64(a) u< zx64(b) iff a u< b -- so
# leaving THOSE untouched is not an oversight, it is the correct,
# already-proven-safe case).
SIGNED_COND_OPS = frozenset([
    "CondSLT", "CondSGE", "CondSLE", "CondSGT", "CondSGN", "CondNSGN",
])


def _signed_operand(argtree, kid_val, atoms, prov, widen_cache):
    """THE BUG (job2_remaining_refusals_report.txt PART B, forced by
    construction, swift/op_296's own raw text): VEX always stores
    amd64g_calculate_condition's cc_dep1/cc_dep2 ZERO-extended to 64
    bits in the guest state regardless of the REAL operation width (the
    width lives in cc_op, which this rewrite discards -- CT.COND_OPS
    substitution only ever keeps cond/dep1/dep2). For an UNSIGNED or
    EQUALITY condition that zero-extension is harmless (see
    SIGNED_COND_OPS's own comment). For a SIGNED condition it is fatal:
    `0 >s zero_extend_64(a)` can NEVER be true for any `a`, because a
    zero-extended 64-bit value's own bit 63 is always 0 -- exactly the
    always-false sign test job2_remaining_refusals_report.txt's PART B
    found rendered for swift/296 (`a` is Int32; real ship reads `a`'s
    OWN sign bit directly, `test %edi,%edi; sets`).

    THE FIX: when `argtree` is STRUCTURALLY a zero-extension node
    (`zx<W>(inner)`, W the storage width, inner the real operand at its
    OWN true width), a signed comparison must read inner's OWN sign
    bit, not always-0. Re-deriving inner and SIGN-extending it instead
    of zero-extending is exactly that: SignExt propagates inner's own
    top bit (its real sign) into every bit above it, so the resulting
    64-bit value's OWN sign (bit 63) equals inner's sign at its real
    width -- provably order-preserving for signed comparison (a
    standard property of sign extension), and it changes NOTHING for
    any operand that is not itself a zx-wrapper (every already-
    converged unit's own shape -- this is a pure ADDITION, gated on a
    structural pattern this corpus's prior generations never triggered
    for any unit that already converged, so it cannot regress one)."""
    if argtree[0] == "leaf":
        return kid_val
    name = argtree[1]
    if not name.startswith("zx"):
        return kid_val
    outw = int(name[2:])
    inner_tree = argtree[2][0]
    inner_val = to_z3_with_prov_v2(inner_tree, atoms, prov, widen_cache)
    inw = inner_val.size()
    if outw <= inw:
        return kid_val
    return z3.SignExt(outw - inw, inner_val)


def _wide_divmod(name, kids):
    dividend128, divisor64 = kids
    if name == "DivModS128to64":
        divisor128 = z3.SignExt(64, divisor64)
        q = dividend128 / divisor128
        r = z3.SRem(dividend128, divisor128)
    else:
        divisor128 = z3.ZeroExt(64, divisor64)
        q = z3.UDiv(dividend128, divisor128)
        r = z3.URem(dividend128, divisor128)
    q64 = z3.Extract(63, 0, q)
    r64 = z3.Extract(63, 0, r)
    return z3.Concat(r64, q64)


def to_z3_v2(tree, atoms, widen_cache=None):
    """tree_match2.to_z3_fixed, plus the four additions above -- used
    to compute the STORED normal_path_root text (no provenance
    needed)."""
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
    kids = [to_z3_v2(a, atoms, widen_cache) for a in args]

    if name in WIDE_MUL_OPS:
        return kids[0] * kids[1]
    if name == "64HLto128":
        hi, lo = kids
        return z3.Concat(hi, lo)
    if name in WIDE_DIVMOD_OPS:
        return _wide_divmod(name, kids)

    prov = {}
    return _fallback_with_prov(tree, name, kids, atoms, prov,
                                widen_cache)


def normalize_v2(expr_text):
    """tree_match2.normalize, pointed at to_z3_v2."""
    tree = parse_expr(expr_text)
    try:
        atoms = {}
        e = to_z3_v2(tree, atoms)
        simplified = z3.simplify(e)
        return str(simplified).replace("\n", " ").strip(), True, \
            "z3 simplify (STAGE 2 wide-arithmetic model)"
    except Exception as exc:
        return expr_text, False, "z3 failed: %r" % exc


def to_z3_with_prov_v2(tree, atoms, prov, widen_cache=None):
    """expr_to_canon.to_z3_with_prov, plus the four additions -- used
    by the RENDERER's own self-consistency re-derivation (needs
    provenance so gen7/gen12 can trace leaves back to a/b)."""
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
    kids = [to_z3_with_prov_v2(a, atoms, prov, widen_cache)
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


def _fallback_with_prov(tree, name, kids, atoms, prov, widen_cache):
    """everything expr_to_canon.to_z3_with_prov already knows how to
    do (CAUSE 1 conditions, And/Or/Xor/Add/Sub/Not, shifts, zx/sx/ex,
    32HLto64, ite, ins@N, and the final opaque-call fallback) -- a
    faithful re-port, since that function is not itself callable as
    "everything after the point my new cases would have matched"."""
    import condition_table as CT

    if name in CT.COND_OPS:
        L, R = kids[0], kids[1]
        if name in SIGNED_COND_OPS:
            # JOB 2 FIX -- see _signed_operand's own docstring.
            L = _signed_operand(tree[2][0], L, atoms, prov, widen_cache)
            R = _signed_operand(tree[2][1], R, atoms, prov, widen_cache)
            if L.size() != R.size():
                if L.size() < R.size():
                    L = z3.SignExt(R.size() - L.size(), L)
                else:
                    R = z3.SignExt(L.size() - R.size(), R)
        elif L.size() != R.size():
            if L.size() < R.size():
                L = z3.ZeroExt(R.size() - L.size(), L)
            else:
                R = z3.ZeroExt(L.size() - R.size(), R)
        pred = CT.cond_to_z3(name, L, R, z3)
        return z3.If(pred, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))
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
                prov[nm] = ("call", "<width-pad for %r>" % serialize(
                    tree))
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
        prov[nm] = ("call", text)
    return atoms[text]
