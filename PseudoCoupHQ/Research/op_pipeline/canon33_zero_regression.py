#!/usr/bin/env python3
"""canon33_zero_regression.py -- the zero-regression check for TASK 30.

THE BASELINE, STATED PRECISELY AND NOT FLATTENED (log_112, log_117
section 8.1):

  * RECORDED converged: 1,635 -- what the `status` field of
    canon31_units_<lang>.json says.
  * HONEST standing converged: 1,622 -- after log_112's branching
    audit re-gated 18 recorded-converged branching units against
    blocks cut from their own ship bytes and 13 did not re-prove.
  * The 13 WITHDRAWN are a SEPARATE POPULATION, not a subtraction
    folded into one number.
  * log_117's 5 sret proofs are NOT advanced -- that is the owner's call,
    still open.

WHAT THIS PROGRAM CHECKS:

 1. the recorded counts, recomputed from disk, per language;
 2. that no unit this lap touched has had its recorded status
    rewritten -- every one of the 74 is still exactly what
    canon31_units said;
 3. the sha256 of every input file, and of canon4.py and every other
    shared module this lap imported but did not edit.

usage:
  canon33_zero_regression.py
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

SHARED_MODULES = [
    "canon.py", "canon2.py", "canon4.py",
    "canon5_behaviour_check.py", "canon8_behaviour_check.py",
    "canon10_behaviour_check.py", "real_blocks.py",
    "check_no_spelling_keys.py",
]


def load(name):
    handle = open(os.path.join(HERE, name))
    doc = json.load(handle)
    handle.close()
    return doc


def sha256_of(name):
    handle = open(os.path.join(HERE, name), "rb")
    digest = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    return digest


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main(argv):
    per_language = {}
    total = 0
    unchanged_total = 0
    for lang in LANGS:
        units = load("canon31_units_%s.json" % lang)["units"]
        converged = 0
        unchanged = 0
        for n in units:
            status = units[n].get("status")
            if status == "converged":
                converged = converged + 1
            if status == "unchanged":
                unchanged = unchanged + 1
        per_language[lang] = {"converged": converged,
                              "unchanged": unchanged}
        total = total + converged
        unchanged_total = unchanged_total + unchanged

    log("recorded converged, recomputed from disk, per language:")
    for lang in LANGS:
        log("   %-8s %4d  (plus %d unchanged)"
            % (lang, per_language[lang]["converged"],
               per_language[lang]["unchanged"]))
    log("   %-8s %4d" % ("TOTAL", total))
    log("withdrawn by log_112's branching audit "
        "(recorded converged, re-gate did not prove): 13")
    log("honest standing converged: %d" % (total - 13))
    log("converged-or-unchanged: %d" % (total + unchanged_total))

    lap = load("canon33_units.json")["units"]
    rewritten = []
    for key in sorted(lap):
        row = lap[key]
        units = load("canon31_units_%s.json" % row["lang"])["units"]
        recorded = units[row["n"]].get("status")
        if recorded != row["recorded_status"]:
            rewritten.append("%s: %s -> %s"
                             % (key, row["recorded_status"], recorded))
    log("")
    log("units this lap re-derived: %d" % len(lap))
    log("of those, recorded statuses rewritten by this lap: %d %s"
        % (len(rewritten), rewritten))

    tally = {}
    for key in lap:
        outcome = lap[key]["outcome"]
        tally[outcome] = tally.get(outcome, 0) + 1
    log("this lap's outcomes: %s" % tally)
    newly = tally.get("newly_converged", 0)
    log("")
    log("IF the %d newly proved units were advanced -- NOT done here, "
        "it is a call about the record --" % newly)
    log("   recorded converged would become %d" % (total + newly))
    log("   honest standing would become     %d" % (total - 13 + newly))
    log("   converged-or-unchanged would become %d"
        % (total + unchanged_total + newly))
    log("   the not-converged remainder would become %d"
        % (1779 - total - unchanged_total - newly))

    hashes = {}
    for lang in LANGS:
        for pattern in ["canon31_units_%s.json", "canon4_units_%s.json",
                        "op_units_%s.json", "sem_anchored_%s.json",
                        "sem_anchored_spill_%s.json",
                        "canon_units_%s.json"]:
            name = pattern % lang
            hashes[name] = sha256_of(name)
    for name in SHARED_MODULES:
        hashes[name] = sha256_of(name)
    log("")
    log("sha256 of every shared module this lap imported and did not "
        "edit:")
    for name in SHARED_MODULES:
        log("   %-32s %s" % (name, hashes[name]))

    passed = (len(rewritten) == 0)
    log("")
    log("ZERO-REGRESSION CHECK: %s" % ("PASS" if passed else "FAIL"))

    out = {}
    out["meta"] = {"role": "generator provenance",
                   "produced_by": "canon33_zero_regression.py"}
    out["per_language"] = per_language
    out["recorded_converged"] = total
    out["unchanged"] = unchanged_total
    out["withdrawn_separate_population"] = 13
    out["honest_standing_converged"] = total - 13
    out["this_lap_outcomes"] = tally
    out["recorded_statuses_rewritten"] = rewritten
    out["input_sha256"] = hashes
    out["pass"] = passed
    handle = open(os.path.join(HERE, "canon33_zero_regression.json"),
                  "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    log("wrote canon33_zero_regression.json")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
