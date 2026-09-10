#!/usr/bin/env bash
# rv3 lane 9 -- the transcripts the log pastes, each command run once
# inside this instance so the log's blocks are what the verifier will
# re-run.  Nothing here writes.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
AP=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work
total=7

echo "[1/$total] the census"
python3 -c "import json, collections; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/census_rv3.json')); print('sources', len(d['rows']), sorted(collections.Counter(r['outcome'] for r in d['rows']).items())); print('no entry:', sorted((m, d['no_entry_in_the_opcode_table'][m]['lines'], d['no_entry_in_the_opcode_table'][m]['targets']) for m in d['no_entry_in_the_opcode_table']))"

echo "[2/$total] the five new rows against the Sail model"
python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/level0_points_rv3.json')); r=d['rows']; print('rows', len(r), 'outcomes', sorted(set(x['outcome'] for x in r))); print('variants', sum(x['variants'] for x in r), 'points', sum(x['points'] for x in r), 'agree', sum(x['agree'] for x in r), 'disagree', sum(x['disagree'] for x in r))"

echo "[3/$total] the inheritance, per target"
python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; t=collections.defaultdict(collections.Counter); [t[r['target']].update([(r['verdict'] or {}).get('outcome')]) for r in rows]; print(sorted((k, sorted(v.items())) for k, v in t.items()))"

echo "[4/$total] the inheritance, kinds, rv2 beside rv3"
python3 -c "import json, collections; old=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64.jsonl')]; new=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; print('rv2', sorted(collections.Counter(r['kind'] for r in old).items())); print('rv3', sorted(collections.Counter(r['kind'] for r in new).items()))"

echo "[5/$total] the cells, and the union with rv2's own loop"
python3 -c "
import json
RV='PseudoCoupHQ/Research/oracle/riscv'
def cells(path):
    out=set()
    for line in open(path):
        line=line.strip()
        if not line: continue
        r=json.loads(line)
        if r['kind']!='proved': continue
        c=r['cell']; out.add((c.get('mnem'),c.get('shape'),c.get('key_width')))
    return out
a=cells(RV+'/certificates_riscv64.jsonl'); b=cells(RV+'/certificates_riscv64_rv3.jsonl'); l=cells(RV+'/rv_loop.jsonl')
print('inherited rv2',len(a),'inherited rv3',len(b),'loop rv2',len(l))
print('union rv2',len(a|l),'union rv3 inheritance + rv2 loop',len(b|l))
print('gained',sorted(b-a),'lost',sorted(a-b))
"

echo "[6/$total] the whole-place reading on the proved rows"
python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; p=[r for r in rows if r['kind']=='proved']; print('proved at key_width', len(p), 'at the whole place', sorted(collections.Counter((r.get('verdict_at_the_whole_place') or {}).get('outcome') for r in p).items()))"

echo "[7/$total] the bank, before this task appends anything"
python3 -c "import json, collections; n=0; a=collections.Counter(); [ (n:=n) for _ in ()]; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl') if l.strip()]; print('records', len(rows), 'by arch', sorted(collections.Counter(str(r.get('arch')) for r in rows).items()))"

echo "lane rv3_l9 done"
