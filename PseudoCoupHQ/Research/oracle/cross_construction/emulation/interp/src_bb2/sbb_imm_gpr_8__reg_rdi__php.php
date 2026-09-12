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
// one named local per gate, over the term of sbb_imm_gpr_8__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v3), Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3))
function emu_sbb_imm_gpr_8__reg_rdi__php($a, $b, $c, $d) {
    $x3_0 = ex_ext($c, 0, 0);
    $x2_0 = ex_ext($d, 0, 0);
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
    $x3_1 = ex_ext($c, 1, 1);
    $x2_1 = ex_ext($d, 1, 1);
    $x2_2 = ex_ext($d, 2, 2);
    $x3_2 = ex_ext($c, 2, 2);
    $x2_3 = ex_ext($d, 3, 3);
    $x3_3 = ex_ext($c, 3, 3);
    $x2_4 = ex_ext($d, 4, 4);
    $x3_4 = ex_ext($c, 4, 4);
    $x2_5 = ex_ext($d, 5, 5);
    $x3_5 = ex_ext($c, 5, 5);
    $x2_6 = ex_ext($d, 6, 6);
    $x3_6 = ex_ext($c, 6, 6);
    $x2_7 = ex_ext($d, 7, 7);
    $x3_7 = ex_ext($c, 7, 7);
    $x3_8 = ex_ext($c, 8, 8);
    $x3_9 = ex_ext($c, 9, 9);
    $x3_10 = ex_ext($c, 10, 10);
    $x3_11 = ex_ext($c, 11, 11);
    $x3_12 = ex_ext($c, 12, 12);
    $x3_13 = ex_ext($c, 13, 13);
    $x3_14 = ex_ext($c, 14, 14);
    $x3_15 = ex_ext($c, 15, 15);
    $x3_16 = ex_ext($c, 16, 16);
    $x3_17 = ex_ext($c, 17, 17);
    $x3_18 = ex_ext($c, 18, 18);
    $x3_19 = ex_ext($c, 19, 19);
    $x3_20 = ex_ext($c, 20, 20);
    $x3_21 = ex_ext($c, 21, 21);
    $x3_22 = ex_ext($c, 22, 22);
    $x3_23 = ex_ext($c, 23, 23);
    $x3_24 = ex_ext($c, 24, 24);
    $x3_25 = ex_ext($c, 25, 25);
    $x3_26 = ex_ext($c, 26, 26);
    $x3_27 = ex_ext($c, 27, 27);
    $x3_28 = ex_ext($c, 28, 28);
    $x3_29 = ex_ext($c, 29, 29);
    $x3_30 = ex_ext($c, 30, 30);
    $x3_31 = ex_ext($c, 31, 31);
    $x3_32 = ex_ext($c, 32, 32);
    $x3_33 = ex_ext($c, 33, 33);
    $x3_34 = ex_ext($c, 34, 34);
    $x3_35 = ex_ext($c, 35, 35);
    $x3_36 = ex_ext($c, 36, 36);
    $x3_37 = ex_ext($c, 37, 37);
    $x3_38 = ex_ext($c, 38, 38);
    $x3_39 = ex_ext($c, 39, 39);
    $x3_40 = ex_ext($c, 40, 40);
    $x3_41 = ex_ext($c, 41, 41);
    $x3_42 = ex_ext($c, 42, 42);
    $x3_43 = ex_ext($c, 43, 43);
    $x3_44 = ex_ext($c, 44, 44);
    $x3_45 = ex_ext($c, 45, 45);
    $x3_46 = ex_ext($c, 46, 46);
    $x3_47 = ex_ext($c, 47, 47);
    $x3_48 = ex_ext($c, 48, 48);
    $x3_49 = ex_ext($c, 49, 49);
    $x3_50 = ex_ext($c, 50, 50);
    $x3_51 = ex_ext($c, 51, 51);
    $x3_52 = ex_ext($c, 52, 52);
    $x3_53 = ex_ext($c, 53, 53);
    $x3_54 = ex_ext($c, 54, 54);
    $x3_55 = ex_ext($c, 55, 55);
    $x3_56 = ex_ext($c, 56, 56);
    $x3_57 = ex_ext($c, 57, 57);
    $x3_58 = ex_ext($c, 58, 58);
    $x3_59 = ex_ext($c, 59, 59);
    $x3_60 = ex_ext($c, 60, 60);
    $x3_61 = ex_ext($c, 61, 61);
    $x3_62 = ex_ext($c, 62, 62);
    $x3_63 = ex_ext($c, 63, 63);
    $g0 = ($x2_0 ^ $x3_0);
    $g1 = ($g0 ^ 1);
    $g2 = ($x1_0 ^ 1);
    $g3 = ($x0_0 ^ 1);
    $g4 = ($g3 | $g2);
    $g5 = ($x1_1 ^ 1);
    $g6 = ($g5 | $g4);
    $g7 = ($g6 ^ 1);
    $g8 = ($x0_1 ^ 1);
    $g9 = ($g8 | $g4);
    $g10 = ($g9 ^ 1);
    $g11 = ($g8 | $g5);
    $g12 = ($g11 ^ 1);
    $g13 = ($g12 | $g10);
    $g14 = ($g13 | $g7);
    $g15 = ($g14 ^ 1);
    $g16 = ($x1_2 ^ 1);
    $g17 = ($g16 | $g15);
    $g18 = ($g17 ^ 1);
    $g19 = ($x0_2 ^ 1);
    $g20 = ($g19 | $g15);
    $g21 = ($g20 ^ 1);
    $g22 = ($g19 | $g16);
    $g23 = ($g22 ^ 1);
    $g24 = ($g23 | $g21);
    $g25 = ($g24 | $g18);
    $g26 = ($g25 ^ 1);
    $g27 = ($x1_3 ^ 1);
    $g28 = ($g27 | $g26);
    $g29 = ($g28 ^ 1);
    $g30 = ($x0_3 ^ 1);
    $g31 = ($g30 | $g26);
    $g32 = ($g31 ^ 1);
    $g33 = ($g30 | $g27);
    $g34 = ($g33 ^ 1);
    $g35 = ($g34 | $g32);
    $g36 = ($g35 | $g29);
    $g37 = ($g36 ^ 1);
    $g38 = ($x1_4 ^ 1);
    $g39 = ($g38 | $g37);
    $g40 = ($g39 ^ 1);
    $g41 = ($x0_4 ^ 1);
    $g42 = ($g41 | $g37);
    $g43 = ($g42 ^ 1);
    $g44 = ($g41 | $g38);
    $g45 = ($g44 ^ 1);
    $g46 = ($g45 | $g43);
    $g47 = ($g46 | $g40);
    $g48 = ($g47 ^ 1);
    $g49 = ($x1_5 ^ 1);
    $g50 = ($g49 | $g48);
    $g51 = ($g50 ^ 1);
    $g52 = ($x0_5 ^ 1);
    $g53 = ($g52 | $g48);
    $g54 = ($g53 ^ 1);
    $g55 = ($g52 | $g49);
    $g56 = ($g55 ^ 1);
    $g57 = ($g56 | $g54);
    $g58 = ($g57 | $g51);
    $g59 = ($g58 ^ 1);
    $g60 = ($x1_6 ^ 1);
    $g61 = ($g60 | $g59);
    $g62 = ($g61 ^ 1);
    $g63 = ($x0_6 ^ 1);
    $g64 = ($g63 | $g59);
    $g65 = ($g64 ^ 1);
    $g66 = ($g63 | $g60);
    $g67 = ($g66 ^ 1);
    $g68 = ($g67 | $g65);
    $g69 = ($g68 | $g62);
    $g70 = ($g69 ^ 1);
    $g71 = ($x1_7 ^ 1);
    $g72 = ($g71 | $g70);
    $g73 = ($g72 ^ 1);
    $g74 = ($x0_7 ^ 1);
    $g75 = ($g74 | $g70);
    $g76 = ($g75 ^ 1);
    $g77 = ($g74 | $g71);
    $g78 = ($g77 ^ 1);
    $g79 = ($g78 | $g76);
    $g80 = ($g79 | $g73);
    $g81 = ($g80 ^ $g1);
    $g82 = ($g81 ^ 1);
    $g83 = ($x3_0 ^ 1);
    $g84 = ($x2_0 ^ $g80);
    $g85 = ($g84 ^ 1);
    $g86 = ($g85 | $g83);
    $g87 = ($x3_1 ^ $g86);
    $g88 = ($g87 ^ 1);
    $g89 = ($g80 ^ 1);
    $g90 = ($x2_0 ^ 1);
    $g91 = ($g90 | $g89);
    $g92 = ($g80 ^ $g91);
    $g93 = ($g92 ^ 1);
    $g94 = ($x2_0 ^ $x2_1);
    $g95 = ($g94 ^ 1);
    $g96 = ($g95 ^ $g93);
    $g97 = ($g96 ^ 1);
    $g98 = ($g97 ^ $g88);
    $g99 = ($g98 ^ 1);
    $g100 = ($g99 ^ 1);
    $g101 = ($x2_0 | $x2_1);
    $g102 = ($g101 ^ $x2_2);
    $g103 = ($g102 ^ 1);
    $g104 = ($g89 | $g91);
    $g105 = ($g104 ^ 1);
    $g106 = ($g95 | $g91);
    $g107 = ($g106 ^ 1);
    $g108 = ($g89 | $g95);
    $g109 = ($g108 ^ 1);
    $g110 = ($g109 | $g107);
    $g111 = ($g110 | $g105);
    $g112 = ($g80 ^ $g111);
    $g113 = ($g112 ^ 1);
    $g114 = ($g113 ^ $g103);
    $g115 = ($g114 ^ 1);
    $g116 = ($x3_1 ^ 1);
    $g117 = ($g116 | $g86);
    $g118 = ($g117 ^ 1);
    $g119 = ($g97 ^ 1);
    $g120 = ($g119 | $g86);
    $g121 = ($g120 ^ 1);
    $g122 = ($g116 | $g119);
    $g123 = ($g122 ^ 1);
    $g124 = ($g123 | $g121);
    $g125 = ($g124 | $g118);
    $g126 = ($x3_2 ^ $g125);
    $g127 = ($g126 ^ 1);
    $g128 = ($g127 ^ $g115);
    $g129 = ($g128 ^ 1);
    $g130 = ($g129 ^ 1);
    $g131 = ($x2_2 | $g101);
    $g132 = ($g131 ^ $x2_3);
    $g133 = ($g132 ^ 1);
    $g134 = ($g89 | $g103);
    $g135 = ($g134 ^ 1);
    $g136 = ($g111 ^ 1);
    $g137 = ($g136 | $g103);
    $g138 = ($g137 ^ 1);
    $g139 = ($g89 | $g136);
    $g140 = ($g139 ^ 1);
    $g141 = ($g140 | $g138);
    $g142 = ($g141 | $g135);
    $g143 = ($g80 ^ $g142);
    $g144 = ($g143 ^ 1);
    $g145 = ($g144 ^ $g133);
    $g146 = ($g145 ^ 1);
    $g147 = ($x3_2 ^ 1);
    $g148 = ($g115 | $g147);
    $g149 = ($g148 ^ 1);
    $g150 = ($g125 ^ 1);
    $g151 = ($g147 | $g150);
    $g152 = ($g151 ^ 1);
    $g153 = ($g115 | $g150);
    $g154 = ($g153 ^ 1);
    $g155 = ($g154 | $g152);
    $g156 = ($g155 | $g149);
    $g157 = ($x3_3 ^ $g156);
    $g158 = ($g157 ^ 1);
    $g159 = ($g158 ^ $g146);
    $g160 = ($g159 ^ 1);
    $g161 = ($g160 ^ 1);
    $g162 = ($x2_3 | $g131);
    $g163 = ($g162 ^ $x2_4);
    $g164 = ($g163 ^ 1);
    $g165 = ($g142 ^ 1);
    $g166 = ($g89 | $g165);
    $g167 = ($g166 ^ 1);
    $g168 = ($g133 | $g89);
    $g169 = ($g168 ^ 1);
    $g170 = ($g165 | $g133);
    $g171 = ($g170 ^ 1);
    $g172 = ($g171 | $g169);
    $g173 = ($g172 | $g167);
    $g174 = ($g80 ^ $g173);
    $g175 = ($g174 ^ 1);
    $g176 = ($g175 ^ $g164);
    $g177 = ($g176 ^ 1);
    $g178 = ($g156 ^ 1);
    $g179 = ($g178 | $g146);
    $g180 = ($g179 ^ 1);
    $g181 = ($x3_3 ^ 1);
    $g182 = ($g181 | $g146);
    $g183 = ($g182 ^ 1);
    $g184 = ($g181 | $g178);
    $g185 = ($g184 ^ 1);
    $g186 = ($g185 | $g183);
    $g187 = ($g186 | $g180);
    $g188 = ($x3_4 ^ $g187);
    $g189 = ($g188 ^ 1);
    $g190 = ($g189 ^ $g177);
    $g191 = ($g190 ^ 1);
    $g192 = ($g191 ^ 1);
    $g193 = ($x2_4 | $g162);
    $g194 = ($g193 ^ $x2_5);
    $g195 = ($g194 ^ 1);
    $g196 = ($g173 ^ 1);
    $g197 = ($g196 | $g164);
    $g198 = ($g197 ^ 1);
    $g199 = ($g89 | $g196);
    $g200 = ($g199 ^ 1);
    $g201 = ($g89 | $g164);
    $g202 = ($g201 ^ 1);
    $g203 = ($g202 | $g200);
    $g204 = ($g203 | $g198);
    $g205 = ($g80 ^ $g204);
    $g206 = ($g205 ^ 1);
    $g207 = ($g206 ^ $g195);
    $g208 = ($g207 ^ 1);
    $g209 = ($x3_4 ^ 1);
    $g210 = ($g209 | $g177);
    $g211 = ($g210 ^ 1);
    $g212 = ($g187 ^ 1);
    $g213 = ($g209 | $g212);
    $g214 = ($g213 ^ 1);
    $g215 = ($g212 | $g177);
    $g216 = ($g215 ^ 1);
    $g217 = ($g216 | $g214);
    $g218 = ($g217 | $g211);
    $g219 = ($x3_5 ^ $g218);
    $g220 = ($g219 ^ 1);
    $g221 = ($g220 ^ $g208);
    $g222 = ($g221 ^ 1);
    $g223 = ($g222 ^ 1);
    $g224 = ($x2_5 | $g193);
    $g225 = ($g224 ^ $x2_6);
    $g226 = ($g225 ^ 1);
    $g227 = ($g204 ^ 1);
    $g228 = ($g89 | $g227);
    $g229 = ($g228 ^ 1);
    $g230 = ($g195 | $g89);
    $g231 = ($g230 ^ 1);
    $g232 = ($g195 | $g227);
    $g233 = ($g232 ^ 1);
    $g234 = ($g233 | $g231);
    $g235 = ($g234 | $g229);
    $g236 = ($g80 ^ $g235);
    $g237 = ($g236 ^ 1);
    $g238 = ($g237 ^ $g226);
    $g239 = ($g238 ^ 1);
    $g240 = ($g218 ^ 1);
    $g241 = ($g240 | $g208);
    $g242 = ($g241 ^ 1);
    $g243 = ($x3_5 ^ 1);
    $g244 = ($g243 | $g240);
    $g245 = ($g244 ^ 1);
    $g246 = ($g243 | $g208);
    $g247 = ($g246 ^ 1);
    $g248 = ($g247 | $g245);
    $g249 = ($g248 | $g242);
    $g250 = ($x3_6 ^ $g249);
    $g251 = ($g250 ^ 1);
    $g252 = ($g251 ^ $g239);
    $g253 = ($g252 ^ 1);
    $g254 = ($g253 ^ 1);
    $g255 = ($x2_6 | $g224);
    $g256 = ($g255 ^ $x2_7);
    $g257 = ($g256 ^ 1);
    $g258 = ($g226 | $g89);
    $g259 = ($g258 ^ 1);
    $g260 = ($g235 ^ 1);
    $g261 = ($g226 | $g260);
    $g262 = ($g261 ^ 1);
    $g263 = ($g89 | $g260);
    $g264 = ($g263 ^ 1);
    $g265 = ($g264 | $g262);
    $g266 = ($g265 | $g259);
    $g267 = ($g80 ^ $g266);
    $g268 = ($g267 ^ 1);
    $g269 = ($g268 ^ $g257);
    $g270 = ($g269 ^ 1);
    $g271 = ($x3_6 ^ 1);
    $g272 = ($g271 | $g239);
    $g273 = ($g272 ^ 1);
    $g274 = ($g249 ^ 1);
    $g275 = ($g274 | $g239);
    $g276 = ($g275 ^ 1);
    $g277 = ($g271 | $g274);
    $g278 = ($g277 ^ 1);
    $g279 = ($g278 | $g276);
    $g280 = ($g279 | $g273);
    $g281 = ($x3_7 ^ $g280);
    $g282 = ($g281 ^ 1);
    $g283 = ($g282 ^ $g270);
    $g284 = ($g283 ^ 1);
    $g285 = ($g284 ^ 1);
    $w0 = $x3_63;
    $w1 = ex_cat($w0, $x3_62, 1);
    $w2 = ex_cat($w1, $x3_61, 1);
    $w3 = ex_cat($w2, $x3_60, 1);
    $w4 = ex_cat($w3, $x3_59, 1);
    $w5 = ex_cat($w4, $x3_58, 1);
    $w6 = ex_cat($w5, $x3_57, 1);
    $w7 = ex_cat($w6, $x3_56, 1);
    $w8 = ex_cat($w7, $x3_55, 1);
    $w9 = ex_cat($w8, $x3_54, 1);
    $w10 = ex_cat($w9, $x3_53, 1);
    $w11 = ex_cat($w10, $x3_52, 1);
    $w12 = ex_cat($w11, $x3_51, 1);
    $w13 = ex_cat($w12, $x3_50, 1);
    $w14 = ex_cat($w13, $x3_49, 1);
    $w15 = ex_cat($w14, $x3_48, 1);
    $w16 = ex_cat($w15, $x3_47, 1);
    $w17 = ex_cat($w16, $x3_46, 1);
    $w18 = ex_cat($w17, $x3_45, 1);
    $w19 = ex_cat($w18, $x3_44, 1);
    $w20 = ex_cat($w19, $x3_43, 1);
    $w21 = ex_cat($w20, $x3_42, 1);
    $w22 = ex_cat($w21, $x3_41, 1);
    $w23 = ex_cat($w22, $x3_40, 1);
    $w24 = ex_cat($w23, $x3_39, 1);
    $w25 = ex_cat($w24, $x3_38, 1);
    $w26 = ex_cat($w25, $x3_37, 1);
    $w27 = ex_cat($w26, $x3_36, 1);
    $w28 = ex_cat($w27, $x3_35, 1);
    $w29 = ex_cat($w28, $x3_34, 1);
    $w30 = ex_cat($w29, $x3_33, 1);
    $w31 = ex_cat($w30, $x3_32, 1);
    $w32 = ex_cat($w31, $x3_31, 1);
    $w33 = ex_cat($w32, $x3_30, 1);
    $w34 = ex_cat($w33, $x3_29, 1);
    $w35 = ex_cat($w34, $x3_28, 1);
    $w36 = ex_cat($w35, $x3_27, 1);
    $w37 = ex_cat($w36, $x3_26, 1);
    $w38 = ex_cat($w37, $x3_25, 1);
    $w39 = ex_cat($w38, $x3_24, 1);
    $w40 = ex_cat($w39, $x3_23, 1);
    $w41 = ex_cat($w40, $x3_22, 1);
    $w42 = ex_cat($w41, $x3_21, 1);
    $w43 = ex_cat($w42, $x3_20, 1);
    $w44 = ex_cat($w43, $x3_19, 1);
    $w45 = ex_cat($w44, $x3_18, 1);
    $w46 = ex_cat($w45, $x3_17, 1);
    $w47 = ex_cat($w46, $x3_16, 1);
    $w48 = ex_cat($w47, $x3_15, 1);
    $w49 = ex_cat($w48, $x3_14, 1);
    $w50 = ex_cat($w49, $x3_13, 1);
    $w51 = ex_cat($w50, $x3_12, 1);
    $w52 = ex_cat($w51, $x3_11, 1);
    $w53 = ex_cat($w52, $x3_10, 1);
    $w54 = ex_cat($w53, $x3_9, 1);
    $w55 = ex_cat($w54, $x3_8, 1);
    $w56 = ex_cat($w55, $g285, 1);
    $w57 = ex_cat($w56, $g254, 1);
    $w58 = ex_cat($w57, $g223, 1);
    $w59 = ex_cat($w58, $g192, 1);
    $w60 = ex_cat($w59, $g161, 1);
    $w61 = ex_cat($w60, $g130, 1);
    $w62 = ex_cat($w61, $g100, 1);
    $w63 = ex_cat($w62, $g82, 1);
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
        $answer = emu_sbb_imm_gpr_8__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
