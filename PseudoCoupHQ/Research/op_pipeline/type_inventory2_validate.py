#!/usr/bin/env python3
"""type_inventory2_validate.py -- TASK 35's validation, run by log_116's
own validator, UNMODIFIED.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check (op_pipeline/check_no_spelling_keys.py)
and refuse its own output on failure.

WHY IT IS SHAPED THIS WAY
-------------------------
The brief says: validate against the corpus EXACTLY as log_116 did.
The strongest reading of "exactly" is not a re-implementation of the
same measurements -- it is the SAME PROGRAM, byte for byte, over the
new inventory. `type_inventory_validate.py` hard-codes its input name
(`type_inventory.json`) and its output names, so this driver:

  1. makes a scratch directory,
  2. symlinks log_116's validator, the spelling guard, and every input
     it reads (op_units_*.json, probe_manifest_*.json, probe_gen.py)
     into it,
  3. symlinks `type_inventory2.json` under the name the validator
     expects, so the validator itself is never edited,
  4. runs it there with the same interpreter,
  5. copies its two outputs back as type_inventory2_validation.json
     and type_inventory2_validation.md,
  6. runs the spelling guard on the copied JSON and refuses its own
     output on failure.

log_116's artifacts are never written to: everything the validator
writes lands in the scratch directory. The driver hashes them before
and after and refuses if any changed.

  /tmp/reconnect_venv/bin/python3 type_inventory2_validate.py
"""

import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GUARDED_UNCHANGED = [
    "type_inventory.json", "type_inventory.md",
    "type_inventory_validation.json", "type_inventory_validation.md",
    "type_inventory.py", "type_inventory_validate.py",
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def snapshot():
    return {n: sha(os.path.join(HERE, n)) for n in GUARDED_UNCHANGED
            if os.path.exists(os.path.join(HERE, n))}


def main():
    before = snapshot()
    work = tempfile.mkdtemp(prefix="type_inventory2_validate_")

    link = ["type_inventory_validate.py", "check_no_spelling_keys.py",
            "probe_gen.py"]
    link += [os.path.basename(p) for p in
             glob.glob(os.path.join(HERE, "op_units_*.json"))]
    link += [os.path.basename(p) for p in
             glob.glob(os.path.join(HERE, "probe_manifest_*.json"))]
    for n in link:
        os.symlink(os.path.join(HERE, n), os.path.join(work, n))
    # the one substitution: the validator's input name points at the
    # superseding inventory
    os.symlink(os.path.join(HERE, "type_inventory2.json"),
               os.path.join(work, "type_inventory.json"))

    p = subprocess.run([sys.executable,
                        os.path.join(work, "type_inventory_validate.py")],
                       capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        raise SystemExit("log_116's validator exited %d" % p.returncode)

    out_json = os.path.join(HERE, "type_inventory2_validation.json")
    out_md = os.path.join(HERE, "type_inventory2_validation.md")
    shutil.copyfile(os.path.join(work, "type_inventory_validation.json"),
                    out_json)
    shutil.copyfile(os.path.join(work, "type_inventory_validation.md"),
                    out_md)

    # stamp the copy so a later reader knows which inventory it measured
    doc = json.load(open(out_json))
    doc["generated_by"] = ("type_inventory_validate.py (UNMODIFIED), driven "
                           "by type_inventory2_validate.py")
    doc["reads"] = ["type_inventory2.json", "op_units_<lang>.json",
                    "probe_manifest_<lang>.json", "probe_gen.py :: HOLDERS"]
    doc["task"] = ("TASK 35 -- the same two-direction validation log_116 ran, "
                   "over the inventory whose swift rows are now extracted")
    json.dump(doc, open(out_json, "w"), indent=1)

    after = snapshot()
    changed = [n for n in before if before[n] != after.get(n)]
    if changed:
        raise SystemExit("REGRESSION: log_116 artifacts changed: %s" % changed)

    g = subprocess.run([sys.executable,
                        os.path.join(HERE, "check_no_spelling_keys.py"),
                        out_json], capture_output=True, text=True)
    sys.stdout.write(g.stdout)
    sys.stderr.write(g.stderr)
    if g.returncode != 0:
        os.remove(out_json)
        raise SystemExit("REFUSED OWN OUTPUT: the spelling-key check failed")

    print("scratch directory: %s" % work)
    print("wrote %s" % out_json)
    print("wrote %s" % out_md)
    print("log_116 artifacts unchanged: %d checked" % len(before))


if __name__ == "__main__":
    main()
