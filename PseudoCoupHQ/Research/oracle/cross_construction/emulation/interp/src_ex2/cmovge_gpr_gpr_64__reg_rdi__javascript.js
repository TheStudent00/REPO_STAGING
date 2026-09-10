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

// task ex1 emulation -- rendered by interp_render.py
// InterpRenderer from the layer-4 term of cmovge_gpr_gpr_64__reg_rdi__javascript.
// The term's layer-5 text, LITERAL:
//   If(v0 <= v1, v2, v3)
function emu_cmovge_gpr_gpr_64__reg_rdi__javascript(a, b, c, d) {
    return m(((sle(b, a, 64)) ? (c) : (d)), 64);
}


const lines = require("fs").readFileSync(0, "utf8").split("\n");
const out = [];
for (const line of lines) {
    const text = line.trim();
    if (text.length === 0) { continue; }
    const values = text.split(/\s+/).map((one) => BigInt(one));
    try {
        out.push(emu_cmovge_gpr_gpr_64__reg_rdi__javascript(...values).toString());
    } catch (problem) {
        out.push("RAISE:" + problem.name);
    }
}
process.stdout.write(out.join("\n") + "\n");
