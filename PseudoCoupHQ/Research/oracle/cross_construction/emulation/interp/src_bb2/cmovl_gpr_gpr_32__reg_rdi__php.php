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
// one named local per gate, over the term of cmovl_gpr_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(31, 31, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1)) == If(Extract(31, 31, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))) == Extract(32, 32, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))), 1, 0), Extract(31, 0, v2), Extract(31, 0, v3)))
function emu_cmovl_gpr_gpr_32__reg_rdi__php($a, $b, $c, $d) {
    $x3_0 = ex_ext($d, 0, 0);
    $x0_31 = ex_ext($b, 31, 31);
    $x0_1 = ex_ext($b, 1, 1);
    $x0_0 = ex_ext($b, 0, 0);
    $x0_2 = ex_ext($b, 2, 2);
    $x0_3 = ex_ext($b, 3, 3);
    $x0_4 = ex_ext($b, 4, 4);
    $x0_5 = ex_ext($b, 5, 5);
    $x0_6 = ex_ext($b, 6, 6);
    $x0_7 = ex_ext($b, 7, 7);
    $x0_8 = ex_ext($b, 8, 8);
    $x0_9 = ex_ext($b, 9, 9);
    $x0_10 = ex_ext($b, 10, 10);
    $x0_11 = ex_ext($b, 11, 11);
    $x0_12 = ex_ext($b, 12, 12);
    $x0_13 = ex_ext($b, 13, 13);
    $x0_14 = ex_ext($b, 14, 14);
    $x0_15 = ex_ext($b, 15, 15);
    $x0_16 = ex_ext($b, 16, 16);
    $x0_17 = ex_ext($b, 17, 17);
    $x0_18 = ex_ext($b, 18, 18);
    $x0_19 = ex_ext($b, 19, 19);
    $x0_20 = ex_ext($b, 20, 20);
    $x0_21 = ex_ext($b, 21, 21);
    $x0_22 = ex_ext($b, 22, 22);
    $x0_23 = ex_ext($b, 23, 23);
    $x0_24 = ex_ext($b, 24, 24);
    $x0_25 = ex_ext($b, 25, 25);
    $x0_26 = ex_ext($b, 26, 26);
    $x0_27 = ex_ext($b, 27, 27);
    $x0_28 = ex_ext($b, 28, 28);
    $x0_29 = ex_ext($b, 29, 29);
    $x0_30 = ex_ext($b, 30, 30);
    $x1_30 = ex_ext($a, 30, 30);
    $x1_29 = ex_ext($a, 29, 29);
    $x1_28 = ex_ext($a, 28, 28);
    $x1_27 = ex_ext($a, 27, 27);
    $x1_26 = ex_ext($a, 26, 26);
    $x1_20 = ex_ext($a, 20, 20);
    $x1_17 = ex_ext($a, 17, 17);
    $x1_14 = ex_ext($a, 14, 14);
    $x1_10 = ex_ext($a, 10, 10);
    $x1_8 = ex_ext($a, 8, 8);
    $x1_2 = ex_ext($a, 2, 2);
    $x1_1 = ex_ext($a, 1, 1);
    $x1_0 = ex_ext($a, 0, 0);
    $x1_3 = ex_ext($a, 3, 3);
    $x1_4 = ex_ext($a, 4, 4);
    $x1_5 = ex_ext($a, 5, 5);
    $x1_6 = ex_ext($a, 6, 6);
    $x1_7 = ex_ext($a, 7, 7);
    $x1_9 = ex_ext($a, 9, 9);
    $x1_11 = ex_ext($a, 11, 11);
    $x1_12 = ex_ext($a, 12, 12);
    $x1_13 = ex_ext($a, 13, 13);
    $x1_15 = ex_ext($a, 15, 15);
    $x1_16 = ex_ext($a, 16, 16);
    $x1_18 = ex_ext($a, 18, 18);
    $x1_19 = ex_ext($a, 19, 19);
    $x1_21 = ex_ext($a, 21, 21);
    $x1_22 = ex_ext($a, 22, 22);
    $x1_23 = ex_ext($a, 23, 23);
    $x1_24 = ex_ext($a, 24, 24);
    $x1_25 = ex_ext($a, 25, 25);
    $x1_31 = ex_ext($a, 31, 31);
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
    $g0 = ($x0_0 | $x0_1);
    $g1 = ($x0_2 | $g0);
    $g2 = ($x0_3 | $g1);
    $g3 = ($x0_4 | $g2);
    $g4 = ($x0_5 | $g3);
    $g5 = ($x0_6 | $g4);
    $g6 = ($x0_7 | $g5);
    $g7 = ($x0_8 | $g6);
    $g8 = ($x0_9 | $g7);
    $g9 = ($x0_10 | $g8);
    $g10 = ($x0_11 | $g9);
    $g11 = ($x0_12 | $g10);
    $g12 = ($x0_13 | $g11);
    $g13 = ($x0_14 | $g12);
    $g14 = ($x0_15 | $g13);
    $g15 = ($x0_16 | $g14);
    $g16 = ($x0_17 | $g15);
    $g17 = ($x0_18 | $g16);
    $g18 = ($x0_19 | $g17);
    $g19 = ($x0_20 | $g18);
    $g20 = ($x0_21 | $g19);
    $g21 = ($x0_22 | $g20);
    $g22 = ($x0_23 | $g21);
    $g23 = ($x0_24 | $g22);
    $g24 = ($x0_25 | $g23);
    $g25 = ($x0_26 | $g24);
    $g26 = ($x0_27 | $g25);
    $g27 = ($x0_28 | $g26);
    $g28 = ($x0_29 | $g27);
    $g29 = ($x0_30 | $g28);
    $g30 = ($x0_31 | $g29);
    $g31 = ($g30 ^ $x0_31);
    $g32 = ($g31 ^ 1);
    $g33 = ($x1_30 ^ 1);
    $g34 = ($g28 ^ $x0_30);
    $g35 = ($g34 ^ 1);
    $g36 = ($g35 | $g33);
    $g37 = ($g36 ^ 1);
    $g38 = ($g27 ^ $x0_29);
    $g39 = ($g38 ^ 1);
    $g40 = ($x1_29 ^ 1);
    $g41 = ($g40 | $g39);
    $g42 = ($g41 ^ 1);
    $g43 = ($x1_28 ^ 1);
    $g44 = ($g26 ^ $x0_28);
    $g45 = ($g44 ^ 1);
    $g46 = ($g45 | $g43);
    $g47 = ($g46 ^ 1);
    $g48 = ($g25 ^ $x0_27);
    $g49 = ($g48 ^ 1);
    $g50 = ($x1_27 ^ 1);
    $g51 = ($g50 | $g49);
    $g52 = ($g51 ^ 1);
    $g53 = ($x1_26 ^ 1);
    $g54 = ($g24 ^ $x0_26);
    $g55 = ($g54 ^ 1);
    $g56 = ($g55 | $g53);
    $g57 = ($g56 ^ 1);
    $g58 = ($g22 ^ $x0_24);
    $g59 = ($g58 ^ 1);
    $g60 = ($g21 ^ $x0_23);
    $g61 = ($g60 ^ 1);
    $g62 = ($g19 ^ $x0_21);
    $g63 = ($g62 ^ 1);
    $g64 = ($x1_20 ^ 1);
    $g65 = ($g18 ^ $x0_20);
    $g66 = ($g65 ^ 1);
    $g67 = ($g66 | $g64);
    $g68 = ($g67 ^ 1);
    $g69 = ($g15 ^ $x0_17);
    $g70 = ($g69 ^ 1);
    $g71 = ($x1_17 ^ 1);
    $g72 = ($g71 | $g70);
    $g73 = ($g72 ^ 1);
    $g74 = ($x1_14 ^ 1);
    $g75 = ($g12 ^ $x0_14);
    $g76 = ($g75 ^ 1);
    $g77 = ($g76 | $g74);
    $g78 = ($g77 ^ 1);
    $g79 = ($g8 ^ $x0_10);
    $g80 = ($g79 ^ 1);
    $g81 = ($x1_10 ^ 1);
    $g82 = ($g81 | $g80);
    $g83 = ($g82 ^ 1);
    $g84 = ($x1_8 ^ 1);
    $g85 = ($g6 ^ $x0_8);
    $g86 = ($g85 ^ 1);
    $g87 = ($g86 | $g84);
    $g88 = ($g87 ^ 1);
    $g89 = ($g2 ^ $x0_4);
    $g90 = ($g89 ^ 1);
    $g91 = ($x1_2 ^ 1);
    $g92 = ($g0 ^ $x0_2);
    $g93 = ($g92 ^ 1);
    $g94 = ($g93 | $g91);
    $g95 = ($g94 ^ 1);
    $g96 = ($x1_1 ^ 1);
    $g97 = ($x0_0 ^ $x0_1);
    $g98 = ($g97 ^ 1);
    $g99 = ($g98 | $g96);
    $g100 = ($g99 ^ 1);
    $g101 = ($x1_0 ^ 1);
    $g102 = ($x0_0 ^ 1);
    $g103 = ($g102 | $g101);
    $g104 = ($g98 | $g103);
    $g105 = ($g104 ^ 1);
    $g106 = ($g96 | $g103);
    $g107 = ($g106 ^ 1);
    $g108 = ($g107 | $g105);
    $g109 = ($g108 | $g100);
    $g110 = ($g109 ^ 1);
    $g111 = ($g91 | $g110);
    $g112 = ($g111 ^ 1);
    $g113 = ($g93 | $g110);
    $g114 = ($g113 ^ 1);
    $g115 = ($g114 | $g112);
    $g116 = ($g115 | $g95);
    $g117 = ($g116 ^ 1);
    $g118 = ($x1_3 ^ 1);
    $g119 = ($g118 | $g117);
    $g120 = ($g119 ^ 1);
    $g121 = ($g1 ^ $x0_3);
    $g122 = ($g121 ^ 1);
    $g123 = ($g122 | $g118);
    $g124 = ($g123 ^ 1);
    $g125 = ($g122 | $g117);
    $g126 = ($g125 ^ 1);
    $g127 = ($g126 | $g124);
    $g128 = ($g127 | $g120);
    $g129 = ($g128 ^ 1);
    $g130 = ($g129 | $g90);
    $g131 = ($g130 ^ 1);
    $g132 = ($x1_4 ^ 1);
    $g133 = ($g132 | $g129);
    $g134 = ($g133 ^ 1);
    $g135 = ($g132 | $g90);
    $g136 = ($g135 ^ 1);
    $g137 = ($g136 | $g134);
    $g138 = ($g137 | $g131);
    $g139 = ($g138 ^ 1);
    $g140 = ($x1_5 ^ 1);
    $g141 = ($g140 | $g139);
    $g142 = ($g141 ^ 1);
    $g143 = ($g3 ^ $x0_5);
    $g144 = ($g143 ^ 1);
    $g145 = ($g144 | $g139);
    $g146 = ($g145 ^ 1);
    $g147 = ($g140 | $g144);
    $g148 = ($g147 ^ 1);
    $g149 = ($g148 | $g146);
    $g150 = ($g149 | $g142);
    $g151 = ($g150 ^ 1);
    $g152 = ($x1_6 ^ 1);
    $g153 = ($g152 | $g151);
    $g154 = ($g153 ^ 1);
    $g155 = ($g4 ^ $x0_6);
    $g156 = ($g155 ^ 1);
    $g157 = ($g156 | $g151);
    $g158 = ($g157 ^ 1);
    $g159 = ($g152 | $g156);
    $g160 = ($g159 ^ 1);
    $g161 = ($g160 | $g158);
    $g162 = ($g161 | $g154);
    $g163 = ($g162 ^ 1);
    $g164 = ($g5 ^ $x0_7);
    $g165 = ($g164 ^ 1);
    $g166 = ($g165 | $g163);
    $g167 = ($g166 ^ 1);
    $g168 = ($x1_7 ^ 1);
    $g169 = ($g168 | $g165);
    $g170 = ($g169 ^ 1);
    $g171 = ($g168 | $g163);
    $g172 = ($g171 ^ 1);
    $g173 = ($g172 | $g170);
    $g174 = ($g173 | $g167);
    $g175 = ($g174 ^ 1);
    $g176 = ($g86 | $g175);
    $g177 = ($g176 ^ 1);
    $g178 = ($g84 | $g175);
    $g179 = ($g178 ^ 1);
    $g180 = ($g179 | $g177);
    $g181 = ($g180 | $g88);
    $g182 = ($g181 ^ 1);
    $g183 = ($x1_9 ^ 1);
    $g184 = ($g183 | $g182);
    $g185 = ($g184 ^ 1);
    $g186 = ($g7 ^ $x0_9);
    $g187 = ($g186 ^ 1);
    $g188 = ($g183 | $g187);
    $g189 = ($g188 ^ 1);
    $g190 = ($g182 | $g187);
    $g191 = ($g190 ^ 1);
    $g192 = ($g191 | $g189);
    $g193 = ($g192 | $g185);
    $g194 = ($g193 ^ 1);
    $g195 = ($g81 | $g194);
    $g196 = ($g195 ^ 1);
    $g197 = ($g194 | $g80);
    $g198 = ($g197 ^ 1);
    $g199 = ($g198 | $g196);
    $g200 = ($g199 | $g83);
    $g201 = ($g200 ^ 1);
    $g202 = ($g9 ^ $x0_11);
    $g203 = ($g202 ^ 1);
    $g204 = ($g203 | $g201);
    $g205 = ($g204 ^ 1);
    $g206 = ($x1_11 ^ 1);
    $g207 = ($g206 | $g201);
    $g208 = ($g207 ^ 1);
    $g209 = ($g203 | $g206);
    $g210 = ($g209 ^ 1);
    $g211 = ($g210 | $g208);
    $g212 = ($g211 | $g205);
    $g213 = ($g212 ^ 1);
    $g214 = ($x1_12 ^ 1);
    $g215 = ($g214 | $g213);
    $g216 = ($g215 ^ 1);
    $g217 = ($g10 ^ $x0_12);
    $g218 = ($g217 ^ 1);
    $g219 = ($g218 | $g213);
    $g220 = ($g219 ^ 1);
    $g221 = ($g218 | $g214);
    $g222 = ($g221 ^ 1);
    $g223 = ($g222 | $g220);
    $g224 = ($g223 | $g216);
    $g225 = ($g224 ^ 1);
    $g226 = ($x1_13 ^ 1);
    $g227 = ($g226 | $g225);
    $g228 = ($g227 ^ 1);
    $g229 = ($g11 ^ $x0_13);
    $g230 = ($g229 ^ 1);
    $g231 = ($g225 | $g230);
    $g232 = ($g231 ^ 1);
    $g233 = ($g226 | $g230);
    $g234 = ($g233 ^ 1);
    $g235 = ($g234 | $g232);
    $g236 = ($g235 | $g228);
    $g237 = ($g236 ^ 1);
    $g238 = ($g76 | $g237);
    $g239 = ($g238 ^ 1);
    $g240 = ($g74 | $g237);
    $g241 = ($g240 ^ 1);
    $g242 = ($g241 | $g239);
    $g243 = ($g242 | $g78);
    $g244 = ($g243 ^ 1);
    $g245 = ($x1_15 ^ 1);
    $g246 = ($g245 | $g244);
    $g247 = ($g246 ^ 1);
    $g248 = ($g13 ^ $x0_15);
    $g249 = ($g248 ^ 1);
    $g250 = ($g245 | $g249);
    $g251 = ($g250 ^ 1);
    $g252 = ($g244 | $g249);
    $g253 = ($g252 ^ 1);
    $g254 = ($g253 | $g251);
    $g255 = ($g254 | $g247);
    $g256 = ($g255 ^ 1);
    $g257 = ($x1_16 ^ 1);
    $g258 = ($g257 | $g256);
    $g259 = ($g258 ^ 1);
    $g260 = ($g14 ^ $x0_16);
    $g261 = ($g260 ^ 1);
    $g262 = ($g261 | $g257);
    $g263 = ($g262 ^ 1);
    $g264 = ($g261 | $g256);
    $g265 = ($g264 ^ 1);
    $g266 = ($g265 | $g263);
    $g267 = ($g266 | $g259);
    $g268 = ($g267 ^ 1);
    $g269 = ($g71 | $g268);
    $g270 = ($g269 ^ 1);
    $g271 = ($g268 | $g70);
    $g272 = ($g271 ^ 1);
    $g273 = ($g272 | $g270);
    $g274 = ($g273 | $g73);
    $g275 = ($g274 ^ 1);
    $g276 = ($x1_18 ^ 1);
    $g277 = ($g276 | $g275);
    $g278 = ($g277 ^ 1);
    $g279 = ($g16 ^ $x0_18);
    $g280 = ($g279 ^ 1);
    $g281 = ($g275 | $g280);
    $g282 = ($g281 ^ 1);
    $g283 = ($g276 | $g280);
    $g284 = ($g283 ^ 1);
    $g285 = ($g284 | $g282);
    $g286 = ($g285 | $g278);
    $g287 = ($g286 ^ 1);
    $g288 = ($x1_19 ^ 1);
    $g289 = ($g288 | $g287);
    $g290 = ($g289 ^ 1);
    $g291 = ($g17 ^ $x0_19);
    $g292 = ($g291 ^ 1);
    $g293 = ($g292 | $g288);
    $g294 = ($g293 ^ 1);
    $g295 = ($g287 | $g292);
    $g296 = ($g295 ^ 1);
    $g297 = ($g296 | $g294);
    $g298 = ($g297 | $g290);
    $g299 = ($g298 ^ 1);
    $g300 = ($g64 | $g299);
    $g301 = ($g300 ^ 1);
    $g302 = ($g299 | $g66);
    $g303 = ($g302 ^ 1);
    $g304 = ($g303 | $g301);
    $g305 = ($g304 | $g68);
    $g306 = ($g305 ^ 1);
    $g307 = ($g306 | $g63);
    $g308 = ($g307 ^ 1);
    $g309 = ($x1_21 ^ 1);
    $g310 = ($g309 | $g306);
    $g311 = ($g310 ^ 1);
    $g312 = ($g309 | $g63);
    $g313 = ($g312 ^ 1);
    $g314 = ($g313 | $g311);
    $g315 = ($g314 | $g308);
    $g316 = ($g315 ^ 1);
    $g317 = ($x1_22 ^ 1);
    $g318 = ($g317 | $g316);
    $g319 = ($g318 ^ 1);
    $g320 = ($g20 ^ $x0_22);
    $g321 = ($g320 ^ 1);
    $g322 = ($g321 | $g317);
    $g323 = ($g322 ^ 1);
    $g324 = ($g321 | $g316);
    $g325 = ($g324 ^ 1);
    $g326 = ($g325 | $g323);
    $g327 = ($g326 | $g319);
    $g328 = ($g327 ^ 1);
    $g329 = ($g328 | $g61);
    $g330 = ($g329 ^ 1);
    $g331 = ($x1_23 ^ 1);
    $g332 = ($g331 | $g61);
    $g333 = ($g332 ^ 1);
    $g334 = ($g331 | $g328);
    $g335 = ($g334 ^ 1);
    $g336 = ($g335 | $g333);
    $g337 = ($g336 | $g330);
    $g338 = ($g337 ^ 1);
    $g339 = ($g338 | $g59);
    $g340 = ($g339 ^ 1);
    $g341 = ($x1_24 ^ 1);
    $g342 = ($g341 | $g59);
    $g343 = ($g342 ^ 1);
    $g344 = ($g341 | $g338);
    $g345 = ($g344 ^ 1);
    $g346 = ($g345 | $g343);
    $g347 = ($g346 | $g340);
    $g348 = ($g347 ^ 1);
    $g349 = ($g23 ^ $x0_25);
    $g350 = ($g349 ^ 1);
    $g351 = ($g350 | $g348);
    $g352 = ($g351 ^ 1);
    $g353 = ($x1_25 ^ 1);
    $g354 = ($g350 | $g353);
    $g355 = ($g354 ^ 1);
    $g356 = ($g353 | $g348);
    $g357 = ($g356 ^ 1);
    $g358 = ($g357 | $g355);
    $g359 = ($g358 | $g352);
    $g360 = ($g359 ^ 1);
    $g361 = ($g360 | $g55);
    $g362 = ($g361 ^ 1);
    $g363 = ($g53 | $g360);
    $g364 = ($g363 ^ 1);
    $g365 = ($g364 | $g362);
    $g366 = ($g365 | $g57);
    $g367 = ($g366 ^ 1);
    $g368 = ($g50 | $g367);
    $g369 = ($g368 ^ 1);
    $g370 = ($g367 | $g49);
    $g371 = ($g370 ^ 1);
    $g372 = ($g371 | $g369);
    $g373 = ($g372 | $g52);
    $g374 = ($g373 ^ 1);
    $g375 = ($g43 | $g374);
    $g376 = ($g375 ^ 1);
    $g377 = ($g45 | $g374);
    $g378 = ($g377 ^ 1);
    $g379 = ($g378 | $g376);
    $g380 = ($g379 | $g47);
    $g381 = ($g380 ^ 1);
    $g382 = ($g39 | $g381);
    $g383 = ($g382 ^ 1);
    $g384 = ($g40 | $g381);
    $g385 = ($g384 ^ 1);
    $g386 = ($g385 | $g383);
    $g387 = ($g386 | $g42);
    $g388 = ($g387 ^ 1);
    $g389 = ($g388 | $g35);
    $g390 = ($g389 ^ 1);
    $g391 = ($g33 | $g388);
    $g392 = ($g391 ^ 1);
    $g393 = ($g392 | $g390);
    $g394 = ($g393 | $g37);
    $g395 = ($g394 ^ 1);
    $g396 = ($x1_31 ^ 1);
    $g397 = ($g396 | $g395);
    $g398 = ($g397 ^ 1);
    $g399 = ($g29 ^ $x0_31);
    $g400 = ($g399 ^ 1);
    $g401 = ($g400 | $g395);
    $g402 = ($g401 ^ 1);
    $g403 = ($g396 | $g400);
    $g404 = ($g403 ^ 1);
    $g405 = ($g404 | $g402);
    $g406 = ($g405 | $g398);
    $g407 = ($x1_31 ^ $g406);
    $g408 = ($g407 ^ 1);
    $g409 = ($g408 ^ $g32);
    $g410 = ($g409 ^ 1);
    $g411 = ($x1_31 ^ $g394);
    $g412 = ($g411 ^ 1);
    $g413 = ($g412 ^ $g400);
    $g414 = ($g413 ^ 1);
    $g415 = ($g414 ^ $g410);
    $g416 = ($g415 ^ 1);
    $g417 = ($g414 ^ $g416);
    $g418 = ($g417 ^ 1);
    $g419 = ($g418 ^ 1);
    $g420 = ($g419 ^ 1);
    $g421 = ($g420 & $x3_0);
    $g422 = ($g419 & $x2_0);
    $g423 = ($g422 | $g421);
    $g424 = ($g420 & $x3_1);
    $g425 = ($g419 & $x2_1);
    $g426 = ($g425 | $g424);
    $g427 = ($g420 & $x3_2);
    $g428 = ($g419 & $x2_2);
    $g429 = ($g428 | $g427);
    $g430 = ($g420 & $x3_3);
    $g431 = ($g419 & $x2_3);
    $g432 = ($g431 | $g430);
    $g433 = ($g420 & $x3_4);
    $g434 = ($g419 & $x2_4);
    $g435 = ($g434 | $g433);
    $g436 = ($g420 & $x3_5);
    $g437 = ($g419 & $x2_5);
    $g438 = ($g437 | $g436);
    $g439 = ($g420 & $x3_6);
    $g440 = ($g419 & $x2_6);
    $g441 = ($g440 | $g439);
    $g442 = ($g420 & $x3_7);
    $g443 = ($g419 & $x2_7);
    $g444 = ($g443 | $g442);
    $g445 = ($g420 & $x3_8);
    $g446 = ($g419 & $x2_8);
    $g447 = ($g446 | $g445);
    $g448 = ($g420 & $x3_9);
    $g449 = ($g419 & $x2_9);
    $g450 = ($g449 | $g448);
    $g451 = ($g420 & $x3_10);
    $g452 = ($g419 & $x2_10);
    $g453 = ($g452 | $g451);
    $g454 = ($g420 & $x3_11);
    $g455 = ($g419 & $x2_11);
    $g456 = ($g455 | $g454);
    $g457 = ($g420 & $x3_12);
    $g458 = ($g419 & $x2_12);
    $g459 = ($g458 | $g457);
    $g460 = ($g420 & $x3_13);
    $g461 = ($g419 & $x2_13);
    $g462 = ($g461 | $g460);
    $g463 = ($g420 & $x3_14);
    $g464 = ($g419 & $x2_14);
    $g465 = ($g464 | $g463);
    $g466 = ($g420 & $x3_15);
    $g467 = ($g419 & $x2_15);
    $g468 = ($g467 | $g466);
    $g469 = ($g420 & $x3_16);
    $g470 = ($g419 & $x2_16);
    $g471 = ($g470 | $g469);
    $g472 = ($g420 & $x3_17);
    $g473 = ($g419 & $x2_17);
    $g474 = ($g473 | $g472);
    $g475 = ($g420 & $x3_18);
    $g476 = ($g419 & $x2_18);
    $g477 = ($g476 | $g475);
    $g478 = ($g420 & $x3_19);
    $g479 = ($g419 & $x2_19);
    $g480 = ($g479 | $g478);
    $g481 = ($g420 & $x3_20);
    $g482 = ($g419 & $x2_20);
    $g483 = ($g482 | $g481);
    $g484 = ($g420 & $x3_21);
    $g485 = ($g419 & $x2_21);
    $g486 = ($g485 | $g484);
    $g487 = ($g420 & $x3_22);
    $g488 = ($g419 & $x2_22);
    $g489 = ($g488 | $g487);
    $g490 = ($g420 & $x3_23);
    $g491 = ($g419 & $x2_23);
    $g492 = ($g491 | $g490);
    $g493 = ($g420 & $x3_24);
    $g494 = ($g419 & $x2_24);
    $g495 = ($g494 | $g493);
    $g496 = ($g420 & $x3_25);
    $g497 = ($g419 & $x2_25);
    $g498 = ($g497 | $g496);
    $g499 = ($g420 & $x3_26);
    $g500 = ($g419 & $x2_26);
    $g501 = ($g500 | $g499);
    $g502 = ($g420 & $x3_27);
    $g503 = ($g419 & $x2_27);
    $g504 = ($g503 | $g502);
    $g505 = ($g420 & $x3_28);
    $g506 = ($g419 & $x2_28);
    $g507 = ($g506 | $g505);
    $g508 = ($g420 & $x3_29);
    $g509 = ($g419 & $x2_29);
    $g510 = ($g509 | $g508);
    $g511 = ($g420 & $x3_30);
    $g512 = ($g419 & $x2_30);
    $g513 = ($g512 | $g511);
    $g514 = ($g420 & $x3_31);
    $g515 = ($g419 & $x2_31);
    $g516 = ($g515 | $g514);
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
    $w32 = ex_cat($w31, $g516, 1);
    $w33 = ex_cat($w32, $g513, 1);
    $w34 = ex_cat($w33, $g510, 1);
    $w35 = ex_cat($w34, $g507, 1);
    $w36 = ex_cat($w35, $g504, 1);
    $w37 = ex_cat($w36, $g501, 1);
    $w38 = ex_cat($w37, $g498, 1);
    $w39 = ex_cat($w38, $g495, 1);
    $w40 = ex_cat($w39, $g492, 1);
    $w41 = ex_cat($w40, $g489, 1);
    $w42 = ex_cat($w41, $g486, 1);
    $w43 = ex_cat($w42, $g483, 1);
    $w44 = ex_cat($w43, $g480, 1);
    $w45 = ex_cat($w44, $g477, 1);
    $w46 = ex_cat($w45, $g474, 1);
    $w47 = ex_cat($w46, $g471, 1);
    $w48 = ex_cat($w47, $g468, 1);
    $w49 = ex_cat($w48, $g465, 1);
    $w50 = ex_cat($w49, $g462, 1);
    $w51 = ex_cat($w50, $g459, 1);
    $w52 = ex_cat($w51, $g456, 1);
    $w53 = ex_cat($w52, $g453, 1);
    $w54 = ex_cat($w53, $g450, 1);
    $w55 = ex_cat($w54, $g447, 1);
    $w56 = ex_cat($w55, $g444, 1);
    $w57 = ex_cat($w56, $g441, 1);
    $w58 = ex_cat($w57, $g438, 1);
    $w59 = ex_cat($w58, $g435, 1);
    $w60 = ex_cat($w59, $g432, 1);
    $w61 = ex_cat($w60, $g429, 1);
    $w62 = ex_cat($w61, $g426, 1);
    $w63 = ex_cat($w62, $g423, 1);
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
        $answer = emu_cmovl_gpr_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
