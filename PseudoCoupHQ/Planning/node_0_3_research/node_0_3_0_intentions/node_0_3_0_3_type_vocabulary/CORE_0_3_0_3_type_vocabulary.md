---
id: hq.research.type_vocabulary
level: 3
status: superseded
supersedes: null
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: type_vocabulary
    path: Planning/node_0_3_research/node_0_3_0_intentions/node_0_3_0_3_type_vocabulary/CORE_0_3_0_3_type_vocabulary.md
super_node:
    name: intentions
    path: ../CORE_0_3_0_intentions.md
sub_nodes: []
---

# CORE 0_3_0_3 — type_vocabulary

## metadata

- **id:** hq.research.type_vocabulary
- **level:** 3
- **status:** superseded
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [intentions](../CORE_0_3_0_intentions.md)

## sub_nodes

*(none yet)*

## definition

> **SUPERSEDED 2026-08-15** by
> [data_representation](../node_0_3_0_4_data_representation/CORE_0_3_0_4_data_representation.md):
> the owner's three-layer clarification (data / representation /
> operation) showed this node's union answered the wrong
> population — type-system taxonomy rather than the ways a
> language can HOLD static content. The extraction
> (`Research/type_vocabulary/raw/`, log_022) is kept as raw
> reference for layer 2; the 59-row step-B ruling is cancelled.


Derive the COMPLETE set of data structures the target compilers
understand, by extracting each compiler's own type enumeration and
taking the union — then grow the verified instrument set to cover
it.

Founded 2026-08-14 on the owner's question: "what will it take to get a
complete set of these data structures and verify them all?" The
answer's first step is this node; the rest is census work in the
co-node `dominant_intentions`.

The six verified dominants (boolean, float, integer, string, list,
dict) are the instruments the fuzzing line measures with. They are
not complete: an estimate against rustc's MIR put roughly 60% of
the lowering vocabulary within reach of the six, with `Call`,
`Ref`, `Aggregate`, `Discriminant` and `Yield` gated behind
instruments that do not exist yet (function, reference,
struct/tuple, enum). UNVERIFIED estimate; this node replaces it
with a measurement.

## the method — derive, never hand-list

Every compiler carries a closed enumeration of the types it
understands, in its own source or specification:

- rustc `TyKind` — Bool, Char, Int, Uint, Float, Str, Adt
  (struct/enum), Array, Slice, Ref, RawPtr, FnDef, FnPtr, Dynamic,
  Closure, Coroutine, Tuple, Never
- go `types.Kind` — Bool, Int.., Float, Complex, String, Pointer,
  Array, Slice, Map, Chan, Struct, Interface, Func
- the JVM's type descriptors; the CLR's `ElementType`; CPython's
  core `PyTypeObject`s; and the equivalents for typescript,
  ruby, php, kotlin, dart, cpp, swift

Union those lists and THAT is the complete set — derived, not
invented. The same move that made the kind work objective
(`node-types.json` for grammar kinds); this is its type-side
counterpart.

Completeness is RELATIVE to the surveyed compilers, and the set is
append-only in spirit: a later language bringing a type none of
these has grows the union. Same posture as `ur.kinds`.

## scope

All 12 target languages where the toolchain allows — swift is
installed and working in the sandbox as of 2026-08-14, so it is IN
unless something blocks it (the owner, 2026-08-14: "if we can include all
12 languages, great. if we can only work on 11, also fine").

Single-language types stay in the union. the owner's ruling, 2026-08-14:
"if they truly dont have equivalents in other languages, not a
problem. in fact, its those gaps the Hub is trying to fill." So
go's channel, csharp's decimal, python/go's complex are findings,
not noise.

## first-pass expectation (to be replaced by measurement)

Beyond the six: nothing/unit, char, tuple, struct/record,
enum/variant, reference/pointer, function/closure, interface
(dynamic dispatch), set, channel, complex, decimal, bigint — call
it a dozen, some base-specific.

## plan of record

A. **extract + union** (this node's own work): pull each
   compiler's type enumeration, normalize spellings, emit the
   union table with per-language presence and the count. The first
   number the owner sees. Measurement only; no judgments about which
   are instruments.
B. **the owner rules the set**: which entries become verified
   instruments, which are derived from others (a `set` may be a
   dict with ignored values), which are out of scope. The only
   step that cannot be delegated.
C. **census pages** for each adopted instrument, in the settled
   owner format (structure / operation / border) — work of the
   co-node `dominant_intentions`, not this one.
D. **verify by harness** — the existing harness at
   `Research/dominant_intentions/harness/`; machine time is
   negligible (41 facts x 14 columns ran in 70 seconds).

Expect the fracture-rich instruments (nothing, function) to need
longer pages than dict's, and a real hand pass. the owner has accepted
that cost in advance.

## record

- artifacts: `PRIVATE/PseudoCoupHQ/Research/type_vocabulary/`
- co-nodes: `dominant_intentions` owns the census and holds the
  verified instruments; `kind_fuzz_clustering` is the consumer —
  every instrument added widens the slice of each compiler's
  lowering vocabulary that fuzzing can reach;
  `kind_signature_clustering` supplies the precedent for
  derive-don't-hand-list.
