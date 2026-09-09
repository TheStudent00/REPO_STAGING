# log_105 -- TASK 22, the remaining 238 unconverged, fourth round

**Role:** Claude Code implementer, TASK 22 of
`log_103_claude_code_task_briefs_round4.md`. **Evidence class stated
per claim below**, per the evidence doctrine. No sub-agents used, per
this task's own instruction -- every artifact below was built and run
directly in this session.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

## plain-words walkthrough

I read AgentMemory.md (including the three 2026-08-31 rulings:
branch-to-alternate-computation as a third detection route, the
arrival/computation lineage-confluence correction, and banking-is-a-
message-not-a-commit), log_103's TASK 22 brief, log_083's STANDING
REQUIREMENTS header, and log_099 in full. I re-verified round 3's own
baseline directly from disk rather than trusting the log's prose:
summed `status`/`converged` over every unit in
`canon28_units_<lang>.json` (the file, not the log) for all five
languages -- **1,541 converged, 238 not-yet-converged**. Matches
log_099's stated round-3 result exactly (evidence class: tool
testimony, reproducible).

## step 1 -- re-counting the 26 UNDECIDED units log_099 named as the
## Sim8-coverage frontier, DIRECTLY off disk

log_099's own prose gave the 26 as "6 jo, 6 je, 4 cltd, 4 register-
spelling, 4 idiv, 2 jb". I re-counted from `canon28_units_<lang>.json`
`job5_no_named_op_ground_truth_verdict == "UNDECIDED"` (the exact
field this population was recorded under) directly, rather than copy
the log's numbers. **The true breakdown is 6 WIDTH_OF-stack-relative,
6 jo, 4 cltd, 4 idiv, 4 je, 2 jb -- still 26 total, but je and the
WIDTH_OF group were transposed in log_099's own prose.** This is a
correction, not a re-litigation: log_099's OWN recommendation (extend
Sim8, named as a frontier) and OWN judgment on the WIDTH_OF group
(the owner-reserved, same units as its separately-discussed "6 SP:64 leaf
atom" bucket) are unaffected by the count swap.

Verbatim sample instances (evidence class: tool testimony,
reproducible -- `canon4_units_<lang>.json` read directly):

```
c/op_210   /   real mnem: mov %edi,%eax; cltd; idiv %esi; ret
c/op_240   /   real mnem: mov %edi,%eax; xor %edx,%edx; idiv %esi; ret
swift/op_12   -   blocks: L0[neg %edi; jo L2; jmp L1], L2[ud2], L1[mov %edi,%eax; ret]
swift/op_236  +   blocks: L0[add %rsi,%rdi; jb L2; jmp L1], L2[ud2], L1[mov %edi,%eax; ret]
go/op_96      /   blocks: L0[test..;je L5;jmp L1], L5[call runtime.panicdivide],
                  L1[cmp..;jne L3;jmp L2], L3[mov..;cltd;idiv %esi], L2[neg..;xor..;jmp L4_p1], L4[ret], L4_p1[mov..;ret]
c/op_31       &   real mnem: mov %rdi,-0x8(%rsp); lea -0x8(%rsp),%rax; ret
```

## step 2 -- the WIDTH_OF/stack-relative 6, re-judged (recommendation
## carried forward, not reopened)

These 6 (`c/31,32,35`, `cpp/43,44,47`, all `&` -- address-of) are the
SAME units log_099 already discussed under its `SP:64` leaf-atom
framing and recommended the owner-reserved: whether "the answer" for an
address-of unit means a stack-relative offset or something compiler-
layout-dependent is a semantic ruling about what the ground-truth
proof itself is proving, not a checker coverage gap. I checked for
new evidence that would change this call (canon.py's own git log,
`git log --oneline -- canon.py`, and a fresh read of `WIDTH_OF`'s own
construction) and found none -- WIDTH_OF is still built only from
plain-register names, no memory-operand entry was ever added.
**Recommendation stands: the owner-reserved, not attempted.**

## step 3 -- the 20 remaining (jo/je/jb/cltd/idiv) -- MODELED, per
## the brief's explicit authorization

Task 22's own brief named this exact gap ("missing jo/je/jb/cltd
models, stack-relative widths, idiv ambient register") and pre-
authorized "a new WRAPPER module extending the simulator (shared file
untouched, wrapper precedent)" as legitimate modelling work. I built
one: **`op_pipeline/canon9_behaviour_check.py`** (new file), a `Sim9`
subclass of `canon8_behaviour_check.Sim8` -- `canon5_behaviour_check.
py` through `canon8_behaviour_check.py` are UNCHANGED, imported by
reference only, the same reuse chain every file in this lineage
already follows.

What `Sim9` adds, and why each is sound (full mechanism, not a
metaphor):

- **`cltd`/`cqto`/`cqo`** -- sign-extends the low register's sign bit
  through the high register (`edx = eax >> 31` using z3's arithmetic
  `>>`, the same idiom `Sim8`'s masked-shift fix already uses for
  `sar`). 32-bit (`cltd`) and 64-bit (`cqto`/`cqo`) forms both
  modeled.
- **`idiv`** -- round 3 judged the dividend "ambient" (unreadable
  from the text alone) because nothing modeled `cltd`. I checked all
  4 c/cpp `idiv` occurrences directly: every one is immediately
  preceded by `cltd`/`xor %edx,%edx` in the SAME text. Once `cltd` is
  modeled and tracked as this run's OWN `edx`/`rdx` state, the
  dividend (`Concat(edx, eax)`) is no longer ambient -- it is exactly
  what real hardware reads, computed by this simulator's own prior
  instruction. `SDiv`/`SRem` on the sign-extended divisor give
  quotient/remainder, written to `eax`/`edx`.
- **`jo`** (6 units) -- a tracked overflow flag. `neg` overflows iff
  the input equals `INT_MIN` for its width (the only value a two's-
  complement negation cannot represent). `add`/`sub` overflow via the
  standard (width+1)-bit signed-extension formula (the extra top bit
  disagreeing with the truncated result's sign bit) -- needed because
  4 of the 6 `jo` units follow `add`/`sub`, not `neg` (found this lap
  by direct inspection after the first `neg`-only version left them
  UNDECIDED; not guessed at up front).
- **`jb`** (2 units) -- carry/borrow flag, tracked directly off
  `add`/`sub` (unsigned overflow / unsigned-less-than), not routed
  through `cmp`'s state.
- **`je`** (4 units) -- ZERO new flag logic. Branch mnemonics were
  given access to the SAME `last_cmp`/`condition_table.py` predicate
  path `canon6_behaviour_check.ExtSim` already uses for `setcc`/
  `cmovcc` -- ExtSim's own header names this exact table as the
  "proved (against angr's ccall)" predicate source; reused unchanged.
- **Control flow.** All 12 `jo`/`je`/`jb` units are real branches (a
  `ud2` or `call <panic-helper>` on the not-taken side), which is why
  `canon8_behaviour_check.anchored_check` (straight-line-only) could
  never have modeled them regardless of mnemonic coverage. I added a
  recursive block-walker (`run_flow`/`run_from`) that explores BOTH
  sides of every conditional branch over the ALREADY-LABELED `blocks`
  (real) / `derived_blocks` (candidate) fields every `canon4_units_
  <lang>.json` record carries (both mutually label-consistent by
  `canon4.py`'s own construction -- no address-to-label resolution
  needed or attempted), z3-merges the two branches' answers with
  `If`, and treats a trapped branch (`ud2`/`call`) as contributing
  NO value. This is sound specifically because `canon6_behaviour_
  check.py`'s own header already establishes and relies on the fact
  that guard/trap/dispatch blocks are NEVER rewritten by `canon4.py`'s
  renderer -- only a compute block is -- so a real trap block and its
  candidate counterpart are byte-identical, sharing the identical
  predicate by construction, not by an assumption invented in this
  file. One additional real-world shape found and handled:
  `go/op_96`'s block `L3` (`mov;cltd;idiv`) has no terminator at all
  in real disassembly -- it falls through to the next compiled block
  by ORDER (`L2`), exactly as x86-64 does when the assembler omits a
  redundant jump; `run_flow` takes the real compiled block order
  (`blocks`'s own list order) and falls through on a terminator-less
  block rather than refusing.

**Driver:** `op_pipeline/canon29.py` (new). Selects its population
from `canon28_units_<lang>.json`'s own `job5_no_named_op_ground_
truth_detail` field by ISA MNEMONIC NAME (`cltd`, `idiv`, `jo`, `je`,
`jb`) -- machine-form evidence about the CHECKER's own prior refusal
text, never a source-language operator token; `operator` is carried
only as a display label. Dispatches straight-line units (no `blocks`
field on the canon4 record) to `Sim9.anchored_check_straight` over
the SAME already-selected `job5_no_named_op_candidate_text`, and
branching units to `Sim9.anchored_check_branching` over `blocks`/
`derived_blocks` directly.

### run output (verbatim)

```
wrote canon29_units_c.json     -- {'attempted': 4,  'accepted': 4,  'attempted_not_proved': 0, 'skipped_not_target_mnemonic': 63, 'skipped_no_candidate_text': 0}
wrote canon29_units_cpp.json   -- {'attempted': 4,  'accepted': 4,  'attempted_not_proved': 0, 'skipped_not_target_mnemonic': 80, 'skipped_no_candidate_text': 0}
wrote canon29_units_go.json    -- {'attempted': 2,  'accepted': 2,  'attempted_not_proved': 0, 'skipped_not_target_mnemonic': 35, 'skipped_no_candidate_text': 0}
wrote canon29_units_rust.json  -- {'attempted': 0,  'accepted': 0,  'attempted_not_proved': 0, 'skipped_not_target_mnemonic': 13, 'skipped_no_candidate_text': 0}
wrote canon29_units_swift.json -- {'attempted': 10, 'accepted': 10, 'attempted_not_proved': 0, 'skipped_not_target_mnemonic': 27, 'skipped_no_candidate_text': 0}
TOTAL: {'attempted': 20, 'accepted': 20, 'attempted_not_proved': 0, 'skipped_not_target_mnemonic': 218, 'skipped_no_candidate_text': 0}
```

**All 20 targeted units PROVED_EQUAL. 0 attempted_not_proved.**

### zero regressions (evidence class: tool testimony, reproducible)

Every `status == "converged"` unit in `canon28_units_<lang>.json`
(1,541 units, all five languages), every `*_text` field, byte-
compared against the corresponding `canon29_units_<lang>.json`
record: **0 differences, 1,541 units checked, PASS.**

**Converged delta: 1,541 -> 1,561 (+20).** Directly counted:
`sum(1 for u in canon29_units_<lang>.json.units.values() if
u['status'] == 'converged')` over all five languages.

Per-language delta:

| lang | before | after | delta |
|---|---|---|---|
| c | 543 | 547 | +4 |
| cpp | 686 | 690 | +4 |
| go | 70 | 72 | +2 |
| rust | 112 | 112 | +0 |
| swift | 130 | 140 | +10 |
| **total** | **1,541** | **1,561** | **+20** |

`check_no_spelling_keys.py` on all 5 `canon29_units_<lang>.json`:
**PASS**, all five (`"exempt: top-level meta declares role
'generator provenance'"` -- same discipline every prior `canonNN_
units_<lang>.json` in this lineage carries; this file gates one
unit's own text at a time against its own ground truth, no grouping
or pairing of units against each other).

## step 4 -- the remaining 218, freshly classified off disk (not
## assumed from round-3 arithmetic)

I re-ran `canon28_units_<lang>.json`'s own `status` field over the
current (post-canon29) population rather than subtracting counts:

```
Counter({'not_yet_converged': 98, 'unchanged': 70, 'no_canon4_text': 50})
```

### bucket A -- the 6 WIDTH_OF/stack-relative units

Already covered in step 2. **Recommendation: the owner-reserved, unchanged
this round.**

### bucket B -- `no_canon4_text`, 50 units, split by a fresh
### per-unit survey (a DIFFERENT, larger population than log_099's
### 16 -- that 16 was the intersection with the `__no_named_op_found__`
### bucket specifically, not the full `no_canon4_text` population)

Reading `canon4_units_<lang>.json`'s own `erasure` field for each of
the 50:

| sub-cause | count | judgment |
|---|---|---|
| `erasure_refused: a branch target address could not be resolved to any walked block (likely a tail jump outside this unit's own block set)` | 16 | **NEW this round** (not in log_099's 16) -- same class: canon4's own erasure-stage refusal, out of a render/gate-layer wrapper's scope. **Recommendation: defer**, owned by canon4's erasure machinery. |
| `erasure_refused: two stack-spilled operands in one instruction` | 8 | **NEW this round.** Same class/recommendation: **defer**. |
| `erasure_refused: too many distinct join paths -- not attempted this slice` | 6 | Log_099's own named cause, re-verified: `canon4.py` line 550 still contains this exact refusal text; `git log --oneline -- canon4.py` shows the file's last change (`8f3dc5a update`) predates this session and was not touched this lap -- **the blocker has NOT fallen. Recommendation: defer stays deferred**, per the brief's own rule. |
| `erasure_refused: value w0 is read before it is defined or before the unit's entry contract names it` | 1 | **NEW this round.** Same class/recommendation: **defer**. |
| `erasure="ok"` but NEITHER `derived_text` (list) NOR `derived_blocks` present at all | 19 | **NEW this round, a genuinely different cause** -- canon4's own erasure step SUCCEEDED but no rendering stage ever produced ANY text form for these units (sample: `cpp/op_753`). This is a canon4-RENDERING omission, not an erasure refusal -- distinct from every cause above. Modifying canon4.py (a shared file every driver in this lineage depends on) is out of a wrapper-only lap's safe scope without re-verifying every downstream consumer, the same standard log_099 itself applied to the Sim8 extension before this lap did it properly. **Recommendation: model, next round** (a dedicated lap owning canon4.py directly, with the downstream re-verification that requires) -- named as a frontier, not attempted here. |

**No sub-cause here was fixed this lap.** All 50 stay at
`no_canon4_text`; 0 converged delta from this bucket, all newly named
rather than left silent.

### bucket C -- `unchanged` (70) + the float/rflags portion of
### `not_yet_converged` (98) -- re-surveyed by machine-form lifter
### name (the SAME `census27.names_from_raw` test, imported
### unchanged, no operator token in the key)

```
 18  ('amd64g_calculate_rflags_c',)
 16  ('Add32F0x4', 'amd64g_calculate_condition')
 16  ('Add64F0x2', 'amd64g_calculate_condition')
 13  ('__no_named_op_found__',)              <- residual, not yet explained; see below
  8  ('Sub32F0x4',)
  8  ('Sub64F0x2',)
  8  ('Div32F0x4',)
  8  ('Div64F0x2',)
  8  ('amd64g_calculate_condition',)
  6  ('Add64F0x2',)
  6  ('Add32F0x4', 'CmpEQ32F0x4', 'XorV128')
  6  ('Add64F0x2', 'CmpEQ64F0x2', 'XorV128')
  6  ('DivModU128to64',)
  ... (remaining rows, smaller float-family combinations, sum to 168 total)
```

- **`amd64g_calculate_rflags_c` (18) -- the `CF_SUB` render rule.**
  Log_099/round 2 recommendation: **the owner-reserved, confirmed still
  reserved** ("substitution proven, render mechanism genuinely
  different from what exists, log_084's own frontier #1"). I checked
  `condition_table9.py`/`condition_table10.py`/`canon22_render.py`
  for any new `CF_SUB` codegen case added since round 3 -- none
  found. **Recommendation: out of scope, not reopened** (no new
  evidence).
- **`amd64g_calculate_condition` (8, and mixed into the float rows
  above)** -- round 2's four named refusal reasons, re-checked for
  new precedent in `canon22_render.py`/`canon7_render.py`/
  `canon17_float.py` this lap: none found. **Recommendation: out of
  scope, not reopened.**
- **The float family (`Add`/`Sub`/`Div`/`Mul` × `32F0x4`/`64F0x2`,
  ~140 of the 168) -- log_099's ranks 3-4 (`Add64F0x2`/`Add32F0x4`,
  82 units), never reached in round 3, explicitly named "open item,
  fresh per-unit survey is the honest next step," NOT given an
  explicit model/defer/out-of-scope verdict by log_099.** This lap's
  survey (the table above) is that fresh per-unit survey. Root cause,
  re-confirmed from round 2's own diagnosis (still current -- no new
  render-table precedent found this lap in `canon17_float.py`): the
  float-operand classifier (`_operand_xmm`) only knows `a`/`b`/
  `zero`; every blocked unit here carries a NESTED EXPRESSION as one
  comparison/arithmetic operand, needing fresh register-allocation
  logic (render a sub-expression into a fresh physical XMM register
  first) rather than a table-row addition -- genuinely bigger surgery
  in a shared render file (`canon17_float.py`), not safely doable as
  an isolated wrapper. **Recommendation: model, next round** (owns
  `canon17_float.py` directly, budgeted as its own lap) -- carrying
  round 2's the owner-reserved judgment forward for the SAME root cause at
  its now-confirmed larger scale, not reopening it casually but not
  leaving it unnamed either.
- **The 13 residual `__no_named_op_found__` units** -- not explained
  by this lap's survey (their `job5_no_named_op_ground_truth_detail`
  is empty, meaning canon28/canon29 never attempted them, yet
  `census27.names_from_raw` finds no named op in their raw text
  either). **Named honestly as unexplained, not silently dropped**;
  likely a `skipped_no_tree_units3_record`/`skipped_no_candidate_
  text` case from canon28's own tally (both non-zero for go/rust/
  swift in round 3's run) -- confirming the exact sub-cause is next
  round's work, not guessed at here.

## converged delta, per-bucket accounting (summary table)

| bucket | count | this lap's disposition | converged delta |
|---|---|---|---|
| Sim8 frontier: `jo`/`je`/`jb`/`cltd`/`idiv` | 20 | MODELED via new `Sim9` wrapper (canon9_behaviour_check.py/canon29.py) | **+20** |
| WIDTH_OF/stack-relative (`SP:64` family) | 6 | the owner-reserved, re-confirmed, not attempted | 0 |
| `no_canon4_text`: "too many join paths" | 6 | defer stays deferred (canon4.py unchanged, blocker did not fall) | 0 |
| `no_canon4_text`: branch-target-unresolved (NEW) | 16 | defer, newly diagnosed, owned by canon4 erasure stage | 0 |
| `no_canon4_text`: two-stack-spilled-operands (NEW) | 8 | defer, newly diagnosed | 0 |
| `no_canon4_text`: value-read-before-defined (NEW) | 1 | defer, newly diagnosed | 0 |
| `no_canon4_text`: erasure=ok but no rendered text at all (NEW) | 19 | model, next round (canon4.py rendering gap, shared-file lap) | 0 |
| `amd64g_calculate_rflags_c` (`CF_SUB`) | 18 | out of scope, not reopened, no new evidence | 0 |
| `amd64g_calculate_condition` | 8 | out of scope, not reopened, no new evidence | 0 |
| float family (`Add`/`Sub`/`Div`/`Mul` F0x2/F0x4, incl. mixed-op rows) | ~140 | model, next round (canon17_float.py register-allocation work, shared-file lap) | 0 |
| residual `__no_named_op_found__` (unexplained) | 13 | named unexplained, next round diagnoses the exact sub-cause | 0 |
| **TOTAL** | **238** (218 remain + 20 converged) | | **+20** |

**This round's non-zero cause, distinguished from round 3's:** round
3's +84 came from a mechanical gate-application gap (a population no
driver's SHAPE FILTER had ever selected). This round's +20 came from
a genuinely different cause -- a SIMULATOR COVERAGE gap (missing
instruction/control-flow models), fixed by the wrapper the brief
itself pre-authorized, with real control-flow proof (branch merging
over `blocks`/`derived_blocks`, not a straight-line-only check).

## files touched this lap (new only)

- `op_pipeline/canon9_behaviour_check.py` (new) -- `Sim9` wrapper:
  `cltd`/`cqto`, `idiv`, tracked `jo`/`jb` flags, and a recursive
  branch-merging control-flow walker (`run_flow`/`run_from`) over
  `blocks`/`derived_blocks`.
- `op_pipeline/canon29.py` (new) -- driver; selects by ISA mnemonic
  name off `canon28_units_<lang>.json`'s own refusal-detail field,
  dispatches straight-line vs branching, writes `canon29_units_
  <lang>.json`.
- `op_pipeline/canon29_units_{c,cpp,go,rust,swift}.json` (new,
  written by canon29.py).

No existing artifact was modified or deleted. `canon28_units_
<lang>.json`, `canon4_units_<lang>.json`, `sem_anchored_spill_
<lang>.json`, `canon.py`, `condition_table.py`, `canon8_behaviour_
check.py` and every earlier file in the `canon5`..`canon8_behaviour_
check.py` lineage are all unchanged (verified read-only for
`canon28_units_<lang>.json` by the zero-regression byte compare
above; the rest were opened read-only, never written).

## `dominant_table24`/`dom_ops22` -- NOT rebuilt, per the brief

Not opened this lap. **Open item, named explicitly:** the 20 newly-
converged units (their own `canon4_units_<lang>.json` unit numbers
are recoverable from `canon29_units_<lang>.json`'s `status ==
"converged"` records with `job6_sim9_ground_truth_verdict ==
"PROVED_EQUAL"`) await `tree_units`/`clusters`/`dominant_table24.json`/
`dom_ops22.json` incorporation by whichever script performs that
step -- same open item log_099 already named for round 3's 84, now
also true of this round's 20, neither rebuilt in this lap either.

## banking

The daemon has already committed every artifact above (`git log
--oneline -3` in `PseudoCoupHQ`, checked directly this lap, shows
`canon29.py`/`canon29_units_c.json`/... already landed in commit
`37380df`) -- this message is written for posterity/searchability,
per the 2026-08-31 ruling, not to claim a staged-not-committed state.

---

## CORRECTION NOTE, appended 2026-09-01 (TASK 25, log_110)

The original text above stands unedited; this note sits below it
because the mistake is part of the record.

**What is wrong: bucket B's 19-unit row.** The table in "bucket B --
`no_canon4_text`, 50 units" gives a row of 19 units described as
"`erasure="ok"` but NEITHER `derived_text` (list) NOR `derived_blocks`
present at all", called "NEW this round, a genuinely different cause",
diagnosed as "a canon4-RENDERING omission", and recommended "model,
next round". That row is not a real cause and those 19 units are not
one group.

**Why the reading was wrong, mechanically.** A `canon4_units_
<lang>.json` record can refuse at two different stages and carries a
separate field for each: `erasure` is the move-erasure stage's own
verdict, and `derive_refused` is the LATER stage that derives the
canonical runnable text. This lap read `erasure` alone. On all 19 of
those records `erasure` is `ok` -- the earlier stage did finish -- and
`derive_refused` names the real cause in words on every one of them.
Nothing needed to be inferred; a second field had to be read.

**The corrected split, counted off disk 2026-09-01** (evidence class:
tool testimony, reproducible):

```
$ cd PseudoCoupHQ/Research/op_pipeline
$ python3 -c "
import json,collections
langs=['c','cpp','go','rust','swift']
c=collections.Counter()
for L in langs:
    d=json.load(open('canon29_units_%s.json'%L))['units']
    d4=json.load(open('canon4_units_%s.json'%L))['units']
    for k,u in d.items():
        if u.get('status')!='no_canon4_text': continue
        r=d4[k]
        if r.get('erasure')!='ok': continue
        c[(L,str(r.get('derive_refused')))]+=1
for (L,t),n in c.most_common(): print(n, L, repr(t))
"
14 cpp 'erasure_refused: two stack-spilled operands in one instruction -- not attempted this slice'
3 rust "erasure_refused: value w0 is read before it is defined or before the unit's entry contract names it"
2 rust 'erasure_refused: the answer value never entered a tracked register (a passthrough this builder does not model)'
```

- **14** belong to the cause this lap had ALREADY counted as 8 --
  "two stack-spilled operands in one instruction". That bucket is
  **8 -> 22**.
- **3** belong to the cause this lap had ALREADY counted as 1 --
  "value w0 is read before it is defined or before the unit's entry
  contract names it". That bucket is **1 -> 4**.
- **2** carry a reason that had no bucket at all and is the only
  genuinely new one in the 19: **"the answer value never entered a
  tracked register"** (canon4's own words: "a passthrough this builder
  does not model"). This is now a NAMED BUCKET of its own.

14 + 3 + 2 = 19. Nothing else in bucket B changes.

**Bucket B, whole and corrected**, keyed on canon4's own refusal text
(machine-form evidence about the pipeline's behaviour; the `operator`
field is not read by this command, so no operator token participates
in the grouping):

```
$ python3 -c "
import json, collections
langs=['c','cpp','go','rust','swift']
c=collections.Counter()
for L in langs:
    d29=json.load(open('canon29_units_%s.json'%L))['units']
    d4=json.load(open('canon4_units_%s.json'%L))['units']
    for k,u in d29.items():
        if u.get('status')!='no_canon4_text': continue
        r=d4[k]
        cause = r.get('erasure') if r.get('erasure')!='ok' else r.get('derive_refused')
        cause = (cause or 'NO REFUSAL FIELD AT ALL').replace('erasure_refused: ','')
        c[cause]+=1
tot=0
for t,n in c.most_common():
    tot+=n; print('%3d  %s'%(n,t))
print('---'); print('%3d  TOTAL no_canon4_text'%tot)
"
 22  two stack-spilled operands in one instruction -- not attempted this slice
 16  a branch target address could not be resolved to any walked block (likely a tail jump outside this unit's own block set) -- not attempted this slice
  6  too many distinct join paths -- not attempted this slice
  4  value w0 is read before it is defined or before the unit's entry contract names it
  2  the answer value never entered a tracked register (a passthrough this builder does not model)
---
 50  TOTAL no_canon4_text
```

The 50-unit total is unchanged, and no unit's `status` changed in any
artifact -- the JSON records always said this. Only the reading was
wrong.

**What this voids.** The recommendation "model, next round (canon4.py
rendering gap, shared-file lap)" attached to the 19 is VOID: there is
no canon4 rendering gap to model. Three of the four remaining causes
keep their existing "defer" disposition at their corrected sizes (22,
16, 6, 4). The 2-unit bucket is new work, and log_109's TASK 26 owns
its diagnosis.

**What is NOT affected.** The +20 convergence, the 1,541 -> 1,561
delta, the zero-regression check, `canon9_behaviour_check.py`,
`canon29.py`, the WIDTH_OF/stack-relative 6, the float family, the
`amd64g_*` buckets, and the 13 residual unexplained units are all
untouched by this correction -- the error was confined to how the 50
`no_canon4_text` units were sorted among themselves.

Full record of this repair, with the rest of the round-4 audit fixes:
`PseudoCoupHQ/DevComms/log_110_task25_record_repairs.md`.
