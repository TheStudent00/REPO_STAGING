#!/usr/bin/env bash
# lp1 lane 9d -- lane 9c again after the guard REFUSED lane 9c's json on its
# merits: the per-clause row carried a LIST of mnemonics (`mnems`), and the
# guard reads a list element `and` / `or` / `xor` as a bare operator token
# in a row structure. The clause row now carries only the COUNT; every
# mnemonic is one key row in the exempt machine-form field `mnem`. Also:
# the guard's rc is captured from the guard, not from the sed after it.
# lp1 lane 9c -- lane 9b again after a second one-line fix: the constructor
# reader dropped the LAST constructor of the `instruction` inductive (no
# newline before `deriving`), so REMW read an empty operand form; nothing
# else changed.
# lp1 lane 9b -- lane 9 again after one fix in the module: the map reader
# missed every `def X_forwards ... : String :=` (the def line ends in `:=`,
# no `do`), so 13 of 29 clauses read no key; nothing else changed.
# lp1 lane 9 -- brief §2 lane 2 over the NEW cache, the part that needs
# no built model, THROUGH THE MODULE this time: `SailModel.definitions`
# and `key_of` of Research/oracle/riscv/leanpath/leanpath/ list the
# execute clauses of the second emit (sail 5745ea9e), count them by
# extension from the model's own source tree, and read every key
# (mnemonic, operand form, width) from the model's own assembly clause
# and `instruction` inductive -- no typed list of mnemonics anywhere.
# strip's simp-unfolded form is NOT here: the emit does not build (lane
# 8, the flag the task stops at); the DIV and MUL clauses are shown RAW,
# LITERAL, from the new cache. THIS LANE FETCHES NOTHING (proxy
# variables unset). Memory bound 6 GB, abort ABORT_MEMORY_LP1 (a text
# reader; peak printed). One process, no pool, no clock. Then the
# spelling guard over the json, and `grep -c exempt` over the files
# this task added.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
export PATH=/opt/venv/bin:$PATH
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main
EMIT=$CACHE/LeanIM
MODEL=/sources/sail-riscv/model
OP=$P/Research/op_pipeline
OUT=$LP/lp1_definitions_sail_5745ea9e.json
total=6
echo "[1/$total] this lane fetches nothing: http_proxy=${http_proxy:-unset}"
echo "  emit tree: $EMIT ($(ls $EMIT/*.lean | wc -l) Lean files, $(cat $EMIT/*.lean | wc -l) lines)"
echo "  module: $LP/leanpath ($(ls $LP/leanpath/*.py | wc -l) files, $(cat $LP/leanpath/*.py | wc -l) lines)"

echo "[2/$total] SailModel.definitions over the new cache, through the module"
cd $LP
python3 -m leanpath definitions "$EMIT" "$MODEL" "$OUT"
echo "  rc=$?"

echo "[3/$total] every key the module read (LITERAL, all of them), and the clauses with no key"
python3 - "$OUT" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("  keys: %d" % d["key_count"])
for k in d["keys"]:
    print("    %-10s | %-14s | %d  <- %s" % (k["mnem"], k["operand_form"], k["width"], k["from_clause"]))
print("  clauses by (extension, width):")
from collections import Counter
c = Counter((r["extension"], r["width"]) for r in d["clauses"])
for (e, w), n in sorted(c.items()):
    print("    %-10s width %2d : %2d clauses" % (e, w, n))
print("  clauses with no key: %s" % [r["clause"] for r in d["clauses"] if not r["mnem_count"]])
PY

echo "[4/$total] strip on DIV, RAW LITERAL from the new cache (the simp form awaits the build)"
awk '/^def execute_DIV /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' "$EMIT/InstsEnd.lean"
echo "  the MUL clause and its helper mult_to_bits_half, RAW LITERAL:"
awk '/^def execute_MUL /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' "$EMIT/InstsEnd.lean"
awk '/^def mult_to_bits_half /{p=1} p{print "    "$0} p&&/\.Low =>/{exit}' "$EMIT/Arithmetic.lean"

echo "[5/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$OUT" > /work/guard.txt 2>&1; grc=$?; sed "s/^/    /" /work/guard.txt
echo "  guard rc=$grc"

echo "[6/$total] grep -c exempt over the files lp1's second launch added (0 expected on every deliverable; a lane that RUNS the guard carries the word inside its command)"
for f in $LP/leanpath/*.py $OUT $LP/lanes_lp1/lp1_l6_*.sh $LP/lanes_lp1/lp1_l7_*.sh $LP/lanes_lp1/lp1_l7b_*.sh $LP/lanes_lp1/lp1_l8_*.sh $LP/lanes_lp1/lp1_l9_*.sh $LP/lanes_lp1/lp1_l9b_*.sh $LP/lanes_lp1/lp1_l9c_*.sh $LP/lanes_lp1/lp1_l9d_*.sh; do
  echo "    $(grep -c exempt "$f") $(basename "$f")"
done
echo "lane lp1_l9d done at $(date -u +%FT%TZ)"
