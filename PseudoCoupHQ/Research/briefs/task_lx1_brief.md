# Task lx1 — the language axis on RISC-V: swift for riscv64 as an install, measured; and the seven interpreted languages against the RISC-V definitions by agreement at points

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, `log_269` §"the swift riscv64 probe"
(swift 6.0.3 in the image names the target and a runtime path that
does not exist; `swift sdk list` fails on a missing `libxml2.so.2`;
the instance had no network), `log_269` §"the interpreted seven" (the
agreement route on x86: 162–166 of 253 each, `agreed` never proved),
`emulation/interp/interp_check.py` and task ex2's log (the route:
edge values first, ≤20,000 points, seven interpreters in the image),
`construct/general/rv6_sources.py` and `emulations_riscv64/` (the
1,960 rendered RISC-V emulations: the sources the interpreters run
are rendered the same way, by `render_general` into each interpreted
language). Instance `lx1.conf` (copy `t4.conf`: the persist volume
holds swift; `proxy = yes` for the SDK probe, and ONLY for that lane).
Lanes under `Research/oracle/riscv/lanes_lx1/`.

## 1. swift on riscv64, as an install question, measured
- with the network on, LITERAL: does swift.org publish a Swift SDK
  for `riscv64-unknown-linux-gnu` for a 6.x release (`swift sdk
  install <url>` after `libxml2` is present in the instance), or does
  a community toolchain exist (a riscv64 Linux build of the compiler
  itself)? Paste the commands and their outputs. If one installs,
  compile the swift probe of log_269 for riscv64 and carve it; then
  run every RISC-V cell on swift through `rv6_all_langs.py`'s route
  (add `swift` to its targets by the same `inherit_rv3` mechanism)
  and report "of 255" beside the four languages. If nothing installs,
  the row is a FLAG with the outputs, not a guess.

## 2. the interpreted seven against the RISC-V definitions
- population: the 255 RISC-V cells; for each, the emulation rendered
  into cpython, php, ruby, java, javascript, dart, csharp (the same
  general render), run at points beside the definition evaluated at
  the same points; recorded `agreed` / `disagreed` / `refused` /
  `timed out`, never proved.
- report "of 255" per interpreter and on all seven, beside x86's
  162–166 of 253; every disagreement with its point, LITERAL (a
  disagreement is a defect in the render or the definition, named,
  not fixed here).
Guard; log (next free number); verifier; PROGRESS on the riscv64
node; sync-back; instance down. Memory bound 6g, abort
`ABORT_MEMORY_LX1`. One process. Nothing under `Research/op_pipeline/`
touched; `riscv_reference.py` READ (task sl1 is regenerating it
beside you: read the store, not the file, if it changes under you,
and record the sha256 you read).
