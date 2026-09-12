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
// one named local per gate, over the term of cmovle_gpr_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Or(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Not(Or(Extract(31, 31, v0) == 0, Extract(31, 31, v1) == 0))), Extract(31, 0, v2), Extract(31, 0, v3)))
function emu_cmovle_gpr_gpr_32__reg_rdi__php($a, $b, $c, $d) {
    $x3_0 = ex_ext($d, 0, 0);
    $x1_31 = ex_ext($a, 31, 31);
    $x0_31 = ex_ext($b, 31, 31);
    $x1_20 = ex_ext($a, 20, 20);
    $x0_20 = ex_ext($b, 20, 20);
    $x1_15 = ex_ext($a, 15, 15);
    $x0_15 = ex_ext($b, 15, 15);
    $x1_26 = ex_ext($a, 26, 26);
    $x0_26 = ex_ext($b, 26, 26);
    $x1_7 = ex_ext($a, 7, 7);
    $x0_7 = ex_ext($b, 7, 7);
    $x1_29 = ex_ext($a, 29, 29);
    $x0_29 = ex_ext($b, 29, 29);
    $x1_1 = ex_ext($a, 1, 1);
    $x0_1 = ex_ext($b, 1, 1);
    $x1_8 = ex_ext($a, 8, 8);
    $x0_8 = ex_ext($b, 8, 8);
    $x1_16 = ex_ext($a, 16, 16);
    $x0_16 = ex_ext($b, 16, 16);
    $x1_22 = ex_ext($a, 22, 22);
    $x0_22 = ex_ext($b, 22, 22);
    $x1_5 = ex_ext($a, 5, 5);
    $x0_5 = ex_ext($b, 5, 5);
    $x1_13 = ex_ext($a, 13, 13);
    $x0_13 = ex_ext($b, 13, 13);
    $x1_6 = ex_ext($a, 6, 6);
    $x0_6 = ex_ext($b, 6, 6);
    $x1_4 = ex_ext($a, 4, 4);
    $x0_4 = ex_ext($b, 4, 4);
    $x1_3 = ex_ext($a, 3, 3);
    $x0_3 = ex_ext($b, 3, 3);
    $x1_0 = ex_ext($a, 0, 0);
    $x0_0 = ex_ext($b, 0, 0);
    $x1_11 = ex_ext($a, 11, 11);
    $x0_11 = ex_ext($b, 11, 11);
    $x1_2 = ex_ext($a, 2, 2);
    $x0_2 = ex_ext($b, 2, 2);
    $x1_10 = ex_ext($a, 10, 10);
    $x0_10 = ex_ext($b, 10, 10);
    $x1_27 = ex_ext($a, 27, 27);
    $x0_27 = ex_ext($b, 27, 27);
    $x1_24 = ex_ext($a, 24, 24);
    $x0_24 = ex_ext($b, 24, 24);
    $x1_12 = ex_ext($a, 12, 12);
    $x0_12 = ex_ext($b, 12, 12);
    $x1_28 = ex_ext($a, 28, 28);
    $x0_28 = ex_ext($b, 28, 28);
    $x1_19 = ex_ext($a, 19, 19);
    $x0_19 = ex_ext($b, 19, 19);
    $x1_14 = ex_ext($a, 14, 14);
    $x0_14 = ex_ext($b, 14, 14);
    $x1_23 = ex_ext($a, 23, 23);
    $x0_23 = ex_ext($b, 23, 23);
    $x1_25 = ex_ext($a, 25, 25);
    $x0_25 = ex_ext($b, 25, 25);
    $x1_30 = ex_ext($a, 30, 30);
    $x0_30 = ex_ext($b, 30, 30);
    $x1_18 = ex_ext($a, 18, 18);
    $x0_18 = ex_ext($b, 18, 18);
    $x1_21 = ex_ext($a, 21, 21);
    $x0_21 = ex_ext($b, 21, 21);
    $x1_17 = ex_ext($a, 17, 17);
    $x0_17 = ex_ext($b, 17, 17);
    $x1_9 = ex_ext($a, 9, 9);
    $x0_9 = ex_ext($b, 9, 9);
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
    $g0 = ($x1_31 ^ 1);
    $g1 = ($x0_31 ^ 1);
    $g2 = ($g1 | $g0);
    $g3 = ($g2 ^ 1);
    $g4 = ($x1_20 ^ 1);
    $g5 = ($x0_20 ^ 1);
    $g6 = ($g5 | $g4);
    $g7 = ($g6 ^ 1);
    $g8 = ($x1_15 ^ 1);
    $g9 = ($x0_15 ^ 1);
    $g10 = ($g9 | $g8);
    $g11 = ($g10 ^ 1);
    $g12 = ($x1_26 ^ 1);
    $g13 = ($x0_26 ^ 1);
    $g14 = ($g13 | $g12);
    $g15 = ($g14 ^ 1);
    $g16 = ($x1_7 ^ 1);
    $g17 = ($x0_7 ^ 1);
    $g18 = ($g17 | $g16);
    $g19 = ($g18 ^ 1);
    $g20 = ($x1_29 ^ 1);
    $g21 = ($x0_29 ^ 1);
    $g22 = ($g21 | $g20);
    $g23 = ($g22 ^ 1);
    $g24 = ($x1_1 ^ 1);
    $g25 = ($x0_1 ^ 1);
    $g26 = ($g25 | $g24);
    $g27 = ($g26 ^ 1);
    $g28 = ($x1_8 ^ 1);
    $g29 = ($x0_8 ^ 1);
    $g30 = ($g29 | $g28);
    $g31 = ($g30 ^ 1);
    $g32 = ($x1_16 ^ 1);
    $g33 = ($x0_16 ^ 1);
    $g34 = ($g33 | $g32);
    $g35 = ($g34 ^ 1);
    $g36 = ($x1_22 ^ 1);
    $g37 = ($x0_22 ^ 1);
    $g38 = ($g37 | $g36);
    $g39 = ($g38 ^ 1);
    $g40 = ($x1_5 ^ 1);
    $g41 = ($x0_5 ^ 1);
    $g42 = ($g41 | $g40);
    $g43 = ($g42 ^ 1);
    $g44 = ($x1_13 ^ 1);
    $g45 = ($x0_13 ^ 1);
    $g46 = ($g45 | $g44);
    $g47 = ($g46 ^ 1);
    $g48 = ($x1_6 ^ 1);
    $g49 = ($x0_6 ^ 1);
    $g50 = ($g49 | $g48);
    $g51 = ($g50 ^ 1);
    $g52 = ($x1_4 ^ 1);
    $g53 = ($x0_4 ^ 1);
    $g54 = ($g53 | $g52);
    $g55 = ($g54 ^ 1);
    $g56 = ($x1_3 ^ 1);
    $g57 = ($x0_3 ^ 1);
    $g58 = ($g57 | $g56);
    $g59 = ($g58 ^ 1);
    $g60 = ($x1_0 ^ 1);
    $g61 = ($x0_0 ^ 1);
    $g62 = ($g61 | $g60);
    $g63 = ($g62 ^ 1);
    $g64 = ($x1_11 ^ 1);
    $g65 = ($x0_11 ^ 1);
    $g66 = ($g65 | $g64);
    $g67 = ($g66 ^ 1);
    $g68 = ($x1_2 ^ 1);
    $g69 = ($x0_2 ^ 1);
    $g70 = ($g69 | $g68);
    $g71 = ($g70 ^ 1);
    $g72 = ($x1_10 ^ 1);
    $g73 = ($x0_10 ^ 1);
    $g74 = ($g73 | $g72);
    $g75 = ($g74 ^ 1);
    $g76 = ($x1_27 ^ 1);
    $g77 = ($x0_27 ^ 1);
    $g78 = ($g77 | $g76);
    $g79 = ($g78 ^ 1);
    $g80 = ($x1_24 ^ 1);
    $g81 = ($x0_24 ^ 1);
    $g82 = ($g81 | $g80);
    $g83 = ($g82 ^ 1);
    $g84 = ($x1_12 ^ 1);
    $g85 = ($x0_12 ^ 1);
    $g86 = ($g85 | $g84);
    $g87 = ($g86 ^ 1);
    $g88 = ($x1_28 ^ 1);
    $g89 = ($x0_28 ^ 1);
    $g90 = ($g89 | $g88);
    $g91 = ($g90 ^ 1);
    $g92 = ($x1_19 ^ 1);
    $g93 = ($x0_19 ^ 1);
    $g94 = ($g93 | $g92);
    $g95 = ($g94 ^ 1);
    $g96 = ($x1_14 ^ 1);
    $g97 = ($x0_14 ^ 1);
    $g98 = ($g97 | $g96);
    $g99 = ($g98 ^ 1);
    $g100 = ($x1_23 ^ 1);
    $g101 = ($x0_23 ^ 1);
    $g102 = ($g101 | $g100);
    $g103 = ($g102 ^ 1);
    $g104 = ($x1_25 ^ 1);
    $g105 = ($x0_25 ^ 1);
    $g106 = ($g105 | $g104);
    $g107 = ($g106 ^ 1);
    $g108 = ($x1_30 ^ 1);
    $g109 = ($x0_30 ^ 1);
    $g110 = ($g109 | $g108);
    $g111 = ($g110 ^ 1);
    $g112 = ($x1_18 ^ 1);
    $g113 = ($x0_18 ^ 1);
    $g114 = ($g113 | $g112);
    $g115 = ($g114 ^ 1);
    $g116 = ($x1_21 ^ 1);
    $g117 = ($x0_21 ^ 1);
    $g118 = ($g117 | $g116);
    $g119 = ($g118 ^ 1);
    $g120 = ($x1_17 ^ 1);
    $g121 = ($x0_17 ^ 1);
    $g122 = ($g121 | $g120);
    $g123 = ($g122 ^ 1);
    $g124 = ($x1_9 ^ 1);
    $g125 = ($x0_9 ^ 1);
    $g126 = ($g125 | $g124);
    $g127 = ($g126 ^ 1);
    $g128 = ($g127 | $g123);
    $g129 = ($g128 | $g119);
    $g130 = ($g129 | $g115);
    $g131 = ($g130 | $g111);
    $g132 = ($g131 | $g107);
    $g133 = ($g132 | $g103);
    $g134 = ($g133 | $g99);
    $g135 = ($g134 | $g95);
    $g136 = ($g135 | $g91);
    $g137 = ($g136 | $g87);
    $g138 = ($g137 | $g83);
    $g139 = ($g138 | $g3);
    $g140 = ($g139 | $g79);
    $g141 = ($g140 | $g75);
    $g142 = ($g141 | $g71);
    $g143 = ($g142 | $g67);
    $g144 = ($g143 | $g63);
    $g145 = ($g144 | $g59);
    $g146 = ($g145 | $g55);
    $g147 = ($g146 | $g51);
    $g148 = ($g147 | $g47);
    $g149 = ($g148 | $g43);
    $g150 = ($g149 | $g39);
    $g151 = ($g150 | $g35);
    $g152 = ($g151 | $g31);
    $g153 = ($g152 | $g27);
    $g154 = ($g153 | $g23);
    $g155 = ($g154 | $g19);
    $g156 = ($g155 | $g15);
    $g157 = ($g156 | $g11);
    $g158 = ($g157 | $g7);
    $g159 = ($g158 ^ 1);
    $g160 = ($g159 | $g3);
    $g161 = ($g160 ^ 1);
    $g162 = ($g161 & $x3_0);
    $g163 = ($g160 & $x2_0);
    $g164 = ($g163 | $g162);
    $g165 = ($g161 & $x3_1);
    $g166 = ($g160 & $x2_1);
    $g167 = ($g166 | $g165);
    $g168 = ($g161 & $x3_2);
    $g169 = ($g160 & $x2_2);
    $g170 = ($g169 | $g168);
    $g171 = ($g161 & $x3_3);
    $g172 = ($g160 & $x2_3);
    $g173 = ($g172 | $g171);
    $g174 = ($g161 & $x3_4);
    $g175 = ($g160 & $x2_4);
    $g176 = ($g175 | $g174);
    $g177 = ($g161 & $x3_5);
    $g178 = ($g160 & $x2_5);
    $g179 = ($g178 | $g177);
    $g180 = ($g161 & $x3_6);
    $g181 = ($g160 & $x2_6);
    $g182 = ($g181 | $g180);
    $g183 = ($g161 & $x3_7);
    $g184 = ($g160 & $x2_7);
    $g185 = ($g184 | $g183);
    $g186 = ($g161 & $x3_8);
    $g187 = ($g160 & $x2_8);
    $g188 = ($g187 | $g186);
    $g189 = ($g161 & $x3_9);
    $g190 = ($g160 & $x2_9);
    $g191 = ($g190 | $g189);
    $g192 = ($g161 & $x3_10);
    $g193 = ($g160 & $x2_10);
    $g194 = ($g193 | $g192);
    $g195 = ($g161 & $x3_11);
    $g196 = ($g160 & $x2_11);
    $g197 = ($g196 | $g195);
    $g198 = ($g161 & $x3_12);
    $g199 = ($g160 & $x2_12);
    $g200 = ($g199 | $g198);
    $g201 = ($g161 & $x3_13);
    $g202 = ($g160 & $x2_13);
    $g203 = ($g202 | $g201);
    $g204 = ($g161 & $x3_14);
    $g205 = ($g160 & $x2_14);
    $g206 = ($g205 | $g204);
    $g207 = ($g161 & $x3_15);
    $g208 = ($g160 & $x2_15);
    $g209 = ($g208 | $g207);
    $g210 = ($g161 & $x3_16);
    $g211 = ($g160 & $x2_16);
    $g212 = ($g211 | $g210);
    $g213 = ($g161 & $x3_17);
    $g214 = ($g160 & $x2_17);
    $g215 = ($g214 | $g213);
    $g216 = ($g161 & $x3_18);
    $g217 = ($g160 & $x2_18);
    $g218 = ($g217 | $g216);
    $g219 = ($g161 & $x3_19);
    $g220 = ($g160 & $x2_19);
    $g221 = ($g220 | $g219);
    $g222 = ($g161 & $x3_20);
    $g223 = ($g160 & $x2_20);
    $g224 = ($g223 | $g222);
    $g225 = ($g161 & $x3_21);
    $g226 = ($g160 & $x2_21);
    $g227 = ($g226 | $g225);
    $g228 = ($g161 & $x3_22);
    $g229 = ($g160 & $x2_22);
    $g230 = ($g229 | $g228);
    $g231 = ($g161 & $x3_23);
    $g232 = ($g160 & $x2_23);
    $g233 = ($g232 | $g231);
    $g234 = ($g161 & $x3_24);
    $g235 = ($g160 & $x2_24);
    $g236 = ($g235 | $g234);
    $g237 = ($g161 & $x3_25);
    $g238 = ($g160 & $x2_25);
    $g239 = ($g238 | $g237);
    $g240 = ($g161 & $x3_26);
    $g241 = ($g160 & $x2_26);
    $g242 = ($g241 | $g240);
    $g243 = ($g161 & $x3_27);
    $g244 = ($g160 & $x2_27);
    $g245 = ($g244 | $g243);
    $g246 = ($g161 & $x3_28);
    $g247 = ($g160 & $x2_28);
    $g248 = ($g247 | $g246);
    $g249 = ($g161 & $x3_29);
    $g250 = ($g160 & $x2_29);
    $g251 = ($g250 | $g249);
    $g252 = ($g161 & $x3_30);
    $g253 = ($g160 & $x2_30);
    $g254 = ($g253 | $g252);
    $g255 = ($g161 & $x3_31);
    $g256 = ($g160 & $x2_31);
    $g257 = ($g256 | $g255);
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
    $w32 = ex_cat($w31, $g257, 1);
    $w33 = ex_cat($w32, $g254, 1);
    $w34 = ex_cat($w33, $g251, 1);
    $w35 = ex_cat($w34, $g248, 1);
    $w36 = ex_cat($w35, $g245, 1);
    $w37 = ex_cat($w36, $g242, 1);
    $w38 = ex_cat($w37, $g239, 1);
    $w39 = ex_cat($w38, $g236, 1);
    $w40 = ex_cat($w39, $g233, 1);
    $w41 = ex_cat($w40, $g230, 1);
    $w42 = ex_cat($w41, $g227, 1);
    $w43 = ex_cat($w42, $g224, 1);
    $w44 = ex_cat($w43, $g221, 1);
    $w45 = ex_cat($w44, $g218, 1);
    $w46 = ex_cat($w45, $g215, 1);
    $w47 = ex_cat($w46, $g212, 1);
    $w48 = ex_cat($w47, $g209, 1);
    $w49 = ex_cat($w48, $g206, 1);
    $w50 = ex_cat($w49, $g203, 1);
    $w51 = ex_cat($w50, $g200, 1);
    $w52 = ex_cat($w51, $g197, 1);
    $w53 = ex_cat($w52, $g194, 1);
    $w54 = ex_cat($w53, $g191, 1);
    $w55 = ex_cat($w54, $g188, 1);
    $w56 = ex_cat($w55, $g185, 1);
    $w57 = ex_cat($w56, $g182, 1);
    $w58 = ex_cat($w57, $g179, 1);
    $w59 = ex_cat($w58, $g176, 1);
    $w60 = ex_cat($w59, $g173, 1);
    $w61 = ex_cat($w60, $g170, 1);
    $w62 = ex_cat($w61, $g167, 1);
    $w63 = ex_cat($w62, $g164, 1);
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
        $answer = emu_cmovle_gpr_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
