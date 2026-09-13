---
id: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis.check
---

# CHECK — 0_3_2_3_1_1_arch_opcode_axis

Node `hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis`. Status `draft`.

## check 1 — completeness

    complete(node) = status is `settled` AND every sub-node complete

**Is this node settled?** **no** — `status: draft`

**Sub-nodes:** *none — this is a leaf.*

### verdict

**NOT COMPLETE** — status is not `settled`.

## check 2 — the untailored rule (the owner, 2026-09-13)

    no line of code this node produces would differ for `mulh` and
    for `add`. A change keyed by an opcode's name or kind fails.

## check 3 — the population stated

    every table row reads "N of M" with M the population the loop
    actually ran over.
