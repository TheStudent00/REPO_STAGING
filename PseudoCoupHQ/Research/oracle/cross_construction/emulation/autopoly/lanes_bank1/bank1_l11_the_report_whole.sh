#!/bin/bash
# bank1_l11_the_report_whole.sh -- task bank1, lane 11.
#
# WHY THIS LANE EXISTS, said out loud: lane 10's section 9 printed a
# placeholder in its two source columns instead of the line on which
# the two artifacts differ.  The cause is in that lane and nowhere
# else: a certificate's `source.path` is relative to THIS folder
# (`src2/or_gpr_gpr_64__primitive__c.c`) and lane 10 joined it to the
# folder above.  `bank.resolve_source` is not wrong -- it tries the
# emulation folder and then the pass's own source folder, and it
# resolved every one of them.  This lane writes bank1.md WHOLE, both
# lane 9's sections and lane 10's, with the join corrected, so the
# report is one generated object rather than two appended ones.
# Lanes 9 and 10 and their logs stand; nothing is deleted.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
OP=PseudoCoupHQ/Research/op_pipeline
M="$A/bank1.md"
total=3

i=1
echo "[$i/$total] the seven changed artifacts, with the source join corrected"
python3 - "$A" <<'PY' | tee /tmp/bank1_changed.txt
import json, os, sys

here = sys.argv[1]
above = os.path.normpath(os.path.join(here, ".."))
document = json.load(open(here + "/bank1_delta.json"))
changed = []
for row in document["audit"]:
    if row["reading"] != "the artifact changed":
        continue
    changed.append(row)

wanted = set()
for row in changed:
    wanted.add((row["cell"]["mnem"], row["cell"]["shape"],
                row["cell"]["key_width"], row["target"], row["place"]))

certificate = {}
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"], cert["target"], cert["place"])
    if key not in wanted:
        continue
    if not cert["preferred"]:
        continue
    certificate[key] = cert
handle.close()

rederived = {}
handle = open(here + "/bank1_delta_runs.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    run = json.loads(text)
    for place in run.get("places") or []:
        key = (run["mnem"], run["shape"], run["key_width"], run["lang"],
               place.get("writes"))
        if key not in wanted:
            continue
        rederived[key] = (run, place)
handle.close()


def source_text(path):
    """the rendered source the certificate names, looked for where the
    passes actually wrote: this folder first, the folder above second.
    `bank.resolve_source` reads it the same way round."""
    if path is None:
        return None
    for root in [here, above]:
        candidate = os.path.join(root, path)
        if os.path.exists(candidate):
            return open(candidate).read()
    return None


def first_difference(left, right):
    if left is None:
        return ("-- the certificate's source is not on disk --", "--")
    if right is None:
        return ("--", "-- the re-derivation rendered nothing --")
    one = left.split("\n")
    two = right.split("\n")
    for index in range(max(len(one), len(two))):
        a = one[index].strip() if index < len(one) else "-- ends --"
        b = two[index].strip() if index < len(two) else "-- ends --"
        if a == b:
            continue
        return (a, b)
    return ("-- identical text --", "-- identical text --")


print("Table D7 -- the seven audited triples whose artifact changed. "
      "The two source columns hold the FIRST line on which the two "
      "rendered sources differ, which is the measurement; the several "
      "hundred characters of preamble they share are not shown.")
print("")
print("| `mnem` | shape | `key_width` | target | place | certificate's "
      "pass | certificate | re-derived | the certificate's source | the "
      "re-derivation's source |")
print("|---|---|---|---|---|---|---|---|---|---|")
for row in changed:
    key = (row["cell"]["mnem"], row["cell"]["shape"],
           row["cell"]["key_width"], row["target"], row["place"])
    cert = certificate.get(key)
    held = rederived.get(key)
    new_source = None
    if held is not None:
        new_source = held[1].get("source")
    path = None
    if cert is not None:
        path = (cert["source"] or {}).get("path")
    left, right = first_difference(source_text(path), new_source)
    left = left.replace("|", "\\|")
    right = right.replace("|", "\\|")
    print("| `%s` | %s | %s | %s | `%s` | `%s` | %s | %s | `%s` | `%s` |"
          % (row["cell"]["mnem"], row["cell"]["shape"],
             row["cell"]["key_width"], row["target"], row["place"],
             row["certificate_pass"], row["certificate_kind"],
             row["rederived_kind"], left[:170], right[:170]))
print("")
for row in changed:
    key = (row["cell"]["mnem"], row["cell"]["shape"],
           row["cell"]["key_width"], row["target"], row["place"])
    cert = certificate.get(key)
    held = rederived.get(key)
    print("%s %s %s on %s at %s"
          % (key[0], key[1], key[2], key[3], key[4]))
    print("   the certificate: pass %s, kind %s, source %s, sha256 %s"
          % (row["certificate_pass"], row["certificate_kind"],
             (cert["source"] or {}).get("path") if cert else "--",
             row["certificate_sha256"]))
    print("   the re-derivation: kind %s, sha256 %s"
          % (row["rederived_kind"], row["rederived_sha256"]))
    if held is not None:
        place = held[1]
        check = place.get("check") or {}
        print("   the re-derivation's verdict: %s -- %s"
              % (check.get("outcome"), check.get("reason")))
        if place.get("refusal_cause"):
            print("   the re-derivation's refusal cause: %s"
                  % place["refusal_cause"])
        if place.get("refusal_detail"):
            print("   the re-derivation's refusal detail: %s"
                  % place["refusal_detail"])
    print("")
PY
echo

i=2
echo "[$i/$total] writing $M whole"
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
list, and one delta pass was run on the five compiled targets — 707
runs where a full pass over the same five is 1,265. A full pass was
then run in the same instance and the same hour, so the cost is
measured rather than inferred: the delta pass ran 55.9% of the full
pass's runs and cost 81.9% of its seconds. That second figure is the
one worth reading twice, and section 6 says why.

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
## 6. The loop reshaped: delta plus audit, and what it cost

GLOSS, before the tables. The delta pass ran 707 of the 1,265 runs a
full pass over these five targets runs — 55.9% — and cost 81.9% of the
full pass's seconds. The two percentages differ because of WHICH runs
the delta skips: a pair every one of whose places is already proved is
a pair the machinery answers quickly, and those are exactly the ones
the delta drops, while the pairs it keeps are the unproved ones that
spend the gate's 3,000 ms ceiling and then its 30,000 ms re-pose. The
saving is real and it is in runs; it is not, at this stage of the
population, a proportional saving in seconds.

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
that pass and both read PASS.

## 8. The seven artifacts that changed, one by one

The audit re-derived 58 certified triples and 51 came back identical.
The seven below did not: the renderer moved between the certificate's
pass and this one, so the same cell now yields a DIFFERENT artifact.
None is an alarm — an alarm is a differing verdict on IDENTICAL inputs
— and none replaces its certificate; each is a new certificate beside
the old one, which is the whole of what a bank is for.

Six of the seven are `imm_*` cells, which is task ap5's own
symbolic-immediate change seen from the other side: the same change
that cost the nineteen pairs of section 4. The seventh, `or` gpr_gpr 64
on c at `flags.high`, is a different mechanism and the more interesting
one — task ap2 proved it through the PRIMITIVE route, and the current
driver refuses that place outright, so a proof that exists is one the
machinery can no longer reach. The certificate keeps it.

**LITERAL**, lane `bank1_l11_the_report_whole.sh`:

H7

echo '```' >> "$M"
cat /tmp/bank1_changed.txt >> "$M"
echo '```' >> "$M"

cat >> "$M" <<'H8'

## 9. Where the objects are

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
H8

echo "  bank1.md written whole: $(wc -l < "$M") line(s), $(stat -c %s "$M") byte(s)"
echo

i=3
echo "[$i/$total] the tally"
wc -l "$A/certificates.jsonl" "$A/bank1_delta_runs.jsonl" \
      "$A/bank1_full_runs.jsonl" "$A/bank1.md"
echo "rendered sources: src_bank1 $(ls "$A/src_bank1" | wc -l), src_bank1_full $(ls "$A/src_bank1_full" | wc -l)"
echo
echo "lane done"
