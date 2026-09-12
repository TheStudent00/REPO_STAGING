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
// one named local per gate, over the term of setle_gpr_one_8__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v2), If(Or(Extract(7, 0, v0) == Extract(7, 0, v1), Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 1, 0)), 1, 0))
function emu_setle_gpr_one_8__reg_rdi__javascript(a, b, c) {
    const x0_7 = ext(b, 7, 7);
    const x1_7 = ext(a, 7, 7);
    const x0_6 = ext(b, 6, 6);
    const x1_6 = ext(a, 6, 6);
    const x1_5 = ext(a, 5, 5);
    const x0_5 = ext(b, 5, 5);
    const x1_4 = ext(a, 4, 4);
    const x0_4 = ext(b, 4, 4);
    const x0_3 = ext(b, 3, 3);
    const x1_3 = ext(a, 3, 3);
    const x1_2 = ext(a, 2, 2);
    const x0_2 = ext(b, 2, 2);
    const x0_1 = ext(b, 1, 1);
    const x1_1 = ext(a, 1, 1);
    const x0_0 = ext(b, 0, 0);
    const x1_0 = ext(a, 0, 0);
    const x2_8 = ext(c, 8, 8);
    const x2_9 = ext(c, 9, 9);
    const x2_10 = ext(c, 10, 10);
    const x2_11 = ext(c, 11, 11);
    const x2_12 = ext(c, 12, 12);
    const x2_13 = ext(c, 13, 13);
    const x2_14 = ext(c, 14, 14);
    const x2_15 = ext(c, 15, 15);
    const x2_16 = ext(c, 16, 16);
    const x2_17 = ext(c, 17, 17);
    const x2_18 = ext(c, 18, 18);
    const x2_19 = ext(c, 19, 19);
    const x2_20 = ext(c, 20, 20);
    const x2_21 = ext(c, 21, 21);
    const x2_22 = ext(c, 22, 22);
    const x2_23 = ext(c, 23, 23);
    const x2_24 = ext(c, 24, 24);
    const x2_25 = ext(c, 25, 25);
    const x2_26 = ext(c, 26, 26);
    const x2_27 = ext(c, 27, 27);
    const x2_28 = ext(c, 28, 28);
    const x2_29 = ext(c, 29, 29);
    const x2_30 = ext(c, 30, 30);
    const x2_31 = ext(c, 31, 31);
    const x2_32 = ext(c, 32, 32);
    const x2_33 = ext(c, 33, 33);
    const x2_34 = ext(c, 34, 34);
    const x2_35 = ext(c, 35, 35);
    const x2_36 = ext(c, 36, 36);
    const x2_37 = ext(c, 37, 37);
    const x2_38 = ext(c, 38, 38);
    const x2_39 = ext(c, 39, 39);
    const x2_40 = ext(c, 40, 40);
    const x2_41 = ext(c, 41, 41);
    const x2_42 = ext(c, 42, 42);
    const x2_43 = ext(c, 43, 43);
    const x2_44 = ext(c, 44, 44);
    const x2_45 = ext(c, 45, 45);
    const x2_46 = ext(c, 46, 46);
    const x2_47 = ext(c, 47, 47);
    const x2_48 = ext(c, 48, 48);
    const x2_49 = ext(c, 49, 49);
    const x2_50 = ext(c, 50, 50);
    const x2_51 = ext(c, 51, 51);
    const x2_52 = ext(c, 52, 52);
    const x2_53 = ext(c, 53, 53);
    const x2_54 = ext(c, 54, 54);
    const x2_55 = ext(c, 55, 55);
    const x2_56 = ext(c, 56, 56);
    const x2_57 = ext(c, 57, 57);
    const x2_58 = ext(c, 58, 58);
    const x2_59 = ext(c, 59, 59);
    const x2_60 = ext(c, 60, 60);
    const x2_61 = ext(c, 61, 61);
    const x2_62 = ext(c, 62, 62);
    const x2_63 = ext(c, 63, 63);
    const g0 = (x1_7 ^ 1n);
    const g1 = (g0 | x0_7);
    const g2 = (x0_7 ^ 1n);
    const g3 = (x1_7 | g2);
    const g4 = (x1_6 ^ 1n);
    const g5 = (g4 | x0_6);
    const g6 = (x0_6 ^ 1n);
    const g7 = (g6 | x1_6);
    const g8 = (x1_5 ^ 1n);
    const g9 = (x0_5 | g8);
    const g10 = (x0_5 ^ 1n);
    const g11 = (g10 | x1_5);
    const g12 = (x1_4 ^ 1n);
    const g13 = (x0_4 | g12);
    const g14 = (x0_4 ^ 1n);
    const g15 = (x1_4 | g14);
    const g16 = (x1_3 ^ 1n);
    const g17 = (g16 | x0_3);
    const g18 = (x0_3 ^ 1n);
    const g19 = (x1_3 | g18);
    const g20 = (x1_2 ^ 1n);
    const g21 = (x0_2 | g20);
    const g22 = (x0_2 ^ 1n);
    const g23 = (x1_2 | g22);
    const g24 = (x1_1 ^ 1n);
    const g25 = (g24 | x0_1);
    const g26 = (x0_1 ^ 1n);
    const g27 = (x1_1 | g26);
    const g28 = (x1_0 ^ 1n);
    const g29 = (g28 | x0_0);
    const g30 = (x0_0 ^ 1n);
    const g31 = (g30 | x1_0);
    const g32 = (g31 & g29);
    const g33 = (g32 & g27);
    const g34 = (g33 & g25);
    const g35 = (g34 & g23);
    const g36 = (g35 & g21);
    const g37 = (g36 & g19);
    const g38 = (g37 & g17);
    const g39 = (g38 & g15);
    const g40 = (g39 & g13);
    const g41 = (g40 & g11);
    const g42 = (g41 & g9);
    const g43 = (g42 & g7);
    const g44 = (g43 & g5);
    const g45 = (g44 & g3);
    const g46 = (g45 & g1);
    const g47 = (x0_0 | x0_1);
    const g48 = (x0_2 | g47);
    const g49 = (x0_3 | g48);
    const g50 = (x0_4 | g49);
    const g51 = (x0_5 | g50);
    const g52 = (x0_6 | g51);
    const g53 = (x0_7 | g52);
    const g54 = (g53 ^ x0_7);
    const g55 = (g54 ^ 1n);
    const g56 = (g51 ^ x0_6);
    const g57 = (g56 ^ 1n);
    const g58 = (g4 | g57);
    const g59 = (g58 ^ 1n);
    const g60 = (g49 ^ x0_4);
    const g61 = (g60 ^ 1n);
    const g62 = (g48 ^ x0_3);
    const g63 = (g62 ^ 1n);
    const g64 = (g63 | g16);
    const g65 = (g64 ^ 1n);
    const g66 = (g47 ^ x0_2);
    const g67 = (g66 ^ 1n);
    const g68 = (g67 | g20);
    const g69 = (g68 ^ 1n);
    const g70 = (g30 | g28);
    const g71 = (g24 | g70);
    const g72 = (g71 ^ 1n);
    const g73 = (x0_0 ^ x0_1);
    const g74 = (g73 ^ 1n);
    const g75 = (g74 | g70);
    const g76 = (g75 ^ 1n);
    const g77 = (g24 | g74);
    const g78 = (g77 ^ 1n);
    const g79 = (g78 | g76);
    const g80 = (g79 | g72);
    const g81 = (g80 ^ 1n);
    const g82 = (g20 | g81);
    const g83 = (g82 ^ 1n);
    const g84 = (g67 | g81);
    const g85 = (g84 ^ 1n);
    const g86 = (g85 | g83);
    const g87 = (g86 | g69);
    const g88 = (g87 ^ 1n);
    const g89 = (g63 | g88);
    const g90 = (g89 ^ 1n);
    const g91 = (g16 | g88);
    const g92 = (g91 ^ 1n);
    const g93 = (g92 | g90);
    const g94 = (g93 | g65);
    const g95 = (g94 ^ 1n);
    const g96 = (g95 | g61);
    const g97 = (g96 ^ 1n);
    const g98 = (g61 | g12);
    const g99 = (g98 ^ 1n);
    const g100 = (g12 | g95);
    const g101 = (g100 ^ 1n);
    const g102 = (g101 | g99);
    const g103 = (g102 | g97);
    const g104 = (g103 ^ 1n);
    const g105 = (g8 | g104);
    const g106 = (g105 ^ 1n);
    const g107 = (g50 ^ x0_5);
    const g108 = (g107 ^ 1n);
    const g109 = (g8 | g108);
    const g110 = (g109 ^ 1n);
    const g111 = (g108 | g104);
    const g112 = (g111 ^ 1n);
    const g113 = (g112 | g110);
    const g114 = (g113 | g106);
    const g115 = (g114 ^ 1n);
    const g116 = (g4 | g115);
    const g117 = (g116 ^ 1n);
    const g118 = (g115 | g57);
    const g119 = (g118 ^ 1n);
    const g120 = (g119 | g117);
    const g121 = (g120 | g59);
    const g122 = (g121 ^ 1n);
    const g123 = (g52 ^ x0_7);
    const g124 = (g123 ^ 1n);
    const g125 = (g124 | g122);
    const g126 = (g125 ^ 1n);
    const g127 = (g0 | g122);
    const g128 = (g127 ^ 1n);
    const g129 = (g0 | g124);
    const g130 = (g129 ^ 1n);
    const g131 = (g130 | g128);
    const g132 = (g131 | g126);
    const g133 = (x1_7 ^ g132);
    const g134 = (g133 ^ 1n);
    const g135 = (g134 ^ g55);
    const g136 = (g135 ^ 1n);
    const g137 = (x1_7 ^ g121);
    const g138 = (g137 ^ 1n);
    const g139 = (g138 ^ g124);
    const g140 = (g139 ^ 1n);
    const g141 = (g140 ^ g136);
    const g142 = (g141 ^ 1n);
    const g143 = (g140 ^ g142);
    const g144 = (g143 ^ 1n);
    const g145 = (g144 ^ 1n);
    const g146 = (g145 | g46);
    const k0 = 0n;
    const w0 = x2_63;
    const w1 = cat(w0, x2_62, 1);
    const w2 = cat(w1, x2_61, 1);
    const w3 = cat(w2, x2_60, 1);
    const w4 = cat(w3, x2_59, 1);
    const w5 = cat(w4, x2_58, 1);
    const w6 = cat(w5, x2_57, 1);
    const w7 = cat(w6, x2_56, 1);
    const w8 = cat(w7, x2_55, 1);
    const w9 = cat(w8, x2_54, 1);
    const w10 = cat(w9, x2_53, 1);
    const w11 = cat(w10, x2_52, 1);
    const w12 = cat(w11, x2_51, 1);
    const w13 = cat(w12, x2_50, 1);
    const w14 = cat(w13, x2_49, 1);
    const w15 = cat(w14, x2_48, 1);
    const w16 = cat(w15, x2_47, 1);
    const w17 = cat(w16, x2_46, 1);
    const w18 = cat(w17, x2_45, 1);
    const w19 = cat(w18, x2_44, 1);
    const w20 = cat(w19, x2_43, 1);
    const w21 = cat(w20, x2_42, 1);
    const w22 = cat(w21, x2_41, 1);
    const w23 = cat(w22, x2_40, 1);
    const w24 = cat(w23, x2_39, 1);
    const w25 = cat(w24, x2_38, 1);
    const w26 = cat(w25, x2_37, 1);
    const w27 = cat(w26, x2_36, 1);
    const w28 = cat(w27, x2_35, 1);
    const w29 = cat(w28, x2_34, 1);
    const w30 = cat(w29, x2_33, 1);
    const w31 = cat(w30, x2_32, 1);
    const w32 = cat(w31, x2_31, 1);
    const w33 = cat(w32, x2_30, 1);
    const w34 = cat(w33, x2_29, 1);
    const w35 = cat(w34, x2_28, 1);
    const w36 = cat(w35, x2_27, 1);
    const w37 = cat(w36, x2_26, 1);
    const w38 = cat(w37, x2_25, 1);
    const w39 = cat(w38, x2_24, 1);
    const w40 = cat(w39, x2_23, 1);
    const w41 = cat(w40, x2_22, 1);
    const w42 = cat(w41, x2_21, 1);
    const w43 = cat(w42, x2_20, 1);
    const w44 = cat(w43, x2_19, 1);
    const w45 = cat(w44, x2_18, 1);
    const w46 = cat(w45, x2_17, 1);
    const w47 = cat(w46, x2_16, 1);
    const w48 = cat(w47, x2_15, 1);
    const w49 = cat(w48, x2_14, 1);
    const w50 = cat(w49, x2_13, 1);
    const w51 = cat(w50, x2_12, 1);
    const w52 = cat(w51, x2_11, 1);
    const w53 = cat(w52, x2_10, 1);
    const w54 = cat(w53, x2_9, 1);
    const w55 = cat(w54, x2_8, 1);
    const w56 = cat(w55, k0, 1);
    const w57 = cat(w56, k0, 1);
    const w58 = cat(w57, k0, 1);
    const w59 = cat(w58, k0, 1);
    const w60 = cat(w59, k0, 1);
    const w61 = cat(w60, k0, 1);
    const w62 = cat(w61, k0, 1);
    const w63 = cat(w62, g146, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_setle_gpr_one_8__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
