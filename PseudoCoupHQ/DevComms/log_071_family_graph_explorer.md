# log 071 — the family graph explorer: the two rulings, made decidable by eye

2026-08-24. **A PICTURE OF MEASUREMENTS. Nothing structural is decided
here — no threshold is ruled, no name is coined, neither reading of
§1.6 is chosen.** No probe was run, no lane was submitted;
`matrices_full_v2/` and `dominant_operators_v1.json` are read-only to
this log.

Read first: `PRIVATE/PseudoCoupHQ/CLAUDE.md` (the vocabulary bans
and the explorer requirements, both binding),
`DevComms/log_069_disagreement_kind_classifier.md` (the ruled
classifier),
`DevComms/log_070_dominant_operators_all.md` (the families and every
number this log re-derives),
`DevComms/STANDING_RULINGS_AWAITING_DEE.md` §1.5 and §1.6 (the two
rulings this exists to make decidable).

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

Products, all under
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`:

| product | what it is |
| --- | --- |
| `family_graph_explorer_v1.html` | **the explorer.** 11.5 MB, ONE self-contained file, data embedded, no CDN, no external URL of any kind, no `position: fixed` |
| `family_graph_explorer_v1.src.html` | the same page with `__DATA__` where the data goes — the maintainable source |
| `build_family_graph.py` | the builder; classifies every pair from `matrices_full_v2/` and splices the page. 13 s under `nice -n 15`, 421 MB peak |
| `family_graph_v1.json` | 11.4 MB, the embedded data standalone, queryable |
| `verify_family_graph.js` | the headless verifier, on `verify_row_graph_v5.js`'s pattern. 47 s |

---

## 1 — WHAT IS DRAWN

**NODES = the 4,077 IDENTITY (CONTRACT) families of log_070** — profiles
with byte-identical full-grid vectors. Equality is transitive, so there
is no clique test and no chaining hazard in the nodes themselves. Each
node carries, straight out of `dominant_operators_v1.json` and
byte-identical to it: its members, its gate block (form pair + level),
its named mode or `UNCLASSIFIED` / `NON-DISCRIMINATING` (with the
`consistent_with` set when it has one), the spellings its members use,
its languages, its member windows, its output form signature, and its
member count.

**CONNECTORS = the disagreement-kind relation** between families inside
one gate block, re-derived cell by cell by the rule log_069 ruled. Four
kinds, each **separately toggleable**, each with **its own colour AND
its own dash pattern**, so they are distinguishable without colour:

| kind | colour | dash | what it means |
| --- | --- | --- | --- |
| WINDOW-only | blue `#4f9cf0` | solid | one side declines where the other answers, never a value clash — same behaviour, narrower holder |
| VALUE-only | red `#e6553f` | long dash `11,5` | both answer, values differ — a real mode boundary |
| MIXED | violet `#b57ee0` | dotted `2,5` | both kinds present — needs the region test |
| DECLINE-KIND | amber `#e0b83e` | dash-dot `10,3,2,3` | both declined, with DIFFERENT declines — §1.5's fourth kind |
| refused WINDOW pair | dim blue | fine dot `1,6` | WINDOW-only with ZERO comparable value cells — the settled decline rule says NO connector; drawn only on request, **never counted, never in the layout** |

Internal connectors tether each member profile to its family node with a
near-zero spring (0.0006 against 0.035 external, 58x weaker). They are
never cut by a control and never counted.

Per gate block, what exists and what is drawn by default:

| gate block | families | member sub-nodes | WINDOW-only connectors | refused | VALUE-only | DECLINE-KIND | MIXED | default drawn | block pairs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fractional\|fractional/L1 | 270 | 791 | 433 | 2096 | 5432 | 34 | 28320 | 5899 | 36315 |
| fractional\|fractional/L2 | 241 | 717 | 434 | 2270 | 3879 | 42 | 22295 | 4355 | 28920 |
| fractional\|truth/L1 | 134 | 206 | 217 | 1274 | 787 | 7 | 6626 | 1011 | 8911 |
| fractional\|truth/L2 | 127 | 202 | 112 | 1380 | 647 | 22 | 5840 | 781 | 8001 |
| fractional\|whole/L1 | 305 | 935 | 891 | 1794 | 3018 | 16 | 40641 | 3925 | 46360 |
| fractional\|whole/L2 | 198 | 833 | 454 | 970 | 1821 | 11 | 16247 | 2286 | 19503 |
| truth\|fractional/L1 | 146 | 206 | 184 | 1514 | 766 | 1 | 8120 | 951 | 10585 |
| truth\|fractional/L2 | 139 | 202 | 155 | 1614 | 688 | 10 | 7124 | 853 | 9591 |
| truth\|truth/L1 | 85 | 186 | 160 | 464 | 412 | 0 | 2534 | 572 | 3570 |
| truth\|truth/L2 | 78 | 183 | 116 | 562 | 361 | 10 | 1954 | 487 | 3003 |
| truth\|whole/L1 | 182 | 281 | 380 | 1871 | 946 | 1 | 13273 | 1327 | 16471 |
| truth\|whole/L2 | 140 | 276 | 182 | 1475 | 771 | 7 | 7295 | 960 | 9730 |
| whole\|fractional/L1 | 314 | 935 | 889 | 1848 | 3137 | 16 | 43251 | 4042 | 49141 |
| whole\|fractional/L2 | 209 | 833 | 467 | 2015 | 1878 | 29 | 17347 | 2374 | 21736 |
| whole\|truth/L1 | 174 | 281 | 579 | 1839 | 1069 | 6 | 11558 | 1654 | 15051 |
| whole\|truth/L2 | 138 | 276 | 130 | 2106 | 837 | 45 | 6335 | 1012 | 9453 |
| **whole\|whole/L1** | **712** | **2001** | **6476** | **3535** | **5302** | **121** | **237682** | **11899** | **253116** |
| whole\|whole/L2 | 485 | 1733 | 4113 | 2852 | 3343 | 104 | 106958 | 7560 | 117370 |
| **total** | **4077** | **11077** | **16372** | **31479** | **35094** | **482** | **583400** | **51948** | **666827** |

Every column reproduces log_070 §1 and §5 exactly; the builder asserts
it and the verifier re-derives it from the CSVs.

---

## 2 — THE RENDERING CAPS, STATED RATHER THAN SILENT

4,077 nodes and 666,827 connectors will not render usefully. Five caps
are in force. **Every one of them is announced in the page itself, in
the status line and in the rule line, with both numbers — what is shown
and what exists. Nothing is silently truncated.**

| # | cap | what it does | how the page says so |
| --- | --- | --- | --- |
| 1 | **one gate block at a time** | the view is ONE `(form_pair, level)` block; the default is `whole\|whole` L1, where every named family lives. **712 of 4,077 nodes.** | the selector lists all eighteen with their family counts; the status line names the block's families and profiles |
| 2 | **MIXED off by default** | MIXED is 87.5% of all pairs and 237,682 of `whole\|whole` L1's 253,116. Default view draws WINDOW-only + VALUE-only + DECLINE-KIND = **11,899 of 253,116 pairs** | the rule line always states all four per-kind counts for the block, drawn or not |
| 3 | **draw cap, default 40,000** | selectable 2,000 / 10,000 / 40,000 / no cap. Applies to DRAWING AND LAYOUT only | when in force: `DRAW CAP IN FORCE: 249581 connectors pass, the first 40000 in kind order are DRAWN, 209581 are not` — and the status line reads `40000 of 249581 connectors drawn [CAP]` |
| 4 | **counts are never capped** | every count in the status line, and **every component count**, is computed over the FULL passing set, never over the drawn subset | the rule line says so in the same sentence as the cap |
| 5 | **MIXED carries no per-cell split** | a MIXED connector embeds only its disagreeing-cell count, not the value/window/token split. This is a FILE-SIZE cap: carrying the split for all 583,400 would add ~9 MB. The three rare kinds carry the full split | the MIXED tooltip says the split is not embedded and points here |

Cap 3 takes the connectors **in kind order** — WINDOW-only, then
VALUE-only, then DECLINE-KIND, then MIXED — so the three rare kinds are
never the ones dropped. That is the only ordering decision in the cap
and it is mechanical.

---

## 3 — §1.6, MADE DECIDABLE: IS WINDOW-ONLY MERGING TRANSITIVE?

### the two readings, side by side, in the panel

The left panel of every block opens with both numbers, labelled and
**neither chosen**:

| gate block | WINDOW-only components | multi-node | largest | not a clique | maximal cliques | components that SPAN census names |
| --- | --- | --- | --- | --- | --- | --- |
| fractional\|fractional/L1 | 110 | 30 | 15 | 12 | 155 | 0 |
| fractional\|fractional/L2 | 72 | 29 | 31 | 12 | 133 | 0 |
| fractional\|truth/L1 | 47 | 23 | 29 | 8 | 79 | 0 |
| fractional\|truth/L2 | 61 | 22 | 13 | 4 | 81 | 0 |
| fractional\|whole/L1 | 79 | 42 | 19 | 12 | 108 | 0 |
| fractional\|whole/L2 | 64 | 20 | 16 | 9 | 94 | 0 |
| truth\|fractional/L1 | 54 | 26 | 13 | 12 | 78 | 0 |
| truth\|fractional/L2 | 59 | 26 | 12 | 5 | 80 | 0 |
| truth\|truth/L1 | 13 | 8 | 41 | 6 | 61 | 0 |
| truth\|truth/L2 | 19 | 10 | 34 | 6 | 57 | 0 |
| truth\|whole/L1 | 36 | 20 | 25 | 11 | 78 | 0 |
| truth\|whole/L2 | 54 | 22 | 14 | 10 | 77 | 0 |
| whole\|fractional/L1 | 87 | 44 | 19 | 11 | 116 | 0 |
| whole\|fractional/L2 | 72 | 22 | 16 | 9 | 102 | 0 |
| whole\|truth/L1 | 24 | 14 | 36 | 13 | 101 | 0 |
| whole\|truth/L2 | 65 | 20 | 12 | 11 | 85 | 0 |
| **whole\|whole/L1** | **61** | **38** | **72** | **22** | **42324** | **5** |
| whole\|whole/L2 | 42 | 18 | 234 | 14 | 28779 | 3 |
| **total** | **1019** | | | | **72588** | **8** |

`whole|whole` L1: **61 groups by component, largest 72 — against 42,324
by maximal clique.** A component is a partition; a maximal-clique cover
is not. The two readings' consequences are on the screen together.

The census names live only in `whole|whole`, which is why the
mode-spanning column is zero everywhere else; those blocks carry no
guarantee vocabulary at all (log_070 §11 tier C).

### the control that makes the chain findable

Three ways in, any one of which lands on it:

1. **the "§1.6 chain" button.** One click: switches to
   `whole|whole` L1, turns WINDOW-only and VALUE-only on, sets colour to
   "by named mode" and highlight to "MODE-SPANNING WINDOW-only
   components only", selects the three families, draws the two hops in
   bright blue and the direct comparison in red, and writes the numbers
   into the panel.
2. **the component panel.** Every multi-node WINDOW-only component is
   listed; the ones that span more than one census name are flagged
   `SPANS MODES` with a red edge and name the modes. Click one and it is
   selected and fitted.
3. **the search box.** Typing `csharp.+ short x short` matches exactly
   the middle family of the chain (verified).

### what the picture shows

| step | family | member quoted | named mode | connector to the next |
| --- | --- | --- | --- | --- |
| 0 | `whole\|whole/L1#531` | `php.+ int x int` | add approximating | WINDOW-only, 207 window cells over 49 comparable |
| 1 | `whole\|whole/L1#390` | `csharp.+ short x short` | NON-DISCRIMINATING, consistent with add approximating / add growing / add wrapping | WINDOW-only, 207 window cells over 49 comparable |
| 2 | `whole\|whole/L1#260` | `cpp.+ int64_t x int64_t` | add wrapping | — |

Compared **directly**, families #531 and #260 are **VALUE-only at 35
value cells over 256 comparable** — the classifier calls that pair
DIFFERENT modes. The two hops run through a family whose declared
holder never reaches its own fracture inside the X set.

All three sit in ONE WINDOW-only component of **29 families / 96
profiles**. This is exactly log_070 §5 and STANDING RULINGS §1.6.

**Seeing that a component spans different named modes** is the point of
the colour mode "by named mode": one connected blob painted in two or
three mode colours. Every such component in the run:

| gate block | families | profiles | census names in the ONE component | spellings | a clique? |
| --- | --- | --- | --- | --- | --- |
| whole\|whole/L1 | 57 | 96 | mod Euclidean (F-i4), mod dividend-sign (F-i4), mod divisor-sign (F-i4) | `%` | **no** |
| whole\|whole/L1 | 55 | 88 | div flooring (F-i3), div truncating (F-i3) | `/` `//` `~/` | **no** |
| whole\|whole/L1 | 36 | 100 | mul approximating, mul growing, mul wrapping | `&*` `*` | **no** |
| whole\|whole/L1 | 29 | 96 | sub approximating, sub wrapping | `&-` `-` | **no** |
| whole\|whole/L1 | 29 | 96 | add approximating, add wrapping | `&+` `+` | **no** |
| whole\|whole/L2 | 234 | 514 | div flooring, div truncating, all three mods, mul growing, mul wrapping | `%` `&*` `*` `/` `//` `<<` `>>` `>>>` `~/` | **no** |
| whole\|whole/L2 | 26 | 96 | sub approximating, sub wrapping | `&-` `-` | **no** |
| whole\|whole/L2 | 26 | 96 | add approximating, add wrapping | `&+` `+` | **no** |

**A reading limit, stated not hidden.** This table names only the
DEFINITE census names in a component. log_070 §5 reports the add group
as swallowing *add wrapping, add growing and add approximating* — the
`growing` arrives through the NON-DISCRIMINATING families whose
`consistent_with` set includes it, `whole|whole/L1#390` among them. The
explorer carries `consistent_with` in the node tooltip, so the third
name is one hover away; it is not counted as a definite name because
log_070 did not name it one. **None of these components is a clique.**

---

## 4 — §1.5, MADE VISIBLE: THE FOURTH DISAGREEMENT KIND

**DECLINE-KIND is drawn as its own kind, with its own colour and its own
dash, and its own toggle** — independently of the other three. Its
extent is therefore visible directly: 482 pairs across the run, 121 of
them in `whole|whole` L1, 0 in `truth|truth` L1, per the table in §1.

The "§1.5 witness" button selects the pair log_069 §7 and log_070 §4
both quote:

| pair | disagreements | value clashes | window | decline-vs-different-decline | comparable cells |
| --- | --- | --- | --- | --- | --- |
| `cpp.% int32_t x int32_t` vs `csharp.% int x int` | 10 | 0 | 0 | 10 | 71 |

Two families that agree at every one of the 71 keys where both answer,
and differ only in HOW they declined the other 10. Under the classifier
as ruled they have no kind; here they have a colour, a dash, a toggle
and a count. **Flagged, not decided.**

---

## 5 — THE BINDING EXPLORER REQUIREMENTS, CHECKED AGAINST `CLAUDE.md`

`CLAUDE.md` "explorer requirements, already fixed — preserve them"
carries **four** bullets. Each, and what was done:

| requirement, as written in `CLAUDE.md` | status |
| --- | --- |
| "Autofit runs ONCE and never again; any wheel or mousedown disables it permanently; a 'fit view' button exists." | held; verified, including that clearing the once-only flag does not resurrect it after a wheel or a mousedown |
| "Internal connector springs near zero — they tether a row to its operator node visually and must never dominate the layout." | held; 0.0006 against 0.035 |
| "Threshold slider cuts EXTERNAL connectors only; components are counted on external connectors only." | held; verified at five kind/slider settings against an independent union-find |
| "Self-contained single file, data embedded, no CDN." | held; the verifier refuses any `<script src` or any `://` in the page |

Two notes, both recorded rather than decided:

- **"never `position: fixed`" is NOT in `CLAUDE.md`.** It arrived in the
  work order for this log. It is honoured anyway — the tooltip is
  `position: absolute` inside a `position: relative` stage — and the
  verifier enforces it. Whether it belongs in `CLAUDE.md` is the owner's.
- **the internal connector tethers a MEMBER PROFILE to its FAMILY
  node**, not a row to an operator node: this graph has no operator
  nodes. Same requirement, same near-zero spring, adapted to the objects
  this picture draws. Mechanical, recorded here for audit.

---

## 6 — THE VERIFIER, AND ITS OUTPUT

`verify_family_graph.js` follows `verify_row_graph_v5.js` exactly: a
canvas-shaped stub RUNS the page's own single inline script verbatim,
and everything the picture stands on is re-derived independently of the
python — the families re-contracted from the CSVs, every pair
re-classified cell by cell, components by an independent union-find,
maximal cliques by an independent Bron-Kerbosch.

Run with `node verify_family_graph.js` in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`. 47 s,
2.7 GB peak. Verbatim:

```
verify_family_graph -- headless checks on the dominant-operator family graph (identity families, the ruled disagreement kinds, both readings of 1.6)
  [self-contained] no <script src>, no URL of any kind anywhere in the page -- data embedded, NO CDN
  [layout] no `position: fixed` anywhere in the page
  [script] the page's ONE inline script ran with no throw
  [embed] the embedded data is BYTE-IDENTICAL to family_graph_v1.json (11,424,310 chars, 18 gate blocks, 4,077 families, 11,077 profiles)
  [nodes] all 4,077 identity families -- id, members, named mode, spellings, languages, member windows, cell counts -- are byte-identical to dominant_operators_v1.json
  [read] 11,077 profiles in 479 matrices read from matrices_full_v2/ and grouped into 18 gate blocks in 42.9 s
  [contract] the identity partition re-derived from scratch out of the CSVs is EXACTLY the one drawn -- 4,077 families, same members and the same `block#i` id every time (equality is transitive, so no clique test)
  [kinds] every pair re-classified cell by cell from the CSVs by the ruled classifier: 439,520 level-1 pairs EXHAUSTIVELY, 17,489 level-2 pairs on a deterministic 1-in-13 sample -- kind, disagreeing cells, value clashes, window cells, decline-vs-different-decline and comparable cells all agree with what is drawn
  [decline rule] every kept WINDOW-only connector has at least one comparable value cell and every refused one has none -- zero comparable keys means NO connector, not a zero-weight one
  [kind totals] WINDOW-only 47,851, VALUE-only 35,094, MIXED 583,400, DECLINE-KIND 482 -- identical to dominant_operators_v1.json and to log_070's table
  [live] W=1 V=1 M=0 D=1 minND=0: 11,899 external connectors, 6 components (4 multi-node, largest 693) -- page and independent union-find agree
  [live] W=1 V=0 M=0 D=0 minND=0: 6,476 external connectors, 61 components (38 multi-node, largest 72) -- page and independent union-find agree
  [live] W=1 V=1 M=1 D=1 minND=0: 249,581 external connectors, 2 components (2 multi-node, largest 707) -- page and independent union-find agree
  [live] W=1 V=1 M=0 D=1 minND=40: 10,982 external connectors, 8 components (3 multi-node, largest 693) -- page and independent union-find agree
  [live] W=0 V=1 M=0 D=0 minND=0: 5,302 external connectors, 113 components (67 multi-node, largest 39) -- page and independent union-find agree
  [filters] every kind toggle and every slider position left the 2,001 internal connectors untouched -- the filters cut EXTERNAL connectors ONLY, and components are counted on external connectors only
  [refused] showing the 3,535 refused WINDOW-only pairs of whole|whole/L1 changes NO component count and no layout -- they are drawn as evidence, never as connectors
  [1.6 components] in all 18 gate blocks the WINDOW-only component count, the largest component, the kept and refused edge counts and the maximal-clique count agree with log_070's relaxation table, recomputed by an independent union-find here
  [1.6 cliques] an independent Bron-Kerbosch on whole|whole/L1 gives 42,324 maximal cliques against 61 connected components (largest 72) -- the two readings, side by side, NEITHER chosen
  [1.6 chain] on whole|whole/L1: `php.+ int x int` (add approximating) --WINDOW-only(207 window cells over 49 comparable)--> `csharp.+ short x short` (NON-DISCRIMINATING) --WINDOW-only(207/49)--> `cpp.+ int64_t x int64_t` (add wrapping); compared DIRECTLY the two ends are VALUE-only at 35 value cells over 256 comparable.  All three sit in ONE WINDOW-only component of 29 families / 96 profiles carrying the census names add approximating + add wrapping -- the component SPANS named modes
  [1.6 findable] that component is listed in the page's own component panel and flagged SPANS MODES (5 of 38 multi-node components are)
  [1.6 control] the page's "1.6 chain" button selects exactly the three families, draws the two hops and the direct VALUE-only comparison, and writes the numbers into the panel
  [1.6 search] typing `csharp.+ short x short` into the search box matches exactly the middle family of the chain
  [1.5 witness] `cpp.% int32_t x int32_t` against `csharp.% int x int` on whole|whole/L1: 10 cells where both declined with DIFFERENT declines, 0 value clashes, 0 window cells, over 71 comparable cells
  [1.5 extent] all 482 DECLINE-KIND pairs of the run are drawn as their own separately toggleable kind, with their own colour AND their own dash
  [1.5 control] the page's "1.5 witness" button selects the pair and reports its cell counts
  [blocks] all 18 gate blocks load from the selector, each showing its own family count and its own per-kind pair counts out of the block's total pairs
  [cap] with MIXED on, 249,581 connectors pass and the cap draws 40,000: the page says so in both the status line ("40000 of 249581 connectors drawn [CAP]") and the rule line, and names the 209,581 not drawn -- NOTHING is silently truncated
  [autofit] runs ONCE and never again; a wheel disables it permanently and so does a mousedown, even after the once-only flag is cleared; the fit view button still works
  [springs] internal 0.0006 against external 0.035 -- a member sub-node is TETHERED to its family node, 58x weaker, and can never dominate the layout
  [vocabulary] none of parent / child / children / sibling / ancestor / descendant / orphan / death / kill / died / dead appears anywhere in the page's own text
ALL CHECKS PASSED
```

**The one place the verifier is not exhaustive, named rather than
buried.** Level-1 blocks — 439,520 pairs — are re-classified cell by
cell with no sampling. Level-2 blocks carry grids of 1,296 to 10,000
cells; 17,489 of their 227,307 pairs are re-classified on a
deterministic 1-in-13 sample, and the remainder are checked against
log_070's own per-block totals rather than re-derived here. Raising the
sample is a matter of runtime, not of method.

**Not done: no live browser render.** The Chrome extension was not
reachable from this session, so the page was never painted on a real
canvas. The verifier runs the page's own script verbatim against a
canvas-shaped stub, so every number, every filter, every component
count, the autofit rule and both witnesses are checked; what is NOT
checked is that the pixels look right.

---

## decided, recorded for audit

- **The nodes are the identity families of log_070, unchanged.** Every
  attribute is copied byte-identical from `dominant_operators_v1.json`
  and the verifier proves it for all 4,077. No family was re-derived, no
  family was renamed, no name was coined.
- **The connectors are the ruled classifier's four kinds, re-derived
  cell by cell.** The builder asserts, and the verifier independently
  confirms, that every per-block and run total reproduces log_070
  exactly: 47,851 WINDOW-only, 35,094 VALUE-only, 583,400 MIXED, 482
  DECLINE-KIND, 666,827 pairs.
- **The settled decline rule is applied and is visible.** 16,372
  WINDOW-only pairs are connectors, 31,479 are refused for having zero
  comparable value cells. The refused ones can be DRAWN on request as
  evidence, and are never counted in a component and never fed to the
  layout — verified.
- **Neither reading of §1.6 is chosen.** Both counts sit side by side in
  the panel for every block, and both are recomputed independently by
  the verifier (union-find and Bron-Kerbosch).
- **Kinds are distinguishable without colour** — each has its own dash,
  and the on-canvas legend draws the dash beside the name.
- **Five rendering caps, all announced in the page with both numbers.**
  The draw cap takes connectors in kind order so the three rare kinds
  are never the ones dropped. The one data cap — no per-cell split
  embedded for MIXED connectors — is stated in the MIXED tooltip.
- **The "min disagreeing cells" slider is a VIEW filter, not a ruled
  threshold**, says so in the rule line, defaults to 0, and cuts
  EXTERNAL connectors only.
- All four of `CLAUDE.md`'s explorer requirements hold and are verified.
  `position: fixed` is avoided although `CLAUDE.md` does not ask for it.
- The internal connector tethers a member profile to its family node
  rather than a row to an operator node, because this graph has no
  operator nodes. Mechanical adaptation, same near-zero spring.
- The absolute vocabulary bans hold in the page's own text, checked by
  the verifier as a regression test.
- Products written: `family_graph_explorer_v1.html`,
  `family_graph_explorer_v1.src.html`, `family_graph_v1.json`,
  `build_family_graph.py`, `verify_family_graph.js`.
  `dominant_operators_v1.json`, `log070_dominant_operators.py` and
  `matrices_full_v2/` are untouched.

## awaiting the owner

1. **§1.6 — component, maximal clique, or pairwise-only.** The picture
   now shows both: on `whole|whole` L1, 61 groups (largest 72) against
   42,324; and five of the 38 multi-node components visibly span more
   than one census name, the add one through
   `csharp.+ short x short`, whose ends clash at 35 value cells when
   compared directly. Structural, so it is his.
2. **§1.5 — a fourth cell kind, or a ruling that a decline-vocabulary
   difference is not a disagreement.** 482 pairs, drawn as their own
   kind so their extent is on the screen. Structural, so it is his.
