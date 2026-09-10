# Task rv3b — the two rows rv3 left waiting for ref2: the twins on the corrected x86 reference, the riscv64 certificates into the bank; then the loop and the readings

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (the
laptop's `~/Programming` is now split into PRIVATE/ and PUBLIC/; the
tower is flat; sync paths in the flat form; container paths unchanged).
Then `task_rv3_brief.md` and its log (`DevComms/log_260`: rows 2 and 4
and §2 are marked `WAITS FOR ref2`; the hashes it read are listed at its
end), `task_ref2_brief.md` and its log (ref2 is CLOSED before this task:
the corrected `reference.py`, the re-derived model table, term store,
pool and bank; every x86 term you read is the corrected one — record
the hashes you read beside rv3's), `Research/GLOSSARY.md`. Instance
`rv3.conf` (reuse). Artifact folder: `Research/oracle/riscv/`; lanes
under `lanes_rv3b/`.

## 1. The two rows, exactly as `task_rv3_brief.md` §1 states them
| row | the change | guard |
|---|---|---|
| the twins | `twins.json` re-derived against ref2's corrected model table; both readings (whole place / own width) beside rv2's 102 / 161 | every twin that appeared or vanished, by cell, with the term text that changed |
| the bank | rv3's `certificates_riscv64.jsonl` (244 proved, 0 disproved, the 434 interpreted agreements, the 56 swift refusals) joins `certificates.jsonl` in the bank's record shape with `arch: "riscv64"` and `inherited_from`; `bank.py`'s delta and 5% audit read `arch` as part of the key; an x86 row is untouched | bank count before → after; the audit's 5% on riscv64 rows: differing verdicts 0, LITERAL |

An inherited certificate whose twin CHANGED under the corrected table
is re-verified (compile for riscv64, gate) before it is banked; one
whose twin vanished is banked as `refused: twin vanished under ref2`
with the two term texts.

## 2. Then the loop and the readings
`task_rv3_brief.md` §2 verbatim: the loop over the cells still untwinned
after the re-derivation, both routes; the collapse column; the count of
cells with a proved riscv64 emulation by either route beside rv2's 116
and rv3's 117; the three readings (coincide on RISC-V: say so once, one
number). Guard over every json/jsonl; log (next free number); verifier
lane; PROGRESS on the riscv64 node and the research node; sync-back;
instance down. Memory bound 6g, peak RSS, abort `ABORT_MEMORY_RV3B`; z3
30 s hard. Shared files this brief authorises: `bank.py` (the `arch`
key), `certificates.jsonl` (append riscv64 rows), nothing else under
`Research/op_pipeline/`. Never delete anything under `<runs>/` or
`PUBLIC/Airlock/`. Reply with the twin deltas, the bank
before → after, the audit line, the cells-proved count beside 116 / 117,
the readings, the tally, every flag LITERAL.
