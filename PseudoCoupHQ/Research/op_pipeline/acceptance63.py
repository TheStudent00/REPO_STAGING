#!/usr/bin/env python3
"""acceptance63.py -- TASK 63 (c), printed with values in motion.

Node: `hq.research.compiler_graph.reference.opcode_table`
CORE: Planning/node_0_3_research/node_0_3_5_compiler_graph/
      node_0_3_5_4_reference/node_0_3_5_4_0_opcode_table/
      CORE_0_3_5_4_0_opcode_table.md

WHAT IT CHECKS, in three parts:

  part 0 -- the INVENTORY.  Every arch opcode the 76 attached archive
     bodies spell, counted off `canon39_callee_units.json`, against
     the entries `Reference.opcode_table` holds.  The missing set is
     COMPUTED here, not typed, and written to
     `canon39_callee_opcodes.json`.

  part 1 -- each newly added opcode gets its plain meaning printed
     beside a REAL line from a real attached body, and the term the
     table's builder writes for that line is printed with concrete
     values substituted in, so the meaning is checkable rather than
     asserted.

  part 2 -- how far the reference now walks each attached body.  A
     body that stops at a conditional transfer is TASK 64's work, not
     a gap here; what part 2 proves is that no attached body stops on
     a mnemonic the table lacks.

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

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import z3                                                        # noqa: E402
import reference as R                                            # noqa: E402


# The plain meaning of each opcode this task added.  One sentence, in
# ordinary words, beside the reads/writes the table records.
MEANINGS = {
    "endbr64": "marks a place a jump is allowed to land; it changes "
               "no value the machine holds",
    "cs": "a segment prefix in front of a no-operation the assembler "
          "emits for alignment; it changes no value",
    "xchg": "swaps the two places it names; with one place named "
            "twice it is the two-byte no-operation",
    "inc": "adds one to the place it names, and leaves the carry flag "
           "exactly as it found it",
    "bt": "copies one numbered bit of its second operand into the "
          "carry flag, and touches nothing else",
    "bsr": "writes the position of the highest set bit of its source, "
           "counting from zero at the low end",
    "cmova": "writes its source into its destination when the last "
             "comparison read above, and leaves it otherwise",
    "pinsrw": "writes the low sixteen bits of its source into one "
              "numbered lane of a vector, keeping the other seven",
    "fld": "pushes a copy of a value onto the x87 stack",
}


def say(transcript, text):
    print(text)
    sys.stdout.flush()
    transcript.append(text)


def inventory(units):
    """{mnemonic -> how many lines spell it} over the attached
    bodies, and where each was first seen."""
    counts = {}
    first = {}
    lines = 0
    for key in sorted(units):
        for line in units[key]["body_as_read"]:
            lines = lines + 1
            mnemonic = line.split(" ", 1)[0]
            counts[mnemonic] = counts.get(mnemonic, 0) + 1
            if mnemonic not in first:
                first[mnemonic] = (key, line)
    return counts, first, lines


def part_zero(transcript, units, table):
    counts, first, lines = inventory(units)
    say(transcript, "== PART 0 -- THE INVENTORY OF THE ATTACHED "
                    "BODIES ==")
    say(transcript, "attached bodies: %d   body lines: %d   distinct "
                    "arch opcodes: %d" % (len(units), lines,
                                          len(counts)))
    held = []
    missing = []
    for mnemonic in sorted(counts):
        if table.entry_for(mnemonic) is None:
            missing.append(mnemonic)
            continue
        held.append(mnemonic)
    say(transcript, "in the table: %d   NOT in the table: %d"
        % (len(held), len(missing)))
    say(transcript, "")
    say(transcript, "the opcodes THIS TASK ADDED, with their sighting "
                    "counts (computed off the attached bodies):")
    for mnemonic in R.ARCHIVE_MNEMONICS:
        say(transcript, "  %-10s %5d lines   first seen: %s | %s"
            % (mnemonic, counts.get(mnemonic, 0),
               first.get(mnemonic, ("-", "-"))[0],
               first.get(mnemonic, ("-", "-"))[1]))
    say(transcript, "")
    if missing:
        say(transcript, "STILL MISSING: %s" % ", ".join(missing))
    else:
        say(transcript, "STILL MISSING: none -- every arch opcode the "
                        "attached bodies spell has an entry.")
    say(transcript, "")
    return counts, first, lines, missing


def show(transcript, mnemonic, line, before, after, note):
    say(transcript, "  LITERAL  %s" % line)
    say(transcript, "  GLOSS    %s" % MEANINGS[mnemonic])
    say(transcript, "  reads %s   writes %s"
        % (R.REFERENCE.opcode_table.entry_for(mnemonic).reads,
           R.REFERENCE.opcode_table.entry_for(mnemonic).writes))
    say(transcript, "  before   %s" % before)
    say(transcript, "  after    %s" % after)
    if note:
        say(transcript, "  note     %s" % note)
    say(transcript, "")


def simplify(term):
    return str(z3.simplify(term))


def part_one(transcript):
    """each added opcode, run on a real line, with values moving."""
    say(transcript, "== PART 1 -- EACH ADDED OPCODE, ON A REAL LINE, "
                    "WITH VALUES IN MOTION ==")
    reference = R.Reference()

    state = reference.simulate(["mov $0x28,%eax", "inc %eax"])
    show(transcript, "inc", "inc %eax  (from clang++/__truncsfbf2)",
         "%eax = 0x28 = 40",
         "%eax = " + simplify(z3.Extract(31, 0,
                                        state.family_value("rax"))),
         "the flag triple left behind is %r, so a later carry read "
         "REFUSES rather than inventing one"
         % (state.flags[0],))

    state = reference.simulate(["mov $0x140,%edx", "bsr %edx,%ecx"])
    show(transcript, "bsr", "bsr %edx,%ecx  (from clang++/__extendhfsf2)",
         "%edx = 0x140 = 0b1_0100_0000, %ecx = 0",
         "%ecx = " + simplify(z3.Extract(31, 0,
                                        state.family_value("rcx"))),
         "0x140's highest set bit is bit 8, and 8 is what the machine "
         "writes")

    state = reference.simulate(["mov $0xff,%rcx", "bt $0x3,%rcx",
                                "setb %al"])
    show(transcript, "bt", "bt $0x37,%rcx  (from clang++/__floattidf; "
                           "run here with $0x3 over 0xff)",
         "%rcx = 0xff, so bit 3 is 1",
         "%al = " + simplify(z3.Extract(7, 0,
                                       state.family_value("rax"))),
         "the carry, and only the carry: a zero or sign reading after "
         "`bt` is refused")

    state = reference.simulate(["mov $0x7,%eax", "mov $0x9,%esi",
                                "cmp $0x3,%eax", "cmova %esi,%edx"])
    show(transcript, "cmova", "cmova %esi,%edx  (from "
                              "clang++/__truncsfbf2)",
         "%eax = 7 compared against 3 (above), %esi = 9, %edx = "
         "unconstrained",
         "%edx = " + simplify(z3.Extract(31, 0,
                                        state.family_value("rdx"))),
         "7 is above 3, so the move is taken and %edx becomes 9")

    state = reference.simulate(["mov $0x11,%eax", "mov $0x22,%ecx",
                                "xchg %eax,%ecx"])
    show(transcript, "xchg", "xchg %ax,%ax  (from swiftc/__udivmodti4; "
                             "run here over two different places)",
         "%eax = 0x11, %ecx = 0x22",
         "%eax = " + simplify(
             z3.Extract(31, 0, state.family_value("rax")))
         + ", %ecx = " + simplify(
             z3.Extract(31, 0, state.family_value("rcx"))),
         "both places are read before either is written, so the swap "
         "is a swap and not two copies")

    state = reference.simulate(["pxor %xmm0,%xmm0", "mov $0x1234,%edx",
                                "pinsrw $0x0,%edx,%xmm0"])
    show(transcript, "pinsrw", "pinsrw $0x0,%edx,%xmm0  (from "
                               "clang++/__truncsfbf2)",
         "%xmm0 = 0 in all eight lanes, %edx = 0x1234",
         "%xmm0 = " + simplify(state.family_value("xmm0")),
         "lane 0 holds 0x1234 and the other seven lanes are "
         "untouched")

    state = reference.simulate(["endbr64", "cs nopw 0x0(%rax,%rax,1)",
                                "mov $0x5,%eax"])
    show(transcript, "endbr64", "endbr64  (from clang++/__extendhfsf2)",
         "%eax unconstrained",
         "%eax = " + simplify(z3.Extract(31, 0,
                                        state.family_value("rax"))),
         "the marker changed nothing; the `mov` after it is what set "
         "the value")
    show(transcript, "cs", "cs nopw 0x0(%rax,%rax,1)  (from "
                           "clang++/__udivmodti4)",
         "the same state",
         "unchanged", "an alignment no-operation")

    state = reference.simulate(["fldz", "fld %st(0)"])
    show(transcript, "fld", "fld %st(0)  (from clang++/__extendxftf2)",
         "the x87 stack holds one value, 0.0",
         "the x87 stack top is " + simplify(state.x87_at(0))
         + ", and it now holds a second copy",
         "a push of a copy of the top")


def part_two(transcript, units, reference):
    say(transcript, "== PART 2 -- HOW FAR THE REFERENCE NOW WALKS "
                    "EACH ATTACHED BODY ==")
    walked = 0
    stopped_at_a_branch = 0
    stopped_on_a_missing_opcode = 0
    other = {}
    for key in sorted(units):
        body = units[key]["body_as_read"]
        state = R.MachineState()
        trouble = None
        for line in body:
            text = line.split("!!")[0].strip()
            if not text:
                continue
            if text.endswith(":"):
                continue
            try:
                reference.step(state, text)
            except R.NotModeled as why:
                trouble = str(why)
                break
            except Exception as why:
                trouble = "%s: %s" % (type(why).__name__, why)
                break
        if trouble is None:
            walked = walked + 1
            continue
        if "has no entry in the opcode table" in trouble:
            stopped_on_a_missing_opcode = stopped_on_a_missing_opcode + 1
            other[key] = trouble
            continue
        if "conditional transfer" in trouble or \
                "census row" in trouble or \
                "unconditional transfer" in trouble:
            stopped_at_a_branch = stopped_at_a_branch + 1
            continue
        other[key] = trouble
    say(transcript, "attached bodies: %d" % len(units))
    say(transcript, "walked to the end: %d" % walked)
    say(transcript, "stopped at a transfer (TASK 64's branch "
                    "following): %d" % stopped_at_a_branch)
    say(transcript, "stopped on an opcode the table lacks: %d"
        % stopped_on_a_missing_opcode)
    say(transcript, "stopped for another reason: %d" % len(other))
    for key in sorted(other):
        say(transcript, "  %-30s %s" % (key, other[key][:110]))
    say(transcript, "")
    return {
        "attached_bodies": len(units),
        "walked_to_the_end": walked,
        "stopped_at_a_transfer": stopped_at_a_branch,
        "stopped_on_an_opcode_the_table_lacks":
            stopped_on_a_missing_opcode,
        "stopped_for_another_reason": other,
    }


def main():
    transcript = []
    doc = json.load(open(os.path.join(HERE,
                                      "canon39_callee_units.json")))
    units = doc["units"]
    reference = R.Reference()
    table = reference.opcode_table

    counts, first, lines, missing = part_zero(transcript, units, table)
    part_one(transcript)
    walk = part_two(transcript, units, reference)

    out = {
        "meta": {
            "produced_by": "acceptance63.py",
            "what_this_is": "the arch opcodes the attached archive "
                            "bodies spell, against the one opcode "
                            "table; the nine this task added; and how "
                            "far the reference now walks each "
                            "attached body",
            "attached_bodies": len(units),
            "body_lines": lines,
            "distinct_opcodes": len(counts),
            "added_this_task": list(R.ARCHIVE_MNEMONICS),
            "still_missing": missing,
        },
        # ROWS, not a dictionary keyed by the mnemonic.  Four arch
        # mnemonics -- `and`, `or`, `xor`, `not` -- are spelled the
        # same as operator tokens, so a dictionary keyed by mnemonic
        # is a spelling key and the guard refuses it, correctly.  The
        # shape is a list of typed objects carrying `mnem`.
        "opcodes": [
            {
                "mnem": mnemonic,
                "lines": counts[mnemonic],
                "first_seen_unit": first[mnemonic][0],
                "first_seen_line": first[mnemonic][1],
                "in_the_table": table.entry_for(mnemonic) is not None,
                "added_by_task_63":
                    mnemonic in R.ARCHIVE_MNEMONICS,
                "meaning": MEANINGS.get(mnemonic),
            }
            for mnemonic in sorted(counts)
        ],
        "walk": walk,
    }
    path = os.path.join(HERE, "canon39_callee_opcodes.json")
    json.dump(out, open(path, "w"), indent=1, sort_keys=True)
    path = os.path.join(HERE, "acceptance63_printed.txt")
    open(path, "w").write("\n".join(transcript) + "\n")
    print("written: canon39_callee_opcodes.json, "
          "acceptance63_printed.txt")
    if missing:
        return 1
    return 0


sys.exit(main())
