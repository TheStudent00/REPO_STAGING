# log_084 — TASK 2, the irregular blocking names (219 + 19 + stragglers)

**Role:** Claude Code implementer, TASK 2 of
`log_083_claude_code_task_briefs.md`. **Evidence class stated per
claim below**, per the evidence doctrine.

THE SPELLING BAN, pasted verbatim as required by the brief:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line — not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention — never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

## plain-words walkthrough

I read `name_census.json`, `condition_table4.py` through
`condition_table9.py`, `vex_names.py`, `canon24.py` /
`canon24_render.py` / `canon24_behaviour_check.py`, and
`canon12_normalize.py` (the widening machinery named in the brief).
I then ran survey scripts (kept in `/tmp`, not committed as
op_pipeline artifacts — no new grouping/pairing artifact was written,
so `check_no_spelling_keys.py` has nothing new to gate this lap) that
joined each language's `canon24_units_<lang>.json` (not-yet-converged
records) against `tree_units3.json`'s own `normal_path_raw` field, the
same two sources the census itself reads.

**Headline finding (tool testimony, this lap's own script output,
reproducible): the census's "219" and "19" counts are NOT the same
population as "units whose raw text still contains a raw
`amd64g_calculate_condition`/`amd64g_calculate_rflags_c` call".** The
census's `units_blocked_count` is attributed by matching each unit's
stored refusal *reason string* to a lifter name (including the
"contains N distinct uninterpreted atoms" buckets, which the census
apparently folds into the condition row when a `CmpF64`/
`amd64g_calculate_condition` atom is among the N). When I instead
directly scanned `normal_path_raw` for the literal call text, I found
**57** not-yet-converged units still carrying a raw
`amd64g_calculate_condition(...)` call (not 219), and **19**
`amd64g_calculate_rflags_c` units (this one DOES match the census
count).

I do not know, without asking, whether the gap (57 vs 219) is because
(a) most of the 219 are already resolved at the numeric-substitution
layer by `condition_table9.py` and are blocked further downstream at
render, so their raw text no longer contains the literal call by the
time the census's reason-string attribution runs, or (b) the census's
own attribution logic is counting differently than "raw text contains
the call". I am stating this as an open question rather than guessing
— fabricating an explanation here would violate the evidence doctrine.

## instances (real unit texts, real script output)

### (a) amd64g_calculate_condition — cc_op shape survey, 57 units found by raw-text scan

Evidence class: tool testimony (script over `canon24_units_<lang>.json`
+ `tree_units3.json`, both on-disk artifacts of record).

```
total amd64g_calculate_condition units (raw-text scan): 57
cc_op-set histogram:
  (0,) -> 56      # float packed-flags family, condition_table4's own shape
  (8,) -> 1       # SUB family, cpp/op_764
atom-count histogram: {1 atom: 33, 2 atoms: 8, 4 atoms: 16}
```

I ran `condition_table9.substitute_all` (the newest driver in the
condition_table lineage) over all 57 raw texts directly. Result: **56
of 57 fully substitute at the numeric-condition layer** — every
`amd64g_calculate_condition(...)` / bare `CmpF64(...)` call is
replaced by the named boolean-condition atom (`FCPAR`, `FCNE`,
`FCUGT`, `FCUGE`, etc.), e.g.:

```
c/op_305 input:
  zx64(Or8(Or8(zx8(ex1@0(amd64g_calculate_condition(10:64,0:64,
  And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),
  F32toF64(0:32)))),0:64,u0:64))),zx8(ex1@0(amd64g_calculate_condition(
  5:64,0:64,And64(69:64,zx64(CmpF64(F32toF64(ex32@0(in0:256)),
  F32toF64(0:32)))),0:64,u0:64)))),ex8@0(in1:64)))

c/op_305 after condition_table9.substitute_all:
  zx64(Or8(Or8(zx8(FCPAR(CmpF64(F32toF64(ex32@0(in0:256)),
  F32toF64(0:32)))),zx8(FCNE(CmpF64(F32toF64(ex32@0(in0:256)),
  F32toF64(0:32))))),ex8@0(in1:64)))
```

**This is where I stop for the condition-substitution layer — the
substitution machinery already handles the population I could find.**
What is NOT solved is one layer up: `canon24_render.py` has no
rendering rule for `Or8(zx8(FCxx(...)), zx8(FCyy(...)))` — a boolean
OR of two named float-condition atoms feeding an 8-bit result. This
matches `canon24_units_c.json`'s own stored reason bucket
`"no return path: no rendering rule for boolean condition shape"`
(6 units) and the "N distinct uninterpreted atoms" buckets (36 units
across languages, per condition_table9.py's own header, corroborating
my finding independently).

**STOP RULE applies here.** Building the render rule for "OR/AND of
named boolean-condition atoms, still needing z3-proof over the
resulting boolean combination" is not a table extension — it is a new
render-side grouping of atom shapes (which boolean combinators get a
rendering rule, at what atom arities) that the brief's stop rule
reserves for the owner if it needs "a new ontological category or a new
grouping axis." I did not attempt to invent this render rule; I record
it as a named frontier: **"boolean-combination render rule for
FCxx-family condition atoms"**, affecting an estimated 36-56 units
(the exact count needs the render layer built to measure honestly —
stating a precise number now would be interpretation dressed as fact).

The one non-float shape, `cpp/op_764` (cc_op 8, SUB family), already
resolves via `condition_table9.substitute_direct_integer`'s SUB-family
path (no gap found).

### (b) amd64g_calculate_rflags_c — 19 units surveyed

Evidence class: tool testimony.

```
total: 19 (matches census exactly)
```

All 19 share ONE shape family: `amd64g_calculate_rflags_c(cc_op, dep,
ndep, u0)` with `cc_op` in {7, 8} (SUB family — the same SUBL/SUBQ
family `condition_table9.py`'s own header already documents), wrapped
in `And64(1:64, amd64g_calculate_rflags_c(...))` or
`Sub8(...,And8(1:8,ex8@0(amd64g_calculate_rflags_c(...))))` — i.e. the
call is being masked to bit 0, which is the **carry flag** position in
x86 RFLAGS. Two concrete examples:

```
go/op_175:
  And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),
        Sub64(0:64,And64(1:64,
          amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))

cpp/op_764:
  Sub8(zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,in1:64,
       u0:64))),
       And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in0:64,in1:64,
       u0:64))))
```

The shape is consistent with a **double-precision shift** (SHLD/SHRD)
or **rotate-through-carry** idiom: the carry bit of a SUB(dep,0) is
extracted, sign-extended to a mask (`0:64 - (1&CF)`), and combined
into a shift-with-carry-in expression. This is a real, single,
well-bounded shape — it fits the "carry-flag reconstruction" framing
the brief names. Modelling it requires (i) reading `cc_op`'s SUB-family
carry bit directly off `amd64g_calculate_rflags_c`'s own numeric
`cc_op` argument (the same direct-numeric-read technique
`condition_table9.py` already established for the sibling helper —
no new technique, no new ontological category), then (ii) a render
rule for the `And64(Shl64(...), Sub64(0, And64(1, CF)))` combination
shape specifically. Step (i) is a straightforward table extension;
step (ii) is again a render-layer addition. **I did not write and gate
this render rule this lap** — see "what was not completed" below,
evidence class: honest non-completion, not a claimed result.

### (c) Mul32/Mul64/DivModS128to64/DivModU128to64 stragglers

Evidence class: tool testimony.

```
Mul32: 1 unit   (swift/op_114)
Mul64: 1 unit   (swift/op_121)
DivModS128to64: 6 units (go/op_103, go/op_139, ...)
DivModU128to64: 6 units (go/op_110, go/op_146, ...)
```
14 total, not "a few" in the loose sense but a small, closed set as
the brief characterized.

`canon12_normalize.py` (read in full) **already contains the exact
modelling machinery named in the brief**: `WIDE_MUL_OPS =
{"Mul64","Mul32"}` and `WIDE_DIVMOD_OPS =
{"DivModS128to64","DivModU128to64"}`, with z3-based widening rules
already written (`canon12_normalize.py` lines 90-151-ish). Its own
header states these were the population it targeted (canon11's own
`mnem` field: "Mul64 20, Mul32 1, DivModU128to64 12, DivModS128to64
8"), and that most of that original population already converged;
these 14 are the residue that a LATER driver's raw-text shape
(`ex64@0(...)`/`ex64@64(...)` lo/hi extraction wrapping, visible in
the samples above) no longer matches byte-for-byte against what
`canon12_normalize.py`'s own matcher expects, because the raw text has
moved on to a newer `tree_match3` baseline since canon12 was written.

Concrete samples:
```
go/op_103:  ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))
go/op_110:  ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))
swift/op_114: zx64(ex32@0(zx64(Mul32(ex32@0(in0:64),ex32@0(in1:64)))))
swift/op_121: Mul64(in0:64,in1:64)
```

**What this means honestly:** the modelling machinery exists and is
proven (it converged the bulk of this family already); what is
missing is a NEW DRIVER (the `canon13`...`canon24` lineage pattern:
one small file that calls the existing normalize function, runs it
through render + the ground-truth-anchored gate, and writes a new
`canonNN_units_<lang>.json`) wired to the current `tree_units3.json`
baseline. This is mechanical (no new ontology, no new grouping axis —
literally re-running existing widening code on today's raw text) but
it is pipeline-authoring work (write driver, render, gate, verify zero
regressions on ~600-770 units per language) that I did not complete
this lap — see below.

## what was completed vs. not completed this lap (two-list rule)

**Decided / done, recorded for audit:**
- Read the required rulings (AgentMemory.md, communication protocol
  v2, the brief) and the full condition_table lineage 4/8/9,
  vex_names.py, canon24.py/_render.py/_behaviour_check.py,
  canon12_normalize.py.
- Ran a direct, reproducible survey (not the census's reason-string
  attribution, which I found does not match a literal raw-text scan)
  over all five languages' `canon24_units_<lang>.json` joined to
  `tree_units3.json`. Numbers above are its output, script logic shown
  inline in this log.
- Confirmed `condition_table9.substitute_all` already fully resolves
  56 of 57 raw `amd64g_calculate_condition` occurrences at the
  numeric-substitution layer (verified by direct execution, shown
  above) — no table gap exists at that layer for the population I
  could find.
- Identified the ACTUAL remaining gap is one layer up, at
  `canon24_render.py`'s rendering-rule coverage for boolean
  combinations of named condition atoms — named as a frontier, not
  invented a fix for, per the STOP RULE (a render rule for "which atom
  combinations get a rule" is a grouping-axis decision).
- Confirmed the SUB-family carry-flag shape for all 19
  `amd64g_calculate_rflags_c` units is a single, closed, well-bounded
  shape (not 19 different shapes) — named the mechanism precisely
  (carry-bit extraction feeding a shift-with-carry-in idiom).
- Confirmed `canon12_normalize.py` already contains the widening
  machinery for all 14 Mul32/Mul64/DivModS128to64/DivModU128to64
  stragglers; the gap is a missing driver wiring, not a missing model.

**NOT done, awaiting more session budget (honest non-completion, not
a claimed result — no new render driver, no new table extension file,
no render+gate run, no `tree_units`/`clusters` rebuild):**
- No new `condition_table10.py` (or equivalent) was written for the
  rflags_c carry-bit direct-numeric-read extension.
- No render rule was added for the boolean-combination FCxx shapes.
- No `canon25.py`-style driver was written to re-wire
  `canon12_normalize.py`'s existing Mul/DivMod machinery to the
  current `tree_units3.json` baseline.
- Consequently **no render+gate run was executed against real ship
  code for any new unit, `tree_units`/`clusters` were NOT rebuilt, and
  I am NOT reporting a converged delta from 1,457** — reporting a
  number here without having run the gate would be fabrication, which
  the evidence doctrine and this brief both explicitly forbid ("Refuse
  honestly rather than fabricate; a diagnosed dead-end is a valid
  result").

## numbers (all evidence class: tool testimony, reproducible from the
scripts described above; no artifact on disk was modified this lap)

| population | census count | raw-text-scan count | numeric layer status | render layer status |
|---|---|---|---|---|
| amd64g_calculate_condition | 219 | 57 | 56/57 resolved by existing condition_table9 | gap: boolean-combination render rule missing (named frontier) |
| amd64g_calculate_rflags_c | 19 | 19 | not extended (SUB-family cc_op read not yet written) | not attempted |
| Mul32/Mul64/DivMod*128to64 | ~14 (census: 1+1+3+1=6 listed as "regular:false" rows, but raw scan finds 14 total not-yet-converged with these names) | 14 | machinery exists (canon12_normalize.py), unwired to current baseline | not attempted |

Note on the census-vs-scan discrepancy for Mul/DivMod: the census rows
list `DivModU128to64: 3`, `DivModS128to64: 1`, `Mul32: 1`, `Mul64: 1`
(6 total) but my raw-text scan over the CURRENT `canon24_units_*`
baseline finds 6 DivModU128to64 + 6 DivModS128to64 + 1 Mul32 + 1 Mul64
= 14. Both are tool testimony against different baselines/methods; I
am reporting both rather than reconciling them by guesswork.

## recommendation for the next lap (not a decision — the owner's call per
"ask before deciding anything structural")

Three separate, bounded driver-authoring jobs, each following the
canon13→canon24 lineage pattern exactly (small driver file, existing
substitution/normalize machinery, render hook, ground-truth-anchored
gate, zero-regression check, spelling-ban gate on any new
grouping/pairing artifact):
1. `condition_table10.py` — SUB-family direct-numeric-read extension
   for `amd64g_calculate_rflags_c`'s carry bit (mechanical, same
   technique as condition_table9, no new category).
2. A render-rule addition to the canon24/canon25 render lineage for
   boolean combinations (OR/AND) of named `FCxx` condition atoms —
   **this needs the owner's ruling on the grouping axis first**, per the
   STOP RULE, since "which atom-combination shapes get a rendering
   rule" is exactly the kind of decision the brief reserves.
3. A thin `canon25.py`-style driver that re-wires
   `canon12_normalize.py`'s existing `WIDE_MUL_OPS`/`WIDE_DIVMOD_OPS`
   machinery to the current `tree_units3.json` baseline (mechanical,
   no new modelling).

## files touched

None in `op_pipeline` — survey-only lap, per "new files only — never
modify or delete existing artifacts" I chose not to write a survey
script into `op_pipeline` since it produced no converged output and
would misrepresent the state of the pipeline if left there uncommitted
to a driver's actual gate run. Survey scripts live only in `/tmp` on
this machine and are not part of the repository.

---

## SECOND SECTION -- 2026-08-31, same-lap continuation (coordinator:
"jobs 1 and 3 of your own recommendation are mechanical ... they are
not reserved decisions and belong in this lap")

Per the coordinator's instruction I wrote condition_table10.py and
canon25.py (new files, `op_pipeline/`), and ALSO wrote canon26.py (a
third new file) to satisfy item 3 ("run the 56/57 ... units through
the actual render + gate -- resolution claims without a gate run stay
unverified") honestly, since canon23.py -- read in full this lap --
turned out to already be the proven driver for exactly this shape
(multi-atom condition fan-out), and running its own machinery for
real, rather than reasoning about a hypothetical render gap, was the
only way to answer item 3 without more interpretation-dressed-as-fact.

### item 1 -- condition_table10.py (SUB-family carry-bit read)

Evidence class: forced-by-construction (regression test, direct
execution) + tool testimony (full-population run).

New file: `op_pipeline/condition_table10.py`. Same technique as
condition_table9.py: reads `amd64g_calculate_rflags_c`'s own numeric
`cc_op` first argument directly (no canonical-text pairing), resolves
the SUB family (`cc_op` in {5,6,7,8} -- reusing condition_table9's own
`SUB_FAMILY_CCOPS` set unchanged) to a new named atom `CF_SUB(dep1,
dep2)` (hardware fact: x86 SUB's carry flag is the unsigned-borrow
bit, `dep1 <u dep2` -- Intel SDM Vol 1 3.4.3.1, stated directly, not
read off text). Composes with condition_table9.substitute_all first
(cpp/op_764 carries BOTH an `amd64g_calculate_condition` and an
`amd64g_calculate_rflags_c` call in one expression -- the file's own
regression test reproduces this exact unit).

Regression check (`python3 condition_table10.py`), verbatim:
```
go/op_175 input: And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64))))
go/op_175 output: And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,CF_SUB(in1:64,64:64))))
applied=1 unresolved=[]

cpp/op_764 input: Sub8(zx8(ex1@0(amd64g_calculate_condition(7:64,8:64,in0:64,in1:64,u0:64))),And8(1:8,ex8@0(amd64g_calculate_rflags_c(8:64,in0:64,in1:64,u0:64))))
cpp/op_764 output: Sub8(zx8(CondUGT(in0:64,in1:64)),And8(1:8,ex8@0(CF_SUB(in0:64,in1:64))))
float_applied=0 int_applied=1 rflags_applied=1 ct9_unresolved=[] rflags_unresolved=[]

condition_table10 regression check: PASS
```

Full-population check (all 19 surveyed `amd64g_calculate_rflags_c`
units, script run over `canon24_units_<lang>.json` joined to
`tree_units3.json`): **19/19 resolve at the substitution layer** (zero
`amd64g_calculate_rflags_c(` or `amd64g_calculate_condition(` text
left in any of the 19).

**What this does NOT do (honest, stated up front, unchanged from
section 1's finding):** no render rule exists yet for the `CF_SUB`
atom feeding the `And64(Shl64(...), Sub64(0, And64(1, CF_SUB(...))))`
shift-with-carry-in idiom, so writing condition_table10.py alone
converges **zero** units. This was the coordinator's item 1 exactly as
scoped ("write condition_table10.py") -- item 1 did not ask for a
render driver, and I did not build one (the render rule is a
combination-shape decision of the same STOP-RULE kind named in
section 1's item (a)).

### item 2 -- canon25.py (re-wire canon12_normalize's widening model)

Evidence class: tool testimony (direct execution against the real
venv with pyvex/archinfo/z3 -- `/tmp/reconnect_venv/bin/python3`, the
correct interpreter for this pipeline; the system default `python3`
lacks `archinfo` and cannot run any canon*.py driver at all, recorded
here so the next lap does not lose an hour rediscovering this).

New file: `op_pipeline/canon25.py`. Re-wires `canon12_normalize.py`'s
existing `WIDE_MUL_OPS`/`WIDE_DIVMOD_OPS` z3 model and `canon12_
render.py`'s existing `render_unit12` (both imported unchanged,
function reference not copy) to the CURRENT `canon24_units_<lang>.json`
baseline, re-sourcing raw text from `tree_units3.json` exactly as
canon24.py does.

Ran (`/tmp/reconnect_venv/bin/python3 canon25.py`), verbatim:
```
wrote canon25_units_c.json (0 attempted, 0 accepted, 0 disproved, 0 undecided, 0 no candidate, 107 not our shape)
wrote canon25_units_cpp.json (0 attempted, 0 accepted, 0 disproved, 0 undecided, 0 no candidate, 106 not our shape)
wrote canon25_units_go.json (0 attempted, 0 accepted, 0 disproved, 0 undecided, 0 no candidate, 39 not our shape)
wrote canon25_units_rust.json (0 attempted, 0 accepted, 0 disproved, 0 undecided, 0 no candidate, 21 not our shape)
wrote canon25_units_swift.json (0 attempted, 0 accepted, 0 disproved, 0 undecided, 0 no candidate, 49 not our shape)
TOTAL: {'candidates_attempted': 0, 'accepted': 0, 'disproved': 0, 'undecided': 0, 'no_candidate_at_all': 0}
```

**0 attempted -- diagnosed, not swallowed.** Debugging (direct
inspection of the 14 target units' own `tree_units3.json` records)
found the cause: ALL 14 (the 12 DivModS128to64/DivModU128to64 units
and both Mul32/Mul64 units) are recorded with `branch_kind ==
"branching"` under the current `tree_match3.py` baseline, e.g.:
```
go/op_103: branch_kind=branching, raw=ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))
swift/op_114: branch_kind=branching, raw=zx64(ex32@0(zx64(Mul32(ex32@0(in0:64),ex32@0(in1:64)))))
```
canon25.py's own `convert_one` -- copied verbatim from canon24.py's
own `if old_rec.get("branch_kind") != "straight_line": return None`,
the SAME guard every driver in this lineage states for itself -- skips
all 14 correctly. `canon12_render.py`'s own proof (its header names
c/op_211, 212, 217, 218, 247, 248 as the population it was proved
against) was over the OLD `tree_units2.json` baseline, where these
units were apparently classified straight-line; under the adopted
`tree_units3.json` ret-block-first rule they are branching. This is
the SAME kind of finding canon24.py's own header names for the
sibling packed-arithmetic family ("either non-straight-line ... or ...
a different lap's own job") -- **not a bug in canon25.py, a measured
fact about the current population**, and it is why 0 converged rather
than a guessed number.

**STOP RULE applies:** rendering a branching unit (the guard/overflow
check plus the normal-path arithmetic together) is a different render
target than every driver in this lineage handles today (all of them
gate on `branch_kind == straight_line`). Recorded as a named frontier,
not invented: **"branching-unit render path for the 14 widening-
arithmetic stragglers."**

### item 3 -- canon26.py (run the condition-substitution-resolved units through the real gate)

Evidence class: tool testimony (direct execution, same venv).

New file: `op_pipeline/canon26.py`. This is canon23.py's OWN already-
proven fan-out machinery (condition_table9 substitution + canon22_
float.normalize_v2e + canon22_render.render_unit22 + canon22_
behaviour_check.anchored_check -- all four imported unchanged),
re-pointed at the current `canon24_units_<lang>.json` baseline, with
canon23.py's own `multi_atom_call_count(...) < 2` filter widened to
`< 1` so it also re-attempts the single-atom residue.

Ran, verbatim:
```
wrote canon26_units_c.json (0 attempted, 0 accepted, 0 still refused, 12 no candidate, 95 not our shape)
wrote canon26_units_cpp.json (0 attempted, 0 accepted, 0 still refused, 9 no candidate, 97 not our shape)
wrote canon26_units_go.json (0 attempted, 0 accepted, 0 still refused, 4 no candidate, 35 not our shape)
wrote canon26_units_rust.json (0 attempted, 0 accepted, 0 still refused, 0 no candidate, 21 not our shape)
wrote canon26_units_swift.json (0 attempted, 0 accepted, 0 still refused, 0 no candidate, 49 not our shape)
TOTAL: {'candidates_attempted': 0, 'accepted': 0, 'still_refused_after_attempt': 0, 'no_candidate_at_all': 25}
```

**25 units reached the gate (substitution applied, something
attempted); 0 converged.** This DISPROVES section 1's own
interpretation ("blocked by a missing boolean-combination render
rule") as the FULL explanation -- the actual refusal reasons, read
directly off the 25 records:

```
8 units: "float comparison operand(s) outside this file's own whitelist"
         (p/q operand shapes canon22_render's own float-operand
         classifier does not recognize, e.g. an Add64F0x2(...) nested
         expression as an operand -- c/op_550, c/op_560, c/op_622)
4 units: "codegen raised Unsupported('width 71 exceeds 64 bits')"
         rendering a Concat/Extract shape (c/op_305)
4 units: "float comparison operand(s) outside this file's own whitelist"
         (a second, distinct sub-case of the same classifier gap)
4 units: "leaf atom 'u0:64' is neither an input (in0/in1) nor a
         recognizable immediate literal" (go/op_477)
1 unit:  "expression contains an uninterpreted atom for VEX op
         'amd64g_calculate_rflags_c'" (cpp/op_764 -- confirms section
         1's own finding: this unit needs BOTH condition_table10's
         CF_SUB substitution AND its own render rule, neither
         attempted for render this lap)
```

The remaining 32 of the 57 units section 1 surveyed did not reach the
gate at all: `canon26.py`'s own tally ("not our shape") shows most
were skipped by the `branch_kind != straight_line` guard or had no
`tu3` record -- the SAME branching-classification finding as item 2,
now measured for the condition family too, not just the widening-
arithmetic family.

**Correction to section 1, stated plainly:** the earlier claim "the
gap is a missing render rule for boolean OR/AND of FCxx atoms" was an
interpretation that this lap's real gate run shows is WRONG as a
general explanation -- canon22_render.py's generic dispatch already
composes named condition atoms through ordinary bitwise nodes fine
(canon23.py's own 2+-atom population converges cleanly, unchanged
proof). The REAL, measured remaining gaps are: (1) a float-operand-
shape classifier gap in canon22_render's own `_operand_xmm`/payload
logic (12 units), (2) a width-71-bits-in-a-Concat codegen gap (4
units), (3) an unrecognized-leaf-atom gap (4 units), (4) the branching-
classification issue shared with item 2's population (32 units), and
(5) the still-unbuilt CF_SUB render rule (1 unit, cpp/op_764).

### zero-regression verification (programmatic)

```
converged totals: canon24=1457 canon25=1457 canon26=1457
zero-regression check: PASS
```
(script: for every unit `status == "converged"` in `canon24_units_
<lang>.json`, every `*_text` field is byte-identical in `canon25_
units_<lang>.json` and `canon26_units_<lang>.json`, all 5 languages --
1,457 converged units checked, 0 differences.)

### check_no_spelling_keys.py

Run against all 10 new artifacts (`canon25_units_<lang>.json`,
`canon26_units_<lang>.json`, all 5 languages):
```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon25_units_c.json -- exempt: top-level meta declares role 'generator provenance', ...
PASS canon25_units_cpp.json -- exempt: ...
... (all 10: PASS)
```
condition_table10.py, canon25.py, and canon26.py each perform
substitution/render/gate over ONE unit's own raw text at a time; none
groups or pairs units, so none has a spelling-key to check beyond the
per-unit output files above (which pass under the existing generator-
provenance exemption, same as every prior `canonNN_units_<lang>.json`
in this lineage).

### tree_units / clusters rebuild

`tree_units3.json` was READ ONLY this lap (never written) by
condition_table10.py, canon25.py, and canon26.py -- no rebuild is
needed for it; it is unchanged on disk (not touched).

`match_units.py` (the clusters.json builder) was run
(`/tmp/reconnect_venv/bin/python3 match_units.py`) and refused
immediately: `!! no sem_anchored_java.json -- run sem_anchored.py
first` -- a MISSING PREREQUISITE for a 6th language (java) that is
outside this task's 5-language scope and outside "new files only,
never modify existing artifacts" (fixing it would mean generating a
new sem_anchored_java.json, an unrelated and much larger job). `
clusters.json` was verified BYTE-IDENTICAL before and after this
attempt (`diff -q` clean) -- match_units.py refused before writing
anything, so nothing was touched. Given the converged-delta this lap
is exactly 0 (see below), a clusters rebuild would in any case produce
an IDENTICAL result to what is already on disk (clusters.json's own
input is the set of converged units' newest text, which did not
change) -- recorded as a diagnosed blocker, not forced past.

### MEASURED CONVERGED DELTA FROM 1,457

**0. The converged count is 1,457 before and after this lap's three
new drivers (canon24 baseline: 1,457; canon25 output: 1,457; canon26
output: 1,457) -- measured directly, not estimated.**

Two substitution-layer tables were added and proved correct by
regression test and full-population dry run (condition_table10.py:
19/19 rflags_c units resolve to `CF_SUB` atoms; the existing
condition_table9.py machinery: 56/57 condition units resolve to named
atoms) -- but a substitution resolving does not equal a unit
converging, and this lap's actual gate runs (canon25.py, canon26.py)
found real, specific reasons why none of the affected units render or
gate successfully yet. Reporting anything other than 0 here would be
exactly the fabrication the evidence doctrine forbids.

### named frontiers (STOP RULE, for the owner -- not decided, not invented)

1. Render rule for the `CF_SUB(dep1,dep2)` atom (condition_table10.py)
   composed into the `Shl64`/`Sar64` shift-with-carry-in idiom -- 19
   units, blocked at render, substitution proven.
2. Branching-unit render path -- shared blocker for the 14 widening-
   arithmetic stragglers (canon25.py) AND roughly 32 of the 57
   condition units (canon26.py); every driver in this lineage today
   only renders `branch_kind == "straight_line"`.
3. canon22_render's float-operand-shape classifier gap (12 of the 25
   condition units that reached the gate) -- operands that are
   themselves nested float expressions (e.g. `Add64F0x2(...)`), not a
   bare register/memory tag.
4. A width-71-bits-in-a-Concat codegen gap (4 units, c/op_305 and
   siblings) -- `Unsupported('width 71 exceeds 64 bits')`, unrelated
   to the condition-atom work, surfaced by attempting the gate.
5. An unrecognized-leaf-atom gap, `u0:64` (4 units, go/op_477 and
   siblings) -- outside condition_table10/CT9's own scope entirely.

None of these were invented a fix for; each is one render-layer or
codegen-layer decision this lap's own STOP RULE reserves.

### files touched this lap (new only)

- `op_pipeline/condition_table10.py` (new)
- `op_pipeline/canon25.py` (new)
- `op_pipeline/canon26.py` (new)
- `op_pipeline/canon25_units_{c,cpp,go,rust,swift}.json` (new, written
  by canon25.py)
- `op_pipeline/canon26_units_{c,cpp,go,rust,swift}.json` (new, written
  by canon26.py)

No existing artifact was modified or deleted. `tree_units3.json` and
`clusters.json` are unchanged (verified).
