#!/usr/bin/env bash
# t88_l3_rss_sample.sh -- TASK 88, lane 3.
#
# lane 2's sample step tried `/usr/bin/time -v` to measure the peak RSS
# of hashing the largest file under /out (ct_typescript_l2.txt, 1.85 GB)
# before hashing the rest. /usr/bin/time is NOT installed in the sandbox
# image, so that measurement came back empty (see
# agent/logs/20260904T220217Z__t88_l2_hash_out.sh.log line 9) even
# though lane 2 itself finished (exit 0, 49.9s, 6004 files, no OOM).
# This lane re-measures the SAME sample, in-process, with Python's own
# resource.getrusage so a real number is pasted, per the memory rule
# that a sample must be measured, not assumed.
#
# Node: hq.research.airlock_audit
set -uo pipefail

echo "== step 1/1: measure peak RSS of streaming sha256 over the largest /out file =="
python3 - <<'PY'
import hashlib, os, resource, subprocess

r = subprocess.run(["find", "/out", "-type", "f", "-printf", "%s\t%p\n"],
                    capture_output=True, text=True)
rows = [l.split("\t", 1) for l in r.stdout.splitlines() if l]
rows.sort(key=lambda x: -int(x[0]))
size, path = rows[0]
size = int(size)
print("largest file: %s (%d bytes, %.2f GB)" % (path, size, size/1e9))

before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
h = hashlib.sha256()
with open(path, "rb") as fh:
    while True:
        chunk = fh.read(1024*1024)
        if not chunk:
            break
        h.update(chunk)
after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("digest: %s" % h.hexdigest())
print("ru_maxrss before: %d KB" % before)
print("ru_maxrss after (this process's PEAK, monotonic): %d KB" % after)
print("peak RSS for streaming sha256 of the largest product: %d KB (%.2f MB)"
      % (after, after/1024))

BOUND_KB = 6*1024*1024
if after > BOUND_KB:
    print("ABORT: measured peak RSS %d KB exceeds the 6 GB bound" % after)
    raise SystemExit(9)
print("under the 6 GB bound by a factor of %.0fx -- streaming hashing of every"
      " remaining file in lane 2 carries the SAME flat RSS, independent of"
      " file size, which is why lane 2 already completed all 6004 files in"
      " 49.9s with work_consumed_mb=0." % (BOUND_KB/max(after,1)))
PY
