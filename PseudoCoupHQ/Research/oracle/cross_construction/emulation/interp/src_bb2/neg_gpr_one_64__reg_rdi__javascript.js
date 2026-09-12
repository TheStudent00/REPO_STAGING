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
// one named local per gate, over the term of neg_gpr_one_64__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   v0*18446744073709551615
function emu_neg_gpr_one_64__reg_rdi__javascript(a) {
    const x0_0 = ext(a, 0, 0);
    const x0_1 = ext(a, 1, 1);
    const x0_2 = ext(a, 2, 2);
    const x0_3 = ext(a, 3, 3);
    const x0_4 = ext(a, 4, 4);
    const x0_5 = ext(a, 5, 5);
    const x0_6 = ext(a, 6, 6);
    const x0_7 = ext(a, 7, 7);
    const x0_8 = ext(a, 8, 8);
    const x0_9 = ext(a, 9, 9);
    const x0_10 = ext(a, 10, 10);
    const x0_11 = ext(a, 11, 11);
    const x0_12 = ext(a, 12, 12);
    const x0_13 = ext(a, 13, 13);
    const x0_14 = ext(a, 14, 14);
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
    const g0 = (x0_0 ^ x0_1);
    const g1 = (g0 ^ 1n);
    const g2 = (g1 ^ 1n);
    const g3 = (x0_1 | x0_0);
    const g4 = (g3 ^ x0_2);
    const g5 = (g4 ^ 1n);
    const g6 = (g5 ^ 1n);
    const g7 = (x0_2 | g3);
    const g8 = (g7 ^ x0_3);
    const g9 = (g8 ^ 1n);
    const g10 = (g9 ^ 1n);
    const g11 = (x0_3 | g7);
    const g12 = (g11 ^ x0_4);
    const g13 = (g12 ^ 1n);
    const g14 = (g13 ^ 1n);
    const g15 = (x0_4 | g11);
    const g16 = (g15 ^ x0_5);
    const g17 = (g16 ^ 1n);
    const g18 = (g17 ^ 1n);
    const g19 = (x0_5 | g15);
    const g20 = (g19 ^ x0_6);
    const g21 = (g20 ^ 1n);
    const g22 = (g21 ^ 1n);
    const g23 = (x0_6 | g19);
    const g24 = (g23 ^ x0_7);
    const g25 = (g24 ^ 1n);
    const g26 = (g25 ^ 1n);
    const g27 = (x0_7 | g23);
    const g28 = (g27 ^ x0_8);
    const g29 = (g28 ^ 1n);
    const g30 = (g29 ^ 1n);
    const g31 = (x0_8 | g27);
    const g32 = (g31 ^ x0_9);
    const g33 = (g32 ^ 1n);
    const g34 = (g33 ^ 1n);
    const g35 = (x0_9 | g31);
    const g36 = (g35 ^ x0_10);
    const g37 = (g36 ^ 1n);
    const g38 = (g37 ^ 1n);
    const g39 = (x0_10 | g35);
    const g40 = (g39 ^ x0_11);
    const g41 = (g40 ^ 1n);
    const g42 = (g41 ^ 1n);
    const g43 = (x0_11 | g39);
    const g44 = (g43 ^ x0_12);
    const g45 = (g44 ^ 1n);
    const g46 = (g45 ^ 1n);
    const g47 = (x0_12 | g43);
    const g48 = (g47 ^ x0_13);
    const g49 = (g48 ^ 1n);
    const g50 = (g49 ^ 1n);
    const g51 = (x0_13 | g47);
    const g52 = (g51 ^ x0_14);
    const g53 = (g52 ^ 1n);
    const g54 = (g53 ^ 1n);
    const g55 = (x0_14 | g51);
    const g56 = (g55 ^ x0_15);
    const g57 = (g56 ^ 1n);
    const g58 = (g57 ^ 1n);
    const g59 = (x0_15 | g55);
    const g60 = (g59 ^ x0_16);
    const g61 = (g60 ^ 1n);
    const g62 = (g61 ^ 1n);
    const g63 = (x0_16 | g59);
    const g64 = (g63 ^ x0_17);
    const g65 = (g64 ^ 1n);
    const g66 = (g65 ^ 1n);
    const g67 = (x0_17 | g63);
    const g68 = (g67 ^ x0_18);
    const g69 = (g68 ^ 1n);
    const g70 = (g69 ^ 1n);
    const g71 = (x0_18 | g67);
    const g72 = (g71 ^ x0_19);
    const g73 = (g72 ^ 1n);
    const g74 = (g73 ^ 1n);
    const g75 = (x0_19 | g71);
    const g76 = (g75 ^ x0_20);
    const g77 = (g76 ^ 1n);
    const g78 = (g77 ^ 1n);
    const g79 = (x0_20 | g75);
    const g80 = (g79 ^ x0_21);
    const g81 = (g80 ^ 1n);
    const g82 = (g81 ^ 1n);
    const g83 = (x0_21 | g79);
    const g84 = (g83 ^ x0_22);
    const g85 = (g84 ^ 1n);
    const g86 = (g85 ^ 1n);
    const g87 = (x0_22 | g83);
    const g88 = (g87 ^ x0_23);
    const g89 = (g88 ^ 1n);
    const g90 = (g89 ^ 1n);
    const g91 = (x0_23 | g87);
    const g92 = (g91 ^ x0_24);
    const g93 = (g92 ^ 1n);
    const g94 = (g93 ^ 1n);
    const g95 = (x0_24 | g91);
    const g96 = (g95 ^ x0_25);
    const g97 = (g96 ^ 1n);
    const g98 = (g97 ^ 1n);
    const g99 = (x0_25 | g95);
    const g100 = (g99 ^ x0_26);
    const g101 = (g100 ^ 1n);
    const g102 = (g101 ^ 1n);
    const g103 = (x0_26 | g99);
    const g104 = (g103 ^ x0_27);
    const g105 = (g104 ^ 1n);
    const g106 = (g105 ^ 1n);
    const g107 = (x0_27 | g103);
    const g108 = (g107 ^ x0_28);
    const g109 = (g108 ^ 1n);
    const g110 = (g109 ^ 1n);
    const g111 = (x0_28 | g107);
    const g112 = (g111 ^ x0_29);
    const g113 = (g112 ^ 1n);
    const g114 = (g113 ^ 1n);
    const g115 = (x0_29 | g111);
    const g116 = (g115 ^ x0_30);
    const g117 = (g116 ^ 1n);
    const g118 = (g117 ^ 1n);
    const g119 = (x0_30 | g115);
    const g120 = (g119 ^ x0_31);
    const g121 = (g120 ^ 1n);
    const g122 = (g121 ^ 1n);
    const g123 = (x0_31 | g119);
    const g124 = (g123 ^ x0_32);
    const g125 = (g124 ^ 1n);
    const g126 = (g125 ^ 1n);
    const g127 = (x0_32 | g123);
    const g128 = (g127 ^ x0_33);
    const g129 = (g128 ^ 1n);
    const g130 = (g129 ^ 1n);
    const g131 = (x0_33 | g127);
    const g132 = (g131 ^ x0_34);
    const g133 = (g132 ^ 1n);
    const g134 = (g133 ^ 1n);
    const g135 = (x0_34 | g131);
    const g136 = (g135 ^ x0_35);
    const g137 = (g136 ^ 1n);
    const g138 = (g137 ^ 1n);
    const g139 = (x0_35 | g135);
    const g140 = (g139 ^ x0_36);
    const g141 = (g140 ^ 1n);
    const g142 = (g141 ^ 1n);
    const g143 = (x0_36 | g139);
    const g144 = (g143 ^ x0_37);
    const g145 = (g144 ^ 1n);
    const g146 = (g145 ^ 1n);
    const g147 = (x0_37 | g143);
    const g148 = (g147 ^ x0_38);
    const g149 = (g148 ^ 1n);
    const g150 = (g149 ^ 1n);
    const g151 = (x0_38 | g147);
    const g152 = (g151 ^ x0_39);
    const g153 = (g152 ^ 1n);
    const g154 = (g153 ^ 1n);
    const g155 = (x0_39 | g151);
    const g156 = (g155 ^ x0_40);
    const g157 = (g156 ^ 1n);
    const g158 = (g157 ^ 1n);
    const g159 = (x0_40 | g155);
    const g160 = (g159 ^ x0_41);
    const g161 = (g160 ^ 1n);
    const g162 = (g161 ^ 1n);
    const g163 = (x0_41 | g159);
    const g164 = (g163 ^ x0_42);
    const g165 = (g164 ^ 1n);
    const g166 = (g165 ^ 1n);
    const g167 = (x0_42 | g163);
    const g168 = (g167 ^ x0_43);
    const g169 = (g168 ^ 1n);
    const g170 = (g169 ^ 1n);
    const g171 = (x0_43 | g167);
    const g172 = (g171 ^ x0_44);
    const g173 = (g172 ^ 1n);
    const g174 = (g173 ^ 1n);
    const g175 = (x0_44 | g171);
    const g176 = (g175 ^ x0_45);
    const g177 = (g176 ^ 1n);
    const g178 = (g177 ^ 1n);
    const g179 = (x0_45 | g175);
    const g180 = (g179 ^ x0_46);
    const g181 = (g180 ^ 1n);
    const g182 = (g181 ^ 1n);
    const g183 = (x0_46 | g179);
    const g184 = (g183 ^ x0_47);
    const g185 = (g184 ^ 1n);
    const g186 = (g185 ^ 1n);
    const g187 = (x0_47 | g183);
    const g188 = (g187 ^ x0_48);
    const g189 = (g188 ^ 1n);
    const g190 = (g189 ^ 1n);
    const g191 = (x0_48 | g187);
    const g192 = (g191 ^ x0_49);
    const g193 = (g192 ^ 1n);
    const g194 = (g193 ^ 1n);
    const g195 = (x0_49 | g191);
    const g196 = (g195 ^ x0_50);
    const g197 = (g196 ^ 1n);
    const g198 = (g197 ^ 1n);
    const g199 = (x0_50 | g195);
    const g200 = (g199 ^ x0_51);
    const g201 = (g200 ^ 1n);
    const g202 = (g201 ^ 1n);
    const g203 = (x0_51 | g199);
    const g204 = (g203 ^ x0_52);
    const g205 = (g204 ^ 1n);
    const g206 = (g205 ^ 1n);
    const g207 = (x0_52 | g203);
    const g208 = (g207 ^ x0_53);
    const g209 = (g208 ^ 1n);
    const g210 = (g209 ^ 1n);
    const g211 = (x0_53 | g207);
    const g212 = (g211 ^ x0_54);
    const g213 = (g212 ^ 1n);
    const g214 = (g213 ^ 1n);
    const g215 = (x0_54 | g211);
    const g216 = (g215 ^ x0_55);
    const g217 = (g216 ^ 1n);
    const g218 = (g217 ^ 1n);
    const g219 = (x0_55 | g215);
    const g220 = (g219 ^ x0_56);
    const g221 = (g220 ^ 1n);
    const g222 = (g221 ^ 1n);
    const g223 = (x0_56 | g219);
    const g224 = (g223 ^ x0_57);
    const g225 = (g224 ^ 1n);
    const g226 = (g225 ^ 1n);
    const g227 = (x0_57 | g223);
    const g228 = (g227 ^ x0_58);
    const g229 = (g228 ^ 1n);
    const g230 = (g229 ^ 1n);
    const g231 = (x0_58 | g227);
    const g232 = (g231 ^ x0_59);
    const g233 = (g232 ^ 1n);
    const g234 = (g233 ^ 1n);
    const g235 = (x0_59 | g231);
    const g236 = (g235 ^ x0_60);
    const g237 = (g236 ^ 1n);
    const g238 = (g237 ^ 1n);
    const g239 = (x0_60 | g235);
    const g240 = (g239 ^ x0_61);
    const g241 = (g240 ^ 1n);
    const g242 = (g241 ^ 1n);
    const g243 = (x0_61 | g239);
    const g244 = (g243 ^ x0_62);
    const g245 = (g244 ^ 1n);
    const g246 = (g245 ^ 1n);
    const g247 = (x0_62 | g243);
    const g248 = (g247 ^ x0_63);
    const g249 = (g248 ^ 1n);
    const g250 = (g249 ^ 1n);
    const w0 = g250;
    const w1 = cat(w0, g246, 1);
    const w2 = cat(w1, g242, 1);
    const w3 = cat(w2, g238, 1);
    const w4 = cat(w3, g234, 1);
    const w5 = cat(w4, g230, 1);
    const w6 = cat(w5, g226, 1);
    const w7 = cat(w6, g222, 1);
    const w8 = cat(w7, g218, 1);
    const w9 = cat(w8, g214, 1);
    const w10 = cat(w9, g210, 1);
    const w11 = cat(w10, g206, 1);
    const w12 = cat(w11, g202, 1);
    const w13 = cat(w12, g198, 1);
    const w14 = cat(w13, g194, 1);
    const w15 = cat(w14, g190, 1);
    const w16 = cat(w15, g186, 1);
    const w17 = cat(w16, g182, 1);
    const w18 = cat(w17, g178, 1);
    const w19 = cat(w18, g174, 1);
    const w20 = cat(w19, g170, 1);
    const w21 = cat(w20, g166, 1);
    const w22 = cat(w21, g162, 1);
    const w23 = cat(w22, g158, 1);
    const w24 = cat(w23, g154, 1);
    const w25 = cat(w24, g150, 1);
    const w26 = cat(w25, g146, 1);
    const w27 = cat(w26, g142, 1);
    const w28 = cat(w27, g138, 1);
    const w29 = cat(w28, g134, 1);
    const w30 = cat(w29, g130, 1);
    const w31 = cat(w30, g126, 1);
    const w32 = cat(w31, g122, 1);
    const w33 = cat(w32, g118, 1);
    const w34 = cat(w33, g114, 1);
    const w35 = cat(w34, g110, 1);
    const w36 = cat(w35, g106, 1);
    const w37 = cat(w36, g102, 1);
    const w38 = cat(w37, g98, 1);
    const w39 = cat(w38, g94, 1);
    const w40 = cat(w39, g90, 1);
    const w41 = cat(w40, g86, 1);
    const w42 = cat(w41, g82, 1);
    const w43 = cat(w42, g78, 1);
    const w44 = cat(w43, g74, 1);
    const w45 = cat(w44, g70, 1);
    const w46 = cat(w45, g66, 1);
    const w47 = cat(w46, g62, 1);
    const w48 = cat(w47, g58, 1);
    const w49 = cat(w48, g54, 1);
    const w50 = cat(w49, g50, 1);
    const w51 = cat(w50, g46, 1);
    const w52 = cat(w51, g42, 1);
    const w53 = cat(w52, g38, 1);
    const w54 = cat(w53, g34, 1);
    const w55 = cat(w54, g30, 1);
    const w56 = cat(w55, g26, 1);
    const w57 = cat(w56, g22, 1);
    const w58 = cat(w57, g18, 1);
    const w59 = cat(w58, g14, 1);
    const w60 = cat(w59, g10, 1);
    const w61 = cat(w60, g6, 1);
    const w62 = cat(w61, g2, 1);
    const w63 = cat(w62, x0_0, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_neg_gpr_one_64__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
