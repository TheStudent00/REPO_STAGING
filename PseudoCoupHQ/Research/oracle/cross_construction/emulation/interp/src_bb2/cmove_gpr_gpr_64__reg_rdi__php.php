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
// one named local per gate, over the term of cmove_gpr_gpr_64__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   If(~(~v0 | ~v1) == 0, v2, v3)
function emu_cmove_gpr_gpr_64__reg_rdi__php($a, $b, $c, $d) {
    $x3_0 = ex_ext($d, 0, 0);
    $x1_35 = ex_ext($a, 35, 35);
    $x0_35 = ex_ext($b, 35, 35);
    $x1_49 = ex_ext($a, 49, 49);
    $x0_49 = ex_ext($b, 49, 49);
    $x1_29 = ex_ext($a, 29, 29);
    $x0_29 = ex_ext($b, 29, 29);
    $x1_30 = ex_ext($a, 30, 30);
    $x0_30 = ex_ext($b, 30, 30);
    $x1_18 = ex_ext($a, 18, 18);
    $x0_18 = ex_ext($b, 18, 18);
    $x1_55 = ex_ext($a, 55, 55);
    $x0_55 = ex_ext($b, 55, 55);
    $x1_42 = ex_ext($a, 42, 42);
    $x0_42 = ex_ext($b, 42, 42);
    $x1_3 = ex_ext($a, 3, 3);
    $x0_3 = ex_ext($b, 3, 3);
    $x1_0 = ex_ext($a, 0, 0);
    $x0_0 = ex_ext($b, 0, 0);
    $x1_47 = ex_ext($a, 47, 47);
    $x0_47 = ex_ext($b, 47, 47);
    $x1_7 = ex_ext($a, 7, 7);
    $x0_7 = ex_ext($b, 7, 7);
    $x1_44 = ex_ext($a, 44, 44);
    $x0_44 = ex_ext($b, 44, 44);
    $x1_10 = ex_ext($a, 10, 10);
    $x0_10 = ex_ext($b, 10, 10);
    $x1_23 = ex_ext($a, 23, 23);
    $x0_23 = ex_ext($b, 23, 23);
    $x1_8 = ex_ext($a, 8, 8);
    $x0_8 = ex_ext($b, 8, 8);
    $x1_4 = ex_ext($a, 4, 4);
    $x0_4 = ex_ext($b, 4, 4);
    $x1_15 = ex_ext($a, 15, 15);
    $x0_15 = ex_ext($b, 15, 15);
    $x1_54 = ex_ext($a, 54, 54);
    $x0_54 = ex_ext($b, 54, 54);
    $x1_1 = ex_ext($a, 1, 1);
    $x0_1 = ex_ext($b, 1, 1);
    $x1_46 = ex_ext($a, 46, 46);
    $x0_46 = ex_ext($b, 46, 46);
    $x1_21 = ex_ext($a, 21, 21);
    $x0_21 = ex_ext($b, 21, 21);
    $x1_13 = ex_ext($a, 13, 13);
    $x0_13 = ex_ext($b, 13, 13);
    $x1_53 = ex_ext($a, 53, 53);
    $x0_53 = ex_ext($b, 53, 53);
    $x1_57 = ex_ext($a, 57, 57);
    $x0_57 = ex_ext($b, 57, 57);
    $x1_60 = ex_ext($a, 60, 60);
    $x0_60 = ex_ext($b, 60, 60);
    $x1_33 = ex_ext($a, 33, 33);
    $x0_33 = ex_ext($b, 33, 33);
    $x1_12 = ex_ext($a, 12, 12);
    $x0_12 = ex_ext($b, 12, 12);
    $x1_63 = ex_ext($a, 63, 63);
    $x0_63 = ex_ext($b, 63, 63);
    $x1_28 = ex_ext($a, 28, 28);
    $x0_28 = ex_ext($b, 28, 28);
    $x1_50 = ex_ext($a, 50, 50);
    $x0_50 = ex_ext($b, 50, 50);
    $x1_58 = ex_ext($a, 58, 58);
    $x0_58 = ex_ext($b, 58, 58);
    $x1_6 = ex_ext($a, 6, 6);
    $x0_6 = ex_ext($b, 6, 6);
    $x1_22 = ex_ext($a, 22, 22);
    $x0_22 = ex_ext($b, 22, 22);
    $x1_36 = ex_ext($a, 36, 36);
    $x0_36 = ex_ext($b, 36, 36);
    $x1_56 = ex_ext($a, 56, 56);
    $x0_56 = ex_ext($b, 56, 56);
    $x1_62 = ex_ext($a, 62, 62);
    $x0_62 = ex_ext($b, 62, 62);
    $x1_31 = ex_ext($a, 31, 31);
    $x0_31 = ex_ext($b, 31, 31);
    $x1_39 = ex_ext($a, 39, 39);
    $x0_39 = ex_ext($b, 39, 39);
    $x1_27 = ex_ext($a, 27, 27);
    $x0_27 = ex_ext($b, 27, 27);
    $x1_9 = ex_ext($a, 9, 9);
    $x0_9 = ex_ext($b, 9, 9);
    $x1_45 = ex_ext($a, 45, 45);
    $x0_45 = ex_ext($b, 45, 45);
    $x1_19 = ex_ext($a, 19, 19);
    $x0_19 = ex_ext($b, 19, 19);
    $x1_32 = ex_ext($a, 32, 32);
    $x0_32 = ex_ext($b, 32, 32);
    $x1_26 = ex_ext($a, 26, 26);
    $x0_26 = ex_ext($b, 26, 26);
    $x1_34 = ex_ext($a, 34, 34);
    $x0_34 = ex_ext($b, 34, 34);
    $x1_52 = ex_ext($a, 52, 52);
    $x0_52 = ex_ext($b, 52, 52);
    $x1_61 = ex_ext($a, 61, 61);
    $x0_61 = ex_ext($b, 61, 61);
    $x1_40 = ex_ext($a, 40, 40);
    $x0_40 = ex_ext($b, 40, 40);
    $x1_14 = ex_ext($a, 14, 14);
    $x0_14 = ex_ext($b, 14, 14);
    $x1_20 = ex_ext($a, 20, 20);
    $x0_20 = ex_ext($b, 20, 20);
    $x1_38 = ex_ext($a, 38, 38);
    $x0_38 = ex_ext($b, 38, 38);
    $x1_43 = ex_ext($a, 43, 43);
    $x0_43 = ex_ext($b, 43, 43);
    $x1_37 = ex_ext($a, 37, 37);
    $x0_37 = ex_ext($b, 37, 37);
    $x1_41 = ex_ext($a, 41, 41);
    $x0_41 = ex_ext($b, 41, 41);
    $x1_2 = ex_ext($a, 2, 2);
    $x0_2 = ex_ext($b, 2, 2);
    $x1_24 = ex_ext($a, 24, 24);
    $x0_24 = ex_ext($b, 24, 24);
    $x1_51 = ex_ext($a, 51, 51);
    $x0_51 = ex_ext($b, 51, 51);
    $x1_5 = ex_ext($a, 5, 5);
    $x0_5 = ex_ext($b, 5, 5);
    $x1_17 = ex_ext($a, 17, 17);
    $x0_17 = ex_ext($b, 17, 17);
    $x1_25 = ex_ext($a, 25, 25);
    $x0_25 = ex_ext($b, 25, 25);
    $x1_59 = ex_ext($a, 59, 59);
    $x0_59 = ex_ext($b, 59, 59);
    $x1_16 = ex_ext($a, 16, 16);
    $x0_16 = ex_ext($b, 16, 16);
    $x1_48 = ex_ext($a, 48, 48);
    $x0_48 = ex_ext($b, 48, 48);
    $x1_11 = ex_ext($a, 11, 11);
    $x0_11 = ex_ext($b, 11, 11);
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
    $x3_32 = ex_ext($d, 32, 32);
    $x2_32 = ex_ext($c, 32, 32);
    $x3_33 = ex_ext($d, 33, 33);
    $x2_33 = ex_ext($c, 33, 33);
    $x3_34 = ex_ext($d, 34, 34);
    $x2_34 = ex_ext($c, 34, 34);
    $x3_35 = ex_ext($d, 35, 35);
    $x2_35 = ex_ext($c, 35, 35);
    $x3_36 = ex_ext($d, 36, 36);
    $x2_36 = ex_ext($c, 36, 36);
    $x3_37 = ex_ext($d, 37, 37);
    $x2_37 = ex_ext($c, 37, 37);
    $x3_38 = ex_ext($d, 38, 38);
    $x2_38 = ex_ext($c, 38, 38);
    $x3_39 = ex_ext($d, 39, 39);
    $x2_39 = ex_ext($c, 39, 39);
    $x3_40 = ex_ext($d, 40, 40);
    $x2_40 = ex_ext($c, 40, 40);
    $x3_41 = ex_ext($d, 41, 41);
    $x2_41 = ex_ext($c, 41, 41);
    $x3_42 = ex_ext($d, 42, 42);
    $x2_42 = ex_ext($c, 42, 42);
    $x3_43 = ex_ext($d, 43, 43);
    $x2_43 = ex_ext($c, 43, 43);
    $x3_44 = ex_ext($d, 44, 44);
    $x2_44 = ex_ext($c, 44, 44);
    $x3_45 = ex_ext($d, 45, 45);
    $x2_45 = ex_ext($c, 45, 45);
    $x3_46 = ex_ext($d, 46, 46);
    $x2_46 = ex_ext($c, 46, 46);
    $x3_47 = ex_ext($d, 47, 47);
    $x2_47 = ex_ext($c, 47, 47);
    $x3_48 = ex_ext($d, 48, 48);
    $x2_48 = ex_ext($c, 48, 48);
    $x3_49 = ex_ext($d, 49, 49);
    $x2_49 = ex_ext($c, 49, 49);
    $x3_50 = ex_ext($d, 50, 50);
    $x2_50 = ex_ext($c, 50, 50);
    $x3_51 = ex_ext($d, 51, 51);
    $x2_51 = ex_ext($c, 51, 51);
    $x3_52 = ex_ext($d, 52, 52);
    $x2_52 = ex_ext($c, 52, 52);
    $x3_53 = ex_ext($d, 53, 53);
    $x2_53 = ex_ext($c, 53, 53);
    $x3_54 = ex_ext($d, 54, 54);
    $x2_54 = ex_ext($c, 54, 54);
    $x3_55 = ex_ext($d, 55, 55);
    $x2_55 = ex_ext($c, 55, 55);
    $x3_56 = ex_ext($d, 56, 56);
    $x2_56 = ex_ext($c, 56, 56);
    $x3_57 = ex_ext($d, 57, 57);
    $x2_57 = ex_ext($c, 57, 57);
    $x3_58 = ex_ext($d, 58, 58);
    $x2_58 = ex_ext($c, 58, 58);
    $x3_59 = ex_ext($d, 59, 59);
    $x2_59 = ex_ext($c, 59, 59);
    $x3_60 = ex_ext($d, 60, 60);
    $x2_60 = ex_ext($c, 60, 60);
    $x3_61 = ex_ext($d, 61, 61);
    $x2_61 = ex_ext($c, 61, 61);
    $x3_62 = ex_ext($d, 62, 62);
    $x2_62 = ex_ext($c, 62, 62);
    $x3_63 = ex_ext($d, 63, 63);
    $x2_63 = ex_ext($c, 63, 63);
    $g0 = ($x1_35 ^ 1);
    $g1 = ($x0_35 ^ 1);
    $g2 = ($g1 | $g0);
    $g3 = ($g2 ^ 1);
    $g4 = ($x1_49 ^ 1);
    $g5 = ($x0_49 ^ 1);
    $g6 = ($g5 | $g4);
    $g7 = ($g6 ^ 1);
    $g8 = ($x1_29 ^ 1);
    $g9 = ($x0_29 ^ 1);
    $g10 = ($g9 | $g8);
    $g11 = ($g10 ^ 1);
    $g12 = ($x1_30 ^ 1);
    $g13 = ($x0_30 ^ 1);
    $g14 = ($g13 | $g12);
    $g15 = ($g14 ^ 1);
    $g16 = ($x1_18 ^ 1);
    $g17 = ($x0_18 ^ 1);
    $g18 = ($g17 | $g16);
    $g19 = ($g18 ^ 1);
    $g20 = ($x1_55 ^ 1);
    $g21 = ($x0_55 ^ 1);
    $g22 = ($g21 | $g20);
    $g23 = ($g22 ^ 1);
    $g24 = ($x1_42 ^ 1);
    $g25 = ($x0_42 ^ 1);
    $g26 = ($g25 | $g24);
    $g27 = ($g26 ^ 1);
    $g28 = ($x1_3 ^ 1);
    $g29 = ($x0_3 ^ 1);
    $g30 = ($g29 | $g28);
    $g31 = ($g30 ^ 1);
    $g32 = ($x1_0 ^ 1);
    $g33 = ($x0_0 ^ 1);
    $g34 = ($g33 | $g32);
    $g35 = ($g34 ^ 1);
    $g36 = ($x1_47 ^ 1);
    $g37 = ($x0_47 ^ 1);
    $g38 = ($g37 | $g36);
    $g39 = ($g38 ^ 1);
    $g40 = ($x1_7 ^ 1);
    $g41 = ($x0_7 ^ 1);
    $g42 = ($g41 | $g40);
    $g43 = ($g42 ^ 1);
    $g44 = ($x1_44 ^ 1);
    $g45 = ($x0_44 ^ 1);
    $g46 = ($g45 | $g44);
    $g47 = ($g46 ^ 1);
    $g48 = ($x1_10 ^ 1);
    $g49 = ($x0_10 ^ 1);
    $g50 = ($g49 | $g48);
    $g51 = ($g50 ^ 1);
    $g52 = ($x1_23 ^ 1);
    $g53 = ($x0_23 ^ 1);
    $g54 = ($g53 | $g52);
    $g55 = ($g54 ^ 1);
    $g56 = ($x1_8 ^ 1);
    $g57 = ($x0_8 ^ 1);
    $g58 = ($g57 | $g56);
    $g59 = ($g58 ^ 1);
    $g60 = ($x1_4 ^ 1);
    $g61 = ($x0_4 ^ 1);
    $g62 = ($g61 | $g60);
    $g63 = ($g62 ^ 1);
    $g64 = ($x1_15 ^ 1);
    $g65 = ($x0_15 ^ 1);
    $g66 = ($g65 | $g64);
    $g67 = ($g66 ^ 1);
    $g68 = ($x1_54 ^ 1);
    $g69 = ($x0_54 ^ 1);
    $g70 = ($g69 | $g68);
    $g71 = ($g70 ^ 1);
    $g72 = ($x1_1 ^ 1);
    $g73 = ($x0_1 ^ 1);
    $g74 = ($g73 | $g72);
    $g75 = ($g74 ^ 1);
    $g76 = ($x1_46 ^ 1);
    $g77 = ($x0_46 ^ 1);
    $g78 = ($g77 | $g76);
    $g79 = ($g78 ^ 1);
    $g80 = ($x1_21 ^ 1);
    $g81 = ($x0_21 ^ 1);
    $g82 = ($g81 | $g80);
    $g83 = ($g82 ^ 1);
    $g84 = ($x1_13 ^ 1);
    $g85 = ($x0_13 ^ 1);
    $g86 = ($g85 | $g84);
    $g87 = ($g86 ^ 1);
    $g88 = ($x1_53 ^ 1);
    $g89 = ($x0_53 ^ 1);
    $g90 = ($g89 | $g88);
    $g91 = ($g90 ^ 1);
    $g92 = ($x1_57 ^ 1);
    $g93 = ($x0_57 ^ 1);
    $g94 = ($g93 | $g92);
    $g95 = ($g94 ^ 1);
    $g96 = ($x1_60 ^ 1);
    $g97 = ($x0_60 ^ 1);
    $g98 = ($g97 | $g96);
    $g99 = ($g98 ^ 1);
    $g100 = ($x1_33 ^ 1);
    $g101 = ($x0_33 ^ 1);
    $g102 = ($g101 | $g100);
    $g103 = ($g102 ^ 1);
    $g104 = ($x1_12 ^ 1);
    $g105 = ($x0_12 ^ 1);
    $g106 = ($g105 | $g104);
    $g107 = ($g106 ^ 1);
    $g108 = ($x1_63 ^ 1);
    $g109 = ($x0_63 ^ 1);
    $g110 = ($g109 | $g108);
    $g111 = ($g110 ^ 1);
    $g112 = ($x1_28 ^ 1);
    $g113 = ($x0_28 ^ 1);
    $g114 = ($g113 | $g112);
    $g115 = ($g114 ^ 1);
    $g116 = ($x1_50 ^ 1);
    $g117 = ($x0_50 ^ 1);
    $g118 = ($g117 | $g116);
    $g119 = ($g118 ^ 1);
    $g120 = ($x1_58 ^ 1);
    $g121 = ($x0_58 ^ 1);
    $g122 = ($g121 | $g120);
    $g123 = ($g122 ^ 1);
    $g124 = ($x1_6 ^ 1);
    $g125 = ($x0_6 ^ 1);
    $g126 = ($g125 | $g124);
    $g127 = ($g126 ^ 1);
    $g128 = ($x1_22 ^ 1);
    $g129 = ($x0_22 ^ 1);
    $g130 = ($g129 | $g128);
    $g131 = ($g130 ^ 1);
    $g132 = ($x1_36 ^ 1);
    $g133 = ($x0_36 ^ 1);
    $g134 = ($g133 | $g132);
    $g135 = ($g134 ^ 1);
    $g136 = ($x1_56 ^ 1);
    $g137 = ($x0_56 ^ 1);
    $g138 = ($g137 | $g136);
    $g139 = ($g138 ^ 1);
    $g140 = ($x1_62 ^ 1);
    $g141 = ($x0_62 ^ 1);
    $g142 = ($g141 | $g140);
    $g143 = ($g142 ^ 1);
    $g144 = ($x1_31 ^ 1);
    $g145 = ($x0_31 ^ 1);
    $g146 = ($g145 | $g144);
    $g147 = ($g146 ^ 1);
    $g148 = ($x1_39 ^ 1);
    $g149 = ($x0_39 ^ 1);
    $g150 = ($g149 | $g148);
    $g151 = ($g150 ^ 1);
    $g152 = ($x1_27 ^ 1);
    $g153 = ($x0_27 ^ 1);
    $g154 = ($g153 | $g152);
    $g155 = ($g154 ^ 1);
    $g156 = ($x1_9 ^ 1);
    $g157 = ($x0_9 ^ 1);
    $g158 = ($g157 | $g156);
    $g159 = ($g158 ^ 1);
    $g160 = ($x1_45 ^ 1);
    $g161 = ($x0_45 ^ 1);
    $g162 = ($g161 | $g160);
    $g163 = ($g162 ^ 1);
    $g164 = ($x1_19 ^ 1);
    $g165 = ($x0_19 ^ 1);
    $g166 = ($g165 | $g164);
    $g167 = ($g166 ^ 1);
    $g168 = ($x1_32 ^ 1);
    $g169 = ($x0_32 ^ 1);
    $g170 = ($g169 | $g168);
    $g171 = ($g170 ^ 1);
    $g172 = ($x1_26 ^ 1);
    $g173 = ($x0_26 ^ 1);
    $g174 = ($g173 | $g172);
    $g175 = ($g174 ^ 1);
    $g176 = ($x1_34 ^ 1);
    $g177 = ($x0_34 ^ 1);
    $g178 = ($g177 | $g176);
    $g179 = ($g178 ^ 1);
    $g180 = ($x1_52 ^ 1);
    $g181 = ($x0_52 ^ 1);
    $g182 = ($g181 | $g180);
    $g183 = ($g182 ^ 1);
    $g184 = ($x1_61 ^ 1);
    $g185 = ($x0_61 ^ 1);
    $g186 = ($g185 | $g184);
    $g187 = ($g186 ^ 1);
    $g188 = ($x1_40 ^ 1);
    $g189 = ($x0_40 ^ 1);
    $g190 = ($g189 | $g188);
    $g191 = ($g190 ^ 1);
    $g192 = ($x1_14 ^ 1);
    $g193 = ($x0_14 ^ 1);
    $g194 = ($g193 | $g192);
    $g195 = ($g194 ^ 1);
    $g196 = ($x1_20 ^ 1);
    $g197 = ($x0_20 ^ 1);
    $g198 = ($g197 | $g196);
    $g199 = ($g198 ^ 1);
    $g200 = ($x1_38 ^ 1);
    $g201 = ($x0_38 ^ 1);
    $g202 = ($g201 | $g200);
    $g203 = ($g202 ^ 1);
    $g204 = ($x1_43 ^ 1);
    $g205 = ($x0_43 ^ 1);
    $g206 = ($g205 | $g204);
    $g207 = ($g206 ^ 1);
    $g208 = ($x1_37 ^ 1);
    $g209 = ($x0_37 ^ 1);
    $g210 = ($g209 | $g208);
    $g211 = ($g210 ^ 1);
    $g212 = ($x1_41 ^ 1);
    $g213 = ($x0_41 ^ 1);
    $g214 = ($g213 | $g212);
    $g215 = ($g214 ^ 1);
    $g216 = ($x1_2 ^ 1);
    $g217 = ($x0_2 ^ 1);
    $g218 = ($g217 | $g216);
    $g219 = ($g218 ^ 1);
    $g220 = ($x1_24 ^ 1);
    $g221 = ($x0_24 ^ 1);
    $g222 = ($g221 | $g220);
    $g223 = ($g222 ^ 1);
    $g224 = ($x1_51 ^ 1);
    $g225 = ($x0_51 ^ 1);
    $g226 = ($g225 | $g224);
    $g227 = ($g226 ^ 1);
    $g228 = ($x1_5 ^ 1);
    $g229 = ($x0_5 ^ 1);
    $g230 = ($g229 | $g228);
    $g231 = ($g230 ^ 1);
    $g232 = ($x1_17 ^ 1);
    $g233 = ($x0_17 ^ 1);
    $g234 = ($g233 | $g232);
    $g235 = ($g234 ^ 1);
    $g236 = ($x1_25 ^ 1);
    $g237 = ($x0_25 ^ 1);
    $g238 = ($g237 | $g236);
    $g239 = ($g238 ^ 1);
    $g240 = ($x1_59 ^ 1);
    $g241 = ($x0_59 ^ 1);
    $g242 = ($g241 | $g240);
    $g243 = ($g242 ^ 1);
    $g244 = ($x1_16 ^ 1);
    $g245 = ($x0_16 ^ 1);
    $g246 = ($g245 | $g244);
    $g247 = ($g246 ^ 1);
    $g248 = ($x1_48 ^ 1);
    $g249 = ($x0_48 ^ 1);
    $g250 = ($g249 | $g248);
    $g251 = ($g250 ^ 1);
    $g252 = ($x1_11 ^ 1);
    $g253 = ($x0_11 ^ 1);
    $g254 = ($g253 | $g252);
    $g255 = ($g254 ^ 1);
    $g256 = ($g255 | $g251);
    $g257 = ($g256 | $g247);
    $g258 = ($g257 | $g243);
    $g259 = ($g258 | $g239);
    $g260 = ($g259 | $g235);
    $g261 = ($g260 | $g231);
    $g262 = ($g261 | $g227);
    $g263 = ($g262 | $g223);
    $g264 = ($g263 | $g219);
    $g265 = ($g264 | $g215);
    $g266 = ($g265 | $g211);
    $g267 = ($g266 | $g207);
    $g268 = ($g267 | $g203);
    $g269 = ($g268 | $g199);
    $g270 = ($g269 | $g195);
    $g271 = ($g270 | $g191);
    $g272 = ($g271 | $g187);
    $g273 = ($g272 | $g183);
    $g274 = ($g273 | $g179);
    $g275 = ($g274 | $g175);
    $g276 = ($g275 | $g171);
    $g277 = ($g276 | $g167);
    $g278 = ($g277 | $g163);
    $g279 = ($g278 | $g159);
    $g280 = ($g279 | $g155);
    $g281 = ($g280 | $g151);
    $g282 = ($g281 | $g147);
    $g283 = ($g282 | $g143);
    $g284 = ($g283 | $g139);
    $g285 = ($g284 | $g135);
    $g286 = ($g285 | $g131);
    $g287 = ($g286 | $g127);
    $g288 = ($g287 | $g123);
    $g289 = ($g288 | $g119);
    $g290 = ($g289 | $g115);
    $g291 = ($g290 | $g111);
    $g292 = ($g291 | $g107);
    $g293 = ($g292 | $g103);
    $g294 = ($g293 | $g99);
    $g295 = ($g294 | $g95);
    $g296 = ($g295 | $g91);
    $g297 = ($g296 | $g87);
    $g298 = ($g297 | $g83);
    $g299 = ($g298 | $g79);
    $g300 = ($g299 | $g75);
    $g301 = ($g300 | $g71);
    $g302 = ($g301 | $g67);
    $g303 = ($g302 | $g63);
    $g304 = ($g303 | $g59);
    $g305 = ($g304 | $g55);
    $g306 = ($g305 | $g51);
    $g307 = ($g306 | $g47);
    $g308 = ($g307 | $g43);
    $g309 = ($g308 | $g39);
    $g310 = ($g309 | $g35);
    $g311 = ($g310 | $g31);
    $g312 = ($g311 | $g27);
    $g313 = ($g312 | $g23);
    $g314 = ($g313 | $g19);
    $g315 = ($g314 | $g15);
    $g316 = ($g315 | $g11);
    $g317 = ($g316 | $g7);
    $g318 = ($g317 | $g3);
    $g319 = ($g318 ^ 1);
    $g320 = ($g319 ^ 1);
    $g321 = ($g320 & $x3_0);
    $g322 = ($g319 & $x2_0);
    $g323 = ($g322 | $g321);
    $g324 = ($g320 & $x3_1);
    $g325 = ($g319 & $x2_1);
    $g326 = ($g325 | $g324);
    $g327 = ($g320 & $x3_2);
    $g328 = ($g319 & $x2_2);
    $g329 = ($g328 | $g327);
    $g330 = ($g320 & $x3_3);
    $g331 = ($g319 & $x2_3);
    $g332 = ($g331 | $g330);
    $g333 = ($g320 & $x3_4);
    $g334 = ($g319 & $x2_4);
    $g335 = ($g334 | $g333);
    $g336 = ($g320 & $x3_5);
    $g337 = ($g319 & $x2_5);
    $g338 = ($g337 | $g336);
    $g339 = ($g320 & $x3_6);
    $g340 = ($g319 & $x2_6);
    $g341 = ($g340 | $g339);
    $g342 = ($g320 & $x3_7);
    $g343 = ($g319 & $x2_7);
    $g344 = ($g343 | $g342);
    $g345 = ($g320 & $x3_8);
    $g346 = ($g319 & $x2_8);
    $g347 = ($g346 | $g345);
    $g348 = ($g320 & $x3_9);
    $g349 = ($g319 & $x2_9);
    $g350 = ($g349 | $g348);
    $g351 = ($g320 & $x3_10);
    $g352 = ($g319 & $x2_10);
    $g353 = ($g352 | $g351);
    $g354 = ($g320 & $x3_11);
    $g355 = ($g319 & $x2_11);
    $g356 = ($g355 | $g354);
    $g357 = ($g320 & $x3_12);
    $g358 = ($g319 & $x2_12);
    $g359 = ($g358 | $g357);
    $g360 = ($g320 & $x3_13);
    $g361 = ($g319 & $x2_13);
    $g362 = ($g361 | $g360);
    $g363 = ($g320 & $x3_14);
    $g364 = ($g319 & $x2_14);
    $g365 = ($g364 | $g363);
    $g366 = ($g320 & $x3_15);
    $g367 = ($g319 & $x2_15);
    $g368 = ($g367 | $g366);
    $g369 = ($g320 & $x3_16);
    $g370 = ($g319 & $x2_16);
    $g371 = ($g370 | $g369);
    $g372 = ($g320 & $x3_17);
    $g373 = ($g319 & $x2_17);
    $g374 = ($g373 | $g372);
    $g375 = ($g320 & $x3_18);
    $g376 = ($g319 & $x2_18);
    $g377 = ($g376 | $g375);
    $g378 = ($g320 & $x3_19);
    $g379 = ($g319 & $x2_19);
    $g380 = ($g379 | $g378);
    $g381 = ($g320 & $x3_20);
    $g382 = ($g319 & $x2_20);
    $g383 = ($g382 | $g381);
    $g384 = ($g320 & $x3_21);
    $g385 = ($g319 & $x2_21);
    $g386 = ($g385 | $g384);
    $g387 = ($g320 & $x3_22);
    $g388 = ($g319 & $x2_22);
    $g389 = ($g388 | $g387);
    $g390 = ($g320 & $x3_23);
    $g391 = ($g319 & $x2_23);
    $g392 = ($g391 | $g390);
    $g393 = ($g320 & $x3_24);
    $g394 = ($g319 & $x2_24);
    $g395 = ($g394 | $g393);
    $g396 = ($g320 & $x3_25);
    $g397 = ($g319 & $x2_25);
    $g398 = ($g397 | $g396);
    $g399 = ($g320 & $x3_26);
    $g400 = ($g319 & $x2_26);
    $g401 = ($g400 | $g399);
    $g402 = ($g320 & $x3_27);
    $g403 = ($g319 & $x2_27);
    $g404 = ($g403 | $g402);
    $g405 = ($g320 & $x3_28);
    $g406 = ($g319 & $x2_28);
    $g407 = ($g406 | $g405);
    $g408 = ($g320 & $x3_29);
    $g409 = ($g319 & $x2_29);
    $g410 = ($g409 | $g408);
    $g411 = ($g320 & $x3_30);
    $g412 = ($g319 & $x2_30);
    $g413 = ($g412 | $g411);
    $g414 = ($g320 & $x3_31);
    $g415 = ($g319 & $x2_31);
    $g416 = ($g415 | $g414);
    $g417 = ($g320 & $x3_32);
    $g418 = ($g319 & $x2_32);
    $g419 = ($g418 | $g417);
    $g420 = ($g320 & $x3_33);
    $g421 = ($g319 & $x2_33);
    $g422 = ($g421 | $g420);
    $g423 = ($g320 & $x3_34);
    $g424 = ($g319 & $x2_34);
    $g425 = ($g424 | $g423);
    $g426 = ($g320 & $x3_35);
    $g427 = ($g319 & $x2_35);
    $g428 = ($g427 | $g426);
    $g429 = ($g320 & $x3_36);
    $g430 = ($g319 & $x2_36);
    $g431 = ($g430 | $g429);
    $g432 = ($g320 & $x3_37);
    $g433 = ($g319 & $x2_37);
    $g434 = ($g433 | $g432);
    $g435 = ($g320 & $x3_38);
    $g436 = ($g319 & $x2_38);
    $g437 = ($g436 | $g435);
    $g438 = ($g320 & $x3_39);
    $g439 = ($g319 & $x2_39);
    $g440 = ($g439 | $g438);
    $g441 = ($g320 & $x3_40);
    $g442 = ($g319 & $x2_40);
    $g443 = ($g442 | $g441);
    $g444 = ($g320 & $x3_41);
    $g445 = ($g319 & $x2_41);
    $g446 = ($g445 | $g444);
    $g447 = ($g320 & $x3_42);
    $g448 = ($g319 & $x2_42);
    $g449 = ($g448 | $g447);
    $g450 = ($g320 & $x3_43);
    $g451 = ($g319 & $x2_43);
    $g452 = ($g451 | $g450);
    $g453 = ($g320 & $x3_44);
    $g454 = ($g319 & $x2_44);
    $g455 = ($g454 | $g453);
    $g456 = ($g320 & $x3_45);
    $g457 = ($g319 & $x2_45);
    $g458 = ($g457 | $g456);
    $g459 = ($g320 & $x3_46);
    $g460 = ($g319 & $x2_46);
    $g461 = ($g460 | $g459);
    $g462 = ($g320 & $x3_47);
    $g463 = ($g319 & $x2_47);
    $g464 = ($g463 | $g462);
    $g465 = ($g320 & $x3_48);
    $g466 = ($g319 & $x2_48);
    $g467 = ($g466 | $g465);
    $g468 = ($g320 & $x3_49);
    $g469 = ($g319 & $x2_49);
    $g470 = ($g469 | $g468);
    $g471 = ($g320 & $x3_50);
    $g472 = ($g319 & $x2_50);
    $g473 = ($g472 | $g471);
    $g474 = ($g320 & $x3_51);
    $g475 = ($g319 & $x2_51);
    $g476 = ($g475 | $g474);
    $g477 = ($g320 & $x3_52);
    $g478 = ($g319 & $x2_52);
    $g479 = ($g478 | $g477);
    $g480 = ($g320 & $x3_53);
    $g481 = ($g319 & $x2_53);
    $g482 = ($g481 | $g480);
    $g483 = ($g320 & $x3_54);
    $g484 = ($g319 & $x2_54);
    $g485 = ($g484 | $g483);
    $g486 = ($g320 & $x3_55);
    $g487 = ($g319 & $x2_55);
    $g488 = ($g487 | $g486);
    $g489 = ($g320 & $x3_56);
    $g490 = ($g319 & $x2_56);
    $g491 = ($g490 | $g489);
    $g492 = ($g320 & $x3_57);
    $g493 = ($g319 & $x2_57);
    $g494 = ($g493 | $g492);
    $g495 = ($g320 & $x3_58);
    $g496 = ($g319 & $x2_58);
    $g497 = ($g496 | $g495);
    $g498 = ($g320 & $x3_59);
    $g499 = ($g319 & $x2_59);
    $g500 = ($g499 | $g498);
    $g501 = ($g320 & $x3_60);
    $g502 = ($g319 & $x2_60);
    $g503 = ($g502 | $g501);
    $g504 = ($g320 & $x3_61);
    $g505 = ($g319 & $x2_61);
    $g506 = ($g505 | $g504);
    $g507 = ($g320 & $x3_62);
    $g508 = ($g319 & $x2_62);
    $g509 = ($g508 | $g507);
    $g510 = ($g320 & $x3_63);
    $g511 = ($g319 & $x2_63);
    $g512 = ($g511 | $g510);
    $w0 = $g512;
    $w1 = ex_cat($w0, $g509, 1);
    $w2 = ex_cat($w1, $g506, 1);
    $w3 = ex_cat($w2, $g503, 1);
    $w4 = ex_cat($w3, $g500, 1);
    $w5 = ex_cat($w4, $g497, 1);
    $w6 = ex_cat($w5, $g494, 1);
    $w7 = ex_cat($w6, $g491, 1);
    $w8 = ex_cat($w7, $g488, 1);
    $w9 = ex_cat($w8, $g485, 1);
    $w10 = ex_cat($w9, $g482, 1);
    $w11 = ex_cat($w10, $g479, 1);
    $w12 = ex_cat($w11, $g476, 1);
    $w13 = ex_cat($w12, $g473, 1);
    $w14 = ex_cat($w13, $g470, 1);
    $w15 = ex_cat($w14, $g467, 1);
    $w16 = ex_cat($w15, $g464, 1);
    $w17 = ex_cat($w16, $g461, 1);
    $w18 = ex_cat($w17, $g458, 1);
    $w19 = ex_cat($w18, $g455, 1);
    $w20 = ex_cat($w19, $g452, 1);
    $w21 = ex_cat($w20, $g449, 1);
    $w22 = ex_cat($w21, $g446, 1);
    $w23 = ex_cat($w22, $g443, 1);
    $w24 = ex_cat($w23, $g440, 1);
    $w25 = ex_cat($w24, $g437, 1);
    $w26 = ex_cat($w25, $g434, 1);
    $w27 = ex_cat($w26, $g431, 1);
    $w28 = ex_cat($w27, $g428, 1);
    $w29 = ex_cat($w28, $g425, 1);
    $w30 = ex_cat($w29, $g422, 1);
    $w31 = ex_cat($w30, $g419, 1);
    $w32 = ex_cat($w31, $g416, 1);
    $w33 = ex_cat($w32, $g413, 1);
    $w34 = ex_cat($w33, $g410, 1);
    $w35 = ex_cat($w34, $g407, 1);
    $w36 = ex_cat($w35, $g404, 1);
    $w37 = ex_cat($w36, $g401, 1);
    $w38 = ex_cat($w37, $g398, 1);
    $w39 = ex_cat($w38, $g395, 1);
    $w40 = ex_cat($w39, $g392, 1);
    $w41 = ex_cat($w40, $g389, 1);
    $w42 = ex_cat($w41, $g386, 1);
    $w43 = ex_cat($w42, $g383, 1);
    $w44 = ex_cat($w43, $g380, 1);
    $w45 = ex_cat($w44, $g377, 1);
    $w46 = ex_cat($w45, $g374, 1);
    $w47 = ex_cat($w46, $g371, 1);
    $w48 = ex_cat($w47, $g368, 1);
    $w49 = ex_cat($w48, $g365, 1);
    $w50 = ex_cat($w49, $g362, 1);
    $w51 = ex_cat($w50, $g359, 1);
    $w52 = ex_cat($w51, $g356, 1);
    $w53 = ex_cat($w52, $g353, 1);
    $w54 = ex_cat($w53, $g350, 1);
    $w55 = ex_cat($w54, $g347, 1);
    $w56 = ex_cat($w55, $g344, 1);
    $w57 = ex_cat($w56, $g341, 1);
    $w58 = ex_cat($w57, $g338, 1);
    $w59 = ex_cat($w58, $g335, 1);
    $w60 = ex_cat($w59, $g332, 1);
    $w61 = ex_cat($w60, $g329, 1);
    $w62 = ex_cat($w61, $g326, 1);
    $w63 = ex_cat($w62, $g323, 1);
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
        $answer = emu_cmove_gpr_gpr_64__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
