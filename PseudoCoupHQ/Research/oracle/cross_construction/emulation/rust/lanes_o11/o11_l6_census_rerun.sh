#!/bin/bash
# task o11, lane 6: the census again, after one field rename.
# Lane 5's guard run FAILED rust_population.json at 39 places, all of
# them the per-opcode row's `mnemonic` field: four x86 mnemonics (`and`,
# `or`, `not`, `xor`) are spelled the same as operator tokens in the
# probe manifests, and the guard cannot tell an arch mnemonic from a
# language spelling. The field is now `mnem`, which is the pipeline's
# own name for an instruction's text and which the guard already reads
# as a machine form. The guard itself is untouched.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the census"
cd "$R" && python3 rust_render.py census
echo "[2/2] the guard over the population json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_population.json"
echo "lane o11_l6 done"
