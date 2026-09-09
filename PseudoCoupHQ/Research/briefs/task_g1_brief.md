# Task g1 — `find_emulation` for go and swift, primitive-first: the same handful on four compiled targets

Law: `LAW.md` beside this file, ALL of it including the tower section.
Then `task_h1_brief.md` and `task_h2_brief.md` beside it (the handful, its
driver, its results: `DevComms/log_238`, `log_240`), the arch_unit_oracle
CORE's "goal" and "Ruling, 2026-09-08" sections, `log_226` (task o11: how a
second-language renderer was built on top of the c one — `rust_render.py`'s
`RustRenderer(E.Renderer)` is the pattern, and its §3.1 is how the target's
own compiler behaviour was MEASURED rather than assumed), and
`Research/oracle/arch_opcodes/single_opcode_units.json` (per language, the
operators whose whole body is one opcode: the PRIMITIVE lookup). Instance
`g1.conf` (copy from `Airlock/instances/g1.conf`, bring it
up). Artifact folder: `Research/oracle/cross_construction/emulation/`, new
sub-folders `go/` and `swift/`, the driver extended in `handful/`; lanes
under `handful/lanes_g1/`.

## 1. What this is, and the one design decision it carries out
the owner's model of an opcode (CORE "goal", 2026-09-08): a PRIMITIVE plus its
EDGE REGIONS. `find_emulation(cell, lang)` therefore tries, in order:
1. **primitive-first**: does `lang` have an operator whose whole lowered
   body IS this cell? The lookup is `single_opcode_units.json` for `lang`:
   a narrow row whose `body_text`, chaff-stripped, is one instruction that
   classifies (m1b's `classify_line`/`key_width`) to the cell's (mnem,
   shape, key_width). Its members' canon `meta` give the operator and the
   operand types (`lhs_type`, `rhs_type`, `expression`). Render THAT: the
   operator on holders of those types, nothing else. The edge regions are
   then whatever the compiler puts around it (a guard, a trap), and the
   gate says whether the body equals the cell on all inputs or only on a
   region: record which, with the counterexample if `sat`.
2. **term rendering** as the fallback, exactly h2's route, when no
   primitive row exists for `lang`.
h2's `idiv` result is the case for this: rendered from the term it became
76 instructions and the gate could not answer; go's `/` on `int32` IS
`idiv` with a guard, and the primitive route renders `a / b`.

## 2. The two renderers
`go_render.py` → `GoRenderer(E.Renderer)`, `swift_render.py` →
`SwiftRenderer(E.Renderer)`, each in its own sub-folder, each following
`rust_render.py`'s shape: one spelling per z3 operator kind over the
target's fixed-width holders (go: `int8..int64`, `uint8..uint64`,
`float32/64`; swift: `Int8..Int64`, `UInt8..UInt64`, `Float`, `Double`),
with the target's WRAPPING forms where the plain operator traps or is
undefined (go: `+ - *` wrap, `<<`/`>>` are defined for any count so the
cell's mask must be spelled; swift: `&+ &- &* &<< &>>`; division: both
trap on zero, which is the edge region, NOT something to hide — render
`/` and let the gate report the region). Before writing a spelling,
MEASURE the target as o11 §3.1 did: a probe source per operator, compiled
at ship flags, the body pasted; the spelling table cites its probe.
Ship flags are the corpus's own: go `go build` (lane_gen.py line 323ff,
package main with the function exported by name), swift `swiftc -O`
(line 333ff), `swiftc` at `/persist/swift/usr/bin/swiftc`. The carve is
lane_gen's / o8's, unchanged; go's calling convention (registers `rax rbx
rcx …`, per the go rows of the model table's attestation) is stated with
the object that shows it.

## 3. Deliverable
The handful's ten cells × {c, rust, go, swift}, primitive-first on all
four (c and rust too: state per cell whether the primitive route or the
term route ran, and for c/rust compare with h2's verdict). One table, 40
rows: cell | lang | route (primitive / term) | rendered (GLOSS, LITERAL in
the section) | landed | composition | gate verdict (with region + counter-
example when `sat`) | cause if refused. Then by cause, what did not work.
Per-target spelling tables with their probes. Guard over every json; log
(next free number, check right before writing); verifier lane; PROGRESS on
the autopoly node; sync-back; instance down.

**swift may not run yet.** `/persist/swift/usr/bin/swiftc` fails to load
`libncurses.so.6` in the current image; a rebuilt image with `libncurses6`
is being pushed to the tower by the coordinator. Do go FIRST, then probe
swiftc (`swiftc --version` in a lane); if it still fails, every swift row
is REFUSED with that literal error, the swift renderer is written and
probed as far as compile-free checks allow, and the log says so. Do not
work around it (no LD_LIBRARY_PATH tricks, no copying libraries).

Memory bound 4g inside the cap. Stop rules per LAW; a target behaviour
you cannot measure is a flag, not a guess. Reply with the 40-row table,
the by-cause list, the spelling tables' row counts, the tally, the two
lists.
