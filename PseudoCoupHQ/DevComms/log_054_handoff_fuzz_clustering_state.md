# log 054 — HANDOFF: fuzz-clustering state, for an earlier branch to resume

2026-08-21. Written at the owner's request so that an earlier conversation
branch (`PCHQ (0-1-1-0-1-0-1-0) (best PCv5 research)` or
`PCHQ (0-1-1-0-1-0) (active)`) can pick the work up without this
window's context. Everything load-bearing is in files; this log says
which files and what is settled, open, and next.

## read these first, in this order

1. `PRIVATE/PseudoCoupHQ/CLAUDE.md` — settled vocabulary,
   canonical form, probe design, scoring rules, explorer requirements,
   how the owner works. Written 2026-08-21 precisely because rulings kept
   getting re-litigated.
2. `PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`
   — the settled ontology: language → operator → profile → cell; key =
   a cell's address; contract vs group; what merging is NOT. the owner's
   verbatim ruling on contraction is quoted there.
3. `.../node_0_3_2_kind_fuzz_clustering/SUPPORT_conversion_spec.md` —
   the full settled spec, accumulated ruling by ruling (canonical form,
   Cartesian probe design, alignment, contract/group, rejected
   designs).
4. This log's "open items" section.

## what exists (data and tools, all under Research/kind_fuzz_clustering/)

- `matrices_cart/` — THE current data. 85 CSVs, one per
  (operator, level): rust + ruby, forms whole/fractional/truth,
  level 1 = all pairs from X (`y = op(x0,x1)`), level 2 = all
  four-tuples from X' (`z = op(op(x0,x1), op(x2,x3))`).
  10,042,779 probes, all measured (log 052). `index.json` carries the
  X sets and the probe-index rule (operands stored once per set).
- `row_graph_v4.json` + `row_graph_explorer_v4.html` — current graph:
  input-key-intersection alignment, contract (identity merge), group
  (partial-overlap clique, drawn as hulls), both scorings on every
  connector (exact-match + graded per-element), transitivity hazard
  measured at 7,212 triples (log 053).
- Earlier generations kept for audit: matrices/ (edge values),
  matrices_interval/ + matrices_interval_c/ (geometric ladder +
  shift/comp1 — designs REJECTED, see CLAUDE.md), row_graph v1–v3,
  dendrogram/graph explorers v1–v3.
- Lane machinery: `l3_cart_values.py` (X sets), `l3_cart_gen.py`
  (lanes), `l3_cart_read.py` (fold), `l3_row_sim.py` (scoring),
  `l3_row_graph_v4.py` (graph), `verify_row_graph_v4.js` (headless).
- Sandbox: lanes drop into `SandboxDesign/agent/drop`;
  progress across all runs:
  `bash SandboxDesign/progress.sh` (`-w` to watch).
  Ruby stall budget is 2 s; ALL ruby stalls so far are `**` with a
  BigDecimal operand.

## the state of the argument (why the next refinement)

The clustering still does not cluster the way the owner expects: operators
with nothing to do with each other connect. Diagnosed causes, in
order of discovery:

1. byte-identity scoring punished numeric closeness → per-element
   graded similarity added (log 051);
2. the diagonal (`v OP v`) cannot distinguish operators that agree on
   equal operands → Cartesian all-pairs design (log 052);
3. identical-vector alignment threw away 172,187 real comparisons →
   input-key intersection (log 053);
4. decline-agreement inflated similarity → declines excluded from
   scoring (log 051, kept since);
5. STILL OPEN: partial-overlap coincidences (a whole profile and a
   truth profile share only the keys drawn from {0,1} — 4 cells — and
   `ruby.*` grouped with `ruby.&` on exactly that; they are identical
   on {0,1} and unrelated everywhere else).

## the owner's rulings at the point of handoff (2026-08-21, end of session)

- **Full grids by construction.** Probe every holder against the FULL
  X set of its form; a value the holder cannot represent fills its
  cell with a distinct outcome `UNREPRESENTABLE` (no probe needed —
  known statically; zero machine cost). Then every profile of a form
  and level has the SAME key set, always.
- **Profile compatibility is a hard gate.** Two profiles attract only
  if they were intended to process the same inputs: same form pair,
  same level, same intended X set. Representability gaps do not break
  compatibility (the intention was the same domain; the gap is data).
  A truth profile and a whole profile are NEVER compatible, whatever
  cells they coincidentally share. Cell agreement counts only inside a
  compatible profile pair — "the key-to-key/cell-to-cell attraction is
  never without the context of the profile-to-profile attraction. if
  the profiles arent compatible, there is no attraction" (the owner,
  verbatim).
- **No key-to-key clustering, ever.**
- With full grids, GROUP (the partial-overlap case) retires; CONTRACT
  keeps its meaning (every cell identical over an identical key set).
- **The research question is DOMINANCE, which is directed.** the owner: a
  dominant operator may exist such that all operators are a subset of
  it, or one could be constructed to contain all operator behaviors.
  Symmetric similarity flattens that. The next object is the directed
  containment relation over compatible profiles — A dominates B when
  everywhere B answers, A answers identically (A may answer more) —
  read as nests / overlaps / contradicts (the line's original ruling),
  rendered as a lattice, not only a similarity graph.
- Scoring on full grids should carry TWO numbers: agreement over value
  cells, and agreement over ALL cells with
  UNREPRESENTABLE/REFUSE/RAISE:*/ABORT treated as answers — the second
  is where representability and overflow differences live. (Related
  standing note: excluding declines made `rust.+ i32` vs `ruby.+
  Integer` score 1.000 while differing at all 14 overflow keys — the
  fracture is exactly what vanished.)

## open items, in priority order

1. Rebuild matrices_cart with full grids + UNREPRESENTABLE; rebuild
   the graph with the compatibility gate; retire group.
2. Build the containment/dominance reading (directed; lattice view).
   Note `dominance_lattice.json` exists from the layer-3 era as
   precedent.
3. the owner's input-overlap criterion (input-overlap % >= output-agreement
   %) — ruled, superseded in part by full grids, but check whether any
   residual case still needs it.
4. Which scoring is THE weight, and at what cut — the owner has not ruled;
   both ride on every connector.
5. The other ten languages — waiting until the pilot clusters the way
   the owner expects. Do not run them before that.
6. Noted to revisit: output-shape variation inside a profile as its
   own clustering signal; declines-as-disagreement vs exclusion;
   `ruby **` stalls (all BigDecimal) — drop from menu vs pay the
   budget.

## working with the owner — read CLAUDE.md's last section, then these

- Show objects, never describe them: markdown tables in chat (raw
  text blocks wrap and are unreadable); full vectors when asked, not
  summaries or samples.
- One meaning per term; the ontology file governs. Do not introduce a
  term without a glossary entry.
- Vocabulary bans are absolute: no parent/child/sibling family words;
  no death/kill words (the OS-stopped outcome is ABORT).
- Two-list rule in every agent report: "decided, recorded for audit"
  strictly separate from "awaiting the owner" (minimal).
- Ask before structural decisions; decide mechanical ones. When the owner
  sketches a form (e.g. `[sign, mant, expo]` with integer mants), he
  is conveying the SPIRIT — clarify the letter once, then follow the
  settled spelling (mant ∈ [1,2), decimal, 31 digits).
- Substantial output goes in a DevComms log; chat carries the
  conclusion and points at it.
