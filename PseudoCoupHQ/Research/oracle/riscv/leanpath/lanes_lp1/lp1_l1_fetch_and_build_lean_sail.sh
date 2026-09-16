#!/usr/bin/env bash
# lp1 lane 1 -- THE ONE LANE WITH THE NETWORK (brief section 2, lane 1).
# elan installs the Lean toolchain the cached emit pins (lean-toolchain:
# leanprover/lean4:v4.29.0); `lake update` in a working copy of the cached
# project fetches `lean-sail` rev v4 from GitHub; `lake build` builds the
# Sail library and then the model's Lean once, into /persist, where every
# later lane finds it. Every host reached is named; a host the proxy
# refuses is a FLAG with the literal refusal, never worked around.
# Sample first: one small module (LeanIM.Defs), then the module the proofs
# import (LeanIM.InstsEnd), then the whole library. Wall time and the
# peak resident of the largest process are printed per step; the cgroup's
# own memory.peak is printed beside them.
set -u
export PATH=/opt/elan/bin:/opt/opam/default/bin:$PATH
CACHE=PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_3243f93_I_insts_M_insts_postlude_main
PERSIST=/persist/lp1
PROJ=$PERSIST/Lean_IM
export ELAN_HOME=$PERSIST/elan
export HOME=/work
total=9
i=1

step() { echo "[$i/$total] $1"; i=$((i+1)); echo "  at $(date -u +%FT%TZ)"; }
peak() { echo "  cgroup memory.peak: $(cat /sys/fs/cgroup/memory.peak 2>/dev/null || echo unreadable) bytes; memory.current: $(cat /sys/fs/cgroup/memory.current 2>/dev/null || echo unreadable)"; }
# run a command under python so the largest descendant's peak resident is read
# from resource.getrusage(RUSAGE_CHILDREN); /usr/bin/time is absent in the image
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

step "the proxy and the hosts this lane will reach (named before any fetch)"
echo "  http_proxy=${http_proxy:-unset} https_proxy=${https_proxy:-unset}"
echo "  hosts: github.com (lean-sail, the toolchain release), objects.githubusercontent.com / release.lean-lang.org (the toolchain archive, wherever elan redirects)"
mkdir -p "$PERSIST"
df -h /persist | tail -1
peak

step "elan: copy the image's elan home to /persist and install the pinned toolchain"
if [ ! -d "$ELAN_HOME" ]; then cp -a /opt/elan "$ELAN_HOME"; fi
export PATH=$ELAN_HOME/bin:$PATH
elan --version
echo "  toolchain the cache pins: $(cat $CACHE/lean-toolchain)"
timed elan toolchain install "$(cat $CACHE/lean-toolchain)" 2>&1 | tail -20
elan toolchain list
peak

step "the working copy of the cached project (the cache itself is never written)"
if [ ! -d "$PROJ" ]; then mkdir -p "$PROJ"; cp -r "$CACHE"/. "$PROJ"/; fi
ls -la "$PROJ" | head -20
cd "$PROJ"
echo "  lean --version (through elan, from lean-toolchain):"; lean --version
lake --version

step "lake update: fetch lean-sail rev v4 (the require in lakefile.toml)"
timed lake update 2>&1 | tail -30
echo "  --- lake-manifest.json after the fetch ---"; cat lake-manifest.json
echo "  --- the library's own commit ---"; git -C .lake/packages/Sail log -1 --format='%H %ci %s' 2>&1
ls .lake/packages/Sail | head; ls .lake/packages/Sail/Sail 2>/dev/null | head -40
peak

step "the library's state and register machinery, LITERAL (what the harness will unfold)"
grep -rn 'PreSailM\b\|structure SequentialState\|def readReg\|def writeReg\|def get_slice_int\|def PreSailM\|abbrev PreSailM' .lake/packages/Sail/Sail/*.lean | head -40
for f in .lake/packages/Sail/Sail/State.lean .lake/packages/Sail/Sail/Sail.lean; do
  if [ -f "$f" ]; then echo "  --- $f (first 220 lines) ---"; sed -n '1,220p' "$f"; fi
done
grep -rn 'def get_slice_int\|def Sail.BitVec.extractLsb\|def extractLsb\|def toNatInt\|infix.*≥b\|notation.*≥b\|infix.*+i\|def toInt' .lake/packages/Sail/Sail/*.lean | head -20

step "lake build Sail (the library alone), timed"
timed lake build Sail 2>&1 | tail -15
peak

step "sample: lake build LeanIM.Defs (one module), timed"
timed lake build LeanIM.Defs 2>&1 | tail -15
peak

step "lake build LeanIM.InstsEnd (the module the proofs import, with everything it imports), timed, -j 4"
timed lake build -j 4 LeanIM.InstsEnd 2>&1 | tail -40
peak
ls -la .lake/build/lib/lean/LeanIM/ 2>/dev/null | wc -l

step "lake build (the whole library, default target), timed, -j 4"
timed lake build -j 4 2>&1 | tail -40
peak
echo "  oleans built: $(ls .lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l) of $(ls $PROJ/LeanIM/*.lean | wc -l) modules"
du -sh "$PROJ/.lake" "$ELAN_HOME" 2>/dev/null
df -h /persist | tail -1
echo "lane lp1_l1 done at $(date -u +%FT%TZ)"
