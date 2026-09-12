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
// one named local per gate, over the term of cmovns_gpr_gpr_32__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Or(Extract(31, 31, v0) == 0, Extract(31, 31, v1) == 0), Extract(31, 0, v2), Extract(31, 0, v3)))
function emu_cmovns_gpr_gpr_32__reg_rdi__javascript(a, b, c, d) {
    const x3_0 = ext(d, 0, 0);
    const x1_31 = ext(a, 31, 31);
    const x0_31 = ext(b, 31, 31);
    const x2_0 = ext(c, 0, 0);
    const x3_1 = ext(d, 1, 1);
    const x2_1 = ext(c, 1, 1);
    const x3_2 = ext(d, 2, 2);
    const x2_2 = ext(c, 2, 2);
    const x3_3 = ext(d, 3, 3);
    const x2_3 = ext(c, 3, 3);
    const x3_4 = ext(d, 4, 4);
    const x2_4 = ext(c, 4, 4);
    const x3_5 = ext(d, 5, 5);
    const x2_5 = ext(c, 5, 5);
    const x3_6 = ext(d, 6, 6);
    const x2_6 = ext(c, 6, 6);
    const x3_7 = ext(d, 7, 7);
    const x2_7 = ext(c, 7, 7);
    const x3_8 = ext(d, 8, 8);
    const x2_8 = ext(c, 8, 8);
    const x3_9 = ext(d, 9, 9);
    const x2_9 = ext(c, 9, 9);
    const x3_10 = ext(d, 10, 10);
    const x2_10 = ext(c, 10, 10);
    const x3_11 = ext(d, 11, 11);
    const x2_11 = ext(c, 11, 11);
    const x3_12 = ext(d, 12, 12);
    const x2_12 = ext(c, 12, 12);
    const x3_13 = ext(d, 13, 13);
    const x2_13 = ext(c, 13, 13);
    const x3_14 = ext(d, 14, 14);
    const x2_14 = ext(c, 14, 14);
    const x3_15 = ext(d, 15, 15);
    const x2_15 = ext(c, 15, 15);
    const x3_16 = ext(d, 16, 16);
    const x2_16 = ext(c, 16, 16);
    const x3_17 = ext(d, 17, 17);
    const x2_17 = ext(c, 17, 17);
    const x3_18 = ext(d, 18, 18);
    const x2_18 = ext(c, 18, 18);
    const x3_19 = ext(d, 19, 19);
    const x2_19 = ext(c, 19, 19);
    const x3_20 = ext(d, 20, 20);
    const x2_20 = ext(c, 20, 20);
    const x3_21 = ext(d, 21, 21);
    const x2_21 = ext(c, 21, 21);
    const x3_22 = ext(d, 22, 22);
    const x2_22 = ext(c, 22, 22);
    const x3_23 = ext(d, 23, 23);
    const x2_23 = ext(c, 23, 23);
    const x3_24 = ext(d, 24, 24);
    const x2_24 = ext(c, 24, 24);
    const x3_25 = ext(d, 25, 25);
    const x2_25 = ext(c, 25, 25);
    const x3_26 = ext(d, 26, 26);
    const x2_26 = ext(c, 26, 26);
    const x3_27 = ext(d, 27, 27);
    const x2_27 = ext(c, 27, 27);
    const x3_28 = ext(d, 28, 28);
    const x2_28 = ext(c, 28, 28);
    const x3_29 = ext(d, 29, 29);
    const x2_29 = ext(c, 29, 29);
    const x3_30 = ext(d, 30, 30);
    const x2_30 = ext(c, 30, 30);
    const x3_31 = ext(d, 31, 31);
    const x2_31 = ext(c, 31, 31);
    const g0 = (x1_31 ^ 1n);
    const g1 = (x0_31 ^ 1n);
    const g2 = (g1 | g0);
    const g3 = (g2 ^ 1n);
    const g4 = (g3 & x3_0);
    const g5 = (g2 & x2_0);
    const g6 = (g5 | g4);
    const g7 = (g3 & x3_1);
    const g8 = (g2 & x2_1);
    const g9 = (g8 | g7);
    const g10 = (g3 & x3_2);
    const g11 = (g2 & x2_2);
    const g12 = (g11 | g10);
    const g13 = (g3 & x3_3);
    const g14 = (g2 & x2_3);
    const g15 = (g14 | g13);
    const g16 = (g3 & x3_4);
    const g17 = (g2 & x2_4);
    const g18 = (g17 | g16);
    const g19 = (g3 & x3_5);
    const g20 = (g2 & x2_5);
    const g21 = (g20 | g19);
    const g22 = (g3 & x3_6);
    const g23 = (g2 & x2_6);
    const g24 = (g23 | g22);
    const g25 = (g3 & x3_7);
    const g26 = (g2 & x2_7);
    const g27 = (g26 | g25);
    const g28 = (g3 & x3_8);
    const g29 = (g2 & x2_8);
    const g30 = (g29 | g28);
    const g31 = (g3 & x3_9);
    const g32 = (g2 & x2_9);
    const g33 = (g32 | g31);
    const g34 = (g3 & x3_10);
    const g35 = (g2 & x2_10);
    const g36 = (g35 | g34);
    const g37 = (g3 & x3_11);
    const g38 = (g2 & x2_11);
    const g39 = (g38 | g37);
    const g40 = (g3 & x3_12);
    const g41 = (g2 & x2_12);
    const g42 = (g41 | g40);
    const g43 = (g3 & x3_13);
    const g44 = (g2 & x2_13);
    const g45 = (g44 | g43);
    const g46 = (g3 & x3_14);
    const g47 = (g2 & x2_14);
    const g48 = (g47 | g46);
    const g49 = (g3 & x3_15);
    const g50 = (g2 & x2_15);
    const g51 = (g50 | g49);
    const g52 = (g3 & x3_16);
    const g53 = (g2 & x2_16);
    const g54 = (g53 | g52);
    const g55 = (g3 & x3_17);
    const g56 = (g2 & x2_17);
    const g57 = (g56 | g55);
    const g58 = (g3 & x3_18);
    const g59 = (g2 & x2_18);
    const g60 = (g59 | g58);
    const g61 = (g3 & x3_19);
    const g62 = (g2 & x2_19);
    const g63 = (g62 | g61);
    const g64 = (g3 & x3_20);
    const g65 = (g2 & x2_20);
    const g66 = (g65 | g64);
    const g67 = (g3 & x3_21);
    const g68 = (g2 & x2_21);
    const g69 = (g68 | g67);
    const g70 = (g3 & x3_22);
    const g71 = (g2 & x2_22);
    const g72 = (g71 | g70);
    const g73 = (g3 & x3_23);
    const g74 = (g2 & x2_23);
    const g75 = (g74 | g73);
    const g76 = (g3 & x3_24);
    const g77 = (g2 & x2_24);
    const g78 = (g77 | g76);
    const g79 = (g3 & x3_25);
    const g80 = (g2 & x2_25);
    const g81 = (g80 | g79);
    const g82 = (g3 & x3_26);
    const g83 = (g2 & x2_26);
    const g84 = (g83 | g82);
    const g85 = (g3 & x3_27);
    const g86 = (g2 & x2_27);
    const g87 = (g86 | g85);
    const g88 = (g3 & x3_28);
    const g89 = (g2 & x2_28);
    const g90 = (g89 | g88);
    const g91 = (g3 & x3_29);
    const g92 = (g2 & x2_29);
    const g93 = (g92 | g91);
    const g94 = (g3 & x3_30);
    const g95 = (g2 & x2_30);
    const g96 = (g95 | g94);
    const g97 = (g3 & x3_31);
    const g98 = (g2 & x2_31);
    const g99 = (g98 | g97);
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
    const w32 = cat(w31, g99, 1);
    const w33 = cat(w32, g96, 1);
    const w34 = cat(w33, g93, 1);
    const w35 = cat(w34, g90, 1);
    const w36 = cat(w35, g87, 1);
    const w37 = cat(w36, g84, 1);
    const w38 = cat(w37, g81, 1);
    const w39 = cat(w38, g78, 1);
    const w40 = cat(w39, g75, 1);
    const w41 = cat(w40, g72, 1);
    const w42 = cat(w41, g69, 1);
    const w43 = cat(w42, g66, 1);
    const w44 = cat(w43, g63, 1);
    const w45 = cat(w44, g60, 1);
    const w46 = cat(w45, g57, 1);
    const w47 = cat(w46, g54, 1);
    const w48 = cat(w47, g51, 1);
    const w49 = cat(w48, g48, 1);
    const w50 = cat(w49, g45, 1);
    const w51 = cat(w50, g42, 1);
    const w52 = cat(w51, g39, 1);
    const w53 = cat(w52, g36, 1);
    const w54 = cat(w53, g33, 1);
    const w55 = cat(w54, g30, 1);
    const w56 = cat(w55, g27, 1);
    const w57 = cat(w56, g24, 1);
    const w58 = cat(w57, g21, 1);
    const w59 = cat(w58, g18, 1);
    const w60 = cat(w59, g15, 1);
    const w61 = cat(w60, g12, 1);
    const w62 = cat(w61, g9, 1);
    const w63 = cat(w62, g6, 1);
    return m(w63, 64);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_cmovns_gpr_gpr_32__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
