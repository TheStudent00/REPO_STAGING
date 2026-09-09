#!/usr/bin/env python3
"""term.py -- THE NODE `term`, node 0_3_5_6 of the compiler graph.

CORE:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_6_term/CORE_0_3_5_6_term.md`
and its four sub-node COREs: `transcribe`, `normalize`, `census`,
`render_back`.

WHAT THIS FILE IS, in the CORE's own words.  A unit's computation as a
z3 expression, read off its ledger from OUT-0 downward (layer 4), and
that expression printed by one fixed rule so that two units computing
the same thing print the same characters (layer 5).  The census is the
filter over ledgers for rows whose producer has no term.

THE CLASS IS `Term`, and its methods are the CORE's sub-nodes:

    transcribe   Ledger -> z3_term
    normalize    z3_term -> normalized_text
    census       a population of ledgers -> the rows whose producer
                 has no builder
    render_back  z3_term -> arch text.  **BUILT 2026-09-03 (task 66),
                 closing the debt log_147 section 8.1 named.**  The
                 class `RenderBack` in section 5 is the sub-node; the
                 rendered text is a SECOND canonical rendering of the
                 unit beside layer 3, wrapped by the same
                 `CanonicalForm.wrap` and gated by the same
                 `Gate.prove_wrapped` against the unit's own ship
                 code.  It replaces nothing: layer 3 stays the
                 unit's own machine code.

MEANINGS COME FROM ONE TABLE.  Every arch opcode's meaning is read
from `reference.Reference.opcode_table` -- the SAME object the gate's
reference route reads.  There is no producer table in this file.  That
is the term CORE's settled rule ("Meanings come from one table shared
with the reference, so route two tests wiring and route one tests
meaning"), and it is why `layer4.py`'s own producer table is not
imported and not copied: it was the second table.

HOW A ROW BECOMES A TERM, said mechanically.  A `reference` builder
reads its inputs through `reference.Operands`, which reads through
`reference.MachineState` and through nothing else.  So this file:

  1. RELINKS each ledger row to the body line that produced it, by
     re-running `ledger.Ledger.walk_dataflow` with two seams recorded
     -- `ledger.mnemonic_of`, called once per body line, says which
     line is being walked; `Ledger.add`, called once per row, stamps
     that line onto the row.  The re-run is then CHECKED row for row
     against the stored canon39 ledger: same row names, same
     producers, same operands, in order.  A unit whose re-run
     disagrees is REFUSED BY NAME.  This is `relink48.py`'s method,
     applied to the landed `ledger.py` instead of to the superseded
     `ledger47.py`; nothing of `relink48.py` is imported.
  2. Walks the rows in the ledger's own order, holding a term per row
     and a HOLDER map (register family -> the row that last resides
     there).  The holder map is the LEDGER'S OWN WIRING: it is filled
     from the rows' `resident` fields, never from a second dataflow
     analysis.
  3. For each row with an arch-opcode producer: seeds a fresh
     `MachineState` with the holder map's terms, seeds the flags and
     the machine stack and the x87 stack from the operand rows the
     row itself names, looks the mnemonic up in
     `Reference.opcode_table`, runs that entry's builder, and reads
     the produced value back out of the state at the place the row
     says it resides.  A flag-pair producer runs the setter's builder
     and then the reader's, over one state, so the pair is one act.
  4. Stops at IN rows, which become free symbols bound to the arrival
     registers -- the reference simulator's own symbols
     (`seed_<family>`), so the two gate routes need no substitution
     step between them.
  5. OUT-0's term, cut to the row's own size, is the unit's term.

WIDTH.  A row carries no width; a body line does.  Every width in a
term therefore comes from the line that produced the value, through
`reference.Operands.width_at` / `.destination_width`, which read the
line's own operand spellings and its AT&T size letter.  That is the
transcribe CORE's settled rule, and it is why the relink exists at
all.

OPERAND SLOTS ARE CHECKED, NOT ASSUMED.  `check_operand_slots` replays
each row's recorded operand rows against the operand texts of its own
body line and records a disagreement rather than assuming it away.

A TERM THAT DOES NOT PROVE IS WITHDRAWN, not kept as a weaker key.
`gate.Gate.prove_term_against_ship` and `.prove_term_against_text` are
the two routes; a unit whose term proves on neither has no layer-5
key, and the pool reads that as `layer5_merge_eligible: false`.

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

No operator token appears in this file.  Producers are typed objects
`{"kind", "mnem"}`; the `operator` field of a unit record is a display
label this file copies and never reads.

Coding discipline: no compound one-liner statements.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402

import canon                                                     # noqa: E402
import canonical_form as CF                                      # noqa: E402
import ledger as L                                               # noqa: E402
import reference as R                                            # noqa: E402


# ==================================================================
# section 0: the two exceptions, refused by name
# ==================================================================

class NoTerm(Exception):
    """this row's producer has no term builder.  Carries the written
    reason sentence the census groups on."""

    def __init__(self, why):
        Exception.__init__(self, why)
        self.why = why


class RelinkDisagreement(Exception):
    """the re-run's ledger is not the stored ledger; refused by name."""


# ==================================================================
# section 1: the relink -- row -> the body line that produced it
#
# The seam method, copied in SHAPE (not in code) from `relink48.py`,
# which did the same against the superseded `ledger47.py`.
# ==================================================================

class _LineStamping(L.Ledger):
    """a `ledger.Ledger` that stamps the current body line onto every
    row it creates.  It changes nothing about the walk: `add` is
    called with the same arguments and returns the same row."""

    def __init__(self, runtime_routines=None, runtime_answers=None,
                 toolchain=None):
        # EVERY INPUT THE RENDER WAS HANDED (task 83).  The relink's
        # re-walk is checked against the stored ledger row for row, so
        # it must be built from the same inputs
        # `canonical_form.CanonicalForm.wrap` built the stored ledger
        # from.  Task 78 added `runtime_answers` and `toolchain` there
        # and this constructor did not pass them, so a body naming an
        # archive-defined routine met `Ledger.runtime_answer`'s
        # refusal and the walk never reached the corpus: 3,927 of the
        # 30,324 units canon40 proved.  Rule and measurement:
        # CORE_0_3_5_6_2_transcribe.md, "THE RELINK IS HANDED EVERY
        # INPUT THE RENDER WAS HANDED".
        L.Ledger.__init__(self, runtime_routines=runtime_routines,
                          runtime_answers=runtime_answers,
                          toolchain=toolchain)
        self.current_line = None
        self.occurrence = 0
        self.line_of_row = {}
        self.occurrence_of_row = {}

    def add(self, block, size, type_name, produced_by, operands,
            note=None, resident=None):
        row = L.Ledger.add(self, block, size, type_name, produced_by,
                           operands, note=note, resident=resident)
        self.line_of_row[row.name()] = self.current_line
        self.occurrence_of_row[row.name()] = self.occurrence
        return row


_ORIGINAL_MNEMONIC_OF = L.mnemonic_of


def relink(unit, runtime_routines=None, runtime_answers=None,
           toolchain=None):
    """(rows, line_of_row) for one canonicalized unit record.

    The rows are the STORED ledger's rows -- this function does not
    replace them.  It re-runs the walk only to learn which body line
    made each row, and then CHECKS the re-run against the stored
    ledger row for row.

    `runtime_answers` and `toolchain` are the ledger's own arguments
    and are passed straight through: the check above cannot hold when
    the re-walk is built from fewer inputs than the render was."""
    body = unit.get("body_verbatim")
    if not body:
        raise RelinkDisagreement("the unit record carries no body")
    ledger = _LineStamping(runtime_routines=runtime_routines,
                           runtime_answers=runtime_answers,
                           toolchain=toolchain)

    def recording_mnemonic_of(line):
        ledger.current_line = line
        ledger.occurrence = ledger.occurrence + 1
        return _ORIGINAL_MNEMONIC_OF(line)

    families = unit.get("arrival_families") or []
    L.mnemonic_of = recording_mnemonic_of
    try:
        # the prelude is `canonical_form.Prelude`, the one canon39 was
        # written with, so the IN rows are numbered in ARRIVAL-CONTRACT
        # order (IN-i is argument i).  `ledger.Ledger.build_prelude`'s
        # vector-first order is the defect task 60 fixed, and using it
        # here would number the inputs differently from the artifact
        # this file is transcribing.
        prelude = CF.Prelude(ledger).emit(families)
        arrival_rows = prelude[2]
        ledger.current_line = None
        ledger.walk_dataflow(body, arrival_rows, families)
    finally:
        L.mnemonic_of = _ORIGINAL_MNEMONIC_OF
    stored = unit.get("ledger") or []
    rebuilt = ledger.as_list()
    check_rebuild(stored, rebuilt)
    return stored, ledger.line_of_row, ledger.occurrence_of_row


def check_rebuild(stored, rebuilt):
    """the re-run is checked against the stored ledger: same row names,
    same producers, same operands, in the same order.  The stored
    ledger carries one more row than the re-run -- OUT-0, which
    `wrap_unit` adds after the walk -- so the check runs over the
    re-run's own length."""
    if len(rebuilt) > len(stored):
        raise RelinkDisagreement(
            "the re-run made %d rows where the stored ledger has %d"
            % (len(rebuilt), len(stored)))
    for index, row in enumerate(rebuilt):
        was = stored[index]
        if row["row"] != was["row"]:
            raise RelinkDisagreement(
                "row %d is %r in the re-run and %r in the stored "
                "ledger" % (index, row["row"], was["row"]))
        if row["produced_by"] != was["produced_by"]:
            raise RelinkDisagreement(
                "row %s has producer %r in the re-run and %r in the "
                "stored ledger"
                % (row["row"], row["produced_by"], was["produced_by"]))
        if row["operands"] != was["operands"]:
            raise RelinkDisagreement(
                "row %s reads %r in the re-run and %r in the stored "
                "ledger"
                % (row["row"], row["operands"], was["operands"]))


# ==================================================================
# section 2: reading a row's produced value back off the machine state
# ==================================================================

RESIDENT_REGISTER = "register %"
RESIDENT_STACK = "the machine stack"
FLAGS_ONLY = "flags only"


def family_of_resident(resident):
    """`"register %rax"` -> `"rax"`, through canon.py's own table, so
    a spelling this codebase does not know is refused rather than
    guessed."""
    if resident is None:
        return None
    if not resident.startswith(RESIDENT_REGISTER):
        return None
    spelling = resident[len(RESIDENT_REGISTER):]
    return canon.FAMILY_OF.get(spelling)


def destination_family(row, line):
    """the register family a row's value resides in.  The row's own
    `resident` field first; failing that, the destination operand of
    the line that produced it."""
    family = family_of_resident(row.get("resident"))
    if family is not None:
        return family
    if not line:
        return None
    operands = L.operands_of(line)
    if not operands:
        return None
    text = operands[-1]
    if not text.startswith("%"):
        return None
    return canon.FAMILY_OF.get(text[1:])


# ==================================================================
# section 3: THE NODE ITSELF -- class Term
# ==================================================================

class Transcription(object):
    """one unit's layer-4 record: the terms per row, the answer term,
    the holes (rows whose producer has no builder), the cascades (rows
    whose producer HAS a builder but whose operand row has no term),
    and the slot disagreements."""

    def __init__(self, unit_name):
        self.unit = unit_name
        self.terms = {}
        self.inputs = {}
        self.out_term = None
        self.holes = []
        self.cascades = []
        self.slot_disagreements = []
        self.refused = None
        self.flag_state = {}
        """row name -> the flag state the opcode that made that row
        LEFT BEHIND.

        A flag pair is one act with two halves.  The setting half is
        often an ordinary arithmetic opcode -- `or %esi,%edi` -- whose
        row carries a VALUE, not a flag state; the flags it also left
        are a second thing the same instruction produced.  So when a
        row is built, the flag state its builder left is kept here
        under that row's name, and the reading half of the pair picks
        it up from the row the ledger says it reads.  Without this,
        every `set<cc>` after a value-writing setter refused for want
        of flags -- measured: 1,364 units."""
        self.memory = {}
        """the body's own memory cells, shared across the per-row
        states.  A cell a body writes and later reads is one cell, so
        the dict is the unit's, not the row's -- the same reason the
        rip counter below is the unit's."""
        self.rip_reads = 0
        """how many rip-relative reads the body has made so far.

        THE REFERENCE KEYS A CONSTANT-POOL READ POSITIONALLY: the k-th
        rip-relative read of a body is `ripconst_k`.  This walk builds
        one machine state PER ROW, so the counter has to live on the
        unit's record and be carried into and out of each state --
        otherwise every row's first read would be `ripconst_0` and a
        body reading two different pool constants would be
        transcribed as reading one, which the gate then DISPROVES.
        Measured: 74 c units of the 610 in the original corpus."""


class Term(object):
    """the node.  One instance holds the shared meanings table and is
    reused across the population, so every unit is transcribed against
    the same table object."""

    def __init__(self, reference=None, runtime_routines=None,
                 runtime_units=None, runtime_answers=None):
        if reference is None:
            reference = R.REFERENCE
        self.reference = reference
        self.opcode_table = reference.opcode_table
        self.runtime_routines = frozenset(runtime_routines or [])
        self.runtime_units = runtime_units or {}
        # THE READINGS ARE A FACT ABOUT THIS MACHINE'S ARCHIVES, read
        # from the one file `canonical_form.runtime_routine_names`
        # already reads its names out of, so the names and the
        # readings can never come from two places.  A caller that
        # passes nothing gets them, because a caller that passes
        # nothing today gets a refusal and never a correct answer.
        if runtime_answers is None:
            runtime_answers = CF.runtime_answer_readings()
        self.runtime_answers = dict(runtime_answers)

    # ---------------------------------------------------------------
    # sub-node: transcribe        (node 0_3_5_6_2)
    # ---------------------------------------------------------------

    def transcribe(self, unit):
        """Ledger -> z3 term.  The walk starts at OUT-0 in the sense
        the CORE means: OUT-0's term is the read, and every row it
        depends on is transcribed because the ledger's row order is
        the body's order, so a row's operands already carry terms when
        the row is reached."""
        record = Transcription(unit.get("unit"))
        # The toolchain is the unit's OWN, read off its language
        # exactly as `canonical_form.wrap_unit` reads it, because one
        # routine's body differs between compilers and a caller handed
        # another toolchain's body is handed a different artifact.
        toolchain = CF.TOOLCHAIN_OF_LANGUAGE.get(unit.get("lang"))
        try:
            rows, line_of_row, occurrence_of_row = relink(
                unit, runtime_routines=self.runtime_routines,
                runtime_answers=self.runtime_answers,
                toolchain=toolchain)
        except RelinkDisagreement as problem:
            record.refused = "relink: %s" % problem
            return record
        except Exception as problem:
            record.refused = "relink raised %s: %s" % (
                type(problem).__name__, problem)
            return record
        shared = {}
        holder = {}
        stack_rows = []
        x87_rows = []
        families = unit.get("arrival_families") or []
        pending = []
        occurrence = None
        for row in rows:
            name = row["row"]
            line = line_of_row.get(name)
            here = occurrence_of_row.get(name)
            if here != occurrence:
                # ONE INSTRUCTION, ONE STATE.  An opcode that writes
                # two places -- `idiv`, whose quotient and remainder
                # are two rows of one line -- must have BOTH rows read
                # the state as it stood before the line ran.  So a
                # row's residence is not published to the holder map
                # until the line that made it is finished.  Measured:
                # without this, `c/op_246`'s remainder row read the
                # quotient row and the gate DISPROVED it.
                self.publish(record, pending, holder, stack_rows,
                             x87_rows)
                pending = []
                occurrence = here
            producer = row["produced_by"]
            kind = producer.get("kind")
            try:
                if row["block"] == "OUT":
                    self.answer_row(record, row)
                elif kind == "non_opcode_phrase":
                    self.plain_row(record, row, shared, families)
                elif kind == "runtime_callee":
                    self.runtime_row(record, row, producer, line,
                                     shared, holder, stack_rows,
                                     x87_rows)
                else:
                    self.opcode_row(record, row, producer, line,
                                    shared, holder, stack_rows,
                                    x87_rows)
            except NoTerm as problem:
                record.holes.append(
                    hole_record(row, producer, line, problem.why))
            except R.NotModeled as problem:
                record.holes.append(
                    hole_record(row, producer, line,
                                "the shared opcode table refused: %s"
                                % problem))
            except Exception as problem:
                record.holes.append(
                    hole_record(row, producer, line,
                                "building the term raised %s: %s"
                                % (type(problem).__name__, problem)))
            pending.append((row, line))
        self.publish(record, pending, holder, stack_rows, x87_rows)
        return record

    def publish(self, record, pending, holder, stack_rows, x87_rows):
        """the rows of one finished line, published to the holder map
        together."""
        for row, line in pending:
            self.remember_residence(record, row, line, holder,
                                    stack_rows, x87_rows)

    # -- the four row shapes -----------------------------------------

    def plain_row(self, record, row, shared, families):
        """a row whose producer is not an arch opcode at all: an
        arrival row, a literal, a stack address the body spells, or
        the answer when no opcode wrote it."""
        name = row["row"]
        block = row["block"]
        if block == "IN":
            symbol = self.input_symbol(row, shared, families)
            record.terms[name] = symbol
            record.inputs[name] = symbol
            return
        if block == "CONST":
            value = row.get("value_at_run") or 0
            record.terms[name] = z3.BitVecVal(
                value & ((1 << 64) - 1), 64)
            return
        if block == "OWN":
            pointer = seed_of(shared, "rsp")
            displacement = row.get("displacement") or 0
            record.terms[name] = pointer - z3.BitVecVal(
                displacement, 64)
            return
        if block == "OUT":
            self.answer_row(record, row)
            return
        raise NoTerm(
            "a row of block %s carries a producer that is not an arch "
            "opcode, and this file has no rule for that pairing"
            % block)

    def input_symbol(self, row, shared, families):
        """IN-i -> the free symbol standing for argument i.

        It is the REFERENCE SIMULATOR'S OWN symbol for the arrival
        register, spelled the way that simulator spells it
        (`seed_<family>`), so the transcribed term and the simulated
        body compare with no substitution step.

        THE WALK FOLLOWS THE LEDGER'S WIRING: the family is read off
        the prelude's own IN-row order (`arrival_families`), which is
        what the ledger transcribed, not off the recorded contract."""
        index = row["index"]
        if index >= len(families):
            raise NoTerm(
                "no arrival contract binding names the register this "
                "input row arrives in")
        family = families[index]
        if family is None:
            raise NoTerm(
                "no arrival contract binding names the register this "
                "input row arrives in")
        return seed_of(shared, family)

    def answer_row(self, record, row):
        """OUT-0.  Its term is the operand row's term, cut to the
        row's own size."""
        name = row["row"]
        if not row["operands"]:
            raise NoTerm(
                "no arch opcode in this body writes the answer "
                "register, so no row produces the answer")
        source = record.terms.get(row["operands"][0])
        if source is None:
            record.cascades.append(cascade_record(
                row, row["produced_by"], row["operands"][0]))
            return
        if is_flag_state(source):
            raise NoTerm(
                "the answer row reads a row that holds a flag state "
                "and not a value")
        record.terms[name] = R.cut(source, row["size"] * 8)
        record.out_term = record.terms[name]

    def runtime_row(self, record, row, producer, line, shared, holder,
                    stack_rows, x87_rows):
        """a row produced by a call into the compiler's OWN runtime
        (libgcc / compiler-rt: the `__divti3` family).

        `runtime_callee.py` (node 0_3_5_1_8) extracted that callee's
        body from the toolchain's own archive and attached it as an
        ArchUnit this caller references.  The callee's body is run
        through the SAME reference, over a state seeded exactly the
        way an ordinary opcode row's is -- from the HOLDER MAP, which
        is the ledger's own wiring, because the caller's own body has
        already placed its values in the registers the callee reads.
        Nothing about a calling rule is assumed here: the registers
        the callee reads are the registers the caller left.

        The answer is read at the place THIS ROW says the value
        resides.  The callee record states no answer home of its own,
        and inventing one would be an unruled rule; the caller's
        ledger row already carries the fact."""
        callee = producer.get("callee")
        unit = self.attached_callee(record, callee)
        if unit is None:
            raise NoTerm(
                "the runtime callee %r has no attached body on this "
                "machine, so the caller's answer is not known"
                % callee)
        row["_line"] = line
        state = self.seeded_state(record, row, shared, holder,
                                  stack_rows, x87_rows)
        body = unit.get("body_verbatim") or unit.get("body_as_read")
        if not body:
            raise NoTerm(
                "the attached body of the runtime callee %r is empty"
                % callee)
        # THE CALLEE'S BODY IS A CONTROL-FLOW GRAPH, NOT A LINE OF TEXT.
        # `clang++/__extendhfsf2` has five transfers over forty
        # instructions (log_167 §3.3), so a line-at-a-time walk stops
        # at the first one.  `Reference.walk_body` is the ONE walk the
        # reference CORE names (2026-09-03, task 64) and the one
        # `simulate` itself uses, so the two gate routes step into an
        # attached callee by the same rule.  Before task 64 this loop
        # called `Reference.step` per line.
        try:
            state = self.reference.walk_body(
                state, body, self.callees_beside(record, callee))
        except R.NotModeled as problem:
            record.rip_reads = state.rip_reads
            raise NoTerm(self.callee_refusal(callee, "", problem))
        except R.LeavesTheUnit as problem:
            record.rip_reads = state.rip_reads
            raise NoTerm(
                "the attached body of the runtime callee %r transfers "
                "out of itself (%s), so it leaves no answer here"
                % (callee, problem))
        record.rip_reads = state.rip_reads
        return_family = destination_family(row, line)
        if return_family is None:
            raise NoTerm(
                "this runtime-callee row names no place its value "
                "resides, so the callee's answer cannot be read")
        if return_family not in state.registers:
            raise NoTerm(
                "the runtime callee %r wrote no value into %s, which "
                "is where this row says its value resides"
                % (callee, return_family))
        record.terms[row["row"]] = R.cut(
            state.registers[return_family], row["size"] * 8)

    TOOLCHAIN_OF = {
        "c": "clang",
        "cpp": "clang++",
        "rust": "rustc",
    }

    def callees_beside(self, record, callee):
        """the routines the attached body may itself transfer into --
        the same toolchain's archive, and no other.  `__divti3` reaches
        `__udivmodti4`, which is one of the six routines reached ONLY
        as a nested callee (log_167 §5.2)."""
        lang = None
        if record.unit is not None:
            lang = record.unit.split("/", 1)[0]
        toolchain = self.TOOLCHAIN_OF.get(lang)
        if toolchain is None:
            return {}
        return self.runtime_units.get(toolchain, {})

    def attached_callee(self, record, callee):
        """the attached body of one runtime routine, from the archive
        of the toolchain that compiled THIS caller.

        The four archives do not agree -- clang's `__udivti3` is three
        instructions, rustc's is sixty-seven -- so the caller's own
        language selects the archive.  A language with no archive read
        on this machine (swift, whose archive is on neither side of
        the container wall, log_161 §4.1.1) gets nothing, and the row
        is refused by name rather than handed another toolchain's
        body."""
        lang = None
        if record.unit is not None:
            lang = record.unit.split("/", 1)[0]
        toolchain = self.TOOLCHAIN_OF.get(lang)
        if toolchain is None:
            return None
        return self.runtime_units.get(toolchain, {}).get(callee)

    def callee_refusal(self, callee, text, problem):
        """the refusal a runtime callee's own body earns, said as what
        it is rather than folded into the caller's `call` cause.

        The archives were read with `ar x` + `objdump -d`, and an
        object file's calls are UNRELOCATED: `call 46 <__divti3+0x46>`
        names an offset, not a symbol, because the symbol lives in the
        relocation table the extraction did not carry.  So a nested
        runtime call inside an attached body has no name to follow,
        and this is a census row rather than a guessed target."""
        mnemonic = L.mnemonic_of(text)
        if L.is_transfer(mnemonic):
            return ("the attached body of the runtime callee %r "
                    "contains the transfer %r, whose target the "
                    "attachment did not record: an archive member's "
                    "calls are unrelocated, so the nested callee has "
                    "no name to follow" % (callee, text))
        return ("the attached body of the runtime callee %r spells "
                "%r, which the shared opcode table refused: %s"
                % (callee, text, problem))

    def opcode_row(self, record, row, producer, line, shared, holder,
                   stack_rows, x87_rows):
        """the ordinary case: an arch opcode, or a flag pair.  The
        meaning comes from the shared table and from nowhere else."""
        name = row["row"]
        if line is None:
            raise NoTerm(
                "no body line was relinked to this row, so the width "
                "and the operand spellings this term needs are not "
                "available")
        blocked = self.blocked_operand(record, row)
        if blocked is not None:
            record.cascades.append(cascade_record(row, producer,
                                                  blocked))
            return
        row["_line"] = line
        state = self.seeded_state(record, row, shared, holder,
                                  stack_rows, x87_rows)
        self.check_operand_slots(record, row, line, holder)
        if producer["kind"] == "flag_pair":
            mnemonics = list(producer["mnem"])
        else:
            mnemonics = [producer["mnem"]]
        # A FLAG PAIR IS ONE ACT WITH TWO HALVES.  The setting half
        # already ran, when its own flags row was transcribed, and its
        # flag state is what `seeded_state` put back on the state; so
        # only the READING half is run here.  The setting half is
        # still looked up, because an unmodelled setter must be a
        # census row and not a silent gap.
        for mnemonic in mnemonics:
            self.entry_or_refuse(mnemonic)
        self.reference.step(state, line)
        record.rip_reads = state.rip_reads
        if state.flags is not None:
            record.flag_state[name] = state.flags
        value = self.read_produced(state, row, line, mnemonics)
        record.terms[name] = value

    def entry_or_refuse(self, mnemonic):
        """the shared table's entry for one mnemonic, or a written
        refusal that becomes a census row."""
        entry = self.opcode_table.entry_for(mnemonic)
        if entry is None:
            raise NoTerm(
                "arch opcode %r has no entry in the shared opcode "
                "table -- no body in the corpus that table was built "
                "over spells it" % mnemonic)
        if entry.build is None:
            if entry.cause is None:
                raise NoTerm(
                    "arch opcode %r has an entry in the shared opcode "
                    "table and no builder: it is a census row, not a "
                    "silent gap" % mnemonic)
            raise NoTerm(
                "arch opcode %r is a census row, not a silent gap: %s"
                % (mnemonic, entry.cause))
        return entry

    def blocked_operand(self, record, row):
        for name in row["operands"]:
            if name not in record.terms:
                return name
        return None

    def seeded_state(self, record, row, shared, holder, stack_rows,
                     x87_rows):
        """a fresh `MachineState` carrying, in its registers, the term
        of whichever row currently resides in each family -- the
        ledger's own wiring, not a second dataflow analysis."""
        state = R.MachineState(shared_seed=shared)
        state.rip_reads = record.rip_reads
        state.memory = record.memory
        for family, row_name in holder.items():
            term = record.terms.get(row_name)
            if term is None:
                continue
            if is_flag_state(term):
                continue
            state.set_family(family, at_family_width(family, term))
        for name in row["operands"]:
            if name in record.flag_state:
                state.flags = record.flag_state[name]
                break
            term = record.terms.get(name)
            if term is None:
                continue
            if is_flag_state(term):
                state.flags = term
                break
        if stack_rows:
            top = record.terms.get(stack_rows[-1])
            if top is not None:
                if not is_flag_state(top):
                    state.push_value(R.full64(top))
        self.seed_x87(record, row, state, x87_rows)
        return state

    def seed_x87(self, record, row, state, x87_rows):
        """the x87 stack, seeded from THIS ROW'S OWN OPERAND WIRING
        where the line names stack positions.

        WHY NOT PUSH ORDER.  `fxch` swaps two positions and makes no
        ledger row, so a stack rebuilt by pushing the X87 rows in
        their own order has the two operands the wrong way round after
        an exchange.  The ledger already resolved that: a row that
        reads the stack lists the X87 rows it reads IN THE ARCH TEXT'S
        OWN OPERAND ORDER, so `fucomip %st(1),%st` with operands
        ['X87-1', 'X87-0'] says position 1 holds X87-1 and position 0
        holds X87-0.  Reading the wiring is the transcription;
        replaying push order is a second dataflow analysis, and it was
        wrong -- measured on `c/regen_36772`, whose comparison came
        out reversed and was DISPROVED."""
        line = None
        placed = False
        texts = []
        if row.get("_line") is not None:
            line = row["_line"]
        if line is not None:
            texts = L.operands_of(line)
        wanted = []
        for text in texts:
            position = L.x87_position_of(text)
            if position is None:
                continue
            wanted.append(position)
        reads = []
        for name in row["operands"]:
            if not name.startswith("X87-"):
                continue
            reads.append(name)
        if wanted and len(wanted) == len(reads):
            depth = 0
            for position, name in zip(wanted, reads):
                term = record.terms.get(name)
                if term is None:
                    continue
                if is_flag_state(term):
                    continue
                state.x87_set(position, term)
                if position + 1 > depth:
                    depth = position + 1
                placed = True
            state.x87["depth"] = depth
        if placed:
            return
        for name in x87_rows:
            term = record.terms.get(name)
            if term is None:
                continue
            if is_flag_state(term):
                continue
            state.x87_push(term)

    def check_operand_slots(self, record, row, line, holder):
        """OPERAND SLOTS ARE CHECKED, NOT ASSUMED.  Every register
        operand the line spells is replayed against the holder map:
        the row the ledger says the value came from must be the row
        this file believes resides in that family.  A disagreement is
        RECORDED, never assumed away."""
        operands = L.operands_of(line)
        named = []
        for text in operands:
            if not text.startswith("%"):
                continue
            family = canon.FAMILY_OF.get(text[1:])
            if family is None:
                continue
            named.append((text, holder.get(family)))
        recorded = list(row["operands"])
        for text, row_name in named:
            if row_name is None:
                continue
            if row_name in recorded:
                continue
            record.slot_disagreements.append({
                "row": row["row"],
                "line": line,
                "operand": text,
                "the_holder_map_says": row_name,
                "the_ledger_row_reads": recorded,
            })

    def read_produced(self, state, row, line, mnemonics):
        """the value the builder wrote, read back off the state at the
        place the row itself says it resides."""
        if row.get("type") == FLAGS_ONLY:
            if state.flags is None:
                raise NoTerm(
                    "the builder for %r left no flag state, and this "
                    "row is a flags-only row" % mnemonics[-1])
            return state.flags
        resident = row.get("resident")
        if resident is not None:
            if resident.startswith(RESIDENT_STACK):
                cells = state.stack["cells"]
                if not cells:
                    raise NoTerm(
                        "the builder for %r moved nothing onto the "
                        "machine stack" % mnemonics[-1])
                newest = min(cells)
                return cells[newest]
        if row["block"] == "X87":
            top = state.x87_at(0)
            if top is None:
                raise NoTerm(
                    "the builder for %r left the x87 stack empty"
                    % mnemonics[-1])
            return top
        family = destination_family(row, line)
        if family is None:
            raise NoTerm(
                "this row names no place its value resides, and its "
                "body line names no destination register")
        if family not in state.registers:
            raise NoTerm(
                "the builder for %r wrote no value into %s, which is "
                "where this row says its value resides"
                % (mnemonics[-1], family))
        return R.cut(state.registers[family], row["size"] * 8)

    def remember_residence(self, record, row, line, holder, stack_rows,
                           x87_rows):
        """the HOLDER MAP, filled from the rows' own `resident` fields
        -- the ledger's wiring written down, never re-derived."""
        name = row["row"]
        if name not in record.terms:
            return
        kind = row["produced_by"].get("kind")
        if kind == "non_opcode_phrase":
            # A LITERAL DOES NOT RESIDE IN A REGISTER.  A CONST row is
            # the body's own immediate operand and an OWN row is a
            # stack address the body spells; neither is the value the
            # line's destination register holds.  Publishing them
            # would answer a later read of that register with the
            # immediate -- measured on `go/op_206`, where
            # `cmp $0x20,%rbx` made the CONST row the holder of the
            # second argument and the gate DISPROVED the unit.
            return
        if row["block"] == "STACK":
            stack_rows.append(name)
            return
        if row["block"] == "X87":
            x87_rows.append(name)
            return
        family = destination_family(row, line)
        if family is None:
            return
        if row.get("type") == FLAGS_ONLY:
            return
        holder[family] = name

    # ---------------------------------------------------------------
    # sub-node: normalize         (node 0_3_5_6_3)
    # ---------------------------------------------------------------

    def normalize(self, term):
        """THE FIXED RULE, the steps in order, exactly as the CORE
        numbers them: simplify ONCE; ORDER the arguments of every
        commutative operator by a key computed from the arguments
        themselves; rename free symbols positionally `v0`, `v1`, ... in
        first-met order; simplify and order the substituted term once
        more; print on one line.

        THE ORDERING STEPS were added 2026-09-03 (task 79), after
        log_169 section 5.3 measured that 1,479 of 26,594 units printed
        a DIFFERENT text on a second walk of the same rule over the
        same unit -- because `z3.simplify` orders a commutative
        operator's arguments by the solver's internal node identity,
        which is a function of what the process built earlier and not
        of the unit.  The ordering is keyed on the sub-term itself
        (`order_commutative` below), never on that identity.

        THE ORDERING NOW RUNS BEFORE THE FIRST SIMPLIFICATION TOO
        (2026-09-07, task t104).  Task 79 put the ordering AFTER each
        simplification, which leaves the first `z3.simplify` looking at
        an UNORDERED term -- and the simplifier is not itself
        order-invariant: a term and its operand-permuted twin can leave
        it in shapes that differ by more than operand order, and no
        ordering afterwards can undo that.  MEASURED before the change,
        over the 27,682 proved units one walk printed: a second term
        built from each unit's own term by permuting the operands of
        every commutative node prints a DIFFERENT text for 899 of them,
        and the solver says the permuted term is the same computation.
        With this one extra call the same measurement reads 0.
        Evidence: `t104_order_probe.json`, `t104_audit.json`.

        The result is a COMPARISON KEY computed beside the runnable
        text, never instead of it, and it is computed only for a term
        the gate PROVED."""
        simplified = order_commutative(term)
        simplified = z3.simplify(simplified)
        simplified = order_commutative(simplified)
        symbols = ordered_symbols(simplified)
        substitution = []
        for index, symbol in enumerate(symbols):
            if symbol.sort().kind() == z3.Z3_BV_SORT:
                fresh = z3.BitVec("v%d" % index, symbol.size())
            else:
                fresh = z3.Const("v%d" % index, symbol.sort())
            substitution.append((symbol, fresh))
        if substitution:
            simplified = z3.substitute(simplified, *substitution)
        simplified = z3.simplify(simplified)
        simplified = order_commutative(simplified)
        return one_line(simplified)

    # ---------------------------------------------------------------
    # sub-node: census            (node 0_3_5_6_4)
    # ---------------------------------------------------------------

    def census(self, records):
        """THE FILTER, never a survey.  Over a population of
        transcriptions, the rows whose producer has no builder, grouped
        one entry per producer, each entry carrying rows blocked,
        units, languages and the WRITTEN REASON SENTENCE that a later
        round's delta is matched on.

        Producers are typed objects, never bare strings, so the
        spelling guard reads a machine form and not a token."""
        entries = {}
        for lang, name, record in records:
            for hole in record.holes:
                key = producer_key(hole["producer"])
                entry = entries.get(key)
                if entry is None:
                    entry = {
                        "producer": hole["producer"],
                        "rows_blocked": 0,
                        "units": [],
                        "languages": [],
                        "reasons": [],
                    }
                    entries[key] = entry
                entry["rows_blocked"] += 1
                if name not in entry["units"]:
                    entry["units"].append(name)
                if lang not in entry["languages"]:
                    entry["languages"].append(lang)
                if hole["why"] not in entry["reasons"]:
                    entry["reasons"].append(hole["why"])
        out = []
        for key in sorted(entries):
            entry = entries[key]
            entry["units_blocked"] = len(entry["units"])
            entry["units"] = sorted(entry["units"])[:40]
            entry["languages"] = sorted(entry["languages"])
            entry["reasons"] = sorted(entry["reasons"])
            out.append(entry)
        out.sort(key=lambda one: (-one["rows_blocked"],
                                  producer_key(one["producer"])))
        return out

    def census_delta(self, before, after):
        """(census_before, census_after) -> what closed and what
        appeared, MATCHED ON THE RECORDED REASON SENTENCE, which is
        the census CORE's own rule -- not on a producer's spelling."""
        was = {}
        for entry in before:
            for reason in entry.get("reasons") or []:
                was.setdefault(reason, 0)
                was[reason] += entry["rows_blocked"]
        now = {}
        for entry in after:
            for reason in entry.get("reasons") or []:
                now.setdefault(reason, 0)
                now[reason] += entry["rows_blocked"]
        closed = []
        appeared = []
        moved = []
        for reason in sorted(was):
            if reason not in now:
                closed.append({"reason": reason,
                               "rows_that_were_blocked": was[reason]})
                continue
            if now[reason] != was[reason]:
                moved.append({"reason": reason,
                              "was": was[reason],
                              "now": now[reason]})
        for reason in sorted(now):
            if reason not in was:
                appeared.append({"reason": reason,
                                 "rows_blocked": now[reason]})
        return {"closed": closed, "appeared": appeared,
                "moved": moved}

    # ---------------------------------------------------------------
    # sub-node: render_back       (node 0_3_5_6_5) -- PLANNED
    # ---------------------------------------------------------------

    def render_back(self, term, unit):
        """z3 term -> a wrapped arch text that computes the same value.

        THE RETURN PATH.  Built 2026-09-03 (task 66), closing the debt
        log_147 section 8.1 named and the CORE of node 0_3_5_6_5
        carries.  The sub-node's own methods are the class
        `RenderBack` below; this method is the term node's door to
        them, so `Term` still holds every method the term CORE names.

        Returns a `Rendering`.  A term the fixed rule has no template
        for is REFUSED BY NAME and never rendered approximately."""
        renderer = RenderBack(self.reference)
        return renderer.render_and_wrap(term, unit)


# ==================================================================
# section 4: the small shared helpers
# ==================================================================

def seed_of(shared, family):
    """the reference simulator's own symbol for a register family."""
    if family in shared:
        return shared[family]
    if family in R.XMM_NAMES:
        bits = 128
    else:
        bits = 64
    shared[family] = z3.BitVec("seed_%s" % family, bits)
    return shared[family]


def at_family_width(family, term):
    """a register family holds 128 bits when it is a vector family and
    64 otherwise; a row's term is cut or grown to that, because a row
    carries a size and a register carries a width and the two are not
    the same fact."""
    if family in R.XMM_NAMES:
        return R.cut(term, 128)
    return R.full64(term)


def is_flag_state(term):
    """a flags row holds the `(setter, left, right)` triple the shared
    table's flag builders leave, not a bit-vector."""
    return isinstance(term, tuple)


def producer_key(producer):
    """a stable sort key for a TYPED producer object.  The key is built
    from the object's own fields, which are machine form."""
    kind = producer.get("kind")
    if kind == "flag_pair":
        return "flag_pair:" + ",".join(producer.get("mnem") or [])
    if kind == "non_opcode_phrase":
        return "non_opcode_phrase:" + str(producer.get("phrase"))
    if kind == "runtime_callee":
        return "runtime_callee:" + str(producer.get("callee"))
    return "arch_opcode:" + str(producer.get("mnem"))


def hole_record(row, producer, line, why):
    return {
        "row": row["row"],
        "block": row["block"],
        "producer": producer,
        "line": line,
        "why": why,
    }


def cascade_record(row, producer, blocked):
    """a row whose PRODUCER has a term but whose operand row does not.
    It is not a census entry -- the census filters on the producer, and
    this row's producer is modelled -- so it is counted separately and
    one hole is never reported as many."""
    return {
        "row": row["row"],
        "producer": producer,
        "blocked_by": blocked,
        "why": "an operand row has no term: %s" % blocked,
    }


def free_symbols_in_order(term):
    """every free symbol, in the order a left-to-right walk meets it."""
    seen = []
    known = set()
    stack = [term]
    while stack:
        node = stack.pop()
        if z3.is_const(node):
            if node.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                key = node.decl().name()
                if key not in known:
                    known.add(key)
                    seen.append(node)
                continue
        children = list(node.children())
        children.reverse()
        stack.extend(children)
    return seen


def ordered_symbols(term):
    """the same list, in the order the PRINTED term shows them, so the
    renaming is a function of the printed shape and nothing else."""
    text = term.sexpr()
    found = free_symbols_in_order(term)

    def position(symbol):
        where = text.find(symbol.decl().name())
        if where >= 0:
            return where
        return len(text)

    return sorted(found, key=position)


# The declaration kinds whose arguments may be put in any order
# without changing the value.  Each is commutative in the solver's own
# semantics, so a fixed order over the argument list is a PRINTING
# choice and never a semantic one.  The float ones are here because the
# residue round 14 measured -- 39 of the 582 `c` units still printing
# differently when the walk order was reversed -- was made ENTIRELY of
# float units, whose adds and multiplies the round-14 table did not
# list.  (Task 79, 2026-09-03; CORE 0_3_5_6_3 design step 2.)
COMMUTATIVE_OPERATORS = frozenset([
    z3.Z3_OP_AND,
    z3.Z3_OP_OR,
    z3.Z3_OP_XOR,
    z3.Z3_OP_EQ,
    z3.Z3_OP_DISTINCT,
    z3.Z3_OP_ADD,
    z3.Z3_OP_MUL,
    z3.Z3_OP_BADD,
    z3.Z3_OP_BMUL,
    z3.Z3_OP_BAND,
    z3.Z3_OP_BOR,
    z3.Z3_OP_BXOR,
    z3.Z3_OP_FPA_EQ,
])

# The same, for an operator that carries a ROUNDING MODE as its first
# argument.  The rounding mode stays where it is; only the value
# arguments after it are put in order.
ROUNDED_COMMUTATIVE_OPERATORS = frozenset([
    z3.Z3_OP_FPA_ADD,
    z3.Z3_OP_FPA_MUL,
])


def operator_name(node):
    """the operator's own name WITH ITS PARAMETERS.

    `Extract(63, 0, x)` and `Extract(127, 64, x)` are different
    operators reading different bits, and z3 spells both `extract`.
    Leaving the parameters out of the key made those two arguments tie,
    and a tie is settled by whatever order the term arrived in -- which
    is the solver's node identity, the very thing this rule removes.
    Half of task 79's first residue was exactly that."""
    declaration = node.decl()
    name = declaration.name()
    try:
        parameters = declaration.params()
    except Exception:
        parameters = []
    if not parameters:
        return name
    spelled = []
    for one in parameters:
        spelled.append(str(one))
    return "%s[%s]" % (name, ",".join(spelled))


def ordering_key(node, cache):
    """(the rebuilt node, its SHAPE key, its CONCRETE key), bottom-up,
    computed with an explicit stack so a deep term cannot exhaust
    Python's own call stack.

    The shape key writes every free symbol as its SORT alone, so no
    register name can decide an order -- two units computing the same
    thing through different registers order their arguments the same
    way.  The concrete key is the same string with the symbols' own
    names, and it breaks a tie between two arguments of identical
    shape, which is a fact of the unit and not of the process."""
    stack = [(node, False)]
    while stack:
        current, expanded = stack.pop()
        key = current.get_id()
        if key in cache:
            continue
        if not z3.is_app(current):
            spelled = str(current)
            cache[key] = (current, spelled, spelled)
            continue
        if not expanded:
            stack.append((current, True))
            for index in range(current.num_args()):
                stack.append((current.arg(index), False))
            continue
        cache[key] = rebuilt_node(current, cache)
    return cache[node.get_id()]


def rebuilt_node(current, cache):
    """one node of `ordering_key`'s walk, with every argument already
    in the cache."""
    declaration = current.decl()
    kind = declaration.kind()
    name = operator_name(current)
    sort_text = current.sort().sexpr()
    if current.num_args() == 0:
        if kind == z3.Z3_OP_UNINTERPRETED:
            shape = "?" + sort_text
        else:
            shape = name + ":" + sort_text
        concrete = name + ":" + sort_text
        return (current, shape, concrete)
    pieces = []
    for index in range(current.num_args()):
        pieces.append(cache[current.arg(index).get_id()])
    if kind in COMMUTATIVE_OPERATORS:
        if len(pieces) > 1:
            pieces = sorted(pieces, key=argument_order)
    elif kind in ROUNDED_COMMUTATIVE_OPERATORS:
        if len(pieces) > 2:
            head = pieces[:1]
            rest = sorted(pieces[1:], key=argument_order)
            pieces = head + rest
    arguments = []
    shapes = []
    concretes = []
    for piece in pieces:
        arguments.append(piece[0])
        shapes.append(piece[1])
        concretes.append(piece[2])
    rebuilt = declaration(*arguments)
    shape = "(%s %s)" % (name, " ".join(shapes))
    concrete = "(%s %s)" % (name, " ".join(concretes))
    return (rebuilt, shape, concrete)


def argument_order(piece):
    """the order of one argument: its shape key first, its concrete key
    as the tie-break.  Both are computed from the argument itself."""
    return (piece[1], piece[2])


def order_commutative(term):
    """THE ORDERING STEP (CORE 0_3_5_6_3, design step 2 and step 4).

    A term -> the same term with the arguments of every commutative
    operator in a fixed order that depends only on the arguments
    themselves.  It is what makes the layer-5 text a function of the
    unit: `z3.simplify` orders those arguments by the solver's internal
    node identity, which depends on what the process built earlier, so
    without this step the same unit prints differently depending on
    which units were walked before it."""
    cache = {}
    answer = ordering_key(term, cache)
    return answer[0]


def one_line(term):
    z3.set_option(max_width=1000000, max_lines=1000000,
                  max_depth=1000000, max_args=1000000)
    text = str(term)
    text = " ".join(text.split())
    return text


TERM = Term()


# ==================================================================
# section 5: THE SUB-NODE `render_back` (node 0_3_5_6_5)
#
# THE RETURN PATH.  AgentMemory, "THE CANONICAL FORM IS ENFORCED"
# (the owner, 2026-08-26): "Tools may transform (lift, z3-simplify,
# e-graphs) ONLY with a RETURN PATH: a valid simplified expression is
# rendered back into canonical runnable instructions; a result that
# cannot return is an intermediate, not a result."  This section IS
# that return path.
#
# THE INVERSE MAP COMES FROM THE ONE TABLE.  Every template below is
# an entry of `reference.Reference.opcode_table` READ BACKWARDS: the
# mnemonic is named here only because a builder there produces that z3
# operator, and only where the table actually holds the mnemonic (the
# table is pruned to the mnemonics the corpus's own bodies spell, so a
# template for `movzwq` -- which no body spells -- is not written).
# No second table of meanings exists in this file.
#
# WHERE TEMPORARIES LIVE.  A rendered body may not spell the ledger
# symbol -- `canonical_form.CanonicalForm.wrap` refuses a body that
# does -- so an intermediate is held in a register of the fixed
# ordered pool and BECOMES a TEMP row when `ledger.Ledger.walk_dataflow`
# walks the rendered body, exactly as every layer-3 body's
# intermediates already become TEMP rows.  The pool is assigned in
# first-needed order and exhaustion is a loud refusal; there is no
# limit of two (AgentMemory, the owner 2026-08-28).
# ==================================================================

REGISTER_WIDTHS = (8, 16, 32, 64)


class NoTemplate(Exception):
    """the fixed rule has no instruction template for this z3
    operator, or no register wide enough for this value.  Refused by
    name; nothing approximate is rendered.

    `cause` is the SHORT CAUSE the report groups on -- the z3 operator
    that has no template, or the shape that has none.  Without it every
    refusal collapses into one line reading "no template", which is
    reporting by sighting dressed as reporting by cause
    (LLM_communication_protocol section 5.3)."""

    def __init__(self, why, cause=None):
        Exception.__init__(self, why)
        self.why = why
        if cause is None:
            cause = "no template"
        self.cause = cause


class Rendering(object):
    """one unit's return path, whatever became of it."""

    def __init__(self, unit_name):
        self.unit = unit_name
        self.body = None
        self.wrapped_text = None
        self.fields = None
        self.refused = None
        self.refusal_cause = None


# -- the inverse map, one entry per z3 operator ---------------------
#
# left column: the z3 operator a `reference` builder produces.
# right column: the mnemonic whose builder produces it, and the shape
# of the instruction the template writes.

TWO_PLACE_MNEMONIC = {
    z3.Z3_OP_BADD: "add",
    z3.Z3_OP_BSUB: "sub",
    z3.Z3_OP_BAND: "and",
    z3.Z3_OP_BOR: "or",
    z3.Z3_OP_BXOR: "xor",
    z3.Z3_OP_BMUL: "imul",
}
"""`build_binary` in `reference.py` reads the destination and the
source at the destination's width and writes `left <op> right` back to
the destination.  Inverted: the destination register carries the left
sub-term, the source register carries the right, and the mnemonic is
the one whose branch of `build_binary` produces that operator."""

ONE_PLACE_MNEMONIC = {
    z3.Z3_OP_BNOT: "not",
    z3.Z3_OP_BNEG: "neg",
}
"""`build_unary`: `not` produces `~value`, `neg` produces `-value`."""

SHIFT_MNEMONIC = {
    z3.Z3_OP_BSHL: "shl",
    z3.Z3_OP_BLSHR: "shr",
    z3.Z3_OP_BASHR: "sar",
}
"""`build_shift`, whose count operand this file writes as an immediate
-- the only count shape `build_shift` models besides `%cl`."""

SIGN_EXTEND_MNEMONIC = {
    (8, 32): "movsbl",
    (8, 64): "movsbq",
    (16, 32): "movswl",
    (32, 64): "movslq",
}
"""`build_extension(..., signed=True)`.  Only the four pairs the one
table actually holds: `SIGN_EXTEND` is pruned to the corpus's own
mnemonics, so `movsbw` and `movswq` have no entry and no template."""

ZERO_EXTEND_MNEMONIC = {
    (8, 32): "movzbl",
    (16, 32): "movzwl",
}
"""`build_extension(..., signed=False)`, the two the table holds."""

PREDICATE_CONDITION = {
    z3.Z3_OP_EQ: "CondEQ",
    z3.Z3_OP_DISTINCT: "CondNE",
    z3.Z3_OP_SLT: "CondSLT",
    z3.Z3_OP_SLEQ: "CondSLE",
    z3.Z3_OP_SGT: "CondSGT",
    z3.Z3_OP_SGEQ: "CondSGE",
    z3.Z3_OP_ULT: "CondULT",
    z3.Z3_OP_ULEQ: "CondULE",
    z3.Z3_OP_UGT: "CondUGT",
    z3.Z3_OP_UGEQ: "CondUGE",
}
"""`condition_table.cond_to_z3` READ BACKWARDS -- the one function
`reference.predicate_of` calls to say what a condition suffix means.
Its body reads `if cond == "CondSLT": return L < R`; this table is
that line, and its nine co-lines, the other way round.  The two
conditions `cond_to_z3` writes as arithmetic on the difference
(`CondSGN`, `CondNSGN`) and the two it writes as a parity fold
(`CondPAR`, `CondNPAR`) have no entry here on purpose: z3 does not
print them as one operator, so no shape of a term names them, and a
term that reaches this rule carrying one of their expansions renders
through the ordinary operators the expansion is made of."""

CONDITION_WIDTHS = (8, 16, 32, 64)
"""the widths a `cmp` may compare at.  The same four register widths
the rest of this rule writes."""

MOVE_CONDITION_WIDTHS = (16, 32, 64)
"""THE MACHINE HAS NO 8-BIT CONDITIONAL MOVE.  `cmov` exists at 16, 32
and 64 bits only, which is why an 8-bit choice whose arms are not the
two literals is refused by name rather than rendered as a mask the
corpus never writes."""


def register_at(family, width):
    """the fixed spelling of a pool register at one width, through
    `ledger.register_text`, so no second naming rule is written."""
    return L.register_text(family, width)


def immediate_text(value, width):
    """a z3 constant printed as the AT&T immediate a `build_binary` or
    `build_plain_move` operand slot reads."""
    masked = value & ((1 << width) - 1)
    return "$0x%x" % masked


class RenderBack(object):
    """the sub-node.  Its methods are the CORE's: `template_table` and
    `temp_pool` as attributes, `render`, `wrap_rendered`, `verify` and
    `refuse` as methods."""

    def __init__(self, reference=None):
        if reference is None:
            reference = R.REFERENCE
        self.reference = reference
        self.template_table = {
            "two_place": TWO_PLACE_MNEMONIC,
            "one_place": ONE_PLACE_MNEMONIC,
            "shift": SHIFT_MNEMONIC,
            "sign_extend": SIGN_EXTEND_MNEMONIC,
            "zero_extend": ZERO_EXTEND_MNEMONIC,
        }
        self.check_templates_against_the_one_table()
        self.condition_suffix = self.suffix_per_condition()
        self.complement = self.complement_per_condition()
        self.set_mnemonic = self.reader_mnemonics("set")
        self.move_mnemonic = self.reader_mnemonics("cmov")
        self.template_table["condition_suffix"] = self.condition_suffix
        self.template_table["set_condition"] = self.set_mnemonic
        self.template_table["move_condition"] = self.move_mnemonic

    # -- the condition table, derived and never typed in -------------

    def suffix_per_condition(self):
        """condition name -> the ONE suffix this rule writes.

        `condition_table.SUFFIX_TO_COND` READ BACKWARDS.  A condition
        has several spellings on this machine (`ae`, `nb`, `nc` are
        one condition); the rule picks the shortest, ties by alphabet,
        so the choice is deterministic and no judgment enters.
        MEASURED CONFIRMATION, recorded rather than assumed: the 14
        suffixes this picks are character-for-character the 14 the
        corpus's own ship bodies write
        (`probe80_conditional_shapes_printed.txt`)."""
        out = {}
        for suffix in sorted(R.CT.SUFFIX_TO_COND):
            condition = R.CT.SUFFIX_TO_COND[suffix]
            if condition not in out:
                out[condition] = suffix
                continue
            standing = out[condition]
            if (len(suffix), suffix) < (len(standing), standing):
                out[condition] = suffix
        return out

    def complement_per_condition(self):
        """condition name -> the condition that is its negation, PROVED
        out of `condition_table.cond_to_z3` rather than typed in.

        WHY THIS IS NOT A TABLE.  z3's simplifier prints `a != b` as
        `Not(a == b)` and `a >= b` as `Not(a < b)`, so a rendering has
        to know which suffix answers the negation of which.  Writing
        those pairs down would be a second table of meanings, which
        this file does not do.  Instead each pair is asked of the one
        function that gives the conditions their meaning: two
        conditions are complements when no starting state makes one
        differ from the negation of the other."""
        left = z3.BitVec("cond_left", 64)
        right = z3.BitVec("cond_right", 64)
        names = sorted(set(R.CT.SUFFIX_TO_COND.values()))
        built = {}
        for name in names:
            built[name] = R.CT.cond_to_z3(name, left, right, z3)
        out = {}
        for name in names:
            for other in names:
                solver = z3.Solver()
                solver.add(built[other] != z3.Not(built[name]))
                if solver.check() == z3.unsat:
                    out[name] = other
                    break
        return out

    def reader_mnemonics(self, prefix):
        """condition name -> the flag-READING mnemonic, kept ONLY where
        the one opcode table holds it WITH a builder.

        The table is pruned to the mnemonics the corpus's own bodies
        spell, so `cmovg` is absent from it -- no body writes one --
        and therefore no template is written for it here either.  A
        term whose choice wants that mnemonic is refused by name at
        render time, which is the same discipline `movsbw` already
        gets."""
        out = {}
        for condition in sorted(self.condition_suffix):
            suffix = self.condition_suffix[condition]
            mnemonic = prefix + suffix
            entry = self.reference.opcode_table.entry_for(mnemonic)
            if entry is None:
                continue
            if entry.build is None:
                continue
            out[condition] = mnemonic
        return out

    def check_templates_against_the_one_table(self):
        """EVERY template names a mnemonic the one table holds WITH a
        builder.  A template for an opcode the table does not model
        would be a second table sneaking in, and would render text the
        gate's own reference cannot read."""
        wanted = []
        wanted.extend(TWO_PLACE_MNEMONIC.values())
        wanted.extend(ONE_PLACE_MNEMONIC.values())
        wanted.extend(SHIFT_MNEMONIC.values())
        wanted.extend(SIGN_EXTEND_MNEMONIC.values())
        wanted.extend(ZERO_EXTEND_MNEMONIC.values())
        wanted.append("mov")
        wanted.append("movabs")
        wanted.append("cmp")
        for mnemonic in sorted(set(wanted)):
            entry = self.reference.opcode_table.entry_for(mnemonic)
            if entry is None:
                raise NoTemplate(
                    "the inverse map names %r, which the one opcode "
                    "table does not hold" % mnemonic)
            if entry.build is None:
                raise NoTemplate(
                    "the inverse map names %r, which the one opcode "
                    "table holds with no builder" % mnemonic)

    # -- the pool ----------------------------------------------------

    def temp_pool(self, arrival_families):
        """the fixed ordered pool, minus the unit's own arrival
        families and the never-renamed registers.  Assigned in
        first-needed order by walk depth."""
        reserved = set(arrival_families) | set(canon.NEVER_RENAME)
        out = []
        for family in L.SCRATCH_POOL:
            if family in reserved:
                continue
            if L.is_vector_family(family):
                continue
            out.append(family)
        return out

    # -- render ------------------------------------------------------

    def render(self, term, arrival_families, result_family,
               result_width):
        """z3 term -> the body lines, ending in `ret`.

        A post-order walk.  `emit` computes a sub-term into the pool
        register at its own depth and returns the width it left there;
        the root is then moved into the answer register at the answer
        width, which is where the epilogue's store reads it."""
        pool = self.temp_pool(arrival_families)
        lines = []
        width = self.emit(term, 0, pool, lines, arrival_families)
        if width < result_width:
            raise NoTemplate(
                "the term is %d bits wide and the answer home is %d, "
                "and no widening rule is ruled for the difference"
                % (width, result_width),
                "the term is narrower than the answer home")
        source = register_at(pool[0], result_width)
        destination = register_at(result_family, result_width)
        if source != destination:
            lines.append("mov %s,%s" % (source, destination))
        lines.append("ret")
        return lines

    def take(self, pool, depth):
        if depth >= len(pool):
            raise NoTemplate(
                "the fixed temp pool holds %d registers and this term "
                "needs a %dth: the pool is exhausted, which is a loud "
                "refusal and never a silent spill"
                % (len(pool), depth + 1),
                "the fixed temp pool is exhausted")
        return pool[depth]

    def width_of(self, node):
        size = node.size()
        if size not in REGISTER_WIDTHS:
            raise NoTemplate(
                "a value of %d bits fits no register width this rule "
                "writes (%s)"
                % (size, ", ".join("%d" % one
                                   for one in REGISTER_WIDTHS)),
                "a value of %d bits fits no register width" % size)
        return size

    def emit(self, node, depth, pool, lines, arrival_families):
        """one sub-term into the pool register at `depth`; returns the
        width the value was left at."""
        if not z3.is_bv(node):
            raise NoTemplate(
                "the term is of sort %s, and this rule renders bit "
                "vectors only" % node.sort(),
                "the term is of sort %s, not a bit vector"
                % node.sort())
        if z3.is_bv_value(node):
            return self.emit_constant(node, depth, pool, lines)
        if z3.is_const(node):
            return self.emit_symbol(node, depth, pool, lines,
                                    arrival_families)
        kind = node.decl().kind()
        if kind in TWO_PLACE_MNEMONIC:
            return self.emit_two_place(node, kind, depth, pool, lines,
                                       arrival_families)
        if kind in ONE_PLACE_MNEMONIC:
            return self.emit_one_place(node, kind, depth, pool, lines,
                                       arrival_families)
        if kind in SHIFT_MNEMONIC:
            return self.emit_shift(node, kind, depth, pool, lines,
                                   arrival_families)
        if kind == z3.Z3_OP_SIGN_EXT:
            return self.emit_extend(node, depth, pool, lines,
                                    arrival_families,
                                    SIGN_EXTEND_MNEMONIC, True)
        if kind == z3.Z3_OP_ZERO_EXT:
            return self.emit_extend(node, depth, pool, lines,
                                    arrival_families,
                                    ZERO_EXTEND_MNEMONIC, False)
        if kind == z3.Z3_OP_EXTRACT:
            return self.emit_extract(node, depth, pool, lines,
                                     arrival_families)
        if kind == z3.Z3_OP_CONCAT:
            return self.emit_concat(node, depth, pool, lines,
                                    arrival_families)
        if kind == z3.Z3_OP_ITE:
            return self.emit_choice(node, depth, pool, lines,
                                    arrival_families)
        raise NoTemplate(
            "no instruction template is written for the z3 operator "
            "%r, so this term has no return path by the fixed rule"
            % node.decl().name(),
            "no template for the z3 operator %r" % node.decl().name())

    def emit_constant(self, node, depth, pool, lines):
        """a literal -> `mov $imm,%r`, or `movabs` where the value
        does not fit a 32-bit immediate field."""
        width = self.width_of(node)
        family = self.take(pool, depth)
        value = node.as_long()
        destination = register_at(family, width)
        if width == 64 and value >= (1 << 31):
            lines.append("movabs %s,%s"
                         % (immediate_text(value, 64), destination))
            return 64
        lines.append("mov %s,%s"
                     % (immediate_text(value, width), destination))
        return width

    def emit_symbol(self, node, depth, pool, lines, arrival_families):
        """a free symbol -> the arrival register the prelude fills from
        that symbol's own IN row.

        THE SYMBOLS ARE THE REFERENCE'S OWN.  `term.transcribe` binds
        IN-i to `seed_<family>` for the family the arrival contract
        names at i, so a free symbol IS an input row, named by its
        register family."""
        name = node.decl().name()
        if not name.startswith("seed_"):
            raise NoTemplate(
                "the term carries the free symbol %r, which is not an "
                "input row of this unit and therefore names no place "
                "the runner fills" % name,
                "a free symbol that is not an input row")
        family = name[len("seed_"):]
        if family not in arrival_families:
            raise NoTemplate(
                "the term reads the register family %r, which this "
                "unit's arrival contract does not name, so no input "
                "row carries it" % family,
                "the term reads a register the arrival contract does "
                "not name")
        width = self.width_of(node)
        destination = self.take(pool, depth)
        source_text = register_at(family, width)
        destination_text = register_at(destination, width)
        lines.append("mov %s,%s" % (source_text, destination_text))
        return width

    def emit_two_place(self, node, kind, depth, pool, lines,
                       arrival_families):
        """`build_binary` inverted: the left sub-term into the
        destination register, the right into the next pool register,
        then the mnemonic over the two.  z3's add / and / or / xor /
        multiply are n-ary, so a run of arguments folds left."""
        width = self.width_of(node)
        children = node.children()
        if len(children) < 2:
            raise NoTemplate(
                "a two-place operator with %d arguments has no "
                "template" % len(children))
        mnemonic = TWO_PLACE_MNEMONIC[kind]
        if mnemonic == "imul" and width == 8:
            # THE MACHINE HAS NO TWO-OPERAND 8-BIT MULTIPLY.  `imul`
            # in its two-operand form exists at 16, 32 and 64 bits
            # only; the 8-bit multiply is the one-operand form over
            # the accumulator pair, which `build_wide_multiply`
            # models and which writes two places, not one.  `as`
            # refuses `imul %r10b,%r11b` with "operand size mismatch"
            # -- measured on 85 rust units before this refusal
            # existed -- so the rule refuses it here by name rather
            # than emitting text the assembler rejects.
            raise NoTemplate(
                "an 8-bit multiply has no two-operand instruction on "
                "this machine, and the one-operand form writes the "
                "accumulator pair rather than one register",
                "an 8-bit multiply has no two-operand instruction")
        left = self.take(pool, depth)
        right = self.take(pool, depth + 1)
        first = self.emit(children[0], depth, pool, lines,
                          arrival_families)
        if first != width:
            raise NoTemplate(
                "a two-place operand came back %d bits wide where the "
                "result is %d" % (first, width))
        for child in children[1:]:
            other = self.emit(child, depth + 1, pool, lines,
                              arrival_families)
            if other != width:
                raise NoTemplate(
                    "a two-place operand came back %d bits wide where "
                    "the result is %d" % (other, width))
            lines.append("%s %s,%s"
                         % (mnemonic, register_at(right, width),
                            register_at(left, width)))
        return width

    def emit_one_place(self, node, kind, depth, pool, lines,
                       arrival_families):
        """`build_unary` inverted."""
        width = self.width_of(node)
        children = node.children()
        if len(children) != 1:
            raise NoTemplate(
                "a one-place operator with %d arguments has no "
                "template" % len(children))
        family = self.take(pool, depth)
        inner = self.emit(children[0], depth, pool, lines,
                          arrival_families)
        if inner != width:
            raise NoTemplate(
                "a one-place operand came back %d bits wide where the "
                "result is %d" % (inner, width))
        mnemonic = ONE_PLACE_MNEMONIC[kind]
        lines.append("%s %s" % (mnemonic, register_at(family, width)))
        return width

    def emit_shift(self, node, kind, depth, pool, lines,
                   arrival_families):
        """`build_shift` inverted, immediate count only -- the one
        count shape besides `%cl` that builder models."""
        width = self.width_of(node)
        children = node.children()
        if len(children) != 2:
            raise NoTemplate(
                "a shift with %d arguments has no template"
                % len(children))
        count = children[1]
        if not z3.is_bv_value(count):
            raise NoTemplate(
                "a shift whose count is not a literal has no "
                "template: `build_shift` models an immediate count "
                "and `%cl`, and this rule writes the immediate",
                "a shift whose count is not a literal")
        family = self.take(pool, depth)
        inner = self.emit(children[0], depth, pool, lines,
                          arrival_families)
        if inner != width:
            raise NoTemplate(
                "a shift operand came back %d bits wide where the "
                "result is %d" % (inner, width))
        amount = count.as_long() & R.shift_mask(width)
        mnemonic = SHIFT_MNEMONIC[kind]
        lines.append("%s $0x%x,%s"
                     % (mnemonic, amount, register_at(family, width)))
        return width

    def emit_extend(self, node, depth, pool, lines, arrival_families,
                    table, signed):
        """`build_extension` inverted.  The 32-to-64 zero extension is
        `mov %eXX,%eXX`, which is what the machine and
        `build_plain_move` both already do: a 32-bit write is a 64-bit
        zero-extending write."""
        children = node.children()
        inner_width = children[0].size()
        width = self.width_of(node)
        family = self.take(pool, depth)
        got = self.emit(children[0], depth, pool, lines,
                        arrival_families)
        if got != inner_width:
            raise NoTemplate(
                "an extension operand came back %d bits wide where "
                "the term says %d" % (got, inner_width))
        if not signed and inner_width == 32 and width == 64:
            lines.append("mov %s,%s"
                         % (register_at(family, 32),
                            register_at(family, 32)))
            return 64
        mnemonic = table.get((inner_width, width))
        if mnemonic is None:
            raise NoTemplate(
                "no widening template is written for %d bits to %d "
                "bits: the one opcode table holds no such mnemonic "
                "because no body in the corpus spells one"
                % (inner_width, width),
                "no widening template for %d bits to %d bits"
                % (inner_width, width))
        lines.append("%s %s,%s"
                     % (mnemonic, register_at(family, inner_width),
                        register_at(family, width)))
        return width

    def emit_extract(self, node, depth, pool, lines, arrival_families):
        """a slice.  A low slice at a register width is the same
        register read narrower and needs no instruction; a slice
        starting above bit 0 is a right shift first."""
        high = node.params()[0]
        low = node.params()[1]
        width = self.width_of(node)
        children = node.children()
        inner_width = children[0].size()
        family = self.take(pool, depth)
        got = self.emit(children[0], depth, pool, lines,
                        arrival_families)
        if got != inner_width:
            raise NoTemplate(
                "a slice operand came back %d bits wide where the "
                "term says %d" % (got, inner_width))
        if low == 0:
            return width
        if inner_width not in REGISTER_WIDTHS:
            raise NoTemplate(
                "a slice out of a %d-bit value fits no register width"
                % inner_width)
        amount = low & R.shift_mask(inner_width)
        if amount != low:
            raise NoTemplate(
                "a slice starting at bit %d needs a shift the machine "
                "masks to %d" % (low, amount))
        lines.append("shr $0x%x,%s"
                     % (amount, register_at(family, inner_width)))
        if high - low + 1 != width:
            raise NoTemplate("a slice of inconsistent width")
        return width

    def emit_concat(self, node, depth, pool, lines, arrival_families):
        """a joining of pieces.  THE ONE SHAPE WITH A TEMPLATE is a
        zero literal on top of one value -- which is a ZERO EXTENSION,
        the thing `build_extension(..., signed=False)` produces and
        which z3's simplifier prints as a `concat`.  So this is not a
        new meaning: it is the same table entry reached under the
        printed shape the simplifier leaves.  Every other joining is
        refused by name."""
        children = node.children()
        if len(children) != 2:
            raise NoTemplate(
                "a joining of %d pieces has no template"
                % len(children),
                "a joining of %d pieces" % len(children))
        head = children[0]
        if not z3.is_bv_value(head):
            raise NoTemplate(
                "a joining whose upper piece is not a literal has no "
                "template",
                "a joining whose upper piece is not a literal")
        if head.as_long() != 0:
            raise NoTemplate(
                "a joining whose upper piece is the literal %d and "
                "not zero is not a zero extension and has no template"
                % head.as_long(),
                "a joining whose upper piece is a literal other than "
                "zero")
        inner_width = children[1].size()
        width = self.width_of(node)
        family = self.take(pool, depth)
        got = self.emit(children[1], depth, pool, lines,
                        arrival_families)
        if got != inner_width:
            raise NoTemplate(
                "a joining operand came back %d bits wide where the "
                "term says %d" % (got, inner_width),
                "a joining operand came back at the wrong width")
        if inner_width == 32 and width == 64:
            lines.append("mov %s,%s"
                         % (register_at(family, 32),
                            register_at(family, 32)))
            return 64
        mnemonic = ZERO_EXTEND_MNEMONIC.get((inner_width, width))
        if mnemonic is None:
            raise NoTemplate(
                "no widening template is written for %d bits to %d "
                "bits: the one opcode table holds no such mnemonic "
                "because no body in the corpus spells one"
                % (inner_width, width),
                "no widening template for %d bits to %d bits"
                % (inner_width, width))
        lines.append("%s %s,%s"
                     % (mnemonic, register_at(family, inner_width),
                        register_at(family, width)))
        return width

    # -- the conditional: a predicate, and a choice ------------------
    #
    # THE SHAPE IS THE CORPUS'S OWN, read off 31,078 ship bodies before
    # any of this was written (`probe80_conditional_shapes.py`): a
    # flag-setting arch opcode, then a flag-reading one, 15,604 of the
    # 18,788 reads exactly one line later, and the single most frequent
    # shape `test <0>,<0>; setne <1>` at 5,691 sightings.  The rule
    # writes `cmp` for every comparison rather than choosing between
    # `cmp` and `test`, because `cmp right,left` is one shape that
    # covers both and `build_flag_only` gives them the same meaning
    # (`test x,x` is `cmp $0,x` on the value the corpus has already
    # computed).
    #
    # A PREDICATE IS NOT COMPUTED INTO A REGISTER.  The walk's rule --
    # one sub-term into one pool register -- does not reach a term
    # whose sort is Bool.  On this machine a comparison leaves its
    # answer in the flags and a suffix reads them, so `emit_condition`
    # returns a SUFFIX, not a width, and leaves nothing behind in a
    # register.  Order is forced: the comparison must be the last
    # flag-setting instruction before its reader, so the arms of a
    # choice are emitted BEFORE the comparison.

    def condition_of(self, node):
        """a z3 predicate -> (condition name, left term, right term).

        `Not(...)` is answered by the complement, which was proved out
        of `condition_table.cond_to_z3` at construction: the simplifier
        prints `a != b` as `Not(a == b)`, so the negation is the
        ordinary case here, not an exception."""
        if z3.is_not(node):
            inner = node.children()[0]
            condition, left, right = self.condition_of(inner)
            other = self.complement.get(condition)
            if other is None:
                raise NoTemplate(
                    "the condition %r has no proved complement, so a "
                    "negated predicate over it has no template"
                    % condition,
                    "a condition with no proved complement")
            return other, left, right
        kind = node.decl().kind()
        condition = PREDICATE_CONDITION.get(kind)
        if condition is None:
            raise NoTemplate(
                "no comparison template is written for the z3 "
                "predicate %r, so a conditional over it has no return "
                "path by the fixed rule" % node.decl().name(),
                "no comparison template for the z3 predicate %r"
                % node.decl().name())
        children = node.children()
        if len(children) != 2:
            raise NoTemplate(
                "a comparison with %d sides has no template"
                % len(children),
                "a comparison with %d sides" % len(children))
        left = children[0]
        right = children[1]
        if not z3.is_bv(left) or not z3.is_bv(right):
            raise NoTemplate(
                "a comparison between values of sort %s and %s is not "
                "a comparison this machine's flags carry"
                % (left.sort(), right.sort()),
                "a comparison between values of sort %s and %s"
                % (left.sort(), right.sort()))
        return condition, left, right

    def emit_condition(self, node, depth, pool, lines,
                       arrival_families):
        """a predicate -> the comparison that leaves it in the flags.
        Returns the CONDITION NAME the reading instruction's suffix
        will carry.  Nothing is left in a register."""
        condition, left, right = self.condition_of(node)
        width = left.size()
        if width != right.size():
            raise NoTemplate(
                "a comparison between a %d-bit side and a %d-bit side "
                "has no template" % (width, right.size()),
                "a comparison between sides of different widths")
        if width not in CONDITION_WIDTHS:
            raise NoTemplate(
                "a comparison at %d bits fits no register width this "
                "rule writes" % width,
                "a comparison at %d bits fits no register width"
                % width)
        left_family = self.take(pool, depth)
        right_family = self.take(pool, depth + 1)
        got = self.emit(left, depth, pool, lines, arrival_families)
        if got != width:
            raise NoTemplate(
                "a comparison side came back %d bits wide where the "
                "term says %d" % (got, width),
                "a comparison side came back at the wrong width")
        got = self.emit(right, depth + 1, pool, lines,
                        arrival_families)
        if got != width:
            raise NoTemplate(
                "a comparison side came back %d bits wide where the "
                "term says %d" % (got, width),
                "a comparison side came back at the wrong width")
        # AT&T `cmp SRC,DST`: `build_flag_only` reads DST as the left
        # of the pair and SRC as the right, so the left term goes in
        # the DESTINATION slot -- which is the second text operand.
        lines.append("cmp %s,%s"
                     % (register_at(right_family, width),
                        register_at(left_family, width)))
        return condition

    def two_literal_arms(self, node):
        """the arms as a pair of literals, or None.

        The corpus's most frequent conditional answers 1 or 0 at eight
        bits, which is exactly what `build_set_condition` writes.  The
        arms come either way round -- the simplifier prints
        `If(x == 0, 0, 1)` for the not-equal case -- and the other way
        round is the complement of the condition, never a second
        template."""
        children = node.children()
        then_arm = children[1]
        else_arm = children[2]
        if not z3.is_bv_value(then_arm):
            return None
        if not z3.is_bv_value(else_arm):
            return None
        return then_arm.as_long(), else_arm.as_long()

    def emit_choice(self, node, depth, pool, lines, arrival_families):
        """`If(predicate, then, else)` -> the corpus's own conditional.

        Two shapes, both read off the corpus: the arms `1` and `0` are
        `set<cc>`; any other pair of arms is `cmov<cc>`."""
        if not z3.is_bv(node):
            raise NoTemplate(
                "a choice whose sort is %s is not a value this rule "
                "puts in a register" % node.sort(),
                "a choice whose sort is %s, not a bit vector"
                % node.sort())
        width = self.width_of(node)
        children = node.children()
        if len(children) != 3:
            raise NoTemplate(
                "a choice with %d parts has no template"
                % len(children),
                "a choice with %d parts" % len(children))
        arms = self.two_literal_arms(node)
        if arms == (1, 0) or arms == (0, 1):
            return self.emit_set_choice(node, arms, depth, pool, lines,
                                        arrival_families, width)
        return self.emit_move_choice(node, depth, pool, lines,
                                     arrival_families, width)

    def emit_set_choice(self, node, arms, depth, pool, lines,
                        arrival_families, width):
        """`build_set_condition` inverted: the condition in the flags,
        then `set<cc>` into the low eight bits of the pool register.

        An answer wider than eight bits is that `set` plus the widening
        the one table already holds -- `movzbl`, which is the widening
        the corpus's own bodies write after a `set` (measured: 519 + 391
        + 284 sightings of a `movzbl` in the two lines after a flag
        read).  No new meaning enters."""
        condition = self.emit_condition(node.children()[0], depth,
                                        pool, lines, arrival_families)
        if arms == (0, 1):
            other = self.complement.get(condition)
            if other is None:
                raise NoTemplate(
                    "the condition %r has no proved complement, so a "
                    "choice with its arms the other way round has no "
                    "template" % condition,
                    "a condition with no proved complement")
            condition = other
        mnemonic = self.set_mnemonic.get(condition)
        if mnemonic is None:
            raise NoTemplate(
                "the one opcode table holds no flag-reading mnemonic "
                "with a builder for the condition %r, because no body "
                "in the corpus spells one" % condition,
                "no flag-reading mnemonic for the condition %r"
                % condition)
        family = self.take(pool, depth)
        lines.append("%s %s" % (mnemonic, register_at(family, 8)))
        if width == 8:
            return 8
        widening = ZERO_EXTEND_MNEMONIC.get((8, 32))
        if widening is None:
            raise NoTemplate(
                "no widening template is written for 8 bits to 32 "
                "bits",
                "no widening template for 8 bits to 32 bits")
        if width == 32:
            lines.append("%s %s,%s"
                         % (widening, register_at(family, 8),
                            register_at(family, 32)))
            return 32
        if width == 64:
            lines.append("%s %s,%s"
                         % (widening, register_at(family, 8),
                            register_at(family, 32)))
            # a 32-bit write is a 64-bit zero-extending write, which is
            # what `build_plain_move` and the machine both do.
            lines.append("mov %s,%s"
                         % (register_at(family, 32),
                            register_at(family, 32)))
            return 64
        raise NoTemplate(
            "no widening template is written for 8 bits to %d bits: "
            "the one opcode table holds no such mnemonic because no "
            "body in the corpus spells one" % width,
            "no widening template for 8 bits to %d bits" % width)

    def emit_move_choice(self, node, depth, pool, lines,
                         arrival_families, width):
        """`build_move_condition` inverted: the else arm into the
        destination register, the then arm into the next, the
        comparison AFTER both of them, then `cmov<cc>`.

        THE ORDER IS FORCED.  A flag reader binds to the most recent
        flag setter, so emitting an arm after the comparison would let
        that arm's own arithmetic overwrite the flags the reader
        needs."""
        if width not in MOVE_CONDITION_WIDTHS:
            raise NoTemplate(
                "a choice at %d bits has no conditional-move "
                "instruction on this machine, which has `cmov` at 16, "
                "32 and 64 bits only" % width,
                "a choice at %d bits has no conditional move" % width)
        children = node.children()
        then_arm = children[1]
        else_arm = children[2]
        destination = self.take(pool, depth)
        source = self.take(pool, depth + 1)
        got = self.emit(else_arm, depth, pool, lines, arrival_families)
        if got != width:
            raise NoTemplate(
                "a choice arm came back %d bits wide where the choice "
                "is %d" % (got, width),
                "a choice arm came back at the wrong width")
        got = self.emit(then_arm, depth + 1, pool, lines,
                        arrival_families)
        if got != width:
            raise NoTemplate(
                "a choice arm came back %d bits wide where the choice "
                "is %d" % (got, width),
                "a choice arm came back at the wrong width")
        condition = self.emit_condition(children[0], depth + 2, pool,
                                        lines, arrival_families)
        mnemonic = self.move_mnemonic.get(condition)
        if mnemonic is None:
            raise NoTemplate(
                "the one opcode table holds no conditional-move "
                "mnemonic with a builder for the condition %r, "
                "because no body in the corpus spells one" % condition,
                "no conditional-move mnemonic for the condition %r"
                % condition)
        lines.append("%s %s,%s"
                     % (mnemonic, register_at(source, width),
                        register_at(destination, width)))
        return width

    # -- wrap_rendered -----------------------------------------------

    def wrap_rendered(self, body_lines, unit):
        """the rendered body -> a wrapped text, through the SAME
        `CanonicalForm.wrap` layer 3 goes through, over the unit's own
        arrival families and its own answer home.  So the rendered
        text is a second canonical rendering of the unit, in one form
        with the first, and the two are comparable character for
        character."""
        form = CF.CanonicalForm()
        text = "; ".join(body_lines)
        return form.wrap(text,
                         list(unit.get("arrival_families") or []),
                         unit.get("result_family"),
                         unit.get("result_width"))

    def render_and_wrap(self, term, unit):
        """the two steps together, with every refusal named."""
        out = Rendering(unit.get("unit"))
        if term is None:
            out.refused = ("this unit has no proved term, so there is "
                           "nothing to render back")
            out.refusal_cause = "no term"
            return out
        # WHAT IS RENDERED IS THE LAYER-5 TERM.  `normalize`'s rule is
        # three steps: simplify ONCE, rename the free symbols
        # positionally, print on one line.  Step one is applied here,
        # because the thing owed a return path is the SIMPLIFIED
        # expression -- AgentMemory, "a valid simplified expression is
        # rendered back into canonical runnable instructions".  Step
        # two is NOT applied: the positional names `v0`, `v1` are a
        # printing for comparison, while a rendering has to keep the
        # symbols the gate binds the input rows to.  Measured on
        # E00029: without step one, 86 of the 158 members carried a
        # multiply by one that the compiler's own body never wrote,
        # and the entry rendered to 8 texts instead of 5.
        term = z3.simplify(term)
        try:
            body = self.render(
                term,
                list(unit.get("arrival_families") or []),
                unit.get("result_family"),
                unit.get("result_width"))
        except NoTemplate as problem:
            out.refused = "%s" % problem
            out.refusal_cause = problem.cause
            return out
        except Exception as problem:
            out.refused = "rendering raised %s: %s" % (
                type(problem).__name__, problem)
            out.refusal_cause = "rendering raised"
            return out
        out.body = body
        try:
            out.fields = self.wrap_rendered(body, unit)
        except L.Refusal as problem:
            out.refused = "the form refused the rendered body: %s" % (
                problem,)
            out.refusal_cause = "the form refused"
            return out
        except Exception as problem:
            out.refused = "wrapping raised %s: %s" % (
                type(problem).__name__, problem)
            out.refusal_cause = "wrapping raised"
            return out
        out.wrapped_text = out.fields["wrapped_text"]
        return out

    # -- verify ------------------------------------------------------

    def merged_for_the_gate(self, unit, fields):
        """the record the gate reads: the RENDERED plumbing on the
        `ours` side, the unit's OWN ship body on the `theirs` side.

        `Gate.prove_wrapped` reads the prelude, the epilogue and the
        arrival families to bind input row i to arrival family i's own
        symbol, and reads `body_verbatim`, `result_family` and
        `arrival_contract_bindings` to simulate the unit's own ship
        code.  So the first three come from the rendering and the last
        three stay the unit's -- which is what "proved against the
        unit's OWN ship code" means here."""
        merged = dict(unit)
        merged["prelude"] = fields["prelude"]
        merged["prelude_resolved"] = fields["prelude_resolved"]
        merged["epilogue"] = fields["epilogue"]
        merged["epilogue_resolved"] = fields["epilogue_resolved"]
        merged["out_row"] = fields["out_row"]
        merged["wrapped_text"] = fields["wrapped_text"]
        return merged

    def verify(self, gate, unit, fields):
        """the rendered wrapped text, gated exactly as a wrapped text
        is.  ONLY `PROVED_ON_SHIP` counts: the structural route's own
        first check is that the compiler's body appears in the wrapped
        text character for character, which a rendered body is not, so
        a structural pass here would be accepting a rendering because
        it is a rendering."""
        merged = self.merged_for_the_gate(unit, fields)
        return gate.prove_wrapped(fields["wrapped_text"], merged)
