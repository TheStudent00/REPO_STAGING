# log 018 — handoff plan: the next couple of days (the owner + Opus 5)

2026-08-13, written by the departing session at the owner's request: usage
for this model is nearly spent; this plan lets research continue
with Opus 5 until it refreshes. Everything here is self-contained —
a fresh session holding ONLY this file plus the pointers it names
can execute the work.

## 0. read these first, in this order

1. `PseudoCoupHQ/AgentMemory.md` — the 12 languages,
   the vision, standing rulings, where things are. Load-bearing.
2. `DevComms/LLM_communication_protocol.md` — the owner's
   communication protocol. Non-negotiable. The sections added this
   week: §9b (cold words re-enter with one line), §11a (every claim
   names its level), §18b (walkthrough before numbers). The
   vocabulary ban (§1: never parent/child/sibling/ancestor —
   super-node/sub-node/co-node) applies to EVERYTHING including
   code comments and delegated-agent output.
3. The two research nodes' PROGRESS files:
   `PseudoCoupHQ/Planning/node_0_3_research/node_0_3_0_kind_clustering/PROGRESS.md`
   and `.../node_0_3_1_dominant_intentions/PROGRESS.md`.

## 1. where everything stands (the walkthrough)

Two research lines ran this week, both in PCHQ's research node,
both feeding PseudoCoup's `ur`/ledger design:

- **kind_clustering** (shape layer): all four plan-of-record steps
  DONE. 411 grammars measured; the similarity spectrum over 31,212
  kinds built; the basis report cross-referenced the clusters
  against the intentions vocabulary; the owner ruled all nine proposals
  (vocabulary additions `import`/`try`/`pair`/`interpolation`/
  `container-form` now live in PCv5 `Tools/ledgerer/ur.py` KINDS).
  The pack generator (P-a) produced the machine-proposed rust
  ts_kind→ur_kind map: 106/163 with evidence, 57-row residue —
  AWAITING DEE'S REVIEW (PCv5 `DevComms/log_021_rust_kind_map_proposal.md`).
- **dominant_intentions** (behavior layer): phase 0 inventory done;
  the basis data-structure lists ruled (level 0 machine, level 1
  engine); the SEED-TIER CENSUS IS COMPLETE — six objects (boolean,
  float, integer, string, list, dict) across five pages in
  `PseudoCoupHQ/Research/dominant_intentions/`,
  every fact UNVERIFIED by design, ZERO contradictions found.
  Standing rules accumulated on the pages: the guarantees rule,
  record-both modes, origin naming (`.java_equals`), staged
  mutability, least-modes. Phase 1 (the harness) has its complete
  work order: verify the census by execution.
- **PCv5 ledgerer** (the code line this all serves): ur.py,
  ledger.py, ts_to_ur.py written and green (17/17,
  `Tools/ledgerer/test_ts_to_ur.py`). Blocked on q1 (the rust map
  review, above). The macro cluster (q3) and pack file layout (q6)
  are the remaining design opens; both can wait.

## 2. work packages, in recommended order

### WP1 — container toolchain installs (small, unblocks WP2)

The SandboxDesign container (see the toolchain skill §0–1a; the
engine/instance policy is NEW this week — read it) runs 8 of the
11 target languages. Install the missing three plus finish swift:

- typescript: `npm install -g typescript` inside a lane script —
  trivial, npm already allowlisted.
- kotlin: standalone kotlinc zip to `/persist` (JDK present).
- dart: dart SDK tarball to `/persist`.
- swift (bonus, not one of the 11 actives): the 748MB tarball is
  already at `/persist/swift` but its binaries need `libncurses6`
  — a lane script running `apt-get install -y libncurses6` (the
  container runs root; ubuntu archives are allowlisted) then
  re-running the hello-world completes it. Prior attempts:
  `SandboxDesign/agent/drop/swift_probe*.sh`, logs in
  `agent/logs/`.
- afterwards update the toolchain skill's §3 image list (it
  already drifted: ruby/php are present but unlisted). Skill
  updates go through the skill-save mechanism, not file edits.

### WP2 — phase 1: the verification harness (the big build)

Purpose: execute every fact in the five census pages across the
installed languages; emit the VERIFIED guarantee table. Design
constraints already settled — do not re-open them:

- fresh build; the old PseudoIR registry/probers are
  existence-proof only, never consulted (the owner's ruling).
- a census fact becomes a VECTOR: {object, fact id (e.g. F-i2),
  per-language snippet, expected result PER CAMP}. Fractures have
  per-language expectations; universals have one.
- per-language runner templates: a snippet wrapped in a main,
  printing results in one shared convention (one value per line,
  tagged; raises/panics caught and printed as `<raise:NAME>`),
  so cross-language diffing is mechanical.
- execution through the SandboxDesign agent lane (serial; batch
  all languages' runs for one object into one lane script to
  respect seriality; products to `/out`, the session copies them
  into the tree).
- results land as data in
  `Research/dominant_intentions/verified/` + a DevComms log per
  the report discipline (§18b: walkthrough first).
- SUCCESS = every census fact either CONFIRMED (with output as
  evidence) or REFUTED (a finding — census page gets corrected
  with provenance). Mode-dependent facts (rust debug/release)
  run BOTH modes per the record-both ruling.
- suggested first run: boolean + float only (the calibration
  pair — expected near-all-confirm), review with the owner, then the
  heavy pages.

### WP3 — PCv5 q1 ratification (the owner's session, Opus assists)

Walk `PseudoCoup_v5/DevComms/log_021_rust_kind_map_proposal.md`
with the owner: confirm the 22 strong, skim the 54 moderate, rule the 33
disagreements (each has a drafted comment), stamp the 57 residue
rows (most have a labeled name-evidence default). Output: the
ratified rust kind map as pack DATA for `ts_to_ur` (its file
layout is q6 — park the layout question; a plain
`kind_map_rust.json` next to ts_to_ur.py is fine for now, marked
provisional). This unblocks running the mapper over the corpus.

### WP4 — kind_clustering P-b (versioned basis artifact; medium)

Package the spectrum + counterparts + archetypes as ONE versioned
data artifact language packs can consume (a manifest naming the
source grammar commits, the feature version (v2), the scripts'
git state; consumers get "basis version X"). No new analysis —
packaging + provenance. CHECK file already lists it.

### WP5 — census extension (only if time is spare)

Machine-readable form of the five census pages
(`census.json`: object / fact / owner / camps / per-language
guarantee) — WP2 needs an ad-hoc version of this anyway; doing it
properly serves both. New OBJECT pages (function-as-value, record)
only if the owner opens them — do not run ahead of his depth.

## 3. decision points RESERVED FOR DEE (do not decide these)

- all q1 rulings (WP3 is his session).
- any new census object beyond the seed six.
- the pack file layout (q6) and macro cluster (q3) design.
- any vocabulary/naming addition (Python-naming for buckets,
  origin-naming for variants are RULED conventions — applying
  them is fine; inventing outside them is not).
- PCv6/PseudoIR remain DEFERRED (standing ruling).
- egress router (P-c) stays parked until builder/egress planning.

## 4. working-style notes for Opus (the failure modes this week)

- work only at the depth the owner has opened; flag, don't decide.
- delegated-agent reports leak jargon: instruct agents to open
  with a plain-words walkthrough and reintroduce every cold term;
  filter their returns before the owner sees them.
- no old-project artifacts in dominant_intentions work — lessons
  carry, artifacts do not.
- SandboxDesign is an ENGINE (toolchain skill §0): instance state
  in gitignored paths only; the numpy criterion gates any tracked
  edit.
- the census's register: hand-written pages, the owner's language,
  worked examples beside every general claim. Keep it.
- when a bash mount path is needed: glob it
  (`M=$(ls -d /sessions/*/mnt)`) — the session name changes.
- checks: `bash PseudoCoupHQ/hq.sh check` should
  stay at 0 errors; PCv5 `python3 Tools/ledgerer/test_ts_to_ur.py`
  should stay 17/17 (needs `pip install tree-sitter==0.26.0
  tree-sitter-rust==0.24.2 --break-system-packages` per fresh
  sandbox).

## 5. suggested day plan

Day 1: WP1 (an hour, mostly waiting on downloads) → WP2 harness
skeleton + the boolean/float calibration run → review with the owner.
Day 2: WP2 full census verification → corrections into the pages
→ WP3 if the owner has review energy, else WP4.
Whatever remains: WP5, and the census.json.
