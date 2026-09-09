# Grammar Pins — provenance manifest

Grammars arrive as pip packages, pinned here by exact version.
Regenerating the frozen censuses with different versions is a
GRAMMAR CHANGE and must update this manifest and the frozen files
in the same commit.

| grammar | pip package | version | verified against frozen census |
|---|---|---|---|
| python | tree-sitter-python | 0.25.0 | 2026-07-28, 12/12 acceptance |
| rust | tree-sitter-rust | 0.24.2 | 2026-07-28, 12/12 acceptance |
| cpp | tree-sitter-cpp | 0.23.4 | 2026-07-28, 12/12 acceptance |

Runtime: tree-sitter (python bindings) 0.26.0.

Install line (per-session sandbox provisioning, or host):

```bash
pip install --break-system-packages tree-sitter==0.26.0 tree-sitter-python==0.25.0 tree-sitter-rust==0.24.2 tree-sitter-cpp==0.23.4
```

Note on the vendoring pattern. The settled plan node
(`~/Programming/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_tree_sitter.md`)
named a pattern from an earlier research repo: in
`~/Programming/PseudoIR/v2/grammars/` there is one folder per
language (12 of them), each holding that grammar's `grammar.json`
and `node-types.json` copied out of the upstream grammar repo, with
the exact upstream commit recorded in a `provenance.json` — so the
grammar inventory is diffable and can never drift silently. This
manifest achieves the same churn guard a lighter way: pip packages
pinned to exact versions, with the frozen census fixtures as the
drift detector. Full-source vendoring in the PseudoIR-v2 style can
be added per grammar if a pin ever proves insufficient — recorded
as a deviation for the owner's awareness, flagged in conversation
2026-07-28.
