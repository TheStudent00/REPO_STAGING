#!/bin/bash
# ref2 lane 8 -- every unit of `term66_store/` transcribed again through the
# CORRECTED reference into `term_ref2_store/`, beside it, with `term66_store/`
# opened for reading only.
#
# The walk is task t104's own (`lanes_t104/t104_walk.py`), imported unmodified
# with its five paths pointed at this task's files: one forked sub-process per
# unit, two passes, the term's own s-expression hashed before and after
# printing, and the store-to-store text delta computed from the two stores on
# disk.
#
# Memory: the stated bound is 12 GB with the named abort ABORT_MEMORY_REF2.
# Pass 1 runs ONE sub-process at 3,072 MB; pass 2 runs TWO at 6,144 MB, and
# two of those is exactly the bound.  The parent does no z3 work and is capped
# at the bound as well, checked after every shard.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"
cd "$L0" || exit 1

echo "[1/2] the walk: 332 shards, pass 1 at 3072 MB / 90 s, pass 2 at 6144 MB / 600 s"
python3 "$L0/ref2_term_walk.py" walk 3072 90 6144 600
echo "--- exit $?"

echo "[2/2] the two stores, counted"
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
    print('%-40s %6d records, %6d with a layer-5 text'
          % (os.path.basename(folder), units, texts))
"
echo "--- exit $?"
