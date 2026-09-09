#!/usr/bin/env bash
# t97 lane 14 -- the ceiling ladder for one of the 44, printed off the
# three pass artifacts rather than off a lane log, so the evidence
# carries no transcript arrow and can be re-run as it stands.
set -u
python3 -c "
import json, glob
want = 'c/regen_1859'
rows = []
for p in sorted(glob.glob('/projects/PseudoCoupHQ/Research/op_pipeline/term97_flagged_slice*.json')):
    for r in json.load(open(p))['flagged']:
        if r['unit'] == want:
            rows.append(('pass 1', r['pass1_ceiling_mb'], r['pass1_child_peak_kb'], r['pass1_wall_seconds'], r['pass1_word']))
for p in sorted(glob.glob('/projects/PseudoCoupHQ/Research/op_pipeline/term97_pass2_*.json')):
    for r in json.load(open(p))['rows']:
        if r['unit'] == want:
            rows.append(('pass 2', r['pass2_ceiling_mb'], r['pass2_child_peak_kb'], r['pass2_wall_seconds'], r['pass2_word']))
print('the ceiling ladder for %s' % want)
for one in rows:
    print('   %-7s ceiling %6d MB   peak %9d kB   wall %6.2f s   %s' % one)
"
