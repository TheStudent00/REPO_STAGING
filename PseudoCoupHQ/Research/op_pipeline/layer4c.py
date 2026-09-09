#!/usr/bin/env python3
"""layer4c.py -- TASK 53: LAYER 4 read off the canon38 (ledger48)
provenance ledger.

WHAT THIS FILE IS, and why it is a THIRD file rather than an edit.
`layer4.py` (task 48) transcribes a ledger47 ledger.  canon38 changed
the ledger: eight blocks instead of six (STACK and X87 are new), a
per-opcode destination table that gives the division and wide-multiply
opcodes their own rows, a row type `flags only`, a row field
`written_half`, positional branch labels in the body, and a typed
`produced_by` object everywhere.  `layer4.py` is NOT edited -- the
brief forbids it and the record needs it intact -- so this file:

  * REPLAYS ledger48's own dataflow walk to recover, per row, the
    operand SLOTS of the body line that made it (a stored row names
    the rows it read, not which slot each filled), and CHECKS the
    replay against the stored ledger row for row: same names, same
    typed producers, same operands, same order.  A disagreement is
    refused by name; nothing is guessed.
  * REUSES layer4.py's producer table unchanged for every opcode that
    table already covers (`layer4.build_producer_term`,
    `layer4.build_pair_term`, `layer4.flags_of`, `layer4.Slot`,
    `layer4.cut`, `layer4.memory_load_term`, `layer4.input_symbol`).
  * ADDS the terms the new blocks and the new table need, and nothing
    else: the machine-stack rows, the x87 rows and their compare, and
    the destination table's halves.

THE FLAG STATE IS NOW A LINK, NOT A MEMORY.  layer4.py carried the
flags a previous opcode left in a running `context`, because ledger47
made no row for a comparison.  ledger48 makes one -- typed `flags
only` -- and puts it first in the operand list of the flag-reading
row.  So this file keys the flag state BY ROW: the pair reads the row
its own operand list names.  That is what closes log 147 section 4.1's
fifth cause.

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

No operator token appears in this file as a key, a grouping or a row
structure.  Every mnemonic this file records sits under `mnem`.

Coding discipline: no compound one-liner statements.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ledger48 is imported BEFORE layer4, deliberately: layer4 imports
# relink48, which instruments ledger47's own `mnemonic_of` for its own
# purposes, and ledger48 binds that name at import time.  Importing
# ledger48 first means ledger48 holds the plain function.
import ledger48 as L48                                            # noqa: E402
import canon                                                      # noqa: E402
import condition_table as CT                                      # noqa: E402
import ledger47 as L47                                            # noqa: E402
import region36 as R36                                            # noqa: E402
import layer4                                                     # noqa: E402
import z3                                                         # noqa: E402

NoTerm = layer4.NoTerm
Slot = layer4.Slot
cut = layer4.cut
full64 = layer4.full64


class ReplayDisagreement(Exception):
    """the replay does not reproduce the stored ledger; refused."""


# ------------------------------------------------------------------
# section 1: the x87 value sort
# ------------------------------------------------------------------
#
# An x87 register holds the 80-bit extended form: 15 exponent bits and
# a 64-bit significand.  z3's FPSort takes (exponent bits, significand
# bits including the leading bit), so FPSort(15, 64) is that form.  The
# comparison rule layer4.float_condition writes is sort-generic
# (fpIsNaN / fpEQ / fpLT), so it reads these values with no change.

X87_SORT = z3.FPSort(15, 64)


def x87_symbol(key):
    return z3.FP("x87_%s" % key, X87_SORT)


def mangle(text):
    out = text.replace("%", "").replace("(", "_").replace(")", "_")
    out = out.replace(",", "_").replace("-", "m").replace("$", "i")
    out = out.replace("*", "s").replace("+", "p").replace(":", "_")
    return out


# ------------------------------------------------------------------
# section 2: THE REPLAY -- ledger48's walk, with the slots kept
# ------------------------------------------------------------------

class Made(dict):
    """one row as this replay built it, with its slots attached."""


def replay(unit):
    """Returns a list of Made rows, in ledger48's own creation order,
    each carrying `slots` (the operand slots of its own body line, in
    the arch text's order) alongside the fields the stored ledger
    carries.  Raises ReplayDisagreement when the replay does not
    reproduce the stored ledger."""
    arrival_families = list(unit["arrival_families"])
    counts = {}
    for block in L48.BLOCK_ORDER:
        counts[block] = 0
    made = []

    def add(block, produced_by, operands, line, slots, **extra):
        index = counts[block]
        counts[block] = index + 1
        record = Made()
        record["row"] = L48.row_text(block, index)
        record["block"] = block
        record["index"] = index
        record["produced_by"] = L48.producer_object(produced_by)
        record["operands"] = list(operands)
        record["line"] = line
        record["slots"] = slots
        record.update(extra)
        made.append(record)
        return record

    # ---------------------------------------------------- prelude
    general = []
    vector = []
    for family in arrival_families:
        if L48.is_vector_family(family):
            vector.append(family)
        else:
            general.append(family)
    arrival_rows = []
    for family in vector + general:
        row = add("IN", "arrival", [], None, [],
                  prelude_loads_into=family)
        arrival_rows.append(row)

    # WHICH REGISTER AN INPUT ROW HOLDS, and the one place canon38
    # disagrees with itself.  ledger48's prelude emits the vector
    # arrivals first, so IN-0 is loaded into the first VECTOR family;
    # its dataflow walk, and the arrival contract canon38_wrapped.py
    # records, both bind IN-i to arrival_families[i] instead.  The two
    # differ only for a unit with both vector and general arrivals.
    # The ledger's own wiring is what layer 4 transcribes, so the
    # binding used here is the walk's -- the same one the stored
    # `arrival_contract_bindings` carries.  The disagreement is
    # reported, not smoothed.
    where = {}
    for index, family in enumerate(arrival_families):
        if index < len(arrival_rows):
            where[family] = arrival_rows[index]["row"]
            arrival_rows[index]["arrival_family"] = family
            loaded = arrival_rows[index]["prelude_loads_into"]
            if loaded != family:
                arrival_rows[index]["prelude_disagrees"] = True
    literals = {}
    own = {}
    stack = []
    x87 = []
    last_flag_row = [None]
    last_flag_setter = [None]
    # ONE rip counter for the whole unit, not one per line: a
    # rip-relative operand is keyed by its POSITION IN THE BODY, and
    # both the gate's reference simulator and textwalk48 count that
    # way, so the three sides name the same constant.
    rip_index = [0]

    def read_operand_slots(operands, mnemonic, treat_last_as_read):
        """(slots in arch order, the row names read in ledger48's own
        order).  This mirrors ledger48.walk_dataflow's
        `read_operand_rows` exactly; the slots are the extra this file
        needs and ledger48 does not keep."""
        slots = []
        named = []
        for position, operand in enumerate(operands):
            value = L48.immediate_value(operand)
            if value is not None:
                if operand not in literals:
                    row = add("CONST",
                              "the body's own immediate operand", [],
                              None, [], const_value=value)
                    literals[operand] = row["row"]
                named.append(literals[operand])
                slots.append(Slot(operand, None, immediate=value))
                continue
            position_in_x87 = L48.x87_position_of(operand)
            if position_in_x87 is not None:
                slot = Slot(operand, None)
                slot.x87_position = position_in_x87
                slots.append(slot)
                continue
            if operand.startswith("%"):
                family = L48.family_of_operand(operand)
                if family is None:
                    slots.append(Slot(operand, None))
                    continue
                is_last = position == len(operands) - 1
                skip = False
                if is_last:
                    if not treat_last_as_read:
                        if mnemonic in L48.PURE_WRITE_MNEMONICS:
                            skip = True
                slot = Slot(operand, None)
                slot.family = family
                slot.row_name = where.get(family)
                slots.append(slot)
                if skip:
                    continue
                if family in where:
                    named.append(where[family])
                continue
            inner = []
            if "(%rip)" in operand:
                inner.append(("rip", ("rip", rip_index[0])))
                rip_index[0] = rip_index[0] + 1
            for token in re.findall(r"%[a-z0-9]+", operand):
                family = canon.FAMILY_OF.get(token[1:])
                if family is None:
                    continue
                if family in where:
                    inner.append((token, where[family]))
                    named.append(where[family])
            for hit in R36.RSP_DISP.finditer(operand):
                displacement = int(hit.group(1), 16)
                key = "-0x%x(%%rsp)" % displacement
                if key not in own:
                    row = add("OWN",
                              "the body's own stack displacement", [],
                              None, [], displacement=displacement)
                    own[key] = row["row"]
                inner.append(("own", own[key]))
                named.append(own[key])
            slots.append(Slot(operand, None, memory=inner))
        return slots, named

    def x87_row_at(position, mnemonic):
        while len(x87) <= position:
            row = add("X87",
                      "an x87 stack position this unit did not itself "
                      "load", [], None, [],
                      x87_position=len(x87))
            x87.append(row["row"])
        return x87[position]

    for raw in unit["body_verbatim"]:
        line = R36.strip_annotation(raw)
        if line.endswith(":"):
            continue
        if line == "ret":
            continue
        mnemonic = L48.mnemonic_of(line)
        operands = L48.operands_of(line)

        base = L48.x87_base(mnemonic)
        if base is not None:
            named_positions = []
            for operand in operands:
                position = L48.x87_position_of(operand)
                if position is not None:
                    named_positions.append(position)
            slots, memory_rows = read_operand_slots(operands, mnemonic,
                                                    True)
            if base in L48.X87_LOADS:
                row = add("X87", mnemonic, memory_rows, line, slots,
                          x87_position=0, x87_base=base)
                x87.insert(0, row["row"])
                continue
            if base in L48.X87_STORES_POP or \
                    base in L48.X87_STORES_KEEP:
                top = x87_row_at(0, mnemonic)
                destination = None
                if operands:
                    destination = operands[-1]
                if destination is not None:
                    family = L48.family_of_operand(destination)
                    if family is not None:
                        if family not in canon.NEVER_RENAME:
                            where[family] = top
                if base in L48.X87_STORES_POP:
                    if x87:
                        x87.pop(0)
                continue
            if base in L48.X87_COMPARE_POP or \
                    base in L48.X87_COMPARE_KEEP:
                sides = []
                if named_positions:
                    for position in named_positions:
                        sides.append(x87_row_at(position, mnemonic))
                else:
                    sides.append(x87_row_at(0, mnemonic))
                add("TEMP", mnemonic, sides + memory_rows, line, slots,
                    row_type="flags only", x87_sides=list(sides),
                    x87_base=base)
                last_flag_setter[0] = mnemonic
                last_flag_row[0] = made[-1]["row"]
                if base in L48.X87_COMPARE_POP:
                    if x87:
                        x87.pop(0)
                continue
            if base in L48.X87_EXCHANGE:
                other = 1
                if named_positions:
                    other = named_positions[0]
                if other == 0:
                    continue
                x87_row_at(other, mnemonic)
                first = x87[0]
                x87[0] = x87[other]
                x87[other] = first
                continue
            sides = []
            for position in named_positions:
                sides.append(x87_row_at(position, mnemonic))
            if not sides:
                sides.append(x87_row_at(0, mnemonic))
            row = add("X87", mnemonic, sides + memory_rows, line, slots,
                      x87_sides=list(sides), x87_base=base)
            destination_position = 0
            if base in L48.X87_ARITH_POP:
                destination_position = 1
                if named_positions:
                    destination_position = named_positions[-1]
            elif named_positions:
                destination_position = named_positions[-1]
            x87_row_at(destination_position, mnemonic)
            row["x87_position"] = destination_position
            x87[destination_position] = row["row"]
            if base in L48.X87_ARITH_POP:
                if x87:
                    x87.pop(0)
            continue

        if mnemonic in L48.PUSH_STEMS:
            slots, read_rows = read_operand_slots(operands, mnemonic,
                                                  True)
            row = add("STACK", mnemonic, read_rows, line, slots,
                      flag_row=last_flag_row[0])
            stack.insert(0, row["row"])
            continue
        if mnemonic in L48.POP_STEMS:
            if stack:
                taken = stack.pop(0)
            else:
                row = add("STACK",
                          "a value the machine stack held before this "
                          "unit was entered", [], None, [])
                taken = row["row"]
            destination = None
            if operands:
                destination = operands[-1]
            if destination is not None:
                family = L48.family_of_operand(destination)
                if family is not None:
                    where[family] = taken
            continue

        stem, rule = L48.destination_rule(mnemonic, len(operands))
        if rule is not None:
            slots, read_rows = read_operand_slots(operands, mnemonic,
                                                  True)
            implicit = []
            implicit_pairs = []
            for family in rule["reads_implicitly"]:
                implicit_pairs.append((family, where.get(family)))
                if family in where:
                    implicit.append(where[family])
            all_read = implicit + read_rows
            written = []
            for family, half in rule["writes"]:
                row = add("TEMP",
                          L48.opcode_producer(mnemonic, half),
                          all_read, line, slots,
                          written_half=half, table_stem=stem,
                          implicit_rows=list(implicit),
                          implicit_pairs=list(implicit_pairs),
                          named_rows=list(read_rows),
                          flag_row=last_flag_row[0])
                written.append((family, row))
            for family, row in written:
                where[family] = row["row"]
            if L48.sets_the_flags(mnemonic):
                last_flag_setter[0] = mnemonic
                last_flag_row[0] = written[0][1]["row"]
            continue

        if L48.comparison_stem(mnemonic) is not None:
            slots, read_rows = read_operand_slots(operands, mnemonic,
                                                  True)
            add("TEMP", mnemonic, read_rows, line, slots,
                row_type="flags only")
            last_flag_setter[0] = mnemonic
            last_flag_row[0] = made[-1]["row"]
            continue

        slots, read_rows = read_operand_slots(operands, mnemonic, False)
        flag_reader = None
        if L48.SETCC.match(mnemonic):
            flag_reader = mnemonic
        if L48.CMOVCC.match(mnemonic):
            flag_reader = mnemonic
        if L48.is_flag_reading_transfer(mnemonic):
            flag_reader = mnemonic
        if flag_reader is not None:
            producer = [last_flag_setter[0], flag_reader]
            operands_of_row = list(read_rows)
            if last_flag_row[0] is not None:
                operands_of_row = [last_flag_row[0]] + operands_of_row
            row = add("GUARD", producer, operands_of_row, line, slots,
                      flag_row=last_flag_row[0])
            if L48.JCC.match(mnemonic):
                continue
            destination = None
            if operands:
                destination = operands[-1]
            if destination is not None:
                family = L48.family_of_operand(destination)
                if family is not None:
                    where[family] = row["row"]
            continue

        if mnemonic in L48.UNCONDITIONAL_TRANSFERS:
            continue
        if not operands:
            continue
        destination = operands[-1]
        family = L48.family_of_operand(destination)
        if family is None:
            continue
        if family in canon.NEVER_RENAME:
            continue
        row = add("TEMP", mnemonic, read_rows, line, slots,
                  flag_row=last_flag_row[0])
        where[family] = row["row"]
        if L48.sets_the_flags(mnemonic):
            last_flag_setter[0] = mnemonic
            last_flag_row[0] = row["row"]

    # ---------------------------------------------------- epilogue
    result_family = unit["result_family"]
    producer = "the body's last write to %%%s" % result_family
    answer_operands = []
    if result_family in where:
        answer_row = where[result_family]
        answer_operands = [answer_row]
        for row in made:
            if row["row"] == answer_row:
                producer = row["produced_by"]
                break
    add("OUT", producer, answer_operands, None, [])

    stored = unit["ledger"]
    if len(made) != len(stored):
        raise ReplayDisagreement(
            "the replay made %d rows, the stored ledger has %d"
            % (len(made), len(stored)))
    for index, (mine, theirs) in enumerate(zip(made, stored)):
        if mine["row"] != theirs["row"]:
            raise ReplayDisagreement(
                "row %d: the replay names %r, the stored ledger says %r"
                % (index, mine["row"], theirs["row"]))
        if mine["produced_by"] != theirs["produced_by"]:
            raise ReplayDisagreement(
                "row %s: the replay's producer is %r, the stored "
                "ledger's is %r"
                % (mine["row"], mine["produced_by"],
                   theirs["produced_by"]))
        if list(mine["operands"]) != list(theirs["operands"]):
            raise ReplayDisagreement(
                "row %s: the replay reads %r, the stored ledger says %r"
                % (mine["row"], mine["operands"], theirs["operands"]))
        mine["size"] = theirs["size"]
        mine["type"] = theirs["type"]
        mine["stored_value_at_run"] = theirs.get("value_at_run")
    return made


# ------------------------------------------------------------------
# section 3: the terms the new blocks and the new table need
# ------------------------------------------------------------------

DIVIDE_SIGNED = frozenset(["idiv"])
DIVIDE_UNSIGNED = frozenset(["div"])
WIDEN_ACCUMULATOR = {"cwtl": (16, 32), "cltq": (32, 64),
                     "cbtw": (8, 16)}
SIGN_SPREAD = {"cltd": 32, "cqto": 64}


def stack_term(row, slots):
    """a machine-stack row: `push` moves a value there, and the row
    holds the value it moved."""
    producer = row["produced_by"]
    if producer.get("kind") != "arch_opcode":
        raise NoTerm(producer.get("phrase"),
                     "this row stands for a value the machine stack "
                     "held before the unit was entered: no opcode in "
                     "this body put it there and no arrival row names "
                     "it, so there is nothing for a term to be about")
    if not slots:
        raise NoTerm(producer.get("mnem"),
                     "this opcode names no operand, so the value it "
                     "moved onto the machine stack has no source row")
    source = slots[0].term
    if source is None:
        raise NoTerm(producer.get("mnem"),
                     "the operand this opcode moved onto the machine "
                     "stack resolves to no row")
    return full64(cut(source, 64))


def x87_term(row, slots, terms):
    """an x87 stack row: a load brings a value in from memory or from
    another position; the arithmetic forms act on positions."""
    producer = row["produced_by"]
    if producer.get("kind") != "arch_opcode":
        return x87_symbol("outside_%s" % row["row"])
    mnemonic = producer["mnem"]
    base = row.get("x87_base")
    if base in L48.X87_LOADS:
        if base in ("fldz",):
            return z3.FPVal(0.0, X87_SORT)
        if base in ("fld1",):
            return z3.FPVal(1.0, X87_SORT)
        for slot in slots:
            if getattr(slot, "x87_position", None) is not None:
                raise NoTerm(mnemonic,
                             "this load copies another x87 stack "
                             "position, and this file follows only "
                             "loads from memory")
        for slot in slots:
            if slot.memory is not None:
                return x87_symbol(mangle(slot.text))
        raise NoTerm(mnemonic,
                     "this x87 load names no memory operand this file "
                     "can read")
    sides = row.get("x87_sides") or []
    values = []
    for name in sides:
        value = terms.get(name)
        if value is None:
            raise NoTerm(mnemonic,
                         "an x87 stack position this opcode reads has "
                         "no term")
        values.append(value)
    if base in ("fchs",):
        return -values[0]
    if base in ("fabs",):
        return z3.fpAbs(values[0])
    if base in ("fsqrt",):
        return z3.fpSqrt(z3.RNE(), values[0])
    raise NoTerm(mnemonic,
                 "no z3 term is written for this x87 arch opcode")


def x87_flags(row, terms):
    """the flags an x87 comparison leaves.

    `fucomip %st(1),%st` is AT&T order: the source is the position the
    text names first and the destination is `%st`, the top.  ledger48
    records the rows in that same text order, so the destination is the
    LAST of them."""
    sides = row.get("x87_sides") or []
    if len(sides) != 2:
        return None
    source = terms.get(sides[0])
    destination = terms.get(sides[1])
    if source is None or destination is None:
        return None
    return {
        "sides": (destination, source, "float"),
        "carry": None,
        "overflow": None,
        "setter": row["produced_by"]["mnem"],
    }


def table_term(row, slots, terms, line, seeds, tag):
    """the destination table's own halves: the division pair, the wide
    multiply pair, the sign spread, and the in-place widenings."""
    producer = row["produced_by"]
    mnemonic = producer["mnem"]
    stem = row.get("table_stem") or mnemonic
    half = row.get("written_half")
    pairs = row.get("implicit_pairs") or []
    named = row.get("named_rows") or []
    operands = L47.operands_of(line) if line else []

    def implicit_term(position):
        """the value the opcode reads without naming it.

        When the ledger holds a row for that register, the row's term
        is the value.  When it does not, the body read the register
        before anything in the body wrote it, so the value is the
        machine's own starting state -- one symbol per family, which
        is the same rule layer4.fill_slots applies to a NAMED operand
        in the same position, and the same symbol the gate's reference
        simulator seeds."""
        if position >= len(pairs):
            raise NoTerm(mnemonic,
                         "this opcode reads a register it does not "
                         "name, and the destination table has no "
                         "entry for that read")
        family, row_name = pairs[position]
        if row_name is None:
            return layer4.seed_of(seeds, family, tag)
        value = terms.get(row_name)
        if value is None:
            raise NoTerm(mnemonic,
                         "the row holding a register this opcode "
                         "reads without naming it has no term")
        return value

    def accumulator_term():
        return implicit_term(0)

    if stem in SIGN_SPREAD:
        width = SIGN_SPREAD[stem]
        accumulator = cut(accumulator_term(), width)
        sign = z3.Extract(width - 1, width - 1, accumulator)
        spread = z3.If(sign == z3.BitVecVal(1, 1),
                       z3.BitVecVal((1 << width) - 1, width),
                       z3.BitVecVal(0, width))
        return full64(spread)

    if stem in WIDEN_ACCUMULATOR:
        source_width, destination_width = WIDEN_ACCUMULATOR[stem]
        accumulator = accumulator_term()
        narrow = cut(accumulator, source_width)
        widened = z3.SignExt(destination_width - source_width, narrow)
        if destination_width >= 32:
            return full64(widened)
        keep = cut(accumulator, 64)
        mask = z3.BitVecVal((1 << destination_width) - 1, 64)
        return (keep & ~mask) | z3.ZeroExt(64 - destination_width,
                                           widened)

    width = layer4.operation_width(line, operands)
    if width is None:
        raise NoTerm(mnemonic,
                     "no operand width could be read off %r" % line)
    if not named:
        raise NoTerm(mnemonic,
                     "this opcode names no operand row to read")
    divisor_or_factor = terms.get(named[-1])
    if divisor_or_factor is None:
        raise NoTerm(mnemonic,
                     "the operand row this opcode reads has no term")
    right = cut(divisor_or_factor, width)

    if stem in DIVIDE_SIGNED or stem in DIVIDE_UNSIGNED:
        low = implicit_term(0)
        high = implicit_term(1)
        dividend = z3.Concat(cut(high, width), cut(low, width))
        wide_right = right
        if stem in DIVIDE_SIGNED:
            wide_right = z3.SignExt(width, right)
            quotient = dividend / wide_right
            remainder = z3.SRem(dividend, wide_right)
        else:
            wide_right = z3.ZeroExt(width, right)
            quotient = z3.UDiv(dividend, wide_right)
            remainder = z3.URem(dividend, wide_right)
        if half == "quotient":
            return full64(cut(quotient, width))
        return full64(cut(remainder, width))

    # the one-operand multiply forms
    accumulator = cut(accumulator_term(), width)
    if stem == "imul":
        product = z3.SignExt(width, accumulator) * \
            z3.SignExt(width, right)
    else:
        product = z3.ZeroExt(width, accumulator) * \
            z3.ZeroExt(width, right)
    if half == "low half":
        return full64(z3.Extract(width - 1, 0, product))
    return full64(z3.Extract(2 * width - 1, width, product))


# ------------------------------------------------------------------
# section 4: THE TRANSCRIPTION -- the canon38 ledger read as a term
# ------------------------------------------------------------------

class Transcription(object):
    """one unit's layer-4 record, over a canon38 ledger."""

    def __init__(self, unit):
        self.unit = unit
        self.terms = {}
        self.flag_states = {}
        self.holes = []
        self.cascades = []
        self.out_term = None
        self.inputs = {}
        self.rows = None
        self.refused = None
        self.seeds = {}


def producer_call_form(producer):
    """layer4.build_producer_term takes a mnemonic or a pair; ledger48
    stores a typed object.  This is the one place the object is turned
    back into the call form layer4 expects, and it is never written to
    an artifact."""
    if producer.get("kind") == "flag_pair":
        return list(producer["mnem"])
    return producer.get("mnem")


def hole_record(row, why):
    return {
        "row": row["row"],
        "producer": row["produced_by"],
        "producer_shape": ("pair"
                           if row["produced_by"].get("kind") ==
                           "flag_pair" else "single"),
        "line": row.get("line"),
        "why": why,
    }


def cascade_record(row, blocked):
    record = hole_record(row,
                         "an operand row has no term: %s" % blocked)
    record["blocked_by"] = blocked
    return record


def transcribe(unit, tag="a"):
    """LAYER 4 for one canon38 unit: the ledger, read from OUT-0 down.

    The walk below runs forward because ledger48's row order is the
    body's own order, so a row's operand rows are always transcribed
    before the row is reached; the TERM is still the bottom-up read of
    OUT-0, and `record.out_term` is that read."""
    record = Transcription(unit)
    try:
        rows = replay(unit)
    except ReplayDisagreement as problem:
        record.refused = "replay: %s" % problem
        return record
    except Exception as problem:
        record.refused = "replay raised %s: %s" \
            % (type(problem).__name__, problem)
        return record
    record.rows = rows
    terms = record.terms
    for row in rows:
        name = row["row"]
        block = row["block"]
        producer = row["produced_by"]
        slots = row.get("slots") or []
        if block == "IN":
            family = row.get("arrival_family")
            if family is None:
                record.holes.append(hole_record(
                    row, "no arrival family names the register this "
                         "input row arrives in"))
                continue
            symbol = layer4.input_symbol(row, family)
            terms[name] = symbol
            record.inputs[name] = symbol
            continue
        if block == "CONST":
            value = row.get("const_value") or 0
            terms[name] = z3.BitVecVal(value & ((1 << 64) - 1), 64)
            continue
        if block == "OWN":
            terms[name] = layer4.stack_pointer(tag) - \
                z3.BitVecVal(row.get("displacement", 0), 64)
            continue
        if block == "OUT":
            if not row["operands"]:
                record.holes.append(hole_record(
                    row,
                    "no arch opcode in this body writes the answer "
                    "register, so no row produces the answer"))
                continue
            source = terms.get(row["operands"][0])
            if source is None:
                record.cascades.append(cascade_record(
                    row, row["operands"][0]))
                continue
            if source.sort_kind() == z3.Z3_FLOATING_POINT_SORT:
                record.holes.append(hole_record(
                    row,
                    "the row this answer reads holds an x87 extended "
                    "value, and no rule in this file returns one to "
                    "the answer register's bits"))
                continue
            terms[name] = cut(source, row["size"] * 8)
            record.out_term = terms[name]
            continue

        layer4.fill_slots(slots, terms, record.seeds, tag)
        blocked = None
        for operand_row in row["operands"]:
            if terms.get(operand_row) is None:
                blocked = operand_row
                break
        if block == "X87":
            if producer.get("kind") != "arch_opcode":
                terms[name] = x87_symbol("outside_%s" % name)
                continue
        if blocked is not None:
            record.cascades.append(cascade_record(row, blocked))
            continue
        try:
            if block == "STACK":
                terms[name] = stack_term(row, slots)
                continue
            if block == "X87":
                terms[name] = x87_term(row, slots, terms)
                continue
            if row.get("row_type") == "flags only":
                if row.get("x87_sides"):
                    found = x87_flags(row, terms)
                else:
                    mnemonic = producer["mnem"]
                    found = layer4.flags_of(mnemonic, slots,
                                            row["line"], None)
                if found is None:
                    record.holes.append(hole_record(
                        row,
                        "this comparison's own row is in the ledger, "
                        "and the two sides it compared could not be "
                        "built into flags this file models"))
                    continue
                record.flag_states[name] = found
                terms[name] = z3.BitVecVal(0, 64)
                continue
            if row.get("written_half") is not None:
                terms[name] = table_term(row, slots, terms,
                                         row["line"], record.seeds,
                                         tag)
                continue
            if producer.get("kind") == "flag_pair":
                # THE FLAG STATE COMES FROM THE LINKED ROW AND FROM
                # NOWHERE ELSE.  ledger48 puts the flag-holding row
                # first in this row's operand list; that row is the
                # one the machine's flags came from.  An earlier
                # search through the rest of the operand list was
                # tried and REMOVED: a flag reader's own destination
                # operand can resolve to some unrelated row that
                # happens to carry a flag state, and reading it gave
                # `c/regen_36623` an answer built from a shift's
                # flags rather than from the subtract-with-borrow's.
                flag_row = row.get("flag_row")
                flags = None
                if flag_row is not None:
                    flags = record.flag_states.get(flag_row)
                context = {"flags": flags}
                terms[name] = layer4.build_pair_term(
                    producer_call_form(producer), row["line"], slots,
                    row, context)
                continue
            context = {"flags":
                       record.flag_states.get(row.get("flag_row"))}
            terms[name] = layer4.build_producer_term(
                producer_call_form(producer), row["line"], slots, row,
                context)
        except NoTerm as problem:
            record.holes.append(hole_record(row, problem.why))
        except Exception as problem:
            record.holes.append(hole_record(
                row, "building the term raised %s: %s"
                     % (type(problem).__name__, problem)))
            continue
        if name in terms:
            if row.get("row_type") != "flags only":
                if L48.sets_the_flags(
                        producer.get("mnem")
                        if producer.get("kind") == "arch_opcode"
                        else ""):
                    try:
                        found = layer4.flags_of(producer["mnem"], slots,
                                                row["line"],
                                                terms.get(name))
                    except Exception:
                        found = None
                    if found is not None:
                        record.flag_states[name] = found
    return record
