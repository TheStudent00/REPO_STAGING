#!/usr/bin/env python3
"""sret_gate.py -- TASK 31: the ground-truth-anchored gate for a unit
whose answer is a byte image in caller-provided memory.

WHY A NEW GATE, and not canon10_behaviour_check's. That gate compares
ONE register: `answer_home_from_real` reads the last instruction of
the real ship text that writes %xmm0 or an rax-family register, and
z3 is asked whether the two texts agree there. On a memory-return
unit that register holds an ADDRESS, and the answer -- the thing the
caller will read -- is the byte image at that address. A gate that
only compares the address would accept a text that stored the wrong
values into the right place. So the comparison here is the pair:

  (1) the value left in the answer register, AND
  (2) EVERY byte of the image, cell by cell, at the offsets the two
      texts write.

THE COMPARISON IS TOTAL, NOT SAMPLED. The two texts' written cells are
compared as SETS first. If the candidate writes a cell the real text
does not, or misses one the real text writes, the verdict is DISPROVED
with the differing offsets named -- it is never quietly ignored.

THE MODEL. A purpose-built exact symbolic executor over five
instruction shapes and nothing else:

    mov  %reg,%reg          register copy
    mov  %reg,DISP(%base)   integer field write
    movb/movw/movl/movq $imm,DISP(%base)   immediate field write
    movss/movsd %xmm,DISP(%base)           float field write
    ret

Every one of those is modelled EXACTLY -- there is no uninterpreted
function anywhere in this file, because none of these instructions
does arithmetic. Any other mnemonic raises `OutsideVocabulary` and the
unit is UNDECIDED by name. That refusal is the honest boundary of this
gate: it decides nothing it cannot model.

MEMORY KEYING, and the one soundness point in it. A cell is keyed by
(base register family, byte offset), NOT by the operand's literal
spelling -- so `(%rdi)` and `0x0(%rdi)` are the SAME cell, which is
what makes a spelling difference between the two texts harmless while
an offset difference is still caught. Widths are recorded per store
and compared: a 32-bit write and a 64-bit write at the same offset are
different cells and the gate says so.

BOTH TEXTS START FROM THE SAME STATE. One shared seed dictionary
hands out one fresh 64-bit (or 128-bit, for an xmm) symbol per
register family, so `%rsi` means the same unknown value in the real
text and in the candidate. That is the same discipline
canon8_behaviour_check.seed_family uses.

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

Coding discipline: no complex/compound one-liner statements.
"""

import re

import z3

import entry_contract3 as EC3


class OutsideVocabulary(Exception):
    pass


REG_COPY_RE = re.compile(r"^mov\s+%([a-z0-9]+),%([a-z0-9]+)$")
STORE_RE = re.compile(
    r"^(mov|movb|movw|movl|movq|movss|movsd)\s+"
    r"(\S+),(?:(-?0x[0-9a-f]+))?\(%([a-z0-9]+)\)$")


class SretSim(object):
    """the exact symbolic executor. `regs` maps a register FAMILY to
    its current symbolic value; `mem` maps (base family, offset,
    width) to the value stored there."""

    def __init__(self, shared_seed, tag):
        self.shared_seed = shared_seed
        self.tag = tag
        self.regs = {}
        self.mem = {}

    def seed(self, family):
        if family in self.shared_seed:
            return self.shared_seed[family]
        if family.startswith("xmm"):
            width = 128
        else:
            width = 64
        value = z3.BitVec("seed_%s" % family, width)
        self.shared_seed[family] = value
        return value

    def get_family(self, family):
        if family in self.regs:
            return self.regs[family]
        value = self.seed(family)
        self.regs[family] = value
        return value

    def read_register(self, operand, width):
        name = operand[1:]
        family = EC3.FAMILY_OF_REGISTER.get(name)
        if family is None:
            raise OutsideVocabulary(
                "register spelling %r is not in this gate's family "
                "table" % operand)
        full = self.get_family(family)
        if width == full.size():
            return full
        if width > full.size():
            raise OutsideVocabulary(
                "a %d-bit read of the %d-bit register %r"
                % (width, full.size(), operand))
        return z3.Extract(width - 1, 0, full)

    def write_register(self, operand, value):
        name = operand[1:]
        family = EC3.FAMILY_OF_REGISTER.get(name)
        if family is None:
            raise OutsideVocabulary(
                "register spelling %r is not in this gate's family "
                "table" % operand)
        declared = EC3.WIDTH_OF_REGISTER.get(name)
        if declared is None:
            raise OutsideVocabulary(
                "register %r has no declared width" % operand)
        if declared == 64:
            self.regs[family] = value
            return
        if declared == 32:
            self.regs[family] = z3.ZeroExt(32, value)
            return
        if declared == 128:
            self.regs[family] = value
            return
        old = self.get_family(family)
        high = z3.Extract(63, declared, old)
        self.regs[family] = z3.Concat(high, value)

    def exec_line(self, raw):
        line = EC3.clean(raw)
        if line == "":
            return
        if line == "ret":
            return
        m = STORE_RE.match(line)
        if m is not None:
            self.exec_store(m)
            return
        m = REG_COPY_RE.match(line)
        if m is not None:
            source = "%" + m.group(1)
            destination = "%" + m.group(2)
            width = EC3.WIDTH_OF_REGISTER.get(m.group(2))
            if width is None:
                raise OutsideVocabulary(
                    "destination register %r has no declared width"
                    % destination)
            value = self.read_register(source, width)
            self.write_register(destination, value)
            return
        raise OutsideVocabulary(
            "instruction %r is outside this gate's five modelled "
            "shapes -- the unit is UNDECIDED, not guessed at" % line)

    def exec_store(self, m):
        mnem = m.group(1)
        source = m.group(2)
        offset_text = m.group(3)
        base_name = m.group(4)
        base_family = EC3.FAMILY_OF_REGISTER.get(base_name)
        if base_family is None:
            raise OutsideVocabulary(
                "store base %%%s is not in this gate's family table"
                % base_name)
        if offset_text is None:
            offset = 0
        else:
            offset = int(offset_text, 16)
        width = EC3.store_width(mnem, source)
        if source.startswith("$"):
            literal = int(source[1:], 0)
            value = z3.BitVecVal(literal, width)
        else:
            value = self.read_register(source, width)
        self.mem[(base_family, offset, width)] = value


def run(lines, shared_seed, tag):
    sim = SretSim(shared_seed, tag)
    for line in lines:
        sim.exec_line(line)
    return sim


def check(real_lines, candidate_lines):
    """(verdict, detail). Verdicts: PROVED_EQUAL, DISPROVED,
    UNDECIDED."""
    shared_seed = {}
    try:
        sim_real = run(real_lines, shared_seed, "real")
        sim_cand = run(candidate_lines, shared_seed, "cand")
    except OutsideVocabulary as exc:
        return "UNDECIDED", str(exc)
    keys_real = set(sim_real.mem.keys())
    keys_cand = set(sim_cand.mem.keys())
    if keys_real != keys_cand:
        only_real = sorted(keys_real - keys_cand)
        only_cand = sorted(keys_cand - keys_real)
        return "DISPROVED", (
            "the two texts write DIFFERENT cells of the answer "
            "image: only the real ship code writes %r, only the "
            "candidate writes %r (each cell is base family, byte "
            "offset, width in bits)" % (only_real, only_cand))
    obligations = []
    answer_family = EC3.FAMILY_OF_REGISTER[EC3.ANSWER_REGISTER]
    value_real = sim_real.get_family(answer_family)
    value_cand = sim_cand.get_family(answer_family)
    obligations.append(("answer register %%%s" % EC3.ANSWER_REGISTER,
                        value_real, value_cand))
    for key in sorted(keys_real):
        label = "image cell base=%%%s offset=0x%x width=%d" % (
            key[0], key[1], key[2])
        obligations.append((label, sim_real.mem[key],
                            sim_cand.mem[key]))
    for label, left, right in obligations:
        solver = z3.Solver()
        solver.add(left != right)
        outcome = solver.check()
        if outcome == z3.unsat:
            continue
        if outcome == z3.sat:
            return "DISPROVED", (
                "z3 found a counterexample under which the candidate "
                "and the unit's own real ship code disagree in the "
                "%s: %s" % (label, solver.model()))
        return "UNDECIDED", "z3 returned %r on the %s" % (
            outcome, label)
    names = []
    for label, _l, _r in obligations:
        names.append(label)
    return "PROVED_EQUAL", (
        "z3 proved the candidate equal to the unit's own real ship "
        "code in every one of the %d compared places (%s), for every "
        "value of every register either text reads before writing"
        % (len(obligations), "; ".join(names)))
