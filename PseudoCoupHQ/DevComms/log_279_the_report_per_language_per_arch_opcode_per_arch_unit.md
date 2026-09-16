# log 279 — the report: what ran tonight, per language, per arch-opcode, with totals; and what it did NOT run on

Written 2026-09-14 by Claude, rebuilt twice at the owner's order. This log
is the report; the chat only points here. Every number says what it
counts. Every name is declared before use, in plain words, with how to
build it. the owner's names keep the owner's meanings; where mine differed, §7
retracts.

## 0. What this is about, in four sentences

An earlier task, t4, printed by program one small source file per
RISC-V instruction in each of four languages: a file whose one
function computes what that instruction computes. Tonight's run
compiled each of those files, asked Lean to prove what the compiled
code computes, and then asked Lean whether that equals Sail's own
definition of some instruction. This report counts how that went, per
language and per instruction, and answers "why 490" and "why not all
RISC-V arch-opcodes". It also says what tonight's run did not touch:
the arch-units.

## 1. The names, yours first

`compiler-operator`
- one operator of one language on one pair of input types: c's `+` on
  an `int32_t` and an `int64_t`; go's `!` on an `int32`.

`arch-unit`
- your definition, kept: the lowered form of a function-wrapped
  compiler-operator. Every compiler-operator was wrapped in a function
  with variable inputs so that its lowered form could be isolated, and
  that lowered form (the machine instructions the compiler emits for
  that function) is the arch-unit.
- built by the census: for each language, for each compiler-operator,
  write `f(a, b) { return a OP b; }`, compile it, and cut the function's
  instructions out of the compiled program. `set_of_arch_units_for_each_lang`
  is that collection per language. For RISC-V it exists:
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/attest_rv.json`
  holds 1,244 such rows (c: 500 attempted, 400 lowered; go: 744
  attempted, 107 lowered; the rest refused by the compiler or not yet
  lowered), each with its operator, its two input types, its
  instructions and its formula. One row, LITERAL:

  > `c/op_0`: operator `!`, left type `int32_t`, body
  > `sltiu a0, a0, 0x1` then `c.jr ra`, formula `!a`.

- tonight's run compiled NONE of these. See §1a.

`arch-opcode`
- your definition, kept: one machine instruction as the compilers
  name it, with what it reads and how many bits it works on.
  `set_of_unique_arch_opcodes` is every arch-opcode any arch-unit of any
  language contains, reduced to one instance each: the union over the
  languages.
- for RISC-V that union, as far as the arch-units above go, is 57
  arch-opcodes (`attest_rv.json`, its `cells` list: for example `add`
  on three 64-bit registers, present in 20 arch-units of c).

`emulated_arch_opcode`
- your definition, kept: one arch-opcode written at a high level in
  one language, with that language's compiler-operators.
- "written" means: PRINTED BY A PROGRAM, t4's `render_general.py`, from
  the instruction's formula. The formula is a tree (for `add`: the node
  `+` over two inputs). The program walks the tree and prints one line
  of the language per node, a named variable each. Two ways of
  printing:
  - THE PLAIN WAY (t4 calls it `native_first`): at a node, if the
    language has an operator of that kind at that width, print it:
    `v0 = a + b`.
  - THE BUILT WAY (t4 calls it `all_constructed`): at every node that
    has a construction, print the construction instead of the
    operator: `+` becomes a carry chain of and, xor and shifts, 32
    lines for a 64-bit add. This is how a language with no operator at
    some width (go has no 128-bit integer) still gets an emulation, and
    t4 printed it for every instruction it could, to measure it.
- one file per (arch-opcode, language, way), in
  `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64/`.
  §2 shows one file each way.

`lowered_emulated_arch_opcode`
- MY name, new, for what tonight actually compiled: one emulated
  arch-opcode file, compiled by the language's compiler, its function
  cut out at its name. Same lowering step as an arch-unit, applied to
  an emulation instead of to a wrapped compiler-operator. I called
  these "arch-units" in log 278, in the tally file and in earlier
  messages; that was wrong (§7).
- tonight: 1,960 of them, 490 per language.

`set_of_emulated_unique_arch_opcodes_for_each_lang`
- your name. For one language: the emulated arch-opcodes t4 printed in
  that language.
- t4 used ONE list for all four languages, so the four sets have the
  same size, 490 files each: 255 arch-opcodes printed the plain way,
  and 235 of those also printed the built way (the 20 not built are
  the float instructions `fadd`, `fsub`, `fmul`, `fdiv`, `fcvt`).
  4 × 490 = 1,960. Where the 255 come from is §1a.

`Sail's definition of an arch-opcode`
- Sail is the language the RISC-V specification is written in, and
  Sail prints its whole RISC-V model as Lean. In that printout every
  instruction is one clause of one function, `execute`; one clause can
  cover a family (`RTYPE` covers add, sub, and, or, xor, sll, srl,
  sra, slt, sltu, with the operation as a field).
- counts in the printout, as of the model version tonight used:
  353 instruction kinds (the constructors of Sail's `instruction`
  type), 339 `execute` clauses. A program turned each clause into a
  pure function (register reads become inputs, the value written to
  the destination register is the output) and Lean checked it against
  the clause: 93 passed (42 single clauses, 51 that only re-dispatch,
  like `c.add` to `add`); 243 touch memory, control registers or traps
  and were not turned; 3 failed. Those 93 are the definitions proof 2
  matches against. So on the DEFINITIONS side tonight already ran on
  all of Sail's RISC-V, and 93 of 339 kinds are usable today.

`proof 1`
- for one lowered emulated arch-opcode: Lean proves "running these
  instructions through Sail's own `execute` leaves this one expression
  in the answer register", the expression written only with the 93
  pure functions. Gets it: COVERED. Not attempted, with the reason
  written down: REFUSED (more than 64 instructions, a call, a float
  instruction, `lui`/`auipc`, a conditional move).

`proof 2`
- for one covered one: Lean proves its expression equal, for every
  input, to one of the 93 definitions with one fixed operation. Three
  provers in order: same text; Lean's integer arithmetic; a bit-level
  check of all 64 bits. Before the provers, both sides are run on four
  sample inputs and every definition that disagrees is dropped; the
  samples only ever remove a definition, never accept one. Gets it:
  MATCHED.

The four ways a covered one ends without a match:
- IDENTITY: it compiled to a bare return, its expression is its
  argument (a `uint8_t` argument arrives zero-extended, so `lbu` has
  nothing to do). Correct; not an instruction.
- BLOCKED BY A CONSTANT: one instruction whose Sail definition takes a
  constant baked into the instruction (`addi`, `slli`, `andi`, ...).
  Proof 2 offers only definitions whose non-register inputs it can
  enumerate; a 12-bit constant cannot be, so its own definition is
  never offered. A gap in my rule; the next fix.
- COMPOSITE: several instructions in the expression (the built way, or
  a compiler rewrite) and every definition dropped by the samples.
  Correct; no single instruction.
- OPEN: a definition survived the samples but no prover closed it.
  Tonight: the built-way `slt`/`sltu` in rust; Sail writes "less than"
  through integers and the bit-level prover cannot open that.

## 1a. Where the 255 come from, and why not all RISC-V arch-opcodes

Verified tonight against the files and the git record. The dates
matter: none of this was done today, and the hand-typed part was
REMOVED today.

- 2026-09-10, task rv1 (four days before this run, before the Lean
  path was designed): a person-typed RISC-V reference,
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/riscv_reference.py`,
  a table of 108 mnemonics with a formula builder each, typed from
  Sail's text and checked against Sail at 860,304 points. That was the
  design of record then: a lifter typed by hand, checked, not proved.
  This session's whole point, from its first message, was that this
  hand-typing is what a formal model makes unnecessary (log 274).
- 2026-09-14 03:02, task sl1 (launched by the daemon from the 09-13
  note, before this session forked; its brief: the lifter's table
  GENERATED from the Sail model): deleted the typed table from that
  file, 693 lines out, 121 in. The commit's own words, LITERAL:

  > TASK sl1 (2026-09-14): THE TABLE IS GENERATED. Sections 4, 4b and 5
  > of this file -- the builders a person typed from Sail's text, the
  > compressed expansions, and the opcode table -- are gone. [...]
  > Nothing below names an instruction. The transcription this
  > replaced is kept beside it for the record, unread by anything.

- Tonight's run (this session's Lean path,
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/`)
  reads none of it: zero references to `riscv_reference`,
  `model_table_rv` or `opcode_table` in its code. Its only definitions
  are Sail's Lean output, checked by Lean (§1, `Sail's definition of an
  arch-opcode`).
- What tonight DID inherit from the typed reference is one thing: the
  choice of which 255 instructions have emulation files, because t4
  printed those files on 09-10/11 from the typed reference's formulas.
  The files are plain c, cpp, rust and go; their meaning tonight came
  from Sail through Lean and from nowhere else. Replacing that
  inherited list is the last item of §8.
- 2026-09-10, task rv2 swept the typed table into the RISC-V model table
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json`:
  1,512 rows of (mnemonic, what it reads, width) tried; 320 got a
  formula ("TRANSLATED"), 1,034 were refused, 88 not spelled, 70 had
  no builder. The 320 translated cells write 255 answer places in all
  (a cell that writes one register is one place; the branch cells
  write a condition; the store cells write memory).
- 2026-09-10/11, task t4 printed one emulation per answer place: 255.
  That is the list. It is the typed reference's reach, not the
  languages' union.

So, to your two questions:

- Is the 255 the union of arch-opcodes used by all the languages? No.
  The union, over the RISC-V arch-units that exist, is 57
  (`attest_rv.json`). The 255 is what the hand-written reference could
  give a formula for, which is wider than the union (the census only
  probes operators, so it never emits `mulhsu` or `sh3add`) and
  narrower than RISC-V (the reference had 108 mnemonics; Sail has 353
  instruction kinds).
- Now that we hold all of Sail's definitions, can we do all RISC-V
  arch-opcodes? On the definitions side we already do: tonight's proof
  2 offers every usable Sail clause, 93 of 339, and the 246 others are
  a rule away (memory, control registers, traps). On the emulations
  side, no: the emulations t4 printed came from the old reference's
  formulas, and there are 255 of them. To emulate every RISC-V
  arch-opcode, the printer would take its formula from Sail's
  definition instead of from `riscv_reference.py`, for each of the 353
  kinds and each value of each operation field. That is a new run, and
  it is the natural next one, because it retires the earlier list from
  the emulation side too.

How many RISC-V instructions there are, counted in Sail's model (the
commit tonight used, `6266b40c`), by reading every mnemonic string its
assembly printer can produce:

| what is counted | count |
|---|---|
| distinct instruction mnemonics the model can print (`add`, `addi`, `vadd.vv`, `c.add`, ...) | 719 |
| of which vector (`v...`) | 368 |
| of which float (`f...`) | 120 |
| of which compressed (`c....`) | 59 |
| of which atomics (`amo...`, `lr`, `sc`) | 12 |
| instruction kinds, one Sail `execute` clause each (a kind covers a family: `RTYPE` is ten mnemonics) | 353 |
| kinds tonight turned into a pure function and Lean-checked | 93 of the 339 the strip step parsed |

A mnemonic is your arch-opcode at the name level; with what it reads
and its width folded in, the count is a little higher (`add` on two
registers and `addi` on a register and a constant are already
different mnemonics in RISC-V, so the difference is small).

## 2. The object: one emulated arch-opcode, both ways

LITERAL, `emulations_riscv64/add_gpr_gpr_gpr_64__reg_a0__c__native_first.c`:

```c
uint64_t
emu_add_gpr_gpr_gpr_64__reg_a0__c__native_first(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)(a + b);
    return v0;
}
```

GLOSS: `add` on two 64-bit registers, printed the plain way with c's
`+`. Lowered, it is one instruction, `add a0, a0, a1`.

LITERAL, the first lines of
`emulations_riscv64/add_gpr_gpr_gpr_64__reg_a0__c__all_constructed.c`
(42 lines in all):

```c
uint64_t
emu_add_gpr_gpr_gpr_64__reg_a0__c__all_constructed(uint64_t a, uint64_t b)
{
    uint64_t v0 = (uint64_t)((uint64_t)((uint64_t)a) & (uint64_t)((uint64_t)b));
    uint64_t v1 = (uint64_t)((uint64_t)(v0) << (unsigned)(uint64_t)(UINT64_C(0x1)));
    uint64_t v2 = (uint64_t)((uint64_t)((uint64_t)a) ^ (uint64_t)((uint64_t)b));
    uint64_t v3 = (uint64_t)((uint64_t)(v2) & (uint64_t)(v1));
```

GLOSS: the same `add`, printed the built way: the carry computed with
and, xor and shifts, no `+` anywhere. Lowered, it is 32 instructions.
Tonight proof 2 proved this one equal to Sail's `RTYPE` with the
operation `ADD`, by the bit-level prover, in 124 seconds.

## 3. The loops

What t4 ran (your loop from the comms protocol's C.1, with the two
ways added):

```
set_of_languages = [c, cpp, rust, go]           # swift too in t4; no swift compiler for RISC-V tonight
answer_places = the 255 answer places of rv2's 320 translated cells

for place in answer_places:
    for lang in set_of_languages:
        print_file(emulate_plain_way(place.formula, lang))     # 255 per lang
        if place is not a float instruction:
            print_file(emulate_built_way(place.formula, lang)) # 235 per lang
```

What ran tonight, over those files:

```
definitions = the 93 pure functions from Sail's Lean printout

for lang in set_of_languages:
    for file in emulations_riscv64 of lang:                    # 490 per lang
        lowered = compile_and_cut(file)                         # a lowered emulated arch-opcode
        expr = proof_1(lowered)                                 # Lean, through Sail's execute
        if expr is REFUSED: write the reason; continue
        candidates = [d for d in definitions
                      if d reads as many registers as expr
                      and d's other inputs can be enumerated]   # constants fall out here
        candidates = [d for d in candidates if samples_agree(expr, d)]
        for d in candidates:
            if proof_2(expr == d): MATCHED; break               # same text, integers, bits
```

## 4. Table 1. Per language

Population: the 1,960 emulation files, one lowered emulated
arch-opcode from each; as of the runs that ended tonight (lanes `l28`
to `l47` on the tower's instance `lp3`).

| language | `set_of_emulated_unique_arch_opcodes_for_each_lang`, lowered | proof 1: COVERED | of which IDENTITY | REFUSED | proof 2: MATCHED | BLOCKED BY A CONSTANT | COMPOSITE | OPEN |
|---|---|---|---|---|---|---|---|---|
| c | 490 | 336 | 99 | 154 | 28 | 66 | 143 | 0 |
| cpp | 490 | 336 | 99 | 154 | 28 | 66 | 143 | 0 |
| rust | 490 | 355 | 99 | 135 | 28 | 54 | 164 | 10 |
| go | 490 | 182 | 66 | 308 | 30 | 18 | 68 | 0 |
| all four | 1,960 | 1,209 | 363 | 751 | 114 | 204 | 518 | 10 |

How to read a row: COVERED + REFUSED = 490. COVERED = IDENTITY +
MATCHED + BLOCKED BY A CONSTANT + COMPOSITE + OPEN. Go is refused most
because its lowered functions carry a call or a stack check inside the
body, and proof 1 does not handle a call. c and cpp are identical
because clang lowers the two to the same instructions for every one of
these files.

Table 1a. The same, split by the two ways of printing.

| language | plain way: files | COVERED | MATCHED | built way: files | COVERED | MATCHED |
|---|---|---|---|---|---|---|
| c | 255 | 167 | 20 | 235 | 169 | 8 |
| cpp | 255 | 167 | 20 | 235 | 169 | 8 |
| rust | 255 | 170 | 20 | 235 | 185 | 8 |
| go | 255 | 95 | 22 | 235 | 87 | 8 |

## 5. Table 2. Per arch-opcode: Sail's definitions and what tonight did with each

Population: the 42 single-clause definitions that passed the pure
function check (the 51 re-dispatching ones point at these). Two counts
per definition: how many covered lowered emulations have it inside
their expression, and how many proof 2 matched to it. Both c / cpp /
rust / go / all.

| Sail's definition | can proof 2 offer it? | inside a covered expression | MATCHED to it |
|---|---|---|---|
| `RTYPE` (add, sub, and, or, xor, sll, srl, sra, slt, sltu) | yes | 141 / 141 / 180 / 64 / 526 | 24 / 24 / 24 / 13 / 85 |
| `ITYPE` (addi, andi, ori, xori, slti, sltiu) | no, a constant | 135 / 135 / 154 / 72 / 496 | 0 |
| `SHIFTIOP` (slli, srli, srai) | no, a constant | 108 / 108 / 141 / 65 / 422 | 0 |
| `ZBA_RTYPEUW` (add.uw, sh1add.uw, sh2add.uw, sh3add.uw) | no, a constant | 54 / 54 / 0 / 0 / 108 | 0 |
| `ZBA_RTYPE` (sh1add, sh2add, sh3add) | no, a constant | 31 / 31 / 0 / 0 / 62 | 0 |
| `SHIFTIWOP` (slliw, srliw, sraiw) | no, a constant | 18 / 18 / 19 / 0 / 55 | 0 |
| `ADDIW` | no, a constant | 16 / 16 / 16 / 0 / 48 | 0 |
| `ZBB_RTYPE` (andn, orn, xnor, max, min, rol, ror) | yes | 13 / 13 / 0 / 0 / 26 | 0 |
| `MUL` (mul, mulh, mulhu, mulhsu) | yes | 4 / 4 / 4 / 2 / 14 | 2 / 2 / 2 / 1 / 7 |
| `RTYPEW` (addw, subw, sllw, srlw, sraw) | yes | 3 / 3 / 4 / 0 / 10 | 2 / 2 / 2 / 0 / 6 |
| `ZBS_IOP` (bclri, bexti, binvi, bseti) | no, a constant | 5 / 5 / 0 / 0 / 10 | 0 |
| `REM` (rem, remu) | yes | 1 / 1 / 2 / 0 / 4 | 0 |
| `DIV` (div, divu) | yes | 1 / 1 / 1 / 0 / 3 | 0 |
| `ZBB_EXTOP` (sext.b, sext.h, zext.h) | yes | 0 | 0 / 0 / 0 / 16 / 16 |
| the other 28 (`CLMUL`, `CLZ`, `CTZ`, `DIVW`, `MULW`, `REMW`, `REV8`, `RORI`, the six `SHA512`, `ZBS_RTYPE`, ...) | mixed | 0 | 0 |
| all 42 | | 13 definitions appear; 1,784 definition-file pairs | 4 definitions matched; 114 files |

Reading the two columns together: the seven "no, a constant" rows are
used constantly and matched never; that is the 204 BLOCKED BY A
CONSTANT of Table 1. `ZBB_EXTOP` is matched by 16 go files whose
expressions never contain it: two shifts by 48 proved equal to zext.h.
28 of the 42 definitions never appear because the 255 places have no
instruction that lowers to them.

## 6. Table 3. Per file, one row each

All 1,960 rows:
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/tally_corpus_final.md`
(language, way, proof 1, instruction count, outcome, the definition
matched, the prover; the file still says "unit" for these, see §7).
Ten rows here, one of each outcome, checked against that file:

| file (the arch-opcode and its answer place) | language | way | proof 1 | instructions | outcome | matched to | prover |
|---|---|---|---|---|---|---|---|
| add_gpr_gpr_gpr_64, reg_a0 | c | plain | COVERED | 1 | MATCHED | `RTYPE` ADD | same text |
| add_gpr_gpr_gpr_64, reg_a0 | c | built | COVERED | 32 | MATCHED | `RTYPE` ADD | bit level, 124 s |
| mulhu_gpr_gpr_gpr_64, reg_a0 | c | plain | COVERED | 1 | MATCHED | `MUL` high, unsigned | integers (the compiler swapped the operands) |
| lhu_gpr_gpr_16, reg_a0 | go | plain | COVERED | 2 | MATCHED | `ZBB_EXTOP` zext.h | bit level, 5 s |
| addi_gpr_gpr_imm_64, reg_a0 | rust | plain | COVERED | 1 | BLOCKED BY A CONSTANT | | |
| and_gpr_gpr_same_64, reg_a0 | cpp | plain | COVERED | 0 | IDENTITY | | |
| bne_gpr_gpr_same_64, branch condition | c | plain | COVERED | 2 | COMPOSITE (xor then sltu) | | |
| slt_gpr_gpr_gpr_64, reg_a0 | rust | built | COVERED | 39 | OPEN (`RTYPE` SLT survived the samples) | | |
| mulh_gpr_gpr_gpr_64, reg_a0 | c | plain | REFUSED: 274 instructions, above the run's bound of 64 (t4 printed the sign extension as 64 shifted copies) | | | | |
| fadd_d_fpr_fpr_fpr_64, freg_fa0 | cpp | plain | REFUSED: a float instruction | | | | |

## 7. What I had wrong, retracted

- I called tonight's 1,960 compiled emulations "arch-units", in log
  278, in `tally_corpus_final.md` (its column says "unit") and in
  chat. An arch-unit is the lowered form of a function-wrapped
  compiler-operator; these are lowered emulations of arch-opcodes. The
  only true arch-units tonight touched were the ten from rv1's census
  in the small first run (`c/op_534`, `go/op_312` and eight more),
  which are in log 278 §4 and not in this report's tables.
- I wrote "490 arch-units per language" as if it were your
  `set_of_arch_units_for_each_lang`. It is t4's 255 answer places
  printed for every language, plain way and built way.
- I wrote that t4's list came from an unknown place. It is rv2's
  model table, 320 translated cells, 255 answer places (§1a).
- I reported "414 with no candidate"; the real split is 204 BLOCKED BY
  A CONSTANT and 518 COMPOSITE.
- I reported 43 single clauses and 50 re-dispatching; it is 42 and 51.
- A table I sent said 98 matched; two result files were missing from
  the laptop's copy; with them it is 114, as the tower's own count
  says.

## 8. Anchors

- research: proof 1 covers 1,209 of the 1,960 lowered emulations with
  no instruction name anywhere in the code that does it; proof 2
  matches 114 of them to Sail's definitions and is blocked by one rule
  (the constants) for 204 more. The arch-units themselves (1,244 for
  RISC-V) have not been through these two proofs yet.
- mine next, in order: run the two proofs over the RISC-V arch-units
  (`attest_rv.json`), which is the set the research is about; the
  constants as inputs to solve; each instruction's value written once
  in the expression instead of copied; Sail's "less than" rewritten
  for the bit-level prover; then your branch idea; then the printer
  fed from Sail's definitions so every RISC-V arch-opcode has an
  emulation.
- yours: whether `lowered_emulated_arch_opcode` is a name you want, or
  what to call these instead; the result folders are large and
  uncommitted.
- third party: none.

## 9. Pointers

- the run's full account: `PRIVATE/PseudoCoupHQ/DevComms/log_278_the_lean_proof_path_runs_the_handful_closes.md`
- every file, one row each: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/tally_corpus_final.md`, made by `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/tally_corpus_final.py`
- the arch-units for RISC-V: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/attest_rv.json`
- rv2's model table: `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/model_table_rv.md`
- the emulations t4 printed: `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64/`
- t4's own report: `PRIVATE/PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/general.md`
