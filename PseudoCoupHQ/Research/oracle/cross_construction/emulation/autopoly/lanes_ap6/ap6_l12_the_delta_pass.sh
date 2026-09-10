#!/bin/bash
# ap6_l12_the_delta_pass.sh -- task ap6, lane 12: the delta pass again,
# from an empty store, after the audit's matcher was given the sixth
# part of its own key.
#
# WHY LANE 10 IS NOT THE ANSWER.  It stopped at pair 192 of 709 on three
# ALARM rows, and lane 11 showed what they were: the audit's key is
# (cell, target, written place, SETTER CELL) and its matcher compared
# the first four parts only, so a run over the setter cell
# `cmp gpr_mem 8` was read against a certificate about `cmp gpr_gpr 8`.
# The two are not one obligation -- their cell terms PRINT the same,
# because the printer canonicalises a free symbol to `v0` and `v1`, and
# they render to the same source, and their ARRIVAL CONTRACTS differ,
# which is the whole of the difference between PROVED and DISPROVED
# there.  That was harmless while the loop wrote one run per (cell,
# target); it is not harmless now that it writes one per setter cell.
# The matcher now compares the setter too.  Nothing about what is
# measured moved: an audit compares a key with itself.
#
# THE STORE IS MOVED BESIDE ITSELF, not deleted, so the pass's own
# counts -- runs, seconds, audited triples -- are one coherent
# measurement rather than a resumed one.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_AP6; lane 10's 840 runs peaked at 1,461,924 kB (23% of
# the bound).  CEILINGS: 3,000 ms per gate call, ONE re-pose at
# 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=2

i=1
echo "[$i/$total] lane 10's store, moved beside itself"
if [ -f "$A/ap6_delta_runs.jsonl" ]; then
    mv "$A/ap6_delta_runs.jsonl" \
       "$A/ap6_delta_runs.jsonl.before_the_audit_key_carried_the_setter"
    echo "  moved: $(wc -l < "$A/ap6_delta_runs.jsonl.before_the_audit_key_carried_the_setter") line(s)"
else
    echo "  no store to move"
fi
echo

i=2
echo "[$i/$total] THE DELTA PASS, whole"
python3 "$A/autopoly.py" --pass ap6_delta --bank run
echo
echo "lane done"
