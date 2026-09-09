<?php

function m($x, $w) {
    if ($w >= 64) { return $x; }
    return $x & ((1 << $w) - 1);
}

function s($x, $w) {
    if ($w >= 64) { return $x; }
    $x = $x & ((1 << $w) - 1);
    if (($x >> ($w - 1)) != 0) { return $x - (1 << $w); }
    return $x;
}

function add($a, $b, $w) {
    if ($w < 64) { return m($a + $b, $w); }
    $lo = ($a & 0xFFFFFFFF) + ($b & 0xFFFFFFFF);
    $hi = (($a >> 32) & 0xFFFFFFFF) + (($b >> 32) & 0xFFFFFFFF)
          + (($lo >> 32) & 1);
    return (($hi & 0xFFFFFFFF) << 32) | ($lo & 0xFFFFFFFF);
}

function bneg($a, $w) {
    return add(bnot($a, $w), 1, $w);
}

function sub($a, $b, $w) {
    return add($a, bneg($b, $w), $w);
}

function mul($a, $b, $w) {
    if ($w < 32) { return m($a * $b, $w); }
    $al = $a & 0xFFFFFFFF;
    $ah = ($a >> 32) & 0xFFFFFFFF;
    $bl = $b & 0xFFFFFFFF;
    $bh = ($b >> 32) & 0xFFFFFFFF;
    $ll = $al * $bl;
    $lo = $ll & 0xFFFFFFFF;
    $carry = ($ll >> 32) & 0xFFFFFFFF;
    $hi = ($al * $bh + $ah * $bl + $carry) & 0xFFFFFFFF;
    $whole = (($hi & 0xFFFFFFFF) << 32) | $lo;
    return m($whole, $w);
}

function band($a, $b, $w) { return m($a & $b, $w); }
function bor($a, $b, $w) { return m($a | $b, $w); }
function bxor($a, $b, $w) { return m($a ^ $b, $w); }
function bnot($a, $w) { return m(~$a, $w); }

function shl($a, $n, $w) {
    if ($n >= $w) { return 0; }
    if ($w >= 64) { return ($a << $n); }
    return m($a << $n, $w);
}

function lshr($a, $n, $w) {
    if ($n >= $w) { return 0; }
    if ($w >= 64) {
        if ($n == 0) { return $a; }
        return ($a >> $n) & ((1 << (64 - $n)) - 1);
    }
    return m($a, $w) >> $n;
}

function ashr($a, $n, $w) {
    $v = s($a, $w);
    $k = $n;
    if ($k >= $w) { $k = $w - 1; }
    return m($v >> $k, $w);
}

function udiv($a, $b, $w) {
    if ($w < 64) { return m(intdiv(m($a, $w), m($b, $w)), $w); }
    $x = $a; $y = $b;
    if ($y < 0) { if (uge_raw($x, $y)) { return 1; } return 0; }
    if ($x >= 0) { return intdiv($x, $y); }
    $q = (intdiv($x >> 1, $y) << 1);
    $r = $x - $q * $y;
    if (uge_raw($r, $y)) { $q = $q + 1; }
    return $q;
}

function uge_raw($x, $y) {
    if (($x < 0) == ($y < 0)) { return $x >= $y; }
    return $x < 0;
}

function urem($a, $b, $w) {
    if ($w < 64) { return m(m($a, $w) % m($b, $w), $w); }
    $q = udiv($a, $b, 64);
    return sub($a, mul($q, $b, 64), 64);
}

function sdiv($a, $b, $w) {
    $x = s($a, $w);
    $y = s($b, $w);
    $q = intdiv(abs($x), abs($y));
    if (($x < 0) != ($y < 0)) { $q = -$q; }
    return m($q, $w);
}

function srem($a, $b, $w) {
    $x = s($a, $w);
    $y = s($b, $w);
    $r = abs($x) % abs($y);
    if ($x < 0) { $r = -$r; }
    return m($r, $w);
}

function ult($a, $b, $w) {
    if ($w < 64) { return m($a, $w) < m($b, $w); }
    return !uge_raw($a, $b);
}
function ule($a, $b, $w) {
    if ($w < 64) { return m($a, $w) <= m($b, $w); }
    return !uge_raw($a, $b) || $a == $b;
}
function ugt($a, $b, $w) { return !ule($a, $b, $w); }
function uge($a, $b, $w) { return !ult($a, $b, $w); }
function slt($a, $b, $w) { return s($a, $w) < s($b, $w); }
function sle($a, $b, $w) { return s($a, $w) <= s($b, $w); }
function sgt($a, $b, $w) { return s($a, $w) > s($b, $w); }
function sge($a, $b, $w) { return s($a, $w) >= s($b, $w); }
function eq($a, $b, $w) { return m($a, $w) == m($b, $w); }
function ne($a, $b, $w) { return m($a, $w) != m($b, $w); }

function cat($hi, $lo, $lw) {
    return shl($hi, $lw, 64) | m($lo, $lw);
}

function ext($x, $hi, $lo) {
    return m(lshr($x, $lo, 64), $hi - $lo + 1);
}

function sext($x, $fromw, $tow) {
    return m(s($x, $fromw), $tow);
}

function b2f($x, $w) {
    if ($w == 32) { return unpack("g", pack("V", m($x, 32)))[1]; }
    return unpack("e", pack("P", $x))[1];
}

function f2b($f, $w) {
    if ($w == 32) { return unpack("V", pack("g", $f))[1]; }
    return unpack("P", pack("e", $f))[1];
}

function fadd($a, $b, $w) { return f2b(b2f($a, $w) + b2f($b, $w), $w); }
function fsub($a, $b, $w) { return f2b(b2f($a, $w) - b2f($b, $w), $w); }
function fmul($a, $b, $w) { return f2b(b2f($a, $w) * b2f($b, $w), $w); }
function fdiv($a, $b, $w) { return f2b(b2f($a, $w) / b2f($b, $w), $w); }
function i2f($x, $fromw, $w) { return f2b((float)s($x, $fromw), $w); }
function u2f($x, $fromw, $w) { return f2b((float)m($x, $fromw), $w); }
function fwiden($x, $fromw, $w) { return f2b(b2f($x, $fromw), $w); }

// task ex1 emulation -- rendered by interp_render.py
// InterpRenderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
function emu_add_gpr_gpr_32__reg_rdi__php($a, $b) {
    return m(cat(0, add($a, $b, 32), 32), 64);
}


$handle = fopen("php://stdin", "r");
while (($line = fgets($handle)) !== false) {
    $text = trim($line);
    if ($text === "") { continue; }
    $values = preg_split("/\\s+/", $text);
    $ints = array();
    foreach ($values as $one) { $ints[] = intval($one); }
    try {
        $answer = emu_add_gpr_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
