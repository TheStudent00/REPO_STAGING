# RISC-V as a second architecture — the handful, level 0, the claim, and the surface

Project node: **arch_unit_oracle**
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`).
Task **rv1**, brief `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv1_brief.md`.
the owner, 2026-09-10: *"explore it as an option"*, not a pivot.

**THE FIRST LINE THE BRIEF ASKS FOR.** Section 3's level-0 result is **a
check at points, not an equality**: the RISC-V reference in this folder
(`riscv_reference.py`) and the ratified Sail model's own C simulator
(`sail_riscv_sim`) were run against each other at **860,304 concrete
points** over **44 instructions**, and they agreed at every one of them.
Agreement at 860,304 points is evidence that the two readings compute the
same mapping; it is not a proof that they do.

Every number below carries the lane that produced it. Lane logs are on the
tower at
`<runs>/rv1/agent/logs/<stamp>__<lane>.log`; the
lane scripts are in this repository under `lanes_rv1/`.

---

## 1. What the objects are

- **the handful** — the ten cells of the arch-opcode model table that task
  h1 named, each one row of
  `PRIVATE/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`
  keyed by the machine triple (`mnem`, operand shape, `key_width`).
- **a corpus unit** — one probe of the operator-equivalence corpus: a
  function body a compiler emitted for one (operator, operand types),
  named `<lang>/op_<n>`, with its own source in
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/probe_manifest_<lang>.json`
  and its proved x86 term in
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/term66_store`.
- **the RISC-V reference** (`riscv_reference.py`) — the riscv64 twin of
  `PRIVATE/PseudoCoupHQ/Research/op_pipeline/reference.py`: one z3
  term per place an instruction writes, read off the instruction's own
  disassembled text.
- **the Sail model** — the RISC-V architecture's own executable
  specification, at `/sources/sail-riscv` inside a lane, compiled to the C
  simulator `sail_riscv_sim`. It is level 0 for RISC-V for free: where x86
  holds level 0 as our own reading of Intel's prose, RISC-V publishes its
  semantics as a ratified artifact.

---

## 2. The handful — ten corpus units compiled for riscv64

Lane `rv1_l14_regenerate.sh` (and, for the first carve, `rv1_l6_carve_again.sh`).
Artifacts `units.json`, `carved.json`.

**The calling convention, stated (the RISC-V psABI, `lp64d`).** Integer
arguments arrive in `a0 .. a7` (`x10 .. x17`) in order and an integer
answer leaves in `a0`; floating-point arguments arrive in `fa0 .. fa7`
(`f10 .. f17`) and a floating-point answer leaves in `fa0`. **There is no
flags register anywhere in the architecture**: a comparison writes a
general register.

**The ship optimisation levels are the corpus's own, untouched**: c is
`clang -std=c17 -O1 -c`, go is `go build`. What was added is the target
and nothing else — `--target=riscv64-unknown-linux-gnu` for clang,
`GOARCH=riscv64 GOOS=linux` for go — plus `-nostdlibinc`, whose cause is
in §6 flag 1.

**Table 1 — the ten units, x86-64 body beside riscv64 body.** The cell is
the machine key; the unit is the corpus unit that attests it.

| cell (`mnem`, shape, width) | unit | source | x86-64 ship body | riscv64 ship body |
|---|---|---|---|---|
| `add` gpr_gpr 32 | go/op_312 | `a + b` int32, int32 | `add %ebx,%eax ; ret` | `c.add a0, a1 ; jalr zero, 0x0(ra)` |
| `sub` imm_gpr 64 | — | — | — | — |
| `imul` gpr_gpr 32 | c/op_174 | `a * b` int32_t, int32_t | `mov %edi,%eax ; imul %esi,%eax ; ret` | `mulw a0, a1, a0 ; c.jr ra` |
| `sar` cl_gpr 32 | c/op_714 | `a >> b` int32_t, int32_t | `mov %esi,%ecx ; mov %edi,%eax ; sar %cl,%eax ; ret` | `sraw a0, a0, a1 ; c.jr ra` |
| `shr` cl_gpr 64 | c/op_726 | `a >> b` uint64_t, int32_t | `mov %esi,%ecx ; mov %rdi,%rax ; shr %cl,%rax ; ret` | `srl a0, a0, a1 ; c.jr ra` |
| `idiv` gpr_one 32 | c/op_210 | `a / b` int32_t, int32_t | `mov %edi,%eax ; cltd ; idiv %esi ; ret` | `divw a0, a0, a1 ; c.jr ra` |
| `cmovne` gpr_gpr 32 | c/op_185 | `a * b` int64_t, bool | `xor %eax,%eax ; test %esi,%esi ; cmovne %rdi,%rax ; ret` | `czero.eqz a0, a0, a1 ; c.jr ra` |
| `setne` gpr_one 8 | c/op_498 | `a != b` int32_t, int32_t | `xor %eax,%eax ; cmp %esi,%edi ; setne %al ; ret` | `c.xor a0, a1 ; sltu a0, zero, a0 ; c.jr ra` |
| `addss` xmm_xmm 32 | c/op_105 | `a + b` int32_t, float | `cvtsi2ss %edi,%xmm1 ; addss %xmm1,%xmm0 ; ret` | `fcvt.s.w fa5, a0, dyn ; fadd.s fa0, fa0, fa5, dyn ; c.jr ra` |
| `cvtsi2sd` gpr_xmm 64 | c/op_106 | `a + b` int32_t, double | `cvtsi2sd %edi,%xmm1 ; addsd %xmm1,%xmm0 ; ret` | `fcvt.d.w fa5, a0 ; fadd.d fa0, fa0, fa5, dyn ; c.jr ra` |
| `add` gpr_gpr 32, the c reading | c/op_102 | `a + b` int32_t, int32_t | `lea (%rdi,%rsi,1),%eax ; ret` | `c.addw a0, a1 ; c.jr ra` |

Ten bodies carved of ten attempted. Nine are c units through clang and one
(go/op_312) is a go unit through the go toolchain, so both compilers the
image can aim at riscv64 are exercised.

**Two readings of the row count, both stated.** The brief names ten cells;
the `sub` immediate-form cell attests **no corpus unit at all**, because
the probe corpus is (operator × holder pair) and never puts a literal on
an operand (§6 flag 2). So: **nine of the brief's ten cells carry a unit**,
and the tenth compiled body is `c/op_102`, the c reading of the same int32
addition the go unit carries — a row of its own, never folded into the
cell it does not attest.

**One row's cell is not the row's own.** The 32-bit `cmovne` cell is
attested only by swift units, and the image has no swift for riscv64;
`c/op_185` is the nearest attested c unit of the same mnemonic, and the
cell it actually attests is `cmovne` gpr_gpr **64**. That is recorded on
the row in `units.json` as `attests_cell`.

**The instruction vocabulary the ten riscv64 bodies spell: 15 mnemonics.**
`c.jr` (9), then one each of `c.add`, `c.addw`, `c.xor`, `czero.eqz`,
`divw`, `fadd.d`, `fadd.s`, `fcvt.d.w`, `fcvt.s.w`, `jalr`, `mulw`,
`sltu`, `sraw`, `srl`.

---

## 3. Level 0 for RISC-V — two readings, checked at points

### 3(a) The reference: `riscv_reference.py`

Built in `reference.py`'s own shape, section for section, so the two can be
read side by side: the widths and register tables, `MachineState`, the
operand reader, the term builders, the one opcode table, the node's class.
1,174 lines, 921 of them code.

Four things are in it that have no counterpart in the x86 file, and each is
a fact of the architecture rather than a choice:

- **There is no flags register.** `MachineState` has no `flags` attribute.
  x86 spends `build_flag_only`, `carry_bit`, `overflow_bit`,
  `predicate_of` and the whole `condition_table.py` on the flags; RISC-V
  spends `slt` / `sltu` — a comparison writes a general register a 0 or a
  1 — and the six branches, which read their comparison inside themselves.
- **Every register write is the full 64 bits.** x86's `full64` /
  `place_bits` / `KEEPS_THE_UPPER_BITS` rule has no counterpart: the
  architecture has no sub-register names. The 32-bit forms (`addw`,
  `srliw`, `mulw`, …) compute at 32 bits and **sign-extend** into the whole
  register, which is one function here (`sign_extend_w`, 5 lines).
- **Register `x0` is the constant zero**, so the assembler's reading aids
  (`li`, `mv`, `ret`, `nop`, `seqz`) need no instructions of their own.
  That is why every body is read through `llvm-objdump -M no-aliases`: an
  aid is a spelling, and a spelling is not machine form.
- **Division does not trap.** RISC-V defines every case: `div` by zero is
  all ones, `rem` by zero is the dividend, `divu` by zero is 2^64−1, and
  `div`(most negative, −1) is the most negative value with `rem` 0.

### 3(b) The ratified Sail model, run concretely

Per instruction variant the harness (`sail_points.py`) writes one
bare-metal assembly program of exactly this shape, links it at
`0x80000000` — the reset address the simulator's default configuration
gives — assembles it with `clang --target=riscv64-unknown-elf
-march=rv64gc_zicond -mabi=lp64d -nostdlib -fuse-ld=lld`, and runs it under
`sail_riscv_sim`:

- `la s0, inputs ; la s1, results ; li s2, N`
- loop: `ld a0, 0(s0)` — the first input
- `ld a1, 8(s0)` — the second input
- **the one instruction under test**, writing `a2`
- `sd a2, 0(s1)` — the output
- `addi s0, s0, 16 ; addi s1, s1, 8 ; addi s2, s2, -1 ; bnez s2, loop`
- store 1 into `tohost`, then spin

The simulator finds `tohost` by symbol and stops when it is written; the
results are read back with `--test-signature`, which prints the region
between `begin_signature` and `end_signature` as 32-bit words, the low word
of each 64-bit result first. The reference's own term for the same
instruction is then evaluated at each point by z3 substitution and
`simplify`.

**The points.** The edge values first — 0, 1, −1, 2, −2, 3, −3, the most
negative and largest signed values, all ones, and every power of two with
both its neighbours (90 distinct values) — then random points, at most
20,000 per instruction.

**Table 2 — level 0 at points, by instruction family.** Lanes
`rv1_l9_sail_full.sh` and `rv1_l10_czero.sh`; artifacts
`level0_points.json`, `level0_points_zicond.json`.

| family | instructions | variants | points | agree | disagree | unevaluated |
|---|---|---|---|---|---|---|
| register/register integer and logic | `add and or sll slt sltu sra srl sub xor` | 1 each | 200,000 | 200,000 | 0 | 0 |
| register/register, 32-bit forms | `addw sllw sraw srlw subw` | 1 each | 100,000 | 100,000 | 0 | 0 |
| register/immediate | `addi andi ori slti sltiu xori` | 20 each | 120,000 | 120,000 | 0 | 0 |
| shift by immediate | `slli srai srli` | 64 each | 59,904 | 59,904 | 0 | 0 |
| register/immediate, 32-bit | `addiw` | 20 | 20,000 | 20,000 | 0 | 0 |
| shift by immediate, 32-bit | `slliw sraiw srliw` | 32 each | 60,000 | 60,000 | 0 | 0 |
| upper immediate | `lui` | 400 | 400 | 400 | 0 | 0 |
| multiply | `mul mulh mulhsu mulhu mulw` | 1 each | 100,000 | 100,000 | 0 | 0 |
| divide and remainder | `div divu rem remu divw divuw remw remuw` | 1 each | 160,000 | 160,000 | 0 | 0 |
| conditional zero (Zicond) | `czero.eqz czero.nez` | 1 each | 40,000 | 40,000 | 0 | 0 |
| **total** | **44 instructions** | **858** | **860,304** | **860,304** | **0** | **0** |

**Zero disagreements, so zero defects were found in (a) and no row had to
be fixed.** The brief's instruction — "a disagreement is a defect in (a),
fixed with the row shown" — had nothing to act on.

**What is NOT checked this way, said out loud rather than counted as
agreement** (54 mnemonics, listed with their cause in
`level0_points.json` under `refused_by_name`):

| refused | count | cause |
|---|---|---|
| `auipc` | 1 | its second input is the program counter, which the harness cannot present as an input |
| the loads, stores, branches and jumps | 19 | their effect is not a value the harness can store from a register, so the brief's shape — one instruction between loads of its inputs and a store of its outputs — does not state them |
| the floating-point family | 34 | the brief's §3 names the base integer set; these are in the reference because the handful's two float bodies spell them |

Peak RSS of the sweep: **56.4 MB** against the stated 6 GB ceiling; the
named abort `ABORT_MEMORY_RV1` was never raised.

---

## 4. The claim, measured

Lane `rv1_l14_regenerate.sh`; artifact `claim.json`. z3 at 3,000 ms per
comparison, at **the unit's own answer width**.

**How the two architectures are put in one place.** The k-th argument of a
kind is bound to ONE shared z3 symbol on both sides: for c the k-th integer
argument is `rdi, rsi, rdx, rcx, r8, r9` on x86-64 and `a0 .. a7` on
riscv64, the k-th floating-point argument `xmm0 .. xmm7` and `fa0 .. fa7`;
go's own register rule names `rax, rbx, rcx, …` on x86-64 and `a0 .. a7` on
riscv64. The x86 term is **re-derived** by walking the unit's own recorded
ship body with `op_pipeline/reference.py`, because the term store holds the
term as text and this line has no reader that turns text back into a z3
object; the store's recorded text is on every row and matched the
re-derivation on 9 of 10 rows (the tenth is §6 flag 3).

**Table 3 — the ten units' terms across the two architectures.**

| unit | cell | answer width | terms identical after `Term.normalize` | equal by z3 | differ | undecided |
|---|---|---|---|---|---|---|
| go/op_312 | `add` gpr_gpr 32 | 32 | yes | — | — | — |
| — | `sub` imm_gpr 64 | — | no unit | — | — | — |
| c/op_174 | `imul` gpr_gpr 32 | 32 | yes | — | — | — |
| c/op_714 | `sar` cl_gpr 32 | 32 | yes | — | — | — |
| c/op_726 | `shr` cl_gpr 64 | 64 | yes | — | — | — |
| c/op_210 | `idiv` gpr_one 32 | 32 | no | no | **yes** | — |
| c/op_185 | `cmovne` gpr_gpr 64 | 64 | no | no | **yes** | — |
| c/op_498 | `setne` gpr_one 8 | 8 | no | no | **yes** | — |
| c/op_105 | `addss` xmm_xmm 32 | 32 | yes | — | — | — |
| c/op_106 | `cvtsi2sd` gpr_xmm 64 | 64 | yes | — | — | — |
| c/op_102 | `add` gpr_gpr 32, c reading | 32 | yes | — | — | — |
| **totals** | | | **7 identical** | **0** | **3** | **0** |

Nothing was undecided; the solver never timed out.

**The three differences, grouped by cause. Two causes, not three.**

**Cause A — the two ABIs' argument-extension rules differ (2 rows).** The
System V x86-64 rule leaves the bits above a narrow argument unspecified,
so clang reads only the argument's own width; the RISC-V psABI requires a
narrow argument to arrive sign- or zero-extended to the whole 64-bit
register, so clang reads all 64 bits. Neither compiler is wrong; the
arrival contract is.

- `c/op_498`, `a != b` on `int32_t`. x86: `If(Extract(31, 0, v0) ==
  Extract(31, 0, v1), 0, 1)`. riscv64: `If(v0 ^ v1 == 0, 0, 1)`.
  Counterexample: `arg0 = 16500306186977935360, arg1 = 0`.
- `c/op_185`, `int64_t * bool`. x86: `If(Extract(31, 0, v0) == 0, 0, v1)` —
  `test %esi,%esi` reads 32 bits of the `bool` argument's register.
  riscv64: `If(v0 == 0, 0, v1)` — `czero.eqz` reads all 64.
  Counterexample: `arg0 = 18446744073709551607,
  arg1 = 16390304541154738176`.

**Cause B — x86's division is a partial mapping and RISC-V's is total (1
row).** `c/op_210`, `a / b` on `int32_t`.

- x86: `Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0) >> 31,
  Extract(31, 0, v0)), <the divisor sign-extended to 64>))` — `idiv` on a
  zero divisor raises, so the term says nothing about that region.
- riscv64: `If(Extract(31, 0, v1) == 0, 4294967295,
  If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) ==
  4294967295), 2147483648, bvsdiv_i(Extract(31, 0, v0),
  Extract(31, 0, v1))))` — `divw` defines both the zero divisor and the
  overflow.
- Counterexample: `arg0 = 2147483648, arg1 = 0`.

**Two differences that are NOT differences, and why they are worth
naming.**

- **The widening.** go's int32 addition lowers to `c.add a0, a1`, which is
  a 64-bit add, while clang's lowers to `c.addw a0, a1`, which is a 32-bit
  add sign-extended. At the unit's own answer width of 32 both are the same
  function, so both rows are identical after `Term.normalize`; the
  widening only shows above the answer width.
- **The lanes.** x86's `cvtsi2ss` writes lane 0 of an `xmm` register and
  keeps the 96 bits above it, so the x86 walk records `xmm1` as an
  ARRIVING register on `c/op_105` and `c/op_106` (the column
  `x86_arrivals_beyond_the_arguments` in `claim.json`). RISC-V has no
  lanes: `fcvt.s.w` writes the whole register, NaN-boxed. At the answer
  width the two agree exactly, and the rounding is round-to-nearest-even on
  both — `llvm-objdump` prints RISC-V's rounding operand as `dyn`, which is
  the `fcsr` register, and `fcsr` holds round-to-nearest-even at reset.

---

## 5. The surface, counted

Lane `rv1_l14_regenerate.sh`; artifact `surface.json`. Counted with
python's own `ast`, not by hand.

**Table 4 — what had to be written, by layer.**

| layer | file written | total lines | code lines |
|---|---|---|---|
| lifter (the reference) | `riscv_reference.py` | 1,174 | 921 |
| carve | `riscv_carve.py` | 291 | 253 |
| calling convention / canonical form | `claim_check.py` | 326 | 286 |
| attestation | `pick_units.py` | 303 | 263 |
| level 0 check (beside the four the brief names) | `sail_points.py` | 550 | 451 |
| **all five** | **5 files** | **2,644** | **2,174** |

**Table 5 — the x86 counterpart of each layer**, so the two sit side by
side. Line counts as of 2026-09-10; `reference.py` is being changed by task
ref2 in the same hour, so its count is an as-of and not a fixed figure.

| layer | the x86 counterpart | its lines |
|---|---|---|
| lifter (the reference) | `op_pipeline/reference.py` | 3,093 |
| lifter (the reference) | `op_pipeline/condition_table.py` | 464 |
| carve | `op_pipeline/lane_gen.py`, the four carve functions inside its `DRIVER` | 116 |
| calling convention / canonical form | `op_pipeline/canonical_form.py`, `Prelude` + `Epilogue` + `Labels` | 154 |
| calling convention / canonical form | `op_pipeline/ledger.py`, `DESTINATION_RULES` + `answer_registers_of_body` + `pick_scratch` + `register_text` + `weave` | 372 |
| attestation | `oracle/arch_opcodes/model/model_table.py`, `attestation` + `attest_command` + `arch_opcode_rows` + `lines_of_unit` + `place_row` | 174 |
| level 0 check | none — level 0 on x86 IS the reference, and its independent check is task ref1's K-framework reading | 0 |

**Table 6 — what transferred untouched.** This task wrote nothing outside
`Research/oracle/riscv/`; every object below was read and none was changed.

| read unchanged | what it is | size |
|---|---|---|
| `op_pipeline/term66_store` | the term store: every unit's proved z3 term | 332 shards |
| `oracle/arch_opcodes/model/model_table.json` | the arch-opcode model table with the corpus's attestation | 71,778 rows |
| `op_pipeline/probe_manifest_c.json` | the c probe corpus's own sources | 750 probes |
| `op_pipeline/probe_manifest_go.json` | the go probe corpus's own sources | 744 probes |
| `op_pipeline/op_units_c.json` | the c units' recorded x86 ship bodies | 750 probes |
| `op_pipeline/op_units_go.json` | the go units' recorded x86 ship bodies | 744 probes |
| `op_pipeline/reference.py` | the x86 reference, called to re-derive each unit's own x86 term | 3,093 lines |
| `op_pipeline/term.py` | `Term.normalize`, called to put both architectures' terms in one comparison form | 2,348 lines |

**The answer to "does solving one architecture solve the rest".**

- **What did not transfer: the READING of a body.** 2,644 lines, and 1,174
  of them — 44% — are the lifter alone. An architecture's instruction
  meanings are its own; nothing about x86's table helps.
- **What did not transfer: the arrival contract.** The two ABIs' rules for
  a narrow argument differ, and that difference is what produced two of the
  three disagreements in §4. This is the layer the brief calls calling
  convention / canonical form.
- **What DID transfer, and it is the larger half of the machinery:** the
  TERM (a z3 expression over bit vectors is architecture-neutral by
  construction), `Term.normalize` (2,348 lines, called unchanged), the term
  store, the model table, the attestation, the probe corpus, and the
  comparison itself — z3 decided x86 against riscv64 with no new
  machinery at all.
- **The shape of the transfer, stated once:** a certificate of this line
  says *this source computes this term*. The term is the same on both
  architectures. What has to be re-verified per architecture is the
  compiler's back end and the ABI's arrival contract — which is exactly
  what task rv2 is written to measure.

---

## 6. Flags

1. **The image has no riscv64 glibc headers.** Every c probe's own
   `#include <stdint.h>` reached `/usr/include/stdint.h`, the x86-64
   build's, and clang refused. LITERAL, lane `rv1_l4_carve_diagnostics.sh`:
   `In file included from /usr/lib/llvm-21/lib/clang/21/include/stdint.h:56:
   /usr/include/stdint.h:26:10: fatal error: 'bits/libc-header-start.h'
   file not found`. `-nostdlibinc` sends the include to clang's own
   per-target resource headers and the optimisation level is untouched.
   Ten of ten probes then compiled.
2. **The `sub` immediate-form cell attests no corpus unit.** The probe
   corpus is (operator × holder pair) and never puts a literal on an
   operand, so no body spells an immediate-form subtract at 64. The row is
   a flag, not a substitution.
3. **`c/op_105`'s store text and the re-derivation differ by the upper
   lane, not by the computation.** The store's recorded
   `layer5_normalized_text` is `Concat(Extract(63, 32, v1), <the 32-bit
   sum>)` — 64 bits — while the unit's `result_width` is 32, and the
   comparison here is at the unit's own answer width as the brief directs.
   The re-derivation is exactly the low 32 bits of the stored term.
4. **One instruction outside RV64I+M is in the reference**, and it is there
   because a carved body spells it: `czero.eqz` of the Zicond extension,
   which clang 21 emits for the handful's select. Its co-instruction
   `czero.nez` is beside it. Both agree with the Sail model at 20,000
   points each.
5. **Three tool spellings the brief did not foresee**, each quoted in lanes
   4 and 5: `llvm-objdump` has no `--no-aliases` (`-M no-aliases` is its
   own spelling); a go riscv64 binary declares no RISC-V attributes, so the
   disassembler decodes its compressed halfwords as `<unknown>` until
   `--mattr=+m,+a,+f,+d,+c` names them; `file` is absent from the image.
6. **A new sub-node is wanted, and it is the owner's to create, not this
   task's.** This folder is a RISC-V line under `arch_unit_oracle` with its
   own reference, its own level-0 oracle and its own carve; it has no
   planning node.

---

## 7. The files

| file | what it is |
|---|---|
| `riscv_reference.py` | the RISC-V reference: one z3 term per written place, in `reference.py`'s own shape |
| `sail_points.py` | the level-0 check: the bare-metal harness, the Sail simulator, and the reference's term evaluated at the same points |
| `riscv_carve.py` | compile a unit's own source for riscv64 at the corpus's ship level and carve at the function symbol |
| `pick_units.py` | the ten cells' own attested corpus units, with their sources and their x86 terms |
| `claim_check.py` | each unit's riscv64 term against its own x86-64 term, z3 at 3,000 ms |
| `surface.py` | the per-architecture surface, counted by layer with `ast` |
| `units.json` | the ten rows: cell, unit, source, x86 ship body, x86 term |
| `carved.json` | the riscv64 bodies |
| `level0_points.json`, `level0_points_zicond.json` | the level-0 point check |
| `sail_smoke.json` | the same check at 200 points, run first to show the harness worked |
| `claim.json` | §4's table with both terms and every counterexample |
| `surface.json` | §5's counts |
| `lanes_rv1/` | every lane submitted, in order |
