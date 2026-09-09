# PlanPlan

The study of **ontology evolution in research project development**
— and the home of the planning framework used across projects.

## Thesis (the owner, 2026-07-28)

Research projects develop ontologies — the named components, terms,
and structures a project thinks in — and those ontologies warp over
time. With enough projects under version control, the warping
becomes observable: VCS history + file structure + extracted
planning instances form a dataset. Plans written here carry prose
for human interpretation AND structured metadata that can be
rigorously analyzed. Keeping prose well-structured works in our
favor: the plan is simultaneously a working document and a data
point.

## What lives here

- `framework/` — the planning framework: protocol, document
  templates, metadata schema. Projects conform to it as their
  planning template; PseudoCoup_v6 is the first conforming
  instance (its `Planning/` restructured 2026-07-28).
- `analysis/` (future) — tools for analyzing VCS histories and
  file structures of conforming projects, and for extracting
  planning instances into the dataset.
- `instances/` (future) — extracted planning snapshots from
  conforming projects, the raw material of the ontology-evolution
  study.

## Working conventions

Same as the PseudoCoup repos: commit via
`bash PlanPlan/git_commit_push.sh` (message from
`DevComms/next_commit_message.txt`); repo created private via
`bash PlanPlan/create_github_repo.sh`.
Terminology: no socio-familial constructs for object relationships
— super-sub / higher-lower, sub-nodes, co-nodes (full replacement
lexicon in the communication protocol §1).
