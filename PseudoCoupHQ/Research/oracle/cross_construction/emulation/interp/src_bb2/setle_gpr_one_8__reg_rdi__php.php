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
// one named local per gate, over the term of setle_gpr_one_8__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v2), If(Or(Extract(7, 0, v0) == Extract(7, 0, v1), Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 1, 0)), 1, 0))
function emu_setle_gpr_one_8__reg_rdi__php($a, $b, $c) {
    $x0_7 = ex_ext($b, 7, 7);
    $x0_1 = ex_ext($b, 1, 1);
    $x0_0 = ex_ext($b, 0, 0);
    $x0_2 = ex_ext($b, 2, 2);
    $x0_3 = ex_ext($b, 3, 3);
    $x0_4 = ex_ext($b, 4, 4);
    $x0_5 = ex_ext($b, 5, 5);
    $x0_6 = ex_ext($b, 6, 6);
    $x1_6 = ex_ext($a, 6, 6);
    $x1_4 = ex_ext($a, 4, 4);
    $x1_3 = ex_ext($a, 3, 3);
    $x1_2 = ex_ext($a, 2, 2);
    $x1_0 = ex_ext($a, 0, 0);
    $x1_1 = ex_ext($a, 1, 1);
    $x1_5 = ex_ext($a, 5, 5);
    $x1_7 = ex_ext($a, 7, 7);
    $x2_8 = ex_ext($c, 8, 8);
    $x2_9 = ex_ext($c, 9, 9);
    $x2_10 = ex_ext($c, 10, 10);
    $x2_11 = ex_ext($c, 11, 11);
    $x2_12 = ex_ext($c, 12, 12);
    $x2_13 = ex_ext($c, 13, 13);
    $x2_14 = ex_ext($c, 14, 14);
    $x2_15 = ex_ext($c, 15, 15);
    $x2_16 = ex_ext($c, 16, 16);
    $x2_17 = ex_ext($c, 17, 17);
    $x2_18 = ex_ext($c, 18, 18);
    $x2_19 = ex_ext($c, 19, 19);
    $x2_20 = ex_ext($c, 20, 20);
    $x2_21 = ex_ext($c, 21, 21);
    $x2_22 = ex_ext($c, 22, 22);
    $x2_23 = ex_ext($c, 23, 23);
    $x2_24 = ex_ext($c, 24, 24);
    $x2_25 = ex_ext($c, 25, 25);
    $x2_26 = ex_ext($c, 26, 26);
    $x2_27 = ex_ext($c, 27, 27);
    $x2_28 = ex_ext($c, 28, 28);
    $x2_29 = ex_ext($c, 29, 29);
    $x2_30 = ex_ext($c, 30, 30);
    $x2_31 = ex_ext($c, 31, 31);
    $x2_32 = ex_ext($c, 32, 32);
    $x2_33 = ex_ext($c, 33, 33);
    $x2_34 = ex_ext($c, 34, 34);
    $x2_35 = ex_ext($c, 35, 35);
    $x2_36 = ex_ext($c, 36, 36);
    $x2_37 = ex_ext($c, 37, 37);
    $x2_38 = ex_ext($c, 38, 38);
    $x2_39 = ex_ext($c, 39, 39);
    $x2_40 = ex_ext($c, 40, 40);
    $x2_41 = ex_ext($c, 41, 41);
    $x2_42 = ex_ext($c, 42, 42);
    $x2_43 = ex_ext($c, 43, 43);
    $x2_44 = ex_ext($c, 44, 44);
    $x2_45 = ex_ext($c, 45, 45);
    $x2_46 = ex_ext($c, 46, 46);
    $x2_47 = ex_ext($c, 47, 47);
    $x2_48 = ex_ext($c, 48, 48);
    $x2_49 = ex_ext($c, 49, 49);
    $x2_50 = ex_ext($c, 50, 50);
    $x2_51 = ex_ext($c, 51, 51);
    $x2_52 = ex_ext($c, 52, 52);
    $x2_53 = ex_ext($c, 53, 53);
    $x2_54 = ex_ext($c, 54, 54);
    $x2_55 = ex_ext($c, 55, 55);
    $x2_56 = ex_ext($c, 56, 56);
    $x2_57 = ex_ext($c, 57, 57);
    $x2_58 = ex_ext($c, 58, 58);
    $x2_59 = ex_ext($c, 59, 59);
    $x2_60 = ex_ext($c, 60, 60);
    $x2_61 = ex_ext($c, 61, 61);
    $x2_62 = ex_ext($c, 62, 62);
    $x2_63 = ex_ext($c, 63, 63);
    $g0 = ($x0_0 | $x0_1);
    $g1 = ($x0_2 | $g0);
    $g2 = ($x0_3 | $g1);
    $g3 = ($x0_4 | $g2);
    $g4 = ($x0_5 | $g3);
    $g5 = ($x0_6 | $g4);
    $g6 = ($x0_7 | $g5);
    $g7 = ($g6 ^ $x0_7);
    $g8 = ($g7 ^ 1);
    $g9 = ($g5 ^ $x0_7);
    $g10 = ($g9 ^ 1);
    $g11 = ($x1_6 ^ 1);
    $g12 = ($g4 ^ $x0_6);
    $g13 = ($g12 ^ 1);
    $g14 = ($g13 | $g11);
    $g15 = ($g14 ^ 1);
    $g16 = ($x1_4 ^ 1);
    $g17 = ($g2 ^ $x0_4);
    $g18 = ($g17 ^ 1);
    $g19 = ($g18 | $g16);
    $g20 = ($g19 ^ 1);
    $g21 = ($x1_3 ^ 1);
    $g22 = ($g1 ^ $x0_3);
    $g23 = ($g22 ^ 1);
    $g24 = ($g23 | $g21);
    $g25 = ($g24 ^ 1);
    $g26 = ($x1_2 ^ 1);
    $g27 = ($g0 ^ $x0_2);
    $g28 = ($g27 ^ 1);
    $g29 = ($g28 | $g26);
    $g30 = ($g29 ^ 1);
    $g31 = ($x1_0 ^ 1);
    $g32 = ($x0_0 ^ 1);
    $g33 = ($g32 | $g31);
    $g34 = ($x0_0 ^ $x0_1);
    $g35 = ($g34 ^ 1);
    $g36 = ($g35 | $g33);
    $g37 = ($g36 ^ 1);
    $g38 = ($x1_1 ^ 1);
    $g39 = ($g38 | $g35);
    $g40 = ($g39 ^ 1);
    $g41 = ($g38 | $g33);
    $g42 = ($g41 ^ 1);
    $g43 = ($g42 | $g40);
    $g44 = ($g43 | $g37);
    $g45 = ($g44 ^ 1);
    $g46 = ($g26 | $g45);
    $g47 = ($g46 ^ 1);
    $g48 = ($g45 | $g28);
    $g49 = ($g48 ^ 1);
    $g50 = ($g49 | $g47);
    $g51 = ($g50 | $g30);
    $g52 = ($g51 ^ 1);
    $g53 = ($g21 | $g52);
    $g54 = ($g53 ^ 1);
    $g55 = ($g52 | $g23);
    $g56 = ($g55 ^ 1);
    $g57 = ($g56 | $g54);
    $g58 = ($g57 | $g25);
    $g59 = ($g58 ^ 1);
    $g60 = ($g18 | $g59);
    $g61 = ($g60 ^ 1);
    $g62 = ($g16 | $g59);
    $g63 = ($g62 ^ 1);
    $g64 = ($g63 | $g61);
    $g65 = ($g64 | $g20);
    $g66 = ($g65 ^ 1);
    $g67 = ($x1_5 ^ 1);
    $g68 = ($g67 | $g66);
    $g69 = ($g68 ^ 1);
    $g70 = ($g3 ^ $x0_5);
    $g71 = ($g70 ^ 1);
    $g72 = ($g66 | $g71);
    $g73 = ($g72 ^ 1);
    $g74 = ($g67 | $g71);
    $g75 = ($g74 ^ 1);
    $g76 = ($g75 | $g73);
    $g77 = ($g76 | $g69);
    $g78 = ($g77 ^ 1);
    $g79 = ($g13 | $g78);
    $g80 = ($g79 ^ 1);
    $g81 = ($g11 | $g78);
    $g82 = ($g81 ^ 1);
    $g83 = ($g82 | $g80);
    $g84 = ($g83 | $g15);
    $g85 = ($g84 ^ 1);
    $g86 = ($g85 | $g10);
    $g87 = ($g86 ^ 1);
    $g88 = ($x1_7 ^ 1);
    $g89 = ($g10 | $g88);
    $g90 = ($g89 ^ 1);
    $g91 = ($g88 | $g85);
    $g92 = ($g91 ^ 1);
    $g93 = ($g92 | $g90);
    $g94 = ($g93 | $g87);
    $g95 = ($x1_7 ^ $g94);
    $g96 = ($g95 ^ 1);
    $g97 = ($g96 ^ $g8);
    $g98 = ($g97 ^ 1);
    $g99 = ($x1_7 ^ $g84);
    $g100 = ($g99 ^ 1);
    $g101 = ($g100 ^ $g10);
    $g102 = ($g101 ^ 1);
    $g103 = ($g102 ^ $g98);
    $g104 = ($g103 ^ 1);
    $g105 = ($g102 ^ $g104);
    $g106 = ($g105 ^ 1);
    $g107 = ($g106 ^ 1);
    $g108 = ($x0_7 | $g88);
    $g109 = ($x0_7 ^ 1);
    $g110 = ($x1_7 | $g109);
    $g111 = ($g11 | $x0_6);
    $g112 = ($x0_6 ^ 1);
    $g113 = ($g112 | $x1_6);
    $g114 = ($x0_5 | $g67);
    $g115 = ($x0_5 ^ 1);
    $g116 = ($g115 | $x1_5);
    $g117 = ($x0_4 | $g16);
    $g118 = ($x0_4 ^ 1);
    $g119 = ($x1_4 | $g118);
    $g120 = ($x0_3 | $g21);
    $g121 = ($x0_3 ^ 1);
    $g122 = ($x1_3 | $g121);
    $g123 = ($x0_2 | $g26);
    $g124 = ($x0_2 ^ 1);
    $g125 = ($x1_2 | $g124);
    $g126 = ($g38 | $x0_1);
    $g127 = ($x0_1 ^ 1);
    $g128 = ($g127 | $x1_1);
    $g129 = ($g31 | $x0_0);
    $g130 = ($g32 | $x1_0);
    $g131 = ($g130 & $g129);
    $g132 = ($g131 & $g128);
    $g133 = ($g132 & $g126);
    $g134 = ($g133 & $g125);
    $g135 = ($g134 & $g123);
    $g136 = ($g135 & $g122);
    $g137 = ($g136 & $g120);
    $g138 = ($g137 & $g119);
    $g139 = ($g138 & $g117);
    $g140 = ($g139 & $g116);
    $g141 = ($g140 & $g114);
    $g142 = ($g141 & $g113);
    $g143 = ($g142 & $g111);
    $g144 = ($g143 & $g110);
    $g145 = ($g144 & $g108);
    $g146 = ($g145 | $g107);
    $k0 = 0;
    $w0 = $x2_63;
    $w1 = ex_cat($w0, $x2_62, 1);
    $w2 = ex_cat($w1, $x2_61, 1);
    $w3 = ex_cat($w2, $x2_60, 1);
    $w4 = ex_cat($w3, $x2_59, 1);
    $w5 = ex_cat($w4, $x2_58, 1);
    $w6 = ex_cat($w5, $x2_57, 1);
    $w7 = ex_cat($w6, $x2_56, 1);
    $w8 = ex_cat($w7, $x2_55, 1);
    $w9 = ex_cat($w8, $x2_54, 1);
    $w10 = ex_cat($w9, $x2_53, 1);
    $w11 = ex_cat($w10, $x2_52, 1);
    $w12 = ex_cat($w11, $x2_51, 1);
    $w13 = ex_cat($w12, $x2_50, 1);
    $w14 = ex_cat($w13, $x2_49, 1);
    $w15 = ex_cat($w14, $x2_48, 1);
    $w16 = ex_cat($w15, $x2_47, 1);
    $w17 = ex_cat($w16, $x2_46, 1);
    $w18 = ex_cat($w17, $x2_45, 1);
    $w19 = ex_cat($w18, $x2_44, 1);
    $w20 = ex_cat($w19, $x2_43, 1);
    $w21 = ex_cat($w20, $x2_42, 1);
    $w22 = ex_cat($w21, $x2_41, 1);
    $w23 = ex_cat($w22, $x2_40, 1);
    $w24 = ex_cat($w23, $x2_39, 1);
    $w25 = ex_cat($w24, $x2_38, 1);
    $w26 = ex_cat($w25, $x2_37, 1);
    $w27 = ex_cat($w26, $x2_36, 1);
    $w28 = ex_cat($w27, $x2_35, 1);
    $w29 = ex_cat($w28, $x2_34, 1);
    $w30 = ex_cat($w29, $x2_33, 1);
    $w31 = ex_cat($w30, $x2_32, 1);
    $w32 = ex_cat($w31, $x2_31, 1);
    $w33 = ex_cat($w32, $x2_30, 1);
    $w34 = ex_cat($w33, $x2_29, 1);
    $w35 = ex_cat($w34, $x2_28, 1);
    $w36 = ex_cat($w35, $x2_27, 1);
    $w37 = ex_cat($w36, $x2_26, 1);
    $w38 = ex_cat($w37, $x2_25, 1);
    $w39 = ex_cat($w38, $x2_24, 1);
    $w40 = ex_cat($w39, $x2_23, 1);
    $w41 = ex_cat($w40, $x2_22, 1);
    $w42 = ex_cat($w41, $x2_21, 1);
    $w43 = ex_cat($w42, $x2_20, 1);
    $w44 = ex_cat($w43, $x2_19, 1);
    $w45 = ex_cat($w44, $x2_18, 1);
    $w46 = ex_cat($w45, $x2_17, 1);
    $w47 = ex_cat($w46, $x2_16, 1);
    $w48 = ex_cat($w47, $x2_15, 1);
    $w49 = ex_cat($w48, $x2_14, 1);
    $w50 = ex_cat($w49, $x2_13, 1);
    $w51 = ex_cat($w50, $x2_12, 1);
    $w52 = ex_cat($w51, $x2_11, 1);
    $w53 = ex_cat($w52, $x2_10, 1);
    $w54 = ex_cat($w53, $x2_9, 1);
    $w55 = ex_cat($w54, $x2_8, 1);
    $w56 = ex_cat($w55, $k0, 1);
    $w57 = ex_cat($w56, $k0, 1);
    $w58 = ex_cat($w57, $k0, 1);
    $w59 = ex_cat($w58, $k0, 1);
    $w60 = ex_cat($w59, $k0, 1);
    $w61 = ex_cat($w60, $k0, 1);
    $w62 = ex_cat($w61, $k0, 1);
    $w63 = ex_cat($w62, $g146, 1);
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
        $answer = emu_setle_gpr_one_8__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
