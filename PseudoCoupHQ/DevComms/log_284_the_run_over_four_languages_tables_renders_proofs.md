# log 284 — the run over four languages: the tables, the renders, the proofs

2026-09-15, early morning to mid-morning, on the tower (instance lp3,
lanes l62 to l75). the owner: "run it." The order given: the gate with the
width rule, then all of c, then cpp, rust, go. Every lane had its
PROGRESS row before its submit; every gate was read before the wide
run it guarded. Nothing in it names an instruction, an operator's
spelling, or a compiler version except the one invocation line per
language.

## 1. walkthrough

Each language's compiler-operators (the operator pipeline's probes,
function-wrapped) were compiled for riscv64 at the corpus's own ship
flags, cut out at their symbols, decoded by Sail's own decoder, and
their meanings composed from Sail's definitions and certified in Lean.
Then the subterms of Sail's definitions (136 of them over the 42
definitions read; 97 typed as 64-bit in and out) were proved against
those meanings, every proof an entry of the language's swap table.
Then every arm of every definition was rendered from that table and
nothing else, compiled, read back, and proved equal to a definition.
Seven defects came out on the way, each found by a gate or by the
first wide run, each fixed by a rule and recorded in the plan's
PROGRESS. What is not in any table is the integer-level residue the
plan names: the 64-bit multiply, divide and remainder, whose Sail
definitions go through unbounded integers.

## 2. per language

| language | probes | meanings certified | keys | entries | rendered | lowered and read back | proved |
|---|---|---|---|---|---|---|---|
| c | 750 | 346 | 11 (10 at 64) | 109 | 13 | 13 | 13 |
| cpp | 1002 | 418 | 11 (10 at 64) | 160 | 13 | 13 | 13 |
| rust | 858 | 90 | 12 (11 at 64) | 38 | 17 | 17 | 16 |
| go | 744 | 21 | 4 (3 at 64) | 6 | 3 | 3 | 2 |

Refusals at the corpus stage, by cause: the language's own compiler
refusing a probe (c 140, cpp 232, rust 733, go 637: mismatched
holders, the pipeline's acceptance gate); float probes the pruned
decoder does not know (c 248, cpp 326, rust 24, go 22); go's calls into
its runtime (40); walk shapes not read (c 16, cpp 26, rust 11, go 24).

Not proved after render: one row in rust and one in go, both `C_NOT`
rendered from the language's complement (`xori a, -1`), an
immediate-carrying definition the proof stage has no candidate for; the
eye tables show the row. Every other rendered emulation compiled back
to the one instruction its definition names and proved by the same
text.

## 3. the swap tables, one matrix

| key: a subterm of Sail's definitions | c | cpp | rust | go |
|---|---|---|---|---|
| `(a &&& b)` | 18 (4 at 64) | 35 (8 at 64) | 5 (2 at 64) |  |
| `(a ^^^ b)` | 17 (4 at 64) | 34 (8 at 64) | 5 (2 at 64) |  |
| `(a \|\|\| b)` | 17 (4 at 64) | 34 (8 at 64) | 5 (2 at 64) |  |
| `(a + b)` | 13 (4 at 64) | 13 (4 at 64) | 2 (2 at 64) |  |
| `(a - b)` | 13 (4 at 64) | 13 (4 at 64) | 2 (2 at 64) |  |
| `shift_bits_left a (extractLsb b 5 0)` | 8 (4 at 64) | 8 (4 at 64) | 6 (4 at 64) |  |
| signed less-than as a bit | 8 (1 at 64) | 8 (1 at 64) | 2 (1 at 64) | 1 (1 at 64) |
| unsigned less-than as a bit | 6 (3 at 64) | 6 (3 at 64) | 1 (1 at 64) | 1 (1 at 64) |
| `shift_bits_right a (extractLsb b 5 0)` | 4 (2 at 64) | 4 (2 at 64) | 3 (2 at 64) |  |
| `shift_bits_right_arith a (extractLsb b 5 0)` | 4 (2 at 64) | 4 (2 at 64) | 3 (2 at 64) |  |
| `(Complement.complement a)` |  |  | 3 (2 at 64) | 3 (2 at 64) |
| the 32-bit multiply (`sign_extend (to_bits_truncate 32 (toInt a *i toInt b))`) | 1 (0 at 64) | 1 (0 at 64) | 1 (0 at 64) | 1 (0 at 64) |

A cell is "units proved equal (of which at 64-bit holders)". go's
table is short because go compiles most operators through its runtime
(a call the walk refuses) and refuses mixed holders; its 21 certified
units are the unary ones, the multiplies and the comparisons.

## 4. the definitions rendered and proved, per language

- c and cpp: RTYPE ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU; the
  three SHIFTIOP forms render with their immediate as an input and
  prove equal to the register form (SLL, SRL, SRA)
- rust: the ten above and ZBB ANDN, ORN, XNOR (the complement key)
- go: SLT, SLTU

## 5. the seven defects, each fixed by a rule

| found by | defect | rule |
|---|---|---|
| l49/l50 | every certificate failed on a phantom `Sail.Vector` | the library index keyed by whole dotted names; a capitalised last segment is a type |
| l53/l55 | the typing pass let lean-sail coerce a Nat and a narrow vector through | the inferred type from `#check`, not an expected type |
| l55 | a constant meaning wrote `fun  =>` inside a string and swallowed every line after it | constant meanings skipped |
| l56 | 92 surviving pairs, 0 proved: the unfolding closed the goal and the bare prover failed on "no goals" | `all_goals` |
| l62 gate | `-` on (int64_t, int32_t) called at 64 | holder widths in every entry; render takes a unit only at 64 |
| l63 | long `#check` results dropped: no shifts, no multiplies | continuation lines joined; literal widths evaluated |
| l66 gate | go's complement failed every stage: its meaning's `sign_extend` never unfolded | the unit's own definitions join the unfold list |
| l70 gate, l72 | go: a `bool` result has no integer conversion; a `nop` the strip never read; the zero-word padding after a function read as body | the return type off the probe's own signature; a clause whose body is only the retire is no change; trailing zero words dropped |

(Eight rows for seven fixes: the last row is three small ones.)

## 6. what stands open, for the plan

- the integer-level primitives (`Int.tdiv`, `*i` at 64, `to_bits_truncate`): no 64-bit compiler-operator proves equal; `compose_at_width` under a once-proved theorem is the plan's answer and is not written
- immediate-carrying definitions (`C_NOT`, the I-type forms): rendered when a key matches with the immediate as an input, but `equals` has no candidate for them; the candidate set of `equals` needs the immediate as a parameter
- 289 of 339 definitions are not read yet (vector, float, control registers, atomics); every table above is over the 42 that are
- the rendered set per language is 13 to 17 definitions because the keys are 11 or 12; the tables grow only by what proves

## 6a. correction, 2026-09-15 mid-morning: the first item of §6 was wrong

§6 says the integer-level primitives have "no 64-bit compiler-operator
[that] proves equal" and that `compose_at_width` is the answer. That was
my reading, and it was wrong. An Opus agent found the true cause (its
report is in the `operator_for` leaf's PROGRESS): the candidate reader
dropped every subterm of a definition that still carried the
definition's flag parameter (`is_unsigned`, the `mul_op` structure), so
the multiply, divide and remainder subterms were never tried against
any arch-unit. The rule that fixed it: a definition is read at every
value of its non-register parameters, as the proof stage already
enumerates them; the `if`s and `match`es a value makes literal are
folded. The gate (lanes l76, l77, 302 s; `runs/gate_c_flags/eye_table.md`):
120 typed candidates, a swap table of 10 subterms, 10 definitions
rendered and 10 proved by the same text, among them MUL (low, signed),
DIV signed and unsigned, REM signed and unsigned, each lowering to its
one instruction (`mul`, `div`, `divu`, `rem`, `remu`). No bit-blasting
was needed; the arch-unit's Lean expression is Sail's definition,
constraints included. `compose_at_width` stays what the plan says it
is, the answer for a width a language lacks (a 128-bit product on a
64-bit word), not for these. The wide run with the rule is §10 below.

## 7. decided, recorded for audit

- the four corpora lowered and read; the four tables; the four renders; every row in `runs/<lang>/pass_b/eye_table.md`
- the seven rules above, in the code and in the leaves' PROGRESS
- nothing is queued on the tower; instance lp3 is idle

## 8. awaiting the owner

- read the eye tables (`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/{handful_c,corpus_cpp,corpus_rust,corpus_go}/pass_b/eye_table.md`)
- the two residues of §6 that need a design word: `compose_at_width` (the once-proved theorem per operation kind), and immediates as parameters of the candidates in `equals`
- instance lp3: leave up or down

## 9. pointers

- the summary of every number here: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/run_summary_2026-09-15.json`
- the lanes: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lanes_lp1/lp3_l62_*` to `lp3_l75_*`
- the plan: `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/`
- the earlier records: log 280 (the start-over and the audit), log 282 (the first gate), log 283 (the verifying session's reply)

## 10. the run again with the flag rule

2026-09-15, afternoon to evening, on the tower (instance lp3, lanes l78
to l81, 3375 s + 191 s + 5436 s + 476 s). The same four languages, the
same corpora, the same walks — nothing was re-lowered. What changed is
one rule in the candidate reader and the same rule in `render`, and the
four swap tables and four renders were written again over it. Every
lane had its PROGRESS row before its submit, and the gate (§6a) was read
before the first of them.

### the defect and the rule

`operator_for`'s candidates are the subterms of Sail's own certified
pure forms over their register reads. The reader dropped every subterm
whose free names still carried one of the definition's NON-register
parameters — the flags a definition takes beside its two register reads.
So every subterm of the divide and the remainder was thrown away before
any proof was tried, and the multiply's one subterm survived only by
accident (a structure field read is one identifier, so the filter never
saw the structure) and was then refused by Lean at typing. The
evaluation stage was never at fault: its own log said `0 did not
evaluate`. The keys were missing because the candidate set was missing.

THE RULE: a pure form is read at EVERY value of its non-register
parameters, by the same `enum_values` the definition side of `equals`
already uses (an `inductive` of nullary constructors is its
constructors, a `structure` of such fields is their product, `Bool` is
false/true), the free form kept beside them; the `if`s and `match`es a
value makes literal are folded; a field read counts as a mention of its
structure; a candidate's unknowns are ordered by the pure form's own
read order; a width Lean prints as a name is evaluated by Lean.
`render.definitions_of` takes a definition's arms by the same rule, so a
definition whose operation IS a flag has arms at all.

Candidates 136 -> 186, of which 120 type exactly `BitVec 64` in and out
(was 97). Definition arms 75 -> 93. Nothing in the rule names an
instruction or an operator token; the guard passes on every product.

### per language

| language | compiler-operators (probes) | arch-units expressed in Lean | keys | entries | keys at 64 | rendered | lowered and read back | proved |
|---|---|---|---|---|---|---|---|---|
| c | 750 | 346 | 23 | 163 | 15 | 18 | 18 | 18 |
| cpp | 1002 | 418 | 23 | 214 | 15 | 18 | 18 | 18 |
| rust | 858 | 90 | 17 | 48 | 12 | 18 | 18 | 17 |
| go | 744 | 21 | 5 | 8 | 4 | 4 | 4 | 3 |

Beside the run of §2, whose tables were written from the short candidate
set: keys c 11 -> 23, cpp 11 -> 23, rust 12 -> 17, go 4 -> 5; entries
109 -> 163, 160 -> 214, 38 -> 48, 6 -> 8; proved 13 -> 18, 13 -> 18,
16 -> 17, 2 -> 3. Nothing that proved before stopped proving.

The corpora and their walks are unchanged, so the refusal counts of §2
stand as written.

### the definitions that now prove and did not before

- c and cpp: the 64-bit multiply (low half, both operands signed), the
  signed and the unsigned divide, the signed and the unsigned remainder
  — five each, every one rendered from a key that is an integer-level
  subterm of Sail's own definition, lowered at the language's ship
  flags, read back as the one instruction the definition names, and
  proved by the same text
- rust and go: the 64-bit multiply
- everything of §4 still proves: the ten register forms and the three
  immediate shift forms for c, cpp and rust; rust's three complement
  forms; go's two comparisons

### the swap tables, one matrix

The full matrix is `runs/key_matrix_2026-09-15_flag_rule.md`. What is
new in it beside §3, all of it integer-level or 32-bit-wide:

| key: a subterm of Sail's definitions | c | cpp | rust | go |
|---|---|---|---|---|
| the 64-bit multiply, low half, both signed | 8 (4 at 64) | 8 (4 at 64) | 2 (2 at 64) | 2 (2 at 64) |
| the unsigned remainder at 64 | 6 (3 at 64) | 6 (3 at 64) | | |
| the unsigned divide at 64 | 6 (3 at 64) | 6 (3 at 64) | | |
| the signed remainder at 64 | 4 (1 at 64) | 4 (1 at 64) | | |
| the signed divide at 64, with its overflow guard | 4 (1 at 64) | 4 (1 at 64) | | |
| the 32-bit left shift, sign-extended | 8 (0 at 64) | 8 (0 at 64) | 3 (0 at 64) | |
| the 32-bit arithmetic right shift, sign-extended | 4 (0 at 64) | 4 (0 at 64) | 3 (0 at 64) | |
| the 32-bit logical right shift, sign-extended | 4 (0 at 64) | 4 (0 at 64) | | |
| the 32-bit add, sign-extended | 3 (0 at 64) | 3 (0 at 64) | 1 (0 at 64) | |
| the 32-bit subtract, sign-extended | 3 (0 at 64) | 3 (0 at 64) | 1 (0 at 64) | |
| the 32-bit remainder and the 32-bit divide, sign-extended | 2 + 2 (0 at 64) | 2 + 2 (0 at 64) | | |

A cell is "arch-units proved equal (of which at 64-bit holders)".

### what still does not prove

- **the W forms.** Eight of c's and cpp's 23 keys are the 32-bit
  operations widened back to 64 — the arch-units that prove equal to
  them are held at 32-bit holders, and the width rule of log 283 §3
  refuses a unit at render whose holders are not the definition's
  operand widths. They are in the table by proof and are not rendered:
  15 of 23 keys are usable at render for c and cpp, 12 of 17 for rust,
  4 of 5 for go. Whether a 32-bit holder may render a 32-bit definition
  is a width question for the plan, not a defect.
- **`C_NOT` in rust and go**, unchanged from §2: rendered from the
  language's complement, lowered, read back — and `equals` has no
  candidate for an immediate-carrying definition. This is still the
  second residue of §6.
- **the composite meanings.** Two of the gate's dozen matched nothing,
  and the same shape recurs across the corpora: an arch-unit whose
  meaning is one definition applied to another (a comparison built of
  two instructions) can never equal a single subterm. `operator_for` is
  keyed by one subterm by design; a composition is `pass_c`'s object.
- **the rest of the refusals at render**: 75 of 93 arms for c, cpp and
  rust, 89 for go. The keys their definitions want are the bit
  manipulations, the rotates, the immediate forms, the sign extensions
  and the mixed-signedness multiplies. The table grows only by what
  proves.
- 289 of 339 definitions are still not read (vector, float, control
  registers, atomics); every table above is over the 42 that are.

### decided, recorded for audit

- the four tables and the four renders rewritten under the flag rule;
  every row in `runs/{handful_c,corpus_cpp,corpus_rust,corpus_go}/pass_b/eye_table.md`
- the summary and the matrix rebuilt by
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/run_summary.py`
  into `run_summary_2026-09-15_flag_rule.json` and
  `key_matrix_2026-09-15_flag_rule.md` beside the earlier
  `run_summary_2026-09-15.json`, which is left as it was written
- the spelling guard passed on every table and every render
- nothing is queued on the tower; no lean, lake, `python3 leanpath`,
  clang, rustc or go process of this run remains; instance lp3 is left up

### awaiting the owner

- the first residue of §6 is closed, by §6a and by this run: the
  integer-level operations prove from the languages' own arch-units,
  and `compose_at_width` was not needed for them
- the width question the W forms raise: may an arch-unit held at 32-bit
  holders render a 32-bit definition, or does the width rule stand?
- the immediate residue is unchanged: the candidate set of `equals`
  needs the immediate as a parameter (`C_NOT` in rust and go)
- the lanes: `lanes_lp1/lp3_l78_*` to `lp3_l81_*`

## 11. the width rule by the definition's own use

2026-09-15, evening, on the tower (instance lp3, lanes l82 to l86). the owner
decided the width question §10 left open. Gate first, its table read,
then the wide run for c and cpp, the two languages with W-form keys.
Every lane had its PROGRESS row before its submit.

### the rule

The rule as it stood asked every arch-unit for 64-bit holders, because a
definition's operands are register reads. That is wrong for the W forms.
Their Sail text reads only the low 32 bits of each register and
sign-extends a 32-bit result, so the width they use is 32. The arch-units
Lean proved equal to them are held at 32-bit holders (c's
`int32_t + int32_t`).

THE RULE: a definition's operand width, per read, is the width the
definition's own subterm uses of that read, read off the key's own text.

| how the subterm uses a read | its operand width |
|---|---|
| sliced from bit 0 by literal bounds, `extractLsb a 31 0` | the slice's width, 32 |
| used whole | 64 |
| used both ways | 64 |
| sliced by a bound written in the architecture's own word size, `extractLsb b (log2_xlen -i 1) 0` | 64 |

- `operator_for` works the widths out when it builds a key. It writes
  them beside the key (`operand_widths`) and into every entry.
- `render` takes an arch-unit for a key when the arch-unit's holder
  widths equal those widths. A refusal names both.
- The result needs no rule, because a definition's result is the
  register.
- Nothing is keyed by a name, and the guard passes on every JSON written.

The last row of the table is my reading, not the owner's words; see "awaiting
the owner". The 64-bit shift masks its amount to six bits. Taken as a slice,
that read would be width 6, no holder has that width, and the three
64-bit shifts and their three immediate forms would stop rendering. Such
a bound grows with the register, so the read stays whole.

### the gate (lane l82, 313 s)

The dozen were picked by a rule, not by an operator token. The rule: the
first c arch-unit of each distinct meaning whose holders are all one
width, with meanings that name a definition this rule reads narrower
than the register first. The rule finds 14 such definitions.

| arch-units expressed in Lean | subterms filled | read at (32, 32) | usable at render | rendered | lowered | proved |
|---|---|---|---|---|---|---|
| 12 | 12 | 8 | 11 | 11 | 11 | 11 |

The seven W forms rendered from arch-units held at (32, 32). Each one
lowered to one instruction and the return, and each proved by the same
text. RTYPEW SRLW was refused, as it should be: its only arch-unit is
held at (1, 1).

### the wide run, per language

Lanes l83 (c table, 3375 s), l84 (c render, 273 s), l85 (cpp table,
4398 s) and l86 (cpp render, 270 s); all exited 0. The walks and corpora
were not redone. The tables are the same keys and entries as in §10,
now with the widths beside each key.

| language | arch-units expressed in Lean | subterms filled | read at (32, 32) | usable at render | rendered | lowered | proved |
|---|---|---|---|---|---|---|---|
| c | 346 | 23 (163 entries) | 8 | 22 (was 15) | 25 (was 18) | 25 | 25 |
| cpp | 418 | 23 (214 entries) | 8 | 22 (was 15) | 25 (was 18) | 25 | 25 |

### the definitions newly proved, the same seven in c and cpp

| definition | arch-unit it rendered from | holders | lowered to |
|---|---|---|---|
| RTYPEW ADDW | `op_102` | (32, 32) | `C_ADDW`, return |
| RTYPEW SUBW | `op_138` | (32, 32) | `C_SUBW`, return |
| RTYPEW SLLW | `op_678` | (32, 32) | `RTYPEW`, return |
| RTYPEW SRAW | `op_714` | (32, 32) | `RTYPEW`, return |
| MULW | `op_174` | (32, 32) | `MULW`, return |
| DIVW, signed | `op_210` | (32, 32) | `DIVW`, return |
| REMW, signed | `op_246` | (32, 32) | `REMW`, return |

Every one proved equal to its definition by the same text. Distinct
definitions proved went from 15 to 22 in each language. Nothing that
proved before stopped proving; all eighteen emulations of §10 still
prove.

### what still does not render

- **RTYPEW SRLW, the 32-bit logical right shift.** It is in the table by
  proof, but its arch-units in c and cpp are held at (1, 1), (1, 32) and
  (1, 64), and none at (32, 32). The rule refuses it, as it should.
- **The unsigned 32-bit divide and remainder.** No arch-unit proved equal
  to them, so the table has no key for them.
- **rust and go were not re-run.** Their tables of record are the §10
  ones. Rendered locally from those tables, and not lowered or proved:
  rust goes from 12 to 17 of 17 keys usable and 18 to 23 emulations
  (MULW, ADDW, SUBW, SLLW, SRAW); go goes from 4 to 5 of 5 keys and 4 to
  5 emulations (MULW).
- The rest of §10's list stands: `C_NOT` in rust and go, the composite
  meanings, and the definitions not read yet.

### decided, recorded for audit

- the rule, coded in `leanpath/operator_for.py` (`operand_widths`,
  `read_slice`) and `leanpath/render.py` (`Renderer.__init__`); the
  PROGRESS rows are in the `operator_for`, `render` and
  `the_run/everything` leaves
- the c and cpp tables and renders rewritten under the rule, every row in
  `runs/{gate_c_widths,handful_c,corpus_cpp}/.../eye_table.md`
- the spelling guard passed on every JSON written by the five lanes
- no lean, lake or `python3 -m leanpath` process of these lanes remains
  on the tower. Instance lp3 is left up and is running another agent's
  queue (l88, l89). About 231 old defunct lean and lake entries from
  earlier runs are still listed there, using no CPU or memory.

### awaiting the owner

- one reading to confirm: a slice bound written in the word size (the
  64-bit shift's mask on its amount) counts as a whole read, so it stays
  at 64
- whether to re-run rust and go under the rule (their local renders gain
  five and one)

### pointers

- the lanes: `lanes_lp1/lp3_l82_*` to `lp3_l86_*`
- the gate: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_c_widths/eye_table.md`
- the eye tables: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/{handful_c,corpus_cpp}/pass_b/eye_table.md`
