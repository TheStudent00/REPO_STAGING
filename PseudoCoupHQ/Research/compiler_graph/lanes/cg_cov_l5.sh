#!/usr/bin/env bash
# cg_cov_l5 — l3 showed `go build -cover` instruments only the main package
# (4 blocks). Rebuild with -coverpkg=cmd/compile/... so every internal
# package of the compiler is instrumented, then redo the probe compile.
set -u
OUT=/out/cg_cov_l5.txt
exec > >(tee "$OUT") 2>&1
say(){ echo "=== $* ==="; }

SRC=/persist/gosrc
export GOROOT="$SRC"; export PATH="$SRC/bin:$PATH"
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache
GO="$SRC/bin/go"

say "build -cover -covermode=count -coverpkg=cmd/compile/..."
cd "$SRC/src/cmd" || exit 93
set -x
"$GO" build -cover -covermode=count -coverpkg=cmd/compile/... -o /persist/compile_cov cmd/compile
A=$?
set +x
echo "build_cover_exit=$A"; [ "$A" -ne 0 ] && exit 94
ls -l /persist/compile_cov

P=/work/probe; rm -rf $P; mkdir -p $P; cd $P
printf 'module probe\n\ngo 1.28\n' > go.mod
cat > probe.go <<'EOF'
package main

//go:noinline
func af(a, b int32) int32 { return a - b }

func main() {
	println(af(7, 3))
}
EOF
say "capture real compile command line"
"$GO" build -a -work -x -o /work/probe.bin . > /work/x.stdout 2> /work/x.log
echo "build_exit=$?"
WORKDIR=$(grep -m1 '^WORK=' /work/x.log | cut -d= -f2)
CMDLINE=$(grep -F "$GOROOT/pkg/tool/linux_amd64/compile" /work/x.log | grep -F 'probe.go' | tail -1)
echo "WORKDIR=$WORKDIR"; echo "$CMDLINE"
[ -z "$CMDLINE" ] && { echo FATAL_NO_CMDLINE; exit 90; }

say "re-run with instrumented compiler"
export GOCOVERDIR=/work/covdata; rm -rf "$GOCOVERDIR"; mkdir -p "$GOCOVERDIR"
NEW=$(printf '%s' "$CMDLINE" | sed "s#$GOROOT/pkg/tool/linux_amd64/compile #/persist/compile_cov #")
cd $P
env WORK="$WORKDIR" GOCOVERDIR="$GOCOVERDIR" bash -c "$NEW"
echo "instrumented_compile_exit=$?"
ls -l "$GOCOVERDIR"
ls -l $P

say "textfmt"
"$GO" tool covdata percent -i="$GOCOVERDIR" | tail -40
"$GO" tool covdata textfmt -i="$GOCOVERDIR" -o /work/coverage_full.txt
echo "textfmt_exit=$?"
TOTAL=$(($(wc -l < /work/coverage_full.txt) - 1))
awk 'NR>1 && $NF+0>0' /work/coverage_full.txt > /work/cov_visited.body
VIS=$(wc -l < /work/cov_visited.body)
{ head -1 /work/coverage_full.txt; cat /work/cov_visited.body; } > /out/coverage_go.txt
echo "total_rows=$TOTAL"
echo "visited_rows=$VIS"

say "target dirs"
for d in ssagen ssa abi amd64; do
  echo "visited_in_$d=$(grep -c "cmd/compile/internal/$d/" /work/cov_visited.body)"
done
grep -E "cmd/compile/internal/(ssagen|ssa|abi|amd64)/" /work/cov_visited.body > /work/target.txt
echo "visited_in_four_dirs_total=$(wc -l < /work/target.txt)"
say "10 samples"
shuf -n 10 /work/target.txt
say "distinct visited files, top 20 by row count"
awk -F: '{print $1}' /work/cov_visited.body | sort | uniq -c | sort -rn | head -20
say disk
du -sh /persist/gosrc /persist/gocache /persist/compile_cov; df -h /work /persist|sed -n 1,4p
echo DONE_OK
