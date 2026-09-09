#!/usr/bin/env bash
# ap1_l7_report_evidence.sh -- task ap1: the report written again with
# the `sat` section split into its two counts, and every figure the
# DevComms log quotes, printed by the machine that holds it.
#
# WHAT THIS LANE ANSWERS, each with the command above it:
#  * the store and the aggregate hold the same 1,012 runs, checked
#    rather than assumed;
#  * how many `sat` verdicts survive task o7's caller-extension
#    re-pose, which is the number Table 1 counts;
#  * why one of the handful's ten cells is not in this loop's outer set
#    at all (`sub` imm_gpr 64), read off task m1's own attestation file;
#  * the four routes' totals over the whole loop;
#  * the cells proved on all four targets, on three, two, one, none.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/5] the report, written again"
python3 autopoly.py report
echo "[2/5] the store and the aggregate hold the same runs"
python3 - <<'PY'
import json
import resource

RUNS = ("PseudoCoupHQ/Research/oracle/cross_construction/"
        "emulation/autopoly/autopoly_runs.jsonl")
AGG = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/autopoly.json")

lines = []
for line in open(RUNS):
    if not line.strip():
        continue
    lines.append(json.loads(line))
document = json.load(open(AGG))
runs = document["runs"]
print("lines on the store: %d" % len(lines))
print("runs on the aggregate: %d" % len(runs))
same = 0
for one, two in zip(lines, runs):
    if json.dumps(one, sort_keys=True) == json.dumps(two, sort_keys=True):
        same = same + 1
print("run for run identical: %d" % same)
keys = set()
for run in runs:
    keys.add((run["mnem"], run["shape"], run["key_width"], run["lang"]))
print("distinct (cell, target) pairs: %d" % len(keys))
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "[3/5] the sat verdicts, and how many survive the re-pose"
python3 - <<'PY'
import json
import resource

AGG = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/autopoly.json")
document = json.load(open(AGG))
held = document["sat_verdicts"]
survived = []
for entry in held:
    if entry.get("under_caller_extension") == "PROVED_ON_SHIP":
        continue
    survived.append(entry)
print("sat at the plain comparison, every written place: %d" % len(held))
print("sat surviving the caller-extension re-pose: %d" % len(survived))
by_lang = {}
for entry in survived:
    by_lang.setdefault(entry["lang"], 0)
    by_lang[entry["lang"]] = by_lang[entry["lang"]] + 1
for lang in sorted(by_lang):
    print("   %-6s %d" % (lang, by_lang[lang]))
print("the five surviving sat places with the most ledger rows:")
for entry in survived[:5]:
    print("   %-10s %-12s %-5s %-6s [%s] %d rows"
          % (entry["mnem"], entry["shape"], entry["key_width"],
             entry["lang"], entry["writes"], entry["ledger_rows"]))
    print("      counterexample: %s" % entry["counterexample"])
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "[4/5] why one handful cell is not in this outer set"
python3 - <<'PY'
import json
import resource

ATTEST = ("PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
          "model_table_attest.json")
document = json.load(open(ATTEST))
for cell in document["cells"]:
    if cell["mnem"] != "sub":
        continue
    print("sub %-10s key_width %-5s ledger_rows %d units %d"
          % (cell["shape"], cell["key_width"], cell["ledger_rows"],
             cell["units"]))
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "[5/5] the routes and the across-target counts"
python3 - <<'PY'
import json
import resource

AGG = ("PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly/autopoly.json")
document = json.load(open(AGG))
print("| route | c | rust | go | swift |")
print("|---|---|---|---|---|")
for name in ("primitive", "primitive+setup", "term", "no route reached"):
    row = [name]
    for lang in ("c", "rust", "go", "swift"):
        row.append("%d" % document["routes"][lang][name]["runs"])
    print("| %s |" % " | ".join(row))
print("")
print("| proved on | cells | ledger rows | share |")
print("|---|---|---|---|")
for many in ("4", "3", "2", "1", "0"):
    held = document["across_targets"][many]
    print("| %s of 4 | %d | %d | %s%% |"
          % (many, held["cells"], held["ledger_rows"],
             held["share_percent"]))
print("")
print("attested ledger rows over the whole outer set: %d"
      % document["ledger_rows_total"])
print("seconds per target: %s" % json.dumps(document["seconds"],
                                            sort_keys=True))
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
