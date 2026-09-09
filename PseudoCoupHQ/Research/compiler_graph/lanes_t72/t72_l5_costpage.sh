#!/usr/bin/env bash
# t72 lane 5 — THE COST PAGE. What a diary lap costs for clang, rustc and
# swiftc ON THIS MACHINE, measured, not estimated from reputation.
#
# For each: the source that is actually on disk, its size, the region's
# file count, whether an instrumented build can be started at all, and
# the wall clock of every step that ran. Every step is capped by
# `timeout` and the cap is printed, so a step that does not finish
# reports the wall clock it reached and what it was doing -- that is a
# measurement, not a failure.
set -u
export CCACHE_DISABLE=1
say() { echo; echo "======== $* ========"; }

say "0. the machine and the toolchain, quoted"
nproc; free -g | head -2; df -h /persist | tail -1
for t in cmake ninja clang clang++ gcc rustc cargo swiftc python3 git; do
  printf '%-10s ' "$t"
  command -v "$t" >/dev/null 2>&1 && { "$t" --version 2>&1 | head -1; } || echo "NOT INSTALLED"
done

say "1. go — the lap that was actually run, for comparison"
echo "source on disk:"; du -sh /sources/golang_src
echo "region files (ssagen, abi, amd64, ssa, non-test):"
find /sources/golang_src/src/cmd/compile/internal/{ssagen,abi,amd64,ssa} \
     -name '*.go' ! -name '*_test.go' | wc -l
echo "toolchain build (make.bash), measured in lane t72_l1: 124 s"
echo "instrumented cmd/compile rebuild, measured in lane t72_l2: 20 s"
echo "one probe compile, measured in lane t72_l3/l4: 0.19 s (5.3 probes/s)"
echo "disk after the lap:"; du -sh /persist/gosrc /persist/gocache /persist/compile_diary_all

say "2. clang / llvm"
echo "checkout HEAD and the pin the graph region uses:"
git -C /sources/llvm-project log -1 --format='%H %cd' 2>&1 | head -1
git -C /sources/llvm-project rev-parse llvmorg-21.1.8 2>&1 | head -1
echo "source on disk:"; du -sh /sources/llvm-project
echo "region files (clang/lib/CodeGen + llvm/lib/Target/X86):"
find /sources/llvm-project/clang/lib/CodeGen /sources/llvm-project/llvm/lib/Target/X86 \
     -name '*.cpp' -o -name '*.h' -o -name '*.td' 2>/dev/null | wc -l
echo "-- cmake configure, X86 only, clang only, Release, ninja (cap 1800 s)"
rm -rf /persist/llvmbuild && mkdir -p /persist/llvmbuild
T=$(date +%s)
timeout 1800 cmake -S /sources/llvm-project/llvm -B /persist/llvmbuild -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS=clang \
    -DLLVM_TARGETS_TO_BUILD=X86 \
    -DLLVM_ENABLE_ASSERTIONS=OFF \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    > /persist/llvm_configure.log 2>&1
RC=$?
echo "   configure exit=$RC  seconds=$(( $(date +%s) - T ))  (cap 1800)"
tail -5 /persist/llvm_configure.log
if [ $RC -eq 0 ]; then
  echo "-- build ONE object of the region: clang/lib/CodeGen/CGExpr.cpp (cap 3600 s)"
  echo "   ninja builds its prerequisites first (tablegen, the generated .inc"
  echo "   headers), so this wall clock is 'first object of CodeGen', not"
  echo "   'one compiler invocation'. Both numbers are printed."
  T=$(date +%s)
  timeout 3600 ninja -C /persist/llvmbuild \
      tools/clang/lib/CodeGen/CMakeFiles/obj.clangCodeGen.dir/CGExpr.cpp.o \
      > /persist/llvm_oneobj.log 2>&1
  RC2=$?
  echo "   one-object exit=$RC2  seconds=$(( $(date +%s) - T ))  (cap 3600)"
  tail -8 /persist/llvm_oneobj.log
  echo "-- total edges in the ninja graph (the full-build denominator):"
  ninja -C /persist/llvmbuild -n 2>/dev/null | wc -l
  echo "-- how many of those are clang/llvm objects:"
  ninja -C /persist/llvmbuild -t targets all 2>/dev/null | grep -c '\.o:' || true
fi
echo "-- disk used by the build tree so far:"; du -sh /persist/llvmbuild 2>/dev/null

say "3. rustc"
echo "checkout HEAD:"; git -C /sources/rust log -1 --format='%H %cd' 2>&1 | head -1
echo "SPARSE CHECKOUT? core.sparseCheckout ="; git -C /sources/rust config core.sparseCheckout
echo "sparse cone:"; git -C /sources/rust sparse-checkout list 2>&1 | head
echo "source on disk:"; du -sh /sources/rust
echo "region files (rustc_codegen_ssa, rustc_codegen_llvm, rustc_middle/src/mir):"
find /sources/rust/compiler/rustc_codegen_ssa /sources/rust/compiler/rustc_codegen_llvm \
     /sources/rust/compiler/rustc_middle/src/mir -name '*.rs' 2>/dev/null | wc -l
echo "-- can x.py even start? (cap 300 s)"
T=$(date +%s)
timeout 300 python3 /sources/rust/x.py --help > /persist/rust_x.log 2>&1
echo "   x.py exit=$?  seconds=$(( $(date +%s) - T ))"
tail -6 /persist/rust_x.log

say "4. swiftc"
echo "checkout tag:"; git -C /sources/swift-6.0.3-RELEASE describe --tags 2>&1 | head -1
echo "source on disk:"; du -sh /sources/swift-6.0.3-RELEASE
echo "region files (lib/SILGen + lib/IRGen):"
find /sources/swift-6.0.3-RELEASE/lib/SILGen /sources/swift-6.0.3-RELEASE/lib/IRGen \
     -name '*.cpp' -o -name '*.h' 2>/dev/null | wc -l
echo "-- what a swift build needs beside the swift tree, and what is here:"
for d in llvm-project cmark swift-syntax swift-corelibs-libdispatch; do
  printf '   %-28s ' "$d"; ls -d /sources/$d >/dev/null 2>&1 && echo present || echo ABSENT
done
echo "-- does this llvm checkout carry the swift fork's branch?"
git -C /sources/llvm-project branch -a 2>&1 | grep -i swift | head -3 || echo "   no swift branch"
echo "-- cmake configure attempt, direct, no build-script (cap 900 s)"
rm -rf /persist/swiftbuild && mkdir -p /persist/swiftbuild
T=$(date +%s)
timeout 900 cmake -S /sources/swift-6.0.3-RELEASE -B /persist/swiftbuild -G Ninja \
    > /persist/swift_configure.log 2>&1
echo "   configure exit=$?  seconds=$(( $(date +%s) - T ))  (cap 900)"
tail -12 /persist/swift_configure.log

say "5. disk at the end"
du -sh /persist/* 2>/dev/null | sort -h | tail -12
df -h /persist | tail -1
echo "DONE t72_l5"
