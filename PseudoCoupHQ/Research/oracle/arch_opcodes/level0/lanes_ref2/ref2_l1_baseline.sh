#!/bin/bash
# ref2 lane 1 -- THE BASELINE, before a single character of the reference
# changes.  Reproduces task ref1's level-0 check into a NEW pair of files
# beside ref1's (nothing overwritten), prints the four defect sites of
# `reference.py` and `condition_table.py` LITERAL, prints the L2 check's
# tally as it stands on disk (259 / 172 / 87), and records the sha256 pair
# that is this task's new `reference_version` field at its BEFORE value.
#
# Memory bound: 6 GB for this lane (the check's own peak was 64 MB at ref1);
# named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"

echo "[1/7] the tools this task needs, and where"
python3 -c "import z3; print('z3', z3.get_version_string())"
which lake lean 2>&1 | sed 's/^/  /'
ls "$OP/lean/archproof" | head -5
echo "--- exit $?"

echo "[2/7] the reference_version BEFORE: sha256 of the two files this task may change"
sha256sum "$OP/reference.py" "$OP/condition_table.py"
echo "--- exit $?"

echo "[3/7] defect 1 LITERAL -- reference.full64"
sed -n '204,213p' "$OP/reference.py"
echo "[3/7] defect 2 LITERAL -- reference.build_carry_binary"
sed -n '968,982p' "$OP/reference.py"
echo "[3/7] defect 3 LITERAL -- condition_table.cond_to_z3, its first four lines"
sed -n '253,258p' "$OP/condition_table.py"
echo "[3/7] defect 4 LITERAL -- reference.WIDTH_IS_NOT_A_SUFFIX"
sed -n '640,652p' "$OP/reference.py"
echo "--- exit $?"

echo "[4/7] the 34 size-lettered mnemonics the width rule reads as suffixed"
python3 -c "
import sys
sys.path.insert(0, '$OP')
import reference as R
names = [m for m in R.REFERENCE.opcode_table.entries
         if m[-1:] in R.SIZE_LETTER and m not in R.WIDTH_IS_NOT_A_SUFFIX]
print('count %d' % len(names))
for name in sorted(names):
    print('  %s' % name)
"
echo "--- exit $?"

echo "[5/7] the level-0 check re-run as the reference stands -- level0_check_ref2_before.json"
cd "$L0" || exit 1
python3 level0_check.py /sources/X86-64-semantics/semantics \
    "$L0/key_map.json" \
    "$L0/level0_check_ref2_before.json" \
    "$L0/level0_check_ref2_before.md" --workers=3
echo "--- exit $?"

echo "[6/7] the L2 check's tally as check_L2.json stands on disk"
python3 -c "
import collections, json
d = json.load(open('$OP/lean/check_L2.json'))
rows = d['rows']
print('rows %d' % len(rows))
print('STATED %d' % sum(1 for r in rows if r['outcome'] == 'STATED'))
print('REFUSED %d' % sum(1 for r in rows if r['outcome'] == 'REFUSED'))
print('DISCREPANCY %d' % sum(1 for r in rows if r['outcome'] == 'DISCREPANCY'))
t = collections.Counter()
for r in rows:
    t[r.get('closed_by') or r.get('outcome')] += 1
for k in sorted(t, key=str):
    print('  %-16s %d' % (k, t[k]))
"
echo "--- exit $?"

echo "[7/7] the populations this task re-derives, counted before it starts"
python3 -c "
import glob, json, os, resource
shards = sorted(glob.glob('$OP/term66_store/*.json'))
print('term66_store shards %d' % len(shards))
d = json.load(open('$OP/certificates_probe.json')) if False else None
lines = 0
with open('$HQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl') as handle:
    for line in handle:
        if line.strip():
            lines = lines + 1
print('certificates.jsonl entries %d' % lines)
print('peak RSS %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"
echo "--- exit $?"
