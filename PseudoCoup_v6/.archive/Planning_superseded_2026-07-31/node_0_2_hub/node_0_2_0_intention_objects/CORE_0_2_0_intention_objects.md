---
id: pcv6.hub.intention_objects
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_2_0 — Intention Objects

The 11-object minimum intention set as runnable PC objects. Each
object = a canon semantics (from `pc_intentions.json` `canon` and
`minimum_set` fields) + a backing implementation + a border.

## Design rules

- **Canon-from-data**: an object's semantics come from its canon
  entry, never re-decided in code. Example: PC.map is
  insertion-ordered (P10, "majority + determinism"); PC.string is
  the Swift view model (P7 — no default indexing unit, explicit
  view per access); PC.int64 traps on overflow with wrapping only
  by explicit spelling (P2, Swift/Rust canon).
- **Backing tiers, chosen per object and recorded**: (a) native
  Python already agrees (PC.bool, PC.float64 — basis_audit
  "native"); (b) polyfill wrapper carries the semantics (PC.int64
  family — T4's FixedWidthInt is the seed); (c) inserted slice
  carries them (qualified arithmetic — T6's chain). One object
  may mix tiers per operation; the LEDGER records which tier
  backs each, so no operation's provenance is ambiguous.
- **Uniform law applies per object**: every operation routes
  through the object's chosen backing or none does.

## Work items (each delegation-ready once T6 insertion lands)

1. PC.int64/PC.uint64 first — T4 wrappers as the default tier,
   the inserted chain as the qualified tier; differential grid vs
   native rustc as acceptance (the PCv5 grid pattern, rebuilt
   PCv6-side).
2. PC.bool/PC.float64 — thin: legislated printing + NaN edges
   (P5 verdict) as the only work.
3. PC.list/PC.map/PC.set/PC.record — canon semantics
   (single-owner list, insertion-ordered map/set, reference
   record + explicit .copy()); acceptance = the divergence-suite
   classes re-run against the PC objects.
4. PC.string/PC.bytes — the Swift-view model; largest single
   design surface; plan its own depth node when reached.
5. PC.bigint/PC.decimal/PC.function_value — per canon entries.

## Acceptance shape (uniform)

Per object: a semantics grid from the canon statement (not from
any prior implementation), executed against the PC object;
divergence-suite classes touching the object re-run green; ledger
records the backing tier per operation.
