#!/usr/bin/env python3
"""region36.py -- THE RULED VIRTUAL REGION and its BLOCK ALLOCATOR.

SUPERSEDED RECORD, 2026-09-05, by the correction "the form, as the owner
meant it" in `Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md`:
the arch-unit is essentially UNCHANGED except for the loading and
unloading of registers into a virtual memory, so the form WRAPS a body
it does not touch (`canonical_form.py`) rather than rewriting every
location in it as `0x<offset>(%r15)` as section 2 below does.  The
`%r15` collision is an artifact of that misreading, not a design
conflict.  This file is kept exactly as it is, as the record of the
form it defined, and is neither edited nor imported by the corrected
line; task 96 (log_201) moved the eleven interpreter units off it.

TASK 43, round 9.  This file is the definition of the form the owner ruled
on 2026-09-02.  His words, verbatim, are the specification:

    "no longer use designated registers at all (meaning that
    registers are not single purpose things but they are still used
    in standardized/normalized ways) FOR ANY OF THEM.  instead using
    a virtual memory that is standardized in terms of the types of
    allocations.  the lineage of an input argument in its own block.
    same for results being in their own block.  everything is loading
    from memory and storing in memory."

and correction 1 of the round-9 briefs, verbatim:

    "input and output isnt the only place where blocks can be
    allocated"

so the allocator hands out ONE TYPED BLOCK PER LINEAGE, and the
lineage kinds are the six named below.

--------------------------------------------------------------------
1.  WHAT IS SUPERSEDED, AND WHY
--------------------------------------------------------------------

Round 8 (canon35_universal.py, log_130) is NOT this form and stays on
disk as the superseded record.  Two concrete shortfalls, both named
in AgentMemory:

  * it kept DESIGNATED REGISTERS as the load targets (a -> %rdi,
    b -> %rsi, answer -> %rax).  A register was still a home.
  * its directory was three slots in the System V red zone,
    -0x8/-0x10/-0x18(%rsp), i.e. %rsp-relative.  A unit whose ANSWER
    IS THE ADDRESS of one of its own stack locations therefore had
    its answer moved by the directory (the six address-of units
    c/op_31 c/op_32 c/op_34 cpp/op_43 cpp/op_44 cpp/op_46 were
    disproved for exactly that).

Both are fixed here by the same move: the region has its own RULED
BASE, and a unit's own stack addresses are a lineage with a block of
their own.

--------------------------------------------------------------------
2.  THE RULED BASE
--------------------------------------------------------------------

THE REGION BASE IS %r15.  Every location in the form is written

    0x<offset>(%r15)

and nothing in the form is written %rsp-relative or %rbp-relative.
%r15 is a SYMBOLIC BASE, not a home for any value: no lineage is
allocated to it, nothing is computed in it, and no unit's core may
mention it (a core that does is REFUSED BY NAME -- measured, that is
4 of the 1,779: cpp/op_765, cpp/op_770, swift/op_703, swift/op_739).

THE MAPPING TO REAL STACK AT RUN TIME, and why the form stays
runnable:

    %r15 = %rsp - REGION_SIZE     (REGION_SIZE = 0x200 = 512 bytes)

established by the CALLER, not by the unit.  The whole region is the
512 bytes immediately BELOW the caller's stack pointer at the moment
it hands control over.  Three properties make this runnable:

  (a) every operand `0xNN(%r15)` is an ordinary x86-64
      disp32(base) memory operand -- a real encoding, assembled by
      `as` and read back by `objdump`, not a notation;
  (b) %r15 is callee-saved in System V, so a caller that sets it
      saves and restores it, and no unit in the form clobbers it;
  (c) the unit itself needs NO PROLOGUE -- it never adjusts %rsp,
      never pushes, and never touches the red zone.  The region is
      the caller's to provide, exactly as the argument values are.

The region sits BELOW %rsp deliberately: the top of the region is
%rsp itself, so the own-address block (6, below) ends exactly where
the unit's own stack scratch used to begin.  That is what makes an
address-of unit's answer come out standardized instead of moved.

--------------------------------------------------------------------
3.  THE ALLOCATION KINDS AND THE FIXED LAYOUT
--------------------------------------------------------------------

Six kinds, the six the brief names.  The layout is FIXED for every
unit in every population -- no per-unit variation, because a
standardized address is the whole point:

    kind            offsets              slots   what a block holds
    ------------------------------------------------------------------
    input           0x000 .. 0x03f       8 x 8   one input argument's
                                                 lineage per block, in
                                                 arrival order
    constant        0x040 .. 0x07f       8 x 8   one literal's lineage
                                                 per block
    temp            0x080 .. 0x0bf       8 x 8   one intermediate
                                                 value's lineage per
                                                 block
    result          0x0c0 .. 0x0cf       2 x 8   the answer's lineage
    guard-outcome   0x0d0 .. 0x0ff       6 x 8   one guard's outcome
                                                 per block
    own-address     0x100 .. 0x1ff       0x100   the unit's OWN stack
                                                 addresses, as one
                                                 lineage
    ------------------------------------------------------------------
    REGION_SIZE     0x200

THE OWN-ADDRESS BLOCK IS AN AFFINE IMAGE, not a slot series.  A unit
that spells its own scratch as `-0xN(%rsp)` has that address rewritten

    -0xN(%rsp)   ->   0x(REGION_SIZE - N)(%r15)

ONE uniform map, the same constant for every displacement in every
unit, so the unit's own internal spacing is preserved exactly and only
the base moves.  Combined with the run-time mapping of (2) --
%r15 = %rsp - REGION_SIZE -- the rewritten address is THE SAME BYTE
the unit addressed before:

    0x(REGION_SIZE - N)(%r15) = %rsp - REGION_SIZE + REGION_SIZE - N
                              = %rsp - N

which is why an address-of unit's answer is unchanged in VALUE and
standardized in TEXT at the same time.  A displacement larger than
0x100 is REFUSED BY NAME (`OwnBlockOverflow`) rather than wrapped.

--------------------------------------------------------------------
4.  ONE FIXED RULE CHOOSES THE SCRATCH REGISTERS
--------------------------------------------------------------------

No register is a home.  Registers are the vehicles a load or a store
rides in, and WHICH vehicle is chosen is decided by one rule applied
identically to every unit -- never by the compiler that emitted the
unit, and never by an argument's identity.

RULE R, stated completely:

  R1  Walk the unit's core in order.  Collect the distinct general
      register families in FIRST-MENTION ORDER, and separately the
      distinct vector register families in first-mention order.
  R2  A family PINNED BY AN ENCODING in that core is a FIXED POINT:
      it maps to itself and is withdrawn from the pool.  The pins are
      the hardware's, not ours -- %rax/%rdx for the sign-extend and
      divide forms, %rcx for a variable shift count.
  R3  Every other family is assigned, in the first-mention order of
      R1, the next register from the fixed pool that is not a fixed
      point:

        general pool: r10 r11 rax rcx rdx rsi rdi r8 r9 rbx r12 r13 r14
        vector  pool: xmm0 .. xmm13

  R4  %rsp, %rbp and %rip are never renamed (canon.NEVER_RENAME), and
      %r15 may not appear at all (2).

The map is a permutation, so applying it to the core is meaning-
preserving by construction; the gate proves it anyway.  Its effect is
that two units computing the same thing produce the SAME TEXT even
when their compilers picked different scratch registers -- which is
the property round 8 could not have, because there the arrival
register was fixed by the argument's identity.

--------------------------------------------------------------------
5.  THE ARRIVAL CONTRACT
--------------------------------------------------------------------

A unit is entered with its region already populated:

  * input block i holds argument i's value, for each argument;
  * constant block j holds literal j's value, for each literal the
    unit materializes (6);
  * every other block is undefined on entry.

On return, the RESULT BLOCK holds the answer.  The answer's home is
the result block and nothing else -- the register the answer happens
to be sitting in at `ret` is incidental and is not part of the form.
That is the concrete difference from round 8, where the answer was
defined to be in %rax and merely copied to a slot.

--------------------------------------------------------------------
6.  CONSTANTS ARE A LINEAGE, SO THEY GET BLOCKS
--------------------------------------------------------------------

Every distinct literal in a unit's core is allocated a constant
block, and the block appears in the unit's directory whether or not
the literal is materialized as a memory operand.  MATERIALIZED means
the instruction is rewritten to read the block:

    xor $0x1,%dil        ->   xor 0x40(%r15),%dil

which is legal x86-64 (an r/m source of the operand's own width) and
is what "everything is loading from memory" means for a literal.
Materialization is applied only where the encoding admits a memory
source -- a two-operand ALU form with a register destination -- and
the whole render is gated; where the full form does not prove, the
REDUCED form (literals left as immediates, blocks still allocated and
recorded) is rendered and gated instead, and the record says which of
the two it carries in `constant_materialization`.

--------------------------------------------------------------------
7.  TEMP AND GUARD-OUTCOME LINEAGES
--------------------------------------------------------------------

  * A unit's own stack scratch splits in two by MEASURED EVIDENCE,
    not by naming: a stack address whose ADDRESS ESCAPES (some line
    takes its `lea`) is an OWN-ADDRESS lineage; a stack address only
    ever loaded from and stored to is a TEMP lineage.  Both are
    rewritten by the affine map of (3); the kind is recorded per
    address so the directory says which lineage each block holds.
  * A register-resident intermediate is recorded as a temp lineage
    with `resident: register` and the rule-R register naming it, and
    its block is allocated.  This lap does NOT spill register temps
    to memory: that is a rewrite of the computation itself, not of
    its plumbing, and it is recorded as a stated limit rather than
    claimed.
  * A branching unit gets one guard-outcome block per branch, from
    its own recorded branch shape.  The block is allocated and
    directoried; materializing the outcome value is likewise not done
    this lap and is recorded as such.

--------------------------------------------------------------------
THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."

No operator token appears in this file.  Coding discipline: no
complex/compound one-liner statements.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon  # noqa: E402

REGION_BASE_REGISTER = "%r15"
REGION_BASE_FAMILY = "r15"
REGION_SIZE = 0x400
REGION_EXTENT = 0x408

INPUT_BASE = 0x000
INPUT_SLOTS = 8
CONST_BASE = 0x040
CONST_SLOTS = 40
TEMP_BASE = 0x180
TEMP_SLOTS = 16
RESULT_BASE = 0x200
RESULT_SLOTS = 2
GUARD_BASE = 0x210
GUARD_SLOTS = 6
OWN_BASE = 0x300
OWN_SPAN = 0x100

KINDS = ("input", "constant", "temp", "result", "own-address",
         "guard-outcome")

POOL_GENERAL = ["r10", "r11", "rax", "rcx", "rdx", "rsi", "rdi",
                "r8", "r9", "rbx", "r12", "r13", "r14"]
POOL_VECTOR = ["xmm%d" % i for i in range(0, 14)]

NEVER_RENAME = set(canon.NEVER_RENAME)

# encodings that PIN a family; the hardware's pins, not ours.
PIN_RAX_RDX_MNEMONICS = frozenset([
    "cltd", "cqto", "cltq", "cwtl", "cbtw", "cwtd",
    "idiv", "idivl", "idivq", "idivb", "idivw",
    "div", "divl", "divq", "divb", "divw",
])
ONE_OPERAND_PIN = frozenset(["mul", "imul", "idiv", "div", "neg_"])
SHIFT_MNEMONICS = frozenset([
    "shl", "shr", "sar", "sal", "rol", "ror", "rcl", "rcr",
    "shld", "shrd",
])

RSP_DISP = re.compile(r"-0x([0-9a-fA-F]+)\(%rsp\)")
BARE_RSP = re.compile(r"(?<![x0-9a-fA-F])\(%rsp\)")
RBP_ANY = re.compile(r"\(%rbp\)")
BLOCK_TEXT = re.compile(r"^0x([0-9a-fA-F]+)\(%r15\)$")
IMMEDIATE = re.compile(r"^\$(-?0x[0-9a-fA-F]+|-?\d+)$")


class Refusal(Exception):
    """refused BY NAME, never silently."""

    def __init__(self, cause, detail):
        Exception.__init__(self, detail)
        self.cause = cause
        self.detail = detail


def block_text(offset):
    return "0x%x(%%r15)" % offset


def is_block_text(text):
    return BLOCK_TEXT.match(text) is not None


def block_offset(text):
    hit = BLOCK_TEXT.match(text)
    if hit is None:
        return None
    return int(hit.group(1), 16)


def own_offset_of_displacement(displacement):
    """the affine map of section 3, the same constant for every unit."""
    if displacement > OWN_SPAN:
        raise Refusal(
            "own-block overflow",
            "the unit spells its own stack address at -0x%x(%%rsp), "
            "which is further than the own-address block's 0x%x bytes "
            "reach; the form refuses by name rather than wrapping it"
            % (displacement, OWN_SPAN))
    if displacement < 0:
        raise Refusal(
            "own-block overflow",
            "the unit spells a positive stack displacement, which "
            "addresses the caller's frame, not the unit's own")
    return REGION_SIZE - displacement


class BlockAllocator(object):
    """lineage -> typed block.  One block per lineage, never reused,
    handed out in first-needed order within each kind."""

    def __init__(self):
        self.blocks = []
        self.by_lineage = {}
        self.counts = {}
        for kind in KINDS:
            self.counts[kind] = 0

    def _limit(self, kind):
        if kind == "input":
            return INPUT_SLOTS
        if kind == "constant":
            return CONST_SLOTS
        if kind == "temp":
            return TEMP_SLOTS
        if kind == "result":
            return RESULT_SLOTS
        if kind == "guard-outcome":
            return GUARD_SLOTS
        return None

    def _base(self, kind):
        if kind == "input":
            return INPUT_BASE
        if kind == "constant":
            return CONST_BASE
        if kind == "temp":
            return TEMP_BASE
        if kind == "result":
            return RESULT_BASE
        if kind == "guard-outcome":
            return GUARD_BASE
        return None

    def allocate(self, kind, lineage, note=None):
        """allocate the block for one lineage of one kind."""
        if kind not in KINDS:
            raise Refusal("unknown allocation kind",
                          "the allocator was asked for kind %r" % kind)
        key = (kind, lineage)
        if key in self.by_lineage:
            return self.by_lineage[key]
        if kind == "own-address":
            raise Refusal(
                "own-address blocks are placed by the affine map",
                "an own-address lineage is placed by "
                "own_offset_of_displacement, not by the slot allocator")
        index = self.counts[kind]
        limit = self._limit(kind)
        if index >= limit:
            raise Refusal(
                "%s block exhaustion" % kind,
                "the unit needs a %d-th %s block and the region "
                "provides %d" % (index + 1, kind, limit))
        offset = self._base(kind) + 8 * index
        record = {
            "kind": kind,
            "lineage": lineage,
            "index": index,
            "offset": offset,
            "text": block_text(offset),
        }
        if note is not None:
            record["note"] = note
        self.counts[kind] = index + 1
        self.by_lineage[key] = record
        self.blocks.append(record)
        return record

    def place_own(self, displacement, escapes):
        """the own-address / temp lineage a stack displacement is."""
        offset = own_offset_of_displacement(displacement)
        kind = "own-address" if escapes else "temp"
        key = (kind, "stack_-0x%x" % displacement)
        if key in self.by_lineage:
            return self.by_lineage[key]
        record = {
            "kind": kind,
            "lineage": "stack_-0x%x" % displacement,
            "was": "-0x%x(%%rsp)" % displacement,
            "offset": offset,
            "text": block_text(offset),
            "placed_by": "the affine map REGION_SIZE - displacement",
        }
        if escapes:
            record["evidence"] = (
                "the address escapes: a line of the core takes its "
                "`lea`, so the lineage is the ADDRESS, not the value")
        else:
            record["evidence"] = (
                "the address never escapes: it is only loaded from "
                "and stored to, so the lineage is an intermediate")
        self.by_lineage[key] = record
        self.blocks.append(record)
        return record

    def directory(self):
        return list(self.blocks)


def split_lines(text):
    out = []
    for piece in text.split(";"):
        piece = piece.strip()
        if piece:
            out.append(piece)
    return out


def mnemonic_of(line):
    return line.split(" ", 1)[0]


def operands_of(line, splitter):
    parts = line.split(" ", 1)
    if len(parts) == 1:
        return []
    out = []
    for item in splitter(parts[1]):
        out.append(item.strip())
    return out


def strip_annotation(line):
    if "!!" not in line:
        return line
    return line.split("!!", 1)[0].strip()


def size_stem(mnemonic):
    """the mnemonic with ONE trailing size suffix removed, and only
    when removing it leaves a stem this file knows.  The earlier
    `rstrip("bwlq")` removed EVERY trailing character in that set, so
    `shl` became `sh` and no variable shift ever pinned %rcx -- which
    is exactly the fault 43 units showed ("shl count operand '%sil' is
    neither %cl nor an immediate")."""
    if mnemonic in SHIFT_MNEMONICS:
        return mnemonic
    if mnemonic in ONE_OPERAND_PIN:
        return mnemonic
    if len(mnemonic) > 1:
        if mnemonic[-1] in "bwlq":
            head = mnemonic[:-1]
            if head in SHIFT_MNEMONICS:
                return head
            if head in ONE_OPERAND_PIN:
                return head
    return mnemonic


def families_pinned(core, splitter):
    """RULE R2: the families this core pins by encoding."""
    pinned = set()
    for raw in core:
        line = strip_annotation(raw)
        mnemonic = mnemonic_of(line)
        operands = operands_of(line, splitter)
        if mnemonic in PIN_RAX_RDX_MNEMONICS:
            pinned.add("rax")
            pinned.add("rdx")
            continue
        base = size_stem(mnemonic)
        if base in ONE_OPERAND_PIN:
            if len(operands) == 1:
                pinned.add("rax")
                pinned.add("rdx")
                continue
        if base in SHIFT_MNEMONICS:
            # only a VARIABLE count pins %rcx; an immediate count does
            # not, so the pool is not narrowed for no reason.
            if operands:
                if operands[0].startswith("%"):
                    pinned.add("rcx")
    return pinned


def register_families_in_order(core, splitter):
    """RULE R1: distinct families, first-mention order, split by file."""
    general = []
    vector = []
    for raw in core:
        line = strip_annotation(raw)
        for token in re.findall(r"%[a-z0-9]+", line):
            family = canon.FAMILY_OF.get(token[1:])
            if family is None:
                continue
            if family in NEVER_RENAME:
                continue
            if family.startswith("xmm"):
                if family not in vector:
                    vector.append(family)
                continue
            if family not in general:
                general.append(family)
    return general, vector


def rule_r_map(core, splitter):
    """RULE R: the fixed scratch-register choice.  Returns
    (family -> family, notes) or raises Refusal."""
    general, vector = register_families_in_order(core, splitter)
    if REGION_BASE_FAMILY in general:
        raise Refusal(
            "the core names the region base",
            "this unit's own core mentions %r15, which the form rules "
            "to be the region base and therefore not available to any "
            "lineage; the unit is refused by name rather than being "
            "rendered onto a base it also uses as a value")
    pinned = families_pinned(core, splitter)
    mapping = {}
    notes = []
    for family in general:
        if family in pinned:
            mapping[family] = family
            notes.append({
                "family": family,
                "assigned": family,
                "why": "R2: pinned by an encoding in this core, so it "
                       "is a fixed point",
            })
    taken = set(mapping.values())
    cursor = 0
    for family in general:
        if family in mapping:
            continue
        while cursor < len(POOL_GENERAL):
            candidate = POOL_GENERAL[cursor]
            if candidate in pinned:
                cursor = cursor + 1
                continue
            if candidate in taken:
                cursor = cursor + 1
                continue
            break
        if cursor >= len(POOL_GENERAL):
            raise Refusal(
                "scratch pool exhausted",
                "the core needs more distinct general registers than "
                "the fixed pool of %d provides" % len(POOL_GENERAL))
        chosen = POOL_GENERAL[cursor]
        mapping[family] = chosen
        taken.add(chosen)
        cursor = cursor + 1
        notes.append({
            "family": family,
            "assigned": chosen,
            "why": "R3: the next free register of the fixed general "
                   "pool, in first-mention order",
        })
    vcursor = 0
    vtaken = set()
    for family in vector:
        if vcursor >= len(POOL_VECTOR):
            raise Refusal(
                "scratch pool exhausted",
                "the core needs more distinct vector registers than "
                "the fixed pool of %d provides" % len(POOL_VECTOR))
        chosen = POOL_VECTOR[vcursor]
        mapping[family] = chosen
        vtaken.add(chosen)
        vcursor = vcursor + 1
        notes.append({
            "family": family,
            "assigned": chosen,
            "why": "R3: the next free register of the fixed vector "
                   "pool, in first-mention order",
        })
    return mapping, notes


def widened(family, width_index):
    """the register name of `family` at the width slot `width_index`
    (0=64, 1=32, 2=16, 3=8)."""
    if family.startswith("xmm"):
        return family
    names = canon.GP_NAMES.get(family)
    if names is None:
        return family
    return names[width_index]


def width_index_of(name):
    for family, names in canon.GP_NAMES.items():
        for index, spelling in enumerate(names):
            if spelling == name:
                return index
    return None


def apply_rule_r(line, mapping):
    """rename every register in one line under the rule-R map, keeping
    each mention's own width."""
    def swap(match):
        name = match.group(0)[1:]
        family = canon.FAMILY_OF.get(name)
        if family is None:
            return match.group(0)
        if family in NEVER_RENAME:
            return match.group(0)
        target = mapping.get(family)
        if target is None:
            return match.group(0)
        if family.startswith("xmm"):
            return "%" + target
        index = width_index_of(name)
        if index is None:
            return match.group(0)
        return "%" + widened(target, index)

    return re.sub(r"%[a-z0-9]+", swap, line)


def rule_r_map_ordered(general_order, vector_order, pinned):
    """RULE R with the first-mention order supplied by the renderer.

    The renderer supplies the order because the text's first mentions
    are the STANDARDIZED LOADS, which come before the core: an input
    lineage is mentioned by its own load, in arrival order, and the
    result lineage by its own store.  Passing the order in keeps R1's
    definition (first mention in the finished text) exact instead of
    approximating it by the core alone."""
    mapping = {}
    notes = []
    if REGION_BASE_FAMILY in general_order:
        raise Refusal(
            "the core names the region base",
            "this unit's own core mentions %r15, which the form rules "
            "to be the region base and therefore not available to any "
            "lineage; the unit is refused by name rather than being "
            "rendered onto a base it also uses as a value")
    for family in general_order:
        if family in pinned:
            mapping[family] = family
            notes.append({
                "family": family,
                "assigned": family,
                "why": "R2: pinned by an encoding in this core",
            })
    taken = set(mapping.values())
    cursor = 0
    for family in general_order:
        if family in mapping:
            continue
        chosen = None
        while cursor < len(POOL_GENERAL):
            candidate = POOL_GENERAL[cursor]
            cursor = cursor + 1
            if candidate in pinned:
                continue
            if candidate in taken:
                continue
            chosen = candidate
            break
        if chosen is None:
            raise Refusal(
                "scratch pool exhausted",
                "the text needs more distinct general registers than "
                "the fixed pool of %d provides" % len(POOL_GENERAL))
        mapping[family] = chosen
        taken.add(chosen)
        notes.append({
            "family": family,
            "assigned": chosen,
            "why": "R3: the next free register of the fixed general "
                   "pool, in first-mention order",
        })
    vcursor = 0
    for family in vector_order:
        if family in mapping:
            continue
        if vcursor >= len(POOL_VECTOR):
            raise Refusal(
                "scratch pool exhausted",
                "the text needs more distinct vector registers than "
                "the fixed pool of %d provides" % len(POOL_VECTOR))
        mapping[family] = POOL_VECTOR[vcursor]
        notes.append({
            "family": family,
            "assigned": POOL_VECTOR[vcursor],
            "why": "R3: the next free register of the fixed vector "
                   "pool, in first-mention order",
        })
        vcursor = vcursor + 1
    return mapping, notes, taken


def free_vehicle(taken, pinned):
    """the CONSTANT VEHICLE: the first register of the fixed general
    pool that no lineage holds and no encoding pins.  A literal is
    loaded from its block into this register and consumed on the very
    next line, so it is live across exactly one instruction."""
    for candidate in POOL_GENERAL:
        if candidate in taken:
            continue
        if candidate in pinned:
            continue
        return candidate
    return None


def immediate_value(text):
    """the 64-bit unsigned image of an immediate operand, or None."""
    hit = IMMEDIATE.match(text)
    if hit is None:
        return None
    body = hit.group(1)
    try:
        if body.startswith("-0x") or body.startswith("0x"):
            value = int(body, 16)
        else:
            value = int(body, 10)
    except ValueError:
        return None
    return value & 0xFFFFFFFFFFFFFFFF
