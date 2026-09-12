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
// one named local per gate, over the term of setb_gpr_one_8__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 0, 1))
function emu_setb_gpr_one_8__reg_rdi__javascript(a, b, c) {
    const x1_0 = ext(c, 0, 0);
    const x2_0 = ext(b, 0, 0);
    const x2_1 = ext(b, 1, 1);
    const x1_1 = ext(c, 1, 1);
    const x2_2 = ext(b, 2, 2);
    const x1_2 = ext(c, 2, 2);
    const x2_3 = ext(b, 3, 3);
    const x1_3 = ext(c, 3, 3);
    const x2_4 = ext(b, 4, 4);
    const x1_4 = ext(c, 4, 4);
    const x2_5 = ext(b, 5, 5);
    const x1_5 = ext(c, 5, 5);
    const x2_6 = ext(b, 6, 6);
    const x1_6 = ext(c, 6, 6);
    const x2_7 = ext(b, 7, 7);
    const x1_7 = ext(c, 7, 7);
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
    const g0 = (x1_0 ^ 1n);
    const g1 = (x2_0 | g0);
    const g2 = (g1 ^ 1n);
    const g3 = (x2_1 ^ 1n);
    const g4 = (g3 | g2);
    const g5 = (g4 ^ 1n);
    const g6 = (x1_1 | g2);
    const g7 = (g6 ^ 1n);
    const g8 = (x1_1 | g3);
    const g9 = (g8 ^ 1n);
    const g10 = (g9 | g7);
    const g11 = (g10 | g5);
    const g12 = (g11 ^ 1n);
    const g13 = (x2_2 ^ 1n);
    const g14 = (g13 | g12);
    const g15 = (g14 ^ 1n);
    const g16 = (x1_2 | g12);
    const g17 = (g16 ^ 1n);
    const g18 = (x1_2 | g13);
    const g19 = (g18 ^ 1n);
    const g20 = (g19 | g17);
    const g21 = (g20 | g15);
    const g22 = (g21 ^ 1n);
    const g23 = (x2_3 ^ 1n);
    const g24 = (g23 | g22);
    const g25 = (g24 ^ 1n);
    const g26 = (x1_3 | g22);
    const g27 = (g26 ^ 1n);
    const g28 = (x1_3 | g23);
    const g29 = (g28 ^ 1n);
    const g30 = (g29 | g27);
    const g31 = (g30 | g25);
    const g32 = (g31 ^ 1n);
    const g33 = (x2_4 ^ 1n);
    const g34 = (g33 | g32);
    const g35 = (g34 ^ 1n);
    const g36 = (x1_4 | g32);
    const g37 = (g36 ^ 1n);
    const g38 = (x1_4 | g33);
    const g39 = (g38 ^ 1n);
    const g40 = (g39 | g37);
    const g41 = (g40 | g35);
    const g42 = (g41 ^ 1n);
    const g43 = (x2_5 ^ 1n);
    const g44 = (g43 | g42);
    const g45 = (g44 ^ 1n);
    const g46 = (x1_5 | g42);
    const g47 = (g46 ^ 1n);
    const g48 = (x1_5 | g43);
    const g49 = (g48 ^ 1n);
    const g50 = (g49 | g47);
    const g51 = (g50 | g45);
    const g52 = (g51 ^ 1n);
    const g53 = (x2_6 ^ 1n);
    const g54 = (g53 | g52);
    const g55 = (g54 ^ 1n);
    const g56 = (x1_6 | g52);
    const g57 = (g56 ^ 1n);
    const g58 = (x1_6 | g53);
    const g59 = (g58 ^ 1n);
    const g60 = (g59 | g57);
    const g61 = (g60 | g55);
    const g62 = (g61 ^ 1n);
    const g63 = (x2_7 ^ 1n);
    const g64 = (g63 | g62);
    const g65 = (x1_7 | g62);
    const g66 = (x1_7 | g63);
    const g67 = (g66 & g65);
    const g68 = (g67 & g64);
    const k0 = 0n;
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
    const w49 = cat(w48, x0_14, 1);
    const w50 = cat(w49, x0_13, 1);
    const w51 = cat(w50, x0_12, 1);
    const w52 = cat(w51, x0_11, 1);
    const w53 = cat(w52, x0_10, 1);
    const w54 = cat(w53, x0_9, 1);
    const w55 = cat(w54, x0_8, 1);
    const w56 = cat(w55, k0, 1);
    const w57 = cat(w56, k0, 1);
    const w58 = cat(w57, k0, 1);
    const w59 = cat(w58, k0, 1);
    const w60 = cat(w59, k0, 1);
    const w61 = cat(w60, k0, 1);
    const w62 = cat(w61, k0, 1);
    const w63 = cat(w62, g68, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_setb_gpr_one_8__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
