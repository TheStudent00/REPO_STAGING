---
id: hq.research.intentions
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: intentions
    path: Planning/node_0_3_research/node_0_3_0_intentions/CORE_0_3_0_intentions.md
super_node:
    name: research
    path: ../CORE_0_3_research.md
sub_nodes:
    - name: kind_signature_clustering
      path: node_0_3_0_0_kind_signature_clustering/CORE_0_3_0_0_kind_signature_clustering.md
    - name: dominant_intentions
      path: node_0_3_0_1_dominant_intentions/CORE_0_3_0_1_dominant_intentions.md
    - name: kind_fuzz_clustering
      path: node_0_3_0_2_kind_fuzz_clustering/CORE_0_3_0_2_kind_fuzz_clustering.md
    - name: type_vocabulary
      path: node_0_3_0_3_type_vocabulary/CORE_0_3_0_3_type_vocabulary.md
    - name: data_representation
      path: node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md
---

# CORE 0_3_0 — intentions

## metadata

- **id:** hq.research.intentions
- **level:** 2
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [research](../CORE_0_3_research.md)

## sub_nodes

- [kind_signature_clustering](node_0_3_0_0_kind_signature_clustering/CORE_0_3_0_0_kind_signature_clustering.md) — Objective clustering of grammar kinds across languages, to give `ur.kinds` and the intentions vocabulary an empirical basis instead of hand-judged tables.
- [dominant_intentions](node_0_3_0_1_dominant_intentions/CORE_0_3_0_1_dominant_intentions.md) — Empirical grounding of dominant intentions by RUNTIME equivalence, so they stop being almost entirely by hand (the owner, 2026-08-13).
- [kind_fuzz_clustering](node_0_3_0_2_kind_fuzz_clustering/CORE_0_3_0_2_kind_fuzz_clustering.md) — **Cluster KINDS by measured behavior, using an automated fuzzer.** the owner's naming, 2026-08-14: "oh kinds.
- [type_vocabulary](node_0_3_0_3_type_vocabulary/CORE_0_3_0_3_type_vocabulary.md) — > **SUPERSEDED 2026-08-15** by > [data_representation](../node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md): > the owner's three-layer clarification (data / representation / > operation) showed this node's union answered the wrong > population — type-system taxonomy rather than the ways a > language can HOLD static content.
- [data_representation](node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md) — The THREE-LAYER anchor of the intentions research, confirmed by the owner 2026-08-15, and the home of layers 1 and 2.

## definition

The research project that establishes what developers MEAN by a
language's features, measured from the language side: what data is,
how each language holds it, and what each compiler's operators do to
it when run. It is the language-level half of the objective in
[research](../CORE_0_3_research.md) §1: it supplies the dominant
TYPES (the holders every language's types resolve to) and the
behaviour census that names an operator's modes; the machine-level
half, the arch-units, is
[operator_equivalence](../node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md).

Founded as separate lines from 2026-08-12; made one project
2026-09-06 by the owner's restructure ruling. Its sub-nodes were the
research node's first five co-nodes and keep their ids.

## 1. the owner's definition of an intention, of record

An intention is what a developer means while using a language's
feature. A DOMINANT intention is an object satisfying all
sub-intentions, such that once defined or polyfilled in every
language it can hot-swap with its sub-equivalent object in any
language without disturbing functional logic; the unused parts of
the dominant intention are inert (the owner, 2026-08-13, recorded in
[dominant_intentions](node_0_3_0_1_dominant_intentions/CORE_0_3_0_1_dominant_intentions.md)).

That definition is testable by execution: for every input in the
sub-object's domain, the dominant and the sub-object produce the
same result. Every sub-node here is one instrument for that test or
one input to it.

## 2. The three layers, which order the sub-nodes

Ruled by the owner 2026-08-15; home
[data_representation](node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md).
Every work package in this project states which layer it serves.

- **Layer 1, the data**: static content, no language. Nine forms:
  nothing, truth, whole, fractional, text, sequence, keyed grouping,
  nesting, identity marks. Ruled complete for content by the
  serialization argument.
- **Layer 2, the representations**: per language, the ways that
  content can be held. One datum, several representations per
  language.
- **Layer 3, the operations**: per representation, what the COMPILER
  can do to it, never builtins. The thing measured.

## 3. The sub-nodes, in relation

- [data_representation](node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md)
  owns layers 1 and 2: the data model and the per-language holder
  tables. It is the anchor the other four answer to.
- [dominant_intentions](node_0_3_0_1_dominant_intentions/CORE_0_3_0_1_dominant_intentions.md)
  verified the six basic data structures by execution across eleven
  languages: boolean, float, integer, string, list, dict. Zero
  contradictions. These are the calibrated instruments: every later
  probe applies an operator to a KNOWN input, so its answer is
  readable.
- [kind_fuzz_clustering](node_0_3_0_2_kind_fuzz_clustering/CORE_0_3_0_2_kind_fuzz_clustering.md)
  owns layer 3: generate a minimal script per operator token over
  the verified holders, run it, record the answer, the raise, or the
  compile refusal, and cluster kinds across languages by what they
  DID. Level-1 and level-2 probes ran for the twelve languages
  (logs 052 to 062); phase 4, relate and cluster, is not run.
- [kind_signature_clustering](node_0_3_0_0_kind_signature_clustering/CORE_0_3_0_0_kind_signature_clustering.md)
  clusters the same kinds by DECLARED signature from the grammars'
  `node-types.json` (arity, slot types, supertypes) across every
  tree-sitter grammar. Done through its step 4. It and the fuzz line
  are mutually checkable: agreement is evidence, disagreement a
  finding.
- [type_vocabulary](node_0_3_0_3_type_vocabulary/CORE_0_3_0_3_type_vocabulary.md)
  is SUPERSEDED (2026-08-15) by data_representation: its 59-row union
  mixed representations with type-checker machinery. Kept as raw
  reference for layer 2's enumeration; its ruling is cancelled.

## 4. What this project delivers to the Hub, and its state

| deliverable | state 2026-09-06 |
|---|---|
| the data model (layer 1) | ruled |
| the six verified holders per language | done, 11 languages |
| the operator behaviour census (layer 3, levels 1 and 2) | run for the twelve; results in `Research/kind_fuzz_clustering/` |
| relate-and-cluster over the census (phase 4) | not run; gated on the owner's review of the eleven design decisions (log 024 §6) |
| layer-2 representation tables for the non-scalar forms | planned (data_representation plan steps 1–3) |
| the grammar-side kind basis | done through step 4; 9 live interpretation decisions in log_010 §7 |

Its part in the master order
([research](../CORE_0_3_research.md) §4.2): step 3 uses its holder
classes for the type join; step 6, the aggregate forms, is where its
layer-2 tables for text, sequence, keyed and nesting become the
holders the probes are generated over.

## 5. Standing rules this project adds

- Only `lhs_canon`, `rhs_canon`, `output_canon` are scored; holder
  names, byte spellings and probe ids are carried for reading, never
  scored. Declines (REFUSE / RAISE / ABORT) are never scored; zero
  comparable keys means no connector.
- Alignment is by shared key, never by identical whole vectors.
  CONTRACT joins rows with the same key set and byte-identical
  outputs; GROUP draws a hull around a mutually-1.0 clique over a
  partial overlap; input overlap must be at least the output
  agreement (the owner's edge criterion).
- The canonical value form `[sign, mant, expo]` with a decimal
  mantissa in [1,2); no fractions in a visible column.
(All recorded in full in `PseudoCoupHQ/CLAUDE.md`.)

## 6. Open, the owner's

- The eleven design decisions gating phase 4 (log 024 §6).
- Whether type_vocabulary moves to `.archive/`.
- The dict gap in java/csharp/rust/cpp/kotlin and the boolean gap in
  kotlin, closable only by opening builtins (log 021 §6).

## 7. Record

- artifacts: `PseudoCoupHQ/Research/{kind_signature_clustering,dominant_intentions,kind_fuzz_clustering,data_representation,type_vocabulary}/`
- logs: PCHQ DevComms 008 to 039 and 052 to 062.
