#!/usr/bin/env python3
# SUPERSEDED 2026-09-03 by reference.py (node 0_3_5_4 reference): one Reference, one MachineState, one opcode_table; this file is a record and is not edited further.
"""canon9_behaviour_check.py -- TASK 22 (log_105, round 4), a WRAPPER
extension of the z3 simulator, adding exactly the coverage log_099's
round-3 lap named as the checker's own gap and left as a frontier
(never attempted that lap, "out of this lap's scope to change
without re-verifying every downstream consumer"). This file does NOT
modify canon5/canon6/canon7/canon8_behaviour_check.py -- it is a new
subclass importing every one of them by reference, the same reuse
discipline every file in this lineage already follows (canon6 wraps
canon5, canon7 wraps canon6, canon8 wraps canon7; this file wraps
canon8). No shared file is touched.

WHAT THIS FILE ADDS, measured directly off the 26 UNDECIDED units
found this lap (re-counted from canon28_units_<lang>.json's own
`job5_no_named_op_ground_truth_detail` field, not copied from
log_099's prose -- see log_105 for the corrected tally):

  6  WIDTH_OF gap, `-0x8(%rsp)`/`-0x1(%rsp)` stack-relative operands
     -- NOT modeled here. These are the SAME 6 units log_099 already
     named under the `SP:64` leaf-atom bucket and recommended
     the owner-reserved (a semantic ruling about what "the answer" means
     for a pointer-valued/address-of unit, not a mechanical checker
     gap). No new evidence surfaced this lap that would change that
     call -- carried forward, not reopened.
  4  `cltd` -- MODELED (sign-extends eax's sign bit through edx,
     32-bit form; `cqto`/`cqo` modeled identically at 64-bit).
  4  `idiv`'s "ambient %edx/%rdx" -- MODELED. Round 3 judged this
     ambient (unreadable from the text alone) because it never
     modeled `cltd`; every occurrence of `idiv` in this corpus is
     immediately preceded by `cltd`/`cqto` in the SAME text (verified
     by direct inspection of all 4 c/cpp pairs this lap), so once
     `cltd` sets edx from THIS simulator's own tracked eax value, the
     dividend is no longer ambient -- it is EDX:EAX as this run's own
     state, exactly what real hardware reads.
  6  `jo` (jump-if-overflow, always following a `neg`) -- MODELED via
     a tracked overflow flag (`neg` overflows in x86-64 iff the
     input equals INT_MIN for its width; the only case where negating
     a two's-complement value cannot be represented).
  4  `je` (jump-if-equal, always following a `test`) -- MODELED, by
     giving branch mnemonics access to the SAME `last_cmp`/
     `condition_table.py` predicate machinery canon6_behaviour_check.
     ExtSim already uses for `setcc`/`cmovcc` -- ZERO new flag logic,
     the predicate table is reused unchanged.
  2  `jb` (jump-if-below/carry, following an `add`) -- MODELED via a
     tracked carry flag (unsigned overflow of the addition).

CONTROL FLOW. The `jo`/`je`/`jb` units are all 2-3 block units with a
`ud2` (illegal-instruction trap) or `call <panic-helper>` on the
not-taken side -- a REAL branch, not a straight line, which is why
canon8_behaviour_check.anchored_check (a straight-line-only text
comparator) could never have modeled it regardless of mnemonic
coverage. This file adds a small recursive block-walker (`run_flow`)
that explores BOTH sides of each conditional branch, merges the two
answer values with a z3 `If` guarded by the branch's own predicate,
and treats a block that traps (`ud2`/`call`) as contributing NO value
-- sound here specifically because canon4.py's own renderer NEVER
rewrites a guard/trap/dispatch block (only a compute block, ratified
and already relied on by canon6_behaviour_check.py's per-block
scoping, see that file's header) -- so the real block and the
candidate (derived) block reaching a trap share the EXACT SAME
predicate text, by construction, not by assumption re-derived here.
The block-structured `blocks` (real) / `derived_blocks` (candidate)
fields already on every canon4_units_<lang>.json record are used
directly -- both are already label-keyed and mutually label-
consistent (canon4.py's own guarantee), so no address-to-label
resolution is attempted or needed.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

This file selects nothing by operator token: unit selection (which
20 of the 26 UNDECIDED units this file attempts) is done by its
caller (canon29.py) from the machine-form `job5_no_named_op_ground_
truth_detail` reason string already on record, never from `operator`.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon9_behaviour_check.py (library only -- no CLI entry point;
  canon29.py is the driver that calls this file's functions)
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                    # noqa: E402
import canon8_behaviour_check as BC8                             # noqa: E402
import condition_table as CT                                     # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC8.LANGS
split_operands = BC8.split_operands
NotModeled = BC8.NotModeled
real_arg_families = BC8.real_arg_families
seed_family = BC8.seed_family


class Trap(Exception):
    """raised when symbolic execution reaches a `ud2`/`call` block --
    a real hardware trap, not a modeling gap. Callers treat a trapped
    branch as contributing no answer value (see module header)."""
    pass


class Sim9(BC8.Sim8):
    """canon8_behaviour_check.Sim8, plus cltd/cqto, idiv, and tracked
    overflow/carry flags for jo/jb (je reuses the existing last_cmp/
    condition_table path unchanged)."""

    def __init__(self, shared_seed, tag):
        BC8.Sim8.__init__(self, shared_seed, tag)
        self.last_flags = {}
        self.rax_write_width = None

    def write(self, operand, value):
        BC8.Sim8.write(self, operand, value)
        name = operand[1:]
        fam = canon.FAMILY_OF.get(name)
        if fam == "rax":
            self.rax_write_width = self.width_of_operand(operand)

    def current_answer(self):
        """(value, width) of the last write to the rax family reached
        on THIS execution path -- the control-flow-aware replacement
        for Sim.answer_value's linear end-of-text scan."""
        if self.rax_write_width is None:
            raise NotModeled(
                "no instruction on this path ever wrote the answer "
                "(rax) family")
        width = self.rax_write_width
        fam_val = self.get_family("rax")
        return z3.Extract(width - 1, 0, fam_val), width

    def cond_bool(self, suffix):
        """the z3 Bool for branch suffix `suffix` (e.g. "o" for jo,
        "b" for jb, "e" for je), preferring a directly-tracked
        overflow/carry flag and falling back to the SAME cmp-based
        condition_table.py predicate setcc/cmovcc already use."""
        if suffix == "o":
            if "O" in self.last_flags:
                return self.last_flags["O"]
            raise NotModeled(
                "jo with no preceding overflow-flag-setting "
                "instruction tracked by this checker -- not modeled")
        if suffix in ("b", "c", "nae") and "C" in self.last_flags:
            return self.last_flags["C"]
        if suffix in CT.SUFFIX_TO_COND:
            if self.last_cmp is None:
                raise NotModeled(
                    "branch suffix %r with no preceding cmp/test in "
                    "this text -- flags carried in from outside this "
                    "sequence, not modeled" % suffix)
            cond = CT.SUFFIX_TO_COND[suffix]
            left, right = self.last_cmp
            return CT.cond_to_z3(cond, left, right, z3)
        raise NotModeled(
            "branch suffix %r has no symbolic predicate model in "
            "this checker" % suffix)

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem in ("cltd", "cqto", "cqo"):
            width = 32 if mnem == "cltd" else 64
            src_name = "%eax" if width == 32 else "%rax"
            dst_name = "%edx" if width == 32 else "%rdx"
            v = self.read_at(src_name, width)
            shift_amt = z3.BitVecVal(width - 1, width)
            filled = v >> shift_amt   # z3 BitVec ">>" is arithmetic
            self.write(dst_name, filled)
            return
        if mnem == "idiv":
            (divisor_op,) = split_operands(rest)
            width = self.width_of_operand(divisor_op)
            if width not in (32, 64):
                raise NotModeled(
                    "idiv at width %d is not modeled (only 32/64-bit "
                    "forms, matching this corpus's cltd/cqto "
                    "coverage)" % width)
            eax_name = "%eax" if width == 32 else "%rax"
            edx_name = "%edx" if width == 32 else "%rdx"
            eax_v = self.read_at(eax_name, width)
            edx_v = self.read_at(edx_name, width)
            dividend = z3.Concat(edx_v, eax_v)
            divisor_v = self.read_at(divisor_op, width)
            divisor_wide = z3.SignExt(width, divisor_v)
            quotient_wide = dividend / divisor_wide       # z3 SDiv
            remainder_wide = dividend % divisor_wide       # z3 SRem
            quotient = z3.Extract(width - 1, 0, quotient_wide)
            remainder = z3.Extract(width - 1, 0, remainder_wide)
            self.write(eax_name, quotient)
            self.write(edx_name, remainder)
            return
        if mnem == "neg":
            (operand,) = split_operands(rest)
            width = self.width_of_operand(operand)
            a = self.read_at(operand, width)
            int_min = z3.BitVecVal(1 << (width - 1), width)
            overflow = (a == int_min)
            self.last_flags = {"O": overflow}
            BC8.Sim8.exec_line(self, line)
            return
        if mnem == "add":
            operands = split_operands(rest)
            src, dst = operands
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            b = self.read_at(src, width)
            wide_sum = z3.ZeroExt(1, a) + z3.ZeroExt(1, b)
            carry = (z3.Extract(width, width, wide_sum) ==
                     z3.BitVecVal(1, 1))
            # signed overflow: the exact (width+1)-bit signed sum's
            # extra top bit disagrees with the sign bit of the
            # truncated width-bit result -- the standard OF formula,
            # independent of/additional to the unsigned CARRY above.
            wide_signed_sum = z3.SignExt(1, a) + z3.SignExt(1, b)
            of_add = (z3.Extract(width, width, wide_signed_sum) !=
                      z3.Extract(width - 1, width - 1,
                                 wide_signed_sum))
            self.last_flags = {"C": carry, "O": of_add}
            BC8.Sim8.exec_line(self, line)
            return
        if mnem == "sub":
            operands = split_operands(rest)
            src, dst = operands
            width = self.width_of_operand(dst)
            a = self.read_at(dst, width)
            b = self.read_at(src, width)
            # x86 SUB's carry flag is the UNSIGNED BORROW: set iff
            # the unsigned minuend is less than the unsigned
            # subtrahend (the same predicate condition_table.py's
            # CondULT already names for cmp -- computed directly
            # here rather than round-tripping through cmp's own
            # last_cmp state, so `sub` alone (no separate cmp/test)
            # still gives jb a flag to read).
            borrow = z3.ULT(a, b)
            wide_signed_diff = z3.SignExt(1, a) - z3.SignExt(1, b)
            of_sub = (z3.Extract(width, width, wide_signed_diff) !=
                      z3.Extract(width - 1, width - 1,
                                 wide_signed_diff))
            self.last_flags = {"C": borrow, "O": of_sub}
            BC8.Sim8.exec_line(self, line)
            return
        BC8.Sim8.exec_line(self, line)


def run_flow(sim, blocks, label, depth=0, order=None):
    """(value, width) reached by symbolically walking `blocks` (a
    dict label -> [instruction lines]) from `label`, exploring both
    sides of every conditional branch and z3-merging with `If`. A
    trapped block (`ud2`/`call`) raises Trap -- callers treat that as
    "no value on this path" (see module header for why this is
    sound: guard/trap blocks are never rewritten, so real and
    candidate always share the identical predicate). `order` is the
    real compiled BLOCK ORDER (canon4_units's own `blocks`/`derived_
    blocks` list order) -- a block whose steps run out with no
    explicit ret/jmp/trap FALLS THROUGH to the next block in that
    same order, exactly as real x86-64 does when the assembler omits
    a redundant jump to the immediately-following block (measured:
    go/op_96's own `L3` block, real disassembly has no terminator on
    `idiv %esi` -- control simply continues into `L2`)."""
    if depth > 40:
        raise NotModeled(
            "control flow recursion exceeded 40 -- possible loop, "
            "not modeled by this straight-DAG-only walker")
    steps = blocks.get(label)
    if steps is None:
        raise NotModeled("branch target label %r has no block "
                         "recorded" % label)
    return run_from(sim, blocks, label, steps, 0, depth, order)


def run_from(sim, blocks, label, steps, idx, depth, order):
    while idx < len(steps):
        line = steps[idx].strip()
        if line == "":
            idx = idx + 1
            continue
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem == "ud2":
            raise Trap()
        if mnem == "call":
            raise Trap()
        if mnem == "ret":
            return sim.current_answer()
        if mnem == "jmp":
            target = rest.strip()
            return run_flow(sim, blocks, target, depth + 1, order)
        if mnem.startswith("j") and len(mnem) > 1:
            suffix = mnem[1:]
            target = rest.strip()
            pred = sim.cond_bool(suffix)
            saved_regs = dict(sim.regs)
            saved_flags = dict(sim.last_flags)
            saved_cmp = sim.last_cmp
            saved_rax_w = sim.rax_write_width
            trapped_t = False
            val_t = None
            try:
                val_t = run_flow(sim, blocks, target, depth + 1,
                                  order)
            except Trap:
                trapped_t = True
            sim.regs = dict(saved_regs)
            sim.last_flags = dict(saved_flags)
            sim.last_cmp = saved_cmp
            sim.rax_write_width = saved_rax_w
            trapped_f = False
            val_f = None
            try:
                val_f = run_from(sim, blocks, label, steps,
                                  idx + 1, depth + 1, order)
            except Trap:
                trapped_f = True
            if trapped_t and trapped_f:
                raise Trap()
            if trapped_t:
                return val_f
            if trapped_f:
                return val_t
            v_t, w_t = val_t
            v_f, w_f = val_f
            w = min(w_t, w_f)
            if w_t != w_f:
                v_t = z3.Extract(w - 1, 0, v_t)
                v_f = z3.Extract(w - 1, 0, v_f)
            merged = z3.If(pred, v_t, v_f)
            return merged, w
        sim.exec_line(line)
        idx = idx + 1
    if order and label in order:
        pos = order.index(label)
        if pos + 1 < len(order):
            next_label = order[pos + 1]
            return run_flow(sim, blocks, next_label, depth + 1, order)
    raise NotModeled(
        "block %r fell off its own end without ret/jmp/trap and has "
        "no next block in compiled order to fall through to" % label)


def anchored_check_straight(lang, n, canon4_docs, sem_docs,
                             candidate_text):
    """same contract as canon8_behaviour_check.anchored_check, but
    using Sim9 (adds cltd/cqto/idiv) -- for the 8 STRAIGHT-LINE
    cltd/idiv units (no block structure recorded, so no control-flow
    walk is needed)."""
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this " \
            "unit (canon4_units's own `mnem` field is empty/missing)"
    a_fam, b_fam = real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    if a_fam is not None and a_fam != "rdi":
        shared_seed[a_fam] = seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi":
        shared_seed[b_fam] = seed_family(shared_seed, "rsi")
    sim_real = Sim9(shared_seed, "real")
    sim_cand = Sim9(shared_seed, "cand")
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    return _finish(val_real, w_real, val_cand, w_cand)


def anchored_check_branching(lang, n, canon4_docs, sem_docs):
    """for units WITH block structure (`blocks` real / `derived_
    blocks` candidate, already present on canon4_units_<lang>.json --
    see module header) -- explores both branches via `run_flow` and
    proves the merged answer values equal."""
    rec = canon4_docs[lang].get(n)
    if rec is None:
        return "UNDECIDED", "no canon4_units record for this unit"
    real_block_list = rec.get("blocks")
    cand_block_list = rec.get("derived_blocks")
    if not real_block_list or not cand_block_list:
        return "UNDECIDED", "no block-structured real/derived text " \
            "recorded for this unit (blocks/derived_blocks empty or " \
            "missing)"
    a_fam, b_fam = real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    if a_fam is not None and a_fam != "rdi":
        shared_seed[a_fam] = seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi":
        shared_seed[b_fam] = seed_family(shared_seed, "rsi")
    real_blocks = {}
    for b in real_block_list:
        real_blocks[b["label"]] = b["steps"]
    cand_blocks = {}
    for b in cand_block_list:
        cand_blocks[b["label"]] = b["steps"]
    real_order = [b["label"] for b in real_block_list]
    cand_order = [b["label"] for b in cand_block_list]
    sim_real = Sim9(shared_seed, "real")
    sim_cand = Sim9(shared_seed, "cand")
    try:
        val_real = run_flow(sim_real, real_blocks,
                             real_block_list[0]["label"],
                             order=real_order)
        val_cand = run_flow(sim_cand, cand_blocks,
                             cand_block_list[0]["label"],
                             order=cand_order)
    except Trap:
        return "UNDECIDED", "both the real and candidate control-" \
            "flow walks trapped unconditionally -- no answer value " \
            "on either side to compare (unexpected for a unit with " \
            "a real return value; reported honestly rather than " \
            "guessed)"
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    v_r, w_r = val_real
    v_c, w_c = val_cand
    return _finish(v_r, w_r, v_c, w_c)


def _finish(val_real, w_real, val_cand, w_cand):
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
            "cltd/idiv/branch-flag-modeled) for every value of " \
            "every register either text reads before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample under which " \
            "this text and the unit's own real ship code compute " \
            "DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r" % result
