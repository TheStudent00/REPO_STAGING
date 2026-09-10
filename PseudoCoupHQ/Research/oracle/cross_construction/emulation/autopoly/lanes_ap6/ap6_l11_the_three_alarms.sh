#!/bin/bash
# ap6_l11_the_three_alarms.sh -- task ap6, lane 11.
#
# WHAT THIS LANE DOES: it reads the three ALARM rows lane 10 stopped on
# and shows the objects behind them.  The alarm says: for the cell
# `setb gpr_one 8` on cpp at `reg_rdi`, a certificate of kind `proved`
# whose setter cell is `cmp gpr_gpr 8` was matched by a re-derivation of
# kind `sat` on inputs the audit read as IDENTICAL.
#
# WHAT IS ASKED HERE, and nothing is changed by it: every run of that
# (cell, target) on lane 10's own store, with its setter cell, the term
# text of the place, the sha256 of the rendered source and the gate's
# verdict.  If two runs over two setter cells carry the same term text
# and the same source and differ in verdict, that is a real alarm and
# this task stops on it.  If they carry different term texts and the
# audit matched them anyway, the alarm is the AUDIT's own: its key is
# six-part -- (cell, target, place, setter) -- and the matcher compares
# only five of the parts, which was harmless while the loop wrote one
# run per (cell, target) and is not harmless now.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6.  The store
# is streamed line by line and never held whole.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=1

echo "[1/$total] every run of \`setb gpr_one 8\` on cpp, on the store"
python3 - "$A" <<'PY'
import sys, json, hashlib, resource
here = sys.argv[1]
print("| setter cell | place | verdict | source sha256 | term text |")
print("|---|---|---|---|---|")
handle = open(here + "/ap6_delta_runs.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    run = json.loads(text)
    if run["mnem"] != "setb":
        continue
    if run["shape"] != "gpr_one" or run["key_width"] != 8:
        continue
    if run["lang"] != "cpp":
        continue
    setter = run.get("setter") or {}
    for place in run.get("places") or []:
        if place.get("writes") != "reg_rdi":
            continue
        source = place.get("source")
        sha = "--"
        if source is not None:
            sha = hashlib.sha256(source.encode("utf-8")).hexdigest()
        check = place.get("check") or {}
        print("| `%s` %s %s | %s | %s | %s | `%s` |"
              % (setter.get("mnem"), setter.get("shape"),
                 setter.get("key_width"), place.get("writes"),
                 check.get("outcome"), sha[:16],
                 (place.get("text") or "")[:70]))
        continue
    continue
handle.close()
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo
echo "lane done"
