# log 002 — directed input generation, and the intention landscape

2026-07-31. the owner's design for reaching the branches a test suite never
takes, recorded, plus an answer to his question of whether tools for
this already exist.

Nothing here is settled. Section 5 is external research, not a
recommendation.

---

## 1. the owner's design, as stated

> there are ideas i have for creating a fuzzer. but the intentions
> data must know what it wants in a language first. not sure if that
> can be captured by a high level operator or data structure. if so,
> i guess that would make it easier.
>
> but lets says for an operator, if we know it and what arguments it
> wants, we can follow those.
>
> we know all nodes of a language from tree-sitter. we can either
> extract input argument types by brute force and/or by analysis. if
> we know the argument types, im wondering what we could to generate
> randomly generated instances of those argument types and then do
> some passes through the compiler to see what lights up. on the
> branches that light up, we could check to see if there are hidden
> branches that only occur under certain conditions. we could use
> that condition-data to navigate to those branches to light them up
> and add them to the intention slice.
>
> also something like the Python debugger and save-states could be
> used to navigate the compiler, where we could branch the walk by
> generating objects necessary to pass through logic gates.

### The loop, restated mechanically

1. **Fix the target.** An operator, named in the intentions data,
   with its argument types known.
2. **Get the argument types.** From tree-sitter's node set for the
   language, by brute force, by analysis, or both.
3. **Generate instances** of those types at random.
4. **Run them through the compiler**, with detectors reporting which
   UR-AST nodes activate — the mechanism from
   `~/Programming/PseudoIR/Planning/node_0_0_tools/node_0_0_1_slice/SUPPORT_brainstorm.md`.
5. **At each activated branch, look underneath it** for further
   branches that only fire under some condition.
6. **Read the condition, then aim at it** — generate an input that
   satisfies it, so the branch fires and joins the slice.
7. **Repeat** until nothing reachable is left dark.

Plus a navigation primitive: **save-states**. Pause at a branch,
snapshot, and fork the walk by synthesising whatever object is needed
to pass the gate — rather than restarting from a fresh input each
time.

This is a strictly stronger answer to log 001's closure problem than
the graph subtraction proposed there. Subtraction NAMES the arms the
tests never took. This REACHES them.

---

## 2. The boundary, answered

Log 001 §7 left open how the structural region gets bounded, and
guessed the retired seam declaration might return. the owner answered:

> if nodes are activate-ed or activate-able on the path from the
> starting node to arch opcodes, then thats the boundary.

So the region is defined by reachability between two fixed ends:

- **Start**: the node where the operator enters the compiler.
- **End**: the architecture opcodes it eventually becomes.
- **The region**: every node lying on some path between them —
  whether or not any run has actually taken that path. "Activatable"
  is doing the work in that sentence: a node that COULD fire on some
  path is inside the boundary even while it stays dark.

Two consequences worth stating.

- **No seam declaration is needed for this.** The boundary is
  computed from the two ends rather than declared by a person. That
  removes the reason log 001 expected the retired seam concept to
  come back.
- **"Activatable" is the whole difficulty.** Deciding it exactly is
  reachability over the compiler's control flow, and an
  over-approximation — everything the call graph says might be
  reached — is cheap but loose, while an exact answer is the
  expensive thing. Which one is good enough here is open.

---

## 3. The intention landscape

> i think we definitely need a computational analysis to create a
> landscape of intention. most of the stuff we are interested in is
> mostly compressible because it is well-behaved over large intervals
> of their parameters and then have edge case behaviors. very
> knowable.

The claim, stated flatly: an operator's behaviour over its input
space is piecewise, with a small number of large regions where the
behaviour is uniform, separated by a small number of edges where it
changes. Signed division over `i64 × i64` has about three regions —
ordinary division, divisor zero, and `MIN / -1` — across a space of
2^128 pairs. The description is tiny; the space is not. That is what
"compressible" means here.

If that holds generally, the landscape rather than the sample is the
right artifact: the goal is not "we tested many inputs" but "we know
where the boundaries are and what happens on each side".

It also reframes coverage. A slice is complete when every REGION has
been entered, not when some number of inputs has been run — and the
edges are exactly where the branches the test suite missed live,
because an edge case is a region so small that random sampling never
lands in it.

---

## 4. Does the intentions data have to know what it wants first?

the owner raised this as the precondition and was unsure whether an
operator or data structure is a high enough level to capture it.

Recorded as an open question, with one observation: the intentions
data already carries `row_satisfiers`, `canon`, `minimum_set` and
`policy_refs` as data — field names settled 2026-07-28 — but none of
those is an argument-type description. If step 2 above needs types,
that is a new field, and adding it is a schema decision.

---

## 5. What already exists, externally

the owner: "im surprised there doesnt exist tools for this kind of thing
already."

**They do exist, and the surprise is warranted only for the
combination.** Every individual step above is a named, mature area.
The assembly — using these techniques on a COMPILER'S OWN INTERNALS,
scoped to one source-language operator, to produce that operator's
slice — is not something any tool does.

This section is here so that a fuzzer built for this project is built
knowing what the known failure modes are. **These are third-party
tools, an entirely separate matter from this lineage's own past
projects; adopting any of them is the owner's call and nothing here
proposes it.**

| Step above | What the area is called | Maturity |
|---|---|---|
| 2–3, generate typed instances | property-based testing | solved; `proptest` for Rust generates from a type description and shrinks failures |
| 4, run and see what lights up | coverage-guided fuzzing | solved; AFL++, libFuzzer, `cargo-fuzz` |
| 5, find branches gated by unmet conditions | concolic execution — run concretely while recording the conditions each branch tested | mechanism solved; expensive |
| 6, read the condition and aim at it | the same: negate one recorded condition, hand it to a solver, get an input that takes the other branch | mechanism solved |
| save-states | state forking at branch points | standard in KLEE and angr, with copy-on-write sharing — and it is the main cost centre |
| 4+6 alternating | "hybrid fuzzing" — fuzz until progress stalls, then solve for the next branch | exists as research prototypes |

Named tools that are actually maintained: **KLEE** (v3.2, Dec 2025),
**angr**, **SymCC** (self-described as maintained best-effort and
understaffed), **AFL++**, **cargo-fuzz** (release June 2026),
**proptest**. **QSYM** is archived read-only since March 2023 and is
not a live option.

Compiler-specific, and closer to home: **rustlantis** generates
well-defined Rust MIR and differentially tests rustc's own
optimisation and codegen paths against each other, finding real
miscompilations through 2025. **Alive2** does bounded translation
validation on LLVM IR-to-IR transforms — it checks ALL executions of
a transform rather than sampling, which is a categorically stronger
result than any amount of fuzzing, and a 2025 follow-on extended it
to the AArch64 backend and found 45 new miscompilations. **LLVM ships
FuzzMutate in-tree**, which mutates IR directly rather than source
text.

Sources: <https://github.com/klee/klee>, <https://docs.angr.io>,
<https://github.com/eurecom-s3/symcc>,
<https://github.com/rust-fuzz/cargo-fuzz>,
<https://dl.acm.org/doi/10.1145/3689780> (rustlantis),
<https://web.ist.utl.pt/nuno.lopes/pubs/armtv-oopsla25.pdf> (Alive2 /
arm-tv), <https://llvm.org/docs/FuzzingLLVM.html>.

### For section 3, the landscape

The computational analysis the owner wants has a name too: **abstract
interpretation over the interval domain** — computing, without
running the program, the ranges a value can hold at each point.
Industrial implementations exist (Astrée; NASA's IKOS, updated March
2025). **LLVM already contains one**: `ConstantRange` with
`LazyValueInfo` propagates provable value ranges along edges, and
feeds the optimiser. It is a compiler internal used to optimise, not
a tool that emits a landscape as a deliverable — but the machinery
for "what ranges can this value take here" is sitting inside the
compiler being sliced.

The separate observation — uniform over large intervals, interesting
at the edges — is the premise of **boundary value analysis**, a
standard test-design technique. It has no automation of its own; it
is a heuristic for aiming, not a computed artifact. So the
"computational analysis to create a landscape" is genuinely not
off-the-shelf.

### The hard number

Symbolic reasoning does not survive contact with a compiler at full
size. A 2025 survey states it plainly: symbolic execution tools "are
typically ineffective for programs consisting of more than a few
thousand lines of code, let alone large codebases with line counts in
the millions" (<https://arxiv.org/html/2508.06643>). KLEE generates
tens to hundreds of thousands of live states within minutes on small
programs. LLVM was measured at 35.56 million lines at the end of 2024
(<https://www.phoronix.com/news/LLVM-Code-Activity-2024>).

**This is why §2's boundary is a precondition rather than a
refinement.** Unbounded, the technique does not work at this scale at
all. Bounded to the region between one operator's entry and its
opcodes, it is a different size of problem. the owner's instinct to bound
by reachability is what makes the rest viable.

The named cheaper variants trade precision for cost: pruning the
control-flow graph toward a target before exploring, or biasing input
generation by distance-to-target without solving conditions at all.

---

## 6. What is genuinely unserved

Worth being precise, since this is where the work actually is.

- **Operator-scoped slicing of a compiler's internals.** The existing
  compiler tools test whole-compiler correctness — does codegen agree
  with codegen, does a transform preserve semantics. None answers
  "what is the complete reachable-branch region inside this compiler
  that implements this one source operator".
- **The landscape as a deliverable.** Interval analysis exists inside
  optimisers as a means; emitting the region map as the artifact is
  not a thing tools do.
- **Joining activations back to UR-AST node identity.** External
  tools report coverage against their own notion of a program point.
  Reporting against a ledger id, so the result is a slice of the hub
  rather than a coverage percentage, is this project's own problem.

---

## 7. Answered and open, as of 2026-07-31

Two of the four closed the same day.

- **Argument types in the intentions data — no obstacle seen.** the owner:
  "i dont see immediately why it wouldnt." Recorded as a lean, not a
  ruling: nothing is known to prevent it, and the schema change has
  not been designed. §4's point stands that none of the settled
  fields (`row_satisfiers`, `canon`, `minimum_set`, `policy_refs`)
  is a type description, so this is an addition rather than a use of
  what is there.
- **"Activatable" is OVER-APPROXIMATED.** the owner, settled: "over-
  approximated would be sufficient and substantially easier." So the
  boundary is everything the control flow says MIGHT be reached
  between the operator's entry and its opcodes, without proving that
  each is genuinely reachable. Consequence to expect: the region
  contains nodes that no input can actually reach, so the dark list
  will carry some items that are dark because they are unreachable
  rather than because they are untested. That is the cost of the
  cheap answer and it is accepted.

Deferred by the owner until the administrative work is settled — annotated
open, not being worked:

- Whether the landscape is computed from analysis, from observation,
  or from both checked against each other.
- Whether any external tool is adopted at all, or whether the fuzzer
  is written here. the owner has said he intends to build it.
