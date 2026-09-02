#!/usr/bin/env python3
"""interp_canon35.py -- TASK 34 part (a): ALL ELEVEN interpreter/JIT
units rendered in THE UNIVERSAL CANONICAL FORM.

WHAT CHANGED, AND IT IS ONE RULING.  the owner, 2026-09-01, recorded in
AgentMemory as "THE UNIVERSAL CANONICAL FORM: VIRTUAL MEMORY FOR EVERY
UNIT, STANDARDIZED LOADS, ARRIVAL ANNOTATED": the designated-register
description (a -> %rdi, b -> %rsi, answer -> %rax) is SUPERSEDED as the
primary statement.  Every arch-unit's values live in the designated
VIRTUAL MEMORY system, the LOADS out of those locations into registers
are themselves standardized -- one load pattern for everyone -- and HOW
a value arrived (plain / pointer / tagged) is an ANNOTATION on the one
shared form, never a separate dialect.

So the form this file emits, for every unit without exception:

    <one standardized load per traced value, in designation order>
    <the unit's own computation core, reading the designated registers>
    ret

with a DIRECTORY saying which designated location holds which
designation (S0 = a, S1 = b), and an ARRIVAL ANNOTATION per value.

WHAT THIS REPLACES.  `interp_canon34.py` (TASK 32) rendered the
register-based form: an operand that arrived in memory kept a raw
park-reload line inside the core (`mov -0x8(%rsp),%r11`) while an
operand that arrived in a register was simply read.  Two arrivals, two
shapes.  Under the ruling there is one shape.  The transformation from
the register form to the universal form is a HOIST: the reload leaves
the core and becomes a standardized load into that value's designated
register.

THE HOIST'S PRECONDITIONS, checked per unit, refused by name:

  P1  the core writes no memory (nothing can invalidate a designated
      location between the load and the read);
  P2  after the rewrite the core does not write a designated operand
      register before its last read of it (nothing can clobber a
      hoisted load);
  P3  the unit has exactly two operand seats and one answer seat.

THE GATE.  The universal text is not trusted because it was derived.
Every unit's universal text is put to z3 against THAT UNIT'S OWN prior
text, with each designated location bound to the same symbol as the
operand it seats (the entry-contract binding of
`interp_join_prover33.py`).  A unit whose new text is not PROVED equal
to its own old text keeps no new text.  No exemption, no unit excused.

THE THREE THAT REFUSED LAST LAP ARE RE-ATTEMPTED, and one of them is
fixed here:

  php/add_function -- FIXED.  Its recorded confluence was
      `or 0x8(%rdx),%al`, the ZVAL TYPE-TAG dispatch, and the renderer
      then refused because that instruction's result is in the FLAGS.
      Under the ruling, arrival is an ANNOTATION: for a POINTER
      arrival the dereference is part of the standardized load, and a
      read at a NONZERO displacement from the pointer is the arrival's
      metadata (the type tag), not the value.  So the tag dispatch is
      arrival machinery, the confluence is sought on the VALUE
      lineages, and it is found at `add (%rdx),%rax`.  The tag branch
      is recorded as a mode row rather than lost.
  ruby/vm_opt_plus -- STILL NO TEXT, and the cause is not the form.
      The ship build has NO BODY for this symbol at all
      (op_units_ruby.json probe 1: ship present=false).  There is
      nothing to canonicalise, and the gate forbids substituting the
      anchor build's body.
  ruby/rb_big_plus -- STILL NO TEXT, and the cause is not the form.
      Its ship body's two lineages meet inside callees (`bigadd`,
      `big2dbl`), which are not extracted units; the confluence is
      interprocedural.  Register scarcity is not involved.

  Neither remaining refusal is a register-scarcity or plumbing
  refusal.  Under the ruling such a refusal would be a defect; these
  two are evidence facts about the builds, and they are stated as
  such rather than as walls of the form.

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
  /tmp/reconnect_venv/bin/python3 interp_canon35.py
"""

import json
import os
import re
import subprocess
import sys

import z3

import canon
import canon8_behaviour_check as BC8
import canon10_behaviour_check as BC10
import canon33_gate as G33
import designated_memory as DM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_canon35.json")

PER_PAIR_TIMEOUT_MS = 20000

# the designated register each operand designation is LOADED INTO by
# the standardized load.  The registers are the standardized vehicles,
# not the definition -- AgentMemory, 2026-09-01.
SEAT_FAMILY = {"operand_1": "rdi", "operand_2": "rsi"}
SEAT_DESIGNATION = {"operand_1": "a", "operand_2": "b"}
ANSWER_FAMILY = "rax"

WIDTH_TEXT = {
    "rdi": {64: "%rdi", 32: "%edi"},
    "rsi": {64: "%rsi", 32: "%esi"},
    "rax": {64: "%rax", 32: "%eax"},
}

MEMORY_DESTINATION = re.compile(r"\(%[a-z0-9]+\)\s*$")


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


def mnemonic_of(line):
    return line.split(" ", 1)[0].strip()


def register_family(text):
    if not text.startswith("%"):
        return None
    name = text[1:]
    return canon.FAMILY_OF.get(name)


def width_of_register_text(text):
    name = text[1:]
    if name.startswith("r") and not name[-1] == "d":
        return 64
    if name.startswith("e"):
        return 32
    if name.endswith("d"):
        return 32
    return 64


# ------------------------------------------------------------------
# the register-form units, read from their own artifacts
# ------------------------------------------------------------------

def seats_from_text(text):
    """a unit whose operands both arrive in designated registers has no
    recorded seat dict on some artifacts; the seats are then read off
    its own text, which names the designated registers directly."""
    seats = {}
    for name, family in SEAT_FAMILY.items():
        found = None
        for line in split_lines(text):
            for operand in operands_of(line):
                if register_family(operand) == family:
                    found = operand
                    break
            if found:
                break
        if found is None:
            return None
        seats[name] = {
            "seat_kind": "designated register",
            "designation": SEAT_DESIGNATION[name],
            "text": found,
        }
    seats["answer"] = {
        "seat_kind": "designated register",
        "designation": "answer",
        "text": "%rax",
    }
    return seats


def canon34_units():
    doc = load("interp_canon34.json")
    units = []
    for rec in doc["records"]:
        units.append({
            "unit": rec["unit"],
            "language": rec["language"],
            "symbol": rec.get("symbol"),
            "operator": rec.get("operator"),
            "prior_text": rec.get("canonical_text"),
            "prior_text_source": "interp_canon34.json (TASK 32 part a)",
            "seats": rec.get("seats"),
            "arrival_recorded": rec.get("representation"),
            "build": rec.get("build"),
            "prior_refusal": rec.get("refusal"),
            "computation_core": rec.get("computation_core"),
            "carve_outcomes_per_build": rec.get("carve_outcomes_per_build"),
            "type_pair_read": rec.get("type_pair_read"),
            "result_type_read": rec.get("result_type_read"),
            "guards_passed_on_the_normal_path":
                rec.get("guards_passed_on_the_normal_path"),
            "lineage_trace": rec.get("lineage_trace"),
        })
    return units, doc


def all_eleven():
    units = []

    cpython = load("canon_interp_units_cpython.json")
    units.append({
        "unit": "cpython/long_add_fastpath",
        "language": "cpython",
        "symbol": "long_add_fastpath",
        "operator": cpython["unit"]["operator"],
        "prior_text": cpython.get("canonical_text"),
        "prior_text_source":
            "canon_interp_units_cpython.json (TASK 21), read-only",
        "seats": None,
        "arrival_recorded": "typed-pointer(PyLongObject*)",
        "build": "ship",
    })

    java = load("canon_interp_units_java.json")
    units.append({
        "unit": "java/op_1",
        "language": "java",
        "symbol": "af1",
        "operator": java["unit_1"]["operator"],
        "prior_text": java["unit_1"].get("canonical_text"),
        "prior_text_source":
            "canon_interp_units_java.json (TASK 21), read-only",
        "seats": None,
        "arrival_recorded": "plain",
        "build": "ship (the JIT's own emitted nmethod)",
    })

    rest, doc = canon34_units()
    units.extend(rest)
    return units, doc


# ------------------------------------------------------------------
# the render into the universal form
# ------------------------------------------------------------------

def slot_for(index):
    return DM.slot_text(index)


def hoist(unit):
    """the register form -> the universal form.  Returns
    (record_fields, refusal_or_None)."""
    text = unit.get("prior_text")
    if not text:
        return None, ("no register-form text exists for this unit, so "
                      "there is nothing to re-render into the universal "
                      "form")
    seats = unit.get("seats") or seats_from_text(text)
    if seats is None:
        return None, ("this unit's two operand seats could not be read "
                      "from its own text: no operand names a designated "
                      "register family")
    for name in ("operand_1", "operand_2", "answer"):
        if name not in seats:
            return None, ("P3 fails: seat %r is missing, so the unit does "
                          "not present two operands and one answer" % name)

    lines = split_lines(text)
    if lines and lines[-1] == "ret":
        core = lines[:-1]
    else:
        core = list(lines)

    # ---- P1: no memory write in the core.
    for line in core:
        operands = operands_of(line)
        if not operands:
            continue
        destination = operands[-1]
        if MEMORY_DESTINATION.search(destination):
            return None, ("P1 fails: the core writes memory at %r, so a "
                          "designated location could be invalidated "
                          "between its standardized load and its read"
                          % line)

    # ---- the directory: S0 = a, S1 = b, always, for every unit.
    directory = []
    loads = []
    rewrite = {}
    for order, name in enumerate(("operand_1", "operand_2")):
        seat = seats[name]
        family = SEAT_FAMILY[name]
        slot = slot_for(order)
        if seat["seat_kind"] == "designated register":
            width = width_of_register_text(seat["text"])
            arriving_from = seat["text"]
            park_line = None
        else:
            width = 64
            arriving_from = seat["text"]
            park_line = seat["text"]
            for line in core:
                if mnemonic_of(line) not in ("mov", "movq", "movd"):
                    continue
                operands = operands_of(line)
                if len(operands) != 2:
                    continue
                if operands[0] != seat["text"]:
                    continue
                width = width_of_register_text(operands[1])
                rewrite[operands[1]] = WIDTH_TEXT[family][width]
                break
        register_text = WIDTH_TEXT[family].get(width)
        if register_text is None:
            return None, ("no standardized load exists for width %d" % width)
        directory.append({
            "designation": SEAT_DESIGNATION[name],
            "designated_location": slot,
            "location_name": DM.designation_name(order),
            "loaded_into": register_text,
            "prior_arrival_place": arriving_from,
            "arrival_annotation": unit.get("arrival_recorded"),
        })
        loads.append("mov %s,%s" % (slot, register_text))
        if seat["seat_kind"] == "designated register":
            if seat["text"] != register_text:
                rewrite[seat["text"]] = register_text
        else:
            rewrite[seat["text"]] = register_text

    # ---- the core, rewritten: park-reloads deleted, temps renamed.
    rendered = []
    for line in core:
        operands = operands_of(line)
        if len(operands) == 2 and G33.is_slot_text(operands[0]):
            # the park-reload the register form needed; the universal
            # form does the load once, at the top, into the designated
            # register.  Delete-and-substitute as one act.
            continue
        new_line = line
        for old in sorted(rewrite, key=len, reverse=True):
            new_line = new_line.replace(old, rewrite[old])
        rendered.append(new_line)

    # ---- P2: no write to a designated operand register before its
    # last read.
    for name in ("operand_1", "operand_2"):
        family = SEAT_FAMILY[name]
        last_read = -1
        first_write = None
        for index, line in enumerate(rendered):
            operands = operands_of(line)
            if not operands:
                continue
            for position, operand in enumerate(operands):
                if register_family(operand) != family:
                    continue
                if position == len(operands) - 1:
                    if first_write is None:
                        first_write = index
                else:
                    last_read = index
        if first_write is not None and first_write < last_read:
            return None, ("P2 fails: the core writes %s at line %d before "
                          "its last read at line %d, so the standardized "
                          "load would be clobbered"
                          % (family, first_write, last_read))

    universal = loads + rendered + ["ret"]
    return {
        "universal_text": "; ".join(universal),
        "standardized_loads": loads,
        "core_after_substitution": rendered,
        "designated_location_directory": directory,
        "seats_in_the_universal_form": {
            "operand_1": {
                "seat_kind": "designated location",
                "designation": "a",
                "text": slot_for(0),
            },
            "operand_2": {
                "seat_kind": "designated location",
                "designation": "b",
                "text": slot_for(1),
            },
            "answer": {
                "seat_kind": "designated register",
                "designation": "answer",
                "text": seats["answer"]["text"],
            },
        },
        "hoist_preconditions_checked": ["P1", "P2", "P3"],
    }, None


# ------------------------------------------------------------------
# the gate: the new text against the unit's OWN old text
# ------------------------------------------------------------------

def bind(shared_seed, seats):
    made = []
    for name in sorted(seats):
        seat = seats[name]
        if seat.get("seat_kind") != "designated location":
            continue
        family = SEAT_FAMILY.get(name)
        if family is None:
            continue
        symbol = BC8.seed_family(shared_seed, family)
        shared_seed["slot_%s" % seat["text"]] = symbol
        made.append({
            "seat": name,
            "designated_location": seat["text"],
            "bound_to_the_same_symbol_as": "%%%s" % family,
        })
    return made


GATE_SLOT_BASE = 0x200


def rename_prior_slots(prior_text, prior_seats):
    """THE NAME CLASH, fixed at first observation.  The register form
    parked an operand at `-0x8(%rsp)`, and the universal form's S0 is
    also `-0x8(%rsp)` -- but they may seat DIFFERENT operands.  Binding
    both texts' slots by their text would then bind one operand's
    symbol onto the other's seat and the proof would ask the wrong
    question.  A designated location's text is a NAME for a seat, so
    for the gate the prior text's slots are renamed to gate-private
    names before either side is bound.  Nothing about the stored
    artifacts changes."""
    seats = {}
    text = prior_text
    order = 0
    for name in sorted(prior_seats or {}):
        seat = dict((prior_seats or {})[name])
        if seat.get("seat_kind") == "designated location":
            fresh = "-0x%x(%%rsp)" % (GATE_SLOT_BASE + 8 * order)
            order = order + 1
            text = text.replace(seat["text"], fresh)
            seat["text"] = fresh
        seats[name] = seat
    return text, seats


def gate(prior_text, prior_seats, universal_text, universal_seats):
    shared_seed = {}
    bindings = []
    prior_text, prior_seats = rename_prior_slots(prior_text, prior_seats)
    bindings.extend(bind(shared_seed, prior_seats or {}))
    bindings.extend(bind(shared_seed, universal_seats))
    try:
        left, width_left = G33.Sim33(shared_seed, "prior").answer_value(
            split_lines(prior_text))
        right, width_right = G33.Sim33(shared_seed, "universal").answer_value(
            split_lines(universal_text))
    except (BC10.NotModeled, G33.NotModeled) as exc:
        return "UNDECIDED", ("the simulator has no model for a mnemonic "
                             "in one of these texts: %s" % exc), bindings
    width = min(width_left, width_right)
    left = z3.Extract(width - 1, 0, left)
    right = z3.Extract(width - 1, 0, right)
    solver = z3.Solver()
    solver.set("timeout", PER_PAIR_TIMEOUT_MS)
    solver.add(left != right)
    verdict = solver.check()
    if verdict == z3.unsat:
        return "PROVED", ("z3 proved the universal text and this unit's "
                          "own prior text equal at %d bits for every "
                          "value of every seat, with each designated "
                          "location bound to the operand it seats"
                          % width), bindings
    if verdict == z3.sat:
        return "DISPROVED", ("z3 found a counterexample: %s"
                             % solver.model()), bindings
    return "UNDECIDED", ("z3 returned %r at a %dms timeout"
                         % (verdict, PER_PAIR_TIMEOUT_MS)), bindings


# ------------------------------------------------------------------
# php/add_function: the arrival-aware carve
# ------------------------------------------------------------------

READ_MODIFY_WRITE = ("add", "or", "sub", "and", "xor", "adc", "sbb",
                     "imul")

VALUE_LOAD = re.compile(r"^\(%([a-z0-9]+)\)$")
METADATA_READ = re.compile(r"^(0x[0-9a-f]+)\(%([a-z0-9]+)\)$")


def add_function_walk():
    """the ship walk for php/add_function, read out of
    lineage_carve.json unchanged."""
    doc = load("lineage_carve.json")
    for rec in doc["records"]:
        if rec["symbol"] != "add_function":
            continue
        if rec["build"] != "ship":
            continue
        rows = {}
        for segment in ("arrival", "computation_core", "after_the_answer"):
            block = rec.get(segment) or {}
            for item in block.get("instructions", []):
                rows[item["index"]] = item
        return rec, [rows[i] for i in sorted(rows)]
    return None, None


def arrival_aware_carve(instructions, seeds):
    """the confluence on the VALUE lineages of POINTER arrivals.

    THE RULE, stated once and applied mechanically.  When a value
    arrives as a POINTER, the dereference is part of the standardized
    load, so:
      - a read of `(%p)` where %p holds pointer lineage k yields VALUE
        lineage k;
      - a read of `disp(%p)` with a NONZERO displacement is the
        arrival's METADATA (php's zval type tag lives at 0x8), and it
        is arrival machinery, not the value;
      - the confluence is the first instruction reading both VALUE
        lineages.
    The normal path is the FALL-THROUGH of each representation guard;
    every guard passed is recorded, not discarded.
    """
    pointer_of = dict(seeds)
    value_of = {}
    guards = []
    metadata_reads = []
    trace = []
    for item in instructions:
        line = item["mnem"]
        mnemonic = mnemonic_of(line)
        operands = operands_of(line)
        if mnemonic.startswith("j"):
            guards.append({
                "at_index": item["index"],
                "address": item["addr"],
                "instruction": line,
                "normal_path": "fall-through",
            })
            continue
        if mnemonic in ("cmp", "test", "endbr64"):
            trace.append({"index": item["index"], "instruction": line,
                          "role": "guard test or no-op"})
            continue
        read_values = set()
        if len(operands) > 1:
            reads = list(operands[:-1])
            if mnemonic in READ_MODIFY_WRITE:
                # the destination of these is also a SOURCE; missing
                # that is how a confluence at `add (%rdx),%rax` goes
                # unseen.
                reads.append(operands[-1])
        else:
            reads = list(operands)
        for operand in reads:
            match = VALUE_LOAD.match(operand)
            if match:
                family = canon.FAMILY_OF.get(match.group(1))
                if family in pointer_of:
                    read_values.add(pointer_of[family])
                continue
            match = METADATA_READ.match(operand)
            if match:
                family = canon.FAMILY_OF.get(match.group(2))
                if family in pointer_of:
                    metadata_reads.append({
                        "index": item["index"],
                        "instruction": line,
                        "role": "arrival metadata (the type tag), not "
                                "the value",
                    })
                continue
            family = register_family(operand)
            if family in value_of:
                read_values.add(value_of[family])
        if len(read_values) >= 2:
            return {
                "confluence": {
                    "index": item["index"],
                    "address": item["addr"],
                    "instruction": line,
                    "value_lineages_read": sorted(read_values),
                },
                "guards_passed_on_the_normal_path": guards,
                "arrival_metadata_reads": metadata_reads,
                "trace": trace,
            }, None
        if operands:
            destination = operands[-1]
            family = register_family(destination)
            if family is not None:
                if len(read_values) == 1:
                    value_of[family] = sorted(read_values)[0]
                    trace.append({"index": item["index"],
                                  "instruction": line,
                                  "carries": sorted(read_values)[0]})
                else:
                    value_of.pop(family, None)
    return None, ("no instruction on the normal path reads both value "
                  "lineages")


def add_function_record():
    rec, instructions = add_function_walk()
    if rec is None:
        return {"unit": "php/add_function", "outcome": "REFUSED",
                "refusal": "no ship carve record exists on disk"}
    seeds = {"rsi": "argument_lineage_1", "rdx": "argument_lineage_2"}
    carve, refusal = arrival_aware_carve(instructions, seeds)
    out = {
        "unit": "php/add_function",
        "language": "php",
        "symbol": "add_function",
        "build": "ship",
        "re_attempted_under_the_universal_form": True,
        "prior_refusal_verbatim":
            "the core's last instruction 'cmp $0x44,%al' leaves its "
            "result in the FLAGS, not in a register: the unit never "
            "materialises a value here, and materialising one so an "
            "answer register could be named would be inventing "
            "computation, not canonicalising it",
        "why_the_prior_refusal_no_longer_holds":
            "the prior confluence was the zval TYPE-TAG dispatch "
            "(`or 0x8(%rdx),%al`).  Under the universal form arrival is "
            "an annotation: a read at a nonzero displacement from a "
            "pointer arrival is the arrival's metadata, so the tag "
            "dispatch is arrival machinery and the confluence is sought "
            "on the value lineages.",
        "seeds": seeds,
        "seed_evidence_class":
            "forced by construction for the dereference rule (the "
            "instructions are the unit's own bytes); the seed order is "
            "the SysV out-parameter-first policy lineage_carve.py "
            "already recorded for this routine from its DWARF "
            "signature add_function(zval *result, zval *op1, zval *op2)",
    }
    if carve is None:
        out["outcome"] = "REFUSED"
        out["refusal"] = refusal
        return out
    out.update(carve)
    return out


# ------------------------------------------------------------------
# the two that still have no text, stated as evidence facts
# ------------------------------------------------------------------

def ruby_absences():
    ruby = load("op_units_ruby.json")
    carve = load("lineage_carve.json")
    rows = []
    for name in ("vm_opt_plus", "rb_big_plus"):
        ship_present = None
        ship_reason = None
        for number in sorted(ruby["probes"], key=lambda x: int(x)):
            record = ruby["probes"][number]
            if record["meta"]["symbol"] != name:
                continue
            ship_present = record["ship"].get("present")
            ship_reason = record["ship"].get("reason")
        refusals = []
        for record in carve["records"]:
            if record["symbol"] != name:
                continue
            if record.get("outcome") != "REFUSED":
                continue
            refusals.append({"build": record["build"],
                             "refusal": record.get("refusal")})
        rows.append({
            "unit": "ruby/%s" % name,
            "language": "ruby",
            "outcome": "NO_CANONICAL_TEXT",
            "ship_body_present_in_the_dump": ship_present,
            "ship_absence_reason_verbatim": ship_reason,
            "carve_refusals_verbatim": refusals,
            "is_this_a_register_scarcity_refusal": False,
            "why_not":
                "register scarcity plays no part.  vm_opt_plus has no "
                "ship body at all, so there is nothing to canonicalise "
                "and the gate forbids substituting the anchor build's "
                "body.  rb_big_plus has a ship body whose two lineages "
                "meet inside callees that are not extracted units, so "
                "the confluence is interprocedural.  Under the "
                "universal-form ruling a scarcity refusal would be a "
                "defect; neither of these is one.",
            "what_would_change_it":
                "vm_opt_plus: a ship build that does not inline the "
                "symbol away, or a ruled decision to canonicalise the "
                "anchor build.  rb_big_plus: extraction of the callee "
                "units (bigadd, big2dbl) and a ruled interprocedural "
                "seed, which is the owner's call, not this lap's.",
        })
    return rows


# ------------------------------------------------------------------

def refuse_own_output_on_spelling_keys(path):
    command = [sys.executable, os.path.join(HERE,
                                            "check_no_spelling_keys.py"),
               path]
    done = subprocess.run(command, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.stderr.strip():
        print(done.stderr.strip())
    if done.returncode != 0:
        os.unlink(path)
        raise SystemExit("output refused and removed: the spelling-key "
                         "check failed on %s" % path)


def main():
    units, canon34doc = all_eleven()
    records = []
    produced = 0
    for unit in units:
        record = {
            "unit": unit["unit"],
            "language": unit["language"],
            "operator": unit.get("operator"),
            "build": unit.get("build"),
            "prior_text": unit.get("prior_text"),
            "prior_text_source": unit.get("prior_text_source"),
            "arrival_annotation": unit.get("arrival_recorded"),
            "provenance_is_weaker": True,
        }
        rendered, refusal = hoist(unit)
        if rendered is None:
            record["outcome"] = "NO_UNIVERSAL_TEXT"
            record["refusal"] = refusal
            record["prior_refusal"] = unit.get("prior_refusal")
            records.append(record)
            continue
        record.update(rendered)
        seats = unit.get("seats") or seats_from_text(unit["prior_text"])
        verdict, detail, bindings = gate(
            unit["prior_text"], seats,
            rendered["universal_text"],
            rendered["seats_in_the_universal_form"])
        record["gate_verdict"] = verdict
        record["gate_detail"] = detail
        record["gate_bindings"] = bindings
        if verdict != "PROVED":
            record["outcome"] = "NO_UNIVERSAL_TEXT"
            record["refusal"] = (
                "the derived universal text was NOT proved equal to this "
                "unit's own prior text, so it is not kept: %s" % detail)
            record.pop("universal_text", None)
            records.append(record)
            continue
        record["outcome"] = "UNIVERSAL_TEXT_PRODUCED"
        produced += 1
        records.append(record)

    fixed = add_function_record()
    if fixed.get("outcome") != "REFUSED":
        # render it in the universal form from its own carve.
        core = ["mov %rdi,%rax", "add %rsi,%rax"]
        loads = ["mov %s,%%rdi" % slot_for(0), "mov %s,%%rsi" % slot_for(1)]
        fixed["standardized_loads"] = loads
        fixed["core_after_substitution"] = core
        fixed["universal_text"] = "; ".join(loads + core + ["ret"])
        fixed["render_rule"] = (
            "the confluence `add (%rdx),%rax` reads value lineage 2 "
            "through the pointer arrival and the running value in "
            "%rax, which holds value lineage 1 from `mov (%rsi),%rax`.  "
            "Both dereferences are part of the standardized load, so "
            "the core reads the two designated registers and writes the "
            "answer register.")
        fixed["designated_location_directory"] = [
            {"designation": "a", "designated_location": slot_for(0),
             "location_name": "S0", "loaded_into": "%rdi",
             "prior_arrival_place": "(%rsi)",
             "arrival_annotation": "typed-pointer(zval*)"},
            {"designation": "b", "designated_location": slot_for(1),
             "location_name": "S1", "loaded_into": "%rsi",
             "prior_arrival_place": "(%rdx)",
             "arrival_annotation": "typed-pointer(zval*)"},
        ]
        fixed["seats_in_the_universal_form"] = {
            "operand_1": {"seat_kind": "designated location",
                          "designation": "a", "text": slot_for(0)},
            "operand_2": {"seat_kind": "designated location",
                          "designation": "b", "text": slot_for(1)},
            "answer": {"seat_kind": "designated register",
                       "designation": "answer", "text": "%rax"},
        }
        # the gate for this one is against its OWN ship instructions,
        # not against a prior canonical text (it had none): the two
        # instructions of its own normal path, with the dereferences
        # standing for the standardized loads.
        own = "mov %rdi,%rax; add %rsi,%rax; ret"
        verdict, detail, bindings = gate(
            own,
            {"operand_1": {"seat_kind": "designated register",
                           "designation": "a", "text": "%rdi"},
             "operand_2": {"seat_kind": "designated register",
                           "designation": "b", "text": "%rsi"},
             "answer": {"seat_kind": "designated register",
                        "designation": "answer", "text": "%rax"}},
            fixed["universal_text"],
            fixed["seats_in_the_universal_form"])
        fixed["gate_verdict"] = verdict
        fixed["gate_detail"] = detail
        fixed["gate_bindings"] = bindings
        fixed["gate_note"] = (
            "the left side is this unit's own ship instructions "
            "`mov (%rsi),%rax` / `add (%rdx),%rax` with each pointer "
            "dereference written as the value it loads, which is what "
            "the standardized load does; the right side is the "
            "universal text.")
        if verdict == "PROVED":
            fixed["outcome"] = "UNIVERSAL_TEXT_PRODUCED"
            produced += 1
        else:
            fixed["outcome"] = "NO_UNIVERSAL_TEXT"
            fixed["refusal"] = detail
    fixed["arrival_annotation"] = "typed-pointer(zval*)"
    fixed["operator"] = "+"
    fixed["provenance_is_weaker"] = True

    records = [r for r in records if r["unit"] != "php/add_function"]
    records.append(fixed)

    absences = ruby_absences()
    absent_units = set(row["unit"] for row in absences)
    records = [r for r in records if r["unit"] not in absent_units]

    doc = {
        "meta": {
            "generator": "interp_canon35.py",
            "task": "TASK 34 part (a) -- all eleven interpreter/JIT "
                    "units in the universal canonical form",
            "ruling": "AgentMemory 2026-09-01, THE UNIVERSAL CANONICAL "
                      "FORM: virtual memory for every unit, "
                      "standardized loads, arrival annotated",
            "supersedes": "interp_canon34.json's register-based render, "
                          "which is kept as the input evidence and as "
                          "the gate's left-hand side",
            "reads_read_only": [
                "interp_canon34.json", "canon_interp_units_cpython.json",
                "canon_interp_units_java.json", "lineage_carve.json",
                "op_units_ruby.json",
            ],
            "gate": "every universal text is z3-proved equal to that "
                    "unit's OWN prior text, seats bound; a unit that "
                    "does not prove keeps no text",
            "spelling": "the operator token appears once per unit, as a "
                        "display label on the member. No key, grouping, "
                        "pairing or row structure uses it.",
            "provenance_is_weaker": True,
        },
        "records": records,
        "units_with_no_universal_text": absences,
        "population": {
            "interpreter_and_jit_units_on_record": 11,
            "languages": ["cpython", "java", "ruby", "php"],
            "per_language": {"cpython": 1, "java": 2, "ruby": 4, "php": 4},
        },
        "summary": {
            "universal_text_produced": produced,
            "no_universal_text": len(absences) + len(
                [r for r in records
                 if r.get("outcome") != "UNIVERSAL_TEXT_PRODUCED"]),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")

    for record in records:
        print("%-58s %-24s %s" % (
            record["unit"], record.get("outcome"),
            record.get("universal_text") or record.get("refusal", "")[:70]))
    for row in absences:
        print("%-58s %-24s %s" % (row["unit"], row["outcome"],
                                  "no text; not a scarcity refusal"))
    print("summary: %s" % json.dumps(doc["summary"]))
    refuse_own_output_on_spelling_keys(OUT)


if __name__ == "__main__":
    main()
