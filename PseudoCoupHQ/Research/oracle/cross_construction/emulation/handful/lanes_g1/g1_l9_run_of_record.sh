#!/usr/bin/env bash
# g1_l9_run_of_record.sh -- task g1: THE RUN OF RECORD.  The forty runs
# again after the one spelling that a rendered emulation (rather than a
# probe) showed was wrong, then every UNDECIDED gate call re-posed at
# 300,000 ms, then the composition column and the report -- ONE lane, so
# `handful3.json` is written end to end by one version of the program
# (task h1's own section 7.1 lesson).
#
# WHAT CHANGED SINCE LANE g1_l7, and nothing else did.  Go's answer-side
# bit reinterpretation was spelled with go's pointer cast
# (`*(*float32)(unsafe.Pointer(&bits))`), which needs a VARIABLE to take
# the address of; binding one made go give the function a stack frame it
# otherwise had none of, so the first `addss` emulation came back
# `sub $0x8,%rsp; ...; addss ...; add $0x8,%rsp; ret` -- NOT_COLLAPSED
# where c's and rust's are LANDED.  The spelling is now the standard
# library's own function, which is an EXPRESSION and needs no variable;
# it costs an inlining-marker `nop`, which task o2's own narrow chaff
# rule already counts as chaff.  The pointer cast stays where there is
# already a variable to take the address of: a parameter.
#
# The re-pose at 300,000 ms is the law's own rule about a time limit: it
# is a FLAG, so the obligation is re-run with more room and whether the
# answer changed is reported.  The verdict OF RECORD stays the one the
# pipeline's own 3,000 ms ceiling gave.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1, checked
# after every run and every re-pose.  Lane g1_l7's own forty runs peaked
# at 459,092 kB.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/5] task g1: handful.py run3"
python3 $H/handful/handful.py run3
echo "[2/5] task g1: handful.py recheck3 300000"
python3 $H/handful/handful.py recheck3 300000
echo "[3/5] task g1: handful.py compose3"
python3 $H/handful/handful.py compose3
echo "[4/5] task g1: handful.py report3"
python3 $H/handful/handful.py report3
echo "[5/5] done"
