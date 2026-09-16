#!/usr/bin/env bash
# lp1 lane 13 -- THIRD launch: the built model stands (lane 12), so the
# Lean harness is built on it and SAMPLED before the handful runs whole:
#   [2] `python3 -m leanpath harness`: Leanpath.lean is written from its
#       template with every def/value-abbrev of the emitted tree as an
#       unfold lemma (a text LISTING of names; a name Lean refuses as a
#       simp lemma is dropped and printed LITERAL), built as a lake lib
#       of the WORKING COPY /persist/lp1/Lean_IM_6266b40c (the cache is
#       never written); then the model's own `sail_model_init` and
#       `reset` are run in Lean on the empty state, under the hypothesis
#       that the support library's three `SailM Unit` axioms leave the
#       state as it is (printed LITERAL), and the state is recorded as S0
#       (LeanpathBase); then a few registers of S0 are peeked, LITERAL.
#   [3] `python3 -m leanpath handful ... 1`: strip on every no-immediate
#       definition instance (the model's own execute on the instance),
#       then ONE unit of rv1 (go/op_312) and the two mulh-on-c units:
#       decode, meaning, equals in stages -- the sample; the population
#       is lane 14.
# THIS LANE FETCHES NOTHING (proxy variables unset). Memory bound 6 GB on
# the driver (ABORT_MEMORY_LP1); each lean process is bounded by the
# instance (20g). One process, no pool, no clock in the driver.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/venv/bin:/opt/opam/default/bin:$PATH
export GOCACHE=/work/lp1gocache GOPATH=/work/lp1gopath
mkdir -p "$GOCACHE" "$GOPATH"
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_I_insts_M_insts_postlude_main
PROJ=/persist/lp1/Lean_IM_6266b40c
WORK=/work/lp1h
REC=$LP/lp1_harness
mkdir -p "$WORK" "$REC"
total=5
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

step "this lane fetches nothing: http_proxy=${http_proxy:-unset}; the tools, LITERAL"
echo "  lean: $(lean --version 2>&1)"; echo "  lake: $(lake --version 2>&1)"
echo "  python3: $(python3 --version 2>&1) at $(command -v python3)"
echo "  clang: $(clang --version 2>&1 | head -1); llvm-objdump: $(command -v llvm-objdump); rustc: $(rustc --version 2>&1); go: $(go version 2>&1)"
echo "  the working copy: $PROJ ($(ls $PROJ/.lake/build/lib/lean/LeanIM/*.olean 2>/dev/null | wc -l) oleans)"
echo "  the module: $LP/leanpath ($(ls $LP/leanpath/*.py | wc -l) files, $(cat $LP/leanpath/*.py | wc -l) lines; lean/ $(ls $LP/leanpath/lean | tr '\n' ' '))"

step "the harness: names listed, Leanpath built, the base state S0 from the model's own init and reset, LeanpathBase built, a few registers peeked (LITERAL)"
cd $LP
timed python3 -m leanpath harness "$CACHE" "$PROJ" "$REC/lp1_harness.json"
echo "  harness rc=$?"
peak

step "SAMPLE: strip on the no-immediate definition instances, then ONE rv1 unit and the two mulh-on-c units through decode, meaning, equals"
cd $LP
timed python3 -m leanpath handful "$CACHE" "$PROJ" "$WORK" "$REC/lp1_handful_sample.json" 1
echo "  handful sample rc=$?"
peak

step "the harness sources and the sample's Lean files, kept under the artifact folder (LITERAL products)"
mkdir -p "$REC/leanpath_src" "$REC/sample_lean"
cp "$PROJ/leanpath_src/"*.lean "$REC/leanpath_src/" 2>/dev/null
cp "$PROJ/leanpath_work/"* "$REC/leanpath_src/" 2>/dev/null
cp "$WORK/"*.lean "$REC/sample_lean/" 2>/dev/null
echo "  $(ls $REC/leanpath_src | wc -l) harness files, $(ls $REC/sample_lean 2>/dev/null | wc -l) sample Lean files kept"
ls -la "$REC" "$REC/leanpath_src" | sed 's/^/    /'
echo "  Leanpath.lean: $(wc -l < $REC/leanpath_src/Leanpath.lean) lines; LeanpathBase.lean: $(wc -l < $REC/leanpath_src/LeanpathBase.lean 2>/dev/null) lines ($(wc -c < $REC/leanpath_src/LeanpathBase.lean 2>/dev/null) bytes)"

step "sizes and the cgroup peak"
du -sh "$PROJ/.lake" "$WORK" "$REC" 2>&1 | sed 's/^/    /'
df -h /work /persist | tail -2 | sed 's/^/    /'
peak
echo "lane lp1_l13 done at $(date -u +%FT%TZ)"
