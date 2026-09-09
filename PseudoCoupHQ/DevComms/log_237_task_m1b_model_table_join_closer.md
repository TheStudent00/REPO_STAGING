# log 237 — task m1b: closing the model table's join, and the four populations it had missed

Node: `hq.research.arch_unit_oracle`
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`,
its "goal" section of 2026-09-07 and its ruling of 2026-09-08). This closes
task m1 (`~/Programming/PseudoCoupHQ/DevComms/log_236_task_m1_arch_opcode_model_table.md`),
the first item of that goal and step 3 of the research master order
(`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md` §4.2).

Date: 2026-09-08. Instance `m1b` (its conf
`~/Programming/Airlock/instances/m1b.conf`), brought up and down by this
task. Every lane ran on the tower guest through
`bash ~/Programming/Airlock/remote_lane.sh`, per LAW's last section; nothing
but file editing, git and those commands ran on the laptop. A lane log's host
path on the tower is
`~/AirlockRuns/m1b/agent/logs/<stamp>__<lane>.sh.log`;
every attribution below names its file.

Paths inside a pasted command are the ones the lane sees:
`/projects/PseudoCoupHQ` IS `~/Programming/PseudoCoupHQ`, mounted into the
instance. Every rendering is labelled **LITERAL** (the object, quoted) or
**GLOSS** (a plain-words reading beside a literal), per
`object.literal-gloss-analogy`.

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

## §0. What was done and found, in plain words, before any figure

Task m1 built the table of every mapping the reference simulator holds and
set the corpus's own attestation beside each row. The attestation was
joined onto the rows by the mnemonic, the operand shape and the width — and
the two sides do not mean the same thing by "width" when the operand is a
vector or an x87 register. The corpus says a hundred and twenty-eight,
because the ledger row that recorded the instruction holds sixteen bytes;
the table says eight, sixteen, thirty-two and sixty-four, because those are
the general-register widths the sweep's loop walks; and the operation itself
adds one thirty-two-bit lane, which is neither. So most vector cells landed
on no row.

This task made one function decide the width on both sides. It reads the
operation's own lane width out of the reference's own tables — a scalar
float operation is thirty-two or sixty-four bits, a whole-register vector
operation is a hundred and twenty-eight, an x87 register is eighty — and
falls back to the width the row already carried for everything else. The
field the sweep already had is untouched and sits beside the new one, so
nothing was overwritten.

Three populations were missing rather than mis-keyed. The first is the flag
consumers: when the ledger records a comparison and the instruction that
reads its flags, it records the pair, and the census the classifier was
copied from steps over such rows. So every `set` and `cmov` instruction in
the corpus attested nothing at all, while the table carried hundreds of rows
for each. They are now attested by their reading half, with the
flag-setting instruction recorded on the cell, because what the mapping
computes is a function of the flags that setter wrote. The second is the
x87 register stack: the sweep spelled general registers, immediates, memory
and vector registers, and no x87 register, so a line like `faddp %st,%st(1)`
had no shape to be classified into. Three operand shapes were added to the
sweep — this is one of the two changes to a shared file the brief
authorises — and the twelve hundred and fifty-nine ledger rows that had no
cell now have one. The third is the control transfers: a conditional branch
writes no value, so it can never carry a value cell; the ledger attests it
in the guard block instead, and those rows are now counted as what they are.

The other authorised change was to the reference itself. Its binary builder
opened by sending any one-operand line to the widening multiply, so a
one-operand `add` was modelled as a multiply into the accumulator pair. That
branch now applies only to the two mnemonics the widening multiply belongs
to, and any other one-operand line is refused by name.

The result is one row per corpus mnemonic in exactly one of four categories.
A hundred and thirty-four of the hundred and sixty-two now carry an attested
cell that lands on a translated row, where task m1's join reached forty.
Three are attested at a form the table has no mapping for, and all three are
entries the reference registers with no builder at all. Seventeen are
control transfers, thirteen of them carrying guard rows and four —
unconditional — producing no ledger row of any kind. Eight are never placed,
and each was measured one level deeper than the table's own cause: five are
instructions that appear in bodies and produce no value the ledger records,
and two have their rows recorded under a non-opcode phrase rather than under
the opcode.

Two things did not work out as the brief expected, and both are flagged
rather than worked around. The check that had to be shown unchanged could
not run at all: the model translator still reads task o2's artifact by the
field name task mn1 renamed, and raises before it states a theorem. And task
mn1's second shape fix — renaming `landed_mnemonic` to `landed_mnem` — does
not satisfy the guard, because the guard's exempt list holds `mnem` exactly
and not a compound built on it, so the same fifty-seven findings come back
under the new name.

---

## §1. The objects, one sentence each, in relation

- The **model table** is
  `~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py`
  and what it writes beside itself: every mapping the reference's
  `opcode_table` holds, one row per operand form the sweep spells, with the
  corpus's attestation joined onto it.
- The **sweep** is `shapes_for`, `attempts_for`, `sweep`, `one_attempt` and
  `run_line` in
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py`:
  it hands every builder every operand spelling it knows at every width.
  This task added three operand spellings to it and changed nothing else.
- The **reference** is
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/reference.py`: one entry
  per arch mnemonic, each holding the builder that turns operand texts plus
  a machine state into the z3 term the opcode writes. This task changed one
  branch of one builder.
- **`key_width`** is the new function in `model_table.py` that decides the
  width the join is keyed by — the operation's own lane width, from the
  reference's own tables — as against the field `width`, which is unchanged
  and is the sweep's loop variable on a row and the operand's register width
  or the ledger row's byte size on a cell.
- A **flag-pair ledger row** is a row of a canon40 unit's ledger whose
  producer is the PAIR (flag-setting arch opcode, flag-reading arch opcode);
  `produced_by.mnem` is a two-element list, the setter then the consumer.
- A **guard row** is a flag-pair row in the ledger's GUARD block whose
  reading half writes the branch condition rather than a value.
- The **coverage table** is this task's acceptance criterion: one record per
  corpus mnemonic, in exactly one of four categories, in
  `model_table.json`'s `counts.coverage`.
- The **162** is the corpus's mnemonic vocabulary,
  `~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json`.

---

## §2. The one width rule

**LITERAL**, `model_table.py`'s own statement of the rule, in the comment
above `key_width`, printed by lane
`20260909T011704Z__m1b_l22_quotes.sh.log` step [1/6], which runs
`sed -n '185,196p'` over that file (the verifier cannot compare a paste
carrying `->`, so this block cites its lane rather than carrying the
command):

```
#   x87 mnemonic (ledger48.x87_base names it)          -> 80
#   reference.FLOAT_BINARY                             -> its 32 / 64
#   reference.FLOAT_COMPARE_MASK                       -> its 32 / 64
#   reference.CONVERT_TO_FLOAT                         -> its 32 / 64
#   reference.LANE_MOVE                                -> its 32 / 64
#   reference.FLOAT_FLAG_ONLY                          -> 32 / 64, the
#       line `width = 32 if ops.mnemonic.endswith("ss") else 64` of
#       reference.build_float_flag_only
#   `cvtss2sd`                                         -> 64, the
#       `FLOAT_SORT[64]` of reference.build_convert_widen
#   reference.PACKED_FLOAT, BITWISE_128, WHOLE_MOVE    -> 128
#   the further whole-register vector mnemonics below  -> 128
```

The two lines the block stops before are `anything else -> the width the
row already carries`, which is the general-register rule, unchanged.

**GLOSS.** The brief named seven of those tables. Two lines are this task's
extension of the same principle and are flagged as such in §14: the four
compare-only float mnemonics, whose width is read from
`build_float_flag_only`'s own line, and six whole-register vector mnemonics
none of the seven tables holds (`punpckldq punpcklqdq unpckhpd unpcklpd
pextrw pcmpeqb pcmpeqd pmovmskb`, of which the corpus attests six). Without
them those mnemonics keep the m1 defect: the corpus's `punpckldq mem_xmm
128` cannot meet a sweep row at 8, 16, 32 or 64.

**LITERAL**, lane `20260909T004445Z__m1b_l7_smoke.sh.log`, the rule and the
classifier put against each other on operand texts the corpus actually
spells — the left column is the corpus's line, the right is what both sides
now key by:

```
   | faddp %st,%st(1)         | st_st    | 128   | key_width 80   |  |
   | fucomip %st(1),%st       | st_st    | 64    | key_width 80   |  |
   | fldz                     | st_none  | 128   | key_width 80   |  |
   | fldt 0x8(%rsp)           | mem_one  | 128   | key_width 80   |  |
   | setne %al                | gpr_one  | 8     | key_width 8    |  |
   | cmovbe %eax,%ecx         | gpr_gpr  | 32    | key_width 32   |  |
   | addss %xmm1,%xmm0        | xmm_xmm  | 128   | key_width 32   |  |
   | cvtsi2sd %eax,%xmm0      | gpr_xmm  | 32    | key_width 64   |  |
   | ucomiss %xmm1,%xmm0      | xmm_xmm  | 64    | key_width 32   |  |
   | add %esi,%edi            | gpr_gpr  | 32    | key_width 32   |  |
```

**WHERE THE RULE MERGES TWO READINGS, named rather than left silent.**
**LITERAL**, lane `20260909T010950Z__m1b_l20_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for r in d['counts']['attestation_width_merges']:
    print('%-10s %-10s key_width %-4s classifier widths %s'
          % (r['mnem'], r['shape'], r['key_width'],
             r['classifier_widths']))
"
cvtsi2sd   gpr_xmm    key_width 64   classifier widths [32, 64]
cvtsi2ss   gpr_xmm    key_width 32   classifier widths [32, 64]
```

**GLOSS.** For the convert family what varies between the two forms is the
SOURCE width — `cvtsi2sd %eax,%xmm0` converts a 32-bit integer,
`cvtsi2sd %rax,%xmm0` a 64-bit one — and the rule the brief states reads the
DESTINATION lane, so both land on one key. Two cells in the whole corpus are
affected; the sweep's own `width` sits beside `key_width` on every row, so
the two forms are still distinguishable in the table.

---

## §3. The flag consumers, attested

**LITERAL**, `model_table.py`, the reading that was missing, lane
`20260909T011704Z__m1b_l22_quotes.sh.log`:

```
$ sed -n '838,843p' /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py
def flag_pair_rows(record):
    """every ledger row whose producer is the PAIR (flag-setting arch
    opcode, flag-reading arch opcode), except the OUT block's answer
    row, which repeats the producer of the row it copies.

    `produced_by.mnem` is a two-element list on such a row: the setter
```

**LITERAL**, lane `20260909T005037Z__m1b_l9_attest.sh.log`, the stream's own
counts:

```
   [332/332] shards read, 31078 units, 130108 arch-opcode rows, 23942 flag-pair rows
   257 cells over 130108 arch-opcode ledger rows and 23942 flag-pair rows
   1201 guard rows over 13 branch mnemonics
   2 cells merge more than one classifier width under one key_width
```

**GLOSS.** 23,942 flag-pair rows carry a line; 1,201 of them name a branch
and are counted as guard rows (§5), and the remaining 22,741 are value cells
for the reading mnemonic. The OUT block's flag-pair rows — 9,723 of them —
are excluded by the same rule task m1 applied to the OUT block's arch-opcode
rows: that row repeats the producer of the row it copies, so counting it
counts one instruction twice.

**ONE CELL IN FULL, LITERAL**, lane
`20260909T010950Z__m1b_l20_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
for row in d['rows']:
    if row['mnem'] != 'setne' or row['shape'] != 'gpr_one':
        continue
    if row['key_width'] != 8 or row['outcome'] != 'TRANSLATED':
        continue
    a = row['attestation']
    print(row['row_id'], row['text'], 'preseeded', row['preseeded'])
    print('  ledger rows %d, of which flag-pair %d, units %d'
          % (a['ledger_rows'], a['flag_pair_rows'], a['units']))
    print('  setters:', ' '.join('%s=%d' % (s['mnem'], s['ledger_rows'])
                                 for s in a['setter']))
    break
"
r64052 setne %dil preseeded True
  ledger rows 10335, of which flag-pair 10335, units 6691
  setters: or=1252 test=5691 ucomiss=1164 ucomisd=432 cmp=1266 fucomip=472 fucomi=57 sbb=1
```

**GLOSS.** Task m1 recorded 0 attested cells for `setne` while the sweep
carried 660 TRANSLATED rows for it. It now carries 10,335 ledger rows over
6,691 units, every one of them a flag-pair row, and the cell names the eight
flag-setting mnemonics whose flags those rows read. `preseeded True` is the
sweep's own second pass: a mnemonic that READS the flags leaves nothing on a
state where the flags are empty, so the sweep hands it a state whose flags
are free symbols — which is exactly the shape a flag consumer's mapping has.

---

## §4. The x87 shapes

**LITERAL**, the whole of this task's first change to a shared file
(`git log -p -1 -- Research/op_pipeline/lean/model_translate.py`, commit
`394f9d93`):

```
@@ -238,6 +238,21 @@ def shapes_for(width):
         ("imm_xmm_gpr", ["$0x1", XMM_B, a]),
         ("imm_gpr_xmm", ["$0x1", b, XMM_A]),
         ("none", []),
+        # THE X87 REGISTER STACK, added 2026-09-08 by task m1b, whose
+        # brief authorises exactly these three and nothing else.  The
+        # x87 stack is the one place the reference models that this
+        # list had no spelling for, so `faddp %st,%st(1)` -- 1,259
+        # ledger rows of the corpus -- had no shape to be classified
+        # into and every x87 mnemonic's attestation collapsed onto
+        # `mem_one`.  These three carry no width of their own: an x87
+        # register is 80 bits whatever the loop variable says, and the
+        # operand texts are the same at all four widths.  `st_none` is
+        # spelled apart from `none` because an x87 opcode with no
+        # operand (`fldz`, `faddp`) reads and writes the stack, which
+        # a general opcode with no operand does not.
+        ("st_st", ["%st", "%st(1)"]),
+        ("st_one", ["%st(1)"]),
+        ("st_none", []),
     ]
     return out
```

**LITERAL**, lane `20260909T010950Z__m1b_l20_claims.sh.log`, the cells those
three shapes gave the corpus:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
seen = []
for row in d['rows']:
    if row['shape'] not in ('st_st', 'st_one', 'st_none'):
        continue
    if row['outcome'] != 'TRANSLATED':
        continue
    if row['attestation']['ledger_rows'] == 0:
        continue
    key = (row['mnem'], row['shape'])
    if key in seen:
        continue
    seen.append(key)
    print('%-10s %-8s key_width %-4s rows %d units %d'
          % (row['mnem'], row['shape'], row['key_width'],
             row['attestation']['ledger_rows'],
             row['attestation']['units']))
print('x87 cells attested at an st shape:', len(seen))
"
fldz       st_none  key_width 80   rows 321 units 321
faddp      st_st    key_width 80   rows 30 units 30
fdivp      st_st    key_width 80   rows 15 units 15
fdivrp     st_st    key_width 80   rows 15 units 15
fmulp      st_st    key_width 80   rows 30 units 30
fsubp      st_st    key_width 80   rows 15 units 15
fsubrp     st_st    key_width 80   rows 15 units 15
fucomi     st_st    key_width 80   rows 108 units 57
fucomip    st_st    key_width 80   rows 1031 units 1031
x87 cells attested at an st shape: 9
```

**GLOSS, and the arithmetic that ties it to log_236.** Those nine cells hold
1,580 ledger rows. 1,259 of them are exactly the rows log_236 §8 reported as
unclassifiable ("an operand text this classifier does not read: '%st(1)'",
1,139, and "'%st'", 120); the remaining 321 are `fldz`, which was classified
into the general `none` shape before and now sits in `st_none`. The
classifier's unclassified list is now one cause long — **LITERAL**, lane
`20260909T005037Z__m1b_l9_attest.sh.log`:

```
   unclassified rows, by cause:
       19797  the answer row of the OUT block, which canonical_form.wrap_unit adds AFTER the dataflow walk: it repeats the producer of the row it copies, so the relink gives it no line of its own and counting it would count one instruction twice
           0  the unit's body could not be relinked, so no row of it has a line
```

**THE SAME-BUILDER EDGES WERE NOT RECOMPUTED FOR THE X87 GROUP**, as the
brief instructs. `model_table.cells_of_pair` skips the three added shapes,
so the same-builder cell population is exactly the one task m1 decided —
51,670 cells against m1's 51,730, the difference being the one-operand
binary rows §6 removed. The reason, quoted from the code: the x87 group's
terms are 80-bit floating point, every solver call on them reaches the
3,000 ms ceiling, and log_236 §10 measured that pass at about 24 hours.

---

## §5. The control transfers

**LITERAL**, `model_table.py`, the test that separates the two populations —
it reads the reference's own entry, never the token; lane
`20260909T011704Z__m1b_l22_quotes.sh.log`:

```
$ sed -n '861,866p' /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py
def writes_the_branch_condition(mnem):
    """does the reference's own entry for this mnemonic write the
    branch condition rather than a value?

    This is the machine-form test that separates the two populations
    the brief names: a flag consumer that writes a register leaves a
```

**LITERAL**, lane `20260909T011911Z__m1b_l24_transfers_again.sh.log`
(lane `20260909T011037Z__m1b_l21_one_operand.sh.log` read the same split
with `> 0` where this one reads `!= 0`; the log verifier refuses a pasted
command carrying a bare `>`, which bash would read as a redirection):

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
with_rows = []
without = []
for r in d['counts']['coverage']:
    if not r['category'].startswith('a control transfer'):
        continue
    if r['attested_by_guard_rows'] != 0:
        with_rows.append('%s=%d' % (r['mnem'], r['attested_by_guard_rows']))
    else:
        without.append(r['mnem'])
print('with guard rows (%d): %s' % (len(with_rows), ' '.join(with_rows)))
print('with none, by nature (%d): %s' % (len(without), ' '.join(without)))
"
with guard rows (13): ja=6 jae=164 jb=50 jbe=126 je=139 jg=15 jge=20 jl=155 jle=29 jne=34 jns=1 jo=37 js=425
with none, by nature (4): call jmp ret ud2
```

**GLOSS, with both sides of the contrast named.**

- **Attested by guard rows (13 mnemonics, 1,201 rows).** A conditional
  branch writes `the branch condition the walk forks on` — the reference's
  own words — so it never leaves a value the ledger can hold. The ledger
  records it as the reading half of a GUARD-block flag pair, and that is its
  attestation.
- **No ledger row of any kind (4 mnemonics: `call`, `jmp`, `ret`, `ud2`).**
  Measured, not assumed: lane `20260909T002030Z__m1b_l2_probe.sh.log`
  streamed all 332 shards and printed `ledger rows produced by a control
  transfer: {}`. An unconditional transfer produces no value, so the ledger,
  which holds one row per value produced, holds none. The count is 0 by
  nature, not by omission, and the coverage table says so on the row.

---

## §6. The reference's one-operand branch

**LITERAL**, the whole of this task's second change to a shared file
(`git log -p -1 -- Research/op_pipeline/reference.py`, commit `9926e8e7`):

```
@@ -784,8 +784,21 @@ def build_spread_sign(ops):
 
 def build_binary(ops):
     if len(ops.texts) == 1:
-        build_wide_multiply(ops)
-        return
+        # CORRECTED 2026-09-08 by task m1b (log_236 section 9, second
+        # item).  This branch used to send EVERY one-operand line of
+        # the binary family to the widening multiply, so `add %edi`
+        # was modelled as `%eax = %edi * %eax`, and the same for
+        # `and`, `or`, `sub` and `xor` -- 24 table rows the corpus
+        # attests zero times.  The one-operand form is the
+        # accumulator-pair widening multiply and belongs to the two
+        # mnemonics that spell it.
+        if ops.mnemonic in WIDE_MULTIPLY:
+            build_wide_multiply(ops)
+            return
+        raise NotModeled(
+            "a one-operand line of %r is not modeled: the one-operand "
+            "form is the accumulator-pair widening multiply, which is "
+            "not this mnemonic's" % ops.mnemonic)
     width = ops.destination_width()
     left = ops.read(1, width)
     right = ops.read(0, width)
```

**LITERAL**, lane `20260909T011037Z__m1b_l21_one_operand.sh.log`, what the
table's one-operand rows became:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
tally = {}
example = {}
for row in d['rows']:
    if row['shape'] not in ('gpr_one', 'mem_one'):
        continue
    if row['builder'] != 'build_binary':
        continue
    key = (row['mnem'], row['outcome'])
    tally[key] = tally.get(key, 0) + 1
    if key not in example:
        example[key] = row.get('reason') or (row.get('text') or '')
for key in sorted(tally, key=str):
    print('%-6s %-32s %2d  %s'
          % (key[0], key[1], tally[key], example[key][:96]))
"
add    NOT_MODELLED_BY_THE_REFERENCE     8  a one-operand line of 'add' is not modeled: the one-operand form is the accumulator-pair widenin
and    NOT_MODELLED_BY_THE_REFERENCE     8  a one-operand line of 'and' is not modeled: the one-operand form is the accumulator-pair widenin
imul   NOT_MODELLED_BY_THE_REFERENCE     4  the memory operand '(%rsi)' of 'imul' states no width, and no other operand of the line states o
imul   TRANSLATED                        4  imul %dil
or     NOT_MODELLED_BY_THE_REFERENCE     8  a one-operand line of 'or' is not modeled: the one-operand form is the accumulator-pair widening
sub    NOT_MODELLED_BY_THE_REFERENCE     8  a one-operand line of 'sub' is not modeled: the one-operand form is the accumulator-pair widenin
xor    NOT_MODELLED_BY_THE_REFERENCE     8  a one-operand line of 'xor' is not modeled: the one-operand form is the accumulator-pair widenin
```

**GLOSS.** `imul` keeps the one-operand mapping, which is the accumulator
pair, and the other five are refused by name. The corpus loses nothing:
**LITERAL**, same lane, `ledger rows attesting a one-operand binary-family
row: 2` — both of them `imul`'s, exactly as log_236 §9 measured before the
change.

**A CONSEQUENCE WORTH NAMING, because it moves a column of the report.**
`model_table.partial_region` quotes every statement of a builder's source
carrying `raise NotModeled(`, `shift_mask(` or `z3.If(`. The new refusal is
such a statement, so the whole binary family's `condition` column now reads
it, where task m1 printed "total on bit patterns". The condition is a
refusal on the NUMBER of operands, not on a value, and log_236 §2 had named
that branch as the thing those three marks did not catch. Nothing about the
mappings changed; the column now shows a condition that was always there.

---

## §7. The coverage table — the acceptance criterion

**LITERAL**, lane `20260909T010950Z__m1b_l20_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
total = 0
for r in d['counts']['coverage_totals']:
    total = total + r['mnemonics']
    print('%3d  %s' % (r['mnemonics'], r['category']))
print('%3d  SUM' % total)
"
134  a value cell on a TRANSLATED row
  3  attested at a form the sweep does not spell
 17  a control transfer -- attested by guard rows and never by a value cell
  8  never placed
162  SUM
```

Table 1 — the four columns, with what each counts and how it moved.

| category | mnemonics | task m1's reading | what it means |
|---|---|---|---|
| a value cell on a TRANSLATED row | 134 | 40 | the corpus's own rows for it land on a mapping the table holds |
| attested at a form the sweep does not spell | 3 | — | `pcmpeqb`, `pcmpeqd`, `pmovmskb` |
| a control transfer | 17 | counted as "never placed" | 13 with guard rows, 4 unconditional with none |
| never placed | 8 | — | each with its cause, §7.2 |

### §7.1 The three attested at a form with no mapping

**LITERAL**, lane `20260909T010453Z__m1b_l15_assemble2.sh.log`:

```
   pcmpeqb    the reference registers it with no builder -- 'no z3 term is written for this arch opcode yet' -- so the sweep states one NO_BUILDER row for it and no row at any shape; the corpus spells it at shape 'mem_xmm'
   pcmpeqd    the reference registers it with no builder -- 'no z3 term is written for this arch opcode yet' -- so the sweep states one NO_BUILDER row for it and no row at any shape; the corpus spells it at shape 'xmm_same'
   pmovmskb   the reference registers it with no builder -- 'no z3 term is written for this arch opcode yet' -- so the sweep states one NO_BUILDER row for it and no row at any shape; the corpus spells it at shape 'xmm_gpr'
```

**GLOSS.** All three are among the six NO_BUILDER entries log_236 §7 listed.
The cause is not a defect of this join: the reference states no mapping for
them at any shape, so there is nothing for their four attested cells (4 of
257) to land on. The other three NO_BUILDER entries — `call`, `jmp`, `ud2` —
are control transfers and sit in the third column.

### §7.2 The eight never placed, each measured

The table's own cause for all eight is that no ledger row of the corpus
names them as a producer. That is true and it is not enough, so lane
`20260909T010546Z__m1b_l16_never_placed_cause.sh.log` measured one level
deeper: how many body lines of the 332 shards spell each, how many of those
lines the relink ties to a ledger row at all, and what that row's producer
is when it does. **LITERAL**:

```
   | mnem | body lines | lines the relink ties to a row |
   | cwtd     |      8 |      0 |
   | fstp     |   1037 |      0 |
   | fstpt    |    126 |      2 |
   | fxch     |    324 |      0 |
   | movb     |     15 |     15 |
   | nop      |    154 |      0 |
   | nopl     |     34 |      0 |
   | pop      |   3372 |      0 |

   where a linked line's row is attributed:
      movb     -> kind non_opcode_phrase  mnem None         15
      fstpt    -> kind non_opcode_phrase  mnem None         2

   o2's own narrow chaff rule, LITERAL:
      NARROW_BARE      = ['nop', 'pop', 'push', 'ret']
      NARROW_PURE_MOVE = ['mov', 'movabs', 'movapd', 'movaps', 'movd', 'movq', 'movsd', 'movss']

   one example body line each: {'pop': ('go/op_103', 'pop %rbp'), 'nopl': ('go/op_103', 'nopl (%rax)'), 'nop': ('go/op_103', 'nop'), 'movb': ('rust/op_786', 'movb $0x0,0x8(%rdi)'), 'fstpt': ('c/regen_305', 'fstpt -0x18(%rsp)'), 'fstp': ('c/regen_34', 'fstp %st(0)'), 'fxch': ('c/regen_15842', 'fxch %st(1)'), 'cwtd': ('go/regen_138', 'cwtd')}
```

Reported by cause, each with a status:

- **Produces no value the ledger records — 6 mnemonics, CLOSED.** `nop`
  (154 lines) and `nopl` (34) compute nothing; `pop %rbp` (3,372) restores a
  saved register, and `nop`, `pop`, `push` and `ret` are exactly task o2's
  own narrow chaff set, quoted above; `fstp %st(0)` (1,037) and `fxch
  %st(1)` (324) permute or discard an x87 stack position; `cwtd` (8) spreads
  the sign across the accumulator pair. Not one of their lines is tied to a
  ledger row.
- **The line IS tied to a row, and the ledger names a non-opcode phrase as
  its producer — 2 mnemonics, OPEN, flagged in §14.** All 15 `movb $0x0,
  0x8(%rdi)` lines and 2 of the 126 `fstpt -0x18(%rsp)` lines carry a row
  whose `produced_by.kind` is `non_opcode_phrase`. An arch opcode's write is
  recorded under a phrase, so no arch-opcode cell can ever exist for it,
  whatever this table does. That is a fact about the ledger, upstream of
  this task.

---

## §8. The counts of the model table, with the corrected join

**LITERAL**, lane `20260909T010950Z__m1b_l20_claims.sh.log`:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
c = d['counts']
print('table %d corpus %d both %d table_only %d corpus_only %d'
      % (c['table_mnemonics'], c['corpus_mnemonics'], c['in_both'],
         len(c['table_only']), len(c['corpus_only'])))
print('attempts %d translated %d triples %d distinct_mappings %d'
      % (c['sweep_attempts'], c['rows_translated'],
         c['translated_triples'],
         c['distinct_mappings_after_identical_text']))
print('identical_text pairs %d classes %d splits %d alias_groups %d'
      % (c['identical_text_pairs'], len(d['identical_text_classes']),
         len(c['mnemonics_with_several_mappings']),
         sum(1 for g in c['alias_groups'] if g['is_an_alias_group'])))
print('attested cells %d placed %d unplaced %d'
      % (c['attested_cells'], c['attested_cells_placed'],
         len(c['attested_cells_with_no_translated_row'])))
print('mnemonics with a placed cell %d, guard rows %d, flag-consumer rows %d'
      % (c['mnemonics_with_a_placed_cell'], c['guard_rows_total'],
         c['flag_consumer_rows']))
"
table 171 corpus 162 both 162 table_only 9 corpus_only 0
attempts 71778 translated 36903 triples 6218 distinct_mappings 5311
identical_text pairs 1072270 classes 2291 splits 86 alias_groups 2
attested cells 257 placed 253 unplaced 4
mnemonics with a placed cell 134, guard rows 1201, flag-consumer rows 22741
```

Table 2 — every count of the table's §5, task m1's reading beside it, and
why each moved. Population: the reference's `opcode_table` and the canon40
corpus's 332 shards, as of 2026-09-08.

| what | m1b | m1 | why it moved |
|---|---|---|---|
| table mnemonics | 171 | 171 | — |
| corpus mnemonics | 162 | 162 | — |
| in both / table only / corpus only | 162 / 9 / 0 | 162 / 9 / 0 | — |
| sweep attempts | 71,778 | 62,418 | the three added shapes, at four widths, over both sweep passes |
| rows TRANSLATED | 36,903 | 34,867 | the x87 rows the three shapes gave, less the one-operand binary rows §6 refused |
| distinct (mnem, shape, key_width) triples with a TRANSLATED row | 6,218 | 8,703 (on `width`) | the key is now the operation's own width, so a vector mnemonic's four loop widths are one key rather than four |
| distinct mappings after `identical_text` | 5,311 | 5,155 | the x87 rows |
| `identical_text` pairs / classes | 1,072,270 / 2,291 | 961,170 / 2,219 | the x87 rows |
| splits | 86 | 86 | — |
| alias groups | 2 | 2 | — |
| attested cells | 257 | 219 | the flag consumers and the x87 shapes |
| attested cells that land on a TRANSLATED row | 253 | 136 | the one width rule |
| attested cells with no TRANSLATED row | 4 | 83 | 82 of m1's 83 were vector cells at width 128 |
| corpus mnemonics with at least one placed cell | 134 | 40 | all four fixes together |
| guard rows | 1,201 | not counted | §5 |
| flag-consumer ledger rows | 22,741 | 0 | §3 |

**THE FIVE EXAMPLE ROWS THE BRIEF NAMES, with their attestation.**
**LITERAL**, same lane:

```
$ python3 -c "
import json
d = json.load(open('/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
want = [('add','gpr_gpr',32), ('imul','gpr_one',32),
        ('imul','gpr_gpr',32), ('sar','cl_gpr',32),
        ('idiv','gpr_one',32)]
for mnem, shape, width in want:
    for row in d['rows']:
        if row['mnem'] != mnem or row['shape'] != shape:
            continue
        if row['width'] != width or row['outcome'] != 'TRANSLATED':
            continue
        a = row['attestation']
        print('%-6s %-8s width %-3s key_width %-4s %s rows %d units %d flag_pair %d'
              % (mnem, shape, width, row['key_width'], row['row_id'],
                 a['ledger_rows'], a['units'], a.get('flag_pair_rows', 0)))
        break
"
add    gpr_gpr  width 32  key_width 32   r00138 rows 11 units 11 flag_pair 0
imul   gpr_one  width 32  key_width 32   r07501 rows 0 units 0 flag_pair 0
imul   gpr_gpr  width 32  key_width 32   r07499 rows 266 units 266 flag_pair 0
sar    cl_gpr   width 32  key_width 32   r12211 rows 335 units 335 flag_pair 0
idiv   gpr_one  width 32  key_width 32   r07409 rows 778 units 389 flag_pair 0
```

**GLOSS.** All five are general-register rows, so `key_width` equals `width`
and their attestation is what log_236 §4 reported, row for row. The row ids
moved because a row id is the attempt's position in the sweep's own output
and the sweep grew; the mappings did not.

---

## §9. The check that had to be unchanged, read three times

**WHAT IT CHECKS, one sentence.** `model_translate.check_command` states
each of task o2's 259 single-opcode rows as a theorem against the model the
sweep builds, or refuses it by cause; the tally of those outcomes is what
must not move when the sweep gains three operand shapes, because adding
shapes changes which model definitions exist and how they are numbered.

Table 3 — the same command, three times, one reading per state of the two
shared files. Every run wrote into a scratch directory under `/work`, never
into `Research/op_pipeline/lean`.

| state of the shared files | rows | STATED | REFUSED | definitions | lane log |
|---|---|---|---|---|---|
| neither change (the baseline) | 259 | 172 | 87 | 3,946 | `20260909T003406Z__m1b_l4_check_baseline2.sh.log` |
| the three x87 shapes only | 259 | 172 | 87 | 3,946 | `20260909T003747Z__m1b_l5_check_after_shapes.sh.log` |
| both changes | 259 | 172 | 87 | 3,910 | `20260909T004110Z__m1b_l6_check_after_reference.sh.log` |

**LITERAL**, the third of those lanes, which carries both changes:

```
[1/2] task m1b: the shapes the sweep spells now
   shapes_for(32): 23 -- gpr_gpr gpr_same gpr_one imm_gpr cl_gpr mem_gpr gpr_mem lea_mem imm_gpr_gpr cl_gpr_gpr xmm_xmm xmm_same gpr_xmm xmm_gpr mem_xmm xmm_mem mem_one imm_xmm_gpr imm_gpr_xmm none st_st st_one st_none
   attempts_for('add'): 92
[2/2] task m1b: model_translate.check_command, redirected
rows: 259
  REFUSED                  87
  STATED                   172
definitions after the check: 3946
   check wall 168.7 s
```

(The block above is lane `20260909T003747Z__m1b_l5_check_after_shapes.sh.log`
— the shapes-only reading. The both-changes lane prints the same three
lines with `definitions after the check: 3910`.)

**GLOSS on the one number that moved.** The tally is identical in all three
readings: no theorem the check states, and no refusal it records, depends on
either change. The definition count falls by 36 in the third reading, which
is the 40 one-operand binary rows §6 refused, less the 4 that were already
refused for want of a width — the definitions those rows used to add to the
model, and nothing else.

**THE CHECK COULD NOT RUN AT ALL AT FIRST, and that is a flag, not a fix.**
**LITERAL**, lane `20260909T003036Z__m1b_l3_check_baseline.sh.log`:

```
  File "/projects/PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py", line 1234, in load_rows
    "mnem": row["mnemonic"],
            ~~~^^^^^^^^^^^^
KeyError: 'mnemonic'
```

`model_translate.load_rows` reads task o2's `single_opcode_units.json` by
the field name task mn1 renamed. The reader was not moved with the field, so
`model_translate.py check` raises before it states a theorem. `model_
translate.py` is a shared file and the brief authorises exactly one change
to it, so this was NOT edited: the three lanes above supply the field name
in their own process (`row.get("mnem")`, falling back to the old spelling)
and are otherwise line for line the shared copy's `load_rows`. The one-line
fix is named in §14.

---

## §10. Task mn1's two shape fixes

### §10.1 o2's zero-opcode examples, FIXED

**LITERAL**, the change in
`~/Programming/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py`:

```
$ sed -n '164,166p' /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py
                    ex.append({"lang": lang, "unit": uid,
                               "operator": operator,
                               "body_text": body_text})
```

**GLOSS.** The guard allows an operator token in an `operator` field only on
a record its `is_unit_object()` recognises, which requires BOTH a language
field and a unit id. These records carried the id and not the language, so
their display label was walked as an ordinary structure field — log_235's
cause D, 30 findings.

**LITERAL**, lane `20260909T010700Z__m1b_l18_o2_regenerate2.sh.log`:

```
   narrow groups in all: 265
   zero-opcode example records, all carrying lang: 30
operator inventory: 91 tokens read from probe_manifest_*.json
PASS single_opcode_units.json -- no operator token in any key, grouping, pairing or row structure
PASS unique_opcodes.json -- no operator token in any key, grouping, pairing or row structure
```

The narrow group count is 265 before and after the regeneration (the lane
prints both), so the population the check of §9 draws its 259 rows from is
unchanged.

### §10.2 o8's landed opcode, RENAMED AS INSTRUCTED, STILL FAILING

`per_opcode.py`'s field `landed_mnemonic` is now `landed_mnem`, and o8's
results were regenerated whole (population, run, report). The guard still
fails, with the same 57 findings under the new name. **LITERAL**, lane
`20260909T010724Z__m1b_l17_o8_regenerate.sh.log`:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS per_opcode_population.json -- no operator token in any key, grouping, pairing or row structure
PASS per_opcode_held.json -- no operator token in any key, grouping, pairing or row structure
FAIL per_opcode_results.json -- 57 spelling-keyed place(s)
     $.results[9].landed_mnem
         operator token 'and' on a structure field -- this is a grouping/row key, not a per-unit label
     $.results[40].landed_mnem
         operator token 'not' on a structure field -- this is a grouping/row key, not a per-unit label
     $.results[42].landed_mnem
         operator token 'or' on a structure field -- this is a grouping/row key, not a per-unit label
```

**GLOSS, and it is mechanical.** The guard's exempt list is
`check_no_spelling_keys.PROSE_FIELDS`, and it holds `mnem` EXACTLY; lane
`20260909T011704Z__m1b_l22_quotes.sh.log`:

```
$ sed -n '106,109p' /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
PROSE_FIELDS = set(["detail", "why", "note", "notes", "text", "condition",
                    "description", "docstring", "expression", "source",
                    "refusal", "reason", "mnem", "bytes", "key", "sem_key",
                    "lifted", "meta"])
```

`landed_mnem` is not that string, so the walk treats it as an ordinary
structure field and the value `and` is a finding, exactly as `landed_
mnemonic` was. The rename the brief names cannot reach the outcome the brief
expects; the remedy is one shape further and is put to the coordinator in
§14 rather than taken here, since the brief names the field and not the
shape.

---

## §11. The guard over every json this task wrote

**LITERAL**, lane `20260909T010820Z__m1b_l19_guard.sh.log`:

```
$ python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_attest.json /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_edges.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS model_table.json -- no operator token in any key, grouping, pairing or row structure
PASS model_table_rows.json -- no operator token in any key, grouping, pairing or row structure
PASS model_table_attest.json -- no operator token in any key, grouping, pairing or row structure
PASS model_table_edges.json -- no operator token in any key, grouping, pairing or row structure
```

The guard was not modified and nothing was asked of it. The new fields keep
the same discipline task m1 set: a flag-setting mnemonic is recorded as
`{"mnem": ..., "ledger_rows": n}` records under `setter`, never as a bare
token; every cause is on the field `reason`, which the guard already reads
as prose; the coverage table is a LIST of records carrying `mnem`, never a
dict keyed by one.

**LITERAL**, the companion count over the four program files this task
changed or added, lane `20260909T011704Z__m1b_l22_quotes.sh.log`:

```
$ grep -c exempt /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.md /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py
/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py:0
/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.md:0
/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py:0
/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py:0
```

**GLOSS.** Lane `20260909T010820Z__m1b_l19_guard.sh.log` ran the same count
over all twenty-one lane scripts as well, and every one of them counts 0
except that guard lane itself, which counts 2 — the word inside its own two
`grep -c exempt` command lines. Nothing in this task claims an exemption.

---

## §12. Time and memory

Every lane stated the bound 16 GB resident inside the instance's 20g, with
the named abort `ABORT_MEMORY_M1B` (`resource.getrusage`, checked after
every shard in the streams, every 5,000 rows in the sweep and every 200
cells in the equivalence pass). The abort never fired.

Table 4 — wall clock and peak resident memory, per lane, from the lanes' own
prints.

| lane | what | wall clock | peak RSS |
|---|---|---|---|
| `m1b_l2_probe.sh` | 332 shards, the whole-corpus survey | 4.4 s | 82,544 kB |
| `m1b_l4_check_baseline2.sh` | the check, baseline reading | 167 s | 129,652 kB |
| `m1b_l8_sweep.sh` | the sweep and the terms | 296 s | 206,788 kB |
| `m1b_l9_attest.sh` | 332 shards, three populations | 4.7 s | 85,880 kB |
| `m1b_l10_edges.sh` | 51,670 cells, both verdicts each | 645 s | 1,418,288 kB |
| `m1b_l15_assemble2.sh` | the join, the counts, the report | 5.1 s | 269,208 kB |
| `m1b_l16_never_placed_cause.sh` | 332 shards, the eight measured | 4.1 s | 331,632 kB |

The equivalence pass is the only long one and it is the one m1 tuned: 5,649
solver calls and 57,079 answers re-used from the memo, over 51,670 cells.

---

## §13. Decided, recorded for audit

- **The join is keyed by `key_width` and the sweep's own `width` is left
  untouched beside it**, as the brief states. Where the two disagree the
  table shows both.
- **The width rule was extended to ten mnemonics the brief's seven tables do
  not hold** — the four compare-only float mnemonics and six whole-register
  vector ones — each read from the reference the same way. Without the
  extension `punpckldq`, `punpcklqdq`, `unpckhpd`, `pextrw` and `cvtss2sd`
  keep the defect the rule exists to remove. Named here and in §14 because
  it is this task's reading of the rule, not the brief's own list.
- **A flag consumer's cell records its setters as records under `setter`**,
  as the brief names the field, with each setter's own row count beside it.
- **The OUT block's flag-pair rows are excluded** by the same rule task m1
  applied to the OUT block's arch-opcode rows; 9,723 rows, all of them
  repeats.
- **The same-builder cell population is exactly task m1's**: the three added
  shapes are skipped, so no x87 solver work was redone, as the brief
  instructs.
- **The three check readings were taken by staging the two changes** — the
  reference's change was reverted for the second reading and restored for
  the third — so each tally is attributable to one change.
- **The check lanes wrote into `/work`, never into
  `Research/op_pipeline/lean`**: `check_L2.json` and the ModelCheck `.lean`
  files there are that folder's own artifacts, and the stored `check_L2.json`
  carries a later `run` pass's outcomes, which a re-run of `check` would have
  discarded.
- **`model_table_rows.json`'s row ids all moved**, because a row id is the
  attempt's position in the sweep's output. Every edge in
  `model_table_edges.json` was recomputed against the new ids in the same
  pass; no document holds two id spaces.

---

## §14. Awaiting the owner — flags for the coordinator

Four, each with the evidence above it and none of them worked around.

1. **`model_translate.load_rows` cannot read task o2's artifact** (§9). It
   reads `row["mnemonic"]` where the regenerated `single_opcode_units.json`
   says `mnem`, so `model_translate.py check` raises `KeyError: 'mnemonic'`
   before stating a theorem. One line in a shared file this brief does not
   name; task mn1's rename left it behind. Until it is changed, the L2
   check runs only with a caller that supplies the field name.
2. **Renaming `landed_mnemonic` to `landed_mnem` does not satisfy the
   guard** (§10.2). The guard exempts `mnem` exactly; a compound name built
   on it is walked as an ordinary field, so the same 57 findings return. The
   shape that would satisfy the guard by the ruling's own mechanism is to
   carry the landed opcode as a record whose field IS `mnem` — for example
   `record["landed"] = {"mnem": landed}` — which is a change of record
   shape, not the rename the brief names, so it was not made.
3. **`st_st` covers two operand orders and the table holds one.** The corpus
   spells the x87 register pair in both orders: the arithmetic-pop family
   writes `%st,%st(1)` (120 rows) and the compares write `%st(1),%st` (1,139
   rows, `fucomip` and `fucomi`), measured in lane
   `20260909T002030Z__m1b_l2_probe.sh.log`. The brief authorises the shape
   `st_st` spelled `%st,%st(1)`, so both orders classify into it and the
   cell's mapping is the first order's. For `fucomip` the two orders name
   different sides of the comparison, so its 1,031 attested rows sit against
   a mapping computed for the other order.
4. **Two mnemonics' rows are recorded under a non-opcode phrase** (§7.2).
   All 15 `movb` lines and 2 `fstpt` lines are tied to a ledger row whose
   `produced_by.kind` is `non_opcode_phrase`, so an arch opcode's write is
   attested under a phrase and no arch-opcode cell can exist for it. That is
   a fact about the ledger, upstream of this table.

---

## §15. The verifier's tally

`check_conventions_log_claims.py --verify --timeout 20` was run over this log
from this task's own instance on the tower, as LAW's final lane. **LITERAL**,
lane `20260909T011954Z__m1b_l25_verify2.sh.log` (host path
`~/AirlockRuns/m1b/agent/logs/20260909T011954Z__m1b_l25_verify2.sh.log`):

```
population: 26 claims across 1 logs
  MATCHES          14
  DIFFERS          0
  UNVERIFIABLE     12
  REFUSED          0
  NOT_RERUNNABLE   0

ONE LINE: 14 of 26 claims reproduce; 12 (46%) carry nothing to re-run

causes, by name:
  attribution_only                 12
```

The first verify lane (`20260909T011814Z__m1b_l23_verify.sh.log`) read 12
MATCHES, 1 DIFFERS, 1 REFUSED and 1 NOT_RERUNNABLE. All three were defects in
THIS LOG and were fixed in it, never in the verifier:

- the DIFFERS was a transcription slip — one line of a pasted table had been
  typed with its last letter missing (`widenin` for `widening`), and the
  paste is now the lane's own;
- the REFUSED was a pasted command carrying a bare `>` inside a python
  comparison, which bash would read as a redirection; the same reading was
  re-run as `!= 0` (lane `m1b_l24_transfers_again.sh`) and that transcript is
  what §5 now carries;
- the NOT_RERUNNABLE was the width rule's own comment block, whose `->`
  arrows the verifier reads as a hand-written gloss; it is now an
  attribution naming the lane and the exact `sed` its step ran.

The 12 UNVERIFIABLE claims are all one shape — a fenced block of a LANE's
output, introduced by an attribution naming that lane's log file, which is
the shape LAW requires for work that ran inside a lane rather than in a
command a reader can re-run. This section itself was appended after the run,
so it is not among the 26 claims the tally counts.
