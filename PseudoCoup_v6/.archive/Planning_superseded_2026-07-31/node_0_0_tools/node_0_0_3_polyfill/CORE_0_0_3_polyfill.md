---
id: pcv6.tools.t4_polyfill
level: 2
status: settled
settled_by: the owner
supersedes: null
---

# CORE 0_0_3 — T4: Polyfill

The wrapper layer filling target-behavior gaps so transpiled code
matches source behavior exactly. Governing law (settled, derived
independently twice): **uniform wrapping, no exemptions — every
operator on a polyfilled type routes through the simulator, or
none do.**

- Mechanism is general (the boundary rule + a UR-AST rewriting
  pass, harvest: v4 `polyfill_engine.py` shape); the wrapper SET
  grows per source-grammar need, discovered by T1's census
  (arithmetic-node inventory from the Rust ingestor's census is
  the first requirements list).
- Harvest: PCv5 `u8()`/`u32()` + support layer; v0
  `runtime/numbers.py` (fixed-width at literals); doctrine in
  `PseudoIR/DevComms/compiler_transpilation_experiment.md`.
- Acceptance: differential — wrapped arithmetic vs native
  source-language execution on a pinned grid (the PCv5 pattern
  that caught the urem guard bug within minutes).
- Depends on: T3's node shapes; buildable in parallel once they
  settle.
