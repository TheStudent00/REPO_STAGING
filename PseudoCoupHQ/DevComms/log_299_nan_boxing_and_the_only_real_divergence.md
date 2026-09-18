# log 299 — NaN-boxing, and the only real divergence between the two architectures

2026-09-17. Follows log 298. the owner asked a question that turned out to be the
whole finding:

> what about at the arch-opcode level?

## 1. Reading the same run one level down

Log 295 reported the cross-architecture check at the ARCH-UNIT level: 507
units, 86 differing after the integer arrival promises. Read at the
ARCH-OPCODE level — 92 RISC-V mnemonics, each scored over every unit whose
body spells it — the same data says something much sharper.

| | opcodes |
|---|---|
| always agrees with x86, never differs | **31** |
| mixed | 13 |
| never agrees | **16** |

And the never-agrees list is almost entirely SINGLE precision:

```
feq.s  fadd.s  fsub.s  fmul.s  fdiv.s  fmv.w.x
fcvt.s.w  fcvt.s.l  fcvt.s.lu  fcvt.s.wu  fcvt.d.s
```

while their DOUBLE-precision twins mostly agree — `fcvt.d.w`, `fcvt.d.l`,
`fcvt.d.wu` and `fdiv.d` always; `fadd.d`, `fsub.d`, `fmul.d`, `fmv.d.x`
mixed.

That split is not a property of floating point. **It is NaN-boxing.** RISC-V
requires a single-precision value in a 64-bit f-register to carry all ones in
bits 63:32, and its operations rely on it; x86 has no such rule. And
`abi_assumptions` skipped every xmm place outright, so float arguments got
**no arrival promise at all** — the same omission that cost 92 units on the
integer side, made again on the float side and not noticed because the
failures were filed under "a float term is a free function" rather than "no
precondition".

`riscv_term` takes `Extract(63, 0, symbol)` as the f-register, so the promise
is one line on bits 63:32 of the shared symbol, and the x86 side, which reads
only 31:0, is untouched by it.

## 2. What the one line was worth

| outcome | free arguments | integer promises | **+ NaN-boxing** |
|---|---|---|---|
| DIFFER | 184 | 86 | **20** |
| EQUAL_BY_Z3 | 63 | 157 | **230** |
| IDENTICAL_AFTER_NORMALIZE | 174 | 174 | 174 |
| UNDECIDED | 36 | 40 | 33 |
| walks refused | 50 | 50 | 50 |

**404 of 507 units agree — 80%.** And nothing regressed: no unit that agreed
before disagrees now.

## 3. The twenty, and the two

| cause | n |
|---|---|
| a float term is a FREE FUNCTION (NaN payload or rounding unpinned) | 10 |
| x86 loads an unconstrained rip-relative constant | 4 |
| x86 reads an arrival beyond the declared arguments | 4 |
| **genuine — no free term, no extra arrival** | **2** |

The two:

```
c/op_210   a / b   width 32   arg1 = 0
c/op_217   a / b   width 64   arg1 = 0
```

Both are **division by zero**, and it is the one true behavioural divergence
between the two architectures in this corpus: RISC-V's `div` and `divw`
DEFINE it as all-ones; x86's `idiv` TRAPS.

**Across 507 compiler-operators lowered on two architectures, the only
genuine divergence is division by zero.** Everything else was either the
question asked without a precondition — 152 units, over two rounds — or one
of three named modelling gaps.

## 4. The float decode: narrowed hard, not closed

Eight lanes. What is now ESTABLISHED, each by a run rather than by reading:

| | |
|---|---|
| the Lean model HAS the float instructions | `FextInsts.lean`, `DextInsts.lean`, `FEQ_S` in `Defs.lean` |
| the DECODER has float clauses | 104 float constructors in `InstsEnd.lean`, where `encdec_backwards` lives |
| `hartSupports Ext_F` | `true` — the static config allows it |
| `currentlyEnabled Ext_F` on the walker's state | **false** |
| after writing misa's F and D bits and mstatus.FS | **true** — so the writes work |
| `feq.s` and `fadd.d` with the extension enabled | **still ILLEGAL** |
| the integer control on the same state | decodes throughout |

So it is none of: a missing model, missing decoder clauses, a broken state
write, or the extension predicate. That is a much smaller problem than it was,
and every one of those was a live hypothesis before it was tested.

What is NOT established is which clause or guard still refuses. The next thing
to look at is whether `encdec_backwards` covers the float instructions at all
— `F_BIN_TYPE_X_S (rs2, rs1, rd, .FEQ_S)` is visible in the FORWARDS
direction and I did not find it in the backwards one, which would explain the
symptom exactly. That is a reading of the emission, not a state question, and
I stopped rather than guess a ninth time.

**Six of the eight lanes failed on Lean spelling rather than on anything about
the model**: `readReg` overloaded, `Register.misa` dotted, the executable
library's name, an unqualified `Ext_F`. The decode symptom is stable and
agrees across l114, l116, l117 and l118, so it is not in doubt; only my
ability to introspect around it was. That ratio is the finding worth keeping
about how this went.

## 5. Two lists

Decided, recorded for audit:

- the NaN-boxing promise is one entry in `abi_assumptions`, guarded on the
  declared type, and the reason it belongs there is written beside it;
- the arch-opcode reading is derived from `claim_abi.json`, not a new run;
- lanes rv1_l18 and lp3_l115 through lp3_l118 used, batch `lp3`.

Awaiting the owner:

- **whether the float layer is worth a model re-emission.** If
  `encdec_backwards` genuinely lacks the float clauses, no state change
  reaches it and the Lean model has to be emitted again with them. That
  is a rebuild of the thing every walk depends on, so it is yours, and it
  is the first hypothesis in §4 that would cost real time to test.
