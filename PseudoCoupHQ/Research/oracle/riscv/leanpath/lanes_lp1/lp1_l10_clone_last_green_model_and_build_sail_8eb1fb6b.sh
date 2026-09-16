#!/usr/bin/env bash
# lp1 lane 10 -- THIRD launch, brief §5 lane 10: the ONE fetch lane of this
# launch (github only). The coordinator pins the LAST GREEN PAIR of the
# model's own Lean CI (compile-lean.yml, last green run 2026-08-20T16:29Z):
#   model  sail-riscv at 6266b40c1c  -> cloned into /persist/sail-riscv-6266b40c
#   sail   sail2 at 8eb1fb6b5b       -> /persist/sail-src checked out there,
#          then the CI recipe: opam install . --deps-only --yes; make install,
#          OPAMROOT=/persist/opam (the copy lane 6 made; findlib.conf relocated)
# then `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DFIRST_PARTY_TESTS=OFF`
# in the model clone (its configure fetches CLI11 from github: the second
# reason this lane has the network) so that build/config/rv64d_v256_e64.json
# exists for that commit; then `sail --list-files I_insts M_insts postlude
# main riscv.sail_project` to confirm the leaf modules before lane 11 emits.
# Also, because the clone carries full history: the diff of extensions/I and
# extensions/M between 6266b40c1c and 3243f93 (brief §5's unverified row),
# LITERAL, saved under the artifact folder. A host the proxy refuses is a
# FLAG with the literal line; nothing is worked around. Sample first: one
# request per host, then the clone, then the sail build, then cmake.
# Wall time and peak resident per step; cgroup peak at the end.
set -u
export HOME=/work
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
MODEL=/persist/sail-riscv-6266b40c
SAILSRC=/persist/sail-src
MODEL_COMMIT=6266b40c1c
SAIL_COMMIT=8eb1fb6b5b
total=10
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

step "what the persistent volume holds from the two earlier launches (LITERAL), and this lane's proxy"
echo "  http_proxy=${http_proxy:-unset} https_proxy=${https_proxy:-unset}"
ls -la /persist /persist/lp1 2>&1 | sed 's/^/    /'
du -sh /persist/lp1/elan /persist/lp1/Lean_IM/.lake /persist/lp1/Lean_IM_5745ea9e/.lake /persist/opam /persist/sail-src 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'
echo "  which cmake: $(command -v cmake || echo ABSENT) $(cmake --version 2>&1 | head -1)"
echo "  which git: $(command -v git || echo ABSENT); which z3: $(command -v z3 || echo ABSENT); which make: $(command -v make || echo ABSENT); which ninja: $(command -v ninja || echo ABSENT)"
echo "  the sail in /persist/opam before this lane: $(/persist/opam/default/bin/sail --version 2>&1)"

step "SAMPLE: one request to each host this lane may need, LITERAL status or refusal (github for the clones and CLI11; opam.ocaml.org only if a dependency is missing)"
for u in https://github.com/riscv/sail-riscv.git/info/refs?service=git-upload-pack https://github.com/rems-project/sail.git/info/refs?service=git-upload-pack https://opam.ocaml.org/index.tar.gz ; do
  echo "  --- $u"
  curl -sS -I -m 40 -o /dev/null -w "    HTTP %{http_code} in %{time_total}s\n" "$u" 2>&1 | sed 's/^/  /'
done

step "git clone https://github.com/riscv/sail-riscv.git (full history) into $MODEL; checkout $MODEL_COMMIT (LITERAL commit line)"
if [ ! -d "$MODEL/.git" ]; then
  timed git clone https://github.com/riscv/sail-riscv.git "$MODEL" 2>&1 | tail -5
else
  echo "  clone already present; fetching"; git -C "$MODEL" fetch --all 2>&1 | tail -3
fi
cd "$MODEL"
git checkout --quiet $MODEL_COMMIT 2>&1 | tail -3
git log -1 --format='  %H %ci %s' 2>&1
echo "  branches containing it: $(git branch -r --contains $MODEL_COMMIT 2>/dev/null | head -3 | tr '\n' ' ')"
echo "  is 3243f93 (the image's model commit) in this clone's history: $(git cat-file -t 3243f93 2>&1)"
echo "  cmake/sail_required_version.txt at $MODEL_COMMIT: $(cat cmake/sail_required_version.txt 2>&1)"
echo "  compile-lean.yml at $MODEL_COMMIT, the sail-setup step (LITERAL):"
grep -n -B2 -A3 'sail-setup' .github/workflows/compile-lean.yml | head -24 | sed 's/^/    /'
echo "  handwritten_support/RiscvExtras.lean: $(ls -la handwritten_support/RiscvExtras.lean 2>&1)"
echo "  model/core/vmem_types.sail at this commit: $(ls model/core/vmem_types.sail 2>&1); is_sv32_mode in the model source: $(grep -rl 'is_sv32_mode' model 2>/dev/null | wc -l) files"

step "the diff of extensions/I and extensions/M between $MODEL_COMMIT and 3243f93 (brief §5's unverified row), LITERAL: --stat here, the whole diff saved under the artifact folder"
git diff --stat $MODEL_COMMIT 3243f93 -- model/extensions/I model/extensions/M 2>&1 | sed 's/^/    /'
git diff $MODEL_COMMIT 3243f93 -- model/extensions/I model/extensions/M > "$LP/lp1_diff_extensions_I_M_6266b40c_to_3243f93.diff" 2>&1
echo "  diff lines: $(wc -l < "$LP/lp1_diff_extensions_I_M_6266b40c_to_3243f93.diff"); saved as $LP/lp1_diff_extensions_I_M_6266b40c_to_3243f93.diff"
echo "  the execute clauses named in that diff (LITERAL grep of the diff for 'function clause execute'):"
grep -n 'function clause execute' "$LP/lp1_diff_extensions_I_M_6266b40c_to_3243f93.diff" | sed 's/^/    /'
echo "  mext_insts.sail and base_insts.sail themselves, changed lines: $(git diff --numstat $MODEL_COMMIT 3243f93 -- model/extensions/M/mext_insts.sail model/extensions/I/base_insts.sail 2>&1 | tr '\n' ' ')"

step "sail at $SAIL_COMMIT: git checkout in $SAILSRC (the clone lane 6 made), LITERAL commit line; then opam install . --deps-only --yes (the CI recipe), timed"
export OPAMROOT=/persist/opam
export OPAMYES=1
export OPAMSWITCH=default
export OCAMLFIND_CONF=/persist/opam/default/lib/findlib.conf
export PATH=/persist/opam/default/bin:$PATH
eval "$(opam env --root=/persist/opam --switch=default --set-root --set-switch 2>&1 | grep -v '^\[' )" || true
cd "$SAILSRC"
git checkout --quiet $SAIL_COMMIT 2>&1 | tail -3
git log -1 --format='  %H %ci %s' 2>&1
echo "  branches containing it: $(git branch -r --contains $SAIL_COMMIT 2>/dev/null | head -3 | tr '\n' ' ')"
echo "  the lean backend's pinned lean-sail rev and toolchain in the sail source at this commit (LITERAL grep):"
grep -rn 'lean-sail\|lean4:v4\|rev = ' src/sail_lean_backend/*.ml 2>/dev/null | head -8 | sed 's/^/    /'
timed opam install . --deps-only --yes 2>&1 | tail -30
rc=$?
if [ $rc -ne 0 ]; then
  echo "  first attempt rc=$rc; running opam update (fetches the index from opam.ocaml.org), then retrying"
  timed opam update --yes 2>&1 | tail -15
  timed opam install . --deps-only --yes 2>&1 | tail -60
  rc=$?
fi
echo "  deps-only rc=$rc"
peak

step "make install (dune build --release; dune install into /persist/opam/default), timed; then sail --version LITERAL"
cd "$SAILSRC"
timed make install 2>&1 | tail -20
echo "  make install rc=$?"
hash -r
echo "  which sail: $(command -v sail)"
echo "  sail --version: $(sail --version 2>&1)"
echo "  sail --dir: $(sail --dir 2>&1)"
for f in --lean --lean-output-dir --lean-force-output --lean-non-beq-type --lean-noncomputable --lean-noncomputable-function --lean-import-file --memo-z3 --memo-z3-path --strict-var --strict-bitvector --strict-exponentials; do
  if sail --help 2>&1 | grep -qE -- "^\s*$f\b"; then echo "    $f: accepted"; else echo "    $f: NOT IN --help"; fi
done
peak

step "cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DFIRST_PARTY_TESTS=OFF in $MODEL (configure only; fetches CLI11 from github), timed"
cd "$MODEL"
timed cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DFIRST_PARTY_TESTS=OFF > /work/cmake_configure.txt 2>&1
rc=$?
echo "  cmake rc=$rc; the last 25 lines (LITERAL):"
tail -25 /work/cmake_configure.txt | sed 's/^/    /'
if [ $rc -ne 0 ]; then echo "  FLAG: cmake configure failed; every line with 'error' (LITERAL):"; grep -n -i 'error' /work/cmake_configure.txt | head -20 | sed 's/^/    /'; fi
echo "  build/config: $(ls build/config 2>&1 | tr '\n' ' ')"
echo "  build/config/rv64d_v256_e64.json: $(ls -la build/config/rv64d_v256_e64.json 2>&1)"
peak

step "sail --list-files I_insts M_insts postlude main riscv.sail_project in $MODEL/model (LEAF names, checked before lane 11 emits)"
cd "$MODEL/model"
timed sail --list-files I_insts M_insts postlude main riscv.sail_project > /work/listfiles.txt 2>&1
echo "  rc above; files resolved: $(tr ' ' '\n' < /work/listfiles.txt | grep -c '\.sail$')"
tr ' ' '\n' < /work/listfiles.txt | grep -E 'base_insts.sail|mext_insts.sail|insts_end.sail|vmem_types.sail' | sed 's/^/    /'
echo "  the leaf modules of riscv.sail_project that carry I and M (LITERAL grep):"
grep -n 'I_insts\|M_insts\|^  *postlude\|^  *main' riscv.sail_project | head -12 | sed 's/^/    /'

step "the DIV clause in the model source at $MODEL_COMMIT (LITERAL), for the record beside log 274 §2.1"
awk '/function clause execute DIV\(/{p=1} p{print "    "$0} p&&/^}/{exit}' "$MODEL/model/extensions/M/mext_insts.sail"

step "sizes, the cgroup peak, and the persistent state left for lane 11 (which fetches nothing)"
du -sh "$MODEL" "$MODEL/build" "$SAILSRC" /persist/opam 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'
peak
echo "lane lp1_l10 done at $(date -u +%FT%TZ)"
