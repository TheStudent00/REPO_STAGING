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
// one named local per gate, over the term of test_cl_gpr_8__flags__javascript.
// The term's layer-5 text, LITERAL:
//   Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
function emu_test_cl_gpr_8__flags__javascript(a, b) {
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
    const k0 = 0n;
    const g0 = (x0_0 & x1_0);
    const g1 = (x0_1 & x1_1);
    const g2 = (x0_2 & x1_2);
    const g3 = (x0_3 & x1_3);
    const g4 = (x0_4 & x1_4);
    const g5 = (x0_5 & x1_5);
    const g6 = (x0_6 & x1_6);
    const g7 = (x0_7 & x1_7);
    const w0 = g7;
    const w1 = cat(w0, g6, 1);
    const w2 = cat(w1, g5, 1);
    const w3 = cat(w2, g4, 1);
    const w4 = cat(w3, g3, 1);
    const w5 = cat(w4, g2, 1);
    const w6 = cat(w5, g1, 1);
    const w7 = cat(w6, g0, 1);
    const w8 = cat(w7, k0, 1);
    const w9 = cat(w8, k0, 1);
    const w10 = cat(w9, k0, 1);
    const w11 = cat(w10, k0, 1);
    const w12 = cat(w11, k0, 1);
    const w13 = cat(w12, k0, 1);
    const w14 = cat(w13, k0, 1);
    const w15 = cat(w14, k0, 1);
    return m(w15, 16);
}



const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_test_cl_gpr_8__flags__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
