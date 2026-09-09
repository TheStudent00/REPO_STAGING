#!/usr/bin/env bash
# t86_l7_all_panes2.sh -- TASK 86, lane 7: THE FULL PASS OF RECORD, against the final code (lane 4 ran before the window shifts were added -- the run that FOUND, through the screenshot rig, that a day of 521 commits is not one windowful).
#
# Five panes rendered at a MECHANICALLY SPACED sample of the moment
# population, plus the present moment.  The sample is every k-th
# position of the history, k = (commits - 1) / 39 -- a rule over
# POSITIONS, not over content: no commit is chosen for what its message
# says, and the whole population is stated beside the sample.
#
# What it answers:
#   * does any render raise;
#   * is the chronology above the tab bar on every one of them, and does
#     the tab bar carry five entries;
#   * which panes can be recomputed at which moments, and which draw the
#     refusal;
#   * does ONE moment change alter MORE THAN ONE pane;
#   * what it all peaks at, against the 1,500 MB cap.
#
# Product: /out/t86_all_panes2.json
# Node: hq.research.compiler_graph.dashboard
set -uo pipefail

REPO=PseudoCoupHQ
cd "$REPO/Research/op_pipeline" || exit 2

mkdir -p /out
python3 - <<'PY'
import json, os, resource, sys, time

sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import dashboard_ouro as D

def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

order = D.moments()
commits = len(D.history())
WANT = 40
picks = []
for i in range(WANT):
    at = int(round(i * (commits - 1) / float(WANT - 1)))
    if at not in picks:
        picks.append(at)
picks.append(len(order) - 1)          # the present moment
total = len(picks) * 5
print("population: %d commits + the working tree = %d moments; this pass "
      "draws 5 panes at %d of them (every %.1fth position, plus now) = %d "
      "renders" % (commits, len(order), len(picks),
                   (commits - 1) / float(WANT - 1), total))

rows = []
step = 0
t_all = time.time()
for at in picks:
    one = order[at]
    D.set_moment(one.key)
    for pane in (1, 2, 3, 4, 5):
        step += 1
        t0 = time.time()
        body = D.render(pane)
        refused = "not recomputable at this moment" in body
        errored = "<h2>error</h2>" in body
        rows.append({
            "position": at,
            "key": one.key,
            "stamp": one.stamp(),
            "pane": pane,
            "bytes": len(body),
            "seconds": round(time.time() - t0, 2),
            "refused": refused,
            "error": errored,
            "chronology_drawn": 'class="chron"' in body,
            "chronology_above_tabs":
                body.index('class="chron"') < body.index('class="tabs"'),
            "tabs": body.count('class="tab"') + body.count('class="tab on"'),
            "peak_mb": round(peak_mb(), 1),
        })
        print("[%d/%d] %s  pane %d  %6d bytes  %5.1f s  %-8s peak %.1f MB"
              % (step, total, one.label(), pane, len(body),
                 rows[-1]["seconds"],
                 "REFUSED" if refused else ("ERROR" if errored else "drawn"),
                 rows[-1]["peak_mb"]))

print("-- one moment change, more than one pane different")
proof = {}
D.set_moment("now")
before = dict((p, D.render(p)) for p in (1, 2, 3, 4, 5))
late = order[int(round(0.985 * (commits - 1)))]
D.set_moment(late.key)
after = dict((p, D.render(p)) for p in (1, 2, 3, 4, 5))
changed = [p for p in (1, 2, 3, 4, 5) if before[p] != after[p]]
proof = {"from": "now", "to": late.key, "to_stamp": late.stamp(),
         "panes_changed": changed,
         "panes_compared": [1, 2, 3, 4, 5]}
print("   one click from now to %s (%s): panes changed = %s"
      % (late.key, late.stamp(), changed))

errors = [r for r in rows if r["error"]]
drawn = [r for r in rows if not r["refused"] and not r["error"]]
by_pane = {}
for r in rows:
    key = str(r["pane"])
    by_pane.setdefault(key, {"drawn": 0, "refused": 0, "moments": len(picks)})
    by_pane[key]["refused" if r["refused"] else "drawn"] += 1

doc = {
    "population": {"commits": commits, "moments": len(order),
                   "moments_sampled": len(picks), "renders": len(rows),
                   "rule": "every (commits-1)/39-th position of the "
                           "history, plus the working tree"},
    "renders": rows,
    "errors": len(errors),
    "chronology_drawn": sum(1 for r in rows if r["chronology_drawn"]),
    "chronology_above_tabs": sum(1 for r in rows
                                 if r["chronology_above_tabs"]),
    "tab_bar_five": sum(1 for r in rows if r["tabs"] == 5),
    "by_pane": by_pane,
    "one_moment_change": proof,
    "peak_resident_mb": round(peak_mb(), 1),
    "seconds": round(time.time() - t_all, 1),
}
with open("/out/t86_all_panes2.json", "w") as fh:
    json.dump(doc, fh, indent=1, sort_keys=True)

print("")
print("renders            %d" % len(rows))
print("errors             %d" % len(errors))
print("chronology drawn   %d of %d" % (doc["chronology_drawn"], len(rows)))
print("above the tab bar  %d of %d" % (doc["chronology_above_tabs"], len(rows)))
print("tab bar of five    %d of %d" % (doc["tab_bar_five"], len(rows)))
for key in sorted(by_pane):
    print("pane %s             recomputed at %d of %d moments, refused at %d"
          % (key, by_pane[key]["drawn"], by_pane[key]["moments"],
             by_pane[key]["refused"]))
print("PEAK RESIDENT      %.1f MB (cap %d MB)" % (peak_mb(), D.MEMORY_CAP_MB))
print("wrote /out/t86_all_panes2.json")
if errors:
    raise SystemExit(9)
PY
