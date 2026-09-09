---
id: pcv6.polyfill.support.polyfill
status: projected
---

# SUPPORT — polyfill

projected 2026-07-30 from the previous plan, now archived at
`~/Programming/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_3_polyfill/CORE_0_0_3_polyfill.md  (134 words)
verdict: clean
changed: nothing

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
