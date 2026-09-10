#!/bin/bash
# t2_l29_the_reproducing_commands.sh -- task t2, lane 29: the commands
# this task's log offers as reproducing commands, run, so what the log
# pastes under each is what the command prints.
#
# Lane 28's verifier reproduced nothing: every claim carried an
# attribution or prose and no command a reader could run. These are the
# commands, and each is short enough for the verifier's own 20-second
# ceiling and reads only files this task wrote.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=5

i=1
echo "[$i/$total] the word of each target, off the renderers' own tables"
echo '$ python3 -c "..."'
python3 -c "import sys; sys.path.insert(0, 'PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct'); import construct as CONS; print(' '.join('%s=%d' % (t, CONS.word_of(t)) for t in ('c', 'cpp', 'rust', 'go', 'swift')))"
echo

i=2
echo "[$i/$total] the three proof forms, off construct.md"
echo '$ grep -A 6 "^| form | places |" .../construct.md'
grep -A 6 "^| form | places |" "$C/construct.md"
echo

i=3
echo "[$i/$total] the lemma tally, off lemmas_t2.json"
echo '$ python3 -c "..."'
python3 -c "import json, collections; d = json.load(open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/lean/lemmas_t2.json')); t = collections.Counter(r['outcome'] for r in d['theorems']); print('theorems %d;' % len(d['theorems']), '; '.join('%s %d' % (k, t[k]) for k in sorted(t)))"
echo

i=4
echo "[$i/$total] the constructed certificates on the bank, by kind"
echo '$ python3 -c "..."'
python3 -c "import json, collections; t = collections.Counter(); h = open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl'); [t.update([json.loads(l)['kind']]) for l in h if l.strip() and json.loads(l).get('route') == 'constructed' and json.loads(l).get('preferred')]; h.close(); print('; '.join('%s %d' % (k, t[k]) for k in sorted(t)))"
echo

i=5
echo "[$i/$total] the spelling guard over this task's own aggregate"
echo '$ python3 .../check_no_spelling_keys.py .../construct.json'
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py "$C/construct.json"
echo
echo "lane done"
