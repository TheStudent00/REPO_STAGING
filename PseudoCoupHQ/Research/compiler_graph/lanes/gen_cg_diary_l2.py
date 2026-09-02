#!/usr/bin/env python3
"""Generate lanes/cg_diary_l2.sh with the instrumenter and targets embedded.

The repository is not mounted inside the Airlock container, so the lane has
to carry its own copies.  Generating the lane from the repo files keeps the
two in step.
"""

import os

REPO = "/sessions/fervent-trusting-darwin/mnt/Programming/PseudoCoupHQ/Research/compiler_graph"

handle = open(os.path.join(REPO, "inject_diary.py"), encoding="utf-8")
injector = handle.read()
handle.close()

handle = open(os.path.join(REPO, "diary_targets.json"), encoding="utf-8")
targets = handle.read()
handle.close()

HEAD = r'''#!/usr/bin/env bash
# cg_diary_l2 — THE DIARY, lap two: every event carries a SUBJECT.
#
# Lap one's diary said WHICH SPOT of the compiler ran.  It did not say WHOSE
# code the compiler was working on.  This lane adds that column: five
# subject spots, where the name of the function under analysis IS reachable,
# open a subject for their goroutine; every instrumented spot that runs
# inside one stamps its event with it; everything else stamps `-`.
set -u
OUT=/out/cg_diary_l2.txt
exec > >(tee "$OUT") 2>&1
say(){ echo "=== $* ==="; }

SRC=/persist/gosrc
export GOROOT="$SRC"; export PATH="$SRC/bin:$PATH"
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache
GO="$SRC/bin/go"

say recon
date -u +%Y-%m-%dT%H:%M:%SZ
python3 -c 'import sys; print("python", sys.version.split()[0])' || { echo FATAL_NO_PYTHON; exit 80; }
"$GO" version || { echo FATAL_NO_TOOLCHAIN; exit 81; }

say "restore the seven touched files from the read-only vendored tree"
for f in cmd/compile/internal/abi/abiutils.go \
         cmd/compile/internal/amd64/galign.go \
         cmd/compile/internal/amd64/ggen.go \
         cmd/compile/internal/amd64/ssa.go \
         cmd/compile/internal/ssagen/ssa.go \
         cmd/compile/internal/ssa/debug.go \
         cmd/compile/internal/gc/compile.go ; do
  cp -f "/sources/golang_src/src/$f" "$SRC/src/$f" || exit 82
  echo "restored $f"
done
rm -rf "$SRC/src/cmd/compile/internal/diary"

rm -rf /work/diary2; mkdir -p /work/diary2

say 'write the instrumenter and its target list into /work/diary2'
cat > /work/diary2/inject_diary.py <<'INJECT_DIARY_PY_EOF'
'''

MID = r'''INJECT_DIARY_PY_EOF
cat > /work/diary2/diary_targets.json <<'DIARY_TARGETS_JSON_EOF'
'''

TAIL = r'''DIARY_TARGETS_JSON_EOF
wc -l /work/diary2/inject_diary.py /work/diary2/diary_targets.json

say "inject"
cd /work/diary2
python3 inject_diary.py inject --targets diary_targets.json --src "$SRC/src"
INJ=$?
echo "inject_exit=$INJ"
[ "$INJ" -ne 0 ] && exit 83
grep -c 'diary.Note(' "$SRC/src/cmd/compile/internal/abi/abiutils.go"
grep -n 'diary.Enter(' "$SRC/src/cmd/compile/internal/ssagen/ssa.go" \
                       "$SRC/src/cmd/compile/internal/ssa/debug.go" \
                       "$SRC/src/cmd/compile/internal/gc/compile.go"

say "rebuild cmd/compile"
cd "$SRC/src/cmd" || exit 84
set -x
"$GO" build -o /persist/compile_diary2 cmd/compile
B=$?
set +x
echo "build_exit=$B"
if [ "$B" -ne 0 ]; then echo FATAL_BUILD_FAILED; exit 85; fi
ls -l /persist/compile_diary2

say "probe"
P=/work/probe2; rm -rf $P; mkdir -p $P; cd $P
printf 'module probe\n\ngo 1.28\n' > go.mod
cat > probe.go <<'EOF'
package main

//go:noinline
func af(a, b int32) int32 { return a - b }

func main() {
	println(af(7, 3))
}
EOF

say "capture the real compile command line"
"$GO" build -a -work -x -o /work/probe2.bin . > /work/x2.stdout 2> /work/x2.log
echo "build_exit=$?"
WORKDIR=$(grep -m1 '^WORK=' /work/x2.log | cut -d= -f2)
CMDLINE=$(grep -F "$GOROOT/pkg/tool/linux_amd64/compile" /work/x2.log | grep -F 'probe.go' | tail -1)
echo "WORKDIR=$WORKDIR"
echo "$CMDLINE"
[ -z "$CMDLINE" ] && { echo FATAL_NO_CMDLINE; exit 86; }

say "replay that exact command line with the diary compiler substituted"
RAW=/work/diary2.raw
rm -f "$RAW"
NEW=$(printf '%s' "$CMDLINE" | sed "s#$GOROOT/pkg/tool/linux_amd64/compile #/persist/compile_diary2 #")
cd $P
env WORK="$WORKDIR" COMPILER_DIARY="$RAW" bash -c "$NEW"
echo "instrumented_compile_exit=$?"
ls -l $P "$RAW"

say "shape the diary"
python3 - "$RAW" /out/diary_go2.txt <<'PY'
import sys
raw = open(sys.argv[1])
out = open(sys.argv[2], "w")
count = 0
for line in raw:
    line = line.rstrip("\n")
    if line == "":
        continue
    seq, subject, record = line.split("\t", 2)
    parts = record.split("|")
    node_id = parts[0]
    name = parts[1]
    where = parts[2]
    out.write("%s\t%s\t%s\t%s\t%s\n" % (seq, subject, node_id, name, where))
    count = count + 1
raw.close()
out.close()
print("events=%d" % count)
PY
echo "shape_exit=$?"
wc -l /out/diary_go2.txt

say "subjects seen, with event counts"
cut -f2 /out/diary_go2.txt | sort | uniq -c | sort -rn

say "spots by subject"
cut -f2,4 /out/diary_go2.txt | sort | uniq -c | sort -k2,2 | head -100

say "ACCEPTANCE: the abi chain, with subjects"
grep -nE 'params_loop|assignParam|tryAllocRegs|allocateRegs|subject_enter' /out/diary_go2.txt | head -120

say "full diary"
cat /out/diary_go2.txt

say disk
df -h /work /persist | sed -n 1,4p
echo DONE_OK
'''

lane = HEAD + injector + MID + targets + TAIL
out = os.path.join(REPO, "lanes", "cg_diary_l2.sh")
handle = open(out, "w", encoding="utf-8")
handle.write(lane)
handle.close()
os.chmod(out, 0o755)
print("wrote %s (%d bytes)" % (out, len(lane)))
