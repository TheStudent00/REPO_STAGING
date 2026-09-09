# tree_sitter (T1) — a ledgerer component

One place owning grammars and parsing for every language PCv6
touches. Nothing else constructs a parser. Plan node:
`Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_tree_sitter.md`
(a component of the ledgerer, id `pcv6.ledgerer`).

- `parse_source.py` — parser factory over pinned grammar packages;
  refuses unknown grammars; bytes in, Tree out, no decode guesses.
- `record_coverage.py` — deterministic node-kind census (named vs
  anonymous) + TOTAL partition into handled / justified-baseline /
  leftover, where leftover IS the worklist; double-claimed kinds
  refused.
- `pins/MANIFEST.md` — exact grammar versions; changing them is a
  grammar change (manifest + frozen censuses update together).
- `fixtures/` — pinned sample sources per grammar + frozen census
  expectations (`expected_<lang>.json`).
- `test_tree_sitter_base.py` — the acceptance test (this tool's
  oracle): frozen-census byte-equality, determinism, clean-parse,
  partition totality/refusal. 12/12 passing at graduation
  (2026-07-28, sandbox).

Run acceptance:

```bash
python3 -m pytest PseudoCoup_v6/Tools/ledgerer/tree_sitter/ -q
```

Registered grammars: python, rust, cpp. Adding one = register in
`parse_source.GRAMMARS`, pin in the manifest, add fixture + frozen
census — one commit.
