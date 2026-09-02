"""
ir.py -- the IR node vocabulary the demos shared, consolidated.

WHAT THIS IS
------------
Every prober demo (prober/u_namespace/demo_u_namespace.py, prober/destructure/
demo_destructure.py, prober/overloaded_ops/demo_overloaded.py, the P2 demos) built
its own little OpNode class, then re-declared the same handful of leaf shapes (a raw
literal/identifier, a binary operator, a call). This module is that vocabulary written
ONCE, so every emitter in emit/ reads the same node types.

There are two kinds of node:

  Raw        -- a leaf reproduced (nearly) verbatim per target: a literal, an
                identifier, or any Python sub-expression that carries no registry op.
                Each emitter applies its own per-target literal fixups (None->null in
                typescript, None->nil in go), so Raw carries the ORIGINAL Python text.

  OpNode     -- a recognized registry op or xform, carrying its op id and named
                operand children (each child is itself a Raw or an OpNode). The
                operand names match what each op's emitter reads: e.g.
                op.null_coalesce carries lhs/rhs, op.overloaded_binary carries
                sym/method/arity/left/right, op.destructure carries names/source.

This is deliberately a thin data vocabulary, NOT a class hierarchy per op. The
per-op behavior lives in the emitters (emit/<target>.py), which switch on op_id.
The single reason ir.py exists is so those emitters, the binder, and the transpiler
all name the same node types instead of re-inventing them.
"""


class Raw:
    """A leaf carrying verbatim Python source text (a literal, an identifier, or a
    sub-expression with no registry op). `py` is the ORIGINAL Python text; each
    emitter applies its own literal fixups (e.g. None->null)."""
    __slots__ = ("py",)

    def __init__(self, py_text):
        self.py = py_text

    def __repr__(self):
        return f"Raw({self.py!r})"


class OpNode:
    """A recognized registry op/xform site. `op` is the registry id (e.g.
    'op.null_coalesce'); `kw` holds named operand children, each a Raw or OpNode.

    The synthetic pseudo-op '__binop__' (sym/lhs/rhs) is used for a plain binary
    operator over non-user operands that still needs structural emission around a
    hoisted child -- it is NOT a registry op, it is the emitter's way of carrying a
    `+`/`-`/... through an emit pass. Emitters switch on op to decide the lowering."""
    __slots__ = ("op", "kw")

    def __init__(self, op, **kw):
        self.op = op
        self.kw = kw

    def __repr__(self):
        inner = ", ".join(f"{k}={v!r}" for k, v in self.kw.items())
        return f"OpNode({self.op}, {inner})"


# The synthetic pseudo-op id for a plain binary operator wrapper (see OpNode docstring).
BINOP = "__binop__"
