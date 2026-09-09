---
id: hq.research.data_representation
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: hq.research.type_vocabulary
designation: grouping
node:
    name: data_representation
    path: Planning/node_0_3_research/node_0_3_0_intentions/node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md
super_node:
    name: intentions
    path: ../CORE_0_3_0_intentions.md
sub_nodes: []
---

# CORE 0_3_0_4 — data_representation

## metadata

- **id:** hq.research.data_representation
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** hq.research.type_vocabulary

## super_node

- [intentions](../CORE_0_3_0_intentions.md)

## sub_nodes

*(none yet)*

## definition

The THREE-LAYER anchor of the intentions research, confirmed by the owner
2026-08-15, and the home of layers 1 and 2. Every work package in
this research line must state which layer it serves before it runs.

the owner's statement that fixed the layers:

> "if i have data files (such as csv), the content of the data is
> agnostic to specific language data structure dynamics. dynamics
> being things like `.append` vs structure such as a list where it
> is expandable on the heap. my thought was that in all the basic
> ways that the data can be imported, how can that data be
> represented in a language and how can that data be operated on
> (in ways that the compiler knows, and not builtin stuff)?"

- **Layer 1 — the data.** Static content, no language, no dynamics.
  Owned HERE.
- **Layer 2 — the representations.** Per language: the ways that
  content can be held. One piece of data, several representations
  per language (a sequence of numbers: python list or tuple; rust
  Vec, array, or slice). Owned HERE.
- **Layer 3 — the operations.** Per representation: what the
  COMPILER knows how to do to it (never builtins). The dynamics —
  the thing MEASURED, never part of the data. Owned by the co-node
  `kind_fuzz_clustering`.

The pipeline: same data in → each representation → each compiler
operation → observe → cluster across languages. Two representations
in different languages that admit the same data and answer the same
under the same operations are equivalent — discovered, not
declared.

## layer 1 — RULED 2026-08-15

The data model:

```
nothing            the absent value
truth value        two values
whole number       unbounded as content
fractional number  decimal text as content
text               unicode
sequence           ordered run of elements
keyed grouping     name -> element
nesting            elements may be any of the above
identity marks     two positions may name ONE node
                   (anchors/references; admits shared
                   nodes and cycles)
```

- **Complete for content, by the serialization argument**: if a
  representation can hold imported data at all, that data can be
  written out and read back — which is exactly expressibility in
  these forms. (Why JSON/CSV carry arbitrary data between languages
  sharing nothing; essentially the JSON model + identity marks,
  identity being JSON's known limit.)
- **Edge values are part of the data**: the census fracture lists
  are the edge sets (max+1, NaN, -0.0, "e-acute", the 4-byte
  codepoint, missing key...). Designed once, mostly already
  derived.
- **Deliberate exclusion**: things whose content is BEHAVIOR (a
  function's content is code; a channel's is a conduit) are not
  data — they enter at layer 3 as things a probe constructs and
  applies. Not a gap; a definition.
- **Completeness is AUDITED, not asserted**: for every layer-2
  representation, one question — can it load layer-1 data? Every
  "no" is either behavioral (files to layer 3, expected) or a
  genuine layer-1 gap (the model grows, append-only).

## layer 2 — the plan

1. **the data file** — write layer 1 as one actual shared file
   (values + edge values + identity-marked shapes), the single
   synthetic source every language loads.
2. **representation enumeration** — per language, the table: which
   language shapes can hold each layer-1 form. Largely mechanical;
   the superseded union extraction (below) is raw reference
   material for it.
3. **the audit** — the load-question over the whole table; refusals
   classified behavioral vs gap.
4. hand-off: the (data, representation) pairs are the inputs
   `kind_fuzz_clustering` fuzzes at layer 3.

## what this supersedes, and why

`type_vocabulary` (node_0_3_3) asked "what types do the compilers
enumerate" and answered with a 59-row union mixing representations
with type-checker machinery — measured honestly, but at the wrong
population for the owner's purpose, and it conflated what the census had
also conflated: STRUCTURE (layer 2) with DYNAMICS (layer 3), while
the data layer (1) was never written down at all. Its extraction
(`Research/type_vocabulary/raw/`, log_022) is kept as raw reference
for layer 2's enumeration; its 59-row step-B ruling is CANCELLED.
The six verified census objects are re-read as: layer-2
representations with layer-3 measurements attached — all still
valid as measurements; only the framing moves.

## record

- artifacts: `PseudoCoupHQ/Research/data_representation/`
- co-nodes: `dominant_intentions` holds the verified census
  (layer-3 measurements of specific layer-2 representations) and
  the harness; `kind_fuzz_clustering` owns layer 3;
  `kind_signature_clustering` supplies the grammar-side data.
