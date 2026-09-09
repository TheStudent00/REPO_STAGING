#!/usr/bin/env bash
# task o6 lane 7 (resume): the unmodified spelling guard over every json
# this task wrote -- the deliverable sites file (decompressed to /work
# first: the guard reads plain json; the document is the same), the join
# json, the package-shape cost record -- and `grep -c exempt` over every
# file this task added (must be 0 each).
set -uo pipefail
CU=PseudoCoupHQ/Research/oracle/compiler_units
mkdir -p /work/o6
echo "[1/3] decompress go_types_sites.json.gz to /work (same document, plain json for the guard)"
gzip -dc "$CU/go_types_sites.json.gz" > /work/o6/go_types_sites.json; ls -l /work/o6/go_types_sites.json
echo "[2/3] check_no_spelling_keys.py over the three json files"
for f in /work/o6/go_types_sites.json "$CU/go_types_join.json" "$CU/go_types_package_shape_cost.json"; do
  python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py "$f"; echo "guard exit for $(basename $f): $?"
done
echo "[3/3] grep -c exempt over every file this task added"
grep -c exempt "$CU/go_types_oracle.go" "$CU/go_types_join.py" "$CU/go_types_join.json" "$CU/go_types_report.md" "$CU/go_types_package_shape_cost.json" /work/o6/go_types_sites.json "$CU"/lanes_o6/*.sh
echo "[3/3] done"
