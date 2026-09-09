# log 045 — the threshold spectrum, one merge tree per coordinate family

2026-08-20. Node: `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering`.
**No probe ran and no lane ran** — everything here is assembly over the
extended matrix log 044 already put on disk (`matrix_extended.json`,
`matrix_extended_base.csv`). the owner ruled the design in conversation the
same day; it is recorded here as SETTLED, not proposed: one dendrogram
per COORDINATE FAMILY, a shared threshold slider, and the congruences
drawn as typed cross-links overlaid on whichever tree is showing.

Vocabulary is the node's: **super-node / sub-node / co-node / sub-tree**
only, never parent/child/sibling; the stopped-process outcome element is
**ABORT**, never death/kill. Third-party keys (`death:` token prefixes in
the underlying answer files, `=== mod 2^w` relation strings) are quoted
as theirs.

## 0. glossary — this log's own words, each tied to the data

- **coordinate family.** One of the five coordinates the decomposition
  carries, each getting its own tree: **form** (the 64 base cells, form
  sets), **sign**, **mant** (the exact absolute value), **container**
  (sorted-values with key-format and order-flag folded), **text** (bytes
  / codepoint-length / grapheme-length / NFC). A leaf is a `lang.op`
  column; similarity is measured BETWEEN columns over that one
  coordinate. Example: in the **mant** family `cpp.&` and `cpp.bitand`
  sit at similarity 1.000 because on every shared input cell their exact
  absolute values are identical — same magnitude, so the mant coordinate
  never disagrees.
- **cross-link.** A typed edge between two columns, drawn as an arc under
  the icicle, carrying a wrap relation and NOT a distance. Example:
  `go.+ ~ python.+` on 27 input cells carries `sign flip, mant sum =
  2^64 (=== mod 2^64)` — go's signed int64 result and python's unbounded
  result are complements to the modulus. It is an edge, never a merge
  height (the one exception is inside the mant tree, below).
- **merge height.** The similarity at which two clusters join — a
  super-node's `birth`. Reading down the form tree, `cpp.!=` and `cpp.==`
  join at height 1.000 (identical form behaviour), while the whole tree's
  last two super-nodes join at height 0.0589. A tall band between two
  heights is a stable cluster; a sliver is an artefact of where the line
  sits.
- **threshold slice.** The horizontal cut the dashed line makes; every
  cluster it crosses is one reading. At slice 0.700 the form tree shows
  its clusters outlined in yellow and the live count updates as the line
  is dragged. There is NO chosen slice — the sweep is the result.

## 1. what was built

- `Research/kind_fuzz_clustering/l3_dendro_extended.py` — the assembler,
  in the l3_* family. It reads `matrix_extended.json` (and the base CSV
  where the form cell is simpler), computes the five per-family
  column-pair similarity matrices, runs average linkage (UPGMA, the exact
  Lance-Williams running mean so a group average is never recomputed),
  sweeps each tree, and emits both the JSON and the explorer HTML with the
  data inlined — the same generate-both pattern
  `make_dendrogram_answers.py` uses.
- `Research/kind_fuzz_clustering/dendro_extended.json` (1.90 MB) — per
  family: `leaves`, `merge_history` (heights), `cluster_count_curve`,
  `stability_plateaus`, the icicle `tree` (bands per node), and the
  `crosslinks` filtered to that family's leaves.
- `Research/kind_fuzz_clustering/dendrogram_extended.html` (1.92 MB) —
  one self-contained file, inline JS/CSS, no CDN, opens from `file://`,
  the data embedded inline as `const DENDRO = {…}` exactly the way
  `dendrogram_answers.html` embeds its `const TREE`. Icicle per family,
  draggable dashed threshold line with the live cluster count, a family
  toggle (five buttons), search, the cluster-count-versus-threshold curve
  with plateaus shaded, the widest-plateau table, and the congruence
  cross-links as arcs — off by default, toggled on, coloured teal, the
  relation string on hover, and highlighted pink when a search touches an
  endpoint.
- `Research/kind_fuzz_clustering/verify_dendro_extended.js` — the
  headless check (below).

The similarity definitions, each a numbered overturnable DECISION in the
script's docstring: form is the mean per-row Jaccard of the two form
sets over the rows both columns probed, UNPROBED rows excluded from both
sides; sign / mant / container / text are the mean per-shared-input-cell
score; a mant pair that a recorded congruence links scores 1.0 on that
cell (a match with a note — **the only place a congruence touches a
height**); container folds 0.6·sorted-values + 0.2·key-format +
0.2·order-flag; text is the equal-weight mean of the four layer Jaccards.

## 2. sanity checks, as printed

```
  239 columns, 37915 congruence records -> 4919 column-pair cross-links
  [form] 239 leaves, 238 merges, 0.5s
  [sign] 129 leaves, 128 merges, 0.1s
  [mant] 129 leaves, 128 merges, 0.1s
  [container] 31 leaves, 30 merges, 0.0s
  [text] 32 leaves, 31 merges, 0.0s
SANITY CHECKS
  [leaves] form      239 leaves
  [leaves] sign      129 leaves
  [leaves] mant      129 leaves
  [leaves] container  31 leaves
  [leaves] text       32 leaves
  [form] go.+ ~ rust.+ pairwise form similarity = 0.9922 ; first shared cluster at threshold 0.9922
  [mant] go.+ ~ python.+ cross-link: sign flip, mant sum = 2^64 (=== mod 2^64)  (w=64, 27 records)
  [text] 9 text-family leaves end in '.+' (concatenation): cpp.+, csharp.+, go.+, java.+, kotlin.+, python.+, ruby.+, rust.+, typescript.+
        pairwise text similarity among the '.+' columns: median 0.369  lowest 0.080  highest 1.000
        cpp.+ ~ csharp.+ first shared cluster at threshold 0.2672
WIDEST PLATEAUS (per family, top 3)
  [form] 0.06..0.17 w=0.11 2c | 0.28..0.38 w=0.10 6c | 0.00..0.05 w=0.05 1c
  [sign] 0.00..0.47 w=0.47 1c | 0.58..0.62 w=0.04 6c | 0.71..0.74 w=0.03 15c
  [mant] 0.00..0.17 w=0.17 1c | 0.27..0.32 w=0.05 5c | 0.18..0.22 w=0.04 2c
  [container] 0.01..0.16 w=0.15 3c | 0.46..0.56 w=0.10 10c | 0.17..0.24 w=0.07 4c
  [text] 0.76..0.95 w=0.19 15c | 0.45..0.63 w=0.18 12c | 0.64..0.73 w=0.09 13c
```

The three named checks PASS. **form**: `go.+` and `rust.+` land at form
similarity **0.9922** and share a cluster from threshold 0.9922 down —
log 033 measured them at 0.907 at the answer grain, and at the pure form
grain they are closer still, because rust's panic and go's wrap accept
the same forms even where they compute different values; the coordinate
that separates them is not the form. **mant**: the `go.+ ~ python.+`
cross-link exists and reads `sign flip, mant sum = 2^64 (=== mod 2^64)`,
w = 64, over 27 input cells — the int64 wrap surfacing as a sign-flip
edge, exactly log 044's postscript-2 spelling. **text**: nine columns
end in `.+` and concatenate a string; they cohere (see §3).

Per-family leaf counts, recorded: **form 239** (every column has at least
one probed base cell), **sign 129**, **mant 129** (the numeric columns —
sign and mant stand on the same 129), **container 31**, **text 32**.
Columns with no cell of a family are ABSENT, not forced in: 110 columns
carry no numeric cell and are off the sign and mant trees, 208 carry no
container cell, 207 no text cell.

## 3. per-family headline readings — what merges first, what never merges

- **form (239 leaves).** First merge at 1.000 is `cpp.!=` with `cpp.==` —
  identical accepted-form behaviour. The tree never fully coheres: the
  root joins two super-nodes of 150 and 89 at height **0.0589**, and the
  widest plateau holds just **2 clusters over [0.06, 0.17]** — the form
  coordinate splits the vocabulary into two broad families and no
  finer stable reading survives at the coarse end. `go.+` and `rust.+`
  are the tight pair the check names.
- **sign (129 leaves).** First merge at 1.000 is `cpp.&` with `cpp.bitand`
  — a spelling twin, same sign on every shared cell. The sign coordinate
  is the most agreeable of the five: its widest plateau is **one cluster
  across [0.00, 0.47]**, meaning the numeric columns broadly agree on
  sign and the tree stays joined until the threshold climbs past 0.47.
  What never merges cleanly are the comparison operators, whose sign
  coordinate is `not-applicable` on the boolean they return — they carry
  sign only where an operand leaks through.
- **mant (129 leaves).** First merge at 1.000, again `cpp.&`/`cpp.bitand`.
  The root joins at **0.1747**, lower than sign's 0.4765: exact
  magnitudes disagree far more readily than signs do, which is the point
  of separating the two coordinates. The congruence layer is doing its
  work here — 4,919 cross-links lift would-be mismatches to matches with
  a note, and without them the wrapping arithmetic operators would read
  as pure disagreement.
- **container (31 leaves).** First merge at 1.000 is `cpp.+` with
  `ruby.+` — same sorted values, key format and order flag. Two columns,
  **`kotlin…` and `python.**`, join the root only at height 0.000**:
  they share no container input cell with the rest, so the tree cannot
  place them and says so rather than inventing a height. The widest
  stable reading is 3 clusters over [0.01, 0.16].
- **text (32 leaves).** First merge at 1.000 is `cpp.+` with `go.+`. The
  root splits at **0.0935** into two coherent halves, and the split is
  legible: the 11-column side is the **string producers** — all nine
  `.+` concatenation columns plus php's `.` concat operator and ruby's
  `<<` append — while the 21-column side is the **text-by-selection**
  operators (`||`, `??`, `?:`, `and`, `%`, `*` returning a text operand).
  So "concatenation columns cohere" holds in the strong form: they are a
  single sub-tree, separated from the operators that merely pass a text
  value through.

## 4. where the data resisted

- **The `.+` columns cohere as a sub-tree but not as a tight cluster.**
  Pairwise text similarity among the nine is median **0.369**, lowest
  0.080, highest 1.000 — they share the string-producing behaviour that
  puts them all on the 11-column side of the root, but they disagree on
  the byte/codepoint/grapheme layers wherever the languages concatenate
  different alphabets or normalize differently. The coherence is
  topological (one sub-tree), not metric (one plateau); stated so it is
  not over-read.
- **Two container columns have no shared cell at all** — `kotlin…` and
  `python.**` join the root at height 0.000. A join at zero is the
  tree's way of saying "not comparable in this family", the same honesty
  log 037 gave the one-slot constructs; it is not a similarity of zero
  that was measured, it is the absence of a shared cell.
- **All 37,915 congruence records collapse to 4,919 column-pair
  cross-links, and every endpoint is numeric.** The form tree carries all
  239 leaves but the cross-links only touch the 129 numeric ones, so the
  same 4,919 arcs appear on the form, sign and mant trees. The container
  and text trees show fewer — 343 and 394 — not placeholders but the real
  subset whose BOTH endpoint columns also hold a cell of that family: a
  column like `python.*` carries numeric cells (so it earns congruences)
  AND container and text cells (so it is a leaf of those trees too), and
  its within-column int128 wrap (`sign flip, mant sum = 2^127`, 12
  records) surfaces as a self-arc on the container tree. So a wrap
  relation measured on a numeric input cell can be drawn over a container
  or text tree wherever the same columns reach into that family — the arc
  is the numeric fact, overlaid, never a container or text distance.
  Drawn cap is the 2,000 strongest by w, noted on the page.
- **Sign is far more agreeable than mant, and that asymmetry is the
  finding the two-coordinate split exists to show.** Sign's root joins at
  0.4765 and mant's at 0.1747; a single numeric distance would have
  averaged the two and hidden that columns agree about direction long
  after they stop agreeing about magnitude.
- **The congruence-as-height lift is confined to mant by construction.**
  It was tempting to let a congruence also pull the sign tree together
  (a wrap IS a sign flip), but a sign flip is a genuine sign
  disagreement — the feature — so the lift stays out of sign and only
  rescues magnitude in mant. Recorded as decision 3, overturnable.

## 5. verification

No jsdom is present (logs 012/014 used it), so the headless check is
DOM-less: `verify_dendro_extended.js` pulls the inline `const DENDRO`
straight out of the HTML the way a browser parse would and runs the two
independent cluster-count methods the page carries — a band-walk over the
tree nodes against a count off the merge history — asserting they agree
**at all 101 thresholds for every family**. It also asserts leaf counts
agree three ways (`n_leaves` == leaf list == leaf nodes == merges + 1),
merge heights are monotone non-increasing, leaf positions are contiguous
`0..n-1`, every cross-link endpoint is a real leaf, the standalone JSON
matches the embed, and the two named readings (the `go.+ ~ python.+`
mod-2^64 cross-link, `go.+`/`rust.+` both form leaves). **All checks pass.**
Real-browser interaction (drag, hover, arc rendering) is unverified, as
every prior explorer log has said of its own.

## 6. bookkeeping

PROGRESS carries a dated entry (log 045). CHECK is untouched: the
extended matrix is log 044's same-day ruling and carries no tracked
CHECK phase, so this visual — its downstream — has no matching open item,
exactly as log 044 recorded for the matrix itself. Said rather than
dropped.
