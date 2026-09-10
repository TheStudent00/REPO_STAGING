#!/bin/bash
# ref2 lane 10 -- the term walk's own tail, and the attribution.
#
#   * 184 units were still short after pass 2 at 6,144 MB.  LAW: a memory
#     ceiling is a FLAG, not an answer -- so they are run again at 10,240 MB
#     with ONE worker, through the SAME `run_pass2`, and whether the answer
#     changed is reported.  This is task t104's own remedy (log_233 section 4
#     item 1) with this task's paths.
#   * then every unit whose layer-5 text moved is walked again at each earlier
#     state of the reference, so the correction that moved it can be NAMED
#     rather than guessed.
#
# Memory bound: 12 GB, named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"
cd "$L0" || exit 1

echo "[1/6] the 184 still short, at 10,240 MB and one worker"
python3 "$L0/ref2_term_walk.py" retry 10240 900
echo "--- exit $?"

echo "[2/6] the moved units at the state after correction 1"
python3 "$L0/ref2_term_walk.py" attribute c1 | tail -4
echo "--- exit $?"

echo "[3/6] the moved units at the state after correction 2"
python3 "$L0/ref2_term_walk.py" attribute c2 | tail -4
echo "--- exit $?"

echo "[4/6] the moved units at the state after correction 3"
python3 "$L0/ref2_term_walk.py" attribute c3 | tail -4
echo "--- exit $?"

echo "[5/6] the moved units, joined and attributed"
python3 "$L0/ref2_term_walk.py" report "$L0/ref2_term_moved.json"
echo "--- exit $?"

echo "[6/6] the two stores, counted, and the guard over what this lane wrote"
python3 -c "
import glob, json, os
def count(folder):
    units = 0
    texts = 0
    for path in sorted(glob.glob(os.path.join(folder, '*.json'))):
        handle = open(path)
        document = json.load(handle)
        handle.close()
        units = units + len(document['units'])
        for name in document['units']:
            if document['units'][name].get('layer5_normalized_text'):
                texts = texts + 1
    return units, texts
for folder in ('$OP/term66_store', '$OP/term_ref2_store'):
    units, texts = count(folder)
    print('%-24s %6d records, %6d with a layer-5 text'
          % (os.path.basename(folder), units, texts))
"
python3 "$OP/check_no_spelling_keys.py" \
    "$L0/ref2_term_audit.json" "$L0/ref2_term_moved.json" \
    "$L0/ref2_term_walk_evidence.json" "$L0/ref2_term_walk_state.json" \
    "$L0/ref2_term_state_c1.json" "$L0/ref2_term_state_c2.json" \
    "$L0/ref2_term_state_c3.json"
echo "--- guard exit $?"
python3 "$OP/check_no_spelling_keys.py" $OP/term_ref2_store/*.json | tail -3
echo "--- store guard exit $?"
