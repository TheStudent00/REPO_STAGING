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
// one named local per gate, over the term of cmovs_gpr_gpr_64__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
function emu_cmovs_gpr_gpr_64__reg_rdi__php($a, $b, $c, $d) {
    $x3_0 = ex_ext($c, 0, 0);
    $x1_63 = ex_ext($a, 63, 63);
    $x0_63 = ex_ext($b, 63, 63);
    $x2_0 = ex_ext($d, 0, 0);
    $x3_1 = ex_ext($c, 1, 1);
    $x2_1 = ex_ext($d, 1, 1);
    $x3_2 = ex_ext($c, 2, 2);
    $x2_2 = ex_ext($d, 2, 2);
    $x3_3 = ex_ext($c, 3, 3);
    $x2_3 = ex_ext($d, 3, 3);
    $x3_4 = ex_ext($c, 4, 4);
    $x2_4 = ex_ext($d, 4, 4);
    $x3_5 = ex_ext($c, 5, 5);
    $x2_5 = ex_ext($d, 5, 5);
    $x3_6 = ex_ext($c, 6, 6);
    $x2_6 = ex_ext($d, 6, 6);
    $x3_7 = ex_ext($c, 7, 7);
    $x2_7 = ex_ext($d, 7, 7);
    $x3_8 = ex_ext($c, 8, 8);
    $x2_8 = ex_ext($d, 8, 8);
    $x3_9 = ex_ext($c, 9, 9);
    $x2_9 = ex_ext($d, 9, 9);
    $x3_10 = ex_ext($c, 10, 10);
    $x2_10 = ex_ext($d, 10, 10);
    $x3_11 = ex_ext($c, 11, 11);
    $x2_11 = ex_ext($d, 11, 11);
    $x3_12 = ex_ext($c, 12, 12);
    $x2_12 = ex_ext($d, 12, 12);
    $x3_13 = ex_ext($c, 13, 13);
    $x2_13 = ex_ext($d, 13, 13);
    $x3_14 = ex_ext($c, 14, 14);
    $x2_14 = ex_ext($d, 14, 14);
    $x3_15 = ex_ext($c, 15, 15);
    $x2_15 = ex_ext($d, 15, 15);
    $x3_16 = ex_ext($c, 16, 16);
    $x2_16 = ex_ext($d, 16, 16);
    $x3_17 = ex_ext($c, 17, 17);
    $x2_17 = ex_ext($d, 17, 17);
    $x3_18 = ex_ext($c, 18, 18);
    $x2_18 = ex_ext($d, 18, 18);
    $x3_19 = ex_ext($c, 19, 19);
    $x2_19 = ex_ext($d, 19, 19);
    $x3_20 = ex_ext($c, 20, 20);
    $x2_20 = ex_ext($d, 20, 20);
    $x3_21 = ex_ext($c, 21, 21);
    $x2_21 = ex_ext($d, 21, 21);
    $x3_22 = ex_ext($c, 22, 22);
    $x2_22 = ex_ext($d, 22, 22);
    $x3_23 = ex_ext($c, 23, 23);
    $x2_23 = ex_ext($d, 23, 23);
    $x3_24 = ex_ext($c, 24, 24);
    $x2_24 = ex_ext($d, 24, 24);
    $x3_25 = ex_ext($c, 25, 25);
    $x2_25 = ex_ext($d, 25, 25);
    $x3_26 = ex_ext($c, 26, 26);
    $x2_26 = ex_ext($d, 26, 26);
    $x3_27 = ex_ext($c, 27, 27);
    $x2_27 = ex_ext($d, 27, 27);
    $x3_28 = ex_ext($c, 28, 28);
    $x2_28 = ex_ext($d, 28, 28);
    $x3_29 = ex_ext($c, 29, 29);
    $x2_29 = ex_ext($d, 29, 29);
    $x3_30 = ex_ext($c, 30, 30);
    $x2_30 = ex_ext($d, 30, 30);
    $x3_31 = ex_ext($c, 31, 31);
    $x2_31 = ex_ext($d, 31, 31);
    $x3_32 = ex_ext($c, 32, 32);
    $x2_32 = ex_ext($d, 32, 32);
    $x3_33 = ex_ext($c, 33, 33);
    $x2_33 = ex_ext($d, 33, 33);
    $x3_34 = ex_ext($c, 34, 34);
    $x2_34 = ex_ext($d, 34, 34);
    $x3_35 = ex_ext($c, 35, 35);
    $x2_35 = ex_ext($d, 35, 35);
    $x3_36 = ex_ext($c, 36, 36);
    $x2_36 = ex_ext($d, 36, 36);
    $x3_37 = ex_ext($c, 37, 37);
    $x2_37 = ex_ext($d, 37, 37);
    $x3_38 = ex_ext($c, 38, 38);
    $x2_38 = ex_ext($d, 38, 38);
    $x3_39 = ex_ext($c, 39, 39);
    $x2_39 = ex_ext($d, 39, 39);
    $x3_40 = ex_ext($c, 40, 40);
    $x2_40 = ex_ext($d, 40, 40);
    $x3_41 = ex_ext($c, 41, 41);
    $x2_41 = ex_ext($d, 41, 41);
    $x3_42 = ex_ext($c, 42, 42);
    $x2_42 = ex_ext($d, 42, 42);
    $x3_43 = ex_ext($c, 43, 43);
    $x2_43 = ex_ext($d, 43, 43);
    $x3_44 = ex_ext($c, 44, 44);
    $x2_44 = ex_ext($d, 44, 44);
    $x3_45 = ex_ext($c, 45, 45);
    $x2_45 = ex_ext($d, 45, 45);
    $x3_46 = ex_ext($c, 46, 46);
    $x2_46 = ex_ext($d, 46, 46);
    $x3_47 = ex_ext($c, 47, 47);
    $x2_47 = ex_ext($d, 47, 47);
    $x3_48 = ex_ext($c, 48, 48);
    $x2_48 = ex_ext($d, 48, 48);
    $x3_49 = ex_ext($c, 49, 49);
    $x2_49 = ex_ext($d, 49, 49);
    $x3_50 = ex_ext($c, 50, 50);
    $x2_50 = ex_ext($d, 50, 50);
    $x3_51 = ex_ext($c, 51, 51);
    $x2_51 = ex_ext($d, 51, 51);
    $x3_52 = ex_ext($c, 52, 52);
    $x2_52 = ex_ext($d, 52, 52);
    $x3_53 = ex_ext($c, 53, 53);
    $x2_53 = ex_ext($d, 53, 53);
    $x3_54 = ex_ext($c, 54, 54);
    $x2_54 = ex_ext($d, 54, 54);
    $x3_55 = ex_ext($c, 55, 55);
    $x2_55 = ex_ext($d, 55, 55);
    $x3_56 = ex_ext($c, 56, 56);
    $x2_56 = ex_ext($d, 56, 56);
    $x3_57 = ex_ext($c, 57, 57);
    $x2_57 = ex_ext($d, 57, 57);
    $x3_58 = ex_ext($c, 58, 58);
    $x2_58 = ex_ext($d, 58, 58);
    $x3_59 = ex_ext($c, 59, 59);
    $x2_59 = ex_ext($d, 59, 59);
    $x3_60 = ex_ext($c, 60, 60);
    $x2_60 = ex_ext($d, 60, 60);
    $x3_61 = ex_ext($c, 61, 61);
    $x2_61 = ex_ext($d, 61, 61);
    $x3_62 = ex_ext($c, 62, 62);
    $x2_62 = ex_ext($d, 62, 62);
    $x3_63 = ex_ext($c, 63, 63);
    $x2_63 = ex_ext($d, 63, 63);
    $g0 = ($x1_63 ^ 1);
    $g1 = ($x0_63 ^ 1);
    $g2 = ($g1 | $g0);
    $g3 = ($g2 ^ 1);
    $g4 = ($g3 & $x3_0);
    $g5 = ($g2 & $x2_0);
    $g6 = ($g5 | $g4);
    $g7 = ($g3 & $x3_1);
    $g8 = ($g2 & $x2_1);
    $g9 = ($g8 | $g7);
    $g10 = ($g3 & $x3_2);
    $g11 = ($g2 & $x2_2);
    $g12 = ($g11 | $g10);
    $g13 = ($g3 & $x3_3);
    $g14 = ($g2 & $x2_3);
    $g15 = ($g14 | $g13);
    $g16 = ($g3 & $x3_4);
    $g17 = ($g2 & $x2_4);
    $g18 = ($g17 | $g16);
    $g19 = ($g3 & $x3_5);
    $g20 = ($g2 & $x2_5);
    $g21 = ($g20 | $g19);
    $g22 = ($g3 & $x3_6);
    $g23 = ($g2 & $x2_6);
    $g24 = ($g23 | $g22);
    $g25 = ($g3 & $x3_7);
    $g26 = ($g2 & $x2_7);
    $g27 = ($g26 | $g25);
    $g28 = ($g3 & $x3_8);
    $g29 = ($g2 & $x2_8);
    $g30 = ($g29 | $g28);
    $g31 = ($g3 & $x3_9);
    $g32 = ($g2 & $x2_9);
    $g33 = ($g32 | $g31);
    $g34 = ($g3 & $x3_10);
    $g35 = ($g2 & $x2_10);
    $g36 = ($g35 | $g34);
    $g37 = ($g3 & $x3_11);
    $g38 = ($g2 & $x2_11);
    $g39 = ($g38 | $g37);
    $g40 = ($g3 & $x3_12);
    $g41 = ($g2 & $x2_12);
    $g42 = ($g41 | $g40);
    $g43 = ($g3 & $x3_13);
    $g44 = ($g2 & $x2_13);
    $g45 = ($g44 | $g43);
    $g46 = ($g3 & $x3_14);
    $g47 = ($g2 & $x2_14);
    $g48 = ($g47 | $g46);
    $g49 = ($g3 & $x3_15);
    $g50 = ($g2 & $x2_15);
    $g51 = ($g50 | $g49);
    $g52 = ($g3 & $x3_16);
    $g53 = ($g2 & $x2_16);
    $g54 = ($g53 | $g52);
    $g55 = ($g3 & $x3_17);
    $g56 = ($g2 & $x2_17);
    $g57 = ($g56 | $g55);
    $g58 = ($g3 & $x3_18);
    $g59 = ($g2 & $x2_18);
    $g60 = ($g59 | $g58);
    $g61 = ($g3 & $x3_19);
    $g62 = ($g2 & $x2_19);
    $g63 = ($g62 | $g61);
    $g64 = ($g3 & $x3_20);
    $g65 = ($g2 & $x2_20);
    $g66 = ($g65 | $g64);
    $g67 = ($g3 & $x3_21);
    $g68 = ($g2 & $x2_21);
    $g69 = ($g68 | $g67);
    $g70 = ($g3 & $x3_22);
    $g71 = ($g2 & $x2_22);
    $g72 = ($g71 | $g70);
    $g73 = ($g3 & $x3_23);
    $g74 = ($g2 & $x2_23);
    $g75 = ($g74 | $g73);
    $g76 = ($g3 & $x3_24);
    $g77 = ($g2 & $x2_24);
    $g78 = ($g77 | $g76);
    $g79 = ($g3 & $x3_25);
    $g80 = ($g2 & $x2_25);
    $g81 = ($g80 | $g79);
    $g82 = ($g3 & $x3_26);
    $g83 = ($g2 & $x2_26);
    $g84 = ($g83 | $g82);
    $g85 = ($g3 & $x3_27);
    $g86 = ($g2 & $x2_27);
    $g87 = ($g86 | $g85);
    $g88 = ($g3 & $x3_28);
    $g89 = ($g2 & $x2_28);
    $g90 = ($g89 | $g88);
    $g91 = ($g3 & $x3_29);
    $g92 = ($g2 & $x2_29);
    $g93 = ($g92 | $g91);
    $g94 = ($g3 & $x3_30);
    $g95 = ($g2 & $x2_30);
    $g96 = ($g95 | $g94);
    $g97 = ($g3 & $x3_31);
    $g98 = ($g2 & $x2_31);
    $g99 = ($g98 | $g97);
    $g100 = ($g3 & $x3_32);
    $g101 = ($g2 & $x2_32);
    $g102 = ($g101 | $g100);
    $g103 = ($g3 & $x3_33);
    $g104 = ($g2 & $x2_33);
    $g105 = ($g104 | $g103);
    $g106 = ($g3 & $x3_34);
    $g107 = ($g2 & $x2_34);
    $g108 = ($g107 | $g106);
    $g109 = ($g3 & $x3_35);
    $g110 = ($g2 & $x2_35);
    $g111 = ($g110 | $g109);
    $g112 = ($g3 & $x3_36);
    $g113 = ($g2 & $x2_36);
    $g114 = ($g113 | $g112);
    $g115 = ($g3 & $x3_37);
    $g116 = ($g2 & $x2_37);
    $g117 = ($g116 | $g115);
    $g118 = ($g3 & $x3_38);
    $g119 = ($g2 & $x2_38);
    $g120 = ($g119 | $g118);
    $g121 = ($g3 & $x3_39);
    $g122 = ($g2 & $x2_39);
    $g123 = ($g122 | $g121);
    $g124 = ($g3 & $x3_40);
    $g125 = ($g2 & $x2_40);
    $g126 = ($g125 | $g124);
    $g127 = ($g3 & $x3_41);
    $g128 = ($g2 & $x2_41);
    $g129 = ($g128 | $g127);
    $g130 = ($g3 & $x3_42);
    $g131 = ($g2 & $x2_42);
    $g132 = ($g131 | $g130);
    $g133 = ($g3 & $x3_43);
    $g134 = ($g2 & $x2_43);
    $g135 = ($g134 | $g133);
    $g136 = ($g3 & $x3_44);
    $g137 = ($g2 & $x2_44);
    $g138 = ($g137 | $g136);
    $g139 = ($g3 & $x3_45);
    $g140 = ($g2 & $x2_45);
    $g141 = ($g140 | $g139);
    $g142 = ($g3 & $x3_46);
    $g143 = ($g2 & $x2_46);
    $g144 = ($g143 | $g142);
    $g145 = ($g3 & $x3_47);
    $g146 = ($g2 & $x2_47);
    $g147 = ($g146 | $g145);
    $g148 = ($g3 & $x3_48);
    $g149 = ($g2 & $x2_48);
    $g150 = ($g149 | $g148);
    $g151 = ($g3 & $x3_49);
    $g152 = ($g2 & $x2_49);
    $g153 = ($g152 | $g151);
    $g154 = ($g3 & $x3_50);
    $g155 = ($g2 & $x2_50);
    $g156 = ($g155 | $g154);
    $g157 = ($g3 & $x3_51);
    $g158 = ($g2 & $x2_51);
    $g159 = ($g158 | $g157);
    $g160 = ($g3 & $x3_52);
    $g161 = ($g2 & $x2_52);
    $g162 = ($g161 | $g160);
    $g163 = ($g3 & $x3_53);
    $g164 = ($g2 & $x2_53);
    $g165 = ($g164 | $g163);
    $g166 = ($g3 & $x3_54);
    $g167 = ($g2 & $x2_54);
    $g168 = ($g167 | $g166);
    $g169 = ($g3 & $x3_55);
    $g170 = ($g2 & $x2_55);
    $g171 = ($g170 | $g169);
    $g172 = ($g3 & $x3_56);
    $g173 = ($g2 & $x2_56);
    $g174 = ($g173 | $g172);
    $g175 = ($g3 & $x3_57);
    $g176 = ($g2 & $x2_57);
    $g177 = ($g176 | $g175);
    $g178 = ($g3 & $x3_58);
    $g179 = ($g2 & $x2_58);
    $g180 = ($g179 | $g178);
    $g181 = ($g3 & $x3_59);
    $g182 = ($g2 & $x2_59);
    $g183 = ($g182 | $g181);
    $g184 = ($g3 & $x3_60);
    $g185 = ($g2 & $x2_60);
    $g186 = ($g185 | $g184);
    $g187 = ($g3 & $x3_61);
    $g188 = ($g2 & $x2_61);
    $g189 = ($g188 | $g187);
    $g190 = ($g3 & $x3_62);
    $g191 = ($g2 & $x2_62);
    $g192 = ($g191 | $g190);
    $g193 = ($g3 & $x3_63);
    $g194 = ($g2 & $x2_63);
    $g195 = ($g194 | $g193);
    $w0 = $g195;
    $w1 = ex_cat($w0, $g192, 1);
    $w2 = ex_cat($w1, $g189, 1);
    $w3 = ex_cat($w2, $g186, 1);
    $w4 = ex_cat($w3, $g183, 1);
    $w5 = ex_cat($w4, $g180, 1);
    $w6 = ex_cat($w5, $g177, 1);
    $w7 = ex_cat($w6, $g174, 1);
    $w8 = ex_cat($w7, $g171, 1);
    $w9 = ex_cat($w8, $g168, 1);
    $w10 = ex_cat($w9, $g165, 1);
    $w11 = ex_cat($w10, $g162, 1);
    $w12 = ex_cat($w11, $g159, 1);
    $w13 = ex_cat($w12, $g156, 1);
    $w14 = ex_cat($w13, $g153, 1);
    $w15 = ex_cat($w14, $g150, 1);
    $w16 = ex_cat($w15, $g147, 1);
    $w17 = ex_cat($w16, $g144, 1);
    $w18 = ex_cat($w17, $g141, 1);
    $w19 = ex_cat($w18, $g138, 1);
    $w20 = ex_cat($w19, $g135, 1);
    $w21 = ex_cat($w20, $g132, 1);
    $w22 = ex_cat($w21, $g129, 1);
    $w23 = ex_cat($w22, $g126, 1);
    $w24 = ex_cat($w23, $g123, 1);
    $w25 = ex_cat($w24, $g120, 1);
    $w26 = ex_cat($w25, $g117, 1);
    $w27 = ex_cat($w26, $g114, 1);
    $w28 = ex_cat($w27, $g111, 1);
    $w29 = ex_cat($w28, $g108, 1);
    $w30 = ex_cat($w29, $g105, 1);
    $w31 = ex_cat($w30, $g102, 1);
    $w32 = ex_cat($w31, $g99, 1);
    $w33 = ex_cat($w32, $g96, 1);
    $w34 = ex_cat($w33, $g93, 1);
    $w35 = ex_cat($w34, $g90, 1);
    $w36 = ex_cat($w35, $g87, 1);
    $w37 = ex_cat($w36, $g84, 1);
    $w38 = ex_cat($w37, $g81, 1);
    $w39 = ex_cat($w38, $g78, 1);
    $w40 = ex_cat($w39, $g75, 1);
    $w41 = ex_cat($w40, $g72, 1);
    $w42 = ex_cat($w41, $g69, 1);
    $w43 = ex_cat($w42, $g66, 1);
    $w44 = ex_cat($w43, $g63, 1);
    $w45 = ex_cat($w44, $g60, 1);
    $w46 = ex_cat($w45, $g57, 1);
    $w47 = ex_cat($w46, $g54, 1);
    $w48 = ex_cat($w47, $g51, 1);
    $w49 = ex_cat($w48, $g48, 1);
    $w50 = ex_cat($w49, $g45, 1);
    $w51 = ex_cat($w50, $g42, 1);
    $w52 = ex_cat($w51, $g39, 1);
    $w53 = ex_cat($w52, $g36, 1);
    $w54 = ex_cat($w53, $g33, 1);
    $w55 = ex_cat($w54, $g30, 1);
    $w56 = ex_cat($w55, $g27, 1);
    $w57 = ex_cat($w56, $g24, 1);
    $w58 = ex_cat($w57, $g21, 1);
    $w59 = ex_cat($w58, $g18, 1);
    $w60 = ex_cat($w59, $g15, 1);
    $w61 = ex_cat($w60, $g12, 1);
    $w62 = ex_cat($w61, $g9, 1);
    $w63 = ex_cat($w62, $g6, 1);
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
        $answer = emu_cmovs_gpr_gpr_64__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
