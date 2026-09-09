#!/usr/bin/env bash
# t104 lane 13 -- lane 11's guard step found two spelling-ban
# violations already sitting in this task's own artifacts:
# `declaration_kind_census` keyed by "name|kind" in four files, and
# `operator_name` (a bare token) on t104_diagnose.json's commutative-
# node rows.  Both are corrected in place by t104_fix_spelling_keys.py
# (counts and evidence untouched, only key/field shape), the matching
# source fix goes into t104_walk.py and t104_diagnose.py so a re-run
# does not reintroduce either, and the full guard runs again to prove
# it: THE SPELLING BAN, pasted verbatim as required:
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
echo "[1/2] the two fixes, in place"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_fix_spelling_keys.py
echo "fix exit $?"
echo "[2/2] the guard again, over every named artifact and every shard"
python3 check_no_spelling_keys.py t104_diagnose.json t104_premise.json t104_audit.json t104_audit_unchanged_rule.json t104_walk_evidence.json t104_walk_evidence_unchanged_rule.json t104_walk_state.json t104_order_probe.json t104_the44.json pool104_candidate.json pool104_delta.json
echo "named artifacts exit $?"
python3 check_no_spelling_keys.py term104_store/*.json | tail -3
echo "store exit $?"
grep -c exempt t104_diagnose.json t104_premise.json t104_audit.json t104_audit_unchanged_rule.json t104_walk_evidence.json t104_walk_evidence_unchanged_rule.json t104_walk_state.json t104_order_probe.json t104_the44.json pool104_candidate.json pool104_delta.json lanes_t104/t104_diagnose.py lanes_t104/t104_premise.py lanes_t104/t104_walk.py lanes_t104/t104_order_probe.py lanes_t104/t104_pool.py lanes_t104/t104_the44.py lanes_t104/t104_perturb.py lanes_t104/t104_pass2_retry.py lanes_t104/t104_fix_spelling_keys.py
