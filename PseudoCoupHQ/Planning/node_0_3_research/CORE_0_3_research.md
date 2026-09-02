---
id: hq.research
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: research
    path: Planning/node_0_3_research/CORE_0_3_research.md
super_node:
    name: hq
    path: ../CORE_0.md
sub_nodes:
    - name: kind_signature_clustering
      path: node_0_3_0_kind_signature_clustering/CORE_0_3_0_kind_signature_clustering.md
    - name: dominant_intentions
      path: node_0_3_1_dominant_intentions/CORE_0_3_1_dominant_intentions.md
    - name: kind_fuzz_clustering
      path: node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md
    - name: type_vocabulary
      path: node_0_3_3_type_vocabulary/CORE_0_3_3_type_vocabulary.md
    - name: data_representation
      path: node_0_3_4_data_representation/CORE_0_3_4_data_representation.md
    - name: compiler_graph
      path: node_0_3_5_compiler_graph/CORE_0_3_5_compiler_graph.md
    - name: interp_feeder
      path: node_0_3_6_interp_feeder/CORE_0_3_6_interp_feeder.md
    - name: remaining_languages
      path: node_0_3_7_remaining_languages/CORE_0_3_7_remaining_languages.md
---

# CORE 0_3 — research

## metadata

- **id:** hq.research
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hq](../CORE_0.md)

## sub_nodes

- [kind_signature_clustering](node_0_3_0_kind_signature_clustering/CORE_0_3_0_kind_signature_clustering.md) — Objective clustering of grammar kinds across languages, to give `ur.kinds` and the intentions vocabulary an empirical basis instead of hand-judged tables.
- [dominant_intentions](node_0_3_1_dominant_intentions/CORE_0_3_1_dominant_intentions.md) — Empirical grounding of dominant intentions by RUNTIME equivalence, so they stop being almost entirely by hand (the owner, 2026-08-13).
- [kind_fuzz_clustering](node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md) — **Cluster KINDS by measured behavior, using an automated fuzzer.** the owner's naming, 2026-08-14: "oh kinds.
- [type_vocabulary](node_0_3_3_type_vocabulary/CORE_0_3_3_type_vocabulary.md) — > **SUPERSEDED 2026-08-15** by > [data_representation](../node_0_3_4_data_representation/CORE_0_3_4_data_representation.md): > the owner's three-layer clarification (data / representation / > operation) showed this node's union answered the wrong > population — type-system taxonomy rather than the ways a > language can HOLD static content.
- [data_representation](node_0_3_4_data_representation/CORE_0_3_4_data_representation.md) — The THREE-LAYER anchor of the intentions research, confirmed by the owner 2026-08-15, and the home of layers 1 and 2.
- [compiler_graph](node_0_3_5_compiler_graph/CORE_0_3_5_compiler_graph.md) — A completely transparent, provable, logical trace connecting a high level variable to its low level form, built by turning the COMPILER'S OWN SOURCE into a graph and walking it.
- [interp_feeder](node_0_3_6_interp_feeder/CORE_0_3_6_interp_feeder.md) — Retrofitting the interpreter language tracks into the semantic pipeline.
- [remaining_languages](node_0_3_7_remaining_languages/CORE_0_3_7_remaining_languages.md) — Extracting arch-units for remaining uncompiled languages.

## definition

Line-wide research: questions that go beyond any specific PC version
but whose answers the versions apply. Founded 2026-08-12 (the owner:
"PCHQ and we will add a research sub_node to PCHQ planning and then
a literal Research folder in PCHQ"). Deliberately LIGHTER rigor than
version-repo planning (the owner, same ruling: "as thorough as needed but
not nearly as rigorous as our PCv5 deep dive").

Artifacts live in `<WORKSPACE_DIR>/PseudoCoupHQ/Research/` (scripts,
data, extracted tables); the record of what was learned lives in
PCHQ `DevComms/` logs; this branch holds only the standing shape of
each research line.

## topics

- **objective kind clustering** (opened 2026-08-12). The problem:
  hand-judged ts_kind → ur_kind bucketing produced 42 DUAL and 37
  UNCERTAIN rows out of 163 for ONE language (PCv5 log_008); across
  12 languages with grammar churn, the decision/maintenance overhead
  is unacceptable (the owner). The direction: decisions as objective as
  possible, very light interpretation — machinery that clusters
  kinds from grammar-shipped features. Initial features (the owner):
  arity, type (input, output). All three ship uniformly in every
  grammar's `src/node-types.json` (`multiple`/`required` per slot;
  per-slot allowed-kind sets; supertype memberships). Cross-language
  type connection must be exportable as data and imported per
  language. First handful of languages: rust, python, kotlin, dart,
  c/cpp. Low-hanging fruit first; see what interpretation remains
  after the objective layer has done its work.
