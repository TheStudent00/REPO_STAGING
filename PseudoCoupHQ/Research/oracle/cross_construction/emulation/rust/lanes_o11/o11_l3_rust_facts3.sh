#!/bin/bash
# task o11, lane 3: the one remaining division question.
# Lane 2 found `a / NonZeroU32::new_unchecked(b)` emits a bare divide
# for UNSIGNED holders, and that `NonZero<i32>` has no division at all,
# so the signed cell had no idiom. This lane tries the stable
# `core::hint::assert_unchecked` route for both readings and all widths.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
export PATH=/opt/cargo/bin:$PATH
echo "[1/2] the third probe set"
cd "$R" && python3 rust_facts.py probe3
echo "[2/2] the guard over the json this lane wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$R/rust_facts3.json"
echo "lane o11_l3 done"
