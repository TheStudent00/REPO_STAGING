---
id: hq.research.lean_proof_path_resistant_to_churn.lean_expr.universal
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: universal
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_2_lean_expr/node_0_3_3_2_6_universal/CORE_0_3_3_2_6_universal.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_3_2_6 — universal

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.lean_expr.universal
- **level:** 4
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_expr](../CORE_0_3_3_2_lean_expr.md)

## sub_nodes

*(none yet)*

## definition

One universal numeric type in Lean, `(sign, mant, expo)`, and every primitive kind as a constraint on it plus a projection of an exact result back into the kind: unsigned n-bit, signed n-bit, bool, IEEE binary, fixed-point.

the owner, 2026-09-15, verbatim: "universal type: (sign, mant, expo) where:
sign is length-1 bit_vec; mant is unbounded bit_vec; expo is (bit_vec,
bit_vec), where the first bit_vec is length-1 and the second bit_vec is
unbounded". The value is `(-1)^sign * mant * 2^expo`, `mant` read as an
integer from its least significant bit, `expo = (-1)^expo.sign *
expo.mag`; an integer is `expo = 0`.

Written once, by hand, general in its parameters. Nothing in it is keyed
by an instruction name or an operator token.

Code, two modules beside the proof project's own Lean sources:

- `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_harness/leanpath_src/Universal.lean`
  — the object and its exact operations; imports nothing.
- `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/lp1_harness/leanpath_src/Kinds.lean`
  — the five kinds, the IEEE operations, the bodies, the checks;
  imports `Universal` only.

### the exact operations on the universal object

- `add sub mul`: align both to the smaller exponent, then integer
  arithmetic; nothing lost.
- `divT remT`: `Int.tdiv` / `Int.tmod` of the aligned mantissas, which
  is Sail's own integer division; a zero divisor gives zero (the model's
  own guard, quotient `-1`, stays the model's).
- `cmp`: compare the aligned mantissas.
- shifts: `shl` moves the exponent; `shrL` / `shrA` read the object at
  a width.
- `band bor bxor bnot`: at a width, because a bit operation has no
  meaning without one (`not` least of all).
- `splitAt q`: the one primitive rounding needs, `(sig, guard, sticky)`.

### the five kinds

One signature for all five: the rounding mode goes in, the five flags
come out.

| kind | constraint (`holds`) | projection (`proj`) |
| --- | --- | --- |
| unsigned n | sign 0, expo 0, mant ≤ n bits | wrap modulo 2^n |
| signed n | expo 0, mant < 2^(n-1) with the sign | wrap modulo 2^n |
| bool | sign 0, expo 0, mant ≤ 1 bit | nonzero to 1 |
| IEEE (e, m) | on the format's grid, exponent in range | round (five modes), five flags; ±∞ and NaN are encodings, not universal objects |
| fixed (w, q) | expo held at q, mant fits w bits | round by the mode, then saturate or wrap; inexact and overflow flagged |

- The integer kinds ARE Sail's functions: `sailToBitsTruncate_eq_ofInt`
  proves Sail's `to_bits_truncate` (transcribed from the emit's
  `Prelude.lean` and the support library's `get_slice_int`) equal to
  `BitVec.ofInt`, the wrap the kinds project by, for every width
  (measured: proved by Lean, 2026-09-15).

### the IEEE part: covered and not yet

- Covered: decode to the five classes; subnormals; the model's five
  rounding modes (RNE RTZ RDN RUP RMM, encoded as the emit's
  `encdec_rounding_mode_forwards`); tininess after rounding; the five
  flags in the model's own bit order; add, sub, mul, div (exact, then
  rounded) and the five comparisons; any e, m (binary16/32/64 are three
  parameter values).
- Bodies today: 27 of the 67 float axioms in
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/leanpath/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM/RiscvExtras.lean`
  — the 12 add/sub/mul/div and the 15 Lt/Lt_quiet/Le/Le_quiet/Eq, each
  a definition in `Kinds.Axioms` of exactly its axiom's type.
- Not yet: 3 MulAdd, 3 Sqrt, 3 roundToInt, 31 conversions (integer to
  float, float to integer, float to float, `f32ToBF16`).
- Unverified: the values are checked against the host's IEEE doubles and
  known constants, not against Sail's softfloat, and no theorem about the
  IEEE part is proved yet.

### the axioms get bodies without editing the cache

The emit in `cache/` stays as Sail produced it. The substitution is a
documented, reversible one-line rewrite per axiom, applied to a working
copy only:

    axiom riscv_f64Add : BitVec 3 → BitVec 64 → BitVec 64 → (BitVec 5 × BitVec 64)
    ->  def   riscv_f64Add := Kinds.Axioms.riscv_f64Add

undone by restoring the file from `cache/`. The other choice, a theorem
`riscv_f64Add rm a b = Kinds.Axioms.riscv_f64Add rm a b`, touches no
file but can only be assumed, never proved, because an axiom has no
body. Not run yet: it needs the model rebuilt in a working copy.

### how it is built

- Lean `leanprover/lean4:v4.29.0`, the proof project's pin.
- Checked inside the proof project's lake environment on the tower with
  `podman exec` (no lane): `Universal.lean` compiled with
  `lean --root=<leanpath_src> -o` into a scratch directory
  (`/work/universal_olean`), then `Kinds.lean` with that directory added
  to `LEAN_PATH`.
- Not yet in the proof project's `roots`. Adding `"Universal", "Kinds"`
  to the `Leanpath` lib in its lakefile is the one-line registration; it
  was not made, because it changes the project the running lanes use.
