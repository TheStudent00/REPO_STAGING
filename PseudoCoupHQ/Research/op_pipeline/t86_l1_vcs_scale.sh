#!/usr/bin/env bash
# t86_l1_vcs_scale.sh -- TASK 86, lane 1.
#
# WHAT SCALE DOES VERSION CONTROL ITSELF SUPPLY?
#
# Task 86 retires the curated chronology (chronology_build.py:163 ran
# `git log --grep=banked -i`).  A moment is a commit; the scale is the
# repository's own history.  Before any code is written, this lane
# MEASURES what that history can offer as marks: how many commits, how
# many tags, how many merges, how many distinct days, and how the
# commits distribute over those days -- because a coarser scale, if one
# is possible at all, must come from what version control carries and
# never from text a writer chose.
#
# Nothing here reads a commit MESSAGE for any grouping, ordering or
# selection.  Subjects are counted only as bytes, to size the page.
#
# Product: /out/t86_vcs_scale.json
# Node: hq.research.compiler_graph.dashboard
set -uo pipefail

REPO=/projects/PseudoCoupHQ
cd "$REPO" || exit 2

echo "[1/6] git, inside the sandbox"
git --version || exit 3
git -C "$REPO" rev-parse --is-inside-work-tree || exit 4

echo "[2/6] the counts, each with the command that produced it"
echo "-- git rev-list --count HEAD"
git -C "$REPO" rev-list --count HEAD
echo "-- git rev-list --count --all"
git -C "$REPO" rev-list --count --all
echo "-- git tag | wc -l"
git -C "$REPO" tag | wc -l
echo "-- git rev-list --count --merges HEAD"
git -C "$REPO" rev-list --count --merges HEAD
echo "-- git for-each-ref --format='%(refname)' | wc -l"
git -C "$REPO" for-each-ref --format='%(refname)' | wc -l

mkdir -p /out
python3 - <<'PY'
import json, os, resource, subprocess, time

REPO = "/projects/PseudoCoupHQ"

def git(*args):
    p = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout

def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

print("[3/6] the whole walk, timed -- one process, one pass")
t0 = time.time()
SEP = "\x01"
REC = "\x02"
raw = git("log", "--format=%H" + SEP + "%cI" + SEP + "%aI" + SEP + "%P" + SEP + "%s" + REC)
walk_seconds = time.time() - t0
raw_bytes = len(raw.encode("utf-8"))

rows = []
for rec in raw.split(REC):
    rec = rec.strip("\n")
    if not rec.strip():
        continue
    parts = rec.split(SEP)
    if len(parts) < 5:
        continue
    sha, cdate, adate, parents, subject = parts[0], parts[1], parts[2], parts[3], parts[4]
    rows.append({
        "commit": sha,
        "committed": cdate,
        "authored": adate,
        "parents": len(parents.split()) if parents.strip() else 0,
        "subject_bytes": len(subject.encode("utf-8")),
    })
print("    commits walked: %d in %.2f s, %d bytes of --format output"
      % (len(rows), walk_seconds, raw_bytes))
print("    peak resident after the walk: %.1f MB" % peak_mb())

print("[4/6] the day distribution -- days are a fact of the commit's own timestamp")
days = {}
for r in rows:
    days.setdefault(r["committed"][:10], 0)
    days[r["committed"][:10]] += 1
counts = sorted(days.values())
n = len(counts)
median = counts[n // 2] if n else 0
print("    distinct committer days: %d" % n)
print("    commits per day: min %d, median %d, max %d"
      % (counts[0] if n else 0, median, counts[-1] if n else 0))
top = sorted(days.items(), key=lambda kv: -kv[1])[:10]
for day, c in top:
    print("      %s  %d commits" % (day, c))

print("[5/6] merges, tags, roots -- the other marks version control carries")
merges = [r for r in rows if r["parents"] > 1]
roots = [r for r in rows if r["parents"] == 0]
tags = [t for t in git("tag").splitlines() if t.strip()]
print("    merge commits: %d" % len(merges))
print("    root commits: %d" % len(roots))
print("    tags: %d" % len(tags))
refs = [l for l in git("for-each-ref", "--format=%(refname)").splitlines() if l.strip()]
print("    refs: %d -> %s" % (len(refs), ", ".join(refs[:10])))

print("[6/6] the same walk with a SIZE CAP, as the page would run it")
t0 = time.time()
capped = git("log", "--format=%H" + SEP + "%cI" + SEP + "%s" + REC)
print("    second walk: %.2f s, %d bytes" % (time.time() - t0, len(capped.encode("utf-8"))))
print("    peak resident at the end: %.1f MB" % peak_mb())

doc = {
    "repo": "PseudoCoupHQ",
    "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "population": "every commit reachable from HEAD",
    "commits_head": len(rows),
    "commits_all_refs": int(git("rev-list", "--count", "--all").strip()),
    "tags": len(tags),
    "merge_commits": len(merges),
    "root_commits": len(roots),
    "refs": refs,
    "distinct_days": n,
    "commits_per_day": {"min": counts[0] if n else 0,
                        "median": median,
                        "max": counts[-1] if n else 0},
    "day_counts": days,
    "first_committed": rows[-1]["committed"] if rows else None,
    "last_committed": rows[0]["committed"] if rows else None,
    "walk_seconds": round(walk_seconds, 3),
    "walk_output_bytes": raw_bytes,
    "peak_resident_mb": round(peak_mb(), 1),
}
with open("/out/t86_vcs_scale.json", "w") as fh:
    json.dump(doc, fh, indent=1, sort_keys=True)
print("wrote /out/t86_vcs_scale.json")
PY
