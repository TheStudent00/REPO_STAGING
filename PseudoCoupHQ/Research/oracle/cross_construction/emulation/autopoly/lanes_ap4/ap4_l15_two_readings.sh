#!/usr/bin/env bash
# ap4_l15_two_readings.sh -- task ap4: two counts the report's tables do
# not make on their own, each generated rather than hand-counted.
#
#  [1] the 114 runs of `answer home or arrival on the x87 stack`, split
#      by target and by which cells they are, so "refused by nature"
#      can be told from anything else.
#  [2] the 12 runs still carrying `this unit record carries no body`,
#      with the carved body LITERAL of each.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import sys
sys.path.insert(0, os.getcwd())
import autopoly4 as A

A.use_task_ap4()
runs = A.read_runs()

print("[1/2] `answer home or arrival on the x87 stack`, by target")
by_lang = {}
cells = set()
for run in runs:
    cause = A.cause_of(run)
    if cause is None or "on the x87 stack" not in cause:
        continue
    by_lang[run["lang"]] = by_lang.get(run["lang"], 0) + 1
    cells.add((run["mnem"], run["shape"], run["key_width"]))
print("   runs: %d over %d distinct cells" % (sum(by_lang.values()),
                                              len(cells)))
for lang in sorted(by_lang):
    print("      %-6s %d" % (lang, by_lang[lang]))
print("   the cells on c, which are the ones NOT refused by nature:")
for run in runs:
    cause = A.cause_of(run)
    if cause is None or "on the x87 stack" not in cause:
        continue
    if run["lang"] != "c":
        continue
    place = A.the_weakest_place(run)
    print("      `%s` %s %s  place `%s`  %s"
          % (run["mnem"], run["shape"], run["key_width"],
             (place or {}).get("writes"),
             A.first_line((place or {}).get("refusal_detail") or "")))

print("")
print("[2/2] the runs still carrying `this unit record carries no body`")
for run in runs:
    cause = A.cause_of(run)
    if cause is None or "carries no body" not in cause:
        continue
    place = A.the_weakest_place(run)
    print("   `%s` %s %s / %s  body: %s"
          % (run["mnem"], run["shape"], run["key_width"], run["lang"],
             ((place or {}).get("body_text") or "")[:110]))
print("")
print("peak resident: %d kB" % A.peak_kb())
PY
echo "done"
