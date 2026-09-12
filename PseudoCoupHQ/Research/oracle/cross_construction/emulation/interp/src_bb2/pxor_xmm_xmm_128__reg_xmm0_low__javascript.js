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
// one named local per gate, over the term of pxor_xmm_xmm_128__reg_xmm0_low__javascript.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, v0) ^ Extract(63, 0, v1)
function emu_pxor_xmm_xmm_128__reg_xmm0_low__javascript(a, b) {
    const x1_0 = ext(b, 0, 0);
    const x0_0 = ext(a, 0, 0);
    const x1_1 = ext(b, 1, 1);
    const x0_1 = ext(a, 1, 1);
    const x1_2 = ext(b, 2, 2);
    const x0_2 = ext(a, 2, 2);
    const x1_3 = ext(b, 3, 3);
    const x0_3 = ext(a, 3, 3);
    const x1_4 = ext(b, 4, 4);
    const x0_4 = ext(a, 4, 4);
    const x1_5 = ext(b, 5, 5);
    const x0_5 = ext(a, 5, 5);
    const x1_6 = ext(b, 6, 6);
    const x0_6 = ext(a, 6, 6);
    const x1_7 = ext(b, 7, 7);
    const x0_7 = ext(a, 7, 7);
    const x1_8 = ext(b, 8, 8);
    const x0_8 = ext(a, 8, 8);
    const x1_9 = ext(b, 9, 9);
    const x0_9 = ext(a, 9, 9);
    const x1_10 = ext(b, 10, 10);
    const x0_10 = ext(a, 10, 10);
    const x1_11 = ext(b, 11, 11);
    const x0_11 = ext(a, 11, 11);
    const x1_12 = ext(b, 12, 12);
    const x0_12 = ext(a, 12, 12);
    const x1_13 = ext(b, 13, 13);
    const x0_13 = ext(a, 13, 13);
    const x1_14 = ext(b, 14, 14);
    const x0_14 = ext(a, 14, 14);
    const x1_15 = ext(b, 15, 15);
    const x0_15 = ext(a, 15, 15);
    const x1_16 = ext(b, 16, 16);
    const x0_16 = ext(a, 16, 16);
    const x1_17 = ext(b, 17, 17);
    const x0_17 = ext(a, 17, 17);
    const x1_18 = ext(b, 18, 18);
    const x0_18 = ext(a, 18, 18);
    const x1_19 = ext(b, 19, 19);
    const x0_19 = ext(a, 19, 19);
    const x1_20 = ext(b, 20, 20);
    const x0_20 = ext(a, 20, 20);
    const x1_21 = ext(b, 21, 21);
    const x0_21 = ext(a, 21, 21);
    const x1_22 = ext(b, 22, 22);
    const x0_22 = ext(a, 22, 22);
    const x1_23 = ext(b, 23, 23);
    const x0_23 = ext(a, 23, 23);
    const x1_24 = ext(b, 24, 24);
    const x0_24 = ext(a, 24, 24);
    const x1_25 = ext(b, 25, 25);
    const x0_25 = ext(a, 25, 25);
    const x1_26 = ext(b, 26, 26);
    const x0_26 = ext(a, 26, 26);
    const x1_27 = ext(b, 27, 27);
    const x0_27 = ext(a, 27, 27);
    const x1_28 = ext(b, 28, 28);
    const x0_28 = ext(a, 28, 28);
    const x1_29 = ext(b, 29, 29);
    const x0_29 = ext(a, 29, 29);
    const x1_30 = ext(b, 30, 30);
    const x0_30 = ext(a, 30, 30);
    const x1_31 = ext(b, 31, 31);
    const x0_31 = ext(a, 31, 31);
    const x1_32 = ext(b, 32, 32);
    const x0_32 = ext(a, 32, 32);
    const x1_33 = ext(b, 33, 33);
    const x0_33 = ext(a, 33, 33);
    const x1_34 = ext(b, 34, 34);
    const x0_34 = ext(a, 34, 34);
    const x1_35 = ext(b, 35, 35);
    const x0_35 = ext(a, 35, 35);
    const x1_36 = ext(b, 36, 36);
    const x0_36 = ext(a, 36, 36);
    const x1_37 = ext(b, 37, 37);
    const x0_37 = ext(a, 37, 37);
    const x1_38 = ext(b, 38, 38);
    const x0_38 = ext(a, 38, 38);
    const x1_39 = ext(b, 39, 39);
    const x0_39 = ext(a, 39, 39);
    const x1_40 = ext(b, 40, 40);
    const x0_40 = ext(a, 40, 40);
    const x1_41 = ext(b, 41, 41);
    const x0_41 = ext(a, 41, 41);
    const x1_42 = ext(b, 42, 42);
    const x0_42 = ext(a, 42, 42);
    const x1_43 = ext(b, 43, 43);
    const x0_43 = ext(a, 43, 43);
    const x1_44 = ext(b, 44, 44);
    const x0_44 = ext(a, 44, 44);
    const x1_45 = ext(b, 45, 45);
    const x0_45 = ext(a, 45, 45);
    const x1_46 = ext(b, 46, 46);
    const x0_46 = ext(a, 46, 46);
    const x1_47 = ext(b, 47, 47);
    const x0_47 = ext(a, 47, 47);
    const x1_48 = ext(b, 48, 48);
    const x0_48 = ext(a, 48, 48);
    const x1_49 = ext(b, 49, 49);
    const x0_49 = ext(a, 49, 49);
    const x1_50 = ext(b, 50, 50);
    const x0_50 = ext(a, 50, 50);
    const x1_51 = ext(b, 51, 51);
    const x0_51 = ext(a, 51, 51);
    const x1_52 = ext(b, 52, 52);
    const x0_52 = ext(a, 52, 52);
    const x1_53 = ext(b, 53, 53);
    const x0_53 = ext(a, 53, 53);
    const x1_54 = ext(b, 54, 54);
    const x0_54 = ext(a, 54, 54);
    const x1_55 = ext(b, 55, 55);
    const x0_55 = ext(a, 55, 55);
    const x1_56 = ext(b, 56, 56);
    const x0_56 = ext(a, 56, 56);
    const x1_57 = ext(b, 57, 57);
    const x0_57 = ext(a, 57, 57);
    const x1_58 = ext(b, 58, 58);
    const x0_58 = ext(a, 58, 58);
    const x1_59 = ext(b, 59, 59);
    const x0_59 = ext(a, 59, 59);
    const x1_60 = ext(b, 60, 60);
    const x0_60 = ext(a, 60, 60);
    const x1_61 = ext(b, 61, 61);
    const x0_61 = ext(a, 61, 61);
    const x1_62 = ext(b, 62, 62);
    const x0_62 = ext(a, 62, 62);
    const x1_63 = ext(b, 63, 63);
    const x0_63 = ext(a, 63, 63);
    const g0 = (x0_0 ^ x1_0);
    const g1 = (g0 ^ 1n);
    const g2 = (g1 ^ 1n);
    const g3 = (x0_1 ^ x1_1);
    const g4 = (g3 ^ 1n);
    const g5 = (g4 ^ 1n);
    const g6 = (x0_2 ^ x1_2);
    const g7 = (g6 ^ 1n);
    const g8 = (g7 ^ 1n);
    const g9 = (x0_3 ^ x1_3);
    const g10 = (g9 ^ 1n);
    const g11 = (g10 ^ 1n);
    const g12 = (x0_4 ^ x1_4);
    const g13 = (g12 ^ 1n);
    const g14 = (g13 ^ 1n);
    const g15 = (x0_5 ^ x1_5);
    const g16 = (g15 ^ 1n);
    const g17 = (g16 ^ 1n);
    const g18 = (x0_6 ^ x1_6);
    const g19 = (g18 ^ 1n);
    const g20 = (g19 ^ 1n);
    const g21 = (x0_7 ^ x1_7);
    const g22 = (g21 ^ 1n);
    const g23 = (g22 ^ 1n);
    const g24 = (x0_8 ^ x1_8);
    const g25 = (g24 ^ 1n);
    const g26 = (g25 ^ 1n);
    const g27 = (x0_9 ^ x1_9);
    const g28 = (g27 ^ 1n);
    const g29 = (g28 ^ 1n);
    const g30 = (x0_10 ^ x1_10);
    const g31 = (g30 ^ 1n);
    const g32 = (g31 ^ 1n);
    const g33 = (x0_11 ^ x1_11);
    const g34 = (g33 ^ 1n);
    const g35 = (g34 ^ 1n);
    const g36 = (x0_12 ^ x1_12);
    const g37 = (g36 ^ 1n);
    const g38 = (g37 ^ 1n);
    const g39 = (x0_13 ^ x1_13);
    const g40 = (g39 ^ 1n);
    const g41 = (g40 ^ 1n);
    const g42 = (x0_14 ^ x1_14);
    const g43 = (g42 ^ 1n);
    const g44 = (g43 ^ 1n);
    const g45 = (x0_15 ^ x1_15);
    const g46 = (g45 ^ 1n);
    const g47 = (g46 ^ 1n);
    const g48 = (x0_16 ^ x1_16);
    const g49 = (g48 ^ 1n);
    const g50 = (g49 ^ 1n);
    const g51 = (x0_17 ^ x1_17);
    const g52 = (g51 ^ 1n);
    const g53 = (g52 ^ 1n);
    const g54 = (x0_18 ^ x1_18);
    const g55 = (g54 ^ 1n);
    const g56 = (g55 ^ 1n);
    const g57 = (x0_19 ^ x1_19);
    const g58 = (g57 ^ 1n);
    const g59 = (g58 ^ 1n);
    const g60 = (x0_20 ^ x1_20);
    const g61 = (g60 ^ 1n);
    const g62 = (g61 ^ 1n);
    const g63 = (x0_21 ^ x1_21);
    const g64 = (g63 ^ 1n);
    const g65 = (g64 ^ 1n);
    const g66 = (x0_22 ^ x1_22);
    const g67 = (g66 ^ 1n);
    const g68 = (g67 ^ 1n);
    const g69 = (x0_23 ^ x1_23);
    const g70 = (g69 ^ 1n);
    const g71 = (g70 ^ 1n);
    const g72 = (x0_24 ^ x1_24);
    const g73 = (g72 ^ 1n);
    const g74 = (g73 ^ 1n);
    const g75 = (x0_25 ^ x1_25);
    const g76 = (g75 ^ 1n);
    const g77 = (g76 ^ 1n);
    const g78 = (x0_26 ^ x1_26);
    const g79 = (g78 ^ 1n);
    const g80 = (g79 ^ 1n);
    const g81 = (x0_27 ^ x1_27);
    const g82 = (g81 ^ 1n);
    const g83 = (g82 ^ 1n);
    const g84 = (x0_28 ^ x1_28);
    const g85 = (g84 ^ 1n);
    const g86 = (g85 ^ 1n);
    const g87 = (x0_29 ^ x1_29);
    const g88 = (g87 ^ 1n);
    const g89 = (g88 ^ 1n);
    const g90 = (x0_30 ^ x1_30);
    const g91 = (g90 ^ 1n);
    const g92 = (g91 ^ 1n);
    const g93 = (x0_31 ^ x1_31);
    const g94 = (g93 ^ 1n);
    const g95 = (g94 ^ 1n);
    const g96 = (x0_32 ^ x1_32);
    const g97 = (g96 ^ 1n);
    const g98 = (g97 ^ 1n);
    const g99 = (x0_33 ^ x1_33);
    const g100 = (g99 ^ 1n);
    const g101 = (g100 ^ 1n);
    const g102 = (x0_34 ^ x1_34);
    const g103 = (g102 ^ 1n);
    const g104 = (g103 ^ 1n);
    const g105 = (x0_35 ^ x1_35);
    const g106 = (g105 ^ 1n);
    const g107 = (g106 ^ 1n);
    const g108 = (x0_36 ^ x1_36);
    const g109 = (g108 ^ 1n);
    const g110 = (g109 ^ 1n);
    const g111 = (x0_37 ^ x1_37);
    const g112 = (g111 ^ 1n);
    const g113 = (g112 ^ 1n);
    const g114 = (x0_38 ^ x1_38);
    const g115 = (g114 ^ 1n);
    const g116 = (g115 ^ 1n);
    const g117 = (x0_39 ^ x1_39);
    const g118 = (g117 ^ 1n);
    const g119 = (g118 ^ 1n);
    const g120 = (x0_40 ^ x1_40);
    const g121 = (g120 ^ 1n);
    const g122 = (g121 ^ 1n);
    const g123 = (x0_41 ^ x1_41);
    const g124 = (g123 ^ 1n);
    const g125 = (g124 ^ 1n);
    const g126 = (x0_42 ^ x1_42);
    const g127 = (g126 ^ 1n);
    const g128 = (g127 ^ 1n);
    const g129 = (x0_43 ^ x1_43);
    const g130 = (g129 ^ 1n);
    const g131 = (g130 ^ 1n);
    const g132 = (x0_44 ^ x1_44);
    const g133 = (g132 ^ 1n);
    const g134 = (g133 ^ 1n);
    const g135 = (x0_45 ^ x1_45);
    const g136 = (g135 ^ 1n);
    const g137 = (g136 ^ 1n);
    const g138 = (x0_46 ^ x1_46);
    const g139 = (g138 ^ 1n);
    const g140 = (g139 ^ 1n);
    const g141 = (x0_47 ^ x1_47);
    const g142 = (g141 ^ 1n);
    const g143 = (g142 ^ 1n);
    const g144 = (x0_48 ^ x1_48);
    const g145 = (g144 ^ 1n);
    const g146 = (g145 ^ 1n);
    const g147 = (x0_49 ^ x1_49);
    const g148 = (g147 ^ 1n);
    const g149 = (g148 ^ 1n);
    const g150 = (x0_50 ^ x1_50);
    const g151 = (g150 ^ 1n);
    const g152 = (g151 ^ 1n);
    const g153 = (x0_51 ^ x1_51);
    const g154 = (g153 ^ 1n);
    const g155 = (g154 ^ 1n);
    const g156 = (x0_52 ^ x1_52);
    const g157 = (g156 ^ 1n);
    const g158 = (g157 ^ 1n);
    const g159 = (x0_53 ^ x1_53);
    const g160 = (g159 ^ 1n);
    const g161 = (g160 ^ 1n);
    const g162 = (x0_54 ^ x1_54);
    const g163 = (g162 ^ 1n);
    const g164 = (g163 ^ 1n);
    const g165 = (x0_55 ^ x1_55);
    const g166 = (g165 ^ 1n);
    const g167 = (g166 ^ 1n);
    const g168 = (x0_56 ^ x1_56);
    const g169 = (g168 ^ 1n);
    const g170 = (g169 ^ 1n);
    const g171 = (x0_57 ^ x1_57);
    const g172 = (g171 ^ 1n);
    const g173 = (g172 ^ 1n);
    const g174 = (x0_58 ^ x1_58);
    const g175 = (g174 ^ 1n);
    const g176 = (g175 ^ 1n);
    const g177 = (x0_59 ^ x1_59);
    const g178 = (g177 ^ 1n);
    const g179 = (g178 ^ 1n);
    const g180 = (x0_60 ^ x1_60);
    const g181 = (g180 ^ 1n);
    const g182 = (g181 ^ 1n);
    const g183 = (x0_61 ^ x1_61);
    const g184 = (g183 ^ 1n);
    const g185 = (g184 ^ 1n);
    const g186 = (x0_62 ^ x1_62);
    const g187 = (g186 ^ 1n);
    const g188 = (g187 ^ 1n);
    const g189 = (x0_63 ^ x1_63);
    const g190 = (g189 ^ 1n);
    const g191 = (g190 ^ 1n);
    const w0 = g191;
    const w1 = cat(w0, g188, 1);
    const w2 = cat(w1, g185, 1);
    const w3 = cat(w2, g182, 1);
    const w4 = cat(w3, g179, 1);
    const w5 = cat(w4, g176, 1);
    const w6 = cat(w5, g173, 1);
    const w7 = cat(w6, g170, 1);
    const w8 = cat(w7, g167, 1);
    const w9 = cat(w8, g164, 1);
    const w10 = cat(w9, g161, 1);
    const w11 = cat(w10, g158, 1);
    const w12 = cat(w11, g155, 1);
    const w13 = cat(w12, g152, 1);
    const w14 = cat(w13, g149, 1);
    const w15 = cat(w14, g146, 1);
    const w16 = cat(w15, g143, 1);
    const w17 = cat(w16, g140, 1);
    const w18 = cat(w17, g137, 1);
    const w19 = cat(w18, g134, 1);
    const w20 = cat(w19, g131, 1);
    const w21 = cat(w20, g128, 1);
    const w22 = cat(w21, g125, 1);
    const w23 = cat(w22, g122, 1);
    const w24 = cat(w23, g119, 1);
    const w25 = cat(w24, g116, 1);
    const w26 = cat(w25, g113, 1);
    const w27 = cat(w26, g110, 1);
    const w28 = cat(w27, g107, 1);
    const w29 = cat(w28, g104, 1);
    const w30 = cat(w29, g101, 1);
    const w31 = cat(w30, g98, 1);
    const w32 = cat(w31, g95, 1);
    const w33 = cat(w32, g92, 1);
    const w34 = cat(w33, g89, 1);
    const w35 = cat(w34, g86, 1);
    const w36 = cat(w35, g83, 1);
    const w37 = cat(w36, g80, 1);
    const w38 = cat(w37, g77, 1);
    const w39 = cat(w38, g74, 1);
    const w40 = cat(w39, g71, 1);
    const w41 = cat(w40, g68, 1);
    const w42 = cat(w41, g65, 1);
    const w43 = cat(w42, g62, 1);
    const w44 = cat(w43, g59, 1);
    const w45 = cat(w44, g56, 1);
    const w46 = cat(w45, g53, 1);
    const w47 = cat(w46, g50, 1);
    const w48 = cat(w47, g47, 1);
    const w49 = cat(w48, g44, 1);
    const w50 = cat(w49, g41, 1);
    const w51 = cat(w50, g38, 1);
    const w52 = cat(w51, g35, 1);
    const w53 = cat(w52, g32, 1);
    const w54 = cat(w53, g29, 1);
    const w55 = cat(w54, g26, 1);
    const w56 = cat(w55, g23, 1);
    const w57 = cat(w56, g20, 1);
    const w58 = cat(w57, g17, 1);
    const w59 = cat(w58, g14, 1);
    const w60 = cat(w59, g11, 1);
    const w61 = cat(w60, g8, 1);
    const w62 = cat(w61, g5, 1);
    const w63 = cat(w62, g2, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_pxor_xmm_xmm_128__reg_xmm0_low__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
