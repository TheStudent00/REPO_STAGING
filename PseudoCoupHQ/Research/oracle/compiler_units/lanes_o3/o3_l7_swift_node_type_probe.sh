#!/usr/bin/env bash
# lane 7 -- task o3b, correction: confirm the swift grammar's node
# kinds by parsing one tiny snippet per operator inside this o3
# instance and printing the actual node.type tree-sitter produces --
# not guessed, not asserted from memory. This is what showed `!=`,
# `<=`, `>=` land under the generic `infix_expression` node instead of
# the dedicated `comparison_expression` / `equality_expression` node
# that `==`, `<`, `>`, `===` land under.
set -euo pipefail
echo "[1/1] swift_node_type_probe.py (one snippet per swift operator)"
python3 PseudoCoupHQ/Research/oracle/compiler_units/swift_node_type_probe.py
echo "[1/1] done"
