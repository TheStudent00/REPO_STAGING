# log 278 — the Lean proof path runs: the handful closes, pass A over the corpus

Written 2026-09-14 by the launching session (Claude), on the tower,
instance `lp3`. Continues log 274 (the design) and logs 275–276 (the
emit that would not build). Plan node:
`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/`.

## 1. In plain words

The design of log 274 now runs end to end on the tower. Sail's own Lean
emit of the RISC-V model (model `6266b40c`, sail `8eb1fb6b`, the last
pair whose Lean CI was green) is the only definition of any opcode.
Three passes were written once and run over everything:

- **strip** reads every `execute_*` clause of the emit and proposes its
  pure form by one rule (register reads become parameters, the written
  value is the result); Lean certifies each proposal against the
  emitted clause. 93 of 339 clauses certify; 243 are refused because
  they have effects the rule does not model (memory, CSRs, traps); 3
  fail.
- **walk** takes a compiled unit (a C, C++, Rust or Go function
  compiled to riscv64), carves its instructions, has Sail's own decoder
  say what each word is, composes the certified pure forms through the
  registers, and asks Lean to certify that running the model's own
  `execute` on those instructions leaves the proposal in the answering
  register. **All 11 walkable units of the handful certify**, 15–17 s
  each; 7 are refused for stated reasons (§4).
- **equals** asks, for each certified unit, which definition it is: every
  certified clause of matching arity, every value of its enumerated
  operation, is a candidate; nothing is chosen by a name. **10 of 11
  units find their definition.** The multiply-high wall of log 273
  falls where log 274 §5.3 said it would: `mulh` and `mulhu` compiled
  with the operands swapped are proved equal to Sail's `MUL` clause at
  the integer level by `grind`, in 1.2 s, after Sail's own helper
  (`mult_to_bits_half`) is unfolded. The eleventh unit is two
  instructions (`xor` then `sltu`), a composite that is no single
  opcode; all 52 candidates are refuted with counterexamples.

Every patch between the first run and the closing run replaced a
spelling with a rule (§6). The certificate's simp set is now derived:
the clauses walked, every emitted definition reachable from them, the
register-index definitions, the callbacks, and the lean-sail helpers
those definitions name in their own text.

Pass A over the rendered corpus (1,960 sources, four languages, both
routes) is running as this is written; §7 carries its tallies when the
lane returns.

## 2. What ran, where

| step | lane | instance | what |
|---|---|---|---|
| strip, whole model | `lp3_l19` | lp3 | 339 clauses → 93 certified (105 s wall) |
| walk, handful v5 | `lp3_l19` | lp3 | 7 of 18 certified; the alias units failed |
| residual probes | `lp3_l18`, `l20`, `l24`, `l27` | lp3 | one certificate each, the goal Lean left |
| cross-toolchains | `lp3_l21` | lp3 | c, cpp, rust, go all emit riscv64 objects |
| gate + equals + corpus | `lp3_l28` | lp3 | the closing run (§4, §5, §7); its equals stage stopped, superseded |
| the 363 failures again | `lp3_l29` | lp3 | lost its record to a closed pipe (`head` in the lane); superseded |
| equals, pooled | `lp3_l30` | lp3 | stopped: one candidate at a time was hours; superseded |
| the 363 again, repaired | `lp3_l31` | lp3 | all 363 certify (§7) |
| equals, round 1 batched | `lp3_l32` | lp3 | the final equals and tallies (§7.1) |

Lane scripts: `Research/oracle/riscv/leanpath/lanes_lp1/`. Code:
`Research/oracle/riscv/leanpath/leanpath/` (`strip.py`, `walk.py`,
`equals.py`, `__main__.py`). Artifacts (on the tower's copy, synced back
at the end of the run): `strip_6266b40c_8eb1fb6b_all_v5/`,
`walk_handful_all_v10/`, `equals_handful_all_v10/`, `walk_corpus_<k>/`,
`equals_corpus_<k>/`.

## 3. strip: 93 of 339

| verdict | count | why |
|---|---|---|
| CERTIFIED | 93 | 42 straight clauses, 51 `ExecuteAs` aliases |
| REFUSED | 243 | an element the one rule does not know: memory, CSR, trap, a monadic `let` |
| FAILED | 3 | `C_SSPUSH`, `C_SSPOPCHK`, `C_EBREAK`: aliases whose target is not a clause the rule certifies |

The alias `C_MUL` joined after the struct literal of its target was
flattened to one line (a text repair in `one_line`, not a spelling).

## 4. walk: the handful, closing run (lane `lp3_l28`, `walk_handful_all_v10`)

18 units: 10 rv1 units (words from `carved.json`), 4 rv9 rendered
`mulh`/`mulhsu` C sources, 4 small multiply probes.

| unit | source | verdict | s | proposal |
|---|---|---|---|---|
| go_op_312 | go, `c.add` | CERTIFIED | 16.4 | `pure_RTYPE a b ADD` |
| c_op_174 | c, `mulw` | CERTIFIED | 16.4 | `pure_MULW b a` |
| c_op_714 | c, `sraw` | CERTIFIED | 16.6 | `pure_RTYPEW a b SRAW` |
| c_op_726 | c, `srl` | CERTIFIED | 16.3 | `pure_RTYPE a b SRL` |
| c_op_210 | c, `divw` | CERTIFIED | 16.3 | `pure_DIVW a b false` |
| c_op_498 | c, `c.xor; sltu` | CERTIFIED | 16.3 | `pure_RTYPE zero_reg (pure_RTYPE a b XOR) SLTU` |
| c_op_102 | c, `c.addw` | CERTIFIED | 16.3 | `pure_RTYPEW a b ADDW` |
| probe_mul | c, `c.mul` | CERTIFIED | 16.6 | `pure_MUL a b {Low, Signed, Signed}` |
| probe_mulh | c, `mulh` | CERTIFIED | 15.5 | `pure_MUL b a {High, Signed, Signed}` |
| probe_mulhu | c, `mulhu` | CERTIFIED | 15.5 | `pure_MUL b a {High, Unsigned, Unsigned}` |
| probe_mulhsu | c, `mulhsu` | CERTIFIED | 15.4 | `pure_MUL a b {High, Signed, Unsigned}` |
| c_op_185 | c, `czero.*` | REFUSED | | no certified pure form for `ZICOND_RTYPE` (a monadic `let`) |
| c_op_105, c_op_106 | c | REFUSED | | a word the decoder calls `ILLEGAL` on the pruned module set |
| mulh_*, mulhsu_* (rv9 renders) | c | REFUSED | | 125–126 instructions, above the walk's bound of 64 |

Wall 63 s for the 11 certificates with four Lean jobs at a time; the
decode of 19 distinct words 8.3 s; two register expressions evaluated
2.9 s.

The certificate of `probe_mul` (c.mul, a compressed instruction that
re-dispatches to `MUL`), its statement and the head of its proof, wrapped
at 72 columns for this page:

```
theorem meaning_probe_mul (s : St) (a : BitVec 64) (b : BitVec 64)
    (h10 : s.regs.get? .x10 = some a) (h11 : s.regs.get? .x11 = some b)
    (hk0 : ∀ {α : Type} (x0 : α) (s : St),
        (plat_term_write x0) s = EStateM.Result.ok () s)
    (hk1 : ∀ (x0 : Arch.pa) (x1 : Nat) (s : St),
        (load_reservation x0 x1) s = EStateM.Result.ok () s)
    (hk2 : ∀ (x0 : Unit) (s : St),
        (cancel_reservation x0) s = EStateM.Result.ok () s) :
    runsTo (walk [LeanIM.instruction.C_MUL
              (LeanIM.cregidx.Cregidx 0x2#3, LeanIM.cregidx.Cregidx 0x3#3)]) s
      ((pure_MUL (a) (b) ({ result_part := Low,
                            signed_rs1 := Signed, signed_rs2 := Signed })))
    := by
  simp (config := {decide := true}) [runsTo, walk, step, execute,
    strip_C_MUL, strip_MUL, alias_C_MUL,
    rX_bits, rX, wX_bits, wX, regval_from_reg, regval_into_reg,
    PreSail.readReg, PreSail.writeReg,
    RETIRE_SUCCESS, reg_name_forwards, to_bits, zero_reg,
    <the 22 emitted callbacks, unfolded>,
    <the 25 emitted definitions reachable from the walked clauses and
     the register-index definitions: creg2reg_idx, zero_extend,
     regval_from_reg, xlenbits, zeros, ...>,
    Sail.BitVec.extractLsb, Sail.BitVec.zeroExtend, Sail.BitVec.truncate,
    bind, pure, get, getThe, modify, modifyGet, set, throw,
    EStateM.bind, EStateM.pure, EStateM.get, EStateM.set,
    EStateM.modifyGet, EStateM.throw, EStateM.instMonad,
    EStateM.instMonadStateOf, MonadStateOf.get, MonadStateOf.set,
    MonadStateOf.modifyGet, MonadState.get, MonadState.set,
    MonadState.modifyGet, BitVec.toNatInt,
    Std.ExtDHashMap.get?_insert_self, Std.ExtDHashMap.get?_insert,
    h10, h11, hk0, hk1, hk2]
```

`walk` runs the model's own `execute` on each decoded instruction (an
`ExecuteAs` re-dispatches once); `runsTo` reads register `x10` of the
state that results. The three `hk` hypotheses say the platform's three
support axioms (`plat_term_write`, `load_reservation`,
`cancel_reservation`, left abstract by the emit) change nothing.

## 5. equals: the handful, closing run (`equals_handful_all_v10`)

Candidates per unit: every certified straight clause reading two
registers, every value of its enumerated operation (52). The unit's own
walked clauses are tried first, its own text first among them; the first
proof stops (`EQUALS_ALL=1` runs the cross-product; lane `lp3_l19` did,
§5.1).

| unit | proposal | definition found | operation | stage | s |
|---|---|---|---|---|---|
| go_op_312 | `pure_RTYPE a b ADD` | RTYPE | ADD | same text (`rfl`) | 1.3 |
| c_op_174 | `pure_MULW b a` | MULW | | **integer level (`grind`)** | 2.4 |
| c_op_714 | `pure_RTYPEW a b SRAW` | RTYPEW | SRAW | same text | 1.1 |
| c_op_726 | `pure_RTYPE a b SRL` | RTYPE | SRL | same text | 1.3 |
| c_op_210 | `pure_DIVW a b false` | DIVW | false | same text | 1.1 |
| c_op_498 | `pure_RTYPE zero_reg (pure_RTYPE a b XOR) SLTU` | none of 52 | | all refuted by `bv_decide` | 4–7 each |
| c_op_102 | `pure_RTYPEW a b ADDW` | RTYPEW | ADDW | same text | 1.1 |
| probe_mul | `pure_MUL a b {Low,S,S}` | MUL | Low, Signed, Signed | same text | 1.1 |
| probe_mulh | `pure_MUL b a {High,S,S}` | MUL | High, Signed, Signed | **integer level** | 2.3 |
| probe_mulhu | `pure_MUL b a {High,U,U}` | MUL | High, Unsigned, Unsigned | **integer level** | 2.3 |
| probe_mulhsu | `pure_MUL a b {High,S,U}` | MUL | High, Signed, Unsigned | same text | 1.1 |

The multiply-high equality, literal (the compiler put the operands the
other way round; the definition is Sail's, its helper unfolded by the
rule of §6.3):

```
theorem probe_mulh__MUL_00_integer_level (a : BitVec 64) (b : BitVec 64) :
    ((pure_MUL (b) (a) ({ result_part := LeanIM.VectorHalf.High,
                          signed_rs1 := LeanIM.Signedness.Signed,
                          signed_rs2 := LeanIM.Signedness.Signed })))
    = (pure_MUL (a) (b) ({ result_part := VectorHalf.High,
                           signed_rs1 := Signedness.Signed,
                           signed_rs2 := Signedness.Signed })) := by
  try simp only [pure_MUL, pure_MUL, mult_to_bits_half, xlen,
                 to_bits_truncate, Sail.BitVec.extractLsb]
  grind
```

`pure_MUL` is the stripped form of Sail's `execute (MUL ...)`:
`mult_to_bits_half (l := xlen) mul_op.signed_rs1 mul_op.signed_rs2
rs1_bits rs2_bits mul_op.result_part`. Nothing here was typed for
multiplication.

### 5.1 the cross-product (lane `lp3_l19`, v5, every candidate tried)

Seven certified units × 52 candidates × up to three stages, 2,649 s.
Each unit proved exactly its own definition and refuted the other 51
(each refutation reaching `bv_decide`, which returns a counterexample or
reports the goal outside its fragment). `c_op_174` (mulw with swapped
operands) proved at the integer level there too. `probe_mulh` and
`probe_mulhu` were undecided in v5 (`grind` failed with `pure_MUL` alone
unfolded); §6.3's rule is what decided them.

## 6. what stood between the first run and the closing run: four spellings that became rules

Every walk certificate of v5 left an unsolved goal. Reading the residual
goals (probe lanes `l18`, `l20`, `l24`, `l27`, each one Lean run on one
certificate) gave four repairs; each was first tried as a name and then
replaced by the rule that would have found the name.

| residual | first fix (a spelling) | the rule that replaced it |
|---|---|---|
| `reg_name_forwards (Regidx (to_bits 10))` unreduced | add `reg_name_forwards, to_bits, extractLsb, zero_reg` | 6.3 |
| `execute (alias_C_ADD ..)` stuck on the re-dispatch | add `alias_C_ADD` | 6.1: every alias definition the walk followed |
| `(creg2reg_idx (Cregidx 2#3)).1.toNat` unreduced | add `creg2reg_idx` | 6.2: every emitted definition whose result is a register index |
| `(zero_extend 10#4).toNat`, then `(Sail.BitVec.zeroExtend (10#4) 5).toNat` | add `zero_extend`, then `Sail.BitVec.zeroExtend` | 6.3 and 6.4 |

- **6.1 aliases.** A compressed instruction's clause is `ExecuteAs
  (RTYPE ...)`; the certificate needs the alias definition unfolded as
  well as its strip theorem. `walk.py` now lists `alias_<X>` for every
  alias it followed.
- **6.2 register indices.** `regidx_defs_of` scans the emit for every
  `def ... : regidx :=` (`creg2reg_idx`, `fregidx_to_regidx`, `ra`,
  `sp`, `t0`, `zreg`, `regidx_offset_range`) and unfolds them all.
- **6.3 reachable definitions.** `strip.emitted_defs` indexes every
  `def`/`abbrev` of the emit (4,750); `strip.reachable` walks the
  identifiers of a seed text transitively through that index. The
  walk's seed is its strip theorems (the pure forms excluded, so they
  stay opaque) and the register-index definitions; the dispatcher and
  its clauses are skipped (the strip theorems stand for them) and the
  callbacks are unfolded but not expanded (their name maps are large).
  25 names for c.mul. The equals stage seeds from the pure forms
  themselves, so Sail's arithmetic helpers open up to Lean's own
  operations before `grind` (that is what decided `mulh`).
- **6.4 library helpers.** `strip.library_refs` reads the `Sail.*`
  names the reachable definitions mention in their own text
  (`Sail.BitVec.zeroExtend`, `extractLsb`, `truncate`) and unfolds
  those too.

One over-reach on the way: seeding 6.3 from the whole certificate text
(pure forms and callbacks included) pulled 73 definitions in, among them
`mult_to_bits_half` and the CSR name maps, and every certificate then
timed out at `isDefEq` (lane `lp3_l25`, 44 s each). The pure forms are
the proposal's vocabulary and must stay opaque in the walk; they are
opened only in equals.

What remains spelled in the certificate: the monad plumbing
(`EStateM.*`, `MonadState*`, `bind`, `pure`, ...), the register-file
map's two lookup lemmas (`Std.ExtDHashMap.get?_insert*`), and
`PreSail.readReg`/`writeReg`, `rX_bits`/`wX_bits`/`rX`/`wX`,
`regval_from_reg`/`regval_into_reg`, `reg_name_forwards`, `to_bits`,
`zero_reg`. The first two groups are Lean's and lean-sail's, not the
model's; the last group is now also produced by 6.3 (it appears in the
reachable set) and the spelled copy is redundant, to be removed once
the corpus run confirms nothing else depends on the order.

## 7. pass A over the rendered corpus — PENDING (lane `lp3_l28`, stages 3–5)

The corpus: `Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64/`,
1,960 rendered sources: the same 255 cells for every language, 255 by
`native_first` and 235 by `all_constructed`, so 490 per language; one
arch-unit is compiled from each source, and the 490 is the render's
doing, not the languages' (log 279). `python3 -m leanpath corpus` lists
every source as a unit (no cell is selected by name), in four shards
walked concurrently, two Lean jobs each, on 8 cores / 31 GB.

Routes (all verified to emit riscv64 in the container, lane `lp3_l21`):

| language | route |
|---|---|
| c | `clang -std=c17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr` |
| cpp | `clang++ -std=c++17 -O1 --target=riscv64-linux-gnu --gcc-toolchain=/usr` |
| rust | `rustc --target riscv64gc-unknown-linux-gnu --crate-type lib --emit obj -C opt-level=1` (target std already installed) |
| go | `GOARCH=riscv64 GOOS=linux go build`, symbol `main.emu_<cell>` |

A resource bound, not a spelling: a unit above 64 instructions is refused
before decode (`WALK_MAX_WORDS`). The rv9 render of `mulh` is 125
instructions because the render spells sign extension as a 64-way OR of
shifted copies of the sign bit and clang at `-O1`/`-O2` keeps it (the
same file on the host: 176-byte frame, 14 spills); the four-instruction
`mulh` cell itself is one instruction and certifies (§4).

The walk stage returned while this was written (the equals stage and
the re-run of the failures, lane `lp3_l29`, still running):

| shard | languages, route | certified | failed | refused | of |
|---|---|---|---|---|---|
| 0 | c and go, all_constructed | 174 | 82 | 234 | 490 |
| 1 | c and go, native_first | 179 | 83 | 228 | 490 |
| 2 | cpp and rust, all_constructed | 256 | 98 | 136 | 490 |
| 3 | cpp and rust, native_first | 237 | 100 | 153 | 490 |
| all | | 846 | 363 | 751 | 1,960 |

Every one of the 363 failures is one syntax error: a unit whose carved
body has no instruction before its return (an identity on the answering
register, or a cell whose answer is a float register the walk does not
read) produced an empty simp list, `[..., execute, ,`. Repaired in
`walk_file` and synced; lane `lp3_l29` walks those 363 again and takes
the tallies over everything (§7.1, to follow).

The refusals so far (shard 1): 102 above the 64-instruction bound, 45
`JALR` (a call inside the body), 26 `ILLEGAL` (float words on the pruned
module set), 22 `C_NOP`, 21 `UTYPE` (`lui`/`auipc`, an effect the rule
does not model), 8 `LOAD`, 4 `ZICOND_RTYPE`.

Certified proposals are not only single opcodes; the walk composes
whatever the compiler emitted, for example (shard 1):

```
bge_gpr_gpr_same  (c)   pure_ITYPE (pure_RTYPE a b SLT) 0x001 XORI
bne_gpr_gpr_same  (c)   pure_RTYPE zero_reg (pure_RTYPE a b XOR) SLTU
lhu_gpr_gpr_imm   (go)  pure_SHIFTIOP (pure_SHIFTIOP a 0x30 SLLI) 0x30 SRLI
lwu_gpr_gpr_imm   (c)   pure_ZBA_RTYPEUW a zero_reg 0b00
mulhu_gpr_gpr_gpr (c)   pure_MUL b a {High, Unsigned, Unsigned}
```

Lane `lp3_l31` walked the 363 again with the repaired text: **all 363
certify** (1,559 s wall, four jobs), each as the identity on the
answering register (`runsTo (walk []) s a`), which is the meaning of a
cell like `and_gpr_gpr_same` (a & a) and says nothing about a cell
whose answer is a float register; the tallies count them apart. So the
walk over the corpus stands at **1,209 certified, 0 failed, 751 refused
of 1,960**.

The equals stage over the corpus took three attempts to be affordable
(§8): one Lean process per candidate and stage (lane `l28`, then `l30`
pooled) meant a composite unit with no same-text candidate paid 52 × 3
processes; lane `l32` batches round 1 (every candidate's same-text and
integer-level theorems) into ONE Lean file per unit and reads the
failing theorems back by line, then runs the fixed-width round
candidate by candidate within a 150 s budget per unit.

### 7.1 the walk over everything (lane `lp3_l31`'s tally)

| | units |
|---|---|
| CERTIFIED | 1,209 |
| of which the identity on the answering register (no instruction before the return) | 363 |
| REFUSED | 751 |
| FAILED | 0 |
| of | 1,960 |

| refusal | units |
|---|---|
| above the 64-instruction bound | 388 |
| `JALR`: a call inside the body | 84 |
| `ILLEGAL`: a word the pruned decoder has no module for (float) | 84 |
| `UTYPE`: `lui`/`auipc`, an effect the one rule does not model | 82 |
| `C_NOP` | 53 |
| a read's register not resolved by the decoder state | 22 |
| `ZICOND_RTYPE`: a monadic `let` in the clause | 22 |
| `LOAD`, `BTYPE` | 15 |
| a Go source that does not compile | 1 |

| language, route | certified | refused |
|---|---|---|
| c, all_constructed | 169 | 66 |
| c, native_first | 167 | 88 |
| cpp, all_constructed | 169 | 66 |
| cpp, native_first | 167 | 88 |
| go, all_constructed | 87 | 148 |
| go, native_first | 95 | 160 |
| rust, all_constructed | 185 | 50 |
| rust, native_first | 170 | 85 |

203 of the 861 cells have at least one certified unit. Go refuses most
because its bodies carry a call or a stack check the rule does not
model; the identity units are the ABI's doing (a `uint8_t` parameter
arrives zero-extended, so `lbu_gpr_gpr_8` compiles to a return).

The `all_constructed` route is where the walk earns its keep: the
render spells an operation from others, the compiler emits the chain,
and the walk composes and certifies the chain as it is, for example
`sub_gpr_gpr_gpr` (rust, all_constructed) or `add_gpr_gpr_gpr`
(constructed from xor, and, shifts). Whether such a chain equals a
single clause is the equals stage's question (§7.2).

### 7.2 equals over everything (lanes `lp3_l40` and `lp3_l47`)

The stage that ran, per certified unit: the same text over every
candidate in one Lean run (`with_reducible rfl`); then, if nothing
matched, one Lean run that evaluates the proposal and every candidate
on four input pairs and drops whatever differs (a filter; nothing is
ever accepted by evaluation); then the provers over the survivors only,
the integer level (`grind`) and the fixed width (`bv_decide`). Eight
processes, 48 minutes for the 846 walked units. The 363 identity units
have no candidate that is the identity; correct, and cheap.

| | units |
|---|---|
| walked units with a definition proved | 114 of 846 |
| by the same text | 76 (`RTYPE` 73, `MUL` 3) |
| at the integer level | 4 (`MUL`, the multiply-high with swapped operands) |
| at the fixed width (`bv_decide`), after §7.5 | 34 (`RTYPE` 12, `ZBB_EXTOP` 16, `RTYPEW` 6) |
| every candidate refuted by evaluation | 722 |
| survived the evaluation, no prover closed it | 10 |

Definitions proved, all told: `RTYPE` 85, `ZBB_EXTOP` 16, `MUL` 7,
`RTYPEW` 6. Of the 114, 22 are proved against a clause other than the
one the unit's own instructions were (the `lhu` cells: two shifts
proved equal to `ZBB_EXTOP ZEXTH`), 92 against their own.

Two honest readings of the 766 without a definition:

- **The candidate rule has a gap, and it is a rule to add, not a name.**
  204 of them are one instruction whose clause carries an immediate
  (`ITYPE`, `SHIFTIOP`, `ADDIW`, `ZBA_RTYPE`, ...): a candidate is a
  certified clause whose other parameters are enumerable, and an
  immediate is a `BitVec 12`, so the unit's own clause is never offered
  and the nine enumerable one-register clauses it does see are all
  refuted by evaluation. The rule to add: a parameter that is not
  enumerable is an unknown to solve, and the same evaluation that
  refutes candidates can solve it. The other 518 are composites (several
  clauses in the expression), every candidate refuted by evaluation:
  correct, they are no single opcode. Per language, per opcode and per
  unit, with totals: `Research/oracle/riscv/leanpath/tally_corpus_final.md`
  (2,000 lines, generated by `tally_corpus_final.py` beside it).
- **The 44 survivors were the constructed adders, shifts and
  zero-extensions, and they were the widening leaf of log 274 made
  concrete.** In lane `l40` `bv_decide` answered "potentially spurious
  counterexample" on every one: the goal still held terms it could not
  open. Lane `l43` read the atoms back: `shift_bits_left`,
  `shift_bits_right`, `Sail.BitVec.extractLsb`, the `+++` append. They
  are lean-sail's, and the emit calls the first two unqualified (`open
  Sail`), so the rule of §6.4, which read only `Sail.`-qualified names
  from the text, missed them. §7.5 is the repair; with it 34 of the 44
  close at the fixed width, the constructed adders among them.

A third reading is about cost rather than truth, and it is the one to
fix first (§7.3).

### 7.5 the widening rule, and what it closed (lanes `lp3_l43`–`lp3_l47`)

The rule as it now stands: `strip.library_index` reads lean-sail's own
sources under the proof project (`.lake/packages/Sail/Sail/*.lean`),
tracks their `namespace` lines, and indexes every `def`/`abbrev` by its
short name (137 of them; private ones excluded, they cannot be named);
`strip.library_refs` then unfolds, alongside the emitted definitions
reachable from a pure form, every library definition the pure form's
own text mentions, by its qualified name. Nothing in it is a spelling
of an operation.

With it, the zero-extension unit closes in five seconds, literal:

```
theorem lhu_gpr_gpr_16__reg_a0__go__all_constructed__ZBB_EXTOP_08_fixed_width
    (a : BitVec 64) :
    ((pure_SHIFTIOP ((pure_SHIFTIOP (a) ((0x30#6)) (SLLI))) ((0x30#6)) (SRLI)))
    = (pure_ZBB_EXTOP (a) (extop_zbb.ZEXTH)) := by
  try simp only [pure_SHIFTIOP, pure_ZBB_EXTOP, log2_xlen,
    shift_bits_right_arith, sign_extend, xlenbits, zero_extend, xlen,
    Sail.BitVec.toNatInt, Sail.BitVec.signExtend, Sail.BitVec.zeroExtend,
    Sail.BitVec.extractLsb, Sail.shift_bits_right, Sail.shift_bits_left]
  bv_decide
```

Two shifts by 48 are `zext.h`; Go emitted them for a `uint16`
parameter, Sail defines `ZEXTH`, and no name connected them.

The constructed adders (`add_gpr_gpr_gpr_64`, all_constructed, c, cpp
and rust: a term of 3,137 clause applications built from xor, and and
shifts) are proved equal to `RTYPE ADD` by `bv_decide` in 124 s each;
the constructed shifts (`sll`, `srl`, `sllw`, `srlw`) to `RTYPE SLL`,
`SRL` and `RTYPEW SLLW`, `SRLW` in 17–100 s.

The ten that remain are the constructed comparisons (`slt`, `sltu`,
and the `blt`/`bltu` branch-condition cells, rust, all_constructed)
against `RTYPE SLT`/`SLTU`: Sail's `<_s` and `<_u` are emitted as
comparisons of `BitVec.toInt`/`toNat` at the `Int` level, which
`bv_decide` cannot open. The next piece of the widening rule is the
rewrite of those to `BitVec.slt`/`ult`; it is a rule too (Lean core
carries the lemmas).

### 7.3 the shape of the expressions, measured

The definitions are small: of the 42 straight clauses, 31 have no branch
at all in their pure form; the rest carry one operation-typed `match`
that a concrete operation collapses before any prover sees it (`RTYPE`
has 10 arms, `ITYPE` 6, `ZBB_RTYPE` 9). Real value guards live only in
the division family: `DIV`, `DIVW`, `REM`, `REMW` chain three or four
two-way `if`s (signedness twice, divisor zero, signed overflow), of
which the signedness ones also collapse with a concrete operation,
leaving two guards and three leaves. Between guards sit a few
operations (median 3 over the segments, at most 22 in the branchless
SHA clauses).

The walked units have no branches at all (the walk refuses them) but
their terms are large: the compose step substitutes each register's
value into every later use, so a value used twice is copied twice, and
a 53-instruction constructed adder becomes a term of 3,137 clause
applications at nesting depth 92 (native units: median 1 application,
depth 2; constructed units: median 3, but a tenth of them above 600).
That duplication, not branching, is what `rfl`, `grind` and the
elaborator were paying for on the constructed units. The remedy is a
rule of the compose step: one `let` per instruction, so the term is
linear in the instruction count and shared values are shared.

the owner's proposal of enumerating the gated branches on both sides and
comparing returns under their guards is sound over these shapes and
cheap (at most two guards a side); it is what `split` followed by a
per-piece prover would do, and it would label a failure by the branch
that fails. It is the next stage to add to `LeanExpr.equals`, after the
`let` sharing.

### 7.4 what the equals stage cost to make affordable

Twenty lanes from `l28` to `l47`. One Lean process per candidate and
stage was many hours. One Lean file per unit holding every candidate's
theorems was still 100 seconds a unit, because `grind` on fifty false
goals is fifty times three seconds and heartbeat caps barely bite. The
evaluation filter is what settled it: 4 to 6 seconds a unit for the
filter, then the provers see one or two candidates. Two Lean facts
worth keeping: `rfl` on a large term unfolds it in the kernel for
minutes (`with_reducible rfl` is instant either way); refuting a false
goal costs as much as proving a true one, so refute by evaluation, not
by proof.

## 8. speed, measured

| step | measured |
|---|---|
| strip, 339 clauses, one Lean run each | 105 s wall |
| decode, 19 distinct words, one Lean run | 8.3 s |
| one walk certificate (one or two instructions) | 15–17 s (Lean import dominates) |
| 11 certificates, four jobs | 63 s wall |
| one equals stage that proves | 1.1–2.4 s |
| one equals stage that refutes (`bv_decide`) | 4–7 s; one `PACK` candidate 122 s |
| equals, 11 units, first proof stopping | 489 s (c_op_498 tried all 52 × 3) |
| the cross-product, 7 units × 52 × 3 | 2,649 s |

## 9. the churn table, checked against what ran

| thing | written once | never written |
|---|---|---|
| the one rule of strip; the walk; the three equals stages; the reachable/regidx/alias/library rules | yes | |
| any clause's pure form; any opcode's key; any register-index helper's name | | derived from the emit |
| the compile routes per language | yes (one line each) | |
| the corpus's units | | listed from the directory |
| the monad plumbing and the two map lemmas | yes (Lean's, lean-sail's) | |

## 10. two lists

Decided, recorded for audit:
- the certificate's simp set is derived by rules 6.1–6.4; the last
  spelled register-path names are redundant and go once the corpus run
  is in;
- pure forms stay opaque in the walk and open in equals;
- a 64-instruction bound before decode;
- the first proof stops equals; `EQUALS_ALL=1` for the cross-product.

Awaiting the owner:
- nothing structural. Next, in order: `let` sharing in compose (§7.3);
  the non-enumerable parameter as an unknown solved by evaluation
  (§7.2); the `Int`-level comparisons rewritten to `BitVec.slt`/`ult`
  for `bv_decide` (§7.5); the branch-enumeration stage (§7.3); then
  pass B and the two churn tests.
