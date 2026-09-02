# kind_fuzz_clustering — artifacts

Created 2026-08-14 with the node
(`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/`).

Phase 0 filled it on 2026-08-15 — measurement only, nothing executed:

- `extract_kinds.py` -> `kinds_<language>.json`: named kinds,
  supertypes, hidden kinds, anonymous tokens, per target language.
- `legal_pairs.py` -> `legal_pairs_<language>.json`: every
  (host kind, slot role, filler kind) triple the grammar declares
  legal, plus the expansion map for the grammar's abstract groupings.
- `probe_space.py` -> `probe_space.json`: the probe space and its size
  (3,556 probes over the 11 targets under the base rule), the depth
  structure, and the kinds no dominant input can reach.

Read the numbers in
`../../DevComms/log_021_fuzz_phase0_probe_space.md`.

Phases 1 and 2 filled it on 2026-08-17 — python only, the loop proved end
to end:

- `probe_design.md`: the generation rules, written BEFORE generation, with
  eleven numbered judgment calls for the owner to overturn.
- `probe_generate.py` -> `probes_python.json`: 20,024 probes over 62 kinds
  (100 signatures under R2), operands taken from the layer-2 cells that
  loaded — 26 cells, 117 values, base and edge alike, baked as literals.
- `lane_build.py` -> `lanes/l3_python.sh`: the self-contained lane; the
  runner cannot see this repo, so the payload travels inside the script.
- `raw/l3_python.txt`: 20,024 lines of `PROBE_ID|RESULT`, one lane run,
  64.5 s. `raw/l3_python.lane.log`: the run's own log.
- `signatures.py` -> `behavior_python.json` + `behavior_python.md`: the
  first behavior signatures — per kind or menu token, the map
  (form, representation, value class) -> answer, with the domain accepted.

Read the numbers in
`../../DevComms/log_024_layer3_python_fuzz.md`.

Reuse, do not rebuild: the harness skeleton at
`../dominant_intentions/harness/` (vectors -> runners -> lane ->
compare) — generated probes replace hand-written vectors.
Instruments: `../dominant_intentions/verified/`.
Grammar data + legal pairs: `../kind_signature_clustering/raw_all/`.
