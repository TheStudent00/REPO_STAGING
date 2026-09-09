# Task m1 — the arch-opcode model table: every mapping the reference holds, keyed by (mnemonic, operand form, width), with the corpus's attestation, and the alias/split report against the 162

Law: `LAW.md` beside this file — ALL of it, including the last section:
every lane runs on the tower through `remote_lane.sh`. Node:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`
— read its "goal" section (the owner's four set names and his loop; this task is
the first item of that goal) and `~/Programming/PseudoCoupHQ/DevComms/log_234_arch_opcode_mappings_as_fits.md`
§2 and §6, then log_221 §2–§3. Instance `m1.conf` (on the tower; bring it
up yourself with `$R up --instance m1`). Artifact folder:
`~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/model/`; lanes
under `lanes_m1/` there. Task mn1 may still be regenerating the o2/o9/o10
artifacts in the same tree with the field `mnemonic` renamed `mnem`: read
whichever name is present, and write ONLY under your own folder.

## 1. What the objects are, in relation
- The **reference** (`Research/op_pipeline/reference.py`) holds an
  `opcode_table` with one entry per arch mnemonic; an entry names the
  places the opcode reads and writes and a **builder**, a function that,
  given operand texts and a machine state, produces the z3 term the
  opcode writes to each place. That builder IS the opcode's mapping.
- The **sweep** in `Research/op_pipeline/lean/model_translate.py`
  (`shapes_for`, `attempts_for`, `sweep`, `one_attempt`, `run_line`) already
  hands every builder every operand shape it spells at every width and
  records the outcome per (mnem, shape, width): `model_L2.json` holds
  62,418 such rows, 34,867 TRANSLATED, over 171 table mnemonics, each row
  carrying `line`, `operands`, `defs[].writes`. REUSE IT: import that
  module, do not re-implement the sweep.
- The **ruling this task serves** (the owner, 2026-09-08): a mnemonic alone is a
  spelling; (mnemonic, operand form, width) is machine form and is the key.
  One spelling can carry two mappings (`imul` one-operand writes the
  accumulator pair; two-operand writes a destination); several spellings can
  share one (`shl`/`sal` in `build_shift`; the `mov*` suffixes). Whether two
  ROWS compute the same mapping is decided by z3 on their terms, never by
  reading names. Rows are never merged; equivalences are REPORTED.
- The **162** is the corpus's mnemonic vocabulary
  (`Research/oracle/arch_opcodes/unique_opcodes.json`). This task's counts
  are set beside it, not in place of it.

## 2. Deliverable: `model_table.py` → `model_table.json`, `model_table.md`
Field for the mnemonic: `mnem` (the guard's machine-form name). Rows keyed
by (`mnem`, `shape`, `width`), one per sweep attempt that TRANSLATED, with:
1. **the mapping, LITERAL**: for each place written (destination register,
   flags, accumulator pair, memory), the z3 term's layer-5 text as the
   pipeline prints it (`Term` normalize/print from `Research/op_pipeline/term.py`
   if it applies to a bare z3 expr; otherwise `str(z3.simplify(t))`, and
   say which); the operands as symbols in arch order.
2. the write set and the read set of the entry (`entry.reads`, `entry.writes`
   spelled as the reference names them), and whether the mapping reads
   flags (a flag consumer) or only writes them.
3. **the partial region**: a builder that refuses or branches on an input
   condition (division by zero, the `MIN / -1` case, a count operand the
   hardware masks) — read the builder; name the condition as the builder
   states it, or "total" if the builder is total on bit patterns. Every
   DIVISION and WIDE_MULTIPLY row, every SHIFT row, and every row whose
   builder raises `NotModeled` for a value-dependent reason gets this
   column filled from the code, quoted.
4. **attestation**: how many ledger rows in the corpus are produced by this
   (mnem, operand form, width) and in how many units, by ONE stream over the
   canon40 shards (`term66_run.shards()`; the loop in
   `Research/oracle/arch_opcodes/signatures/ledger_signatures.py`
   `census_pass` shows the record and row shape — copy the reading, not the
   holder logic). The operand form of a ledger row is classified into the
   sweep's shape names by the operand TEXTS (register / immediate / memory
   / `%cl`, and count), the width from the register names or the row's own
   size; state the classifier LITERAL and count the rows it could not
   classify, by cause.
5. **equivalences between rows**, REPORTED not applied: for every pair of
   rows at the same (shape, width) whose destination terms are
   textually identical after normalisation, an `identical_text` edge; for
   every pair of mnemonics the reference registers with the SAME builder
   function (`entry.build is other.build`), a `same_builder` edge; and for
   each `same_builder` pair, z3's verdict on the destination terms AND on
   the flags terms separately, 3,000 ms ceiling (`add` and `lea`: expect
   destination equal on the plain form and flags NOT equal, since `lea`
   writes none; say what you find). The spelling guard runs over the json;
   these edges are keyed by row ids, never by tokens.
6. **The counts, beside the 162**: table mnemonics (171) vs corpus
   mnemonics (162): in both / table only / corpus only, LITERAL lists of the
   two differences (the corpus-only ones are the mnemonics the reference
   cannot model: name them); rows TRANSLATED; distinct mappings among them
   after `identical_text` (a number, with the caveat that text identity is
   an under-count of true equivalence); mnemonics that carry more than one
   distinct mapping across their shapes (the splits, `imul` expected),
   listed; alias groups (the `same_builder` groups whose z3 verdicts are
   equal on every written place), listed.
7. NO_BUILDER (6) and NOT_MODELLED rows: counted by cause, the causes
   quoted from the sweep rows.
8. Guard over every json; report (`model_table.md`, sections in the order
   above, five example rows in full: `add` gpr_gpr 32, `imul` gpr_one 32 and
   gpr_gpr 32, `sar` cl_gpr 32, `idiv` gpr_one 32); log (next free number;
   check `ls ~/Programming/PseudoCoupHQ/DevComms | tail` right before
   writing; task mn1 may take one); verifier lane on the tower; PROGRESS
   entry on the arch_unit_oracle node (append only); sync-back; instance
   down.

Memory: the L2 sweep ran under 8g; the shard stream under 12g; state the
bound at 16g inside the 20g cap, sample first, paste peak RSS, named abort
`ABORT_MEMORY_M1`. Stop rules per LAW; in particular a new outcome name or
a new field the brief did not name → flag, do not invent. Reply with the
counts of §6, the five example rows, the `add`/`lea` verdict, the tally,
the two lists.
