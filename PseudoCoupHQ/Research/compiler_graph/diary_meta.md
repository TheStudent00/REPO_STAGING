# diary_meta — THE DIARY for the compiler graph (CORE 0_3_5, open item 1)

Produced 2026-08-24 in Airlock, lane `cg_diary_l1.sh`. This supersedes
the tally (`coverage_go.txt` / `coverage_meta.md`) for the region it
covers: the tally recorded HOW MANY TIMES each spot ran and lost the
order; the diary records each spot AS IT IS ENTERED, so the order is
kept.

**Evidence class.** Every line of `diary_go.txt` is fact FOR THE
OBSERVED RUN — one compile of one probe file by one compiler binary. It
proves what happened that time. It does not bound other inputs; the map
(`graph_go.json`) is what bounds all runs.

## What the diary is

`diary_go.txt`, one line per event, tab separated, in the order the
events happened:

```
seq   map_node_id                                              func_name    file:line
1     src/cmd/compile/internal/amd64/galign.go:266-603:func     Init         src/cmd/compile/internal/amd64/galign.go:14
```

The second column is the node id OF THE MAP — `<file>:<start_byte>-<end_byte>:<kind>`
— so a diary event joins to a map node by string equality, with no
line-number matching and no interpretation step. (The tally had to be
joined by `file:line` spans, and that join needed a correction: a
function's `func` header line never appears in coverage. The diary has
no such problem because the id is written into the source at injection
time.)

`file:line` in the fourth column is the ORIGINAL line, before injection.
Injection adds one line to each instrumented function, so lines in the
edited copy sit below the original ones; the recorded number is the one
that matches the vendored tree and the map.

## How it was produced

The pattern is v0's `inject_emitid`: place an edit at a byte offset that
comes from the parse, so the code announces its own id as it runs.

1. `inject_diary.py select` reads `graph_go.json`, picks the target
   spots (below), writes `diary_targets.json` — each record carries the
   map node id and the node's `start_byte`.
2. `inject_diary.py inject` writes a new package
   `cmd/compile/internal/diary` into a COPY of the compiler source
   (Airlock `/persist/gosrc/src`, never the read-only vendored tree),
   and inserts into each target, immediately after the brace that opens
   the body, exactly ONE self-contained statement:

   ```go
   func (state *assignState) assignParam(typ *types.Type, name *ir.Name, isResult bool) ABIParamAssignment {
   	diary.Note("src/cmd/compile/internal/abi/abiutils.go:20680-21192:method|assignParam|src/cmd/compile/internal/abi/abiutils.go:603")
   	registers := state.tryAllocRegs(typ)
   ```

   The body brace is found by scanning forward from the map node's
   `start_byte` for the first `{` whose rest of line is blank, which
   steps over `struct{}` / `map[string]struct{}` in signatures. Edits
   are applied in descending offset order, so every offset the map gave
   is still valid when it is used. One import line is added per touched
   file.
3. `diary.Note` appends `seq \t record \n` to the file named by the
   environment variable `COMPILER_DIARY`, under a lock, unbuffered.
   With the variable unset the compiler behaves exactly as before, so
   the instrumented binary is safe to leave in place.
4. cmd/compile is rebuilt, and the probe compiled by the replay recipe
   of `coverage_meta.md`: capture the real tool command line with
   `go build -a -work -x`, then run that exact line with the diary
   compiler substituted for `$GOROOT/pkg/tool/linux_amd64/compile`. The
   profile is therefore exactly one compile, of the probe's
   `package main` — no stdlib, no linker.

## Exact commands (container paths)

```sh
SRC=/persist/gosrc
export GOROOT="$SRC" PATH="$SRC/bin:$PATH"
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache

# restore the five files that get edited, from the read-only tree
for f in cmd/compile/internal/abi/abiutils.go \
         cmd/compile/internal/amd64/galign.go \
         cmd/compile/internal/amd64/ggen.go \
         cmd/compile/internal/amd64/ssa.go \
         cmd/compile/internal/ssagen/ssa.go ; do
  cp -f "/sources/golang_src/src/$f" "$SRC/src/$f"
done
rm -rf "$SRC/src/cmd/compile/internal/diary"

python3 inject_diary.py inject --targets diary_targets.json --src "$SRC/src"

cd "$SRC/src/cmd"
"$SRC/bin/go" build -o /persist/compile_diary cmd/compile

# probe: module probe, go 1.28
#   package main
#   //go:noinline
#   func af(a, b int32) int32 { return a - b }
#   func main() { println(af(7, 3)) }
cd /work/probe
"$SRC/bin/go" build -a -work -x -o /work/probe.bin . > /work/x.stdout 2> /work/x.log
# then replay the captured command line with /persist/compile_diary
# substituted, with COMPILER_DIARY=/work/diary.raw set.
```

The target list is produced on the host (the map is 126 MB and is not
mounted in the container):

```sh
python3 inject_diary.py select --graph graph_go.json --out diary_targets.json
```

Versions are unchanged from `coverage_meta.md`: tree `9f1012d9`
(2026-07-15), toolchain built from it,
`go version go1.28-devel-pseudocoup linux/amd64`, python 3.13.14 in the
container. The tree's provenance remains **unverified** (no `VERSION`
file upstream; the one in the copy was written by the earlier lane).

## Which spots are instrumented, and why those

Minimality rule of the CORE: only enough to show, in order, the spots
that handled the probe's parameters. 56 spots, in 5 files.

- **`seed_file`** (37) — every function and method of
  `internal/abi/abiutils.go`, the file the whole acceptance path lives
  in.
- **`map_neighbourhood`** (14) — the functions of `internal/ssagen`
  that THE MAP connects to the seed file within 3 call hops, in either
  direction. Computed, not chosen: the map's call edges are lifted to
  function-to-function edges (a function CONTAINS a call node which
  CALLS a function) and a breadth-first walk out of the 37 seeds is
  filtered to `internal/ssagen` and `internal/amd64`.
- **`hand_picked`** (5) — `internal/amd64`. The map reaches NO amd64
  function from the seed file at any hop; that is exactly the named
  frontier already recorded in `acceptance_query.txt` leg 2 ("NO PATH.
  Every branch died"), caused by unresolved field selectors. So these
  five are named by a person, not by the map, and are marked as such.
  They are the package's entry points into instruction emission.
- **`acceptance_path_start`** (1) — the parameter loop inside
  `ABIAnalyzeFuncType`. It is a loop, not a function, so it is named by
  the map node of the loop's own variable, `abiutils.go:12455-12460:local_var`
  — the node the 8-step acceptance path starts from.

41 of the 56 spots produced events; 15 never ran during the probe
compile. Counts below are per spot for this run.

**src/cmd/compile/internal/abi/abiutils.go**

| line | name | chosen by | events |
| --- | --- | --- | --- |
| 39 | `Config` | seed_file | 7 |
| 43 | `InParams` | seed_file | 16 |
| 47 | `OutParams` | seed_file | 24 |
| 51 | `InRegistersUsed` | seed_file | 13 |
| 55 | `OutRegistersUsed` | seed_file | 16 |
| 59 | `InParam` | seed_file | 6 |
| 63 | `OutParam` | seed_file | 6 |
| 67 | `SpillAreaOffset` | seed_file | 9 |
| 71 | `SpillAreaSize` | seed_file | 0 |
| 79 | `ArgWidth` | seed_file | 9 |
| 108 | `Offset` | seed_file | 0 |
| 118 | `RegisterTypes` | seed_file | 7 |
| 137 | `RegisterTypesAndOffsets` | seed_file | 6 |
| 148 | `appendParamTypes` | seed_file | 8 |
| 197 | `appendParamOffsets` | seed_file | 6 |
| 249 | `FrameOffset` | seed_file | 9 |
| 277 | `NewABIConfig` | seed_file | 2 |
| 282 | `Which` | seed_file | 0 |
| 289 | `LocalsOffset` | seed_file | 18 |
| 296 | `FloatIndexFor` | seed_file | 2 |
| 303 | `NumParamRegs` | seed_file | 0 |
| 315 | `ABIAnalyzeTypes` | seed_file | 0 |
| 353 | `ABIAnalyzeFuncType` | seed_file | 9 |
| 362 | `ABIAnalyzeFuncType.params_loop` | acceptance_path_start | 10 |
| 397 | `ABIAnalyze` | seed_file | 7 |
| 410 | `updateOffset` | seed_file | 7 |
| 438 | `regString` | seed_file | 0 |
| 449 | `ToString` | seed_file | 0 |
| 469 | `String` | seed_file | 0 |
| 492 | `align` | seed_file | 7 |
| 497 | `alignTo` | seed_file | 25 |
| 505 | `nextSlot` | seed_file | 7 |
| 514 | `allocateRegs` | seed_file | 10 |
| 573 | `setup` | seed_file | 9 |
| 603 | `assignParam` | seed_file | 10 |
| 623 | `tryAllocRegs` | seed_file | 10 |
| 657 | `ComputePadding` | seed_file | 0 |

**src/cmd/compile/internal/amd64/galign.go**

| line | name | chosen by | events |
| --- | --- | --- | --- |
| 14 | `Init` | hand_picked | 1 |

**src/cmd/compile/internal/amd64/ggen.go**

| line | name | chosen by | events |
| --- | --- | --- | --- |
| 28 | `ginsnop` | hand_picked | 0 |

**src/cmd/compile/internal/amd64/ssa.go**

| line | name | chosen by | events |
| --- | --- | --- | --- |
| 24 | `ssaMarkMoves` | hand_picked | 2 |
| 227 | `ssaGenValue` | hand_picked | 13 |
| 2454 | `ssaGenBlock` | hand_picked | 2 |

**src/cmd/compile/internal/ssagen/ssa.go**

| line | name | chosen by | events |
| --- | --- | --- | --- |
| 80 | `InitConfig` | map_neighbourhood | 1 |
| 294 | `buildssa` | map_neighbourhood | 2 |
| 645 | `zeroResults` | map_neighbourhood | 2 |
| 1663 | `stmt` | map_neighbourhood | 8 |
| 3028 | `exprCheckPtr` | map_neighbourhood | 8 |
| 3754 | `resultOfCall` | map_neighbourhood | 0 |
| 3848 | `append` | map_neighbourhood | 0 |
| 4681 | `softfloatInit` | map_neighbourhood | 0 |
| 4837 | `openDeferSave` | map_neighbourhood | 0 |
| 5371 | `canSSA` | map_neighbourhood | 9 |
| 5761 | `putArg` | map_neighbourhood | 3 |
| 6298 | `dottype1` | map_neighbourhood | 0 |
| 7533 | `defframe` | map_neighbourhood | 2 |
| 8100 | `deferstruct` | map_neighbourhood | 1 |

## Result

329 events. The whole compile of the probe touched 41 of the 56
instrumented spots. The acceptance excerpt is in the lane output
`/out/cg_diary_l1.txt` and reproduced in the report; in short, the
`params_loop -> assignParam -> tryAllocRegs -> allocateRegs` chain
appears ten times, each time in that exact order with nothing of the
instrumented set interleaved, three of those times inside the single
`ABIAnalyzeFuncType` call that analyses `af`.

## What the diary does NOT show

- Only entries are recorded, not exits. Nesting is read off the entry
  order plus the map's call edges; the diary alone does not prove
  containment.
- The 15 spots with zero events say only that they did not run in THIS
  run.
- The compile ran with `-c=6`, so the compiler may use several
  goroutines. `diary.Note` takes a lock, so no event is lost or torn,
  but events from different goroutines could in principle interleave in
  the sequence. In the observed run the chains below are contiguous, so
  no interleaving happened inside them; the diary does not carry a
  goroutine id, so that is an observation, not a guarantee. Adding a
  goroutine id to the record would close it.
- The register leg is still bounded by the frontier of
  `acceptance_query.txt` leg 2: the amd64 events sit in the diary in
  order relative to the abi events, but the MAP still has no edge
  joining them. Ordering next to each other is not a connection. That
  is lap two's "follow the dot", not something the diary can close.

## Files

- `inject_diary.py` — the instrumenter, both modes, re-runnable.
- `diary_targets.json` — the 56 chosen spots, with their map node ids.
- `diary_go.txt` — 329 events, in order.
- `lanes/cg_diary_l1.sh` — the lane, with the instrumenter and the
  target list embedded (the repo is not mounted in the container).
  It restores the five touched files first, so it is re-runnable.

---

# lap two — the diary says WHOSE parameters were being worked on

Appended 2026-08-24, lane `cg_diary_l2.sh`. Nothing above is rewritten;
`diary_go.txt` stands as the lap-one record. The new record is
`diary_go2.txt`.

## what was missing

A lap-one line said which SPOT of the compiler ran. It did not say whose
code the compiler was working on. Ten runs of the
`params_loop -> assignParam -> tryAllocRegs -> allocateRegs` chain were
visible; which of them belonged to the probe's `af` was read off the
surrounding order by a person, which is exactly the interpretation step
this node exists to remove.

## where the name is, and where it is not

The name is genuinely NOT reachable at the spots the chain runs in:

- `func (config *ABIConfig) ABIAnalyzeFuncType(ft *types.Type)` receives a
  function TYPE. A `*types.Type` carries no function name.
- `func (state *assignState) assignParam(typ *types.Type, name *ir.Name,
  isResult bool)` has a `name`, but it is the PARAMETER's name (`a`, `b`),
  not the function's.
- `tryAllocRegs(typ *types.Type)` and `allocateRegs(regs []RegIndex,
  t *types.Type)` have only the assign state and a type.

So the name is taken ONE LEVEL HIGHER, at five spots where an `*ir.Func`
or an `*ssa.Func` is in hand, and carried down. Those five, with the
expression that yields the name:

| file | function | expression |
| --- | --- | --- |
| `internal/gc/compile.go` | `enqueueFunc` | `fn.Sym().Name` |
| `internal/ssagen/ssa.go` | `buildssa` | `fn.Sym().Name` |
| `internal/ssagen/ssa.go` | `genssa` | `f.Name` |
| `internal/ssa/debug.go` | `PopulateABIInRegArgOps` | `f.Name` |
| `internal/ssa/debug.go` | `BuildFuncDebugNoOptimized` | `f.Name` |

`internal/gc` and `internal/ssa/debug.go` were not touched in lap one, so
the lane now restores SEVEN files, not five.

## how it is carried

`diary.Enter(spot, subject)` pushes the subject on a stack held PER
GOROUTINE and returns the func that pops it; it is injected as exactly one
statement, `defer diary.Enter("buildssa", fn.Sym().Name)()`, at the same
body brace the `Note` calls use. `diary.Note` stamps each event with the
innermost subject open on ITS OWN goroutine, or `-` when none is open.
The goroutine number comes from the first line of
`runtime.Stack(buf, false)`. Per goroutine and not one global matters:
the compile runs with `-c=6` and the probe's two functions are compiled
concurrently.

`Enter` also writes its own event, with the map node id `-` (these five
spots are subject boundaries, not spots from `diary_targets.json`).

## the record

`diary_go2.txt`, tab separated, one line per event:

```
seq   subject   map_node_id                                               spot_name   file:line
24    af        src/cmd/compile/internal/abi/abiutils.go:12455-12460:local_var  ABIAnalyzeFuncType.params_loop  src/cmd/compile/internal/abi/abiutils.go:362
```

337 events: 329 spot events, as in lap one, plus 8 subject-boundary
events. By subject: `main` 190, `af` 138, `-` 9. The nine `-` events are
compiler set-up that runs before any function is dequeued
(`amd64.Init`, `ssagen.InitConfig`, `deferstruct`, `NewABIConfig` x2,
`ArgWidth` x2, `LocalsOffset` x2).

## what the subject column corrected

Lap one recorded: "the chains below are contiguous, so no interleaving
happened inside them". That is now shown to be WRONG for at least one
chain. Events 42-46 of `diary_go2.txt`:

```
42  af    ...:12455-12460:local_var  ABIAnalyzeFuncType.params_loop
43  af    ...:20680-21192:method     assignParam
44  af    ...:21321-21801:method     tryAllocRegs
45  main  ...:12455-12460:local_var  ABIAnalyzeFuncType.params_loop
46  af    ...:17900-19209:method     allocateRegs
```

`main`'s loop event sits inside `af`'s chain. The chain is still `af`'s —
the subject says so — but the ORDER alone would have mis-read it. The
open point of lap one ("adding a goroutine id would close it") is
therefore half closed: the subject separates the two compiles, and a
goroutine id would close it fully.

## exact commands (container paths)

As lap one, with the restore list extended and the outputs renamed:

```sh
SRC=/persist/gosrc
for f in cmd/compile/internal/abi/abiutils.go \
         cmd/compile/internal/amd64/galign.go \
         cmd/compile/internal/amd64/ggen.go \
         cmd/compile/internal/amd64/ssa.go \
         cmd/compile/internal/ssagen/ssa.go \
         cmd/compile/internal/ssa/debug.go \
         cmd/compile/internal/gc/compile.go ; do
  cp -f "/sources/golang_src/src/$f" "$SRC/src/$f"
done
rm -rf "$SRC/src/cmd/compile/internal/diary"
python3 inject_diary.py inject --targets diary_targets.json --src "$SRC/src"
cd "$SRC/src/cmd" && "$SRC/bin/go" build -o /persist/compile_diary2 cmd/compile
```

The 56 spots and `diary_targets.json` are unchanged from lap one, so
`inject_diary.py select` did not have to be re-run.

## what lap two still does NOT show

- Still entries only, no exits, for the 56 spots. The five subject spots
  DO have an exit (the deferred pop), but it is not written down.
- No goroutine id in the record. The subject makes the interleave
  readable; a goroutine id would make it provable.
- A subject is the name of the function the compiler had in hand at the
  nearest enclosing subject spot. It is NOT proof that the spot's work
  concerned that function; it is proof of what was in hand. For the abi
  chain the two coincide, because `ABIAnalyze` is called on that
  function's own type inside `buildssa`.
- `-` means no subject spot was open, not that no function existed.

## files

- `inject_diary.py` — both modes, plus `SUBJECT_SPOTS`.
- `diary_go2.txt` — 337 events, in order, with subjects.
- `lanes/cg_diary_l2.sh` — the lane, generated from the repo copies of
  `inject_diary.py` and `diary_targets.json`. Restores the seven touched
  files first, so it is re-runnable.
