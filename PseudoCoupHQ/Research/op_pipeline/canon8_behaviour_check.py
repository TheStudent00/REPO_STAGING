#!/usr/bin/env python3
"""canon8_behaviour_check.py -- RE-ANCHORS the behaviour gate to
GROUND TRUTH (this lap's JOB 1, AgentMemory op_pipeline lap 2026-08-29
follow-on).

THE DEFECT THIS FILE FIXES. canon7_behaviour_check.check_pair() proves
a freshly-rendered candidate equal to the unit's PREVIOUS canonical
text (canon5_text/canon7_text -- "the good state"). That is the wrong
anchor when the previous text is itself wrong. canon7's own run found
78 units (ground_truth tally REAL_BYTES_MATCH_NEW_ONLY, recorded on
canon7_units_<lang>.json's `ground_truth_check` field, since no
separate canon7_behaviour_check.json exists on disk -- the brief's
name for that data was a label for the per-unit field, verified by
direct count) where the candidate the OLD gate refused matches the
unit's own REAL DISASSEMBLY and the stored text does not: the gate
was refusing correct renderings because they diverged from a
pre-existing wrong "good" state.

THE FIX: prove every candidate against the unit's OWN REAL SHIP CODE
(canon4_units_<lang>.json's own `mnem` field) DIRECTLY, not against
canon5/canon7's stored text. canon4's `mnem` is verified byte-identical
to op_units_<lang>.json's `probes[n]["ship"]["mnem"]` (spot-checked:
c/op_427, cpp/op_427, go/op_528 -- same list, same order) -- so reading
it off canon4_units is reading the SAME real-ship-code testimony
op_units_<lang>.json carries, already joined onto the unit record; no
new join is needed.

A REGISTER-IDENTITY GAP THE OLD FUNCTION ALSO HAD, discovered while
building this fix. canon4/5/7 text is RENAMED to the canonical
designated registers (a->rdi/edi, b->rsi/esi, per the ratified C
calling rule); real ship code is NOT renamed -- for c/cpp/rust/swift
the System V ABI happens to put a/b in rdi/rsi already, so a literal
text comparison against real mnem accidentally works, but for GO the
real ABI does not follow System V (verified: go/op_528's real mnem is
`cmp %eax,%ebx`, i.e. a arrives in %eax, b in %ebx -- read off
sem_anchored_spill_go.json's own `sem.anchor_registers` field, which
canon7.py already loads as `sem_map` and which is FORCED BY
CONSTRUCTION, the same order-sensitive a-b/b-a compile trick
AgentMemory's evidence doctrine names as the model example). Comparing
`cmp %eax,%ebx` against canonical `cmp %edi,%esi` with the OLD Sim's
plain per-family symbolic seeding treats %eax/%ebx and %edi/%esi as
FOUR unrelated unconstrained values -- any two-argument comparison is
then trivially "DISPROVED" by a same-a-different-b counterexample,
independent of whether the texts actually compute the same thing.
This is the root cause of most of the 98 NEITHER_MATCHES_DIRECTLY
verdicts that are NOT the shift-masking bug (see below): 4 measured
(go/528, go/564, go/600, go/636 -- all `cmp %eax,%ebx; setXX %al`
shapes). THE FIX: before simulating real ship text, PRE-BIND the
shared z3 seed dict so the real argument-carrying family(ies) share
the SAME symbolic value as the canonical rdi/rsi seed would get, read
off `sem.anchor_registers` (`in0` -> a's real family, `in1` -> b's
real family; identity, not a guess -- see sem_anchored.py's own header
for why in0/in1 mean "first/second SOURCE OPERAND", forced by the
a-b/b-a compile order trick). For c/cpp/rust/swift this binding is
almost always a no-op (in0/in1 already name rdi/rsi), verified by
spot-check (c/427: in0=rdi, in1=rsi).

THE SHIFT-COUNT MASKING BUG (the other cause of NEITHER_MATCHES_
DIRECTLY, 82 of 98 measured: 32 c, 32 cpp, 18 rust, every one a
`shl/shr/sar %cl,<dst>` or equivalent shape). canon6_behaviour_check.
ExtSim's %cl-shift handling reads the full 8-bit %cl value and
zero-extends/truncates it to the destination width WITHOUT masking --
so a symbolic %cl value of, say, 200 shifts a 32-bit operand by 200
in the z3 model. Real x86-64 hardware masks the count to 5 bits (mod
32) for an 8/16/32-bit destination and to 6 bits (mod 64) for a 64-bit
destination (Intel SDM, SHL/SHR/SAR) BEFORE using it -- so real
hardware's shift-by-200 is really shift-by-8 (200 mod 32). The
unmasked model and real hardware AGREE on small counts and DISAGREE
on large ones; z3 finds the disagreeing region and reports
DISPROVED/counterexample, which is a MODELING ARTIFACT, not a real
mismatch. FIX: mask the count to 5 bits (width != 64) or 6 bits
(width == 64) before shifting, both for the %cl form and the immediate
form (the immediate form is currently never out-of-range in this
corpus -- verified, compilers already emit legal immediates -- but the
masking is applied uniformly rather than asserted-safe-by-inspection).

12 REMAINING NEITHER_MATCHES_DIRECTLY units (c/427,428,432,438 and
their cpp duplicates: `movslq %edi,%r10; mov %r10d,%eax; and ...`) are
NEITHER of the above -- they are a GENUINE PRE-EXISTING DEFECT in
canon4/5/7's own "good" text: the derived_text round-trips a sign-
extended 64-bit value through a 32-bit register (`mov %r10d,%eax`
zero-extends the LOW 32 bits of the already-sign-extended %r10 back
into %eax, silently discarding the sign-extension movslq just
performed), so both old and new lose to real ground truth. This file
surfaces that (both gv_old and gv_new DISPROVED against real text) but
does NOT attempt to fix canon4's derived_text -- that is a renderer/
canon4 defect, out of THIS file's scope (a behaviour CHECKER, not a
renderer), reported honestly rather than patched over.

REUSES canon7_behaviour_check.Sim7 UNCHANGED for everything except the
%cl/immediate shift branch, which THIS file overrides with the masked
version; movabs/push/pop stay exactly as Sim7 defined them.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon8_behaviour_check.py (library only -- no CLI entry point;
  canon8.py is the driver that calls this file's functions)
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                    # noqa: E402
import canon7_behaviour_check as BC7                             # noqa: E402
import z3                                                        # noqa: E402

LANGS = BC7.LANGS
split_operands = BC7.split_operands
NotModeled = BC7.NotModeled


class Sim8(BC7.Sim7):
    """canon7_behaviour_check.Sim7, plus MASKED shift counts (the fix
    -- see this file's header, "THE SHIFT-COUNT MASKING BUG")."""

    def mask_for_width(self, width):
        if width == 64:
            return 0x3F
        return 0x1F

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem in ("shl", "shr", "sar"):
            operands = split_operands(rest)
            count_op, dst = operands
            width = self.width_of_operand(dst)
            mask = self.mask_for_width(width)
            if count_op == "%cl":
                cl_v = self.read_at(count_op, 8)
            elif count_op.startswith("$"):
                cl_v = z3.BitVecVal(int(count_op[1:], 0) & 0xFF, 8)
            else:
                raise NotModeled(
                    "%s count operand %r is neither %%cl nor an "
                    "immediate -- not modeled" % (mnem, count_op))
            masked8 = cl_v & z3.BitVecVal(mask, 8)
            if width > 8:
                amt = z3.ZeroExt(width - 8, masked8)
            else:
                amt = masked8
            a = self.read_at(dst, width)
            if mnem == "shl":
                r = a << amt
            elif mnem == "shr":
                r = z3.LShR(a, amt)
            else:
                r = a >> amt
            self.write(dst, r)
            return
        BC7.Sim7.exec_line(self, line)


def real_text_of(lang, n, canon4_docs):
    """the unit's own real ship mnemonic text, joined with `; `, read
    off canon4_units_<lang>.json's own `mnem` field -- verified
    byte-identical to op_units_<lang>.json's `probes[n]["ship"]["mnem"]`
    (see file header)."""
    rec = canon4_docs[lang].get(n)
    if rec is None:
        return None
    mnem = rec.get("mnem")
    if not mnem:
        return None
    return "; ".join(mnem)


def real_arg_families(lang, n, sem_docs):
    """(a_family_or_None, b_family_or_None) -- the REAL register
    family (canon.py family name, e.g. "rax") that argument a / b
    arrives in, read off sem_anchored_spill_<lang>.json's own
    `sem.anchor_registers` field (`in0` -> a, `in1` -> b). Returns
    None for a side with no recorded anchor register (e.g. a constant
    fold, or a unit outside this evidence's coverage) -- callers must
    not guess when this is None."""
    doc = sem_docs.get(lang, {})
    rec = doc.get(n)
    if rec is None:
        return None, None
    ar = (rec.get("sem") or {}).get("anchor_registers") or {}
    return ar.get("in0"), ar.get("in1")


def seed_family(shared_seed, family):
    """shared_seed[family], creating a fresh 64-bit symbol under the
    SAME naming convention Sim.get_family uses ("seed_<family>"), so a
    pre-bound family and a lazily-seeded one are indistinguishable to
    the simulator."""
    if family not in shared_seed:
        shared_seed[family] = z3.BitVec("seed_%s" % family, 64)
    return shared_seed[family]


def anchored_check(lang, n, canon4_docs, sem_docs, candidate_text):
    """(verdict, detail) -- z3-checks `candidate_text` against the
    unit's own REAL SHIP CODE directly (THE RE-ANCHORED GATE), with
    the register-identity fix (real arg registers bound to the same
    seed the canonical rdi/rsi family would use) and the shift-mask
    fix (via Sim8). Returns ("UNDECIDED", reason) if there is no real
    text to check against, or if either side hits a NotModeled
    mnemonic/shape."""
    real_text = real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this " \
            "unit (canon4_units's own `mnem` field is empty/missing)"
    a_fam, b_fam = real_arg_families(lang, n, sem_docs)
    shared_seed = {}
    # canonical roles always seed under "rdi"/"rsi" (the designated
    # argument registers); pre-bind the REAL text's argument family
    # to the SAME symbol, so a register-renamed real form and the
    # canonical form start from one shared unconstrained state.
    if a_fam is not None and a_fam != "rdi":
        shared_seed[a_fam] = seed_family(shared_seed, "rdi")
    if b_fam is not None and b_fam != "rsi":
        shared_seed[b_fam] = seed_family(shared_seed, "rsi")
    sim_real = Sim8(shared_seed, "real")
    sim_cand = Sim8(shared_seed, "cand")
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
    solver.add(val_real != val_cand)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved this text equal to the " \
            "unit's own real ship code (register-identity-bound, " \
            "shift-count-masked model) for every value of every " \
            "register either text reads before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample under which " \
            "this text and the unit's own real ship code compute " \
            "DIFFERENT answers: %s" % model
    return "UNDECIDED", "z3 returned %r" % result


def reanchor_unit(lang, n, canon4_docs, sem_docs, old_text, candidate):
    """the JOB 1 decision rule: ACCEPT `candidate` iff it proves equal
    to the unit's own real ship code DIRECTLY -- the old text is no
    longer the anchor, only informative context. Returns a dict with
    the two independent verdicts and the decision, never silently
    dropping either."""
    gv_old, detail_old = anchored_check(
        lang, n, canon4_docs, sem_docs, old_text)
    gv_new, detail_new = anchored_check(
        lang, n, canon4_docs, sem_docs, candidate)
    if gv_new == "PROVED_EQUAL":
        decision = "ACCEPT_CANDIDATE"
    elif gv_old == "PROVED_EQUAL":
        decision = "KEEP_OLD -- old text proved equal to ground " \
            "truth, candidate did not"
    else:
        decision = "KEEP_OLD -- NEITHER text proved equal to ground " \
            "truth (a pre-existing defect this checker surfaces but " \
            "does not fix -- see canon8_behaviour_check.py header)"
    return {
        "ground_truth_verdict_old": gv_old,
        "ground_truth_detail_old": detail_old,
        "ground_truth_verdict_new": gv_new,
        "ground_truth_detail_new": detail_new,
        "decision": decision,
    }
