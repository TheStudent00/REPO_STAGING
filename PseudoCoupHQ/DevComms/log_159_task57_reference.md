# log 159 — TASK 57: `reference.py`, the one symbolic simulator

Date: 2026-09-03. Home: `PseudoCoupHQ/Research/op_pipeline`.
Node: `hq.research.compiler_graph.reference`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_4_reference/`)
and its two sub-nodes `opcode_table`, `machine_state`.
Brief: log 158, TASK 57.

---

## 0. The walk, in plain words, before any figure

**The four names, each introduced before it is used.**

- **THE REFERENCE** is one object that walks a unit's own compiled
  body, instruction by instruction, over a machine whose registers
  hold z3 terms rather than numbers, and hands back the term the body
  leaves in its answer register. It is what "proved against ship"
  means.
- **THE MACHINE STATE** is that machine: registers, the condition
  flags, memory, the machine stack, the x87 register stack.
- **THE OPCODE TABLE** is the one table from an arch opcode's name to
  its meaning — which places it reads, which places it writes, and the
  builder that turns its operands into a z3 term.
- **A CENSUS ROW** is an opcode that has an entry in that table and no
  builder. A body that reaches one is refused by name; nothing is
  stepped over silently.

**What this lap changed.** The pipeline carried FOUR references —
`canon9_behaviour_check.Sim9`, `canon10_behaviour_check.Sim10`,
`canon12_behaviour_check.Sim10`, and the one `gate48.py` reaches
through `canon10` — and log 153's 415-unit withdrawal was two of them
disagreeing about the division remainder. There is now one:
`reference.py`, class `Reference`. The three `canon*` files are
superseded records and carry one header comment line each saying so.

**The headline, with its population.** Over **all 31,078 canon38 unit
records**, the one reference walks **25,827** bodies to an answer
term where the superseded route walked **20,892**, with **zero
regressions** — not one unit the old route answered is refused here —
and 4,935 gained. 642 unit records carry no body at all (canon38's own
refusals) and are counted in their own column rather than read as
either side answering.

---

## 1. The verdict, with its population

### 1.1 The population line

Every canon38 unit record: **11 interpreter, 1,779 original, 29,288
regenerated — 31,078 in all**. Nothing is sampled; both routes walked
every one.

### 1.2 The one-line state

**25,827 of 31,078 unit bodies walk to an answer term under the one
reference; 4,609 are refused by name; 642 carry no body. The
superseded route reached 20,892 on the same population. Zero units
regressed.**

### 1.3 Reach, side by side

LITERAL — `coverage57_printed.txt`, the table it prints:

```
REACH, per population (every unit walked, none sampled)
  population        units ref:answer    ref:no old:answer    old:no  no body
  interpreter          11          9         0          9         0        2
  original           1779       1660       103       1572       191       16
  regenerated       29288      24158      4506      19311      9353      624
  ALL               31078      25827      4609      20892      9544      642

REGRESSIONS -- units the superseded route answered and this reference refuses: 0

GAINED -- units this reference answers and the superseded route refused: 4935
```

GLOSS. `ref:` is `reference.Reference`; `old:` is
`canon10_behaviour_check.Sim10` driven exactly as
`gate48.reference_answer` drives it, reproduced inside `coverage57.py`
so no reused file is edited. **This is not a verdict count.** Reaching
an answer term is not the same as proving one; the proving is task
58's gate. What this measures is how much of the corpus the reference
can speak about at all, which is the thing the two missing state
blocks were costing.

### 1.4 Where the remaining 4,609 refusals go, each with its own count

LITERAL — `coverage57_printed.txt`:

```
    3743  arch opcode 'call' has an entry in the opcode table and no builder
     325  arch opcode 'js' has an entry in the opcode table and no builder
     141  arch opcode 'jl' has an entry in the opcode table and no builder
      88  arch opcode 'je' has an entry in the opcode table and no builder
      88  an address computation over base register '%rip'
      53  arch opcode 'jae' ...
      48  arch opcode 'jb' ...
      34  arch opcode 'jo' ...
      24  arch opcode 'jbe' ...
      18  arch opcode 'jge' ...
      15  arch opcode 'jg' ...
      10  a division at width 8 is not modeled
      10  a division at width 16 is not modeled
       6  arch opcode 'ja' ...
       4  a widening multiply at width 8 is not modeled
       1  arch opcode 'jne' ...
       1  a widening multiply at width 16 is not modeled
```

GLOSS, with the causes named. **3,743 are `call`** — a transfer into a
routine whose body is not in the unit YET. the owner's round-12 ruling
(log_158, TASK 59(b)) is that the callee's body is extracted from the
toolchain's libgcc / compiler-rt archive and attached as an ArchUnit
the caller references, with the producer
`{"kind": "runtime_callee", "callee": "__divti3"}`; task 59 (node
0_3_5_1_8 `runtime_callee`) delivers that. Until it lands the table
carries `call` as an entry with no builder and the refusal says
"runtime callee not yet attached (Task 59, node 0_3_5_1_8)". See §10. **753 are conditional transfers** — this
reference walks a body in TEXT ORDER, which is exactly what the route
the gate calls does today, and refuses a branch rather than guessing
which side runs. **88 are an address computation off `%rip`**: `lea`
of a rip-relative address asks for the ADDRESS of a compiler constant,
and this reference models the value a read through that address
returns, not the address itself. **25 are the 8- and 16-bit division
and widening-multiply forms**, whose destination pair is the
accumulator's own two halves rather than two register families.

---

## 2. The three acceptance instances, printed with values

All three are `acceptance57_printed.txt`, produced by
`acceptance57.py`.

### 2.1 (a) `c/op_246` — the division remainder

LITERAL:

```
LITERAL -- the unit's own ship body, and its answer home:
  body:        mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret
  answer home: rax at 32 bits

LITERAL -- the answer term this reference builds:
  Extract(31,
          0,
          bvsrem_i(Concat(Extract(31, 0, seed_rdi) >> 31,
                          Extract(31, 0, seed_rdi)),
                   Concat(Extract(31, 31, seed_rsi), ... )))

LITERAL -- does the answer term use SRem?  yes

LITERAL -- the two remainders at 32 bits, inputs 7 and -3:
  z3.SRem(7, -3)  = 1            (as a signed value: 1)
  7 % -3 in z3py  = 4294967294   (as a signed value: -2)

LITERAL -- the reference run on this unit's own body with
its two arrival registers bound to 7 and -3:
  answer = 1   (as a signed value: 1)
```

GLOSS. `bvsrem_i` is z3's own printed name for the signed-remainder
declaration, so the term is `SRem` and not `%`. x86's `idiv` leaves a
remainder whose sign follows the DIVIDEND: 7 divided by −3 leaves 1.
z3py's `%` on a bit vector is `bvsmod`, whose sign follows the
DIVISOR, and gives −2. The superseded route computed the second and
compared it against a ledger term computing the first, which is the
whole of log 153 §5's 415-unit withdrawal. The fix is visible in the
two lines printed side by side.

### 2.2 (b) `c/regen_11491` — the machine stack round trips

LITERAL:

```
LITERAL -- the unit's own ship body:
  push %rax
  call L0 !!reloc=R_X86_64_PLT32:__divti3-0x4
  L0:
  pop %rcx
  ret

LITERAL -- the unit's own ledger rows:
  IN-0     8-byte general value             {"kind": "non_opcode_phrase", "phrase": "arrival"}
  STACK-0  8-byte value on the machine stack {"kind": "arch_opcode", "mnem": "push"}
  OUT-0    8-byte general value             {"kind": "non_opcode_phrase", "phrase": "the body's last write to %rax"}

LITERAL -- the machine state after the unit's own `push`:
  stack pointer   18446744073709551608 + seed_rsp
  cell at offset  -8
  cell holds      seed_rax

LITERAL -- the round trip, put to z3:
  pushed  seed_rax
  popped  seed_rax
  solver.add(popped != pushed); solver.check() = unsat
  stack pointer back to  seed_rsp
  stack offset back to   0

LITERAL -- the whole body, walked:
  refused: arch opcode 'call' is a census row, not a silent gap:
           runtime callee not yet attached (Task 59, node 0_3_5_1_8):
           the callee's body is to be extracted from the toolchain's
           libgcc / compiler-rt archive and attached as an ArchUnit
           this caller references, with the producer
           {"kind": "runtime_callee"}
```

GLOSS. `18446744073709551608` is −8 at 64 bits, so the pointer moved
down one slot and back. The value the `push` put at offset −8 is the
value the `pop` takes back, and z3 answers `unsat` to the two being
different — a proof for every value of the register, not a sample. The
STACK-0 row the ledger makes for this unit is exactly that cell. This
unit's own body then transfers into `__divti3`, a compiler support
routine whose body is not in the unit YET, and the walk refuses it by
name with that reason; that refusal is the honest state of the unit,
not a defect of the stack model. Task 59 attaches the callee.

### 2.3 (c) `cpp/regen_36796` — both loads reach the compare

LITERAL:

```
LITERAL -- the unit's own ledger rows:
  X87-0    x87 stack value      {"kind": "arch_opcode", "mnem": "fldt"}
  X87-1    x87 stack value      {"kind": "arch_opcode", "mnem": "fldt"}
  TEMP-0   flags only           {"kind": "arch_opcode", "mnem": "fucomip"}  X87-0,X87-1
  GUARD-0  flag-derived value   {"kind": "flag_pair", "mnem": ["fucomip", "seta"]}  TEMP-0
  OUT-0    1-byte general value {"kind": "flag_pair", "mnem": ["fucomip", "seta"]}  GUARD-0

LITERAL -- the x87 stack after the unit's own two loads:
  position 0 (the top)  x87_0x8_rsp_
  position 1            x87_0x18_rsp_
  depth                 2

LITERAL -- the flag triple the compare leaves:
  setter             fucomip
  left  (the top)    x87_0x8_rsp_
  right (position 1) x87_0x18_rsp_

LITERAL -- the answer term this reference builds:
  If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_),
         Not(fpEQ(x87_0x8_rsp_, x87_0x18_rsp_)),
         Not(Or(fpIsNaN(x87_0x18_rsp_), fpIsNaN(x87_0x8_rsp_)))),
     1,
     0)

LITERAL -- do BOTH loads appear in the answer term?  yes
```

GLOSS. Take `0x18(%rsp) = 2.0` and `0x8(%rsp) = 3.0`. The first `fldt`
loads 2.0 and becomes position 0; the second loads 3.0 and pushes on
top, so position 0 holds 3.0 and position 1 holds 2.0.
`fucomip %st(1),%st` is AT&T order — source `%st(1)`, destination
`%st` — so it compares the top against position 1 and leaves the
triple (`fucomip`, top, position 1). `seta` asks for above-and-ordered,
and both loads are in the answer.

**This is the same term log 153 §4.3 printed off the LEDGER route.**
Section 4.3's block reads
`ZeroExt(56, If(And(Not(x87_0x8_rsp_ < x87_0x18_rsp_), Not(fpEQ(...)), Not(Or(fpIsNaN(...)))),  1, 0))`.
Two routes that share no code path now name one term. That is what the
x87 CORRECTION in §4 below was for.

---

## 3. The table itself

LITERAL — `acceptance57_printed.txt`, part 0:

```
  arch opcodes the corpus's own bodies spell   162
  entries in Reference.opcode_table            162
  entries WITH a term builder                  143
  entries with NO builder (census rows)         19
```

GLOSS. The 162 is COMPUTED, not typed: `acceptance57.py` and the
`CORPUS_MNEMONICS` literal in `reference.py` were both derived from
`canon38_wrapped_{c,cpp,go,rust,swift}.json`, `canon38_interp.json`
and `canon38_regen_store/*.json` over **181,125 body lines**. No entry
is invented for an opcode no body contains, and every opcode any body
contains has exactly one entry. The 19 census rows are `call`, `ud2`,
`jmp`, twelve conditional transfers, and `pcmpeqb` / `pcmpeqd` /
`pmovmskb`.

What the one table folds in, each named with the file it came from:

| folded in | from | what it gave |
|---|---|---|
| producer table | `layer4.py` | the integer, move, extension, shift and flag families, and the `full64` / `cut` write rule |
| condition route | `condition_table.py` | `SUFFIX_TO_COND` and `cond_to_z3` for every `set`/`cmov`/`j` suffix |
| lane builders | `vex_names.py` | real IEEE terms under `RNE`, lane 0 written and the upper lanes kept |
| division | `canon12_behaviour_check.py` | `SDiv`/`UDiv` and `SRem`/`URem` |

Two changes of substance against the superseded route, both settled
rules of the CORE rather than choices made here:

1. **Float opcodes are real IEEE terms.** `canon10` carried the scalar
   float vocabulary as uninterpreted functions (`FADD32`, `FLT64`,
   …), which is precisely why `gate48.py` returned UNDECIDED whenever
   a body spelled a float opcode — the ledger route carried real z3
   FPA and the two were not symbolically comparable. This reference
   builds `fpAdd`/`fpSub`/`fpMul`/`fpDiv` under round-to-nearest-even.
2. **The flag triple answers the carry and overflow suffixes by
   rebuilding them**, rather than remembering separate bits. A
   condition is then exactly what set it.

---

## 4. The CORRECTION written into the tree before any code

Round 12's binding rule 2: a shape the tree lacks is added to the tree
first. One was found and one was written.

**What was wrong.** Both `CORE_0_3_5_4_reference.md`'s design block and
`CORE_0_3_5_4_1_machine_state.md`'s said the x87 positions each hold
"a bit-vector term".

**Why that is wrong.** An x87 register holds the 80-bit extended form.
The ledger route already builds those values at `FPSort(15, 64)`
(`layer4c.py` section 1, `X87_SORT = z3.FPSort(15, 64)`, and
`x87_symbol`), and log 153 §4.3 prints them as `x87_0x18_rsp_` under
`fpEQ`/`fpIsNaN`. z3 cannot compare a bit vector with a float, so a
bit-vector reference could never have been gated against the ledger's
term — the two routes would have been incomparable by construction,
which is the same class of defect as the remainder.

**What was written.** Both design blocks corrected, and a settled rule
added to `machine_state` with its provenance (PROTOCOL §2): an x87
position holds an `FPSort(15, 64)` term, and a load from memory is the
symbol `x87_<mangled memory operand text>`. Recorded in
`node_0_3_5_4_1_machine_state/PROGRESS.md` before a line of code was
written. §2.3 above is the evidence that the correction was the right
one: the reference's answer term and the ledger's are now one term.

No other correction was needed. Nothing is open for the owner.

---

## 5. The guard

LITERAL — `guard57_transcript.txt`, in full:

```
guard57.py -- every artifact task 57 writes, unmodified guard, ONE process.  Nothing was added to any field set, and no artifact was declared out of the walk.
$ python3 check_no_spelling_keys.py <2 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS acceptance57.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage57.json -- no operator token in any key, grouping, pairing or row structure

GUARD EXIT CODE = 0
```

LITERAL — the two checks the standing requirement names:

```
$ grep -c exempt guard57_transcript.txt
0
$ git status --porcelain Research/op_pipeline/check_no_spelling_keys.py
(no output -- the guard file is unmodified)
```

GLOSS. Every JSON this task writes is WALKED, not skipped. Neither
artifact declares `role: generator provenance` — that field was
removed from both after a first run showed it buying an exemption,
which is exactly the failure log 147 §13.7 named. One process, two
paths, nothing added to any field set.

---

## 6. The one permitted edit

LITERAL — `git show --stat 784551a`, restricted to the three files:

```
 Research/op_pipeline/canon10_behaviour_check.py | 1 +
 Research/op_pipeline/canon12_behaviour_check.py | 1 +
 Research/op_pipeline/canon9_behaviour_check.py  | 1 +
 3 files changed, 3 insertions(+)
```

The one line, identical in each, inserted after the shebang:

```
# SUPERSEDED 2026-09-03 by reference.py (node 0_3_5_4 reference): one Reference, one MachineState, one opcode_table; this file is a record and is not edited further.
```

`gate48.py`, `layer4*.py`, `ledger4*.py`, `vex_names.py`,
`condition_table.py` and `check_no_spelling_keys.py` are untouched.

---

## 7. File inventory

New files, all in `PseudoCoupHQ/Research/op_pipeline/`:

| file | lines | what it is |
|---|---|---|
| `reference.py` | 1,660 | THE deliverable: `Reference`, `MachineState`, `OpcodeTable`, `Entry` |
| `acceptance57.py` | 377 | the three acceptance instances, printed with values |
| `acceptance57_printed.txt` | — | its output, LITERAL/GLOSS labelled |
| `acceptance57.json` | — | the same figures as data |
| `coverage57.py` | 236 | reach of the one reference against the superseded route, every unit |
| `coverage57_printed.txt` | — | its output |
| `coverage57.json` | — | the same figures as data |
| `guard57.py` | 128 | the unmodified guard, one process, over both JSON artifacts |
| `guard57_transcript.txt` | — | the transcript pasted in §5 |
| `guard57.json` | — | the guard's own counts |

Edited (the ONE permitted edit, one header comment line each):
`canon9_behaviour_check.py`, `canon10_behaviour_check.py`,
`canon12_behaviour_check.py`.

Planning files touched, all under
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_4_reference/`:

| file | what changed |
|---|---|
| `CORE_0_3_5_4_reference.md` | design block: the x87 correction |
| `PROGRESS.md` | three entries — the file, the three instances, the supersession |
| `node_0_3_5_4_0_opcode_table/PROGRESS.md` | three entries — `SRem`, the one table, real IEEE floats |
| `node_0_3_5_4_1_machine_state/CORE_0_3_5_4_1_machine_state.md` | design block corrected, and the new settled rule with its provenance |
| `node_0_3_5_4_1_machine_state/PROGRESS.md` | the correction record, plus three entries — the stack, the x87 stack, the one state object |

---

## 8. The two lists

### Decided, recorded for audit

1. **The x87 sort correction** — written into both COREs with
   provenance before coding (§4).
2. **`call` is an entry with no builder, with the cause
   "runtime callee not yet attached (Task 59, node 0_3_5_1_8)".**
   No question went to the owner: log_158 TASK 59(b) already rules it. The
   first wording of this log and of `reference.py` said "out of scope",
   which is the SUPERSEDED framing; corrected the same day — §10.
3. **`simulate` walks in text order and refuses a branch.** This is
   exactly what the route the gate calls does today; a branch-merging
   walk is a shape the CORE does not state and was not coded.
4. **A unit record with no body is refused by name.** The superseded
   route walked an empty body to completion and handed back the answer
   register's own seed — an answer to nothing. Those 642 records are
   counted in their own column and kept out of the regression
   comparison, which is what makes the zero honest.
5. **`role: generator provenance` removed from both artifacts** after a
   first guard run showed it buying an exemption.

### Awaiting the owner

*Nothing.*

---

## 9. What this hands the next task

Task 58's `gate.py` imports `Reference` and calls `simulate` /
`answer_of`. The expectation it is to test is now sharp: the 415
remainder withdrawals should prove, because the term is `SRem` on both
routes; and a large part of the 5,602 undecided should decide, because
4,935 units the old route could not walk at all now reach an answer
term, and the float vocabulary is real IEEE on both sides rather than
uninterpreted on one. Neither is claimed here — reach is not a
verdict, and the gate is what produces one.

---

## 10. CORRECTION, 2026-09-03 (same day, after review)

**What was wrong.** The first version of `reference.py`'s header
comment, of `acceptance57.py`'s gloss, and of §1.4 / §2.2 / §8 of this
log said that a `call` into a compiler support routine (`__divti3` and
its family) is "refused by name — library routine, out of scope per
AgentMemory".

**Why it is wrong.** That framing is SUPERSEDED by the owner's round-12
ruling, log_158 TASK 59(b): the callee's body is to be extracted from
the toolchain's libgcc / compiler-rt archive (`gcc
-print-libgcc-file-name`, clang's `libclang_rt.builtins-x86_64.a`,
rustc's bundled compiler-builtins, swift's), the bodies pulled out with
`ar x` + `objdump -d`, and each attached as an ArchUnit the caller
references, with the caller's answer row carrying the producer
`{"kind": "runtime_callee", "callee": "__divti3"}`. Log_158 says it in
as many words of `out_of_scope_library_calls.json`: **"its verdict
superseded; its list stands"**. So these 3,743 units are not out of
scope; they are waiting on an attachment that node 0_3_5_1_8
(`runtime_callee`) delivers in task 59.

**What was changed.**

1. `reference.py` — the header paragraph rewritten; `Entry` gained a
   `cause` field; the `call` entry carries
   `RUNTIME_CALLEE_CAUSE`, and `Reference.step` quotes the entry's own
   cause in its refusal. The other census rows gained their own causes
   too (`TRANSFER_CAUSE`, `NO_TERM_CAUSE`) rather than sharing one
   blanket sentence.
2. `acceptance57.py` — parts 0 and (b) gloss rewritten; part 0 now
   prints each census row's cause, and `acceptance57.json` carries a
   `census_causes` map.
3. `acceptance57.py` and `coverage57.py` re-run. **The figures did not
   move**: 25,827 of 31,078 reach an answer, 4,609 refused, 642 no
   body, 0 regressions, 4,935 gained — only the reason strings changed.
4. This log's §1.4, §2.2 and §8 corrected in place.

LITERAL — the refusal `c/regen_11491` now carries, from
`acceptance57_printed.txt`:

```
  refused: arch opcode 'call' is a census row, not a silent gap:
           runtime callee not yet attached (Task 59, node 0_3_5_1_8):
           the callee's body is to be extracted from the toolchain's
           libgcc / compiler-rt archive and attached as an ArchUnit
           this caller references, with the producer
           {"kind": "runtime_callee"}
```

LITERAL — the phrase is gone from the code, and survives in exactly
one place, the retraction sentence itself:

```
$ grep -c -i "out of scope" reference.py acceptance57_printed.txt
reference.py:0
acceptance57_printed.txt:1
```

The one remaining line reads `earlier "out of scope" framing is
superseded.` — the correction being stated, not the claim being made.
It is left standing rather than deleted, so the record shows what was
corrected.
