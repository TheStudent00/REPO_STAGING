# log 272 — task lx1: the language axis on RISC-V — swift for riscv64 as an install, measured; the seven interpreted languages against the RISC-V definitions by agreement at points

Node: `hq.research.arch_unit_oracle.architectures.riscv64.language_axis`
(`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_2_language_axis/PROGRESS.md`).

Brief: `PRIVATE/PseudoCoupHQ/Research/briefs/task_lx1_brief.md`.
Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, all of it.
Background read in full before any work, per the brief: log_269
(`PRIVATE/PseudoCoupHQ/DevComms/log_269_bb2_the_bit_blast_route_on_x86_and_the_interpreted_seven.md`)
§"the interpreted seven" and §9 (the swift riscv64 probe, no-network
state); `Research/GLOSSARY.md`; `AgentMemory.md` §"the arch-opcode
emulation line"; `CLAUDE.md`.

Date: 2026-09-13. Instance `lx1`
(`PUBLIC/Airlock/instances/lx1.conf`, copied from
`t4.conf`, `proxy = yes` — used ONLY by lanes `lx1_l1` through
`lx1_l5`, the swift probe; every lane from `lx1_l6` on reaches no
network). Every lane ran on the tower guest through
`bash $HOME/Programming/PUBLIC/Airlock/remote_lane.sh`; nothing but
file editing, git and those commands ran on the laptop. A lane log's
host path on the tower is
`<runs>/lx1/agent/logs/<stamp>__<lane>.sh.log`;
every attribution below names its file. Paths inside a pasted command
are the ones the lane sees: `PseudoCoupHQ` IS
`PRIVATE/PseudoCoupHQ`. Every rendering is labelled
**LITERAL** (the object, quoted) or **GLOSS** (a plain-words reading
beside a literal). Lane scripts live under
`Research/oracle/riscv/lanes_lx1/`, written to the repo before
submission, per LAW.

THE SPELLING BAN, pasted verbatim as required:

> **THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25
> after a second violation).** No operator token may appear in ANY
> key, grouping, pairing, row structure, candidate selection, or
> comparison scope, anywhere in this line — not in matching, not in
> "which pairs get compared", not in report rows, not in dropdowns.
> The candidate set for comparison comes from machine-form evidence
> (clusters, connections, type pairs) or from ratified intention —
> never from the token. The token appears exactly once per unit: as
> a display label on the member. HISTORY OF VIOLATIONS, so the
> pattern is visible: (1) the arch campaign's cross-language matrix
> (caught by the owner 2026-08-24); (2) verdicts.py's row pairing (caught
> by the owner 2026-08-25 — the fix brief itself reintroduced it as
> "same-operator pairs"). MECHANICAL GUARD REQUIRED: every pipeline
> stage that groups or pairs units must run the spelling-key check
> (op_pipeline/check_no_spelling_keys.py) and refuse its own output
> on failure. A brief handed to any subagent for this line MUST
> paste this paragraph verbatim.

---

# 1. What this is, one sentence per object, in relation

- `cell` — one `arch_opcode` as a row of the RISC-V model table: one
  (mnemonic, operand shape, key width) triple. `twins.json` holds 255
  of them; that is the population both sections of this task count
  against.
- `term` — a cell's mapping as one z3 formula over unknown
  bit-vectors, architecture-neutral once built
  (`Research/GLOSSARY.md`).
- `emulation` — source in a target language which, run, computes a
  cell's term. For the seven interpreted targets there is no carve
  and no proof: the source is what runs, and the check is agreement
  over a sample, never a gate.
- `swift SDK` — an installable bundle (`swift sdk install <url>`, or
  a package manager entry) that lets `swiftc` produce code for a
  target triple it does not carry a runtime for out of the box. This
  task's section 1 asks whether one exists, published, for
  `riscv64-*-linux-*`.
- `interp_render.InterpRenderer` — task ex1's own renderer (called,
  not forked here): a term whose free symbols are parameter-slot
  names → one source file in the target's own operators.
- `interp_check`'s fuzz-census method — task ex1's own check (called,
  not forked): a sample of points built by a stated rule, the
  reference's own term evaluated at each point, the interpreter's own
  answer at each point, compared; an agreement is evidence, never a
  proof; declines are dropped from both numerator and denominator.

# 2. The walkthrough

Section 1 asked, with the network on, whether swift.org publishes an
installable SDK for a riscv64 Linux target, or whether a maintained
community toolchain does. Five lanes answered it. The image's swift
6.0.3 could not even run `swift sdk list` (a missing
`libxml2.so.2`), and the reason turned out to be more than "not
installed yet": Ubuntu's current suite ships libxml2 under soname 16
(`libxml2-16`, already installed, providing `libxml2.so.2`'s
successor `libxml2.so.16`) and no configured suite carries the old
soname any more, so `apt-get install libxml2` has no candidate at
all — a genuine incompatibility between this swift release and this
OS release, not a missing package. That closed off using
`swift sdk list` to ask the network directly, so the lanes asked the
network by other doors: swift.org's own release JSON names five
platforms and none of them is riscv64; the one non-x86_64/aarch64
platform it does carry, `static-sdk`, turned out to be a real,
downloadable artifact bundle (swift.org still serves it, 311 MB, for
swift-6.0.3-RELEASE), and its own manifest — not a guess, the
`swift-sdk.json` inside the bundle itself — lists exactly two target
triples, `x86_64-swift-linux-musl` and `aarch64-swift-linux-musl`. No
riscv64 entry. A GitHub search for a community toolchain found one
repository, `mcritz/swift-riscv64`, which describes building swift
from source for riscv64 hardware via a community CI server; it
publishes zero GitHub releases and was last touched in 2023, for
swift's 5.8 branch — a build recipe and a CI badge, not an
installable riscv64 Linux compiler. Nothing installs. Section 1's row
is a FLAG, per LAW, with every command and its output below — not a
guess.

Section 2 asked for the seven interpreted languages (cpython, php,
ruby, java, javascript, dart, csharp), each cell's term rendered into
that language's own operators the same way `interp_render.py` already
does for x86 cells (task ex1/ex2), run at a sample of points beside
the RISC-V reference's own term evaluated at the same points, over
all 255 RISC-V cells. No existing driver did this for RISC-V cells —
`expand2.py` (task ex2) is wired to the x86 model table's own
consumer/setter row reader — so this task wrote one,
`Research/oracle/riscv/rv_interp.py`, which reuses `interp_render.py`
and `interp_check.py` UNCHANGED (their render, sample, reference-eval
and interpreter-eval functions are imported and called) and supplies
only the RISC-V-side front half: `rv_loop.riscv_terms` for the term,
`rv_loop.in_parameter_slots` and `handful.place_record` (already the
established path — `rv_general.py`, task t4, uses the identical two
calls for the compiled-language RISC-V loop) to put that term in the
parameter-slot form the renderer and the checker both read. A sample
of 5 cells × 7 languages (35 runs) was run first and pasted before
the whole population: 35 of 35 agreed. The whole population — 255
cells × 7 languages, 1,785 runs — then ran in one pass, 626 seconds,
peak resident 135 MB, well inside the 6 GB bound; nothing hit the
60-second per-run timeout, so no retry pass was needed. Six of the
seven languages agree on 237–246 of 255; three languages (php, java,
dart) each carry two or three genuine disagreements, all at exactly
two points — an unsigned-64-to-float conversion at 2^63 (`fcvt.d.lu`,
`fcvt.s.lu`) and a signed 64-bit division edge (`div` at
(−1, INT64_MIN+1)) — named below, LITERAL, and not fixed here per the
brief. 237 of 255 agree on all seven at once.

# 3. Section 1 — swift on riscv64, as an install question, measured

## 3.1 libxml2 blocks `swift sdk list`, and it is not a simple absence

**LITERAL**, lane `lx1_l1_swift_riscv64_install_probe.sh` step [1/6],
tower log
`<runs>/lx1/agent/logs/20260913T170554Z__lx1_l1_swift_riscv64_install_probe.sh.log`:

```
  E: setgroups 0 failed - setgroups (1: Operation not permitted)
  E: Method gave invalid 400 URI Failure message: Failed to
     setgroups - setgroups (1: Operation not permitted)
  E: Method http has died unexpectedly!
  E: Sub-process http returned an error code (112)
  exit: 100
  Package libxml2 is not available, but is referred to by another
  package. This may mean that the package is missing, has been
  obsoleted, or is only available from another source
  E: Package 'libxml2' has no installation candidate
  exit: 100
```

**LITERAL**, lane `lx1_l2_swift_riscv64_probe_refined.sh` step [2/4], tower log
`<runs>/lx1/agent/logs/20260913T170630Z__lx1_l2_swift_riscv64_probe_refined.sh.log`,
read what apt actually holds under every name libxml2 might carry:

```
  libxml2:
    Installed: (none)
    Candidate: (none)
  ii  libxml2-16:amd64 2.15.2+dfsg-0.1ubuntu0.1 amd64  GNOME XML lib
  /usr/lib/x86_64-linux-gnu/libxml2.so.16
  /usr/lib/x86_64-linux-gnu/libxml2.so.16.1.2
```

**GLOSS.** libxml2 IS on the image, installed, under the package name
Ubuntu's current suite gives it (`libxml2-16`, soname 16,
`libxml2.so.16`). Swift 6.0.3's `swift-sdk` helper binary wants the
older soname, `libxml2.so.2`, which no package in this suite's
configured sources (`archive.ubuntu.com` / `security.ubuntu.com`,
suite `resolute`, per the same lane's step [3/4]) carries any more.
This is a version mismatch between the swift release and the OS
release, not a package that merely needs installing.

## 3.2 swift.org's own platform list, and the one bundle it does serve

**LITERAL**, lane `lx1_l1` step [4/6]:

```
  https://www.swift.org/api/v1/install/releases.json — 51,125 bytes
  grep -io riscv64: (count: 0)
  platforms named: "Linux", "Windows", "android-sdk", "static-sdk",
  "wasm-sdk"
```

**LITERAL**, lane `lx1_l3_swift_static_sdk_bundle_contents.sh` (tower log
`<runs>/lx1/agent/logs/20260913T170726Z__lx1_l3_swift_static_sdk_bundle_contents.sh.log`)
downloaded the `static-sdk` bundle swift.org serves for 6.0.3
(`swift-6.0.3-RELEASE_static-linux-0.0.1.artifactbundle.tar.gz`, 200
OK, 311,056,985 bytes, sha256
`67f765e0030e661a7450f7e4877cfe008db4f57f177d5a08a6e26fd661cdd0bd`)
and read its own manifest, step [4/4]:

```
  info.json:
  {
    "schemaVersion": "1.0",
    "artifacts": {
      "swift-6.0.3-RELEASE_static-linux-0.0.1": {
        "variants": [
          {"path": "..../swift-linux-musl"}
        ],
        "version": "0.0.1", "type": "swiftSDK"
      }
    }
  }

  swift-sdk.json (the manifest naming every triple the bundle
  carries):
  {
    "schemaVersion": "4.0",
    "targetTriples": {
      "x86_64-swift-linux-musl": { ... },
      "aarch64-swift-linux-musl": { ... }
    }
  }
```

**GLOSS.** The bundle's own manifest — the object that decides which
triples `swift sdk install` would register, not a guess about it —
names exactly two target triples. Neither is riscv64. This is the
one non-x86_64/non-aarch64 SDK platform swift.org's release list
carries at all, and it does not carry riscv64 either.

## 3.3 the one community repository, and what it actually publishes

**LITERAL**, lane `lx1_l4_swift_community_riscv64_search.sh` (tower
log
`<runs>/lx1/agent/logs/20260913T170834Z__lx1_l4_swift_community_riscv64_search.sh.log`)
step [1/2], GitHub repository search for "swift riscv64":

```
  total_count: 1
  - mcritz/swift-riscv64 -- Building swift for riscv64 platforms
```

**LITERAL**, lane `lx1_l5_swift_community_repo_check.sh` (tower log
`<runs>/lx1/agent/logs/20260913T170853Z__lx1_l5_swift_community_repo_check.sh.log`)
read that repository's own releases and README:

```
  releases: [] (zero)
  pushed_at: 2023-09-29T16:59:01Z
  stargazers_count: 0

  README:
  # Swift on Riscv64
  Building swift for riscv64 platforms
  ### How to setup a Developer Environment for Riscv64 using Docker
  ### Builds running on Swift Community CI Server
  Ubuntu Jammy 22.04 - Swift release/5.8 branch
  ### Riscv64 Hardware - Visionfive 2
```

**GLOSS.** Zero releases: nothing to download and install. The
content is a Docker recipe for BUILDING swift from source and a CI
badge for swift's 5.8 branch (not 6.x), last touched in 2023. It is a
"how to build one yourself" project, not a "here is one, installed",
and it targets a swift release three major versions behind this
image's.

## 3.4 the row

**FLAG (per LAW: no tool installs → FLAG with the commands and their
outputs, not a guess).** No Swift SDK for any riscv64 triple is
published by swift.org for swift 6.0.3, and no maintained community
distribution of a riscv64 Linux swift compiler was found. Nothing was
compiled, carved or run through `rv6_all_langs.py`'s route for swift,
because the brief's own gate for that step — "if one installs" —
never opened.

# 4. Section 2 — the interpreted seven against the RISC-V definitions

## 4.1 the sha256 of every store this task read

**LITERAL**, lane `lx1_l6_interp_sample.sh` step [1/3], tower log
`<runs>/lx1/agent/logs/20260913T171142Z__lx1_l6_interp_sample.sh.log`
(task sl1 runs beside this task and may regenerate `riscv_reference.py`;
this is the hash this task's every run actually read, not a claim
that the file stays this way):

```
  riscv_reference.py
    325e96a25cca475c8b0b150e4beca72a7a08682618844f38fae43625e955349e
  twins.json
    3ebdad9e3313c8663d9ac8cf0701ffb47801ce53dcc7e31a2c10701ad1dd473e
  model_table_rv.json
    9c7f211689f079e774219febb6704b59cb3afde2213ac2e1f0982e87d0f508f0
```

## 4.2 the sample, 5 cells × 7 languages, before the population

**LITERAL**, same lane, step [3/3]:

```
  [1/3] 255 cells (sample: first 5)
  [2/3] 255 (cell, place) terms rebuilt
  [3/3] 35/35 runs, 15 s, peak 135,440 kB

  add   gpr_gpr_gpr  64  x 7 languages: AGREED, AGREED, AGREED,
                                        AGREED, AGREED, AGREED, AGREED
  add   gpr_gpr_same 64  x 7: all AGREED
  addi  gpr_gpr_imm  64  x 7: all AGREED
  addiw gpr_gpr_imm  32  x 7: all AGREED
  addw  gpr_gpr_gpr  32  x 7: all AGREED
```

35 of 35 agreed. The driver (`Research/oracle/riscv/rv_interp.py`,
written for this task) reproduces the interpreted route correctly on
a first, small population before the whole run.

## 4.3 THE INTERPRETED SEVEN, THE TERM'S OWN OPERATORS, of 255 on every row

**LITERAL**, lane `lx1_l8_interp_table_and_guard.sh` step [1/3], tower
log
`<runs>/lx1/agent/logs/20260913T172342Z__lx1_l8_interp_table_and_guard.sh.log`,
over the full population lane `lx1_l7_interp_full_population.sh`
(tower log
`<runs>/lx1/agent/logs/20260913T171217Z__lx1_l7_interp_full_population.sh.log`,
1,785 of 1,785 runs completed in one pass, 626 s, peak resident 135
MB, zero TIMEOUT so no retry pass ran):

| language | agreed | disagreed | refused | timed out | of |
|---|---|---|---|---|---|
| cpython | 246 | 0 | 9 | 0 | 255 |
| php | 237 | 3 | 15 | 0 | 255 |
| ruby | 246 | 0 | 9 | 0 | 255 |
| java | 238 | 2 | 15 | 0 | 255 |
| javascript | 246 | 0 | 9 | 0 | 255 |
| dart | 238 | 2 | 15 | 0 | 255 |
| csharp | 240 | 0 | 15 | 0 | 255 |
| **agreeing on all seven** | **237** | | | | **255** |

Table 4.3 — the population is the 255 RISC-V cells `twins.json` holds
(brief §2), every row carries its own "of 255".

## 4.4 beside x86's own two readings (log_269)

The brief's own background reading (log_269 §8) names x86's
interpreted-seven number as "162–166 of 253". THAT reading is task
bb2's own BIT-BLAST CIRCUIT route (z3's own gate circuits, printed as
named-gate source, over 253 x86 cells) — a different render from the
one this task's brief asks for in section 2 ("the emulation rendered
... the same general render", i.e. the term printed in the language's
own operators, tier 1/tier 2, the same concept `render_general.py`
and `interp_render.py` both implement). Log_269 §8 itself carries the
OTHER x86 reading, task ex2's own, which IS the term's-own-operators
route this task's section 2 uses — put beside it, not the bit-blast
one, because it is the same route:

| language | x86, ex2 (term's own operators), of 253 | riscv64, this task, of 255 |
|---|---|---|
| cpython | 193 | 246 |
| php | 184 | 237 |
| ruby | 193 | 246 |
| java | 184 | 238 |
| javascript | 193 | 246 |
| dart | 184 | 238 |
| csharp | 184 | 240 |

Table 4.4 — same route (the term's own operators) on both
architectures; the x86 column is log_269 §8's own table, unchanged.

## 4.5 EVERY DISAGREEMENT, LITERAL

**LITERAL**, lane `lx1_l8` step [1/3]:

| language | mnem | shape | width | point | reference | interpreter |
|---|---|---|---|---|---|---|
| php | `div` | `gpr_gpr_gpr` | 64 | [18446744073709551615, 9223372036854775809] | 9223372036854775807 | 9223372036854775808 |
| dart | `fcvt.d.lu` | `fpr_gpr` | 64 | [9223372036854775808] | 4890909195324358656 | 14114281232179134464 |
| java | `fcvt.d.lu` | `fpr_gpr` | 64 | [9223372036854775808] | 4890909195324358656 | 14114281232179134464 |
| php | `fcvt.d.lu` | `fpr_gpr` | 64 | [9223372036854775808] | 4890909195324358656 | 14114281232179134464 |
| dart | `fcvt.s.lu` | `fpr_gpr` | 32 | [9223372036854775808] | 18446744071008419840 | 18446744073155903488 |
| java | `fcvt.s.lu` | `fpr_gpr` | 32 | [9223372036854775808] | 18446744071008419840 | 18446744073155903488 |
| php | `fcvt.s.lu` | `fpr_gpr` | 32 | [9223372036854775808] | 18446744071008419840 | 18446744073155903488 |

Table 4.5. **GLOSS**, stated once and not resolved here (the brief:
"a disagreement is a defect in the render or the definition, named,
not fixed here"). Both defects are named by their instance, not
fixed: (a) the `div` disagreement is one point,
(lhs=2^64−1, rhs=2^63+1) — signed −1 divided by a value one past
`INT64_MIN` — where php's own integer division disagrees with the
reference by exactly 1; (b) the two `fcvt.*.lu` (convert an unsigned
64-bit integer to a float/double) disagreements are the SAME point
(2^63) and the SAME wrong answer across all three languages that
show it (dart, java, php), which is evidence the defect is in the
CONSTRUCTION `interp_render` builds for this operation at this point
(a common code path those three take and cpython/ruby/javascript do
not), not three independent interpreter quirks.

## 4.6 EVERY REFUSAL, BY CAUSE

**LITERAL**, lane `lx1_l8` step [1/3]:

| language | cause | cells |
|---|---|---|
| cpython | operator not covered by the renderer | 8 |
| php | operator not covered by the renderer | 8 |
| ruby | operator not covered by the renderer | 8 |
| java | operator not covered by the renderer | 8 |
| javascript | operator not covered by the renderer | 8 |
| dart | operator not covered by the renderer | 8 |
| csharp | operator not covered by the renderer | 8 |
| php | a width c has no holder for | 6 |
| java | a width c has no holder for | 6 |
| dart | a width c has no holder for | 6 |
| csharp | a width c has no holder for | 6 |
| cpython | the runner did not answer | 1 |
| php | the runner did not answer | 1 |
| ruby | the runner did not answer | 1 |
| java | the runner did not answer | 1 |
| javascript | the runner did not answer | 1 |
| dart | the runner did not answer | 1 |
| csharp | the runner did not answer | 1 |

Table 4.6. Both causes are `interp_render`'s own refusal text
(`emulate.Refused`), unchanged, read off the render attempt; "the
runner did not answer" is the one cell every language refused the
same way (1 cell, all seven languages), consistent with a
render-level or arrival-level cause rather than a per-language one —
named here, not diagnosed further, per the brief's "not fixed here".

# 5. The guards

## 5.1 the spelling guard

**LITERAL**, lane `lx1_l8` step [2/3]:

```
  lx1_interp_runs.jsonl.as_one.json  (1,785 rows)
    operator inventory: 91 tokens
    PASS -- no operator token in any key, grouping, pairing or row
    structure

  lx1_interp_sample.jsonl.as_one.json  (35 rows)
    operator inventory: 91 tokens
    PASS -- no operator token in any key, grouping, pairing or row
    structure
```

`grep -c exempt` over `rv_interp.py` (the one file this task added
under `Research/oracle/riscv/`): 0.

## 5.2 memory

Peak resident recorded on every lane: sample 135,440 kB, full
population 135,432 kB, table+guard 135,176 kB — all one order of
magnitude under the 6 GB bound (`ABORT_MEMORY_LX1`, never triggered).
One process throughout; no worker pool.

## 5.3 the conventions verifier

**LITERAL**, the reproducing command this task ran as lane `lx1_l9_conventions_verifier.sh`, from the `lx1` instance:

```
CCLC=PseudoCoupHQ/Research/op_pipeline
CCLC=$CCLC/check_conventions_log_claims.py
LOG=PseudoCoupHQ/DevComms
LOG=$LOG/log_272_lx1_riscv64_language_axis.md
python3 $CCLC --verify --timeout 20 $LOG
```

Tally pasted in §5.3a below once run.

### 5.3a tally

**LITERAL**, lane `lx1_l10_conventions_verifier_rerun.sh` (tower log
`<runs>/lx1/agent/logs/20260913T172925Z__lx1_l10_conventions_verifier_rerun.sh.log`):

```
  log_272_lx1_riscv64_language_axis.md: 11 claims extracted
  claims 11 | MATCHES 0 | DIFFERS 0 | UNVERIFIABLE 11 | REFUSED 0
  NOT_RERUNNABLE 0
  causes: attribution_only 10, prose_only 1
```

Zero DIFFERS. Every claim in this log is an ATTRIBUTION (a lane and
a step number cited above the pasted object) or the one PROSE
sentence in §2 asserting the sample's own count — never a bare `$ `
shell transcript — a deliberate choice: every command this task ran
either reaches the network (refused by this same verifier's own
`reaches_the_network` rule had it been posed as one) or writes
(`apt-get install`, also refused), so posing them as re-runnable
claims would have added REFUSED rows, not MATCHES, for no gain; the
LITERAL text is preserved either way. A first run of this same lane
(`lx1_l9_conventions_verifier.sh`, tower log
`<runs>/lx1/agent/logs/20260913T172841Z__lx1_l9_conventions_verifier.sh.log`)
found 4 claims mis-shaped as `bare_paste` (an attribution lead-in
missing its **LITERAL** marker) — also UNVERIFIABLE, never DIFFERS,
but fixed for §5.1a of the comms protocol ("every rendering says
LITERAL or GLOSS") before this re-run.

# 6. Two lists

## Decided, recorded for audit

- Section 1's row is a FLAG: no swift SDK or maintained community
  toolchain for riscv64 exists to install for swift 6.0.3, measured
  with the network on across five lanes (§3); nothing was compiled or
  carved for swift, because the brief's own "if one installs" gate
  never opened.
- `Research/oracle/riscv/rv_interp.py` was written to run the seven
  interpreted languages against RISC-V cells, reusing
  `interp_render.py` and `interp_check.py` unchanged (imported and
  called) and mirroring `rv_general.py`'s (task t4) own front half
  (`rv_loop.riscv_terms`, `rv_loop.in_parameter_slots`,
  `handful.place_record`) rather than `expand2.py`'s x86-row reader,
  which does not apply to RISC-V cells.
- The full 255-cell × 7-language population (1,785 runs) completed in
  one pass with zero timeouts; the two genuine defect classes found
  (§4.5) are recorded LITERAL and left unfixed, as the brief states.

## Awaiting the owner

- Whether the `fcvt.d.lu` / `fcvt.s.lu` unsigned-to-float defect at
  2^63, shared by dart/java/php and absent from cpython/ruby/
  javascript, is worth its own follow-on task to isolate in
  `interp_render.py`'s construction, or waits for a later pass over
  every render refusal together.
- Whether the `div` disagreement (php, one point) is a php-specific
  integer-division quirk at that exact edge or a rendering gap;
  distinguishing the two needs a probe this task did not run.
- Whether the incompatibility found in §3.1 (this image's swift 6.0.3
  wanting `libxml2.so.2`, which this Ubuntu suite no longer ships
  under any package name) is worth recording as a standing fact about
  the image, since it also blocks any FUTURE swift SDK probe in this
  image unless the image itself changes.
