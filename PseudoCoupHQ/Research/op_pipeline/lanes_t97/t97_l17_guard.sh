#!/usr/bin/env bash
# t97 lane 17 -- the UNMODIFIED spelling guard again, ONE process, over
# the FINAL artifact set, so the count in log_202 section 7.3 is the
# count over what this task actually leaves on disk.
set -u
cd PseudoCoupHQ/Research/op_pipeline
python3 guard97_term_pool.py
echo "-- exit $?"
echo
echo "grep -c exempt over the guard's own output:"
grep -c exempt guard97_term_pool_transcript.txt
