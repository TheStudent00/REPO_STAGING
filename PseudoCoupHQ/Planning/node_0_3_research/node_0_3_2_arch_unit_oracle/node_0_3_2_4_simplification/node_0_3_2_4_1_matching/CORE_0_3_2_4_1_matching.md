---
id: hq.research.arch_unit_oracle.simplification.matching
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: matching
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_1_matching/CORE_0_3_2_4_1_matching.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes:
    - name: walk
      path: node_0_3_2_4_1_0_walk/CORE_0_3_2_4_1_0_walk.md
    - name: liveness
      path: node_0_3_2_4_1_1_liveness/CORE_0_3_2_4_1_1_liveness.md
    - name: fingerprint_index
      path: node_0_3_2_4_1_2_fingerprint_index/CORE_0_3_2_4_1_2_fingerprint_index.md
    - name: gate_rule
      path: node_0_3_2_4_1_3_gate_rule/CORE_0_3_2_4_1_3_gate_rule.md
    - name: term_graph_candidates
      path: node_0_3_2_4_1_4_term_graph_candidates/CORE_0_3_2_4_1_4_term_graph_candidates.md
---

# CORE 0_3_2_4_1 — matching

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.matching
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

- [walk](node_0_3_2_4_1_0_walk/CORE_0_3_2_4_1_0_walk.md) — `walk.step(state, instruction) -> state` - one reference step on a symbolic state; the walk from i is shared by every j, so the whole body costs N² steps, never N³.
- [liveness](node_0_3_2_4_1_1_liveness/CORE_0_3_2_4_1_1_liveness.md) — `liveness(E, i, j) -> live_interface` - one backward pass per i gives, for every j, what the segment reads from before i and what it writes that is read after j (registers and flags).
- [fingerprint_index](node_0_3_2_4_1_2_fingerprint_index/CORE_0_3_2_4_1_2_fingerprint_index.md) — `FingerprintIndex` - every unit's term evaluated at k concrete points, edge values first, keyed by the k-tuple; `lookup(fingerprint)` returns the units that agree at every point.
- [gate_rule](node_0_3_2_4_1_3_gate_rule/CORE_0_3_2_4_1_3_gate_rule.md) — `gate_rule(E, i, j, t, u)` - if `Term.normalize(t) == Term.normalize(u.term)`: IDENTICAL; else z3 at 3,000 ms: PROVED / DISPROVED / UNDECIDED.
- [term_graph_candidates](node_0_3_2_4_1_4_term_graph_candidates/CORE_0_3_2_4_1_4_term_graph_candidates.md) — `term_graph_candidates(E) -> sub-graphs` - the second candidate source: connected sub-graphs of the body's data-flow term instead of text ranges, so a computation the compiler interleaved with another is still one candidate.

## definition

Task rm1's algorithm: contiguous segments and, second, connected
sub-graphs of the body's term, matched to the language's own units by
fingerprint and decided by z3. Sound by construction; incomplete by
design (it finds what is structurally present).

`segment`, `live interface`, `rewrite rule`
- as `Research/GLOSSARY.md` states them.

```
index = FingerprintIndex(units_of(lang))            # once, M units
for E in emulator_arch_units(lang):
    for i in range(N):
        state = fresh_symbolic_inputs()
        for j in range(i, N):
            state = walk.step(state, E[j])          # one step per (i, j): N² in all
            t = project(state, liveness(E, i, j))
            for u in index.lookup(fingerprint(t)):  # usually 0 or 1
                gate_rule(E, i, j, t, u)            # identical text, else z3
```
