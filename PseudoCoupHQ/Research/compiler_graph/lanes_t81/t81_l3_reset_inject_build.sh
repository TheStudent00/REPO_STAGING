#!/usr/bin/env bash
# t81 lane 3 — RESET the working tree to the pin, re-inject the entry
# hooks with the corrected label flattening, prove one object of EACH
# half of the region compiles, then build clang.
#
# WHY A RESET FIRST. Lane 2 (log 20260904T035629Z) injected a label
# carrying a newline into a C string literal, the literal ran on into
# the rest of the function, and CGExpr.cpp failed to compile with
# `use of undeclared identifier 'E'` twenty times over. The tree on
# /persist still holds those edits, and the injector skips any file
# that already carries the marker. So the edits are undone from the
# object store before anything else happens.
#
# ORDER IS DELIBERATE, unchanged from lane 2: the two single-object
# builds come before the full build, so a defect in the injected text
# costs 80 seconds and not 22 minutes, and BOTH halves of the region
# are proved.
set -u
say() { echo; echo "======== $* ========"; }
REPO=/projects/PseudoCoupHQ/Research/compiler_graph

say "[1/7] reset the working tree to the pin"
T=$(date +%s)
git -C /persist/llvmsrc checkout -- . 2>&1 | tail -3
echo "   checkout -- . exit=$? seconds=$(( $(date +%s) - T ))"
git -C /persist/llvmsrc clean -fdq 2>&1 | tail -3
echo "   head, QUOTED:"; git -C /persist/llvmsrc rev-parse HEAD
echo "   files still carrying the marker (must be 0):"
grep -rl "t81diary" /persist/llvmsrc/clang/lib/CodeGen \
     /persist/llvmsrc/llvm/lib/Target/X86 2>/dev/null | wc -l
echo "   git says the tree is clean (must print nothing):"
git -C /persist/llvmsrc status --porcelain | head -5

say "[2/7] the injection"
T=$(date +%s)
python3 "$REPO/t81/inject_diary_clang.py" \
    --targets "$REPO/t81/diary_targets_cpp.json" \
    --src /persist/llvmsrc \
    --report "$REPO/t81/inject_report_cpp2.json" \
    > /persist/inject2.log 2>&1
RC=$?
echo "   inject exit=$RC seconds=$(( $(date +%s) - T ))"
tail -10 /persist/inject2.log
if [ $RC -ne 0 ]; then echo "   STOP: the injector failed"; exit 2; fi

say "[3/7] every injected statement is ONE well-formed line"
python3 - <<'PY'
import json, os, re, sys
report = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                        't81/inject_report_cpp2.json'))
files = sorted({c.rsplit(':', 1)[0]
                for c in report['instrumented_coordinates']})
pattern = re.compile(r'^\s*t81diary::(note|enter)\(.*\);\s*$')
bad = []
total = 0
for name in files:
    full = os.path.join('/persist/llvmsrc', name)
    for number, line in enumerate(open(full, errors='replace'), 1):
        if 't81diary::note(' not in line and 't81diary::enter(' not in line:
            continue
        if 't81diary::note(const char' in line or 'inline void' in line:
            continue
        total = total + 1
        if not pattern.match(line.rstrip('\n')):
            bad.append('%s:%d: %s' % (name, number, line.rstrip()[:120]))
print('   injected call lines : %d' % total)
print('   malformed           : %d' % len(bad))
for row in bad[:10]:
    print('      %s' % row)
# an unbalanced double quote inside the record would run the literal on
runon = [row for row in bad]
sys.exit(1 if bad else 0)
PY
if [ $? -ne 0 ]; then echo "   STOP: an injected statement is not one line"; exit 3; fi

say "[4/7] one object of clang's CodeGen half (cap 5400 s)"
T=$(date +%s)
timeout 5400 ninja -C /persist/llvmbuild -j6 \
    tools/clang/lib/CodeGen/CMakeFiles/obj.clangCodeGen.dir/CGExpr.cpp.o \
    > /persist/obj_codegen2.log 2>&1
RC=$?
echo "   exit=$RC seconds=$(( $(date +%s) - T )) (cost page, cold: 73 s)"
tail -20 /persist/obj_codegen2.log
if [ $RC -ne 0 ]; then echo "   STOP: the injected CodeGen text does not compile"; exit 4; fi

say "[5/7] one object of llvm's X86 half (cap 5400 s)"
X86OBJ=$(ninja -C /persist/llvmbuild -t targets all 2>/dev/null \
         | grep -o '[^ ]*X86ISelLowering\.cpp\.o' | head -1)
echo "   target: $X86OBJ"
T=$(date +%s)
timeout 5400 ninja -C /persist/llvmbuild -j6 "$X86OBJ" \
    > /persist/obj_x862.log 2>&1
RC=$?
echo "   exit=$RC seconds=$(( $(date +%s) - T ))"
tail -20 /persist/obj_x862.log
if [ $RC -ne 0 ]; then echo "   STOP: the injected X86 text does not compile"; exit 5; fi

say "[6/7] the full instrumented clang build (cap 10800 s)"
T=$(date +%s)
timeout 10800 ninja -C /persist/llvmbuild -j6 clang > /persist/llvm_full2.log 2>&1
RC=$?
echo "   full build exit=$RC seconds=$(( $(date +%s) - T )) (cost page: 1,316 s)"
tail -6 /persist/llvm_full2.log
if [ $RC -ne 0 ]; then
  echo "   the failing edges, by file:"
  grep -n "error:" /persist/llvm_full2.log | head -40
  echo "   STOP: the instrumented build did not finish"
  exit 6
fi
echo "   build tree after:"; du -sh /persist/llvmbuild
echo "   (cost page: 784 MB)"
ls -la /persist/llvmbuild/bin/clang-* 2>/dev/null | head -2

say "[7/7] the pin, QUOTED from the binary just built"
/persist/llvmbuild/bin/clang --version 2>&1 | head -3
df -h /persist | tail -1
echo "DONE t81_l3"
