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
// one named local per gate, over the term of sub_gpr_gpr_16__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v1)*65535 + Extract(15, 0, v0))
function emu_sub_gpr_gpr_16__reg_rdi__javascript(a, b) {
    const x0_0 = ext(a, 0, 0);
    const x1_0 = ext(b, 0, 0);
    const x0_1 = ext(a, 1, 1);
    const x1_1 = ext(b, 1, 1);
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
    const g0 = (x1_0 ^ x0_0);
    const g1 = (g0 ^ 1n);
    const g2 = (g1 ^ 1n);
    const g3 = (x0_0 ^ 1n);
    const g4 = (x1_0 ^ 1n);
    const g5 = (g4 | g3);
    const g6 = (x0_1 ^ g5);
    const g7 = (g6 ^ 1n);
    const g8 = (x1_0 ^ x1_1);
    const g9 = (g8 ^ 1n);
    const g10 = (g9 ^ g7);
    const g11 = (g10 ^ 1n);
    const g12 = (x1_0 | x1_1);
    const g13 = (g12 ^ x1_2);
    const g14 = (g13 ^ 1n);
    const g15 = (x0_1 ^ 1n);
    const g16 = (g9 | g15);
    const g17 = (g16 ^ 1n);
    const g18 = (g15 | g5);
    const g19 = (g18 ^ 1n);
    const g20 = (g9 | g5);
    const g21 = (g20 ^ 1n);
    const g22 = (g21 | g19);
    const g23 = (g22 | g17);
    const g24 = (x0_2 ^ g23);
    const g25 = (g24 ^ 1n);
    const g26 = (g25 ^ g14);
    const g27 = (g26 ^ 1n);
    const g28 = (g27 ^ 1n);
    const g29 = (x1_2 | g12);
    const g30 = (g29 ^ x1_3);
    const g31 = (g30 ^ 1n);
    const g32 = (x0_2 ^ 1n);
    const g33 = (g14 | g32);
    const g34 = (g33 ^ 1n);
    const g35 = (g23 ^ 1n);
    const g36 = (g32 | g35);
    const g37 = (g36 ^ 1n);
    const g38 = (g14 | g35);
    const g39 = (g38 ^ 1n);
    const g40 = (g39 | g37);
    const g41 = (g40 | g34);
    const g42 = (x0_3 ^ g41);
    const g43 = (g42 ^ 1n);
    const g44 = (g43 ^ g31);
    const g45 = (g44 ^ 1n);
    const g46 = (g45 ^ 1n);
    const g47 = (x1_3 | g29);
    const g48 = (g47 ^ x1_4);
    const g49 = (g48 ^ 1n);
    const g50 = (g41 ^ 1n);
    const g51 = (g50 | g31);
    const g52 = (g51 ^ 1n);
    const g53 = (x0_3 ^ 1n);
    const g54 = (g53 | g50);
    const g55 = (g54 ^ 1n);
    const g56 = (g31 | g53);
    const g57 = (g56 ^ 1n);
    const g58 = (g57 | g55);
    const g59 = (g58 | g52);
    const g60 = (x0_4 ^ g59);
    const g61 = (g60 ^ 1n);
    const g62 = (g61 ^ g49);
    const g63 = (g62 ^ 1n);
    const g64 = (g63 ^ 1n);
    const g65 = (x1_4 | g47);
    const g66 = (g65 ^ x1_5);
    const g67 = (g66 ^ 1n);
    const g68 = (g59 ^ 1n);
    const g69 = (g68 | g49);
    const g70 = (g69 ^ 1n);
    const g71 = (x0_4 ^ 1n);
    const g72 = (g71 | g49);
    const g73 = (g72 ^ 1n);
    const g74 = (g71 | g68);
    const g75 = (g74 ^ 1n);
    const g76 = (g75 | g73);
    const g77 = (g76 | g70);
    const g78 = (x0_5 ^ g77);
    const g79 = (g78 ^ 1n);
    const g80 = (g79 ^ g67);
    const g81 = (g80 ^ 1n);
    const g82 = (g81 ^ 1n);
    const g83 = (x1_5 | g65);
    const g84 = (g83 ^ x1_6);
    const g85 = (g84 ^ 1n);
    const g86 = (x0_5 ^ 1n);
    const g87 = (g67 | g86);
    const g88 = (g87 ^ 1n);
    const g89 = (g77 ^ 1n);
    const g90 = (g86 | g89);
    const g91 = (g90 ^ 1n);
    const g92 = (g67 | g89);
    const g93 = (g92 ^ 1n);
    const g94 = (g93 | g91);
    const g95 = (g94 | g88);
    const g96 = (x0_6 ^ g95);
    const g97 = (g96 ^ 1n);
    const g98 = (g97 ^ g85);
    const g99 = (g98 ^ 1n);
    const g100 = (g99 ^ 1n);
    const g101 = (x1_6 | g83);
    const g102 = (g101 ^ x1_7);
    const g103 = (g102 ^ 1n);
    const g104 = (g95 ^ 1n);
    const g105 = (x0_6 ^ 1n);
    const g106 = (g105 | g104);
    const g107 = (g106 ^ 1n);
    const g108 = (g85 | g104);
    const g109 = (g108 ^ 1n);
    const g110 = (g85 | g105);
    const g111 = (g110 ^ 1n);
    const g112 = (g111 | g109);
    const g113 = (g112 | g107);
    const g114 = (x0_7 ^ g113);
    const g115 = (g114 ^ 1n);
    const g116 = (g115 ^ g103);
    const g117 = (g116 ^ 1n);
    const g118 = (g117 ^ 1n);
    const g119 = (x1_7 | g101);
    const g120 = (g119 ^ x1_8);
    const g121 = (g120 ^ 1n);
    const g122 = (x0_7 ^ 1n);
    const g123 = (g103 | g122);
    const g124 = (g123 ^ 1n);
    const g125 = (g113 ^ 1n);
    const g126 = (g122 | g125);
    const g127 = (g126 ^ 1n);
    const g128 = (g103 | g125);
    const g129 = (g128 ^ 1n);
    const g130 = (g129 | g127);
    const g131 = (g130 | g124);
    const g132 = (x0_8 ^ g131);
    const g133 = (g132 ^ 1n);
    const g134 = (g133 ^ g121);
    const g135 = (g134 ^ 1n);
    const g136 = (g135 ^ 1n);
    const g137 = (x1_8 | g119);
    const g138 = (g137 ^ x1_9);
    const g139 = (g138 ^ 1n);
    const g140 = (x0_8 ^ 1n);
    const g141 = (g140 | g121);
    const g142 = (g141 ^ 1n);
    const g143 = (g131 ^ 1n);
    const g144 = (g121 | g143);
    const g145 = (g144 ^ 1n);
    const g146 = (g140 | g143);
    const g147 = (g146 ^ 1n);
    const g148 = (g147 | g145);
    const g149 = (g148 | g142);
    const g150 = (x0_9 ^ g149);
    const g151 = (g150 ^ 1n);
    const g152 = (g151 ^ g139);
    const g153 = (g152 ^ 1n);
    const g154 = (g153 ^ 1n);
    const g155 = (x1_9 | g137);
    const g156 = (g155 ^ x1_10);
    const g157 = (g156 ^ 1n);
    const g158 = (g149 ^ 1n);
    const g159 = (g139 | g158);
    const g160 = (g159 ^ 1n);
    const g161 = (x0_9 ^ 1n);
    const g162 = (g161 | g158);
    const g163 = (g162 ^ 1n);
    const g164 = (g161 | g139);
    const g165 = (g164 ^ 1n);
    const g166 = (g165 | g163);
    const g167 = (g166 | g160);
    const g168 = (x0_10 ^ g167);
    const g169 = (g168 ^ 1n);
    const g170 = (g169 ^ g157);
    const g171 = (g170 ^ 1n);
    const g172 = (g171 ^ 1n);
    const g173 = (x1_10 | g155);
    const g174 = (g173 ^ x1_11);
    const g175 = (g174 ^ 1n);
    const g176 = (x0_10 ^ 1n);
    const g177 = (g157 | g176);
    const g178 = (g177 ^ 1n);
    const g179 = (g167 ^ 1n);
    const g180 = (g176 | g179);
    const g181 = (g180 ^ 1n);
    const g182 = (g157 | g179);
    const g183 = (g182 ^ 1n);
    const g184 = (g183 | g181);
    const g185 = (g184 | g178);
    const g186 = (x0_11 ^ g185);
    const g187 = (g186 ^ 1n);
    const g188 = (g187 ^ g175);
    const g189 = (g188 ^ 1n);
    const g190 = (g189 ^ 1n);
    const g191 = (x1_11 | g173);
    const g192 = (g191 ^ x1_12);
    const g193 = (g192 ^ 1n);
    const g194 = (g185 ^ 1n);
    const g195 = (x0_11 ^ 1n);
    const g196 = (g195 | g194);
    const g197 = (g196 ^ 1n);
    const g198 = (g195 | g175);
    const g199 = (g198 ^ 1n);
    const g200 = (g194 | g175);
    const g201 = (g200 ^ 1n);
    const g202 = (g201 | g199);
    const g203 = (g202 | g197);
    const g204 = (x0_12 ^ g203);
    const g205 = (g204 ^ 1n);
    const g206 = (g205 ^ g193);
    const g207 = (g206 ^ 1n);
    const g208 = (g207 ^ 1n);
    const g209 = (x1_12 | g191);
    const g210 = (g209 ^ x1_13);
    const g211 = (g210 ^ 1n);
    const g212 = (g203 ^ 1n);
    const g213 = (x0_12 ^ 1n);
    const g214 = (g213 | g212);
    const g215 = (g214 ^ 1n);
    const g216 = (g193 | g213);
    const g217 = (g216 ^ 1n);
    const g218 = (g193 | g212);
    const g219 = (g218 ^ 1n);
    const g220 = (g219 | g217);
    const g221 = (g220 | g215);
    const g222 = (x0_13 ^ g221);
    const g223 = (g222 ^ 1n);
    const g224 = (g223 ^ g211);
    const g225 = (g224 ^ 1n);
    const g226 = (g225 ^ 1n);
    const g227 = (x1_13 | g209);
    const g228 = (g227 ^ x1_14);
    const g229 = (g228 ^ 1n);
    const g230 = (g221 ^ 1n);
    const g231 = (g230 | g211);
    const g232 = (g231 ^ 1n);
    const g233 = (x0_13 ^ 1n);
    const g234 = (g211 | g233);
    const g235 = (g234 ^ 1n);
    const g236 = (g233 | g230);
    const g237 = (g236 ^ 1n);
    const g238 = (g237 | g235);
    const g239 = (g238 | g232);
    const g240 = (x0_14 ^ g239);
    const g241 = (g240 ^ 1n);
    const g242 = (g241 ^ g229);
    const g243 = (g242 ^ 1n);
    const g244 = (g243 ^ 1n);
    const g245 = (x1_14 | g227);
    const g246 = (g245 ^ x1_15);
    const g247 = (g246 ^ 1n);
    const g248 = (g239 ^ 1n);
    const g249 = (g229 | g248);
    const g250 = (g249 ^ 1n);
    const g251 = (x0_14 ^ 1n);
    const g252 = (g229 | g251);
    const g253 = (g252 ^ 1n);
    const g254 = (g251 | g248);
    const g255 = (g254 ^ 1n);
    const g256 = (g255 | g253);
    const g257 = (g256 | g250);
    const g258 = (x0_15 ^ g257);
    const g259 = (g258 ^ 1n);
    const g260 = (g259 ^ g247);
    const g261 = (g260 ^ 1n);
    const g262 = (g261 ^ 1n);
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
    const w48 = cat(w47, g262, 1);
    const w49 = cat(w48, g244, 1);
    const w50 = cat(w49, g226, 1);
    const w51 = cat(w50, g208, 1);
    const w52 = cat(w51, g190, 1);
    const w53 = cat(w52, g172, 1);
    const w54 = cat(w53, g154, 1);
    const w55 = cat(w54, g136, 1);
    const w56 = cat(w55, g118, 1);
    const w57 = cat(w56, g100, 1);
    const w58 = cat(w57, g82, 1);
    const w59 = cat(w58, g64, 1);
    const w60 = cat(w59, g46, 1);
    const w61 = cat(w60, g28, 1);
    const w62 = cat(w61, g11, 1);
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
        out.push(emu_sub_gpr_gpr_16__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
