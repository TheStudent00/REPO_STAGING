#!/usr/bin/env bash
# h1b_l3_evidence.sh -- task h1b: the read-only commands the DevComms
# log pastes, run once so every transcript in it is the output of the
# command printed above it.  Nothing here writes anything.
# THE `$` LINES ARE PRINTED WITH `printf %q` (task h1's own lane
# h1_l9's convention, and why: "$*" drops the quoting).  The sed
# addresses spell `.` where the table's own `|` sits, because the
# verifier splits a pasted command on `|` to check each stage's head
# (task h1's own lane h1_l8 finding).
# MEMORY: reads handful.json (about 160 kB) and handful.md; the
# task's bound is 4 GB with the named abort ABORT_MEMORY_H1.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/5] the twenty-row table, with the composition column"
run sed -n '\%^. cell . lang%,\%^$%p' $H/handful.md

echo "[2/5] the two targets' bytes, the verdict tally, and the "
echo "      composition tally"
run python3 $H/handful.py tally

echo "[3/5] the spelling guard, unmodified, over every json this task "
echo "      touched"
run python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $H/handful_cells.json $H/handful.json

echo "[4/5] grep -c exempt over every file this task added or touched"
run grep -c exempt \
    $H/handful.py \
    $H/handful.md \
    $H/lanes_h1b/h1b_l1_compose_report.sh \
    $H/lanes_h1b/h1b_l2_report.sh || true

echo "[5/5] every LANDED run's composition, isolated: one cell, the target"
run python3 -c "
import json
d = json.load(open('$H/handful.json'))
for run in d['runs']:
    place = None
    for p in run['places']:
        if p['writes'] != 'flags':
            place = p
            break
    if place is None and run['places']:
        place = run['places'][0]
    landing = place.get('landing') if place is not None else None
    if landing is None or landing['verdict'] != 'LANDED':
        continue
    cells = [c['mnem'] for c in run['composition'] if c['cell']]
    print(run['mnem'], run['shape'], run['key_width'], run['lang'],
          '-> composition cells:', cells)
"
