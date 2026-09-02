"""Shared statement-hoisting mechanism (the R4 core).

ONE implementation, consumed by EVERY synthetic_stmt lowering. A synthetic_stmt
lowering is one where the op has no expression form in the target (e.g. Go's
null_coalesce: the only honest realization is an `if` statement, which cannot sit
inside a larger expression). To place such an op where an expression is required,
we HOIST it: pull the statement(s) out to run BEFORE the enclosing statement, and
leave a plain variable in the expression's place.

    hoist(expr_node, emit_prelude) -> (prelude_statements, replacement_expr)

        prelude_statements : list[str]  -- target statements to emit, in order,
                                           before the enclosing statement.
        replacement_expr   : str        -- the expression that stands in for the
                                           hoisted op (usually a fresh temp name).

The contract every synthetic_stmt lowering obeys:
  1. Sub-expressions are hoisted FIRST (depth-first), so their preludes run before
     this op's prelude -- preserving left-to-right evaluation order.
  2. Preludes ACCUMULATE in encounter order; the final replacement expression uses
     only temp names, never a re-evaluated sub-expression.
  3. One fresh temp name per hoisted op (a monotonic counter), so two hoists in one
     expression (the double-hoist test) never collide.
"""


class Hoister:
    def __init__(self, prefix="_h"):
        self.prelude = []      # accumulated target statements, in emit order
        self._n = 0
        self._prefix = prefix

    def fresh(self):
        name = f"{self._prefix}{self._n}"
        self._n += 1
        return name

    def hoist_stmt(self, stmt_lines, result_expr):
        """Register statement lines to run in the prelude, binding `result_expr`
        into a fresh temp; return the temp name to use in the enclosing expression.
        `stmt_lines` is a list of target lines that must run before the temp is read.
        """
        tmp = self.fresh()
        for ln in stmt_lines:
            self.prelude.append(ln.replace("@TMP@", tmp))
        return tmp, result_expr
