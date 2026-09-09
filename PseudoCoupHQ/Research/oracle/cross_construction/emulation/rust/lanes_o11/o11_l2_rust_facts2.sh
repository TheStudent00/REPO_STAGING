#!/bin/bash
# task o11, lane 2: the gaps lane 1 left.
# Lane 1 showed plain `/` and `%` emit a zero-divisor check and a call
# to a panic routine in BOTH the ship and the debug build, and that
# `unchecked_div` is not a method on stable rustc 1.96.1. This lane
# searches for a division idiom that emits a bare divide, and asks
# whether 16- and 128-bit float holders exist.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the second probe set"
cd "$R" && python3 rust_facts.py probe2
echo "[2/2] the guard over the json this lane wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_facts2.json"
echo "lane o11_l2 done"
