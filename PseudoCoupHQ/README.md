# PseudoCoupHQ

The headquarters of the PseudoCoup line: the plan the projects sit
inside, the day-by-day record, and the research that proves what a
program can carry across languages. The line's aim is a hub, a
disciplined Python, into which every one of twelve languages can be
brought and out of which each can be regenerated with nothing lost.
The research here answers, with machine-checked proofs, which parts
of a program already carry.

## The flagship finding, 2026-09-12: what you can code with today, in every language

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
| float - | 32, 64 | yes | yes | yes | no | yes | 4 of 5 |
| float == != stored as a value | 32, 64 | yes | yes | yes | no | yes | 4 of 5 |
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
| `fa - fb`, `fa == fb` on go | undecided at the check | the same walk |
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
| `DevComms/` | the record: 275 numbered logs, one per day of work or per task, append-only; `LLM_communication_protocol.md` is the form every report takes |
| `Research/oracle/` | the arch-unit oracle: `arch_opcodes/` (the cells and level 0), `cross_construction/emulation/` (the emulations, certificates, constructions, Lean lemmas), `riscv/` (the RISC-V line and its primitives as gate netlists), `coverage/` (the banks and reach), `hub/` (the composed round trip) |
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
  K-framework x86-64 semantics, Lean, the compilers of the five
  languages (gcc, clang, rustc, go, swiftc), tree-sitter, and podman
  through the Airlock sandbox.

## License

OTU GREEN LICENSE FOR UNIVERSAL WORKS: the PDF at the root of this
repository is the license text.
