#!/usr/bin/env python3
"""vex_names_census.py -- JOB 2 (log_082 lap): SPLIT THE MINER'S TWO
INSTRUMENTS.

super_op_miner.py's own `candidates` rows join, in one row, (a) a
recurring instruction sub-sequence and (b) the unmodelled lifter names
blocking the units that contain it -- but the names often appear
NOWHERE in the sub-sequence itself (measured, this lap's own report:
the halving-routine candidate's own sub-sequence is ['mov %P0,%P3',
'shr $1,%P3'] while its own listed blocking names Add32F0x4/
Sub32F0x4/Mul32F0x4/Div32F0x4 come from addss/subss/mulss/divss
ELSEWHERE in the same carrier units). That join is CO-OCCURRENCE
presented as a causal relation, exactly the thing THE SPELLING BAN's
own evidence discipline exists to prevent.

THIS FILE emits TWO artifacts instead, each honest about which
relation it encodes:

  name_census.json -- per unmodelled lifter name: units blocked
    (count and list), languages, sample units, and whether the name
    is REGULAR (parseable by JOB 1's vex_names.py translator) or
    IRREGULAR. Ranked by units blocked, descending -- this is the
    ACTIONABLE ranking (what to model next, and how many units each
    would unblock).

  idiom_candidates.json -- per recurring instruction sub-sequence
    (super_op_miner.py's own mining, reused UNCHANGED): support,
    languages, sample units, and a NEW field,
    `names_within_own_lifted_form`, naming which of the row's own
    `blocking_lifter_names` actually occur WITHIN the sub-sequence's
    own real-mnem instructions (checked by real-hardware mnemonic
    family: Add32F0x4 -> addss, CmpEQ64F0x2 -> cmpeqsd/cmpneqsd, and
    so on -- VEX_NAME_TO_MNEM below), separate from
    `blocking_lifter_names`, which stays exactly what super_op_miner.py
    already means by it: names that merely CO-OCCUR somewhere in the
    same carrier units. A name in `blocking_lifter_names` but NOT in
    `names_within_own_lifted_form` is co-occurrence, not cause.

BASELINE: canon24_units_<lang>.json (JOB 1's own newest generation --
recomputing the census on the POST-JOB-1 blocking picture, not the
stale pre-JOB-1 one super_op_candidates.json was built from).
super_op_miner.py's own loading/mining functions are REUSED BY IMPORT,
unchanged, just pointed at the new baseline -- this file adds no new
mining logic, only the split and the within-vs-co-occur check.

THE SPELLING BAN, verbatim as required: "No operator token may appear
in ANY key, grouping, pairing, row structure, candidate selection, or
comparison scope, anywhere in this line -- not in matching, not in
'which pairs get compared', not in report rows, not in dropdowns. The
candidate set for comparison comes from machine-form evidence
(clusters, connections, type pairs) or from ratified intention -- never
from the token. The token appears exactly once per unit: as a display
label on the member. MECHANICAL GUARD REQUIRED: every pipeline stage
that groups or pairs units must run check_no_spelling_keys.py and
refuse its own output on failure." Neither artifact here groups or
keys by the source-language operator token: name_census.json is keyed
by LIFTER NAME (a machine-form VEX op spelling, not a source operator)
and idiom_candidates.json is keyed by SUB-SEQUENCE (machine-form
instruction text), exactly super_op_miner.py's own existing scope.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  vex_names_census.py [--name-census FILE] [--idiom-candidates FILE]
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import super_op_miner as SM                                     # noqa: E402
import vex_names as VN                                           # noqa: E402

LANGS = SM.LANGS

BASELINE_PREFIX = "canon24_units_"

# --------------------------------------------------------------------
# VEX lifter name -> the real x86-64 mnemonic FAMILY it lowers to on
# this corpus's own ship code (forced by construction: read directly
# off canon4_units's own `mnem` for every worked example this lap
# opened -- c/op_501's own CmpEQ32F0x4-inside-XorV128 unit ships as
# `cvtsi2ss`+`cmpneqss`+`movd`+`and`, canon20_arith.py's own header
# states Add/Sub/Mul/Div32F0x4 -> addss/subss/mulss/divss directly).
# A name with NO entry here is left unmapped, honestly -- this file
# never guesses a mnemonic family it has not measured.
# --------------------------------------------------------------------

VEX_NAME_TO_MNEM = {
    "Add32F0x4": ("addss",),
    "Add64F0x2": ("addsd",),
    "Sub32F0x4": ("subss",),
    "Sub64F0x2": ("subsd",),
    "Mul32F0x4": ("mulss",),
    "Mul64F0x2": ("mulsd",),
    "Div32F0x4": ("divss",),
    "Div64F0x2": ("divsd",),
    "CmpEQ32F0x4": ("cmpeqss", "cmpneqss"),
    "CmpEQ64F0x2": ("cmpeqsd", "cmpneqsd"),
    "XorV128": ("xorps", "xorpd"),
    "OrV128": ("orps", "orpd"),
    "AndV128": ("andps", "andpd"),
    "Mul32": ("imul", "mul"),
    "Mul64": ("imul", "mul"),
    "DivModU128to64": ("div",),
    "DivModS128to64": ("idiv",),
}


def names_within(instructions, blocking_names):
    """which of `blocking_names` has a real mnemonic (VEX_NAME_TO_MNEM)
    that actually appears as the FIRST TOKEN of one of `instructions`
    -- i.e. genuinely inside the sub-sequence's own lifted/real-mnem
    form, not merely somewhere else in a carrier unit."""
    mnems_here = set()
    for line in instructions:
        parts = line.strip().split(" ", 1)
        if parts:
            mnems_here.add(parts[0])
    out = []
    for name in blocking_names:
        family = VEX_NAME_TO_MNEM.get(name)
        if family is None:
            continue
        if mnems_here & set(family):
            out.append(name)
    return sorted(out)


def load_blocked_from_canon24():
    """super_op_miner.load_blocked_units(), pointed at canon24_units_
    <lang>.json instead of canon23_units_<lang>.json -- same function,
    same shape, new (post-JOB-1) baseline. Reimplemented rather than
    parameterized because super_op_miner.py's own loader hard-codes
    its filename (this file does not edit super_op_miner.py)."""
    tree3 = json.load(open(os.path.join(HERE, "tree_units3.json")))["units"]
    tree3_by_key = {(r["lang"], r["n"]): r for r in tree3}

    blocked = []
    load_report = {}
    for lang in LANGS:
        c24_path = os.path.join(HERE, "%s%s.json" % (BASELINE_PREFIX, lang))
        c24 = json.load(open(c24_path))["units"]
        c4 = json.load(open(
            os.path.join(HERE, "canon4_units_%s.json" % lang)))["units"]
        n_total = len(c24)
        n_not_converged = 0
        n_with_mnem = 0
        n_with_names = 0
        for key, rec in c24.items():
            if rec.get("converged"):
                continue
            n_not_converged += 1
            c4rec = c4.get(key)
            if c4rec is None or not isinstance(c4rec.get("mnem"), list):
                continue
            n_with_mnem += 1
            tree3rec = tree3_by_key.get((lang, key))
            names = SM.unmodelled_names_for_unit(rec, tree3rec)
            if not names:
                continue
            n_with_names += 1
            blocked.append({
                "unit": rec["unit"],
                "lang": lang,
                "n": key,
                "unmodelled_names": names,
                "mnem_norm": SM.normalize_positionally(c4rec["mnem"]),
            })
        load_report[lang] = {
            "total_units_in_file": n_total,
            "not_yet_converged": n_not_converged,
            "not_yet_converged_with_mnem": n_with_mnem,
            "not_yet_converged_with_unmodelled_name": n_with_names,
        }
    return blocked, load_report


def build_name_census(blocked):
    per_name = {}
    for u in blocked:
        for name in u["unmodelled_names"]:
            row = per_name.setdefault(name, {
                "units_blocked": set(),
                "languages": set(),
                "sample_unit_ids": set(),
            })
            row["units_blocked"].add(u["unit"])
            row["languages"].add(u["lang"])
            row["sample_unit_ids"].add(u["unit"])

    rows = []
    for name, row in per_name.items():
        rows.append({
            "lifter_name": name,
            "units_blocked_count": len(row["units_blocked"]),
            "languages": sorted(row["languages"]),
            "sample_unit_ids": sorted(row["sample_unit_ids"])[:8],
            "regular": VN.is_regular_name(name),
            "regular_note": (
                "parseable by vex_names.py's own generic dispatch "
                "(LANE_ARITH_RE / LANE_CMP_RE / the whole-register-"
                "bitwise trio)" if VN.is_regular_name(name) else
                "not parseable by vex_names.py -- an irregular helper "
                "call or a not-yet-generalized shape"),
        })
    rows.sort(key=lambda r: (-r["units_blocked_count"], r["lifter_name"]))
    return rows


def build_idiom_candidates(blocked):
    occ_by_key = SM.enumerate_occurrences(blocked)
    rows = SM.recurring_sequences(blocked, occ_by_key)
    out_rows = []
    for r in rows:
        within = names_within(r["instructions"], r["blocking_lifter_names"])
        co_occur_only = sorted(
            set(r["blocking_lifter_names"]) - set(within))
        out_rows.append({
            "instructions": r["instructions"],
            "support": r["support"],
            "languages": r["languages"],
            "blocked_unit_count": r["blocked_unit_count"],
            "sample_unit_ids": r["sample_unit_ids"],
            "blocking_lifter_names": r["blocking_lifter_names"],
            "names_within_own_lifted_form": within,
            "names_co_occurring_only": co_occur_only,
            "relation_note": (
                "blocking_lifter_names is CO-OCCURRENCE (every "
                "unmodelled name found anywhere in this row's own "
                "carrier units); names_within_own_lifted_form is the "
                "subset ALSO found as a real mnemonic inside this "
                "row's own instruction sub-sequence -- the honest "
                "narrower claim. An empty names_within_own_lifted_form "
                "with a non-empty blocking_lifter_names means this "
                "idiom's own instructions are compiler bookkeeping "
                "that merely happens to share carrier units with the "
                "listed names, not their cause."),
        })
    return out_rows


def run_guard(paths):
    guard = os.path.join(HERE, "check_no_spelling_keys.py")
    proc = subprocess.run(
        [sys.executable, guard] + list(paths),
        capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--name-census", default=os.path.join(
        HERE, "name_census.json"))
    ap.add_argument("--idiom-candidates", default=os.path.join(
        HERE, "idiom_candidates.json"))
    args = ap.parse_args(argv[1:])

    blocked, load_report = load_blocked_from_canon24()

    census_rows = build_name_census(blocked)
    idiom_rows = build_idiom_candidates(blocked)

    census_doc = {
        "role": "name census instrument (JOB 2, log_082 lap)",
        "evidence_class": "the tool's own testimony -- every field "
            "here is read off canon24_units_<lang>.json's own "
            "converged/reason fields and tree_units3.json's own "
            "normal_path_raw, the same sources super_op_miner.py's "
            "own instrument already used, just re-run on the post-"
            "JOB-1 baseline.",
        "baseline": "%s<lang>.json" % BASELINE_PREFIX,
        "load_report": load_report,
        "distinct_unmodelled_names": len(census_rows),
        "rows": census_rows,
    }

    idiom_doc = {
        "role": "idiom candidate instrument (JOB 2, log_082 lap)",
        "evidence_class": "the tool's own testimony for the mining "
            "(support/support/instructions, super_op_miner.py's own "
            "logic, reused unchanged); names_within_own_lifted_form "
            "is forced by construction -- an exact-token check of the "
            "row's own instruction text against VEX_NAME_TO_MNEM, "
            "never a guess.",
        "baseline": "%s<lang>.json" % BASELINE_PREFIX,
        "min_support": SM.MIN_SUPPORT,
        "min_length_instructions": SM.MIN_LENGTH,
        "vex_name_to_mnem": {k: list(v) for k, v in
                              sorted(VEX_NAME_TO_MNEM.items())},
        "candidates": idiom_rows,
    }

    with open(args.name_census, "w") as f:
        json.dump(census_doc, f, indent=1)
        f.write("\n")
    with open(args.idiom_candidates, "w") as f:
        json.dump(idiom_doc, f, indent=1)
        f.write("\n")

    rc, out, err = run_guard([args.name_census, args.idiom_candidates])
    guard_result = {
        "exit_code": rc,
        "passed": rc == 0,
        "stdout_tail": out[-4000:],
        "stderr_tail": err[-2000:],
    }
    census_doc["spelling_guard"] = guard_result
    idiom_doc["spelling_guard"] = guard_result
    with open(args.name_census, "w") as f:
        json.dump(census_doc, f, indent=1)
        f.write("\n")
    with open(args.idiom_candidates, "w") as f:
        json.dump(idiom_doc, f, indent=1)
        f.write("\n")

    print("blocked units (post-JOB-1 baseline): %d" % len(blocked))
    print("distinct unmodelled names: %d" % len(census_rows))
    print("idiom candidates: %d" % len(idiom_rows))
    print("spelling guard exit code: %d (%s)" %
          (rc, "PASS" if rc == 0 else "FAIL"))
    if rc != 0:
        print(out)
        print(err, file=sys.stderr)
        return 1
    print()
    print("name census, top 10 by units blocked:")
    for r in census_rows[:10]:
        print("  blocked=%-4d regular=%-5s langs=%s  %s" % (
            r["units_blocked_count"], r["regular"],
            ",".join(r["languages"]), r["lifter_name"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
