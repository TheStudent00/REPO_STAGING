#!/usr/bin/env bash
# t104 lane 9 -- THE SPELLING-BAN GUARD, unmodified, over every json
# this task wrote: the named artifacts and every shard of the new
# store.
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
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/3] the named artifacts"
python3 check_no_spelling_keys.py t104_diagnose.json t104_premise.json t104_audit.json t104_walk_evidence.json t104_walk_state.json t104_order_probe.json pool104_candidate.json pool104_delta.json
echo "named artifacts exit $?"
echo "[2/3] every shard of term104_store"
python3 check_no_spelling_keys.py term104_store/*.json | tail -5
echo "store exit $?"
echo "[3/3] grep -c exempt over every file this task added"
grep -c exempt t104_diagnose.json t104_premise.json t104_audit.json t104_walk_evidence.json t104_walk_state.json t104_order_probe.json pool104_candidate.json pool104_delta.json lanes_t104/t104_diagnose.py lanes_t104/t104_premise.py lanes_t104/t104_walk.py lanes_t104/t104_order_probe.py lanes_t104/t104_pool.py lanes_t104/t104_the44.py lanes_t104/t104_perturb.py
