# log 154 — TASK 54: the_pool3, the pool over canon38

Date: 2026-09-03. Author: Claude Code (implementer), no sub-agents.
Working directory: `PRIVATE/PseudoCoupHQ/Research/op_pipeline`.
Python: `/tmp/reconnect_venv/bin/python3`. Assembly on the host:
`as --64`, `objdump -d`.

Every rendering below is labelled **LITERAL**, **GLOSS** or **ANALOGY**,
per the protocol's §5.1a. A gloss never appears without the literal it
glosses. Every figure states its population, per §3.4a.

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

# 1. The verdict, with its population

## 1.1 The one-line state

**The same 30,436 units, re-merged over canon38 on ruling 1's three
grounds, collapse from 5,274 entries to 2,247; the entries reaching
across more than one language rise from 423 to 632; the three
compiled-and-interpreted entries hold; the families go from 35 to 36
over the same 197 nodes.**

## 1.2 The population, stated on the artifact

LITERAL — `the_pool3.json`, `meta.population`, read back by
`audit54.py` section (c):

```
    every unit TASK 52 (log_152) proved: 30,436 of 31,078 attempted --
    original 1,763, interpreter 9, regenerated 28,664
```

LITERAL — `the_pool3.json`, `summary.units_by_arrival_population`:

```
    {"interpreter": 9, "original": 1763, "regenerated": 28664}
```

- Nothing is sampled. Every unit `canon38_*` marks
  `WRAPPED_TEXT_PROVED` is a member, and the builder refuses its own
  output if any of them lacks a layer-4 record (`REFUSED OWN OUTPUT:
  N proved units have no layer-4 record`). It did not fire: 30,436
  records were read for 30,436 members.

## 1.3 The counts against pool2, per population

LITERAL — `audit54_printed.txt`, section (a). Population of both
columns: the same 30,436 units.

```
    quantity                                          pool2    pool3    delta
    member units                                      30436    30436       +0
    entries                                            5274     2247    -3027
    entries spanning more than one language             423      632     +209
    entries spanning compiled and interpreted             3        3       +0
    families                                             35       36       +1
    family nodes                                        197      197       +0
    nodes in a family                                   161      165       +4
    singleton families                                    0        0       +0
    distinct layer-3 wrapped texts                     6277     2997    -3280
    distinct layer-5 texts among eligible units        1132     1104      -28
    proved edges applied                                118      118       +0
```

GLOSS — the two numbers that drive everything below. The layer-3
ground got 3,280 stronger (6,277 distinct wrapped texts down to
2,997), because ruling 4's positional branch labels stopped a unit's
own name from sitting inside its own text. The layer-5 ground got
slightly weaker (1,132 distinct texts down to 1,104, but 282 fewer
units eligible to use it), because task 53's flag link cost 699 old
proofs and won 417 new ones.

## 1.4 The brief-strict count — RECORDED on the artifact, not used

Ruling 1: the pool merges on three grounds and the two-ground count is
recorded, never used.

LITERAL — `audit54_printed.txt`, section (b):

```
    pool3 entries, three grounds (THE COUNT)            2247
    pool3 entries, layer-5 identity + proved edges      8394
    pool2 entries, three grounds                        5274
    pool2 entries, layer-5 identity + proved edges      8140
```

LITERAL — where it is recorded, `the_pool3.json` `summary`:

```
 "entries": 2247,
 "entries_under_the_brief_strict_rule": 8394,
```

LITERAL — `the_pool3.json` `meta.brief_strict_count_note`:

```
    the two-ground count (layer-5 identity and proved edges only, no
    layer-3 identity) is RECORDED in the summary as
    `entries_under_the_brief_strict_rule` and is NOT the pool's entry
    count, per ruling 1
```

---

# 2. The merge, with values moving through it

## 2.1 The three grounds, named before they are used

- **Layer 3, the wrapped text.** The unit's memory-wrapped machine
  code as one line of arch opcodes: a prelude that loads each arriving
  lineage out of the ledger, the compiler's own body verbatim, an
  epilogue that stores the answer to OUT-0. Two units whose wrapped
  texts are the same string are the same machine code twice.
- **Layer 5, the normalized term.** Task 53 transcribed each ledger
  from OUT-0 downward into a z3 term, proved that term equal to the
  unit's own machine code, then printed it with its free symbols
  renamed positionally `v0, v1, …`. Only a PROVED term counts.
- **A proved edge.** A pair an earlier prover established equal:
  `proved_edges{,2,3}.json`, `interp_join3.json`,
  `interp_fastpath.json`. 118 of them have both endpoints in this
  pool, the same 118 pool2 applied.

The join is closed under transitivity.

## 2.2 The counts each ground contributed, over the 30,436

LITERAL — `the_pool3_run.log`:

```
   distinct_layer3_wrapped_texts                  2997
   distinct_layer5_texts_among_eligible_units     1104
   layer3_identity_merges                         27439
   layer5_identity_merges                         22028
   proved_edges_applied                           118
   entries 2247
```

GLOSS: 27,439 units arrived at a wrapped text some earlier unit
already held, 22,028 at a layer-5 text some earlier eligible unit
already held, and 118 pairs arrived carrying a proof. The three
overlap heavily; the entry count is what survives all three closed
under transitivity, not their sum.

## 2.3 Two units arriving at one entry, with the strings shown

LITERAL — `audit54_printed.txt`, section (e), the ground listed on the
entry, and `acceptance53_printed.txt` part (e) for the two texts:

```
    c/op_109   layer 3: mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi;
                        mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi;
                        lea (%rdi,%rsi,1),%rax;
                        mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret
               layer 5: v0 + v1
    go/op_319  layer 3: mov ledger+0x00(%rip),%rax; mov 0x0(%rax),%rax;
                        mov ledger+0x00(%rip),%rbx; mov 0x8(%rbx),%rbx;
                        add %rbx,%rax;
                        mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret
               layer 5: v0 + v1
```

- The two layer-3 texts are DIFFERENT strings: one compiler wrote a
  single address-arithmetic instruction, the other a register move and
  an add. Ground (b) does not reach between them.
- The two layer-5 texts are the SAME string, `v0 + v1`, and both terms
  are proved against their own machine code. Ground (a) joins them.
- Both land in `E00029`, and so do 156 more units.

## 2.4 The representative, decided by real bytes

- The rule (AgentMemory, the owner 2026-08-29): the simplest member —
  fewest bytes of machine code, ties by first-in-list order.
- 394 of the 2,247 entries carry more than one wrapped text, which is
  where the byte count has to decide something. Those 1,144 distinct
  texts were assembled with `as --64` and their bytes counted from
  `objdump -d`.
- LITERAL — `the_pool3_run.log`:

```
   entries carrying more than one wrapped text 394
   distinct texts to assemble 1144
   texts newly assembled 1144, cache holds 1144
```

- **8 of the 1,144 texts would not assemble**, and the substitution is
  stated on the entry rather than hidden. All 8 carry an inline
  constant-pool relocation note the stored text keeps, e.g.
  `addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4`, which is
  not assembler syntax. **2 entries of the 2,247** fall back to
  character length for their representative, and each says so in
  `representative_size_measured_as`:
  "the text would not assemble, so its character length stands in and
  the substitution is stated here rather than hidden".

---

# 3. THE UNITS WITH NO PROVED TERM — carried, and flagged

THE REPRESENTATIVE RULE names the simplest member of a group that has
been PROVED equivalent. A term that was disproved, undecided, or never
built is not proof of anything, so it may not join two units.

LITERAL — `audit54_printed.txt`, section (d), population 30,436:

```
     23132  eligible -- the term was proved
      5602  the layer-4 term was undecided on both routes, so the layer-5 text is not proved equivalence
      1287  no layer-4 term was built for this unit, so it has no layer-5 text to be identical to
       415  the layer-4 term was DISPROVED against this unit's own machine code and was withdrawn, so its layer-5 text is refuted evidence and may not join anything
     30436  TOTAL
```

- 23,132 + 5,602 + 1,287 + 415 = 30,436, and those are task 53's own
  four figures (log 153 §1.2), recomputed here from the `layer4c_*`
  artifacts rather than copied.
- **All 7,304 are CARRIED as members.** Removing them would misstate
  the population, and the authoritative count line is 30,436.
- **All 7,304 are EXCLUDED from ground (a)**, each with the flag
  `layer5_merge_eligible: false` and the reason printed above stored
  beside it on the member.
- **All 7,304 remain reachable by ground (b) and ground (c)**, because
  neither rests on the term: layer-3 identity is the same machine code
  twice, and a proved edge was established elsewhere. That is what
  THE REPRESENTATIVE RULE permits and what this pool does.
- The 415 withdrawn are the ones the brief names. They are a proper
  subset of the 7,304 and are treated identically to the other 6,889.

LITERAL — one such member as stored in `the_pool3.json`:

```
 "layer5_merge_eligible": false,
 "layer5_merge_eligibility_reason": "the layer-4 term was DISPROVED
   against this unit's own machine code and was withdrawn, so its
   layer-5 text is refuted evidence and may not join anything"
```

---

# 4. E00029's SUCCESSOR, PRINTED VERBATIM

## 4.1 The successor is `E00029` again, and it is not a guess

The successor was found by a JOIN ON MEMBER SETS: take pool2's
`E00029`, follow its 158 members into pool3, and see where they land.

LITERAL — `audit54_printed.txt`, section (e):

```
    pool2 E00029: 158 members, representative go/op_319
    those members land in 1 pool3 entr(y/ies):
      E00029 holds 158 of them, and has 158 members in all
```

GLOSS: all 158 landed in one pool3 entry, and that entry acquired no
new member. Integer addition neither split nor grew; it kept its id by
coincidence of ordering, not by name-matching.

## 4.2 The entry itself

LITERAL — `the_pool3.json`, entry `E00029`, every field except the
158-long `members` list and the 26-long `cross_language_grounds` list:

```
 "entry_id": "E00029",
 "member_count": 158,
 "representative": "go/op_319",
 "representative_size": 35,
 "representative_size_measured_as": "bytes of machine code, assembled with `as` and counted from objdump",
 "representative_rule": "the simplest member -- fewest bytes of machine code, ties broken by first-in-list order",
 "languages": ["c", "cpp", "cpython", "go", "php", "ruby", "rust"],
 "language_count": 7,
 "spans_more_than_one_language": true,
 "arrival_populations": ["interpreter", "original", "regenerated"],
 "spans_compiled_and_interpreted": true,
 "distinct_wrapped_text_count": 12,
 "layer5_normalized_texts": ["v0 + v1"],
 "distinct_layer5_text_count": 1,
 "members_not_layer5_eligible": 0,
 "type_key": "rdi,rsi|64"
```

LITERAL — its 26 cross-language grounds, by kind (7 + 1 + 17 + 1 = 26):

```
   17  a PROVED_EQUAL relation of the interpreter join
    7  layer-3 text identity
    1  layer-5 text identity
    1  the fast-path proof
```

LITERAL — the first of those grounds, as stored:

```
 {
  "ground": "layer-3 text identity",
  "languages_it_joins": ["c", "cpp", "rust"],
  "detail": "these members carry the SAME wrapped text, character for character -- the same machine code twice",
  "wrapped_text": "mov ledger+0x00(%rip),%rdi; mov 0x0(%rdi),%rdi; mov ledger+0x00(%rip),%rsi; mov 0x8(%rsi),%rsi; lea (%rdi,%rsi,1),%rax; mov ledger+0x38(%rip),%r11; mov %rax,0x0(%r11); ret"
 }
```

- Seven languages in one entry, three of them interpreters
  (`cpython`, `php`, `ruby`), 12 distinct wrapped texts, ONE layer-5
  text. Every member's term is proved: `members_not_layer5_eligible`
  is 0.
- The representative is `go/op_319` at 35 assembled bytes, unchanged
  from pool2. The brief's note stands: the php/add_function question
  is moot.
- The full record, with all 158 members and all 26 grounds, is in
  `audit54_printed.txt` section (e) and in `the_pool3.json`.

---

# 5. EVERY SPLIT AND EVERY MERGE, WITH ITS COMPUTED CAUSE

## 5.1 How the comparison was made

- `compare_pool2_pool3.py` is a JOIN ON MEMBER SETS and nothing else.
  No entry is matched by name; no token is read.
- SPLIT — one pool2 entry whose shared members land in MORE THAN ONE
  pool3 entry. MERGE — one pool3 entry whose shared members come from
  MORE THAN ONE pool2 entry.
- The cause is COMPUTED by asking the machine forms: for a merge,
  which ground crosses the old boundary; for a split, which ground
  failed.

LITERAL — `pool2_pool3_delta_printed.txt`:

```
== populations
   pool2 member units                       30436
   pool3 member units                       30436
   units in both, the comparable population 30436
   in pool2 only -- absent from the newer pool 0
   in pool3 only -- absent from the older pool 0

== the join on member sets
   pool2 entries holding a shared unit       5274
   pool3 entries holding a shared unit       2247
   pool2 entries that SPLIT                  60
   pool3 entries that MERGED                 719
```

- **The comparable population is the whole population.** Both pools
  hold exactly the same 30,436 units, so no split or merge is
  contaminated by an arrival or a departure.

## 5.2 The cause tallies

LITERAL — `pool2_pool3_delta_printed.txt`, split causes (population:
the 60 splits; one entry may carry more than one cause; the
"N member(s)" lines differ only in N and are one cause):

```
       60  the members carry more than one layer-3 wrapped text, so layer-3 identity does not join them
       11  the eligible members normalize to more than one layer-5 text, so layer-5 identity does not join them
       49  N member(s) have no eligible layer-5 text, so no layer-5 ground can reach them
```

LITERAL — merge grounds (population: the 719 merges):

```
      711  layer-3 wrapped-text identity
       13  layer-5 normalized-text identity
        0  no single crossing pair -- transitive chain only
```

- **Every merge has a named crossing pair.** Zero merges are
  transitive-only, so no merge in this pool rests on a chain nobody
  can point at.
- **Every split has a computed cause.** Zero splits are UNEXPLAINED —
  the builder emits that word when the machine forms agree and it does
  not appear once.

## 5.3 The mechanism behind the 60 splits, with the numbers

The split cause "N member(s) have no eligible layer-5 text" is task
53's flag link showing up here. LITERAL — `audit54_printed.txt`,
section (g), population 30,436:

```
    eligible in pool2 (canon37 / layer4b)             23414
    eligible in pool3 (canon38 / layer4c)             23132
    lost eligibility                                    699
    gained eligibility                                  417
    net                                                -282
```

- 699 units were proved at layer 4 over canon37 and are not proved
  over canon38; 417 went the other way; 699 − 417 = 282, exactly log
  153 §1.3's −282, and 699 is exactly log 153 §4.2's "the flag link
  costs 699 old proofs".
- **So the splits are not a canon38 layer-3 regression.** A pool2
  entry that had been held together by a layer-5 text lost the member
  carrying that proof, and layer-3 identity was never able to reach
  the rest of it — which is what "distinct layer-3 texts 8" on those
  rows says.

## 5.4 EVERY SPLIT — all 60, one line each

Read: pool2 entry, shared members, the pool3 entries they landed in,
distinct layer-3 texts among them, distinct layer-5 texts among the
eligible ones, causes. Full blocks with member lists are in
`pool2_pool3_delta_full.txt`.

```
E00103    99 members  into 3 pool3 entries [E00103,E02151,E02189]  l3 texts 28  l5 texts 1  CAUSE: more than one layer-3 text; 2 member(s) with no eligible layer-5 text
E00124     6 members  into 2 pool3 entries [E00124,E00250]  l3 texts 2  l5 texts 3  CAUSE: more than one layer-3 text; more than one layer-5 text
E00179   136 members  into 3 pool3 entries [E00178,E01589,E01787]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00180    70 members  into 3 pool3 entries [E00179,E01590,E01790]  l3 texts 6  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00183   136 members  into 3 pool3 entries [E00182,E01566,E01796]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00184   118 members  into 11 pool3 entries [E00183,E01563,E01569,E01571,E01610,E01629,E01784,E01788,E01789,E01802,E01805]  l3 texts 17  l5 texts 1  CAUSE: more than one layer-3 text; 28 member(s) with no eligible layer-5 text
E00185   148 members  into 11 pool3 entries [E00184,E01564,E01579,E01581,E01611,E01630,E01785,E01792,E01793,E01803,E01806]  l3 texts 17  l5 texts 1  CAUSE: more than one layer-3 text; 32 member(s) with no eligible layer-5 text
E00188   126 members  into 3 pool3 entries [E00187,E01565,E01794]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00189    70 members  into 3 pool3 entries [E00188,E01576,E01797]  l3 texts 6  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00191    12 members  into 2 pool3 entries [E00190,E00267]  l3 texts 2  l5 texts 9  CAUSE: more than one layer-3 text; more than one layer-5 text
E00192    78 members  into 3 pool3 entries [E00191,E01575,E01795]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00203   126 members  into 3 pool3 entries [E00202,E01585,E01786]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00207   136 members  into 3 pool3 entries [E00206,E01693,E01750]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00208    70 members  into 3 pool3 entries [E00207,E01694,E01754]  l3 texts 6  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00211   136 members  into 3 pool3 entries [E00210,E01671,E01759]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00212   118 members  into 11 pool3 entries [E00211,E01668,E01674,E01676,E01713,E01732,E01747,E01751,E01752,E01766,E01769]  l3 texts 17  l5 texts 1  CAUSE: more than one layer-3 text; 28 member(s) with no eligible layer-5 text
E00213   148 members  into 11 pool3 entries [E00212,E01669,E01684,E01686,E01714,E01733,E01748,E01755,E01756,E01767,E01770]  l3 texts 17  l5 texts 1  CAUSE: more than one layer-3 text; 32 member(s) with no eligible layer-5 text
E00216   126 members  into 3 pool3 entries [E00215,E01670,E01757]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00217    70 members  into 3 pool3 entries [E00216,E01681,E01760]  l3 texts 6  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00220    78 members  into 3 pool3 entries [E00219,E01680,E01758]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00228    12 members  into 2 pool3 entries [E00227,E00270]  l3 texts 2  l5 texts 9  CAUSE: more than one layer-3 text; more than one layer-5 text
E00231   126 members  into 3 pool3 entries [E00230,E01690,E01749]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00232    78 members  into 3 pool3 entries [E00231,E01691,E01753]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 14 member(s) with no eligible layer-5 text
E00275    36 members  into 2 pool3 entries [E00275,E01866]  l3 texts 2  l5 texts 1  CAUSE: more than one layer-3 text; 7 member(s) with no eligible layer-5 text
E00278    36 members  into 2 pool3 entries [E00278,E01847]  l3 texts 2  l5 texts 1  CAUSE: more than one layer-3 text; 7 member(s) with no eligible layer-5 text
E00279    30 members  into 6 pool3 entries [E00279,E01846,E01851,E01853,E01900,E01920]  l3 texts 6  l5 texts 1  CAUSE: more than one layer-3 text; 13 member(s) with no eligible layer-5 text
E00282    10 members  into 4 pool3 entries [E00282,E01857,E01862,E01921]  l3 texts 4  l5 texts 1  CAUSE: more than one layer-3 text; 5 member(s) with no eligible layer-5 text
E01045     4 members  into 2 pool3 entries [E00693,E00753]  l3 texts 2  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01187     2 members  into 2 pool3 entries [E00780,E00817]  l3 texts 2  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01235     4 members  into 2 pool3 entries [E00810,E00819]  l3 texts 2  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01638    10 members  into 2 pool3 entries [E00982,E01266]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01669     4 members  into 2 pool3 entries [E01000,E01777]  l3 texts 4  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01675     3 members  into 2 pool3 entries [E01004,E01544]  l3 texts 3  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01676     4 members  into 2 pool3 entries [E01005,E01281]  l3 texts 4  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01717    10 members  into 2 pool3 entries [E01022,E01252]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01721    26 members  into 10 pool3 entries [E01026,E01031,E01033,E01067,E01096,E01267,E01270,E01271,E01283,E01286]  l3 texts 10  l5 texts 0  CAUSE: more than one layer-3 text; 26 member(s) with no eligible layer-5 text
E01722    30 members  into 10 pool3 entries [E01027,E01041,E01043,E01068,E01097,E01268,E01273,E01275,E01284,E01287]  l3 texts 10  l5 texts 0  CAUSE: more than one layer-3 text; 30 member(s) with no eligible layer-5 text
E01723    12 members  into 2 pool3 entries [E01028,E01276]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01727    10 members  into 2 pool3 entries [E01034,E01253]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01731    12 members  into 2 pool3 entries [E01038,E01277]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01741    12 members  into 2 pool3 entries [E01044,E01269]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01742    12 members  into 2 pool3 entries [E01045,E01272]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01806     6 members  into 2 pool3 entries [E01084,E01274]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 6 member(s) with no eligible layer-5 text
E01807    60 members  into 3 pool3 entries [E01085,E01591,E01791]  l3 texts 8  l5 texts 1  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01828    10 members  into 2 pool3 entries [E01102,E01230]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01829    10 members  into 2 pool3 entries [E01103,E01236]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01867     4 members  into 2 pool3 entries [E01126,E01762]  l3 texts 4  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01868     4 members  into 2 pool3 entries [E01127,E01245]  l3 texts 4  l5 texts 2  CAUSE: more than one layer-3 text; more than one layer-5 text
E01909    10 members  into 2 pool3 entries [E01144,E01216]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01913    26 members  into 10 pool3 entries [E01148,E01153,E01155,E01188,E01213,E01231,E01234,E01235,E01247,E01250]  l3 texts 10  l5 texts 0  CAUSE: more than one layer-3 text; 26 member(s) with no eligible layer-5 text
E01914    30 members  into 10 pool3 entries [E01149,E01163,E01165,E01189,E01214,E01232,E01238,E01239,E01248,E01251]  l3 texts 10  l5 texts 0  CAUSE: more than one layer-3 text; 30 member(s) with no eligible layer-5 text
E01915    12 members  into 2 pool3 entries [E01150,E01240]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01919    10 members  into 2 pool3 entries [E01156,E01217]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 10 member(s) with no eligible layer-5 text
E01923    12 members  into 2 pool3 entries [E01160,E01241]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01933    12 members  into 2 pool3 entries [E01166,E01233]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E01934    12 members  into 2 pool3 entries [E01167,E01237]  l3 texts 2  l5 texts 0  CAUSE: more than one layer-3 text; 12 member(s) with no eligible layer-5 text
E04307    30 members  into 2 pool3 entries [E01848,E01901]  l3 texts 2  l5 texts 1  CAUSE: more than one layer-3 text; 6 member(s) with no eligible layer-5 text
E04314    18 members  into 2 pool3 entries [E01858,E01922]  l3 texts 2  l5 texts 1  CAUSE: more than one layer-3 text; 6 member(s) with no eligible layer-5 text
E04326    30 members  into 2 pool3 entries [E01869,E01873]  l3 texts 2  l5 texts 1  CAUSE: more than one layer-3 text; 6 member(s) with no eligible layer-5 text
E04327    18 members  into 2 pool3 entries [E01870,E01875]  l3 texts 2  l5 texts 1  CAUSE: more than one layer-3 text; 6 member(s) with no eligible layer-5 text
```

## 5.5 EVERY MERGE — all 719, one line each

Read: pool3 entry, shared members, the pool2 entries they came from,
and the crossing pairs that carry each ground. `x37` means 37 pairs of
members drawn from two different pool2 entries share that ground.

```
E00033    12 members  from  4 pool2 entries [E00033,E00474,E00475,E02415]  CAUSE: layer-3 wrapped-text identity x37; layer-5 normalized-text identity x6
E00049     6 members  from  2 pool2 entries [E00049,E00582]  CAUSE: layer-3 wrapped-text identity x5; layer-5 normalized-text identity x3
E00137     4 members  from  2 pool2 entries [E00137,E00139]  CAUSE: layer-5 normalized-text identity x1
E00172    18 members  from  5 pool2 entries [E00173,E00296,E00297,E01628,E03474]  CAUSE: layer-3 wrapped-text identity x85; layer-5 normalized-text identity x18
E00189    12 members  from  2 pool2 entries [E00190,E00235]  CAUSE: layer-3 wrapped-text identity x14; layer-5 normalized-text identity x24
E00217    12 members  from  2 pool2 entries [E00218,E04007]  CAUSE: layer-3 wrapped-text identity x5; layer-5 normalized-text identity x9
E00218    12 members  from  2 pool2 entries [E00219,E00270]  CAUSE: layer-5 normalized-text identity x1
E00283     3 members  from  3 pool2 entries [E00283,E04408,E04413]  CAUSE: layer-3 wrapped-text identity x3
E00287     3 members  from  3 pool2 entries [E00287,E04355,E04356]  CAUSE: layer-3 wrapped-text identity x3
E00302     2 members  from  2 pool2 entries [E00304,E04802]  CAUSE: layer-3 wrapped-text identity x1
E00303     3 members  from  3 pool2 entries [E00305,E04800,E04803]  CAUSE: layer-3 wrapped-text identity x3
E00305     2 members  from  2 pool2 entries [E00307,E04813]  CAUSE: layer-3 wrapped-text identity x1
E00306     3 members  from  3 pool2 entries [E00308,E04811,E04814]  CAUSE: layer-3 wrapped-text identity x3
E00307     4 members  from  4 pool2 entries [E00309,E04816,E04819,E04821]  CAUSE: layer-3 wrapped-text identity x6
E00308     7 members  from  7 pool2 entries [E00310,E04832,E04840,E04850,E04860,E04865,E04875]  CAUSE: layer-3 wrapped-text identity x21
E00309    13 members  from 13 pool2 entries [E00311,E04830,E04833,E04838,E04841,E04848,E04851,E04858,E04861,E04863,E04866,E04873,E04876]  CAUSE: layer-3 wrapped-text identity x78
E00311     7 members  from  7 pool2 entries [E00313,E00316,E04824,E04845,E04855,E04870,E04880]  CAUSE: layer-3 wrapped-text identity x21
E00312    12 members  from 12 pool2 entries [E00314,E00317,E04822,E04825,E04843,E04846,E04853,E04856,E04868,E04871,E04878,E04881]  CAUSE: layer-3 wrapped-text identity x66
E00314     2 members  from  2 pool2 entries [E00318,E04902]  CAUSE: layer-3 wrapped-text identity x1
E00315     3 members  from  3 pool2 entries [E00319,E04900,E04903]  CAUSE: layer-3 wrapped-text identity x3
E00317     3 members  from  3 pool2 entries [E00321,E04885,E04910]  CAUSE: layer-3 wrapped-text identity x3
E00318     5 members  from  5 pool2 entries [E00322,E04883,E04886,E04908,E04911]  CAUSE: layer-3 wrapped-text identity x10
E00320     4 members  from  4 pool2 entries [E00324,E04924,E04950,E04964]  CAUSE: layer-3 wrapped-text identity x6
E00321     7 members  from  7 pool2 entries [E00325,E04922,E04925,E04948,E04951,E04962,E04965]  CAUSE: layer-3 wrapped-text identity x21
E00334     2 members  from  2 pool2 entries [E00338,E05086]  CAUSE: layer-3 wrapped-text identity x1
E00335     3 members  from  3 pool2 entries [E00339,E05083,E05087]  CAUSE: layer-3 wrapped-text identity x3
E00336     2 members  from  2 pool2 entries [E00340,E05021]  CAUSE: layer-3 wrapped-text identity x1
E00337     3 members  from  3 pool2 entries [E00341,E05018,E05022]  CAUSE: layer-3 wrapped-text identity x3
E00338     3 members  from  3 pool2 entries [E00342,E05024,E05028]  CAUSE: layer-3 wrapped-text identity x3
E00339     2 members  from  2 pool2 entries [E00343,E05034]  CAUSE: layer-3 wrapped-text identity x1
E00340     3 members  from  3 pool2 entries [E00344,E05031,E05035]  CAUSE: layer-3 wrapped-text identity x3
E00341     3 members  from  3 pool2 entries [E00345,E05037,E05041]  CAUSE: layer-3 wrapped-text identity x3
E00342     2 members  from  2 pool2 entries [E00346,E05046]  CAUSE: layer-3 wrapped-text identity x1
E00343     3 members  from  3 pool2 entries [E00347,E05043,E05047]  CAUSE: layer-3 wrapped-text identity x3
E00344     3 members  from  3 pool2 entries [E00348,E05049,E05053]  CAUSE: layer-3 wrapped-text identity x3
E00345     2 members  from  2 pool2 entries [E00349,E05059]  CAUSE: layer-3 wrapped-text identity x1
E00346     3 members  from  3 pool2 entries [E00350,E05056,E05060]  CAUSE: layer-3 wrapped-text identity x3
E00347     3 members  from  3 pool2 entries [E00351,E05062,E05066]  CAUSE: layer-3 wrapped-text identity x3
E00348     2 members  from  2 pool2 entries [E00352,E05073]  CAUSE: layer-3 wrapped-text identity x1
E00349     3 members  from  3 pool2 entries [E00353,E05069,E05074]  CAUSE: layer-3 wrapped-text identity x3
E00350     3 members  from  3 pool2 entries [E00354,E05076,E05080]  CAUSE: layer-3 wrapped-text identity x3
E00369     4 members  from  4 pool2 entries [E00373,E00378,E05251,E05266]  CAUSE: layer-3 wrapped-text identity x6
E00370     6 members  from  6 pool2 entries [E00374,E00379,E05248,E05252,E05263,E05267]  CAUSE: layer-3 wrapped-text identity x15
E00371     6 members  from  6 pool2 entries [E00375,E00380,E05254,E05258,E05269,E05273]  CAUSE: layer-3 wrapped-text identity x15
E00372     4 members  from  4 pool2 entries [E00376,E00381,E05246,E05261]  CAUSE: layer-3 wrapped-text identity x6
E00373     4 members  from  4 pool2 entries [E00377,E00382,E05245,E05260]  CAUSE: layer-3 wrapped-text identity x6
E00377     3 members  from  2 pool2 entries [E00386,E02312]  CAUSE: layer-3 wrapped-text identity x2
E00383     4 members  from  4 pool2 entries [E00392,E00396,E02315,E02317]  CAUSE: layer-3 wrapped-text identity x6
E00385     4 members  from  4 pool2 entries [E00394,E00397,E02316,E02318]  CAUSE: layer-3 wrapped-text identity x6
E00390    10 members  from 10 pool2 entries [E00401,E00459,E00461,E00488,E00498,E02375,E02377,E02383,E02399,E02409]  CAUSE: layer-3 wrapped-text identity x45
E00391    10 members  from 10 pool2 entries [E00402,E00460,E00462,E00489,E00499,E02376,E02378,E02384,E02400,E02410]  CAUSE: layer-3 wrapped-text identity x45
E00393    10 members  from 10 pool2 entries [E00404,E00409,E00410,E00417,E00422,E02323,E02324,E02327,E02334,E02339]  CAUSE: layer-3 wrapped-text identity x45
E00394     3 members  from  3 pool2 entries [E00405,E02319,E05055]  CAUSE: layer-3 wrapped-text identity x3
E00395     2 members  from  2 pool2 entries [E00406,E02320]  CAUSE: layer-3 wrapped-text identity x1
E00396     4 members  from  4 pool2 entries [E00407,E00451,E02321,E02367]  CAUSE: layer-3 wrapped-text identity x6
E00397     4 members  from  4 pool2 entries [E00408,E00455,E02322,E02371]  CAUSE: layer-3 wrapped-text identity x6
E00398     2 members  from  2 pool2 entries [E00411,E02328]  CAUSE: layer-3 wrapped-text identity x1
E00399     2 members  from  2 pool2 entries [E00412,E02329]  CAUSE: layer-3 wrapped-text identity x1
E00400    24 members  from 23 pool2 entries [E00413,E00416,E00418,E00421,E00426,E00476,E00486,E00490,E00496,E00506,E02325,E02330,E02333,E02335,E02338,E02343,E02379,E02391,E02397,E02401,E02407,E02418,E02420]  CAUSE: layer-3 wrapped-text identity x275
E00401    16 members  from 16 pool2 entries [E00414,E00415,E00419,E00420,E00479,E00484,E00492,E00494,E02331,E02332,E02336,E02337,E02393,E02395,E02403,E02405]  CAUSE: layer-3 wrapped-text identity x120
E00402     6 members  from  6 pool2 entries [E00423,E00500,E02326,E02340,E02381,E02411]  CAUSE: layer-3 wrapped-text identity x15
E00403     8 members  from  8 pool2 entries [E00424,E00425,E00502,E00504,E02341,E02342,E02413,E02416]  CAUSE: layer-3 wrapped-text identity x28
E00404    10 members  from 10 pool2 entries [E00427,E00432,E00433,E00441,E00446,E02348,E02349,E02352,E02357,E02362]  CAUSE: layer-3 wrapped-text identity x45
E00405     2 members  from  2 pool2 entries [E00428,E02344]  CAUSE: layer-3 wrapped-text identity x1
E00406     2 members  from  2 pool2 entries [E00429,E02345]  CAUSE: layer-3 wrapped-text identity x1
E00407     4 members  from  4 pool2 entries [E00430,E00452,E02346,E02368]  CAUSE: layer-3 wrapped-text identity x6
E00408     4 members  from  4 pool2 entries [E00431,E00456,E02347,E02372]  CAUSE: layer-3 wrapped-text identity x6
E00411    24 members  from 23 pool2 entries [E00436,E00440,E00442,E00445,E00450,E00477,E00487,E00491,E00497,E00507,E02350,E02353,E02356,E02358,E02361,E02366,E02380,E02392,E02398,E02402,E02408,E02419,E02421]  CAUSE: layer-3 wrapped-text identity x275
E00412    16 members  from 16 pool2 entries [E00437,E00439,E00443,E00444,E00480,E00485,E00493,E00495,E02354,E02355,E02359,E02360,E02394,E02396,E02404,E02406]  CAUSE: layer-3 wrapped-text identity x120
E00414     6 members  from  6 pool2 entries [E00447,E00501,E02351,E02363,E02382,E02412]  CAUSE: layer-3 wrapped-text identity x15
E00415     8 members  from  8 pool2 entries [E00448,E00449,E00503,E00505,E02364,E02365,E02414,E02417]  CAUSE: layer-3 wrapped-text identity x28
E00416     4 members  from  4 pool2 entries [E00453,E00464,E02369,E02386]  CAUSE: layer-3 wrapped-text identity x6
E00417     4 members  from  4 pool2 entries [E00454,E00470,E02370,E02389]  CAUSE: layer-3 wrapped-text identity x6
E00418     4 members  from  4 pool2 entries [E00457,E00465,E02373,E02387]  CAUSE: layer-3 wrapped-text identity x6
E00419     4 members  from  4 pool2 entries [E00458,E00471,E02374,E02390]  CAUSE: layer-3 wrapped-text identity x6
E00420     2 members  from  2 pool2 entries [E00463,E02385]  CAUSE: layer-3 wrapped-text identity x1
E00423     2 members  from  2 pool2 entries [E00468,E02388]  CAUSE: layer-3 wrapped-text identity x1
E00431    10 members  from 10 pool2 entries [E00508,E00566,E00568,E00601,E00611,E02478,E02480,E02486,E02502,E02512]  CAUSE: layer-3 wrapped-text identity x45
E00432    10 members  from 10 pool2 entries [E00509,E00567,E00569,E00602,E00612,E02479,E02481,E02487,E02503,E02513]  CAUSE: layer-3 wrapped-text identity x45
E00434    10 members  from 10 pool2 entries [E00511,E00516,E00517,E00524,E00529,E02426,E02427,E02430,E02437,E02442]  CAUSE: layer-3 wrapped-text identity x45
E00435     3 members  from  3 pool2 entries [E00512,E02422,E05068]  CAUSE: layer-3 wrapped-text identity x3
E00436     2 members  from  2 pool2 entries [E00513,E02423]  CAUSE: layer-3 wrapped-text identity x1
E00437     2 members  from  2 pool2 entries [E00514,E02424]  CAUSE: layer-3 wrapped-text identity x1
E00438     2 members  from  2 pool2 entries [E00515,E02425]  CAUSE: layer-3 wrapped-text identity x1
E00439     2 members  from  2 pool2 entries [E00518,E02431]  CAUSE: layer-3 wrapped-text identity x1
E00440     2 members  from  2 pool2 entries [E00519,E02432]  CAUSE: layer-3 wrapped-text identity x1
E00441    12 members  from 11 pool2 entries [E00520,E00523,E00525,E00528,E00533,E02428,E02433,E02436,E02438,E02441,E02446]  CAUSE: layer-3 wrapped-text identity x65
E00442     8 members  from  8 pool2 entries [E00521,E00522,E00526,E00527,E02434,E02435,E02439,E02440]  CAUSE: layer-3 wrapped-text identity x28
E00443     3 members  from  3 pool2 entries [E00530,E02429,E02443]  CAUSE: layer-3 wrapped-text identity x3
E00444     4 members  from  4 pool2 entries [E00531,E00532,E02444,E02445]  CAUSE: layer-3 wrapped-text identity x6
E00445    10 members  from 10 pool2 entries [E00534,E00539,E00540,E00548,E00553,E02451,E02452,E02455,E02460,E02465]  CAUSE: layer-3 wrapped-text identity x45
E00446     2 members  from  2 pool2 entries [E00535,E02447]  CAUSE: layer-3 wrapped-text identity x1
E00447     2 members  from  2 pool2 entries [E00536,E02448]  CAUSE: layer-3 wrapped-text identity x1
E00448     2 members  from  2 pool2 entries [E00537,E02449]  CAUSE: layer-3 wrapped-text identity x1
E00449     2 members  from  2 pool2 entries [E00538,E02450]  CAUSE: layer-3 wrapped-text identity x1
E00452    12 members  from 11 pool2 entries [E00543,E00547,E00549,E00552,E00557,E02453,E02456,E02459,E02461,E02464,E02469]  CAUSE: layer-3 wrapped-text identity x65
E00453     8 members  from  8 pool2 entries [E00544,E00546,E00550,E00551,E02457,E02458,E02462,E02463]  CAUSE: layer-3 wrapped-text identity x28
E00455     3 members  from  3 pool2 entries [E00554,E02454,E02466]  CAUSE: layer-3 wrapped-text identity x3
E00456     4 members  from  4 pool2 entries [E00555,E00556,E02467,E02468]  CAUSE: layer-3 wrapped-text identity x6
E00457     2 members  from  2 pool2 entries [E00558,E02470]  CAUSE: layer-3 wrapped-text identity x1
E00458     2 members  from  2 pool2 entries [E00559,E02471]  CAUSE: layer-3 wrapped-text identity x1
E00459     2 members  from  2 pool2 entries [E00560,E02472]  CAUSE: layer-3 wrapped-text identity x1
E00460     2 members  from  2 pool2 entries [E00561,E02473]  CAUSE: layer-3 wrapped-text identity x1
E00461     2 members  from  2 pool2 entries [E00562,E02474]  CAUSE: layer-3 wrapped-text identity x1
E00462     2 members  from  2 pool2 entries [E00563,E02475]  CAUSE: layer-3 wrapped-text identity x1
E00463     2 members  from  2 pool2 entries [E00564,E02476]  CAUSE: layer-3 wrapped-text identity x1
E00464     2 members  from  2 pool2 entries [E00565,E02477]  CAUSE: layer-3 wrapped-text identity x1
E00465     2 members  from  2 pool2 entries [E00570,E02488]  CAUSE: layer-3 wrapped-text identity x1
E00467     2 members  from  2 pool2 entries [E00572,E02489]  CAUSE: layer-3 wrapped-text identity x1
E00468     2 members  from  2 pool2 entries [E00573,E02490]  CAUSE: layer-3 wrapped-text identity x1
E00471     2 members  from  2 pool2 entries [E00576,E02491]  CAUSE: layer-3 wrapped-text identity x1
E00473     2 members  from  2 pool2 entries [E00578,E02492]  CAUSE: layer-3 wrapped-text identity x1
E00474     2 members  from  2 pool2 entries [E00579,E02493]  CAUSE: layer-3 wrapped-text identity x1
E00477    12 members  from 12 pool2 entries [E00583,E00599,E00603,E00609,E00623,E02482,E02494,E02500,E02504,E02510,E02520,E02522]  CAUSE: layer-3 wrapped-text identity x66
E00478    12 members  from 12 pool2 entries [E00584,E00600,E00604,E00610,E00624,E02483,E02495,E02501,E02505,E02511,E02521,E02523]  CAUSE: layer-3 wrapped-text identity x66
E00480     8 members  from  8 pool2 entries [E00586,E00597,E00605,E00607,E02496,E02498,E02506,E02508]  CAUSE: layer-3 wrapped-text identity x28
E00481     8 members  from  8 pool2 entries [E00587,E00598,E00606,E00608,E02497,E02499,E02507,E02509]  CAUSE: layer-3 wrapped-text identity x28
E00491     3 members  from  3 pool2 entries [E00613,E02484,E02514]  CAUSE: layer-3 wrapped-text identity x3
E00492     3 members  from  3 pool2 entries [E00614,E02485,E02515]  CAUSE: layer-3 wrapped-text identity x3
E00496     4 members  from  4 pool2 entries [E00618,E00621,E02516,E02518]  CAUSE: layer-3 wrapped-text identity x6
E00497     4 members  from  4 pool2 entries [E00619,E00622,E02517,E02519]  CAUSE: layer-3 wrapped-text identity x6
E00499    10 members  from 10 pool2 entries [E00625,E00688,E00690,E00719,E00729,E02580,E02582,E02588,E02604,E02614]  CAUSE: layer-3 wrapped-text identity x45
E00500    10 members  from 10 pool2 entries [E00626,E00689,E00691,E00720,E00730,E02581,E02583,E02589,E02605,E02615]  CAUSE: layer-3 wrapped-text identity x45
E00502    10 members  from 10 pool2 entries [E00628,E00633,E00634,E00641,E00646,E02528,E02529,E02532,E02539,E02544]  CAUSE: layer-3 wrapped-text identity x45
E00503     3 members  from  3 pool2 entries [E00629,E02524,E05017]  CAUSE: layer-3 wrapped-text identity x3
E00504     2 members  from  2 pool2 entries [E00630,E02525]  CAUSE: layer-3 wrapped-text identity x1
E00505     4 members  from  4 pool2 entries [E00631,E00675,E02526,E02572]  CAUSE: layer-3 wrapped-text identity x6
E00506     4 members  from  4 pool2 entries [E00632,E00684,E02527,E02576]  CAUSE: layer-3 wrapped-text identity x6
E00507     2 members  from  2 pool2 entries [E00635,E02533]  CAUSE: layer-3 wrapped-text identity x1
E00508     2 members  from  2 pool2 entries [E00636,E02534]  CAUSE: layer-3 wrapped-text identity x1
E00509    24 members  from 23 pool2 entries [E00637,E00640,E00642,E00645,E00650,E00705,E00717,E00721,E00727,E00739,E02530,E02535,E02538,E02540,E02543,E02548,E02584,E02596,E02602,E02606,E02612,E02622,E02624]  CAUSE: layer-3 wrapped-text identity x275
E00510    16 members  from 16 pool2 entries [E00638,E00639,E00643,E00644,E00708,E00715,E00723,E00725,E02536,E02537,E02541,E02542,E02598,E02600,E02608,E02610]  CAUSE: layer-3 wrapped-text identity x120
E00511     6 members  from  6 pool2 entries [E00647,E00732,E02531,E02545,E02586,E02616]  CAUSE: layer-3 wrapped-text identity x15
E00512     8 members  from  8 pool2 entries [E00648,E00649,E00734,E00737,E02546,E02547,E02618,E02620]  CAUSE: layer-3 wrapped-text identity x28
E00513    10 members  from 10 pool2 entries [E00651,E00656,E00657,E00665,E00670,E02553,E02554,E02557,E02562,E02567]  CAUSE: layer-3 wrapped-text identity x45
E00514     2 members  from  2 pool2 entries [E00652,E02549]  CAUSE: layer-3 wrapped-text identity x1
E00515     2 members  from  2 pool2 entries [E00653,E02550]  CAUSE: layer-3 wrapped-text identity x1
E00516     4 members  from  4 pool2 entries [E00654,E00676,E02551,E02573]  CAUSE: layer-3 wrapped-text identity x6
E00517     4 members  from  4 pool2 entries [E00655,E00685,E02552,E02577]  CAUSE: layer-3 wrapped-text identity x6
E00520    24 members  from 23 pool2 entries [E00660,E00664,E00666,E00669,E00674,E00706,E00718,E00722,E00728,E00740,E02555,E02558,E02561,E02563,E02566,E02571,E02585,E02597,E02603,E02607,E02613,E02623,E02625]  CAUSE: layer-3 wrapped-text identity x275
E00521    16 members  from 16 pool2 entries [E00661,E00663,E00667,E00668,E00709,E00716,E00724,E00726,E02559,E02560,E02564,E02565,E02599,E02601,E02609,E02611]  CAUSE: layer-3 wrapped-text identity x120
E00523     6 members  from  6 pool2 entries [E00671,E00733,E02556,E02568,E02587,E02617]  CAUSE: layer-3 wrapped-text identity x15
E00524     8 members  from  8 pool2 entries [E00672,E00673,E00735,E00738,E02569,E02570,E02619,E02621]  CAUSE: layer-3 wrapped-text identity x28
E00527     4 members  from  4 pool2 entries [E00679,E00695,E02574,E02591]  CAUSE: layer-3 wrapped-text identity x6
E00528     4 members  from  4 pool2 entries [E00680,E00701,E02575,E02594]  CAUSE: layer-3 wrapped-text identity x6
E00532     4 members  from  4 pool2 entries [E00686,E00696,E02578,E02592]  CAUSE: layer-3 wrapped-text identity x6
E00533     4 members  from  4 pool2 entries [E00687,E00702,E02579,E02595]  CAUSE: layer-3 wrapped-text identity x6
E00535     2 members  from  2 pool2 entries [E00693,E02590]  CAUSE: layer-3 wrapped-text identity x1
E00539     2 members  from  2 pool2 entries [E00699,E02593]  CAUSE: layer-3 wrapped-text identity x1
E00551    10 members  from 10 pool2 entries [E00741,E00836,E00840,E00883,E00903,E02722,E02726,E02738,E02764,E02784]  CAUSE: layer-3 wrapped-text identity x45
E00552    10 members  from 10 pool2 entries [E00742,E00837,E00841,E00884,E00904,E02723,E02727,E02739,E02765,E02785]  CAUSE: layer-3 wrapped-text identity x45
E00553    12 members  from 12 pool2 entries [E00743,E00838,E00905,E00910,E00927,E02724,E02732,E02736,E02740,E02786,E02790,E02802]  CAUSE: layer-3 wrapped-text identity x66
E00554    12 members  from 12 pool2 entries [E00744,E00839,E00906,E00911,E00928,E02725,E02733,E02737,E02741,E02787,E02791,E02803]  CAUSE: layer-3 wrapped-text identity x66
E00557    10 members  from 10 pool2 entries [E00747,E00752,E00753,E00760,E00765,E02630,E02631,E02634,E02641,E02646]  CAUSE: layer-3 wrapped-text identity x45
E00558     3 members  from  3 pool2 entries [E00748,E02626,E05030]  CAUSE: layer-3 wrapped-text identity x3
E00559     2 members  from  2 pool2 entries [E00749,E02627]  CAUSE: layer-3 wrapped-text identity x1
E00560     2 members  from  2 pool2 entries [E00750,E02628]  CAUSE: layer-3 wrapped-text identity x1
E00561     2 members  from  2 pool2 entries [E00751,E02629]  CAUSE: layer-3 wrapped-text identity x1
E00562     2 members  from  2 pool2 entries [E00754,E02635]  CAUSE: layer-3 wrapped-text identity x1
E00563     2 members  from  2 pool2 entries [E00755,E02636]  CAUSE: layer-3 wrapped-text identity x1
E00564    12 members  from 11 pool2 entries [E00756,E00759,E00761,E00764,E00769,E02632,E02637,E02640,E02642,E02645,E02650]  CAUSE: layer-3 wrapped-text identity x65
E00565     8 members  from  8 pool2 entries [E00757,E00758,E00762,E00763,E02638,E02639,E02643,E02644]  CAUSE: layer-3 wrapped-text identity x28
E00566     3 members  from  3 pool2 entries [E00766,E02633,E02647]  CAUSE: layer-3 wrapped-text identity x3
E00567     4 members  from  4 pool2 entries [E00767,E00768,E02648,E02649]  CAUSE: layer-3 wrapped-text identity x6
E00568    10 members  from 10 pool2 entries [E00770,E00775,E00776,E00784,E00789,E02655,E02656,E02659,E02664,E02669]  CAUSE: layer-3 wrapped-text identity x45
E00569     2 members  from  2 pool2 entries [E00771,E02651]  CAUSE: layer-3 wrapped-text identity x1
E00570     2 members  from  2 pool2 entries [E00772,E02652]  CAUSE: layer-3 wrapped-text identity x1
E00571     2 members  from  2 pool2 entries [E00773,E02653]  CAUSE: layer-3 wrapped-text identity x1
E00572     2 members  from  2 pool2 entries [E00774,E02654]  CAUSE: layer-3 wrapped-text identity x1
E00575    12 members  from 11 pool2 entries [E00779,E00783,E00785,E00788,E00793,E02657,E02660,E02663,E02665,E02668,E02673]  CAUSE: layer-3 wrapped-text identity x65
E00576     8 members  from  8 pool2 entries [E00780,E00782,E00786,E00787,E02661,E02662,E02666,E02667]  CAUSE: layer-3 wrapped-text identity x28
E00578     3 members  from  3 pool2 entries [E00790,E02658,E02670]  CAUSE: layer-3 wrapped-text identity x3
E00579     4 members  from  4 pool2 entries [E00791,E00792,E02671,E02672]  CAUSE: layer-3 wrapped-text identity x6
E00580     2 members  from  2 pool2 entries [E00794,E02674]  CAUSE: layer-3 wrapped-text identity x1
E00581     2 members  from  2 pool2 entries [E00795,E02675]  CAUSE: layer-3 wrapped-text identity x1
E00582     2 members  from  2 pool2 entries [E00796,E02676]  CAUSE: layer-3 wrapped-text identity x1
E00583     6 members  from  6 pool2 entries [E00797,E00817,E00818,E02677,E02700,E02701]  CAUSE: layer-3 wrapped-text identity x15
E00584    13 members  from 12 pool2 entries [E00798,E00801,E00804,E00805,E00806,E00809,E02678,E02684,E02687,E02688,E02691,E02697]  CAUSE: layer-3 wrapped-text identity x77
E00585     2 members  from  2 pool2 entries [E00799,E02682]  CAUSE: layer-3 wrapped-text identity x1
E00586     2 members  from  2 pool2 entries [E00800,E02683]  CAUSE: layer-3 wrapped-text identity x1
E00587     8 members  from  8 pool2 entries [E00802,E00803,E00807,E00808,E02685,E02686,E02689,E02690]  CAUSE: layer-3 wrapped-text identity x28
E00588     9 members  from  9 pool2 entries [E00810,E00811,E00814,E02679,E02680,E02681,E02692,E02693,E02696]  CAUSE: layer-3 wrapped-text identity x36
E00589     4 members  from  4 pool2 entries [E00812,E00813,E02694,E02695]  CAUSE: layer-3 wrapped-text identity x6
E00590     2 members  from  2 pool2 entries [E00815,E02698]  CAUSE: layer-3 wrapped-text identity x1
E00591     2 members  from  2 pool2 entries [E00816,E02699]  CAUSE: layer-3 wrapped-text identity x1
E00592    13 members  from 12 pool2 entries [E00819,E00822,E00825,E00826,E00827,E00830,E02702,E02708,E02711,E02712,E02715,E02721]  CAUSE: layer-3 wrapped-text identity x77
E00593     2 members  from  2 pool2 entries [E00820,E02706]  CAUSE: layer-3 wrapped-text identity x1
E00594     2 members  from  2 pool2 entries [E00821,E02707]  CAUSE: layer-3 wrapped-text identity x1
E00595     8 members  from  8 pool2 entries [E00823,E00824,E00828,E00829,E02709,E02710,E02713,E02714]  CAUSE: layer-3 wrapped-text identity x28
E00596     9 members  from  9 pool2 entries [E00831,E00832,E00835,E02703,E02704,E02705,E02716,E02717,E02720]  CAUSE: layer-3 wrapped-text identity x36
E00597     4 members  from  4 pool2 entries [E00833,E00834,E02718,E02719]  CAUSE: layer-3 wrapped-text identity x6
E00598    13 members  from 13 pool2 entries [E00842,E00858,E00881,E00885,E00889,E00901,E02728,E02750,E02762,E02766,E02770,E02782,E02806]  CAUSE: layer-3 wrapped-text identity x78
E00599    13 members  from 13 pool2 entries [E00843,E00859,E00882,E00886,E00890,E00902,E02729,E02751,E02763,E02767,E02771,E02783,E02807]  CAUSE: layer-3 wrapped-text identity x78
E00600     2 members  from  2 pool2 entries [E00844,E02742]  CAUSE: layer-3 wrapped-text identity x1
E00602     2 members  from  2 pool2 entries [E00846,E02743]  CAUSE: layer-3 wrapped-text identity x1
E00603     2 members  from  2 pool2 entries [E00847,E02744]  CAUSE: layer-3 wrapped-text identity x1
E00606     2 members  from  2 pool2 entries [E00850,E02745]  CAUSE: layer-3 wrapped-text identity x1
E00608     2 members  from  2 pool2 entries [E00852,E02746]  CAUSE: layer-3 wrapped-text identity x1
E00609     2 members  from  2 pool2 entries [E00853,E02747]  CAUSE: layer-3 wrapped-text identity x1
E00612    12 members  from 12 pool2 entries [E00856,E00879,E00887,E00899,E00925,E02730,E02748,E02760,E02768,E02780,E02800,E02804]  CAUSE: layer-3 wrapped-text identity x66
E00613    12 members  from 12 pool2 entries [E00857,E00880,E00888,E00900,E00926,E02731,E02749,E02761,E02769,E02781,E02801,E02805]  CAUSE: layer-3 wrapped-text identity x66
E00615     8 members  from  8 pool2 entries [E00861,E00875,E00891,E00895,E02752,E02756,E02772,E02776]  CAUSE: layer-3 wrapped-text identity x28
E00616     8 members  from  8 pool2 entries [E00862,E00876,E00892,E00896,E02753,E02757,E02773,E02777]  CAUSE: layer-3 wrapped-text identity x28
E00617     8 members  from  8 pool2 entries [E00863,E00877,E00893,E00897,E02754,E02758,E02774,E02778]  CAUSE: layer-3 wrapped-text identity x28
E00618     8 members  from  8 pool2 entries [E00864,E00878,E00894,E00898,E02755,E02759,E02775,E02779]  CAUSE: layer-3 wrapped-text identity x28
E00630     3 members  from  3 pool2 entries [E00908,E02734,E02788]  CAUSE: layer-3 wrapped-text identity x3
E00631     3 members  from  3 pool2 entries [E00909,E02735,E02789]  CAUSE: layer-3 wrapped-text identity x3
E00635     4 members  from  4 pool2 entries [E00915,E00921,E02792,E02796]  CAUSE: layer-3 wrapped-text identity x6
E00636     4 members  from  4 pool2 entries [E00916,E00922,E02793,E02797]  CAUSE: layer-3 wrapped-text identity x6
E00637     4 members  from  4 pool2 entries [E00917,E00923,E02794,E02798]  CAUSE: layer-3 wrapped-text identity x6
E00638     4 members  from  4 pool2 entries [E00918,E00924,E02795,E02799]  CAUSE: layer-3 wrapped-text identity x6
E00642    12 members  from 12 pool2 entries [E00930,E00967,E00990,E00993,E01000,E02844,E02848,E02850,E02852,E02872,E02874,E02880]  CAUSE: layer-3 wrapped-text identity x66
E00643    12 members  from 12 pool2 entries [E00931,E00968,E00991,E00994,E01001,E02845,E02849,E02851,E02853,E02873,E02875,E02881]  CAUSE: layer-3 wrapped-text identity x66
E00645     2 members  from  2 pool2 entries [E00933,E02808]  CAUSE: layer-3 wrapped-text identity x1
E00646     6 members  from  6 pool2 entries [E00934,E00950,E00951,E02809,E02826,E02827]  CAUSE: layer-3 wrapped-text identity x15
E00647    13 members  from 11 pool2 entries [E00935,E00936,E00939,E00940,E00941,E00944,E02810,E02814,E02817,E02819,E02825]  CAUSE: layer-3 wrapped-text identity x76
E00648     8 members  from  7 pool2 entries [E00937,E00938,E00942,E00943,E02815,E02816,E02818]  CAUSE: layer-3 wrapped-text identity x27
E00649     9 members  from  9 pool2 entries [E00945,E00946,E00949,E02811,E02812,E02813,E02820,E02821,E02824]  CAUSE: layer-3 wrapped-text identity x36
E00650     4 members  from  4 pool2 entries [E00947,E00948,E02822,E02823]  CAUSE: layer-3 wrapped-text identity x6
E00651    13 members  from 11 pool2 entries [E00952,E00953,E00956,E00957,E00958,E00961,E02828,E02832,E02835,E02837,E02843]  CAUSE: layer-3 wrapped-text identity x76
E00652     8 members  from  7 pool2 entries [E00954,E00955,E00959,E00960,E02833,E02834,E02836]  CAUSE: layer-3 wrapped-text identity x27
E00653     9 members  from  9 pool2 entries [E00962,E00963,E00966,E02829,E02830,E02831,E02838,E02839,E02842]  CAUSE: layer-3 wrapped-text identity x36
E00654     4 members  from  4 pool2 entries [E00964,E00965,E02840,E02841]  CAUSE: layer-3 wrapped-text identity x6
E00655    13 members  from 13 pool2 entries [E00969,E00971,E00978,E00980,E00982,E00988,E02846,E02854,E02860,E02862,E02864,E02870,E02882]  CAUSE: layer-3 wrapped-text identity x78
E00656    13 members  from 13 pool2 entries [E00970,E00972,E00979,E00981,E00983,E00989,E02847,E02855,E02861,E02863,E02865,E02871,E02883]  CAUSE: layer-3 wrapped-text identity x78
E00657     8 members  from  8 pool2 entries [E00973,E00976,E00984,E00986,E02856,E02858,E02866,E02868]  CAUSE: layer-3 wrapped-text identity x28
E00658     8 members  from  8 pool2 entries [E00974,E00977,E00985,E00987,E02857,E02859,E02867,E02869]  CAUSE: layer-3 wrapped-text identity x28
E00661     4 members  from  4 pool2 entries [E00995,E00998,E02876,E02878]  CAUSE: layer-3 wrapped-text identity x6
E00662     4 members  from  4 pool2 entries [E00996,E00999,E02877,E02879]  CAUSE: layer-3 wrapped-text identity x6
E00665     4 members  from  4 pool2 entries [E01003,E01010,E01016,E01083]  CAUSE: layer-3 wrapped-text identity x6
E00667     4 members  from  4 pool2 entries [E01005,E01046,E01052,E01084]  CAUSE: layer-3 wrapped-text identity x6
E00675     2 members  from  2 pool2 entries [E01014,E01015]  CAUSE: layer-3 wrapped-text identity x1
E00676     2 members  from  2 pool2 entries [E01017,E01025]  CAUSE: layer-3 wrapped-text identity x1
E00679     5 members  from  5 pool2 entries [E01020,E01026,E01030,E01031,E01034]  CAUSE: layer-3 wrapped-text identity x10
E00680     6 members  from  6 pool2 entries [E01021,E01023,E01027,E01028,E01032,E01033]  CAUSE: layer-3 wrapped-text identity x15
E00682     2 members  from  2 pool2 entries [E01024,E01029]  CAUSE: layer-3 wrapped-text identity x1
E00689     2 members  from  2 pool2 entries [E01041,E01100]  CAUSE: layer-5 normalized-text identity x1
E00697     2 members  from  2 pool2 entries [E01050,E01051]  CAUSE: layer-3 wrapped-text identity x1
E00698     2 members  from  2 pool2 entries [E01053,E01061]  CAUSE: layer-3 wrapped-text identity x1
E00701     5 members  from  5 pool2 entries [E01056,E01062,E01066,E01067,E01070]  CAUSE: layer-3 wrapped-text identity x10
E00702     6 members  from  6 pool2 entries [E01057,E01059,E01063,E01064,E01068,E01069]  CAUSE: layer-3 wrapped-text identity x15
E00704     2 members  from  2 pool2 entries [E01060,E01065]  CAUSE: layer-3 wrapped-text identity x1
E00705     2 members  from  2 pool2 entries [E01071,E01081]  CAUSE: layer-3 wrapped-text identity x1
E00706     2 members  from  2 pool2 entries [E01072,E01082]  CAUSE: layer-3 wrapped-text identity x1
E00715     2 members  from  2 pool2 entries [E01085,E01130]  CAUSE: layer-3 wrapped-text identity x1
E00716     2 members  from  2 pool2 entries [E01086,E01131]  CAUSE: layer-3 wrapped-text identity x1
E00732     4 members  from  2 pool2 entries [E01103,E01127]  CAUSE: layer-5 normalized-text identity x4
E00733     5 members  from  5 pool2 entries [E01104,E01132,E01140,E01142,E01148]  CAUSE: layer-3 wrapped-text identity x10
E00734     5 members  from  5 pool2 entries [E01105,E01133,E01141,E01143,E01149]  CAUSE: layer-3 wrapped-text identity x10
E00737     6 members  from  6 pool2 entries [E01108,E01123,E01134,E01136,E01144,E01146]  CAUSE: layer-3 wrapped-text identity x15
E00738     6 members  from  6 pool2 entries [E01109,E01124,E01135,E01137,E01145,E01147]  CAUSE: layer-3 wrapped-text identity x15
E00752     2 members  from  2 pool2 entries [E01125,E01138]  CAUSE: layer-3 wrapped-text identity x1
E00754     2 members  from  2 pool2 entries [E01126,E01139]  CAUSE: layer-3 wrapped-text identity x1
E00757     4 members  from  4 pool2 entries [E01150,E01157,E01163,E01230]  CAUSE: layer-3 wrapped-text identity x6
E00759     4 members  from  4 pool2 entries [E01152,E01193,E01199,E01231]  CAUSE: layer-3 wrapped-text identity x6
E00767     2 members  from  2 pool2 entries [E01161,E01162]  CAUSE: layer-3 wrapped-text identity x1
E00768     2 members  from  2 pool2 entries [E01164,E01172]  CAUSE: layer-3 wrapped-text identity x1
E00771     5 members  from  5 pool2 entries [E01167,E01173,E01177,E01178,E01181]  CAUSE: layer-3 wrapped-text identity x10
E00772     6 members  from  6 pool2 entries [E01168,E01170,E01174,E01175,E01179,E01180]  CAUSE: layer-3 wrapped-text identity x15
E00774     2 members  from  2 pool2 entries [E01171,E01176]  CAUSE: layer-3 wrapped-text identity x1
E00789     2 members  from  2 pool2 entries [E01197,E01198]  CAUSE: layer-3 wrapped-text identity x1
E00790     2 members  from  2 pool2 entries [E01200,E01208]  CAUSE: layer-3 wrapped-text identity x1
E00793     5 members  from  5 pool2 entries [E01203,E01209,E01213,E01214,E01217]  CAUSE: layer-3 wrapped-text identity x10
E00794     6 members  from  6 pool2 entries [E01204,E01206,E01210,E01211,E01215,E01216]  CAUSE: layer-3 wrapped-text identity x15
E00796     2 members  from  2 pool2 entries [E01207,E01212]  CAUSE: layer-3 wrapped-text identity x1
E00797     2 members  from  2 pool2 entries [E01218,E01228]  CAUSE: layer-3 wrapped-text identity x1
E00798     2 members  from  2 pool2 entries [E01219,E01229]  CAUSE: layer-3 wrapped-text identity x1
E00807     2 members  from  2 pool2 entries [E01232,E01276]  CAUSE: layer-3 wrapped-text identity x1
E00808     2 members  from  2 pool2 entries [E01233,E01277]  CAUSE: layer-3 wrapped-text identity x1
E00811     4 members  from  2 pool2 entries [E01236,E01247]  CAUSE: layer-5 normalized-text identity x4
E00825     4 members  from  2 pool2 entries [E01249,E01273]  CAUSE: layer-5 normalized-text identity x2
E00826     5 members  from  5 pool2 entries [E01250,E01278,E01286,E01288,E01294]  CAUSE: layer-3 wrapped-text identity x10
E00827     5 members  from  5 pool2 entries [E01251,E01279,E01287,E01289,E01295]  CAUSE: layer-3 wrapped-text identity x10
E00830     6 members  from  6 pool2 entries [E01254,E01269,E01280,E01282,E01290,E01292]  CAUSE: layer-3 wrapped-text identity x15
E00831     6 members  from  6 pool2 entries [E01255,E01270,E01281,E01283,E01291,E01293]  CAUSE: layer-3 wrapped-text identity x15
E00845     2 members  from  2 pool2 entries [E01271,E01284]  CAUSE: layer-3 wrapped-text identity x1
E00846     2 members  from  2 pool2 entries [E01272,E01285]  CAUSE: layer-3 wrapped-text identity x1
E00851    44 members  from 41 pool2 entries [E01298,E01304,E01310,E01311,E01314,E01318,E01319,E01320,E01323,E01324,E01328,E01396,E01399,E01414,E01433,E01436,E01439,E01448,E01451,E01463,E03197,E03198,E03199,E03201,E03204,E03208,E03209,E03212,E03213,E03279,E03283,E03286,E03294,E03307,E03323,E03326,E03329,E03338,E03341,E03353,E03356]  CAUSE: layer-3 wrapped-text identity x943
E00852    44 members  from 41 pool2 entries [E01299,E01329,E01335,E01336,E01339,E01343,E01344,E01345,E01348,E01349,E01353,E01397,E01400,E01415,E01434,E01437,E01440,E01449,E01452,E01464,E03221,E03222,E03223,E03225,E03226,E03230,E03231,E03234,E03235,E03280,E03284,E03287,E03295,E03308,E03324,E03327,E03330,E03339,E03342,E03354,E03357]  CAUSE: layer-3 wrapped-text identity x943
E00853    20 members  from 20 pool2 entries [E01300,E01354,E01360,E01361,E01364,E01368,E01369,E01370,E01373,E01374,E01378,E01398,E01401,E01416,E01435,E01438,E01441,E01450,E01453,E01465]  CAUSE: layer-3 wrapped-text identity x190
E00857     3 members  from  3 pool2 entries [E01305,E03192,E05137]  CAUSE: layer-3 wrapped-text identity x3
E00858     2 members  from  2 pool2 entries [E01306,E03193]  CAUSE: layer-3 wrapped-text identity x1
E00860     4 members  from  4 pool2 entries [E01308,E01380,E03195,E03267]  CAUSE: layer-3 wrapped-text identity x6
E00861     4 members  from  4 pool2 entries [E01309,E01390,E03196,E03273]  CAUSE: layer-3 wrapped-text identity x6
E00862     2 members  from  2 pool2 entries [E01312,E03202]  CAUSE: layer-3 wrapped-text identity x1
E00863     2 members  from  2 pool2 entries [E01313,E03203]  CAUSE: layer-3 wrapped-text identity x1
E00864    16 members  from 16 pool2 entries [E01315,E01317,E01321,E01322,E01418,E01430,E01442,E01445,E03205,E03207,E03210,E03211,E03310,E03320,E03332,E03335]  CAUSE: layer-3 wrapped-text identity x120
E00865     2 members  from  2 pool2 entries [E01316,E01423]  CAUSE: layer-3 wrapped-text identity x1
E00866     6 members  from  6 pool2 entries [E01325,E01454,E03200,E03214,E03290,E03344]  CAUSE: layer-3 wrapped-text identity x15
E00867     8 members  from  8 pool2 entries [E01326,E01327,E01457,E01460,E03215,E03216,E03347,E03350]  CAUSE: layer-3 wrapped-text identity x28
E00868     2 members  from  2 pool2 entries [E01330,E03217]  CAUSE: layer-3 wrapped-text identity x1
E00871     4 members  from  4 pool2 entries [E01333,E01381,E03219,E03268]  CAUSE: layer-3 wrapped-text identity x6
E00872     4 members  from  4 pool2 entries [E01334,E01391,E03220,E03274]  CAUSE: layer-3 wrapped-text identity x6
E00875    16 members  from 16 pool2 entries [E01340,E01342,E01346,E01347,E01419,E01431,E01443,E01446,E03227,E03229,E03232,E03233,E03311,E03321,E03333,E03336]  CAUSE: layer-3 wrapped-text identity x120
E00877     6 members  from  6 pool2 entries [E01350,E01455,E03224,E03236,E03291,E03345]  CAUSE: layer-3 wrapped-text identity x15
E00878     8 members  from  8 pool2 entries [E01351,E01352,E01458,E01461,E03237,E03238,E03348,E03351]  CAUSE: layer-3 wrapped-text identity x28
E00882     2 members  from  2 pool2 entries [E01358,E01382]  CAUSE: layer-3 wrapped-text identity x1
E00883     2 members  from  2 pool2 entries [E01359,E01392]  CAUSE: layer-3 wrapped-text identity x1
E00886     8 members  from  8 pool2 entries [E01365,E01367,E01371,E01372,E01420,E01432,E01444,E01447]  CAUSE: layer-3 wrapped-text identity x28
E00887     2 members  from  2 pool2 entries [E01366,E01424]  CAUSE: layer-3 wrapped-text identity x1
E00888     2 members  from  2 pool2 entries [E01375,E01456]  CAUSE: layer-3 wrapped-text identity x1
E00889     4 members  from  4 pool2 entries [E01376,E01377,E01459,E01462]  CAUSE: layer-3 wrapped-text identity x6
E00893     4 members  from  4 pool2 entries [E01385,E01404,E03270,E03299]  CAUSE: layer-3 wrapped-text identity x6
E00894     4 members  from  4 pool2 entries [E01386,E01410,E03271,E03304]  CAUSE: layer-3 wrapped-text identity x6
E00896     2 members  from  2 pool2 entries [E01388,E01425]  CAUSE: layer-3 wrapped-text identity x1
E00898     4 members  from  4 pool2 entries [E01393,E01405,E03276,E03300]  CAUSE: layer-3 wrapped-text identity x6
E00899     4 members  from  4 pool2 entries [E01394,E01411,E03277,E03305]  CAUSE: layer-3 wrapped-text identity x6
E00900     2 members  from  2 pool2 entries [E01395,E01426]  CAUSE: layer-3 wrapped-text identity x1
E00901     2 members  from  2 pool2 entries [E01402,E03297]  CAUSE: layer-3 wrapped-text identity x1
E00905     2 members  from  2 pool2 entries [E01408,E03302]  CAUSE: layer-3 wrapped-text identity x1
E00915    68 members  from 65 pool2 entries [E01466,E01472,E01478,E01479,E01482,E01486,E01487,E01488,E01491,E01492,E01496,E01564,E01567,E01582,E01601,E01604,E01607,E01616,E01619,E01632,E03364,E03365,E03366,E03368,E03371,E03375,E03376,E03379,E03380,E03446,E03450,E03453,E03461,E03475,E03491,E03494,E03497,E03506,E03509,E03521,E03524,E04641,E04642,E04643,E04645,E04648,E04652,E04653,E04654,E04657,E04658,E04662,E04663,E04728,E04731,E04734,E04740,E04751,E04764,E04767,E04770,E04779,E04782,E04794,E04797]  CAUSE: layer-3 wrapped-text identity x2275
E00916    68 members  from 65 pool2 entries [E01467,E01497,E01503,E01504,E01507,E01511,E01512,E01513,E01516,E01517,E01521,E01565,E01568,E01583,E01602,E01605,E01608,E01617,E01620,E01633,E03388,E03389,E03390,E03392,E03393,E03397,E03398,E03401,E03402,E03447,E03451,E03454,E03462,E03476,E03492,E03495,E03498,E03507,E03510,E03522,E03525,E04668,E04669,E04670,E04672,E04673,E04676,E04677,E04678,E04681,E04682,E04686,E04687,E04729,E04732,E04735,E04741,E04752,E04765,E04768,E04771,E04780,E04783,E04795,E04798]  CAUSE: layer-3 wrapped-text identity x2275
E00917    20 members  from 20 pool2 entries [E01468,E01522,E01528,E01529,E01532,E01536,E01537,E01538,E01541,E01542,E01546,E01566,E01569,E01584,E01603,E01606,E01609,E01618,E01621,E01634]  CAUSE: layer-3 wrapped-text identity x190
E00921     4 members  from  4 pool2 entries [E01473,E03359,E04636,E05135]  CAUSE: layer-3 wrapped-text identity x6
E00922     3 members  from  3 pool2 entries [E01474,E03360,E04637]  CAUSE: layer-3 wrapped-text identity x3
E00924     6 members  from  6 pool2 entries [E01476,E01548,E03362,E03434,E04639,E04716]  CAUSE: layer-3 wrapped-text identity x15
E00925     6 members  from  6 pool2 entries [E01477,E01558,E03363,E03440,E04640,E04722]  CAUSE: layer-3 wrapped-text identity x15
E00926     3 members  from  3 pool2 entries [E01480,E03369,E04646]  CAUSE: layer-3 wrapped-text identity x3
E00927     3 members  from  3 pool2 entries [E01481,E03370,E04647]  CAUSE: layer-3 wrapped-text identity x3
E00928    24 members  from 24 pool2 entries [E01483,E01485,E01489,E01490,E01586,E01598,E01610,E01613,E03372,E03374,E03377,E03378,E03478,E03488,E03500,E03503,E04649,E04651,E04655,E04656,E04754,E04761,E04773,E04776]  CAUSE: layer-3 wrapped-text identity x276
E00929     2 members  from  2 pool2 entries [E01484,E01591]  CAUSE: layer-3 wrapped-text identity x1
E00930    10 members  from 10 pool2 entries [E01493,E01622,E03367,E03381,E03457,E03512,E04644,E04659,E04737,E04785]  CAUSE: layer-3 wrapped-text identity x45
E00931    12 members  from 12 pool2 entries [E01494,E01495,E01625,E01629,E03382,E03383,E03515,E03518,E04660,E04661,E04788,E04791]  CAUSE: layer-3 wrapped-text identity x66
E00932     3 members  from  3 pool2 entries [E01498,E03384,E04664]  CAUSE: layer-3 wrapped-text identity x3
E00935     6 members  from  6 pool2 entries [E01501,E01549,E03386,E03435,E04666,E04717]  CAUSE: layer-3 wrapped-text identity x15
E00936     6 members  from  6 pool2 entries [E01502,E01559,E03387,E03441,E04667,E04723]  CAUSE: layer-3 wrapped-text identity x15
E00939    24 members  from 24 pool2 entries [E01508,E01510,E01514,E01515,E01587,E01599,E01611,E01614,E03394,E03396,E03399,E03400,E03479,E03489,E03501,E03504,E04674,E04675,E04679,E04680,E04755,E04762,E04774,E04777]  CAUSE: layer-3 wrapped-text identity x276
E00941    10 members  from 10 pool2 entries [E01518,E01623,E03391,E03403,E03458,E03513,E04671,E04683,E04738,E04786]  CAUSE: layer-3 wrapped-text identity x45
E00942    12 members  from 12 pool2 entries [E01519,E01520,E01626,E01630,E03404,E03405,E03516,E03519,E04684,E04685,E04789,E04792]  CAUSE: layer-3 wrapped-text identity x66
E00946     2 members  from  2 pool2 entries [E01526,E01550]  CAUSE: layer-3 wrapped-text identity x1
E00947     2 members  from  2 pool2 entries [E01527,E01560]  CAUSE: layer-3 wrapped-text identity x1
E00950     8 members  from  8 pool2 entries [E01533,E01535,E01539,E01540,E01588,E01600,E01612,E01615]  CAUSE: layer-3 wrapped-text identity x28
E00951     2 members  from  2 pool2 entries [E01534,E01592]  CAUSE: layer-3 wrapped-text identity x1
E00952     2 members  from  2 pool2 entries [E01543,E01624]  CAUSE: layer-3 wrapped-text identity x1
E00953     4 members  from  4 pool2 entries [E01544,E01545,E01627,E01631]  CAUSE: layer-3 wrapped-text identity x6
E00957     6 members  from  6 pool2 entries [E01553,E01572,E03437,E03466,E04719,E04745]  CAUSE: layer-3 wrapped-text identity x15
E00958     6 members  from  6 pool2 entries [E01554,E01578,E03438,E03471,E04720,E04749]  CAUSE: layer-3 wrapped-text identity x15
E00960     2 members  from  2 pool2 entries [E01556,E01593]  CAUSE: layer-3 wrapped-text identity x1
E00962     6 members  from  6 pool2 entries [E01561,E01573,E03443,E03467,E04725,E04746]  CAUSE: layer-3 wrapped-text identity x15
E00963     6 members  from  6 pool2 entries [E01562,E01579,E03444,E03472,E04726,E04750]  CAUSE: layer-3 wrapped-text identity x15
E00964     2 members  from  2 pool2 entries [E01563,E01594]  CAUSE: layer-3 wrapped-text identity x1
E00965     3 members  from  3 pool2 entries [E01570,E03464,E04743]  CAUSE: layer-3 wrapped-text identity x3
E00969     3 members  from  3 pool2 entries [E01576,E03469,E04747]  CAUSE: layer-3 wrapped-text identity x3
E00979    20 members  from 20 pool2 entries [E01635,E01735,E01738,E01760,E01784,E01787,E01790,E01799,E01803,E01822,E02162,E02168,E02169,E02172,E02176,E02177,E02178,E02181,E02182,E02186]  CAUSE: layer-3 wrapped-text identity x190
E00980    20 members  from 20 pool2 entries [E01636,E01736,E01739,E01761,E01785,E01788,E01791,E01800,E01804,E01823,E02187,E02192,E02193,E02194,E02197,E02198,E02199,E02202,E02203,E02207]  CAUSE: layer-3 wrapped-text identity x190
E00981    20 members  from 20 pool2 entries [E01637,E01737,E01740,E01762,E01786,E01789,E01792,E01801,E01805,E01824,E02208,E02214,E02215,E02218,E02222,E02223,E02224,E02227,E02228,E02232]  CAUSE: layer-3 wrapped-text identity x190
E00986    20 members  from 20 pool2 entries [E01642,E01648,E01649,E01652,E01656,E01657,E01658,E01661,E01662,E01666,E02159,E02245,E02248,E02260,E02274,E02277,E02280,E02289,E02292,E02304]  CAUSE: layer-3 wrapped-text identity x190
E00990     2 members  from  2 pool2 entries [E01646,E02233]  CAUSE: layer-3 wrapped-text identity x1
E00991     2 members  from  2 pool2 entries [E01647,E02239]  CAUSE: layer-3 wrapped-text identity x1
E00994     8 members  from  8 pool2 entries [E01653,E01655,E01659,E01660,E02263,E02271,E02283,E02286]  CAUSE: layer-3 wrapped-text identity x28
E00995     2 members  from  2 pool2 entries [E01654,E02266]  CAUSE: layer-3 wrapped-text identity x1
E00996     2 members  from  2 pool2 entries [E01663,E02295]  CAUSE: layer-3 wrapped-text identity x1
E00997     4 members  from  4 pool2 entries [E01664,E01665,E02298,E02301]  CAUSE: layer-3 wrapped-text identity x6
E00998    20 members  from 20 pool2 entries [E01667,E01673,E01674,E01677,E01681,E01682,E01683,E01686,E01687,E01691,E02160,E02246,E02249,E02261,E02275,E02278,E02281,E02290,E02293,E02305]  CAUSE: layer-3 wrapped-text identity x190
E01002     2 members  from  2 pool2 entries [E01671,E02234]  CAUSE: layer-3 wrapped-text identity x1
E01003     2 members  from  2 pool2 entries [E01672,E02240]  CAUSE: layer-3 wrapped-text identity x1
E01004     3 members  from  2 pool2 entries [E01675,E02252]  CAUSE: layer-5 normalized-text identity x2
E01006     8 members  from  8 pool2 entries [E01678,E01680,E01684,E01685,E02264,E02272,E02284,E02287]  CAUSE: layer-3 wrapped-text identity x28
E01008     2 members  from  2 pool2 entries [E01688,E02296]  CAUSE: layer-3 wrapped-text identity x1
E01009     4 members  from  4 pool2 entries [E01689,E01690,E02299,E02302]  CAUSE: layer-3 wrapped-text identity x6
E01010    20 members  from 20 pool2 entries [E01692,E01698,E01699,E01702,E01706,E01707,E01708,E01711,E01712,E01716,E02161,E02247,E02250,E02262,E02276,E02279,E02282,E02291,E02294,E02306]  CAUSE: layer-3 wrapped-text identity x190
E01014     2 members  from  2 pool2 entries [E01696,E02235]  CAUSE: layer-3 wrapped-text identity x1
E01015     2 members  from  2 pool2 entries [E01697,E02241]  CAUSE: layer-3 wrapped-text identity x1
E01018     8 members  from  8 pool2 entries [E01703,E01705,E01709,E01710,E02265,E02273,E02285,E02288]  CAUSE: layer-3 wrapped-text identity x28
E01019     2 members  from  2 pool2 entries [E01704,E02267]  CAUSE: layer-3 wrapped-text identity x1
E01020     2 members  from  2 pool2 entries [E01713,E02297]  CAUSE: layer-3 wrapped-text identity x1
E01021     4 members  from  4 pool2 entries [E01714,E01715,E02300,E02303]  CAUSE: layer-3 wrapped-text identity x6
E01023     2 members  from  2 pool2 entries [E01718,E02166]  CAUSE: layer-3 wrapped-text identity x1
E01024     2 members  from  2 pool2 entries [E01719,E02190]  CAUSE: layer-3 wrapped-text identity x1
E01025     2 members  from  2 pool2 entries [E01720,E02212]  CAUSE: layer-3 wrapped-text identity x1
E01029     2 members  from  2 pool2 entries [E01724,E02254]  CAUSE: layer-3 wrapped-text identity x1
E01030     2 members  from  2 pool2 entries [E01725,E02258]  CAUSE: layer-3 wrapped-text identity x1
E01032     2 members  from  2 pool2 entries [E01726,E02268]  CAUSE: layer-3 wrapped-text identity x1
E01035     2 members  from  2 pool2 entries [E01728,E02167]  CAUSE: layer-3 wrapped-text identity x1
E01036     2 members  from  2 pool2 entries [E01729,E02191]  CAUSE: layer-3 wrapped-text identity x1
E01037     2 members  from  2 pool2 entries [E01730,E02213]  CAUSE: layer-3 wrapped-text identity x1
E01039     2 members  from  2 pool2 entries [E01732,E02255]  CAUSE: layer-3 wrapped-text identity x1
E01040     2 members  from  2 pool2 entries [E01733,E02259]  CAUSE: layer-3 wrapped-text identity x1
E01042     2 members  from  2 pool2 entries [E01734,E02269]  CAUSE: layer-3 wrapped-text identity x1
E01052     2 members  from  2 pool2 entries [E01749,E02236]  CAUSE: layer-3 wrapped-text identity x1
E01053     2 members  from  2 pool2 entries [E01750,E02242]  CAUSE: layer-3 wrapped-text identity x1
E01059     2 members  from  2 pool2 entries [E01756,E02237]  CAUSE: layer-3 wrapped-text identity x1
E01060     2 members  from  2 pool2 entries [E01757,E02243]  CAUSE: layer-3 wrapped-text identity x1
E01064     8 members  from  8 pool2 entries [E01764,E01781,E01793,E01796,E02173,E02175,E02179,E02180]  CAUSE: layer-3 wrapped-text identity x28
E01065     8 members  from  8 pool2 entries [E01765,E01782,E01794,E01797,E02195,E02196,E02200,E02201]  CAUSE: layer-3 wrapped-text identity x28
E01066     8 members  from  8 pool2 entries [E01766,E01783,E01795,E01798,E02219,E02221,E02225,E02226]  CAUSE: layer-3 wrapped-text identity x28
E01071     2 members  from  2 pool2 entries [E01769,E02174]  CAUSE: layer-3 wrapped-text identity x1
E01073     2 members  from  2 pool2 entries [E01771,E02220]  CAUSE: layer-3 wrapped-text identity x1
E01074     2 members  from  2 pool2 entries [E01772,E02238]  CAUSE: layer-3 wrapped-text identity x1
E01075     2 members  from  2 pool2 entries [E01773,E02244]  CAUSE: layer-3 wrapped-text identity x1
E01087     2 members  from  2 pool2 entries [E01809,E02183]  CAUSE: layer-3 wrapped-text identity x1
E01088     2 members  from  2 pool2 entries [E01810,E02204]  CAUSE: layer-3 wrapped-text identity x1
E01089     2 members  from  2 pool2 entries [E01811,E02229]  CAUSE: layer-3 wrapped-text identity x1
E01093     4 members  from  4 pool2 entries [E01815,E01819,E02184,E02185]  CAUSE: layer-3 wrapped-text identity x6
E01094     4 members  from  4 pool2 entries [E01816,E01820,E02205,E02206]  CAUSE: layer-3 wrapped-text identity x6
E01095     4 members  from  4 pool2 entries [E01817,E01821,E02230,E02231]  CAUSE: layer-3 wrapped-text identity x6
E01099    20 members  from 20 pool2 entries [E01825,E01927,E01930,E01951,E01975,E01978,E01981,E01990,E01993,E02009,E02015,E02021,E02022,E02025,E02029,E02030,E02031,E02034,E02035,E02039]  CAUSE: layer-3 wrapped-text identity x190
E01100    20 members  from 20 pool2 entries [E01826,E01928,E01931,E01952,E01976,E01979,E01982,E01991,E01994,E02010,E02040,E02045,E02046,E02047,E02050,E02051,E02052,E02055,E02056,E02060]  CAUSE: layer-3 wrapped-text identity x190
E01101    20 members  from 20 pool2 entries [E01827,E01929,E01932,E01953,E01977,E01980,E01983,E01992,E01995,E02011,E02061,E02067,E02068,E02071,E02075,E02076,E02077,E02080,E02081,E02085]  CAUSE: layer-3 wrapped-text identity x190
E01108    20 members  from 20 pool2 entries [E01834,E01840,E01841,E01844,E01848,E01849,E01850,E01853,E01854,E01858,E02012,E02098,E02101,E02112,E02126,E02129,E02132,E02141,E02144,E02156]  CAUSE: layer-3 wrapped-text identity x190
E01112     2 members  from  2 pool2 entries [E01838,E02086]  CAUSE: layer-3 wrapped-text identity x1
E01113     2 members  from  2 pool2 entries [E01839,E02092]  CAUSE: layer-3 wrapped-text identity x1
E01116     8 members  from  8 pool2 entries [E01845,E01847,E01851,E01852,E02115,E02123,E02135,E02138]  CAUSE: layer-3 wrapped-text identity x28
E01117     2 members  from  2 pool2 entries [E01846,E02118]  CAUSE: layer-3 wrapped-text identity x1
E01118     2 members  from  2 pool2 entries [E01855,E02147]  CAUSE: layer-3 wrapped-text identity x1
E01119     4 members  from  4 pool2 entries [E01856,E01857,E02150,E02153]  CAUSE: layer-3 wrapped-text identity x6
E01120    20 members  from 20 pool2 entries [E01859,E01865,E01866,E01869,E01873,E01874,E01875,E01878,E01879,E01883,E02013,E02099,E02102,E02113,E02127,E02130,E02133,E02142,E02145,E02157]  CAUSE: layer-3 wrapped-text identity x190
E01122     4 members  from  2 pool2 entries [E01861,E03920]  CAUSE: layer-5 normalized-text identity x3
E01124     2 members  from  2 pool2 entries [E01863,E02087]  CAUSE: layer-3 wrapped-text identity x1
E01125     2 members  from  2 pool2 entries [E01864,E02093]  CAUSE: layer-3 wrapped-text identity x1
E01128     8 members  from  8 pool2 entries [E01870,E01872,E01876,E01877,E02116,E02124,E02136,E02139]  CAUSE: layer-3 wrapped-text identity x28
E01130     2 members  from  2 pool2 entries [E01880,E02148]  CAUSE: layer-3 wrapped-text identity x1
E01131     4 members  from  4 pool2 entries [E01881,E01882,E02151,E02154]  CAUSE: layer-3 wrapped-text identity x6
E01132    20 members  from 20 pool2 entries [E01884,E01890,E01891,E01894,E01898,E01899,E01900,E01903,E01904,E01908,E02014,E02100,E02103,E02114,E02128,E02131,E02134,E02143,E02146,E02158]  CAUSE: layer-3 wrapped-text identity x190
E01136     2 members  from  2 pool2 entries [E01888,E02088]  CAUSE: layer-3 wrapped-text identity x1
E01137     2 members  from  2 pool2 entries [E01889,E02094]  CAUSE: layer-3 wrapped-text identity x1
E01140     8 members  from  8 pool2 entries [E01895,E01897,E01901,E01902,E02117,E02125,E02137,E02140]  CAUSE: layer-3 wrapped-text identity x28
E01141     2 members  from  2 pool2 entries [E01896,E02119]  CAUSE: layer-3 wrapped-text identity x1
E01142     2 members  from  2 pool2 entries [E01905,E02149]  CAUSE: layer-3 wrapped-text identity x1
E01143     4 members  from  4 pool2 entries [E01906,E01907,E02152,E02155]  CAUSE: layer-3 wrapped-text identity x6
E01145     2 members  from  2 pool2 entries [E01910,E02019]  CAUSE: layer-3 wrapped-text identity x1
E01146     2 members  from  2 pool2 entries [E01911,E02043]  CAUSE: layer-3 wrapped-text identity x1
E01147     2 members  from  2 pool2 entries [E01912,E02065]  CAUSE: layer-3 wrapped-text identity x1
E01151     2 members  from  2 pool2 entries [E01916,E02106]  CAUSE: layer-3 wrapped-text identity x1
E01152     2 members  from  2 pool2 entries [E01917,E02110]  CAUSE: layer-3 wrapped-text identity x1
E01154     2 members  from  2 pool2 entries [E01918,E02120]  CAUSE: layer-3 wrapped-text identity x1
E01157     2 members  from  2 pool2 entries [E01920,E02020]  CAUSE: layer-3 wrapped-text identity x1
E01158     2 members  from  2 pool2 entries [E01921,E02044]  CAUSE: layer-3 wrapped-text identity x1
E01159     2 members  from  2 pool2 entries [E01922,E02066]  CAUSE: layer-3 wrapped-text identity x1
E01161     2 members  from  2 pool2 entries [E01924,E02107]  CAUSE: layer-3 wrapped-text identity x1
E01162     2 members  from  2 pool2 entries [E01925,E02111]  CAUSE: layer-3 wrapped-text identity x1
E01164     2 members  from  2 pool2 entries [E01926,E02121]  CAUSE: layer-3 wrapped-text identity x1
E01173     2 members  from  2 pool2 entries [E01940,E02089]  CAUSE: layer-3 wrapped-text identity x1
E01174     2 members  from  2 pool2 entries [E01941,E02095]  CAUSE: layer-3 wrapped-text identity x1
E01180     2 members  from  2 pool2 entries [E01947,E02090]  CAUSE: layer-3 wrapped-text identity x1
E01181     2 members  from  2 pool2 entries [E01948,E02096]  CAUSE: layer-3 wrapped-text identity x1
E01185     8 members  from  8 pool2 entries [E01955,E01972,E01984,E01987,E02026,E02028,E02032,E02033]  CAUSE: layer-3 wrapped-text identity x28
E01186     8 members  from  8 pool2 entries [E01956,E01973,E01985,E01988,E02048,E02049,E02053,E02054]  CAUSE: layer-3 wrapped-text identity x28
E01187     8 members  from  8 pool2 entries [E01957,E01974,E01986,E01989,E02072,E02074,E02078,E02079]  CAUSE: layer-3 wrapped-text identity x28
E01192     2 members  from  2 pool2 entries [E01960,E02027]  CAUSE: layer-3 wrapped-text identity x1
E01194     2 members  from  2 pool2 entries [E01962,E02073]  CAUSE: layer-3 wrapped-text identity x1
E01195     2 members  from  2 pool2 entries [E01963,E02091]  CAUSE: layer-3 wrapped-text identity x1
E01196     2 members  from  2 pool2 entries [E01964,E02097]  CAUSE: layer-3 wrapped-text identity x1
E01204     2 members  from  2 pool2 entries [E01996,E02036]  CAUSE: layer-3 wrapped-text identity x1
E01205     2 members  from  2 pool2 entries [E01997,E02057]  CAUSE: layer-3 wrapped-text identity x1
E01206     2 members  from  2 pool2 entries [E01998,E02082]  CAUSE: layer-3 wrapped-text identity x1
E01210     4 members  from  4 pool2 entries [E02002,E02006,E02037,E02038]  CAUSE: layer-3 wrapped-text identity x6
E01211     4 members  from  4 pool2 entries [E02003,E02007,E02058,E02059]  CAUSE: layer-3 wrapped-text identity x6
E01212     4 members  from  4 pool2 entries [E02004,E02008,E02083,E02084]  CAUSE: layer-3 wrapped-text identity x6
E01292     2 members  from  2 pool2 entries [E02311,E02313]  CAUSE: layer-3 wrapped-text identity x1
E01294     2 members  from  2 pool2 entries [E02884,E04420]  CAUSE: layer-3 wrapped-text identity x1
E01295     2 members  from  2 pool2 entries [E02885,E04421]  CAUSE: layer-3 wrapped-text identity x1
E01296     2 members  from  2 pool2 entries [E02886,E04422]  CAUSE: layer-3 wrapped-text identity x1
E01297     4 members  from  4 pool2 entries [E02887,E02888,E04423,E04424]  CAUSE: layer-3 wrapped-text identity x6
E01298     4 members  from  4 pool2 entries [E02889,E02963,E04425,E04482]  CAUSE: layer-3 wrapped-text identity x6
E01299     4 members  from  4 pool2 entries [E02890,E02901,E04426,E04437]  CAUSE: layer-3 wrapped-text identity x6
E01300    18 members  from 18 pool2 entries [E02891,E02892,E02893,E02896,E02902,E02906,E02907,E02910,E02911,E04427,E04428,E04429,E04432,E04438,E04442,E04443,E04446,E04447]  CAUSE: layer-3 wrapped-text identity x153
E01301     2 members  from  2 pool2 entries [E02894,E04430]  CAUSE: layer-3 wrapped-text identity x1
E01302     2 members  from  2 pool2 entries [E02895,E04431]  CAUSE: layer-3 wrapped-text identity x1
E01303    12 members  from 12 pool2 entries [E02897,E02899,E02903,E02904,E02908,E02909,E04433,E04435,E04439,E04440,E04444,E04445]  CAUSE: layer-3 wrapped-text identity x66
E01304     2 members  from  2 pool2 entries [E02898,E04434]  CAUSE: layer-3 wrapped-text identity x1
E01305     4 members  from  4 pool2 entries [E02900,E02905,E04436,E04441]  CAUSE: layer-3 wrapped-text identity x6
E01306     2 members  from  2 pool2 entries [E02912,E04448]  CAUSE: layer-3 wrapped-text identity x1
E01308     2 members  from  2 pool2 entries [E02914,E04449]  CAUSE: layer-3 wrapped-text identity x1
E01318     2 members  from  2 pool2 entries [E02924,E04450]  CAUSE: layer-3 wrapped-text identity x1
E01319     2 members  from  2 pool2 entries [E02925,E04451]  CAUSE: layer-3 wrapped-text identity x1
E01320     2 members  from  2 pool2 entries [E02926,E04452]  CAUSE: layer-3 wrapped-text identity x1
E01321     4 members  from  4 pool2 entries [E02927,E02928,E04453,E04454]  CAUSE: layer-3 wrapped-text identity x6
E01322     4 members  from  4 pool2 entries [E02929,E02964,E04455,E04483]  CAUSE: layer-3 wrapped-text identity x6
E01323     4 members  from  4 pool2 entries [E02930,E02941,E04456,E04467]  CAUSE: layer-3 wrapped-text identity x6
E01324    18 members  from 18 pool2 entries [E02931,E02932,E02933,E02936,E02942,E02946,E02947,E02950,E02951,E04457,E04458,E04459,E04462,E04468,E04472,E04473,E04476,E04477]  CAUSE: layer-3 wrapped-text identity x153
E01325     2 members  from  2 pool2 entries [E02934,E04460]  CAUSE: layer-3 wrapped-text identity x1
E01326     2 members  from  2 pool2 entries [E02935,E04461]  CAUSE: layer-3 wrapped-text identity x1
E01327    12 members  from 12 pool2 entries [E02937,E02939,E02943,E02944,E02948,E02949,E04463,E04465,E04469,E04470,E04474,E04475]  CAUSE: layer-3 wrapped-text identity x66
E01328     2 members  from  2 pool2 entries [E02938,E04464]  CAUSE: layer-3 wrapped-text identity x1
E01329     4 members  from  4 pool2 entries [E02940,E02945,E04466,E04471]  CAUSE: layer-3 wrapped-text identity x6
E01330     4 members  from  4 pool2 entries [E02952,E02961,E04478,E04480]  CAUSE: layer-3 wrapped-text identity x6
E01331     4 members  from  4 pool2 entries [E02953,E02962,E04479,E04481]  CAUSE: layer-3 wrapped-text identity x6
E01342     4 members  from  4 pool2 entries [E02968,E03014,E04484,E04506]  CAUSE: layer-3 wrapped-text identity x6
E01343     4 members  from  4 pool2 entries [E02969,E03015,E04485,E04507]  CAUSE: layer-3 wrapped-text identity x6
E01350    18 members  from 18 pool2 entries [E02976,E02979,E02982,E02992,E03016,E03024,E03026,E03032,E03034,E04486,E04488,E04490,E04496,E04508,E04516,E04518,E04524,E04526]  CAUSE: layer-3 wrapped-text identity x153
E01351    18 members  from 18 pool2 entries [E02977,E02980,E02983,E02993,E03017,E03025,E03027,E03033,E03035,E04487,E04489,E04491,E04497,E04509,E04517,E04519,E04525,E04527]  CAUSE: layer-3 wrapped-text identity x153
E01354     2 members  from  2 pool2 entries [E02984,E04492]  CAUSE: layer-3 wrapped-text identity x1
E01355     2 members  from  2 pool2 entries [E02985,E04493]  CAUSE: layer-3 wrapped-text identity x1
E01358     2 members  from  2 pool2 entries [E02988,E04494]  CAUSE: layer-3 wrapped-text identity x1
E01359     2 members  from  2 pool2 entries [E02989,E04495]  CAUSE: layer-3 wrapped-text identity x1
E01362    12 members  from 12 pool2 entries [E02994,E03009,E03018,E03020,E03028,E03030,E04498,E04502,E04510,E04512,E04520,E04522]  CAUSE: layer-3 wrapped-text identity x66
E01363    12 members  from 12 pool2 entries [E02995,E03010,E03019,E03021,E03029,E03031,E04499,E04503,E04511,E04513,E04521,E04523]  CAUSE: layer-3 wrapped-text identity x66
E01366     2 members  from  2 pool2 entries [E02998,E04500]  CAUSE: layer-3 wrapped-text identity x1
E01368     2 members  from  2 pool2 entries [E03000,E04501]  CAUSE: layer-3 wrapped-text identity x1
E01377     4 members  from  4 pool2 entries [E03011,E03022,E04504,E04514]  CAUSE: layer-3 wrapped-text identity x6
E01378     4 members  from  4 pool2 entries [E03012,E03023,E04505,E04515]  CAUSE: layer-3 wrapped-text identity x6
E01380     2 members  from  2 pool2 entries [E03036,E04528]  CAUSE: layer-3 wrapped-text identity x1
E01381     2 members  from  2 pool2 entries [E03037,E04529]  CAUSE: layer-3 wrapped-text identity x1
E01382     2 members  from  2 pool2 entries [E03038,E04530]  CAUSE: layer-3 wrapped-text identity x1
E01383     4 members  from  4 pool2 entries [E03039,E03040,E04531,E04532]  CAUSE: layer-3 wrapped-text identity x6
E01384     4 members  from  4 pool2 entries [E03041,E03117,E04533,E04590]  CAUSE: layer-3 wrapped-text identity x6
E01385     4 members  from  4 pool2 entries [E03042,E03053,E04534,E04545]  CAUSE: layer-3 wrapped-text identity x6
E01386    18 members  from 18 pool2 entries [E03043,E03044,E03045,E03048,E03054,E03058,E03059,E03062,E03063,E04535,E04536,E04537,E04540,E04546,E04550,E04551,E04554,E04555]  CAUSE: layer-3 wrapped-text identity x153
E01387     2 members  from  2 pool2 entries [E03046,E04538]  CAUSE: layer-3 wrapped-text identity x1
E01388     2 members  from  2 pool2 entries [E03047,E04539]  CAUSE: layer-3 wrapped-text identity x1
E01389    12 members  from 12 pool2 entries [E03049,E03051,E03055,E03056,E03060,E03061,E04541,E04543,E04547,E04548,E04552,E04553]  CAUSE: layer-3 wrapped-text identity x66
E01390     2 members  from  2 pool2 entries [E03050,E04542]  CAUSE: layer-3 wrapped-text identity x1
E01391     4 members  from  4 pool2 entries [E03052,E03057,E04544,E04549]  CAUSE: layer-3 wrapped-text identity x6
E01392     2 members  from  2 pool2 entries [E03064,E04556]  CAUSE: layer-3 wrapped-text identity x1
E01394     2 members  from  2 pool2 entries [E03066,E04557]  CAUSE: layer-3 wrapped-text identity x1
E01404     2 members  from  2 pool2 entries [E03076,E04558]  CAUSE: layer-3 wrapped-text identity x1
E01405     2 members  from  2 pool2 entries [E03077,E04559]  CAUSE: layer-3 wrapped-text identity x1
E01406     2 members  from  2 pool2 entries [E03078,E04560]  CAUSE: layer-3 wrapped-text identity x1
E01407     4 members  from  4 pool2 entries [E03079,E03080,E04561,E04562]  CAUSE: layer-3 wrapped-text identity x6
E01408     4 members  from  4 pool2 entries [E03081,E03118,E04563,E04591]  CAUSE: layer-3 wrapped-text identity x6
E01409     4 members  from  4 pool2 entries [E03082,E03093,E04564,E04575]  CAUSE: layer-3 wrapped-text identity x6
E01410    18 members  from 18 pool2 entries [E03083,E03084,E03085,E03088,E03094,E03098,E03099,E03102,E03103,E04565,E04566,E04567,E04570,E04576,E04580,E04581,E04584,E04585]  CAUSE: layer-3 wrapped-text identity x153
E01411     2 members  from  2 pool2 entries [E03086,E04568]  CAUSE: layer-3 wrapped-text identity x1
E01412     2 members  from  2 pool2 entries [E03087,E04569]  CAUSE: layer-3 wrapped-text identity x1
E01413    12 members  from 12 pool2 entries [E03089,E03091,E03095,E03096,E03100,E03101,E04571,E04573,E04577,E04578,E04582,E04583]  CAUSE: layer-3 wrapped-text identity x66
E01414     2 members  from  2 pool2 entries [E03090,E04572]  CAUSE: layer-3 wrapped-text identity x1
E01415     4 members  from  4 pool2 entries [E03092,E03097,E04574,E04579]  CAUSE: layer-3 wrapped-text identity x6
E01416     4 members  from  4 pool2 entries [E03104,E03115,E04586,E04588]  CAUSE: layer-3 wrapped-text identity x6
E01417     4 members  from  4 pool2 entries [E03105,E03116,E04587,E04589]  CAUSE: layer-3 wrapped-text identity x6
E01430     4 members  from  4 pool2 entries [E03122,E03170,E04592,E04614]  CAUSE: layer-3 wrapped-text identity x6
E01431     4 members  from  4 pool2 entries [E03123,E03171,E04593,E04615]  CAUSE: layer-3 wrapped-text identity x6
E01439    18 members  from 18 pool2 entries [E03131,E03135,E03137,E03147,E03172,E03180,E03182,E03188,E03190,E04594,E04596,E04598,E04604,E04616,E04624,E04626,E04632,E04634]  CAUSE: layer-3 wrapped-text identity x153
E01440    18 members  from 18 pool2 entries [E03132,E03136,E03138,E03148,E03173,E03181,E03183,E03189,E03191,E04595,E04597,E04599,E04605,E04617,E04625,E04627,E04633,E04635]  CAUSE: layer-3 wrapped-text identity x153
E01443     2 members  from  2 pool2 entries [E03139,E04600]  CAUSE: layer-3 wrapped-text identity x1
E01444     2 members  from  2 pool2 entries [E03140,E04601]  CAUSE: layer-3 wrapped-text identity x1
E01447     2 members  from  2 pool2 entries [E03143,E04602]  CAUSE: layer-3 wrapped-text identity x1
E01448     2 members  from  2 pool2 entries [E03144,E04603]  CAUSE: layer-3 wrapped-text identity x1
E01451    12 members  from 12 pool2 entries [E03149,E03164,E03174,E03176,E03184,E03186,E04606,E04610,E04618,E04620,E04628,E04630]  CAUSE: layer-3 wrapped-text identity x66
E01452    12 members  from 12 pool2 entries [E03150,E03165,E03175,E03177,E03185,E03187,E04607,E04611,E04619,E04621,E04629,E04631]  CAUSE: layer-3 wrapped-text identity x66
E01455     2 members  from  2 pool2 entries [E03153,E04608]  CAUSE: layer-3 wrapped-text identity x1
E01457     2 members  from  2 pool2 entries [E03155,E04609]  CAUSE: layer-3 wrapped-text identity x1
E01466     4 members  from  4 pool2 entries [E03166,E03178,E04612,E04622]  CAUSE: layer-3 wrapped-text identity x6
E01467     4 members  from  4 pool2 entries [E03167,E03179,E04613,E04623]  CAUSE: layer-3 wrapped-text identity x6
E01471     2 members  from  2 pool2 entries [E03206,E03314]  CAUSE: layer-3 wrapped-text identity x1
E01477     2 members  from  2 pool2 entries [E03242,E03269]  CAUSE: layer-3 wrapped-text identity x1
E01478     2 members  from  2 pool2 entries [E03243,E03275]  CAUSE: layer-3 wrapped-text identity x1
E01479    24 members  from 24 pool2 entries [E03244,E03245,E03246,E03248,E03251,E03255,E03256,E03257,E03260,E03261,E03265,E03266,E03281,E03285,E03288,E03296,E03309,E03325,E03328,E03331,E03340,E03343,E03355,E03358]  CAUSE: layer-3 wrapped-text identity x276
E01480     4 members  from  4 pool2 entries [E03247,E03262,E03292,E03346]  CAUSE: layer-3 wrapped-text identity x6
E01483     8 members  from  8 pool2 entries [E03252,E03254,E03258,E03259,E03312,E03322,E03334,E03337]  CAUSE: layer-3 wrapped-text identity x28
E01484     2 members  from  2 pool2 entries [E03253,E03315]  CAUSE: layer-3 wrapped-text identity x1
E01485     4 members  from  4 pool2 entries [E03263,E03264,E03349,E03352]  CAUSE: layer-3 wrapped-text identity x6
E01486     2 members  from  2 pool2 entries [E03272,E03316]  CAUSE: layer-3 wrapped-text identity x1
E01487     2 members  from  2 pool2 entries [E03278,E03317]  CAUSE: layer-3 wrapped-text identity x1
E01498     2 members  from  2 pool2 entries [E03361,E04638]  CAUSE: layer-3 wrapped-text identity x1
E01499     4 members  from  4 pool2 entries [E03373,E03482,E04650,E04757]  CAUSE: layer-3 wrapped-text identity x6
E01500     2 members  from  2 pool2 entries [E03385,E04665]  CAUSE: layer-3 wrapped-text identity x1
E01502     2 members  from  2 pool2 entries [E03406,E04688]  CAUSE: layer-3 wrapped-text identity x1
E01503     2 members  from  2 pool2 entries [E03407,E04689]  CAUSE: layer-3 wrapped-text identity x1
E01504     2 members  from  2 pool2 entries [E03408,E04690]  CAUSE: layer-3 wrapped-text identity x1
E01505     4 members  from  4 pool2 entries [E03409,E03436,E04691,E04718]  CAUSE: layer-3 wrapped-text identity x6
E01506     4 members  from  4 pool2 entries [E03410,E03442,E04692,E04724]  CAUSE: layer-3 wrapped-text identity x6
E01507    48 members  from 48 pool2 entries [E03411,E03412,E03413,E03415,E03418,E03422,E03423,E03424,E03427,E03428,E03432,E03433,E03448,E03452,E03455,E03463,E03477,E03493,E03496,E03499,E03508,E03511,E03523,E03526,E04693,E04694,E04695,E04697,E04700,E04704,E04705,E04706,E04709,E04710,E04714,E04715,E04730,E04733,E04736,E04742,E04753,E04766,E04769,E04772,E04781,E04784,E04796,E04799]  CAUSE: layer-3 wrapped-text identity x1128
E01508     8 members  from  8 pool2 entries [E03414,E03429,E03459,E03514,E04696,E04711,E04739,E04787]  CAUSE: layer-3 wrapped-text identity x28
E01509     2 members  from  2 pool2 entries [E03416,E04698]  CAUSE: layer-3 wrapped-text identity x1
E01510     2 members  from  2 pool2 entries [E03417,E04699]  CAUSE: layer-3 wrapped-text identity x1
E01511    16 members  from 16 pool2 entries [E03419,E03421,E03425,E03426,E03480,E03490,E03502,E03505,E04701,E04703,E04707,E04708,E04756,E04763,E04775,E04778]  CAUSE: layer-3 wrapped-text identity x120
E01512     4 members  from  4 pool2 entries [E03420,E03483,E04702,E04758]  CAUSE: layer-3 wrapped-text identity x6
E01513     8 members  from  8 pool2 entries [E03430,E03431,E03517,E03520,E04712,E04713,E04790,E04793]  CAUSE: layer-3 wrapped-text identity x28
E01514     4 members  from  4 pool2 entries [E03439,E03484,E04721,E04759]  CAUSE: layer-3 wrapped-text identity x6
E01515     4 members  from  4 pool2 entries [E03445,E03485,E04727,E04760]  CAUSE: layer-3 wrapped-text identity x6
E01519     2 members  from  2 pool2 entries [E03465,E04744]  CAUSE: layer-3 wrapped-text identity x1
E01521     2 members  from  2 pool2 entries [E03470,E04748]  CAUSE: layer-3 wrapped-text identity x1
E01526     2 members  from  2 pool2 entries [E03527,E05105]  CAUSE: layer-3 wrapped-text identity x1
E01529     2 members  from  2 pool2 entries [E03530,E04138]  CAUSE: layer-3 wrapped-text identity x1
E01530     2 members  from  2 pool2 entries [E03531,E04144]  CAUSE: layer-3 wrapped-text identity x1
E01531    24 members  from 24 pool2 entries [E03532,E03533,E03534,E03536,E03539,E03543,E03544,E03545,E03548,E03549,E03553,E03554,E04150,E04153,E04156,E04162,E04173,E04187,E04190,E04193,E04202,E04205,E04217,E04220]  CAUSE: layer-3 wrapped-text identity x276
E01532     4 members  from  4 pool2 entries [E03535,E03550,E04159,E04208]  CAUSE: layer-3 wrapped-text identity x6
E01535     8 members  from  8 pool2 entries [E03540,E03542,E03546,E03547,E04176,E04184,E04196,E04199]  CAUSE: layer-3 wrapped-text identity x28
E01536     2 members  from  2 pool2 entries [E03541,E04179]  CAUSE: layer-3 wrapped-text identity x1
E01537     4 members  from  4 pool2 entries [E03551,E03552,E04211,E04214]  CAUSE: layer-3 wrapped-text identity x6
E01540     2 members  from  2 pool2 entries [E03557,E04139]  CAUSE: layer-3 wrapped-text identity x1
E01541     2 members  from  2 pool2 entries [E03558,E04145]  CAUSE: layer-3 wrapped-text identity x1
E01542    24 members  from 24 pool2 entries [E03559,E03560,E03561,E03563,E03564,E03568,E03569,E03570,E03573,E03574,E03578,E03579,E04151,E04154,E04157,E04163,E04174,E04188,E04191,E04194,E04203,E04206,E04218,E04221]  CAUSE: layer-3 wrapped-text identity x276
E01543     4 members  from  4 pool2 entries [E03562,E03575,E04160,E04209]  CAUSE: layer-3 wrapped-text identity x6
E01545     8 members  from  8 pool2 entries [E03565,E03567,E03571,E03572,E04177,E04185,E04197,E04200]  CAUSE: layer-3 wrapped-text identity x28
E01547     4 members  from  4 pool2 entries [E03576,E03577,E04212,E04215]  CAUSE: layer-3 wrapped-text identity x6
E01551     2 members  from  2 pool2 entries [E03583,E04140]  CAUSE: layer-3 wrapped-text identity x1
E01552     2 members  from  2 pool2 entries [E03584,E04146]  CAUSE: layer-3 wrapped-text identity x1
E01553    24 members  from 24 pool2 entries [E03585,E03586,E03587,E03589,E03592,E03596,E03597,E03598,E03601,E03602,E03606,E03607,E04152,E04155,E04158,E04164,E04175,E04189,E04192,E04195,E04204,E04207,E04219,E04222]  CAUSE: layer-3 wrapped-text identity x276
E01554     4 members  from  4 pool2 entries [E03588,E03603,E04161,E04210]  CAUSE: layer-3 wrapped-text identity x6
E01557     8 members  from  8 pool2 entries [E03593,E03595,E03599,E03600,E04178,E04186,E04198,E04201]  CAUSE: layer-3 wrapped-text identity x28
E01558     2 members  from  2 pool2 entries [E03594,E04180]  CAUSE: layer-3 wrapped-text identity x1
E01559     4 members  from  4 pool2 entries [E03604,E03605,E04213,E04216]  CAUSE: layer-3 wrapped-text identity x6
E01560     2 members  from  2 pool2 entries [E03608,E04061]  CAUSE: layer-3 wrapped-text identity x1
E01561     2 members  from  2 pool2 entries [E03609,E04088]  CAUSE: layer-3 wrapped-text identity x1
E01562     2 members  from  2 pool2 entries [E03610,E04113]  CAUSE: layer-3 wrapped-text identity x1
E01567     2 members  from  2 pool2 entries [E03611,E04167]  CAUSE: layer-3 wrapped-text identity x1
E01568     2 members  from  2 pool2 entries [E03612,E04171]  CAUSE: layer-3 wrapped-text identity x1
E01570     2 members  from  2 pool2 entries [E03613,E04181]  CAUSE: layer-3 wrapped-text identity x1
E01572     2 members  from  2 pool2 entries [E03614,E04062]  CAUSE: layer-3 wrapped-text identity x1
E01573     2 members  from  2 pool2 entries [E03615,E04089]  CAUSE: layer-3 wrapped-text identity x1
E01574     2 members  from  2 pool2 entries [E03616,E04114]  CAUSE: layer-3 wrapped-text identity x1
E01577     2 members  from  2 pool2 entries [E03617,E04168]  CAUSE: layer-3 wrapped-text identity x1
E01578     2 members  from  2 pool2 entries [E03618,E04172]  CAUSE: layer-3 wrapped-text identity x1
E01580     2 members  from  2 pool2 entries [E03619,E04182]  CAUSE: layer-3 wrapped-text identity x1
E01582    24 members  from 24 pool2 entries [E03620,E03626,E03629,E03637,E03650,E03673,E03676,E03679,E03688,E03691,E03704,E03707,E04063,E04064,E04065,E04067,E04070,E04074,E04075,E04076,E04079,E04080,E04084,E04085]  CAUSE: layer-3 wrapped-text identity x276
E01583    24 members  from 24 pool2 entries [E03621,E03627,E03630,E03638,E03651,E03674,E03677,E03680,E03689,E03692,E03705,E03708,E04090,E04091,E04092,E04094,E04095,E04098,E04099,E04100,E04103,E04104,E04108,E04109]  CAUSE: layer-3 wrapped-text identity x276
E01584    24 members  from 24 pool2 entries [E03622,E03628,E03631,E03639,E03652,E03675,E03678,E03681,E03690,E03693,E03706,E03709,E04115,E04116,E04117,E04119,E04122,E04126,E04127,E04128,E04131,E04132,E04136,E04137]  CAUSE: layer-3 wrapped-text identity x276
E01593     4 members  from  4 pool2 entries [E03633,E03694,E04066,E04081]  CAUSE: layer-3 wrapped-text identity x6
E01594     4 members  from  4 pool2 entries [E03634,E03695,E04093,E04105]  CAUSE: layer-3 wrapped-text identity x6
E01595     4 members  from  4 pool2 entries [E03635,E03696,E04118,E04133]  CAUSE: layer-3 wrapped-text identity x6
E01599     2 members  from  2 pool2 entries [E03642,E04141]  CAUSE: layer-3 wrapped-text identity x1
E01600     2 members  from  2 pool2 entries [E03643,E04147]  CAUSE: layer-3 wrapped-text identity x1
E01604     2 members  from  2 pool2 entries [E03647,E04142]  CAUSE: layer-3 wrapped-text identity x1
E01605     2 members  from  2 pool2 entries [E03648,E04148]  CAUSE: layer-3 wrapped-text identity x1
E01607     8 members  from  8 pool2 entries [E03653,E03670,E03682,E03685,E04071,E04073,E04077,E04078]  CAUSE: layer-3 wrapped-text identity x28
E01608     8 members  from  8 pool2 entries [E03654,E03671,E03683,E03686,E04096,E04097,E04101,E04102]  CAUSE: layer-3 wrapped-text identity x28
E01609     8 members  from  8 pool2 entries [E03655,E03672,E03684,E03687,E04123,E04125,E04129,E04130]  CAUSE: layer-3 wrapped-text identity x28
E01613     2 members  from  2 pool2 entries [E03657,E04072]  CAUSE: layer-3 wrapped-text identity x1
E01615     2 members  from  2 pool2 entries [E03659,E04124]  CAUSE: layer-3 wrapped-text identity x1
E01616     2 members  from  2 pool2 entries [E03660,E04143]  CAUSE: layer-3 wrapped-text identity x1
E01617     2 members  from  2 pool2 entries [E03661,E04149]  CAUSE: layer-3 wrapped-text identity x1
E01626     4 members  from  4 pool2 entries [E03697,E03701,E04082,E04083]  CAUSE: layer-3 wrapped-text identity x6
E01627     4 members  from  4 pool2 entries [E03698,E03702,E04106,E04107]  CAUSE: layer-3 wrapped-text identity x6
E01628     4 members  from  4 pool2 entries [E03699,E03703,E04134,E04135]  CAUSE: layer-3 wrapped-text identity x6
E01632     2 members  from  2 pool2 entries [E03710,E05134]  CAUSE: layer-3 wrapped-text identity x1
E01635     2 members  from  2 pool2 entries [E03713,E03972]  CAUSE: layer-3 wrapped-text identity x1
E01636     2 members  from  2 pool2 entries [E03714,E03978]  CAUSE: layer-3 wrapped-text identity x1
E01637    24 members  from 24 pool2 entries [E03715,E03716,E03717,E03719,E03722,E03726,E03727,E03728,E03731,E03732,E03736,E03737,E03984,E03987,E03990,E03996,E04008,E04022,E04025,E04028,E04037,E04040,E04052,E04055]  CAUSE: layer-3 wrapped-text identity x276
E01638     4 members  from  4 pool2 entries [E03718,E03733,E03993,E04043]  CAUSE: layer-3 wrapped-text identity x6
E01641     8 members  from  8 pool2 entries [E03723,E03725,E03729,E03730,E04011,E04019,E04031,E04034]  CAUSE: layer-3 wrapped-text identity x28
E01642     2 members  from  2 pool2 entries [E03724,E04014]  CAUSE: layer-3 wrapped-text identity x1
E01643     4 members  from  4 pool2 entries [E03734,E03735,E04046,E04049]  CAUSE: layer-3 wrapped-text identity x6
E01646     2 members  from  2 pool2 entries [E03740,E03973]  CAUSE: layer-3 wrapped-text identity x1
E01647     2 members  from  2 pool2 entries [E03741,E03979]  CAUSE: layer-3 wrapped-text identity x1
E01648    24 members  from 24 pool2 entries [E03742,E03743,E03744,E03746,E03747,E03751,E03752,E03753,E03756,E03757,E03761,E03762,E03985,E03988,E03991,E03997,E04009,E04023,E04026,E04029,E04038,E04041,E04053,E04056]  CAUSE: layer-3 wrapped-text identity x276
E01649     4 members  from  4 pool2 entries [E03745,E03758,E03994,E04044]  CAUSE: layer-3 wrapped-text identity x6
E01650     8 members  from  8 pool2 entries [E03748,E03750,E03754,E03755,E04012,E04020,E04032,E04035]  CAUSE: layer-3 wrapped-text identity x28
E01652     4 members  from  4 pool2 entries [E03759,E03760,E04047,E04050]  CAUSE: layer-3 wrapped-text identity x6
E01656     2 members  from  2 pool2 entries [E03766,E03974]  CAUSE: layer-3 wrapped-text identity x1
E01657     2 members  from  2 pool2 entries [E03767,E03980]  CAUSE: layer-3 wrapped-text identity x1
E01658    24 members  from 24 pool2 entries [E03768,E03769,E03770,E03772,E03775,E03779,E03780,E03781,E03784,E03785,E03789,E03790,E03986,E03989,E03992,E03998,E04010,E04024,E04027,E04030,E04039,E04042,E04054,E04057]  CAUSE: layer-3 wrapped-text identity x276
E01659     4 members  from  4 pool2 entries [E03771,E03786,E03995,E04045]  CAUSE: layer-3 wrapped-text identity x6
E01662     8 members  from  8 pool2 entries [E03776,E03778,E03782,E03783,E04013,E04021,E04033,E04036]  CAUSE: layer-3 wrapped-text identity x28
E01663     2 members  from  2 pool2 entries [E03777,E04015]  CAUSE: layer-3 wrapped-text identity x1
E01664     4 members  from  4 pool2 entries [E03787,E03788,E04048,E04051]  CAUSE: layer-3 wrapped-text identity x6
E01665     2 members  from  2 pool2 entries [E03791,E03894]  CAUSE: layer-3 wrapped-text identity x1
E01666     2 members  from  2 pool2 entries [E03792,E03922]  CAUSE: layer-3 wrapped-text identity x1
E01667     2 members  from  2 pool2 entries [E03793,E03947]  CAUSE: layer-3 wrapped-text identity x1
E01672     2 members  from  2 pool2 entries [E03794,E04001]  CAUSE: layer-3 wrapped-text identity x1
E01673     2 members  from  2 pool2 entries [E03795,E04005]  CAUSE: layer-3 wrapped-text identity x1
E01675     2 members  from  2 pool2 entries [E03796,E04016]  CAUSE: layer-3 wrapped-text identity x1
E01677     2 members  from  2 pool2 entries [E03797,E03895]  CAUSE: layer-3 wrapped-text identity x1
E01678     2 members  from  2 pool2 entries [E03798,E03923]  CAUSE: layer-3 wrapped-text identity x1
E01679     2 members  from  2 pool2 entries [E03799,E03948]  CAUSE: layer-3 wrapped-text identity x1
E01682     2 members  from  2 pool2 entries [E03800,E04002]  CAUSE: layer-3 wrapped-text identity x1
E01683     2 members  from  2 pool2 entries [E03801,E04006]  CAUSE: layer-3 wrapped-text identity x1
E01685     2 members  from  2 pool2 entries [E03802,E04017]  CAUSE: layer-3 wrapped-text identity x1
E01687    24 members  from 24 pool2 entries [E03803,E03807,E03810,E03818,E03831,E03854,E03857,E03860,E03869,E03872,E03885,E03888,E03896,E03897,E03898,E03900,E03903,E03907,E03908,E03909,E03912,E03913,E03917,E03918]  CAUSE: layer-3 wrapped-text identity x276
E01688    24 members  from 24 pool2 entries [E03804,E03808,E03811,E03819,E03832,E03855,E03858,E03861,E03870,E03873,E03886,E03889,E03924,E03925,E03926,E03928,E03929,E03932,E03933,E03934,E03937,E03938,E03942,E03943]  CAUSE: layer-3 wrapped-text identity x276
E01689    24 members  from 24 pool2 entries [E03805,E03809,E03812,E03820,E03833,E03856,E03859,E03862,E03871,E03874,E03887,E03890,E03949,E03950,E03951,E03953,E03956,E03960,E03961,E03962,E03965,E03966,E03970,E03971]  CAUSE: layer-3 wrapped-text identity x276
E01696     4 members  from  4 pool2 entries [E03814,E03875,E03899,E03914]  CAUSE: layer-3 wrapped-text identity x6
E01697     4 members  from  4 pool2 entries [E03815,E03876,E03927,E03939]  CAUSE: layer-3 wrapped-text identity x6
E01698     4 members  from  4 pool2 entries [E03816,E03877,E03952,E03967]  CAUSE: layer-3 wrapped-text identity x6
E01702     2 members  from  2 pool2 entries [E03823,E03975]  CAUSE: layer-3 wrapped-text identity x1
E01703     2 members  from  2 pool2 entries [E03824,E03981]  CAUSE: layer-3 wrapped-text identity x1
E01707     2 members  from  2 pool2 entries [E03828,E03976]  CAUSE: layer-3 wrapped-text identity x1
E01708     2 members  from  2 pool2 entries [E03829,E03982]  CAUSE: layer-3 wrapped-text identity x1
E01710     8 members  from  8 pool2 entries [E03834,E03851,E03863,E03866,E03904,E03906,E03910,E03911]  CAUSE: layer-3 wrapped-text identity x28
E01711     8 members  from  8 pool2 entries [E03835,E03852,E03864,E03867,E03930,E03931,E03935,E03936]  CAUSE: layer-3 wrapped-text identity x28
E01712     8 members  from  8 pool2 entries [E03836,E03853,E03865,E03868,E03957,E03959,E03963,E03964]  CAUSE: layer-3 wrapped-text identity x28
E01716     2 members  from  2 pool2 entries [E03838,E03905]  CAUSE: layer-3 wrapped-text identity x1
E01718     2 members  from  2 pool2 entries [E03840,E03958]  CAUSE: layer-3 wrapped-text identity x1
E01719     2 members  from  2 pool2 entries [E03841,E03977]  CAUSE: layer-3 wrapped-text identity x1
E01720     2 members  from  2 pool2 entries [E03842,E03983]  CAUSE: layer-3 wrapped-text identity x1
E01729     4 members  from  4 pool2 entries [E03878,E03882,E03915,E03916]  CAUSE: layer-3 wrapped-text identity x6
E01730     4 members  from  4 pool2 entries [E03879,E03883,E03940,E03941]  CAUSE: layer-3 wrapped-text identity x6
E01731     4 members  from  4 pool2 entries [E03880,E03884,E03968,E03969]  CAUSE: layer-3 wrapped-text identity x6
E01735     2 members  from  2 pool2 entries [E03891,E05106]  CAUSE: layer-3 wrapped-text identity x1
E01771     2 members  from  2 pool2 entries [E04058,E05082]  CAUSE: layer-3 wrapped-text identity x1
E01812    11 members  from 11 pool2 entries [E04228,E04229,E04231,E04234,E04238,E04239,E04240,E04243,E04244,E04248,E04249]  CAUSE: layer-3 wrapped-text identity x55
E01813     2 members  from  2 pool2 entries [E04230,E04245]  CAUSE: layer-3 wrapped-text identity x1
E01816     4 members  from  4 pool2 entries [E04235,E04237,E04241,E04242]  CAUSE: layer-3 wrapped-text identity x6
E01818     2 members  from  2 pool2 entries [E04246,E04247]  CAUSE: layer-3 wrapped-text identity x1
E01824    11 members  from 11 pool2 entries [E04255,E04256,E04258,E04261,E04265,E04266,E04267,E04270,E04271,E04275,E04276]  CAUSE: layer-3 wrapped-text identity x55
E01825     2 members  from  2 pool2 entries [E04257,E04272]  CAUSE: layer-3 wrapped-text identity x1
E01828     4 members  from  4 pool2 entries [E04262,E04264,E04268,E04269]  CAUSE: layer-3 wrapped-text identity x6
E01830     2 members  from  2 pool2 entries [E04273,E04274]  CAUSE: layer-3 wrapped-text identity x1
E01836    11 members  from 11 pool2 entries [E04282,E04283,E04285,E04288,E04292,E04293,E04294,E04297,E04298,E04302,E04303]  CAUSE: layer-3 wrapped-text identity x55
E01837     2 members  from  2 pool2 entries [E04284,E04299]  CAUSE: layer-3 wrapped-text identity x1
E01840     4 members  from  4 pool2 entries [E04289,E04291,E04295,E04296]  CAUSE: layer-3 wrapped-text identity x6
E01842     2 members  from  2 pool2 entries [E04300,E04301]  CAUSE: layer-3 wrapped-text identity x1
E01863    11 members  from 11 pool2 entries [E04318,E04323,E04337,E04357,E04380,E04384,E04387,E04396,E04399,E04414,E04417]  CAUSE: layer-3 wrapped-text identity x55
E01864    11 members  from 11 pool2 entries [E04319,E04324,E04338,E04358,E04381,E04385,E04388,E04397,E04400,E04415,E04418]  CAUSE: layer-3 wrapped-text identity x55
E01865    11 members  from 11 pool2 entries [E04320,E04325,E04339,E04359,E04382,E04386,E04389,E04398,E04401,E04416,E04419]  CAUSE: layer-3 wrapped-text identity x55
E01876     2 members  from  2 pool2 entries [E04331,E04402]  CAUSE: layer-3 wrapped-text identity x1
E01877     2 members  from  2 pool2 entries [E04332,E04403]  CAUSE: layer-3 wrapped-text identity x1
E01878     2 members  from  2 pool2 entries [E04333,E04404]  CAUSE: layer-3 wrapped-text identity x1
E01897     4 members  from  4 pool2 entries [E04360,E04377,E04390,E04393]  CAUSE: layer-3 wrapped-text identity x6
E01898     4 members  from  4 pool2 entries [E04361,E04378,E04391,E04394]  CAUSE: layer-3 wrapped-text identity x6
E01899     4 members  from  4 pool2 entries [E04362,E04379,E04392,E04395]  CAUSE: layer-3 wrapped-text identity x6
E01917     2 members  from  2 pool2 entries [E04405,E04410]  CAUSE: layer-3 wrapped-text identity x1
E01918     2 members  from  2 pool2 entries [E04406,E04411]  CAUSE: layer-3 wrapped-text identity x1
E01919     2 members  from  2 pool2 entries [E04407,E04412]  CAUSE: layer-3 wrapped-text identity x1
E01926     3 members  from  3 pool2 entries [E04805,E04808,E04810]  CAUSE: layer-3 wrapped-text identity x3
E01935     5 members  from  5 pool2 entries [E04823,E04844,E04854,E04869,E04879]  CAUSE: layer-3 wrapped-text identity x10
E01936     5 members  from  5 pool2 entries [E04826,E04847,E04857,E04872,E04882]  CAUSE: layer-3 wrapped-text identity x10
E01940     6 members  from  6 pool2 entries [E04831,E04839,E04849,E04859,E04864,E04874]  CAUSE: layer-3 wrapped-text identity x15
E01941     6 members  from  6 pool2 entries [E04834,E04842,E04852,E04862,E04867,E04877]  CAUSE: layer-3 wrapped-text identity x15
E01945     2 members  from  2 pool2 entries [E04884,E04909]  CAUSE: layer-3 wrapped-text identity x1
E01946     2 members  from  2 pool2 entries [E04887,E04912]  CAUSE: layer-3 wrapped-text identity x1
E01950     2 members  from  2 pool2 entries [E04891,E04894]  CAUSE: layer-3 wrapped-text identity x1
E01963     2 members  from  2 pool2 entries [E04913,E04916]  CAUSE: layer-3 wrapped-text identity x1
E01971     3 members  from  3 pool2 entries [E04923,E04949,E04963]  CAUSE: layer-3 wrapped-text identity x3
E01972     3 members  from  3 pool2 entries [E04926,E04952,E04966]  CAUSE: layer-3 wrapped-text identity x3
E01976     2 members  from  2 pool2 entries [E04930,E04933]  CAUSE: layer-3 wrapped-text identity x1
E01984     2 members  from  2 pool2 entries [E04939,E04942]  CAUSE: layer-3 wrapped-text identity x1
E01992     2 members  from  2 pool2 entries [E04953,E04956]  CAUSE: layer-3 wrapped-text identity x1
E02153     2 members  from  2 pool2 entries [E05157,E05160]  CAUSE: layer-3 wrapped-text identity x1
E02194     2 members  from  2 pool2 entries [E05198,E05202]  CAUSE: layer-3 wrapped-text identity x1
E02240     2 members  from  2 pool2 entries [E05247,E05262]  CAUSE: layer-3 wrapped-text identity x1
E02241     2 members  from  2 pool2 entries [E05249,E05264]  CAUSE: layer-3 wrapped-text identity x1
E02242     2 members  from  2 pool2 entries [E05250,E05265]  CAUSE: layer-3 wrapped-text identity x1
E02243     2 members  from  2 pool2 entries [E05253,E05268]  CAUSE: layer-3 wrapped-text identity x1
E02244     2 members  from  2 pool2 entries [E05255,E05270]  CAUSE: layer-3 wrapped-text identity x1
E02245     2 members  from  2 pool2 entries [E05256,E05271]  CAUSE: layer-3 wrapped-text identity x1
E02246     2 members  from  2 pool2 entries [E05257,E05272]  CAUSE: layer-3 wrapped-text identity x1
E02247     2 members  from  2 pool2 entries [E05259,E05274]  CAUSE: layer-3 wrapped-text identity x1
```

---

# 6. THE SYMBOLIC-TARGET QUESTION — pool2's 4,499 members

## 6.1 What was asked, and what was measured

Log 148 §4.2.2 measured 4,499 member units whose canon37 wrapped text
carried a symbol comment on a branch target — text like
`jl 47a678 <main.op_174+0x18>`, which puts the unit's OWN NAME inside
its own text and so keeps two otherwise identical units apart. Ruling
4 replaced those with positional labels `L0..`. The brief asks how
many of the 4,499 now merge on layer-3 identity.

The measurement is: for each of the 4,499, does its canon38 wrapped
text belong to some other unit of the pool as well.

LITERAL — `audit54_printed.txt`, section (f):

```
    member units whose canon37 wrapped text carries a symbol
    comment (the population this question is about)    4499
    of those, sharing their canon37 text with another unit
    -- already merging on layer-3 identity before       84
    of those, sharing their canon38 text with another unit
    -- MERGING ON LAYER-3 IDENTITY NOW                4065
    of those, NEWLY merging on layer-3 identity       3981
    of those, still the only holder of their text      434
    check: 4065 + 434 = 4499, the population
    also, over the whole 30,436:
      units carrying a symbol comment in canon38         0
```

## 6.2 The answer, stated plainly

- **4,065 of the 4,499 now merge on layer-3 wrapped-text identity.**
- **3,981 of them did not before**: only 84 of the 4,499 shared their
  canon37 text with anything, because the name inside the text made
  each one unique.
- 434 remain the only holder of their canon38 text. They are not a
  failure of ruling 4 — zero stored texts carry a symbol comment now
  (the last line above) — they simply have no twin.
- The population reconciles exactly: 4,065 + 434 = 4,499.

---

# 7. THE FAMILIES

## 7.1 The rule, imported rather than restated

`build_the_families3.py` imports `dom_ops.py` — `build_nodes`,
`fill_nodes`, `build_edges`, `best_per_language`, `mutual_edges`,
`components` — so THE DOM_OP CONSTRUCTION RULE cannot drift here.
Nodes are (language, grammar-operator, ARITY); edges only BETWEEN
languages, weighted by shared entry count; each node keeps its single
strongest counterpart per foreign language, kept only when MUTUAL;
connected components of the mutual-best graph are the families. The
token is a `label` display field read by nothing.

LITERAL — `the_families3_run.log`:

```
-- reading the pool
   pool entries 2247, pool units 30436
-- nodes (language, grammar-operator, arity) 197
-- cross-language edges, raw 867
-- edges surviving the mutual filter 305
-- families 36
```

## 7.2 What moved, computed by node set

The two family sets were compared by their NODE SETS, not by name.

LITERAL — the command and its output:

```
$ /tmp/reconnect_venv/bin/python3 -c "
import json
def sets(p):
    d=json.load(open(p))
    return {f['family_id']: frozenset(n['id'] for n in f['nodes']) for f in d['families']}
a=sets('the_families2.json'); b=sets('the_families3.json')
sa=set(a.values()); sb=set(b.values())
print('families2',len(a),'families3',len(b))
print('node sets identical in both:',len(sa&sb))
print('only in families2:',len(sa-sb))
for s in sorted(sa-sb,key=len): print('   size',len(s),sorted(s)[:8])
print('only in families3:',len(sb-sa))
for s in sorted(sb-sa,key=len): print('   size',len(s),sorted(s)[:8])
"
families2 35 families3 36
node sets identical in both: 30
only in families2: 5
   size 2 ['N0001', 'N0047']
   size 2 ['N0077', 'N0179']
   size 3 ['N0050', 'N0093', 'N0161']
   size 5 ['N0003', 'N0049', 'N0105', 'N0136', 'N0160']
   size 17 ['N0013', 'N0016', 'N0020', 'N0040', 'N0059', 'N0062', 'N0066', 'N0103']
only in families3: 6
   size 3 ['N0029', 'N0077', 'N0179']
   size 3 ['N0001', 'N0047', 'N0090']
   size 4 ['N0004', 'N0050', 'N0093', 'N0161']
   size 6 ['N0003', 'N0049', 'N0092', 'N0105', 'N0136', 'N0160']
   size 8 ['N0016', 'N0020', 'N0040', 'N0062', 'N0066', 'N0114', 'N0147', 'N0167']
   size 9 ['N0013', 'N0059', 'N0103', 'N0113', 'N0130', 'N0132', 'N0133', 'N0141']
```

- **30 of the 35 families are unchanged node for node.**
- **Four families each gained exactly one node** (2→3, 2→3, 3→4, 5→6).
  That is where `nodes_in_a_family` 161 → 165 comes from.
- **One 17-node family became an 8-node family and a 9-node family.**
  That is the whole of 35 → 36. 8 + 9 = 17, so no node was lost.
- No family is a singleton, in either round.

---

# 8. THE GUARD, RUN WITHOUT EXEMPTION

`check_no_spelling_keys.py` was not edited. Its committed copy is
`fdff0b2` of 2026-08-26.

LITERAL — the commands and their output:

```
$ git status --porcelain Research/op_pipeline/check_no_spelling_keys.py
$ sha256sum Research/op_pipeline/check_no_spelling_keys.py
a377462b38e8610d8bb60ac668f0a5adc72ee571d15efab85e40a9afdaa511f7  Research/op_pipeline/check_no_spelling_keys.py
$ git log -1 --format='%h %ad %s' -- Research/op_pipeline/check_no_spelling_keys.py
fdff0b2 Wed Aug 26 13:14:26 2026 -0400 update
```

- `git status --porcelain` printed NOTHING over the guard file, which
  is what "unmodified" means here. The sha256 is the same one log 153
  §7 pasted.

LITERAL — `guard54.py`'s own line, and `guard54_transcript.txt` in
full:

```
$ /tmp/reconnect_venv/bin/python3 guard54.py
TASK 54: 4 paths  PASS 4  FAIL 0  exempt 0  exit 0
guard exit=0

$ cat guard54_transcript.txt
guard54.py -- every artifact task 54 writes, unmodified guard, ONE process.  No file declares the provenance role and nothing was added to any field set.
$ python3 check_no_spelling_keys.py <4 paths, one process>

operator inventory: 91 tokens read from probe_manifest_*.json
PASS the_pool3.json -- no operator token in any key, grouping, pairing or row structure
PASS the_families3.json -- no operator token in any key, grouping, pairing or row structure
PASS pool2_pool3_delta.json -- no operator token in any key, grouping, pairing or row structure
PASS the_pool3_bytes.json -- no operator token in any key, grouping, pairing or row structure

GUARD EXIT CODE = 0

$ grep -c exempt guard54_transcript.txt
0
```

- ONE process, every JSON artifact this task writes, no exemption of
  any kind. `grep -c exempt` = 0. Exit 0.
- No file this task writes declares `role: generator provenance`, and
  nothing was added to any field set to quiet the checker.
- `the_pool3_bytes.json` is walked too, although its keys are raw
  assembly texts, precisely so that nothing hides behind "it is only a
  cache".

---

# 9. ZERO REGRESSIONS

## 9.1 Nothing prior was edited

LITERAL — the command and its output:

```
$ git status --porcelain Research/op_pipeline/the_pool2.json \
    Research/op_pipeline/the_pool1.json \
    Research/op_pipeline/the_families2.json \
    Research/op_pipeline/the_families1.json \
    Research/op_pipeline/build_the_pool2.py \
    Research/op_pipeline/build_the_families2.py \
    Research/op_pipeline/compare_pool1_pool2.py \
    Research/op_pipeline/the_pool2_bytes.json
```

- The command printed NOTHING. Every superseded artifact and every
  reused program is byte for byte what it was.
- `build_the_pool2.py` is IMPORTED by `build_the_pool3.py` —
  `layer5_eligibility`, `type_key_of`, `proved_edge_list` and
  `UnionFind` come from it unchanged — and by
  `compare_pool2_pool3.py` for its proved-edge list. Import is not
  edit.
- `build_the_families3.py` and `compare_pool2_pool3.py` were derived
  from their round-10 counterparts by NAME SUBSTITUTION ONLY, and each
  says so in its own docstring.

## 9.2 The population did not move

LITERAL — `audit54_printed.txt` section (a), first row: member units
30,436 in both pools, delta +0. Both pools hold the identical unit set
(§5.1: 0 units in either pool only).

## 9.3 The counts that must not move, did not

- entries spanning compiled and interpreted: 3 → 3.
- proved edges applied: 118 → 118.
- family nodes: 197 → 197.
- singleton families: 0 → 0.

---

# 10. THE EVIDENCE CLASS OF EACH CLAIM

- **Forced by construction** — layer-3 wrapped-text identity (two
  identical strings are identical bytes; the texts assemble and were
  assembled); the representative's byte count (`as` + `objdump` on the
  actual text); every count in this log (a program walked the
  artifact and printed it).
- **The tool's own testimony** — layer-5 eligibility, which rests on
  z3's verdict over the lifter's model of the machine, recorded by
  task 53; the proved edges, which rest on earlier provers.
- **Human interpretation of stated design** — nothing in this log
  rests on it. The one place it could have — the recorded entry
  contract — is not read by this task; the pool reads the arrival
  families the body itself shows.
- **Sampled observation** — used nowhere. Every "all N" here is a full
  walk of the population named beside it.

---

# 11. THE COMPLETE FILE INVENTORY

## 11.1 Code written this task (six files, all new; nothing reused was edited)

| file | bytes | what it is |
|---|---|---|
| `build_the_pool3.py` | 26,178 | THE POOL. canon38 + layer4c intake, ruling 1's three grounds, transitive closure, the representative rule, the brief-strict count recorded. Imports `build_the_pool2.py` unedited. |
| `build_the_families3.py` | 10,150 | the dom_op rule over `the_pool3.json`, via `dom_ops.py`. Derived from `build_the_families2.py` by name substitution. |
| `compare_pool2_pool3.py` | 12,630 | every split and every merge, joined on member sets, causes computed. Derived from `compare_pool1_pool2.py` by name substitution. |
| `audit54.py` | 11,954 | the figures: headline counts, the brief-strict count, the population, eligibility, E00029's successor, the symbolic-target question, eligibility movement, zero regressions. |
| `print_delta54.py` | 5,674 | prints every split and every merge in full, and writes the two one-line tables this log carries. |
| `guard54.py` | 4,824 | runs the UNMODIFIED guard, one process, over every task-54 JSON artifact. |

## 11.2 Data written this task

| file | bytes | what it is |
|---|---|---|
| `the_pool3.json` | 31,225,989 | THE POOL: 2,247 entries over 30,436 members. |
| `the_families3.json` | 215,520 | 36 families over 197 nodes. |
| `pool2_pool3_delta.json` | 455,694 | 60 splits, 719 merges, causes computed. |
| `the_pool3_bytes.json` | 326,610 | the assembled byte counts of the 1,144 texts the representative rule had to decide between. |
| `guard54.json` | 299 | the guard run's counts. |

## 11.3 Transcripts and logs written this task

| file | bytes | what it is |
|---|---|---|
| `the_pool3_run.log` | 1,606 | the pool build, start to finish. |
| `the_families3_run.log` | 445 | the family build. |
| `audit54_printed.txt` | 41,256 | sections (a)–(h), including E00029 verbatim. |
| `pool2_pool3_delta_printed.txt` | 2,095 | the comparison's own run. |
| `pool2_pool3_delta_full.txt` | 200,218 | every split and every merge, with member lists. |
| `pool2_pool3_splits_oneline.txt` | 10,189 | the 60 splits, one line each (§5.4). |
| `pool2_pool3_merges_oneline.txt` | 90,308 | the 719 merges, one line each (§5.5). |
| `guard54_transcript.txt` | 667 | 4 PASS, 0 FAIL, 0 exempt, exit 0. |

## 11.4 Read, never written

`canon38_wrapped_{c,cpp,go,rust,swift}.json`, `canon38_interp.json`,
`canon38_regen_store/*.json`, `layer4c_terms_{c,cpp,go,rust,swift}.json`,
`layer4c_interp.json`, `layer4c_regen_store/*.json`,
`proved_edges.json`, `proved_edges2.json`, `proved_edges3.json`,
`interp_join3.json`, `interp_fastpath.json`, `the_pool2.json`,
`the_families2.json`, `build_the_pool2.py`, `build_the_families2.py`,
`compare_pool1_pool2.py`, `dom_ops.py`, `dom_ops_0branch.py`,
`probe_manifest_*.json`, `check_no_spelling_keys.py`.

## 11.5 Scratch, outside the repository (named, not banked)

`/tmp/the_pool3_work` — the batch `.s` and `.o` files the byte
measurement assembled.

---

# 12. Resume state

## 12.1 Nothing is part-done

Every step ran to completion in-session; there is no chunked state and
no resume file. The pool build takes 7 seconds, the family build 2.

## 12.2 How to re-run, in order

1. `build_the_pool3.py > the_pool3_run.log`
2. `build_the_families3.py > the_families3_run.log`
3. `compare_pool2_pool3.py > pool2_pool3_delta_printed.txt`
4. `print_delta54.py > pool2_pool3_delta_full.txt`
5. `audit54.py > audit54_printed.txt`
6. `guard54.py` — LAST, because it walks the artifacts steps 1–3 wrote.

All six run under `/tmp/reconnect_venv/bin/python3`. Steps 2–6 are
read-only over step 1's artifact.

---

# 13. Decided and recorded for audit / awaiting the owner

## 13.1 Decided, recorded (no answer needed)

1. **The undecided and the no-term units are treated exactly like the
   withdrawn.** The brief names the 415 withdrawn; the same rule
   reaches all 7,304 units with no proved term, because the reason is
   the same in every case — an unproved term is not evidence of
   equivalence. Each carries its own reason string, so the three
   causes stay distinguishable on the artifact (§3).
2. **The 8 texts that will not assemble keep the character-length
   substitution pool2 used**, and each of the 2 affected entries says
   so in `representative_size_measured_as` rather than presenting a
   character count as a byte count (§2.4).
3. **`the_pool3_bytes.json` is walked by the guard** even though it is
   a cache, so no artifact of this task sits outside the check.
4. **The delta is computed against pool2 only.** pool1 is two rounds
   back and holds a different population (28,984); comparing across it
   would mix arrivals into splits.

## 13.2 Awaiting the owner

1. **The 434 lone symbolic-target units (§6.2).** They carry no symbol
   comment any more and still hold their text alone. Nothing is wrong
   with them; the question is whether that residue is worth a pass of
   its own or is simply the tail.
2. **Task 53's two open calls still gate the layer-5 ground here**: a
   gate route pointing at a reference whose remainder matches the
   machine would decide the 415, and a gate route modelling the
   machine stack and the x87 stack would decide a large part of the
   5,602 undecided. Both would raise ground (a)'s reach in the next
   pool; neither is done here, because neither is this task's.
