#!/usr/bin/env bash
# t104 lane 11 -- THE POOL over the changed normalizer's texts, then
# the spelling-ban guard over every json this task wrote.
#
# Step 1 runs `pool66_run.py` UNMODIFIED so its own refusal is on the
# record: it refuses to write a pool over a member set short of the
# population it names, and 44 members are short.  That refusal is not
# worked around; what step 2 writes is a CANDIDATE that carries the
# shortfall in its own summary.
#
# Step 2 builds the same ruled merge twice over the same member set --
# once with the layer-5 texts of term66_store/ (the rule as it stood)
# and once with those of term104_store/ (the changed rule) -- so the
# difference between the two entry counts is the normalizer's and
# nothing else's, and answers the t100 edge question off
# pool100_edges.json.
#
# THE SPELLING BAN, pasted verbatim as required:
#
# "THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
# a second violation).  No operator token may appear in ANY key,
# grouping, pairing, row structure, candidate selection, or comparison
# scope, anywhere in this line -- not in matching, not in "which pairs
# get compared", not in report rows, not in dropdowns.  The candidate
# set for comparison comes from machine-form evidence (clusters,
# connections, type pairs) or from ratified intention -- never from the
# token.  The token appears exactly once per unit: as a display label
# on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
# the arch campaign's cross-language matrix (caught by the owner
# 2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
# -- the fix brief itself reintroduced it as "same-operator pairs").
# MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
# units must run the spelling-key check
# (op_pipeline/check_no_spelling_keys.py) and refuse its own output on
# failure.  A brief handed to any subagent for this line MUST paste
# this paragraph verbatim."
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/4] pool66_run.py, unmodified, for its own refusal"
python3 pool66_run.py
echo "pool66_run.py exit $?"
echo "[2/4] the before build, the after build, the candidate, the delta"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_pool.py
echo "pool exit $?"
echo "[3/4] the guard over the named artifacts"
python3 check_no_spelling_keys.py t104_diagnose.json t104_premise.json t104_audit.json t104_audit_unchanged_rule.json t104_walk_evidence.json t104_walk_evidence_unchanged_rule.json t104_walk_state.json t104_order_probe.json t104_the44.json pool104_candidate.json pool104_delta.json
echo "named artifacts exit $?"
echo "[4/4] the guard over every shard of term104_store, then grep -c exempt"
python3 check_no_spelling_keys.py term104_store/*.json | tail -3
echo "store exit $?"
grep -c exempt t104_diagnose.json t104_premise.json t104_audit.json t104_walk_evidence.json t104_order_probe.json t104_the44.json pool104_candidate.json pool104_delta.json lanes_t104/t104_diagnose.py lanes_t104/t104_premise.py lanes_t104/t104_walk.py lanes_t104/t104_order_probe.py lanes_t104/t104_pool.py lanes_t104/t104_the44.py lanes_t104/t104_perturb.py
