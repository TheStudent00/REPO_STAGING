import struct
import sys


def m(x, w):
    return x & ((1 << w) - 1)


def s(x, w):
    x = x & ((1 << w) - 1)
    if x >> (w - 1):
        return x - (1 << w)
    return x


def add(a, b, w):
    return m(a + b, w)


def sub(a, b, w):
    return m(a - b, w)


def mul(a, b, w):
    return m(a * b, w)


def band(a, b, w):
    return m(a & b, w)


def bor(a, b, w):
    return m(a | b, w)


def bxor(a, b, w):
    return m(a ^ b, w)


def bnot(a, w):
    return m(~a, w)


def bneg(a, w):
    return m(-a, w)


def shl(a, n, w):
    if n >= w:
        return 0
    return m(a << n, w)


def lshr(a, n, w):
    if n >= w:
        return 0
    return m(a, w) >> n


def ashr(a, n, w):
    v = s(a, w)
    k = n
    if k >= w:
        k = w - 1
    return m(v >> k, w)


def udiv(a, b, w):
    return m(m(a, w) // m(b, w), w)


def urem(a, b, w):
    return m(m(a, w) % m(b, w), w)


def sdiv(a, b, w):
    x = s(a, w)
    y = s(b, w)
    q = abs(x) // abs(y)
    if (x < 0) != (y < 0):
        q = -q
    return m(q, w)


def srem(a, b, w):
    x = s(a, w)
    y = s(b, w)
    r = abs(x) % abs(y)
    if x < 0:
        r = -r
    return m(r, w)


def ult(a, b, w):
    return m(a, w) < m(b, w)


def ule(a, b, w):
    return m(a, w) <= m(b, w)


def ugt(a, b, w):
    return m(a, w) > m(b, w)


def uge(a, b, w):
    return m(a, w) >= m(b, w)


def slt(a, b, w):
    return s(a, w) < s(b, w)


def sle(a, b, w):
    return s(a, w) <= s(b, w)


def sgt(a, b, w):
    return s(a, w) > s(b, w)


def sge(a, b, w):
    return s(a, w) >= s(b, w)


def eq(a, b, w):
    return m(a, w) == m(b, w)


def ne(a, b, w):
    return m(a, w) != m(b, w)


def cat(hi, lo, lw):
    return (hi << lw) | m(lo, lw)


def ext(x, hi, lo):
    return m(x >> lo, hi - lo + 1)


def sext(x, fromw, tow):
    return m(s(x, fromw), tow)


def b2f(x, w):
    if w == 32:
        return struct.unpack("<f", struct.pack("<I", m(x, 32)))[0]
    return struct.unpack("<d", struct.pack("<Q", m(x, 64)))[0]


def f2b(f, w):
    if w == 32:
        try:
            return struct.unpack("<I", struct.pack("<f", f))[0]
        except OverflowError:
            if f > 0:
                return 0x7f800000
            return 0xff800000
    return struct.unpack("<Q", struct.pack("<d", f))[0]


def fadd(a, b, w):
    return f2b(b2f(a, w) + b2f(b, w), w)


def fsub(a, b, w):
    return f2b(b2f(a, w) - b2f(b, w), w)


def fmul(a, b, w):
    return f2b(b2f(a, w) * b2f(b, w), w)


def fdiv(a, b, w):
    return f2b(b2f(a, w) / b2f(b, w), w)


def i2f(x, fromw, w):
    return f2b(float(s(x, fromw)), w)


def u2f(x, fromw, w):
    return f2b(float(m(x, fromw)), w)


def fwiden(x, fromw, w):
    return f2b(b2f(x, fromw), w)

# task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
# one named local per gate, over the term of movsbl_widen_gpr_gpr_32__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(0, Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 0, v0))
def emu_movsbl_widen_gpr_gpr_32__reg_rdi__cpython(a):
    x0_0 = ext(a, 0, 0)
    x0_1 = ext(a, 1, 1)
    x0_2 = ext(a, 2, 2)
    x0_3 = ext(a, 3, 3)
    x0_4 = ext(a, 4, 4)
    x0_5 = ext(a, 5, 5)
    x0_6 = ext(a, 6, 6)
    x0_7 = ext(a, 7, 7)
    k0 = 0
    w0 = k0
    w1 = cat(w0, k0, 1)
    w2 = cat(w1, k0, 1)
    w3 = cat(w2, k0, 1)
    w4 = cat(w3, k0, 1)
    w5 = cat(w4, k0, 1)
    w6 = cat(w5, k0, 1)
    w7 = cat(w6, k0, 1)
    w8 = cat(w7, k0, 1)
    w9 = cat(w8, k0, 1)
    w10 = cat(w9, k0, 1)
    w11 = cat(w10, k0, 1)
    w12 = cat(w11, k0, 1)
    w13 = cat(w12, k0, 1)
    w14 = cat(w13, k0, 1)
    w15 = cat(w14, k0, 1)
    w16 = cat(w15, k0, 1)
    w17 = cat(w16, k0, 1)
    w18 = cat(w17, k0, 1)
    w19 = cat(w18, k0, 1)
    w20 = cat(w19, k0, 1)
    w21 = cat(w20, k0, 1)
    w22 = cat(w21, k0, 1)
    w23 = cat(w22, k0, 1)
    w24 = cat(w23, k0, 1)
    w25 = cat(w24, k0, 1)
    w26 = cat(w25, k0, 1)
    w27 = cat(w26, k0, 1)
    w28 = cat(w27, k0, 1)
    w29 = cat(w28, k0, 1)
    w30 = cat(w29, k0, 1)
    w31 = cat(w30, k0, 1)
    w32 = cat(w31, x0_7, 1)
    w33 = cat(w32, x0_7, 1)
    w34 = cat(w33, x0_7, 1)
    w35 = cat(w34, x0_7, 1)
    w36 = cat(w35, x0_7, 1)
    w37 = cat(w36, x0_7, 1)
    w38 = cat(w37, x0_7, 1)
    w39 = cat(w38, x0_7, 1)
    w40 = cat(w39, x0_7, 1)
    w41 = cat(w40, x0_7, 1)
    w42 = cat(w41, x0_7, 1)
    w43 = cat(w42, x0_7, 1)
    w44 = cat(w43, x0_7, 1)
    w45 = cat(w44, x0_7, 1)
    w46 = cat(w45, x0_7, 1)
    w47 = cat(w46, x0_7, 1)
    w48 = cat(w47, x0_7, 1)
    w49 = cat(w48, x0_7, 1)
    w50 = cat(w49, x0_7, 1)
    w51 = cat(w50, x0_7, 1)
    w52 = cat(w51, x0_7, 1)
    w53 = cat(w52, x0_7, 1)
    w54 = cat(w53, x0_7, 1)
    w55 = cat(w54, x0_7, 1)
    w56 = cat(w55, x0_7, 1)
    w57 = cat(w56, x0_6, 1)
    w58 = cat(w57, x0_5, 1)
    w59 = cat(w58, x0_4, 1)
    w60 = cat(w59, x0_3, 1)
    w61 = cat(w60, x0_2, 1)
    w62 = cat(w61, x0_1, 1)
    w63 = cat(w62, x0_0, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_movsbl_widen_gpr_gpr_32__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
