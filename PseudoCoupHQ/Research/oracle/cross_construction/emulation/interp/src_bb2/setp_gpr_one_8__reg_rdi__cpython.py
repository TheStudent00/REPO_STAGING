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
# one named local per gate, over the term of setp_gpr_one_8__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 8, v2), If(Extract(1, 1, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(2, 2, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(3, 3, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(4, 4, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(5, 5, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(6, 6, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(7, 7, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(0, 0, v0) + 1 == Extract(0, 0, v1), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0))
def emu_setp_gpr_one_8__reg_rdi__cpython(a, b, c):
    x1_0 = ext(a, 0, 0)
    x0_0 = ext(b, 0, 0)
    x1_1 = ext(a, 1, 1)
    x0_1 = ext(b, 1, 1)
    x1_2 = ext(a, 2, 2)
    x0_2 = ext(b, 2, 2)
    x1_3 = ext(a, 3, 3)
    x0_3 = ext(b, 3, 3)
    x1_4 = ext(a, 4, 4)
    x0_4 = ext(b, 4, 4)
    x1_5 = ext(a, 5, 5)
    x0_5 = ext(b, 5, 5)
    x1_6 = ext(a, 6, 6)
    x0_6 = ext(b, 6, 6)
    x1_7 = ext(a, 7, 7)
    x0_7 = ext(b, 7, 7)
    x2_8 = ext(c, 8, 8)
    x2_9 = ext(c, 9, 9)
    x2_10 = ext(c, 10, 10)
    x2_11 = ext(c, 11, 11)
    x2_12 = ext(c, 12, 12)
    x2_13 = ext(c, 13, 13)
    x2_14 = ext(c, 14, 14)
    x2_15 = ext(c, 15, 15)
    x2_16 = ext(c, 16, 16)
    x2_17 = ext(c, 17, 17)
    x2_18 = ext(c, 18, 18)
    x2_19 = ext(c, 19, 19)
    x2_20 = ext(c, 20, 20)
    x2_21 = ext(c, 21, 21)
    x2_22 = ext(c, 22, 22)
    x2_23 = ext(c, 23, 23)
    x2_24 = ext(c, 24, 24)
    x2_25 = ext(c, 25, 25)
    x2_26 = ext(c, 26, 26)
    x2_27 = ext(c, 27, 27)
    x2_28 = ext(c, 28, 28)
    x2_29 = ext(c, 29, 29)
    x2_30 = ext(c, 30, 30)
    x2_31 = ext(c, 31, 31)
    x2_32 = ext(c, 32, 32)
    x2_33 = ext(c, 33, 33)
    x2_34 = ext(c, 34, 34)
    x2_35 = ext(c, 35, 35)
    x2_36 = ext(c, 36, 36)
    x2_37 = ext(c, 37, 37)
    x2_38 = ext(c, 38, 38)
    x2_39 = ext(c, 39, 39)
    x2_40 = ext(c, 40, 40)
    x2_41 = ext(c, 41, 41)
    x2_42 = ext(c, 42, 42)
    x2_43 = ext(c, 43, 43)
    x2_44 = ext(c, 44, 44)
    x2_45 = ext(c, 45, 45)
    x2_46 = ext(c, 46, 46)
    x2_47 = ext(c, 47, 47)
    x2_48 = ext(c, 48, 48)
    x2_49 = ext(c, 49, 49)
    x2_50 = ext(c, 50, 50)
    x2_51 = ext(c, 51, 51)
    x2_52 = ext(c, 52, 52)
    x2_53 = ext(c, 53, 53)
    x2_54 = ext(c, 54, 54)
    x2_55 = ext(c, 55, 55)
    x2_56 = ext(c, 56, 56)
    x2_57 = ext(c, 57, 57)
    x2_58 = ext(c, 58, 58)
    x2_59 = ext(c, 59, 59)
    x2_60 = ext(c, 60, 60)
    x2_61 = ext(c, 61, 61)
    x2_62 = ext(c, 62, 62)
    x2_63 = ext(c, 63, 63)
    g0 = (x1_0 ^ 1)
    g1 = (x0_0 ^ 1)
    g2 = (g1 | g0)
    g3 = (x1_1 ^ 1)
    g4 = (g3 | g2)
    g5 = (g4 ^ 1)
    g6 = (x0_1 ^ 1)
    g7 = (g6 | g2)
    g8 = (g7 ^ 1)
    g9 = (g6 | g3)
    g10 = (g9 ^ 1)
    g11 = (g10 | g8)
    g12 = (g11 | g5)
    g13 = (x1_2 ^ g12)
    g14 = (g13 ^ 1)
    g15 = (x0_2 ^ g14)
    g16 = (g15 ^ 1)
    g17 = (g12 ^ 1)
    g18 = (x1_2 ^ 1)
    g19 = (g18 | g17)
    g20 = (g19 ^ 1)
    g21 = (x0_2 ^ 1)
    g22 = (g21 | g17)
    g23 = (g22 ^ 1)
    g24 = (g21 | g18)
    g25 = (g24 ^ 1)
    g26 = (g25 | g23)
    g27 = (g26 | g20)
    g28 = (x1_3 ^ g27)
    g29 = (g28 ^ 1)
    g30 = (x0_3 ^ g29)
    g31 = (g30 ^ 1)
    g32 = (g27 ^ 1)
    g33 = (x1_3 ^ 1)
    g34 = (g33 | g32)
    g35 = (g34 ^ 1)
    g36 = (x0_3 ^ 1)
    g37 = (g36 | g32)
    g38 = (g37 ^ 1)
    g39 = (g36 | g33)
    g40 = (g39 ^ 1)
    g41 = (g40 | g38)
    g42 = (g41 | g35)
    g43 = (x1_4 ^ g42)
    g44 = (g43 ^ 1)
    g45 = (x0_4 ^ g44)
    g46 = (g45 ^ 1)
    g47 = (g42 ^ 1)
    g48 = (x1_4 ^ 1)
    g49 = (g48 | g47)
    g50 = (g49 ^ 1)
    g51 = (x0_4 ^ 1)
    g52 = (g51 | g47)
    g53 = (g52 ^ 1)
    g54 = (g51 | g48)
    g55 = (g54 ^ 1)
    g56 = (g55 | g53)
    g57 = (g56 | g50)
    g58 = (x1_5 ^ g57)
    g59 = (g58 ^ 1)
    g60 = (x0_5 ^ g59)
    g61 = (g60 ^ 1)
    g62 = (g57 ^ 1)
    g63 = (x1_5 ^ 1)
    g64 = (g63 | g62)
    g65 = (g64 ^ 1)
    g66 = (x0_5 ^ 1)
    g67 = (g66 | g62)
    g68 = (g67 ^ 1)
    g69 = (g66 | g63)
    g70 = (g69 ^ 1)
    g71 = (g70 | g68)
    g72 = (g71 | g65)
    g73 = (x1_6 ^ g72)
    g74 = (g73 ^ 1)
    g75 = (x0_6 ^ g74)
    g76 = (g75 ^ 1)
    g77 = (g72 ^ 1)
    g78 = (x1_6 ^ 1)
    g79 = (g78 | g77)
    g80 = (g79 ^ 1)
    g81 = (x0_6 ^ 1)
    g82 = (g81 | g77)
    g83 = (g82 ^ 1)
    g84 = (g81 | g78)
    g85 = (g84 ^ 1)
    g86 = (g85 | g83)
    g87 = (g86 | g80)
    g88 = (x1_7 ^ g87)
    g89 = (g88 ^ 1)
    g90 = (x0_7 ^ g89)
    g91 = (g90 ^ 1)
    g92 = (x1_0 ^ x0_0)
    g93 = (g92 ^ 1)
    g94 = (g93 ^ g91)
    g95 = (g94 ^ 1)
    g96 = (g95 ^ g76)
    g97 = (g96 ^ 1)
    g98 = (g97 ^ g61)
    g99 = (g98 ^ 1)
    g100 = (g99 ^ g46)
    g101 = (g100 ^ 1)
    g102 = (g101 ^ g31)
    g103 = (g102 ^ 1)
    g104 = (g103 ^ g16)
    g105 = (g104 ^ 1)
    g106 = (x1_1 ^ g2)
    g107 = (g106 ^ 1)
    g108 = (x0_1 ^ g107)
    g109 = (g108 ^ 1)
    g110 = (g109 ^ g105)
    g111 = (g110 ^ 1)
    k0 = 0
    w0 = x2_63
    w1 = cat(w0, x2_62, 1)
    w2 = cat(w1, x2_61, 1)
    w3 = cat(w2, x2_60, 1)
    w4 = cat(w3, x2_59, 1)
    w5 = cat(w4, x2_58, 1)
    w6 = cat(w5, x2_57, 1)
    w7 = cat(w6, x2_56, 1)
    w8 = cat(w7, x2_55, 1)
    w9 = cat(w8, x2_54, 1)
    w10 = cat(w9, x2_53, 1)
    w11 = cat(w10, x2_52, 1)
    w12 = cat(w11, x2_51, 1)
    w13 = cat(w12, x2_50, 1)
    w14 = cat(w13, x2_49, 1)
    w15 = cat(w14, x2_48, 1)
    w16 = cat(w15, x2_47, 1)
    w17 = cat(w16, x2_46, 1)
    w18 = cat(w17, x2_45, 1)
    w19 = cat(w18, x2_44, 1)
    w20 = cat(w19, x2_43, 1)
    w21 = cat(w20, x2_42, 1)
    w22 = cat(w21, x2_41, 1)
    w23 = cat(w22, x2_40, 1)
    w24 = cat(w23, x2_39, 1)
    w25 = cat(w24, x2_38, 1)
    w26 = cat(w25, x2_37, 1)
    w27 = cat(w26, x2_36, 1)
    w28 = cat(w27, x2_35, 1)
    w29 = cat(w28, x2_34, 1)
    w30 = cat(w29, x2_33, 1)
    w31 = cat(w30, x2_32, 1)
    w32 = cat(w31, x2_31, 1)
    w33 = cat(w32, x2_30, 1)
    w34 = cat(w33, x2_29, 1)
    w35 = cat(w34, x2_28, 1)
    w36 = cat(w35, x2_27, 1)
    w37 = cat(w36, x2_26, 1)
    w38 = cat(w37, x2_25, 1)
    w39 = cat(w38, x2_24, 1)
    w40 = cat(w39, x2_23, 1)
    w41 = cat(w40, x2_22, 1)
    w42 = cat(w41, x2_21, 1)
    w43 = cat(w42, x2_20, 1)
    w44 = cat(w43, x2_19, 1)
    w45 = cat(w44, x2_18, 1)
    w46 = cat(w45, x2_17, 1)
    w47 = cat(w46, x2_16, 1)
    w48 = cat(w47, x2_15, 1)
    w49 = cat(w48, x2_14, 1)
    w50 = cat(w49, x2_13, 1)
    w51 = cat(w50, x2_12, 1)
    w52 = cat(w51, x2_11, 1)
    w53 = cat(w52, x2_10, 1)
    w54 = cat(w53, x2_9, 1)
    w55 = cat(w54, x2_8, 1)
    w56 = cat(w55, k0, 1)
    w57 = cat(w56, k0, 1)
    w58 = cat(w57, k0, 1)
    w59 = cat(w58, k0, 1)
    w60 = cat(w59, k0, 1)
    w61 = cat(w60, k0, 1)
    w62 = cat(w61, k0, 1)
    w63 = cat(w62, g111, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_setp_gpr_one_8__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
