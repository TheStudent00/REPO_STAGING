#!/usr/bin/env bash
# lp1 lane 19 -- brief §2 lane 2 over the FOURTH cache (the all-modules emit lane 16 wrote; the handful is measured against it), the same reader as lane 14 over the four-module one. Lane 14 was: brief §2 lane 2 over the THIRD cache (model 6266b40c1c,
# sail 8eb1fb6b5b), through the module: `SailModel.definitions` and
# `key_of` list the execute clauses of the emit, count them by extension
# from the model's own source tree (the clone /persist/sail-riscv-6266b40c;
# the mounted /sources/sail-riscv is the LATER commit 3243f93 and is not
# used), and read every key (mnemonic, operand form, width) from the
# model's own assembly clause and `instruction` inductive -- no typed list
# of mnemonics anywhere. `strip`'s simp-unfolded form (DIV and one MUL
# clause) is the handful lane's (lane 15), where the harness runs it
# through the model's own execute; here the two clauses are quoted RAW,
# LITERAL, from the cache. THIS LANE FETCHES NOTHING (proxy variables
# unset). Memory bound 6 GB, abort ABORT_MEMORY_LP1 (a text reader; peak
# printed). One process, no pool, no clock. Then the spelling guard over
# the json, and `grep -c exempt` over the files this launch added.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
export PATH=/opt/venv/bin:$PATH
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules
EMIT=$CACHE/LeanIM
MODEL=/persist/sail-riscv-6266b40c/model
OP=$P/Research/op_pipeline
OUT=$LP/lp1_definitions_6266b40c_sail_8eb1fb6b_all_modules.json
total=7
echo "[1/$total] this lane fetches nothing: http_proxy=${http_proxy:-unset}"
echo "  emit tree: $EMIT ($(ls $EMIT/*.lean | wc -l) Lean files, $(cat $EMIT/*.lean | wc -l) lines)"
echo "  model source for the extension of each clause: $MODEL ($(git -C /persist/sail-riscv-6266b40c log -1 --format='%h %ci'))"
echo "  module: $LP/leanpath ($(ls $LP/leanpath/*.py | wc -l) files, $(cat $LP/leanpath/*.py | wc -l) lines)"

echo "[2/$total] SailModel.definitions over the third cache, through the module"
cd $LP
python3 -m leanpath definitions "$EMIT" "$MODEL" "$OUT"
echo "  rc=$?"

echo "[3/$total] the first 80 keys the module read (LITERAL; all are in the json), the counts by width and by operand form, and the clauses with no key"
python3 - "$OUT" <<'PY'
import json, sys
from collections import Counter
d = json.load(open(sys.argv[1]))
print("  keys: %d" % d["key_count"])
for k in d["keys"][:80]:
    print("    %-10s | %-22s | %d  <- %s" % (k["mnem"], k["operand_form"], k["width"], k["from_clause"]))
print("  keys by width (of %d): %s" % (d["key_count"], dict(Counter(k["width"] for k in d["keys"]))))
print("  keys by operand form (of %d):" % d["key_count"])
for f, n in Counter(k["operand_form"] for k in d["keys"]).most_common():
    print("    %-24s %d" % (f or "(none)", n))
print("  clauses by (extension, width):")
c = Counter((r["extension"], r["width"]) for r in d["clauses"])
for (e, w), n in sorted(c.items()):
    print("    %-10s width %2d : %2d clauses" % (e, w, n))
print("  clauses with no key: %s" % [r["clause"] for r in d["clauses"] if not r["mnem_count"]])
PY

echo "[4/$total] the modules of the emit inside and outside the import closure of LeanIM.lean (the modules built of the files), LITERAL"
python3 - "$CACHE" <<'PY'
import os, sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath.sail_model import SailModel
root = sys.argv[1]
cl = SailModel.import_closure(root)
files = sorted(f[:-5] for f in os.listdir(os.path.join(root, "LeanIM")) if f.endswith(".lean"))
inside = [f for f in files if "LeanIM." + f in cl]
outside = [f for f in files if "LeanIM." + f not in cl]
print("  modules in the closure: %d (plus LeanIM.lean itself); outside it: %d of %d files" % (len(inside), len(outside), len(files)))
print("  outside the closure (LITERAL): %s" % " ".join(outside))
PY

echo "[5/$total] strip's inputs RAW LITERAL from the third cache: the DIV clause and the MUL clause with its helper (the simp forms are lane 15's)"
awk '/^def execute_DIV /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' "$EMIT/InstsEnd.lean"
echo "  execute_MUL and mult_to_bits_half:"
awk '/^def execute_MUL /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' "$EMIT/InstsEnd.lean"
awk '/^def mult_to_bits_half /{p=1} p{print "    "$0} p&&/\.Low =>/{exit}' "$EMIT/Arithmetic.lean"

echo "[6/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$OUT" > /work/guard.txt 2>&1; grc=$?; sed "s/^/    /" /work/guard.txt
echo "  guard rc=$grc"

echo "[7/$total] grep -c exempt over the files this launch added (0 expected on every deliverable; a lane that RUNS the guard carries the word inside its command)"
for f in $LP/leanpath/*.py $LP/leanpath/lean/* $OUT $LP/lanes_lp1/lp1_l1[0-9]*.sh; do
  echo "    $(grep -c exempt "$f") $(basename "$f")"
done
echo "lane lp1_l19 done at $(date -u +%FT%TZ)"
