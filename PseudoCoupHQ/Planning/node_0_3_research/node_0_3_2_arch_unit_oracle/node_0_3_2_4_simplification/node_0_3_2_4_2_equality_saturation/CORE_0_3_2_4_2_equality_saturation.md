---
id: hq.research.arch_unit_oracle.simplification.equality_saturation
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: equality_saturation
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_2_equality_saturation/CORE_0_3_2_4_2_equality_saturation.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes:
    - name: rule_set
      path: node_0_3_2_4_2_0_rule_set/CORE_0_3_2_4_2_0_rule_set.md
    - name: egraph
      path: node_0_3_2_4_2_1_egraph/CORE_0_3_2_4_2_1_egraph.md
    - name: extract
      path: node_0_3_2_4_2_2_extract/CORE_0_3_2_4_2_2_extract.md
---

# CORE 0_3_2_4_2 — equality_saturation

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.equality_saturation
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

- [rule_set](node_0_3_2_4_2_0_rule_set/CORE_0_3_2_4_2_0_rule_set.md) — `RuleSet` - mined rules (from matching) and the algebraic identities, each with its certificate; loading a rule without one is refused.
- [egraph](node_0_3_2_4_2_1_egraph/CORE_0_3_2_4_2_1_egraph.md) — `EGraph` - the equality graph over term nodes (egg's shape): classes of equal terms, rules applied to every class; saturation until a fixed point or the budget.
- [extract](node_0_3_2_4_2_2_extract/CORE_0_3_2_4_2_2_extract.md) — `extract(g, cost) -> body` - the cheapest representative per class under a cost that counts the language's own units; the extracted body is re-gated against E before it is recorded.

## definition

Every form the rule set can generate, held at once in an e-graph, and
the cheapest extracted; no greedy ordering trap. Complete over the
rule set, and no further.

`rule set`
- the rules mined by matching, plus the algebraic identities the
  reference already knows (`x*2 == x+x`, `x/8 == x>>3` unsigned,
  `(a&b)|(a&~b) == a`, ...), each carried with a certificate.

```
g = EGraph(term_of(E))
saturate(g, rule_set, budget)          # apply every rule everywhere until nothing changes or the budget ends
best = extract(g, cost = instruction_count over units_of(lang))
```
