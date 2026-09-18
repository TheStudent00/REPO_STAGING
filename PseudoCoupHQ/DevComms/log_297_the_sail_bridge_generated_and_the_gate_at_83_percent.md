# log 297 — the Sail bridge, generated, and the gate at 83%

2026-09-17. Follows log 296. One blocker, named at the end of 296, is closed.
It took five lanes and three of them were wrong in ways worth keeping.

## 1. What was blocking

Sail's Lean backend defines every comparison over `Int`:

```lean
def zopz0zI_u (x y : BitVec k_n) : Bool :=
  ((BitVec.toNatInt x) <b (BitVec.toNatInt y))
```

`<b` is `Int.blt`. `bv_decide` cannot bitblast it — it abstracts the whole
comparison and answers with a spurious counterexample. `BitVec.ult` is the
same predicate and IS inside the fragment. Sail ships no lemma between them:
`@[simp_sail]` marks the definitions so they UNFOLD, which is what produces
the Int spelling, and a grep for `ult` or `blt` across the Sail Lean library
returns nothing.

## 2. Generated, not typed

`Bridges.lean` was hand-written and broke on a Lean minor version within
hours. So `leanpath/sail_bridge.py` READS each definition out of the Prelude,
takes the family from the conversion it uses (`toInt` signed, `toNatInt`
unsigned) and the relation from the comparison token, and writes the matching
BitVec spelling. A definition whose shape it does not recognise is SKIPPED AND
NAMED — a rename in Sail becomes a missing lemma, never a wrong one.

The proof is not guessed either. The generator's `matrix` mode emits one
theorem per (lemma, candidate tactic) so the run reports WHICH tactic carried.

## 3. Three wrong lanes, each measured

**l106 — the right lemmas in the wrong file.** All eight failed with
`Function expected at zopz0zI_s`. Not mathematics: scope. Sail's definitions
live inside the module's namespace under a stack of `open`s and the generator
had emitted a bare `import`. Every `#check` of a BitVec name passed in the
same run, which is what identified it. Fixed by taking the header from
`leanpath.strip.header_of` — the same function the gate's own files use.

**l107 — the bridge is real.** 8 of 8:

| family | lemmas | proved by |
|---|---|---|
| signed (`toInt`) | 4 | **`rfl`** — they ARE the BitVec predicate |
| unsigned (`toNatInt`) | 4 | `simp [def, conv, target]` |

**l108 — the bridge in, and nothing moved.** 0 of 35. The residuals said why
in one line: the simp set carried BOTH `zopz0zI_s`, the definition, AND
`sail_bridge_zopz0zI_s`, the rewrite back. **simp unfolds first**, so every
goal already read `(...).toInt <b (...).toInt` and the bridge had nothing to
match. A set cannot both unfold a definition and rewrite it.

**l109 — the definitions dropped.** 2 of 35 moved, both 64-bit equality. And
the residual showed the bridge FIRING — `.ult` where `Int.blt` had been — with
something else now abstract: the wrapper.

```lean
def bool_bit_forwards (arg_ : Bool) : (BitVec 1) :=
  match arg_ with | true => 1#1 | false => 0#1
```

`BitVec.ofBool` is that function, natively, and the identity holds by `rfl` —
checked on the toolchain before the generator was extended, not after.

**l110 — the second family.** 31 of 35 moved, 80 arch-units.

## 4. Where the integer layer now stands

| | classes | arch-units | share |
|---|---|---|---|
| **PROVED** | **131** | **542** | **83%** |
| UNDECIDED | 4 | 6 | 1% |
| NOT REACHED — the walk refused | 51 | 104 | 16% |

At the start of this session the gate had certified seven theorems on a
hand-picked dozen. It has now certified **542 arch-units**, by way of 131
class representatives.

The four left UNDECIDED are `au_425_go_mul_i32_i32` (which uses no comparison
at all — the bridge does not apply to it) and the three shift units,
`au_445_go_shr_i32_u64`, `au_448_go_shr_i64_u64` and one more: Sail's
arithmetic shift takes its count through `Int`, the other shape lane l103
named, and it needs its own bridge.

## 5. The integration, in one place

Getting this right by hand is two mistakes deep — l108 and l109 are both
"looks like hard mathematics, is actually a simp-set bug". So
`equals.simp_set_with_bridge` returns the set and the lemma text TOGETHER, and
a caller is given no way to take the drop without the emit. The two families
are read from the Prelude on demand and cached.

## 6. Two lists

Decided, recorded for audit:

- `leanpath/sail_bridge.py` written; it generates from the Prelude and names
  what it cannot recognise;
- l106's failure is recorded as scope, not mathematics, and the `#check` line
  that proved it is in the lane;
- l108's and l109's negative results are kept in full — they are the reason
  `simp_set_with_bridge` exists;
- lanes lp3_l106 through lp3_l110 used, batch `lp3`.

Awaiting the owner:

- the **51 NOT REACHED** are now the largest block, 104 arch-units, and they
  are the walk refusing a branch or a call rather than Lean failing. Widening
  the walk is the next real piece of engineering.
- the arithmetic-shift bridge would take the remaining 4. Same mechanism,
  small; say whether it is worth a lane now or should ride with the walk work.
