# Task bank1 — the polyfill library as banked certificates: bank every proved pair on disk, restore the 19, and turn the loop into delta plus audit

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it. Then the five
loop briefs `task_ap1_brief.md` … `task_ap5_brief.md` beside this file and
their logs (`DevComms/log_243`, `244`, `245`, `246`, `249`), and the stores
`.../emulation/autopoly/autopoly_runs.jsonl`, `autopoly2_runs.jsonl`, …,
`autopoly5_runs.jsonl` with their `src*/` folders. Instance `bank1.conf`
(copy from `PUBLIC/Airlock/instances/bank1.conf`). Artifact folder:
`.../emulation/autopoly/`; new files `certificates.jsonl`, `bank.py`, and
the driver change; lanes under `lanes_bank1/`. Task ex2's closer may still
be writing `expand2_*` in the same folder when you start: do not touch
those files; change the loop driver LAST, after `expand2.md` exists.

## 1. The finding this task carries out (the owner, 2026-09-10, from a branch conversation)
The passes re-derived every emulation from the cell's term every time, so
a renderer change made the same cell yield a different artifact, and the
old proof no longer described what had just been built. Counted on the
STRICT reading (every written place, flags included), proved (cell,
target) pairs per pass were 330 / 434 / 465 / 521 / 504, their union 523;
19 pairs proved by some pass are not proved by the last, five of them
cells on all four through pass 4 and not in pass 5 (`and`, `cmp` ×2, `mov`,
`or`, all `imm_gpr` — exactly what pass 5 changed). Passes 2–5 spent 75%
to 98% of their runs re-doing known results, and every change cost a full
pass, three guards, a report and a verifier before its effect was visible.
A proof is a certificate about ONE artifact — the term text, the rendered
source, the compiler and its flags, the carved body, the verdict — and a
certificate cannot regress; only the machinery can fail to reproduce it.
The deliverable is the LIBRARY, one proved emulation per (cell, target),
and it only grows.

## 2. The bank
`certificates.jsonl`, one line per (cell key, target, written place):
term text; rendered source (path and sha256); compiler version and flags
LITERAL; carved body bytes and text; gate verdict in z3's words with the
region sentence when one applied; the pass and lane that produced it;
`kind`: `proved` (unsat), `proved_under_caller_extension`, `agreed`
(an interpreted target's whole-sample agreement, with the sample count),
`sat` (with the counterexample), `undecided`, `refused` (with the cause).
Bank every run of every pass on disk, preferring for each key the
strongest kind, ties by the earliest pass; keep every weaker or later
entry too, marked `superseded_by`. Report: pairs banked per kind, the 523
strict proved pairs recovered (name the 19 restored with their pass), and
the headline in THREE readings, stated as three every time from now on:
strict (every written place), destination-only, and CORPUS-NEEDED —
destination proved AND flags proved wherever the corpus's attestation
shows a consumer reading that cell's flags (the flag-pair rows the model
table counts), flags ignored where no consumer ever does. Cells on all
four (and all five) under each reading, with rows and shares.

## 3. The loop, reshaped: delta plus audit
`autopoly.py` gains a `--bank` mode that is the default from now on: the
pairs attempted are (a) every (cell, target, place) with no certificate of
kind `proved`/`agreed`, and (b) an AUDIT sample: 5% of certified pairs
chosen by `random.Random(<date>)`, re-derived from the term; a re-derived
verdict that differs from its certificate on IDENTICAL inputs (same term
text, same source sha256, same compiler and flags) is an ALARM that stops
the pass and names the pair — a differing artifact (the renderer changed)
is recorded as a new entry beside the old one, never replacing it. The
count is monotone by construction: report per pass "certified before /
attempted / newly certified / audited / alarms". Ceilings, memory,
bookkeeping as ap1. Then run ONE pass in this mode on the four compiled
targets (+ cpp) to show its cost: expect a few hundred runs, not 1,012.

## 4. Deliverable
`bank.py`, `certificates.jsonl`, `autopoly.py --bank`, `bank1.md` (§2's
tables, the 19, the three readings, §3's pass and its cost against a full
pass); guard over every json/jsonl; log (next free number, check right
before writing); verifier lane; PROGRESS on the autopoly node — and one
dated line in the research node's PROGRESS naming the design error and
its cost, in the coordinator's words above; sync-back; instance down.
Memory bound 6g, sample 20, peak RSS, abort `ABORT_MEMORY_BANK1`. No
shared-file change authorised. Never delete anything under
`<runs>/` or `PUBLIC/Airlock/`. Reply with the banked counts
per kind, the 19 restored, the three headline readings, the delta pass's
cost line, the tally, the two lists.
