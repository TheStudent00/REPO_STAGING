#!/usr/bin/env bash
# Fetches LLVM sources for tracing sdiv -> IDIV64r -> bytes.
#
#   ./fetch_llvm.sh             sources for reading (~80 MB) — ENOUGH
#                               for the full walk-through
#   ./fetch_llvm.sh --tblgen    additionally obtain llvm-tblgen and
#                               generate the ISel matcher .inc files
#                               (only needed for the GRAMMAR SURVEY
#                               comparison against Cranelift's
#                               generated Rust)
#
# Idempotent; repairs a previously failed sparse-checkout.
#
# FIX vs the first version: cone-mode sparse-checkout takes
# DIRECTORIES ONLY. The earlier script listed llvm/CMakeLists.txt (a
# file), which made git reject the whole call — leaving a clone with
# git objects but no working tree. This version lists directories
# only and repairs that state.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
# Shared sources root, outside the repo — see
# ../rust_routing/fetch_sources.sh for why (~/Programming/Sources is
# filtered out of Timeshift).
SRC="${PC_SOURCES:-$HOME/Programming/Sources}"
mkdir -p "$SRC"
LP="$SRC/llvm-project"
mkdir -p "$SRC"

say() { printf '\n== %s\n' "$*"; }

# directories the walk-through reads
READ_DIRS=(
  llvm/lib/Target/X86              # X86ISelLowering, DAGToDAG, MCCodeEmitter, *.td
  llvm/lib/CodeGen/SelectionDAG    # the generic ISel machinery
  llvm/include/llvm/CodeGen
  llvm/include/llvm/MC
  llvm/lib/MC
  llvm/include/llvm/Target         # Target.td, TargetSelectionDAG.td
  llvm/include/llvm/IR             # Intrinsics*.td
)

say "llvm-project (sparse, read set)"
if [ ! -d "$LP/.git" ]; then
    git clone --depth 1 --filter=blob:none --sparse \
        https://github.com/llvm/llvm-project.git "$LP"
else
    echo "   clone present"
fi

# repair: clear any stale lock from an interrupted run
rm -f "$LP/.git/info/sparse-checkout.lock" 2>/dev/null || true

git -C "$LP" sparse-checkout set "${READ_DIRS[@]}"
echo "   working tree:"
for d in "${READ_DIRS[@]}"; do
    [ -d "$LP/$d" ] && printf '     ok       %s\n' "$d" \
                    || printf '     MISSING  %s\n' "$d"
done
du -sh "$LP" | sed 's/^/   /'

say "rustc_codegen_llvm + rustc_codegen_ssa"
RUST="$SRC/rust"
if [ -d "$RUST/compiler/rustc_codegen_llvm" ]; then
    echo "   present"
elif [ -d "$RUST/.git" ]; then
    git -C "$RUST" sparse-checkout add \
        compiler/rustc_codegen_llvm compiler/rustc_codegen_ssa
else
    echo "   rust checkout missing — run rust_routing/fetch_sources.sh"
fi

# ---------------------------------------------------------------
[ "$1" != "--tblgen" ] && { say "done (read set only — this is enough
   for the walk-through). Re-run with --tblgen for the matcher .inc
   files needed by the grammar survey."; exit 0; }

say "locating llvm-tblgen"
TBL=""
for cand in llvm-tblgen llvm-tblgen-21 llvm-tblgen-20 llvm-tblgen-19 \
            /usr/lib/llvm-21/bin/llvm-tblgen /usr/lib/llvm-20/bin/llvm-tblgen; do
    if command -v "$cand" >/dev/null 2>&1; then TBL="$(command -v "$cand")"; break; fi
    [ -x "$cand" ] && { TBL="$cand"; break; }
done
[ -x "$SRC/tblgen-build/bin/llvm-tblgen" ] && TBL="$SRC/tblgen-build/bin/llvm-tblgen"

if [ -z "$TBL" ]; then
    echo "   not found on the system."
    echo "   TRY FIRST (cheap):   sudo apt install llvm-21-dev"
    echo "                        (Debian/Ubuntu ship llvm-tblgen there)"
    echo
    read -r -p "   Build it from source instead? Needs the FULL llvm/ tree (~1-2 GB fetch, 10-20 min). [y/N] " yn
    [ "$yn" = "y" ] || { echo "   skipping tblgen step"; exit 0; }
    git -C "$LP" sparse-checkout set llvm
    cmake -S "$LP/llvm" -B "$SRC/tblgen-build" -G Ninja \
          -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD=X86 >/dev/null
    ninja -C "$SRC/tblgen-build" llvm-tblgen
    TBL="$SRC/tblgen-build/bin/llvm-tblgen"
fi
echo "   using: $TBL"

# VERSION PIN. The clone tracks main (LLVM 22-dev); a release
# llvm-tblgen cannot parse main's Target.td (it uses newer TableGen
# operators such as !sort). Check out the tag matching the binary.
TBLVER=$("$TBL" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
if [ -n "$TBLVER" ]; then
    TAG="llvmorg-$TBLVER"
    if ! git -C "$LP" rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
        echo "   pinning sources to $TAG (matches llvm-tblgen)"
        git -C "$LP" fetch --depth 1 origin "refs/tags/$TAG:refs/tags/$TAG" \
            2>/dev/null || {
            echo "   exact tag missing; trying release branch"
            BR="release/${TBLVER%.*.*}.x"
            git -C "$LP" fetch --depth 1 origin "$BR" && \
                git -C "$LP" checkout -q FETCH_HEAD
        }
    fi
    git -C "$LP" checkout -q "$TAG" 2>/dev/null && \
        echo "   sources now at $TAG" || \
        echo "   NOTE: could not pin; tblgen may fail on version skew"
fi

say "generating the ISel matcher + instr info tables"
# NOTE: no -gen-emitter. X86 does not use it; the encoder is
# hand-written C++ (X86MCCodeEmitter.cpp). Confirmed via X86's
# own CMakeLists.txt, survey 2026-07-25.
OUT="$SRC/generated"; mkdir -p "$OUT"
run_tblgen() {   # $1 = -gen-flag, $2 = output name
    "$TBL" "$1" \
        -I "$LP/llvm/lib/Target/X86" -I "$LP/llvm/include" \
        "$LP/llvm/lib/Target/X86/X86.td" -o "$OUT/$2" \
        && printf '   %8s lines  %s\n' "$(wc -l < "$OUT/$2")" "$2" \
        || echo "   FAILED: $2 (needs more .td includes — report the error)"
}
run_tblgen -gen-dag-isel      X86GenDAGISel.inc
run_tblgen -gen-instr-info    X86GenInstrInfo.inc

say "done — run ./check_resources.sh to confirm"
