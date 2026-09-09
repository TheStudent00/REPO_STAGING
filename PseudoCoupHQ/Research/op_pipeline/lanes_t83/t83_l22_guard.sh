#!/usr/bin/env bash
# t83 lane 22 -- the guard re-run.  Lane 21 passed 27 of 27 paths with
# 0 FAIL, but `grep -c exempt` over the transcript came back 1: the
# count matched the driver's OWN heading sentence, which contained the
# word inside "exemption".  The heading now says "carve-out", nothing
# else changed, and the count is pasted again.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/4] the guard, one process, nothing skipped"
python3 guard83_term_pool.py
echo "-- exit $?"
echo
echo "[2/4] the command the guard ran"
sed -n '3p' guard83_term_pool_transcript.txt
echo
echo "[3/4] grep -c exempt over the guard's own output"
grep -c exempt guard83_term_pool_transcript.txt
echo
echo "[4/4] the whole transcript"
cat guard83_term_pool_transcript.txt
exit 0
