#!/usr/bin/env bash
set -u
echo "[1/2] verifying artifacts against manifest"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t102/t102_artifacts.py \
  PseudoCoupHQ/Research/op_pipeline/lanes_t102/t102_manifest.json \
  PseudoCoupHQ/Research/op_pipeline/lanes_t102/t102_artifacts_result.json
echo "[2/2] done"
