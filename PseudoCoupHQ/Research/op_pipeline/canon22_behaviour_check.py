#!/usr/bin/env python3
"""canon22_behaviour_check.py -- THE GROUND-TRUTH-ANCHORED GATE for
canon22_render.py's conversion-extended ucomisd/ucomiss flags family,
built on REAL z3 FLOATING-POINT SEMANTICS, the SAME reasoning canon21_
behaviour_check.py's own header already states for its sibling
(packed-mask) family: canon17_behaviour_check.py's own Sim9f keys
is_nan/is_lt/is_eq off a STRUCTURAL TAG (`_tag_of` -- "a"/"b"/"zero"
only), and a converted operand (`cvtsi2ss %edi,%xmm2`) is a FRESH
register with no tag -- neither the pristine "a" seed nor "b", a VALUE
computed from one of them. Real semantics are therefore load-bearing
here, exactly as they were for canon21_behaviour_check.py's own
target set, for the identical reason.

THE MODEL: `ucomisd`/`ucomiss` are reinterpreted DIRECTLY as real
IEEE754 unordered-compare predicates on the two operands' own raw
bits (read via the INHERITED `read_at`, so ordinary GP-family
register tracking and shared-seed identity binding are UNCHANGED) --
`fpBVToFP` reinterprets each tracked value's own low 32/64 bits as
F32/F64 per the mnemonic's OWN suffix (never guessed), `fpIsNaN` for
the unordered case, `fpLT`/`fpEQ` (both already IEEE754-correct: z3's
own FPA theory defines them false whenever either operand is NaN) for
the ordered case -- producing the SAME (is_nan, is_lt, is_eq) triple
condition_table4.fcond_to_z3 already consumes, so the EXISTING setcc
dispatch (inherited from canon17_behaviour_check.Sim9f, unchanged)
still drives every CondXX formula without modification.
`cvtsi2sd`/`cvtsi2ss`/`cvtss2sd` are the SAME three conversion
instructions canon21_behaviour_check.Sim11f already models (real
`fpSignedToFP`/`fpFPToFP`/`fpToIEEEBV`) -- reused verbatim, not
re-derived, since a conversion instruction does not care what
consumes its result (a comparison here, a packed arithmetic op
there).

WHY THIS SUPERSEDES Sim9f's OWN `_compute_flags` FOR ucomisd/ucomiss
ONLY: `_compute_flags`'s tag system is a strict partial function --
three shapes recognized, everything else (including a converted
register) raises NotModeled. This file replaces the ucomisd/ucomiss
dispatch with a real-FPA computation instead of widening `_tag_of`,
for the SAME reason canon21_behaviour_check.py's own header gives for
its own sibling supersession: a converted register has no stable tag
identity to hang a per-pair boolean off, but real FPA never needed one
in the first place. Every OTHER mnemonic (mov/cmp/setcc[integer]/
xorps/movd/movq/...) is inherited from Sim9f UNCHANGED.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon22_behaviour_check.py (library only -- canon22.py is the driver
  that calls anchored_check())
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon17_behaviour_check as BC17                          # noqa: E402
import canon21_behaviour_check as BC21                          # noqa: E402
import condition_table4 as CT4                                  # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC17.LANGS
split_operands = BC17.split_operands
NotModeled = BC17.NotModeled
real_text_of = BC17.real_text_of
real_arg_families = BC17.real_arg_families
seed_family = BC17.seed_family

F32 = BC21.F32
F64 = BC21.F64
RM = BC21.RM
_fp32_of = BC21._fp32_of
_fp64_of = BC21._fp64_of

SUFFIX_TO_FCOND = BC17.SUFFIX_TO_FCOND


class Sim12f(BC17.Sim9f):
    """canon17_behaviour_check.Sim9f, with ucomisd/ucomiss reinterpreted
    via real z3 FPA (never tag-based) and the three conversion
    instructions canon21_behaviour_check.Sim11f already models added
    verbatim. See file header."""

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

        if mnem in ("ucomisd", "ucomiss"):
            src, dst = split_operands(rest)
            is_double = mnem == "ucomisd"
            reader = _fp64_of if is_double else _fp32_of
            dst_v = reader(self.read_at(dst, 64))
            src_v = reader(self.read_at(src, 64))
            is_nan = z3.Or(z3.fpIsNaN(dst_v), z3.fpIsNaN(src_v))
            is_lt = z3.fpLT(dst_v, src_v)
            is_eq = z3.fpEQ(dst_v, src_v)
            self.last_fcc = (is_nan, is_lt, is_eq)
            self.last_flagsetter = "float"
            return

        BC17.Sim9f.exec_line(self, line)


def anchored_check(lang, n, canon4_docs, sem_docs, candidate_text,
                    a_is_vector=True):
    """canon17_behaviour_check.anchored_check, pointed at Sim12f. No
    fcmp mutual-exclusivity constraints are added here (unlike
    canon17_behaviour_check.anchored_check's own tag-based model) --
    real z3 FPA's own `fpLT`/`fpEQ` are ALREADY mutually exclusive by
    construction (IEEE754 total-order-on-non-NaN semantics baked into
    the theory itself), so no separate constraint needs adding, and
    none is fabricated."""
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
    sim_real = Sim12f(shared_seed, "real", a_is_vector)
    sim_cand = Sim12f(shared_seed, "cand", a_is_vector)
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
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 FPA proved this text equal to the " \
            "unit's own real ship code (real fpSignedToFP/fpFPToFP/" \
            "fpToIEEEBV conversion semantics, real fpLT/fpEQ/fpIsNaN " \
            "ucomisd/ucomiss semantics, register-identity-bound for " \
            "every non-converted operand)"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 FPA found a counterexample under " \
            "which this text and the unit's own real ship code " \
            "compute DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r (15000ms timeout, or " \
        "otherwise declined to decide)" % result
