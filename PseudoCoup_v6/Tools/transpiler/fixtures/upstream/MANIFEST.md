# Vendored upstream compiler source — LLVM encoder

One file, 66 KB. **Not this project's code.**

| file | upstream project | upstream path |
|---|---|---|
| `X86MCCodeEmitter.cpp` | llvm/llvm-project | `llvm/lib/Target/X86/MCTargetDesc/X86MCCodeEmitter.cpp` |

sha256 at vendoring, 2026-07-31: `9322e2dd4bc19764...`

This is the same file as the copy in
`PRIVATE/PseudoCoup_v6/Tools/ledgerer/fixtures/upstream/`, and
the duplication is deliberate: the standing rule is that a tool's
oracle assets live beside the tool they check, so each suite is
self-contained and neither breaks if the other is moved. 66 KB is a
cheap price for that.

## Why it is here

Until 2026-07-31 it was read out of `PRIVATE/PseudoCoup_v5`
through a `PCV5_ROOT` environment variable, which made this suite
unable to run without another repo on disk. That was a dependency on
a past project rather than a transplant from one. It is now a
transplant: PCv5 can be deleted and this suite still passes.

It was never PCv5's work. PCv5 had merely fetched it.

## Provenance: KNOWN

Recovered 2026-07-31 from PCv5 before its source trees were removed.
PCv5 held llvm-project as a git submodule, and the gitlink pinned it
at commit

    2078da43e25a4623cab2d0d60decddf709aaea28

So this file is
`llvm/lib/Target/X86/MCTargetDesc/X86MCCodeEmitter.cpp` at that commit
of llvm/llvm-project, and can be re-fetched exactly. PCv5's
`.gitmodules` was empty, so the SHA was recorded and the URL was not —
the SHA is the part that matters, since llvm-project is the only place
it resolves.

This is the good case. The three Rust files vendored under
`PRIVATE/PseudoCoup_v6/Tools/ledgerer/fixtures/upstream/` are
the bad one: they came from a `git clone --depth 1` with nothing
pinned, so their revision is unrecoverable. See that manifest.

## Rules

- Do not edit. Upstream text.
- Replacing it is a re-vendoring: record the new checksum and source.
