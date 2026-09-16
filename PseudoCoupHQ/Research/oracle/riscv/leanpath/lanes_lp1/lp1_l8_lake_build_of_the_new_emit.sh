#!/usr/bin/env bash
# lp1 lane 8 -- `lake build` of the NEW emit (brief §4, lane 8), as lane 1d
# did for the first: a working copy of the cache under /persist, the
# 4.29.0 toolchain the cache pins (already in /persist/lp1/elan from the
# github route), and the lean-sail library ALREADY fetched and built by
# lane 1d at rev v4 (commit 79b4d08) under /persist/lp1/Lean_IM/.lake --
# copied into the new project so that NOTHING IS FETCHED if the new emit
# pins the same rev. If the new emit pins a DIFFERENT lean-sail rev, a
# `lake update` is authorised in this lane (brief §4) and this log says
# so. Sample first (LeanIM.Defs, the module that failed under the first
# emit), then the whole library. Bounded by the instance (20g); wall time,
# the largest descendant's peak resident and the cgroup peak are printed;
# the count of modules built "of N". A build error is a FLAG: the first
# twelve error lines LITERAL, and the task stops at it.
# Before the build, the library's state and register machinery is
# printed LITERAL (the harness lanes unfold exactly these definitions).
set -u
export HOME=/work
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/venv/bin:$PATH
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_3243f93_sail_5745ea9e_I_insts_M_insts_postlude_main
OLDPROJ=/persist/lp1/Lean_IM
PROJ=/persist/lp1/Lean_IM_5745ea9e
total=9
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

step "the new cache and what it pins (LITERAL); the first project's pin beside it"
ls "$CACHE" | tr '\n' ' '; echo
echo "  new lakefile.toml:"; sed 's/^/    /' "$CACHE/lakefile.toml"
echo "  new lean-toolchain: $(cat $CACHE/lean-toolchain)"
echo "  first project's lake-manifest.json (the rev lane 1d fetched):"; sed 's/^/    /' "$OLDPROJ/lake-manifest.json"
NEWREV="$(grep -E '^rev' "$CACHE/lakefile.toml" | head -1 | sed 's/.*= *"//; s/".*//')"
OLDREV="$(grep -E '^rev' "$OLDPROJ/lakefile.toml" | head -1 | sed 's/.*= *"//; s/".*//')"
echo "  lean-sail rev pinned: new='$NEWREV' first='$OLDREV'"

step "the working copy of the new cache (the cache itself is never written), with the library copied in if the rev is the same"
if [ ! -d "$PROJ/LeanIM" ]; then mkdir -p "$PROJ"; cp -r "$CACHE"/. "$PROJ"/; rm -f "$PROJ/emit_lane.log"; fi
if [ "$NEWREV" = "$OLDREV" ] && [ -d "$OLDPROJ/.lake/packages/Sail" ]; then
  if [ ! -d "$PROJ/.lake/packages/Sail" ]; then mkdir -p "$PROJ/.lake"; cp -a "$OLDPROJ/.lake/packages" "$PROJ/.lake/"; fi
  cp "$OLDPROJ/lake-manifest.json" "$PROJ/lake-manifest.json"
  unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
  echo "  same rev: the built lean-sail (commit $(git -C $PROJ/.lake/packages/Sail rev-parse HEAD 2>&1)) copied in; THIS LANE FETCHES NOTHING (proxy variables unset)"
else
  echo "  DIFFERENT rev: the new emit pins lean-sail rev '$NEWREV' (the first pinned '$OLDREV'); this lane FETCHES it with lake update from github.com (authorised by brief §4 for this lane, and said so here); http_proxy=${http_proxy:-unset}"
  cd "$PROJ"
  timed lake update 2>&1 | tail -20
  echo "  --- lake-manifest.json after the fetch (LITERAL) ---"; sed 's/^/    /' lake-manifest.json
  echo "  --- the library's own commit and toolchain (LITERAL) ---"
  git -C .lake/packages/Sail log -1 --format='  %H %ci %s' 2>&1; echo "    lean-toolchain: $(cat .lake/packages/Sail/lean-toolchain 2>&1)"
  ls .lake/packages/Sail/Sail 2>/dev/null | tr '\n' ' '; echo
fi
cd "$PROJ"
echo "  lean: $(lean --version 2>&1)"; echo "  lake: $(lake --version 2>&1)"
du -sh "$PROJ" 2>&1 | sed 's/^/    /'

step "the library's state and register machinery, LITERAL (Sail.lean: SequentialState, PreSailM, readReg, writeReg, and any initial/default state)"
SL=.lake/packages/Sail/Sail
grep -n 'structure SequentialState\|abbrev PreSailM\|def readReg\|def writeReg\|inductive Error\|Inhabited (SequentialState\|def initial\|initialState\|def get_slice_int\|def toNatInt\|def extractLsb\|def updateSubrange\|def zeroExtend\|def signExtend' $SL/*.lean 2>&1 | head -30 | sed 's/^/    /'
for f in $SL/Sail.lean; do
  s=$(grep -n 'structure SequentialState' $f | head -1 | cut -d: -f1)
  if [ -n "$s" ]; then a=$((s-4)); b=$((s+95)); echo "  --- $f lines $a-$b ---"; sed -n "${a},${b}p" $f | sed 's/^/    /'; fi
  s=$(grep -n '^def toNatInt' $f | head -1 | cut -d: -f1)
  if [ -n "$s" ]; then a=$((s-2)); b=$((s+30)); echo "  --- $f lines $a-$b (BitVec helpers) ---"; sed -n "${a},${b}p" $f | sed 's/^/    /'; fi
  s=$(grep -n '^def get_slice_int' $f | head -1 | cut -d: -f1)
  if [ -n "$s" ]; then a=$((s-2)); b=$((s+8)); echo "  --- $f lines $a-$b (get_slice_int) ---"; sed -n "${a},${b}p" $f | sed 's/^/    /'; fi
done
echo "  --- the Int/BitVec notations (+i, *i, ≥b, ...) ---"
grep -n 'infixl\|notation' $SL/Sail.lean | head -40 | sed 's/^/    /'
echo "  --- the emitted model's initial state / main / SailM lines ---"
grep -n 'SailM\b.*:=\|initial\|def main\|Inhabited (SequentialState\|instance : Inhabited' LeanIM.lean LeanIM/Defs.lean 2>/dev/null | head -12 | sed 's/^/    /'
grep -n 'def initialize_registers' -A 3 LeanIM.lean | head -8 | sed 's/^/    /'
echo "  --- simp_sail attribute (the library's own simp set) ---"
grep -rn 'simp_sail' $SL/*.lean | head -5 | sed 's/^/    /'
grep -c 'simp_sail' LeanIM/*.lean | grep -v ':0' | head -5 | sed 's/^/    /'

step "lake build Sail (the library; expected up to date), timed"
timed lake build Sail 2>&1 | tail -8
peak

step "SAMPLE: lake build LeanIM.Defs (the module that failed under the first emit), timed"
timed lake build LeanIM.Defs > /work/defs_build.txt 2>&1
rc=$?
tail -12 /work/defs_build.txt | sed 's/^/    /'
echo "  LeanIM.Defs rc=$rc; error lines: $(grep -c 'error' /work/defs_build.txt)"
if [ $rc -ne 0 ]; then echo "  FLAG: the first twelve error lines, LITERAL:"; grep -n 'error' /work/defs_build.txt | head -12 | sed 's/^/    /'; fi
peak

step "lake build LeanIM.InstsEnd (the module the proofs import, with everything it imports), timed, -j 4"
timed lake build -j 4 LeanIM.InstsEnd > /work/instsend_build.txt 2>&1
rc=$?
tail -12 /work/instsend_build.txt | sed 's/^/    /'
echo "  LeanIM.InstsEnd rc=$rc; error lines: $(grep -c 'error' /work/instsend_build.txt)"
if [ $rc -ne 0 ]; then echo "  FLAG: the first twelve error lines, LITERAL:"; grep -n 'error' /work/instsend_build.txt | head -12 | sed 's/^/    /'; fi
echo "  oleans so far: $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l)"
peak

step "lake build (the whole library, default target), timed, -j 4"
timed lake build -j 4 > /work/all_build.txt 2>&1
rc=$?
tail -12 /work/all_build.txt | sed 's/^/    /'
echo "  whole build rc=$rc; error lines: $(grep -c 'error' /work/all_build.txt); warning lines: $(grep -c 'warning' /work/all_build.txt)"
if [ $rc -ne 0 ]; then echo "  FLAG: the first twelve error lines, LITERAL:"; grep -n 'error' /work/all_build.txt | head -12 | sed 's/^/    /'; fi
peak

step "the count of modules built, of N"
NMOD=$(( $(ls LeanIM/*.lean | wc -l) + 1 ))
NOLE=$(( $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l) + $(ls .lake/build/lib/lean/LeanIM.olean 2>/dev/null | wc -l) ))
echo "  modules built: $NOLE of $NMOD (LeanIM/*.lean plus LeanIM.lean)"
du -sh "$PROJ/.lake" "$PROJ" 2>&1 | sed 's/^/    /'
df -h /persist | tail -1 | sed 's/^/    /'

step "a one-file smoke test of the built model: import it, unfold execute on a symbolic state, timed (the harness's first move)"
mkdir -p /work/smoke
cat > /work/smoke/Smoke.lean <<'EOF'
import LeanIM
open Sail LeanIM LeanIM.Functions
set_option maxHeartbeats 2000000
#check @execute
#check @encdec_backwards
#check @rX_bits
#check @wX_bits
#check @PreSail.readReg
#check @PreSail.writeReg
#print PreSail.readReg
#print PreSail.writeReg
#print SailM
#check (default : SequentialState RegisterType trivialChoiceSource)
EOF
cd "$PROJ"
timed lake env lean /work/smoke/Smoke.lean 2>&1 | head -60 | sed 's/^/    /'
peak
echo "lane lp1_l8 done at $(date -u +%FT%TZ)"
