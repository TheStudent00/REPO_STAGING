#!/bin/bash
# task o11, lane 14: the remaining evidence blocks -- the coverage
# table's own class summary, the three literal examples, and the two
# per-opcode tables that are not LANDED.
set -u
export PATH=/opt/cargo/bin:$PATH
R=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/rust

run() {
  echo "\$ $1"
  eval "$1"
  echo
}

echo "[1/6] the coverage table's own class summary"
run "grep '^Rust cells' $R/rust_report.md"

echo "[2/6] example: collapsed to byte identity"
run "sed -n '/^### 3.1/,/^### 3.2/p' $R/rust_report.md"

echo "[3/6] example: proved, not byte-identical"
run "sed -n '/^### 3.2/,/^### 3.3/p' $R/rust_report.md"

echo "[4/6] example: disproved, with seeds"
run "sed -n '/^### 3.3/,/^## 4\\./p' $R/rust_report.md"

echo "[5/6] LANDED_ELSEWHERE"
run "sed -n '/^### LANDED_ELSEWHERE/,/^### NOT_COLLAPSED/p' $R/rust_report.md"

echo "[6/6] NOT_COLLAPSED"
run "sed -n '/^### NOT_COLLAPSED/,/^## 8\\./p' $R/rust_report.md"
echo "lane o11_l14 done"
