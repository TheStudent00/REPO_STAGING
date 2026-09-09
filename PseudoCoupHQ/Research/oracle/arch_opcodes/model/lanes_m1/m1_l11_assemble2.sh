#!/usr/bin/env bash
# m1_l11_assemble2.sh -- task m1: assemble and report, re-run after two
# corrections to the COUNTS (nothing measured by the sweep, the
# attestation or the solver changed; only how the already-measured rows
# are counted):
#  * the SPLITS are now counted by the set of PLACES a mnemonic's rows
#    write -- the split the ruling of 2026-09-08 names -- with the
#    destination-text count kept beside it as the finer reading. The
#    first run counted only destination texts over every sweep attempt,
#    which fanned out over the second pass's flag seeds and read `adc`
#    as 181 mappings.
#  * the reverse join is now reported: the (mnem, shape, width) cells
#    the corpus attests for which the table has no TRANSLATED row.
set -euo pipefail
echo "[1/2] task m1: model_table.py assemble"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py assemble
echo "[2/2] task m1: model_table.py report"
python3 model_table.py report
echo "[2/2] done"
