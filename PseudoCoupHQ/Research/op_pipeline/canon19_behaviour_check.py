#!/usr/bin/env python3
"""canon19_behaviour_check.py -- THE GROUND-TRUTH-ANCHORED GATE,
EXTENDED WITH THE PACKED-MASK COMPARE MNEMONICS, for JOB 1's packed-
mask float compare rendering (canon19_render.py). Mirrors canon17_
behaviour_check.py's own shape exactly (prove the candidate directly
against the unit's own real ship code, register-identity pre-bound via
a SHARED z3 seed, reusing Sim9f's is_nan/is_lt/is_eq per-operand-pair
model UNCHANGED) -- the difference is six new mnemonics: `cmpeqsd`/
`cmpneqsd`/`cmpeqss`/`cmpneqss` (a packed compare that WRITES A VALUE,
not a flag -- all-ones across the register if the ordered-equality
predicate holds, all-zeros otherwise, using the SAME is_nan/is_eq
booleans `_compute_flags` already derives for ucomisd/ucomiss) and
`andps`/`andpd`/`orps`/`orpd`/`movaps`/`movapd` (plain 64-bit
register-register bitwise-AND/OR/copy -- the SAME shape `xorps`/
`xorpd` already have in Sim9f, just a different combining operator, or
none at all for the copy).

WHY THE FULL 64 BITS, NOT JUST THE LANE WIDTH: real CMPEQSS only
writes the low 32 bits of its destination (upper 96 preserved); this
corpus's own downstream use (verified by this lap's own survey, see
condition_table5.py's file header) NEVER reads past the low 32 bits of
a packed-mask result either way (the outermost extraction is always
`ex32@0(...)`/`movd`), so broadcasting the SAME 0/all-ones answer
across the full 64-bit tracked width is observationally identical for
every text this file ever compares, and avoids teaching Sim8's `write`
a narrower-than-64 partial-write mode it does not otherwise have.

REUSES canon17_behaviour_check.Sim9f UNCHANGED for every mnemonic it
already knows (ucomisd/ucomiss/xorps/xorpd/movd/movq/the float setcc
dispatch, plus everything inherited from Sim8) -- this file adds
exactly the six new mnemonics above and falls back to Sim9f.exec_line
for everything else.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon19_behaviour_check.py (library only -- canon19.py is the driver
  that calls anchored_check())
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon17_behaviour_check as BC17                           # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC17.LANGS
split_operands = BC17.split_operands
NotModeled = BC17.NotModeled
real_text_of = BC17.real_text_of
real_arg_families = BC17.real_arg_families
seed_family = BC17.seed_family

ALL_ONES_64 = (1 << 64) - 1


class Sim10f(BC17.Sim9f):
    """canon17_behaviour_check.Sim9f, plus the packed-mask-compare
    value-writing mnemonics and plain XMM AND/OR/copy. See file
    header."""

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        if mnem in ("movd", "movq"):
            src, dst = split_operands(rest)
            if src.startswith("%xmm"):
                # THE XMM-SOURCE GAP: canon.py's own WIDTH_OF declares
                # every xmm spelling at a fixed 64 bits (no e-/r-
                # prefix-style width-in-the-name the way GP registers
                # have), so Sim8's inherited `movd`/`movq` handler
                # (which calls read_at(src, 32-or-64) and requires the
                # operand's OWN declared width to match exactly) can
                # never read `movd %xmmN,%eax` -- a form no PRIOR
                # generation's own render ever produced (canon16_xmm.
                # py's own movd/movq are GP->XMM only), so this is a
                # genuinely new, narrow direction, not a widened
                # meaning of an old one. Truncate from the tracked
                # 64-bit family explicitly instead of asserting an
                # exact-width match.
                width = 32 if mnem == "movd" else 64
                full = self.read_at(src, 64)
                v = z3.Extract(width - 1, 0, full) \
                    if width < 64 else full
                v = z3.ZeroExt(64 - width, v) if width < 64 else v
                self.write(dst, v)
                return

        if mnem in ("cmpeqsd", "cmpneqsd", "cmpeqss", "cmpneqss"):
            src, dst = split_operands(rest)
            dst_v = self.read_at(dst, 64)
            src_v = self.read_at(src, 64)
            is_nan, is_lt, is_eq = self._compute_flags(dst_v, src_v)
            truth = z3.And(z3.Not(is_nan), is_eq)
            if mnem.startswith("cmpneq"):
                truth = z3.Not(truth)
            val = z3.If(truth, z3.BitVecVal(ALL_ONES_64, 64),
                         z3.BitVecVal(0, 64))
            self.write(dst, val)
            self.last_flagsetter = None
            return

        if mnem in ("andps", "andpd", "orps", "orpd"):
            src, dst = split_operands(rest)
            a = self.read_at(dst, 64)
            b = self.read_at(src, 64)
            if mnem.startswith("and"):
                self.write(dst, a & b)
            else:
                self.write(dst, a | b)
            return

        if mnem in ("movaps", "movapd"):
            src, dst = split_operands(rest)
            self.write(dst, self.read_at(src, 64))
            return

        BC17.Sim9f.exec_line(self, line)


def anchored_check(lang, n, canon4_docs, sem_docs, candidate_text,
                    a_is_vector=True):
    """canon17_behaviour_check.anchored_check, pointed at Sim10f."""
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
    sim_real = Sim10f(shared_seed, "real", a_is_vector)
    sim_cand = Sim10f(shared_seed, "cand", a_is_vector)
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
            "packed-mask compare model -- is_nan/is_lt/is_eq shared " \
            "per operand pair) for every value of every register " \
            "either text reads before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample under which " \
            "this text and the unit's own real ship code compute " \
            "DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r" % result
