#!/usr/bin/env bash
# Fetches the rustc source the slices are cut from, and reports an
# inventory. Run on the host from this folder:
#
#   bash ~/Programming/PseudoCoup_v5/Research/rust_routing/fetch_sources.sh
#
#   rustc codegen — a sparse checkout of rust-lang/rust (~50 MB, not
#   ~1 GB). Directories are added by
#   ~/Programming/PseudoCoup_v5/Research/llvm_trace/fetch_llvm.sh as it
#   needs them.
#
# 2026-08-02: a second step was removed from this script by a standing
# prohibition — see ~/Programming/PseudoCoupHQ/CRANELIFT_IS_BANNED.md.
# It fetched and built a banned backend. Nothing here fetches it now,
# and nothing here may fetch it again.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
# Language sources live OUTSIDE the repo, in one shared folder:
# ~/Programming/Sources (the owner, 2026-08-02). That folder is filtered out
# of Timeshift, so multi-hundred-MB upstream checkouts are not carried
# into system snapshots. Every fetcher in this repo writes here.
SRC="${PC_SOURCES:-$HOME/Programming/Sources}"
mkdir -p "$SRC"
echo "== sources root: $SRC"

# The pre-2026-08-02 location was this folder's own `sources/`. If one
# is still there, say so rather than silently fetching a second copy.
if [ -d "$HERE/sources" ]; then
    echo "   NOTE: an old checkout is still at $HERE/sources"
    echo "         move or delete it; nothing reads it now."
fi

echo "== rustc (sparse checkout)"
if [ ! -d "$SRC/rust" ]; then
    git clone --depth 1 --filter=blob:none --sparse \
        https://github.com/rust-lang/rust.git "$SRC/rust"
    git -C "$SRC/rust" sparse-checkout set \
        compiler/rustc_codegen_ssa compiler/rustc_codegen_llvm
else
    echo "   present"
fi

echo
echo "== inventory (path | lines) ============================"
inv() {
    for f in $1; do
        [ -f "$f" ] && printf '%8s  %s\n' "$(wc -l < "$f")" \
            "${f#$SRC/}"
    done
}
CG="$SRC/rust/compiler"
echo "-- MIR -> LLVM IR routing"
inv "$CG/rustc_codegen_ssa/src/mir/rvalue.rs"
inv "$CG/rustc_codegen_llvm/src/builder.rs"
inv "$CG/rustc_codegen_llvm/src/declare.rs"

echo
echo "Share this output (or: bash ~/Programming/PseudoCoup_v5/Research/rust_routing/fetch_sources.sh > fetch_report.txt)"
