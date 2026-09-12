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
// one named local per gate, over the term of cmove_gpr_gpr_32__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
function emu_cmove_gpr_gpr_32__reg_rdi__javascript(a, b, c, d) {
    const x3_0 = ext(d, 0, 0);
    const x1_17 = ext(a, 17, 17);
    const x0_17 = ext(b, 17, 17);
    const x1_26 = ext(a, 26, 26);
    const x0_26 = ext(b, 26, 26);
    const x1_22 = ext(a, 22, 22);
    const x0_22 = ext(b, 22, 22);
    const x1_13 = ext(a, 13, 13);
    const x0_13 = ext(b, 13, 13);
    const x1_30 = ext(a, 30, 30);
    const x0_30 = ext(b, 30, 30);
    const x1_4 = ext(a, 4, 4);
    const x0_4 = ext(b, 4, 4);
    const x1_0 = ext(a, 0, 0);
    const x0_0 = ext(b, 0, 0);
    const x1_31 = ext(a, 31, 31);
    const x0_31 = ext(b, 31, 31);
    const x1_7 = ext(a, 7, 7);
    const x0_7 = ext(b, 7, 7);
    const x1_19 = ext(a, 19, 19);
    const x0_19 = ext(b, 19, 19);
    const x1_11 = ext(a, 11, 11);
    const x0_11 = ext(b, 11, 11);
    const x1_6 = ext(a, 6, 6);
    const x0_6 = ext(b, 6, 6);
    const x1_23 = ext(a, 23, 23);
    const x0_23 = ext(b, 23, 23);
    const x1_8 = ext(a, 8, 8);
    const x0_8 = ext(b, 8, 8);
    const x1_20 = ext(a, 20, 20);
    const x0_20 = ext(b, 20, 20);
    const x1_25 = ext(a, 25, 25);
    const x0_25 = ext(b, 25, 25);
    const x1_28 = ext(a, 28, 28);
    const x0_28 = ext(b, 28, 28);
    const x1_5 = ext(a, 5, 5);
    const x0_5 = ext(b, 5, 5);
    const x1_15 = ext(a, 15, 15);
    const x0_15 = ext(b, 15, 15);
    const x1_9 = ext(a, 9, 9);
    const x0_9 = ext(b, 9, 9);
    const x1_29 = ext(a, 29, 29);
    const x0_29 = ext(b, 29, 29);
    const x1_10 = ext(a, 10, 10);
    const x0_10 = ext(b, 10, 10);
    const x1_27 = ext(a, 27, 27);
    const x0_27 = ext(b, 27, 27);
    const x1_3 = ext(a, 3, 3);
    const x0_3 = ext(b, 3, 3);
    const x1_24 = ext(a, 24, 24);
    const x0_24 = ext(b, 24, 24);
    const x1_18 = ext(a, 18, 18);
    const x0_18 = ext(b, 18, 18);
    const x1_16 = ext(a, 16, 16);
    const x0_16 = ext(b, 16, 16);
    const x1_2 = ext(a, 2, 2);
    const x0_2 = ext(b, 2, 2);
    const x1_14 = ext(a, 14, 14);
    const x0_14 = ext(b, 14, 14);
    const x1_12 = ext(a, 12, 12);
    const x0_12 = ext(b, 12, 12);
    const x1_1 = ext(a, 1, 1);
    const x0_1 = ext(b, 1, 1);
    const x1_21 = ext(a, 21, 21);
    const x0_21 = ext(b, 21, 21);
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
    const g0 = (x1_17 ^ 1n);
    const g1 = (x0_17 ^ 1n);
    const g2 = (g1 | g0);
    const g3 = (g2 ^ 1n);
    const g4 = (x1_26 ^ 1n);
    const g5 = (x0_26 ^ 1n);
    const g6 = (g5 | g4);
    const g7 = (g6 ^ 1n);
    const g8 = (x1_22 ^ 1n);
    const g9 = (x0_22 ^ 1n);
    const g10 = (g9 | g8);
    const g11 = (g10 ^ 1n);
    const g12 = (x1_13 ^ 1n);
    const g13 = (x0_13 ^ 1n);
    const g14 = (g13 | g12);
    const g15 = (g14 ^ 1n);
    const g16 = (x1_30 ^ 1n);
    const g17 = (x0_30 ^ 1n);
    const g18 = (g17 | g16);
    const g19 = (g18 ^ 1n);
    const g20 = (x1_4 ^ 1n);
    const g21 = (x0_4 ^ 1n);
    const g22 = (g21 | g20);
    const g23 = (g22 ^ 1n);
    const g24 = (x1_0 ^ 1n);
    const g25 = (x0_0 ^ 1n);
    const g26 = (g25 | g24);
    const g27 = (g26 ^ 1n);
    const g28 = (x1_31 ^ 1n);
    const g29 = (x0_31 ^ 1n);
    const g30 = (g29 | g28);
    const g31 = (g30 ^ 1n);
    const g32 = (x1_7 ^ 1n);
    const g33 = (x0_7 ^ 1n);
    const g34 = (g33 | g32);
    const g35 = (g34 ^ 1n);
    const g36 = (x1_19 ^ 1n);
    const g37 = (x0_19 ^ 1n);
    const g38 = (g37 | g36);
    const g39 = (g38 ^ 1n);
    const g40 = (x1_11 ^ 1n);
    const g41 = (x0_11 ^ 1n);
    const g42 = (g41 | g40);
    const g43 = (g42 ^ 1n);
    const g44 = (x1_6 ^ 1n);
    const g45 = (x0_6 ^ 1n);
    const g46 = (g45 | g44);
    const g47 = (g46 ^ 1n);
    const g48 = (x1_23 ^ 1n);
    const g49 = (x0_23 ^ 1n);
    const g50 = (g49 | g48);
    const g51 = (g50 ^ 1n);
    const g52 = (x1_8 ^ 1n);
    const g53 = (x0_8 ^ 1n);
    const g54 = (g53 | g52);
    const g55 = (g54 ^ 1n);
    const g56 = (x1_20 ^ 1n);
    const g57 = (x0_20 ^ 1n);
    const g58 = (g57 | g56);
    const g59 = (g58 ^ 1n);
    const g60 = (x1_25 ^ 1n);
    const g61 = (x0_25 ^ 1n);
    const g62 = (g61 | g60);
    const g63 = (g62 ^ 1n);
    const g64 = (x1_28 ^ 1n);
    const g65 = (x0_28 ^ 1n);
    const g66 = (g65 | g64);
    const g67 = (g66 ^ 1n);
    const g68 = (x1_5 ^ 1n);
    const g69 = (x0_5 ^ 1n);
    const g70 = (g69 | g68);
    const g71 = (g70 ^ 1n);
    const g72 = (x1_15 ^ 1n);
    const g73 = (x0_15 ^ 1n);
    const g74 = (g73 | g72);
    const g75 = (g74 ^ 1n);
    const g76 = (x1_9 ^ 1n);
    const g77 = (x0_9 ^ 1n);
    const g78 = (g77 | g76);
    const g79 = (g78 ^ 1n);
    const g80 = (x1_29 ^ 1n);
    const g81 = (x0_29 ^ 1n);
    const g82 = (g81 | g80);
    const g83 = (g82 ^ 1n);
    const g84 = (x1_10 ^ 1n);
    const g85 = (x0_10 ^ 1n);
    const g86 = (g85 | g84);
    const g87 = (g86 ^ 1n);
    const g88 = (x1_27 ^ 1n);
    const g89 = (x0_27 ^ 1n);
    const g90 = (g89 | g88);
    const g91 = (g90 ^ 1n);
    const g92 = (x1_3 ^ 1n);
    const g93 = (x0_3 ^ 1n);
    const g94 = (g93 | g92);
    const g95 = (g94 ^ 1n);
    const g96 = (x1_24 ^ 1n);
    const g97 = (x0_24 ^ 1n);
    const g98 = (g97 | g96);
    const g99 = (g98 ^ 1n);
    const g100 = (x1_18 ^ 1n);
    const g101 = (x0_18 ^ 1n);
    const g102 = (g101 | g100);
    const g103 = (g102 ^ 1n);
    const g104 = (x1_16 ^ 1n);
    const g105 = (x0_16 ^ 1n);
    const g106 = (g105 | g104);
    const g107 = (g106 ^ 1n);
    const g108 = (x1_2 ^ 1n);
    const g109 = (x0_2 ^ 1n);
    const g110 = (g109 | g108);
    const g111 = (g110 ^ 1n);
    const g112 = (x1_14 ^ 1n);
    const g113 = (x0_14 ^ 1n);
    const g114 = (g113 | g112);
    const g115 = (g114 ^ 1n);
    const g116 = (x1_12 ^ 1n);
    const g117 = (x0_12 ^ 1n);
    const g118 = (g117 | g116);
    const g119 = (g118 ^ 1n);
    const g120 = (x1_1 ^ 1n);
    const g121 = (x0_1 ^ 1n);
    const g122 = (g121 | g120);
    const g123 = (g122 ^ 1n);
    const g124 = (x1_21 ^ 1n);
    const g125 = (x0_21 ^ 1n);
    const g126 = (g125 | g124);
    const g127 = (g126 ^ 1n);
    const g128 = (g127 | g123);
    const g129 = (g128 | g119);
    const g130 = (g129 | g115);
    const g131 = (g130 | g111);
    const g132 = (g131 | g107);
    const g133 = (g132 | g103);
    const g134 = (g133 | g99);
    const g135 = (g134 | g95);
    const g136 = (g135 | g91);
    const g137 = (g136 | g87);
    const g138 = (g137 | g83);
    const g139 = (g138 | g79);
    const g140 = (g139 | g75);
    const g141 = (g140 | g71);
    const g142 = (g141 | g67);
    const g143 = (g142 | g63);
    const g144 = (g143 | g59);
    const g145 = (g144 | g55);
    const g146 = (g145 | g51);
    const g147 = (g146 | g47);
    const g148 = (g147 | g43);
    const g149 = (g148 | g39);
    const g150 = (g149 | g35);
    const g151 = (g150 | g31);
    const g152 = (g151 | g27);
    const g153 = (g152 | g23);
    const g154 = (g153 | g19);
    const g155 = (g154 | g15);
    const g156 = (g155 | g11);
    const g157 = (g156 | g7);
    const g158 = (g157 | g3);
    const g159 = (g158 ^ 1n);
    const g160 = (g159 ^ 1n);
    const g161 = (g160 & x3_0);
    const g162 = (g159 & x2_0);
    const g163 = (g162 | g161);
    const g164 = (g160 & x3_1);
    const g165 = (g159 & x2_1);
    const g166 = (g165 | g164);
    const g167 = (g160 & x3_2);
    const g168 = (g159 & x2_2);
    const g169 = (g168 | g167);
    const g170 = (g160 & x3_3);
    const g171 = (g159 & x2_3);
    const g172 = (g171 | g170);
    const g173 = (g160 & x3_4);
    const g174 = (g159 & x2_4);
    const g175 = (g174 | g173);
    const g176 = (g160 & x3_5);
    const g177 = (g159 & x2_5);
    const g178 = (g177 | g176);
    const g179 = (g160 & x3_6);
    const g180 = (g159 & x2_6);
    const g181 = (g180 | g179);
    const g182 = (g160 & x3_7);
    const g183 = (g159 & x2_7);
    const g184 = (g183 | g182);
    const g185 = (g160 & x3_8);
    const g186 = (g159 & x2_8);
    const g187 = (g186 | g185);
    const g188 = (g160 & x3_9);
    const g189 = (g159 & x2_9);
    const g190 = (g189 | g188);
    const g191 = (g160 & x3_10);
    const g192 = (g159 & x2_10);
    const g193 = (g192 | g191);
    const g194 = (g160 & x3_11);
    const g195 = (g159 & x2_11);
    const g196 = (g195 | g194);
    const g197 = (g160 & x3_12);
    const g198 = (g159 & x2_12);
    const g199 = (g198 | g197);
    const g200 = (g160 & x3_13);
    const g201 = (g159 & x2_13);
    const g202 = (g201 | g200);
    const g203 = (g160 & x3_14);
    const g204 = (g159 & x2_14);
    const g205 = (g204 | g203);
    const g206 = (g160 & x3_15);
    const g207 = (g159 & x2_15);
    const g208 = (g207 | g206);
    const g209 = (g160 & x3_16);
    const g210 = (g159 & x2_16);
    const g211 = (g210 | g209);
    const g212 = (g160 & x3_17);
    const g213 = (g159 & x2_17);
    const g214 = (g213 | g212);
    const g215 = (g160 & x3_18);
    const g216 = (g159 & x2_18);
    const g217 = (g216 | g215);
    const g218 = (g160 & x3_19);
    const g219 = (g159 & x2_19);
    const g220 = (g219 | g218);
    const g221 = (g160 & x3_20);
    const g222 = (g159 & x2_20);
    const g223 = (g222 | g221);
    const g224 = (g160 & x3_21);
    const g225 = (g159 & x2_21);
    const g226 = (g225 | g224);
    const g227 = (g160 & x3_22);
    const g228 = (g159 & x2_22);
    const g229 = (g228 | g227);
    const g230 = (g160 & x3_23);
    const g231 = (g159 & x2_23);
    const g232 = (g231 | g230);
    const g233 = (g160 & x3_24);
    const g234 = (g159 & x2_24);
    const g235 = (g234 | g233);
    const g236 = (g160 & x3_25);
    const g237 = (g159 & x2_25);
    const g238 = (g237 | g236);
    const g239 = (g160 & x3_26);
    const g240 = (g159 & x2_26);
    const g241 = (g240 | g239);
    const g242 = (g160 & x3_27);
    const g243 = (g159 & x2_27);
    const g244 = (g243 | g242);
    const g245 = (g160 & x3_28);
    const g246 = (g159 & x2_28);
    const g247 = (g246 | g245);
    const g248 = (g160 & x3_29);
    const g249 = (g159 & x2_29);
    const g250 = (g249 | g248);
    const g251 = (g160 & x3_30);
    const g252 = (g159 & x2_30);
    const g253 = (g252 | g251);
    const g254 = (g160 & x3_31);
    const g255 = (g159 & x2_31);
    const g256 = (g255 | g254);
    const k0 = 0n;
    const w0 = k0;
    const w1 = cat(w0, k0, 1);
    const w2 = cat(w1, k0, 1);
    const w3 = cat(w2, k0, 1);
    const w4 = cat(w3, k0, 1);
    const w5 = cat(w4, k0, 1);
    const w6 = cat(w5, k0, 1);
    const w7 = cat(w6, k0, 1);
    const w8 = cat(w7, k0, 1);
    const w9 = cat(w8, k0, 1);
    const w10 = cat(w9, k0, 1);
    const w11 = cat(w10, k0, 1);
    const w12 = cat(w11, k0, 1);
    const w13 = cat(w12, k0, 1);
    const w14 = cat(w13, k0, 1);
    const w15 = cat(w14, k0, 1);
    const w16 = cat(w15, k0, 1);
    const w17 = cat(w16, k0, 1);
    const w18 = cat(w17, k0, 1);
    const w19 = cat(w18, k0, 1);
    const w20 = cat(w19, k0, 1);
    const w21 = cat(w20, k0, 1);
    const w22 = cat(w21, k0, 1);
    const w23 = cat(w22, k0, 1);
    const w24 = cat(w23, k0, 1);
    const w25 = cat(w24, k0, 1);
    const w26 = cat(w25, k0, 1);
    const w27 = cat(w26, k0, 1);
    const w28 = cat(w27, k0, 1);
    const w29 = cat(w28, k0, 1);
    const w30 = cat(w29, k0, 1);
    const w31 = cat(w30, k0, 1);
    const w32 = cat(w31, g256, 1);
    const w33 = cat(w32, g253, 1);
    const w34 = cat(w33, g250, 1);
    const w35 = cat(w34, g247, 1);
    const w36 = cat(w35, g244, 1);
    const w37 = cat(w36, g241, 1);
    const w38 = cat(w37, g238, 1);
    const w39 = cat(w38, g235, 1);
    const w40 = cat(w39, g232, 1);
    const w41 = cat(w40, g229, 1);
    const w42 = cat(w41, g226, 1);
    const w43 = cat(w42, g223, 1);
    const w44 = cat(w43, g220, 1);
    const w45 = cat(w44, g217, 1);
    const w46 = cat(w45, g214, 1);
    const w47 = cat(w46, g211, 1);
    const w48 = cat(w47, g208, 1);
    const w49 = cat(w48, g205, 1);
    const w50 = cat(w49, g202, 1);
    const w51 = cat(w50, g199, 1);
    const w52 = cat(w51, g196, 1);
    const w53 = cat(w52, g193, 1);
    const w54 = cat(w53, g190, 1);
    const w55 = cat(w54, g187, 1);
    const w56 = cat(w55, g184, 1);
    const w57 = cat(w56, g181, 1);
    const w58 = cat(w57, g178, 1);
    const w59 = cat(w58, g175, 1);
    const w60 = cat(w59, g172, 1);
    const w61 = cat(w60, g169, 1);
    const w62 = cat(w61, g166, 1);
    const w63 = cat(w62, g163, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_cmove_gpr_gpr_32__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
