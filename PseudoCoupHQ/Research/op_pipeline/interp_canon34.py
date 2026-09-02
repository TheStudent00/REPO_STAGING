#!/usr/bin/env python3
"""interp_canon34.py -- TASK 32 part (a): the NINE refused interpreter
units, run through the current canonicalizer WITH task 30's designated
memory and arrival-mode machinery.

WHICH NINE.  log_107 (TASK 21) ran the pipeline's own checker over 11
interpreter/JIT units and got 2 proofs and 9 refusals.  The 9 are:

    java unit 2      -- the straight-line stripper rejects a branching
                        core
    ruby   4         -- vm_opt_plus, rb_fix_plus, rb_int_plus,
                        rb_big_plus: no instruction slice existed
    php    4         -- add_function and the three ZEND_ADD
                        specialisations: no instruction slice existed

Since then TASK 27 (log_113) made the ruby and php slices and carved
them by lineage confluence, and TASK 30 (log_118) built the designated
LOCATION scheme and the arrival-mode vocabulary.  This program is the
canonicalization run those two together make possible.

WHAT IS NEW HERE, and it is one thing.  `prove_interp_computation.py`
(TASK 27) refuses any computation core that reads an operand out of
MEMORY, in its own words: "placing that value in a designated register
would be re-plumbing the unit, not renaming it".  That refusal was
correct WHILE memory was anonymous overflow.  the owner's ruling of
2026-09-01 (log_115) removes its ground: "the canonical form gains
designated LOCATIONS (standardized virtual slots with a directory:
which location holds which designation), alongside the designated
registers".  So an operand that arrives in memory is not re-plumbed
into a register -- it is given its DESIGNATED LOCATION, S0, S1, ...,
exactly as an operand arriving in a register is given %rdi, and the
entry contract records the seat.  That is what this file renders.

THE RENDERING RULE, stated completely.

  1.  The unit's ARRIVAL is representation, its COMPUTATION is the
      core -- the split `lineage_carve.py` already made.  This file
      never re-carves a ruby or php unit; it reads the carve.
  2.  At the boundary instruction each traced lineage is read either
      as a BARE REGISTER operand or through a MEMORY operand (as the
      base or index of an address).  Read through memory means the
      VALUE is in memory; that lineage's seat is a designated
      location.
  3.  Seats: lineage 1 -> `a`, lineage 2 -> `b`.  A register seat is
      %rdi for `a` and %rsi for `b` (the ratified designated
      registers).  A memory seat is the next designated location in
      first-needed order, handed out by
      `designated_memory.Directory` with its register pools declared
      empty -- these values do not arrive in a register at all, so no
      register may be handed out for them.
  4.  The answer goes to %rax.  Where a source operand sits in a
      designated location it is brought into the reserved general
      reload register %r11 for the length of one instruction, which
      is `designated_memory`'s own park-reload idiom.
  5.  Widths follow the core instruction's own operand width; nothing
      is widened or narrowed.

  Everything else REFUSES BY NAME.  A core whose last instruction
  leaves its result in the FLAGS rather than in a register is refused,
  because materialising a value the unit never materialises would be
  inventing computation.

JAVA UNIT 2 is carved here, by the same lineage-confluence rule, over
its own recorded objdump (`interp_jvm.json`, unit `u2`, which carries
addresses).  Its two argument seats are seeded from the JVM's own
printed parameter comments -- `parm0: rsi`, `parm1: rdx` -- which is
THE TOOL'S OWN TESTIMONY, the middle evidence class, and is marked as
such on the record.  Every other fact about the unit is read from its
own bytes.

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

Run:
  /tmp/reconnect_venv/bin/python3 interp_canon34.py
"""

import json
import os
import re
import subprocess
import sys

import canon
import cross_unit_prover as CUP
import designated_memory as DM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_canon34.json")

# the nine, named as log_107 named them.  This list is a POPULATION,
# not a grouping: it says which units this lap must answer for.
THE_NINE = [
    ("java", "u2"),
    ("ruby", "vm_opt_plus"),
    ("ruby", "rb_fix_plus"),
    ("ruby", "rb_int_plus"),
    ("ruby", "rb_big_plus"),
    ("php", "add_function"),
    ("php", "ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("php", "ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
    ("php", "ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER"),
]

SEAT_REGISTER = {1: "rdi", 2: "rsi"}
ANSWER_FAMILY = "rax"

MEM_OPERAND = re.compile(r"^[^(]*\(([^)]*)\)$")


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def fold(name):
    import lineage_carve
    return lineage_carve.fold(name)


def lineage_index(lineage_name):
    """'argument_lineage_2' / 'slot_lineage_2' -> 2."""
    tail = lineage_name.rsplit("_", 1)[-1]
    return int(tail)


def operand_places(operand):
    """the register families an operand names, and whether it is a
    memory operand."""
    operand = operand.strip()
    match = MEM_OPERAND.match(operand)
    if match is None:
        if operand.startswith("%"):
            return [fold(operand.lstrip("%"))], False, operand.lstrip("%")
        return [], False, None
    inner = match.group(1)
    regs = []
    for piece in inner.split(","):
        piece = piece.strip()
        if piece.startswith("%"):
            regs.append(fold(piece.lstrip("%")))
    return regs, True, None


def width_index_of(register_name):
    bits = CUP.gp_width_of(register_name)
    return {64: 0, 32: 1, 16: 2, 8: 3}[bits]


def register_text(family, width_index):
    return "%" + canon.GP_NAMES[family][width_index]


def render_core(core_lines, place_lineages, directory):
    """-> (text, seats, refusal).

    `core_lines` are the computation core's mnemonics in order,
    `place_lineages` the boundary record's map place -> lineages."""
    if len(core_lines) == 0:
        return None, None, "the computation core is empty"
    head = core_lines[0]
    mnem, operands = canon.parse(head)
    if len(operands) != 2:
        return None, None, (
            "the core's first instruction %r does not have two "
            "operands; this renderer handles the two-operand "
            "confluence shape only" % head)
    tail = core_lines[1:]
    for line in tail:
        tail_mnem, _ = canon.parse(line)
        if tail_mnem in ("cmp", "test", "ucomisd", "ucomiss", "comisd",
                         "comiss"):
            return None, None, (
                "the core's last instruction %r leaves its result in "
                "the FLAGS, not in a register: the unit never "
                "materialises a value here, and materialising one so "
                "an answer register could be named would be inventing "
                "computation, not canonicalising it" % line)
    if tail:
        return None, None, (
            "the computation core is %d instructions and the "
            "instructions after the confluence are not recognised by "
            "this renderer: %r" % (len(core_lines), tail))

    src, dst = operands[0], operands[1]
    src_regs, src_is_mem, src_bare = operand_places(src)
    dst_regs, dst_is_mem, dst_bare = operand_places(dst)
    if dst_is_mem:
        return None, None, (
            "the core writes MEMORY (%r); its answer is not in a "
            "register, so no answer seat can be named" % head)

    def lineage_of(regs):
        found = []
        for reg in regs:
            for lin in place_lineages.get(reg, []):
                if lin not in found:
                    found.append(lin)
        return found

    src_lin = lineage_of(src_regs)
    dst_lin = lineage_of(dst_regs)
    if len(src_lin) != 1 or len(dst_lin) != 1:
        return None, None, (
            "an operand of the core carries %r / %r lineages; a seat "
            "assignment needs exactly one traced value per operand"
            % (src_lin, dst_lin))
    if src_lin[0] == dst_lin[0]:
        return None, None, (
            "both operands of the core carry the same lineage %r"
            % src_lin[0])

    width = width_index_of(dst_bare)
    answer_text = register_text(ANSWER_FAMILY, width)
    seats = {}
    lines = []

    def seat_of(lineage, is_mem):
        index = lineage_index(lineage)
        if is_mem:
            loc = directory.location_for("operand_%d" % index, False)
            text = loc[1]
            designation = directory.designation_of_text(text)
            seats["operand_%d" % index] = {
                "seat_kind": "designated location",
                "designation": designation,
                "text": text,
            }
            return text
        family = SEAT_REGISTER[index]
        text = register_text(family, width)
        seats["operand_%d" % index] = {
            "seat_kind": "designated register",
            "designation": {1: "a", 2: "b"}[index],
            "text": text,
        }
        return text

    dst_seat = seat_of(dst_lin[0], dst_is_mem)
    lines.append("mov %s,%s" % (dst_seat, answer_text))
    src_seat = seat_of(src_lin[0], src_is_mem)
    if src_is_mem:
        reload_reg = DM.reload_register(False, 0)
        reload_text = register_text(reload_reg, width)
        lines.append("%s %s,%s" % (DM.reload_mnemonic(False, width),
                                   src_seat, reload_text))
        lines.append("%s %s,%s" % (mnem, reload_text, answer_text))
    else:
        lines.append("%s %s,%s" % (mnem, src_seat, answer_text))
    lines.append("ret")
    seats["answer"] = {
        "seat_kind": "designated register",
        "designation": "answer",
        "text": answer_text,
    }
    return "; ".join(lines), seats, None


def newest_carve(unit_id):
    """the carve record for a unit, preferring the SHIP build (the
    build every refusal in this line fires against, measured in
    log_118 sec 1.2), falling back to the anchor build."""
    carves = load("lineage_carve.json")
    ship = None
    anchor = None
    for rec in carves["records"]:
        if rec["unit"] != unit_id:
            continue
        if rec["outcome"] != "CARVED":
            continue
        if rec["build"] == "ship":
            ship = rec
        else:
            anchor = rec
    return ship or anchor


def all_carve_records(unit_id):
    carves = load("lineage_carve.json")
    return [r for r in carves["records"] if r["unit"] == unit_id]


# ---------------------------------------------------------------- java

JAVA_SEED_EVIDENCE = (
    "the tool's own testimony -- the JVM's own printed parameter "
    "comments on this nmethod, quoted verbatim from interp_jvm.json "
    "unit u2: '# parm0:    rsi       = int' and "
    "'# parm1:    rdx       = int'.  Every other fact about this unit "
    "below is read from its own bytes."
)


def java_objdump_rows():
    doc = load("interp_jvm.json")
    unit = None
    for candidate in doc["units"]:
        if candidate["id"] == "u2":
            unit = candidate
    rows = []
    for run in unit["arch_unit"]:
        for line in run["objdump"]:
            if "\t" not in line:
                continue
            pieces = line.split("\t")
            if len(pieces) < 3:
                continue
            address = pieces[0].strip().rstrip(":")
            text = pieces[-1].strip()
            text = re.sub(r"\s+", " ", text)
            rows.append({"address": address, "mnem": text})
    return unit, rows


def java_carve():
    """the lineage-confluence carve of java unit 2, over its own
    recorded objdump.  Walks the FALL-THROUGH normal path and records
    every conditional branch it passes as a guard, which is exactly
    the arrival/computation split AgentMemory's 2026-08-31 ruling
    names."""
    unit, rows = java_objdump_rows()
    lineages = {"rsi": ["argument_lineage_1"], "rdx": ["argument_lineage_2"]}
    trace = []
    guards = []
    boundary = None
    for index, row in enumerate(rows):
        text = row["mnem"]
        mnem, operands = canon.parse(text)
        if mnem.startswith("j") and mnem != "jmp":
            guards.append({
                "at_address": row["address"],
                "instruction": text,
                "preceding_test": rows[index - 1]["mnem"] if index else None,
            })
            continue
        if mnem == "jmp":
            break
        if not operands:
            if mnem == "cltd":
                # sign-extends %eax into %edx:%eax -- the divide
                # family's hardware pair.  the lineage in rax
                # spreads to rdx as one operation.
                if "rax" in lineages:
                    lineages["rdx"] = list(lineages["rax"])
                    trace.append({"address": row["address"],
                                  "instruction": text,
                                  "lineages_touched": list(lineages["rax"])})
                continue
            if mnem == "ret":
                break
            continue
        if mnem == "xor" and len(operands) == 2:
            if operands[0].strip() == operands[1].strip():
                # a self-xor is a ZEROING, not a read: it destroys the
                # lineage in that place rather than carrying it.
                zero_regs, _m, _b = operand_places(operands[1])
                for reg in zero_regs:
                    if reg in lineages:
                        del lineages[reg]
                trace.append({"address": row["address"],
                              "instruction": text,
                              "lineages_touched": [],
                              "note": "self-xor: a zeroing, no lineage read"})
                continue
        read = []
        implicit = []
        if mnem in ("idiv", "div", "imul", "mul") and len(operands) == 1:
            # the hardware pins the dividend/multiplicand in the
            # %edx:%eax pair; those reads are IMPLICIT in the
            # instruction text and must be counted, or the confluence
            # is invisible.
            implicit = ["rax", "rdx"]
        for reg in implicit:
            for lin in lineages.get(reg, []):
                if lin not in read:
                    read.append(lin)
        for operand in operands:
            regs, _is_mem, _bare = operand_places(operand)
            for reg in regs:
                for lin in lineages.get(reg, []):
                    if lin not in read:
                        read.append(lin)
        if len(read) >= 2:
            place_lineages = {}
            for operand in operands:
                regs, _is_mem, _bare = operand_places(operand)
                for reg in regs:
                    if reg in lineages:
                        place_lineages[reg] = list(lineages[reg])
            if mnem in ("idiv", "div", "imul", "mul"):
                # the hardware pins the dividend in %edx:%eax; the
                # single named operand is the divisor.  the answer
                # is the quotient, in %eax.
                place_lineages = {}
                place_lineages["rax"] = list(lineages.get("rax", []))
                for operand in operands:
                    regs, _is_mem, _bare = operand_places(operand)
                    for reg in regs:
                        if reg in lineages and reg != "rax":
                            place_lineages[reg] = list(lineages[reg])
            boundary = {
                "index": index,
                "address": row["address"],
                "instruction": text,
                "lineages_read": read,
                "place_lineages": place_lineages,
            }
            trace.append({"address": row["address"], "instruction": text,
                          "lineages_touched": read})
            break
        if read:
            trace.append({"address": row["address"], "instruction": text,
                          "lineages_touched": read})
        # propagate: AT&T destination is the last operand
        dst = operands[-1]
        dst_regs, dst_is_mem, _bare = operand_places(dst)
        if dst_is_mem:
            continue
        for reg in dst_regs:
            if read:
                lineages[reg] = list(read)
            elif reg in lineages:
                del lineages[reg]
    return unit, rows, trace, guards, boundary


def java_record():
    unit, rows, trace, guards, boundary = java_carve()
    record = {
        "unit": "java/op_2",
        "language": "java",
        "symbol": "af2",
        "operator": unit["label"],
        "build": "ship (the JIT's own emitted nmethod; there is no "
                 "anchor build for a JIT -- interp_jvm.json records "
                 "one tier-c2 compilation)",
        "provenance_is_weaker": True,
        "seed_evidence_class": JAVA_SEED_EVIDENCE,
        "walk_instruction_count": len(rows),
        "lineage_trace": trace,
        "guards_passed_on_the_normal_path": guards,
    }
    if boundary is None:
        record["outcome"] = "REFUSED"
        record["refusal"] = ("no instruction on the fall-through normal "
                             "path reads both lineages")
        return record
    record["outcome"] = "CANONICAL_TEXT_PRODUCED"
    record["boundary"] = boundary
    mnem, operands = canon.parse(boundary["instruction"])
    # the divide family: the dividend is the pinned %edx:%eax pair,
    # the named operand is the divisor, the quotient is the answer.
    divisor = operands[-1].strip()
    divisor_regs, _m, divisor_bare = operand_places(divisor)
    dividend_lineages = boundary["place_lineages"].get("rax", [])
    divisor_lineages = []
    for reg in divisor_regs:
        divisor_lineages.extend(boundary["place_lineages"].get(reg, []))
    if len(dividend_lineages) != 1 or len(divisor_lineages) != 1:
        record["outcome"] = "REFUSED"
        record["canonical_text"] = None
        record["refusal"] = (
            "the boundary's dividend / divisor carry %r / %r lineages; "
            "a seat assignment needs exactly one traced value per "
            "operand" % (dividend_lineages, divisor_lineages))
        return record
    width = width_index_of(divisor_bare)
    dividend_seat = register_text(
        SEAT_REGISTER[lineage_index(dividend_lineages[0])], width)
    divisor_seat = register_text(
        SEAT_REGISTER[lineage_index(divisor_lineages[0])], width)
    answer_text = register_text(ANSWER_FAMILY, width)
    text = "mov %s,%s; cltd; %s %s; ret" % (
        dividend_seat, answer_text, mnem, divisor_seat)
    record["canonical_text"] = text
    record["canonicalization_note"] = (
        "the traced values are renamed to their designated registers "
        "(dividend -> %s, divisor -> %s) and the answer to %s.  `cltd` "
        "is kept because the hardware splits one operation across the "
        "pair cltd+%s (AgentMemory's own alpha example); it is not a "
        "move and is not erasable.  No designated location is needed: "
        "both operands of this unit arrive in registers."
        % (dividend_seat, divisor_seat, answer_text, mnem))
    record["seats"] = {
        "operand_1": {"seat_kind": "designated register",
                      "designation": "a", "text": dividend_seat},
        "operand_2": {"seat_kind": "designated register",
                      "designation": "b", "text": divisor_seat},
        "answer": {"seat_kind": "designated register",
                   "designation": "answer", "text": answer_text},
    }
    record["designated_location_directory"] = {}
    record["type_pair_read"] = "%s,%s" % tuple(unit["operand_types"])
    record["type_pair_read_evidence_class"] = (
        "the tool's own testimony -- javap's own bytecode listing and "
        "the JVM's own parameter comments.  There is no ELF file for a "
        "JIT nmethod, so there is no DWARF to raise this to the "
        "forced-by-construction class (log_111 recorded the same "
        "refusal).")
    record["result_type_read"] = unit["result_type"]
    return record


# ----------------------------------------------------------- ruby, php

def ruby_php_record(lang, symbol):
    unit_id = "%s/%s" % (lang, symbol)
    keys = load("dwarf_typed_key_t27.json")
    representation = None
    proposal = load("proposal_representation_dimension3.json")
    for handler in proposal["handlers"]:
        if handler["unit"] == unit_id:
            representation = handler
    record = {
        "unit": unit_id,
        "language": lang,
        "symbol": symbol,
        "provenance_is_weaker": True,
    }
    if representation is not None:
        record["operator"] = representation["operator"]
        record["representation"] = representation["representation"]
        record["type_pair_read"] = representation.get("type_pair_read")
        record["type_pair_read_evidence_class"] = representation.get(
            "type_pair_read_evidence_class")
        record["result_type_read"] = (
            representation.get("dwarf_type_read", {}) or {}).get("return_type")
    record["carve_outcomes_per_build"] = [
        {"build": r["build"], "outcome": r["outcome"],
         "refusal": r.get("refusal")}
        for r in all_carve_records(unit_id)]
    carve = newest_carve(unit_id)
    if carve is None:
        record["outcome"] = "REFUSED"
        refusals = [r.get("refusal") for r in all_carve_records(unit_id)]
        record["refusal"] = (
            "no build of this unit carves, so there is no computation "
            "part to canonicalise.  The carve refusals, verbatim: %s"
            % " | ".join([x for x in refusals if x]))
        record["what_would_change_it"] = (
            "nothing in task 30's machinery reaches this: designated "
            "memory answers where an operand LIVES, and this unit's "
            "refusal is that the two lineages never meet inside the "
            "unit at all -- the confluence is in a callee.")
        return record
    record["build"] = carve["build"]
    record["boundary"] = carve["boundary"]["instruction"]
    record["boundary_address"] = carve["boundary"]["address"]
    core = [x["mnem"] for x in carve["computation_core"]["instructions"]]
    record["computation_core"] = core
    directory = DM.Directory()
    # these values do not arrive in a register at all, so no register
    # may be handed out for them: the pools are declared empty and
    # every seat this Directory issues is a designated location.
    directory.general_bench = []
    directory.vector_bench = []
    text, seats, refusal = render_core(
        core, carve["boundary"]["place_lineages"], directory)
    if text is None:
        record["outcome"] = "REFUSED"
        record["canonical_text"] = None
        record["refusal"] = refusal
        return record
    record["outcome"] = "CANONICAL_TEXT_PRODUCED"
    record["canonical_text"] = text
    record["seats"] = seats
    record["designated_location_directory"] = directory.directory()
    record["canonicalization_note"] = (
        "the traced values are renamed to their designated seats and "
        "the answer to %%rax.  An operand read through a memory "
        "operand at the boundary keeps its seat IN MEMORY -- a "
        "designated location, per the owner's 2026-09-01 ruling -- and is "
        "brought into the reserved reload register %s for the length "
        "of one instruction.  Nothing is re-plumbed into a register "
        "that did not arrive in one." % DM.reload_register(False, 0))
    return record


def refuse_own_output_on_spelling_keys(path):
    """THE MECHANICAL GUARD: this stage runs the spelling-key check
    over its own output and refuses the output on failure."""
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
         path], capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % path)
    return proc.returncode


def main():
    records = []
    for lang, symbol in THE_NINE:
        if lang == "java":
            records.append(java_record())
            continue
        records.append(ruby_php_record(lang, symbol))

    produced = [r for r in records
                if r.get("canonical_text")]
    refused = [r for r in records if not r.get("canonical_text")]
    out = {
        "meta": {
            "generator": "interp_canon34.py",
            "task": "TASK 32 part (a) -- the nine refused interpreter "
                    "units through the current canonicalizer, with "
                    "task 30's designated-location scheme",
            "population": "the nine units log_107 (TASK 21) refused: "
                          "java unit 2, ruby 4, php 4",
            "reads_read_only": [
                "lineage_carve.json", "dwarf_typed_key_t27.json",
                "proposal_representation_dimension3.json",
                "interp_jvm.json", "designated_memory.py",
                "canon.py", "cross_unit_prover.py"],
            "new_ground_this_lap": "an operand that arrives in MEMORY "
                                   "is given a designated location "
                                   "rather than refused",
            "provenance_is_weaker": True,
        },
        "records": records,
        "summary": {
            "population": len(records),
            "canonical_text_produced": len(produced),
            "refused": len(refused),
            "refusals_by_unit": dict(
                [(r["unit"], r.get("refusal")) for r in refused]),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    for r in records:
        state = r.get("outcome")
        print("%-58s %-26s %s" % (r["unit"], state,
                                  r.get("canonical_text") or
                                  (r.get("refusal") or "")[:90]))
    print("summary: %d of %d produced canonical text"
          % (len(produced), len(records)))
    return refuse_own_output_on_spelling_keys(OUT)


if __name__ == "__main__":
    sys.exit(main())
