---
id: pcv6.on_scripts
level: 3
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_2_0_0 — on scripts

## metadata

- **id:** pcv6.on_scripts
- **level:** 3
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

driving the api over an ordinary program

a program in one of the 12 languages goes through the ledgerer and
the transpiler into the hub, and back out to another language. it is
the worked example of the api: one call in, converted program out.

the compiler case is not here. putting a language's semantics into
the hub is PseudoIR's work, planned at
`PRIVATE/PseudoIR/Planning`, not a use of the finished thing.

## support

- [SUPPORT_behavioral_oracle.md](SUPPORT_behavioral_oracle.md) — the
  acceptance that matters here is behavior, not byte-identity
