#!/bin/bash
# t2_l23_the_pass_with_the_lemmas_b.sh -- task t2, lane 23: lane 21 again, after lane 22 measured that the lemma table and the tier keyed an extension under two different widths: THE PASS,
# re-run with the lemma table in place, and the bank and the report
# rebuilt around it.
#
# WHY IT IS RUN AGAIN.  The brief's proof order is canonical form, then
# the schema's lemma, then z3 -- and lane 17 ran before the lemmas
# existed, so every equality it discharged fell through to z3 and every
# certificate it banked says so.  The ORDERED shape is lemmas first,
# then the pass, so the pass is run in that order and its own earlier
# store is moved beside itself rather than left to be read as the
# record.  Nothing is deleted.
#
# THE STEPS, and the middle one is the point: the bank is rebuilt
# WITHOUT this pass first, so the keys it certified become uncertified
# again and the pass attempts them; then it is rebuilt with the pass.
#
# MEMORY: bound 6 GB resident, checked after EVERY store line, named
# abort ABORT_MEMORY_T2; lane 17's 2,479 store lines peaked at
# 2,368,560 kB, 38% of the bound.
# CEILINGS: the gate's 3,000 ms, one re-pose at 30,000 ms, the
# equality's HARD 30,000 ms, the constructed term's 200,000 nodes.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=6

i=1
echo "[$i/$total] lane 17's store, moved beside itself"
if [ -f "$C/t2_construct_runs.jsonl" ]; then
    mv "$C/t2_construct_runs.jsonl" \
       "$C/t2_construct_runs.jsonl.before_the_lemma_key_carried_the_shape_alone"
    echo "  moved: $(wc -l < "$C/t2_construct_runs.jsonl.before_the_lemma_key_carried_the_shape_alone") line(s)"
else
    echo "  no store to move"
fi
echo

i=2
echo "[$i/$total] THE BANK WITHOUT THIS PASS"
python3 "$A/bank.py" build
echo

i=3
echo "[$i/$total] THE PASS"
python3 "$C/construct.py" run
echo

i=4
echo "[$i/$total] THE BANK WITH THIS PASS"
python3 "$C/construct.py" bank
echo

i=5
echo "[$i/$total] THE THREE READINGS"
python3 "$A/bank.py" readings
echo

i=6
echo "[$i/$total] construct.md"
python3 "$C/construct_report.py"
cat "$C/construct.md"
echo
echo "lane done"
