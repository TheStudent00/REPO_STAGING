#!/usr/bin/env bash
# g1_l10_guard.sh -- task g1: the unmodified spelling guard over every
# json this task's own programs write, and `grep -c exempt` over every
# file it added or changed.
#
# THE THREE JSON THIS TASK WRITES: `handful3.json` (the forty runs),
# `handful3_primitive.json` (the primitive lookup, whose rows carry the
# chosen member's OWN probe as a UNIT OBJECT -- `lang` plus `unit` plus
# `n` plus the `operator` display label, which is the one shape the ban
# allows a token in and the one the guard's own except-list names), and
# `handful3_spellings.json` (the two spelling tables, keyed by z3
# declaration kind).  `go_facts.json` is guarded too: it is a
# measurement of the go COMPILER, not of any unit, and it carries no
# pool member at all.
#
# The guard itself is never modified and no exemption is claimed
# anywhere; `grep -c exempt` over every file this task added answers 0
# on each, which is why `grep -c` exits 1 and the step carries `|| true`
# on its own line rather than the lane failing on a zero count.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1; the guard
# reads json files of a few hundred kB and reports its own peak.
set -uo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/2] task g1: the guard over the four json this task's own programs write"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $H/handful/handful3.json $H/handful/handful3_primitive.json \
    $H/handful/handful3_spellings.json $H/go/go_facts.json
echo "[2/2] task g1: grep -c exempt over every file this task added or changed"
grep -c exempt $H/go/go_facts.py $H/go/go_render.py \
    $H/swift/swift_render.py $H/handful/handful.py \
    $H/handful/handful3.md \
    $H/handful/lanes_g1/g1_l5_go_facts3.sh \
    $H/handful/lanes_g1/g1_l9_run_of_record.sh \
    $H/handful/lanes_g1/g1_l10_guard.sh
echo "done"
