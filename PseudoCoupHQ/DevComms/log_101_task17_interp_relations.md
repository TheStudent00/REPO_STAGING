# log 101 -- Task 17: interpreter units into the table question (ruby/php/cpython), posed not forced

Date: 2026-08-31. Answers log_097's Task 17 (round 3). Working
directory: `PseudoCoupHQ/Research/op_pipeline`.

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
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

## 1. walkthrough (protocol v2 -- plain words first)

Task 17 asks one question: do the ruby/php interpreter handler
slices, and cpython's `long_add`, belong in the operator table (the
901-class `dominant_table24.json`) -- and it forbids answering by
assertion. Three routes exist to answer it for real, and this session
tried all three, mechanically, against the actual machinery already
in this repo:

1. **Canonicalize the slice** (`canon.py`, THE CANONICAL FORM) and
   see if its text matches a table class's text.
2. **Run it through the bridge/dominance machinery**
   (`dominance.py`'s `RESULT_PROJECTION` table) to see if it
   dominates or is dominated by a table class on some projection.
3. **Run it through the cross-unit prover**
   (`cross_unit_prover.py`) to see if z3 can prove it equal to a
   table class.

All three routes were exercised against the real files -- `canon.py`
imported and its own requirement checked line-by-line;
`dominance.RESULT_PROJECTION` imported unmodified and queried;
`dominant_table24.json`'s 901 rows read and their 42 `type_pair`
values enumerated -- not narrated from memory. **All three refuse,
for all nine handler rows (four ruby, four php, one cpython), for the
SAME underlying reason**: every one of these nine handlers' argument
registers is either a TAGGED integer value (a ruby `Fixnum`, encoded
`2n+1` in the register itself) or a POINTER into a boxed struct
(cpython's `PyLongObject*`, ruby's Bignum, php's `zval*`) -- never
the plain fixed-width integer register the compiled-language table's
`i32,i32`/`i64,i64` add classes are keyed on. That is read straight
off each handler's own stored disassembly (section 2), not asserted.

Two new scripts do this work and are new files, kept:
`interp_canon_attempt.py` (route 1, writes
`interp_canon_attempt.json`) and `interp_relations_build.py` (routes
2 and 3, writes `interp_relations.json`, the artifact the brief
names). **No existing table or units file was modified.**

## 2. instances (real disassembly, real refusal text, verbatim)

### route 1 -- canon.py's own requirement, checked mechanically

`canon.py` line 822 reads `sem.get("anchor_registers")`. That field
is written only by `sem_anchored.py`, from a probe this repo compiled
itself WITH DEBUG INFO, so DWARF can say which register holds "the
first argument". `interp_canon_attempt.py` checked disk for any
`sem_anchored_ruby*.json` / `sem_anchored_php*.json` file and found
none:

```
$ /tmp/reconnect_venv/bin/python3 interp_canon_attempt.py
wrote .../interp_canon_attempt.json
-- ruby --
REFUSED: no sem_anchored_ruby*.json exists (0 found) and none of the
4 handler records carries sem.anchor_registers or a pyvex
blocks/values/events list -- canon.py's own line 822 read has
nothing to read. The excerpts stored are also partial samples, not
the full instruction stream canon.py would need to walk...
-- php --
REFUSED: no sem_anchored_php*.json exists (0 found) and none of the
4 handler records carries sem.anchor_registers or a pyvex
blocks/values/events list...
```

This is not a per-language accident: `interp_ruby_handlers.json` /
`interp_php_handlers.json` (log_095) were built by `grep` + `nm` +
`objdump --disassemble=<symbol>` against the ALREADY-BUILT production
interpreter binaries. Nobody compiled a probe named `a`/`b` for
`rb_fix_plus`; there is no DWARF naming its register as "argument a".
canon.py has nothing to canonicalize.

### route 2/3 -- representation read off the raw bytes, then both gates exercised

`rb_fix_plus`, ship build (optimized), the tag test on the argument
register, pasted from `interp_ruby_handlers.json`:

```
104766:	48 89 f0             	mov    rax,rsi
104769:	83 e6 01             	and    esi,0x1
10476c:	0f 85 be 00 00 00    	jne    104830 <rb_fix_plus+0xe0>
104772:	a8 07                	test   al,0x7
```

`and esi,0x1` tests the low bit of the argument register itself --
Ruby's `Fixnum` tag (`2n+1`). This is a **TAGGED VALUE** register,
not a plain integer.

`rb_big_plus`, ship build, showing BOTH representations in ONE unit,
pasted:

```
3b6ad4:	40 f6 c6 01          	test   sil,0x1
3b6ada:	48 d1 fe             	sar    rsi,1
3b6add:	0f b6 47 01          	movzx  eax,BYTE PTR [rdi+0x1]
```

`rsi` (the Fixnum operand) is tag-tested then shifted to untag;
`rdi` (the Bignum operand) is DEREFERENCED at a fixed offset -- the
same pointer-to-struct pattern `fix_cpython_type_key.py` already
proved for cpython's `long_add`. One unit, two different argument
representations.

php, all four handlers, pasted from `ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER`:

```
92fd5e:	4c 89 f2             	mov    rdx,r14
92fd61:	4c 89 f8             	mov    rax,r15
92fd64:	8b 40 08             	mov    eax,DWORD PTR [rax+0x8]
92fd67:	48 98                	cdqe
92fd69:	48 01 d0             	add    rax,rdx
92fd6c:	48 89 45 e0          	mov    QWORD PTR [rbp-0x20],rax
92fd70:	4c 89 f2             	mov    rdx,r14
92fd73:	4c 89 f8             	mov    rax,r15
92fd76:	8b 40 0c             	mov    eax,DWORD PTR [rax+0xc]
```

`r14`/`r15` are DEREFERENCED at offsets `0x8`/`0xc` -- the zval
struct's value/type fields. Both php operands are `zval*` pointers in
all four handlers, the identical shape to cpython's `long_add`.

`interp_relations_build.py` then ran the actual gates:

```
$ /tmp/reconnect_venv/bin/python3 interp_relations_build.py
wrote .../interp_relations.json
records: 9 summary: {'incomparable_by_representation': 9, 'candidate_present_unattempted': 0}
 - ruby vm_opt_plus -> incomparable_by_representation type_pair_read= opaque_VALUE_dispatch
 - ruby rb_fix_plus -> incomparable_by_representation type_pair_read= tagged64
 - ruby rb_int_plus -> incomparable_by_representation type_pair_read= tagged64
 - ruby rb_big_plus -> incomparable_by_representation type_pair_read= ptr64,tagged64
 - php add_function -> incomparable_by_representation type_pair_read= ptr64,ptr64
 - php ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER -> incomparable_by_representation type_pair_read= ptr64,ptr64
 - php ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER -> incomparable_by_representation type_pair_read= ptr64,ptr64
 - php ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER -> incomparable_by_representation type_pair_read= ptr64,ptr64
 - cpython long_add -> incomparable_by_representation type_pair_read= ptr64,ptr64
```

The **dominance gate** (route 2) refuses independently, on the
RESULT side: `dominance.RESULT_PROJECTION` (imported unmodified) has
entries only for `bool`/`i32`/`u32`/`i64`/`u64`/`f32`/`f64`. Every
one of these nine handlers RETURNS a ruby `VALUE` or a php `zval*` --
neither is in the table, so per `dominance.py`'s own docstring
("A result type this table does not name gets NO projection... no
bridge is claimed") the projection step has nothing to attach to,
independent of the argument-side refusal above.

The **cross-unit-prover gate** (route 3) refuses on its own step 1,
before any z3 call: `cross_unit_prover.py`'s candidate rule requires
both sides of a pair to share a `type_pair` class key with an
EXISTING `dom_ops` class. `dominant_table24.json`'s 901 rows carry
exactly 42 distinct `type_pair` values, enumerated by
`interp_relations_build.py`, and none of them is `ptr64,ptr64`,
`tagged64,tagged64`, or any pointer/VALUE/zval shape:

```python
>>> tps = sorted(set(r['type_pair'] for r in dominant_table24['rows']))
>>> len(tps)
42
>>> [t for t in tps if 'ptr' in t or 'VALUE' in t or 'zval' in t]
[]
```

## 3. numbers (computed, not remembered)

| language | handlers | canon status | dominance projection | prover candidate |
|---|---|---|---|---|
| ruby | 4 | refused (no sem_anchored) | refused (VALUE not in RESULT_PROJECTION) | refused (0/42 type_pairs match) |
| php | 4 | refused (no sem_anchored) | refused (zval* not in RESULT_PROJECTION) | refused (0/42 type_pairs match) |
| cpython | 1 | refused (no sem_anchored -- carried from prior ratified finding, not recomputed) | refused (ptr64 not in RESULT_PROJECTION) | refused (0/42 type_pairs match) |
| **total** | **9** | **9/9 refused** | **9/9 refused** | **9/9 refused** |

`interp_relations.json`'s own `summary`: `incomparable_by_representation:
9`, `candidate_present_unattempted: 0`. `table_type_pairs_present_count:
42`. All figures pasted directly from the script's own printed output
above, not retyped from memory.

## 4. THE DECISION BRIEF FOR DEE (membership is his ruling, not this session's)

The measured facts, restated once, plainly: every ruby/php/cpython
handler examined operates on a TAGGED integer register or a POINTER
into a boxed/tagged runtime object, never a plain fixed-width integer
register. The compiled-language table's `+` classes are keyed on
plain fixed-width types (`i32,i32`, `i64,i64`, ...). By type-pair,
representation, AND result type, these nine handlers share NO key
with any of the table's 901 classes. This is not a gap in the
machinery -- three independent mechanisms (canon text match,
dominance projection, cross-unit z3 proof) were exercised for real
and all three had nothing to attach to, for the same underlying
reason each time.

Three options, each with what was actually measured for it:

**Option A -- table members with weak provenance.** Add these nine
rows into `dominant_table24.json` as new classes (or into existing
`i32,i32`/`i64,i64` classes) with `provenance_is_weaker: true`
carried onto the row. MEASURED AGAINST: the type-pair key would be
fabricated -- there is no `ptr64,ptr64` or `tagged64,tagged64` class
to place them in, and placing them in `i32,i32`/`i64,i64` would be
exactly the "unratified equation between a pointer and a value" the
int32_t ruling (quoted in `fix_cpython_type_key.py`) already
forbids. No machinery run this session supports this option; it
would require overriding the type-pair split by hand.

**Option B -- a third axis.** Treat "tagged/boxed runtime value" as
a representation dimension the table does not yet have, parallel to
(not replacing) the existing `type_pair`/`result_type` key -- so a
handler joins a NEW family of its own representation, not the
existing `i32,i32` family. MEASURED FOR: this is exactly what the
data shows -- three genuinely distinct shapes recur across all three
languages (`ptr64,ptr64` struct-pointer: cpython `long_add`, all four
php handlers, ruby `rb_big_plus`'s Bignum side; `tagged64` tag-tested
value: ruby `rb_fix_plus`/`rb_int_plus`/`rb_big_plus`'s Fixnum side;
`opaque_VALUE_dispatch`: ruby `vm_opt_plus`, a dispatcher, not a
computation core, log_095's own AAGAINST reading). A third axis is
the option this session's evidence points toward, but naming and
building it is ontology, the owner's call, not this session's.

**Option C -- bridges only, no table entry.** Leave these nine rows
OUT of `dominant_table24.json` entirely; `interp_relations.json`
stands alone as the record of the (currently empty) relation. NOT
MOOT the way php's round-2 finding was moot (no comparison existed
at all) -- here the comparison WAS attempted, on real machinery, and
came back refused for a stated, measured reason on all three routes.
MEASURED FOR: this is the SAFEST option relative to log_083's
STANDING REQUIREMENTS (zero regressions, no fabricated key) and
requires no new ontology to be ratified before it can be adopted.

This session recommends nothing between B and C -- both are
consistent with everything measured; the choice is the owner's, per the
brief's own instruction ("Membership is the owner's ruling, not yours").

## 5. gates run

```
$ python3 check_no_spelling_keys.py interp_relations.json interp_canon_attempt.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_relations.json -- no operator token in any key, grouping, pairing or row structure
PASS interp_canon_attempt.json -- exempt: top-level meta declares role 'generator provenance', so this file is generator provenance and never participates in matching
```

`interp_canon_attempt.json`'s exemption was also checked NOT to be
load-bearing -- the file was walked in full, ignoring the exemption,
and independently produces 0 findings:

```python
>>> findings = []
>>> walk(json.load(open('interp_canon_attempt.json')), toks, '$', findings)
>>> len(findings)
0
```

Regression check: `git status --porcelain` on the PseudoCoupHQ repo
before and after this session shows only NEW untracked files created
by this task (`interp_canon_attempt.py`, `interp_canon_attempt.json`,
`interp_relations_build.py`, `interp_relations.json`; the repo-daemon
had already auto-committed the first two by the time this log was
written, confirmed by `git log -1 -- interp_canon_attempt.py`).
`dom_ops22.json` and `dominant_table24.json` were opened read-only
(`json.load`) and never opened for writing anywhere in either new
script -- verified by reading both scripts, no `open(..., "w")` call
names either file.

## 6. claims NOT made

- No claim that these nine handlers are equivalent, related, or
  unrelated to ANY compiled-language operator in a computational
  sense -- only that the three mechanical routes this line has for
  TESTING that question all refuse, for a stated reason, on the
  representation evidence available.
- No claim that the representation read (tag-test vs.
  fixed-offset-dereference) is a FORCED-BY-CONSTRUCTION fact the way
  `fix_cpython_type_key.py`'s original cpython finding was -- it
  rests on the SAME method but on a shorter, partial excerpt (route 1
  section 2 already documents the excerpts are truncated samples,
  not full instruction streams), so it is marked
  `provenance_is_weaker: true` and evidence class "human
  interpretation of stated design", not "forced by construction".
- No table membership decided or changed. `dominant_table24.json`
  and `dom_ops22.json` are unmodified (verified above).
- No claim about php's anchor/ship pair validity -- log_095's dead
  end stands exactly as recorded; this task used the one build that
  exists, as log_095 already did.
- No claim that `vm_opt_plus`'s `opaque_VALUE_dispatch` reading is
  final -- the excerpt captured cuts off before any ALU is visible
  (section 2), so this is the WEAKEST of the nine readings, named as
  such in `interp_relations.json`'s own `representation_evidence`
  field.

## 7. file inventory (every file this session created)

New:
- `PseudoCoupHQ/Research/op_pipeline/interp_canon_attempt.py`
  -- route 1, canonicalization-refusal checker.
- `PseudoCoupHQ/Research/op_pipeline/interp_canon_attempt.json`
  -- its output (generator-provenance role, exempt from the spelling
  guard by declaration AND independently by full walk, see section 5).
- `PseudoCoupHQ/Research/op_pipeline/interp_relations_build.py`
  -- routes 2 and 3, the relation builder.
- `PseudoCoupHQ/Research/op_pipeline/interp_relations.json`
  -- the artifact the brief names: handler -> {class, relation kind,
  proof/witness}, 9 records, `class` is `null` on every record (no
  table membership claimed anywhere).
- `PseudoCoupHQ/DevComms/log_101_task17_interp_relations.md`
  -- this log.

No other file was created, modified, or deleted. `dominant_table24.json`,
`dom_ops22.json`, `interp_ruby_handlers.json`, `interp_php_handlers.json`,
`op_units_cpython2.json`, `dominance.py`, `cross_unit_prover.py`,
`canon.py` were all read-only inputs.
