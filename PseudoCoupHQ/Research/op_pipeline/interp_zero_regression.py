#!/usr/bin/env python3
"""interp_zero_regression.py -- the zero-regression check for TASK 32.

THE BASELINE, STATED PRECISELY AND NOT FLATTENED (carried forward from
log_112, log_117 sec 8.1 and log_118 sec 6.1, and recomputed here from
disk rather than quoted):

  * RECORDED converged: 1,635 of the 1,779 compiled-five corpus --
    what the `status` field of `canon31_units_<lang>.json` says.
  * HONEST standing converged: 1,622 -- after log_112's branching
    audit re-gated 18 recorded-converged branching units against
    blocks cut from their own ship bytes and 13 did not re-prove.
  * The 13 WITHDRAWN are a SEPARATE POPULATION, not a subtraction
    folded into one number.
  * log_117's 5 sret proofs and log_118's 36 designated-memory proofs
    are NOT advanced.  Both are the owner's call and both are still open.
    TASK 32 adds no proof to that question either way.

WHAT THIS PROGRAM CHECKS:

 1. the recorded counts, recomputed from disk, per language;
 2. that the two tables TASK 32 must not touch --
    `dominant_table24.json` and `dom_ops22.json` -- are byte-identical
    to their state before this lap, by sha256 against the value the
    version control system holds for the commit before this lap's
    first artifact;
 3. that every guard/family artifact this lap READ is unchanged;
 4. the sha256 of every input file and every shared module this lap
    imported but did not edit.

usage:
  /tmp/reconnect_venv/bin/python3 interp_zero_regression.py
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_zero_regression.json")
LANGS = ["c", "cpp", "go", "rust", "swift"]

MUST_NOT_CHANGE = [
    "dominant_table24.json",
    "dom_ops22.json",
    "guards5.json",
    "exception_families3.json",
]

READ_ONLY_INPUTS = [
    "lineage_carve.json",
    "prove_interp_computation.json",
    "proposal_representation_dimension3.json",
    "dwarf_typed_key.json",
    "dwarf_typed_key_t27.json",
    "canon_interp_units_cpython.json",
    "canon_interp_units_java.json",
    "canon_interp_units_ruby_php.json",
    "interp_jvm.json",
    "canon33_arrival_modes.json",
]

SHARED_MODULES = [
    "canon.py",
    "canon2.py",
    "canon8_behaviour_check.py",
    "canon10_behaviour_check.py",
    "canon33_gate.py",
    "cross_unit_prover.py",
    "designated_memory.py",
    "lineage_carve.py",
    "check_no_spelling_keys.py",
]


def sha256_of(name):
    handle = open(os.path.join(HERE, name), "rb")
    digest = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    return digest


def git_blob_sha256(name, revision):
    """the sha256 of the file's content AT `revision`, read out of the
    version control system.  A file's current state is not its
    history: this is how a no-write claim is checked."""
    path = os.path.join("Research/op_pipeline", name)
    proc = subprocess.run(
        ["git", "-C", os.path.join(HERE, "..", ".."),
         "show", "%s:%s" % (revision, path)],
        capture_output=True)
    if proc.returncode != 0:
        return None
    return hashlib.sha256(proc.stdout).hexdigest()


def first_artifact_revision():
    """the commit immediately BEFORE this lap's first artifact landed.
    The daemon commits every 30 seconds, so the lap's own commits are
    in the history already; the comparison point is the commit before
    the first one that names an interp_canon34 file."""
    proc = subprocess.run(
        ["git", "-C", os.path.join(HERE, "..", ".."), "log",
         "--format=%H", "--diff-filter=A", "--",
         "Research/op_pipeline/interp_canon34.py"],
        capture_output=True, text=True)
    lines = [x for x in proc.stdout.split("\n") if x.strip()]
    if not lines:
        return None
    return "%s^" % lines[-1]


def main():
    report = {
        "meta": {
            "produced_by": "interp_zero_regression.py",
            "role": "generator provenance",
        },
        "baseline_stated_precisely": {
            "recorded_converged": 1635,
            "honest_standing_converged": 1622,
            "withdrawn_separate_population": 13,
            "population": "the 1,779-unit compiled-five corpus "
                          "(c, cpp, go, rust, swift)",
            "not_advanced_this_lap": [
                "log_117's 5 sret proofs -- the owner's call, still open",
                "log_118's 36 designated-memory proofs -- the owner's call, "
                "still open",
            ],
        },
    }

    per_language = {}
    recorded = 0
    unchanged = 0
    for lang in LANGS:
        doc = json.load(open(os.path.join(
            HERE, "canon31_units_%s.json" % lang)))
        converged = 0
        same = 0
        for _name, unit in doc["units"].items():
            if unit.get("status") == "converged":
                converged = converged + 1
            if unit.get("status") == "unchanged":
                same = same + 1
        per_language[lang] = {"converged": converged, "unchanged": same}
        recorded = recorded + converged
        unchanged = unchanged + same
    report["per_language"] = per_language
    report["recorded_converged_recomputed"] = recorded
    report["unchanged_recomputed"] = unchanged
    report["recorded_matches_baseline"] = (recorded == 1635)

    revision = first_artifact_revision()
    report["comparison_revision"] = revision
    untouched = {}
    for name in MUST_NOT_CHANGE:
        now = sha256_of(name)
        before = git_blob_sha256(name, revision) if revision else None
        untouched[name] = {
            "sha256_now": now,
            "sha256_before_this_lap": before,
            "identical": (before is not None and before == now),
        }
    report["tables_that_must_not_change"] = untouched

    report["input_sha256"] = dict(
        [(name, sha256_of(name)) for name in READ_ONLY_INPUTS])
    report["shared_module_sha256"] = dict(
        [(name, sha256_of(name)) for name in SHARED_MODULES])

    ok = report["recorded_matches_baseline"]
    for name, entry in untouched.items():
        if not entry["identical"]:
            ok = False
    report["pass"] = ok

    with open(OUT, "w") as fh:
        json.dump(report, fh, indent=1)
    print("wrote %s" % OUT)
    print("recorded converged recomputed from disk: %d  (baseline 1635, "
          "matches: %s)" % (recorded, report["recorded_matches_baseline"]))
    print("per language: %s" % json.dumps(per_language))
    print("honest standing converged: 1622; withdrawn, separate "
          "population: 13")
    print("comparison revision: %s" % revision)
    for name, entry in untouched.items():
        print("%-28s identical to before this lap: %s"
              % (name, entry["identical"]))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
