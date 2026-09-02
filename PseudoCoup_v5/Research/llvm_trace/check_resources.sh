#!/usr/bin/env bash
# Reports what is already present for the LLVM chain investigation.
# Safe to run any time; changes nothing.
set +e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/sources"
RUSTSRC="$HERE/../rust_routing/sources"

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
no()   { printf '  \033[31m✗\033[0m %s\n' "$1"; }
note() { printf '    %s\n' "$1"; }

echo "== toolchains =="
for t in git cmake ninja clang++ g++ python3 rustc; do
    if command -v "$t" >/dev/null 2>&1; then
        ok "$t  ($("$t" --version 2>/dev/null | head -1 | cut -c1-50))"
    else
        no "$t  MISSING"
    fi
done

echo
echo "== already-fetched Rust sources (from rust_routing) =="
for p in \
  "$RUSTSRC/rust/compiler/rustc_codegen_llvm" \
  "$RUSTSRC/rust/compiler/rustc_codegen_ssa" \
  "$RUSTSRC/encoder/asm/assembler.rs"
do
    [ -e "$p" ] && ok "$(basename "$p")  ($(du -sh "$p" 2>/dev/null | cut -f1))" \
                || no "$(basename "$p")  not fetched"
done

echo
echo "== LLVM sources (this investigation) =="
if [ -d "$SRC/llvm-project/.git" ]; then
    ok "llvm-project clone ($(du -sh "$SRC/llvm-project" 2>/dev/null | cut -f1))"
    for p in llvm/lib/Target/X86 llvm/lib/CodeGen/SelectionDAG \
             llvm/include/llvm/CodeGen; do
        [ -d "$SRC/llvm-project/$p" ] && ok "  $p" || no "  $p not in sparse set"
    done
else
    no "llvm-project  not cloned  (run ./fetch_llvm.sh)"
fi

echo
echo "== TableGen-generated files (need a build to exist) =="
for f in X86GenDAGISel.inc X86GenInstrInfo.inc; do
    G=$(find "$SRC" -name "$f" 2>/dev/null | head -1)
    [ -n "$G" ] && ok "$f  ($(wc -l < "$G") lines)" \
                || no "$f  not generated  (fetch_llvm.sh --tblgen)"
done
note "X86GenMCCodeEmitter.inc is NOT expected: X86 never runs"
note "-gen-emitter; its encoder is hand-written C++"
note "(X86MCCodeEmitter.cpp). Verified by survey 2026-07-25."

TBL=""
for c in llvm-tblgen llvm-tblgen-21 llvm-tblgen-20 llvm-tblgen-19 \
         /usr/lib/llvm-21/bin/llvm-tblgen; do
    command -v "$c" >/dev/null 2>&1 && { TBL="$(command -v "$c")"; break; }
    [ -x "$c" ] && { TBL="$c"; break; }
done
[ -z "$TBL" ] && [ -x "$SRC/tblgen-build/bin/llvm-tblgen" ] && TBL="$SRC/tblgen-build/bin/llvm-tblgen"
[ -n "$TBL" ] && ok "llvm-tblgen  ($TBL)" \
              || no "llvm-tblgen  none found  (sudo apt install llvm-21-dev)"

echo
echo "== disk =="
df -h "$HERE" | tail -1 | awk '{print "  free on this filesystem:", $4}'
