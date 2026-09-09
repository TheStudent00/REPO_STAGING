#!/usr/bin/env python3
"""t96_step.py -- THE SEVENTH BLOCK KIND, AS MACHINE STATE, STEPPED.

TASK 96, round 19.  `LLM_communication_protocol.md` section 4.6: when
the subject is what a machine does, the explanation is the STATE,
stepped, with real values -- not prose about it.

This program steps `php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_
TMPVARCV_HANDLER` -- the one straight-line whole handler in the
population, ten instructions -- three times over the same starting
values:

    FORM 1  region36: refused by name before it runs, because the form
            claims %r15 as its region base and this body uses %r15 as
            its own bytecode pointer.  The refusal is printed as the
            step that never happens.
    FORM 2  canonical_form.py, unmodified.  The body runs; but nothing
            in the form says where %r15 and %r14 came from.
    FORM 3  the same, plus the seventh block kind: the prelude loads
            each arriving area's base out of the ledger.

The instructions are READ from `t96_canonical.json`, not typed here.
The starting values are an ILLUSTRATIVE INSTANTIATION of a real body,
said once: two php integers 3 and 4 in the value frame, and a bytecode
that names slot 0x00 for the first operand, 0x10 for the second and
0x20 for the answer.  Everything else -- which register changes, at
which step, to what -- is computed by the stepper from the actual
instruction text.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.

usage:
  t96_step.py
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SOURCE = os.path.join(HERE, "t96_canonical.json")
UNIT = ("php/ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_"
        "HANDLER")

# the illustrative instantiation, stated once.
LEDGER_AT = 0x600000
AREA_AT = 0x700000          # the AREA block, as the ledger names it
OPCODE_AT = 0x700000        # AREA-0, extent 0: the bytecode
FRAME_AT = 0x700100         # AREA-1, extent 1: the value frame
OUT_AT = 0x500000           # the OUT block


def start_memory():
    """the bytes the runner puts down before the unit is entered.

    the bytecode: the current opcode names its first operand at frame
    offset 0x00 and its second at 0x10; the NEXT opcode, 0x20 further
    on, names the answer slot at 0x10 -- which the body reads as
    -0x10 from the advanced pointer.
    """
    memory = {}
    memory[OPCODE_AT + 0x8] = 0x00      # first operand's slot
    memory[OPCODE_AT + 0xc] = 0x10      # second operand's slot
    memory[OPCODE_AT + 0x20 - 0x10] = 0x20   # the answer's slot
    memory[FRAME_AT + 0x00] = 3         # the php integer 3
    memory[FRAME_AT + 0x10] = 4         # the php integer 4
    return memory


REGISTERS = ("r15", "r14", "rcx", "rax", "rdx", "r11")

MEM_OPERAND = re.compile(
    r"^(-?0x[0-9a-f]+)?\((%[a-z0-9]+)(?:,(%[a-z0-9]+),([1248]))?\)$")
IMMEDIATE = re.compile(r"^\$(-?0x[0-9a-f]+|-?\d+)$")
LEDGER_OPERAND = re.compile(r"^ledger\+0x([0-9a-f]+)\(%rip\)$")


def family_of(text):
    name = text.lstrip("%")
    table = {
        "eax": "rax", "ecx": "rcx", "edx": "rdx",
        "r11d": "r11", "r14d": "r14", "r15d": "r15",
    }
    return table.get(name, name)


class Machine(object):
    def __init__(self, ledger_entries, seed=None):
        self.registers = {}
        for name in REGISTERS:
            self.registers[name] = None
        for name, value in (seed or {}).items():
            self.registers[name] = value
        self.memory = start_memory()
        self.ledger = dict(ledger_entries)
        self.notes = []

    def value_of(self, operand):
        hit = IMMEDIATE.match(operand)
        if hit is not None:
            text = hit.group(1)
            if text.startswith("0x") or text.startswith("-0x"):
                return int(text, 16)
            return int(text, 10)
        hit = LEDGER_OPERAND.match(operand)
        if hit is not None:
            return self.ledger.get(int(hit.group(1), 16))
        if operand.startswith("%"):
            return self.registers.get(family_of(operand))
        address = self.address_of(operand)
        if address is None:
            return None
        return self.memory.get(address)

    def address_of(self, operand):
        hit = MEM_OPERAND.match(operand)
        if hit is None:
            return None
        text = hit.group(1)
        base = self.registers.get(family_of(hit.group(2)))
        if base is None:
            return None
        displacement = 0
        if text is not None:
            displacement = int(text, 16)
        index = 0
        if hit.group(3) is not None:
            held = self.registers.get(family_of(hit.group(3)))
            if held is None:
                return None
            index = held * int(hit.group(4))
        return base + displacement + index

    def step(self, line):
        parts = line.split(" ", 1)
        mnemonic = parts[0]
        if len(parts) == 1:
            return "%s -- nothing changes" % mnemonic
        operands = split_operands(parts[1])
        if mnemonic in ("mov", "movslq", "movl", "lea"):
            return self.move(mnemonic, operands)
        if mnemonic == "add":
            return self.add(operands)
        return "%s -- not stepped" % mnemonic

    def move(self, mnemonic, operands):
        source, destination = operands[0], operands[1]
        if mnemonic == "lea":
            value = self.address_of(source)
        else:
            value = self.value_of(source)
        return self.write(destination, value)

    def add(self, operands):
        source, destination = operands[0], operands[1]
        one = self.value_of(source)
        two = self.value_of(destination)
        if one is None or two is None:
            return "add -- an operand is not known"
        return self.write(destination, one + two)

    def write(self, destination, value):
        if destination.startswith("%"):
            family = family_of(destination)
            self.registers[family] = value
            return "%%%s = %s" % (family, show(value))
        address = self.address_of(destination)
        if address is None:
            return "a store whose address is not known"
        self.memory[address] = value
        return "[%s] = %s" % (show(address), show(value))


def split_operands(text):
    out = []
    depth = 0
    piece = ""
    for character in text:
        if character == "(":
            depth = depth + 1
        if character == ")":
            depth = depth - 1
        if character == "," and depth == 0:
            out.append(piece.strip())
            piece = ""
            continue
        piece = piece + character
    if piece.strip():
        out.append(piece.strip())
    return out


def show(value):
    if value is None:
        return "?"
    if value < 0:
        return "-0x%x" % (-value)
    return "0x%x" % value


def run(title, lines, ledger_entries, seed=None):
    print("")
    print("=" * 72)
    print(title)
    print("=" * 72)
    machine = Machine(ledger_entries, seed)
    header = "%-4s %-34s" % ("step", "instruction")
    for name in REGISTERS:
        header = header + " %-10s" % ("%" + name)
    print(header)
    print("-" * len(header))
    row = "%-4s %-34s" % ("--", "(entry)")
    for name in REGISTERS:
        row = row + " %-10s" % show(machine.registers[name])
    print(row)
    for index, line in enumerate(lines):
        note = machine.step(line)
        row = "%-4d %-34s" % (index, line)
        for name in REGISTERS:
            row = row + " %-10s" % show(machine.registers[name])
        print(row)
        machine.notes.append((index, line, note))
    print("")
    print("what each step did:")
    for index, line, note in machine.notes:
        print("  %-4d %-34s %s" % (index, line, note))
    print("")
    print("memory, at the end:")
    for address in sorted(machine.memory):
        where = name_of_address(address)
        print("  %-12s %-34s %s"
              % (show(address), where, show(machine.memory[address])))
    return machine


def name_of_address(address):
    if OPCODE_AT <= address < OPCODE_AT + 0x100:
        return "AREA-0 (the bytecode) + 0x%x" % (address - OPCODE_AT)
    if FRAME_AT <= address < FRAME_AT + 0x100:
        return "AREA-1 (the value frame) + 0x%x" % (address - FRAME_AT)
    if OUT_AT <= address < OUT_AT + 0x40:
        return "OUT-0 (the answer) + 0x%x" % (address - OUT_AT)
    return "outside every block this form names"


def main():
    document = json.load(open(SOURCE))
    record = None
    for candidate in document["records"]:
        if candidate["unit"] == UNIT:
            record = candidate
            break
    if record is None:
        print("the unit is not in %s" % SOURCE)
        return 1

    print("THE UNIT: %s" % UNIT)
    print("the illustrative instantiation, stated once:")
    print("  the ledger sits at %s" % show(LEDGER_AT))
    print("  its AREA entry (0x40) holds %s" % show(AREA_AT))
    print("  its OUT  entry (0x38) holds %s" % show(OUT_AT))
    print("  AREA-0, extent 0x000, is the bytecode at %s"
          % show(OPCODE_AT))
    print("  AREA-1, extent 0x100, is the value frame at %s"
          % show(FRAME_AT))
    print("  the value frame holds the php integer 3 at +0x00 and 4 "
          "at +0x10")
    print("  the bytecode names slot 0x00, then 0x10, then (one "
          "opcode on) 0x20")

    old = record["the_superseded_form"]
    print("")
    print("=" * 72)
    print("FORM 1 -- region36 + canon36_universal (SUPERSEDED RECORD)")
    print("=" * 72)
    print("there is no state to step: the form refused this unit "
          "before rendering it.")
    print("its own words:")
    print("  %s" % old.get("refusal"))

    ledger_entries = {0x38: OUT_AT, 0x40: AREA_AT}

    two = record["the_canonical_form"]
    lines = two["wrapped_text"].split("; ")
    run("FORM 2 -- canonical_form.py, unmodified (PART A)", lines,
        ledger_entries, {"r15": OPCODE_AT, "r14": FRAME_AT})
    print("READ THIS AGAINST THE ENTRY ROW: %r15 and %r14 are "
          "already filled at (entry), and NOTHING in the form put "
          "them there.  The body runs; the form says nothing about "
          "where its operands came from.")

    three = record["the_canonical_form_with_the_seventh_block"]
    if three.get("outcome") == "REFUSED":
        print("")
        print("FORM 3 refused: %s" % three.get("refusal"))
        return 0
    lines = three["wrapped_text"].split("; ")
    print("")
    print("(for FORM 3 the entry row is EMPTY: nothing is assumed. "
          "for FORM 2 above, %r15 and %r14 had to be handed to the "
          "stepper, because the form does not fill them)")
    run("FORM 3 -- canonical_form.py + the seventh block kind "
        "(PART B)", lines, ledger_entries, {})
    print("READ THIS AGAINST THE ENTRY ROW: every register starts "
          "unknown.  Steps 0 to 2 are the form's own prelude, and "
          "they put each arriving area's base into the register the "
          "body itself expects it in.  The body is byte-identical "
          "to FORM 2's.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
