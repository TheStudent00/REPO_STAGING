#!/usr/bin/env python3
"""acceptance58.py -- the acceptance instances for task 58, printed
with values, LITERAL and GLOSS labelled.

  (a) `c/op_246` -- the division remainder.  Withdrawn in log 153
      because the superseded reference computed the remainder with
      z3py's `%` (sign follows the DIVISOR) while the ledger's term
      uses `SRem` (sign follows the DIVIDEND, which is what the
      machine leaves).  It proves here.
  (b) `cpp/regen_36796` -- an x87 compare, UNDECIDED on both routes in
      log 153 for want of any x87 model in either reference.  It
      decides here.
  (c) the wrapped-text route and the six structural checks on
      `c/op_246`, so the other two obligations of the node are shown
      running rather than only described.

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

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate as GATE                                               # noqa: E402
import layer4c                                                    # noqa: E402
import z3                                                         # noqa: E402


def find_unit(name, paths):
    for path in paths:
        document = json.load(open(os.path.join(HERE, path)))
        if name in document["units"]:
            return document["units"][name]
    raise KeyError(name)


def one_line(term):
    return " ".join(("%s" % term).split())


def main(argv):
    gate = GATE.Gate()
    record = {}

    print("PART (a) -- c/op_246, the division remainder, withdrawn in "
          "log 153 and proved here")
    print("")
    unit = find_unit("c/op_246", ["canon38_wrapped_c.json"])
    print("LITERAL -- the unit's own ship body, and its answer home:")
    print("  body:        %s" % unit["body_text"])
    print("  answer home: %s at %d bits"
          % (unit["result_family"], unit["result_width"]))
    transcription = layer4c.transcribe(unit)
    term = transcription.out_term
    print("")
    print("LITERAL -- the ledger's own OUT-0 term, on one line:")
    print("  %s" % one_line(term))
    print("")
    print("LITERAL -- does the ledger's term use SRem?  %s"
          % ("yes" if "bvsrem" in ("%s" % term.decl()) or
             "SRem" in one_line(term) or
             "bvsrem" in one_line(term) else "no"))
    ship = gate.prove_term_against_ship(term, unit)
    text = gate.prove_term_against_text(term, unit)
    print("")
    print("LITERAL -- the two routes:")
    print("  route one (%s): %s" % (ship.route, ship.outcome))
    print("      %s" % ship.reason)
    print("  route two (%s): %s" % (text.route, text.outcome))
    print("      %s" % text.reason)
    print("")
    print("LITERAL -- the two remainders at 32 bits, inputs 7 and -3:")
    a = z3.BitVecVal(7, 32)
    b = z3.BitVecVal(-3, 32)
    solver = z3.Solver()
    remainder = z3.simplify(z3.SRem(a, b))
    modulo = z3.simplify(a % b)
    print("  z3.SRem(7, -3)  = %s" % remainder)
    print("  7 %% -3 in z3py  = %s   (as a signed value: %d)"
          % (modulo, modulo.as_long() - (1 << 32)))
    print("")
    print("LITERAL -- both sides run with the two arrival registers "
          "bound to 7 and -3:")
    bound = {"rdi": z3.BitVecVal(7, 64), "rsi": z3.BitVecVal(-3, 64)}
    state = gate.reference.simulate(unit["body_verbatim"], None, bound)
    concrete = gate.reference.answer_of(
        state, (unit["result_family"], unit["result_width"]))
    print("  the reference's answer = %s" % z3.simplify(concrete))
    ledger_bound = layer4c.transcribe(unit)
    substituted = z3.substitute(
        ledger_bound.out_term,
        (z3.BitVec("seed_rdi", 64), z3.BitVecVal(7, 64)),
        (z3.BitVec("seed_rsi", 64), z3.BitVecVal(-3, 64)))
    print("  the ledger's term      = %s" % z3.simplify(substituted))
    print("")
    print("GLOSS.  x86's own division leaves a remainder whose sign "
          "follows the DIVIDEND: 7 divided by -3 leaves 1.  z3py's "
          "`%` on a bit vector is `bvsmod`, whose sign follows the "
          "DIVISOR, and gives -2.  The superseded reference computed "
          "the second and compared it against a ledger term computing "
          "the first, which is the whole of log 153 section 5's "
          "415-unit withdrawal.  Both sides now say 1 and the solver "
          "proves them equal for every input, not only for these two.")
    record["c/op_246"] = {
        "route one": ship.as_dict(),
        "route two": text.as_dict(),
        "the reference's answer at 7 and -3":
            "%s" % z3.simplify(concrete),
        "the ledger's term at 7 and -3":
            "%s" % z3.simplify(substituted),
    }

    print("")
    print("")
    print("PART (b) -- cpp/regen_36796, an x87 compare, UNDECIDED on "
          "both routes in log 153 and decided here")
    print("")
    unit = find_unit(
        "cpp/regen_36796",
        [os.path.join("canon38_regen_store",
                      "op_units2_cpp_c0091.json")])
    print("LITERAL -- the unit's own ship body:")
    for line in unit["body_verbatim"]:
        print("  %s" % line)
    print("")
    print("LITERAL -- log 153 section 4.3's verdict on this unit:")
    print("  route one (the ship simulation): UNDECIDED")
    print("  route two (the text-order walk): UNDECIDED")
    transcription = layer4c.transcribe(unit)
    term = transcription.out_term
    print("")
    print("LITERAL -- the ledger's own OUT-0 term:")
    print("  %s" % one_line(term))
    print("")
    state = gate.reference.simulate(unit["body_verbatim"][:2], None)
    print("LITERAL -- the x87 stack after the unit's own two loads:")
    print("  position 0 (the top)  %s" % state.x87_at(0))
    print("  position 1            %s" % state.x87_at(1))
    print("  depth                 %d" % state.x87["depth"])
    whole = gate.reference.simulate(unit["body_verbatim"], None)
    answer = gate.reference.answer_of(
        whole, (unit["result_family"], unit["result_width"]))
    print("")
    print("LITERAL -- the reference's own answer term:")
    print("  %s" % one_line(answer))
    ship = gate.prove_term_against_ship(term, unit)
    text = gate.prove_term_against_text(term, unit)
    print("")
    print("LITERAL -- the two routes now:")
    print("  route one (%s): %s" % (ship.route, ship.outcome))
    print("      %s" % ship.reason)
    print("  route two (%s): %s" % (text.route, text.outcome))
    print("      %s" % text.reason)
    print("")
    print("LITERAL -- the values moving.  Take the memory the two "
          "loads read as 0x18(%rsp) = 2.0 and 0x8(%rsp) = 3.0:")
    top = state.x87_at(0)
    second = state.x87_at(1)
    solver = z3.Solver()
    solver.add(top == z3.FPVal(3.0, top.sort()))
    solver.add(second == z3.FPVal(2.0, second.sort()))
    solver.add(z3.Extract(0, 0, term) != z3.BitVecVal(1, 1))
    print("  the ledger's term with those two values, asked to be "
          "anything but 1: %s" % solver.check())
    print("")
    print("GLOSS.  The first load puts 2.0 on the x87 register stack; "
          "the second pushes 3.0 on top, so position 0 holds 3.0 and "
          "position 1 holds 2.0.  The compare is AT&T order -- source "
          "%st(1), destination %st -- so it compares the top against "
          "position 1, and the condition asks for above-and-ordered: "
          "3.0 is above 2.0 and neither is NaN, so the answer is 1.  "
          "`unsat` above means the term cannot be anything else at "
          "those two values.  Both loads are in the answer, which is "
          "what log 153 section 4.3 could not reach: neither "
          "superseded reference modelled the x87 stack at all.")
    record["cpp/regen_36796"] = {
        "route one": ship.as_dict(),
        "route two": text.as_dict(),
        "the reference's answer term": one_line(answer),
    }

    print("")
    print("")
    print("PART (c) -- the other two obligations of this node, run on "
          "c/op_246")
    print("")
    unit = find_unit("c/op_246", ["canon38_wrapped_c.json"])
    wrapped = gate.prove_wrapped(unit["wrapped_text"], unit)
    print("LITERAL -- the wrapped text:")
    print("  %s" % unit["wrapped_text"])
    print("")
    print("LITERAL -- prove_wrapped: %s" % wrapped.outcome)
    print("  route:            %s" % wrapped.route)
    print("  reason:           %s" % wrapped.reason)
    print("  counterexample:   %s" % wrapped.counterexample)
    print("  solver timeout:   %d ms" % wrapped.solver_timeout_ms)
    print("")
    passed, notes = gate.structural_checks(unit["wrapped_text"], unit)
    print("LITERAL -- structural_checks: all six passed = %s" % passed)
    for note in notes:
        print("  %s" % note)
    record["c/op_246 wrapped"] = wrapped.as_dict()
    record["c/op_246 structural checks"] = {
        "all six passed": passed,
        "notes": notes,
    }

    handle = open(os.path.join(HERE, "acceptance58.json"), "w")
    json.dump({
        "meta": {
            "produced_by": "acceptance58.py",
            "population": "three named units of the 30,436",
        },
        "instances": record,
    }, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
