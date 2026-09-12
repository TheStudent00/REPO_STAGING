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
// one named local per gate, over the term of sets_gpr_one_8__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v2), If(Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0), 0, 1))
function emu_sets_gpr_one_8__reg_rdi__javascript(a, b, c) {
    const x1_7 = ext(a, 7, 7);
    const x0_7 = ext(b, 7, 7);
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
    const g0 = (x0_7 & x1_7);
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
    const w63 = cat(w62, g0, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_sets_gpr_one_8__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
