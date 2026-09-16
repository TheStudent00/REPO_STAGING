# log 289 — Sail's RISC-V primitives, and the problems in them

## 1. how this was counted

- start: the 354 `execute` clauses in Sail's Lean output (`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/`)
- follow: every definition of the emit they reach (1365 of the emit's 4750)
- keep: every name those bottom out in that the emit does not define; names bound inside a definition are dropped
- full result: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/sail_primitives_inventory.json`

## 2. the primitives

### 2.1 fixed-width values

| primitive | what it does | definitions that use it (NOT a count of uses — corrected 2026-09-15) |
|---|---|---|
| `Sail.BitVec.extractLsb` | the low bits of a value, from bit hi down to bit lo | 325 |
| `Sail.BitVec.updateSubrange` | write bits hi..lo of a value | 150 |
| `Sail.BitVec.length` | how many bits a value has | 54 |
| `Sail.BitVec.zeroExtend` | widen, filling with zeros | 2 |
| `Sail.BitVec.signExtend` | widen, copying the top bit | 1 |
| `Sail.BitVec.truncate` | narrow to the low bits | 2 |
| `shift_bits_left` | shift left by a value | 12 |
| `shift_bits_right` | shift right by a value | 10 |
| `BitVec.access` | one bit of a value | 142 |
| `BitVec.update` | set one bit of a value | 26 |
| `BitVec.countTrailingZeros` | zeros below the lowest one | 5 |
| `BitVec.countLeadingZeros` | zeros above the highest one | 5 |
| `BitVec.sshiftRight` | shift right, copying the top bit | 1 |
| `BitVec.join1` | join single bits into a value | 5 |
| `+++` | join two values end to end | 94 |
| `^^^` | bit by bit exclusive or | 74 |
| `&&&` | bit by bit and | 55 |
| `|||` | bit by bit or | 27 |
| `<<<` | shift left by a count | 22 |
| `>>>` | shift right by a count | 33 |
| `==` | equal | 290 |
| `!=` | not equal | 59 |

### 2.2 unbounded numbers

| primitive | what it does | definitions that use it (NOT a count of uses — corrected 2026-09-15) |
|---|---|---|
| `+i` | add | 119 |
| `-i` | subtract | 233 |
| `*i` | multiply | 116 |
| `^i` | raise to a power | 54 |
| `Int.tdiv` | divide, toward zero | 42 |
| `Int.tmod` | remainder, toward zero | 24 |
| `Int.ediv` | divide, Euclidean — NOT flooring; the two differ on a negative divisor (`7 / -2` is -3, flooring gives -4) | 2 |
| `Int.natAbs` | size without the sign | 3 |
| `BitVec.toInt` | read a value as a signed number | 36 |
| `BitVec.toNatInt` | read a value as an unsigned number | 112 |
| `BitVec.addInt` | add a number to a value | 19 |
| `BitVec.subInt` | subtract a number from a value | 7 |
| `get_slice_int` | take bits out of a number | 4 |
| `<b` | less than | 65 |
| `≤b` | less than or equal | 86 |
| `>b` | greater than | 61 |
| `≥b` | greater than or equal | 73 |

### 2.3 containers

| primitive | what it does | definitions that use it (NOT a count of uses — corrected 2026-09-15) |
|---|---|---|
| `Vector` | a container of values, its length in its type | 135 |
| `vectorUpdate` | write one element | 99 |
| `vectorInit` | a container with every element the same | 15 |
| `Vector.length` | how many elements | 4 |
| `untilFuelM` | repeat until a test holds, with a bound on the repeats | 3 |

### 2.4 machine state

- the emit defines these itself (`rX_bits`, `wX_bits`, `readReg`, `vmem_read`, `vmem_write`, the control registers), and they bottom out in the lean-sail package's own machine: `/work/proof/.lake/packages/Sail/Sail/ConcurrencyInterfaceV1.lean` (`readReg`, `writeReg`, `writeByte`)

### 2.5 declared with no body

- 75 declarations in `RiscvExtras.lean`, all distinct; 73 of them are reached from the execute clauses

#### 2.5.1 float arithmetic — 12

| declaration | signature |
|---|---|
| `riscv_f16Add` | BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) |
| `riscv_f16Div` | BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) |
| `riscv_f16Mul` | BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) |
| `riscv_f16Sub` | BitVec 3 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) |
| `riscv_f32Add` | BitVec 3 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) |
| `riscv_f32Div` | BitVec 3 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) |
| ... 6 more | |

#### 2.5.2 float fused multiply-add — 3, square root — 3, round to integer — 3

| declaration | signature |
|---|---|
| `riscv_f16MulAdd` | BitVec 3 → BitVec 16 → BitVec 16 → BitVec 16 → (BitVec 5 × BitVec 16) |
| `riscv_f32MulAdd` | BitVec 3 → BitVec 32 → BitVec 32 → BitVec 32 → (BitVec 5 × BitVec 32) |
| `riscv_f64MulAdd` | BitVec 3 → BitVec 64 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64) |
| `riscv_f16Sqrt` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 16) |
| `riscv_f32Sqrt` | BitVec 3 → BitVec 32 → (BitVec 5 × BitVec 32) |
| ... 4 more | |

#### 2.5.3 float compare — 15

| declaration | signature |
|---|---|
| `riscv_f16Eq` | BitVec 16 → BitVec 16 → (BitVec 5 × Bool) |
| `riscv_f16Le` | BitVec 16 → BitVec 16 → (BitVec 5 × Bool) |
| `riscv_f16Le_quiet` | BitVec 16 → BitVec 16 → (BitVec 5 × Bool) |
| `riscv_f16Lt` | BitVec 16 → BitVec 16 → (BitVec 5 × Bool) |
| `riscv_f16Lt_quiet` | BitVec 16 → BitVec 16 → (BitVec 5 × Bool) |
| `riscv_f32Eq` | BitVec 32 → BitVec 32 → (BitVec 5 × Bool) |
| ... 9 more | |

#### 2.5.4 conversions — 31

| declaration | signature |
|---|---|
| `riscv_f16ToF32` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 32) |
| `riscv_f16ToF64` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 64) |
| `riscv_f16ToI32` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 32) |
| `riscv_f16ToI64` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 64) |
| `riscv_f16ToUi32` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 32) |
| `riscv_f16ToUi64` | BitVec 3 → BitVec 16 → (BitVec 5 × BitVec 64) |
| ... 25 more | |

#### 2.5.5 platform — 8

| declaration | signature |
|---|---|
| `cancel_reservation` | Unit → SailM Unit |
| `get_16_random_bits` | Unit → SailM (BitVec 16) |
| `load_reservation` | Arch.pa → Nat → SailM Unit |
| `match_reservation` | Arch.pa → Bool |
| `plat_term_read` | Unit → SailM String |
| `sys_enable_experimental_extensions` | Unit → Bool |
| `valid_reservation` | Unit → Bool |
| `plat_term_write` | α → SailM Unit |

## 3. the problems

### 3.1 the float operations have no meaning in Lean

- 40 of the 67 float declarations have no body; 27 have one from the universal type (`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_harness/leanpath_src/Kinds.lean`), agreeing with Sail's own SoftFloat at 183,300 points
- consequence: a definition that calls one of the 40 has no meaning we can compute

### 3.2 the platform declarations have no meaning in Lean

- 8: terminal read and write, the atomic reservation (four of them), random bits, an experimental-extensions flag
- consequence: the atomic and system instructions cannot be expressed as a value

### 3.3 no bridge from Sail's primitives to the universal type

- proved today: 1 (Sail's truncation equals the kinds' wrap, `Universal.lean`)
- needed: one proved statement per primitive above, roughly 44 of them
- consequence: section 1.2 of log 288 cannot be completed by rewriting alone

### 3.4 containers are outside the universal type

- `Vector` and memory hold elements; the universal type is one element
- consequence: the vector instructions and every load and store need a container form first

### 3.5 our reader, not Sail

- 93 of Sail's 353 definitions have been turned into pure forms
- consequence: the other 260 are complete in Lean and unusable by our pipeline

## 4. pointers

- the inventory: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/sail_primitives_inventory.json`
- Sail's Lean output: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/`
- the universal type and its kinds: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_harness/leanpath_src/Universal.lean`, `Kinds.lean`
- the five sections with their marks: `PRIVATE/PseudoCoupHQ/DevComms/log_288_project_communication_template_with_completion_marks.md`
