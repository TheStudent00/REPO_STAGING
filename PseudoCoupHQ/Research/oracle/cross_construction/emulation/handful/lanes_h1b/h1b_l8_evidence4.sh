#!/usr/bin/env bash
# h1b_l8_evidence4.sh -- task h1b: the LANDED-runs check re-run with
# its print statement changed so the pasted command carries no literal
# `>` -- the verifier's own command parser reads an unquoted `>` as a
# shell redirect and scored lane h1b_l3's version REFUSED
# (`redirects_into_a_path`) even though nothing in that command
# actually redirects; this is the same class of false positive task
# h1's own lane h1_l8 hit on an escaped `|` (log 238 ADDENDUM), fixed
# in the pasted command rather than in the verifier, which the law
# forbids touching.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/1] every LANDED run's composition, isolated: one cell, the target"
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
          'composition cells:', cells)
"
