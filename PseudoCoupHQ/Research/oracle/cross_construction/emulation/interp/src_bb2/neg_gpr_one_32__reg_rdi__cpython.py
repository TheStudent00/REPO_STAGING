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
# one named local per gate, over the term of neg_gpr_one_32__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(0, Extract(31, 0, v0)*4294967295)
def emu_neg_gpr_one_32__reg_rdi__cpython(a):
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
    g0 = (x0_0 ^ x0_1)
    g1 = (g0 ^ 1)
    g2 = (g1 ^ 1)
    g3 = (x0_1 | x0_0)
    g4 = (g3 ^ x0_2)
    g5 = (g4 ^ 1)
    g6 = (g5 ^ 1)
    g7 = (x0_2 | g3)
    g8 = (g7 ^ x0_3)
    g9 = (g8 ^ 1)
    g10 = (g9 ^ 1)
    g11 = (x0_3 | g7)
    g12 = (g11 ^ x0_4)
    g13 = (g12 ^ 1)
    g14 = (g13 ^ 1)
    g15 = (x0_4 | g11)
    g16 = (g15 ^ x0_5)
    g17 = (g16 ^ 1)
    g18 = (g17 ^ 1)
    g19 = (x0_5 | g15)
    g20 = (g19 ^ x0_6)
    g21 = (g20 ^ 1)
    g22 = (g21 ^ 1)
    g23 = (x0_6 | g19)
    g24 = (g23 ^ x0_7)
    g25 = (g24 ^ 1)
    g26 = (g25 ^ 1)
    g27 = (x0_7 | g23)
    g28 = (g27 ^ x0_8)
    g29 = (g28 ^ 1)
    g30 = (g29 ^ 1)
    g31 = (x0_8 | g27)
    g32 = (g31 ^ x0_9)
    g33 = (g32 ^ 1)
    g34 = (g33 ^ 1)
    g35 = (x0_9 | g31)
    g36 = (g35 ^ x0_10)
    g37 = (g36 ^ 1)
    g38 = (g37 ^ 1)
    g39 = (x0_10 | g35)
    g40 = (g39 ^ x0_11)
    g41 = (g40 ^ 1)
    g42 = (g41 ^ 1)
    g43 = (x0_11 | g39)
    g44 = (g43 ^ x0_12)
    g45 = (g44 ^ 1)
    g46 = (g45 ^ 1)
    g47 = (x0_12 | g43)
    g48 = (g47 ^ x0_13)
    g49 = (g48 ^ 1)
    g50 = (g49 ^ 1)
    g51 = (x0_13 | g47)
    g52 = (g51 ^ x0_14)
    g53 = (g52 ^ 1)
    g54 = (g53 ^ 1)
    g55 = (x0_14 | g51)
    g56 = (g55 ^ x0_15)
    g57 = (g56 ^ 1)
    g58 = (g57 ^ 1)
    g59 = (x0_15 | g55)
    g60 = (g59 ^ x0_16)
    g61 = (g60 ^ 1)
    g62 = (g61 ^ 1)
    g63 = (x0_16 | g59)
    g64 = (g63 ^ x0_17)
    g65 = (g64 ^ 1)
    g66 = (g65 ^ 1)
    g67 = (x0_17 | g63)
    g68 = (g67 ^ x0_18)
    g69 = (g68 ^ 1)
    g70 = (g69 ^ 1)
    g71 = (x0_18 | g67)
    g72 = (g71 ^ x0_19)
    g73 = (g72 ^ 1)
    g74 = (g73 ^ 1)
    g75 = (x0_19 | g71)
    g76 = (g75 ^ x0_20)
    g77 = (g76 ^ 1)
    g78 = (g77 ^ 1)
    g79 = (x0_20 | g75)
    g80 = (g79 ^ x0_21)
    g81 = (g80 ^ 1)
    g82 = (g81 ^ 1)
    g83 = (x0_21 | g79)
    g84 = (g83 ^ x0_22)
    g85 = (g84 ^ 1)
    g86 = (g85 ^ 1)
    g87 = (x0_22 | g83)
    g88 = (g87 ^ x0_23)
    g89 = (g88 ^ 1)
    g90 = (g89 ^ 1)
    g91 = (x0_23 | g87)
    g92 = (g91 ^ x0_24)
    g93 = (g92 ^ 1)
    g94 = (g93 ^ 1)
    g95 = (x0_24 | g91)
    g96 = (g95 ^ x0_25)
    g97 = (g96 ^ 1)
    g98 = (g97 ^ 1)
    g99 = (x0_25 | g95)
    g100 = (g99 ^ x0_26)
    g101 = (g100 ^ 1)
    g102 = (g101 ^ 1)
    g103 = (x0_26 | g99)
    g104 = (g103 ^ x0_27)
    g105 = (g104 ^ 1)
    g106 = (g105 ^ 1)
    g107 = (x0_27 | g103)
    g108 = (g107 ^ x0_28)
    g109 = (g108 ^ 1)
    g110 = (g109 ^ 1)
    g111 = (x0_28 | g107)
    g112 = (g111 ^ x0_29)
    g113 = (g112 ^ 1)
    g114 = (g113 ^ 1)
    g115 = (x0_29 | g111)
    g116 = (g115 ^ x0_30)
    g117 = (g116 ^ 1)
    g118 = (g117 ^ 1)
    g119 = (x0_30 | g115)
    g120 = (g119 ^ x0_31)
    g121 = (g120 ^ 1)
    g122 = (g121 ^ 1)
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
    w32 = cat(w31, g122, 1)
    w33 = cat(w32, g118, 1)
    w34 = cat(w33, g114, 1)
    w35 = cat(w34, g110, 1)
    w36 = cat(w35, g106, 1)
    w37 = cat(w36, g102, 1)
    w38 = cat(w37, g98, 1)
    w39 = cat(w38, g94, 1)
    w40 = cat(w39, g90, 1)
    w41 = cat(w40, g86, 1)
    w42 = cat(w41, g82, 1)
    w43 = cat(w42, g78, 1)
    w44 = cat(w43, g74, 1)
    w45 = cat(w44, g70, 1)
    w46 = cat(w45, g66, 1)
    w47 = cat(w46, g62, 1)
    w48 = cat(w47, g58, 1)
    w49 = cat(w48, g54, 1)
    w50 = cat(w49, g50, 1)
    w51 = cat(w50, g46, 1)
    w52 = cat(w51, g42, 1)
    w53 = cat(w52, g38, 1)
    w54 = cat(w53, g34, 1)
    w55 = cat(w54, g30, 1)
    w56 = cat(w55, g26, 1)
    w57 = cat(w56, g22, 1)
    w58 = cat(w57, g18, 1)
    w59 = cat(w58, g14, 1)
    w60 = cat(w59, g10, 1)
    w61 = cat(w60, g6, 1)
    w62 = cat(w61, g2, 1)
    w63 = cat(w62, x0_0, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_neg_gpr_one_32__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
