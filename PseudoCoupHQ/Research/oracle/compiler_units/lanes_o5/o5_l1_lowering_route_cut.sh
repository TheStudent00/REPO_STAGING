#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] lowering_route_cut.py -- o4's go_compiler/clang_llvm_cpp variant sites cut to the LOWERING ROUTE (task 95 emitter defs + task 81/72 diaries)"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.py
echo "exit: $?"
