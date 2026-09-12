<?php

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

// task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
// one named local per gate, over the term of cmovbe_gpr_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Or(Extract(31, 0, v1)*4294967295 == Extract(31, 0, v0), Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1), Extract(31, 0, v2), Extract(31, 0, v3)))
function emu_cmovbe_gpr_gpr_32__reg_rdi__php($a, $b, $c, $d) {
    $x3_0 = ex_ext($d, 0, 0);
    $x1_0 = ex_ext($a, 0, 0);
    $x0_0 = ex_ext($b, 0, 0);
    $x1_1 = ex_ext($a, 1, 1);
    $x0_1 = ex_ext($b, 1, 1);
    $x1_2 = ex_ext($a, 2, 2);
    $x0_2 = ex_ext($b, 2, 2);
    $x1_3 = ex_ext($a, 3, 3);
    $x0_3 = ex_ext($b, 3, 3);
    $x1_4 = ex_ext($a, 4, 4);
    $x0_4 = ex_ext($b, 4, 4);
    $x1_5 = ex_ext($a, 5, 5);
    $x0_5 = ex_ext($b, 5, 5);
    $x1_6 = ex_ext($a, 6, 6);
    $x0_6 = ex_ext($b, 6, 6);
    $x1_7 = ex_ext($a, 7, 7);
    $x0_7 = ex_ext($b, 7, 7);
    $x1_8 = ex_ext($a, 8, 8);
    $x0_8 = ex_ext($b, 8, 8);
    $x1_9 = ex_ext($a, 9, 9);
    $x0_9 = ex_ext($b, 9, 9);
    $x1_10 = ex_ext($a, 10, 10);
    $x0_10 = ex_ext($b, 10, 10);
    $x1_11 = ex_ext($a, 11, 11);
    $x0_11 = ex_ext($b, 11, 11);
    $x1_12 = ex_ext($a, 12, 12);
    $x0_12 = ex_ext($b, 12, 12);
    $x1_13 = ex_ext($a, 13, 13);
    $x0_13 = ex_ext($b, 13, 13);
    $x1_14 = ex_ext($a, 14, 14);
    $x0_14 = ex_ext($b, 14, 14);
    $x1_15 = ex_ext($a, 15, 15);
    $x0_15 = ex_ext($b, 15, 15);
    $x1_16 = ex_ext($a, 16, 16);
    $x0_16 = ex_ext($b, 16, 16);
    $x1_17 = ex_ext($a, 17, 17);
    $x0_17 = ex_ext($b, 17, 17);
    $x1_18 = ex_ext($a, 18, 18);
    $x0_18 = ex_ext($b, 18, 18);
    $x1_19 = ex_ext($a, 19, 19);
    $x0_19 = ex_ext($b, 19, 19);
    $x1_20 = ex_ext($a, 20, 20);
    $x0_20 = ex_ext($b, 20, 20);
    $x1_21 = ex_ext($a, 21, 21);
    $x0_21 = ex_ext($b, 21, 21);
    $x1_22 = ex_ext($a, 22, 22);
    $x0_22 = ex_ext($b, 22, 22);
    $x1_23 = ex_ext($a, 23, 23);
    $x0_23 = ex_ext($b, 23, 23);
    $x1_24 = ex_ext($a, 24, 24);
    $x0_24 = ex_ext($b, 24, 24);
    $x1_25 = ex_ext($a, 25, 25);
    $x0_25 = ex_ext($b, 25, 25);
    $x1_26 = ex_ext($a, 26, 26);
    $x0_26 = ex_ext($b, 26, 26);
    $x1_27 = ex_ext($a, 27, 27);
    $x0_27 = ex_ext($b, 27, 27);
    $x1_28 = ex_ext($a, 28, 28);
    $x0_28 = ex_ext($b, 28, 28);
    $x1_29 = ex_ext($a, 29, 29);
    $x0_29 = ex_ext($b, 29, 29);
    $x1_30 = ex_ext($a, 30, 30);
    $x0_30 = ex_ext($b, 30, 30);
    $x1_31 = ex_ext($a, 31, 31);
    $x0_31 = ex_ext($b, 31, 31);
    $x2_0 = ex_ext($c, 0, 0);
    $x3_1 = ex_ext($d, 1, 1);
    $x2_1 = ex_ext($c, 1, 1);
    $x3_2 = ex_ext($d, 2, 2);
    $x2_2 = ex_ext($c, 2, 2);
    $x3_3 = ex_ext($d, 3, 3);
    $x2_3 = ex_ext($c, 3, 3);
    $x3_4 = ex_ext($d, 4, 4);
    $x2_4 = ex_ext($c, 4, 4);
    $x3_5 = ex_ext($d, 5, 5);
    $x2_5 = ex_ext($c, 5, 5);
    $x3_6 = ex_ext($d, 6, 6);
    $x2_6 = ex_ext($c, 6, 6);
    $x3_7 = ex_ext($d, 7, 7);
    $x2_7 = ex_ext($c, 7, 7);
    $x3_8 = ex_ext($d, 8, 8);
    $x2_8 = ex_ext($c, 8, 8);
    $x3_9 = ex_ext($d, 9, 9);
    $x2_9 = ex_ext($c, 9, 9);
    $x3_10 = ex_ext($d, 10, 10);
    $x2_10 = ex_ext($c, 10, 10);
    $x3_11 = ex_ext($d, 11, 11);
    $x2_11 = ex_ext($c, 11, 11);
    $x3_12 = ex_ext($d, 12, 12);
    $x2_12 = ex_ext($c, 12, 12);
    $x3_13 = ex_ext($d, 13, 13);
    $x2_13 = ex_ext($c, 13, 13);
    $x3_14 = ex_ext($d, 14, 14);
    $x2_14 = ex_ext($c, 14, 14);
    $x3_15 = ex_ext($d, 15, 15);
    $x2_15 = ex_ext($c, 15, 15);
    $x3_16 = ex_ext($d, 16, 16);
    $x2_16 = ex_ext($c, 16, 16);
    $x3_17 = ex_ext($d, 17, 17);
    $x2_17 = ex_ext($c, 17, 17);
    $x3_18 = ex_ext($d, 18, 18);
    $x2_18 = ex_ext($c, 18, 18);
    $x3_19 = ex_ext($d, 19, 19);
    $x2_19 = ex_ext($c, 19, 19);
    $x3_20 = ex_ext($d, 20, 20);
    $x2_20 = ex_ext($c, 20, 20);
    $x3_21 = ex_ext($d, 21, 21);
    $x2_21 = ex_ext($c, 21, 21);
    $x3_22 = ex_ext($d, 22, 22);
    $x2_22 = ex_ext($c, 22, 22);
    $x3_23 = ex_ext($d, 23, 23);
    $x2_23 = ex_ext($c, 23, 23);
    $x3_24 = ex_ext($d, 24, 24);
    $x2_24 = ex_ext($c, 24, 24);
    $x3_25 = ex_ext($d, 25, 25);
    $x2_25 = ex_ext($c, 25, 25);
    $x3_26 = ex_ext($d, 26, 26);
    $x2_26 = ex_ext($c, 26, 26);
    $x3_27 = ex_ext($d, 27, 27);
    $x2_27 = ex_ext($c, 27, 27);
    $x3_28 = ex_ext($d, 28, 28);
    $x2_28 = ex_ext($c, 28, 28);
    $x3_29 = ex_ext($d, 29, 29);
    $x2_29 = ex_ext($c, 29, 29);
    $x3_30 = ex_ext($d, 30, 30);
    $x2_30 = ex_ext($c, 30, 30);
    $x3_31 = ex_ext($d, 31, 31);
    $x2_31 = ex_ext($c, 31, 31);
    $g0 = ($x1_0 ^ 1);
    $g1 = ($x0_0 ^ 1);
    $g2 = ($g1 | $g0);
    $g3 = ($x1_1 ^ 1);
    $g4 = ($g3 | $g2);
    $g5 = ($g4 ^ 1);
    $g6 = ($x0_1 ^ 1);
    $g7 = ($g6 | $g2);
    $g8 = ($g7 ^ 1);
    $g9 = ($g6 | $g3);
    $g10 = ($g9 ^ 1);
    $g11 = ($g10 | $g8);
    $g12 = ($g11 | $g5);
    $g13 = ($g12 ^ 1);
    $g14 = ($x1_2 ^ 1);
    $g15 = ($g14 | $g13);
    $g16 = ($g15 ^ 1);
    $g17 = ($x0_2 ^ 1);
    $g18 = ($g17 | $g13);
    $g19 = ($g18 ^ 1);
    $g20 = ($g17 | $g14);
    $g21 = ($g20 ^ 1);
    $g22 = ($g21 | $g19);
    $g23 = ($g22 | $g16);
    $g24 = ($g23 ^ 1);
    $g25 = ($x1_3 ^ 1);
    $g26 = ($g25 | $g24);
    $g27 = ($g26 ^ 1);
    $g28 = ($x0_3 ^ 1);
    $g29 = ($g28 | $g24);
    $g30 = ($g29 ^ 1);
    $g31 = ($g28 | $g25);
    $g32 = ($g31 ^ 1);
    $g33 = ($g32 | $g30);
    $g34 = ($g33 | $g27);
    $g35 = ($g34 ^ 1);
    $g36 = ($x1_4 ^ 1);
    $g37 = ($g36 | $g35);
    $g38 = ($g37 ^ 1);
    $g39 = ($x0_4 ^ 1);
    $g40 = ($g39 | $g35);
    $g41 = ($g40 ^ 1);
    $g42 = ($g39 | $g36);
    $g43 = ($g42 ^ 1);
    $g44 = ($g43 | $g41);
    $g45 = ($g44 | $g38);
    $g46 = ($g45 ^ 1);
    $g47 = ($x1_5 ^ 1);
    $g48 = ($g47 | $g46);
    $g49 = ($g48 ^ 1);
    $g50 = ($x0_5 ^ 1);
    $g51 = ($g50 | $g46);
    $g52 = ($g51 ^ 1);
    $g53 = ($g50 | $g47);
    $g54 = ($g53 ^ 1);
    $g55 = ($g54 | $g52);
    $g56 = ($g55 | $g49);
    $g57 = ($g56 ^ 1);
    $g58 = ($x1_6 ^ 1);
    $g59 = ($g58 | $g57);
    $g60 = ($g59 ^ 1);
    $g61 = ($x0_6 ^ 1);
    $g62 = ($g61 | $g57);
    $g63 = ($g62 ^ 1);
    $g64 = ($g61 | $g58);
    $g65 = ($g64 ^ 1);
    $g66 = ($g65 | $g63);
    $g67 = ($g66 | $g60);
    $g68 = ($g67 ^ 1);
    $g69 = ($x1_7 ^ 1);
    $g70 = ($g69 | $g68);
    $g71 = ($g70 ^ 1);
    $g72 = ($x0_7 ^ 1);
    $g73 = ($g72 | $g68);
    $g74 = ($g73 ^ 1);
    $g75 = ($g72 | $g69);
    $g76 = ($g75 ^ 1);
    $g77 = ($g76 | $g74);
    $g78 = ($g77 | $g71);
    $g79 = ($g78 ^ 1);
    $g80 = ($x1_8 ^ 1);
    $g81 = ($g80 | $g79);
    $g82 = ($g81 ^ 1);
    $g83 = ($x0_8 ^ 1);
    $g84 = ($g83 | $g79);
    $g85 = ($g84 ^ 1);
    $g86 = ($g83 | $g80);
    $g87 = ($g86 ^ 1);
    $g88 = ($g87 | $g85);
    $g89 = ($g88 | $g82);
    $g90 = ($g89 ^ 1);
    $g91 = ($x1_9 ^ 1);
    $g92 = ($g91 | $g90);
    $g93 = ($g92 ^ 1);
    $g94 = ($x0_9 ^ 1);
    $g95 = ($g94 | $g90);
    $g96 = ($g95 ^ 1);
    $g97 = ($g94 | $g91);
    $g98 = ($g97 ^ 1);
    $g99 = ($g98 | $g96);
    $g100 = ($g99 | $g93);
    $g101 = ($g100 ^ 1);
    $g102 = ($x1_10 ^ 1);
    $g103 = ($g102 | $g101);
    $g104 = ($g103 ^ 1);
    $g105 = ($x0_10 ^ 1);
    $g106 = ($g105 | $g101);
    $g107 = ($g106 ^ 1);
    $g108 = ($g105 | $g102);
    $g109 = ($g108 ^ 1);
    $g110 = ($g109 | $g107);
    $g111 = ($g110 | $g104);
    $g112 = ($g111 ^ 1);
    $g113 = ($x1_11 ^ 1);
    $g114 = ($g113 | $g112);
    $g115 = ($g114 ^ 1);
    $g116 = ($x0_11 ^ 1);
    $g117 = ($g116 | $g112);
    $g118 = ($g117 ^ 1);
    $g119 = ($g116 | $g113);
    $g120 = ($g119 ^ 1);
    $g121 = ($g120 | $g118);
    $g122 = ($g121 | $g115);
    $g123 = ($g122 ^ 1);
    $g124 = ($x1_12 ^ 1);
    $g125 = ($g124 | $g123);
    $g126 = ($g125 ^ 1);
    $g127 = ($x0_12 ^ 1);
    $g128 = ($g127 | $g123);
    $g129 = ($g128 ^ 1);
    $g130 = ($g127 | $g124);
    $g131 = ($g130 ^ 1);
    $g132 = ($g131 | $g129);
    $g133 = ($g132 | $g126);
    $g134 = ($g133 ^ 1);
    $g135 = ($x1_13 ^ 1);
    $g136 = ($g135 | $g134);
    $g137 = ($g136 ^ 1);
    $g138 = ($x0_13 ^ 1);
    $g139 = ($g138 | $g134);
    $g140 = ($g139 ^ 1);
    $g141 = ($g138 | $g135);
    $g142 = ($g141 ^ 1);
    $g143 = ($g142 | $g140);
    $g144 = ($g143 | $g137);
    $g145 = ($g144 ^ 1);
    $g146 = ($x1_14 ^ 1);
    $g147 = ($g146 | $g145);
    $g148 = ($g147 ^ 1);
    $g149 = ($x0_14 ^ 1);
    $g150 = ($g149 | $g145);
    $g151 = ($g150 ^ 1);
    $g152 = ($g149 | $g146);
    $g153 = ($g152 ^ 1);
    $g154 = ($g153 | $g151);
    $g155 = ($g154 | $g148);
    $g156 = ($g155 ^ 1);
    $g157 = ($x1_15 ^ 1);
    $g158 = ($g157 | $g156);
    $g159 = ($g158 ^ 1);
    $g160 = ($x0_15 ^ 1);
    $g161 = ($g160 | $g156);
    $g162 = ($g161 ^ 1);
    $g163 = ($g160 | $g157);
    $g164 = ($g163 ^ 1);
    $g165 = ($g164 | $g162);
    $g166 = ($g165 | $g159);
    $g167 = ($g166 ^ 1);
    $g168 = ($x1_16 ^ 1);
    $g169 = ($g168 | $g167);
    $g170 = ($g169 ^ 1);
    $g171 = ($x0_16 ^ 1);
    $g172 = ($g171 | $g167);
    $g173 = ($g172 ^ 1);
    $g174 = ($g171 | $g168);
    $g175 = ($g174 ^ 1);
    $g176 = ($g175 | $g173);
    $g177 = ($g176 | $g170);
    $g178 = ($g177 ^ 1);
    $g179 = ($x1_17 ^ 1);
    $g180 = ($g179 | $g178);
    $g181 = ($g180 ^ 1);
    $g182 = ($x0_17 ^ 1);
    $g183 = ($g182 | $g178);
    $g184 = ($g183 ^ 1);
    $g185 = ($g182 | $g179);
    $g186 = ($g185 ^ 1);
    $g187 = ($g186 | $g184);
    $g188 = ($g187 | $g181);
    $g189 = ($g188 ^ 1);
    $g190 = ($x1_18 ^ 1);
    $g191 = ($g190 | $g189);
    $g192 = ($g191 ^ 1);
    $g193 = ($x0_18 ^ 1);
    $g194 = ($g193 | $g189);
    $g195 = ($g194 ^ 1);
    $g196 = ($g193 | $g190);
    $g197 = ($g196 ^ 1);
    $g198 = ($g197 | $g195);
    $g199 = ($g198 | $g192);
    $g200 = ($g199 ^ 1);
    $g201 = ($x1_19 ^ 1);
    $g202 = ($g201 | $g200);
    $g203 = ($g202 ^ 1);
    $g204 = ($x0_19 ^ 1);
    $g205 = ($g204 | $g200);
    $g206 = ($g205 ^ 1);
    $g207 = ($g204 | $g201);
    $g208 = ($g207 ^ 1);
    $g209 = ($g208 | $g206);
    $g210 = ($g209 | $g203);
    $g211 = ($g210 ^ 1);
    $g212 = ($x1_20 ^ 1);
    $g213 = ($g212 | $g211);
    $g214 = ($g213 ^ 1);
    $g215 = ($x0_20 ^ 1);
    $g216 = ($g215 | $g211);
    $g217 = ($g216 ^ 1);
    $g218 = ($g215 | $g212);
    $g219 = ($g218 ^ 1);
    $g220 = ($g219 | $g217);
    $g221 = ($g220 | $g214);
    $g222 = ($g221 ^ 1);
    $g223 = ($x1_21 ^ 1);
    $g224 = ($g223 | $g222);
    $g225 = ($g224 ^ 1);
    $g226 = ($x0_21 ^ 1);
    $g227 = ($g226 | $g222);
    $g228 = ($g227 ^ 1);
    $g229 = ($g226 | $g223);
    $g230 = ($g229 ^ 1);
    $g231 = ($g230 | $g228);
    $g232 = ($g231 | $g225);
    $g233 = ($g232 ^ 1);
    $g234 = ($x1_22 ^ 1);
    $g235 = ($g234 | $g233);
    $g236 = ($g235 ^ 1);
    $g237 = ($x0_22 ^ 1);
    $g238 = ($g237 | $g233);
    $g239 = ($g238 ^ 1);
    $g240 = ($g237 | $g234);
    $g241 = ($g240 ^ 1);
    $g242 = ($g241 | $g239);
    $g243 = ($g242 | $g236);
    $g244 = ($g243 ^ 1);
    $g245 = ($x1_23 ^ 1);
    $g246 = ($g245 | $g244);
    $g247 = ($g246 ^ 1);
    $g248 = ($x0_23 ^ 1);
    $g249 = ($g248 | $g244);
    $g250 = ($g249 ^ 1);
    $g251 = ($g248 | $g245);
    $g252 = ($g251 ^ 1);
    $g253 = ($g252 | $g250);
    $g254 = ($g253 | $g247);
    $g255 = ($g254 ^ 1);
    $g256 = ($x1_24 ^ 1);
    $g257 = ($g256 | $g255);
    $g258 = ($g257 ^ 1);
    $g259 = ($x0_24 ^ 1);
    $g260 = ($g259 | $g255);
    $g261 = ($g260 ^ 1);
    $g262 = ($g259 | $g256);
    $g263 = ($g262 ^ 1);
    $g264 = ($g263 | $g261);
    $g265 = ($g264 | $g258);
    $g266 = ($g265 ^ 1);
    $g267 = ($x1_25 ^ 1);
    $g268 = ($g267 | $g266);
    $g269 = ($g268 ^ 1);
    $g270 = ($x0_25 ^ 1);
    $g271 = ($g270 | $g266);
    $g272 = ($g271 ^ 1);
    $g273 = ($g270 | $g267);
    $g274 = ($g273 ^ 1);
    $g275 = ($g274 | $g272);
    $g276 = ($g275 | $g269);
    $g277 = ($g276 ^ 1);
    $g278 = ($x1_26 ^ 1);
    $g279 = ($g278 | $g277);
    $g280 = ($g279 ^ 1);
    $g281 = ($x0_26 ^ 1);
    $g282 = ($g281 | $g277);
    $g283 = ($g282 ^ 1);
    $g284 = ($g281 | $g278);
    $g285 = ($g284 ^ 1);
    $g286 = ($g285 | $g283);
    $g287 = ($g286 | $g280);
    $g288 = ($g287 ^ 1);
    $g289 = ($x1_27 ^ 1);
    $g290 = ($g289 | $g288);
    $g291 = ($g290 ^ 1);
    $g292 = ($x0_27 ^ 1);
    $g293 = ($g292 | $g288);
    $g294 = ($g293 ^ 1);
    $g295 = ($g292 | $g289);
    $g296 = ($g295 ^ 1);
    $g297 = ($g296 | $g294);
    $g298 = ($g297 | $g291);
    $g299 = ($g298 ^ 1);
    $g300 = ($x1_28 ^ 1);
    $g301 = ($g300 | $g299);
    $g302 = ($g301 ^ 1);
    $g303 = ($x0_28 ^ 1);
    $g304 = ($g303 | $g299);
    $g305 = ($g304 ^ 1);
    $g306 = ($g303 | $g300);
    $g307 = ($g306 ^ 1);
    $g308 = ($g307 | $g305);
    $g309 = ($g308 | $g302);
    $g310 = ($g309 ^ 1);
    $g311 = ($x1_29 ^ 1);
    $g312 = ($g311 | $g310);
    $g313 = ($g312 ^ 1);
    $g314 = ($x0_29 ^ 1);
    $g315 = ($g314 | $g310);
    $g316 = ($g315 ^ 1);
    $g317 = ($g314 | $g311);
    $g318 = ($g317 ^ 1);
    $g319 = ($g318 | $g316);
    $g320 = ($g319 | $g313);
    $g321 = ($g320 ^ 1);
    $g322 = ($x1_30 ^ 1);
    $g323 = ($g322 | $g321);
    $g324 = ($g323 ^ 1);
    $g325 = ($x0_30 ^ 1);
    $g326 = ($g325 | $g321);
    $g327 = ($g326 ^ 1);
    $g328 = ($g325 | $g322);
    $g329 = ($g328 ^ 1);
    $g330 = ($g329 | $g327);
    $g331 = ($g330 | $g324);
    $g332 = ($g331 ^ 1);
    $g333 = ($x1_31 ^ 1);
    $g334 = ($g333 | $g332);
    $g335 = ($g334 ^ 1);
    $g336 = ($x0_31 ^ 1);
    $g337 = ($g336 | $g332);
    $g338 = ($g337 ^ 1);
    $g339 = ($g336 | $g333);
    $g340 = ($g339 ^ 1);
    $g341 = ($g340 | $g338);
    $g342 = ($g341 | $g335);
    $g343 = ($x1_1 | $x1_0);
    $g344 = ($x1_2 | $g343);
    $g345 = ($x1_3 | $g344);
    $g346 = ($x1_4 | $g345);
    $g347 = ($x1_5 | $g346);
    $g348 = ($x1_6 | $g347);
    $g349 = ($x1_7 | $g348);
    $g350 = ($x1_8 | $g349);
    $g351 = ($x1_9 | $g350);
    $g352 = ($x1_10 | $g351);
    $g353 = ($x1_11 | $g352);
    $g354 = ($x1_12 | $g353);
    $g355 = ($x1_13 | $g354);
    $g356 = ($x1_14 | $g355);
    $g357 = ($x1_15 | $g356);
    $g358 = ($x1_16 | $g357);
    $g359 = ($x1_17 | $g358);
    $g360 = ($x1_18 | $g359);
    $g361 = ($x1_19 | $g360);
    $g362 = ($x1_20 | $g361);
    $g363 = ($x1_21 | $g362);
    $g364 = ($x1_22 | $g363);
    $g365 = ($x1_23 | $g364);
    $g366 = ($x1_24 | $g365);
    $g367 = ($x1_25 | $g366);
    $g368 = ($x1_26 | $g367);
    $g369 = ($x1_27 | $g368);
    $g370 = ($x1_28 | $g369);
    $g371 = ($x1_29 | $g370);
    $g372 = ($x1_30 | $g371);
    $g373 = ($g372 ^ $x1_31);
    $g374 = ($g373 ^ 1);
    $g375 = ($g374 ^ $x0_31);
    $g376 = ($g375 ^ 1);
    $g377 = ($g371 ^ $x1_30);
    $g378 = ($g377 ^ 1);
    $g379 = ($g378 ^ $x0_30);
    $g380 = ($g379 ^ 1);
    $g381 = ($g370 ^ $x1_29);
    $g382 = ($g381 ^ 1);
    $g383 = ($g382 ^ $x0_29);
    $g384 = ($g383 ^ 1);
    $g385 = ($g369 ^ $x1_28);
    $g386 = ($g385 ^ 1);
    $g387 = ($g386 ^ $x0_28);
    $g388 = ($g387 ^ 1);
    $g389 = ($g368 ^ $x1_27);
    $g390 = ($g389 ^ 1);
    $g391 = ($g390 ^ $x0_27);
    $g392 = ($g391 ^ 1);
    $g393 = ($g367 ^ $x1_26);
    $g394 = ($g393 ^ 1);
    $g395 = ($g394 ^ $x0_26);
    $g396 = ($g395 ^ 1);
    $g397 = ($g366 ^ $x1_25);
    $g398 = ($g397 ^ 1);
    $g399 = ($g398 ^ $x0_25);
    $g400 = ($g399 ^ 1);
    $g401 = ($g365 ^ $x1_24);
    $g402 = ($g401 ^ 1);
    $g403 = ($g402 ^ $x0_24);
    $g404 = ($g403 ^ 1);
    $g405 = ($g364 ^ $x1_23);
    $g406 = ($g405 ^ 1);
    $g407 = ($g406 ^ $x0_23);
    $g408 = ($g407 ^ 1);
    $g409 = ($g363 ^ $x1_22);
    $g410 = ($g409 ^ 1);
    $g411 = ($g410 ^ $x0_22);
    $g412 = ($g411 ^ 1);
    $g413 = ($g362 ^ $x1_21);
    $g414 = ($g413 ^ 1);
    $g415 = ($g414 ^ $x0_21);
    $g416 = ($g415 ^ 1);
    $g417 = ($g361 ^ $x1_20);
    $g418 = ($g417 ^ 1);
    $g419 = ($g418 ^ $x0_20);
    $g420 = ($g419 ^ 1);
    $g421 = ($g360 ^ $x1_19);
    $g422 = ($g421 ^ 1);
    $g423 = ($g422 ^ $x0_19);
    $g424 = ($g423 ^ 1);
    $g425 = ($g359 ^ $x1_18);
    $g426 = ($g425 ^ 1);
    $g427 = ($g426 ^ $x0_18);
    $g428 = ($g427 ^ 1);
    $g429 = ($g358 ^ $x1_17);
    $g430 = ($g429 ^ 1);
    $g431 = ($g430 ^ $x0_17);
    $g432 = ($g431 ^ 1);
    $g433 = ($g357 ^ $x1_16);
    $g434 = ($g433 ^ 1);
    $g435 = ($g434 ^ $x0_16);
    $g436 = ($g435 ^ 1);
    $g437 = ($g356 ^ $x1_15);
    $g438 = ($g437 ^ 1);
    $g439 = ($g438 ^ $x0_15);
    $g440 = ($g439 ^ 1);
    $g441 = ($g355 ^ $x1_14);
    $g442 = ($g441 ^ 1);
    $g443 = ($g442 ^ $x0_14);
    $g444 = ($g443 ^ 1);
    $g445 = ($g354 ^ $x1_13);
    $g446 = ($g445 ^ 1);
    $g447 = ($g446 ^ $x0_13);
    $g448 = ($g447 ^ 1);
    $g449 = ($g353 ^ $x1_12);
    $g450 = ($g449 ^ 1);
    $g451 = ($g450 ^ $x0_12);
    $g452 = ($g451 ^ 1);
    $g453 = ($g352 ^ $x1_11);
    $g454 = ($g453 ^ 1);
    $g455 = ($g454 ^ $x0_11);
    $g456 = ($g455 ^ 1);
    $g457 = ($g351 ^ $x1_10);
    $g458 = ($g457 ^ 1);
    $g459 = ($g458 ^ $x0_10);
    $g460 = ($g459 ^ 1);
    $g461 = ($g350 ^ $x1_9);
    $g462 = ($g461 ^ 1);
    $g463 = ($g462 ^ $x0_9);
    $g464 = ($g463 ^ 1);
    $g465 = ($g349 ^ $x1_8);
    $g466 = ($g465 ^ 1);
    $g467 = ($g466 ^ $x0_8);
    $g468 = ($g467 ^ 1);
    $g469 = ($g348 ^ $x1_7);
    $g470 = ($g469 ^ 1);
    $g471 = ($g470 ^ $x0_7);
    $g472 = ($g471 ^ 1);
    $g473 = ($g347 ^ $x1_6);
    $g474 = ($g473 ^ 1);
    $g475 = ($g474 ^ $x0_6);
    $g476 = ($g475 ^ 1);
    $g477 = ($g346 ^ $x1_5);
    $g478 = ($g477 ^ 1);
    $g479 = ($g478 ^ $x0_5);
    $g480 = ($g479 ^ 1);
    $g481 = ($g345 ^ $x1_4);
    $g482 = ($g481 ^ 1);
    $g483 = ($g482 ^ $x0_4);
    $g484 = ($g483 ^ 1);
    $g485 = ($g344 ^ $x1_3);
    $g486 = ($g485 ^ 1);
    $g487 = ($g486 ^ $x0_3);
    $g488 = ($g487 ^ 1);
    $g489 = ($g343 ^ $x1_2);
    $g490 = ($g489 ^ 1);
    $g491 = ($g490 ^ $x0_2);
    $g492 = ($g491 ^ 1);
    $g493 = ($x1_0 ^ $x1_1);
    $g494 = ($g493 ^ 1);
    $g495 = ($g494 ^ $x0_1);
    $g496 = ($g495 ^ 1);
    $g497 = ($x1_0 ^ $x0_0);
    $g498 = ($g497 ^ 1);
    $g499 = ($g498 ^ 1);
    $g500 = ($g499 | $g496);
    $g501 = ($g500 | $g492);
    $g502 = ($g501 | $g488);
    $g503 = ($g502 | $g484);
    $g504 = ($g503 | $g480);
    $g505 = ($g504 | $g476);
    $g506 = ($g505 | $g472);
    $g507 = ($g506 | $g468);
    $g508 = ($g507 | $g464);
    $g509 = ($g508 | $g460);
    $g510 = ($g509 | $g456);
    $g511 = ($g510 | $g452);
    $g512 = ($g511 | $g448);
    $g513 = ($g512 | $g444);
    $g514 = ($g513 | $g440);
    $g515 = ($g514 | $g436);
    $g516 = ($g515 | $g432);
    $g517 = ($g516 | $g428);
    $g518 = ($g517 | $g424);
    $g519 = ($g518 | $g420);
    $g520 = ($g519 | $g416);
    $g521 = ($g520 | $g412);
    $g522 = ($g521 | $g408);
    $g523 = ($g522 | $g404);
    $g524 = ($g523 | $g400);
    $g525 = ($g524 | $g396);
    $g526 = ($g525 | $g392);
    $g527 = ($g526 | $g388);
    $g528 = ($g527 | $g384);
    $g529 = ($g528 | $g380);
    $g530 = ($g529 | $g376);
    $g531 = ($g530 ^ 1);
    $g532 = ($g531 | $g342);
    $g533 = ($g532 ^ 1);
    $g534 = ($g533 & $x3_0);
    $g535 = ($g532 & $x2_0);
    $g536 = ($g535 | $g534);
    $g537 = ($g533 & $x3_1);
    $g538 = ($g532 & $x2_1);
    $g539 = ($g538 | $g537);
    $g540 = ($g533 & $x3_2);
    $g541 = ($g532 & $x2_2);
    $g542 = ($g541 | $g540);
    $g543 = ($g533 & $x3_3);
    $g544 = ($g532 & $x2_3);
    $g545 = ($g544 | $g543);
    $g546 = ($g533 & $x3_4);
    $g547 = ($g532 & $x2_4);
    $g548 = ($g547 | $g546);
    $g549 = ($g533 & $x3_5);
    $g550 = ($g532 & $x2_5);
    $g551 = ($g550 | $g549);
    $g552 = ($g533 & $x3_6);
    $g553 = ($g532 & $x2_6);
    $g554 = ($g553 | $g552);
    $g555 = ($g533 & $x3_7);
    $g556 = ($g532 & $x2_7);
    $g557 = ($g556 | $g555);
    $g558 = ($g533 & $x3_8);
    $g559 = ($g532 & $x2_8);
    $g560 = ($g559 | $g558);
    $g561 = ($g533 & $x3_9);
    $g562 = ($g532 & $x2_9);
    $g563 = ($g562 | $g561);
    $g564 = ($g533 & $x3_10);
    $g565 = ($g532 & $x2_10);
    $g566 = ($g565 | $g564);
    $g567 = ($g533 & $x3_11);
    $g568 = ($g532 & $x2_11);
    $g569 = ($g568 | $g567);
    $g570 = ($g533 & $x3_12);
    $g571 = ($g532 & $x2_12);
    $g572 = ($g571 | $g570);
    $g573 = ($g533 & $x3_13);
    $g574 = ($g532 & $x2_13);
    $g575 = ($g574 | $g573);
    $g576 = ($g533 & $x3_14);
    $g577 = ($g532 & $x2_14);
    $g578 = ($g577 | $g576);
    $g579 = ($g533 & $x3_15);
    $g580 = ($g532 & $x2_15);
    $g581 = ($g580 | $g579);
    $g582 = ($g533 & $x3_16);
    $g583 = ($g532 & $x2_16);
    $g584 = ($g583 | $g582);
    $g585 = ($g533 & $x3_17);
    $g586 = ($g532 & $x2_17);
    $g587 = ($g586 | $g585);
    $g588 = ($g533 & $x3_18);
    $g589 = ($g532 & $x2_18);
    $g590 = ($g589 | $g588);
    $g591 = ($g533 & $x3_19);
    $g592 = ($g532 & $x2_19);
    $g593 = ($g592 | $g591);
    $g594 = ($g533 & $x3_20);
    $g595 = ($g532 & $x2_20);
    $g596 = ($g595 | $g594);
    $g597 = ($g533 & $x3_21);
    $g598 = ($g532 & $x2_21);
    $g599 = ($g598 | $g597);
    $g600 = ($g533 & $x3_22);
    $g601 = ($g532 & $x2_22);
    $g602 = ($g601 | $g600);
    $g603 = ($g533 & $x3_23);
    $g604 = ($g532 & $x2_23);
    $g605 = ($g604 | $g603);
    $g606 = ($g533 & $x3_24);
    $g607 = ($g532 & $x2_24);
    $g608 = ($g607 | $g606);
    $g609 = ($g533 & $x3_25);
    $g610 = ($g532 & $x2_25);
    $g611 = ($g610 | $g609);
    $g612 = ($g533 & $x3_26);
    $g613 = ($g532 & $x2_26);
    $g614 = ($g613 | $g612);
    $g615 = ($g533 & $x3_27);
    $g616 = ($g532 & $x2_27);
    $g617 = ($g616 | $g615);
    $g618 = ($g533 & $x3_28);
    $g619 = ($g532 & $x2_28);
    $g620 = ($g619 | $g618);
    $g621 = ($g533 & $x3_29);
    $g622 = ($g532 & $x2_29);
    $g623 = ($g622 | $g621);
    $g624 = ($g533 & $x3_30);
    $g625 = ($g532 & $x2_30);
    $g626 = ($g625 | $g624);
    $g627 = ($g533 & $x3_31);
    $g628 = ($g532 & $x2_31);
    $g629 = ($g628 | $g627);
    $k0 = 0;
    $w0 = $k0;
    $w1 = ex_cat($w0, $k0, 1);
    $w2 = ex_cat($w1, $k0, 1);
    $w3 = ex_cat($w2, $k0, 1);
    $w4 = ex_cat($w3, $k0, 1);
    $w5 = ex_cat($w4, $k0, 1);
    $w6 = ex_cat($w5, $k0, 1);
    $w7 = ex_cat($w6, $k0, 1);
    $w8 = ex_cat($w7, $k0, 1);
    $w9 = ex_cat($w8, $k0, 1);
    $w10 = ex_cat($w9, $k0, 1);
    $w11 = ex_cat($w10, $k0, 1);
    $w12 = ex_cat($w11, $k0, 1);
    $w13 = ex_cat($w12, $k0, 1);
    $w14 = ex_cat($w13, $k0, 1);
    $w15 = ex_cat($w14, $k0, 1);
    $w16 = ex_cat($w15, $k0, 1);
    $w17 = ex_cat($w16, $k0, 1);
    $w18 = ex_cat($w17, $k0, 1);
    $w19 = ex_cat($w18, $k0, 1);
    $w20 = ex_cat($w19, $k0, 1);
    $w21 = ex_cat($w20, $k0, 1);
    $w22 = ex_cat($w21, $k0, 1);
    $w23 = ex_cat($w22, $k0, 1);
    $w24 = ex_cat($w23, $k0, 1);
    $w25 = ex_cat($w24, $k0, 1);
    $w26 = ex_cat($w25, $k0, 1);
    $w27 = ex_cat($w26, $k0, 1);
    $w28 = ex_cat($w27, $k0, 1);
    $w29 = ex_cat($w28, $k0, 1);
    $w30 = ex_cat($w29, $k0, 1);
    $w31 = ex_cat($w30, $k0, 1);
    $w32 = ex_cat($w31, $g629, 1);
    $w33 = ex_cat($w32, $g626, 1);
    $w34 = ex_cat($w33, $g623, 1);
    $w35 = ex_cat($w34, $g620, 1);
    $w36 = ex_cat($w35, $g617, 1);
    $w37 = ex_cat($w36, $g614, 1);
    $w38 = ex_cat($w37, $g611, 1);
    $w39 = ex_cat($w38, $g608, 1);
    $w40 = ex_cat($w39, $g605, 1);
    $w41 = ex_cat($w40, $g602, 1);
    $w42 = ex_cat($w41, $g599, 1);
    $w43 = ex_cat($w42, $g596, 1);
    $w44 = ex_cat($w43, $g593, 1);
    $w45 = ex_cat($w44, $g590, 1);
    $w46 = ex_cat($w45, $g587, 1);
    $w47 = ex_cat($w46, $g584, 1);
    $w48 = ex_cat($w47, $g581, 1);
    $w49 = ex_cat($w48, $g578, 1);
    $w50 = ex_cat($w49, $g575, 1);
    $w51 = ex_cat($w50, $g572, 1);
    $w52 = ex_cat($w51, $g569, 1);
    $w53 = ex_cat($w52, $g566, 1);
    $w54 = ex_cat($w53, $g563, 1);
    $w55 = ex_cat($w54, $g560, 1);
    $w56 = ex_cat($w55, $g557, 1);
    $w57 = ex_cat($w56, $g554, 1);
    $w58 = ex_cat($w57, $g551, 1);
    $w59 = ex_cat($w58, $g548, 1);
    $w60 = ex_cat($w59, $g545, 1);
    $w61 = ex_cat($w60, $g542, 1);
    $w62 = ex_cat($w61, $g539, 1);
    $w63 = ex_cat($w62, $g536, 1);
    return ex_m($w63, 64);
}



$handle = fopen("php://stdin", "r");
while (($line = fgets($handle)) !== false) {
    $text = trim($line);
    if ($text === "") { continue; }
    $values = preg_split("/\\s+/", $text);
    $ints = array();
    foreach ($values as $one) { $ints[] = ex_parse($one); }
    try {
        $answer = emu_cmovbe_gpr_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
