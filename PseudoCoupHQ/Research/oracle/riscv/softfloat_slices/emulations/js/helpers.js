'use strict';
// Support for the javascript emulations.  Hand written, not generated.
//
// Every value crossing this boundary is a NON-NEGATIVE BigInt already held to
// its width; `w` (itself a BigInt) says which width.  BigInt and not Number:
// a Number is an IEEE double and would lose the low bits of the 64-bit values
// these slices carry.  The semantics are the Go helpers' semantics, which the
// SoftFloat test already passed -- the three don't-care pins of
// scripts/emit_emulations.js are made here and nowhere else.

function sfSgn(x, w) {              // the SIGNED reading of a width-w pattern
  const m = (1n << w) - 1n;
  const v = x & m;
  return (v >> (w - 1n)) ? v - (1n << w) : v;
}

function sfUdiv(a, b) {             // PIN: a zero divisor yields zero
  return b === 0n ? 0n : a / b;
}

function sfCtlz(x, w) {             // PIN: ctlz(0) is the bit width
  let n = 0n;
  while (n < w && !((x >> (w - 1n - n)) & 1n)) n += 1n;
  return n;
}

function sfAbs(x, w) {              // the most negative value wraps
  return (sfSgn(x, w) < 0n ? (1n << w) - x : x) & ((1n << w) - 1n);
}

function sfUsubsat(a, b) {          // saturating unsigned subtract
  return a > b ? a - b : 0n;
}

function sfFshl(a, b, c, w) {       // high w bits of (a:b) shifted left
  const s = c & (w - 1n);
  return s === 0n ? a : ((a << s) | (b >> (w - s))) & ((1n << w) - 1n);
}

module.exports = { sfSgn, sfUdiv, sfCtlz, sfAbs, sfUsubsat, sfFshl };
