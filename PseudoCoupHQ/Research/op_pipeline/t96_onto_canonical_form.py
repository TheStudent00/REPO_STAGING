#!/usr/bin/env python3
"""t96_onto_canonical_form.py -- THE ELEVEN INTERPRETER UNITS PUT ON
THE CANONICAL FORM.

TASK 96, round 19.  The correction this implements, quoted from
`CORE_0_3_5_2_canonical_form.md`, heading "the form, as the owner meant it
-- CORRECTION 2026-09-05":

    "The arch-unit is essentially UNCHANGED except for the loading and
    unloading of registers into a virtual memory."  ...  "`region36.py`
    quotes the 2026-09-02 ruling and implements it as: rewrite EVERY
    location in the body as `0x<offset>(%r15)`.  That requires one
    register to hold a fixed base for a whole body, which is where the
    `%r15` collision comes from."  ...  "`canonical_form.py` (canon40)
    wraps rather than rewrites.  Loads at the front, body verbatim, a
    store at the back, addressed rip-relative through the ledger."

So this program renders each of the eleven THREE ways and gates each,
and prints them side by side.  It DECIDES NOTHING: the form is
`canonical_form.py`'s, the gate is `gate.py`'s, the bodies are the
ones task 94 read off the symbol table and DWARF.

    FORM 1, the superseded record.  `region36` + `canon36_universal`,
            as task 94 rendered it.  READ from `t94_recarve.json`,
            never re-run: those two files are superseded records and
            are not imported, edited or executed by this program.

    FORM 2, PART A.  `canonical_form.CanonicalForm.wrap`, unmodified,
            over the re-carved body.  Prelude in arrival-contract
            order, body verbatim, epilogue into OUT-0.

    FORM 3, PART B.  The same, plus the seventh block kind of
            `t96_arriving_area.py` -- an arriving addressable area.

WHAT IS NOT TOUCHED.  `canonical_form.py`, `ledger.py`, `gate.py`,
`region36.py`, `canon36_universal.py`, `reference.py` are IMPORTED OR
READ, never edited.  The eleven bodies are taken character-for-
character from `t94_recarve.json` and `t94_bounds.json`.  NO BODY IS
NARROWED: the function-body boundary is the owner's ruling of 2026-09-05 and
is not this task's to touch.

WHY `wrap` IS OVERRIDDEN RATHER THAN `canonical_form.py` EDITED.
`CanonicalForm.wrap` builds `ledger.Ledger` and `Prelude` by name, so
the seventh block cannot be reached without either editing that file
or overriding the method.  Editing it would put a second, task-shaped
rule inside the node's own code; overriding it here keeps that file
exactly as the node ratified it.  The override calls the SAME
`self.labels`, the SAME `Epilogue`, and the SAME `ledger.weave`; only
the prelude and the ledger object differ, which is precisely what the
seventh block kind is.

TIME AND MEMORY.
  * Every gate is asked at 20,000 ms and re-asked at 120,000 ms if and
    only if the first answer was UNDECIDED FOR TIME.  Task 91 measured
    that the longer run turns some UNDECIDED into DISPROVED and never
    into a proof, so a slow unit gets the longer run before its
    verdict is recorded.
  * MEMORY BOUND: 6 GB, aborting by the name `T96_MEMORY_ABORT`.  The
    peak resident size is printed at the end of the run.

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

The member's display label travels on the field `label` and is read by
nothing.  Nothing here is keyed, grouped, paired or selected by it: the
population is the eleven records of `t94_recarve.json`, in that file's
own order.

Coding discipline: no compound one-liner statements.

usage:
  t96_onto_canonical_form.py            writes t96_canonical.json
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon as CANON                                             # noqa: E402
import canonical_form as CF                                       # noqa: E402
import gate as GATE                                               # noqa: E402
import ledger as L                                                # noqa: E402
import t96_arriving_area as AREA                                  # noqa: E402


SHORT_TIMEOUT_MS = 20000
LONG_TIMEOUT_MS = 120000
MEMORY_CAP_KB = 6 * 1024 * 1024
MEMORY_ABORT = "T96_MEMORY_ABORT"

RECARVE = os.path.join(HERE, "t94_recarve.json")
BOUNDS = os.path.join(HERE, "t94_bounds.json")
OUT = os.path.join(HERE, "t96_canonical.json")


def check_memory(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > MEMORY_CAP_KB:
        raise MemoryError(
            "%s: peak resident size %d kB passed the stated 6 GB bound "
            "at %s" % (MEMORY_ABORT, peak, where))
    return peak


# ------------------------------------------------------------------
# the arch-unit facts, read from records
# ------------------------------------------------------------------

def read_bodies():
    """label -> the re-carved body and its bytes.

    The body is `t94_recarve.json`'s `recarved.body_verbatim`, which is
    objdump's own text for the function's own bounds.  The bytes are
    `t94_bounds.json`'s per-instruction `bytes`, concatenated -- the
    same instructions, as the same file recorded them.  A JIT nmethod
    has no `t94_bounds.json` record, so it has no bytes, and
    `ledger.positional_labels` then leaves every transfer exactly as
    the disassembler wrote it.
    """
    recarve = json.load(open(RECARVE))
    bounds = json.load(open(BOUNDS))
    bytes_of = {}
    for record in bounds["records"]:
        body = record.get("body")
        if not body:
            continue
        pieces = []
        for line in body:
            pieces.append(line["bytes"].replace(" ", ""))
        bytes_of[record["unit"]] = "".join(pieces)
    out = []
    for record in recarve["records"]:
        carved = record.get("recarved") or {}
        out.append({
            "unit": record["unit"],
            "label": record.get("label"),
            "language": record.get("language"),
            "handler_function": record.get("handler_function"),
            "body_verbatim": carved.get("body_verbatim"),
            "body_bytes": bytes_of.get(record["unit"]),
            "arrival_contract": record.get("arrival_contract") or {},
            "old_form": old_form_of(record),
            "old_verdict": record.get("new_verdict"),
            "old_verdict_cause": record.get("cause"),
        })
    return out


def old_form_of(record):
    """FORM 1 as task 94 recorded it -- read, never re-run."""
    universal = record.get("universal_form") or {}
    text = universal.get("universal_text")
    if text:
        return {
            "outcome": "RENDERED",
            "wrapped_text": text,
            "region_base": universal.get("region_base"),
            "region_size": universal.get("region_size"),
            "block_counts": universal.get("block_counts"),
        }
    return {
        "outcome": "REFUSED",
        "wrapped_text": None,
        "refusal": record.get("cause"),
    }


def contract_families(contract):
    """the arrival contract's own families, in its own order."""
    out = []
    for key in ("a", "b", "c", "d", "e", "f", "g", "h"):
        family = contract.get(key)
        if family:
            out.append(family)
    return out


# ------------------------------------------------------------------
# FORM 3 -- the canonical form with the seventh block kind
# ------------------------------------------------------------------

class AreaRow(object):
    """what `Ledger.walk_dataflow` needs of a row: a name.  An AREA
    row is a dict on `AreaLedger`, not a `ledger.Row`, because its
    size is an extent rather than a value's width."""

    def __init__(self, record):
        self.record = record
        self.size = record["size"]
        self.offset = record["offset"]

    def name(self):
        return self.record["row"]


class AreaPrelude(object):
    """`canonical_form.Prelude` with one branch added: an arrival that
    is an AREA gets its base, not its value.

    Everything else is `canonical_form.Prelude`'s own code, reached by
    delegation rather than copied.
    """

    def __init__(self, ledger, areas):
        self.ledger = ledger
        self.inner = CF.Prelude(ledger)
        self.areas = {}
        for record in areas:
            self.areas[record["base_family"]] = record

    def emit(self, arrival_families):
        literal = []
        resolved = []
        rows = []
        general = []
        any_vector = False
        for family in arrival_families:
            if family in self.areas:
                continue
            if L.is_vector_family(family):
                any_vector = True
            else:
                general.append(family)
        scratch = None
        if any_vector:
            reserved = set(general) | set(CANON.NEVER_RENAME)
            scratch = L.pick_scratch(reserved)
        for family in arrival_families:
            if family in self.areas:
                record = self.areas[family]
                row = self.ledger.add_area(
                    family, record["displacements"])
                rows.append(AreaRow(row))
                pair, one = AREA.area_prelude_lines(row, family)
                literal.extend(pair)
                resolved.append(one)
                continue
            row = self.inner.add_row(family)
            rows.append(row)
            if L.is_vector_family(family):
                pair, one = self.inner.emit_vector_row(row, family,
                                                       scratch)
            else:
                pair, one = self.inner.emit_general_row(row, family)
            literal.extend(pair)
            resolved.append(one)
        return literal, resolved, rows, scratch


class AreaForm(CF.CanonicalForm):
    """`CanonicalForm` with the seventh block kind.

    `wrap` is OVERRIDDEN, not re-implemented: it is the parent's own
    sequence with `ledger.Ledger` replaced by `t96_arriving_area
    .AreaLedger` and `Prelude` by `AreaPrelude`.  `self.labels`, the
    `Epilogue` and `ledger.weave` are the parent's.
    """

    block_order = tuple(list(CF.CanonicalForm.block_order)
                        + [AREA.AREA_BLOCK])

    def wrap(self, body_text, arrival_families, result_family,
             result_width, body_bytes=None, label=None,
             toolchain=None, areas=None):
        if not body_text:
            raise L.Refusal(
                "no text",
                "no text exists for this unit, so there is no body to "
                "wrap")
        ledger = AREA.AreaLedger(
            runtime_routines=self.runtime_routines,
            runtime_answers=self.runtime_answers,
            toolchain=toolchain)
        prelude = AreaPrelude(ledger, areas or [])
        epilogue = CF.Epilogue(ledger)
        body_as_read = L.split_lines(body_text)
        for raw in body_as_read:
            line = L.R36.strip_annotation(raw)
            if L.LEDGER_SYMBOL in line:
                raise L.Refusal(
                    "the body names the ledger symbol",
                    "the body spells %r, which would collide with the "
                    "form's own symbol" % L.LEDGER_SYMBOL)
        body, label_record = self.labels.rewrite(body_as_read,
                                                 body_bytes)
        prelude_literal, prelude_resolved, arrival_rows, \
            prelude_scratch = prelude.emit(arrival_families)
        where, holes = ledger.walk_dataflow(body, arrival_rows,
                                            arrival_families)
        producer = "the body's last write to %%%s" % result_family
        operands = []
        if result_family in where:
            answer_row = where[result_family]
            operands = [answer_row]
            source_row = ledger.by_row.get(answer_row)
            if source_row is not None:
                producer = source_row.produced_by
        epilogue_literal, epilogue_resolved, out_row, \
            epilogue_scratch = epilogue.emit(result_family,
                                             result_width, producer,
                                             operands)
        literal_lines, returns = epilogue.place(body, prelude_literal,
                                                epilogue_literal)
        resolved_lines, _ = epilogue.place(body, prelude_resolved,
                                           epilogue_resolved)
        self.wrapped_text = "; ".join(literal_lines)
        fields = {
            "wrapped_text": self.wrapped_text,
            "wrapped_text_resolved": "; ".join(resolved_lines),
            "body_verbatim": list(body),
            "body_as_read": list(body_as_read),
            "branch_labels": label_record,
            "prelude": prelude_literal,
            "prelude_resolved": prelude_resolved,
            "epilogue": epilogue_literal,
            "epilogue_resolved": epilogue_resolved,
            "prelude_scratch": prelude_scratch,
            "epilogue_scratch": epilogue_scratch,
            "returns": returns,
            "ledger": ledger.as_list(),
            "ledger_block_bytes": ledger.block_bytes(),
            "ledger_symbol": L.LEDGER_SYMBOL,
            "ledger_entries": list(self.block_order),
            "out_row": out_row.name(),
            "arrival_families": list(arrival_families),
            "result_family": result_family,
            "result_width": result_width,
            "producer_holes": holes,
            "transfer_shapes": list(ledger.transfer_shapes),
            "form": "canonical_form + the seventh block kind",
            "addressing": "two steps for a value that arrives (block "
                          "base, then the row); ONE step for an area "
                          "that arrives (the block base IS the "
                          "address the body reaches through), plus a "
                          "`lea` where the extent moves the base",
        }
        fields["arrival_contract_bindings"] = self.area_bindings(
            arrival_families, arrival_rows)
        return fields

    def area_bindings(self, arrival_families, arrival_rows):
        out = []
        for index, family in enumerate(arrival_families):
            row = arrival_rows[index]
            entry = {
                "row": row.name(),
                "bound_to_the_same_symbol_as": "%" + family,
                "size": row.size,
            }
            if isinstance(row, AreaRow):
                entry["kind"] = "an arriving addressable area"
                entry["what_the_register_holds_at_entry"] = (
                    "the area's own base address, so the body's own "
                    "displacements reach the same bytes they always "
                    "did")
            else:
                entry["kind"] = "one value that arrives"
            out.append(entry)
        return out


# ------------------------------------------------------------------
# the gate, at two limits
# ------------------------------------------------------------------

def timed_out(verdict):
    if verdict.outcome != GATE.UNDECIDED:
        return False
    return "did not answer inside its" in (verdict.reason or "")


def gate_twice(fields, record):
    """the gate at 20,000 ms, and again at 120,000 ms if and only if
    the first answer was UNDECIDED FOR TIME."""
    wanted = dict(record)
    wanted.update(fields)
    short = GATE.Gate(solver_timeout_ms=SHORT_TIMEOUT_MS)
    first = short.prove_wrapped(fields["wrapped_text"], wanted)
    out = {
        "gate_at_20000ms": {
            "verdict": first.outcome,
            "detail": first.reason,
            "route": first.route,
        },
        "verdict": first.outcome,
        "verdict_detail": first.reason,
        "verdict_route": first.route,
        "solver_timeout_ms": first.solver_timeout_ms,
        "answer_changed_with_more_room": False,
    }
    if first.counterexample is not None:
        out["counterexample"] = first.counterexample
    if not timed_out(first):
        out["gate_at_120000ms"] = {
            "verdict": "NOT_RUN",
            "detail": "the 20,000 ms run did not hit its time limit, "
                      "so the longer run would ask the same solver "
                      "the same question",
        }
        return out
    longer = GATE.Gate(solver_timeout_ms=LONG_TIMEOUT_MS)
    second = longer.prove_wrapped(fields["wrapped_text"], wanted)
    out["gate_at_120000ms"] = {
        "verdict": second.outcome,
        "detail": second.reason,
        "route": second.route,
    }
    out["verdict"] = second.outcome
    out["verdict_detail"] = second.reason
    out["verdict_route"] = second.route
    out["solver_timeout_ms"] = second.solver_timeout_ms
    out["answer_changed_with_more_room"] = (
        second.outcome != first.outcome)
    if second.counterexample is not None:
        out["counterexample"] = second.counterexample
    return out


# ------------------------------------------------------------------
# the three renderings, per unit
# ------------------------------------------------------------------

def render_form_two(form, unit):
    """PART A -- `canonical_form.CanonicalForm.wrap`, unmodified."""
    families = contract_families(unit["arrival_contract"])
    contract = unit["arrival_contract"]
    base = {
        "form": "canonical_form.py, unmodified",
        "arrival_families": list(families),
    }
    if not unit["body_verbatim"]:
        base["outcome"] = "REFUSED"
        base["refusal_cause"] = "no canonical text"
        base["refusal"] = "this handler has no ship body to wrap"
        return base
    try:
        fields = form.wrap(
            "; ".join(unit["body_verbatim"]), families,
            contract.get("result"), contract.get("result_width"),
            body_bytes=unit["body_bytes"], label=unit["unit"])
    except L.Refusal as bad:
        base["outcome"] = "REFUSED"
        base["refusal_cause"] = bad.cause
        base["refusal"] = bad.detail
        return base
    base.update(fields)
    base["outcome"] = "WRAPPED"
    base.update(gate_twice(fields, base))
    return base


def render_form_three(form, unit):
    """PART B -- the same, plus the seventh block kind."""
    contract = unit["arrival_contract"]
    base = {"form": "canonical_form.py + t96_arriving_area.py"}
    if not unit["body_verbatim"]:
        base["outcome"] = "REFUSED"
        base["refusal_cause"] = "no canonical text"
        base["refusal"] = "this handler has no ship body to wrap"
        return base
    areas = AREA.read_arriving_areas(unit["body_verbatim"])
    base["arriving_areas"] = areas
    area_families = []
    for record in areas:
        area_families.append(record["base_family"])
    families = []
    for family in contract_families(contract):
        families.append(family)
    for family in area_families:
        if family in families:
            continue
        families.append(family)
    base["arrival_families"] = list(families)
    base["value_arrivals"] = AREA.value_arrivals(
        unit["body_verbatim"], areas, contract_families(contract))
    try:
        fields = form.wrap(
            "; ".join(unit["body_verbatim"]), families,
            contract.get("result"), contract.get("result_width"),
            body_bytes=unit["body_bytes"], label=unit["unit"],
            areas=areas)
    except AREA.AreaRefusal as bad:
        base["outcome"] = "REFUSED"
        base["refusal_cause"] = bad.cause
        base["refusal"] = bad.detail
        return base
    except L.Refusal as bad:
        base["outcome"] = "REFUSED"
        base["refusal_cause"] = bad.cause
        base["refusal"] = bad.detail
        return base
    base.update(fields)
    base["outcome"] = "WRAPPED"
    base.update(gate_twice(fields, base))
    return base


# ------------------------------------------------------------------
# the three shortfalls log_199 flagged, asked per unit
# ------------------------------------------------------------------

def shortfalls(unit, form_two, form_three):
    """log_199 section 3.2's three shortfalls, asked of THIS unit under
    the corrected form.  Each answer carries the fact that decides it,
    not an opinion."""
    body = unit["body_verbatim"] or []
    out = {}

    # 1 -- the %r15 collision
    names_r15 = False
    for line in body:
        if "%r15" in line:
            names_r15 = True
            break
    text_two = form_two.get("wrapped_text")
    claimed = False
    if text_two is not None:
        # the form claims a register when the FORM's own lines write
        # it; the prelude and the epilogue are the form's own lines.
        for line in (form_two.get("prelude") or []) + \
                (form_two.get("epilogue") or []):
            if "%r15" in line:
                claimed = True
                break
    out["the_r15_collision"] = {
        "the_body_names_r15": names_r15,
        "the_form_claims_r15": claimed,
        "gone": (form_two.get("outcome") == "WRAPPED"
                 and not claimed),
        "why": "under region36 the form itself owned %r15 as the "
               "region base, so a body naming it was refused BY NAME. "
               "canonical_form.py names no region base: the ledger is "
               "at an absolute address, reached rip-relative, and the "
               "form's own lines here name %r15 only if the unit's own "
               "arrival contract does",
    }

    # 2 -- no block kind for memory the unit obtains at run time
    obtained = AREA.read_obtained_memory(body)
    out["memory_obtained_at_run_time"] = {
        "sightings": len(obtained),
        "first_three": obtained[:3],
        "gone": form_two.get("outcome") == "WRAPPED",
        "why": "the region form had to give every byte the body "
               "touches a block, because it REWROTE every location "
               "into the region. the canonical form rewrites nothing: "
               "the body's own store through a pointer it obtained "
               "stays exactly as the compiler wrote it, and the answer "
               "is read out of the unit's own answer home by the "
               "epilogue, not off a result block",
    }

    # 3 -- an input block holds a pointer, not the object it addresses
    areas = form_three.get("arriving_areas") or []
    out["an_input_block_holds_a_pointer"] = {
        "arriving_areas_found": len(areas),
        "bases": ["%" + a["base_family"] for a in areas],
        "gone": (form_three.get("outcome") == "WRAPPED"
                 and len(areas) > 0),
        "not_applicable": len(areas) == 0,
        "why": "the seventh block kind gives an arriving pointer's "
               "OBJECT a block of its own -- an addressable extent the "
               "body reaches into at its own displacements -- instead "
               "of an input row holding the pointer's value. where a "
               "body dereferences no arriving register there is "
               "nothing for this shortfall to be about",
    }
    return out


# ------------------------------------------------------------------
# the driver
# ------------------------------------------------------------------

def main():
    units = read_bodies()
    plain = CF.new_form()
    area_form = AreaForm(
        runtime_routines=plain.runtime_routines,
        unattached_callers=plain.unattached_callers,
        runtime_answers=plain.runtime_answers)
    records = []
    total = len(units)
    for index, unit in enumerate(units):
        sys.stderr.write("[%d/%d] %s\n" % (index + 1, total,
                                           unit["unit"]))
        sys.stderr.flush()
        form_two = render_form_two(plain, unit)
        check_memory("form two, %s" % unit["unit"])
        form_three = render_form_three(area_form, unit)
        check_memory("form three, %s" % unit["unit"])
        records.append({
            "unit": unit["unit"],
            "label": unit["label"],
            "language": unit["language"],
            "handler_function": unit["handler_function"],
            "body_instruction_count":
                len(unit["body_verbatim"] or []) or None,
            "body_bytes_were_read": unit["body_bytes"] is not None,
            "arrival_contract": unit["arrival_contract"],
            "the_superseded_form": unit["old_form"],
            "the_superseded_verdict": unit["old_verdict"],
            "the_superseded_cause": unit["old_verdict_cause"],
            "the_canonical_form": form_two,
            "the_canonical_form_with_the_seventh_block":
                form_three,
            "the_three_shortfalls": shortfalls(unit, form_two,
                                               form_three),
        })
    peak = check_memory("the end of the run")
    document = {
        "meta": {
            "generator": "t96_onto_canonical_form.py",
            "task": "TASK 96 round 19 -- the eleven interpreter units "
                    "onto the canonical form, and the seventh block "
                    "kind",
            "correction":
                "CORE_0_3_5_2_canonical_form.md, 'the form, as the owner "
                "meant it -- CORRECTION 2026-09-05' and 'the seventh "
                "block kind -- an arriving addressable area'",
            "form_one": "region36 + canon36_universal, READ from "
                        "t94_recarve.json and never re-run; those two "
                        "files are superseded records",
            "form_two": "canonical_form.CanonicalForm.wrap, "
                        "unmodified",
            "form_three": "the same, plus t96_arriving_area.py's "
                          "seventh block kind",
            "gate": "gate.py Gate.prove_wrapped against the unit's "
                    "OWN ship body, at 20,000 ms and again at "
                    "120,000 ms when the first answer was undecided "
                    "for time",
            "boundary": "the owner's ruling of 2026-09-05: the unit is a "
                        "function body. No body was narrowed.",
            "memory_bound_kB": MEMORY_CAP_KB,
            "memory_abort_name": MEMORY_ABORT,
            "peak_resident_size_kB": peak,
            "spelling": "the member's display label travels on the "
                        "field `label`; no key, grouping, pairing, row "
                        "structure or selection in this file uses it",
        },
        "records": records,
        "verdict_movements": movements(records),
        "summary": summary(records),
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s" % OUT)
    print("peak resident size kB: %d" % peak)
    for row in document["verdict_movements"]:
        print("%-58s %-18s -> %-22s | %s"
              % (row["unit"], row["from"], row["to_form_two"],
                 row["to_form_three"]))
    print(json.dumps(document["summary"], indent=1, sort_keys=True))
    return 0


def verdict_of(rendering):
    if rendering.get("outcome") == "REFUSED":
        return "REFUSED: %s" % rendering.get("refusal_cause")
    return rendering.get("verdict") or rendering.get("outcome")


def movements(records):
    out = []
    for record in records:
        out.append({
            "unit": record["unit"],
            "from": record["the_superseded_verdict"],
            "from_cause": record["the_superseded_cause"],
            "to_form_two": verdict_of(record["the_canonical_form"]),
            "to_form_two_cause":
                record["the_canonical_form"].get("verdict_detail")
                or record["the_canonical_form"].get("refusal"),
            "to_form_three": verdict_of(
                record["the_canonical_form_with_the_seventh_block"]),
            "to_form_three_cause":
                record["the_canonical_form_with_the_seventh_block"]
                .get("verdict_detail")
                or record["the_canonical_form_with_the_seventh_block"]
                .get("refusal"),
        })
    return out


def summary(records):
    two = {}
    three = {}
    gone = {"the_r15_collision": 0,
            "memory_obtained_at_run_time": 0,
            "an_input_block_holds_a_pointer": 0}
    for record in records:
        key = verdict_of(record["the_canonical_form"])
        two[key] = two.get(key, 0) + 1
        key = verdict_of(
            record["the_canonical_form_with_the_seventh_block"])
        three[key] = three.get(key, 0) + 1
        for name in gone:
            if record["the_three_shortfalls"][name]["gone"]:
                gone[name] = gone[name] + 1
    return {
        "population": len(records),
        "form_two_verdicts": two,
        "form_three_verdicts": three,
        "shortfalls_gone_per_unit": gone,
    }


if __name__ == "__main__":
    sys.exit(main())
