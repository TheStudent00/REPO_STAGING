---
id: hq
level: 0
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: hq
    path: Planning/CORE_0.md
    repo: PseudoCoupHQ
    remote: https://github.com/TheStudent00/PseudoCoupHQ.git
super_node: null
sub_nodes:
    - name: projects
      path: node_0_0_projects/CORE_0_0_projects.md
    - name: exchange
      path: node_0_1_exchange/CORE_0_1_exchange.md
    - name: conventions
      path: node_0_2_conventions/CORE_0_2_conventions.md
    - name: research
      path: node_0_3_research/CORE_0_3_research.md
---

# CORE 0 — PseudoCoupHQ

## metadata

- **id:** hq
- **level:** 0
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

- [projects](node_0_0_projects/CORE_0_0_projects.md) — what each repo in the line is, and what stage it is at.
- [exchange](node_0_1_exchange/CORE_0_1_exchange.md) — what crosses between PseudoCoup and PseudoIR, and why the bootstrap cycle stops.
- [conventions](node_0_2_conventions/CORE_0_2_conventions.md) — the rules the work is done under, and where each one lives.
- [research](node_0_3_research/CORE_0_3_research.md) — The master plan of PCHQ's research: the one node that states the objective every research project serves, assigns each project its contribution to that objective, orders the work between them, and holds the rulings all of them share.

## definition

the meta-planning root over the PseudoCoup line. it holds what is
true ACROSS the projects, so no project has to hold a copy of it.

this tree is deliberately shallow. detail belongs in the project
plans; what belongs here is the frame they all sit inside, stated
once, at a level a reader can finish in a minute before descending
into any of them.

## the repos

three, and these are the whole of it.

- `~/Programming/PseudoCoup_v5` — being gutted and rebuilt as the
  Frankenstein transpiler and ledgerer. live for new work.
- `~/Programming/PseudoCoup_v6` — the tool to transpile from source
  languages into the hub. live for new work.
- `~/Programming/PseudoIR` — the system the hub is constructed with.
  live for new work.

HQ reads and copies from anything in `~/Programming` it needs. only
the three above take new work from here.

*meta-note, not a repo entry: this tree conforms to the planning
framework in `~/Programming/PlanPlan`, and the work is done under
the communication protocol in `~/Programming/DevComms`. neither is
part of the line and neither is HQ's to change. access to both is per
request.*

## support

- [SUPPORT_planning_trees.md](SUPPORT_planning_trees.md) — why there
  is more than one planning tree, what this one is and is not, how
  authority flows between them, and why PseudoCoup_v5 has none

## HQ is the authority for the shared frame

the two-artifact exchange and the closing cycle are stated in
[exchange](node_0_1_exchange/CORE_0_1_exchange.md). the project plans
may still say them — the owner, 2026-07-31 — but they say them AS
DEPENDENTS: HQ is where the statement is settled, and a project's
copy that disagrees with HQ is the project's error to fix, per the
framework's governance rule that a sub-document may refine its
super-document and never contradict it.

that is the point of extracting them here. before HQ existed the
cycle text lived twice, in
`~/Programming/PseudoCoup_v6/Planning/CORE_0.md` and
`~/Programming/PseudoIR/Planning/CORE_0.md`, differing by a word,
with nothing to say which was right.
