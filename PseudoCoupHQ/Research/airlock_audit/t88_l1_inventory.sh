#!/usr/bin/env bash
# t88_l1_inventory.sh -- TASK 88, lane 1.
#
# Full recursive inventory of /out (agent/out), the products a caller
# was supposed to read out and place into the real tree per
# agent/README.md's "The loop" step 4. This lane MOVES, COPIES, and
# DELETES NOTHING -- it only lists.
#
# Recounts, by name, the two numbers `./airlock doctor` reported
# (266 top-level entries, and a du total) so this audit's own numbers
# are traceable to commands run inside this lane rather than to the
# doctor snapshot.
#
# Product: printed to stdout only (captured into the daemon's log at
# agent/logs/<stamp>__t88_l1_inventory.sh.log). Nothing is written to
# /out, so the population this lane audits is not changed by auditing
# it.
#
# Node: hq.research.airlock_audit
set -uo pipefail

echo "== recount: top-level entries in /out (matches doctor's phrasing) =="
echo '$ find /out -mindepth 1 -maxdepth 1 | wc -l'
find /out -mindepth 1 -maxdepth 1 | wc -l

echo
echo "== recount: du -sb /out (bytes, streaming du, not a whole-file read) =="
echo '$ du -sb /out'
du -sb /out

echo
echo "== recount: total recursive file count under /out =="
echo '$ find /out -type f | wc -l'
find /out -type f | wc -l

python3 - <<'PY'
import json, os, subprocess, sys

OUT = "/out"
top = sorted(os.listdir(OUT))
total = len(top)
print()
print("== per-product (top-level entry) accounting, [i/total] ==")

products = []
for i, name in enumerate(top, 1):
    p = os.path.join(OUT, name)
    is_dir = os.path.isdir(p)
    if is_dir:
        # streaming du -sb per top-level entry; no whole-file reads
        r = subprocess.run(["du", "-sb", p], capture_output=True, text=True)
        size_b = int(r.stdout.split()[0]) if r.returncode == 0 else -1
        nfiles = 0
        newest = 0.0
        oldest = None
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    st = os.stat(fp)
                except OSError:
                    continue
                nfiles += 1
                newest = max(newest, st.st_mtime)
                oldest = st.st_mtime if oldest is None else min(oldest, st.st_mtime)
    else:
        st = os.stat(p)
        size_b = st.st_size
        nfiles = 1
        newest = st.st_mtime
        oldest = st.st_mtime
    products.append({
        "name": name,
        "kind": "dir" if is_dir else "file",
        "bytes": size_b,
        "recursive_file_count": nfiles,
        "mtime_oldest": oldest,
        "mtime_newest": newest,
    })
    print("[%d/%d] %-40s %-4s %14d bytes  %6d files" %
          (i, total, name, products[-1]["kind"], size_b, nfiles))

total_bytes = sum(p["bytes"] for p in products if p["bytes"] >= 0)
total_files = sum(p["recursive_file_count"] for p in products)
print()
print("== summary ==")
print("population: %d top-level products under /out" % total)
print("sum of per-product du -sb: %d bytes (%.2f GB)" % (total_bytes, total_bytes/1e9))
print("sum of per-product recursive file counts: %d files" % total_files)

with open("/work/t88_inventory.json", "w") as fh:
    json.dump({"population": "%d top-level products" % total,
               "products": products}, fh, indent=1, sort_keys=True)

print()
print("== JSON-LINES manifest (one product per line, machine-parseable) ==")
for p in products:
    print("PRODUCT\t" + json.dumps(p, sort_keys=True))

print()
print("== full recursive file listing (JSON-LINES, relpath from /out) ==")
n = 0
for root, dirs, files in os.walk(OUT):
    for f in files:
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, OUT)
        try:
            st = os.stat(fp)
        except OSError:
            continue
        n += 1
        print("FILE\t" + json.dumps({"rel": rel, "bytes": st.st_size,
                                      "mtime": st.st_mtime}, sort_keys=True))
print("wrote %d FILE lines" % n)
PY
echo "[1/1] inventory complete"
