# log 048 — operator agreement graph (row-grain best-match), 2026-08-21

Assembly only; **no probe ran**. Vocabulary held: super-node /
sub-node / co-node / sub-tree; the OS-stopped outcome is ABORT.

## what and why

the owner REJECTED the set-identity aggregation of log 047's string
clustering (`l3_dendro_strings.py`): comparing the sorted SET of
distinct output_canon strings per input pair zeroed cross-language
pairs (go.+ ~ python.+ = 0.0000) even though individual rows match
byte-identically — python `int+int` and go `uint64+uint64` produce
the same output_canon for the same input canons (verified: 26 such
byte-identical rows exist for that holder pairing alone).

the owner's design (2026-08-20, settled, his words): each operator-matrix
is a node; its connections to other nodes are the percentage of
agreement; the threshold is the cutoff for connection. Realized at
the ROW grain:

- Nodes: the 242 `lang.op` matrices (v2 canonical forms, `matrices/`).
- Edge weight: align by input pair (lhs_canon, rhs_canon); for each
  pair present in BOTH matrices, score 1 if ANY row of A and ANY row
  of B for that pair have byte-identical output_canon (best-match),
  else 0; weight = matched / shared. Pairs in only one matrix
  excluded. No shared pairs → no edge; zero matches → no edge (never
  a 0-weight edge).
- Per edge also: `n_shared`, `n_matched`, and the VALUE-only rate
  (`value_weight`, `n_shared_value`, `n_matched_value`) with
  REFUSE / RAISE:* / ABORT rows excluded from both sides, so
  decline-agreement and value-agreement stay separable.
- The threshold is a SPECTRUM: the explorer has a slider; edges draw
  when weight >= threshold.

## products

- `Research/kind_fuzz_clustering/l3_agreement_graph.py` — builder.
- `Research/kind_fuzz_clustering/agreement_graph.json` — 242 nodes
  (language/operator attributes), 22,488 edges (weight, n_shared,
  n_matched, value_weight, n_shared_value, n_matched_value). 3.18 MB.
- `Research/kind_fuzz_clustering/graph_explorer.html` — single
  self-contained file, data embedded, NO external scripts (matches
  the precedent `dendrogram_strings.html`, which carries no CDN
  dependency). Force-directed canvas graph; threshold slider with
  live edge count and connected-component count; node color by
  language (legend), operator label, comparison ops ringed; search;
  hover shows node identity or edge numbers (weight, n_shared,
  n_matched, value_weight with its fraction); toggle to weight/cut
  edges by value_weight instead of weight; drag, pan, zoom.

## sanity numbers (printed by the builder, verbatim)

- `go.+ ~ python.+ = 0.3432` (n_shared=169, n_matched=58,
  value_weight=0.5370, n_shared_value=108, n_matched_value=58) —
  far from the rejected rule's 0.0000. The cited row match exists:
  python `int+int` vs go `uint64+uint64` share byte-identical
  output_canon on 26 input pairs (e.g. `[1, 1.3125, 5]` +
  `[1, 1.3125, 5]` → `[1, 1.3125, 6]` in both).
- `go.+ ~ rust.+ = 0.9471` (n_shared=189, n_matched=179,
  value_weight=0.9219, n_shared_value=128, n_matched_value=118) —
  up from 0.9206 under the set rule.
- Components: t=0.95 → 35 (15 multi-node, largest 171); t=0.85 → 11
  (6 multi-node, largest 207); t=0.70 → 4 (2 multi-node, largest
  238).
- Arithmetic vs comparisons: mixed components exist at ALL three
  thresholds (3 / 2 / 1 mixed at 0.95 / 0.85 / 0.70) — under
  best-match the arithmetic group does NOT form a component distinct
  from comparisons, unlike the log-047 clustering. Best-match is
  more permissive: one agreeing holder row (or shared decline
  tokens) is enough to bridge.
- Highest-degree node: `dart.??` (degree 236, language dart).

## headless verify (all pass)

JSON reloads well-formed; 242 nodes / 22,488 edges consistent with
the in-memory build; no 0-weight edges; every edge endpoint is a
node; HTML has the data embedded, the placeholder gone, and no
`<script src` (self-contained).

## decided vs awaiting

Decided, recorded for audit (overturnable): the VALUE-only
denominator counts an input pair only when BOTH sides still hold at
least one value output after removing decline rows; edges with zero
matches are omitted rather than written at weight 0; the explorer's
value_weight toggle swaps both the cutoff and the drawn weight.

Awaiting the owner (minimal): none new. Still open from log 047: the
`c_int64+c_int64` expected-string discrepancy in the approved
python.+ slice.
