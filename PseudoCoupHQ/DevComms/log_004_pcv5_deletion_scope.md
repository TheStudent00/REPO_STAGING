# log 004 — the PCv5 deletion: measurement, then execution

2026-07-31. the owner: "the content exists in the VCS. if we dont need that
previous version content, delete it." Then, after the measurement
below showed the premise was false for the biggest part: "worst case i
have it in Timeshift. if its not being tracked by git and especially
if its source from other repos. delete it."

**Done. `~/Programming/PseudoCoup_v5/` went from 550 MB to 55 MB.**
Sections 1 to 5 are the measurement made first, kept because it is
what decided the scope. Section 7 is what was actually done, including
a mistake and its fix.

---

## 1. The finding: 430 MB of it is NOT in the VCS

`~/Programming/PseudoCoup_v5/` is 550 MB on disk. Its `.git` is 54 MB.
The gap is vendored upstream compiler source that git never tracked.

| path | on disk | files tracked by git |
|---|---|---|
| `Research/rust_routing/sources` | 315 MB | **0** |
| `Research/llvm_trace/sources` | 115 MB | 3 |

`Research/rust_routing/.gitignore` contains the line `sources/`, so
that exclusion was deliberate. Deleting those folders is **not
recoverable from version control**.

## 2. It is also load-bearing today

Those exact paths are what PseudoCoup_v6's suite reads through
`PCV5_ROOT`. Live references in PCv6's own tool code:

- `Research/rust_routing/sources/rust/compiler/rustc_codegen_llvm/src`
- `Research/rust_routing/sources/rust/compiler/rustc_codegen_ssa/src/`
- `Research/llvm_trace/sources/llvm-project/llvm/lib/`
- `Research/llvm_trace/sources/llvm-project/llvm/lib/Target/X86/`

Delete them and 95 tests stop passing, with no `git checkout` to undo
it.

**They are also not "previous version content".** They are third-party
upstream source — rustc and llvm-project — that happens to sit under
PCv5's tree. By the transplant-versus-dependency test recorded in
`~/Programming/PseudoCoup_v6/AgentMemory/02_decisions.md`, PCv6
depending on them is the dependency case and is already queued to fix
by vendoring them into PCv6.

There are fetch scripts — `Research/rust_routing/fetch_sources.sh` and
`Research/llvm_trace/fetch_llvm.sh` — so the sources are
reconstructible from upstream in principle. Whether they reproduce the
same revisions was NOT checked; the scripts have not been read or run.
Treat "we can just re-fetch" as unverified.

## 3. What IS tracked, and therefore safe to delete

All of these are recoverable with `git checkout`.

| path | on disk | files tracked | live references |
|---|---|---|---|
| `Designing` | 204 KB | 9 | none found |
| `Research/vocab_transpiler` | 67 MB | 92 | R3's `run_checks.sh` only |
| `Research/basis_audit` | 404 KB | 44 | none found |
| `Research/cpp_ingress` | 140 KB | 4 | referenced by live PCv6 code |
| `Research/divergence_suite` | 36 KB | 8 | referenced by live PCv6 code |
| `Research/int64_js` | 16 KB | 2 | none found |
| `Research/interp_insertion` | 40 KB | 7 | none found |

Note the size column is misleading for `vocab_transpiler`: 92 tracked
files, but 67 MB on disk, most of it in `differential/` — so a large
part of that folder is generated output that is also untracked.
Unverified how much.

## 4. The harvest problem

Two of these folders are NAMED SOURCES in the harvest map for the
rebuild PCv5 is about to undergo. From
`~/Programming/PseudoCoup_v6/AgentMemory/03_lineage_and_harvest.md`:

> Compiler-source ingress, oracle-checked | PCv5
> `Research/{vocab_transpiler,cpp_ingress}`

Deleting a named harvest source before the harvest runs is the
opposite of the intended order. The recorded lesson from the last
purge is on exactly this shape of mistake: roughly 1,900 lines of
direction-neutral machinery were deleted to remove 16 lines that named
a retired backend, because the scope was accepted without being
measured.

## 5. Proposed scope

Four groups, in the order they can safely be acted on.

- **Delete now, unreferenced and tracked** — `Designing/`,
  `Research/basis_audit`, `Research/int64_js`,
  `Research/interp_insertion`. About 664 KB. Nothing live points at
  them; git holds all of it.
- **Delete after the harvest, not before** — `Research/vocab_transpiler`,
  `Research/cpp_ingress`. Named in the harvest map as the
  compiler-source-ingress holder. Tracked, so deletable at any time —
  the argument is sequencing, not safety.
- **Do not delete until PCv6 stops needing it** —
  `Research/divergence_suite`, plus the two `sources/` trees. The
  sources additionally are not in git at all.
- **Keep** — `DevComms/`. It holds the two 2026-07-27 surveys, which
  are the line-cited evidence behind every harvest claim, and this
  version's own planning tree references them.

## 6. What was wanted from the owner — answered same day

He gave the go-ahead with a wider scope than proposed: Timeshift is
the backstop, untracked content goes, especially other repos' source,
and anything important enough to keep moves to an archive OUTSIDE the
project folder rather than inside it.

---

## 7. What was actually done

### The enabling step: vendor first, then delete

Rather than archive 430 MB, the four files anything actually READ were
copied into the repos that read them. That turned a dependency into a
transplant and made the deletion safe.

| vendored to | files | size |
|---|---|---|
| `PseudoCoup_v6/Tools/ledgerer/fixtures/upstream/` | `declare.rs`, `va_arg.rs`, `rvalue.rs`, `X86MCCodeEmitter.cpp` | 192 KB |
| `PseudoCoup_v6/Tools/transpiler/fixtures/upstream/` | `X86MCCodeEmitter.cpp` | 66 KB |
| `PseudoIR/Tools/intentions/fixtures/upstream/` | `pc_verdicts.json` | 32 KB |

Each has a `MANIFEST.md` recording what it is, where it came from, its
checksum, and why it moved. `PCV5_ROOT` is gone from every test.

**A provenance win found on the way out.** PCv5 held llvm-project as a
git submodule, and the gitlink pinned commit
`2078da43e25a4623cab2d0d60decddf709aaea28`. So the LLVM file's exact
upstream revision is known and recorded. The three Rust files are the
opposite case: `Research/rust_routing/fetch_sources.sh` used
`git clone --depth 1` with nothing pinned, so their revision is
unrecoverable. Both facts are in the manifests, because a future test
claiming agreement with a named rustc version cannot be built on those
three files.

### Removed

- `Research/rust_routing/sources` — 315 MB, untracked, upstream rustc.
- `Research/llvm_trace/sources` — 115 MB, upstream LLVM, including
  36 MB of tracked generated `.inc` tables and a submodule.
- `Research/vocab_transpiler/differential/harness` — 64 MB of
  committed Rust build artifacts.
- `Designing/`, `Research/basis_audit`, `Research/int64_js`,
  `Research/interp_insertion` — tracked, recoverable from git.

### Kept

About 1.5 MB under `Research/`: `cpp_ingress`, `divergence_suite`,
`vocab_transpiler`'s python, `rust_routing`'s slice scripts. Named in
the harvest map as sources for the rebuild this version is undergoing,
and small. Deleting after the harvest stays open. `DevComms/` kept —
it holds the two surveys.

### THE MISTAKE

`Designing/` was deleted after checking that PseudoCoup_v6 did not
read it. **PseudoIR was not checked, and 10 of its tests broke
immediately** — `test_intentions.py` read
`Designing/pc_verdicts.json` through the same `PCV5_ROOT` pattern.

Restored from git, vendored properly, deleted again. All 135 tests
across the three repos now pass with PCv5 gutted and no environment
variable set anywhere.

The lesson is not "check more carefully". It is that **the dependency
existed in two repos and only one was on the list**, because the list
came from the PCv6 investigation that first found the problem. When a
class of defect is found in one place, the search for it has to be run
everywhere before acting on the finding, not after.

It was caught by a test, not by review — which is the argument for
tests as the thing progress is read off, and the same argument the
per-node CHECK policy rests on.

### Fallout the checker caught

Deleting `Designing/` left three prose references dangling, in PCv5's
own research CORE and twice in PseudoIR's intentions support file.
`check_plans.py` named all three by cause. Fixed: one rewritten to
describe what the gutting removed, two marked `(historical)`.
