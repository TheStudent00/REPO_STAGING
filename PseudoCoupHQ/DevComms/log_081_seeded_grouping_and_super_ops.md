# log 081 — seeded grouping under conditions, and super-logical compiler-operators

Date: 2026-08-29. Ratified in conversation ("yes to all of it. we
are aligned"). Companion ruling added to
`PseudoCoupHQ/AgentMemory.md` under "SEEDED GROUPING
UNDER CONDITIONS". Supersedes the narrow core definition; the core
becomes a special case.

## 1. The reframe the owner brought, in his own construction

Arch-units are dataflow graphs from arguments to answer. His
worked example, kept verbatim:

> ```
> def func_0 -> int (a_0: int, b_0: int):
>     a_1 = machine_op_0(a_0)
>     a_2 = machine_op_1(a_1)
>     b_1 = machine_op_2(b_0)
>     ret = machine_op_3(a_2, a_1, a_0, b_1, b_0)
>     return ret
>
> def func_1 -> int (a_0: int, b_0: int):
>     a_1 = machine_op_0(a_0)
>     a_2 = machine_op_1(a_1)
>     b_1 = machine_op_2(b_0)
>     ret = machine_op_3(a_2, a_1, b_1)
>     return ret
> ```
>
> `func_1` evades core-detection because tracing only got to
> `machine_op_0(a_0)` and `machine_op_2(b_0)` because `a_0` and
> `b_0` were never called at the same time.

- The old core definition ("the distinguished instruction whose
  operands are the traced arguments") only exists when the
  operator is one instruction taking both arguments directly.
- The trace rule that replaces it (the owner's words): if a traced
  variable is transformed by an operator, the result of that
  transformation takes on the responsibility. Tracing follows
  transformations indefinitely; any stopping depth is an
  implementation defect, never a policy.
- The measured units this reframe explains: `c/op_501`
  (conversion between argument and compare — depth), `c/op_285`
  (three tests joined by or — breadth). Both were stuck for the
  same reason: the tracer modelled a path, the unit is a graph.

## 2. Graph, not tree — fan-out

- Edges point away from the arguments (the owner's temporal picture is
  right). The one addition: a node's result can feed several
  later nodes. In message terms: the same message goes to several
  recipients; sending does not consume it — the register still
  holds the value.
- Consequence for seed equality: whether a shared sub-computation
  is written once or twice is a compiler choice, not a
  computational difference. Seed equality is graph equality, so
  those choices do not split seeds.

## 3. The ratified grouping: seed + conditions

- SEED: the normal-path computation graph of a unit, from
  arguments to answer.
- GUARDED CONTAINMENT (the owner's formulation): if another unit
  contains the seed in one branch, then WITHIN THE CONDITIONS
  THAT GATE THAT BRANCH the two are computationally equivalent.
  The relation recorded is "contains seed S under condition C" —
  C kept as data (the mode rows already extract it), never
  discarded.
- Measured instance already in hand: go modulo block L3 is
  character-identical to c's whole modulo unit; the gate is
  `b != 0 and b != -1`. Within those conditions, go IS c.

## 4. Why not unbiased whole-graph similarity — the bias problem

- Whole-graph comparison groups by whatever dominates the graph,
  and for guarded units that is often the exception machinery:
  go's divide and go's modulo share the SAME panic-call guard
  structure while computing different things.
- Seeded grouping splits the two axes:
    - operator grouping, by seed (what the normal path computes)
    - exception grouping, by guard component (which condition is
      checked and which response follows), grouped across
      operators and languages — all `panic-call:runtime.panicdivide`
      guards are one exception family whichever operator carries
      them.
- Both axes automate from existing stages: seeds from the
  converged forms, guards from mode extraction, containment from
  the annotation layer.
- The payoff the owner named: on a major language update, re-probe and
  diff TWO small tables — did any operator change seed family,
  did any guard change exception family — instead of re-judging
  units by hand.

## 5. Super-logical compiler-operators

- The observation: an idiom that recurs across arch-units is the
  COMPILER'S logic, not the operator's. The instance:
  `cpp/op_765`'s halve-convert-double routine, emitted inline
  because the hardware has no unsigned-64-to-float instruction.
  That routine is written as high-level code in the compiler's
  legalization stage (evidence class: knowledge of compiler
  structure; the compiler-graph instrument can measure the path).
- The detector already exists: the component miner's recurrence
  counts. The automation rule ratified:
    - a recurring component whose lifted form contains an
      UNMODELLED name is a SUPER-OP CANDIDATE;
    - mine it, model it once, and every unit containing it
      unblocks together;
    - so pyvex's coverage never again requires hand-intervention
      — gaps surface by recurrence, not by someone noticing.
- Shown this session: the lifter models `cvtsi2ss` completely
  (`I32StoF64` then `F64toF32` with a rounding mode); the block
  was OUR whitelist that never translated those names to z3.
  The limiting factor was one table of ours, not the lifter and
  not z3.

## 6. What this supersedes, and what it keeps

- Supersedes: the core as "the distinguished instruction" — now a
  special case (seed of depth one).
- Keeps: canonical form as the home representation (log_075);
  the ground-truth-anchored gate; the spelling ban; compositional
  matching (log-level: the alpha/beta/gamma levels become
  seed-components); the mode rows and their response vocabulary.

## 7. The work this orders

1. Extend the translation table with the conversion names the
   lifter already produces (I32StoF64, I64StoF64, F64toF32,
   F32toF64, and the packed forms) — unblocks the ~130
   conversion-mixed units.
2. Teach the tracer fan-out (multiple tests joined by and/or) —
   the ~78 multi-atom units.
3. Run the super-op miner: recurring components x unmodelled
   names -> candidate list, model by recurrence rank.
4. Bring branching units into canonicalization (the erasure
   refusals), which also brings them into the table population.
5. Build the two grouping tables: seed families (operator
   grouping) and guard families (exception grouping), with
   guarded containment as the cross-unit relation.
