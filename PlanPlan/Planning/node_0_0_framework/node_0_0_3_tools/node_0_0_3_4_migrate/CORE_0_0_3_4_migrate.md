---
id: pp.framework.tools.migrate
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: migrate
    path: Planning/node_0_0_framework/node_0_0_3_tools/node_0_0_3_4_migrate/CORE_0_0_3_4_migrate.md
super_node:
    name: tools
    path: ../CORE_0_0_3_tools.md
sub_nodes:
    - name: migrations
      designation: code (variable)
      realize: false
    - name: plan
      designation: code (function)
      realize: false
    - name: apply
      designation: code (function)
      realize: false
---

# CORE 0_0_3_4 — migrate

## sub_nodes

- migrations — code (variable) *(realize: false)*
- plan — code (function) *(realize: false)*
- apply — code (function) *(realize: false)*

## definition

applies one named change across every repo that uses the framework —
addresses, filename grammar, section headings — as one dry-runnable
operation rather than a hand pass over hundreds of files.

`generate_nodes.py --rename-field` covers one frontmatter key. This
covers everything wider than that. A migration that has to be applied
by hand is a migration that ends up half-applied, and a half-applied
migration is worse than none: the checks then describe a state nobody
intended.

## design

```
class Migration
	attributes:
		name
		TEXT_RULES
		NAME_RE
	methods:
		rename
		rewrite
```

- `Migration.name` — the subcommand a caller types.
- `Migration.TEXT_RULES` — the anchored substitutions applied inside
  files.
- `Migration.NAME_RE` — what a file or folder name must match to be
  renamed.
- `Migration.rename` — new basename for one name, or nothing.
- `Migration.rewrite` — new text for one file's contents.

The engine around them is three `realize: false` parts, designed here
because each is a paragraph rather than a branch:

- **`migrations`** — the registry mapping a subcommand name to its
  Migration. Append-only in practice: a migration already run stays
  listed, because a second repo adopting the framework later has to
  run the same sequence.
- **`plan`** — walks the repos and returns four lists: text edits,
  file renames, folder renames, and code files MATCHED but not
  touched. It writes nothing, which is what makes the dry run the
  default rather than a flag.
- **`apply`** — performs those lists in a fixed order: text, then
  files, then folders deepest-first. The order is the property that
  makes a partial run describable — a parent folder renamed before
  its children would orphan them.

## rules

- **Dry run is the default.** Same contract as `generate_nodes.py`.
- **Every pattern is anchored to a grammar prefix** — `node_`,
  `CORE_`, `CHECK_`, `SUPPORT_`, or a `CORE <chain>` heading. An
  unanchored substitution over hundreds of files cannot be reviewed,
  and prose containing a number that looks like an address is common.
- **Code is reported, not rewritten, unless `--include-code`.** The
  report is the review step. It earned itself on the first real run:
  reading the list showed one entry was a live constant
  (`PseudoCoup_v5/hub/__init__.py`'s `_HUB_PLAN`) that would otherwise
  have dangled.
- **Bare constants never match, in either mode.** `return "1"`,
  `CHAIN = "1_0"`. These need a person's judgement, so they stay
  invisible on purpose, and the tool's docstring says to grep for them
  when a migration changes what they mean.
- **A migration is not undone by a second migration.** Reversing one
  means writing the inverse and running it, so that both directions
  are recorded and reviewable.

## notes

- built 2026-08-05 at the owner's request, immediately used for
  `renumber-root` — see this node's PROGRESS and the framework node's.
- the tool holds sequencing and text rules only; it knows nothing
  about the planning grammar beyond the four prefixes, and does not
  import `planning_model`. That keeps it usable for a change the
  grammar has not anticipated, which is the case it exists for.
