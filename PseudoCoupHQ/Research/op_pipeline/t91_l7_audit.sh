#!/usr/bin/env bash
# t91_l7_audit.sh -- TASK 91, lane 7: the report, computed off the four
# re-gate stores.
#
# It runs only after lanes 2..5 have written all four stores; the lane
# refuses by name if any of the four is short of the 332 source
# documents canon38 holds, rather than reporting a partial population
# as if it were the whole.
#
# THE MEMORY BOUND: the audit holds one record per unit (30,436 of
# them) plus, per canon38 source document in turn, that document's
# bodies and ledger PRODUCERS -- never its terms.  Cap 6000 MB, abort
# named T91_MEMORY_ABORT.
#
# Products: t91_audit.json, t91_audit_printed.txt in the project tree.
set -uo pipefail

cd /projects/PseudoCoupHQ/Research/op_pipeline || exit 2

expected=332
status=0
for d in t91_regate_store_attached_callees_fix \
         t91_regate_store_attached_callees_control \
         t91_regate_store_no_attached_callees_fix \
         t91_regate_store_no_attached_callees_control; do
  have=$(ls "$d" 2>/dev/null | wc -l)
  echo "$d: $have of $expected source documents"
  if [ "$have" -ne "$expected" ]; then
    echo "T91_POPULATION_REFUSAL: $d is short; the audit will not "\
"report a partial population as a whole one."
    status=5
  fi
done
if [ "$status" -ne 0 ]; then
  exit $status
fi

python3 t91_audit.py 2>&1 | tee t91_audit_printed.txt
exit ${PIPESTATUS[0]}
