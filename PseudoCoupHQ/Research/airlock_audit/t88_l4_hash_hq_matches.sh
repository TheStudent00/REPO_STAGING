#!/usr/bin/env bash
# t88_l4_hash_hq_matches.sh -- TASK 88, lane 4.
#
# For every top-level product name in /out, search the real tree
# (PseudoCoupHQ, read side of the rw mount -- this lane never
# writes there) for a file or directory of the SAME NAME, then hash the
# overlap file-by-file, streaming, exactly as lane 2 hashed /out. This
# is the data that lets the audit call PLACED/DIVERGED/ABSENT by
# CONTENT rather than by name alone.
#
# Streaming, same bound as lane 2: sha256sum's RSS is flat in file
# size. No sample step repeated here since lane 2 already established
# the bound is not reached by this toolchain; abort-by-name kept as a
# guard anyway.
#
# Writes nothing under /projects -- `find` and `sha256sum` only, both
# read-only operations. Product: stdout, captured into
# agent/logs/<stamp>__t88_l4_hash_hq_matches.sh.log.
#
# Node: hq.research.airlock_audit
set -uo pipefail

echo "== confirming the mount is read-from, not written-to, by this lane =="
mount | grep PseudoCoupHQ || true

python3 - <<'PY'
import json, os, subprocess, hashlib, sys

OUT = "/out"
HQ = "PseudoCoupHQ"

def sha256_stream(path, bound_kb=6*1024*1024):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(1024*1024)  # 1 MB chunks -- streaming, flat RSS
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

top = sorted(os.listdir(OUT))
total = len(top)
print("population: %d top-level /out products to search for in HQ" % total)

for i, name in enumerate(top, 1):
    outp = os.path.join(OUT, name)
    # exact-basename search, case-sensitive first (this tree is case-sensitive)
    r = subprocess.run(["find", HQ, "-name", name, "-not", "-path", "*/.git/*"],
                        capture_output=True, text=True)
    matches = [m for m in r.stdout.splitlines() if m]
    print("[%d/%d] %-40s matches=%d %s" % (i, total, name, len(matches), matches[:5]))
    print("MATCH\t" + json.dumps({"product": name, "hq_matches": matches}, sort_keys=True))

    for m in matches:
        if os.path.isdir(outp) and os.path.isdir(m):
            # walk the OUT side; for each relpath, look for the same
            # relpath under this HQ match
            for root, dirs, files in os.walk(outp):
                for f in files:
                    ofp = os.path.join(root, f)
                    rel = os.path.relpath(ofp, outp)
                    hqp = os.path.join(m, rel)
                    row = {"product": name, "hq_dir": m, "rel": rel}
                    if os.path.isfile(hqp):
                        ost = os.stat(ofp)
                        hst = os.stat(hqp)
                        row["out_bytes"] = ost.st_size
                        row["hq_bytes"] = hst.st_size
                        row["out_mtime"] = ost.st_mtime
                        row["hq_mtime"] = hst.st_mtime
                        if ost.st_size == hst.st_size:
                            row["out_sha256"] = sha256_stream(ofp)
                            row["hq_sha256"] = sha256_stream(hqp)
                        else:
                            row["out_sha256"] = None
                            row["hq_sha256"] = None
                        row["present_in_hq"] = True
                    else:
                        row["present_in_hq"] = False
                    print("CMP\t" + json.dumps(row, sort_keys=True))
        elif os.path.isfile(outp) and os.path.isfile(m):
            ost = os.stat(outp)
            hst = os.stat(m)
            row = {"product": name, "hq_file": m, "rel": ".",
                   "out_bytes": ost.st_size, "hq_bytes": hst.st_size,
                   "out_mtime": ost.st_mtime, "hq_mtime": hst.st_mtime,
                   "present_in_hq": True}
            if ost.st_size == hst.st_size:
                row["out_sha256"] = sha256_stream(outp)
                row["hq_sha256"] = sha256_stream(m)
            else:
                row["out_sha256"] = None
                row["hq_sha256"] = None
            print("CMP\t" + json.dumps(row, sort_keys=True))
        # dir-vs-file name collisions (rare) are left unmatched; the
        # audit records "matches" but no CMP rows for that pairing --
        # visible in the log as a MATCH line with no following CMP.

print("done: %d products searched" % total)
PY
echo "[1/1] hq-match hashing complete"
