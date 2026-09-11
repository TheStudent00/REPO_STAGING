---
id: hq.research.arch_unit_oracle.simplification
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: simplification
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/CORE_0_3_2_4_simplification.md
super_node:
    name: arch_unit_oracle
    path: ../CORE_0_3_2_arch_unit_oracle.md
sub_nodes:
    - name: emulator_arch_units
      path: node_0_3_2_4_0_emulator_arch_units/CORE_0_3_2_4_0_emulator_arch_units.md
    - name: matching
      path: node_0_3_2_4_1_matching/CORE_0_3_2_4_1_matching.md
    - name: equality_saturation
      path: node_0_3_2_4_2_equality_saturation/CORE_0_3_2_4_2_equality_saturation.md
    - name: synthesis
      path: node_0_3_2_4_3_synthesis/CORE_0_3_2_4_3_synthesis.md
    - name: learned_proposal
      path: node_0_3_2_4_4_learned_proposal/CORE_0_3_2_4_4_learned_proposal.md
    - name: measurement
      path: node_0_3_2_4_5_measurement/CORE_0_3_2_4_5_measurement.md
    - name: guarantees
      path: node_0_3_2_4_6_guarantees/CORE_0_3_2_4_6_guarantees.md
---

# CORE 0_3_2_4 — simplification

## metadata

- **id:** hq.research.arch_unit_oracle.simplification
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit_oracle](../CORE_0_3_2_arch_unit_oracle.md)

## sub_nodes

- [emulator_arch_units](node_0_3_2_4_0_emulator_arch_units/CORE_0_3_2_4_0_emulator_arch_units.md) — The population every path reads: each proved emulation's compiled body as an arch-unit of its language, with its cell, tier and certificate.
- [matching](node_0_3_2_4_1_matching/CORE_0_3_2_4_1_matching.md) — Task rm1's algorithm: contiguous segments and, second, connected sub-graphs of the body's term, matched to the language's own units by fingerprint and decided by z3.
- [equality_saturation](node_0_3_2_4_2_equality_saturation/CORE_0_3_2_4_2_equality_saturation.md) — Every form the rule set can generate, held at once in an e-graph, and the cheapest extracted; no greedy ordering trap.
- [synthesis](node_0_3_2_4_3_synthesis/CORE_0_3_2_4_3_synthesis.md) — Task rm2: component-based synthesis.
- [learned_proposal](node_0_3_2_4_4_learned_proposal/CORE_0_3_2_4_4_learned_proposal.md) — A model that ORDERS candidates; z3 that ACCEPTS them.
- [measurement](node_0_3_2_4_5_measurement/CORE_0_3_2_4_5_measurement.md) — One benchmark for every path, so the paths are compared on the same bodies with the same metric.
- [guarantees](node_0_3_2_4_6_guarantees/CORE_0_3_2_4_6_guarantees.md) — What each number in this node is allowed to claim.

## definition

Leveraging the `backstop`'s emulator arch-units: finding, and proving,
the shorter form the compiler did not find. Created 2026-09-11 on the owner's
word: "why dont we explore all of these paths? i dont see why we need
to pick a single model." Every path is a sub-node; they share one
population (sub-node 0), one benchmark (sub-node 5) and one statement
of what each number guarantees (sub-node 6).

`emulator arch-unit`
- the compiled body of an emulation, any tier: machine code the
  compiler produced for the emulation's source. An arch-unit of its
  language like any other, so it joins `set_of_arch_units_for_each_lang`.
- measured already: the compiler folded 0 of 14 backstop bodies back to
  the one instruction they emulate (t2), and 31% of tier-1 bodies landed
  on their own opcode (ap6). The rest is what this node goes after.

`the shorter form`
- a combination of the language's own arch-units whose term equals the
  emulator arch-unit's term on its live interface, with fewer
  instructions. "Equals" is always z3's verdict, carried as a certificate.

```
for lang in set_of_languages:
    E_set = emulator_arch_units(lang)                 # sub-node 0, from the bank
    for E in E_set:
        for method in (matching, equality_saturation, synthesis, learned_proposal):
            shorter = method.find(E, units_of(lang))  # each method a sub-node
            record(E, method, shorter, guarantee_of(method))   # sub-nodes 5 and 6
```

## the paths, in relation
| sub-node | what it proposes | what it guarantees (sub-node 6) | cost |
|---|---|---|---|
| [matching](node_0_3_2_4_1_matching/CORE_0_3_2_4_1_matching.md) | sub-terms of E that already equal a unit | every rule it emits is true | N² walks; z3 only on fingerprint collisions |
| [equality_saturation](node_0_3_2_4_2_equality_saturation/CORE_0_3_2_4_2_equality_saturation.md) | every form the rule set can generate, at once | reaches everything the rules span, no ordering trap | bounded by the rule set |
| [synthesis](node_0_3_2_4_3_synthesis/CORE_0_3_2_4_3_synthesis.md) | a wiring of at most k units equal to E | the shortest straight-line form at bound k, or none exists at k | exponential in k |
| [learned_proposal](node_0_3_2_4_4_learned_proposal/CORE_0_3_2_4_4_learned_proposal.md) | ranked candidates from a model trained on the bank | nothing on its own; z3 accepts, the model only orders | training once; proposals cheap |

Prior art, named so the claim is placed and not overclaimed: peephole
superoptimization (Bansal & Aiken 2006), Souper, STOKE, equality
saturation (egg), component-based synthesis (Gulwani 2011), learned
superoptimizers (Bunel 2017, AlphaDev). The claim is the two
differences: the candidates are the language's OWN proved arch-units,
and every rule carries a certificate.
