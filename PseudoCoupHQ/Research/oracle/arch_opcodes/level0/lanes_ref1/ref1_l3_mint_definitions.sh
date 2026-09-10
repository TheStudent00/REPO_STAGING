#!/usr/bin/env bash
# ref1 lane 3 -- the MInt function definitions, read from the third-party
# source itself, so the parser's grammar states each function's meaning from
# their own text rather than from a guess.  Nothing is copied out.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
total=6

echo "[1/$total] the wrapper file, whole"
wc -l $S/x86-mint-wrapper.k
cat $S/x86-mint-wrapper.k

echo "[2/$total] common/ file list"
ls -la $S/common/

echo "[3/$total] where negMInt, extractMInt, concatenateMInt are DEFINED"
grep -rn "syntax MInt ::=\|syntax Bool ::=\|syntax Int ::=" $S/*.k $S/common/*.k | head -60

echo "[4/$total] getParentValue / convToRegKeys / getFlag definitions"
grep -rn "getParentValue\|convToRegKeys\|rule getFlag\|syntax .*getFlag" $S/x86-configuration.k $S/common/*.k $S/*.k 2>/dev/null | head -40

echo "[5/$total] handleImmediateWithSignExtend"
grep -rn -A6 "handleImmediateWithSignExtend" $S/*.k $S/common/*.k 2>/dev/null | head -60

echo "[6/$total] shiftCountMask and the division helpers"
grep -rn -A8 "rule shiftCountMask\|syntax .*shiftCountMask\|rule idiv_quotient_int32\|rule div_quotient_int32" $S/*.k $S/common/*.k 2>/dev/null | head -60
