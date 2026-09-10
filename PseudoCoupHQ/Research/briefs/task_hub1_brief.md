# Task hub1 — Hub v1, first form: the dictionary read off the polyfill-complete set, and one typed go file lowered as source composition of proved emulations, gated against go's own output

Law: `PseudoCoupHQ/Research/LAW.md`, ALL of it. Node:
`Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/`
— read its CORE's "definition" (source composition, ruled 2026-09-07)
and the four sub-nodes' CORE definitions (front_end, dictionary, joiner,
oracle_test) — this task is steps 4 and 5 of the master order
(`CORE_0_3_research.md` §4.2). Then the AutoPoly loop's table
(`.../emulation/autopoly/autopoly4.md` and the fifth pass ap5 left, its
`across_targets.on_all_four_list` and every run's rendered source under
`autopoly/src*/`), `DevComms/log_246`, and the go front-end artifacts
(`Research/oracle/compiler_units/go_types_oracle.go`, `go_types_join.py`,
log_216: go/types as the type oracle, 77% of sites typed at 541 MB per
package). Instance `hub1.conf` (copy from `Airlock/instances/hub1.conf`;
mounts `sandbox-persist` read-only). Artifact folder:
`Research/oracle/hub/`; lanes under `lanes_hub1/`.

## 1. What the objects are, in relation
- The **dictionary** (sub-node dictionary): for each cell the loop proved
  on a target, that target's proved emulation SOURCE — the function the
  renderer printed and the compiler landed and the gate proved. The loop
  already holds every entry; this task writes them out as one lookup:
  key (target, mnem, shape, key_width) → the emulation source, its route
  (primitive / primitive+setup / term), its verdict, the ledger rows it
  covers. The key is machine form; a source operator token never keys
  anything (the LAW's ban). The go SIDE of the lookup — from a go
  operator node with its operand types to the cell go lowers it to — is
  `single_opcode_units.json`'s go rows plus the model table's attestation
  of go units (which cells go's compiler produces for `+` on `int32`,
  `>>` on `uint64`, …), read from the corpus, never guessed.
- The **front end** (sub-node front_end): tree-sitter-go parses the
  file; go/types (the oracle already built in o6) types each operator
  node's operands; each typed node resolves to the go cell (mnem, shape,
  key_width) the corpus attests for that operator at those holders.
- **Source composition** (the CORE's ruled egress): the target file is
  the tree walked post-order, each operator node replaced by a CALL of
  its cell's emulation function (the dictionary entry, emitted once per
  cell as a static inline function in the target), operands passed as
  the target's holders of the cell's widths; the target's own compiler
  then lowers and optimises across the calls.
- The **oracle test** (sub-node oracle_test): body A = go's own build of
  the file, carved per function; body B = the target's build of the
  composed file, carved per function; the gate over A and B as over two
  units. PROVED / DISPROVED with counterexample / UNDECIDED, per function.

## 2. The handful first
One go file, written for this task and kept under `hub/handful/`: eight
explicitly typed functions, each one or two operators, covering `+ - *`
on `int32` and `int64`, `>>` and `<<` on `uint64` with a count, `/` on
`int32`, `float64 + *`, one comparison feeding a select
(`if a != b { return c } return d`), and one two-operator expression
(`(a + b) * c`). Targets: c and rust (then go itself as the identity
check: composing go from go must round-trip to a proved-equal body).
For each function: the tree with its typed nodes (LITERAL), the cells
resolved, the composed target source (LITERAL), both carved bodies, the
gate's verdict. A node whose cell has no proved entry on a target is a
result by cause (the dictionary's hole), never a hand-written fallback.

## 3. Then the measure
Over the corpus's OWN go units (the `go/op_*` and `go/regen_*` sources
the pipeline generated, which are one-operator functions): how many can
the dictionary compose to c and to rust, and of those how many the gate
proves against go's own body — counts and ledger-row shares. That is Hub
v1's first oracle number.

## 4. Deliverable
`hub/dictionary.json` (+ `.md`: entries per target, holes per target by
cause), `hub/hub.py` (front end + resolve + compose), `hub/handful/` (the
file, the composed sources, the bodies), `hub/oracle_test.md` (§2 and §3
tables); guard over every json; log (next free number, check right
before writing); verifier lane; PROGRESS on the hub_compiler node and
its four sub-nodes (append, dated); sync-back; instance down. Memory
bound 6g (go/types per package ran at 541 MB), sample first, peak RSS,
abort `ABORT_MEMORY_HUB1`. No shared-file change is authorised; the
renderers and the loop's driver are READ. Never delete anything under
`<runs>/` or `Airlock/`. Reply with the handful's
eight-function table, the §3 counts, the dictionary's entry and hole
counts per target, the tally, the two lists.
