---
id: pcv6.on_scripts.support.behavioral_oracle
status: projected
---

# SUPPORT — behavioral oracle

projected 2026-07-30 from the previous plan, now archived at
`~/Programming/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_4_application_ingress/node_0_4_2_behavioral_oracle/CORE_0_4_2_behavioral_oracle.md  (288 words)
verdict: clean
changed: nothing

---

# CORE 0_4_2 — Behavioral Oracle

The acceptance that actually matters for application ingress: does
the hub program BEHAVE like the source program? Byte-identity
proves compiler-vocabulary reproduction; it cannot prove that an
ingressed application means the same thing. Behavior can.

## The harvest (the lineage's hardest, most valuable asset)

v0's `oracle.py` + `fuzz.py`
(`~/Programming/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/`,
verified green in place by R3): transpile the source language's
OWN TEST SUITE alongside the program, run both sides, compare
outputs — the compiler/program authors' own intent statements
become the test. v0 got the Kotlin suite passing in Python
160/160 this way. WFL's own planning named this the Phase-4
target it never reached ("both prior efforts drowned at
behavior-proof, not translation").

## Why it is a distinct node and not just "a test"

- It requires RUNNING the source language (a toolchain), so it is
  host-dependent and cannot run in the sandbox unaided — it needs
  the same staged-script pattern as R1/R3 for host execution.
- It is a differential fuzzer, not a fixed grid: deterministic
  input generation, both sides executed, outputs diffed. Building
  it well is a real project, correctly its own node.

## Acceptance shape

- For a source program WITH tests: transpiled tests pass in the
  hub (the v0 result reproduced PCv6-side).
- For a source program WITHOUT tests: the fuzzer generates inputs,
  runs source and hub versions, diffs — divergences reported by
  cause, never swallowed.

## Sequencing

Last of the application-ingress nodes; needs a working ingestor
(node_0_4_0) and intent capture (node_0_4_1) to have something to
test. But its DESIGN should be settled early because it defines
what "ingress correct" even means — recorded here so the ingestor
work aims at a behavioral bar from the start, not a structural one.
