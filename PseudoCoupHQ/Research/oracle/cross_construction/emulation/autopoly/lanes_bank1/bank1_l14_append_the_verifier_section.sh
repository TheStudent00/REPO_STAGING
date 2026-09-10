#!/bin/bash
# bank1_l14_append_the_verifier_section.sh -- task bank1, lane 14.
#
# WHAT THIS LANE DOES: appends section 14 to log 253, the conventions
# verifier's own tally over that log as lane 13 ran it.  A third pass
# over the log WITH this section in place would find this section's own
# prose UNVERIFIABLE -- a table of verifier results is not itself a
# command output -- which is exactly what tasks ex1 and ex2 recorded
# and for the same reason.  The obligation, zero DIFFERS, is met by
# lane 13 and is not re-opened by adding the account of it.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

L=PseudoCoupHQ/DevComms/log_253_task_bank1_the_bank.md
total=1

i=1
echo "[$i/$total] appending section 14 to log 253"
cat >> "$L" <<'S14'

# 14. The conventions verifier over this log

One pass, lane `bank1_l13_verify_253.sh`, over this log as lane 12 wrote it
(`<runs>/bank1/agent/logs/*__bank1_l13_verify_253.sh.log`).

| lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|
| `bank1_l13_verify_253.sh` | 20 | 11 | **0** | 9 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0**.

* **MATCHES (11)** — every fenced block in §3 to §12, each the output of the
  command on its first line, each re-run by the verifier and each answering
  the same way. They are `bank.py kinds`, `readings`, `restored`, `backups`;
  `autopoly.py --bank report`, `cost`, `audit`, `tally`, `changed`; the two
  guard calls; and the `wc -l` tally.
* **UNVERIFIABLE (9)** — the walkthrough, the reading definitions, the four
  glosses and the two lists: prose findings, each stated as such rather than
  claimed reproducible.

Every block in this log was written by capture, never by hand: lane
`bank1_l12_write_the_log.sh` ran each command and redirected its own output
into the file.
S14
echo "  log 253 is now $(wc -l < "$L") line(s)"
echo
echo "lane done"
