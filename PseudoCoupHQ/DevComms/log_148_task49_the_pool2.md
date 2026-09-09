# log 148 — TASK 49: the pool rebuilt on the wrapped form

Date: 2026-09-02. Author: Claude Code (implementer), no sub-agents.
Working directory: `~/Programming/PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3`. Assembly on the host:
`as --64`, `objdump -d`.

Every rendering below is labelled **LITERAL**, **GLOSS** or
**ANALOGY**, per the protocol's §5.1a. A gloss never appears without
the literal it glosses. Every figure states its population, per §3.4a.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
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
line MUST paste this paragraph verbatim."

---

# 1. What was done, and where it stands

## 1.1 In plain words, before any figure

The pool was rebuilt. It now holds every arch-unit TASK 47 proved in
the memory-wrapped form — 30,436 units of the 31,078 attempted — and
it merges two units into one entry on three grounds and nothing else:
their layer-5 normalized texts are the same string; or their layer-3
wrapped texts are the same string; or an earlier proof established
them equal. The joins are closed under transitivity. Language,
arrival annotation and population ride on the members as columns, so
there is still no compiled table and no interpreter table anywhere in
the artifact.

The new ground is layer 5. TASK 48 built a term for each unit off its
provenance ledger, proved that term equal to the unit's own machine
code, and normalized the printed term so no register name survives.
Two compilers that write integer addition with different
instructions and different argument registers now print one string,
`v0 + v1`, and the pool joins them on it. That is what "rebuilt on the
wrapped form" bought: 22,282 of the merges in this pool are layer-5
merges, and they reach across languages in a way the instruction text
alone does not.

## 1.2 The counts, per population

LITERAL — `acceptance49_printed.txt`, section (a):

```
    quantity                              pool1      pool2
    member units                              28984      30436
    entries                                    5548       5274
    entries spanning more than one language      663        423
    entries spanning compiled and interpreted        3          3
    families                                     31         35
    family nodes                                190        197
    nodes in a family                           145        161
    singleton families                            0          0
```

- **The population, stated on the artifact.** `the_pool2.json`'s
  `meta.population` reads: "every unit TASK 47 (log_146) proved:
  30,436 of 31,078 attempted — original 1,763, interpreter 9,
  regenerated 28,664". The summary block carries the same split as
  measured data.
- **Multi-language fell from 663 to 423, and that is consolidation,
  not loss.** §5 computes where all 663 went; no join was lost.
- **The families grew from 31 to 35** over 197 nodes, and none is a
  singleton. §6 prints all 35.

## 1.3 The 826 withdrawals — carried, and flagged

The brief asks which, so it is answered before anything rests on it.

- **They are CARRIED in the pool as members.** They are units TASK 47
  proved; removing them would misstate the population, and the
  authoritative count line is 30,436.
- **They are EXCLUDED from merging by layer-5 text.** Their layer-4
  term was DISPROVED by z3 against their own machine code. THE
  REPRESENTATIVE RULE names the simplest member of a group that has
  been PROVED equivalent; a refuted term is not proof of anything, so
  it may not join two units.
- **They remain reachable by the other two grounds**, because neither
  rests on the term: layer-3 text identity is the same machine code
  twice, and a proved edge was established elsewhere.
- **The flag is a field on each member**, so nothing about this is
  implicit.

LITERAL — one such member, as stored in `the_pool2.json`
(`go/op_174`, printed from the artifact):

```
"layer5_merge_eligible": false,
"layer5_merge_eligibility_reason": "the layer-4 term was undecided on
    both routes, so the layer-5 text is not proved equivalence"
```

- The same treatment, and the same field, covers every unit with no
  proved layer-5 text: **7,022 of the 30,436**, made of 4,142 with no
  term built, 826 withdrawn, and 2,054 undecided on both routes.
  Those three numbers are TASK 48's own, recomputed here from the
  `layer4b_*` artifacts rather than copied from log 147.

## 1.4 One departure from the brief's letter, declared

- The brief names two grounds: layer-5 text identity and proved
  edges. This pool applies a third — **layer-3 wrapped-text
  identity**.
- The reason: pool1's own merge ground was text identity at its own
  layer (the region36 universal text). Dropping it would put two
  character-identical instruction sequences into two entries, which
  is not a rebuild but a loss. Layer-3 identity is not an inference
  from a term; it is the same machine code twice.
- **The brief-strict number is computed and stated anyway**, so
  nothing is hidden by the choice: under layer-5 identity and proved
  edges alone the pool has **8,140 entries** instead of 5,274. That
  figure is on the artifact as
  `summary.entries_under_the_brief_strict_rule`, and
  `build_the_pool2.build_pool` computes it from the same code path
  with one switch.

---

# 2. The merge, with values moving through it

## 2.1 The names, each introduced before it is used

- **A unit** — one arch-unit: real machine code from a real compiler
  or interpreter, with a recorded arrival contract.
- **The wrapped form (layer 3)** — TASK 47's form: a standardized
  prelude loads each argument out of a memory row into the register
  the compiler expects, the compiler's own body follows verbatim, a
  standardized epilogue stores the answer into row `OUT-0`.
- **The wrapped text** — that form printed as one string. This is the
  runnable record.
- **The provenance ledger (layer 4)** — TASK 48's table beside each
  unit: one row per value, carrying its type, the arch opcode that
  produced it, and the rows it read.
- **The layer-5 normalized text** — the term transcribed from that
  ledger downward from `OUT-0`, put once through z3's simplifier,
  with its free symbols renamed positionally `v0`, `v1`, … and
  printed on one line.
- **An entry** — one distinct computation: a set of units the pool has
  proved to be the same computation.
- **A member** — one unit inside an entry, carrying its language, its
  arrival annotation and its population as fields of its own.

## 2.2 Four units arriving at one entry, with the strings shown

Take integer addition and watch four members reach the same entry by
three different grounds. All four strings below are LITERAL, quoted
from `the_pool2_entry_E00029.json`.

**`c/op_109`** — c's 64-bit integer addition.

```
mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
lea (%rdi,%rsi,1),%rax;
mov ledger+0x28(%rip),%r11; mov %rax,0x0(%r11); ret
```

**`go/op_319`** — go's, from a different compiler.

```
mov ledger+0x00(%rip),%rax; mov 0x0(%rax),%rax;
mov ledger+0x00(%rip),%rbx; mov 0x8(%rbx),%rbx;
add %rbx,%rax;
mov ledger+0x28(%rip),%r11; mov %rax,0x0(%r11); ret
```

**`php/add_function`** — from a running interpreter.

```
mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
mov %rdi,%rax; add %rsi,%rax;
mov ledger+0x28(%rip),%r11; mov %rax,0x0(%r11); ret
```

**`ruby/rb_fix_plus`** — from another running interpreter.

```
mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
mov %rsi,%rax; add %rdi,%rax;
mov ledger+0x28(%rip),%r11; mov %rax,0x0(%r11); ret
```

GLOSS, walked step by step, with the layer-3 strings above as the
material.

1. **Compare `c/op_109` with `go/op_319` at layer 3.** Character 1 of
   c's body region is `l` (`lea`); character 1 of go's is `a`
   (`add`). c loads its first argument into `%rdi`, go into `%rax`.
   The two strings differ. Layer-3 identity does NOT join them.
2. **Compare `php/add_function` with `ruby/rb_fix_plus` at layer 3.**
   php writes `mov %rdi,%rax; add %rsi,%rax`; ruby writes
   `mov %rsi,%rax; add %rdi,%rax`. The operands are swapped. Again
   the strings differ, and layer-3 identity does not join them.
3. **Now read the same four units at layer 5.** Each unit's stored
   `layer5_normalized_text` field is, for all four, the same eight
   characters:

   ```
   v0 + v1
   ```

   `v0` is the value in row `IN-0` and `v1` the value in row `IN-1`;
   the names are positional, assigned in the order the printed term
   shows them, so no register name survives. All four terms were
   proved equal to their own units' machine code by TASK 48, so every
   one of the four is eligible, and the four collapse into one entry
   on that string.
4. **A fifth join arrives from an older proof.** `interp_join3.json`
   carries a `PROVED_EQUAL` relation between `c/op_109` and
   `cpython/long_add_fastpath`, and `interp_fastpath.json` carries the
   fast-path proof. Both are applied as proved edges, and both fall
   inside the entry layer 5 had already formed — the entry now records
   them as extra grounds rather than as the ground that built it.
5. **Transitivity closes it.** The entry ends with 158 member units:
   c 68, cpp 68, rust 8, go 7, php 4, ruby 2, cpython 1 — across all
   three arrival populations, 139 regenerated, 12 original, 7
   interpreter.

## 2.3 The representative, decided by real bytes

- THE REPRESENTATIVE RULE: the simplest member — fewest bytes of
  machine code, ties broken by first-in-list order.
- Members sharing one wrapped text assemble to the same bytes, so the
  byte count only has to decide inside the **434 entries that carry
  more than one wrapped text**. Those entries hold **1,437 distinct
  texts**; every one was written to a `.s` file, assembled with
  `as --64`, and its bytes counted from `objdump -d`. All 1,437
  assembled; no fall-back stood in anywhere in the pool. The measured
  sizes are kept in `the_pool2_bytes.json`.
- For the entry in §2.2 the winner is `go/op_319` at **35 bytes** —
  go's two-instruction body plus the standardized plumbing is shorter
  than c's `lea` form once the prelude is counted, and shorter than
  either interpreter's three-instruction body.

---

# 3. THE ANSWER TO "PRINT E00033's SUCCESSOR VERBATIM"

## 3.1 The successor is `E00029`, and it is not a guess

The successor was computed, not matched by name: every member of
pool1's `E00033` was looked up in pool2 and the destinations tallied.

LITERAL — `acceptance49_printed.txt`, section (b), first four lines:

```
    the_pool1.json E00033: 18 members, 7 languages ['c', 'cpp', 'cpython', 'go', 'php', 'ruby', 'rust']
    every one of its members lands in: {"E00029": 18}
    members TASK 47 did not prove, so absent from pool2: 0 []
```

GLOSS: all 18 of pool1's members land in one pool2 entry, `E00029`,
and none was lost to a TASK 47 refusal. `E00029` then holds 140
further members that `E00033` did not.

## 3.2 The entry itself

- The complete entry is written verbatim to
  `~/Programming/PseudoCoupHQ/Research/op_pipeline/the_pool2_entry_E00029.json`
  (118,843 bytes: every field, all 158 member objects).
- `acceptance49_printed.txt` §(b) prints it in the log-readable form:
  every field except `members` pretty-printed, then all 158 stored
  member objects one per line, exactly as they sit in the file.
- The entry's own head, LITERAL, from that file:

```
 "entry_id": "E00029",
 "member_count": 158,
 "representative": "go/op_319",
 "representative_size": 35,
 "representative_size_measured_as": "bytes of machine code, assembled with `as` and counted from objdump",
 "representative_rule": "the simplest member -- fewest bytes of machine code, ties broken by first-in-list order",
 "languages": ["c","cpp","cpython","go","php","ruby","rust"],
 "language_count": 7,
 "spans_more_than_one_language": true,
 "arrival_populations": ["interpreter","original","regenerated"],
 "spans_compiled_and_interpreted": true,
 "distinct_wrapped_text_count": 12,
 "layer5_normalized_texts": ["v0 + v1"],
 "distinct_layer5_text_count": 1,
 "members_not_layer5_eligible": 0,
 "type_key": "rdi,rsi|64"
```

- **12 wrapped texts, one layer-5 text.** That single line is the
  whole point of the rebuild: twelve different instruction
  sequences, from five compilers and three interpreters, that TASK 48
  proved compute one term.
- Five member objects, LITERAL, as stored — one per language that has
  a distinct arrival annotation:

```
{"unit":"c/op_109","lang":"c","operator":"+","population":"original","arrival_annotation":"plain","layer5_normalized_text":"v0 + v1","layer5_merge_eligible":true,"out_row":"OUT-0","result_width":64, ...}
{"unit":"go/op_319","lang":"go","operator":"+","population":"original","arrival_annotation":"plain", ...}
{"unit":"cpython/long_add_fastpath","lang":"cpython","operator":"+","population":"interpreter","arrival_annotation":"typed-pointer(PyLongObject*)", ...}
{"unit":"php/add_function","lang":"php","operator":"+","population":"interpreter","arrival_annotation":"typed-pointer(zval*)", ...}
{"unit":"ruby/rb_fix_plus","lang":"ruby","operator":"+","population":"interpreter","arrival_annotation":"tagged-value(Fixnum, 2n+1 encoding)", ...}
```

  GLOSS: the `operator` field is the display label the ban permits —
  one per member, read by nothing. The `arrival_annotation` field is
  the real information here: three interpreters hand their addition
  three differently-shaped values (a `PyLongObject*`, a `zval*`, a
  tagged fixnum), and the computation underneath is one computation.

---

# 4. EVERY ENTRY THAT SPLIT OR MERGED, WITH ITS COMPUTED CAUSE

## 4.1 How the comparison was made

- The join is on MEMBER SETS. `compare_pool1_pool2.py` reads both
  pools read-only, indexes unit → entry in each, and asks two
  questions over the units present in BOTH pools.
- **SPLIT** — one pool1 entry whose shared members land in more than
  one pool2 entry. **MERGED** — one pool2 entry whose shared members
  come from more than one pool1 entry.
- The cause of each is COMPUTED from the machine forms, never
  asserted: for a merge, every crossing pair is tested against each
  of the three grounds; for a split, the parts' layer-3 texts and
  layer-5 eligibility are counted.

LITERAL — `pool1_pool2_delta_printed.txt`, the headline block:

```
== populations
   pool1 member units                       28984
   pool2 member units                       30436
   units in both, the comparable population 28378
   in pool1 only -- TASK 47 refused them    606
   in pool2 only -- newly proved this round 2058

== the join on member sets
   pool1 entries holding a shared unit       5065
   pool2 entries holding a shared unit       3851
   pool1 entries that SPLIT                  14
   pool2 entries that MERGED                 492
```

## 4.2 The 14 splits, all of them, with causes

LITERAL — `pool1_pool2_delta_printed.txt`, the split-cause tally:

```
== SPLIT causes, computed, one entry may carry more than one
       14  the members carry more than one layer-3 wrapped text, so layer-3 identity does not join them
        7  the eligible members normalize to more than one layer-5 text, so layer-5 identity does not join them
        7  2 member(s) have no eligible layer-5 text, so no layer-5 ground can reach them
```

Every one of the 14 is printed in full in `acceptance49_printed.txt`
§(c). They fall into exactly two causes, and each is walked below with
its strings.

### 4.2.1 Cause A — the two forms are different terms (7 entries)

Worked instance: pool1's `E00010`, five members, becomes pool2's
`E00010` (four members) and `E00148` (one member).

LITERAL — pool1's `E00010`, its one universal text
(`the_pool1.json`, field `universal_texts`):

```
movq 0x0(%r15),%xmm0; mov 0x40(%r15),%r11; mov %r11d,%r10d;
movd %r10d,%xmm1; xorps %xmm1,%xmm0; movq %xmm0,0x200(%r15); ret
```

LITERAL — the same five units in pool2, layer 3 then layer 5:

```
c/op_15    -> E00010
   L3: xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; mov ledger+0x28(%rip),%r11; movq %xmm0,0x0(%r11); ret
   L5: Extract(63, 0, v0) ^ Extract(63, 0, v1)
go/op_9    -> E00148
   L3: movss 0x1d5dc(%rip),%xmm1; pxor %xmm1,%xmm0; mov ledger+0x28(%rip),%r11; movq %xmm0,0x0(%r11); ret
   L5: Concat(Extract(63, 32, v0), Extract(31, 0, v0) ^ Extract(31, 0, v1))
```

GLOSS, with the difference named: c's term reads the whole 64 bits of
each input and answers the whole 64 bits. go's term touches only the
low 32 bits and CONCATENATES the untouched upper 32 bits of `v0` back
onto the answer. Those are two different functions of the same two
inputs, and no proof relates them. Pool1's region36 form had rewritten
both into one register-renamed string and merged them; the wrapped
form keeps each compiler's own instructions, and layer 5 then shows
they are not the same term. **This split is pool1's over-merge being
corrected, not a capability lost.**

### 4.2.2 Cause B — a branch label carries the unit's own name (7 entries)

Worked instance: pool1's `E00530`, two members, becomes pool2's
`E00313` and `E00316`.

LITERAL — the two wrapped texts, with the one difference marked by
reading them against each other:

```
go/op_174 -> E00313
   ... test %ebx,%ebx; jl 47a678 <main.op_174+0x18>; mov %ebx,%ecx; shl %cl,%rax; ...
go/op_180 -> E00316
   ... test %ebx,%ebx; jl 47a678 <main.op_180+0x18>; mov %ebx,%ecx; shl %cl,%rax; ...
```

LITERAL — both units' layer-5 texts, which ARE the same string:

```
~(~(v0 << Concat(0, Extract(5, 0, v1))) | ~(18446744073709551615*If(Or(Not(Extract(31, 7, v1) == 0), ULE(64, Extract(6, 0, v1))), 0, 1)))
```

LITERAL — both units' stored eligibility reason:

```
"the layer-4 term was undecided on both routes, so the layer-5 text is not proved equivalence"
```

GLOSS, the mechanism in three steps. (1) The two instruction
sequences are identical except for the text inside the angle brackets,
which is the assembler's symbolic name for the branch target and
contains the unit's own name — `main.op_174` against `main.op_180`.
(2) So layer-3 identity, which is a character comparison, does not
join them. (3) Their layer-5 texts are identical, but neither term was
proved on either route, so layer-5 identity is not allowed to join
them either. Both grounds fail for reasons that have nothing to do
with the computation, and the pool1 entry splits.

**This is a defect in the layer-3 form, and it is a flag, not
something this task fixed.** AgentMemory's canonical-form ruling
requires branch labels normalized positionally (`L0..` in address
order); the wrapped text does not do that yet. The size of the effect
was measured rather than guessed:

```
member units whose wrapped text carries a symbolic target: 4499
distinct wrapped texts as stored      : 6277
distinct after blanking <...> targets : 2999
```

GLOSS: normalizing the branch target alone would take the pool's
distinct layer-3 texts from 6,277 to 2,999. That is work for the next
lap on TASK 47's form; nothing here was changed to chase it.

## 4.3 The 492 merges, with their grounds

LITERAL — `pool1_pool2_delta_printed.txt`:

```
== MERGE grounds, computed, one entry may carry more than one
     451  layer-5 normalized-text identity
     279  layer-3 wrapped-text identity
       0  no single crossing pair -- transitive chain only
```

- **Zero merges rest on a chain with no ground on any crossing
  pair.** Every one of the 492 has at least one pair of members, from
  two different pool1 entries, joined by a ground that can be pointed
  at.
- **Layer 5 is the majority ground**, at 451 of 492. That is the
  measurable answer to what the rebuild bought.
- The largest, LITERAL, from `acceptance49_printed.txt` §(c):

```
      E00184 <- 19 pool1 entries, 114 shared members
        CAUSE: layer-3 wrapped-text identity -- 138 crossing pair(s), for instance c/op_541 with c/regen_36634
        CAUSE: layer-5 normalized-text identity -- 5769 crossing pair(s), for instance c/op_541 with c/op_649
      E00011 <- 15 pool1 entries, 386 shared members
        CAUSE: layer-3 wrapped-text identity -- 1932 crossing pair(s), for instance c/op_101 with c/op_215
        CAUSE: layer-5 normalized-text identity -- 11315 crossing pair(s), for instance c/op_101 with c/op_215
```

---

# 5. WHERE POOL1's 663 MULTI-LANGUAGE ENTRIES WENT

The figure fell from 663 to 423 and that reads like a loss, so it was
computed rather than explained away.

LITERAL — `acceptance49_printed.txt`, section (d):

```
    pool1 multi-language entries                          663
      of those, fewer than two languages survive TASK 47   43
      the rest land in this many pool2 multi-language entries  318
    pool2 multi-language entries                          423
      of those, holding no unit from a pool1 multi-language entry 105
```

- **620 of the 663 are still multi-language**, and they now sit inside
  318 pool2 entries — the 492 merges of §4.3 consolidated them.
- **43 lost comparability**, not membership: TASK 47 refused enough of
  their members that fewer than two languages survive in them. Those
  refusals are TASK 47's, listed in log 146 §8.
- **105 pool2 multi-language entries are new**, holding no unit from
  any pool1 multi-language entry.
- 318 + 105 = 423. The arithmetic closes.

LITERAL — what holds each of the 423 together, same section:

```
      180  layer-3 text identity + layer-5 text identity
      136  layer-3 text identity
       90  layer-5 text identity
       13  a proved edge of the cross-unit prover + layer-3 text identity + layer-5 text identity
        2  a proved edge of the cross-unit prover + layer-5 text identity
        1  a PROVED_EQUAL relation of the interpreter join + layer-3 text identity + layer-5 text identity
        1  a PROVED_EQUAL relation of the interpreter join + layer-3 text identity + layer-5 text identity + the fast-path proof
```

GLOSS: 90 cross-language entries exist ONLY because of layer 5 — no
character-identical instruction text and no prior proof relates their
members. Those 90 are the rebuild's own contribution to cross-language
reach.

---

# 6. THE FAMILIES

## 6.1 The rule, imported rather than restated

- THE DOM_OP CONSTRUCTION RULE is applied unchanged. Nodes are
  (language, grammar-operator, arity) — the provenance of a probe
  inside ONE language. Edges only BETWEEN languages, weighted by the
  number of pool entries in which both nodes have member units, then
  by distinct machine-form shape keys. Each node keeps its single
  strongest counterpart per foreign language, kept only when MUTUAL.
  Connected components of the mutual-best graph are the families.
- `build_the_families2.py` IMPORTS `dom_ops.build_nodes`,
  `fill_nodes`, `build_edges`, `best_per_language`, `mutual_edges` and
  `components`, and `dom_ops_0branch.arity_bucket_of`, rather than
  restating them, so the rule cannot drift here. The only change from
  TASK 44 is which pool the entries come from.

LITERAL — `the_families2_run.log`:

```
-- reading the pool
   pool entries 5274, pool units 30436
-- nodes (language, grammar-operator, arity) 197
-- cross-language edges, raw 864
-- edges surviving the mutual filter 294
-- families 35
{
 "edges_mutual": 294,
 "edges_raw": 864,
 "entry_count": 5274,
 "equally_strongest_ties": 109,
 "families": 35,
 "nodes": 197,
 "nodes_in_a_family": 161,
 "nodes_with_no_surviving_edge": 36,
 "singleton_families": 0
}
```

## 6.2 The two continuity checks

- **The ratified sighting survives, unchanged.** The family whose
  nodes are five different spellings of one machine behaviour is
  `F0009` in both files, same size, same languages.

LITERAL — `acceptance49_printed.txt`, section (e), last block:

```
      the_families1.json  F0009 size 6 ['c', 'cpp', 'go', 'rust', 'swift']
      the_families2.json  F0009 size 6 ['c', 'cpp', 'go', 'rust', 'swift']
```

  LITERAL — its nodes in `the_families2.json`:

```
      F0009 size  6 ['c', 'cpp', 'go', 'rust', 'swift']
           c:~(unary) cpp:compl(unary) cpp:~(unary) go:^(unary) rust:!(unary) swift:~(unary)
```

- **The nine-language family grew.** In `the_families1.json` `F0001`
  had nine nodes in nine languages. In `the_families2.json` it has
  seventeen nodes in the same nine languages.

LITERAL — `the_families2.json`, `F0001`:

```
      F0001 size 17 ['c', 'cpp', 'cpython', 'go', 'java', 'php', 'ruby', 'rust', 'swift']
           c:+(binary) c:++(unary) c:--(unary) c:__extension__(unary) cpp:+(binary) cpp:++(unary) cpp:--(unary) cpython:+(binary) go:+(binary) go:+(unary) java:+(binary) php:+(binary) ruby:+(binary) rust:+(binary) rust:..=(unary) swift:+(binary) swift:+(unary)
```

  GLOSS: the eight nodes that joined are unary nodes whose units share
  pool entries with the binary ones — the increment and decrement
  nodes of c and cpp, go's and swift's unary plus, and rust's
  inclusive-range node. The labels are display fields; entry
  co-membership is what attached them. Whether a unary increment node
  belongs in the same family as a binary addition node is a question
  about the rule's edge weights, not about this lap, and it is left
  standing rather than tuned.

- All 35 families, with every node, are printed in
  `acceptance49_printed.txt` section (e).

---

# 7. THE GUARD, RUN WITHOUT EXEMPTION

The lesson of log 147 §13 is applied literally: no guard file was
edited, nothing was added to any field set at run time, and **no
artifact this lap wrote declares a `role` field anywhere**. Every file
is walked in full.

LITERAL — `guard49_plain_transcript.txt`, complete:

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py the_pool2.json the_families2.json pool1_pool2_delta.json the_pool2_entry_E00029.json the_pool2_bytes.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS the_pool2.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families2.json -- no operator token in any key, grouping, pairing or row structure
PASS pool1_pool2_delta.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool2_entry_E00029.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool2_bytes.json -- no operator token in any key, grouping, pairing or row structure
PLAIN GUARD EXIT CODE = 0
```

The counts over that transcript, computed rather than eyeballed:

```
$ grep -c '^PASS ' Research/op_pipeline/guard49_plain_transcript.txt
5
$ grep -c '^FAIL' Research/op_pipeline/guard49_plain_transcript.txt
0
$ grep -c exempt Research/op_pipeline/guard49_plain_transcript.txt
0
```

GLOSS: five PASS lines, zero FAIL, exit code 0, and — the load-bearing
part — **zero lines say "exempt"**. Every line says "no operator token
in any key, grouping, pairing or row structure", which is the guard
having walked the file.

- The merge itself reads no token. The keys are a layer-5 string, a
  layer-3 string, or a proved-edge pair. The token rides on the member
  as `operator` and on a family node as `label`, and nothing reads
  either.
- `the_pool2_bytes.json` is keyed by wrapped-text strings and is
  checked with the rest, since a byte-measurement cache is still an
  artifact this stage wrote.

---

# 8. ZERO REGRESSIONS

Four claims, each checked rather than asserted, by
`zero_regression49.py`.

LITERAL — `zero_regression49_printed.txt`, in full:

```
CLAIM ONE -- task 47's and task 48's artifacts are untouched
  paths asked about: 678
  command: git status --porcelain -- ... (678 paths)
  the version control system reports 0 changed path(s)
  PASS -- no prior artifact differs from what is committed, so none was modified by this lap.

CLAIM TWO -- the_pool1.json and the_families1.json are untouched
  the_families1.json is TRACKED; the version control system reports 0 changed path(s)
  the_pool1.json is NOT tracked, so the version control system cannot answer for it.
    sha256            e54b90848c498395cb42dd18ab0aff39e2510a9c0071cd289203fbe4cb86572f
    size in bytes     18648016
    modified at       1788381142
    this lap's newest source file, modified at 1788398025
    PASS -- the_pool1.json predates every source file this lap wrote, so no program of this lap rewrote it.
  PASS

CLAIM THREE -- no program of this lap opens a prior artifact for writing
    build_the_pool2.py       open for writing: stem + ".s", "w"
    build_the_pool2.py       open for writing: BYTE_CACHE, "w"
    build_the_pool2.py       open for writing: path, "w"
    build_the_families2.py   open for writing: path, "w"
    compare_pool1_pool2.py   open for writing: path, "w"
    acceptance49.py          open for writing: path, "w"
  PASS -- every write names a file this lap created

CLAIM FOUR -- no unit loses pool membership
  pool1 member units                                28984
  of those, still proved by task 47                 28378
  of those, members of the_pool2.json               28378
  missing                                           0
  pool1 units task 47 did NOT prove, so not carried  606
  pool2 units that are new this round                2058
  every unit task 47 proved is a pool2 member: True
  PASS

ALL FOUR CLAIMS: PASS
```

- **The one honest gap, named.** `the_pool1.json` is 18.6 MB and is
  not tracked by the version control system, so the strongest
  available evidence for it is its sha256 plus the fact that its
  modification time (1788381142) is 16,883 seconds earlier than the
  newest source file this lap wrote (1788398025). That is weaker than
  the version control system's answer, and it is labelled as such
  rather than presented alongside it as the same kind of proof.
- The `git status` used in CLAIM ONE also answers the write-claim
  question the binding rules require: the version control system was
  asked before anything was ruled, and the daemon has already
  committed this lap's files (`git log --oneline -3` shows
  `81757b3 auto: 3 files (acceptance49.py, acceptance49_printed.txt,
  the_pool2_entry_E00029.json)`).

---

# 9. COMPLETE FILE INVENTORY

## 9.1 New this lap, all in `~/Programming/PseudoCoupHQ/Research/op_pipeline`

| file | bytes | what it is |
| --- | --- | --- |
| `build_the_pool2.py` | 29,866 | builds the pool: intake of the three populations from the canon37 artifacts, the layer-5 / layer-3 / proved-edge merge with transitive closure, the eligibility rule, the representative rule with real assembled byte counts, and the brief-strict count computed from the same code |
| `the_pool2.json` | 33,810,895 | **THE POOL** — 5,274 entries over 30,436 member units |
| `the_pool2_bytes.json` | 453,051 | the 1,437 assembled texts and their measured byte counts |
| `the_pool2_run.log` | 1,466 | the build's own printed output |
| `build_the_families2.py` | 9,970 | the dom_op construction rule over the pool, importing `dom_ops` and `dom_ops_0branch` unchanged |
| `the_families2.json` | 210,545 | the 35 families, the 36 unattached nodes, the 109 equally-strongest ties |
| `the_families2_run.log` | 445 | the family build's printed output |
| `compare_pool1_pool2.py` | 12,432 | the join on member sets: every split and every merge, each with its computed cause |
| `pool1_pool2_delta.json` | 413,108 | the 14 splits and the 492 merges, with causes and crossing-pair counts |
| `pool1_pool2_delta_printed.txt` | 1,096 | that program's printed output |
| `acceptance49.py` | 11,066 | every figure this report states, computed |
| `acceptance49_printed.txt` | 134,267 | its output, including `E00029` member by member and all 35 families |
| `the_pool2_entry_E00029.json` | 118,843 | E00033's successor, verbatim |
| `zero_regression49.py` | 8,506 | the four zero-regression claims |
| `zero_regression49_printed.txt` | 1,800 | their transcript |
| `guard49_plain_transcript.txt` | 559 | the UNMODIFIED guard over all five artifacts, exit code included |
| `DevComms/log_148_task49_the_pool2.md` | this file | the report |
| `Planning/node_0_3_research/node_0_3_5_compiler_graph/PROGRESS.md` | — | a dated entry appended under the single `# PROGRESS` heading (edited, not created) |

## 9.2 Read by this lap, read-only, none modified

- `canon37_wrapped_{c,cpp,go,rust,swift}.json`, `canon37_interp.json`,
  `canon37_regen_store/*.json` (326 files) — TASK 47's proved units.
- `layer4b_terms_{c,cpp,go,rust,swift}.json`, `layer4b_interp.json`,
  `layer4b_regen_store/*.json` (326 files) — TASK 48's SECOND-VERSION
  layer-4 records, per log 147 §13. The first-version `layer4_*` files
  and `name_census2.json` are NOT read by any program of this lap.
- `proved_edges.json`, `proved_edges2.json`, `proved_edges3.json`,
  `interp_join3.json`, `interp_fastpath.json` — the proved edges.
- `the_pool1.json`, `the_families1.json` — read for the comparison
  only; both are the superseded record and stay on disk unchanged.
- `probe_manifest_*.json` — read by the guard for its token inventory.
- `dom_ops.py`, `dom_ops_0branch.py`, `check_no_spelling_keys.py` —
  imported or run, unmodified.

---

# 10. THE EVIDENCE CLASS OF EACH CLAIM

- **Forced by construction over artifacts this lap built:** the entry
  count, the member counts, the population split, the language spans,
  the compiled/interpreted spans, the family and node counts, the
  split and merge counts and their causes, the multi-language
  accounting, the eligibility breakdown. Each is a count over a file
  on disk, printed by the program that wrote it.
- **Measured with a tool:** the representative byte counts (`as
  --64` plus `objdump -d` over 1,437 texts), the sha256, the `git
  status` and `git log` lines, the guard transcript.
- **Inherited testimony, weaker than the above, carried with its own
  wording:** every proved edge, and every layer-4 verdict. This pool
  re-proves nothing. A layer-5 join rests on TASK 48's two z3 routes,
  which are proofs about a MODEL of the machine — the lifter's — and
  each entry names the artifact the ground came from.
- **This lap's own judgment, named as such:** (1) that layer-3
  wrapped-text identity belongs among the grounds beside layer-5
  identity, stated in §1.4 with the brief-strict count printed beside
  it so the choice can be struck; (2) that the 826 withdrawals are
  carried-and-flagged rather than dropped, stated in §1.3; (3) that
  an entry's `type_key` — which register family each arriving lineage
  loads through, and how wide the answer is — is the right
  machine-form stand-in for the compiled table's operand-type key in
  the families' second edge weight. All three sit on the artifact's
  `meta` so they can be struck.

---

# 11. WHAT IS PUT TO DEE

Nothing is awaiting a decision to continue. Two things are recorded
for a ruling whenever he wants one, and neither blocks TASK 51.

- **The branch-label defect in the layer-3 form (§4.2.2).** 4,499
  member units carry a symbolic branch target that contains the
  unit's own name, and normalizing it would take the pool's distinct
  layer-3 texts from 6,277 to 2,999. AgentMemory's canonical-form
  ruling already requires positional branch labels; the wrapped form
  does not do it yet. This is a fix to TASK 47's form, not to the
  pool.
- **The third merge ground (§1.4).** Layer-3 wrapped-text identity was
  kept. The brief-strict count without it is 8,140 entries against
  5,274.
