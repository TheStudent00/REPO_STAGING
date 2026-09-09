#!/usr/bin/env bash
# lane 8 -- task o3b, correction: SWIFT_RULE_TO_NODE_TYPES fixed at
# cause. Parsing `a != b` / `a <= b` / `a >= b` in this same runner
# image showed these three land under the generic `infix_expression`
# node (same catch-all this grammar version uses for a user-defined
# custom operator), not under `comparison_expression` /
# `equality_expression` the way `==` / `<` / `>` / `===` do.
# `_comparison_operator` and `_equality_operator` now map to BOTH
# node types; no token is special-cased -- the existing generic
# child-text scan in get_operator_text still does the matching.
# Regenerates compiler_operators_used.json / .md (all six rows).
set -euo pipefail
echo "[1/1] compiler_operators_used.py (all six rows, swift comparison/equality node-type fix)"
python3 PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.py
echo "[1/1] done"
