#!/usr/bin/env bash
# t91_l11_lost_proof_routes.sh -- TASK 91, lane 11: the 245 lost proofs
# re-read with the question lane 9 could not answer.
#
# WHY A SECOND LANE.  Lane 9 established the SHAPE of all 245 -- every
# one carries a positional label and a conditional transfer -- and then
# could not compare the two references on them, because the SUPERSEDED
# simulator refuses a conditional transfer outright.  That refusal is
# itself the answer to a different question: if the superseded
# simulator refused these bodies, then log 153's proof of them did not
# come from route one at all.  This lane asks which of log 153's two
# routes carried each proof, and what the two routes say now, both read
# off the stored verdicts rather than argued.
#
# THE MEMORY BOUND: one canon38 source document at a time; cap 6000 MB,
# abort named T91_MEMORY_ABORT.  Lane 9 measured 98.6 MB for this same
# walk.
#
# Product: t91_lost_proofs.json, t91_lost_proofs_printed.txt.
set -uo pipefail

cd /projects/PseudoCoupHQ/Research/op_pipeline || exit 2

python3 -m py_compile t91_lost_proofs.py || exit 3
python3 t91_lost_proofs.py 2>&1 | tee t91_lost_proofs_printed.txt
exit ${PIPESTATUS[0]}
