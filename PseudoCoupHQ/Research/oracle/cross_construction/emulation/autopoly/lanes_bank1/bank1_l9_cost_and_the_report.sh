#!/bin/bash
# bank1_l9_cost_and_the_report.sh -- task bank1, lane 9.
#
# WHAT THIS LANE DOES: the MEASURED cost of the delta pass beside the
# full pass lane 8 ran in the same instance and the same hour, and then
# `bank1.md`, written by running each command and capturing its own
# output into the file.  No transcript in that report is typed by hand.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1; the full
# pass peaked at 2,412,736 kB (38% of the bound), the delta at
# 996,780 kB (15.8%).
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
M="$A/bank1.md"
total=4

i=1
echo "[$i/$total] the measured cost, delta beside full"
python3 "$A/autopoly.py" --bank cost
echo

i=2
echo "[$i/$total] the audit, with the certificate's own pass named"
python3 "$A/autopoly.py" --bank audit
echo

i=3
echo "[$i/$total] writing $M"
: > "$M"

block () {   # block "<command line>" -- run it, fence its own output
    echo '```' >> "$M"
    echo "\$ $1" >> "$M"
    eval "$1" >> "$M" 2>&1
    echo '```' >> "$M"
    echo >> "$M"
}

cat >> "$M" <<'HEAD'
# bank1 — the polyfill library as banked certificates, and the loop reshaped to delta plus audit

Task `bank1`, 2026-09-10, instance `bank1` on the tower guest. Brief:
`Research/briefs/task_bank1_brief.md`. Law: `Research/LAW.md`, read in
full including its tower section.

Every rendering below is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal. Every
fenced block is the output of the command on its first line, captured
by the lane that ran it — none is typed by hand.

---

## 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table, holding, per place the opcode writes, the z3
  term the reference simulator's own builder puts there.
* A **WRITTEN PLACE** is one destination that opcode writes — `reg_rdi`,
  `flags`, `reg_xmm0.low`, `x87_7`, `stack_-8` — and it is part of a
  certificate's key because the gate answers per place, not per run.
* A **CERTIFICATE** is one record about ONE ARTIFACT: one (cell, target,
  written place) with the term text it was posed on, the rendered source
  and its sha256, the compiler and its flags, the carved body, and the
  gate's own verdict.
* **THE BANK** is `certificates.jsonl`: every certificate of every pass,
  the strongest for each key marked `preferred`, every weaker or later
  one kept beside it and marked `superseded_by`.
* **THE DELTA PASS** is the loop run over the (cell, target, written
  place) triples the bank holds no proof for, plus a 5% audit sample of
  the ones it does, re-derived from the term.
* **AN ALARM** is an audited triple whose re-derived verdict differs
  from its certificate ON IDENTICAL INPUTS — the same term text, the
  same source sha256, the same compiler and flags.

## 2. The walkthrough, before any figure

Nine stores were on disk when this task began: the five compiled
passes `ap1` to `ap5`, task ap3's normalise-off ablation, task ex1's
cpp pass, task ex1's interpreted handful, and task ex2's interpreted
loop. Each was read line by line and every run turned into one
certificate per written place; a run that never reached a place at all
was banked as one certificate with a null place and the kind `refused`,
so an attempt and its cause are banked rather than lost. The strongest
certificate of each key was marked preferred, ties going to the
earliest pass, and every other entry kept beside it.

Two things the first build got wrong were found by reading its own
output and fixed, and both are recorded here rather than tidied away.
The first: the interpreted route was read `rendered` first and
`refusal_cause` second, so task ex2's thirty-eight nullary runs came
out `undecided` where task ex2's own account calls them refused — 418
against ex2's 456. The second: every certificate named its store as
`...`, and the spelling guard splits a string on
`/ | : ,` and refuses any piece that is an operator token, which `~`
is; the guard refused the file 11,340 times, once per certificate, and
the record is now written the guard's way, as a repository-relative
path.

Then the loop was reshaped. The driver `autopoly.py` gained a `--bank`
mode whose attempted set is read off the bank rather than off the cell
list, and one delta pass was run on the five compiled targets. It is
the whole of what this task changed about how the loop runs.

HEAD

block "python3 $A/bank.py kinds"

cat >> "$M" <<'H2'
## 3. THE THREE READINGS

Stated as three every time from now on. STRICT: every written place of
the pair is proved. DESTINATION-ONLY: every place of the pair's
destination register is proved and the flags are not read — the reading
tasks ap1 to ap5 reported. CORPUS-NEEDED: the destination is proved AND
the flags are proved wherever the corpus's own attestation records a
consumer reading a cell of this `mnem`'s flags, the flags ignored where
no consumer ever does.

H2

block "python3 $A/bank.py readings"

cat >> "$M" <<'H3'
## 4. The nineteen pairs a certificate restores

H3

block "python3 $A/bank.py restored"

cat >> "$M" <<'H4'
## 5. The stores this task did not bank, and the audit of that exclusion

Each is a WITHIN-PASS backup its own log records as defective and keeps
beside the run of record; none is a pass of the loop. Leaving one out
silently would be a claim, so each was read anyway and the answer
measured.

H4

block "python3 $A/bank.py backups"

cat >> "$M" <<'H5'
## 6. The loop reshaped: delta plus audit

H5

block "python3 $A/autopoly.py --bank report"
block "python3 $A/autopoly.py --bank cost"
block "python3 $A/autopoly.py --bank audit"
block "python3 $A/autopoly.py --bank tally"

cat >> "$M" <<'H6'
## 7. The guard

H6

block "python3 $OP/check_no_spelling_keys.py $A/certificates.json"
block "python3 $OP/check_no_spelling_keys.py $A/bank1_delta.json"

cat >> "$M" <<'H7'
The two jsonl stores are guarded by the same program over a json array
of their lines, materialised under `/tmp` inside the instance and never
in the repository; lane `bank1_l7_delta_report_and_rebank.sh` carries
that pass.

## 8. Where the objects are

* `Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl`
  — the bank.
* `Research/oracle/cross_construction/emulation/autopoly/certificates.json`
  — its aggregate, with the three readings.
* `Research/oracle/cross_construction/emulation/autopoly/bank.py`
  — the program that reads every run on disk and writes the bank.
* `Research/oracle/cross_construction/emulation/autopoly/autopoly.py`
  — the loop driver, `--bank` mode.
* `Research/oracle/cross_construction/emulation/autopoly/autopoly1.py`
  — task ap1's driver, copied unchanged, so log 243's own commands and
  task ap1's lanes still answer.
* `Research/oracle/cross_construction/emulation/autopoly/bank1_delta_runs.jsonl`
  — the delta pass's store; `bank1_full_runs.jsonl` the full pass's.
* `Research/oracle/cross_construction/emulation/autopoly/lanes_bank1/`
  — this task's lane scripts.
H7

echo "  bank1.md written: $(wc -l < "$M") line(s), $(stat -c %s "$M") byte(s)"
echo

i=4
echo "[$i/$total] the tally"
wc -l "$A/certificates.jsonl" "$A/bank1_delta_runs.jsonl" \
      "$A/bank1_full_runs.jsonl" "$A/bank1.md"
ls "$A/src_bank1" | wc -l
ls "$A/src_bank1_full" | wc -l
echo
echo "lane done"
