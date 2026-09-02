#!/usr/bin/env python3
"""interp_join_prover33.py -- the prover for a canonical text that has
a DESIGNATED LOCATION in it.

WHY IT EXISTS, and it is a cause fixed at first observation.
`build_interp_join1.py`'s first run put php's three specialised
handlers to `cross_unit_prover.prove_pair` and got UNDECIDED on every
one of 267 candidate pairs, with the prover naming its own limit:

    this file's reused integer simulator (canon8_behaviour_check.Sim8)
    has no model for a mnemonic in this pair's text -- an instrument
    limit, not an unknowable-input case: operand '-0x8(%rsp)' is
    neither an immediate nor a plain register

That is not a fact about php.  It is the simulator predating the owner's
2026-09-01 designated-memory ruling.  TASK 30 already built the
simulator that does model it -- `canon33_gate.Sim33`, whose own
docstring calls the addition "the designated-location store" -- so the
fix is to use that simulator here, not to carry the UNDECIDED as a
finding.  `cross_unit_prover.py` is imported for its population and
its class keys and is NOT edited.

THE ENTRY-CONTRACT BINDING, which is the whole soundness argument.
An interpreter unit whose operand `a` arrives in designated location
S0 and a compiled unit whose operand `a` arrives in `%rdi` are being
asked whether they compute the same thing FROM THE SAME INPUTS.  So
the two seats must start from the same symbol.  This file binds them:
for each seat the renderer recorded as a designated location, the
simulator's seed for that slot is set to the SAME z3 symbol the
compiled side's designated register seed uses.  This is the entry
contract's own rule -- "value-here + needed-there produces the adapter
mov by rule" (AgentMemory, 2026-08-26) -- applied to the seed dict
instead of to emitted text.  Without the binding the proof would be
vacuously undecidable; with it the proof is the real question.

WHAT IT REFUSES.  Anything Sim33 has no model for comes back
UNDECIDED with Sim33's own words, unchanged.  Nothing is forced.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.
"""

import z3

import canon8_behaviour_check as BC8
import canon10_behaviour_check as BC10
import canon33_gate as G33

PER_PAIR_TIMEOUT_MS = 12000

SEAT_REGISTER = {"operand_1": "rdi", "operand_2": "rsi"}


def bind_seats(shared_seed, seats):
    """the entry-contract binding.  -> the list of bindings made, for
    the record."""
    made = []
    if not seats:
        return made
    for name in sorted(seats):
        seat = seats[name]
        if seat.get("seat_kind") != "designated location":
            continue
        family = SEAT_REGISTER.get(name)
        if family is None:
            continue
        symbol = BC8.seed_family(shared_seed, family)
        shared_seed["slot_%s" % seat["text"]] = symbol
        made.append({
            "seat": name,
            "designated_location": seat["text"],
            "bound_to_the_same_symbol_as": "%%%s" % family,
            "why": "the designated location IS this operand's seat, so "
                   "it holds the same value the compiled unit receives "
                   "in its designated register",
        })
    return made


def prove_pair_33(interp_text, seats, compiled_text):
    """(verdict, detail, bindings)."""
    shared_seed = {}
    bindings = bind_seats(shared_seed, seats)
    lines_a = [line.strip() for line in interp_text.split(";")]
    lines_b = [line.strip() for line in compiled_text.split(";")]
    try:
        val_a, width_a = G33.Sim33(shared_seed, "interp").answer_value(
            lines_a)
        val_b, width_b = G33.Sim33(shared_seed, "compiled").answer_value(
            lines_b)
    except (BC10.NotModeled, G33.NotModeled) as exc:
        return "UNDECIDED", (
            "canon33_gate.Sim33 (task 30's designated-location "
            "simulator) has no model for a mnemonic in this pair's "
            "text -- an instrument limit, not an unknowable-input "
            "case: %s" % exc), bindings
    width = min(width_a, width_b)
    val_a = z3.Extract(width - 1, 0, val_a)
    val_b = z3.Extract(width - 1, 0, val_b)
    solver = z3.Solver()
    solver.set("timeout", PER_PAIR_TIMEOUT_MS)
    solver.add(val_a != val_b)
    result = solver.check()
    if result == z3.unsat:
        return "PROVED", (
            "z3 proved bit-level equality at %d bits for every value of "
            "every seat either text reads before writing, with the "
            "designated locations bound to the compiled side's "
            "designated registers (%dms timeout)"
            % (width, PER_PAIR_TIMEOUT_MS)), bindings
    if result == z3.sat:
        return "DISPROVED", (
            "z3 found a counterexample: %s" % solver.model()), bindings
    return "UNDECIDED", (
        "z3 returned %r (timeout at %dms, or otherwise declined to "
        "decide) -- counted honestly"
        % (result, PER_PAIR_TIMEOUT_MS)), bindings
