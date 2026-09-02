---
id: hq.research.data_representation.progress
status: living
---

# PROGRESS — data_representation

- 2026-08-15: node founded (the owner: "probably a new node"), superseding
  `type_vocabulary` after the owner's three-layer clarification pulled the
  research back into focus: data (static content, no dynamics) /
  representation (how a language holds it) / operation (what the
  compiler can do to it — the measured dynamics). Layer 1 RULED the
  same day: the seven content forms + nesting + identity marks,
  complete-for-content by the serialization argument, behavior
  excluded to layer 3, completeness audited against layer 2. The
  type_vocabulary union (log_022) demoted to raw reference; its
  59-row ruling cancelled.
- next: layer 2 step 1 — the shared data FILE (values + edge values
  + identity-marked shapes), then the per-language representation
  enumeration and the load-audit.
- 2026-08-15: layer-2 step 1 DONE — the shared data file written by
  hand: `<WORKSPACE_DIR>/PseudoCoupHQ/Research/data_representation/data_layer1.json`
  (parses clean; ~87 leaf values across the seven forms + identity
  shapes). Conventions documented in its `__spec__`: `#special` for
  NaN/inf/-0.0 (JSON cannot hold them), `#int` for beyond-double
  whole numbers (so no parser silently rounds), `#anchor`/`#ref`
  identity marks (shared node, diamond, cycle). Edge values carry
  provenance: they ARE the census fracture lists — nothing
  invented. The file is read by the harness GENERATOR (python),
  which bakes values into generated source per language — probes
  never parse it at runtime, so no per-language parser dependency.
- next: step 2 — the per-language representation enumeration (12
  languages: which language shapes can hold each layer-1 form),
  with the superseded union extraction as raw reference; then the
  load-audit.
- 2026-08-17: layer-2 steps 2 and 3 DONE, reported in
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_023_layer2_representations.md`.
  ENUMERATION: 328 (form, representation) cells across the 12
  languages, one file per language
  (`Research/data_representation/representations_<language>.json`),
  each cell carrying its spelling (literal or constructor) and a
  one-line note; sequence is the most crowded form at 60 cells,
  truth the emptiest at 13. AUDIT: the load-question made real —
  `audit_generate.py` bakes the layer-1 values into per-cell
  programs that construct the representation and print the content
  back in the census harness's `FACT_ID|RESULT` convention, run as
  one sandbox lane per language; `audit_classify.py` rules on every
  cell. 1,324 probes ran: 211 cells LOAD, 66 PARTIAL (base values
  held, a named edge refused), 18 REFUSES-behavioral, 33 NOT-RUN
  (all c# — no toolchain reachable through the sandbox's package
  proxy). LAYER-1 VERDICT: no REFUSES-gap anywhere; every form is
  held by at least one representation in every language that ran, so
  layer 1 stands audited and does not grow. IDENTITY (new measured
  ground): of the 34 identity cells that ran, 23 hold a shared node
  and 24 hold a cycle; the split is owning holders (answer `copied`)
  against referring holders (answer `shared`), identically in every
  language; rust's `Rc<T>` is the one holder of sharing WITHOUT
  editing, a cycle costs strictly more than sharing (only
  `Rc<RefCell<T>>` holds one), and php's array is the only measured
  holder that takes a cycle while refusing a shared node.
- next: step 4 — hand-off to `kind_fuzz_clustering`. Its layer-3
  input space is the 211 LOADS cells, or 277 counting the PARTIAL
  ones with their refused edge excluded per cell; c#'s 33 cells are
  generated and waiting on a toolchain.
- 2026-08-17: gap-closing follow-up (postscript to log_023). php's
  three extension-gated cells (GMP, BCMath, mbstring codepoints) went
  REFUSES-behavioral -> LOADS after `php8.5-gmp`/`php8.5-bcmath`/
  `php8.5-mbstring` were installed in the sandbox and `l2_php.sh` was
  re-run; whole-audit totals now 214 LOADS / 66 PARTIAL / 15
  REFUSES-behavioral / 33 NOT-RUN (328 cells). c# stayed blocked: a
  probe confirmed `dot.net` and its CDN hosts still refused after
  the owner's prior `allow.sh sync`, so `proxy/allowlist.txt` gained a
  `.NET SDK` block (`.dot.net`, `.microsoft.com`, `.azureedge.net`,
  `.dotnetcli.blob.core.windows.net`, and two more) and the owner needs to
  run `bash <WORKSPACE_DIR>/SandboxDesign/allow.sh sync` again before
  the 33 c# cells can be attempted. Coverage is still eleven of twelve
  languages; the §5 layer-1 verdict is unchanged and does not yet
  cover twelve of twelve.
- 2026-08-17: c#'s gap closed (second postscript to log_023), after
  the owner re-ran `allow.sh sync`. dot.net answered (`301`/`302`/`400`, no
  more `000`); the .NET SDK installed to `/persist/dotnet` (a
  tar-ownership quirk hit unused workload manifests only, same shape
  as the earlier php apt quirk — worth folding into `SandboxDesign`
  generally). `dotnet run`'s implicit NuGet restore hits
  `api.nuget.org`, off the allowlist and unneeded for BCL-only probes,
  so it was bypassed: two persisted helper scripts
  (`/persist/dotnet-csc-build.sh`, `/persist/dotnet-csc-run.sh`)
  compile directly with the SDK's own Roslyn `csc.dll` against the
  installed reference-assembly pack, no network. `audit_generate.py`'s
  `RECIPE`/`PRESENCE` for csharp were pointed at these scripts and
  `l2_csharp.sh` was regenerated (inheriting the three prior harness
  defect fixes unchanged) and run whole: 33 cells / 150 probes -> 20
  LOADS, 11 PARTIAL, 2 REFUSES-behavioral, 0 NOT-RUN. **Whole-audit
  totals now 234 LOADS / 77 PARTIAL / 17 REFUSES-behavioral / 0
  NOT-RUN (328 cells) — coverage is twelve of twelve languages.** No
  REFUSES-gap found anywhere (c#'s `form_verdicts` all `held`); the §5
  layer-1 verdict is now complete rather than bounded: layer 1 stands
  audited across every language, not just eleven of twelve.
- next: step 4 — hand-off to `kind_fuzz_clustering` is now unblocked on
  all twelve languages; its layer-3 input space is 234 LOADS cells, or
  311 counting the 77 PARTIAL ones with their refused edge excluded
  per cell.

