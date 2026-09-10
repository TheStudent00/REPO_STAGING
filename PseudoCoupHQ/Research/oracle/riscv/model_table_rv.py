#!/usr/bin/env python3
"""model_table_rv.py -- THE RISC-V MODEL TABLE: one row per (`mnem`,
operand shape, `key_width`) the RISC-V reference models, with the z3 term
each written place receives.

Node: hq.research.arch_unit_oracle.  Task rv2, brief section 2 step 1,
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

WHAT THIS IS, one sentence, in relation: the riscv64 twin of
`PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py`
-- the same sweep, over `riscv_reference.py`'s own opcode table instead of
`op_pipeline/reference.py`'s, writing rows of the same shape so the two
tables' cells can be matched term against term.

THE OBJECTS, one sentence each.
  * A CELL is one (`mnem`, operand shape, `key_width`) row: the
    reference's mapping of that instruction at that operand form and
    width, as a z3 term per written place.
  * AN OPERAND SHAPE is one legal way to spell an instruction's operands
    -- a PROBE, not a meaning.  The reference's own builder decides
    whether it models the spelling; a refusal is recorded by name.
  * `key_width` is the width the operation itself computes at, read off
    the reference's own tables and never guessed: 32 for the `w` forms
    (which compute at 32 and sign-extend into the whole register), the
    float family's own 32 or 64, the load/store access width, and 64
    otherwise.

WHAT IS DIFFERENT FROM THE x86 SWEEP, and each is a fact of the
architecture:
  * THERE IS NO FLAGS PLACE.  x86's sweep records a `flags` place on
    almost every row; nothing here writes one.  The one non-register
    place a RISC-V instruction leaves is the BRANCH CONDITION, which the
    six branches compute inside themselves.
  * THE WIDTH IS IN THE MNEMONIC, not in the operand spelling.  x86
    sweeps four operand widths per shape because `%dil`, `%di`, `%edi`
    and `%rdi` are four spellings of one register; RISC-V has no
    sub-register names, so one mnemonic has exactly one width.
  * THE SYMBOLIC IMMEDIATE CANNOT BE SPELLED.  x86's sweep gained four
    `imm_symbolic_*` shapes (task ap5) by putting a register in the
    immediate's slot, because `reference.Operands.read_text` reads the
    two the same way.  `riscv_reference.Operands.immediate` REFUSES a
    non-literal, so this sweep records the refusal by name rather than
    changing a file task rv1 closed.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope, anywhere
in this line -- not in matching, not in "which pairs get compared", not in
report rows, not in dropdowns.  The candidate set for comparison comes from
machine-form evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token.  The token appears exactly once per
unit: as a display label on the member.  HISTORY OF VIOLATIONS, so the
pattern is visible: (1) the arch campaign's cross-language matrix (caught
by the owner 2026-08-24); (2) verdicts.py's row pairing (caught by the owner
2026-08-25 -- the fix brief itself reintroduced it as "same-operator
pairs").  MECHANICAL GUARD REQUIRED: every pipeline stage that groups or
pairs units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste this
paragraph verbatim."

HOW THIS FILE OBEYS IT.  Every field that carries a mnemonic is named
`mnem`, which the guard reads as a machine form (the ruling of
2026-09-08); a list of mnemonics is a list of records each carrying
`mnem`, never a list of bare strings.  No operator token of any probe
manifest is read here at all.

Coding discipline (the owner's ruling): no complex/compound one-liner statements.

usage:
  model_table_rv.py sweep <op_pipeline dir> <out prefix>
  model_table_rv.py report <out prefix>
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import riscv_reference as RV                                # noqa: E402
import z3                                                    # noqa: E402


ABORT_KB = 6 * 1024 * 1024
ABORT_NAME = "ABORT_MEMORY_RV2"


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check_memory(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("%s: %d kB at %s" % (ABORT_NAME, peak, where))


def say(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def write_json(path, document):
    fh = open(path, "w")
    json.dump(document, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()


# ==================================================================
# section 0: THE ONE WIDTH RULE -- `key_width`
# ==================================================================
#
# `key_width` is the width the JOIN is keyed by: the operation's own
# lane width, as the reference's own tables state it.  The x86 table
# needs a function of (mnem, width) because its sweep walks four
# operand widths per shape; RISC-V's width is in the mnemonic, so this
# is a function of the mnemonic alone and every branch of it names the
# reference table it reads.

WIDTH_32_FAMILIES = ("R_TYPE_W", "I_TYPE_W", "SHIFT_I_W", "MULTIPLY_W",
                     "DIVIDE_W")
"""the `w` forms: the builder computes at 32 bits and calls
`sign_extend_w` to place the result in the whole register."""


def key_width(mnem):
    """the width this instruction computes at, read off the reference."""
    if mnem in RV.R_TYPE_W:
        return 32
    if mnem in RV.I_TYPE_W:
        return 32
    if mnem in RV.SHIFT_I_W:
        return 32
    if mnem in RV.MULTIPLY_W:
        return 32
    if mnem in RV.DIVIDE_W:
        return 32
    if mnem in RV.UPPER:
        return 32
    if mnem in RV.LOAD:
        return RV.LOAD[mnem][0]
    if mnem in RV.STORE:
        return RV.STORE[mnem]
    if mnem in RV.FLOAT_BINARY:
        return RV.FLOAT_BINARY[mnem][1]
    if mnem in RV.FLOAT_FROM_INTEGER:
        return RV.FLOAT_FROM_INTEGER[mnem][0]
    if mnem in RV.FLOAT_WIDEN:
        return RV.FLOAT_WIDEN[mnem][1]
    if mnem in RV.FLOAT_MOVE:
        return RV.FLOAT_MOVE[mnem][1]
    if mnem in RV.FLOAT_COMPARE:
        return RV.FLOAT_COMPARE[mnem][1]
    if mnem in RV.FLOAT_LOAD:
        return RV.FLOAT_LOAD[mnem]
    if mnem in RV.FLOAT_STORE:
        return RV.FLOAT_STORE[mnem]
    return 64


WIDTH_RULE = (
    "the width the instruction computes at, read off riscv_reference's "
    "own tables: 32 for R_TYPE_W / I_TYPE_W / SHIFT_I_W / MULTIPLY_W / "
    "DIVIDE_W / UPPER (the builders that compute at 32 and place the "
    "result through sign_extend_w); the LOAD and STORE access width; "
    "the float family's own width from FLOAT_BINARY, "
    "FLOAT_FROM_INTEGER, FLOAT_WIDEN, FLOAT_MOVE, FLOAT_COMPARE, "
    "FLOAT_LOAD and FLOAT_STORE; 64 otherwise, which is the whole "
    "register")


# ==================================================================
# section 1: THE OPERAND SHAPES THE SWEEP TRIES
# ==================================================================
#
# These are PROBES, not semantics.  `a0` is the destination and `a1`,
# `a2` the sources, so the shape names read destination-first exactly as
# the disassembler prints RISC-V.  `0x3` is the same literal the x86
# sweep spells `$0x3`, so a literal-immediate cell of one architecture
# and a literal-immediate cell of the other carry the same constant and
# can be compared as terms.

GPR_D = "a0"
GPR_1 = "a1"
GPR_2 = "a2"
FPR_D = "fa0"
FPR_1 = "fa1"
FPR_2 = "fa2"
IMMEDIATE = "0x3"
MEMORY = "0x0(a1)"

SHAPES = [
    ("gpr_gpr_gpr", [GPR_D, GPR_1, GPR_2]),
    ("gpr_gpr_same", [GPR_D, GPR_1, GPR_1]),
    ("gpr_gpr_imm", [GPR_D, GPR_1, IMMEDIATE]),
    ("gpr_gpr_symbolic_imm", [GPR_D, GPR_1, GPR_2]),
    ("gpr_imm", [GPR_D, IMMEDIATE]),
    ("gpr_mem", [GPR_D, MEMORY]),
    ("gpr_gpr", [GPR_D, GPR_1]),
    ("fpr_fpr_fpr", [FPR_D, FPR_1, FPR_2]),
    ("fpr_fpr", [FPR_D, FPR_1]),
    ("fpr_gpr", [FPR_D, GPR_1]),
    ("gpr_fpr", [GPR_D, FPR_1]),
    ("gpr_fpr_fpr", [GPR_D, FPR_1, FPR_2]),
    ("fpr_mem", [FPR_D, MEMORY]),
    ("none", []),
]

SYMBOLIC_IMMEDIATE_SHAPE = "gpr_gpr_symbolic_imm"
"""the shape whose third operand stands in for a FREE immediate.

x86's sweep spells it by putting a register in the immediate's slot,
because `reference.Operands.read_text` reads a register and an immediate
the same way.  `riscv_reference.Operands.immediate` does not: it REFUSES
a non-literal by name.  So this shape is attempted only where the
instruction's builder actually READS an immediate -- machine-form
evidence off the builder's own source, `ops.immediate(` in its text, and
never a reading of the mnemonic -- and every such attempt records the
reference's own refusal.  Where the builder reads no immediate the row
is NOT_SPELLED: the register form is already the row above it, and a
second identical spelling would be a second cell for one mapping."""

IMMEDIATE_MARK = "ops.immediate("
"""what a builder's source says when it reads an immediate operand."""


def reads_an_immediate(entry):
    if entry.build is None:
        return False
    import inspect
    try:
        source = inspect.getsource(entry.build)
    except Exception:
        return False
    return IMMEDIATE_MARK in source


# ==================================================================
# section 2: RUN one line on a fresh state, and read what changed
# ==================================================================

NAME_OF_INDEX = {}
for _name, _index in RV.INTEGER_REGISTERS.items():
    if _name.startswith("x"):
        continue
    if _index in NAME_OF_INDEX:
        continue
    NAME_OF_INDEX[_index] = _name

FLOAT_NAME_OF_INDEX = {}
for _name, _index in RV.FLOAT_REGISTERS.items():
    if _name.startswith("f") and _name[1:].isdigit():
        continue
    if _index in FLOAT_NAME_OF_INDEX:
        continue
    FLOAT_NAME_OF_INDEX[_index] = _name


def register_name(index):
    return NAME_OF_INDEX.get(index, "x%d" % index)


def float_name(index):
    return FLOAT_NAME_OF_INDEX.get(index, "f%d" % index)


def run_line(reference, mnem, texts):
    """one instruction on a fresh state.

    Returns (written places -> term, the branch condition or nothing,
    the line as the reference was handed it).  A fresh state seeds every
    register the builder reads as a free symbol, so what the line leaves
    behind is already the instruction's generic mapping.  A register or
    memory cell whose term after the line is character-for-character its
    own arrival symbol was READ, not written, and is dropped -- the same
    correction the x86 sweep makes in `model_translate.run_line` and
    `model_table.drop_cells_only_read`.
    """
    state = RV.MachineState({})
    line = mnem
    if texts:
        line = "%s %s" % (mnem, ", ".join(texts))
    reference.step(state, line)
    written = {}
    for index, term in state.registers.items():
        seed = state.shared_seed.get("seed_x%d" % index)
        if seed is not None and term.sexpr() == seed.sexpr():
            continue
        written["reg_%s" % register_name(index)] = term
    for index, term in state.fregisters.items():
        seed = state.shared_seed.get("seed_f%d" % index)
        if seed is not None and term.sexpr() == seed.sexpr():
            continue
        written["freg_%s" % float_name(index)] = term
    for text, term in state.memory.items():
        name = RV.memory_symbol_name(text)
        seed = state.shared_seed.get(name)
        if seed is not None and term.sexpr() == seed.sexpr():
            continue
        written["mem_%s" % name] = term
    return written, state.branch_condition, line


# ==================================================================
# section 3: THE ROWS
# ==================================================================

def rows_of(reference, normaliser):
    """one row per (mnemonic, shape) the sweep attempts."""
    table = reference.opcode_table
    out = []
    index = 0
    names = sorted(table.entries)
    for mnem in names:
        entry = table.entries[mnem]
        for shape, texts in SHAPES:
            row = one_attempt(reference, normaliser, entry, mnem, shape,
                              texts, index)
            out.append(row)
            index = index + 1
        check_memory("after %s" % mnem)
    return out


def one_attempt(reference, normaliser, entry, mnem, shape, texts, index):
    row = {
        "row_id": "rv%05d" % index,
        "mnem": mnem,
        "shape": shape,
        "key_width": key_width(mnem),
        "operands": list(texts),
        "reads": list(entry.reads),
        "writes": list(entry.writes),
        "builder": builder_name(entry),
        "condition": partial_region(entry),
    }
    if entry.cause is not None:
        row["entry_note"] = entry.cause
    if entry.build is None:
        row["outcome"] = "NO_BUILDER"
        row["reason"] = entry.cause or "this entry states no mapping"
        return row
    if shape == SYMBOLIC_IMMEDIATE_SHAPE and not reads_an_immediate(entry):
        row["outcome"] = "NOT_SPELLED"
        row["reason"] = ("this builder's own source reads no immediate "
                         "operand, so a register in the immediate's slot "
                         "is not a second spelling of anything -- it is "
                         "the register form already recorded on the "
                         "gpr_gpr_gpr row")
        return row
    try:
        written, condition, line = run_line(reference, mnem, texts)
    except Exception as problem:
        row["outcome"] = "REFUSED"
        row["reason"] = "%s: %s" % (type(problem).__name__, problem)
        return row
    row["outcome"] = "TRANSLATED"
    row["text"] = line
    row["mapping"] = []
    for place in sorted(written):
        row["mapping"].append({
            "writes": place,
            "text": normalised(normaliser, written[place]),
        })
    if condition is not None:
        row["mapping"].append({
            "writes": "branch_condition",
            "text": normalised(normaliser, z3.If(
                condition, z3.BitVecVal(1, RV.XLEN),
                z3.BitVecVal(0, RV.XLEN))),
        })
    if not row["mapping"]:
        row["reason"] = ("the line ran and left no place changed -- "
                         "every place it touched held its own arrival "
                         "value before and after, which is a read and "
                         "not a write")
    return row


def normalised(normaliser, term):
    return normaliser.normalize(term)


def builder_name(entry):
    if entry.build is None:
        return None
    return entry.build.__name__


CONDITION_MARKS = ("raise NotModeled(", "shift_amount(", "z3.If(")

TOTAL_ON_BIT_PATTERNS = (
    "total on bit patterns: this builder's own source states no "
    "refusal, no hardware mask and no branch on an operand value")


def partial_region(entry):
    """the condition this instruction's builder states, quoted from the
    builder's own source, or the sentence that says there is none.

    The three marks are the x86 table's own three, with the mask named
    by RISC-V's own spelling (`shift_amount`, where x86 spells
    `shift_mask`)."""
    if entry.build is None:
        return "no builder: this entry states no mapping at all"
    import inspect
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


# ==================================================================
# section 4: THE COMMANDS
# ==================================================================

def sweep_command(op_dir, prefix):
    reference = RV.RiscvReference()
    sys.path.insert(0, op_dir)
    import term as TERMS                                    # noqa: E402
    import reference as X86                                 # noqa: E402
    normaliser = TERMS.Term(X86.Reference())
    say("[1/3] the sweep over riscv_reference's opcode table")
    rows = rows_of(reference, normaliser)
    say("   %d attempts" % len(rows))
    say("[2/3] the census of outcomes")
    census = {}
    for row in rows:
        census[row["outcome"]] = census.get(row["outcome"], 0) + 1
    for outcome in sorted(census):
        say("   %-24s %d" % (outcome, census[outcome]))
    cells = {}
    for row in rows:
        if row["outcome"] != "TRANSLATED":
            continue
        cells[(row["mnem"], row["shape"], row["key_width"])] = True
    say("   distinct cells (mnem, shape, key_width): %d" % len(cells))
    say("[3/3] writing")
    document = {
        "meta": {
            "task": "rv2",
            "what": "one row per (mnem, operand shape, key_width) the "
                    "RISC-V reference models, with the z3 term each "
                    "written place receives, printed by term.Term."
                    "normalize (the pipeline's layer-5 rule)",
            "reference": "Research/oracle/riscv/riscv_reference.py, "
                         "task rv1, read and called and not changed",
            "width_rule": WIDTH_RULE,
            "shape_note": "the operand shapes are probes, not meanings; "
                          "the reference's own builder decides whether "
                          "it models a spelling and a refusal is "
                          "recorded by name",
            "no_flags": "there is no flags place anywhere in this "
                        "table: the architecture has no flags register",
            "peak_kb": peak_kb(),
            "memory_bound_kb": ABORT_KB,
            "memory_abort": ABORT_NAME,
        },
        "rows": rows,
    }
    write_json(prefix + ".json", document)
    say("peak RSS: %d kB" % peak_kb())
    return 0


def report_command(prefix):
    document = json.load(open(prefix + ".json"))
    rows = document["rows"]
    lines = []
    lines.append("# model_table_rv.md -- the RISC-V arch-instruction "
                 "model table")
    lines.append("")
    lines.append("Task rv2, node `hq.research.arch_unit_oracle`. Written "
                 "by `model_table_rv.py`; never hand-edited.")
    lines.append("")
    lines.append("**What this table is, one sentence.** Every mapping "
                 "`riscv_reference.py`'s `opcode_table` holds, one row "
                 "per (`mnem`, operand shape, `key_width`) the sweep in "
                 "this file spells, with the z3 term each written place "
                 "receives printed by the pipeline's layer-5 rule "
                 "(`term.Term.normalize`). Every term below is LITERAL.")
    lines.append("")
    census = {}
    for row in rows:
        census[row["outcome"]] = census.get(row["outcome"], 0) + 1
    cells = {}
    mnems = {}
    for row in rows:
        mnems[row["mnem"]] = True
        if row["outcome"] != "TRANSLATED":
            continue
        cells[(row["mnem"], row["shape"], row["key_width"])] = True
    lines.append("Table 1 -- the sweep's own counts.")
    lines.append("")
    lines.append("| what | count |")
    lines.append("|---|---|")
    lines.append("| sweep attempts | %d |" % len(rows))
    for outcome in sorted(census):
        lines.append("| rows %s | %d |" % (outcome, census[outcome]))
    lines.append("| table mnemonics | %d |" % len(mnems))
    lines.append("| distinct cells | %d |" % len(cells))
    lines.append("")
    lines.append("The one width rule, LITERAL from the json's `meta`: %s"
                 % document["meta"]["width_rule"])
    lines.append("")
    lines.append("Table 2 -- every TRANSLATED cell, with the term of "
                 "every place it writes.")
    lines.append("")
    lines.append("| `mnem` | shape | `key_width` | writes | term |")
    lines.append("|---|---|---|---|---|")
    seen = {}
    for row in rows:
        if row["outcome"] != "TRANSLATED":
            continue
        key = (row["mnem"], row["shape"], row["key_width"])
        if key in seen:
            continue
        seen[key] = True
        for place in row["mapping"]:
            lines.append("| `%s` | %s | %d | `%s` | `%s` |"
                         % (row["mnem"], row["shape"], row["key_width"],
                            place["writes"], place["text"]))
    lines.append("")
    fh = open(prefix + ".md", "w")
    fh.write("\n".join(lines) + "\n")
    fh.close()
    say("wrote %s.md, %d lines" % (prefix, len(lines)))
    return 0


def main():
    command = sys.argv[1]
    if command == "sweep":
        return sweep_command(sys.argv[2], sys.argv[3])
    if command == "report":
        return report_command(sys.argv[2])
    raise SystemExit("unknown command %r" % command)


if __name__ == "__main__":
    sys.exit(main())
