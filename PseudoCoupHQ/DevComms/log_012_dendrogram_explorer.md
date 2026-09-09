# log_012 — dendrogram explorer for the kind-clustering merge tree

Date: 2026-08-12

## What it is

`Research/kind_signature_clustering/dendrogram_explorer.html` — a single
self-contained file (double-click to open; D3 from cdnjs, merge tree
embedded inline). It draws the entire agglomerative merge tree over the
800 pooled kinds (rust, python, dart, c, cpp) as an icicle: x = leaf
order, y = merge height, so **every horizontal line is a threshold
slice of the spectrum**. Companion export: `export_tree.py` writes
`merge_tree.json` from `similarity_matrix.npz` (spectrum.py untouched).

## How to read it

- Drag the dashed pink line: top of the chart = fewest clusters (the
  spectrum end where everything has merged), bottom = 800 singletons.
  The live label shows the cluster count at that height (79 at 0.5,
  matching `spectrum.clusters_at`).
- Leaves are colored by language (legend); joined segments are colored
  by language-mix entropy — gray = single-language merge, saturated
  purple = strongly cross-language. The purple structure is the finding.
- **Wide vertical runs are stable clusters**: a segment's height is its
  stability band [own merge height, super-node's merge height) — the
  threshold range over which that exact member set is a maximal cluster.
  Hover shows members (capped list), merge height, and band width.
- Search box: type a kind name, Enter — matching leaves outline in pink
  and the view zooms to their smallest shared segment. Scroll to zoom
  horizontally, drag background to pan, "reset view" to return.

## Known limitations

- Segments narrower than ~1/3 px at the current zoom are culled for
  speed; zoom in to see them.
- Hover member lists cap at 24 labels (+count).
- Zoom is horizontal only; the vertical axis stays the full [0, 1]
  spectrum so the threshold line always means the same thing.
- Verified headlessly (jsdom): renders, counts match scipy. Not yet
  opened in a real browser — drag/hover interactions untested there.

## Feedback round 1 — 2026-08-12

the owner: "it would be awesome if the dashed threshold line placement
highlighted the clusters that correspond to that threshold level."

Implemented: with the line at height t, every segment that is a current
cluster of the partition at t — maximal below the line, i.e. born at or
below t and absorbed into its super-node strictly above t — gets a
bright yellow (#ffd400) outline at full fill opacity; segments entirely
above the line dim to 30% fill opacity, everything else sits at 85%.
Singleton clusters (leaves below t) are highlighted like any other
segment. Restyling reuses the existing culled draw pass with no
transitions, so dragging the line stays fast. A code assertion
(console.warn) fires if the highlighted-segment count ever diverges
from the reported cluster count. Search-match pink outlines still win
over the cluster highlight.

Verified headlessly (jsdom + d3, as before): highlighted count equals
reported cluster count at t=0.5 (79), t=0.2 (287), t=0.8 (12); no
warnings. Visual appearance in a real browser still unverified.
