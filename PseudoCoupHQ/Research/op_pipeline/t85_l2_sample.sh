#!/usr/bin/env bash
# t85_l2_sample.sh -- TASK 85, lane 2: THE SAMPLE, run before the full pass.
#
# THE MEMORY BOUND, stated before the run.
#   what is held:  ONE moment's index over the whole unit population,
#                  built from the artifact blobs git holds at that
#                  commit.  A unit BODY is never held.
#   page cap:      dashboard_ouro.MEMORY_CAP_MB = 1500 MB, abort named
#                  OURO_MEMORY_ABORT, caught per pane.
#   lane cap:      6000 MB, abort named T85_SAMPLE_MEMORY_ABORT, checked
#                  after every pane render; the lane stops by that name
#                  rather than swapping the machine.
#   to beat:       402.3 MB, the measured whole-process peak of the
#                  present-day page (log_184).
#
# The sample is FOUR renders, not 195: the five panes at ONE past moment
# (the earliest that holds a corpus) plus one present-day render.
# Product: /out/t85_sample.json
set -uo pipefail

cd PseudoCoupHQ/Research/op_pipeline || exit 2
mkdir -p /out

python3 - <<'PY'
import json, os, resource, sys, time

sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
import dashboard_ouro as dash

LANE_CAP_MB = 6000
LANE_ABORT = "T85_SAMPLE_MEMORY_ABORT"


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check(stage):
    now = peak()
    if now > LANE_CAP_MB:
        raise SystemExit("%s: peak resident size %.1f MB passed the lane's "
                         "stated cap of %d MB during %s"
                         % (LANE_ABORT, now, LANE_CAP_MB, stage))
    return now


# the earliest moment whose tree holds a corpus, found from the lane-1
# facts rather than guessed: step index 35.
SAMPLE_KEYS = ["35", "now"]
rows = []
total = len(SAMPLE_KEYS) * 5
i = 0
for key in SAMPLE_KEYS:
    dash.set_moment(key)
    moment = dash.current_moment()
    for number in (1, 2, 3, 4, 5):
        i += 1
        started = time.time()
        html = dash.render(number)
        seconds = time.time() - started
        rss = check("pane %d at moment %s" % (number, key))
        refused = "not recomputable at this moment" in html
        error = "<h2>error</h2>" in html
        rows.append({
            "moment": key,
            "label": moment.label(),
            "pane": number,
            "seconds": round(seconds, 2),
            "peak_rss_mb": round(rss, 1),
            "characters": len(html),
            "refused": refused,
            "error": error,
            "chronology_above_tabs": html.find('class="chron"') < html.find('class="tabs"'),
        })
        print("[%d/%d] moment %s pane %d — %d chars, %.2f s, peak %.1f MB%s%s"
              % (i, total, key, number, len(html), seconds, rss,
                 ", REFUSED" if refused else "",
                 ", ERROR" if error else ""))
        if error:
            at = html.find("<pre>")
            print("       " + html[at:at + 300].replace("\n", " "))

with open("/out/t85_sample.json", "w") as fh:
    json.dump({"population": "%d renders (5 panes at 2 moments)" % total,
               "lane_cap_mb": LANE_CAP_MB,
               "lane_abort": LANE_ABORT,
               "page_cap_mb": dash.MEMORY_CAP_MB,
               "page_abort": dash.ABORT_NAME,
               "peak_rss_mb": round(peak(), 1),
               "renders": rows}, fh, indent=1, sort_keys=True)
print("SAMPLE PEAK RESIDENT SIZE: %.1f MB, cap %d MB" % (peak(), LANE_CAP_MB))
PY
