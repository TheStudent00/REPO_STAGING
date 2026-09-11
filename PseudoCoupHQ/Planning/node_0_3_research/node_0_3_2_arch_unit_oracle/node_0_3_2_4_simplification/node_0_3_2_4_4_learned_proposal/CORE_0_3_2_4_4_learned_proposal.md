---
id: hq.research.arch_unit_oracle.simplification.learned_proposal
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: learned_proposal
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_4_learned_proposal/CORE_0_3_2_4_4_learned_proposal.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes:
    - name: dataset
      path: node_0_3_2_4_4_0_dataset/CORE_0_3_2_4_4_0_dataset.md
    - name: model
      path: node_0_3_2_4_4_1_model/CORE_0_3_2_4_4_1_model.md
    - name: propose_then_gate
      path: node_0_3_2_4_4_2_propose_then_gate/CORE_0_3_2_4_4_2_propose_then_gate.md
---

# CORE 0_3_2_4_4 — learned_proposal

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.learned_proposal
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

- [dataset](node_0_3_2_4_4_0_dataset/CORE_0_3_2_4_4_0_dataset.md) — `Dataset` - pairs (term, shorter form): the bank's real bodies first, reverse-constructed expansions as augmentation, and "no shorter form at bound k" labels taken only from synthesis's residue, carrying their k.
- [model](node_0_3_2_4_4_1_model/CORE_0_3_2_4_4_1_model.md) — `Model` - a proposer over term graphs (a small graph network or a transformer over normalized term text), conditioned on the unit vocabulary available; outputs a ranked list of units or rule sketches.
- [propose_then_gate](node_0_3_2_4_4_2_propose_then_gate/CORE_0_3_2_4_4_2_propose_then_gate.md) — `propose_then_gate(E, top_n)` - the loop above; reports hits per rank so the model's value is a measured number (candidates verified before the first hit).

## definition

A model that ORDERS candidates; z3 that ACCEPTS them. One model over
terms (language- and architecture-neutral), conditioned on the
target's unit vocabulary; never one model per language. Changes the
constant, never the guarantee.

```
for cert in bank:                                   # the compiler's real expansions
    data.append((term_of(cert.body), cert.cell))
for u in units_of(lang):                            # synthetic, provably labelled
    body = expand(u, rules_backwards, depth)
    data.append((term_of(body), u))
candidates = model.propose(term_of(E), units_of(lang), top_n)
for c in candidates:
    if gate(c.term == term_of(E)): return rule(c)
```
