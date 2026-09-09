#!/usr/bin/env bash
# t72 lane 6 — THE COST PAGE, second pass, after lane 5 found why the
# first configure attempts exited in zero seconds.
#
# WHAT LANE 5 FOUND: /sources/llvm-project and /sources/rust have SPARSE
# WORKING TREES (llvm: 7 cone paths, no clang/ and no cmake/ on disk;
# rust: 3 codegen crates, no rustc_middle). Their object stores are
# COMPLETE (git show at the pin returns clang/lib/CodeGen/CGExpr.cpp),
# so a full tree can be made with NO NETWORK -- which matters, because
# this instance has no route out at all. /sources is read-only, so the
# tree is made in /persist by a shared-object clone.
set -u
say() { echo; echo "======== $* ========"; }

say "A. clang / llvm — make a full tree at the region's pin"
T=$(date +%s)
rm -rf /persist/llvmsrc
git clone --shared --no-checkout /sources/llvm-project /persist/llvmsrc \
    > /persist/llvm_clone.log 2>&1
echo "   shared clone exit=$? seconds=$(( $(date +%s) - T ))"
T=$(date +%s)
git -C /persist/llvmsrc sparse-checkout disable >> /persist/llvm_clone.log 2>&1
git -C /persist/llvmsrc checkout llvmorg-21.1.8 >> /persist/llvm_clone.log 2>&1
RC=$?
echo "   checkout llvmorg-21.1.8 exit=$RC seconds=$(( $(date +%s) - T ))"
git -C /persist/llvmsrc log -1 --format='   HEAD %H %cd'
echo "   working tree disk (objects are shared with /sources, not copied):"
du -sh --exclude=.git /persist/llvmsrc
du -sh /persist/llvmsrc/.git
echo "   region files now on disk (clang/lib/CodeGen + llvm/lib/Target/X86):"
find /persist/llvmsrc/clang/lib/CodeGen /persist/llvmsrc/llvm/lib/Target/X86 \
     -type f \( -name '*.cpp' -o -name '*.h' -o -name '*.td' \) | wc -l

say "B. clang / llvm — cmake configure (cap 1800 s)"
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
    > /persist/llvm_configure2.log 2>&1
RC=$?
echo "   configure exit=$RC seconds=$(( $(date +%s) - T )) (cap 1800)"
tail -6 /persist/llvm_configure2.log
if [ $RC -ne 0 ]; then echo "   STOP: configure did not finish"; fi

if [ $RC -eq 0 ]; then
  say "C. clang / llvm — the full-build denominator, then ONE region object"
  echo "   ninja edges for a full clang+llvm(X86) build:"
  ninja -C /persist/llvmbuild -n 2>/dev/null | wc -l
  echo "   objects the build would compile:"
  ninja -C /persist/llvmbuild -t targets all 2>/dev/null | grep -c '\.o:'
  echo "   -- one region object, CGExpr.cpp.o, WITH its prerequisites (cap 5400 s)"
  echo "      (ninja builds llvm-tblgen and the generated .inc headers first;"
  echo "       that is the real cost of touching this region at all)"
  T=$(date +%s)
  timeout 5400 ninja -C /persist/llvmbuild -j6 \
      tools/clang/lib/CodeGen/CMakeFiles/obj.clangCodeGen.dir/CGExpr.cpp.o \
      > /persist/llvm_oneobj2.log 2>&1
  echo "      exit=$? seconds=$(( $(date +%s) - T )) (cap 5400)"
  tail -6 /persist/llvm_oneobj2.log
  echo "   -- the same object again, now that prerequisites exist (the marginal cost):"
  touch /persist/llvmsrc/clang/lib/CodeGen/CGExpr.cpp
  T=$(date +%s)
  timeout 900 ninja -C /persist/llvmbuild -j6 \
      tools/clang/lib/CodeGen/CMakeFiles/obj.clangCodeGen.dir/CGExpr.cpp.o \
      > /persist/llvm_oneobj3.log 2>&1
  echo "      exit=$? seconds=$(( $(date +%s) - T ))"
  echo "   build tree disk:"; du -sh /persist/llvmbuild
fi

say "D. rustc — the pin frontier, measured"
echo "   the compiler that compiled the corpus, quoted from the toolchain:"
rustc --version --verbose 2>&1 | head -4
echo "   is that commit in the source checkout's object store?"
git -C /sources/rust cat-file -e 31fca3adb 2>&1 && echo "   PRESENT" || echo "   ABSENT — the exact source is not on this machine"
echo "   the checkout's own head, and whether the region is complete there:"
git -C /sources/rust log -1 --format='   %H %cd'
for d in compiler/rustc_codegen_ssa compiler/rustc_codegen_llvm compiler/rustc_middle/src/mir ; do
  printf '   %-38s working tree ' "$d"
  ls -d "/sources/rust/$d" >/dev/null 2>&1 && echo -n "present" || echo -n "ABSENT"
  git -C /sources/rust cat-file -e "7c329d6c:$d" 2>/dev/null && echo "  / objects present" || echo "  / objects ABSENT"
done
echo "   full tree by shared clone (cap 900 s):"
T=$(date +%s)
rm -rf /persist/rustsrc
timeout 900 git clone --shared --no-checkout /sources/rust /persist/rustsrc > /persist/rust_clone.log 2>&1
git -C /persist/rustsrc sparse-checkout disable >> /persist/rust_clone.log 2>&1
timeout 900 git -C /persist/rustsrc checkout 7c329d6c >> /persist/rust_clone.log 2>&1
echo "      exit=$? seconds=$(( $(date +%s) - T ))"
du -sh --exclude=.git /persist/rustsrc 2>/dev/null
echo "   does bootstrap exist now?"
ls /persist/rustsrc/src/bootstrap/bootstrap.py 2>&1 | head -1
echo "   submodules a rustc build needs (llvm-project), present?"
ls -d /persist/rustsrc/src/llvm-project 2>&1 | head -1
ls /persist/rustsrc/src/llvm-project 2>/dev/null | wc -l

say "E. swiftc — what stops it here"
echo "   swiftc installed in this container?"; command -v swiftc || echo "   NOT INSTALLED"
echo "   the swift build needs these repos beside the swift tree:"
for d in cmark swift-syntax swift-corelibs-libdispatch llvm-project ; do
  printf '   %-30s ' "$d"; ls -d /sources/$d >/dev/null 2>&1 && echo present || echo ABSENT
done
echo "   and the llvm it needs is APPLE'S FORK, not upstream. Branches here:"
git -C /sources/llvm-project branch -a 2>&1 | head -5
echo "   this instance has proxy = no: nothing can be fetched. So a swift"
echo "   build cannot be started here at all; that is the measurement."

say "F. disk at the end"
du -sh /persist/* 2>/dev/null | sort -h | tail -14
df -h /persist | tail -1
echo "DONE t72_l6"
