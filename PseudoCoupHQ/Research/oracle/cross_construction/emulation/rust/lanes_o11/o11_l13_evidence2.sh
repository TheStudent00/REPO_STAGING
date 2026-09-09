#!/bin/bash
# task o11, lane 13: the evidence blocks the DevComms log pastes.
# Lane 12 printed its `$` line through "$*", which dropped the quoting,
# so the printed command was not the one that ran. Here the command is
# one string, echoed verbatim and then evaluated, so the `$` line IS
# the command.
set -u
export PATH=/opt/cargo/bin:$PATH
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust

run() {
  echo "\$ $1"
  eval "$1"
  echo
}

echo "[1/12] rustc"
run "rustc --version"

echo "[2/12] the emitted body of each measured rule"
run "python3 $R/rust_facts.py show plain_sum_u32 wrapping_sum_u32 plain_left_shift_u32 wrapping_left_shift_u32 plain_quotient_u32 plain_quotient_i32 nonzero_quotient_u32 hinted_quotient_u32 hinted_quotient_i32 unreachable_quotient_i32 widen_u8_to_u32 narrow_u32_to_u8 sign_extend_i8_to_i64 sum_u128 saturating_f64_to_i64 truncating_f64_to_i64 f64_bits bits_f64 absolute_f64 float16_holder float128_holder wide_arrival_u8"

echo "[3/12] the coverage table's class counts"
run "grep -c '^| Z3_OP_' $R/rust_report.md"
run "grep -c '^| Z3_OP_.* | idiom | ' $R/rust_report.md"

echo "[4/12] the sorts"
run "sed -n '/^### The sorts/,/^## 1\\./p' $R/rust_report.md"

echo "[5/12] the population"
run "sed -n '/^## 1\\. The population/,/^## 2\\./p' $R/rust_report.md"

echo "[6/12] the per-x table"
run "sed -n '/^## 2\\. Per x/,/^### What the control/p' $R/rust_report.md"

echo "[7/12] what the control does"
run "sed -n '/^### What the control/,/^## 3\\./p' $R/rust_report.md"

echo "[8/12] the refusals"
run "sed -n '/^## 5\\. Refusals/,/^## 6\\./p' $R/rust_report.md"

echo "[9/12] the disproved and the undecided"
run "sed -n '/^## 6\\. The disproved/,/^## 7\\./p' $R/rust_report.md"

echo "[10/12] the per-opcode question"
run "sed -n '/^## 7\\. Task o8/,/^### Per x and per mnemonic/p' $R/rust_report.md"
run "sed -n '/^### Mnemonics never landed/,/^### NOT_COLLAPSED/p' $R/rust_report.md"

echo "[11/12] bounds and memory"
run "sed -n '/^## 8\\. Bounds/,\$p' $R/rust_report.md"

echo "[12/12] the guard over every json this task wrote"
run "python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $R/rust_facts.json $R/rust_facts2.json $R/rust_facts3.json $R/rust_facts4.json $R/coverage_table.json $R/rust_population.json $R/rust_indexes.json $R/rust_held.json $R/rust_sample.json $R/rust_run.json $R/rust_control.json $R/rust_peropcode.json $R/rust_results.json"
echo "lane o11_l13 done"
