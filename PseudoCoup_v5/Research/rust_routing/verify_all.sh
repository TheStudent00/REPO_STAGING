#!/usr/bin/env bash
# Runs the whole rust_routing proof chain, incl. the rustc diff.
cd "$(dirname "$0")" || exit 1
set -e

for t in test_output_ring.py test_slice_routing.py test_end_to_end.py \
         test_hub_module.py; do
    echo "===== $t"
    python3 "$t" | tail -3
done

echo "===== grid vs native rustc"
if command -v rustc >/dev/null; then
    rustc -O ground_truth.rs -o /tmp/pc_gt 2>/dev/null
    /tmp/pc_gt > /tmp/pc_rs.txt
    python3 verify_vs_rustc.py > /tmp/pc_py.txt
    if diff -q /tmp/pc_rs.txt /tmp/pc_py.txt >/dev/null; then
        echo "PASS: $(wc -l < /tmp/pc_rs.txt) rows byte-identical to rustc"
    else
        echo "FAIL: differences vs rustc"; diff /tmp/pc_rs.txt /tmp/pc_py.txt | head
        exit 1
    fi
else
    echo "skipped (no rustc in this environment)"
fi
