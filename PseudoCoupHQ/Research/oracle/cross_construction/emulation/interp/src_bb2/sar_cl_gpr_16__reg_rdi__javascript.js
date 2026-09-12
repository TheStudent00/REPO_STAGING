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
// one named local per gate, over the term of sar_cl_gpr_16__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1)))
function emu_sar_cl_gpr_16__reg_rdi__javascript(a, b) {
    const x0_0 = ext(a, 0, 0);
    const x0_1 = ext(a, 1, 1);
    const x1_0 = ext(b, 0, 0);
    const x0_2 = ext(a, 2, 2);
    const x0_3 = ext(a, 3, 3);
    const x1_1 = ext(b, 1, 1);
    const x0_4 = ext(a, 4, 4);
    const x0_5 = ext(a, 5, 5);
    const x0_6 = ext(a, 6, 6);
    const x0_7 = ext(a, 7, 7);
    const x1_2 = ext(b, 2, 2);
    const x0_8 = ext(a, 8, 8);
    const x0_9 = ext(a, 9, 9);
    const x0_10 = ext(a, 10, 10);
    const x0_11 = ext(a, 11, 11);
    const x0_12 = ext(a, 12, 12);
    const x0_13 = ext(a, 13, 13);
    const x0_14 = ext(a, 14, 14);
    const x0_15 = ext(a, 15, 15);
    const x1_3 = ext(b, 3, 3);
    const x1_4 = ext(b, 4, 4);
    const x0_16 = ext(a, 16, 16);
    const x0_17 = ext(a, 17, 17);
    const x0_18 = ext(a, 18, 18);
    const x0_19 = ext(a, 19, 19);
    const x0_20 = ext(a, 20, 20);
    const x0_21 = ext(a, 21, 21);
    const x0_22 = ext(a, 22, 22);
    const x0_23 = ext(a, 23, 23);
    const x0_24 = ext(a, 24, 24);
    const x0_25 = ext(a, 25, 25);
    const x0_26 = ext(a, 26, 26);
    const x0_27 = ext(a, 27, 27);
    const x0_28 = ext(a, 28, 28);
    const x0_29 = ext(a, 29, 29);
    const x0_30 = ext(a, 30, 30);
    const x0_31 = ext(a, 31, 31);
    const x0_32 = ext(a, 32, 32);
    const x0_33 = ext(a, 33, 33);
    const x0_34 = ext(a, 34, 34);
    const x0_35 = ext(a, 35, 35);
    const x0_36 = ext(a, 36, 36);
    const x0_37 = ext(a, 37, 37);
    const x0_38 = ext(a, 38, 38);
    const x0_39 = ext(a, 39, 39);
    const x0_40 = ext(a, 40, 40);
    const x0_41 = ext(a, 41, 41);
    const x0_42 = ext(a, 42, 42);
    const x0_43 = ext(a, 43, 43);
    const x0_44 = ext(a, 44, 44);
    const x0_45 = ext(a, 45, 45);
    const x0_46 = ext(a, 46, 46);
    const x0_47 = ext(a, 47, 47);
    const x0_48 = ext(a, 48, 48);
    const x0_49 = ext(a, 49, 49);
    const x0_50 = ext(a, 50, 50);
    const x0_51 = ext(a, 51, 51);
    const x0_52 = ext(a, 52, 52);
    const x0_53 = ext(a, 53, 53);
    const x0_54 = ext(a, 54, 54);
    const x0_55 = ext(a, 55, 55);
    const x0_56 = ext(a, 56, 56);
    const x0_57 = ext(a, 57, 57);
    const x0_58 = ext(a, 58, 58);
    const x0_59 = ext(a, 59, 59);
    const x0_60 = ext(a, 60, 60);
    const x0_61 = ext(a, 61, 61);
    const x0_62 = ext(a, 62, 62);
    const x0_63 = ext(a, 63, 63);
    const g0 = (x1_0 ^ 1n);
    const g1 = (x1_0 & x0_1);
    const g2 = (g0 & x0_0);
    const g3 = (g1 | g2);
    const g4 = (x1_0 ^ 1n);
    const g5 = (x1_0 & x0_3);
    const g6 = (g4 & x0_2);
    const g7 = (g5 | g6);
    const g8 = (x1_1 ^ 1n);
    const g9 = (x1_1 & g7);
    const g10 = (g8 & g3);
    const g11 = (g9 | g10);
    const g12 = (x1_0 ^ 1n);
    const g13 = (x1_0 & x0_5);
    const g14 = (g12 & x0_4);
    const g15 = (g13 | g14);
    const g16 = (x1_0 ^ 1n);
    const g17 = (x1_0 & x0_7);
    const g18 = (g16 & x0_6);
    const g19 = (g17 | g18);
    const g20 = (x1_1 ^ 1n);
    const g21 = (x1_1 & g19);
    const g22 = (g20 & g15);
    const g23 = (g21 | g22);
    const g24 = (x1_2 ^ 1n);
    const g25 = (x1_2 & g23);
    const g26 = (g24 & g11);
    const g27 = (g25 | g26);
    const g28 = (x1_0 ^ 1n);
    const g29 = (x1_0 & x0_9);
    const g30 = (g28 & x0_8);
    const g31 = (g29 | g30);
    const g32 = (x1_0 ^ 1n);
    const g33 = (x1_0 & x0_11);
    const g34 = (g32 & x0_10);
    const g35 = (g33 | g34);
    const g36 = (x1_1 ^ 1n);
    const g37 = (x1_1 & g35);
    const g38 = (g36 & g31);
    const g39 = (g37 | g38);
    const g40 = (x1_0 ^ 1n);
    const g41 = (x1_0 & x0_13);
    const g42 = (g40 & x0_12);
    const g43 = (g41 | g42);
    const g44 = (x1_0 ^ 1n);
    const g45 = (x1_0 & x0_15);
    const g46 = (g44 & x0_14);
    const g47 = (g45 | g46);
    const g48 = (x1_1 ^ 1n);
    const g49 = (x1_1 & g47);
    const g50 = (g48 & g43);
    const g51 = (g49 | g50);
    const g52 = (x1_2 ^ 1n);
    const g53 = (x1_2 & g51);
    const g54 = (g52 & g39);
    const g55 = (g53 | g54);
    const g56 = (x1_3 ^ 1n);
    const g57 = (x1_3 & g55);
    const g58 = (g56 & g27);
    const g59 = (g57 | g58);
    const g60 = (x1_4 ^ 1n);
    const g61 = (x1_4 & x0_15);
    const g62 = (g60 & g59);
    const g63 = (g61 | g62);
    const g64 = (x1_0 ^ 1n);
    const g65 = (x1_0 & x0_2);
    const g66 = (g64 & x0_1);
    const g67 = (g65 | g66);
    const g68 = (x1_0 ^ 1n);
    const g69 = (x1_0 & x0_4);
    const g70 = (g68 & x0_3);
    const g71 = (g69 | g70);
    const g72 = (x1_1 ^ 1n);
    const g73 = (x1_1 & g71);
    const g74 = (g72 & g67);
    const g75 = (g73 | g74);
    const g76 = (x1_0 ^ 1n);
    const g77 = (x1_0 & x0_6);
    const g78 = (g76 & x0_5);
    const g79 = (g77 | g78);
    const g80 = (x1_0 ^ 1n);
    const g81 = (x1_0 & x0_8);
    const g82 = (g80 & x0_7);
    const g83 = (g81 | g82);
    const g84 = (x1_1 ^ 1n);
    const g85 = (x1_1 & g83);
    const g86 = (g84 & g79);
    const g87 = (g85 | g86);
    const g88 = (x1_2 ^ 1n);
    const g89 = (x1_2 & g87);
    const g90 = (g88 & g75);
    const g91 = (g89 | g90);
    const g92 = (x1_0 ^ 1n);
    const g93 = (x1_0 & x0_10);
    const g94 = (g92 & x0_9);
    const g95 = (g93 | g94);
    const g96 = (x1_0 ^ 1n);
    const g97 = (x1_0 & x0_12);
    const g98 = (g96 & x0_11);
    const g99 = (g97 | g98);
    const g100 = (x1_1 ^ 1n);
    const g101 = (x1_1 & g99);
    const g102 = (g100 & g95);
    const g103 = (g101 | g102);
    const g104 = (x1_0 ^ 1n);
    const g105 = (x1_0 & x0_14);
    const g106 = (g104 & x0_13);
    const g107 = (g105 | g106);
    const g108 = (x1_1 ^ 1n);
    const g109 = (x1_1 & x0_15);
    const g110 = (g108 & g107);
    const g111 = (g109 | g110);
    const g112 = (x1_2 ^ 1n);
    const g113 = (x1_2 & g111);
    const g114 = (g112 & g103);
    const g115 = (g113 | g114);
    const g116 = (x1_3 ^ 1n);
    const g117 = (x1_3 & g115);
    const g118 = (g116 & g91);
    const g119 = (g117 | g118);
    const g120 = (x1_4 ^ 1n);
    const g121 = (x1_4 & x0_15);
    const g122 = (g120 & g119);
    const g123 = (g121 | g122);
    const g124 = (x1_1 ^ 1n);
    const g125 = (x1_1 & g15);
    const g126 = (g124 & g7);
    const g127 = (g125 | g126);
    const g128 = (x1_1 ^ 1n);
    const g129 = (x1_1 & g31);
    const g130 = (g128 & g19);
    const g131 = (g129 | g130);
    const g132 = (x1_2 ^ 1n);
    const g133 = (x1_2 & g131);
    const g134 = (g132 & g127);
    const g135 = (g133 | g134);
    const g136 = (x1_1 ^ 1n);
    const g137 = (x1_1 & g43);
    const g138 = (g136 & g35);
    const g139 = (g137 | g138);
    const g140 = (x1_1 | x1_0);
    const g141 = (g140 ^ 1n);
    const g142 = (g140 & x0_15);
    const g143 = (g141 & x0_14);
    const g144 = (g142 | g143);
    const g145 = (x1_2 ^ 1n);
    const g146 = (x1_2 & g144);
    const g147 = (g145 & g139);
    const g148 = (g146 | g147);
    const g149 = (x1_3 ^ 1n);
    const g150 = (x1_3 & g148);
    const g151 = (g149 & g135);
    const g152 = (g150 | g151);
    const g153 = (x1_4 ^ 1n);
    const g154 = (x1_4 & x0_15);
    const g155 = (g153 & g152);
    const g156 = (g154 | g155);
    const g157 = (x1_1 ^ 1n);
    const g158 = (x1_1 & g79);
    const g159 = (g157 & g71);
    const g160 = (g158 | g159);
    const g161 = (x1_1 ^ 1n);
    const g162 = (x1_1 & g95);
    const g163 = (g161 & g83);
    const g164 = (g162 | g163);
    const g165 = (x1_2 ^ 1n);
    const g166 = (x1_2 & g164);
    const g167 = (g165 & g160);
    const g168 = (g166 | g167);
    const g169 = (x1_1 ^ 1n);
    const g170 = (x1_1 & g107);
    const g171 = (g169 & g99);
    const g172 = (g170 | g171);
    const g173 = (x1_2 ^ 1n);
    const g174 = (x1_2 & x0_15);
    const g175 = (g173 & g172);
    const g176 = (g174 | g175);
    const g177 = (x1_3 ^ 1n);
    const g178 = (x1_3 & g176);
    const g179 = (g177 & g168);
    const g180 = (g178 | g179);
    const g181 = (x1_4 ^ 1n);
    const g182 = (x1_4 & x0_15);
    const g183 = (g181 & g180);
    const g184 = (g182 | g183);
    const g185 = (x1_2 ^ 1n);
    const g186 = (x1_2 & g39);
    const g187 = (g185 & g23);
    const g188 = (g186 | g187);
    const g189 = (x1_2 ^ 1n);
    const g190 = (x1_2 & x0_15);
    const g191 = (g189 & g51);
    const g192 = (g190 | g191);
    const g193 = (x1_3 ^ 1n);
    const g194 = (x1_3 & g192);
    const g195 = (g193 & g188);
    const g196 = (g194 | g195);
    const g197 = (x1_4 ^ 1n);
    const g198 = (x1_4 & x0_15);
    const g199 = (g197 & g196);
    const g200 = (g198 | g199);
    const g201 = (x1_2 ^ 1n);
    const g202 = (x1_2 & g103);
    const g203 = (g201 & g87);
    const g204 = (g202 | g203);
    const g205 = (x1_2 | x1_1);
    const g206 = (g205 ^ 1n);
    const g207 = (g205 & x0_15);
    const g208 = (g206 & g107);
    const g209 = (g207 | g208);
    const g210 = (x1_3 ^ 1n);
    const g211 = (x1_3 & g209);
    const g212 = (g210 & g204);
    const g213 = (g211 | g212);
    const g214 = (x1_4 ^ 1n);
    const g215 = (x1_4 & x0_15);
    const g216 = (g214 & g213);
    const g217 = (g215 | g216);
    const g218 = (x1_2 ^ 1n);
    const g219 = (x1_2 & g139);
    const g220 = (g218 & g131);
    const g221 = (g219 | g220);
    const g222 = (x1_2 | g140);
    const g223 = (g222 ^ 1n);
    const g224 = (g222 & x0_15);
    const g225 = (g223 & x0_14);
    const g226 = (g224 | g225);
    const g227 = (x1_3 ^ 1n);
    const g228 = (x1_3 & g226);
    const g229 = (g227 & g221);
    const g230 = (g228 | g229);
    const g231 = (x1_4 ^ 1n);
    const g232 = (x1_4 & x0_15);
    const g233 = (g231 & g230);
    const g234 = (g232 | g233);
    const g235 = (x1_2 ^ 1n);
    const g236 = (x1_2 & g172);
    const g237 = (g235 & g164);
    const g238 = (g236 | g237);
    const g239 = (x1_4 | x1_3);
    const g240 = (g239 ^ 1n);
    const g241 = (g239 & x0_15);
    const g242 = (g240 & g238);
    const g243 = (g241 | g242);
    const g244 = (g239 ^ 1n);
    const g245 = (g239 & x0_15);
    const g246 = (g244 & g55);
    const g247 = (g245 | g246);
    const g248 = (g239 ^ 1n);
    const g249 = (g239 & x0_15);
    const g250 = (g248 & g115);
    const g251 = (g249 | g250);
    const g252 = (g239 ^ 1n);
    const g253 = (g239 & x0_15);
    const g254 = (g252 & g148);
    const g255 = (g253 | g254);
    const g256 = (x1_3 | x1_2);
    const g257 = (x1_4 | g256);
    const g258 = (g257 ^ 1n);
    const g259 = (g257 & x0_15);
    const g260 = (g258 & g172);
    const g261 = (g259 | g260);
    const g262 = (g257 ^ 1n);
    const g263 = (g257 & x0_15);
    const g264 = (g262 & g51);
    const g265 = (g263 | g264);
    const g266 = (x1_3 | g205);
    const g267 = (x1_4 | g266);
    const g268 = (g267 ^ 1n);
    const g269 = (g267 & x0_15);
    const g270 = (g268 & g107);
    const g271 = (g269 | g270);
    const g272 = (x1_3 | g222);
    const g273 = (x1_4 | g272);
    const g274 = (g273 ^ 1n);
    const g275 = (g273 & x0_15);
    const g276 = (g274 & x0_14);
    const g277 = (g275 | g276);
    const w0 = x0_63;
    const w1 = cat(w0, x0_62, 1);
    const w2 = cat(w1, x0_61, 1);
    const w3 = cat(w2, x0_60, 1);
    const w4 = cat(w3, x0_59, 1);
    const w5 = cat(w4, x0_58, 1);
    const w6 = cat(w5, x0_57, 1);
    const w7 = cat(w6, x0_56, 1);
    const w8 = cat(w7, x0_55, 1);
    const w9 = cat(w8, x0_54, 1);
    const w10 = cat(w9, x0_53, 1);
    const w11 = cat(w10, x0_52, 1);
    const w12 = cat(w11, x0_51, 1);
    const w13 = cat(w12, x0_50, 1);
    const w14 = cat(w13, x0_49, 1);
    const w15 = cat(w14, x0_48, 1);
    const w16 = cat(w15, x0_47, 1);
    const w17 = cat(w16, x0_46, 1);
    const w18 = cat(w17, x0_45, 1);
    const w19 = cat(w18, x0_44, 1);
    const w20 = cat(w19, x0_43, 1);
    const w21 = cat(w20, x0_42, 1);
    const w22 = cat(w21, x0_41, 1);
    const w23 = cat(w22, x0_40, 1);
    const w24 = cat(w23, x0_39, 1);
    const w25 = cat(w24, x0_38, 1);
    const w26 = cat(w25, x0_37, 1);
    const w27 = cat(w26, x0_36, 1);
    const w28 = cat(w27, x0_35, 1);
    const w29 = cat(w28, x0_34, 1);
    const w30 = cat(w29, x0_33, 1);
    const w31 = cat(w30, x0_32, 1);
    const w32 = cat(w31, x0_31, 1);
    const w33 = cat(w32, x0_30, 1);
    const w34 = cat(w33, x0_29, 1);
    const w35 = cat(w34, x0_28, 1);
    const w36 = cat(w35, x0_27, 1);
    const w37 = cat(w36, x0_26, 1);
    const w38 = cat(w37, x0_25, 1);
    const w39 = cat(w38, x0_24, 1);
    const w40 = cat(w39, x0_23, 1);
    const w41 = cat(w40, x0_22, 1);
    const w42 = cat(w41, x0_21, 1);
    const w43 = cat(w42, x0_20, 1);
    const w44 = cat(w43, x0_19, 1);
    const w45 = cat(w44, x0_18, 1);
    const w46 = cat(w45, x0_17, 1);
    const w47 = cat(w46, x0_16, 1);
    const w48 = cat(w47, x0_15, 1);
    const w49 = cat(w48, g277, 1);
    const w50 = cat(w49, g271, 1);
    const w51 = cat(w50, g265, 1);
    const w52 = cat(w51, g261, 1);
    const w53 = cat(w52, g255, 1);
    const w54 = cat(w53, g251, 1);
    const w55 = cat(w54, g247, 1);
    const w56 = cat(w55, g243, 1);
    const w57 = cat(w56, g234, 1);
    const w58 = cat(w57, g217, 1);
    const w59 = cat(w58, g200, 1);
    const w60 = cat(w59, g184, 1);
    const w61 = cat(w60, g156, 1);
    const w62 = cat(w61, g123, 1);
    const w63 = cat(w62, g63, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_sar_cl_gpr_16__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
