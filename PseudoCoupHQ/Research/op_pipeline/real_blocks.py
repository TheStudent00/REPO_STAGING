#!/usr/bin/env python3
"""real_blocks.py -- TASK 26: the REAL control-flow blocks of a unit,
built from its own ship BYTES.

WHY THIS FILE EXISTS -- a defect found this lap, forced by canon4.py's
own source. canon4.py lines 772-777 read:

    out["blocks"] = block_records
    out["erased_form"] = erased_flat
    out["derived_blocks"] = block_records

`blocks` and `derived_blocks` are THE SAME LIST OBJECT: both are the
DERIVED (canonicalized, register-renamed) rendering. Measured across
the whole corpus: 88 units carry both fields and in 88 of 88 the two
are byte-identical JSON, 0 differ. So any gate that treats `blocks`
as ground truth and `derived_blocks` as the candidate is comparing a
text with ITSELF -- a circular check that proves nothing. That is
what canon9_behaviour_check.anchored_check_branching does, and what
this lap's first canon30 run inherited.

This file supplies the missing ground truth. It disassembles the
unit's own ship bytes (op_units_<lang>.json's `probes[n]["ship"]
["bytes"]`, the same bytes canon4's `mnem` was printed from) with
capstone ONLY to learn each instruction's OFFSET and LENGTH, then
builds blocks whose step text is objdump's own AT&T mnemonic strings
-- the exact spelling every simulator in this lineage already parses.
capstone is never asked for the instruction text, so no second
spelling convention enters the pipeline.

BLOCK CONSTRUCTION, plainly:
  - leaders: offset 0, every branch target, and the instruction after
    every branch or jump.
  - a block runs from its leader to the next leader.
  - a branch operand `js c <op_549+0xc>` names a byte offset (0xc);
    it is rewritten to that offset's own block label.
  - block labels are `R<offset in hex>`, and the block LIST is in
    ascending offset order -- the real compiled order, which is what
    the branch walker's fall-through rule needs.
  - a target that is not the first byte of any decoded instruction is
    a refusal by name, never a guess.

Coding discipline: no complex/compound one-liner statements.
"""

import re

import capstone


class NotCuttable(Exception):
    pass


BRANCH_TARGET_RE = re.compile(r"^\s*([0-9a-f]+)\s*(<.*>)?\s*$")

# objdump prints a branch target as an ABSOLUTE address followed by
# the symbol-relative form in angle brackets, e.g.
#   js c <op_549+0xc>              (unit based at 0)
#   je 47a658 <main.op_96+0x18>    (unit based at its link address)
# The bracketed `+0x..` is the offset FROM THE UNIT'S OWN SYMBOL,
# which is what a unit-local block cut needs; it is preferred over
# the absolute address whenever objdump printed it, so a slice taken
# from a linked binary cuts exactly like one based at zero. A bare
# `<symbol>` with no `+` names the symbol's first byte, offset 0.
SYMBOL_RELATIVE_RE = re.compile(r"<[^<>]*?\+0x([0-9a-f]+)>")
SYMBOL_START_RE = re.compile(r"<[^<>+]*>")


def decode_offsets(byte_strings):
    """[(offset, length)] for each instruction in the unit's own ship
    bytes, in order. capstone is used ONLY for lengths/offsets."""
    blob = bytes(int(b, 16) for b in byte_strings)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    out = []
    for insn in md.disasm(blob, 0):
        out.append((insn.address, insn.size))
    consumed = 0
    for _, size in out:
        consumed = consumed + size
    if consumed != len(blob):
        raise NotCuttable(
            "capstone decoded %d of %d bytes -- the byte list and the "
            "instruction list do not line up" % (consumed, len(blob)))
    return out


def is_jump(mnem):
    if mnem == "jmp":
        return True
    if mnem.startswith("j") and len(mnem) > 1:
        return True
    return False


def target_offset(rest):
    text = rest.strip()
    m = SYMBOL_RELATIVE_RE.search(text)
    if m is not None:
        return int(m.group(1), 16)
    m = SYMBOL_START_RE.search(text)
    if m is not None:
        return 0
    m = BRANCH_TARGET_RE.match(text)
    if m is None:
        raise NotCuttable(
            "branch operand %r is not a plain hex offset -- not "
            "cuttable" % rest)
    return int(m.group(1), 16)


def build(byte_strings, mnem_lines):
    """[{"label": ..., "steps": [...]}] in ascending-offset order --
    the unit's REAL blocks, step text taken verbatim from
    `mnem_lines`."""
    offsets = decode_offsets(byte_strings)
    if len(offsets) != len(mnem_lines):
        raise NotCuttable(
            "capstone found %d instructions, the recorded mnemonic "
            "list has %d -- not cuttable"
            % (len(offsets), len(mnem_lines)))
    index_of_offset = {}
    for i, pair in enumerate(offsets):
        index_of_offset[pair[0]] = i
    leaders = set([0])
    targets = {}
    for i, line in enumerate(mnem_lines):
        text = line.strip()
        if "!!" in text:
            text = text.split("!!", 1)[0].strip()
        parts = text.split(" ", 1)
        mnem = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if not is_jump(mnem):
            continue
        tgt = target_offset(rest)
        if tgt not in index_of_offset:
            raise NotCuttable(
                "branch target offset 0x%x is not the start of any "
                "decoded instruction -- not cuttable" % tgt)
        targets[i] = tgt
        leaders.add(tgt)
        if i + 1 < len(offsets):
            leaders.add(offsets[i + 1][0])
    ordered_leaders = sorted(leaders)
    label_of = {}
    for off in ordered_leaders:
        label_of[off] = "R%x" % off
    blocks = []
    for pos, off in enumerate(ordered_leaders):
        if pos + 1 < len(ordered_leaders):
            end = ordered_leaders[pos + 1]
        else:
            end = None
        steps = []
        for i, pair in enumerate(offsets):
            ins_off = pair[0]
            if ins_off < off:
                continue
            if end is not None and ins_off >= end:
                break
            text = mnem_lines[i].strip()
            if "!!" in text:
                text = text.split("!!", 1)[0].strip()
            if i in targets:
                parts = text.split(" ", 1)
                mnem = parts[0]
                text = "%s %s" % (mnem, label_of[targets[i]])
            steps.append(text)
        blocks.append({"label": label_of[off], "steps": steps})
    return blocks


def has_branch(mnem_lines):
    for line in mnem_lines:
        text = line.strip()
        parts = text.split(" ", 1)
        if is_jump(parts[0]):
            return True
    return False
