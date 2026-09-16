---
id: hq.research.lean_proof_path_resistant_to_churn.language.check
---

# CHECK — 0_3_3_4_language

Node `hq.research.lean_proof_path_resistant_to_churn.language`. Status `draft`.

## check 1 — completeness

> a node being complete means its sub-nodes are complete. if a node is
> a leaf with no sub-nodes, it is complete.
>
> there is a difference between an intentionally empty list vs a list
> that wont be empty eventually. but we have things like "draft"
> codifications to indicate an incomplete node.
>
> — the owner, 2026-07-31

    complete(node) = status is `settled` AND every sub-node complete

**Is this node settled?** **no** — `status: draft`

**Sub-nodes:**

- `compile` — not settled
- `compiler_corpus` — not settled
- `operator_for` — not settled
- `render` — not settled
- `compose_at_width` — not settled

### verdict

**NOT COMPLETE** — status is not `settled`.

## check 2 — nothing hand-written that breaks with churn

the owner, 2026-09-14: "fully built out proving nothing is made by-hand that
breaks with churn." The test, run over this node's code once it exists:

- the spelling-ban checker `PRIVATE/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py`
  over every file this node writes: no operator token, no mnemonic, in
  any key or grouping
- a grep of this node's code for a mnemonic, a compiler version string
  or a language release: zero hits, except the one invocation line of
  `Language.compile`, which is plumbing and declared as such
- the churn rerun of `the_run.churn_tests`: this node's code is not
  edited when the compiler or the model changes

**Verdict:** pending — the code for this node does not exist yet.
