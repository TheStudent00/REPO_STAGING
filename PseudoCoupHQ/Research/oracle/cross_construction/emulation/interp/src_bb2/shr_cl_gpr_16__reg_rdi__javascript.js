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
// one named local per gate, over the term of shr_cl_gpr_16__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1))))
function emu_shr_cl_gpr_16__reg_rdi__javascript(a, b) {
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
    const g61 = (g60 & g59);
    const g62 = (x1_0 ^ 1n);
    const g63 = (x1_0 & x0_2);
    const g64 = (g62 & x0_1);
    const g65 = (g63 | g64);
    const g66 = (x1_0 ^ 1n);
    const g67 = (x1_0 & x0_4);
    const g68 = (g66 & x0_3);
    const g69 = (g67 | g68);
    const g70 = (x1_1 ^ 1n);
    const g71 = (x1_1 & g69);
    const g72 = (g70 & g65);
    const g73 = (g71 | g72);
    const g74 = (x1_0 ^ 1n);
    const g75 = (x1_0 & x0_6);
    const g76 = (g74 & x0_5);
    const g77 = (g75 | g76);
    const g78 = (x1_0 ^ 1n);
    const g79 = (x1_0 & x0_8);
    const g80 = (g78 & x0_7);
    const g81 = (g79 | g80);
    const g82 = (x1_1 ^ 1n);
    const g83 = (x1_1 & g81);
    const g84 = (g82 & g77);
    const g85 = (g83 | g84);
    const g86 = (x1_2 ^ 1n);
    const g87 = (x1_2 & g85);
    const g88 = (g86 & g73);
    const g89 = (g87 | g88);
    const g90 = (x1_0 ^ 1n);
    const g91 = (x1_0 & x0_10);
    const g92 = (g90 & x0_9);
    const g93 = (g91 | g92);
    const g94 = (x1_0 ^ 1n);
    const g95 = (x1_0 & x0_12);
    const g96 = (g94 & x0_11);
    const g97 = (g95 | g96);
    const g98 = (x1_1 ^ 1n);
    const g99 = (x1_1 & g97);
    const g100 = (g98 & g93);
    const g101 = (g99 | g100);
    const g102 = (x1_0 ^ 1n);
    const g103 = (x1_0 & x0_14);
    const g104 = (g102 & x0_13);
    const g105 = (g103 | g104);
    const g106 = (x0_15 ^ 1n);
    const g107 = (x1_0 | g106);
    const g108 = (g107 ^ 1n);
    const g109 = (x1_1 ^ 1n);
    const g110 = (x1_1 & g108);
    const g111 = (g109 & g105);
    const g112 = (g110 | g111);
    const g113 = (x1_2 ^ 1n);
    const g114 = (x1_2 & g112);
    const g115 = (g113 & g101);
    const g116 = (g114 | g115);
    const g117 = (x1_3 ^ 1n);
    const g118 = (x1_3 & g116);
    const g119 = (g117 & g89);
    const g120 = (g118 | g119);
    const g121 = (g60 & g120);
    const g122 = (x1_1 ^ 1n);
    const g123 = (x1_1 & g15);
    const g124 = (g122 & g7);
    const g125 = (g123 | g124);
    const g126 = (x1_1 ^ 1n);
    const g127 = (x1_1 & g31);
    const g128 = (g126 & g19);
    const g129 = (g127 | g128);
    const g130 = (x1_2 ^ 1n);
    const g131 = (x1_2 & g129);
    const g132 = (g130 & g125);
    const g133 = (g131 | g132);
    const g134 = (x1_1 ^ 1n);
    const g135 = (x1_1 & g43);
    const g136 = (g134 & g35);
    const g137 = (g135 | g136);
    const g138 = (g47 ^ 1n);
    const g139 = (x1_1 | g138);
    const g140 = (g139 ^ 1n);
    const g141 = (x1_2 ^ 1n);
    const g142 = (x1_2 & g140);
    const g143 = (g141 & g137);
    const g144 = (g142 | g143);
    const g145 = (x1_3 ^ 1n);
    const g146 = (x1_3 & g144);
    const g147 = (g145 & g133);
    const g148 = (g146 | g147);
    const g149 = (g60 & g148);
    const g150 = (x1_1 ^ 1n);
    const g151 = (x1_1 & g77);
    const g152 = (g150 & g69);
    const g153 = (g151 | g152);
    const g154 = (x1_1 ^ 1n);
    const g155 = (x1_1 & g93);
    const g156 = (g154 & g81);
    const g157 = (g155 | g156);
    const g158 = (x1_2 ^ 1n);
    const g159 = (x1_2 & g157);
    const g160 = (g158 & g153);
    const g161 = (g159 | g160);
    const g162 = (x1_1 ^ 1n);
    const g163 = (x1_1 & g105);
    const g164 = (g162 & g97);
    const g165 = (g163 | g164);
    const g166 = (x1_1 | g107);
    const g167 = (g166 ^ 1n);
    const g168 = (x1_2 ^ 1n);
    const g169 = (x1_2 & g167);
    const g170 = (g168 & g165);
    const g171 = (g169 | g170);
    const g172 = (x1_3 ^ 1n);
    const g173 = (x1_3 & g171);
    const g174 = (g172 & g161);
    const g175 = (g173 | g174);
    const g176 = (g60 & g175);
    const g177 = (x1_2 ^ 1n);
    const g178 = (x1_2 & g39);
    const g179 = (g177 & g23);
    const g180 = (g178 | g179);
    const g181 = (g51 ^ 1n);
    const g182 = (x1_2 | g181);
    const g183 = (g182 ^ 1n);
    const g184 = (x1_3 ^ 1n);
    const g185 = (x1_3 & g183);
    const g186 = (g184 & g180);
    const g187 = (g185 | g186);
    const g188 = (g60 & g187);
    const g189 = (x1_2 ^ 1n);
    const g190 = (x1_2 & g101);
    const g191 = (g189 & g85);
    const g192 = (g190 | g191);
    const g193 = (g112 ^ 1n);
    const g194 = (x1_2 | g193);
    const g195 = (g194 ^ 1n);
    const g196 = (x1_3 ^ 1n);
    const g197 = (x1_3 & g195);
    const g198 = (g196 & g192);
    const g199 = (g197 | g198);
    const g200 = (g60 & g199);
    const g201 = (x1_2 ^ 1n);
    const g202 = (x1_2 & g137);
    const g203 = (g201 & g129);
    const g204 = (g202 | g203);
    const g205 = (x1_2 | g139);
    const g206 = (g205 ^ 1n);
    const g207 = (x1_3 ^ 1n);
    const g208 = (x1_3 & g206);
    const g209 = (g207 & g204);
    const g210 = (g208 | g209);
    const g211 = (g60 & g210);
    const g212 = (x1_2 ^ 1n);
    const g213 = (x1_2 & g165);
    const g214 = (g212 & g157);
    const g215 = (g213 | g214);
    const g216 = (x1_2 | g166);
    const g217 = (g216 ^ 1n);
    const g218 = (x1_3 ^ 1n);
    const g219 = (x1_3 & g217);
    const g220 = (g218 & g215);
    const g221 = (g219 | g220);
    const g222 = (g60 & g221);
    const g223 = (x1_3 ^ 1n);
    const g224 = (g60 & g223);
    const g225 = (g224 & g55);
    const g226 = (g60 & g223);
    const g227 = (g226 & g116);
    const g228 = (g60 & g223);
    const g229 = (g228 & g144);
    const g230 = (g60 & g223);
    const g231 = (g230 & g171);
    const g232 = (x1_2 ^ 1n);
    const g233 = (g60 & g223);
    const g234 = (g233 & g232);
    const g235 = (g234 & g51);
    const g236 = (g60 & g223);
    const g237 = (g236 & g232);
    const g238 = (g237 & g112);
    const g239 = (x1_1 ^ 1n);
    const g240 = (g60 & g223);
    const g241 = (g240 & g232);
    const g242 = (g241 & g239);
    const g243 = (g242 & g47);
    const g244 = (x1_0 ^ 1n);
    const g245 = (g60 & g223);
    const g246 = (g245 & g232);
    const g247 = (g246 & g239);
    const g248 = (g247 & g244);
    const g249 = (g248 & x0_15);
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
    const w48 = cat(w47, g249, 1);
    const w49 = cat(w48, g243, 1);
    const w50 = cat(w49, g238, 1);
    const w51 = cat(w50, g235, 1);
    const w52 = cat(w51, g231, 1);
    const w53 = cat(w52, g229, 1);
    const w54 = cat(w53, g227, 1);
    const w55 = cat(w54, g225, 1);
    const w56 = cat(w55, g222, 1);
    const w57 = cat(w56, g211, 1);
    const w58 = cat(w57, g200, 1);
    const w59 = cat(w58, g188, 1);
    const w60 = cat(w59, g176, 1);
    const w61 = cat(w60, g149, 1);
    const w62 = cat(w61, g121, 1);
    const w63 = cat(w62, g61, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_shr_cl_gpr_16__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
