#!/usr/bin/env bash
# rv3 lane 11 -- four more transcripts, so that four claims the first
# verifier pass could only cite now carry a command to re-run.  Nothing
# here writes.
set -u
export HOME=/work
total=4

echo "[1/$total] the census's own no-entry table, from the artifact"
python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/census_rv3.json'))['no_entry_in_the_opcode_table']; [print('%-10s lines %3d  sources %3d  targets %s' % (m, d[m]['lines'], d[m]['sources'], ','.join(d[m]['targets']))) for m in sorted(d, key=lambda k: -d[k]['lines'])]"

echo "[2/$total] the two mnemonics task rv2's own loop store refused on"
python3 -c "import json, re; seen={}; [seen.setdefault(re.search(chr(39)+'([a-z0-9.]+)'+chr(39), (json.loads(l).get('verdict') or {}).get('reason') or '').group(1), ((json.loads(l).get('verdict') or {}).get('reason') or '')[:96]) for l in open('PseudoCoupHQ/Research/oracle/riscv/rv_loop.jsonl') if 'no entry in the riscv opcode table' in ((json.loads(l).get('verdict') or {}).get('reason') or '')]; [print(seen[m]) for m in sorted(seen) if m in ('bseti', 'fsgnjn.d')]"

echo "[3/$total] every refusal left in the re-run, with its cause"
python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; r=[x for x in rows if x['kind']=='refused']; print('refused', len(r), sorted(collections.Counter((x['target'], (x['verdict'] or {}).get('outcome')) for x in r).items()))"

echo "[4/$total] the rust rows the re-run produced"
python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64_rv3.jsonl')]; r=[x for x in rows if x['target']=='rust']; print('rust rows', len(r), sorted(collections.Counter(x['kind'] for x in r).items()), 'compiler', sorted(set((x.get('compiler') or {}).get('target_triple') for x in r)))"

echo "lane rv3_l11 done"
