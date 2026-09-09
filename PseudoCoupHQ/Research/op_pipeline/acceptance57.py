#!/usr/bin/env python3
"""acceptance57.py -- TASK 57's acceptance instances for `reference.py`
(node 0_3_5_4 reference), printed with values.

Parts, in the brief's own order:

  0  the table itself: how many arch opcodes the corpus spells, how
     many entries the table carries, and which entries have NO builder
     (the census rows).
  a  `c/op_246` -- the division remainder.  The answer term uses
     `SRem`; inputs `7, -3` give `1`, and what z3's `%` would have
     given is printed beside it so the fix is visible.
  b  `c/regen_11491` -- the push/pop unit.  The machine stack round
     trips: the value pushed is the value popped.
  c  `cpp/regen_36796` -- the x87 compare unit.  Both loads reach the
     compare: the two X87 rows and the compare's own two operands.

Every printed block is labelled LITERAL (a value read or computed by
this program, pasted as it came) or GLOSS (this program's own words
about it), per the communication protocol section 5.1a.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim."

The three units are named by their machine-form unit ids, which is how
the brief names them; no operator token selects, groups or pairs
anything here.

usage:
  acceptance57.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import reference as REF                                       # noqa: E402
import z3                                                     # noqa: E402

OUT_JSON = os.path.join(HERE, "acceptance57.json")

WANTED = ("c/op_246", "c/regen_11491", "cpp/regen_36796")


def unit_records():
    """every canon38 unit record this program needs, found by its own
    `unit` field."""
    found = {}
    paths = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        paths.append(os.path.join(HERE,
                                  "canon38_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon38_interp.json"))
    paths.extend(sorted(glob.glob(
        os.path.join(HERE, "canon38_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for record in document.get("units", {}).values():
            name = record.get("unit")
            if name in WANTED:
                found[name] = record
        if len(found) == len(WANTED):
            break
    return found


def line(text=""):
    print(text)


def part_zero(reference, summary):
    table = reference.opcode_table
    missing = table.without_a_builder()
    line("=" * 68)
    line("PART 0 -- the ONE table")
    line("=" * 68)
    line()
    line("LITERAL -- computed by this program:")
    line("  arch opcodes the corpus's own bodies spell   %d"
         % len(REF.CORPUS_MNEMONICS))
    line("  entries in Reference.opcode_table            %d"
         % len(table.entries))
    line("  entries WITH a term builder                  %d"
         % (len(table.entries) - len(missing)))
    line("  entries with NO builder (census rows)        %d"
         % len(missing))
    line()
    line("LITERAL -- the census rows, by name:")
    for mnemonic in missing:
        entry = table.entry_for(mnemonic)
        line("  %-10s reads %s" % (mnemonic, ", ".join(entry.reads)
                                   or "nothing"))
        if entry.cause is not None:
            line("             cause: %s" % entry.cause)
    line()
    line("GLOSS.  Every arch opcode any body in the corpus spells has")
    line("exactly one entry.  An opcode with no builder is a census")
    line("row and is refused BY NAME when a body reaches it, never")
    line("stepped over.  Fifteen of the nineteen are transfers, which")
    line("this reference refuses because it walks a body in text")
    line("order.  `call` is a transfer into a routine whose body is")
    line("not in the unit YET -- task 59 attaches the runtime callee")
    line("(log_158, TASK 59(b)); until then the refusal says so.")
    line()
    summary["table"] = {
        "arch_opcodes_the_corpus_spells": len(REF.CORPUS_MNEMONICS),
        "entries": len(table.entries),
        "entries_with_a_builder":
            len(table.entries) - len(missing),
        "entries_without_a_builder": len(missing),
        "census_rows": missing,
        "census_causes": dict(
            (name, table.entry_for(name).cause)
            for name in missing
            if table.entry_for(name).cause is not None),
    }


def part_a(reference, unit, summary):
    line("=" * 68)
    line("PART (a) -- c/op_246, the division remainder")
    line("=" * 68)
    line()
    line("LITERAL -- the unit's own ship body, and its answer home:")
    line("  body:        %s" % "; ".join(unit["body_verbatim"]))
    line("  answer home: %s at %d bits"
         % (unit["result_family"], unit["result_width"]))
    line()
    state = reference.simulate(unit["body_verbatim"],
                               unit.get("arrival_contract_bindings"))
    answer = reference.answer_of(
        state, (unit["result_family"], unit["result_width"]))
    printed = str(z3.simplify(answer))
    line("LITERAL -- the answer term this reference builds:")
    for chunk in printed.split("\n"):
        line("  %s" % chunk)
    line()
    uses_signed_remainder = "srem" in printed.lower()
    line("LITERAL -- does the answer term use SRem?  %s"
         % ("yes" if uses_signed_remainder else "no"))
    line()

    # the two remainders, at the same width, on the same inputs.
    width = 32
    dividend = z3.BitVecVal(7, width)
    divisor = z3.BitVecVal(-3, width)
    signed_remainder = z3.simplify(z3.SRem(dividend, divisor))
    modulo_remainder = z3.simplify(dividend % divisor)
    line("LITERAL -- the two remainders at 32 bits, inputs 7 and -3:")
    line("  z3.SRem(7, -3)  = %s   (as a signed value: %d)"
         % (signed_remainder, signed_remainder.as_signed_long()))
    line("  7 %% -3 in z3py  = %s   (as a signed value: %d)"
         % (modulo_remainder, modulo_remainder.as_signed_long()))
    line()

    # the same inputs put through the reference itself.
    bound = {}
    bound["rdi"] = z3.BitVecVal(7, 64)
    bound["rsi"] = z3.BitVecVal((-3) & ((1 << 64) - 1), 64)
    seeded = reference.simulate(unit["body_verbatim"], None, bound)
    concrete = reference.answer_of(
        seeded, (unit["result_family"], unit["result_width"]))
    value = z3.simplify(concrete)
    line("LITERAL -- the reference run on this unit's own body with")
    line("its two arrival registers bound to 7 and -3:")
    line("  answer = %s   (as a signed value: %d)"
         % (value, value.as_signed_long()))
    line()
    line("GLOSS.  `idiv` leaves a remainder whose sign follows the")
    line("DIVIDEND, so 7 divided by -3 leaves 1.  z3py's `%` on a bit")
    line("vector is `bvsmod`, whose sign follows the DIVISOR, and it")
    line("gives -2.  The superseded route computed the second and")
    line("compared it against a ledger term that computed the first,")
    line("which is the whole of the 415-unit withdrawal of log 153")
    line("section 5.  This reference computes 1.")
    line()
    summary["part_a"] = {
        "unit": unit["unit"],
        "body": unit["body_verbatim"],
        "answer_term_uses_signed_remainder": uses_signed_remainder,
        "signed_remainder_of_7_and_minus_3":
            signed_remainder.as_signed_long(),
        "modulo_remainder_of_7_and_minus_3":
            modulo_remainder.as_signed_long(),
        "reference_answer_on_7_and_minus_3":
            value.as_signed_long(),
    }


def part_b(reference, unit, summary):
    line("=" * 68)
    line("PART (b) -- c/regen_11491, the machine stack")
    line("=" * 68)
    line()
    line("LITERAL -- the unit's own ship body:")
    for step in unit["body_verbatim"]:
        line("  %s" % step)
    line()
    line("LITERAL -- the unit's own ledger rows:")
    for row in unit["ledger"]:
        line("  %-8s %-32s %s"
             % (row["row"], row["type"],
                json.dumps(row["produced_by"], sort_keys=True)))
    line()

    # the push, run on this unit's own first body line.
    state = reference.simulate(unit["body_verbatim"][:1], None)
    offset = state.stack["offset"]
    stored = state.stack["cells"][offset]
    line("LITERAL -- the machine state after the unit's own `push`:")
    line("  stack pointer   %s" % z3.simplify(state.stack["pointer"]))
    line("  cell at offset  %d" % offset)
    line("  cell holds      %s" % z3.simplify(stored))
    line()

    # the round trip, proved rather than asserted.
    popped_state = reference.simulate(
        ["push %rax", "pop %rcx"], None)
    popped = popped_state.family_value("rcx")
    pushed = popped_state.seed("rax")
    solver = z3.Solver()
    solver.add(popped != pushed)
    verdict = solver.check()
    line("LITERAL -- the round trip, put to z3:")
    line("  pushed  %s" % pushed)
    line("  popped  %s" % z3.simplify(popped))
    line("  solver.add(popped != pushed); solver.check() = %s"
         % verdict)
    line("  stack pointer back to  %s"
         % z3.simplify(popped_state.stack["pointer"]))
    line("  stack offset back to   %d" % popped_state.stack["offset"])
    line()

    # what this unit's own body does next, said honestly.
    try:
        reference.simulate(unit["body_verbatim"], None)
        refusal = None
    except REF.NotModeled as problem:
        refusal = str(problem)
    line("LITERAL -- the whole body, walked:")
    line("  refused: %s" % refusal)
    line()
    line("GLOSS.  The value the `push` puts at stack offset -8 is the")
    line("value a `pop` takes back: z3 answers `unsat` to the two")
    line("being different, which is a proof for every value of the")
    line("register, not a sample.  The pointer and the offset both")
    line("return to where they started.  This unit's own body then")
    line("transfers into `__divti3`, a compiler support routine whose")
    line("body is not in the unit YET: the owner's round-12 ruling (log_158,")
    line("TASK 59(b)) is that the callee's body is extracted from the")
    line("toolchain's libgcc / compiler-rt archive and attached as an")
    line("ArchUnit this caller references, with the producer")
    line("{\"kind\": \"runtime_callee\", \"callee\": \"__divti3\"}.")
    line("Task 59 delivers that attachment (node 0_3_5_1_8).  Until it")
    line("lands the table carries `call` as an entry with no builder")
    line("and the walk refuses it by name with that reason -- the")
    line("earlier \"out of scope\" framing is superseded.")
    line()
    summary["part_b"] = {
        "unit": unit["unit"],
        "body": unit["body_verbatim"],
        "stack_offset_after_the_push": offset,
        "cell_holds": str(z3.simplify(stored)),
        "round_trip_solver_answer": str(verdict),
        "round_trip_is_proved": verdict == z3.unsat,
        "pointer_after_the_pop":
            str(z3.simplify(popped_state.stack["pointer"])),
        "whole_body_refusal": refusal,
    }


def part_c(reference, unit, summary):
    line("=" * 68)
    line("PART (c) -- cpp/regen_36796, the x87 compare")
    line("=" * 68)
    line()
    line("LITERAL -- the unit's own ship body:")
    for step in unit["body_verbatim"]:
        line("  %s" % step)
    line()
    line("LITERAL -- the unit's own ledger rows:")
    for row in unit["ledger"]:
        line("  %-8s %-24s %-34s %s"
             % (row["row"], row["type"],
                json.dumps(row["produced_by"], sort_keys=True),
                ",".join(row.get("operands") or [])))
    line()

    # the two loads, read straight off the machine state.
    after_loads = reference.simulate(unit["body_verbatim"][:2], None)
    top = after_loads.x87_at(0)
    below = after_loads.x87_at(1)
    line("LITERAL -- the x87 stack after the unit's own two loads:")
    line("  position 0 (the top)  %s" % top)
    line("  position 1            %s" % below)
    line("  depth                 %d" % after_loads.x87["depth"])
    line()

    after_compare = reference.simulate(unit["body_verbatim"][:3], None)
    setter, left, right = after_compare.flags
    line("LITERAL -- the flag triple the compare leaves:")
    line("  setter            %s" % setter)
    line("  left  (the top)   %s" % left)
    line("  right (position 1)%s" % right)
    line()

    state = reference.simulate(unit["body_verbatim"], None)
    answer = reference.answer_of(
        state, (unit["result_family"], unit["result_width"]))
    printed = str(z3.simplify(answer))
    line("LITERAL -- the answer term this reference builds:")
    for chunk in printed.split("\n"):
        line("  %s" % chunk)
    line()
    reaches = str(left) in printed and str(right) in printed
    line("LITERAL -- do BOTH loads appear in the answer term?  %s"
         % ("yes" if reaches else "no"))
    line()
    line("GLOSS.  `fldt 0x18(%rsp)` loads 2.0 and becomes position 0.")
    line("`fldt 0x8(%rsp)` loads 3.0 and pushes on top, so position 0")
    line("holds 3.0 and position 1 holds 2.0.  `fucomip %st(1),%st` is")
    line("AT&T order -- source `%st(1)`, destination `%st` -- so it")
    line("compares the top against position 1 and leaves the triple")
    line("(fucomip, top, position 1).  `seta` asks for above and")
    line("ordered, which is exactly the two loads compared, and both")
    line("of them are in the answer term.")
    line()
    summary["part_c"] = {
        "unit": unit["unit"],
        "body": unit["body_verbatim"],
        "x87_position_0": str(top),
        "x87_position_1": str(below),
        "flag_setter": setter,
        "flag_left": str(left),
        "flag_right": str(right),
        "both_loads_reach_the_answer": reaches,
    }


def main(argv):
    reference = REF.Reference()
    records = unit_records()
    for name in WANTED:
        if name not in records:
            print("MISSING unit record: %s" % name)
            return 2
    summary = {
        "meta": {
            "generator": "acceptance57.py",
            "form": "the acceptance instances of task 57, printed "
                    "with values; every figure computed by this "
                    "program from the units' own canon38 records",
        },
    }
    part_zero(reference, summary)
    part_a(reference, records["c/op_246"], summary)
    part_b(reference, records["c/regen_11491"], summary)
    part_c(reference, records["cpp/regen_36796"], summary)
    handle = open(OUT_JSON, "w")
    json.dump(summary, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s" % OUT_JSON)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
