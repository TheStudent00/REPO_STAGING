# Task hub2 — Hub v2: the dictionary at two levels (cells and operator bodies), comparisons as the pair entry, and the lookup key with its holders

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it. Then
`task_hub1_brief.md` beside this file and its log `DevComms/log_252` (its
§5 decisions and §6 "Awaiting the owner" are this task's inputs), the
hub_compiler node's CORE and sub-nodes, `Research/oracle/hub/` as hub1
left it, the bank task's certificates (`task_bank1_brief.md`; its log;
`.../emulation/autopoly/certificates.jsonl` — the dictionary is READ FROM
THE BANK from now on), and the pool-entry emulation work: `log_218` (o7,
c), `log_226` (o11, rust), `log_230`/`o13` (mode rendering), the pool
(`Research/op_pipeline/the_pool5.json`; pool6 candidate `pool104_candidate.json`).
Instance `hub2.conf` (copy from `PUBLIC/Airlock/instances/hub2.conf`;
mounts `sandbox-persist` read-only). Artifact folder: `Research/oracle/hub/`,
new files `dictionary2.*`, `hub2.py`, `oracle_test2.*`; lanes under
`lanes_hub2/`. Task bank1 must have CLOSED before this task starts.

## 1. The three holes hub1 measured, and the three answers (coordinator, 2026-09-10)
| hole | answer |
|---|---|
| a comparison feeding a select cannot compose: 61 cells write only flags | the front end resolves the (comparison, consumer) node pair as ONE entry: the loop's flag-pair cells (`test`/`cmp` + `cmov*`/`set*`), whose emulations are proved (the pair rendered as one function: the comparison then the select). No flag state crosses a node; the pair IS the node |
| go lowers a guarded construct to a SEQUENCE (`<<` uint64: six cells; `/` int32: eight) | the dictionary gains a second level: OPERATOR-BODY entries — the pool entry go's unit belongs to, with the emulation o7 (c) / o11 (rust) proved for that entry (`Research/oracle/cross_construction/emulation/emulation_results.json` and the rust results), and o13's mode rendering where the entry carries guard rows. A node resolves first to a cell (v1), else to its unit's pool entry; the composition calls the entry's proved emulation. Both levels keyed machine form: cell key, or pool entry id |
| the primitive route's lookup carries no holder widths (five proved entries with truth-holder parameters) | the dictionary records, per entry, the parameter holders the proof was made over; the composition refuses a mismatch BY CAUSE as hub1 did; and one line to the coordinator naming the loop fix (the lookup should carry the matched body's holders) — NOT made here |

## 2. Deliverable
`dictionary2.json/.md`: per target, cell-level entries (from the bank's
`proved`/`proved_under_caller_extension` certificates, with their holders)
and body-level entries (pool entries with a proved o7/o11 emulation, with
the mode where rendered), holes by cause at both levels. `hub2.py`: the
front end resolving a node to a cell, else a pair, else a pool entry.
Then the SAME handful (`hub/handful/handful.go`) and the SAME measure
over the corpus's go units, so every number sits beside hub1's:
`oracle_test2.md` with hub1 → hub2 per function and per target, and the
measure's counts (composed / proved / disproved / undecided, ledger rows)
hub1 → hub2. Expect `f5`, `f6`, `f8` to move; say what does and does not,
by cause. Guard over every json; log (next free number, check right
before writing); verifier lane; PROGRESS on the hub_compiler node and its
sub-nodes; sync-back; instance down. Memory bound 6g, sample first, peak
RSS, abort `ABORT_MEMORY_HUB2`. No shared-file change is authorised; the
renderers, the loop's driver and the bank are READ. Never delete anything
under `<runs>/` or `PUBLIC/Airlock/`. Waits in short calls.
Reply with the handful table hub1 → hub2, the measure hub1 → hub2, the
dictionary's counts at both levels per target, the tally, the two lists.
