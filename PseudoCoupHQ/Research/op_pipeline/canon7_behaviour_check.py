#!/usr/bin/env python3
"""canon7_behaviour_check.py -- THE BEHAVIOUR GATE for canon7.

Mandatory per this lap's brief: every unit whose text changes must be
z3-proved equivalent to its previous canonical text (canon5_text, the
good state) BEFORE the new text is written; anything disproved or
undecided KEEPS THE OLD TEXT and is recorded with its reason.
Disproved cases are cross-checked against the unit's own real
disassembly (canon4's own `mnem`), same as canon5_behaviour_check.py/
canon6_behaviour_check.py already do.

REUSES canon6_behaviour_check.ExtSim UNCHANGED (which itself reuses
canon5_behaviour_check.Sim UNCHANGED) -- this file adds exactly one
new thing to the modeled vocabulary: `push`/`pop`, needed because
canon7_render.py's ordered temp pool can spill into the callee-saved
tier (%rbx/%r12../%r15) and wraps the unit in a push/pop pair when it
does. Modeled as a symbolic stack (a Python list of z3 values) --
sufficient for a straight-line push-body-pop-ret sequence, which is
the only shape canon7_render.py ever emits.

A CAVEAT ON EVIDENCE CLASS, stated honestly (the evidence doctrine
requires it): canon5_behaviour_check.Sim.write() zero-extends EVERY
sub-64-bit write up to the full 64-bit family register, unconditionally
-- an over-approximation of real x86-64 (which only auto-zero-extends
a 32-bit write; an 8/16-bit write leaves the upper bits alone). This
checker's PROVED_EQUAL is therefore a proof of the SIMPLIFIED symbolic
model, not a bit-for-bit hardware claim, for any pair where an 8/16-
bit answer is compared without a following 32-bit-native write. This
lap's own fix (canon7_render.py's answer-width convention) makes every
canon7 answer finish at a native 32/64-bit write, which closes the gap
for canon7's own outputs; it is recorded here rather than silently
relied on.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon7_behaviour_check.py [--in DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon6_behaviour_check as C6BC                          # noqa: E402
import z3                                                       # noqa: E402

LANGS = C6BC.LANGS
split_operands = C6BC.split_operands
NotModeled = C6BC.NotModeled


class Sim7(C6BC.ExtSim):
    """canon6_behaviour_check.ExtSim, plus push/pop."""

    def __init__(self, shared_seed, tag):
        C6BC.ExtSim.__init__(self, shared_seed, tag)
        self.push_stack = []

    def exec_line(self, line):
        line = line.strip()
        parts = line.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if mnem == "movabs":
            # `movabs $imm,%reg64` is semantically an ordinary `mov`
            # of an immediate into a register -- GAS only requires
            # the distinct mnemonic because a plain `mov` cannot
            # encode a 64-bit immediate that does not fit in 32
            # signed bits. Neither canon5_behaviour_check.Sim nor
            # canon6_behaviour_check.ExtSim modeled it (never
            # exercised by their own corpora); canon7_render.py's own
            # mask-immediate-width fix (item 3, this lap) is the
            # first thing in this pipeline to emit it at scale, so
            # it is modeled here rather than left UNDECIDED by name
            # only.
            self.exec_line("mov " + rest)
            return
        if mnem == "push":
            (reg,) = split_operands(rest)
            width = self.width_of_operand(reg)
            self.push_stack.append(self.read_at(reg, width))
            return
        if mnem == "pop":
            (reg,) = split_operands(rest)
            if not self.push_stack:
                raise NotModeled(
                    "pop with an empty symbolic push stack -- "
                    "unbalanced push/pop in this text")
            v = self.push_stack.pop()
            self.write(reg, v)
            return
        C6BC.ExtSim.exec_line(self, line)


def check_pair(text_a, text_b):
    lines_a = [ln.strip() for ln in text_a.split(";")]
    lines_b = [ln.strip() for ln in text_b.split(";")]
    shared_seed = {}
    sim_a = Sim7(shared_seed, "a")
    sim_b = Sim7(shared_seed, "b")
    try:
        val_a, w_a = sim_a.answer_value(lines_a)
        val_b, w_b = sim_b.answer_value(lines_b)
    except NotModeled as exc:
        return "UNDECIDED", str(exc)
    if w_a != w_b:
        w = min(w_a, w_b)
        val_a = z3.Extract(w - 1, 0, val_a)
        val_b = z3.Extract(w - 1, 0, val_b)
    solver = z3.Solver()
    solver.add(val_a != val_b)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED_EQUAL", "z3 proved the two answer values " \
            "equal for every value of every register either text " \
            "reads before writing"
    if result == z3.sat:
        model = solver.model()
        return "DISPROVED", "z3 found a counterexample machine " \
            "state under which the two texts compute DIFFERENT " \
            "answers: %s" % model
    return "UNDECIDED", "z3 returned %r" % result


def ground_truth_check(lang, n, canon4_docs, old_text, new_text):
    """cross-check a DISPROVED pair against the unit's own real
    disassembly (canon4's own `mnem`) -- forced-by-construction
    ground truth, same pattern as canon5_behaviour_check.py /
    canon6_behaviour_check.py."""
    real_mnem = canon4_docs[lang][n].get("mnem") or []
    real_text = "; ".join(real_mnem)
    gv_old, _ = check_pair(real_text, old_text)
    gv_new, _ = check_pair(real_text, new_text)
    if gv_new == "PROVED_EQUAL" and gv_old != "PROVED_EQUAL":
        return "REAL_BYTES_MATCH_NEW_ONLY -- the unit's own real " \
            "disassembly proves canon7_text correct and the old " \
            "(canon5) text WRONG (a pre-existing defect, not a " \
            "canon7 regression)"
    if gv_old == "PROVED_EQUAL" and gv_new != "PROVED_EQUAL":
        return "REAL_BYTES_MATCH_OLD_ONLY -- the unit's own real " \
            "disassembly proves the old (canon5) text correct and " \
            "canon7_text WRONG -- KEEPING THE OLD TEXT"
    if gv_old == "PROVED_EQUAL" and gv_new == "PROVED_EQUAL":
        return "REAL_BYTES_MATCH_BOTH (should be impossible -- " \
            "flagged for review)"
    return "NEITHER_MATCHES_DIRECTLY (gv_old=%s gv_new=%s)" % (
        gv_old, gv_new)
