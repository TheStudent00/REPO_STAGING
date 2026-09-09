# log 215 — task o5: the lowering-route cut

Date: 2026-09-06. Instance `o5`, brought down at the end of this log.
Node: `hq.research.arch_unit_oracle.compiler_units.lowering_route_cut`
(`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_0_compiler_units/node_0_3_2_0_2_lowering_route_cut/CORE_0_3_2_0_2_lowering_route_cut.md`).
Step 1 of the master order (log_212 section 4).

Every rendering in this log is labelled per the protocol's §5.1a:
**LITERAL** is the object itself quoted from a file or a lane log,
**GLOSS** is a plain-words reading sitting beside a literal, and
**ANALOGY** is something that resembles the thing and is not it. No
gloss appears without its literal.

---

# 0. Restart note — the brief was not on disk when this run started

This task's own scratchpad brief (`task_o5_brief.md`) and the shared
law file (`LAW.md`) that a first attempt of this task read, per that
attempt's own `o5.conf` (copied under this brief's instruction from
`o3.conf`, quoting sizing reasoning back at itself), were **not
present** in the scratchpad directory named for this restart — the
first attempt was stopped by a session-wide usage limit before it
wrote either file's content anywhere durable, and the failure
notification shows it mid-read of `operator_variants_by_search.py`'s
`main()`, never having reached a deliverable.

What this run reconstructed the task from instead, all primary
sources, none invented:

- the node's own CORE (quoted in full at the top of
  `lowering_route_cut.py`'s docstring);
- `o5.conf`'s own header comment, which quotes the brief's sizing
  instructions back (cpus=2, memory=4g, `ABORT_MEMORY_O5` at 2 GB, the
  diary text size estimate, "Instance o5.conf from o3.conf");
- the orchestrating session's own parallel-launch summary naming this
  task's deliverable: "task o4's variants restricted to the emitter
  definitions and the diary-visited functions";
- task 95 (log_200) and task 81 (log_190) for what "emitter
  definitions" and "diary-visited functions" concretely are;
- the sibling restart briefs (`task_o6_resume.md`, `task_o7_brief.md`)
  for the shared conventions this line uses (the guard, the log-claims
  verifier, the Airlock lane/log/PROGRESS/instance-down closing
  sequence) — read for FORMAT only, not copied as this task's content.

Flagged here rather than silently patched over, per the standing rule
that a missing input is a flag, not a license to invent the brief's
specifics. If the original brief resurfaces with instructions this run
did not anticipate, this log's own method (section 2) is what to
check against it.

---

# 1. What was done, in plain words

## 1.1 The one-line account

`lowering_route_cut.py` re-scans o4's two ROUTED rows (`go_compiler`,
`clang_llvm_cpp` — the only two with both a diary and an
arch-opcode-node measurement) for the same operator sites o4 found,
keeping only sites whose ENCLOSING FUNCTION is a member of the union
of task 95's emitter definitions (57 go / 251 clang,
`arch_opcode_nodes_{go,cpp}.json`) and task 81/72's diary-visited
function declarations — so the compiler's ROUTING is counted apart
from its whole source, answering the owner's 2026-09-06 surprise at the
whole-source counts.

## 1.2 The numbers that matter, each with its population

**LITERAL**, re-run inside instance `o5`:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.json'))
for row in d['rows']:
    print(row['row_id'])
    for k, v in row['population_at_each_filter'].items():
        print(' ', k, '=', v)
"
clang_llvm_cpp
  whole_source_sites_all_lowered_operators = 39451
  emitter_definitions = 251
  diary_visited_functions = 1331
  emitter_definitions_also_diary_visited = 45
  route_population_union = 1537
  sites_on_route_total = 0
  sites_on_route_resolved_to_a_variant = 0
  sites_on_route_unresolved_or_partial = 0
  distinct_route_variants = 0
go_compiler
  whole_source_sites_all_lowered_operators = 103475
  emitter_definitions = 57
  diary_visited_functions = 731
  emitter_definitions_also_diary_visited = 12
  route_population_union = 776
  sites_on_route_total = 5446
  sites_on_route_resolved_to_a_variant = 283
  sites_on_route_unresolved_or_partial = 5163
  distinct_route_variants = 104
```

**GLOSS.**

- **go: 103,475 whole-source sites cut to 5,446 on the route (5.3%),
  283 of those resolved into 104 distinct variants.** This is the
  number the CORE's "tens of variants in a handful of types"
  expectation should be read against — same order of magnitude, a
  little over "tens" (104), because `go_compiler`'s row is the WHOLE
  of `cmd/compile` (four sub-packages: `ssagen`, `amd64`, `ssa`,
  `abi`), not one narrow file.
- **clang: 39,451 whole-source sites cut to ZERO on the route.** Not a
  bug — checked below (section 1.3) and cross-checked against two
  independently published numbers.
- **The two population sizes that matter are independently
  verifiable**: `diary_visited_functions` (731 go, 1,331 clang) and
  `emitter_definitions` (57 go, 251 clang) are re-derivations of
  numbers task 72/81 and task 95 already published. 1,331 is log_190's
  own headline number verbatim ("1,331 of 8,871 instrumented compiler
  bodies visited by at least one of those 1,380 probes"); 57 and 251
  are log_200's own headline numbers verbatim ("57 of 1,859 go
  definitions produce a machine instruction"; "251 of 10,789 clang
  definitions produce one"). Getting these exactly right from a
  from-scratch re-parse of the diary text and a from-scratch read of
  `arch_opcode_nodes_{go,cpp}.json` is the check that the route
  population itself is built correctly, before its intersection with
  o4's sites is trusted.

## 1.3 Why clang lands at zero, not a bug

**LITERAL**, `operator_variants_by_search.py` `rows_def`, the
`clang_llvm_cpp` row's own scanned directories:

```
[f"{SOURCES}/llvm-project/llvm/lib/CodeGen/SelectionDAG",
 f"{SOURCES}/llvm-project/llvm/include/llvm/CodeGen",
 f"{SOURCES}/llvm-project/llvm/include/llvm/IR",
 f"{SOURCES}/llvm-project/llvm/include/llvm/MC",
 f"{SOURCES}/llvm-project/llvm/include/llvm/Target"]
```

**LITERAL**, `arch_opcode_nodes_cpp.json`'s own region and every
`definitions_marked` file prefix:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupGraphs/arch_opcode_nodes_cpp.json'))
print('region_directories', d['region_directories'])
print('definitions_marked file prefixes', sorted(set('/'.join(x['file'].split('/')[:4]) for x in d['definitions_marked'])))
"
region_directories ['clang/lib/CodeGen', 'llvm/lib/Target/X86']
definitions_marked file prefixes ['llvm/lib/Target/X86']
```

**GLOSS.** o4 scanned `llvm/lib/CodeGen/SelectionDAG` (LLVM's
target-independent DAG legalization) plus four include trees. Task
95's 251 emitter definitions are ALL in `llvm/lib/Target/X86` (the
backend that actually encodes machine instructions) — a directory o4
never scanned for this row. Task 81's diary hooks were placed in
`clang/lib/CodeGen` (the clang FRONTEND's own IR generation, log_190
section 2.1) — a third, still different directory. `SelectionDAG` sits
between the two: it consumes the frontend's IR and produces the input
the backend encodes, and apparently no function IN `SelectionDAG`
ITSELF (as opposed to functions it calls in `Target/X86`) happens to
both use a lowered operator AND be one of the 1,537 route
coordinates. That is a real, checkable fact about this row's directory
choice, not a defect in the cut: the emitter-definition and
diary-visited population sizes both reproduce their source tasks'
published numbers exactly (section 1.2), so the union is correctly
built; it simply does not reach into the one directory o4 measured.

**What this is NOT claimed to mean:** not that clang's compiler never
routes an operator through code the diary/emitter evidence would
recognize — the diary's own visited set (1,331) and task 95's emitter
set (251) are both non-empty and both drawn from clang's own source;
it is o4's PARTICULAR five directories for this one row that miss
them. Widening the clang row's directories (to `clang/lib/CodeGen` and
`llvm/lib/Target/X86` themselves) would be a natural next step and is
named here as awaiting the owner, not attempted — o4's own row definitions
are reused verbatim per this task's reuse convention (section 2 of
`lowering_route_cut.py`'s docstring), and widening them is a change to
o4's own deliverable, not this cut.

## 1.4 The go route, by variant (top 15 of 104, full table in
`lowering_route_cut.md`)

**LITERAL**:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.json'))
row = [r for r in d['rows'] if r['row_id']=='go_compiler'][0]
for v in row['route_variants'][:15]:
    ops = v['operands']
    lhs = ops[0]['spelling']
    rhs = ops[1]['spelling'] if len(ops) > 1 else ''
    print(v['operator'], '|', lhs, '|', rhs, '| sites=' + str(v['sites']))
"
- | integer literal |  | sites=70
<< | integer literal | integer literal | sites=12
& | registerCursor |  | sites=10
- | integer literal | integer literal | sites=9
! | bool |  | sites=8
< | int64 | integer literal | sites=6
+ | uint64 | uint64 | sites=6
- | integer literal | int | sites=6
& | State |  | sites=5
& | types.Sym |  | sites=4
- | uint64 | uint64 | sites=4
+ | int64 | int64 | sites=4
< | register | integer literal | sites=4
- | register | integer literal | sites=4
* | **Value |  | sites=4
```

**GLOSS.** Unary `-` on an integer literal dominates (70 sites) —
sign-flip constants inside instruction-selection rewrite rules, which
is exactly the kind of site the route is meant to isolate: it is
COUNTED against the whole-source population of the same operator
(7,225 sites for `-`/integer-literal in o4's un-cut json, log_210) but
never claimed to BE all of it.

## 1.5 Five literal route-site examples, with the reason each is on
the route

**LITERAL**:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.json'))
row = [r for r in d['rows'] if r['row_id']=='go_compiler'][0]
for ex in row['route_examples_sample'][:5]:
    print(ex['site'], '|', ex['operator'], '|', ex['operand_types'], '| enclosing func line', ex['enclosing_function_line'], '|', ex['route_reason'])
"
src/cmd/compile/internal/amd64/ggen.go:14 | % | ['int64', 'integer literal'] | enclosing func line 13 | diary
src/cmd/compile/internal/amd64/ggen.go:17 | >= | ['int64', 'integer literal'] | enclosing func line 13 | diary
src/cmd/compile/internal/amd64/ggen.go:22 | != | ['int64', 'integer literal'] | enclosing func line 13 | diary
src/cmd/compile/internal/amd64/ssa.go:132 | <= | ['int64', 'integer literal'] | enclosing func line 121 | diary
src/cmd/compile/internal/amd64/ssa.go:135 | <= | ['int64', 'integer literal'] | enclosing func line 121 | diary
```

**GLOSS.** All five sampled examples are `route_reason: diary` (the
function was seen entered while compiling some probe of the original
corpus), not `emitter_def` — expected, since `emitter_definitions` is
the much smaller set (57 vs 731 for go) and sits mostly at the very
bottom of the call chain (the instruction-emission call itself), while
a probe's compilation visits many MORE functions upstream of that
point. 12 of the 776 go route coordinates are `emitter_def+diary`
(both); none of the sampled 40 examples happened to land on one, which
is expected given they are 12 of 776 (~1.5%) of the route population.

## 1.6 What is NOT claimed

- **Not** that this is the FULL lowering route. It is o4's two routed
  rows' sites, cut by a route population built from two existing
  measurements (task 95, task 81/72) over the SAME two rows' own
  scanned directories. A wider directory choice (section 1.3) or a
  third route signal would change the numbers.
- **Not** that the 104 go variants or the 0 clang variants are
  compiler-independent. Both compilers are pinned exactly as o3/o4 and
  task 95/81/72 pinned them; nothing was rebuilt.
- **Not** that `sites_on_route_unresolved_or_partial` (5,163 of 5,446
  for go) means those sites are uninteresting — they are the same
  "unresolved by search alone" population o4 already reports for the
  whole source (o4's `sites_unresolved`/`sites_partly_resolved`
  columns), inherited unchanged onto the smaller route population;
  this task did not attempt a stronger resolver.
- **Not** that `diaries/extended`'s extra 2,600 regenerated probes
  were folded into the cut. They were read separately as a robustness
  check only (below) because task 95/81's own citation is the base
  1,380-probe corpus, not the regenerated extension.

## 1.7 Robustness check — the regenerated-probe diary extension

**LITERAL**:

```
$ python3 -c "
import json
d = json.load(open('PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.json'))
row = [r for r in d['rows'] if r['row_id']=='clang_llvm_cpp'][0]
print(row['diary_extended_robustness_check'])
"
{'dirs': ['PseudoCoupGraphs/diaries/extended'], 'n_files': 3980, 'n_lines': 24932220, 'distinct_coords': 1482, 'distinct_coords_gained_over_base_diary': 151}
```

**GLOSS.** Reading `diaries/extended` (the 1,380 original + 2,600
regenerated probes, 3,980 files) instead of `diaries/c_and_cpp` widens
the clang diary-visited set from 1,331 to 1,482 distinct function
coordinates (+151, matching log_190's own "151 further compiler bodies
are reached when 2,600 regenerated probes are added" exactly). The
route union would grow from 1,537 to roughly 1,537 + up to 151 (some
of the 151 may already be emitter definitions) — still nowhere near
touching `llvm/lib/CodeGen/SelectionDAG`, so this does not change
section 1.3's zero.

---

# 2. The instrument

`lowering_route_cut.py`
(`PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.py`),
imports its scanning machinery from `operator_variants_by_search.py`
(task o4) and `compiler_operators_used.py` (task o3) rather than
forking it — `build_language_inventory`, `lowered_set_for`,
`iter_source_files`, `build_parser`, `get_operator_text`,
`operand_nodes`, `unwrap_and_resolve`, `describe`, `COLLECTORS`,
`FUNC_TYPES`, `CLASS_TYPES`, `line_of`. NEW in this task: an
enclosing-function-OWN-LINE map (o4's own `enclosing_stacks` keeps the
function node's tree-sitter id, not its source line, since o4 never
needed the line), the emitter-definition and diary-visited population
builders, and the route-membership filter applied inside the site
walk. The docstring at the top of the file carries the full method
note; not duplicated here.

## 2.1 Diary line parsing, checked against two conventions

Task 81's clang diary line (log_190 section 2.1):
`file#line#kind#ordinal|display_name|file:line` — the enclosing
function's own declaration coordinate is the LAST `|`-separated field.
Task 72's go diary line (found in `diaries/go/*.txt`, not previously
quoted in a log) uses a DIFFERENT first two fields but the SAME
convention for the last one:

**LITERAL**, `diaries/go/op_0.txt` line 1:

```
1	-	src/cmd/compile/internal/ssa/rewrite.go:22841-22896:func|StringToAux|src/cmd/compile/internal/ssa/rewrite.go:815
```

**GLOSS.** Splitting on `\t` then taking field 3, then splitting THAT
on `|` and taking the LAST field, gives `file:line` for both diary
families with the one parsing rule — no per-language branch was
needed. `n_unparsed_lines` (1,380 for clang, 3,540 for go, both in
section 1.2's own json) counts the lines this rule could not read
(fewer than 3 tab fields, usually the diary's own header/footer
lines — one unparsed line per file at minimum, matching the file
counts closely).

## 2.2 Cost

**LITERAL**:

```
$ cat PseudoCoupHQ/Research/oracle/compiler_units/lane_logs/20260906T103637Z__o5_l1b_lowering_route_cut.sh.log
# script: /drop/o5_l1b_lowering_route_cut.sh
# started: 2026-09-06T10:36:37+00:00
# timeout: 3600s
# work free before: 1024 MB
------------------------------------------------------------
[1/1] lowering_route_cut.py -- route_examples given lang+unit fields (guard fix, o5_l2 findings)
[clang_llvm_cpp] scanning...
  clang_llvm_cpp: files=561 whole_source_sites=39451 route_sites=0 route_variants=0
[go_compiler] scanning...
  go_compiler: files=734 whole_source_sites=103475 route_sites=5446 route_variants=104
done in 83.8s, peak RSS 515.5 MB
exit: 0
------------------------------------------------------------
# exit 0 in 83.9s
# work free after: 1024 MB (consumed 0 MB)
```

**GLOSS.** 83.8s, 515.5 MB peak — well under the 2,048 MB
`ABORT_MEMORY_O5` bound and the 3,600s timeout. Diary text (~2.3 GB
across `diaries/go` and `diaries/c_and_cpp`) is streamed one line at a
time; the accumulated visited-coordinate sets top out at 731 and 1,331
entries, which is why peak RSS tracks the tree-sitter parse of the
largest single source file plus the small accumulating sets, not the
diary text's own size — the design `o5.conf`'s own header comment
predicted.

A first run (`o5_l1_lowering_route_cut.sh`, not repeated in full here)
produced the same numbers; it is superseded by `o5_l1b` only because
the guard below found `route_examples_sample` entries with a bare
`operator` field and no `lang`/`unit` — the SAME finding shape task
o3 hit and fixed in log_209 (rule 1 of the guard's own violation
list). Fixed the same way: each example object given an opaque
`unit` id (`f"{row_id}#ex{i}"`), never colon-joined with the operator
token.

## 2.3 The guard, final run

**LITERAL**:

```
$ python3 Airlock/airlock submit PseudoCoupHQ/Research/oracle/compiler_units/lanes_o5/o5_l2b_spelling_guard.sh --instance o5 --no-batch
```

```
(not re-run here: submits/moves the sandbox itself, by design outside
this verifier's scope)
$ cat PseudoCoupHQ/Research/oracle/compiler_units/lane_logs/20260906T103904Z__o5_l2b_spelling_guard.sh.log
# script: /drop/o5_l2b_spelling_guard.sh
# started: 2026-09-06T10:39:04+00:00
# timeout: 3600s
# work free before: 1024 MB
------------------------------------------------------------
[1/1] check_no_spelling_keys.py over lowering_route_cut.json, final
operator inventory: 91 tokens read from probe_manifest_*.json
PASS lowering_route_cut.json -- no operator token in any key, grouping, pairing or row structure
guard exit: 0
------------------------------------------------------------
# exit 0 in 0.1s
# work free after: 1024 MB (consumed 0 MB)
```

**GLOSS.** PASS. The first attempt (`o5_l2_spelling_guard.sh`) found
40 findings (every `route_examples_sample[i].operator`, one per go
example) — the fix in section 2.2, re-run here clean.

---

# 3. Instance up/down

**LITERAL**:

```
$ bash Airlock/up.sh --instance o5
=== airlock up ===
  instance: o5   runner: o5-runner   agent: <runs>/o5/agent
  config:   Airlock/instances/o5.conf
  proxy: none (instance is configured 'proxy = no' — no route out at all)
  o5-runner already existed; started (bound to <runs>/o5/agent/drop)

  o5-runner  Up Less than a second  localhost/sandbox-runner:latest
```

Mounts came from this machine's shared `mounts.conf` (`o5.conf` sets
no `mounts_file` override): `PseudoCoupHQ:rw`, `/sources:ro`,
`PseudoCoupGraphs:rw`, `PlanPlan:ro` — already
covering every path this task reads; no mount edit was needed.

```
$ bash Airlock/down.sh --instance o5
```

(run at the close of this log, output not pasted — see the verifier
tally below, which was run BEFORE the instance came down, since the
verifier itself is a lane submitted to instance `o5`.)

---

# 4. Verifier tally

(this section is written AFTER the lane below actually ran, over the
file as it stood through section 3 — the same two-pass shape task o3
used in log_209, to avoid a claim about a lane log that does not exist
yet)

**LITERAL**, first pass (`o5_l3_claims_verify.sh`):

```
$ python3 Airlock/airlock submit PseudoCoupHQ/Research/oracle/compiler_units/lanes_o5/o5_l3_claims_verify.sh --instance o5 --no-batch
```

```
$ cat <runs>/o5/agent/logs/20260906T152204Z__o5_l3_claims_verify.sh.log
...
log_215_task_o5_lowering_route_cut.md: 13 claims extracted
...
   claims 13 | MATCHES 4 | DIFFERS 1 | UNVERIFIABLE 3 | REFUSED 4 | NOT_RERUNNABLE 1
```

**GLOSS.** 1 DIFFER, at section 1.2's `python3 -c "..."` re-run
(line 73 as the file then stood): the verifier's fresh run of that
exact command prints `clang_llvm_cpp` first then `go_compiler` (the
order `d['rows']` is stored in the json), but section 1.2 had pasted
the two rows in the opposite order (`go_compiler` then
`clang_llvm_cpp`) — same two rows, same values, wrong order, a paste
error introduced when the section was drafted go-first for narrative
reasons. Per the standing rule (fix the paste to the literal re-run,
never the verifier), section 1.2 above was corrected to the actual
output order (`clang_llvm_cpp` then `go_compiler`); no value changed.

**LITERAL**, second pass (`o5_l3b_claims_verify.sh`), after that fix:

```
$ python3 Airlock/airlock submit PseudoCoupHQ/Research/oracle/compiler_units/lanes_o5/o5_l3b_claims_verify.sh --instance o5 --no-batch
```

```
$ cat <runs>/o5/agent/logs/20260906T152402Z__o5_l3b_claims_verify.sh.log
...
log_215_task_o5_lowering_route_cut.md: 13 claims extracted
...
   claims 13 | MATCHES 5 | DIFFERS 0 | UNVERIFIABLE 3 | REFUSED 4 | NOT_RERUNNABLE 1
   VERDICT (SUMMARY, ALL LOGS): 5 of 13 claims reproduce; 3 (23%) carry
   nothing to re-run (2 attribution_only citing source files with no
   command, 1 prose_only restating section 1.2's own numbers with no
   command beside it); 4 REFUSED (3 `submits_or_moves_the_sandbox` —
   the `airlock submit`/`up.sh`/`down.sh` calls in sections 2.3 and 3,
   refused by design; 1 `redirects_into_a_path` — section 1.2's third
   `python3 -c` at the file's earlier line numbering, a bare `>`
   pasted output the checker cannot safely replay); 1
   NOT_RERUNNABLE — the elided (`...`) lane-log cat in section 2.2.

**TALLY LINE: claims 13 | MATCHES 5 | DIFFERS 0 | UNVERIFIABLE 3 |
REFUSED 4 | NOT_RERUNNABLE 1. Zero DIFFERS.**
