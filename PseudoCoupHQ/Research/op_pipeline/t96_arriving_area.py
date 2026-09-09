#!/usr/bin/env python3
"""t96_arriving_area.py -- THE SEVENTH BLOCK KIND: AN ARRIVING
ADDRESSABLE AREA.

TASK 96, round 19.  Planned in
`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md`,
heading "the seventh block kind -- an arriving addressable area
(planned 2026-09-05)", and in AgentMemory "the rulings of 2026-09-04 /
2026-09-05".

    "`region36.py:271` allocates six kinds: input, constant, temp,
    result, own-address, guard-outcome.  Five hold ONE VALUE each.
    `own-address` is already an addressable AREA -- 0x100 bytes the
    unit reaches into at its own offsets, described there as 'an
    affine image, not a slot series', mapped so the unit's internal
    spacing is preserved and only the base moves.

    php's value frame is that same shape and ARRIVES rather than being
    the unit's own scratch, and its offsets (0x40, 0x50, 0x60) are
    constants sitting in the bytecode.  So the gap is one kind, with a
    working precedent, not a new capability."

NOTHING HERE IS A SECOND MECHANISM BESIDE `own-address`.  Every rule
below is `own-address`'s rule with one word changed, and the word is
said at each rule.

--------------------------------------------------------------------
1.  WHY THIS FILE EXISTS RATHER THAN AN EDIT TO region36.py
--------------------------------------------------------------------

`region36.py` and `canon36_universal.py` are SUPERSEDED RECORDS as of
2026-09-05 (the correction "the form, as the owner meant it").  They are not
edited.  The seventh kind is therefore added HERE, over
`canonical_form.py` + `ledger.py`, which is the form the correction
names.  This file imports `ledger.py` and subclasses its `Ledger`; it
copies none of it.

--------------------------------------------------------------------
2.  THE EVIDENCE THAT A BLOCK IS AN ARRIVING AREA -- MACHINE FORM ONLY
--------------------------------------------------------------------

`own-address`'s evidence, region36 section 7, verbatim in substance:
"a stack address whose ADDRESS ESCAPES (some line takes its `lea`) is
an OWN-ADDRESS lineage; a stack address only ever loaded from and
stored to is a TEMP lineage".  Evidence read off the body, never a
name.

The same shape, one word changed -- `%rsp` becomes any family:

    A REGISTER FAMILY THE BODY DEREFERENCES BEFORE THE BODY HAS
    WRITTEN IT holds the base of an area that ARRIVED.  A family that
    arrives and is only ever used as a value is an INPUT.

Read in one pass in text order, exactly as `Ledger.walk_dataflow`
reads.  `%rsp`, `%rbp` and `%rip` are excluded because the unit's own
frame is already two kinds -- `OWN` and `STACK` -- and this kind is
for memory that is NOT the unit's own scratch.

`lea` IS NOT A DEREFERENCE, and is excluded.  `own-address`'s evidence
reads a `lea` as an address ESCAPING; here the evidence wanted is the
opposite one -- the body reaching THROUGH the base -- and a `lea`
never reaches through anything.  MEASURED, and this is why the rule is
stated: `java/op_1` spells `lea (%rsi,%rdx,1),%eax`, where `%rsi` and
`%rdx` are two values being added and neither is an area
(`t96_l2_survey.sh`, lane log named in the report).

A COPY OF AN AREA'S BASE STILL NAMES THAT AREA.  The walk carries a
family -> area map, which is `Ledger.walk_dataflow`'s own `where` map:
a plain register-to-register move of a base makes the destination
another name for the same area, and any other write to a family drops
it.  Without this, `cpython/long_add`'s `mov 0x18(%rcx),%ecx` would go
unattributed, because `%rcx` holds a copy of `%rsi`.

A BASE ADVANCED BY A CONSTANT STILL NAMES THAT AREA, AT A SHIFTED
OFFSET.  This is `own-address`'s affine image itself: base plus a
constant, spacing preserved.  The walk therefore carries a SHIFT per
holder, and a displacement is attributed as `shift + d`.  MEASURED,
and this is why the rule is stated: php's
`ZEND_ADD_LONG_NO_OVERFLOW_SPEC_...` reads its two operand slots at
`0x8(%r15)` and `0xc(%r15)`, then advances the bytecode pointer with
`add $0x20,%r15`, then reads its answer slot at `-0x10(%r15)`.  That
third read is the SAME area at `0x20 - 0x10 = 0x10`; without the shift
it would be attributed to nothing and read as memory the unit obtained
at run time, which it is not.

WHAT THE WALK STILL DROPS, said rather than hidden: a base changed by
anything other than a plain move or a constant add or subtract -- a
variable advance, an arithmetic combination -- is dropped, and any
later reach through it is unattributed.  None occurs in this
population; the rule is stated so the next population is read against
it rather than against silence.

A TRANSFER WRITES THE CONVENTION'S ANSWER REGISTERS.  `call` names no
destination operand, so the walk would otherwise treat a pointer a
callee HANDED BACK as one that arrived.  System V leaves an integer
answer in the accumulator and a floating one in vector position 0, so
the walk marks those two written at every transfer.  Memory a unit
obtains at run time is therefore NOT an arriving area, and is not
given a block by this file.

A REACH THROUGH AN INDEX REGISTER IS NOT BOUNDED BY THE TEXT, and is
recorded as such rather than counted as if it were.  php's specialized
handlers reach their value frame as `0x8(%r14,%rax,1)`, where `%rax`
came out of the bytecode -- which is the owner's own observation that the
frame's offsets "are constants sitting in the bytecode".  The
displacement the text spells is 0x8; the byte actually reached is
0x8 + whatever the bytecode said.  Every such area carries
`reached_through_an_index_register`, and its recorded reach is stated
as a floor, never as the extent.

--------------------------------------------------------------------
3.  THE BLOCK, AND ITS AFFINE MAP
--------------------------------------------------------------------

`own-address` is ONE block of `OWN_SPAN` = 0x100 bytes and is mapped
by ONE uniform constant, "the same constant for every displacement in
every unit, so the unit's own internal spacing is preserved exactly
and only the base moves" (region36 section 3).

The seventh kind is one block, `AREA`, divided into EXTENTS of
`AREA_SPAN` = 0x100 bytes -- one extent per arriving area, extent `i`
at `AREA_SPAN * i`.  Within its extent the map is the identity: the
unit's own displacement `d` addresses `extent_base + d`.  Spacing
preserved, only the base moves -- the same sentence as `own-address`.

A displacement outside `[AREA_ORIGIN - AREA_SPAN, AREA_ORIGIN)`
measured from the extent base is REFUSED BY NAME (`arriving-area
overflow`), which is `own_offset_of_displacement`'s refusal
(`own-block overflow`) with the same shape.

`AREA_ORIGIN` is decided by MEASUREMENT, not by taste: `survey`
prints, for every unit in the population, the smallest and largest
displacement the body spells from an arriving base.  When every
displacement is non-negative the origin is 0 and the map is the plain
identity.  The origin in force is written on every record.

MEASURED 2026-09-05 over these eleven bodies (`t96_l2_survey.sh`): the
smallest displacement is 0x0 and the largest is 0x538.  The origin is
therefore 0 and the map is the plain identity -- no constant is
invented.  0x538 is `java/op_1` and `java/op_2` reaching into the
HotSpot thread structure through `%r15`; it is past `AREA_SPAN`, so
those two are REFUSED BY NAME, which is what
`own_offset_of_displacement` does with a stack displacement past
`OWN_SPAN`.  `AREA_SPAN` IS NOT WIDENED TO ADMIT THEM: 0x100 is
`own-address`'s own constant, and changing it is a decision this tree
does not answer, so it is FLAGGED rather than taken.

--------------------------------------------------------------------
4.  HOW THE BASE REACHES THE REGISTER -- ONE STEP, NOT TWO
--------------------------------------------------------------------

This is the whole mechanical difference between the seventh kind and
an `IN` row, and it is the difference between an ADDRESS and a VALUE.

  IN-i, a value that arrives (canonical_form.Prelude.emit_general_row):

      mov ledger+0x00(%rip),%rdi      the IN block's base
      mov 0x0(%rdi),%rdi              the VALUE the row holds

  AREA-i, an area that arrives (this file):

      mov ledger+0x40(%rip),%rdi      the AREA block's base
      lea 0x100(%rdi),%rdi            this area's extent  (only i > 0,
                                      and only when the origin or the
                                      extent index moves the base)

The second line is a `lea`, not a load: the register ends holding an
ADDRESS the unit then reaches into at its own offsets, rather than a
value the unit consumes.  That is `own-address`'s "affine image, not a
slot series", written as a prelude line instead of as a rewrite.

The ledger gains one entry, `AREA`, appended after `OUT`, so the eight
entries the canonical form already writes keep their offsets and the
new entry is the ninth at 0x40.  No existing entry moves.

--------------------------------------------------------------------
5.  WHAT THIS KIND DOES NOT DO
--------------------------------------------------------------------

It does not touch the body.  The body still spells `0x40(%r15)`; only
the value of `%r15` at entry now comes from the ledger instead of from
a convention nobody wrote down.  The canonical form's rule -- the
compiler's body is verbatim -- is untouched, and gate check C1 is
therefore still the check that decides.

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

No operator token appears in this file.  The evidence for every block
is the body's own bytes; nothing is grouped, paired or selected by a
member's display label.

Coding discipline: no compound one-liner statements.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                      # noqa: E402
import ledger as L                                                # noqa: E402


# the block's own name, and the entry it takes on the ledger.  It is
# APPENDED, so every entry the canonical form already writes keeps the
# offset it has.
AREA_BLOCK = "AREA"
AREA_ENTRY_INDEX = len(L.BLOCK_ORDER)
AREA_ENTRY_OFFSET = L.LEDGER_ENTRY_SIZE * AREA_ENTRY_INDEX

# own-address's OWN_SPAN, 0x100, unchanged.
AREA_SPAN = 0x100

# the uniform constant of section 3.  0 is the identity map; `survey`
# is what decides whether 0 is right for a population.
AREA_ORIGIN = 0

# System V's answer registers, section 2.
TRANSFER_WRITES = ("rax", "xmm0")

# the unit's own frame, which is already two kinds.
NOT_AN_ARRIVING_BASE = set(canon.NEVER_RENAME)

MEMORY_OPERAND = re.compile(
    r"(-?0x[0-9a-fA-F]+)?\(\s*(%[a-z0-9]+)\s*"
    r"(?:,\s*(%[a-z0-9]+)\s*(?:,\s*[1248]\s*)?)?\)")

# `lea` computes an address; it never reaches through one.  Section 2.
NOT_A_DEREFERENCE = frozenset(["lea", "leal", "leaq", "leaw"])

# a plain register-to-register move, which makes the destination
# another name for whatever the source named.  Section 2.
PLAIN_MOVE = frozenset(["mov", "movq", "movl"])

# a base advanced by a constant is the same area at a shifted offset --
# own-address's own affine image.  Section 2.
CONSTANT_ADVANCE = {"add": 1, "addq": 1, "addl": 1,
                    "sub": -1, "subq": -1, "subl": -1}


class AreaRefusal(L.Refusal):
    """refused BY NAME, never silently -- own_offset_of_displacement's
    shape."""


def area_entry_text():
    """the AREA block's own ledger entry, rip-relative, exactly as
    `ledger.ledger_entry_text` writes the other eight."""
    return "%s+0x%02x(%%rip)" % (L.LEDGER_SYMBOL, AREA_ENTRY_OFFSET)


def extent_base(index):
    """extent `i` of the AREA block."""
    return AREA_SPAN * index


def area_offset_of_displacement(displacement):
    """the affine map of section 3, the same constant for every unit.

    own-address's map is `REGION_SIZE - N` for a displacement `-N`
    below %rsp.  An arriving area is reached at the unit's own
    displacement `d`, so the map is `AREA_ORIGIN + d`, and
    AREA_ORIGIN is one constant for every displacement in every unit.
    """
    offset = AREA_ORIGIN + displacement
    if offset < 0:
        raise AreaRefusal(
            "arriving-area overflow",
            "the unit reaches its arriving area at displacement "
            "0x%x, which is 0x%x below the extent's own base; the "
            "form refuses by name rather than wrapping it"
            % (displacement, -offset))
    if offset >= AREA_SPAN:
        raise AreaRefusal(
            "arriving-area overflow",
            "the unit reaches its arriving area at displacement "
            "0x%x, which is further than the extent's 0x%x bytes "
            "reach; the form refuses by name rather than wrapping it"
            % (displacement, AREA_SPAN))
    return offset


def memory_bases(line):
    """every (base family, displacement, indexed) a line DEREFERENCES.

    The index register of a scaled operand is a VALUE, not a base, so
    it is not returned as a base; `indexed` says the operand carried
    one, which is what makes the recorded displacement a floor rather
    than the reach (section 2).

    A `lea` is not a dereference, so it contributes nothing.
    """
    mnemonic = L.mnemonic_of(line)
    if mnemonic in NOT_A_DEREFERENCE:
        return []
    found = []
    for hit in MEMORY_OPERAND.finditer(line):
        text = hit.group(1)
        register = hit.group(2)
        index = hit.group(3)
        family = canon.FAMILY_OF.get(register[1:])
        if family is None:
            continue
        if text is None:
            displacement = 0
        elif text.startswith("-0x"):
            displacement = -int(text[3:], 16)
        else:
            displacement = int(text, 16)
        found.append((family, displacement, index is not None))
    return found


def written_families(line):
    """the families one line writes, by `ledger.destination_rule` and
    by the ordinary rule that file states ('the destination is the
    last named operand')."""
    mnemonic = L.mnemonic_of(line)
    operands = L.operands_of(line)
    if L.is_transfer(mnemonic):
        return list(TRANSFER_WRITES)
    stem, rule = L.destination_rule(mnemonic, len(operands))
    if rule is not None:
        out = []
        for family, _what in rule["writes"]:
            out.append(family)
        return out
    if not operands:
        return []
    last = operands[-1]
    if not last.startswith("%"):
        return []
    family = L.family_of_operand(last)
    if family is None:
        return []
    return [family]


def read_arriving_areas(body):
    """the arriving areas alone -- `walk_bases`' first answer."""
    areas, _obtained = walk_bases(body)
    return areas


def read_obtained_memory(body):
    """the dereferences through a base the body itself wrote --
    `walk_bases`' second answer.  This is log_199 section 3.2.2's
    "memory the unit obtains at run time", counted by the SAME walk
    that finds the areas, so a reach through an advanced area base is
    not counted twice."""
    _areas, obtained = walk_bases(body)
    return obtained


def walk_bases(body):
    """the body -> (the arriving addressable areas it evidences, in
    FIRST-SIGHTING ORDER, with the displacements it reaches each at;
    the dereferences through a base the body itself wrote).

    ONE PASS IN TEXT ORDER, which is `Ledger.walk_dataflow`'s own
    order.  A family the body dereferences before the body has written
    it holds the base of an area that arrived (section 2), and a plain
    move of that base makes the destination another name for the same
    area.
    """
    written = set()
    holder = {}                # family -> (the area it names, shift)
    order = []
    areas = {}
    obtained = []

    def sight(record, displacement, indexed, line):
        record["sightings"] = record["sightings"] + 1
        if displacement not in record["displacements"]:
            record["displacements"].append(displacement)
        if indexed:
            record["reached_through_an_index_register"] = True
            if line not in record["indexed_sightings"]:
                record["indexed_sightings"].append(line)

    for index, raw in enumerate(body):
        line = L.R36.strip_annotation(raw).strip()
        if not line:
            continue
        if line.endswith(":"):
            continue
        if line == "ret":
            continue
        for family, displacement, indexed in memory_bases(line):
            if family in NOT_AN_ARRIVING_BASE:
                continue
            if family in holder:
                held, shift = holder[family]
                sight(held, shift + displacement, indexed, line)
                continue
            if family in written:
                obtained.append({
                    "at_index": index,
                    "instruction": line,
                    "base": "%" + family,
                    "the_body_spells": "0x%x" % displacement,
                })
                continue
            record = {
                "base_family": family,
                "first_sighting_line_index": index,
                "first_sighting": line,
                "displacements": [],
                "sightings": 0,
                "also_named_by": [],
                "advanced_by": [],
                "reached_through_an_index_register": False,
                "indexed_sightings": [],
                "evidence":
                    "the body dereferences %%%s at line %d and has "
                    "not written %%%s before that line, so what "
                    "arrived in %%%s is the base of an area, not a "
                    "value" % (family, index, family, family),
            }
            order.append(family)
            areas[family] = record
            holder[family] = (record, 0)
            sight(record, displacement, indexed, line)

        mnemonic = L.mnemonic_of(line)
        operands = L.operands_of(line)
        moved = None
        advanced = None
        if mnemonic in PLAIN_MOVE:
            if len(operands) == 2:
                if operands[0].startswith("%"):
                    if operands[1].startswith("%"):
                        source = L.family_of_operand(operands[0])
                        if source in holder:
                            moved = holder[source]
        if mnemonic in CONSTANT_ADVANCE:
            if len(operands) == 2:
                if operands[1].startswith("%"):
                    target = L.family_of_operand(operands[1])
                    amount = L.immediate_value(operands[0])
                    if target in holder:
                        if amount is not None:
                            sign = CONSTANT_ADVANCE[mnemonic]
                            held, shift = holder[target]
                            advanced = (target,
                                        (held, shift + sign * amount))
                            if line not in held["advanced_by"]:
                                held["advanced_by"].append(line)
        for family in written_families(line):
            written.add(family)
            if family in holder:
                del holder[family]
        if moved is not None:
            destination = L.family_of_operand(operands[1])
            if destination is not None:
                holder[destination] = moved
                named = "%" + destination
                if named not in moved[0]["also_named_by"]:
                    moved[0]["also_named_by"].append(named)
        if advanced is not None:
            holder[advanced[0]] = advanced[1]

    out = []
    for family in order:
        record = areas[family]
        record["displacements"].sort()
        record["smallest_displacement"] = record["displacements"][0]
        record["largest_displacement"] = record["displacements"][-1]
        if record["reached_through_an_index_register"]:
            record["the_reach_is_a_floor_not_the_extent"] = (
                "this area is reached with an index register, so the "
                "byte the body lands on is the displacement above "
                "PLUS whatever the index holds at run time; the "
                "recorded reach is a floor and the extent this body "
                "needs is not readable from its text")
        out.append(record)
    return out, obtained


def value_arrivals(body, areas, recorded_families):
    """the recorded arrival families that are NOT an arriving area --
    the ones that hold ONE VALUE, and keep an `IN` row."""
    area_families = set()
    for record in areas:
        area_families.add(record["base_family"])
    out = []
    for family in recorded_families:
        if family in area_families:
            continue
        out.append(family)
    return out


class AreaLedger(L.Ledger):
    """`ledger.Ledger` with the seventh block.

    Nothing of the eight blocks changes: `add` is the ledger's own
    `add` for every block it already knows, and this subclass only
    answers for `AREA`, which its parent refuses by name because it is
    not in `BLOCK_ORDER`.
    """

    def __init__(self, *args, **keywords):
        L.Ledger.__init__(self, *args, **keywords)
        self.area_rows = []
        self.area_count = 0

    def add_area(self, base_family, displacements, note=None):
        """one arriving area -> its extent in the AREA block.

        The row's `offset` is the extent's own base, and the unit's
        own displacements are preserved inside it by the affine map.
        """
        index = self.area_count
        base = extent_base(index)
        reached = []
        for displacement in displacements:
            inside = area_offset_of_displacement(displacement)
            reached.append({
                "the_body_spells": "0x%x" % displacement,
                "lands_at_offset_in_the_block": base + inside,
            })
        row = {
            "row": "%s-%d" % (AREA_BLOCK, index),
            "block": AREA_BLOCK,
            "index": index,
            "offset": base,
            "size": AREA_SPAN,
            "type": "an arriving addressable area",
            "produced_by": "arrival",
            "operands": [],
            "bound_to_the_same_symbol_as": "%" + base_family,
            "ledger_entry": AREA_ENTRY_INDEX,
            "ledger_entry_text": area_entry_text(),
            "the_map": "the identity inside the extent, origin 0x%x: "
                       "the unit's own displacement d addresses "
                       "extent_base + 0x%x + d, so the unit's internal "
                       "spacing is preserved and only the base moves"
                       % (AREA_ORIGIN, AREA_ORIGIN),
            "reaches": reached,
            "note": note or ("the runner fills this area and puts its "
                             "base in %%%s before the unit is entered"
                             % base_family),
        }
        self.area_count = index + 1
        self.area_rows.append(row)
        return row

    def as_list(self):
        out = L.Ledger.as_list(self)
        for row in self.area_rows:
            out.append(dict(row))
        return out

    def block_bytes(self):
        out = L.Ledger.block_bytes(self)
        out[AREA_BLOCK] = AREA_SPAN * self.area_count
        return out


def area_prelude_lines(row, base_family):
    """the prelude for one arriving area -- section 4.

    One step where the extent is the block's own base; a second `lea`
    where the extent or the origin moves the base.  Both write the
    family the body itself expects the base in, so gate check C2 sees
    only an arrival family.
    """
    pointer = L.register_text(base_family, 64)
    literal = []
    literal.append("mov %s,%s" % (area_entry_text(), pointer))
    shift = row["offset"] + AREA_ORIGIN
    if shift != 0:
        literal.append("lea 0x%x(%s),%s" % (shift, pointer, pointer))
    resolved = "lea %s,%s" % (row["row"], pointer)
    return literal, resolved


# ------------------------------------------------------------------
# the survey that decides AREA_ORIGIN -- section 3
# ------------------------------------------------------------------

def survey(records):
    """(unit label, body) pairs -> the displacement range each body
    spells from an arriving base."""
    out = []
    smallest = None
    largest = None
    for label, body in records:
        if body is None:
            out.append({"unit": label, "body": None})
            continue
        areas = read_arriving_areas(body)
        row = {
            "unit": label,
            "areas": [],
        }
        for record in areas:
            row["areas"].append({
                "base": "%" + record["base_family"],
                "smallest_displacement":
                    "0x%x" % record["smallest_displacement"],
                "largest_displacement":
                    "0x%x" % record["largest_displacement"],
                "sightings": record["sightings"],
                "first_sighting": record["first_sighting"],
                "also_named_by": list(record["also_named_by"]),
                "reached_through_an_index_register":
                    record["reached_through_an_index_register"],
                "advanced_by": list(record["advanced_by"]),
                "inside_the_extent":
                    record["largest_displacement"] < AREA_SPAN,
            })
            low = record["smallest_displacement"]
            high = record["largest_displacement"]
            if smallest is None or low < smallest:
                smallest = low
            if largest is None or high > largest:
                largest = high
        out.append(row)
    return {
        "records": out,
        "smallest_displacement_in_the_population": smallest,
        "largest_displacement_in_the_population": largest,
        "the_origin_this_implies":
            0 if (smallest is None or smallest >= 0) else -smallest,
        "the_origin_in_force": AREA_ORIGIN,
        "the_extent_span": AREA_SPAN,
    }
