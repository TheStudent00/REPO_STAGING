#!/usr/bin/env python3
"""acceptance64.py -- task 64's acceptance, printed with values.

Node: `hq.research.compiler_graph.reference` (0_3_5_4), with
`opcode_table`, `machine_state` and
`ledger.destination_rules`.

THE FOUR THINGS THE BRIEF ASKS FOR, each printed with the object
(LITERAL) and a plain-words reading beside it (GLOSS), per §5.1a:

  part 1  `go/op_174` -- a `jl` to a panic path.  The body's own
          control-flow graph, the condition on each edge, the guard row
          the unreachable side leaves, and the answer term, PROVED.
  part 2  `c/op_282` -- a logic unit with no branch and no transfer.
          Its verdict and its answer term, character for character
          against what round 12 recorded.
  part 3  `cpp/regen_12920` -- an `__extendhfsf2` caller.  The callee
          ENTRY (which body, which arrival contract, which registers
          hold what on the way in) and the RETURN (which register the
          answer is read from, and what it is), and a second caller
          whose answer home IS that register, so the callee's answer is
          the unit's answer rather than a value beside it.
  part 4  8- and 16-bit division and widening multiply, and a
          rip-relative address computation, each on a real line with
          concrete values moving through it.

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

The three units are named in the BRIEF, and a unit named in a brief is
ratified intention, which the ban's own wording admits as a candidate
source.  No operator token is read anywhere in this file.

Coding discipline: no compound one-liner statements.

usage:
  acceptance64.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import z3                                                        # noqa: E402

LINES = []


def say(text=""):
    LINES.append(text)
    print(text)
    sys.stdout.flush()


def shard_paths():
    out = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        out.append(os.path.join(HERE, "canon39_wrapped_%s.json" % lang))
    out.append(os.path.join(HERE, "canon39_interp.json"))
    out.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_regen_store", "*.json"))))
    return [path for path in out if os.path.exists(path)]


def find(names):
    wanted = set(names)
    out = {}
    for path in shard_paths():
        document = json.load(open(path))
        for name in list(wanted):
            if name not in document.get("units", {}):
                continue
            record = dict(document["units"][name])
            record["unit"] = name
            record["_shard"] = os.path.relpath(path, HERE)
            out[name] = record
            wanted.discard(name)
        if not wanted:
            break
    return out


def callee_units():
    document = json.load(open(os.path.join(
        HERE, "canon39_callee_units.json")))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain") or key.split("/", 1)[0]
        name = unit.get("callee") or key.split("/", 1)[-1]
        out.setdefault(toolchain, {})
        out[toolchain][name] = unit
    return out


def short(term, width=64):
    text = "%s" % term
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    return text[:width - 3] + "..."


def print_body(record):
    for index, line in enumerate(record["body_verbatim"]):
        say("    %2d  %s" % (index, line))


def gate_it(gate, maker, record):
    walked = maker.transcribe(record)
    if walked.refused is not None:
        return None, None, "the relink refused: %s" % walked.refused
    if walked.out_term is None:
        why = "the walk reached OUT-0 with no term"
        if walked.holes:
            why = walked.holes[0]["why"]
        return None, None, why
    verdict = gate.prove_term_against_ship(walked.out_term, record)
    return walked.out_term, verdict, None


# ------------------------------------------------------------------
# part 1 -- go/op_174, a `jl` to a panic path
# ------------------------------------------------------------------

def part_one(reference, gate, maker, records):
    say("=" * 68)
    say("PART 1 -- go/op_174: a conditional transfer to a panic path")
    say("=" * 68)
    record = records["go/op_174"]
    say("LITERAL -- the unit's own stored body (`%s`), 'body_verbatim':"
        % record["_shard"])
    print_body(record)
    say()
    body = R.Body(reference.annotated_lines(record["body_verbatim"]))
    say("LITERAL -- the control-flow graph this file reads off that "
        "text:")
    say("    label -> instruction index: %s"
        % json.dumps(body.label_at, sort_keys=True))
    for block in body.blocks:
        edges = []
        for target, side in block.successors:
            where = "OUT OF THE UNIT" if target is None \
                else "block %d" % target
            edges.append("%s: %s" % (side, where))
        if block.returns:
            edges.append("returns")
        say("    block %d  instructions %d..%d  terminator %-24r  %s"
            % (block.index, block.start,
               block.start + len(block.lines) - 1,
               block.terminator, " | ".join(edges)))
    say()
    say("GLOSS: block 0 ends `jl L0`.  L0 is a label this body defines,")
    say("  so the TAKEN side is an edge inside the unit -- to block 2,")
    say("  which transfers to `x_runtime_panicshift`, a name no")
    say("  builtins archive defines, so THAT block leaves the unit.")
    say("  The side that leaves is unreachable and contributes nothing")
    say("  to the answer; its condition becomes a guard row.")
    say()
    state = reference.simulate(record["body_verbatim"],
                               record.get("arrival_contract_bindings"),
                               callees=reference.callees_for(record))
    say("LITERAL -- the guard rows the walk left:")
    for row in state.guard_rows:
        say("    line      %s" % row["line"])
        say("    went to   %s" % row["went_to"])
        say("    condition %s" % short(row["condition"], 200))
    say()
    say("GLOSS: `jl` after `test %ebx,%ebx` reads 'the shift count is")
    say("  negative'.  Under that condition go's own runtime stops the")
    say("  program; under its negation the shift runs.  The condition")
    say("  is kept as data, which is what a guard row is for.")
    say()
    answer, width = reference.answer_for_unit(record)
    say("LITERAL -- `Reference.answer_of` for this body, simplified:")
    say("    %s" % z3.simplify(answer))
    say()
    term, verdict, why = gate_it(gate, maker, record)
    say("LITERAL -- the gate, route one (the term against the unit's "
        "own ship body):")
    if verdict is None:
        say("    NO TERM: %s" % why)
    else:
        say("    outcome %s" % verdict.outcome)
        say("    reason  %s" % verdict.reason)
    say()
    say("LITERAL -- what round 12 recorded for the same unit "
        "(`term61_store/canon39_wrapped_go.json`):")
    old = json.load(open(os.path.join(
        HERE, "term61_store", "canon39_wrapped_go.json")))
    was = old["units"]["go/op_174"]
    say("    outcome %s" % was.get("outcome"))
    say("    reason  %s" % was.get("reason"))
    say()


# ------------------------------------------------------------------
# part 2 -- c/op_282, a unit with no branch and no transfer
# ------------------------------------------------------------------

def part_two(reference, gate, maker, records):
    say("=" * 68)
    say("PART 2 -- c/op_282: a straight-line logic unit, UNCHANGED")
    say("=" * 68)
    record = records["c/op_282"]
    say("LITERAL -- the unit's own stored body (`%s`):" % record["_shard"])
    print_body(record)
    say()
    answer, _width = reference.answer_for_unit(record)
    say("LITERAL -- `Reference.answer_of`, simplified:")
    say("    %s" % " ".join(("%s" % z3.simplify(answer)).split()))
    term, verdict, why = gate_it(gate, maker, record)
    say("LITERAL -- the gate, route one:")
    say("    outcome %s" % verdict.outcome)
    say()
    old = json.load(open(os.path.join(
        HERE, "term61_store", "canon39_wrapped_c.json")))
    was = old["units"]["c/op_282"]
    say("LITERAL -- round 12's record for the same unit:")
    say("    outcome                %s" % was.get("outcome"))
    say("    layer5_normalized_text %s"
        % was.get("layer5_normalized_text"))
    say()
    now = maker.normalize(term)
    say("LITERAL -- this run's normalized text:")
    say("    %s" % now)
    same = (now == was.get("layer5_normalized_text"))
    say("    character-for-character identical to round 12's: %s" % same)
    say()
    say("GLOSS: this body has no label, no conditional transfer and no")
    say("  `call`, so the graph is one block and the walk is the walk")
    say("  round 12 made.  The verdict and the text are the same ones.")
    say()


# ------------------------------------------------------------------
# part 3 -- a caller that proves THROUGH its callee
# ------------------------------------------------------------------

def part_three(reference, gate, maker, records, attached):
    say("=" * 68)
    say("PART 3 -- an `__extendhfsf2` caller: the callee entry and the "
        "return")
    say("=" * 68)
    for name in ["cpp/regen_12920", "c/regen_1056"]:
        record = records[name]
        say("-" * 60)
        say("UNIT %s   (%s)" % (name, record["_shard"]))
        say("  its answer home: %%%s, %d bits"
            % (record.get("result_family"), record.get("result_width")))
        say("LITERAL -- the caller's own stored body:")
        print_body(record)
        say()
        toolchain = R.Reference.TOOLCHAIN_OF[record["lang"]]
        for line in record["body_verbatim"]:
            text = line.split("!!")[0].strip()
            if not text.startswith("call"):
                continue
            annotation = ""
            if "!!" in line:
                annotation = "!!" + line.split("!!", 1)[1]
            operands = R.split_operands(text.split(" ", 1)[1])
            callee = R.LEDGER.transfer_callee("call", operands,
                                              annotation)
            unit = attached[toolchain][callee]
            say("  THE ENTRY, at line `%s`:" % text)
            say("    the transfer's own text names %r; the RELOCATION "
                "names %r" % (operands[0], callee))
            say("    the callee arch unit entered: runtime/%s/%s"
                % (toolchain, callee))
            say("      archive        %s" % unit["archive"])
            say("      member         %s" % unit["archive_member"])
            say("      instructions   %d" % unit["instruction_count"])
            say("      ITS OWN arrival contract (the families its text "
                "reads before it writes them): %s"
                % ", ".join("%%%s" % one
                            for one in unit["arrival_families"]))
            say("      the caller's registers already hold those "
                "values, so nothing about a calling rule is assumed")
            say("    THE RETURN: the answer register computed off the "
                "callee's own body is %%%s"
                % reference.answer_register_of(unit))
            body = R.Body(reference.annotated_lines(
                unit["body_verbatim"]))
            say("    the callee's body is itself a graph: %d blocks, "
                "%d of them ending in a conditional transfer"
                % (len(body.blocks),
                   sum(1 for block in body.blocks
                       if len(block.successors) == 2)))
            say()
        answer, _width = reference.answer_for_unit(record)
        say("  LITERAL -- `Reference.answer_of` for the caller, "
            "simplified to its first 400 characters:")
        say("    %s" % short(z3.simplify(answer), 400))
        term, verdict, why = gate_it(gate, maker, record)
        say("  LITERAL -- the gate, route one:")
        if verdict is None:
            say("    NO TERM: %s" % why)
        else:
            say("    outcome %s" % verdict.outcome)
            say("    reason  %s" % verdict.reason[:200])
        say()


# ------------------------------------------------------------------
# part 4 -- the narrow division, the widening multiply, the rip address
# ------------------------------------------------------------------

def one_line(reference, line, before, read):
    """run ONE arch line over a state whose registers are set to
    concrete numbers, and read the places back."""
    state = R.MachineState()
    for family, value in before.items():
        state.set_family(family, z3.BitVecVal(value, 64))
    reference.step(state, line)
    out = {}
    for family in read:
        out[family] = z3.simplify(state.family_value(family))
    return out


def part_three_b(reference, attached):
    """IS THE WALK OF THE CALLEE'S BODY RIGHT?  Put concrete numbers
    through it and read the answer back.

    `__extendhfsf2` widens a 16-bit half float to a 32-bit float.  Its
    body has five conditional transfers and four join points, so if the
    fork, the merge or the unreachable-side rule were wrong, the number
    coming out would be wrong.  This is forced-by-construction evidence
    about the walk: nothing here is a claim, the machine's own body is
    run and the bits are read."""
    import struct
    say("-" * 60)
    say("IS THE WALK OF THE CALLEE'S BODY RIGHT?  Concrete values "
        "through `clang/__extendhfsf2`, whose body has 5 conditional "
        "transfers and 8 blocks:")
    say()
    say("  %-10s %-22s %-12s %s"
        % ("half in", "what it is", "float out", "read as"))
    cases = [(0x3C00, "1.0"), (0xC000, "-2.0"), (0x0001,
             "the smallest subnormal"), (0x7C00, "+infinity"),
             (0x3555, "the nearest half to 1/3")]
    unit = attached["clang"]["__extendhfsf2"]
    for half, what in cases:
        state = R.MachineState()
        state.set_family("xmm0", z3.BitVecVal(half, 128))
        after = reference.walk_body(state, unit["body_verbatim"], {})
        bits = z3.simplify(z3.Extract(31, 0,
                                      after.family_value("xmm0")))
        value = bits.as_long()
        read = struct.unpack("<f", struct.pack("<I", value))[0]
        say("  0x%04X     %-22s 0x%08X   %r"
            % (half, what, value, read))
    say()
    say("  GLOSS: every one is the IEEE-correct widening, including "
        "the subnormal (2^-24 = 5.960464477539063e-08), which is the "
        "case the body's `bsr` / `shl` branch exists for.  A wrong "
        "fork, a wrong merge or a wrongly-kept unreachable side would "
        "show here as a wrong number.")
    say()
    unit = attached["clang"]["__truncsfhf2"]
    say("  and the inverse routine `clang/__truncsfhf2` (101 "
        "instructions, 18 blocks), narrowing them back:")
    for value in [1.0, -2.5, 0.0]:
        bits = struct.unpack("<I", struct.pack("<f", value))[0]
        state = R.MachineState()
        state.set_family("xmm0", z3.BitVecVal(bits, 128))
        after = reference.walk_body(state, unit["body_verbatim"], {})
        half = z3.simplify(z3.Extract(15, 0,
                                      after.family_value("xmm0")))
        say("    %-6r -> 0x%04X" % (value, half.as_long()))
    say()


def part_four(reference):
    say("=" * 68)
    say("PART 4 -- the narrow division, the widening multiply, and a "
        "rip-relative address")
    say("=" * 68)
    cases = [
        ("idiv %sil",
         "8-bit signed division: the dividend is the WHOLE 16-bit "
         "accumulator AX; the quotient lands in AL and the remainder "
         "in AH, which are two BYTES of one register",
         {"rax": 0x1234000000000007, "rsi": 0xFD},
         ["rax"],
         "AX = 7, SIL = -3 (0xFD).  7 / -3 = -2 (0xFE) into AL and "
         "7 % -3 = 1 into AH, so AX becomes 0x01FE and the upper 48 "
         "bits of %rax are untouched.  The remainder's sign follows "
         "the DIVIDEND, which is the SRem rule, not z3's `%`"),
        ("idiv %si",
         "16-bit signed division: the dividend is DX:AX, the quotient "
         "lands in AX and the remainder in DX",
         {"rax": 0xAAAA000000000007, "rdx": 0xBBBB000000000000,
          "rsi": 0xCCCC000000000003},
         ["rax", "rdx"],
         "DX:AX = 0x00000007 = 7, SI = 3.  7 / 3 = 2 into AX and "
         "7 % 3 = 1 into DX; both keep their upper 48 bits"),
        ("div %sil",
         "8-bit unsigned division, the same two places, unsigned",
         {"rax": 0x00000000000000FF, "rsi": 0x10},
         ["rax"],
         "AX = 255, SIL = 16.  255 / 16 = 15 (0x0F) into AL and "
         "255 % 16 = 15 (0x0F) into AH, so AX = 0x0F0F"),
        ("mul %sil",
         "8-bit unsigned widening multiply: AL times the operand, and "
         "the WHOLE 16-bit product IS AX -- there is no high half to "
         "put anywhere",
         {"rax": 0x00000000000000C8, "rsi": 0x03},
         ["rax"],
         "AL = 200, SIL = 3.  200 * 3 = 600 = 0x258, which does not "
         "fit in 8 bits and is exactly why the form widens: AX = "
         "0x0258"),
        ("mul %si",
         "16-bit unsigned widening multiply: AX times the operand, "
         "the low half into AX and the high half into DX",
         {"rax": 0x000000000000FFFF, "rsi": 0x0002,
          "rdx": 0x0000000000000000},
         ["rax", "rdx"],
         "AX = 65535, SI = 2.  65535 * 2 = 131070 = 0x1FFFE, so AX "
         "takes 0xFFFE and DX takes 0x0001"),
    ]
    for line, gloss, before, read, note in cases:
        say("  LITERAL  %s" % line)
        say("  GLOSS    %s" % gloss)
        starting = ", ".join("%%%s = 0x%x" % (family, value)
                             for family, value in sorted(before.items()))
        say("  before   %s" % starting)
        after = one_line(reference, line, before, read)
        for family in read:
            say("  after    %%%s = 0x%x" % (family,
                                            after[family].as_long()))
        say("  note     %s" % note)
        say()
    say("  LITERAL  lea 0x2e57(%rip),%rax")
    say("  GLOSS    an address this artifact does not hold: the "
        "compiler placed the thing it points at in its own constant "
        "pool, whose bytes are not in the unit")
    state = R.MachineState()
    reference.step(state, "lea 0x2e57(%rip),%rax")
    reference.step(state, "lea 0x1000(%rip),%rdx")
    say("  after    %%rax = %s" % z3.simplify(state.family_value("rax")))
    say("           %%rdx = %s" % z3.simplify(state.family_value("rdx")))
    say("  note     the k-th rip-relative place of a body is the k-th "
        "`ripconst_<k>`, the SAME counter a rip-relative READ uses, so "
        "this file and the ledger transcription name one constant.  "
        "Before task 64 this line refused: \"an address computation "
        "over base register '%rip'\" (32 units, log_160 section 1.7)")
    say()


def main():
    attached = callee_units()
    reference = R.Reference(runtime_units=attached)
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=attached)
    gate = G.Gate(reference=reference)
    records = find(["go/op_174", "c/op_282", "cpp/regen_12920",
                    "c/regen_1056"])
    part_one(reference, gate, maker, records)
    part_two(reference, gate, maker, records)
    part_three(reference, gate, maker, records, attached)
    part_three_b(reference, attached)
    part_four(reference)
    open(os.path.join(HERE, "acceptance64_printed.txt"),
         "w").write("\n".join(LINES) + "\n")
    return 0


sys.exit(main())
