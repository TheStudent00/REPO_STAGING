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
// one named local per gate, over the term of shr_cl_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, LShR(Extract(31, 0, v0), Concat(0, Extract(4, 0, v1))))
function emu_shr_cl_gpr_32__reg_rdi__php($a, $b) {
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
    $x1_4 = ex_ext($b, 4, 4);
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
    $g60 = ($x1_0 ^ 1);
    $g61 = ($x1_0 & $x0_17);
    $g62 = ($g60 & $x0_16);
    $g63 = ($g61 | $g62);
    $g64 = ($x1_0 ^ 1);
    $g65 = ($x1_0 & $x0_19);
    $g66 = ($g64 & $x0_18);
    $g67 = ($g65 | $g66);
    $g68 = ($x1_1 ^ 1);
    $g69 = ($x1_1 & $g67);
    $g70 = ($g68 & $g63);
    $g71 = ($g69 | $g70);
    $g72 = ($x1_0 ^ 1);
    $g73 = ($x1_0 & $x0_21);
    $g74 = ($g72 & $x0_20);
    $g75 = ($g73 | $g74);
    $g76 = ($x1_0 ^ 1);
    $g77 = ($x1_0 & $x0_23);
    $g78 = ($g76 & $x0_22);
    $g79 = ($g77 | $g78);
    $g80 = ($x1_1 ^ 1);
    $g81 = ($x1_1 & $g79);
    $g82 = ($g80 & $g75);
    $g83 = ($g81 | $g82);
    $g84 = ($x1_2 ^ 1);
    $g85 = ($x1_2 & $g83);
    $g86 = ($g84 & $g71);
    $g87 = ($g85 | $g86);
    $g88 = ($x1_0 ^ 1);
    $g89 = ($x1_0 & $x0_25);
    $g90 = ($g88 & $x0_24);
    $g91 = ($g89 | $g90);
    $g92 = ($x1_0 ^ 1);
    $g93 = ($x1_0 & $x0_27);
    $g94 = ($g92 & $x0_26);
    $g95 = ($g93 | $g94);
    $g96 = ($x1_1 ^ 1);
    $g97 = ($x1_1 & $g95);
    $g98 = ($g96 & $g91);
    $g99 = ($g97 | $g98);
    $g100 = ($x1_0 ^ 1);
    $g101 = ($x1_0 & $x0_29);
    $g102 = ($g100 & $x0_28);
    $g103 = ($g101 | $g102);
    $g104 = ($x1_0 ^ 1);
    $g105 = ($x1_0 & $x0_31);
    $g106 = ($g104 & $x0_30);
    $g107 = ($g105 | $g106);
    $g108 = ($x1_1 ^ 1);
    $g109 = ($x1_1 & $g107);
    $g110 = ($g108 & $g103);
    $g111 = ($g109 | $g110);
    $g112 = ($x1_2 ^ 1);
    $g113 = ($x1_2 & $g111);
    $g114 = ($g112 & $g99);
    $g115 = ($g113 | $g114);
    $g116 = ($x1_3 ^ 1);
    $g117 = ($x1_3 & $g115);
    $g118 = ($g116 & $g87);
    $g119 = ($g117 | $g118);
    $g120 = ($x1_4 ^ 1);
    $g121 = ($x1_4 & $g119);
    $g122 = ($g120 & $g59);
    $g123 = ($g121 | $g122);
    $g124 = ($x1_0 ^ 1);
    $g125 = ($x1_0 & $x0_2);
    $g126 = ($g124 & $x0_1);
    $g127 = ($g125 | $g126);
    $g128 = ($x1_0 ^ 1);
    $g129 = ($x1_0 & $x0_4);
    $g130 = ($g128 & $x0_3);
    $g131 = ($g129 | $g130);
    $g132 = ($x1_1 ^ 1);
    $g133 = ($x1_1 & $g131);
    $g134 = ($g132 & $g127);
    $g135 = ($g133 | $g134);
    $g136 = ($x1_0 ^ 1);
    $g137 = ($x1_0 & $x0_6);
    $g138 = ($g136 & $x0_5);
    $g139 = ($g137 | $g138);
    $g140 = ($x1_0 ^ 1);
    $g141 = ($x1_0 & $x0_8);
    $g142 = ($g140 & $x0_7);
    $g143 = ($g141 | $g142);
    $g144 = ($x1_1 ^ 1);
    $g145 = ($x1_1 & $g143);
    $g146 = ($g144 & $g139);
    $g147 = ($g145 | $g146);
    $g148 = ($x1_2 ^ 1);
    $g149 = ($x1_2 & $g147);
    $g150 = ($g148 & $g135);
    $g151 = ($g149 | $g150);
    $g152 = ($x1_0 ^ 1);
    $g153 = ($x1_0 & $x0_10);
    $g154 = ($g152 & $x0_9);
    $g155 = ($g153 | $g154);
    $g156 = ($x1_0 ^ 1);
    $g157 = ($x1_0 & $x0_12);
    $g158 = ($g156 & $x0_11);
    $g159 = ($g157 | $g158);
    $g160 = ($x1_1 ^ 1);
    $g161 = ($x1_1 & $g159);
    $g162 = ($g160 & $g155);
    $g163 = ($g161 | $g162);
    $g164 = ($x1_0 ^ 1);
    $g165 = ($x1_0 & $x0_14);
    $g166 = ($g164 & $x0_13);
    $g167 = ($g165 | $g166);
    $g168 = ($x1_0 ^ 1);
    $g169 = ($x1_0 & $x0_16);
    $g170 = ($g168 & $x0_15);
    $g171 = ($g169 | $g170);
    $g172 = ($x1_1 ^ 1);
    $g173 = ($x1_1 & $g171);
    $g174 = ($g172 & $g167);
    $g175 = ($g173 | $g174);
    $g176 = ($x1_2 ^ 1);
    $g177 = ($x1_2 & $g175);
    $g178 = ($g176 & $g163);
    $g179 = ($g177 | $g178);
    $g180 = ($x1_3 ^ 1);
    $g181 = ($x1_3 & $g179);
    $g182 = ($g180 & $g151);
    $g183 = ($g181 | $g182);
    $g184 = ($x1_0 ^ 1);
    $g185 = ($x1_0 & $x0_18);
    $g186 = ($g184 & $x0_17);
    $g187 = ($g185 | $g186);
    $g188 = ($x1_0 ^ 1);
    $g189 = ($x1_0 & $x0_20);
    $g190 = ($g188 & $x0_19);
    $g191 = ($g189 | $g190);
    $g192 = ($x1_1 ^ 1);
    $g193 = ($x1_1 & $g191);
    $g194 = ($g192 & $g187);
    $g195 = ($g193 | $g194);
    $g196 = ($x1_0 ^ 1);
    $g197 = ($x1_0 & $x0_22);
    $g198 = ($g196 & $x0_21);
    $g199 = ($g197 | $g198);
    $g200 = ($x1_0 ^ 1);
    $g201 = ($x1_0 & $x0_24);
    $g202 = ($g200 & $x0_23);
    $g203 = ($g201 | $g202);
    $g204 = ($x1_1 ^ 1);
    $g205 = ($x1_1 & $g203);
    $g206 = ($g204 & $g199);
    $g207 = ($g205 | $g206);
    $g208 = ($x1_2 ^ 1);
    $g209 = ($x1_2 & $g207);
    $g210 = ($g208 & $g195);
    $g211 = ($g209 | $g210);
    $g212 = ($x1_0 ^ 1);
    $g213 = ($x1_0 & $x0_26);
    $g214 = ($g212 & $x0_25);
    $g215 = ($g213 | $g214);
    $g216 = ($x1_0 ^ 1);
    $g217 = ($x1_0 & $x0_28);
    $g218 = ($g216 & $x0_27);
    $g219 = ($g217 | $g218);
    $g220 = ($x1_1 ^ 1);
    $g221 = ($x1_1 & $g219);
    $g222 = ($g220 & $g215);
    $g223 = ($g221 | $g222);
    $g224 = ($x1_0 ^ 1);
    $g225 = ($x1_0 & $x0_30);
    $g226 = ($g224 & $x0_29);
    $g227 = ($g225 | $g226);
    $g228 = ($x0_31 ^ 1);
    $g229 = ($x1_0 | $g228);
    $g230 = ($g229 ^ 1);
    $g231 = ($x1_1 ^ 1);
    $g232 = ($x1_1 & $g230);
    $g233 = ($g231 & $g227);
    $g234 = ($g232 | $g233);
    $g235 = ($x1_2 ^ 1);
    $g236 = ($x1_2 & $g234);
    $g237 = ($g235 & $g223);
    $g238 = ($g236 | $g237);
    $g239 = ($x1_3 ^ 1);
    $g240 = ($x1_3 & $g238);
    $g241 = ($g239 & $g211);
    $g242 = ($g240 | $g241);
    $g243 = ($x1_4 ^ 1);
    $g244 = ($x1_4 & $g242);
    $g245 = ($g243 & $g183);
    $g246 = ($g244 | $g245);
    $g247 = ($x1_1 ^ 1);
    $g248 = ($x1_1 & $g15);
    $g249 = ($g247 & $g7);
    $g250 = ($g248 | $g249);
    $g251 = ($x1_1 ^ 1);
    $g252 = ($x1_1 & $g31);
    $g253 = ($g251 & $g19);
    $g254 = ($g252 | $g253);
    $g255 = ($x1_2 ^ 1);
    $g256 = ($x1_2 & $g254);
    $g257 = ($g255 & $g250);
    $g258 = ($g256 | $g257);
    $g259 = ($x1_1 ^ 1);
    $g260 = ($x1_1 & $g43);
    $g261 = ($g259 & $g35);
    $g262 = ($g260 | $g261);
    $g263 = ($x1_1 ^ 1);
    $g264 = ($x1_1 & $g63);
    $g265 = ($g263 & $g47);
    $g266 = ($g264 | $g265);
    $g267 = ($x1_2 ^ 1);
    $g268 = ($x1_2 & $g266);
    $g269 = ($g267 & $g262);
    $g270 = ($g268 | $g269);
    $g271 = ($x1_3 ^ 1);
    $g272 = ($x1_3 & $g270);
    $g273 = ($g271 & $g258);
    $g274 = ($g272 | $g273);
    $g275 = ($x1_1 ^ 1);
    $g276 = ($x1_1 & $g75);
    $g277 = ($g275 & $g67);
    $g278 = ($g276 | $g277);
    $g279 = ($x1_1 ^ 1);
    $g280 = ($x1_1 & $g91);
    $g281 = ($g279 & $g79);
    $g282 = ($g280 | $g281);
    $g283 = ($x1_2 ^ 1);
    $g284 = ($x1_2 & $g282);
    $g285 = ($g283 & $g278);
    $g286 = ($g284 | $g285);
    $g287 = ($x1_1 ^ 1);
    $g288 = ($x1_1 & $g103);
    $g289 = ($g287 & $g95);
    $g290 = ($g288 | $g289);
    $g291 = ($g107 ^ 1);
    $g292 = ($x1_1 | $g291);
    $g293 = ($g292 ^ 1);
    $g294 = ($x1_2 ^ 1);
    $g295 = ($x1_2 & $g293);
    $g296 = ($g294 & $g290);
    $g297 = ($g295 | $g296);
    $g298 = ($x1_3 ^ 1);
    $g299 = ($x1_3 & $g297);
    $g300 = ($g298 & $g286);
    $g301 = ($g299 | $g300);
    $g302 = ($x1_4 ^ 1);
    $g303 = ($x1_4 & $g301);
    $g304 = ($g302 & $g274);
    $g305 = ($g303 | $g304);
    $g306 = ($x1_1 ^ 1);
    $g307 = ($x1_1 & $g139);
    $g308 = ($g306 & $g131);
    $g309 = ($g307 | $g308);
    $g310 = ($x1_1 ^ 1);
    $g311 = ($x1_1 & $g155);
    $g312 = ($g310 & $g143);
    $g313 = ($g311 | $g312);
    $g314 = ($x1_2 ^ 1);
    $g315 = ($x1_2 & $g313);
    $g316 = ($g314 & $g309);
    $g317 = ($g315 | $g316);
    $g318 = ($x1_1 ^ 1);
    $g319 = ($x1_1 & $g167);
    $g320 = ($g318 & $g159);
    $g321 = ($g319 | $g320);
    $g322 = ($x1_1 ^ 1);
    $g323 = ($x1_1 & $g187);
    $g324 = ($g322 & $g171);
    $g325 = ($g323 | $g324);
    $g326 = ($x1_2 ^ 1);
    $g327 = ($x1_2 & $g325);
    $g328 = ($g326 & $g321);
    $g329 = ($g327 | $g328);
    $g330 = ($x1_3 ^ 1);
    $g331 = ($x1_3 & $g329);
    $g332 = ($g330 & $g317);
    $g333 = ($g331 | $g332);
    $g334 = ($x1_1 ^ 1);
    $g335 = ($x1_1 & $g199);
    $g336 = ($g334 & $g191);
    $g337 = ($g335 | $g336);
    $g338 = ($x1_1 ^ 1);
    $g339 = ($x1_1 & $g215);
    $g340 = ($g338 & $g203);
    $g341 = ($g339 | $g340);
    $g342 = ($x1_2 ^ 1);
    $g343 = ($x1_2 & $g341);
    $g344 = ($g342 & $g337);
    $g345 = ($g343 | $g344);
    $g346 = ($x1_1 ^ 1);
    $g347 = ($x1_1 & $g227);
    $g348 = ($g346 & $g219);
    $g349 = ($g347 | $g348);
    $g350 = ($x1_1 | $g229);
    $g351 = ($g350 ^ 1);
    $g352 = ($x1_2 ^ 1);
    $g353 = ($x1_2 & $g351);
    $g354 = ($g352 & $g349);
    $g355 = ($g353 | $g354);
    $g356 = ($x1_3 ^ 1);
    $g357 = ($x1_3 & $g355);
    $g358 = ($g356 & $g345);
    $g359 = ($g357 | $g358);
    $g360 = ($x1_4 ^ 1);
    $g361 = ($x1_4 & $g359);
    $g362 = ($g360 & $g333);
    $g363 = ($g361 | $g362);
    $g364 = ($x1_2 ^ 1);
    $g365 = ($x1_2 & $g39);
    $g366 = ($g364 & $g23);
    $g367 = ($g365 | $g366);
    $g368 = ($x1_2 ^ 1);
    $g369 = ($x1_2 & $g71);
    $g370 = ($g368 & $g51);
    $g371 = ($g369 | $g370);
    $g372 = ($x1_3 ^ 1);
    $g373 = ($x1_3 & $g371);
    $g374 = ($g372 & $g367);
    $g375 = ($g373 | $g374);
    $g376 = ($x1_2 ^ 1);
    $g377 = ($x1_2 & $g99);
    $g378 = ($g376 & $g83);
    $g379 = ($g377 | $g378);
    $g380 = ($g111 ^ 1);
    $g381 = ($x1_2 | $g380);
    $g382 = ($g381 ^ 1);
    $g383 = ($x1_3 ^ 1);
    $g384 = ($x1_3 & $g382);
    $g385 = ($g383 & $g379);
    $g386 = ($g384 | $g385);
    $g387 = ($x1_4 ^ 1);
    $g388 = ($x1_4 & $g386);
    $g389 = ($g387 & $g375);
    $g390 = ($g388 | $g389);
    $g391 = ($x1_2 ^ 1);
    $g392 = ($x1_2 & $g163);
    $g393 = ($g391 & $g147);
    $g394 = ($g392 | $g393);
    $g395 = ($x1_2 ^ 1);
    $g396 = ($x1_2 & $g195);
    $g397 = ($g395 & $g175);
    $g398 = ($g396 | $g397);
    $g399 = ($x1_3 ^ 1);
    $g400 = ($x1_3 & $g398);
    $g401 = ($g399 & $g394);
    $g402 = ($g400 | $g401);
    $g403 = ($x1_2 ^ 1);
    $g404 = ($x1_2 & $g223);
    $g405 = ($g403 & $g207);
    $g406 = ($g404 | $g405);
    $g407 = ($g234 ^ 1);
    $g408 = ($x1_2 | $g407);
    $g409 = ($g408 ^ 1);
    $g410 = ($x1_3 ^ 1);
    $g411 = ($x1_3 & $g409);
    $g412 = ($g410 & $g406);
    $g413 = ($g411 | $g412);
    $g414 = ($x1_4 ^ 1);
    $g415 = ($x1_4 & $g413);
    $g416 = ($g414 & $g402);
    $g417 = ($g415 | $g416);
    $g418 = ($x1_2 ^ 1);
    $g419 = ($x1_2 & $g262);
    $g420 = ($g418 & $g254);
    $g421 = ($g419 | $g420);
    $g422 = ($x1_2 ^ 1);
    $g423 = ($x1_2 & $g278);
    $g424 = ($g422 & $g266);
    $g425 = ($g423 | $g424);
    $g426 = ($x1_3 ^ 1);
    $g427 = ($x1_3 & $g425);
    $g428 = ($g426 & $g421);
    $g429 = ($g427 | $g428);
    $g430 = ($x1_2 ^ 1);
    $g431 = ($x1_2 & $g290);
    $g432 = ($g430 & $g282);
    $g433 = ($g431 | $g432);
    $g434 = ($x1_2 | $g292);
    $g435 = ($g434 ^ 1);
    $g436 = ($x1_3 ^ 1);
    $g437 = ($x1_3 & $g435);
    $g438 = ($g436 & $g433);
    $g439 = ($g437 | $g438);
    $g440 = ($x1_4 ^ 1);
    $g441 = ($x1_4 & $g439);
    $g442 = ($g440 & $g429);
    $g443 = ($g441 | $g442);
    $g444 = ($x1_2 ^ 1);
    $g445 = ($x1_2 & $g321);
    $g446 = ($g444 & $g313);
    $g447 = ($g445 | $g446);
    $g448 = ($x1_2 ^ 1);
    $g449 = ($x1_2 & $g337);
    $g450 = ($g448 & $g325);
    $g451 = ($g449 | $g450);
    $g452 = ($x1_3 ^ 1);
    $g453 = ($x1_3 & $g451);
    $g454 = ($g452 & $g447);
    $g455 = ($g453 | $g454);
    $g456 = ($x1_2 ^ 1);
    $g457 = ($x1_2 & $g349);
    $g458 = ($g456 & $g341);
    $g459 = ($g457 | $g458);
    $g460 = ($x1_2 | $g350);
    $g461 = ($g460 ^ 1);
    $g462 = ($x1_3 ^ 1);
    $g463 = ($x1_3 & $g461);
    $g464 = ($g462 & $g459);
    $g465 = ($g463 | $g464);
    $g466 = ($x1_4 ^ 1);
    $g467 = ($x1_4 & $g465);
    $g468 = ($g466 & $g455);
    $g469 = ($g467 | $g468);
    $g470 = ($x1_3 ^ 1);
    $g471 = ($x1_3 & $g87);
    $g472 = ($g470 & $g55);
    $g473 = ($g471 | $g472);
    $g474 = ($g115 ^ 1);
    $g475 = ($x1_3 | $g474);
    $g476 = ($g475 ^ 1);
    $g477 = ($x1_4 ^ 1);
    $g478 = ($x1_4 & $g476);
    $g479 = ($g477 & $g473);
    $g480 = ($g478 | $g479);
    $g481 = ($x1_3 ^ 1);
    $g482 = ($x1_3 & $g211);
    $g483 = ($g481 & $g179);
    $g484 = ($g482 | $g483);
    $g485 = ($g238 ^ 1);
    $g486 = ($x1_3 | $g485);
    $g487 = ($g486 ^ 1);
    $g488 = ($x1_4 ^ 1);
    $g489 = ($x1_4 & $g487);
    $g490 = ($g488 & $g484);
    $g491 = ($g489 | $g490);
    $g492 = ($x1_3 ^ 1);
    $g493 = ($x1_3 & $g286);
    $g494 = ($g492 & $g270);
    $g495 = ($g493 | $g494);
    $g496 = ($g297 ^ 1);
    $g497 = ($x1_3 | $g496);
    $g498 = ($g497 ^ 1);
    $g499 = ($x1_4 ^ 1);
    $g500 = ($x1_4 & $g498);
    $g501 = ($g499 & $g495);
    $g502 = ($g500 | $g501);
    $g503 = ($x1_3 ^ 1);
    $g504 = ($x1_3 & $g345);
    $g505 = ($g503 & $g329);
    $g506 = ($g504 | $g505);
    $g507 = ($g355 ^ 1);
    $g508 = ($x1_3 | $g507);
    $g509 = ($g508 ^ 1);
    $g510 = ($x1_4 ^ 1);
    $g511 = ($x1_4 & $g509);
    $g512 = ($g510 & $g506);
    $g513 = ($g511 | $g512);
    $g514 = ($x1_3 ^ 1);
    $g515 = ($x1_3 & $g379);
    $g516 = ($g514 & $g371);
    $g517 = ($g515 | $g516);
    $g518 = ($x1_3 | $g381);
    $g519 = ($g518 ^ 1);
    $g520 = ($x1_4 ^ 1);
    $g521 = ($x1_4 & $g519);
    $g522 = ($g520 & $g517);
    $g523 = ($g521 | $g522);
    $g524 = ($x1_3 ^ 1);
    $g525 = ($x1_3 & $g406);
    $g526 = ($g524 & $g398);
    $g527 = ($g525 | $g526);
    $g528 = ($x1_3 | $g408);
    $g529 = ($g528 ^ 1);
    $g530 = ($x1_4 ^ 1);
    $g531 = ($x1_4 & $g529);
    $g532 = ($g530 & $g527);
    $g533 = ($g531 | $g532);
    $g534 = ($x1_3 ^ 1);
    $g535 = ($x1_3 & $g433);
    $g536 = ($g534 & $g425);
    $g537 = ($g535 | $g536);
    $g538 = ($x1_3 | $g434);
    $g539 = ($g538 ^ 1);
    $g540 = ($x1_4 ^ 1);
    $g541 = ($x1_4 & $g539);
    $g542 = ($g540 & $g537);
    $g543 = ($g541 | $g542);
    $g544 = ($x1_3 ^ 1);
    $g545 = ($x1_3 & $g459);
    $g546 = ($g544 & $g451);
    $g547 = ($g545 | $g546);
    $g548 = ($x1_3 | $g460);
    $g549 = ($g548 ^ 1);
    $g550 = ($x1_4 ^ 1);
    $g551 = ($x1_4 & $g549);
    $g552 = ($g550 & $g547);
    $g553 = ($g551 | $g552);
    $g554 = ($x1_4 ^ 1);
    $g555 = ($g554 & $g119);
    $g556 = ($g554 & $g242);
    $g557 = ($g554 & $g301);
    $g558 = ($g554 & $g359);
    $g559 = ($g554 & $g386);
    $g560 = ($g554 & $g413);
    $g561 = ($g554 & $g439);
    $g562 = ($g554 & $g465);
    $g563 = ($x1_3 ^ 1);
    $g564 = ($g554 & $g563);
    $g565 = ($g564 & $g115);
    $g566 = ($g554 & $g563);
    $g567 = ($g566 & $g238);
    $g568 = ($g554 & $g563);
    $g569 = ($g568 & $g297);
    $g570 = ($g554 & $g563);
    $g571 = ($g570 & $g355);
    $g572 = ($x1_2 ^ 1);
    $g573 = ($g554 & $g563);
    $g574 = ($g573 & $g572);
    $g575 = ($g574 & $g111);
    $g576 = ($g554 & $g563);
    $g577 = ($g576 & $g572);
    $g578 = ($g577 & $g234);
    $g579 = ($x1_1 ^ 1);
    $g580 = ($g554 & $g563);
    $g581 = ($g580 & $g572);
    $g582 = ($g581 & $g579);
    $g583 = ($g582 & $g107);
    $g584 = ($x1_0 ^ 1);
    $g585 = ($g554 & $g563);
    $g586 = ($g585 & $g572);
    $g587 = ($g586 & $g579);
    $g588 = ($g587 & $g584);
    $g589 = ($g588 & $x0_31);
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
    $w32 = ex_cat($w31, $g589, 1);
    $w33 = ex_cat($w32, $g583, 1);
    $w34 = ex_cat($w33, $g578, 1);
    $w35 = ex_cat($w34, $g575, 1);
    $w36 = ex_cat($w35, $g571, 1);
    $w37 = ex_cat($w36, $g569, 1);
    $w38 = ex_cat($w37, $g567, 1);
    $w39 = ex_cat($w38, $g565, 1);
    $w40 = ex_cat($w39, $g562, 1);
    $w41 = ex_cat($w40, $g561, 1);
    $w42 = ex_cat($w41, $g560, 1);
    $w43 = ex_cat($w42, $g559, 1);
    $w44 = ex_cat($w43, $g558, 1);
    $w45 = ex_cat($w44, $g557, 1);
    $w46 = ex_cat($w45, $g556, 1);
    $w47 = ex_cat($w46, $g555, 1);
    $w48 = ex_cat($w47, $g553, 1);
    $w49 = ex_cat($w48, $g543, 1);
    $w50 = ex_cat($w49, $g533, 1);
    $w51 = ex_cat($w50, $g523, 1);
    $w52 = ex_cat($w51, $g513, 1);
    $w53 = ex_cat($w52, $g502, 1);
    $w54 = ex_cat($w53, $g491, 1);
    $w55 = ex_cat($w54, $g480, 1);
    $w56 = ex_cat($w55, $g469, 1);
    $w57 = ex_cat($w56, $g443, 1);
    $w58 = ex_cat($w57, $g417, 1);
    $w59 = ex_cat($w58, $g390, 1);
    $w60 = ex_cat($w59, $g363, 1);
    $w61 = ex_cat($w60, $g305, 1);
    $w62 = ex_cat($w61, $g246, 1);
    $w63 = ex_cat($w62, $g123, 1);
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
        $answer = emu_shr_cl_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
