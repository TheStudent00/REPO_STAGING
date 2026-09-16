# log 273 — rv9: the arch-opcode axis on RISC-V, under the owner's rule of 2026-09-13; the multiply-high cause named from the objects, the bit-blast route at three optimization settings, and rv4's regression named at last

Node: `hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_1_arch_opcode_axis/PROGRESS.md`).

Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_rv9_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
It follows rv6 (`PRIVATE/PseudoCoupHQ/DevComms/log_265_rv6_every_riscv_arch_opcode_four_languages.md`),
bb1 (`PRIVATE/PseudoCoupHQ/DevComms/log_267_bb1_the_bit_blast_route_on_riscv.md`),
rd1 (`PRIVATE/PseudoCoupHQ/DevComms/log_268_rd1_the_guard_dominates_the_operation.md`)
and rv4 (`PRIVATE/PseudoCoupHQ/DevComms/log_263_rv4_the_timed_riscv_round_optimization_off.md`).

Date: 2026-09-13. Instance `rv9`
(`PUBLIC/Airlock/instances/rv9.conf`). Every lane ran on the
tower guest through `bash $HOME/Programming/PUBLIC/Airlock/remote_lane.sh`;
nothing but file editing and git ran on the laptop. A lane log's host path on
the tower is
`<runs>/rv9/agent/logs/<stamp>__<lane>.sh.log`, and
every attribution below names its file. Paths inside a pasted command are the
ones the lane sees: `PseudoCoupHQ` IS
`PRIVATE/PseudoCoupHQ`. Every rendering is labelled **LITERAL**
(the object, quoted) or **GLOSS** (a plain-words reading beside a literal).

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

## 0. In plain words, before any table

Four boxes of the RISC-V table have never had a proof on any language by
any route. This task was told to find out WHY, without being allowed to
know what those four boxes are. So nothing here was written for them:
the population was chosen by reading verdicts out of stores this task did
not write — "every box no store records a proof for" — and the same four
questions were then asked of every member of it.

The answer is short. The compiler does not call a library routine; on c,
c++ and rust the compiled body refers to no symbol outside itself at all.
The body and the definition are both correct — evaluated at two hundred
input points, edge values first, they agree at every one. What they are
not is the SAME TEXT: the compiler replaced the doubled-width product
with the architecture's own high-half instruction plus a correction sum,
so the body's formula has a sum at its root where the definition's has an
extract, and the canonical form (order the commutative arguments,
simplify, rename, simplify again) does not bridge that. The prover is
then asked an identity about a sixty-four-bit multiplier, and it does not
answer: not in three seconds, not in thirty, not through its own
bit-blast tactic in thirty, and not when the question is narrowed to the
low eight, sixteen or thirty-two bits. On go there is no doubled-width
holder at all, so the render constructs the product and the body comes
out at fourteen to nineteen thousand instructions, which is above the
four thousand the gate is offered, and it was never posed.

The second half of the task was the other route: compile z3's own circuit
with less rewriting, so the check compares like with like. Measured at
three settings over every box the blast route had left open, that idea is
WRONG, and the measurement says why in one line: with optimization off
the bodies get two to four times BIGGER, not smaller, because every gate
now travels through the stack. Proofs fall from 137 to 117 of 480
attempts, and refusals rise from 208 to 239. One box moved the other way
and it is recorded below.

The third thing was rv4's old regression — optimization off made the
check worse and the cause was never named. It is named now, and it is one
sentence with a body under it: with optimization off the compiler frames
its locals on the stack, which makes it emit one instruction the lifter
has no entry for, `c.addi4spn`; that alone refuses the walk on 83 of the
120 boxes that lost their proof, and every one of the 120 without
exception gained instructions that name a memory address. One box's body
is two instructions at ship flags and twenty-six at optimization off, and
both are pasted.

---

## 1. What the objects are, one sentence each, in relation

- **A cell** is one `arch_opcode` as a row of the model table — a
  (mnemonic, operand form, width) triple — and the RISC-V table holds 255
  of them, which is the denominator of every table below.
- **The native route** is the cell's term printed in the target
  language's own operators, compiled, carved and gated.
- **The bit-blast route** is the same cell's term turned into an
  and-or-not-xor circuit by z3's own tactic, that circuit written as one
  named local per gate, compiled, carved and gated.
- **A setting** is one rule about the COMPILE FLAGS, applied to all four
  languages at once, and never about a cell: `ship` is each route's own
  line untouched, `one` moves every optimization-level flag to level 1
  and turns go's inlining off, `off` moves every optimization-level flag
  to level 0 and turns go's local optimizations and inlining off.
- **The canonical form** is `term.Term.normalize`'s rule: order the
  arguments of every commutative node, simplify, order again, rename the
  free symbols positionally, simplify and order once more, print on one
  line.
- **A reference out of the unit** is an instruction of the carved body
  whose operand text carries a `<symbol>` annotation naming a symbol that
  is not the unit's own; it is how a call to a library routine looks in
  the carved text, and it is read without consulting any mnemonic.
- **The population**, in both halves of this task, is a reading of
  VERDICTS in stores this task did not write, never a reading of names.

---

## 2. How the population was chosen, so that no name was ever read

`rv9_native.py`'s own filter, **LITERAL** (lane `rv9_l4` step [2/3], the
run's step [1/5]):

```
[1/5] the population: every (cell, place) no store records a proof for
   4 of 255 (cell, place) keys the stores hold carry no proof on any
   language by any route
     mulh gpr_gpr_gpr 64, place reg_a0
     mulh gpr_gpr_same 64, place reg_a0
     mulhsu gpr_gpr_gpr 64, place reg_a0
     mulhsu gpr_gpr_same 64, place reg_a0
```

**GLOSS.** The three stores read are `rd1_all.jsonl` (the native route and
the backstop under the guarded render), `rv6_all.jsonl` (the same two
before it) and `bb1_all.jsonl` (the bit-blast route). A key is in the
population when NO row of any of them carries `kind == "proved"`, on any
of the four languages, under any policy. The four names printed are the
OUTPUT of that filter and were never its input; the same program run
against a table with different boxes open would print those instead.

Section 2's population is the same kind of reading, one step wider
(lane `rv9_l5` step [2/3]), **LITERAL**:

```
   the blast route left 120 of 255 (cell, place) keys unproved on at
   least one language
   4 keys carry no proof in any store, by any route
   the population is their union: 120 keys
```

---

## 3. Section 1 — the native route on the four, cause named

Lane `rv9_l4_the_native_route_with_the_width_sweep_and_the_points.sh`,
tower log
`<runs>/rv9/agent/logs/20260913T172731Z__rv9_l4_the_native_route_with_the_width_sweep_and_the_points.sh.log`,
`state=done exit=0` in 969.2 s, peak resident 474,016 kB, memory bound
6,291,456 kB with the named abort `ABORT_MEMORY_RV9`. Store
`construct/general/rv9_native.jsonl`; sources
`construct/general/src_rv9_native/`. The lifter it read, by sha256:
`325e96a25cca475c8b0b150e4beca72a7a08682618844f38fae43625e955349e`
(`Research/oracle/riscv/riscv_reference.py`, unchanged by this task —
task sl1 owns that file).

### 3.1 The measurement, all sixteen (cell, language) pairs

**LITERAL**, lane `rv9_l4`, the run's step [3/5]:

| mnem | shape | width | language | statements | source lines | body | refs out | memory operands | outcome | identical after normalize | check s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `mulh` | `gpr_gpr_gpr` | 64 | c | 6 | 17 | 274 | 0 | 48 | UNDECIDED | False | 3.037 |
| `mulh` | `gpr_gpr_gpr` | 64 | cpp | 6 | 18 | 274 | 0 | 48 | UNDECIDED | False | 3.513 |
| `mulh` | `gpr_gpr_gpr` | 64 | go | 13567 | 13593 | 18836 | 1 | 3272 | NOT_GATED | None | None |
| `mulh` | `gpr_gpr_gpr` | 64 | rust | 6 | 18 | 274 | 0 | 48 | UNDECIDED | False | 3.043 |
| `mulh` | `gpr_gpr_same` | 64 | c | 4 | 15 | 126 | 0 | 10 | UNDECIDED | False | 3.034 |
| `mulh` | `gpr_gpr_same` | 64 | cpp | 4 | 16 | 126 | 0 | 10 | UNDECIDED | False | 3.039 |
| `mulh` | `gpr_gpr_same` | 64 | go | 13501 | 13526 | 18876 | 1 | 3389 | NOT_GATED | None | None |
| `mulh` | `gpr_gpr_same` | 64 | rust | 4 | 16 | 126 | 0 | 10 | UNDECIDED | False | 3.518 |
| `mulhsu` | `gpr_gpr_gpr` | 64 | c | 5 | 16 | 125 | 0 | 10 | UNDECIDED | False | 3.04 |
| `mulhsu` | `gpr_gpr_gpr` | 64 | cpp | 5 | 17 | 125 | 0 | 10 | UNDECIDED | False | 3.039 |
| `mulhsu` | `gpr_gpr_gpr` | 64 | go | 13503 | 13529 | 14531 | 1 | 2864 | NOT_GATED | None | None |
| `mulhsu` | `gpr_gpr_gpr` | 64 | rust | 5 | 17 | 125 | 0 | 10 | UNDECIDED | False | 3.524 |
| `mulhsu` | `gpr_gpr_same` | 64 | c | 5 | 16 | 125 | 0 | 10 | UNDECIDED | False | 3.028 |
| `mulhsu` | `gpr_gpr_same` | 64 | cpp | 5 | 17 | 125 | 0 | 10 | UNDECIDED | False | 3.312 |
| `mulhsu` | `gpr_gpr_same` | 64 | go | 13502 | 13527 | 14831 | 1 | 2984 | NOT_GATED | None | None |
| `mulhsu` | `gpr_gpr_same` | 64 | rust | 5 | 17 | 125 | 0 | 10 | UNDECIDED | False | 3.313 |

Census over the sixteen: `undecided 12`, `refused 4` (the four go rows,
every one of them `NOT_GATED` with its size on the row).

### 3.2 Does the body call a library routine? On c, c++ and rust, no

The brief's second question, and the answer is a count, not an opinion.
**LITERAL**, lane `rv9_l4`, "EVERY REFERENCE A BODY MAKES TO A SYMBOL
OUTSIDE ITSELF" — the whole table, four rows:

| mnem | shape | width | language | symbol | the instruction, LITERAL |
|---|---|---|---|---|---|
| `mulh` | `gpr_gpr_gpr` | 64 | go | `runtime.morestack_noctxt.abi0` | `jal t0, 0x6a790 <runtime.morestack_noctxt.abi0>` |
| `mulh` | `gpr_gpr_same` | 64 | go | `runtime.morestack_noctxt.abi0` | `jal t0, 0x6a790 <runtime.morestack_noctxt.abi0>` |
| `mulhsu` | `gpr_gpr_gpr` | 64 | go | `runtime.morestack_noctxt.abi0` | `jal t0, 0x6a790 <runtime.morestack_noctxt.abi0>` |
| `mulhsu` | `gpr_gpr_same` | 64 | go | `runtime.morestack_noctxt.abi0` | `jal t0, 0x6a790 <runtime.morestack_noctxt.abi0>` |

**GLOSS.** c, c++ and rust refer to NOTHING outside the unit — the count
is 0 on every one of their twelve rows, so the standing rule about
attaching a callee's body from the toolchain archive has nothing to fire
on. go's one reference per body is its own stack-growth entry, which
computes no value of the emulation; and go's bodies are above the
instruction ceiling anyway, so they were never posed and the attach rule
never came up. The library-routine hypothesis is closed: it is not that.

### 3.3 The two formulas, and the exact node at which they part

The whole of one rendered source, **LITERAL** (lane `rv9_l4`, the
`mulhsu gpr_gpr_gpr 64` c section; the two long lines are cut where the
lane's own printer cut them, and the count of characters not shown is the
printer's):

```
uint64_t
emu_mulhsu_gpr_gpr_gpr_64__reg_a0__c__native_first(uint64_t a, uin
t64_t b)
{
    unsigned __int128 v0 = (unsigned __int128)(((unsigned __int128
)(UINT64_C(0x0)) << 64) | (unsigned __int128)((uint64_t)b));
    uint32_t v1 = ((uint32_t)((uint64_t)a >> 63) & UINT32_C(0x1));
    unsigned __int128 v2 = (unsigned __int128)(((unsigned __int128
)(v1) << 127) | ((unsigned __int128)(v1) << 126) | ((unsigned __in
... 1889 characters of this line are not shown ...
 | ((unsigned __int128)(v1) << 65) | ((unsigned __int128)(v1) <<
 64) | (unsigned __int128)((uint64_t)a));
    unsigned __int128 v3 = (unsigned __int128)((unsigned __int128)
(v2) * (unsigned __int128)(v0));
    uint64_t v4 = (uint64_t)((unsigned __int128)(v3) >> 64);
    return (uint64_t)(v4);
}
```

The last five instructions of what the compiler made of it,
**LITERAL**, same section:

```
c.or a2, a3
c.mul a2, a1
mulhu a0, a0, a1
c.add a0, a2
c.jr ra
```

**GLOSS, values in motion.** The source asks for a 128-bit product of a
sign-widened `a` and a zero-widened `b`, then its top half. The compiler
does not build a 128-bit product: it computes the unsigned top half in
one instruction (`mulhu a0, a0, a1`), computes the correction the sign
widening contributes as a 64-bit product (`c.mul a2, a1`, where `a2` is
the replicated sign bit assembled by the sixty shift-and-or instructions
above it), and adds the two. That is the same number by an identity about
multiplication; it is not the same TEXT.

The two canonical texts, **LITERAL**, with their node counts as the lane
printed them:

```
the BODY's formula, canonical, 193 distinct nodes:
Concat(Extract(63, 57, Concat(0, Extract(63, 63, v0), 0)*184467440
73709551615 + Concat(0, Extract(63, 63, v0), 0)) | Extract(63, 57,
 Concat(0, Extract(63, 63, v0), 0)*18446744073709551615), Extract(
... 8473 characters of this line are not shown ...
cat(0, Extract(63, 63, v0), 0)*18446744073709551615) | Extract(63,
 63, v0), Extract(63, 63, v0))*v1 + Extract(127, 64, Concat(0, v0)
*Concat(0, v1))

the DEFINITION's formula, canonical, 8 distinct nodes:
Extract(127, 64, Concat(Extract(63, 63, v0), Extract(63, 63, v0),
... 990 characters of this line are not shown ...
 v0), Extract(63, 63, v0), Extract(63, 63, v0), v0)*Concat(0, v1))
```

`identical after normalize: False`, and the first node at which they
differ, **LITERAL**:

```
THE FIRST NODE AT WHICH THEY DIFFER
  path from the root: []
  what differs: the declaration kind
  the body's node:       + | sort BitVec(64)
  the definition's node: Extract | sort BitVec(64)
```

**GLOSS.** They differ at the ROOT. The body's answer is a sum; the
definition's is an extract. Nothing downstream is even compared, because
the walk stops at the first position where the two shapes part, and that
position is position zero. This is the same on all twelve rows: the same
path `[]`, the same two declaration kinds.

`canonical_agrees_with_normalize` is `{"body": true, "definition":
true}` on every row — this task computed the canonical form from the
functions `term.py` exports and checked its own text against
`Term.normalize`'s own return on the same term, so the two texts above
are that file's rule and not a second one.

### 3.4 It is not the budget, and it is not the width

The law's rule on a limit is that it is a FLAG: re-run with more room and
report whether the answer changed. It did not. **LITERAL**, lane
`rv9_l4`:

| mnem | shape | width | language | at 3,000 ms | at 30000 ms | seconds | through z3's own bit-blast tactic | seconds |
|---|---|---|---|---|---|---|---|---|
| `mulh` | `gpr_gpr_gpr` | 64 | c | UNDECIDED | UNDECIDED | 30.04 | UNDECIDED | 30.015 |
| `mulh` | `gpr_gpr_gpr` | 64 | cpp | UNDECIDED | UNDECIDED | 30.04 | UNDECIDED | 30.022 |
| `mulh` | `gpr_gpr_gpr` | 64 | rust | UNDECIDED | UNDECIDED | 30.524 | UNDECIDED | 30.026 |
| `mulh` | `gpr_gpr_same` | 64 | c | UNDECIDED | UNDECIDED | 30.036 | UNDECIDED | 30.016 |
| `mulh` | `gpr_gpr_same` | 64 | cpp | UNDECIDED | UNDECIDED | 30.043 | UNDECIDED | 30.014 |
| `mulh` | `gpr_gpr_same` | 64 | rust | UNDECIDED | UNDECIDED | 30.528 | UNDECIDED | 30.027 |
| `mulhsu` | `gpr_gpr_gpr` | 64 | c | UNDECIDED | UNDECIDED | 30.043 | UNDECIDED | 30.028 |
| `mulhsu` | `gpr_gpr_gpr` | 64 | cpp | UNDECIDED | UNDECIDED | 30.061 | UNDECIDED | 30.02 |
| `mulhsu` | `gpr_gpr_gpr` | 64 | rust | UNDECIDED | UNDECIDED | 30.524 | UNDECIDED | 30.032 |
| `mulhsu` | `gpr_gpr_same` | 64 | c | UNDECIDED | UNDECIDED | 30.032 | UNDECIDED | 30.022 |
| `mulhsu` | `gpr_gpr_same` | 64 | cpp | UNDECIDED | UNDECIDED | 30.033 | UNDECIDED | 30.015 |
| `mulhsu` | `gpr_gpr_same` | 64 | rust | UNDECIDED | UNDECIDED | 30.338 | UNDECIDED | 30.024 |

And the same equality narrowed to the low k bits, at the gate's own
budget — `inherit.at_width` is the gate's own narrowing and is called, so
this is the same question, truncated. **LITERAL**, the first three rows
of twelve; all twelve read the same:

| mnem | shape | width | language | 8 bits | 16 bits | 32 bits | 64 bits |
|---|---|---|---|---|---|---|---|
| `mulh` | `gpr_gpr_gpr` | 64 | c | UNDECIDED (3.019s) | UNDECIDED (3.02s) | UNDECIDED (3.026s) | UNDECIDED (3.037s) |
| `mulh` | `gpr_gpr_gpr` | 64 | cpp | UNDECIDED (3.128s) | UNDECIDED (3.02s) | UNDECIDED (3.026s) | UNDECIDED (3.516s) |
| `mulh` | `gpr_gpr_gpr` | 64 | rust | UNDECIDED (3.018s) | UNDECIDED (3.224s) | UNDECIDED (3.026s) | UNDECIDED (3.041s) |

**GLOSS.** Ten times the budget does not close it. z3's own bit-blast
tactic at that budget does not close it. Asking only about the low eight
bits does not close it — which is the answer to "is it the shape or the
size": narrowing the question does not help, because every bit of the
high half of a product depends on the whole multiplier either way.

### 3.5 The emulation is right; it is the proof that is missing

The two terms EVALUATED at two hundred input points, edge values first —
evidence, never a proof, which is the word this line already uses for the
interpreted route. **LITERAL**, the first three rows of twelve; all
twelve read `200 | 200 | none`:

| mnem | shape | width | language | points | agreed | first point at which they differ |
|---|---|---|---|---|---|---|
| `mulh` | `gpr_gpr_gpr` | 64 | c | 200 | 200 | none |
| `mulh` | `gpr_gpr_gpr` | 64 | cpp | 200 | 200 | none |
| `mulh` | `gpr_gpr_gpr` | 64 | rust | 200 | 200 | none |

**GLOSS.** The compiled body and the cell's definition answer the same at
every sampled point, edges included. Nothing suggests the emulation is
wrong; what is missing is a proof.

### 3.6 The cause, in one paragraph, and what would close it

**Named cause.** On c, c++ and rust the native route produces a correct
emulation whose CARVED body the compiler has rewritten from a
doubled-width product into the architecture's own high-half instruction
plus a correction sum. The lifted formula therefore carries a sum at its
root where the definition carries an extract, the canonical form does not
rewrite one into the other (it orders and simplifies; it knows no
identity about multiplication), and the resulting equality is a
sixty-four-bit multiplier identity that z3 does not decide at 3,000 ms, at
30,000 ms, through its own bit-blast tactic, or narrowed to any width
offered. On go there is no doubled-width holder, the render constructs
the product from primitives, and the body lands at 14,531 to 18,876
instructions — above the 4,000 the gate is offered, so it is NOT_GATED
with its size and nothing is proved or disproved.

**What would close it, and why this task did not write it.** The brief
allows a GENERIC normalization rule and forbids one that names the cell.
The rule that would close this gap is an ALGEBRAIC identity about the
high half of a width-doubled product, general in width — which is exactly
the lemma `construct/lean/OWED.md` §2 already owes and which t4 recorded
as owed (log_262: "OWED: Lean lemma general in width; algebraic lemma for
mul/div"). It is not a rewriting of shapes: `Term.normalize` is
`z3.simplify` plus a commutative ordering, and no ordering turns a sum
into an extract. Writing it would mean changing
`Research/op_pipeline/term.py`, a shared file this brief did not name and
the launch note forbids touching. That line is stopped here and appears
under "flag for the coordinator" in §7.

---

## 4. Section 2 — the bit-blast route at three optimization settings

Lanes `rv9_l5_the_whole_population_at_setting_ship.sh`,
`rv9_l6_the_whole_population_at_setting_one.sh` and
`rv9_l7_the_whole_population_at_setting_off.sh`; tower logs
`<runs>/rv9/agent/logs/20260913T174342Z__rv9_l5_the_whole_population_at_setting_ship.sh.log`,
`.../20260913T182132Z__rv9_l6_the_whole_population_at_setting_one.sh.log`
and
`.../20260913T190119Z__rv9_l7_the_whole_population_at_setting_off.sh.log`;
all three `state=done exit=0`, in 2,269.3 s, 2,387.2 s and 598.6 s, peak
resident 230,328 kB, 233,760 kB and 360,192 kB, each under the stated
6,291,456 kB bound with the named abort `ABORT_MEMORY_RV9`. Stores
`construct/general/rv9_set_ship.jsonl`, `rv9_set_one.jsonl`,
`rv9_set_off.jsonl`. 120 keys × 4 languages = 480 attempts per setting.

### 4.1 The three flag lines, LITERAL

Each lane printed its own setting before it ran. **LITERAL**, lanes
`rv9_l5`, `rv9_l6` and `rv9_l7`, step [0/2] of each:

```
the setting: ship
c    : clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchai
n=/usr
cpp  : /usr/bin/clang++ -std=c++20 -O1 --target=riscv64-linux-gnu -
-gcc-toolchain=/usr
rust : rustc --crate-type=lib --emit=obj -C opt-level=1 -C debug-as
sertions=off --target=riscv64gc-unknown-linux-gnu
go   : GOARCH=riscv64 GOOS=linux go build -o <obj> .

the setting: one
c    : clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchai
n=/usr
cpp  : /usr/bin/clang++ -std=c++20 -O1 --target=riscv64-linux-gnu -
-gcc-toolchain=/usr
rust : rustc --crate-type=lib --emit=obj -C opt-level=1 -C debug-as
sertions=off --target=riscv64gc-unknown-linux-gnu
go   : GOARCH=riscv64 GOOS=linux go build -gcflags=all=-l -o <obj> .

the setting: off
c    : clang -std=c17 -O0 --target=riscv64-linux-gnu --gcc-toolchai
n=/usr
cpp  : /usr/bin/clang++ -std=c++20 -O0 --target=riscv64-linux-gnu -
-gcc-toolchain=/usr
rust : rustc --crate-type=lib --emit=obj -C opt-level=0 -C debug-as
sertions=off --target=riscv64gc-unknown-linux-gnu
go   : GOARCH=riscv64 GOOS=linux go build -gcflags=all=-N -l -o <obj> .
```

**GLOSS.** `ship` and `one` differ on go alone, because the other three
routes already ship at level 1. Both were run anyway and neither was
assumed, and that identity is itself a check on the table: every c, c++
and rust number below is the same in the two columns, and so is every
body size.

### 4.2 The outcome, setting by setting

**LITERAL**, lane `rv9_l9`, step [3/5]:

| setting | language | attempts | proved | disproved | undecided | refused | of |
|---|---|---|---|---|---|---|---|
| ship | c | 120 | 1 | 0 | 67 | 52 | 255 |
| ship | c++ | 120 | 1 | 0 | 67 | 52 | 255 |
| ship | rust | 120 | 67 | 1 | 0 | 52 | 255 |
| ship | go | 120 | 68 | 0 | 0 | 52 | 255 |
| one | c | 120 | 1 | 0 | 67 | 52 | 255 |
| one | c++ | 120 | 1 | 0 | 67 | 52 | 255 |
| one | rust | 120 | 67 | 1 | 0 | 52 | 255 |
| one | go | 120 | 68 | 0 | 0 | 52 | 255 |
| off | c | 120 | 0 | 0 | 60 | 60 | 255 |
| off | c++ | 120 | 0 | 0 | 60 | 60 | 255 |
| off | rust | 120 | 58 | 4 | 0 | 58 | 255 |
| off | go | 120 | 59 | 0 | 0 | 61 | 255 |

Totals over the 480 attempts of each setting, **LITERAL**, the three
lanes' own censuses: ship `proved 137, refused 208, sat 1, undecided
134`; one `proved 137, refused 208, sat 1, undecided 134`; off `proved
117, refused 239, sat 4, undecided 120`.

### 4.3 Why: the bodies get BIGGER, not smaller

**LITERAL**, lane `rv9_l9`:

| language | setting | bodies carved | smallest | median | mean | largest |
|---|---|---|---|---|---|---|
| c | ship | 92 | 89 | 755 | 23521.239 | 250188 |
| c | one | 92 | 89 | 755 | 23521.239 | 250188 |
| c | off | 92 | 417 | 2940 | 75271.587 | 564866 |
| c++ | ship | 92 | 89 | 755 | 23521.239 | 250188 |
| c++ | one | 92 | 89 | 755 | 23521.239 | 250188 |
| c++ | off | 92 | 417 | 2940 | 75271.587 | 564866 |
| rust | ship | 94 | 88 | 815 | 25003.755 | 247289 |
| rust | one | 94 | 88 | 815 | 25003.755 | 247289 |
| rust | off | 94 | 149 | 1152 | 47820.362 | 311689 |
| go | ship | 90 | 245 | 1104 | 22964.044 | 209870 |
| go | one | 90 | 245 | 1104 | 22964.044 | 209870 |
| go | off | 92 | 377 | 3976 | 70796.543 | 503430 |

**GLOSS.** The brief's idea was that less rewriting would let the carved
body follow z3's circuit gate by gate, so the check would compare like
with like. It does the opposite. With optimization off the median c body
goes from 755 to 2,940 instructions and the largest from 250,188 to
564,866, because every gate's value now travels to the stack and back;
more bodies cross the 4,000-instruction ceiling and are NOT_GATED, which
is why `refused` rises from 52 to 60 on c and from 52 to 61 on go.

### 4.4 Four attempts in full, as the brief asks them to be recorded

Compiled / carved / lifted / verdict / seconds / body instructions, per
(cell, language, setting). The whole table is 1,440 rows in lane
`rv9_l9`'s log and in the three stores; **LITERAL**, two keys of it:

| mnem | shape | width | place | language | setting | compiled | carved instructions | lifted | verdict | compile s | check s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | c | ship | True | 257 | yes | PROVED | 0.107 | 0.051 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | c | one | True | 257 | yes | PROVED | 0.111 | 0.055 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | c | off | True | 1426 | no | WALK_REFUSED | 0.09 | 0.001 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | go | ship | True | 955 | yes | PROVED | 0.197 | 0.136 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | go | off | True | 2261 | yes | PROVED | 0.2 | 0.095 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | rust | ship | True | 256 | yes | DISPROVED | 0.115 | 0.059 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | rust | one | True | 256 | yes | DISPROVED | 0.119 | 0.051 |
| `czero.eqz` | `gpr_gpr_gpr` | 64 | reg_a0 | rust | off | True | 600 | yes | PROVED | 0.105 | 0.122 |
| `divw` | `gpr_gpr_gpr` | 32 | reg_a0 | c | ship | True | 20488 | no | NOT_GATED | 2.617 | None |
| `divw` | `gpr_gpr_gpr` | 32 | reg_a0 | c | off | True | 108196 | no | NOT_GATED | 1.193 | None |
| `divw` | `gpr_gpr_gpr` | 32 | reg_a0 | go | ship | True | 33129 | no | NOT_GATED | 56.748 | None |
| `divw` | `gpr_gpr_gpr` | 32 | reg_a0 | go | off | True | 107172 | no | NOT_GATED | 1.249 | None |
| `divw` | `gpr_gpr_gpr` | 32 | reg_a0 | rust | ship | True | 20484 | no | NOT_GATED | 2.277 | None |
| `divw` | `gpr_gpr_gpr` | 32 | reg_a0 | rust | off | True | 59444 | no | NOT_GATED | 1.599 | None |

### 4.5 The ONE place where the brief's idea held

Reading the stores for what optimization off proves that ship flags did
not, **LITERAL** (`python3` over the three stores and `bb1_all.jsonl`,
run on the laptop over the synced files):

```
$ python3 -c "
import json
G='Research/oracle/cross_construction/emulation/construct/'
G=G+'general/'
def proved(path,target):
    out=set()
    for l in open(path):
        r=json.loads(l)
        if r['target']!=target: continue
        for a in r.get('attempts') or []:
            if (a.get('verdict') or {}).get('outcome')=='PROVED':
                c=r['cell']
                out.add((c['mnem'],c['shape'],c['key_width']))
    return out
bb=proved(G+'bb1_all.jsonl','rust')
for s in ('ship','one','off'):
    print(s, sorted(proved(G+'rv9_set_%s.jsonl'%s,'rust')-bb))"
ship []
one []
off [('czero.eqz', 'gpr_gpr_gpr', 64)]
```

That key's three rows are in §4.4: on rust the blast route is DISPROVED
at ship and at `one` with 256 carved instructions, and PROVED at
optimization off with 600. **GLOSS.** This is exactly the effect the
brief predicted — with less rewriting the body's meaning as the walk
reads it matches the circuit — and it happened once in 120 keys, against
20 proofs lost elsewhere.

### 4.6 What the four disproofs at optimization off are

**LITERAL**, the counterexamples of every `sat` row of the three stores
(cut at 160 characters by the reader):

```
ship czero.eqz gpr_gpr_gpr 64 reg_a0 rust
  {"seed_x11": "18446744073709551615",
   "seed_x12": "9223372036854775808"}
one  czero.eqz gpr_gpr_gpr 64 reg_a0 rust
  {"seed_x11": "18446744073709551615",
   "seed_x12": "9223372036854775808"}
off  sub gpr_gpr_gpr 64 reg_a0 rust
  {"seed_MEM__0x100_a1_": "0", "seed_MEM__0x108_a1_": "0", ...}
off  add gpr_gpr_gpr 64 reg_a0 rust
  {"seed_MEM__0x4e0_a1_": "0", "seed_MEM__0x4e8_a1_": "0", ...}
off  beq gpr_gpr_gpr 64 branch_condition rust
  {"seed_MEM__0x800_a0_": "1", "seed_x10": "0", "seed_x11": "23058...}
off  beq gpr_gpr_same 64 branch_condition rust
  {"seed_MEM__0x7f0_a0_": "18446743936237043712", ...}
```

**GLOSS.** Every disproof introduced by optimization off names memory
seeds in its counterexample — `seed_MEM__<offset>_<register>_` is the
walk's parameter for a memory location it must read without knowing what
was put there. That is the same stack traffic §4.3 measured, now visible
in the counterexample itself.

### 4.7 Every outcome that is not a proof, by cause

**LITERAL**, lane `rv9_l9`, the top of its cause table (causes cut at 120
characters by the reader):

| setting | language | outcome | cause | attempts |
|---|---|---|---|---|
| off | go | NOT_GATED | the carved body is larger than the number of instructions this task's gate is offered | 33 |
| off | c | NOT_GATED | the same | 32 |
| off | c++ | NOT_GATED | the same | 32 |
| off | rust | NOT_GATED | the same | 32 |
| off | c | the blast refused | the bit-blast route is a circuit over BITS and this term is not a bit-vector term over bit-vector arrivals | 26 |
| ship | c | the blast refused | the same | 26 |
| ship | rust | NOT_GATED | the same as the first row | 26 |
| ship | c | NOT_GATED | the same as the first row | 24 |
| ship | go | NOT_GATED | the same as the first row | 22 |
| off | c | WALK_REFUSED | `NotModeled: no entry in the riscv opcode table for 'c.addi4spn' (line 'c.addi4spn s0, sp, 0x1f0')` | 20 |
| off | c | WALK_REFUSED | `NotModeled: no entry in the riscv opcode table for 'bexti' (line 'bexti a1, a1, 0x1')` | 18 |
| ship | c | WALK_REFUSED | `NotModeled: no entry in the riscv opcode table for 'bexti' (line 'bexti a4, a0, 0x2')` | 16 |
| off | c | WALK_REFUSED | `NotModeled: no entry in the riscv opcode table for 'sh3add' (line 'sh3add a3, a3, s0')` | 13 |
| ship | c | WALK_REFUSED | `NotModeled: no entry in the riscv opcode table for 'c.not' (line 'c.not a1')` | 6 |
| ship | c | WALK_REFUSED | `NotModeled: no entry in the riscv opcode table for 'orn' (line 'orn a2, ra, t6')` | 5 |

**GLOSS.** The 26 blast refusals per language are the float places, where
a circuit over bits has no node to blast — unchanged from bb1. The
NOT_GATED rows are the size ceiling. The WALK_REFUSED rows are the
lifter's missing entries, and optimization off adds two more names to the
list bb1 already owed (`bexti`, `orn`, `c.not`): `c.addi4spn` and
`sh3add`. c++ reads identically to c on every row.

---

## 5. Why optimization off makes the check worse — rv4's cause, named

Lane `rv9_l8_the_optimization_off_regression_by_cause.sh`, tower log
`<runs>/rv9/agent/logs/20260913T191119Z__rv9_l8_the_optimization_off_regression_by_cause.sh.log`,
`state=done exit=0` in 273.7 s, peak resident 374,088 kB. The population
is rv4's own — the loop's untwinned cells on c and go, 188 runs — and
the same render, lifter and gate are used at both settings, so the two
columns are one measurement. Store `construct/general/rv9_offcause.jsonl`.

### 5.1 The census at both settings

**LITERAL**, lane `rv9_l8` step [3/5]:

| setting | proved | disproved | undecided | refused | runs |
|---|---|---|---|---|---|
| ship | 166 | 6 | 8 | 8 | 188 |
| off | 46 | 39 | 95 | 8 | 188 |

**GLOSS.** rv4 (log_263) measured 144 proved and 36 proved on the same
188 runs; this lane measures 166 and 46, higher on both sides, because it
runs rv3's compile routes and the guarded render of rd1, which rv4 did
not have. The SHAPE is the same and it is the shape that is the subject:
optimization off costs about three quarters of the proofs.

### 5.2 The transitions

**LITERAL**, lane `rv9_l8` step [4/5]:

| at ship flags | with optimization off | keys |
|---|---|---|
| proved | undecided | 84 |
| proved | proved | 46 |
| proved | sat | 36 |
| refused | refused | 8 |
| undecided | undecided | 7 |
| sat | undecided | 4 |
| sat | sat | 2 |
| undecided | sat | 1 |

### 5.3 The three candidate causes, counted over the 120 keys that lost a proof

The brief names three candidates — stack traffic, an instruction the
lifter lacks, the walk order — and this lane reads each of them off the
carved body: an instruction naming a memory address is one whose operand
text holds the architecture's own `offset(register)` form; a branch
inside the unit is one whose `<label>` resolves to this unit's own
symbol; the walk's refusal is the lifter's own message. **LITERAL**:

| the walk refused | more instructions naming memory | more branches inside the unit | keys |
|---|---|---|---|
| True | True | False | 46 |
| True | True | True | 37 |
| False | True | True | 35 |
| False | True | False | 2 |

**GLOSS, read as a cause.** Of the 120 keys that had a proof and lost it:
ALL 120 gained instructions that name a memory address — no exception, so
stack traffic is the one property that is necessary. 83 of 120 had their
WALK refused outright. Only 72 of 120 gained a branch inside the unit,
and 48 lost their proof without gaining one, so the walk order is NOT
necessary and cannot be the cause on its own.

### 5.4 The instruction the lifter lacks, LITERAL, with its count

**LITERAL**, lane `rv9_l8`, the distinct walk refusals over those 83
keys, summed by the name the lifter printed (the lane prints one row per
distinct message; the messages differ only in the stack offset):

| the refusal, LITERAL | keys |
|---|---|
| `NotModeled: no entry in the riscv opcode table for 'c.addi4spn' (line 'c.addi4spn s0, sp, <offset>)'` — 21 distinct offsets | 82 |
| `NotModeled: no entry in the riscv opcode table for 'c.not' (line 'c.not a0')` | 1 |

**GLOSS.** 82 of the 83 refusals are ONE missing entry, and it is the
compressed instruction that forms the address of a stack frame. It
appears only when the compiler frames its locals on the stack — which is
what optimization off makes it do everywhere.

### 5.5 One body, both settings, LITERAL

The lane chooses the key whose carved body grew most, which is a
machine-form rule and not a pick. **LITERAL**, lane `rv9_l8` step [4/5]:

```
mulhu gpr_gpr_same 64, place reg_a0, c: 46317 instructions more with
optimization off

--- setting ship, policy native_first, 2 instructions
    verdict: {"compared_on_bits": 64, "counterexample": null,
              "outcome": "PROVED", "solver_timeout_ms": 3000}
mulhu a0, a0, a0
c.jr ra

--- setting off, policy native_first, 26 instructions
    verdict: {"outcome": "WALK_REFUSED", "reason": "NotModeled: no
              entry in the riscv opcode table for 'c.addi4spn'
              (line 'c.addi4spn s0, sp, 0x50')"}
c.addi16sp sp, -0x50
c.sdsp ra, 0x48(sp)
c.sdsp s0, 0x40(sp)
c.addi4spn s0, sp, 0x50
sd a0, -0x18(s0)
ld a0, -0x18(s0)
c.li a1, 0x0
sd a1, -0x28(s0)
sd a0, -0x30(s0)
```

**GLOSS.** At ship flags the whole emulation is the one instruction the
cell names and a return, and the gate proves it in a few milliseconds.
With optimization off the same source becomes twenty-six instructions
that write the argument to the stack and read it back before anything is
computed, and the fourth of them is the one the lifter has no entry for,
so the walk stops there and the cell is lost. rv4's written cause ("no
memory model") was retracted in log_263 and the retraction was right: the
lifter DOES model loads and stores on named cells. What it lacks is the
entry for the stack-address instruction that only appears once
optimization is off.

---

## 6. Section 3 — the union of every route, of 255

Lane `rv9_l9_the_union_of_every_route_and_the_three_settings.sh`, tower
log
`<runs>/rv9/agent/logs/20260913T191701Z__rv9_l9_the_union_of_every_route_and_the_three_settings.sh.log`,
`state=done exit=0` in 1.6 s. Both tables below are computed from the
stores by the SAME reader in the same run, which is what lets them be set
against each other.

### 6.1 Before this task

**LITERAL**, reading `rd1_all.jsonl` and `bb1_all.jsonl`:

| language | all_constructed | bit_blast | native_first | any route | of |
|---|---|---|---|---|---|
| c | 143 | 136 | 241 | 243 | 255 |
| c++ | 143 | 136 | 241 | 243 | 255 |
| rust | 196 | 202 | 246 | 247 | 255 |
| go | 183 | 203 | 240 | 243 | 255 |
| **proved on at least one language** | **199** | **203** | **251** | **251** | **255** |
| **proved on all four languages** | | | | **235** | **255** |

**GLOSS.** Set against log_267's own table, every number agrees except
go's, and go's difference is accounted for: log_267 read `rv6_all.jsonl`
and this reader reads `rd1_all.jsonl`, which holds the two go proofs
(`div` and `rem` at `gpr_gpr_gpr` 64) that rd1's guarded render added and
log_268 recorded. So log_267 prints go native 238 and any-route 241 where
this prints 240 and 243; the backstop column (143 / 143 / 196 / 183) and
the bit-blast column (136 / 136 / 202 / 203) are log_267's numbers
exactly, and so are c, c++ and rust on every route. That agreement is the
check that this reader reads what the earlier logs read.

### 6.2 After this task

**LITERAL**, the same reader over the same two stores plus this task's
four (`rv9_native`, `rv9_set_ship`, `rv9_set_one`, `rv9_set_off`):

| language | all_constructed | bit_blast | native_first | any route | of |
|---|---|---|---|---|---|
| c | 143 | 136 | 241 | 243 | 255 |
| c++ | 143 | 136 | 241 | 243 | 255 |
| rust | 196 | 203 | 246 | 247 | 255 |
| go | 183 | 203 | 240 | 243 | 255 |
| **proved on at least one language** | **199** | **203** | **251** | **251** | **255** |
| **proved on all four languages** | | | | **235** | **255** |

### 6.3 What moved, and what is left

**LITERAL**:

| what | before | after | of |
|---|---|---|---|
| c, any route | 243 | 243 | 255 |
| c++, any route | 243 | 243 | 255 |
| rust, any route | 247 | 247 | 255 |
| go, any route | 243 | 243 | 255 |
| proved on at least one language | 251 | 251 | 255 |
| proved on all four languages | 235 | 235 | 255 |
| rust, the bit-blast route alone | 202 | 203 | 255 |

| cells with no proof on any language by any route, after | mnem | shape | width |
|---|---|---|---|
|  | `mulh` | `gpr_gpr_gpr` | 64 |
|  | `mulh` | `gpr_gpr_same` | 64 |
|  | `mulhsu` | `gpr_gpr_gpr` | 64 |
|  | `mulhsu` | `gpr_gpr_same` | 64 |

**LITERAL**, the lane's closing line: `the keys the stores hold: 255;
with a proof somewhere: 251; left: 4`.

**GLOSS.** The headline does not move: 251 of 255 on some language, 235
of 255 on all four, the same four boxes open. One column moved — the
bit-blast route on rust, 202 to 203 of 255 — and §4.5 names the cell and
the setting. The task's product is not a number; it is the named cause
under §3.6 and §5.4, and a measured refutation of the idea that less
optimization would close the blast route.

---

## 7. The guard, the counts, and the verifier

### 7.1 The spelling-key guard, over every json this task wrote

**LITERAL**, lane `rv9_l9` step [4/5], which ran
`check_no_spelling_keys.py` over the nine json this task wrote (the
command is in the lane script, whose path is in §7.4):

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS rv9_native.json -- no operator token in any key, grouping, pair
ing or row structure
PASS rv9_native_sample.json -- ... same ...
PASS rv9_set_ship.json -- ... same ...
PASS rv9_set_one.json -- ... same ...
PASS rv9_set_off.json -- ... same ...
PASS rv9_set_sample_ship.json -- ... same ...
PASS rv9_set_sample_one.json -- ... same ...
PASS rv9_set_sample_off.json -- ... same ...
PASS rv9_offcause.json -- ... same ...
  guard rc=0
```

`check_no_spelling_keys.py` was not modified; its sha256 as this task's
lanes read it is
`a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7`.

### 7.2 `grep -c exempt` over every file this task added

**LITERAL**, lane `rv9_l9` step [5/5]: zero on fifteen of the seventeen
files; the two that are not zero are the word inside a sentence, not an
exemption of anything.

```
rv9_native.py:1      line 72: "which the guard exempts as machine form"
rv9_settings.py:0
rv9_offcause.py:0
rv9_union.py:0
lanes_rv9/rv9_l1..l8:0 (eight lane scripts)
lanes_rv9/rv9_l9...:3  the check's own label and its command
```

### 7.3 The files this task added, and the one it changed

It changed NONE. Four new drivers under
`Research/oracle/cross_construction/emulation/construct/general/`
(`rv9_native.py`, `rv9_settings.py`, `rv9_offcause.py`, `rv9_union.py`),
nine lane scripts under `Research/oracle/riscv/lanes_rv9/`, and this
task's own stores beside them. `rv6_all.jsonl`, `rd1_all.jsonl` and
`bb1_all.jsonl` were read and not touched; `riscv_reference.py` was read
and its sha256 recorded on every lane (task sl1 owns it);
`Research/op_pipeline/` was not written to at all.

### 7.4 The lanes

| lane | submitted | elapsed | what |
|---|---|---|---|
| `rv9_l1_the_native_route_sample_of_two_cells.sh` | 17:05:37Z | 53.0 s | the sample: two keys, four languages, every object printed |
| `rv9_l2_the_native_route_on_every_cell_with_no_proof.sh` | 17:08:36Z | 818.5 s | section 1 whole, before the width sweep and the points were added |
| `rv9_l3_the_three_settings_sample_spread.sh` | 17:24:28Z | 180.6 s | the sample for section 2: six keys spread over the gate-count order, three settings |
| `rv9_l4_the_native_route_with_the_width_sweep_and_the_points.sh` | 17:27:31Z | 969.2 s | section 1 whole, with the width sweep and the sampled points |
| `rv9_l5_the_whole_population_at_setting_ship.sh` | 17:43:42Z | 2,269.3 s | 480 attempts at ship flags |
| `rv9_l6_the_whole_population_at_setting_one.sh` | 18:21:32Z | 2,387.2 s | 480 attempts at level 1, go inlining off |
| `rv9_l7_the_whole_population_at_setting_off.sh` | 19:01:19Z | 598.6 s | 480 attempts at optimization off |
| `rv9_l8_the_optimization_off_regression_by_cause.sh` | 19:11:19Z | 273.7 s | rv4's regression, both settings, the three properties |
| `rv9_l9_the_union_of_every_route_and_the_three_settings.sh` | 19:17:01Z | 1.6 s | the tables, the guard, the exempt count |
| `rv9_l10_the_verifier_over_the_final_log.sh` | 19:23:57Z | 0.1 s | the verifier; it found two defects in this log |
| `rv9_l11_the_verifier_over_the_final_log_again.sh` | 19:24:57Z | 0.1 s | the verifier after the log was fixed |

Every lane `state=done exit=0`. One process each, no pool, no clock in
any driver.

### 7.5 The verifier

Two lanes, both from THIS task's instance. Lane
`rv9_l10_the_verifier_over_the_final_log.sh` (tower log
`<runs>/rv9/agent/logs/20260913T192357Z__rv9_l10_the_verifier_over_the_final_log.sh.log`)
read the log as first written and reported `DIFFERS 1, REFUSED 1`. Both
were defects of THE LOG and both were fixed in it, not in the verifier:
the §4.5 transcript named its stores by relative path and the verifier's
working directory is the project root, so the paths did not resolve; and
the §7.1 block began with a `$ ` command that this log's own 72-column
rule had cut across two lines, which is not a command. §4.5 now names its
stores from the project root and §7.1 is an attribution to the lane that
ran the guard, with the command in the lane script.

Lane `rv9_l11_the_verifier_over_the_final_log_again.sh`, tower log
`<runs>/rv9/agent/logs/20260913T192457Z__rv9_l11_the_verifier_over_the_final_log_again.sh.log`,
`state=done exit=0`. The tally, **LITERAL**:

```
## log_273_rv9_the_arch_opcode_axis_the_multiply_high_cause_named.md
   claims 19 | MATCHES 1 | DIFFERS 0 | UNVERIFIABLE 18 | REFUSED 0 |
   NOT_RERUNNABLE 0
   VERDICT: 1 of 19 claims reproduce; 18 (95%) carry nothing to re-run

causes, by name:
  attribution_only                 12
  prose_only                       6
```

ZERO DIFFERS. The one claim that reproduces is §4.5's transcript; the
eighteen that carry nothing to re-run are attributions to a lane log and
the glosses beside them, which is the shape this tool names
`attribution_only` and `prose_only` and counts rather than passes. As in
log_268, the one thing the tally cannot count is itself: this block is an
attribution either way, so re-running the verifier once more prints
exactly the tally above.

---

## 8. FLAGS, each LITERAL

1. **The gate's budget does not close the four, at any room offered.**
   LITERAL, §3.4: twelve rows, `UNDECIDED` at 3,000 ms, `UNDECIDED` at
   30,000 ms, `UNDECIDED` through z3's own bit-blast tactic at 30,000 ms,
   `UNDECIDED` on the low 8, 16, 32 and 64 bits. Count: 12 of 12.
2. **go's bodies for the four are over the ceiling.** LITERAL, §3.1:
   `NOT_GATED` with 18,836 / 18,876 / 14,531 / 14,831 instructions
   against the stated ceiling of 4,000. Count: 4 of 4.
3. **The lifter has no entry for five instructions the compilers write.**
   LITERAL, §4.7 and §5.4: `bexti`, `orn`, `c.not` (owed since bb1) and,
   new here, `c.addi4spn` and `sh3add`. Counts: at ship flags 31 c and 31
   c++ WALK_REFUSED attempts of 120; at optimization off 51 and 51 of
   120; in the regression population 83 of 120 keys.
4. **Optimization off loses 20 proofs of 480 on the blast route and 120
   of 188 keys on the native route.** LITERAL, §4.2 and §5.2.
5. **Four disproofs appear at optimization off that are not there at ship
   flags**, every one with memory seeds in its counterexample. LITERAL,
   §4.6. Count: 4 of 480.
6. **One disproof stands at ship flags and at level 1 and is a proof at
   optimization off** (`czero.eqz gpr_gpr_gpr 64` on rust). LITERAL,
   §4.5. Count: 1 of 120.
7. **Nothing this task ran adds a cell to the headline.** LITERAL, §6.3:
   `the keys the stores hold: 255; with a proof somewhere: 251; left: 4`.

---

## 9. The two lists

### 9.1 Decided, recorded for audit

1. **The population is a reading of verdicts, in both halves.** A cell
   enters section 1's population when no store records a proof for it on
   any language by any route, and section 2's when the blast route left it
   unproved on at least one language. No filter anywhere in this task
   reads a mnemonic; the four names in §2 are printed output.
2. **The three settings are one textual rule per language** — any
   `-O<level>` flag moves to the stated level, any `opt-level=<n>` moves
   to the stated level, go gains its inlining or local-optimization flag —
   applied to all four routes at once. Nothing is keyed on a cell.
3. **`ship` and `one` were both run rather than assumed equal** for c,
   c++ and rust, and the identity of their columns is reported as the
   check it is (§4.1, §4.2, §4.3).
4. **New stores rather than an overwrite.** `rv6_all.jsonl`,
   `rd1_all.jsonl` and `bb1_all.jsonl` are untouched; this task's rows
   are in `rv9_native.jsonl`, `rv9_set_ship.jsonl`, `rv9_set_one.jsonl`,
   `rv9_set_off.jsonl` and `rv9_offcause.jsonl`, so §6.1 and §6.2 are two
   readings of files that both still exist.
5. **Fields added only to this task's own store rows** — `references_out`,
   `memory_operands`, `branches_inside`, `body_term_text`,
   `definition_term_text`, `identical_after_normalize`,
   `first_difference`, `with_more_room`, `at_each_width`, `agreement`.
   No certificate and no shared store gained a field.
6. **The canonical form is `term.py`'s own rule, called from it**, and
   each row records whether this task's text agrees with
   `Term.normalize`'s own return on the same term; it does, on every row.
7. **The sampled-point probe is labelled evidence, never a proof**, in
   the driver's own words and in this log.
8. **Lane `rv9_l2` was kept** even though `rv9_l4` supersedes it: it is
   the same measurement before two more were added, and both are in the
   repo.

### 9.2 Awaiting the owner

1. **The lemma that would close the four is an algebraic one about the
   high half of a width-doubled product, general in width, and it belongs
   in a file this brief did not name.** `Term.normalize` lives in
   `Research/op_pipeline/term.py`; the launch note says to touch nothing
   under `Research/op_pipeline/`. The rule is not a shape rewrite —
   ordering and simplifying never turn a sum into an extract — so it is
   the owed algebraic lemma of `construct/lean/OWED.md` §2 and not a
   normalization rule at all. **Flag for the coordinator; that line is
   stopped here.**
2. **The lifter's missing entries now number five**, and two of them
   (`c.addi4spn`, `sh3add`) are what optimization off costs. Whether they
   are added by hand or wait for task sl1's generated table is sl1's
   question, not this one's; this log records the names and the counts.
