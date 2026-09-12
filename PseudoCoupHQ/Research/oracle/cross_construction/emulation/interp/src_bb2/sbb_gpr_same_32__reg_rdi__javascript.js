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
// one named local per gate, over the term of sbb_gpr_same_32__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1, 1, 0)*4294967295)
function emu_sbb_gpr_same_32__reg_rdi__javascript(a, b, c) {
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
    const x1_8 = ext(a, 8, 8);
    const x0_8 = ext(b, 8, 8);
    const x1_9 = ext(a, 9, 9);
    const x0_9 = ext(b, 9, 9);
    const x1_10 = ext(a, 10, 10);
    const x0_10 = ext(b, 10, 10);
    const x1_11 = ext(a, 11, 11);
    const x0_11 = ext(b, 11, 11);
    const x1_12 = ext(a, 12, 12);
    const x0_12 = ext(b, 12, 12);
    const x1_13 = ext(a, 13, 13);
    const x0_13 = ext(b, 13, 13);
    const x1_14 = ext(a, 14, 14);
    const x0_14 = ext(b, 14, 14);
    const x1_15 = ext(a, 15, 15);
    const x0_15 = ext(b, 15, 15);
    const x1_16 = ext(a, 16, 16);
    const x0_16 = ext(b, 16, 16);
    const x1_17 = ext(a, 17, 17);
    const x0_17 = ext(b, 17, 17);
    const x1_18 = ext(a, 18, 18);
    const x0_18 = ext(b, 18, 18);
    const x1_19 = ext(a, 19, 19);
    const x0_19 = ext(b, 19, 19);
    const x1_20 = ext(a, 20, 20);
    const x0_20 = ext(b, 20, 20);
    const x1_21 = ext(a, 21, 21);
    const x0_21 = ext(b, 21, 21);
    const x1_22 = ext(a, 22, 22);
    const x0_22 = ext(b, 22, 22);
    const x1_23 = ext(a, 23, 23);
    const x0_23 = ext(b, 23, 23);
    const x1_24 = ext(a, 24, 24);
    const x0_24 = ext(b, 24, 24);
    const x1_25 = ext(a, 25, 25);
    const x0_25 = ext(b, 25, 25);
    const x1_26 = ext(a, 26, 26);
    const x0_26 = ext(b, 26, 26);
    const x1_27 = ext(a, 27, 27);
    const x0_27 = ext(b, 27, 27);
    const x1_28 = ext(a, 28, 28);
    const x0_28 = ext(b, 28, 28);
    const x1_29 = ext(a, 29, 29);
    const x0_29 = ext(b, 29, 29);
    const x1_30 = ext(a, 30, 30);
    const x0_30 = ext(b, 30, 30);
    const x1_31 = ext(a, 31, 31);
    const x0_31 = ext(b, 31, 31);
    const g0 = (x1_0 ^ 1n);
    const g1 = (x0_0 ^ 1n);
    const g2 = (g1 | g0);
    const g3 = (x1_1 ^ 1n);
    const g4 = (g3 | g2);
    const g5 = (g4 ^ 1n);
    const g6 = (x0_1 ^ 1n);
    const g7 = (g6 | g2);
    const g8 = (g7 ^ 1n);
    const g9 = (g6 | g3);
    const g10 = (g9 ^ 1n);
    const g11 = (g10 | g8);
    const g12 = (g11 | g5);
    const g13 = (g12 ^ 1n);
    const g14 = (x1_2 ^ 1n);
    const g15 = (g14 | g13);
    const g16 = (g15 ^ 1n);
    const g17 = (x0_2 ^ 1n);
    const g18 = (g17 | g13);
    const g19 = (g18 ^ 1n);
    const g20 = (g17 | g14);
    const g21 = (g20 ^ 1n);
    const g22 = (g21 | g19);
    const g23 = (g22 | g16);
    const g24 = (g23 ^ 1n);
    const g25 = (x1_3 ^ 1n);
    const g26 = (g25 | g24);
    const g27 = (g26 ^ 1n);
    const g28 = (x0_3 ^ 1n);
    const g29 = (g28 | g24);
    const g30 = (g29 ^ 1n);
    const g31 = (g28 | g25);
    const g32 = (g31 ^ 1n);
    const g33 = (g32 | g30);
    const g34 = (g33 | g27);
    const g35 = (g34 ^ 1n);
    const g36 = (x1_4 ^ 1n);
    const g37 = (g36 | g35);
    const g38 = (g37 ^ 1n);
    const g39 = (x0_4 ^ 1n);
    const g40 = (g39 | g35);
    const g41 = (g40 ^ 1n);
    const g42 = (g39 | g36);
    const g43 = (g42 ^ 1n);
    const g44 = (g43 | g41);
    const g45 = (g44 | g38);
    const g46 = (g45 ^ 1n);
    const g47 = (x1_5 ^ 1n);
    const g48 = (g47 | g46);
    const g49 = (g48 ^ 1n);
    const g50 = (x0_5 ^ 1n);
    const g51 = (g50 | g46);
    const g52 = (g51 ^ 1n);
    const g53 = (g50 | g47);
    const g54 = (g53 ^ 1n);
    const g55 = (g54 | g52);
    const g56 = (g55 | g49);
    const g57 = (g56 ^ 1n);
    const g58 = (x1_6 ^ 1n);
    const g59 = (g58 | g57);
    const g60 = (g59 ^ 1n);
    const g61 = (x0_6 ^ 1n);
    const g62 = (g61 | g57);
    const g63 = (g62 ^ 1n);
    const g64 = (g61 | g58);
    const g65 = (g64 ^ 1n);
    const g66 = (g65 | g63);
    const g67 = (g66 | g60);
    const g68 = (g67 ^ 1n);
    const g69 = (x1_7 ^ 1n);
    const g70 = (g69 | g68);
    const g71 = (g70 ^ 1n);
    const g72 = (x0_7 ^ 1n);
    const g73 = (g72 | g68);
    const g74 = (g73 ^ 1n);
    const g75 = (g72 | g69);
    const g76 = (g75 ^ 1n);
    const g77 = (g76 | g74);
    const g78 = (g77 | g71);
    const g79 = (g78 ^ 1n);
    const g80 = (x1_8 ^ 1n);
    const g81 = (g80 | g79);
    const g82 = (g81 ^ 1n);
    const g83 = (x0_8 ^ 1n);
    const g84 = (g83 | g79);
    const g85 = (g84 ^ 1n);
    const g86 = (g83 | g80);
    const g87 = (g86 ^ 1n);
    const g88 = (g87 | g85);
    const g89 = (g88 | g82);
    const g90 = (g89 ^ 1n);
    const g91 = (x1_9 ^ 1n);
    const g92 = (g91 | g90);
    const g93 = (g92 ^ 1n);
    const g94 = (x0_9 ^ 1n);
    const g95 = (g94 | g90);
    const g96 = (g95 ^ 1n);
    const g97 = (g94 | g91);
    const g98 = (g97 ^ 1n);
    const g99 = (g98 | g96);
    const g100 = (g99 | g93);
    const g101 = (g100 ^ 1n);
    const g102 = (x1_10 ^ 1n);
    const g103 = (g102 | g101);
    const g104 = (g103 ^ 1n);
    const g105 = (x0_10 ^ 1n);
    const g106 = (g105 | g101);
    const g107 = (g106 ^ 1n);
    const g108 = (g105 | g102);
    const g109 = (g108 ^ 1n);
    const g110 = (g109 | g107);
    const g111 = (g110 | g104);
    const g112 = (g111 ^ 1n);
    const g113 = (x1_11 ^ 1n);
    const g114 = (g113 | g112);
    const g115 = (g114 ^ 1n);
    const g116 = (x0_11 ^ 1n);
    const g117 = (g116 | g112);
    const g118 = (g117 ^ 1n);
    const g119 = (g116 | g113);
    const g120 = (g119 ^ 1n);
    const g121 = (g120 | g118);
    const g122 = (g121 | g115);
    const g123 = (g122 ^ 1n);
    const g124 = (x1_12 ^ 1n);
    const g125 = (g124 | g123);
    const g126 = (g125 ^ 1n);
    const g127 = (x0_12 ^ 1n);
    const g128 = (g127 | g123);
    const g129 = (g128 ^ 1n);
    const g130 = (g127 | g124);
    const g131 = (g130 ^ 1n);
    const g132 = (g131 | g129);
    const g133 = (g132 | g126);
    const g134 = (g133 ^ 1n);
    const g135 = (x1_13 ^ 1n);
    const g136 = (g135 | g134);
    const g137 = (g136 ^ 1n);
    const g138 = (x0_13 ^ 1n);
    const g139 = (g138 | g134);
    const g140 = (g139 ^ 1n);
    const g141 = (g138 | g135);
    const g142 = (g141 ^ 1n);
    const g143 = (g142 | g140);
    const g144 = (g143 | g137);
    const g145 = (g144 ^ 1n);
    const g146 = (x1_14 ^ 1n);
    const g147 = (g146 | g145);
    const g148 = (g147 ^ 1n);
    const g149 = (x0_14 ^ 1n);
    const g150 = (g149 | g145);
    const g151 = (g150 ^ 1n);
    const g152 = (g149 | g146);
    const g153 = (g152 ^ 1n);
    const g154 = (g153 | g151);
    const g155 = (g154 | g148);
    const g156 = (g155 ^ 1n);
    const g157 = (x1_15 ^ 1n);
    const g158 = (g157 | g156);
    const g159 = (g158 ^ 1n);
    const g160 = (x0_15 ^ 1n);
    const g161 = (g160 | g156);
    const g162 = (g161 ^ 1n);
    const g163 = (g160 | g157);
    const g164 = (g163 ^ 1n);
    const g165 = (g164 | g162);
    const g166 = (g165 | g159);
    const g167 = (g166 ^ 1n);
    const g168 = (x1_16 ^ 1n);
    const g169 = (g168 | g167);
    const g170 = (g169 ^ 1n);
    const g171 = (x0_16 ^ 1n);
    const g172 = (g171 | g167);
    const g173 = (g172 ^ 1n);
    const g174 = (g171 | g168);
    const g175 = (g174 ^ 1n);
    const g176 = (g175 | g173);
    const g177 = (g176 | g170);
    const g178 = (g177 ^ 1n);
    const g179 = (x1_17 ^ 1n);
    const g180 = (g179 | g178);
    const g181 = (g180 ^ 1n);
    const g182 = (x0_17 ^ 1n);
    const g183 = (g182 | g178);
    const g184 = (g183 ^ 1n);
    const g185 = (g182 | g179);
    const g186 = (g185 ^ 1n);
    const g187 = (g186 | g184);
    const g188 = (g187 | g181);
    const g189 = (g188 ^ 1n);
    const g190 = (x1_18 ^ 1n);
    const g191 = (g190 | g189);
    const g192 = (g191 ^ 1n);
    const g193 = (x0_18 ^ 1n);
    const g194 = (g193 | g189);
    const g195 = (g194 ^ 1n);
    const g196 = (g193 | g190);
    const g197 = (g196 ^ 1n);
    const g198 = (g197 | g195);
    const g199 = (g198 | g192);
    const g200 = (g199 ^ 1n);
    const g201 = (x1_19 ^ 1n);
    const g202 = (g201 | g200);
    const g203 = (g202 ^ 1n);
    const g204 = (x0_19 ^ 1n);
    const g205 = (g204 | g200);
    const g206 = (g205 ^ 1n);
    const g207 = (g204 | g201);
    const g208 = (g207 ^ 1n);
    const g209 = (g208 | g206);
    const g210 = (g209 | g203);
    const g211 = (g210 ^ 1n);
    const g212 = (x1_20 ^ 1n);
    const g213 = (g212 | g211);
    const g214 = (g213 ^ 1n);
    const g215 = (x0_20 ^ 1n);
    const g216 = (g215 | g211);
    const g217 = (g216 ^ 1n);
    const g218 = (g215 | g212);
    const g219 = (g218 ^ 1n);
    const g220 = (g219 | g217);
    const g221 = (g220 | g214);
    const g222 = (g221 ^ 1n);
    const g223 = (x1_21 ^ 1n);
    const g224 = (g223 | g222);
    const g225 = (g224 ^ 1n);
    const g226 = (x0_21 ^ 1n);
    const g227 = (g226 | g222);
    const g228 = (g227 ^ 1n);
    const g229 = (g226 | g223);
    const g230 = (g229 ^ 1n);
    const g231 = (g230 | g228);
    const g232 = (g231 | g225);
    const g233 = (g232 ^ 1n);
    const g234 = (x1_22 ^ 1n);
    const g235 = (g234 | g233);
    const g236 = (g235 ^ 1n);
    const g237 = (x0_22 ^ 1n);
    const g238 = (g237 | g233);
    const g239 = (g238 ^ 1n);
    const g240 = (g237 | g234);
    const g241 = (g240 ^ 1n);
    const g242 = (g241 | g239);
    const g243 = (g242 | g236);
    const g244 = (g243 ^ 1n);
    const g245 = (x1_23 ^ 1n);
    const g246 = (g245 | g244);
    const g247 = (g246 ^ 1n);
    const g248 = (x0_23 ^ 1n);
    const g249 = (g248 | g244);
    const g250 = (g249 ^ 1n);
    const g251 = (g248 | g245);
    const g252 = (g251 ^ 1n);
    const g253 = (g252 | g250);
    const g254 = (g253 | g247);
    const g255 = (g254 ^ 1n);
    const g256 = (x1_24 ^ 1n);
    const g257 = (g256 | g255);
    const g258 = (g257 ^ 1n);
    const g259 = (x0_24 ^ 1n);
    const g260 = (g259 | g255);
    const g261 = (g260 ^ 1n);
    const g262 = (g259 | g256);
    const g263 = (g262 ^ 1n);
    const g264 = (g263 | g261);
    const g265 = (g264 | g258);
    const g266 = (g265 ^ 1n);
    const g267 = (x1_25 ^ 1n);
    const g268 = (g267 | g266);
    const g269 = (g268 ^ 1n);
    const g270 = (x0_25 ^ 1n);
    const g271 = (g270 | g266);
    const g272 = (g271 ^ 1n);
    const g273 = (g270 | g267);
    const g274 = (g273 ^ 1n);
    const g275 = (g274 | g272);
    const g276 = (g275 | g269);
    const g277 = (g276 ^ 1n);
    const g278 = (x1_26 ^ 1n);
    const g279 = (g278 | g277);
    const g280 = (g279 ^ 1n);
    const g281 = (x0_26 ^ 1n);
    const g282 = (g281 | g277);
    const g283 = (g282 ^ 1n);
    const g284 = (g281 | g278);
    const g285 = (g284 ^ 1n);
    const g286 = (g285 | g283);
    const g287 = (g286 | g280);
    const g288 = (g287 ^ 1n);
    const g289 = (x1_27 ^ 1n);
    const g290 = (g289 | g288);
    const g291 = (g290 ^ 1n);
    const g292 = (x0_27 ^ 1n);
    const g293 = (g292 | g288);
    const g294 = (g293 ^ 1n);
    const g295 = (g292 | g289);
    const g296 = (g295 ^ 1n);
    const g297 = (g296 | g294);
    const g298 = (g297 | g291);
    const g299 = (g298 ^ 1n);
    const g300 = (x1_28 ^ 1n);
    const g301 = (g300 | g299);
    const g302 = (g301 ^ 1n);
    const g303 = (x0_28 ^ 1n);
    const g304 = (g303 | g299);
    const g305 = (g304 ^ 1n);
    const g306 = (g303 | g300);
    const g307 = (g306 ^ 1n);
    const g308 = (g307 | g305);
    const g309 = (g308 | g302);
    const g310 = (g309 ^ 1n);
    const g311 = (x1_29 ^ 1n);
    const g312 = (g311 | g310);
    const g313 = (g312 ^ 1n);
    const g314 = (x0_29 ^ 1n);
    const g315 = (g314 | g310);
    const g316 = (g315 ^ 1n);
    const g317 = (g314 | g311);
    const g318 = (g317 ^ 1n);
    const g319 = (g318 | g316);
    const g320 = (g319 | g313);
    const g321 = (g320 ^ 1n);
    const g322 = (x1_30 ^ 1n);
    const g323 = (g322 | g321);
    const g324 = (g323 ^ 1n);
    const g325 = (x0_30 ^ 1n);
    const g326 = (g325 | g321);
    const g327 = (g326 ^ 1n);
    const g328 = (g325 | g322);
    const g329 = (g328 ^ 1n);
    const g330 = (g329 | g327);
    const g331 = (g330 | g324);
    const g332 = (g331 ^ 1n);
    const g333 = (x1_31 ^ 1n);
    const g334 = (g333 | g332);
    const g335 = (g334 ^ 1n);
    const g336 = (x0_31 ^ 1n);
    const g337 = (g336 | g332);
    const g338 = (g337 ^ 1n);
    const g339 = (g336 | g333);
    const g340 = (g339 ^ 1n);
    const g341 = (g340 | g338);
    const g342 = (g341 | g335);
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
    const w32 = cat(w31, g342, 1);
    const w33 = cat(w32, g342, 1);
    const w34 = cat(w33, g342, 1);
    const w35 = cat(w34, g342, 1);
    const w36 = cat(w35, g342, 1);
    const w37 = cat(w36, g342, 1);
    const w38 = cat(w37, g342, 1);
    const w39 = cat(w38, g342, 1);
    const w40 = cat(w39, g342, 1);
    const w41 = cat(w40, g342, 1);
    const w42 = cat(w41, g342, 1);
    const w43 = cat(w42, g342, 1);
    const w44 = cat(w43, g342, 1);
    const w45 = cat(w44, g342, 1);
    const w46 = cat(w45, g342, 1);
    const w47 = cat(w46, g342, 1);
    const w48 = cat(w47, g342, 1);
    const w49 = cat(w48, g342, 1);
    const w50 = cat(w49, g342, 1);
    const w51 = cat(w50, g342, 1);
    const w52 = cat(w51, g342, 1);
    const w53 = cat(w52, g342, 1);
    const w54 = cat(w53, g342, 1);
    const w55 = cat(w54, g342, 1);
    const w56 = cat(w55, g342, 1);
    const w57 = cat(w56, g342, 1);
    const w58 = cat(w57, g342, 1);
    const w59 = cat(w58, g342, 1);
    const w60 = cat(w59, g342, 1);
    const w61 = cat(w60, g342, 1);
    const w62 = cat(w61, g342, 1);
    const w63 = cat(w62, g342, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_sbb_gpr_same_32__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
