#!/usr/bin/env bash
# Runs the syn_shim demo against the vendored corpus.
#
#   bash ~/Programming/PseudoCoup_v5/Research/syn_shim/run.sh
#
# Needs: pip install tree-sitter==0.26.0 tree-sitter-rust==0.24.2
# Corpus: ~/Programming/Sources/rust (override with PC_SOURCES)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="${PC_SOURCES:-$HOME/Programming/Sources}"
F="$SRC/rust/compiler/rustc_codegen_llvm/src/coverageinfo/mapgen.rs"

[ -f "$F" ] || { echo "corpus missing: $F"; exit 1; }

python3 - "$F" "$HERE/real_enum.rs" <<'EOF'
import re, sys
src = open(sys.argv[1], errors="replace").read()
m = re.search(r'#\[derive\([^)]*TryFromU32[^)]*\)\]\s*(?:#\[[^\]]*\]\s*)*'
              r'((?:pub\s+)?enum\s+\w+\s*\{[^}]*\})', src, re.S)
if not m:
    sys.exit("no derive(TryFromU32) enum found")
open(sys.argv[2], "w").write(m.group(1))
EOF

python3 "$HERE/derive_try_from_u32.py" "$HERE/real_enum.rs"
