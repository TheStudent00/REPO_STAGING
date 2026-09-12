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
# one named local per gate, over the term of setb_gpr_one_8__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 0, 1))
def emu_setb_gpr_one_8__reg_rdi__cpython(a, b, c):
    x1_0 = ext(c, 0, 0)
    x2_0 = ext(b, 0, 0)
    x2_1 = ext(b, 1, 1)
    x1_1 = ext(c, 1, 1)
    x2_2 = ext(b, 2, 2)
    x1_2 = ext(c, 2, 2)
    x2_3 = ext(b, 3, 3)
    x1_3 = ext(c, 3, 3)
    x2_4 = ext(b, 4, 4)
    x1_4 = ext(c, 4, 4)
    x2_5 = ext(b, 5, 5)
    x1_5 = ext(c, 5, 5)
    x2_6 = ext(b, 6, 6)
    x1_6 = ext(c, 6, 6)
    x2_7 = ext(b, 7, 7)
    x1_7 = ext(c, 7, 7)
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
    x0_32 = ext(a, 32, 32)
    x0_33 = ext(a, 33, 33)
    x0_34 = ext(a, 34, 34)
    x0_35 = ext(a, 35, 35)
    x0_36 = ext(a, 36, 36)
    x0_37 = ext(a, 37, 37)
    x0_38 = ext(a, 38, 38)
    x0_39 = ext(a, 39, 39)
    x0_40 = ext(a, 40, 40)
    x0_41 = ext(a, 41, 41)
    x0_42 = ext(a, 42, 42)
    x0_43 = ext(a, 43, 43)
    x0_44 = ext(a, 44, 44)
    x0_45 = ext(a, 45, 45)
    x0_46 = ext(a, 46, 46)
    x0_47 = ext(a, 47, 47)
    x0_48 = ext(a, 48, 48)
    x0_49 = ext(a, 49, 49)
    x0_50 = ext(a, 50, 50)
    x0_51 = ext(a, 51, 51)
    x0_52 = ext(a, 52, 52)
    x0_53 = ext(a, 53, 53)
    x0_54 = ext(a, 54, 54)
    x0_55 = ext(a, 55, 55)
    x0_56 = ext(a, 56, 56)
    x0_57 = ext(a, 57, 57)
    x0_58 = ext(a, 58, 58)
    x0_59 = ext(a, 59, 59)
    x0_60 = ext(a, 60, 60)
    x0_61 = ext(a, 61, 61)
    x0_62 = ext(a, 62, 62)
    x0_63 = ext(a, 63, 63)
    g0 = (x1_0 ^ 1)
    g1 = (x2_0 | g0)
    g2 = (g1 ^ 1)
    g3 = (x2_1 ^ 1)
    g4 = (g3 | g2)
    g5 = (g4 ^ 1)
    g6 = (x1_1 | g2)
    g7 = (g6 ^ 1)
    g8 = (x1_1 | g3)
    g9 = (g8 ^ 1)
    g10 = (g9 | g7)
    g11 = (g10 | g5)
    g12 = (g11 ^ 1)
    g13 = (x2_2 ^ 1)
    g14 = (g13 | g12)
    g15 = (g14 ^ 1)
    g16 = (x1_2 | g12)
    g17 = (g16 ^ 1)
    g18 = (x1_2 | g13)
    g19 = (g18 ^ 1)
    g20 = (g19 | g17)
    g21 = (g20 | g15)
    g22 = (g21 ^ 1)
    g23 = (x2_3 ^ 1)
    g24 = (g23 | g22)
    g25 = (g24 ^ 1)
    g26 = (x1_3 | g22)
    g27 = (g26 ^ 1)
    g28 = (x1_3 | g23)
    g29 = (g28 ^ 1)
    g30 = (g29 | g27)
    g31 = (g30 | g25)
    g32 = (g31 ^ 1)
    g33 = (x2_4 ^ 1)
    g34 = (g33 | g32)
    g35 = (g34 ^ 1)
    g36 = (x1_4 | g32)
    g37 = (g36 ^ 1)
    g38 = (x1_4 | g33)
    g39 = (g38 ^ 1)
    g40 = (g39 | g37)
    g41 = (g40 | g35)
    g42 = (g41 ^ 1)
    g43 = (x2_5 ^ 1)
    g44 = (g43 | g42)
    g45 = (g44 ^ 1)
    g46 = (x1_5 | g42)
    g47 = (g46 ^ 1)
    g48 = (x1_5 | g43)
    g49 = (g48 ^ 1)
    g50 = (g49 | g47)
    g51 = (g50 | g45)
    g52 = (g51 ^ 1)
    g53 = (x2_6 ^ 1)
    g54 = (g53 | g52)
    g55 = (g54 ^ 1)
    g56 = (x1_6 | g52)
    g57 = (g56 ^ 1)
    g58 = (x1_6 | g53)
    g59 = (g58 ^ 1)
    g60 = (g59 | g57)
    g61 = (g60 | g55)
    g62 = (g61 ^ 1)
    g63 = (x2_7 ^ 1)
    g64 = (g63 | g62)
    g65 = (x1_7 | g62)
    g66 = (x1_7 | g63)
    g67 = (g66 & g65)
    g68 = (g67 & g64)
    k0 = 0
    w0 = x0_63
    w1 = cat(w0, x0_62, 1)
    w2 = cat(w1, x0_61, 1)
    w3 = cat(w2, x0_60, 1)
    w4 = cat(w3, x0_59, 1)
    w5 = cat(w4, x0_58, 1)
    w6 = cat(w5, x0_57, 1)
    w7 = cat(w6, x0_56, 1)
    w8 = cat(w7, x0_55, 1)
    w9 = cat(w8, x0_54, 1)
    w10 = cat(w9, x0_53, 1)
    w11 = cat(w10, x0_52, 1)
    w12 = cat(w11, x0_51, 1)
    w13 = cat(w12, x0_50, 1)
    w14 = cat(w13, x0_49, 1)
    w15 = cat(w14, x0_48, 1)
    w16 = cat(w15, x0_47, 1)
    w17 = cat(w16, x0_46, 1)
    w18 = cat(w17, x0_45, 1)
    w19 = cat(w18, x0_44, 1)
    w20 = cat(w19, x0_43, 1)
    w21 = cat(w20, x0_42, 1)
    w22 = cat(w21, x0_41, 1)
    w23 = cat(w22, x0_40, 1)
    w24 = cat(w23, x0_39, 1)
    w25 = cat(w24, x0_38, 1)
    w26 = cat(w25, x0_37, 1)
    w27 = cat(w26, x0_36, 1)
    w28 = cat(w27, x0_35, 1)
    w29 = cat(w28, x0_34, 1)
    w30 = cat(w29, x0_33, 1)
    w31 = cat(w30, x0_32, 1)
    w32 = cat(w31, x0_31, 1)
    w33 = cat(w32, x0_30, 1)
    w34 = cat(w33, x0_29, 1)
    w35 = cat(w34, x0_28, 1)
    w36 = cat(w35, x0_27, 1)
    w37 = cat(w36, x0_26, 1)
    w38 = cat(w37, x0_25, 1)
    w39 = cat(w38, x0_24, 1)
    w40 = cat(w39, x0_23, 1)
    w41 = cat(w40, x0_22, 1)
    w42 = cat(w41, x0_21, 1)
    w43 = cat(w42, x0_20, 1)
    w44 = cat(w43, x0_19, 1)
    w45 = cat(w44, x0_18, 1)
    w46 = cat(w45, x0_17, 1)
    w47 = cat(w46, x0_16, 1)
    w48 = cat(w47, x0_15, 1)
    w49 = cat(w48, x0_14, 1)
    w50 = cat(w49, x0_13, 1)
    w51 = cat(w50, x0_12, 1)
    w52 = cat(w51, x0_11, 1)
    w53 = cat(w52, x0_10, 1)
    w54 = cat(w53, x0_9, 1)
    w55 = cat(w54, x0_8, 1)
    w56 = cat(w55, k0, 1)
    w57 = cat(w56, k0, 1)
    w58 = cat(w57, k0, 1)
    w59 = cat(w58, k0, 1)
    w60 = cat(w59, k0, 1)
    w61 = cat(w60, k0, 1)
    w62 = cat(w61, k0, 1)
    w63 = cat(w62, g68, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_setb_gpr_one_8__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
