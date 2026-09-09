---
id: hq.exchange.progress
status: living
---

# PROGRESS — exchange

- 2026-07-31: extracted here from the two project CORE_0 files, which
  each carried their own copy. the copies differed: the "cycle
  closes" text differed by one word ("this project" vs "PseudoCoup"),
  and the two-artifact statement was worded differently in each, with
  nothing to say which was authoritative. that is the "two parallel
  stores of one fact" failure recorded in
  `PseudoIR/Agent_Memory.md` §6.
- 2026-07-31 **done** (the owner: "yeah add them"): both project CORE_0
  files now open their "the other project" section with a line
  naming this node as where the exchange and the cycle are settled,
  and stating that a project copy disagreeing with HQ's is the
  project copy that is wrong. edited:
  `PseudoCoup_v6/Planning/CORE_0.md` and
  `PseudoIR/Planning/CORE_0.md`.
- consequence to watch: those pointers are cross-repo paths, so
  renaming this node now breaks two files in two other repos. that
  is the first concrete case for the cross-project consistency check
  under discussion — a dangling cross-repo node reference is exactly
  what it would catch.
