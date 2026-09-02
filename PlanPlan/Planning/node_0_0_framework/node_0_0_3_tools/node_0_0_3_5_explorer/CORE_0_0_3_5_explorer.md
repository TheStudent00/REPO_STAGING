---
id: pp.framework.tools.explorer
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: explorer
    path: Planning/node_0_0_framework/node_0_0_3_tools/node_0_0_3_5_explorer/CORE_0_0_3_5_explorer.md
super_node:
    name: tools
    path: ../CORE_0_0_3_tools.md
sub_nodes:
    - name: to_data
      designation: code (function)
      realize: false
    - name: build
      designation: code (function)
      realize: false
    - name: serve
      designation: code (function)
      realize: false
---

# CORE 0_0_3_5 — explorer

## sub_nodes

- to_data — code (function) *(realize: false)*
- build — code (function) *(realize: false)*
- serve — code (function) *(realize: false)*

## definition

a card explorer for one planning tree: one card per node, clicked open
in place to reveal that node's files and its sub-node cards, indented.

it answers a different question from `render_plan`. that one renders a
plan to READ, top to bottom. this one is for NAVIGATING — start
collapsed, open only the branch in hand, the way a file manager is
used (the owner, 2026-08-05).

## design

```
to_data(node)   -> dict
build(root)     -> html
serve(root, port)
```

- `to_data` — the tree as plain data: name, id, designation, status,
  definition line, the files in the node's folder by role, and
  children. `realize: false` register entries become cards too, marked
  — they are structure the register states, and omitting them would
  show less than the plan says.
- `build` — that data as one self-contained page: JSON embedded,
  script inline, no CDN, no framework, no build step.
- `serve` — an `http.server` that calls `build` on EVERY request.

## rules

- **A `file://` page cannot run a program on the machine showing it.**
  That is a browser boundary, not a gap to engineer around, and it is
  why "auto-updating HTML" has exactly two honest forms: regenerate a
  snapshot, or serve it and let a refresh be the re-scan. Both are
  offered; neither pretends to be the other.
- **Vanilla script only.** No CDN and no library — a page that fetches
  something is a page that breaks offline, breaks when a version moves,
  and stops being one file. The interaction here is showing and hiding
  elements, which needs nothing more.
- **The snapshot is written where the caller says**, never into a
  planning tree. An `.html` inside a node folder would be a stray by
  the grammar (§1), so writing one there breaks the checks.

## notes

- built 2026-08-05 at the owner's request: "id also like an updated project
  node explorer (like file system/management explorer) ... each node
  represented as a card. if a card is selected, it can expand to reveal
  indented cards of the sub_nodes. maybe also revealing the files
  contained within that clicked card."
- `--serve` was verified to re-scan rather than cache: with the server
  running, a node folder was created and the next request showed 5
  nodes where the previous showed 4, without a restart.
