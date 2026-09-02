#!/usr/bin/env python3
"""canon21_behaviour_check.py -- THE GROUND-TRUTH-ANCHORED GATE for
canon21_render.py's conversion-extended packed-mask float compare
family, built on REAL z3 FLOATING-POINT SEMANTICS (z3.FPSort/
fpSignedToFP/fpBVToFP/fpToIEEEBV/fpIsNaN/fpEQ -- the task's own
instruction for this family). Unlike canon19_behaviour_check.py's own
Sim10f (which never needed z3 FPA -- its own compare operands were
always TAGGED a/b/zero, so an uninterpreted-but-consistent boolean
model sufficed, condition_table4.py's own reasoning), a converted
operand (`cvtsi2ss %edi,%xmm2`) is a FRESH register with no tag: it is
neither the pristine "a" seed nor the pristine "b" seed, it is a VALUE
computed from one of them. Real semantics are therefore load-bearing
here in a way they were not for the pure-float family, exactly as the
task's own brief says.

THE MODEL: `cmpeqsd`/`cmpneqsd`/`cmpeqss`/`cmpneqss` are reinterpreted
DIRECTLY as real IEEE754 predicates on the two operands' own raw bits
(read via the INHERITED `read_at`, so ordinary GP-family register
tracking, shared-seed identity binding, and every other mnemonic this
lineage already models are UNCHANGED) -- `fpBVToFP` reinterprets each
64-bit tracked value's own low 32/64 bits as F32/F64 (the mnemonic's
own suffix says which, never guessed), and the compare's truth is
`fpEQ` (which z3's own FPA theory already defines to be FALSE whenever
either operand is NaN -- IEEE754's own unordered-compare rule, so no
separate `fpIsNaN` term is needed to get that behaviour; `fpIsNaN` is
used anyway, ANDed in explicitly, so the model's NaN handling is
readable at the term level rather than resting on knowing z3's fpEQ
convention). `cvtsi2sd`/`cvtsi2ss` use `fpSignedToFP` (round-to-
nearest-ties-to-even, z3.RNE() -- this corpus's own compilers never
change MXCSR, same finding canon20_behaviour_check.py already made and
restates here); `cvtss2sd` uses `fpFPToFP` for the width change. Both
write back via `fpToIEEEBV` so the result re-enters the SAME raw-
BitVec register model every other instruction already uses -- exactly
Sim20's own "a bag of bits; the instruction decides what they mean"
discipline (canon20_behaviour_check.py's own header), applied here to
Sim9f's family-based register file instead of Sim20's own bespoke one.

WHY THIS SUPERSEDES, RATHER THAN EXTENDS, Sim10f's `_compute_flags`
FOR THESE FOUR MNEMONICS ONLY: `_compute_flags`'s own tag system
(_tag_of) is a STRICT PARTIAL FUNCTION -- it recognizes literally three
shapes (pristine xmm0, pristine xmm1, concrete zero) and raises
NotModeled otherwise, INCLUDING for a converted register, which is
exactly the case this file exists to close. Rather than teach _tag_of
a fourth, conversion-shaped case (which would still need to fall back
to real FPA reasoning the moment two DIFFERENT conversion kinds of the
SAME source needed to be told apart, e.g. i32_to_f32 vs i32_to_f64 of
the same %edi), this file computes the real value once and lets z3's
own FPA theory decide -- strictly more general, and it still proves
the OLD pure-tagged units too (never exercised on this family's own
target set, since condition_table5.py's own unextended driver already
converges those; recorded here only so the model is understood to be a
superset, not a narrower replacement).

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon21_behaviour_check.py (library only -- canon21.py is the driver
  that calls anchored_check())
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon19_behaviour_check as BC19                          # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC19.LANGS
split_operands = BC19.split_operands
NotModeled = BC19.NotModeled
real_text_of = BC19.real_text_of
real_arg_families = BC19.real_arg_families
seed_family = BC19.seed_family

F32 = z3.Float32()
F64 = z3.Float64()
RM = z3.RNE()


def _fp32_of(raw):
    return z3.fpBVToFP(z3.Extract(31, 0, raw), F32)


def _fp64_of(raw):
    return z3.fpBVToFP(z3.Extract(63, 0, raw), F64)


class Sim11f(BC19.Sim10f):
    """canon19_behaviour_check.Sim10f, plus real z3-FPA conversion
    instructions and a real-FPA reinterpretation of the four packed-
    mask scalar compare mnemonics. See file header."""

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        if mnem in ("cvtsi2sd", "cvtsi2ss"):
            src, dst = split_operands(rest)
            src_name = src[1:]
            width = 64 if src_name.startswith("r") else 32
            ival = self.read_at(src, width)
            sort = F64 if mnem == "cvtsi2sd" else F32
            fpv = z3.fpSignedToFP(RM, ival, sort)
            bits = z3.fpToIEEEBV(fpv)
            if mnem == "cvtsi2ss":
                bits = z3.ZeroExt(32, bits)
            self.write(dst, bits)
            self.last_flagsetter = None
            return

        if mnem == "cvtss2sd":
            src, dst = split_operands(rest)
            f32v = _fp32_of(self.read_at(src, 64))
            f64v = z3.fpFPToFP(RM, f32v, F64)
            self.write(dst, z3.fpToIEEEBV(f64v))
            self.last_flagsetter = None
            return

        if mnem == "cvtsd2ss":
            src, dst = split_operands(rest)
            f64v = _fp64_of(self.read_at(src, 64))
            f32v = z3.fpFPToFP(RM, f64v, F32)
            self.write(dst, z3.ZeroExt(32, z3.fpToIEEEBV(f32v)))
            self.last_flagsetter = None
            return

        if mnem in ("cmpeqsd", "cmpneqsd", "cmpeqss", "cmpneqss"):
            src, dst = split_operands(rest)
            is_double = mnem.endswith("sd")
            reader = _fp64_of if is_double else _fp32_of
            dst_v = reader(self.read_at(dst, 64))
            src_v = reader(self.read_at(src, 64))
            is_nan = z3.Or(z3.fpIsNaN(dst_v), z3.fpIsNaN(src_v))
            truth = z3.And(z3.Not(is_nan), z3.fpEQ(dst_v, src_v))
            if mnem.startswith("cmpneq"):
                truth = z3.Not(truth)
            width = 64
            val = z3.If(truth, z3.BitVecVal((1 << width) - 1, width),
                         z3.BitVecVal(0, width))
            self.write(dst, val)
            self.last_flagsetter = None
            return

        BC19.Sim10f.exec_line(self, line)


def anchored_check(lang, n, canon4_docs, sem_docs, candidate_text,
                    a_is_vector=True):
    """canon19_behaviour_check.anchored_check, pointed at Sim11f."""
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
    sim_real = Sim11f(shared_seed, "real", a_is_vector)
    sim_cand = Sim11f(shared_seed, "cand", a_is_vector)
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
    solver.set("timeout", 15000)
    for c in shared_seed.get("fcmp_constraints", []):
        solver.add(c)
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 FPA proved this text equal to the " \
            "unit's own real ship code (real fpSignedToFP/fpFPToFP/ " \
            "fpToIEEEBV conversion semantics, real fpEQ/fpIsNaN " \
            "compare semantics, register-identity-bound for every " \
            "non-converted operand)"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 FPA found a counterexample under " \
            "which this text and the unit's own real ship code " \
            "compute DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r (15000ms timeout, or " \
        "otherwise declined to decide)" % result
