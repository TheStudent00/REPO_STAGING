#!/usr/bin/env bash
# ap5_l17_guard_check_and_the_handful_b.sh -- task ap5: two of the four
# guards the brief names, which are what prove the two changes to the
# shared files harmless.
#
#  [1] `model_translate.py check`: 259 rows, 172 STATED, 87 REFUSED.
#      Every file `check_command` writes is copied aside before and
#      copied back after, and compared by sha256 -- task ap3's own
#      protection, because the stored `check_L2.json` carries the Lean
#      run's 19 DISCREPANCY verdicts that a fresh `check` cannot know.
#  [2] the h2 handful: `handful.py sources_counts`, 24 of 24 rendered
#      identical to the file task h1 wrote.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
# THE SECOND PASS.  The guards are re-run over the code as this task
# FINALLY leaves it -- lane ap5_l15's fix to `align_by_row`'s new
# branch landed after the first pass of them -- so the tally of
# record is this one.  A lane name is used ONCE, so this is a new
# name and the first pass stays on the record.
set -euo pipefail

echo "[1/2] model_translate.py check -- the tally the brief names"
python3 - <<'PY'
import glob
import hashlib
import json
import os
import shutil

LEAN = "PseudoCoupHQ/Research/op_pipeline/lean"
KEEP = "/tmp/ap5_check_before_b"
if os.path.isdir(KEEP):
    shutil.rmtree(KEEP)
os.makedirs(KEEP)
paths = [os.path.join(LEAN, "check_L2.json")]
paths.extend(sorted(glob.glob(os.path.join(LEAN, "archproof",
                                           "Archproof", "*.lean"))))
index = {}
for number, path in enumerate(paths):
    if not os.path.exists(path):
        continue
    handle = open(path, "rb")
    body = handle.read()
    handle.close()
    kept = os.path.join(KEEP, "f%05d" % number)
    open(kept, "wb").write(body)
    index[path] = [kept, hashlib.sha256(body).hexdigest()]
json.dump(index, open("/tmp/ap5_check_index_b.json", "w"))
print("   files check_command can write, copied aside: %d" % len(index))
document = json.load(open(os.path.join(LEAN, "check_L2.json")))
rows = document.get("rows") or []
counted = {}
for row in rows:
    counted[row.get("outcome")] = counted.get(row.get("outcome"), 0) + 1
print("   the stored tally, off the artifact as it stands")
print("      check_L2.json rows: %d" % len(rows))
for name in sorted(counted):
    print("         %-12s %d" % (name, counted[name]))
PY

cd PseudoCoupHQ/Research/op_pipeline/lean
python3 model_translate.py check 2>&1 | tail -8

python3 - <<'PY'
import hashlib
import json
import os
import shutil

LEAN = "PseudoCoupHQ/Research/op_pipeline/lean"
ART = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly")
shutil.copyfile(os.path.join(LEAN, "check_L2.json"),
                os.path.join(ART, "autopoly5_check_L2_rerun.json"))
document = json.load(open(os.path.join(ART,
                                       "autopoly5_check_L2_rerun.json")))
rows = document.get("rows") or []
counted = {}
for row in rows:
    counted[row.get("outcome")] = counted.get(row.get("outcome"), 0) + 1
print("   the re-derived check, kept as autopoly5_check_L2_rerun.json:"
      " rows %d" % len(rows))
for name in sorted(counted):
    print("      %-12s %d" % (name, counted[name]))

index = json.load(open("/tmp/ap5_check_index_b.json"))
same = 0
moved = []
for path in sorted(index):
    kept, digest = index[path]
    shutil.copyfile(kept, path)
    handle = open(path, "rb")
    got = hashlib.sha256(handle.read()).hexdigest()
    handle.close()
    if got == digest:
        same = same + 1
    else:
        moved.append(path)
if not moved:
    print("   RESTORED IDENTICAL: every file check_command wrote is "
          "back to its stored bytes (%d files)" % same)
else:
    print("   NOT RESTORED: %d file(s) differ" % len(moved))
    for path in moved[:10]:
        print("      %s" % path)
PY

echo ""
echo "[2/2] the h2 handful: sources_counts"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py sources_counts 2>&1 | tail -12
echo "done"
