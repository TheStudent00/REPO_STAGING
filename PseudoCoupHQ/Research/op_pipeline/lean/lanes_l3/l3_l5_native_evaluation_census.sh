#!/bin/bash
# l3 lane 5 -- WHERE THE NATIVE-EVALUATION TRUST ACTUALLY COMES FROM, read off
# the artifacts and off the toolchain, before anything is re-proved.
#   (a) does any theorem in this project use `native_decide` as its tactic?
#   (b) the axioms line of every proved row of the check, by tactic;
#   (c) the same for task L1's own edge theorems;
#   (d) what the installed Lean says about `bv_decide` and `ofReduceBool`:
#       the tactic's own sources in the toolchain, and its configuration
#       fields, so a way to close a goal WITHOUT the native-evaluation axiom
#       is read rather than guessed at.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/6] every tactic word in every .lean file of the project"
grep -rho "native_decide\|bv_decide\|decide\b\|ofReduceBool" \
     archproof/Archproof archproof/Edges archproof/Main.lean \
     archproof/Archproof.lean 2>/dev/null | sort | uniq -c

echo "[2/6] the check's proved rows, axioms by tactic"
python3 -c "
import collections, json, re
d = json.load(open('$LEANDIR/check_L2.json'))
proved = [r for r in d['rows'] if r.get('closed_by')]
print('   proved rows %d' % len(proved))
print('   missing axioms %d' % sum(1 for r in proved if not r.get('axioms')))
print('   sorryAx %d' % sum(1 for r in proved if 'sorryAx' in (r.get('axioms') or '')))
pats = collections.Counter()
for r in proved:
    a = re.sub(chr(39) + '[^' + chr(39) + ']+' + chr(39), 'THEOREM', r['axioms'] or '(none recorded)')
    pats[(r['closed_by'], a)] += 1
for k in sorted(pats, key=str):
    print('   %4d  %s' % (pats[k], k))
print('   rows carrying Lean.ofReduceBool: %d'
      % sum(1 for r in proved if 'ofReduceBool' in (r.get('axioms') or '')))
"

echo "[3/6] task L1's own edge results, and any axioms they recorded"
python3 -c "
import json, os
for name in ('L1_ten_edges.json', 'L1_three_undecided.json',
             'L1_divide_ladder.json', 'L1_divide_ladder_t600.json',
             'L1_edges_selected.json'):
    path = os.path.join('$LEANDIR', name)
    d = json.load(open(path))
    print('   %-28s top-level keys %s' % (name, sorted(d) if isinstance(d, dict) else type(d).__name__))
    rows = d.get('rows') if isinstance(d, dict) else None
    if isinstance(rows, list):
        for r in rows[:40]:
            print('      %s' % {k: r[k] for k in sorted(r) if k in
                                ('name','outcome','tactic','axioms','wall_seconds','peak_kb','bits')})
"

echo "[4/6] the axioms of L1's Edges theorems, as the files stand"
grep -rn "print axioms\|by " archproof/Edges/*.lean 2>/dev/null | head -40

echo "[5/6] where the toolchain keeps bv_decide, and what mentions ofReduceBool"
elan show 2>/dev/null | head -5
TC=$(dirname $(dirname $(readlink -f $(command -v lean))))
echo "   toolchain root: $TC"
find "$TC" -name '*.lean' -path '*BVDecide*' 2>/dev/null | head -30
echo "   --- files under the toolchain naming ofReduceBool ---"
grep -rl "ofReduceBool" "$TC" --include='*.lean' 2>/dev/null | head -20

echo "[6/6] bv_decide's own configuration fields, LITERAL"
find "$TC" -name 'Basic.lean' -path '*BVDecide*' 2>/dev/null | head -5
grep -rn "structure BVDecideConfig" -A 60 "$TC" --include='*.lean' 2>/dev/null | head -90
echo "--- exit $?"
