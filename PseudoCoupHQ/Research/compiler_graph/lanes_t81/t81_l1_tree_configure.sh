#!/usr/bin/env bash
# t81 lane 1 — the PATH CHECK, then the llvm tree at the pin, then the
# cmake configure. Everything the instrumented build needs and nothing
# it does not.
#
# The cost page (log_175 section 6.2, measured by task 72) says: shared
# clone 0 s, sparse-checkout disable plus checkout 10 s, configure 11 s.
# This lane prints its OWN timings beside those, so the schedule is
# re-measured rather than inherited.
set -u
say() { echo; echo "======== $* ========"; }

say "0. which side of the wall"
echo "hostname: $(cat /etc/hostname 2>/dev/null)"
echo "-- a host-only path must NOT exist in here:"
# a glob, so no user name is ever written into a tracked artifact
ls -d /home/*/Programming 2>&1 || echo "  ABSENT (as expected inside the container)"
echo "-- container-only paths that must exist:"
for p in /persist /sources /projects/PseudoCoupHQ /work /out ; do
  printf '  %-28s ' "$p"; ls -d "$p" >/dev/null 2>&1 && echo present || echo ABSENT
done

say "1. the toolchain, QUOTED"
cmake --version 2>&1 | head -1
ninja --version 2>&1 | head -1
clang --version 2>&1 | head -1
clang++ --version 2>&1 | head -1
python3 --version 2>&1
nproc
free -g | head -2
df -h /persist | tail -1

say "2. the read-only source, and its working tree"
ls -d /sources/llvm-project 2>&1
echo "-- the sparse cone on the read-only tree (why a clone is needed):"
git -C /sources/llvm-project sparse-checkout list 2>&1 | head
echo "-- the pin, resolved from the object store:"
git -C /sources/llvm-project rev-parse llvmorg-21.1.8^{commit} 2>&1

say "3. the working tree at the pin, in /persist"
if [ -d /persist/llvmsrc/.git ]; then
  echo "   already present; head:"
  git -C /persist/llvmsrc rev-parse HEAD 2>&1
else
  T=$(date +%s)
  git clone --shared --no-checkout /sources/llvm-project /persist/llvmsrc \
      > /persist/llvm_clone.log 2>&1
  echo "   shared clone exit=$? seconds=$(( $(date +%s) - T ))"
  T=$(date +%s)
  git -C /persist/llvmsrc sparse-checkout disable >> /persist/llvm_clone.log 2>&1
  git -C /persist/llvmsrc checkout llvmorg-21.1.8 >> /persist/llvm_clone.log 2>&1
  RC=$?
  echo "   checkout llvmorg-21.1.8 exit=$RC seconds=$(( $(date +%s) - T )) (cost page: 10 s)"
fi
echo "   head, QUOTED:"; git -C /persist/llvmsrc rev-parse HEAD 2>&1
echo "   working tree size:"; du -sh /persist/llvmsrc 2>&1

say "4. the region on disk, counted against the graph's own file count"
find /persist/llvmsrc/clang/lib/CodeGen /persist/llvmsrc/llvm/lib/Target/X86 \
     -type f \( -name '*.cpp' -o -name '*.h' -o -name '*.td' \) | wc -l
echo "   of which .cpp:"
find /persist/llvmsrc/clang/lib/CodeGen /persist/llvmsrc/llvm/lib/Target/X86 \
     -type f -name '*.cpp' | wc -l

say "5. every target file this lap will edit is present at the pin"
python3 - <<'PY'
import json, os
targets = json.load(open('/projects/PseudoCoupHQ/Research/compiler_graph/'
                         't81/diary_targets_cpp.json'))
files = sorted({row['file'] for row in targets['targets']})
absent = [f for f in files if not os.path.exists('/persist/llvmsrc/' + f)]
print('   target files : %d' % len(files))
print('   absent       : %d' % len(absent))
for name in absent[:10]:
    print('      %s' % name)
PY

say "6. cmake configure (cap 1800 s)"
if [ -f /persist/llvmbuild/build.ninja ]; then
  echo "   already configured; skipping"
else
  rm -rf /persist/llvmbuild && mkdir -p /persist/llvmbuild
  T=$(date +%s)
  timeout 1800 cmake -S /persist/llvmsrc/llvm -B /persist/llvmbuild -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLVM_ENABLE_PROJECTS=clang \
      -DLLVM_TARGETS_TO_BUILD=X86 \
      -DLLVM_ENABLE_ASSERTIONS=OFF \
      -DLLVM_INCLUDE_TESTS=OFF \
      -DLLVM_INCLUDE_BENCHMARKS=OFF \
      -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
      > /persist/llvm_configure.log 2>&1
  RC=$?
  echo "   configure exit=$RC seconds=$(( $(date +%s) - T )) (cost page: 11 s)"
  tail -6 /persist/llvm_configure.log
fi
echo "   objects a full clang build would compile:"
ninja -C /persist/llvmbuild -t targets all 2>/dev/null | grep -c '\.o:'

say "7. disk"
du -sh /persist/llvmsrc /persist/llvmbuild 2>&1
df -h /persist | tail -1
echo "DONE t81_l1"
