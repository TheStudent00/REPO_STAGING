#!/usr/bin/env bash
# ref1 lane 14 -- the check over the first twenty matched variants, the
# sample the brief asks for before any bulk run: peak RSS, wall clock, and
# every outcome, so the shape of the answer is seen before the whole set.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
total=2

echo "[1/$total] twenty variants, three solver processes"
cd $L0
python3 level0_check.py $S $L0/key_map.json \
    /tmp/level0_sample.json /tmp/level0_sample.md --limit=20 --workers=3

echo "[2/$total] every place of those twenty, one line each"
python3 -c "
import json
d = json.load(open('/tmp/level0_sample.json'))
for v in d['variants']:
    for p in v['places']:
        print('%-22s %-14s %-10s %s' % (v['variant'], p['place'],
              p['outcome'], (p.get('reason') or '')[:90]))
"
