# Vendored upstream compiler source — ledgerer corpus

Four files, 192 KB. **Not this project's code.** Upstream rustc and
LLVM source, copied in so this repo's suite runs on its own.

| file | upstream project | upstream path |
|---|---|---|
| `declare.rs` | rust-lang/rust | `compiler/rustc_codegen_llvm/src/declare.rs` |
| `va_arg.rs` | rust-lang/rust | `compiler/rustc_codegen_llvm/src/va_arg.rs` |
| `rvalue.rs` | rust-lang/rust | `compiler/rustc_codegen_ssa/src/mir/rvalue.rs` |
| `X86MCCodeEmitter.cpp` | llvm/llvm-project | `llvm/lib/Target/X86/MCTargetDesc/X86MCCodeEmitter.cpp` |

Checksums at vendoring, 2026-07-31:

| file | sha256 (first 16) |
|---|---|
| `declare.rs` | `ec3f4bebea7a16af` |
| `va_arg.rs` | `708cc97f84d4ead4` |
| `rvalue.rs` | `4b7b7d2b3919e185` |
| `X86MCCodeEmitter.cpp` | `9322e2dd4bc19764` |

## Why they are here

Until 2026-07-31 these were read out of `PRIVATE/PseudoCoup_v5`
through a `PCV5_ROOT` environment variable. That made this repo's
suite unable to pass without another repo on disk — six tests failing
with `FileNotFoundError` if PCv5 was absent.

By the transplant-versus-dependency test recorded in
`PRIVATE/PseudoCoup_v6/AgentMemory/02_decisions.md` — *after the
harvest, could the source repo be deleted without anything breaking?*
— that was a dependency, which is not allowed. It is now a transplant:
PCv5 can be deleted and this suite still passes. Verified the day of
the move, 95 passed with no environment variable set.

They were never PCv5's work. PCv5 had merely fetched them.

## Provenance: known for the LLVM file, unknown for the Rust ones

Recovered 2026-07-31 by inspecting PCv5 before its source trees were
removed. The two halves differ and the difference matters.

**`X86MCCodeEmitter.cpp` — revision KNOWN.** PCv5 held llvm-project as
a git submodule, and the gitlink pinned it at commit

    2078da43e25a4623cab2d0d60decddf709aaea28

so this file is `llvm/lib/Target/X86/MCTargetDesc/X86MCCodeEmitter.cpp`
at that commit of llvm/llvm-project, and can be re-fetched exactly.
(PCv5's `.gitmodules` was empty, so the SHA was recorded but the URL
was not — the SHA is what matters, since llvm-project is the only
place it resolves.)

**The three `.rs` files — revision UNKNOWN.** PCv5 fetched them with
`git clone --depth 1` in `Research/rust_routing/fetch_sources.sh`,
with no tag, branch or commit pinned. A shallow clone of whatever
`master` was on the day. There is no record of the day, so there is no
way to name the revision.

That is a gap rather than a disaster: these are a ledger corpus,
exercising uniqueness, recount equality, round-trip and refusal, and
the acceptance does not depend on which rustc release the text came
from. But a future test claiming agreement with a NAMED rustc version
cannot be built on these three files. It needs a fresh fetch with the
revision recorded at the time.

The checksums above therefore pin what we have, which for the Rust
files is all the identity they have.

## Rules

- Do not edit these files. They are upstream text.
- Replacing one is a re-vendoring: record the new checksum here and
  say where it came from.
