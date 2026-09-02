#!/usr/bin/env python3
"""arrival_modes.py -- ARRIVAL REPRESENTATION AS A TRACKED DIMENSION.

the owner's ruling, log_115 (2026-09-01), both halves: "(1) log the
pointer-types as part of tracked modes, then (2) simplify the
expression so the unit is no longer a pointer unit; OR standardize the
canonical form as pointer-based everywhere so everything is uniform.
Two canon units agreeing on the simplified instructions but differing
in modes is INFORMATION for dominant-operator decisions, not a
nuisance -- record the difference, never discard it."

THE VOCABULARY.  Three arrival representations, and no fourth is
invented:

  plain               the operand arrives AS ITS VALUE in its seat.
  typed-pointer(T)    the operand arrives as the ADDRESS of a T; the
                      value is behind one or more field reads.
  tagged              the operand arrives as a machine word that is
                      sometimes a value and sometimes a pointer,
                      told apart by bits of the word itself.

A MODE IS MEASURED, NOT DECLARED, WHEREVER THE MACHINE FORM CAN
DECIDE IT.  For a compiled unit the test is over the unit's own ship
text and nothing else:

    an argument's arrival register is DEREFERENCED by the unit --
    it appears as the base of a memory operand -- if and only if the
    operand arrived as an address.

`plain` is therefore a MEASUREMENT on the compiled corpus, not an
assumption carried in from the brief.  The brief says compiled units
are plain; this file checks it and would report any unit that is not.

For an interpreter/JIT handler the mode is READ from the recorded
representation column (proposal_representation_dimension3.json, opened
read-only) and normalized into the three names above.  That is
weaker evidence -- the tool's own testimony plus DWARF -- and the
record says so per unit.

THE SPELLING BAN.  A mode is a machine-form property of a unit.  No
operator token takes part in assigning it, in keying it, or in
pairing units by it.  The token rides on a row only as a display
label.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402

PLAIN = "plain"
TAGGED = "tagged"

MEMORY_OPERAND = re.compile(r"\(([^)]*)\)")


def typed_pointer(type_name):
    return "typed-pointer(%s)" % type_name


def strip_annotation(line):
    text = line.strip()
    if "!!" in text:
        text = text.split("!!", 1)[0].strip()
    return text


def base_registers_of(line):
    """every register named inside a memory operand of one
    instruction, as its canon.py FAMILY.  An index register counts
    too: `(%rax,%rcx,8)` dereferences through both."""
    out = []
    text = strip_annotation(line)
    for inner in MEMORY_OPERAND.findall(text):
        for field in inner.split(","):
            field = field.strip()
            if not field.startswith("%"):
                continue
            family = canon.FAMILY_OF.get(field[1:])
            if family is None:
                continue
            out.append(family)
    return out


def written_families(line):
    """the register families one instruction WRITES.  Approximated by
    the last operand of an AT&T instruction, which is its destination
    -- plus the call convention's own clobber for `call`, which is
    handled by the caller."""
    text = strip_annotation(line)
    parts = text.split(" ", 1)
    if len(parts) < 2:
        return []
    operands = parts[1].split(",")
    last = operands[-1].strip()
    if not last.startswith("%"):
        return []
    family = canon.FAMILY_OF.get(last[1:])
    if family is None:
        return []
    return [family]


def dereferenced_families(mnem_lines):
    """`lea` IS EXCLUDED, and the exclusion is the whole reason this
    test is a measurement rather than a coincidence counter: `lea`
    computes an address and reads NO memory.  `lea (%rdi,%rsi,1),%eax`
    is the compilers' ordinary spelling of an integer addition whose
    operands are plain values.  Counting it as a dereference reported
    48 compiled units as pointer-arrival units when in fact 45 of them
    add two plain integers."""
    out = set()
    written = set()
    for line in mnem_lines or []:
        text = strip_annotation(line)
        if not text.startswith("lea "):
            for family in base_registers_of(line):
                if family in written:
                    continue
                out.add(family)
        if text.startswith("call"):
            # a call returns its own value in %rax; a dereference of
            # %rax after a call is a dereference of the CALLEE's
            # result, not of an argument that arrived from outside.
            written.add("rax")
        for family in written_families(line):
            written.add(family)
    return out


def compiled_mode(sem_record):
    """(mode, evidence) for one compiled unit, measured on its own ship
    text."""
    anchor = (sem_record.get("sem") or {}).get("anchor_registers") or {}
    meta = sem_record.get("meta") or {}
    lines = sem_record.get("mnem") or []
    seats = {}
    if anchor.get("in0") is not None:
        seats["a"] = canon.FAMILY_OF.get(anchor["in0"], anchor["in0"])
    if anchor.get("in1") is not None:
        seats["b"] = canon.FAMILY_OF.get(anchor["in1"], anchor["in1"])
    dereferenced = dereferenced_families(lines)
    pointing = []
    for designation in sorted(seats):
        if seats[designation] in dereferenced:
            pointing.append(designation)
    evidence = {}
    evidence["seats"] = dict(seats)
    evidence["dereferenced_families"] = sorted(dereferenced)
    evidence["evidence_class"] = (
        "forced by construction -- the arrival seats come from the "
        "recorded anchor registers and the dereference set is read "
        "off the unit's own ship text")
    if not pointing:
        evidence["pointing_seats"] = []
        return PLAIN, evidence
    evidence["pointing_seats"] = pointing
    names = []
    for designation in pointing:
        if designation == "a":
            names.append(meta.get("lhs_type") or meta.get("lhs_rep")
                         or "unknown")
        else:
            names.append(meta.get("rhs_type") or meta.get("rhs_rep")
                         or "unknown")
    return typed_pointer(",".join(names)), evidence


def normalize_recorded(representation):
    """the three-name vocabulary for a recorded representation string.
    Refuses by returning None rather than guessing."""
    if representation is None:
        return None
    text = representation.strip()
    if text.startswith("tagged"):
        return TAGGED
    if text.startswith("typed-pointer"):
        return text
    if text == "plain":
        return PLAIN
    return None
