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
// one named local per gate, over the term of sbb_imm_gpr_8__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v3), Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3))
function emu_sbb_imm_gpr_8__reg_rdi__javascript(a, b, c, d) {
    const x3_0 = ext(c, 0, 0);
    const x2_0 = ext(d, 0, 0);
    const x1_0 = ext(a, 0, 0);
    const x0_0 = ext(b, 0, 0);
    const x1_1 = ext(a, 1, 1);
    const x0_1 = ext(b, 1, 1);
    const x1_2 = ext(a, 2, 2);
    const x0_2 = ext(b, 2, 2);
    const x1_3 = ext(a, 3, 3);
    const x0_3 = ext(b, 3, 3);
    const x1_4 = ext(a, 4, 4);
    const x0_4 = ext(b, 4, 4);
    const x1_5 = ext(a, 5, 5);
    const x0_5 = ext(b, 5, 5);
    const x1_6 = ext(a, 6, 6);
    const x0_6 = ext(b, 6, 6);
    const x1_7 = ext(a, 7, 7);
    const x0_7 = ext(b, 7, 7);
    const x3_1 = ext(c, 1, 1);
    const x2_1 = ext(d, 1, 1);
    const x2_2 = ext(d, 2, 2);
    const x3_2 = ext(c, 2, 2);
    const x2_3 = ext(d, 3, 3);
    const x3_3 = ext(c, 3, 3);
    const x2_4 = ext(d, 4, 4);
    const x3_4 = ext(c, 4, 4);
    const x2_5 = ext(d, 5, 5);
    const x3_5 = ext(c, 5, 5);
    const x2_6 = ext(d, 6, 6);
    const x3_6 = ext(c, 6, 6);
    const x2_7 = ext(d, 7, 7);
    const x3_7 = ext(c, 7, 7);
    const x3_8 = ext(c, 8, 8);
    const x3_9 = ext(c, 9, 9);
    const x3_10 = ext(c, 10, 10);
    const x3_11 = ext(c, 11, 11);
    const x3_12 = ext(c, 12, 12);
    const x3_13 = ext(c, 13, 13);
    const x3_14 = ext(c, 14, 14);
    const x3_15 = ext(c, 15, 15);
    const x3_16 = ext(c, 16, 16);
    const x3_17 = ext(c, 17, 17);
    const x3_18 = ext(c, 18, 18);
    const x3_19 = ext(c, 19, 19);
    const x3_20 = ext(c, 20, 20);
    const x3_21 = ext(c, 21, 21);
    const x3_22 = ext(c, 22, 22);
    const x3_23 = ext(c, 23, 23);
    const x3_24 = ext(c, 24, 24);
    const x3_25 = ext(c, 25, 25);
    const x3_26 = ext(c, 26, 26);
    const x3_27 = ext(c, 27, 27);
    const x3_28 = ext(c, 28, 28);
    const x3_29 = ext(c, 29, 29);
    const x3_30 = ext(c, 30, 30);
    const x3_31 = ext(c, 31, 31);
    const x3_32 = ext(c, 32, 32);
    const x3_33 = ext(c, 33, 33);
    const x3_34 = ext(c, 34, 34);
    const x3_35 = ext(c, 35, 35);
    const x3_36 = ext(c, 36, 36);
    const x3_37 = ext(c, 37, 37);
    const x3_38 = ext(c, 38, 38);
    const x3_39 = ext(c, 39, 39);
    const x3_40 = ext(c, 40, 40);
    const x3_41 = ext(c, 41, 41);
    const x3_42 = ext(c, 42, 42);
    const x3_43 = ext(c, 43, 43);
    const x3_44 = ext(c, 44, 44);
    const x3_45 = ext(c, 45, 45);
    const x3_46 = ext(c, 46, 46);
    const x3_47 = ext(c, 47, 47);
    const x3_48 = ext(c, 48, 48);
    const x3_49 = ext(c, 49, 49);
    const x3_50 = ext(c, 50, 50);
    const x3_51 = ext(c, 51, 51);
    const x3_52 = ext(c, 52, 52);
    const x3_53 = ext(c, 53, 53);
    const x3_54 = ext(c, 54, 54);
    const x3_55 = ext(c, 55, 55);
    const x3_56 = ext(c, 56, 56);
    const x3_57 = ext(c, 57, 57);
    const x3_58 = ext(c, 58, 58);
    const x3_59 = ext(c, 59, 59);
    const x3_60 = ext(c, 60, 60);
    const x3_61 = ext(c, 61, 61);
    const x3_62 = ext(c, 62, 62);
    const x3_63 = ext(c, 63, 63);
    const g0 = (x2_0 ^ x3_0);
    const g1 = (g0 ^ 1n);
    const g2 = (x1_0 ^ 1n);
    const g3 = (x0_0 ^ 1n);
    const g4 = (g3 | g2);
    const g5 = (x1_1 ^ 1n);
    const g6 = (g5 | g4);
    const g7 = (g6 ^ 1n);
    const g8 = (x0_1 ^ 1n);
    const g9 = (g8 | g4);
    const g10 = (g9 ^ 1n);
    const g11 = (g8 | g5);
    const g12 = (g11 ^ 1n);
    const g13 = (g12 | g10);
    const g14 = (g13 | g7);
    const g15 = (g14 ^ 1n);
    const g16 = (x1_2 ^ 1n);
    const g17 = (g16 | g15);
    const g18 = (g17 ^ 1n);
    const g19 = (x0_2 ^ 1n);
    const g20 = (g19 | g15);
    const g21 = (g20 ^ 1n);
    const g22 = (g19 | g16);
    const g23 = (g22 ^ 1n);
    const g24 = (g23 | g21);
    const g25 = (g24 | g18);
    const g26 = (g25 ^ 1n);
    const g27 = (x1_3 ^ 1n);
    const g28 = (g27 | g26);
    const g29 = (g28 ^ 1n);
    const g30 = (x0_3 ^ 1n);
    const g31 = (g30 | g26);
    const g32 = (g31 ^ 1n);
    const g33 = (g30 | g27);
    const g34 = (g33 ^ 1n);
    const g35 = (g34 | g32);
    const g36 = (g35 | g29);
    const g37 = (g36 ^ 1n);
    const g38 = (x1_4 ^ 1n);
    const g39 = (g38 | g37);
    const g40 = (g39 ^ 1n);
    const g41 = (x0_4 ^ 1n);
    const g42 = (g41 | g37);
    const g43 = (g42 ^ 1n);
    const g44 = (g41 | g38);
    const g45 = (g44 ^ 1n);
    const g46 = (g45 | g43);
    const g47 = (g46 | g40);
    const g48 = (g47 ^ 1n);
    const g49 = (x1_5 ^ 1n);
    const g50 = (g49 | g48);
    const g51 = (g50 ^ 1n);
    const g52 = (x0_5 ^ 1n);
    const g53 = (g52 | g48);
    const g54 = (g53 ^ 1n);
    const g55 = (g52 | g49);
    const g56 = (g55 ^ 1n);
    const g57 = (g56 | g54);
    const g58 = (g57 | g51);
    const g59 = (g58 ^ 1n);
    const g60 = (x1_6 ^ 1n);
    const g61 = (g60 | g59);
    const g62 = (g61 ^ 1n);
    const g63 = (x0_6 ^ 1n);
    const g64 = (g63 | g59);
    const g65 = (g64 ^ 1n);
    const g66 = (g63 | g60);
    const g67 = (g66 ^ 1n);
    const g68 = (g67 | g65);
    const g69 = (g68 | g62);
    const g70 = (g69 ^ 1n);
    const g71 = (x1_7 ^ 1n);
    const g72 = (g71 | g70);
    const g73 = (g72 ^ 1n);
    const g74 = (x0_7 ^ 1n);
    const g75 = (g74 | g70);
    const g76 = (g75 ^ 1n);
    const g77 = (g74 | g71);
    const g78 = (g77 ^ 1n);
    const g79 = (g78 | g76);
    const g80 = (g79 | g73);
    const g81 = (g80 ^ g1);
    const g82 = (g81 ^ 1n);
    const g83 = (x2_0 ^ g80);
    const g84 = (g83 ^ 1n);
    const g85 = (x3_0 ^ 1n);
    const g86 = (g85 | g84);
    const g87 = (x3_1 ^ g86);
    const g88 = (g87 ^ 1n);
    const g89 = (g80 ^ 1n);
    const g90 = (x2_0 ^ 1n);
    const g91 = (g90 | g89);
    const g92 = (g80 ^ g91);
    const g93 = (g92 ^ 1n);
    const g94 = (x2_0 ^ x2_1);
    const g95 = (g94 ^ 1n);
    const g96 = (g95 ^ g93);
    const g97 = (g96 ^ 1n);
    const g98 = (g97 ^ g88);
    const g99 = (g98 ^ 1n);
    const g100 = (g99 ^ 1n);
    const g101 = (x2_0 | x2_1);
    const g102 = (g101 ^ x2_2);
    const g103 = (g102 ^ 1n);
    const g104 = (g95 | g91);
    const g105 = (g104 ^ 1n);
    const g106 = (g89 | g91);
    const g107 = (g106 ^ 1n);
    const g108 = (g89 | g95);
    const g109 = (g108 ^ 1n);
    const g110 = (g109 | g107);
    const g111 = (g110 | g105);
    const g112 = (g80 ^ g111);
    const g113 = (g112 ^ 1n);
    const g114 = (g113 ^ g103);
    const g115 = (g114 ^ 1n);
    const g116 = (x3_1 ^ 1n);
    const g117 = (g116 | g86);
    const g118 = (g117 ^ 1n);
    const g119 = (g97 ^ 1n);
    const g120 = (g116 | g119);
    const g121 = (g120 ^ 1n);
    const g122 = (g119 | g86);
    const g123 = (g122 ^ 1n);
    const g124 = (g123 | g121);
    const g125 = (g124 | g118);
    const g126 = (x3_2 ^ g125);
    const g127 = (g126 ^ 1n);
    const g128 = (g127 ^ g115);
    const g129 = (g128 ^ 1n);
    const g130 = (g129 ^ 1n);
    const g131 = (x2_2 | g101);
    const g132 = (g131 ^ x2_3);
    const g133 = (g132 ^ 1n);
    const g134 = (g111 ^ 1n);
    const g135 = (g103 | g134);
    const g136 = (g135 ^ 1n);
    const g137 = (g89 | g134);
    const g138 = (g137 ^ 1n);
    const g139 = (g89 | g103);
    const g140 = (g139 ^ 1n);
    const g141 = (g140 | g138);
    const g142 = (g141 | g136);
    const g143 = (g80 ^ g142);
    const g144 = (g143 ^ 1n);
    const g145 = (g144 ^ g133);
    const g146 = (g145 ^ 1n);
    const g147 = (g125 ^ 1n);
    const g148 = (x3_2 ^ 1n);
    const g149 = (g148 | g147);
    const g150 = (g149 ^ 1n);
    const g151 = (g115 | g148);
    const g152 = (g151 ^ 1n);
    const g153 = (g115 | g147);
    const g154 = (g153 ^ 1n);
    const g155 = (g154 | g152);
    const g156 = (g155 | g150);
    const g157 = (x3_3 ^ g156);
    const g158 = (g157 ^ 1n);
    const g159 = (g158 ^ g146);
    const g160 = (g159 ^ 1n);
    const g161 = (g160 ^ 1n);
    const g162 = (x2_3 | g131);
    const g163 = (g162 ^ x2_4);
    const g164 = (g163 ^ 1n);
    const g165 = (g142 ^ 1n);
    const g166 = (g165 | g133);
    const g167 = (g166 ^ 1n);
    const g168 = (g89 | g165);
    const g169 = (g168 ^ 1n);
    const g170 = (g89 | g133);
    const g171 = (g170 ^ 1n);
    const g172 = (g171 | g169);
    const g173 = (g172 | g167);
    const g174 = (g80 ^ g173);
    const g175 = (g174 ^ 1n);
    const g176 = (g175 ^ g164);
    const g177 = (g176 ^ 1n);
    const g178 = (g156 ^ 1n);
    const g179 = (x3_3 ^ 1n);
    const g180 = (g179 | g178);
    const g181 = (g180 ^ 1n);
    const g182 = (g146 | g179);
    const g183 = (g182 ^ 1n);
    const g184 = (g146 | g178);
    const g185 = (g184 ^ 1n);
    const g186 = (g185 | g183);
    const g187 = (g186 | g181);
    const g188 = (x3_4 ^ g187);
    const g189 = (g188 ^ 1n);
    const g190 = (g189 ^ g177);
    const g191 = (g190 ^ 1n);
    const g192 = (g191 ^ 1n);
    const g193 = (x2_4 | g162);
    const g194 = (g193 ^ x2_5);
    const g195 = (g194 ^ 1n);
    const g196 = (g173 ^ 1n);
    const g197 = (g89 | g196);
    const g198 = (g197 ^ 1n);
    const g199 = (g89 | g164);
    const g200 = (g199 ^ 1n);
    const g201 = (g196 | g164);
    const g202 = (g201 ^ 1n);
    const g203 = (g202 | g200);
    const g204 = (g203 | g198);
    const g205 = (g80 ^ g204);
    const g206 = (g205 ^ 1n);
    const g207 = (g206 ^ g195);
    const g208 = (g207 ^ 1n);
    const g209 = (g187 ^ 1n);
    const g210 = (g209 | g177);
    const g211 = (g210 ^ 1n);
    const g212 = (x3_4 ^ 1n);
    const g213 = (g212 | g177);
    const g214 = (g213 ^ 1n);
    const g215 = (g212 | g209);
    const g216 = (g215 ^ 1n);
    const g217 = (g216 | g214);
    const g218 = (g217 | g211);
    const g219 = (x3_5 ^ g218);
    const g220 = (g219 ^ 1n);
    const g221 = (g220 ^ g208);
    const g222 = (g221 ^ 1n);
    const g223 = (g222 ^ 1n);
    const g224 = (x2_5 | g193);
    const g225 = (g224 ^ x2_6);
    const g226 = (g225 ^ 1n);
    const g227 = (g204 ^ 1n);
    const g228 = (g195 | g227);
    const g229 = (g228 ^ 1n);
    const g230 = (g89 | g227);
    const g231 = (g230 ^ 1n);
    const g232 = (g89 | g195);
    const g233 = (g232 ^ 1n);
    const g234 = (g233 | g231);
    const g235 = (g234 | g229);
    const g236 = (g80 ^ g235);
    const g237 = (g236 ^ 1n);
    const g238 = (g237 ^ g226);
    const g239 = (g238 ^ 1n);
    const g240 = (g218 ^ 1n);
    const g241 = (g208 | g240);
    const g242 = (g241 ^ 1n);
    const g243 = (x3_5 ^ 1n);
    const g244 = (g208 | g243);
    const g245 = (g244 ^ 1n);
    const g246 = (g243 | g240);
    const g247 = (g246 ^ 1n);
    const g248 = (g247 | g245);
    const g249 = (g248 | g242);
    const g250 = (x3_6 ^ g249);
    const g251 = (g250 ^ 1n);
    const g252 = (g251 ^ g239);
    const g253 = (g252 ^ 1n);
    const g254 = (g253 ^ 1n);
    const g255 = (x2_6 | g224);
    const g256 = (g255 ^ x2_7);
    const g257 = (g256 ^ 1n);
    const g258 = (g89 | g226);
    const g259 = (g258 ^ 1n);
    const g260 = (g235 ^ 1n);
    const g261 = (g226 | g260);
    const g262 = (g261 ^ 1n);
    const g263 = (g89 | g260);
    const g264 = (g263 ^ 1n);
    const g265 = (g264 | g262);
    const g266 = (g265 | g259);
    const g267 = (g80 ^ g266);
    const g268 = (g267 ^ 1n);
    const g269 = (g268 ^ g257);
    const g270 = (g269 ^ 1n);
    const g271 = (g249 ^ 1n);
    const g272 = (g239 | g271);
    const g273 = (g272 ^ 1n);
    const g274 = (x3_6 ^ 1n);
    const g275 = (g274 | g271);
    const g276 = (g275 ^ 1n);
    const g277 = (g239 | g274);
    const g278 = (g277 ^ 1n);
    const g279 = (g278 | g276);
    const g280 = (g279 | g273);
    const g281 = (x3_7 ^ g280);
    const g282 = (g281 ^ 1n);
    const g283 = (g282 ^ g270);
    const g284 = (g283 ^ 1n);
    const g285 = (g284 ^ 1n);
    const w0 = x3_63;
    const w1 = cat(w0, x3_62, 1);
    const w2 = cat(w1, x3_61, 1);
    const w3 = cat(w2, x3_60, 1);
    const w4 = cat(w3, x3_59, 1);
    const w5 = cat(w4, x3_58, 1);
    const w6 = cat(w5, x3_57, 1);
    const w7 = cat(w6, x3_56, 1);
    const w8 = cat(w7, x3_55, 1);
    const w9 = cat(w8, x3_54, 1);
    const w10 = cat(w9, x3_53, 1);
    const w11 = cat(w10, x3_52, 1);
    const w12 = cat(w11, x3_51, 1);
    const w13 = cat(w12, x3_50, 1);
    const w14 = cat(w13, x3_49, 1);
    const w15 = cat(w14, x3_48, 1);
    const w16 = cat(w15, x3_47, 1);
    const w17 = cat(w16, x3_46, 1);
    const w18 = cat(w17, x3_45, 1);
    const w19 = cat(w18, x3_44, 1);
    const w20 = cat(w19, x3_43, 1);
    const w21 = cat(w20, x3_42, 1);
    const w22 = cat(w21, x3_41, 1);
    const w23 = cat(w22, x3_40, 1);
    const w24 = cat(w23, x3_39, 1);
    const w25 = cat(w24, x3_38, 1);
    const w26 = cat(w25, x3_37, 1);
    const w27 = cat(w26, x3_36, 1);
    const w28 = cat(w27, x3_35, 1);
    const w29 = cat(w28, x3_34, 1);
    const w30 = cat(w29, x3_33, 1);
    const w31 = cat(w30, x3_32, 1);
    const w32 = cat(w31, x3_31, 1);
    const w33 = cat(w32, x3_30, 1);
    const w34 = cat(w33, x3_29, 1);
    const w35 = cat(w34, x3_28, 1);
    const w36 = cat(w35, x3_27, 1);
    const w37 = cat(w36, x3_26, 1);
    const w38 = cat(w37, x3_25, 1);
    const w39 = cat(w38, x3_24, 1);
    const w40 = cat(w39, x3_23, 1);
    const w41 = cat(w40, x3_22, 1);
    const w42 = cat(w41, x3_21, 1);
    const w43 = cat(w42, x3_20, 1);
    const w44 = cat(w43, x3_19, 1);
    const w45 = cat(w44, x3_18, 1);
    const w46 = cat(w45, x3_17, 1);
    const w47 = cat(w46, x3_16, 1);
    const w48 = cat(w47, x3_15, 1);
    const w49 = cat(w48, x3_14, 1);
    const w50 = cat(w49, x3_13, 1);
    const w51 = cat(w50, x3_12, 1);
    const w52 = cat(w51, x3_11, 1);
    const w53 = cat(w52, x3_10, 1);
    const w54 = cat(w53, x3_9, 1);
    const w55 = cat(w54, x3_8, 1);
    const w56 = cat(w55, g285, 1);
    const w57 = cat(w56, g254, 1);
    const w58 = cat(w57, g223, 1);
    const w59 = cat(w58, g192, 1);
    const w60 = cat(w59, g161, 1);
    const w61 = cat(w60, g130, 1);
    const w62 = cat(w61, g100, 1);
    const w63 = cat(w62, g82, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_sbb_imm_gpr_8__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
