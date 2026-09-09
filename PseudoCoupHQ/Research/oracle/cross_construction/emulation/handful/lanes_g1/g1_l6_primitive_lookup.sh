#!/usr/bin/env bash
# g1_l6_primitive_lookup.sh -- task g1: the PRIMITIVE LOOKUP alone, over
# the forty (cell, target) pairs, and the two per-target spelling tables.
#
# WHAT THIS MEASURES, and why it runs before the forty runs do.  Task
# g1's one design decision is that `find_emulation(cell, lang)` asks
# first whether the target has an OPERATOR whose whole lowered body IS
# the cell.  This lane runs that question ALONE -- no render, no
# compile, no gate -- so which of the forty pairs takes the primitive
# route and which falls back to the term route is on the record before
# anything is built on it, together with the ground each choice rested
# on: how many of that language's single-opcode rows classify to the
# cell, which row the corpus attests most, and which member of it
# resolves to a probe of that language's own manifest.
#
# The second step prints the two spelling tables the two new renderers
# were written from: go's, every row with the probe in `go_facts.json`
# that measured it, and swift's, every row marked UNMEASURED because
# there is no swiftc in this image to measure one.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1, checked
# after every lookup; the program prints its own peak.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/4] task g1: the go renderer's ship flags and go's own argument sequence"
python3 $H/go/go_render.py flags
echo "[2/4] task g1: the swift renderer's ship flags, and what swiftc answers here"
python3 $H/swift/swift_render.py flags
echo "[3/4] task g1: handful.py primitive3"
python3 $H/handful/handful.py primitive3
echo "[4/4] task g1: handful.py spellings3"
python3 $H/handful/handful.py spellings3
