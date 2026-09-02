---
id: pir.rust_llvm_slice.progress
status: blocked
---

# PROGRESS — rust llvm — slice

- 2026-07-31: node created; holds the rust and llvm specifics for this stage.
- 2026-07-31: status -> blocked. stage 2 (IRMapping) has no answer,
  so the chain cannot close; stages 1 and 3 are not blocked, and
  stage 1 produces the count that decides stage 2. also removed a
  claim I had repeated from the previous plan — that the matcher
  table is "not transpilable by the 1:1-function strategy" — which
  does not describe this project's transpiler at all.
