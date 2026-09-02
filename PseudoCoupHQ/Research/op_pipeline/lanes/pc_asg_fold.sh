#!/bin/sh
# pc_asg_fold.sh -- Job 2 of the 2026-08-26 lap.
#
# The 749 accepted compound-assignment units through the existing
# pipeline stages, in one universe with the 1758 plain units, so the
# question "what does an assignment unit relate to?" has plain units in
# the room to relate to.
#
# The stage is a SIBLING of op_pipeline (Research/stage_asg): each
# stage finds the lifter at dirname(HERE)/kind_fuzz_clustering, so a
# stage nested inside op_pipeline would not find it.
#
# Pure Python plus z3 over records already extracted: no compiler.
set -e

D=$(dirname "$0")/..
cd "$D"
S=../stage_asg

echo "== stage the two populations into one universe"
python3 asg_stage.py

cd "$S"

echo
echo "== sem-anchor (lift + anchored operand ids)"
python3 sem_anchored.py

echo
echo "== canonicalise (the canonical runnable form; refusals are loud)"
python3 canon.py --in . --out .

echo
echo "== match (byte and anchored-sem clusters)"
python3 match_units.py

echo
echo "== verdicts, three-verdict scheme plus the honest UNDECIDED bin"
python3 verdicts3.py --budget=900

echo
echo "== which relation carries an assignment unit to the plain units"
cp ../op_pipeline/asg_relation_lane.py .
python3 asg_relation_lane.py

cd ../op_pipeline
cp "$S"/asg_relation.json "$S"/asg_relation.md .

echo
echo "== fold into the class table"
python3 asg_fold_lane.py --stage "$S"

echo
echo "== the dom_op construction over the folded table"
python3 dom_ops5.py

echo
echo "== THE SPELLING BAN: the mechanical guard, on every product"
python3 check_no_spelling_keys.py \
    asg_relation.json dominant_table7.json \
    dom_ops5.json dom_ops5_digest_shape.json \
    "$S"/clusters.json "$S"/verdicts3.json
