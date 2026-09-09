#!/usr/bin/env bash
# t88_l2_hash_out.sh -- TASK 88, lane 2.
#
# sha256 every file under /out, BY STREAMING (sha256sum reads in fixed
# small chunks; it never loads a whole file into memory), so hashing a
# 5.8 GB product costs kilobytes of RSS, not gigabytes.
#
# THE MEMORY BOUND, STATED BEFORE THE PASS. sha256sum's own RSS is
# O(1) in file size -- it is a streaming digest, not a whole-file read.
# Step 1 below SAMPLES the single largest file under /out (measured,
# not assumed to be kind_fuzz_clustering) under `/usr/bin/time -v` and
# prints Maximum resident set size. If that sample's RSS were to
# project past 6,144 MB across the run this lane ABORTS BY NAME before
# hashing the rest; a streaming tool makes that projection flat, not
# linear in corpus size, so the expectation is a few MB regardless of
# which file is largest.
#
# Product: printed to stdout only, captured into
# agent/logs/<stamp>__t88_l2_hash_out.sh.log. Writes nothing to /out.
#
# Node: hq.research.airlock_audit
set -uo pipefail

echo "== step 1/2: sample -- hash the single largest file under /out, measure peak RSS =="
LARGEST=$(find /out -type f -printf '%s\t%p\n' | sort -rn | head -1)
LSIZE=$(echo "$LARGEST" | cut -f1)
LPATH=$(echo "$LARGEST" | cut -f2-)
echo "largest file: $LPATH ($LSIZE bytes)"
echo '$ /usr/bin/time -v sha256sum "$LPATH"'
/usr/bin/time -v sha256sum "$LPATH" 2>&1 | tee /work/sample_time.txt
PEAK_KB=$(grep 'Maximum resident set size' /work/sample_time.txt | awk '{print $NF}')
echo "sampled peak RSS: ${PEAK_KB} KB"
if [ -n "${PEAK_KB:-}" ] && [ "$PEAK_KB" -gt 6291456 ]; then
    echo "ABORT: sampled peak RSS ${PEAK_KB} KB exceeds the 6 GB (6291456 KB) bound -- refusing to hash the rest by name."
    exit 9
fi
echo "under bound, proceeding with the full pass (streaming hash, RSS is flat in file size)"

echo
echo "== step 2/2: sha256 every file under /out, streaming, [i/total] =="
TOTAL=$(find /out -type f | wc -l)
echo "total files: $TOTAL"
i=0
find /out -type f | sort | while IFS= read -r f; do
    i=$((i+1))
    rel="${f#/out/}"
    sz=$(stat -c%s "$f")
    h=$(sha256sum "$f" | awk '{print $1}')
    echo "HASHOUT	$rel	$sz	$h"
    if [ $((i % 200)) -eq 0 ]; then
        echo "[progress] $i/$TOTAL hashed" >&2
    fi
done
echo "[$TOTAL/$TOTAL] all files under /out hashed"
