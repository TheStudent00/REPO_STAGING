#!/usr/bin/env python3
"""l3_boundary_gen.py -- generate the BISECTION lanes for log 042.

One source file per language, one compile per language, every target
bisected inside the running process.  A target is a cell from
`boundary_targets.json': one operation, two holders, one side varying
along the whole-number axis, whose two adjacent samples answered in
different classes.  The boundary is the least value at which the
class changes, and this finds it by halving the span.

Decision B3.  The varying operand is a RUN TIME variable of the
holder's own type, not a literal.  A literal would need one compile
per probe, which is sixty compiles per target.  The cost is that a
boundary the compiler creates by folding a literal is invisible here;
the endpoints are re-measured at run time and a disagreement with the
stored answer is printed as ENDPOINT_MISMATCH rather than hidden.

Decision B4.  Phase A is the targets whose FIXED operand is also a
whole holder, so the exact result is an integer and the reference
arithmetic needs nothing but big integers.  The other targets --
fixed operand fractional, text, or a container -- are listed as
deferred with their count.

Usage:
    python3 l3_boundary_gen.py [--limit N] [--langs a,b,c]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.join(HERE, "lanes")

WAVE = ["python", "ruby", "php", "typescript", "dart",
        "java", "kotlin", "csharp", "go", "cpp", "rust"]

# how the varying operand of each whole holder is built from a
# candidate.  `%s' takes a decimal-string / big-integer expression in
# the language's own candidate type.
CAND = {
    "python": {
        "int": "%s",
        "decimal.Decimal": "Decimal(%s)",
        "fractions.Fraction": "Fraction(%s)",
        "ctypes.c_int64": "ctypes.c_int64(%s).value",
    },
    "ruby": {
        "Integer": "(%s)",
        "Rational": "Rational(%s, 1)",
        "BigDecimal": "BigDecimal((%s).to_s)",
    },
    "php": {
        "int": "intval(%s)",
        "GMP (ext-gmp)": "gmp_init(%s)",
        "BCMath string-carried number (ext-bcmath)": "(%s)",
    },
    "typescript": {
        "number": "Number(%s)",
        "bigint": "(%s)",
    },
    "dart": {
        "int": "(%s).toInt()",
        "BigInt": "(%s)",
        "double (whole number)": "(%s).toDouble()",
    },
    "java": {
        "short": "(short)(%s).longValue()",
        "int": "(int)(%s).longValue()",
        "long": "(%s).longValue()",
        "Integer": "Integer.valueOf((int)(%s).longValue())",
        "Long": "Long.valueOf((%s).longValue())",
        "BigInteger": "(%s)",
    },
    "kotlin": {
        "Int": "(%s).toInt()",
        "Long": "(%s).toLong()",
        "ULong": "(%s).toLong().toULong()",
        "BigInteger": "(%s)",
    },
    "csharp": {
        "short": "(short)(long)(%s)",
        "int": "(int)(long)(%s)",
        "long": "(long)(%s)",
        "ulong": "(ulong)(%s)",
        "System.Numerics.BigInteger": "(%s)",
    },
    "go": {
        "int32": "int32(%s.Int64())",
        "int64": "%s.Int64()",
        "int": "int(%s.Int64())",
        "uint64": "%s.Uint64()",
    },
    "cpp": {
        "int32_t": "(int32_t)(%s)",
        "int64_t": "(int64_t)(%s)",
        "uint64_t": "(uint64_t)(%s)",
        "__int128": "(__int128)(%s)",
    },
    "rust": {
        "i32": "((%s) as i32)",
        "i64": "((%s) as i64)",
        "u64": "((%s) as u64)",
        "i128": "((%s) as i128)",
    },
}

# the candidate expression handed to CAND, per language
CANDVAR = {
    "python": "c", "ruby": "c", "php": "$c", "typescript": "c",
    "dart": "c", "java": "c", "kotlin": "c", "csharp": "c", "go": "c",
    "cpp": "c", "rust": "c",
}


def progress(m):
    sys.stdout.write(m + "\n")
    sys.stdout.flush()


def rename(decl, name, lang):
    """The manifests declare a variable called `v'.  Rename it."""
    import re
    if lang == "php":
        return re.sub(r"\$v\b", "$" + name, decl)
    return re.sub(r"\bv\b", name, decl)


def load():
    d = json.load(open(os.path.join(HERE, "boundary_targets.json")))
    forms, decls, pres = {}, {}, {}
    for lang in set(r["language"] for r in d["rows"]):
        m = json.load(open(os.path.join(HERE, "manifest_%s.json" % lang)))
        for h in m["holders"]:
            forms[(lang, h["holder"])] = h["form"]
            pres[(lang, h["holder"])] = h.get("pre", "")
            for vc, txt in h["value_classes"]:
                decls[(lang, h["holder"], vc)] = txt
    return d, forms, decls, pres


# Decision B5.  Two operation families are held out of phase A because
# one probe of them can cost unbounded time or memory on a holder with
# no width: `**' raises a number to a number the axis makes enormous,
# and `<<' / `>>' shift by one.  Sixty probes of `42 ** 9007199254740993'
# is not a measurement, it is a hang.  They are listed as deferred.
UNBOUNDED_OPS = {"**"}
SHIFTS = {"<<", ">>"}
WIDTHLESS = {
    ("python", "int"), ("python", "decimal.Decimal"),
    ("python", "fractions.Fraction"), ("python", "ctypes.c_int64"),
    ("ruby", "Integer"), ("ruby", "Rational"), ("ruby", "BigDecimal"),
    ("php", "GMP (ext-gmp)"),
    ("php", "BCMath string-carried number (ext-bcmath)"),
    ("dart", "BigInt"), ("typescript", "bigint"),
    ("java", "BigInteger"), ("kotlin", "BigInteger"),
    ("csharp", "System.Numerics.BigInteger"),
}


def unbounded(r):
    if r["language"] == "rust" and r["operation"] == "..":
        return "the range operator carries no answer class here"
    if r["operation"] in UNBOUNDED_OPS:
        return "unbounded operation"
    if r["operation"] in SHIFTS and (
            (r["language"], r["vary_holder"]) in WIDTHLESS or
            (r["language"], r["fixed_holder"]) in WIDTHLESS):
        return "shift on a holder with no width"
    return None


def phase_a(d, forms):
    keep, defer = [], []
    for n, r in enumerate(d["rows"]):
        fh = r["lhs_holder"] if r["varying_side"] == "rhs" else r["rhs_holder"]
        vh = r["rhs_holder"] if r["varying_side"] == "rhs" else r["lhs_holder"]
        r = dict(r, tid=n, fixed_holder=fh, vary_holder=vh)
        if forms.get((r["language"], fh)) != "whole":
            r["deferred"] = "fixed operand is not a whole holder"
            defer.append(r)
        elif vh not in CAND.get(r["language"], {}):
            r["deferred"] = "no phase-A harness for this language"
            defer.append(r)
        elif unbounded(r):
            r["deferred"] = unbounded(r)
            defer.append(r)
        else:
            keep.append(r)
    return keep, defer


# ---------------------------------------------------------------- emit

def expr(lang, r, a_txt, b_txt):
    """The operation applied, with the two operand names."""
    op = r["operation"]
    if lang == "php":
        return "(($%s) %s ($%s))" % (a_txt, op, b_txt)
    return "((%s) %s (%s))" % (a_txt, op, b_txt)


def sides(r):
    """Return (varying name, fixed name) in lhs/rhs order."""
    if r["varying_side"] == "lhs":
        return "a", "b", "a", "b"      # vary=a fixed=b, expr a op b
    return "b", "a", "a", "b"          # vary=b fixed=a, expr a op b


HEAD = {}

# ------------------------------------------------------------- python

HEAD["python"] = r'''
import sys, ctypes, math
from decimal import Decimal
from fractions import Fraction

EXACT = {"+", "-", "*", "<", "<=", ">", ">=", "==", "!="}

def want(op, a, b):
    if op not in EXACT: return None
    if op == "+": return a + b
    if op == "-": return a - b
    if op == "*": return a * b
    return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b,
            "==": a == b, "!=": a != b}[op]

def asnum(r):
    if isinstance(r, bool): return r
    if isinstance(r, int): return Fraction(r)
    if isinstance(r, float):
        if r != r or r in (float("inf"), float("-inf")): return None
        return Fraction(r)
    if isinstance(r, Decimal):
        try: return Fraction(r)
        except Exception: return None
    if isinstance(r, Fraction): return r
    return None

def fid(r, op, a, b):
    w = want(op, a, b)
    if w is None: return "na"
    g = asnum(r)
    if g is None: return "na"
    if isinstance(w, bool) or isinstance(g, bool):
        if not (isinstance(w, bool) and isinstance(g, bool)): return "na"
        return "exact" if w == g else "inexact"
    return "exact" if g == Fraction(w) else "inexact"

def sig(fn, c, op, a, b):
    try:
        r = fn(c)
    except BaseException as e:
        return "raise|%s|na" % type(e).__name__
    return "answer|%s|%s" % (type(r).__name__, fid(r, op, a, b))
'''

FOOT_PY = r'''
def bisect(tid, fn, op, lov, hiv, fixed, vary_is_lhs):
    def s(c):
        a = c if vary_is_lhs else fixed
        b = fixed if vary_is_lhs else c
        return sig(lambda x: fn(x), c, op, Fraction(a), Fraction(b))
    lo, hi = lov, hiv
    slo, shi = s(lo), s(hi)
    probes = 2
    if slo == shi:
        print("N|%d|%s|%s" % (tid, slo, shi)); return probes
    other = set()
    while hi - lo > 1:
        mid = (lo + hi) // 2
        sm = s(mid); probes += 1
        if sm == slo: lo = mid
        else:
            if sm != shi: other.add(sm)
            hi = mid
    print("B|%d|%d|%d|%s|%s|%d|%s" %
          (tid, lo, hi, slo, shi, probes, ";".join(sorted(other))))
    return probes

def main():
    total = 0
    n = len(TARGETS)
    for k, t in enumerate(TARGETS):
        total += t()
        if (k + 1) % 25 == 0 or k + 1 == n:
            sys.stderr.write("progress %d/%d probes=%d\n" % (k + 1, n, total))
            sys.stderr.flush()
    sys.stderr.write("DONE targets=%d probes=%d\n" % (n, total))

main()
'''

# --------------------------------------------------------------- ruby

HEAD["ruby"] = r'''
require 'bigdecimal'
require 'rational'
EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="]

def want(op, a, b)
  return nil unless EXACT.include?(op)
  case op
  when "+" then a + b
  when "-" then a - b
  when "*" then a * b
  when "<" then a < b
  when "<=" then a <= b
  when ">" then a > b
  when ">=" then a >= b
  when "==" then a == b
  when "!=" then a != b
  end
end

def asnum(r)
  return r if r == true || r == false
  return Rational(r) if r.is_a?(Integer)
  if r.is_a?(Float)
    return nil if r.nan? || r.infinite?
    return Rational(r)
  end
  return r if r.is_a?(Rational)
  return Rational(r.to_s) if r.is_a?(BigDecimal) rescue return nil
  nil
end

def fid(r, op, a, b)
  w = want(op, a, b)
  return "na" if w.nil?
  g = asnum(r)
  return "na" if g.nil?
  if w == true || w == false
    return "na" unless g == true || g == false
    return w == g ? "exact" : "inexact"
  end
  return "na" if g == true || g == false
  g == Rational(w) ? "exact" : "inexact"
end

def sig(c, op, a, b)
  begin
    r = yield c
  rescue Exception => e
    return "raise|#{e.class}|na"
  end
  "answer|#{r.class}|#{fid(r, op, a, b)}"
end
'''

FOOT_RB = r'''
def bisect(tid, op, lov, hiv, fixed, vary_is_lhs, &fn)
  s = lambda do |c|
    a = vary_is_lhs ? c : fixed
    b = vary_is_lhs ? fixed : c
    sig(c, op, Rational(a), Rational(b), &fn)
  end
  lo = lov; hi = hiv
  slo = s.call(lo); shi = s.call(hi)
  probes = 2
  if slo == shi
    puts "N|#{tid}|#{slo}|#{shi}"
    return probes
  end
  other = {}
  while hi - lo > 1
    mid = (lo + hi) / 2
    sm = s.call(mid); probes += 1
    if sm == slo then lo = mid
    else
      other[sm] = true if sm != shi
      hi = mid
    end
  end
  puts "B|#{tid}|#{lo}|#{hi}|#{slo}|#{shi}|#{probes}|#{other.keys.sort.join(';')}"
  probes
end

total = 0
TARGETS.each_with_index do |t, k|
  total += t.call
  if (k + 1) % 25 == 0 || k + 1 == TARGETS.length
    STDERR.puts "progress #{k + 1}/#{TARGETS.length} probes=#{total}"
  end
end
STDERR.puts "DONE targets=#{TARGETS.length} probes=#{total}"
'''

# ---------------------------------------------------------------- php

HEAD["php"] = r'''<?php
// this php has neither ext-gmp nor ext-bcmath, so the reference
// arithmetic is decimal strings, done here.  bi_* take and give
// strings like "-9223372036854775808".
function bi_norm($s) {
  $s = trim($s); $neg = false;
  if ($s !== "" && ($s[0] === "-" || $s[0] === "+")) {
    $neg = $s[0] === "-"; $s = substr($s, 1);
  }
  $s = ltrim($s, "0"); if ($s === "") { $s = "0"; $neg = false; }
  return ($neg ? "-" : "") . $s;
}
function bi_neg($a) {
  $a = bi_norm($a);
  if ($a === "0") return "0";
  return $a[0] === "-" ? substr($a, 1) : "-" . $a;
}
function bi_ucmp($a, $b) {
  if (strlen($a) != strlen($b)) return strlen($a) < strlen($b) ? -1 : 1;
  return strcmp($a, $b) <=> 0;
}
function bi_uadd($a, $b) {
  $r = ""; $c = 0; $i = strlen($a) - 1; $j = strlen($b) - 1;
  while ($i >= 0 || $j >= 0 || $c) {
    $d = $c;
    if ($i >= 0) $d += ord($a[$i--]) - 48;
    if ($j >= 0) $d += ord($b[$j--]) - 48;
    $c = intdiv($d, 10); $r = chr(48 + $d % 10) . $r;
  }
  return bi_norm($r);
}
function bi_usub($a, $b) {          // a >= b
  $r = ""; $c = 0; $i = strlen($a) - 1; $j = strlen($b) - 1;
  while ($i >= 0) {
    $d = (ord($a[$i--]) - 48) - $c - ($j >= 0 ? ord($b[$j--]) - 48 : 0);
    if ($d < 0) { $d += 10; $c = 1; } else { $c = 0; }
    $r = chr(48 + $d) . $r;
  }
  return bi_norm($r);
}
function bi_umul($a, $b) {
  $n = strlen($a); $m = strlen($b); $p = array_fill(0, $n + $m, 0);
  for ($i = $n - 1; $i >= 0; $i--) {
    $x = ord($a[$i]) - 48;
    for ($j = $m - 1; $j >= 0; $j--) {
      $p[$i + $j + 1] += $x * (ord($b[$j]) - 48);
    }
  }
  for ($k = $n + $m - 1; $k > 0; $k--) {
    $p[$k - 1] += intdiv($p[$k], 10); $p[$k] %= 10;
  }
  $s = ""; foreach ($p as $d) $s .= chr(48 + $d);
  return bi_norm($s);
}
function bi_parts($a) {
  $a = bi_norm($a);
  if ($a[0] === "-") return [true, substr($a, 1)];
  return [false, $a];
}
function bi_add($a, $b) {
  list($sa, $ua) = bi_parts($a); list($sb, $ub) = bi_parts($b);
  if ($sa === $sb) { $r = bi_uadd($ua, $ub); return $sa ? bi_neg($r) : $r; }
  $c = bi_ucmp($ua, $ub);
  if ($c === 0) return "0";
  if ($c > 0) { $r = bi_usub($ua, $ub); return $sa ? bi_neg($r) : $r; }
  $r = bi_usub($ub, $ua); return $sb ? bi_neg($r) : $r;
}
function bi_sub($a, $b) { return bi_add($a, bi_neg($b)); }
function bi_mul($a, $b) {
  list($sa, $ua) = bi_parts($a); list($sb, $ub) = bi_parts($b);
  $r = bi_umul($ua, $ub);
  if ($r === "0") return "0";
  return ($sa xor $sb) ? bi_neg($r) : $r;
}
function bi_cmp($a, $b) {
  list($sa, $ua) = bi_parts($a); list($sb, $ub) = bi_parts($b);
  if ($sa !== $sb) return $sa ? -1 : 1;
  $c = bi_ucmp($ua, $ub);
  return $sa ? -$c : $c;
}
function bi_half($a) {              // floor(a / 2), a >= 0
  list($sa, $u) = bi_parts($a); $r = ""; $c = 0;
  for ($i = 0; $i < strlen($u); $i++) {
    $d = $c * 10 + ord($u[$i]) - 48;
    $r .= chr(48 + intdiv($d, 2)); $c = $d % 2;
  }
  return bi_norm($r);
}

$EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="];

function wantv($op, $a, $b) {
  global $EXACT;
  if (!in_array($op, $EXACT, true)) return null;
  switch ($op) {
    case "+": return bi_add($a, $b);
    case "-": return bi_sub($a, $b);
    case "*": return bi_mul($a, $b);
    case "<": return bi_cmp($a, $b) < 0;
    case "<=": return bi_cmp($a, $b) <= 0;
    case ">": return bi_cmp($a, $b) > 0;
    case ">=": return bi_cmp($a, $b) >= 0;
    case "==": return bi_cmp($a, $b) == 0;
    case "!=": return bi_cmp($a, $b) != 0;
  }
  return null;
}

function asint($r) {
  if (is_bool($r)) return $r;
  if (is_int($r)) return (string)$r;
  if (is_float($r)) {
    if (is_nan($r) || is_infinite($r)) return null;
    if (floor($r) != $r) return "NONINT";
    return bi_norm(sprintf("%.0f", $r));
  }
  if (is_string($r) && preg_match('/^-?[0-9]+$/', $r)) return bi_norm($r);
  return null;
}

function fidv($r, $op, $a, $b) {
  $w = wantv($op, $a, $b);
  if ($w === null) return "na";
  $g = asint($r);
  if ($g === null) return "na";
  if (is_bool($w)) {
    if (!is_bool($g)) return "na";
    return $w === $g ? "exact" : "inexact";
  }
  if (is_bool($g)) return "na";
  if ($g === "NONINT") return "inexact";
  return bi_cmp($g, $w) == 0 ? "exact" : "inexact";
}

function tname($r) {
  if (is_object($r)) return get_class($r);
  return gettype($r);
}

function sigv($fn, $c, $op, $a, $b) {
  try {
    $r = $fn($c);
  } catch (\Throwable $e) {
    return "raise|" . get_class($e) . "|na";
  }
  return "answer|" . tname($r) . "|" . fidv($r, $op, $a, $b);
}
'''

FOOT_PHP = r'''
function bisect($tid, $fn, $op, $lov, $hiv, $fixed, $vary_is_lhs) {
  $s = function ($c) use ($fn, $op, $fixed, $vary_is_lhs) {
    $a = $vary_is_lhs ? $c : $fixed;
    $b = $vary_is_lhs ? $fixed : $c;
    return sigv($fn, $c, $op, $a, $b);
  };
  $lo = bi_norm($lov); $hi = bi_norm($hiv);
  $slo = $s($lo); $shi = $s($hi);
  $probes = 2;
  if ($slo === $shi) { echo "N|$tid|$slo|$shi\n"; return $probes; }
  $other = [];
  while (bi_cmp(bi_sub($hi, $lo), "1") > 0) {
    $mid = bi_half(bi_add($lo, $hi));
    $sm = $s($mid); $probes++;
    if ($sm === $slo) { $lo = $mid; }
    else { if ($sm !== $shi) $other[$sm] = true; $hi = $mid; }
  }
  $o = array_keys($other); sort($o);
  echo "B|$tid|" . $lo . "|" . $hi .
       "|$slo|$shi|$probes|" . implode(";", $o) . "\n";
  return $probes;
}

$total = 0;
$n = count($TARGETS);
foreach ($TARGETS as $k => $t) {
  $total += $t();
  if (($k + 1) % 25 == 0 || $k + 1 == $n)
    fwrite(STDERR, "progress " . ($k + 1) . "/$n probes=$total\n");
}
fwrite(STDERR, "DONE targets=$n probes=$total\n");
'''

# --------------------------------------------------------- typescript

HEAD["typescript"] = r'''
const EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="];

function wantv(op: string, a: bigint, b: bigint): any {
  if (EXACT.indexOf(op) < 0) return null;
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "<": return a < b;
    case "<=": return a <= b;
    case ">": return a > b;
    case ">=": return a >= b;
    case "==": return a === b;
    case "!=": return a !== b;
  }
  return null;
}

function asint(r: any): any {
  if (typeof r === "boolean") return r;
  if (typeof r === "bigint") return r;
  if (typeof r === "number") {
    if (!isFinite(r)) return null;
    if (Math.floor(r) !== r) return "NONINT";
    return BigInt(r);
  }
  return null;
}

function fidv(r: any, op: string, a: bigint, b: bigint): string {
  const w = wantv(op, a, b);
  if (w === null) return "na";
  const g = asint(r);
  if (g === null) return "na";
  if (typeof w === "boolean") {
    if (typeof g !== "boolean") return "na";
    return w === g ? "exact" : "inexact";
  }
  if (typeof g === "boolean") return "na";
  if (g === "NONINT") return "inexact";
  return (g as bigint) === (w as bigint) ? "exact" : "inexact";
}

function tname(r: any): string {
  if (r === null) return "null";
  const t = typeof r;
  if (t === "object") return (r as any).constructor ?
      (r as any).constructor.name : "object";
  return t;
}

function sigv(fn: (c: bigint) => any, c: bigint, op: string,
              a: bigint, b: bigint): string {
  let r: any;
  try { r = fn(c); }
  catch (e: any) {
    return "raise|" + (e && e.constructor ? e.constructor.name : "?") + "|na";
  }
  return "answer|" + tname(r) + "|" + fidv(r, op, a, b);
}

function bisect(tid: number, fn: (c: bigint) => any, op: string,
                lov: bigint, hiv: bigint, fixed: bigint,
                varyIsLhs: boolean): number {
  const s = (c: bigint) => {
    const a = varyIsLhs ? c : fixed;
    const b = varyIsLhs ? fixed : c;
    return sigv(fn, c, op, a, b);
  };
  let lo = lov, hi = hiv;
  const slo = s(lo), shi = s(hi);
  let probes = 2;
  if (slo === shi) { console.log("N|" + tid + "|" + slo + "|" + shi); return probes; }
  const other: any = {};
  while (hi - lo > 1n) {
    const mid = (lo + hi) / 2n;
    const sm = s(mid); probes++;
    if (sm === slo) lo = mid;
    else { if (sm !== shi) other[sm] = true; hi = mid; }
  }
  console.log("B|" + tid + "|" + lo + "|" + hi + "|" + slo + "|" + shi +
              "|" + probes + "|" + Object.keys(other).sort().join(";"));
  return probes;
}
'''

FOOT_TS = r'''
let total = 0;
for (let k = 0; k < TARGETS.length; k++) {
  total += TARGETS[k]();
  if ((k + 1) % 25 === 0 || k + 1 === TARGETS.length)
    process.stderr.write("progress " + (k + 1) + "/" + TARGETS.length +
                         " probes=" + total + "\n");
}
process.stderr.write("DONE targets=" + TARGETS.length + " probes=" + total + "\n");
'''

# --------------------------------------------------------------- dart

HEAD["dart"] = r'''
import 'dart:io';

const EXACT = ["+", "-", "*", "<", "<=", ">", ">=", "==", "!="];

dynamic wantv(String op, BigInt a, BigInt b) {
  if (!EXACT.contains(op)) return null;
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "<": return a < b;
    case "<=": return a <= b;
    case ">": return a > b;
    case ">=": return a >= b;
    case "==": return a == b;
    case "!=": return a != b;
  }
  return null;
}

dynamic asint(dynamic r) {
  if (r is bool) return r;
  if (r is BigInt) return r;
  if (r is int) return BigInt.from(r);
  if (r is double) {
    if (r.isNaN || r.isInfinite) return null;
    if (r != r.truncateToDouble()) return "NONINT";
    return BigInt.from(r);
  }
  return null;
}

String fidv(dynamic r, String op, BigInt a, BigInt b) {
  var w = wantv(op, a, b);
  if (w == null) return "na";
  var g = asint(r);
  if (g == null) return "na";
  if (w is bool) {
    if (g is! bool) return "na";
    return w == g ? "exact" : "inexact";
  }
  if (g is bool) return "na";
  if (g == "NONINT") return "inexact";
  return (g as BigInt) == (w as BigInt) ? "exact" : "inexact";
}

String sigv(dynamic Function(BigInt) fn, BigInt c, String op,
            BigInt a, BigInt b) {
  dynamic r;
  try { r = fn(c); }
  catch (e) { return "raise|" + e.runtimeType.toString() + "|na"; }
  return "answer|" + r.runtimeType.toString() + "|" + fidv(r, op, a, b);
}

int bisect(int tid, dynamic Function(BigInt) fn, String op,
           BigInt lov, BigInt hiv, BigInt fixed, bool varyIsLhs) {
  String s(BigInt c) {
    var a = varyIsLhs ? c : fixed;
    var b = varyIsLhs ? fixed : c;
    return sigv(fn, c, op, a, b);
  }
  var lo = lov, hi = hiv;
  var slo = s(lo), shi = s(hi);
  var probes = 2;
  if (slo == shi) { print("N|$tid|$slo|$shi"); return probes; }
  var other = <String>{};
  while (hi - lo > BigInt.one) {
    var mid = (lo + hi) ~/ BigInt.two;
    var sm = s(mid); probes++;
    if (sm == slo) { lo = mid; }
    else { if (sm != shi) other.add(sm); hi = mid; }
  }
  var o = other.toList()..sort();
  print("B|$tid|$lo|$hi|$slo|$shi|$probes|${o.join(';')}");
  return probes;
}
'''

FOOT_DART = r'''
void main() {
  var total = 0;
  for (var k = 0; k < TARGETS.length; k++) {
    total += TARGETS[k]();
    if ((k + 1) % 25 == 0 || k + 1 == TARGETS.length)
      stderr.writeln("progress ${k + 1}/${TARGETS.length} probes=$total");
  }
  stderr.writeln("DONE targets=${TARGETS.length} probes=$total");
}
'''

# --------------------------------------------------------------- java

HEAD["java"] = r'''
import java.math.BigInteger;
import java.util.*;
import java.util.function.Function;

public class BND {
  static final List<String> EXACT = Arrays.asList(
      "+", "-", "*", "<", "<=", ">", ">=", "==", "!=");

  static Object wantv(String op, BigInteger a, BigInteger b) {
    if (!EXACT.contains(op)) return null;
    switch (op) {
      case "+": return a.add(b);
      case "-": return a.subtract(b);
      case "*": return a.multiply(b);
      case "<": return a.compareTo(b) < 0;
      case "<=": return a.compareTo(b) <= 0;
      case ">": return a.compareTo(b) > 0;
      case ">=": return a.compareTo(b) >= 0;
      case "==": return a.compareTo(b) == 0;
      case "!=": return a.compareTo(b) != 0;
    }
    return null;
  }

  static Object asint(Object r) {
    if (r instanceof Boolean) return r;
    if (r instanceof BigInteger) return r;
    if (r instanceof Short || r instanceof Integer || r instanceof Long)
      return BigInteger.valueOf(((Number) r).longValue());
    if (r instanceof Double || r instanceof Float) {
      double d = ((Number) r).doubleValue();
      if (Double.isNaN(d) || Double.isInfinite(d)) return null;
      if (d != Math.floor(d)) return "NONINT";
      return new java.math.BigDecimal(d).toBigInteger();
    }
    return null;
  }

  static String fidv(Object r, String op, BigInteger a, BigInteger b) {
    Object w = wantv(op, a, b);
    if (w == null) return "na";
    Object g = asint(r);
    if (g == null) return "na";
    if (w instanceof Boolean) {
      if (!(g instanceof Boolean)) return "na";
      return w.equals(g) ? "exact" : "inexact";
    }
    if (g instanceof Boolean) return "na";
    if ("NONINT".equals(g)) return "inexact";
    return ((BigInteger) g).equals((BigInteger) w) ? "exact" : "inexact";
  }

  static String sigv(Function<BigInteger, Object> fn, BigInteger c,
                     String op, BigInteger a, BigInteger b) {
    Object r;
    try { r = fn.apply(c); }
    catch (Throwable t) { return "raise|" + t.getClass().getName() + "|na"; }
    String tn = (r == null) ? "null" : r.getClass().getSimpleName();
    return "answer|" + tn + "|" + fidv(r, op, a, b);
  }

  static int bisect(int tid, Function<BigInteger, Object> fn, String op,
                    BigInteger lov, BigInteger hiv, BigInteger fixed,
                    boolean varyIsLhs) {
    java.util.function.Function<BigInteger, String> s = (c) -> {
      BigInteger a = varyIsLhs ? c : fixed;
      BigInteger b = varyIsLhs ? fixed : c;
      return sigv(fn, c, op, a, b);
    };
    BigInteger lo = lov, hi = hiv;
    String slo = s.apply(lo), shi = s.apply(hi);
    int probes = 2;
    if (slo.equals(shi)) {
      System.out.println("N|" + tid + "|" + slo + "|" + shi);
      return probes;
    }
    TreeSet<String> other = new TreeSet<String>();
    while (hi.subtract(lo).compareTo(BigInteger.ONE) > 0) {
      BigInteger mid = lo.add(hi).shiftRight(1);
      String sm = s.apply(mid); probes++;
      if (sm.equals(slo)) lo = mid;
      else { if (!sm.equals(shi)) other.add(sm); hi = mid; }
    }
    System.out.println("B|" + tid + "|" + lo + "|" + hi + "|" + slo + "|" +
                       shi + "|" + probes + "|" + String.join(";", other));
    return probes;
  }
'''

FOOT_JAVA = r'''
  public static void main(String[] args) {
    int total = 0;
    int n = TARGETS.size();
    for (int k = 0; k < n; k++) {
      total += TARGETS.get(k).get();
      if ((k + 1) % 25 == 0 || k + 1 == n)
        System.err.println("progress " + (k + 1) + "/" + n +
                           " probes=" + total);
    }
    System.err.println("DONE targets=" + n + " probes=" + total);
  }
}
'''

# ------------------------------------------------------------- kotlin

HEAD["kotlin"] = r'''
import java.math.BigInteger
import java.math.BigDecimal

val EXACT = listOf("+", "-", "*", "<", "<=", ">", ">=", "==", "!=")

fun wantv(op: String, a: BigInteger, b: BigInteger): Any? = when (op) {
  "+" -> a.add(b)
  "-" -> a.subtract(b)
  "*" -> a.multiply(b)
  "<" -> a.compareTo(b) < 0
  "<=" -> a.compareTo(b) <= 0
  ">" -> a.compareTo(b) > 0
  ">=" -> a.compareTo(b) >= 0
  "==" -> a.compareTo(b) == 0
  "!=" -> a.compareTo(b) != 0
  else -> null
}

fun asint(r: Any?): Any? = when (r) {
  is Boolean -> r
  is BigInteger -> r
  is Byte, is Short, is Int, is Long -> BigInteger.valueOf((r as Number).toLong())
  is ULong -> BigInteger(r.toString())
  is UInt -> BigInteger(r.toString())
  is Double -> if (r.isNaN() || r.isInfinite()) null
               else if (r != Math.floor(r)) "NONINT" else BigDecimal(r).toBigInteger()
  is Float -> asint(r.toDouble())
  else -> null
}

fun fidv(r: Any?, op: String, a: BigInteger, b: BigInteger): String {
  val w = wantv(op, a, b) ?: return "na"
  val g = asint(r) ?: return "na"
  if (w is Boolean) {
    if (g !is Boolean) return "na"
    return if (w == g) "exact" else "inexact"
  }
  if (g is Boolean) return "na"
  if (g == "NONINT") return "inexact"
  return if ((g as BigInteger) == (w as BigInteger)) "exact" else "inexact"
}

fun sigv(fn: (BigInteger) -> Any?, c: BigInteger, op: String,
         a: BigInteger, b: BigInteger): String {
  val r: Any?
  try { r = fn(c) }
  catch (t: Throwable) { return "raise|" + t.javaClass.name + "|na" }
  val tn = if (r == null) "null" else r!!::class.simpleName
  return "answer|" + tn + "|" + fidv(r, op, a, b)
}

fun bisect(tid: Int, fn: (BigInteger) -> Any?, op: String,
           lov: BigInteger, hiv: BigInteger, fixed: BigInteger,
           varyIsLhs: Boolean): Int {
  fun s(c: BigInteger): String {
    val a = if (varyIsLhs) c else fixed
    val b = if (varyIsLhs) fixed else c
    return sigv(fn, c, op, a, b)
  }
  var lo = lov; var hi = hiv
  val slo = s(lo); val shi = s(hi)
  var probes = 2
  if (slo == shi) { println("N|$tid|$slo|$shi"); return probes }
  val other = sortedSetOf<String>()
  while (hi.subtract(lo) > BigInteger.ONE) {
    val mid = lo.add(hi).shiftRight(1)
    val sm = s(mid); probes++
    if (sm == slo) lo = mid
    else { if (sm != shi) other.add(sm); hi = mid }
  }
  println("B|$tid|$lo|$hi|$slo|$shi|$probes|" + other.joinToString(";"))
  return probes
}
'''

FOOT_KT = r'''
fun main() {
  var total = 0
  val n = TARGETS.size
  for (k in 0 until n) {
    total += TARGETS[k]()
    if ((k + 1) % 25 == 0 || k + 1 == n)
      System.err.println("progress ${k + 1}/$n probes=$total")
  }
  System.err.println("DONE targets=$n probes=$total")
}
'''

# ------------------------------------------------------------- csharp

HEAD["csharp"] = r'''
using System;
using System.Collections.Generic;
using System.Numerics;

public static class BND {
  static readonly HashSet<string> EXACT = new HashSet<string>(
      new string[] {"+", "-", "*", "<", "<=", ">", ">=", "==", "!="});

  static object wantv(string op, BigInteger a, BigInteger b) {
    if (!EXACT.Contains(op)) return null;
    switch (op) {
      case "+": return a + b;
      case "-": return a - b;
      case "*": return a * b;
      case "<": return a < b;
      case "<=": return a <= b;
      case ">": return a > b;
      case ">=": return a >= b;
      case "==": return a == b;
      case "!=": return a != b;
    }
    return null;
  }

  static object asint(object r) {
    if (r is bool) return r;
    if (r is BigInteger) return r;
    if (r is short || r is int || r is long)
      return new BigInteger(Convert.ToInt64(r));
    if (r is ushort || r is uint || r is ulong)
      return new BigInteger(Convert.ToUInt64(r));
    if (r is double || r is float) {
      double d = Convert.ToDouble(r);
      if (double.IsNaN(d) || double.IsInfinity(d)) return null;
      if (d != Math.Floor(d)) return "NONINT";
      return new BigInteger(d);
    }
    if (r is decimal) {
      decimal m = (decimal) r;
      if (m != Math.Floor(m)) return "NONINT";
      return new BigInteger(m);
    }
    return null;
  }

  static string fidv(object r, string op, BigInteger a, BigInteger b) {
    object w = wantv(op, a, b);
    if (w == null) return "na";
    object g = asint(r);
    if (g == null) return "na";
    if (w is bool) {
      if (!(g is bool)) return "na";
      return ((bool) w) == ((bool) g) ? "exact" : "inexact";
    }
    if (g is bool) return "na";
    if ((g as string) == "NONINT") return "inexact";
    return ((BigInteger) g) == ((BigInteger) w) ? "exact" : "inexact";
  }

  static string sigv(Func<BigInteger, object> fn, BigInteger c, string op,
                     BigInteger a, BigInteger b) {
    object r;
    try { r = fn(c); }
    catch (Exception e) { return "raise|" + e.GetType().Name + "|na"; }
    string tn = (r == null) ? "null" : r.GetType().Name;
    return "answer|" + tn + "|" + fidv(r, op, a, b);
  }

  public static int bisect(int tid, Func<BigInteger, object> fn, string op,
                           BigInteger lov, BigInteger hiv, BigInteger fixedv,
                           bool varyIsLhs) {
    Func<BigInteger, string> s = (c) => {
      BigInteger a = varyIsLhs ? c : fixedv;
      BigInteger b = varyIsLhs ? fixedv : c;
      return sigv(fn, c, op, a, b);
    };
    BigInteger lo = lov, hi = hiv;
    string slo = s(lo), shi = s(hi);
    int probes = 2;
    if (slo == shi) { Console.WriteLine("N|" + tid + "|" + slo + "|" + shi); return probes; }
    SortedSet<string> other = new SortedSet<string>();
    while (hi - lo > 1) {
      BigInteger mid = (lo + hi) / 2;
      string sm = s(mid); probes++;
      if (sm == slo) lo = mid;
      else { if (sm != shi) other.Add(sm); hi = mid; }
    }
    Console.WriteLine("B|" + tid + "|" + lo + "|" + hi + "|" + slo + "|" +
                      shi + "|" + probes + "|" + string.Join(";", other));
    return probes;
  }
'''

FOOT_CS = r'''
  public static void Main() {
    int total = 0;
    int n = TARGETS.Count;
    for (int k = 0; k < n; k++) {
      total += TARGETS[k]();
      if ((k + 1) % 25 == 0 || k + 1 == n)
        Console.Error.WriteLine("progress " + (k + 1) + "/" + n +
                                " probes=" + total);
    }
    Console.Error.WriteLine("DONE targets=" + n + " probes=" + total);
  }
}
'''

# ----------------------------------------------------------------- go

HEAD["go"] = r'''
package main

import (
	"fmt"
	"math"
	"math/big"
	"os"
	"reflect"
	"sort"
	"strings"
)

var EXACT = map[string]bool{"+": true, "-": true, "*": true, "<": true,
	"<=": true, ">": true, ">=": true, "==": true, "!=": true}

func wantv(op string, a, b *big.Int) interface{} {
	if !EXACT[op] {
		return nil
	}
	switch op {
	case "+":
		return new(big.Int).Add(a, b)
	case "-":
		return new(big.Int).Sub(a, b)
	case "*":
		return new(big.Int).Mul(a, b)
	case "<":
		return a.Cmp(b) < 0
	case "<=":
		return a.Cmp(b) <= 0
	case ">":
		return a.Cmp(b) > 0
	case ">=":
		return a.Cmp(b) >= 0
	case "==":
		return a.Cmp(b) == 0
	case "!=":
		return a.Cmp(b) != 0
	}
	return nil
}

func asint(r interface{}) interface{} {
	switch v := r.(type) {
	case bool:
		return v
	case int:
		return big.NewInt(int64(v))
	case int32:
		return big.NewInt(int64(v))
	case int64:
		return big.NewInt(v)
	case uint64:
		return new(big.Int).SetUint64(v)
	case float64:
		if math.IsNaN(v) || math.IsInf(v, 0) {
			return nil
		}
		if v != math.Trunc(v) {
			return "NONINT"
		}
		f := new(big.Float).SetFloat64(v)
		i, _ := f.Int(nil)
		return i
	case float32:
		return asint(float64(v))
	}
	return nil
}

func fidv(r interface{}, op string, a, b *big.Int) string {
	w := wantv(op, a, b)
	if w == nil {
		return "na"
	}
	g := asint(r)
	if g == nil {
		return "na"
	}
	if wb, ok := w.(bool); ok {
		gb, ok2 := g.(bool)
		if !ok2 {
			return "na"
		}
		if wb == gb {
			return "exact"
		}
		return "inexact"
	}
	if _, ok := g.(bool); ok {
		return "na"
	}
	if s, ok := g.(string); ok && s == "NONINT" {
		return "inexact"
	}
	if g.(*big.Int).Cmp(w.(*big.Int)) == 0 {
		return "exact"
	}
	return "inexact"
}

func sigv(fn func(*big.Int) interface{}, c *big.Int, op string,
	a, b *big.Int) (out string) {
	defer func() {
		if e := recover(); e != nil {
			out = fmt.Sprintf("raise|%v|na", e)
		}
	}()
	r := fn(c)
	tn := "null"
	if r != nil {
		tn = reflect.TypeOf(r).String()
	}
	return "answer|" + tn + "|" + fidv(r, op, a, b)
}

func bisect(tid int, fn func(*big.Int) interface{}, op string,
	lov, hiv, fixedv *big.Int, varyIsLhs bool) int {
	s := func(c *big.Int) string {
		a, b := c, fixedv
		if !varyIsLhs {
			a, b = fixedv, c
		}
		return sigv(fn, c, op, a, b)
	}
	lo := new(big.Int).Set(lov)
	hi := new(big.Int).Set(hiv)
	slo, shi := s(lo), s(hi)
	probes := 2
	if slo == shi {
		fmt.Printf("N|%d|%s|%s\n", tid, slo, shi)
		return probes
	}
	other := map[string]bool{}
	one := big.NewInt(1)
	for new(big.Int).Sub(hi, lo).Cmp(one) > 0 {
		mid := new(big.Int).Rsh(new(big.Int).Add(lo, hi), 1)
		sm := s(mid)
		probes++
		if sm == slo {
			lo = mid
		} else {
			if sm != shi {
				other[sm] = true
			}
			hi = mid
		}
	}
	keys := []string{}
	for k := range other {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	fmt.Printf("B|%d|%s|%s|%s|%s|%d|%s\n", tid, lo.String(), hi.String(),
		slo, shi, probes, strings.Join(keys, ";"))
	return probes
}
'''

FOOT_GO = r'''
func main() {
	total := 0
	n := len(TARGETS)
	for k := 0; k < n; k++ {
		total += TARGETS[k]()
		if (k+1)%25 == 0 || k+1 == n {
			fmt.Fprintf(os.Stderr, "progress %d/%d probes=%d\n", k+1, n, total)
		}
	}
	fmt.Fprintf(os.Stderr, "DONE targets=%d probes=%d\n", n, total)
}
'''


# ----------------------------------------------------------------- cpp

HEAD["cpp"] = r'''
#include <cstdint>
#include <cstdio>
#include <cmath>
#include <csetjmp>
#include <csignal>
#include <string>
#include <set>
#include <vector>
#include <type_traits>

typedef __int128 i128;
typedef unsigned __int128 u128;

static sigjmp_buf JB;
static void onfpe(int) { siglongjmp(JB, 1); }

static std::string dec(u128 v) {
  if (v == 0) return "0";
  std::string s;
  while (v) { s.insert(s.begin(), char('0' + (int)(v % 10))); v /= 10; }
  return s;
}
static std::string decs(i128 v) {
  if (v < 0) return "-" + dec((u128)(-v));
  return dec((u128)v);
}
static u128 parse(const char *s) {
  u128 v = 0;
  for (const char *p = s; *p; p++) v = v * 10 + (u128)(*p - '0');
  return v;
}

// the exact result.  kind 0 = none, 1 = integer, 2 = bool,
// 3 = an integer too wide for i128 to hold
struct Want { int kind; i128 v; bool b; };

static Want wantv(const std::string &op, i128 a, i128 b) {
  Want w = {0, 0, false};
  i128 r;
  if (op == "+") {
    if (__builtin_add_overflow(a, b, &r)) { w.kind = 3; return w; }
    w.kind = 1; w.v = r; return w;
  }
  if (op == "-") {
    if (__builtin_sub_overflow(a, b, &r)) { w.kind = 3; return w; }
    w.kind = 1; w.v = r; return w;
  }
  if (op == "*") {
    if (__builtin_mul_overflow(a, b, &r)) { w.kind = 3; return w; }
    w.kind = 1; w.v = r; return w;
  }
  w.kind = 2;
  if (op == "<") { w.b = a < b; return w; }
  if (op == "<=") { w.b = a <= b; return w; }
  if (op == ">") { w.b = a > b; return w; }
  if (op == ">=") { w.b = a >= b; return w; }
  if (op == "==") { w.b = a == b; return w; }
  if (op == "!=") { w.b = a != b; return w; }
  w.kind = 0; return w;
}

template <class T>
static std::string fidv(T r, const std::string &op, i128 a, i128 b) {
  Want w = wantv(op, a, b);
  if (w.kind == 0) return "na";
  if constexpr (std::is_same_v<T, bool>) {
    if (w.kind != 2) return "na";
    return (r == w.b) ? "exact" : "inexact";
  } else if constexpr (std::is_integral_v<T> ||
                       std::is_same_v<T, __int128> ||
                       std::is_same_v<T, unsigned __int128>) {
    if (w.kind == 2) return "na";
    if (w.kind == 3) return "inexact";
    return ((i128)r == w.v) ? "exact" : "inexact";
  } else if constexpr (std::is_floating_point_v<T>) {
    if (w.kind == 2) return "na";
    double d = (double)r;
    if (std::isnan(d) || std::isinf(d)) return "na";
    if (d != std::floor(d)) return "inexact";
    if (w.kind == 3) return "inexact";
    long double L = (long double)r;
    return (L == (long double)w.v) ? "exact" : "inexact";
  } else {
    return "na";
  }
}

template <class T>
static const char *tname(T) {
  if constexpr (std::is_same_v<T, bool>) return "bool";
  else if constexpr (std::is_same_v<T, int32_t>) return "int32_t";
  else if constexpr (std::is_same_v<T, int64_t>) return "int64_t";
  else if constexpr (std::is_same_v<T, uint64_t>) return "uint64_t";
  else if constexpr (std::is_same_v<T, __int128>) return "__int128";
  else if constexpr (std::is_same_v<T, unsigned __int128>) return "u__int128";
  else if constexpr (std::is_same_v<T, int>) return "int";
  else if constexpr (std::is_same_v<T, unsigned>) return "unsigned";
  else if constexpr (std::is_same_v<T, double>) return "double";
  else if constexpr (std::is_same_v<T, float>) return "float";
  else return "other";
}

template <class T>
static std::string sigof(T r, const std::string &op, i128 a, i128 b) {
  return std::string("answer|") + tname(r) + "|" + fidv(r, op, a, b);
}

typedef std::string (*TFN)(u128, i128, i128);

static int bisect(int tid, TFN fn, const char *ops, const char *lov,
                  const char *hiv, const char *fixv, bool varyIsLhs) {
  std::string op(ops);
  u128 lo = parse(lov), hi = parse(hiv);
  i128 fx = (i128)parse(fixv);
  auto s = [&](u128 c) {
    i128 a = varyIsLhs ? (i128)c : fx;
    i128 b = varyIsLhs ? fx : (i128)c;
    return fn(c, a, b);
  };
  std::string slo = s(lo), shi = s(hi);
  int probes = 2;
  if (slo == shi) {
    printf("N|%d|%s|%s\n", tid, slo.c_str(), shi.c_str());
    return probes;
  }
  std::set<std::string> other;
  while (hi - lo > 1) {
    u128 mid = lo + (hi - lo) / 2;
    std::string sm = s(mid); probes++;
    if (sm == slo) lo = mid;
    else { if (sm != shi) other.insert(sm); hi = mid; }
  }
  std::string o;
  for (std::set<std::string>::iterator it = other.begin();
       it != other.end(); ++it) { if (!o.empty()) o += ";"; o += *it; }
  printf("B|%d|%s|%s|%s|%s|%d|%s\n", tid, dec(lo).c_str(), dec(hi).c_str(),
         slo.c_str(), shi.c_str(), probes, o.c_str());
  return probes;
}
'''

FOOT_CPP = r'''
int main() {
  signal(SIGFPE, onfpe);
  reg();
  int total = 0;
  int n = (int)TARGETS.size();
  for (int k = 0; k < n; k++) {
    total += TARGETS[k]();
    if ((k + 1) % 25 == 0 || k + 1 == n)
      fprintf(stderr, "progress %d/%d probes=%d\n", k + 1, n, total);
    fflush(stdout);
  }
  fprintf(stderr, "DONE targets=%d probes=%d\n", n, total);
  return 0;
}
'''

# ---------------------------------------------------------------- rust

HEAD["rust"] = r'''
use std::collections::BTreeSet;
use std::panic;

#[derive(Clone, Copy)]
enum Want { None, Int(i128), Wide, Bool(bool) }

fn wantv(op: &str, a: i128, b: i128) -> Want {
    match op {
        "+" => match a.checked_add(b) { Some(v) => Want::Int(v), None => Want::Wide },
        "-" => match a.checked_sub(b) { Some(v) => Want::Int(v), None => Want::Wide },
        "*" => match a.checked_mul(b) { Some(v) => Want::Int(v), None => Want::Wide },
        "<" => Want::Bool(a < b),
        "<=" => Want::Bool(a <= b),
        ">" => Want::Bool(a > b),
        ">=" => Want::Bool(a >= b),
        "==" => Want::Bool(a == b),
        "!=" => Want::Bool(a != b),
        _ => Want::None,
    }
}

pub enum Got { I(i128), B(bool), F(f64), Other }

pub trait Val { fn got(&self) -> Got; fn tn(&self) -> &'static str; }
impl Val for i32 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "i32" } }
impl Val for i64 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "i64" } }
impl Val for u64 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "u64" } }
impl Val for i128 { fn got(&self) -> Got { Got::I(*self) } fn tn(&self) -> &'static str { "i128" } }
impl Val for u128 { fn got(&self) -> Got { Got::Other } fn tn(&self) -> &'static str { "u128" } }
impl Val for bool { fn got(&self) -> Got { Got::B(*self) } fn tn(&self) -> &'static str { "bool" } }
impl Val for f64 { fn got(&self) -> Got { Got::F(*self) } fn tn(&self) -> &'static str { "f64" } }
impl Val for f32 { fn got(&self) -> Got { Got::F(*self as f64) } fn tn(&self) -> &'static str { "f32" } }
impl Val for u32 { fn got(&self) -> Got { Got::I(*self as i128) } fn tn(&self) -> &'static str { "u32" } }

pub fn fidv(g: Got, op: &str, a: i128, b: i128) -> &'static str {
    let w = wantv(op, a, b);
    match (w, g) {
        (Want::None, _) => "na",
        (Want::Bool(wb), Got::B(gb)) => if wb == gb { "exact" } else { "inexact" },
        (Want::Bool(_), _) => "na",
        (_, Got::B(_)) => "na",
        (Want::Wide, Got::I(_)) => "inexact",
        (Want::Wide, Got::F(_)) => "inexact",
        (Want::Int(wv), Got::I(gv)) => if wv == gv { "exact" } else { "inexact" },
        (Want::Int(wv), Got::F(f)) => {
            if f.is_nan() || f.is_infinite() { "na" }
            else if f != f.floor() { "inexact" }
            else if (f as i128) == wv { "exact" } else { "inexact" }
        }
        (_, Got::Other) => "na",
    }
}

pub fn sigof<T: Val>(r: T, op: &str, a: i128, b: i128) -> String {
    format!("answer|{}|{}", r.tn(), fidv(r.got(), op, a, b))
}

type TFN = fn(u128, i128, i128) -> String;

fn bisect(tid: i32, f: TFN, op: &str, lov: u128, hiv: u128, fixv: u128,
          vary_is_lhs: bool) -> i32 {
    let fx = fixv as i128;
    let s = |c: u128| -> String {
        let a = if vary_is_lhs { c as i128 } else { fx };
        let b = if vary_is_lhs { fx } else { c as i128 };
        match panic::catch_unwind(|| f(c, a, b)) {
            Ok(v) => v,
            Err(_) => "raise|panic|na".to_string(),
        }
    };
    let mut lo = lov;
    let mut hi = hiv;
    let slo = s(lo);
    let shi = s(hi);
    let mut probes = 2;
    if slo == shi {
        println!("N|{}|{}|{}", tid, slo, shi);
        return probes;
    }
    let mut other: BTreeSet<String> = BTreeSet::new();
    while hi - lo > 1 {
        let mid = lo + (hi - lo) / 2;
        let sm = s(mid);
        probes += 1;
        if sm == slo { lo = mid; }
        else {
            if sm != shi { other.insert(sm); }
            hi = mid;
        }
    }
    let o: Vec<String> = other.into_iter().collect();
    println!("B|{}|{}|{}|{}|{}|{}|{}", tid, lo, hi, slo, shi, probes,
             o.join(";"));
    probes
}
'''

FOOT_RS = r'''
fn main() {
    panic::set_hook(Box::new(|_| {}));
    let t = reg();
    let mut total = 0;
    let n = t.len();
    for k in 0..n {
        total += t[k]();
        if (k + 1) % 25 == 0 || k + 1 == n {
            eprintln!("progress {}/{} probes={}", k + 1, n, total);
        }
    }
    eprintln!("DONE targets={} probes={}", n, total);
}
'''


def big_lit(lang, n):
    s = str(n)
    return {
        "python": s,
        "ruby": s,
        "php": '"%s"' % s,
        "typescript": s + "n",
        "dart": 'BigInt.parse("%s")' % s,
        "java": 'new BigInteger("%s")' % s,
        "kotlin": 'BigInteger("%s")' % s,
        "csharp": 'BigInteger.Parse("%s")' % s,
        "go": 'mustBig("%s")' % s,
    }[lang]


def emit_target(lang, r, decls, candvar="c"):
    """Return the per-target closure text."""
    vary = r["vary_holder"]
    fixed_decl = rename(decls[(r["language"], r["fixed_holder"],
                               r["fixed_value"])], "f", lang)
    cexpr = CAND[lang][vary] % CANDVAR[lang]
    if r["varying_side"] == "lhs":
        a, b = cexpr, "f"
    else:
        a, b = "f", cexpr
    op = r["operation"]
    lov, hiv = r["low_value"], r["high_value"]
    fixnum = None
    # the fixed operand's numeric value, from the axis
    from l3_boundary_targets import WHOLE_VALUE
    fixnum = WHOLE_VALUE[r["fixed_value"]]
    vlhs = "true" if r["varying_side"] == "lhs" else "false"

    if lang == "python":
        body = ("(lambda f=None: None)")
        return ("    (%d, lambda c: (%s), %r, %s, %s, %s, %s),\n" % (
            r["tid"], "((%s) %s (%s))" % (a, op, b), op, lov, hiv,
            fixnum, "True" if r["varying_side"] == "lhs" else "False"))
    if lang == "ruby":
        return ("  lambda { bisect(%d, %s, %s, %s, %s, %s) { |c| ((%s) %s (%s)) } },\n" % (
            r["tid"], op.__repr__().replace("'", '"'), lov, hiv, fixnum,
            "true" if r["varying_side"] == "lhs" else "false", a, op, b))
    if lang == "php":
        fa = "$f" if b == "f" or a == "f" else None
        aa = a if a != "f" else "$f"
        bb = b if b != "f" else "$f"
        return ('  function () { %s return bisect(%d, function ($c) { %s return ((%s) %s (%s)); }, "%s", "%s", "%s", "%s", %s); },\n' % (
            "", r["tid"], fixed_decl, aa, op, bb, op, lov, hiv, fixnum, vlhs))
    if lang == "typescript":
        return ("  () => { %s return bisect(%d, (c: bigint) => ((%s) %s (%s)), \"%s\", %sn, %sn, %sn, %s); },\n" % (
            fixed_decl, r["tid"], a, op, b, op, lov, hiv, fixnum, vlhs))
    if lang == "dart":
        return ("  () { %s return bisect(%d, (BigInt c) => ((%s) %s (%s)), \"%s\", BigInt.parse(\"%s\"), BigInt.parse(\"%s\"), BigInt.parse(\"%s\"), %s); },\n" % (
            fixed_decl, r["tid"], a, op, b, op, lov, hiv, fixnum, vlhs))
    if lang == "java":
        return ("    TARGETS.add(() -> { %s return bisect(%d, (c) -> ((Object)((%s) %s (%s))), \"%s\", new BigInteger(\"%s\"), new BigInteger(\"%s\"), new BigInteger(\"%s\"), %s); });\n" % (
            fixed_decl, r["tid"], a, op, b, op, lov, hiv, fixnum, vlhs))
    if lang == "kotlin":
        return ("  { %s bisect(%d, { c -> ((%s) %s (%s)) as Any? }, \"%s\", BigInteger(\"%s\"), BigInteger(\"%s\"), BigInteger(\"%s\"), %s) },\n" % (
            fixed_decl, r["tid"], a, op, b, op, lov, hiv, fixnum, vlhs))
    if lang == "csharp":
        return ("    TARGETS.Add(() => { %s return bisect(%d, (c) => ((object)((%s) %s (%s))), \"%s\", BigInteger.Parse(\"%s\"), BigInteger.Parse(\"%s\"), BigInteger.Parse(\"%s\"), %s); });\n" % (
            fixed_decl, r["tid"], a, op, b, op, lov, hiv, fixnum, vlhs))
    if lang == "cpp":
        return (r'''static std::string T%d(u128 c, i128 a, i128 b) {
  if (sigsetjmp(JB, 1)) return std::string("death|SIGFPE|na");
  %s
  auto r = ((%s) %s (%s));
  return sigof(r, "%s", a, b);
}
''' % (r["tid"], fixed_decl, a, op, b, op))
    if lang == "rust":
        return ('fn t%d(c: u128, a: i128, b: i128) -> String {\n'
                '    %s\n    sigof(((%s) %s (%s)), "%s", a, b)\n}\n'
                % (r["tid"], fixed_decl, a, op, b, op))
    if lang == "go":
        return ("\tTARGETS = append(TARGETS, func() int { %s return bisect(%d, func(c *big.Int) interface{} { return ((%s) %s (%s)) }, \"%s\", mustBig(\"%s\"), mustBig(\"%s\"), mustBig(\"%s\"), %s) })\n" % (
            fixed_decl, r["tid"], a, op, b, op, lov, hiv, fixnum, vlhs))
    raise KeyError(lang)


def build(lang, rows, decls, pres):
    parts = [HEAD[lang]]
    pre = sorted(set(p.strip() for (l, h), p in pres.items()
                     if l == lang and p.strip()))
    if lang == "python":
        parts.append("\nTARGETS_RAW = [\n")
        for r in rows:
            parts.append(emit_target(lang, r, decls))
        parts.append("]\n")
        # python: the fixed operand decl is inlined per target below
        parts = [HEAD[lang]]
        parts.append("\nTARGETS = []\n")
        for r in rows:
            fixed_decl = rename(decls[(lang, r["fixed_holder"],
                                       r["fixed_value"])], "f", lang)
            vary = r["vary_holder"]
            cexpr = CAND[lang][vary] % "c"
            a, b = (cexpr, "f") if r["varying_side"] == "lhs" else ("f", cexpr)
            from l3_boundary_targets import WHOLE_VALUE
            fixnum = WHOLE_VALUE[r["fixed_value"]]
            parts.append(
                "def _t%d():\n    %s\n    return bisect(%d, lambda c: ((%s) %s (%s)), %r, %s, %s, %s, %s)\n"
                "TARGETS.append(_t%d)\n" % (
                    r["tid"], fixed_decl, r["tid"], a, r["operation"], b,
                    r["operation"], r["low_value"], r["high_value"], fixnum,
                    r["varying_side"] == "lhs", r["tid"]))
        parts.append(FOOT_PY)
        # bisect() must exist before the target bodies run; FOOT_PY defines
        # it and calls main() last, so move it before the TARGETS.
        head, body = parts[0], "".join(parts[1:-1])
        foot = FOOT_PY
        defs, run = foot.split("def main():")
        return head + defs + body + "def main():" + run
    if lang == "ruby":
        parts.append("\nTARGETS = [\n")
        for r in rows:
            fixed_decl = rename(decls[(lang, r["fixed_holder"],
                                       r["fixed_value"])], "f", lang)
            vary = r["vary_holder"]
            cexpr = CAND[lang][vary] % "c"
            a, b = (cexpr, "f") if r["varying_side"] == "lhs" else ("f", cexpr)
            from l3_boundary_targets import WHOLE_VALUE
            fixnum = WHOLE_VALUE[r["fixed_value"]]
            parts.append(
                '  lambda { %s; bisect(%d, "%s", %s, %s, %s, %s) { |c| ((%s) %s (%s)) } },\n'
                % (fixed_decl, r["tid"], r["operation"], r["low_value"],
                   r["high_value"], fixnum,
                   "true" if r["varying_side"] == "lhs" else "false",
                   a, r["operation"], b))
        parts.append("]\n")
        # bisect defined in FOOT before use -- ruby needs the def first
        defs, run = FOOT_RB.split("total = 0")
        return HEAD[lang] + defs + "".join(parts[1:]) + "total = 0" + run
    if lang == "php":
        body = ["\n$TARGETS = [\n"]
        for r in rows:
            fixed_decl = rename(decls[(lang, r["fixed_holder"],
                                       r["fixed_value"])], "f", lang)
            vary = r["vary_holder"]
            cexpr = CAND[lang][vary] % "$c"
            a, b = (cexpr, "$f") if r["varying_side"] == "lhs" else ("$f", cexpr)
            from l3_boundary_targets import WHOLE_VALUE
            fixnum = WHOLE_VALUE[r["fixed_value"]]
            body.append(
                '  function () { %s return bisect(%d, function ($c) { %s return ((%s) %s (%s)); }, "%s", "%s", "%s", "%s", %s); },\n'
                % (fixed_decl, r["tid"], fixed_decl, a, r["operation"], b,
                   r["operation"], r["low_value"], r["high_value"], fixnum,
                   "true" if r["varying_side"] == "lhs" else "false"))
        body.append("];\n")
        defs, run = FOOT_PHP.split("$total = 0;")
        return HEAD[lang] + defs + "".join(body) + "$total = 0;" + run
    if lang == "typescript":
        body = ["\nconst TARGETS: (() => number)[] = [\n"]
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("];\n")
        return HEAD[lang] + "".join(body) + FOOT_TS
    if lang == "dart":
        body = ["\nfinal TARGETS = <int Function()>[\n"]
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("];\n")
        return HEAD[lang] + "".join(body) + FOOT_DART
    if lang == "java":
        body = ["\n  static final List<java.util.function.Supplier<Integer>> TARGETS = new ArrayList<>();\n  static void reg() {\n"]
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("  }\n")
        foot = FOOT_JAVA.replace("int total = 0;", "reg();\n    int total = 0;")
        return HEAD[lang] + "".join(body) + foot
    if lang == "kotlin":
        body = ["\nval TARGETS: List<() -> Int> = listOf(\n"]
        body.append(",\n".join(emit_target(lang, r, decls).rstrip().rstrip(",")
                               for r in rows))
        body.append("\n)\n")
        return HEAD[lang] + "".join(body) + FOOT_KT
    if lang == "csharp":
        body = ["\n  static readonly List<Func<int>> TARGETS = new List<Func<int>>();\n  static void Reg() {\n"]
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("  }\n")
        foot = FOOT_CS.replace("int total = 0;", "Reg();\n    int total = 0;")
        return HEAD[lang] + "".join(body) + foot
    if lang == "go":
        body = ["\nvar TARGETS []func() int\n\nfunc mustBig(s string) *big.Int {\n\tv, _ := new(big.Int).SetString(s, 10)\n\treturn v\n}\n\nfunc reg() {\n"]
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("}\n")
        foot = FOOT_GO.replace("total := 0", "reg()\n\ttotal := 0")
        return HEAD[lang] + "".join(body) + foot
    if lang == "cpp":
        inc = []
        for (l, h), p in sorted(pres.items()):
            if l != "cpp":
                continue
            for line in p.splitlines():
                if line.strip().startswith("#include") and line not in inc:
                    inc.append(line)
        body = []
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("\nstatic std::vector<int (*)()> TARGETS;\n\n"
                    "static void reg() {\n")
        for r in rows:
            body.append(
                '  TARGETS.push_back([]() { return bisect(%d, T%d, "%s", "%s", "%s", "%s", %s); });\n'
                % (r["tid"], r["tid"], r["operation"], r["low_value"],
                   r["high_value"],
                   __import__("l3_boundary_targets").WHOLE_VALUE[
                       r["fixed_value"]],
                   "true" if r["varying_side"] == "lhs" else "false"))
        body.append("}\n")
        return ("\n".join(inc) + "\n" + HEAD[lang] + "".join(body) +
                FOOT_CPP)
    if lang == "rust":
        body = []
        for r in rows:
            body.append(emit_target(lang, r, decls))
        body.append("\nfn reg() -> Vec<Box<dyn Fn() -> i32>> {\n"
                    "    let mut v: Vec<Box<dyn Fn() -> i32>> = Vec::new();\n")
        for r in rows:
            body.append(
                '    v.push(Box::new(|| bisect(%d, t%d, "%s", %su128, %su128, %su128, %s)));\n'
                % (r["tid"], r["tid"], r["operation"], r["low_value"],
                   r["high_value"],
                   __import__("l3_boundary_targets").WHOLE_VALUE[
                       r["fixed_value"]],
                   "true" if r["varying_side"] == "lhs" else "false"))
        body.append("    v\n}\n")
        return HEAD[lang] + "".join(body) + FOOT_RS
    raise KeyError(lang)


def main():
    limit = None
    langs = WAVE
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--limit":
            limit = int(args[i + 1])
        if a == "--langs":
            langs = args[i + 1].split(",")
    d, forms, decls, pres = load()
    keep, defer = phase_a(d, forms)
    progress("phase A targets: %d   deferred: %d" % (len(keep), len(defer)))
    os.makedirs(os.path.join(HERE, "bnd"), exist_ok=True)
    index = {}
    for lang in langs:
        rows = [r for r in keep if r["language"] == lang]
        if limit:
            rows = rows[:limit]
        if not rows:
            continue
        src = build(lang, rows, decls, pres)
        ext = {"python": "py", "ruby": "rb", "php": "php",
               "typescript": "ts", "dart": "dart", "java": "java",
               "kotlin": "kt", "csharp": "cs", "go": "go",
               "cpp": "cpp", "rust": "rs"}[lang]
        name = {"java": "BND.java", "csharp": "BND.cs"}.get(
            lang, "bnd_%s.%s" % (lang, ext))
        p = os.path.join(HERE, "bnd", name)
        open(p, "w").write(src)
        index[lang] = {"targets": len(rows), "source": name,
                       "bytes": len(src)}
        progress("  %-11s %5d targets  %7d bytes  %s" %
                 (lang, len(rows), len(src), name))
    json.dump({"phase_a": len(keep), "deferred": len(defer),
               "per_language": index},
              open(os.path.join(HERE, "bnd", "index.json"), "w"), indent=1)
    progress("wrote bnd/")


if __name__ == "__main__":
    main()
