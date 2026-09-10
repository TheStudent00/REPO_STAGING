# Task ap6 — one versioned driver: the task-name gates stripped, consumers over every attested setter, the lookup with holders, and re-attempts by code version

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it (waits in short
calls). Then `task_bank1_brief.md` and its log `DevComms/log_253` (the bank,
bank mode, its §"Awaiting the owner" items 1–2), `task_hub2_brief.md` and
`log_254` (§"Awaiting the owner" items 1–3), `log_252` §6, the driver
`.../emulation/handful/handful.py` (its nine `use_task_*` gates and
`fixes_are_on`), `.../autopoly/autopoly.py` (bank mode), the bank
`certificates.jsonl`. Instance `ap6.conf` (copy from
`PUBLIC/Airlock/instances/ap6.conf`; mounts `sandbox-persist` ro).
Artifact folder: `.../emulation/`; lanes under `autopoly/lanes_ap6/`.

## 1. What this is (the owner, 2026-09-10)
"It better actually be working and not be you editing things so it's
effectively you solving everything by hand." The driver's contract rules
are general (no branch keyed on an opcode name exists — checked), but they
are switched on by TASK NAME, nine gates, so that older runs reproduce
verbatim. That is provenance done in the worst way. This task makes ONE
driver with no task gates, records the driver's and each renderer's code
version (sha256 of the source files) on every certificate, and makes
re-attempts depend on that version rather than on a task label.

## 2. The changes, each with its guard
| change | where | guard |
|---|---|---|
| every `use_task_*` gate and `fixes_are_on` removed; every contract rule unconditional; `autopoly1.py` (ap1's frozen copy) stays as the reproduction of log_243 only | `handful.py`, `autopoly.py` | the bank's audit at 100% of certified pairs ONCE (every certificate re-derived): a differing verdict on identical inputs is an ALARM and a STOP; a differing artifact (the source changed because a rule now applies) is recorded beside the old certificate |
| each flag consumer rendered over EVERY setter cell the corpus attests before it (m1b's flag-pair rows; 44 distinct pairs on go), not one setter at one width | driver | the 10 pair units hub2 served still prove; the count of pair-level certificates before/after |
| the primitive lookup's key carries the matched body's holders; an entry records its parameter holders; a truth-holder body is never matched to a non-truth cell | driver | hub1's five unusable entries become either usable (matched at the right holders) or refused by cause at the loop, not at the composition |
| re-attempt rule in bank mode: a `refused`/`undecided`/`sat` key is re-attempted only when the code version recorded on its certificate differs from the current one for that target; certified keys only through the audit sample | `autopoly.py` bank mode | the delta pass's cost against log_253's: runs and seconds |
| the gate's narrow-answer re-pose (hub2 item 3): when a body's answer is wider than the node's, compare on the node's width as the caller-extension re-pose does for arguments | driver (the check), not `gate.py` | `go/regen_146`'s verdict before/after |

## 3. Then one delta pass, and the three readings
Bank mode over the five compiled targets; the cost line; the three
readings (strict, destination-only, corpus-needed) at all four / five /
twelve, beside log_253's; the audit's alarms (expected 0). Certificates
gain `code_version`. Guard over every json/jsonl; log (next free number);
verifier lane; PROGRESS on the autopoly node; sync-back; instance down.
Memory bound 6g, sample 20, peak RSS, abort `ABORT_MEMORY_AP6`. No
shared-file change outside the emulation folder. Never delete anything
under `<runs>/` or `PUBLIC/Airlock/`. Reply with the gate
count before/after (expected 9 → 0), the audit's result, the pair-level
before/after, the cost line, the three readings, the tally, the two lists.
