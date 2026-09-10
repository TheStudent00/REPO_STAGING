# Task ex2 — the interpreted loop: every attested cell on the seven interpreted targets, by the check ex1 defined

Law: `PseudoCoupHQ/Research/LAW.md`, ALL of it. Then
`task_ex1_brief.md` beside this file and its log `DevComms/log_248` (§3
the sample rule LITERAL, §4 the 70-row handful, §5 the declines, the
"Awaiting the owner" on the JIT dumps — NOT this task's), `task_ap1_brief.md`
(the loop's bookkeeping: order by attested rows, one jsonl line per run,
resume by skipping), and the driver as task ap5 left it (ap5 runs before
this task; read its log). Instance `ex2.conf` (copy from
`Airlock/instances/ex2.conf`; mounts `sandbox-persist`
read-only — dart and .NET live there). Artifact folder:
`.../emulation/autopoly/`, writing `expand2_*`; lanes under
`handful/lanes_ex2/`.

## 1. What this is
the owner's loop over the interpreted half of `set_of_languages`: the 253
attested cells × {cpython, php, ruby, java, javascript, dart, csharp},
1,771 runs, by ex1's route (the cell's mapping rendered in the target's
own operators over its own value model) and ex1's CHECK exactly as stated
in log_248 §3 (the ordered sample with the edge values first, ≤ 20,000
points per place, declines counted under the target's own word, an
agreement is evidence and never a proof). Nothing new in method. A cell
the route cannot render is a result by cause.

## 2. Bookkeeping
Runs ordered by attested ledger rows descending; `expand2_runs.jsonl`,
one line per run, resume by skipping; per run: cell key; target; rendered
source path; sample size; agreements / disagreements / declines by word;
the FIRST disagreement LITERAL (inputs, the reference's value, the
interpreter's value); cause when refused. Interpreter time per run is
bounded: 60 s per run, a run past it is recorded `TIMEOUT` with the point
count reached (no new outcome name: `TIMEOUT` is the existing word for a
lane or a solver that ran out of room, and the LAW says a limit is a
flag: re-run those with 600 s once and record both).

## 3. Deliverable
`expand2.md`: (1) THE table per target — cells attempted / rendered /
whole sample agrees / any disagreement / refused / timed out — counts and
ledger-row shares; (2) the cells that agree on ALL SEVEN interpreters, on
all twelve targets (the five compiled proved + seven agreeing), counts and
shares, beside the all-four/all-five line; (3) EVERY disagreement, with
its point, since a disagreement is where an interpreter's value model
differs from the opcode's (python's unbounded int at the width mask, php's
int overflow to float, javascript's doubles and 32-bit operator coercion,
java's int/long); (4) declines by target and word; (5) refusals by cause;
(6) the handful's 70 runs reproduced inside the loop. Guard over every
json; log (next free number, check right before writing); verifier lane;
PROGRESS on the autopoly node and the remaining_languages node (append);
sync-back; instance down. Memory bound 6g, sample 20 runs, peak RSS,
abort `ABORT_MEMORY_EX2`. No shared-file change is authorised. Never
delete anything under `<runs>/` or `Airlock/`. Reply
with the per-target table, the all-seven and all-twelve lines, the
disagreement count with three examples, the tally, the two lists.
