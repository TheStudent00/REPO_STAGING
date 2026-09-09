---
id: hq.research.dominant_intentions.progress
status: living
---

# PROGRESS — dominant_intentions

- 2026-08-13: node founded (the owner: "yes second research sub_node...
  something like that would do" re the name). Definition of record,
  standing shape, and the slow-walk plan in the CORE. Swift excluded
  pending the container install attempt (allowlist entries staged;
  probe blocked until host-side `allow.sh sync`).
- 2026-08-13: phase 0 inventory DONE (log_017). Registry: 10 ops / 2
  xforms, all vectors and columns filled, 93/120 runtime-confirmed;
  prober code entirely absent (design survives in schema.md only —
  the v2/ working tree is gone); container executes 8/11 languages
  (typescript, kotlin, dart absent; csharp deliberately so).
- 2026-08-13: old-project artifacts DEMOTED to existence-proof-only
  (the owner's ruling) — this node builds fresh; the phase-0 registry
  findings are evidence of feasibility, never inputs.
- 2026-08-13: basis lists drafted
  (`SUPPORT_BRAINSTORM_basis_data_structures.md`); calibration
  census drafted, then REFACTORED to the owner format ruled by the owner
  (every fact files under structure / operation / border; border
  facts billed to the other party):
  `PseudoCoupHQ/Research/dominant_intentions/census_boolean_float.md`
  (draft 2). Post-refactor: bool featureless as the seed order
  assumed (its apparent fractures were `choice`'s and the truth()
  conversion's, misfiled); float has ONE genuine operation
  fracture (division by zero); the border ledger pre-writes
  vectors for choice, truth(), equality, printing, ordering.
- 2026-08-13: integer and string census pages drafted and ruled
  through (`census_integer.md`, `census_string.md`). Standing rules
  accumulated on the pages: the GUARANTEES rule (Hub models every
  guarantee as a distinct operation/mode; ingress reads which one
  statically; transpiler makes guarantees explicit, never guesses);
  record-both for mode-dependent behavior; least-modes = the set of
  existing guarantees; ORIGIN NAMING for variant operations
  (`.java_equals`); mutability STAGED (PCv5 polyfill approximation,
  v6/v7 native via slices; ledger's origin+intent auto-determines
  mode). Pattern three pages in: fractures are almost always
  guarantees; guarantees never contradict; hard residue shrinking.
- 2026-08-13: list and dict pages drafted (`census_list.md`,
  `census_dict.md`); overflow CLOSED (the owner confirmed the two-adds
  reading); cpp UB overflow ruled (explicit handling transpiles;
  unhandled gets safely managed; deliberate UB = manual). Dict
  resolved the php impostor (php array = dominant dict wearing a
  list view — the owner's dict-list instinct materialized) and produced
  the census's first ANTI-guarantee (go's randomized iteration —
  inert under the dominant's order promise, closing the inertness
  loop). **SEED TIER COMPLETE: six objects, zero contradictions.**
  Dominance over the basic tier = one mechanical guarantee table +
  origin-named variants + pay-per-feature representation + the
  staged sharing plan.
- next: phase 1 — the harness, whose work order is now complete:
  verify every census fact by execution across the container's
  languages; the verified table is the basic tier of the basis.
- 2026-08-14: WP1 container toolchain installs DONE. 11/11 target
  languages now run in the sandbox (python3, node, tsc, javac+java,
  go, rustc, ruby, php, kotlinc, g++, all hello-world confirmed),
  plus swift (bonus, hello-world confirmed) — 12 total. typescript
  (`npm install -g typescript`, tsc 7.0.2) and kotlin (kotlinc
  2.3.21 zip from GitHub, unzipped to `/persist/kotlinc`) installed
  clean. swift's libncurses block resolved by symlink
  (`libncursesw.so.6.6` -> `libncurses.so.6`) since no plain
  `libncurses6` apt package exists on the container's <os>
  (only the wide-char `libncursesw6`/`libtinfo6` variants ship) —
  this symlink is NOT persisted across container restarts and must
  be reapplied per-session until folded into the image build.
  dart REMAINS BLOCKED: `storage.googleapis.com` 403s through the
  egress proxy; `.googleapis.com` staged in
  `SandboxDesign/proxy/allowlist.txt` (instance state, gitignored),
  awaiting the owner's `bash SandboxDesign/allow.sh sync`
  before retry. Toolchain skill §3 image list still needs updating
  (ruby/php present-but-unlisted drift, plus this run's additions)
  — deferred to the skill-save mechanism, not done here.
- 2026-08-14: WP2 CALIBRATION RUN DONE (phase 1 first light) —
  harness built fresh under
  `PseudoCoupHQ/Research/dominant_intentions/harness/`
  (vectors → per-language runners → one lane script → compare);
  boolean/float census executed across 13 columns (11 targets +
  rust in BOTH build modes per record-both + swift bonus).
  **CONFIRMED 109 / REFUTED 1 / SKIPPED 20** (csharp deliberate,
  dart pending allowlist sync). The F-f1 fracture verified
  exactly as censused (python/php raise, everyone else inf; go
  refuses the CONSTANT at compile time as censused). The one
  REFUTED cell is instructive, not wrong: typescript's checker
  refuses comparing two bool LITERALS (TS2367 disjoint singleton
  types) while comparing bool VALUES fine — proposed as a new
  border fact (boolean, checker) in the log; census page
  untouched pending the owner. Report:
  `PseudoCoupHQ/DevComms/log_019_calibration_run.md`.
- 2026-08-14: WP2 FULL CENSUS RUN DONE (phase 1 complete) — the
  four heavy pages (integer, string, list, dict) executed across
  14 columns, now including dart in BOTH modes (SDK installed once
  `allow.sh sync` opened `.googleapis.com`; `dart compile js`
  verified working). 41 facts, 79 probe definitions, 715 probe
  results, 70 seconds of machine time. **CONFIRMED 467 / REFUTED 7
  / SKIPPED 100** over 574 cells. All seven refutations are dart
  (six) plus php's string mutability (one); eleven corrections
  PROPOSED for the owner, census pages untouched. Headline: rust debug
  PANICS and rust release WRAPS on the same overflow source, the
  record-both-modes ruling earning itself in one row; go's
  iteration-order anti-guarantee verified as UNSTABLE; cpp's
  insert-on-read confirmed by the map size. Residue still EMPTY
  after six objects. Report:
  `PseudoCoupHQ/DevComms/log_020_full_census_run.md`.
- 2026-08-14: the owner RULED. log_020 §3 corrections 1-11 and log_019
  §3's typescript border fact APPLIED to the census pages
  (`census_integer.md`, `census_string.md`, `census_list.md`,
  `census_dict.md`, `census_boolean_float.md`): camp placements for
  dart's Euclidean modulo, php's dividend-sign modulo and its
  mutable-in-place string, ruby's codepoint camp, java's slice
  WINDOW, php/cpp's slice and assignment COPY camps; compile-time
  refusal adopted as a first-class camp answer; mode annotations
  now apply per-fact not per-language; typescript's bool-literal
  refusal added to boolean's border list. Rust's bare `+` gets the
  name **`unspecified`** (the owner's ruling, provisional on his veto),
  the C standards literature's own term, recorded on
  `census_integer.md`'s standing rules. Follow-up: the dart-web
  overflow gap (log_020 §6 item 3) closed by a small lane script
  (`dartweb_overflow.sh`) reaching the 64-bit max by arithmetic (63
  doublings, never a literal) — result: silent float erosion, no
  throw/wrap/refusal (`maxVal` and `maxVal + 1` both print
  `9223372036854776000`), confirming the census's original
  "behaves as floats" claim for overflow itself; recorded on
  `census_integer.md`'s F-i2 dart-web entry and as a dated
  postscript on `log_020_full_census_run.md`.
- 2026-08-19: **CENSUS FOLD-BACK — the layer-3 campaign's findings
  carried back onto the five reference pages.** The pages were
  hand-drafted 2026-08-13 and marked UNVERIFIED throughout; logs 024
  to 037 then measured them and the pages were never updated. Each
  page now ends with one dated section, `## layer-3 findings, folded
  back 2026-08-19`, carrying only what the runs PROVED that the page
  does not already say — every claim with its log and section, its
  level (measured / derived), and its own small glossary so the
  section reads without the logs open. Nothing above the new sections
  was edited. Per page: **integer** — the wrap camp agrees BIT FOR
  BIT (`INT:64:8000000000000029` in five languages, rust's panic a
  debug-build property), php's fall to float with the actual tokens
  and the 1.000-against-0.306 cell agreement, python contradicting
  itself between its `int` and `ctypes.c_int64` holders, the answer
  grain showing `go.+` nearest the PANICKING `rust.+` at 0.907 while
  `go.+` against `java.+` is 0.094 with agreement 1.000, c++'s
  division by zero being an uncatchable `SIGFPE` DEATH, the shift
  mixed-holder table (total in go and rust only, two sharp against
  four blunt, closed by ruling kotlin OUT on two measured tests), and
  `42 << 42` giving seven acceptances and five answers — which adds a
  camp F-i6 had no row for, whether the shift COUNT is masked;
  **boolean/float** — the full twelve-language truthiness table
  (swift joins the bool-only camp; the refuse/coerce line is NOT the
  static-against-open line; a **T** for a checked language means the
  HOLDER was accepted), `pi + pi` bit-identical across seven
  (`FLOAT:64:401921fb54442d18`) with the method half that recording
  bits rather than printed decimals is what makes the claim possible,
  the −0.0 sign-read lesson (parsing php's `-0` as a number first
  would have manufactured a fracture belonging to the READER), the
  five known fractures that did not fracture, and NaN read through
  the operators; **string** — the e-acute concatenation as a HOLDER
  story (python and ruby's string holders identical at
  `text:c3a968656c6c6f` and 1.000 on `text|text`; the disagreement is
  entirely between the codepoint-array holders, ruby's carrying 233
  and php's carrying 195 and 169), php's row not being evidence about
  php's TEXT at all, the concatenation universal needing its spelling
  caveat, indexing splitting by holder inside one language, and text
  in the if-condition slot; **list** — php's `+` measured as a union
  by KEY (php answers the LEFT operand), ruby's `Set` holder answering
  as keyed, the two refusal KINDS being different and meaningful,
  `IndexError` as a RANGE and not a WIDTH complaint, python's
  containers disagreeing across holders where its numbers agree,
  repetition as a fifth operation, and iteration's frozenset caveat;
  **dict** — the php impostor resolution now MEASURED rather than
  argued, keyed merge as an operation the dominant needs and python
  lacks, F-d3's refusal kind as its own finding, holders of one form
  not all comparing equal, a `for` visiting the KEYS as the prior
  question F-d2 assumes, and c++ flatly refusing a `std::map` in a
  condition while accepting whole and fractional — the sharpest
  evidence that coercion-to-bool is a per-STRUCTURE decision inside a
  language rather than a per-language camp. Record:
  `PseudoCoupHQ/DevComms/log_039_census_foldback_and_log_rewrites.md`.
- 2026-08-29 — LANGUAGE-UPDATE DRILL, rust 1.98.0 (shipped 2026-08-20,
  five algebraic float methods stabilised). Measured, not asserted: the
  shape layer correctly did nothing (pin check 12/12, rust kind map
  byte-identical at 163 kinds / 106 proposed / 57 residue, token
  alphabet unchanged — and none of the three CAN see a release, since
  all read pinned or transcribed data); the toolchain cost 86 s and one
  command with one version pin in the estate and zero breakage; the
  existing float vectors re-ran with a 1-line PATH change and drifted
  by zero (20 rust cells, 78 probes, 100 CONFIRMED / 0 REFUTED at both
  1.96.1 and 1.98.0, result files byte-identical). The new methods DO
  change their answer with the build — one source, four builds, five
  probes differing, `loopmul` going from 4611686018427388000 to `inf`
  at O3 — while the ordinary operators moved on 0 of 12 probes and
  every NaN/infinity/negative-zero probe stayed bit-identical. Adding
  them cost 2 files and 193 lines with ZERO tool changes, but needed a
  probe shape the vectors format cannot express (bound-once AND opaque,
  both required — measured). Proposed to the owner, not decided: a fourth
  guaranteed arithmetic mode beside `wrapping`/`growing`/`approximating`,
  candidate name `rearranging`; ingress records it, never `unspecified`.
  Record: `PseudoCoupHQ/DevComms/log_076_rust_198_update_drill.md`.
- next: WP3/WP4, or a new census object if the owner opens one.
