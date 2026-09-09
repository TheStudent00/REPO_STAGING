#!/usr/bin/env bash
# t91_l12_guards_final.sh -- TASK 91, lane 12 (final): THE MECHANICAL GUARD.
#
# `check_no_spelling_keys.py` UNMODIFIED, in ONE process, over every
# artifact task 91 wrote: the two population files, the four re-gate
# stores (332 source documents each), the audit, the sample and the
# reference evidence.  The check's own operator inventory is read from
# `probe_manifest_*.json` inside that one process.
#
# The lane then counts the word `exempt` in the check's own output: the
# provenance exemption must be claimed by NOTHING here, so that count
# must be 0.
#
# Product: t91_guard_final_printed.txt in the project tree.
set -uo pipefail

cd PseudoCoupHQ/Research/op_pipeline || exit 2

files=$(ls t91_populations.json t91_audit.json t91_sample.json \
           t91_reference_evidence.json t91_lost_proofs.json t91_timeouts.json 2>/dev/null)
stores=$(ls t91_regate_store_attached_callees_fix/*.json \
            t91_regate_store_attached_callees_control/*.json \
            t91_regate_store_no_attached_callees_fix/*.json \
            t91_regate_store_no_attached_callees_control/*.json \
            2>/dev/null)

echo "artifacts handed to the check, in ONE process:"
echo "  named files:      $(echo "$files" | wc -w)"
echo "  store documents:  $(echo "$stores" | wc -w)"
echo ""

python3 check_no_spelling_keys.py $files $stores \
    > t91_guard_final_printed.txt 2>&1
rc=$?

echo "check_no_spelling_keys.py exit code: $rc"
echo ""
echo "PASS lines:  $(grep -c '^PASS' t91_guard_final_printed.txt)"
echo "FAIL lines:  $(grep -c '^FAIL' t91_guard_final_printed.txt)"
echo "exempt count (must be 0): $(grep -c exempt t91_guard_final_printed.txt)"
echo ""
echo "--- the first and last lines of the check's own output ---"
head -3 t91_guard_final_printed.txt
echo "..."
tail -3 t91_guard_final_printed.txt
echo ""
if grep -q '^FAIL' t91_guard_final_printed.txt; then
  echo "T91_SPELLING_GUARD_REFUSAL: the check failed on an artifact "\
"this task wrote; the output is refused."
  grep '^FAIL' -A 4 t91_guard_final_printed.txt | head -40
  exit 6
fi
if [ "$(grep -c exempt t91_guard_final_printed.txt)" -ne 0 ]; then
  echo "T91_SPELLING_GUARD_REFUSAL: an artifact claimed the "\
"provenance exemption; nothing here may."
  exit 7
fi
exit $rc
