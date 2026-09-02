#!/usr/bin/env python3
"""canon31_controls.py -- TASK 26: two controls on the float gate,
because a gate that only ever says yes and a gate that only ever says
no are both useless, and both look like a result.

CONTROL 1, NEGATIVE, over every straight-line unit canon31 accepted.
Each accepted candidate text is MUTATED in a way that must change the
answer, and the identical gate is re-run. A mutation that still
proves equal is a defect in the model and is named by unit.

  swap_float_arith  the last scalar float arithmetic mnemonic becomes
                    a different one of the same width (addss <->
                    subss, mulsd <-> divsd, ...). These are four
                    DIFFERENT uninterpreted function symbols.
  swap_operands     the operand order of that instruction is
                    reversed. The functions are not commutative.
  drop_last_arith   that instruction is deleted.

CONTROL 2, POSITIVE, over every BRANCHING unit canon31 DISPROVED.
The gate is re-run with the unit's OWN REAL blocks standing in as the
candidate. If real-against-real proves equal, the walker, the float
model, the answer-home rule and the constant guard all work on that
unit, and the DISPROVED verdict is about the CANDIDATE TEXT, not
about this checker. A unit that cannot even prove equal to itself is
named -- its DISPROVED verdict would carry no weight.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon31_controls.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                      # noqa: E402
import real_blocks                                          # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

SWAP_ARITH = {
    "addss": "subss", "subss": "addss",
    "addsd": "subsd", "subsd": "addsd",
    "mulss": "divss", "divss": "mulss",
    "mulsd": "divsd", "divsd": "mulsd",
}

ARITH_MNEM = frozenset(SWAP_ARITH.keys())


def last_arith_index(lines):
    found = None
    for i, raw in enumerate(lines):
        parts = raw.strip().split(" ", 1)
        if parts[0] in ARITH_MNEM:
            found = i
    return found


def mutate(lines, kind):
    idx = last_arith_index(lines)
    if idx is None:
        return None
    out = list(lines)
    line = out[idx].strip()
    parts = line.split(" ", 1)
    mnem = parts[0]
    rest = parts[1] if len(parts) > 1 else ""
    if kind == "swap_float_arith":
        out[idx] = "%s %s" % (SWAP_ARITH[mnem], rest)
        return out
    if kind == "swap_operands":
        ops = [o.strip() for o in rest.split(",")]
        if len(ops) != 2:
            return None
        if ops[0] == ops[1]:
            return None
        out[idx] = "%s %s,%s" % (mnem, ops[1], ops[0])
        return out
    if kind == "drop_last_arith":
        del out[idx]
        return out
    return None


def load_all():
    canon4 = {}
    canon31 = {}
    sem = {}
    ops = {}
    for lang in LANGS:
        canon4[lang] = json.load(
            open(os.path.join(HERE, "canon4_units_%s.json" % lang))
        )["units"]
        canon31[lang] = json.load(
            open(os.path.join(HERE, "canon31_units_%s.json" % lang))
        )["units"]
        sem[lang] = json.load(
            open(os.path.join(HERE,
                              "sem_anchored_spill_%s.json" % lang))
        )["units"]
        ops[lang] = json.load(
            open(os.path.join(HERE, "op_units_%s.json" % lang))
        )["probes"]
    return canon4, canon31, sem, ops


def main():
    canon4, canon31, sem, ops = load_all()
    neg = {
        "units_tested": 0,
        "mutations_applied": 0,
        "mutations_rejected": 0,
        "mutations_still_proved_equal": 0,
        "mutations_not_applicable": 0,
    }
    neg_failures = []
    pos = {
        "units_tested": 0,
        "real_against_real_proved": 0,
        "real_against_real_not_proved": 0,
    }
    pos_failures = []
    rows = {}
    for lang in LANGS:
        for n, rec in canon31[lang].items():
            verdict = rec.get("job8_ground_truth_verdict")
            if verdict is None:
                continue
            key = "%s/%s" % (lang, n)
            if verdict == "PROVED_EQUAL":
                text = rec.get("job8_candidate_text")
                if text is None:
                    continue
                lines = [ln.strip() for ln in text.split(";")]
                neg["units_tested"] += 1
                for kind in ("swap_float_arith", "swap_operands",
                             "drop_last_arith"):
                    mutated = mutate(lines, kind)
                    if mutated is None:
                        neg["mutations_not_applicable"] += 1
                        continue
                    neg["mutations_applied"] += 1
                    v, _d = BC10.anchored_check_straight(
                        lang, n, canon4, sem, "; ".join(mutated))
                    rows["neg/%s/%s" % (key, kind)] = v
                    if v == "PROVED_EQUAL":
                        neg["mutations_still_proved_equal"] += 1
                        neg_failures.append("%s/%s" % (key, kind))
                        continue
                    neg["mutations_rejected"] += 1
                continue
            if verdict != "DISPROVED":
                continue
            probe = ops[lang].get(n)
            if probe is None:
                continue
            ship = probe.get("ship") or {}
            try:
                real_list = real_blocks.build(ship["bytes"],
                                              ship["mnem"])
            except real_blocks.NotCuttable:
                continue
            pos["units_tested"] += 1
            patched = {}
            for other in canon4:
                patched[other] = canon4[other]
            patched[lang] = dict(canon4[lang])
            rec4 = dict(canon4[lang][n])
            rec4["derived_blocks"] = real_list
            patched[lang][n] = rec4
            v, _d = BC10.anchored_check_branching_real(
                lang, n, patched, ops, sem)
            rows["pos/%s" % key] = v
            if v == "PROVED_EQUAL":
                pos["real_against_real_proved"] += 1
                continue
            pos["real_against_real_not_proved"] += 1
            pos_failures.append(key)
    print("CONTROL 1 (negative, mutation): %r" % neg)
    if neg_failures:
        print("   mutations the gate FAILED to reject:")
        for f in neg_failures:
            print("      ", f)
    else:
        print("   PASS -- every applied mutation was rejected")
    print("CONTROL 2 (positive, real against real): %r" % pos)
    if pos_failures:
        print("   units that could not even prove equal to "
              "themselves:")
        for f in pos_failures:
            print("      ", f)
    else:
        print("   PASS -- every DISPROVED branching unit proves "
              "equal to itself, so the DISPROVED verdict is about "
              "the candidate text, not about this checker")
    out = {
        "meta": {
            "role": "generator provenance",
            "produced_by": "canon31_controls.py",
            "negative": neg,
            "positive": pos,
        },
        "negative_failures": neg_failures,
        "positive_failures": pos_failures,
        "per_unit": rows,
    }
    path = os.path.join(HERE, "canon31_controls.json")
    fh = open(path, "w")
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon31_controls.json")


if __name__ == "__main__":
    main()
