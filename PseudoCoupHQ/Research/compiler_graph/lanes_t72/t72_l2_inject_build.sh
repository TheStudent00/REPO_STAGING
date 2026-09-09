#!/usr/bin/env bash
# t72 lane 2 — inject the diary hook into EVERY function body of the go
# lowering region, rebuild cmd/compile, and smoke-test ONE probe so the
# diary's size per compile is measured before 590 of them are run.
set -euo pipefail
REPO=/projects/PseudoCoupHQ/Research/compiler_graph
SRC=/persist/gosrc
export GOROOT="$SRC" PATH="$SRC/bin:$PATH"
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache

echo "[1/6] restore every touched file from the READ-ONLY tree"
python3 - <<'PY'
import json, os, shutil
targets = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/t72/diary_targets_all.json'))
files = sorted({t['file'] for t in targets})
files += ['src/cmd/compile/internal/ssagen/ssa.go',
          'src/cmd/compile/internal/gc/compile.go',
          'src/cmd/compile/internal/base/base.go']
n = 0
for rel in sorted(set(files)):
    src = os.path.join('/sources/golang_src', rel)
    dst = os.path.join('/persist/gosrc', rel)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        n += 1
print('restored %d files' % n)
PY
rm -rf "$SRC/src/cmd/compile/internal/diary"

echo "[2/6] inject"
python3 "$REPO/t72/inject_diary_region.py" \
    --targets "$REPO/t72/diary_targets_all.json" \
    --src "$SRC/src" \
    --report "$REPO/t72/inject_report.json" | tail -12

echo "[3/6] build cmd/compile"
T=$(date +%s)
cd "$SRC/src/cmd"
"$SRC/bin/go" build -o /persist/compile_diary_all cmd/compile 2> /persist/build_diary_all.log || {
    echo "BUILD FAILED — first 60 lines:"; head -60 /persist/build_diary_all.log; exit 3; }
echo "  build seconds: $(( $(date +%s) - T ))"
ls -la /persist/compile_diary_all

echo "[4/6] capture the real tool command line (go build -a -work -x)"
rm -rf /work/probe && mkdir -p /work/probe
cd /work/probe
printf 'module probe\n\ngo 1.28\n' > go.mod
cat > probe.go <<'GO'
package main

//go:noinline
func op_smoke(a int32) int32 {
	return +a
}

var ga int32
var sink interface{}

func main() {
	sink = op_smoke(ga)
	_ = sink
}
GO
"$SRC/bin/go" build -a -work -x -o /work/probe.bin . > /work/x.stdout 2> /work/x.log
WORKDIR=$(grep -m1 '^WORK=' /work/x.log | cut -d= -f2)
echo "  WORK=$WORKDIR"
grep -m1 "compile -o .*_pkg_.a" /work/x.log | tail -1 > /work/toolline.raw || true
# the LAST compile line is the main package's
grep "compile " /work/x.log | grep -- "-p main" | tail -1 > /work/toolline.raw
echo "  captured tool line:"; cat /work/toolline.raw
cp /work/toolline.raw "$REPO/t72/toolline_raw.txt"
mkdir -p /persist/probecfg
cp "$WORKDIR/b001/importcfg" /persist/probecfg/importcfg
cp /work/toolline.raw /persist/probecfg/toolline.raw
echo "  importcfg lines: $(wc -l < /persist/probecfg/importcfg)"

echo "[5/6] smoke: replay that line with the diary compiler"
mkdir -p /work/out
rm -f /work/smoke.diary
cd /work/probe
python3 - <<'PY'
import os, shlex, subprocess, sys
line = open('/work/toolline.raw').read().strip()
parts = shlex.split(line)
# substitute the compiler binary and the output path; keep every other flag
parts[0] = '/persist/compile_diary_all'
for i, p in enumerate(parts):
    if p == '-o':
        parts[i + 1] = '/work/out/_pkg_.a'
env = dict(os.environ, COMPILER_DIARY='/work/smoke.diary')
print('replaying with %d args' % len(parts))
r = subprocess.run(parts, env=env, cwd='/work/probe',
                   capture_output=True, text=True)
print('exit', r.returncode)
if r.returncode != 0:
    print(r.stdout[-3000:]); print(r.stderr[-3000:]); sys.exit(4)
open('/work/toolline.parts', 'w').write('\n'.join(parts))
PY
echo "  diary size:  $(stat -c %s /work/smoke.diary) bytes"
echo "  diary lines: $(wc -l < /work/smoke.diary)"
echo "  distinct node ids: $(cut -f3 /work/smoke.diary | sort -u | wc -l)"
echo "  first 12 lines, LITERAL:"
head -12 /work/smoke.diary
echo "  gzip size: $(gzip -c /work/smoke.diary | wc -c) bytes"
cp /work/smoke.diary "$REPO/t72/smoke.diary"

echo "[6/6] disk"
du -sh /persist/gosrc /persist/gocache /persist/compile_diary_all
df -h /persist | tail -1
echo "DONE t72_l2"
