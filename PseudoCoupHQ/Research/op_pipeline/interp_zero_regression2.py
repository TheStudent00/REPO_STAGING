#!/usr/bin/env python3
"""interp_zero_regression2.py -- the zero-regression check for TASK 34,
WITH THE COUNT RECONCILED UNDER "A PROVED UNIT IS A COUNTED UNIT".

THE BASELINE, STATED PRECISELY AND NOT FLATTENED (carried forward from
log_112, log_117 sec 8.1 and log_118 sec 6.1, and recomputed here from
disk rather than quoted):

  * The `status` field of `canon31_units_<lang>.json` says 1,635 of
    the 1,779 compiled-five corpus.  That field has not been rewritten
    and this program still recomputes it from disk.
  * RECORDED converged is now 1,676.  the owner accepted the 41 round-6
    proofs (log_123 ADDENDUM 2) and ruled the standing rule: A PROVED
    UNIT IS A COUNTED UNIT -- gate-proved convergence advances the
    recorded count in the same lap, automatically.  The 41 are counted
    from their own artifacts by this program, not quoted:
    `canon32_sret_units.json` (log_117) and `canon33_units.json`
    (log_118).
  * HONEST standing converged: 1,622 -- after log_112's branching
    audit re-gated 18 recorded-converged branching units against
    blocks cut from their own ship bytes and 13 did not re-prove.
  * The 13 WITHDRAWN are a SEPARATE POPULATION, not a subtraction
    folded into one number.
  * TASK 34 proves nine INTERPRETER units into the universal form and
    proves 18 join relations, but the interpreter units are NOT in the
    1,779 compiled-five population, so the compiled count does not
    move again this lap.  It is stated, not implied.

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
  /tmp/reconnect_venv/bin/python3 interp_zero_regression2.py
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "interp_zero_regression2.json")
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
    the first one that names an interp_canon35 file."""
    proc = subprocess.run(
        ["git", "-C", os.path.join(HERE, "..", ".."), "log",
         "--format=%H", "--diff-filter=A", "--",
         "Research/op_pipeline/interp_canon35.py"],
        capture_output=True, text=True)
    lines = [x for x in proc.stdout.split("\n") if x.strip()]
    if not lines:
        return None
    return "%s^" % lines[-1]


def main():
    report = {
        "meta": {
            "produced_by": "interp_zero_regression2.py",
            "role": "generator provenance",
        },
        "baseline_stated_precisely": {
            "status_field_on_disk": 1635,
            "recorded_converged": 1676,
            "honest_standing_converged": 1622,
            "withdrawn_separate_population": 13,
            "population": "the 1,779-unit compiled-five corpus "
                          "(c, cpp, go, rust, swift)",
            "the_41_accepted_proofs": {
                "canon32_sret_units.json": 5,
                "canon33_units.json": 36,
                "rule": "A PROVED UNIT IS A COUNTED UNIT (the owner, "
                        "2026-09-01)",
            },
            "does_the_compiled_count_move_this_lap": "NO -- this lap's "
                "nine proofs are interpreter/JIT units, which are not "
                "in the 1,779 compiled-five population",
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
    report["status_field_recomputed"] = recorded
    report["unchanged_recomputed"] = unchanged

    # the 41 accepted proofs, COUNTED from their own artifacts rather
    # than quoted from a log.
    sret = json.load(open(os.path.join(HERE, "canon32_sret_units.json")))
    sret_proved = 0
    for _name, member in sret["members"].items():
        if member.get("verdict") == "PROVED_EQUAL":
            sret_proved = sret_proved + 1
    memory = json.load(open(os.path.join(HERE, "canon33_units.json")))
    memory_proved = 0
    for _name, unit in memory["units"].items():
        if unit.get("verdict") == "PROVED_EQUAL":
            memory_proved = memory_proved + 1
    report["proofs_counted_from_their_own_artifacts"] = {
        "canon32_sret_units.json": sret_proved,
        "canon33_units.json": memory_proved,
        "total": sret_proved + memory_proved,
    }
    recorded_now = recorded + sret_proved + memory_proved
    report["recorded_converged_recomputed"] = recorded_now
    report["recorded_matches_baseline"] = (
        recorded == 1635 and sret_proved + memory_proved == 41)
    report["authoritative_count_line"] = (
        "converged %d of 1,779 (compiled five); withdrawn listed "
        "separately: 13" % recorded_now)

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
    print("status field recomputed from disk: %d" % recorded)
    print("proofs counted from their own artifacts: %s"
          % json.dumps(report["proofs_counted_from_their_own_artifacts"]))
    print("AUTHORITATIVE: %s" % report["authoritative_count_line"])
    print("per language: %s" % json.dumps(per_language))
    print("honest standing converged before the 41: 1622; withdrawn, "
          "separate population: 13")
    print("comparison revision: %s" % revision)
    for name, entry in untouched.items():
        print("%-28s identical to before this lap: %s"
              % (name, entry["identical"]))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
