#!/usr/bin/env bash
# R1 checks 1-2: reproducibility + internal consistency of the
# PCv5 intentions data. Runnable on host or sandbox:
#   bash run_checks.sh
# Writes logs to ./runs/ (this folder). Read-only w.r.t. git state:
# regenerates in the PCv5 working tree, diffs against HEAD, and
# restores the tree afterwards.

set -u
PCV5=PseudoCoup_v5
DESIGN="$PCV5/Designing"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/runs"
mkdir -p "$OUT"
PASS1=1; PASS1B=1

echo "== R1 check 1: byte-identical regeneration =="

# 1a. pc_verdicts.json
( cd "$DESIGN" && python3 build_verdicts.py ) \
    > "$OUT/build_verdicts.stdout" 2> "$OUT/build_verdicts.stderr" \
    || { echo "  build_verdicts.py FAILED to run (see runs/build_verdicts.stderr)"; PASS1=0; }
if git -C "$PCV5" diff --exit-code -- Designing/pc_verdicts.json \
    > "$OUT/pc_verdicts.diff" 2>&1; then
    echo "  pc_verdicts.json: byte-identical to HEAD — PASS"
else
    echo "  pc_verdicts.json: DIFFERS from HEAD — FAIL (runs/pc_verdicts.diff)"
    PASS1=0
fi

# 1b. intention_tables.html
( cd "$DESIGN" && python3 intention_tables_gen.py ) \
    > "$OUT/tables_gen.stdout" 2> "$OUT/tables_gen.stderr" \
    || { echo "  intention_tables_gen.py FAILED to run (see runs/tables_gen.stderr)"; PASS1B=0; }
if git -C "$PCV5" diff --exit-code -- Designing/intention_tables.html \
    > "$OUT/intention_tables.diff" 2>&1; then
    echo "  intention_tables.html: byte-identical to HEAD — PASS"
else
    echo "  intention_tables.html: DIFFERS from HEAD — FAIL (runs/intention_tables.diff)"
    PASS1B=0
fi

# restore the PCv5 tree exactly as found
git -C "$PCV5" checkout -- Designing/pc_verdicts.json Designing/intention_tables.html 2>/dev/null

echo
echo "== R1 check 2: internal consistency (counts/completeness) =="
python3 - "$DESIGN/pc_verdicts.json" <<'EOF' | tee "$OUT/consistency.txt"
import json, sys
d = json.load(open(sys.argv[1]))
def size(v):
    return len(v) if hasattr(v, "__len__") else v
for k, v in d.items():
    print(f"  {k}: {type(v).__name__} size={size(v)}")
# expected from the PCv5 record: 45 compat pairs, 108 basis cells,
# 11 border-lattice entries — locate and check whatever fields hold them
def count_cells(obj):
    if isinstance(obj, dict):
        return sum(count_cells(v) for v in obj.values()) or len(obj)
    if isinstance(obj, list):
        return len(obj)
    return 1
print("  (interpret against expected 45 / 108 / 11 in REPORT.md)")
EOF

echo
if [ "$PASS1" -eq 1 ] && [ "$PASS1B" -eq 1 ]; then
    echo "CHECK 1 PASS (both artifacts reproduce byte-identically)"
else
    echo "CHECK 1 FAIL — see runs/ diffs"
fi
echo "Check 2 output in runs/consistency.txt — interpretation goes in REPORT.md."
echo "Checks 3-4 are scripted separately after 1-2 pass."
