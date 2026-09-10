# Task ref2 — correcting level 0: the four defects ref1 located in reference.py, each proved against the independent reading, then every term that rests on them re-derived and audited

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in short
calls). Then `task_ref1_brief.md` and `DevComms/log_256` (the finding: four
mechanisms, each one line of `reference.py`; the counterexamples; the
undefined regions), `Research/oracle/arch_opcodes/level0/` (the K parser
and `level0_check.json` — the oracle this task re-runs after each fix),
`reference.py` (`full64`, `build_carry_binary`, `Operands.width_at` and
`WIDTH_IS_NOT_A_SUFFIX`), `condition_table.py` (`cond_to_z3`), `log_233`
(t104: the before/after audit shape for a normaliser change — the same
shape here for a reference change), `log_251` (the L2 check's tally
259/172/87, the guard), the bank (`certificates.jsonl`; `code_version`).
Instance `ref2.conf`. Artifact folder: `Research/oracle/arch_opcodes/level0/`
(the check), `Research/op_pipeline/` (the reference — the ONE authorised
shared change), lanes under `level0/lanes_ref2/`. STARTS ON DEE'S WORD:
the reference is the line's ground truth and every term rests on it.

## 1. The four corrections, each a hardware fact, each proved against the K reading before the next
| # | defect (log_256 cause) | the correction | the fact it rests on |
|---|---|---|---|
| 1 | `full64` zero-extends every sub-64-bit register write | a 32-bit write zero-extends to 64 (as now); an 8- or 16-bit write keeps the register's other bits | Intel SDM Vol. 1 §3.4.1.1: 8/16-bit operands leave the upper 56/48 bits unmodified; the K reading agrees on all 116 places |
| 2 | `build_carry_binary` puts the incoming carry into the destination but not into the flags | the flags are computed from the same sum that includes the carry | 204 places; the K reading agrees |
| 3 | `cond_to_z3` computes every condition on L−R | the condition reads the FLAGS the setter wrote (CF/ZF/SF/OF/PF as the setter's own builder states them), not a re-derivation from operands; L−R stays as the special case it is right for | `add`/`neg` rows disagree today; `sub`/`cmp` rows must not move |
| 4 | `sub`/`sbb` missing from `WIDTH_IS_NOT_A_SUFFIX` | add them (and audit the 34 size-lettered mnemonics: which are genuinely suffixed) | `sub %esi,(%rax)` modelled at 8 bits; 12 places |
After EACH: re-run `level0_check` (agree / disagree / undefined / refused
per place, before → after) and the L2 check (259 / 172 / 87 expected to
hold or to change in a stated direction); paste both.

## 2. Everything that rests on the reference, re-derived and audited
Exactly t104's shape: (a) the model table re-swept (`model_translate`,
and the symbolic-immediate spellings ap5 added, which the table on disk
never received): rows whose term TEXT changed, by mnemonic and place,
with three examples LITERAL per correction; (b) the term store
(`term66_store` → a `term_ref2` store): units whose layer-5 text changed,
counted by which correction moved them, three examples each; the pool
rebuilt over the new texts and the entry count before → after (a merge
or split is a finding, listed); (c) the canon40 proofs are self-consistent
under either reading (a body against its own term) — say so, and re-run
a sample of 200 to show WRAPPED_TEXT_PROVED holds; (d) the bank: every
certificate's `reference_version` (new field, authorised: the sha256 of
`reference.py` and `condition_table.py`) recorded; certificates whose
cell's term text changed are NOT deleted — they are marked
`reference_superseded` and the loop in bank mode re-attempts those keys
(the code-version rule, now including the reference); the audit at 100%
over the moved keys: alarms are expected where the old reading was wrong,
and each is listed with the old and new verdict; (e) the three readings
of the polyfill-complete set before → after.

## 3. What this task does NOT do
Nothing is decided about a disagreement the four corrections do not
close: it is reported as ref1 reported it. The undefined regions are not
"fixed": they are Intel's, recorded, and the corpus-needed reading is
what respects them.

## 4. Deliverable
`level0/ref2.md` (§1 and §2 tables), the corrected `reference.py` and
`condition_table.py` with each diff LITERAL in the log, the new stores
beside the old (nothing overwritten), the bank updated; guard over every
json; log (next free number); verifier lane; PROGRESS on the research
node, the arch_unit_oracle node and the operator_equivalence node (the
reference is its object); sync-back; instance down. Memory: the term
re-derivation streams 332 shards, bound 12g inside the cap, sample first,
peak RSS, abort `ABORT_MEMORY_REF2`. Never delete anything under
`<runs>/` or `PUBLIC/Airlock/`. Reply with the level-0
before → after per correction, the L2 tally, the moved-term counts, the
pool before → after, the bank's alarms, the three readings, the tally,
the two lists.
