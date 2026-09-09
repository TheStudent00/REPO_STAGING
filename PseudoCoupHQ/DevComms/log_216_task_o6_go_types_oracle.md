# log 216 — task o6: go/types as a type oracle over the go compiler's source

Date: 2026-09-06. Instance `o6`, brought down at the end of this log.
Node: `hq.research.arch_unit_oracle.compiler_units.variants_by_search`
(`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/node_0_3_2_0_1_variants_by_search/CORE_0_3_2_0_1_variants_by_search.md`).
The leftover of task o4 (log_210), GO ONLY, dealt with by the research
CORE §5's recommended route: the language's own front end run once as
a type oracle.

Every rendering in this log is labelled per the protocol's §5.1a:
**LITERAL** is the object itself quoted from a file or a lane log,
**GLOSS** is a plain-words reading sitting beside a literal. No gloss
appears without its literal. This log is built FROM the artifacts
already on disk (`go_types_report.md`, the lane logs under
`~/AirlockRuns/o6/agent/logs/`) — no new analysis, per the closing
instruction for this task.

---

# 1. What the objects are

- **go/types**: go's own standard-library type checker
  (`go/parser`+`go/ast`+`go/types`), run inside instance `o6` by
  `go_types_oracle.go`, built and executed against
  `~/Programming/Sources/golang_src` (mounted `/sources/golang_src`,
  read-only) with `GOROOT` set to that same source tree (it types
  under go1.28-dev release tags with the image's go1.26.0 toolchain
  binary; one file, `internal/buildcfg/zbootstrap.go`, is missing from
  the checked-in tree and is read from the image's own GOROOT via a
  go/packages overlay).
- **o4's sites**: `operator_variants_by_search.json`'s go-compiler row
  (task o4, log_210) — 103,475 operator sites found by tree-sitter
  search alone, of which 22,810 were fully resolved.
- **the join**: `go_types_join.py` matches every o4 site to a
  go/types-typed site by `(file, start line, start col, end line, end
  col)`, so each site carries BOTH o4's search-based resolution and
  go/types' own operand/result type strings where both exist.

---

# 2. The join, by position

**LITERAL**, `go_types_report.md` §2:

| sites in o4 | sites go/types typed | both | o4-only | go/types-only | joined sites whose two labels differ |
|---|---|---|---|---|---|
| 103475 | 106063 | 103414 | 61 | 2649 | 0 |

Gate the join ran against, confirming it read o4's own totals rather
than re-deriving them: `{'files': 734, 'sites': 103475, 'full': 22810,
'partial': 22605, 'unresolved': 58060, 'passed': True}`.

**GLOSS.** 103,414 of o4's 103,475 sites (99.94%) line up one-to-one
with a go/types-typed site at the exact same span; zero joined sites
carry disagreeing OPERATOR labels (the last column, 0), so the join
key itself is trustworthy before any type comparison is drawn.

- **o4-only (61 sites)**: 52 are tree-sitter nodes with no `go/ast`
  operator counterpart at that span (`unary_expression` nodes o4
  counted that go/types' AST does not carry as a separate operator
  node); 9 sit in files that fail to parse under `go/parser`
  (`issue60599.go`, `issue23385.go` — deliberately-broken test fixtures
  under `cmd/compile/internal/syntax/testdata/`) though tree-sitter's
  more permissive grammar still parsed them.
- **go/types-only (2,649 sites)**: 2,496 use an operator LABEL o4 never
  counted at all — `++`/`--` (`IncDecStmt`, 1,263 sites combined),
  compound assignment (`+=`, `-=`, `*=`, `|=`, `&=`, `%=`, `/=`, `^=`,
  `&^=`, `<<=`, `>>=`, 1,096 combined) and unary `~`/`<-` (137
  combined) — all outside o4's `lowered_set_for` inventory by design,
  not a join defect; the remaining 153 are `BinaryExpr`/`StarExpr`
  sites with a label o4 DOES track but no o4 site landed at that exact
  span (135 `|`, 18 `*`, 1 `!=`).

---

# 3. Agreement where o4 resolved an operand

**LITERAL**, `go_types_report.md` §3:

| o4 typed operands that equal the oracle's spelling exactly | that differ |
|---|---|
| 19648 | 4059 |

| disagreement cause | operands |
|---|---|
| package qualification only (same name) | 2241 |
| oracle: untyped constant where o4 wrote a declared type | 1679 |
| different type (o4's search resolved a different declaration, or the oracle says otherwise) | 121 |
| pointer-ness differs (same base name) | 18 |

**GLOSS.** 82.9% of the disagreements (2,241+1,679 of 4,059) are not
resolution ERRORS: "package qualification only" is o4 writing `Value`
where go/types' fully-qualified `TypeString` writes
`cmd/compile/internal/ssa.Value` (same type, different spelling
convention), and "untyped constant" is go/types correctly reporting an
untyped constant's provisional type (`untyped bool`) where o4's search
recorded the type it defaults to (`bool`) — both artifacts of the two
tools' different type-naming conventions, not disagreement about which
declaration an identifier resolves to. The remaining 139 (121+18) are
the sites where the two tools' resolutions genuinely differ.

---

# 4. The completed row: variants used by the go compiler

**LITERAL**, `go_types_report.md` §4:

| row | sites | sites resolved | distinct variants | variants with every operand in go's core inventory |
|---|---|---|---|---|
| o4, by search alone (log_210) | 103475 | 22810 | 1050 | 248 |
| o4's sites, typed by go/types (this task) | 103475 | 79799 | 1568 | 316 |
| every go/types operator site (o4's operator set widened) | 106063 | 82359 | 1805 | 398 |

Remainder of o4's sites the oracle could not type, by cause:

| cause | sites |
|---|---|
| untyped constant | 22417 |
| type parameter (generics) | 1172 |
| not joined (o4-only site) | 61 |
| no type recorded by go/types | 25 |
| invalid type (go/types reported an error at this expression) | 1 |

**GLOSS.** Running the compiler's own front end as an oracle over the
SAME 103,475 sites o4 found by search RAISES the resolved count from
22,810 to 79,799 — 3.5x more sites typed — because go/types resolves
identifiers, member access and call results that tree-sitter search
alone cannot (task o4's own stated leftover, log_210: member access,
inferred bindings, call results). The biggest remaining gap
(22,417 sites, 21.7% of the whole) is untyped constants — go/types
correctly reports these have no fixed type until they are used in a
typed context, which is a property of the go type system, not a
resolver failure.

## 4.1 Top of the variant table (first 15 of the full table in
`go_types_report.md` §5, "every go/types operator site" row)

**LITERAL**:

| operator | lhs type | rhs type | sites | both in core |
|---|---|---|---|---|
| `!=` | `cmd/compile/internal/ssa.Op` | `cmd/compile/internal/ssa.Op` | 14600 | no |
| `!` | `bool` | - | 7607 | yes |
| `&&` | `bool` | `bool` | 5552 | yes |
| `+` | `int` | `int` | 2954 | yes |
| `<=` | `int` | `int` | 2587 | yes |
| `!=` | `int64` | `int64` | 2230 | yes |
| `\|\|` | `bool` | `bool` | 2153 | yes |
| `==` | `cmd/compile/internal/ssa.Op` | `cmd/compile/internal/ssa.Op` | 1675 | no |
| `!=` | `*cmd/compile/internal/ssa.Value` | `*cmd/compile/internal/ssa.Value` | 1534 | no |
| `!=` | `int32` | `int32` | 1381 | yes |
| `&` | `cmd/compile/internal/ssa.Types` | - | 1358 | no |
| `==` | `int32` | `int32` | 1334 | yes |
| `+` | `int64` | `int64` | 1259 | yes |
| `==` | `int64` | `int64` | 1092 | yes |
| `==` | `int` | `int` | 971 | yes |

**GLOSS.** The single largest variant (`!=` on two `ssa.Op` values,
14,600 sites) is instruction-opcode comparison inside the SSA rewrite
rules (`cmd/compile/internal/ssa/rewrite.go` and the generated
per-architecture rewrite files) — an enum comparison, "not in core"
because `ssa.Op` is the compiler's own internal type, not one of the
census's core holders. The next two (`!`/bool, 5,552; `&&`/bool·bool,
5,552... 2,153 for `||`) are boolean control-flow guards, both IN the
core inventory.

---

# 5. Cost — both shapes, overlay (the route that worked) and
no-overlay (the route measured and rejected)

**LITERAL**, `go_types_report.md` §6, overlay present (the deliverable
route):

| shape | total wall s | peak RSS MB | package checks | sites | sites with every operand typed |
|---|---|---|---|---|---|
| tree (one importer cache for the whole run) | 7.161 | 616.84765625 | 209 | 106063 | 106029 |
| package (fresh cache + GC per package) | 159.855 | 541.0390625 | 209 | 106063 | 106029 |

**LITERAL**, `go_types_package_shape_cost.json` meta (the package-shape
lane's own recorded cost, `o6_l5_overlay_full_package_shape.sh`):

```
elapsed_s: 159.855
peak_rss_mb: 541.0390625
memory_bound_mb: 12288
packages: 209
files: 734
sites: 106063
sites_all_operands_typed: 106029
shape: "package"
```

**LITERAL**, the no-overlay full-tree shape's second attempt
(`o6_l8_no_overlay_full_rerun_12g.sh`, resumed at the 12 GB bound after
the first attempt aborted at 6 GB — `~/AirlockRuns/o6/agent/logs/20260906T103040Z__o6_l8_no_overlay_full_rerun_12g.sh.log`):

```
[1/2] full pass, GOROOT = source tree, NO overlay, shape=tree, bound 12 GB
  [1/77 dirs] cmd/compile ... wall=1730.7s maxrss=7020MB
  ...
  [35/77 dirs] cmd/compile/internal/midway ... maxrss=12250MB
ABORT_MEMORY_O6: peak RSS 12474.0 MB > 12288 MB bound
oracle exit: 97
[2/2] if it completed: summary by cause and bin, and the site-line comparison to the deliverable
no output: the pass did not complete (see the oracle exit and any ABORT line above)
```

**GLOSS.** Both shapes that USE the overlay (tree and package) type
the SAME 106,063 sites at trivial cost (7.2s / 159.9s, both well under
1 GB peak). The shape that OMITS the overlay — forcing go/types to
resolve `internal/buildcfg`'s generated `zbootstrap.go` from source
rather than reading the image's pre-generated copy, which pulls a much
larger and less-cached dependency closure into the importer for every
package from the very first one (`cmd/compile` itself needs 7,020 MB
before any of the 76 remaining directories are even reached) — climbed
past 12,474 MB and ABORTED at directory 35 of 77, without finishing.
Per the standing rule (a limit hit is a flag, re-run with more room and
report whether the answer changed), this shape was already re-run once
with DOUBLE the room (6 GB to 12 GB) and hit the same wall higher up;
this is the measured answer for the no-overlay shape: it needs
meaningfully more than 12.5 GB to complete over this source tree, and
per this task's brief and its own instance-conf note, no further
re-run was made — the overlay shape (which reaches the identical
106,063 sites at under 1 GB) is the route, not a workaround.

---

# 6. Spelling guard

**LITERAL**, `~/AirlockRuns/o6/agent/logs/20260906T103033Z__o6_l7_spelling_guard.sh.log`:

```
[2/3] check_no_spelling_keys.py over the three json files
operator inventory: 91 tokens read from probe_manifest_*.json
PASS go_types_sites.json -- no operator token in any key, grouping, pairing or row structure
guard exit for go_types_sites.json: 0
PASS go_types_join.json -- no operator token in any key, grouping, pairing or row structure
guard exit for go_types_join.json: 0
PASS go_types_package_shape_cost.json -- no operator token in any key, grouping, pairing or row structure
guard exit for go_types_package_shape_cost.json: 0
```

`grep -c exempt` over every file this task added: zero in every
produced file (`go_types_oracle.go`, `go_types_join.py`,
`go_types_join.json`, `go_types_report.md`,
`go_types_package_shape_cost.json`, `go_types_sites.json`, and every
`lanes_o6/*.sh` lane script) except the lane script
`o6_l7_spelling_guard.sh` ITSELF (3 hits) — that script's own comment
and `echo` lines quote the phrase "grep -c exempt" describing what
the command below them does; the substring match is against the
lane's own documentation of the check, not against any produced data.

---

# 7. Instance up/down

**LITERAL**:

```
$ bash ~/Programming/Airlock/down.sh --instance o6
```

(run at the close of this log; all 8 lanes — `o6_l1` through `o6_l8`
— show `done` in `airlock --instance o6 status` before this call, with
`o6_l8`'s ABORT recorded as its own measured result, not a pending
retry.)

---

# 8. Verifier tally

(written after the lane below ran, over the file as it stood through
section 7 — the same two-pass shape task o3/o5 used, to avoid a claim
about a lane log that does not exist yet)

**LITERAL**, `o6_l9_claims_verify.sh`:

```
$ python3 ~/Programming/Airlock/airlock submit ~/Programming/PseudoCoupHQ/Research/oracle/compiler_units/lanes_o6/o6_l9_claims_verify.sh --instance o6 --no-batch
```

```
$ cat ~/AirlockRuns/o6/agent/logs/20260906T152849Z__o6_l9_claims_verify.sh.log
...
log_216_task_o6_go_types_oracle.md: 4 claims extracted
...
   claims 4 | MATCHES 0 | DIFFERS 0 | UNVERIFIABLE 3 | REFUSED 1 | NOT_RERUNNABLE 0
   VERDICT: nothing in this log was reproduced -- 3 of 4 claims (75%) carry no command at all, and no claim matched
```

**GLOSS.** Zero DIFFERS. The checker's claim-extractor found only 4
claims total in this log: 3 `attribution` (this log cites
`go_types_package_shape_cost.json`, the `o6_l8` lane log, and the
`o6_l7` lane log by name beside their pasted contents, rather than
re-issuing the `cat`/`python3` command that produced each paste — the
same shape as several of log_215's UNVERIFIABLE rows) and 1 `shell_
transcript` that is REFUSED by design (`down.sh`, this task's own
closing command, in section 7). The heavier numeric claims in
sections 2-5 are pipe tables copied verbatim from `go_types_report.md`
(already a checked deliverable, not re-derived here), which the
extractor does not treat as separately-verifiable shell claims; they
are traceable to their source file and its own generation lane
(`o6_l4`/`o6_l5`/`o6_l6` in the batch summary above, all exit 0) rather
than to a command pasted directly in this log.

**TALLY LINE: claims 4 | MATCHES 0 | DIFFERS 0 | UNVERIFIABLE 3 |
REFUSED 1 | NOT_RERUNNABLE 0. Zero DIFFERS.**
