#!/usr/bin/env bash
# t85_l1_gitfacts.sh -- TASK 85, lane 1.
#
# What every pane would have to READ to be recomputed at a past moment,
# and whether git holds it at that moment.  One `git ls-tree -r -l` per
# chronology step; nothing is checked out, nothing is written to the
# tree.  Product: /out/t85_gitfacts.json
#
# Node: hq.research.compiler_graph.dashboard
set -uo pipefail

REPO=PseudoCoupHQ
cd "$REPO" || exit 2

echo "== git, inside the sandbox"
git --version || exit 3
echo "== the repository the lane sees"
git -C "$REPO" rev-parse --is-inside-work-tree
git -C "$REPO" rev-parse HEAD

mkdir -p /out
python3 - <<'PY'
import json, os, subprocess, sys

REPO = "PseudoCoupHQ"
CHRON = os.path.join(REPO, "Research/op_pipeline/chronology.json")

with open(CHRON) as fh:
    chron = json.load(fh)
steps = chron["steps"]
total = len(steps)

# what each pane would open at a moment, as PATH PREFIXES in the tree.
WANTED = {
    "corpus_wrapped":  "Research/op_pipeline/canon39_wrapped_",
    "corpus_interp":   "Research/op_pipeline/canon39_interp.json",
    "corpus_regen":    "Research/op_pipeline/canon39_regen_store/",
    "manifests":       "Research/op_pipeline/probe_manifest",
    "term_store":      "Research/op_pipeline/term65_store/",
    "render_store":    "Research/op_pipeline/render_back_store/",
    "pool":            "Research/op_pipeline/the_pool",
    "census":          "Research/op_pipeline/name_census",
    "audit65":         "Research/op_pipeline/audit65.json",
    "graph_files":     "Research/compiler_graph/graph_",
    "coverage_go_f":   "Research/compiler_graph/coverage_go_files.json",
    "coverage_go_s":   "Research/compiler_graph/coverage_go_summary.json",
    "chronology":      "Research/op_pipeline/chronology.json",
}

out = []
for i, step in enumerate(steps, 1):
    commit = step["commit"]
    listing = subprocess.run(
        ["git", "-C", REPO, "ls-tree", "-r", "-l", commit,
         "Research/"],
        capture_output=True, text=True)
    if listing.returncode != 0:
        print("[%d/%d] %s LS-TREE FAILED: %s"
              % (i, total, commit[:8], listing.stderr.strip()))
        out.append({"commit": commit, "error": listing.stderr.strip()})
        continue
    buckets = {k: {"files": 0, "bytes": 0, "examples": []} for k in WANTED}
    for line in listing.stdout.splitlines():
        # <mode> blob <sha> <size>\t<path>
        head, _, path = line.partition("\t")
        parts = head.split()
        if len(parts) < 4 or parts[1] != "blob":
            continue
        try:
            size = int(parts[3])
        except ValueError:
            size = 0
        for name, prefix in WANTED.items():
            if path.startswith(prefix):
                b = buckets[name]
                b["files"] += 1
                b["bytes"] += size
                if len(b["examples"]) < 3:
                    b["examples"].append(os.path.basename(path))
    row = {
        "commit": commit,
        "day": step.get("day"),
        "scale": step.get("scale"),
        "round": step.get("round"),
        "buckets": buckets,
    }
    out.append(row)
    have = [k for k in WANTED if buckets[k]["files"]]
    print("[%d/%d] %s %s  holds: %s"
          % (i, total, step.get("day"), commit[:8],
             ", ".join(sorted(have)) or "(none of the wanted paths)"))

with open("/out/t85_gitfacts.json", "w") as fh:
    json.dump({"repo": "PseudoCoupHQ",
               "population": "%d chronology steps" % total,
               "wanted": WANTED,
               "steps": out}, fh, indent=1, sort_keys=True)
print("wrote /out/t85_gitfacts.json over %d steps" % total)
PY
