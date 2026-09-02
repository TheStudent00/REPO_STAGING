#!/usr/bin/env bash
# cg_cov_l3 — compile the probe with the coverage-instrumented compiler,
# collect GOCOVERDIR profiles, render textfmt.
set -u
OUT=/out/cg_cov_l3.txt
exec > >(tee "$OUT") 2>&1
say(){ echo "=== $* ==="; }

SRC=/persist/gosrc
export GOROOT="$SRC"; export PATH="$SRC/bin:$PATH"
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache
GO="$SRC/bin/go"

P=/work/probe; rm -rf $P; mkdir -p $P; cd $P
cat > go.mod <<'EOF'
module probe

go 1.28
EOF
cat > probe.go <<'EOF'
package main

//go:noinline
func af(a, b int32) int32 { return a - b }

func main() {
	println(af(7, 3))
}
EOF
say probe
cat probe.go
"$GO" version

say "capture real compile command line"
"$GO" build -a -work -x -o /work/probe.bin . > /work/x.stdout 2> /work/x.log
echo "build_exit=$?"
WORKDIR=$(grep -m1 '^WORK=' /work/x.log | cut -d= -f2)
echo "WORKDIR=$WORKDIR"
CMDLINE=$(grep -F "$GOROOT/pkg/tool/linux_amd64/compile" /work/x.log | grep -F 'probe.go' | tail -1)
echo "CMDLINE:"; echo "$CMDLINE"
[ -z "$CMDLINE" ] && { echo FATAL_NO_CMDLINE; tail -40 /work/x.log; exit 90; }
# the dir the go command cd'd into before that compile (the probe dir)
grep -n '^cd ' /work/x.log | tail -3

say "re-run that compile with the instrumented binary"
export GOCOVERDIR=/work/covdata
rm -rf "$GOCOVERDIR"; mkdir -p "$GOCOVERDIR"
NEW=$(printf '%s' "$CMDLINE" | sed "s#$GOROOT/pkg/tool/linux_amd64/compile #/persist/compile_cov #")
echo "NEW:"; echo "$NEW"
cd $P
env WORK="$WORKDIR" GOCOVERDIR="$GOCOVERDIR" bash -c "$NEW"
echo "instrumented_compile_exit=$?"
ls -l "$GOCOVERDIR"

say "textfmt"
"$GO" tool covdata percent -i="$GOCOVERDIR" | tail -5
"$GO" tool covdata textfmt -i="$GOCOVERDIR" -o /work/coverage_full.txt
echo "textfmt_exit=$?"
TOTAL=$(($(wc -l < /work/coverage_full.txt) - 1))
awk 'NR>1 && $NF+0>0' /work/coverage_full.txt > /work/cov_visited.body
VIS=$(wc -l < /work/cov_visited.body)
{ head -1 /work/coverage_full.txt; cat /work/cov_visited.body; } > /out/coverage_go.txt
echo "total_rows=$TOTAL visited_rows=$VIS"

say "target dirs"
for d in ssagen ssa abi amd64; do
  n=$(grep -c "cmd/compile/internal/$d/" /work/cov_visited.body)
  echo "visited_in_$d=$n"
done
grep -E "cmd/compile/internal/(ssagen|ssa|abi|amd64)/" /work/cov_visited.body > /work/target.txt
echo "visited_in_four_dirs_total=$(wc -l < /work/target.txt)"
say "10 samples"
shuf -n 10 /work/target.txt 2>/dev/null || head -10 /work/target.txt

say disk
du -sh /work/* 2>/dev/null; df -h /work /persist | sed -n 1,4p
cp /out/coverage_go.txt /out/cg_coverage_go.txt
echo DONE_OK
