#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] grep -c exempt over the §7 regenerated/added files"
grep -c exempt \
  PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.json \
  PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.py \
  PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.md \
  PseudoCoupHQ/Research/oracle/compiler_units/lanes_o4/o4_l4_nested_operands_regen.sh \
  PseudoCoupHQ/Research/oracle/compiler_units/lanes_o4/o4_l5_spelling_guard.sh
echo "[1/1] done"
