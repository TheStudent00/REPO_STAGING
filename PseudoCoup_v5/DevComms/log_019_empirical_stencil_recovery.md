# log 019 — research: recovering stencils empirically from rustc's pretty-printer

2026-08-12, at the owner's instruction ("im certainly interested in seeing
the outcome of the research project"). The question, from the
compiler-fallback discussion: rustc's arrangement knowledge is
procedural (parsing code in `rustc_parse`, printing code in
`rustc_ast_pretty`), never a readable table — so can the arrangements
be recovered EMPIRICALLY, by having rustc print a construct back to
source and observing the tokens?

## 1. The verdict

**Yes. The method works, mechanically and automatably.** Feed rustc a
minimal program with unique placeholder identifiers in every slot,
pretty-print it back, substitute the placeholders with slot names —
everything left literal IS the stencil, recovered from the compiler's
own understanding rather than from any grammar.

## 2. The instrument

- rustc 1.75, extracted from the Ubuntu .deb into the sandbox with no
  root (`dpkg -x`; `LD_LIBRARY_PATH` to its bundled
  `librustc_driver`). The rustup channel is blocked by the sandbox
  network allowlist (403), and apt has no newer rustc on jammy.
- the pretty-printer is `-Zunpretty=normal`; on a stable rustc that
  `-Z` flag unlocks with `RUSTC_BOOTSTRAP=1`. `-Zunpretty=ast-tree`
  prints rustc's own node structure for the same source.

## 3. The evidence — five recovered stencils

Placeholders in, stencils out, verbatim from the run:

> `struct S { aaa: BBB }`
> → `struct <_> { <name>: <type>, }`
>
> `fn fff(ggg: III) -> JJJ { kkk }`
> → `fn <name>(<param.pattern>: <param.type>) -> <return_type> { <body> }`
>
> `let x = &raw const AAA;`
> → `let x = &raw const <value>;`
>
> `match aaa { BBB if ccc => ddd, _ => eee }`
> → `match <value> { <pattern> if <guard> => <arm.value>, _ => <fallback>, }`
>
> `let g = move |aaa: BBB| ccc;`
> → `let g = move |<param>: <param.type>| <body>;`

Note what came through: not only the fixed tokens (`:`, `->`, `=>`)
but the VARIANT tokens too — `&raw const`, `move`, the `if` guard.
The recovery captures exactly the information our variant field
stores.

## 4. Three findings beyond the yes

- **rustc normalizes on the way out.** The one-line struct came back
  multi-line with a trailing comma added. rustc's printer has its own
  canonical formatting — structurally the same move as our faithful
  convergence, which corroborates that design choice: the compiler
  team ALSO chose "canonical form out" over "bytes preserved."
- **the instrument is itself pinned.** Our 1.75 refused `safe fn`
  (stabilized 1.82): `error: expected one of '!' or '::'`. So
  compiler-as-authority carries a version pin exactly as the grammar
  does — the fallback does not escape pinning, it doubles it. the owner's
  host rustc (1.96.1, per the toolchain notes) would parse it; the
  sandbox cannot demonstrate that.
- **rustc's vocabulary is confirmed third.** `ast-tree` for
  `pub struct S { aaa: BBB }` names `Struct`, `Path`, `Public` —
  neither tree-sitter's `struct_item`/`visibility_modifier` nor
  `ur`'s. Any rustc-sourced structure imported into `ur` pays a
  second mapping vocabulary, as flagged in the fallback discussion.

## 5. Standing rulings this feeds (the owner, 2026-08-12)

- ordering: **bump the pin first, compiler fallback second** — "after
  the research, we will go with your lean."
- the fallback's shape when built: refuse by name, warn that a naive
  mapping exists, proceed only on explicit user acceptance; such
  nodes may enter the ledger with honest substrate and unresolved
  `ur_kind`, ingress without egress.
- `check_pin` gains the staleness check beside it (the differential
  alphabet of log_018, now extended by the keyword comparison —
  which found the `safe` gap this log's instrument then confirmed
  from the other side).

## 6. Reproduction

Sandbox setup (each bash call is fresh; re-export the path):

    cd /sessions/*/  &&  export LD_LIBRARY_PATH=$PWD/rustc-local/usr/lib/x86_64-linux-gnu
    RUSTC_BOOTSTRAP=1 rustc-local/usr/bin/rustc -Zunpretty=normal <file.rs>

VERIFIED on the owner's own infrastructure the same day, via the
SandboxDesign agent lane (script
`SandboxDesign/agent/drop/stencil_probe_196.sh`, log
`20260812T055925Z` in `SandboxDesign/agent/logs/`): rustc 1.96.1
parses `unsafe extern "C" { safe fn f(); }` and pretty-prints it
back cleanly — the construct the pinned grammar refuses (§4) and the
Cowork sandbox's 1.75 refused too. The full chain is demonstrated:
grammar gap detected (log_018 keyword check) → construct confirmed
unparseable by the pin → structure recoverable from the current
compiler.
