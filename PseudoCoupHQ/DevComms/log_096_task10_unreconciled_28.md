# log 096 -- TASK 10, the 28 unreconciled branching units

Date: 2026-08-31. Session: Claude Code, round 2, TASK 10 of
log_091. Ran alone (no sub-agents).

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (`op_pipeline/check_no_spelling_keys.py`) and
refuse its own output on failure.

## walkthrough

The task named three possible per-unit causes for the 28 units in
`dominant_table24.json`'s `unreconciled_branching_units` bin: (1) the
seed's computation has not converged into any class (no class exists
to match), (2) a representative mismatch (the seed matches a class
member's RAW text but not the group's chosen representative text),
(3) genuinely new. It also named the fix to attempt before accepting
any of those three: extend seed matching to use the representative
rule AND the proved-edge set, not exact text alone, since a seed
proved equal to a class member belongs in that class.

`build_table24.py`'s `add_branching_members()` already tries TWO
text pools per seed: a row's representative (post-substitution) text,
and every 0-branch member's own pre-substitution raw text (see its
own docstring, table24.json's `unmatched_branching_seeds` /
`ambiguous_branching_seeds`: 58 of 66 seeds hit neither pool, 4 hit
more than one). That is exact TEXT equality against both pools
already -- the representative rule's own substituted text is one of
the two pools tried. What was missing was the PROVED-EDGE half: a
seed whose text is not character-identical to any pool member, but
is z3-provably equal to one, was never given a chance.

I built that chance. `task10_seed_prove.py` (diagnostic, standalone)
and `build_table24b.py` (the rebuild, TASK 10's deliverable) both
add a second pass: for each of the 58 unmatched + 4 ambiguous seeds,
compute the seed's OWN machine-form class key -- `(type_pair,
result_type family)`, the SAME two fields every table24 row is
already keyed on, read from the seed's own unit meta
(`dom_ops_0branch.type_pair_of`, `result_type_norm.class_family`) --
never the operator token. Restrict candidates to rows sharing that
key (this alone, by construction, resolves the kind of TEXT
ambiguity the swift `mov %edi,%eax; ret` seeds show: 25 rows share
that exact text across unrelated types, but only the rows in the
seed's own type/result pool are legitimate candidates). Then, for
every candidate in the seed's own pool, run
`cross_unit_prover.prove_pair` -- UNCHANGED, the same z3 machinery
(`Sim8`/`Sim20`/`Sim20Cmp`) `build_representatives3.py`'s ground (c)
already uses for 0-branch pairs -- between the seed's text and the
candidate row's canonical text. Proved equal to exactly one row: the
seed joins that row (`join_method: "proof"`). Proved equal to more
than one: a new PROOF-LEVEL ambiguity, kept separate from and not
confused with the original TEXT ambiguity. Proved equal to none: the
per-candidate verdict (PROVED/DISPROVED/UNDECIDED/REFUSED, with
`cross_unit_prover`'s own detail text) is carried forward as the
diagnosis.

RESULT: the proof pass ran to completion against all 287 candidate
pairs (36 seeds had a nonempty pool; 26 had an empty pool). It found
**zero** new joins. `dominant_table24b.json` / `dom_ops22b.json` are
therefore byte-identical in membership, class count, dom-op count and
family count to `dominant_table24.json` / `dom_ops22.json` -- the
mechanical extension is real and ran, but it changed nothing, and
that is reported honestly rather than manufactured into a false
gain.

## instances (per-unit diagnosis, real texts, real prover output)

**Cause 1 -- not converged, class-key pool is EMPTY (26 of 62
attempted seeds, all 8 `c`/`cpp` "u64,f32 -> f32" seeds and all 10
`swift` range-operator seeds).**

```
c/op_117   type_pair=u64,f32  result_family=f32   pool=0
  seed_text: "addss %xmm3,%xmm0; ret"
```
No 0-branch class in the whole 901-class table carries `(u64,f32,
f32)` as its key at all -- the halving/doubling float-conversion
idiom's SUFFIX (this is the u64->float idiom TASK 3/log_089 proved
seeds for) never converged into a 0-branch class of its own; there
is nothing to match against, proved-edge or not. Same story for
`c/op_122`, `c/op_153`, `c/op_158`, `c/op_189`, `c/op_194`,
`c/op_225`, `c/op_230` and their `cpp` co-nodes.

```
swift/op_877  type_pair=i64,i64  result_family=unknown(swift type
              name 'Range<Int64>' not in th...)
  seed_text: "mov %edi,%eax; ret"
```
`result_type_norm.class_family` has no entry for Swift's
`Range<...>`/`ClosedRange<...>` result types at all -- these seeds'
RESULT is a range struct, not a scalar, so no class-key pool can even
be formed. Same for `swift/op_870`, `/op_884`, `/op_891`, `/op_898`,
`/op_906`, `/op_913`, `/op_920`, `/op_927`, `/op_934`. This is also
why 3 of table24's original 4 TEXT-ambiguous seeds
(`swift/op_884`, `/op_913`, `/op_920`) are range-typed: `mov
%edi,%eax; ret` is a generic identity move that 25 unrelated 0-branch
classes happen to share verbatim; type-key restriction would have
resolved the text ambiguity to a single class IF the seed's own
result family were known, but it is not -- so these stay both TEXT-
ambiguous (unresolved) and now diagnosed as class-family-unknown.
This is an instrument gap in `result_type_norm.py`
(non-scalar/range result types), not a text-consolidation frontier
question; flagged, not fixed here (out of this task's scope -- it is
a new-mechanism addition to a different file with its own review
burden).

**Cause 3-leaning (candidates exist, none PROVED; instrument limit,
not text-consolidation) -- 36 seeds with a nonempty pool.**

```
c/op_477   type_pair=u64,f32  result_family=i32   pool=2
  seed_text: "cmpeqss %xmm2,%xmm0; movd %xmm0,%r10d; and $0x1,%r10d;
              mov %r10d,%eax; ret"
  C0782  UNDECIDED  cand="xorps %xmm2,%xmm2; ucomiss %xmm2,%xmm0;
                          mov $0,%eax; setp %al; mov $0,..."
    detail: "this file's Sim20Cmp ... has no model for a mnemonic in
             this pair's text"
  C0783  UNDECIDED  (same candidate text, different class -- a
                     type-pair-order twin)
```
Both candidates in this pool use `setp` (set-if-parity, the NaN-
unordered flag) which `cross_unit_prover.Sim20Cmp` (this file's own
comparison extension) has no model for -- the SAME instrument gap
`prove_pair`'s own docstring names for float comparisons generally.
Every `f32`/`u64` comparison-result seed in the pool (`c/op_482`,
`/op_513`, `/op_518`, `/op_549`, `/op_554`, `/op_585`, `/op_590`,
`/op_621`, `/op_626`, `/op_657`, `/op_662`, and the `cpp` co-nodes
`/op_477`, `/op_482`, `/op_513`, `/op_518`, `/op_981`, `/op_986`)
returns the identical `UNDECIDED` reason.

```
go/op_103   type_pair=i64,i64  result_family=i64   pool=12
  seed_text: "mov %edi,%eax; cqto; idiv %rsi; ret"
  C0695  UNDECIDED  cand="mov %edi,%eax; ret"
    detail: "this file's reused integer simulator (canon8_
             behaviour_check.Sim8) has no model for a mnemonic in
             this pair's text"
  ... (11 more candidates, all UNDECIDED, same reason -- Sim8 has no
      model for `cqto`/`idiv`)
```
Every go/rust divide-or-remainder seed (`go/op_103`, `/op_110`,
`/op_139`, `/op_146`; `rust/op_656`, `/op_692`) and every swift
overflow-guarded seed that still carries its OWN branch labels in
`seed_text` (`swift/op_114`, `/op_12`, `/op_121`, `/op_13`, `/op_157`,
`/op_193`, `/op_222`, `/op_229`, `/op_236`, `/op_258`, `/op_265`,
`/op_272` -- e.g. `swift/op_114`: `"imul %esi,%edi; jo L2; jmp L1;
mov %edi,%eax; ret"`) fails the SAME way: `Sim8` has no model for
`cqto`/`cltd`/`idiv`/`jo`/`jmp` -- these seeds were extracted with
control-flow or wide-divide mnemonics still IN the text (unlike the
c/cpp idiom-suffix seeds, which are pure straight-line), and neither
`Sim8` nor `Sim20Cmp` was ever built to model them. This is an
INSTRUMENT LIMIT on `cross_unit_prover.py`'s two reused simulators,
not a text-consolidation frontier and not (necessarily) a genuinely-
new computation -- it could be either, and the honest answer is that
this pass cannot tell, because it cannot evaluate the candidates at
all. Extending `Sim8`/`Sim20Cmp` to model divide/branch mnemonics is
a real, separate, non-trivial simulator change (out of this task's
scope; named as an open item, not attempted).

**No unit, of the 28 or the 62 attempted, changed status.** Zero
seeds joined by proof. The full per-candidate verdict table (287
pairs) is in `task10_seed_prove_results.json`; every row above is a
verbatim excerpt, not a summary.

## the un-ratified frontier (log_090 SS5) -- not decided here

Per the task's own note: log_090 SS5 left open WHICH text-
consolidation output (`representatives5.json`'s pre-canon24 grouping
vs `table23b.py`'s own proved-edge consolidation) is canonical for a
seed-fragment match target. This session's proof extension is
mechanical and orthogonal to that question -- it never chooses
between the two consolidation outputs, it only tries a THIRD,
independent path (class-key + z3) that needed no such choice. Since
it resolved nothing, every one of the 28 units remains exactly as
un-ratified as table24 left it; `dominant_table24b.json` carries
BOTH the original `cause_table24` text (verbatim, unedited) AND a new
`task10_proof_pass_diagnosis` field per unit, so both sides are shown
side by side, per the task's instruction, rather than a frontier
question being decided by omission.

## numbers

- 66 resolved seeds in `seeds2.json`; 4 matched a class by exact
  text (table24's pass 1, unchanged); 58 unmatched, 4 text-ambiguous
  (unchanged from table24).
- Pass 2 (this session, class-key + z3 proof): 62 seeds attempted
  (58 unmatched + 4 text-ambiguous). 36 had a nonempty class-key
  pool (287 candidate pairs total); 26 had an empty pool.
  **0 PROVED, 0 DISPROVED, 287 UNDECIDED/REFUSED** (all UNDECIDED in
  this run -- either `Sim8` or `Sim20Cmp` lacked a model for a
  mnemonic in one side of every pair attempted; no pair reached a
  REFUSED `(%rip)`-relative-load case in this population).
- `dominant_table24b.json` vs `dominant_table24.json`: 901 vs 901
  classes, 1,645 vs 1,645 total members (0-branch + branching), 26
  vs 26 dom-op families, 28 vs 28 unreconciled units -- byte-
  identical member sets, verified programmatically (`ma - mb = {}`,
  `mb - ma = {}`).
- Both new artifacts pass `check_no_spelling_keys.py` in full, no
  exemption claimed: `PASS dominant_table24b.json`, `PASS
  dom_ops22b.json`.

## artifacts written this session (every one named, including the
## diagnostic that got superseded by nothing -- it is still current)

- `op_pipeline/task10_seed_prove.py` -- standalone diagnostic: seed
  class-key computation + z3 proof pass, writes
  `task10_seed_prove_results.json`. Run twice (first run had a
  cosmetic-only bug: `list(tkey)` on a comma-joined type_pair STRING
  iterated it into characters in the printed/JSON `type_pair` field
  only -- the actual candidate-pool filtering used the correct
  string value throughout, so pool sizes and verdicts were already
  correct in the first run; fixed to `tkey` directly and re-run for
  a clean report field). Both runs' output committed to disk is the
  second (corrected) one; the first is not separately kept.
- `op_pipeline/task10_seed_prove_results.json` -- the 62-seed
  diagnostic result (per-seed pool, per-candidate verdict).
- `op_pipeline/build_table24b.py` -- the rebuild (TASK 10's
  deliverable generator).
- `op_pipeline/dominant_table24b.json` -- NEW grouping table (does
  not overwrite `dominant_table24.json`).
- `op_pipeline/dom_ops22b.json` -- NEW dom-op family table (does not
  overwrite `dom_ops22.json`).
- `op_pipeline/representatives24b.json` -- NEW representative-groups
  side file (mirrors `representatives24.json`'s role, byte-identical
  content since the representative-groups step itself is unchanged
  from `build_table24.py`).
- `op_pipeline/task10_nonzero_pool_dump.txt` -- a scratch text dump
  of the 36 nonzero-pool seeds' full verdict tables, used to write
  the instances section above; kept as a record, not consumed by any
  other file.

Nothing else was written. No file from a prior session was edited.
