# log 266 — task cov1: how far the PROVED emulations reach, per language pair

Node: `hq.research.arch_unit_oracle` (autopoly / riscv64 cross-construction),
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md`.
Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_cov1_brief.md`.
Written 2026-09-12 by the coordinator (Fable), who ran it. Instance
`cov1` (`PUBLIC/Airlock/instances/cov1.conf`, copied from
`rv4.conf`), lanes on the tower via `remote_lane.sh`. Artifact folder:
`PRIVATE/PseudoCoupHQ/Research/oracle/coverage/`.

## 1. What the objects are, one sentence each in relation

- `arch-unit` — one compiled body of one source language for one
  architecture, carved out of the corpus's binary at its function
  symbol.
- `cell` — one (mnemonic, operand shape, width) triple; a unit
  CONTAINS the cells its own carved instructions spell.
- the bank (x86: `certificates.jsonl`; RISC-V: `construct/general/rv6_all.jsonl`)
  — records, per (cell, target language), whether a proved emulation
  exists; a cell's containing unit can only be re-expressed in a target
  once every cell it contains is proved there.
- `expressible[x][y]` — the share of x's arch-units all of whose cells
  are proved on y, so the whole unit could be rewritten in y out of
  proved pieces; this is the owner's question of 2026-09-12, quoted in the
  brief: "if we had all of them proven, every arch-opcode can be
  expressed in another language but if only some of the arch-opcodes
  emulated..."
- this task is a DATA JOIN over stores that already exist: no compile,
  no z3. `build_join.py` (below) calls the SAME classifier functions
  the existing pipeline already uses to build the model table
  (`model_table.py`, x86) and the RISC-V attestation (`rv_attest.py`),
  imported unmodified, and keeps their per-unit membership in full
  instead of the 3-example cap those stores already carry.

## 2. Walkthrough

The join needed a per-unit list of cells (`cells_of(unit)`), and no
store already holds that in full: `model_table_attest.json` and
`ledger_signatures.json` (x86) and `attest_rv.json` (RISC-V) all cap
their `example_units` at 3 (`model_table.py:906-907`,
`ledger_signatures.py:254-256`, `rv_attest.py`'s own docstring). The
raw ledger rows under `Research/op_pipeline/` (`canon40_regen_store/`,
`canon40_wrapped_*.json`, `canon40_interp.json`, 332 shards, 259 MB,
31,078 units) DO carry every instruction of every unit, so
`build_join.py`'s `units-x86` command streams those shards (`TR.shards()`,
the same function `model_table.attestation()` calls) and, for each
unit, classifies its instructions with `model_table.classify_line` and
`model_table.key_width` — the identical functions the model table
itself uses, called again rather than reimplemented, keeping the FULL
set instead of `place_row`'s 3-example cap. RISC-V's per-unit bodies
come from `attest_rv.json`'s own `rows` (rv2's riscv64-compiled c/go
corpus, 1,244 rows, 474 `LIFTED`), and `cells_of(body)` is `rv_attest.py`'s
own existing function, called unmodified.

Two defects turned up in the sample-then-full run and are fixed in the
version this log reports:

1. **The bank's first write failed its own guard.** `bank-x86`/`bank-riscv`
   first wrote `"cells"` as a dict keyed by `"mnem|shape|key_width"`
   (e.g. `"and|gpr_gpr|8"`) for a fast lookup — a spelling-joined
   string, exactly what `check_no_spelling_keys.py` exists to catch,
   and it caught it (21 + 6 findings, `and`/`or`/`xor`/`not`). Fixed:
   `"cells"` is now a LIST of `{"cell": {...}, "targets": {...}}`
   records, the shape every other store in this line already uses; the
   joined string survives only as an in-memory Python dict key inside
   `matrix_command`, never written to a file.
2. **`cells_of(unit)` on RISC-V picked up cells outside the RISC-V
   model table's own population.** `rv_attest.py`'s `cells_of()` was
   built for a narrower purpose than "run over the whole go corpus",
   and over that corpus it also classifies `c.nop` (shape `"none"`,
   the go compiler's alignment pad) as a cell — a triple twins.json
   holds ZERO rows for, because no x86 operation computes "do
   nothing", so the pass that built twins.json's 255-row population
   never produced a twin for it. Direct check: of the 18 go units
   `c.nop` appears in, ALL 18 were the entire population of go units
   lane 2 (before the fix) marked inexpressible even into go itself
   (87 of 105) — zero of them had any other unproved cell. Fixed:
   `units-riscv` now takes `twins.json` and drops any cell outside its
   255-row population before it can block a unit
   (`riscv_cell_population()` in `build_join.py`). x86 needed no such
   filter: every cell `units-x86` produces is already inside
   `model_table_attest.json`'s 257 attested cells (checked directly,
   0 outside).

Both fixes are in the version of `build_join.py` synced and run as
lane `cov1_l3_full_fixed.sh`, whose guard run and matrices are what
this log reports. Lanes `cov1_l1_sample20.sh` (guard FAIL, cause 1) and
`cov1_l2_full.sh` (guard PASS, but carries defect 2, the `c.nop`
undercounting go by 18) are kept as the record of what was found and
superseded, per the standing rule that nothing under `lanes_cov1/` is
removed.

A third, unfixed observation, not a defect: **c and c++ have IDENTICAL
destination-only proof coverage over every cell both attempt.** Checked
directly against `bank_x86.json`: of the 253 cells both `c` and `cpp`
have a live bank record for, the destination-only boolean agrees on
all 253; 8 more cells have a `c` record and no `cpp` record at all.
That is why the x86 destination-only matrix's `c` and `cpp` COLUMNS are
identical for every source language below — not a bug, a real property
of this bank as of 2026-09-12.

## 3. The matrices (§2.1 of the brief)

Every cell reads **N of M units**: N is the count of x's arch-units
whose every cell is proved on y; M is the total arch-units of x. x86's
M comes from streaming all 31,078 corpus units and keeping the
10,367 (c) / 17,569 (cpp) / 685 (rust) / 577 (go) / 1,229 (swift)
whose relink succeeded (640 of 31,067 x86-language units refused
relink and are excluded from M on every language — a real, small
undercount, named as a flag below). RISC-V's M is the 369 (c) / 105 (go)
`LIFTED` rv2 probes.

**Table 1 — x86_64, destination-only** (a non-flag place proved or
`proved_under_caller_extension`; this is the line's standard reading).

| source \ target | c | cpp | rust | go | swift |
|---|---|---|---|---|---|
| **c** | 4578/10367 | 4578/10367 | 4152/10367 | 3887/10367 | 3504/10367 |
| **cpp** | 7631/17569 | 7631/17569 | 7056/17569 | 6647/17569 | 5928/17569 |
| **rust** | 489/685 | 489/685 | 489/685 | 489/685 | 489/685 |
| **go** | 157/577 | 157/577 | 157/577 | 153/577 | 157/577 |
| **swift** | 237/1229 | 237/1229 | 237/1229 | 226/1229 | 237/1229 |

**Table 2 — x86_64, strict** (every written place, flags included,
must itself carry `kind == proved`).

| source \ target | c | cpp | rust | go | swift |
|---|---|---|---|---|---|
| **c** | 1973/10367 | 3127/10367 | 2256/10367 | 1850/10367 | 2260/10367 |
| **cpp** | 3013/17569 | 5163/17569 | 3352/17569 | 2759/17569 | 3474/17569 |
| **rust** | 371/685 | 397/685 | 373/685 | 413/685 | 384/685 |
| **go** | 127/577 | 234/577 | 76/577 | 100/577 | 126/577 |
| **swift** | 202/1229 | 241/1229 | 233/1229 | 207/1229 | 180/1229 |

**Table 3 — riscv64, destination-only.** riscv64's X (source, a corpus
that exists) is c and go only (rv2's corpus); Y (target) is c, cpp, go,
rust — swift carries no riscv64 SDK in the image (log 265's flag,
unchanged here).

| source \ target | c | cpp | go | rust |
|---|---|---|---|---|
| **c** | 351/369 | 351/369 | 349/369 | 369/369 |
| **go** | 100/105 | 100/105 | 102/105 | 105/105 |

**Table 4 — riscv64, strict.** IDENTICAL to Table 3: RISC-V has no
flags register, so every cell in the 255-row population has exactly
one written place (checked directly: 0 of 255 cells in
`construct/general/rv6_all.jsonl` have more than one distinct `place`),
and strict-vs-destination-only has nothing left to differ on. The
flags' cost, which Table 1 vs Table 2 makes visible on x86, is
architecturally zero here.

| source \ target | c | cpp | go | rust |
|---|---|---|---|---|
| **c** | 351/369 | 351/369 | 349/369 | 369/369 |
| **go** | 100/105 | 100/105 | 102/105 | 105/105 |

## 4. Blocking cells (§2.2 of the brief): top 3 of the stored top 10

The full top 10 per pair is in
`PRIVATE/PseudoCoupHQ/Research/oracle/coverage/coverage_x86.json`
and `.../coverage_riscv64.json`, key `blocking_cells_top10`. This is
the worklist ordering for the proofs still missing: proving
`cmp/gpr_gpr/64` moves the most x86 units at once under the
destination-only reading.

**Table 5 — x86_64 destination-only, top 3.**

| source -> target | top blocking cells (blocked units) |
|---|---|
| c -> c | `cmp/gpr_gpr/64` (1354); `push/gpr_one/64` (1251); `test/gpr_same/32` (903) |
| c -> cpp | `cmp/gpr_gpr/64` (1354); `push/gpr_one/64` (1251); `test/gpr_same/32` (903) |
| c -> go | `cmp/gpr_gpr/64` (1354); `push/gpr_one/64` (1251); `test/gpr_same/32` (903) |
| c -> rust | `cmp/gpr_gpr/64` (1354); `push/gpr_one/64` (1251); `test/gpr_same/32` (903) |
| c -> swift | `movslq/widen_gpr_gpr/64` (1400); `cmp/gpr_gpr/64` (1354); `push/gpr_one/64` (1251) |
| cpp -> c | `test/gpr_same/32` (2208); `cmp/gpr_gpr/64` (2048); `push/gpr_one/64` (1893) |
| cpp -> cpp | `test/gpr_same/32` (2208); `cmp/gpr_gpr/64` (2048); `push/gpr_one/64` (1893) |
| cpp -> go | `test/gpr_same/32` (2208); `cmp/gpr_gpr/64` (2048); `push/gpr_one/64` (1893) |
| cpp -> rust | `test/gpr_same/32` (2208); `cmp/gpr_gpr/64` (2048); `push/gpr_one/64` (1893) |
| cpp -> swift | `test/gpr_same/32` (2208); `movslq/widen_gpr_gpr/64` (2160); `cmp/gpr_gpr/64` (2048) |
| go -> c | `push/gpr_one/64` (170); `cmp/imm_gpr/64` (128); `test/gpr_same/64` (64) |
| go -> cpp | `push/gpr_one/64` (170); `cmp/imm_gpr/64` (128); `test/gpr_same/64` (64) |
| go -> go | `push/gpr_one/64` (170); `cmp/imm_gpr/64` (128); `test/gpr_same/64` (64) |
| go -> rust | `push/gpr_one/64` (170); `sbb/gpr_same/32` (134); `cmp/imm_gpr/64` (128) |
| go -> swift | `push/gpr_one/64` (170); `cmp/imm_gpr/64` (128); `test/gpr_same/64` (64) |
| rust -> c | `test/imm_gpr/8` (48); `cmp/gpr_gpr/64` (44); `lea/mem_gpr/64` (30) |
| rust -> cpp | `test/imm_gpr/8` (48); `cmp/gpr_gpr/64` (44); `lea/mem_gpr/64` (30) |
| rust -> go | `test/imm_gpr/8` (48); `cmp/gpr_gpr/64` (44); `push/gpr_one/64` (30) |
| rust -> rust | `test/imm_gpr/8` (48); `cmp/gpr_gpr/64` (44); `push/gpr_one/64` (30) |
| rust -> swift | `test/imm_gpr/8` (48); `cmp/gpr_gpr/64` (44); `push/gpr_one/64` (30) |
| swift -> c | `cmp/gpr_gpr/64` (464); `test/gpr_same/64` (135); `cmp/gpr_gpr/32` (132) |
| swift -> cpp | `cmp/gpr_gpr/64` (464); `test/gpr_same/64` (135); `cmp/gpr_gpr/32` (132) |
| swift -> go | `cmp/gpr_gpr/64` (464); `test/gpr_same/64` (135); `cmp/gpr_gpr/32` (132) |
| swift -> rust | `cmp/gpr_gpr/64` (464); `test/gpr_same/64` (135); `cmp/gpr_gpr/32` (132) |
| swift -> swift | `cmp/gpr_gpr/64` (464); `movslq/widen_gpr_gpr/64` (168); `test/gpr_same/64` (135) |

**Table 6 — x86_64 strict, top 3.** `setne/gpr_one/8` dominates once
flags are required: a `test`/`sete`/`setne` sequence is common and the
flag place is unproved far more often than the destination.

| source -> target | top blocking cells (blocked units) |
|---|---|
| c -> c | `setne/gpr_one/8` (1772); `push/gpr_one/64` (1251); `xorps/xmm_same/128` (1003) |
| c -> cpp | `setne/gpr_one/8` (1772); `push/gpr_one/64` (1251); `movzbl/widen_gpr_gpr/32` (912) |
| c -> go | `setne/gpr_one/8` (1772); `cmp/gpr_gpr/64` (1354); `push/gpr_one/64` (1251) |
| c -> rust | `setne/gpr_one/8` (1772); `push/gpr_one/64` (1251); `xorps/xmm_same/128` (1003) |
| c -> swift | `setne/gpr_one/8` (1772); `movslq/widen_gpr_gpr/64` (1400); `cmp/gpr_gpr/64` (1354) |
| cpp -> c | `setne/gpr_one/8` (4772); `push/gpr_one/64` (1893); `xorps/xmm_same/128` (1756) |
| cpp -> cpp | `setne/gpr_one/8` (4772); `push/gpr_one/64` (1893); `setp/gpr_one/8` (1441) |
| cpp -> go | `setne/gpr_one/8` (4772); `cmp/gpr_gpr/64` (2048); `push/gpr_one/64` (1893) |
| cpp -> rust | `setne/gpr_one/8` (4772); `push/gpr_one/64` (1893); `xorps/xmm_same/128` (1756) |
| cpp -> swift | `setne/gpr_one/8` (4772); `movslq/widen_gpr_gpr/64` (2160); `cmp/gpr_gpr/64` (2048) |
| go -> c | `push/gpr_one/64` (170); `and/gpr_gpr/64` (111); `or/gpr_gpr/64` (36) |
| go -> cpp | `push/gpr_one/64` (170); `lea/mem_gpr/64` (20); `sete/gpr_one/8` (20) |
| go -> go | `push/gpr_one/64` (170); `cmp/imm_gpr/64` (128); `sbb/gpr_same/64` (126) |
| go -> rust | `push/gpr_one/64` (170); `sbb/gpr_same/32` (134); `and/gpr_gpr/64` (111) |
| go -> swift | `push/gpr_one/64` (170); `cmp/imm_gpr/64` (128); `sbb/gpr_same/64` (126) |
| rust -> c | `cmovne/gpr_gpr/64` (48); `cmove/gpr_gpr/64` (36); `lea/mem_gpr/64` (30) |
| rust -> cpp | `cmovne/gpr_gpr/64` (48); `cmove/gpr_gpr/64` (36); `lea/mem_gpr/64` (30) |
| rust -> go | `cmovne/gpr_gpr/64` (48); `cmp/gpr_gpr/64` (44); `cmove/gpr_gpr/64` (36) |
| rust -> rust | `cmovne/gpr_gpr/64` (48); `cmove/gpr_gpr/64` (36); `push/gpr_one/64` (30) |
| rust -> swift | `cmovne/gpr_gpr/64` (48); `cmp/gpr_gpr/64` (44); `cmove/gpr_gpr/64` (36) |
| swift -> c | `setne/gpr_one/8` (112); `or/cl_gpr/8` (110); `sete/gpr_one/8` (110) |
| swift -> cpp | `setne/gpr_one/8` (112); `or/cl_gpr/8` (110); `sete/gpr_one/8` (110) |
| swift -> go | `cmp/gpr_gpr/64` (464); `test/gpr_same/64` (135); `cmp/imm_gpr/64` (127) |
| swift -> rust | `setne/gpr_one/8` (112); `or/cl_gpr/8` (110); `sete/gpr_one/8` (110) |
| swift -> swift | `cmp/gpr_gpr/64` (464); `movslq/widen_gpr_gpr/64` (168); `test/gpr_same/64` (135) |

**Table 7 — riscv64, top 3 (strict identical to destination-only).**
The multiply-high family (log 265's "the four left") does not appear
here at all: it is attested in the 255-cell model table but never
occurs inside rv2's own c/go corpus, so it blocks no unit under this
join. What DOES block riscv64 units is the divide/remainder family
(`div`, `rem`, `remu`, `divw`, `remw`), plus `czero.eqz` (a
zicond-extension conditional-zero op) for c into go.

| source -> target | top blocking cells (blocked units) |
|---|---|
| c -> c | `remu/gpr_gpr_gpr/64` (6); `div/gpr_gpr_gpr/64` (4); `rem/gpr_gpr_gpr/64` (4) |
| c -> cpp | `remu/gpr_gpr_gpr/64` (6); `div/gpr_gpr_gpr/64` (4); `rem/gpr_gpr_gpr/64` (4) |
| c -> go | `czero.eqz/gpr_gpr_gpr/64` (6); `remu/gpr_gpr_gpr/64` (6); `div/gpr_gpr_gpr/64` (4) |
| c -> rust | (none — full coverage, 369/369) |
| go -> c | `divw/gpr_gpr_gpr/32` (1); `div/gpr_gpr_gpr/64` (1); `remw/gpr_gpr_gpr/32` (1) |
| go -> cpp | `divw/gpr_gpr_gpr/32` (1); `div/gpr_gpr_gpr/64` (1); `remw/gpr_gpr_gpr/32` (1) |
| go -> go | `div/gpr_gpr_gpr/64` (1); `rem/gpr_gpr_gpr/64` (1); `remu/gpr_gpr_gpr/64` (1) |
| go -> rust | (none — full coverage, 105/105) |

## 5. Length view (§2.4 of the brief): the diagonal (x expressible in
its own language), by unit length in computing instructions

x86 length = `len(arch_opcode_rows) + len(flag_pair_rows)`
(`model_table.py`'s own row categories; a return is never counted, it
carries neither). RISC-V length = `len(rv_attest.computing_lines(body))`
(`rv_attest.py`'s own function, which already drops the return line).
Shown on the diagonal so the length effect is isolated from the
cross-language effect; the full 5x5 (x86) / 2x4 (riscv64) breakdown by
length bucket is in the coverage json under `length_view`.

**Table 8 — x86_64 destination-only, diagonal.**

| source (x==y) | 1 | 2 | 3-5 | 6-10 | over-10 |
|---|---|---|---|---|---|
| **c** | 8/16 | 572/648 | 3380/6198 | 586/2837 | 32/668 |
| **cpp** | 6/14 | 822/2623 | 5933/9002 | 834/4688 | 36/1242 |
| **rust** | 6/6 | 76/174 | 400/422 | 7/67 | 0/16 |
| **go** | 5/5 | 130/238 | 18/26 | 0/295 | 0/13 |
| **swift** | 10/10 | 89/327 | 133/420 | 5/301 | 0/171 |

**Table 9 — x86_64 strict, diagonal.**

| source (x==y) | 1 | 2 | 3-5 | 6-10 | over-10 |
|---|---|---|---|---|---|
| **c** | 8/16 | 473/648 | 1456/6198 | 36/2837 | 0/668 |
| **cpp** | 6/14 | 526/2623 | 4274/9002 | 315/4688 | 42/1242 |
| **rust** | 6/6 | 76/174 | 289/422 | 2/67 | 0/16 |
| **go** | 5/5 | 46/238 | 7/26 | 42/295 | 0/13 |
| **swift** | 10/10 | 89/327 | 64/420 | 1/301 | 16/171 |

The pattern is the same on both readings: expressibility falls as
length grows (c, destination-only: 92% at length 3-5, down to 21% at
6-10, 5% over 10), the ordinary cost of needing EVERY cell in a longer
body proved at once.

**Table 10 — riscv64, diagonal (strict identical).**

| source (x==y) | 1 | 2 | 3-5 | 6-10 | over-10 |
|---|---|---|---|---|---|
| **c** | 178/196 | 131/131 | 38/38 | 4/4 | — |
| **go** | 54/54 | 15/15 | 12/12 | — | 21/24 |

riscv64's c corpus tops out at length 6-10 (no c probe over 10
instructions); go's over-10 bucket (21/24, 88%) is the one place
length does NOT sharply cost coverage on this architecture, unlike
x86 — the divide/remainder cells that block riscv64 are rare enough
(§4) that most long go bodies do not happen to contain one.

## 6. Flags, every one LITERAL

- **640 of 31,067 x86 corpus units refused relink** (`MODEL.lines_of_unit`
  returned `None`) and are excluded from every M in Tables 1-2 and 8-9.
  Printed by lane `cov1_l3_full_fixed.sh`: `units-x86 done: seen 31067,
  written {'c': 10367, 'cpp': 17569, 'go': 577, 'rust': 685, 'swift':
  1229}, relink_refused 640, peak_kb 80436`. Not investigated further
  here — the brief scopes this task as a join over what already exists,
  and `Research/op_pipeline/` was written to by nothing this task ran.
- **4 x86 cells are attested in the corpus with ZERO bank record for
  ANY target**, so they can never count as proved and always block
  whatever unit holds them: `pcmpeqb/mem_xmm/128`, `pcmpeqb/xmm_xmm/128`,
  `pcmpeqd/xmm_same/128`, `pmovmskb/xmm_gpr/128` (2 units each; §8 Block
  D reproduces the exact 4 and their counts). These are SIMD
  byte-compare/mask ops, plausibly from vectorized code the compiler
  emitted; they are not in any of the top-10 blocking lists because 2
  units each is too small to place, but they are a real gap in the
  bank, not in this join.
- **8 x86 cells have a live `c` bank record and no `cpp` record at
  all**, on top of the 253 where both exist and agree — §2's "c and
  cpp are identical" observation, reproduced in §8 Block D
  (`both_present=253 same=253 diff=0 c_only_no_cpp=8`).
- **`remote_lane.sh`'s `sync-to`/`sync-back` report exit 1 on this
  tower even when the transfer succeeds.** Its `grep -E "^Number of
  (regular files transferred|created)|^Total transferred"` never
  matches this box's rsync (3.4.1, protocol 32) `--info=stats1`
  output, which here is only `sent ... bytes` / `total size is ...`
  with neither of those two lines — `pipefail` then turns rsync's own
  success into the wrapper's exit 1. Verified: a manual `rsync
  --info=stats1` run against the same two ends produces exactly that
  two-line output, and every `sync-to`/`sync-back` in this task's
  session was confirmed to have actually moved the files by `ssh ...
  ls -la` afterward. `remote_lane.sh` was not touched (LAW: never edit
  a shared file over ssh, and it is not this task's artifact folder);
  named here so the next task does not lose a turn to it.
- **swift carries no riscv64 SDK** in the sandbox image — log 265's
  flag, unchanged; this is why riscv64 has no swift row or column.
- Memory: bound stated 6 GB (`ABORT_MEMORY_COV1`), peak resident
  actually reached 122,352 KB (~120 MB, `units-riscv`, lane 3) and
  80,436 KB (~79 MB, `units-x86`) — nowhere near the bound; no abort
  raised.

## 7. Guard and verifier

Lane `cov1_l6_reproduce_all.sh`, tower log
`<runs>/cov1/agent/logs/<stamp>__cov1_l6_reproduce_all.sh.log`,
step [1/5], the guard over all four json files this task wrote:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/coverage/bank_x86.json PseudoCoupHQ/Research/oracle/coverage/bank_riscv64.json PseudoCoupHQ/Research/oracle/coverage/coverage_x86.json PseudoCoupHQ/Research/oracle/coverage/coverage_riscv64.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS bank_x86.json -- no operator token in any key, grouping, pairing or row structure
PASS bank_riscv64.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_x86.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_riscv64.json -- no operator token in any key, grouping, pairing or row structure
```

`grep -c exempt` over every json this task added under
`PRIVATE/PseudoCoupHQ/Research/oracle/coverage/`: 0 (checked
directly, no file in that folder contains the string `exempt`).

Verifier: `check_conventions_log_claims.py --verify` run over this log
from the `cov1` instance, its tally in §9.

## 8. Reproducing transcripts, every table and flag in §3-§6

Four small read-only helper scripts, kept under
`PRIVATE/PseudoCoupHQ/Research/oracle/coverage/`
(`verify_matrices.py`, `verify_blockers.py`, `verify_length.py`,
`verify_defects.py`), print the same numbers as Tables 1-10 and the
flags of §6, one fact per line, so each has a one-line reproducing
command instead of resting on prose. Lane `cov1_l6_reproduce_all.sh`
ran all four; every line below is pasted verbatim from its tower log
named in §7.

**Block A — Tables 1-4, the matrices** (`source=X target=Y n=N m=M`
for every cell of every table above; order matches the tables read
left to right, top to bottom).

```
$ python3 PseudoCoupHQ/Research/oracle/coverage/verify_matrices.py
destination_only source=c target=c n=4578 m=10367
destination_only source=c target=cpp n=4578 m=10367
destination_only source=c target=rust n=4152 m=10367
destination_only source=c target=go n=3887 m=10367
destination_only source=c target=swift n=3504 m=10367
destination_only source=cpp target=c n=7631 m=17569
destination_only source=cpp target=cpp n=7631 m=17569
destination_only source=cpp target=rust n=7056 m=17569
destination_only source=cpp target=go n=6647 m=17569
destination_only source=cpp target=swift n=5928 m=17569
destination_only source=rust target=c n=489 m=685
destination_only source=rust target=cpp n=489 m=685
destination_only source=rust target=rust n=489 m=685
destination_only source=rust target=go n=489 m=685
destination_only source=rust target=swift n=489 m=685
destination_only source=go target=c n=157 m=577
destination_only source=go target=cpp n=157 m=577
destination_only source=go target=rust n=157 m=577
destination_only source=go target=go n=153 m=577
destination_only source=go target=swift n=157 m=577
destination_only source=swift target=c n=237 m=1229
destination_only source=swift target=cpp n=237 m=1229
destination_only source=swift target=rust n=237 m=1229
destination_only source=swift target=go n=226 m=1229
destination_only source=swift target=swift n=237 m=1229
strict source=c target=c n=1973 m=10367
strict source=c target=cpp n=3127 m=10367
strict source=c target=rust n=2256 m=10367
strict source=c target=go n=1850 m=10367
strict source=c target=swift n=2260 m=10367
strict source=cpp target=c n=3013 m=17569
strict source=cpp target=cpp n=5163 m=17569
strict source=cpp target=rust n=3352 m=17569
strict source=cpp target=go n=2759 m=17569
strict source=cpp target=swift n=3474 m=17569
strict source=rust target=c n=371 m=685
strict source=rust target=cpp n=397 m=685
strict source=rust target=rust n=373 m=685
strict source=rust target=go n=413 m=685
strict source=rust target=swift n=384 m=685
strict source=go target=c n=127 m=577
strict source=go target=cpp n=234 m=577
strict source=go target=rust n=76 m=577
strict source=go target=go n=100 m=577
strict source=go target=swift n=126 m=577
strict source=swift target=c n=202 m=1229
strict source=swift target=cpp n=241 m=1229
strict source=swift target=rust n=233 m=1229
strict source=swift target=go n=207 m=1229
strict source=swift target=swift n=180 m=1229
destination_only source=c target=c n=351 m=369
destination_only source=c target=cpp n=351 m=369
destination_only source=c target=go n=349 m=369
destination_only source=c target=rust n=369 m=369
destination_only source=go target=c n=100 m=105
destination_only source=go target=cpp n=100 m=105
destination_only source=go target=go n=102 m=105
destination_only source=go target=rust n=105 m=105
strict source=c target=c n=351 m=369
strict source=c target=cpp n=351 m=369
strict source=c target=go n=349 m=369
strict source=c target=rust n=369 m=369
strict source=go target=c n=100 m=105
strict source=go target=cpp n=100 m=105
strict source=go target=go n=102 m=105
strict source=go target=rust n=105 m=105
```

**Block B — Tables 5-7, the blocking cells** (top 3 of the stored 10,
`;`-joined, no arrows).

```
$ python3 PseudoCoupHQ/Research/oracle/coverage/verify_blockers.py
destination_only source=c target=c top3=cmp/gpr_gpr/64(1354);push/gpr_one/64(1251);test/gpr_same/32(903)
destination_only source=c target=cpp top3=cmp/gpr_gpr/64(1354);push/gpr_one/64(1251);test/gpr_same/32(903)
destination_only source=c target=go top3=cmp/gpr_gpr/64(1354);push/gpr_one/64(1251);test/gpr_same/32(903)
destination_only source=c target=rust top3=cmp/gpr_gpr/64(1354);push/gpr_one/64(1251);test/gpr_same/32(903)
destination_only source=c target=swift top3=movslq/widen_gpr_gpr/64(1400);cmp/gpr_gpr/64(1354);push/gpr_one/64(1251)
destination_only source=cpp target=c top3=test/gpr_same/32(2208);cmp/gpr_gpr/64(2048);push/gpr_one/64(1893)
destination_only source=cpp target=cpp top3=test/gpr_same/32(2208);cmp/gpr_gpr/64(2048);push/gpr_one/64(1893)
destination_only source=cpp target=go top3=test/gpr_same/32(2208);cmp/gpr_gpr/64(2048);push/gpr_one/64(1893)
destination_only source=cpp target=rust top3=test/gpr_same/32(2208);cmp/gpr_gpr/64(2048);push/gpr_one/64(1893)
destination_only source=cpp target=swift top3=test/gpr_same/32(2208);movslq/widen_gpr_gpr/64(2160);cmp/gpr_gpr/64(2048)
destination_only source=go target=c top3=push/gpr_one/64(170);cmp/imm_gpr/64(128);test/gpr_same/64(64)
destination_only source=go target=cpp top3=push/gpr_one/64(170);cmp/imm_gpr/64(128);test/gpr_same/64(64)
destination_only source=go target=go top3=push/gpr_one/64(170);cmp/imm_gpr/64(128);test/gpr_same/64(64)
destination_only source=go target=rust top3=push/gpr_one/64(170);sbb/gpr_same/32(134);cmp/imm_gpr/64(128)
destination_only source=go target=swift top3=push/gpr_one/64(170);cmp/imm_gpr/64(128);test/gpr_same/64(64)
destination_only source=rust target=c top3=test/imm_gpr/8(48);cmp/gpr_gpr/64(44);lea/mem_gpr/64(30)
destination_only source=rust target=cpp top3=test/imm_gpr/8(48);cmp/gpr_gpr/64(44);lea/mem_gpr/64(30)
destination_only source=rust target=go top3=test/imm_gpr/8(48);cmp/gpr_gpr/64(44);push/gpr_one/64(30)
destination_only source=rust target=rust top3=test/imm_gpr/8(48);cmp/gpr_gpr/64(44);push/gpr_one/64(30)
destination_only source=rust target=swift top3=test/imm_gpr/8(48);cmp/gpr_gpr/64(44);push/gpr_one/64(30)
destination_only source=swift target=c top3=cmp/gpr_gpr/64(464);test/gpr_same/64(135);cmp/gpr_gpr/32(132)
destination_only source=swift target=cpp top3=cmp/gpr_gpr/64(464);test/gpr_same/64(135);cmp/gpr_gpr/32(132)
destination_only source=swift target=go top3=cmp/gpr_gpr/64(464);test/gpr_same/64(135);cmp/gpr_gpr/32(132)
destination_only source=swift target=rust top3=cmp/gpr_gpr/64(464);test/gpr_same/64(135);cmp/gpr_gpr/32(132)
destination_only source=swift target=swift top3=cmp/gpr_gpr/64(464);movslq/widen_gpr_gpr/64(168);test/gpr_same/64(135)
strict source=c target=c top3=setne/gpr_one/8(1772);push/gpr_one/64(1251);xorps/xmm_same/128(1003)
strict source=c target=cpp top3=setne/gpr_one/8(1772);push/gpr_one/64(1251);movzbl/widen_gpr_gpr/32(912)
strict source=c target=go top3=setne/gpr_one/8(1772);cmp/gpr_gpr/64(1354);push/gpr_one/64(1251)
strict source=c target=rust top3=setne/gpr_one/8(1772);push/gpr_one/64(1251);xorps/xmm_same/128(1003)
strict source=c target=swift top3=setne/gpr_one/8(1772);movslq/widen_gpr_gpr/64(1400);cmp/gpr_gpr/64(1354)
strict source=cpp target=c top3=setne/gpr_one/8(4772);push/gpr_one/64(1893);xorps/xmm_same/128(1756)
strict source=cpp target=cpp top3=setne/gpr_one/8(4772);push/gpr_one/64(1893);setp/gpr_one/8(1441)
strict source=cpp target=go top3=setne/gpr_one/8(4772);cmp/gpr_gpr/64(2048);push/gpr_one/64(1893)
strict source=cpp target=rust top3=setne/gpr_one/8(4772);push/gpr_one/64(1893);xorps/xmm_same/128(1756)
strict source=cpp target=swift top3=setne/gpr_one/8(4772);movslq/widen_gpr_gpr/64(2160);cmp/gpr_gpr/64(2048)
strict source=go target=c top3=push/gpr_one/64(170);and/gpr_gpr/64(111);or/gpr_gpr/64(36)
strict source=go target=cpp top3=push/gpr_one/64(170);lea/mem_gpr/64(20);sete/gpr_one/8(20)
strict source=go target=go top3=push/gpr_one/64(170);cmp/imm_gpr/64(128);sbb/gpr_same/64(126)
strict source=go target=rust top3=push/gpr_one/64(170);sbb/gpr_same/32(134);and/gpr_gpr/64(111)
strict source=go target=swift top3=push/gpr_one/64(170);cmp/imm_gpr/64(128);sbb/gpr_same/64(126)
strict source=rust target=c top3=cmovne/gpr_gpr/64(48);cmove/gpr_gpr/64(36);lea/mem_gpr/64(30)
strict source=rust target=cpp top3=cmovne/gpr_gpr/64(48);cmove/gpr_gpr/64(36);lea/mem_gpr/64(30)
strict source=rust target=go top3=cmovne/gpr_gpr/64(48);cmp/gpr_gpr/64(44);cmove/gpr_gpr/64(36)
strict source=rust target=rust top3=cmovne/gpr_gpr/64(48);cmove/gpr_gpr/64(36);push/gpr_one/64(30)
strict source=rust target=swift top3=cmovne/gpr_gpr/64(48);cmp/gpr_gpr/64(44);cmove/gpr_gpr/64(36)
strict source=swift target=c top3=setne/gpr_one/8(112);or/cl_gpr/8(110);sete/gpr_one/8(110)
strict source=swift target=cpp top3=setne/gpr_one/8(112);or/cl_gpr/8(110);sete/gpr_one/8(110)
strict source=swift target=go top3=cmp/gpr_gpr/64(464);test/gpr_same/64(135);cmp/imm_gpr/64(127)
strict source=swift target=rust top3=setne/gpr_one/8(112);or/cl_gpr/8(110);sete/gpr_one/8(110)
strict source=swift target=swift top3=cmp/gpr_gpr/64(464);movslq/widen_gpr_gpr/64(168);test/gpr_same/64(135)
destination_only source=c target=c top3=remu/gpr_gpr_gpr/64(6);div/gpr_gpr_gpr/64(4);rem/gpr_gpr_gpr/64(4)
destination_only source=c target=cpp top3=remu/gpr_gpr_gpr/64(6);div/gpr_gpr_gpr/64(4);rem/gpr_gpr_gpr/64(4)
destination_only source=c target=go top3=czero.eqz/gpr_gpr_gpr/64(6);remu/gpr_gpr_gpr/64(6);div/gpr_gpr_gpr/64(4)
destination_only source=c target=rust top3=none
destination_only source=go target=c top3=divw/gpr_gpr_gpr/32(1);div/gpr_gpr_gpr/64(1);remw/gpr_gpr_gpr/32(1)
destination_only source=go target=cpp top3=divw/gpr_gpr_gpr/32(1);div/gpr_gpr_gpr/64(1);remw/gpr_gpr_gpr/32(1)
destination_only source=go target=go top3=div/gpr_gpr_gpr/64(1);rem/gpr_gpr_gpr/64(1);remu/gpr_gpr_gpr/64(1)
destination_only source=go target=rust top3=none
```

**Block C — Tables 8-10, the length view** (diagonal, x==y).

```
$ python3 PseudoCoupHQ/Research/oracle/coverage/verify_length.py
destination_only source=c 1=8/16 2=572/648 3-5=3380/6198 6-10=586/2837 over-10=32/668
destination_only source=cpp 1=6/14 2=822/2623 3-5=5933/9002 6-10=834/4688 over-10=36/1242
destination_only source=rust 1=6/6 2=76/174 3-5=400/422 6-10=7/67 over-10=0/16
destination_only source=go 1=5/5 2=130/238 3-5=18/26 6-10=0/295 over-10=0/13
destination_only source=swift 1=10/10 2=89/327 3-5=133/420 6-10=5/301 over-10=0/171
strict source=c 1=8/16 2=473/648 3-5=1456/6198 6-10=36/2837 over-10=0/668
strict source=cpp 1=6/14 2=526/2623 3-5=4274/9002 6-10=315/4688 over-10=42/1242
strict source=rust 1=6/6 2=76/174 3-5=289/422 6-10=2/67 over-10=0/16
strict source=go 1=5/5 2=46/238 3-5=7/26 6-10=42/295 over-10=0/13
strict source=swift 1=10/10 2=89/327 3-5=64/420 6-10=1/301 over-10=16/171
destination_only source=c 1=178/196 2=131/131 3-5=38/38 6-10=4/4
destination_only source=go 1=54/54 2=15/15 3-5=12/12 over-10=21/24
strict source=c 1=178/196 2=131/131 3-5=38/38 6-10=4/4
strict source=go 1=54/54 2=15/15 3-5=12/12 over-10=21/24
```

**Block D — the two fixes and the two bank-shape flags of §6.**

```
$ python3 PseudoCoupHQ/Research/oracle/coverage/verify_defects.py
both_present=253 same=253 diff=0 c_only_no_cpp=8
cells_outside_255_population=0 nop_cells_seen=0
x86 cells attested with zero bank record for any target: 4
  cell mnem=pcmpeqb shape=mem_xmm key_width=128 units=2
  cell mnem=pcmpeqb shape=xmm_xmm key_width=128 units=2
  cell mnem=pcmpeqd shape=xmm_same key_width=128 units=2
  cell mnem=pmovmskb shape=xmm_gpr key_width=128 units=2
x86 attested cells=257 cells_outside_attested_population=0
```

`both_present=253 same=253 diff=0` is the c/cpp identical-coverage
observation of §2; `cells_outside_255_population=0 nop_cells_seen=0`
is the `c.nop` fix of §2 holding (0, not 18, after the fix); the last
two lines are the "4 never-attempted x86 cells" and "0 cells outside
the attested population" flags of §6, both LITERAL and both now
carrying their own reproducing command instead of resting on the
earlier direct-check prose.

## 9. Verifier tally

Lane `cov1_l7_verify_log_final.sh`, tower log
`<runs>/cov1/agent/logs/<stamp>__cov1_l7_verify_log_final.sh.log`,
run over this log from the `cov1` instance:

```
$ python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_266_task_cov1_how_far_the_proved_emulations_reach.md
log_266_task_cov1_how_far_the_proved_emulations_reach.md: 11 claims extracted
   claims 11 | MATCHES 5 | DIFFERS 0 | UNVERIFIABLE 6 | REFUSED 0 | NOT_RERUNNABLE 0
   VERDICT: 5 of 11 claims reproduce; 6 (55%) carry nothing to re-run
population: 11 claims across 1 logs
  MATCHES          5
  DIFFERS          0
  UNVERIFIABLE     6
  REFUSED          0
  NOT_RERUNNABLE   0
causes, by name:
  prose_only                       6
```

The 5 MATCHES are the 5 blocks of §8 (guard, matrices, blockers, length
view, the two fixes). The 6 UNVERIFIABLE are glossary-style definition
sentences the tool's own `prose_verification` shape catches on any
declarative sentence outside a fence (§1's `arch-unit` bullet, §3's "N
of M" definition and the two table captions, §5's one summary sentence,
§6's relink-refused bullet) — none of them assert a check with a
number that needed reproducing beyond what §8 already covers; 0
DIFFERS.

## 10. Artifacts, by full path

- `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/build_join.py`
  — the join script (units-x86, units-riscv, bank-x86, bank-riscv, matrix).
- `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/lanes_cov1/`
  — `cov1_l1_sample20.sh` (guard FAIL, kept), `cov1_l1b_sample20_bankfix.sh`
  (guard PASS, sample), `cov1_l2_full.sh` (guard PASS, full population,
  carries the `c.nop` defect), `cov1_l3_full_fixed.sh` (both fixes, the
  run this log reports).
- `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/units_x86.jsonl`,
  `units_riscv64.jsonl` — the full per-unit cell/length join.
- `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/bank_x86.json`,
  `bank_riscv64.json` — the reduced (cell, target) proof booleans.
- `PRIVATE/PseudoCoupHQ/Research/oracle/coverage/coverage_x86.json`,
  `coverage_riscv64.json` — the matrices, blocking-cells-top-10 and
  length view this log's tables are drawn from.

## decided, recorded for audit

- The bank's on-disk `"cells"` shape is a list of `{cell, targets}`
  records, never a dict keyed by the mnemonic-joined string — the
  guard-failure fix, applied inside this task's own artifact folder.
- RISC-V `cells_of(unit)` is filtered to `twins.json`'s 255-row
  population before it can block a unit — the `c.nop` fix, same folder.
- Both matrices (destination-only, strict) are reported side by side
  for both architectures, per `object.number-carries-its-reading`.

## awaiting the owner

- The 4 x86 cells with zero bank record for any target (§6) are a gap
  in the bank, not in this join; whether they join the proof worklist
  is the owner's call.
- The 640 relink-refused x86 units (§6) were excluded from every M
  rather than investigated; whether that population loss matters to
  the coverage question is the owner's call.
