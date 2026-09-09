# log 017 — ts_to_ur: the six open questions

2026-08-06, recording the chat response at the owner's request ("please
expand on the open questions" / "add comments to you response in
DevComms"). A working record per protocol §18a — nothing here
settles anything. This is the opening inventory for the `ts_to_ur`
deep-dive, in weight order, each question stating what is already
settled around it and what remains the owner's to rule.

Context: `ur.py` and `ledger.py` are complete and exercised
(`PseudoCoup_v5/Tools/ledgerer/`). The unbuilt trio is
`ts_to_ur`, `ur_to_ledger`, `builder` — and `ts_to_ur` is where the
plan is thinnest.

---

## 1. the rust map itself

the mapper's heart is the ts_kind -> ur_kind table for rust: 163
rows. `PseudoCoup_v5/DevComms/log_008_kinds_coarse_tagging_draft.md`
drafted it, and the owner's later rulings — coupled (log_015), the three
constructs (log_014), the three form buckets incl. `proof-form` —
resolved the five uncertain families. **but nobody has applied
those rulings back to the 163 rows.** one ratification pass turns
the draft into the mapper's data.

- settled nearby: the map is DATA (a table the census checks for
  totality against the grammar), thin code executing it — the
  log_002 §8.2 lean, never formally ruled.
- remaining: the ratification pass; the formal data-not-code ruling.

## 2. anonymous nodes — the sleeper

ids count anonymous tokens (`{`, `,`, `->`) — constitutive, from
idgen. but does each become a `ur.Node`? the corpus numbers make
this real: **544k total nodes, 304k named — ~240k anonymous, 44% of
everything** (log_007). materialize them all and the UR tree nearly
doubles for tokens carrying no intention; skip them and child
POSITIONS must still count them or every id breaks.

- middle paths exist (count positions, materialize named only, keep
  anon info recoverable from spans), each with a cost.
- this decision shapes the mapper's inner loop more than any other.
- remaining: entirely open; the first real conversation of the
  deep-dive.

## 3. macros at mapping time — the biggest cluster

the owner's sequencing (log_005 §2) says step 1 delivers "kinds one and
two EXPANDED." so the mapper (or a co-writer beside it) must do four
things whose boundaries are undrawn:

- mark each `token_tree` opaque — RULED (the opacity form, node's
  CORE).
- re-parse contents under the per-macro shape table —
  `PseudoCoup_v5/DevComms/log_010_token_tree_reparse_coverage.md`:
  20 shapes -> 82.98% measured coverage; a seventh
  "match-arm-pattern" shape would close most of the residue (44% of
  failures were `matches!`-style pattern+guard). table UNRATIFIED.
- run the kind-one engine
  (`PseudoCoup_v5/Research/macro_engine.py`, pulled
  into ledgerer scope by log_005 §2) producing `GeneratedOrigin`
  sub-trees. WHERE it sits relative to the mapper is undrawn.
- mint sub-addressed ids for injected nodes — ruled yes in
  principle (node CORE, 2026-08-06); the CONCRETE SPELLING of the
  sub-address is unpicked. log_010's offset finding applies: the
  arithmetic remap works, `included_ranges` alone does not.

## 4. the error files

5 of 111 corpus files carry ERROR nodes (nightly `decl_macro`
syntax the stable grammar rejects — log_007, log_002 §5.0c). three
recorded options, none ruled:

- refuse those files honestly;
- admit them with ERROR stretches as opaque nodes (refusal posture
  applied to form — consistent with everything else);
- patch the grammar — log_002 called this the cheap fix BECAUSE the
  pin is already ours.

this decides whether `TryFromU32`'s definition file is ingestible.

## 5. pinning and census — one ratification

everything designed, nothing ratified: `ts_to_ur` as owner of the
vendored pinned grammars; the runtime pin check
(`Language.semantic_version` against the manifest); the census
discipline — unknown kind at ingest -> refuse, or a WFL-style
justified baseline. one yes makes it plan (the `tree_sitter_base`
design, projected at
`PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_tree_sitter.md`).

## 6. what a language pack IS

the per-language sub-module's shape, concretely: presumably
{pinned grammar, the kind map, the query files, the macro shape
table, the census baseline} — all data — plus nothing per-language
in code. saying so explicitly is what keeps language two cheap.
falls out of 1, 3, and 5 once they are ruled.

---

## reading of the order

2 and 3 are the real design conversations (they shape the code);
1 and 5 are ratifications of work already done; 4 is one ruling;
6 falls out of the others. proposed next step, the owner's choice: a
log_002-style brainstorm document for this node opening with the
anonymous-node numbers and the macro pipeline, or a one-at-a-time
walk in chat as done for the ledger.
