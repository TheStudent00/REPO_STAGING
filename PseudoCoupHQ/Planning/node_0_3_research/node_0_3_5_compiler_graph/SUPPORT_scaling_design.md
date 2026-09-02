---
id: hq.research.compiler_graph.support.scaling_design
level: 3
status: draft
settled_by: the owner
designation: rule
node:
    name: compiler_graph
    path: Planning/node_0_3_research/node_0_3_5_compiler_graph/CORE_0_3_5_compiler_graph.md
---

# SUPPORT — scaling_design

Brainstormed with the owner 2026-08-26, banked at his request. Status:
design, not ruled except where marked. The pilot (c, cpp, go, rust,
swift; scalar core; ship+anchor; 51 dom_ops covering 142/142
measured operator-nodes) proved the method; this file is the road
for the other eight languages and the deferred operator buckets.

## the milestone accounting (2026-08-26)

- 28 multi-language dom_ops (119 operator-nodes) + 23 singleton
  dom_ops = 51 dominant operators, 142/142 measured nodes covered.
- Singleton reading RULED (the owner): an unattached operator IS a
  dom_op with one member; accumulation licenses a union of one.
- Three singletons are provisional (go ==/!=/! stranded by the
  mirror-candidate gap; C's comparisons are satellites by bridge).
- Scope of the claim: five of thirteen languages, scalar type
  core, ~19 binary + unaries, one architecture, one ship level.
  Theory done, recipe frozen, coverage is labor.

## deferred operator buckets (from the probe-generator scoping,
approved with the "binary first, second pass later" plan)

- compound assignment (`a += b`): a binary core PLUS a store back
  into the operand. Deferred then because stores in units needed
  machinery; the canonical form and store-to-field dataflow now
  exist, so this is owed work, not blocked work. Expectation:
  cores land in existing dom_ops with the store as an appendage.
- structural operators (call, index, member, cast): not scalar
  computations; need their own probe shape. A later chapter.

## the two remaining execution models

### JIT languages (java, kotlin, csharp, typescript-on-v8)

- The arch-unit EXISTS — at run time. Official dump switches:
  JVM `-XX:+PrintAssembly` (needs hsdis), .NET `DOTNET_JitDisasm`,
  V8 `--print-opt-code`.
- The JIT specializes on observed types. Not a bug for us: the
  type-pair key becomes the WARM-UP RECIPE — warm the probe with
  (i32,i32) calls and the dump is the (i32,i32) arch-unit.
- Deoptimization guards are MODES with a new response kind:
  `deopt-continue-elsewhere` (bail to the interpreter). core+modes
  absorbs this with one vocabulary entry.
- the owner's resource instinct (unconfirmed): JVM likely the heavier
  lift (hsdis plugin build, warm-up ceremony). Ordered second.

### interpreted languages (python, ruby, php) — ORDERED FIRST (the owner)

- The operator never becomes its own machine code. What executes
  is the INTERPRETER'S OWN HANDLER — a C function inside CPython,
  compiled once, shared by every program.
- Therefore: the arch-unit for python `+` is a SLICE OF THE
  INTERPRETER BINARY (the handler), and WHICH handler a probe
  reaches is a path question — exactly the map+diary+tally
  instrument already built for Go's compiler, pointed at CPython:
  build the interpreter with coverage/diary, run the probe, watch
  which handler ran, in what order. The interpreter plays the
  compiler's role; the toolkit transfers unchanged (C source,
  tree-sitter-c, objdump, the id-emission diary).
- Honest expectation: python's `+` (arbitrary precision, digit
  loop) byte-matches nobody. It joins the table through BRIDGES
  and DOMINANCE (its value projected onto fixed width agrees;
  overflow-to-growth is its mode — the interval-probe name
  `growing` finally applies), or through ratified intention.
- Cheap extra middle form: each interpreter's BYTECODE is a small
  closed vocabulary (python `dis`): `a + b` is one BINARY_OP
  instruction — a normalized layer between source and handler,
  nearly free to extract and useful as the dispatch anchor.

## next practical lap (RULED by the owner, 2026-08-26)

CPython first: the handler slice via the coverage/diary
instrument. JVM warm-up pilot second (resource instinct, may be
wrong — record what it actually costs when tried).
