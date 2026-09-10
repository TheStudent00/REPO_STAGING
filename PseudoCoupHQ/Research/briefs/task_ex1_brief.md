# Task ex1 — expanding beyond the four: cpp as a fifth compiled target, and the check for the interpreted languages, each on the handful first

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it. Then
`task_ap4_brief.md` beside this file and its log (ap4 runs BEFORE this
task and changes the driver; read what it left), `task_g1_brief.md` (how
a target is added: a renderer subclass, spellings MEASURED by probes at
ship flags, the ship flags from `Research/op_pipeline/lane_gen.py`'s own
branch for the language), the research CORE's §4.2 and the
`node_0_3_1_12_remaining_languages` node (which languages the corpus holds
and how each was compiled or run: `lane_gen.py`, and the interpreter
work in `Research/op_pipeline/interp103_*`, log_222). Instance `ex1.conf`
(copy from `PUBLIC/Airlock/instances/ex1.conf`; mounts
`sandbox-persist` read-only — the interpreter anchors live there). Artifact
folder: `.../emulation/`, new sub-folders `cpp/` and `interp/`; results
under `autopoly/` as `expand1_*`; lanes under `handful/lanes_ex1/`.

## 1. What this is (the owner, 2026-09-09: "begin to expand into the other languages")
Two expansions, each a HANDFUL first, per the owner's standing rule, and only
then the loop.

### 1.1 cpp, the fifth compiled target
c's renderer with cpp's holders and ship flags (`lane_gen.py`'s cpp
branch, LITERAL in the log). `cpp_render.py` → `CppRenderer(E.Renderer)`;
probes for anything cpp spells differently from c (it should be nearly
nothing at these holders; measure, do not assume: `static_cast`, the
`<cstdint>` names, `long double`). Then the handful's ten cells on cpp
beside c's verdicts, then the loop's 253 cells on cpp alone (253 runs).
Report cpp's column in the per-target table's shape, and the all-FIVE
count beside the all-four, without redefining the four: the
polyfill-complete set is reported at both widths until the owner says which
counts.

### 1.2 The interpreted languages: what `find_emulation` and its CHECK are there
The corpus holds cpython, php, ruby and java units (and the JIT outputs
under `Research/op_pipeline/jit_out_*` for javascript, dart, csharp:
read `log_222` and the remaining_languages node for what each is). For an
interpreted target there is no carve: the emulation is SOURCE in that
language, and the check must be different. Define it, then run it on the
handful:
- **the emulation**: the cell's mapping rendered in the target's own
  operators over its own value model (python's unbounded int: the mask to
  the cell's width is part of the rendering; php's int is 64-bit; ruby's
  Integer unbounded; java's int/long fixed) — a renderer subclass per
  language, spellings measured by running the interpreter on probes, not
  assumed.
- **the check**: the interpreter is a black box, so the check is the fuzz
  census's method (the pipeline's own `Research/fuzz` line: read its CORE):
  the reference's mapping and the interpreter's answer compared on a
  sampled input set that INCLUDES the cell's edge regions (the shift
  count boundary, the sign boundary, zero and MIN/-1 for division, NaN
  and infinities for floats), with the sample stated and the count of
  points. A disagreement is a `sat`-like result with the point LITERAL.
  Where the language has a JIT whose output the corpus already carves
  (`jit_out_*`), ALSO carve and gate that output the compiled way, and
  report both checks side by side.
- The handful's ten cells × {cpython, php, ruby, java} (+ javascript, dart,
  csharp if their runners are in the image or the persist volume; say
  which are not). One table: cell | target | route | rendered (GLOSS) |
  sample points | agreements / disagreements | the first disagreement
  LITERAL | JIT carve verdict where one exists.

## 2. Deliverable
`expand1.md` with the cpp column and all-five line, the interpreted
handful table, the definition of the interpreted check as it was run
(the sample rule LITERAL), and by cause what did not run. Guard over every
json; log (next free number, check right before writing); verifier lane;
PROGRESS on the autopoly node AND on the remaining_languages node (append
only); sync-back; instance down. Memory bound 6g, sample first, peak RSS,
abort `ABORT_MEMORY_EX1`. Stop rules per LAW; no shared-file changes are
authorised by this brief; a runner that is absent from the image is a
flag (install into Airlock is the coordinator's), not a workaround. Reply
with the cpp column and the all-five/all-four line, the interpreted table,
the sample rule, the tally, the two lists.
