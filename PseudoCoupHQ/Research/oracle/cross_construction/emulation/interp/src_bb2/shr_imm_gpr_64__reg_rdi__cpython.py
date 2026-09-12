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
# one named local per gate, over the term of shr_imm_gpr_64__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(0, Extract(63, 3, v0))
def emu_shr_imm_gpr_64__reg_rdi__cpython(a):
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
    k0 = 0
    w0 = k0
    w1 = cat(w0, k0, 1)
    w2 = cat(w1, k0, 1)
    w3 = cat(w2, x0_63, 1)
    w4 = cat(w3, x0_62, 1)
    w5 = cat(w4, x0_61, 1)
    w6 = cat(w5, x0_60, 1)
    w7 = cat(w6, x0_59, 1)
    w8 = cat(w7, x0_58, 1)
    w9 = cat(w8, x0_57, 1)
    w10 = cat(w9, x0_56, 1)
    w11 = cat(w10, x0_55, 1)
    w12 = cat(w11, x0_54, 1)
    w13 = cat(w12, x0_53, 1)
    w14 = cat(w13, x0_52, 1)
    w15 = cat(w14, x0_51, 1)
    w16 = cat(w15, x0_50, 1)
    w17 = cat(w16, x0_49, 1)
    w18 = cat(w17, x0_48, 1)
    w19 = cat(w18, x0_47, 1)
    w20 = cat(w19, x0_46, 1)
    w21 = cat(w20, x0_45, 1)
    w22 = cat(w21, x0_44, 1)
    w23 = cat(w22, x0_43, 1)
    w24 = cat(w23, x0_42, 1)
    w25 = cat(w24, x0_41, 1)
    w26 = cat(w25, x0_40, 1)
    w27 = cat(w26, x0_39, 1)
    w28 = cat(w27, x0_38, 1)
    w29 = cat(w28, x0_37, 1)
    w30 = cat(w29, x0_36, 1)
    w31 = cat(w30, x0_35, 1)
    w32 = cat(w31, x0_34, 1)
    w33 = cat(w32, x0_33, 1)
    w34 = cat(w33, x0_32, 1)
    w35 = cat(w34, x0_31, 1)
    w36 = cat(w35, x0_30, 1)
    w37 = cat(w36, x0_29, 1)
    w38 = cat(w37, x0_28, 1)
    w39 = cat(w38, x0_27, 1)
    w40 = cat(w39, x0_26, 1)
    w41 = cat(w40, x0_25, 1)
    w42 = cat(w41, x0_24, 1)
    w43 = cat(w42, x0_23, 1)
    w44 = cat(w43, x0_22, 1)
    w45 = cat(w44, x0_21, 1)
    w46 = cat(w45, x0_20, 1)
    w47 = cat(w46, x0_19, 1)
    w48 = cat(w47, x0_18, 1)
    w49 = cat(w48, x0_17, 1)
    w50 = cat(w49, x0_16, 1)
    w51 = cat(w50, x0_15, 1)
    w52 = cat(w51, x0_14, 1)
    w53 = cat(w52, x0_13, 1)
    w54 = cat(w53, x0_12, 1)
    w55 = cat(w54, x0_11, 1)
    w56 = cat(w55, x0_10, 1)
    w57 = cat(w56, x0_9, 1)
    w58 = cat(w57, x0_8, 1)
    w59 = cat(w58, x0_7, 1)
    w60 = cat(w59, x0_6, 1)
    w61 = cat(w60, x0_5, 1)
    w62 = cat(w61, x0_4, 1)
    w63 = cat(w62, x0_3, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_shr_imm_gpr_64__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
