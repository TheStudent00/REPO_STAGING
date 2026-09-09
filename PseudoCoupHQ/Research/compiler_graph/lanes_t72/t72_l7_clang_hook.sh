#!/usr/bin/env bash
# t72 lane 7 — the cost page's two remaining measurements for clang:
#   (a) the EMISSION HOOK, proved by a one-file instrumented build;
#   (b) the FULL clang+llvm(X86) build, timed, so round 15 has a real
#       denominator instead of a reputation.
# Plus the rust clone's actual error text, which lane 6 did not print.
set -u
say() { echo; echo "======== $* ========"; }

say "0. why the rust shared clone exited 128"
cat /persist/rust_clone.log 2>&1 | head -20

say "1. the emission hook for clang, one file, proved by building it"
F=/persist/llvmsrc/clang/lib/CodeGen/CGExpr.cpp
cp -f "$F" /persist/CGExpr.cpp.orig
python3 - <<'PY'
path = '/persist/llvmsrc/clang/lib/CodeGen/CGExpr.cpp'
text = open(path).read()
hook = '''
// ---- t72 diary hook, one translation unit, no build-file change ----
// The go lap's hook is a generated go package plus one statement per
// function body. The same shape in C++ is a file-scope helper plus one
// statement per body; this proves the C++ half compiles in-tree.
#include <cstdio>
#include <cstdlib>
namespace {
void t72_diary_note(const char *record) {
  static FILE *out = nullptr;
  static bool tried = false;
  if (!tried) {
    tried = true;
    const char *path = std::getenv("COMPILER_DIARY");
    if (path) out = std::fopen(path, "a");
  }
  if (out) { std::fputs(record, out); std::fputc('\\n', out); }
}
} // namespace
'''
anchor = '\nusing namespace clang;\n'
assert anchor in text, 'anchor not found'
text = text.replace(anchor, anchor + hook, 1)
# one entry hook, in one real body of the region
body = 'RValue CodeGenFunction::EmitAnyExpr(const Expr *E,'
at = text.index(body)
brace = text.index('{', text.index(')', at))
note = '\n  t72_diary_note("clang/lib/CodeGen/CGExpr.cpp|EmitAnyExpr");'
text = text[:brace + 1] + note + text[brace + 1:]
open(path, 'w').write(text)
print('   hook + 1 entry statement written into CGExpr.cpp')
PY
echo "   rebuild that one object:"
T=$(date +%s)
timeout 900 ninja -C /persist/llvmbuild -j6 \
    tools/clang/lib/CodeGen/CMakeFiles/obj.clangCodeGen.dir/CGExpr.cpp.o \
    > /persist/llvm_hookobj.log 2>&1
echo "      instrumented one-file build exit=$? seconds=$(( $(date +%s) - T ))"
tail -4 /persist/llvm_hookobj.log

say "2. the full clang+llvm(X86) build, timed (cap 10800 s)"
echo "   objects to compile: $(ninja -C /persist/llvmbuild -t targets all 2>/dev/null | grep -c '\.o:')"
T=$(date +%s)
timeout 10800 ninja -C /persist/llvmbuild -j6 clang > /persist/llvm_full.log 2>&1
RC=$?
echo "   full build exit=$RC seconds=$(( $(date +%s) - T )) (cap 10800)"
tail -4 /persist/llvm_full.log
echo "   build tree disk after:"; du -sh /persist/llvmbuild
ls -la /persist/llvmbuild/bin/clang-* 2>/dev/null | head -2
echo "   the pin, QUOTED from the binary just built:"
/persist/llvmbuild/bin/clang --version 2>&1 | head -2

say "3. restore CGExpr.cpp"
cp -f /persist/CGExpr.cpp.orig "$F"
echo "   restored"

say "4. disk"
du -sh /persist/llvmsrc /persist/llvmbuild /persist/gosrc 2>/dev/null
df -h /persist | tail -1
echo "DONE t72_l7"
