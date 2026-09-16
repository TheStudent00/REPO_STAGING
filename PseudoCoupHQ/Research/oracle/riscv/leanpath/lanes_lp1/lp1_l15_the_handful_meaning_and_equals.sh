#!/usr/bin/env bash
# lp1 lane 15 -- brief §2 lanes 3 and 4 over the third cache, the POPULATION
# after lane 13c's sample: the ten carved units of rv1 (log 258; their
# bodies and words from Research/oracle/riscv/carved.json, their sources
# from units.json) plus `mulh` on c twice (the plain `(__int128)a * b >> 64`
# compiled in this lane at ship flags, and rv6's rendered emulation source
# of the same cell), each through the harness: decode by the model's own
# decoder (one word and its constructor printed LITERAL), compose in Lean
# (the walk of Sail's own execute), the answering register's expression
# LITERAL, then `equals` against every no-immediate definition instance in
# key order, in the plan's stages (rfl / grind / widen+bv_decide /
# bv_decide, 30 s budget), stopping at the first proof. Every refusal is a
# row with the construct named by the run. Seconds per stage and the
# driver's peak resident are printed. THIS LANE FETCHES NOTHING. Memory
# bound 6 GB on the driver (ABORT_MEMORY_LP1); lean processes bounded by
# the instance. One process, no pool.
set -u
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
export HOME=/work
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/venv/bin:/opt/opam/default/bin:$PATH
export GOCACHE=/work/lp1gocache GOPATH=/work/lp1gopath
mkdir -p "$GOCACHE" "$GOPATH"
P=PseudoCoupHQ
LP=$P/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules
PROJ=/persist/lp1/Lean_IM_6266b40c_all
WORK=/work/lp1handful
REC=$LP/lp1_harness_all
mkdir -p "$WORK" "$REC/handful_lean"
total=4
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

step "this lane fetches nothing: http_proxy=${http_proxy:-unset}; the harness in place (LITERAL)"
ls -la $PROJ/leanpath_src | sed 's/^/    /'
ls $PROJ/.lake/build/lib/lean/ | grep -i leanpath | sed 's/^/    /'
echo "  base mode from the harness record: $(python3 -c "import json;print(json.load(open('$REC/lp1_harness.json')).get('base_mode'))")"

step "the handful: strip on the definition instances, then every unit through decode, meaning, equals"
cd $LP
timed python3 -m leanpath handful "$CACHE" "$PROJ" "$WORK" "$REC/lp1_handful.json" 99
echo "  handful rc=$?"
peak

step "the Lean files of this run, kept under the artifact folder (the theorem files are the certificates)"
cp "$WORK/"*.lean "$REC/handful_lean/" 2>/dev/null
echo "  $(ls $REC/handful_lean | wc -l) Lean files kept; $(grep -l 'leanpath_stage' $REC/handful_lean/*.lean 2>/dev/null | wc -l) of them are equals theorems"
du -sh "$REC/handful_lean" | sed 's/^/    /'

step "the cgroup peak"
peak
echo "lane lp1_l15 done at $(date -u +%FT%TZ)"
