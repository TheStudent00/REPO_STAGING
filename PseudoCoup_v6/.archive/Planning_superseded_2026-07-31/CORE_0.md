---
id: pcv6.planning
level: 0
status: settled
settled_by: the owner
supersedes: pcv6.planning.master_plan_flat
---

# CORE 0 — PseudoCoup_v6 Planning

Planning root (`node_0`) under the PlanningPlan framework
([PROTOCOL](../../PlanningPlan/framework/PROTOCOL.md)). the owner's
original Level-1 draft is preserved verbatim in
[SUPPORT_0_dee_frame.md](SUPPORT_0_dee_frame.md). The one-page
capability view is
[SUPPORT_0_dashboard.md](SUPPORT_0_dashboard.md).

## Core objectives

- **Ultimate**: greatest amount of automation of transpiling and
  slicing of languages — in particular the 12.
- **Intermediate**: Rust (LLVM) transpiling and slicing.
- **Current program**: construct the tools (composition from the
  lineage's best components; generalize then specialize;
  tree-sitter as the foundation of all ingress).

### Note on the ultimate goal (the owner, 2026-07-28)

The circumstance the mostly-automated system is meant for is
compiler transpiling + slicing + inserting. The project is
designed to produce a Hub that all of the 12 languages (and
potentially more) can be converted into without violating the
intentions of the source scripts; the Hub is meant to satisfy
those intentions. Although the intentions are reasonably small in
number, if the intention-landscape changes, there needs to be
something in place to allow the repo to keep up with churn. A
mostly automated system can update the repo within a short amount
of time — it makes the repo more resilient and capable of being
maintained by a handful of developers, potentially even one.

## Core components

transpiler · intentions · lessons · polyfill · slicer — defined in
[AgentMemory/00_project.md](../AgentMemory/00_project.md); settled
decisions in [AgentMemory/02_decisions.md](../AgentMemory/02_decisions.md).

## Nodes

- [node_0_0_tools](node_0_0_tools/CORE_0_0_tools.md) — the tools
  program: T1–T6 in dependency order; the ledger and transpiler
  upgrades carry the deepest detail. **Built through T6
  extraction.**
- [node_0_1_research](node_0_1_research/CORE_0_1_research.md) —
  the research queue feeding the tools (R1–R5 complete).
- [node_0_2_hub](node_0_2_hub/CORE_0_2_hub.md) — the Hub itself as
  a deliverable: intention objects, borders, surface spelling.
  Assembles after T6 insertion. *(planning depth added 2026-07-29)*
- [node_0_3_application_rust_llvm](node_0_3_application_rust_llvm/CORE_0_3_application_rust_llvm.md)
  — the intermediate goal as a campaign: MIR→IR front half, the
  ISel gap, the all-LLVM chain, architectures. *(2026-07-29)*
- [node_0_4_application_ingress](node_0_4_application_ingress/CORE_0_4_application_ingress.md)
  — the OTHER half: converting the 12 languages' application
  programs into the Hub (dashboard row 5, previously unplanned).
  *(2026-07-29)*

## Planning frontier

The tools line (node_0_0) is built through T6 extraction and its
sub-tree is deep. The three nodes above (Hub, Rust/LLVM
application, application ingress) are planned to level 2–4 but
UNBUILT — they are the frontier. All their nodes are `status:
draft` pending the owner's review; none supersedes a settled decision,
each only extends the frame downward.
