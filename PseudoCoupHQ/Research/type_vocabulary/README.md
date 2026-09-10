# type_vocabulary — artifacts

Created 2026-08-14 with the node
(`Planning/node_0_3_research/node_0_3_3_type_vocabulary/`). Step A ran
2026-08-16: the 12 compilers' type enumerations were extracted and
unioned. Report: `../../DevComms/log_022_type_vocabulary_union.md`.

- `raw/<language>.types.json` — each language's own enumeration,
  verbatim names, with the source it came from and how authoritative
  that source is (compiler-enum / runtime-enumerated / doc-sourced /
  sdk-source-enumerated).
- `union.py` — the union program. Every normalization decision is a
  visible entry in its `ENTRIES` table, and it checks on every run
  that each present-cell's cited raw spelling really appears in that
  language's raw file. Run:
  `python3 PRIVATE/PseudoCoupHQ/Research/type_vocabulary/union.py`
- `type_union.json` — the union, 59 entries, per-language marker plus
  the raw spelling behind each marker.
- `type_union.md` — the same table in pipe form.

Step B (the owner rules which entries become instruments) has not run. Until
it does, nothing here changes the six verified instruments.

Consumers: `../dominant_intentions/` (census pages for each adopted
instrument, and the harness that verifies them),
`../kind_fuzz_clustering/` (every instrument widens the reachable
slice of each compiler's lowering vocabulary).
