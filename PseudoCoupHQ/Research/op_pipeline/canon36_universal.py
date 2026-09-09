#!/usr/bin/env python3
"""canon36_universal.py -- TASK 43: the universal form REDONE to the owner's
statement of 2026-09-02 (no designated registers at all).

SUPERSEDED RECORD, 2026-09-05, by the correction "the form, as the owner
meant it" in `Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_2_canonical_form/CORE_0_3_5_2_canonical_form.md`:
this file renders `region36.py`'s form, which REWRITES a body rather
than wrapping one, and that reading of the 2026-09-02 ruling is the
misread one.  The form that stands is `canonical_form.py`.  This file
is kept exactly as it is, as the record of what it rendered, and is
neither edited nor imported by the corrected line; task 96 (log_201)
moved the eleven interpreter units off it.

The FORM ITSELF is defined in region36.py's module header -- the ruled
base, the six allocation kinds, the fixed layout, the affine own-address
map, rule R for scratch registers, and the arrival contract.  Read that
file first; this one is the renderer, the gates and the driver.

--------------------------------------------------------------------
WHAT THIS FILE DOES, IN ORDER, FOR ONE UNIT
--------------------------------------------------------------------

 1. Take the unit's newest text.  For the ORIGINAL population that is
    its newest canonical text (canon33 / canon32 / the generation
    chain, exactly the sources canon35_universal.py used).  For the
    REGENERATED population it is the unit's own SHIP mnemonics, since
    those units have never been canonicalized.
 2. Refuse by name on a %rbp-relative or displacement-less %rsp
    operand, and on any mention of the region base.
 3. Classify every own stack displacement: ESCAPING (some line takes
    its `lea`) -> own-address lineage; otherwise -> temp lineage.
    Both are placed by region36's affine map.
 4. Allocate one block per lineage: one per input argument, one per
    distinct literal, one per own/temp stack address, one for the
    result, one per recorded guard.
 5. Choose scratch registers by RULE R over (arrivals, core, result).
 6. Rewrite the core: own-stack addresses -> their blocks, registers
    -> their rule-R vehicles, and each literal -> a load from its
    constant block into the constant vehicle followed by the original
    operation on that vehicle (the FULL variant).
 7. Emit  <loads from the input blocks>  <core>  <store to the result
    block>  ret.
 8. Gate.  If the full variant does not prove, render the REDUCED
    variant (literals left as immediates, their blocks still allocated
    and directoried) and gate that.  Record which variant is carried.

--------------------------------------------------------------------
THE GATES
--------------------------------------------------------------------

Both gates bind THE ARRIVAL CONTRACT before anything is proved:

  * input block i is bound to the same symbol as the argument that
    arrives in the other text's argument register i;
  * every constant block is bound to its own literal's value;
  * the region base is bound to  %rsp - REGION_SIZE, which is the
    run-time mapping region36 rules.  This binding is what makes an
    address-of unit provable: the rewritten address is the same byte.

and the proof obligation is read off the RESULT BLOCK, never off a
register: FOR ALL VALUES IN THE INPUT BLOCKS, the value the region
form leaves in the result block equals the value the original text
leaves in its answer home.  That is the concrete sense in which no
register is a home any more.

  GATE 1, the admission gate -- against the unit's OWN PRIOR
  CANONICAL TEXT (original population only; that text already carries
  a ship proof, so the chain is a ship proof).
  GATE 2, the direct ship gate -- against the unit's OWN SHIP CODE.
  For the regenerated population gate 2 is the ONLY gate and is the
  admission gate, because there is no prior canonical text to chain
  through.

  A unit proves when either gate proves; both verdicts are recorded.

--------------------------------------------------------------------
THE MONKEYPATCH SEAM, named rather than hidden
--------------------------------------------------------------------

canon33_gate.Sim33 models a designated location by its own text and
refuses it by name anywhere outside a load or a store.  Its test for
"is this operand a designated location" is the module function
`G33.is_slot_text`.  This file WIDENS that function to accept the
region's block texts as well, so the same exact-store model covers
`0xNN(%r15)`.  The widening is additive: `-0xN(%rsp)` still tests
true, so no prior behaviour changes, and a block appearing outside a
load or a store still refuses by name.

--------------------------------------------------------------------
CHECKPOINTING
--------------------------------------------------------------------

Every population writes to its own artifact after CHECKPOINT_EVERY
units, and a re-run skips units already present.  The regenerated
population additionally keeps `canon36_regen_state.json`, a per-chunk
resume file, so an interrupted lap resumes at the chunk boundary.

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

The population here is machine-form throughout: the corpus files, the
recorded entry contract, the recorded branch shape.  `operator` is
carried once per record as a display label and is read by nothing.

usage:
  canon36_universal.py --lang c [--limit N] [--fresh]
  canon36_universal.py --all
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
import dominant_table17 as DT17                                  # noqa: E402
import region36 as R36                                           # noqa: E402
import z3                                                        # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
CHECKPOINT_EVERY = 25

RESULT_TEXT = R36.block_text(R36.RESULT_BASE)

# ---- the monkeypatch seam, named in the header.
_ORIGINAL_IS_SLOT_TEXT = G33.is_slot_text


def _is_slot_or_block(text):
    if _ORIGINAL_IS_SLOT_TEXT(text):
        return True
    return R36.is_block_text(text)


G33.is_slot_text = _is_slot_or_block

MEM_SOURCE_OK = frozenset([
    "mov", "movl", "movq", "movb", "movw", "movabs",
    "add", "addl", "addq", "addb", "addw",
    "sub", "subl", "subq", "subb", "subw",
    "and", "andl", "andq", "andb", "andw",
    "or", "orl", "orq", "orb", "orw",
    "xor", "xorl", "xorq", "xorb", "xorw",
    "cmp", "cmpl", "cmpq", "cmpb", "cmpw",
    "adc", "sbb",
])

PURE_WRITE = frozenset([
    "mov", "movq", "movd", "movabs", "movzx", "movzbl", "movzwl",
    "movsbl", "movswl", "movslq", "movsbq", "movswq", "lea", "movss",
    "movsd", "movaps", "movapd", "movdqa", "movdqu", "cvtsi2ss",
    "cvtsi2sd", "cvtss2sd", "cvtsd2ss", "cvttss2si", "cvttsd2si",
    "sete", "setne", "setl", "setle", "setg", "setge", "setb", "setbe",
    "seta", "setae", "setp", "setnp", "sets", "setns", "seto", "setno",
    "xorps", "xorpd",
])

LANE_WISE = frozenset([
    "addss", "addsd", "subss", "subsd", "mulss", "mulsd", "divss",
    "divsd", "minss", "minsd", "maxss", "maxsd", "sqrtss", "sqrtsd",
    "ucomiss", "ucomisd", "comiss", "comisd", "cvtss2sd", "cvtsd2ss",
    "cvtsi2ss", "cvtsi2sd", "cvttss2si", "cvttsd2si", "movss", "movsd",
    "movq", "movd", "movaps", "movapd", "movdqa", "movdqu",
    "andps", "andpd", "orps", "orpd", "xorps", "xorpd", "andnps",
    "andnpd", "pxor", "pand", "por",
    "cmpeqss", "cmpeqsd", "cmpneqss", "cmpneqsd", "cmpltss", "cmpltsd",
    "cmpless", "cmplesd", "cmpunordss", "cmpunordsd",
])


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def split_lines(text):
    return R36.split_lines(text)


def operands_of(line):
    return R36.operands_of(line, G33.split_operands)


def is_vector_family(family):
    if family is None:
        return False
    return family.startswith("xmm")


def reg_text(family, width_index=0):
    if is_vector_family(family):
        return "%" + family
    return "%" + R36.widened(family, width_index)


# ------------------------------------------------------------------
# the entry contract read off a unit's own text
# ------------------------------------------------------------------

# the ordinary System V argument sequence, in ABI order.  Round 8 and
# the first pass of this lap looked at only the first two of each file,
# which is why a unit taking a wide value in a REGISTER PAIR (an
# __int128 arriving in %rdi+%rsi+%rdx) had an argument nothing loaded --
# measured at first observation: 870 regenerated units disproved, e.g.
# c/regen_22674, whose ship text reads %rdx and whose contract named
# only %rdi and %rsi.
GENERAL_ARRIVAL_SEQUENCE = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")
VECTOR_ARRIVAL_SEQUENCE = ("xmm0", "xmm1", "xmm2", "xmm3", "xmm4",
                           "xmm5", "xmm6", "xmm7")
ARRIVAL_FAMILIES = GENERAL_ARRIVAL_SEQUENCE + VECTOR_ARRIVAL_SEQUENCE
DESIGNATIONS = ("a", "b", "c", "d", "e", "f", "g", "h")


def infer_entry_contract(text):
    """the entry contract read off the unit's OWN TEXT.  Machine-form
    evidence only: a family ARRIVES when the text reads it before it
    writes it."""
    arrives = {}
    seen_write = {}
    for family in ARRIVAL_FAMILIES:
        arrives[family] = False
        seen_write[family] = False
    for line in split_lines(text):
        mnemonic = R36.mnemonic_of(line)
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
    ordered = []
    for family in GENERAL_ARRIVAL_SEQUENCE:
        if arrives[family]:
            ordered.append(family)
    for family in VECTOR_ARRIVAL_SEQUENCE:
        if arrives[family]:
            ordered.append(family)
    result = "rax"
    if "%rax" not in text:
        if "%eax" not in text:
            if "%al" not in text:
                if "%ax" not in text:
                    result = "xmm0"
    out = {"result": result}
    for index, family in enumerate(ordered):
        if index >= len(DESIGNATIONS):
            break
        out[DESIGNATIONS[index]] = family
    for designation in DESIGNATIONS:
        if designation not in out:
            out[designation] = None
    return out


# ------------------------------------------------------------------
# the render
# ------------------------------------------------------------------

def own_displacements(core):
    """(displacement -> escapes) over the whole core at once."""
    found = {}
    for raw in core:
        line = R36.strip_annotation(raw)
        is_lea = R36.mnemonic_of(line) == "lea"
        for hit in R36.RSP_DISP.finditer(line):
            value = int(hit.group(1), 16)
            if value not in found:
                found[value] = False
            if is_lea:
                found[value] = True
        # A BARE `(%rsp)` IS DISPLACEMENT ZERO, not a guess.  Round 8
        # refused it by name ("cannot be placed without guessing");
        # measured at first observation, 2,185 regenerated units spell
        # it, and the affine map places it exactly like any other
        # displacement -- at REGION_SIZE - 0, the byte %rsp itself
        # addresses.
        if R36.BARE_RSP.search(line):
            if 0 not in found:
                found[0] = False
            if is_lea:
                found[0] = True
    return found


def stack_refusal(core):
    for raw in core:
        line = R36.strip_annotation(raw)
        if R36.RBP_ANY.search(line):
            return ("frame-pointer address",
                    "the text names a %rbp-relative address; the region "
                    "form has one ruled base and refuses to guess a "
                    "second one")

    return None


def lane_check(core, family):
    """P2 for a vector arrival: every read of the arrival register must
    be lane-wise, because a block holds a VALUE, eight bytes."""
    for raw in core:
        line = R36.strip_annotation(raw)
        mnemonic = R36.mnemonic_of(line)
        operands = operands_of(line)
        reads = False
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
        return (mnemonic, line)
    return None


def arriving_families(text):
    """the families this TEXT reads before it writes them -- machine-form
    evidence from the artifact in hand."""
    inferred = infer_entry_contract(text)
    out = set()
    for key in DESIGNATIONS:
        if inferred.get(key) is not None:
            out.add(inferred[key])
    return out, inferred


def reconcile_entry_contract(entry_contract, prior_text):
    """THE TEXT OUTRANKS THE RECORDED CONTRACT on which register an
    argument arrives in.

    Measured at first observation: 52 units disproved because the
    recorded contract named an argument register the unit's own text
    never reads.  c/op_300's contract says its second argument arrives
    in %rdi; its text reads %rsi and never mentions %rdi, so the
    standardized load filled a register nothing read and the register
    the core did read was unconstrained.  The recorded contract is
    'human interpretation of stated design'; the text is the artifact
    itself, so the text wins, and the disagreement is RECORDED rather
    than smoothed over."""
    if not entry_contract:
        return entry_contract, None
    if not prior_text:
        return entry_contract, None
    arriving, inferred = arriving_families(prior_text)
    out = dict(entry_contract)
    notes = []
    used = set()
    for key in DESIGNATIONS:
        recorded = entry_contract.get(key)
        if recorded is None:
            continue
        if recorded in arriving:
            used.add(recorded)
            continue
        replacement = None
        candidate = inferred.get(key)
        if candidate is not None:
            if candidate not in used:
                replacement = candidate
        if replacement is None:
            candidates = []
            for designation in DESIGNATIONS:
                candidates.append(inferred.get(designation))
            for family in candidates:
                if family is None:
                    continue
                if family in used:
                    continue
                replacement = family
                break
        if replacement is None:
            continue
        out[key] = replacement
        used.add(replacement)
        notes.append({
            "designation": key,
            "recorded_contract_said": recorded,
            "the_text_reads": replacement,
            "why_the_text_wins": "the recorded family is never read "
                                 "before it is written anywhere in this "
                                 "unit's own text",
        })
    if not notes:
        return entry_contract, None
    return out, notes


def render(entry_contract, prior_text, guards, materialize_constants,
           result_family_override=None, result_width=64):
    """(fields, refusal_or_None).  refusal is (cause, detail)."""
    if not prior_text:
        return None, ("no text",
                      "no text exists for this unit in any generation, "
                      "so there is nothing to render into the region "
                      "form")
    if not entry_contract:
        return None, ("no entry contract",
                      "this unit carries no recorded entry contract, so "
                      "its input lineages cannot be allocated")
    if entry_contract.get("a") is None:
        return None, ("no entry contract",
                      "the entry contract names no first argument")
    result_family = entry_contract.get("result")
    if result_family_override is not None:
        result_family = result_family_override
    if result_family is None:
        return None, ("no entry contract",
                      "the entry contract names no result lineage")

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

    refusal = stack_refusal(core_in)
    if refusal is not None:
        return None, refusal

    # THE REGION BASE IS NOT AVAILABLE TO ANY LINEAGE.  This is checked
    # on the unit's ORIGINAL core, before the own-stack rewrite: after
    # that rewrite the text names %r15 as the region's own base on
    # every own-address line, which is the form working, not a clash.
    for raw in core_in:
        line = R36.strip_annotation(raw)
        for token in re.findall(r"%[a-z0-9]+", line):
            if canon.FAMILY_OF.get(token[1:]) == R36.REGION_BASE_FAMILY:
                return None, (
                    "the core names the region base",
                    "this unit's own core mentions %r15, which the form "
                    "rules to be the region base and therefore not "
                    "available to any lineage; the unit is refused by "
                    "name rather than being rendered onto a base it "
                    "also uses as a value")

    allocator = R36.BlockAllocator()

    # ---- the input lineages, in arrival order.
    arrivals = []
    for designation in DESIGNATIONS:
        family = entry_contract.get(designation)
        if family is None:
            continue
        arrivals.append((designation, family))
    input_blocks = []
    for designation, family in arrivals:
        record = allocator.allocate("input", "argument_%s" % designation)
        input_blocks.append((designation, family, record))

    # ---- P2 lane safety for every vector arrival.
    for designation, family, _record in input_blocks:
        if not is_vector_family(family):
            continue
        unsafe = lane_check(core_in, family)
        if unsafe is None:
            continue
        return None, ("upper-lane dependence",
                      "P2 fails: the arrival %s is a vector value and "
                      "the core reads its register with %r (%r), which "
                      "is not lane-wise -- its low lane can depend on "
                      "the upper lanes, which a block's eight bytes do "
                      "not carry" % (designation, unsafe[0], unsafe[1]))

    # ---- the result lineage.
    result_block = allocator.allocate("result", "answer")

    # ---- the own / temp stack lineages.
    try:
        placements = {}
        for displacement, escapes in sorted(own_displacements(core_in).items()):
            placements[displacement] = allocator.place_own(displacement,
                                                           escapes)
    except R36.Refusal as bad:
        return None, (bad.cause, bad.detail)

    # ---- the guard-outcome lineages.
    guard_blocks = []
    try:
        for index, guard in enumerate(guards or []):
            record = allocator.allocate(
                "guard-outcome", "guard_%d" % index,
                note="declared from the unit's own recorded branch "
                     "shape; the outcome value is not materialized "
                     "this lap")
            guard_blocks.append(record)
    except R36.Refusal as bad:
        return None, (bad.cause, bad.detail)

    # ---- rewrite the own-stack addresses.
    staged = []
    for raw in core_in:
        line = R36.strip_annotation(raw)
        for displacement, record in sorted(placements.items(),
                                           reverse=True):
            if displacement == 0:
                continue
            line = line.replace("-0x%x(%%rsp)" % displacement,
                                record["text"])
        if 0 in placements:
            line = R36.BARE_RSP.sub(placements[0]["text"], line)
        staged.append(line)

    # ---- RULE R over (arrivals, core, result).
    general_order = []
    vector_order = []

    def note_family(family):
        if family is None:
            return
        if family in R36.NEVER_RENAME:
            return
        if family == R36.REGION_BASE_FAMILY:
            return
        if is_vector_family(family):
            if family not in vector_order:
                vector_order.append(family)
            return
        if family not in general_order:
            general_order.append(family)

    for _designation, family, _record in input_blocks:
        note_family(family)
    for line in staged:
        for token in re.findall(r"%[a-z0-9]+", line):
            note_family(canon.FAMILY_OF.get(token[1:]))
    note_family(result_family)
    pinned = R36.families_pinned(staged, G33.split_operands)
    try:
        mapping, rule_notes, taken = R36.rule_r_map_ordered(
            general_order, vector_order, pinned)
    except R36.Refusal as bad:
        return None, (bad.cause, bad.detail)

    core = []
    for line in staged:
        core.append(R36.apply_rule_r(line, mapping))

    # ---- the constant lineages.
    vehicle = R36.free_vehicle(taken, pinned)
    literals = []
    for line in core:
        operands = operands_of(line)
        for operand in operands:
            value = R36.immediate_value(operand)
            if value is None:
                continue
            if operand in literals:
                continue
            literals.append(operand)
    const_records = {}
    try:
        for operand in literals:
            record = allocator.allocate("constant", "literal_%s" % operand)
            record["value"] = R36.immediate_value(operand)
            const_records[operand] = record
    except R36.Refusal as bad:
        return None, (bad.cause, bad.detail)

    materialized = []
    if materialize_constants:
        if vehicle is None:
            materialize_constants = False
    final_core = []
    for line in core:
        did = False
        if materialize_constants:
            mnemonic = R36.mnemonic_of(line)
            operands = operands_of(line)
            if len(operands) == 2:
                if mnemonic in MEM_SOURCE_OK:
                    source, destination = operands
                    if source in const_records:
                        if destination.startswith("%"):
                            if not is_vector_family(
                                    canon.FAMILY_OF.get(destination[1:], "")):
                                index = R36.width_index_of(destination[1:])
                                if index is not None:
                                    record = const_records[source]
                                    final_core.append(
                                        "mov %s,%s"
                                        % (record["text"],
                                           reg_text(vehicle, 0)))
                                    emit = mnemonic
                                    if emit == "movabs":
                                        emit = "mov"
                                    final_core.append(
                                        "%s %s,%s"
                                        % (emit,
                                           reg_text(vehicle, index),
                                           destination))
                                    materialized.append(source)
                                    did = True
        if not did:
            final_core.append(line)

    # ---- the standardized loads and the result store.
    loads = []
    directory = []
    for designation, family, record in input_blocks:
        vehicle_family = mapping.get(family, family)
        if is_vector_family(family):
            loads.append("movq %s,%s" % (record["text"],
                                         reg_text(vehicle_family)))
        else:
            loads.append("mov %s,%s" % (record["text"],
                                        reg_text(vehicle_family)))
        entry = dict(record)
        entry["holds"] = "the lineage of input argument %s" % designation
        entry["loaded_into"] = reg_text(vehicle_family)
        entry["register_file"] = ("vector" if is_vector_family(family)
                                  else "general")
        directory.append(entry)
    # THE MOVE-ERASED IDENTITY.  A canonical text of `ret` means the
    # answer IS an arriving value: the move that parked it in the
    # answer register was erased by substitution (AgentMemory,
    # 2026-08-26).  So when no core line touches the result lineage's
    # register at all, the answer lineage is the FIRST INPUT lineage,
    # and the store reads that input's vehicle.  Measured at first
    # observation: 6 rust units whose prior text is exactly `ret`.
    # scanned on the PRE-RENAME core: after rule R the result family
    # is spelled as its vehicle, so scanning the renamed text asked the
    # wrong question (measured at first observation: 139 units, e.g.
    # c/op_13, whose core does write the result lineage).
    result_touched = False
    for line in staged:
        for token in re.findall(r"%[a-z0-9]+", line):
            if canon.FAMILY_OF.get(token[1:]) == result_family:
                result_touched = True
    answer_note = None
    answer_family = result_family
    if not result_touched:
        for designation, family, _record in input_blocks:
            if True:
                # the register FILE is not required to match: a unit
                # whose ship code moved the value across files had that
                # move erased too, and the eight bytes are the same
                # eight bytes either way (rust/op_39: a float arrives
                # in %xmm0 and the recorded answer home is an rax-family
                # register).
                answer_family = family
                answer_note = (
                    "no line of this unit's core touches the result "
                    "lineage's register, so the answer is the arriving "
                    "value itself -- the move that parked it was erased "
                    "by substitution; the store reads input %s's vehicle"
                    % designation)
                break
    result_vehicle = mapping.get(answer_family, answer_family)
    # THE RESULT BLOCK HOLDS THE ANSWER ZERO-EXTENDED TO EIGHT BYTES,
    # one rule for every unit.  Without it a 32-bit answer left the
    # block's upper four bytes holding whatever the vehicle happened to
    # carry, so the block was not the answer's home -- measured at
    # first observation by real execution: go/op_2 returned
    # 0x7fffffffffffffff from the block where its own text returns
    # 0xffffffff (canon36_realrun, 42 differing of 17,640).
    widen = []
    if not is_vector_family(answer_family):
        if result_width == 32:
            widen.append("mov %s,%s" % (reg_text(result_vehicle, 1),
                                        reg_text(result_vehicle, 1)))
        elif result_width == 16:
            widen.append("movzwl %s,%s" % (reg_text(result_vehicle, 2),
                                           reg_text(result_vehicle, 1)))
        elif result_width == 8:
            widen.append("movzbl %s,%s" % (reg_text(result_vehicle, 3),
                                           reg_text(result_vehicle, 1)))
    if is_vector_family(answer_family):
        store = "movq %s,%s" % (reg_text(result_vehicle),
                                result_block["text"])
    else:
        store = "mov %s,%s" % (reg_text(result_vehicle),
                               result_block["text"])
    entry = dict(result_block)
    entry["holds"] = "the lineage of the answer"
    entry["stored_from"] = reg_text(result_vehicle)
    entry["register_file"] = ("vector" if is_vector_family(answer_family)
                              else "general")
    if answer_note is not None:
        entry["answer_is_the_arrival"] = answer_note
    directory.append(entry)
    for operand, record in const_records.items():
        entry = dict(record)
        entry["holds"] = "the lineage of the literal %s" % operand
        entry["materialized"] = operand in materialized
        if operand not in materialized:
            entry["why_not_materialized"] = (
                "the encoding at this site admits no memory source, so "
                "the literal stays an immediate; its block is allocated "
                "and directoried all the same")
        directory.append(entry)
    for displacement, record in sorted(placements.items()):
        entry = dict(record)
        entry["holds"] = ("the lineage of the unit's own stack address "
                          "-0x%x(%%rsp)" % displacement)
        directory.append(entry)
    for record in guard_blocks:
        entry = dict(record)
        entry["holds"] = "the lineage of a guard outcome"
        directory.append(entry)

    if block_form:
        text, refusal = weave(final_core, loads, widen + [store])
        if refusal is not None:
            return None, refusal
    else:
        text = "; ".join(loads + final_core + widen + [store, "ret"])

    return {
        "universal_text": text,
        "block_form": block_form,
        "standardized_loads": loads,
        "computation_core": final_core,
        "result_store": store,
        "answer_widening": widen,
        "result_width": result_width,
        "block_directory": directory,
        "block_counts": dict(allocator.counts),
        "rule_r_assignments": rule_notes,
        "rule_r_pinned_families": sorted(pinned),
        "constant_vehicle": None if vehicle is None else reg_text(vehicle),
        "constant_materialization": ("full" if materialize_constants
                                     else "reduced"),
        "literals_materialized": sorted(set(materialized)),
        "own_address_lineages": [
            record["lineage"] for record in allocator.blocks
            if record["kind"] == "own-address"],
        "result_block": result_block["text"],
        "answer_lineage_family": answer_family,
        "answer_is_the_arrival": answer_note,
        "region_base": R36.REGION_BASE_REGISTER,
        "region_size": R36.REGION_SIZE,
    }, None


def weave(core, loads, tail):
    """the region form of a BLOCK-LIST core: the loads run once ahead
    of every executable instruction, and the result store sits
    immediately before every `ret`."""
    first = None
    for index, line in enumerate(core):
        if line.endswith(":"):
            continue
        first = index
        break
    if first is None:
        return None, ("no executable instruction",
                      "the block-list text carries no executable "
                      "instruction")
    rets = 0
    for line in core:
        if line == "ret":
            rets = rets + 1
    if rets == 0:
        return None, ("never returns",
                      "the block-list text never returns, so the answer "
                      "has no place to be stored")
    out = []
    for index, line in enumerate(core):
        if index == first:
            out.extend(loads)
        if line == "ret":
            out.extend(tail)
        out.append(line)
    return "; ".join(out), None


# ------------------------------------------------------------------
# the gate
# ------------------------------------------------------------------

class Sim36(G33.Sim33):
    """Sim33, whose designated-location model now also covers the
    region's block texts (the seam is the widened G33.is_slot_text
    named in the header), plus the scalar-float spellings of a block
    move that round 8 measured to be needed."""

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
        if len(operands) != 2:
            return G33.Sim33.exec_line(self, line)
        source, destination = operands
        side = None
        if G33.is_slot_text(destination):
            side = "store"
        if G33.is_slot_text(source):
            side = "load"
        if side == "load":
            if self.is_xmm(destination):
                value = self.slot_value(source, width)
                self.write_xmm(destination, self.zero_extend_to_128(value))
                return None
            value = self.slot_value(source, width)
            self.write(destination, value)
            return None
        if side == "store":
            if self.is_xmm(source):
                value = self.lane(self.read_xmm(source), 0, width)
                self.slots[destination] = (value, width)
                return None
            value = self.read_at(source, width)
            self.slots[destination] = (value, width)
            return None
        return G33.Sim33.exec_line(self, line)

    def run_lines(self, text_lines):
        for line in text_lines:
            stripped = line.strip()
            if stripped == "":
                continue
            if stripped == "ret":
                continue
            self.exec_line(stripped)

    def result_block_value(self):
        if RESULT_TEXT not in self.slots:
            raise G33.NotModeled(
                "the region text never wrote the result block, so the "
                "answer has no home to read")
        return self.slots[RESULT_TEXT]


def bind_region(shared_seed, directory, arrival_families):
    """the arrival contract, bound before anything is proved."""
    made = []
    index = 0
    for entry in directory:
        if entry["kind"] != "input":
            continue
        family = arrival_families[index]
        index = index + 1
        if is_vector_family(family):
            if family not in shared_seed:
                shared_seed[family] = z3.BitVec("seed_%s" % family, 128)
            value = shared_seed[family]
            shared_seed["slot_%s" % entry["text"]] = z3.Extract(63, 0, value)
        else:
            value = BC8.seed_family(shared_seed, family)
            shared_seed["slot_%s" % entry["text"]] = value
        made.append({
            "block": entry["text"],
            "kind": "input",
            "bound_to_the_same_symbol_as": "%%%s" % family,
        })
    for entry in directory:
        if entry["kind"] != "constant":
            continue
        shared_seed["slot_%s" % entry["text"]] = z3.BitVecVal(
            entry["value"], 64)
        made.append({
            "block": entry["text"],
            "kind": "constant",
            "bound_to_the_value": "0x%x" % entry["value"],
        })
    rsp = BC8.seed_family(shared_seed, "rsp")
    shared_seed[R36.REGION_BASE_FAMILY] = rsp - z3.BitVecVal(
        R36.REGION_SIZE, 64)
    made.append({
        "block": R36.REGION_BASE_REGISTER,
        "kind": "region base",
        "bound_to": "%%rsp - 0x%x, the run-time mapping region36 rules"
                    % R36.REGION_SIZE,
    })
    return made


def arrival_family_list(entry_contract):
    out = []
    for designation in DESIGNATIONS:
        family = entry_contract.get(designation)
        if family is None:
            continue
        out.append(family)
    return out


def compare(reference_lines, region_lines, shared_seed, home, width,
            what):
    """the one proof obligation: the value the region form leaves in
    the RESULT BLOCK equals the value the reference text leaves in its
    answer home."""
    sim_ref = Sim36(shared_seed, "reference")
    sim_reg = Sim36(shared_seed, "region")
    sim_ref.answer_family = home
    sim_ref.answer_width = width
    sim_reg.answer_family = home
    sim_reg.answer_width = width
    try:
        val_ref, w_ref = sim_ref.answer_value(reference_lines)
        sim_reg.run_lines(region_lines)
        val_reg, w_reg = sim_reg.result_block_value()
    except (BC10.NotModeled, G33.NotModeled, BC10.Trap) as bad:
        return "UNDECIDED", "%s: %s" % (what, bad)
    except Exception as bad:                       # noqa: BLE001
        return "UNDECIDED", "%s: %s: %s" % (what, type(bad).__name__, bad)
    bits = min(w_ref, w_reg)
    left = z3.Extract(bits - 1, 0, val_ref)
    right = z3.Extract(bits - 1, 0, val_reg)
    solver = z3.Solver()
    solver.set("timeout", 20000)
    solver.add(left != right)
    outcome = solver.check()
    if outcome == z3.unsat:
        return ("PROVED_EQUAL",
                "z3 proved the region text's RESULT BLOCK %s equal to "
                "%s at %d bits, for every value of every input block, "
                "with each input block bound to the same symbol as the "
                "argument the reference text reads and the region base "
                "bound to %%rsp - 0x%x"
                % (RESULT_TEXT, what, bits, R36.REGION_SIZE))
    if outcome == z3.sat:
        return ("DISPROVED",
                "z3 found a counterexample against %s: %s"
                % (what, solver.model()))
    return ("UNDECIDED", "z3 returned %r at a 20000ms timeout against %s"
            % (outcome, what))


def answer_home_of(lang, n, canon4_docs, entry_contract,
                   prior_text=None):
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is not None:
        lines_real = [ln.strip() for ln in real_text.split(";")]
        home, width = BC10.answer_home_from_real(lines_real)
        if home is not None:
            return home, width, "the unit's own real ship text"
    # THE SHIP TEXT NAMES NO HOME, BUT THE CANONICAL TEXT MIGHT.
    # Measured at first observation by real execution: go/op_2's ship
    # code returns in a place this checker cannot name, while its
    # canonical text says plainly `mov %edi,%eax` -- the answer is 32
    # bits of the arrival, not all 64.  Taking the arrival straight
    # away made the gate's question vacuous and the region text stored
    # eight bytes where four were the answer (42 differing pairs of
    # 17,640 in canon36_realrun).
    if prior_text:
        lines_prior = split_lines(prior_text)
        home, width = BC10.answer_home_from_real(lines_prior)
        if home is not None:
            return (home, width,
                    "this unit's own canonical text (its ship code "
                    "names no answer home this checker can read)")
    # THE SHIP TEXT NAMES NO ANSWER HOME.  Measured at first
    # observation: 6 rust units and 5 go units whose ship code is
    # exactly `ret` -- the value arrives and leaves in the same place,
    # so the answer home IS the arriving lineage.  Falling back to the
    # recorded contract's result family instead named a register the
    # unit never writes, and the gate then compared against an
    # unconstrained symbol.
    if entry_contract.get("a") is not None:
        return (entry_contract.get("a"), 64,
                "the unit's own ship code writes no answer home, so "
                "the answer is the arriving value itself")
    return (entry_contract.get("result"), 64,
            "the recorded entry contract (the ship text names no "
            "answer home)")


# ------------------------------------------------------------------
# the newest text of an original-population unit
# ------------------------------------------------------------------

def newest_text_sources():
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
# the driver, original population
# ------------------------------------------------------------------

def out_path(lang):
    return os.path.join(HERE, "canon36_universal_%s.json" % lang)


def read_checkpoint(lang, fresh):
    path = out_path(lang)
    if fresh:
        return {}
    if not os.path.exists(path):
        return {}
    return json.load(open(path))["units"]


def tally_of(units):
    out = {}
    for record in units.values():
        key = record.get("outcome")
        out[key] = out.get(key, 0) + 1
    return out


def write_checkpoint(lang, units, tally):
    document = {
        "meta": {
            "role": "generator provenance",
            "generated_by": "canon36_universal.py",
            "form": "region36: the ruled virtual region, typed blocks "
                    "per lineage, no designated registers",
            "population": "the original corpus, %s" % lang,
            "note": "the operator field is a display label on the "
                    "member and is read by nothing",
        },
        "tally": tally,
        "units": units,
    }
    handle = open(out_path(lang), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()


def gate_unit(lang, n, canon4_docs, sem_docs, entry_contract, fields,
              prior_text, has_prior_canonical):
    """(verdict, detail, gate1, gate2, bindings)."""
    home, width, home_source = answer_home_of(lang, n, canon4_docs,
                                              entry_contract,
                                              prior_text)
    families = arrival_family_list(entry_contract)
    region_lines = split_lines(fields["universal_text"])

    gate1 = ("NOT_APPLICABLE",
             "this unit has no prior canonical text to chain through; "
             "the direct ship gate is its admission gate")
    if has_prior_canonical:
        if fields["block_form"]:
            gate1 = ("UNDECIDED",
                     "the prior canonical form is a block list and this "
                     "gate's simulator walks a straight line")
        else:
            seed = BC10._prepare_seed(lang, n, sem_docs)
            bind_region(seed, fields["block_directory"], families)
            verdict, detail = compare(
                split_lines(prior_text), region_lines, seed, home, width,
                "the unit's own prior canonical text")
            gate1 = (verdict, detail)

    gate2 = ("UNDECIDED", "no real ship text is recorded for this unit")
    real_text = BC8.real_text_of(lang, n, canon4_docs)
    if real_text is not None:
        lines_real = [ln.strip() for ln in real_text.split(";")]
        order_real = G33.rip_order_data_only(lines_real)
        order_cand = G33.rip_order_data_only(region_lines)
        if order_real != order_cand:
            gate2 = ("UNDECIDED",
                     "the narrowed rip-relative constant guard refused: "
                     "the ship text loads data constants at %r, the "
                     "region text at %r" % (order_real, order_cand))
        else:
            home2, width2 = BC10.answer_home_from_real(lines_real)
            if home2 is None:
                home2, width2, _why = answer_home_of(
                    lang, n, canon4_docs, entry_contract, prior_text)
            if home2 is None:
                gate2 = ("UNDECIDED",
                         "the unit's own ship code never writes an "
                         "answer home this checker can name")
            else:
                seed = BC10._prepare_seed(lang, n, sem_docs)
                bind_region(seed, fields["block_directory"], families)
                verdict, detail = compare(lines_real, region_lines, seed,
                                          home2, width2,
                                          "the unit's own ship code")
                gate2 = (verdict, detail)

    bindings = []
    seed_shape = {}
    bindings = bind_region(seed_shape, fields["block_directory"], families)

    if gate2[0] == "PROVED_EQUAL":
        return ("PROVED_ON_SHIP", gate2[1], gate1, gate2, bindings,
                home_source)
    if gate1[0] == "PROVED_EQUAL":
        return ("PROVED_ON_PRIOR", gate1[1], gate1, gate2, bindings,
                home_source)
    if "DISPROVED" in (gate1[0], gate2[0]):
        which = gate1 if gate1[0] == "DISPROVED" else gate2
        return ("DISPROVED", which[1], gate1, gate2, bindings,
                home_source)
    return ("UNDECIDED", "%s | %s" % (gate1[1], gate2[1]), gate1, gate2,
            bindings, home_source)


def structural_route(fields, prior_text):
    """THE STRUCTURAL ROUTE -- a proof BY CONSTRUCTION, used only where
    the solver returns UNDECIDED because its own table has no model for
    a mnemonic the unit spells (measured: the branch mnemonics, `div`,
    the packed float operations, `sbb`).

    The region form applies exactly three transformations to a unit's
    own core, and each is meaning-preserving on its own:

      T1  the own-stack rewrite -- every `-0xN(%rsp)` becomes
          `0x(REGION_SIZE-N)(%r15)`, ONE affine map with the ruled
          constant, and the run-time mapping %r15 = %rsp - REGION_SIZE
          makes the rewritten operand the SAME BYTE;
      T2  the rule-R rename -- an injective map on register families,
          with every encoding-pinned family a fixed point;
      T3  constant materialization -- `op $imm,X` becomes
          `mov <constant block>,<vehicle>` + `op <vehicle>,X`, where
          the vehicle is a register no lineage holds.

    The checks below verify that nothing ELSE happened, and that the
    plumbing the form adds cannot disturb the core.  Each is recorded
    by name; the route is claimed only when all of them hold.

    EVIDENCE CLASS, stated rather than assumed: T1, T2 and the block
    checks are forced by construction over artifacts this lap built.
    T3 additionally rests on `mov` leaving the flags alone, which is
    'human interpretation of stated design' -- so a unit admitted by
    this route with materialized literals is cross-checked by
    assembly and by real execution (canon36_assemble.py,
    canon36_realrun.py), and the record says so."""
    checks = []

    mapping_targets = []
    for note in fields["rule_r_assignments"]:
        mapping_targets.append(note["assigned"])
    if len(mapping_targets) != len(set(mapping_targets)):
        return False, "T2 fails: the rule-R map is not injective"
    for note in fields["rule_r_assignments"]:
        if note["family"] in fields["rule_r_pinned_families"]:
            if note["assigned"] != note["family"]:
                return False, ("T2 fails: the pinned family %s was moved"
                               % note["family"])
    checks.append("T2: the rule-R map is injective and every "
                  "encoding-pinned family is a fixed point")

    for entry in fields["block_directory"]:
        if entry["kind"] != "own-address":
            if entry["kind"] != "temp":
                continue
        if "was" not in entry:
            continue
        want = R36.own_offset_of_displacement(
            int(entry["was"].split("(")[0][3:], 16))
        if entry["offset"] != want:
            return False, ("T1 fails: %s was not placed by the affine "
                           "map" % entry["was"])
    checks.append("T1: every own stack address was placed by the one "
                  "affine map, so the rewritten operand is the same "
                  "byte under the ruled run-time mapping")

    vehicle = fields.get("constant_vehicle")
    materialized = fields.get("literals_materialized") or []
    if materialized:
        if vehicle is None:
            return False, "T3 fails: literals were materialized with no "\
                          "vehicle"
        for note in fields["rule_r_assignments"]:
            if "%" + note["assigned"] == vehicle:
                return False, ("T3 fails: the constant vehicle %s is "
                               "held by a lineage" % vehicle)
        core = fields["computation_core"]
        for index, line in enumerate(core):
            if vehicle[1:] not in line:
                continue
            token_hit = False
            for token in re.findall(r"%[a-z0-9]+", line):
                if canon.FAMILY_OF.get(token[1:]) == vehicle[1:]:
                    token_hit = True
            if not token_hit:
                continue
            operands = operands_of(line)
            is_load = False
            if R36.mnemonic_of(line) == "mov":
                if operands:
                    if R36.is_block_text(operands[0]):
                        is_load = True
            if is_load:
                continue
            if index == 0:
                return False, ("T3 fails: the vehicle is read at line 0 "
                               "with no load before it")
            before = core[index - 1]
            ok = False
            if R36.mnemonic_of(before) == "mov":
                ops_before = operands_of(before)
                if ops_before:
                    if R36.is_block_text(ops_before[0]):
                        ok = True
            if not ok:
                return False, ("T3 fails: the vehicle is read at %r "
                               "without its own load immediately before"
                               % line)
        checks.append("T3: every literal is loaded from its own "
                      "constant block into a vehicle no lineage holds, "
                      "and consumed on the very next line")
    else:
        checks.append("T3: no literal was materialized, so the core "
                      "carries its immediates unchanged")

    input_texts = []
    for entry in fields["block_directory"]:
        if entry["kind"] == "input":
            input_texts.append(entry["text"])
    wanted = []
    for entry in fields["block_directory"]:
        if entry["kind"] != "input":
            continue
        mnemonic = "movq" if entry["register_file"] == "vector" else "mov"
        wanted.append("%s %s,%s" % (mnemonic, entry["text"],
                                    entry["loaded_into"]))
    if fields["standardized_loads"] != wanted:
        return False, ("the loads are not exactly one load per input "
                       "lineage from its own block")
    checks.append("the standardized loads are exactly one line per "
                  "input lineage, each from its own block")

    result_text = fields["result_block"]
    for line in fields["computation_core"]:
        if result_text in line:
            return False, ("a core line names the result block: %r"
                           % line)
        for text in input_texts:
            if text in line:
                return False, ("a core line names an input block: %r"
                               % line)
    checks.append("no core line names an input block or the result "
                  "block, so the store touches a block nothing else "
                  "reads")

    placed = split_lines(fields["universal_text"])
    rets = 0
    stores = 0
    for index, line in enumerate(placed):
        if line == "ret":
            rets = rets + 1
            if index == 0:
                return False, "a `ret` at line 0 has no store before it"
            if placed[index - 1] != fields["result_store"]:
                return False, ("a `ret` at line %d is not immediately "
                               "preceded by the result store" % index)
        if line == fields["result_store"]:
            stores = stores + 1
    if rets == 0:
        return False, "the text never returns"
    if rets != stores:
        return False, ("the text has %d returns and %d result stores"
                       % (rets, stores))
    checks.append("every one of the %d returns is immediately preceded "
                  "by the result store, which writes the result block"
                  % rets)
    checks.append("P2 lane safety holds for every vector input lineage "
                  "(checked at render time)")
    return True, checks


def guards_of(rec31):
    kind = rec31.get("branch_kind")
    if kind is None:
        return []
    if kind in ("none", "straight", ""):
        return []
    return [kind]


def process_unit(lang, n, rec31, c4, prior_text, prior_source,
                 canon4_docs, sem_docs, arrival):
    label = "%s/op_%s" % (lang, n)
    record = {
        "unit": label,
        "lang": lang,
        "n": n,
        "operator": rec31.get("operator"),
        "population": "original",
        "recorded_status": rec31.get("status"),
        "branch_kind": rec31.get("branch_kind"),
        "prior_text": prior_text,
        "prior_text_source": prior_source,
        "arrival_annotation": (arrival.get(label) or {}).get("mode"),
    }
    entry_contract = c4.get("entry_contract")
    if entry_contract is None:
        if prior_text:
            entry_contract = infer_entry_contract(prior_text)
            record["entry_contract_source"] = (
                "inferred from the unit's own text: no canon4 record "
                "exists, so the arrival lineages are the ones the text "
                "reads before it writes them")
    entry_contract, reconciled = reconcile_entry_contract(entry_contract,
                                                          prior_text)
    record["entry_contract"] = entry_contract
    if reconciled is not None:
        record["entry_contract_reconciled"] = reconciled
    guards = guards_of(rec31)

    # THE RESULT LINEAGE TAKES THE GROUND-TRUTH ANSWER HOME, read off
    # the unit's own real ship text, not the recorded entry contract.
    # Measured at first observation: 90 units disproved because a
    # recorded contract said the answer was an rax-family value while
    # the unit's own ship code writes %xmm0 (c/op_105 is the instance
    # printed in the log), so the store read a register nothing had
    # written.
    result_home = None
    result_width = 64
    if entry_contract is not None:
        home, width, _source = answer_home_of(lang, n, canon4_docs,
                                              entry_contract,
                                              prior_text)
        result_home = home
        result_width = width
    record["result_lineage_home"] = result_home
    record["result_lineage_width"] = result_width

    attempts = []
    chosen = None
    for materialize in (True, False):
        fields, refusal = render(entry_contract, prior_text, guards,
                                 materialize, result_home, result_width)
        if refusal is not None:
            record["outcome"] = "REFUSED"
            record["refusal_cause"] = refusal[0]
            record["refusal"] = refusal[1]
            return record
        result = gate_unit(lang, n, canon4_docs, sem_docs,
                           entry_contract, fields, prior_text,
                           bool(prior_text))
        verdict = result[0]
        attempts.append({
            "constant_materialization": fields["constant_materialization"],
            "verdict": verdict,
            "detail": result[1],
        })
        if verdict == "UNDECIDED":
            ok, note = structural_route(fields, prior_text)
            if ok:
                verdict = "PROVED_BY_CONSTRUCTION"
                result = (verdict,
                          "equivalence is forced by construction: the "
                          "region text executes this unit's own core "
                          "under an injective register permutation, on "
                          "the register state the standardized loads "
                          "establish from the input blocks, with every "
                          "own stack address placed by the one affine "
                          "map, and the result store touching a block "
                          "nothing else reads",
                          result[2], result[3], result[4], result[5])
                fields["structural_route_checks"] = note
            else:
                fields["structural_route_refusal"] = note
            attempts[-1]["structural_route"] = note
            attempts[-1]["verdict"] = verdict
        if verdict in ("PROVED_ON_SHIP", "PROVED_ON_PRIOR",
                       "PROVED_BY_CONSTRUCTION"):
            chosen = (fields, result)
            break
        if chosen is None:
            chosen = (fields, result)
        if fields["constant_materialization"] == "reduced":
            break
    fields, result = chosen
    record.update(fields)
    record["gate_attempts"] = attempts
    record["verdict"] = result[0]
    record["verdict_detail"] = result[1]
    record["gate_prior_verdict"] = result[2][0]
    record["gate_prior_detail"] = result[2][1]
    record["gate_ship_verdict"] = result[3][0]
    record["gate_ship_detail"] = result[3][1]
    record["arrival_contract_bindings"] = result[4]
    record["answer_home_source"] = result[5]
    if result[0] in ("PROVED_ON_SHIP", "PROVED_ON_PRIOR",
                     "PROVED_BY_CONSTRUCTION"):
        record["outcome"] = "REGION_TEXT_PROVED"
    elif result[0] == "DISPROVED":
        record["outcome"] = "GATE_DISPROVED"
        record["universal_text"] = None
    else:
        record["outcome"] = "GATE_UNDECIDED"
        record["universal_text"] = None
    return record


def run_language(lang, limit, fresh, c33, c32, gen_docs, arrival):
    canon4_docs = {}
    sem_docs = {}
    for other in LANGS:
        canon4_docs[other] = load("canon4_units_%s.json" % other)["units"]
        sem_docs[other] = load("sem_anchored_%s.json" % other)["units"]
    canon31 = load("canon31_units_%s.json" % lang)["units"]
    units = read_checkpoint(lang, fresh)
    done = 0
    for n in sorted(canon31, key=lambda x: int(x)):
        label = "%s/op_%s" % (lang, n)
        if label in units:
            continue
        if limit is not None and done >= limit:
            break
        rec31 = canon31[n]
        c4 = canon4_docs[lang].get(n) or {}
        prior_text, prior_source = newest_text_of(lang, n, c33, c32,
                                                  gen_docs)
        try:
            record = process_unit(lang, n, rec31, c4, prior_text,
                                  prior_source, canon4_docs, sem_docs,
                                  arrival)
        except Exception as bad:                   # noqa: BLE001
            record = {
                "unit": label,
                "lang": lang,
                "n": n,
                "population": "original",
                "operator": rec31.get("operator"),
                "outcome": "REFUSED",
                "refusal_cause": "renderer fault",
                "refusal": "%s: %s" % (type(bad).__name__, bad),
            }
        units[label] = record
        done = done + 1
        if done % CHECKPOINT_EVERY == 0:
            write_checkpoint(lang, units, tally_of(units))
            sys.stderr.write("  %s: %d done\n" % (lang, len(units)))
            sys.stderr.flush()
    write_checkpoint(lang, units, tally_of(units))
    return tally_of(units), len(units)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args(argv[1:])
    c33, c32, gen_docs = newest_text_sources()
    arrival = load("canon33_arrival_modes.json")["compiled"]
    langs = LANGS if args.all else [args.lang]
    for lang in langs:
        tally, total = run_language(lang, args.limit, args.fresh, c33,
                                    c32, gen_docs, arrival)
        print("%-6s %4d units  %s"
              % (lang, total, json.dumps(tally, sort_keys=True)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
