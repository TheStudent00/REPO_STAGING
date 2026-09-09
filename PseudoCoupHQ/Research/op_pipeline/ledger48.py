#!/usr/bin/env python3
"""ledger48.py -- THE MEMORY-WRAPPED FORM, REPAIRED (canon38).

TASK 52, round 11.  `ledger47.py` is NOT edited: everything this file
does not change is IMPORTED from it, so the two forms cannot drift on
the parts that are the same.

WHAT THIS FILE CHANGES, and nothing else, each item naming the ruling
it implements (the owner, 2026-09-02; AgentMemory "ROUND 10 RULINGS";
briefs in log_151).

RULING 2 -- TWO MORE BLOCK KINDS.  The fixed block order becomes

    IN / CONST / TEMP / OWN / STACK / X87 / GUARD / OUT

  * STACK is the MACHINE STACK.  `push` makes a row that holds the
    value it moved; `pop` takes the newest such row and binds the
    register it wrote to it.  A `pop` with no matching `push` inside
    the body makes a row typed as a value that was on the stack
    before the unit was entered, rather than nothing at all.
    Census cause closed: 4,298 rows had no row to be about.
  * X87 is the x87 REGISTER STACK, positions %st .. %st(7).  A load
    (`fld`, `fild`, `fldz`, `fld1`) pushes a row; a store with a pop
    (`fstp`, `fistp`) takes one off; an arithmetic form reads the
    positions it names and writes one of them; `fxch` swaps two
    positions; a comparison (`fucomip`, `fucomi`, `fcomi`, ...) reads
    the two positions it names and writes NO row of its own -- it
    writes the flags, which is what the following flag-reading opcode
    picks up.  Census cause closed: 1,072 rows had no row to be about.

RULING 3 -- IMPLICIT DESTINATIONS ARE PER-OPCODE RULES.  ledger47's
one rule ("the destination is the last named operand") is wrong for
every opcode that writes a register it does not name.  Here there is
a TABLE, one row per opcode:

    opcode          writes                        reads implicitly
    ----------------------------------------------------------------
    idiv, div       accumulator = quotient,       accumulator, data
                    data register = remainder     register (the
                                                  dividend pair)
    mul, imul       accumulator = low half,       accumulator
    (one operand)   data register = high half
    cltd, cqto      data register                 accumulator
    cwtl, cltq,     accumulator                   accumulator
    cbtw

  and, also under this ruling:

  * an unconditional `jmp` is NEVER a flag reader (ledger47's `j[a-z]+`
    pattern matched it and made a GUARD row with no condition to be:
    324 such rows);
  * a COMPARISON opcode's row is typed `flags only` and does NOT
    rebind its named destination.  ledger47 made a TEMP row for
    `cmp %esi,%edi` typed as an ordinary write and repointed %rdi at
    it, which is false of the machine.  The flags row is carried
    forward and becomes an OPERAND of the flag-reading opcode's GUARD
    row, so the pair's lineage is in the ledger instead of being
    named in prose.

RULING 4 -- BRANCH LABELS ARE POSITIONAL.  A transfer whose target is
inside this unit is stored as `L0`, `L1`, ... assigned in ADDRESS
ORDER, with the label defined on the instruction it names; the
objdump symbol comment (`<main.op_174+0x18>`) is dropped.  A transfer
OUT of the unit keeps its callee -- that is real information, and it
is not the unit's own name -- but loses the address and the angle
brackets: `call 12 <__truncsfhf2@plt> !!reloc=...` becomes
`call x___truncsfhf2 !!reloc=...`.  Log 148 §4.2.2 measured what this
is worth: distinct layer-3 texts 6,277 -> about 2,999.

RULING 5 -- EVERY `produced_by` IS A TYPED OBJECT.  `{"kind": ...,
"mnem": ...}`, the shape `layer4.producer_object` already writes, with
two kinds added for the two new blocks.  No artifact this line writes
declares `role: generator provenance`; the unmodified guard walks
every one of them in full.

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

No operator token appears in this file as a key, a grouping or a row
structure.  Every mnemonic this file records sits under `mnem`, which
is this codebase's ratified machine-form field.

Coding discipline: no compound one-liner statements.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import ledger47 as L47                                           # noqa: E402
import region36 as R36                                           # noqa: E402

# ------------------------------------------------------------------
# IMPORTED UNCHANGED from ledger47 (named, so a reader can see exactly
# what did not change)
# ------------------------------------------------------------------
Refusal = L47.Refusal
split_lines = L47.split_lines
operands_of = L47.operands_of
mnemonic_of = L47.mnemonic_of
family_of_operand = L47.family_of_operand
is_vector_family = L47.is_vector_family
register_text = L47.register_text
pick_scratch = L47.pick_scratch
align_up = L47.align_up
weave = L47.weave
immediate_value = L47.immediate_value
PURE_WRITE_MNEMONICS = L47.PURE_WRITE_MNEMONICS
FLAG_SETTER_STEMS = L47.FLAG_SETTER_STEMS
sets_the_flags = L47.sets_the_flags
flag_setter_stem = L47.flag_setter_stem
SCRATCH_POOL = L47.SCRATCH_POOL
LEDGER_SYMBOL = L47.LEDGER_SYMBOL
LEDGER_ENTRY_SIZE = L47.LEDGER_ENTRY_SIZE
SETCC = L47.SETCC
CMOVCC = L47.CMOVCC

# ------------------------------------------------------------------
# RULING 2: the block order
# ------------------------------------------------------------------

BLOCK_ORDER = ("IN", "CONST", "TEMP", "OWN", "STACK", "X87", "GUARD",
               "OUT")
LEDGER_ENTRIES = len(BLOCK_ORDER)
LEDGER_BYTES = LEDGER_ENTRY_SIZE * LEDGER_ENTRIES

ROW_TEXT = re.compile(r"^(IN|CONST|TEMP|OWN|STACK|X87|GUARD|OUT)-(\d+)$")


def ledger_entry_index(block):
    return BLOCK_ORDER.index(block)


def ledger_entry_offset(block):
    return LEDGER_ENTRY_SIZE * ledger_entry_index(block)


def ledger_entry_text(block):
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
# RULING 5: the typed producer
# ------------------------------------------------------------------

NON_OPCODE_PHRASES = (
    "arrival",
    "the body's own immediate operand",
    "the body's own stack displacement",
    "the body's last write to",
    "a value the machine stack held before this unit was entered",
    "an x87 stack position this unit did not itself load",
)


def producer_object(producer):
    """THE PRODUCER, AS A TYPED MACHINE-FORM OBJECT.

    Same shape as `layer4.producer_object`: the mnemonic sits under
    `mnem`, which check_no_spelling_keys.py already carries as a
    machine-form field beside `bytes`, `key` and `sem_key`; `kind`
    comes from a fixed vocabulary that contains no operator token.

    The kinds:
      arch_opcode        one mnemonic
      flag_pair          (flag-setting opcode, flag-reading opcode)
      non_opcode_phrase  the recorded phrases that are not opcodes
    """
    if isinstance(producer, dict):
        return producer
    if isinstance(producer, list):
        return {
            "kind": "flag_pair",
            "mnem": [str(one) for one in producer],
        }
    text = str(producer)
    for phrase in NON_OPCODE_PHRASES:
        if text.startswith(phrase):
            return {"kind": "non_opcode_phrase", "phrase": text}
    return {"kind": "arch_opcode", "mnem": text}


def opcode_producer(mnemonic, role=None):
    out = {"kind": "arch_opcode", "mnem": str(mnemonic)}
    if role is not None:
        out["writes_which_half"] = role
    return out


# ------------------------------------------------------------------
# RULING 3: the per-opcode destination table
# ------------------------------------------------------------------
#
# ACCUMULATOR is the %rax family; DATA REGISTER is the %rdx family.
# The table is read by stem: one operand-size suffix is removed before
# the lookup, exactly as ledger47's flag-setter test does, so `idivl`
# and `idivq` are both `idiv`.
#
# `writes` is a list of (register family, what that half is), in the
# order the rows are made.  `reads_implicitly` is the list of register
# families the opcode reads without naming them.  `named_operands_are`
# says how to read the operands the opcode DOES spell.

ACCUMULATOR = "rax"
DATA_REGISTER = "rdx"

DESTINATION_RULES = {
    "idiv": {
        "writes": [(ACCUMULATOR, "quotient"),
                   (DATA_REGISTER, "remainder")],
        "reads_implicitly": [ACCUMULATOR, DATA_REGISTER],
        "named_operands_are": "all read",
        "only_when_operand_count_is": None,
        "why": "this opcode divides the value held in the data "
               "register and the accumulator together by the operand "
               "it names, and leaves the quotient in the accumulator "
               "and the remainder in the data register; it names "
               "neither destination",
    },
    "div": {
        "writes": [(ACCUMULATOR, "quotient"),
                   (DATA_REGISTER, "remainder")],
        "reads_implicitly": [ACCUMULATOR, DATA_REGISTER],
        "named_operands_are": "all read",
        "only_when_operand_count_is": None,
        "why": "as idiv, without the sign",
    },
    "mul": {
        "writes": [(ACCUMULATOR, "low half"),
                   (DATA_REGISTER, "high half")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 1,
        "why": "the one-operand form multiplies the accumulator by "
               "the operand it names and leaves the low half in the "
               "accumulator and the high half in the data register",
    },
    "imul": {
        "writes": [(ACCUMULATOR, "low half"),
                   (DATA_REGISTER, "high half")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 1,
        "why": "the ONE-OPERAND form only: the two- and three-operand "
               "forms name their destination and are left to the "
               "ordinary rule",
    },
    "cltd": {
        "writes": [(DATA_REGISTER, "the sign of the accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "spreads the sign of the accumulator's low 32 bits "
               "through the data register; it names no operand at "
               "all, so ledger47's walk skipped it entirely",
    },
    "cqto": {
        "writes": [(DATA_REGISTER, "the sign of the accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "as cltd, at 64 bits",
    },
    "cwtl": {
        "writes": [(ACCUMULATOR, "the widened accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "widens the accumulator's low 16 bits to 32, in place",
    },
    "cltq": {
        "writes": [(ACCUMULATOR, "the widened accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "widens the accumulator's low 32 bits to 64, in place",
    },
    "cbtw": {
        "writes": [(ACCUMULATOR, "the widened accumulator")],
        "reads_implicitly": [ACCUMULATOR],
        "named_operands_are": "all read",
        "only_when_operand_count_is": 0,
        "why": "widens the accumulator's low 8 bits to 16, in place",
    },
}

SIZE_SUFFIX = ("b", "w", "l", "q")


def destination_rule(mnemonic, operand_count):
    """the table row for `mnemonic`, or None when the ordinary rule
    ('the destination is the last named operand') applies."""
    stem = mnemonic
    if stem not in DESTINATION_RULES:
        if len(mnemonic) > 3:
            if mnemonic[-1] in SIZE_SUFFIX:
                stem = mnemonic[:-1]
    rule = DESTINATION_RULES.get(stem)
    if rule is None:
        return None, None
    wanted = rule["only_when_operand_count_is"]
    if wanted is not None:
        if operand_count != wanted:
            return None, None
    return stem, rule


# ------------------------------------------------------------------
# RULING 3: comparisons write flags, not registers
# ------------------------------------------------------------------

COMPARISON_STEMS = frozenset([
    "cmp", "test",
    "ucomiss", "ucomisd", "comiss", "comisd",
    "vucomiss", "vucomisd", "vcomiss", "vcomisd",
    "ptest", "vptest",
    "bt",
    "fucomi", "fucomip", "fcomi", "fcomip",
    "fucom", "fucomp", "fcom", "fcomp", "ftst",
])


def comparison_stem(mnemonic):
    if mnemonic in COMPARISON_STEMS:
        return mnemonic
    if len(mnemonic) > 2:
        if mnemonic[-1] in SIZE_SUFFIX:
            stem = mnemonic[:-1]
            if stem in COMPARISON_STEMS:
                return stem
    return None


# ------------------------------------------------------------------
# RULING 3: an unconditional transfer is not a flag reader
# ------------------------------------------------------------------

JCC = re.compile(r"^j[a-z]+$")
UNCONDITIONAL_TRANSFERS = frozenset(["jmp", "jmpq"])


def is_flag_reading_transfer(mnemonic):
    if JCC.match(mnemonic) is None:
        return False
    if mnemonic in UNCONDITIONAL_TRANSFERS:
        return False
    return True


# ------------------------------------------------------------------
# RULING 2: the machine stack
# ------------------------------------------------------------------

PUSH_STEMS = frozenset(["push", "pushq", "pushl", "pushw"])
POP_STEMS = frozenset(["pop", "popq", "popl", "popw"])


# ------------------------------------------------------------------
# RULING 2: the x87 register stack
# ------------------------------------------------------------------
#
# A mnemonic is reduced to its BASE by removing operand-size letters
# from the end until a base this file knows is left (`fldt` -> `fld`,
# `fildll` -> `fild`, `fstpt` -> `fstp`, `fisubrs` -> `fisubr`).

X87_LOADS = frozenset(["fld", "fild", "fldz", "fld1", "fldpi",
                       "fldl2e", "fldl2t", "fldlg2", "fldln2"])
X87_STORES_POP = frozenset(["fstp", "fistp", "fisttp"])
X87_STORES_KEEP = frozenset(["fst", "fist"])
X87_ARITH_POP = frozenset(["faddp", "fsubp", "fsubrp", "fmulp",
                           "fdivp", "fdivrp"])
X87_ARITH_KEEP = frozenset(["fadd", "fsub", "fsubr", "fmul", "fdiv",
                            "fdivr",
                            "fiadd", "fisub", "fisubr", "fimul",
                            "fidiv", "fidivr"])
X87_ONE_PLACE = frozenset(["fchs", "fabs", "fsqrt", "frndint", "f2xm1",
                           "fcos", "fsin", "fptan", "fyl2x"])
X87_EXCHANGE = frozenset(["fxch"])
X87_COMPARE_POP = frozenset(["fucomip", "fcomip", "fucomp", "fcomp"])
X87_COMPARE_KEEP = frozenset(["fucomi", "fcomi", "fucom", "fcom",
                              "ftst"])

X87_BASES = (X87_LOADS | X87_STORES_POP | X87_STORES_KEEP
             | X87_ARITH_POP | X87_ARITH_KEEP | X87_ONE_PLACE
             | X87_EXCHANGE | X87_COMPARE_POP | X87_COMPARE_KEEP)

X87_SIZE_LETTERS = ("s", "l", "t", "q", "b", "w")

X87_POSITION = re.compile(r"^%st(?:\((\d)\))?$")


def x87_base(mnemonic):
    """the base form of an x87 mnemonic, or None when this is not one."""
    if not mnemonic.startswith("f"):
        return None
    text = mnemonic
    while True:
        if text in X87_BASES:
            return text
        if len(text) <= 3:
            return None
        if text[-1] not in X87_SIZE_LETTERS:
            return None
        text = text[:-1]


def x87_position_of(operand):
    """the x87 stack position an operand names: 0 for `%st` and
    `%st(0)`, N for `%st(N)`; None when the operand is not one."""
    hit = X87_POSITION.match(operand)
    if hit is None:
        return None
    if hit.group(1) is None:
        return 0
    return int(hit.group(1))


X87_POSITIONS = 8


# ------------------------------------------------------------------
# RULING 4: positional branch labels
# ------------------------------------------------------------------

TRANSFER_TARGET = re.compile(r"^([0-9a-f]+)\s*(?:<([^>]*)>)?$")
INNER_OFFSET = re.compile(r"\+0x([0-9a-f]+)$")
EXTERNAL_NAME = re.compile(r"[^A-Za-z0-9_]")
TRANSFER_MNEMONIC = re.compile(r"^(j[a-z]+|call|callq|loop[a-z]*)$")


def is_transfer(mnemonic):
    return TRANSFER_MNEMONIC.match(mnemonic) is not None


def external_symbol(inner):
    """the callee's own name, as an assembler identifier.  The address
    and the angle brackets go; the callee stays, because a call to one
    runtime routine is not a call to another and the ruling is about
    the unit's OWN name appearing in its own text."""
    head = inner.split("@")[0]
    head = head.split("+")[0]
    head = head.split("-")[0]
    return "x_" + EXTERNAL_NAME.sub("_", head)


def instruction_offsets(byte_text):
    """the byte offset of every instruction, read off the unit's own
    bytes with capstone; None when the bytes are not available."""
    if not byte_text:
        return None
    try:
        import capstone
    except ImportError:
        return None
    cleaned = byte_text.replace(" ", "").replace("\n", "")
    try:
        blob = bytes.fromhex(cleaned)
    except ValueError:
        return None
    engine = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    offsets = []
    for instruction in engine.disasm(blob, 0):
        offsets.append(instruction.address)
    return offsets


def split_off_annotation(line):
    """(the instruction text, the trailing `!!...` annotation or '')."""
    if "!!" not in line:
        return line, ""
    head, tail = line.split("!!", 1)
    return head.strip(), "!!" + tail


def reloc_callee(annotation):
    """the callee named in a `!!reloc=R_X86_64_PLT32:NAME-0x4`
    annotation, or None."""
    if "reloc=" not in annotation:
        return None
    piece = annotation.split("reloc=", 1)[1]
    if ":" not in piece:
        return None
    name = piece.split(":", 1)[1]
    name = name.split("-")[0]
    name = name.split("+")[0]
    name = name.strip()
    if not name:
        return None
    return name


def positional_labels(body_lines, byte_text):
    """RULING 4, applied to one body.

    Returns (new_body_lines, record).  `record` names every rewrite,
    every label defined and every transfer this file could not place,
    so nothing is silently changed.
    """
    offsets = instruction_offsets(byte_text)
    by_offset = {}
    if offsets is not None:
        if len(offsets) == len(body_lines):
            for index, offset in enumerate(offsets):
                by_offset[offset] = index
    found = []
    for index, raw in enumerate(body_lines):
        text, annotation = split_off_annotation(raw)
        parts = text.split(" ", 1)
        if len(parts) != 2:
            continue
        mnemonic = parts[0]
        if not is_transfer(mnemonic):
            continue
        hit = TRANSFER_TARGET.match(parts[1].strip())
        if hit is None:
            continue
        address = int(hit.group(1), 16)
        inner = hit.group(2)
        inside = None
        if inner is not None:
            offset_hit = INNER_OFFSET.search(inner)
            if offset_hit is not None:
                candidate = int(offset_hit.group(1), 16)
                if candidate in by_offset:
                    inside = candidate
        if inside is None:
            if address in by_offset:
                inside = address
        found.append({
            "line_index": index,
            "mnem": mnemonic,
            "address": address,
            "inner": inner,
            "inside_at_offset": inside,
            "annotation": annotation,
        })
    inside_targets = []
    for entry in found:
        if entry["inside_at_offset"] is None:
            continue
        if entry["inside_at_offset"] in inside_targets:
            continue
        inside_targets.append(entry["inside_at_offset"])
    inside_targets.sort()
    label_of_offset = {}
    for rank, offset in enumerate(inside_targets):
        label_of_offset[offset] = "L%d" % rank
    outside_addresses = []
    for entry in found:
        if entry["inside_at_offset"] is not None:
            continue
        if entry["address"] in outside_addresses:
            continue
        outside_addresses.append(entry["address"])
    outside_addresses.sort()
    label_of_outside = {}
    for rank, address in enumerate(outside_addresses):
        label_of_outside[address] = "L%d" % (len(inside_targets) + rank)

    rewrites = []
    replaced = {}
    for entry in found:
        text, annotation = split_off_annotation(body_lines[
            entry["line_index"]])
        was = text
        if entry["inside_at_offset"] is not None:
            label = label_of_offset[entry["inside_at_offset"]]
            now = "%s %s" % (entry["mnem"], label)
            how = "a transfer to an instruction inside this unit"
        else:
            callee = None
            if entry["annotation"]:
                callee = reloc_callee(entry["annotation"])
            if callee is None:
                if entry["inner"]:
                    callee = entry["inner"]
            if callee is None:
                label = label_of_outside[entry["address"]]
                now = "%s %s" % (entry["mnem"], label)
                how = ("a transfer this file could not place: neither "
                       "the bytes nor a symbol comment says where it "
                       "goes, so the target is a positional label and "
                       "the address is dropped")
            else:
                now = "%s %s" % (entry["mnem"], external_symbol(callee))
                how = "a transfer out of this unit, to a named callee"
        if annotation:
            now = "%s %s" % (now, annotation)
        replaced[entry["line_index"]] = now
        rewrites.append({
            "line_index": entry["line_index"],
            "was": was,
            "now": now,
            "how": how,
        })

    out = []
    label_lines = []
    for index, raw in enumerate(body_lines):
        offset_here = None
        if offsets is not None:
            if len(offsets) == len(body_lines):
                offset_here = offsets[index]
        if offset_here is not None:
            if offset_here in label_of_offset:
                name = label_of_offset[offset_here]
                out.append("%s:" % name)
                label_lines.append({"label": name,
                                    "before_line_index": index})
        if index in replaced:
            out.append(replaced[index])
            continue
        out.append(raw)
    record = {
        "transfers_seen": len(found),
        "labels_defined": label_lines,
        "rewrites": rewrites,
        "bytes_were_read": offsets is not None and len(by_offset) > 0,
        "how": "targets inside the unit become L0.. in address order "
               "and the label is defined on the instruction it names; "
               "a transfer out of the unit keeps its callee and loses "
               "its address; the objdump symbol comment is dropped "
               "either way",
    }
    return out, record


# ------------------------------------------------------------------
# the ledger table
# ------------------------------------------------------------------

class LedgerTable(object):
    """the provenance ledger of one unit, over the eight blocks."""

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
            "produced_by": producer_object(produced_by),
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
# the wrapper's prelude and epilogue -- ledger47's, with this file's
# block offsets
# ------------------------------------------------------------------

def build_prelude(arrival_families, table):
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
        row = table.add("IN", size, type_name, "arrival", [],
                        note="the runner fills this row before the "
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


# ------------------------------------------------------------------
# THE DATAFLOW WALK, with rulings 2 and 3 in it
# ------------------------------------------------------------------

def walk_dataflow(body, table, arrival_rows, arrival_families):
    """emit a row for every value the body produces.

    Returns (where, notes).  `where` maps a register family to the row
    holding its current value; `notes` records every place the walk
    could not model, by name.
    """
    where = {}
    for index, family in enumerate(arrival_families):
        where[family] = arrival_rows[index]["row"]
    literals = {}
    own = {}
    stack = []                     # the machine stack, newest first
    x87 = []                       # the x87 stack, position 0 first
    last_flag_setter = None
    last_flag_row = None
    notes = []

    def read_operand_rows(operands, mnemonic, treat_last_as_read):
        """the rows this line READS, in operand order."""
        rows_read = []
        for position, operand in enumerate(operands):
            value = immediate_value(operand)
            if value is not None:
                if operand not in literals:
                    made = table.add(
                        "CONST", 8, "literal",
                        "the body's own immediate operand", [],
                        note="not materialized: the body is kept "
                             "verbatim, so the literal stays an "
                             "immediate in the text")
                    made["value_at_run"] = value
                    literals[operand] = made["row"]
                rows_read.append(literals[operand])
                continue
            if x87_position_of(operand) is not None:
                continue
            if operand.startswith("%"):
                family = family_of_operand(operand)
                if family is None:
                    continue
                is_last = position == len(operands) - 1
                if is_last:
                    if not treat_last_as_read:
                        if mnemonic in PURE_WRITE_MNEMONICS:
                            continue
                if family in where:
                    rows_read.append(where[family])
                continue
            for token in re.findall(r"%[a-z0-9]+", operand):
                family = canon.FAMILY_OF.get(token[1:])
                if family is None:
                    continue
                if family in where:
                    rows_read.append(where[family])
            for hit in R36.RSP_DISP.finditer(operand):
                displacement = int(hit.group(1), 16)
                key = "-0x%x(%%rsp)" % displacement
                if key not in own:
                    made = table.add(
                        "OWN", 8, "the unit's own stack address",
                        "the body's own stack displacement", [],
                        note="the body is kept verbatim, so this row "
                             "records the address the body itself "
                             "spells: %%rsp - 0x%x" % displacement)
                    made["displacement"] = displacement
                    made["address_is"] = "%%rsp - 0x%x" % displacement
                    own[key] = made["row"]
                rows_read.append(own[key])
        return rows_read

    def x87_row_at(position, mnemonic):
        """the row at x87 stack position `position`, made on demand."""
        while len(x87) <= position:
            made = table.add(
                "X87", 16, "x87 stack value",
                "an x87 stack position this unit did not itself load",
                [],
                note="the body reads x87 stack position %d without "
                     "having loaded it inside this body, so the row "
                     "stands for what was there when the unit was "
                     "entered" % len(x87),
                resident="x87 stack position %d" % len(x87))
            made["x87_position"] = len(x87)
            x87.append(made["row"])
            notes.append({
                "row_producer_hole": mnemonic,
                "why": "an x87 stack position was read before this "
                       "body loaded it; the row records that it came "
                       "from outside the body",
            })
        return x87[position]

    for raw in body:
        line = R36.strip_annotation(raw)
        if line.endswith(":"):
            continue
        if line == "ret":
            continue
        mnemonic = mnemonic_of(line)
        operands = operands_of(line)

        # -------------------------------------------------- x87
        base = x87_base(mnemonic)
        if base is not None:
            named = []
            for operand in operands:
                position = x87_position_of(operand)
                if position is not None:
                    named.append(position)
            memory_rows = read_operand_rows(operands, mnemonic, True)
            if base in X87_LOADS:
                made = table.add(
                    "X87", 16, "x87 stack value",
                    opcode_producer(mnemonic), memory_rows,
                    note="this opcode pushed a value onto the x87 "
                         "register stack; it becomes position 0 and "
                         "every other position moves down one",
                    resident="x87 stack position 0")
                made["x87_position"] = 0
                x87.insert(0, made["row"])
                if len(x87) > X87_POSITIONS:
                    notes.append({
                        "row_producer_hole": mnemonic,
                        "why": "the x87 register stack has eight "
                               "positions and this body pushed past "
                               "the eighth",
                    })
                continue
            if base in X87_STORES_POP or base in X87_STORES_KEEP:
                top = x87_row_at(0, mnemonic)
                destination = operands[-1] if operands else None
                if destination is not None:
                    family = family_of_operand(destination)
                    if family is not None:
                        if family not in canon.NEVER_RENAME:
                            where[family] = top
                if base in X87_STORES_POP:
                    if x87:
                        x87.pop(0)
                continue
            if base in X87_COMPARE_POP or base in X87_COMPARE_KEEP:
                sides = []
                if named:
                    for position in named:
                        sides.append(x87_row_at(position, mnemonic))
                else:
                    sides.append(x87_row_at(0, mnemonic))
                made = table.add(
                    "TEMP", 8, "flags only",
                    opcode_producer(mnemonic), sides + memory_rows,
                    note="a comparison writes the flags and no "
                         "register: this row is the flag state the "
                         "next flag-reading opcode picks up")
                last_flag_setter = mnemonic
                last_flag_row = made["row"]
                if base in X87_COMPARE_POP:
                    if x87:
                        x87.pop(0)
                continue
            if base in X87_EXCHANGE:
                other = 1
                if named:
                    other = named[0]
                if other == 0:
                    continue
                x87_row_at(other, mnemonic)
                first = x87[0]
                x87[0] = x87[other]
                x87[other] = first
                continue
            # arithmetic, and the one-place forms
            sides = []
            for position in named:
                sides.append(x87_row_at(position, mnemonic))
            if not sides:
                sides.append(x87_row_at(0, mnemonic))
            made = table.add(
                "X87", 16, "x87 stack value",
                opcode_producer(mnemonic), sides + memory_rows,
                note="this opcode wrote an x87 stack position",
                resident="an x87 stack position")
            destination_position = 0
            if base in X87_ARITH_POP:
                destination_position = 1
                if named:
                    destination_position = named[-1]
            elif named:
                destination_position = named[-1]
            x87_row_at(destination_position, mnemonic)
            made["x87_position"] = destination_position
            x87[destination_position] = made["row"]
            if base in X87_ARITH_POP:
                if x87:
                    x87.pop(0)
            continue

        # -------------------------------------------------- the stack
        if mnemonic in PUSH_STEMS:
            read_rows = read_operand_rows(operands, mnemonic, True)
            made = table.add(
                "STACK", 8, "8-byte value on the machine stack",
                opcode_producer(mnemonic), read_rows,
                note="this opcode moved a value onto the machine "
                     "stack; the row holds the value it moved",
                resident="the machine stack, newest entry")
            stack.insert(0, made["row"])
            continue
        if mnemonic in POP_STEMS:
            if stack:
                taken = stack.pop(0)
            else:
                made = table.add(
                    "STACK", 8, "8-byte value on the machine stack",
                    "a value the machine stack held before this unit "
                    "was entered", [],
                    note="this opcode took a value off the machine "
                         "stack that no opcode in this body put "
                         "there",
                    resident="the machine stack, before entry")
                taken = made["row"]
            destination = operands[-1] if operands else None
            if destination is not None:
                family = family_of_operand(destination)
                if family is not None:
                    where[family] = taken
            continue

        # ------------------------------------ the destination table
        stem, rule = destination_rule(mnemonic, len(operands))
        if rule is not None:
            read_rows = read_operand_rows(operands, mnemonic, True)
            implicit = []
            for family in rule["reads_implicitly"]:
                if family in where:
                    implicit.append(where[family])
            all_read = implicit + read_rows
            made_rows = []
            for family, half in rule["writes"]:
                made = table.add(
                    "TEMP", 8, "8-byte general value",
                    opcode_producer(mnemonic, half), all_read,
                    note="the per-opcode destination rule: %s"
                         % rule["why"],
                    resident="register %%%s" % family)
                made["written_half"] = half
                made_rows.append((family, made))
            for family, made in made_rows:
                where[family] = made["row"]
            if sets_the_flags(mnemonic):
                last_flag_setter = mnemonic
                last_flag_row = made_rows[0][1]["row"]
            continue

        # ------------------------------------------- comparisons
        if comparison_stem(mnemonic) is not None:
            read_rows = read_operand_rows(operands, mnemonic, True)
            made = table.add(
                "TEMP", 8, "flags only",
                opcode_producer(mnemonic), read_rows,
                note="a comparison writes the flags and no register: "
                     "this row is the flag state the next "
                     "flag-reading opcode picks up, and the "
                     "destination operand keeps the value it had")
            last_flag_setter = mnemonic
            last_flag_row = made["row"]
            continue

        # ------------------------------------------- flag readers
        read_rows = read_operand_rows(operands, mnemonic, False)
        flag_reader = None
        if SETCC.match(mnemonic):
            flag_reader = mnemonic
        if CMOVCC.match(mnemonic):
            flag_reader = mnemonic
        if is_flag_reading_transfer(mnemonic):
            flag_reader = mnemonic
        if flag_reader is not None:
            producer = [last_flag_setter, flag_reader]
            operands_of_row = list(read_rows)
            if last_flag_row is not None:
                operands_of_row = [last_flag_row] + operands_of_row
            if last_flag_setter is None:
                notes.append({
                    "row_producer_hole": flag_reader,
                    "why": "no flag-setting arch opcode precedes this "
                           "flag-reading opcode in the body, so the "
                           "pair the ledger records is incomplete",
                })
            made = table.add("GUARD", 8, "flag-derived value", producer,
                             operands_of_row,
                             note="the producer is the pair "
                                  "(flag-setting opcode, flag-reading "
                                  "opcode), and the first operand is "
                                  "the row holding the flag state that "
                                  "pair reads")
            if JCC.match(mnemonic):
                continue
            destination = operands[-1] if operands else None
            if destination is not None:
                family = family_of_operand(destination)
                if family is not None:
                    where[family] = made["row"]
            continue

        if mnemonic in UNCONDITIONAL_TRANSFERS:
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
        if size == 16:
            type_name = "16-byte vector value"
        else:
            type_name = "8-byte general value"
        made = table.add("TEMP", size, type_name,
                         opcode_producer(mnemonic), read_rows,
                         resident="register %%%s" % family)
        where[family] = made["row"]
        if sets_the_flags(mnemonic):
            last_flag_setter = mnemonic
            last_flag_row = made["row"]
    return where, notes


# ------------------------------------------------------------------
# the whole render for one unit
# ------------------------------------------------------------------

def wrap_unit(body_text, arrival_families, result_family, result_width,
              body_bytes=None):
    """(fields).  As ledger47.wrap_unit, with ruling 4 applied to the
    body before anything else and rulings 2/3/5 inside the walk."""
    if not body_text:
        raise Refusal("no text",
                      "no text exists for this unit, so there is no "
                      "body to wrap")
    body_as_read = split_lines(body_text)
    for raw in body_as_read:
        line = R36.strip_annotation(raw)
        if LEDGER_SYMBOL in line:
            raise Refusal(
                "the body names the ledger symbol",
                "the body spells %r, which would collide with the "
                "form's own symbol" % LEDGER_SYMBOL)
    body, label_record = positional_labels(body_as_read, body_bytes)
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
        "body_as_read": list(body_as_read),
        "branch_labels": label_record,
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
        "form": "ledger48",
        "addressing": "two steps: read the block's base out of the "
                      "ledger at an absolute address (rip-relative), "
                      "then read the row inside that block",
    }
    return fields
