# probe_design — layer 3, phase 1

The generation rules, written down before anything was generated, so that
the owner can inspect them and overturn any of them by number. Executable form:
`probe_generate.py`. First language: python (the CORE's proposal, confirmed
by log_021 §6.4 — python has the highest depth-1 share of the eleven).

Three cold words first, because each has been away long enough that a
definition does not survive the gap.

- **Layer 1** is the DATA: fixed content, no language — nothing, truth,
  whole number, fractional number, text, sequence, keyed grouping, nesting,
  identity marks. It lives in
  `../data_representation/data_layer1.json`.
- **Layer 2** is the REPRESENTATIONS: per language, the ways a running
  program can HOLD that content. One (form, representation) pair is a CELL;
  the load-audit says which cells actually take the data.
- **Layer 3**, which this file serves, is the OPERATIONS: what the
  COMPILER can do to a loaded cell — operators, indexing, comparison,
  iteration, arithmetic. Never builtins, never standard-library calls.

A **KIND** is what tree-sitter's grammar declares: a named construct
(`binary_operator`, `subscript`) or an anonymous token (`+`, `is not`).
A **PROBE** is one measurement: one kind (or one token off a menu), one
operand assignment drawn from layer-2 cells, one spelling mode.

---

## (a) which kinds are probed

The instrument is the grammar's own legal-slot table
(`legal_pairs_python.json`, phase 0). A slot is probeable when the grammar
declares that a dominant-typed filler may legally stand in it. For python
that is **68 slots over 61 host kinds**; the other 61 named kinds take no
dominant input at all and are honest exclusions, already listed in phase 0.

Under the **R2 ruling** — each operator on a token menu is its own probe —
the five menu-carrying hosts contribute one signature per token, not one
per host:

| host | menu | tokens |
|---|---|---|
| `binary_operator` | 13 | `%` `&` `*` `**` `+` `-` `/` `//` `<<` `>>` `@` `^` `\|` |
| `comparison_operator` | 11 | `!=` `<` `<=` `<>` `==` `>` `>=` `in` `is` `is not` `not in` |
| `augmented_assignment` | 13 | the thirteen `<op>=` spellings |
| `boolean_operator` | 2 | `and` `or` |
| `unary_operator` | 3 | `+` `-` `~` |

The 68 slots are split into two tiers, because they are not all asking the
same question.

- **Tier A — the operations.** The kinds the layer-3 definition names:
  arithmetic and bitwise (`binary_operator`, `augmented_assignment`),
  comparison and membership and identity (`comparison_operator`),
  truth-testing (`if_statement`, `while_statement`,
  `conditional_expression`, `not_operator`, `boolean_operator`),
  indexing and slicing (`subscript`, `slice`, `delete_statement`),
  iteration (`for_statement`, the three comprehensions,
  `generator_expression`, tuple unpacking), and adjacent-literal
  concatenation. These get the full input matrix.
- **Tier B — the placements.** Every remaining dominant-typed slot, asked
  only "does this kind accept this cell, and what comes back" — one
  representative value per cell. A placement probe is cheap and its answer
  is still a domain measurement.

## (b) what each probe position takes as input

Operands are layer-2 CELLS, not raw layer-1 values, because a form has
several holders and the difference between holders is the thing layer 3 is
here to measure.

- **Input cells**: the 23 cells the python load-audit judged LOADS, plus
  the 3 judged PARTIAL with their refused edges dropped — **26 cells**.
- **Atoms**: one operand per (form, representation, value class) that
  actually loaded — **117 atoms**, of which 43 can be spelled as a bare
  literal. Base values AND edge values are both baked in as literals by the
  generator, exactly as the layer-2 generator bakes them; no probe parses
  the data file at run time.
- **Single-operand set U** = all 117 atoms.
- **Operand pairs P** = **200 ordered pairs**, built by four rules rather
  than by the 117 x 117 = 13,689 cross product:

  | rule | pairs | what it asks |
  |---|---|---|
  | same-cell | 26 | X op X — the operation's home ground |
  | cross-representation | 60 | two holders of ONE form, e.g. int x Decimal |
  | cross-form | 42 | the seven canonical holders against each other |
  | edge lane | 72 | every non-base value of a canonical cell: against itself, and both ways against `whole.int` 42 |

**Both spellings.** The calibration lesson from log_019 is that a value's
spelling can change what is measured. So every probe whose operands can all
be written as bare literals is generated TWICE:

- **opaque** — the operand is built into a variable first, and the operator
  sees a name. The compiler cannot fold it.
- **direct** — the literal stands in the operator's slot. The compiler may
  fold, warn, or refuse.

A difference between the two is a finding about the COMPILER, not about the
data. 6,956 probes carry a direct twin.

## (c) what a probe prints

One line, `PROBE_ID|RESULT`, the convention the census harness and the
layer-2 audit both use. `PROBE_ID` is
`<family>.<token>.<left atom>.<right atom>.<mode>`; an atom id is
`<form>.<representation>.<value class>`. No probe id may hold a `|`.

`RESULT` is one of:

| spelling | meaning |
|---|---|
| `<type>:<value>` | it answered — the type the compiler produced, then the canonicalized value |
| `<raise:NAME>` | it raised, NAME being the raise's own name |
| `<compile-error:NAME>` | the compiler refused the source outright |
| `<timeout>` / `<compile-timeout>` | it did not finish inside the budget |
| `<no-answer>` | it ran and bound nothing |

Canonicalization: sets and keyed groupings are printed in a fixed order so
that an unordered holder cannot answer differently run to run; newlines,
tabs and the pipe are escaped; anything past 160 characters is cut with
`<trunc>`.

## (d) enclosing context

- **depth 1** — no wrapper; the probe is the whole program.
- **depth 2** — the wrapper is GENERATED by the rule that needs it: `elif`
  gets its `if`, a comprehension clause gets its comprehension, `except`
  gets its `try`, a decorator gets a definition to sit on. 17 kinds.
- **depth 3+** — python's tail is exactly the nine hosts phase 0 measured,
  and all nine wrappers are **HAND-WRITTEN** and marked as such in
  `probes_python.json` (`wrap: "hand"`): `complex_pattern`,
  `default_parameter`, `dict_pattern`, `format_expression`,
  `keyword_argument`, `keyword_pattern`, `typed_default_parameter`,
  `union_pattern`, `with_item`.

## (e) the judgment calls, numbered, for the owner to overturn

1. **The input is a layer-2 CELL, not a dominant.** Phase 0 counted probes
   against six dominants; layer 3 replaces each dominant with the cells
   that hold that form — python's whole number has four holders, its
   sequence five. This is what makes the run bigger than phase 0's 686 and
   it is the whole point of the three-layer split; without it a probe
   cannot tell `int` from `Decimal`.
2. **Operand pairs are chosen by four rules, not enumerated.** 200 of the
   13,689 possible ordered pairs. The rules are in (b) and each is there to
   answer a question; the cross product answers none of them better.
3. **A cell classified REFUSES-behavioral is not an input.** python has one
   — `sequence.array.array` — and two of its five values did load. Dropping
   the whole cell is the literal reading of the hand-off rule and it costs
   the run a measured holder. Overturnable: admit the cell with only its
   loaded values, exactly as PARTIAL cells are admitted.
4. **Catching is harness mechanics.** The runner wraps each probe in its
   own try/except so one raise cannot kill a batch, and a `raise`
   PLACEMENT probe is wrapped so the raise can be read. Catching is never
   itself a probed operation.
5. **Python needs no bisect.** Its compiler is reachable at run time, so
   the driver compiles each probe on its own and a refusal isolates
   exactly. The bisect crux in the CORE is a cost of the ten compiled
   languages, not of this one — it is deferred, not solved.
6. **A budget is enforced, and exceeding it is a result.** Two seconds of
   wall clock and 2 GB of address space per probe. `42 ** i64max` is a
   legitimate probe of `**` whose honest answer is "did not finish".
7. **A pattern slot gets only the direct spelling.** In `case {X}:` a
   variable name is not an opaque spelling of a literal — it is a capture
   pattern, a different construct. So the four pattern hosts are probed
   with literals only.
8. **The depth-3+ tail is written up front, not grown from refusals.** The
   CORE left this open; nine wrappers is small enough that writing them
   costs less than a second pass.
9. **Identity atoms are hand-built.** The layer-2 identity probes end in a
   verdict word rather than in the object, so layer 3 spells the three
   identity shapes itself, once per holder. Their construction uses an
   append — layer-2 mechanics for building the operand, never a probed
   operation.
10. **`await` is deferred.** Driving a coroutine needs an event runner,
    which is a standard-library call, and the CORE rules those out of
    scope. It is recorded as deferred rather than silently dropped.
11. **Tier B asks a smaller question than tier A.** One representative
    value per cell, not the full matrix. Overturnable at the cost of about
    a fivefold run, which python can afford and the ten may not.
