# log 298 — the Hub in miniature, and why the float layer cannot be gated yet

2026-09-17. Follows log 297. the owner asked for two things: the tasks from the
agreed leans, and

> a small demo. the reason is that it would be great to have some real
> indicators of it doing actual work. an oracle in a sense. but small. i dont
> want things to get too far into that realm yet.

So: a demonstration that builds nothing, and one measurement that came back
blocked with the blocker named.

## 1. `ask.py` — the Hub in miniature

`Research/oracle/hub/demo/ask.py`. One file. It BUILDS NOTHING: it reads
artifacts other tasks already wrote and answers one question with its
provenance attached, naming the file every line came from.

```
python3 ask.py --operator + --lhs int32_t --rhs int64_t --from c --to go
```

| step | answer | from |
|---|---|---|
| does go accept it? | **NO** — `invalid operation: a + b (mismatched types int32 and int64)` | `attest_rv.json` |
| what does c lower it to? | `c/op_103` — `c.add a0, a1 ; c.jr ra` | `attest_rv.json` |
| the emulation, in go | `Au_240_c_add_i32_i64`, four lines | `arch_units/go/` |
| is it PROVED? | **PROVED**, the psABI `abi` statement | `gate_classes/gate.json` |
| what does that proof cover? | 4 arch-units, across c and cpp | `equivalence_classes.json` |

That is the line's whole claim in one answer: **an operator go refuses, handed
back as working go source, with a machine-checked certificate that it computes
what c's operator computes.**

### 1.1 A bug it had, found by asking an unflattering question

The first version answered "rust REFUSES `int64 + int64`", which is false.
It had matched any `BUILDFAIL` of that operator in the target, and rust
refuses `+` on MISMATCHED operands while accepting it on matched ones. The
question is about *these operands*, so the probe has to agree on the operand
SHAPES — the same notion the equivalence classes key on, because type
spellings differ per language and shapes do not. Fixed; rust now answers

```
yes -- rust lowers it itself, e.g. rust/op_541
its own arch-opcodes   c.add a0, a1 ; c.jr ra
```

— the same body c produces, which is exactly why they share a class.

It is also honest where there is nothing to claim: a float unit answers
"its class has not been put to Lean", because §2 is why.

## 2. The float layer: blocked, and the blocker named

144 classes, 329 arch-units, never gated. Lane l111 put them and got nothing,
for two separate reasons, neither mathematical.

**The emulation side: 0 of 142 compiled.** `arch_units.h` includes
`sfemul.h`, which lives in `emul_rm0/c`, and the lane carried only
`-I arch_units/c`. Adding the second include compiles it — verified by hand.

**The arch side: 142 of 142 walks refused**, every one with "no certified pure
form for ILLEGAL". Lane l114 decoded three real words, assembled rather than
typed, on the walker's own state through the walker's own `eval_file`:

| word | decodes to |
|---|---|
| `feq.s a0, fa0, fa5` | `instruction.ILLEGAL` |
| `fadd.d fa0, fa0, fa1` | `instruction.ILLEGAL` |
| `add a0, a0, a1` | `instruction.C_ADD (…)` |

The integer word decodes and both float words do not. **The decoder is gating
on the machine state.** What is NOT the problem, checked rather than assumed:
the Lean model HAS the float instructions — `FextInsts.lean`,
`DextInsts.lean`, and `f_bin_op_x_S` with `FEQ_S`, `FLT_S`, `FLE_S` in
`Defs.lean`. The model does not need re-emitting; the state the walk decodes
on needs misa's F and D bits.

## 3. Three lanes lost to writing beside the machinery

Worth recording as a pattern, because it cost four lanes this session and
every failure looked like a real result until it was read:

| lane | what was written by hand | what it looked like |
|---|---|---|
| l106 | the Lean file's header | eight lemmas "failing" — actually out of scope |
| l108 | the simp set | the bridge "not working" — actually unfold-before-rewrite |
| l112 | the machine state | "no output" — actually a non-elaborating file |
| l113 | the executable library's name | a traceback |

In every case the walker or `equals` already had the thing. l112 and l113 are
the same lane twice, and l114 is it a third time with the name read out of the
lakefile instead of assumed.

A smaller one in the same family: l114's own reading line tested for the
string `Illegal` against output that says `ILLEGAL`, so it printed the wrong
conclusion above correct data. The data is in §2 and the conclusion there is
read off the table, not off that line.

## 4. Two lists

Decided, recorded for audit:

- `hub/demo/ask.py` written and corrected; it builds nothing and names its
  sources per line;
- the float compile fix is known and verified but NOT yet applied to a lane,
  because §2's second reason makes it moot until the state is settled;
- lanes lp3_l111 through lp3_l114 used, batch `lp3`.

Awaiting the owner:

- **the walker's machine state.** Enabling F and D in misa is what unblocks
  329 arch-units. It also changes the state every walk decodes on, which is
  every result the walker has produced. That is structural and I am not
  changing it without your word.
