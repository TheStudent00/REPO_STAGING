#!/bin/bash
# t4_l30_the_transcripts.sh -- task t4, lane 30: the six commands whose
# output the log pastes as a SHELL TRANSCRIPT, run here so the paste is
# the output and not a retyping of it.
#
# The conventions verifier re-runs a `$ ` line and compares; a claim
# with no `$ ` line is UNVERIFIABLE by its own definition. Lane 29 found
# 20 of 20 claims in this log UNVERIFIABLE and zero DIFFERS, which is
# the law's own bar and no more; these six are what it can actually
# re-run.
#
#   [1/2] the six commands, each with its output
#   [2/2] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
A=$P/Research/oracle/cross_construction/emulation/autopoly
total=2

i=1
echo "[$i/$total] the six commands, each with its output"
echo ""

echo '$ sha256sum PseudoCoupHQ/Research/op_pipeline/reference.py'
sha256sum PseudoCoupHQ/Research/op_pipeline/reference.py
echo ""

echo '$ wc -l PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t4_general_runs.jsonl'
wc -l PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/t4_general_runs.jsonl
echo ""

echo '$ python3 -c "import json;d=json.load(open(\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/construction_proofs.json\"));print(d[\"meta\"][\"forms\"])"'
python3 -c "import json;d=json.load(open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/construction_proofs.json'));print(d['meta']['forms'])"
echo ""

echo '$ python3 -c "import json;d=json.load(open(\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/kind_census.json\"));print(len(d[\"rows\"]))"'
python3 -c "import json;d=json.load(open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/kind_census.json'));print(len(d['rows']))"
echo ""

echo '$ python3 -c "import json,collections;rows=[];[rows.extend(json.load(open(p))[\"rows\"]) for p in [\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lemmas_t4_1_of_2.json\",\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lemmas_t4_2_of_2.json\"]];print(sorted(collections.Counter(r[\"outcome\"] for r in rows).items()))"'
python3 -c "import json,collections;rows=[];[rows.extend(json.load(open(p))['rows']) for p in ['PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lemmas_t4_1_of_2.json','PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/lemmas_t4_2_of_2.json']];print(sorted(collections.Counter(r['outcome'] for r in rows).items()))"
echo ""

echo '$ python3 -c "import json,collections;rows=[json.loads(l) for l in open(\"PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/rv_general.jsonl\")];print(sorted(collections.Counter(r[\"kind\"] for r in rows).items()))"'
python3 -c "import json,collections;rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/rv_general.jsonl')];print(sorted(collections.Counter(r['kind'] for r in rows).items()))"
echo ""

i=2
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
