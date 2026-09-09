#!/bin/bash
# task o11, lane 15: the one evidence block lane 12 printed with its
# quoting dropped -- the coverage table's rows where the c cell and the
# rust cell disagree.
set -u
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust

run() {
  echo "\$ $1"
  eval "$1"
  echo
}

echo "[1/1] the coverage table's rows where the two targets differ"
run 'grep -E "^\| Z3_OP_(BADD|BSUB|BMUL|BNEG|BUDIV_I|BUREM_I|BSDIV_I|BSREM_I|FPA_ABS|FPA_IS_INF|FPA_IS_NEGATIVE|FPA_IS_POSITIVE|FPA_TO_FP|FPA_TO_IEEE_BV|FPA_TO_SBV|FPA_TO_UBV) " /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust/rust_report.md'
echo "lane o11_l15 done"
