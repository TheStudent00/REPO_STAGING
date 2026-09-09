#!/bin/bash
# o10_l6_recheck.sh -- task o10: re-run the two commands the log
# pastes verbatim, from /projects/PseudoCoupHQ (the verifier's own
# cwd), to get their exact, re-pasteable output.
set -euo pipefail
cd /projects/PseudoCoupHQ
echo "[1/2] task o10: grand total, from PseudoCoupHQ root"
python3 -c "
import json, glob
total=0
for f in ['Research/op_pipeline/canon40_wrapped_c.json',
          'Research/op_pipeline/canon40_wrapped_cpp.json',
          'Research/op_pipeline/canon40_wrapped_go.json',
          'Research/op_pipeline/canon40_wrapped_rust.json',
          'Research/op_pipeline/canon40_wrapped_swift.json',
          'Research/op_pipeline/canon40_interp.json']:
    d=json.load(open(f)); total+=len(d['units'])
regen=sum(len(json.load(open(f))['units'])
          for f in glob.glob('Research/op_pipeline/canon40_regen_store/*.json'))
print('grand total', total+regen)
"
echo "[2/2] task o10: sign-sensitive pairs sample, from PseudoCoupHQ root"
python3 -c "
import json
d = json.load(open('Research/oracle/arch_opcodes/signatures/ledger_signatures.json'))
pairs = d['reading_kinds']['sign_sensitive_pairs']
sample = pairs[:2] + [p for p in pairs
                      if 'addsd' in (p['mnemonic_a'], p['mnemonic_b'])]
for p in sample:
    print(p['mnemonic_a'] + ' ' + p['mnemonic_b'] + ' ' +
          str(p['shared_families']) + ' ' + str(p['example_signature_swap']))
"
echo "[2/2] done"
