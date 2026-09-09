#!/usr/bin/env python3
# SUPERSEDED 2026-09-03 by reference.py (node 0_3_5_4 reference): one Reference, one MachineState, one opcode_table; this file is a record and is not edited further.
"""canon12_behaviour_check.py -- STAGE 2's own gate extension: the
ground-truth simulator (canon5_behaviour_check.Sim through canon9.
Sim9) has NEVER modeled `cltd`/`cqto`/`idiv`/`div`/the 1-operand
widening `imul`/`mul` -- canon5_behaviour_check.py's own header says
so explicitly ("idiv is explicitly OUT OF SCOPE... whether the two
texts agree depends on a fact this checker cannot read off the
rendered text alone"), because %rdx there is TRULY ambient (no
instruction in that corpus's vocabulary ever DEFINES it before an
idiv reads it).

THAT REASON DOES NOT APPLY HERE. Every idiv/div this lap's Stage 2
renders is IMMEDIATELY preceded, in the SAME instruction text, by a
`cqto`/`cltd`/`xor %edx,%edx` that DEFINES %rdx/%edx locally -- and
so is every real ship idiv/div this corpus's own C/Rust/Swift/Go
compilers emit (measured: canon4_units's own `mnem` for every c/op_
211/212/216/217/218/222/247/248, all sixteen -- see this lap's
report). %rdx is not ambient in this comparison; it is locally
computed, so it CAN be modeled soundly, and doing so is what actually
lets Stage 2's candidates be PROVED, not just asserted plausible.

FOUR MNEMONICS ADDED, on top of canon9.Sim9 (reused via subclass,
same pattern canon8/canon9 already use for their own additions):
  - `cltd` / `cqto`: %edx/%rdx = sign_bits(%eax/%rax) -- arithmetic
    right-shift by (width-1), z3's own `>>` on a BitVec (verified:
    `z3.simplify(Concat(X >> 63, X))` proved identical to
    `z3.simplify(SignExt(64, X))` for every X, unsat on inequality).
  - `idiv S` / `div S`: reads the AMBIENT-BUT-LOCALLY-DEFINED %edx:%eax
    or %rdx:%rax pair (width taken from S's own operand width, same
    "read the text's own stated width" discipline `answer_value`
    already uses elsewhere in this lineage), divides by S sign/zero-
    extended to double width (signed: z3's `/`, decl `bvsdiv_i`,
    TRUNCATING toward zero -- matches x86 `idiv`, verified by direct
    experiment, NOT z3's `%` operator which is FLOORED `bvsmod`;
    unsigned: `z3.UDiv`/`z3.URem`), quotient into %eax/%rax, remainder
    into %edx/%rdx -- the same two x86-64-defined destinations real
    hardware writes, so a SUBSEQUENT instruction reading either one
    (e.g. `mov %rdx,%rax` for the `%` case) is modeled correctly with
    no special-casing needed at the call site.
  - 1-operand `imul S` / `mul S` (the WIDENING form -- disambiguated
    from the already-modeled 2-operand `imul S,D` purely by operand
    COUNT, never by guessing): %edx:%eax or %rdx:%rax = S sign/zero-
    extended times %eax/%rax sign/zero-extended, split high:low into
    the same destination pair. Not exercised by Stage 2's own target
    units (Mul64/Mul32 all measured as the 2-operand truncating form
    -- see canon12_normalize.py's header) but added for completeness
    and because it costs nothing extra once idiv/div's register-pair
    read/write plumbing exists.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon9 as C9                                              # noqa: E402
import canon8_behaviour_check as BC8                             # noqa: E402
import z3                                                        # noqa: E402

LOW_REG = {32: "%eax", 64: "%rax"}
HIGH_REG = {32: "%edx", 64: "%rdx"}


class Sim10(C9.Sim9):
    """canon9.Sim9, plus cltd/cqto/idiv/div/widening-imul/mul -- see
    file header for why %rdx is safe to model here (locally defined,
    never ambient, in every text this checker is asked to compare)."""

    def exec_line(self, line):
        stripped = line.strip()
        parts = stripped.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        if mnem in ("cltd", "cqto"):
            width = 32 if mnem == "cltd" else 64
            lo_reg = LOW_REG[width]
            hi_reg = HIGH_REG[width]
            a = self.read_at(lo_reg, width)
            sign = a >> z3.BitVecVal(width - 1, width)
            self.write(hi_reg, sign)
            return

        if mnem in ("idiv", "div"):
            (divisor_op,) = BC8.split_operands(rest)
            width = self.width_of_operand(divisor_op)
            lo_reg = LOW_REG[width]
            hi_reg = HIGH_REG[width]
            lo = self.read_at(lo_reg, width)
            hi = self.read_at(hi_reg, width)
            dividend = z3.Concat(hi, lo)
            divisor_v = self.read_at(divisor_op, width)
            if mnem == "idiv":
                divisor_ext = z3.SignExt(width, divisor_v)
                q = dividend / divisor_ext
                r = z3.SRem(dividend, divisor_ext)
            else:
                divisor_ext = z3.ZeroExt(width, divisor_v)
                q = z3.UDiv(dividend, divisor_ext)
                r = z3.URem(dividend, divisor_ext)
            self.write(lo_reg, z3.Extract(width - 1, 0, q))
            self.write(hi_reg, z3.Extract(width - 1, 0, r))
            return

        if mnem in ("imul", "mul"):
            operands = BC8.split_operands(rest)
            if len(operands) == 1:
                (src_op,) = operands
                width = self.width_of_operand(src_op)
                lo_reg = LOW_REG[width]
                hi_reg = HIGH_REG[width]
                a = self.read_at(lo_reg, width)
                b = self.read_at(src_op, width)
                if mnem == "imul":
                    prod = z3.SignExt(width, a) * z3.SignExt(width, b)
                else:
                    prod = z3.ZeroExt(width, a) * z3.ZeroExt(width, b)
                self.write(lo_reg, z3.Extract(width - 1, 0, prod))
                self.write(hi_reg,
                           z3.Extract(2 * width - 1, width, prod))
                return

        C9.Sim9.exec_line(self, line)


def wide_anchored_check(lang, n, canon4_docs, sem_docs, text):
    """canon9.job2_anchored_check, using Sim10 (this file's idiv/div/
    cltd/cqto/widening-mul-aware simulator) instead of Sim9 --
    everything else (real-text lookup, register-identity pre-binding,
    shift-count masking, logic-flag tracking) is reused UNCHANGED."""
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this " \
            "unit"
    a_fam, b_fam = BC8.real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    if a_fam is not None and a_fam != "rdi":
        shared_seed[a_fam] = BC8.seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi":
        shared_seed[b_fam] = BC8.seed_family(shared_seed, "rsi")
    sim_real = Sim10(shared_seed, "real")
    sim_cand = Sim10(shared_seed, "cand")
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in text.split(";")]
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except BC8.NotModeled as exc:
        return "UNDECIDED", str(exc)
    if w_real != w_cand:
        w = min(w_real, w_cand)
        val_real = z3.Extract(w - 1, 0, val_real)
        val_cand = z3.Extract(w - 1, 0, val_cand)
    solver = z3.Solver()
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved this text equal to the " \
            "unit's own real ship code (register-identity-bound, " \
            "shift-masked, logic-flag-aware, idiv/div/cltd/cqto-" \
            "modeled model)"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample: %s" % model
    return "UNDECIDED", "z3 returned %r" % result
