# transpiler (T3) — ingress framework increment

The generalized four-stage ingress pipeline. Plan node:
`PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_1_transpiler/`
(id `pcv6.tools.t3_transpiler`).

- `ur_ast.py` — the Universal Rich AST node vocabulary
  (transplanted from `PseudoCoup/pseudocoup/core/ur_ast.py`;
  UI-specific nodes deliberately not carried yet). Every built node
  records its ledger id in `metadata["ledger_id"]`.
- `ingest_source.py` — the framework: parse (T1) → census GATE
  (leftover kinds refuse ingestion, `GateFailure`) → UR-AST build
  via the ingestor's node table → ledger population (T2) with
  resolved types replacing `unresolvable`. UR nodes and ledger
  records get their ids from ONE walk — id equality by
  construction, never two id maths.
- The **ingestor contract** (`Ingestor`): a grammar name, a node
  table, a justified baseline, an optional type resolver — and
  nothing else. Parsers, keys, and ledger writes are framework-
  owned (the historical bare-name violation is structurally
  impossible).
- `test_transpiler.py` — acceptance per the settled framework
  node: all four stages on a toy python-grammar fixture; UR nodes
  carry ids that exist in the ledger; resolved types replace
  markers; ledger checks green post-ingest; the gate REFUSES an
  unknown kind; determinism. 6/6 at graduation (2026-07-28), and
  the full three-tool stack 25/25 in one run.

Run acceptance:

```bash
python3 -m pytest PseudoCoup_v6/Tools/transpiler/ -q
```

A Rust ingestor increment was built here pointing at a retired
reference backend instead of the settled LLVM/rustc-LLVM direction;
it was removed as mis-aimed (2026-07-30). The forward direction for
Rust ingestion is LLVM/rustc-LLVM.
