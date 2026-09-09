---
id: hq.research.kind_signature_clustering
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: kind_signature_clustering
    path: Planning/node_0_3_research/node_0_3_0_intentions/node_0_3_0_0_kind_signature_clustering/CORE_0_3_0_0_kind_signature_clustering.md
super_node:
    name: intentions
    path: ../CORE_0_3_0_intentions.md
sub_nodes: []
---

# CORE 0_3_0_0 — kind_signature_clustering

## metadata

- **id:** hq.research.kind_signature_clustering
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [intentions](../CORE_0_3_0_intentions.md)

## sub_nodes

*(none yet)*

## definition

Objective clustering of grammar kinds across languages, to give
`ur.kinds` and the intentions vocabulary an empirical basis instead
of hand-judged tables. Graduated from a topic bullet 2026-08-12 when
the owner widened the scope from the 12 target languages to EVERY grammar
tree-sitter covers: "perform the analysis to see if we can generate
a robust basis for clustering to inform our `ur` design (including
intentions)". The 12 remain the transpilation targets; the wider set
is scaffolding for the basis.

## the standing shape

- **features come from grammar-shipped data only**
  (`src/node-types.json`: arity, input types, output positions;
  supertypes derived where undeclared). decisions as objective as
  possible, very light interpretation (the owner's founding constraint).
- **the artifact is the merge tree / similarity spectrum, never one
  cut** (the owner, 2026-08-12): clusters are queries at a threshold;
  branching across the whole spectrum is observed meta-language
  structure. visual: interactive dendrogram/icicle explorer.
- **full population always** — no sampling, no hand-picked answer
  keys as primary instruments. validation is hold-out against the
  grammars' own declarations (reference frame, not oracle).
- **take every grammar, tag by category** (general-purpose / query /
  markup / config / notation), report per category, never
  pre-filter (the owner: "hells yeah. agreed."). grammar quality is
  measured (role coverage, supertype presence, arity discipline),
  and tiering by quality is a live interpretation decision to rule
  explicitly.

## plan of record (2026-08-12)

1. enumeration survey — how many grammars ship node-types.json,
   sizes, quality signals, category tags. measurement only.
2. decision-6 fix — output positions as COUNTS, not sets (1,271
   identical-feature pairs at 5 languages measure the current
   resolution floor; saturation compounds at scale).
3. scaled ingestion — all grammars; sparse spectrum (per-kind top-k
   counterparts with merge heights) replacing the dense matrix.
4. basis report — widest-band many-language clusters cross-referenced
   against the 11 minimum-set objects and categories A-J: which
   intentions have empirical clusters, and which clusters have no
   intention bucket (evidence of missing vocabulary).

## record

- artifacts: `PseudoCoupHQ/Research/kind_signature_clustering/`
- reports so far: PCHQ DevComms log_008 (landscape, 6 languages),
  log_009 (first pass, purity 0.685), log_010 (spectrum + hold-out,
  AUC 0.712/0.804). live interpretation decisions: log_010 §7
  (9 remain).
