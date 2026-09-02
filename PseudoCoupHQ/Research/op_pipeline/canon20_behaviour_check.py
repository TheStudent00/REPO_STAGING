#!/usr/bin/env python3
"""canon20_behaviour_check.py -- JOB 3's GROUND-TRUTH-ANCHORED GATE,
built on REAL z3 FLOATING-POINT SEMANTICS (z3.FPSort/fpAdd/fpSub/
fpMul/fpDiv/fpSignedToFP/fpFPToFP/fpToIEEEBV/fpBVToFP -- the task's
own instruction, since real rounding/denormal/infinity/NaN-propagation
behaviour is exactly what this family needs and the rest of this
lineage's own uninterpreted-boolean model (condition_table4.py) was
built to AVOID needing). `Sim20` is a small, self-contained register
simulator in canon16.py's own style (NOT a subclass of the Sim7/8/9/10
GP-only lineage -- see that file's own header for why a narrow target
gets its own Sim rather than extending the shared one), tracking every
register (GP and XMM alike) as a raw 64-bit BitVec and reinterpreting
those bits as an FPSort value ONLY at the point an FPA instruction
needs one -- exactly how the real hardware's own registers work (a
bag of bits; the INSTRUCTION decides what they mean).

BIT-LEVEL PROOF (the task's own requirement, restated so it is not
lost): equality is checked via `fpToIEEEBV`, comparing raw BIT
PATTERNS with z3's own `!=` on BitVecs -- NEVER z3's `fpEQ` (which
treats -0.0 as equal to +0.0 and treats EVERY NaN as equal to every
other NaN, exactly the two distinctions IEEE754's own equality
predicate is defined to erase and this file's own gate is explicitly
required NOT to erase).

ROUNDING MODE: z3.RNE() (round-to-nearest-ties-to-even) uniformly --
x86-64's own MXCSR default, and this corpus's own compilers never
emit an instruction to change it (measured: no `ldmxcsr`/`vldmxcsr` in
any sampled real ship mnem for this family).

TIMEOUT (the task's own requirement): FPA solving can be slow. Each
`anchored_check` call sets a PER-CALL z3 solver timeout
(`PER_UNIT_TIMEOUT_MS`); a solver result of `unknown` (timeout, or any
other reason z3 declines to decide) is reported as UNDECIDED, counted
HONESTLY by the driver rather than folded into "refused" or silently
treated as a pass.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402

PER_UNIT_TIMEOUT_MS = 15000


class NotModeled(Exception):
    pass


F32 = z3.Float32()
F64 = z3.Float64()
RM = z3.RNE()


class Sim20(object):
    """see file header. `regs` maps a bare register name ('eax',
    'rdi', 'xmm0', 'xmm2', ...) to a 64-bit z3 BitVec -- the SAME
    "raw bits, reinterpreted only when an instruction needs a
    meaning" model canon16.py's own Sim16 uses, extended with real
    FPA conversion/arithmetic instructions."""

    def __init__(self, shared_seed, tag, resolved_const_bits=None):
        self.shared_seed = shared_seed
        self.tag = tag
        self.regs = {}
        # the ALREADY-RESOLVED `.rodata` constant (canon20_arith.py's
        # own CONST_SIGN/float_bits, forced by construction from the
        # unit's own `operator` field) this unit's real ship code
        # reads via a bare `N(%rip)` operand -- None for a unit that
        # has no such operand at all (see file header's own const
        # bucket; every OTHER unit in this file's own target set
        # never touches this).
        self.resolved_const_bits = resolved_const_bits

    def get(self, name):
        if name not in self.regs:
            if name not in self.shared_seed:
                self.shared_seed[name] = z3.BitVec(
                    "seed_%s" % name, 64)
            self.regs[name] = self.shared_seed[name]
        return self.regs[name]

    def _fp32_of(self, raw):
        return z3.fpBVToFP(z3.Extract(31, 0, raw), F32)

    def _fp64_of(self, raw):
        return z3.fpBVToFP(z3.Extract(63, 0, raw), F64)

    def exec_line(self, line):
        line = line.strip()
        reloc_at = line.find("!!reloc")
        if reloc_at != -1:
            line = line[:reloc_at].strip()
        if line == "ret" or line == "":
            return
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        operands = [o.strip() for o in rest.split(",")]

        if mnem in ("mov", "movabs"):
            src, dst = operands
            if not src.startswith("$"):
                raise NotModeled(
                    "%s with a non-immediate source is not modeled "
                    "-- %r" % (mnem, line))
            v = int(src[1:], 0) & 0xFFFFFFFFFFFFFFFF
            self.regs[dst[1:]] = z3.BitVecVal(v, 64)
            return

        if mnem in ("movd", "movq"):
            src, dst = operands
            width = 32 if mnem == "movd" else 64
            v = self.get(src[1:])
            v = z3.Extract(width - 1, 0, v)
            v = z3.ZeroExt(64 - width, v)
            self.regs[dst[1:]] = v
            return

        if mnem in ("movaps", "movapd"):
            src, dst = operands
            self.regs[dst[1:]] = self.get(src[1:])
            return

        if mnem in ("cvtsi2sd", "cvtsi2ss"):
            src, dst = operands
            src_name = src[1:]
            width = 64 if src_name.startswith("r") else 32
            raw = self.get(src_name)
            ival = z3.Extract(width - 1, 0, raw)
            sort = F64 if mnem == "cvtsi2sd" else F32
            fpv = z3.fpSignedToFP(RM, ival, sort)
            bits = z3.fpToIEEEBV(fpv)
            if mnem == "cvtsi2ss":
                bits = z3.ZeroExt(32, bits)
            self.regs[dst[1:]] = bits
            return

        if mnem == "cvtss2sd":
            src, dst = operands
            f32v = self._fp32_of(self.get(src[1:]))
            f64v = z3.fpFPToFP(RM, f32v, F64)
            self.regs[dst[1:]] = z3.fpToIEEEBV(f64v)
            return

        if mnem == "cvtsd2ss":
            src, dst = operands
            f64v = self._fp64_of(self.get(src[1:]))
            f32v = z3.fpFPToFP(RM, f64v, F32)
            self.regs[dst[1:]] = z3.ZeroExt(
                32, z3.fpToIEEEBV(f32v))
            return

        if mnem in ("addsd", "subsd", "mulsd", "divsd",
                    "addss", "subss", "mulss", "divss"):
            src, dst = operands
            is_double = mnem.endswith("sd")
            width = 64 if is_double else 32
            reader = self._fp64_of if is_double else self._fp32_of
            src_v = self._operand_fp(src, width, reader)
            dst_v = reader(self.get(dst[1:]))
            op = mnem[:3]
            if op == "add":
                rv = z3.fpAdd(RM, dst_v, src_v)
            elif op == "sub":
                rv = z3.fpSub(RM, dst_v, src_v)
            elif op == "mul":
                rv = z3.fpMul(RM, dst_v, src_v)
            else:
                rv = z3.fpDiv(RM, dst_v, src_v)
            bits = z3.fpToIEEEBV(rv)
            if not is_double:
                bits = z3.ZeroExt(32, bits)
            self.regs[dst[1:]] = bits
            return

        raise NotModeled(
            "mnemonic %r has no symbolic model in Sim20 -- %r"
            % (mnem, line))

    def _operand_fp(self, operand, width, reader):
        """`width` (32 or 64) is passed EXPLICITLY by the caller --
        NOT inferred by comparing `reader is self._fp64_of`, which is
        unreliable (Python creates a FRESH bound-method object on
        every attribute access, so two separately-obtained references
        to the SAME bound method are not guaranteed `is`-equal; this
        was measured to silently pick the 32-bit branch for a 64-bit
        `addsd`, truncating the resolved constant to its own low 32
        bits before zero-extending -- a real, caught-by-the-gate-
        itself bug, not a hypothetical one: see canon20.py's own
        report for the before/after)."""
        if operand.endswith("(%rip)"):
            if self.resolved_const_bits is None:
                raise NotModeled(
                    "a rip-relative operand appeared with no "
                    "resolved constant recorded for this unit -- "
                    "no return path")
            bits = z3.BitVecVal(self.resolved_const_bits, 64)
            return reader(bits) if width == 64 else \
                reader(z3.ZeroExt(32, z3.Extract(31, 0, bits)))
        return reader(self.get(operand[1:]))

    def answer_value(self, lines, width):
        for line in lines:
            self.exec_line(line)
        full = self.get("xmm0")
        return z3.Extract(width - 1, 0, full)


def width_of(precision):
    return precision


def anchored_check(real_text, candidate_text, precision,
                    resolved_const_bits=None):
    """(verdict, detail). verdict in {PROVED_EQUAL, DISPROVED,
    UNDECIDED}. Proves the two texts' final %xmm0 value equal at the
    BIT level (fpToIEEEBV, never fpEQ -- see file header), with a
    per-call solver timeout; a timeout is reported UNDECIDED, never
    folded into a refusal or a silent pass."""
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    shared_seed = {}
    try:
        val_real = Sim20(
            shared_seed, "real", resolved_const_bits
        ).answer_value(lines_real, precision)
        val_cand = Sim20(
            shared_seed, "cand", resolved_const_bits
        ).answer_value(lines_cand, precision)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    solver = z3.Solver()
    solver.set("timeout", PER_UNIT_TIMEOUT_MS)
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 FPA proved this text's final " \
            "%%xmm0 bit pattern equal to the unit's own real ship " \
            "code's, at the answer's own %d-bit stated width " \
            "(fpToIEEEBV bit-level comparison, RNE rounding, " \
            "%dms timeout)" % (precision, PER_UNIT_TIMEOUT_MS)
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 FPA found a counterexample under " \
            "which this text and the unit's own real ship code " \
            "compute DIFFERENT bit patterns: %s" % model
    return "UNDECIDED", "z3 returned %r (solver timeout at %dms, or " \
        "otherwise declined to decide) -- counted honestly, never " \
        "treated as a pass" % (result, PER_UNIT_TIMEOUT_MS)
