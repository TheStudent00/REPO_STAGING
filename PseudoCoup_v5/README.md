# PseudoCoup v5

Experimental stage of the PCv7 program: a Python-central hub language
(disciplined Python + qualified vocabulary) with lossless egress to 12
targets, ingress modes, and a border grammar.

## Version roadmap

- **v5 (this repo, experimental):** basis audit, divergence suite,
  self-hosted polyfills, canon selection. Prove the two-layer program.
- **v6 (experimental):** ingress modes, border grammar implementation,
  origin qualifiers in the parser, egress-coverage analyzer.
- **v7 (polished):** the consolidated language. Policies frozen from
  [Designing/PCv7_policy_decisions.md](Designing/PCv7_policy_decisions.md).

## Layout

```
DevComms/     project memory. append-only logs with correction
              history; project_state.md is the reorientation point.
Designing/    settled analysis and decisions. generated reports
              live beside their generators (edit data, rerun).
Research/     code that runs. each experiment in its own folder
              with expected outputs recorded.
```

## Rules

- moves, not copies: one canonical home per document.
- generated files are never hand-edited.
- logs preserve why a position fell, not just the final position.
- a policy is formal when a runnable artifact could falsify it.

## Start here

1. [DevComms/project_state.md](DevComms/project_state.md) — where we are
2. [Designing/PCv7_policy_decisions.md](Designing/PCv7_policy_decisions.md) — the 20 policies
3. [Designing/intention_tables.html](Designing/intention_tables.html) — the evidence tables
