#!/usr/bin/env python3
"""model_table.py -- tasks m1 and m1b: THE ARCH-OPCODE MODEL TABLE.

WHAT TASK m1b CHANGED, 2026-09-08, in one paragraph, because the join
this program writes was wrong in three mechanical ways and the fourth
population was missing. (1) The JOIN is now keyed by `key_width`, the
operation's own lane width from the reference's own tables, computed by
one function called on both sides -- section 0 -- because the corpus
said `addss xmm_xmm 128` where the sweep said 8, 16, 32 and 64 and the
operation's width is 32. (2) FLAG CONSUMERS are attested: a ledger row
whose producer is the pair (flag-setting opcode, flag-reading opcode)
now attests the READING half, with the setter recorded on the cell.
(3) The x87 register stack has operand classes here and three operand
shapes in `model_translate.shapes_for` (`st_st`, `st_one`, `st_none`),
so `faddp %st,%st(1)` has a shape to be classified into. (4) Control
transfers are counted as what they are -- attested by the ledger's
GUARD rows, never by value cells -- and the coverage table, one row per
corpus mnemonic in exactly one of four categories, is the acceptance
criterion.

Node: hq.research.arch_unit_oracle
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/
node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`, the "goal"
section of 2026-09-07 and the ruling of 2026-09-08).

WHAT THIS PROGRAM WRITES, one sentence, in relation. `reference.py`'s
`opcode_table` holds one entry per arch mnemonic, and each entry's
BUILDER turns operand texts plus a machine state into the z3 term the
opcode writes to each place; this program runs every builder over every
operand shape the sweep in `lean/model_translate.py` spells, prints each
resulting term by the pipeline's own layer-5 rule, sets the corpus's own
attestation beside each (mnem, operand shape, width), and REPORTS which
rows compute the same mapping -- it never merges them.

THE KEY IS THE TRIPLE (the owner, 2026-09-08). A mnemonic alone is a spelling;
(mnemonic, operand form, width) is machine form, because the instruction
bytes and the ISA fix it and the reference's builders are that
determination. The mnemonic sits in the field `mnem`, which the guard
`op_pipeline/check_no_spelling_keys.py` already reads as a machine form,
because `mnem` is one of its `PROSE_FIELDS`. Nothing is asked of the
guard and the guard is not touched.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections, type
pairs) or from ratified intention -- never from the token. The token
appears exactly once per unit: as a display label on the member. HISTORY
OF VIOLATIONS, so the pattern is visible: (1) the arch campaign's
cross-language matrix (caught by the owner 2026-08-24); (2) verdicts.py's row
pairing (caught by the owner 2026-08-25 -- the fix brief itself reintroduced it
as "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
stage that groups or pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure. A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

Every edge this program writes is keyed by ROW IDS. The candidate set for
a comparison is (a) the rows that share an operand shape and a width --
machine-form evidence -- or (b) the pairs of entries the reference
registers with the SAME BUILDER OBJECT, `entry.build is other.build`,
which is a fact about the table's own function objects and not about any
token.

MEMORY BOUND: 16 GB resident, inside the m1 instance's 20g; named abort
ABORT_MEMORY_M1 (`resource.getrusage`), checked after every mnemonic in
the sweep and after every shard in the attestation stream. The canon40
shards (332 files, 259 MB) are streamed one at a time and dropped.

Coding discipline: no compound one-liner statements.

usage:
  model_table.py sweep      the builders over every shape -> model_table_rows.json
  model_table.py attest     the corpus's ledger rows      -> model_table_attest.json
  model_table.py edges      the reported equivalences     -> model_table_edges.json
  model_table.py edges --sample N   the same, over the first N cells only
  model_table.py assemble   the three, joined and counted -> model_table.json
  model_table.py report     model_table.json              -> model_table.md
"""

# THE JSON FIELD NAMES, and why each is what it is. The guard
# `check_no_spelling_keys.py` fails a bare operator token wherever it is
# a key, a list element, or a string value on a structure field, and
# `and`, `or`, `xor` and `not` are all three: arch mnemonics AND operator
# spellings in the probe manifests' inventory. So every field of this
# program's json that CARRIES a mnemonic is named `mnem`, which the guard
# already reads as a machine form, `mnem` being one of its `PROSE_FIELDS`
# -- the ruling of 2026-09-08, and nothing asked of the guard here. A
# list of mnemonics is a list of records each carrying `mnem`, never a
# list of bare strings. The sweep's own `cause` string is
# carried as `reason`, and a printed term as `text`, because those two
# field names are in the guard's `PROSE_FIELDS` and a free-text sentence
# is not a key.

import collections
import hashlib
import inspect
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ARCH_OPCODES = os.path.normpath(os.path.join(HERE, ".."))
OP = os.path.normpath(os.path.join(HERE, "..", "..", "..", "op_pipeline"))
LEAN = os.path.join(OP, "lean")
sys.path.insert(0, OP)
sys.path.insert(0, LEAN)

import z3                                                    # noqa: E402
import canon                                                 # noqa: E402
import ledger48 as L48                                       # noqa: E402
import reference as R                                        # noqa: E402
import term as T                                             # noqa: E402
import canonical_form as CF                                  # noqa: E402
import term66_run as TR                                      # noqa: E402
import model_translate as MT                                 # noqa: E402

UNIQUE_OPCODES_JSON = os.path.join(ARCH_OPCODES,
                                   "unique_opcodes.json")
ROWS_JSON = os.path.join(HERE, "model_table_rows.json")
ATTEST_JSON = os.path.join(HERE, "model_table_attest.json")
EDGES_JSON = os.path.join(HERE, "model_table_edges.json")
OUT_JSON = os.path.join(HERE, "model_table.json")
OUT_MD = os.path.join(HERE, "model_table.md")

ABORT_MEMORY_M1_KB = 16 * 1024 * 1024

SOLVER_CEILING_MS = 3000


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    now = peak_kb()
    if now <= ABORT_MEMORY_M1_KB:
        return
    raise SystemExit("ABORT_MEMORY_M1: %d kB resident at %s (ceiling "
                     "%d kB)" % (now, where, ABORT_MEMORY_M1_KB))


def say(text):
    print(text)
    sys.stdout.flush()


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    say("   wrote %s (%.1f MB)"
        % (path, os.path.getsize(path) / (1024.0 * 1024.0)))


# ==================================================================
# section 0: THE ONE WIDTH RULE -- `key_width`
# ==================================================================
#
# WHAT `key_width` IS, one sentence: the width the JOIN is keyed by --
# the operation's own lane width, as the reference's own tables state
# it -- as against the field `width`, which stays what it always was on
# a sweep row (the loop variable the sweep walked) and on an attested
# cell (the width the operand's register name or the ledger row's byte
# size gave).
#
# WHY IT EXISTS, measured. Task m1 joined the corpus's attestation onto
# the table's rows by (mnem, shape, width), and the two sides do not
# spell `width` the same way for a vector or an x87 operand. The corpus
# says `addss xmm_xmm 128` -- 128 because the ledger row it came from
# holds sixteen bytes -- while the sweep's rows for the same mnemonic
# and shape say 8, 16, 32 and 64, the four general-register widths its
# loop walks. Neither number is the operation's width: `addss` adds ONE
# 32-bit lane. So 82 of the corpus's 219 attested cells landed on no
# row at all. This function is the one place that decides, and both
# sides call it.
#
# THE RULE, LITERAL, and where each number is read from:
#   x87 mnemonic (ledger48.x87_base names it)          -> 80
#   reference.FLOAT_BINARY                             -> its 32 / 64
#   reference.FLOAT_COMPARE_MASK                       -> its 32 / 64
#   reference.CONVERT_TO_FLOAT                         -> its 32 / 64
#   reference.LANE_MOVE                                -> its 32 / 64
#   reference.FLOAT_FLAG_ONLY                          -> 32 / 64, the
#       line `width = 32 if ops.mnemonic.endswith("ss") else 64` of
#       reference.build_float_flag_only
#   `cvtss2sd`                                         -> 64, the
#       `FLOAT_SORT[64]` of reference.build_convert_widen
#   reference.PACKED_FLOAT, BITWISE_128, WHOLE_MOVE    -> 128
#   the further whole-register vector mnemonics below  -> 128
#   reference.SIGN_EXTEND, ZERO_EXTEND (task ap2)      -> the pair's
#       DESTINATION width, the register the widening move writes
#   anything else                                      -> the width the
#       row already carries (the general-register rule, unchanged)
#
# The last two lines of the table above are this task's own extension
# of the brief's list, and it is flagged as such in the log: the brief
# named seven reference tables, and the corpus attests six more vector
# mnemonics that none of the seven holds. Each one's width is read from
# the reference the same way -- the builder's own source -- and every
# one of them is a whole-register operation.

X87_KEY_WIDTH = 80

WHOLE_REGISTER_KEY_WIDTH = 128

FURTHER_WHOLE_REGISTER = ("punpckldq", "punpcklqdq", "unpckhpd",
                          "unpcklpd", "pextrw", "pcmpeqb", "pcmpeqd",
                          "pmovmskb")
"""the vector mnemonics the brief's seven tables do not hold, each of
which reads or writes the WHOLE 128-bit register: the two unpack pairs
(`build_unpack_*` call `ops.read_128` on both operands), the word
extraction (`build_extract_word` reads `ops.read_128(1)`), and the
three the reference registers with no builder at all."""


def scalar_lane_widths():
    """every mnemonic whose operation works on ONE lane of a vector
    register, with that lane's width in bits, read from the
    reference's own tables."""
    out = {}
    for mnem in R.FLOAT_BINARY:
        out[mnem] = R.FLOAT_BINARY[mnem][1]
    for mnem in R.FLOAT_COMPARE_MASK:
        out[mnem] = R.FLOAT_COMPARE_MASK[mnem][1]
    for mnem in R.CONVERT_TO_FLOAT:
        out[mnem] = R.CONVERT_TO_FLOAT[mnem]
    for mnem in R.LANE_MOVE:
        out[mnem] = R.LANE_MOVE[mnem]
    for mnem in R.FLOAT_FLAG_ONLY:
        if mnem.endswith("ss"):
            out[mnem] = 32
        else:
            out[mnem] = 64
    out["cvtss2sd"] = 64
    return out


def whole_register_mnemonics():
    """every mnemonic whose operation is on the whole 128-bit vector
    register, read from the reference's own tables plus the six the
    brief's tables do not hold."""
    out = set()
    for mnem in R.PACKED_FLOAT:
        out.add(mnem)
    for mnem in R.BITWISE_128:
        out.add(mnem)
    for mnem in R.WHOLE_MOVE:
        out.add(mnem)
    for mnem in FURTHER_WHOLE_REGISTER:
        out.add(mnem)
    return out


SCALAR_LANE_WIDTH = scalar_lane_widths()

WHOLE_REGISTER = whole_register_mnemonics()


def zero_operand_widths():
    """every mnemonic that carries NO OPERAND AT ALL and whose width is
    therefore in the reference's own tables rather than in an operand
    text, with that width in bits.

    ADDED 2026-09-09 by task h2, whose brief authorises exactly this
    additive rule and nothing else in this file. `cqto`, `cltq`, `cltd`,
    `cwtd`, `cqo` and their like name no register: the register they
    read and the register they write are fixed by the mnemonic, and the
    reference states which. `reference.SPREAD_SIGN` gives the
    accumulator width whose sign bit the line spreads into the data
    register; `reference.ACCUMULATOR_WIDEN` gives the (source,
    destination) pair whose DESTINATION is the register the line writes.
    Both are read here, never typed."""
    out = {}
    for mnem in R.SPREAD_SIGN:
        out[mnem] = R.SPREAD_SIGN[mnem]
    for mnem in R.ACCUMULATOR_WIDEN:
        out[mnem] = R.ACCUMULATOR_WIDEN[mnem][1]
    return out


ZERO_OPERAND_WIDTH = zero_operand_widths()


def widening_move_widths():
    """every mnemonic that WIDENS one register into another, with the
    width of the register it WRITES, in bits.

    ADDED 2026-09-09 by task ap2, one more case of this same rule and
    nothing else in this file.  `movslq %eax,%rdx` names two operands
    of two different widths, so there is no single width the operand
    text gives and `classify_line` leaves the row's `width` null: task
    ap1's loop found eight such cells, six of them attested, and the
    driver could not so much as format a label for them (log_243
    section 6, 24 runs, and item 2 of its awaiting-the owner list).

    THE WIDTH OF A WIDENING MOVE IS ITS DESTINATION WIDTH, which is
    what the operation's own lane is: `movslq` reads 32 bits and the
    thing it does -- the sign extension -- happens in 64.  It is the
    same reading `ACCUMULATOR_WIDEN` above already gets (`cltq` is
    `movslq` on fixed registers, and `zero_operand_widths` takes its
    DESTINATION), so the two widening families now answer alike.

    Read from `reference.SIGN_EXTEND` and `reference.ZERO_EXTEND`, the
    builder's own tables, never typed.  An entry whose pair is None
    (`movsx`, `movzx`, whose widths are in the operand text) is left
    out, so such a row passes through to the general rule unchanged."""
    out = {}
    for table in (R.SIGN_EXTEND, R.ZERO_EXTEND):
        for mnem in table:
            pair = table[mnem]
            if pair is None:
                continue
            out[mnem] = pair[1]
    return out


WIDENING_MOVE_WIDTH = widening_move_widths()


def key_width(mnem, width):
    """THE ONE WIDTH RULE. Called on both sides of the join: on every
    sweep row and on every attested cell.

    A zero-operand mnemonic passes through unchanged here: it is not an
    x87 line, not a scalar lane and not a whole-register vector line, so
    the width `classify_line` read from `ZERO_OPERAND_WIDTH` is already
    the operation's own width."""
    if L48.x87_base(mnem) is not None:
        return X87_KEY_WIDTH
    if mnem in SCALAR_LANE_WIDTH:
        return SCALAR_LANE_WIDTH[mnem]
    if mnem in WHOLE_REGISTER:
        return WHOLE_REGISTER_KEY_WIDTH
    if mnem in WIDENING_MOVE_WIDTH:
        return WIDENING_MOVE_WIDTH[mnem]
    return width


# ==================================================================
# section 1: THE MAPPING ROWS -- one per sweep attempt that TRANSLATED
# ==================================================================
#
# The sweep is `model_translate.sweep`, imported and run, never
# re-implemented: it is the same function that wrote `model_L2.json`'s
# 62,418 rows, so this table's population is that population. What this
# section adds is the TERM: the sweep records which Lean definition a
# place got, and this program re-runs the same line to hold the z3 term
# itself and print it by the pipeline's own layer-5 rule.


def mapping_rows():
    """every sweep attempt, with the z3 term of every place a
    TRANSLATED attempt wrote."""
    holder = T.Term()
    model = MT.Model()
    say("[1/4] the sweep (model_translate.sweep), over the whole table")
    started = time.time()
    swept = MT.sweep(model)
    say("   %d attempts in %.0f s" % (len(swept), time.time() - started))
    check_memory("after the sweep")
    say("[2/4] the terms, one re-run of each TRANSLATED attempt")
    table = R.REFERENCE.opcode_table
    out = []
    total = len(swept)
    for index, attempt in enumerate(swept):
        row = row_of_attempt(holder, table, index, attempt)
        out.append(row)
        if (index + 1) % 5000 == 0 or index + 1 == total:
            say("   [%d/%d] rows built" % (index + 1, total))
            check_memory("row %d" % index)
    return out


def row_of_attempt(holder, table, index, attempt):
    """one sweep attempt as one table row.

    `row_id` is the attempt's position in the sweep's own output, which
    is a machine form (the order the table's entries and the shape list
    are walked) and is what every edge in section 3 is keyed by."""
    mnem = attempt["mnem"]
    entry = table.entries[mnem]
    row = {
        "row_id": "r%05d" % index,
        "mnem": mnem,
        "shape": attempt.get("shape"),
        "width": attempt.get("width"),
        "key_width": key_width(mnem, attempt.get("width")),
        "operands": attempt.get("operands") or [],
        "preseeded": attempt.get("preseeded", False),
        "outcome": attempt["outcome"],
    }
    setter = attempt.get("flags_in_setter")
    if setter is not None:
        row["flags_in"] = {"mnem": setter}
    if attempt.get("cause") is not None:
        row["reason"] = attempt["cause"]
    row["reads"] = list(entry.reads)
    row["writes"] = list(entry.writes)
    row["reads_the_flags"] = R.FLAGS in entry.reads
    row["writes_the_flags"] = R.FLAGS in entry.writes
    row["builder"] = builder_name(entry)
    row["condition"] = partial_region(entry)
    if attempt["outcome"] != "TRANSLATED":
        return row
    row["text"] = attempt.get("line")
    places, flags = places_of_attempt(attempt)
    if places is None:
        row["outcome"] = "TRANSLATED"
        row["reason"] = flags
        return row
    row["mapping"] = []
    for place in sorted(places):
        row["mapping"].append({
            "writes": place,
            "text": holder.normalize(places[place]),
        })
    if flags is not None:
        pair = z3.Concat(MT.as_bits(flags[1]), MT.as_bits(flags[2]))
        row["mapping"].append({
            "writes": "flags",
            "mnem": flags[0],
            "text": holder.normalize(pair),
        })
    if not row["mapping"]:
        row["reason"] = ("the sweep records this attempt TRANSLATED, "
                         "and every place it left behind was a memory "
                         "cell holding its own arrival value -- a read, "
                         "not a write")
    return row


def places_of_attempt(attempt):
    """re-run the attempt's own line on the state the sweep handed its
    builder, and return (places written -> z3 term, the flag triple)."""
    state = None
    if attempt.get("preseeded"):
        width = attempt.get("width") or 64
        state = MT.preseeded_state(width, attempt.get("flags_in_setter"))
    try:
        written, flags, state, _line = MT.run_line(
            attempt["mnem"], attempt.get("operands") or [], state)
    except Exception as problem:
        return None, ("the re-run of this attempt's own line raised "
                      "%s: %s" % (type(problem).__name__, problem))
    drop_cells_only_read(written, state)
    return written, flags


def drop_cells_only_read(written, state):
    """a memory cell the builder only READ is not a place the opcode
    writes.

    `reference.MachineState.memory_cell` puts the cell's own arrival
    symbol into `state.memory` the first time a line reads the cell, so
    `model_translate.snapshot` sees a memory entry that was not there
    before the line ran and `run_line` reports it as written.
    `run_line` already applies exactly this correction to REGISTERS
    (`state.shared_seed.get(place[4:])`); it does not apply it to
    memory. A cell whose term is character-for-character the arrival
    symbol of THAT cell held its arrival value before the line and
    holds it after, so it is dropped here. A cell that holds any other
    term -- including another place's arrival symbol, which is what a
    plain store leaves -- is kept."""
    for text in state.memory:
        place = "mem_%s" % R.mangle(text)
        if place not in written:
            continue
        seed = state.shared_seed.get(R.memory_symbol_name(text))
        if seed is None:
            continue
        if written[place].sexpr() != seed.sexpr():
            continue
        del written[place]


def builder_name(entry):
    if entry.build is None:
        return None
    return entry.build.__name__


# THE PARTIAL REGION, read from the builder's own source. A builder
# states a condition in exactly three shapes in `reference.py`: it
# REFUSES (`raise NotModeled(...)`), it MASKS a count the way the
# hardware does (`shift_mask(...)`), or it BRANCHES on a value
# (`z3.If(...)`). Every statement carrying one of those marks is quoted
# whole; a builder carrying none of them is total on bit patterns.
CONDITION_MARKS = ("raise NotModeled(", "shift_mask(", "z3.If(")

TOTAL_ON_BIT_PATTERNS = (
    "total on bit patterns: this builder's own source states no "
    "refusal, no hardware mask and no branch on an operand value")


def partial_region(entry):
    """the condition this opcode's builder states, quoted from the
    builder's own source, or the sentence that says there is none."""
    if entry.build is None:
        return "no builder: this entry states no mapping at all"
    try:
        source = inspect.getsource(entry.build)
    except Exception as problem:
        return ("the builder's source could not be read: %s: %s"
                % (type(problem).__name__, problem))
    quoted = condition_statements(source)
    if not quoted:
        return TOTAL_ON_BIT_PATTERNS
    return " || ".join(quoted)


def condition_statements(source):
    """every statement of a builder's source that carries a condition
    mark, quoted whole -- from the marked line until its parentheses
    balance."""
    lines = source.split("\n")
    out = []
    index = 0
    while index < len(lines):
        line = lines[index]
        marked = False
        for mark in CONDITION_MARKS:
            if mark in line:
                marked = True
        if not marked:
            index = index + 1
            continue
        pieces = [line.strip()]
        depth = line.count("(") - line.count(")")
        while depth > 0 and index + 1 < len(lines):
            index = index + 1
            pieces.append(lines[index].strip())
            depth = depth + lines[index].count("(")
            depth = depth - lines[index].count(")")
        out.append(" ".join(pieces))
        index = index + 1
    return out


def sweep_command():
    rows = mapping_rows()
    say("[3/4] the census of outcomes")
    census = collections.Counter()
    for row in rows:
        census[row["outcome"]] += 1
    for outcome in sorted(census):
        say("   %-32s %d" % (outcome, census[outcome]))
    say("[4/4] writing")
    document = {
        "meta": {
            "task": "m1",
            "what": "one row per sweep attempt over the reference's "
                    "opcode table; the mapping is the z3 term each "
                    "written place received, printed by term.Term."
                    "normalize (the pipeline's layer-5 rule)",
            "sweep": "model_translate.sweep, imported and run",
            "peak_kb": peak_kb(),
        },
        "rows": rows,
    }
    write_json(ROWS_JSON, document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 2: THE CORPUS'S ATTESTATION
# ==================================================================
#
# One stream over the canon40 shards. The reading of a shard, a unit
# record and a ledger row is copied from `signatures/ledger_signatures
# .py`'s `census_pass` -- `document["units"]`, `record["ledger"]`,
# `row["produced_by"]["kind"] == "arch_opcode"`, `row["produced_by"]
# ["mnem"]`, per-unit deduplication as it streams, at most three example
# unit ids kept per cell. The HOLDER logic of that census is not copied:
# this task's cell is the sweep's own (shape, width), not a signature.
#
# A ledger row does not carry the instruction's operand texts, so the
# body line that made the row is read with `term.relink`, which re-walks
# the body only to learn which line made which row and CHECKS the re-walk
# against the stored ledger.


GPR_WIDTH_OF_NAME = {}


def _install_gpr_widths():
    """every general register spelling the pipeline's own tables name,
    with its width in bits. Built from `canon.WIDTH_OF` and
    `reference.WIDTH_BITS`, plus `reference.HIGH_BYTE_OF` for the four
    high-byte spellings -- never typed here."""
    for name in canon.WIDTH_OF:
        if name in R.XMM_NAMES:
            continue
        code = canon.WIDTH_OF[name]
        GPR_WIDTH_OF_NAME["%" + name] = R.WIDTH_BITS[code]
    for name in R.HIGH_BYTE_OF:
        GPR_WIDTH_OF_NAME["%" + name] = 8


def operand_texts(line):
    """the operand texts of one body line, in the arch text's own order,
    splitting on commas that are NOT inside parentheses."""
    pieces = line.split(None, 1)
    if len(pieces) < 2:
        return []
    rest = pieces[1].strip()
    out = []
    depth = 0
    current = []
    for character in rest:
        if character == "(":
            depth = depth + 1
        if character == ")":
            depth = depth - 1
        if character == "," and depth == 0:
            out.append("".join(current).strip())
            current = []
            continue
        current.append(character)
    tail = "".join(current).strip()
    if tail:
        out.append(tail)
    return out


def operand_class(text, index, count):
    """one operand text as the sweep's own operand kind, with its width
    where a register name gives one.

    THE CLASSIFIER, LITERAL. `$...` is an immediate; `%cl` is the count
    register the shift shapes name, but ONLY where it is the FIRST of
    several operands, which is the only position the sweep's `cl_gpr`
    and `cl_gpr_gpr` shapes spell it in -- `%cl` written last is the
    destination register, an ordinary 8-bit general register; a `%xmm*`
    name is a vector register; `%st` and `%st(N)` are x87
    register-stack positions, read by the pipeline's own
    `ledger48.x87_position_of`; any other `%name` the pipeline's own
    register table knows is a general register at that table's width;
    anything carrying `(` is a memory reference, and one whose
    parentheses hold a comma is the indexed form the sweep calls
    `lea_mem`."""
    if text.startswith("$"):
        return "imm", None
    if text == "%cl" and index == 0 and count > 1:
        return "cl", 8
    if text.startswith("%xmm"):
        return "xmm", None
    if L48.x87_position_of(text) is not None:
        return "st", None
    if text.startswith("%"):
        width = GPR_WIDTH_OF_NAME.get(text)
        if width is None:
            return None, None
        return "gpr", width
    if "(" in text:
        inside = text[text.find("("):]
        if "," in inside:
            return "index_mem", None
        return "mem", None
    return None, None


SHAPE_OF_CLASSES = {
    ("gpr", "gpr"): "gpr_gpr",
    ("imm", "gpr"): "imm_gpr",
    ("cl", "gpr"): "cl_gpr",
    ("mem", "gpr"): "mem_gpr",
    ("gpr", "mem"): "gpr_mem",
    ("index_mem", "gpr"): "lea_mem",
    ("xmm", "xmm"): "xmm_xmm",
    ("gpr", "xmm"): "gpr_xmm",
    ("xmm", "gpr"): "xmm_gpr",
    ("mem", "xmm"): "mem_xmm",
    ("xmm", "mem"): "xmm_mem",
    ("index_mem", "xmm"): "mem_xmm",
    ("gpr",): "gpr_one",
    ("mem",): "mem_one",
    ("index_mem",): "mem_one",
    ("imm", "gpr", "gpr"): "imm_gpr_gpr",
    ("cl", "gpr", "gpr"): "cl_gpr_gpr",
    ("imm", "xmm", "gpr"): "imm_xmm_gpr",
    ("imm", "gpr", "xmm"): "imm_gpr_xmm",
    ("st", "st"): "st_st",
    ("st",): "st_one",
    (): "none",
}

ST_SHAPES = ("st_st", "st_one", "st_none")
"""the three operand shapes task m1b added to `model_translate.
shapes_for`. They carry NO width of their own: an x87 register is 80
bits whatever the sweep's loop variable says, and `key_width` gives
every x87 row 80 on both sides of the join."""

SAME_OPERAND_SHAPE = {
    "gpr_gpr": "gpr_same",
    "xmm_xmm": "xmm_same",
}


def classify_line(mnem, line, row_size):
    """(shape name, width, the cause it could not be classified).

    The width comes from the register names; where a shape names no
    register -- `mem_one` -- it comes from the ledger row's own `size`,
    which is the byte count the row holds. An x87 line's shape names
    no width at all, and none is asked of it: `key_width` gives every
    x87 row 80 bits from the mnemonic alone."""
    texts = operand_texts(line)
    classes = []
    widths = []
    for index, text in enumerate(texts):
        kind, width = operand_class(text, index, len(texts))
        if kind is None:
            return None, None, ("an operand text this classifier does "
                                "not read: %r" % text)
        classes.append(kind)
        widths.append(width)
    shape = SHAPE_OF_CLASSES.get(tuple(classes))
    if not classes and L48.x87_base(mnem) is not None:
        shape = "st_none"
    if shape is None:
        return None, None, ("an operand-kind combination the sweep "
                            "does not spell: %s" % "_".join(classes))
    if len(texts) == 2 and texts[0] == texts[1]:
        shape = SAME_OPERAND_SHAPE.get(shape, shape)
    width = None
    for candidate in widths:
        if candidate is not None:
            width = candidate
    if shape in ("mem_one", "none") or width is None:
        if row_size:
            width = row_size * 8
    widened = widening_shape(mnem, classes, widths)
    if widened is not None:
        return widened, None, None
    if shape in ST_SHAPES:
        return shape, width, None
    if width is None and not classes:
        # THE ZERO-OPERAND RULE, added 2026-09-09 by task h2. A line with
        # no operand text at all -- `cqto`, `cltq`, `cltd`, `cwtd`, `cqo`
        # -- has no register name to read a width from, and a carved
        # emulation body has no ledger row to give one either, so this
        # classifier used to refuse it ("no register name and no row size
        # to give a width", the one cause task h1b's composition column
        # hit, log 239 section 6). The width is in the reference's own
        # tables and is taken from there. LAST, so nothing that already
        # classified moves: a line whose operand text gave a width, and a
        # line whose ledger row gave one, are both decided above this.
        width = ZERO_OPERAND_WIDTH.get(mnem)
    if width is None:
        return None, None, ("no register name and no row size to give "
                            "a width")
    return shape, width, None


def widening_shape(mnem, classes, widths):
    """the sweep's own widening shapes: a mnemonic the reference's
    SIGN_EXTEND / ZERO_EXTEND tables give a (source, destination) width
    pair, spelled at exactly those two widths, is `widen_*` and carries
    no width of its own -- which is how `model_translate.attempts_for`
    records it."""
    pair = MT.widening_pair(mnem)
    if pair is None:
        return None
    if len(classes) != 2:
        return None
    if widths[1] != pair[1]:
        return None
    if classes[1] != "gpr":
        return None
    if classes[0] == "gpr" and widths[0] == pair[0]:
        return "widen_gpr_gpr"
    if classes[0] in ("mem", "index_mem"):
        return "widen_mem_gpr"
    return None


def attestation():
    """one stream over the canon40 shards: per (mnem, shape, width), how
    many ledger rows the corpus holds and in how many units."""
    _install_gpr_widths()
    readings = CF.runtime_answer_readings()
    routines = CF.runtime_routine_names(readings)
    cells = {}
    widths_of_key = {}
    guards = {}
    unclassifiable = collections.Counter()
    unclassifiable_example = {}
    relink_refusals = collections.Counter()
    units_seen = 0
    units_relinked = 0
    rows_seen = 0
    pair_rows_seen = 0
    shard_paths = TR.shards()
    total = len(shard_paths)
    for number, path in enumerate(shard_paths):
        document = json.load(open(path))
        for unit_id, record in document["units"].items():
            units_seen = units_seen + 1
            line_of_row = lines_of_unit(record, routines, readings)
            if line_of_row is None:
                producer_rows = arch_opcode_rows(record)
                relink_refusals[record.get("lang") or "?"] += len(
                    producer_rows)
                unclassifiable["the unit's body could not be relinked, "
                               "so no row of it has a line"] += len(
                    producer_rows)
                continue
            units_relinked = units_relinked + 1
            seen_here = set()
            for row in arch_opcode_rows(record):
                rows_seen = rows_seen + 1
                mnem = row["produced_by"]["mnem"]
                line = line_of_row.get(row["row"])
                if line is None:
                    unclassifiable[no_line_cause(row)] += 1
                    continue
                place_row(cells, widths_of_key, unclassifiable,
                          unclassifiable_example, seen_here, unit_id,
                          mnem, line, row, None)
            for row in flag_pair_rows(record):
                pair_rows_seen = pair_rows_seen + 1
                setter = row["produced_by"]["mnem"][0]
                consumer = row["produced_by"]["mnem"][1]
                line = line_of_row.get(row["row"])
                if line is None:
                    unclassifiable[no_line_cause(row)] += 1
                    continue
                if writes_the_branch_condition(consumer):
                    hold_guard_row(guards, consumer, setter, line,
                                   unit_id, seen_here)
                    continue
                place_row(cells, widths_of_key, unclassifiable,
                          unclassifiable_example, seen_here, unit_id,
                          consumer, line, row, setter)
        del document
        check_memory("shard %d" % number)
        if (number + 1) % 50 == 0 or number + 1 == total:
            say("   [%d/%d] shards read, %d units, %d arch-opcode "
                "rows, %d flag-pair rows"
                % (number + 1, total, units_seen, rows_seen,
                   pair_rows_seen))
    return {
        "cells": sorted(cells.values(),
                        key=lambda c: (c["mnem"], str(c["shape"]),
                                       str(c["key_width"]))),
        "guard_rows": guard_records(guards),
        "width_merges": width_merges(widths_of_key),
        "units_seen": units_seen,
        "units_relinked": units_relinked,
        "rows_seen": rows_seen,
        "flag_pair_rows_seen": pair_rows_seen,
        "shards": total,
        "unclassified": dict(unclassifiable),
        "unclassified_example": dict(unclassifiable_example),
        "relink_refusals": dict(relink_refusals),
    }


def place_row(cells, widths_of_key, unclassifiable,
              unclassifiable_example, seen_here, unit_id, mnem, line,
              row, setter):
    """one ledger row into its (mnem, shape, key_width) cell.

    `setter` is None for an ordinary arch-opcode row and is the
    flag-SETTING mnemonic for a flag-pair row, whose consumer reads the
    flags that setter wrote -- so the cell records it, since the
    mapping the consumer computes is a function of that flag state."""
    shape, width, cause = classify_line(mnem, line, row.get("size"))
    if cause is not None:
        unclassifiable[cause] += 1
        if cause not in unclassifiable_example:
            unclassifiable_example[cause] = line
        return
    key = (mnem, shape, key_width(mnem, width))
    widths_of_key.setdefault(key, set()).add(width)
    cell = cells.get(key)
    if cell is None:
        cell = {
            "mnem": mnem,
            "shape": shape,
            "width": width,
            "key_width": key[2],
            "ledger_rows": 0,
            "flag_pair_rows": 0,
            "units": 0,
            "example_units": [],
            "setter": [],
        }
        cells[key] = cell
    cell["ledger_rows"] += 1
    if setter is not None:
        cell["flag_pair_rows"] += 1
        hold_setter(cell["setter"], setter)
    if key in seen_here:
        return
    seen_here.add(key)
    cell["units"] += 1
    if len(cell["example_units"]) < 3:
        cell["example_units"].append(unit_id)


def hold_setter(held, setter):
    """the flag-setting mnemonic, as a RECORD carrying `mnem` -- never a
    bare token in a list, which the spelling guard reads as a key."""
    for record in held:
        if record["mnem"] == setter:
            record["ledger_rows"] += 1
            return
    held.append({"mnem": setter, "ledger_rows": 1})


def flag_pair_rows(record):
    """every ledger row whose producer is the PAIR (flag-setting arch
    opcode, flag-reading arch opcode), except the OUT block's answer
    row, which repeats the producer of the row it copies.

    `produced_by.mnem` is a two-element list on such a row: the setter
    then the consumer. `ledger_signatures.census_pass` records the
    consumer in `seen_as_flag_pair_element` and moves on, so task m1,
    which copied that reading, attested no flag consumer at all."""
    out = []
    for row in record.get("ledger") or []:
        produced_by = row.get("produced_by") or {}
        if produced_by.get("kind") != "flag_pair":
            continue
        mnem = produced_by.get("mnem")
        if not isinstance(mnem, list) or len(mnem) != 2:
            continue
        if row.get("block") == "OUT":
            continue
        out.append(row)
    return out


def writes_the_branch_condition(mnem):
    """does the reference's own entry for this mnemonic write the
    branch condition rather than a value?

    This is the machine-form test that separates the two populations
    the brief names: a flag consumer that writes a register leaves a
    VALUE cell, and one that writes only the fork the walk takes leaves
    a GUARD row and no value cell by nature."""
    entry = R.REFERENCE.opcode_table.entries.get(mnem)
    if entry is None:
        return False
    return R.THE_BRANCH_CONDITION in entry.writes


def hold_guard_row(guards, consumer, setter, line, unit_id, seen_here):
    record = guards.get(consumer)
    if record is None:
        record = {
            "mnem": consumer,
            "guard_rows": 0,
            "units": 0,
            "example_units": [],
            "text": line,
            "setter": [],
        }
        guards[consumer] = record
    record["guard_rows"] += 1
    hold_setter(record["setter"], setter)
    key = ("guard", consumer)
    if key in seen_here:
        return
    seen_here.add(key)
    record["units"] += 1
    if len(record["example_units"]) < 3:
        record["example_units"].append(unit_id)


def guard_records(guards):
    out = []
    for mnem in sorted(guards):
        out.append(guards[mnem])
    return out


def width_merges(widths_of_key):
    """the cells whose rows carried MORE THAN ONE of the classifier's
    own widths under one `key_width` -- the places where the one width
    rule merges two readings, listed so the merge is visible rather
    than silent."""
    out = []
    for key in sorted(widths_of_key, key=str):
        held = widths_of_key[key]
        if len(held) < 2:
            continue
        out.append({
            "mnem": key[0],
            "shape": key[1],
            "key_width": key[2],
            "classifier_widths": sorted(w for w in held
                                        if w is not None),
        })
    return out


OUT_ROW_CAUSE = (
    "the answer row of the OUT block, which canonical_form.wrap_unit "
    "adds AFTER the dataflow walk: it repeats the producer of the row "
    "it copies, so the relink gives it no line of its own and counting "
    "it would count one instruction twice")


def no_line_cause(row):
    if row.get("block") == "OUT":
        return OUT_ROW_CAUSE
    return ("a row the relink gave no line, and it is not the OUT "
            "block's answer row")


def arch_opcode_rows(record):
    out = []
    for row in record.get("ledger") or []:
        produced_by = row.get("produced_by") or {}
        if produced_by.get("kind") != "arch_opcode":
            continue
        if not isinstance(produced_by.get("mnem"), str):
            continue
        out.append(row)
    return out


def lines_of_unit(record, routines, readings):
    toolchain = CF.TOOLCHAIN_OF_LANGUAGE.get(record.get("lang"))
    try:
        _rows, line_of_row, _occurrence = T.relink(
            record, runtime_routines=routines,
            runtime_answers=readings, toolchain=toolchain)
    except Exception:
        return None
    return line_of_row


def attest_command():
    say("[1/2] the corpus's attestation, one stream over the shards")
    found = attestation()
    say("   %d cells over %d arch-opcode ledger rows and %d flag-pair "
        "rows" % (len(found["cells"]), found["rows_seen"],
                  found["flag_pair_rows_seen"]))
    guard_total = 0
    for record in found["guard_rows"]:
        guard_total = guard_total + record["guard_rows"]
    say("   %d guard rows over %d branch mnemonics"
        % (guard_total, len(found["guard_rows"])))
    say("   %d cells merge more than one classifier width under one "
        "key_width" % len(found["width_merges"]))
    say("   unclassified rows, by cause:")
    for cause in sorted(found["unclassified"]):
        say("      %6d  %s" % (found["unclassified"][cause], cause))
    say("[2/2] writing")
    document = {
        "meta": {
            "task": "m1",
            "what": "per (mnem, operand shape, width), how many ledger "
                    "rows of the canon40 corpus that triple produced "
                    "and in how many units",
            "reading": "copied from signatures/ledger_signatures.py "
                       "census_pass; the body line of a row comes from "
                       "term.relink",
            "peak_kb": peak_kb(),
        },
    }
    for name in sorted(found):
        document[name] = found[name]
    write_json(ATTEST_JSON, document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 3: THE EQUIVALENCES, REPORTED AND NEVER APPLIED
# ==================================================================
#
# Two kinds of edge, both keyed by row ids.
#
#   identical_text -- two rows at the same (shape, width) whose written
#       places and their layer-5 texts are the same object, flags
#       excluded. Textual identity is an UNDER-COUNT of equivalence: two
#       rows can compute one function and print differently.
#   same_builder   -- two mnemonics the reference registers with the
#       same builder OBJECT (`entry.build is other.build`). For each such
#       pair, at each (shape, width) where both carry a TRANSLATED row,
#       z3 is asked whether the destination terms differ and whether the
#       flags terms differ, separately, at a 3,000 ms ceiling. z3's own
#       words are the verdict: `unsat` (no differing point exists, so the
#       terms are equal), `sat` (a differing point exists) and `unknown`
#       (the ceiling was reached).


def destination_key(row):
    """the row's destination mapping: every written place except the
    flags, with its layer-5 text, in place order."""
    out = []
    for written in row.get("mapping") or []:
        if written["writes"] == "flags":
            continue
        out.append((written["writes"], written["text"]))
    out.sort()
    return tuple(out)


def flags_key(row):
    for written in row.get("mapping") or []:
        if written["writes"] == "flags":
            return written["text"]
    return None


def identical_text_edges(rows):
    """every pair of TRANSLATED rows at one (shape, width) whose
    destination mapping is the same text."""
    buckets = {}
    for row in rows:
        if row["outcome"] != "TRANSLATED":
            continue
        key = (row["shape"], row["width"], destination_key(row))
        buckets.setdefault(key, []).append(row["row_id"])
    classes = []
    pairs = 0
    for key in sorted(buckets, key=lambda k: (str(k[0]), str(k[1]))):
        members = sorted(buckets[key])
        pairs = pairs + len(members) * (len(members) - 1) // 2
        if len(members) < 2:
            continue
        classes.append({
            "shape": key[0],
            "width": key[1],
            "members": members,
        })
    return classes, pairs, len(buckets)


def same_builder_pairs(table):
    """every pair of mnemonics the table registers with the same builder
    object. The candidate set is the identity of the FUNCTION the table
    holds, never a reading of the names."""
    by_object = {}
    for mnem in sorted(table.entries):
        entry = table.entries[mnem]
        if entry.build is None:
            continue
        by_object.setdefault(id(entry.build), []).append(mnem)
    groups = []
    for key in sorted(by_object):
        members = by_object[key]
        if len(members) < 2:
            continue
        groups.append(sorted(members))
    groups.sort(key=lambda g: (-len(g), g[0]))
    return groups


SOLVER_MEMO = {}
"""one entry per DISTINCT question put to z3.

A question is the pair of the two terms' own s-expressions. z3's answer
is a function of the terms alone, so a question already asked is not
asked twice -- the memo re-uses the answer rather than skipping a
comparison, and `solver_calls` / `solver_memo_hits` in the edges
document's meta say how many of each there were. Nothing is compared
less than the brief asks; the same question is simply not re-put. This
matters because the x87 group's terms are 80-bit floating point, where
a `z3.Solver` run reaches the 3,000 ms ceiling and answers `unknown`."""

SOLVER_CALLS = [0, 0]
"""[calls actually made, answers taken from the memo]."""


def question_key(left, right):
    digest = hashlib.sha1()
    digest.update(left.sexpr().encode("utf-8"))
    digest.update(b"\x00")
    digest.update(right.sexpr().encode("utf-8"))
    return digest.hexdigest()


def solver_verdict(left, right):
    """z3 asked whether two terms can differ, at the 3,000 ms ceiling.

    Returns (its own word, milliseconds, a refusal sentence or None)."""
    if left is None or right is None:
        return None, 0, "one of the two places is not written at all"
    if left.sort().sexpr() != right.sort().sexpr():
        return None, 0, ("the two terms are of different sorts, %s and "
                         "%s, so no equality between them is even "
                         "stated" % (left.sort().sexpr(),
                                     right.sort().sexpr()))
    key = question_key(left, right)
    held = SOLVER_MEMO.get(key)
    if held is not None:
        SOLVER_CALLS[1] = SOLVER_CALLS[1] + 1
        return held[0], held[1], held[2]
    solver = z3.Solver()
    solver.set("timeout", SOLVER_CEILING_MS)
    solver.add(left != right)
    started = time.time()
    answer = solver.check()
    took = int((time.time() - started) * 1000)
    SOLVER_CALLS[0] = SOLVER_CALLS[0] + 1
    SOLVER_MEMO[key] = (str(answer), took, None)
    return str(answer), took, None


def cells_of_pair(by_key, group_id, left_mnem, right_mnem):
    """every (shape, width) at which both mnemonics of one same-builder
    pair carry a TRANSLATED row.

    THE THREE X87 SHAPES ARE NOT IN THIS POPULATION, and that is task
    m1b's brief instructing it: the x87 group's terms are 80-bit
    floating point, every solver call on them reaches the 3,000 ms
    ceiling and answers `unknown`, and task m1 measured the pass at
    about 24 hours before its memo. Leaving `st_st`, `st_one` and
    `st_none` out keeps this population EXACTLY the one m1 decided, so
    the verdicts are comparable row for row; nothing else is skipped."""
    out = []
    for key in sorted(by_key, key=str):
        if key[0] != left_mnem:
            continue
        if key[1] in ST_SHAPES:
            continue
        mirror = (right_mnem, key[1], key[2])
        other = by_key.get(mirror)
        if other is None:
            continue
        out.append({
            "edge": [by_key[key]["row_id"], other["row_id"]],
            "group_id": group_id,
            "shape": key[1],
            "width": key[2],
        })
    return out


def decide_cell(cell):
    """the two verdicts for one cell, from the rows' own z3 terms."""
    left_places, left_flags = terms_for(cell["edge"][0])
    right_places, right_flags = terms_for(cell["edge"][1])
    record = {
        "edge": cell["edge"],
        "group_id": cell["group_id"],
        "shape": cell["shape"],
        "width": cell["width"],
    }
    left_destination = joined_destination(left_places)
    right_destination = joined_destination(right_places)
    answer, took, refusal = solver_verdict(left_destination,
                                           right_destination)
    record["destination_verdict"] = answer
    record["destination_ms"] = took
    if refusal is not None:
        record["destination_refusal"] = refusal
    answer, took, refusal = solver_verdict(left_flags, right_flags)
    record["flags_verdict"] = answer
    record["flags_ms"] = took
    if refusal is not None:
        record["flags_refusal"] = refusal
    record["left_writes_flags"] = left_flags is not None
    record["right_writes_flags"] = right_flags is not None
    return record


def joined_destination(places):
    """every destination place of a row as ONE term, so a mnemonic that
    writes two places is compared on both at once. The places are joined
    in name order, which is the same order for both sides of an edge or
    the sorts differ and the verdict says so."""
    if places is None:
        return None
    names = sorted(places)
    if not names:
        return None
    pieces = []
    for name in names:
        pieces.append(MT.as_bits(places[name]))
    if len(pieces) == 1:
        return pieces[0]
    return z3.Concat(*pieces)


ROWS_BY_ID = {}

TERMS_OF_ID = {}

TERM_CACHE_CEILING = 400
"""how many rows' rebuilt z3 terms are held at once.

A rebuilt term holds z3 AST nodes, and the sample run measured about
0.7 MB of resident memory per row. The cells are walked in row-id
order, so two cells that share a row are almost always next to each
other; a cache this size is emptied and refilled a few dozen times
over the whole pass and keeps the terms inside a few hundred MB."""


def load_rows_by_id(rows):
    for row in rows:
        ROWS_BY_ID[row["row_id"]] = row


def terms_for(row_id):
    """the z3 terms of one row -- (places written -> term, the flags
    pair or None) -- rebuilt by re-running the row's own line."""
    held = TERMS_OF_ID.get(row_id)
    if held is not None:
        return held
    if len(TERMS_OF_ID) >= TERM_CACHE_CEILING:
        TERMS_OF_ID.clear()
    row = ROWS_BY_ID[row_id]
    attempt = {
        "mnem": row["mnem"],
        "operands": row["operands"],
        "preseeded": row.get("preseeded", False),
        "flags_in_setter": (row.get("flags_in") or {}).get("mnem"),
        "width": row.get("width"),
    }
    places, flags = places_of_attempt(attempt)
    pair = None
    if flags is not None:
        pair = z3.Concat(MT.as_bits(flags[1]), MT.as_bits(flags[2]))
    TERMS_OF_ID[row_id] = (places, pair)
    return TERMS_OF_ID[row_id]


def rows_by_triple(rows):
    """one TRANSLATED row per (mnem, shape, width) -- THE KEY the ruling
    of 2026-09-08 names -- the first in the sweep's own order.

    A triple can carry several sweep attempts: the sweep's second pass
    re-runs a flag-reading mnemonic once per flag-setting mnemonic it
    saw, and those attempts differ only in which seed state the builder
    was handed, not in the instruction. The seed is a probe choice, not
    part of the machine form, so the comparison is made once per triple
    and the first attempt in sweep order is the one compared. The count
    of triples carrying more than one attempt is reported beside it."""
    by_key = {}
    several = 0
    for row in rows:
        if row["outcome"] != "TRANSLATED":
            continue
        key = (row["mnem"], row["shape"], row["width"])
        if key in by_key:
            several = several + 1
            continue
        by_key[key] = row
    return by_key, several


def edge_cells(by_key, groups, sample):
    """every (same-builder pair, shape, width) cell, in row-id order."""
    cells = []
    for index, group in enumerate(groups):
        group_id = "g%02d" % index
        for first in range(0, len(group)):
            for second in range(first + 1, len(group)):
                cells.extend(cells_of_pair(by_key, group_id,
                                           group[first], group[second]))
    cells.sort(key=lambda c: c["edge"])
    say("   %d (pair, shape, width) cells in all" % len(cells))
    if sample is not None:
        cells = cells[:sample]
    return cells


def edges_command(sample):
    say("[1/4] reading the rows")
    document = json.load(open(ROWS_JSON))
    rows = document["rows"]
    say("   %d rows" % len(rows))
    say("[2/4] identical_text: classes and pairs")
    classes, pairs, buckets = identical_text_edges(rows)
    say("   %d classes of more than one row; %d pairs; %d distinct "
        "mappings among the TRANSLATED rows" % (len(classes), pairs,
                                                buckets))
    say("[3/4] same_builder: the cells, and z3's two verdicts each")
    table = R.REFERENCE.opcode_table
    groups = same_builder_pairs(table)
    say("   %d same-builder groups" % len(groups))
    by_key, several = rows_by_triple(rows)
    say("   %d distinct (mnem, shape, width) triples carry a "
        "TRANSLATED row; %d further attempts share a triple with one "
        "of them and are not compared a second time"
        % (len(by_key), several))
    cells = edge_cells(by_key, groups, sample)
    say("   %d cells to decide" % len(cells))
    load_rows_by_id(rows)
    decided = []
    total = len(cells)
    started = time.time()
    for index, cell in enumerate(cells):
        decided.append(decide_cell(cell))
        if (index + 1) % 200 == 0 or index + 1 == total:
            say("   [%d/%d] cells decided, %.0f s, %d solver calls, "
                "%d answers re-used"
                % (index + 1, total, time.time() - started,
                   SOLVER_CALLS[0], SOLVER_CALLS[1]))
            check_memory("cell %d" % index)
    say("   the pair the brief names, decided the same way")
    named = named_pair_cells(rows)
    say("[4/4] writing")
    document = {
        "meta": {
            "task": "m1",
            "what": "the equivalences between rows, REPORTED and never "
                    "applied; every edge is keyed by row ids",
            "solver_ceiling_ms": SOLVER_CEILING_MS,
            "sample": sample,
            "triples_translated": len(by_key),
            "attempts_sharing_a_triple": several,
            "solver_calls": SOLVER_CALLS[0],
            "solver_memo_hits": SOLVER_CALLS[1],
            "peak_kb": peak_kb(),
        },
        "named_pair_cells": named,
        "identical_text_classes": classes,
        "identical_text_pairs": pairs,
        "distinct_mappings": buckets,
        "same_builder_groups": groups_as_records(groups),
        "same_builder_cells": decided,
    }
    write_json(EDGES_JSON, document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


# THE ONE PAIR THE BRIEF NAMES. `add` and `lea` do NOT share a builder
# (`build_binary` versus `build_lea`), so they are not a `same_builder`
# edge; the brief asks for z3's verdict on them anyway, on the ground
# that a destination term can be equal where the flags terms are not.
# The candidate set here is the brief's own instruction, which the
# spelling ban allows as ratified intention; the cells are keyed by row
# ids like every other edge.
NAMED_PAIR = ("add", "lea")


def named_pair_cells(rows):
    groups = [sorted(NAMED_PAIR)]
    by_key, _several = rows_by_triple(rows)
    cells = edge_cells(by_key, groups, None)
    load_rows_by_id(rows)
    out = []
    for cell in cells:
        cell["group_id"] = "named_pair"
        out.append(decide_cell(cell))
    return out


def groups_as_records(groups):
    """a same-builder group as a list of members, each member a record
    whose mnemonic sits in `mnem` -- never a bare token in a list."""
    out = []
    for index, group in enumerate(groups):
        members = []
        for mnem in group:
            members.append({"mnem": mnem})
        out.append({
            "group_id": "g%02d" % index,
            "size": len(group),
            "members": members,
        })
    return out


# ==================================================================
# section 4: THE COUNTS, and the one document
# ==================================================================


def counts_of(rows, edges, attest):
    table = R.REFERENCE.opcode_table
    corpus = json.load(open(UNIQUE_OPCODES_JSON))
    corpus_mnems = set()
    for record in corpus["cross_language_rows"]:
        corpus_mnems.add(record["mnem"])
    table_mnems = set(table.entries)
    translated = []
    for row in rows:
        if row["outcome"] == "TRANSLATED":
            translated.append(row)
    splits = mnemonics_with_several_mappings(rows)
    aliases = alias_groups(edges)
    in_table = set()
    for row in translated:
        in_table.add((row["mnem"], row["shape"], row["key_width"]))
    orphan_cells = []
    for cell in attest["cells"]:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        if key in in_table:
            continue
        orphan_cells.append(cell)
    coverage = coverage_table(rows, attest, corpus_mnems, in_table)
    out = {
        "coverage": coverage["rows"],
        "coverage_totals": coverage["totals"],
        "attestation_width_merges": attest["width_merges"],
        "guard_rows": attest["guard_rows"],
        "table_mnemonics": len(table_mnems),
        "corpus_mnemonics": len(corpus_mnems),
        "in_both": len(table_mnems & corpus_mnems),
        "table_only": as_records(sorted(table_mnems - corpus_mnems)),
        "corpus_only": as_records(sorted(corpus_mnems - table_mnems)),
        "sweep_attempts": len(rows),
        "rows_translated": len(translated),
        "distinct_mappings_after_identical_text":
            edges["distinct_mappings"],
        "identical_text_pairs": edges["identical_text_pairs"],
        "mnemonics_with_several_mappings": splits,
        "alias_groups": aliases,
        "attested_cells": len(attest["cells"]),
        "attested_ledger_rows": attest["rows_seen"],
        "attested_cells_with_no_translated_row": orphan_cells,
        "attested_cells_placed": len(attest["cells"]) - len(orphan_cells),
        "translated_triples": len(in_table),
        "guard_rows_total": guard_rows_total(attest),
        "flag_consumer_rows": flag_consumer_rows(attest),
        "mnemonics_with_a_placed_cell": mnemonics_placed(coverage),
    }
    return out


def guard_rows_total(attest):
    total = 0
    for record in attest["guard_rows"]:
        total = total + record["guard_rows"]
    return total


def flag_consumer_rows(attest):
    total = 0
    for cell in attest["cells"]:
        total = total + cell["flag_pair_rows"]
    return total


def mnemonics_placed(coverage):
    total = 0
    for record in coverage["rows"]:
        if record["category"] == PLACED:
            total = total + 1
    return total


def as_records(mnems):
    out = []
    for mnem in mnems:
        out.append({"mnem": mnem})
    return out


# ==================================================================
# THE COVERAGE TABLE -- the acceptance criterion
# ==================================================================
#
# One row per mnemonic of the corpus's 162, in exactly one of four
# categories, so the four counts sum to 162:
#
#   placed          -- at least one attested VALUE cell of this
#                      mnemonic lands on a TRANSLATED row of the table
#   unspelled_form  -- it has attested value cells and NONE of them
#                      lands on a TRANSLATED row, so the corpus spells
#                      an operand form the table has no mapping for
#   guard_only      -- a control transfer: it writes no value by
#                      nature, so it has no value cell to place; it is
#                      attested by the ledger's GUARD rows instead, and
#                      the count is 0 for an unconditional transfer,
#                      which produces no ledger row at all
#   never_placed    -- no value cell, and not a control transfer: the
#                      corpus produced no ledger row this table could
#                      key. Every one carries its cause.

PLACED = "a value cell on a TRANSLATED row"

UNSPELLED_FORM = "attested at a form the sweep does not spell"

GUARD_ONLY = "a control transfer -- attested by guard rows and never by a value cell"

NEVER_PLACED = "never placed"


def is_a_control_transfer(mnem):
    """the reference's own reading, not the token's: an entry that
    writes the branch condition, or one of the three the reference's
    `TRANSFER` set names (`call`, `jmp`, `ud2`), or `ret`, which the
    reference holds in `NO_OPERATION` and the brief names with them."""
    if writes_the_branch_condition(mnem):
        return True
    if mnem in R.TRANSFER:
        return True
    if mnem == "ret":
        return True
    return False


def corpus_occurrences():
    """per mnemonic, how many body lines of the corpus spell it --
    task o2's own product, `unique_opcodes.json`, summed over its
    per-language counts."""
    document = json.load(open(UNIQUE_OPCODES_JSON))
    out = {}
    for record in document["cross_language_rows"]:
        total = 0
        for field in record:
            if field == "mnem":
                continue
            value = record[field]
            if isinstance(value, int):
                total = total + value
        out[record["mnem"]] = total
    return out


def sweep_causes_by_mnem_and_shape(rows):
    """per (mnem, shape), the sweep's own most common refusal, so a
    cell with no TRANSLATED row carries a cause quoted rather than
    asserted."""
    out = {}
    for row in rows:
        if row["outcome"] == "TRANSLATED":
            continue
        reason = row.get("reason")
        if reason is None:
            continue
        key = (row["mnem"], row["shape"])
        bucket = out.setdefault(key, collections.Counter())
        bucket[reason] += 1
    return out


def coverage_table(rows, attest, corpus_mnems, in_table):
    """one record per corpus mnemonic, and the four category totals."""
    occurrences = corpus_occurrences()
    refusals = sweep_causes_by_mnem_and_shape(rows)
    table = R.REFERENCE.opcode_table
    cells_of = {}
    for cell in attest["cells"]:
        cells_of.setdefault(cell["mnem"], []).append(cell)
    guards_of = {}
    for record in attest["guard_rows"]:
        guards_of[record["mnem"]] = record
    out = []
    totals = collections.Counter()
    for mnem in sorted(corpus_mnems):
        record = one_coverage_row(mnem, cells_of.get(mnem) or [],
                                  guards_of.get(mnem), in_table,
                                  refusals, occurrences, table)
        totals[record["category"]] += 1
        out.append(record)
    listed = []
    for category in (PLACED, UNSPELLED_FORM, GUARD_ONLY, NEVER_PLACED):
        listed.append({"category": category, "mnemonics":
                       totals[category]})
    return {"rows": out, "totals": listed}


def one_coverage_row(mnem, cells, guard, in_table, refusals,
                     occurrences, table):
    placed = []
    unplaced = []
    ledger_rows = 0
    flag_pair_rows = 0
    for cell in cells:
        ledger_rows = ledger_rows + cell["ledger_rows"]
        flag_pair_rows = flag_pair_rows + cell["flag_pair_rows"]
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        if key in in_table:
            placed.append(cell)
        else:
            unplaced.append(cell)
    record = {
        "mnem": mnem,
        "attested_value_cells_placed": len(placed),
        "attested_value_cells_at_an_unspelled_form": len(unplaced),
        "attested_by_guard_rows": 0,
        "attested_value_cells_never_placed": 0,
        "ledger_rows": ledger_rows,
        "flag_pair_rows": flag_pair_rows,
        "corpus_occurrences": occurrences.get(mnem, 0),
    }
    if guard is not None:
        record["attested_by_guard_rows"] = guard["guard_rows"]
    if is_a_control_transfer(mnem):
        record["category"] = GUARD_ONLY
        record["reason"] = control_transfer_cause(mnem, guard, table)
        return record
    if placed:
        record["category"] = PLACED
        return record
    if unplaced:
        record["category"] = UNSPELLED_FORM
        record["reason"] = unplaced_cause(unplaced, refusals,
                                          table)
        return record
    record["category"] = NEVER_PLACED
    record["attested_value_cells_never_placed"] = 1
    record["reason"] = never_placed_cause(mnem, record, table)
    return record


def control_transfer_cause(mnem, guard, table):
    entry = table.entries.get(mnem)
    if guard is not None:
        return ("a flag-reading transfer: the ledger records it as the "
                "reading half of a GUARD-block flag pair, %d rows, and "
                "it writes %r rather than a value"
                % (guard["guard_rows"],
                   R.THE_BRANCH_CONDITION))
    if entry is not None and entry.build is None:
        return ("an unconditional transfer: it produces no ledger row "
                "of any kind, because the ledger records one row per "
                "value produced and this opcode produces none; the "
                "reference registers it with no builder -- %r"
                % (entry.cause or "no cause recorded"))
    return ("an unconditional transfer: it produces no ledger row of "
            "any kind, because the ledger records one row per value "
            "produced and this opcode produces none")


def unplaced_cause(unplaced, refusals, table):
    """the cause, quoted from the sweep or from the reference's own
    entry, that the attested form has no TRANSLATED row."""
    cell = unplaced[0]
    entry = table.entries.get(cell["mnem"])
    if entry is not None and entry.build is None:
        return ("the reference registers it with no builder -- %r -- "
                "so the sweep states one NO_BUILDER row for it and no "
                "row at any shape; the corpus spells it at shape %r"
                % (entry.cause or "no cause recorded", cell["shape"]))
    bucket = refusals.get((cell["mnem"], cell["shape"]))
    if bucket is None:
        return ("the sweep spells no attempt at all at shape %r, so "
                "the table has no row for the form the corpus spells"
                % cell["shape"])
    reason, count = bucket.most_common(1)[0]
    return ("the sweep's own refusal at shape %r, %d attempts: %s"
            % (cell["shape"], count, reason))


def never_placed_cause(mnem, record, table):
    entry = table.entries.get(mnem)
    if entry is None:
        return ("the reference's opcode table holds no entry for it "
                "at all")
    if entry.build is None:
        return ("the reference registers it with no builder -- %r -- "
                "so the table states no mapping to place anything on"
                % (entry.cause or "no cause recorded"))
    return ("no ledger row of the corpus names it as a producer, so "
            "the classifier never saw a line of it; the corpus's own "
            "body lines spell it %d times (unique_opcodes.json)"
            % record["corpus_occurrences"])


def mnemonics_with_several_mappings(rows):
    """the SPLITS: one spelling carrying more than one mapping.

    TWO READINGS, both counted, because they answer different
    questions and only the first is the one the ruling of 2026-09-08
    names.

      `place_kind_sets` -- the distinct multisets of place KINDS the
        mnemonic's TRANSLATED rows write, a kind being one of `reg`,
        `flags`, `mem`, `stack`, `x87`. THIS IS THE SPLIT CRITERION,
        and it is the ruling's own example read mechanically:
        one-operand `imul` writes two registers (the accumulator pair)
        and two-operand `imul` writes one register and the flags, so
        the spelling carries two mappings. The kind abstracts away
        WHICH register, so a mnemonic whose only difference between
        shapes is that the destination is `%edi` in one and `%eax` in
        another is not counted as split.
      `distinct_place_sets` -- the same count before that abstraction,
        over the place NAMES. Always the larger, because a different
        destination register is a different place name.
      `distinct_destination_texts` -- how many distinct destination
        mappings its rows print, over the deduplicated (mnem, shape,
        width) triples. Larger again, because the same computation at
        two widths prints two texts. Reported so the finer picture is
        on the page, not as the split count.
    """
    by_key, _several = rows_by_triple(rows)
    places = {}
    kinds = {}
    texts = {}
    for key in by_key:
        row = by_key[key]
        written = []
        written_kinds = []
        for entry in row.get("mapping") or []:
            written.append(entry["writes"])
            written_kinds.append(place_kind(entry["writes"]))
        places.setdefault(row["mnem"], set()).add(tuple(sorted(written)))
        kinds.setdefault(row["mnem"], set()).add(
            tuple(sorted(written_kinds)))
        texts.setdefault(row["mnem"], set()).add(destination_key(row))
    out = []
    for mnem in sorted(kinds):
        if len(kinds[mnem]) < 2:
            continue
        listed = []
        for one in sorted(kinds[mnem]):
            listed.append(" ".join(one) or "(nothing)")
        out.append({
            "mnem": mnem,
            "place_kind_sets": listed,
            "distinct_place_sets": len(places[mnem]),
            "distinct_destination_texts": len(texts[mnem]),
        })
    out.sort(key=lambda r: (-len(r["place_kind_sets"]), r["mnem"]))
    return out


def place_kind(place):
    """the KIND of a place the sweep names: which register a write
    lands in is a fact about the operand spelling, the kind is a fact
    about the mapping."""
    if place == "flags":
        return "flags"
    for prefix, kind in (("reg_", "reg"), ("mem_", "mem"),
                         ("stack_", "stack"), ("x87_", "x87")):
        if place.startswith(prefix):
            return kind
    return "other"


def cell_is_equal_everywhere(cell):
    """one cell counts as equal when z3 answered `unsat` on the
    destination and, where both sides write flags, on the flags too."""
    if cell.get("destination_verdict") != "unsat":
        return False
    if cell.get("destination_refusal") is not None:
        return False
    if not cell.get("left_writes_flags"):
        if not cell.get("right_writes_flags"):
            return True
    if cell.get("flags_verdict") != "unsat":
        return False
    return True


def alias_groups(edges):
    """every same-builder group, with how many of its cells came back
    equal on every written place and how many did not. A group whose
    cells are ALL equal is an alias group: the reference's own builder
    object gives its members one mapping, and z3 agrees on every place
    they write."""
    tally = {}
    for group in edges["same_builder_groups"]:
        tally[group["group_id"]] = {
            "group_id": group["group_id"],
            "size": group["size"],
            "members": group["members"],
            "cells": 0,
            "cells_equal_everywhere": 0,
            "cells_not_equal": 0,
        }
    for cell in edges["same_builder_cells"]:
        group_id = cell.get("group_id")
        if group_id is None:
            continue
        entry = tally[group_id]
        entry["cells"] += 1
        if cell_is_equal_everywhere(cell):
            entry["cells_equal_everywhere"] += 1
        else:
            entry["cells_not_equal"] += 1
    out = []
    for group_id in sorted(tally):
        entry = tally[group_id]
        entry["is_an_alias_group"] = False
        if entry["cells"] > 0:
            if entry["cells_not_equal"] == 0:
                entry["is_an_alias_group"] = True
        out.append(entry)
    return out


def causes_of(rows):
    """the NO_BUILDER and NOT_MODELLED rows, counted by the cause the
    sweep itself wrote."""
    by_outcome = {}
    for row in rows:
        outcome = row["outcome"]
        if outcome == "TRANSLATED":
            continue
        reason = row.get("reason") or "(no cause recorded)"
        bucket = by_outcome.setdefault(outcome, collections.Counter())
        bucket[reason] += 1
    out = {}
    for outcome in sorted(by_outcome):
        listed = []
        for reason in sorted(by_outcome[outcome],
                             key=lambda r: (-by_outcome[outcome][r], r)):
            listed.append({
                "reason": reason,
                "count": by_outcome[outcome][reason],
            })
        out[outcome] = listed
    return out


def assemble_command():
    say("[1/3] reading the three")
    rows_document = json.load(open(ROWS_JSON))
    attest_document = json.load(open(ATTEST_JSON))
    edges_document = json.load(open(EDGES_JSON))
    rows = rows_document["rows"]
    say("[2/3] joining the attestation onto the rows, and counting")
    by_triple = {}
    for cell in attest_document["cells"]:
        key = (cell["mnem"], cell["shape"], cell["key_width"])
        by_triple[key] = cell
    attested = 0
    for row in rows:
        key = (row["mnem"], row["shape"], row["key_width"])
        cell = by_triple.get(key)
        if cell is None:
            row["attestation"] = {"ledger_rows": 0, "units": 0}
            continue
        attested = attested + 1
        row["attestation"] = {
            "ledger_rows": cell["ledger_rows"],
            "units": cell["units"],
            "example_units": cell["example_units"],
            "flag_pair_rows": cell["flag_pair_rows"],
            "setter": cell["setter"],
        }
    say("   %d of %d rows carry a corpus attestation"
        % (attested, len(rows)))
    counted = counts_of(rows, edges_document, attest_document)
    causes = causes_of(rows)
    say("[3/3] writing")
    document = {
        "meta": {
            "task": "m1",
            "what": "the arch-opcode model table: every mapping the "
                    "reference holds, keyed by (mnem, operand shape, "
                    "width), with the corpus's attestation and the "
                    "reported equivalences",
            "layer5_printer": "term.Term.normalize -- the pipeline's "
                              "own fixed-rule re-render, which applies "
                              "to a bare z3 expression",
            "solver_ceiling_ms": SOLVER_CEILING_MS,
            "peak_kb": peak_kb(),
        },
        "counts": counted,
        "causes": causes,
        "attestation_unclassified": attest_document["unclassified"],
        "attestation_unclassified_example":
            attest_document["unclassified_example"],
        "attestation_flag_pair_rows_seen":
            attest_document["flag_pair_rows_seen"],
        "attestation_shards": attest_document["shards"],
        "attestation_units_seen": attest_document["units_seen"],
        "attestation_units_relinked": attest_document["units_relinked"],
        "identical_text_classes":
            edges_document["identical_text_classes"],
        "same_builder_groups": edges_document["same_builder_groups"],
        "same_builder_cells": edges_document["same_builder_cells"],
        "named_pair_cells": edges_document["named_pair_cells"],
        "rows": rows,
    }
    write_json(OUT_JSON, document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


# ==================================================================
# section 5: THE REPORT
# ==================================================================
#
# `model_table.md`, sections in the brief's own order. Every table is a
# markdown pipe table (the protocol's `media.pipe-tables`); every table
# and block carries a label so it can be pointed at.


EXAMPLE_ROWS = (
    ("add", "gpr_gpr", 32),
    ("imul", "gpr_one", 32),
    ("imul", "gpr_gpr", 32),
    ("sar", "cl_gpr", 32),
    ("idiv", "gpr_one", 32),
)


def report_command():
    document = json.load(open(OUT_JSON))
    lines = []
    write_report_head(lines, document)
    write_report_examples(lines, document)
    write_report_partial(lines, document)
    write_report_attestation(lines, document)
    write_report_edges(lines, document)
    write_report_counts(lines, document)
    write_report_causes(lines, document)
    write_report_width_rule(lines, document)
    write_report_coverage(lines, document)
    write_report_guard_rows(lines, document)
    handle = open(OUT_MD, "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    say("wrote %s (%d lines)" % (OUT_MD, len(lines)))
    return 0


def write_report_head(lines, document):
    counts = document["counts"]
    lines.append("# model_table.md — the arch-opcode model table")
    lines.append("")
    lines.append("Tasks m1 and m1b, node "
                 "`hq.research.arch_unit_oracle`. Written by "
                 "`model_table.py`; never hand-edited. Sections 7, 8 "
                 "and 9 are task m1b's: the one width rule, the "
                 "coverage table over the corpus's 162 mnemonics, and "
                 "the control transfers' guard rows.")
    lines.append("")
    lines.append("**What this table is, one sentence.** Every mapping "
                 "the reference simulator's `opcode_table` holds, one "
                 "row per (`mnem`, operand shape, width) the sweep in "
                 "`op_pipeline/lean/model_translate.py` spells, with "
                 "the z3 term each written place receives printed by "
                 "the pipeline's layer-5 rule, the corpus's own "
                 "attestation beside it, and the equivalences between "
                 "rows reported rather than applied.")
    lines.append("")
    lines.append("The printer is `term.Term.normalize`, the pipeline's "
                 "own fixed-rule re-render; it applies to a bare z3 "
                 "expression, so the fallback the brief allowed "
                 "(`str(z3.simplify(t))`) was not used. Every term "
                 "below is LITERAL.")
    lines.append("")
    lines.append("| what | count |")
    lines.append("|---|---|")
    lines.append("| sweep attempts | %d |" % counts["sweep_attempts"])
    lines.append("| rows TRANSLATED | %d |" % counts["rows_translated"])
    lines.append("| table mnemonics | %d |" % counts["table_mnemonics"])
    lines.append("| corpus mnemonics | %d |"
                 % counts["corpus_mnemonics"])
    lines.append("")


def find_row(document, mnem, shape, width):
    for row in document["rows"]:
        if row["mnem"] != mnem:
            continue
        if row["shape"] != shape:
            continue
        if row["width"] != width:
            continue
        if row["outcome"] != "TRANSLATED":
            continue
        return row
    return None


def write_report_examples(lines, document):
    lines.append("## 1. Five rows in full, LITERAL")
    lines.append("")
    for mnem, shape, width in EXAMPLE_ROWS:
        row = find_row(document, mnem, shape, width)
        lines.append("### `%s` %s %s" % (mnem, shape, width))
        lines.append("")
        if row is None:
            lines.append("No TRANSLATED row at this triple.")
            lines.append("")
            continue
        lines.append("Block — the row as `model_table.json` holds it:")
        lines.append("")
        lines.append("```")
        lines.append(json.dumps(row, indent=1, sort_keys=True))
        lines.append("```")
        lines.append("")


def write_report_partial(lines, document):
    lines.append("## 2. The partial region, read from each builder's "
                 "own source")
    lines.append("")
    lines.append("The rule, LITERAL: every statement of a builder's "
                 "source carrying one of the marks `raise "
                 "NotModeled(`, `shift_mask(`, `z3.If(` is quoted "
                 "whole; a builder carrying none of them is recorded "
                 "as total on bit patterns.")
    lines.append("")
    lines.append("WHAT THE THREE MARKS DO NOT CATCH, named rather than "
                 "left implicit: a branch on the NUMBER of operands. "
                 "`reference.build_binary` opens `if len(ops.texts) == "
                 "1: build_wide_multiply(ops); return`, so a "
                 "one-operand line of any BINARY-family mnemonic is "
                 "given the accumulator-pair widening multiply. That "
                 "is why `add`, `and`, `or`, `sub` and `xor` carry "
                 "`gpr_one` and `mem_one` rows whose mapping is a "
                 "multiply, and it is recorded here as a fact about "
                 "the reference, not repaired: `reference.py` is a "
                 "shared file this task did not touch. Measured: 28 "
                 "such rows, of which only `imul`'s are attested by "
                 "the corpus at all (2 ledger rows).")
    lines.append("")
    lines.append("THE DIVISION ROWS, since the brief asks for them by "
                 "name: `build_division`'s only stated condition is a "
                 "WIDTH refusal. It writes z3's `SDiv`/`UDiv` and "
                 "`SRem`/`URem`, which are TOTAL functions on bit "
                 "patterns, so division by zero and the `MIN / -1` "
                 "case are not branched on and no fault region is "
                 "named in the model. The fault is the machine's, and "
                 "this reference does not carry it.")
    lines.append("")
    seen = {}
    for row in document["rows"]:
        builder = row.get("builder")
        if builder is None:
            continue
        if builder in seen:
            continue
        seen[builder] = row["condition"]
    lines.append("Table 1 — one line per builder in the table, with "
                 "the condition its own source states.")
    lines.append("")
    lines.append("| builder | condition, quoted |")
    lines.append("|---|---|")
    for builder in sorted(seen):
        text = seen[builder].replace("|", "\\|")
        lines.append("| `%s` | %s |" % (builder, text))
    lines.append("")


def write_report_attestation(lines, document):
    lines.append("## 3. The corpus's attestation")
    lines.append("")
    lines.append("Every arch-opcode ledger row AND every flag-pair "
                 "ledger row of every canon40 unit is classified into "
                 "the sweep's own operand shapes by the operand TEXTS "
                 "of the body line that made it (`term.relink` gives "
                 "the line). The classifier is `operand_class` and "
                 "`SHAPE_OF_CLASSES` in `model_table.py`, LITERAL "
                 "there.")
    lines.append("")
    lines.append("A FLAG-PAIR row's producer is the pair (flag-setting "
                 "opcode, flag-reading opcode), and the READING half "
                 "is the mnemonic attested: its operands come from the "
                 "relinked line like any other, its cell is keyed like "
                 "any other, and the cell records the setter, since "
                 "what the mapping computes is a function of the flags "
                 "that setter wrote. Task m1 attested none of them, "
                 "having copied `ledger_signatures.census_pass`, which "
                 "records the consumer in `seen_as_flag_pair_element` "
                 "and moves on.")
    lines.append("")
    lines.append("| what | count |")
    lines.append("|---|---|")
    lines.append("| shards streamed | %d |"
                 % document["attestation_shards"])
    lines.append("| units seen | %d |"
                 % document["attestation_units_seen"])
    lines.append("| units relinked | %d |"
                 % document["attestation_units_relinked"])
    lines.append("| units the relink refused | %d |"
                 % (document["attestation_units_seen"]
                    - document["attestation_units_relinked"]))
    lines.append("| attested (mnem, shape, key_width) cells | %d |"
                 % document["counts"]["attested_cells"])
    lines.append("| arch-opcode ledger rows seen | %d |"
                 % document["counts"]["attested_ledger_rows"])
    lines.append("| flag-pair ledger rows seen (the OUT block's "
                 "repeats excluded) | %d |"
                 % document["attestation_flag_pair_rows_seen"])
    lines.append("| of those, guard rows for a branch | %d |"
                 % document["counts"]["guard_rows_total"])
    lines.append("| of those, value cells for a flag consumer | %d |"
                 % document["counts"]["flag_consumer_rows"])
    unplaced = 0
    for cause in document["attestation_unclassified"]:
        unplaced = unplaced + document["attestation_unclassified"][cause]
    lines.append("| arch-opcode rows placed into a cell | %d |"
                 % (document["counts"]["attested_ledger_rows"]
                    - unplaced))
    lines.append("| attested cells that land on a TRANSLATED row | %d |"
                 % document["counts"]["attested_cells_placed"])
    lines.append("")
    lines.append("Table 2 — the rows the classifier could not place, "
                 "by cause.")
    lines.append("")
    lines.append("| cause | rows | an example line |")
    lines.append("|---|---|---|")
    causes = document["attestation_unclassified"]
    examples = document["attestation_unclassified_example"]
    for cause in sorted(causes, key=lambda c: (-causes[c], c)):
        example = examples.get(cause, "")
        lines.append("| %s | %d | `%s` |" % (cause, causes[cause],
                                             example))
    lines.append("")


def write_report_edges(lines, document):
    lines.append("## 4. The equivalences, REPORTED and never applied")
    lines.append("")
    lines.append("Table 3 — the same-builder groups and z3's verdicts "
                 "over their cells. A cell is one (pair, shape, width) "
                 "at which both mnemonics carry a TRANSLATED row; the "
                 "verdict words are z3's own (`unsat` = no differing "
                 "point exists, `sat` = one does, `unknown` = the "
                 "3,000 ms ceiling).")
    lines.append("")
    lines.append("| group | members | cells | equal everywhere | not "
                 "equal | alias group |")
    lines.append("|---|---|---|---|---|---|")
    for group in document["counts"]["alias_groups"]:
        members = []
        for member in group["members"]:
            members.append("`%s`" % member["mnem"])
        lines.append("| %s | %s | %d | %d | %d | %s |"
                     % (group["group_id"], " ".join(members),
                        group["cells"],
                        group["cells_equal_everywhere"],
                        group["cells_not_equal"],
                        group["is_an_alias_group"]))
    lines.append("")
    lines.append("Table 4 — the pair the brief names, decided the same "
                 "way. These two do not share a builder, so this is "
                 "not a `same_builder` edge.")
    lines.append("")
    lines.append("| shape | width | destination | flags | left writes "
                 "flags | right writes flags |")
    lines.append("|---|---|---|---|---|---|")
    for cell in document["named_pair_cells"]:
        lines.append("| %s | %s | %s | %s | %s | %s |"
                     % (cell["shape"], cell["width"],
                        cell.get("destination_verdict")
                        or cell.get("destination_refusal"),
                        cell.get("flags_verdict")
                        or cell.get("flags_refusal"),
                        cell["left_writes_flags"],
                        cell["right_writes_flags"]))
    lines.append("")


def write_report_counts(lines, document):
    counts = document["counts"]
    lines.append("## 5. The counts, beside the 162")
    lines.append("")
    lines.append("| what | count |")
    lines.append("|---|---|")
    lines.append("| table mnemonics | %d |" % counts["table_mnemonics"])
    lines.append("| corpus mnemonics | %d |"
                 % counts["corpus_mnemonics"])
    lines.append("| in both | %d |" % counts["in_both"])
    lines.append("| table only | %d |" % len(counts["table_only"]))
    lines.append("| corpus only | %d |" % len(counts["corpus_only"]))
    lines.append("| rows TRANSLATED | %d |" % counts["rows_translated"])
    lines.append("| distinct mappings after `identical_text` | %d |"
                 % counts["distinct_mappings_after_identical_text"])
    lines.append("| `identical_text` pairs | %d |"
                 % counts["identical_text_pairs"])
    lines.append("| distinct (mnem, shape, key_width) triples with a "
                 "TRANSLATED row | %d |" % counts["translated_triples"])
    lines.append("| attested cells | %d |" % counts["attested_cells"])
    lines.append("| attested cells that land on a TRANSLATED row | %d |"
                 % counts["attested_cells_placed"])
    lines.append("| attested cells with no TRANSLATED row | %d |"
                 % len(counts["attested_cells_with_no_translated_row"]))
    lines.append("| corpus mnemonics with at least one placed cell | "
                 "%d |" % counts["mnemonics_with_a_placed_cell"])
    lines.append("| guard rows, over the branch mnemonics | %d |"
                 % counts["guard_rows_total"])
    lines.append("")
    lines.append("`identical_text` is textual identity after "
                 "normalisation, which is an UNDER-COUNT of true "
                 "equivalence: two rows can compute one function and "
                 "print differently, and only a solver call decides "
                 "that. The %d pairs are written as the %d equivalence "
                 "CLASSES they form, keyed by row ids "
                 "(`identical_text_classes`), because textual identity "
                 "is an equivalence relation and the classes carry the "
                 "same information as the pairs."
                 % (counts["identical_text_pairs"],
                    len(document["identical_text_classes"])))
    lines.append("")
    lines.append("Table only, LITERAL: %s"
                 % listed(counts["table_only"]))
    lines.append("")
    lines.append("Corpus only, LITERAL: %s"
                 % listed(counts["corpus_only"]))
    lines.append("")
    lines.append("Table 5 — the SPLITS: the mnemonics whose TRANSLATED "
                 "rows do not all write the same multiset of place "
                 "KINDS, which is the split the ruling of 2026-09-08 "
                 "names read mechanically (one-operand `imul` writes "
                 "two registers, the accumulator pair; two-operand "
                 "`imul` writes one register and the flags). The last "
                 "two columns are the finer readings, before the kind "
                 "abstraction and then over destination texts; both "
                 "are larger by construction.")
    lines.append("")
    lines.append("| mnem | place kind sets | place-name sets | "
                 "destination texts |")
    lines.append("|---|---|---|---|")
    for record in counts["mnemonics_with_several_mappings"]:
        sets = []
        for one in record["place_kind_sets"]:
            sets.append("`%s`" % one)
        lines.append("| `%s` | %s | %d | %d |"
                     % (record["mnem"], " / ".join(sets),
                        record["distinct_place_sets"],
                        record["distinct_destination_texts"]))
    lines.append("")
    lines.append("Table 6 — the (mnem, shape, width) cells the corpus "
                 "attests for which the table carries no TRANSLATED "
                 "row. The sweep spells vector operands at the four "
                 "general-register widths only, so a corpus row at a "
                 "128-bit vector width has no cell of its own in the "
                 "table.")
    lines.append("")
    lines.append("| mnem | shape | width | ledger rows | units |")
    lines.append("|---|---|---|---|---|")
    for cell in counts["attested_cells_with_no_translated_row"]:
        lines.append("| `%s` | %s | %s | %d | %d |"
                     % (cell["mnem"], cell["shape"], cell["width"],
                        cell["ledger_rows"], cell["units"]))
    lines.append("")


def listed(records):
    if not records:
        return "(none)"
    out = []
    for record in records:
        out.append("`%s`" % record["mnem"])
    return " ".join(out)


def write_report_width_rule(lines, document):
    lines.append("## 7. The one width rule, `key_width`")
    lines.append("")
    lines.append("**What it is, one sentence.** `key_width` is the "
                 "width the JOIN between the table's rows and the "
                 "corpus's attestation is keyed by -- the operation's "
                 "own lane width as the reference's own tables state "
                 "it -- as against the field `width`, which stays what "
                 "it always was: the loop variable on a sweep row, and "
                 "the operand register's width or the ledger row's "
                 "byte size on an attested cell.")
    lines.append("")
    lines.append("Why it exists: the two sides did not spell `width` "
                 "the same way for a vector or an x87 operand. The "
                 "corpus said `addss xmm_xmm 128` (its ledger row "
                 "holds sixteen bytes) where the table said 8, 16, 32 "
                 "and 64 (the four general-register widths the sweep's "
                 "loop walks), and `addss` adds one 32-bit lane, which "
                 "is neither number.")
    lines.append("")
    lines.append("Table 7 — the rule, LITERAL, and where each number "
                 "is read from. `model_table.key_width` is the one "
                 "function; both sides call it.")
    lines.append("")
    lines.append("| the mnemonic is | `key_width` | read from |")
    lines.append("|---|---|---|")
    lines.append("| an x87 mnemonic (`ledger48.x87_base` names it) | 80"
                 " | the x87 register's own width, `reference."
                 "X87_SORT` = `z3.FPSort(15, 64)` |")
    lines.append("| in `reference.FLOAT_BINARY` | 32 or 64 | the "
                 "table's own second field |")
    lines.append("| in `reference.FLOAT_COMPARE_MASK` | 32 or 64 | the "
                 "table's own second field |")
    lines.append("| in `reference.CONVERT_TO_FLOAT` | 32 or 64 | the "
                 "table's own value (the destination lane) |")
    lines.append("| in `reference.LANE_MOVE` | 32 or 64 | the table's "
                 "own value |")
    lines.append("| in `reference.FLOAT_FLAG_ONLY` | 32 or 64 | "
                 "`build_float_flag_only`'s own line, `width = 32 if "
                 "ops.mnemonic.endswith(\"ss\") else 64` |")
    lines.append("| `cvtss2sd` | 64 | `build_convert_widen`'s own "
                 "`FLOAT_SORT[64]` |")
    lines.append("| in `reference.PACKED_FLOAT`, `BITWISE_128` or "
                 "`WHOLE_MOVE` | 128 | the whole vector register |")
    lines.append("| one of the six further whole-register vector "
                 "mnemonics (`model_table.FURTHER_WHOLE_REGISTER`) | "
                 "128 | each builder's own `ops.read_128` |")
    lines.append("| anything else | the row's own `width` | unchanged "
                 "|")
    lines.append("")
    merges = document["counts"]["attestation_width_merges"]
    lines.append("Table 8 — the cells where the one rule MERGES more "
                 "than one of the classifier's own widths under a "
                 "single `key_width`, listed so the merge is visible. "
                 "The convert family is the case: what varies between "
                 "its two forms is the SOURCE width, and the rule "
                 "reads the destination lane, so both forms land on "
                 "one key. The sweep's own `width` sits beside "
                 "`key_width` on every row, so nothing is lost.")
    lines.append("")
    lines.append("| mnem | shape | key_width | the classifier's widths "
                 "|")
    lines.append("|---|---|---|---|")
    for record in merges:
        widths = []
        for width in record["classifier_widths"]:
            widths.append(str(width))
        lines.append("| `%s` | %s | %s | %s |"
                     % (record["mnem"], record["shape"],
                        record["key_width"], " ".join(widths)))
    if not merges:
        lines.append("| (none) | | | |")
    lines.append("")


def write_report_coverage(lines, document):
    lines.append("## 8. The coverage table: one row per corpus "
                 "mnemonic")
    lines.append("")
    lines.append("Every one of the corpus's 162 mnemonics sits in "
                 "exactly ONE of four categories, so the four counts "
                 "sum to 162.")
    lines.append("")
    lines.append("Table 9 — the four categories and their totals.")
    lines.append("")
    lines.append("| category | mnemonics |")
    lines.append("|---|---|")
    for record in document["counts"]["coverage_totals"]:
        lines.append("| %s | %d |" % (record["category"],
                                      record["mnemonics"]))
    lines.append("")
    lines.append("Table 10 — one row per corpus mnemonic. `placed` is "
                 "the count of that mnemonic's attested value cells "
                 "that land on a TRANSLATED row of the table; "
                 "`unspelled` the count that land on none; `guard` the "
                 "ledger's GUARD-block rows that name it as the "
                 "reading half of a flag pair; `flag pair` the ledger "
                 "rows of its value cells that came from a flag pair "
                 "rather than from an arch-opcode row.")
    lines.append("")
    lines.append("| mnem | placed | unspelled | guard | ledger rows | "
                 "flag pair | category | cause, quoted |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for record in document["counts"]["coverage"]:
        reason = record.get("reason") or ""
        reason = reason.replace("|", "\\|")
        lines.append("| `%s` | %d | %d | %d | %d | %d | %s | %s |"
                     % (record["mnem"],
                        record["attested_value_cells_placed"],
                        record["attested_value_cells_at_an_unspelled"
                               "_form"],
                        record["attested_by_guard_rows"],
                        record["ledger_rows"],
                        record["flag_pair_rows"],
                        record["category"], reason))
    lines.append("")


def write_report_guard_rows(lines, document):
    lines.append("## 9. The control transfers, and the guard rows that "
                 "attest them")
    lines.append("")
    lines.append("A conditional transfer writes no value: the "
                 "reference's entry for it writes %r, the fork the "
                 "walk takes. So it can carry no value cell by nature, "
                 "and the ledger attests it in a different population "
                 "-- the GUARD block, where the producer is the PAIR "
                 "(flag-setting opcode, flag-reading opcode) and this "
                 "mnemonic is the reading half. An UNCONDITIONAL "
                 "transfer produces no ledger row of any kind, and its "
                 "count is 0 by nature rather than by omission."
                 % R.THE_BRANCH_CONDITION)
    lines.append("")
    lines.append("Table 11 — the guard rows, per branch mnemonic, with "
                 "the flag-setting mnemonics whose flags it read.")
    lines.append("")
    lines.append("| mnem | guard rows | units | an example line | the "
                 "setters, with their row counts |")
    lines.append("|---|---|---|---|---|")
    for record in document["counts"]["guard_rows"]:
        setters = []
        for one in sorted(record["setter"],
                          key=lambda s: -s["ledger_rows"]):
            setters.append("`%s` %d" % (one["mnem"], one["ledger_rows"]))
        lines.append("| `%s` | %d | %d | `%s` | %s |"
                     % (record["mnem"], record["guard_rows"],
                        record["units"], record.get("text") or "",
                        " ".join(setters)))
    lines.append("")


def write_report_causes(lines, document):
    lines.append("## 6. NO_BUILDER and NOT_MODELLED, by cause")
    lines.append("")
    for outcome in sorted(document["causes"]):
        lines.append("### %s" % outcome)
        lines.append("")
        lines.append("| rows | cause, quoted from the sweep row |")
        lines.append("|---|---|")
        for record in document["causes"][outcome]:
            text = record["reason"].replace("|", "\\|")
            lines.append("| %d | %s |" % (record["count"], text))
        lines.append("")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    command = argv[1]
    if command == "sweep":
        return sweep_command()
    if command == "attest":
        return attest_command()
    if command == "edges":
        sample = None
        if "--sample" in argv:
            sample = int(argv[argv.index("--sample") + 1])
        return edges_command(sample)
    if command == "assemble":
        return assemble_command()
    if command == "report":
        return report_command()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
