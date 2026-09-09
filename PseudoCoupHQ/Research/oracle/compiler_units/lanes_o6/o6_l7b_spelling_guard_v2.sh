#!/usr/bin/env bash
# task o6 lane 7b (resume, over the second build's files): the unmodified
# spelling guard over every json this task wrote -- the deliverable sites
# file (decompressed to /work first: the guard reads plain json; the
# document is the same), the join json, the package-shape cost record --
# and the count of the forbidden annotation word over every file this
# task added (0 each; this lane's own grep pattern is the one place the
# word appears, shown by line so the count is read against it).
set -uo pipefail
CU=PseudoCoupHQ/Research/oracle/compiler_units
mkdir -p /work/o6
echo "[1/3] decompress go_types_sites.json.gz to /work (same document, plain json for the guard)"
gzip -dc "$CU/go_types_sites.json.gz" > /work/o6/go_types_sites.json; ls -l /work/o6/go_types_sites.json
echo "[2/3] check_no_spelling_keys.py over the three json files"
for f in /work/o6/go_types_sites.json "$CU/go_types_join.json" "$CU/go_types_package_shape_cost.json"; do
  python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py "$f"; echo "guard exit for $(basename $f): $?"
done
echo "[3/3] the annotation-word count over every file this task added (the lane scripts included)"
grep -c exempt "$CU/go_types_oracle.go" "$CU/go_types_join.py" "$CU/go_types_join.json" "$CU/go_types_report.md" "$CU/go_types_package_shape_cost.json" /work/o6/go_types_sites.json "$CU"/lanes_o6/*.sh
echo "the lines that carry the word, LITERAL (expected: only this lane's own grep commands):"
grep -n exempt "$CU"/lanes_o6/*.sh
echo "[3/3] done"
