#!/usr/bin/env python3
"""t91_audit.py -- TASK 91's REPORT, computed off the run's own stores.

WHAT IT ANSWERS, and against which population each figure is stated.

  1. THE POPULATION LINE.  30,436 units in log 153; 30,436 in
     `t91_populations.json`; 30,436 in each re-gate store.  A unit in
     one and not the other is named, never dropped.
  2. THE FOUR STATES per run, against log 153 section 1.2.
  3. THE TWO POPULATIONS TASK 91 WAS SENT TO MOVE -- the 415 withdrawn
     disproofs and the 5,602 undecided -- each as a THREE-WAY SPLIT
     (proves / disproves / stays undecided) with the cause of every
     part, INCLUDING the part that did not move.
  4. ZERO REGRESSION over the 23,132 units log 153 recorded as proved:
     every one still proved, or named with its cause.
  5. THE WALL-CLOCK CONTROL.  `gate.SOLVER_MILLISECONDS` is a wall
     clock, so unchanged code re-run can move a verdict.  The `fix` and
     `control` runs of ONE configuration are identical code over an
     identical population, so their disagreement is the wall clock and
     is reported separately from the movement the reference caused.
  6. THE CONSISTENCY LINE: units proved on one route and disproved on
     the other.  The gate CORE: "two routes never contradict".

THE CAUSE VOCABULARY is `audit64.cause_of`'s, reused rather than
reinvented, with canon38 in the place of canon39 -- so the two rounds'
reports read against each other.

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

No operator token appears in this file.  Rows are grouped by STATE and
by the run's own recorded REASON -- machine-form evidence off the
artifacts -- never by any spelling.

Coding discipline (the owner's ruling): no compound one-liner statements.

usage:
  t91_audit.py            writes t91_audit.json and prints the report
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ("c", "cpp", "go", "rust", "swift")
STATES = ("proved", "withdrawn", "undecided", "no term")
RUNS = (("attached_callees", "fix"),
        ("attached_callees", "control"),
        ("no_attached_callees", "fix"),
        ("no_attached_callees", "control"))
HEADLINE = ("attached_callees", "fix")
OUT = os.path.join(HERE, "t91_audit.json")


def store_of(configuration, label):
    """every record of one run, keyed by unit name."""
    out = {}
    directory = os.path.join(HERE, "t91_regate_store_%s_%s"
                             % (configuration, label))
    if not os.path.isdir(directory):
        return out
    for path in sorted(glob.glob(os.path.join(directory, "*.json"))):
        document = json.load(open(path))
        for name, record in document.get("units", {}).items():
            out[name] = record
    return out


def canon38_units():
    """the stored canon38 record of every unit: its body and its
    ledger, which is what a cause is computed off."""
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
        for name, record in document.get("units", {}).items():
            if "ledger" not in record:
                continue
            out[name] = {
                "body_verbatim": record.get("body_verbatim"),
                "ledger_producers": producers_of(record),
            }
    return out


def producers_of(record):
    """the (kind, callee) of every ledger row, which is all a cause
    needs -- the terms themselves are never held."""
    out = []
    for row in record.get("ledger") or []:
        producer = row.get("produced_by") or {}
        if not isinstance(producer, dict):
            continue
        out.append((producer.get("kind"), producer.get("callee")))
    return out


def callee_archives():
    path = os.path.join(HERE, "canon39_callee_units.json")
    if not os.path.exists(path):
        return {}
    document = json.load(open(path))
    out = {}
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain")
        if toolchain is None:
            toolchain = key.split("/", 1)[0]
        name = unit.get("callee")
        if name is None:
            name = key.split("/", 1)[-1]
        out.setdefault(toolchain, set())
        out[toolchain].add(name)
    return out


TOOLCHAIN_OF = {"c": "clang", "cpp": "clang++", "go": "go",
                "rust": "rustc", "swift": "swiftc"}


def call_targets(unit_record):
    """the routines this body transfers into, resolved the way the
    reference itself resolves them -- `ledger.transfer_callee`, which
    reads the RELOCATION on the line as well as its text, because an
    unlinked `call` disassembles as a transfer to an address inside
    the unit and only the relocation still says where it goes.  The
    first version of this file split the text on a space and lost the
    relocation, which left 2,969 disproofs with no computed cause;
    this is that defect fixed."""
    import ledger as LEDGER
    import reference as R
    out = []
    for raw in unit_record.get("body_verbatim") or []:
        line = raw.strip()
        if line == "":
            continue
        text = line.split(R.ANNOTATION)[0].strip()
        annotation = ""
        if R.ANNOTATION in line:
            annotation = line.split(R.ANNOTATION, 1)[1]
        parts = text.split(" ", 1)
        mnemonic = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        named = LEDGER.transfer_callee(mnemonic, R.split_operands(rest),
                                       annotation)
        if named is None:
            continue
        out.append(named)
    return out


def attached_here(name, unit_record, archives):
    """the routines this body transfers into that the archive of ITS
    OWN toolchain holds a body for -- `Reference.callees_for`'s own
    rule, so this cause is computed off the same fact the walk used."""
    lang = name.split("/", 1)[0]
    toolchain = TOOLCHAIN_OF.get(lang)
    held = archives.get(toolchain) or set()
    out = []
    for target in call_targets(unit_record):
        if target in held:
            out.append(target)
    return out


def ledger_names_the_callee(unit_record, callee):
    for kind, named in unit_record.get("ledger_producers") or []:
        if kind != "runtime_callee":
            continue
        if named == callee:
            return True
    return False


def has_a_conditional_transfer(unit_record):
    import reference as R
    for raw in unit_record.get("body_verbatim") or []:
        text = raw.split("!!")[0].strip()
        if text == "":
            continue
        if R.is_conditional_transfer(text.split(" ", 1)[0]):
            return True
    return False


def reason_of(record):
    """the reason the run itself recorded, from the route that decided
    -- never a phrase invented here."""
    if record.get("transcription_refused"):
        return record["transcription_refused"]
    ship = record.get("ship") or {}
    text = record.get("text") or {}
    proved = ("PROVED_ON_SHIP", "PROVED_BY_CONSTRUCTION")
    if ship.get("outcome") in proved:
        return ship.get("reason")
    if text.get("outcome") in proved:
        return text.get("reason")
    if ship.get("outcome") == "DISPROVED":
        return ship.get("reason")
    if text.get("outcome") == "DISPROVED":
        return text.get("reason")
    return ship.get("reason") or text.get("reason")


def cause_of(name, was, now, record, canon, archives, task53_reason):
    """the cause of one unit's movement or of its standing still,
    computed off its own artifacts.  `audit64.cause_of`'s vocabulary."""
    unit_record = canon.get(name)
    if unit_record is None:
        return "the unit is not in canon38's transcribed population"
    unmodelled = []
    for callee in attached_here(name, unit_record, archives):
        if ledger_names_the_callee(unit_record, callee):
            continue
        unmodelled.append(callee)
    if now == "withdrawn" and unmodelled:
        return ("the unit's own stored canon38 ledger carries NO row "
                "for its transfer into the compiler's own runtime, so "
                "its term asserts the transfer changed nothing; the "
                "reference now walks that callee's body, and the two "
                "disagree")
    if now == "proved" and was != "proved":
        if was == "withdrawn":
            return ("the ONE reference's remainder is the machine's: "
                    "SRem/URem, whose sign follows the dividend, in "
                    "the place of the z3 operator whose sign follows "
                    "the divisor (log 153 section 5)")
        if unmodelled or attached_here(name, unit_record, archives):
            return ("the reference now enters the attached runtime "
                    "callee's body and returns through its answer "
                    "register")
        if has_a_conditional_transfer(unit_record):
            return ("the reference now follows this body's own "
                    "branches and merges them at the join")
        return ("the reference now models something this body spells "
                "that it refused before (the machine stack, the x87 "
                "stack, the narrow division and widening multiply, or "
                "a rip-relative address)")
    if was == "proved" and now != "proved":
        return "A PROOF WAS LOST: %s" % (reason_of(record) or "")
    reason = reason_of(record)
    if reason is None:
        reason = "no reason recorded on the new record"
    if was == now:
        return "did not move; the run's own reason: %s" % reason[:180]
    return "the new run's own recorded reason: %s" % reason[:180]


def counted(rows):
    counter = collections.Counter()
    examples = collections.defaultdict(list)
    for key, name in rows:
        counter[key] += 1
        if len(examples[key]) < 3:
            examples[key].append(name)
    out = []
    for key, total in counter.most_common():
        out.append((total, key, examples[key]))
    return out


def print_causes(rows, indent="     "):
    for total, key, examples in counted(rows):
        print("%s%6d | %s" % (indent, total, key))
        print("%s       sightings: %s" % (indent, ", ".join(examples)))


def main():
    populations = json.load(open(os.path.join(
        HERE, "t91_populations.json")))
    was_of = {}
    for state in populations["buckets"]:
        for name in populations["buckets"][state]:
            was_of[name] = state
    canon = canon38_units()
    archives = callee_archives()
    stores = {}
    for configuration, label in RUNS:
        stores[(configuration, label)] = store_of(configuration, label)

    document = {"meta": {"generated_by": "t91_audit.py"}, "runs": {}}

    print("=" * 70)
    print("THE POPULATION LINE")
    print("=" * 70)
    print("  units in log 153 section 1.2:                     %d"
          % populations["meta"]["log_153_section_1_2"]["units"])
    print("  units in t91_populations.json:                    %d"
          % populations["units_in_all"])
    print("  units carrying a canon38 ledger:                  %d"
          % len(canon))
    for configuration, label in RUNS:
        store = stores[(configuration, label)]
        print("  units in the %-22s %-8s run:  %d"
              % (configuration, label, len(store)))
        missing = set(was_of) - set(store)
        extra = set(store) - set(was_of)
        if missing:
            print("     in log 153 and NOT in this run: %d  %s"
                  % (len(missing), sorted(missing)[:5]))
        if extra:
            print("     in this run and NOT in log 153: %d  %s"
                  % (len(extra), sorted(extra)[:5]))

    for configuration, label in RUNS:
        store = stores[(configuration, label)]
        if not store:
            continue
        print("")
        print("=" * 70)
        print("THE FOUR STATES -- configuration %r, run %r"
              % (configuration, label))
        print("=" * 70)
        counts = collections.Counter()
        per_population = collections.defaultdict(collections.Counter)
        for name, record in store.items():
            state = record.get("state")
            counts[state] += 1
            per_population[record.get("population")][state] += 1
            per_population[record.get("population")]["units"] += 1
        print("  %-12s %10s %10s %9s" % ("state", "log 153", "here",
                                         "delta"))
        expected = populations["meta"]["log_153_section_1_2"]
        for state in STATES:
            print("  %-12s %10d %10d %+9d"
                  % (state, expected[state], counts[state],
                     counts[state] - expected[state]))
        print("  %-12s %10d %10d %+9d"
              % ("units", expected["units"], sum(counts.values()),
                 sum(counts.values()) - expected["units"]))
        document["runs"]["%s/%s" % (configuration, label)] = {
            "counts": dict(counts),
            "per_population": {k: dict(v) for k, v
                               in per_population.items()},
        }
        print("")
        print("  PER POPULATION")
        for population in sorted(per_population,
                                 key=lambda x: str(x)):
            print("    %s" % population)
            for state in STATES:
                print("      %-12s %8d"
                      % (state, per_population[population][state]))
            print("      %-12s %8d"
                  % ("units", per_population[population]["units"]))

    for configuration, label in RUNS:
        store = stores[(configuration, label)]
        if not store:
            continue
        print("")
        print("=" * 70)
        print("THE TWO POPULATIONS TASK 91 RE-GATES -- configuration "
              "%r, run %r" % (configuration, label))
        print("=" * 70)
        for bucket in ("withdrawn", "undecided"):
            names = populations["buckets"][bucket]
            split = collections.Counter()
            rows = collections.defaultdict(list)
            for name in names:
                record = store.get(name)
                if record is None:
                    split["missing from this run"] += 1
                    continue
                now = record.get("state")
                split[now] += 1
                cause = cause_of(name, bucket, now, record, canon,
                                 archives,
                                 populations["task_53_reason"].get(name))
                rows[now].append((cause, name))
            print("")
            print("  STARTING POPULATION: the %d units log 153 records "
                  "as %s" % (len(names), bucket))
            for state in STATES:
                share = 0.0
                if names:
                    share = 100.0 * split[state] / len(names)
                print("    %-12s %8d   %5.1f%% of the %d"
                      % (state, split[state], share, len(names)))
            if split["missing from this run"]:
                print("    %-12s %8d"
                      % ("missing", split["missing from this run"]))
            for state in STATES:
                if not rows[state]:
                    continue
                print("")
                print("    -- %s -> %s  (%d units), by computed cause"
                      % (bucket, state, len(rows[state])))
                print_causes(rows[state], indent="       ")
            document["runs"]["%s/%s" % (configuration, label)][
                "bucket_%s" % bucket] = dict(split)

    print("")
    print("=" * 70)
    print("ZERO REGRESSION -- the 23,132 units log 153 records as "
          "proved")
    print("=" * 70)
    for configuration, label in RUNS:
        store = stores[(configuration, label)]
        if not store:
            continue
        proved_before = populations["buckets"]["proved"]
        kept = 0
        lost = []
        for name in proved_before:
            record = store.get(name)
            if record is None:
                lost.append(("missing from this run", name))
                continue
            if record.get("state") == "proved":
                kept = kept + 1
                continue
            lost.append(("%s -- %s" % (record.get("state"),
                                       (reason_of(record) or "")[:150]),
                         name))
        print("")
        print("  configuration %r, run %r" % (configuration, label))
        print("    units still proved (kept)          %8d" % kept)
        print("    proofs lost                        %8d" % len(lost))
        if lost:
            print_causes(lost, indent="       ")
        document["runs"]["%s/%s" % (configuration, label)][
            "zero_regression"] = {"kept": kept, "lost": len(lost)}

    print("")
    print("=" * 70)
    print("THE WALL-CLOCK CONTROL -- unchanged code re-run")
    print("=" * 70)
    for configuration in ("attached_callees", "no_attached_callees"):
        fix = stores.get((configuration, "fix")) or {}
        control = stores.get((configuration, "control")) or {}
        if not fix or not control:
            continue
        moved = []
        for name in sorted(set(fix) & set(control)):
            first = fix[name].get("state")
            second = control[name].get("state")
            if first == second:
                continue
            moved.append(("%s in the fix run, %s in the control run"
                          % (first, second), name))
        share = 100.0 * len(moved) / max(1, len(set(fix) & set(control)))
        print("")
        print("  configuration %r: %d of %d units answer differently "
              "when the SAME code is run twice (%.2f%%)"
              % (configuration, len(moved),
                 len(set(fix) & set(control)), share))
        print_causes(moved, indent="     ")
        document["runs"].setdefault("wall_clock", {})
        document["runs"]["wall_clock"][configuration] = {
            "units_in_both": len(set(fix) & set(control)),
            "answered_differently": len(moved),
        }

    print("")
    print("=" * 70)
    print("THE CONSISTENCY LINE -- two routes never contradict")
    print("=" * 70)
    for configuration, label in RUNS:
        store = stores[(configuration, label)]
        if not store:
            continue
        contradictions = []
        proved = ("PROVED_ON_SHIP", "PROVED_BY_CONSTRUCTION")
        for name, record in store.items():
            first = (record.get("ship") or {}).get("outcome")
            second = (record.get("text") or {}).get("outcome")
            if first in proved and second == "DISPROVED":
                contradictions.append(name)
                continue
            if second in proved and first == "DISPROVED":
                contradictions.append(name)
        print("  %-22s %-8s  units proved on one route and disproved "
              "on the other: %d"
              % (configuration, label, len(contradictions)))
        if contradictions:
            print("     %s" % sorted(contradictions)[:10])
        document["runs"]["%s/%s" % (configuration, label)][
            "contradictions"] = len(contradictions)

    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    print("")
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
