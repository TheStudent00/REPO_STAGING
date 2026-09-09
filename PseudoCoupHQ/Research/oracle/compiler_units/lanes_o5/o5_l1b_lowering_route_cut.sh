#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] lowering_route_cut.py -- route_examples given lang+unit fields (guard fix, o5_l2 findings)"
python3 PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.py
echo "exit: $?"
