---
id: hq.research.arch_unit_oracle.architectures.riscv64.language_axis.check
---

# CHECK — 0_3_2_3_1_2_language_axis

Node `hq.research.arch_unit_oracle.architectures.riscv64.language_axis`. Status `draft`.

## check 1 — completeness

    complete(node) = status is `settled` AND every sub-node complete

**Is this node settled?** **no** — `status: draft`

**Sub-nodes:** *none — this is a leaf.*

### verdict

**NOT COMPLETE** — status is not `settled`.

## check 2 — agreement is never proof

    an interpreted row is `agreed` / `disagreed` / `refused` / `timed out`;
    the word proved never appears on an interpreted row.

## check 3 — the population stated

    every table row reads "N of 255".
