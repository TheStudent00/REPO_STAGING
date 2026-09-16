#!/usr/bin/env bash
# lp1 lane 10 -- the conventions verifier over this launch's log (LAW's
# final lane), from the instance. Fetches nothing. It re-runs the log's
# reproducing commands and sorts each claim; zero DIFFERS is required.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
export PATH=/opt/venv/bin:$PATH
P=PseudoCoupHQ
LOG=$P/DevComms/log_276_lp1_the_re_emit_with_sail_5745ea9e_does_not_build_either.md
echo "[1/1] verifier over $LOG"
python3 $P/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 "$LOG"
echo "  verifier rc=$?"
echo "lane lp1_l10 done"
