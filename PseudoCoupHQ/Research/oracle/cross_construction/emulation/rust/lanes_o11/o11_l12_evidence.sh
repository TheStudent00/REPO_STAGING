#!/bin/bash
# task o11, lane 12: the evidence blocks the DevComms log pastes.
# Every block below is one command and its output, printed here so the
# log's transcripts are the lane's own and not hand-tidied.
set -u
R=PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust
OP=PseudoCoupHQ/Research/op_pipeline
export PATH=/opt/cargo/bin:$PATH

run() {
  echo "\$ $*"
  "$@"
  echo
}

echo "[1/11] rustc, and the emitted body of each measured rule"
run rustc --version
run python3 "$R/rust_facts.py" show plain_sum_u32 wrapping_sum_u32 \
    plain_left_shift_u32 wrapping_left_shift_u32 plain_quotient_u32 \
    plain_quotient_i32 nonzero_quotient_u32 hinted_quotient_u32 \
    hinted_quotient_i32 unreachable_quotient_i32 widen_u8_to_u32 \
    narrow_u32_to_u8 sign_extend_i8_to_i64 sum_u128 \
    saturating_f64_to_i64 truncating_f64_to_i64 f64_bits bits_f64 \
    absolute_f64 float16_holder float128_holder wide_arrival_u8

echo "[2/11] the coverage table's rows where the two targets differ"
run grep -E "^\| Z3_OP_(BADD|BSUB|BMUL|BNEG|BUDIV_I|BUREM_I|BSDIV_I|BSREM_I|FPA_ABS|FPA_IS_INF|FPA_IS_NEGATIVE|FPA_IS_POSITIVE|FPA_TO_FP|FPA_TO_IEEE_BV|FPA_TO_SBV|FPA_TO_UBV) " "$R/rust_report.md"

echo "[3/11] the sorts"
run sed -n "/^### The sorts/,/^## 1\./p" "$R/rust_report.md"

echo "[4/11] the population"
run sed -n "/^## 1\. The population/,/^## 2\./p" "$R/rust_report.md"

echo "[5/11] the per-x table"
run sed -n "/^## 2\. Per x/,/^### What the control/p" "$R/rust_report.md"

echo "[6/11] what the control does"
run sed -n "/^### What the control/,/^## 3\./p" "$R/rust_report.md"

echo "[7/11] the refusals"
run sed -n "/^## 5\. Refusals/,/^## 6\./p" "$R/rust_report.md"

echo "[8/11] the disproved and the undecided"
run sed -n "/^## 6\. The disproved/,/^## 7\./p" "$R/rust_report.md"

echo "[9/11] the per-opcode question"
run sed -n "/^## 7\. Task o8/,/^### Per x and per mnemonic/p" "$R/rust_report.md"
run sed -n "/^### Mnemonics never landed/,/^### NOT_COLLAPSED/p" "$R/rust_report.md"

echo "[10/11] bounds and memory"
run sed -n "/^## 8\. Bounds/,\$p" "$R/rust_report.md"

echo "[11/11] the guard over every json this task wrote"
run python3 "$OP/check_no_spelling_keys.py" "$R/rust_facts.json" \
    "$R/rust_facts2.json" "$R/rust_facts3.json" "$R/rust_facts4.json" \
    "$R/coverage_table.json" "$R/rust_population.json" \
    "$R/rust_indexes.json" "$R/rust_held.json" "$R/rust_sample.json" \
    "$R/rust_run.json" "$R/rust_control.json" "$R/rust_peropcode.json" \
    "$R/rust_results.json"
echo "lane o11_l12 done"
