#!/usr/bin/env bash
# ex2_l3_retry600.sh -- task ex2, step 3 (brief §2): the retry pass.
# Every run the first pass (`ex2_l2_the_loop.sh`, 60 s per run) recorded
# TIMEOUT is re-run once, from a second cold render, at 600 s, into
# `expand2_runs_retry600.jsonl`. Both records are kept: the first
# pass's TIMEOUT stays on `expand2_runs.jsonl` and the retry's own
# outcome lands on the retry file; `expand2.py`'s `effective()` is what
# later reads decide which one the tables count.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX2; each runner is a separate short-lived process handed
# the whole sample at once. Resumable the same way the first pass is:
# `retry` skips any pair already on `expand2_runs_retry600.jsonl`.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/1] the retry pass: every first-pass TIMEOUT, once, at 600 s"
python3 expand2.py retry
echo "done"
