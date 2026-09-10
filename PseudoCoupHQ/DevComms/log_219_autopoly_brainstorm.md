# log_219 — AutoPoly: the owner's commentary on the emulation result, and the coordinator's

Line-wide (research master plan). Written 2026-09-06 by the coordinator
(Fable) at the owner's request, after task o7 (log_218). the owner's words are
verbatim; the coordinator's are marked as opinion where they are
opinion. The standing shape of the idea lives in
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/SUPPORT_BRAINSTORM_autopoly.md`;
this log is the record of the day.

## 1. the owner's commentary, verbatim

> "those results are very encouraging.
>
> what it makes me think of is, if we can automate the creation of
> proven lower-optimized-equivalent high level emulations with our
> arch-unit knowledge, we would gain efficient polyfill across all
> languages, not just in the hub. also the pre-compiling of polyfill
> would make it just as fast as slice-insertions into compilers --
> which has been the overall direction of PCHQ but we might be able to
> side-step the iterative-development altogether (AutoPoly->Hub, et
> al. instead of PCv5->PseudoIR->PCv6. "AutoPoly" being our automated
> polyfiller and "Hub, et al." referring to ingress into hub and
> ingress out of hub to some target).
>
> the simplification down to the direct `c` equivalent is unbelievably
> interesting to me. as is the equivalence not being detected when it
> is by design. (my mind immediately starts to wonder about how to
> push z3 further or augment it somehow -- such as machine learning.).
>
> very brainstormy. but i think these are important ideas to explore
> so im curious what you think."

## 2. The result this rests on, restated with its population

Task o7, log_218: 206 pool entries with a go, rust or swift member and
no c member, each rendered from its proved term to a C function by one
renderer and compiled by clang at ship flags. 168 of 204 compiled
emulations proved equivalent to the x unit by the gate; 193 of 204
under the caller-extension reading of narrow arguments; 5 of 204
byte-identical to an existing c unit, against a control ceiling of 14
of 33 (clang reproduces a c unit's own bytes from its own term 42% of
the time). Where the proof fails, the x body carries a guard the term
lacks in 6 of the 11 unrescued cases.

## 3. The coordinator's commentary

### 3.1 What AutoPoly IS, in one sentence, in relation

AutoPoly is the pipeline that turns one dominant operator (a pool
entry) into a PROVED source-level function in a target language y:
entry → term → render to y source → compile with y's own compiler at
ship flags → carve at the function body → gate against the entry's
unit. Its output is y SOURCE, carrying a proof; the pool supplies the
operators, the renderer supplies the language, the gate supplies the
proof. Task o7 is AutoPoly with y = c and the gate run once per entry.

### 3.2 Why "efficient polyfill across all languages, not just in the hub" follows

- The output is source, so it runs through ANY build of y's compiler,
  not through our machine-code stitching. A polyfill for go's `&^` in
  c is a c function; every c compiler optimizes it as native code.
- "Pre-compiled" is measurable: the emulation is compiled by y's
  optimizer, so its speed is the optimizer's. The control says clang
  emits the SAME bytes as the native unit 42% of the time and
  behaviour-equivalent bytes 70–100%. The remaining question is size
  and cycles of the equivalent-but-different bodies against the
  native ones; that is a measurement (byte count now, `llvm-mca` or
  cycle counts later), not a design question.
- Opinion: this is where the speed claim against slice insertion
  should be settled, by that measurement, before the route is
  declared.

### 3.3 AutoPoly → Hub: what changes in the plan if it holds

- The hub_compiler node today lowers by placing one canonical BODY per
  operator node and joining them through memory rows (machine-code
  stitching). The AutoPoly form lowers by placing one proved SOURCE
  function per operator node and letting y's compiler join them —
  which means y's optimizer works ACROSS operators, which the row
  join by construction cannot.
- So the Hub becomes source-to-source: ingress = tree-sitter over x
  plus a typing route (o6 shows the front end as oracle is cheap on
  go), each operator node resolved to its dominant operator; egress =
  the AutoPoly emulation of that dominant operator in y, composed as
  y source. The proofs are done once per (entry, y) and reused; the
  per-file oracle test (gate over the whole composed function against
  x's compiler's output) stays as the check.
- Opinion: this side-steps PCv5 → PseudoIR → PCv6 as the owner says, because
  the compiler's own lowering and optimization are invoked, never
  reproduced. What it does NOT side-step: the typing of ingress (the
  key needs types), the aggregate forms (text, sequence, keyed,
  nesting have no arch-units yet), and the languages without a corpus.
- This changes hub_compiler's definition (machine-code join → source
  composition). That is the owner's to rule; the node is not edited on this
  log.

### 3.4 "Simplification down to the direct c equivalent"

- What happened mechanically: the go unit's term was a 128-bit
  division nest (`Extract(31, 0, bvudiv_i(Concat(0, v0), Concat(0,
  v1)))`); rendered literally to C it is a 128-bit expression; clang's
  instruction selection recognised that the high halves are zero and
  emitted the 32-bit `div`. The collapse is the optimizer's algebra,
  not ours.
- Opinion: this is superoptimization by proxy. The renderer emits ONE
  source form; clang chooses among the forms it can prove equal. Two
  levers follow: (a) render several equivalent source forms per term
  and keep the one whose compiled body is smallest or byte-identical
  to a known unit — the gate proves each, so the search is sound; (b)
  treat the 42% control ceiling as the thing to raise, since it
  measures how far the renderer's form is from what clang emits
  natively.

### 3.5 "Equivalence not detected when it is by design"

- The 36 disproved emulations are not solver failures. The gate found
  a real input where the two bodies differ, and in 6 of the 11
  unrescued cases the difference is a GUARD in the x body: a zero
  divisor or a signed extreme sent down another path (go's
  `runtime.panicdivide`). The term is total; the body is not.
- The pipeline already has the vocabulary for this: the ledger's
  guard-outcome rows, the DIFFERS-BY-DESIGN verdict, the exception
  families, and the directional bridge ("X dominates Y on projection
  P", with the adapter). What AutoPoly lacks is rendering the MODE: an
  emulation of a guarded operator must render the guard too (`if (b ==
  0) trap();` before the division), or the proof must be posed on the
  projection that excludes the guarded domain, with the exclusion
  named.
- Opinion: this is not a place to push z3. z3 answered correctly. The
  work is to carry the mode from the ledger into the renderer, so a
  polyfill for a trapping operator traps. The 5 unattributed disproofs
  are one small lane (evaluate both bodies at the recorded seeds).

### 3.6 Pushing z3, and machine learning

- Where z3 actually limits us today: UNDECIDED on wide division and
  multiplication (task t100: 102 of the first 2,954 pairs timed out at
  the sub-process ceiling; the 3,000 ms gate ceiling is the owner's), and
  the cost of proving many pairs (43,410 candidate pairs, 18,307
  answered in two four-hour windows).
- Opinion on ML, held to the evidence doctrine (the gate is the judge;
  nothing learned is evidence):
    - **Proposer, never judge.** A model may PROPOSE a rewrite, a
      lemma, a candidate pair, or a source form; z3 or the gate
      decides. Anything accepted is proved; anything the model got
      wrong costs a solver call, never a wrong entry in the pool.
    - **Ordering the pair work.** Which of the 43,410 pairs are worth
      proving first is a ranking problem with labelled data already on
      disk (18,307 verdicts with their terms). A ranker that puts
      proved pairs ahead of disproved ones would turn t100 from four
      hours per 3,700 pairs into hours per thousands of edges.
    - **Choosing the rendering.** Which source form clang collapses to
      the smallest body is a search over equivalent forms; a model can
      order the search; the gate proves the winner.
    - **Not this:** learning equivalence itself, or replacing the
      reference simulator. Both would put interpretation where a proof
      stands.
- Concrete first experiment, cheap: the ranker over t100's 18,307
  verdicts, features from the two terms' texts and the type key, scored
  by how many proved edges land in the first N pairs against the
  brief's pair-count order. Measured, not asserted, before any ML is
  wired into a lane.

## 4. What the coordinator proposes, as tasks (none opened without the owner)

1. **Render the mode.** Extend the renderer to emit the guard from the
   ledger's guard-outcome rows; re-run the 36 disproved. Expected:
   most move to proved, the rest are the unattributed five.
2. **Rust as the second emitting language** (a rust renderer; the
   population is the entries with a c/go/swift member and no rust
   member). Then go, then swift, so AutoPoly covers the five compiled
   languages in both directions.
3. **Size and cycles**: for every proved emulation, body bytes against
   the native unit's bytes; then `llvm-mca` cycle estimates. This is
   the "as fast as slice insertion" claim, measured.
4. **The Hub as source composition**: one explicitly typed go file →
   C source composed from AutoPoly emulations → clang → gate against
   go's own output for the whole function. This replaces master-plan
   step 5's join-through-rows if the owner rules the change to hub_compiler.
5. **The ranker experiment** over t100's verdicts (§3.6).
6. **The five unattributed disproofs**, one lane.

## 5. Awaiting the owner

- Unfreeze cross_construction on the emulation route (AutoPoly as its
  sub-node), or found AutoPoly as its own sub-node of arch_unit_oracle.
- Whether hub_compiler's definition moves from machine-code join to
  source composition.
- The order among §4's six.
