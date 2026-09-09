#!/usr/bin/env bash
# t104 lane 10 -- THE RE-NORMALIZATION WALK AGAIN, with the changed
# normalizer.
#
# WHAT CHANGED BETWEEN THIS LANE AND LANE 3.  One function:
# `Term.normalize` in `term.py` now calls `order_commutative` ONCE MORE,
# before the first `z3.simplify`.  Lane 3 measured why: over the 27,682
# proved units it walked, a second term built from each unit's own term
# by permuting the operands of every commutative node printed a
# DIFFERENT text for 899 of them; lane 8 asked the solver and it says
# those permuted terms are the same computation, and that this one
# extra call closes the difference.
#
# WHAT LANE 3's RUN IS KEPT AS.  Lane 3 walked with the rule UNCHANGED
# and found 0 of 27,866 records' texts changed -- that is, term66_store
# is a faithful print of the rule as it stood.  Its audit is copied to
# t104_audit_unchanged_rule.json before this lane overwrites anything,
# so the before is on disk and not only in a lane log.
#
# The store and the walk state are cleared so this is a fresh walk of
# the whole population and not a resume of the old rule's answers.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/3] keep lane 3's audit, clear the store and the walk state"
cp t104_audit.json t104_audit_unchanged_rule.json
cp t104_walk_evidence.json t104_walk_evidence_unchanged_rule.json
rm -f t104_walk_state.json t104_walk_evidence.json
rm -rf term104_store
echo "[2/3] the walk, with the changed normalizer"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_walk.py 1536 60 3072 900
echo "walk exit $?"
echo "[3/3] shards written"
ls term104_store/*.json | wc -l
