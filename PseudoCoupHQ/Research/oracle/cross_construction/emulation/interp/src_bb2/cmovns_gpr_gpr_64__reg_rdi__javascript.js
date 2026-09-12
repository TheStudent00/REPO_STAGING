"use strict";
const view = new DataView(new ArrayBuffer(8));

function m(x, w) { return BigInt.asUintN(w, x); }
function s(x, w) { return BigInt.asIntN(w, x); }
function add(a, b, w) { return m(a + b, w); }
function sub(a, b, w) { return m(a - b, w); }
function mul(a, b, w) { return m(a * b, w); }
function band(a, b, w) { return m(a & b, w); }
function bor(a, b, w) { return m(a | b, w); }
function bxor(a, b, w) { return m(a ^ b, w); }
function bnot(a, w) { return m(~a, w); }
function bneg(a, w) { return m(-a, w); }
function shl(a, n, w) {
    if (n >= BigInt(w)) { return 0n; }
    return m(a << n, w);
}
function lshr(a, n, w) {
    if (n >= BigInt(w)) { return 0n; }
    return m(a, w) >> n;
}
function ashr(a, n, w) {
    const v = s(a, w);
    let k = n;
    if (k >= BigInt(w)) { k = BigInt(w - 1); }
    return m(v >> k, w);
}
function udiv(a, b, w) { return m(m(a, w) / m(b, w), w); }
function urem(a, b, w) { return m(m(a, w) % m(b, w), w); }
function sdiv(a, b, w) { return m(s(a, w) / s(b, w), w); }
function srem(a, b, w) { return m(s(a, w) % s(b, w), w); }
function ult(a, b, w) { return m(a, w) < m(b, w); }
function ule(a, b, w) { return m(a, w) <= m(b, w); }
function ugt(a, b, w) { return m(a, w) > m(b, w); }
function uge(a, b, w) { return m(a, w) >= m(b, w); }
function slt(a, b, w) { return s(a, w) < s(b, w); }
function sle(a, b, w) { return s(a, w) <= s(b, w); }
function sgt(a, b, w) { return s(a, w) > s(b, w); }
function sge(a, b, w) { return s(a, w) >= s(b, w); }
function eq(a, b, w) { return m(a, w) === m(b, w); }
function ne(a, b, w) { return m(a, w) !== m(b, w); }
function cat(hi, lo, lw) { return (hi << BigInt(lw)) | m(lo, lw); }
function ext(x, hi, lo) { return m(x >> BigInt(lo), hi - lo + 1); }
function sext(x, fromw, tow) { return m(s(x, fromw), tow); }
function b2f(x, w) {
    if (w === 32) {
        view.setUint32(0, Number(m(x, 32)), true);
        return view.getFloat32(0, true);
    }
    view.setBigUint64(0, m(x, 64), true);
    return view.getFloat64(0, true);
}
function f2b(f, w) {
    if (w === 32) {
        view.setFloat32(0, f, true);
        return BigInt(view.getUint32(0, true));
    }
    view.setFloat64(0, f, true);
    return view.getBigUint64(0, true);
}
function fadd(a, b, w) { return f2b(b2f(a, w) + b2f(b, w), w); }
function fsub(a, b, w) { return f2b(b2f(a, w) - b2f(b, w), w); }
function fmul(a, b, w) { return f2b(b2f(a, w) * b2f(b, w), w); }
function fdiv(a, b, w) { return f2b(b2f(a, w) / b2f(b, w), w); }
function i2f(x, fromw, w) { return f2b(Number(s(x, fromw)), w); }
function u2f(x, fromw, w) { return f2b(Number(m(x, fromw)), w); }
function fwiden(x, fromw, w) { return f2b(b2f(x, fromw), w); }

// task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
// one named local per gate, over the term of cmovns_gpr_gpr_64__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
function emu_cmovns_gpr_gpr_64__reg_rdi__javascript(a, b, c, d) {
    const x3_0 = ext(d, 0, 0);
    const x1_63 = ext(a, 63, 63);
    const x0_63 = ext(b, 63, 63);
    const x2_0 = ext(c, 0, 0);
    const x3_1 = ext(d, 1, 1);
    const x2_1 = ext(c, 1, 1);
    const x3_2 = ext(d, 2, 2);
    const x2_2 = ext(c, 2, 2);
    const x3_3 = ext(d, 3, 3);
    const x2_3 = ext(c, 3, 3);
    const x3_4 = ext(d, 4, 4);
    const x2_4 = ext(c, 4, 4);
    const x3_5 = ext(d, 5, 5);
    const x2_5 = ext(c, 5, 5);
    const x3_6 = ext(d, 6, 6);
    const x2_6 = ext(c, 6, 6);
    const x3_7 = ext(d, 7, 7);
    const x2_7 = ext(c, 7, 7);
    const x3_8 = ext(d, 8, 8);
    const x2_8 = ext(c, 8, 8);
    const x3_9 = ext(d, 9, 9);
    const x2_9 = ext(c, 9, 9);
    const x3_10 = ext(d, 10, 10);
    const x2_10 = ext(c, 10, 10);
    const x3_11 = ext(d, 11, 11);
    const x2_11 = ext(c, 11, 11);
    const x3_12 = ext(d, 12, 12);
    const x2_12 = ext(c, 12, 12);
    const x3_13 = ext(d, 13, 13);
    const x2_13 = ext(c, 13, 13);
    const x3_14 = ext(d, 14, 14);
    const x2_14 = ext(c, 14, 14);
    const x3_15 = ext(d, 15, 15);
    const x2_15 = ext(c, 15, 15);
    const x3_16 = ext(d, 16, 16);
    const x2_16 = ext(c, 16, 16);
    const x3_17 = ext(d, 17, 17);
    const x2_17 = ext(c, 17, 17);
    const x3_18 = ext(d, 18, 18);
    const x2_18 = ext(c, 18, 18);
    const x3_19 = ext(d, 19, 19);
    const x2_19 = ext(c, 19, 19);
    const x3_20 = ext(d, 20, 20);
    const x2_20 = ext(c, 20, 20);
    const x3_21 = ext(d, 21, 21);
    const x2_21 = ext(c, 21, 21);
    const x3_22 = ext(d, 22, 22);
    const x2_22 = ext(c, 22, 22);
    const x3_23 = ext(d, 23, 23);
    const x2_23 = ext(c, 23, 23);
    const x3_24 = ext(d, 24, 24);
    const x2_24 = ext(c, 24, 24);
    const x3_25 = ext(d, 25, 25);
    const x2_25 = ext(c, 25, 25);
    const x3_26 = ext(d, 26, 26);
    const x2_26 = ext(c, 26, 26);
    const x3_27 = ext(d, 27, 27);
    const x2_27 = ext(c, 27, 27);
    const x3_28 = ext(d, 28, 28);
    const x2_28 = ext(c, 28, 28);
    const x3_29 = ext(d, 29, 29);
    const x2_29 = ext(c, 29, 29);
    const x3_30 = ext(d, 30, 30);
    const x2_30 = ext(c, 30, 30);
    const x3_31 = ext(d, 31, 31);
    const x2_31 = ext(c, 31, 31);
    const x3_32 = ext(d, 32, 32);
    const x2_32 = ext(c, 32, 32);
    const x3_33 = ext(d, 33, 33);
    const x2_33 = ext(c, 33, 33);
    const x3_34 = ext(d, 34, 34);
    const x2_34 = ext(c, 34, 34);
    const x3_35 = ext(d, 35, 35);
    const x2_35 = ext(c, 35, 35);
    const x3_36 = ext(d, 36, 36);
    const x2_36 = ext(c, 36, 36);
    const x3_37 = ext(d, 37, 37);
    const x2_37 = ext(c, 37, 37);
    const x3_38 = ext(d, 38, 38);
    const x2_38 = ext(c, 38, 38);
    const x3_39 = ext(d, 39, 39);
    const x2_39 = ext(c, 39, 39);
    const x3_40 = ext(d, 40, 40);
    const x2_40 = ext(c, 40, 40);
    const x3_41 = ext(d, 41, 41);
    const x2_41 = ext(c, 41, 41);
    const x3_42 = ext(d, 42, 42);
    const x2_42 = ext(c, 42, 42);
    const x3_43 = ext(d, 43, 43);
    const x2_43 = ext(c, 43, 43);
    const x3_44 = ext(d, 44, 44);
    const x2_44 = ext(c, 44, 44);
    const x3_45 = ext(d, 45, 45);
    const x2_45 = ext(c, 45, 45);
    const x3_46 = ext(d, 46, 46);
    const x2_46 = ext(c, 46, 46);
    const x3_47 = ext(d, 47, 47);
    const x2_47 = ext(c, 47, 47);
    const x3_48 = ext(d, 48, 48);
    const x2_48 = ext(c, 48, 48);
    const x3_49 = ext(d, 49, 49);
    const x2_49 = ext(c, 49, 49);
    const x3_50 = ext(d, 50, 50);
    const x2_50 = ext(c, 50, 50);
    const x3_51 = ext(d, 51, 51);
    const x2_51 = ext(c, 51, 51);
    const x3_52 = ext(d, 52, 52);
    const x2_52 = ext(c, 52, 52);
    const x3_53 = ext(d, 53, 53);
    const x2_53 = ext(c, 53, 53);
    const x3_54 = ext(d, 54, 54);
    const x2_54 = ext(c, 54, 54);
    const x3_55 = ext(d, 55, 55);
    const x2_55 = ext(c, 55, 55);
    const x3_56 = ext(d, 56, 56);
    const x2_56 = ext(c, 56, 56);
    const x3_57 = ext(d, 57, 57);
    const x2_57 = ext(c, 57, 57);
    const x3_58 = ext(d, 58, 58);
    const x2_58 = ext(c, 58, 58);
    const x3_59 = ext(d, 59, 59);
    const x2_59 = ext(c, 59, 59);
    const x3_60 = ext(d, 60, 60);
    const x2_60 = ext(c, 60, 60);
    const x3_61 = ext(d, 61, 61);
    const x2_61 = ext(c, 61, 61);
    const x3_62 = ext(d, 62, 62);
    const x2_62 = ext(c, 62, 62);
    const x3_63 = ext(d, 63, 63);
    const x2_63 = ext(c, 63, 63);
    const g0 = (x1_63 ^ 1n);
    const g1 = (x0_63 ^ 1n);
    const g2 = (g1 | g0);
    const g3 = (g2 ^ 1n);
    const g4 = (g3 & x3_0);
    const g5 = (g2 & x2_0);
    const g6 = (g5 | g4);
    const g7 = (g3 & x3_1);
    const g8 = (g2 & x2_1);
    const g9 = (g8 | g7);
    const g10 = (g3 & x3_2);
    const g11 = (g2 & x2_2);
    const g12 = (g11 | g10);
    const g13 = (g3 & x3_3);
    const g14 = (g2 & x2_3);
    const g15 = (g14 | g13);
    const g16 = (g3 & x3_4);
    const g17 = (g2 & x2_4);
    const g18 = (g17 | g16);
    const g19 = (g3 & x3_5);
    const g20 = (g2 & x2_5);
    const g21 = (g20 | g19);
    const g22 = (g3 & x3_6);
    const g23 = (g2 & x2_6);
    const g24 = (g23 | g22);
    const g25 = (g3 & x3_7);
    const g26 = (g2 & x2_7);
    const g27 = (g26 | g25);
    const g28 = (g3 & x3_8);
    const g29 = (g2 & x2_8);
    const g30 = (g29 | g28);
    const g31 = (g3 & x3_9);
    const g32 = (g2 & x2_9);
    const g33 = (g32 | g31);
    const g34 = (g3 & x3_10);
    const g35 = (g2 & x2_10);
    const g36 = (g35 | g34);
    const g37 = (g3 & x3_11);
    const g38 = (g2 & x2_11);
    const g39 = (g38 | g37);
    const g40 = (g3 & x3_12);
    const g41 = (g2 & x2_12);
    const g42 = (g41 | g40);
    const g43 = (g3 & x3_13);
    const g44 = (g2 & x2_13);
    const g45 = (g44 | g43);
    const g46 = (g3 & x3_14);
    const g47 = (g2 & x2_14);
    const g48 = (g47 | g46);
    const g49 = (g3 & x3_15);
    const g50 = (g2 & x2_15);
    const g51 = (g50 | g49);
    const g52 = (g3 & x3_16);
    const g53 = (g2 & x2_16);
    const g54 = (g53 | g52);
    const g55 = (g3 & x3_17);
    const g56 = (g2 & x2_17);
    const g57 = (g56 | g55);
    const g58 = (g3 & x3_18);
    const g59 = (g2 & x2_18);
    const g60 = (g59 | g58);
    const g61 = (g3 & x3_19);
    const g62 = (g2 & x2_19);
    const g63 = (g62 | g61);
    const g64 = (g3 & x3_20);
    const g65 = (g2 & x2_20);
    const g66 = (g65 | g64);
    const g67 = (g3 & x3_21);
    const g68 = (g2 & x2_21);
    const g69 = (g68 | g67);
    const g70 = (g3 & x3_22);
    const g71 = (g2 & x2_22);
    const g72 = (g71 | g70);
    const g73 = (g3 & x3_23);
    const g74 = (g2 & x2_23);
    const g75 = (g74 | g73);
    const g76 = (g3 & x3_24);
    const g77 = (g2 & x2_24);
    const g78 = (g77 | g76);
    const g79 = (g3 & x3_25);
    const g80 = (g2 & x2_25);
    const g81 = (g80 | g79);
    const g82 = (g3 & x3_26);
    const g83 = (g2 & x2_26);
    const g84 = (g83 | g82);
    const g85 = (g3 & x3_27);
    const g86 = (g2 & x2_27);
    const g87 = (g86 | g85);
    const g88 = (g3 & x3_28);
    const g89 = (g2 & x2_28);
    const g90 = (g89 | g88);
    const g91 = (g3 & x3_29);
    const g92 = (g2 & x2_29);
    const g93 = (g92 | g91);
    const g94 = (g3 & x3_30);
    const g95 = (g2 & x2_30);
    const g96 = (g95 | g94);
    const g97 = (g3 & x3_31);
    const g98 = (g2 & x2_31);
    const g99 = (g98 | g97);
    const g100 = (g3 & x3_32);
    const g101 = (g2 & x2_32);
    const g102 = (g101 | g100);
    const g103 = (g3 & x3_33);
    const g104 = (g2 & x2_33);
    const g105 = (g104 | g103);
    const g106 = (g3 & x3_34);
    const g107 = (g2 & x2_34);
    const g108 = (g107 | g106);
    const g109 = (g3 & x3_35);
    const g110 = (g2 & x2_35);
    const g111 = (g110 | g109);
    const g112 = (g3 & x3_36);
    const g113 = (g2 & x2_36);
    const g114 = (g113 | g112);
    const g115 = (g3 & x3_37);
    const g116 = (g2 & x2_37);
    const g117 = (g116 | g115);
    const g118 = (g3 & x3_38);
    const g119 = (g2 & x2_38);
    const g120 = (g119 | g118);
    const g121 = (g3 & x3_39);
    const g122 = (g2 & x2_39);
    const g123 = (g122 | g121);
    const g124 = (g3 & x3_40);
    const g125 = (g2 & x2_40);
    const g126 = (g125 | g124);
    const g127 = (g3 & x3_41);
    const g128 = (g2 & x2_41);
    const g129 = (g128 | g127);
    const g130 = (g3 & x3_42);
    const g131 = (g2 & x2_42);
    const g132 = (g131 | g130);
    const g133 = (g3 & x3_43);
    const g134 = (g2 & x2_43);
    const g135 = (g134 | g133);
    const g136 = (g3 & x3_44);
    const g137 = (g2 & x2_44);
    const g138 = (g137 | g136);
    const g139 = (g3 & x3_45);
    const g140 = (g2 & x2_45);
    const g141 = (g140 | g139);
    const g142 = (g3 & x3_46);
    const g143 = (g2 & x2_46);
    const g144 = (g143 | g142);
    const g145 = (g3 & x3_47);
    const g146 = (g2 & x2_47);
    const g147 = (g146 | g145);
    const g148 = (g3 & x3_48);
    const g149 = (g2 & x2_48);
    const g150 = (g149 | g148);
    const g151 = (g3 & x3_49);
    const g152 = (g2 & x2_49);
    const g153 = (g152 | g151);
    const g154 = (g3 & x3_50);
    const g155 = (g2 & x2_50);
    const g156 = (g155 | g154);
    const g157 = (g3 & x3_51);
    const g158 = (g2 & x2_51);
    const g159 = (g158 | g157);
    const g160 = (g3 & x3_52);
    const g161 = (g2 & x2_52);
    const g162 = (g161 | g160);
    const g163 = (g3 & x3_53);
    const g164 = (g2 & x2_53);
    const g165 = (g164 | g163);
    const g166 = (g3 & x3_54);
    const g167 = (g2 & x2_54);
    const g168 = (g167 | g166);
    const g169 = (g3 & x3_55);
    const g170 = (g2 & x2_55);
    const g171 = (g170 | g169);
    const g172 = (g3 & x3_56);
    const g173 = (g2 & x2_56);
    const g174 = (g173 | g172);
    const g175 = (g3 & x3_57);
    const g176 = (g2 & x2_57);
    const g177 = (g176 | g175);
    const g178 = (g3 & x3_58);
    const g179 = (g2 & x2_58);
    const g180 = (g179 | g178);
    const g181 = (g3 & x3_59);
    const g182 = (g2 & x2_59);
    const g183 = (g182 | g181);
    const g184 = (g3 & x3_60);
    const g185 = (g2 & x2_60);
    const g186 = (g185 | g184);
    const g187 = (g3 & x3_61);
    const g188 = (g2 & x2_61);
    const g189 = (g188 | g187);
    const g190 = (g3 & x3_62);
    const g191 = (g2 & x2_62);
    const g192 = (g191 | g190);
    const g193 = (g3 & x3_63);
    const g194 = (g2 & x2_63);
    const g195 = (g194 | g193);
    const w0 = g195;
    const w1 = cat(w0, g192, 1);
    const w2 = cat(w1, g189, 1);
    const w3 = cat(w2, g186, 1);
    const w4 = cat(w3, g183, 1);
    const w5 = cat(w4, g180, 1);
    const w6 = cat(w5, g177, 1);
    const w7 = cat(w6, g174, 1);
    const w8 = cat(w7, g171, 1);
    const w9 = cat(w8, g168, 1);
    const w10 = cat(w9, g165, 1);
    const w11 = cat(w10, g162, 1);
    const w12 = cat(w11, g159, 1);
    const w13 = cat(w12, g156, 1);
    const w14 = cat(w13, g153, 1);
    const w15 = cat(w14, g150, 1);
    const w16 = cat(w15, g147, 1);
    const w17 = cat(w16, g144, 1);
    const w18 = cat(w17, g141, 1);
    const w19 = cat(w18, g138, 1);
    const w20 = cat(w19, g135, 1);
    const w21 = cat(w20, g132, 1);
    const w22 = cat(w21, g129, 1);
    const w23 = cat(w22, g126, 1);
    const w24 = cat(w23, g123, 1);
    const w25 = cat(w24, g120, 1);
    const w26 = cat(w25, g117, 1);
    const w27 = cat(w26, g114, 1);
    const w28 = cat(w27, g111, 1);
    const w29 = cat(w28, g108, 1);
    const w30 = cat(w29, g105, 1);
    const w31 = cat(w30, g102, 1);
    const w32 = cat(w31, g99, 1);
    const w33 = cat(w32, g96, 1);
    const w34 = cat(w33, g93, 1);
    const w35 = cat(w34, g90, 1);
    const w36 = cat(w35, g87, 1);
    const w37 = cat(w36, g84, 1);
    const w38 = cat(w37, g81, 1);
    const w39 = cat(w38, g78, 1);
    const w40 = cat(w39, g75, 1);
    const w41 = cat(w40, g72, 1);
    const w42 = cat(w41, g69, 1);
    const w43 = cat(w42, g66, 1);
    const w44 = cat(w43, g63, 1);
    const w45 = cat(w44, g60, 1);
    const w46 = cat(w45, g57, 1);
    const w47 = cat(w46, g54, 1);
    const w48 = cat(w47, g51, 1);
    const w49 = cat(w48, g48, 1);
    const w50 = cat(w49, g45, 1);
    const w51 = cat(w50, g42, 1);
    const w52 = cat(w51, g39, 1);
    const w53 = cat(w52, g36, 1);
    const w54 = cat(w53, g33, 1);
    const w55 = cat(w54, g30, 1);
    const w56 = cat(w55, g27, 1);
    const w57 = cat(w56, g24, 1);
    const w58 = cat(w57, g21, 1);
    const w59 = cat(w58, g18, 1);
    const w60 = cat(w59, g15, 1);
    const w61 = cat(w60, g12, 1);
    const w62 = cat(w61, g9, 1);
    const w63 = cat(w62, g6, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_cmovns_gpr_gpr_64__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
