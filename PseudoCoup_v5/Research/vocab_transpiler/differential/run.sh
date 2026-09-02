#!/usr/bin/env bash
# Orchestrates the differential test suite.
#
# Full mode (requires a Rust toolchain -- `cargo` on PATH):
#   ./run.sh
#
# Python-only mode (what this sandbox can actually do -- no cargo here):
#   ./run.sh --python-only
#
# Full mode:
#   1. gen_rust_harness.py   -> writes harness/src/main.rs, harness/Cargo.toml, SKIPPED_RUST.txt
#   2. cargo run --release   -> harness_out.txt
#   3. run_python_side.py    -> python_out.txt
#   4. compare.py            -> report.txt   (nonzero exit if any byte mismatch)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

PYTHON_ONLY=0
for arg in "$@"; do
    case "$arg" in
        --python-only) PYTHON_ONLY=1 ;;
        *) echo "unknown argument: $arg" >&2; exit 2 ;;
    esac
done

echo "== step 1/4: gen_rust_harness.py =="
python3 gen_rust_harness.py

if [ "$PYTHON_ONLY" -eq 0 ]; then
    if ! command -v cargo >/dev/null 2>&1; then
        echo ""
        echo "ERROR: cargo not found. This step must be run by someone with a Rust"
        echo "toolchain (see README.md -- ask the owner). Re-run with --python-only to"
        echo "regenerate python_out.txt only."
        echo ""
        exit 1
    fi

    echo "== step 2/4: cargo run --release (harness) =="
    (cd harness && cargo run --release) > harness_out.txt

else
    echo "== step 2/4: skipped (--python-only); harness_out.txt left as-is =="
fi

echo "== step 3/4: run_python_side.py =="
python3 run_python_side.py > python_out.txt

echo "== step 4/4: compare.py =="
python3 compare.py
