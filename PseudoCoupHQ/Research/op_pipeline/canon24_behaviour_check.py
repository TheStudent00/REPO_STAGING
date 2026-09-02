#!/usr/bin/env python3
"""canon24_behaviour_check.py -- THE GROUND-TRUTH-ANCHORED GATE for
canon24_render.py's own CmpEQ32F0x4/64F0x2 (and the XorV128-wrapped
CmpNEQ compound; see vex_names.py's own header) family.

`Sim24` extends canon22_behaviour_check.Sim12f (the GP-integer +
condition-aware lineage already used to gate the fcond family's own
zx64/And32/ex32@0/movd wrapping -- the SAME surrounding shape this
file's own target units carry) with the FOUR packed-mask compare
mnemonics real ship code actually emits for this family: cmpeqss/
cmpeqsd/cmpneqss/cmpneqsd. Modeled with real z3 FPA (fpBVToFP/fpEQ/
fpIsNaN, reusing canon21_behaviour_check.py's own `_fp32_of`/`_fp64_of`
helpers via canon22_behaviour_check's own re-export), the SAME
discipline canon21_behaviour_check.py's own header states for the
sibling packed-mask family: real semantics are load-bearing because a
CONVERTED operand (`cvtsi2ss %edi,%xmm1`) is a fresh register with no
stable a/b/zero tag to hang a per-pair boolean off.

Every OTHER mnemonic (mov/movd/movq/and/test/setcc/cvtsi2sd/cvtsi2ss/
cvtss2sd/ucomisd/ucomiss/...) is inherited from Sim12f UNCHANGED.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon24_behaviour_check.py (library only -- canon24.py is the driver
  that calls anchored_check_24())
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon22_behaviour_check as BC22                          # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC22.LANGS
split_operands = BC22.split_operands
NotModeled = BC22.NotModeled
real_text_of = BC22.real_text_of
real_arg_families = BC22.real_arg_families
seed_family = BC22.seed_family

_fp32_of = BC22._fp32_of
_fp64_of = BC22._fp64_of


class Sim24(BC22.Sim12f):
    """canon22_behaviour_check.Sim12f, plus cmpeqss/cmpeqsd/cmpneqss/
    cmpneqsd, and a corrected movd/movq FOR AN XMM SOURCE. See file
    header.

    THE movd/movq FIX (found while gating this family's own first
    worked example, c/op_501 -- real ship code's own `movd %xmm1,
    %eax`): the inherited Sim9f movd/movq handling calls `read_at(src,
    width)`, which requires the source's OWN declared width to equal
    the width requested -- true for a GP source (`movd %eax,%xmm0`,
    32-bit source, 32-bit request) but FALSE for an XMM source, which
    this Sim lineage always tracks as a 64-bit family register
    (canon.py's own WIDTH_OF table): `movd %xmm1,%eax` is a legitimate
    NARROWING read (low 32 of a 64-bit-tracked value), not a width
    mismatch. Never exercised before this family (every prior fcond
    unit writes its boolean answer straight into a GP register via
    setcc, never via movd-from-xmm), so this is a real, newly-measured
    gap, fixed here rather than in the shared Sim9f/Sim12f (this
    lineage's own "wrap, do not edit an earlier generation" rule)."""

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        if mnem in ("movd", "movq"):
            src, dst = split_operands(rest)
            width = 32 if mnem == "movd" else 64
            src_name = src[1:] if src.startswith("%") else None
            if src_name is not None and src_name.startswith("xmm"):
                raw64 = self.read_at(src, 64)
                v = z3.Extract(width - 1, 0, raw64)
            else:
                v = self.read_at(src, width)
            v = z3.ZeroExt(64 - width, v) if width < 64 else v
            self.write(dst, v)
            self.last_flagsetter = None
            return

        if mnem in ("cmpeqss", "cmpeqsd", "cmpneqss", "cmpneqsd"):
            src, dst = split_operands(rest)
            is_double = mnem.endswith("sd")
            width = 64 if is_double else 32
            reader = _fp64_of if is_double else _fp32_of
            dst_v = reader(self.read_at(dst, 64))
            src_v = reader(self.read_at(src, 64))
            truth = z3.And(
                z3.Not(z3.Or(z3.fpIsNaN(dst_v), z3.fpIsNaN(src_v))),
                z3.fpEQ(dst_v, src_v))
            if mnem.startswith("cmpneq"):
                truth = z3.Not(truth)
            lane = z3.If(truth, z3.BitVecVal((1 << width) - 1, width),
                          z3.BitVecVal(0, width))
            val = lane if width == 64 else z3.ZeroExt(32, lane)
            self.write(dst, val)
            self.last_flagsetter = None
            return

        BC22.Sim12f.exec_line(self, line)


def anchored_check_24(lang, n, canon4_docs, sem_docs, candidate_text,
                       a_is_vector=True):
    """canon22_behaviour_check.anchored_check, pointed at Sim24."""
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
    sim_real = Sim24(shared_seed, "real", a_is_vector)
    sim_cand = Sim24(shared_seed, "cand", a_is_vector)
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
            "unit's own real ship code (real fpEQ/fpIsNaN cmpeqss/" \
            "cmpeqsd/cmpneqss/cmpneqsd semantics, register-identity-" \
            "bound for every non-converted operand, inherited " \
            "mov/and/test/setcc/cvtsi2sX GP+condition modeling)"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 FPA found a counterexample under " \
            "which this text and the unit's own real ship code " \
            "compute DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r (15000ms timeout, or " \
        "otherwise declined to decide)" % result
