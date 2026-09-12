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
// one named local per gate, over the term of add_gpr_gpr_32__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
function emu_add_gpr_gpr_32__reg_rdi__javascript(a, b) {
    const x0_0 = ext(a, 0, 0);
    const x1_0 = ext(b, 0, 0);
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
    const g0 = (x1_0 ^ x0_0);
    const g1 = (g0 ^ 1n);
    const g2 = (g1 ^ 1n);
    const g3 = (x1_0 ^ 1n);
    const g4 = (x0_0 ^ 1n);
    const g5 = (g4 | g3);
    const g6 = (x1_1 ^ g5);
    const g7 = (g6 ^ 1n);
    const g8 = (x0_1 ^ g7);
    const g9 = (g8 ^ 1n);
    const g10 = (g9 ^ 1n);
    const g11 = (x1_1 ^ 1n);
    const g12 = (g11 | g5);
    const g13 = (g12 ^ 1n);
    const g14 = (x0_1 ^ 1n);
    const g15 = (g14 | g5);
    const g16 = (g15 ^ 1n);
    const g17 = (g14 | g11);
    const g18 = (g17 ^ 1n);
    const g19 = (g18 | g16);
    const g20 = (g19 | g13);
    const g21 = (x1_2 ^ g20);
    const g22 = (g21 ^ 1n);
    const g23 = (x0_2 ^ g22);
    const g24 = (g23 ^ 1n);
    const g25 = (g20 ^ 1n);
    const g26 = (x1_2 ^ 1n);
    const g27 = (g26 | g25);
    const g28 = (g27 ^ 1n);
    const g29 = (x0_2 ^ 1n);
    const g30 = (g29 | g25);
    const g31 = (g30 ^ 1n);
    const g32 = (g29 | g26);
    const g33 = (g32 ^ 1n);
    const g34 = (g33 | g31);
    const g35 = (g34 | g28);
    const g36 = (x1_3 ^ g35);
    const g37 = (g36 ^ 1n);
    const g38 = (x0_3 ^ g37);
    const g39 = (g38 ^ 1n);
    const g40 = (g35 ^ 1n);
    const g41 = (x1_3 ^ 1n);
    const g42 = (g41 | g40);
    const g43 = (g42 ^ 1n);
    const g44 = (x0_3 ^ 1n);
    const g45 = (g44 | g40);
    const g46 = (g45 ^ 1n);
    const g47 = (g44 | g41);
    const g48 = (g47 ^ 1n);
    const g49 = (g48 | g46);
    const g50 = (g49 | g43);
    const g51 = (x1_4 ^ g50);
    const g52 = (g51 ^ 1n);
    const g53 = (x0_4 ^ g52);
    const g54 = (g53 ^ 1n);
    const g55 = (g50 ^ 1n);
    const g56 = (x1_4 ^ 1n);
    const g57 = (g56 | g55);
    const g58 = (g57 ^ 1n);
    const g59 = (x0_4 ^ 1n);
    const g60 = (g59 | g55);
    const g61 = (g60 ^ 1n);
    const g62 = (g59 | g56);
    const g63 = (g62 ^ 1n);
    const g64 = (g63 | g61);
    const g65 = (g64 | g58);
    const g66 = (x1_5 ^ g65);
    const g67 = (g66 ^ 1n);
    const g68 = (x0_5 ^ g67);
    const g69 = (g68 ^ 1n);
    const g70 = (g65 ^ 1n);
    const g71 = (x1_5 ^ 1n);
    const g72 = (g71 | g70);
    const g73 = (g72 ^ 1n);
    const g74 = (x0_5 ^ 1n);
    const g75 = (g74 | g70);
    const g76 = (g75 ^ 1n);
    const g77 = (g74 | g71);
    const g78 = (g77 ^ 1n);
    const g79 = (g78 | g76);
    const g80 = (g79 | g73);
    const g81 = (x1_6 ^ g80);
    const g82 = (g81 ^ 1n);
    const g83 = (x0_6 ^ g82);
    const g84 = (g83 ^ 1n);
    const g85 = (g80 ^ 1n);
    const g86 = (x1_6 ^ 1n);
    const g87 = (g86 | g85);
    const g88 = (g87 ^ 1n);
    const g89 = (x0_6 ^ 1n);
    const g90 = (g89 | g85);
    const g91 = (g90 ^ 1n);
    const g92 = (g89 | g86);
    const g93 = (g92 ^ 1n);
    const g94 = (g93 | g91);
    const g95 = (g94 | g88);
    const g96 = (x1_7 ^ g95);
    const g97 = (g96 ^ 1n);
    const g98 = (x0_7 ^ g97);
    const g99 = (g98 ^ 1n);
    const g100 = (g95 ^ 1n);
    const g101 = (x1_7 ^ 1n);
    const g102 = (g101 | g100);
    const g103 = (g102 ^ 1n);
    const g104 = (x0_7 ^ 1n);
    const g105 = (g104 | g100);
    const g106 = (g105 ^ 1n);
    const g107 = (g104 | g101);
    const g108 = (g107 ^ 1n);
    const g109 = (g108 | g106);
    const g110 = (g109 | g103);
    const g111 = (x1_8 ^ g110);
    const g112 = (g111 ^ 1n);
    const g113 = (x0_8 ^ g112);
    const g114 = (g113 ^ 1n);
    const g115 = (g110 ^ 1n);
    const g116 = (x1_8 ^ 1n);
    const g117 = (g116 | g115);
    const g118 = (g117 ^ 1n);
    const g119 = (x0_8 ^ 1n);
    const g120 = (g119 | g115);
    const g121 = (g120 ^ 1n);
    const g122 = (g119 | g116);
    const g123 = (g122 ^ 1n);
    const g124 = (g123 | g121);
    const g125 = (g124 | g118);
    const g126 = (x1_9 ^ g125);
    const g127 = (g126 ^ 1n);
    const g128 = (x0_9 ^ g127);
    const g129 = (g128 ^ 1n);
    const g130 = (g125 ^ 1n);
    const g131 = (x1_9 ^ 1n);
    const g132 = (g131 | g130);
    const g133 = (g132 ^ 1n);
    const g134 = (x0_9 ^ 1n);
    const g135 = (g134 | g130);
    const g136 = (g135 ^ 1n);
    const g137 = (g134 | g131);
    const g138 = (g137 ^ 1n);
    const g139 = (g138 | g136);
    const g140 = (g139 | g133);
    const g141 = (x1_10 ^ g140);
    const g142 = (g141 ^ 1n);
    const g143 = (x0_10 ^ g142);
    const g144 = (g143 ^ 1n);
    const g145 = (g140 ^ 1n);
    const g146 = (x1_10 ^ 1n);
    const g147 = (g146 | g145);
    const g148 = (g147 ^ 1n);
    const g149 = (x0_10 ^ 1n);
    const g150 = (g149 | g145);
    const g151 = (g150 ^ 1n);
    const g152 = (g149 | g146);
    const g153 = (g152 ^ 1n);
    const g154 = (g153 | g151);
    const g155 = (g154 | g148);
    const g156 = (x1_11 ^ g155);
    const g157 = (g156 ^ 1n);
    const g158 = (x0_11 ^ g157);
    const g159 = (g158 ^ 1n);
    const g160 = (g155 ^ 1n);
    const g161 = (x1_11 ^ 1n);
    const g162 = (g161 | g160);
    const g163 = (g162 ^ 1n);
    const g164 = (x0_11 ^ 1n);
    const g165 = (g164 | g160);
    const g166 = (g165 ^ 1n);
    const g167 = (g164 | g161);
    const g168 = (g167 ^ 1n);
    const g169 = (g168 | g166);
    const g170 = (g169 | g163);
    const g171 = (x1_12 ^ g170);
    const g172 = (g171 ^ 1n);
    const g173 = (x0_12 ^ g172);
    const g174 = (g173 ^ 1n);
    const g175 = (g170 ^ 1n);
    const g176 = (x1_12 ^ 1n);
    const g177 = (g176 | g175);
    const g178 = (g177 ^ 1n);
    const g179 = (x0_12 ^ 1n);
    const g180 = (g179 | g175);
    const g181 = (g180 ^ 1n);
    const g182 = (g179 | g176);
    const g183 = (g182 ^ 1n);
    const g184 = (g183 | g181);
    const g185 = (g184 | g178);
    const g186 = (x1_13 ^ g185);
    const g187 = (g186 ^ 1n);
    const g188 = (x0_13 ^ g187);
    const g189 = (g188 ^ 1n);
    const g190 = (g185 ^ 1n);
    const g191 = (x1_13 ^ 1n);
    const g192 = (g191 | g190);
    const g193 = (g192 ^ 1n);
    const g194 = (x0_13 ^ 1n);
    const g195 = (g194 | g190);
    const g196 = (g195 ^ 1n);
    const g197 = (g194 | g191);
    const g198 = (g197 ^ 1n);
    const g199 = (g198 | g196);
    const g200 = (g199 | g193);
    const g201 = (x1_14 ^ g200);
    const g202 = (g201 ^ 1n);
    const g203 = (x0_14 ^ g202);
    const g204 = (g203 ^ 1n);
    const g205 = (g200 ^ 1n);
    const g206 = (x1_14 ^ 1n);
    const g207 = (g206 | g205);
    const g208 = (g207 ^ 1n);
    const g209 = (x0_14 ^ 1n);
    const g210 = (g209 | g205);
    const g211 = (g210 ^ 1n);
    const g212 = (g209 | g206);
    const g213 = (g212 ^ 1n);
    const g214 = (g213 | g211);
    const g215 = (g214 | g208);
    const g216 = (x1_15 ^ g215);
    const g217 = (g216 ^ 1n);
    const g218 = (x0_15 ^ g217);
    const g219 = (g218 ^ 1n);
    const g220 = (g215 ^ 1n);
    const g221 = (x1_15 ^ 1n);
    const g222 = (g221 | g220);
    const g223 = (g222 ^ 1n);
    const g224 = (x0_15 ^ 1n);
    const g225 = (g224 | g220);
    const g226 = (g225 ^ 1n);
    const g227 = (g224 | g221);
    const g228 = (g227 ^ 1n);
    const g229 = (g228 | g226);
    const g230 = (g229 | g223);
    const g231 = (x1_16 ^ g230);
    const g232 = (g231 ^ 1n);
    const g233 = (x0_16 ^ g232);
    const g234 = (g233 ^ 1n);
    const g235 = (g230 ^ 1n);
    const g236 = (x1_16 ^ 1n);
    const g237 = (g236 | g235);
    const g238 = (g237 ^ 1n);
    const g239 = (x0_16 ^ 1n);
    const g240 = (g239 | g235);
    const g241 = (g240 ^ 1n);
    const g242 = (g239 | g236);
    const g243 = (g242 ^ 1n);
    const g244 = (g243 | g241);
    const g245 = (g244 | g238);
    const g246 = (x1_17 ^ g245);
    const g247 = (g246 ^ 1n);
    const g248 = (x0_17 ^ g247);
    const g249 = (g248 ^ 1n);
    const g250 = (g245 ^ 1n);
    const g251 = (x1_17 ^ 1n);
    const g252 = (g251 | g250);
    const g253 = (g252 ^ 1n);
    const g254 = (x0_17 ^ 1n);
    const g255 = (g254 | g250);
    const g256 = (g255 ^ 1n);
    const g257 = (g254 | g251);
    const g258 = (g257 ^ 1n);
    const g259 = (g258 | g256);
    const g260 = (g259 | g253);
    const g261 = (x1_18 ^ g260);
    const g262 = (g261 ^ 1n);
    const g263 = (x0_18 ^ g262);
    const g264 = (g263 ^ 1n);
    const g265 = (g260 ^ 1n);
    const g266 = (x1_18 ^ 1n);
    const g267 = (g266 | g265);
    const g268 = (g267 ^ 1n);
    const g269 = (x0_18 ^ 1n);
    const g270 = (g269 | g265);
    const g271 = (g270 ^ 1n);
    const g272 = (g269 | g266);
    const g273 = (g272 ^ 1n);
    const g274 = (g273 | g271);
    const g275 = (g274 | g268);
    const g276 = (x1_19 ^ g275);
    const g277 = (g276 ^ 1n);
    const g278 = (x0_19 ^ g277);
    const g279 = (g278 ^ 1n);
    const g280 = (g275 ^ 1n);
    const g281 = (x1_19 ^ 1n);
    const g282 = (g281 | g280);
    const g283 = (g282 ^ 1n);
    const g284 = (x0_19 ^ 1n);
    const g285 = (g284 | g280);
    const g286 = (g285 ^ 1n);
    const g287 = (g284 | g281);
    const g288 = (g287 ^ 1n);
    const g289 = (g288 | g286);
    const g290 = (g289 | g283);
    const g291 = (x1_20 ^ g290);
    const g292 = (g291 ^ 1n);
    const g293 = (x0_20 ^ g292);
    const g294 = (g293 ^ 1n);
    const g295 = (g290 ^ 1n);
    const g296 = (x1_20 ^ 1n);
    const g297 = (g296 | g295);
    const g298 = (g297 ^ 1n);
    const g299 = (x0_20 ^ 1n);
    const g300 = (g299 | g295);
    const g301 = (g300 ^ 1n);
    const g302 = (g299 | g296);
    const g303 = (g302 ^ 1n);
    const g304 = (g303 | g301);
    const g305 = (g304 | g298);
    const g306 = (x1_21 ^ g305);
    const g307 = (g306 ^ 1n);
    const g308 = (x0_21 ^ g307);
    const g309 = (g308 ^ 1n);
    const g310 = (g305 ^ 1n);
    const g311 = (x1_21 ^ 1n);
    const g312 = (g311 | g310);
    const g313 = (g312 ^ 1n);
    const g314 = (x0_21 ^ 1n);
    const g315 = (g314 | g310);
    const g316 = (g315 ^ 1n);
    const g317 = (g314 | g311);
    const g318 = (g317 ^ 1n);
    const g319 = (g318 | g316);
    const g320 = (g319 | g313);
    const g321 = (x1_22 ^ g320);
    const g322 = (g321 ^ 1n);
    const g323 = (x0_22 ^ g322);
    const g324 = (g323 ^ 1n);
    const g325 = (g320 ^ 1n);
    const g326 = (x1_22 ^ 1n);
    const g327 = (g326 | g325);
    const g328 = (g327 ^ 1n);
    const g329 = (x0_22 ^ 1n);
    const g330 = (g329 | g325);
    const g331 = (g330 ^ 1n);
    const g332 = (g329 | g326);
    const g333 = (g332 ^ 1n);
    const g334 = (g333 | g331);
    const g335 = (g334 | g328);
    const g336 = (x1_23 ^ g335);
    const g337 = (g336 ^ 1n);
    const g338 = (x0_23 ^ g337);
    const g339 = (g338 ^ 1n);
    const g340 = (g335 ^ 1n);
    const g341 = (x1_23 ^ 1n);
    const g342 = (g341 | g340);
    const g343 = (g342 ^ 1n);
    const g344 = (x0_23 ^ 1n);
    const g345 = (g344 | g340);
    const g346 = (g345 ^ 1n);
    const g347 = (g344 | g341);
    const g348 = (g347 ^ 1n);
    const g349 = (g348 | g346);
    const g350 = (g349 | g343);
    const g351 = (x1_24 ^ g350);
    const g352 = (g351 ^ 1n);
    const g353 = (x0_24 ^ g352);
    const g354 = (g353 ^ 1n);
    const g355 = (g350 ^ 1n);
    const g356 = (x1_24 ^ 1n);
    const g357 = (g356 | g355);
    const g358 = (g357 ^ 1n);
    const g359 = (x0_24 ^ 1n);
    const g360 = (g359 | g355);
    const g361 = (g360 ^ 1n);
    const g362 = (g359 | g356);
    const g363 = (g362 ^ 1n);
    const g364 = (g363 | g361);
    const g365 = (g364 | g358);
    const g366 = (x1_25 ^ g365);
    const g367 = (g366 ^ 1n);
    const g368 = (x0_25 ^ g367);
    const g369 = (g368 ^ 1n);
    const g370 = (g365 ^ 1n);
    const g371 = (x1_25 ^ 1n);
    const g372 = (g371 | g370);
    const g373 = (g372 ^ 1n);
    const g374 = (x0_25 ^ 1n);
    const g375 = (g374 | g370);
    const g376 = (g375 ^ 1n);
    const g377 = (g374 | g371);
    const g378 = (g377 ^ 1n);
    const g379 = (g378 | g376);
    const g380 = (g379 | g373);
    const g381 = (x1_26 ^ g380);
    const g382 = (g381 ^ 1n);
    const g383 = (x0_26 ^ g382);
    const g384 = (g383 ^ 1n);
    const g385 = (g380 ^ 1n);
    const g386 = (x1_26 ^ 1n);
    const g387 = (g386 | g385);
    const g388 = (g387 ^ 1n);
    const g389 = (x0_26 ^ 1n);
    const g390 = (g389 | g385);
    const g391 = (g390 ^ 1n);
    const g392 = (g389 | g386);
    const g393 = (g392 ^ 1n);
    const g394 = (g393 | g391);
    const g395 = (g394 | g388);
    const g396 = (x1_27 ^ g395);
    const g397 = (g396 ^ 1n);
    const g398 = (x0_27 ^ g397);
    const g399 = (g398 ^ 1n);
    const g400 = (g395 ^ 1n);
    const g401 = (x1_27 ^ 1n);
    const g402 = (g401 | g400);
    const g403 = (g402 ^ 1n);
    const g404 = (x0_27 ^ 1n);
    const g405 = (g404 | g400);
    const g406 = (g405 ^ 1n);
    const g407 = (g404 | g401);
    const g408 = (g407 ^ 1n);
    const g409 = (g408 | g406);
    const g410 = (g409 | g403);
    const g411 = (x1_28 ^ g410);
    const g412 = (g411 ^ 1n);
    const g413 = (x0_28 ^ g412);
    const g414 = (g413 ^ 1n);
    const g415 = (g410 ^ 1n);
    const g416 = (x1_28 ^ 1n);
    const g417 = (g416 | g415);
    const g418 = (g417 ^ 1n);
    const g419 = (x0_28 ^ 1n);
    const g420 = (g419 | g415);
    const g421 = (g420 ^ 1n);
    const g422 = (g419 | g416);
    const g423 = (g422 ^ 1n);
    const g424 = (g423 | g421);
    const g425 = (g424 | g418);
    const g426 = (x1_29 ^ g425);
    const g427 = (g426 ^ 1n);
    const g428 = (x0_29 ^ g427);
    const g429 = (g428 ^ 1n);
    const g430 = (g425 ^ 1n);
    const g431 = (x1_29 ^ 1n);
    const g432 = (g431 | g430);
    const g433 = (g432 ^ 1n);
    const g434 = (x0_29 ^ 1n);
    const g435 = (g434 | g430);
    const g436 = (g435 ^ 1n);
    const g437 = (g434 | g431);
    const g438 = (g437 ^ 1n);
    const g439 = (g438 | g436);
    const g440 = (g439 | g433);
    const g441 = (x1_30 ^ g440);
    const g442 = (g441 ^ 1n);
    const g443 = (x0_30 ^ g442);
    const g444 = (g443 ^ 1n);
    const g445 = (g440 ^ 1n);
    const g446 = (x1_30 ^ 1n);
    const g447 = (g446 | g445);
    const g448 = (g447 ^ 1n);
    const g449 = (x0_30 ^ 1n);
    const g450 = (g449 | g445);
    const g451 = (g450 ^ 1n);
    const g452 = (g449 | g446);
    const g453 = (g452 ^ 1n);
    const g454 = (g453 | g451);
    const g455 = (g454 | g448);
    const g456 = (x1_31 ^ g455);
    const g457 = (g456 ^ 1n);
    const g458 = (x0_31 ^ g457);
    const g459 = (g458 ^ 1n);
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
    const w32 = cat(w31, g459, 1);
    const w33 = cat(w32, g444, 1);
    const w34 = cat(w33, g429, 1);
    const w35 = cat(w34, g414, 1);
    const w36 = cat(w35, g399, 1);
    const w37 = cat(w36, g384, 1);
    const w38 = cat(w37, g369, 1);
    const w39 = cat(w38, g354, 1);
    const w40 = cat(w39, g339, 1);
    const w41 = cat(w40, g324, 1);
    const w42 = cat(w41, g309, 1);
    const w43 = cat(w42, g294, 1);
    const w44 = cat(w43, g279, 1);
    const w45 = cat(w44, g264, 1);
    const w46 = cat(w45, g249, 1);
    const w47 = cat(w46, g234, 1);
    const w48 = cat(w47, g219, 1);
    const w49 = cat(w48, g204, 1);
    const w50 = cat(w49, g189, 1);
    const w51 = cat(w50, g174, 1);
    const w52 = cat(w51, g159, 1);
    const w53 = cat(w52, g144, 1);
    const w54 = cat(w53, g129, 1);
    const w55 = cat(w54, g114, 1);
    const w56 = cat(w55, g99, 1);
    const w57 = cat(w56, g84, 1);
    const w58 = cat(w57, g69, 1);
    const w59 = cat(w58, g54, 1);
    const w60 = cat(w59, g39, 1);
    const w61 = cat(w60, g24, 1);
    const w62 = cat(w61, g10, 1);
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
        out.push(emu_add_gpr_gpr_32__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
