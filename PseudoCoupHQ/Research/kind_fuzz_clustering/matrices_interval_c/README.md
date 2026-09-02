# interval matrices -- ruling C (breaking the diagonal)

ADDITIONAL rows on top of `../matrices_interval/`, which is not modified.  Same ten columns, same canon rules, same `;` vector separator.

- `IV32:<a>|<b>:shift` -- C1, `x_k OP x_{(k+1) mod 32}`.  No new values; the pairing moved.
- `IV32:<a>|<b>:comp1` -- C2, `op(op(x,x'), op(x,x'))`.  The composed operands are the operator's own diagonal outputs and appear in the two input vectors; `lhs_holder`/`rhs_holder` still name the SOURCE operand holders.

A position whose composed OPERAND declined was not run and carries a decline token, so ruling B excludes it from every comparison.
