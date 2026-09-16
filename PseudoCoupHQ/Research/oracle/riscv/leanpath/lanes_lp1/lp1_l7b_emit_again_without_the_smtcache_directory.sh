#!/usr/bin/env bash
# lp1 lane 7b -- lane 7 AGAIN, one change: lane 7 pre-created /work/smtcache as a
# DIRECTORY (a mkdir of mine, not in the verbatim invocation) and this sail
# writes its --memo-z3-path as a FILE, so the run ended rc=2 with
# "/work/smtcache: Is a directory" AFTER writing the Lean tree (117 files,
# 63,066 lines, 216 s). This lane makes no such directory; the product of the
# rc=2 run is replaced by this rc-checked one; lane 7's own output stays
# beside as emit_lane_l7_rc2.log (the record).
# lp1 lane 7 -- the re-emit (brief §4, lane 7): the sail compiler built in
# lane 6 from source at 5745ea9e53 (in the copied opam root /persist/opam)
# runs its Lean backend over the model, the invocation of log 274 §3
# VERBATIM (working directory /opt/sail-riscv-src/model, the image's
# configured clone at commit 3243f93, config
# build/config/rv64d_v256_e64.json, leaf modules I_insts M_insts postlude
# main), into a NEW cache folder whose name carries BOTH commits:
#   Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/
# with MANIFEST.md in the shape of the first cache's and this lane's own
# output beside it as emit_lane.log. THIS LANE FETCHES NOTHING (proxy
# variables unset). Bounded by the instance (20g); the sail process's
# peak resident and the cgroup peak are printed. The first cache folder
# is not touched. About 45 minutes (log 274 §3, l5: 45.5 min, 17 GB).
set -u
set -o pipefail
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
export OPAMROOT=/persist/opam
export OPAMSWITCH=default
export OCAMLFIND_CONF=/persist/opam/default/lib/findlib.conf
export PATH=/persist/opam/default/bin:/opt/venv/bin:$PATH
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main
FIRST=$LP/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main
SRC=/opt/sail-riscv-src
cfg=$SRC/build/config/rv64d_v256_e64.json
total=7
i=1
step() { echo "[$i/$total] $1"; i=$((i+1)); echo "  at $(date -u +%FT%TZ)"; }
peak() { echo "  cgroup memory.peak: $(cat /sys/fs/cgroup/memory.peak 2>/dev/null || echo unreadable) bytes; memory.current: $(cat /sys/fs/cgroup/memory.current 2>/dev/null || echo unreadable)"; }
timed() {
python3 - "$@" <<'PY'
import resource, subprocess, sys, time
cmd = sys.argv[1:]
t0 = time.time()
p = subprocess.run(cmd)
t1 = time.time()
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print("  rc=%d wall=%.1fs largest-descendant peak resident=%d kB" % (p.returncode, t1 - t0, ru.ru_maxrss))
sys.exit(p.returncode)
PY
}
mkdir -p "$CACHE"; if [ -f "$CACHE/emit_lane.log" ] && [ ! -f "$CACHE/emit_lane_l7_rc2.log" ]; then mv "$CACHE/emit_lane.log" "$CACHE/emit_lane_l7_rc2.log"; fi; rm -rf "$CACHE/LeanIM" "$CACHE/LeanIM.lean" "$CACHE/lakefile.toml" "$CACHE/lake-manifest.json" "$CACHE/lean-toolchain" "$CACHE/.gitignore"

main() {
step "this lane fetches nothing: http_proxy=${http_proxy:-unset}; the sail it uses, LITERAL"
echo "  which sail: $(command -v sail)"
echo "  sail --version: $(sail --version 2>&1)"
echo "  sail --dir: $(sail --dir 2>&1)"
echo "  z3: $(command -v z3 || echo ABSENT) $(z3 --version 2>&1 | head -1)"
echo "  the model: $SRC (the image's configured clone)"
git -C $SRC log -1 --format='  model commit %H %ci %s' 2>&1 | head -2
echo "  /sources/sail-riscv (the mounted source, for the record): $(git -C /sources/sail-riscv log -1 --format='%h %ci' 2>&1 | head -1)"
echo "  config: $cfg ($(stat -c %s $cfg 2>&1) bytes)"
echo "  the cache folder this lane writes: $CACHE"
echo "  the first cache folder, NOT touched: $FIRST ($(ls $FIRST/LeanIM/*.lean 2>/dev/null | wc -l) Lean files)"

step "sail --list-files I_insts M_insts postlude main riscv.sail_project (seconds; LEAF names, checked first)"
cd $SRC/model
timed sail --list-files I_insts M_insts postlude main riscv.sail_project > /work/listfiles.txt 2>&1
echo "  files resolved: $(tr ' ' '\n' < /work/listfiles.txt | grep -c '\.sail$')"
tr ' ' '\n' < /work/listfiles.txt | grep -E 'base_insts.sail|mext_insts.sail|insts_end.sail' | sed 's/^/    /'

step "the emit: sail --lean, the invocation of log 274 §3 verbatim, timed (no /work/smtcache is made beforehand; the sail process peak resident is the largest-descendant figure)"
rm -rf /work/smtcache /work/leanout; mkdir -p /work/leanout
cd $SRC/model
timed sail --strict-var --strict-bitvector --strict-exponentials \
  --memo-z3-path /work/smtcache --config $cfg --lean --memo-z3 \
  --lean-output-dir /work/leanout --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult \
  --lean-non-beq-type Step --lean-noncomputable \
  --lean-noncomputable-function encdec_forwards \
  --lean-noncomputable-function encdec_backwards \
  --lean-noncomputable-function encdec_forwards_matches \
  --lean-noncomputable-function encdec_backwards_matches \
  --lean-noncomputable-function encdec_compressed_forwards \
  --lean-noncomputable-function encdec_compressed_backwards \
  --lean-noncomputable-function encdec_compressed_forwards_matches \
  --lean-noncomputable-function encdec_compressed_backwards_matches \
  --lean-import-file ../handwritten_support/RiscvExtras.lean \
  -o Lean_IM I_insts M_insts postlude main riscv.sail_project 2>&1 | tail -30
echo "  emit rc=$?"
peak

step "what the backend wrote (LITERAL sizes), and the two facts the first launch flagged: the leak count and execute_DIV's line"
ls -la /work/leanout/Lean_IM 2>&1 | sed 's/^/    /'
echo "  Lean files: $(ls /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l); lines: $(cat /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l); bytes: $(du -sb /work/leanout/Lean_IM 2>/dev/null | cut -f1)"
echo "  lakefile.toml (LITERAL):"; sed 's/^/    /' /work/leanout/Lean_IM/lakefile.toml 2>&1
echo "  lean-toolchain (LITERAL): $(cat /work/leanout/Lean_IM/lean-toolchain 2>&1)"
echo "  lake-manifest.json (LITERAL):"; sed 's/^/    /' /work/leanout/Lean_IM/lake-manifest.json 2>&1
echo "  occurrences of 'is_sv32_mode(' (the first emit's leak, 3 sites in Defs.lean): $(grep -rho 'is_sv32_mode(' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l)"
echo "  the same three abbrevs now (LITERAL, grep -n 'vpn_level_size\|abbrev pte_bits\|abbrev ppn_bits'):"
grep -rn 'abbrev vpn_level_size\|abbrev pte_bits\|abbrev ppn_bits' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | head -6 | sed 's/^/    /'
echo "  execute clauses: $(grep -rhoE '^def execute_[A-Za-z0-9_]+' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | sort -u | wc -l)"
echo "  execute_DIV at: $(grep -rn '^def execute_DIV ' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | cut -d: -f1,2)"
echo "  the DIV clause as this sail wrote it (LITERAL):"
awk '/^def execute_DIV /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' /work/leanout/Lean_IM/LeanIM/InstsEnd.lean 2>/dev/null

step "copy the emit into the cache folder (a build product; nobody edits a file in it)"
cp -r /work/leanout/Lean_IM/. "$CACHE"/
ls -la "$CACHE" | sed 's/^/    /'
echo "  Lean files in the cache: $(ls $CACHE/LeanIM/*.lean | wc -l); lines: $(cat $CACHE/LeanIM/*.lean | wc -l)"

step "MANIFEST.md, in the shape of the first cache's"
SAILV="$(sail --version 2>&1)"
MC="$(git -C $SRC log -1 --format='%h (%ci)' 2>/dev/null || echo '3243f93 (2026-09-09 21:47:21 +0000)')"
NF="$(tr ' ' '\n' < /work/listfiles.txt | grep -c '\.sail$')"
NL="$(cat $CACHE/LeanIM/*.lean | wc -l)"
DIVAT="$(grep -rn '^def execute_DIV ' $CACHE/LeanIM/*.lean | head -1 | sed "s#$CACHE/##" | cut -d: -f1,2)"
REQ="$(grep -A3 '^\[\[require\]\]' $CACHE/lakefile.toml | tr '\n' ' ')"
TC="$(cat $CACHE/lean-toolchain)"
cat > "$CACHE/MANIFEST.md" <<EOF
# the cached emit: Sail's Lean output for the RISC-V model (second emit, sail built from source)

- model: \`sail-riscv\` commit $MC, the
  image's clone \`/opt/sail-riscv-src\`, config
  \`build/config/rv64d_v256_e64.json\`
- sail: $SAILV, built from source in lane
  \`lp1_l6_build_sail_from_source.sh\` (branch \`sail2\`, the head before the
  model's own commit of 2026-09-09; the model's CI builds its Lean with
  sail "latest" by this recipe), Lean backend; the opam root is the copy
  \`/persist/opam\` on the tower instance \`lp1\`'s persistent volume
- modules handed to sail (LEAF names): \`I_insts M_insts postlude main\`,
  resolved to $NF source files, \`base_insts.sail\` and \`mext_insts.sail\`
  among them
- lane: \`lp1_l7_emit_with_sail_5745ea9e.sh\`, tower instance \`lp1\`,
  2026-09-13/14, 20 GB cap; the lane's own output is beside this file as
  \`emit_lane.log\`; the invocation is in log 274 §3, verbatim
- product: \`LeanIM/*.lean\`, $NL lines; \`execute_DIV\` at
  \`$DIVAT\`; the lake project requires $REQ and toolchain
  \`$TC\` (\`lean-toolchain\`)
- the first emit (sail 0.20.2 from opam) is the co-folder
  \`sail-riscv_3243f93_I_insts_M_insts_postlude_main/\`, kept as the record
  of the build failure log 275 §4.2 flags; nothing in it is edited
- this folder is a BUILD PRODUCT, cached by the model commit, the sail
  commit and the module list in its name; the regeneration test deletes
  it and gets it back by running lanes 6 and 7. Nobody edits a file in it.
EOF
sed 's/^/    /' "$CACHE/MANIFEST.md"

step "sizes, the cgroup peak, and the work volume"
du -sh "$CACHE" /work/leanout /work/smtcache 2>&1 | sed 's/^/    /'
df -h /work | tail -1 | sed 's/^/    /'
peak
echo "lane lp1_l7b done at $(date -u +%FT%TZ)"
}
main 2>&1 | tee "$CACHE/emit_lane.log"
