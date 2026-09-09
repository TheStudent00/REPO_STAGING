#!/usr/bin/env bash
# ap1_l9_repose.sh -- task ap1: what the ONE re-pose at 30,000 ms moved.
#
# WHY THIS LANE: the law's rule is that a time limit is a FLAG -- re-run
# with more room and report whether the answer changed. The loop poses
# every gate call at the pipeline's own 3,000 ms, keeps that as the
# verdict of record, and re-poses every UNDECIDED once at 30,000 ms.
# This lane counts, over all 1,012 runs, how many places were re-posed
# and what each re-pose answered, so "whether the answer changed" is a
# number rather than a sentence.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import resource

AGG = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/autopoly.json")
document = json.load(open(AGG))

posed = 0
answers = {}
moved = []
for run in document["runs"]:
    for place in (run.get("places") or []):
        check = place.get("check") or {}
        again = check.get("recheck")
        if again is None:
            continue
        posed = posed + 1
        outcome = again.get("outcome")
        answers.setdefault(outcome, 0)
        answers[outcome] = answers[outcome] + 1
        if outcome == "UNDECIDED":
            continue
        moved.append((run["mnem"], run["shape"], run["key_width"],
                      run["lang"], place["writes"], run["route"],
                      run["attested_ledger_rows"], outcome))
print("places re-posed at 30000 ms: %d" % posed)
for outcome in sorted(answers):
    print("   %-16s %d" % (outcome, answers[outcome]))
print("")
print("the places whose answer MOVED:")
for one in moved:
    print("   %-10s %-12s %-5s %-6s [%s] route %-16s %d rows -> %s"
          % (one[0], one[1], one[2], one[3], one[4], one[5], one[6],
             one[7]))
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
