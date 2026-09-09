---
id: hq.research.kind_signature_clustering.progress
status: living
---

# PROGRESS — kind_signature_clustering

- 2026-08-12: node founded (graduated from the research CORE's topic
  bullet). Plan-of-record steps 1–4 all ran the same day — see the
  super-node's PROGRESS for the per-step record and the reports
  (PCHQ DevComms logs 008–015).
- 2026-08-12: basis-report proposals P1–P9 ALL RULED by the owner (walk in
  `~/Programming/PseudoCoupHQ/DevComms/log_016_ingress_egress_asymmetry.md`
  §6 and the conversation following): vocabulary additions adopted
  (`import`, `try`, `pair`, `interpolation`, `container-form`),
  Python-naming rule, two-layer classification, shape-invisibility
  standing fact, split mapping strategy. carried into
  `~/Programming/PseudoCoup_v5/Tools/ledgerer/ur.py` (KINDS) and the
  ur CORE the same day.
- 2026-08-13: P-a BUILT and run on rust —
  `~/Programming/PseudoCoupHQ/Research/kind_signature_clustering/pack_generator.py`
  (language-agnostic; anchors from basis_xref + ruled additions,
  seven-slice threshold band, four-part dilution guard, counterpart
  and labeled name-only channels, mechanical confidence). Output:
  `proposed_kind_map_rust.{json,md}` — 106/163 proposed (22 strong /
  54 moderate / 30 weak), 57 residue; diffed against the hand draft
  (`compare_rust_hand.py`). Report: PCv5
  `log_021_rust_kind_map_proposal.md` (it is the q1 instrument, so it
  lands PCv5-side). Pending the owner's review. Known re-pins before
  language two: import anchor is include-flavored; interpolation has
  no admissible anchor at t=0.40.
- next: the owner reviews log_021 §3/§5 (q1 ratification); then P-b
  (versioned shared basis) and language two (c/cpp suggested).
- 2026-08-14: RENAMED `kind_clustering` -> `kind_signature_clustering`
  (the owner: both lines are clustering; this one clusters kinds by their
  DECLARED SIGNATURE — arity, slot types, supertypes — while the new
  co-node `kind_fuzz_clustering` clusters the same kinds by MEASURED
  BEHAVIOR). Folder, CORE and CHECK filenames renamed with it.
  FRAMEWORK TENSION worth flagging to PlanPlan: §3 says "renames and
  moves keep the id, so ontology change stays traceable", but
  `check_plans.py` enforces `node-self-name` (the id's last segment
  must equal the folder/name). The id therefore had to change too —
  formerly `hq.research.kind_clustering` (with `.progress`/`.check`
  sub-ids). One of the two rules should give; the owner's call.
  Artifacts stayed under the historical `kind_clustering` folder name
  (directly under `Research/`) so the ten DevComms logs and the
  scripts' internal paths kept resolving — also the owner's to re-rule if he
  wants them moved. (Superseded 2026-08-15 — see the bullet below: he
  did.)
- 2026-08-15: ARTIFACT DIRECTORY RENAMED to match — the `Research/`
  folder `kind_clustering` became `kind_signature_clustering`,
  finishing the 2026-08-14 refactor above. Done with PlanPlan's new
  `~/Programming/PlanPlan/framework/rename_node.py` (JOB 1 of the same
  piece of work that did this rename: `python3 rename_node.py
  <planning_root> kind_clustering kind_signature_clustering --apply
  --also-artifacts <old research dir>=<new research dir>
  --scan-root ~/Programming/PseudoCoupHQ --scan-root
  ~/Programming/PseudoCoup_v5`). The tool found the node already at its
  new name (2026-08-14's manual rename), so it did the node-level steps
  as a no-op and ran only its reference sweep + the artifact rename:
  25 files edited across PseudoCoupHQ and PseudoCoup_v5 (DevComms logs
  008–016, the planning tree, `.gitignore`, the co-node
  `kind_fuzz_clustering/README.md`, and the six scripts/logs inside the
  artifact directory that hardcoded their own old path), plus the
  directory move itself. A repo-wide grep for the old `Research/`
  path (`kind_clustering` immediately under it) returns nothing
  afterward, excluding `.git`'s own index. `hq.sh check` still 0
  errors.

