"""Support for the python emulations.  Hand written, not generated.

Every value crossing this boundary is a NON-NEGATIVE python int already held
to its width; `w` says which width, because an unbounded int does not carry
one.  The semantics are the Go helpers' semantics, which the SoftFloat test
already passed -- the three don't-care pins of `scripts/emit_emulations.py`
are made here and nowhere else.
"""


def sf_sgn(x, w):
    """The SIGNED reading of a width-w bit pattern."""
    m = (1 << w) - 1
    v = x & m
    return v - (1 << w) if v >> (w - 1) else v


def sf_udiv(a, b):
    """Unsigned divide.  PIN: a zero divisor yields zero."""
    return 0 if b == 0 else a // b


def sf_ctlz(x, w):
    """Count leading zeros.  PIN: ctlz(0) is the bit width."""
    n = 0
    while n < w and not (x >> (w - 1 - n)) & 1:
        n += 1
    return n


def sf_abs(x, w):
    """|x| read signed, back in the width.  The most negative value wraps."""
    return ((1 << w) - x if sf_sgn(x, w) < 0 else x) & ((1 << w) - 1)


def sf_usubsat(a, b):
    """Saturating unsigned subtract."""
    return a - b if a > b else 0


def sf_fshl(a, b, c, w):
    """Funnel shift left: the high w bits of (a:b) shifted left by c mod w."""
    s = c & (w - 1)
    return a if s == 0 else ((a << s) | (b >> (w - s))) & ((1 << w) - 1)
