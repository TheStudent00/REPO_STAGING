# PseudoCoupHQ

The headquarters of the PseudoCoup line: the plan the projects sit
inside, the day-by-day record, and the research that proves what a
program can carry across languages. The line's aim is a hub, a
disciplined Python, into which every one of twelve languages can be
brought and out of which each can be regenerated with nothing lost.
The research here answers, with machine-checked proofs, which parts
of a program already carry.

## The flagship finding, 2026-09-17: the whole chain in Lean, machine-checked

The line from a language's operator down to the machine's own definition
is one loop with five steps. Each step is a number, and the numbers are
measured, not asserted.

```python
# 1.1  every RISC-V instruction, in Lean, from the Sail model
arch_opcode_leans = {}
for arch_opcode in sail_riscv_model:
    arch_opcode_leans[arch_opcode] = get_sail_def(arch_opcode, output="Lean")

# 1.2  the float primitives, which Sail leaves as axioms, given bodies
for arch_opcode in arch_opcode_leans:
    arch_opcode_leans[arch_opcode] = gmp_slice_insertion(arch_opcode_leans[arch_opcode])

# 2  every language's compiler-operators, lowered to arch-units, in Lean
for lang in langs:
    for compiler_operator in lang.compiler_operators:
        arch_unit = lower(compiler_operator)              # compile for RISC-V
        arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
        arch_unit.kinds = discover_kinds(arch_unit.lean)  # read off the Lean

# 3  the primitives: which arch-units equal which pieces of Sail's definitions
sail_lean_primitives = pieces_of(arch_opcode_leans)       # a + b, a xor b, ...
for lang in langs:
    for primitive in sail_lean_primitives:
        for arch_unit in lang.arch_units:
            if prove_lean_equivalence(primitive, arch_unit.lean):
                lang.arch_unit_lean_primitives[primitive] = arch_unit

# 4  every arch-opcode emulated in every language, from those primitives only
for lang in langs:
    for arch_opcode, definition in arch_opcode_leans.items():
        emulation = build_emulation(definition, lang.arch_unit_lean_primitives)
        arch_unit = lower(emulation)
        arch_unit.lean = build_unit_lean(arch_unit, arch_opcode_leans)
        emulation.proven = prove_lean_equivalence(definition, arch_unit.lean)

# 5  any language's arch-unit expressed in any other language's
for lang_i in langs:
    for lang_j in langs:
        for arch_unit_i in lang_i.arch_units:
            for arch_unit_j in lang_j.arch_units:
                if prove_lean_equivalence(arch_unit_i.lean, arch_unit_j.lean):
                    equivalents.add(arch_unit_i, arch_unit_j)
```

| step | | complete |
|---|---|---|
| 1.1 | 1038 of 1038 arch-opcodes are full-body Lean | **100%** |
| 1.2 | 67 of 67 float axioms given a body | **100%** |
| 2 | 1612 of 2364 arch-units are full-body Lean | **68%** |
| 3 | | 0% |
| 4 | artifacts yes, this proof no | 0% |
| 5 | | 0% |

### 1.1 — the model was already whole

The Sail RISC-V model emitted to Lean has a body for **every** instruction:
354 `execute_*` clauses, no `sorry`, covering 1038 arch-opcodes because one
clause covers a whole dispatch enum. `execute_ITYPE` is one clause and six
arch-opcodes.

### 1.2 — the 67 axioms now have bodies

Sail declares all 67 floating-point externals with a type and no body, so
Lean, Rocq, Isabelle and SMT all had the same hole. They are now definitions,
walked from the flattened Berkeley SoftFloat slices over 24 primitive integer
operations. Nothing was written by hand and no float definition was assumed.

| | |
|---|---|
| axioms given a body | 67 of 67 |
| IR instructions walked into Lean | 111,562 |
| Lean generated | 114,713 lines, 68 modules |
| `lake build` of the whole model | 204 jobs, 0 errors |
| `#print axioms riscv_f64Add` | `[propext, Quot.sound]` — Lean's own two |
| `axiom` left in the model | 8, all platform hooks, none float |

### 2 — an arch-unit is its arch-opcodes, composed

An arch-unit is a compiler-operator lowered to machine instructions. Every
one of those instructions already has a Lean body, so the unit's Lean is
those bodies in order with the unit's own operands:

```lean
-- c/op_0, which is C's `!` on int32_t
noncomputable def unit_c_op_0 : SailM ExecutionResult := do
  let _ ← execute_ITYPE (0x001#12) (regidx.Regidx 0x0a#5) (regidx.Regidx 0x0a#5) (.SLTIU)
  pure (execute_C_JR (regidx.Regidx 0x01#5))
```

Which clause, and which operand is which argument, is read out of the model's
own `assembly_forwards` clause — the same clause that names the mnemonic. Sail's
decoder is never run: it is `noncomputable` in the proof emit, and it is not
needed, because the disassembly already names the instruction.

| language | arch-units on riscv64 | full-body Lean |
|---|---|---|
| c++ | 770 of 770 | **770** |
| c | 610 of 610 | **610** |
| rust | 125 of 125 | **125** |
| go | 107 of 107 | **107** |

Every compiled language is complete. Lean typechecks all 1612;
`lake build Units`: 4 modules, 0 errors.

### What is left, and exactly what each piece is

The last three gaps in the compiled languages were all flags, and all three
are closed: c++'s ship flags said `-std=c++17` while `<=>` is C++20; the
lifter's assembler targeted a march string without `zcb` or `zfa`; and `fli`
prints its constant as a value where the model spells it as an index, which
the model's own FLI table inverts.

What is left is 752 units in eight languages, and one dictionary —
`COMPILE` in `Research/oracle/riscv/riscv_carve.py` — which holds a compile
rule for c, c++, rust and go and nothing else.

| language | units | route |
|---|---|---|
| csharp | 253 | .NET 9 NativeAOT, if it has a riscv64 runtime identifier |
| javascript | 240 | the interpreter binary |
| swift | 167 | swiftc targeting riscv64 |
| dart | 82 | AOT, and `gen_snapshot` is built per target |
| php, ruby, java, cpython | 10 | the interpreter binary |

For the interpreted languages the arch-unit lives in the **interpreter
binary** — the same route already proven on Berkeley SoftFloat: compile for
riscv64, link the transitive helpers, internalize, inline, dead-code
eliminate, until one function per operation is left. `riscv64-linux-gnu-gcc`
is already in the image, so the C interpreters cross-compile directly.

The step-by-step record is `DevComms/log_287_project_communication_template.md`.

## The 2026-09-16 finding: every arch-unit emulated across four languages

Every readable RISC-V arch-unit — a compiler-operator lowered to machine
instructions — is now computed in c, c++, rust and go using integer
operators alone, including all the floating-point ones. **474 of 474.**

This is the inter-language connection demonstrated end to end: what one
language's compiler emitted, the other three reproduce exactly, and the
answer is checked against each language's own native operator rather
than against our own machinery.

| | comparisons | mismatches |
|---|---|---|
| each arch-unit against its own language's operator | 589,317,696 | **0** |
| cross-language, byte for byte | 446,526,000 | **0** |

The generated code was disassembled and checked: **no float instruction
and no vector register anywhere**, in any language. A double division is
computed from shifts, masks and integer arithmetic.

### What made it possible: the floats had no definition anywhere

RISC-V's floating-point instructions had no meaning in any formal
backend. The Sail model declares all 67 of them external with no body,
so Lean, Rocq, Isabelle and SMT all have the same hole; the C simulator
works only because it links a library. Until this was solved, every
float arch-unit was a dead end.

The method, and it names no instruction anywhere:

1. **Find where the logic actually lives.** Follow Sail's C backend
   down: integers land in GMP, floats in Berkeley SoftFloat, which the
   model already vendors. Both are ordinary integer C.
2. **Slice.** Compile the operation for riscv64, link only what it
   reaches, make everything else internal, then inline and delete what
   is unreachable. One function per operation.
3. **Specialise to the caller.** Sail fixes the rounding mode and clears
   the exception flags at every call. Pinning those deletes the dead
   arms and, with them, every computed jump. 15% smaller, and a whole
   class of obstacle disappears rather than being worked around.
4. **Flatten.** With no loops, no calls and no memory left, the control
   flow graph is acyclic, so every branch becomes arithmetic:
   `(a & mask) | (b & ~mask)`. One basic block, no jumps.
5. **Emit and compose.** Print that block as source in each language,
   then compose the arch-unit's instructions from those pieces.

Each step is mechanical. No person wrote a definition, and no step
knows the name of any instruction.

### The fourth guarantee

- **EMULATED.** The operation is computed in every language from
  integer operators alone, checked against that language's own operator
  and against the other three. The inter-language connection is
  demonstrated; it is **primed for proof, not lacking it**. The proofs
  are the work in front of us, and the shape is already in place: a
  float operation's Lean expression is derived by the same machinery
  that proves the integer ones, and stands at 21 of 43 today, blocked on
  a Lean kernel limit rather than on anything about floats.

### Six places where "the same operator" means different things

Found by machine, not by argument, and each one a portability fact the
line needs:

| what | where |
|---|---|
| a NaN's sign and payload are unspecified in C and go; RISC-V pins the canonical quiet NaN, x86 does something else | 92 of 174 float units |
| C's division is undefined at a zero divisor and at the most negative over minus one; the host faults | 32 units |
| clang folds `a / (bool)b` into the identity, so at zero the answer is `a`, not all ones | 8 units |
| go panics where RISC-V does not | 18 units |
| RISC-V's shift takes the low bits of the count; go gives zero; C is undefined | 18 units |
| go leaves a 32-bit answer non-canonical in the register | 6 units |

Any round trip claiming bit-exactness must pin these deliberately or
exclude them.

### What the probe generator did not reach

737 of the 1,244 arch-units have no body at all. The probe asked each
compiler for `a OP b` in that compiler's own syntax and the compiler
refused the spelling: go will not implicitly add an `int32` to an
`int64`, and c will not apply `%` to two doubles.

A refusal is not an operation without meaning, and this is the case the
line exists for — an operator one language has, carried into a language
that lacks it. Sorted by what was actually refused, **691 of the 737 are
buildable from pieces already in the corpus**: widen-then-operate for the
216 mixed integer widths, convert-then-operate for the 342 mixed
int-and-float, and either the bit-pattern or the float-semantic reading
for the 98 integer operators applied to floats. Only 46 are not runtime
operations at all — `alignof` is a property of a type, and unary `*`,
`&` and `<-` on a non-pointer compute no value.

Those 691 are open work, not a closed exclusion. Reaching them needs a
second probe form: one that asks for the emulation rather than for the
spelling the compiler rejects.

The record: `DevComms/log_293_below_sail_gmp_softfloat_and_the_float_gap_sized.md`.
The emulations, the slices and the tooling:
`Research/oracle/riscv/softfloat_slices/`.

## The 2026-09-12 finding: what you can code with today, in every language

Fixed-width integers and floats; every arithmetic, logic, shift and
compare operator in the vocabulary table below; assignment; a compare
stored as a value; a select (`a if c else b`); `if` / `elif` / `else`;
`while` and counted `for` loops; functions with calls, early return
and recursion; records with fixed-width fields. The expressions are
proved on all five compiled languages (c, c++, rust, go, swift). The
control constructs are the same construct in every language and
round-trip today through all twelve, but their branches are not yet
proved on the machine body. Not yet at all: signed divide and
remainder outside c and c++, float subtraction and float equality on
go, sign extension into swift, 80-bit floats outside c and c++,
closures, generators, virtual dispatch, growing containers.

**Superseded in part, 2026-09-16.** The float exclusions above were
about a language lacking a native operator that lowers. Every one of
them is now EMULATED: computed from integer operators in c, c++, rust
and go, and tested. They are no longer refusals, they are unproved.
The section above is the current statement; this one is kept because
its proof counts still stand and nothing here has been un-proved.

### The three guarantees a line can carry

- **PROVED, N of 5.** The line's operator lowers to arch-opcodes whose
  emulation in N of the five compiled languages z3 confirmed equal to
  the machine definition for every input. The round trip closes on
  the certificates alone.
- **STRUCTURAL.** The construct is the same construct in every
  target: an `if` is an `if`, a `while` a `while`, a call a call. The
  target's own compiler emits its branch and call instructions.
  Verified by the twelve-language round trip on the quick-fox program
  (identical output through every language); not yet proved by z3 on
  the machine body, because the walk reads a body in text order and a
  compare feeding a branch writes flags only. Both are owed.
- **NOT YET.** Refused at some language; the cause and the opener are
  in the table of exclusions.

### The program, every line marked

```python
def mix(h: int, x: int) -> int:         # STRUCTURAL: call, return
    h = (h ^ x) & 0xFFFFFFFF            # PROVED 5 of 5: xor, and
    h = (h + (h << 5)) & 0xFFFFFFFF     # PROVED 5 of 5: shl, add
    return h                            # STRUCTURAL: return

def checksum(xs: list[int], n: int) -> int:
    h: int = 2166136261                 # PROVED 5 of 5: constant
    for i in range(n):                  # STRUCTURAL: counted loop
        v: int = xs[i]                  # PROVED 5 of 5: load
        v = -v if v < 0 else v          # PROVED 5 of 5: compare as a
                                        #   value, negate, select
        h = mix(h, v)                   # STRUCTURAL: call; arguments
                                        #   arrive under the contract
    return h

def sign(v: int) -> int:
    if v < 0:                           # STRUCTURAL: if / elif / else
        return -1                       #   with three early returns
    elif v == 0:
        return 0
    else:
        return 1

def fact(n: int) -> int:
    if n <= 1:                          # STRUCTURAL: if, early return
        return 1
    return n * fact(n - 1)              # PROVED 5 of 5: sub, signed
                                        #   mul; STRUCTURAL: recursion

def mean(xs: list[float], n: int) -> float:
    s: float = 0.0                      # PROVED 5 of 5: constant
    i: int = 0
    while i < n:                        # STRUCTURAL: while; its test
        s = s + xs[i]                   #   feeds a branch
        i = i + 1                       # PROVED 5 of 5: fadd, add
    return s / float(n)                 # PROVED 5 of 5: cvt, fdiv
```

Lines you would have to change today:

```python
q = a // b            # 2 of 5 (c, c++), and only in the machine's
                      #   truncating form; Python's floor form is
                      #   one compare and adjust on top, both proved
r = a % b             # 2 of 5 (c, c++): the same cell as divide
d = fa - fb           # 4 of 5: go refused
e = fa == fb          # 4 of 5: go refused
y = int64(int32(x))   # 4 of 5: swift refused (sign-extend 32 -> 64)
```

### The expression vocabulary, x86-64, destination reading

| operator, as written | widths | c | c++ | rust | go | swift | languages |
|---|---|---|---|---|---|---|---|
| integer + and - | 8, 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| + with carry, - with borrow | 64 (borrow also 8) | yes | yes | yes | yes | yes | 5 of 5; borrow at 32 is 4 of 5 (rust no) |
| negate | 8, 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| & \| ^ ~ | 8, 32, 64 (~ also 16) | yes | yes | yes | yes | yes | 5 of 5 |
| << >> arithmetic and logical, by constant and by count; double-word shifts | 8, 16, 32, 64; double-word 64 | yes | yes | yes | yes | yes | 5 of 5 |
| signed * | 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5; at 8 it is 1 of 5 (go) |
| unsigned widening * | 8, 16, 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| select `a if c else b`, the attested conditions | 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| compare stored as a value | 8-bit answer | yes | yes | yes | yes | 12 of 15 conditions | 5 of 5 on 12 conditions; overflow and parity 4 of 5 |
| constants, moves, loads | 8 to 64 | yes | yes | yes | yes | yes | 5 of 5 |
| address arithmetic | 64 | register form yes; memory form no | same | yes | yes | yes | 5 of 5 register form; 3 of 5 memory form |
| zero-extend 8, 16 -> 32 | 32 | yes | yes | yes | yes | yes | 5 of 5 |
| sign-extend 32 -> 64 and 8 -> 64 | 64 | yes | yes | yes | yes | no | 4 of 5 |
| sign-extend 8, 16 -> 32 | 32 | no | no | no | yes | no | 1 of 5 |
| float + * / | 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| float - | 32, 64 | yes | yes | yes | no (EMULATED) | yes | 4 of 5 proved, 5 of 5 emulated |
| float == != stored as a value | 32, 64 | yes | yes | yes | no (EMULATED) | yes | 4 of 5 proved, 5 of 5 emulated |
| int -> float, float -> double, moves between int and float registers | 32, 64 | yes | yes | yes | yes | yes | 5 of 5 |
| 128-bit register logic, moves, unpack, extract | 128 | yes | yes | yes | yes | yes | 5 of 5 (register forms only) |
| signed / and % | 32, 64 | yes | yes | no | no | no | 2 of 5; at 8, 16 it is 0 of 5 |
| unsigned / and % | 8 to 64 | no | no | no | no | no | 0 of 5 |
| 80-bit long double | 80 | yes | yes | no | no | no | 2 of 5 |
| compare feeding a branch; float compare feeding a branch; push | | no | no | no | no | no | 0 of 5: flags or stack, no answer register; these are structural |

### Outside today, with cause and opener

| you cannot write, or not yet | why | what opens it |
|---|---|---|
| `a // b`, `a % b` on rust, go, swift | the divide check runs out; go's own zero check | branch-following walk; divide lemma |
| `fa - fb`, `fa == fb` on go | undecided at the check | **OPENED 2026-09-16: EMULATED** from integer operators and tested; the proof is what remains |
| `int64(int32(x))` on swift | the widening move refused at arrival | arrival contract, the convertible verdict |
| long double outside c, c++ | no holder | the x87 arrival as two words |
| a condition proved as the branch it feeds | flags only, no answer register | the flags-consumer contract |
| try/except, classes with methods, lists, dicts, strings | carried by the round trip today; nothing proved at the machine level: runtime library and dispatch, not operators | runtime-callee extraction |
| closures, generators, virtual dispatch, side effects that depend on evaluation order | discipline Forbid rows | nothing; write without them |
| a 128-bit value across a call | arrival refused | the calling convention as hub structure |

### How a line is carried

```
for stmt in program:
    if stmt is an assignment:
        for node in stmt.expression, leaves first:
            cell = arch_opcode_of(node.operator, node.widths)
            cert = bank[cell][target]        # PROVED, or the cause
        # a compare stored as a value, or a select, is such a node
    elif stmt is if / elif / while / for / return:
        emit target's own construct          # STRUCTURAL
        # its test is a compare feeding a branch: flags only, no
        # answer register; the flags-consumer contract is owed
    elif stmt is a call:
        emit target's own call               # STRUCTURAL
        for arg in stmt.args:
            verdict = arrival(arg.width)     # <= 64: identical or
                                             # convertible; 128, 80:
                                             # refused
```

## The numbers behind it

An arch-opcode is one machine instruction the compiler can write,
keyed by mnemonic, operand form and width. x86-64 holds 253 attested
ones; RISC-V 255. "Proved" means: source in that language, compiled
at shipping settings, read back into logic, and confirmed by z3 equal
to the machine's definition for every input. The definition is the
Sail model for RISC-V and, for x86-64, a reference checked against
the K-framework semantics. The destination reading proves the answer
register; the strict reading proves every written place, flags
included.

| language | x86-64, destination | x86-64, strict | of | RISC-V | of |
|---|---|---|---|---|---|
| c | 207 | 168 | 253 | 243 | 255 |
| c++ | 229 | 197 | 253 | 243 | 255 |
| rust | 176 | 138 | 253 | 247 | 255 |
| go | 164 | 119 | 253 | 241 | 255 |
| swift | 167 | 124 | 253 | no toolchain | 255 |
| on at least one compiled language | 233 | 201 | 253 | 251 | 255 |
| on every compiled language | 154 | 111 | 253 | 235 | 255 |

The seven interpreted languages (python, php, ruby, javascript, dart,
c#, java) have no machine body to check; they are tested beside the
definition at edge values and ordinary values, 162 of 253 agreeing on
all seven. Agreement is evidence, never proof, and is never counted
as one.

Followed upward to real compiled code: of the units the compilers
produced for c's operators, 4,578 of 10,367 are already expressible
in c out of proved pieces alone, and 3,504 of them in swift; rust
489 of 685 into every target; on RISC-V, c 351 of 369 and go 100 of
105. The blockers are structural, not arithmetic: a compare feeding a
branch, the stack, a widening move at a call. Each is named above
with the piece that opens it.

## How a proof is made

1. **The population.** Every operator of every compiled language at
   every type pair is compiled at shipping settings; each body is
   carved out at its symbol. The instructions those bodies use are
   reduced to one instance per (mnemonic, form, width): the cells.
2. **The definition.** Each cell's meaning is a z3 function from
   input bit-vectors to output bit-vectors (`Research/oracle/arch_opcodes/level0/`
   for x86-64, checked against the K-framework semantics;
   `Research/oracle/riscv/riscv_reference.py` for RISC-V, checked
   against the Sail model). A disagreement there is a defect in the
   reference, and level 0 is fixed before anything above it counts.
3. **The emulation.** For each cell and each language, source that
   should compute the cell. Three routes: the language's own operator
   (native); a construction from `& | ^ ~`, a conditional and
   variables (the backstop, `Research/oracle/cross_construction/emulation/construct/general/build.py`,
   with Lean lemmas under `construct/lean/`); and z3's own bit-blast
   circuits rendered as code (`bitblast.py` beside it).
4. **The check.** The emulation is compiled at shipping settings,
   carved, lifted to its z3 term, and z3 decides equality with the
   cell's definition. Equal means a certificate with the source, the
   flags, the term and the hashes; unequal or undecided is recorded
   with the cause, never dropped.
5. **The join.** `Research/oracle/coverage/build_join.py` joins every
   unit's cells with the per-(cell, language) certificates into the
   banks (`bank_x86.json`, `bank_riscv64.json`) and the reach
   matrices, which is what the tables above are read from.

Every run goes through the Airlock sandbox as a lane script kept in
the repository, and every number in a report names the log that
measured it.

## What lives here

| folder | what it holds |
|---|---|
| `Planning/` | the planning tree: `CORE_0.md` at the root; `node_0_3_research/` holds the research plan, and `node_0_3_2_arch_unit_oracle/` the arch-unit oracle whose results are above |
| `DevComms/` | the record: 275 numbered logs, one per day of work or per task, append-only; `comms_protocol.md` is the form every report takes |
| `Research/oracle/` | the arch-unit oracle: `arch_opcodes/` (the cells and level 0), `cross_construction/emulation/` (the emulations, certificates, constructions, Lean lemmas), `riscv/` (the RISC-V line, its primitives as gate netlists, and `softfloat_slices/`: the float operations sliced and flattened, and every arch-unit emulated in four languages), `coverage/` (the banks and reach), `hub/` (the composed round trip) |
| `Research/op_pipeline/` | the corpus: every operator of every language compiled, carved and manifested |
| `Research/briefs/` | the 37 task briefs, each the contract a run was executed under |
| `Research/GLOSSARY.md`, `Research/LAW.md` | every load-bearing word, defined before use; the rules every run obeys |
| `CLAUDE.md`, `AgentMemory.md` | what an agent must load before working here |

The logs that carry the finding above: `DevComms/log_271_what_you_can_code_with_today.md`
(the code-level statement), `log_270_autopoly_progress_report_2026-09-12.md`
(the numbers and the disciplines matrix), `log_266_task_cov1_how_far_the_proved_emulations_reach.md`
(the reach), `log_269_bb2_the_bit_blast_route_on_x86_and_the_interpreted_seven.md`
(the bit-blast route and the interpreted seven).

## Vocabulary

This line uses its own lexicon for structure: super-node, sub-node,
co-node, sub-tree, higher and lower; a process the operating system
stops is an ABORT. Every report defines each term where it is first
used. The glossary is the source.

## Credits

- **the owner (GitHub: <owner>)**: the vision of the hub, the ontology,
  the disciplines, every ruling, and the direction of every round. The
  research program is theirs.
- **Claude (Anthropic)**, a fundamental intelligence in this R&D:
  under the owner's direction it designed and ran the proof pipeline, wrote
  the reference simulators and their level-0 checks, the lifters, the
  backstop constructions and their Lean lemmas, the bit-blast route,
  the coverage joins, the briefs, the logs, the glossary, and this
  README. The generation at the time of this finding is Claude Fable
  5.1; earlier generations carried the line to that point.
- **Foundations relied on:** z3, the Sail RISC-V model, the
  K-framework x86-64 semantics, Lean, Berkeley SoftFloat and GMP (both
  reached through the Sail model's own C backend), the LLVM toolchain,
  the compilers of the five languages (gcc, clang, rustc, go, swiftc),
  tree-sitter, and podman through the Airlock sandbox.

### What is claimed, and what is used

The floating-point logic in the emulations is Berkeley SoftFloat's
algorithm, sliced and transformed; the integer arithmetic under Sail's
C backend is GMP's. Neither is ours and neither is claimed.

What is claimed is the method and what it produces: taking an
instruction's logic out of a reference implementation by machine,
specialising it to the context its caller fixes, flattening it to a
single branch-free expression, and composing those into arch-unit
emulation that carries unchanged across four languages — with no person
naming an instruction at any step. The pieces are prior art, in the
ordinary way that every program stands on its compiler. The combination,
and the inter-language connection it establishes, is the finding.

## License

OTU GREEN LICENSE FOR UNIVERSAL WORKS: the PDF at the root of this
repository is the license text.
