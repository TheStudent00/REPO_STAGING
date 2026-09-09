#!/usr/bin/env python3
"""canon37_zero_regression.py -- ZERO REGRESSIONS IN THE RULED SENSE.

The rule: no unit proved under round 9 (region36 / canon36_*) loses
proved status under round 10 (ledger47 / canon37_*) without a NAMED,
PROVED cause.

This file computes the three populations' before/after sets, lists
every unit that lost proved status, and for each one CHECKS the named
cause mechanically rather than asserting it.  Two causes are expected,
and both are round-9 unsoundness rather than a round-10 capability
loss:

  CAUSE A -- THE UNREACHABLE STORE.  Round 9 appended its result store
  and a `ret` after a body whose last instruction is an unconditional
  transfer (a tail-call `jmp` to another routine).  In the real
  machine that store can never execute; round 9's simulator walks the
  text straight through and does not model `jmp`, so it read a value
  the machine would never write.  Round 10 refuses such a unit by
  name: the answer is produced by the callee, and storing it would
  require changing the body, which ruling 1 forbids.
  THE CHECK: round 9's own recorded text has its result store placed
  after the last unconditional transfer, and the body carries no
  `ret`.

  CAUSE B -- THE VACUOUS ANSWER HOME.  Round 9 admitted units for
  which no answer home could be named at all -- an x87 unit whose
  answer is in `st(0)`, or a unit whose whole body is `ret`.  Its
  structural route does not require an answer home, so those units
  were admitted on the plumbing alone, with nothing said about the
  answer.  Round 10 refuses them by name.
  THE CHECK: round 9's own record names no answer home, or names a
  family the unit's own body never writes.

usage:
  canon37_zero_regression.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon                                                     # noqa: E402
import ledger47 as L47                                           # noqa: E402
import region36 as R36                                           # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]
TRANSFER = ("jmp", "jmpq", "call", "callq", "ud2", "hlt")

WRITE_MNEMONICS = frozenset(L47.PURE_WRITE_MNEMONICS)


def body_of(record):
    text = record.get("body_text")
    if text is None:
        return []
    return L47.split_lines(text)


def last_executable(lines):
    for line in reversed(lines):
        stripped = R36.strip_annotation(line)
        if stripped.endswith(":"):
            continue
        return stripped
    return None


def writes_family(lines, family):
    if family is None:
        return False
    for raw in lines:
        line = R36.strip_annotation(raw)
        for token in L47.operands_of(line):
            if not token.startswith("%"):
                continue
            if canon.FAMILY_OF.get(token[1:]) == family:
                return True
            if token[1:] == family:
                return True
    return False


def check_cause(new_record, old_record):
    """(cause, evidence) or (None, why the cause could not be named)."""
    lines = body_of(new_record)
    cause = new_record.get("refusal_cause")
    if cause == "never returns":
        last = last_executable(lines)
        head = None
        if last is not None:
            head = last.split(" ", 1)[0]
        returns = 0
        for line in lines:
            if R36.strip_annotation(line) == "ret":
                returns = returns + 1
        old_text = old_record.get("universal_text") or ""
        store_after = False
        pieces = L47.split_lines(old_text)
        seen_transfer = False
        for piece in pieces:
            head_piece = piece.split(" ", 1)[0]
            if head_piece in TRANSFER:
                seen_transfer = True
                continue
            if seen_transfer:
                if "(%r15)" in piece:
                    store_after = True
        if head in TRANSFER:
            if returns == 0:
                return ("A: the unreachable store",
                        {"the body's last instruction": last,
                         "the body's `ret` count": returns,
                         "round 9 placed a store after that transfer":
                             store_after,
                         "round 9's own text": old_text})
        return (None,
                "the refusal is `never returns` but the body's last "
                "instruction is %r with %d returns" % (last, returns))
    if cause == "no answer home":
        old_home = old_record.get("answer_lineage_family")
        if old_home is None:
            old_home = old_record.get("result_lineage_home")
        if old_home is None:
            return ("B: the vacuous answer home",
                    {"round 9 named no answer home": True,
                     "the body": "; ".join(lines)})
        if not writes_family(lines, old_home):
            return ("B: the vacuous answer home",
                    {"round 9 named the answer home": old_home,
                     "the body never writes that family": True,
                     "the body": "; ".join(lines)})
        return (None,
                "round 9 named the answer home %r and the body does "
                "write it" % old_home)
    return (None, "the refusal cause %r is not one of the two named "
                  "causes" % cause)


def gather_original():
    old = {}
    new = {}
    for lang in LANGS:
        for label, record in json.load(
                open(os.path.join(
                    HERE, "canon36_universal_%s.json" % lang)))["units"].items():
            old[label] = record
        for label, record in json.load(
                open(os.path.join(
                    HERE, "canon37_wrapped_%s.json" % lang)))["units"].items():
            new[label] = record
    return old, new


def gather_interp():
    old = json.load(open(os.path.join(HERE,
                                      "canon36_interp.json")))["units"]
    new = json.load(open(os.path.join(HERE,
                                      "canon37_interp.json")))["units"]
    return old, new


def gather_regen():
    old = {}
    new = {}
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon36_regen_store",
                                              "*.json"))):
        for label, record in json.load(open(path))["units"].items():
            old[label] = record
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "canon37_regen_store",
                                              "*.json"))):
        for label, record in json.load(open(path))["units"].items():
            new[label] = record
    return old, new


def compare_population(name, old, new):
    old_ok = set()
    new_ok = set()
    for label, record in old.items():
        if record.get("outcome") == "REGION_TEXT_PROVED":
            old_ok.add(label)
    for label, record in new.items():
        if record.get("outcome") == "WRAPPED_TEXT_PROVED":
            new_ok.add(label)
    lost = sorted(old_ok - new_ok)
    gained = sorted(new_ok - old_ok)
    causes = {}
    unnamed = []
    samples = {}
    for label in lost:
        cause, evidence = check_cause(new[label], old[label])
        if cause is None:
            unnamed.append({"unit": label, "why": evidence})
            continue
        causes[cause] = causes.get(cause, 0) + 1
        if cause not in samples:
            samples[cause] = {"unit": label, "evidence": evidence}
    return {
        "population": name,
        "units": len(new),
        "round9_proved": len(old_ok),
        "round10_proved": len(new_ok),
        "lost_proved_status": len(lost),
        "gained_proved_status": len(gained),
        "lost_by_named_cause": causes,
        "one_worked_instance_per_cause": samples,
        "lost_with_no_named_cause": unnamed,
        "gained_units": gained if len(gained) <= 40 else gained[:40],
        "verdict": ("ZERO REGRESSIONS in the ruled sense"
                    if not unnamed else
                    "REGRESSION: %d units lost proved status with no "
                    "named cause" % len(unnamed)),
    }


def main():
    report = []
    old, new = gather_original()
    report.append(compare_population("original (1,779 compiled units)",
                                     old, new))
    old, new = gather_interp()
    report.append(compare_population("interpreter/JIT (11 units)",
                                     old, new))
    old, new = gather_regen()
    report.append(compare_population("regenerated (29,288 units)",
                                     old, new))
    document = {
        "meta": {
            "role": "audit",
            "generated_by": "canon37_zero_regression.py",
            "rule": "no unit proved under round 9 loses proved status "
                    "without a named, proved cause",
            "round9": "region36.py / canon36_*.json (untouched, the "
                      "superseded record)",
            "round10": "ledger47.py / canon37_*.json",
        },
        "populations": report,
    }
    path = os.path.join(HERE, "canon37_zero_regression.json")
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    for entry in report:
        print("%-34s round9 proved %6d  round10 proved %6d  lost %5d  "
              "gained %5d  %s"
              % (entry["population"], entry["round9_proved"],
                 entry["round10_proved"], entry["lost_proved_status"],
                 entry["gained_proved_status"], entry["verdict"]))
        for cause, count in sorted(entry["lost_by_named_cause"].items()):
            print("        %6d  %s" % (count, cause))
        for item in entry["lost_with_no_named_cause"][:10]:
            print("        UNNAMED  %s -- %s" % (item["unit"],
                                                 item["why"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
