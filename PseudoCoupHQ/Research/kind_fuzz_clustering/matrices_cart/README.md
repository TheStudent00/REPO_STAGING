# cartesian matrices

The settled probe design of 2026-08-21.

- **level 1** `y = op(x0, x1)` for ALL ordered pairs from a shared set `X`.
- **level 2** `z = op(op(x0,x1), op(x2,x3))` with all four operands from a subset `X'`.  The two intermediates are never enumerated, deduped, capped or unioned -- they exist inside the expression.

One CSV per `language.operator.L<level>`.  One row per (level, operator, lhs holder, rhs holder); the probe axis lives inside the row as `output_canon_vector`.  Operand sets are named by `x_set_a` / `x_set_b` and recorded in full in `index.json`, with the probe-index rule, so every position is reconstructible exactly.

A value a holder cannot represent is ABSENT from that holder's set -- never coerced.  A slot with no value carries `REFUSE`, `RAISE:<kind>` or `ABORT`; nothing is padded and no slot is ever empty.
