# coverage_meta — runtime layer for the compiler graph (log 072 §5a)

Produced 2026-08-24 in Airlock. Per-block execution counts of the Go
compiler's own source, for one compile of our probe file. Joins to a
tree-sitter graph of the same tree by `file:startLine.startCol,endLine.endCol`.

## Versions

- container toolchain (bootstrap only): `go1.26.0 linux/amd64`, GOROOT `/usr/lib/go-1.26`
- vendored tree `/sources/golang_src` (= `Sources/golang_src`):
  **no `VERSION` file** (the brief assumed one). It is a grafted shallow
  git checkout of master, commit `9f1012d9a1aa0831ff44ac9c767e96f9943d13fe`,
  2026-07-15. `src/internal/goversion/goversion.go` says `Version = 28`,
  i.e. **Go 1.28-dev** — two releases ahead of the installed 1.26.0.
- toolchain actually used: built from that tree, reports
  `go version go1.28-devel-pseudocoup linux/amd64`.

## Approach

Approach 1 (`go build -cover cmd/compile` with the installed go 1.26)
FAILED: `ambiguous import: found package cmd/compile in multiple modules
(cmd /persist/gosrc/src/cmd/compile, /usr/lib/go-1.26/src/cmd/compile)`.
The go command always adds its own GOROOT `cmd` module, so a foreign
`cmd` tree cannot be built in place by a mismatched toolchain.

Approach 2 (build the whole tree, then instrument) WORKED, with one fix:
`cmd/dist` needs a `VERSION` file or a VCS, and the copy had neither
(`.git` removed), so it tried `jj` and died. Writing a `VERSION` file
into the copy resolves it.

Second correction: `go build -cover` alone instruments only the *main*
package — the first run yielded 4 blocks total. `-covermode=count
-coverpkg=cmd/compile/...` is required for per-block counts across the
compiler. (`-cover` also defaults to `mode: set`, i.e. 0/1, not counts.)

## Exact commands (container paths)

```sh
export GOTOOLCHAIN=local GOPROXY=off GOFLAGS=-mod=mod GOCACHE=/persist/gocache
SRC=/persist/gosrc
cp -a /sources/golang_src/. $SRC/ && rm -rf $SRC/.git
printf 'go1.28-devel-pseudocoup\ntime 2026-07-15T22:11:42Z\n' > $SRC/VERSION

cd $SRC/src && GOROOT_BOOTSTRAP=/usr/lib/go-1.26 bash make.bash

export GOROOT=$SRC PATH=$SRC/bin:$PATH
cd $SRC/src/cmd
$SRC/bin/go build -cover -covermode=count -coverpkg=cmd/compile/... \
    -o /persist/compile_cov cmd/compile

# probe (module probe, go 1.28):
#   package main
#   //go:noinline
#   func af(a, b int32) int32 { return a - b }
#   func main() { println(af(7, 3)) }
cd /work/probe
$SRC/bin/go build -a -work -x -o /work/probe.bin .   # captures the real tool cmdline
# replay that exact cmdline with the instrumented binary substituted:
export GOCOVERDIR=/work/covdata
WORK=<the -work dir> /persist/compile_cov -o $WORK/b001/_pkg_.a \
  -trimpath "$WORK/b001=>" -p main -lang=go1.28 -complete \
  -buildid ... -goversion go1.28-devel-pseudocoup -c=6 -nolocalimports \
  -importcfg $WORK/b001/importcfg -pack ./probe.go

$SRC/bin/go tool covdata textfmt -i=/work/covdata -o coverage_full.txt
```

Direct invocation was chosen over `-toolexec`/GOROOT swapping because
swapping the compiler binary invalidates the whole build cache and would
have mixed the stdlib compiles into the profile. This way the profile is
**exactly one compile, of our probe's `package main`**.

## Row counts

| | rows |
|---|---|
| total blocks (all of cmd/compile/...) | 141,731 |
| visited (count > 0) — what `coverage_go.txt` keeps | 8,284 |
| visited in `internal/{ssagen,ssa,abi,amd64}` | 3,492 |

Breakdown: ssa 2,654 · ssagen 709 · abi 79 · amd64 50.
`coverage_go.txt` is 8,285 lines: the `mode: count` header plus the
visited rows. Unvisited rows were dropped; the total above is the record.

## Sample visited rows (target directories)

```
cmd/compile/internal/ssagen/ssa.go:518.2,518.19 1 2
cmd/compile/internal/ssa/decompose.go:246.2,248.31 3 4
cmd/compile/internal/ssagen/ssa.go:392.2,395.1 5 2
cmd/compile/internal/ssa/rewritegeneric.go:34680.3,34680.23 1 10
cmd/compile/internal/ssa/debug.go:884.2,884.21 1 6
cmd/compile/internal/ssagen/intrinsics.go:939.2,940.64 1 1
cmd/compile/internal/ssa/rewriteAMD64.go:7491.2,7491.14 1 19
cmd/compile/internal/ssa/allocators.go:18.3,19.1 1 62
cmd/compile/internal/ssa/fuse.go:51.5,52.1 1 2
cmd/compile/internal/abi/abiutils.go:48.2,49.1 1 24
```

## Caveats

- Spans are relative to `/persist/gosrc`, a byte copy of
  `Sources/golang_src` at commit 9f1012d9 (plus an added
  `VERSION` file, which is not a Go source file). Line numbers are
  therefore valid against the vendored tree as-is.
- Counts are for THIS run of THIS probe — the evidence class of log 072
  §5a: singleton proven per input, not a bound over all inputs.
- The linker, assembler and stdlib compiles are NOT in the profile by
  construction; only the probe's own package compile is.

## Lane scripts

`lanes/cg_cov_l1.sh` (recon + failed approach 1), `l2` (make.bash +
first instrumented build), `l3` (probe replay, exposed the 4-block
main-package-only problem), `l4` (`-coverpkg`, mode `set`),
`l5` (`-covermode=count` — the delivered run). Archived in Airlock at
`agent/drop/.done/20260824T21*__cg_cov_l*.sh`.

## Disk

`/persist`: gosrc 316M + gocache 687M + compile_cov 40M ≈ 1.05 GB
(157 GB free before, 156 GB after). `/work` peak consumption 10 MB of
the 4 GB cap.
