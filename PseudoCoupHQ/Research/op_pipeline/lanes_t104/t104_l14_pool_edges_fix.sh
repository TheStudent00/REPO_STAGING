#!/usr/bin/env bash
# t104 lane 14 -- `t104_pool.py`'s `edge_answer()` read only
# `pool100_edges.json`'s `edges` array (the 12 t100 applied edges) and
# never `proved_but_not_applied` (the 214 t100 proved-but-not-applied
# edges), so `proved_but_not_applied_edges` and both
# `not_applied_that_merge_by_text_*` counters stayed 0 regardless of
# what the 214 did -- the brief's §3(d) question ("which of t100's 214
# unapplied and 12 applied edges now merge by text alone") was only
# ever answered for the 12.  The function is fixed to walk both arrays,
# distinguished by their own `edge_applies` field.  This lane re-runs
# ONLY `t104_pool.py` (not `pool66_run.py` again -- its own refusal is
# already on the record from lane 11) over the SAME, already-complete
# term104_store, and re-guards the two files it writes.
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
echo "[1/2] the pool build again, both edge populations this time"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_pool.py
echo "pool exit $?"
echo "[2/2] the guard over the two files it wrote"
python3 check_no_spelling_keys.py pool104_candidate.json pool104_delta.json
echo "guard exit $?"
grep -c exempt pool104_candidate.json pool104_delta.json lanes_t104/t104_pool.py
