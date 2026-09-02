#!/bin/sh
# pc_mirror2.sh -- Job 1 of the 2026-08-26 lap.
#
# The third candidate rule, widened from classes of one to classes of
# three or fewer, then the class table rebuilt and the dom_op
# construction re-run over it.
#
# Source table is dominant_table5.json, NOT dominant_table4.json as the
# brief said: table 5 is table 4 plus the single java member the jvm
# join added, and it is what dom_ops3.json was built from.  Reading
# table 4 would silently drop java from the lap.
#
# Pure Python plus z3 over records already extracted: no compiler.
set -e

D=$(dirname "$0")/..
cd "$D"

echo "== the widened candidate rule -> verdicts6"
python3 candidates_mirror2.py

echo
echo "== the class rebuild -> dominant_table6, bridges6"
python3 dominant_table6.py

echo
echo "== the dom_op construction -> dom_ops4"
python3 dom_ops4.py

echo
echo "== THE SPELLING BAN: the mechanical guard, on every product"
python3 check_no_spelling_keys.py \
    verdicts6.json dominant_table6.json bridges6.json \
    dom_ops4.json dom_ops4_digest_shape.json
