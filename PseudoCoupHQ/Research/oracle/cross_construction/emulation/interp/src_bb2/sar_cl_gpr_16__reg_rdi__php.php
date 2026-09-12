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
// one named local per gate, over the term of sar_cl_gpr_16__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1)))
function emu_sar_cl_gpr_16__reg_rdi__php($a, $b) {
    $x0_0 = ex_ext($a, 0, 0);
    $x0_1 = ex_ext($a, 1, 1);
    $x1_0 = ex_ext($b, 0, 0);
    $x0_2 = ex_ext($a, 2, 2);
    $x0_3 = ex_ext($a, 3, 3);
    $x1_1 = ex_ext($b, 1, 1);
    $x0_4 = ex_ext($a, 4, 4);
    $x0_5 = ex_ext($a, 5, 5);
    $x0_6 = ex_ext($a, 6, 6);
    $x0_7 = ex_ext($a, 7, 7);
    $x1_2 = ex_ext($b, 2, 2);
    $x0_8 = ex_ext($a, 8, 8);
    $x0_9 = ex_ext($a, 9, 9);
    $x0_10 = ex_ext($a, 10, 10);
    $x0_11 = ex_ext($a, 11, 11);
    $x0_12 = ex_ext($a, 12, 12);
    $x0_13 = ex_ext($a, 13, 13);
    $x0_14 = ex_ext($a, 14, 14);
    $x0_15 = ex_ext($a, 15, 15);
    $x1_3 = ex_ext($b, 3, 3);
    $x1_4 = ex_ext($b, 4, 4);
    $x0_16 = ex_ext($a, 16, 16);
    $x0_17 = ex_ext($a, 17, 17);
    $x0_18 = ex_ext($a, 18, 18);
    $x0_19 = ex_ext($a, 19, 19);
    $x0_20 = ex_ext($a, 20, 20);
    $x0_21 = ex_ext($a, 21, 21);
    $x0_22 = ex_ext($a, 22, 22);
    $x0_23 = ex_ext($a, 23, 23);
    $x0_24 = ex_ext($a, 24, 24);
    $x0_25 = ex_ext($a, 25, 25);
    $x0_26 = ex_ext($a, 26, 26);
    $x0_27 = ex_ext($a, 27, 27);
    $x0_28 = ex_ext($a, 28, 28);
    $x0_29 = ex_ext($a, 29, 29);
    $x0_30 = ex_ext($a, 30, 30);
    $x0_31 = ex_ext($a, 31, 31);
    $x0_32 = ex_ext($a, 32, 32);
    $x0_33 = ex_ext($a, 33, 33);
    $x0_34 = ex_ext($a, 34, 34);
    $x0_35 = ex_ext($a, 35, 35);
    $x0_36 = ex_ext($a, 36, 36);
    $x0_37 = ex_ext($a, 37, 37);
    $x0_38 = ex_ext($a, 38, 38);
    $x0_39 = ex_ext($a, 39, 39);
    $x0_40 = ex_ext($a, 40, 40);
    $x0_41 = ex_ext($a, 41, 41);
    $x0_42 = ex_ext($a, 42, 42);
    $x0_43 = ex_ext($a, 43, 43);
    $x0_44 = ex_ext($a, 44, 44);
    $x0_45 = ex_ext($a, 45, 45);
    $x0_46 = ex_ext($a, 46, 46);
    $x0_47 = ex_ext($a, 47, 47);
    $x0_48 = ex_ext($a, 48, 48);
    $x0_49 = ex_ext($a, 49, 49);
    $x0_50 = ex_ext($a, 50, 50);
    $x0_51 = ex_ext($a, 51, 51);
    $x0_52 = ex_ext($a, 52, 52);
    $x0_53 = ex_ext($a, 53, 53);
    $x0_54 = ex_ext($a, 54, 54);
    $x0_55 = ex_ext($a, 55, 55);
    $x0_56 = ex_ext($a, 56, 56);
    $x0_57 = ex_ext($a, 57, 57);
    $x0_58 = ex_ext($a, 58, 58);
    $x0_59 = ex_ext($a, 59, 59);
    $x0_60 = ex_ext($a, 60, 60);
    $x0_61 = ex_ext($a, 61, 61);
    $x0_62 = ex_ext($a, 62, 62);
    $x0_63 = ex_ext($a, 63, 63);
    $g0 = ($x1_0 ^ 1);
    $g1 = ($x1_0 & $x0_1);
    $g2 = ($g0 & $x0_0);
    $g3 = ($g1 | $g2);
    $g4 = ($x1_0 ^ 1);
    $g5 = ($x1_0 & $x0_3);
    $g6 = ($g4 & $x0_2);
    $g7 = ($g5 | $g6);
    $g8 = ($x1_1 ^ 1);
    $g9 = ($x1_1 & $g7);
    $g10 = ($g8 & $g3);
    $g11 = ($g9 | $g10);
    $g12 = ($x1_0 ^ 1);
    $g13 = ($x1_0 & $x0_5);
    $g14 = ($g12 & $x0_4);
    $g15 = ($g13 | $g14);
    $g16 = ($x1_0 ^ 1);
    $g17 = ($x1_0 & $x0_7);
    $g18 = ($g16 & $x0_6);
    $g19 = ($g17 | $g18);
    $g20 = ($x1_1 ^ 1);
    $g21 = ($x1_1 & $g19);
    $g22 = ($g20 & $g15);
    $g23 = ($g21 | $g22);
    $g24 = ($x1_2 ^ 1);
    $g25 = ($x1_2 & $g23);
    $g26 = ($g24 & $g11);
    $g27 = ($g25 | $g26);
    $g28 = ($x1_0 ^ 1);
    $g29 = ($x1_0 & $x0_9);
    $g30 = ($g28 & $x0_8);
    $g31 = ($g29 | $g30);
    $g32 = ($x1_0 ^ 1);
    $g33 = ($x1_0 & $x0_11);
    $g34 = ($g32 & $x0_10);
    $g35 = ($g33 | $g34);
    $g36 = ($x1_1 ^ 1);
    $g37 = ($x1_1 & $g35);
    $g38 = ($g36 & $g31);
    $g39 = ($g37 | $g38);
    $g40 = ($x1_0 ^ 1);
    $g41 = ($x1_0 & $x0_13);
    $g42 = ($g40 & $x0_12);
    $g43 = ($g41 | $g42);
    $g44 = ($x1_0 ^ 1);
    $g45 = ($x1_0 & $x0_15);
    $g46 = ($g44 & $x0_14);
    $g47 = ($g45 | $g46);
    $g48 = ($x1_1 ^ 1);
    $g49 = ($x1_1 & $g47);
    $g50 = ($g48 & $g43);
    $g51 = ($g49 | $g50);
    $g52 = ($x1_2 ^ 1);
    $g53 = ($x1_2 & $g51);
    $g54 = ($g52 & $g39);
    $g55 = ($g53 | $g54);
    $g56 = ($x1_3 ^ 1);
    $g57 = ($x1_3 & $g55);
    $g58 = ($g56 & $g27);
    $g59 = ($g57 | $g58);
    $g60 = ($x1_4 ^ 1);
    $g61 = ($x1_4 & $x0_15);
    $g62 = ($g60 & $g59);
    $g63 = ($g61 | $g62);
    $g64 = ($x1_0 ^ 1);
    $g65 = ($x1_0 & $x0_2);
    $g66 = ($g64 & $x0_1);
    $g67 = ($g65 | $g66);
    $g68 = ($x1_0 ^ 1);
    $g69 = ($x1_0 & $x0_4);
    $g70 = ($g68 & $x0_3);
    $g71 = ($g69 | $g70);
    $g72 = ($x1_1 ^ 1);
    $g73 = ($x1_1 & $g71);
    $g74 = ($g72 & $g67);
    $g75 = ($g73 | $g74);
    $g76 = ($x1_0 ^ 1);
    $g77 = ($x1_0 & $x0_6);
    $g78 = ($g76 & $x0_5);
    $g79 = ($g77 | $g78);
    $g80 = ($x1_0 ^ 1);
    $g81 = ($x1_0 & $x0_8);
    $g82 = ($g80 & $x0_7);
    $g83 = ($g81 | $g82);
    $g84 = ($x1_1 ^ 1);
    $g85 = ($x1_1 & $g83);
    $g86 = ($g84 & $g79);
    $g87 = ($g85 | $g86);
    $g88 = ($x1_2 ^ 1);
    $g89 = ($x1_2 & $g87);
    $g90 = ($g88 & $g75);
    $g91 = ($g89 | $g90);
    $g92 = ($x1_0 ^ 1);
    $g93 = ($x1_0 & $x0_10);
    $g94 = ($g92 & $x0_9);
    $g95 = ($g93 | $g94);
    $g96 = ($x1_0 ^ 1);
    $g97 = ($x1_0 & $x0_12);
    $g98 = ($g96 & $x0_11);
    $g99 = ($g97 | $g98);
    $g100 = ($x1_1 ^ 1);
    $g101 = ($x1_1 & $g99);
    $g102 = ($g100 & $g95);
    $g103 = ($g101 | $g102);
    $g104 = ($x1_0 ^ 1);
    $g105 = ($x1_0 & $x0_14);
    $g106 = ($g104 & $x0_13);
    $g107 = ($g105 | $g106);
    $g108 = ($x1_1 ^ 1);
    $g109 = ($x1_1 & $x0_15);
    $g110 = ($g108 & $g107);
    $g111 = ($g109 | $g110);
    $g112 = ($x1_2 ^ 1);
    $g113 = ($x1_2 & $g111);
    $g114 = ($g112 & $g103);
    $g115 = ($g113 | $g114);
    $g116 = ($x1_3 ^ 1);
    $g117 = ($x1_3 & $g115);
    $g118 = ($g116 & $g91);
    $g119 = ($g117 | $g118);
    $g120 = ($x1_4 ^ 1);
    $g121 = ($x1_4 & $x0_15);
    $g122 = ($g120 & $g119);
    $g123 = ($g121 | $g122);
    $g124 = ($x1_1 ^ 1);
    $g125 = ($x1_1 & $g15);
    $g126 = ($g124 & $g7);
    $g127 = ($g125 | $g126);
    $g128 = ($x1_1 ^ 1);
    $g129 = ($x1_1 & $g31);
    $g130 = ($g128 & $g19);
    $g131 = ($g129 | $g130);
    $g132 = ($x1_2 ^ 1);
    $g133 = ($x1_2 & $g131);
    $g134 = ($g132 & $g127);
    $g135 = ($g133 | $g134);
    $g136 = ($x1_1 ^ 1);
    $g137 = ($x1_1 & $g43);
    $g138 = ($g136 & $g35);
    $g139 = ($g137 | $g138);
    $g140 = ($x1_1 | $x1_0);
    $g141 = ($g140 ^ 1);
    $g142 = ($g140 & $x0_15);
    $g143 = ($g141 & $x0_14);
    $g144 = ($g142 | $g143);
    $g145 = ($x1_2 ^ 1);
    $g146 = ($x1_2 & $g144);
    $g147 = ($g145 & $g139);
    $g148 = ($g146 | $g147);
    $g149 = ($x1_3 ^ 1);
    $g150 = ($x1_3 & $g148);
    $g151 = ($g149 & $g135);
    $g152 = ($g150 | $g151);
    $g153 = ($x1_4 ^ 1);
    $g154 = ($x1_4 & $x0_15);
    $g155 = ($g153 & $g152);
    $g156 = ($g154 | $g155);
    $g157 = ($x1_1 ^ 1);
    $g158 = ($x1_1 & $g79);
    $g159 = ($g157 & $g71);
    $g160 = ($g158 | $g159);
    $g161 = ($x1_1 ^ 1);
    $g162 = ($x1_1 & $g95);
    $g163 = ($g161 & $g83);
    $g164 = ($g162 | $g163);
    $g165 = ($x1_2 ^ 1);
    $g166 = ($x1_2 & $g164);
    $g167 = ($g165 & $g160);
    $g168 = ($g166 | $g167);
    $g169 = ($x1_1 ^ 1);
    $g170 = ($x1_1 & $g107);
    $g171 = ($g169 & $g99);
    $g172 = ($g170 | $g171);
    $g173 = ($x1_2 ^ 1);
    $g174 = ($x1_2 & $x0_15);
    $g175 = ($g173 & $g172);
    $g176 = ($g174 | $g175);
    $g177 = ($x1_3 ^ 1);
    $g178 = ($x1_3 & $g176);
    $g179 = ($g177 & $g168);
    $g180 = ($g178 | $g179);
    $g181 = ($x1_4 ^ 1);
    $g182 = ($x1_4 & $x0_15);
    $g183 = ($g181 & $g180);
    $g184 = ($g182 | $g183);
    $g185 = ($x1_2 ^ 1);
    $g186 = ($x1_2 & $g39);
    $g187 = ($g185 & $g23);
    $g188 = ($g186 | $g187);
    $g189 = ($x1_2 ^ 1);
    $g190 = ($x1_2 & $x0_15);
    $g191 = ($g189 & $g51);
    $g192 = ($g190 | $g191);
    $g193 = ($x1_3 ^ 1);
    $g194 = ($x1_3 & $g192);
    $g195 = ($g193 & $g188);
    $g196 = ($g194 | $g195);
    $g197 = ($x1_4 ^ 1);
    $g198 = ($x1_4 & $x0_15);
    $g199 = ($g197 & $g196);
    $g200 = ($g198 | $g199);
    $g201 = ($x1_2 ^ 1);
    $g202 = ($x1_2 & $g103);
    $g203 = ($g201 & $g87);
    $g204 = ($g202 | $g203);
    $g205 = ($x1_2 | $x1_1);
    $g206 = ($g205 ^ 1);
    $g207 = ($g205 & $x0_15);
    $g208 = ($g206 & $g107);
    $g209 = ($g207 | $g208);
    $g210 = ($x1_3 ^ 1);
    $g211 = ($x1_3 & $g209);
    $g212 = ($g210 & $g204);
    $g213 = ($g211 | $g212);
    $g214 = ($x1_4 ^ 1);
    $g215 = ($x1_4 & $x0_15);
    $g216 = ($g214 & $g213);
    $g217 = ($g215 | $g216);
    $g218 = ($x1_2 ^ 1);
    $g219 = ($x1_2 & $g139);
    $g220 = ($g218 & $g131);
    $g221 = ($g219 | $g220);
    $g222 = ($x1_2 | $g140);
    $g223 = ($g222 ^ 1);
    $g224 = ($g222 & $x0_15);
    $g225 = ($g223 & $x0_14);
    $g226 = ($g224 | $g225);
    $g227 = ($x1_3 ^ 1);
    $g228 = ($x1_3 & $g226);
    $g229 = ($g227 & $g221);
    $g230 = ($g228 | $g229);
    $g231 = ($x1_4 ^ 1);
    $g232 = ($x1_4 & $x0_15);
    $g233 = ($g231 & $g230);
    $g234 = ($g232 | $g233);
    $g235 = ($x1_2 ^ 1);
    $g236 = ($x1_2 & $g172);
    $g237 = ($g235 & $g164);
    $g238 = ($g236 | $g237);
    $g239 = ($x1_4 | $x1_3);
    $g240 = ($g239 ^ 1);
    $g241 = ($g239 & $x0_15);
    $g242 = ($g240 & $g238);
    $g243 = ($g241 | $g242);
    $g244 = ($g239 ^ 1);
    $g245 = ($g239 & $x0_15);
    $g246 = ($g244 & $g55);
    $g247 = ($g245 | $g246);
    $g248 = ($g239 ^ 1);
    $g249 = ($g239 & $x0_15);
    $g250 = ($g248 & $g115);
    $g251 = ($g249 | $g250);
    $g252 = ($g239 ^ 1);
    $g253 = ($g239 & $x0_15);
    $g254 = ($g252 & $g148);
    $g255 = ($g253 | $g254);
    $g256 = ($x1_3 | $x1_2);
    $g257 = ($x1_4 | $g256);
    $g258 = ($g257 ^ 1);
    $g259 = ($g257 & $x0_15);
    $g260 = ($g258 & $g172);
    $g261 = ($g259 | $g260);
    $g262 = ($g257 ^ 1);
    $g263 = ($g257 & $x0_15);
    $g264 = ($g262 & $g51);
    $g265 = ($g263 | $g264);
    $g266 = ($x1_3 | $g205);
    $g267 = ($x1_4 | $g266);
    $g268 = ($g267 ^ 1);
    $g269 = ($g267 & $x0_15);
    $g270 = ($g268 & $g107);
    $g271 = ($g269 | $g270);
    $g272 = ($x1_3 | $g222);
    $g273 = ($x1_4 | $g272);
    $g274 = ($g273 ^ 1);
    $g275 = ($g273 & $x0_15);
    $g276 = ($g274 & $x0_14);
    $g277 = ($g275 | $g276);
    $w0 = $x0_63;
    $w1 = ex_cat($w0, $x0_62, 1);
    $w2 = ex_cat($w1, $x0_61, 1);
    $w3 = ex_cat($w2, $x0_60, 1);
    $w4 = ex_cat($w3, $x0_59, 1);
    $w5 = ex_cat($w4, $x0_58, 1);
    $w6 = ex_cat($w5, $x0_57, 1);
    $w7 = ex_cat($w6, $x0_56, 1);
    $w8 = ex_cat($w7, $x0_55, 1);
    $w9 = ex_cat($w8, $x0_54, 1);
    $w10 = ex_cat($w9, $x0_53, 1);
    $w11 = ex_cat($w10, $x0_52, 1);
    $w12 = ex_cat($w11, $x0_51, 1);
    $w13 = ex_cat($w12, $x0_50, 1);
    $w14 = ex_cat($w13, $x0_49, 1);
    $w15 = ex_cat($w14, $x0_48, 1);
    $w16 = ex_cat($w15, $x0_47, 1);
    $w17 = ex_cat($w16, $x0_46, 1);
    $w18 = ex_cat($w17, $x0_45, 1);
    $w19 = ex_cat($w18, $x0_44, 1);
    $w20 = ex_cat($w19, $x0_43, 1);
    $w21 = ex_cat($w20, $x0_42, 1);
    $w22 = ex_cat($w21, $x0_41, 1);
    $w23 = ex_cat($w22, $x0_40, 1);
    $w24 = ex_cat($w23, $x0_39, 1);
    $w25 = ex_cat($w24, $x0_38, 1);
    $w26 = ex_cat($w25, $x0_37, 1);
    $w27 = ex_cat($w26, $x0_36, 1);
    $w28 = ex_cat($w27, $x0_35, 1);
    $w29 = ex_cat($w28, $x0_34, 1);
    $w30 = ex_cat($w29, $x0_33, 1);
    $w31 = ex_cat($w30, $x0_32, 1);
    $w32 = ex_cat($w31, $x0_31, 1);
    $w33 = ex_cat($w32, $x0_30, 1);
    $w34 = ex_cat($w33, $x0_29, 1);
    $w35 = ex_cat($w34, $x0_28, 1);
    $w36 = ex_cat($w35, $x0_27, 1);
    $w37 = ex_cat($w36, $x0_26, 1);
    $w38 = ex_cat($w37, $x0_25, 1);
    $w39 = ex_cat($w38, $x0_24, 1);
    $w40 = ex_cat($w39, $x0_23, 1);
    $w41 = ex_cat($w40, $x0_22, 1);
    $w42 = ex_cat($w41, $x0_21, 1);
    $w43 = ex_cat($w42, $x0_20, 1);
    $w44 = ex_cat($w43, $x0_19, 1);
    $w45 = ex_cat($w44, $x0_18, 1);
    $w46 = ex_cat($w45, $x0_17, 1);
    $w47 = ex_cat($w46, $x0_16, 1);
    $w48 = ex_cat($w47, $x0_15, 1);
    $w49 = ex_cat($w48, $g277, 1);
    $w50 = ex_cat($w49, $g271, 1);
    $w51 = ex_cat($w50, $g265, 1);
    $w52 = ex_cat($w51, $g261, 1);
    $w53 = ex_cat($w52, $g255, 1);
    $w54 = ex_cat($w53, $g251, 1);
    $w55 = ex_cat($w54, $g247, 1);
    $w56 = ex_cat($w55, $g243, 1);
    $w57 = ex_cat($w56, $g234, 1);
    $w58 = ex_cat($w57, $g217, 1);
    $w59 = ex_cat($w58, $g200, 1);
    $w60 = ex_cat($w59, $g184, 1);
    $w61 = ex_cat($w60, $g156, 1);
    $w62 = ex_cat($w61, $g123, 1);
    $w63 = ex_cat($w62, $g63, 1);
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
        $answer = emu_sar_cl_gpr_16__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
