#!/usr/bin/env python3
"""canon33_fixes.py -- two causes found while the newly-rendered units
were being gated, fixed at first observation (AgentMemory, 2026-08-28).

Both were already in canon4.py's deriving pass.  Neither could be SEEN
before this lap, because every unit that exposes them was refused
earlier, at the two-parked-operands rule, and so never reached a gate.
Both are fixed HERE, in a new file, and installed by rebinding
canon4's module globals in the driver's own process.  canon4.py is not
edited.

CAUSE 1 -- A FALL-THROUGH BLOCK EMITS NO JUMP, BUT THE BLOCKS ARE
REORDERED.  canon4.py emits a unit's blocks in the order its path
walk discovered them, which is NOT their address order (it cannot be:
one block can be rendered several times, once per incoming path).  A
block that ends in a conditional branch is safe -- canon4 already
makes both edges explicit, the branch to its target and a `jmp` to
its fall-through.  A block with NO control instruction at all was
given nothing, so it silently fell into whichever block happened to
be printed next.

  MEASURED: `cpp/op_765`.  Its real ship code runs L0, L1, L2, L3 in
  address order; the walk discovered L0, L2, L1, L3.  L2 ends with
  `addss` and no control instruction, so in the rendered text it fell
  into L1 -- which recomputes the conversion and discards L2's work.
  The gate DISPROVED it with a counterexample.  Fixed here, the same
  unit proves equal.

  THE FIX: when a block record carries no control instruction and has
  exactly ONE successor, emit `jmp <that successor's label>`.  The
  successor label is the one canon4's own walk already recorded in
  `succ_labels`; nothing is inferred.  Zero successors emits nothing,
  as before.  Two or more without a control instruction is impossible
  and refuses by name.

CAUSE 2 -- THE DEAD-MOV CLEANUP IS ALIAS-BLIND.  canon4's
`dead_mov_cleanup` deletes a `mov` whose destination text does not
appear again later in the text.  It compares SPELLINGS.  `%rcx`,
`%ecx`, `%cx` and `%cl` are four spellings of one register.

  MEASURED: `swift/op_703`.  A variable shift count is hardware-pinned
  to `%cl`, so the deriving pass emits `mov %esi,%ecx` and the shift
  then reads `%cl`.  The cleanup searched the later text for the
  literal `%ecx`, did not find it (the later text says `%cl`), and
  deleted the mov -- leaving the shift reading whatever was in `%cl`.
  The gate DISPROVED it: with `b = 64`, `%cl = 8`, the two texts shift
  by different amounts.

  THE FIX: resolve the destination to its register FAMILY (canon.py's
  own FAMILY_OF) and look for ANY spelling of that family
  (canon.py's own GP_NAMES row) in the later text.  Same heuristic,
  same conservatism, one table lookup wider.

CAUSE 3 -- THE ANSWER MOVE IS ALWAYS 32 BITS.  Both of canon4's
return paths land the finished value in the answer register with a
move rendered at width index 1, which is the 32-bit alias:
`ensure(final_name, contract["result"], 1)` in the straight-line
derive, and `render(cur, 1)` / `render(target, 1)` in
`render_control_line`'s `ret` case.  A 64-bit answer is TRUNCATED by
that move.  The unit computes the right value and returns the wrong
one.

  MEASURED: `swift/op_703`.  Its answer is a 64-bit shifted value; the
  ship code carries it in `%rax`.  The candidate ended `mov %edi,%eax`
  and the gate DISPROVED it with `b = 11`,
  `a = 4914318053212165` -- an answer above 2^32, where the truncation
  shows.

  THE FIX: render the answer move at width index 0 (the 64-bit alias).
  This is never worse than the 32-bit move and is right whenever the
  answer is wider than 32 bits: a value computed by a 32-bit write
  already has zeroes in bits 32-63 on x86-64, so the 64-bit move
  carries exactly what the 32-bit move carried; a value computed at 64
  bits is carried whole instead of cut.

THE SPELLING BAN.  No operator token appears in this file.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402
import canon2  # noqa: E402
import canon4  # noqa: E402

Erasure = canon2.Erasure

# captured at import time, BEFORE the driver rebinds canon4's globals
# -- calling canon4.render_control_line after the rebinding would call
# this file's own replacement and recurse for ever (measured: a
# RecursionError on 25 units the first time this file was installed).
ORIGINAL_RENDER_CONTROL_LINE = canon4.render_control_line


def family_spellings(destination_text):
    """every rendered spelling of the register family the given
    operand text names, or None when the text is not a plain
    register."""
    if not destination_text.startswith("%"):
        return None
    name = destination_text[1:]
    family = canon.FAMILY_OF.get(name)
    if family is None:
        return None
    if canon.is_vector(family):
        return ["%" + family]
    row = canon.GP_NAMES.get(family)
    if row is None:
        return None
    out = []
    for spelling in row:
        out.append("%" + spelling)
    return out


def dead_mov_cleanup33(lines, contract):
    """canon4.dead_mov_cleanup, with CAUSE 2 fixed: a destination is
    dead only when NO spelling of its register family is read later."""
    protected = canon4.answer_register_texts(contract)
    lines = list(lines)
    changed = True
    while changed:
        changed = False
        for i, line in enumerate(lines):
            if not line.startswith("mov "):
                continue
            try:
                _, operands = line.split(" ", 1)
                destination = operands.split(",")[-1]
            except ValueError:
                continue
            if not destination.startswith("%"):
                continue
            if destination in protected:
                continue
            spellings = family_spellings(destination)
            if spellings is None:
                spellings = [destination]
            rest = " ".join(lines[i + 1:])
            still_read = False
            for spelling in spellings:
                if spelling in rest:
                    still_read = True
                    break
            if still_read:
                continue
            del lines[i]
            changed = True
            break
    return lines


def widen_answer_move(lines):
    """CAUSE 3 on the branching return path: the `mov` that lands the
    returned value in the answer register is re-rendered at the 64-bit
    alias of the SAME two registers.  Only a register-to-register
    `mov` immediately before `ret` is touched, and only when both
    spellings resolve through canon.py's own tables."""
    if len(lines) < 2:
        return lines
    if lines[-1] != "ret":
        return lines
    line = lines[-2]
    if not line.startswith("mov "):
        return lines
    _, operands = line.split(" ", 1)
    parts = operands.split(",")
    if len(parts) != 2:
        return lines
    source, destination = parts[0].strip(), parts[1].strip()
    if not source.startswith("%") or not destination.startswith("%"):
        return lines
    source_family = canon.FAMILY_OF.get(source[1:])
    destination_family = canon.FAMILY_OF.get(destination[1:])
    if source_family is None or destination_family is None:
        return lines
    if canon.is_vector(source_family) or canon.is_vector(
            destination_family):
        return lines
    wide = "mov %%%s,%%%s" % (canon.GP_NAMES[source_family][0],
                              canon.GP_NAMES[destination_family][0])
    out = list(lines)
    out[-2] = wide
    return out


def render_control_line33(rec, contract, walker):
    """canon4.render_control_line, with CAUSE 1 and CAUSE 3 fixed."""
    if rec.get("control") is not None:
        return widen_answer_move(
            ORIGINAL_RENDER_CONTROL_LINE(rec, contract, walker))
    labels = rec.get("succ_labels") or []
    if not labels:
        return []
    if len(labels) == 1:
        return ["jmp %s" % labels[0]]
    raise Erasure(
        "erasure_refused: a block with no control instruction has %d "
        "successors, which cannot happen in a cut block set -- "
        "refused rather than guessed" % len(labels))
