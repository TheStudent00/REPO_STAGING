---
id: pcv6.application.rust_llvm.isel_gap
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_3_1 — The Instruction-Selection Gap

Between the front half's output (an LLVM IR opcode / ISD node) and
the encoder's input (a machine instruction) sits LLVM's
instruction selector: a 1,145-line hand-written bytecode VM
(`SelectCodeCommon`) plus a ~375k-line generated `MatcherTable[]`
byte array, plus 210 hand-matched C++ cases in
`X86ISelDAGToDAG.cpp::Select()`. Measured in PCv5; the survey said
the generated matcher is NOT transpilable by the 1:1-function
strategy.

## The three options (priced in PCv5, DECIDED HERE only after the
front half lands — do not pre-commit)

| option | what it is | cost |
|---|---|---|
| a. hand-map | declare the few opcodes the hub actually emits (integer arithmetic is a handful) as a small table; stub the rest with asserted reachability | cheap, honest, cuttable — fits the imprecise-but-safe default |
| b. transpile the VM | slice `SelectCodeCommon` and carry `MatcherTable[]` as data | full solution, expensive; the table-as-data is the hard part |
| c. llvmlite oracle | use llvmlite as a reference oracle rather than extracting the selector | avoids extraction; introduces a runtime dependency |

## The deciding evidence (gathered by doing the front half first)

How many distinct ISD nodes does the hub actually exercise? The
front half's output set answers it. If it is a handful (expected
for integer arithmetic), option (a) is obviously right and the
expensive options wait for a real need. This is the churn-
resilience principle applied: build the cheap safe version, widen
only where an intention demands.

## Acceptance (option-independent)

The selected machine instruction for each hub-emitted ISD node
matches what `llc` produces for that node (host ground truth), by
whichever option is chosen.

## Open (the owner)

- The option choice itself, after the front half's ISD-node count
  is known.
