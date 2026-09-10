# log 254 — task hub2: Hub v2, the dictionary at two levels — the cells read from the bank, the comparison and its consumer as one pair entry, the operator body as a pool entry, and the holders on every entry

Node: `hq.research.arch_unit_oracle.hub_compiler`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/`),
its CORE's "definition" of 2026-09-07 (SOURCE COMPOSITION) and its four
sub-nodes front_end, dictionary, joiner, oracle_test. Line: steps 4 and 5
of the master order,
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/CORE_0_3_research.md`
§4.2. Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, read in full
including its tower section. Brief:
`PRIVATE/PseudoCoupHQ/Research/briefs/task_hub2_brief.md`.
Inputs: task hub1's report `log_252` (its §5 decisions and §6 "Awaiting
the owner" are this task's three holes) and task bank1's `log_253` (the
certificates the dictionary is now read from).
Date: 2026-09-10. Instance `hub2`, on the tower guest.

Artifact folder: `PRIVATE/PseudoCoupHQ/Research/oracle/hub/` —
new files `hub2.py`, `dictionary2.json` / `.md`, `oracle_test2.json` /
`.md`, `measure2.json`, `hub2_paste_a_pair.py`, and under `handful/` the
four composed files `composed2_c.c`, `composed2_rust.rs`,
`composed2_go.go`, `composed2_go_inlinable.go`. Lane scripts:
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/lanes_hub2/`, sixteen of
them, each kept in the repo as the standing rule of 2026-09-07 requires.
Every lane log named below is on the TOWER
(`<user>@<tower>`) under
`<runs>/hub2/agent/logs/`.

Paths inside a pasted command are the ones the lane sees:
`PseudoCoupHQ` IS `PRIVATE/PseudoCoupHQ`, mounted into
the instance. Every rendering is labelled per the protocol's
`object.literal-gloss-analogy`: **LITERAL** is the object itself,
quoted; **GLOSS** is a plain-words reading beside a literal.

---

# 1. What this is, one sentence per object in relation

* A **CELL** is one (`mnem`, operand shape, `key_width`) row of the
  arch-opcode model table — the machine-form key ruled 2026-09-08.
* A **WRITTEN PLACE** is one destination an opcode writes (`reg_rdi`,
  `flags`, `x87_7`); only a place whose name begins `reg_` is a value a
  composition can pass on.
* A **CERTIFICATE** is task bank1's record about ONE artifact: one
  (cell, target, written place) with the term it was posed on, the
  rendered source and its sha256, the compiler and its flags, the carved
  body and the gate's verdict. **THE BANK**
  (`PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl`)
  holds every certificate of every pass with the strongest per key
  marked `preferred`, and from this task on the dictionary is READ FROM
  IT.
* A **PAIR** is (setter cell, consumer cell): the arch opcode that writes
  a flag state and the arch opcode that reads it, which the corpus's own
  ledgers record as ONE ROW whose `produced_by.mnem` is the two of them.
  The loop renders a consumer's emulation over one setter and the
  rendered function is the comparison then the select, so no flag state
  crosses a node: the pair IS the node.
* A **POOL ENTRY** is one distinct computation of
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/the_pool5.json`, the
  units proved equal collapsed to one entry. Task o7 (log 218) rendered
  an emulation of an entry in c, task o11 (log 226) in rust, and task
  o13 (log 230) re-rendered the disproved ones with the MODE — the guard
  the body carries — in place.
* **THE DICTIONARY, at two levels**: level one is per (target, cell) —
  task hub1's — and level two is per (target, pool entry). Between them
  sits the PAIR, which is level one keyed by the pair rather than by the
  consumer alone. A node resolves to a cell, else to a pair, else to its
  unit's pool entry.
* **THE HOLDERS**: every entry records the parameter holders the proof
  was made over, and the composition refuses a mismatch BY CAUSE.
* **THIS TASK** is the three answers of the brief's §1 built and
  measured, over the SAME handful and the SAME measure task hub1 ran.

**THE ANSWER, in three sentences.** The dictionary now holds **176 cell
entries on c, 175 on rust and 161 on go** (task hub1 held 151 / 151 /
161), **39 / 38 / 34 pair entries**, and **195 / 285 / 0 body entries**.
Of the handful's eight functions **`f5` moved from a hole to PROVED on
c** through the body level, and `f6` and `f8` did not move — each for a
cause named off the record. Over the corpus's own go units the
dictionary composes **325 of 590 to c (290 proved, 32 under caller
extension, 3 disproved) and 276 of 590 to rust (260 + 13, 3 disproved)**,
where task hub1 could ask about 134 units at all.

Three things are said before the numbers so the numbers are not misread.

* **THE 134 UNITS TASK HUB1 ASKED ABOUT ANSWER IDENTICALLY.** Same
  units, same measure, same composition: c 100 composed / 98 proved,
  rust 114 / 112, go 124 composed and 108 proved on the re-pose — every
  figure equal to task hub1's own (§7). What grew is the population, not
  the reading of it.
* **THE PAIR LEVEL IS SMALL, AND ITS SIZE IS THE FINDING.** The corpus's
  go units attest 44 distinct pairs; the dictionary serves **10** of the
  104 units that carry one, because the loop renders each consumer over
  exactly ONE setter — the one that consumer's own attestation records
  the most ledger rows for — at that setter's own width, and every other
  attested pair is at another width. Ignoring the setter's width would
  make it 58, and the setter's width is part of the machine-form key.
* **THREE COMPOSITIONS ARE DISPROVED and they are kept as results.**
  Two are a go `bool` operand carried through c's and rust's own truth
  holder, which collapses every non-zero byte to one while go's own body
  compares the raw byte; the third is a body whose two sides differ
  above the eight bits the node answers in. Each carries the gate's own
  counterexample (§8).

---

# 2. The walkthrough, before any figure

Task hub1 left three holes and the coordinator's brief answered each
with a shape to build. The first day's work was to find out what those
shapes are made of, because none of them is an idea — each is a reading
of an object already on disk.

The **cell level** moved from one pass's store to the bank. A
certificate names its artifact by sha256 but carries no parameter list,
and the brief's third hole is exactly about parameters, so every
preferred certificate is joined back to the RUN that produced it, in the
store the certificate itself names, and the join is checked: the run's
rendered source is hashed and the hash must be the certificate's. All
512 preferred certificates of the three targets joined and all 512
hashed to their certificate. That is where the extra entries come from —
25 more on c and 24 more on rust than task hub1 held — and the passes
they come from are mostly `ap1`, which is the bank's whole point.

The **pair level** is read off two objects that already record it. The
corpus's own ledger marks a flag row with `produced_by.mnem` as a
two-element list, the setter then the consumer; and the loop's own run
record carries a `setter` field naming the setter its emulation was
rendered over, with that setter's own line. Classify both lines with the
model table's own classifier and both sides are keyed the same way. The
first run of the dictionary lane produced ZERO pair entries because the
classifier's register-width table had not been installed in that process
and it refused every general-register operand; the one call was added
and nothing else changed (lane `hub2_l7`).

The **body level** is tasks o7, o11 and o13 read as a lookup keyed by
pool entry id. There is no go column: task o7 renders c and task o11
renders rust, and no renderer of the body level was ever run for go.

Then the same handful and the same measure. The measure's first pass
found two defects of this task's own and each was fixed in the one place
that owned it: a go emulation may call a HELPER function its own file
declares (`sel32`), and task hub1's reader carried the emulation's own
function alone, so all ten go pair compositions failed to build with
`undefined: sel32`; and four go compositions failed with `cannot convert
a (variable of type bool) to type int32`, because go has no conversion
from its truth holder into an integer holder where c and rust both have
one. The first is the composed file's furniture and is now general; the
second is a holder mismatch and is now REFUSED BY CAUSE, which is the
brief's third answer applied on the node's side rather than the entry's.

---

# 3. The dictionary, at two levels (step 4 of the master order)

`PRIVATE/PseudoCoupHQ/Research/oracle/hub/dictionary2.json` and its
reading `dictionary2.md`, both written by
`python3 PseudoCoupHQ/Research/oracle/hub/hub2.py dictionary`
(lane `hub2_l7_dictionary_again.sh`).

Table 1 — entries and holes per target at each level, and the attested
ledger rows the cell level covers, out of the outer set's 133,044.

```
$ sed -n '5,17p' PseudoCoupHQ/Research/oracle/hub/dictionary2.md
## 1. Entries and holes per target, per level

| target | level | entries | ledger rows the entries cover | holes | ledger rows the holes cover |
|---|---|---|---|---|---|
| c | cell | 176 | 104086 | 77 | 28958 |
| c | pair | 39 | -- | 37 | -- |
| c | body | 195 | -- | 92 | -- |
| rust | cell | 175 | 102451 | 78 | 30593 |
| rust | pair | 38 | -- | 37 | -- |
| rust | body | 285 | -- | 106 | -- |
| go | cell | 161 | 98458 | 92 | 34586 |
| go | pair | 34 | -- | 37 | -- |
| go | body | 0 | -- | 137 | -- |
```

**GLOSS.** The cell level's own population is the same 253-cell outer
set task hub1 reported over, so 176 against its 151 is the bank's
recovery measured: 25 cells on c whose proof exists and which the last
pass no longer reached. The pair level's hole count is the pairs go's
own corpus attests that the dictionary cannot serve. The body level's
hole population is the 137 pool entries a corpus go unit belongs to.

Table 2 — the cell entries by the route the loop took to them and by the
kind of certificate the bank prefers, with the passes those certificates
come from.

```
$ sed -n '19,26p' PseudoCoupHQ/Research/oracle/hub/dictionary2.md
## 2. Cell entries per target by route and by the certificate's kind

| target | primitive | primitive+setup | term | `proved` | `proved_under_caller_extension` | the passes the certificates come from |
|---|---|---|---|---|---|---|
| c | 24 | 2 | 150 | 155 | 21 | ap1 128, ap2 31, ap3 7, ap4 7, ap5 3 |
| rust | 21 | 0 | 154 | 154 | 21 | ap1 132, ap2 31, ap3 7, ap4 4, ap5 1 |
| go | 16 | 0 | 145 | 161 | 0 | ap1 124, ap2 23, ap3 10, ap4 3, ap5 1 |
```

**GLOSS, and it is task bank1's finding measured from the other side.**
Only 3 of c's 176 preferred certificates come from the last pass; 128
come from the first. A dictionary read from one pass's store is a
dictionary of that pass.

Table 3 — the cell holes on c, by cause. The other two targets' tables
are `dictionary2.md` §3.

```
$ sed -n '27,38p' PseudoCoupHQ/Research/oracle/hub/dictionary2.md
## 3. Cell holes per target, by cause

### c

| cells | ledger rows | cause |
|---|---|---|
| 61 | 26348 | the cell writes no register place: every place it writes is a flag place, which is not a value a composition can pass on |
| 10 | 505 | z3 found a starting state under which the two sides differ |
| 4 | 1097 | term reads state that is not an arrival register |
| 1 | 384 | the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| 1 | 624 | the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either |
```

**GLOSS.** The 61 flag-only cells are unchanged from task hub1 and they
are not a defect: they are exactly the cells the PAIR level exists to
reach, and at the pair level they are reached as the consumer half of an
entry rather than alone. What the bank closed is the DISPROVED column:
35 cells on c in task hub1's reading, 10 here.

---

# 4. The pair level, and why it is ten units and not fifty-eight

Table 4 — the pairs go's own corpus attests at the setter width the loop
also rendered, off `dictionary2.md` §5. The full table is 44 rows.

```
$ grep -n 'cmp gpr_gpr 8 +' PseudoCoupHQ/Research/oracle/hub/dictionary2.md | head -12
211:| cmp gpr_gpr 8 + seta gpr_one 8 | 1 | -- | -- | -- |
212:| cmp gpr_gpr 8 + setae gpr_one 8 | 1 | -- | -- | -- |
213:| cmp gpr_gpr 8 + setb gpr_one 8 | 1 | proved | proved | proved |
214:| cmp gpr_gpr 8 + setbe gpr_one 8 | 1 | proved | proved | proved |
215:| cmp gpr_gpr 8 + sete gpr_one 8 | 4 | proved | proved | proved |
216:| cmp gpr_gpr 8 + setg gpr_one 8 | 1 | proved | proved | proved |
217:| cmp gpr_gpr 8 + setge gpr_one 8 | 1 | proved | proved | proved |
218:| cmp gpr_gpr 8 + setl gpr_one 8 | 1 | proved | proved | proved |
219:| cmp gpr_gpr 8 + setle gpr_one 8 | 1 | proved | proved | proved |
220:| cmp gpr_gpr 8 + setne gpr_one 8 | 4 | -- | -- | -- |
763:| go/op_491 | binary | bool | bool | bool | `a == b` | -- | `cmp gpr_gpr 8 + sete gpr_one 8` | E00319 |
769:| go/op_527 | binary | bool | bool | bool | `a != b` | -- | `cmp gpr_gpr 8 + setne gpr_one 8` | E00320 |
```

**GLOSS, and it is the whole of the pair level's size.** Every served
pair is at `cmp gpr_gpr 8`, the width the loop's own chosen setter line
`cmp %sil,%dil` has. The same consumers at `cmp gpr_gpr 16`, `32` and
`64` — which is what most of go's corpus attests — have no entry,
because the loop renders each consumer over ONE setter and that one is
8 bits wide. Two rows of the 8-bit block are `--` on every target for a
second and different reason: `seta`, `setae` and `setne` were rendered
over the setters `add` and `test`, so no pair of theirs is over `cmp` at
any width.

Here is the object the pair level buys, and it is not a description.
**LITERAL**, one pair composition and the two bodies the gate compared
(lane `hub2_l14_the_pastes.sh`):

```
$ python3 PseudoCoupHQ/Research/oracle/hub/hub2_paste_a_pair.py
the corpus go unit: go/regen_478
the composed c function:
bool
hub_go_regen_478(int8_t a, int8_t b)
{
    bool hub_t0 = (bool)((uint8_t)(emu_sete_gpr_one_8__reg_rdi__c((uint8_t)(b), (uint8_t)(a))));
    return hub_t0;
}
body A, go's own: cmp %al,%bl; sete %al; ret
body B, the composition: cmp %dil,%sil; sete %al; ret
the gate: z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row
```

**GLOSS.** One call, no flag state crossing anything, and the target's
own compiler emitted the comparison and the select as go's own compiler
did. That is the brief's first answer working: the pair IS the node.

---

# 5. The body level, and the handful's `f5`

Table 5 — how the corpus's 590 go units are named by the corpus at the
three levels.

```
$ sed -n '466,473p' PseudoCoupHQ/Research/oracle/hub/dictionary2.md
## 8. The go side: how each corpus go unit is named

| the levels the corpus names this unit at | go units |
|---|---|
| body | 339 |
| cell, body | 134 |
| pair, body | 104 |
| none | 13 |
```

**GLOSS.** 339 go units are named at the body level ALONE — the
constructs go lowers to a sequence — and they are the population task
hub1 could not ask about at all. The 13 named at no level are the units
whose bodies could not be relinked.

**LITERAL**, the composed `f5_u64_shift` on c, two body-level calls in a
row:

```
$ sed -n '100,106p' PseudoCoupHQ/Research/oracle/hub/handful/composed2_c.c
uint64_t
f5_u64_shift(uint64_t a, uint64_t n)
{
    uint64_t hub_t0 = (uint64_t)((uint64_t)(emu_E00310__go_op_176((uint64_t)(a), (uint64_t)(n))));
    uint64_t hub_t1 = (uint64_t)((uint64_t)(emu_E00316__go_op_218((uint64_t)(hub_t0), (uint64_t)(n))));
    return hub_t1;
}
```

**LITERAL**, the two bodies the gate then compared, off
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/oracle_test2.json`,
`results[*]` for `f5_u64_shift` on c:

| side | the body, LITERAL |
|---|---|
| A, go's own | `mov %rbx,%rcx; shl %cl,%rax; cmp $0x40,%rcx; sbb %rdx,%rdx; and %rdx,%rax; shr %cl,%rax; and %rdx,%rax; ret` |
| B, the composition | `mov %rsi,%rcx; shl %cl,%rdi; shr %cl,%rdi; xor %eax,%eax; cmp $0x40,%rsi; cmovb %rdi,%rax; ret` |

**GLOSS, and it is the CORE's own claim measured a second time.** Go's
own body clamps twice — `sbb`/`and` after the shift, then `and` again —
because it lowered two separate shift constructs. The composition called
two emulations of two whole operator bodies and c's compiler then
lowered ACROSS them, emitting ONE clamp as `cmp $0x40` and a `cmovb`.
The gate proved the two equal. `f5` was a hole in Hub v1 for exactly the
reason the second level exists: go lowers `<<` on `uint64` to six cells
and no cell names it.

---

# 6. The handful (step 5 of the master order), hub1 beside hub2

The file is unchanged: the same
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/handful/handful.go` task
hub1 wrote, eight explicitly typed functions. 13 operator nodes, all 13
typed by go/types, and — this is new — all 13 resolved to a corpus unit,
where task hub1 resolved 9: the four the narrow rule does not hold are
now resolved through the same source-to-source agreement and served, or
not served, by the level that names them.

Table 6 — the eight functions per target, task hub1's verdict then this
task's, and the level each composed at.

```
$ sed -n '25,52p' PseudoCoupHQ/Research/oracle/hub/oracle_test2.md
## 2. The handful, function by function and target by target: task hub1 then task hub2

| function | target | hub1: the gate's verdict | hub1: re-posed without `//go:noinline` | hub2: the gate's verdict | hub2: re-posed without `//go:noinline` | hub2: the levels it composed at |
|---|---|---|---|---|---|---|
| f1_i32_add_sub | c | PROVED | -- | PROVED | -- | cell |
| f2_i32_add_mul | c | PROVED | -- | PROVED | -- | cell |
| f3_i64_add_sub | c | HOLE | -- | HOLE | -- | -- |
| f4_i64_mul | c | PROVED | -- | PROVED | -- | cell |
| f5_u64_shift | c | HOLE | -- | PROVED | -- | body |
| f6_i32_div | c | HOLE | -- | HOLE | -- | -- |
| f7_f64_add_mul | c | PROVED | -- | PROVED | -- | cell |
| f8_i32_select | c | HOLE | -- | HOLE | -- | -- |
| f1_i32_add_sub | rust | PROVED | -- | PROVED | -- | cell |
| f2_i32_add_mul | rust | PROVED | -- | PROVED | -- | cell |
| f3_i64_add_sub | rust | PROVED | -- | PROVED | -- | cell |
| f4_i64_mul | rust | PROVED | -- | PROVED | -- | cell |
| f5_u64_shift | rust | HOLE | -- | HOLE | -- | -- |
| f6_i32_div | rust | HOLE | -- | HOLE | -- | -- |
| f7_f64_add_mul | rust | PROVED | -- | PROVED | -- | cell |
| f8_i32_select | rust | HOLE | -- | HOLE | -- | -- |
| f1_i32_add_sub | go | UNDECIDED | PROVED | UNDECIDED | PROVED | cell |
| f2_i32_add_mul | go | UNDECIDED | PROVED | UNDECIDED | PROVED | cell |
| f3_i64_add_sub | go | UNDECIDED | PROVED | UNDECIDED | PROVED | cell |
| f4_i64_mul | go | UNDECIDED | PROVED | UNDECIDED | PROVED | cell |
| f5_u64_shift | go | HOLE | -- | HOLE | -- | -- |
| f6_i32_div | go | HOLE | -- | HOLE | -- | -- |
| f7_f64_add_mul | go | UNDECIDED | PROVED | UNDECIDED | PROVED | cell |
| f8_i32_select | go | HOLE | -- | HOLE | -- | -- |
```

**GLOSS.** One function moved: `f5_u64_shift` on c, HOLE → PROVED. Five
prove on c where four did; rust and go are unchanged. The brief expected
`f5`, `f6` and `f8` to move and two of the three did not, each for a
cause that is now off the record rather than a shrug.

Table 7 — what did not move, and why. Every cause is `oracle_test2.md`
§3 cut to its last clause; the whole of each is in the file.

| function | target | the level that would have served it, and the cause |
|---|---|---|
| `f3_i64_add_sub` | c | CELL: the bank's entry for `add gpr_gpr 64` on c exists and the composition refuses it — "the emulation `emu_add_gpr_gpr_64__primitive__c` declares its parameter 0 in c's truth holder `bool` … the proof was made over that holder and this node's operand is not in it". BODY: its pool entry E00029 is outside task o7's population — "filter P1 keeps only an entry the target has NO member of, and this entry has 166 member(s) in c" |
| `f5_u64_shift` | rust | BODY: "the dictionary has no proved emulation of the pool entry E00310 on rust: the entry is in the emulation study's population and was not in the run set the pass on record walked" |
| `f5_u64_shift` | go | BODY: "no renderer of the body level was run for go: task o7 renders c and task o11 renders rust" |
| `f6_i32_div` | all three | BODY: "the dictionary has no proved emulation of the pool entry E00302 … the emulation study's filter P2 keeps only an entry that carries a layer-5 text, and this entry carries none" |
| `f8_i32_select` | c, rust | PAIR: "the dictionary has no proved entry for the pair `cmp gpr_gpr 32 + setne gpr_one 8` … the loop renders each consumer over ONE setter … and for this consumer that setter is `test gpr_gpr 8`, which is not the setter this pair is over". BODY: E00163 is outside both populations by filter P1 — it has 429 c members and 429 rust members |
| `f8_i32_select` | go | the same pair cause, and the body level has no go column |

**GLOSS, and it is what the brief's first answer turned out to be worth
on this file.** `f8`'s comparison node no longer fails for want of a
flag state crossing a node — the pair IS resolved, `cmp gpr_gpr 32 +
setne gpr_one 8`, read off go's own body for `a != b`. It fails because
the loop never rendered that pair: it rendered `setne` over `test` at 8
bits. The hole moved from the design to one missing run.

---

# 7. The measure over the corpus's own go units

Body A is not rebuilt: the corpus's own canon40 record for the unit IS
go's own carved body. Body B is the composition of that unit's own
construct for the target, built and carved at the target's own ship
flags.

Table 8 — the measure over TASK HUB1'S OWN POPULATION, the 134 units
that name one cell: hub1's row then hub2's, per target.

```
$ sed -n '88,99p' PseudoCoupHQ/Research/oracle/hub/oracle_test2.md
## 5. The measure over task hub1's own population: hub1 then hub2

The 134 corpus go units task hub1 asked about -- the ones task o2's narrow rule holds and that name exactly one cell. Same units, same measure, so the two rows are the same object twice.

| target | task | units asked | composed | ledger rows the composed cells cover | built and carved | proved | proved under caller extension | disproved | undecided | ledger rows the proved cells cover | proved on the re-pose without `//go:noinline` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | hub1 | 134 | 100 | 56830 | 100 | 98 | 2 | 0 | 0 | 56830 | 0 |
| c | hub2 | 134 | 100 | 56830 | 100 | 98 | 2 | 0 | 0 | 56830 | 0 |
| rust | hub1 | 134 | 114 | 62745 | 114 | 112 | 2 | 0 | 0 | 62745 | 0 |
| rust | hub2 | 134 | 114 | 62745 | 114 | 112 | 2 | 0 | 0 | 62745 | 0 |
| go | hub1 | 134 | 124 | 74677 | 124 | 0 | 0 | 0 | 124 | 0 | 108 |
| go | hub2 | 134 | 124 | 74677 | 124 | 0 | 0 | 0 | 124 | 0 | 108 |
```

**GLOSS.** Every figure equal. The two tasks are the same object twice
on the population they share, which is what makes the rest of the table
readable as growth rather than as drift.

Table 9 — the measure over EVERY corpus go unit, per target.

```
$ sed -n '101,107p' PseudoCoupHQ/Research/oracle/hub/oracle_test2.md
## 6. The measure over EVERY corpus go unit, per target

| target | units asked | composed | built and carved | proved | proved under caller extension | disproved | undecided | ledger rows the composed cells cover | ledger rows the proved cells cover | pool members the composed body entries cover | proved on the re-pose without `//go:noinline` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | 590 | 325 | 325 | 290 | 32 | 3 | 0 | 66173 | 63495 | 3287 | 0 |
| rust | 590 | 276 | 276 | 260 | 13 | 3 | 0 | 72088 | 69410 | 2290 | 0 |
| go | 590 | 132 | 132 | 0 | 0 | 0 | 132 | 81342 | 0 | 0 | 116 |
```

Table 10 — the same measure split by the level each unit was served at.

```
$ sed -n '109,121p' PseudoCoupHQ/Research/oracle/hub/oracle_test2.md
## 7. The measure by level

| target | level | composed | built and carved | proved | proved under caller extension | disproved | undecided | proved on the re-pose without `//go:noinline` |
|---|---|---|---|---|---|---|---|---|
| c | cell | 100 | 100 | 98 | 2 | 0 | 0 | 0 |
| c | pair | 10 | 10 | 8 | 0 | 2 | 0 | 0 |
| c | body | 215 | 215 | 184 | 30 | 1 | 0 | 0 |
| rust | cell | 114 | 114 | 112 | 2 | 0 | 0 | 0 |
| rust | pair | 10 | 10 | 8 | 0 | 2 | 0 | 0 |
| rust | body | 152 | 152 | 140 | 11 | 1 | 0 | 0 |
| go | cell | 124 | 124 | 0 | 0 | 0 | 124 | 108 |
| go | pair | 8 | 8 | 0 | 0 | 0 | 8 | 8 |
| go | body | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
```

**GLOSS, and it is Hub v2's own number.** The body level is where the
growth is: 215 units composed on c and 184 of them proved, against the
100 the cell level reaches. On go every strict verdict is UNDECIDED for
task hub1's one reason — `//go:noinline` on the emulation forbids the
inlining the method rests on — and the re-pose without that one line
proves 116 of 132. The pair level composes 10 on c and rust and 8 on go,
the two missing being the two whose operands are in go's truth holder,
which go cannot spell into an integer holder and which is refused by
cause.

---

# 8. The three disproved compositions, by cause

Two causes, three sightings, and both are results rather than defects.

**CAUSE 1 — a go `bool` operand carried through the target's own truth
holder (2 sightings: `go/op_491` and `go/regen_471`, both on c and on
rust).** LITERAL, the composition and the two bodies, off
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/measure2.json`:

| what | the object |
|---|---|
| the composed c function | `bool hub_go_op_491(bool a, bool b) { bool hub_t0 = (bool)((uint8_t)(emu_sete_gpr_one_8__reg_rdi__c((uint8_t)(b), (uint8_t)(a)))); return hub_t0; }` |
| body A, go's own | `cmp %al,%bl; sete %al; ret` |
| body B, the composition | `mov %edi,%eax; xor %esi,%eax; xor $0x1,%al; ret` |
| the gate | z3 found a starting state under which the two sides differ |
| the counterexample | `[IN_0 = 8, IN_1 = 247]` |

**GLOSS.** c's `bool` parameter holds 0 or 1, so c's compiler lowered
`sete(a, b)` to `1 ^ a ^ b`, which is correct for every value c's own
truth holder can hold. Go's body compares the RAW BYTE that arrives, and
the gate poses over every value of the arriving register: at 8 and 247
the two answer differently. The proof is posed over the register, and a
truth holder is not a faithful holder of a register.

**CAUSE 2 — the two sides differ above the bits the node answers in (1
sighting: `go/regen_146`, on c and on rust).** LITERAL:

| what | the object |
|---|---|
| body A, go's own | `push %rbp; mov %rsp,%rbp; test %bl,%bl; je …; movzbl %bl,%ecx; movzbl %al,%eax; xor %edx,%edx; div %cx; pop %rbp; ret; call …panicdivide` |
| body B, the composition | `test %esi,%esi; je …; movzbl %dil,%eax; div %sil; ret; push %rax; call …runtime_panicdivide` |
| the gate's own width note | body A answers 32 bits and body B answers 64, so the gate's own rule cut both to 32 |
| the counterexample | `[IN_1 = 129, IN_0 = 255]` |

**GLOSS.** The node answers in `uint8`. Go's own body divides at 16 bits
(`div %cx`) and leaves the quotient in `%ax` with the bits above it
zero; the mode-rendered c emulation divides at 8 bits (`div %sil`) and
leaves the REMAINDER in `%ah`. Both quotients are 1. The gate compares
32 bits because body A's answer place is 32, and the two differ in bits
8 to 15, which are above the eight the node answers in. The gate has a
re-pose for narrow ARGUMENTS (the caller extension); it has none for a
narrow ANSWER, and that is the second list's item 3.

---

# 9. The two defects this task's own machinery had, and where each was fixed

Both were found by the measure's own output and each was fixed in the
one place that owned it. Both are in `hub2.py`; no shared file was
touched.

| defect | sightings | the fix, and where |
|---|---|---|
| a go emulation may call a HELPER function its own file declares, and task hub1's `strip_go` carried the emulation's own function alone | 10 go pair compositions, all failing to build with `./main.go:5:63: undefined: sel32` | `hub2.py` `go_blocks` / `strip_go`: the composed go file carries every function the emulation's file declares except `main`, deduplicated by its own text, exactly as the composed c file carries its `static inline` helpers |
| go has no conversion from its truth holder into an integer holder, where c and rust both have one | 4 go cell compositions failing with `./main.go:10:59: cannot convert a (variable of type bool) to type int32` | `hub2.py` `check_operand_holders`: a node operand in the truth holder whose entry parameter is not in the truth holder is REFUSED BY CAUSE on such a target |

---

# 10. The guards, the memory, and the lanes

**THE SPELLING GUARD**, over every json this task wrote, lane
`hub2_l13_the_guard.sh`:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/dictionary2.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dictionary2.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/oracle_test2.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS oracle_test2.json -- no operator token in any key, grouping, pairing or row structure
```

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/measure2.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS measure2.json -- no operator token in any key, grouping, pairing or row structure
```

It passed first time, and the reason is worth one sentence because a
PAIR is a pairing and the ban names pairings: a pair's key is two CELLS,
and which two cells make a pair is read off the corpus's own ledger row
whose `produced_by.mnem` is the setter then the consumer as the ledgerer
wrote it from the unit's own body. No source operator token enters any
key, grouping, pairing or row structure of anything this task wrote.

**NO EXEMPTION** anywhere in what this task adds: `grep -c exempt`
returns 0 on `hub2.py` and on every lane script except
`hub2_l13_the_guard.sh`, which reads 2 because that lane's own two lines
of prose say what it checks.

**MEMORY.** Bound 6 GB resident on the one collecting process, named
abort `ABORT_MEMORY_HUB2`, checked after every unit of work. The sample
ran first as the law requires — lane `hub2_l9_measure_sample.sh`, the
first 12 units, 36 rows in 9.5 s, peak **98,516 kB**. The whole
population then ran at peak **122,992 kB**, 2.0% of the bound, and never
aborted. The dictionary lane peaked at **166,236 kB** (the pool is held
whole while its index is built and is dropped after) and the handful
lane at **96,944 kB**. No lane hit a time or memory limit, so nothing is
re-run for room.

**THE LANES**, sixteen, all kept in
`PRIVATE/PseudoCoupHQ/Research/oracle/hub/lanes_hub2/`: `l1` to
`l5` the two levels explored (the bank's own counts, the corpus's
attested pairs, tasks o7/o11/o13's populations, and the pair key at full
cell granularity), `l6` and `l7` the dictionary, `l8` the handful, `l9`
the measure sampled, `l10` the measure whole, `l11` the tables, `l12`
the handful and the measure again after §9's two fixes, `l13` the
guards, `l14` the pastes of this log, `l15` and `l16` the verifier. Nothing under
`<runs>/` or `PUBLIC/Airlock/` was deleted, and no shared
file was changed: `hub.py`, `emulate.py`, `go_render.py`,
`rust_render.py`, `handful.py`, `model_table.py`, `ledger.py`,
`pool100_entry_equivalence.py`, `gate.py`, `reference.py`,
`canonical_form.py`, `term97_walk.py`, `bank.py`, `autopoly.py` and
`go_types_oracle.go` are all IMPORTED or RUN, never edited.

**ONE ARTIFACT IS ON DISK AND NOT IN GIT, and it is the repo-daemon's
standing behaviour on this line, not a choice of this task's.**
`dictionary2.json` is held out of every commit by the daemon's
sensitive-information guard, which reads the sha256 strings the bank's
certificates carry as high-entropy strings:
`PseudoCoupHQ: HOLDING Research/oracle/hub/dictionary2.json -- sensitive
info detected (high_entropy_string@L2304, ...); never staged, never
edited`. Task bank1's own `certificates.json`, its `bank1_delta_runs.jsonl`
and the logs 249 and 253 are in the same state. The file is on this
machine and on the tower, `dictionary2.md` beside it IS in git, and
`hub2.py dictionary` rebuilds it in one second. Nothing was done to work
around the guard.

**THE TALLY.**

```
$ wc -l PseudoCoupHQ/Research/oracle/hub/hub2.py PseudoCoupHQ/Research/oracle/hub/dictionary2.json PseudoCoupHQ/Research/oracle/hub/dictionary2.md PseudoCoupHQ/Research/oracle/hub/oracle_test2.json PseudoCoupHQ/Research/oracle/hub/oracle_test2.md PseudoCoupHQ/Research/oracle/hub/measure2.json
   2678 PseudoCoupHQ/Research/oracle/hub/hub2.py
 153728 PseudoCoupHQ/Research/oracle/hub/dictionary2.json
   1285 PseudoCoupHQ/Research/oracle/hub/dictionary2.md
   1866 PseudoCoupHQ/Research/oracle/hub/oracle_test2.json
    736 PseudoCoupHQ/Research/oracle/hub/oracle_test2.md
  62432 PseudoCoupHQ/Research/oracle/hub/measure2.json
 222725 total
```

---

# 11. The two lists

## Decided, recorded for audit

1. **The dictionary's cell level is read from the bank and joined back
   to the run that produced each certificate**, because a certificate
   names its artifact but carries no parameter list and the brief's
   third hole is about parameters. The join is CHECKED — the run's
   rendered source is hashed and the hash must be the certificate's —
   and all 512 preferred certificates of the three targets joined and
   matched. A certificate whose run cannot be found, or whose source
   does not hash to the certificate's, would be a hole with that as its
   cause and there are none. §2, §3.
2. **A pair's key is TWO CELLS**, setter and consumer, each the
   machine-form key ruled 2026-09-08, and which two cells make a pair is
   read off the corpus's own ledger row whose `produced_by.mnem` is the
   two of them. The setter's WIDTH is part of the key. §4.
3. **The PAIR RULE, the pair analogue of task o2's narrow rule**: a
   corpus unit is ONE PAIR PLUS CHAFF when its ledger holds exactly one
   flag-pair row whose consumer line the model table's classifier reads,
   and every arch-opcode row outside the OUT block is that pair's setter
   and there is exactly one. 104 of the corpus's 590 go units are, and
   they are disjoint from the 134 the narrow rule names.
4. **A node resolves to a corpus unit exactly as task hub1 resolved it**
   — the type tuple as the candidate set, the two sources' own operator
   nodes compared by the same parser — and the LEVEL that serves the
   resolved unit is decided by what the dictionary holds for it, in the
   order cell, pair, body. Nothing about the node's own text chooses a
   level.
5. **The holder table gains one holder, `bool`**, go's truth holder,
   which a comparison's own result sits in and which task hub1 never
   met. c reaches it by a cast; rust and go both refuse a cast into it,
   so the conversion from the emulation's 8-bit answer is written as the
   target's own test against zero, and WHICH conversion is used is
   decided by the node's result holder — machine form.
6. **A node operand in go's truth holder whose entry parameter is not in
   a truth holder is refused by cause on go**, which has no conversion
   from `bool` into an integer holder; c and rust have one and the gate
   answers on what comes out of it. §9.
7. **The three DISPROVED compositions are kept and reported, not
   refused into invisibility.** Two are the truth-holder carriage
   question with the gate's own counterexample; one is a difference
   above the bits the node answers in. §8.
8. **The body level has no go column** and says so as a cause on every
   one of its 137 hole rows: task o7 renders c, task o11 renders rust,
   and this task rendered nothing new.

## Awaiting the owner

1. **The loop renders each flag consumer over ONE setter — the one that
   consumer's own attestation records the most ledger rows for — at that
   setter's own width.** The corpus attests 44 distinct pairs over its
   go units and the dictionary serves 10 of the 104 units that carry
   one; with the setter's width ignored (which is not the machine-form
   key) it would be 58. Whether the loop should render a consumer over
   EVERY attested setter cell, rather than over one setter mnemonic at
   one width, is a question about the LOOP and is the single change that
   would move the pair level most. It is also the whole of why the
   handful's `f8` does not compose. §4, §6.
2. **The primitive route's lookup still carries no holder**, and task
   hub1's finding stands unchanged: `emu_add_gpr_gpr_64__primitive__c`
   and its family are PROVED in the bank and unusable by a composition
   because their parameters are the target's truth holder. This task
   records the holders on every entry and refuses by cause, which is
   what the brief asked; the fix — the lookup carrying the matched
   body's holders — belongs to the loop and is NOT made here.
3. **The gate has a re-pose for a narrow ARGUMENT (the caller
   extension) and none for a narrow ANSWER.** `go/regen_146` is
   disproved on c and on rust only in the bits above the eight its node
   answers in (§8, cause 2). Whether an answer-width re-pose belongs
   beside the caller extension is a question about the GATE.

---

# 12. The conventions verifier

Run FROM this task's own instance, as the law requires:

    python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_254_task_hub2_the_dictionary_at_two_levels.md

| pass | lane | claims | MATCHES | DIFFERS | UNVERIFIABLE | REFUSED | NOT_RERUNNABLE |
|---|---|---|---|---|---|---|---|
| 1 | `hub2_l15_verifier.sh` | 22 | 14 | **0** | 8 | 0 | 0 |
| 2 | `hub2_l16_verifier_b.sh` | 22 | 15 | **0** | 7 | 0 | 0 |

**GLOSS**, and the obligation the law states is the DIFFERS column: **0
on both passes**. The one claim that moved between them was a defect in
the pasted COMMAND and never in the claim: §4's pair paste cited its
program in the prose above the fence instead of on the fence's own first
line, so the verifier read it as an attribution with nothing to re-run;
the command was moved onto the first line of the block and the block was
completed with the line of output it had been cut short of. Nothing else
changed, and the verifier was not touched.

The 7 UNVERIFIABLE are the object definitions of §1, the answer
paragraph, and five glosses: prose findings, each stated as such rather
than claimed reproducible, and each naming the file it reads.

Every block in this log was written by capture: lane
`hub2_l14_the_pastes.sh` ran each command and this log carries its own
output.

The only thing added to this file after pass 2 is this section's second
row, the paragraphs under it, the lane count corrected from fifteen to
sixteen in the header and in §10, and §10's paragraph on the artifact
the repo-daemon holds out of git. None of them carries a command.
