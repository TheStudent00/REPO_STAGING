#!/bin/bash
# task o13, lane 1: the guard vocabulary, and what each candidate
# outcome spelling actually emits.
#   [1] where the toolchain is
#   [2] the guard-outcome vocabulary off the ledgers of the disproved
#       units (`mode.py vocabulary`)
#   [3] the outcome spellings, measured in c and in rust
#       (`mode.py facts`)
#   [4] the unmodified spelling guard over both json files
set -u
M=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode
G=/projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
export PATH=/opt/cargo/bin:$PATH
echo "[1/4] where the toolchain is"
command -v clang || echo "clang NOT on PATH"
command -v rustc || echo "rustc NOT on PATH"
command -v objdump || echo "objdump NOT on PATH"
clang --version | head -1
rustc --version
python3 -c 'import z3; print("z3", z3.get_version_string())'
echo "[2/4] the guard vocabulary"
cd "$M" && python3 mode.py vocabulary
echo "[3/4] the outcome spellings, measured"
cd "$M" && python3 mode.py facts
echo "[4/4] the guard over the json this lane wrote"
for f in mode_population.json mode_facts.json; do
  python3 "$G" "$M/$f"
done
echo "lane o13_l1 done"
