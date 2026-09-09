---
id: hq.research.dominant_intentions.support.BRAINSTORM_basis_data_structures
status: draft
---

# SUPPORT_BRAINSTORM — basis data structures

2026-08-13, from conversation with the owner. Fresh derivation, no
old-project artifacts consulted (the owner's standing instruction for this
node: lessons carry forward, artifacts do not). Level-1 list is
PROPOSED, awaiting the owner's ruling; level 0 is closed by the machine.

## level 0 — what the machine itself has (closed list)

```
fixed-width integer     8/16/32/64 bits, signed or
                        unsigned; the only numbers
                        the hardware natively has
float                   IEEE 754, 32 or 64 bit
address                 a place in memory, not a
                        value; "where", never "what"
block                   a run of adjacent memory
                        cells; the machine's only
                        container
```

Everything is these. A boolean is an integer wearing a costume; a
character is an integer; a struct is a block with a floor plan.

## level 1 — what every engine builds from level 0 (proposed, five)

Constructions that recur across all five engine bases (LLVM, JVM,
CLR, V8, own-VM) before any language shows up:

```
boxed value        a level-0 value wrapped in a
                   block with a tag saying what
                   it is (how python knows 5 is
                   an int at runtime)
growable buffer    block + count + capacity;
                   re-allocated bigger when full —
                   the machinery under every list,
                   vec, and string
byte string        growable buffer of integers +
                   an encoding convention saying
                   how bytes become text
hash table         blocks of (key, value) pairs
                   reached by address arithmetic
                   on the key — under every dict,
                   map, and object
tagged record      a block whose first cells say
                   which floor plan the rest
                   follows — how engines represent
                   "one of several shapes"
```

## the composition claim

Every high-level data structure of the 12 target languages is a
composition of these nine — and languages on the SAME base still
compose differently (the owner's caveat, built in). Worked examples:

- "integer": rust = level-0 raw (i64, nothing added); python =
  boxed growable buffer OF integers (whence unboundedness);
  javascript = the float (no integer costume at all).
- "array": rust Vec = (address, count, capacity) over a block;
  python list = same shape but the block holds addresses of boxed
  values; php "array" = a hash table with an ordering bolted on.
  Same developer word, different level-1 parts entirely.

## what the composition table is FOR (open, the owner: "i dont fully
understand the influence it will have")

Working answers, none settled:

- it tells the dominant object what it must CONTAIN (the union of
  the compositions' capabilities) and the vector tests what they
  must PROBE (each place two compositions differ is a fracture is
  a test vector).
- it prices polyfills: a target whose composition lacks a part
  shows exactly what must be supplied.
- the engine bases predict where compositions repeat (same base,
  often same parts) — a prediction the runtime results can check.

## the dominant container question (the owner, 2026-08-13)

the owner: construct a dominant structure doing what all languages do —
union of features, "dict-list", contiguous access AND keyed access
— possibly "strictly the efficiency infimum".

Standing observations from the discussion (see the conversation
log; thoughts in the reply of the same date):

- existence proofs exist: php's array IS a dict-list; V8's arrays
  switch representation silently (contiguous while indices stay
  dense, hash mode when they stop) — the union container ships in
  production engines today.
- the efficiency-infimum worry refines to PAY-PER-FEATURE: with an
  adaptive representation, the cost of the union is only paid at
  the moment a beyond-the-costume feature is first touched — which
  is the owner's own inertness requirement, restated as an efficiency
  property.
- true contradictions to enumerate by testing, not argument:
  mostly VALUE semantics (fixed-width wrap vs bignum overflow),
  not container semantics. Pointers/indirection (the owner's instinct)
  solve type-mixing at the cost of cache locality.
