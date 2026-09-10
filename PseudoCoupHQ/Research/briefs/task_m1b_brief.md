# Task m1b — closer for the model table: the attestation join that lost 122 of the 162 mnemonics, three defects the table found, and the two shape fixes left from mn1

Law: `LAW.md` beside this file, ALL of it including the tower section.
Read then `task_m1_brief.md` beside it (the task you are closing) and
`PRIVATE/PseudoCoupHQ/DevComms/log_236_task_m1_arch_opcode_model_table.md`
(what it delivered), then `Research/oracle/arch_opcodes/model/model_table.py`.
Instance `m1b.conf` is on the tower (bring it up). Artifact folder: the same
`Research/oracle/arch_opcodes/model/`; lanes under `lanes_m1b/`.

## 1. What is wrong, measured by the coordinator from m1's own artifacts
`model_table_attest.json` holds 219 attested cells; joined to the sweep's
rows, only 136 land on a TRANSLATED row, and those 136 cover **40 of the
corpus's 162 mnemonics**. 122 corpus mnemonics have NO attested cell at
all. log_236 reported "83 attested cells with no TRANSLATED row" and did
not notice the 122. Three mechanical causes, each verified:

| cause | evidence | what is missing |
|---|---|---|
| (a) the WIDTH label disagrees between the two sides for xmm forms | attested `addss xmm_xmm 128`, `cvtss2sd xmm_same 128`; the sweep's rows for the same mnemonics carry `width` 8, 16, 32, 64 — the loop variable, meaningless for an xmm operand | every scalar/packed float mnemonic (`addss addsd divsd cvt* andps orps pand …`) |
| (b) flag CONSUMERS are never read | the classifier copies o10's `census_pass`, which on a ledger row with `produced_by.kind == "flag_pair"` (`mnem` a two-element list, setter then consumer) records the consumer in `seen_as_flag_pair_element` and `continue`s | every `set*`, `cmov*` (0 attested cells each, while the sweep has 660 and 748 TRANSLATED rows for `setne` and `cmovne`) |
| (c) x87 operands `%st`, `%st(i)` have no operand class and no sweep shape | 1,259 rows unclassified, log_236 §3 | the x87 family |
| (d) control transfers (`j*`, `call`, `jmp`, `ret`, `ud2`) produce no value row by nature | — | these are not value cells; they are attested by GUARD rows, a different population, and must be counted as such, never left as "never placed" |

## 2. Deliverable
1. **One width rule, stated LITERAL, applied on BOTH sides.** A cell's
   `width` is the operation's own lane width as the reference's tables give
   it: gpr forms from the register name (as now); xmm scalar forms from
   `FLOAT_BINARY` / `FLOAT_COMPARE_MASK` / `CONVERT_TO_FLOAT` / `LANE_MOVE`
   (32 or 64); whole-register xmm forms (`PACKED_FLOAT`, `BITWISE_128`,
   `WHOLE_MOVE`) 128; x87 80. Add a `key_width` to every sweep row and every
   attested cell computed by that one function in `model_table.py`; leave
   the sweep's own `width` field as it is (the loop label) beside it. Do not
   edit `model_translate.py` for this.
2. **Flag consumers attested**: read `flag_pair` rows; the consumer is
   `mnem[1]`, its operands from the relinked line, its cell keyed like any
   other, with the setter recorded in the cell (`setter`), since the mapping
   reads the flags that setter wrote. Count them.
3. **x87 shapes**: add operand classes for `%st` and `%st(i)` to the
   classifier AND — this is authorised, as an ADDITIVE change to a shared
   file — add shapes `st_st` (`%st,%st(1)`), `st_one` (`%st(1)`), `st_none`
   to `model_translate.shapes_for`, re-run the sweep for the x87 mnemonics
   only, and re-run `check_L2.json`'s 153-row check to show it is unchanged
   (paste its tally). Do NOT recompute same-builder edges for the x87 group
   (log_236 measured ≈24 h there); say so.
4. **Control transfers**: for `j* jmp call ret ud2`, count the ledger's
   guard-outcome rows per mnemonic (the block the ledger records for a
   branch) and report them as `attested_by_guard_rows`, a separate column,
   with the value-cell count 0 by nature.
5. **`build_binary`'s one-operand branch** (log_236 "awaiting"): its first
   line sends any one-operand line to `build_wide_multiply`. Authorised,
   minimal: that branch applies only when `ops.mnemonic in WIDE_MULTIPLY`;
   any other one-operand line raises `NotModeled` naming the reason. Then
   re-run the sweep for `add and or sub xor` and paste the `check_L2` tally
   again (expected unchanged: no one-operand form of those exists in the
   corpus). This is the only change to `reference.py`; show the diff LITERAL.
6. **The coverage table, the acceptance criterion**: one row per corpus
   mnemonic (162): attested value cells with a TRANSLATED row / attested
   cells at a form the sweep does not spell / attested by guard rows only /
   never placed. The four columns sum to 162 rows, and EVERY "never placed"
   carries a cause quoted from the classifier. A mnemonic with a cause that
   is a defect of ours, not of the corpus, is a flag, not a closed row.
7. mn1's two shape fixes: `per_opcode.py`'s field `landed_mnemonic` →
   `landed_mnem`, regenerate o8's results; `single_opcode_units.py`'s
   `zero_opcode_examples` records gain their `lang` field, regenerate o2's.
   Guard over both, pasted.
8. Refresh `model_table.json/.md` (§3, §5 counts with the corrected join,
   the five example rows' attestation) and the guard over every json; log
   (next free number, check right before writing); verifier lane on the
   tower; PROGRESS entry on the arch_unit_oracle node; sync-back; instance
   down.

Memory: as m1 (bound 16g inside 20g, sample first, peak RSS pasted, abort
`ABORT_MEMORY_M1B`). Stop rules per LAW. Reply with the coverage table's
four column totals, the corrected §5 counts, the `check_L2` tallies, the
tally, the two lists.
