---
id: hq.research.arch_unit_oracle.simplification.emulator_arch_units
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: emulator_arch_units
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_0_emulator_arch_units/CORE_0_3_2_4_0_emulator_arch_units.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes:
    - name: extract
      path: node_0_3_2_4_0_0_extract/CORE_0_3_2_4_0_0_extract.md
    - name: attest
      path: node_0_3_2_4_0_1_attest/CORE_0_3_2_4_0_1_attest.md
    - name: population
      path: node_0_3_2_4_0_2_population/CORE_0_3_2_4_0_2_population.md
---

# CORE 0_3_2_4_0 — emulator_arch_units

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.emulator_arch_units
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

- [extract](node_0_3_2_4_0_0_extract/CORE_0_3_2_4_0_0_extract.md) — `extract(certificate) -> (body, term)` - compile at the certificate's flags, carve at the symbol, walk through the reference.
- [attest](node_0_3_2_4_0_1_attest/CORE_0_3_2_4_0_1_attest.md) — `attest(body)` - one row in the canon store: the body, its term text, `origin: emulation`, the cell, the tier, the certificate id.
- [population](node_0_3_2_4_0_2_population/CORE_0_3_2_4_0_2_population.md) — `Population` - the set of emulator arch-units per language, with counts by tier (tier 1 / schema / backstop) and by outcome of the compiler's own collapse (LANDED / NOT COLLAPSED).

## definition

The population every path reads: each proved emulation's compiled body
as an arch-unit of its language, with its cell, tier and certificate.

`emulator_arch_units.extract(certificate)`
- compile the certificate's source with its compiler and flags, carve
  at the symbol, walk the body through the reference: the body and its
  term, beside the certificate that proved it.

`emulator_arch_units.attest(body)`
- register the body in the language's canon store with `origin:
  emulation`, its cell and tier, so `set_of_arch_units_for_each_lang`
  grows by exactly these and nothing else is re-derived.

```
for cert in bank where cert.verdict in (proved, identical):
    body, term = extract(cert)
    attest(body)                       # now a member of set_of_arch_units_for_each_lang
```
