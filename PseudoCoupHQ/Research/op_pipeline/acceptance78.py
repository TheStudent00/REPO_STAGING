#!/usr/bin/env python3
"""acceptance78.py -- the mechanism of task 78, printed on real units.

Five parts, each a LITERAL block from an artifact on disk or from the
code run here:

  1. one attached callee's own body, and the reading of it -- the rule
     of `CORE_0_3_5_3_3_destination_rules.md` shown working;
  2. `c/regen_1056`, whose answer home IS `%xmm0`: its ledger row for
     the transfer in canon39 (none) and in canon40;
  3. a `guard_exit` unit, printed with the block-ending transfer that
     names it;
  4. `go/op_30`, the `unread_runtime_routine` shape, with the two
     lines that show the routine comes back;
  5. the callee-saved cross-check: no reading names a callee-saved
     family, which the reading was never told about.

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

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CALLEE_SAVED = ("rbx", "r12", "r13", "r14", "r15", "rbp")


def find_unit(label):
    for lang in ("c", "cpp", "go", "rust", "swift"):
        for prefix in ("canon40", "canon39"):
            path = os.path.join(HERE,
                                "%s_wrapped_%s.json" % (prefix, lang))
            if not os.path.exists(path):
                continue
            units = json.load(open(path))["units"]
            if label in units:
                return prefix, units[label]
    for prefix in ("canon40", "canon39"):
        pattern = os.path.join(HERE, "%s_regen_store" % prefix,
                               "*.json")
        for path in sorted(glob.glob(pattern)):
            units = json.load(open(path))["units"]
            if label in units:
                return prefix, units[label]
    return None, None


def unit_from(prefix, label):
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "%s_wrapped_%s.json" % (prefix, lang))
        if not os.path.exists(path):
            continue
        units = json.load(open(path))["units"]
        if label in units:
            return units[label]
    pattern = os.path.join(HERE, "%s_regen_store" % prefix, "*.json")
    for path in sorted(glob.glob(pattern)):
        units = json.load(open(path))["units"]
        if label in units:
            return units[label]
    return None


def runtime_rows(record):
    out = []
    for row in record.get("ledger") or []:
        producer = row.get("produced_by")
        if not isinstance(producer, dict):
            continue
        if producer.get("kind") != "runtime_callee":
            continue
        out.append(row)
    return out


def part_one(out):
    out.append("PART 1 -- ONE ATTACHED CALLEE'S BODY, AND THE READING")
    out.append("")
    bodies = json.load(open(os.path.join(
        HERE, "canon39_callee_units.json")))["units"]
    readings = json.load(open(os.path.join(
        HERE, "runtime_answers78.json")))["readings"]
    key = "clang/__extendhfsf2"
    out.append("LITERAL -- canon39_callee_units.json, %s" % key)
    for line in bodies[key]["body_verbatim"]:
        out.append("    %s" % line)
    out.append("")
    out.append("LITERAL -- runtime_answers78.json, the same key")
    out.append("    families: %s"
               % ",".join(readings[key]["families"]))
    out.append("    x87: %s" % readings[key]["x87"])
    out.append("    how: %s" % readings[key]["how"])
    out.append("")
    out.append("GLOSS: the last instruction before the return is "
               "`movd %esi,%xmm0`, so the family this routine answers "
               "in is read off the body as `xmm0` -- the accumulator "
               "the superseded rule 4 named is in the set too, "
               "because the body does change it, but it is not what "
               "the caller reads.")
    out.append("")


def part_two(out):
    out.append("PART 2 -- c/regen_1056, WHOSE ANSWER HOME IS %xmm0")
    out.append("")
    for prefix in ("canon39", "canon40"):
        record = unit_from(prefix, "c/regen_1056")
        if record is None:
            out.append("  %s: not on disk" % prefix)
            continue
        rows = runtime_rows(record)
        out.append("LITERAL -- %s, c/regen_1056" % prefix)
        out.append("    outcome:        %s" % record.get("outcome"))
        out.append("    result_family:  %s"
                   % record.get("result_family"))
        out.append("    runtime rows:   %d" % len(rows))
        for row in rows:
            out.append("      %s-%d  %s  %s"
                       % (row["block"], row["index"],
                          row["produced_by"]["callee"],
                          row.get("resident")))
        answer = None
        for row in record.get("ledger") or []:
            if row["block"] != "OUT":
                continue
            answer = row
        if answer is not None:
            out.append("    OUT-0 produced_by: %s"
                       % json.dumps(answer.get("produced_by")))
        out.append("")


def part_three(out):
    out.append("PART 3 -- A GUARD EXIT, PRINTED")
    out.append("")
    chosen = None
    for lang in ("go", "rust"):
        path = os.path.join(HERE, "canon40_wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        units = json.load(open(path))["units"]
        for label in sorted(units):
            shapes = units[label].get("transfer_shapes") or []
            kinds = [one["kind"] for one in shapes]
            if "guard_exit" in kinds:
                chosen = (label, units[label])
                break
        if chosen is not None:
            break
    if chosen is None:
        out.append("  no guard exit found in the original population")
        out.append("")
        return
    label, record = chosen
    out.append("LITERAL -- canon40, %s" % label)
    out.append("    outcome: %s" % record.get("outcome"))
    for line in record.get("body_verbatim") or []:
        out.append("    %s" % line)
    out.append("    transfer_shapes: %s"
               % json.dumps(record.get("transfer_shapes")))
    out.append("")


def part_four(out):
    out.append("PART 4 -- go/op_30, THE UNREAD RUNTIME ROUTINE")
    out.append("")
    record = unit_from("canon40", "go/op_30")
    if record is None:
        out.append("  go/op_30 is not on disk")
        out.append("")
        return
    out.append("LITERAL -- canon40, go/op_30")
    for line in record.get("body_verbatim") or []:
        out.append("    %s" % line)
    out.append("    transfer_shapes: %s"
               % json.dumps(record.get("transfer_shapes")))
    out.append("    runtime rows: %d" % len(runtime_rows(record)))
    out.append("")
    out.append("GLOSS: `call x_runtime_newobject` is followed by `mov "
               "0x20(%rsp),%ecx` and `mov %ecx,(%rax)` in the same "
               "block, so the routine comes back and the caller reads "
               "%rax.  No archive index on this machine defines the "
               "routine, so its own answer cannot be read and no row "
               "is guessed.")
    out.append("")


def part_five(out):
    out.append("PART 5 -- THE CALLEE-SAVED CROSS-CHECK")
    out.append("")
    readings = json.load(open(os.path.join(
        HERE, "runtime_answers78.json")))["readings"]
    offenders = []
    for key in sorted(readings):
        families = readings[key].get("families") or []
        for family in families:
            if family in CALLEE_SAVED:
                offenders.append("%s: %s" % (key, family))
    out.append("readings: %d" % len(readings))
    out.append("readings naming a callee-saved family %s: %d %s"
               % (str(CALLEE_SAVED), len(offenders),
                  ", ".join(offenders)))
    out.append("")
    out.append("GLOSS: the reading was never told which families the "
               "calling convention preserves.  It walks the body and "
               "asks whether each family ends holding the value it "
               "arrived with.  That it names none of the preserved "
               "families is a cross-check the reading did not aim at: "
               "forced by construction, from the bodies themselves.")
    out.append("")


def main(argv):
    out = []
    out.append("TASK 78 ACCEPTANCE -- THE RUNTIME ANSWER REGISTER")
    out.append("")
    part_one(out)
    part_two(out)
    part_three(out)
    part_four(out)
    part_five(out)
    text = "\n".join(out) + "\n"
    handle = open(os.path.join(HERE, "acceptance78_printed.txt"), "w")
    handle.write(text)
    handle.close()
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
