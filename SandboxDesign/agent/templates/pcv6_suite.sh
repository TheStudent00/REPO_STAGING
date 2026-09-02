#!/usr/bin/env bash
# Run the full PseudoCoup_v6 tool suite against the read-only project mounts.
#
# Template — copy its text into agent/drop/<name>.sh to run it. Products and a
# copy of the summary land in /out; the daemon records the exit code in
# /status/<name>.sh.status.
#
# Toolchain pins are the ones of record in
# <WORKSPACE_DIR>/PseudoCoup_v6/Tools/tree_sitter_base/pins/MANIFEST.md.
set -uo pipefail

PCV6=/projects/PseudoCoup_v6
export PCV5_ROOT=/projects/PseudoCoup_v5

echo "== free space on /work before: $(df -Pm /work | awk 'NR==2{print $4" MB"}')"
echo "== suite: PseudoCoup_v6 Tools (read-only mount)"

cd "$PCV6"
uv run --no-project --python 3.13 \
    --with pytest \
    --with tree-sitter==0.26.0 \
    --with tree-sitter-python==0.25.0 \
    --with tree-sitter-rust==0.24.2 \
    --with tree-sitter-cpp==0.23.4 \
    pytest Tools -q 2>&1 | tee /out/pcv6_suite.txt
rc=${PIPESTATUS[0]}

echo "== free space on /work after:  $(df -Pm /work | awk 'NR==2{print $4" MB"}')"
echo "== pytest exit: $rc"
exit "$rc"
