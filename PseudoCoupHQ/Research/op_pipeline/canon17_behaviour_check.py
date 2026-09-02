#!/usr/bin/env python3
"""canon17_behaviour_check.py -- THE GROUND-TRUTH-ANCHORED GATE,
EXTENDED WITH XMM + THE FLOAT FLAG ALGEBRA, for JOB 1/2's float
packed-flags rendering (canon17_render.py). Mirrors canon8_behaviour_
check.py's own `anchored_check` shape exactly (prove the candidate
directly against the unit's own real ship code, register-identity
pre-bound via a SHARED z3 seed) -- the difference is entirely in the
Sim: canon.py's own FAMILY_OF/WIDTH_OF table ALREADY carries
"xmm0".."xmm15" as ordinary 64-bit-wide families (confirmed by direct
read of canon.py), so `canon5_behaviour_check.Sim`'s existing
`get_family`/`read_at`/`write` machinery -- unchanged -- already
tracks an xmm register as a plain 64-bit symbolic value; this file
only teaches `exec_line` FOUR new mnemonics (`ucomisd`/`ucomiss`/
`xorps`/`xorpd`/`movd`/`movq` -- six, all reusing the inherited
read_at/write) and the FLOAT setcc dispatch (`sete`/`setne`/`setp`/
`setnp`/`setb`/`setae`/`seta`/`setbe` reading UCOMISD/UCOMISS flags,
not `cmp`/`test` flags -- see below for why these cannot share Sim8's
existing integer setcc dispatch even though the SUFFIX spellings
collide).

WHY THE FLAG ALGEBRA NEEDS ITS OWN is_nan/is_lt/is_eq, NOT z3 FPA
(condition_table4.py's header states the reasoning this file APPLIES):
this Sim never asks what makes two xmm values "NaN" or "less than" in
real IEEE754 terms. It only needs: (a) the SAME comparison (same two
OPERANDS, in one gate call) reads the SAME three booleans everywhere
it recurs (WITHIN one text -- ucomisd's flags persisting across
several setcc's) and (b) the REAL SHIP TEXT and the CANDIDATE TEXT,
compared in the SAME gate call, reference the SAME booleans for "a
vs b" / "a vs 0.0" / "b vs 0.0" even though they may use DIFFERENT
physical registers or DIFFERENT instruction forms to get there. Both
requirements are met by keying is_nan (per operand) and is_lt/is_eq
(per unordered operand PAIR, direction re-derived from the pair's own
canonical order -- see `_tag_key`/`_pair_key` below) off a STRUCTURAL
TAG ("a"/"b"/"zero"), never off which physical register or which
Python z3 object happened to carry the value -- and storing the fresh
Bool symbols in `shared_seed` (the SAME dict canon8_behaviour_check.py
already threads between its "real" and "candidate" Sim instances), so
one gate call's two simulations (real vs candidate) share identity
exactly like every other register family already does.

TAG DERIVATION (`_tag_of`): a value is "a" iff it IS xmm0's own shared
seed (the argument's pristine, nothing-written-since-entry value); "b"
iff xmm1's; "zero" iff it is a CONCRETE zero (self-XOR, `xorps
%xmmT,%xmmT` -- detected structurally at the instruction, both real
ship's own idiom and canon17_render.py's own rendering use exactly
this form, so no bit-pattern reinterpretation is needed); anything
else (an intermediate float VALUE -- a conversion, an arithmetic
result) is UNTAGGED and raises NotModeled -- an honest refusal, same
shape as every other "not yet in this file's own scope" case in this
lineage, never a guess.

THE MUTUAL-EXCLUSIVITY CONSTRAINT: `is_lt` and `is_eq` for the SAME
pair cannot both be true (no real ordered compare is both). Recorded
once per pair, in `shared_seed["fcmp_constraints"]`, and ADDED TO THE
SOLVER by `anchored_check` below before it asks z3 to prove or
disprove -- a real, if narrow, semantic fact about ANY total order,
not specific to floats, kept explicit rather than left for the
formulas to accidentally rely on.

REUSES canon8_behaviour_check.Sim8 UNCHANGED for every GP-only
mnemonic (mov/movabs/cmp/test/setcc[integer]/cmov/shr/sar/shl[masked]/
movzx/movsx/add/sub/and/or/xor/not/neg/lea/push/pop) -- this file adds
exactly the six xmm-touching mnemonics plus the float-flag setcc
dispatch, and falls back to Sim8.exec_line for everything else.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon17_behaviour_check.py (library only -- canon17.py is the driver
  that calls anchored_check())
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon8_behaviour_check as BC8                            # noqa: E402
import condition_table4 as CT4                                  # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC8.LANGS
split_operands = BC8.split_operands
NotModeled = BC8.NotModeled
real_text_of = BC8.real_text_of
real_arg_families = BC8.real_arg_families
seed_family = BC8.seed_family

FCOND_TO_SUFFIX = {
    "FCEQ": "e", "FCNE": "ne", "FCPAR": "p", "FCNPAR": "np",
    "FCULT": "b", "FCUGE": "ae", "FCUGT": "a", "FCULE": "be",
}
SUFFIX_TO_FCOND = dict(
    (v, k) for k, v in FCOND_TO_SUFFIX.items())

TAG_ORDER = ["a", "b", "zero"]


class Sim9f(BC8.Sim8):
    """canon8_behaviour_check.Sim8, plus ucomisd/ucomiss/xorps/xorpd/
    movd/movq and the float-flag setcc dispatch. See file header.

    `a_is_vector` -- canon.py's own `designated()` rule, restated:
    argument a is always the FIRST float argument's home (%xmm0) when
    a itself is a float; b shares that same register FILE (%xmm1)
    only when a is ALSO a float -- otherwise b (the ONLY float
    argument, e.g. `a:bool && b:float`) takes %xmm0 itself. Passed in
    by the caller (this file never re-derives it -- the unit's own
    recorded `meta.lhs_rep` already says whether a is a float, forced-
    by-construction evidence, not a guess)."""

    def __init__(self, shared_seed, tag, a_is_vector=True):
        BC8.Sim8.__init__(self, shared_seed, tag)
        self.last_flagsetter = None    # "int" | "float" | None
        self.last_fcc = None           # (is_nan, is_lt, is_eq), Bools
        self.a_is_vector = a_is_vector
        self.b_xmm_reg = "xmm1" if a_is_vector else "xmm0"

    def _pristine_seed(self, family):
        """the z3 symbol shared_seed[family] would hand out -- forces
        it to exist (so a comparison against a register never yet
        touched still gets a stable identity to tag against) without
        marking it as "already read" in `self.regs` (matching
        get_family's own laziness for every OTHER register)."""
        if family not in self.shared_seed:
            self.shared_seed[family] = z3.BitVec(
                "seed_%s" % family, 64)
        return self.shared_seed[family]

    def _tag_of(self, value):
        # `read_at` always wraps its result in `z3.Extract(w-1,0,...)`,
        # even at the register's own full width -- so a value that is
        # STRUCTURALLY a literal 0, or STRUCTURALLY the untouched
        # xmm0/xmm1 seed, does not compare `.eq()`-equal to a bare
        # BitVecVal/seed until the wrapping Extract is folded away.
        # z3.simplify() does exactly that (Extract of a known-width
        # value at its own full width is an identity, and z3 already
        # knows it) -- without it, EVERY read tags as "not modeled",
        # even the corpus's own plain self-XOR-to-zero idiom.
        value = z3.simplify(value)
        if z3.is_bv_value(value) and value.as_long() == 0:
            return "zero"
        if self.a_is_vector and \
                value.eq(z3.simplify(self._pristine_seed("xmm0"))):
            return "a"
        if value.eq(z3.simplify(self._pristine_seed(self.b_xmm_reg))):
            return "b"
        return None

    def _bool_seed(self, name):
        key = "fcmp_bool_%s" % name
        if key not in self.shared_seed:
            self.shared_seed[key] = z3.Bool(key)
        return self.shared_seed[key]

    def _nan_of(self, tag):
        if tag == "zero":
            return z3.BoolVal(False)
        return self._bool_seed("nan_%s" % tag)

    def _pair_lt_eq(self, tag_x, tag_y):
        """(is_lt(x,y), is_eq(x,y)) -- directional/symmetric booleans
        for the ORDERED comparison of x against y, derived from ONE
        canonical-order pair of fresh symbols so "x<y" and "y<x" (two
        different instructions, possibly in two different texts) are
        provably consistent rather than independently guessed."""
        if tag_x == tag_y:
            raise NotModeled(
                "a float comparison between two operands sharing the "
                "same tag (%r) is not modeled -- never measured in "
                "this corpus" % tag_x)
        lo, hi = sorted([tag_x, tag_y], key=TAG_ORDER.index)
        lt_lo_hi = self._bool_seed("lt_%s_%s" % (lo, hi))
        eq = self._bool_seed("eq_%s_%s" % (lo, hi))
        cons_key = "fcmp_constrained_%s_%s" % (lo, hi)
        if cons_key not in self.shared_seed:
            self.shared_seed[cons_key] = True
            constraints = self.shared_seed.setdefault(
                "fcmp_constraints", [])
            constraints.append(z3.Not(z3.And(lt_lo_hi, eq)))
        if tag_x == lo:
            return lt_lo_hi, eq
        return z3.And(z3.Not(lt_lo_hi), z3.Not(eq)), eq

    def _compute_flags(self, dst_val, src_val):
        """(is_nan, is_lt, is_eq) for `ucomisX SRC,DST` -- AT&T
        operand order, DST compared against SRC (Intel: UCOMISD
        dst,src) -- exactly condition_table4.fcond_to_z3's own three
        arguments, so the setcc dispatch below can hand them straight
        through with no reconstruction. Raises NotModeled if either
        operand cannot be tagged a/b/zero."""
        tag_dst = self._tag_of(dst_val)
        tag_src = self._tag_of(src_val)
        if tag_dst is None or tag_src is None:
            raise NotModeled(
                "ucomisd/ucomiss operand is not one of this file's "
                "own tagged values (a/b/zero) -- an intermediate "
                "float value, out of this file's own scope")
        is_nan = z3.Or(self._nan_of(tag_dst), self._nan_of(tag_src))
        is_lt, is_eq = self._pair_lt_eq(tag_dst, tag_src)
        return is_nan, is_lt, is_eq

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        if mnem in ("ucomisd", "ucomiss"):
            src, dst = split_operands(rest)
            dst_v = self.read_at(dst, 64)
            src_v = self.read_at(src, 64)
            self.last_fcc = self._compute_flags(dst_v, src_v)
            self.last_flagsetter = "float"
            return

        if mnem in ("xorps", "xorpd"):
            src, dst = split_operands(rest)
            if src == dst:
                self.write(dst, z3.BitVecVal(0, 64))
                return
            a = self.read_at(dst, 64)
            b = self.read_at(src, 64)
            self.write(dst, a ^ b)
            return

        if mnem in ("movd", "movq"):
            src, dst = split_operands(rest)
            width = 32 if mnem == "movd" else 64
            v = self.read_at(src, width)
            v = z3.ZeroExt(64 - width, v) if width < 64 else v
            self.write(dst, v)
            return

        if mnem.startswith("set") and \
                mnem[3:] in SUFFIX_TO_FCOND and \
                self.last_flagsetter == "float":
            (dst,) = split_operands(rest)
            if self.last_fcc is None:
                raise NotModeled(
                    "float setcc with no preceding ucomisd/ucomiss "
                    "in this text")
            is_nan, is_lt, is_eq = self.last_fcc
            fcond = SUFFIX_TO_FCOND[mnem[3:]]
            pred = CT4.fcond_to_z3(fcond, is_nan, is_lt, is_eq, z3)
            bit = z3.If(pred, z3.BitVecVal(1, 8), z3.BitVecVal(0, 8))
            self.write(dst, bit)
            return

        if mnem in ("cmp", "test"):
            self.last_flagsetter = "int"
            BC8.Sim8.exec_line(self, line)
            return

        BC8.Sim8.exec_line(self, line)


def anchored_check(lang, n, canon4_docs, sem_docs, candidate_text,
                    a_is_vector=True):
    """canon8_behaviour_check.anchored_check, pointed at Sim9f -- see
    that function's own docstring for the register-identity pre-
    binding this file inherits unchanged. Adds the fcmp mutual-
    exclusivity constraints (see file header) to the solver before
    checking. `a_is_vector`: see Sim9f's own docstring -- the caller's
    own recorded meta.lhs_rep says whether argument a is a float."""
    real_text = real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this " \
            "unit (canon4_units's own `mnem` field is empty/missing)"
    a_fam, b_fam = real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    if a_fam is not None and a_fam != "rdi" and \
            not a_fam.startswith("xmm") and not a_fam.startswith("ymm"):
        shared_seed[a_fam] = seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi" and \
            not b_fam.startswith("xmm") and not b_fam.startswith("ymm"):
        shared_seed[b_fam] = seed_family(shared_seed, "rsi")
    sim_real = Sim9f(shared_seed, "real", a_is_vector)
    sim_cand = Sim9f(shared_seed, "cand", a_is_vector)
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    if w_real != w_cand:
        w = min(w_real, w_cand)
        val_real = z3.Extract(w - 1, 0, val_real)
        val_cand = z3.Extract(w - 1, 0, val_cand)
    solver = z3.Solver()
    for c in shared_seed.get("fcmp_constraints", []):
        solver.add(c)
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved this text equal to the " \
            "unit's own real ship code (register-identity-bound, " \
            "float packed-flags model -- is_nan/is_lt/is_eq shared " \
            "per operand pair) for every value of every register " \
            "either text reads before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample under which " \
            "this text and the unit's own real ship code compute " \
            "DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r" % result
