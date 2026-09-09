---
id: pcv6.progress
status: living
---

# PROGRESS — node_0

- 2026-08-02: `pcv6` now states its `super_node` — `hq.projects`,
  absolute path, `repo: PseudoCoupHQ` and its remote. It was added
  because HQ's roster began naming this repo in `sub_nodes` while
  bringing PCv5's chain to the 2026-08-02 rules, and PROTOCOL §1 does
  not allow an edge written at one end only.
  - That single field is the whole of this tree's conformance to
    those rules. Its 10 COREs carry no `sub_nodes` and its CHECK
    files no frontmatter id; both arrive when a chain in THIS tree is
    descended into, which is the working order the owner settled the same
    day.
- 2026-07-30: restructure started. CORE_0 holds the owner's structures; one
  node per component, each CORE carrying that component's definition
  and nothing more. Component content is unwritten.
- 2026-07-30: application node retired. it meant "using the tools"
  when written and "the software itself" when read back, so it was
  split into two acts: construction (node_0_3) and api (node_0_4).
  hub promoted to level 1 as the thing the project produces.
  frontmatter ids made flat throughout (identity, not address).
- 2026-07-31: previous plan projected onto this one. 35 old COREs read
  and classified: 25 carried clean, 8 carried with the retired backend
  replaced by llvm, 1 died (seam declarations), 1 unresolved (ledger
  scale). content landed as 26 SUPPORT files (~9,900 words) beside the
  destination COREs rather than inside them, so the COREs stay in
  the owner's register. the old tree at ../Planning is untouched.
- 2026-07-31: this tree promoted from Scratch to Planning. the
  previous Planning tree (35 nodes) moved to
  ~/Programming/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31
  — its content was already projected into SUPPORT files across this
  tree and PseudoIR's. seven references from Tools/ and Research/
  repointed at the nodes that now hold that material.
- 2026-07-31: the code caught up with the plan, inside this repo.
  Tools/ledger -> Tools/ledgerer; Tools/tree_sitter_base ->
  Tools/ledgerer/tree_sitter (a component, per the ledgerer CORE);
  Tools/slicer -> Tools/insert (it holds only insertion code — the
  selection and extraction halves went in the purge). Application/
  archived with the node it was named for. 128 tests green before and
  after.
- 2026-07-31: insert/ and intentions/ moved to
  ~/Programming/PseudoIR/Tools/. An earlier entry recorded this as NOT
  done and pending a ruling on cross-repo imports; the move and the
  mechanism both landed and the entry was stale. The mechanism is the
  environment variable `PSEUDOCOUP_ROOT` (default
  ~/Programming/PseudoCoup_v6), read by
  ~/Programming/PseudoIR/Tools/insert/cross_border.py and
  ~/Programming/PseudoIR/Tools/intentions/validate_form.py, each
  refusing with a named error when the directory is absent — recorded
  in ~/Programming/PseudoIR/Tools/README.md and Agent_Memory.md §7. No
  ruling on cross-repo imports is recorded in either repo; if one was
  wanted, the code went ahead of it.
- 2026-07-31 (verified in review, not from a recorded count): the 128
  split 95 here and 33 in PseudoIR, so the move lost nothing.
  `PCV5_ROOT=~/Programming/PseudoCoup_v5 python3 -m pytest Tools -q`
  in ~/Programming/PseudoCoup_v6 gives 95 passed;
  `PSEUDOCOUP_ROOT=~/Programming/PseudoCoup_v6 python3 -m pytest Tools
  -q` in ~/Programming/PseudoIR gives 33 passed.
