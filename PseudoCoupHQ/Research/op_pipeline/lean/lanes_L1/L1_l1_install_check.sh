#!/bin/bash
# L1 lane 1 — is Lean installed in the image, and does a `lake` project
# build with no network at all?
#
# Three steps: the version line; a bare `lake new` project; a `lake build`
# of a trivial theorem written into that project.
set -u

TOTAL=3
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean

# elan and lake both want a writable HOME. /work is the instance's own
# tmpfs; nothing here is a deliverable.
export HOME=/work/L1home
mkdir -p "$HOME"

echo "[1/$TOTAL] lean --version, lake --version, and where they live"
echo "--- which lean; which lake"
which lean
which lake
echo "--- lean --version"
lean --version
echo "--- lake --version"
lake --version
echo "--- elan toolchain list"
elan toolchain list
echo "--- ELAN_HOME=$ELAN_HOME  PATH carries /opt/elan/bin?"
echo "$PATH" | tr ':' '\n' | grep -n elan

echo "[2/$TOTAL] lake new archproof, in the artifact folder, with no network"
cd "$LEANDIR" || exit 1
rm -rf archproof
lake new archproof
echo "--- files lake created"
find archproof -type f -not -path '*/.git/*' | sort
echo "--- archproof/lean-toolchain, LITERAL"
cat archproof/lean-toolchain
echo "--- archproof/lakefile.toml, LITERAL"
cat archproof/lakefile.toml 2>/dev/null || cat archproof/lakefile.lean 2>/dev/null

echo "[3/$TOTAL] a trivial theorem over BitVec, and lake build"
cat > archproof/Archproof/Smoke.lean <<'LEAN'
-- The smallest possible check that this toolchain proves anything:
-- one arithmetic identity over 32-bit words, discharged by bv_decide,
-- which bit-blasts the goal to a SAT solver and checks the solver's
-- certificate inside Lean's kernel.
theorem smoke_add_comm (v0 v1 : BitVec 32) : v0 + v1 = v1 + v0 := by
  bv_decide
LEAN
cat > archproof/Archproof.lean <<'LEAN'
import Archproof.Basic
import Archproof.Smoke
LEAN
echo "--- Archproof/Smoke.lean, LITERAL"
cat archproof/Archproof/Smoke.lean
echo "--- lake build"
cd archproof || exit 1
time lake build
echo "--- lake build exit $?"
