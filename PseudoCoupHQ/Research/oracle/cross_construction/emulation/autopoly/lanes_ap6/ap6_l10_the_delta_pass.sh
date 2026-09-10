#!/bin/bash
# ap6_l10_the_delta_pass.sh -- task ap6, lane 10.
#
# WHAT THIS LANE DOES: THE DELTA PASS, whole, over the five compiled
# targets, through the one driver this task leaves behind -- no task
# gates, one held cell per setter cell the sweep posed before each flag
# consumer, the primitive lookup carrying the matched body's holders,
# and the gate's narrow-answer re-pose beside the caller extension.
# Lane 9's sixty runs are on the store already and are skipped.
#
# IT CARRIES ITS OWN AUDIT: 5% of the certified place-triples, seed
# `2026-09-10`.  A re-derived verdict that differs from its certificate
# ON IDENTICAL INPUTS is an ALARM and stops the pass; a differing
# ARTIFACT -- and this pass has two reasons to produce them, the holders
# and the answer width -- is a NEW certificate beside the old one and
# never in place of it.  The 100% audit of lane 4 is the guard on the
# gate removal and it answered with 0 alarms; this one is the guard on
# what the pass itself changes.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_AP6; lane 9's sixty peaked at 258,808 kB (4% of the
# bound).  CEILINGS: 3,000 ms per gate call, ONE re-pose at 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=1

i=1
echo "[$i/$total] THE DELTA PASS, whole"
python3 "$A/autopoly.py" --pass ap6_delta --bank run
echo
echo "lane done"
