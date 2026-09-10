#!/bin/bash
# t2_l25_the_lemmas_and_the_pass_of_record.sh -- task t2, lane 25: the
# lemmas restated over the shapes the pass's own store now records, and
# THE PASS OF RECORD run against them.
#
# WHY ONCE MORE.  Lane 24 named the one lemma each remaining `sat` place
# was short of: `extend_zero_w8_t128`, the eight-bit shift count widened
# to the value's width.  It was missing because the lemma plan reads the
# pass's own store for the shapes it must cover, and the store it read
# had been written before the shapes were recorded on it.  So the plan
# is read again from the store that has them, and the pass is run
# against the table that results -- the ORDERED shape, lemmas first.
#
# The schemas themselves are unchanged since lane 20 verified them at
# every width, so this lane does not re-verify them; lane 20's own
# tables are the record for that.
#
# MEMORY: bound 6 GB resident, checked after EVERY store line, named
# abort ABORT_MEMORY_T2; lane 23's 2,479 store lines peaked at
# 2,368,560 kB, 38% of the bound.
# CEILINGS: the gate's 3,000 ms, one re-pose at 30,000 ms, the
# equality's HARD 30,000 ms, 120 s of `lean` per theorem, and the
# constructed term's 200,000 nodes.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=7

i=1
echo "[$i/$total] THE SHAPES THE PASS'S OWN STORE RECORDS"
python3 "$C/lean/run_lemmas_t2.py" instances
echo

i=2
echo "[$i/$total] THE LEMMAS, per shape and per limb"
python3 "$C/lean/run_lemmas_t2.py" prove 120
echo

i=3
echo "[$i/$total] lane 23's store, moved beside itself"
if [ -f "$C/t2_construct_runs.jsonl" ]; then
    mv "$C/t2_construct_runs.jsonl" \
       "$C/t2_construct_runs.jsonl.before_the_shift_count_lemma"
    echo "  moved: $(wc -l < "$C/t2_construct_runs.jsonl.before_the_shift_count_lemma") line(s)"
else
    echo "  no store to move"
fi
echo

i=4
echo "[$i/$total] THE BANK WITHOUT THIS PASS"
python3 "$A/bank.py" build
echo

i=5
echo "[$i/$total] THE PASS OF RECORD"
python3 "$C/construct.py" run
echo

i=6
echo "[$i/$total] THE BANK WITH THIS PASS, and the three readings"
python3 "$C/construct.py" bank
python3 "$A/bank.py" readings
echo

i=7
echo "[$i/$total] construct.md"
python3 "$C/construct_report.py"
cat "$C/construct.md"
echo
echo "lane done"
