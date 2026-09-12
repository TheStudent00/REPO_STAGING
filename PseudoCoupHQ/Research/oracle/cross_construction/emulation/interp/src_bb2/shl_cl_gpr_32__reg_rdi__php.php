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
// one named local per gate, over the term of shl_cl_gpr_32__reg_rdi__php.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) << Concat(0, Extract(4, 0, v1)))
function emu_shl_cl_gpr_32__reg_rdi__php($a, $b) {
    $x0_0 = ex_ext($a, 0, 0);
    $x1_0 = ex_ext($b, 0, 0);
    $x1_1 = ex_ext($b, 1, 1);
    $x1_2 = ex_ext($b, 2, 2);
    $x1_3 = ex_ext($b, 3, 3);
    $x1_4 = ex_ext($b, 4, 4);
    $x0_1 = ex_ext($a, 1, 1);
    $x0_2 = ex_ext($a, 2, 2);
    $x0_3 = ex_ext($a, 3, 3);
    $x0_4 = ex_ext($a, 4, 4);
    $x0_5 = ex_ext($a, 5, 5);
    $x0_6 = ex_ext($a, 6, 6);
    $x0_7 = ex_ext($a, 7, 7);
    $x0_8 = ex_ext($a, 8, 8);
    $x0_9 = ex_ext($a, 9, 9);
    $x0_10 = ex_ext($a, 10, 10);
    $x0_11 = ex_ext($a, 11, 11);
    $x0_12 = ex_ext($a, 12, 12);
    $x0_13 = ex_ext($a, 13, 13);
    $x0_14 = ex_ext($a, 14, 14);
    $x0_15 = ex_ext($a, 15, 15);
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
    $g0 = ($x1_0 ^ 1);
    $g1 = ($x1_1 ^ 1);
    $g2 = ($x1_2 ^ 1);
    $g3 = ($x1_3 ^ 1);
    $g4 = ($x1_4 ^ 1);
    $g5 = ($g4 & $g3);
    $g6 = ($g5 & $g2);
    $g7 = ($g6 & $g1);
    $g8 = ($g7 & $g0);
    $g9 = ($g8 & $x0_0);
    $g10 = ($x1_0 ^ 1);
    $g11 = ($x1_0 & $x0_0);
    $g12 = ($g10 & $x0_1);
    $g13 = ($g11 | $g12);
    $g14 = ($g4 & $g3);
    $g15 = ($g14 & $g2);
    $g16 = ($g15 & $g1);
    $g17 = ($g16 & $g13);
    $g18 = ($x1_0 ^ 1);
    $g19 = ($x1_0 & $x0_1);
    $g20 = ($g18 & $x0_2);
    $g21 = ($g19 | $g20);
    $g22 = ($x0_0 ^ 1);
    $g23 = ($x1_0 | $g22);
    $g24 = ($g23 ^ 1);
    $g25 = ($x1_1 ^ 1);
    $g26 = ($x1_1 & $g24);
    $g27 = ($g25 & $g21);
    $g28 = ($g26 | $g27);
    $g29 = ($g4 & $g3);
    $g30 = ($g29 & $g2);
    $g31 = ($g30 & $g28);
    $g32 = ($x1_0 ^ 1);
    $g33 = ($x1_0 & $x0_2);
    $g34 = ($g32 & $x0_3);
    $g35 = ($g33 | $g34);
    $g36 = ($x1_1 ^ 1);
    $g37 = ($x1_1 & $g13);
    $g38 = ($g36 & $g35);
    $g39 = ($g37 | $g38);
    $g40 = ($g4 & $g3);
    $g41 = ($g40 & $g2);
    $g42 = ($g41 & $g39);
    $g43 = ($x1_0 ^ 1);
    $g44 = ($x1_0 & $x0_3);
    $g45 = ($g43 & $x0_4);
    $g46 = ($g44 | $g45);
    $g47 = ($x1_1 ^ 1);
    $g48 = ($x1_1 & $g21);
    $g49 = ($g47 & $g46);
    $g50 = ($g48 | $g49);
    $g51 = ($x1_1 | $g23);
    $g52 = ($g51 ^ 1);
    $g53 = ($x1_2 ^ 1);
    $g54 = ($x1_2 & $g52);
    $g55 = ($g53 & $g50);
    $g56 = ($g54 | $g55);
    $g57 = ($g4 & $g3);
    $g58 = ($g57 & $g56);
    $g59 = ($x1_0 ^ 1);
    $g60 = ($x1_0 & $x0_4);
    $g61 = ($g59 & $x0_5);
    $g62 = ($g60 | $g61);
    $g63 = ($x1_1 ^ 1);
    $g64 = ($x1_1 & $g35);
    $g65 = ($g63 & $g62);
    $g66 = ($g64 | $g65);
    $g67 = ($g13 ^ 1);
    $g68 = ($x1_1 | $g67);
    $g69 = ($g68 ^ 1);
    $g70 = ($x1_2 ^ 1);
    $g71 = ($x1_2 & $g69);
    $g72 = ($g70 & $g66);
    $g73 = ($g71 | $g72);
    $g74 = ($g4 & $g3);
    $g75 = ($g74 & $g73);
    $g76 = ($x1_0 ^ 1);
    $g77 = ($x1_0 & $x0_5);
    $g78 = ($g76 & $x0_6);
    $g79 = ($g77 | $g78);
    $g80 = ($x1_1 ^ 1);
    $g81 = ($x1_1 & $g46);
    $g82 = ($g80 & $g79);
    $g83 = ($g81 | $g82);
    $g84 = ($x1_2 ^ 1);
    $g85 = ($x1_2 & $g28);
    $g86 = ($g84 & $g83);
    $g87 = ($g85 | $g86);
    $g88 = ($g4 & $g3);
    $g89 = ($g88 & $g87);
    $g90 = ($x1_0 ^ 1);
    $g91 = ($x1_0 & $x0_6);
    $g92 = ($g90 & $x0_7);
    $g93 = ($g91 | $g92);
    $g94 = ($x1_1 ^ 1);
    $g95 = ($x1_1 & $g62);
    $g96 = ($g94 & $g93);
    $g97 = ($g95 | $g96);
    $g98 = ($x1_2 ^ 1);
    $g99 = ($x1_2 & $g39);
    $g100 = ($g98 & $g97);
    $g101 = ($g99 | $g100);
    $g102 = ($g4 & $g3);
    $g103 = ($g102 & $g101);
    $g104 = ($x1_0 ^ 1);
    $g105 = ($x1_0 & $x0_7);
    $g106 = ($g104 & $x0_8);
    $g107 = ($g105 | $g106);
    $g108 = ($x1_1 ^ 1);
    $g109 = ($x1_1 & $g79);
    $g110 = ($g108 & $g107);
    $g111 = ($g109 | $g110);
    $g112 = ($x1_2 ^ 1);
    $g113 = ($x1_2 & $g50);
    $g114 = ($g112 & $g111);
    $g115 = ($g113 | $g114);
    $g116 = ($x1_2 | $g51);
    $g117 = ($g116 ^ 1);
    $g118 = ($x1_3 ^ 1);
    $g119 = ($x1_3 & $g117);
    $g120 = ($g118 & $g115);
    $g121 = ($g119 | $g120);
    $g122 = ($g4 & $g121);
    $g123 = ($x1_0 ^ 1);
    $g124 = ($x1_0 & $x0_8);
    $g125 = ($g123 & $x0_9);
    $g126 = ($g124 | $g125);
    $g127 = ($x1_1 ^ 1);
    $g128 = ($x1_1 & $g93);
    $g129 = ($g127 & $g126);
    $g130 = ($g128 | $g129);
    $g131 = ($x1_2 ^ 1);
    $g132 = ($x1_2 & $g66);
    $g133 = ($g131 & $g130);
    $g134 = ($g132 | $g133);
    $g135 = ($x1_2 | $g68);
    $g136 = ($g135 ^ 1);
    $g137 = ($x1_3 ^ 1);
    $g138 = ($x1_3 & $g136);
    $g139 = ($g137 & $g134);
    $g140 = ($g138 | $g139);
    $g141 = ($g4 & $g140);
    $g142 = ($x1_0 ^ 1);
    $g143 = ($x1_0 & $x0_9);
    $g144 = ($g142 & $x0_10);
    $g145 = ($g143 | $g144);
    $g146 = ($x1_1 ^ 1);
    $g147 = ($x1_1 & $g107);
    $g148 = ($g146 & $g145);
    $g149 = ($g147 | $g148);
    $g150 = ($x1_2 ^ 1);
    $g151 = ($x1_2 & $g83);
    $g152 = ($g150 & $g149);
    $g153 = ($g151 | $g152);
    $g154 = ($g28 ^ 1);
    $g155 = ($x1_2 | $g154);
    $g156 = ($g155 ^ 1);
    $g157 = ($x1_3 ^ 1);
    $g158 = ($x1_3 & $g156);
    $g159 = ($g157 & $g153);
    $g160 = ($g158 | $g159);
    $g161 = ($g4 & $g160);
    $g162 = ($x1_0 ^ 1);
    $g163 = ($x1_0 & $x0_10);
    $g164 = ($g162 & $x0_11);
    $g165 = ($g163 | $g164);
    $g166 = ($x1_1 ^ 1);
    $g167 = ($x1_1 & $g126);
    $g168 = ($g166 & $g165);
    $g169 = ($g167 | $g168);
    $g170 = ($x1_2 ^ 1);
    $g171 = ($x1_2 & $g97);
    $g172 = ($g170 & $g169);
    $g173 = ($g171 | $g172);
    $g174 = ($g39 ^ 1);
    $g175 = ($x1_2 | $g174);
    $g176 = ($g175 ^ 1);
    $g177 = ($x1_3 ^ 1);
    $g178 = ($x1_3 & $g176);
    $g179 = ($g177 & $g173);
    $g180 = ($g178 | $g179);
    $g181 = ($g4 & $g180);
    $g182 = ($x1_0 ^ 1);
    $g183 = ($x1_0 & $x0_11);
    $g184 = ($g182 & $x0_12);
    $g185 = ($g183 | $g184);
    $g186 = ($x1_1 ^ 1);
    $g187 = ($x1_1 & $g145);
    $g188 = ($g186 & $g185);
    $g189 = ($g187 | $g188);
    $g190 = ($x1_2 ^ 1);
    $g191 = ($x1_2 & $g111);
    $g192 = ($g190 & $g189);
    $g193 = ($g191 | $g192);
    $g194 = ($x1_3 ^ 1);
    $g195 = ($x1_3 & $g56);
    $g196 = ($g194 & $g193);
    $g197 = ($g195 | $g196);
    $g198 = ($g4 & $g197);
    $g199 = ($x1_0 ^ 1);
    $g200 = ($x1_0 & $x0_12);
    $g201 = ($g199 & $x0_13);
    $g202 = ($g200 | $g201);
    $g203 = ($x1_1 ^ 1);
    $g204 = ($x1_1 & $g165);
    $g205 = ($g203 & $g202);
    $g206 = ($g204 | $g205);
    $g207 = ($x1_2 ^ 1);
    $g208 = ($x1_2 & $g130);
    $g209 = ($g207 & $g206);
    $g210 = ($g208 | $g209);
    $g211 = ($x1_3 ^ 1);
    $g212 = ($x1_3 & $g73);
    $g213 = ($g211 & $g210);
    $g214 = ($g212 | $g213);
    $g215 = ($g4 & $g214);
    $g216 = ($x1_0 ^ 1);
    $g217 = ($x1_0 & $x0_13);
    $g218 = ($g216 & $x0_14);
    $g219 = ($g217 | $g218);
    $g220 = ($x1_1 ^ 1);
    $g221 = ($x1_1 & $g185);
    $g222 = ($g220 & $g219);
    $g223 = ($g221 | $g222);
    $g224 = ($x1_2 ^ 1);
    $g225 = ($x1_2 & $g149);
    $g226 = ($g224 & $g223);
    $g227 = ($g225 | $g226);
    $g228 = ($x1_3 ^ 1);
    $g229 = ($x1_3 & $g87);
    $g230 = ($g228 & $g227);
    $g231 = ($g229 | $g230);
    $g232 = ($g4 & $g231);
    $g233 = ($x1_0 ^ 1);
    $g234 = ($x1_0 & $x0_14);
    $g235 = ($g233 & $x0_15);
    $g236 = ($g234 | $g235);
    $g237 = ($x1_1 ^ 1);
    $g238 = ($x1_1 & $g202);
    $g239 = ($g237 & $g236);
    $g240 = ($g238 | $g239);
    $g241 = ($x1_2 ^ 1);
    $g242 = ($x1_2 & $g169);
    $g243 = ($g241 & $g240);
    $g244 = ($g242 | $g243);
    $g245 = ($x1_3 ^ 1);
    $g246 = ($x1_3 & $g101);
    $g247 = ($g245 & $g244);
    $g248 = ($g246 | $g247);
    $g249 = ($g4 & $g248);
    $g250 = ($x1_0 ^ 1);
    $g251 = ($x1_0 & $x0_15);
    $g252 = ($g250 & $x0_16);
    $g253 = ($g251 | $g252);
    $g254 = ($x1_1 ^ 1);
    $g255 = ($x1_1 & $g219);
    $g256 = ($g254 & $g253);
    $g257 = ($g255 | $g256);
    $g258 = ($x1_2 ^ 1);
    $g259 = ($x1_2 & $g189);
    $g260 = ($g258 & $g257);
    $g261 = ($g259 | $g260);
    $g262 = ($x1_3 ^ 1);
    $g263 = ($x1_3 & $g115);
    $g264 = ($g262 & $g261);
    $g265 = ($g263 | $g264);
    $g266 = ($x1_3 | $g116);
    $g267 = ($g266 ^ 1);
    $g268 = ($x1_4 ^ 1);
    $g269 = ($x1_4 & $g267);
    $g270 = ($g268 & $g265);
    $g271 = ($g269 | $g270);
    $g272 = ($x1_0 ^ 1);
    $g273 = ($x1_0 & $x0_16);
    $g274 = ($g272 & $x0_17);
    $g275 = ($g273 | $g274);
    $g276 = ($x1_1 ^ 1);
    $g277 = ($x1_1 & $g236);
    $g278 = ($g276 & $g275);
    $g279 = ($g277 | $g278);
    $g280 = ($x1_2 ^ 1);
    $g281 = ($x1_2 & $g206);
    $g282 = ($g280 & $g279);
    $g283 = ($g281 | $g282);
    $g284 = ($x1_3 ^ 1);
    $g285 = ($x1_3 & $g134);
    $g286 = ($g284 & $g283);
    $g287 = ($g285 | $g286);
    $g288 = ($x1_3 | $g135);
    $g289 = ($g288 ^ 1);
    $g290 = ($x1_4 ^ 1);
    $g291 = ($x1_4 & $g289);
    $g292 = ($g290 & $g287);
    $g293 = ($g291 | $g292);
    $g294 = ($x1_0 ^ 1);
    $g295 = ($x1_0 & $x0_17);
    $g296 = ($g294 & $x0_18);
    $g297 = ($g295 | $g296);
    $g298 = ($x1_1 ^ 1);
    $g299 = ($x1_1 & $g253);
    $g300 = ($g298 & $g297);
    $g301 = ($g299 | $g300);
    $g302 = ($x1_2 ^ 1);
    $g303 = ($x1_2 & $g223);
    $g304 = ($g302 & $g301);
    $g305 = ($g303 | $g304);
    $g306 = ($x1_3 ^ 1);
    $g307 = ($x1_3 & $g153);
    $g308 = ($g306 & $g305);
    $g309 = ($g307 | $g308);
    $g310 = ($x1_3 | $g155);
    $g311 = ($g310 ^ 1);
    $g312 = ($x1_4 ^ 1);
    $g313 = ($x1_4 & $g311);
    $g314 = ($g312 & $g309);
    $g315 = ($g313 | $g314);
    $g316 = ($x1_0 ^ 1);
    $g317 = ($x1_0 & $x0_18);
    $g318 = ($g316 & $x0_19);
    $g319 = ($g317 | $g318);
    $g320 = ($x1_1 ^ 1);
    $g321 = ($x1_1 & $g275);
    $g322 = ($g320 & $g319);
    $g323 = ($g321 | $g322);
    $g324 = ($x1_2 ^ 1);
    $g325 = ($x1_2 & $g240);
    $g326 = ($g324 & $g323);
    $g327 = ($g325 | $g326);
    $g328 = ($x1_3 ^ 1);
    $g329 = ($x1_3 & $g173);
    $g330 = ($g328 & $g327);
    $g331 = ($g329 | $g330);
    $g332 = ($x1_3 | $g175);
    $g333 = ($g332 ^ 1);
    $g334 = ($x1_4 ^ 1);
    $g335 = ($x1_4 & $g333);
    $g336 = ($g334 & $g331);
    $g337 = ($g335 | $g336);
    $g338 = ($x1_0 ^ 1);
    $g339 = ($x1_0 & $x0_19);
    $g340 = ($g338 & $x0_20);
    $g341 = ($g339 | $g340);
    $g342 = ($x1_1 ^ 1);
    $g343 = ($x1_1 & $g297);
    $g344 = ($g342 & $g341);
    $g345 = ($g343 | $g344);
    $g346 = ($x1_2 ^ 1);
    $g347 = ($x1_2 & $g257);
    $g348 = ($g346 & $g345);
    $g349 = ($g347 | $g348);
    $g350 = ($x1_3 ^ 1);
    $g351 = ($x1_3 & $g193);
    $g352 = ($g350 & $g349);
    $g353 = ($g351 | $g352);
    $g354 = ($g56 ^ 1);
    $g355 = ($x1_3 | $g354);
    $g356 = ($g355 ^ 1);
    $g357 = ($x1_4 ^ 1);
    $g358 = ($x1_4 & $g356);
    $g359 = ($g357 & $g353);
    $g360 = ($g358 | $g359);
    $g361 = ($x1_0 ^ 1);
    $g362 = ($x1_0 & $x0_20);
    $g363 = ($g361 & $x0_21);
    $g364 = ($g362 | $g363);
    $g365 = ($x1_1 ^ 1);
    $g366 = ($x1_1 & $g319);
    $g367 = ($g365 & $g364);
    $g368 = ($g366 | $g367);
    $g369 = ($x1_2 ^ 1);
    $g370 = ($x1_2 & $g279);
    $g371 = ($g369 & $g368);
    $g372 = ($g370 | $g371);
    $g373 = ($x1_3 ^ 1);
    $g374 = ($x1_3 & $g210);
    $g375 = ($g373 & $g372);
    $g376 = ($g374 | $g375);
    $g377 = ($g73 ^ 1);
    $g378 = ($x1_3 | $g377);
    $g379 = ($g378 ^ 1);
    $g380 = ($x1_4 ^ 1);
    $g381 = ($x1_4 & $g379);
    $g382 = ($g380 & $g376);
    $g383 = ($g381 | $g382);
    $g384 = ($x1_0 ^ 1);
    $g385 = ($x1_0 & $x0_21);
    $g386 = ($g384 & $x0_22);
    $g387 = ($g385 | $g386);
    $g388 = ($x1_1 ^ 1);
    $g389 = ($x1_1 & $g341);
    $g390 = ($g388 & $g387);
    $g391 = ($g389 | $g390);
    $g392 = ($x1_2 ^ 1);
    $g393 = ($x1_2 & $g301);
    $g394 = ($g392 & $g391);
    $g395 = ($g393 | $g394);
    $g396 = ($x1_3 ^ 1);
    $g397 = ($x1_3 & $g227);
    $g398 = ($g396 & $g395);
    $g399 = ($g397 | $g398);
    $g400 = ($g87 ^ 1);
    $g401 = ($x1_3 | $g400);
    $g402 = ($g401 ^ 1);
    $g403 = ($x1_4 ^ 1);
    $g404 = ($x1_4 & $g402);
    $g405 = ($g403 & $g399);
    $g406 = ($g404 | $g405);
    $g407 = ($x1_0 ^ 1);
    $g408 = ($x1_0 & $x0_22);
    $g409 = ($g407 & $x0_23);
    $g410 = ($g408 | $g409);
    $g411 = ($x1_1 ^ 1);
    $g412 = ($x1_1 & $g364);
    $g413 = ($g411 & $g410);
    $g414 = ($g412 | $g413);
    $g415 = ($x1_2 ^ 1);
    $g416 = ($x1_2 & $g323);
    $g417 = ($g415 & $g414);
    $g418 = ($g416 | $g417);
    $g419 = ($x1_3 ^ 1);
    $g420 = ($x1_3 & $g244);
    $g421 = ($g419 & $g418);
    $g422 = ($g420 | $g421);
    $g423 = ($g101 ^ 1);
    $g424 = ($x1_3 | $g423);
    $g425 = ($g424 ^ 1);
    $g426 = ($x1_4 ^ 1);
    $g427 = ($x1_4 & $g425);
    $g428 = ($g426 & $g422);
    $g429 = ($g427 | $g428);
    $g430 = ($x1_0 ^ 1);
    $g431 = ($x1_0 & $x0_23);
    $g432 = ($g430 & $x0_24);
    $g433 = ($g431 | $g432);
    $g434 = ($x1_1 ^ 1);
    $g435 = ($x1_1 & $g387);
    $g436 = ($g434 & $g433);
    $g437 = ($g435 | $g436);
    $g438 = ($x1_2 ^ 1);
    $g439 = ($x1_2 & $g345);
    $g440 = ($g438 & $g437);
    $g441 = ($g439 | $g440);
    $g442 = ($x1_3 ^ 1);
    $g443 = ($x1_3 & $g261);
    $g444 = ($g442 & $g441);
    $g445 = ($g443 | $g444);
    $g446 = ($x1_4 ^ 1);
    $g447 = ($x1_4 & $g121);
    $g448 = ($g446 & $g445);
    $g449 = ($g447 | $g448);
    $g450 = ($x1_0 ^ 1);
    $g451 = ($x1_0 & $x0_24);
    $g452 = ($g450 & $x0_25);
    $g453 = ($g451 | $g452);
    $g454 = ($x1_1 ^ 1);
    $g455 = ($x1_1 & $g410);
    $g456 = ($g454 & $g453);
    $g457 = ($g455 | $g456);
    $g458 = ($x1_2 ^ 1);
    $g459 = ($x1_2 & $g368);
    $g460 = ($g458 & $g457);
    $g461 = ($g459 | $g460);
    $g462 = ($x1_3 ^ 1);
    $g463 = ($x1_3 & $g283);
    $g464 = ($g462 & $g461);
    $g465 = ($g463 | $g464);
    $g466 = ($x1_4 ^ 1);
    $g467 = ($x1_4 & $g140);
    $g468 = ($g466 & $g465);
    $g469 = ($g467 | $g468);
    $g470 = ($x1_0 ^ 1);
    $g471 = ($x1_0 & $x0_25);
    $g472 = ($g470 & $x0_26);
    $g473 = ($g471 | $g472);
    $g474 = ($x1_1 ^ 1);
    $g475 = ($x1_1 & $g433);
    $g476 = ($g474 & $g473);
    $g477 = ($g475 | $g476);
    $g478 = ($x1_2 ^ 1);
    $g479 = ($x1_2 & $g391);
    $g480 = ($g478 & $g477);
    $g481 = ($g479 | $g480);
    $g482 = ($x1_3 ^ 1);
    $g483 = ($x1_3 & $g305);
    $g484 = ($g482 & $g481);
    $g485 = ($g483 | $g484);
    $g486 = ($x1_4 ^ 1);
    $g487 = ($x1_4 & $g160);
    $g488 = ($g486 & $g485);
    $g489 = ($g487 | $g488);
    $g490 = ($x1_0 ^ 1);
    $g491 = ($x1_0 & $x0_26);
    $g492 = ($g490 & $x0_27);
    $g493 = ($g491 | $g492);
    $g494 = ($x1_1 ^ 1);
    $g495 = ($x1_1 & $g453);
    $g496 = ($g494 & $g493);
    $g497 = ($g495 | $g496);
    $g498 = ($x1_2 ^ 1);
    $g499 = ($x1_2 & $g414);
    $g500 = ($g498 & $g497);
    $g501 = ($g499 | $g500);
    $g502 = ($x1_3 ^ 1);
    $g503 = ($x1_3 & $g327);
    $g504 = ($g502 & $g501);
    $g505 = ($g503 | $g504);
    $g506 = ($x1_4 ^ 1);
    $g507 = ($x1_4 & $g180);
    $g508 = ($g506 & $g505);
    $g509 = ($g507 | $g508);
    $g510 = ($x1_0 ^ 1);
    $g511 = ($x1_0 & $x0_27);
    $g512 = ($g510 & $x0_28);
    $g513 = ($g511 | $g512);
    $g514 = ($x1_1 ^ 1);
    $g515 = ($x1_1 & $g473);
    $g516 = ($g514 & $g513);
    $g517 = ($g515 | $g516);
    $g518 = ($x1_2 ^ 1);
    $g519 = ($x1_2 & $g437);
    $g520 = ($g518 & $g517);
    $g521 = ($g519 | $g520);
    $g522 = ($x1_3 ^ 1);
    $g523 = ($x1_3 & $g349);
    $g524 = ($g522 & $g521);
    $g525 = ($g523 | $g524);
    $g526 = ($x1_4 ^ 1);
    $g527 = ($x1_4 & $g197);
    $g528 = ($g526 & $g525);
    $g529 = ($g527 | $g528);
    $g530 = ($x1_0 ^ 1);
    $g531 = ($x1_0 & $x0_28);
    $g532 = ($g530 & $x0_29);
    $g533 = ($g531 | $g532);
    $g534 = ($x1_1 ^ 1);
    $g535 = ($x1_1 & $g493);
    $g536 = ($g534 & $g533);
    $g537 = ($g535 | $g536);
    $g538 = ($x1_2 ^ 1);
    $g539 = ($x1_2 & $g457);
    $g540 = ($g538 & $g537);
    $g541 = ($g539 | $g540);
    $g542 = ($x1_3 ^ 1);
    $g543 = ($x1_3 & $g372);
    $g544 = ($g542 & $g541);
    $g545 = ($g543 | $g544);
    $g546 = ($x1_4 ^ 1);
    $g547 = ($x1_4 & $g214);
    $g548 = ($g546 & $g545);
    $g549 = ($g547 | $g548);
    $g550 = ($x1_0 ^ 1);
    $g551 = ($x1_0 & $x0_29);
    $g552 = ($g550 & $x0_30);
    $g553 = ($g551 | $g552);
    $g554 = ($x1_1 ^ 1);
    $g555 = ($x1_1 & $g513);
    $g556 = ($g554 & $g553);
    $g557 = ($g555 | $g556);
    $g558 = ($x1_2 ^ 1);
    $g559 = ($x1_2 & $g477);
    $g560 = ($g558 & $g557);
    $g561 = ($g559 | $g560);
    $g562 = ($x1_3 ^ 1);
    $g563 = ($x1_3 & $g395);
    $g564 = ($g562 & $g561);
    $g565 = ($g563 | $g564);
    $g566 = ($x1_4 ^ 1);
    $g567 = ($x1_4 & $g231);
    $g568 = ($g566 & $g565);
    $g569 = ($g567 | $g568);
    $g570 = ($x1_0 ^ 1);
    $g571 = ($x1_0 & $x0_30);
    $g572 = ($g570 & $x0_31);
    $g573 = ($g571 | $g572);
    $g574 = ($x1_1 ^ 1);
    $g575 = ($x1_1 & $g533);
    $g576 = ($g574 & $g573);
    $g577 = ($g575 | $g576);
    $g578 = ($x1_2 ^ 1);
    $g579 = ($x1_2 & $g497);
    $g580 = ($g578 & $g577);
    $g581 = ($g579 | $g580);
    $g582 = ($x1_3 ^ 1);
    $g583 = ($x1_3 & $g418);
    $g584 = ($g582 & $g581);
    $g585 = ($g583 | $g584);
    $g586 = ($x1_4 ^ 1);
    $g587 = ($x1_4 & $g248);
    $g588 = ($g586 & $g585);
    $g589 = ($g587 | $g588);
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
    $w33 = ex_cat($w32, $g569, 1);
    $w34 = ex_cat($w33, $g549, 1);
    $w35 = ex_cat($w34, $g529, 1);
    $w36 = ex_cat($w35, $g509, 1);
    $w37 = ex_cat($w36, $g489, 1);
    $w38 = ex_cat($w37, $g469, 1);
    $w39 = ex_cat($w38, $g449, 1);
    $w40 = ex_cat($w39, $g429, 1);
    $w41 = ex_cat($w40, $g406, 1);
    $w42 = ex_cat($w41, $g383, 1);
    $w43 = ex_cat($w42, $g360, 1);
    $w44 = ex_cat($w43, $g337, 1);
    $w45 = ex_cat($w44, $g315, 1);
    $w46 = ex_cat($w45, $g293, 1);
    $w47 = ex_cat($w46, $g271, 1);
    $w48 = ex_cat($w47, $g249, 1);
    $w49 = ex_cat($w48, $g232, 1);
    $w50 = ex_cat($w49, $g215, 1);
    $w51 = ex_cat($w50, $g198, 1);
    $w52 = ex_cat($w51, $g181, 1);
    $w53 = ex_cat($w52, $g161, 1);
    $w54 = ex_cat($w53, $g141, 1);
    $w55 = ex_cat($w54, $g122, 1);
    $w56 = ex_cat($w55, $g103, 1);
    $w57 = ex_cat($w56, $g89, 1);
    $w58 = ex_cat($w57, $g75, 1);
    $w59 = ex_cat($w58, $g58, 1);
    $w60 = ex_cat($w59, $g42, 1);
    $w61 = ex_cat($w60, $g31, 1);
    $w62 = ex_cat($w61, $g17, 1);
    $w63 = ex_cat($w62, $g9, 1);
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
        $answer = emu_shl_cl_gpr_32__reg_rdi__php(...$ints);
        if ($answer < 0) {
            echo sprintf("%s\n", sprintf("%u", $answer));
        } else {
            echo $answer . "\n";
        }
    } catch (Throwable $problem) {
        echo "RAISE:" . get_class($problem) . "\n";
    }
}
