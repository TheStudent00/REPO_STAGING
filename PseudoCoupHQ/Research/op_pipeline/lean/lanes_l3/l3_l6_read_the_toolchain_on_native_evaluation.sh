#!/bin/bash
# l3 lane 6 -- READ, off the installed toolchain rather than from memory, how
# `Lean.ofReduceBool` enters a `bv_decide` proof and whether this Lean has any
# route that closes the same goal without it.  Nothing is proved here; this
# lane only quotes the toolchain.
set -u
export HOME=/work/l3home
mkdir -p "$HOME"
SRC=/opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean

echo "[1/5] every tactic syntax Std.Tactic.BVDecide declares"
grep -n "^syntax\|^macro\|elab \"\|syntax (name" "$SRC/Std/Tactic/BVDecide/Syntax.lean"

echo "[2/5] where the LRAT certificate is checked, and what it uses"
grep -n "ofReduceBool\|ofReduceNat\|mkAuxDecl\|Decidable\|kernel" \
     "$SRC/Lean/Elab/Tactic/BVDecide/Frontend/LRAT.lean"

echo "[3/5] the same in the bv_decide frontend"
grep -n "ofReduceBool\|trustCompiler\|native\|kernel" \
     "$SRC/Lean/Elab/Tactic/BVDecide/Frontend/BVDecide.lean" \
     "$SRC/Lean/Elab/Tactic/BVDecide/Frontend/BVCheck.lean"

echo "[4/5] the doc comment on the ofReduceBool use, LITERAL"
grep -n "ofReduceBool" -B 20 "$SRC/Lean/Elab/Tactic/BVDecide/Frontend/LRAT.lean" | head -60

echo "[5/5] what `decide` offers beside native evaluation in this Lean"
grep -n "kernel\|native" "$SRC/Init/Tactics.lean" | grep -i "decide" | head -30
grep -n "structure DecideConfig" -A 25 "$SRC/Init/Tactics.lean" | head -40
echo "--- exit $?"
