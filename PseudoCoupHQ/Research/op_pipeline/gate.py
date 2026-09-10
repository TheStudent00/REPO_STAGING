#!/usr/bin/env python3
"""gate.py -- THE GATE.  The proof obligations and the object that
discharges them.

The code of node `hq.research.compiler_graph.gate`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_5_gate/CORE_0_3_5_5_gate.md`).
Its class is `Gate`; its methods are the CORE's `methods:`
(`prove_wrapped`, `prove_term_against_ship`, `prove_term_against_text`,
`structural_checks`, `zero_regression`); its sub-node `verdict` is the
class `Verdict`, whose attributes are that node's own five sub-nodes
(`outcome`, `reason`, `counterexample`, `route`, `solver_timeout_ms`).

NOTHING IN THIS RESEARCH IS COUNTED UNLESS IT PASSED A GATE.  A wrapped
text is counted when it provably computes what the unit's own ship code
computes, for every value of every input row; a term is counted when it
provably equals the reference's answer for that same body, and
independently when a walk of the body in text order rebuilds it.

THE REFERENCE IS `reference.py`.  This file carries no simulator of its
own (CORE settled rule, 2026-09-03).  `canon9/10/12_behaviour_check.py`
and the four simulators they carried are superseded records.

WHAT WAS COPIED UNCHANGED FROM SUPERSEDED RECORDS, said out loud rather
than hidden.  `canon*`, `gate48.py`, `textwalk48.py` and `layer4*.py`
are superseded records and are NOT edited by this file:

  * `structural_checks`' six checks are `canon37_gate.structural_route`
    (C1-C5) and `canon38_gate.check_six` (C6) rewritten here as the
    CORE's six named methods `check_one` .. `check_six`.  The logic is
    the same logic; the shape is the CORE's.
  * `prove_term_against_text`'s walk is `textwalk48.walk`, copied
    unchanged in substance.  It walks the body in TEXT ORDER using the
    SAME meanings the ledger transcription used (`layer4`'s producer
    table, reached through `layer4c`), which is what makes route two
    evidence about the LEDGER'S WIRING rather than about the meanings:
    if route two used `reference.py`'s table it would be route one
    again, and the two routes would share a code path.
  * `prove_term_against_ship` replaces `gate48.gate`.  Its reference
    side is `reference.Reference`, not `canon10_behaviour_check.Sim10`,
    which is the whole point of this lap: one remainder (`SRem`), a
    modelled machine stack and x87 stack, and real IEEE floats on both
    sides.

THE FIVE OUTCOMES, and which one a term route may reach.
PROVED_ON_SHIP is "the solver showed equality against the unit's own
ship code".  Both term routes compare against the unit's OWN SHIP
BODY -- route one as the reference walks it, route two as the ledger's
meanings walk it in text order -- so a proved term carries
PROVED_ON_SHIP with `route` saying which obligation produced it.  No
sixth outcome is invented; the CORE names five.

A SOLVER TIMEOUT IS UNDECIDED, never DISPROVED, and the timeout in
force is recorded on the verdict (3,000 ms today).

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

No operator token appears in this file.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                      # noqa: E402
import ledger47 as L47                                            # noqa: E402
import ledger48 as L48                                            # noqa: E402
import region36 as R36                                            # noqa: E402
import layer4                                                     # noqa: E402
import reference as REF                                           # noqa: E402
import z3                                                         # noqa: E402


SOLVER_MILLISECONDS = 3000

PROVED_ON_SHIP = "PROVED_ON_SHIP"
PROVED_BY_CONSTRUCTION = "PROVED_BY_CONSTRUCTION"
DISPROVED = "DISPROVED"
UNDECIDED = "UNDECIDED"
REFUSED = "REFUSED"

ROUTE_WRAPPED = "the wrapped text against the unit's own ship body"
ROUTE_TERM_SHIP = "the term against the unit's own ship body"
ROUTE_TERM_TEXT = "the term against the body walked in text order"


class Verdict(object):
    """what a gate returns about one unit -- the sub-node `verdict`.

    Its five attributes are that node's five sub-nodes.  `outcome` is
    one of the five the CORE names.  `reason` is plain words: which
    obligation was discharged, or what stopped it.  `counterexample`
    is the solver's own model, quoted rather than summarized, and is
    set only when the outcome is DISPROVED.  `route` says which
    obligation produced the verdict.  `solver_timeout_ms` is the limit
    that was in force, recorded so an UNDECIDED can be re-read later.
    """

    def __init__(self, outcome, reason, route,
                 counterexample=None,
                 solver_timeout_ms=SOLVER_MILLISECONDS):
        self.outcome = outcome
        self.reason = reason
        self.counterexample = counterexample
        self.route = route
        self.solver_timeout_ms = solver_timeout_ms

    def proved(self):
        if self.outcome == PROVED_ON_SHIP:
            return True
        return self.outcome == PROVED_BY_CONSTRUCTION

    def as_dict(self):
        return {
            "outcome": self.outcome,
            "reason": self.reason,
            "counterexample": self.counterexample,
            "route": self.route,
            "solver_timeout_ms": self.solver_timeout_ms,
        }

    def __repr__(self):
        return "Verdict(%s on %s)" % (self.outcome, self.route)


class NotWalkable(Exception):
    """this body cannot be walked in text order by this file."""


def is_flag_reader(mnemonic):
    """copied unchanged from `textwalk48.is_flag_reader`."""
    for prefix in ("set", "cmov", "j"):
        if not mnemonic.startswith(prefix):
            continue
        if len(mnemonic) <= len(prefix):
            continue
        suffix = mnemonic[len(prefix):]
        if suffix in layer4.CT.SUFFIX_TO_COND:
            return True
        if suffix in ("o", "no"):
            return True
    return False


def transfers_inside_the_unit(line, defined):
    """does this line transfer to a label the SAME body defines?"""
    parts = line.split(" ", 1)
    if len(parts) != 2:
        return False
    mnemonic = parts[0]
    if not mnemonic.startswith("j"):
        return False
    if mnemonic != "jmp" and not is_flag_reader(mnemonic):
        return False
    return parts[1].strip() in defined


def label_definitions(lines):
    out = []
    for line in lines:
        if line.endswith(":"):
            out.append(line[:-1])
    return out


class Gate(object):
    """the object that discharges the proof obligations."""

    def __init__(self, reference=None,
                 solver_timeout_ms=SOLVER_MILLISECONDS):
        if reference is None:
            reference = REF.Reference()
        self.reference = reference
        self.solver_timeout_ms = solver_timeout_ms

    # -- the solver, in one place -------------------------------------

    def decide(self, ours, theirs, route, proved_reason):
        """the one place a solver is asked anything.  Two terms in,
        one Verdict out.  Widths are cut to the narrower of the two,
        which is what both superseded routes did."""
        if ours.size() != theirs.size():
            narrow = min(ours.size(), theirs.size())
            ours = z3.Extract(narrow - 1, 0, ours)
            theirs = z3.Extract(narrow - 1, 0, theirs)
        solver = z3.Solver()
        solver.set("timeout", self.solver_timeout_ms)
        try:
            solver.add(ours != theirs)
        except Exception as problem:
            return Verdict(
                UNDECIDED,
                "the two terms are not comparable: %s" % problem,
                route, None, self.solver_timeout_ms)
        try:
            answer = solver.check()
        except Exception as problem:
            return Verdict(UNDECIDED, "z3 raised %s" % problem,
                           route, None, self.solver_timeout_ms)
        if answer == z3.unsat:
            return Verdict(PROVED_ON_SHIP, proved_reason, route,
                           None, self.solver_timeout_ms)
        if answer == z3.sat:
            return Verdict(
                DISPROVED,
                "z3 found a starting state under which the two sides "
                "differ", route, "%s" % solver.model(),
                self.solver_timeout_ms)
        return Verdict(
            UNDECIDED,
            "the solver did not answer inside its %d ms limit, so the "
            "verdict is undecided and never disproved"
            % self.solver_timeout_ms,
            route, None, self.solver_timeout_ms)

    def comparable(self, ours, theirs):
        """two BIT VECTORS are comparable whatever their widths --
        `decide` cuts both to the narrower, which is what both
        superseded routes did and what the answer home's own width
        means.  A float sort against a bit vector is NOT comparable,
        and saying so is the honest verdict rather than a coerced
        one."""
        left = z3.is_bv(ours)
        right = z3.is_bv(theirs)
        if left and right:
            return True
        return ours.sort() == theirs.sort()

    # -- route: the term against the unit's own ship body -------------

    def prove_term_against_ship(self, term, unit):
        """(term, unit) -> Verdict.  Route one: the ledger-transcribed
        OUT-0 term against `Reference.answer_of` for the unit's own
        ship body."""
        route = ROUTE_TERM_SHIP
        if term is None:
            return Verdict(UNDECIDED,
                           "the ledger built no term for OUT-0",
                           route, None, self.solver_timeout_ms)
        try:
            theirs, _width = self.reference.answer_for_unit(unit)
        except REF.NotModeled as problem:
            return Verdict(UNDECIDED, self.refusal_wording(problem),
                           route, None, self.solver_timeout_ms)
        except Exception as problem:
            return Verdict(
                UNDECIDED,
                "the reference raised %s: %s"
                % (type(problem).__name__, problem),
                route, None, self.solver_timeout_ms)
        if not self.comparable(term, theirs):
            return Verdict(
                UNDECIDED,
                "the reference's answer and the ledger's term are of "
                "different z3 sorts (%s against %s), so the solver has "
                "nothing to compare" % (theirs.sort(), term.sort()),
                route, None, self.solver_timeout_ms)
        return self.decide(
            term, theirs, route,
            "z3 proved the ledger-transcribed OUT-0 term equal to the "
            "value the unit's own ship body leaves in its own answer "
            "home, for every value of every register either side reads "
            "before writing")

    def refusal_wording(self, problem):
        """the reference's own refusal, with the `call` case said the
        way the owner's round-12 ruling says it.  A unit whose answer comes
        from a transfer into the compiler's OWN runtime is REFUSED
        because that callee is not attached yet (task 59, node
        0_3_5_1_8 runtime_callee) -- it is never "out of scope"."""
        text = "%s" % problem
        if "'call'" in text:
            return ("refused: runtime callee not yet attached (task "
                    "59, node 0_3_5_1_8) -- the reference's own words: "
                    "%s" % text)
        return "the reference: %s" % text

    # -- route: the term against the body walked in text order --------

    def walk_in_text_order(self, unit):
        """the value the unit's own body leaves in its own answer home,
        walked in TEXT ORDER with the same meanings the ledger
        transcription used.  Copied unchanged in substance from
        `textwalk48.walk`; it is the ledger's own producer table
        driven by the text's order instead of by the ledger's wiring,
        so agreement is evidence about the WIRING."""
        registers = {}
        seeds = {}
        memory = {}
        rip_index = [0]
        flags = {"flags": None}
        last_setter = [None]
        for binding in unit.get("arrival_contract_bindings", []):
            register = binding.get("bound_to_the_same_symbol_as", "")
            family = canon.FAMILY_OF.get(register[1:])
            if family is None:
                continue
            registers[family] = layer4.seed_of(seeds, family, "a")
        defined = set(label_definitions(
            [R36.strip_annotation(raw)
             for raw in unit["body_verbatim"]]))
        for raw in unit["body_verbatim"]:
            line = R36.strip_annotation(raw)
            if line.endswith(":"):
                continue
            if transfers_inside_the_unit(line, defined):
                # A SILENT GAP MADE FALSE PROOFS, AND IT IS NAMED HERE.
                # This walk goes down the page.  When a transfer's
                # target is a label THIS BODY DEFINES, the page order
                # is not the run order: the body holds two alternative
                # computations and the walk was quietly reading them as
                # one after the other.  Measured on 2026-09-03 (task
                # 64) over canon39's 30,432: 230 units this route
                # called PROVED while route one -- which now follows
                # the branches -- DISPROVED them with a counterexample
                # against the unit's own ship body.  `c/op_117` is the
                # worked case: `js L0` chooses between converting the
                # value directly and halving it first, and this walk
                # was adding BOTH answers together.  A transfer whose
                # target is NOT defined here leaves the unit, and the
                # fall-through is then the only reachable path, so it
                # is walked as before.
                raise NotWalkable(
                    "this body transfers to %r, a label it defines "
                    "itself, so the page order is not the run order "
                    "and a text-order walk has no one answer to reach"
                    % line)
            if line == "" or line == "ret":
                continue
            mnemonic = L47.mnemonic_of(line)
            if mnemonic is None:
                continue
            if mnemonic.startswith("j") and not is_flag_reader(mnemonic):
                continue
            if mnemonic in ("call", "ud2", "nop", "hlt") or \
                    mnemonic.startswith("j"):
                if mnemonic == "call":
                    raise NotWalkable(
                        "refused: runtime callee not yet attached "
                        "(task 59, node 0_3_5_1_8) -- the body "
                        "transfers out of the unit (%r), so a "
                        "text-order walk has no answer to reach"
                        % line)
                if mnemonic == "ud2":
                    raise NotWalkable(
                        "the body transfers out of the unit (%r), so "
                        "a text-order walk has no answer to reach"
                        % line)
                continue
            operands = L47.operands_of(line)
            slots = []
            for _position, operand in enumerate(operands):
                value = L47.immediate_value(operand)
                if value is not None:
                    slots.append(layer4.Slot(operand, None,
                                             immediate=value))
                    continue
                if operand.startswith("%"):
                    family = layer4.family_of(operand)
                    slot = layer4.Slot(operand, None)
                    slot.family = family
                    if family is not None:
                        if family not in registers:
                            registers[family] = layer4.seed_of(
                                seeds, family, "a")
                        slot.term = registers[family]
                    slots.append(slot)
                    continue
                inner = []
                if "(%rip)" in operand:
                    inner.append(("rip", ("rip", rip_index[0])))
                    rip_index[0] = rip_index[0] + 1
                for token in re.findall(r"%[a-z0-9]+", operand):
                    family = canon.FAMILY_OF.get(token[1:])
                    if family is None:
                        continue
                    if family not in registers:
                        registers[family] = layer4.seed_of(
                            seeds, family, "a")
                    inner.append((token, registers[family]))
                for hit in R36.RSP_DISP.finditer(operand):
                    displacement = int(hit.group(1), 16)
                    key = "own_%x" % displacement
                    if key not in memory:
                        memory[key] = z3.BitVec("seed_rsp", 64) - \
                            z3.BitVecVal(displacement, 64)
                    inner.append(("own", memory[key]))
                slot = layer4.Slot(operand, None, memory=inner)
                slot.term = layer4.memory_load_term(slot, seeds, "a")
                slots.append(slot)
            for slot in slots:
                if slot.immediate is not None:
                    slot.term = z3.BitVecVal(
                        slot.immediate & ((1 << 64) - 1), 64)
            row = {"row": "walk", "size": 8, "block": "TEMP"}
            producer = mnemonic
            if is_flag_reader(mnemonic):
                producer = [last_setter[0], mnemonic]
            try:
                value = layer4.build_producer_term(producer, line,
                                                   slots, row, flags)
            except layer4.NoTerm as problem:
                raise NotWalkable("%s" % problem.why)
            if L47.sets_the_flags(mnemonic):
                last_setter[0] = mnemonic
                try:
                    found = layer4.flags_of(mnemonic, slots, line,
                                            value)
                except Exception:
                    found = None
                if found is not None:
                    flags["flags"] = found
            if not operands:
                continue
            destination = operands[-1]
            family = layer4.family_of(destination)
            if family is None:
                continue
            if family in canon.NEVER_RENAME:
                continue
            if mnemonic in layer4.FLAG_ONLY:
                continue
            registers[family] = value
        home = unit["result_family"]
        if home not in registers:
            raise NotWalkable(
                "the answer home %r is never written by this body, so "
                "the walk has no answer" % home)
        return layer4.cut(registers[home], unit["result_width"])

    def prove_term_against_text(self, term, unit):
        """(term, unit) -> Verdict.  Route two: the term against the
        body walked in text order with the same meanings table.
        Evidence about the LEDGER'S WIRING, not about the meanings."""
        route = ROUTE_TERM_TEXT
        if term is None:
            return Verdict(UNDECIDED,
                           "the ledger built no term for OUT-0",
                           route, None, self.solver_timeout_ms)
        try:
            theirs = self.walk_in_text_order(unit)
        except NotWalkable as problem:
            return Verdict(UNDECIDED,
                           "the text-order walk: %s" % problem,
                           route, None, self.solver_timeout_ms)
        except Exception as problem:
            return Verdict(
                UNDECIDED,
                "the text-order walk raised %s: %s"
                % (type(problem).__name__, problem),
                route, None, self.solver_timeout_ms)
        if not self.comparable(term, theirs):
            return Verdict(
                UNDECIDED,
                "the text-order walk's answer and the ledger's term "
                "are of different z3 sorts (%s against %s)"
                % (theirs.sort(), term.sort()),
                route, None, self.solver_timeout_ms)
        return self.decide(
            term, theirs, route,
            "z3 proved the ledger-transcribed OUT-0 term equal to the "
            "same body walked in text order, for every value of every "
            "register either walk reads before writing")

    # -- route: the wrapped text against the unit's own ship body -----

    def wrapped_answer(self, unit, shared_seed):
        """OUT-0 of the wrapped text, as the one reference walks it.

        THE BINDING, stated once.  The wrapped text reaches an input
        row in two steps: read the block's base out of the ledger at an
        absolute rip-relative address, then read the row inside that
        block.  The second read's own operand text is the cell the
        reference reads, so input row i is bound by writing the arrival
        family i's own symbol into that cell BEFORE the walk -- which
        is exactly `canon37_gate.bind_arrival`'s obligation, "input row
        i is bound to the same symbol as the argument the reference
        text reads in arrival register i", carried here without a
        second simulator."""
        state = REF.MachineState(shared_seed)
        prelude = list(unit.get("prelude") or [])
        resolved = list(unit.get("prelude_resolved") or [])
        families = list(unit.get("arrival_families") or [])
        if len(prelude) != 2 * len(resolved):
            raise REF.NotModeled(
                "this unit's prelude is not one two-step load per "
                "input row (%d lines for %d loads), so the input rows "
                "cannot be bound" % (len(prelude), len(resolved)))
        index = 0
        for position in range(len(resolved)):
            second = prelude[2 * position + 1]
            operands = REF.split_operands(
                second.split(" ", 1)[1] if " " in second else "")
            if len(operands) != 2:
                raise REF.NotModeled(
                    "the second step of a two-step load has %d "
                    "operands: %r" % (len(operands), second))
            cell_text = operands[0]
            if index >= len(families):
                raise REF.NotModeled(
                    "the prelude loads more rows than the arrival "
                    "contract names families")
            family = families[index]
            index = index + 1
            state.set_memory_cell(cell_text, state.seed(family))
        epilogue = list(unit.get("epilogue") or [])
        if len(epilogue) != 2:
            raise REF.NotModeled(
                "this unit's epilogue is not the two-step store this "
                "form emits: %r" % epilogue)
        store = epilogue[-1]
        store_operands = REF.split_operands(
            store.split(" ", 1)[1] if " " in store else "")
        if len(store_operands) != 2:
            raise REF.NotModeled(
                "the epilogue's store has %d operands: %r"
                % (len(store_operands), store))
        out_cell = store_operands[1]
        for line in self.reference.body_lines(unit.get("wrapped_text")):
            self.reference.step(state, line)
        if out_cell not in state.memory:
            raise REF.NotModeled(
                "the wrapped text never wrote the OUT row's own cell "
                "%r" % out_cell)
        return REF.cut(state.memory[out_cell],
                       unit.get("result_width"))

    def prove_wrapped(self, wrapped_text, unit):
        """(wrapped_text, unit) -> Verdict.  OUT-0 of the wrapped text
        equals the reference's answer for the unit's own ship body, for
        every value of every input row, inputs bound row-i <->
        arrival-register-i.

        FALLS TO `structural_checks` ONLY where the reference has no
        model for a mnemonic the body spells -- never as a cheaper
        first choice (CORE settled rule, log_146 section 5.3)."""
        route = ROUTE_WRAPPED
        shared_seed = {}
        wanted = dict(unit)
        wanted["wrapped_text"] = wrapped_text
        try:
            ours = self.wrapped_answer(wanted, shared_seed)
        except REF.NotModeled as problem:
            return self.structural_fallback(wanted, problem, route)
        except Exception as problem:
            return self.structural_fallback(
                wanted, "%s: %s" % (type(problem).__name__, problem),
                route)
        try:
            state = self.reference.simulate(
                unit.get("body_verbatim"),
                unit.get("arrival_contract_bindings"), shared_seed)
            theirs = self.reference.answer_of(
                state, (unit.get("result_family"),
                        unit.get("result_width")))
        except REF.NotModeled as problem:
            return self.structural_fallback(wanted, problem, route)
        except Exception as problem:
            return self.structural_fallback(
                wanted, "%s: %s" % (type(problem).__name__, problem),
                route)
        if ours.sort() != theirs.sort():
            return self.structural_fallback(
                wanted,
                "the two answers are of different z3 sorts (%s "
                "against %s)" % (ours.sort(), theirs.sort()), route)
        return self.decide(
            ours, theirs, route,
            "z3 proved the wrapped text's %s equal to the value the "
            "unit's own ship body leaves in its own answer home, for "
            "every value of every input row, with each input row bound "
            "to the same symbol as the argument the reference reads in "
            "its arrival register" % unit.get("out_row"))

    def structural_fallback(self, unit, problem, route):
        """the solver could not answer for want of a model, so the six
        mechanical checks are asked instead."""
        passed, note = self.structural_checks(
            unit.get("wrapped_text"), unit)
        if passed:
            return Verdict(
                PROVED_BY_CONSTRUCTION,
                "the reference has no model for something this body "
                "spells (%s), and the form applies NO transformation "
                "to the body, so the six mechanical checks carry it: "
                "%s" % (problem, " | ".join(note)),
                route, None, self.solver_timeout_ms)
        return Verdict(
            UNDECIDED,
            "the reference has no model for something this body spells "
            "(%s), and the structural route does not carry it: %s"
            % (problem, note), route, None, self.solver_timeout_ms)

    # -- the sub-node: the six mechanical checks ----------------------

    def structural_checks(self, wrapped_text, unit):
        """(wrapped_text, unit) -> (all six passed, notes or the line
        that failed).

        Because the canonical form applies NO transformation to the
        body, the obligation reduces to two claims that can be checked
        by looking: the compiler's body is present and unchanged, and
        the added plumbing cannot disturb it.  A unit passing all six
        is PROVED_BY_CONSTRUCTION; a unit failing any is not counted,
        whatever its text looks like."""
        fields = dict(unit)
        fields["wrapped_text"] = wrapped_text
        notes = []
        for check in (self.check_one, self.check_two, self.check_three,
                      self.check_four, self.check_five, self.check_six):
            try:
                passed, note = check(fields)
            except Exception as problem:
                return False, ("%s raised %s: %s"
                               % (check.__name__,
                                  type(problem).__name__, problem))
            if not passed:
                return False, note
            if isinstance(note, list):
                notes.extend(note)
            else:
                notes.append(note)
        return True, notes

    def check_one(self, fields):
        """C1 -- the body appears in the wrapped text
        character-for-character and in its own order: no register
        renamed, no immediate moved, no stack address rewritten."""
        body = fields["body_verbatim"]
        placed = L47.split_lines(fields["wrapped_text"])
        prelude = fields["prelude"]
        epilogue = fields["epilogue"]
        body_seen = []
        for line in placed:
            if line in prelude:
                continue
            if line in epilogue:
                continue
            body_seen.append(line)
        if body_seen != body:
            extra = []
            for line in body_seen:
                if line not in body:
                    extra.append(line)
            return False, ("C1 fails: the wrapped text does not carry "
                           "the body character-for-character; "
                           "unaccounted lines %r" % extra[:4])
        return True, ("C1: the body appears in the wrapped text "
                      "character-for-character and in its own order -- "
                      "no register was renamed, no immediate was "
                      "moved, no stack address was rewritten")

    def check_two(self, fields):
        """C2 -- the prelude writes only the registers the arrival
        contract names, one two-step load per input row, plus at most
        one general scratch that is not an arrival family."""
        written = []
        for line in fields["prelude"]:
            operands = L47.operands_of(line)
            if not operands:
                continue
            family = L47.family_of_operand(operands[-1])
            if family is None:
                continue
            written.append(family)
        wanted = set(fields["arrival_families"])
        scratch = fields.get("prelude_scratch")
        if scratch is not None:
            wanted.add(scratch)
        for family in written:
            if family not in wanted:
                return False, ("C2 fails: the prelude writes %s, which "
                               "is neither an arrival family nor the "
                               "one scratch the form allows" % family)
        note = ("C2: the prelude writes only the registers the arrival "
                "contract names, one two-step load per input row")
        if scratch is not None and scratch not in \
                fields["arrival_families"]:
            note = note + (" (its one scratch %%%s is not an arrival "
                           "family, so the body never reads it before "
                           "writing it)" % scratch)
        return True, note

    def check_three(self, fields):
        """C3 -- every `ret` is immediately preceded by the
        epilogue."""
        placed = L47.split_lines(fields["wrapped_text"])
        epilogue = fields["epilogue"]
        for index, line in enumerate(placed):
            if line != "ret":
                continue
            if index < len(epilogue):
                return False, ("C3 fails: a `ret` has no epilogue "
                               "before it")
            window = placed[index - len(epilogue):index]
            if window != epilogue:
                return False, ("C3 fails: a `ret` at line %d is not "
                               "immediately preceded by the epilogue"
                               % index)
        return True, ("C3: every one of the %s returns is immediately "
                      "preceded by the epilogue, which stores the "
                      "compiler's own result register into %s"
                      % (fields.get("returns"), fields.get("out_row")))

    def check_four(self, fields):
        """C4 -- no body line names the ledger symbol or any ledger
        row."""
        for line in fields["body_verbatim"]:
            if L47.LEDGER_SYMBOL in line:
                return False, ("C4 fails: a body line names the ledger "
                               "symbol: %r" % line)
            for operand in L47.operands_of(line):
                if L47.is_row_text(operand) or L48.is_row_text(operand):
                    return False, ("C4 fails: a body line names a "
                                   "ledger row: %r" % line)
        return True, ("C4: no body line names the ledger symbol or any "
                      "ledger row, so the body and the plumbing touch "
                      "disjoint text")

    def check_five(self, fields):
        """C5 -- the epilogue's pointer register is not the result
        register."""
        pointer = fields.get("epilogue_scratch")
        if pointer == fields["result_family"]:
            return False, ("C5 fails: the epilogue's pointer register "
                           "is the result register")
        return True, ("C5: the epilogue's pointer register %%%s is not "
                      "the result register %%%s, so loading the block "
                      "base cannot destroy the answer"
                      % (pointer, fields["result_family"]))

    def check_six(self, fields):
        """C6 -- the label rewrite touched only transfer targets: an
        intra-unit target became `L0..` and an out-of-unit transfer
        lost its address and comment; nothing else on any line
        changed.

        C6 exists because the positional label rewrite makes C1's
        original character-for-character wording false as written; it
        is a NEW check, not a reuse of canon37's claim."""
        was = fields.get("body_as_read")
        now = fields.get("body_verbatim")
        record = fields.get("branch_labels") or {}
        if was is None:
            return False, "C6 fails: the record carries no body as read"
        defined = label_definitions(now)
        if len(defined) != len(set(defined)):
            return False, ("C6 fails: a label is defined more than "
                           "once: %r" % defined)
        stored_without_labels = []
        for line in now:
            if line.endswith(":"):
                continue
            stored_without_labels.append(line)
        if len(stored_without_labels) != len(was):
            return False, ("C6 fails: the stored body has %d "
                           "instructions and the body as read has %d"
                           % (len(stored_without_labels), len(was)))
        rewritten_at = {}
        for entry in record.get("rewrites") or []:
            rewritten_at[entry["line_index"]] = entry
        by_target = {}
        for index, old in enumerate(was):
            new = stored_without_labels[index]
            if new == old:
                if index in rewritten_at:
                    return False, ("C6 fails: line %d is recorded as "
                                   "rewritten and is unchanged" % index)
                continue
            if index not in rewritten_at:
                return False, ("C6 fails: line %d changed and no "
                               "rewrite is recorded for it: %r -> %r"
                               % (index, old, new))
            old_text, old_annotation = L48.split_off_annotation(old)
            new_text, new_annotation = L48.split_off_annotation(new)
            if old_annotation != new_annotation:
                return False, ("C6 fails: line %d's trailing "
                               "annotation changed" % index)
            old_parts = old_text.split(" ", 1)
            new_parts = new_text.split(" ", 1)
            if old_parts[0] != new_parts[0]:
                return False, ("C6 fails: line %d's mnemonic changed, "
                               "%r to %r" % (index, old_parts[0],
                                             new_parts[0]))
            if not L48.is_transfer(old_parts[0]):
                return False, ("C6 fails: line %d changed and is not a "
                               "transfer: %r" % (index, old))
            target_was = old_parts[1].strip()
            target_now = new_parts[1].strip()
            if target_was in by_target:
                if by_target[target_was] != target_now:
                    return False, ("C6 fails: the same target %r was "
                                   "rewritten two ways" % target_was)
            by_target[target_was] = target_now
        used = set()
        for line in stored_without_labels:
            text, _annotation = L48.split_off_annotation(line)
            parts = text.split(" ", 1)
            if len(parts) != 2:
                continue
            if not L48.is_transfer(parts[0]):
                continue
            target = parts[1].strip()
            if not target.startswith("L"):
                continue
            if target[1:].isdigit():
                used.add(target)
        for name in sorted(used):
            if name not in defined:
                return False, ("C6 fails: the stored body branches to "
                               "%s and defines no such label" % name)
        return True, ("C6: the only text this form changed inside the "
                      "body is the TARGET operand of %d transfer(s); "
                      "every mnemonic, every other operand and every "
                      "trailing annotation is the body's own, the "
                      "rewrite is a function of the target, and every "
                      "positional label the body branches to is "
                      "defined exactly once in it" % len(rewritten_at))

    # -- the sub-node: zero regression --------------------------------

    def zero_regression(self, verdicts_before, verdicts_after,
                        cause_of=None):
        """the before-and-after check over a whole population.

        `verdicts_before` and `verdicts_after` are mappings from unit
        name to a STATE STRING -- `proved`, `withdrawn`, `undecided`,
        `no term` -- joined on the unit name.  `cause_of` is a callable
        (unit name, before, after) -> cause, COMPUTED over that unit's
        own artifact; a lost proof with no computed cause is reported
        as such rather than smoothed.

        THE RULE, as numbered statements: (1) no unit proved in the
        previous round loses PROVED without a named cause; (2) the
        cause is CHECKED over the unit's own artifact, mechanically;
        (3) a change of text with the verdict unchanged is not a
        regression; (4) the report is by cause with its sightings,
        never a list of every sighting."""
        comparison = self.compare(verdicts_before, verdicts_after)
        losses = self.explain_losses(comparison, cause_of)
        return self.report(comparison, losses)

    def compare(self, verdicts_before, verdicts_after):
        """(verdicts_before, verdicts_after) -> per unit, kept / lost /
        gained, joined on unit name."""
        kept = []
        lost = []
        gained = []
        moved = []
        missing = []
        for name in sorted(verdicts_before):
            before = verdicts_before[name]
            if name not in verdicts_after:
                missing.append(name)
                continue
            after = verdicts_after[name]
            if before == "proved" and after == "proved":
                kept.append(name)
                continue
            if before == "proved":
                lost.append(name)
                continue
            if after == "proved":
                gained.append(name)
                continue
            if before != after:
                moved.append(name)
        for name in sorted(verdicts_after):
            if name not in verdicts_before:
                gained.append(name)
        return {
            "kept": kept,
            "lost": lost,
            "gained": gained,
            "moved": moved,
            "missing_from_the_new_run": missing,
        }

    def explain_losses(self, comparison, cause_of):
        """each lost proof -> a cause, checked over that unit's own
        artifact, not asserted."""
        causes = {}
        for name in comparison["lost"]:
            cause = None
            if cause_of is not None:
                cause = cause_of(name)
            if cause is None:
                cause = ("NO CAUSE WAS COMPUTED FOR THIS LOSS -- it is "
                         "reported as an unexplained regression")
            causes.setdefault(cause, []).append(name)
        return causes

    def report(self, comparison, causes):
        """the counts plus every cause with the units under it."""
        return {
            "kept": len(comparison["kept"]),
            "lost": len(comparison["lost"]),
            "gained": len(comparison["gained"]),
            "moved_without_losing_a_proof": len(comparison["moved"]),
            "missing_from_the_new_run":
                len(comparison["missing_from_the_new_run"]),
            "causes": [
                {
                    "cause": cause,
                    "units": len(names),
                    "sightings": sorted(names)[:3],
                }
                for cause, names in sorted(
                    causes.items(), key=lambda pair: -len(pair[1]))
            ],
            "regressions_without_a_named_cause": sum(
                len(names) for cause, names in causes.items()
                if cause.startswith("NO CAUSE WAS COMPUTED")),
        }


GATE = Gate()
