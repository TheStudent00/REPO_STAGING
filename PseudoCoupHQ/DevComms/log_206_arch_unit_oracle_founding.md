# log_206 — the arch_unit_oracle line: founding thoughts

This log belongs to the arch_unit_oracle line
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_8_arch_unit_oracle/CORE_0_3_8_arch_unit_oracle.md`),
forked 2026-09-05 from the operator-equivalence line. Written by the
coordinator (Fable) in answer to the owner's "thoughts?" on the three
objectives. Nothing here is measured unless marked measured; the
numbers quoted from the main line are as of 2026-09-05 and their
populations are named.

## 1. What each objective IS, in relation to what already exists

### 1.1 Compiling the compilers (compiler_units)

- **What it is:** the main line's pipeline with a different
  population. An arch-unit today is one operator's machine code,
  carved from a probe function's body. Here the body carved is a
  function of the compiler itself — clang's `SelectionDAGBuilder::visitAdd`,
  go's `ssagen`, php's `ZEND_ADD_SPEC` handler.
- **What already exists for it:**
    - The unit boundary rule (function body from symtab/DWARF) needs
      no change; a compiler is a binary with a symbol table.
    - The compiler graphs for go and clang already list every
      definition (1,859 and 10,789) and which of them emit machine
      instructions (57 and 251, task 95). Those emitter definitions
      are the natural first population: they are the functions whose
      arch-units, if provable, would state "this compiler function
      produces this opcode" as a theorem instead of a static
      detection.
    - The interpreter handlers (11 units, task 94/96) are already
      compiler_units in this sense; they moved to this node's
      population by definition, though the artifacts stay where they
      are.
- **The first fact it must measure, before anything else:** the
  term walk over the probe corpus puts 485 of 30,280 units in
  NO_TERM, and the largest cause (223 units, measured in task 99) is
  a callee body with a loop. A compiler's functions are mostly
  loops. So the expected outcome of running the walk unchanged over
  a compiler's bodies is that MOST are NO_TERM, and the measurement
  that matters is the fraction and the cause table, not the proofs.
  That fraction is the ceiling on objectives 2 and 3 as well, since
  they compose bodies and every body composed must have a term.
- **What follows from that measurement:** either bounded unrolling
  or loop invariants for the walk. Which one is a research question
  the measurement will pose; it is not chosen here.

### 1.2 Our own Hub-like compiler (hub_compiler)

- **What it is:** a lowering. Source file in, machine code out,
  where every operator in the source is replaced by ONE POOL ENTRY
  — a body already proved by the gate to compute that operator on
  those operand types — and the entries are joined through the
  canonical form's memory rows: entry N stores its answer into a
  row, entry N+1 loads its arguments from rows.
- **Why it is "Hub-like":** the Hub (AgentMemory, 2026-08-05) is
  the center of intention, holding every language's operator
  intentions in one place. The pool IS that center at the machine
  level: one entry per distinct computation, members from every
  language. A compiler that lowers through the pool lowers through
  the Hub.
- **The oracle test, exactly:** for one source file F in language L,
  body A = what L's own compiler emits for F, body B = what our
  lowering emits for F. Run the gate over A and B as it runs over
  two units today. Three outcomes, each informative:
    - PROVED: our composition of pool entries equals the original
      compiler's output. The pool entries used are confirmed IN
      CONTEXT, not only in isolation. This is the guard-rail.
    - DISPROVED with a counterexample: either a pool entry is wrong
      in context (a main-line defect, located to the entry), or the
      original compiler did something the operator-by-operator
      model does not (an optimisation across operators). The
      counterexample says which.
    - NO_TERM / UNDECIDED: the composed body is outside the walk's
      reach; the cause table says why.
- **Why it might vectorize lowering:** if each operator's lowering
  is an independent lookup into the pool, and the joins are the
  same prelude/epilogue every time, then lowering a file is a map
  over its operator list with no dependence between elements. That
  is the shape a vector operation has. The thing that normally
  prevents it, register allocation across operators, is absent
  because every value crosses between entries through a memory row.
  The cost is speed of the emitted code, which is not this node's
  objective.
- **What must exist that does not yet:**
    - A front end that yields the operator list with operand types
      per operator. The main line's probe generator already does
      this for ONE operator at a time from `operator_arity.json`;
      the ledger of PCv5 (`ts_to_ur`) does it for whole files. Which
      of those is the front end is the owner's to rule.
    - A joiner that emits the row traffic between entries. The
      canonical form's prelude and epilogue are the two halves of
      it already.

### 1.3 x's units as y's building blocks (cross_construction)

- **What it is:** the hub compiler with the pool restricted to one
  language. For each arch-unit U of language y, find a composition
  of x's arch-units whose gate verdict against U is PROVED. The
  measured result is a map: which of y's operators x can build,
  which it cannot, and the composition for each it can.
- **What already exists for it:**
    - Terms. 27,866 of 30,280 units have a proved z3 term. A
      composition of x's units has a term that is the substitution
      of their terms into each other, so the search can run at the
      term level first (fast, symbolic) and be confirmed at the
      body level by the gate (slow, authoritative).
    - Distinct bodies. The corpus has 2,744 distinct machine bodies
      across 31,067 compiled units, and 642 of them appear in more
      than one language. Those 642 are compositions of length one,
      already found: the same body IS both languages' unit.
- **Why it automates polyfill:** a polyfill is code in y that
  supplies an operator y lacks. If the map says y's operator O
  decomposes into x's units, and each of those x units has a
  counterpart in y's own pool (the 642 shared bodies are the seed of
  that), then the composition rewritten in y's counterparts IS the
  polyfill, and it arrives proved rather than written.
- **The open part:** composition search is synthesis, and synthesis
  over 2,744 blocks does not enumerate. The usable structure is the
  term: a y term is a tree of z3 operations, and x's terms are
  subtrees; matching subtrees bottom-up is a rewriting problem,
  which does terminate. Whether that finds compositions the gate
  then confirms is the experiment.

## 2. How the three relate, as one line

- compiler_units measures the ceiling (what fraction of real bodies
  get a term).
- hub_compiler builds the producer (compose pool entries, join
  through rows, prove against the original).
- cross_construction is the producer with one language's pool, and
  its output is the polyfill map.
- Each is an oracle for the main line: agreement confirms a pool
  entry in context; disagreement locates a defect to an entry, a
  join, or an optimisation the model lacks.

## 3. Where it might help slicing

The main line's slicing question is: which low-level operands are
which high-level variables. In the hub compiler, that question has
no search in it. Every value is a named memory row by construction,
because our lowering put it there. So a file lowered by us carries
its own slice. Comparing the row-named body to the original
compiler's body under the gate, when PROVED, transfers the naming:
the counterexample-free equivalence says the original compiler's
register at each point holds the row's value. That is a slice of the
original compiler's output obtained without walking the compiler.
Unverified; it is the reason objective 2 is worth doing first after
the ceiling measurement.

## 4. Order proposed, and why

1. compiler_units, first measurement only: run the existing term
   walk over the emitter definitions of go (57) and clang (251),
   report the four states and the NO_TERM cause table. Cheap, uses
   nothing new, and every later step needs its answer.
2. hub_compiler, smallest file: one function of two operators in c,
   lowered through two pool entries, gated against clang's body.
   One PROVED or one located counterexample.
3. cross_construction, seed: the 642 shared bodies as length-one
   compositions, then the term-rewriting search for length two.

## 5. Isolation, as set up

- Planning node: `node_0_3_8_arch_unit_oracle`, own sub-nodes.
- Artifacts: `PRIVATE/PseudoCoupHQ/Research/oracle/` (created
  empty, with a README naming the line).
- Airlock instances: `o<N>.conf`; lane names `o<N>_l<M>_<what>.sh`.
- Main-line artifacts are read, never written. Nothing under
  `Research/op_pipeline/` changes from this line.

## 6. Awaiting the owner

- The names: `arch_unit_oracle`, `compiler_units`, `hub_compiler`,
  `cross_construction`, `Research/oracle/`, instance prefix `o`.
- The front end for the hub compiler (the probe generator's operator
  list, or PCv5's `ts_to_ur` ledger).
- Whether the interpreter handler units (11, task 94/96) are to be
  moved under compiler_units or only cited from there.

## 7. Corrections from the owner, same day, and what they change

- **Objective 1 is the operators the compiler USES, not whole
  compiler functions.** §1.1 above read it as the pipeline over
  compiler function bodies; that is retired. The population is the
  operator sites in the compiler's own source (already parsed in the
  compiler graph), each made an arch-unit by generating the probe
  for that site's (operator, operand types) and compiling it with
  the compiler's own compiler. The comparison is offered-versus-used,
  through the pool, never through the token. Whole-function lowering
  stays a possible later sub-node, not started.
- **Objective 2's front end is tree-sitter, with the ledgerer where
  it applies.** The tree's nesting is the data flow; one memory row
  per tree edge; entries placed per operator node in post-order.
  §1.2's "which front end" question is closed.
- **Work order: objective 3 first.** §4's order is retired. the owner: "we
  should already have everything we need." Task o1 opens it.
