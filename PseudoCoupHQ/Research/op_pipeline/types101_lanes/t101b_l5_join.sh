#!/usr/bin/env bash
# t101b lane 5 -- second re-run of the join. Lane 4 got past the
# off_holder Counter/defaultdict bug (fixed in lane 3->4) and completed
# holders_table/spellings_table/entry_holders, then hit a SECOND bug at
# main()'s summary print: entry_holders returned dict(tot) instead of
# tot (a Counter), so a totals key that was never incremented (here:
# members_compiled_without_rows, when every compiled probe had rows)
# was simply absent from the plain dict, and ptot["members_compiled_
# without_rows"] raised KeyError. Fixed at cause: return the Counter
# itself (its __missing__ returns 0 for an absent key, same as every
# other Counter in this file); one line changed. Same work as lane 3/4:
# the original brief's §2 steps 2-5 over the rows lane 2 wrote.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] types101_join.py ========"
python3 types101_join.py
rc=$?
echo "types101_join.py exit ${rc}"
exit ${rc}
