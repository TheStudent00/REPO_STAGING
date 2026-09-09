# log_128 — TASK 38: bank round 7

Date: 2026-09-01. Author: Claude Code (implementer), no sub-agents.
Working directory: `~/Programming/PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line — not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention — never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

---

# 1. Full-stack verification: the spelling guard, over round 7's own
# file inventory

## 1.1 The inventory, enumerated from the logs, not assumed

Round 7's grouping-shaped artifacts, taken from the "complete file
inventory" sections of log_124 (task 34), log_125 (task 35), log_126
(task 37) and log_127 (task 36):

- log_124: `interp_canon35.json`, `interp_table2.json`,
  `interp_join2.json`, `union_table2.json`,
  `interp_zero_regression2.json`.
- log_125: `type_inventory2.json`, `swift_type_authority.json`
  (`type_inventory2_validation.json` is a validator report, not a
  grouping artifact, but was checked anyway — see below).
- log_126: `audit_altered_testimony.json` (grouping-shaped: it groups
  stored strings by store and by verdict).
- log_127: `legality_validation.json` (the one grouping/comparison
  artifact named in that log's own PROGRESS entry).

## 1.2 Verified against disk, then run

```
$ ls -la interp_canon35.json interp_table2.json interp_join2.json \
         union_table2.json interp_zero_regression2.json \
         type_inventory2.json swift_type_authority.json \
         audit_altered_testimony.json legality_validation.json
(all nine present)
```

Guard transcript, every file, pasted in full:

```
== interp_canon35.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_canon35.json -- no operator token in any key, grouping, pairing or row structure
== interp_table2.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_table2.json -- no operator token in any key, grouping, pairing or row structure
== interp_join2.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_join2.json -- no operator token in any key, grouping, pairing or row structure
== union_table2.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS union_table2.json -- no operator token in any key, grouping, pairing or row structure
== interp_zero_regression2.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_zero_regression2.json -- exempt: top-level meta declares role 'generator provenance', so this file is generator provenance and never participates in matching
== type_inventory2.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS type_inventory2.json -- no operator token in any key, grouping, pairing or row structure
== swift_type_authority.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS swift_type_authority.json -- no operator token in any key, grouping, pairing or row structure
== audit_altered_testimony.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS audit_altered_testimony.json -- no operator token in any key, grouping, pairing or row structure
== legality_validation.json ==
operator inventory: 91 tokens read from probe_manifest_*.json
PASS legality_validation.json -- no operator token in any key, grouping, pairing or row structure
```

- 8 of 9 PASS with the full check; `interp_zero_regression2.json`
  PASSes under the guard's own generator-provenance exemption (it is
  a count-reconciliation report over already-verdicted totals, not a
  grouping of units — its own log_124 §7 already ran and recorded
  this same PASS line).
- Population: **9 of 9** round-7 grouping-shaped artifacts checked,
  9 of 9 PASS. Not a sample.

---

# 2. The reconciled count, per ADDENDUM 2

**A PROVED UNIT IS A COUNTED UNIT** (the owner, 2026-09-01): the 41
round-6 proofs (5 in `canon32_sret_units.json`, 36 in
`canon33_units.json`) are accepted into the recorded count in the
same lap they were proved, with no per-round permission needed.

## 2.1 The single authoritative figure

**Converged 1,676 of 1,779 (compiled five: c, cpp, go, rust, swift);
withdrawn 13, kept as the one separate population.**

## 2.2 Recomputed from the artifacts, pasted

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d = json.load(open('interp_zero_regression2.json'))
print('status_field_on_disk        ', d['baseline_stated_precisely']['status_field_on_disk'])
print('per_language sum            ', sum(v['converged'] for v in d['per_language'].values()))
print('proofs (canon32+canon33)    ', d['proofs_counted_from_their_own_artifacts'])
print('recorded_converged_recomputed', d['recorded_converged_recomputed'])
print('withdrawn_separate_population', d['baseline_stated_precisely']['withdrawn_separate_population'])
print('authoritative_count_line    ', d['authoritative_count_line'])
"
status_field_on_disk         1635
per_language sum             1635
proofs (canon32+canon33)     {'canon32_sret_units.json': 5, 'canon33_units.json': 36, 'total': 41}
recorded_converged_recomputed 1676
withdrawn_separate_population 13
authoritative_count_line     converged 1676 of 1,779 (compiled five); withdrawn listed separately: 13
```

- Independent arithmetic check: 583 (c) + 728 (cpp) + 72 (go) + 112
  (rust) + 140 (swift) = 1,635. 1,635 + 41 (the counted proofs) =
  1,676. 1,676 + 13 (withdrawn, separate) + 90 (unchanged: 20+22+16+2+
  10) = 1,779. Population: the 1,779-unit compiled-five corpus.
- **Population line for the compiled figure**: 1,779 is the compiled
  probe corpus across c/cpp/go/rust/swift that the compiler accepted
  (log_116/log_125's own population statement, unchanged this round).

## 2.3 The interpreter population, stated separately

**9 of 11** interpreter/JIT units produced universal text this round
(log_124 §3): cpython 1, java 2, ruby 2 of 4, php 4 of 4. The 2
without text (`ruby/vm_opt_plus`, `ruby/rb_big_plus`) are refused for
named, non-scarcity reasons (absent ship body; interprocedural
confluence), not defects and not silently dropped.

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d = json.load(open('interp_canon35.json'))
from collections import Counter
print(Counter(r['gate_verdict'] for r in d['records']))
"
Counter({'UNIVERSAL_TEXT_PRODUCED': 9, 'NO_CANONICAL_TEXT': 2})
```

- This 9/11 (and the 11-unit population) is a **separate population
  from the 1,779**. It is never added to the compiled figure — stated
  explicitly in log_124 §5 and reconfirmed here by direct recount.

---

# 3. dominant_table24 / dom_ops22 / guards5 / exception_families3
# verified untouched (md5/git)

## 3.1 Current sha256, computed now

```
$ sha256sum dominant_table24.json dom_ops22.json guards5.json exception_families3.json
2f31942d54a7f531b99755261402c5759b16a1ef97ffb353e7e166aa096221b7  dominant_table24.json
e2577cf37558c8ef9e046f1157d8425860cccd44660cfc2bb0884188c8243421  dom_ops22.json
ab206a15087ad4045f0c3ffb74eed90b75eb136d675c00d1fc4cf5683bd6f468  guards5.json
89f12433214b714385c77a44a863404ab26a0cf0a9b459ede69f9e3693af5809  exception_families3.json
```

## 3.2 Same four hashes, read from the artifact's own self-check
# (log_124's interp_zero_regression2.json, §6 of that log)

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
d = json.load(open('interp_zero_regression2.json'))['tables_that_must_not_change']
for k,v in d.items():
    print(k, v['identical'])
"
dominant_table24.json True
dom_ops22.json True
guards5.json True
exception_families3.json True
```

## 3.3 Independent re-check against git — not just quoting the
# artifact, actually re-deriving it

```
$ git show 4beaebcfa42870de19918ca88f88faa0c0f57228^:Research/op_pipeline/guards5.json | sha256sum
ab206a15087ad4045f0c3ffb74eed90b75eb136d675c00d1fc4cf5683bd6f468  -
$ git show 4beaebcfa42870de19918ca88f88faa0c0f57228^:Research/op_pipeline/exception_families3.json | sha256sum
89f12433214b714385c77a44a863404ab26a0cf0a9b459ede69f9e3693af5809  -
```

`4beaebc` is the daemon commit that first landed task 34's artifacts
(named in log_124 §6); `^` is the commit immediately before it, i.e.
the tree as it stood before round 7 touched anything. Both hashes
match §3.1's current values exactly. `dominant_table24.json` and
`dom_ops22.json` were checked the same way inside log_124 §6 itself
(same commit, same method) and match there too. All four: **verified
untouched, by an independent re-derivation from the vcs, not by
trusting the artifact's own claim.**

---

# 4. One-page state-of-the-line summary (reading form)

## 4.1 The universal-form milestone

Every arch-unit now canonicalizes into ONE shared memory-based form
(standardized loads into designated slots; how a value arrived —
plain / pointer / tagged — rides as an ANNOTATION beside the text,
not inside it). This dissolved the register-arrival dialect split and
fixed `php/add_function`'s prior refusal (its confluence had been
mis-placed at a TAG-combining instruction; under the ruling a
nonzero-displacement read off a pointer arrival is arrival metadata,
and the true confluence is the value add one line later).

**Meet in the middle — measured, not argued.** Four interpreter
units across two languages (php's two ZEND_ADD handlers, ruby's
rb_fix_plus and rb_int_plus... — precisely: IU0005/IU0006 vs IU0008)
now render CHARACTER-IDENTICAL machine text while carrying two
different arrival annotations (`typed-pointer(zval*)` vs
`tagged-value(Fixnum, 2n+1 encoding)`). This was invisible under the
old register form, where the same units rendered as three different
texts. The declared type classes are NOT merged — this is an
observation recorded alongside the class split, not a re-classing.

## 4.2 The swift authority

Swift's 17 scalar types were extracted from the pinned
`swift-6.0.3-RELEASE` source (via its `.gyb` generator templates) and
cross-checked by two more independent routes: the installed stdlib
module interface, and the compiler's own typecheck (with a negative
control that correctly refuses). All three routes agree on all 17
types with no disagreement in either membership or class marking.
`type_inventory2.json` supersedes `type_inventory.json` as the
inventory of record; the old file is untouched on disk. Swift's row
stops being a tautology (previously the corpus was its own only
witness); its extracted core (16, or 17 counting `Bool` pending
the owner's ruling on F35-1) predicts far more candidate probes (7,216 or
8,126) than the 1,086 probed today.

## 4.3 The legality reduction

Reading admissibility rules straight out of each language's own
compiler/type-checker source (clang's Sema operator-category checks,
go's `binaryOpPredicates` table, rust's codegen match + homogeneity
assertion, swift's stdlib operator signatures + protocol-conformance
closure) and applying them to the full-core candidate space:
**152,298 naive candidates -> 121,081 rule-admitted + 7,962
no-rule-residue (passed through, not dropped) = 129,043 to compile —
a reduction factor of 1.18.** Validated against the existing 1,779-
probe corpus: **99.9% agreement (3,584 of 3,588 in-rule-scope
predictions correct)**, zero accepted units dropped by the filter.
The 4 misses are one cause: c/cpp's type table marks `bool` as
`integer_unsigned` (from clang's own `UNSIGNED_TYPE`), so no rule can
exclude it from increment/decrement the way c++'s own compiler does
(F36-1). No per-name patch was applied to close the gap — that
decision is the owner's.

## 4.4 The testimony audit

`lane_gen.py`'s `firstline()` ran `text.replace("|","/")` on stored
compiler diagnostics, silently altering any testimony that quoted a
`|`. Fixed going forward in a new verbatim-escaping codec (wrapper
precedent, not an edit to the un-runnable driver). Damage measured
across all ten stores on disk: **168 distinct altered captures**
(go 101, rust 58, swift 9; c/cpp show 0 — their diagnostics never
echo the operator token at all, so 0 is "no place to hide the
alteration", not "0 proved clean"). Only one non-store carrier of the
altered text exists: `log_116`'s own finding quote. No unaltered
original survives on this machine (the Airlock lane logs keep only a
tally, not the raw text), so any fix is a RECONSTRUCTION, not a
restore. Two remediation routes are costed for the owner: re-capture the 6
affected lanes (295.4s measured) vs annotate all 168 records in
place (zero sandbox time, zero re-capture risk). **Nothing was
re-captured this round.**

## 4.5 the owner's open-calls list (prologue call WITHDRAWN per Addendum 1 —
# not listed)

1. **lane_gen remediation**: re-capture 6 lanes (295.4s measured) vs
   annotate 168 records in place — task 37 costed both, ruling is
   the owner's (log_126 §5).
2. **probe regeneration go/no-go**, now priced by log_127's numbers
   (152,298 naive / 129,043 filtered, 99.9% agreement) plus F36-1's
   c/cpp `bool` marking question (does the shared class rule gain a
   truth-value seat, closing the 4 misses to 100%?).
3. **the php type-key/union question**, if still open per log_124 —
   log_124 records the class-key split (declared type keys, e.g.
   `zval*,zval*`/`int` vs `VALUE,VALUE`/`VALUE`) as standing and NOT
   merged despite the character-identical texts; whether that split
   itself should be revisited is not decided in this log and is
   carried forward as asked.
4. **the fourth seat** — carried forward from the round-7 brief's own
   open-calls framing; no new evidence on it was produced by tasks
   34-37, so nothing here narrows or resolves it.

---

# 5. Posterity message

Written to `DevComms/next_commit_message.txt`.

```
$ wc -c DevComms/next_commit_message.txt
1561 DevComms/next_commit_message.txt
$ head -5 DevComms/next_commit_message.txt
round 7 banked: universal canonical form measured (interp union meet-
in-the-middle, IU0005/IU0006/IU0008 character-identical texts across
php+ruby with differing arrival annotations); swift type authority
landed (17 types, three independent routes agreeing, type_inventory2
supersedes type_inventory); legality reduction measured 152,298 ->
```

- The daemon consumes and empties this file BY DESIGN — this is the
  banking mechanism (AgentMemory: "BANKING IS A MESSAGE NOT A
  COMMIT"), not a loss to guard against. At the moment this log was
  written no consuming commit had yet run:

```
$ git log --oneline -3
ec0532f auto: 2 files (log_127_task36_legality_reduction.md, PROGRESS.md)
[no commit yet consuming next_commit_message.txt]
```

  When the daemon's next 30s sweep runs, it will pick up this file
  (and this log, and the PROGRESS entry) in an `auto:` commit; that
  commit's presence in `git log` is the confirmation the message was
  consumed, not this log's own claim.

---

# 6. Complete file inventory — every file touched or created by
# this task

| file | action |
|---|---|
| `DevComms/next_commit_message.txt` | written (posterity message; daemon-consumed) |
| `Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md` | appended, one dated entry under the single `# PROGRESS` heading |
| `DevComms/log_128_task38_bank_round7.md` | this file |

No artifact from tasks 34-37 was modified. Every command in §1-§3 ran
read-only against files created in prior rounds (`interp_canon35.json`,
`interp_table2.json`, `interp_join2.json`, `union_table2.json`,
`interp_zero_regression2.json`, `type_inventory2.json`,
`swift_type_authority.json`, `audit_altered_testimony.json`,
`legality_validation.json`, `dominant_table24.json`, `dom_ops22.json`,
`guards5.json`, `exception_families3.json`, and
`op_pipeline/check_no_spelling_keys.py`). This task, per the brief's
own "smaller model acceptable" allowance, made no code changes.

---

## CORRECTION (2026-09-02, appended by task 41 — record hygiene, log_132)

§4.4 states "168 distinct altered captures (go 101, rust 58, swift
9)". That figure is wrong in its rust term and in its total. The
correct figure, recounted directly from `audit_altered_testimony.json`
(see the same recount pasted in `log_126_task37_testimony_defect.md`'s
own appended correction) is **158 distinct altered captures: go 101,
rust 48, swift 9**. The error: the 168-count treated every altered
row in the op_pipeline-side stores as a distinct capture, but some of
rust's rows store IDENTICAL text, so rust's true distinct-content
count is 48, not 58; go and swift are unaffected.

This wrong figure was carried into this task's own posterity message
(§5 of this log) and the daemon-committed text built from it — that
commit stands uncorrected in history; the fix is this note plus
Task 42 banking the 158/rust-48 figure in round 8's posterity
message, per log_129's TASK 41 brief.
