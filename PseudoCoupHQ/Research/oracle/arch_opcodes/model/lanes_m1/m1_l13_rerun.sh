#!/usr/bin/env bash
# m1_l13_rerun.sh -- task m1: sweep, edges, assemble and report re-run
# after one correction to WHAT COUNTS AS A PLACE WRITTEN.
#
# THE DEFECT, found by reading the `add`/`lea` cells the brief names.
# `reference.MachineState.memory_cell` puts a cell's arrival symbol into
# `state.memory` the first time a line READS that cell, so
# `model_translate.run_line` -- which reports every place the state
# gained -- reports a read-only memory cell as written. It already
# applies this correction to registers (`state.shared_seed.get(...)`)
# and not to memory. The effect: `add (%rsi),%edi` was recorded as
# writing three places (192 bits joined) where it writes one, and every
# `add`/`lea` cell was refused for "different sorts". `model_table.py`
# now drops a memory place whose term is character-for-character that
# cell's own arrival symbol. `model_translate.py` is NOT touched: it is
# a shared file this brief did not name, and the correction lives in
# this task's own program.
#
# MEMORY BOUND: 16g resident, named abort ABORT_MEMORY_M1.
set -euo pipefail
echo "[1/4] task m1: model_table.py sweep"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py sweep
echo "[2/4] task m1: model_table.py edges"
python3 model_table.py edges
echo "[3/4] task m1: model_table.py assemble"
python3 model_table.py assemble
echo "[4/4] task m1: model_table.py report"
python3 model_table.py report
echo "[4/4] done"
