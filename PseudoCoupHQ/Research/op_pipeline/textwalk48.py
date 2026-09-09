#!/usr/bin/env python3
"""textwalk48.py -- THE SECOND GATE ROUTE: the body walked in TEXT
ORDER, with the same producer table layer 4 uses.

WHY A SECOND ROUTE EXISTS, said plainly.  The first route (gate48.py)
compares the transcribed term against the behaviour checker's own
simulator.  That simulator carries the scalar-float vocabulary as
UNINTERPRETED FUNCTIONS, so on any unit whose body spells a float
opcode the two sides cannot be compared at all, and the verdict there
is UNDECIDED.  That would leave the float half of the corpus with no
gate.

WHAT THIS ROUTE TESTS, and what it does not.  It walks the unit's own
body one instruction at a time, keeping a register-to-term map, and
builds the answer from the register the unit's own result home names.
It uses layer4.py's producer table for the meaning of each opcode.  So
it shares the SEMANTICS with layer 4 and shares nothing else: the
layer-4 side reads the PROVENANCE LEDGER's graph, this side reads the
ARCH TEXT's order.  Agreement is therefore evidence about the LEDGER'S
WIRING -- which is exactly what needed testing, and exactly what the
implicit-destination family (the division opcodes) fails.  It is NOT
evidence about the producer table itself; route one is what tests that,
and every claim below says which route carried it.

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
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                      # noqa: E402
import layer4                                                     # noqa: E402
import ledger47 as L47                                            # noqa: E402
import region36 as R36                                            # noqa: E402
import z3                                                         # noqa: E402


class NotWalkable(Exception):
    """this body cannot be walked in text order by this file."""


def is_flag_reader(mnemonic):
    for prefix in ("set", "cmov", "j"):
        if mnemonic.startswith(prefix) and len(mnemonic) > len(prefix):
            suffix = mnemonic[len(prefix):]
            if suffix in layer4.CT.SUFFIX_TO_COND or \
                    suffix in ("o", "no"):
                return True
    return False


def walk(unit):
    """the value the unit's own body leaves in its own answer home, as
    a term over the same symbols layer 4 uses."""
    registers = {}
    seeds = {}
    memory = {}
    rip_index = [0]
    flags = {"flags": None}
    last_setter = [None]
    for binding in unit.get("arrival_contract_bindings", []):
        register = binding.get("bound_to_the_same_symbol_as", "")
        family = canon.FAMILY_OF.get(register[1:])
        if family is None:
            continue
        registers[family] = layer4.seed_of(seeds, family, "a")
    for raw in unit["body_verbatim"]:
        line = R36.strip_annotation(raw)
        if line.endswith(":") or line == "" or line == "ret":
            continue
        mnemonic = L47.mnemonic_of(line)
        if mnemonic is None:
            continue
        if mnemonic.startswith("j") and not is_flag_reader(mnemonic):
            continue
        if mnemonic in ("call", "ud2", "nop", "hlt") or \
                mnemonic.startswith("j"):
            if mnemonic in ("call", "ud2"):
                raise NotWalkable(
                    "the body transfers out of the unit (%r), so a "
                    "text-order walk has no answer to reach" % line)
            continue
        operands = L47.operands_of(line)
        slots = []
        for position, operand in enumerate(operands):
            value = L47.immediate_value(operand)
            if value is not None:
                slots.append(layer4.Slot(operand, None,
                                         immediate=value))
                continue
            if operand.startswith("%"):
                family = layer4.family_of(operand)
                slot = layer4.Slot(operand, None)
                slot.family = family
                if family is not None:
                    if family not in registers:
                        registers[family] = layer4.seed_of(
                            seeds, family, "a")
                    slot.term = registers[family]
                slots.append(slot)
                continue
            inner = []
            if "(%rip)" in operand:
                inner.append(("rip", ("rip", rip_index[0])))
                rip_index[0] += 1
            for token in re.findall(r"%[a-z0-9]+", operand):
                family = canon.FAMILY_OF.get(token[1:])
                if family is None:
                    continue
                if family not in registers:
                    registers[family] = layer4.seed_of(seeds, family,
                                                       "a")
                inner.append((token, registers[family]))
            for hit in R36.RSP_DISP.finditer(operand):
                displacement = int(hit.group(1), 16)
                key = "own_%x" % displacement
                if key not in memory:
                    memory[key] = z3.BitVec("seed_rsp", 64) - \
                        z3.BitVecVal(displacement, 64)
                inner.append(("own", memory[key]))
            slot = layer4.Slot(operand, None, memory=inner)
            slot.term = layer4.memory_load_term(slot, seeds, "a")
            slots.append(slot)
        for slot in slots:
            if slot.immediate is not None:
                slot.term = z3.BitVecVal(
                    slot.immediate & ((1 << 64) - 1), 64)
        row = {"row": "walk", "size": 8, "block": "TEMP"}
        producer = mnemonic
        if is_flag_reader(mnemonic):
            producer = [last_setter[0], mnemonic]
        try:
            value = layer4.build_producer_term(producer, line, slots,
                                               row, flags)
        except layer4.NoTerm as problem:
            raise NotWalkable("%s" % problem.why)
        if L47.sets_the_flags(mnemonic):
            last_setter[0] = mnemonic
            try:
                found = layer4.flags_of(mnemonic, slots, line, value)
            except Exception:
                found = None
            if found is not None:
                flags["flags"] = found
        if not operands:
            continue
        destination = operands[-1]
        family = layer4.family_of(destination)
        if family is None:
            continue
        if family in canon.NEVER_RENAME:
            continue
        if mnemonic in layer4.FLAG_ONLY:
            continue
        registers[family] = value
    home = unit["result_family"]
    if home not in registers:
        raise NotWalkable(
            "the answer home %r is never written by this body, so the "
            "walk has no answer" % home)
    return layer4.cut(registers[home], unit["result_width"])


def gate(unit, transcription, milliseconds=3000):
    """(verdict, detail) -- the transcribed term against the same body
    walked in text order."""
    if transcription.out_term is None:
        return "UNDECIDED", "layer 4 built no term for OUT-0"
    try:
        theirs = walk(unit)
    except NotWalkable as problem:
        return "UNDECIDED", "the text-order walk: %s" % problem
    except Exception as problem:
        return "UNDECIDED", ("the text-order walk raised %s: %s"
                             % (type(problem).__name__, problem))
    ours = transcription.out_term
    if ours.size() != theirs.size():
        narrow = min(ours.size(), theirs.size())
        ours = z3.Extract(narrow - 1, 0, ours)
        theirs = z3.Extract(narrow - 1, 0, theirs)
    solver = z3.Solver()
    solver.set("timeout", milliseconds)
    try:
        solver.add(ours != theirs)
        answer = solver.check()
    except Exception as problem:
        return "UNDECIDED", "z3 raised %s" % problem
    if answer == z3.unsat:
        return "PROVED_EQUAL", (
            "z3 proved the ledger-transcribed OUT-0 term equal to the "
            "same body walked in text order, for every value of every "
            "register either walk reads before writing")
    if answer == z3.sat:
        return "DISPROVED", (
            "z3 found a starting state under which the ledger's own "
            "wiring and the body's text order give different answers: "
            "%s" % solver.model())
    return "UNDECIDED", "z3 returned %r" % answer
