# Task ap3 — AutoPoly loop, third pass: the vector ARRIVAL as two halves, the x87 cells through c's 80-bit holder, the blocked check un-blocked, and one fix measured alone

Law: `~/Programming/PseudoCoupHQ/Research/LAW.md`, ALL of it including the
tower section. Then `task_ap2_brief.md` and `task_ap1_brief.md` beside this
file and their logs `DevComms/log_244` (ap2: the change table, §"Awaiting
the owner"), `log_243`; the driver `.../emulation/autopoly/autopoly.py` and
`.../emulation/handful/handful.py` as ap2 left them; the four renderers;
`Research/op_pipeline/lean/model_translate.py` (`load_rows`). Instance
`ap3.conf` (copy from `~/Programming/Airlock/instances/ap3.conf`; mounts
`sandbox-persist` read-only). Artifact folder: `.../emulation/autopoly/`,
writing `autopoly3_*`; lanes under `lanes_ap3/`.

## 1. What this is
ap2 left 66 cells proved on no target. Of the causes that remain, these are
OURS and mechanical; the arrival-contract cells (38 places, 12 cells) and
every `sat` stay untouched, awaiting the owner. One cause = one fix in the layer
that owns it; each measured on its own cells before the loop re-runs.

## 2. The fixes
| cause in ap2 | runs / rows | fix | where | guard |
|---|---|---|---|---|
| "vector arrival used beyond its low lane" — a whole 128-bit ARRIVAL has no holder | 40 / (from log_244) | the arrival side of ap2's fix 3: a 128-bit arriving register becomes TWO 64-bit parameters (low, high) in the plan, and the term's reads of it are rewritten to `Concat(high, low)`; the gate aligns the two halves against the arrival's two 64-bit slices | driver | the four vector cells of the handful and every ap2-proved vector cell unchanged |
| the 32 x87 cells at `key_width` 80 (ap2's "no setter", correctly not setter cells) | 128 / 6,284 | c and cpp on x86-64 have an 80-bit holder, `long double`; PROBE it first (a `long double` add compiled at ship flags, body pasted: does clang emit the x87 opcode?), and if the probe lands, render the x87 cells' lane as `long double` on c and cpp by the term route; rust, go and swift have no 80-bit holder: their rows are REFUSED with that sentence, by nature | driver (c/cpp only) | the probe LITERAL; nothing else moves |
| `model_translate.py check` stops on `KeyError: 'mnemonic'` in `load_rows` (open since log_237; ap2 could not re-derive `check_L2`) | — | `load_rows` reads `row["mnem"]` (with `mnemonic` accepted as a fallback for the old artifact if you want; say so). Authorised: one line in a shared file | `model_translate.py` | run `check` and paste its tally: 259 rows, 172 STATED (153 + 19 DISCREPANCY), 87 REFUSED expected; a different number is a FINDING |
| h2's normalise-before-render, moved alongside five other fixes in ap2, never measured alone on the 1,012 | — | run the loop once with that switch OFF and once ON, all else as ap2; report the runs whose rendered source differs and whose verdict differs | driver flag | the count; if zero, say the fix is a measured no-op at scale and leave it ON |

## 3. The loop, again
Exactly ap2's loop over the same cells, writing `autopoly3_*`; then the
per-target table, the all-four count and share (ap1 → ap2 → ap3), the
change table per cause (ap2 → ap3), and the `sat` list with regions.

## 4. Deliverable
`autopoly3.md` with the tables; the probe; the `check` tally; guard over
every json; log (next free number, check right before writing); verifier
lane; PROGRESS on the autopoly node; sync-back; instance down. Memory:
bound 6g inside the cap, sample the first 20 runs, paste peak RSS, named
abort `ABORT_MEMORY_AP3`. Stop rules per LAW; never delete anything under
`~/AirlockRuns/` or `~/Programming/Airlock/` on either machine — a lane
name that collides gets a new name. Reply with the per-target table, the
all-four count and share (three passes), the change table, the x87 probe
result, the `check` tally, the fix-1 measurement, the tally, the two lists.
