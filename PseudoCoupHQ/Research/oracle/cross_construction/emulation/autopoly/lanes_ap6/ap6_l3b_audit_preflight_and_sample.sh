#!/bin/bash
# ap6_l3_audit_preflight_and_sample.sh -- task ap6, lane 3b: lane 3 again, after a sort key that formatted a tuple with `%s` was written as `str`.
#
# WHAT THIS LANE DOES: the plan of THE 100% AUDIT -- every certificate
# the bank holds for the five compiled targets, re-derived from the
# cell's own term -- and then the first 20 of its runs as the memory
# sample, so the pass's own peak is measured before the pass runs.
#
# WHY 100%: it is the guard on the removal of the nine task-name gates.
# The rules the gates used to switch on are now unconditional, so every
# certificate is re-derived once through the one driver: a re-derived
# verdict that differs from its certificate ON IDENTICAL INPUTS (same
# term text, same source sha256, same compiler and flags) is an ALARM
# and stops the pass; a differing ARTIFACT is a new certificate recorded
# beside the old one and never in place of it.
#
# `--attempts off` leaves ONLY the audit, so what this measures is
# re-derivation and nothing else.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_AP6.  CEILINGS: 3,000 ms per gate call, ONE re-pose at
# 30,000 ms -- the loop's two ceilings of record, unchanged.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=2

i=1
echo "[$i/$total] THE PLAN: what the 100% audit re-derives"
python3 "$A/autopoly.py" --pass ap6_audit --audit-share 1 \
    --attempts off --bank preflight
echo

i=2
echo "[$i/$total] THE MEMORY SAMPLE: the first 20 runs of the audit"
python3 "$A/autopoly.py" --pass ap6_audit --audit-share 1 \
    --attempts off --bank run 20
echo
echo "lane done"
