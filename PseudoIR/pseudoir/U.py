"""
U -- the Hub null-safety namespace (PseudoIR v2, R4).

the owner's DECIDED notation (2026-07-14): the registry null-safety ops are spelled as
FUNCTIONS under an importable module `U` in the Hub. The Hub source stays valid,
runnable Python, which preserves the CPython-as-oracle property: to know what a
Hub program MEANS, you run it under CPython, and this module IS the reference
semantics for the null-safety ops. Every function here is written to match the
op vectors in registry/ops.json EXACTLY -- null-only, never falsy.

Op -> function map:
    op.null_coalesce   -> U.coalesce(a, b)
    op.safe_call       -> U.safe(x).attr.attr...   (proxy; .unwrap(default) to exit)
    op.coalesce_assign -> (no direct function form -- see coalesce_assign note below)
    op.not_null_assert -> U.not_null(x)

Escalation surface (do NOT extend without the owner sign-off): anything beyond
coalesce / safe / not_null, and method CALLS through a safe chain
(U.safe(x).method()), which are trickier than attribute access -- see the _SafeProxy
note. This module deliberately keeps the API to the three ops plus the safe proxy.
"""

_MISSING = object()


def coalesce(a, b):
    """op.null_coalesce: yield a unless a IS None, in which case yield b.

    NULL-ONLY, never falsy. coalesce(0, 99) == 0 and coalesce("", "X") == "" --
    that is the falsy-trap vector that separates true null-coalescing from a
    boolean `a or b` (which would wrongly return 99 and "X"). The check is
    `a is None`, never `not a`.
    """
    return a if a is not None else b


def not_null(x):
    """op.not_null_assert: assert x is not None and return it; raise on None.

    This is an ASSERTION, not a default -- distinct from coalesce. A None input
    raises ValueError (CPython's runtime signal), matching the op's `null_raises`
    vector; a present value passes straight through.
    """
    if x is None:
        raise ValueError("U.not_null: value was None")
    return x


class _SafeProxy:
    """The value carried through a U.safe(...) chain.

    Wraps either a real value or the short-circuited None state. Attribute access
    on a proxy wrapping None yields another None-state proxy WITHOUT touching the
    missing attribute (the short-circuit) -- so `U.safe(u).address.street` yields
    a None-state proxy if u, u.address, or u.address.street is None, and never
    raises AttributeError on the way. `.unwrap(default)` leaves the proxy world,
    returning the carried value, or `default` (via coalesce) if the chain
    short-circuited to None.

    METHOD CALLS through the chain (U.safe(x).method()) are an ESCALATION, not
    built here: making the proxy callable would have to distinguish "call the
    wrapped attribute" from "the user wanted the attribute itself", and short-
    circuit a call on None -- trickier than attribute access. Probed and recorded
    in REPORT_r4.md; deliberately NOT implemented. This proxy supports attribute
    access and .unwrap() only.
    """
    __slots__ = ("_val",)

    def __init__(self, val):
        self._val = val

    def __getattr__(self, name):
        # _val is None (short-circuited) OR the attribute is absent -> stay None.
        if self._val is None:
            return _SafeProxy(None)
        nxt = getattr(self._val, name, None)
        return _SafeProxy(nxt)

    def unwrap(self, default=None):
        """Exit the chain: return the carried value, or `default` if it is None.
        `.unwrap(d)` is exactly `U.coalesce(<carried value>, d)`."""
        return coalesce(self._val, default)

    def __repr__(self):
        return f"U.safe({self._val!r})"


def safe(x):
    """op.safe_call: begin a null-short-circuiting attribute chain over x.

    `U.safe(x).a.b.c.unwrap(default)` yields x.a.b.c if every link is present,
    or `default` if x or any intermediate is None -- without ever raising on the
    missing hop. Around a bare chain you either call .unwrap(d) or wrap the whole
    thing in U.coalesce(...). See _SafeProxy for the short-circuit mechanism and
    the method-call escalation.
    """
    return _SafeProxy(x)


# op.coalesce_assign note (recorded here as the reference semantics decision):
#
# There is deliberately NO `U.coalesce_assign(x, y)` function. Python cannot
# assign THROUGH a function call -- a function receives the VALUE of x, not the
# NAME x, so `U.coalesce_assign(x, y)` could never rebind the caller's x the way
# `x ??= y` does in a native target. A function can only return a new value.
#
# The Hub idiom for op.coalesce_assign is therefore the ordinary rebinding:
#
#     x = U.coalesce(x, y)
#
# This is exact: it assigns y to x only when x is None (coalesce is null-only),
# leaves a falsy-but-present x unchanged (coalesce_assign's falsy_trap vector),
# and rebinds the real name x at the call site. Ingest recognizes the shape
# `<name> = U.coalesce(<same name>, <rhs>)` as op.coalesce_assign; every non-python
# target still emits its native `??=` / `x = x ?: y` from that one op. This is the
# recorded decision path: the awkwardness is Python's (no assign-through-call), not
# the op's, and the rebinding idiom sidesteps it without a function.


# ---------------------------------------------------------------------------
# range_inclusive -- the Hub notation for op.range with inclusive_end=True.
#
# The range prober (prober/range/demo_range.py) established `range_inclusive(a, b)`
# / `range_inclusive(a, b, step)` as the Hub spelling that marks an INCLUSIVE end
# bound, distinct from Python's own exclusive `range(a, b)`. Python has no inclusive
# range builtin, so for the Hub source to stay runnable under CPython (the oracle),
# this function IS that reference semantics: it yields a..b INCLUSIVE of b, with an
# optional step. Ordinary `range(...)` in Hub source stays Python's native exclusive
# builtin and needs nothing here.
#
# It is exported at module scope so a Hub file can call it bare after
# `from pseudoir.U import range_inclusive` (what the python-passthrough emitter and
# the oracle runner inject), matching how `U.coalesce` is called after importing U.
# ---------------------------------------------------------------------------
def range_inclusive(a, b, step=1):
    """op.range with inclusive_end=True: yield a..b including b, stepping by `step`."""
    if step == 0:
        raise ValueError("range_inclusive: step must be non-zero")
    end = b + (1 if step > 0 else -1)
    return range(a, end, step)
