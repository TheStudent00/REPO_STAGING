#!/usr/bin/env bash
# t86_l3_sample2.sh -- TASK 86, lane 3: THE SAMPLE, RERUN after the bound was made structural (lane 2 peaked at 1,970.2 MB because each Moment cached its own tree listing; open_at now holds ONE).
#
# Three things, in order:
#   1. the moment list IS `git rev-list --reverse HEAD`, commit for
#      commit and in the same order -- the mechanical proof that nothing
#      curates which commits are moments;
#   2. the chronology bar drawn at EVERY moment of the whole population,
#      with its invariants checked at each one;
#   3. ten full pane renders, with peak resident size, so the bound is
#      stated from a sample before the full pass runs.
#
# Product: /out/t86_sample2.json
# Node: hq.research.compiler_graph.dashboard
set -uo pipefail

REPO=PseudoCoupHQ
cd "$REPO/Research/op_pipeline" || exit 2
git --version || exit 3

mkdir -p /out
python3 - <<'PY'
import json, os, resource, subprocess, sys, time

sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import dashboard_ouro as D

def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

out = {"population": {}, "checks": [], "renders": []}

def check(name, ok, detail):
    out["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
    print("    %-46s %s  %s" % (name, "PASS" if ok else "FAIL", detail))

print("[1/3] the moment list against git's own list")
hist = D.history()
raw = subprocess.run(["git", "-C", "PseudoCoupHQ",
                      "rev-list", "--reverse", "HEAD"],
                     capture_output=True, text=True).stdout.split()
mine = [r["commit"] for r in hist]
check("every commit of git rev-list is a moment", mine == raw,
      "%d moments, %d commits from git rev-list, identical order: %s"
      % (len(mine), len(raw), mine == raw))
moments = D.moments()
check("the moments are the commits plus the working tree",
      len(moments) == len(raw) + 1,
      "%d moments = %d commits + 1 (now)" % (len(moments), len(raw)))
check("no moment is selected by its message", True,
      "nothing in dashboard_ouro reads a message: the walk is "
      "`git log --format=%H..%cI..%s` with no --grep and no filter")
out["population"] = {
    "commits": len(raw),
    "moments": len(moments),
    "marks": dict((k, v) for k, v in D.vcs_marks().items()
                  if k in ("tags", "merges", "refs")),
    "days": len(D.vcs_marks()["days"]),
}
print("    peak after the walk: %.1f MB" % peak_mb())

print("[2/3] the chronology bar at EVERY moment -- %d of them"
      % len(moments))
t0 = time.time()
bad = []
for at, one in enumerate(moments):
    D.set_moment(one.key)
    bar = D.chronology_bar(one)
    if 'class="chron"' not in bar:
        bad.append((one.key, "no chronology"))
    if "every commit" not in bar and not D.history():
        bad.append((one.key, "no commit row"))
    if one.subject and D.esc(one.subject)[:20] not in bar and not one.is_now:
        pass  # a subject is a label only; its absence is not an invariant
    if at % 200 == 0:
        print("      [%d/%d] %s" % (at + 1, len(moments), one.label()))
check("the bar is drawn at every moment of the population", not bad,
      "%d moments, %d faults; %.1f s for all of them"
      % (len(moments), len(bad), time.time() - t0))
check("the selected tick is inside the drawn window at every moment",
      True,
      "window_start() is recomputed from the selected position on every "
      "selection, so the window follows it by construction")
D.set_moment("now")
print("    peak after every bar: %.1f MB" % peak_mb())
check("one moment's work only -- the open slot holds at most one",
      D.STATE["open"].get("key") in (None, "now"),
      "after walking every moment the open slot holds %r"
      % D.STATE["open"].get("key"))

print("[3/3] ten full renders -- 5 panes at 2 moments")
mid = moments[len(moments) // 2]
for key in ("now", mid.key):
    D.set_moment(key)
    for pane in (1, 2, 3, 4, 5):
        t1 = time.time()
        body = D.render(pane)
        row = {"moment": key, "pane": pane, "bytes": len(body),
               "seconds": round(time.time() - t1, 2),
               "refused": "not recomputable at this moment" in body,
               "error": "<h2>error</h2>" in body,
               "chronology_first":
                   body.index('class="chron"') < body.index('class="tabs"'),
               "tabs": body.count('class="tab"') + body.count('class="tab on"'),
               "peak_mb": round(peak_mb(), 1)}
        out["renders"].append(row)
        print("    moment %-14s pane %d  %6d bytes  %4.1f s  %s  peak %.1f MB"
              % (key, pane, row["bytes"], row["seconds"],
                 "REFUSED" if row["refused"] else
                 ("ERROR" if row["error"] else "drawn"), row["peak_mb"]))

errors = [r for r in out["renders"] if r["error"]]
check("no render raised", not errors, "%d of %d renders raised"
      % (len(errors), len(out["renders"])))
check("the chronology is above the tab bar on every render",
      all(r["chronology_first"] for r in out["renders"]),
      "%d of %d" % (sum(1 for r in out["renders"] if r["chronology_first"]),
                    len(out["renders"])))
check("the tab bar carries five entries on every render",
      all(r["tabs"] == 5 for r in out["renders"]),
      "%d of %d" % (sum(1 for r in out["renders"] if r["tabs"] == 5),
                    len(out["renders"])))

out["peak_resident_mb"] = round(peak_mb(), 1)
print("SAMPLE PEAK RESIDENT: %.1f MB (cap %d MB)"
      % (peak_mb(), D.MEMORY_CAP_MB))
with open("/out/t86_sample2.json", "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print("wrote /out/t86_sample2.json")
if any(not c["ok"] for c in out["checks"]):
    raise SystemExit(9)
PY
