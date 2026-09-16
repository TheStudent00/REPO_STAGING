#!/usr/bin/env bash
# lp1 lane 1e -- lane 1d's `lake build LeanIM.Defs` failed and the lane
# cut the output to its tail. This lane fetches nothing (proxy variables
# unset) and prints the FIRST errors of that build in full, LITERAL, so
# the cause is named from the object and not guessed.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
echo "this lane fetches nothing: http_proxy=${http_proxy:-unset}"
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/opam/default/bin:$PATH
export HOME=/work
PROJ=/persist/lp1/Lean_IM
cd "$PROJ"
total=2
echo "[1/$total] lake build LeanIM.Defs, the first 60 lines of its output"
lake build LeanIM.Defs 2>&1 | head -60
echo "[2/$total] lean on the file directly, first 40 lines, plus the lines it points at"
lake env lean LeanIM/Defs.lean 2>&1 | head -40
for n in 620 625 626; do echo "  Defs.lean:$n: $(sed -n "${n}p" LeanIM/Defs.lean)"; done
echo "lane lp1_l1e done"
