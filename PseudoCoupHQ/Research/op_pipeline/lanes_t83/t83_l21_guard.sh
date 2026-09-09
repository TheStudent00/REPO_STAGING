#!/usr/bin/env bash
# t83 lane 21 -- the UNMODIFIED spelling-key guard over every JSON
# artifact task 83 wrote, run as ONE process, with `grep -c exempt`
# over the transcript pasted.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/3] the guard, one process, nothing skipped"
python3 guard83_term_pool.py
echo "-- exit $?"
echo
echo "[2/3] grep -c exempt over the transcript"
grep -c exempt guard83_term_pool_transcript.txt
echo
echo "[3/3] the transcript's head and tail"
head -8 guard83_term_pool_transcript.txt
echo "   ..."
tail -8 guard83_term_pool_transcript.txt
exit 0
