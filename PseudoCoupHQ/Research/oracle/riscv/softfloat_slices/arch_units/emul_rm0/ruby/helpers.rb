# Support for the ruby emulations.  Hand written, not generated.
#
# Every value crossing this boundary is a NON-NEGATIVE ruby Integer already
# held to its width; +w+ says which width, because an unbounded Integer does
# not carry one.  The semantics are the Go helpers' semantics, which the
# SoftFloat test already passed -- the three don't-care pins of
# scripts/emit_emulations.py are made here and nowhere else.

def sf_sgn(x, w)            # the SIGNED reading of a width-w bit pattern
  m = (1 << w) - 1
  v = x & m
  (v >> (w - 1)) == 1 ? v - (1 << w) : v
end

def sf_udiv(a, b)           # PIN: a zero divisor yields zero
  b == 0 ? 0 : a / b
end

def sf_ctlz(x, w)           # PIN: ctlz(0) is the bit width
  n = 0
  n += 1 while n < w && ((x >> (w - 1 - n)) & 1) == 0
  n
end

def sf_abs(x, w)            # the most negative value wraps, as LLVM's does
  (sf_sgn(x, w) < 0 ? (1 << w) - x : x) & ((1 << w) - 1)
end

def sf_usubsat(a, b)        # saturating unsigned subtract
  a > b ? a - b : 0
end

def sf_fshl(a, b, c, w)     # high w bits of (a:b) shifted left by c mod w
  s = c & (w - 1)
  s == 0 ? a : ((a << s) | (b >> (w - s))) & ((1 << w) - 1)
end
