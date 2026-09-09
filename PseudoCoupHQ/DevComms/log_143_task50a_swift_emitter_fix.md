# log 143 — Task 50(a): the swift probe emitter's `@_cdecl` test, fixed and measured

Date: 2026-09-02. Implementer: Claude Code (Opus), fenced brief from
round 10 (`log_142_claude_code_task_briefs_round10.md`, TASK 50 part
(a)). The finding this closes is F45-4 of
`log_137_task45_type_second_witness.md`; the sequencing call is
`log_140_open_calls_explained.md` §4, where the owner's lean was "fix now".

Every rendering below is labelled **LITERAL** (the object itself,
quoted from a named file), **GLOSS** (a plain-words reading sitting
next to its literal) or **ANALOGY**. Protocol §5.1a.

---

# 1. What was wrong, what was done, what it measures

## 1.1 The one-sentence statement

The swift probe emitter attached an export attribute after testing only
the function's RESULT type. A probe whose result is fine but whose
PARAMETER is a 128-bit integer therefore got an attribute the compiler
would not honour, and swiftc refused the whole function. The test now
covers the result and every parameter, and the set of types it tests
against is no longer written by hand — it is measured from the compiler.

## 1.2 The three numbers that say whether it worked

- **276 of 276.** Every probe log 137 counted under F45-4 now compiles.
  Set equality, both directions, against the banked id set.
- **0 regressions.** Of the 891 probes the fix newly exports, none was
  accepted before and refused after; all 630 that still refuse were
  already refused in the banked store, for reasons that never mention
  the attribute.
- **516 = 516.** The probes whose generated text the fix changes in the
  narrowing direction are EXACTLY the probes the compiler refused with
  that diagnostic. Set equality, computed, pasted in §5.2.

## 1.3 The banked population predates this fix — stated, as the brief requires

The 29,288 accepted probes banked on 2026-09-02 (log 131, validated in
`regen_witness_validation1.json`) were produced by `probe_gen.py`'s
emitter as it stood before today. Nothing in this task re-ran the
regeneration, rewrote a store, or altered a manifest. A future
regeneration WILL differ from the banked one in swift, by the 1,407
sources §5.1 counts; that was the whole content of the sequencing call
in log 140 §4, and it is now paid.

## 1.4 The choice the brief asked me to state

`probe_gen.py` is not edited. `probe_gen2.py` already exists and is the
regeneration's candidate builder, so the corrected emitter is a THIRD
file, **`probe_gen3.py`**, which imports `probe_gen` and replaces
exactly one function. Same shape probe_gen2.py already uses, for the
same reason: the two cannot drift, because everything except the one
changed function is imported rather than copied.

---

# 2. The defect, with values moving

## 2.1 The name at the top of this sub-tree, glossed before it is used

`@_cdecl("op_375")` is a swift attribute. **GLOSS:** it asks swiftc to
export the function under the C calling convention with the symbol name
in the quotes. The probe pipeline wants that, because every later stage
looks a unit up by the symbol `op_N`; without the attribute the symbol
is swift's mangled name and the probe records `symbol_exact: false`.

Swift only honours the attribute when every type the function shows to
C can be expressed in C. A 128-bit integer in swift is an ordinary
struct (`public struct Int128`), and a struct has no C spelling here, so
a function carrying one cannot be exported.

## 2.2 The literal defect

**LITERAL** — `~/Programming/PseudoCoupHQ/Research/op_pipeline/probe_gen.py`,
lines 361 and 364–377, unchanged on disk (md5 `a5cb8a36…`, §6.2):

```python
C_REPRESENTABLE = {"Int32", "Int64", "UInt64", "Float", "Double", "Bool"}


def emit_swift(n, op, arity, pos, lt, rt, res):
    params = "_ a: %s" % lt
    if arity == "binary":
        params = "_ a: %s, _ b: %s" % (lt, rt)
    body = expression(op, arity, pos)
    cdecl = res in C_REPRESENTABLE
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    if cdecl:
        lines.append('@_cdecl("op_%d")' % n)
    lines.append("public func op_%d(%s) -> %s {" % (n, params, res))
    lines.append("    return %s" % body)
    lines.append("}")
    return "\n".join(lines) + "\n", cdecl
```

**GLOSS:** `lt` and `rt` are the two parameter types and `res` is the
result type. The line `cdecl = res in C_REPRESENTABLE` reads `res`. It
never reads `lt`. It never reads `rt`. So the parameters cannot
influence the decision at all.

## 2.3 One probe, walked with its actual types

Take `swift/probe_375`. Its holders are `Int` on the left and `Int128`
on the right; its result type is `Bool`.

Step 1 — the emitter computes `cdecl`. `res` is `"Bool"`. `"Bool"` is in
the six-spelling set. So `cdecl` is true, and the attribute line is
written. `lt = "Int"` and `rt = "Int128"` were never consulted.

Step 2 — the source that lands in the lane. **LITERAL**, the stored
`source` field of probe 375 in `probe_manifest2_swift.json`:

```swift
// probe 375 -- binary <
@_cdecl("op_375")
public func op_375(_ a: Int, _ b: Int128) -> Bool {
    return a < b
}
```

Step 3 — what swiftc says. **LITERAL**, the `refused` field of the same
probe in `trickle_store/op_units2_swift_c0000.json`, banked 2026-09-02:

```
/work/regen_swift_c0000/u/n375/unit.swift:3:13: error: method cannot
be marked @_cdecl because the type of the parameter 2 cannot be
represented in Objective-C
```

**GLOSS:** "parameter 2" is `b`, the `Int128`. The compiler is
complaining about the attribute, not about `a < b`. Remove the
attribute and the function is ordinary swift.

Step 4 — what the corrected emitter writes for the same record.
**LITERAL**, the `source_after` field of probe 375 in
`task50a_diff1.json`:

```swift
// probe 375 -- binary <
public func op_375(_ a: Int, _ b: Int128) -> Bool {
    return a < b
}
```

One line gone. Nothing else in the text moves.

Step 5 — what swiftc says now. **LITERAL**, the row for probe 375 in
`task50a_raw/recompile_swift.txt`, compiled today in the `trickle`
instance: verdict `ACCEPT`, empty diagnostic. The probe compiles.

---

# 3. Where "C-representable" now comes from

## 3.1 Why the hand list had to go, not just be extended

The brief required the answer be derived from witness data rather than
a hand list. There was no such field to read: `type_inventory3.json`
records, per swift type, which authorities admit the spelling and
whether the compiler will accept it as a declaration — it records
nothing about the export attribute. **So the witness was measured, in
the shape the inventory already uses for its `declarable` field: one
tiny compile per type per position, in the trickle instance, no operator
anywhere in the source.**

## 3.2 The two forms compiled, per type

**LITERAL** — the two sources for `Int128`, as
`swift_cdecl_witness1.py` writes them (echoed by `--emit`, and quoted
back inside the compiler's own diagnostics in §3.4):

```swift
@_cdecl("cdeclHolder")
public func cdeclHolder(_ a: Int128) -> Int32 {
    return 0
}
```

```swift
@_cdecl("cdeclAnswer")
public func cdeclAnswer(_ a: Int32) -> Int128 {
    return Int128(0)
}
```

**GLOSS:** the first pins the result at a type the corpus already
exports, so a refusal is about the parameter. The second pins the
parameter for the mirror reason. Both positions are recorded
separately, because assuming one position answers for the other is
precisely the defect being fixed.

The zero value in the result form is built from the type's own recorded
CLASS in the inventory (`truth_value` returns `false`; every other class
returns `T(0)`), and a class the program has no construction for is
refused by name rather than guessed at.

## 3.3 The run

**LITERAL** — the terminal, host side:

```
$ /tmp/reconnect_venv/bin/python3 swift_cdecl_witness1.py --run
swift   34 compilations (17 types x 2 forms) -> .../task50a_lanes/cdecl_swift.sh
instance trickle  runner trickle-runner  cpus 6  agent ~/Programming/Airlock/instances/trickle/agent
dropped ~/Programming/Airlock/instances/trickle/agent/drop/cdecl_swift.sh
status: {"script": "cdecl_swift.sh", "state": "done", "exit": "0", "started": "2026-09-02T23:37:59+00:00", "finished": "2026-09-02T23:38:07+00:00", "elapsed_s": "7.2", "verdict": "exit 0"}
wrote .../swift_cdecl_witness1.json
tally: {"cdecl_parameter_accept": 15, "cdecl_parameter_refuse": 2, "cdecl_result_accept": 15, "cdecl_result_refuse": 2}
  Bool       parameter ACCEPT result ACCEPT
  Double     parameter ACCEPT result ACCEPT
  Float      parameter ACCEPT result ACCEPT
  Float16    parameter ACCEPT result ACCEPT
  Float80    parameter ACCEPT result ACCEPT
  Int        parameter ACCEPT result ACCEPT
  Int128     parameter REFUSE result REFUSE
  Int16      parameter ACCEPT result ACCEPT
  Int32      parameter ACCEPT result ACCEPT
  Int64      parameter ACCEPT result ACCEPT
  Int8       parameter ACCEPT result ACCEPT
  UInt       parameter ACCEPT result ACCEPT
  UInt128    parameter REFUSE result REFUSE
  UInt16     parameter ACCEPT result ACCEPT
  UInt32     parameter ACCEPT result ACCEPT
  UInt64     parameter ACCEPT result ACCEPT
  UInt8      parameter ACCEPT result ACCEPT
operator inventory: 91 tokens read from probe_manifest_*.json
PASS swift_cdecl_witness1.json -- no operator token in any key, grouping, pairing or row structure
```

Flags: `/persist/swift/usr/bin/swiftc -Onone -g -c`, copied from
`lane_gen.py :: compile_probe` anchor mode — the probe lanes' own.
Toolchain banner printed by the lane itself: `Swift version 6.0.3
(swift-6.0.3-RELEASE)`, `Target: x86_64-unknown-linux-gnu`.

## 3.4 The two refusals, verbatim

**LITERAL** — the `parameter_form.refusal` and `result_form.refusal`
fields of `Int128` in `swift_cdecl_witness1.json`:

```
/work/decl_swift/u/d00013/decl.swift:2:13: error: method cannot be marked @_cdecl because the type of the parameter cannot be represented in Objective-C
1 | @_cdecl("cdeclHolder")
2 | public func cdeclHolder(_ a: Int128) -> Int32 {
  |             |                `- note: Swift structs cannot be represented in Objective-C
  |             `- error: method cannot be marked @_cdecl because the type of the parameter cannot be represented in Objective-C
3 |     return 0
4 | }
```

```
/work/decl_swift/u/d00014/decl.swift:2:13: error: method cannot be marked @_cdecl because its result type cannot be represented in Objective-C
1 | @_cdecl("cdeclAnswer")
2 | public func cdeclAnswer(_ a: Int32) -> Int128 {
  |             |                          `- note: Swift structs cannot be represented in Objective-C
  |             `- error: method cannot be marked @_cdecl because its result type cannot be represented in Objective-C
3 |     return Int128(0)
4 | }
```

`UInt128` gives the same two, with its own spelling. Evidence class:
**the tool's own testimony** — swiftc reporting on what swiftc will
accept, one compile per claim.

## 3.5 The corrected test

**LITERAL** — `probe_gen3.py`:

```python
def cdecl_allowed(lt, rt, res):
    parameter_ok, result_ok = representable_sets()
    if res not in result_ok:
        return False
    if lt not in parameter_ok:
        return False
    if rt is not None and rt not in parameter_ok:
        return False
    return True
```

`representable_sets()` reads `swift_cdecl_witness1.json` and refuses if
the file is not there — there is no hand list left to fall back to.

---

# 4. A second defect the measurement exposed, reported rather than hidden

## 4.1 The hand list was wrong in both directions

**LITERAL** — the terminal:

```
$ /tmp/reconnect_venv/bin/python3 probe_gen3.py
measurement read from swift_cdecl_witness1.json
  accepted in a parameter position: 15 types
  accepted in a result position:    15 types
  the old hand list held 6 spellings
```

**GLOSS:** the hand list named six spellings. The compiler accepts
fifteen of the inventory's seventeen, in both positions, refusing only
the two 128-bit integers. So besides attaching the attribute where the
compiler refuses it (the F45-4 defect), the old emitter also WITHHELD
the attribute from probes the compiler would have exported — every
probe whose result type is `Int8`, `Int16`, `Int`, `UInt`, `UInt8`,
`UInt16`, `UInt32`, `Float16` or `Float80`.

## 4.2 Why this matters to the pipeline, not just to tidiness

A probe without the attribute still COMPILES; it records
`symbol_exact: false` and carries swift's mangled symbol instead of
`op_N`. So this second defect never showed up as a refusal — it showed
up as probes the later stages have to resolve the harder way. 261 of
the 891 newly-exported probes compile, so a future regeneration gains
261 swift units with exact `op_N` symbols that today carry mangled
ones.

## 4.3 This is why the diff is not the 276 the brief predicted

The brief expected "exactly the 276 differ". It is not 276, and the
number was not tuned to make it so. The honest decomposition is in §5;
the short form: 516 lose the attribute (the 276 counted in log 137 plus
240 that carry the identical cause but sat outside the legality
oracle's scope, so log 137 never counted them as misses), and 891 gain
it, from the second defect above.

---

# 5. The diff over the whole swift candidate set

## 5.1 Both candidate sets walked, every stored source compared

**LITERAL** — the terminal:

```
$ /tmp/reconnect_venv/bin/python3 task50a_diff1.py
probe_manifest_swift.json     1086 candidates   1086 unchanged     0 changed  {}
probe_manifest2_swift.json    4187 candidates   2780 unchanged  1407 changed  {'attribute_added': 891, 'attribute_removed': 516}
banked shape count 276 ; re-derived from 11 store files: 276
attribute_removed in the regeneration set: 516
in the refusals but not fixed: 0
fixed but not in the refusals: 240
wrote .../task50a_diff1.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS task50a_diff1.json -- no operator token in any key, grouping, pairing or row structure
```

| candidate set | file | candidates | text unchanged | text changed |
|---|---|---:|---:|---:|
| the original run (6 hand-written holders) | `probe_manifest_swift.json` | 1,086 | 1,086 | **0** |
| the regeneration (extracted scalar core) | `probe_manifest2_swift.json` | 4,187 | 2,780 | 1,407 |

**GLOSS of the zero:** the original run's six holder types are all
inside both the old six-spelling list and the measured fifteen, so the
fix cannot touch any of its 1,086 sources. The original corpus is
byte-identical under the corrected emitter.

## 5.2 The narrowing direction is EXACTLY the compiler's refusals

**LITERAL** — the terminal, a set comparison over the trickle stores:

```
$ /tmp/reconnect_venv/bin/python3 -c "..."
all swift probes refused with this shape: 516
attribute_removed set: 516
shape-set == removed-set: True
```

**GLOSS:** the set of swift probes swiftc refused with that diagnostic,
and the set of probes whose attribute the fix removes, are the same 516
ids. Not overlapping — equal. Evidence class: **forced by
construction**, over the whole banked swift population.

Every one of the 516 has a 128-bit holder and a C-representable result
— the exact defect shape:

```
REMOVED: how many have a 128-bit holder:
  516 of 516
REMOVED where the RESULT is 128-bit: 0
REMOVED by result_type: {'Bool': 464, 'Int32': 12, 'Int64': 12, 'UInt64': 12, 'Double': 8, 'Float': 8}
```

**GLOSS:** zero of the 516 has a 128-bit RESULT — which is why the old
result-only test passed all 516 through. The 128-bit type is always on
a parameter, the one place the old test could not see.

## 5.3 How 516 splits into 276 + 240

**LITERAL** — the terminal:

```
attribute_removed: 516
oracle-legal subset (log 137 F45-4 count): 276
now ACCEPT: 276
now-ACCEPT set == the log-137 276 set: True
the 240 that still refuse, filter_verdict tally: Counter({'no_rule': 240})
```

**GLOSS:** `regen_validate1.py` counted a MISS only inside the legality
oracle's scope — a probe the filter called `legal` that the compiler
refused. The other 240 carry the identical refusal and the identical
cause, but their filter verdict was `no_rule`, so the oracle predicted
nothing about them and they were never misses. The number 276 was
always a count of misses, never a count of the cause's sightings. The
cause's true population is 516.

---

# 6. The compile, and what it proves

## 6.1 The run

1,407 sources — every probe whose text the fix changes — compiled in
the trickle instance with the probe lanes' own anchor flags. The full
regeneration was NOT re-run: 1,407 compiles, not 129,553.

**LITERAL** — the terminal:

```
$ /tmp/reconnect_venv/bin/python3 task50a_recompile1.py --run
swift  1407 compilations -> .../task50a_lanes/recompile_swift.sh
  by direction of the text change: {'attribute_added': 891, 'attribute_removed': 516}
instance trickle  runner trickle-runner  cpus 6  agent ~/Programming/Airlock/instances/trickle/agent
status: {"script": "recompile_swift.sh", "state": "done", "exit": "0", "started": "2026-09-02T23:54:16+00:00", "finished": "2026-09-02T23:58:41+00:00", "elapsed_s": "264.6", "work_consumed_mb": "1", "verdict": "exit 0"}
tally: {
 "attribute_added_refuse": 630,
 "total": 1407,
 "attribute_added_accept": 261,
 "attribute_removed_accept": 276,
 "attribute_removed_refuse": 240
}
the 276 counted in log 137: 276, now {'ACCEPT': 276}
same cause, outside the oracle scope: 240, now {'REFUSE': 240}
still refusing: 870 ; regressions: 0
    505  error: type-casting operator expects a type on its right-hand side (got: parameter <Q>)
    136  error: cannot convert value of type <Q> to expected argument type <Q>
    128  error: argument type <Q> expected to be an instance of a class or class-constrained type
     36  error: cannot find operator <Q> in scope; did you mean <Q>?
     27  error: cannot convert return expression of type <Q> to return type <Q>
      9  error: <Q> may only be used to pass an argument to inout parameter
      9  error: value of optional type <Q> not unwrapped; did you mean to use <Q> or chain with <Q>?
      9  error: <Q> in a function that does not support concurrency
      9  error: cannot force unwrap value of non-optional type <Q>
      2  error: type <Q> cannot be used as a boolean; test for <Q> instead
wrote .../task50a_recompile1.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS task50a_recompile1.json -- no operator token in any key, grouping, pairing or row structure
```

(`<Q>` is `regen_validate1.shape_of`'s placeholder for a quoted span —
the same normalisation the banked validation used, so the shapes here
and there are comparable. The verbatim per-probe messages are in
`task50a_recompile1.json :: still_refusing`.)

| direction of the text change | compiled | accept | refuse |
|---|---:|---:|---:|
| attribute removed | 516 | **276** | 240 |
| attribute added | 891 | 261 | 630 |
| total | 1,407 | 537 | 870 |

## 6.2 The 276 — the claim the task exists to make

All 276 accept, and the accepting set IS the banked set (§5.3, set
equality both directions). F45-4 is closed: 276 refusals of one cause,
gone, with no legality content lost.

## 6.3 The 240 that still refuse are refusing for real reasons

**LITERAL** — one of them, from `task50a_recompile1.json ::
still_refusing`:

```
swift/probe_1117  Bool with Int128 -> Bool
/work/decl_swift/u/d00411/decl.swift:3:12: error: argument type 'Bool' expected to be an instance of a class or class-constrained type
1 | // probe 1117 -- binary !==
2 | public func op_1117(_ a: Bool, _ b: Int128) -> Bool {
3 |     return a !== b
  |            `- error: argument type 'Bool' expected to be an instance of a class or class-constrained type
4 | }
```

**GLOSS:** with the attribute gone the compiler has moved on to judging
the expression itself, and it says the operator does not apply to these
operands. That is the acceptance oracle doing its job — a refusal with
legality content, which is exactly what the pipeline wants a refusal to
be. Checked mechanically: **0 of the 240 mentions the attribute** in its
new diagnostic.

## 6.4 Zero regressions from the widening

**LITERAL** — the terminal:

```
attribute_added refusals: 630
any mentioning _cdecl: 0
banked verdict of those 630: Counter({'REFUSE': 630})
attribute_removed still refusing: 240 any mentioning _cdecl: 0
```

**GLOSS:** all 630 were already refused in the banked store, and none
of them refuses because of the attribute the fix added. So attaching
the attribute more widely took nothing away; it gained 261 exactly-named
symbols.

---

# 7. Guards, and what was not touched

## 7.1 The spelling-key check on every JSON written

The three products each run `check_no_spelling_keys.py` on themselves
and delete their own output on failure. All three passed on the first
run; the PASS lines are pasted in §3.3, §5.1 and §6.1.

```
PASS swift_cdecl_witness1.json -- no operator token in any key, grouping, pairing or row structure
PASS task50a_diff1.json        -- no operator token in any key, grouping, pairing or row structure
PASS task50a_recompile1.json   -- no operator token in any key, grouping, pairing or row structure
```

Where the token rides, and only there: the `operator` display field on
a probe record, and the expression inside a `source` / `refusal` string.
Nothing selects, keys or groups by it. The compiled set was selected by
PROBE ID from a diff computed on generated TEXT; rows are grouped by the
DIRECTION of the text change and by the COMPILER'S OWN message shape.
The C-representability decision reads TYPES only.

## 7.2 Zero regression — nothing that existed was altered

**LITERAL** — the terminal, after everything ran:

```
$ md5sum probe_gen.py probe_gen2.py probe_manifest_swift.json probe_manifest2_swift.json regen_witness_validation1.json type_inventory3.json
a5cb8a36d0e081cbd1cfa5aef3bd4b65  probe_gen.py
de01785ebf07399455f3c1a0ac0a0ac4  probe_gen2.py
ac36c1a56a5f6718df84c174b6c4bad6  probe_manifest_swift.json
1e760040e2c5ddf9eae426388c7a1ead  probe_manifest2_swift.json
d586d72869c38e1e6c3a494a75f1dc15  regen_witness_validation1.json
e4680dc422fa837b6733db040cd3c15e  type_inventory3.json

$ git -C ~/Programming/PseudoCoupHQ status --porcelain Research/op_pipeline/probe_gen.py Research/op_pipeline/trickle_store
(no output)
```

**GLOSS:** `probe_gen.py` is unedited, both manifests are unedited, the
banked validation and the corrected type inventory are unedited, and no
file in `trickle_store/` differs from what the daemon last committed.
New files only.

## 7.3 Which side of the container wall each step ran on

Generation, the two diffs and every count ran on the host. Only the 34
witness compilations and the 1,407 recompilations ran inside
`trickle-runner`. Every submission went through
`python3 ~/Programming/Airlock/airlock --instance trickle submit …`
(the `Instance` class in `trickle2.py`). **Nothing on the project side
ran podman**, per `TRICKLE_SUPERSEDED.md`.

## 7.4 One process event, recorded rather than hidden

The recompilation lane was submitted at 23:41:14 UTC and stopped at
about 23:41:37 with 125 of 1,407 done, its status file left saying
`running`. Cause: the trickle instance was brought DOWN while the lane
was in flight — the co-agent finishing Task 50(b) took the instance down
at the end of its own run (`log_144`, "Trickle instance brought down
after the run"). The lane was still queued in `agent/drop`, so bringing
the instance back up re-ran it from the start; it completed at 23:58:41
with exit 0. No result is a mixture of the two attempts: the lane
recreates its work root and reopens its product file at the top.

**Worth a decision from the owner (§9):** two agents sharing one Airlock
instance can stop each other's runs, and neither can see the other's
queue before acting.

---

# 8. Complete file inventory

## 8.1 New files written by this task

| file | bytes | what it is |
|---|---:|---|
| `Research/op_pipeline/swift_cdecl_witness1.py` | 13,505 | measures C-representability per swift type per position; builds the lane, submits it, folds the product |
| `Research/op_pipeline/swift_cdecl_witness1.json` | 10,944 | the measurement: 17 types × 2 positions, verdict + verbatim refusal |
| `Research/op_pipeline/probe_gen3.py` | 6,893 | the corrected `emit_swift`; imports `probe_gen`, replaces one function |
| `Research/op_pipeline/task50a_diff1.py` | 10,021 | walks both swift candidate sets, diffs generated text, cross-checks against the banked refusals |
| `Research/op_pipeline/task50a_diff1.json` | 702,604 | the 1,407 changed sources, before and after, with direction |
| `Research/op_pipeline/task50a_recompile1.py` | 12,537 | compiles the changed sources, tallies verdicts, names regressions |
| `Research/op_pipeline/task50a_recompile1.json` | 730,065 | the tallies, the 870 still-refusing with verbatim messages, the shape census |
| `Research/op_pipeline/task50a_lanes/cdecl_swift.sh` | 5,553 | the witness lane, generated |
| `Research/op_pipeline/task50a_lanes/recompile_swift.sh` | 31,544 | the recompilation lane, generated |
| `Research/op_pipeline/task50a_outbox/cdecl_swift.sh` | 5,553 | the copy handed to `airlock submit` |
| `Research/op_pipeline/task50a_outbox/recompile_swift.sh` | 31,544 | the copy handed to `airlock submit` |
| `Research/op_pipeline/task50a_raw/cdecl_swift.txt` | 3,196 | the witness lane's product, verbatim, marker-headed |
| `Research/op_pipeline/task50a_raw/recompile_swift.txt` | 589,352 | the recompilation lane's product, verbatim, marker-headed |
| `DevComms/log_143_task50a_swift_emitter_fix.md` | this file | the report |

## 8.2 Files read, not written

`probe_gen.py`, `probe_gen2.py`, `declare_lane.py` (its `lane()` and
driver are reused unchanged), `lane_gen.py`, `verbatim_diag.py`,
`regen_validate1.py` (its `shape_of` and `declarable_sets` are imported,
so the shapes here and in the banked validation are computed by the same
code), `trickle2.py` (its `Instance`), `type_inventory3.json`,
`legality_quirks.json`, `probe_manifest_swift.json`,
`probe_manifest2_swift.json`, `regen_witness_validation1.json`,
`trickle_store/op_units2_swift_*.json` (11 files),
`check_no_spelling_keys.py`.

---

# 9. Two lists

## 9.1 Decided, recorded for audit

- The corrected emitter lives in `probe_gen3.py`, importing `probe_gen`;
  `probe_gen.py` is untouched. (§1.4)
- C-representability is measured, not listed: a new witness file, in the
  same shape `type_inventory3.json` uses for `declarable`. (§3)
- The `attribute_added` half was compiled too, not only the 516. A
  widening that is not asked of the compiler is a guess; the answer is 0
  regressions. (§6.4)
- Both the 276 (log 137's oracle-scope count) and the 240 (the same
  cause outside the oracle's scope) are reported as separate
  populations, neither folded into the other. (§5.3)

## 9.2 Awaiting the owner

1. **Two agents share one Airlock instance and can stop each other's
   lanes** (§7.4). Whether an instance should refuse a `down` while a
   lane is running, or whether the convention is one instance per agent,
   is an Airlock question — flagged, not decided.
2. **When the swift regeneration is re-run**, it will produce 1,407
   sources differing from the banked ones: 516 losing the attribute (276
   of them turning refusal into acceptance) and 891 gaining it (261 of
   them turning a mangled symbol into `op_N`). The banked 29,288 predate
   the fix. Whether to re-run swift alone or wait for a whole-corpus
   regeneration is a sequencing call, not a design call.
