#!/usr/bin/env bash
# m1_l6_edges_sample.sh -- task m1: the equivalence pass over the FIRST
# 400 same-builder cells only, to measure what the whole pass costs
# before it is run (the standing "sample first" rule). It writes
# model_table_edges.json with meta.sample = 400; the whole pass
# overwrites it. MEMORY BOUND: 16g, named abort ABORT_MEMORY_M1.
set -euo pipefail
echo "[1/1] task m1: model_table.py edges --sample 400"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py edges --sample 400
echo "[1/1] done"
