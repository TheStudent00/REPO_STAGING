# log 274 — the Lean proof path: Sail's own Lean output as the definition of every arch-opcode, a walk that is Sail's own step, and a prover that never names an instruction

Node: `hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/`,
created with this log).

Date: 2026-09-13, written by Fable in conversation with the owner, after the
launch of sl1 / rv9 / lx1 (`log_272`, `log_273`; the sl1 session was
lost mid-run and its route (a) probes stay under
`Research/oracle/riscv/sail_lifter/`). Every rendering below is labelled
**LITERAL** (the object, quoted, with its path) or **GLOSS** (a plain
reading beside a literal). Every lane named ran through
`bash $HOME/Programming/PUBLIC/Airlock/remote_lane.sh` on the tower or
through `PUBLIC/Airlock/up.sh` on the laptop; the lane
scripts of this session are in this session's scratchpad only, because
this was discussion, and are reproduced in §3.

---

## 0. In plain words, before anything else

the owner asked what Sail is, whether the definition of an instruction can be
pulled out of it by a program instead of a person, and why the line
needs a lifter at all if Sail already emits Lean. The answers, in the
order they arrived:

Sail is a programming language for writing down what a machine
instruction does, with its own compiler. The RISC-V model in it is the
definition of RISC-V, typed by the specification's authors, and nothing
analysed `div` to produce it. The sail compiler does not lower a clause
to a machine instruction; it lowers it to the operation the clause is
built around, on integers with no width, and truncates at the end. One
of its backends writes Lean, and the Lean it writes for `DIV` is on this
page (§2.3), produced this afternoon.

Given that, the lifter is not a separate thing to write. It is Sail's own
`execute` applied to each instruction of a compiled body in order, with
the registers left unknown. The reference file a person typed becomes
unnecessary. The prover is Lean: its automatic bit-vector prover where
the widths are fixed, its algebra where the definition's integer form
makes an identity trivial, and a small closed set of once-proved
theorems where a construction is built from narrower pieces.

the owner's criterion for the line, restated on 2026-09-13, is the test every
piece below is measured against: if the repo stops being edited and the
things it processes churn, the system regenerates everything by running.
The design here has three passes, none with a case for any opcode; under
a new compiler release or a new model commit, nobody writes anything.

---

## 1. The words, declared before use

`Sail`
- a language from the Cambridge REMS group for instruction-set
  definitions. The RISC-V model at
  `SOURCES/sail-riscv/model/` is a set of clauses, three
  per instruction: how it is encoded, what it does, how it is spelled.
- built: by people, by hand, as the specification. It is level 0 by
  ratification; nothing below it is checked against anything above it.

`the sail compiler`
- the program `sail` (0.20.2 in the image, `/opt/opam/default/bin/sail`;
  also in the laptop's image, built three days ago from the same
  Containerfile). It reads the model and writes it out in another form:
  a C simulator (`sail_riscv_sim`), Lean, Rocq, Isabelle, SMT.
- it never writes machine instructions. The `DIV` clause is not lowered
  to `div`; it is the meaning of `div`.

`our compiler`
- clang, rustc, go, swiftc: reads a language, writes machine
  instructions. `a / b` in c lowers to one `div`. A different level.

`arch_opcode`
- one machine instruction the compiler can write, keyed by mnemonic,
  operand form and width; its definition is one Sail `execute` clause.
- built: the key from the `mapping clause assembly` line; the definition
  from the clause, as Lean, with the register reads and the write
  stripped.

`arch_unit`
- the compiled machine code of one source operator at one type pair, cut
  out of the binary at its function symbol. A list of instructions.

`meaning of a unit` (the lifter, the owner's `build_unit_lean`)
- the unit as one expression: apply each instruction's definition in
  order, thread the registers, leave the inputs unknown.
- built: decode each word with Sail's own decoder (`encdec`, emitted),
  apply Sail's own `execute` (emitted), in Lean. A branch forks the walk;
  the two sides are joined under the branch condition.

`gate` (the owner's `prove_lean_equivalence`)
- the one yes/no question asked per emulation: does this compiled body
  compute the same function as the definition, for every input.

`sail_lean_primitives`
- the operations every definition bottoms out in, measured over the
  emit: `BitVec.toInt`, `BitVec.toNatInt`, `to_bits_truncate`,
  `Int.tdiv`, integer `+ - * ^`, comparisons, `extractLsb`, `if`. They
  are Lean's own `Int` and `BitVec` operations, not Sail-specific ones.

`widening`
- the rule that rewrites a width-free definition as fixed-width
  operations: every integer in it came from a register, so every
  intermediate is bounded; pick a width per node that provably loses
  nothing (a 64 by 64 product fits in 128 bits) and replace each
  integer operation by the bit-vector one at that width, citing Lean's
  library fact for the replacement.

`bit-blast`
- turn an equation between fixed-width expressions into a circuit of
  and, or, not gates and ask a SAT solver whether any input makes the
  sides differ. None, with the search exhausted, is the proof. Lean's
  tactic for it is `bv_decide`; z3 does the same inside `proved_equal`
  (`Research/oracle/cross_construction/emulation/handful/handful.py`
  lines 2356 to 2364, budget 3,000 ms).

`the swap table` (the owner's `lang_x_arch_unit_lean_primitives`)
- per language: which of its own compiled units computes each Sail
  primitive at each width. Filled by pass A (proof), never by hand.

`written once` / `never written`
- the owner's distinction, 2026-09-13: a person writing the algorithm that
  connects Lean expressions is different from a person wiring specific
  things by hand. The first resists churn; the second needs constant
  intervention. Everything in this design is sorted onto one side or
  the other in §6.

---

## 2. What Sail is, on the page

### 2.1 The definition of DIV, as its authors wrote it

**LITERAL**, `SOURCES/sail-riscv/model/extensions/M/mext_insts.sail`
lines 53 to 67 (commit `3243f93`, 2026-09-09):

```
function clause execute DIV(rs2, rs1, rd, is_unsigned) = {
  let rs1_bits = X(rs1);
  let rs2_bits = X(rs2);
  let rs1_int = if is_unsigned then unsigned(rs1_bits)
                else signed(rs1_bits);
  let rs2_int = if is_unsigned then unsigned(rs2_bits)
                else signed(rs2_bits);

  let quotient = if rs2_int == 0 then -1
                 else quot_round_zero(rs1_int, rs2_int);
  // Check for signed overflow.
  let quotient = if not(is_unsigned) & quotient >= 2 ^ (xlen - 1)
                 then negate(2 ^ (xlen - 1)) else quotient;
  X(rd) = to_bits_truncate(quotient);
  RETIRE_SUCCESS
}

mapping clause assembly = DIV(rs2, rs1, rd, is_unsigned)
  <-> "div" ^ maybe_u(is_unsigned) ^ spc() ^ reg_name(rd)
      ^ sep() ^ reg_name(rs1) ^ sep() ^ reg_name(rs2)
```

**GLOSS.** Read two registers as integers, signed or unsigned by the
flag. Divide by zero gives all ones. Signed most-negative over minus one
gives most-negative back. Truncate to the register width and write it.
The second clause says the same instruction is spelled `div` or `divu`
with three register names: this is where the machine-form key comes
from, and nobody types it.

### 2.2 What the sail compiler lowers the operation to, per backend

**LITERAL**, `/opt/opam/default/share/sail/lib/arith.sail` lines 170 to
175, inside the image:

```
/*! Truncating division (rounds towards zero) */
val tdiv_int = pure {
  coq: "Z.quot",
  lean: "Int.tdiv",
  _: "tdiv_int"
} : (int, int) -> int
```

**LITERAL**, the C runtime the simulator links,
`/opt/opam/default/share/sail/lib/sail.c` lines 459 to 462:

```
void tdiv_int(sail_int *rop, const sail_int op1, const sail_int op2)
{
  mpz_tdiv_q(*rop, op1, op2);
}
```

**GLOSS.** The C simulator computes `div` with GMP's big-integer
division, never with the host's `div` instruction. In Lean it is
`Int.tdiv`, in Rocq `Z.quot`. The width enters once, at
`to_bits_truncate`, after the mathematics is done.

### 2.3 The DIV clause as the Lean backend wrote it

**LITERAL**, `<runs>/sail0/agent/out/lean/LeanIM/InstsEnd.lean`
lines 4362 to 4383 (the tower; lane `sail0_l5_lean_I_insts_M_insts.sh`,
§3):

```
def execute_DIV (rs2 : regidx) (rs1 : regidx) (rd : regidx)
    (is_unsigned : Bool) : SailM ExecutionResult := do
  let rs1_bits ← do (rX_bits rs1)
  let rs2_bits ← do (rX_bits rs2)
  let rs1_int :=
    if (is_unsigned : Bool)
    then (BitVec.toNatInt rs1_bits)
    else (BitVec.toInt rs1_bits)
  let rs2_int :=
    if (is_unsigned : Bool)
    then (BitVec.toNatInt rs2_bits)
    else (BitVec.toInt rs2_bits)
  let quotient :=
    if ((rs2_int == 0) : Bool)
    then (Neg.neg 1)
    else (Int.tdiv rs1_int rs2_int)
  let quotient :=
    if (((not is_unsigned) && (quotient ≥b (2 ^i (xlen -i 1)))) : Bool)
    then (Neg.neg (2 ^i (xlen -i 1)))
    else quotient
  (wX_bits rd (to_bits_truncate (l := 64) quotient))
  (pure RETIRE_SUCCESS)
```

**GLOSS**, line against line with §2.1: `X(rs1)` became `rX_bits rs1`, a
register read. `signed` and `unsigned` became `BitVec.toInt` and
`BitVec.toNatInt`. `quot_round_zero` became `Int.tdiv`. The two `if`s are
unchanged. `to_bits_truncate (l := 64)` is, in `Prelude.lean` line 319,
`get_slice_int 64 n 0`: the low 64 bits. `SailM` is the wrapper carrying
the register file; the only lines that are not a plain expression are
the two reads and the one write. Strip them and the term of the cell
`div` at (register, register, register, 64) is:

```
to_bits_truncate 64
  (if b == 0 then -1
   else if signed && Int.tdiv a b >= 2^63 then -(2^63)
   else Int.tdiv a b)
where a = toInt rs1_bits, b = toInt rs2_bits
```

**LITERAL**, `Arithmetic.lean` lines 249 to 251 of the same output, the
helper every `MUL` family clause calls:

```
let result_wide := (to_bits_truncate (l := (2 *i l)) (rs1_int *i rs2_int))
match result_part with
| .High => (Sail.BitVec.extractLsb result_wide ((2 *i l) -i 1) l)
```

**GLOSS.** Multiply as integers, truncate to twice the width, and `mulh`
is the upper half. General in `l`; the width is a parameter, never a
case. This is the object `log_273` §3.6 named as the missing identity:
on c, c++ and rust the compiler rewrote the doubled-width product into
`mulh` plus a correction sum, so the lifted formula has a sum at its
root where the definition has an extract, and the equality is a 64-bit
multiplier identity no bit-blast decides. At the integer level both
sides are the same polynomial (§5.3).

### 2.4 The operator census, measured

Over the 13 extension folders the compilers target (I, M, A, F, D, C,
Zba, Zbb, Zbs, Zicond, Zbc, Zbkb, Zbkx), 63 execute clauses:

| kind | count | examples |
|---|---|---|
| operator symbols | about 20 | `+ - * & \| ^ @ == != << >>`, `<_s <_u` |
| control forms | 8 | `let if then else match foreach assert return` |
| helper functions called | 146 distinct | `sign_extend`, `zero_extend`, `signed`, `to_bits_truncate`, `quot_round_zero`, `X` |

Every helper is itself Sail, written out of the same operators; the Lean
backend inlines nothing but emits each as a Lean definition, so a reader
of the Lean output chases no helper: they are all there as functions.

---

## 3. The emit, measured

Five lanes, all this afternoon, all on instance `sail0`
(`PUBLIC/Airlock/instances/sail0.conf`, copied from
`o3.conf`, sizes stated in its header).

| lane | where | cap | modules handed to sail | result |
|---|---|---|---|---|
| l1 | laptop | 6 GB | cmake configure of the model | refused: the C emulator build fetches CLI11 from GitHub and the instance has no network |
| l2 | laptop | 6 GB | cmake target `generated_lean_rv64d` in the image's own configured clone `/opt/sail-riscv-src` | stopped by the OS at 6.1 GB after 7.5 min; `oom_kill 1` in the cgroup |
| l3 | laptop | 16 GB | the same | 16.5 GB flat, 93% CPU, nothing written after 22 min; stopped on the owner's word ("use the tower") |
| l4 | tower | 20 GB | `I M Zicsr postlude main` | 47.5 min, peak 17.0 GB, 55,873 lines in 116 files; NO execute clause for any I or M instruction |
| l5 | tower | 20 GB | `I_insts M_insts postlude main` | 45.5 min, 62,893 lines, 2.5 MB, 91 source files resolved; `BaseInsts.lean` and `MextInsts.lean` present; `execute_DIV` at `InstsEnd.lean:4362` |

Two facts a future lane must know:

- **Module names are leaf names.** `I` and `M` are groups in
  `SOURCES/sail-riscv/model/riscv.sail_project`; the
  instruction files are in the leaves `I_insts` (`requires exceptions,
  sys, I_types, Zicfilp_regs`) and `M_insts` (`requires sys, I,
  M_types`). `sail --list-files <modules> riscv.sail_project` resolves a
  selection in seconds; l5 checked it before emitting, l4 did not.
- **The emit is heavy and fixed in cost.** About 45 minutes and 17 GB
  for two extensions with the substrate they require. It runs once per
  model commit and is cached by that commit (`SailModel.definitions`,
  §4); it is never on a lane's critical path.

**LITERAL**, the sail invocation l5 used (working directory
`/opt/sail-riscv-src/model`, config
`/opt/sail-riscv-src/build/config/rv64d_v256_e64.json`, the flags copied
from `model/CMakeLists.txt` lines 413 to 480):

```
sail --strict-var --strict-bitvector --strict-exponentials \
  --memo-z3-path /work/smtcache --config $cfg --lean --memo-z3 \
  --lean-output-dir /work/leanout --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult \
  --lean-non-beq-type Step --lean-noncomputable \
  --lean-noncomputable-function encdec_forwards \
  --lean-noncomputable-function encdec_backwards \
  --lean-noncomputable-function encdec_forwards_matches \
  --lean-noncomputable-function encdec_backwards_matches \
  --lean-noncomputable-function encdec_compressed_forwards \
  --lean-noncomputable-function encdec_compressed_backwards \
  --lean-noncomputable-function encdec_compressed_forwards_matches \
  --lean-noncomputable-function encdec_compressed_backwards_matches \
  --lean-import-file ../handwritten_support/RiscvExtras.lean \
  -o Lean_IM I_insts M_insts postlude main riscv.sail_project
```

Housekeeping done on the way: two stale lines in the laptop's
`PUBLIC/Airlock/mounts.conf` (the sources folder had moved
to `SOURCES`, the graphs folder to
`LOCAL/PseudoCoupGraphs`) were corrected; both instances
are down; the Lean tree of l5 stays at
`<runs>/sail0/agent/out/lean/`.

---

## 4. The proof path, as classes

the owner's rough loop of 2026-09-13, rewritten with classes at his request,
with the updates of the later turns folded in. Every method body is a
rule over its inputs; none names an opcode. The plan node registers each
class and method under its own name (§7).

```python
class SailModel:
    commit                                  # the cache key
    def definitions(self) -> list[ArchOpcode]:
        # sail --lean over the leaf modules; ~45 min, ~17 GB;
        # once per commit, cached. One ArchOpcode per execute
        # clause; the key from the assembly clause.

class ArchOpcode:
    key                                     # (mnemonic, operand form, width)
    definition: LeanExpr                    # the execute clause, reads and
                                            #   the write stripped

class LeanExpr:
    def equals(self, other: LeanExpr) -> Proof | None:
        # 1. integer level: normalize both sides (ring); same
        #    polynomial, no circuit
        # 2. fixed width: widen, then Lean's bit-vector prover,
        #    with a budget
        # 3. width a variable: the once-proved theorem for this
        #    construction kind
    def widen(self) -> LeanExpr:
        # bounds from the inputs' widths; a width per node that
        # loses nothing; Lean's library fact per replacement
    def primitives(self) -> set[SailPrimitive]

class ArchUnit:                             # one compiled body
    language: Language
    source: str
    instructions: list[bytes]
    def meaning(self, defs: list[ArchOpcode]) -> LeanExpr:
        # decode each word with Sail's own decoder, apply its
        # definition, registers unknown; a branch forks the
        # walk and the sides join under the branch condition;
        # a load or store is on a named cell; a call attaches
        # the callee's body from the toolchain archive

class Language:
    name
    corpus: list[ArchUnit]                  # every unit its compiler made
    operator_for: dict[SailPrimitive, ArchUnit]   # filled by pass A
    def compile(self, source: str) -> ArchUnit    # invoke; cut the body out
    def render(self, e: LeanExpr) -> str:
        # walk e; at each primitive write the operator that
        # operator_for holds; where none exists at that width,
        # compose it from narrower ones (schoolbook, shift-subtract)

class Emulation:
    opcode: ArchOpcode
    language: Language
    unit: ArchUnit
    proof: Proof                            # the Lean theorem file

class Dictionary:
    entries: dict[(Language, ArchOpcode), Emulation]

class System:
    def run(self, model: SailModel, langs: list[Language]) -> Dictionary:
        defs = model.definitions()
        for lang in langs:
            for unit in lang.corpus:
                unit.lean = unit.meaning(defs)

        # pass A: find. What does each language already compute?
        for lang in langs:
            for unit in lang.corpus:
                for op in defs:
                    if p := op.definition.equals(unit.lean):
                        dictionary.add(Emulation(op, lang, unit, p))
                    for prim in op.definition.primitives():
                        if p := prim.expr.equals(unit.lean):
                            lang.operator_for[prim] = unit

        # pass B: build. Everything pass A did not find.
        for op in defs:
            for lang in langs:
                if (lang, op) not in dictionary:
                    unit = lang.compile(lang.render(op.definition))
                    unit.lean = unit.meaning(defs)
                    if p := op.definition.equals(unit.lean):
                        dictionary.add(Emulation(op, lang, unit, p))

        # pass C: units against units, across languages (the Hub)
        return dictionary
```

Pass A is "whoever gets there first" (the owner's ruling of 2026-09-10) done
by proof over the corpus rather than by rendering. Pass B is the
backstop. Both use the same two mechanisms, `meaning` and `equals`.
`operator_for` is the owner's swap table, an output of pass A, an input to no
one.

---

## 5. Lean against z3, and why the hard cells move

### 5.1 The two tools

| | z3 | Lean |
|---|---|---|
| what it is | an automatic solver: proved, differ with a counterexample, or budget out; no proof object | a proof checker; a claim holds when a proof is built and the kernel checks it; `bv_decide` does what z3 does and checks the SAT solver's certificate |
| where it is in the line | `proved_equal`, handful.py:2356, 3,000 ms | the schema lemmas, `Research/oracle/cross_construction/emulation/construct/lean/schema_add_w16_8_1.lean` and its siblings, proved by `bv_decide` |
| fixed width | fast | same engine, slower, certificate checked |
| 64-bit multiply and divide circuits | 30 to 3,000 s then out of memory (log_262) | `bv_decide` timed out at 16-bit multiply (log_262) |
| a theorem for every width, by induction | cannot state it | the only place it can live |

### 5.2 What Sail emitting Lean changes

The definition side of every RISC-V cell arrives in Lean with no reader
of ours between. Moving the gate to Lean means the meaning of a unit is
also a Lean expression (it is, by construction, §4), and the equality is
a Lean theorem: automatic where it closes, a once-proved lemma where it
does not. z3 may stay as a fast counterexample finder; it is no longer
the ground on which a certificate rests.

### 5.3 The expectation for `mulh`, not yet run

At fixed width the current line hands the prover a 128-bit multiplier
circuit on each side and waits (log_273 §3.6, measured at four budgets
and every width offered). Compared at Sail's integer level, before
widening, "high half of a*b" on the definition's side and the compiled
`(__int128)a*b >> 64` on c's side are the same integer expression, and
`mulh` plus a correction sum is the same polynomial rearranged, which
Lean's `ring` closes without a search. This is the first thing the
handful (§7) tries. Unverified until it runs.

### 5.4 The schoolbook identity, for the case a language lacks the width

```
(ah * 2^64 + al) * (bh * 2^64 + bl)
  = ah*bh * 2^128 + (ah*bl + al*bh) * 2^64 + al*bl
```

A polynomial identity; `ring` proves it for every width in one call.
What remains is the carry bookkeeping between the pieces at fixed width,
small. Division's shift-and-subtract loop needs an invariant proof by
induction, once. Hardware multipliers are verified this way because
bit-blasting them fails; the theorems are textbook and mention no
opcode.

With the swap table, this case may be empty for our five compiled
languages: c and c++ hold `__int128`, rust `u128`, go `bits.Mul64`, swift
`multipliedFullWidth`, so `render` never composes `mulh` from pieces for
them.

---

## 6. Written once, never written: the churn table

`written once`: part of the system, like the algorithm; mentions no
opcode, compiler or language version. `never written`: anything per
opcode, per compiler, per language release.

| what changes | what a person does |
|---|---|
| a compiler releases a new version | nothing; run; pass A re-proves, pass B rebuilds what moved |
| the Sail model changes a definition | nothing; the cache misses on the new commit, `definitions()` re-emits, everything downstream regenerates |
| a new language joins | nothing semantic; how to invoke its compiler and cut a body out, which is plumbing |
| Sail's own library gains a primitive that maps to a Lean function with no library facts | one bridge fact, once; no example is known, since Sail emits into Lean's own `Int` and `BitVec`, whose facts Lean's library carries |
| a language lacks an operation kind at a width, and the construction's theorem for that kind is not yet in the system | that theorem, once, general in width; a closed set the size of Sail's primitive vocabulary, about a dozen kinds, possibly empty for our five languages (§5.4) |

If either once-written theorem is wrong, nothing passes, because Lean
checks it: the system fails loudly rather than drifting.

### 6.1 The cycle check

What rests on what, top to bottom, with no arrow pointing back up:

- a dictionary entry rests on `equals`, which rests on Lean;
- both sides of that proof rest on `definitions()`, which rest on the
  sail compiler reading the model;
- the model is the ratified definition; the point check against the C
  simulator catches only a backend bug, since both come from one text.

An emulation is never proved against itself: its meaning comes from the
definitions of the instructions the compiler chose, and the definition
it is proved against comes from the model directly. The only way to
close a loop would be to let a proved emulation feed a definition, and
nothing in the three passes does that.

---

## 7. What happens next, in the owner's order

1. This log: banked.
2. The plan: node `lean_proof_path` under the riscv64 node, one sub-node
   per class of §4, one leaf per method, designations `code (class)`
   and `code (method)`, so the plan and the code share names
   (`plan_and_code.md` §1). Registered and generated with
   `generate_nodes.py`, checked with `check_plans.py`.
3. The handful: the artifact folder `Research/oracle/riscv/leanpath/`,
   one instance, lanes on the tower. First `definitions()` for the
   `I_insts M_insts` selection (or the cached l5 tree), then `meaning`
   over ten carved units from rv1's handful, then `equals` on those
   ten, `mulh` on c among them, then pass A over the rv6 corpus of 255
   cells on c, c++, rust, go.
4. Everything: the full selection of extensions the compilers target,
   every cell, every language, pass B for what pass A misses, the
   regeneration test, and the churn test (re-run on the same inputs,
   byte-identical dictionary or the diff named).

### 7.1 Speed, expected and to be measured

| step | cost | how often |
|---|---|---|
| `definitions()` | 45 min, 17 GB (measured, l5) | once per model commit |
| `meaning` per unit | Lean elaboration of a few unfoldings; seconds expected | once per unit per definitions commit |
| `equals` at integer level or by `bv_decide` on add, shift, logic, compare | under a second expected (log_262: 246 places by `bv_decide`) | per (unit, cell) pair |
| `equals` on multiply and divide by circuit | the known wall; avoided by §5.3 | |
| a full pass A over 255 cells by 4 languages | about 1,000 questions; an hour is the expectation | per run |

Unverified until the handful runs; the handful exists to measure it.

---

## 8. Two lists

### Decided, recorded for audit

- The words of §1 are the line's names for this path; the glossary
  gains entries for `meaning of a unit`, `widening`, `bit-blast`, `the
  swap table`, `written once`.
- The plan node is created at level 5 under riscv64 as
  `node_0_3_2_3_1_3_lean_proof_path`, with class and method sub-nodes
  named as in §4; it supersedes nothing yet, and `lifter_from_sail`
  (sl1) stays registered with a PROGRESS entry pointing here.
- The emit is cached by model commit and run on the tower; module names
  handed to sail are leaf names, checked with `--list-files` first.
- Two mount lines in the laptop's `mounts.conf` corrected (instance
  state, gitignored).

### Awaiting the owner

- Whether the RISC-V gate moves from z3 to Lean, taking Sail's Lean
  output as the definition side; the bank's certificates on RISC-V and
  the owed width-general lemma rest on it. This log and the plan assume
  yes, as the conversation of 2026-09-13 did; the handful is built on
  it.
- The node's name, `lean_proof_path`, chosen by Fable from the owner's phrase
  "a proof path that has high resistance to churn"; rename on his word.
