#!/usr/bin/env bash
# lp1 lane 16 -- the emit AGAIN with the module selection the model's own Lean CI uses: `--all-modules` (model/CMakeLists.txt:9, `set(SAIL_MODULES "--all-modules" ...)`, LITERAL in lane 10b's clone), in place of the four leaf names. Brief §1 permits another selection into a new cache folder named the same way. Why: under `I_insts M_insts postlude main` the model's `currentlyEnabled` is partial (61 of 126 arms; the emit's own warning named `Ext_A`), and both the model's `sail_model_init` (through `legalize_mseccfg` -> `Ext_S` -> `Ext_Zicsr`) and the decoder's first guard reach its catch-all `assert false "Pattern match failure at extensions/M/mext_insts.sail:14"` -- lane 13d, LITERAL -- so no init and no decode completes on that emit. Otherwise as lane 11: The
# sail built in lane 10 (sail2 at 8eb1fb6b5b, in the copied opam root
# /persist/opam) runs its Lean backend over the model clone at 6266b40c1c
# (/persist/sail-riscv-6266b40c, the model's last commit whose Lean CI was
# green), the invocation of log 274 §3 verbatim except for the two paths the
# brief names (that clone's model dir and its own config,
# build/config/rv64d_v256_e64.json, produced by lane 10b), leaf modules
# I_insts M_insts postlude main, into the NEW cache folder whose name
# carries both commits:
#   Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_I_insts_M_insts_postlude_main/
# with MANIFEST.md in the existing shape and this lane's own output beside
# it as emit_lane.log. THIS LANE FETCHES NOTHING (proxy variables unset).
# No /work/smtcache directory is pre-made (log 276 §4.3). Bounded by the
# instance (20g); the sail process's peak resident and the cgroup peak are
# printed. The two earlier cache folders are not touched. Expected minutes
# (the second launch measured 217 s with a from-source sail).
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
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules
SECOND=$LP/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main
SRC=/persist/sail-riscv-6266b40c
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
mkdir -p "$CACHE"

main() {
step "this lane fetches nothing: http_proxy=${http_proxy:-unset}; the sail and the model it uses, LITERAL"
echo "  which sail: $(command -v sail)"
echo "  sail --version: $(sail --version 2>&1)"
echo "  sail --dir: $(sail --dir 2>&1)"
echo "  z3: $(command -v z3 || echo ABSENT) $(z3 --version 2>&1 | head -1)"
echo "  the model: $SRC"
git -C $SRC log -1 --format='  model commit %H %ci %s' 2>&1 | head -2
echo "  config: $cfg ($(stat -c %s $cfg 2>&1) bytes, sha256 $(sha256sum $cfg | cut -c1-16)...)"
echo "  the cache folder this lane writes: $CACHE"
echo "  the three earlier cache folders, NOT touched: $(ls -d $LP/cache/sail-riscv_3243f93* $LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_I_insts* | tr "\n" " ")"

step "sail --list-files --all-modules riscv.sail_project (seconds; the CI's selection, checked first)"
cd $SRC/model
timed sail --list-files --all-modules riscv.sail_project > /work/listfiles.txt 2>&1
echo "  files resolved: $(tr ' ' '\n' < /work/listfiles.txt | grep -c '\.sail$')"
tr ' ' '\n' < /work/listfiles.txt | grep -E 'base_insts.sail|mext_insts.sail|insts_end.sail' | sed 's/^/    /'

step "the emit: sail --lean, the invocation of log 274 §3 with this clone's paths, timed (no /work/smtcache made beforehand; the sail process peak resident is the largest-descendant figure)"
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
  -o Lean_IM --all-modules riscv.sail_project 2>&1 | tail -30
echo "  emit rc=$?"
peak

step "what the backend wrote (LITERAL sizes), the pins, the leak count of the earlier emits, execute_DIV's line"
ls -la /work/leanout/Lean_IM 2>&1 | sed 's/^/    /'
echo "  Lean files: $(ls /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l); lines: $(cat /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l); bytes: $(du -sb /work/leanout/Lean_IM 2>/dev/null | cut -f1)"
echo "  lakefile.toml (LITERAL):"; sed 's/^/    /' /work/leanout/Lean_IM/lakefile.toml 2>&1
echo "  lean-toolchain (LITERAL): $(cat /work/leanout/Lean_IM/lean-toolchain 2>&1)"
echo "  lake-manifest.json (LITERAL):"; sed 's/^/    /' /work/leanout/Lean_IM/lake-manifest.json 2>&1
echo "  occurrences of 'is_sv32_mode(' (the earlier emits' leak, 3 sites in Defs.lean): $(grep -rho 'is_sv32_mode(' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l)"
echo "  Sail call syntax of any type-level function in a Lean abbrev (grep 'abbrev .*[a-z_]([a-z_]' ): $(grep -rhoE '^abbrev .*[a-z_]\([a-z_]' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | wc -l)"
echo "  execute clauses: $(grep -rhoE '^def execute_[A-Za-z0-9_]+' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | sort -u | wc -l)"
echo "  execute_DIV at: $(grep -rn '^def execute_DIV ' /work/leanout/Lean_IM/LeanIM/*.lean 2>/dev/null | cut -d: -f1,2)"
echo "  the DIV clause as this sail wrote it (LITERAL):"
awk '/^def execute_DIV /{p=1} p{print "    "$0} p&&/RETIRE_SUCCESS/{exit}' /work/leanout/Lean_IM/LeanIM/InstsEnd.lean 2>/dev/null

step "copy the emit into the cache folder (a build product; nobody edits a file in it)"
cp -r /work/leanout/Lean_IM/. "$CACHE"/
ls -la "$CACHE" | sed 's/^/    /'
echo "  Lean files in the cache: $(ls $CACHE/LeanIM/*.lean | wc -l); lines: $(cat $CACHE/LeanIM/*.lean | wc -l)"

step "MANIFEST.md, in the shape of the earlier caches'"
SAILV="$(sail --version 2>&1)"
MC="$(git -C $SRC log -1 --format='%h (%ci)' 2>/dev/null)"
NF="$(tr ' ' '\n' < /work/listfiles.txt | grep -c '\.sail$')"
NL="$(cat $CACHE/LeanIM/*.lean | wc -l)"
DIVAT="$(grep -rn '^def execute_DIV ' $CACHE/LeanIM/*.lean | head -1 | sed "s#$CACHE/##" | cut -d: -f1,2)"
REQ="$(grep -A3 '^\[\[require\]\]' $CACHE/lakefile.toml | tr '\n' ' ')"
TC="$(cat $CACHE/lean-toolchain)"
CFGSHA="$(sha256sum $cfg | cut -c1-64)"
cat > "$CACHE/MANIFEST.md" <<EOF2
# the cached emit: Sail's Lean output for the RISC-V model (third emit: the last pair the model's own Lean CI built green)

- model: \`sail-riscv\` commit $MC, the clone
  \`/persist/sail-riscv-6266b40c\` on the tower instance \`lp1\`'s persistent
  volume (lane \`lp1_l10_clone_last_green_model_and_build_sail_8eb1fb6b.sh\`),
  the model's last commit whose Lean workflow (\`compile-lean.yml\`) ran
  green (2026-08-20T16:29Z, measured through the GitHub API on
  2026-09-13 by the coordinator); config
  \`build/config/rv64d_v256_e64.json\` produced by that clone's own
  \`config/CMakeLists.txt\` (lane \`lp1_l10b_cmake_configure_without_asio.sh\`,
  cmake with the model's own \`-DDOWNLOAD_ASIO=OFF\`; sha256 $CFGSHA)
- sail: $SAILV, built from source in lane
  \`lp1_l10_clone_last_green_model_and_build_sail_8eb1fb6b.sh\` (branch
  \`sail2\`, the head on 2026-08-20; the model's CI builds its Lean with
  sail "latest" by this recipe), Lean backend; the opam root is the copy
  \`/persist/opam\` on the tower instance \`lp1\`'s persistent volume
- modules handed to sail: \`--all-modules\` (the CI's selection, model/CMakeLists.txt:9),
  resolved to $NF source files, \`base_insts.sail\` and \`mext_insts.sail\`
  among them
- lane: \`lp1_l16_emit_6266b40c_all_modules.sh\`, tower instance
  \`lp1\`, 2026-09-14, 20 GB cap; the lane's own output is beside this file
  as \`emit_lane.log\`; the invocation is in log 274 §3, verbatim but for
  the clone's two paths
- product: \`LeanIM/*.lean\`, $NL lines; \`execute_DIV\` at
  \`$DIVAT\`; the lake project requires $REQ and toolchain
  \`$TC\` (\`lean-toolchain\`)
- the two earlier emits are the co-folders
  \`sail-riscv_3243f93_I_insts_M_insts_postlude_main/\` (sail 0.20.2 from
  opam; log 275 §4.2) and
  \`sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main/\` (sail
  built at 5745ea9e; log 276 §4.1), kept as the records of the two build
  failures; nothing in them is edited
- this folder is a BUILD PRODUCT, cached by the model commit, the sail
  commit and the module list in its name; the regeneration test deletes
  it and gets it back by running lanes 10, 10b and 11. Nobody edits a
  file in it.
EOF2
sed 's/^/    /' "$CACHE/MANIFEST.md"

step "sizes, the cgroup peak, and the work volume"
du -sh "$CACHE" /work/leanout /work/smtcache 2>&1 | sed 's/^/    /'
df -h /work | tail -1 | sed 's/^/    /'
peak
echo "lane lp1_l16 done at $(date -u +%FT%TZ)"
}
main 2>&1 | tee "$CACHE/emit_lane.log"
