#!/bin/bash
# lp1_l15_emit_with_zc_zb_and_build.sh -- the coordinator's first lane of the
# fourth launch (Fable in the foreground, on the owner's word 2026-09-14). The
# handful's ten bodies carry C-extension words (c.add, the c.jr return) and
# pass A meets Zba/Zbb/Zbs, so the emit's module selection grows; the emit
# is minutes now. Same green pair: model 6266b40c, sail 8eb1fb6b. Then the
# Lean build of the new emit, into /persist. The Sail Lean library is copied
# from the already-built project; a fetch happens only if lake insists, and
# is reported.
set -uo pipefail
total=7
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
MODS="I_insts M_insts Zca Zcb Zba Zbb Zbs postlude main"
NAME=sail-riscv_6266b40c_sail_8eb1fb6b_I_M_Zca_Zcb_Zba_Zbb_Zbs_postlude_main
CACHE=PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/$NAME
P=/persist/lp1/Lean_IMZ
echo "[1/$total] tools, LITERAL (this lane fetches nothing unless lake insists; see step 6)"
which sail; sail --version; git -C $SRC log -1 --format='model %h %ci'; git -C /persist/sail-src log -1 --format='sail %h %ci' 2>/dev/null
ls $ELAN_HOME/bin | tr '\n' ' '; echo; ls $ELAN_HOME/toolchains; ls -la $CFG || { echo "FLAG: config missing"; exit 3; }
echo "[2/$total] the selection, resolved first: sail --list-files $MODS"
cd $SRC/model
sail --config $CFG --list-files $MODS riscv.sail_project 2>&1 | tr ' ' '\n' | grep -v '^$' > /work/files.txt
echo "  files: $(wc -l < /work/files.txt)"
grep -E 'base_insts|mext_insts|zca|zcb|zba|zbb|zbs|Zc|Zb' /work/files.txt | sed 's/^/  /'
grep -q 'mext_insts.sail' /work/files.txt || { echo "FLAG: selection did not resolve; output:"; head -5 /work/files.txt; exit 3; }
echo "[3/$total] the emit"
OUT=/work/emit; rm -rf $OUT /work/smtcache; mkdir -p $OUT
start=$(date +%s)
sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache \
  --config $CFG --lean --memo-z3 --lean-output-dir $OUT --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  --lean-noncomputable \
  --lean-noncomputable-function encdec_forwards --lean-noncomputable-function encdec_backwards \
  --lean-noncomputable-function encdec_forwards_matches --lean-noncomputable-function encdec_backwards_matches \
  --lean-noncomputable-function encdec_compressed_forwards --lean-noncomputable-function encdec_compressed_backwards \
  --lean-noncomputable-function encdec_compressed_forwards_matches --lean-noncomputable-function encdec_compressed_backwards_matches \
  --lean-import-file ../handwritten_support/RiscvExtras.lean -o Lean_IMZ \
  $MODS riscv.sail_project > /work/emit.log 2>&1
rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"; grep -vE 'Redundant|\^|^\s*\|' /work/emit.log | grep -vE '^\s*$' | head -4 | cut -c1-160
[ $rc -eq 0 ] || { echo "FLAG: the emit failed"; tail -20 /work/emit.log; exit 3; }
echo "  Lean files: $(find $OUT/Lean_IMZ -name '*.lean' | wc -l); lines: $(find $OUT/Lean_IMZ -name '*.lean' | xargs cat | wc -l)"
echo "[4/$total] into the cache $CACHE"
mkdir -p $CACHE && cp -a $OUT/Lean_IMZ/. $CACHE/ && cp /work/emit.log $CACHE/emit_lane.log
cat > $CACHE/MANIFEST.md <<M
# the cached emit: Sail's Lean output for the RISC-V model, the green pair, with C and Zb

- model: \`sail-riscv\` commit \`6266b40c1c\` (2026-08-20, the last commit whose own Lean CI passed), clone at /persist/sail-riscv-6266b40c, config \`build/config/rv64d_v256_e64.json\`
- sail: built from source at \`8eb1fb6b5b\` (branch sail2, 2026-08-18, the head on that date), Lean backend
- modules handed to sail (LEAF names): \`$MODS\`, resolved to $(wc -l < /work/files.txt) source files
- lane: \`lp1_l15_emit_with_zc_zb_and_build.sh\`, tower instance \`lp1\`, 2026-09-14; the lane's log is beside this file as \`emit_lane.log\`
- product: \`LeanIMZ/*.lean\`; the lake project the backend wrote (\`lakefile.toml\`, \`lean-toolchain\`)
- a BUILD PRODUCT cached by the model commit, the sail commit and the module list in its name; nobody edits a file in it
M
ls $CACHE | head; grep -E 'rev|name' $CACHE/lakefile.toml; cat $CACHE/lean-toolchain
echo "[5/$total] the built project in /persist: $P (the Sail Lean library copied from the built 6266b40c project)"
rm -rf $P; cp -a $CACHE $P; mkdir -p $P/.lake
cp -a /persist/lp1/Lean_IM_6266b40c/.lake/packages $P/.lake/ 2>/dev/null && echo "  packages copied: $(ls $P/.lake/packages)"
if diff <(grep -E '^rev' $CACHE/lakefile.toml) <(grep -E '^rev' /persist/lp1/Lean_IM_6266b40c/lakefile.toml) >/dev/null; then cp /persist/lp1/Lean_IM_6266b40c/lake-manifest.json $P/ && echo "  same lean-sail rev; manifest copied"; else echo "  lean-sail rev differs from the built project; lake may fetch (proxy on, github allowed); said so"; fi
echo "[6/$total] lake build"
cd $P; cat lean-toolchain; start=$(date +%s)
lake build > /work/lake.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake.log | head -14 | cut -c1-200
grep -qiE 'fetch|clon|download' /work/lake.log && { echo "  FETCHED during lake build (LITERAL):"; grep -iE 'fetch|clon|download' /work/lake.log | head -5; }
echo "  modules built: $(find $P/.lake/build/lib -name '*.olean' 2>/dev/null | wc -l) olean files of $(find $P/LeanIMZ -name '*.lean' | wc -l) sources"
echo "[7/$total] what the emit holds for the walk"
grep -c '^def execute_\|^noncomputable def execute_' $P/LeanIMZ/InstsEnd.lean | sed 's/^/  execute clauses: /'
grep -n 'ExecuteAs' $P/LeanIMZ/InstsEnd.lean | head -3 | cut -c1-140
grep -n '^def encdec_compressed_forwards\|^noncomputable def encdec_compressed_forwards\|^def encdec_forwards\|^noncomputable def encdec_forwards' $P/LeanIMZ/InstsEnd.lean | cut -c1-140
cp /work/lake.log $CACHE/lake_build.log; echo done
