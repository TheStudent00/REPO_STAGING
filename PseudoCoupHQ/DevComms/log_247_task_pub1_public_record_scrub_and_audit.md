# log_247 — task pub1: the public record — REPO_STAGING scrub and the other five public repos, audit only

Read first, in full, before any of this work: the cardinal rule at the
top of `PRIVATE/DevComms/LLM_communication_protocol.md` ("NEVER
PUT SENSITIVE INFORMATION IN A PUBLIC REPO"), the brief at
`PRIVATE/PseudoCoupHQ/Research/briefs/task_pub1_brief.md`, and
`PUBLIC/REPO_STAGING/stage.sh` +
`PUBLIC/REPO_STAGING/scrub_patterns.tsv`. No sub-agents were
used; this was done by hand, in the foreground, over the tracked text
of six private sources and five public repositories.

## Walkthrough

`stage.sh` copies the TRACKED files of six private sources
(`PlanPlan`, `PseudoCoupHQ`, `PseudoCoup_v5`, `PseudoCoup_v6`,
`PseudoIR`, `DevComms`) into a gitignored private area,
`REPO_STAGING/.stage_tmp/`, runs every `<regex><TAB><replacement>`
line of `scrub_patterns.tsv` over the text files there, and refuses to
touch the public tree — no commit, no push — if any pattern still
matches afterward. `bash stage.sh --no-push` fills `.stage_tmp/` and
stops before the push either way, so it is safe to run repeatedly
while patterns are incomplete.

I ran `bash stage.sh --no-push` first to fill `.stage_tmp/`, then
grepped that private area, restricted to the ~9,000-10,000 files that
would actually be tracked (checked with `git check-ignore` against
REPO_STAGING's own `.gitignore`, the same test the check step itself
uses), for every fingerprint class the owner named: OS name+version, kernel
string, podman version, memory, core count, CPU model, Unraid
version, disk size, MAC address, container id, and any hostname not
yet covered. §1 below lists what I actually found, by file and line,
before I wrote a single pattern.

I then added 16 new lines to `scrub_patterns.tsv` (§2), fixed one
already-broken line I found while doing this (a `~` → `~` no-op that
could never converge — traced to a botched earlier redaction, evidence
in §2), and fixed one bug in my OWN first draft of a new pattern
(a line starting `#[0-9]+-Ubuntu…` was silently skipped by
`stage.sh`'s own comment filter, `case "$pat" in '#'*) continue`,
because a scrub pattern is not allowed to start with `#`). Three
`--no-push` runs later, every fingerprint class converged to zero
except one: `\bDee\b` still matches 7 files. I traced all 7 by hand
(§4). Six are coincidental byte noise inside compressed PNG
screenshots — confirmed unreadable garbage, not text, by `strings`
and a hex dump. The seventh is real: a genuine, live "the owner" comment in
`PseudoCoupHQ/Research/kind_fuzz_clustering/verify_row_graph_v4.js`,
which `file(1)` misreports as `application/octet-stream` ("a node
script executable (binary data)"), so `stage.sh`'s own text-file gate
skips it during scrubbing — and I demonstrated that the check step's
own default `grep` (no `-a`) inconsistently detects this survivor too
(it found it once, missed it on a bare rerun, and only forcing text
mode with `-a` found it reliably every time). That is a real gap in
the tool itself, not something a new pattern line can fix, so I did
not touch `stage.sh` or the private source — out of the authority this
task gave me. Because of this one survivor, `stage.sh --no-push` never
printed "clean", so per my own instructions I did **not** run
`bash stage.sh` (the pushing form). REPO_STAGING's tip is unchanged.

For §3, I ran the same class-by-class greps (forced-text, restricted
to `git ls-files` — a long line coming from an embedded base64 image
in one `.ipynb` was excluded as noise, since a random byte run that
long can coincidentally spell a short word) over each of the five
public repositories named in the brief, read-only, no edits, no
pushes: `Airlock`, `GraphModel`, `Ourobrowser`, `PseudoCoup`,
`ZSpectralCompression`. I also ran Airlock's own guard,
`scrub_check.sh`. Findings are in §3's table.

---

## §1. The objects — machine fingerprints found in REPO_STAGING's private area, before any pattern was written

Commands run (restricted to the file list that `git check-ignore`
says would actually be tracked):

```
bash stage.sh --no-push
grep -rnEi '<class-regex>' .stage_tmp/<would-be-tracked files>
```

| class | files (examples) | literal instance |
|---|---|---|
| OS name+version | `PseudoCoupHQ/DevComms/log_077_returning_session_briefing.md:460` | `base is <os>, kernel <kernel>.` |
| OS name+version | `PseudoCoupHQ/Planning/.../node_0_3_0_1_dominant_intentions/PROGRESS.md:66` | `libncurses6 apt package exists on the container's <os>` |
| kernel string | `log_077:460`, `log_167_task63_runtime_callee_generalized.md:376`, `log_184_task77_dashboard_in_ourobrowser.md:293`, `Research/op_pipeline/canon39_callee_swift_lane_printed.txt:10` | `<kernel>` |
| kernel build tag | same `canon39_callee_swift_lane_printed.txt:10` | `uname: Linux <container-id> <kernel> #<build>-<os> SMP …` |
| memory | `PseudoCoupHQ/Research/LAW.md:133` | `The tower guest has <ram> and runs one heavy lane at a time.` |
| core count | `log_131_task40_regeneration_trickle.md:34,342`, `Planning/.../PROGRESS.md:2560`, `Research/op_pipeline/regen_cost.md:45` | `capped at 6 of this machine's <cores>`, `cpu cap: 6 of <cores>` |
| container id (hostname-shaped hex) | `log_138_airlock_instances_feature.md:434,514`, `log_175_task72_go_diaries_coverage.md:779`, `canon39_callee_swift_lane_printed.txt:10,11` | `hostname: <container-id>`, `hostname: <container-id>`, `hostname: <container-id>` |
| account handle / real name (`<user>`, bare) | 556 occurrences, e.g. `log_195_task89_bank_round15.md:70` | `-rw-rw-r-- 1 <user> <user> 5811 Sep 3 23:17 check_dashboard_py_no_spelling.py` (an `ls -l` paste) |
| account handle / real name (`<tower-user>`, bare) | 84 occurrences, e.g. `log_239_task_h1b_composition_column.md:27` | `/home/<tower-user>/AirlockRuns/h1b/agent/logs/` |
| absolute home path | 316 occurrences of `/home/<user>/Programming` + 204 of `/home/<user>(airlock)?/AirlockRuns`, e.g. `log_124_task34_interp_union_relaunch.md:97` | ``shell's `hostname` is `<user>` and `/home/<user>/Programming/PRIVATE/PseudoCoupHQ` `` |
| working name (`the owner`) | 7,352 occurrences across 1,338 files (this is the whole corpus's normal use of his working name, not a special case) | e.g. `PseudoCoupHQ/AgentMemory.md:8` — `Created 2026-08-12 at the owner's instruction` |

Checked and confirmed **absent** everywhere in the current corpus (no
literal instance found, despite a broad case-insensitive search):
podman version banners, Unraid version, disk sizes stated as a machine
fingerprint (the corpus does contain plenty of unrelated *data-volume*
byte counts, e.g. `9,734,518,662 bytes / 9.73 GB`, which are research
output sizes, not a disk's capacity), MAC addresses, and any CPU-model
string (`Ryzen`, `Xeon`, `EPYC` all checked, zero hits beyond the
brief's own illustrative text).

Two things checked and ruled NOT a fingerprint, so not scrubbed:
- `56 core`, `786 core`, `793 core`, `1,086 core`, `3436 core` — all
  research vocabulary (`core-equivalence classes`, Rust's
  `core::ops::RangeInclusive`, `core-differing unit pairs`), not a
  core *count* of any machine.
- `Ubuntu clang version 21.1.8 (6ubuntu1)`, `gcc (Ubuntu
  15.2.0-16ubuntu1) 15.2.0`, `GNU objdump (GNU Binutils for Ubuntu)
  2.46` — compiler/binutils version banners (the Debian/Ubuntu package
  suffix is part of the *toolchain's own version string*), which is
  exactly the class the owner's ruling says to KEEP. None of these match the
  `Ubuntu NN.NN` OS-release shape the new pattern targets, confirmed
  by hand.

---

## §2. REPO_STAGING — before / after, and the added patterns

**Before** (counts from §1, same restricted file set): every class
above nonzero except podman/Unraid/disk/MAC/CPU-model (zero, see
above).

**One existing bug fixed.** `scrub_patterns.tsv` already had two
broken lines, `~␉~` (pattern equals replacement — a no-op that can
never converge, since `sed` "replacing" `~` with itself leaves `~`
present forever) and one still-present no-op, `<tower-user>␉<tower-user>`
(left as is — harmless, zero live matches, not blocking, not part of
this brief). I found the forensic cause of the `~␉~` line in
`PseudoCoup_v6/Research/r2_compiler_source_census/census_sources.py`,
whose real (private, unscrubbed) content reads
`"Research/rust_routing/sources/encoder/asm~/.cargo/"` — that `asm~`
is exactly what you get if `/home/<user>` → `~` had been run across
this project's files INCLUDING `scrub_patterns.tsv` itself, which
turned the pattern's own left-hand side `/home/<user>` into `~`,
producing the broken `~␉~`. I replaced it with the working line that
evidence points to:

```
/home/[a-zA-Z0-9_]+	~
```

placed at its original position (before the later `` →
empty block), so `/home/<user>/Programming/...` and
`/home/<tower-user>/AirlockRuns/...` both convert to `~/...` first and
then get stripped project-relative by the existing rules below it.

**New lines added** (LITERAL, in the order they now appear in
`scrub_patterns.tsv`):

```
\bDee\b	the owner
\b<user>\b	<user>
\b<tower-user>\b	<user>
[Uu]buntu [0-9]{2}\.[0-9]{2}( LTS)?	<os>
[0-9]+\.[0-9]+\.[0-9]+-[0-9]+-generic	<kernel>
[#][0-9]+-Ubuntu\b	#<build>-<os>
guest has <ram>	guest has <ram>
\b12 cores\b	<cores>
\b10 vCPUs\b	<vcpu>
\bRyzen 7 3700X\b	<cpu>
\bpodman version [0-9]+\.[0-9]+\.[0-9]+\b	podman version <podman>
\bUnraid [0-9]+(\.[0-9]+){1,2}\b	Unraid <unraid>
([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}	<mac>
hostname: [0-9a-f]{12}\b	hostname: <container-id>
Linux [0-9a-f]{12}\b	Linux <container-id>
```

(The last three lines above did not exist as one class in the brief's
wording — they cover "hostnames not yet covered" and "container ids".)

Podman/Unraid/MAC/CPU-model patterns are added defensively per the
brief's class list even though zero real instances currently exist to
verify them against (flagged in §4.3).

**One bug I introduced and then fixed**: my first draft of the
kernel-build-tag pattern was `#[0-9]+-Ubuntu\b`. `stage.sh` treats any
`scrub_patterns.tsv` line whose PATTERN starts with `#` as a comment
(`case "$pat" in '#'*) continue`) — so that line was silently doing
nothing. Rewrote it as `[#][0-9]+-Ubuntu\b` (a bracket expression, not
a leading `#`), confirmed it now fires with a targeted `sed` test and
then a full `--no-push` run.

**After** (same restricted file set, forced-text `grep -a` to avoid
the binary-detection flakiness documented in §4.1): every class is
zero except `\bDee\b`, still 7 — all seven traced and explained in
§4. No other class regressed or remained nonzero.

**Spot-checked substitutions** (all read correctly):
- `log_077…md:460` → `base is <os>, kernel <kernel>.`
- `LAW.md:133` → `The tower guest has <ram> and runs one heavy lane…`
- `log_131…md:342` → `cpu cap: 6 of <cores>`
- `canon39_callee_swift_lane_printed.txt:10` → `uname: Linux <container-id> <kernel> #<build>-<os> SMP PREEMPT_DYNAMIC …`
- `log_124…md` → `-rw-rw-r-- 1 <user> <user> 29587 …` (an `ls -l` paste, name gone from both owner and group columns)
- `AgentMemory.md:8` → `Created 2026-08-12 at the owner's instruction…`

**REPO_STAGING tip: unchanged, `6e0eb55`** (`stage
2026-09-09T19:04:30Z: PlanPlan PseudoCoupHQ PseudoCoup_v5 PseudoCoup_v6
PseudoIR DevComms (3 files, scrubbed)`, already on `origin/master`).
`bash stage.sh` (the pushing form) was **not** run, because
`--no-push` never printed "clean" — one real survivor remains (§4.1).
`scrub_patterns.tsv` sits as an uncommitted working-tree edit; I did
not commit or push it, since only `bash stage.sh` is allowed to push
and its own gate was not satisfied.

---

## §3. Audit of the other five public repositories (read-only, no edits, no pushes)

Command, run per repo: `git ls-files -z | xargs -0 grep -nIE
'<class-regex>'`, forced-text, three example lines quoted with file
and line number.

**Table 1 — repo × class, hit counts (files : lines).** `0:0` means
checked, none found.

| class | Airlock | GraphModel | Ourobrowser | PseudoCoup | ZSpectralCompression |
|---|---|---|---|---|---|
| `the owner` (working name) | 0:0 | 0:0 | 77:180 | 5:35 | 98:218 |
| `<user>`/`<tower-user>` (account) | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| `<owner>` (public identity — see note) | 2:11 | 0:0 | 3:3 | 0:0 | 1:1 |
| email address | 1:4 (the public noreply address, see note) | 0:0 | 0:0 | 0:0 | 0:0 |
| IPv4 address | 1:1 (`127.0.0.1`, a proxy default, not personal) | 0:0 | 0:0 | 0:0 | 0:0 |
| MAC address | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| container-id hostname | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| absolute `/home/<user>` path | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| absolute `/Users/<user>` path | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| `~/Programming` (path outside project root) | 0:0 | 0:0 | 91:130 | 7:51 | 106:192 |
| secrets (key/token/password patterns) | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| OS name+version | 2:3 (see note) | 0:0 | 0:0 | 0:0 | 0:0 |
| kernel string | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| memory/cores (`3N GiB`/`1N cores`/`vCPUs`) | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| CPU model | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| podman version | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| Unraid version | 0:0 | 0:0 | 0:0 | 0:0 | 0:0 |
| Airlock's own `scrub_check.sh` | **PASS** — 7 patterns, 67 tracked files, 0 untracked-and-unignored, 0 offenders | n/a | n/a | n/a | n/a |

Examples, LITERAL, file and line:

- **Ourobrowser**, `the owner`:
  - `Planning/CHECK_0.md:14` — `> — the owner, 2026-07-31`
  - `Planning/CHECK_0.md:37` — `the owner's to settle; PROTOCOL §2 reserves level-1 COREs to him.`
  - `Planning/CORE_0.md:5` — `settled_by: the owner`
- **Ourobrowser**, `~/Programming`:
  - `Planning/CHECK_0.md:41-42` — `python3 PRIVATE/PlanPlan/framework/check_plans.py \` / `PUBLIC/Ourobrowser/Planning`
  - `Planning/DASHBOARD.md:2` — `<!-- Produced by PRIVATE/PlanPlan/framework/generate_dashboards.py …`
- **ZSpectralCompression**, `the owner`:
  - `DevComms/log_001_one_dimensional_measurements.md:8` — `the owner, 2026-09-08:`
  - `DevComms/log_001_one_dimensional_measurements.md:140,168` — `the owner:` (speaker label)
- **ZSpectralCompression**, `~/Programming`:
  - `DevComms/log_001_one_dimensional_measurements.md:3` — `` Repo: `PUBLIC/ZSpectralCompression`. Written 2026-09-08 by ``
  - `DevComms/log_001_one_dimensional_measurements.md:266` — `` `PUBLIC/ZSpectralCompression/zspectral_compression.py` — the ``
- **PseudoCoup**, `the owner`:
  - `.planning/00_Upgrade_Plan.md:4` — `` `version = "3.0.0"` -> `"4.0.0"` (rename approved by the owner in the executing session). ``
  - `.planning/00_Upgrade_Plan.md:20` — `Status date: 2026-07-14. Author-of-record: planning agent, for the owner's sign-off.`
- **PseudoCoup**, `~/Programming` (a tracked config file, not a log):
  - `.claude/launch.json:8-9` — `"PRIVATE/PseudoCoupHQ/Research/op_pipeline/dashboard_test_server.py"`, `"PRIVATE/PseudoCoupHQ/Research"`
- **Airlock**, `<owner>`/email (both deliberate, see note):
  - `DevComms/log_002_pii_scrub.md:29-30` — `` **Deliberately kept.** `<owner>` and "The Student" are the chosen public identity for this line of work. ``
- **Airlock**, OS name+version (see note):
  - `Containerfile:45` — `# <os> ships 3.14; the host develops on 3.13 (via Anaconda), and`
  - `up.sh:157,162` — `# that name. podman's older CNI backend, which is what <os>'s podman`, `# naming the cause. Seen 2026-09-08 on a fresh <os> guest.`

**Notes on the two tables above** (read judgements, not actions —
nothing in §3 was changed):
- `<owner>` and its `@users.noreply.github.com` address are, per
  Airlock's own `DevComms/log_002_pii_scrub.md`, the deliberately
  chosen public identity for this body of work — not a leak of a
  private handle.
- Airlock's `Containerfile`/`up.sh` mentions of "<os>"/"Ubuntu
  26.04" read as the tool's own documented build-image tag (necessary
  for anyone building the container), not a fingerprint of the owner's
  personal machine — a different case from REPO_STAGING's DevComms
  logs, which describe the owner's actual running infrastructure. Flagged in
  §4 for the owner to confirm this reading.

---

## §4. What could not be scrubbed by pattern, by cause — flagged, not forced

### §4.1 A real leak a pattern cannot reach: `verify_row_graph_v4.js` (the one item that actually blocks "clean")

- **What**: line 4 of
  `PseudoCoupHQ/Research/kind_fuzz_clustering/verify_row_graph_v4.js`
  reads `// with the owner's three rulings of 2026-08-21.` — a real,
  legible comment, not noise.
- **Why a pattern can't fix it**: `stage.sh` only scrubs a file if
  `file -b --mime-type` returns `text/*`, `application/json`,
  `application/x-shellscript`, or `application/javascript`. For this
  file, `file` returns `application/octet-stream` (its own words:
  "a node script executable (binary data)") — the `#!/usr/bin/env
  node` shebang plus something later in the file makes `file` call it
  binary, so `stage.sh`'s scrub loop skips it outright, regardless of
  which patterns exist.
- **The check step is not reliable here either**: `stage.sh`'s
  survivor check runs `grep -rlE` with no `-a`. I reproduced this
  directly — a bare `grep -n 'the owner' <file>` on this exact file returned
  no match and exit code 1 (GNU grep's own binary-file heuristic
  triggering, independent of `stage.sh`), while `grep -an 'the owner'
  <file>` reliably finds it at line 4 every time. This means a future
  `--no-push` run could, by the same heuristic, silently fail to flag
  this survivor and print "clean" with the real comment still inside.
- **What I did / did not do**: found it, traced the mechanism, did
  not touch `stage.sh` (a tool-logic change) or the private source in
  `PseudoCoupHQ` (outside REPO_STAGING, outside this brief) — both are
  outside what I was authorized to edit.
- **Two ways to close it, the owner's call**: (a) widen `stage.sh`'s
  `is_text()` to also treat a file `file(1)` calls "... script
  executable" as text, so the scrub step actually reaches it; or (b)
  edit the one private comment directly. Either way, `--no-push` needs
  a rerun before "clean" is real.

### §4.2 Binary noise, not a leak: six PNG screenshots

- `PseudoCoupHQ/DevComms/screens/log_198/06_pane4_go_one_probe_walk.png`
- `PseudoCoupHQ/DevComms/screens/log_198/09_pane4_cpp_now_figure2_dynamic.png`
- `PseudoCoupHQ/DevComms/screens/log_198/13_pane4_go_at_an_earlier_commit.png`
- `PseudoCoupHQ/DevComms/screens/log_192/tab1_unitviewer_now.png`
- `PseudoCoupHQ/DevComms/screens/log_192/day_click_moves_the_window_selects_nothing.png`
- `PseudoCoupHQ/DevComms/screens/log_191/tab1_unitviewer_at_round12.png`

Each trips `\bDee\b` in the survivor check. I pulled the actual bytes
around every match with `strings`/a hex dump: `$Idee`, `9dee`,
`RsDEE`, `1DEE`, `deer`, `Deeg`, `the owner˾`, `the owner˞` — unreadable garbage
inside the compressed pixel stream, not rendered text and not a PNG
metadata chunk (no `tEXt`/`iTXt` chunk present). `stage.sh` correctly
never scrubs binaries (a `sed` rewrite would corrupt the image), and
its check step has no way to tell coincidental noise from a real leak
in a binary file — it can only refuse. **Flagged, not forced**: is a
6-file coincidence an acceptable, permanent exception, and if so
should the check step gain the same `is_text()` gate the scrub step
already has (which would also silently un-block §4.1's real leak
unless §4.1 is fixed first) — or should these particular screenshots
be gitignored as regenerable dashboard output (REPO_STAGING's own
stated policy already excludes other regenerable Research output by
the same reasoning)? the owner's call either way.

### §4.3 Added without a real instance to test against

`podman version`, `Unraid <version>`, and a MAC-address pattern were
added per the brief's named class list, but zero real occurrences
exist anywhere in the current corpus, so none of the three has been
exercised against a live example. Not wrong to have added them, but
unverified — noted so nobody mistakes "pattern exists" for "pattern
proven".

### §4.4 Disk sizes — no pattern added at all

Zero real machine-disk-size fingerprint found anywhere in the corpus
after a broad search (`TB`, `NVMe`, `SSD`, `df -h`-shaped output). The
corpus is, however, full of legitimate *research data-volume* byte
counts (`9,734,518,662 bytes / 9.73 GB`, dozens of `.json` product
sizes) that a generic `[0-9]+ ?(GB|TB)` pattern would wrongly mangle.
No safe, narrow phrasing suggested itself from the evidence on hand.
**Flagged for the owner**: what exact wording should this pattern look for,
if/when a real disk-size fingerprint appears?

### §4.5 Toolchain-adjacent strings, left alone on purpose

`Ubuntu clang version 21.1.8 (6ubuntu1)`, `gcc (Ubuntu
15.2.0-16ubuntu1) 15.2.0`, and one OpenJDK build string,
`25.0.3+9-2-26.04.2-Ubuntu`, all carry the word "Ubuntu" as part of a
KEPT toolchain version banner, not as a bare `Ubuntu NN.NN` OS
release. The OpenJDK one is genuinely dual — it is JDK build
provenance (kept, per the owner's ruling) AND it happens to embed the same
`26.04` release number that is already scrubbed elsewhere via the
direct `base is <os>` statement in `log_077`. Left
unscrubbed rather than risk damaging protected toolchain text.
**Flagged for the owner** to confirm this reading is the intended line.

### §4.6 Not touched, not blocking

`scrub_patterns.tsv`'s pre-existing `<tower-user>␉<tower-user>` line
is the same broken-identity shape as the `~␉~` bug I fixed in §2, but
currently has zero live matches and is not blocking anything, so I
left it as found rather than take an unasked-for action on a line
outside this brief's named classes.

---

## The two lists

**Decided, recorded for audit** (done, in this session, within the
authority the brief gave: scrub_patterns.tsv edits and `bash stage.sh
--no-push` runs only):
1. Fixed the broken `~␉~` no-op in `scrub_patterns.tsv`, replacing it
   with a working `/home/[a-zA-Z0-9_]+␉~` line, forensically traced to
   a prior botched redaction.
2. Added 15 new fingerprint patterns (§2) covering OS version, kernel
   string, kernel build tag, tower RAM, core count, vCPU, CPU model,
   podman version, Unraid version, MAC address, container-id hostname
   (two phrasings), and the two real names (`the owner`, `<user>`/`<tower-user>`).
3. Found and fixed a bug in my own first draft (a `#`-leading pattern
   silently skipped by `stage.sh`'s own comment filter).
4. Converged, via three `--no-push` runs plus a forced-text
   cross-check, every named fingerprint class in REPO_STAGING's
   private area to zero, except the one item in §4.1.
5. Audited all five other public repositories read-only (§3), and ran
   Airlock's own `scrub_check.sh` (PASS).
6. Did **not** run `bash stage.sh` (the pushing form) — "clean" was
   never printed, so per my own gating instruction, nothing was
   pushed. REPO_STAGING's tip is unchanged: `6e0eb55`.

**Awaiting the owner** (each needs his judgement, not mine):
1. §4.1 — the real, live `verify_row_graph_v4.js` "the owner" comment that
   `stage.sh`'s text-file gate cannot see; needs either a `stage.sh`
   fix or a private-source edit before "clean" is real.
2. §4.2 — whether the six coincidental PNG byte-matches are an
   acceptable permanent exception, and if the check step should gain
   the scrub step's own binary-skip logic (which would also affect
   §4.1).
3. §4.3 — three patterns (podman/Unraid/MAC) added with no real
   instance yet to prove them against.
4. §4.4 — disk sizes: no safe pattern found; what wording should it
   look for.
5. §4.5 — whether the OpenJDK build string's embedded `26.04` needs
   its own careful pattern, or stays inside the kept toolchain string.
6. §4.6 — the pre-existing `<tower-user>␉<tower-user>` no-op line,
   left untouched.
7. §3's Ourobrowser (180 `the owner` / 130 `~/Programming`), ZSpectralCompression
   (218 `the owner` / 192 `~/Programming`), and PseudoCoup (35 `the owner` / 51
   `~/Programming`, including a tracked `.claude/launch.json`) hits —
   audit only, per the brief; what to do about them is explicitly not
   this task's call.
8. §3's note on Airlock's `Containerfile`/`up.sh` Ubuntu-version
   mentions — my reading is that these are the tool's own necessary
   build-image documentation, not a personal fingerprint; asking the owner
   to confirm rather than deciding it silently.
