---
id: hq.research.arch_unit_oracle.progress
status: living
---

# PROGRESS — arch_unit_oracle

- 2026-09-05: node founded by the owner in a forked conversation, as a
  parallel line that must not interfere with the operator-equivalence
  line. Founding thoughts and proposed order:
  `~/Programming/PseudoCoupHQ/DevComms/log_206_arch_unit_oracle_founding.md`.
  Artifact folder `~/Programming/PseudoCoupHQ/Research/oracle/`
  created. Status: planned.
- 2026-09-05: three sub-nodes registered and generated
  (compiler_units, hub_compiler, cross_construction), definitions
  written by the coordinator. Status: draft, awaiting the owner's naming.
- 2026-09-05, the owner's corrections: compiler_units = the operator SITES
  in the compiler's own source as arch-units, set against the offered
  corpus (not whole-function lowering); hub_compiler's front end =
  tree-sitter (ledgerer where it applies), nesting drives the joins;
  work order = cross_construction FIRST. Definitions rewritten.
- 2026-09-05: task o1 (cross_construction, first measurement)
  started — length-one construction map over `the_pool5.json` per
  ordered language pair, and a bounded length-two feasibility probe
  at the layer-5 term level. done — report
  `~/Programming/PseudoCoupHQ/DevComms/log_207_task_o1_cross_construction_map.md`,
  artifacts `~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/`.
  Coordinator re-derived three length-one cells and the all-five count
  (60) from `the_pool5.json` directly: match. Length one: c and cpp
  build each other ~46-52%; every language builds 45-77% of rust and
  go; length two at depth 2 adds under 3.1% in any cell. Next: task o2,
  gate confirmation of the length-two compositions.
- awaiting the owner: the node and sub-node names, the artifact folder
  name, the `o` instance prefix; the placement of the 11 interpreter
  handler units under compiler_units.
- 2026-09-05/06: task o2 done — per language, the single-arch-opcode
  arch-units under two chaff rules (narrow / wide) grouped by distinct
  body, and the unique arch opcodes per language (162 mnemonics across
  nine languages). Report
  `~/Programming/PseudoCoupHQ/DevComms/log_208_task_o2_single_opcode_units.md`,
  artifacts `~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/`.
  Awaiting the owner: which chaff rule stands; the folder name; the guard
  collision (mnemonics `and`/`or`/`xor`/`not` spell cpp's alternative
  operator tokens, so the spelling guard flags the `mnemonic` field).
- 2026-09-06: cross_construction FROZEN by the owner. Reason: per language,
  only 10-26 of 20-32 compiler-operators lower to a single arch opcode
  (and most of those only on some operand types; comparisons never),
  so one language's single-opcode units cannot build another's. Stays
  frozen unless a way to chain arch-units down to one opcode appears.
  Next: compiler_units (offered vs used), pending the owner's confirmation of
  the table shape.
- 2026-09-06: task o3 (compiler_units) opened — per compiler, the
  grammar operators used in its own source (tree-sitter search, no
  compilation) against the operators offered and the subset the
  corpus has lowered. Sources: llvm-project and rust are SPARSE
  checkouts (codegen dirs only); go and swift full. in-progress.
- 2026-09-06: task o3 done —
  `~/Programming/PseudoCoupHQ/DevComms/log_209_task_o3_compiler_operators_used.md`,
  artifacts `~/Programming/PseudoCoupHQ/Research/oracle/compiler_units/`.
  Every compiler uses every scalar operator the corpus lowered except
  cpp's alternative spellings and `<=>` (clang, swiftc) and `^` (rustc,
  sparse). "Used but not lowered" is entirely assignment/structural
  operators the corpus scoped out. Flags: llvm and rust checkouts are
  sparse; swift stdlib row needs a swift parser in the runner image.
- 2026-09-06: tree-sitter-swift 0.7.3 installed INTO the Airlock image
  (Airlock requirements-analysis.txt); swift standard-library row added
  to task o3's table (log_209 §8), then corrected in §9 after the
  coordinator found `!=`/`<=`/`>=` reported unused against a plain text
  count: the swift grammar puts those under `infix_expression`. Row now
  36 used / 25 in the lowered set / 1 never used (`try!`).
- 2026-09-06: task o4 done — operator VARIANTS (operator × written
  operand types) at every lowered-operator site in each compiler's
  source, resolved by search only (declarations in the same file,
  literals, casts, nested operators), leftovers by reason.
  `~/Programming/PseudoCoupHQ/DevComms/log_210_task_o4_operator_variants_by_search.md`
  (§7 = nested-operand extension). Fully resolved: clang 17%, go
  compiler 22%, go stdlib 20%, rustc 6%, swiftc 11%, swift stdlib 9%.
  Leftover is dominated by call results, member access, inferred
  bindings, and declarations in other files. Next step, the owner's: the
  compiler's own type dump for the leftover.
- 2026-09-06 (task t102, bank, log_214): the founding note and o1-o4
  verified artifact-by-artifact against their own logs (all present).
  Verifier tallies re-run from inside `t102` over logs 206-210: zero
  DIFFERS on every pass that completed; log_207 (o1) fully
  self-contained (5 of 8 claims reproduce); logs 208/209 (o2/o3) carry
  large REFUSED counts because their own re-verification submitted
  lanes to instances `o2`/`o3`, correctly refused when read back from
  `t102`; log_210's (o4) re-verification inside `t102` was killed
  (SIGKILL) at 17 of 18 claims — banked in its place is log_210's OWN
  internal final tally, printed in the log itself: 18 claims, 8
  MATCHES, 0 DIFFERS. Evidence:
  `~/Programming/PseudoCoupHQ/DevComms/log_214_task_t102_bank_rounds_16_19_and_founding.md`.
- 2026-09-07 (the owner's reframing): the line's emulation work is labelled by
  what it emulates. o7/o11/o13 emulate POOL ENTRIES (AutoPoly, level 3);
  o8 and o11's per-opcode rows emulate ARCH OPCODES and are the only runs
  of the owner's loop: 25 of 162 opcodes, targets c and rust. The o9 census keyed
  signatures on DWARF source types, so c's promotions read as opcode
  width changes: wrong level; the model is (mnemonic, width) from the
  reference. New goal in CORE: full model of `set_of_unique_arch_opcodes`
  and the fit study (log_234). No new runs until the portable Airlock is
  on the server.
- 2026-09-08 (task m1, DONE, log_236): the arch-opcode MODEL TABLE, the
  first item of the CORE's "goal" and step 3 of the research master
  order. `~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py`
  runs `model_translate.sweep` (imported, not re-implemented) over the
  reference's whole opcode table and keeps the z3 term of every place
  each attempt writes, printed by `term.Term.normalize`: 62,418 sweep
  attempts, 34,867 TRANSLATED, over 8,703 distinct (mnem, shape, width)
  triples; 5,155 distinct mappings after `identical_text` (2,219
  classes over 961,170 pairs). Beside each row, the corpus's own
  attestation from one stream over the 332 canon40 shards: 130,108
  arch-opcode ledger rows seen, 109,052 placed into 219 cells. Beside
  the 162: all 162 corpus mnemonics are IN the table, corpus-only is
  EMPTY, table-only is the nine archive mnemonics; the mnemonics the
  reference cannot model are the six no-builder entries (`call`, `jmp`,
  `pcmpeqb`, `pcmpeqd`, `pmovmskb`, `ud2`). 86 splits by place kind
  (`imul`: `reg reg` one-operand versus `flags reg` two-operand); 2
  alias groups of 24 same-builder groups (`movapd movaps movdqa`,
  `fstp fstpt`). `add`/`lea`: destination `sat` at all 12 shared cells
  and no flags comparison stated, because `lea` writes none — the
  equality the brief expected holds across two DIFFERENT operand
  shapes, which the machine-form key never pairs. Guard PASSES on all
  four json. Two items flagged for the coordinator in log_236 §12:
  `reference.build_binary`'s one-operand branch (a one-operand
  `add`/`and`/`or`/`sub`/`xor` is modelled as the widening multiply; 24
  rows, 0 attested), and the sweep's shape grammar having no x87
  register operand (1,259 corpus ledger rows unplaceable). Evidence:
  `~/Programming/PseudoCoupHQ/DevComms/log_236_task_m1_arch_opcode_model_table.md`;
  artifacts and lane scripts under
  `~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/model/`.
- 2026-09-08 (task m1b, DONE, log_237): the model table's JOIN closed,
  and the three populations task m1 had not read. The join is now keyed
  by `key_width` — the operation's own lane width, read from the
  reference's own tables by one function in `model_table.py` and applied
  to BOTH sides (x87 80, scalar float 32/64 from `FLOAT_BINARY` /
  `FLOAT_COMPARE_MASK` / `CONVERT_TO_FLOAT` / `LANE_MOVE` /
  `FLOAT_FLAG_ONLY`, whole-register vector 128, everything else the
  width the row already carried) — while the sweep's own `width` stays
  beside it untouched. FLAG CONSUMERS are attested: a flag-pair ledger
  row now attests its READING half with the setter recorded on the cell
  (22,741 rows; `setne gpr_one 8` alone holds 10,335 rows over 6,691
  units, where m1 read 0). The x87 stack has three operand shapes in
  `model_translate.shapes_for` (`st_st`, `st_one`, `st_none` — one of
  the two authorised changes to a shared file), so the 1,259 ledger
  rows that had no shape now sit in 9 cells and the classifier's
  unclassified list is one cause long (the OUT block's repeats).
  CONTROL TRANSFERS are counted as guard rows: 1,201 over 13 branch
  mnemonics, and 0 by nature for `call`, `jmp`, `ret`, `ud2`, measured.
  `reference.build_binary`'s one-operand branch (the other authorised
  change) now applies only to `WIDE_MULTIPLY` and otherwise raises
  `NotModeled`. THE COVERAGE TABLE, the acceptance criterion, sums to
  162: 134 mnemonics with a value cell on a TRANSLATED row (m1 reached
  40), 3 attested at a form with no mapping (all three no-builder
  entries), 17 control transfers, 8 never placed, each with a cause
  measured over the 332 shards. Attested cells 257, of which 253 land
  on a TRANSLATED row (m1: 219 and 136). `check_L2`'s tally is
  unchanged under both changes, read three times: 259 rows, 172 STATED,
  87 REFUSED. Guard PASSES on all four json. mn1's two shape fixes:
  o2's `zero_opcode_examples` records carry `lang` and o2's guard now
  PASSES; o8's `landed_mnemonic` is `landed_mnem` and o8's guard STILL
  FAILS with the same 57 findings, because the guard exempts `mnem`
  exactly — flagged, not worked around. Four items for the coordinator
  in log_237 §14, the first being that `model_translate.load_rows`
  still reads o2's artifact by the old field name and raises
  `KeyError: 'mnemonic'`. Evidence:
  `~/Programming/PseudoCoupHQ/DevComms/log_237_task_m1b_model_table_join_closer.md`;
  artifacts and lane scripts under
  `~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/model/`.
