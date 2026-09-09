#!/usr/bin/env bash
# t99 lane 10 -- re-run of the final lane after log_205's evidence
# blocks were converted to real $ command / pasted-output shell
# transcripts (lane 9's run, before that edit, scored 0 MATCHES / 8
# UNVERIFIABLE because the first draft only quoted objects, never a
# reproducing command).
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_205 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /out/t99_l10_claims_log205.json \
  PseudoCoupHQ/DevComms/log_205_task_99_recording_gaps.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
