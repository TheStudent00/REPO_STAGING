#!/usr/bin/env python3
"""canonical_form.py -- THE CANONICAL FORM.

The code of node `hq.research.compiler_graph.canonical_form`
(`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md`).
Its class is `CanonicalForm`; its methods are the CORE's `methods:`
(`wrap`, `assemble`, `refuse`); its attributes are the CORE's
`attributes:` (`block_order`, `wrapped_text`).  Its four realized
sub-nodes are the four classes `Prelude`, `Epilogue`, `Labels` and
`Refuse`, held on the instance as `self.prelude`, `self.epilogue`,
`self.labels` and `self.refusal`.

TASK 60, round 12 (log_158).  Binding rule 1 of the round: the code
carries the node's name.  This module therefore IMPORTS NOTHING FROM
`ledger47.py`, `ledger48.py`, `gate48.py`, or any `canon37_*` /
`canon38_*` driver.  Those are superseded records: never edited, never
imported.  What this module DOES import is the three modules this
round landed, each carrying its own node's name:

  * `ledger.py`   -- node 0_3_5_3, task 59 (log_161).  `Ledger`,
                     `Row`, `Producer`, `DESTINATION_RULES`,
                     `FLAG_RULES`, `positional_labels`, `weave`,
                     `Refusal`.
  * `gate.py`     -- node 0_3_5_5, task 58 (log_160).  `Gate`,
                     `Verdict`.
  * `reference.py`-- node 0_3_5_4, task 57 (log_159), reached only
                     through `gate.py`.

--------------------------------------------------------------------
WHAT IS NEW HERE, AND NOTHING ELSE
--------------------------------------------------------------------

THE PRELUDE EMITS IN ARRIVAL-CONTRACT ORDER.

`ledger48.build_prelude`, and the copy of it `ledger.py` carries
unchanged, sorts the arrival families VECTOR FIRST and then GENERAL,
and numbers the IN rows in that sorted order.  `walk_dataflow` and the
`arrival_contract_bindings` the drivers record bind `IN-i` to
`arrival_families[i]` -- the contract's own order.  The two orders
differ for every unit that has BOTH a vector arrival and a general
arrival.  log_153 section 9 printed the disagreement on `c/op_105` and
declined to choose; the CORE chose, 2026-09-03:

    "IN rows are numbered in `arrival_contract` order, and the prelude
    emits in that same order.  The prelude's vector-first ordering
    (log_153 section 9) is a defect against this line."
    -- CORE_0_3_5_2_canonical_form.md, settled rules

    "The prelude emits in arrival_contract order -- IN-0 first,
    whichever family that is.  Emitting the vector arrivals first is a
    defect, not an alternative order."
    -- CORE_0_3_5_2_2_prelude.md, design rule 5

So `Prelude.emit` walks `arrival_contract` in its own order and emits
one load per family in that order.  Nothing else about the load
changes: it is still the two-step load through the ledger, the general
destination is still the pointer for its own first step, and a vector
row is still moved with `movdqu` through one general scratch that is
not an arrival family.

THE ORDER IS SAFE, said rather than assumed.  A vector load's scratch
is picked against the set of GENERAL ARRIVAL FAMILIES and the
never-rename set, so it is never a register a previous load has
already filled with an arrival value, whichever order the loads run
in.  A general load uses its own destination as its pointer, so it
touches nothing else.  Therefore reordering the loads cannot make one
load destroy another's result.  This is structural check C2, which
`gate.py` runs per unit.

--------------------------------------------------------------------
WHAT IS DELEGATED RATHER THAN COPIED, said out loud
--------------------------------------------------------------------

The epilogue and the label rewrite are UNCHANGED by this task.  Their
logic lives in `ledger.py` (`Ledger.build_epilogue`,
`positional_labels`), which copied it from the superseded record with
that fact stated on each section.  Copying it a second time into this
file would put two texts of one rule on disk, and a rule with two
texts drifts.  So `Epilogue` and `Labels` here are the node's SHAPE --
the CORE's named methods -- and each method calls the one text in
`ledger.py`.  The shape is this node's; the logic is the one logic.

`wrap` is `ledger.Ledger.wrap_unit`'s sequence with the prelude call
replaced by this file's `Prelude.emit`, because the prelude is a
sub-node of THIS node, not of the ledger.

--------------------------------------------------------------------
WHERE THE ARCH-UNIT FACTS COME FROM
--------------------------------------------------------------------

Reading a unit's body, its arrival contract and its answer home is
node 0_3_5_1 (`arch_unit`), not this node, and that reading was done
and recorded in round 11.  This file therefore takes those facts from
the RECORDED ARTIFACTS of canon38 -- data files, not code -- and
re-renders every one of the 31,078 units from them.  A data file is a
record; reading it is not importing a superseded module.  The fields
read per unit are exactly: `body_text`, `body_bytes`, `body_source`,
`arrival_families`, `entry_contract`, `result_family`,
`result_width`, `lang`, `n`, `population`, `operator` (a display
label, read by nothing).

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

No operator token appears in this file.  The selection of what to
render is the corpus files on disk; the operator field travels as a
display label on the member and is read by nothing.

Coding discipline: no compound one-liner statements.

usage:
  canonical_form.py --population original [--limit N] [--fresh]
  canonical_form.py --population interpreter
  canonical_form.py --population regenerated [--limit N]
  canonical_form.py --assemble [--stride 30]
  canonical_form.py --defect-census
  canonical_form.py --show-op-105
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ledger as L                                                # noqa: E402
import gate as GATE                                               # noqa: E402
import canon                                                      # noqa: E402


LANGS = ["c", "cpp", "go", "rust", "swift"]
CHECKPOINT_EVERY = 200

FORM_NAME = "canonical_form"

# THE ARTIFACT PREFIX.  `canon39` is round 13's render (task 60);
# `--prefix canon40` is task 78's, rendered with the CORRECTED runtime
# destination rule of `CORE_0_3_5_3_3_destination_rules.md` rule 4.
# The arch-unit facts are read from the canon38 records either way:
# a render always starts from the recorded facts, never from another
# render.
PREFIX = "canon39"


def out_path(name):
    return os.path.join(HERE, "%s_%s" % (PREFIX, name))


# THE TOOLCHAIN THAT BUILT EACH LANGUAGE'S UNITS, so a callee's body
# comes from the compiler that built its caller.  Read off
# `canon39_callee_units.json`'s own keys, which `runtime_callee.py`
# wrote from the archive each toolchain named as its own.
TOOLCHAIN_OF_LANGUAGE = {
    "c": "clang",
    "cpp": "clang++",
    "rust": "rustc",
    "swift": "swiftc",
}


# ------------------------------------------------------------------
# where the arch-unit facts are recorded (data files, not modules)
# ------------------------------------------------------------------

def recorded_original(lang):
    path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
    return json.load(open(path))["units"]


def recorded_interpreter():
    path = os.path.join(HERE, "canon38_interp.json")
    return json.load(open(path))["units"]


def recorded_regenerated_shards():
    pattern = os.path.join(HERE, "canon38_regen_store", "*.json")
    return sorted(glob.glob(pattern))


def runtime_answer_readings():
    """per `toolchain/name`, the register families that callee's OWN
    body changes -- `runtime_answers78.json`, written by
    `runtime_answers78.py` from `ledger.answer_registers_of_body`
    over the 76 callee arch units task 63 extracted.

    THIS IS THE FIX OF log_168 §5.3.  canon39 was rendered with
    `runtime_callee_units.json`, task 59's FOUR-NAME division family,
    and with a rule that wrote one row on the accumulator; 2,862 units
    carried a transfer into a routine an archive defines with no
    ledger row naming it, and every float lowering's answer sits in
    `%xmm0`, not `%rax`."""
    path = os.path.join(HERE, "runtime_answers78.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    return document.get("readings", {})


def runtime_routine_names(readings=None):
    """the routine names the compilers' OWN archives define, as
    `runtime_callee.py` (node 0_3_5_1_8, tasks 59 and 63) read them off
    the archives' own symbol indexes.  Handed to `ledger.Ledger` so its
    runtime transfer rule can fire."""
    if readings is None:
        readings = runtime_answer_readings()
    names = set()
    for key in readings:
        if "/" in key:
            names.add(key.split("/", 1)[1])
        else:
            names.add(key)
    if names:
        return frozenset(names)
    path = os.path.join(HERE, "runtime_callee_units.json")
    if not os.path.exists(path):
        return frozenset()
    document = json.load(open(path))
    for key in document.get("units", {}):
        if "/" in key:
            names.add(key.split("/", 1)[1])
        else:
            names.add(key)
    return frozenset(names)


def unattached_runtime_callers():
    """the callers whose runtime callee has NO body on this machine.
    log_161 section 4.1.1: swift's archive is on neither side of the
    container wall, so four callers stay unattached.  Such a caller is
    REFUSED BY NAME rather than counted as if its answer were known."""
    path = os.path.join(HERE, "runtime_callee_attachments.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    readings = runtime_answer_readings()
    have = set()
    for key in readings:
        if readings[key].get("refuse"):
            continue
        if "/" in key:
            have.add(key.split("/", 1)[1])
    out = {}
    for label, record in document.get("units", {}).items():
        if record.get("attached"):
            continue
        callee = record.get("callee")
        if callee is not None and callee in have:
            # task 63 extracted swift's archive INSIDE the instance
            # where swift lives, so this caller's callee now has a
            # body and the refusal task 59 recorded is answered.
            continue
        out[label] = record.get("why_not") or "no callee body"
    return out


# ------------------------------------------------------------------
# sub-node: prelude   (node 0_3_5_2_2)
# ------------------------------------------------------------------

class Prelude(object):
    """the standardized lines placed BEFORE the compiler's body that
    put each arriving value into the register the compiler's own code
    expects it in.

    The CORE's `## design`, as numbered statements, is the whole of
    this class.  Statement 5 is what this task changed: the emission
    order is the arrival contract's order, IN-0 first, whichever
    family that is.
    """

    def __init__(self, ledger):
        self.ledger = ledger

    def emit(self, arrival_families):
        """arrival_contract -> the prelude lines, IN CONTRACT ORDER.

        Returns (literal, resolved, rows, scratch), the same four the
        rest of the form expects.

        The scratch register is picked ONCE, before any line is
        emitted, against every GENERAL arrival family and the
        never-rename set.  It is therefore not a register any load in
        this prelude writes an arrival value into, whichever order the
        loads run in -- which is why the order may change without the
        loads interfering.
        """
        literal = []
        resolved = []
        rows = []
        general = []
        any_vector = False
        for family in arrival_families:
            if L.is_vector_family(family):
                any_vector = True
            else:
                general.append(family)
        scratch = None
        if any_vector:
            reserved = set(general) | set(canon.NEVER_RENAME)
            scratch = L.pick_scratch(reserved)
        for family in arrival_families:
            if L.is_vector_family(family):
                row = self.add_row(family)
                rows.append(row)
                pair, one = self.emit_vector_row(row, family, scratch)
            else:
                row = self.add_row(family)
                rows.append(row)
                pair, one = self.emit_general_row(row, family)
            literal.extend(pair)
            resolved.append(one)
        return literal, resolved, rows, scratch

    def add_row(self, family):
        """IN-i, sized by the type of the value that arrives in it."""
        if L.is_vector_family(family):
            size = 16
            type_name = "16-byte vector value"
        else:
            size = 8
            type_name = "8-byte general value"
        return self.ledger.add(
            "IN", size, type_name, "arrival", [],
            note="the runner fills this row before the unit is "
                 "entered")

    def emit_general_row(self, row, family):
        """IN-i, general destination -> the two step lines.

        Step one reads the ledger entry for the IN block into the
        DESTINATION register; step two reads the row at IN-i's offset
        from that base into the same register.  The destination is the
        pointer for its own step one, so no register is reserved.
        """
        pointer = L.register_text(family, 64)
        literal = []
        literal.append("mov %s,%s"
                       % (L.ledger_entry_text("IN"), pointer))
        literal.append("mov 0x%x(%s),%s"
                       % (row.offset, pointer, pointer))
        resolved = "mov %s,%s" % (row.name(), pointer)
        return literal, resolved

    def emit_vector_row(self, row, family, scratch):
        """IN-i, vector destination -> `movdqu` through one general
        scratch.  A 16-byte row does not fit a general register, so
        the pointer cannot be the destination and one scratch is
        needed; it is not an arrival family, so the body cannot read
        it before writing it."""
        pointer = L.register_text(scratch, 64)
        literal = []
        literal.append("mov %s,%s"
                       % (L.ledger_entry_text("IN"), pointer))
        literal.append("movdqu 0x%x(%s),%%%s"
                       % (row.offset, pointer, family))
        resolved = "movdqu %s,%%%s" % (row.name(), family)
        return literal, resolved


# ------------------------------------------------------------------
# sub-node: epilogue   (node 0_3_5_2_3)
# ------------------------------------------------------------------

class Epilogue(object):
    """the standardized lines placed BEFORE every `ret` that store the
    compiler's own result register into OUT-0.

    UNCHANGED BY THIS TASK.  The one text of this rule is
    `ledger.Ledger.build_epilogue`, which carries the pointer choice
    (`pick_pointer`) inside it.  This class is the CORE's shape and
    calls that one text; it does not carry a second copy.
    """

    def __init__(self, ledger):
        self.ledger = ledger

    def emit(self, result_family, result_width, producer, operands):
        """answer_home -> the epilogue lines: ledger entry -> OUT block
        base -> store the result register into OUT-0."""
        return self.ledger.build_epilogue(result_family, result_width,
                                          producer, operands)

    def pick_pointer(self, result_family):
        """result register -> a pointer register that is not it.  The
        same choice `build_epilogue` makes inside itself; exposed here
        because the CORE names it, and checked by C5."""
        reserved = set([result_family]) | set(canon.NEVER_RENAME)
        return L.pick_scratch(reserved)

    def place(self, body, prelude_lines, epilogue_lines):
        """body_text -> the same lines inserted immediately before
        every `ret`.  The one text is `ledger.weave`."""
        return L.weave(body, prelude_lines, epilogue_lines)


# ------------------------------------------------------------------
# sub-node: labels   (node 0_3_5_2_4)
# ------------------------------------------------------------------

class Labels(object):
    """the rewrite that replaces every branch target inside a unit
    with a positional name, `L0`, `L1`, ... in address order.

    UNCHANGED BY THIS TASK.  The one text is
    `ledger.positional_labels`, which locates targets by
    disassembling the unit's own bytes with capstone and keeps an
    out-of-unit transfer's callee as its operand.  This class is the
    CORE's shape over that one text.
    """

    def rewrite(self, body_lines, byte_text):
        """body_text + targets -> the same text with L0.. defined and
        named.  Returns (lines, record)."""
        return L.positional_labels(body_lines, byte_text)

    def locate_targets(self, byte_text):
        """body_bytes -> the offset of every instruction, which is
        what decides whether a transfer's target is inside the unit
        (capstone)."""
        return L.instruction_offsets(byte_text)

    def rewrite_external(self, mnemonic, operands, annotation):
        """an out-of-unit transfer -> callee kept as operand, address
        and angle-bracket comment dropped."""
        return L.transfer_callee(mnemonic, operands, annotation)


# ------------------------------------------------------------------
# sub-node: refuse   (node 0_3_5_2_7)
# ------------------------------------------------------------------

class Refuse(object):
    """the named reasons a unit cannot be put into the canonical form
    at all.  A refusal is a verdict on the record, not a unit quietly
    dropped: `record` returns a row that travels with the population.
    """

    causes = {
        "never returns":
            "the whole body is a transfer into another routine, so "
            "there is no moment in this unit at which the answer "
            "exists to be stored; turning that transfer into a call "
            "would change the body, which ruling 1 forbids",
        "no answer home":
            "this unit's own code names no register the answer is "
            "left in, so there is nothing to store into OUT-0",
        "no canonical text":
            "this handler has no ship body to wrap",
        "no text":
            "no ship text and no canonical text exist for this unit, "
            "so there is no body to wrap",
        "the body names the ledger symbol":
            "the body spells the form's own symbol, which would "
            "collide with it",
        "no runtime callee body":
            "this unit's answer arrives through a call into its own "
            "compiler's runtime, and that compiler's archive is not "
            "on this machine, so the callee's body cannot be read "
            "and the answer is not known (log_161 section 4.1.1)",
        "renderer fault":
            "the renderer raised on this unit; the exception is "
            "quoted on the row",
    }

    def classify(self, problem):
        """a `ledger.Refusal` (or a cause string) -> a cause name and
        its detail, or nothing when the unit can be wrapped."""
        if problem is None:
            return None
        if isinstance(problem, L.Refusal):
            return problem.cause, problem.detail
        if isinstance(problem, tuple):
            return problem[0], problem[1]
        cause = str(problem)
        return cause, self.causes.get(cause, cause)

    def record(self, unit_record, problem):
        """cause + unit -> a refusal row, written onto the unit's own
        record so the refused unit is visible rather than absent."""
        found = self.classify(problem)
        if found is None:
            return unit_record
        cause, detail = found
        unit_record["outcome"] = "REFUSED"
        unit_record["refusal_cause"] = cause
        unit_record["refusal"] = detail
        unit_record["refusal_cause_is_named_in_the_core"] = (
            cause in self.causes)
        return unit_record


# ------------------------------------------------------------------
# the node's class
# ------------------------------------------------------------------

class CanonicalForm(object):
    """THE one form every arch-unit is rendered into.

    attributes:
      block_order   -- IN, CONST, TEMP, OWN, STACK, X87, GUARD, OUT;
                       eight 8-byte ledger entries, 0x40 bytes
      wrapped_text  -- prelude + body verbatim + epilogue, one string;
                       the runnable record (layer 3).  Held per call
                       on the returned fields, and on the instance as
                       the last one wrapped.
    """

    block_order = L.BLOCK_ORDER

    def __init__(self, runtime_routines=None,
                 unattached_callers=None, runtime_answers=None):
        self.wrapped_text = None
        self.runtime_routines = frozenset(runtime_routines or [])
        self.runtime_answers = dict(runtime_answers or {})
        self.unattached_callers = dict(unattached_callers or {})
        self.labels = Labels()
        self.refusal = Refuse()

    # ------------------------------------------------------- wrap
    def wrap(self, body_text, arrival_families, result_family,
             result_width, body_bytes=None, label=None,
             toolchain=None):
        """ArchUnit -> wrapped_text + Ledger.

        Calls prelude, labels, epilogue; the body is never touched.
        Raises `ledger.Refusal` where the unit cannot be wrapped, which
        `refuse` turns into a row.
        """
        if label is not None and label in self.unattached_callers:
            raise L.Refusal(
                "no runtime callee body",
                self.unattached_callers[label])
        if not body_text:
            raise L.Refusal(
                "no text",
                "no text exists for this unit, so there is no body to "
                "wrap")
        ledger = L.Ledger(runtime_routines=self.runtime_routines,
                          runtime_answers=self.runtime_answers,
                          toolchain=toolchain)
        prelude = Prelude(ledger)
        epilogue = Epilogue(ledger)
        body_as_read = L.split_lines(body_text)
        for raw in body_as_read:
            line = L.R36.strip_annotation(raw)
            if L.LEDGER_SYMBOL in line:
                raise L.Refusal(
                    "the body names the ledger symbol",
                    "the body spells %r, which would collide with the "
                    "form's own symbol" % L.LEDGER_SYMBOL)
        body, label_record = self.labels.rewrite(body_as_read,
                                                 body_bytes)
        prelude_literal, prelude_resolved, arrival_rows, \
            prelude_scratch = prelude.emit(arrival_families)
        where, holes = ledger.walk_dataflow(body, arrival_rows,
                                            arrival_families)
        producer = "the body's last write to %%%s" % result_family
        operands = []
        if result_family in where:
            answer_row = where[result_family]
            operands = [answer_row]
            source_row = ledger.by_row.get(answer_row)
            if source_row is not None:
                producer = source_row.produced_by
        epilogue_literal, epilogue_resolved, out_row, \
            epilogue_scratch = epilogue.emit(result_family,
                                             result_width, producer,
                                             operands)
        literal_lines, returns = epilogue.place(body, prelude_literal,
                                                epilogue_literal)
        resolved_lines, _ = epilogue.place(body, prelude_resolved,
                                           epilogue_resolved)
        self.wrapped_text = "; ".join(literal_lines)
        fields = {
            "wrapped_text": self.wrapped_text,
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
            "ledger": ledger.as_list(),
            "ledger_block_bytes": ledger.block_bytes(),
            "ledger_symbol": L.LEDGER_SYMBOL,
            "ledger_entries": list(self.block_order),
            "out_row": out_row.name(),
            "arrival_families": list(arrival_families),
            "arrival_contract_bindings":
                self.bindings(arrival_families, arrival_rows),
            "result_family": result_family,
            "result_width": result_width,
            "producer_holes": holes,
            "transfer_shapes": list(ledger.transfer_shapes),
            "form": FORM_NAME,
            "prelude_order":
                "arrival_contract order: IN-i is argument i, and the "
                "prelude emits IN-0 first, whichever family that is "
                "(CORE_0_3_5_2_2_prelude design rule 5)",
            "addressing": "two steps: read the block's base out of the "
                          "ledger at an absolute address "
                          "(rip-relative), then read the row inside "
                          "that block",
        }
        return fields

    def bindings(self, arrival_families, arrival_rows):
        """IN-i <-> the family the arrival contract names at i.

        Under the fixed order this is also the row the prelude's i-th
        load fills, so the bindings and the prelude now agree.  Under
        the vector-first order they did not, which is the defect
        log_153 section 9 printed.
        """
        out = []
        for index, family in enumerate(arrival_families):
            row = arrival_rows[index]
            out.append({
                "row": row.name(),
                "bound_to_the_same_symbol_as": "%" + family,
                "size": row.size,
            })
        return out

    # ----------------------------------------------------- refuse
    def refuse(self, unit_record, problem):
        """the named reasons a unit cannot be wrapped, recorded as a
        row that travels with the population."""
        return self.refusal.record(unit_record, problem)

    # --------------------------------------------------- assemble
    POSITIONAL = re.compile(r"^L\d+$")
    RIP_ZERO = re.compile(r"0x0\(%rip\)")
    BATCH = 60
    WORK = "/tmp/canon_assemble_work"

    def render_for_assembler(self, symbol, wrapped_text):
        """one wrapped text -> assembler lines under its own symbol.

        Two mechanical things and no repair: a positional label is
        made local to its symbol so a batch of many symbols does not
        collide, and every out-of-unit callee (and every positional
        label the body branches to without defining) is declared once
        as a stub so the instruction encodes as the transfer it is.
        This checks the ENCODING, not the presence of the callee.
        """
        notes = []
        stubs = set()
        defined = set()
        used = set()
        lines = []
        count = 0
        for raw in L.split_lines(wrapped_text):
            line = raw
            if line.endswith(":"):
                name = line[:-1]
                if self.POSITIONAL.match(name) is not None:
                    defined.add(name)
                    lines.append(".L%s_%s:" % (symbol, name))
                    continue
                lines.append(line)
                continue
            text, _annotation = L.split_off_annotation(line)
            if "!!" in line:
                notes.append("stripped a reading annotation")
            line = text
            parts = line.split(" ", 1)
            if len(parts) == 2:
                if L.is_transfer(parts[0]):
                    target = parts[1].strip()
                    if self.POSITIONAL.match(target) is not None:
                        used.add(target)
                        line = "%s .L%s_%s" % (parts[0], symbol,
                                               target)
                    elif target.startswith("x_"):
                        stubs.add(target)
                        notes.append("a transfer out of the unit was "
                                     "bound to the named stub %s"
                                     % target)
            if self.RIP_ZERO.search(line):
                line = self.RIP_ZERO.sub("canon39_pool(%rip)", line)
                notes.append("rip-relative data reference bound to a "
                             "real local constant pool")
            lines.append("    " + line)
            count = count + 1
        out = []
        for name in sorted(used - defined):
            stubs.add("%s_unplaced_%s" % (symbol, name))
            notes.append("the body branches to %s and defines no such "
                         "label, so the target is a stub" % name)
        for line in lines:
            fixed = line
            for name in sorted(used - defined):
                fixed = fixed.replace(".L%s_%s" % (symbol, name),
                                      "%s_unplaced_%s" % (symbol,
                                                          name))
            out.append(fixed)
        return out, count, sorted(set(notes)), sorted(stubs)

    def write_batch(self, path, items):
        """the batch's .s file, with the ledger symbol defined as an
        EIGHT-entry table of eight-byte pointers in `.data`."""
        handle = open(path, "w")
        handle.write("    .text\n")
        stubs = set()
        for item in items:
            for name in item[3]:
                stubs.add(name)
        for name in sorted(stubs):
            handle.write("%s:\n    ret\n" % name)
        for item in items:
            symbol = item[0]
            handle.write("    .globl %s\n" % symbol)
            handle.write("%s:\n" % symbol)
            for line in item[1]:
                handle.write(line + "\n")
        handle.write("    .section .rodata\n")
        handle.write("    .align 16\n")
        handle.write("canon39_pool:\n")
        handle.write("    .quad 0\n    .quad 0\n    .quad 0\n"
                     "    .quad 0\n")
        handle.write("    .data\n")
        handle.write("    .align 8\n")
        handle.write("%s:\n" % L.LEDGER_SYMBOL)
        for block in self.block_order:
            handle.write("    .quad 0    # the base address of the %s "
                         "block, written by the runner\n" % block)
        handle.close()

    def assemble(self, path, obj):
        """wrapped_text -> object file via `as --64`."""
        proc = subprocess.run(["as", "--64", path, "-o", obj],
                              capture_output=True, text=True)
        return proc.returncode, proc.stderr

    def disassemble(self, obj):
        proc = subprocess.run(["objdump", "-d", obj],
                              capture_output=True, text=True)
        return proc.stdout

    def relocations(self, obj):
        proc = subprocess.run(["objdump", "-r", obj],
                              capture_output=True, text=True)
        return proc.stdout

    def counts_from_dump(self, dump):
        out = {}
        symbol = None
        for line in dump.splitlines():
            head = re.match(r"^[0-9a-f]+ <([^>]+)>:$", line.strip())
            if head is not None:
                symbol = head.group(1)
                out[symbol] = 0
                continue
            if symbol is None:
                continue
            if re.match(r"^\s+[0-9a-f]+:\s", line) is not None:
                if "\t" in line:
                    tail = line.split("\t")
                    if len(tail) >= 3 and tail[2].strip():
                        out[symbol] = out[symbol] + 1
        return out


# ------------------------------------------------------------------
# the drivers: all 31,078 units, three populations
# ------------------------------------------------------------------

def is_vector(family):
    return L.is_vector_family(family)


def affected_by_the_defect(arrival_families):
    """a unit is affected by the vector-first defect exactly when its
    contract names BOTH a vector arrival and a general one -- those
    are the units whose two orders differ."""
    vector = 0
    general = 0
    for family in arrival_families or []:
        if is_vector(family):
            vector = vector + 1
        else:
            general = general + 1
    return vector > 0 and general > 0


def base_record(recorded):
    """the arch-unit facts, carried across from the record."""
    out = {}
    for key in ("unit", "lang", "n", "operator", "population",
                "recorded_status", "branch_kind", "body_source",
                "body_text", "body_bytes", "entry_contract",
                "entry_contract_source", "recorded_entry_contract",
                "entry_contract_disagreement", "answer_home_source",
                "arrival_annotation", "build", "prior_text",
                "prior_text_source"):
        if key in recorded:
            out[key] = recorded[key]
    return out


def render_one(form, gate, recorded):
    """one unit -> its canon39 record, gated."""
    record = base_record(recorded)
    label = recorded.get("unit")
    record["unit"] = label
    families = list(recorded.get("arrival_families") or [])
    record["arrival_families"] = families
    record["prelude_order_was_affected_by_the_vector_first_defect"] = \
        affected_by_the_defect(families)
    body_text = recorded.get("body_text")
    if body_text is None:
        cause = recorded.get("refusal_cause") or "no text"
        detail = recorded.get("refusal") or form.refusal.causes.get(
            cause, cause)
        return form.refuse(record, (cause, detail))
    try:
        fields = form.wrap(body_text, families,
                           recorded.get("result_family"),
                           recorded.get("result_width"),
                           body_bytes=recorded.get("body_bytes"),
                           label=label,
                           toolchain=TOOLCHAIN_OF_LANGUAGE.get(
                               recorded.get("lang")))
    except L.Refusal as bad:
        return form.refuse(record, bad)
    except Exception as bad:                            # noqa: BLE001
        return form.refuse(
            record, ("renderer fault",
                     "%s: %s" % (type(bad).__name__, bad)))
    record.update(fields)
    verdict = gate.prove_wrapped(fields["wrapped_text"], record)
    record["verdict"] = verdict.outcome
    record["verdict_detail"] = verdict.reason
    record["verdict_route"] = verdict.route
    record["solver_timeout_ms"] = verdict.solver_timeout_ms
    if verdict.counterexample is not None:
        record["counterexample"] = verdict.counterexample
    if verdict.proved():
        record["outcome"] = "WRAPPED_TEXT_PROVED"
    elif verdict.outcome == GATE.DISPROVED:
        record["outcome"] = "GATE_DISPROVED"
    else:
        record["outcome"] = "GATE_UNDECIDED"
    return record


def tally_of(units):
    out = {}
    for record in units.values():
        key = record.get("outcome")
        out[key] = out.get(key, 0) + 1
    return out


def document_of(units, population, produced_from):
    return {
        "meta": {
            "generated_by": "canonical_form.py",
            "node": "hq.research.compiler_graph.canonical_form",
            "form": "the canonical form: prelude from the ledger into "
                    "the compiler's own registers IN ARRIVAL-CONTRACT "
                    "ORDER, body verbatim, epilogue into OUT-0",
            "population": population,
            "arch_unit_facts_read_from": produced_from,
            "gate": "gate.py Gate.prove_wrapped, against the unit's "
                    "own ship code",
            "note": "the operator field is a display label on the "
                    "member and is read by nothing",
        },
        "tally": tally_of(units),
        "units": units,
    }


def write_json(path, document):
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def new_form():
    readings = runtime_answer_readings()
    return CanonicalForm(
        runtime_routines=runtime_routine_names(readings),
        unattached_callers=unattached_runtime_callers(),
        runtime_answers=readings)


def run_original(args):
    form = new_form()
    gate = GATE.Gate()
    for lang in (LANGS if args.lang is None else [args.lang]):
        path = out_path("wrapped_%s.json" % lang)
        units = {}
        if os.path.exists(path) and not args.fresh:
            units = json.load(open(path))["units"]
        recorded = recorded_original(lang)
        done = 0
        for label in sorted(recorded):
            if label in units:
                continue
            if args.limit is not None and done >= args.limit:
                break
            units[label] = render_one(form, gate, recorded[label])
            done = done + 1
            if done % CHECKPOINT_EVERY == 0:
                write_json(path, document_of(
                    units, "the original corpus, %s" % lang,
                    "canon38_wrapped_%s.json" % lang))
                sys.stderr.write("  %s: %d done\n" % (lang,
                                                      len(units)))
                sys.stderr.flush()
        write_json(path, document_of(
            units, "the original corpus, %s" % lang,
            "canon38_wrapped_%s.json" % lang))
        print("%-6s %4d units  %s"
              % (lang, len(units), json.dumps(tally_of(units),
                                              sort_keys=True)))
    return 0


def run_interpreter(args):
    form = new_form()
    gate = GATE.Gate()
    path = out_path("interp.json")
    units = {}
    if os.path.exists(path) and not args.fresh:
        units = json.load(open(path))["units"]
    recorded = recorded_interpreter()
    for label in sorted(recorded):
        if label in units:
            continue
        units[label] = render_one(form, gate, recorded[label])
    write_json(path, document_of(units, "the interpreter population",
                                 "canon38_interp.json"))
    print("interp %4d units  %s"
          % (len(units), json.dumps(tally_of(units), sort_keys=True)))
    return 0


def regen_state_path():
    return out_path("regen_state.json")


def read_regen_state():
    path = regen_state_path()
    if not os.path.exists(path):
        return {"shards_done": [], "tally": {}}
    return json.load(open(path))


def write_regen_state(state):
    write_json(regen_state_path(), state)


def run_regenerated(args):
    form = new_form()
    gate = GATE.Gate()
    store = out_path("regen_store")
    if not os.path.isdir(store):
        os.makedirs(store)
    state = read_regen_state()
    if args.fresh:
        state = {"shards_done": [], "tally": {}}
    done_shards = set(state["shards_done"])
    shards = recorded_regenerated_shards()
    processed = 0
    for source in shards:
        name = os.path.basename(source)
        if name in done_shards:
            continue
        if args.limit is not None and processed >= args.limit:
            break
        recorded = json.load(open(source))["units"]
        units = {}
        for label in sorted(recorded):
            units[label] = render_one(form, gate, recorded[label])
        write_json(os.path.join(store, name),
                   document_of(units,
                               "the regenerated corpus, shard %s"
                               % name,
                               os.path.join("canon38_regen_store",
                                            name)))
        for key, value in tally_of(units).items():
            state["tally"][key] = state["tally"].get(key, 0) + value
        state["shards_done"].append(name)
        done_shards.add(name)
        write_regen_state(state)
        processed = processed + 1
        sys.stderr.write("  shard %s done (%d of %d)  %s\n"
                         % (name, len(state["shards_done"]),
                            len(shards),
                            json.dumps(state["tally"],
                                       sort_keys=True)))
        sys.stderr.flush()
    print("regen shards %d of %d  %s"
          % (len(state["shards_done"]), len(shards),
             json.dumps(state["tally"], sort_keys=True)))
    return 0


# ------------------------------------------------------------------
# assemble driver
# ------------------------------------------------------------------

def assemble_sources():
    whole = []
    for lang in LANGS:
        path = out_path("wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            whole.append((label, rec["wrapped_text"], "original"))
    path = out_path("interp.json")
    if os.path.exists(path):
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            whole.append((label, rec["wrapped_text"], "interpreter"))
    regen = []
    pattern = os.path.join(out_path("regen_store"), "*.json")
    for path in sorted(glob.glob(pattern)):
        for label, rec in json.load(open(path))["units"].items():
            if rec.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            regen.append((label, rec["wrapped_text"], "regenerated"))
    return whole, regen


def run_assemble(args):
    form = CanonicalForm()
    work = form.WORK
    if not os.path.isdir(work):
        os.makedirs(work)
    whole, regen = assemble_sources()
    sampled = regen[::args.stride]
    offered = whole + sampled
    items = []
    per_unit = {}
    for label, text, population in offered:
        symbol = "u_" + label.replace("/", "_")
        lines, count, notes, stubs = form.render_for_assembler(symbol,
                                                               text)
        items.append((symbol, lines, count, stubs))
        per_unit[symbol] = {
            "unit": label,
            "population": population,
            "instruction_lines": count,
            "normalizations": notes,
        }
    batches = []
    index = 0
    while index < len(items):
        batches.append(items[index:index + form.BATCH])
        index = index + form.BATCH
    assembled = 0
    failures = []
    relocation_total = 0
    transcripts = []
    for number, batch in enumerate(batches):
        source = os.path.join(work, "batch_%04d.s" % number)
        obj = os.path.join(work, "batch_%04d.o" % number)
        form.write_batch(source, batch)
        code, err = form.assemble(source, obj)
        if code != 0:
            for one in batch:
                single = os.path.join(work, "one_%s.s" % one[0])
                single_obj = os.path.join(work, "one_%s.o" % one[0])
                form.write_batch(single, [one])
                one_code, one_err = form.assemble(single, single_obj)
                if one_code != 0:
                    failures.append({
                        "unit": per_unit[one[0]]["unit"],
                        "assembler_message": one_err.strip()[:400],
                    })
                    per_unit[one[0]]["assembles"] = False
                    continue
                dump = form.disassemble(single_obj)
                seen = form.counts_from_dump(dump)
                per_unit[one[0]]["assembles"] = True
                per_unit[one[0]]["disassembled_instructions"] = \
                    seen.get(one[0], 0)
                assembled = assembled + 1
            continue
        dump = form.disassemble(obj)
        seen = form.counts_from_dump(dump)
        relocation_text = form.relocations(obj)
        relocation_total = relocation_total + len(
            re.findall(r"R_X86_64_PC32\s+(?:%s|\.data)"
                       % L.LEDGER_SYMBOL, relocation_text))
        for one in batch:
            got = seen.get(one[0], 0)
            ok = got >= one[2]
            per_unit[one[0]]["assembles"] = ok
            per_unit[one[0]]["disassembled_instructions"] = got
            if ok:
                assembled = assembled + 1
            else:
                failures.append({
                    "unit": per_unit[one[0]]["unit"],
                    "assembler_message":
                        "the symbol disassembled to %d instructions, "
                        "fewer than the %d the text spells"
                        % (got, one[2]),
                })
        if len(transcripts) < args.transcripts:
            for one in batch:
                if len(transcripts) >= args.transcripts:
                    break
                block = []
                keep = False
                for line in dump.splitlines():
                    head = re.match(r"^[0-9a-f]+ <([^>]+)>:$",
                                    line.strip())
                    if head is not None:
                        keep = head.group(1) == one[0]
                        if keep:
                            block = [line]
                        continue
                    if keep:
                        if line.strip() == "":
                            keep = False
                            continue
                        block.append(line)
                if block:
                    transcripts.append({
                        "unit": per_unit[one[0]]["unit"],
                        "source_file": source,
                        "objdump": "\n".join(block),
                    })
    transcript_path = out_path("assemble_transcripts.txt")
    handle = open(transcript_path, "w")
    handle.write("canonical_form.py --assemble -- SAMPLED objdump "
                 "transcripts, verbatim\n")
    handle.write("Each block below is `objdump -d` output on the "
                 "object file `as --64` produced.\n\n")
    for item in transcripts:
        handle.write("==== %s   (from %s)\n"
                     % (item["unit"], item["source_file"]))
        handle.write(item["objdump"])
        handle.write("\n\n")
    handle.close()
    document = {
        "meta": {
            "produced_by": "canonical_form.py --assemble",
            "ledger_symbol_defined_in_the_emitted_assembly":
                "%s: eight .quad entries, one per block, in .data"
                % L.LEDGER_SYMBOL,
            "regenerated_population_is_sampled": {
                "stride": args.stride,
                "sampled": len(sampled),
                "of": len(regen),
            },
        },
        "offered": len(items),
        "assembled": assembled,
        "failed": len(failures),
        "ledger_relocations_counted": relocation_total,
        "failures": failures[:200],
        "transcripts_file": transcript_path,
        "units": per_unit,
    }
    write_json(out_path("assemble.json"), document)
    print("offered %d  assembled %d  failed %d  ledger relocations %d"
          % (len(items), assembled, len(failures), relocation_total))
    return 0


# ------------------------------------------------------------------
# the two printed instances the task owes
# ------------------------------------------------------------------

def run_defect_census(args):
    """how many units the vector-first defect affects, computed from
    canon38, with its breakdown."""
    counts = {}
    per_language = {}
    populations = []
    for lang in LANGS:
        populations.append(("original", lang,
                            recorded_original(lang)))
    populations.append(("interpreter", None, recorded_interpreter()))
    for source in recorded_regenerated_shards():
        populations.append(("regenerated", None,
                            json.load(open(source))["units"]))
    total = {}
    for population, _lang, units in populations:
        for label, rec in units.items():
            total[population] = total.get(population, 0) + 1
            if not affected_by_the_defect(rec.get("arrival_families")):
                continue
            counts[population] = counts.get(population, 0) + 1
            key = (population, rec.get("lang"))
            per_language[key] = per_language.get(key, 0) + 1
    print("population totals      %s" % json.dumps(total,
                                                   sort_keys=True))
    print("affected by the defect %s" % json.dumps(counts,
                                                   sort_keys=True))
    print("affected, per language:")
    for key in sorted(per_language, key=lambda k: (k[0], k[1] or "")):
        print("  %-12s %-6s %6d"
              % (key[0], key[1], per_language[key]))
    print("affected total %d of %d"
          % (sum(counts.values()), sum(total.values())))
    return 0


def run_show_op_105(args):
    """`c/op_105`'s prelude before (canon38) and after (canon39)."""
    before = recorded_original("c")["c/op_105"]
    form = new_form()
    after = form.wrap(before["body_text"],
                      before["arrival_families"],
                      before["result_family"],
                      before["result_width"],
                      body_bytes=before.get("body_bytes"),
                      label="c/op_105")
    print("LITERAL -- c/op_105, body: %s" % before["body_text"])
    print("LITERAL -- arrival_families      %s"
          % before["arrival_families"])
    print("")
    print("LITERAL -- canon38 prelude_resolved   %s"
          % before["prelude_resolved"])
    print("LITERAL -- canon38 prelude            %s"
          % before["prelude"])
    print("LITERAL -- canon38 bindings           %s"
          % json.dumps(before["arrival_contract_bindings"],
                       sort_keys=True))
    print("")
    print("LITERAL -- canon39 prelude_resolved   %s"
          % after["prelude_resolved"])
    print("LITERAL -- canon39 prelude            %s"
          % after["prelude"])
    print("LITERAL -- canon39 bindings           %s"
          % json.dumps(after["arrival_contract_bindings"],
                       sort_keys=True))
    print("")
    print("LITERAL -- canon39 wrapped_text_resolved  %s"
          % after["wrapped_text_resolved"])
    return 0


def state_string(record):
    """the four-state string `gate.Gate.zero_regression` joins on."""
    outcome = record.get("outcome")
    if outcome == "WRAPPED_TEXT_PROVED":
        return "proved"
    if outcome == "REFUSED":
        return "refused"
    if outcome == "GATE_DISPROVED":
        return "withdrawn"
    return "undecided"


def read_all(prefix):
    """every unit of all three populations under one prefix."""
    out = {}
    for lang in LANGS:
        path = os.path.join(HERE, "%s_wrapped_%s.json" % (prefix, lang))
        if os.path.exists(path):
            out.update(json.load(open(path))["units"])
    path = os.path.join(HERE, "%s_interp.json" % prefix)
    if os.path.exists(path):
        out.update(json.load(open(path))["units"])
    pattern = os.path.join(HERE, "%s_regen_store" % prefix, "*.json")
    for path in sorted(glob.glob(pattern)):
        out.update(json.load(open(path))["units"])
    return out


def run_zero_regression(args):
    """canon39 against canon38, over all 31,078, with the cause of
    every loss computed over the unit's own canon39 record."""
    before_records = read_all("canon38")
    after_records = read_all(PREFIX)
    before = {}
    after = {}
    for label, rec in before_records.items():
        before[label] = state_string(rec)
    for label, rec in after_records.items():
        after[label] = state_string(rec)

    def cause_of(name):
        record = after_records.get(name)
        if record is None:
            return ("the unit is absent from the new run -- it was "
                    "not rendered")
        if record.get("outcome") == "REFUSED":
            return ("REFUSED, cause %r: %s"
                    % (record.get("refusal_cause"),
                       record.get("refusal")))
        return ("%s: %s" % (record.get("verdict"),
                            record.get("verdict_detail")))

    report = GATE.Gate().zero_regression(before, after, cause_of)
    before_tally = {}
    after_tally = {}
    for label, value in before.items():
        before_tally[value] = before_tally.get(value, 0) + 1
    for label, value in after.items():
        after_tally[value] = after_tally.get(value, 0) + 1
    refusal_before = {}
    refusal_after = {}
    for label, rec in before_records.items():
        if rec.get("outcome") == "REFUSED":
            key = rec.get("refusal_cause")
            refusal_before[key] = refusal_before.get(key, 0) + 1
    for label, rec in after_records.items():
        if rec.get("outcome") == "REFUSED":
            key = rec.get("refusal_cause")
            refusal_after[key] = refusal_after.get(key, 0) + 1
    document = {
        "meta": {
            "produced_by": "canonical_form.py --zero-regression",
            "before": "canon38 (log_152), the baseline",
            "after": "canon39, this task's render",
            "rule": "no unit proved in the previous round loses "
                    "PROVED without a named cause, checked over that "
                    "unit's own artifact",
        },
        "population_before": len(before),
        "population_after": len(after),
        "states_before": before_tally,
        "states_after": after_tally,
        "refusal_causes_before": refusal_before,
        "refusal_causes_after": refusal_after,
        "report": report,
    }
    write_json(out_path("zero_regression.json"),
               document)
    print("population before %d  after %d"
          % (len(before), len(after)))
    print("states before %s" % json.dumps(before_tally,
                                          sort_keys=True))
    print("states after  %s" % json.dumps(after_tally, sort_keys=True))
    print("refusal causes before %s" % json.dumps(refusal_before,
                                                  sort_keys=True))
    print("refusal causes after  %s" % json.dumps(refusal_after,
                                                  sort_keys=True))
    print("kept %d  lost %d  gained %d  moved %d  missing %d"
          % (report["kept"], report["lost"], report["gained"],
             report["moved_without_losing_a_proof"],
             report["missing_from_the_new_run"]))
    print("regressions without a named cause = %d"
          % report["regressions_without_a_named_cause"])
    for entry in report["causes"]:
        print("  %d unit(s): %s" % (entry["units"], entry["cause"]))
        print("    sightings: %s" % ", ".join(entry["sightings"]))
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--population",
                        choices=["original", "interpreter",
                                 "regenerated"])
    parser.add_argument("--lang")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--assemble", action="store_true")
    parser.add_argument("--stride", type=int, default=30)
    parser.add_argument("--transcripts", type=int, default=6)
    parser.add_argument("--defect-census", action="store_true")
    parser.add_argument("--show-op-105", action="store_true")
    parser.add_argument("--zero-regression", action="store_true")
    parser.add_argument("--prefix", default=PREFIX,
                        help="the artifact prefix to write; canon39 "
                             "is round 13's render, canon40 is task "
                             "78's with the corrected runtime "
                             "destination rule")
    args = parser.parse_args(argv[1:])
    globals()["PREFIX"] = args.prefix
    if args.zero_regression:
        return run_zero_regression(args)
    if args.defect_census:
        return run_defect_census(args)
    if args.show_op_105:
        return run_show_op_105(args)
    if args.assemble:
        return run_assemble(args)
    if args.population == "original":
        return run_original(args)
    if args.population == "interpreter":
        return run_interpreter(args)
    if args.population == "regenerated":
        return run_regenerated(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
