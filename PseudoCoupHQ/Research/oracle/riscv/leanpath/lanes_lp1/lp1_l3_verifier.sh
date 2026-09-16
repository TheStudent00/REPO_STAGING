#!/usr/bin/env bash
# lp1 lane 3 -- the conventions verifier over this task's log, from the
# instance (LAW's final lane). Fetches nothing. It re-runs the log's
# reproducing commands and sorts each claim; zero DIFFERS is required.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
P=PseudoCoupHQ
LOG=$P/DevComms/log_275_lp1_the_cached_emit_does_not_build_under_the_pinned_toolchain.md
echo "[1/1] verifier over $LOG"
python3 $P/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 "$LOG"
echo "  verifier rc=$?"
echo "lane lp1_l3 done"
