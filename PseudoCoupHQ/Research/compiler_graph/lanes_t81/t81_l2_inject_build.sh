#!/usr/bin/env bash
# t81 lane 2 — place the entry hooks in the region, prove ONE object of
# each half of the region still compiles, then build clang, timed
# against the cost page's 1,316 s / 784 MB (log_175 section 6.2).
#
# ORDER MATTERS AND IS DELIBERATE. The two single-object builds come
# before the full build so that a defect in the injected text costs 80
# seconds rather than 22 minutes, and so that both halves of the region
# — clang's CodeGen and llvm's X86 backend — are proved, not one.
set -u
say() { echo; echo "======== $* ========"; }
REPO=/projects/PseudoCoupHQ/Research/compiler_graph

say "[1/6] the injection"
if grep -q "t81diary::note(" /persist/llvmsrc/clang/lib/CodeGen/CGExpr.cpp 2>/dev/null; then
  echo "   already injected; skipping the edit"
else
  T=$(date +%s)
  python3 "$REPO/t81/inject_diary_clang.py" \
      --targets "$REPO/t81/diary_targets_cpp.json" \
      --src /persist/llvmsrc \
      --report "$REPO/t81/inject_report_cpp.json" \
      > /persist/inject.log 2>&1
  RC=$?
  echo "   inject exit=$RC seconds=$(( $(date +%s) - T ))"
  tail -8 /persist/inject.log
fi
echo "   LITERAL, the first injected statement of CGExpr.cpp:"
grep -m1 -n "t81diary::note(" /persist/llvmsrc/clang/lib/CodeGen/CGExpr.cpp

say "[2/6] one object of clang's CodeGen half (cap 5400 s)"
T=$(date +%s)
timeout 5400 ninja -C /persist/llvmbuild -j6 \
    tools/clang/lib/CodeGen/CMakeFiles/obj.clangCodeGen.dir/CGExpr.cpp.o \
    > /persist/obj_codegen.log 2>&1
RC=$?
echo "   exit=$RC seconds=$(( $(date +%s) - T )) (cost page, cold: 73 s)"
tail -20 /persist/obj_codegen.log
if [ $RC -ne 0 ]; then echo "   STOP: the injected CodeGen text does not compile"; exit 2; fi

say "[3/6] one object of llvm's X86 half (cap 5400 s)"
X86OBJ=$(ninja -C /persist/llvmbuild -t targets all 2>/dev/null \
         | grep -o '[^ ]*X86ISelLowering\.cpp\.o' | head -1)
echo "   target: $X86OBJ"
T=$(date +%s)
timeout 5400 ninja -C /persist/llvmbuild -j6 "$X86OBJ" \
    > /persist/obj_x86.log 2>&1
RC=$?
echo "   exit=$RC seconds=$(( $(date +%s) - T ))"
tail -20 /persist/obj_x86.log
if [ $RC -ne 0 ]; then echo "   STOP: the injected X86 text does not compile"; exit 3; fi

say "[4/6] the full instrumented clang build (cap 10800 s)"
T=$(date +%s)
timeout 10800 ninja -C /persist/llvmbuild -j6 clang > /persist/llvm_full.log 2>&1
RC=$?
echo "   full build exit=$RC seconds=$(( $(date +%s) - T )) (cost page: 1,316 s)"
tail -6 /persist/llvm_full.log
if [ $RC -ne 0 ]; then
  echo "   the failing edges, by file:"
  grep -n "error:" /persist/llvm_full.log | head -40
  echo "   STOP: the instrumented build did not finish"
  exit 4
fi
echo "   build tree after:"; du -sh /persist/llvmbuild
echo "   (cost page: 784 MB)"
ls -la /persist/llvmbuild/bin/clang-* 2>/dev/null | head -2

say "[5/6] the pin, QUOTED from the binary just built"
/persist/llvmbuild/bin/clang --version 2>&1 | head -3

say "[6/6] the emission hook proved on one probe"
mkdir -p /work/probe /persist/probecfg
python3 - <<'PY'
import json
probes = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                        't81/probes_cpp.json'))['probes']
open('/work/probe/unit.c', 'w').write(probes['c/op_0']['source'])
open('/work/probe/unit.cpp', 'w').write(probes['cpp/op_0']['source'])
print('   probe c/op_0 and cpp/op_0 written')
PY
rm -f /work/smoke.c.* /work/smoke.cpp.*
echo "   the SHIP tool line, as op_pipeline/trickle_lanes/regen_c_c0023.sh writes it:"
echo "     clang   -std=c17   -O1 -c unit.c   -o unit_ship.o"
echo "     clang++ -std=c++20 -O1 -c unit.cpp -o unit_ship.o"
T=$(date +%s)
COMPILER_DIARY=/work/smoke.c /persist/llvmbuild/bin/clang -std=c17 -O1 \
    -c /work/probe/unit.c -o /work/probe/unit_c.o 2>&1 | head -5
echo "   c probe exit=$? seconds=$(( $(date +%s) - T ))"
T=$(date +%s)
COMPILER_DIARY=/work/smoke.cpp /persist/llvmbuild/bin/clang++ -std=c++20 -O1 \
    -c /work/probe/unit.cpp -o /work/probe/unit_cpp.o 2>&1 | head -5
echo "   cpp probe exit=$? seconds=$(( $(date +%s) - T ))"
echo "   diary files produced (one per process — the driver forks -cc1):"
for f in /work/smoke.c.* /work/smoke.cpp.* ; do
  [ -e "$f" ] || continue
  printf '     %-24s %10d lines %10d bytes\n' "$(basename "$f")" \
      "$(wc -l < "$f")" "$(stat -c %s "$f")"
done
echo "   LITERAL, the first five lines of the largest c diary:"
LARGEST=$(ls -S /work/smoke.c.* 2>/dev/null | head -1)
head -5 "$LARGEST" 2>&1
echo "   malformed lines (not three tab fields):"
awk -F'\t' 'NF!=3' "$LARGEST" 2>/dev/null | wc -l
cp -f "$LARGEST" "$REPO/t81/smoke_c_op_0.diary" 2>/dev/null || true

say "disk"
du -sh /persist/llvmsrc /persist/llvmbuild 2>&1
df -h /persist | tail -1
echo "DONE t81_l2"
