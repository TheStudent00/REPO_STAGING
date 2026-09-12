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
# one named local per gate, over the term of cmp_gpr_gpr_32__flags__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
def emu_cmp_gpr_gpr_32__flags__cpython(a, b):
    x1_0 = ext(b, 0, 0)
    x1_1 = ext(b, 1, 1)
    x1_2 = ext(b, 2, 2)
    x1_3 = ext(b, 3, 3)
    x1_4 = ext(b, 4, 4)
    x1_5 = ext(b, 5, 5)
    x1_6 = ext(b, 6, 6)
    x1_7 = ext(b, 7, 7)
    x1_8 = ext(b, 8, 8)
    x1_9 = ext(b, 9, 9)
    x1_10 = ext(b, 10, 10)
    x1_11 = ext(b, 11, 11)
    x1_12 = ext(b, 12, 12)
    x1_13 = ext(b, 13, 13)
    x1_14 = ext(b, 14, 14)
    x1_15 = ext(b, 15, 15)
    x1_16 = ext(b, 16, 16)
    x1_17 = ext(b, 17, 17)
    x1_18 = ext(b, 18, 18)
    x1_19 = ext(b, 19, 19)
    x1_20 = ext(b, 20, 20)
    x1_21 = ext(b, 21, 21)
    x1_22 = ext(b, 22, 22)
    x1_23 = ext(b, 23, 23)
    x1_24 = ext(b, 24, 24)
    x1_25 = ext(b, 25, 25)
    x1_26 = ext(b, 26, 26)
    x1_27 = ext(b, 27, 27)
    x1_28 = ext(b, 28, 28)
    x1_29 = ext(b, 29, 29)
    x1_30 = ext(b, 30, 30)
    x1_31 = ext(b, 31, 31)
    x0_0 = ext(a, 0, 0)
    x0_1 = ext(a, 1, 1)
    x0_2 = ext(a, 2, 2)
    x0_3 = ext(a, 3, 3)
    x0_4 = ext(a, 4, 4)
    x0_5 = ext(a, 5, 5)
    x0_6 = ext(a, 6, 6)
    x0_7 = ext(a, 7, 7)
    x0_8 = ext(a, 8, 8)
    x0_9 = ext(a, 9, 9)
    x0_10 = ext(a, 10, 10)
    x0_11 = ext(a, 11, 11)
    x0_12 = ext(a, 12, 12)
    x0_13 = ext(a, 13, 13)
    x0_14 = ext(a, 14, 14)
    x0_15 = ext(a, 15, 15)
    x0_16 = ext(a, 16, 16)
    x0_17 = ext(a, 17, 17)
    x0_18 = ext(a, 18, 18)
    x0_19 = ext(a, 19, 19)
    x0_20 = ext(a, 20, 20)
    x0_21 = ext(a, 21, 21)
    x0_22 = ext(a, 22, 22)
    x0_23 = ext(a, 23, 23)
    x0_24 = ext(a, 24, 24)
    x0_25 = ext(a, 25, 25)
    x0_26 = ext(a, 26, 26)
    x0_27 = ext(a, 27, 27)
    x0_28 = ext(a, 28, 28)
    x0_29 = ext(a, 29, 29)
    x0_30 = ext(a, 30, 30)
    x0_31 = ext(a, 31, 31)
    w0 = x0_31
    w1 = cat(w0, x0_30, 1)
    w2 = cat(w1, x0_29, 1)
    w3 = cat(w2, x0_28, 1)
    w4 = cat(w3, x0_27, 1)
    w5 = cat(w4, x0_26, 1)
    w6 = cat(w5, x0_25, 1)
    w7 = cat(w6, x0_24, 1)
    w8 = cat(w7, x0_23, 1)
    w9 = cat(w8, x0_22, 1)
    w10 = cat(w9, x0_21, 1)
    w11 = cat(w10, x0_20, 1)
    w12 = cat(w11, x0_19, 1)
    w13 = cat(w12, x0_18, 1)
    w14 = cat(w13, x0_17, 1)
    w15 = cat(w14, x0_16, 1)
    w16 = cat(w15, x0_15, 1)
    w17 = cat(w16, x0_14, 1)
    w18 = cat(w17, x0_13, 1)
    w19 = cat(w18, x0_12, 1)
    w20 = cat(w19, x0_11, 1)
    w21 = cat(w20, x0_10, 1)
    w22 = cat(w21, x0_9, 1)
    w23 = cat(w22, x0_8, 1)
    w24 = cat(w23, x0_7, 1)
    w25 = cat(w24, x0_6, 1)
    w26 = cat(w25, x0_5, 1)
    w27 = cat(w26, x0_4, 1)
    w28 = cat(w27, x0_3, 1)
    w29 = cat(w28, x0_2, 1)
    w30 = cat(w29, x0_1, 1)
    w31 = cat(w30, x0_0, 1)
    w32 = cat(w31, x1_31, 1)
    w33 = cat(w32, x1_30, 1)
    w34 = cat(w33, x1_29, 1)
    w35 = cat(w34, x1_28, 1)
    w36 = cat(w35, x1_27, 1)
    w37 = cat(w36, x1_26, 1)
    w38 = cat(w37, x1_25, 1)
    w39 = cat(w38, x1_24, 1)
    w40 = cat(w39, x1_23, 1)
    w41 = cat(w40, x1_22, 1)
    w42 = cat(w41, x1_21, 1)
    w43 = cat(w42, x1_20, 1)
    w44 = cat(w43, x1_19, 1)
    w45 = cat(w44, x1_18, 1)
    w46 = cat(w45, x1_17, 1)
    w47 = cat(w46, x1_16, 1)
    w48 = cat(w47, x1_15, 1)
    w49 = cat(w48, x1_14, 1)
    w50 = cat(w49, x1_13, 1)
    w51 = cat(w50, x1_12, 1)
    w52 = cat(w51, x1_11, 1)
    w53 = cat(w52, x1_10, 1)
    w54 = cat(w53, x1_9, 1)
    w55 = cat(w54, x1_8, 1)
    w56 = cat(w55, x1_7, 1)
    w57 = cat(w56, x1_6, 1)
    w58 = cat(w57, x1_5, 1)
    w59 = cat(w58, x1_4, 1)
    w60 = cat(w59, x1_3, 1)
    w61 = cat(w60, x1_2, 1)
    w62 = cat(w61, x1_1, 1)
    w63 = cat(w62, x1_0, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_cmp_gpr_gpr_32__flags__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
