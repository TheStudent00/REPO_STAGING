#!/usr/bin/env bash
# t85_l4_all_moments2.sh -- TASK 85, lane 4: THE FULL PASS, RE-RUN.
#
# Every pane rendered at every moment, so that "which panes recompute and
# which refuse" is a MEASUREMENT and not a claim.  Population: 5 panes x
# 40 moments (39 chronology steps + the present moment) = 200 renders.
#
# THE MEMORY BOUND, stated before the run.
#   what is held:  ONE moment's index, shard maps and pool map.  Selecting
#                  the next moment drops all of them (dashboard_ouro.
#                  set_moment) before the next is read, so memory does not
#                  grow with the number of moments visited -- which is the
#                  whole reason this pass is affordable at all.
#   page cap:      MEMORY_CAP_MB = 1500 MB, abort OURO_MEMORY_ABORT.
#   lane cap:      6000 MB, abort T85_FULL_MEMORY_ABORT2, checked after
#                  every render.
#   sample first:  t85_l2_sample.sh, 10 renders, measured peak 223.6 MB.
#   to beat:       402.3 MB (log_184, the present-day page's whole-process
#                  peak over all its panes).
#
# Re-run of lane 3 after the defect lane 3 FOUND was fixed: three of its
# 200 renders raised TypeError because an older pool generation carries a
# nested object where the present one carries a count (dashboard_ouro.
# count_cell).  This lane also counts the tab bar correctly -- lane 3
# counted `class="tab "` and so saw only the ACTIVE tab -- and it proves
# the one-moment rule directly: one moment change, more than one pane
# different.
#
# Product: /out/t85_all_moments2.json
set -uo pipefail

cd PseudoCoupHQ/Research/op_pipeline || exit 2
mkdir -p /out

python3 - <<'PY'
import json, os, re, resource, sys, time

sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import dashboard_ouro as dash

LANE_CAP_MB = 6000
LANE_ABORT = "T85_FULL_MEMORY_ABORT2"
POP = re.compile(r'<div class="pop">(.*?)</div>', re.S)


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


keys = [one.key for one in dash.moments()]
total = len(keys) * 5
rows = []
i = 0
started_all = time.time()
for key in keys:
    dash.set_moment(key)
    moment = dash.current_moment()
    for number in (1, 2, 3, 4, 5):
        i += 1
        started = time.time()
        html = dash.render(number)
        seconds = time.time() - started
        rss = peak()
        if rss > LANE_CAP_MB:
            raise SystemExit("%s: peak resident size %.1f MB passed the "
                             "lane's stated cap of %d MB at pane %d, "
                             "moment %s" % (LANE_ABORT, rss, LANE_CAP_MB,
                                            number, key))
        refused = "not recomputable at this moment" in html
        error = "<h2>error</h2>" in html
        found = POP.search(html)
        pop = found.group(1).strip() if found else ""
        index = dash.STATE.get("index") or {}
        rows.append({
            "moment": key,
            "day": moment.day or "now",
            "commit": (moment.commit or "")[:10],
            "round": moment.round,
            "pane": number,
            "pane_name": dict(dash.PANE_NAMES)[number],
            "seconds": round(seconds, 2),
            "peak_rss_mb": round(rss, 1),
            "characters": len(html),
            "refused": refused,
            "error": error,
            "index_rows": len(index.get("rows") or []),
            "population_line": pop,
            "chronology_drawn": 'class="chron"' in html,
            "chronology_above_tabs": (html.find('class="chron"') > -1
                                      and html.find('class="chron"')
                                      < html.find('class="tabs"')),
            "tabs_in_bar": html.count('class="tab"') + html.count('class="tab on"'),
            "ticks_in_chronology": html.count('class="tick'),
        })
        print("[%d/%d] %s pane %d %-18s %7d chars %6.2f s peak %6.1f MB "
              "rows %6d%s%s"
              % (i, total, key.rjust(3), number,
                 dict(dash.PANE_NAMES)[number], len(html), seconds, rss,
                 len(index.get("rows") or []),
                 "  REFUSED" if refused else "",
                 "  ERROR" if error else ""))
        if error:
            at = html.find("<pre>")
            print("       " + html[at:at + 400].replace("\n", " "))

# --- the answers this lane exists to give ---------------------------
recompute = {}
refuse = {}
errors = 0
for row in rows:
    bucket = refuse if row["refused"] else recompute
    bucket.setdefault(row["pane"], []).append(row["moment"])
    if row["error"]:
        errors += 1

summary = {
    "population": "%d renders — 5 panes x %d moments (%d chronology steps "
                  "and the present moment)" % (total, len(keys), len(keys) - 1),
    "moments": len(keys),
    "errors": errors,
    "peak_rss_mb": round(peak(), 1),
    "lane_cap_mb": LANE_CAP_MB,
    "lane_abort": LANE_ABORT,
    "page_cap_mb": dash.MEMORY_CAP_MB,
    "page_abort": dash.ABORT_NAME,
    "seconds": round(time.time() - started_all, 1),
    "per_pane": {
        str(number): {
            "name": dict(dash.PANE_NAMES)[number],
            "recomputed_at": len(recompute.get(number, [])),
            "refused_at": len(refuse.get(number, [])),
            "recomputed_moments": recompute.get(number, []),
            "refused_moments": refuse.get(number, []),
        }
        for number in (1, 2, 3, 4, 5)
    },
    "tab_bar_entries": sorted({row["tabs_in_bar"] for row in rows}),
    "chronology_drawn_on_every_render":
        all(row["chronology_drawn"] for row in rows),
    "chronology_above_tabs_on_every_render":
        all(row["chronology_above_tabs"] for row in rows),
    "renders": rows,
}
with open("/out/t85_all_moments2.json", "w") as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)

print()
print("errors: %d of %d renders" % (errors, total))
print("chronology drawn on every render: %s"
      % summary["chronology_drawn_on_every_render"])
print("chronology ABOVE the tab bar on every render: %s"
      % summary["chronology_above_tabs_on_every_render"])
print("tab-bar entries seen, over all %d renders: %s"
      % (total, summary["tab_bar_entries"]))
for number in (1, 2, 3, 4, 5):
    one = summary["per_pane"][str(number)]
    print("pane %d %-18s recomputed at %2d of %d moments, refused at %2d"
          % (number, one["name"], one["recomputed_at"], len(keys),
             one["refused_at"]))
print("FULL PASS PEAK RESIDENT SIZE: %.1f MB, page cap %d MB, lane cap %d MB"
      % (peak(), dash.MEMORY_CAP_MB, LANE_CAP_MB))

# --- THE ONE-MOMENT RULE, proved directly ---------------------------
print()
print("== one moment, applied to all of them: the SAME two panes at two "
      "moments")
proof = {}
for key in ("now", "31"):
    dash.set_moment(key)
    for number in (2, 5):
        html = dash.render(number)
        found = POP.search(html)
        proof["%s/%d" % (key, number)] = found.group(1).strip() if found else ""
        print("  moment %-4s pane %d: %s"
              % (key, number, proof["%s/%d" % (key, number)][:150]))
same = (proof["now/2"] == proof["31/2"], proof["now/5"] == proof["31/5"])
print("  pane 2 unchanged by the moment change: %s" % same[0])
print("  pane 5 unchanged by the moment change: %s" % same[1])
print("  MORE THAN ONE PANE CHANGED: %s" % (not same[0] and not same[1]))
with open("/out/t85_one_moment_proof.json", "w") as fh:
    json.dump({"population": "2 panes x 2 moments = 4 renders",
               "population_lines": proof,
               "pane_2_changed": not same[0],
               "pane_5_changed": not same[1],
               "more_than_one_pane_changed": (not same[0]) and (not same[1])},
              fh, indent=1, sort_keys=True)
PY