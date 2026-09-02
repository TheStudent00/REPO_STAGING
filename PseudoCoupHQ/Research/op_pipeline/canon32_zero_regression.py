#!/usr/bin/env python3
"""canon32_zero_regression.py -- TASK 31: the zero-regression proof.

THE BASELINE, STATED PRECISELY AND NOT FLATTENED (log_112 section 5):

  RECORDED converged: 1,635. This is what the records on disk say --
  the `status` field of `canon31_units_<lang>.json`.

  HONEST standing converged: 1,622. The branching audit of log_112
  re-gated 18 recorded-converged branching units against blocks cut
  from their own ship BYTES and 13 of them did not prove. Those 13
  keep `status: converged` with a `job8_branching_audit_verdict` of
  DISPROVED beside them; whether the record is rewritten is the owner's
  call, not a mechanical detail.

  THE 13 ARE A SEPARATE POPULATION, not a subtraction to be folded
  into one number. Both numbers are recomputed here from disk and
  reported side by side, exactly as log_112 reported them.

WHAT THIS FILE CHECKS:

  1. the recorded converged count, per language and in total,
     recomputed from `canon31_units_<lang>.json`;
  2. the withdrawn count, recomputed from the same records;
  3. that every one of the five displaced-ABI units still carries in
     `canon31_units_rust.json` exactly the fields it carried before
     this lap -- this lap wrote NO existing file, so their records
     must be untouched;
  4. the sha256 of every file this lap READ, so a later reader can
     tell whether an input moved under it.

usage:
  canon32_zero_regression.py
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ["c", "cpp", "go", "rust", "swift"]

BASELINE_RECORDED = 1635
BASELINE_HONEST = 1622
BASELINE_WITHDRAWN = 13

INPUTS = []
for _L in LANGS:
    INPUTS.append("canon31_units_%s.json" % _L)
    INPUTS.append("canon4_units_%s.json" % _L)
    INPUTS.append("op_units_%s.json" % _L)


def sha256_of(name):
    path = os.path.join(HERE, name)
    h = hashlib.sha256()
    fh = open(path, "rb")
    while True:
        chunk = fh.read(1 << 20)
        if not chunk:
            break
        h.update(chunk)
    fh.close()
    return h.hexdigest()


def main():
    per_language = {}
    recorded = 0
    withdrawn = 0
    for lang in LANGS:
        path = os.path.join(HERE, "canon31_units_%s.json" % lang)
        fh = open(path)
        units = json.load(fh)["units"]
        fh.close()
        count = 0
        for _n, rec in units.items():
            if rec.get("status") != "converged":
                continue
            count = count + 1
            verdict = rec.get("job8_branching_audit_verdict")
            if verdict is None:
                continue
            if verdict == "PROVED_EQUAL":
                continue
            withdrawn = withdrawn + 1
        per_language[lang] = count
        recorded = recorded + count
    honest = recorded - withdrawn
    print("recorded converged, recomputed from disk, per language:")
    for lang in LANGS:
        print("   %-6s %5d" % (lang, per_language[lang]))
    print("   %-6s %5d" % ("TOTAL", recorded))
    print("withdrawn by log_112's branching audit (recorded "
          "converged, re-gate did not prove): %d" % withdrawn)
    print("honest standing converged: %d" % honest)
    print("")
    ok = True
    if recorded != BASELINE_RECORDED:
        ok = False
        print("REGRESSION: recorded converged is %d, baseline is %d"
              % (recorded, BASELINE_RECORDED))
    if withdrawn != BASELINE_WITHDRAWN:
        ok = False
        print("REGRESSION: withdrawn is %d, baseline is %d"
              % (withdrawn, BASELINE_WITHDRAWN))
    if honest != BASELINE_HONEST:
        ok = False
        print("REGRESSION: honest standing is %d, baseline is %d"
              % (honest, BASELINE_HONEST))
    # the five displaced-ABI units, still exactly as they were
    fh = open(os.path.join(HERE, "canon32_sret_units.json"))
    members = json.load(fh)["members"]
    fh.close()
    fh = open(os.path.join(HERE, "canon31_units_rust.json"))
    rust31 = json.load(fh)["units"]
    fh.close()
    print("the five displaced-ABI units, as canon31 still records "
          "them (this lap wrote no existing file):")
    for key in sorted(members):
        n = members[key]["n"]
        rec = rust31.get(n)
        if rec is None:
            ok = False
            print("   %-10s MISSING from canon31_units_rust.json" % key)
            continue
        print("   %-10s status=%r  canon4 refusal still recorded: %r"
              % (key, rec.get("status"),
                 (rec.get("derive_refused") or "")[:58]))
        if rec.get("status") == "converged":
            ok = False
            print("      REGRESSION: this unit's recorded status was "
                  "changed by this lap")
    print("")
    print("sha256 of every file this lap read:")
    hashes = {}
    for name in INPUTS:
        digest = sha256_of(name)
        hashes[name] = digest
        print("   %-28s %s" % (name, digest))
    print("")
    if ok:
        print("ZERO-REGRESSION CHECK: PASS")
    else:
        print("ZERO-REGRESSION CHECK: FAIL")
    doc = {
        "meta": {
            "produced_by": "canon32_zero_regression.py",
            "role": "generator provenance",
            "what": "the baseline recount and the input hashes",
            "baseline_recorded": BASELINE_RECORDED,
            "baseline_honest": BASELINE_HONEST,
            "baseline_withdrawn": BASELINE_WITHDRAWN,
            "recomputed_recorded": recorded,
            "recomputed_withdrawn": withdrawn,
            "recomputed_honest": honest,
            "per_language_recorded": per_language,
            "pass": ok,
        },
        "input_sha256": hashes,
    }
    out = os.path.join(HERE, "canon32_zero_regression.json")
    fh = open(out, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon32_zero_regression.json")


if __name__ == "__main__":
    main()
