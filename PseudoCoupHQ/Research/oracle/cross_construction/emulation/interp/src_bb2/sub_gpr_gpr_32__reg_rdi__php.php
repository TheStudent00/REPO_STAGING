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
// one named local per gate, over the term of sub_gpr_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1))
function emu_sub_gpr_gpr_32__reg_rdi__php($a, $b) {
    $x0_0 = ex_ext($b, 0, 0);
    $x1_0 = ex_ext($a, 0, 0);
    $x1_1 = ex_ext($a, 1, 1);
    $x0_1 = ex_ext($b, 1, 1);
    $x0_2 = ex_ext($b, 2, 2);
    $x1_2 = ex_ext($a, 2, 2);
    $x0_3 = ex_ext($b, 3, 3);
    $x1_3 = ex_ext($a, 3, 3);
    $x0_4 = ex_ext($b, 4, 4);
    $x1_4 = ex_ext($a, 4, 4);
    $x0_5 = ex_ext($b, 5, 5);
    $x1_5 = ex_ext($a, 5, 5);
    $x0_6 = ex_ext($b, 6, 6);
    $x1_6 = ex_ext($a, 6, 6);
    $x0_7 = ex_ext($b, 7, 7);
    $x1_7 = ex_ext($a, 7, 7);
    $x0_8 = ex_ext($b, 8, 8);
    $x1_8 = ex_ext($a, 8, 8);
    $x0_9 = ex_ext($b, 9, 9);
    $x1_9 = ex_ext($a, 9, 9);
    $x0_10 = ex_ext($b, 10, 10);
    $x1_10 = ex_ext($a, 10, 10);
    $x0_11 = ex_ext($b, 11, 11);
    $x1_11 = ex_ext($a, 11, 11);
    $x0_12 = ex_ext($b, 12, 12);
    $x1_12 = ex_ext($a, 12, 12);
    $x0_13 = ex_ext($b, 13, 13);
    $x1_13 = ex_ext($a, 13, 13);
    $x0_14 = ex_ext($b, 14, 14);
    $x1_14 = ex_ext($a, 14, 14);
    $x0_15 = ex_ext($b, 15, 15);
    $x1_15 = ex_ext($a, 15, 15);
    $x0_16 = ex_ext($b, 16, 16);
    $x1_16 = ex_ext($a, 16, 16);
    $x0_17 = ex_ext($b, 17, 17);
    $x1_17 = ex_ext($a, 17, 17);
    $x0_18 = ex_ext($b, 18, 18);
    $x1_18 = ex_ext($a, 18, 18);
    $x0_19 = ex_ext($b, 19, 19);
    $x1_19 = ex_ext($a, 19, 19);
    $x0_20 = ex_ext($b, 20, 20);
    $x1_20 = ex_ext($a, 20, 20);
    $x0_21 = ex_ext($b, 21, 21);
    $x1_21 = ex_ext($a, 21, 21);
    $x0_22 = ex_ext($b, 22, 22);
    $x1_22 = ex_ext($a, 22, 22);
    $x0_23 = ex_ext($b, 23, 23);
    $x1_23 = ex_ext($a, 23, 23);
    $x0_24 = ex_ext($b, 24, 24);
    $x1_24 = ex_ext($a, 24, 24);
    $x0_25 = ex_ext($b, 25, 25);
    $x1_25 = ex_ext($a, 25, 25);
    $x0_26 = ex_ext($b, 26, 26);
    $x1_26 = ex_ext($a, 26, 26);
    $x0_27 = ex_ext($b, 27, 27);
    $x1_27 = ex_ext($a, 27, 27);
    $x0_28 = ex_ext($b, 28, 28);
    $x1_28 = ex_ext($a, 28, 28);
    $x0_29 = ex_ext($b, 29, 29);
    $x1_29 = ex_ext($a, 29, 29);
    $x0_30 = ex_ext($b, 30, 30);
    $x1_30 = ex_ext($a, 30, 30);
    $x0_31 = ex_ext($b, 31, 31);
    $x1_31 = ex_ext($a, 31, 31);
    $g0 = ($x1_0 ^ $x0_0);
    $g1 = ($g0 ^ 1);
    $g2 = ($g1 ^ 1);
    $g3 = ($x1_0 ^ 1);
    $g4 = ($x0_0 ^ 1);
    $g5 = ($g4 | $g3);
    $g6 = ($x1_1 ^ $g5);
    $g7 = ($g6 ^ 1);
    $g8 = ($x0_0 ^ $x0_1);
    $g9 = ($g8 ^ 1);
    $g10 = ($g9 ^ $g7);
    $g11 = ($g10 ^ 1);
    $g12 = ($x0_1 | $x0_0);
    $g13 = ($g12 ^ $x0_2);
    $g14 = ($g13 ^ 1);
    $g15 = ($x1_1 ^ 1);
    $g16 = ($g15 | $g5);
    $g17 = ($g16 ^ 1);
    $g18 = ($g9 | $g5);
    $g19 = ($g18 ^ 1);
    $g20 = ($g9 | $g15);
    $g21 = ($g20 ^ 1);
    $g22 = ($g21 | $g19);
    $g23 = ($g22 | $g17);
    $g24 = ($x1_2 ^ $g23);
    $g25 = ($g24 ^ 1);
    $g26 = ($g25 ^ $g14);
    $g27 = ($g26 ^ 1);
    $g28 = ($g27 ^ 1);
    $g29 = ($x0_2 | $g12);
    $g30 = ($g29 ^ $x0_3);
    $g31 = ($g30 ^ 1);
    $g32 = ($g23 ^ 1);
    $g33 = ($g14 | $g32);
    $g34 = ($g33 ^ 1);
    $g35 = ($x1_2 ^ 1);
    $g36 = ($g35 | $g14);
    $g37 = ($g36 ^ 1);
    $g38 = ($g35 | $g32);
    $g39 = ($g38 ^ 1);
    $g40 = ($g39 | $g37);
    $g41 = ($g40 | $g34);
    $g42 = ($x1_3 ^ $g41);
    $g43 = ($g42 ^ 1);
    $g44 = ($g43 ^ $g31);
    $g45 = ($g44 ^ 1);
    $g46 = ($g45 ^ 1);
    $g47 = ($x0_3 | $g29);
    $g48 = ($g47 ^ $x0_4);
    $g49 = ($g48 ^ 1);
    $g50 = ($g41 ^ 1);
    $g51 = ($x1_3 ^ 1);
    $g52 = ($g51 | $g50);
    $g53 = ($g52 ^ 1);
    $g54 = ($g51 | $g31);
    $g55 = ($g54 ^ 1);
    $g56 = ($g31 | $g50);
    $g57 = ($g56 ^ 1);
    $g58 = ($g57 | $g55);
    $g59 = ($g58 | $g53);
    $g60 = ($x1_4 ^ $g59);
    $g61 = ($g60 ^ 1);
    $g62 = ($g61 ^ $g49);
    $g63 = ($g62 ^ 1);
    $g64 = ($g63 ^ 1);
    $g65 = ($x0_4 | $g47);
    $g66 = ($g65 ^ $x0_5);
    $g67 = ($g66 ^ 1);
    $g68 = ($g59 ^ 1);
    $g69 = ($x1_4 ^ 1);
    $g70 = ($g69 | $g68);
    $g71 = ($g70 ^ 1);
    $g72 = ($g69 | $g49);
    $g73 = ($g72 ^ 1);
    $g74 = ($g68 | $g49);
    $g75 = ($g74 ^ 1);
    $g76 = ($g75 | $g73);
    $g77 = ($g76 | $g71);
    $g78 = ($x1_5 ^ $g77);
    $g79 = ($g78 ^ 1);
    $g80 = ($g79 ^ $g67);
    $g81 = ($g80 ^ 1);
    $g82 = ($g81 ^ 1);
    $g83 = ($x0_5 | $g65);
    $g84 = ($g83 ^ $x0_6);
    $g85 = ($g84 ^ 1);
    $g86 = ($g77 ^ 1);
    $g87 = ($g86 | $g67);
    $g88 = ($g87 ^ 1);
    $g89 = ($x1_5 ^ 1);
    $g90 = ($g67 | $g89);
    $g91 = ($g90 ^ 1);
    $g92 = ($g89 | $g86);
    $g93 = ($g92 ^ 1);
    $g94 = ($g93 | $g91);
    $g95 = ($g94 | $g88);
    $g96 = ($x1_6 ^ $g95);
    $g97 = ($g96 ^ 1);
    $g98 = ($g97 ^ $g85);
    $g99 = ($g98 ^ 1);
    $g100 = ($g99 ^ 1);
    $g101 = ($x0_6 | $g83);
    $g102 = ($g101 ^ $x0_7);
    $g103 = ($g102 ^ 1);
    $g104 = ($x1_6 ^ 1);
    $g105 = ($g104 | $g85);
    $g106 = ($g105 ^ 1);
    $g107 = ($g95 ^ 1);
    $g108 = ($g104 | $g107);
    $g109 = ($g108 ^ 1);
    $g110 = ($g107 | $g85);
    $g111 = ($g110 ^ 1);
    $g112 = ($g111 | $g109);
    $g113 = ($g112 | $g106);
    $g114 = ($x1_7 ^ $g113);
    $g115 = ($g114 ^ 1);
    $g116 = ($g115 ^ $g103);
    $g117 = ($g116 ^ 1);
    $g118 = ($g117 ^ 1);
    $g119 = ($x0_7 | $g101);
    $g120 = ($g119 ^ $x0_8);
    $g121 = ($g120 ^ 1);
    $g122 = ($g113 ^ 1);
    $g123 = ($x1_7 ^ 1);
    $g124 = ($g123 | $g122);
    $g125 = ($g124 ^ 1);
    $g126 = ($g123 | $g103);
    $g127 = ($g126 ^ 1);
    $g128 = ($g122 | $g103);
    $g129 = ($g128 ^ 1);
    $g130 = ($g129 | $g127);
    $g131 = ($g130 | $g125);
    $g132 = ($x1_8 ^ $g131);
    $g133 = ($g132 ^ 1);
    $g134 = ($g133 ^ $g121);
    $g135 = ($g134 ^ 1);
    $g136 = ($g135 ^ 1);
    $g137 = ($x0_8 | $g119);
    $g138 = ($g137 ^ $x0_9);
    $g139 = ($g138 ^ 1);
    $g140 = ($g131 ^ 1);
    $g141 = ($x1_8 ^ 1);
    $g142 = ($g141 | $g140);
    $g143 = ($g142 ^ 1);
    $g144 = ($g121 | $g141);
    $g145 = ($g144 ^ 1);
    $g146 = ($g121 | $g140);
    $g147 = ($g146 ^ 1);
    $g148 = ($g147 | $g145);
    $g149 = ($g148 | $g143);
    $g150 = ($x1_9 ^ $g149);
    $g151 = ($g150 ^ 1);
    $g152 = ($g151 ^ $g139);
    $g153 = ($g152 ^ 1);
    $g154 = ($g153 ^ 1);
    $g155 = ($x0_9 | $g137);
    $g156 = ($g155 ^ $x0_10);
    $g157 = ($g156 ^ 1);
    $g158 = ($g149 ^ 1);
    $g159 = ($g158 | $g139);
    $g160 = ($g159 ^ 1);
    $g161 = ($x1_9 ^ 1);
    $g162 = ($g161 | $g158);
    $g163 = ($g162 ^ 1);
    $g164 = ($g161 | $g139);
    $g165 = ($g164 ^ 1);
    $g166 = ($g165 | $g163);
    $g167 = ($g166 | $g160);
    $g168 = ($x1_10 ^ $g167);
    $g169 = ($g168 ^ 1);
    $g170 = ($g169 ^ $g157);
    $g171 = ($g170 ^ 1);
    $g172 = ($g171 ^ 1);
    $g173 = ($x0_10 | $g155);
    $g174 = ($g173 ^ $x0_11);
    $g175 = ($g174 ^ 1);
    $g176 = ($g167 ^ 1);
    $g177 = ($g157 | $g176);
    $g178 = ($g177 ^ 1);
    $g179 = ($x1_10 ^ 1);
    $g180 = ($g179 | $g176);
    $g181 = ($g180 ^ 1);
    $g182 = ($g157 | $g179);
    $g183 = ($g182 ^ 1);
    $g184 = ($g183 | $g181);
    $g185 = ($g184 | $g178);
    $g186 = ($x1_11 ^ $g185);
    $g187 = ($g186 ^ 1);
    $g188 = ($g187 ^ $g175);
    $g189 = ($g188 ^ 1);
    $g190 = ($g189 ^ 1);
    $g191 = ($x0_11 | $g173);
    $g192 = ($g191 ^ $x0_12);
    $g193 = ($g192 ^ 1);
    $g194 = ($g185 ^ 1);
    $g195 = ($g194 | $g175);
    $g196 = ($g195 ^ 1);
    $g197 = ($x1_11 ^ 1);
    $g198 = ($g197 | $g194);
    $g199 = ($g198 ^ 1);
    $g200 = ($g175 | $g197);
    $g201 = ($g200 ^ 1);
    $g202 = ($g201 | $g199);
    $g203 = ($g202 | $g196);
    $g204 = ($x1_12 ^ $g203);
    $g205 = ($g204 ^ 1);
    $g206 = ($g205 ^ $g193);
    $g207 = ($g206 ^ 1);
    $g208 = ($g207 ^ 1);
    $g209 = ($x0_12 | $g191);
    $g210 = ($g209 ^ $x0_13);
    $g211 = ($g210 ^ 1);
    $g212 = ($g203 ^ 1);
    $g213 = ($g193 | $g212);
    $g214 = ($g213 ^ 1);
    $g215 = ($x1_12 ^ 1);
    $g216 = ($g215 | $g212);
    $g217 = ($g216 ^ 1);
    $g218 = ($g215 | $g193);
    $g219 = ($g218 ^ 1);
    $g220 = ($g219 | $g217);
    $g221 = ($g220 | $g214);
    $g222 = ($x1_13 ^ $g221);
    $g223 = ($g222 ^ 1);
    $g224 = ($g223 ^ $g211);
    $g225 = ($g224 ^ 1);
    $g226 = ($g225 ^ 1);
    $g227 = ($x0_13 | $g209);
    $g228 = ($g227 ^ $x0_14);
    $g229 = ($g228 ^ 1);
    $g230 = ($g221 ^ 1);
    $g231 = ($x1_13 ^ 1);
    $g232 = ($g231 | $g230);
    $g233 = ($g232 ^ 1);
    $g234 = ($g211 | $g230);
    $g235 = ($g234 ^ 1);
    $g236 = ($g231 | $g211);
    $g237 = ($g236 ^ 1);
    $g238 = ($g237 | $g235);
    $g239 = ($g238 | $g233);
    $g240 = ($x1_14 ^ $g239);
    $g241 = ($g240 ^ 1);
    $g242 = ($g241 ^ $g229);
    $g243 = ($g242 ^ 1);
    $g244 = ($g243 ^ 1);
    $g245 = ($x0_14 | $g227);
    $g246 = ($g245 ^ $x0_15);
    $g247 = ($g246 ^ 1);
    $g248 = ($g239 ^ 1);
    $g249 = ($x1_14 ^ 1);
    $g250 = ($g249 | $g248);
    $g251 = ($g250 ^ 1);
    $g252 = ($g229 | $g248);
    $g253 = ($g252 ^ 1);
    $g254 = ($g229 | $g249);
    $g255 = ($g254 ^ 1);
    $g256 = ($g255 | $g253);
    $g257 = ($g256 | $g251);
    $g258 = ($x1_15 ^ $g257);
    $g259 = ($g258 ^ 1);
    $g260 = ($g259 ^ $g247);
    $g261 = ($g260 ^ 1);
    $g262 = ($g261 ^ 1);
    $g263 = ($x0_15 | $g245);
    $g264 = ($g263 ^ $x0_16);
    $g265 = ($g264 ^ 1);
    $g266 = ($g257 ^ 1);
    $g267 = ($x1_15 ^ 1);
    $g268 = ($g267 | $g266);
    $g269 = ($g268 ^ 1);
    $g270 = ($g247 | $g266);
    $g271 = ($g270 ^ 1);
    $g272 = ($g247 | $g267);
    $g273 = ($g272 ^ 1);
    $g274 = ($g273 | $g271);
    $g275 = ($g274 | $g269);
    $g276 = ($x1_16 ^ $g275);
    $g277 = ($g276 ^ 1);
    $g278 = ($g277 ^ $g265);
    $g279 = ($g278 ^ 1);
    $g280 = ($g279 ^ 1);
    $g281 = ($x0_16 | $g263);
    $g282 = ($g281 ^ $x0_17);
    $g283 = ($g282 ^ 1);
    $g284 = ($g275 ^ 1);
    $g285 = ($x1_16 ^ 1);
    $g286 = ($g285 | $g284);
    $g287 = ($g286 ^ 1);
    $g288 = ($g265 | $g284);
    $g289 = ($g288 ^ 1);
    $g290 = ($g265 | $g285);
    $g291 = ($g290 ^ 1);
    $g292 = ($g291 | $g289);
    $g293 = ($g292 | $g287);
    $g294 = ($x1_17 ^ $g293);
    $g295 = ($g294 ^ 1);
    $g296 = ($g295 ^ $g283);
    $g297 = ($g296 ^ 1);
    $g298 = ($g297 ^ 1);
    $g299 = ($x0_17 | $g281);
    $g300 = ($g299 ^ $x0_18);
    $g301 = ($g300 ^ 1);
    $g302 = ($x1_17 ^ 1);
    $g303 = ($g302 | $g283);
    $g304 = ($g303 ^ 1);
    $g305 = ($g293 ^ 1);
    $g306 = ($g302 | $g305);
    $g307 = ($g306 ^ 1);
    $g308 = ($g283 | $g305);
    $g309 = ($g308 ^ 1);
    $g310 = ($g309 | $g307);
    $g311 = ($g310 | $g304);
    $g312 = ($x1_18 ^ $g311);
    $g313 = ($g312 ^ 1);
    $g314 = ($g313 ^ $g301);
    $g315 = ($g314 ^ 1);
    $g316 = ($g315 ^ 1);
    $g317 = ($x0_18 | $g299);
    $g318 = ($g317 ^ $x0_19);
    $g319 = ($g318 ^ 1);
    $g320 = ($g311 ^ 1);
    $g321 = ($x1_18 ^ 1);
    $g322 = ($g321 | $g320);
    $g323 = ($g322 ^ 1);
    $g324 = ($g301 | $g321);
    $g325 = ($g324 ^ 1);
    $g326 = ($g320 | $g301);
    $g327 = ($g326 ^ 1);
    $g328 = ($g327 | $g325);
    $g329 = ($g328 | $g323);
    $g330 = ($x1_19 ^ $g329);
    $g331 = ($g330 ^ 1);
    $g332 = ($g331 ^ $g319);
    $g333 = ($g332 ^ 1);
    $g334 = ($g333 ^ 1);
    $g335 = ($x0_19 | $g317);
    $g336 = ($g335 ^ $x0_20);
    $g337 = ($g336 ^ 1);
    $g338 = ($x1_19 ^ 1);
    $g339 = ($g319 | $g338);
    $g340 = ($g339 ^ 1);
    $g341 = ($g329 ^ 1);
    $g342 = ($g319 | $g341);
    $g343 = ($g342 ^ 1);
    $g344 = ($g338 | $g341);
    $g345 = ($g344 ^ 1);
    $g346 = ($g345 | $g343);
    $g347 = ($g346 | $g340);
    $g348 = ($x1_20 ^ $g347);
    $g349 = ($g348 ^ 1);
    $g350 = ($g349 ^ $g337);
    $g351 = ($g350 ^ 1);
    $g352 = ($g351 ^ 1);
    $g353 = ($x0_20 | $g335);
    $g354 = ($g353 ^ $x0_21);
    $g355 = ($g354 ^ 1);
    $g356 = ($x1_20 ^ 1);
    $g357 = ($g356 | $g337);
    $g358 = ($g357 ^ 1);
    $g359 = ($g347 ^ 1);
    $g360 = ($g356 | $g359);
    $g361 = ($g360 ^ 1);
    $g362 = ($g359 | $g337);
    $g363 = ($g362 ^ 1);
    $g364 = ($g363 | $g361);
    $g365 = ($g364 | $g358);
    $g366 = ($x1_21 ^ $g365);
    $g367 = ($g366 ^ 1);
    $g368 = ($g367 ^ $g355);
    $g369 = ($g368 ^ 1);
    $g370 = ($g369 ^ 1);
    $g371 = ($x0_21 | $g353);
    $g372 = ($g371 ^ $x0_22);
    $g373 = ($g372 ^ 1);
    $g374 = ($g365 ^ 1);
    $g375 = ($g355 | $g374);
    $g376 = ($g375 ^ 1);
    $g377 = ($x1_21 ^ 1);
    $g378 = ($g355 | $g377);
    $g379 = ($g378 ^ 1);
    $g380 = ($g377 | $g374);
    $g381 = ($g380 ^ 1);
    $g382 = ($g381 | $g379);
    $g383 = ($g382 | $g376);
    $g384 = ($x1_22 ^ $g383);
    $g385 = ($g384 ^ 1);
    $g386 = ($g385 ^ $g373);
    $g387 = ($g386 ^ 1);
    $g388 = ($g387 ^ 1);
    $g389 = ($x0_22 | $g371);
    $g390 = ($g389 ^ $x0_23);
    $g391 = ($g390 ^ 1);
    $g392 = ($g383 ^ 1);
    $g393 = ($x1_22 ^ 1);
    $g394 = ($g393 | $g392);
    $g395 = ($g394 ^ 1);
    $g396 = ($g393 | $g373);
    $g397 = ($g396 ^ 1);
    $g398 = ($g392 | $g373);
    $g399 = ($g398 ^ 1);
    $g400 = ($g399 | $g397);
    $g401 = ($g400 | $g395);
    $g402 = ($x1_23 ^ $g401);
    $g403 = ($g402 ^ 1);
    $g404 = ($g403 ^ $g391);
    $g405 = ($g404 ^ 1);
    $g406 = ($g405 ^ 1);
    $g407 = ($x0_23 | $g389);
    $g408 = ($g407 ^ $x0_24);
    $g409 = ($g408 ^ 1);
    $g410 = ($x1_23 ^ 1);
    $g411 = ($g391 | $g410);
    $g412 = ($g411 ^ 1);
    $g413 = ($g401 ^ 1);
    $g414 = ($g410 | $g413);
    $g415 = ($g414 ^ 1);
    $g416 = ($g391 | $g413);
    $g417 = ($g416 ^ 1);
    $g418 = ($g417 | $g415);
    $g419 = ($g418 | $g412);
    $g420 = ($x1_24 ^ $g419);
    $g421 = ($g420 ^ 1);
    $g422 = ($g421 ^ $g409);
    $g423 = ($g422 ^ 1);
    $g424 = ($g423 ^ 1);
    $g425 = ($x0_24 | $g407);
    $g426 = ($g425 ^ $x0_25);
    $g427 = ($g426 ^ 1);
    $g428 = ($x1_24 ^ 1);
    $g429 = ($g409 | $g428);
    $g430 = ($g429 ^ 1);
    $g431 = ($g419 ^ 1);
    $g432 = ($g428 | $g431);
    $g433 = ($g432 ^ 1);
    $g434 = ($g409 | $g431);
    $g435 = ($g434 ^ 1);
    $g436 = ($g435 | $g433);
    $g437 = ($g436 | $g430);
    $g438 = ($x1_25 ^ $g437);
    $g439 = ($g438 ^ 1);
    $g440 = ($g439 ^ $g427);
    $g441 = ($g440 ^ 1);
    $g442 = ($g441 ^ 1);
    $g443 = ($x0_25 | $g425);
    $g444 = ($g443 ^ $x0_26);
    $g445 = ($g444 ^ 1);
    $g446 = ($x1_25 ^ 1);
    $g447 = ($g427 | $g446);
    $g448 = ($g447 ^ 1);
    $g449 = ($g437 ^ 1);
    $g450 = ($g449 | $g427);
    $g451 = ($g450 ^ 1);
    $g452 = ($g446 | $g449);
    $g453 = ($g452 ^ 1);
    $g454 = ($g453 | $g451);
    $g455 = ($g454 | $g448);
    $g456 = ($x1_26 ^ $g455);
    $g457 = ($g456 ^ 1);
    $g458 = ($g457 ^ $g445);
    $g459 = ($g458 ^ 1);
    $g460 = ($g459 ^ 1);
    $g461 = ($x0_26 | $g443);
    $g462 = ($g461 ^ $x0_27);
    $g463 = ($g462 ^ 1);
    $g464 = ($x1_26 ^ 1);
    $g465 = ($g445 | $g464);
    $g466 = ($g465 ^ 1);
    $g467 = ($g455 ^ 1);
    $g468 = ($g464 | $g467);
    $g469 = ($g468 ^ 1);
    $g470 = ($g445 | $g467);
    $g471 = ($g470 ^ 1);
    $g472 = ($g471 | $g469);
    $g473 = ($g472 | $g466);
    $g474 = ($x1_27 ^ $g473);
    $g475 = ($g474 ^ 1);
    $g476 = ($g475 ^ $g463);
    $g477 = ($g476 ^ 1);
    $g478 = ($g477 ^ 1);
    $g479 = ($x0_27 | $g461);
    $g480 = ($g479 ^ $x0_28);
    $g481 = ($g480 ^ 1);
    $g482 = ($x1_27 ^ 1);
    $g483 = ($g482 | $g463);
    $g484 = ($g483 ^ 1);
    $g485 = ($g473 ^ 1);
    $g486 = ($g482 | $g485);
    $g487 = ($g486 ^ 1);
    $g488 = ($g463 | $g485);
    $g489 = ($g488 ^ 1);
    $g490 = ($g489 | $g487);
    $g491 = ($g490 | $g484);
    $g492 = ($x1_28 ^ $g491);
    $g493 = ($g492 ^ 1);
    $g494 = ($g493 ^ $g481);
    $g495 = ($g494 ^ 1);
    $g496 = ($g495 ^ 1);
    $g497 = ($x0_28 | $g479);
    $g498 = ($g497 ^ $x0_29);
    $g499 = ($g498 ^ 1);
    $g500 = ($x1_28 ^ 1);
    $g501 = ($g481 | $g500);
    $g502 = ($g501 ^ 1);
    $g503 = ($g491 ^ 1);
    $g504 = ($g500 | $g503);
    $g505 = ($g504 ^ 1);
    $g506 = ($g481 | $g503);
    $g507 = ($g506 ^ 1);
    $g508 = ($g507 | $g505);
    $g509 = ($g508 | $g502);
    $g510 = ($x1_29 ^ $g509);
    $g511 = ($g510 ^ 1);
    $g512 = ($g511 ^ $g499);
    $g513 = ($g512 ^ 1);
    $g514 = ($g513 ^ 1);
    $g515 = ($x0_29 | $g497);
    $g516 = ($g515 ^ $x0_30);
    $g517 = ($g516 ^ 1);
    $g518 = ($g509 ^ 1);
    $g519 = ($x1_29 ^ 1);
    $g520 = ($g519 | $g518);
    $g521 = ($g520 ^ 1);
    $g522 = ($g518 | $g499);
    $g523 = ($g522 ^ 1);
    $g524 = ($g499 | $g519);
    $g525 = ($g524 ^ 1);
    $g526 = ($g525 | $g523);
    $g527 = ($g526 | $g521);
    $g528 = ($x1_30 ^ $g527);
    $g529 = ($g528 ^ 1);
    $g530 = ($g529 ^ $g517);
    $g531 = ($g530 ^ 1);
    $g532 = ($g531 ^ 1);
    $g533 = ($x0_30 | $g515);
    $g534 = ($g533 ^ $x0_31);
    $g535 = ($g534 ^ 1);
    $g536 = ($g527 ^ 1);
    $g537 = ($g536 | $g517);
    $g538 = ($g537 ^ 1);
    $g539 = ($x1_30 ^ 1);
    $g540 = ($g539 | $g517);
    $g541 = ($g540 ^ 1);
    $g542 = ($g539 | $g536);
    $g543 = ($g542 ^ 1);
    $g544 = ($g543 | $g541);
    $g545 = ($g544 | $g538);
    $g546 = ($x1_31 ^ $g545);
    $g547 = ($g546 ^ 1);
    $g548 = ($g547 ^ $g535);
    $g549 = ($g548 ^ 1);
    $g550 = ($g549 ^ 1);
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
    $w32 = ex_cat($w31, $g550, 1);
    $w33 = ex_cat($w32, $g532, 1);
    $w34 = ex_cat($w33, $g514, 1);
    $w35 = ex_cat($w34, $g496, 1);
    $w36 = ex_cat($w35, $g478, 1);
    $w37 = ex_cat($w36, $g460, 1);
    $w38 = ex_cat($w37, $g442, 1);
    $w39 = ex_cat($w38, $g424, 1);
    $w40 = ex_cat($w39, $g406, 1);
    $w41 = ex_cat($w40, $g388, 1);
    $w42 = ex_cat($w41, $g370, 1);
    $w43 = ex_cat($w42, $g352, 1);
    $w44 = ex_cat($w43, $g334, 1);
    $w45 = ex_cat($w44, $g316, 1);
    $w46 = ex_cat($w45, $g298, 1);
    $w47 = ex_cat($w46, $g280, 1);
    $w48 = ex_cat($w47, $g262, 1);
    $w49 = ex_cat($w48, $g244, 1);
    $w50 = ex_cat($w49, $g226, 1);
    $w51 = ex_cat($w50, $g208, 1);
    $w52 = ex_cat($w51, $g190, 1);
    $w53 = ex_cat($w52, $g172, 1);
    $w54 = ex_cat($w53, $g154, 1);
    $w55 = ex_cat($w54, $g136, 1);
    $w56 = ex_cat($w55, $g118, 1);
    $w57 = ex_cat($w56, $g100, 1);
    $w58 = ex_cat($w57, $g82, 1);
    $w59 = ex_cat($w58, $g64, 1);
    $w60 = ex_cat($w59, $g46, 1);
    $w61 = ex_cat($w60, $g28, 1);
    $w62 = ex_cat($w61, $g11, 1);
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
        $answer = emu_sub_gpr_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
