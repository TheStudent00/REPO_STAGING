#!/usr/bin/env python3
"""canon30_negative_control.py -- TASK 26: does the float gate ever
say no?

canon30.py returned 116 attempted / 116 PROVED_EQUAL. A gate that
proves everything it is shown is indistinguishable from a gate that
is not looking. This file is the check: it takes each unit canon30
accepted, MUTATES the candidate text in a way that must change the
computed answer, and re-runs the identical gate. A mutation that
still proves equal is a defect in the model, reported by unit.

The three mutations, each a change no correct rendering could make:

  swap_float_arith  -- the last scalar float arithmetic mnemonic is
                       replaced by a different one of the same width
                       (addss <-> subss, mulsd <-> divsd, ...). The
                       four arithmetic functions are four DIFFERENT
                       uninterpreted symbols, so two texts differing
                       in one of them can only be proved equal by a
                       broken model.
  swap_operands     -- the operand order of the last scalar float
                       arithmetic instruction is reversed. The
                       uninterpreted functions are not commutative,
                       so this must be visible.
  drop_last_arith   -- the last scalar float arithmetic instruction
                       is deleted outright.

A mutation that cannot be applied to a unit (no scalar float
arithmetic in its text) is reported as not_applicable, never counted
as a pass.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon30_negative_control.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                      # noqa: E402

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
        line = raw.strip()
        parts = line.split(" ", 1)
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


def main():
    canon4_docs = {}
    sem_docs = {}
    canon30_docs = {}
    for lang in LANGS:
        p4 = os.path.join(HERE, "canon4_units_%s.json" % lang)
        canon4_docs[lang] = json.load(open(p4))["units"]
        ps = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        sem_docs[lang] = json.load(open(ps))["units"]
        p30 = os.path.join(HERE, "canon30_units_%s.json" % lang)
        canon30_docs[lang] = json.load(open(p30))["units"]
    tally = {
        "units_tested": 0,
        "mutations_applied": 0,
        "mutations_rejected_by_gate": 0,
        "mutations_still_proved_equal": 0,
        "mutations_not_applicable": 0,
    }
    failures = []
    rows = {}
    for lang in LANGS:
        for n, rec in canon30_docs[lang].items():
            verdict = rec.get("job7_float_ground_truth_verdict")
            if verdict != "PROVED_EQUAL":
                continue
            text = rec.get("job7_candidate_text")
            if text is None:
                # a branching unit: mutate its derived_blocks copy
                rec4 = canon4_docs[lang].get(n) or {}
                blocks = rec4.get("derived_blocks")
                if not blocks:
                    continue
                flat = []
                for b in blocks:
                    for s in b["steps"]:
                        flat.append(s)
                idx = last_arith_index(flat)
                if idx is None:
                    tally["mutations_not_applicable"] += 3
                    continue
                tally["units_tested"] += 1
                for kind in ("swap_float_arith", "swap_operands",
                             "drop_last_arith"):
                    mutated = mutate_blocks(blocks, kind)
                    if mutated is None:
                        tally["mutations_not_applicable"] += 1
                        continue
                    tally["mutations_applied"] += 1
                    v, d = check_blocks(lang, n, canon4_docs,
                                        sem_docs, mutated)
                    record(tally, failures, rows, lang, n, kind, v)
                continue
            lines = [ln.strip() for ln in text.split(";")]
            tally["units_tested"] += 1
            for kind in ("swap_float_arith", "swap_operands",
                         "drop_last_arith"):
                mutated = mutate(lines, kind)
                if mutated is None:
                    tally["mutations_not_applicable"] += 1
                    continue
                tally["mutations_applied"] += 1
                v, d = BC10.anchored_check_straight(
                    lang, n, canon4_docs, sem_docs,
                    "; ".join(mutated))
                record(tally, failures, rows, lang, n, kind, v)
    print("negative control tally: %r" % tally)
    if failures:
        print("MUTATIONS THE GATE FAILED TO REJECT:")
        for f in failures:
            print("   ", f)
    else:
        print("PASS -- every applied mutation was rejected by the "
              "gate (no mutation proved equal)")
    out = {
        "meta": {
            "role": "generator provenance",
            "produced_by": "canon30_negative_control.py",
            "tally": tally,
        },
        "per_unit": rows,
        "failures": failures,
    }
    path = os.path.join(HERE, "canon30_negative_control.json")
    fh = open(path, "w")
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon30_negative_control.json")


def mutate_blocks(blocks, kind):
    """apply the same mutation to the LAST scalar-float-arithmetic
    line across the block list, preserving block structure."""
    target_block = None
    target_idx = None
    for bi, b in enumerate(blocks):
        idx = last_arith_index(b["steps"])
        if idx is not None:
            target_block = bi
            target_idx = idx
    if target_block is None:
        return None
    out = []
    for bi, b in enumerate(blocks):
        steps = list(b["steps"])
        if bi == target_block:
            mutated = mutate(steps, kind)
            if mutated is None:
                return None
            steps = mutated
        out.append({"label": b["label"], "steps": steps})
    return out


def check_blocks(lang, n, canon4_docs, sem_docs, mutated_blocks):
    """the branching gate, with the candidate block list replaced by
    the mutated one -- the real side is untouched ground truth."""
    rec = dict(canon4_docs[lang][n])
    rec["derived_blocks"] = mutated_blocks
    patched = {}
    for key in canon4_docs:
        patched[key] = canon4_docs[key]
    patched[lang] = dict(canon4_docs[lang])
    patched[lang][n] = rec
    return BC10.anchored_check_branching(lang, n, patched, sem_docs)


def record(tally, failures, rows, lang, n, kind, verdict):
    key = "%s/%s/%s" % (lang, n, kind)
    rows[key] = verdict
    if verdict == "PROVED_EQUAL":
        tally["mutations_still_proved_equal"] += 1
        failures.append(key)
        return
    tally["mutations_rejected_by_gate"] += 1


if __name__ == "__main__":
    main()
