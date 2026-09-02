# clusters_preliminary — layer 3, phase 4, PRELIMINARY
Built 2026-08-18 13:47:39 from `clusters_preliminary.json`. **Every number here is
PRELIMINARY.** Scope: nine acceptance grids (route A) + three route-C behavior tables, all complete; plus a value-matrix OVERLAY for the matrices that pass the completeness gate, decisions 8-11

## the shape of the pass

- **233 operation signatures** over twelve languages; 229 have a
  non-empty accepted domain and 4 are empty and excluded
  (`csharp.is`, `java.instanceof`, `kotlin.&`, `python.@`).
- the shared space is the **64 ordered form pairs** over the eight
  layer-1 forms, which all twelve languages carry.
- **46 clusters** at the 0.70 cut, **58** at 0.85.
- **2909 relation edges**: contradicts 7, equals 687, nested_by 1009, nests 588, overlaps 618.

## the numbered decisions

**1.** HOLDER-TO-FORM PROJECTION.  A language's acceptance grid is at holder grain, and two languages do not share holders, so nothing can be compared until both are projected onto the layer-1 forms they DO share.  Every holder is replaced by its form and a domain becomes a set of ordered FORM pairs.  All twelve languages carry all eight forms, so the shared space is the same 64 ordered pairs for every language pair -- no pair-specific restriction is needed.  Overturnable: the projection is lossy exactly where CORE ruling 1 said it would be (Decimal(42) + Fraction(42) raises though both hold one form), so a holder-grain comparison remains available for language pairs that have a holder correspondence.

**2.** EXISTENTIAL PROJECTION RULE.  A projected form-pair cell counts as ACCEPTED if AT LEAST ONE holder pair with those forms was accepted. Rationale: the question a domain answers is `can this operation take these forms at all', which is existential.  The alternatives -- universal (all holder pairs accept) and majority -- are computed and stored alongside as `density` so overturning this costs a re-read and not a re-run.

**3.** ROUTE-C DOMAIN RULE.  For python, ruby and php acceptance does not exist as a separate verdict; execution is the only evidence (CORE ruling 5, route C).  A cell counts as ACCEPTED there if at least one probe returned ANSWER.  RAISE, REFUSE and BUDGET all count as not-accepted.  Overturnable: RAISE is arguably `accepted then failed', which would widen these three domains.

**4.** SIMILARITY MEASURE.  Jaccard on the ACCEPT sets over the 64 shared form pairs: |A and B| / |A or B|.  Chosen because it ignores the enormous agreed-REFUSE background that would make every pair of operations look ~90 percent alike under plain agreement.  An operation with an EMPTY domain is excluded from clustering entirely rather than being scored 0 against everything.

**5.** CLUSTER CUT.  Average-linkage agglomerative over 1 - Jaccard, cut at similarity 0.70.  The 0.85 cut is computed too and reported beside it, because the honest thing to show is how much the picture moves with the threshold.  Nothing in the data picks 0.70; it is a reading choice.

**6.** RELATIONS.  Over the shared space: NESTS if one accept set strictly contains the other and the contained one is non-empty; OVERLAPS if they intersect and neither contains the other; CONTRADICTS is reserved for the SAME SPELLED operation in two languages whose accept sets are disjoint while both are non-empty. Overturnable: `contradicts' in the CORE is defined at the answer grain (same input, different answer) and only three languages have answers, so this is the acceptance-grain reading of it and is labelled as such.

**7.** THE MIXED-HOLDER STATISTIC IS COMPUTED, NEVER ASSERTED.  The shift exemption is a claim about HOLDERS, which the form projection destroys, so a second statistic is measured at holder grain: among accepted probes whose two holders share one form, the fraction whose holders DIFFER.  No operation and no language is named in the code that computes it.  Whether the shifts separate out is then an observation about the data, not a restatement of the input.

**8.** PRELIMINARY SCOPE, AND THE COMPLETENESS GATE.  Only completed artifacts are read.  The nine acceptance grids and the three route-C behavior tables are complete and are read in full.  A value matrix is read ONLY if its own `complete` field is true -- the gate, not the file's existence, decides.  Reading a part-finished lane would produce a domain that shrinks for a reason that is not a fact about the language, which is the error this gate exists to prevent.  At this pass SEVEN matrices pass the gate (typescript, csharp, java, rust, go, swift, kotlin -- kotlin's sixth and last shard landed during this session) and two do not: cpp, which had not started, and dart, whose second shard was never queued at all, a gap rather than a wait.

**9.** THE VALUE MATRIX IS AN OVERLAY, NOT THE PRIMARY DOMAIN.  The clustering proper runs on the acceptance grids for ALL TWELVE languages.  It would be a measurement artifact to widen six languages' domains with value-matrix evidence and not the other six: every cross-language similarity involving a gated language would then move for a reason about WHICH LANE FINISHED rather than about the languages.  So the matrices are read as a separate overlay and reported as a delta.  Overturnable when all nine matrices land, at which point the overlay should simply BECOME the primary domain for the nine statically checked languages.

**10.** OVERLAY RULE, EXISTENTIAL OVER VALUES.  In an admitted matrix a (operation, lhs holder, rhs holder) cell counts as accepted if AT LEAST ONE value combination accepted -- the same existential posture as decision 2, one layer down.  A `split` cell (verdict moved with the VALUE, not the holder pair) therefore counts as accepted.  This is the widest reading and it is chosen deliberately, because the overlay's job here is to BOUND how wrong the one-value-per-holder acceptance grid could be, and a bound wants the extreme.

**11.** THE OVERLAY MEASURES THE GRID'S ERROR.  For each admitted language the count of cells where the grid and the existential overlay disagree is reported.  That number is the honest error bar on every domain in this pass, including the domains of the six languages that have no matrix yet -- there is no reason to think their grids are better behaved than the measured ones.

## per-language operation signatures

Domain size is the count of accepted ordered form pairs out of 64.

| language | operations | mean domain | widest operation | narrowest non-empty |
|---|---|---|---|---|
| go | 19 | 3.5 | == (18) | % (1) |
| rust | 19 | 4.1 | < (8) | << (1) |
| cpp | 19 | 13.3 | && (32) | % (4) |
| swift | 6 | 3.2 | < (5) | && (1) |
| dart | 17 | 14.6 | == (64) | || (2) |
| csharp | 19 | 10.3 | + (32) | && (1) |
| kotlin | 16 | 18.2 | ?: (64) | && (1) |
| java | 19 | 6.7 | + (32) | << (1) |
| typescript | 23 | 18.7 | && (64) | - (4) |
| python | 24 | 26.9 | == (64) | << (4) |
| ruby | 22 | 27.2 | == (64) | >> (2) |
| php | 26 | 44.3 | < (64) | / (12) |

## the value-matrix overlay, under the completeness gate

Decisions 8 to 11. A refused matrix contributes NOTHING; it is not
partially read.

| language | gate | pair cells | split cells | grid disagrees | operations widened |
|---|---|---|---|---|---|
| go | admitted | 7600 | 103 | 0 | 0 |
| rust | admitted | 9196 | 136 | 14 | 7 |
| cpp | REFUSED | — | — | — | — |
| swift | admitted | 3456 | 9 | 6 | 3 |
| dart | REFUSED | — | — | — | — |
| csharp | admitted | 18000 | 718 | 18 | 3 |
| kotlin | admitted | 11492 | 1234 | 150 | 2 |
| java | admitted | 20480 | 759 | 30 | 0 |
| typescript | admitted | 12167 | 876 | 704 | 8 |

## the mixed-holder statistic (decision 7)

Among accepted probes whose two holders carry the SAME form, the
fraction whose holders DIFFER. Computed without naming any
operation. Statically checked languages only — in the open-dispatch
three the number is near 1 for almost everything and says little.

| operation | mean ratio | signatures |
|---|---|---|
| `>>>` | 0.800 | 1 |
| `in` | 0.750 | 2 |
| `?:` | 0.737 | 1 |
| `<<` | 0.619 | 7 |
| `>>` | 0.619 | 7 |
| `??` | 0.521 | 3 |
| `+` | 0.482 | 7 |
| `==` | 0.446 | 8 |
| `!=` | 0.409 | 7 |
| `<` | 0.394 | 9 |
| `>` | 0.394 | 9 |
| `>=` | 0.394 | 9 |
| `-` | 0.384 | 7 |
| `%` | 0.371 | 8 |
| `<=` | 0.370 | 8 |
| `/` | 0.366 | 8 |
| `&` | 0.352 | 7 |
| `^` | 0.352 | 7 |
| `|` | 0.352 | 7 |
| `*` | 0.325 | 9 |
| `&&` | 0.207 | 9 |
| `||` | 0.207 | 9 |
| `..` | 0.083 | 2 |

### the same statistic per language, shifts against arithmetic

| language | `<<` | `>>` | `+` | `-` | `*` |
|---|---|---|---|---|---|
| go | 0.75 (12/16) | 0.75 (12/16) | 0.00 (0/7) | 0.00 (0/6) | 0.00 (0/6) |
| rust | 0.75 (12/16) | 0.75 (12/16) | 0.14 (1/7) | 0.00 (0/6) | 0.00 (0/6) |
| cpp | 0.71 (12/17) | 0.71 (12/17) | 0.64 (16/25) | 0.64 (14/22) | 0.67 (14/21) |
| swift | — | — | — | — | 0.00 (0/6) |
| dart | 0.60 (3/5) | 0.60 (3/5) | — | — | 0.50 (6/12) |
| csharp | 0.73 (8/11) | 0.73 (8/11) | 0.70 (26/37) | 0.64 (16/25) | 0.64 (16/25) |
| kotlin | — | — | 0.61 (31/51) | 0.65 (26/40) | 0.36 (4/11) |
| java | 0.80 (20/25) | 0.80 (20/25) | 0.78 (32/41) | 0.76 (22/29) | 0.76 (22/29) |
| typescript | 0.00 (0/3) | 0.00 (0/3) | 0.50 (4/8) | 0.00 (0/3) | 0.00 (0/3) |

## clusters at the 0.70 cut

- **cluster 1** — 34 members over 6 languages: `dart.==`, `kotlin.!=`, `kotlin.==`, `kotlin.?:`, `php.!=`, `php.!==`, `php.&&`, `php..`, `php.<`, `php.<=`, `php.<=>`, `php.==`, `php.===`, `php.>`, `php.>=`, `php.and`, `php.or`, `php.xor`, `php.||`, `python.!=`, `python.==`, `python.and`, `python.is`, `python.is not`, `python.or`, `ruby.!=`, `ruby.&&`, `ruby.<=>`, `ruby.==`, `ruby.===`, `ruby.||`, `typescript.&&`, `typescript.??`, `typescript.||`

- **cluster 2** — 23 members over 4 languages: `java.%`, `java.*`, `java.-`, `java./`, `java.<`, `java.<=`, `java.>`, `java.>=`, `kotlin.%`, `kotlin.*`, `kotlin./`, `ruby.**`, `ruby./`, `typescript.%`, `typescript.&`, `typescript.*`, `typescript.**`, `typescript.-`, `typescript./`, `typescript.<<`, `typescript.>>`, `typescript.^`, `typescript.|`

- **cluster 3** — 14 members over 2 languages: `cpp.!=`, `cpp.<`, `cpp.<=`, `cpp.==`, `cpp.>`, `cpp.>=`, `php.&`, `php.*`, `php.**`, `php.-`, `php.<<`, `php.>>`, `php.^`, `php.|`

- **cluster 4** — 12 members over 6 languages: `csharp.&&`, `csharp.||`, `go.&&`, `go.||`, `java.&&`, `java.||`, `kotlin.&&`, `kotlin.||`, `rust.&&`, `rust.||`, `swift.&&`, `swift.||`

- **cluster 5** — 12 members over 3 languages: `go.%`, `go.&`, `go.&^`, `go.<<`, `go.>>`, `go.^`, `go.|`, `java.<<`, `java.>>`, `java.>>>`, `rust.<<`, `rust.>>`

- **cluster 6** — 10 members over 2 languages: `cpp.%`, `cpp.&`, `cpp.<<`, `cpp.>>`, `cpp.^`, `cpp.|`, `python.&`, `python.<<`, `python.>>`, `python.^`

- **cluster 7** — 9 members over 2 languages: `cpp.<=>`, `csharp.%`, `csharp.*`, `csharp.-`, `csharp./`, `csharp.<`, `csharp.<=`, `csharp.>`, `csharp.>=`

- **cluster 8** — 8 members over 3 languages: `cpp.*`, `cpp./`, `php.%`, `php./`, `python.**`, `python.-`, `python./`, `python.//`

- **cluster 9** — 8 members over 1 languages: `dart.%`, `dart.*`, `dart./`, `dart.<`, `dart.<=`, `dart.>`, `dart.>=`, `dart.~/`

- **cluster 10** — 8 members over 3 languages: `go.*`, `go.-`, `go./`, `rust.%`, `rust.*`, `rust.-`, `rust./`, `swift.*`

- **cluster 11** — 7 members over 3 languages: `go.+`, `go.<`, `go.<=`, `go.>`, `go.>=`, `kotlin...`, `rust.+`

- **cluster 12** — 7 members over 1 languages: `rust.!=`, `rust...`, `rust.<`, `rust.<=`, `rust.==`, `rust.>`, `rust.>=`

- **cluster 13** — 6 members over 2 languages: `csharp.!=`, `csharp.==`, `typescript.!=`, `typescript.!==`, `typescript.==`, `typescript.===`

- **cluster 14** — 6 members over 2 languages: `java.&`, `java.^`, `java.|`, `rust.&`, `rust.^`, `rust.|`

- **cluster 15** — 5 members over 1 languages: `csharp.&`, `csharp.<<`, `csharp.>>`, `csharp.^`, `csharp.|`

- **cluster 16** — 5 members over 1 languages: `dart.&`, `dart.<<`, `dart.>>`, `dart.^`, `dart.|`

- **cluster 17** — 5 members over 1 languages: `python.+`, `python.<`, `python.<=`, `python.>`, `python.>=`

- **cluster 18** — 4 members over 1 languages: `kotlin.<`, `kotlin.<=`, `kotlin.>`, `kotlin.>=`

- **cluster 19** — 4 members over 1 languages: `ruby.<`, `ruby.<=`, `ruby.>`, `ruby.>=`

- **cluster 20** — 4 members over 1 languages: `typescript.<`, `typescript.<=`, `typescript.>`, `typescript.>=`

- **cluster 21** — 3 members over 1 languages: `ruby.&`, `ruby.^`, `ruby.|`

- **cluster 22** — 3 members over 1 languages: `swift.<`, `swift.>`, `swift.>=`

- **cluster 23** — 2 members over 1 languages: `cpp.&&`, `cpp.||`

- **cluster 24** — 2 members over 1 languages: `cpp.+`, `cpp.-`

- **cluster 25** — 2 members over 2 languages: `csharp.+`, `java.+`

- **cluster 26** — 2 members over 2 languages: `dart.??`, `ruby.=~`

- **cluster 27** — 2 members over 1 languages: `go.!=`, `go.==`

- **cluster 28** — 2 members over 1 languages: `java.!=`, `java.==`

- **cluster 29** — 2 members over 1 languages: `python.in`, `python.not in`

- **cluster 30** — 2 members over 1 languages: `ruby.+`, `ruby.-`

## relation edges — a sample of each kind

- **overlaps** — `cpp.!=` vs `csharp.!=`, jaccard 0.571. only-in-first: `fractional|truth`, `truth|fractional`, `truth|whole`, `whole|truth`. only-in-second: `keyed|keyed`, `keyed|nothing`, `nesting|nesting`, `nesting|nothing`.

- **overlaps** — `cpp.!=` vs `csharp.==`, jaccard 0.571. only-in-first: `fractional|truth`, `truth|fractional`, `truth|whole`, `whole|truth`. only-in-second: `keyed|keyed`, `keyed|nothing`, `nesting|nesting`, `nesting|nothing`.

- **overlaps** — `cpp.!=` vs `dart.*`, jaccard 0.500. only-in-first: `fractional|truth`, `sequence|nothing`, `sequence|sequence`, `text|text`. only-in-second: `nothing|keyed`, `nothing|nesting`, `nothing|truth`, `text|whole`.

- **nested_by** — `cpp.!=` vs `php.!=`, jaccard 0.312. only-in-first: none. only-in-second: `fractional|keyed`, `fractional|nesting`, `fractional|sequence`, `fractional|text`.

- **nested_by** — `cpp.!=` vs `python.!=`, jaccard 0.312. only-in-first: none. only-in-second: `fractional|keyed`, `fractional|nesting`, `fractional|sequence`, `fractional|text`.

- **nests** — `cpp.!=` vs `python.-`, jaccard 0.500. only-in-first: `fractional|nothing`, `nothing|fractional`, `nothing|nothing`, `nothing|sequence`. only-in-second: none.

- **nested_by** — `cpp.!=` vs `ruby.!=`, jaccard 0.312. only-in-first: none. only-in-second: `fractional|keyed`, `fractional|nesting`, `fractional|sequence`, `fractional|text`.

- **nests** — `cpp.%` vs `go.%`, jaccard 0.250. only-in-first: `truth|truth`, `truth|whole`, `whole|truth`. only-in-second: none.

- **nests** — `cpp.%` vs `java.&`, jaccard 0.500. only-in-first: `truth|whole`, `whole|truth`. only-in-second: none.

- **equals** — `cpp.%` vs `python.<<`, jaccard 1.000. only-in-first: none. only-in-second: none.

- **equals** — `cpp.%` vs `python.>>`, jaccard 1.000. only-in-first: none. only-in-second: none.

- **equals** — `cpp.&` vs `python.<<`, jaccard 1.000. only-in-first: none. only-in-second: none.

- **contradicts** — `cpp.||` vs `dart.||`, jaccard 0.000. only-in-first: `fractional|fractional`, `fractional|nothing`, `fractional|sequence`, `fractional|text`. only-in-second: `nothing|nothing`, `nothing|truth`.

- **contradicts** — `csharp.||` vs `dart.||`, jaccard 0.000. only-in-first: `truth|truth`. only-in-second: `nothing|nothing`, `nothing|truth`.

- **contradicts** — `dart.||` vs `go.||`, jaccard 0.000. only-in-first: `nothing|nothing`, `nothing|truth`. only-in-second: `truth|truth`.
