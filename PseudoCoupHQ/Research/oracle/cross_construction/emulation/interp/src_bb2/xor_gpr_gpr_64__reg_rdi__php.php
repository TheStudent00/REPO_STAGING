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
// one named local per gate, over the term of xor_gpr_gpr_64__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   v0 ^ v1
function emu_xor_gpr_gpr_64__reg_rdi__php($a, $b) {
    $x1_0 = ex_ext($b, 0, 0);
    $x0_0 = ex_ext($a, 0, 0);
    $x1_1 = ex_ext($b, 1, 1);
    $x0_1 = ex_ext($a, 1, 1);
    $x1_2 = ex_ext($b, 2, 2);
    $x0_2 = ex_ext($a, 2, 2);
    $x1_3 = ex_ext($b, 3, 3);
    $x0_3 = ex_ext($a, 3, 3);
    $x1_4 = ex_ext($b, 4, 4);
    $x0_4 = ex_ext($a, 4, 4);
    $x1_5 = ex_ext($b, 5, 5);
    $x0_5 = ex_ext($a, 5, 5);
    $x1_6 = ex_ext($b, 6, 6);
    $x0_6 = ex_ext($a, 6, 6);
    $x1_7 = ex_ext($b, 7, 7);
    $x0_7 = ex_ext($a, 7, 7);
    $x1_8 = ex_ext($b, 8, 8);
    $x0_8 = ex_ext($a, 8, 8);
    $x1_9 = ex_ext($b, 9, 9);
    $x0_9 = ex_ext($a, 9, 9);
    $x1_10 = ex_ext($b, 10, 10);
    $x0_10 = ex_ext($a, 10, 10);
    $x1_11 = ex_ext($b, 11, 11);
    $x0_11 = ex_ext($a, 11, 11);
    $x1_12 = ex_ext($b, 12, 12);
    $x0_12 = ex_ext($a, 12, 12);
    $x1_13 = ex_ext($b, 13, 13);
    $x0_13 = ex_ext($a, 13, 13);
    $x1_14 = ex_ext($b, 14, 14);
    $x0_14 = ex_ext($a, 14, 14);
    $x1_15 = ex_ext($b, 15, 15);
    $x0_15 = ex_ext($a, 15, 15);
    $x1_16 = ex_ext($b, 16, 16);
    $x0_16 = ex_ext($a, 16, 16);
    $x1_17 = ex_ext($b, 17, 17);
    $x0_17 = ex_ext($a, 17, 17);
    $x1_18 = ex_ext($b, 18, 18);
    $x0_18 = ex_ext($a, 18, 18);
    $x1_19 = ex_ext($b, 19, 19);
    $x0_19 = ex_ext($a, 19, 19);
    $x1_20 = ex_ext($b, 20, 20);
    $x0_20 = ex_ext($a, 20, 20);
    $x1_21 = ex_ext($b, 21, 21);
    $x0_21 = ex_ext($a, 21, 21);
    $x1_22 = ex_ext($b, 22, 22);
    $x0_22 = ex_ext($a, 22, 22);
    $x1_23 = ex_ext($b, 23, 23);
    $x0_23 = ex_ext($a, 23, 23);
    $x1_24 = ex_ext($b, 24, 24);
    $x0_24 = ex_ext($a, 24, 24);
    $x1_25 = ex_ext($b, 25, 25);
    $x0_25 = ex_ext($a, 25, 25);
    $x1_26 = ex_ext($b, 26, 26);
    $x0_26 = ex_ext($a, 26, 26);
    $x1_27 = ex_ext($b, 27, 27);
    $x0_27 = ex_ext($a, 27, 27);
    $x1_28 = ex_ext($b, 28, 28);
    $x0_28 = ex_ext($a, 28, 28);
    $x1_29 = ex_ext($b, 29, 29);
    $x0_29 = ex_ext($a, 29, 29);
    $x1_30 = ex_ext($b, 30, 30);
    $x0_30 = ex_ext($a, 30, 30);
    $x1_31 = ex_ext($b, 31, 31);
    $x0_31 = ex_ext($a, 31, 31);
    $x1_32 = ex_ext($b, 32, 32);
    $x0_32 = ex_ext($a, 32, 32);
    $x1_33 = ex_ext($b, 33, 33);
    $x0_33 = ex_ext($a, 33, 33);
    $x1_34 = ex_ext($b, 34, 34);
    $x0_34 = ex_ext($a, 34, 34);
    $x1_35 = ex_ext($b, 35, 35);
    $x0_35 = ex_ext($a, 35, 35);
    $x1_36 = ex_ext($b, 36, 36);
    $x0_36 = ex_ext($a, 36, 36);
    $x1_37 = ex_ext($b, 37, 37);
    $x0_37 = ex_ext($a, 37, 37);
    $x1_38 = ex_ext($b, 38, 38);
    $x0_38 = ex_ext($a, 38, 38);
    $x1_39 = ex_ext($b, 39, 39);
    $x0_39 = ex_ext($a, 39, 39);
    $x1_40 = ex_ext($b, 40, 40);
    $x0_40 = ex_ext($a, 40, 40);
    $x1_41 = ex_ext($b, 41, 41);
    $x0_41 = ex_ext($a, 41, 41);
    $x1_42 = ex_ext($b, 42, 42);
    $x0_42 = ex_ext($a, 42, 42);
    $x1_43 = ex_ext($b, 43, 43);
    $x0_43 = ex_ext($a, 43, 43);
    $x1_44 = ex_ext($b, 44, 44);
    $x0_44 = ex_ext($a, 44, 44);
    $x1_45 = ex_ext($b, 45, 45);
    $x0_45 = ex_ext($a, 45, 45);
    $x1_46 = ex_ext($b, 46, 46);
    $x0_46 = ex_ext($a, 46, 46);
    $x1_47 = ex_ext($b, 47, 47);
    $x0_47 = ex_ext($a, 47, 47);
    $x1_48 = ex_ext($b, 48, 48);
    $x0_48 = ex_ext($a, 48, 48);
    $x1_49 = ex_ext($b, 49, 49);
    $x0_49 = ex_ext($a, 49, 49);
    $x1_50 = ex_ext($b, 50, 50);
    $x0_50 = ex_ext($a, 50, 50);
    $x1_51 = ex_ext($b, 51, 51);
    $x0_51 = ex_ext($a, 51, 51);
    $x1_52 = ex_ext($b, 52, 52);
    $x0_52 = ex_ext($a, 52, 52);
    $x1_53 = ex_ext($b, 53, 53);
    $x0_53 = ex_ext($a, 53, 53);
    $x1_54 = ex_ext($b, 54, 54);
    $x0_54 = ex_ext($a, 54, 54);
    $x1_55 = ex_ext($b, 55, 55);
    $x0_55 = ex_ext($a, 55, 55);
    $x1_56 = ex_ext($b, 56, 56);
    $x0_56 = ex_ext($a, 56, 56);
    $x1_57 = ex_ext($b, 57, 57);
    $x0_57 = ex_ext($a, 57, 57);
    $x1_58 = ex_ext($b, 58, 58);
    $x0_58 = ex_ext($a, 58, 58);
    $x1_59 = ex_ext($b, 59, 59);
    $x0_59 = ex_ext($a, 59, 59);
    $x1_60 = ex_ext($b, 60, 60);
    $x0_60 = ex_ext($a, 60, 60);
    $x1_61 = ex_ext($b, 61, 61);
    $x0_61 = ex_ext($a, 61, 61);
    $x1_62 = ex_ext($b, 62, 62);
    $x0_62 = ex_ext($a, 62, 62);
    $x1_63 = ex_ext($b, 63, 63);
    $x0_63 = ex_ext($a, 63, 63);
    $g0 = ($x0_0 ^ $x1_0);
    $g1 = ($g0 ^ 1);
    $g2 = ($g1 ^ 1);
    $g3 = ($x0_1 ^ $x1_1);
    $g4 = ($g3 ^ 1);
    $g5 = ($g4 ^ 1);
    $g6 = ($x0_2 ^ $x1_2);
    $g7 = ($g6 ^ 1);
    $g8 = ($g7 ^ 1);
    $g9 = ($x0_3 ^ $x1_3);
    $g10 = ($g9 ^ 1);
    $g11 = ($g10 ^ 1);
    $g12 = ($x0_4 ^ $x1_4);
    $g13 = ($g12 ^ 1);
    $g14 = ($g13 ^ 1);
    $g15 = ($x0_5 ^ $x1_5);
    $g16 = ($g15 ^ 1);
    $g17 = ($g16 ^ 1);
    $g18 = ($x0_6 ^ $x1_6);
    $g19 = ($g18 ^ 1);
    $g20 = ($g19 ^ 1);
    $g21 = ($x0_7 ^ $x1_7);
    $g22 = ($g21 ^ 1);
    $g23 = ($g22 ^ 1);
    $g24 = ($x0_8 ^ $x1_8);
    $g25 = ($g24 ^ 1);
    $g26 = ($g25 ^ 1);
    $g27 = ($x0_9 ^ $x1_9);
    $g28 = ($g27 ^ 1);
    $g29 = ($g28 ^ 1);
    $g30 = ($x0_10 ^ $x1_10);
    $g31 = ($g30 ^ 1);
    $g32 = ($g31 ^ 1);
    $g33 = ($x0_11 ^ $x1_11);
    $g34 = ($g33 ^ 1);
    $g35 = ($g34 ^ 1);
    $g36 = ($x0_12 ^ $x1_12);
    $g37 = ($g36 ^ 1);
    $g38 = ($g37 ^ 1);
    $g39 = ($x0_13 ^ $x1_13);
    $g40 = ($g39 ^ 1);
    $g41 = ($g40 ^ 1);
    $g42 = ($x0_14 ^ $x1_14);
    $g43 = ($g42 ^ 1);
    $g44 = ($g43 ^ 1);
    $g45 = ($x0_15 ^ $x1_15);
    $g46 = ($g45 ^ 1);
    $g47 = ($g46 ^ 1);
    $g48 = ($x0_16 ^ $x1_16);
    $g49 = ($g48 ^ 1);
    $g50 = ($g49 ^ 1);
    $g51 = ($x0_17 ^ $x1_17);
    $g52 = ($g51 ^ 1);
    $g53 = ($g52 ^ 1);
    $g54 = ($x0_18 ^ $x1_18);
    $g55 = ($g54 ^ 1);
    $g56 = ($g55 ^ 1);
    $g57 = ($x0_19 ^ $x1_19);
    $g58 = ($g57 ^ 1);
    $g59 = ($g58 ^ 1);
    $g60 = ($x0_20 ^ $x1_20);
    $g61 = ($g60 ^ 1);
    $g62 = ($g61 ^ 1);
    $g63 = ($x0_21 ^ $x1_21);
    $g64 = ($g63 ^ 1);
    $g65 = ($g64 ^ 1);
    $g66 = ($x0_22 ^ $x1_22);
    $g67 = ($g66 ^ 1);
    $g68 = ($g67 ^ 1);
    $g69 = ($x0_23 ^ $x1_23);
    $g70 = ($g69 ^ 1);
    $g71 = ($g70 ^ 1);
    $g72 = ($x0_24 ^ $x1_24);
    $g73 = ($g72 ^ 1);
    $g74 = ($g73 ^ 1);
    $g75 = ($x0_25 ^ $x1_25);
    $g76 = ($g75 ^ 1);
    $g77 = ($g76 ^ 1);
    $g78 = ($x0_26 ^ $x1_26);
    $g79 = ($g78 ^ 1);
    $g80 = ($g79 ^ 1);
    $g81 = ($x0_27 ^ $x1_27);
    $g82 = ($g81 ^ 1);
    $g83 = ($g82 ^ 1);
    $g84 = ($x0_28 ^ $x1_28);
    $g85 = ($g84 ^ 1);
    $g86 = ($g85 ^ 1);
    $g87 = ($x0_29 ^ $x1_29);
    $g88 = ($g87 ^ 1);
    $g89 = ($g88 ^ 1);
    $g90 = ($x0_30 ^ $x1_30);
    $g91 = ($g90 ^ 1);
    $g92 = ($g91 ^ 1);
    $g93 = ($x0_31 ^ $x1_31);
    $g94 = ($g93 ^ 1);
    $g95 = ($g94 ^ 1);
    $g96 = ($x0_32 ^ $x1_32);
    $g97 = ($g96 ^ 1);
    $g98 = ($g97 ^ 1);
    $g99 = ($x0_33 ^ $x1_33);
    $g100 = ($g99 ^ 1);
    $g101 = ($g100 ^ 1);
    $g102 = ($x0_34 ^ $x1_34);
    $g103 = ($g102 ^ 1);
    $g104 = ($g103 ^ 1);
    $g105 = ($x0_35 ^ $x1_35);
    $g106 = ($g105 ^ 1);
    $g107 = ($g106 ^ 1);
    $g108 = ($x0_36 ^ $x1_36);
    $g109 = ($g108 ^ 1);
    $g110 = ($g109 ^ 1);
    $g111 = ($x0_37 ^ $x1_37);
    $g112 = ($g111 ^ 1);
    $g113 = ($g112 ^ 1);
    $g114 = ($x0_38 ^ $x1_38);
    $g115 = ($g114 ^ 1);
    $g116 = ($g115 ^ 1);
    $g117 = ($x0_39 ^ $x1_39);
    $g118 = ($g117 ^ 1);
    $g119 = ($g118 ^ 1);
    $g120 = ($x0_40 ^ $x1_40);
    $g121 = ($g120 ^ 1);
    $g122 = ($g121 ^ 1);
    $g123 = ($x0_41 ^ $x1_41);
    $g124 = ($g123 ^ 1);
    $g125 = ($g124 ^ 1);
    $g126 = ($x0_42 ^ $x1_42);
    $g127 = ($g126 ^ 1);
    $g128 = ($g127 ^ 1);
    $g129 = ($x0_43 ^ $x1_43);
    $g130 = ($g129 ^ 1);
    $g131 = ($g130 ^ 1);
    $g132 = ($x0_44 ^ $x1_44);
    $g133 = ($g132 ^ 1);
    $g134 = ($g133 ^ 1);
    $g135 = ($x0_45 ^ $x1_45);
    $g136 = ($g135 ^ 1);
    $g137 = ($g136 ^ 1);
    $g138 = ($x0_46 ^ $x1_46);
    $g139 = ($g138 ^ 1);
    $g140 = ($g139 ^ 1);
    $g141 = ($x0_47 ^ $x1_47);
    $g142 = ($g141 ^ 1);
    $g143 = ($g142 ^ 1);
    $g144 = ($x0_48 ^ $x1_48);
    $g145 = ($g144 ^ 1);
    $g146 = ($g145 ^ 1);
    $g147 = ($x0_49 ^ $x1_49);
    $g148 = ($g147 ^ 1);
    $g149 = ($g148 ^ 1);
    $g150 = ($x0_50 ^ $x1_50);
    $g151 = ($g150 ^ 1);
    $g152 = ($g151 ^ 1);
    $g153 = ($x0_51 ^ $x1_51);
    $g154 = ($g153 ^ 1);
    $g155 = ($g154 ^ 1);
    $g156 = ($x0_52 ^ $x1_52);
    $g157 = ($g156 ^ 1);
    $g158 = ($g157 ^ 1);
    $g159 = ($x0_53 ^ $x1_53);
    $g160 = ($g159 ^ 1);
    $g161 = ($g160 ^ 1);
    $g162 = ($x0_54 ^ $x1_54);
    $g163 = ($g162 ^ 1);
    $g164 = ($g163 ^ 1);
    $g165 = ($x0_55 ^ $x1_55);
    $g166 = ($g165 ^ 1);
    $g167 = ($g166 ^ 1);
    $g168 = ($x0_56 ^ $x1_56);
    $g169 = ($g168 ^ 1);
    $g170 = ($g169 ^ 1);
    $g171 = ($x0_57 ^ $x1_57);
    $g172 = ($g171 ^ 1);
    $g173 = ($g172 ^ 1);
    $g174 = ($x0_58 ^ $x1_58);
    $g175 = ($g174 ^ 1);
    $g176 = ($g175 ^ 1);
    $g177 = ($x0_59 ^ $x1_59);
    $g178 = ($g177 ^ 1);
    $g179 = ($g178 ^ 1);
    $g180 = ($x0_60 ^ $x1_60);
    $g181 = ($g180 ^ 1);
    $g182 = ($g181 ^ 1);
    $g183 = ($x0_61 ^ $x1_61);
    $g184 = ($g183 ^ 1);
    $g185 = ($g184 ^ 1);
    $g186 = ($x0_62 ^ $x1_62);
    $g187 = ($g186 ^ 1);
    $g188 = ($g187 ^ 1);
    $g189 = ($x0_63 ^ $x1_63);
    $g190 = ($g189 ^ 1);
    $g191 = ($g190 ^ 1);
    $w0 = $g191;
    $w1 = ex_cat($w0, $g188, 1);
    $w2 = ex_cat($w1, $g185, 1);
    $w3 = ex_cat($w2, $g182, 1);
    $w4 = ex_cat($w3, $g179, 1);
    $w5 = ex_cat($w4, $g176, 1);
    $w6 = ex_cat($w5, $g173, 1);
    $w7 = ex_cat($w6, $g170, 1);
    $w8 = ex_cat($w7, $g167, 1);
    $w9 = ex_cat($w8, $g164, 1);
    $w10 = ex_cat($w9, $g161, 1);
    $w11 = ex_cat($w10, $g158, 1);
    $w12 = ex_cat($w11, $g155, 1);
    $w13 = ex_cat($w12, $g152, 1);
    $w14 = ex_cat($w13, $g149, 1);
    $w15 = ex_cat($w14, $g146, 1);
    $w16 = ex_cat($w15, $g143, 1);
    $w17 = ex_cat($w16, $g140, 1);
    $w18 = ex_cat($w17, $g137, 1);
    $w19 = ex_cat($w18, $g134, 1);
    $w20 = ex_cat($w19, $g131, 1);
    $w21 = ex_cat($w20, $g128, 1);
    $w22 = ex_cat($w21, $g125, 1);
    $w23 = ex_cat($w22, $g122, 1);
    $w24 = ex_cat($w23, $g119, 1);
    $w25 = ex_cat($w24, $g116, 1);
    $w26 = ex_cat($w25, $g113, 1);
    $w27 = ex_cat($w26, $g110, 1);
    $w28 = ex_cat($w27, $g107, 1);
    $w29 = ex_cat($w28, $g104, 1);
    $w30 = ex_cat($w29, $g101, 1);
    $w31 = ex_cat($w30, $g98, 1);
    $w32 = ex_cat($w31, $g95, 1);
    $w33 = ex_cat($w32, $g92, 1);
    $w34 = ex_cat($w33, $g89, 1);
    $w35 = ex_cat($w34, $g86, 1);
    $w36 = ex_cat($w35, $g83, 1);
    $w37 = ex_cat($w36, $g80, 1);
    $w38 = ex_cat($w37, $g77, 1);
    $w39 = ex_cat($w38, $g74, 1);
    $w40 = ex_cat($w39, $g71, 1);
    $w41 = ex_cat($w40, $g68, 1);
    $w42 = ex_cat($w41, $g65, 1);
    $w43 = ex_cat($w42, $g62, 1);
    $w44 = ex_cat($w43, $g59, 1);
    $w45 = ex_cat($w44, $g56, 1);
    $w46 = ex_cat($w45, $g53, 1);
    $w47 = ex_cat($w46, $g50, 1);
    $w48 = ex_cat($w47, $g47, 1);
    $w49 = ex_cat($w48, $g44, 1);
    $w50 = ex_cat($w49, $g41, 1);
    $w51 = ex_cat($w50, $g38, 1);
    $w52 = ex_cat($w51, $g35, 1);
    $w53 = ex_cat($w52, $g32, 1);
    $w54 = ex_cat($w53, $g29, 1);
    $w55 = ex_cat($w54, $g26, 1);
    $w56 = ex_cat($w55, $g23, 1);
    $w57 = ex_cat($w56, $g20, 1);
    $w58 = ex_cat($w57, $g17, 1);
    $w59 = ex_cat($w58, $g14, 1);
    $w60 = ex_cat($w59, $g11, 1);
    $w61 = ex_cat($w60, $g8, 1);
    $w62 = ex_cat($w61, $g5, 1);
    $w63 = ex_cat($w62, $g2, 1);
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
        $answer = emu_xor_gpr_gpr_64__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
