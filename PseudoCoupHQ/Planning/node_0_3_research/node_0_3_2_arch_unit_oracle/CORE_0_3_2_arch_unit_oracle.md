---
id: hq.research.arch_unit_oracle
level: 2
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: arch_unit_oracle
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md
super_node:
    name: research
    path: ../CORE_0_3_research.md
sub_nodes:
    - name: compiler_units
      path: node_0_3_2_0_compiler_units/CORE_0_3_2_0_compiler_units.md
    - name: hub_compiler
      path: node_0_3_2_1_hub_compiler/CORE_0_3_2_1_hub_compiler.md
    - name: cross_construction
      path: node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md
    - name: architectures
      path: node_0_3_2_3_architectures/CORE_0_3_2_3_architectures.md
---

# CORE 0_3_2 — arch_unit_oracle

## metadata

- **id:** hq.research.arch_unit_oracle
- **level:** 2
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [research](../CORE_0_3_research.md)

## sub_nodes

- [compiler_units](node_0_3_2_0_compiler_units/CORE_0_3_2_0_compiler_units.md) — The operators a compiler's OWN SOURCE uses, each taken as an arch-unit, set against the operators that compiler OFFERS to the programs it compiles — the existing corpus — so that the difference between what a compiler offers and what it uses is measured.
- [hub_compiler](node_0_3_2_1_hub_compiler/CORE_0_3_2_1_hub_compiler.md) — Our own Hub-like compiler: a lowering that reads a source file through tree-sitter, types each operator node by the language's own front end run once as a type oracle (ruled 2026-09-07 on o6's measurement: go/types typed 79,799 of 103,475 sites at 541 MB and 160 s), resolves each node to its dominant operator, and emits target SOURCE composed from AutoPoly's proved emulations, one per node, so that the target's own compiler lowers and optimizes ACROSS the operators; its output is compared by the gate against what the original compiler emits for the same file.
- [cross_construction](node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md) — Language x's arch-units as the ONLY building blocks from which every arch-unit of language y is constructed, each construction proved by the gate, so that the set of y's operators that x can express is measured rather than assumed.
- [architectures](node_0_3_2_3_architectures/CORE_0_3_2_3_architectures.md) — The architectures the oracle runs on, one sub-node each, so that the part of the line that touches the machine is kept apart from the part that does not.

## definition

A parallel research line, forked 2026-09-05 from the operator
equivalence line
([operator_equivalence](../node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md)),
that turns the arch-unit machinery on itself in three ways and uses
each as an ORACLE — an independent answer that the main line's
answers can be checked against.

An **oracle**, in this node, is a second way of producing the same
machine code, or the same proof, from a different starting point,
so that agreement between the two is evidence and disagreement is a
located defect. The main line proves two compilers' units
equivalent; this node builds the units a second way and asks
whether the proof still holds.

Founded by the owner, 2026-09-05, verbatim:

> "the objectives are to explore two main things: 1. compiling /
> interpreting the compilers/interpreters to study their arch-units.
> 2. to construct our own Hub-like compiler/interpreter which we use
> with our knowledge of arch-units to compile files and compare them
> to how the original compiler compiles the same files. Oracle
> building. 3. exploring taking language x's arch-units as building
> blocks to construct all the arch-units of another language. these
> are to provide a means of guard-rail-ing the other project but also
> provide the stepping stones for the next phase of research and
> development. any combination of these might give us insights into
> how to easily slice. if we can achieve (3), we can basically
> automate polyfill for those languages that are expressive enough in
> their primitive building blocks. if we can achieve (2), we actually
> might be able to vectorize the lowering process."

## goal, added 2026-09-07: full modelling of `set_of_unique_arch_opcodes`, and the owner's loop

the owner's names, 2026-09-07 (verbatim definitions in
`PRIVATE/DevComms/LLM_communication_protocol_cases.md` Appendix C.1),
adopted as this node's names:

| name | definition | what holds it today |
|---|---|---|
| `set_of_unique_arch_opcodes` | every arch opcode called by any arch-unit of any compiler/interpreter, reduced to one instance each | `Research/oracle/arch_opcodes/unique_opcodes.json`, 162 |
| `set_of_arch_units_for_each_lang` | per language, every arch-unit its compiler/interpreter produced | the canon stores per language |
| `set_of_singletons_for_each_lang` | per language, the arch-units whose body is one arch opcode; a sub-set of the above | `Research/oracle/arch_opcodes/single_opcode_units.json` |
| `set_of_emulated_unique_arch_opcodes_for_each_lang` | per language, one `emulated_arch_opcode_i` per member of `set_of_unique_arch_opcodes` | o8 (c target) and o11 (rust target): 25 of 162 opcodes, two targets |

The loop, the owner's, verbatim:

```
for arch_opcode_i in set_of_unique_arch_opcodes:
    for lang_i in set_of_languages:
        emulated_arch_opcode = find_emulation(arch_opcode_i)
        set_of_emulated_unique_arch_opcodes_for_each_lang.append(emulated_arch_opcode_i)
```

`emulated_arch_opcode_i` is constructed at a high level with `lang_i`'s
compiler-operators (or constructable so, since it can be built from the
arch-units already extracted).

**The goal.** The full model of every member of
`set_of_unique_arch_opcodes`: per (mnemonic, operand width), the total
function on bit patterns, flags included, the fault region named. The
model comes from the reference simulator's own builders (`reference.py`,
160 of 162 mnemonics as of 2026-09-07), never from singletons; the
singletons are only where a mapping is visible in isolation.

**Why (the owner, 2026-09-07):** "im curious about the regression-fitting
type idea. and using those fits as a means of composing emulations. ...
an operator mapping can literally be plotted and interpolated through.
those interpolations could be added/combined/composed
(function-composition f(g(x)) and whatever else) to match (emulate) the
arch-opcode regression-fitting." The coordinator's reading of that idea,
with the bases in which each opcode class is an exact fit, is
`PRIVATE/PseudoCoupHQ/DevComms/log_234_arch_opcode_mappings_as_fits.md`.

**Ruling, 2026-09-08 (the owner, after the spelling guard flagged `and`/`or`/`xor`
in the o2 artifacts): a mnemonic alone is a spelling; the machine-form key
is (mnemonic, operand form, width).** The ban forbids a label standing in
for a mapping it does not determine: a source token `+` lowers to `add`,
`lea`, `addsd`, a call or a loop depending on types, compiler and flags, so
it may never key anything. A mnemonic with its operand form and width is
fixed by the instruction bytes and the ISA, and the reference's builders are
that determination, so the triple is a key. Consequences, all in effect:
- the model table (task m1) is keyed by the triple; the mnemonic sits in the
  field `mnem`, which the guard already exempts as machine form (`PROSE_FIELDS`,
  "a byte/sem key is a machine form"). The o2/o8/o9/o10 artifacts named that
  field `mnemonic` and are regenerated with `mnem` (task mn1). No exemption,
  no change to the guard.
- one spelling may carry two mappings (`imul` one-operand vs two-operand:
  different write sets) and several spellings one builder (`shl`/`sal`; the
  `mov*` suffixes). Whether two ROWS compute the same mapping is z3's verdict
  on their terms, never a reading of names: `add` and `lea` share a
  destination term on the plain form and differ on flags, so they are two
  mappings. Rows are reported equivalent, never merged.
- the 162 stands as the corpus's mnemonic VOCABULARY (log_221 §3's operation
  symbols). The table's row count is a different number by construction and
  is the deliverable, not a correction of o2.
- record of a near-miss: the coordinator (Opus) first diagnosed the guard's
  findings correctly as a string collision, then, on hearing the ban's
  principle restated, reversed to "the guard caught a real defect; every
  mnemonic-keyed count must be recomputed". That reversal replaced a correct
  claim with agreement (log_229 §4.5) and would have relitigated o2 and o9
  before the runs. Fable reviewed and the owner ruled as above.

**State of the loop, 2026-09-07:** outer loop run over 25 of 162 (the
singleton mnemonics), inner loop over 2 of 9 languages (c, rust); the
check exists for compiled targets (compile, carve, gate) and not for
interpreted ones. No new runs until the portable Airlock is on the
server (the owner, 2026-09-07).

## what this node shares with the main line, and what it does not

- **Shared, read-only:** the objects the main line has settled and
  the artifacts it has produced — the arch-unit (a function body's
  machine code plus arrival and answer facts), the canonical form
  (body verbatim between a memory-row prelude and epilogue), the
  ledger, the reference simulator, the gate, the term, the pool
  (`the_pool5.json`, 1,831 entries over 30,432 members as of
  2026-09-05), and the compiler graphs. This node reads them and
  never writes them.
- **Own, and never written by the main line:** everything under
  `PRIVATE/PseudoCoupHQ/Research/oracle/`, every sub-node
  below this CORE, and every Airlock instance named `o<N>.conf`.
  the owner, 2026-09-05: "i dont want either to interfere with the other."
- **Shared by repo, not by line:** the DevComms log numbering, which
  is per repo. A log of this line says so in its first line.

## standing rules, carried from the main line without change

- The unit boundary is a function body, read from the symbol table
  and DWARF (the owner, 2026-09-04).
- The canonical form keeps the body unchanged; only loads and stores
  at the edges (the owner, 2026-09-02, corrected reading 2026-09-05).
- The spelling ban: no operator token in any key, grouping, pairing
  or comparison scope; the guard runs on every artifact.
- Proofs are made against the one reference simulator, through the
  one gate; a body this node composes is proved by the same gate
  that proves the main line's units, never by a gate of its own.
- All compute through Airlock; memory bound stated per task; every
  report's claims re-runnable and attributed to a lane log.

## the three sub-nodes, in relation to each other, in work order

Order ruled by the owner, 2026-09-05: cross_construction first ("i just
want it to be a study of arch-units. we should already have
everything we need"). Run and FROZEN 2026-09-06 (see "state"); the
order now follows the research master plan.

1. [cross_construction](node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md)
   changes the VOCABULARY: y's unit must be written using only x's
   units. It needs nothing that does not exist: the pool, the terms,
   the gate. Its measured result is how capable each language is at
   constructing every other, and the polyfill map.
2. [hub_compiler](node_0_3_2_1_hub_compiler/CORE_0_3_2_1_hub_compiler.md)
   changes the PRODUCER: the machine code comes from us, one pool
   entry per tree-sitter operator node, joined along the tree's
   edges. Its oracle test is the gate over our body against theirs.
3. [compiler_units](node_0_3_2_0_compiler_units/CORE_0_3_2_0_compiler_units.md)
   changes the POPULATION: the operator sites in the compiler's own
   source, each as an arch-unit, set against the operators the
   compiler offers.

## state, 2026-09-06

| sub-node | task | result | status |
|---|---|---|---|
| cross_construction | o1 (log_207) | length-one construction: c and cpp build each other ~46–52%; every language builds 45–77% of rust and go; depth-2 composition adds under 3.1% in any cell | done |
| — | o2 (log_208) | per compiled language, 10–26 of 20–32 compiler-operators lower to a single arch opcode on some operand types; comparisons never; 60–130 distinct arch opcodes per language | done |
| cross_construction | — | **FROZEN by the owner 2026-09-06**: one language's single-opcode units cannot build another's; reopens only if a way to chain units down to one opcode appears | frozen |
| compiler_units | o3 (log_209) | every compiler uses essentially every scalar operator the corpus lowered; the gap runs the other way (assignment, member, cast operators used and never lowered) | done |
| compiler_units | o4 (log_210) | operator variants at every site, resolved by search alone: 6–22% of sites; leftover is call results, member access, inferred bindings, other-file declarations | done |
| compiler_units | step 1 of the master order | cut o4 to the lowering route (emitter definitions, diary functions) | next |
| hub_compiler | steps 4–5 of the master order | the Hub v1 dictionary read; one explicitly typed go file lowered by lookup and join, gated against go's output | after steps 2–3 |

The master order is [research](../CORE_0_3_research.md) §4.2. The
review that set it: `PRIVATE/PseudoCoupHQ/DevComms/log_211_review_paths_to_the_hub.md`.

## what this node does not decide

Sub-node names, the folder name `Research/oracle/`, and the instance
prefix `o` were chosen by the coordinator on 2026-09-05 so that work
could begin; each is the owner's to rename. The hub compiler's front end
(tree-sitter, with the ledgerer where it applies) and the work order
(cross_construction first) were ruled by the owner the same day.
