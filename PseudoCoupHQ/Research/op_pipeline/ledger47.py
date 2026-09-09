#!/usr/bin/env python3
"""ledger47.py -- THE MEMORY-WRAPPED FORM and THE PROVENANCE LEDGER.

TASK 47, round 10.  This file is the definition of the form the owner ruled
on 2026-09-02.  His two rulings are the specification, verbatim.

RULING 1:

    "keeping the arch-unit usage of registers as is but with our
    insertion of loading from memory. because if the compiler already
    presents a form that is free of register conflicts and we can
    insert our memory-paradigm to update within the compiler-proven
    register use, we get the consistent symbolics for z3 and a
    functioning arch-unit."

RULING 2:

    "the ledger should also track the operator that a result might
    create. all the data moving through the arch-units, even temporary
    data."

--------------------------------------------------------------------
1.  WHAT IS SUPERSEDED, AND WHY
--------------------------------------------------------------------

region36.py / canon36_universal.py (round 9, log_135) stay on disk
untouched as the superseded record.  TWO of their choices are dropped
here, by name:

  * THE %r15 ANCHOR is dropped.  Round 9 reserved %r15 as the region
    base, so a unit whose own body mentions %r15 was REFUSED BY NAME
    (measured: 4 of the 1,779 -- cpp/op_765, cpp/op_770, swift/op_703,
    swift/op_739).  Those refusals were self-inflicted.  Here the
    ledger lives at an ABSOLUTE ADDRESS reached rip-relative, so NO
    register is reserved and no body can collide with the form.
  * THE SCRATCH-REGISTER REWRITE (round 9's rule R) is dropped.  Round
    9 renamed every register family in the body by a fixed pool order.
    Ruling 1 forbids that: the compiler's register use is already
    proven conflict-free, so it is REUSED, not redone.  The body is
    kept CHARACTER-FOR-CHARACTER.

What is KEPT from round 9: the BLOCK VOCABULARY (the six allocation
kinds) and THE GATE (prove the wrapped text against the unit's own
ship code, under the arrival contract, reading the answer out of the
output block and never out of a register).

--------------------------------------------------------------------
2.  THE LEDGER: WHAT IT IS, MECHANICALLY
--------------------------------------------------------------------

The ledger is a small table in RAM.  It has ONE entry per block, each
entry EIGHT BYTES, holding that block's real base address.  The
entries are in a fixed order, so "block k" is always "ledger entry k":

    entry  offset   block   what the block holds
    ---------------------------------------------------------------
      0    0x00     IN      one row per input argument
      1    0x08     CONST   one row per literal the body materializes
      2    0x10     TEMP    one row per intermediate value
      3    0x18     OWN     one row per stack address the unit owns
      4    0x20     GUARD   one row per guard outcome
      5    0x28     OUT     the answer; OUT-0 is the answer's row
    ---------------------------------------------------------------
    LEDGER_ENTRIES = 6, LEDGER_BYTES = 0x30

THE LEDGER'S OWN BASE IS AN ABSOLUTE ADDRESS.  It is written in the
text as a rip-relative operand on a named symbol:

    mov ledger+0x00(%rip),%rdi

RELOCATION, stated: `ledger` is an ordinary symbol in the unit's
object file.  The assembler emits an R_X86_64_PC32 relocation for the
rip-relative operand; the link editor (or the loader, for a
position-independent image) resolves it to the one address the runner
placed the table at.  No register is reserved, no base is passed in,
and the operand is a real x86-64 encoding -- canon37_assemble.py
assembles it with `as` and reads it back with `objdump`.

ADDRESSING IS TWO STEPS, ALWAYS.  Reading input row 0:

    mov ledger+0x00(%rip),%rdi     step 1: the IN block's base address
    mov 0x0(%rdi),%rdi             step 2: the row inside that block

Step 1 uses the DESTINATION REGISTER ITSELF as the pointer, so the
prelude needs no scratch register at all for a general-register
arrival, and nothing the body will read can be disturbed.

NO CONTIGUITY IS ASSUMED.  Nothing in the text says where any block
is, or that any two blocks are near each other.  The runner allocates
the six blocks wherever it likes, writes their addresses into the six
ledger entries, fills the IN rows, calls the unit, and reads OUT-0.

--------------------------------------------------------------------
3.  ROWS ARE TYPED, AND A ROW IS SIZED BY ITS TYPE
--------------------------------------------------------------------

Round 9 gave every block an 8-byte slot.  That is why 1,479
regenerated units were REFUSED BY NAME for reading a vector register
in a way an 8-byte slot could not carry ("P2 lane safety").  Here a
row's SIZE IS ITS TYPE'S SIZE:

    a general-register argument   ->  8-byte row,  loaded with `mov`
    a vector-register argument    ->  16-byte row, loaded with `movdqu`

so a 16-byte value gets a 16-byte row and arrives whole.  Rows inside
a block are laid out in allocation order, each aligned up to its own
size, so a 16-byte row is 16-byte aligned.

--------------------------------------------------------------------
4.  THE WRAPPED FORM: PRELUDE, BODY VERBATIM, EPILOGUE
--------------------------------------------------------------------

    <prelude>    one two-step load per input row, into the register
                 the ARRIVAL CONTRACT names for that argument
    <body>       the compiler's own instructions, character for
                 character, in their own order
    <epilogue>   one two-step store of the compiler's result register
                 into OUT-0, immediately before every `ret`

Nothing else is touched.  The body's registers are the compiler's;
its immediates are the compiler's; its own stack addresses are the
compiler's.

THE ARRIVAL CONTRACT is the recorded fact of which register the
compiler expects each input in -- c takes its first two in
%rdi/%rsi, go takes its in %rax/%rbx, an sret unit takes its
destination seat in %rdi.  The prelude loads INTO those registers;
it never moves an argument to a register of our choosing.

SCRATCH REGISTERS, by one fixed rule and only where unavoidable:

  * a general-register arrival needs NO scratch (section 2);
  * a vector arrival needs one general register to hold the IN block's
    base.  It is the first family of the fixed pool that is not a
    general arrival family.  Vector loads run FIRST, so this register
    is either reloaded by a later general arrival load or is a family
    the body never reads before writing (the arrival contract is
    exactly "the families the body reads before it writes them").
  * the epilogue needs one general register to hold the OUT block's
    base.  It is the first family of the fixed pool that is not the
    result family.  The body has finished by then.

    fixed pool: r11 r10 rax rcx rdx rsi rdi r8 r9 rbx r12 r13 r14 r15

--------------------------------------------------------------------
5.  THE PROVENANCE LEDGER (ruling 2)
--------------------------------------------------------------------

Every value that moves through the unit gets a ROW, and every row
carries:

    row            its name, e.g. IN-0, TEMP-3, OUT-0
    block          IN / CONST / TEMP / OWN / GUARD / OUT
    index, offset, size
    type           what the row holds, in machine terms
    produced_by    THE ARCH OPCODE that made this value, or, for a
                   flag-derived value, THE PAIR (flag-setting opcode,
                   flag-reading opcode).  Never an operator token, and
                   never a lifter helper name.
    operands       the rows this value was computed from
    value_at_run   the value observed when the unit was executed, when
                   it was executed; null otherwise

Temporaries and guard outcomes get rows whether or not they are also
stored to memory.  Storing is a separate and cheap choice; the ROWS
are the information.  Read as a whole, the table IS the unit's
dataflow graph.

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
compound one-liner statements.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import region36 as R36                                           # noqa: E402

LEDGER_SYMBOL = "ledger"
BLOCK_ORDER = ("IN", "CONST", "TEMP", "OWN", "GUARD", "OUT")
LEDGER_ENTRY_SIZE = 8
LEDGER_ENTRIES = len(BLOCK_ORDER)
LEDGER_BYTES = LEDGER_ENTRY_SIZE * LEDGER_ENTRIES

SCRATCH_POOL = ["r11", "r10", "rax", "rcx", "rdx", "rsi", "rdi",
                "r8", "r9", "rbx", "r12", "r13", "r14", "r15"]

ROW_TEXT = re.compile(r"^(IN|CONST|TEMP|OWN|GUARD|OUT)-(\d+)$")

PURE_WRITE_MNEMONICS = frozenset([
    "mov", "movl", "movq", "movb", "movw", "movabs",
    "movzbl", "movzwl", "movzbq", "movzwq", "movsbl", "movswl",
    "movsbq", "movswq", "movslq", "movsbw", "movzbw",
    "lea", "movss", "movsd", "movaps", "movapd", "movdqa", "movdqu",
    "movd", "set", "xorps", "pxor",
])

# THE ARCH OPCODES THAT SET THE FLAGS A LATER OPCODE READS.
# Kept as STEMS: an operand-size suffix (b/w/l/q) is stripped before
# the test, so `cmpl` and `cmpq` are both `cmp`.  The x87 and SSE
# comparison forms are here too, because they are what a float unit's
# `setp`/`setne` pair actually reads (measured at first observation on
# this lap: `fucomip` in c/regen_34 and `mul` in swift/op_128 were
# missing, and 1,156 guard rows reported the hole rather than hiding
# it).
FLAG_SETTER_STEMS = frozenset([
    "cmp", "test",
    "add", "sub", "and", "or", "xor", "inc", "dec", "neg",
    "shl", "shr", "sar", "sal", "rol", "ror", "rcl", "rcr",
    "shld", "shrd",
    "adc", "sbb", "imul", "mul", "div", "idiv",
    "bt", "bts", "btr", "btc", "bsf", "bsr", "popcnt", "lzcnt",
    "tzcnt", "xadd", "cmpxchg",
    "ucomiss", "ucomisd", "comiss", "comisd",
    "vucomiss", "vucomisd", "vcomiss", "vcomisd",
    "fucomi", "fucomip", "fcomi", "fcomip", "fucom", "fucomp",
    "fcom", "fcomp", "ftst",
    "ptest", "vptest",
    "cmpeqss", "cmpeqsd", "cmpss", "cmpsd",
])

SIZE_SUFFIX = ("b", "w", "l", "q")


def flag_setter_stem(mnemonic):
    """the stem of `mnemonic`, with ONE operand-size suffix removed and
    only when removing it leaves a stem this file knows."""
    if mnemonic in FLAG_SETTER_STEMS:
        return mnemonic
    if len(mnemonic) < 2:
        return None
    if mnemonic[-1] in SIZE_SUFFIX:
        stem = mnemonic[:-1]
        if stem in FLAG_SETTER_STEMS:
            return stem
    return None


def sets_the_flags(mnemonic):
    return flag_setter_stem(mnemonic) is not None


class Refusal(Exception):
    """refused BY NAME, never silently."""

    def __init__(self, cause, detail):
        Exception.__init__(self, detail)
        self.cause = cause
        self.detail = detail


# ------------------------------------------------------------------
# the ledger's own addressing
# ------------------------------------------------------------------

def ledger_entry_index(block):
    return BLOCK_ORDER.index(block)


def ledger_entry_offset(block):
    return LEDGER_ENTRY_SIZE * ledger_entry_index(block)


def ledger_entry_text(block):
    """step 1 of the two-step: the operand that reads the block's base
    address out of the ledger, at an absolute address, rip-relative."""
    return "%s+0x%02x(%%rip)" % (LEDGER_SYMBOL, ledger_entry_offset(block))


def row_text(block, index):
    return "%s-%d" % (block, index)


def is_row_text(text):
    return ROW_TEXT.match(text) is not None


def parse_row_text(text):
    hit = ROW_TEXT.match(text)
    if hit is None:
        return None
    return hit.group(1), int(hit.group(2))


# ------------------------------------------------------------------
# rows
# ------------------------------------------------------------------

def align_up(value, alignment):
    if alignment <= 1:
        return value
    remainder = value % alignment
    if remainder == 0:
        return value
    return value + (alignment - remainder)


class LedgerTable(object):
    """the provenance ledger of one unit: one row per value that moves
    through it, in block order, each row typed and sized by its type."""

    def __init__(self):
        self.rows = []
        self.by_row = {}
        self.next_offset = {}
        self.counts = {}
        for block in BLOCK_ORDER:
            self.next_offset[block] = 0
            self.counts[block] = 0

    def add(self, block, size, type_name, produced_by, operands,
            note=None, resident=None):
        if block not in BLOCK_ORDER:
            raise Refusal("unknown block",
                          "the ledger was asked for block %r" % block)
        index = self.counts[block]
        offset = align_up(self.next_offset[block], size)
        name = row_text(block, index)
        record = {
            "row": name,
            "block": block,
            "index": index,
            "offset": offset,
            "size": size,
            "type": type_name,
            "produced_by": produced_by,
            "operands": list(operands),
            "value_at_run": None,
            "ledger_entry": ledger_entry_index(block),
            "ledger_entry_text": ledger_entry_text(block),
        }
        if note is not None:
            record["note"] = note
        if resident is not None:
            record["resident"] = resident
        self.counts[block] = index + 1
        self.next_offset[block] = offset + size
        self.rows.append(record)
        self.by_row[name] = record
        return record

    def block_bytes(self):
        out = {}
        for block in BLOCK_ORDER:
            out[block] = self.next_offset[block]
        return out

    def as_list(self):
        return list(self.rows)


# ------------------------------------------------------------------
# reading a body
# ------------------------------------------------------------------

def split_lines(text):
    return R36.split_lines(text)


def operands_of(line):
    return R36.operands_of(line, G33.split_operands)


def mnemonic_of(line):
    return R36.mnemonic_of(line)


def family_of_operand(operand):
    if not operand.startswith("%"):
        return None
    return canon.FAMILY_OF.get(operand[1:])


def is_vector_family(family):
    if family is None:
        return False
    return family.startswith("xmm")


def register_text(family, width):
    """the spelling of `family` at `width` bits."""
    if is_vector_family(family):
        return "%" + family
    index = {64: 0, 32: 1, 16: 2, 8: 3}.get(width)
    if index is None:
        index = 0
    return "%" + R36.widened(family, index)


def pick_scratch(reserved):
    for family in SCRATCH_POOL:
        if family in reserved:
            continue
        return family
    raise Refusal(
        "no scratch register",
        "every family of the fixed pool is reserved by this unit, so "
        "the form has no register to hold a block base in")


# ------------------------------------------------------------------
# the wrapper
# ------------------------------------------------------------------

def build_prelude(arrival_families, table):
    """(literal_lines, resolved_lines, rows).  One two-step load per
    input row, into the register the arrival contract names."""
    literal = []
    resolved = []
    rows = []
    general = []
    vector = []
    for family in arrival_families:
        if is_vector_family(family):
            vector.append(family)
        else:
            general.append(family)
    scratch = None
    if vector:
        scratch = pick_scratch(set(general) | set(canon.NEVER_RENAME))
    order = vector + general
    for family in order:
        if is_vector_family(family):
            size = 16
            type_name = "16-byte vector value"
        else:
            size = 8
            type_name = "8-byte general value"
        row = table.add("IN", size, type_name, "arrival",
                        [], note="the runner fills this row before the "
                                 "unit is entered")
        rows.append(row)
        if is_vector_family(family):
            pointer = register_text(scratch, 64)
            literal.append("mov %s,%s" % (ledger_entry_text("IN"),
                                          pointer))
            literal.append("movdqu 0x%x(%s),%%%s"
                           % (row["offset"], pointer, family))
            resolved.append("movdqu %s,%%%s" % (row["row"], family))
        else:
            pointer = register_text(family, 64)
            literal.append("mov %s,%s" % (ledger_entry_text("IN"),
                                          pointer))
            literal.append("mov 0x%x(%s),%s"
                           % (row["offset"], pointer, pointer))
            resolved.append("mov %s,%s" % (row["row"], pointer))
    return literal, resolved, rows, scratch


def build_epilogue(result_family, result_width, table, producer,
                   operands):
    """(literal_lines, resolved_lines, row).  One two-step store of the
    compiler's own result register into OUT-0."""
    if result_family is None:
        raise Refusal(
            "no answer home",
            "this unit's own code names no register the answer is left "
            "in, so there is nothing to store into OUT-0")
    if is_vector_family(result_family):
        if result_width > 64:
            size = 16
            mnemonic = "movdqu"
            source = "%" + result_family
            type_name = "16-byte vector value"
        else:
            size = 8
            mnemonic = "movq"
            source = "%" + result_family
            type_name = "8-byte vector-held value"
    else:
        size = max(1, result_width // 8)
        size = align_up(size, 1)
        if size not in (1, 2, 4, 8):
            size = 8
        mnemonic = "mov"
        source = register_text(result_family, size * 8)
        type_name = "%d-byte general value" % size
    row = table.add("OUT", size, type_name, producer, operands,
                    note="the answer; the runner reads this row when "
                         "the unit returns")
    scratch = pick_scratch(set([result_family]) | set(canon.NEVER_RENAME))
    pointer = register_text(scratch, 64)
    literal = []
    literal.append("mov %s,%s" % (ledger_entry_text("OUT"), pointer))
    literal.append("%s %s,0x%x(%s)"
                   % (mnemonic, source, row["offset"], pointer))
    resolved = ["%s %s,%s" % (mnemonic, source, row["row"])]
    return literal, resolved, row, scratch


def weave(body, prelude, epilogue):
    """the wrapped text: the prelude ahead of the first executable
    instruction, the epilogue immediately before every `ret`."""
    first = None
    for index, line in enumerate(body):
        if line.endswith(":"):
            continue
        first = index
        break
    if first is None:
        raise Refusal("no executable instruction",
                      "the body carries no executable instruction")
    returns = 0
    for line in body:
        if line == "ret":
            returns = returns + 1
    if returns == 0:
        raise Refusal("never returns",
                      "the body never returns, so the answer has no "
                      "place to be stored")
    out = []
    for index, line in enumerate(body):
        if index == first:
            out.extend(prelude)
        if line == "ret":
            out.extend(epilogue)
        out.append(line)
    return out, returns


# ------------------------------------------------------------------
# the dataflow walk that fills TEMP, CONST, OWN and GUARD rows
# ------------------------------------------------------------------

IMMEDIATE = re.compile(r"^\$(-?0x[0-9a-fA-F]+|-?\d+)$")
SETCC = re.compile(r"^set[a-z]+$")
JCC = re.compile(r"^j[a-z]+$")
CMOVCC = re.compile(r"^cmov[a-z]+$")


def immediate_value(operand):
    hit = IMMEDIATE.match(operand)
    if hit is None:
        return None
    text = hit.group(1)
    if text.startswith("-0x"):
        return -int(text[3:], 16)
    if text.startswith("0x"):
        return int(text, 16)
    return int(text, 10)


def walk_dataflow(body, table, arrival_rows, arrival_families):
    """emit a row for every value the body produces.

    The producer of a row is THE ARCH OPCODE that wrote it.  For a
    value derived from the flags -- what a `setcc`, a `cmovcc` or a
    conditional branch reads -- the producer is THE PAIR (the
    flag-setting opcode, the flag-reading opcode), which is a real
    arch-opcode producer, never a lifter helper name."""
    where = {}
    for index, family in enumerate(arrival_families):
        where[family] = arrival_rows[index]["row"]
    literals = {}
    own = {}
    last_flag_setter = None
    notes = []
    for raw in body:
        line = R36.strip_annotation(raw)
        if line.endswith(":"):
            continue
        if line == "ret":
            continue
        mnemonic = mnemonic_of(line)
        operands = operands_of(line)
        read_rows = []
        for position, operand in enumerate(operands):
            value = immediate_value(operand)
            if value is not None:
                if operand not in literals:
                    row = table.add("CONST", 8, "literal",
                                    "the body's own immediate operand",
                                    [], note="not materialized: the "
                                             "body is kept verbatim, "
                                             "so the literal stays an "
                                             "immediate in the text")
                    row["value_at_run"] = value
                    literals[operand] = row["row"]
                read_rows.append(literals[operand])
                continue
            if operand.startswith("%"):
                family = family_of_operand(operand)
                if family is None:
                    continue
                is_last = position == len(operands) - 1
                if is_last:
                    if mnemonic in PURE_WRITE_MNEMONICS:
                        continue
                if family in where:
                    read_rows.append(where[family])
                continue
            # a register inside a memory operand is a READ of that
            # register's row (it is part of the address computation).
            for token in re.findall(r"%[a-z0-9]+", operand):
                family = canon.FAMILY_OF.get(token[1:])
                if family is None:
                    continue
                if family in where:
                    read_rows.append(where[family])
            for hit in R36.RSP_DISP.finditer(operand):
                displacement = int(hit.group(1), 16)
                key = "-0x%x(%%rsp)" % displacement
                if key not in own:
                    row = table.add(
                        "OWN", 8, "the unit's own stack address",
                        "the body's own stack displacement", [],
                        note="the body is kept verbatim, so this row "
                             "records the address the body itself "
                             "spells: %%rsp - 0x%x" % displacement)
                    row["displacement"] = displacement
                    row["address_is"] = "%%rsp - 0x%x" % displacement
                    own[key] = row["row"]
                read_rows.append(own[key])
        if sets_the_flags(mnemonic):
            last_flag_setter = mnemonic
        flag_reader = None
        if SETCC.match(mnemonic):
            flag_reader = mnemonic
        if CMOVCC.match(mnemonic):
            flag_reader = mnemonic
        if JCC.match(mnemonic):
            flag_reader = mnemonic
        if flag_reader is not None:
            producer = [last_flag_setter, flag_reader]
            if last_flag_setter is None:
                producer = [None, flag_reader]
                notes.append({
                    "row_producer_hole": flag_reader,
                    "why": "no flag-setting arch opcode precedes this "
                           "flag-reading opcode in the body, so the "
                           "pair the ledger records is incomplete",
                })
            row = table.add("GUARD", 8, "flag-derived value", producer,
                            read_rows,
                            note="the producer is the pair "
                                 "(flag-setting opcode, flag-reading "
                                 "opcode), which is what actually made "
                                 "this value")
            if JCC.match(mnemonic):
                continue
            destination = operands[-1] if operands else None
            if destination is not None:
                family = family_of_operand(destination)
                if family is not None:
                    where[family] = row["row"]
            continue
        if not operands:
            continue
        destination = operands[-1]
        family = family_of_operand(destination)
        if family is None:
            continue
        if family in canon.NEVER_RENAME:
            continue
        size = 16 if is_vector_family(family) else 8
        type_name = "16-byte vector value" if size == 16 \
            else "8-byte general value"
        row = table.add("TEMP", size, type_name, mnemonic, read_rows,
                        resident="register %%%s" % family)
        where[family] = row["row"]
    return where, notes


# ------------------------------------------------------------------
# the whole render for one unit
# ------------------------------------------------------------------

def wrap_unit(body_text, arrival_families, result_family, result_width):
    """(fields, None) or raises Refusal.

    fields carries the LITERAL wrapped text (real instructions, real
    encodings, assembled by canon37_assemble.py) and the RESOLVED text
    (the same text with each two-step pair written as one line naming
    the row, which is what the gate's simulator walks).  The two are
    the same thing: section 2's lemma, checked once by
    canon37_lemma.py, is that step 1 followed by step 2 reads exactly
    the row the resolved line names."""
    if not body_text:
        raise Refusal("no text",
                      "no text exists for this unit, so there is no "
                      "body to wrap")
    body = split_lines(body_text)
    for raw in body:
        line = R36.strip_annotation(raw)
        if LEDGER_SYMBOL in line:
            raise Refusal(
                "the body names the ledger symbol",
                "the body spells %r, which would collide with the "
                "form's own symbol" % LEDGER_SYMBOL)
    table = LedgerTable()
    prelude_literal, prelude_resolved, arrival_rows, prelude_scratch = \
        build_prelude(arrival_families, table)
    where, holes = walk_dataflow(body, table, arrival_rows,
                                 arrival_families)
    producer = "the body's last write to %%%s" % result_family
    operands = []
    if result_family in where:
        answer_row = where[result_family]
        operands = [answer_row]
        source_row = table.by_row.get(answer_row)
        if source_row is not None:
            producer = source_row["produced_by"]
    epilogue_literal, epilogue_resolved, out_row, epilogue_scratch = \
        build_epilogue(result_family, result_width, table, producer,
                       operands)
    literal_lines, returns = weave(body, prelude_literal,
                                   epilogue_literal)
    resolved_lines, _ = weave(body, prelude_resolved, epilogue_resolved)
    fields = {
        "wrapped_text": "; ".join(literal_lines),
        "wrapped_text_resolved": "; ".join(resolved_lines),
        "body_verbatim": list(body),
        "prelude": prelude_literal,
        "prelude_resolved": prelude_resolved,
        "epilogue": epilogue_literal,
        "epilogue_resolved": epilogue_resolved,
        "prelude_scratch": prelude_scratch,
        "epilogue_scratch": epilogue_scratch,
        "returns": returns,
        "ledger": table.as_list(),
        "ledger_block_bytes": table.block_bytes(),
        "ledger_symbol": LEDGER_SYMBOL,
        "ledger_entries": list(BLOCK_ORDER),
        "out_row": out_row["row"],
        "arrival_families": list(arrival_families),
        "result_family": result_family,
        "result_width": result_width,
        "producer_holes": holes,
        "addressing": "two steps: read the block's base out of the "
                      "ledger at an absolute address (rip-relative), "
                      "then read the row inside that block",
    }
    return fields
