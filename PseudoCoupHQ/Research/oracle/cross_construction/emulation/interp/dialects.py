#!/usr/bin/env python3
"""dialects.py -- task ex1: ONE HELPER PRELUDE PER INTERPRETED
LANGUAGE, and nothing else.

Node: hq.research.arch_unit_oracle.cross_construction.autopoly, with
`node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages`.

WHAT THIS FILE IS, in one sentence: for each interpreted target, the
text of the small set of functions its emulations are written in
terms of, written in that language's OWN operators over that
language's OWN value model, every rule of it measured by a probe
before it was written.

WHY IT IS SHAPED THIS WAY.  The compiled targets' renderers emit
expressions with the language's casts inline, because c, rust, go and
swift all have fixed-width holders and the cast IS the mask.  Not one
of the seven languages here does: python's and ruby's integers are
unbounded, javascript's BigInt is unbounded, php's is 64-bit and
OVERFLOWS TO A FLOAT rather than wrapping, and java's, dart's and
c#'s are fixed but mask their own shift counts.  Writing the mask
inline in seven dialects would be seven chances to spell one of those
five facts wrong.  Instead each language states its value model ONCE,
as a prelude of named functions, and the renderer emits calls.  Every
function below is the language's own operators; nothing is emulated
through a big-number library, which would be a different value model
from the one the brief asks for.

THE VALUE CONVENTION, stated once and true of every dialect:
  * a value of width `w` is carried as a NON-NEGATIVE integer in
    [0, 2^w) in the unbounded dialects, and as the low `w` bits of the
    language's 64-bit integer (higher bits zero) in the fixed ones;
  * a FLOAT is carried as its IEEE bit pattern in the same way, so
    `fp.to_ieee_bv` and the one-argument `fpToFP` are the identity and
    no rendering ever round-trips a value through a wider float than
    the one the term names;
  * an arrival reaches the emulation as a decimal integer on one line
    of standard input, and the answer leaves it as a decimal integer
    on one line of standard output, or as the token `RAISE:<kind>`
    when the language raised.

WHAT WAS MEASURED BEFORE EACH RULE WAS WRITTEN -- lane
`ex1_l2_cpp_and_value_model_probes.sh` sections [4/9] to [8/9] and
lane `ex1_l3_the_ten_cells_and_what_they_ask_for.sh` sections [2/4] to
[4/4], on the tower under
`<runs>/ex1/agent/logs/`.  The five findings
every prelude below is built on, each LITERAL from those logs:

    python     division rounds       (-7) // 2          -> -4
    ruby       division rounds       -7 / 2             -> -4
    php        at the width boundary PHP_INT_MAX + 1    -> 9.223372036854776E+18
    php        its type there        gettype(...)       -> 'double'
    php        a shift count at the width  1 << 64      -> 0
    java       a shift count at the width  1 << 32      -> 1
    java       a long shift count at 64    1L << 64     -> 1
    dart       a shift count at the width  1 << 64      -> 0
    csharp     a shift count at the width  1 << 32      -> 1
    javascript division truncates    (-7n) / 2n         -> -3

so: python's and ruby's `/` FLOOR and z3's `bvsdiv` TRUNCATES, which is
why `sdiv` is spelled with `abs` in both; php's `+` leaves the integers
entirely at the boundary, which is why its 64-bit arithmetic is done in
two 32-bit halves; and java's and c#'s shift counts are masked while
dart's and php's saturate to zero, which is why every shift here tests
its count first.

MEMORY: this file is text.  It allocates nothing.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

The operator tokens in the strings below are the OUTPUT TEXT of a
printer.  Nothing here keys, groups, pairs or selects anything.

Coding discipline: no compound one-liner statements.
"""

# ==================================================================
# cpython
# ==================================================================

CPYTHON_PRELUDE = '''import struct
import sys


def m(x, w):
    return x & ((1 << w) - 1)


def s(x, w):
    x = x & ((1 << w) - 1)
    if x >> (w - 1):
        return x - (1 << w)
    return x


def add(a, b, w):
    return m(a + b, w)


def sub(a, b, w):
    return m(a - b, w)


def mul(a, b, w):
    return m(a * b, w)


def band(a, b, w):
    return m(a & b, w)


def bor(a, b, w):
    return m(a | b, w)


def bxor(a, b, w):
    return m(a ^ b, w)


def bnot(a, w):
    return m(~a, w)


def bneg(a, w):
    return m(-a, w)


def shl(a, n, w):
    if n >= w:
        return 0
    return m(a << n, w)


def lshr(a, n, w):
    if n >= w:
        return 0
    return m(a, w) >> n


def ashr(a, n, w):
    v = s(a, w)
    k = n
    if k >= w:
        k = w - 1
    return m(v >> k, w)


def udiv(a, b, w):
    return m(m(a, w) // m(b, w), w)


def urem(a, b, w):
    return m(m(a, w) % m(b, w), w)


def sdiv(a, b, w):
    x = s(a, w)
    y = s(b, w)
    q = abs(x) // abs(y)
    if (x < 0) != (y < 0):
        q = -q
    return m(q, w)


def srem(a, b, w):
    x = s(a, w)
    y = s(b, w)
    r = abs(x) % abs(y)
    if x < 0:
        r = -r
    return m(r, w)


def ult(a, b, w):
    return m(a, w) < m(b, w)


def ule(a, b, w):
    return m(a, w) <= m(b, w)


def ugt(a, b, w):
    return m(a, w) > m(b, w)


def uge(a, b, w):
    return m(a, w) >= m(b, w)


def slt(a, b, w):
    return s(a, w) < s(b, w)


def sle(a, b, w):
    return s(a, w) <= s(b, w)


def sgt(a, b, w):
    return s(a, w) > s(b, w)


def sge(a, b, w):
    return s(a, w) >= s(b, w)


def eq(a, b, w):
    return m(a, w) == m(b, w)


def ne(a, b, w):
    return m(a, w) != m(b, w)


def cat(hi, lo, lw):
    return (hi << lw) | m(lo, lw)


def ext(x, hi, lo):
    return m(x >> lo, hi - lo + 1)


def sext(x, fromw, tow):
    return m(s(x, fromw), tow)


def b2f(x, w):
    if w == 32:
        return struct.unpack("<f", struct.pack("<I", m(x, 32)))[0]
    return struct.unpack("<d", struct.pack("<Q", m(x, 64)))[0]


def f2b(f, w):
    if w == 32:
        try:
            return struct.unpack("<I", struct.pack("<f", f))[0]
        except OverflowError:
            if f > 0:
                return 0x7f800000
            return 0xff800000
    return struct.unpack("<Q", struct.pack("<d", f))[0]


def fadd(a, b, w):
    return f2b(b2f(a, w) + b2f(b, w), w)


def fsub(a, b, w):
    return f2b(b2f(a, w) - b2f(b, w), w)


def fmul(a, b, w):
    return f2b(b2f(a, w) * b2f(b, w), w)


def fdiv(a, b, w):
    return f2b(b2f(a, w) / b2f(b, w), w)


def i2f(x, fromw, w):
    return f2b(float(s(x, fromw)), w)


def u2f(x, fromw, w):
    return f2b(float(m(x, fromw)), w)


def fwiden(x, fromw, w):
    return f2b(b2f(x, fromw), w)
'''

CPYTHON_MAIN = '''

def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = %(symbol)s(*values)
            sys.stdout.write("%%d\\n" %% answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%%s\\n" %% type(problem).__name__)
    sys.stdout.flush()


main()
'''

# ==================================================================
# ruby
# ==================================================================

RUBY_PRELUDE = '''def m(x, w)
  x & ((1 << w) - 1)
end

def s(x, w)
  x = x & ((1 << w) - 1)
  return x - (1 << w) if (x >> (w - 1)) != 0
  x
end

def add(a, b, w)
  m(a + b, w)
end

def sub(a, b, w)
  m(a - b, w)
end

def mul(a, b, w)
  m(a * b, w)
end

def band(a, b, w)
  m(a & b, w)
end

def bor(a, b, w)
  m(a | b, w)
end

def bxor(a, b, w)
  m(a ^ b, w)
end

def bnot(a, w)
  m(~a, w)
end

def bneg(a, w)
  m(-a, w)
end

def shl(a, n, w)
  return 0 if n >= w
  m(a << n, w)
end

def lshr(a, n, w)
  return 0 if n >= w
  m(a, w) >> n
end

def ashr(a, n, w)
  v = s(a, w)
  k = n
  k = w - 1 if k >= w
  m(v >> k, w)
end

def udiv(a, b, w)
  m(m(a, w) / m(b, w), w)
end

def urem(a, b, w)
  m(m(a, w) % m(b, w), w)
end

def sdiv(a, b, w)
  x = s(a, w)
  y = s(b, w)
  q = x.abs / y.abs
  q = -q if (x < 0) != (y < 0)
  m(q, w)
end

def srem(a, b, w)
  x = s(a, w)
  y = s(b, w)
  r = x.abs % y.abs
  r = -r if x < 0
  m(r, w)
end

def ult(a, b, w)
  m(a, w) < m(b, w)
end

def ule(a, b, w)
  m(a, w) <= m(b, w)
end

def ugt(a, b, w)
  m(a, w) > m(b, w)
end

def uge(a, b, w)
  m(a, w) >= m(b, w)
end

def slt(a, b, w)
  s(a, w) < s(b, w)
end

def sle(a, b, w)
  s(a, w) <= s(b, w)
end

def sgt(a, b, w)
  s(a, w) > s(b, w)
end

def sge(a, b, w)
  s(a, w) >= s(b, w)
end

def eq(a, b, w)
  m(a, w) == m(b, w)
end

def ne(a, b, w)
  m(a, w) != m(b, w)
end

def cat(hi, lo, lw)
  (hi << lw) | m(lo, lw)
end

def ext(x, hi, lo)
  m(x >> lo, hi - lo + 1)
end

def sext(x, fromw, tow)
  m(s(x, fromw), tow)
end

def b2f(x, w)
  return [m(x, 32)].pack("V").unpack1("e") if w == 32
  [m(x, 64)].pack("Q<").unpack1("E")
end

def f2b(f, w)
  return [f].pack("e").unpack1("V") if w == 32
  [f].pack("E").unpack1("Q<")
end

def fadd(a, b, w)
  f2b(b2f(a, w) + b2f(b, w), w)
end

def fsub(a, b, w)
  f2b(b2f(a, w) - b2f(b, w), w)
end

def fmul(a, b, w)
  f2b(b2f(a, w) * b2f(b, w), w)
end

def fdiv(a, b, w)
  f2b(b2f(a, w) / b2f(b, w), w)
end

def i2f(x, fromw, w)
  f2b(s(x, fromw).to_f, w)
end

def u2f(x, fromw, w)
  f2b(m(x, fromw).to_f, w)
end

def fwiden(x, fromw, w)
  f2b(b2f(x, fromw), w)
end
'''

RUBY_MAIN = '''

STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts %(symbol)s(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
'''

# ==================================================================
# javascript, on node
# ==================================================================

JAVASCRIPT_PRELUDE = '''"use strict";
const view = new DataView(new ArrayBuffer(8));

function m(x, w) { return BigInt.asUintN(w, x); }
function s(x, w) { return BigInt.asIntN(w, x); }
function add(a, b, w) { return m(a + b, w); }
function sub(a, b, w) { return m(a - b, w); }
function mul(a, b, w) { return m(a * b, w); }
function band(a, b, w) { return m(a & b, w); }
function bor(a, b, w) { return m(a | b, w); }
function bxor(a, b, w) { return m(a ^ b, w); }
function bnot(a, w) { return m(~a, w); }
function bneg(a, w) { return m(-a, w); }
function shl(a, n, w) {
    if (n >= BigInt(w)) { return 0n; }
    return m(a << n, w);
}
function lshr(a, n, w) {
    if (n >= BigInt(w)) { return 0n; }
    return m(a, w) >> n;
}
function ashr(a, n, w) {
    const v = s(a, w);
    let k = n;
    if (k >= BigInt(w)) { k = BigInt(w - 1); }
    return m(v >> k, w);
}
function udiv(a, b, w) { return m(m(a, w) / m(b, w), w); }
function urem(a, b, w) { return m(m(a, w) % m(b, w), w); }
function sdiv(a, b, w) { return m(s(a, w) / s(b, w), w); }
function srem(a, b, w) { return m(s(a, w) % s(b, w), w); }
function ult(a, b, w) { return m(a, w) < m(b, w); }
function ule(a, b, w) { return m(a, w) <= m(b, w); }
function ugt(a, b, w) { return m(a, w) > m(b, w); }
function uge(a, b, w) { return m(a, w) >= m(b, w); }
function slt(a, b, w) { return s(a, w) < s(b, w); }
function sle(a, b, w) { return s(a, w) <= s(b, w); }
function sgt(a, b, w) { return s(a, w) > s(b, w); }
function sge(a, b, w) { return s(a, w) >= s(b, w); }
function eq(a, b, w) { return m(a, w) === m(b, w); }
function ne(a, b, w) { return m(a, w) !== m(b, w); }
function cat(hi, lo, lw) { return (hi << BigInt(lw)) | m(lo, lw); }
function ext(x, hi, lo) { return m(x >> BigInt(lo), hi - lo + 1); }
function sext(x, fromw, tow) { return m(s(x, fromw), tow); }
function b2f(x, w) {
    if (w === 32) {
        view.setUint32(0, Number(m(x, 32)), true);
        return view.getFloat32(0, true);
    }
    view.setBigUint64(0, m(x, 64), true);
    return view.getFloat64(0, true);
}
function f2b(f, w) {
    if (w === 32) {
        view.setFloat32(0, f, true);
        return BigInt(view.getUint32(0, true));
    }
    view.setFloat64(0, f, true);
    return view.getBigUint64(0, true);
}
function fadd(a, b, w) { return f2b(b2f(a, w) + b2f(b, w), w); }
function fsub(a, b, w) { return f2b(b2f(a, w) - b2f(b, w), w); }
function fmul(a, b, w) { return f2b(b2f(a, w) * b2f(b, w), w); }
function fdiv(a, b, w) { return f2b(b2f(a, w) / b2f(b, w), w); }
function i2f(x, fromw, w) { return f2b(Number(s(x, fromw)), w); }
function u2f(x, fromw, w) { return f2b(Number(m(x, fromw)), w); }
function fwiden(x, fromw, w) { return f2b(b2f(x, fromw), w); }
'''

JAVASCRIPT_MAIN = '''

const lines = require("fs").readFileSync(0, "utf8").split("\\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\\s+/).map((one) => BigInt(one));
    try {
        out.push(%(symbol)s(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\\n") + "\\n");
'''

# ==================================================================
# php
# ==================================================================
#
# THE ONE THING THAT IS NOT LIKE THE OTHERS.  php's integer is 64 bits
# and does NOT wrap: lane ex1_l3 [2/4] measured
# `0x7FFF... + 0x7FFF...` leaving the integers for a double
# (`gettype(...)` -> 'double'), and neither gmp nor bcmath is loaded
# (`extension_loaded("gmp")` -> false).  So `add`, `sub` and `mul` are
# spelled in two 32-bit halves, which php's own integer holds exactly,
# and no 64-bit intermediate ever exceeds the boundary.

PHP_PRELUDE = '''<?php

function ex_maskbits($w) {
    // THE MASK, AND WHY IT IS NOT `(1 << $w) - 1`.  php's `1 << 63` is
    // PHP_INT_MIN, so `(1 << 63) - 1` leaves the integers for a double
    // and the mask becomes a float -- measured on lane ex1_l7's first
    // pass, where `shr` cl_gpr 64 answered 0 where the reference
    // answered 1 at the point [2, 1].
    if ($w >= 64) { return -1; }
    if ($w == 63) { return PHP_INT_MAX; }
    return (1 << $w) - 1;
}

function ex_m($x, $w) {
    if ($w >= 64) { return $x; }
    return $x & ex_maskbits($w);
}

function ex_s($x, $w) {
    if ($w >= 64) { return $x; }
    $x = ex_m($x, $w);
    if ((($x >> ($w - 1)) & 1) != 0) {
        if ($w == 63) { return $x + PHP_INT_MIN; }
        return $x - (1 << $w);
    }
    return $x;
}

function ex_add($a, $b, $w) {
    if ($w < 64) { return ex_m($a + $b, $w); }
    $lo = ($a & 0xFFFFFFFF) + ($b & 0xFFFFFFFF);
    $hi = (($a >> 32) & 0xFFFFFFFF) + (($b >> 32) & 0xFFFFFFFF)
          + (($lo >> 32) & 1);
    return (($hi & 0xFFFFFFFF) << 32) | ($lo & 0xFFFFFFFF);
}

function ex_bneg($a, $w) {
    return ex_add(ex_bnot($a, $w), 1, $w);
}

function ex_sub($a, $b, $w) {
    return ex_add($a, ex_bneg($b, $w), $w);
}

function ex_mul($a, $b, $w) {
    // THE MULTIPLY IN 16-BIT LIMBS, and the limb size is the
    // measurement's own: a 32-bit by 32-bit product is up to 2^64 and
    // php leaves the integers there, which is what answered 2147483648
    // where the reference answered 2147483647 at the point
    // [2147483649, 4294967295] on lane ex1_l7's first pass.  Every
    // product below is under 2^34 and every running sum under 2^36.
    if ($w <= 16) { return ex_m($a * $b, $w); }
    $a0 = $a & 0xFFFF;
    $a1 = ($a >> 16) & 0xFFFF;
    $a2 = ($a >> 32) & 0xFFFF;
    $a3 = ($a >> 48) & 0xFFFF;
    $b0 = $b & 0xFFFF;
    $b1 = ($b >> 16) & 0xFFFF;
    $b2 = ($b >> 32) & 0xFFFF;
    $b3 = ($b >> 48) & 0xFFFF;
    $p0 = $a0 * $b0;
    $p1 = $a0 * $b1 + $a1 * $b0;
    $p2 = $a0 * $b2 + $a1 * $b1 + $a2 * $b0;
    $p3 = $a0 * $b3 + $a1 * $b2 + $a2 * $b1 + $a3 * $b0;
    $r0 = $p0 & 0xFFFF;
    $t1 = $p1 + ($p0 >> 16);
    $r1 = $t1 & 0xFFFF;
    $t2 = $p2 + ($t1 >> 16);
    $r2 = $t2 & 0xFFFF;
    $t3 = $p3 + ($t2 >> 16);
    $r3 = $t3 & 0xFFFF;
    $whole = $r0 | ($r1 << 16) | ($r2 << 32) | ($r3 << 48);
    return ex_m($whole, $w);
}

function ex_band($a, $b, $w) { return ex_m($a & $b, $w); }
function ex_bor($a, $b, $w) { return ex_m($a | $b, $w); }
function ex_bxor($a, $b, $w) { return ex_m($a ^ $b, $w); }
function ex_bnot($a, $w) { return ex_m(~$a, $w); }

function ex_shl($a, $n, $w) {
    if ($n >= $w) { return 0; }
    if ($w >= 64) { return ($a << $n); }
    return ex_m($a << $n, $w);
}

function ex_lshr($a, $n, $w) {
    if ($n >= $w) { return 0; }
    if ($w >= 64) {
        if ($n == 0) { return $a; }
        return ($a >> $n) & (PHP_INT_MAX >> ($n - 1));
    }
    return ex_m($a, $w) >> $n;
}

function ex_ashr($a, $n, $w) {
    $v = ex_s($a, $w);
    $k = $n;
    if ($k >= $w) { $k = $w - 1; }
    return ex_m($v >> $k, $w);
}

function ex_udiv($a, $b, $w) {
    if ($w < 64) { return ex_m(intdiv(ex_m($a, $w), ex_m($b, $w)), $w); }
    $x = $a; $y = $b;
    if ($y < 0) { if (ex_uge_raw($x, $y)) { return 1; } return 0; }
    if ($x >= 0) { return intdiv($x, $y); }
    $q = intdiv(ex_lshr($x, 1, 64), $y) << 1;
    $r = ex_sub($x, ex_mul($q, $y, 64), 64);
    if (ex_uge_raw($r, $y)) { $q = ex_add($q, 1, 64); }
    return $q;
}

function ex_uge_raw($x, $y) {
    if (($x < 0) == ($y < 0)) { return $x >= $y; }
    return $x < 0;
}

function ex_urem($a, $b, $w) {
    if ($w < 64) { return ex_m(ex_m($a, $w) % ex_m($b, $w), $w); }
    $q = ex_udiv($a, $b, 64);
    return ex_sub($a, ex_mul($q, $b, 64), 64);
}

function ex_sdiv($a, $b, $w) {
    // php's OWN `intdiv` TRUNCATES -- lane ex1_l2 [5/9] measured
    // `intdiv(-7, 2)` -> -3 -- which is z3's `bvsdiv`, so the abs-based
    // spelling python and ruby need (their division FLOORS) is wrong
    // here in one more way than it is unnecessary: `abs(PHP_INT_MIN)`
    // leaves the integers for a float, and 27 points of lane ex1_l8's
    // first pass declined `RAISE:TypeError` because of it.
    return ex_m(intdiv(ex_s($a, $w), ex_s($b, $w)), $w);
}

function ex_srem($a, $b, $w) {
    // php's own remainder takes the sign of the DIVIDEND -- lane
    // ex1_l2 [5/9], `-7 % 2` -> -1 -- which is z3's `bvsrem`.
    return ex_m(ex_s($a, $w) % ex_s($b, $w), $w);
}

function ex_ult($a, $b, $w) {
    if ($w < 64) { return ex_m($a, $w) < ex_m($b, $w); }
    return !ex_uge_raw($a, $b);
}
function ex_ule($a, $b, $w) {
    if ($w < 64) { return ex_m($a, $w) <= ex_m($b, $w); }
    return !ex_uge_raw($a, $b) || $a == $b;
}
function ex_ugt($a, $b, $w) { return !ex_ule($a, $b, $w); }
function ex_uge($a, $b, $w) { return !ex_ult($a, $b, $w); }
function ex_slt($a, $b, $w) { return ex_s($a, $w) < ex_s($b, $w); }
function ex_sle($a, $b, $w) { return ex_s($a, $w) <= ex_s($b, $w); }
function ex_sgt($a, $b, $w) { return ex_s($a, $w) > ex_s($b, $w); }
function ex_sge($a, $b, $w) { return ex_s($a, $w) >= ex_s($b, $w); }
function ex_eq($a, $b, $w) { return ex_m($a, $w) == ex_m($b, $w); }
function ex_ne($a, $b, $w) { return ex_m($a, $w) != ex_m($b, $w); }

function ex_cat($hi, $lo, $lw) {
    return ex_shl($hi, $lw, 64) | ex_m($lo, $lw);
}

function ex_ext($x, $hi, $lo) {
    return ex_m(ex_lshr($x, $lo, 64), $hi - $lo + 1);
}

function ex_sext($x, $fromw, $tow) {
    return ex_m(ex_s($x, $fromw), $tow);
}

function ex_b2f($x, $w) {
    if ($w == 32) { return unpack("g", pack("V", ex_m($x, 32)))[1]; }
    return unpack("e", pack("P", $x))[1];
}

function ex_f2b($f, $w) {
    if ($w == 32) { return unpack("V", pack("g", $f))[1]; }
    return unpack("P", pack("e", $f))[1];
}

function ex_fadd($a, $b, $w) { return ex_f2b(ex_b2f($a, $w) + ex_b2f($b, $w), $w); }
function ex_fsub($a, $b, $w) { return ex_f2b(ex_b2f($a, $w) - ex_b2f($b, $w), $w); }
function ex_fmul($a, $b, $w) { return ex_f2b(ex_b2f($a, $w) * ex_b2f($b, $w), $w); }
function ex_fdiv($a, $b, $w) { return ex_f2b(ex_b2f($a, $w) / ex_b2f($b, $w), $w); }
function ex_i2f($x, $fromw, $w) { return ex_f2b((float)ex_s($x, $fromw), $w); }
function ex_u2f($x, $fromw, $w) { return ex_f2b((float)ex_m($x, $fromw), $w); }
function ex_fwiden($x, $fromw, $w) { return ex_f2b(ex_b2f($x, $fromw), $w); }

function ex_parse($text) {
    // A DECIMAL STRING TO THE 64-BIT PATTERN IT NAMES.  php's own
    // `intval` SATURATES at PHP_INT_MAX rather than wrapping, so a
    // sample point at or above 2^63 would arrive as the wrong value;
    // this builds it with the exact 64-bit helpers above instead.
    $negative = false;
    if (strlen($text) > 0 && $text[0] === "-") {
        $negative = true;
        $text = substr($text, 1);
    }
    $value = 0;
    $length = strlen($text);
    for ($i = 0; $i < $length; $i++) {
        $digit = ord($text[$i]) - 48;
        $value = ex_add(ex_mul($value, 10, 64), $digit, 64);
    }
    if ($negative) { return ex_bneg($value, 64); }
    return $value;
}
'''

PHP_MAIN = '''

$handle = fopen("php://stdin", "r");
while (($line = fgets($handle)) !== false) {
    $text = trim($line);
    if ($text === "") { continue; }
    $values = preg_split("/\\\\s+/", $text);
    $ints = array();
    foreach ($values as $one) { $ints[] = ex_parse($one); }
    try {
        $answer = %(symbol)s(...$ints);
        if ($answer < 0) {
            echo sprintf("%%s\\n", sprintf("%%u", $answer));
        } else {
            echo $answer . "\\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\\n";
    }
}
'''

# ==================================================================
# java
# ==================================================================
#
# `s(x, 64)` is `(x << 0) >> 0`, which is x; `m(x, 64)` returns x
# untouched, because java's own `1L << 64` is 1 -- lane ex1_l2 [7/9]
# measured it -- so the mask a fixed-width dialect writes must never be
# built by shifting BY the width.

JAVA_PRELUDE = '''import java.io.*;
import java.util.*;

public class Emu {
    static long m(long x, int w) {
        if (w >= 64) { return x; }
        return x & ((1L << w) - 1L);
    }
    static long s(long x, int w) {
        if (w >= 64) { return x; }
        return (x << (64 - w)) >> (64 - w);
    }
    static long add(long a, long b, int w) { return m(a + b, w); }
    static long sub(long a, long b, int w) { return m(a - b, w); }
    static long mul(long a, long b, int w) { return m(a * b, w); }
    static long band(long a, long b, int w) { return m(a & b, w); }
    static long bor(long a, long b, int w) { return m(a | b, w); }
    static long bxor(long a, long b, int w) { return m(a ^ b, w); }
    static long bnot(long a, int w) { return m(~a, w); }
    static long bneg(long a, int w) { return m(-a, w); }
    static long shl(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(a << n, w);
    }
    static long lshr(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(m(a, w) >>> n, w);
    }
    static long ashr(long a, long n, int w) {
        long v = s(a, w);
        long k = n;
        if (k >= w) { k = w - 1; }
        return m(v >> k, w);
    }
    static long udiv(long a, long b, int w) {
        return m(Long.divideUnsigned(m(a, w), m(b, w)), w);
    }
    static long urem(long a, long b, int w) {
        return m(Long.remainderUnsigned(m(a, w), m(b, w)), w);
    }
    static long sdiv(long a, long b, int w) {
        return m(s(a, w) / s(b, w), w);
    }
    static long srem(long a, long b, int w) {
        return m(s(a, w) % s(b, w), w);
    }
    static boolean ult(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) < 0;
    }
    static boolean ule(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) <= 0;
    }
    static boolean ugt(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) > 0;
    }
    static boolean uge(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) >= 0;
    }
    static boolean slt(long a, long b, int w) { return s(a, w) < s(b, w); }
    static boolean sle(long a, long b, int w) { return s(a, w) <= s(b, w); }
    static boolean sgt(long a, long b, int w) { return s(a, w) > s(b, w); }
    static boolean sge(long a, long b, int w) { return s(a, w) >= s(b, w); }
    static boolean eq(long a, long b, int w) { return m(a, w) == m(b, w); }
    static boolean ne(long a, long b, int w) { return m(a, w) != m(b, w); }
    static long cat(long hi, long lo, int lw) {
        return (hi << lw) | m(lo, lw);
    }
    static long ext(long x, int hi, int lo) {
        return m(x >>> lo, hi - lo + 1);
    }
    static long sext(long x, int fromw, int tow) {
        return m(s(x, fromw), tow);
    }
    static double b2f(long x, int w) {
        if (w == 32) { return Float.intBitsToFloat((int) m(x, 32)); }
        return Double.longBitsToDouble(x);
    }
    static long f2b(double f, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(Float.floatToRawIntBits((float) f));
        }
        return Double.doubleToRawLongBits(f);
    }
    static long fadd(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    + Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) + b2f(b, w), w);
    }
    static long fsub(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    - Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) - b2f(b, w), w);
    }
    static long fmul(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    * Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) * b2f(b, w), w);
    }
    static long fdiv(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    / Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) / b2f(b, w), w);
    }
    static long i2f(long x, int fromw, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(
                Float.floatToRawIntBits((float) s(x, fromw)));
        }
        return Double.doubleToRawLongBits((double) s(x, fromw));
    }
    static long u2f(long x, int fromw, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(Float.floatToRawIntBits(
                (float) Long.parseUnsignedLong(
                    Long.toUnsignedString(m(x, fromw)))));
        }
        return Double.doubleToRawLongBits(
            (double) m(x, fromw));
    }
    static long fwiden(long x, int fromw, int w) {
        return f2b(b2f(x, fromw), w);
    }
'''

JAVA_MAIN = '''
    public static void main(String[] args) throws IOException {
        BufferedReader reader =
            new BufferedReader(new InputStreamReader(System.in));
        StringBuilder answers = new StringBuilder();
        String line = reader.readLine();
        while (line != null) {
            String text = line.trim();
            if (text.length() != 0) {
                String[] parts = text.split("\\\\s+");
                long[] values = new long[parts.length];
                for (int i = 0; i < parts.length; i++) {
                    values[i] = Long.parseUnsignedLong(parts[i]);
                }
                try {
                    answers.append(Long.toUnsignedString(%(call)s));
                    answers.append("\\n");
                } catch (Throwable problem) {
                    answers.append("RAISE:");
                    answers.append(problem.getClass().getSimpleName());
                    answers.append("\\n");
                }
            }
            line = reader.readLine();
        }
        System.out.print(answers);
    }
}
'''

# ==================================================================
# dart
# ==================================================================

DART_PRELUDE = '''import 'dart:io';
import 'dart:typed_data';

final ByteData _view = ByteData(8);

int m(int x, int w) {
  if (w >= 64) { return x; }
  return x & ((1 << w) - 1);
}
int s(int x, int w) {
  if (w >= 64) { return x; }
  return (x << (64 - w)) >> (64 - w);
}
int add(int a, int b, int w) => m(a + b, w);
int sub(int a, int b, int w) => m(a - b, w);
int mul(int a, int b, int w) => m(a * b, w);
int band(int a, int b, int w) => m(a & b, w);
int bor(int a, int b, int w) => m(a | b, w);
int bxor(int a, int b, int w) => m(a ^ b, w);
int bnot(int a, int w) => m(~a, w);
int bneg(int a, int w) => m(-a, w);
int shl(int a, int n, int w) {
  if (n >= w) { return 0; }
  return m(a << n, w);
}
int lshr(int a, int n, int w) {
  if (n >= w) { return 0; }
  return m(m(a, w) >>> n, w);
}
int ashr(int a, int n, int w) {
  final int v = s(a, w);
  int k = n;
  if (k >= w) { k = w - 1; }
  return m(v >> k, w);
}
int udiv(int a, int b, int w) {
  if (w < 64) { return m(m(a, w) ~/ m(b, w), w); }
  if (b < 0) { return uge(a, b, 64) ? 1 : 0; }
  if (a >= 0) { return a ~/ b; }
  final int q = (a >>> 1) ~/ b << 1;
  final int r = a - q * b;
  return uge(r, b, 64) ? q + 1 : q;
}
int urem(int a, int b, int w) {
  if (w < 64) { return m(m(a, w) % m(b, w), w); }
  return sub(a, mul(udiv(a, b, 64), b, 64), 64);
}
int sdiv(int a, int b, int w) => m(s(a, w) ~/ s(b, w), w);
int srem(int a, int b, int w) => m(s(a, w).remainder(s(b, w)), w);
bool ult(int a, int b, int w) {
  if (w < 64) { return m(a, w) < m(b, w); }
  if ((a < 0) == (b < 0)) { return a < b; }
  return b < 0;
}
bool ule(int a, int b, int w) => ult(a, b, w) || m(a, w) == m(b, w);
bool ugt(int a, int b, int w) => !ule(a, b, w);
bool uge(int a, int b, int w) => !ult(a, b, w);
bool slt(int a, int b, int w) => s(a, w) < s(b, w);
bool sle(int a, int b, int w) => s(a, w) <= s(b, w);
bool sgt(int a, int b, int w) => s(a, w) > s(b, w);
bool sge(int a, int b, int w) => s(a, w) >= s(b, w);
bool eq(int a, int b, int w) => m(a, w) == m(b, w);
bool ne(int a, int b, int w) => m(a, w) != m(b, w);
int cat(int hi, int lo, int lw) => (hi << lw) | m(lo, lw);
int ext(int x, int hi, int lo) => m(x >>> lo, hi - lo + 1);
int sext(int x, int fromw, int tow) => m(s(x, fromw), tow);
double b2f(int x, int w) {
  if (w == 32) {
    _view.setUint32(0, m(x, 32), Endian.little);
    return _view.getFloat32(0, Endian.little);
  }
  _view.setUint64(0, x, Endian.little);
  return _view.getFloat64(0, Endian.little);
}
int f2b(double f, int w) {
  if (w == 32) {
    _view.setFloat32(0, f, Endian.little);
    return _view.getUint32(0, Endian.little);
  }
  _view.setFloat64(0, f, Endian.little);
  return _view.getUint64(0, Endian.little);
}
int fadd(int a, int b, int w) => f2b(b2f(a, w) + b2f(b, w), w);
int fsub(int a, int b, int w) => f2b(b2f(a, w) - b2f(b, w), w);
int fmul(int a, int b, int w) => f2b(b2f(a, w) * b2f(b, w), w);
int fdiv(int a, int b, int w) => f2b(b2f(a, w) / b2f(b, w), w);
int i2f(int x, int fromw, int w) => f2b(s(x, fromw).toDouble(), w);
int u2f(int x, int fromw, int w) => f2b(m(x, fromw).toDouble(), w);
int fwiden(int x, int fromw, int w) => f2b(b2f(x, fromw), w);
'''

DART_MAIN = '''

void main() {
  final StringBuffer out = StringBuffer();
  String? line = stdin.readLineSync();
  while (line != null) {
    final String text = line.trim();
    if (text.isNotEmpty) {
      final List<int> values = text
          .split(RegExp(r"\\s+"))
          .map((one) => BigInt.parse(one).toSigned(64).toInt())
          .toList();
      try {
        final int answer = %(call)s;
        out.writeln(answer < 0
            ? (BigInt.from(answer).toUnsigned(64)).toString()
            : answer.toString());
      } catch (problem) {
        out.writeln("RAISE:${problem.runtimeType}");
      }
    }
    line = stdin.readLineSync();
  }
  stdout.write(out.toString());
}
'''

# ==================================================================
# csharp
# ==================================================================

CSHARP_PRELUDE = '''using System;
using System.Text;

public static class Emu {
    public static long m(long x, int w) {
        if (w >= 64) { return x; }
        return x & ((1L << w) - 1L);
    }
    public static long s(long x, int w) {
        if (w >= 64) { return x; }
        return (x << (64 - w)) >> (64 - w);
    }
    public static long add(long a, long b, int w) { return m(unchecked(a + b), w); }
    public static long sub(long a, long b, int w) { return m(unchecked(a - b), w); }
    public static long mul(long a, long b, int w) { return m(unchecked(a * b), w); }
    public static long band(long a, long b, int w) { return m(a & b, w); }
    public static long bor(long a, long b, int w) { return m(a | b, w); }
    public static long bxor(long a, long b, int w) { return m(a ^ b, w); }
    public static long bnot(long a, int w) { return m(~a, w); }
    public static long bneg(long a, int w) { return m(unchecked(-a), w); }
    public static long shl(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(a << (int) n, w);
    }
    public static long lshr(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m((long)(((ulong) m(a, w)) >> (int) n), w);
    }
    public static long ashr(long a, long n, int w) {
        long v = s(a, w);
        long k = n;
        if (k >= w) { k = w - 1; }
        return m(v >> (int) k, w);
    }
    public static long udiv(long a, long b, int w) {
        return m((long)(((ulong) m(a, w)) / ((ulong) m(b, w))), w);
    }
    public static long urem(long a, long b, int w) {
        return m((long)(((ulong) m(a, w)) % ((ulong) m(b, w))), w);
    }
    public static long sdiv(long a, long b, int w) { return m(s(a, w) / s(b, w), w); }
    public static long srem(long a, long b, int w) { return m(s(a, w) % s(b, w), w); }
    public static bool ult(long a, long b, int w) { return ((ulong) m(a, w)) < ((ulong) m(b, w)); }
    public static bool ule(long a, long b, int w) { return ((ulong) m(a, w)) <= ((ulong) m(b, w)); }
    public static bool ugt(long a, long b, int w) { return ((ulong) m(a, w)) > ((ulong) m(b, w)); }
    public static bool uge(long a, long b, int w) { return ((ulong) m(a, w)) >= ((ulong) m(b, w)); }
    public static bool slt(long a, long b, int w) { return s(a, w) < s(b, w); }
    public static bool sle(long a, long b, int w) { return s(a, w) <= s(b, w); }
    public static bool sgt(long a, long b, int w) { return s(a, w) > s(b, w); }
    public static bool sge(long a, long b, int w) { return s(a, w) >= s(b, w); }
    public static bool eq(long a, long b, int w) { return m(a, w) == m(b, w); }
    public static bool ne(long a, long b, int w) { return m(a, w) != m(b, w); }
    public static long cat(long hi, long lo, int lw) { return (hi << lw) | m(lo, lw); }
    public static long ext(long x, int hi, int lo) {
        return m((long)(((ulong) x) >> lo), hi - lo + 1);
    }
    public static long sext(long x, int fromw, int tow) { return m(s(x, fromw), tow); }
    public static double b2f(long x, int w) {
        if (w == 32) { return BitConverter.UInt32BitsToSingle((uint) m(x, 32)); }
        return BitConverter.Int64BitsToDouble(x);
    }
    public static long f2b(double f, int w) {
        if (w == 32) { return (long) BitConverter.SingleToUInt32Bits((float) f); }
        return BitConverter.DoubleToInt64Bits(f);
    }
    public static long fadd(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    + BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) + b2f(b, w), w);
    }
    public static long fsub(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    - BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) - b2f(b, w), w);
    }
    public static long fmul(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    * BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) * b2f(b, w), w);
    }
    public static long fdiv(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    / BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) / b2f(b, w), w);
    }
    public static long i2f(long x, int fromw, int w) {
        if (w == 32) {
            return (long) BitConverter.SingleToUInt32Bits((float) s(x, fromw));
        }
        return BitConverter.DoubleToInt64Bits((double) s(x, fromw));
    }
    public static long u2f(long x, int fromw, int w) {
        if (w == 32) {
            return (long) BitConverter.SingleToUInt32Bits((float)(ulong) m(x, fromw));
        }
        return BitConverter.DoubleToInt64Bits((double)(ulong) m(x, fromw));
    }
    public static long fwiden(long x, int fromw, int w) { return f2b(b2f(x, fromw), w); }
'''

CSHARP_MAIN = '''
    public static void Main() {
        StringBuilder answers = new StringBuilder();
        string line = Console.ReadLine();
        while (line != null) {
            string text = line.Trim();
            if (text.Length != 0) {
                string[] parts = text.Split((char[]) null,
                    StringSplitOptions.RemoveEmptyEntries);
                long[] values = new long[parts.Length];
                for (int i = 0; i < parts.Length; i++) {
                    values[i] = unchecked((long) ulong.Parse(parts[i]));
                }
                try {
                    answers.Append(((ulong) %(call)s).ToString());
                    answers.Append("\\n");
                } catch (Exception problem) {
                    answers.Append("RAISE:");
                    answers.Append(problem.GetType().Name);
                    answers.Append("\\n");
                }
            }
            line = Console.ReadLine();
        }
        Console.Write(answers.ToString());
    }
}
'''
