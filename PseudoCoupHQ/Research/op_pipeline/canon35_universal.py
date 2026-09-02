#!/usr/bin/env python3
"""canon35_universal.py -- TASK 39: THE UNIVERSAL-FORM MIGRATION for
every compiled unit.

WHAT THIS FILE IS.  Round 7 put the 9 interpreter units into the
universal canonical form (interp_canon35.py, log_124).  The 1,779
compiled units still carried register-first canonical texts.  the owner's
correction (2026-09-01, verbatim): "not just interpreter languages.
ive been saying 'canonical form using universal memory' in reference
to everything. for every language."  This file renders EVERY compiled
unit into the same universal form.

--------------------------------------------------------------------
THE UNIVERSAL-FORM RENDERING FOR A COMPILED UNIT, STATED MECHANICALLY
--------------------------------------------------------------------

A unit's universal text is exactly three segments, in this order:

    <standardized loads>      one per traced argument, designation order
    <the computation core>    the unit's own newest canonical core
    <the answer store>  + ret the answer to its designated location

1.  THE DESIGNATED LOCATIONS (the directory).  Fixed for every unit in
    the corpus, no per-unit variation:

        S0  -0x8(%rsp)    holds  a       (argument 1)
        S1  -0x10(%rsp)   holds  b       (argument 2, when the unit
                                          has one; unused otherwise)
        S2  -0x18(%rsp)   holds  answer

    The addresses come from designated_memory.slot_text(i), unchanged
    (log_118).  They sit in the System V 128-byte red zone, so the
    form still needs no prologue.  S2 is reserved for the answer even
    in a one-argument unit: the directory is a STANDARD, so `answer
    lives at S2` must not depend on how many arguments a unit takes.

2.  THE PRIVATE REGION, and why a bias exists.  Some units already
    spell stack-relative scratch of their own (`overflow_slots_used`
    1 or 2, plus the own-frame `lea` units that park a byte or a word
    at -0x1(%rsp) / -0x4(%rsp)).  When such an address is one of
    S0/S1/S2 it would COLLIDE with the directory.  Only then is a bias
    applied, and it is applied to EVERY stack-relative displacement in
    that unit at once, as one uniform act: PRIVATE_BIAS = 0x20 shifts
    -0x1(%rsp) to -0x21(%rsp) and -0x8(%rsp) to -0x28(%rsp), clear of
    the whole directory (S0..S3).  The same
    constant is added to every displacement, so the unit's own scratch
    keeps its exact relative structure and only moves.  A unit whose
    displacements do not collide is left untouched -- the smallest
    change that makes the directory sound.  A unit whose text names
    `(%rsp)` with no displacement, or any %rbp-relative address, is
    REFUSED BY NAME rather than biased by guesswork.  A unit whose
    ANSWER is the address of one of its own private locations cannot
    survive a bias (the address is what moves), and the gate disproves
    it; that refusal is recorded with that cause.

3.  THE STANDARDIZED LOAD.  One pattern for everyone:

        integer-file argument   mov  <slot>,%<64-bit designated reg>
        vector-file argument    movq <slot>,%xmm<k>

    The designated register is the one the unit's own entry contract
    already names (canon4_units_<lang>.json `entry_contract`: a ->
    rdi or xmm0, b -> rsi/xmm0/xmm1, per canon.designated()).  The
    registers are the standardized VEHICLES; the memory locations are
    the definition.  The load is always full-width (64 bits) so that
    the pattern does not vary with the argument's declared width: a
    core that reads %edi or %dil reads the low lanes of the same
    loaded value.

4.  THE COMPUTATION CORE.  The unit's own newest canonical text with
    its trailing `ret` removed and the private bias of (2) applied.
    Nothing else is rewritten: the core already reads the designated
    registers, which is what the standardized loads have just filled.

5.  THE ANSWER.  The answer is stored to its designated location AND
    remains in its register:

        integer result   mov  %rax,-0x18(%rsp)
        vector result    movq %xmm0,-0x18(%rsp)

    Both homes are recorded in the artifact
    (`answer_seats`: {"designated_location": "-0x18(%rsp)",
    "designated_register": "%rax"}).  The store is the last act
    before `ret`, so it cannot disturb the computation.  The record
    also carries `universal_text_no_answer_store`, the same text
    without that one line, because the interpreter side's universal
    form (interp_canon35.py) does not emit it -- so the two views can
    be compared on identical ground without either being re-rendered.

6.  THE ARRIVAL ANNOTATION.  Read, never invented, from
    canon33_arrival_modes.json's `compiled` map: plain for compiled
    scalar units (measured 1,776), typed-pointer(T) where the
    log_117/118 machinery measured a dereferenced arrival (measured
    3: rust/op_786, rust/op_793, rust/op_800).  The annotation rides
    BESIDE the text and is never spelled inside it -- that is what
    lets a pointer-arriving unit and a plain-arriving unit meet on
    the same memory-based form.

7.  THE PRECONDITIONS, each refusing by name:
      P1  the core must not write a designated location.  After the
          bias of (2) no stack write can land on S0/S1/S2, so P1 can
          only fail through a write whose address this file cannot
          read -- and that case is already refused in (2).  It is
          still checked, and reported, rather than assumed.
      P2  for a VECTOR arrival, every core line that reads the
          arrival register must be lane-wise: a scalar-float
          operation or a bit-parallel packed one, whose low lane
          depends only on the operands' low lanes.  A designated
          location holds a VALUE, eight bytes; the standardized load
          therefore fills the low lane and zeroes the rest, so a unit
          whose answer depends on the upper lanes of an arriving
          register depends on something that is not the value.  That
          is a finding, and it is recorded by name rather than
          rendered.
      P3  the unit must present an entry contract naming its
          arguments and its result.

    A PRECONDITION THIS RENDER DOES NOT NEED, named so its absence is
    not read as an oversight: the interpreter lap (interp_canon35.py)
    had to check that the core does not write a designated operand
    register before its last read of it, because THAT lap rewrote
    register names inside the core (it deleted park-reloads and
    substituted the designated register downstream).  This lap copies
    the core VERBATIM and only prepends loads, so a core that
    overwrites an arrival register does exactly what it did before --
    there is nothing to clobber.  The first-mention shape is still
    measured and recorded per unit (`first_mention_of_each_arrival`)
    as information, never as a refusal.

--------------------------------------------------------------------
THE GATE
--------------------------------------------------------------------

TWO gates run on every unit, and BOTH verdicts are recorded.  Both
bind THE ARRIVAL CONTRACT:

    slot_-0x8(%rsp)   is bound to the same symbol as the canonical
                      a-register
    slot_-0x10(%rsp)  is bound to the same symbol as the canonical
                      b-register

so the proof obligation is exactly the ruled one: FOR ALL VALUES IN
THE DESIGNATED LOCATIONS, the universal text computes what the
original computes on those values.

  GATE 1, THE ADMISSION GATE -- the universal text against THE UNIT'S
  OWN PRIOR CANONICAL TEXT, z3, under Sim35.  This is the interpreter
  lap's gate shape (interp_canon35.py, log_124 section 3), reused
  because the prior text is itself already gate-proved against the
  unit's own ship code by the generation that converged it; the chain
  universal == prior == ship is therefore a proof against the ship
  code that does not re-litigate gate quirks this lap did not touch.
  A unit that does not prove here keeps NO universal text.

  GATE 1b, THE STRUCTURAL ROUTE, used only where gate 1 returns
  UNDECIDED (the simulator has no model for some mnemonic the unit
  spells).  It is a proof BY CONSTRUCTION rather than by solver, and
  it is admissible only when every one of these holds, each checked
  mechanically and recorded:
      (i)   the computation core is character-identical to the prior
            canonical text's core -- no bias was applied, nothing was
            substituted;
      (ii)  the standardized loads write only the arrival registers,
            one line each, and each load's source is that arrival's
            designated location;
      (iii) no core line names S0, S1 or S2 in any operand;
      (iv)  the answer store is the last line before `ret`, it reads
            the answer register and writes S2, and no core line reads
            S2;
      (v)   P2's lane-safety holds for every vector arrival.
  Under (i)-(v) the universal text executes the same instruction
  sequence as the prior text on the same register state -- the loads
  establish exactly the arrival values the prior text assumed, and
  the store touches a location nothing else reads.  Equivalence is
  therefore forced by construction, and the record says
  PROVED_BY_CONSTRUCTION with the five checks listed.

  GATE 2, THE DIRECT SHIP GATE -- the universal text against the
  unit's own ship code, canon33_gate's own straight-line checker with
  the arrival contract bound.  Recorded per unit as
  `ship_gate_verdict` / `ship_gate_detail`.  Where it proves, the
  universal text stands on the ship code with no chain at all.  Where
  it refuses, the reason is recorded verbatim and the unit rests on
  gate 1's chain; the refusal reasons are tallied in the report, never
  averaged away.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

The population key here is machine-form throughout: the corpus of
canon31_units_<lang>.json, the recorded entry_contract, the recorded
branch shape.  `operator` is carried once per record as a display
label and is read by nothing.

Coding discipline: no complex/compound one-liner statements.

CHECKPOINTING.  Work is written to canon35_universal_<lang>.json after
every CHECKPOINT_EVERY units.  A re-run skips units already present in
that file, so an interrupted lap resumes rather than restarting.

usage:
  canon35_universal.py --lang c [--limit N] [--fresh]
  canon35_universal.py --all
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import canon8_behaviour_check as BC8                             # noqa: E402
import canon10_behaviour_check as BC10                           # noqa: E402
import canon33_gate as G33                                       # noqa: E402
import designated_memory as DM                                   # noqa: E402
import dominant_table17 as DT17                                  # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
CHECKPOINT_EVERY = 25
PRIVATE_BIAS = 0x20

SLOT_A = DM.slot_text(0)
SLOT_B = DM.slot_text(1)
SLOT_ANSWER = DM.slot_text(2)
SLOT_D = DM.slot_text(3)

WIDEST = {
    "rdi": "%rdi",
    "rsi": "%rsi",
    "rax": "%rax",
    "rdx": "%rdx",
    "rcx": "%rcx",
    "r8": "%r8",
    "r9": "%r9",
}

RSP_DISP = re.compile(r"-0x([0-9a-fA-F]+)\(%rsp\)")
BARE_RSP = re.compile(r"(?<![x0-9a-fA-F])\(%rsp\)")
RBP_ANY = re.compile(r"\(%rbp\)")


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def split_lines(text):
    out = []
    for piece in text.split(";"):
        piece = piece.strip()
        if piece:
            out.append(piece)
    return out


def operands_of(line):
    parts = line.split(" ", 1)
    if len(parts) == 1:
        return []
    return [x.strip() for x in G33.split_operands(parts[1])]


def is_vector_family(family):
    if family is None:
        return False
    return family.startswith("xmm")


def register_text(family):
    """the standardized vehicle for a designated register family."""
    if is_vector_family(family):
        return "%" + family
    text = WIDEST.get(family)
    if text is not None:
        return text
    return "%" + family


def load_line(family, slot):
    if is_vector_family(family):
        return "movq %s,%s" % (slot, register_text(family))
    return "mov %s,%s" % (slot, register_text(family))


def store_line(family, slot):
    if is_vector_family(family):
        return "movq %s,%s" % (register_text(family), slot)
    return "mov %s,%s" % (register_text(family), slot)


# ------------------------------------------------------------------
# the private region: bias every stack-relative displacement
# ------------------------------------------------------------------

COLLIDING = frozenset([8, 16, 24])

# mnemonics whose destination operand is written without being read.
PURE_WRITE = frozenset([
    "mov", "movq", "movd", "movabs", "movzx", "movzbl", "movzwl",
    "movsbl", "movswl", "movslq", "movsbq", "movswq", "lea", "movss",
    "movsd", "movaps", "movapd", "movdqa", "movdqu", "cvtsi2ss",
    "cvtsi2sd", "cvtss2sd", "cvtsd2ss", "cvttss2si", "cvttsd2si",
    "sete", "setne", "setl", "setle", "setg", "setge", "setb", "setbe",
    "seta", "setae", "setp", "setnp", "sets", "setns", "seto", "setno",
    "xorps", "xorpd",
])

# mnemonics whose low lane depends only on the operands' low lanes:
# the scalar-float operations, and the bit-parallel packed ones.
LANE_WISE = frozenset([
    "addss", "addsd", "subss", "subsd", "mulss", "mulsd", "divss",
    "divsd", "minss", "minsd", "maxss", "maxsd", "sqrtss", "sqrtsd",
    "ucomiss", "ucomisd", "comiss", "comisd", "cmpss", "cmpsd",
    "cvtss2sd", "cvtsd2ss", "cvttss2si", "cvttsd2si", "cvtsi2ss",
    "cvtsi2sd", "movss", "movsd", "movq", "movd",
    "andps", "andpd", "andnps", "andnpd", "orps", "orpd", "xorps",
    "xorpd", "pand", "pandn", "por", "pxor",
    # lane-preserving copies: each lane of the result is the same lane
    # of the source
    "movaps", "movapd", "movdqa", "movdqu",
])
for _suffix in ("ss", "sd"):
    for _predicate in ("eq", "lt", "le", "unord", "neq", "nlt", "nle",
                       "ord"):
        LANE_WISE = LANE_WISE | frozenset(
            ["cmp" + _predicate + _suffix])


def stack_check(core_in):
    """(needs_bias, refusal_or_None) over the whole core at once."""
    needs = False
    for line in core_in:
        if RBP_ANY.search(line):
            return False, ("the text names a %rbp-relative address, "
                           "which the universal form's red-zone "
                           "directory cannot place")
        if BARE_RSP.search(line):
            return False, ("the text names `(%rsp)` with no "
                           "displacement, which cannot be placed in "
                           "the private region without guessing")
        for hit in RSP_DISP.finditer(line):
            if int(hit.group(1), 16) in COLLIDING:
                needs = True
    return needs, None


def bias_line(line):
    def shift(match):
        old = int(match.group(1), 16)
        return "-0x%x(%%rsp)" % (old + PRIVATE_BIAS)

    return RSP_DISP.sub(shift, line)


# ------------------------------------------------------------------
# the newest canonical text of a compiled unit
# ------------------------------------------------------------------

def newest_text_sources():
    """(canon33 map, canon32-sret map, DT17 generation docs)."""
    c33 = {}
    doc33 = load("canon33_units.json")
    for label, rec in doc33["units"].items():
        if rec.get("outcome") != "newly_converged":
            continue
        c33[label] = "; ".join(rec["candidate"])
    c32 = {}
    doc32 = load("canon32_sret_units.json")
    for key, rec in doc32["members"].items():
        lang, _, n = key.partition("/")
        c32["%s/op_%s" % (lang, n)] = "; ".join(rec["canonical_text"])
    DT17.GENERATIONS = ["canon24"] + DT17.GENERATIONS
    gen_docs = DT17.load_generation_docs()
    return c33, c32, gen_docs


def newest_text_of(lang, n, c33, c32, gen_docs):
    label = "%s/op_%s" % (lang, n)
    if label in c33:
        return c33[label], "canon33_units.json (newly converged)"
    if label in c32:
        return c32[label], "canon32_sret_units.json (displaced ABI)"
    text, gen = DT17.final_text_of(lang, n, gen_docs)
    if text is None:
        return None, None
    return text, gen


# ------------------------------------------------------------------
# the render
# ------------------------------------------------------------------

ARRIVAL_FAMILIES = ("rdi", "rsi", "xmm0", "xmm1")


def infer_entry_contract(text):
    """the entry contract read off the unit's OWN TEXT, for the units
    that carry no canon4 record.  Machine-form evidence only: a family
    is an ARRIVAL when the text reads it before it writes it, and the
    designations follow canon.designated()'s own rule (a takes rdi, or
    xmm0 when the first argument is a floating-point value; b takes
    rsi, xmm1 when a is also floating point, xmm0 otherwise)."""
    arrives = {}
    for family in ARRIVAL_FAMILIES:
        arrives[family] = False
    seen_write = {}
    for family in ARRIVAL_FAMILIES:
        seen_write[family] = False
    for line in split_lines(text):
        mnemonic = line.split(" ", 1)[0]
        operands = operands_of(line)
        for position, operand in enumerate(operands):
            if not operand.startswith("%"):
                continue
            family = canon.FAMILY_OF.get(operand[1:])
            if family not in arrives:
                continue
            is_write = position == len(operands) - 1
            if is_write and mnemonic in PURE_WRITE:
                seen_write[family] = True
                continue
            if not seen_write[family]:
                arrives[family] = True
    a_family = None
    if arrives["rdi"]:
        a_family = "rdi"
    elif arrives["xmm0"]:
        a_family = "xmm0"
    b_family = None
    if arrives["rsi"]:
        b_family = "rsi"
    elif arrives["xmm1"]:
        b_family = "xmm1"
    elif arrives["xmm0"] and a_family != "xmm0":
        b_family = "xmm0"
    result = "rax"
    lowered = text
    if "%rax" not in lowered:
        if "%eax" not in lowered:
            if "%al" not in lowered:
                result = "xmm0"
    return {"a": a_family, "b": b_family, "result": result}


def weave_blocks(core, loads, answer_store):
    """the universal form of a BLOCK-LIST core.  (with_store,
    without_store, refusal).

    The loads go immediately after the entry label, ahead of every
    executable instruction, so they run once before anything else; a
    branch back to the entry label re-runs them, which is harmless
    because no line of the core writes a designated location (checked
    as P1 and again as structural check (iii)).  The answer store goes
    immediately before every `ret`, so whichever path the unit takes,
    the answer reaches its designated location and stays in its
    register."""
    first_instruction = None
    for index, line in enumerate(core):
        if line.endswith(":"):
            continue
        first_instruction = index
        break
    if first_instruction is None:
        return None, None, ("the block-list text carries no executable "
                            "instruction")
    ret_count = 0
    for line in core:
        if line == "ret":
            ret_count = ret_count + 1
    if ret_count == 0:
        return None, None, ("the block-list text never returns, so the "
                            "answer has no place to be stored")
    with_store = []
    without = []
    for index, line in enumerate(core):
        if index == first_instruction:
            with_store.extend(loads)
            without.extend(loads)
        if line == "ret":
            with_store.append(answer_store)
        with_store.append(line)
        without.append(line)
    return "; ".join(with_store), "; ".join(without), None


def seat_spec_of(entry_contract, displaced):
    """the designations in designation order, and the result family.

    Ordinary contract: a, then b when the unit has one.  DISPLACED-ABI
    contract (canon32's measured three-seat family): the result
    destination first, then a, then b -- the order the ABI itself
    hands them over, so the directory mirrors the arrival."""
    if displaced is not None:
        spec = []
        for seat in displaced["seats"]:
            spec.append((seat["designation"], seat["register"]))
        return spec, displaced["exit"]["register"]
    spec = [("a", entry_contract.get("a"))]
    if entry_contract.get("b") is not None:
        spec.append(("b", entry_contract.get("b")))
    return spec, entry_contract.get("result")


def render(entry_contract, prior_text, displaced=None):
    """(record_fields, refusal_or_None)."""
    if not prior_text:
        return None, ("no canonical text exists for this unit in any "
                      "generation, so there is nothing to re-render "
                      "into the universal form")
    if not entry_contract and displaced is None:
        return None, ("P3 fails: this unit carries no recorded entry "
                      "contract, so its designations cannot be seated")
    spec, r_family = seat_spec_of(entry_contract or {}, displaced)
    if spec[0][1] is None:
        return None, ("P3 fails: the entry contract names no first "
                      "argument")
    if r_family is None:
        return None, ("P3 fails: the entry contract names no result "
                      "home")

    lines = split_lines(prior_text)
    block_form = False
    for line in lines:
        if line.endswith(":"):
            block_form = True
    if block_form:
        core_in = list(lines)
    elif lines and lines[-1] == "ret":
        core_in = lines[:-1]
    else:
        core_in = list(lines)

    needs_bias, refusal = stack_check(core_in)
    if refusal is not None:
        return None, refusal
    core = []
    for line in core_in:
        if needs_bias:
            core.append(bias_line(line))
        else:
            core.append(line)

    # ---- P1: no write to a designated location.
    for line in core:
        operands = operands_of(line)
        if len(operands) != 2:
            continue
        destination = operands[1]
        if destination in (SLOT_A, SLOT_B, SLOT_ANSWER, SLOT_D):
            return None, ("P1 fails: the core writes the designated "
                          "location %s at %r" % (destination, line))

    seats = []
    for order, pair in enumerate(spec):
        seats.append((pair[0], pair[1], DM.slot_text(order)))
    answer_slot = DM.slot_text(max(2, len(seats)))

    # ---- P2: lane safety for a vector arrival.
    lane_safe = {}
    for designation, family, _slot in seats:
        if not is_vector_family(family):
            lane_safe[designation] = True
            continue
        unsafe = None
        for line in core:
            mnemonic = line.split(" ", 1)[0]
            reads = False
            operands = operands_of(line)
            for position, operand in enumerate(operands):
                if not operand.startswith("%"):
                    continue
                if canon.FAMILY_OF.get(operand[1:]) != family:
                    continue
                if position != len(operands) - 1:
                    reads = True
                elif mnemonic not in PURE_WRITE:
                    reads = True
            if not reads:
                continue
            if mnemonic in LANE_WISE:
                continue
            unsafe = (mnemonic, line)
            break
        if unsafe is not None:
            return None, ("P2 fails: the arrival %s is a vector value "
                          "and the core reads its register with %r "
                          "(%r), which is not lane-wise -- its low "
                          "lane can depend on the upper lanes, which "
                          "a designated location's eight bytes do not "
                          "carry" % (designation, unsafe[0], unsafe[1]))
        lane_safe[designation] = True

    # ---- the first-mention shape, recorded as information.
    first_mention = {}
    for designation, family, _slot in seats:
        shape = "never mentioned"
        for line in core:
            mnemonic = line.split(" ", 1)[0]
            operands = operands_of(line)
            hit = None
            for position, operand in enumerate(operands):
                if not operand.startswith("%"):
                    continue
                if canon.FAMILY_OF.get(operand[1:]) != family:
                    continue
                if position != len(operands) - 1:
                    hit = "read"
                elif mnemonic in PURE_WRITE:
                    hit = "written without being read"
                else:
                    hit = "read and written"
                break
            if hit is not None:
                shape = hit
                break
        first_mention[designation] = shape

    loads = []
    directory = []
    for order, seat in enumerate(seats):
        designation, family, slot = seat
        loads.append(load_line(family, slot))
        directory.append({
            "designation": designation,
            "designated_location": slot,
            "location_name": DM.designation_name(order),
            "loaded_into": register_text(family),
            "register_file": "vector" if is_vector_family(family)
                             else "general",
        })
    answer_store = store_line(r_family, answer_slot)
    directory.append({
        "designation": "answer",
        "designated_location": answer_slot,
        "location_name": DM.designation_name(max(2, len(seats))),
        "stored_from": register_text(r_family),
        "register_file": "vector" if is_vector_family(r_family)
                         else "general",
    })

    if block_form:
        universal, without_store, refusal = weave_blocks(
            core, loads, answer_store)
        if refusal is not None:
            return None, refusal
    else:
        universal = loads + core + [answer_store, "ret"]
        without_store = loads + core + ["ret"]
    if block_form:
        universal_text = universal
        no_store_text = without_store
    else:
        universal_text = "; ".join(universal)
        no_store_text = "; ".join(without_store)
    return {
        "universal_text": universal_text,
        "universal_text_no_answer_store": no_store_text,
        "block_form": block_form,
        "standardized_loads": loads,
        "computation_core": core,
        "answer_store": answer_store,
        "designated_location_directory": directory,
        "answer_seats": {
            "designated_location": answer_slot,
            "designated_register": register_text(r_family),
        },
        "preconditions_checked": ["P1", "P2", "P3"],
        "first_mention_of_each_arrival": first_mention,
        "private_region_bias_applied": needs_bias,
        "private_region_bias": "-0x%x" % PRIVATE_BIAS,
    }, None


# ------------------------------------------------------------------
# the gate, with the arrival contract bound
# ------------------------------------------------------------------

class Sim35(G33.Sim33):
    """Sim33 with the scalar-float spellings of a designated-location
    move added to the set it models.  MEASURED CAUSE, not a guess: the
    own-frame units park a float with `movss %xmm0,-0x4(%rsp)` /
    `movsd %xmm0,-0x8(%rsp)`, and Sim33's SLOT_MNEMONICS tuple lists
    only mov/movd/movq, so those lines refused by name.  The width is
    the mnemonic's own suffix (ss = 32, sd = 64), which is why the
    generic width_of_operand path cannot serve here."""

    FLOAT_SLOT_WIDTH = {"movss": 32, "movsd": 64, "movq": 64}

    def exec_line(self, line):
        text = line.strip()
        parts = text.split(" ", 1)
        mnemonic = parts[0]
        width = self.FLOAT_SLOT_WIDTH.get(mnemonic)
        if width is None:
            return G33.Sim33.exec_line(self, line)
        rest = parts[1] if len(parts) > 1 else ""
        operands = G33.split_operands(rest)
        if len(operands) == 2:
            source, destination = operands
            slot_side = None
            if G33.is_slot_text(destination):
                slot_side = "store"
            if G33.is_slot_text(source):
                slot_side = "load"
            if slot_side == "load" and self.is_xmm(destination):
                value = self.slot_value(source, width)
                self.write_xmm(destination,
                               self.zero_extend_to_128(value))
                return None
            if slot_side == "store" and self.is_xmm(source):
                value = self.lane(self.read_xmm(source), 0, width)
                self.slots[destination] = (value, width)
                return None
        if len(operands) != 2:
            return G33.Sim33.exec_line(self, line)
        source, destination = operands
        if G33.is_slot_text(destination):
            value = self.read_at(source, width)
            self.slots[destination] = (value, width)
            return None
        if G33.is_slot_text(source):
            value = self.slot_value(source, width)
            self.write(destination, value)
            return None
        return G33.Sim33.exec_line(self, line)


GATE_PRIVATE_BIAS = 0x200


def rename_prior_slots(text):
    """THE NAME CLASH, the same one interp_canon35.py fixed at first
    observation.  The prior text may park its own scratch at
    -0x8(%rsp), which is the universal form's S0 -- a different seat
    entirely.  Binding both texts' slots by their text would put one
    value's symbol on the other's seat and ask the wrong question.  So
    for the gate, and only for the gate, the prior text's stack
    displacements are moved to gate-private names.  Nothing stored
    changes."""

    def shift(match):
        old = int(match.group(1), 16)
        return "-0x%x(%%rsp)" % (old + GATE_PRIVATE_BIAS)

    return RSP_DISP.sub(shift, text)


def bind_arrival(shared_seed, directory):
    """the arrival contract: each designated location carries the same
    value the canonical form's designated register carries."""
    made = []
    for entry in directory:
        if entry["designation"] == "answer":
            continue
        designation = entry["designation"]
        family = entry["loaded_into"][1:]
        family = canon.FAMILY_OF.get(family, family)
        slot = entry["designated_location"]
        if is_vector_family(family):
            if family not in shared_seed:
                shared_seed[family] = BC10.z3.BitVec(
                    "seed_%s" % family, 128)
            value = shared_seed[family]
        else:
            value = BC8.seed_family(shared_seed, family)
        shared_seed["slot_%s" % slot] = value
        made.append({
            "designation": designation,
            "designated_location": slot,
            "bound_to_the_same_symbol_as": "%%%s" % family,
        })
    return made


STACK_LEA = re.compile(r"lea\s+-0x[0-9a-fA-F]+\(%rsp\)")


def disproof_cause(prior_text, needs_bias):
    """the ONE cause this lap can name mechanically for a disproof."""
    if not needs_bias:
        return None
    if not STACK_LEA.search(prior_text or ""):
        return None
    return ("the answer of this unit is the ADDRESS of one of its own "
            "private stack locations, and that location collides with "
            "the directory (S0/S1/S2), so the universal form must move "
            "it -- which moves the answer.  This unit's answer is not "
            "invariant under a designated-location directory placed in "
            "the red zone; what would change it is a ruled directory "
            "base other than %rsp for units whose answer is an address")


def structural_route(record, prior_text):
    """GATE 1b.  (True, checks) when equivalence is forced by
    construction; (False, reason) otherwise."""
    checks = []
    if record.get("private_region_bias_applied"):
        return False, ("(i) fails: this unit's private stack region "
                       "was biased, so its core is not character-"
                       "identical to the prior text's core")
    prior_lines = split_lines(prior_text)
    prior_core = prior_lines
    if not record.get("block_form"):
        if prior_core and prior_core[-1] == "ret":
            prior_core = prior_core[:-1]
    if record["computation_core"] != prior_core:
        return False, ("(i) fails: the rendered core differs from the "
                       "prior text's core")
    checks.append("(i) the core is character-identical to the prior "
                  "text's core")

    wanted = []
    for entry in record["designated_location_directory"]:
        if entry["designation"] == "answer":
            continue
        wanted.append("%s %s,%s" % (
            "movq" if entry["register_file"] == "vector" else "mov",
            entry["designated_location"], entry["loaded_into"]))
    if record["standardized_loads"] != wanted:
        return False, ("(ii) fails: the standardized loads are not "
                       "exactly one load per arrival from its own "
                       "designated location")
    checks.append("(ii) the standardized loads write only the arrival "
                  "registers, one line each, each from its own "
                  "designated location")

    for line in record["computation_core"]:
        for slot in (SLOT_A, SLOT_B, SLOT_ANSWER, SLOT_D):
            if slot in line:
                return False, ("(iii) fails: the core names the "
                               "designated location %s at %r"
                               % (slot, line))
    checks.append("(iii) no core line names a designated location")

    store = record["answer_store"]
    if not store.endswith(record["answer_seats"]["designated_location"]):
        return False, "(iv) fails: the answer store does not write S2"
    if record.get("block_form"):
        rets = 0
        stores = 0
        for line in split_lines(record["universal_text"]):
            if line == "ret":
                rets = rets + 1
            if line == store:
                stores = stores + 1
        if rets != stores:
            return False, ("(iv) fails: the block-list text has %d "
                           "returns and %d answer stores"
                           % (rets, stores))
        placed = split_lines(record["universal_text"])
        for index, line in enumerate(placed):
            if line != "ret":
                continue
            if index == 0 or placed[index - 1] != store:
                return False, ("(iv) fails: a `ret` at line %d is not "
                               "preceded by the answer store" % index)
        checks.append("(iv) every one of the %d returns is immediately "
                      "preceded by the answer store, which writes the "
                      "answer's designated location" % rets)
        checks.append("(v) lane safety holds for every vector arrival "
                      "(P2, checked at render time)")
        return True, checks
    checks.append("(iv) the answer store is the last line before "
                  "`ret`, reads the answer register and writes the "
                  "answer's designated location, which no core line "
                  "reads")

    checks.append("(v) lane safety holds for every vector arrival "
                  "(P2, checked at render time)")
    return True, checks


def answer_home_of(lang, n, canon4_docs, entry_contract):
    """the answer home the GROUND TRUTH names, read off the unit's own
    real ship text; the recorded entry contract's result family at 64
    bits when the ship text names none."""
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is not None:
        lines_real = [ln.strip() for ln in real_text.split(";")]
        home, width = BC10.answer_home_from_real(lines_real)
        if home is not None:
            return home, width, "the unit's own real ship text"
    return (entry_contract.get("result"), 64,
            "the recorded entry contract (the ship text names no "
            "answer home)")


def gate_against_prior(lang, n, canon4_docs, sem_docs, entry_contract,
                       directory, prior_text, universal_text,
                       needs_bias):
    """GATE 1.  (verdict, detail, bindings)."""
    home, width_home, home_source = answer_home_of(
        lang, n, canon4_docs, entry_contract)
    shared_seed = BC10._prepare_seed(lang, n, sem_docs)
    bindings = bind_arrival(shared_seed, directory)
    if needs_bias:
        lines_prior = split_lines(rename_prior_slots(prior_text))
    else:
        lines_prior = split_lines(prior_text)
    lines_universal = split_lines(universal_text)
    sim_prior = Sim35(shared_seed, "prior")
    sim_universal = Sim35(shared_seed, "universal")
    for sim in (sim_prior, sim_universal):
        sim.answer_family = home
        sim.answer_width = width_home
    try:
        val_prior, w_prior = sim_prior.answer_value(lines_prior)
        val_universal, w_universal = sim_universal.answer_value(
            lines_universal)
    except (BC10.NotModeled, G33.NotModeled) as bad:
        return "UNDECIDED", str(bad), bindings
    width = min(w_prior, w_universal)
    left = BC10.z3.Extract(width - 1, 0, val_prior)
    right = BC10.z3.Extract(width - 1, 0, val_universal)
    solver = BC10.z3.Solver()
    solver.set("timeout", 20000)
    solver.add(left != right)
    outcome = solver.check()
    if outcome == BC10.z3.unsat:
        return ("PROVED_EQUAL",
                "z3 proved the universal text and this unit's own "
                "prior canonical text equal at %d bits in the answer "
                "home %s, for every value of every designated "
                "location, with each location bound to the same "
                "symbol as the designated register it seats; the "
                "answer home comes from %s"
                % (width, home, home_source), bindings)
    if outcome == BC10.z3.sat:
        return ("DISPROVED",
                "z3 found a counterexample: %s" % solver.model(),
                bindings)
    return ("UNDECIDED",
            "z3 returned %r at a 20000ms timeout" % outcome, bindings)


def gate_straight(lang, n, canon4_docs, sem_docs, entry_contract,
                  directory, universal_text):
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is None:
        return "UNDECIDED", "no real ship mnem recorded for this unit", []
    lines_real = [ln.strip() for ln in real_text.split(";")]
    lines_cand = split_lines(universal_text)
    order_real = G33.rip_order_data_only(lines_real)
    order_cand = G33.rip_order_data_only(lines_cand)
    if order_real != order_cand:
        return ("UNDECIDED",
                "the narrowed rip-relative constant guard refused: "
                "real text loads data constants at %r, universal text "
                "at %r" % (order_real, order_cand), [])
    home, width = BC10.answer_home_from_real(lines_real)
    if home is None:
        return ("UNDECIDED",
                "the unit's own real ship code never writes %xmm0 or "
                "an rax-family register", [])
    shared_seed = BC10._prepare_seed(lang, n, sem_docs)
    bindings = bind_arrival(shared_seed, directory)
    sim_real = Sim35(shared_seed, "real")
    sim_cand = Sim35(shared_seed, "universal")
    for sim in (sim_real, sim_cand):
        sim.answer_family = home
        sim.answer_width = width
    try:
        val_real, w_real = sim_real.answer_value(lines_real)
        val_cand, w_cand = sim_cand.answer_value(lines_cand)
    except (BC10.NotModeled, G33.NotModeled) as bad:
        return "UNDECIDED", str(bad), bindings
    verdict, detail = BC10._finish(val_real, w_real, val_cand, w_cand,
                                   home, width)
    return verdict, detail, bindings


# ------------------------------------------------------------------
# the driver
# ------------------------------------------------------------------

def displaced_contracts():
    """the measured three-seat (memory-return) family, canon32."""
    out = {}
    doc = json.load(open(os.path.join(HERE, "canon32_sret_units.json")))
    for key, rec in doc["members"].items():
        lang, _, n = key.partition("/")
        out["%s/op_%s" % (lang, n)] = rec["entry_contract_after"]
    return out


def finish(record, verdict, detail, bindings):
    record["gate_verdict"] = verdict
    record["gate_detail"] = detail
    record["arrival_contract_bindings"] = bindings
    if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
        record["outcome"] = "UNIVERSAL_TEXT_PROVED"
        record["admitted_by"] = verdict
        return record
    record["outcome"] = "GATE_" + verdict
    record["universal_text"] = None
    record["universal_text_no_answer_store"] = None
    return record


def out_path(lang):
    return os.path.join(HERE, "canon35_universal_%s.json" % lang)


def read_checkpoint(lang, fresh):
    if fresh:
        return {}
    path = out_path(lang)
    if not os.path.exists(path):
        return {}
    return json.load(open(path))["units"]


def write_checkpoint(lang, units, tally):
    doc = {
        "meta": {
            "produced_by": "canon35_universal.py",
            "role": "generator provenance",
            "language": lang,
            "population_key": "machine-form: every unit of "
                              "canon31_units_<lang>.json, the corpus "
                              "of record",
            "form": "standardized loads from the designated locations, "
                    "the unit's own computation core, the answer "
                    "stored to its designated location and left in "
                    "its designated register",
            "directory": {"S0": SLOT_A, "S1": SLOT_B,
                          "S2": SLOT_ANSWER},
            "private_region_bias": "-0x%x" % PRIVATE_BIAS,
            "gate": "canon33_gate.Sim33 against the unit's own ship "
                    "code, with the arrival contract bound (each "
                    "designated location carries the same symbol as "
                    "the canonical designated register)",
            "tally": tally,
        },
        "units": units,
    }
    tmp = out_path(lang) + ".tmp"
    fh = open(tmp, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.close()
    os.rename(tmp, out_path(lang))


def tally_of(units):
    out = {}
    for _label, rec in units.items():
        key = rec["outcome"]
        out[key] = out.get(key, 0) + 1
    return out


def run_language(lang, limit, fresh, c33, c32, gen_docs, arrival,
                 displaced):
    canon4_docs = {}
    for other in LANGS:
        canon4_docs[other] = load("canon4_units_%s.json" % other)["units"]
    sem_docs = {}
    for other in LANGS:
        sem_docs[other] = load("sem_anchored_%s.json" % other)["units"]
    canon31 = load("canon31_units_%s.json" % lang)["units"]

    units = read_checkpoint(lang, fresh)
    done = 0
    keys = sorted(canon31, key=lambda x: int(x))
    for n in keys:
        label = "%s/op_%s" % (lang, n)
        if label in units:
            continue
        if limit is not None and done >= limit:
            break
        rec31 = canon31[n]
        c4 = canon4_docs[lang].get(n) or {}
        entry_contract = c4.get("entry_contract")
        branching = "derived_blocks" in c4
        prior_text, prior_source = newest_text_of(lang, n, c33, c32,
                                                  gen_docs)
        record = {
            "unit": label,
            "lang": lang,
            "n": n,
            "operator": rec31.get("operator"),
            "recorded_status": rec31.get("status"),
            "branch_kind": rec31.get("branch_kind"),
            "prior_text": prior_text,
            "prior_text_source": prior_source,
            "entry_contract": entry_contract,
            "arrival_annotation": (arrival.get(label) or {}).get("mode"),
        }
        record["branching"] = branching
        if entry_contract is None and prior_text:
            entry_contract = infer_entry_contract(prior_text)
            record["entry_contract"] = entry_contract
            record["entry_contract_source"] = (
                "inferred from the unit's own text: no canon4 record "
                "exists for this unit, so the arrival families are the "
                "ones the text reads before it writes them")
        fields, refusal = render(entry_contract, prior_text,
                                 displaced.get(label))
        record["displaced_abi"] = displaced.get(label) is not None
        if refusal is not None:
            record["outcome"] = "REFUSED"
            record["refusal"] = refusal
            units[label] = record
            done = done + 1
            continue
        record.update(fields)
        if fields["block_form"]:
            verdict = "UNDECIDED"
            detail = ("the unit's canonical form is a block list, and "
                      "gate 1's simulator walks a straight line; a "
                      "linear walk of a branching text would answer a "
                      "question nobody asked, so it is not run here")
            bindings = []
        else:
            verdict, detail, bindings = gate_against_prior(
                lang, n, canon4_docs, sem_docs, entry_contract,
                fields["designated_location_directory"], prior_text,
                record["universal_text"],
                fields["private_region_bias_applied"])
        if verdict == "DISPROVED":
            named = disproof_cause(prior_text,
                                   fields["private_region_bias_applied"])
            if named is not None:
                detail = named + "  [z3 detail: " + detail + "]"
        record["gate_verdict"] = verdict
        record["gate_detail"] = detail
        record["arrival_contract_bindings"] = bindings
        record["structural_route"] = None
        if verdict == "UNDECIDED":
            ok, note = structural_route(record, prior_text)
            record["structural_route"] = note
            if ok:
                verdict = "PROVED_BY_CONSTRUCTION"
                detail = ("equivalence is forced by construction: the "
                          "universal text executes the prior text's "
                          "own core, verbatim, on the register state "
                          "the standardized loads establish from the "
                          "designated locations")
                record["gate_verdict"] = verdict
                record["gate_detail"] = detail
        if fields["block_form"]:
            ship_verdict = "NOT_APPLICABLE"
            ship_detail = ("the direct ship gate here is the straight-"
                           "line checker, and this unit's canonical "
                           "form is a block list")
            record["ship_gate_verdict"] = ship_verdict
            record["ship_gate_detail"] = ship_detail
            units[label] = finish(record, verdict, detail, bindings)
            done = done + 1
            if done % CHECKPOINT_EVERY == 0:
                write_checkpoint(lang, units, tally_of(units))
            continue
        ship_verdict, ship_detail, _b = gate_straight(
            lang, n, canon4_docs, sem_docs, entry_contract,
            fields["designated_location_directory"],
            record["universal_text"])
        record["ship_gate_verdict"] = ship_verdict
        record["ship_gate_detail"] = ship_detail
        if verdict in ("PROVED_EQUAL", "PROVED_BY_CONSTRUCTION"):
            record["outcome"] = "UNIVERSAL_TEXT_PROVED"
            record["admitted_by"] = verdict
        else:
            record["outcome"] = "GATE_" + verdict
            record["universal_text"] = None
            record["universal_text_no_answer_store"] = None
        units[label] = record
        done = done + 1
        if done % CHECKPOINT_EVERY == 0:
            write_checkpoint(lang, units, tally_of(units))
            sys.stderr.write("  %s: %d done\n" % (lang, len(units)))
            sys.stderr.flush()
    write_checkpoint(lang, units, tally_of(units))
    return tally_of(units), len(units)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--fresh", action="store_true")
    args = ap.parse_args(argv[1:])

    c33, c32, gen_docs = newest_text_sources()
    arrival = load("canon33_arrival_modes.json")["compiled"]
    displaced = displaced_contracts()

    langs = LANGS if args.all else [args.lang]
    for lang in langs:
        tally, total = run_language(lang, args.limit, args.fresh, c33,
                                    c32, gen_docs, arrival, displaced)
        print("%-6s %4d units  %s" % (lang, total,
                                      json.dumps(tally, sort_keys=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
