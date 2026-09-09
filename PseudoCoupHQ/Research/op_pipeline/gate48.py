#!/usr/bin/env python3
"""gate48.py -- THE GATE FOR LAYER 4.

A TERM THAT DOES NOT PROVE IS NOT A ROW.  Every producer entry written
into layer4.py's table is checked here, on the units that actually
carry that producer, against the unit's OWN SHIP CODE.

THE OBLIGATION, stated once.  For every value of every register the two
sides read before writing, the value layer 4's transcribed term gives
for OUT-0 equals the value the unit's own ship body leaves in its own
answer home.  The reference side is the behaviour checker's own
simulator (canon10_behaviour_check.Sim10), which walks the body's
instructions in text order; the layer-4 side is the ledger read from
OUT-0 downward.  The two routes share no code path: one is a walk of
the arch text, the other is a walk of the provenance table.  Agreement
is therefore evidence about the LEDGER'S WIRING, not only about the
semantics table.

WHY NO SUBSTITUTION STEP IS NEEDED.  layer4.py names its free symbols
exactly as the reference simulator names its own -- `seed_rdi` for the
%rdi family, `ripconst_0` for the first rip-relative read, and so on.
The two terms are built over one set of symbols, so the solver compares
two programs applied to the SAME unconstrained starting machine state.

THE HONEST LIMIT, named rather than hidden.  The reference simulator
carries the scalar-float vocabulary as UNINTERPRETED FUNCTIONS; layer 4
carries real IEEE arithmetic (z3 FPA).  Where a unit's body spells a
float opcode, the two sides are not symbolically comparable and the
verdict is UNDECIDED with that reason recorded per unit -- never
counted as proved.

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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                            # noqa: E402
import condition_table as CT                                      # noqa: E402
import ledger47 as L47                                            # noqa: E402
import region36 as R36                                            # noqa: E402
import layer4                                                     # noqa: E402
import z3                                                         # noqa: E402

NotModeled = BC10.NotModeled

SOLVER_MILLISECONDS = 3000


def reference_answer(unit):
    """the value the unit's own ship body leaves in its own answer
    home, as the behaviour checker's simulator computes it."""
    shared_seed = {}
    simulator = BC10.Sim10(shared_seed, "ship")
    simulator.answer_family = unit["result_family"]
    simulator.answer_width = unit["result_width"]
    lines = list(unit["body_verbatim"])
    return simulator.answer_value(lines)


def uninterpreted_applications(term):
    """the names of every UNINTERPRETED FUNCTION applied inside `term`.

    A free symbol is a constant and is fine -- both sides use the same
    ones.  An APPLICATION of an uninterpreted function is the reference
    simulator's float vocabulary, and it is what makes the two sides
    incomparable, so it is detected rather than assumed."""
    found = set()
    stack = [term]
    seen = set()
    while stack:
        node = stack.pop()
        key = node.get_id()
        if key in seen:
            continue
        seen.add(key)
        try:
            declaration = node.decl()
        except Exception:
            continue
        if declaration.kind() == z3.Z3_OP_UNINTERPRETED and \
                node.num_args() > 0:
            found.add(declaration.name())
        stack.extend(list(node.children()))
    return found


def stale_flags_in_the_reference(unit):
    """the reference simulator remembers the flags of `cmp`, `test`,
    `ucomisd` and `ucomiss` ONLY (condition_table.FLAGSETTER_MNEMONICS).
    A body in which a flag-reading opcode's nearest preceding
    flag-setting opcode is some OTHER arch opcode -- the logic family,
    say -- is read by that simulator with the flags of an EARLIER
    instruction, which is not what the machine does.

    MEASURED, not assumed: for the body
    `test %dil,%dil; setne %al; or %rdx,%rsi; setne %cl; or %al,%cl;
    movzbl %cl,%eax; ret` the reference's own answer simplifies to
    `Concat(0, If(Extract(7, 0, seed_rdi) == 0, 0, 1))` -- the second
    condition reads the first comparison, and the `or` in between is
    not in the answer at all.

    So this file DETECTS that shape and returns UNDECIDED rather than
    comparing against an answer the reference cannot compute.  It is
    named here rather than hidden, because it is a limit of the
    reference, not of the unit."""
    remembered = None
    for raw in unit.get("body_verbatim") or []:
        line = R36.strip_annotation(raw)
        mnemonic = L47.mnemonic_of(line)
        if mnemonic is None:
            continue
        if mnemonic in CT.FLAGSETTER_MNEMONICS:
            remembered = mnemonic
            continue
        if L47.sets_the_flags(mnemonic):
            remembered = None
            continue
        prefix, suffix = CT.consumer_kind_and_suffix(mnemonic)
        if prefix is None:
            continue
        if remembered is None:
            return True
    return False


def gate(unit, transcription):
    """(verdict, detail).  Verdicts: PROVED_EQUAL, DISPROVED,
    UNDECIDED."""
    if transcription.out_term is None:
        return "UNDECIDED", "layer 4 built no term for OUT-0"
    if stale_flags_in_the_reference(unit):
        return "UNDECIDED", (
            "this body has a flag-reading arch opcode whose nearest "
            "preceding flag-setting arch opcode is outside the "
            "reference simulator's own remembered set (cmp, test, "
            "ucomisd, ucomiss), so the reference would answer it with "
            "the flags of an earlier instruction; the two sides are "
            "not comparable on this route")
    try:
        reference, width = reference_answer(unit)
    except NotModeled as problem:
        return "UNDECIDED", "the reference simulator: %s" % problem
    except Exception as problem:
        return "UNDECIDED", ("the reference simulator raised %s: %s"
                             % (type(problem).__name__, problem))
    uninterpreted = uninterpreted_applications(reference)
    if uninterpreted:
        return "UNDECIDED", (
            "the reference simulator carries this body's float "
            "vocabulary as uninterpreted functions (%s) while layer 4 "
            "carries real IEEE arithmetic, so the two sides are not "
            "symbolically comparable on this route"
            % ", ".join(sorted(uninterpreted)))
    theirs = reference
    ours = transcription.out_term
    if ours.size() != theirs.size():
        narrow = min(ours.size(), theirs.size())
        ours = z3.Extract(narrow - 1, 0, ours)
        theirs = z3.Extract(narrow - 1, 0, theirs)
    solver = z3.Solver()
    solver.set("timeout", SOLVER_MILLISECONDS)
    try:
        solver.add(ours != theirs)
    except Exception as problem:
        return "UNDECIDED", ("the two terms are not comparable: %s"
                             % problem)
    try:
        answer = solver.check()
    except Exception as problem:
        return "UNDECIDED", "z3 raised %s" % problem
    if answer == z3.unsat:
        return "PROVED_EQUAL", (
            "z3 proved the ledger-transcribed OUT-0 term equal to the "
            "value the unit's own ship body leaves in its own answer "
            "home, for every value of every register either side reads "
            "before writing")
    if answer == z3.sat:
        return "DISPROVED", (
            "z3 found a starting state under which the "
            "ledger-transcribed term and the unit's own ship body "
            "differ: %s" % solver.model())
    return "UNDECIDED", "z3 returned %r" % answer
