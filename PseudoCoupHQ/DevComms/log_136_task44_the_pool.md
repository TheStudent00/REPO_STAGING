# log 136 — TASK 44: THE MERGED POOL

Date: 2026-09-02. Author: Claude Code (implementer), no sub-agents.
Working directory: `PseudoCoupHQ/Research/op_pipeline`.
Python: the session's `/tmp/reconnect_venv/bin/python3` was cleared out
from under this task by a `/tmp` reset partway through; the three
programs written here import nothing outside the standard library, so
they were re-run end to end under `~/anaconda3/bin/python3`
(Python 3.13.9) and produced the same artifacts. Every transcript
below is from that re-run.

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

# 1. What was done, in plain words, before any figure

The line had been keeping several tables at once: a compiled table, an
interpreter table, and a join between them. the owner's correction, verbatim:

> there is a pool of all the arch-units we canonicalized and merged
> them when they are equivalent. not an accounting of every languages
> contribution to the number of units.

So there is now one pool and nothing else. Every unit TASK 43 proved
went into it — the original corpus's 1,752, the interpreter and JIT
units' 9, and the regenerated population's 27,223, which is 28,984
units. Units that were proved to compute the same thing were collapsed
into a single entry. An entry is ONE DISTINCT COMPUTATION. It carries
its member units, and each member carries its own language, its own
arrival annotation and the population it arrived from — as columns on
the member, not as a partition of the pool.

The pool holds 5,548 entries. 663 of them have members in more than
one language. Three of them have members on both sides of the
compiled/interpreted line, and the one the acceptance rests on holds
CPython's addition fast path and c's `op_109` as two members of the
same entry, printed in full in §4.

The compiled-only table and the interpreter-only table have stopped
being objects this line depends on. `dominant_table25.json` and
`dom_ops23.json` are still on disk, byte for byte, as the superseded
record; §7 recomputes their headline figures by FILTERING the pool,
which is now the only way anyone gets one.

---

# 2. The pool, with units moving into it

## 2.1 The names, each introduced before it is used

- **A unit** — one arch-unit: a piece of real machine code extracted
  from a real compiler's or interpreter's output, with a recorded
  entry contract.
- **The universal form** — TASK 43's `region36` form (log_135): the
  unit rewritten so every value lives in a typed block of one ruled
  virtual memory region, loaded out of its block at the start and
  stored into the result block at the end, with the scratch registers
  chosen by one fixed rule rather than by the original compiler.
- **The universal text** — the finished text of that form, one string
  per unit. This is the machine form the merge reads.
- **An entry** — one distinct computation: a set of units the pool has
  proved to be the same computation.
- **A member** — one unit inside an entry, carrying its language, its
  arrival annotation and its population as fields of its own.

## 2.2 The two ways two units join, and nothing else

- **Text identity.** The two units' universal texts are the same
  string, character for character. This is a machine form, not a
  token: it is what the unit's code became after the form removed the
  compiler's own idiosyncrasies.
- **A proved edge.** Some earlier proof established the two units
  equal. Five artifacts carry those, and every one of them is read
  read-only here:
  `proved_edges.json`, `proved_edges2.json`, `proved_edges3.json`
  (the cross-unit prover's pairs whose verdict is `PROVED`),
  `interp_join3.json` (its `PROVED_EQUAL` relations and its proved
  interpreter-to-interpreter edge), and `interp_fastpath.json` (the
  fast-path proof).
- **Closed under transitivity.** If a joins b and b joins c, all three
  are one entry. That is what puts CPython, php, ruby and five
  compiled languages in one entry in §4 rather than in three.

## 2.3 The merge with values moving through it

Take four units and watch them arrive.

- `c/op_109` is c's 64-bit integer addition. Its universal text:

```
mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax;
mov %r11,%rcx; add %rcx,%rax; mov %rax,0x200(%r15); ret
```

- `go/op_319` arrives from a different compiler and a different
  language. Its universal text is the SAME 108 characters. The two
  are one entry by text identity. No token was consulted to notice
  it; the strings were compared.
- `php/add_function` arrives from a running interpreter. Its
  universal text differs by one instruction — it adds straight into
  `%rax` instead of routing through `%rcx`:

```
mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax;
add %r11,%rax; mov %rax,0x200(%r15); ret
```

  so text identity does NOT join it to `c/op_109`. It joins to
  `php/ZEND_ADD_LONG_SPEC_...` and to `ruby/rb_int_plus` by text
  identity instead.
- `ruby/rb_fix_plus` is joined to `c/op_109` by a proved edge — z3
  proved the two equal bit for bit (TASK 27, log_113) — and to
  `ruby/rb_int_plus` by the interpreter join's own proved edge. So
  transitivity pulls the php chain in as well, and all of it lands in
  ONE entry with eighteen members across seven languages.

## 2.4 The counts the merge produced

```
$ python3 build_the_pool1.py
-- intake
   units in the pool 28984
   by arrival population {"interpreter": 9, "original": 1752, "regenerated": 27223}
-- the merge
   distinct universal texts 5572
   proved edges applied 118
   entries 5548
   texts measured in bytes of machine code 44
-- wrote the_pool1.json
{
 "distinct_universal_texts": 5572,
 "entries": 5548,
 "entries_spanning_compiled_and_interpreted": 3,
 "entries_spanning_more_than_one_language": 663,
 "entries_with_more_than_one_universal_text": 20,
 "proved_edges_applied": 118,
 "text_identity_merges": 23412,
 "units_by_arrival_population": {
  "interpreter": 9,
  "original": 1752,
  "regenerated": 27223
 },
 "units_in_the_pool": 28984
}
```

- **28,984 units become 5,548 entries.** 23,412 of the collapses are
  text identity; the 118 proved edges then merge 5,572 distinct texts
  down to 5,548 entries, which is 24 further collapses across texts
  that are NOT identical.
- **20 entries carry more than one universal text.** Those are exactly
  the entries a proved edge built: an entry with one text needed no
  edge. Each is listed in §5.3.

## 2.5 The representative

- THE REPRESENTATIVE RULE names each entry: the simplest member,
  fewest bytes of machine code, ties broken by first-in-list order.
- Every member of a text-identical group assembles to the same bytes,
  so the byte count only ever has to decide something inside those 20
  multi-text entries. The 44 texts those entries carry were assembled
  with `as` and their bytes counted from `objdump` — real machine-code
  bytes, not a proxy. All 44 assembled; no fall-back was used
  anywhere in the pool.
- The first-in-list order is stated in the artifact's `meta`: the
  originals in the corpus's own language order and numeric unit order,
  then the interpreter units, then the regenerated population.

---

# 3. What the pool is NOT, said plainly rather than implied

- There is no compiled table in `the_pool1.json` and no interpreter
  table. `population` is a field on a member. An entry's
  `arrival_populations` is DERIVED from its members and is a
  description, never a grouping.
- Nothing in the merge read an operator token. The merge key is the
  machine text or a proved edge; the token rides on the member as its
  `operator` display label and is read by nothing. The guard in §6
  confirms this mechanically and with no exemption claimed.
- The pool does not re-prove anything. Every join in it was proved by
  TASK 43 or by an earlier task, and every cross-language join names
  the artifact and the wording of the proof that made it.

---

# 4. The acceptance instance — the CPython/c entry, verbatim

The brief asks for this entry printed verbatim. What follows is
`E00033` from `the_pool1.json`, unedited except that the fifteen
further `PROVED_EQUAL` grounds of the same shape are elided by name
after the first two (the file carries all twenty).

```
{
 "arrival_populations": ["interpreter", "original"],
 "distinct_universal_text_count": 3,
 "entry_id": "E00033",
 "language_count": 7,
 "languages": ["c", "cpp", "cpython", "go", "php", "ruby", "rust"],
 "member_count": 18,
 "representative": "php/add_function",
 "representative_size": 21,
 "representative_size_measured_as": "bytes of machine code, assembled with `as` and counted from objdump",
 "representative_rule": "the simplest member -- fewest bytes of machine code, ties broken by first-in-list order",
 "spans_compiled_and_interpreted": true,
 "spans_more_than_one_language": true,
 "type_key": "general,general|64",
 "members": [
  {"unit": "c/op_109",   "lang": "c",   "operator": "+", "population": "original",
   "arrival_annotation": "plain", "region_base": "%r15", "result_block": "0x200(%r15)",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; mov %r11,%rcx; add %rcx,%rax; mov %rax,0x200(%r15); ret"},
  {"unit": "c/op_110",   "lang": "c",   "operator": "+", "population": "original", ... same text ...},
  {"unit": "c/op_115",   "lang": "c",   "operator": "+", "population": "original", ... same text ...},
  {"unit": "c/op_116",   "lang": "c",   "operator": "+", "population": "original", ... same text ...},
  {"unit": "cpp/op_109", "lang": "cpp", "operator": "+", "population": "original", ... same text ...},
  {"unit": "cpp/op_110", "lang": "cpp", "operator": "+", "population": "original", ... same text ...},
  {"unit": "cpp/op_115", "lang": "cpp", "operator": "+", "population": "original", ... same text ...},
  {"unit": "cpp/op_116", "lang": "cpp", "operator": "+", "population": "original", ... same text ...},
  {"unit": "go/op_319",  "lang": "go",  "operator": "+", "population": "original", ... same text ...},
  {"unit": "go/op_326",  "lang": "go",  "operator": "+", "population": "original", ... same text ...},
  {"unit": "rust/op_541","lang": "rust","operator": "+", "population": "original", ... same text ...},
  {"unit": "rust/op_548","lang": "rust","operator": "+", "population": "original", ... same text ...},
  {"unit": "cpython/long_add_fastpath", "lang": "cpython", "operator": "+",
   "population": "interpreter", "arrival_annotation": "typed-pointer(PyLongObject*)",
   "region_base": "%r15", "result_block": "0x200(%r15)",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; mov %r11,%rcx; add %rcx,%rax; mov %rax,0x200(%r15); ret"},
  {"unit": "php/ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER", "lang": "php", "operator": "+",
   "population": "interpreter", "arrival_annotation": "typed-pointer(zval*)",
   "universal_text": "... mov %r11,%rcx; add %rcx,%rax; ..." (the same text as c/op_109)},
  {"unit": "php/ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER", "lang": "php", "operator": "+",
   "population": "interpreter", "arrival_annotation": "typed-pointer(zval*)",
   "universal_text": "... the same text as c/op_109 ..."},
  {"unit": "php/add_function", "lang": "php", "operator": "+",
   "population": "interpreter", "arrival_annotation": "typed-pointer(zval*)",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; add %r11,%rax; mov %rax,0x200(%r15); ret"},
  {"unit": "ruby/rb_fix_plus", "lang": "ruby", "operator": "+",
   "population": "interpreter", "arrival_annotation": "tagged-value(Fixnum, 2n+1 encoding)",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r11,%rax; add %r10,%rax; mov %rax,0x200(%r15); ret"},
  {"unit": "ruby/rb_int_plus", "lang": "ruby", "operator": "+",
   "population": "interpreter", "arrival_annotation": "tagged-value(Fixnum, 2n+1 encoding)",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; add %r11,%rax; mov %rax,0x200(%r15); ret"}
 ],
 "universal_texts": [
  "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; mov %r11,%rcx; add %rcx,%rax; mov %rax,0x200(%r15); ret",
  "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; add %r11,%rax; mov %rax,0x200(%r15); ret",
  "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r11,%rax; add %r10,%rax; mov %rax,0x200(%r15); ret"
 ],
 "cross_language_grounds": [
  {"ground": "text identity",
   "languages_it_joins": ["c", "cpp", "cpython", "go", "php", "rust"],
   "detail": "these members carry the SAME region36 universal-form text, character for character",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; mov %r11,%rcx; add %rcx,%rax; mov %rax,0x200(%r15); ret"},
  {"ground": "text identity",
   "languages_it_joins": ["php", "ruby"],
   "detail": "these members carry the SAME region36 universal-form text, character for character",
   "universal_text": "mov 0x0(%r15),%r10; mov 0x8(%r15),%r11; mov %r10,%rax; add %r11,%rax; mov %rax,0x200(%r15); ret"},
  {"ground": "a PROVED_EQUAL relation of the interpreter join",
   "languages_it_joins": ["c", "cpython"],
   "left": "cpython/long_add_fastpath", "right": "c/op_109",
   "source_artifact": "interp_join3.json",
   "scope": "the interpreter unit's COMPUTATION part only; its arrival prefix is representation, not computation",
   "evidence": "z3 unsat through canon9_behaviour_check.Sim9, re-run by canon_interp_cpython.py (TASK 21) over the same result log_106's independent script found",
   "evidence_class": "forced by construction (the solver's unsat over a register binding derived from the unit's own recorded instruction semantics)",
   "established_by": "TASK 21 (log_107), read here read-only"},
  {"ground": "a PROVED_EQUAL relation of the interpreter join",
   "languages_it_joins": ["c", "ruby"],
   "left": "ruby/rb_fix_plus", "right": "c/op_109",
   "source_artifact": "interp_join3.json",
   "scope": "the interpreter unit's COMPUTATION part only",
   "evidence": "z3 proved bit-level equality for every value of every register either text reads before writing (fpToIEEEBV/BitVec comparison, 12000ms timeout)",
   "evidence_class": "forced by construction (solver unsat, cross_unit_prover.prove_pair)",
   "established_by": "TASK 27 (log_113), read here read-only"},
  ... fifteen further PROVED_EQUAL grounds of that same shape, joining
      ruby/rb_fix_plus and ruby/rb_int_plus to c/op_109, c/op_116,
      cpp/op_109, cpp/op_116, go/op_319, go/op_326, rust/op_541 and
      rust/op_548 ...
  {"ground": "the fast-path proof",
   "languages_it_joins": ["c", "cpython"],
   "left": "cpython/long_add_fastpath", "right": "c/op_109",
   "source_artifact": "interp_fastpath.json",
   "scope": "the fast path's COMPUTATION over the domain the unit's own bytes bound",
   "detail": "over the domain where CPython takes this fast path, is CPython's fast-path COMPUTATION (unit index 34 alone, with medium_value(a)/medium_value(b) as the symbolic inputs) the SAME function of its two inputs as c's i64 addition unit?"}
 ]
}
```

## 4.1 What this entry answers in the brief

- **The CPython fast path sits IN the same entry as `c/op_109`**, as a
  member beside it, not in a second table joined to it. Its language
  and its arrival annotation `typed-pointer(PyLongObject*)` are
  columns on that member.
- **Every merge across a language boundary names its proved ground.**
  Six of this entry's seven languages are joined by TEXT IDENTITY with
  the text printed; ruby is joined by named solver proofs; cpython is
  joined twice over, by text identity and by two independent proofs.
- **The representative is `php/add_function` at 21 bytes** — an
  interpreter unit is the simplest member of this entry, which is only
  sayable because the pool has no compiled/interpreted partition to
  stop it.

---

# 5. The pool's shape

## 5.1 By member count

```
$ python3 -c "..."   (the shape queries, transcript in §9)
== entries by member count, top 8
   E00928 539 ['c', 'cpp', 'rust', 'swift'] ['regenerated'] rep c/regen_7272
   E01364 534 ['c', 'cpp', 'rust', 'swift'] ['regenerated'] rep c/regen_15753
   E01715 534 ['c', 'cpp', 'rust', 'swift'] ['regenerated'] rep c/regen_24225
   E02705 329 ['c', 'cpp', 'rust'] ['regenerated'] rep c/regen_47459
   E00650 321 ['c', 'cpp', 'rust'] ['regenerated'] rep c/regen_1000
   E00781 321 ['c', 'cpp', 'rust'] ['regenerated'] rep c/regen_4136
   E00012 308 ['c', 'cpp', 'go', 'rust', 'swift'] ['original', 'regenerated'] rep c/op_19
   E00072 258 ['c', 'cpp', 'go', 'rust'] ['original', 'regenerated'] rep c/op_174
== size distribution
  singletons 3807 2..4 852 5..99 845 >=100 44
```

- **3,807 entries have one member.** That is the honest majority: most
  of the regenerated population's 27,223 units compute something no
  other unit in the pool computes in the same way.
- The largest entries are regenerated ones — 539 units of one
  computation — which is what a population generated by sweeping types
  over the same operator units should look like.

## 5.2 By language span

```
== entries by language count
  {1: 4885, 2: 515, 3: 70, 4: 50, 5: 27, 7: 1}
```

- **663 entries span more than one language** (515 + 70 + 50 + 27 + 1).
- **The single seven-language entry is `E00033` of §4.** No entry
  spans six, and none spans eight or nine: the interpreter units all
  concern one computation, so the cross-language reach that includes
  them concentrates in that one entry.
- **Three entries span compiled and interpreted:** `E00028` (java's
  JIT unit with c, cpp, go and rust), `E00033` (§4), and `E00097`
  (java's second unit with c and cpp, and with 128 members including
  regenerated ones).

## 5.3 The 20 entries a proved edge built

These are the entries carrying more than one universal text — the
places where the merge went beyond text identity.

```
   E00012 members 308 texts 3 [c cpp go rust swift]  cross-unit prover + text identity
   E00025 members   6 texts 2 [c cpp go rust swift]  cross-unit prover + text identity
   E00033 members  18 texts 3 [c cpp cpython go php ruby rust]
                                    interpreter join + fast-path proof + text identity
   E00072 members 258 texts 2 [c cpp go rust]        cross-unit prover + text identity
   E00213 members   5 texts 2 [c cpp go rust swift]  cross-unit prover + text identity
   E00219 members   5 texts 2 [c cpp go rust swift]  cross-unit prover + text identity
   E00237 members   6 texts 2 [c cpp go rust swift]  cross-unit prover + text identity
   E00243 members   6 texts 2 [c cpp go rust swift]  cross-unit prover + text identity
   E00414 members   6 texts 2 [cpp go rust swift]    cross-unit prover + text identity
   E00415 members   3 texts 2 [cpp swift]            cross-unit prover
   E00416 members   3 texts 2 [cpp swift]            cross-unit prover
   E00417 members  10 texts 2 [cpp go rust swift]    cross-unit prover + text identity
   E00421 members   9 texts 2 [cpp go rust swift]    cross-unit prover + text identity
   E00422 members   5 texts 2 [cpp swift]            cross-unit prover
   E00423 members   5 texts 2 [cpp swift]            cross-unit prover
   E00424 members  14 texts 2 [cpp go rust swift]    cross-unit prover + text identity
   E00427 members 119 texts 3 [cpp go rust swift]    cross-unit prover + text identity
   E00445 members  87 texts 2 [cpp go rust swift]    cross-unit prover + text identity
   E00464 members 119 texts 3 [cpp go rust swift]    cross-unit prover + text identity
   E00482 members  87 texts 2 [cpp go rust swift]    cross-unit prover + text identity
```

- Every one of the twenty is cross-language. A proved edge that joined
  two units of the same language would have merged texts inside one
  language; none did.

---

# 6. The guards

## 6.1 The spelling-key check on both artifacts, no exemption claimed

Both files carry a top-level `rows`-shaped grouping field (`entries`,
`families`) and neither declares the generator-provenance role, so the
checker walks them IN FULL.

```
$ python3 check_no_spelling_keys.py the_pool1.json the_families1.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS the_pool1.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families1.json -- no operator token in any key, grouping, pairing or row structure
EXIT=0
```

- The token appears in `the_pool1.json` exactly once per member, in
  the member's `operator` field, on an object that carries a language
  and a unit id — the one place the ban allows it. In
  `the_families1.json` it appears exactly once per node, in the node's
  `label` field, on an object that carries a language and a node id.
- Nothing keyed, grouped, paired or selected reads it. Stated as a
  mechanism rather than a promise: the pool's merge key is
  `universal_text` or a proved-edge endpoint pair; the families'
  pairing scope is entry co-membership; the families' edge weights are
  a count of shared entries and a count of shared machine-form shape
  keys; the tie-break is machine-form quantities only, imported from
  `dom_ops.rank_key` unchanged.

## 6.2 Zero regression — every prior artifact untouched

`canon36_zero_regression.json` records the sha256 of fifteen watched
artifacts. Every one was recomputed from disk after this task's work:

```
sha records found: 15
  SAME  canon35_universal_c.json
  SAME  canon35_universal_cpp.json
  SAME  canon35_universal_go.json
  SAME  canon35_universal_rust.json
  SAME  canon35_universal_swift.json
  SAME  dom_ops22.json
  SAME  dom_ops23.json
  SAME  dominant_table24.json
  SAME  dominant_table25.json
  SAME  interp_canon35.json
  SAME  interp_join2.json
  SAME  interp_join3.json
  SAME  interp_table2.json
  SAME  union_table2.json
  SAME  union_table3.json
```

```
$ git status --porcelain Research/op_pipeline
?? Research/op_pipeline/the_pool1.json
```

- **`dominant_table25.json` and `dom_ops23.json` are unchanged on
  disk.** They cease to exist as objects the line depends on; they do
  not cease to exist as records.
- The only line `git status` shows is this task's own new pool file,
  waiting for the daemon's next cycle; the daemon had already
  committed the three programs and `the_families1.json` (`f83ebdb`,
  `fe4d2e6`). **New files only, throughout.**

---

# 7. The families, and the continuity figures

## 7.1 The rule, imported rather than restated

THE DOM_OP CONSTRUCTION RULE is applied unchanged: nodes are
(language, grammar-operator, arity) — the provenance of a probe inside
ONE language; edges only BETWEEN languages, weighted by shared
equivalence-class count; each node keeps its single strongest
counterpart per foreign language, kept only when MUTUAL; connected
components of the mutual-best graph are the families.

- `build_the_families1.py` IMPORTS `dom_ops.build_nodes`,
  `fill_nodes`, `build_edges`, `best_per_language`, `mutual_edges` and
  `components` rather than restating them, so the rule cannot drift
  here.
- The only thing that changed is WHAT THE CLASSES ARE: the equivalence
  classes are now the pool's entries, over every language in the pool,
  rather than the compiled-only table's rows.
- The arity is read off the unit's own entry contract — does a second
  arriving lineage exist — by `dom_ops_0branch.arity_bucket_of`,
  imported unchanged. That is machine form over asserted form; it is
  the same function round 8's node set used, so node identity is like
  for like across the two rounds; and it is the only arity source
  EVERY population in the pool carries, since no probe manifest
  describes an interpreter unit.

## 7.2 The families over the whole pool

```
$ python3 build_the_families1.py
-- reading the pool
   pool entries 5548, pool units 28984
-- nodes (language, grammar-operator, arity) 190
-- cross-language edges, raw 544
-- edges surviving the mutual filter 244
-- families 31
{
 "edges_mutual": 244,
 "edges_raw": 544,
 "entry_count": 5548,
 "equally_strongest_ties": 61,
 "families": 31,
 "nodes": 190,
 "nodes_in_a_family": 145,
 "nodes_with_no_surviving_edge": 45,
 "singleton_families": 0
}
```

- **31 families, none of them a singleton.** 145 of the 190 nodes sit
  in one; 45 have no surviving mutual-best edge and are named
  individually in `the_families1.json`'s `unattached_nodes`.

## 7.3 The result the compiled-only table could not produce

`F0001` has NINE nodes in NINE languages, and it is the first family
in the file:

```
F0001 size 9 ['c', 'cpp', 'cpython', 'go', 'java', 'php', 'ruby', 'rust', 'swift']
     c:+(binary) cpp:+(binary) cpython:+(binary) go:+(binary) java:+(binary)
     php:+(binary) ruby:+(binary) rust:+(binary) swift:+(binary)
```

- Four of those nine languages are interpreted or JIT-compiled. They
  are in the family because their units share pool entries with the
  compiled ones — the mechanism is entry co-membership, and no token
  took part. A compiled-only table could not have produced this
  family at all; the merge is what made it available.
- The ratified sighting survives the change, which is the check that
  the rule was not quietly altered. `F0009` is still the bitwise-not
  family across five different spellings:

```
F0009 size 6 ['c', 'cpp', 'go', 'rust', 'swift']
     c:~(unary) cpp:compl(unary) cpp:~(unary) go:^(unary) rust:!(unary) swift:~(unary)
```

- `F0004` is the division family, and java's JIT unit joins it beside
  c, cpp, go, rust and swift.

## 7.4 The original-1,779 subset, DERIVED by filtering the pool

The brief asks for the original corpus's figures beside the pool's,
for continuity with round 8's 898 / 137 / 26 / 20. There is no second
table: `the_pool1_original_subset.py` FILTERS the pool — it keeps only
members whose `population` field reads `original`, drops an entry left
with no such member, and runs the same imported rule over what is
left. Nothing is re-grouped; members are hidden, and the merge that
already happened over the whole pool stands.

```
$ python3 the_pool1_original_subset.py
== the whole pool, no filter
{"edges_mutual": 244, "edges_raw": 544, "entries": 5548, "families": 31,
 "member_units": 28984, "nodes": 190, "nodes_in_a_family": 145,
 "nodes_with_no_surviving_edge": 45}
== filtered to members whose population reads 'original'
{"edges_mutual": 205, "edges_raw": 391, "entries": 604, "families": 26,
 "member_units": 1752, "nodes": 140, "nodes_in_a_family": 119,
 "nodes_with_no_surviving_edge": 21}
== round 8's compiled-only figures, for continuity
{"class_count": 898, "dom_op_count": 26, "nodes": 137,
 "nodes_with_no_surviving_edge": 20}
```

| figure | round 8, compiled-only | the pool, filtered to `original` |
| --- | --- | --- |
| units covered | 1,639 | 1,752 |
| classes / entries | 898 | 604 |
| nodes | 137 | 140 |
| families | 26 | 26 |
| nodes with no surviving edge | 20 | 21 |

- **Families: 26 and 26.** The number is unchanged, which is the
  continuity the brief asked for.
- **Units: 1,639 against 1,752, a difference of 113.** Verified by
  set difference rather than asserted: every one of `dominant_table25`'s
  units is in the pool (`table-only 0`), and the pool carries 113 more.
  Those 113 are the units round 8's table left out — its branching
  units and the address-of units TASK 43 rescued.
- **Nodes: 137 against 140.** Recomputing round 8's node set from its
  own rows with THIS task's arity function reproduces 137 exactly, so
  the comparison is like for like, and the difference is exactly three
  node identities, each carried only by units the round-8 table did
  not hold:

```
round8 table nodes (same arity function) 137   pool-original nodes 140
IN POOL NOT IN ROUND8 TABLE:
   ('rust', '%', 'binary')    carried only by rust/op_678, rust/op_685, rust/op_692
   ('swift', '...', 'binary') carried only by swift/op_906, swift/op_913, swift/op_920,
                                              swift/op_927, swift/op_934
   ('swift', '..<', 'binary') carried only by swift/op_870, swift/op_877, swift/op_884,
                                              swift/op_891, swift/op_898
IN ROUND8 NOT IN POOL: []
```

- **Entries: 604 against 898 classes.** This is not a like-for-like
  count and is not reported as one. Round 8's class key was (operand-type
  key, result family, representative text); a pool entry's merge key is
  the machine text or a proved edge ALONE. Dropping the type and result
  components merges classes that carried the same text with different
  operand types. The direction of the difference is therefore expected.

## 7.5 The finding inside that comparison: two round-8 classes SPLIT

Checked rather than assumed — every round-8 class was traced to the
pool entries its units landed in:

```
round8 classes covered 898 of which split across pool entries 2
  C0499 -> ['E00125', 'E00524', 'E00565']
      E00125 ['c/op_246', 'cpp/op_246']
      E00524 ['go/op_132']
      E00565 ['swift/op_186']
  C0500 -> ['E00097', 'E00521', 'E00562']
      E00097 ['c/op_210', 'cpp/op_210']
      E00521 ['go/op_96']
      E00562 ['swift/op_150']
```

- Both are integer division. The c and cpp members' texts are a bare
  `idiv`. The go members' texts carry go's own divide-by-zero guard
  and its overflow special case (`call runtime.panicdivide`); the
  swift members' carry swift's (`ud2`). Those are different
  computations — one traps, one panics, one does neither — and the
  pool separates them where round 8's representative substitution had
  put them in one class.
- This is a correction, not a regression: the pool says three things
  where the earlier table said one, and each of the three is what the
  machine actually does.

---

# 8. Every file, named

## 8.1 Written by this task (new files only)

| file | what it is |
| --- | --- |
| `Research/op_pipeline/build_the_pool1.py` | builds the pool: intake of all three populations, the text-identity and proved-edge merge with transitive closure, the representative rule with real assembled byte counts |
| `Research/op_pipeline/the_pool1.json` | THE POOL — 5,548 entries over 28,984 member units, 18.6 MB |
| `Research/op_pipeline/build_the_families1.py` | the dom_op construction rule over the pool, importing `dom_ops` and `dom_ops_0branch` unchanged |
| `Research/op_pipeline/the_families1.json` | the 31 families, the 45 unattached nodes, the 61 equally-strongest ties |
| `Research/op_pipeline/the_pool1_original_subset.py` | the continuity filter: derives the original-corpus figures FROM the pool, so no second table exists |
| `DevComms/log_136_task44_the_pool.md` | this report |
| `Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md` | appended a dated entry under the single `# PROGRESS` heading (edited, not created) |

## 8.2 Read by this task, read-only, none modified

- `canon36_universal_c.json`, `canon36_universal_cpp.json`,
  `canon36_universal_go.json`, `canon36_universal_rust.json`,
  `canon36_universal_swift.json` — the original corpus's 1,752 proved
  units.
- `canon36_interp.json` — the interpreter and JIT population's 9
  proved units.
- `canon36_regen_store/*.json` (326 files) — the regenerated
  population's 27,223 proved units.
- `proved_edges.json`, `proved_edges2.json`, `proved_edges3.json`,
  `interp_join3.json`, `interp_fastpath.json` — the proved edges.
- `dominant_table25.json`, `dom_ops23.json` — round 8's compiled-only
  table and families, read for the §7.4 continuity comparison only.
- `canon36_zero_regression.json` — the fifteen watched sha256 records.
- `probe_manifest_*.json` — read by the guard for its token inventory.
- `dom_ops.py`, `dom_ops_0branch.py`, `check_no_spelling_keys.py` —
  imported or run, unmodified.

---

# 9. The evidence class of each claim in this report

- **Forced by construction over artifacts this task built:** the entry
  count, the member counts, the language spans, the compiled/interpreted
  spans, the family count, the node count, the subset figures. Each is
  a count over a file on disk, printed by the program that wrote it.
- **Measured with a tool:** the representative byte counts (`as` plus
  `objdump` over 44 texts), the sha256 comparisons, the `git status`
  line.
- **Inherited testimony, weaker than the above, and carried with its
  own wording:** every proved edge. The pool re-proves nothing. Each
  cross-language ground in the artifact carries the source artifact,
  the scope, the evidence sentence and the task that established it,
  copied rather than paraphrased — including the two scope
  restrictions that matter, "the interpreter unit's COMPUTATION part
  only" and the fast path's domain bound.
- **This task's own judgment, named as such:** that a pool entry's
  `type_key` — which register file each arriving lineage loads
  through, and how wide the answer is — is the right machine-form
  stand-in for the compiled table's operand-type key in the families'
  second edge weight. It is read off each unit's own block directory
  and no token enters it, but the choice of that quantity is this
  task's, and it is stated on the artifact's `meta` so it can be
  struck.
