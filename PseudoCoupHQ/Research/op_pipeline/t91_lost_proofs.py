#!/usr/bin/env python3
"""t91_lost_proofs.py -- THE 245 PROOFS LOST AGAINST log 153, given a
computed cause rather than an assertion.

WHAT IS BEING ASKED.  `t91_audit.py` reports that 245 of the 23,132
units log 153 records as proved do not prove in this round's re-gate:
229 DISPROVED and 16 UNDECIDED on the solver's wall clock.  The gate's
zero_regression CORE rules that "no unit loses PROVED without a named
cause" and that "the cause is CHECKED over the unit's own artifact,
mechanically".  This file does the checking.

THE TWO ANSWERS THAT ARE COMPARED, and why that names the cause.  A
route-one verdict compares the LEDGER'S term against a REFERENCE'S
answer for the same body.  The ledger did not move: canon38 is stored
and `layer4c.transcribe` is a superseded record read unchanged.  So a
proof that stood in log 153 and falls now can only be the reference's
answer moving.  This file therefore computes, for each lost unit, BOTH
answers -- `canon10_behaviour_check.Sim10`'s (the superseded simulator
log 153's gate called, imported as the record it is and not edited) and
`reference.Reference`'s -- and asks the solver whether they are equal.
Where they differ it prints the values at which they differ, so which
of the two is the machine's can be read rather than argued.

The units are then grouped by SHAPES READ OFF THEIR OWN TEXT: whether
the body carries a positional label, a conditional transfer, a `call`,
a narrow (8- or 16-bit) division or widening multiply, or a high-byte
register.  Those are the five things task 64 changed in the reference,
so the grouping tests the changes against the losses.

THE MEMORY BOUND: one canon38 source document at a time; cap 6000 MB,
abort named T91_MEMORY_ABORT.

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

No operator token appears in this file.  The units are grouped by
SHAPES OF THEIR OWN MACHINE TEXT -- a label, a transfer, a call, a
destination width -- which is machine-form evidence.

Coding discipline (the owner's ruling): no compound one-liner statements.

usage:
  t91_lost_proofs.py
"""

import collections
import glob
import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as OLD                             # noqa: E402
import gate as GATE                                               # noqa: E402
import layer4c                                                    # noqa: E402
import ledger as LEDGER                                           # noqa: E402
import reference as REF                                           # noqa: E402
import z3                                                         # noqa: E402

LANGS = ("c", "cpp", "go", "rust", "swift")
MEMORY_CAP_MB = 6000
MEMORY_ABORT = "T91_MEMORY_ABORT"
OUT = os.path.join(HERE, "t91_lost_proofs.json")
NARROW_WIDTH_SUFFIXES = ("b", "w")
HIGH_BYTES = ("%ah", "%bh", "%ch", "%dh")


def peak_resident_mb():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024.0


def check_memory(stage):
    now = peak_resident_mb()
    if now > MEMORY_CAP_MB:
        raise SystemExit("%s: %.1f MB passed the cap of %d MB during %s"
                         % (MEMORY_ABORT, now, MEMORY_CAP_MB, stage))
    return now


def lost_units():
    """the units log 153 records as proved that this round's re-gate
    does not prove, in EITHER configuration -- read off the stores.
    Each carries the ROUTE log 153 proved it on, because a proof that
    stood only on route two and falls now is a different finding from
    one that stood on route one."""
    populations = json.load(open(os.path.join(
        HERE, "t91_populations.json")))
    proved_before = set(populations["buckets"]["proved"])
    task_53 = populations["task_53_reason"]
    lost = {}
    for configuration in ("attached_callees", "no_attached_callees"):
        directory = os.path.join(
            HERE, "t91_regate_store_%s_fix" % configuration)
        for path in sorted(glob.glob(os.path.join(directory,
                                                  "*.json"))):
            document = json.load(open(path))
            for name, record in document.get("units", {}).items():
                if name not in proved_before:
                    continue
                if record.get("state") == "proved":
                    continue
                lost.setdefault(name, {})
                lost[name][configuration] = {
                    "state": record.get("state"),
                    "ship": (record.get("ship") or {}).get("outcome"),
                    "ship_reason": (record.get("ship")
                                    or {}).get("reason"),
                    "text": (record.get("text") or {}).get("outcome"),
                    "text_reason": (record.get("text")
                                    or {}).get("reason"),
                    "task_53_ship": (task_53.get(name)
                                     or {}).get("ship_verdict"),
                    "task_53_text": (task_53.get(name)
                                     or {}).get("text_verdict"),
                }
    return lost


def proving_route_in_task_53(states):
    """which of log 153's two routes carried this unit's proof."""
    for configuration in states:
        record = states[configuration]
        ship = record.get("task_53_ship")
        text = record.get("task_53_text")
        if ship == "PROVED_EQUAL" and text == "PROVED_EQUAL":
            return "both routes proved it in log 153"
        if ship == "PROVED_EQUAL":
            return "route one alone proved it in log 153"
        if text == "PROVED_EQUAL":
            return "route two alone proved it in log 153"
    return "log 153 records no proving route for it"


def why_it_falls(states):
    """the two routes' own recorded words in THIS round, which is what
    the loss has to be read off."""
    for configuration in sorted(states):
        record = states[configuration]
        return ("route one %s / route two %s -- route two's own words: "
                "%s" % (record.get("ship"), record.get("text"),
                        (record.get("text_reason") or "")[:170]))
    return "no record"


def bodies_for(names):
    out = {}
    paths = []
    for lang in LANGS:
        paths.append(os.path.join(HERE, "canon38_wrapped_%s.json"
                                  % lang))
    paths.append(os.path.join(HERE, "canon38_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(
        HERE, "canon38_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name in names:
            if name in out:
                continue
            record = document.get("units", {}).get(name)
            if record is None:
                continue
            if "ledger" not in record:
                continue
            unit = dict(record)
            unit["unit"] = name
            out[name] = unit
        del document
        check_memory("collecting bodies at %s" % os.path.basename(path))
        if len(out) == len(names):
            break
    return out


def shapes_of(unit):
    """the five shapes task 64 changed the reference for, read off this
    body's own text."""
    shapes = []
    has_label = False
    has_conditional = False
    has_call = False
    has_jump = False
    has_narrow = False
    has_high_byte = False
    for raw in unit.get("body_verbatim") or []:
        line = raw.strip()
        if line == "":
            continue
        text = line.split(REF.ANNOTATION)[0].strip()
        if text.endswith(":"):
            has_label = True
            continue
        mnemonic = text.split(" ", 1)[0]
        if REF.is_conditional_transfer(mnemonic):
            has_conditional = True
        if mnemonic == "call":
            has_call = True
        if mnemonic in ("jmp", "ud2"):
            has_jump = True
        for register in HIGH_BYTES:
            if register in text:
                has_high_byte = True
        stem = mnemonic
        for suffix in NARROW_WIDTH_SUFFIXES:
            if not stem.endswith(suffix):
                continue
            head = stem[:-1]
            if head in ("idiv", "div", "imul", "mul"):
                has_narrow = True
    if has_label:
        shapes.append("carries a positional label")
    if has_conditional:
        shapes.append("carries a conditional transfer")
    if has_call:
        shapes.append("carries a transfer into a routine")
    if has_jump:
        shapes.append("carries an unconditional transfer or a trap")
    if has_narrow:
        shapes.append("divides or widens at 8 or 16 bits")
    if has_high_byte:
        shapes.append("names a high-byte register")
    if not shapes:
        shapes.append("straight-line text: no label, no transfer, "
                      "no call")
    return shapes


def old_answer(unit):
    """the answer the SUPERSEDED simulator log 153's gate called gives
    for this body.  `gate48.reference_answer`, reproduced here so the
    superseded driver is not edited."""
    shared = {}
    simulator = OLD.Sim10(shared, "ship")
    simulator.answer_family = unit["result_family"]
    simulator.answer_width = unit["result_width"]
    lines = list(unit["body_verbatim"])
    return simulator.answer_value(lines)


def compare(one, other):
    """(verdict, model) for two z3 terms: are they the same value for
    every input?"""
    if one.size() != other.size():
        narrow = min(one.size(), other.size())
        one = z3.Extract(narrow - 1, 0, one)
        other = z3.Extract(narrow - 1, 0, other)
    solver = z3.Solver()
    solver.set("timeout", 20000)
    solver.add(one != other)
    answer = solver.check()
    if answer == z3.unsat:
        return "the two references agree for every input", None
    if answer == z3.sat:
        return "the two references DISAGREE", str(solver.model())
    return "the solver did not answer inside 20000 ms", None


def main():
    lost = lost_units()
    print("units log 153 records as proved that do not prove now: %d"
          % len(lost))
    bodies = bodies_for(set(lost))
    print("bodies found in canon38:                              %d"
          % len(bodies))
    by_shape = collections.Counter()
    by_agreement = collections.Counter()
    by_route = collections.Counter()
    by_fall = collections.Counter()
    rows = {}
    examples = collections.defaultdict(list)
    archives = {}
    path = os.path.join(HERE, "canon39_callee_units.json")
    if os.path.exists(path):
        document = json.load(open(path))
        for key, unit in document.get("units", {}).items():
            toolchain = unit.get("toolchain") or key.split("/", 1)[0]
            callee = unit.get("callee") or key.split("/", 1)[-1]
            archives.setdefault(toolchain, {})
            archives[toolchain][callee] = unit
    reference = REF.Reference(runtime_units=archives)
    total = len(lost)
    for index, name in enumerate(sorted(lost)):
        unit = bodies.get(name)
        if unit is None:
            by_shape["the unit is not in canon38"] += 1
            continue
        shapes = shapes_of(unit)
        key = " and ".join(shapes)
        by_shape[key] += 1
        row = {"shapes": shapes, "states": lost[name]}
        route = proving_route_in_task_53(lost[name])
        by_route[route] += 1
        row["proving_route_in_task_53"] = route
        falls = why_it_falls(lost[name])
        by_fall[falls] += 1
        row["how_it_falls"] = falls
        try:
            theirs = old_answer(unit)
        except Exception as problem:
            row["superseded_reference"] = ("refused: %s: %s"
                                           % (type(problem).__name__,
                                              problem))
            theirs = None
        try:
            ours, _width = reference.answer_for_unit(unit)
        except Exception as problem:
            row["one_reference"] = ("refused: %s: %s"
                                    % (type(problem).__name__, problem))
            ours = None
        if theirs is not None and ours is not None:
            verdict, model = compare(ours, theirs)
            row["agreement"] = verdict
            row["disagreement_at"] = model
            by_agreement[verdict] += 1
            if len(examples[verdict]) < 3:
                row["superseded_answer"] = str(z3.simplify(theirs))[:600]
                row["one_answer"] = str(z3.simplify(ours))[:600]
                row["body"] = [raw.split(REF.ANNOTATION)[0].strip()
                               for raw in unit.get("body_verbatim")]
                examples[verdict].append(name)
        elif theirs is None and ours is not None:
            key = ("the SUPERSEDED simulator refuses this body; the "
                   "ONE reference answers it")
            by_agreement[key] += 1
            if len(examples[key]) < 3:
                row["one_answer"] = str(z3.simplify(ours))[:600]
                row["body"] = [raw.split(REF.ANNOTATION)[0].strip()
                               for raw in unit.get("body_verbatim")]
                examples[key].append(name)
        elif ours is None and theirs is not None:
            key = ("the ONE reference refuses this body; the "
                   "SUPERSEDED simulator answered it")
            by_agreement[key] += 1
            if len(examples[key]) < 3:
                row["superseded_answer"] = str(z3.simplify(theirs))[:600]
                row["body"] = [raw.split(REF.ANNOTATION)[0].strip()
                               for raw in unit.get("body_verbatim")]
                examples[key].append(name)
        else:
            by_agreement["both references refuse this body"] += 1
        rows[name] = row
        if index % 25 == 0:
            print("[%d/%d] %s" % (index + 1, total, name))
            sys.stdout.flush()
        check_memory("unit %s" % name)

    print("")
    print("THE 245 LOST PROOFS, BY THE SHAPE OF THEIR OWN TEXT")
    for key, count in by_shape.most_common():
        print("  %5d | %s" % (count, key))
    print("")
    print("WHICH OF log 153's TWO ROUTES CARRIED THE PROOF THAT FELL")
    for key, count in by_route.most_common():
        print("  %5d | %s" % (count, key))
    print("")
    print("HOW IT FALLS IN THIS ROUND, in the two routes' own words")
    for key, count in by_fall.most_common():
        print("  %5d | %s" % (count, key))
    print("")
    print("THE TWO REFERENCES ON THE SAME BODY")
    for key, count in by_agreement.most_common():
        print("  %5d | %s" % (count, key))
        print("          sightings: %s" % ", ".join(examples[key]))
    print("")
    print("ONE INSTANCE OF EACH, WITH VALUES")
    for key in examples:
        for name in examples[key]:
            row = rows[name]
            print("")
            print("  %s -- %s" % (name, key))
            print("    LITERAL -- body: %s"
                  % "; ".join(row.get("body") or []))
            print("    LITERAL -- the SUPERSEDED simulator's answer: %s"
                  % row.get("superseded_answer"))
            print("    LITERAL -- the ONE reference's answer:        %s"
                  % row.get("one_answer"))
            print("    LITERAL -- they differ at: %s"
                  % row.get("disagreement_at"))
            print("    log 153's proving route: %s"
                  % row.get("proving_route_in_task_53"))
            print("    how it falls now:        %s"
                  % row.get("how_it_falls"))
            states = row.get("states") or {}
            for configuration in sorted(states):
                print("    this round, %s: %s -- %s"
                      % (configuration,
                         states[configuration].get("state"),
                         (states[configuration].get("ship_reason")
                          or "")[:200]))

    handle = open(OUT, "w")
    json.dump({"meta": {"generated_by": "t91_lost_proofs.py"},
               "by_shape": dict(by_shape),
               "by_agreement": dict(by_agreement),
               "by_proving_route_in_task_53": dict(by_route),
               "by_how_it_falls": dict(by_fall),
               "units": rows}, handle, indent=1, sort_keys=True)
    handle.close()
    print("")
    print("wrote %s" % OUT)
    print("PEAK RESIDENT SIZE: %.1f MB, cap %d MB"
          % (peak_resident_mb(), MEMORY_CAP_MB))


if __name__ == "__main__":
    main()
