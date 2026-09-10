# data_representation — artifacts

Created 2026-08-15 with the node
(`Planning/node_0_3_research/node_0_3_4_data_representation/`).
Raw reference from the superseded union extraction:
`../type_vocabulary/raw/` — a candidate checklist only, never a
decision instrument.

## layer 1 — the data

- `data_layer1.json` — the shared synthetic source, values and edge
  values and identity-marked shapes. Its `__spec__` states the
  conventions: `#special` for NaN/infinity/-0.0, `#int` for whole
  numbers past double exactness, `#anchor`/`#ref` for identity marks.

## layer 2 — the representations, and the audit (2026-08-17, log_023)

- `representations_<language>.json`, twelve files — per layer-1 form,
  the shapes that language can hold that form in, each with its
  spelling (literal or constructor), a one-line note, and the source
  snippets the audit runs. 328 (form, representation) cells.
- `audit_generate.py` — bakes the layer-1 values into one tiny program
  per cell, which builds the representation and prints the content
  back as `FACT_ID|RESULT`. Writes one sandbox lane script per
  language into `audit/lanes/`. Probes never parse the data file at
  run time.
- `audit_classify.py` — reads the lane output and rules on every cell:
  LOADS / PARTIAL (with the refused edge named) / REFUSES-behavioral,
  and REFUSES-gap decided across a whole form. Writes
  `audit/audit_<language>.json`.
- `audit/raw/` — the lane output as it was printed, plus the
  compilers' own words for every refusal (`l2_errors*.txt`).

Result: 211 cells LOAD, 66 PARTIAL, 18 REFUSES-behavioral, 33 NOT-RUN
(all c#, no toolchain reachable). No REFUSES-gap: layer 1 stands
audited. Full account in
`PRIVATE/PseudoCoupHQ/DevComms/log_023_layer2_representations.md`.

**2026-08-17 postscript 1:** php's three extension-gated cells (GMP,
BCMath, mbstring codepoints) moved REFUSES-behavioral -> LOADS after
`php8.5-gmp`/`php8.5-bcmath`/`php8.5-mbstring` were installed and
`l2_php.sh` was re-run. Totals after: 214 LOADS, 66 PARTIAL, 15
REFUSES-behavioral, 33 NOT-RUN (still all c# — the sandbox proxy still
refused dot.net; `proxy/allowlist.txt` was extended and awaited an
`allow.sh sync`). Coverage remained eleven of twelve languages.

**2026-08-17 postscript 2:** after the owner's `allow.sh sync`, dot.net
answered (no more `000`); the .NET SDK installed to `/persist/dotnet`
(one tar-ownership quirk on unused workload manifests, core SDK intact);
`dotnet run`'s NuGet restore was avoided by compiling directly with the
SDK's own Roslyn `csc.dll` against the installed reference-assembly pack
via two persisted helper scripts. c#'s 33 cells ran: 20 LOADS, 11
PARTIAL, 2 REFUSES-behavioral, 0 NOT-RUN. **Current totals: 234 LOADS,
77 PARTIAL, 17 REFUSES-behavioral, 0 NOT-RUN (328 cells, 12 of 12
languages).** No REFUSES-gap in any language; layer 1 stands audited,
complete. Full account in the log's second postscript section.
