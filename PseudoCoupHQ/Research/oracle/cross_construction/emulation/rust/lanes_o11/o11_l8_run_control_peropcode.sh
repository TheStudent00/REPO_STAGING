#!/bin/bash
# task o11, lane 8: the run of record.
#   the run      -- 400 of the 561 entries that pass every filter,
#                   drawn uniformly, seed 20260907 (the brief's ceiling)
#   the control  -- 40 entries that DO have a rust member, emulated
#                   from that member's own term
#   the per-opcode -- task o8's question with rust as the target, over
#                   the single-opcode rows of c, go and swift
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/4] the run"
cd "$R" && python3 rust_render.py run
echo "[2/4] the control"
cd "$R" && python3 rust_render.py control 40
echo "[3/4] the per-opcode question"
cd "$R" && python3 rust_render.py peropcode
echo "[4/4] the guard over every json this lane wrote"
for f in rust_run.json rust_control.json rust_peropcode.json; do
  python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
      "$R/$f"
done
echo "lane o11_l8 done"
