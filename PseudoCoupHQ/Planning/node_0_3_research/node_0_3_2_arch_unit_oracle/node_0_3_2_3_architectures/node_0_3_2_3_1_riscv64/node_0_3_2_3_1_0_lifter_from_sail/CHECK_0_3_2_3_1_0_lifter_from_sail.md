---
id: hq.research.arch_unit_oracle.architectures.riscv64.lifter_from_sail.check
---

# CHECK — 0_3_2_3_1_0_lifter_from_sail

Node `hq.research.arch_unit_oracle.architectures.riscv64.lifter_from_sail`. Status `draft`.

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

*none — this is a leaf.*

### verdict

**NOT COMPLETE** — status is not `settled`.

## check 2 — the regeneration test (the owner, 2026-09-13)

    delete the generated table; run the lane; the table is back,
    byte-identical or its diff named. A person typing a row anywhere
    in the path fails this check.

## check 3 and beyond

None yet.
