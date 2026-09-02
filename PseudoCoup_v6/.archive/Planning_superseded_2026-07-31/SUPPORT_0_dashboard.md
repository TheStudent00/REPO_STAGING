---
id: pcv6.planning.dashboard
status: living
---

# Dashboard — Hub-Construction Capability

One page, capability-framed: how far can we go TODAY toward
converting source scripts from the 12 languages into the Hub
without violating their intentions. Detail lives in the node
PROGRESS files; this is the view from above. Updated whenever any
PROGRESS file changes. Last update: 2026-07-28.

**State as of 2026-07-30, post-purge: 128 tests green** — T1
tree_sitter_base 12, T2 ledger 7, T3 transpiler 8, T4 polyfill 68,
T5 intentions 19, T6 slicer (insertion only) 14. Everything below
reflects that count, not the pre-purge numbers.

## Bottom line

We can parse three languages, reproduce every PCv5 compiler-ingress
artifact byte-identically through the new tool stack, and wrap
fixed-width integer behavior. We cannot yet ingest an ordinary
application script from ANY of the 12 into hub form, cannot yet
slice automatically, and PCv5's chain is still the only place a
hub expression executes end to end. The gap between "tools green"
and "Hub constructible" is: application-source ingress, real type
population, T5/T6, and emission.

## The capability ladder

| # | capability | status | today, concretely |
|---|---|---|---|
| 1 | Parse a source language (turn its script text into the node tree every other tool reads) | **partial** | 3 grammars pinned + acceptance-tested (python, rust, cpp); the other 9 of the 12 not yet registered (pattern exists) |
| 2 | Identify every node + record it (ledger) | **partial** | ids, spans, anchors: done and proven on real compiler files; `semantic.type` exists only as honest `unresolvable` markers — no ingestor populates real types yet |
| 3 | Know the intentions (steering data) | **strong** | PCv5 data copied forward + four steering fields as data (satisfiers, canon, set, policy links); four slicing request forms express the proven chain, machine-validated (27/27) |
| 4 | Transpile COMPILER source into the hub | **partial** | the LLVM x86-64 C++ encoder ingests and reproduces its reference byte-identically. Two Rust-side ingestors existed but were aimed at a retired backend and were removed (2026-07-30); Rust ingestion must be rebuilt against rustc-LLVM |
| 5 | Transpile APPLICATION source into the hub | **not started in PCv6** | the actual "convert the 12 languages' scripts" capability; lineage holds Kotlin ingress (v4/WFL), uncomposed here |
| 6 | Fill behavior gaps (polyfill) | **partial** | fixed-width ints done under the uniform law, MIN/-1 trap implemented per ruling (stack 104 green); strings/collections/etc. unstarted |
| 7 | Slice compiler semantics by intention | **design settled, build removed** | selection and extraction were built and green, then removed (2026-07-30) because every form they consumed pointed at a retired backend. The settled design stands (forms as data, persisted plans, follow-the-calls, over-approximate-plus-asserted-stubs); the machinery is rebuilt when the first LLVM-facing form exists |
| 8 | Insert + execute in the hub | **half built** | mount/border/cache with platform assertions (a wrong arch/cc/os REFUSES before mmap) and page accounting; `-7 idiv 2 → -3` executed from mounted bytes written from the Intel SDM. Not yet fed by an extracted encoder — that waits on row 7 |
| 9 | Verify behavior (not just bytes) | **per-tool only** | every tool has its oracle; a v0-style behavioral oracle (run the source language's own tests in the hub) not composed |
| 10 | Emit hub → the 12 languages | **deferred** | by design, until ingress stands |

## Reading the ladder

Rows 1–4 are where the work has been: the machinery that eats
COMPILER code, because that is how the hub acquires each
language's exact semantics (transpile the compiler, slice it,
insert it). Row 5 is the other half of the project — eating
ordinary programs — and it is untouched in PCv6 so far; it reuses
rows 1–2 directly, needs row 3's data, and is where the lineage's
application-ingress harvest (v4/WFL) comes in. Rows 7–8 turn row
4's output into running hub semantics. Row 10 closes the loop.
