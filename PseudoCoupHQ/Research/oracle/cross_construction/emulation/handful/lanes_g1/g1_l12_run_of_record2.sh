#!/usr/bin/env bash
# g1_l12_run_of_record2.sh -- task g1: THE RUN OF RECORD.  The primitive
# lookup and the forty runs again, then every UNDECIDED gate call
# re-posed at 300,000 ms, then the composition column and the report --
# ONE lane, so `handful3.json` is written end to end by one version of
# the program (task h1's own section 7.1 lesson).
#
# WHAT CHANGED SINCE LANE g1_l9, and nothing else did.  ONE FIELD SHAPE:
# the primitive lookup's record of the chosen member now carries `lang`
# and `unit` and `n` beside the `operator` display label, which is the
# UNIT-OBJECT shape the spelling ban allows a token in and the one the
# guard's own except-list names; it was `operator_display_label` on a
# record with no `lang`, which is not that shape.  Nothing about what is
# measured, rendered, compiled, carved or proved is different, and lane
# g1_l9's own numbers are the check on that: the two runs must agree row
# for row.
#
# The re-pose at 300,000 ms is the law's own rule about a time limit: it
# is a FLAG, so the obligation is re-run with more room and whether the
# answer changed is reported.  The verdict OF RECORD stays the one the
# pipeline's own 3,000 ms ceiling gave; lane g1_l9 got UNDECIDED at both
# ceilings on all six.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1, checked
# after every run and every re-pose.  Lane g1_l9 peaked at 257,240 kB on
# the composition step and 459,092 kB on the runs.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/6] task g1: handful.py primitive3"
python3 $H/handful/handful.py primitive3
echo "[2/6] task g1: handful.py run3"
python3 $H/handful/handful.py run3
echo "[3/6] task g1: handful.py recheck3 300000"
python3 $H/handful/handful.py recheck3 300000
echo "[4/6] task g1: handful.py compose3"
python3 $H/handful/handful.py compose3
echo "[5/6] task g1: handful.py report3"
python3 $H/handful/handful.py report3
echo "[6/6] task g1: handful.py spellings3"
python3 $H/handful/handful.py spellings3
