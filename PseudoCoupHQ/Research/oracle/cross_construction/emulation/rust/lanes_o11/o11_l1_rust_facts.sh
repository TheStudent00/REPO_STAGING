#!/bin/bash
# task o11, lane 1: what rustc itself does, read off its own emission.
# Runs `rust_facts.py probe` -- one small rust function per question the
# coverage table's rust column asks, compiled at the rust corpus's own
# ship flags and carved with the pipeline's objdump reader.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/4] where the toolchain is"
command -v rustc || echo "rustc NOT on PATH"
command -v objdump || echo "objdump NOT on PATH"
rustc --version
rustc --print target-spec-json --target x86_64-unknown-linux-gnu \
    -Z unstable-options 2>/dev/null | head -5 \
    || echo "(target-spec-json needs a nightly flag; skipped)"
echo "[2/4] python and z3"
python3 -c 'import z3; print("z3", z3.get_version_string())'
echo "[3/4] the probes"
cd "$R" && python3 rust_facts.py probe
echo "[4/4] the guard over the json this lane wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_facts.json"
echo "lane o11_l1 done"
