#!/bin/bash
# task o13, lane 2: the outcome spellings again, after lane 1's guard
# run FAILED `mode_facts.json` on five places -- each a bare arch
# mnemonic in a list, and `xor` is both an arch mnemonic and an
# operator token.  The answer to a spelling collision is a SHAPE
# change, never an exemption (producer CORE, log_147 13.7): the body's
# opcodes are now typed objects `{"kind": "arch_opcode", "mnem": ...}`.
# This lane also adds the no-guard BASELINE probe, so the cost of each
# spelling is measured rather than judged.
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the outcome spellings, measured, with the baseline"
cd "$M" && python3 mode.py facts
echo "[2/2] the guard over the json this lane wrote"
python3 "$G" "$M/mode_facts.json"
echo "lane o13_l2 done"
