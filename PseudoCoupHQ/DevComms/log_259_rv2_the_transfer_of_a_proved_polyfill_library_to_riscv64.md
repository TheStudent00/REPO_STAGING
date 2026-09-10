# log_259 — task rv2: the transfer, measured — RISC-V's model table, its cells matched to x86's by TERM, inherited certificates re-verified on riscv64, and the loop only over what has no twin

Project node: **arch_unit_oracle**
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
Written 2026-09-10 by the implementer of task rv2, brief
`PRIVATE/PseudoCoupHQ/Research/briefs/task_rv2_brief.md`.

Deliverables: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json`
and `.md`, `.../riscv/twins.json` and `.md`, `.../riscv/transfer.md`,
`.../riscv/certificates_riscv64.jsonl`. Lanes:
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/lanes_rv2/`. Lane logs are
on the TOWER at
`<runs>/rv2/agent/logs/<stamp>__<lane>.log` — that is
a tower path, not a path on this laptop.

---

## 1. What was done and what came of it — the walkthrough, before any figures

The task asked whether a library of proved emulations, built for one machine,
carries to a second one. The library is keyed by MAPPINGS rather than by
opcode names, so in principle it should: a certificate says "this source
computes this term", and a term is a z3 expression over bit vectors, which
knows nothing about which machine it came from. What can differ is the
compiler's back end for the second machine, and the rules about how arguments
arrive and answers leave.

I built RISC-V's own model table first, by sweeping the reference task rv1
wrote over every operand form and width the architecture has, and printing the
term each instruction leaves in each place it writes. Then I matched every
RISC-V cell against every x86 cell by term: identical text first, then the
solver. Then, for each RISC-V cell that had a twin, I took every certificate
the bank holds about that twin, took its source unchanged, compiled it for
riscv64 at the corpus's own flags, carved the body, read it back into a term,
and asked the solver whether it computes the same thing. What was left over —
the cells with no twin — went through the loop itself, on riscv64.

Three things had to be settled before any of it was sound, and each is a
finding rather than a detail. The first is that task ref2 is correcting the x86
reference in the same hours, and the model table on disk and every certificate
in the bank were produced BEFORE those corrections; I read the pre-correction
reference ref2 kept beside its own work, and the re-run of the x86 table
reproduced its recorded text on all 8,403 place rows, which is the check that
the reading was the right one. The second is that a headline about twins needs
its reading stated: RISC-V writes all 64 bits of a register and its 32-bit
forms sign-extend, where x86's 32-bit write zero-extends, so at the whole
written place a `w` form can never twin an x86 32-bit form; both readings are
reported and neither replaces the other. The third is that the two
architectures cannot be joined through a cell's own symbol names, because a
cell's symbols are named after the sweep's operand registers whatever the
language; the join that needs no guess is an ARGUMENT'S POSITION, which is
what task rv1 already used and what this task ended on after two wrong
attempts, both recorded below.

What came out is this. Of the 255 RISC-V cells the reference models, 161 have
an x86 cell that computes the same term at the operation's own width, so the
loop had to be run on only 94 of them. Every certificate that compiled and
walked was PROVED on riscv64 and none was disproved: 103 of them, over 34
distinct RISC-V cells, on c and go. A further 434 certificates on the seven
interpreted targets transfer as they are. The rest of the twinned cells — 127
of them — have a twin and nothing to inherit from it, because the x86 loop has
itself proved only part of its own table; that is the honest limit on how much
of the workload the transfer removed, and it is a limit on the x86 side, not
on the transfer.

---

## 2. What the objects are, one sentence each

- **a CELL** — one (`mnem`, operand shape, `key_width`) row of a model table:
  the reference's mapping of that instruction at that operand form and width,
  as a z3 term per written place.
- **a TWIN** — an (x86 cell, x86 place) whose place term is the same function
  as a RISC-V cell's place term: identical after `term.Term.normalize` (a TEXT
  twin) or proved equal by z3 (a Z3 twin).
- **a CERTIFICATE** — one banked record about one (cell, target, written
  place): the term, the rendered source and its sha256, the compiler and its
  flags, the carved body, and the gate's own verdict.
- **an INHERITED CERTIFICATE** — the same record re-measured on riscv64: the
  same source, a riscv64 compiler, a riscv64 body, and this task's verdict,
  carrying `arch` and `inherited_from`.
- **a SINGLETON** — a corpus probe whose whole riscv64 body is ONE computing
  instruction and the return, so the probe's own source IS the target
  language's primitive for that cell.

---

## 3. What was read, and exactly as it stood

Every figure below is an as-of. Task ref2 is changing `reference.py` and task
t2 last wrote the bank at 13:25 on 2026-09-10; these are the bytes this task
read.

| file | sha256 |
|---|---|
| `Research/oracle/arch_opcodes/model/model_table_rows.json` | `f146dcba5893bac47bf00b2f0a97f7944fd19d86f3db22749b69b6b7599dfcd8` |
| `Research/oracle/arch_opcodes/model/model_table_attest.json` | `152c122c475e927f1fa9845d7fc4df71fd97064f49766bd7b724d74291e05740` |
| `Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl` | `bfd80360c0afdb4e6d2d227d6ea399f9781fcd0671dc121d676c18e02c2d49b8` |
| `Research/op_pipeline/reference.py` AS IT STANDS (ref2's four corrections applied) | `40df3b55455f8d7a6e35ef04b7219701b957af65ad08f4d81fd550d911525e72` |
| `Research/oracle/arch_opcodes/level0/ref2_originals/reference.py` — **the one this task walked with** | `3893363145df57944286222c18756465757d4e69a6eea0783e0f03265b7156e0` |
| `Research/oracle/arch_opcodes/level0/ref2_originals/condition_table.py` — likewise | `be2d0ad6425bdb4c437c04565c3b421ba57551e933e1df40daaef00fe408667f` |
| `Research/oracle/riscv/riscv_reference.py` (task rv1, READ and called) | `cfe5048190a3b821af3c700645011e37447f0675f1b43590e0349d91bd1ee813` |
| `Research/oracle/cross_construction/emulation/handful/handful.py` (the renderer, READ and called) | `42125df2c847eb305a965e7dcea0c3516629b6eb1ede72a9833b94c944d60141` |

The bank's `code_version` as it stood: the newest certificates
(`t2_construct`, 5,303 of them) carry
`{"driver": "42125df2c847eb305a965e7dcea0c3516629b6eb1ede72a9833b94c944d60141",
"driver_source": "handful.py", "loop": "bc7a70379ba9dd35cc472c6461c331e2cc350677c0231f67d236dfc0f84ba2bb", ...}`,
which is `handful.py` and `autopoly.py` exactly as they sit on disk now;
12,593 of the 24,758 certificates carry `code_version: null`, which is every
certificate banked before 2026-09-10.

Nothing under `Research/op_pipeline/` and nothing in the bank file was
written by this task.

---

## 4. The RISC-V model table — section 2.1 of the brief

Lane `rv2_l2_sweep_again_and_sample.sh`, artifacts `model_table_rv.json` and
`model_table_rv.md`.

| what | count |
|---|---|
| sweep attempts | 1,512 |
| rows TRANSLATED | 320 |
| rows REFUSED (the reference refuses the spelling, by name) | 1,034 |
| rows NO_BUILDER | 70 |
| rows NOT_SPELLED | 88 |
| mnemonics in the reference's table | 108 |
| CELLS — distinct (`mnem`, shape, `key_width`) with at least one written place | **255** |

Three things about this table that the x86 one does not have, each a fact of
the architecture:

- **There is no flags place anywhere in it.** The one non-register place a
  RISC-V instruction leaves is the BRANCH CONDITION, which the six branches
  compute inside themselves.
- **The width is in the mnemonic, not in the operand spelling.** x86's sweep
  walks four operand widths per shape because `%dil`, `%di`, `%edi` and `%rdi`
  are four spellings of one register; RISC-V has no sub-register names, so one
  mnemonic has one width and `key_width` is a function of the mnemonic alone,
  read off the reference's own tables.
- **The symbolic immediate cannot be spelled.** x86's sweep gained four
  `imm_symbolic_*` shapes (task ap5) by putting a register in the immediate's
  slot, because `reference.Operands.read_text` reads a register and an
  immediate the same way. `riscv_reference.Operands.immediate` refuses a
  non-literal by name, so the 88 NOT_SPELLED rows are exactly the mnemonics
  whose builders read no immediate at all, and the ones that do read one are
  REFUSED by the reference itself.

### 4.1 The attestation on riscv64

Lane `rv2_l10_attest_again.sh`, artifact `attest_rv.json`. The corpus's own
probe sources compiled for riscv64 at the corpus's ship flags, carved at the
function symbol, walked by the RISC-V reference.

| what | count |
|---|---|
| c probes in `probe_manifest_c.json` | 750 |
| c probes attempted (the brief's sample of 500) | 500 |
| go probes in `probe_manifest_go.json` | 744 |
| go probes attempted (all of them) | 744 |
| LIFTED (compiled, carved and walked) | 474 |
| WALK_REFUSED (compiled and carved; the reference has no entry for a line) | 33 |
| BUILDFAIL | 737 |
| riscv64 cells the carved bodies attest | 57 |
| riscv64 SINGLETONS (whole body is one computing instruction) | 31 |

**The 737 BUILDFAILs are not a failure of the riscv64 route, and the
cross-tab says so.** The corpus is generated by COMPILE-OR-REFUSE: a probe the
x86 build refused was recorded as refused and never became a unit. The
question the count actually raises is whether the riscv64 build refuses the
SAME probes, and it does, exactly:

| language, x86 ship body in the store, riscv64 built | probes |
|---|---|
| c, no, no | 100 |
| c, yes, yes | 400 |
| go, no, no | 637 |
| go, yes, yes | 107 |

Zero probes built on one architecture and not the other.

---

## 5. The match, by term — section 2.2 of the brief

Lane `rv2_l9_match_all_twins.sh`, artifacts `twins.json` and `twins.md`.

**The x86 side was re-derived and checked before anything was matched.** The
x86 table holds each place's term as TEXT and this line has no reader that
turns text back into a z3 object, so each of the 5,912 distinct x86 cells had
its own line re-run through `model_translate.run_line` — the same function
that wrote the table. The re-run reproduced the table's own recorded text on
**8,403 place rows, differed on 0 and refused 0**. Those 8,403 rows carry only
**679 distinct place terms**, which is why the match is cheap.

**THE HEADLINE CARRIES ITS READING, and there are two.**

| twin | READING 1: the whole written place | READING 2: at the cell's own `key_width` |
|---|---|---|
| TEXT | 101 | 158 |
| Z3 | 1 | 3 |
| NONE | 153 | 94 |
| **cells with a twin, of 255** | **102 (40.0%)** | **161 (63.1%)** |

Reading 1 is the whole 64-bit register. Reading 2 cuts both sides to the width
the operation computes at. The gap between them is one architecture fact:
**RISC-V's 32-bit forms sign-extend their result into the whole register and
x86's zero-extend theirs**, so at the whole place a `w` form can never twin an
x86 32-bit form. Reading 2 is the one the gate uses, because an emulation is
compared on the node's own width (task ap6's re-pose).

**The none list, by mnemonic** (untwinned under BOTH readings, 94 cells over
these mnemonics) — the brief expected `slt`/`sltu`, `mulh*`, the divides,
`auipc`/`lui`, and it was right about all of them:

| `mnem` | untwinned shapes |
|---|---|
| `auipc` `lui` | 1 each — the term is a constant or reads the program counter |
| `slt` `slti` `sltiu` `sltu` | 1 each — a comparison writes a general register a 0 or a 1, where x86 writes 8 bits into a register and keeps the other 56 |
| `mulh` `mulhu` `mulhsu` | 1, 1, 2 — the high half of a widening multiply, at a shape x86 does not spell |
| `div` `divu` `divw` `divuw` `rem` `remu` `remw` `remuw` | 2 each — RISC-V defines the zero divisor and the MIN/−1 overflow; x86's `idiv` raises, so its term says nothing about those regions |
| `czero.eqz` `czero.nez` | 1, 2 — the condition is a register's own value; x86's `cmov` reads the FLAGS, so the two terms do not even have the same arity |
| `beq` `bne` `blt` `bge` `bltu` `bgeu` | 4 each — the branch condition is a place x86 has no counterpart for |
| `jal` `jalr` `lh` `sb` `sh` `sw` `flw` `fsw` | 8 each — transfers, and the narrow loads and stores |
| the floating-point family (`fadd.*`, `fcvt.*`, `feq.*`, `fle.*`, `flt.*`, `fmul.*`, `fdiv.*`, `fsub.*`, `fmv.w.x`) | 1–2 each |

Full table: `Research/oracle/riscv/twins.md`, Table 4.

---

## 6. The inheritance — section 2.3 of the brief

Lane `rv2_l14_inherit_body_against_body.sh`, artifacts
`certificates_riscv64.jsonl` (734 records) and `certificates_riscv64.json`.

| target | certificates | outcome |
|---|---|---|
| `c` | 32 | **proved** |
| `c` | 15 | refused — BUILD_REFUSED |
| `c` | 11 | refused — WALK_REFUSED |
| `go` | 71 | **proved** |
| `rust` | 61 | refused — BUILD_REFUSED |
| `cpython` `php` `ruby` `java` `javascript` `dart` `csharp` | 62 each, 434 in all | **agreed**, transfers as it is |
| `cpp` | 54 | refused — NOT_ATTEMPTED (the brief names c, go and rust) |
| `swift` | 56 | refused — NOT_ATTEMPTED (no riscv64 swift in the image) |

| what | count |
|---|---|
| certificates attempted | 734 |
| **PROVED on riscv64**, at the cell's own `key_width` | **103** |
| **DISPROVED on riscv64** | **0** |
| transferred as they are (interpreted) | 434 |
| refused, with a cause | 197 |
| of the PROVED, also proved at the WHOLE written place | 83 |
| of the PROVED, differing above the operation's own width | 20 |
| distinct RISC-V cells with an inherited PROVED certificate | 34 |

**There are no disproved inheritances.** Every certificate whose source built
for riscv64 and whose body the reference could walk was proved. The 20 rows
that hold at the operation's width but not at the whole register are the
extension rule again — a c function returning a 32-bit value leaves it
sign-extended in `a0` under the riscv64 psABI, and the x86 cell's term says
the upper 32 bits are zero — and they are recorded per row as
`verdict_at_the_whole_place`, not hidden.

### 6.1 How the two architectures are put in one place, and two wrong attempts before it

This is the part that took three lanes, and each wrong attempt is recorded
because the numbers moved a lot between them.

- **Lane 11 bound arrival register `a<k>` to the k-th PRINTED SYMBOL of the
  cell's term.** 87 proved, 13 disproved. The 13 included `sub` on both c and
  go: the source is `return a - b`, the riscv64 body is `c.sub a0, a1`, and
  the two terms printed the SAME text — a swap, not a difference.
- **Lane 12 bound every source by ARGUMENT POSITION** (`seed_rsi` is the
  second argument of a c function, and the second argument is in `a1`). 27
  proved, 65 disproved — worse, because a RENDERED source declares one
  parameter per family in the term's own printed order, which is not the
  argument sequence.
- **Lane 13 read the certificate's own `route`** and used the printed order
  for a rendered source and the argument sequence for a corpus probe. 85
  proved, 18 disproved. The 18 still printed identical texts, because a
  cell's symbols are named after the SWEEP'S operand registers (`%rdi`,
  `%rsi`) whatever the language, and which argument feeds which instruction
  operand is the compiler's choice.
- **Lane 14 stopped aligning to the cell at all.** It walks the certificate's
  OWN x86-64 body beside the riscv64 one, both as functions of the same
  arguments — argument k in `rdi/rsi/...` (`rax/rbx/...` for go) and in
  `a0..`, a float argument in `xmm0..` and `fa0..`. That is task rv1's own
  method, it needs no guess, and the chain is sound: the bank proved the
  x86-64 body computes the cell's term, and this lane proves the riscv64 body
  computes the same function of the same arguments. **103 proved, 0
  disproved.**

### 6.2 One interpreter's handful, re-run

Lane `rv2_l18_interp_final.sh`, artifact `interp_recheck.json`. An `agreed`
certificate says "this source, run by this interpreter, answers what the term
says at every point of a sample". The interpreter is a program; the language's
arithmetic is defined by the language, not by the machine underneath it, so
the claim does not mention the host architecture. What was checked is the
weaker, checkable half — the same source, run again:

| `mnem` | shape | `key_width` | place | outcome | agreements / points |
|---|---|---|---|---|---|
| `add` | gpr_gpr | 32 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `imul` | gpr_gpr | 32 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `sar` | cl_gpr | 32 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `shr` | cl_gpr | 64 | reg_rdi | AGREES_AT_EVERY_POINT | 200 / 200 |
| `addss` | xmm_xmm | 32 | reg_xmm0 | THE_CERTIFICATE_IS_ABOUT_A_RE_POSED_TERM | 0 / 0 |
| `cvtsi2sd` | gpr_xmm | 64 | reg_xmm0 | THE_CERTIFICATE_IS_ABOUT_A_RE_POSED_TERM | 0 / 0 |

800 points, 800 agreements, 0 disagreements. It is a CHECK AT POINTS, not a
proof, exactly as the original agreement was. The two vector rows are named
rather than counted: the pipeline's gate re-poses a vector place onto the LANE
the operation writes and renders the emulation from THAT, so the source takes
fewer arguments than the whole place reads; re-posing a vector place is the
driver's job and this task's small re-runner does not restate it.

---

## 7. The loop on the delta — section 2.4 of the brief

Lane `rv2_l15_loop_and_interp.sh`, artifacts `rv_loop.jsonl` (188 rows) and
`rv_loop.json`. `find_emulation` over the 94 cells with no twin under either
reading, on c and go, both routes.

| what | count |
|---|---|
| cells with no twin | 94 |
| runs (cells x written places x targets) | 188 |
| runs **proved** | 135 |
| runs refused | 42 |
| runs sat | 11 |
| distinct cells PROVED by the loop | **82** |
| riscv64 SINGLETONS available to the primitive route | 31 |

All 135 proved runs came through the TERM route. The primitive route — the
x86 loop's "which corpus body IS this cell's own opcode", answered on riscv64
by `rv_attest.py` — fires only where the term route did not prove, and it
proved nothing the term route had not.

**The 11 sat rows have one dominant cause, and it is a limit task rv1 stated
rather than a difference between the machines: 9 of the 11 have a BRANCH in
their carved body.** `riscv_reference.simulate` walks a body in TEXT ORDER and
records a branch as a guard row; no branch-merging walk is coded, because the
ten bodies of task rv1's handful had none. Go's riscv64 lowering is branchy —
its stack-growth check sits at the head of every function — so a go emulation
of a divide or a conditional zero reads as a constant to a text-order walk.
The two rows without a branch are `divuw` and `divw` at `gpr_gpr_same` 32,
where the cell divides a value by itself and the compiler folds the whole
thing.

---

## 8. The count — section 2.5 of the brief

Artifact `Research/oracle/riscv/transfer.md`, Table 10, written by
`transfer.py` from this folder's own json.

| what | cells | share of the 255 |
|---|---|---|
| RISC-V cells with at least one written place | 255 | 100% |
| with an x86 twin, READING 1 (the whole written place) | 102 | 40.0% |
| with an x86 twin, READING 2 (at the cell's own `key_width`) | 161 | 63.1% |
| reached by an INHERITED certificate (proved or agreed) | 34 | 13.3% |
| twinned, but the x86 bank holds NO proved or agreed certificate for the twin | 127 | 49.8% |
| the loop still had to run (the untwinned) | 94 | 36.9% |
| PROVED by the loop | 82 | 32.2% |
| **with at least one proved riscv64 emulation, from either route** | **116** | **45.5%** |
| **with none yet** | **139** | **54.5%** |

**The shrinkage, in three sentences, each with its reading.** Of the 255
RISC-V cells, 161 (63.1%) have an x86 cell that computes the same term at the
cell's own width, so the LOOP had to be run on only 94 (36.9%) of them — and
that is the number the hypothesis asked for. What ACTUALLY arrived by
inheritance is smaller, and its reason is not the transfer: only 34 cells
(13.3%) had an x86 twin the BANK holds a proved or agreed certificate for,
because the x86 loop has itself proved only part of its own table, so 127
twinned cells have a twin and nothing yet to inherit from it. Between the two
routes 116 cells (45.5%) now carry at least one proved riscv64 emulation and
139 do not.

**THE THREE READINGS of the RISC-V polyfill-complete set, and on RISC-V they
COINCIDE.** The reason is one fact: **the architecture has no flags
register**, so a RISC-V cell writes exactly one place. Strict (every written
place proved), destination-only (the destination alone) and corpus-needed (the
destination plus the flags wherever the corpus shows a consumer reading them)
are three ways of saying the same thing when there is one place and no flags.

| reading | what it counts | RISC-V | x86 |
|---|---|---|---|
| strict | every written place proved | **74** | 2,007 |
| destination-only | the destination place proved | **74** | 2,265 |
| corpus-needed | the destination proved, and the flags wherever a consumer reads them | **74** | 2,221 |

The RISC-V column counts CELLS with every written place proved or agreed on
BOTH compiled targets; the x86 column is the bank's own count of proved (cell,
target) PAIRS as `certificates.json` records it. The two are not the same
population and are printed side by side rather than divided.

---

## 9. The flags

Each is a flag with its literal output, not a workaround and not a redesign.
Status is on every item.

1. **The x86 reference is being corrected by task ref2 while this task ran, so
   this task read the PRE-CORRECTION one — RESOLVED, and stated as an
   as-of.** `Research/op_pipeline/reference.py` on disk is byte-identical to
   ref2's `ref2_originals/reference_c4.py` (all four corrections applied,
   sha256 `40df3b55…`), while `model_table_rows.json` and every certificate in
   the bank were produced under `ref2_originals/reference.py` (sha256
   `3893363145…`). Measured, lane `rv2_l2_sweep_again_and_sample.sh`: against
   the CORRECTED reference the re-run of 20 x86 cells reproduced the table's
   recorded text on 32 of 40 place rows; lane `rv2_l3_sample_pre_correction.sh`
   against the PRE-correction one, **40 of 40**, and over the whole table
   **8,403 of 8,403, 0 differing**. Every 8- and 16-bit destination row was
   what moved, which is ref2's correction 1. **When ref2's corrected model
   table lands, `twins.json` has to be re-run against it.**
2. **`rust`'s riscv64 target is installed and every rendered source still
   refuses — OPEN.** LITERAL, lane `rv2_l1_sweep.sh`:
   `error[E0463]: can't find crate for 'std'` /
   `= note: the 'riscv64gc-unknown-none-elf' target may not support the standard library` /
   `= note: 'std' is required by '<unknown>' because it does not declare '#![no_std]'`.
   All 61 rust certificates refuse this way. The brief says the source is
   taken UNCHANGED, so adding `#![no_std]` was not done. What would fix it is
   a riscv64 target WITH a standard library (`riscv64gc-unknown-linux-gnu`),
   which is an install and therefore the coordinator's.
3. **Fifteen c certificates refuse on `string.h` — OPEN, and it is task rv1's
   flag 1 reaching a second header.** LITERAL, lane
   `rv2_l14_inherit_body_against_body.sh`:
   `/work/rv2inherit/run000021/unit.c:4:10: fatal error: 'string.h' file not found`.
   `-nostdlibinc` sends the include to clang's own per-target resource
   headers, which carry `stdint.h` but not `string.h`; the sources that need
   it are the ones whose renderer uses `memcpy` to move bits between a float
   and an integer holder. Nothing was worked around: the image has no riscv64
   c library.
4. **Eleven c certificates and 16 loop runs refuse because the RISC-V
   reference has no entry for a bit-manipulation instruction clang 21 emits —
   OPEN.** LITERAL, same lane:
   `NotModeled: no entry in the riscv opcode table for 'c.zext.w' (line 'c.zext.w a0')`.
   By instruction, over both: `c.zext.w` 6, `add.uw` 7, `c.mul` 6, `bseti` 4,
   `fsgnjn.d` 1. These are the Zba, Zbb and Zbs extensions. `riscv_reference.py`
   is task rv1's and is READ here, never written; adding entries to it is a
   change to a closed task's deliverable and is the coordinator's call.
5. **Nine of the loop's 11 sat rows have a BRANCH in their carved body —
   OPEN, and it is task rv1's own stated limit.** `riscv_reference.simulate`
   walks a body in text order and codes no branch-merging walk. Go's riscv64
   lowering puts a stack-growth check at the head of every function, so a
   go emulation of a divide reads as a constant to a text-order walk. This is
   not a difference between the two machines.
6. **The riscv64 certificates are NOT in the bank file — DECIDED, and the
   brief's own wording is the thing departed from.** Brief §3 says
   "certificates appended to the bank with `arch`"; the coordinator's
   instruction for this task says "do not touch anything under
   `Research/op_pipeline/` or the bank file", because task ref2 runs beside
   this one. The 734 records are in
   `Research/oracle/riscv/certificates_riscv64.jsonl` in the bank's own record
   shape, each carrying `arch: "riscv64"` and `inherited_from`. They are a
   concatenation away from being in the bank and nothing was lost.
7. **`cpp` was not attempted — OPEN.** The brief names c and go (and rust);
   cpp is neither named nor excluded, and `clang++` can aim at riscv64 by the
   same route as `clang`. 54 certificates sit unattempted for that reason
   alone.
8. **"the 590 go units" of the brief is not a population any store on disk
   spells — REPORTED.** `probe_manifest_go.json` holds 744 probes and
   `op_units_go.json` records an x86 ship body for 107 of them; the 590 of the
   research CORE's §3 table counts something else. This task attempted all 744
   and reports both numbers.
9. **A planning sub-node for the RISC-V line is still WANTED**, as task rv1's
   flag 7 said. `Research/oracle/riscv/` now holds a second architecture's
   reference, its level-0 oracle, its carve, its model table, its twin join,
   its inherited certificates and its own loop, and it has no node.

---

## 10. The guard, memory, and where nothing was written

- **The spelling guard passes on every json and jsonl this task wrote.**
  LITERAL, lane `rv2_l20_transfer_with_the_gap.sh`:
  `operator inventory: 91 tokens read from probe_manifest_*.json`, then
  `PASS model_table_rv.json`, `PASS twins.json`, `PASS attest_rv.json`,
  `PASS attest_rv_sample.json`, `PASS inherit_plan.json`,
  `PASS certificates_riscv64.json`, `PASS rv_loop.json`,
  `PASS interp_recheck.json`, `PASS certificates_riscv64.jsonl.as_one.json`,
  `PASS rv_loop.jsonl.as_one.json`, `guard rc=0`. The guard was not modified.
- **The count of the word the guard hunts for, over every deliverable file:**
  LITERAL, same lane: `deliverable files scanned: 36` /
  `deliverable files containing the word: 0`.
- **Memory.** Bound 6 GB, named abort `ABORT_MEMORY_RV2`, never raised. Peak
  resident per stage: the sweep 59.4 MB; the match 517 MB (the x86 rows
  document is 50 MB of json and is reduced to one record per distinct cell as
  it is read); the attestation sweep 57 MB; the inheritance 252 MB; the loop
  158 MB. The sample the law asks for was run first, lane
  `rv2_l3_sample_pre_correction.sh` (20 x86 cells, 245 MB) and lane
  `rv2_l5_attest_sample.sh` (20 probes per language, 53 MB).
- **Nothing was written outside `Research/oracle/riscv/`**, this log, and the
  two PROGRESS files the brief names. `reference.py`, `term.py`,
  `model_translate.py`, `model_table.py`, `handful.py`, `riscv_reference.py`,
  `riscv_carve.py`, `claim_check.py` and the bank were READ.
- **Nothing under `PUBLIC/Airlock/` or `<runs>/` was deleted**,
  on either machine.

---

## 11. How to re-run any of it

`$R` is `bash PUBLIC/Airlock/remote_lane.sh` with
`AIRLOCK_REMOTE=<user>@<tower>` and
`AIRLOCK_REMOTE_ROOT=Programming/Airlock`.

| what | command |
|---|---|
| the instance | `bash PUBLIC/Airlock/remote_lane.sh conf PUBLIC/Airlock/instances/rv2.conf` then `bash PUBLIC/Airlock/remote_lane.sh up --instance rv2` |
| mirror the folder | `bash PUBLIC/Airlock/remote_lane.sh sync-to Programming/PseudoCoupHQ/Research/oracle/riscv` |
| any lane | `bash PUBLIC/Airlock/remote_lane.sh submit --instance rv2 --batch rv2 --weight 1 PRIVATE/PseudoCoupHQ/Research/oracle/riscv/lanes_rv2/<lane>.sh` |
| wait for it | `bash PUBLIC/Airlock/remote_lane.sh wait --instance rv2 <lane>.sh` — repeated, each call at most 100 s |
| bring it back | `bash PUBLIC/Airlock/remote_lane.sh sync-back Programming/PseudoCoupHQ/Research/oracle/riscv` |

Inside a lane, where this repository is mounted at `PseudoCoupHQ`,
the six commands that produce the deliverable are, in order:

- `python3 PseudoCoupHQ/Research/oracle/riscv/model_table_rv.py sweep PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/riscv/model_table_rv`
- `python3 PseudoCoupHQ/Research/oracle/riscv/rv_attest.py run PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/riscv/attest_rv /work/rv2attest2 500 all`
- `python3 PseudoCoupHQ/Research/oracle/riscv/twins.py match PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_attest.json PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json PseudoCoupHQ/Research/oracle/riscv/twins 3000`
- `python3 PseudoCoupHQ/Research/oracle/riscv/inherit.py run PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json PseudoCoupHQ/Research/oracle/riscv/twins.json PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64 /work/rv2inherit`
- `python3 PseudoCoupHQ/Research/oracle/riscv/rv_loop.py run PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals PseudoCoupHQ/Research/op_pipeline PseudoCoupHQ/Research/oracle/cross_construction/emulation PseudoCoupHQ/Research/oracle/riscv/twins.json PseudoCoupHQ/Research/oracle/riscv/attest_rv.json PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json PseudoCoupHQ/Research/oracle/riscv/rv_loop PseudoCoupHQ/Research/oracle/riscv/src_rv2 /work/rv2loop`
- `python3 PseudoCoupHQ/Research/oracle/riscv/transfer.py PseudoCoupHQ/Research/oracle/riscv PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/certificates.json PseudoCoupHQ/Research/oracle/riscv/transfer.md`

---

## 12. The claims, each with the command that reproduces it

Every block below is a transcript, pasted whole and not tidied. Each command
runs INSIDE the `rv2` instance.

The RISC-V model table's counts — §4:

```
$ python3 -c "import json, collections; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json')); rows=d['rows']; cells=set((r['mnem'], r['shape'], r['key_width']) for r in rows if r['outcome']=='TRANSLATED' and r.get('mapping')); print('attempts', len(rows), 'census', sorted(collections.Counter(r['outcome'] for r in rows).items()), 'cells', len(cells))"
attempts 1512 census [('NOT_SPELLED', 88), ('NO_BUILDER', 70), ('REFUSED', 1034), ('TRANSLATED', 320)] cells 255
```

The twin, in both readings — §5:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/twins.json')); print('reading1', d['census'], 'reading2', d['census_at_key_width'], 'cells', d['meta']['riscv_cells'], 'rerun agrees', d['meta']['x86_rerun_agrees'], 'differs', d['meta']['x86_rerun_differs'], 'distinct x86 place terms', d['meta']['x86_distinct_place_terms'])"
reading1 {'NONE': 153, 'TEXT': 101, 'Z3': 1} reading2 {'NONE': 94, 'TEXT': 158, 'Z3': 3} cells 255 rerun agrees 8403 differs 0 distinct x86 place terms 679
```

The inheritance's tally — §6:

```
$ python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64.jsonl')]; print(sorted(collections.Counter(r['kind'] for r in rows).items())); print('cells proved', len(set((r['cell']['mnem'],r['cell']['shape'],r['cell']['key_width']) for r in rows if r['kind']=='proved')))"
[('agreed', 434), ('proved', 103), ('refused', 197)]
cells proved 34
```

The two builds' agreement on the corpus — §4.1:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/attest_rv.json')); print(json.dumps(d['meta']['the_two_builds_agree'], sort_keys=True)); print('singletons', len(d['singletons']), 'cells', len(d['cells']))"
{"c|x86_body=False|riscv64_built=False": 100, "c|x86_body=True|riscv64_built=True": 400, "go|x86_body=False|riscv64_built=False": 637, "go|x86_body=True|riscv64_built=True": 107}
singletons 31 cells 57
```

The loop on the delta — §7:

```
$ python3 -c "import json, collections; rows=[json.loads(l) for l in open('PseudoCoupHQ/Research/oracle/riscv/rv_loop.jsonl')]; print('runs', len(rows), sorted(collections.Counter(r['kind'] for r in rows).items())); print('cells proved', len(set((r['cell']['mnem'],r['cell']['shape'],r['cell']['key_width']) for r in rows if r['kind']=='proved')))"
runs 188 [('proved', 135), ('refused', 42), ('sat', 11)]
cells proved 82
```

The interpreter's handful, re-run — §6.2:

```
$ python3 -c "import json; d=json.load(open('PseudoCoupHQ/Research/oracle/riscv/interp_recheck.json')); m=d['meta']; print('certificates', m['certificates'], 'points', m['points'], 'agreements', m['agreements'], 'disagreements', m['disagreements'])"
certificates 6 points 800 agreements 800 disagreements 0
```

The spelling guard over every json and jsonl this task wrote — §10:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json PseudoCoupHQ/Research/oracle/riscv/twins.json PseudoCoupHQ/Research/oracle/riscv/attest_rv.json PseudoCoupHQ/Research/oracle/riscv/attest_rv_sample.json PseudoCoupHQ/Research/oracle/riscv/inherit_plan.json PseudoCoupHQ/Research/oracle/riscv/certificates_riscv64.json PseudoCoupHQ/Research/oracle/riscv/rv_loop.json PseudoCoupHQ/Research/oracle/riscv/interp_recheck.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS model_table_rv.json -- no operator token in any key, grouping, pairing or row structure
PASS twins.json -- no operator token in any key, grouping, pairing or row structure
PASS attest_rv.json -- no operator token in any key, grouping, pairing or row structure
PASS attest_rv_sample.json -- no operator token in any key, grouping, pairing or row structure
PASS inherit_plan.json -- no operator token in any key, grouping, pairing or row structure
PASS certificates_riscv64.json -- no operator token in any key, grouping, pairing or row structure
PASS rv_loop.json -- no operator token in any key, grouping, pairing or row structure
PASS interp_recheck.json -- no operator token in any key, grouping, pairing or row structure
```

---

## 13. Decided, recorded for audit

- **The x86 reference this task walked with is the PRE-CORRECTION one**
  (`ref2_originals/reference.py`, sha256 `3893363145…`), because the model
  table on disk and every certificate in the bank were produced under it and a
  match against a half-corrected reference would compare two different ground
  truths. The choice is printed by every run and recorded in every json.
- **The headline twin count carries its reading**, and both readings are on
  every table: the whole written place, and the cell's own `key_width`.
- **The gate compares on the cell's own `key_width`**, which is the pipeline's
  own rule for a narrow answer; the whole-place verdict sits beside it on
  every row.
- **The two architectures are joined by an ARGUMENT'S POSITION**, never by a
  cell's symbol names, and the certificate's own x86-64 body is walked beside
  the riscv64 one so that no alignment has to be guessed.
- **The candidate scope for the z3 pass is a term's WIDTH and ARITY**, and a
  pair that disagrees at any of 12 concrete sample points is excluded without
  a solver call — the filter decides no twin, it only removes pairs the solver
  would have answered `sat` for.
- **The symbolic-immediate shape is attempted only where the builder's own
  source reads an immediate** (`ops.immediate(` in its text), because a
  register in the immediate's slot of an instruction that reads no immediate
  is not a second spelling of anything.
- **`rv_loop.py` renames a RISC-V term's symbols to the renderer's parameter
  slots before rendering**, which changes no value and no structure: the
  renderer reads a symbol's name to decide which parameter slot it takes, and
  the source it emits mentions no register at all.
- **The 734 riscv64 certificates are in `certificates_riscv64.jsonl` in this
  folder**, not in the bank, for the reason in §9 flag 6.
- **The instance configuration `rv2.conf`** is at
  `PUBLIC/Airlock/instances/rv2.conf`.

## 14. Awaiting the owner

- **Whether the Hub's dictionary key must carry the arrival contract's
  extension rule.** This is the question task rv1's log left open and this task
  put numbers against: 20 of the 103 inherited proofs hold at the operation's
  own width and not at the whole register, and 59 of the 255 RISC-V cells fail
  to twin at the whole place while twinning at their own width. Both are the
  same fact — a 32-bit result is sign-extended into a riscv64 register and
  zero-extended into an x86 one — and whether the Hub keys on it or picks it
  by policy is a ruling, not a measurement.
- **A planning sub-node for the RISC-V line**, still wanted, still the owner's to
  create.

**The RISC-V reference gained no entries for the Zba, Zbb and Zbs
instructions clang 21 emits (`c.zext.w`, `add.uw`, `c.mul`, `bseti`), which
refuse 27 rows across the inheritance and the loop; `riscv_reference.py` is
task rv1's closed deliverable and this task READ it, so extending it — and
therefore re-running §6 and §7 — waits for the owner's word.**
