#!/bin/bash
# task o11, lane 17: every evidence block the DevComms log pastes, in
# ONE lane and in a form check_conventions_log_claims.py can re-run.
# Lanes 13 to 15 used sed's `/.../` addresses, whose argument starts
# with a `/`; the verifier reads a token starting `/` as a path and
# scores the claim REFUSED (log_unreachable) rather than running it.
# sed's `\%...%` address form says the same thing without a leading
# slash. `rustc --version` is off the verifier's read-only allowlist,
# so the version is read out of the json the facts lane wrote instead.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust

run() {
  echo "\$ $1"
  eval "$1"
  echo
}

echo "[1/16] rustc, out of the json lane o11_l1 wrote"
run "grep rustc_version $R/rust_facts.json"

echo "[2/16] the emitted body of each measured rule"
run "python3 $R/rust_facts.py show plain_sum_u32 wrapping_sum_u32 plain_left_shift_u32 wrapping_left_shift_u32 plain_quotient_u32 plain_quotient_i32 nonzero_quotient_u32 hinted_quotient_u32 hinted_quotient_i32 unreachable_quotient_i32 widen_u8_to_u32 narrow_u32_to_u8 sign_extend_i8_to_i64 sum_u128 saturating_f64_to_i64 truncating_f64_to_i64 f64_bits bits_f64 absolute_f64 float16_holder float128_holder wide_arrival_u8"

echo "[3/16] the coverage table's row count and its class summary"
run "grep -c '^| Z3_OP_' $R/rust_report.md"
run "grep '^Rust cells' $R/rust_report.md"

echo "[4/16] the coverage table's rows where the two targets differ"
run 'grep -E "^\| Z3_OP_(BADD|BSUB|BMUL|BNEG|BUDIV_I|BUREM_I|BSDIV_I|BSREM_I|FPA_ABS|FPA_IS_INF|FPA_IS_NEGATIVE|FPA_IS_POSITIVE|FPA_TO_FP|FPA_TO_IEEE_BV|FPA_TO_SBV|FPA_TO_UBV) " /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust/rust_report.md'

echo "[5/16] the sorts"
run "sed -n '\\%^### The sorts%,\\%^## 1\\.%p' $R/rust_report.md"

echo "[6/16] the population"
run "sed -n '\\%^## 1\\. The population%,\\%^## 2\\.%p' $R/rust_report.md"

echo "[7/16] the per-x table"
run "sed -n '\\%^## 2\\. Per x%,\\%^### What the control%p' $R/rust_report.md"

echo "[8/16] what the control does"
run "sed -n '\\%^### What the control%,\\%^## 3\\.%p' $R/rust_report.md"

echo "[9/16] example: collapsed to byte identity"
run "sed -n '\\%^### 3.1%,\\%^### 3.2%p' $R/rust_report.md"

echo "[10/16] example: proved, not byte-identical"
run "sed -n '\\%^### 3.2%,\\%^### 3.3%p' $R/rust_report.md"

echo "[11/16] example: disproved, with seeds"
run "sed -n '\\%^### 3.3%,\\%^## 4\\.%p' $R/rust_report.md"

echo "[12/16] the refusals"
run "sed -n '\\%^## 5\\. Refusals%,\\%^## 6\\.%p' $R/rust_report.md"

echo "[13/16] the disproved and the undecided"
run "sed -n '\\%^## 6\\. The disproved%,\\%^## 7\\.%p' $R/rust_report.md"

echo "[14/16] the per-opcode question"
run "sed -n '\\%^## 7\\. Task o8%,\\%^### Per x and per mnemonic%p' $R/rust_report.md"
run "sed -n '\\%^### Mnemonics never landed%,\\%^### NOT_COLLAPSED%p' $R/rust_report.md"
run "sed -n '\\%^### LANDED_ELSEWHERE%,\\%^### NOT_COLLAPSED%p' $R/rust_report.md"
run "sed -n '\\%^### NOT_COLLAPSED%,\\%^## 8\\.%p' $R/rust_report.md"

echo "[15/16] bounds and memory"
run "sed -n '\\%^## 8\\. Bounds%,\$p' $R/rust_report.md"

echo "[16/16] the guard over every json this task wrote"
run "python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $R/rust_facts.json $R/rust_facts2.json $R/rust_facts3.json $R/rust_facts4.json $R/coverage_table.json $R/rust_population.json $R/rust_indexes.json $R/rust_held.json $R/rust_sample.json $R/rust_run.json $R/rust_control.json $R/rust_peropcode.json $R/rust_results.json"
echo "lane o11_l17 done"
