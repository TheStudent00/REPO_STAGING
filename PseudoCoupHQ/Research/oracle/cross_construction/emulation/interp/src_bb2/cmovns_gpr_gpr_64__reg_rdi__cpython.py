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
# one named local per gate, over the term of cmovns_gpr_gpr_64__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
def emu_cmovns_gpr_gpr_64__reg_rdi__cpython(a, b, c, d):
    x3_0 = ext(d, 0, 0)
    x1_63 = ext(a, 63, 63)
    x0_63 = ext(b, 63, 63)
    x2_0 = ext(c, 0, 0)
    x3_1 = ext(d, 1, 1)
    x2_1 = ext(c, 1, 1)
    x3_2 = ext(d, 2, 2)
    x2_2 = ext(c, 2, 2)
    x3_3 = ext(d, 3, 3)
    x2_3 = ext(c, 3, 3)
    x3_4 = ext(d, 4, 4)
    x2_4 = ext(c, 4, 4)
    x3_5 = ext(d, 5, 5)
    x2_5 = ext(c, 5, 5)
    x3_6 = ext(d, 6, 6)
    x2_6 = ext(c, 6, 6)
    x3_7 = ext(d, 7, 7)
    x2_7 = ext(c, 7, 7)
    x3_8 = ext(d, 8, 8)
    x2_8 = ext(c, 8, 8)
    x3_9 = ext(d, 9, 9)
    x2_9 = ext(c, 9, 9)
    x3_10 = ext(d, 10, 10)
    x2_10 = ext(c, 10, 10)
    x3_11 = ext(d, 11, 11)
    x2_11 = ext(c, 11, 11)
    x3_12 = ext(d, 12, 12)
    x2_12 = ext(c, 12, 12)
    x3_13 = ext(d, 13, 13)
    x2_13 = ext(c, 13, 13)
    x3_14 = ext(d, 14, 14)
    x2_14 = ext(c, 14, 14)
    x3_15 = ext(d, 15, 15)
    x2_15 = ext(c, 15, 15)
    x3_16 = ext(d, 16, 16)
    x2_16 = ext(c, 16, 16)
    x3_17 = ext(d, 17, 17)
    x2_17 = ext(c, 17, 17)
    x3_18 = ext(d, 18, 18)
    x2_18 = ext(c, 18, 18)
    x3_19 = ext(d, 19, 19)
    x2_19 = ext(c, 19, 19)
    x3_20 = ext(d, 20, 20)
    x2_20 = ext(c, 20, 20)
    x3_21 = ext(d, 21, 21)
    x2_21 = ext(c, 21, 21)
    x3_22 = ext(d, 22, 22)
    x2_22 = ext(c, 22, 22)
    x3_23 = ext(d, 23, 23)
    x2_23 = ext(c, 23, 23)
    x3_24 = ext(d, 24, 24)
    x2_24 = ext(c, 24, 24)
    x3_25 = ext(d, 25, 25)
    x2_25 = ext(c, 25, 25)
    x3_26 = ext(d, 26, 26)
    x2_26 = ext(c, 26, 26)
    x3_27 = ext(d, 27, 27)
    x2_27 = ext(c, 27, 27)
    x3_28 = ext(d, 28, 28)
    x2_28 = ext(c, 28, 28)
    x3_29 = ext(d, 29, 29)
    x2_29 = ext(c, 29, 29)
    x3_30 = ext(d, 30, 30)
    x2_30 = ext(c, 30, 30)
    x3_31 = ext(d, 31, 31)
    x2_31 = ext(c, 31, 31)
    x3_32 = ext(d, 32, 32)
    x2_32 = ext(c, 32, 32)
    x3_33 = ext(d, 33, 33)
    x2_33 = ext(c, 33, 33)
    x3_34 = ext(d, 34, 34)
    x2_34 = ext(c, 34, 34)
    x3_35 = ext(d, 35, 35)
    x2_35 = ext(c, 35, 35)
    x3_36 = ext(d, 36, 36)
    x2_36 = ext(c, 36, 36)
    x3_37 = ext(d, 37, 37)
    x2_37 = ext(c, 37, 37)
    x3_38 = ext(d, 38, 38)
    x2_38 = ext(c, 38, 38)
    x3_39 = ext(d, 39, 39)
    x2_39 = ext(c, 39, 39)
    x3_40 = ext(d, 40, 40)
    x2_40 = ext(c, 40, 40)
    x3_41 = ext(d, 41, 41)
    x2_41 = ext(c, 41, 41)
    x3_42 = ext(d, 42, 42)
    x2_42 = ext(c, 42, 42)
    x3_43 = ext(d, 43, 43)
    x2_43 = ext(c, 43, 43)
    x3_44 = ext(d, 44, 44)
    x2_44 = ext(c, 44, 44)
    x3_45 = ext(d, 45, 45)
    x2_45 = ext(c, 45, 45)
    x3_46 = ext(d, 46, 46)
    x2_46 = ext(c, 46, 46)
    x3_47 = ext(d, 47, 47)
    x2_47 = ext(c, 47, 47)
    x3_48 = ext(d, 48, 48)
    x2_48 = ext(c, 48, 48)
    x3_49 = ext(d, 49, 49)
    x2_49 = ext(c, 49, 49)
    x3_50 = ext(d, 50, 50)
    x2_50 = ext(c, 50, 50)
    x3_51 = ext(d, 51, 51)
    x2_51 = ext(c, 51, 51)
    x3_52 = ext(d, 52, 52)
    x2_52 = ext(c, 52, 52)
    x3_53 = ext(d, 53, 53)
    x2_53 = ext(c, 53, 53)
    x3_54 = ext(d, 54, 54)
    x2_54 = ext(c, 54, 54)
    x3_55 = ext(d, 55, 55)
    x2_55 = ext(c, 55, 55)
    x3_56 = ext(d, 56, 56)
    x2_56 = ext(c, 56, 56)
    x3_57 = ext(d, 57, 57)
    x2_57 = ext(c, 57, 57)
    x3_58 = ext(d, 58, 58)
    x2_58 = ext(c, 58, 58)
    x3_59 = ext(d, 59, 59)
    x2_59 = ext(c, 59, 59)
    x3_60 = ext(d, 60, 60)
    x2_60 = ext(c, 60, 60)
    x3_61 = ext(d, 61, 61)
    x2_61 = ext(c, 61, 61)
    x3_62 = ext(d, 62, 62)
    x2_62 = ext(c, 62, 62)
    x3_63 = ext(d, 63, 63)
    x2_63 = ext(c, 63, 63)
    g0 = (x1_63 ^ 1)
    g1 = (x0_63 ^ 1)
    g2 = (g1 | g0)
    g3 = (g2 ^ 1)
    g4 = (g3 & x3_0)
    g5 = (g2 & x2_0)
    g6 = (g5 | g4)
    g7 = (g3 & x3_1)
    g8 = (g2 & x2_1)
    g9 = (g8 | g7)
    g10 = (g3 & x3_2)
    g11 = (g2 & x2_2)
    g12 = (g11 | g10)
    g13 = (g3 & x3_3)
    g14 = (g2 & x2_3)
    g15 = (g14 | g13)
    g16 = (g3 & x3_4)
    g17 = (g2 & x2_4)
    g18 = (g17 | g16)
    g19 = (g3 & x3_5)
    g20 = (g2 & x2_5)
    g21 = (g20 | g19)
    g22 = (g3 & x3_6)
    g23 = (g2 & x2_6)
    g24 = (g23 | g22)
    g25 = (g3 & x3_7)
    g26 = (g2 & x2_7)
    g27 = (g26 | g25)
    g28 = (g3 & x3_8)
    g29 = (g2 & x2_8)
    g30 = (g29 | g28)
    g31 = (g3 & x3_9)
    g32 = (g2 & x2_9)
    g33 = (g32 | g31)
    g34 = (g3 & x3_10)
    g35 = (g2 & x2_10)
    g36 = (g35 | g34)
    g37 = (g3 & x3_11)
    g38 = (g2 & x2_11)
    g39 = (g38 | g37)
    g40 = (g3 & x3_12)
    g41 = (g2 & x2_12)
    g42 = (g41 | g40)
    g43 = (g3 & x3_13)
    g44 = (g2 & x2_13)
    g45 = (g44 | g43)
    g46 = (g3 & x3_14)
    g47 = (g2 & x2_14)
    g48 = (g47 | g46)
    g49 = (g3 & x3_15)
    g50 = (g2 & x2_15)
    g51 = (g50 | g49)
    g52 = (g3 & x3_16)
    g53 = (g2 & x2_16)
    g54 = (g53 | g52)
    g55 = (g3 & x3_17)
    g56 = (g2 & x2_17)
    g57 = (g56 | g55)
    g58 = (g3 & x3_18)
    g59 = (g2 & x2_18)
    g60 = (g59 | g58)
    g61 = (g3 & x3_19)
    g62 = (g2 & x2_19)
    g63 = (g62 | g61)
    g64 = (g3 & x3_20)
    g65 = (g2 & x2_20)
    g66 = (g65 | g64)
    g67 = (g3 & x3_21)
    g68 = (g2 & x2_21)
    g69 = (g68 | g67)
    g70 = (g3 & x3_22)
    g71 = (g2 & x2_22)
    g72 = (g71 | g70)
    g73 = (g3 & x3_23)
    g74 = (g2 & x2_23)
    g75 = (g74 | g73)
    g76 = (g3 & x3_24)
    g77 = (g2 & x2_24)
    g78 = (g77 | g76)
    g79 = (g3 & x3_25)
    g80 = (g2 & x2_25)
    g81 = (g80 | g79)
    g82 = (g3 & x3_26)
    g83 = (g2 & x2_26)
    g84 = (g83 | g82)
    g85 = (g3 & x3_27)
    g86 = (g2 & x2_27)
    g87 = (g86 | g85)
    g88 = (g3 & x3_28)
    g89 = (g2 & x2_28)
    g90 = (g89 | g88)
    g91 = (g3 & x3_29)
    g92 = (g2 & x2_29)
    g93 = (g92 | g91)
    g94 = (g3 & x3_30)
    g95 = (g2 & x2_30)
    g96 = (g95 | g94)
    g97 = (g3 & x3_31)
    g98 = (g2 & x2_31)
    g99 = (g98 | g97)
    g100 = (g3 & x3_32)
    g101 = (g2 & x2_32)
    g102 = (g101 | g100)
    g103 = (g3 & x3_33)
    g104 = (g2 & x2_33)
    g105 = (g104 | g103)
    g106 = (g3 & x3_34)
    g107 = (g2 & x2_34)
    g108 = (g107 | g106)
    g109 = (g3 & x3_35)
    g110 = (g2 & x2_35)
    g111 = (g110 | g109)
    g112 = (g3 & x3_36)
    g113 = (g2 & x2_36)
    g114 = (g113 | g112)
    g115 = (g3 & x3_37)
    g116 = (g2 & x2_37)
    g117 = (g116 | g115)
    g118 = (g3 & x3_38)
    g119 = (g2 & x2_38)
    g120 = (g119 | g118)
    g121 = (g3 & x3_39)
    g122 = (g2 & x2_39)
    g123 = (g122 | g121)
    g124 = (g3 & x3_40)
    g125 = (g2 & x2_40)
    g126 = (g125 | g124)
    g127 = (g3 & x3_41)
    g128 = (g2 & x2_41)
    g129 = (g128 | g127)
    g130 = (g3 & x3_42)
    g131 = (g2 & x2_42)
    g132 = (g131 | g130)
    g133 = (g3 & x3_43)
    g134 = (g2 & x2_43)
    g135 = (g134 | g133)
    g136 = (g3 & x3_44)
    g137 = (g2 & x2_44)
    g138 = (g137 | g136)
    g139 = (g3 & x3_45)
    g140 = (g2 & x2_45)
    g141 = (g140 | g139)
    g142 = (g3 & x3_46)
    g143 = (g2 & x2_46)
    g144 = (g143 | g142)
    g145 = (g3 & x3_47)
    g146 = (g2 & x2_47)
    g147 = (g146 | g145)
    g148 = (g3 & x3_48)
    g149 = (g2 & x2_48)
    g150 = (g149 | g148)
    g151 = (g3 & x3_49)
    g152 = (g2 & x2_49)
    g153 = (g152 | g151)
    g154 = (g3 & x3_50)
    g155 = (g2 & x2_50)
    g156 = (g155 | g154)
    g157 = (g3 & x3_51)
    g158 = (g2 & x2_51)
    g159 = (g158 | g157)
    g160 = (g3 & x3_52)
    g161 = (g2 & x2_52)
    g162 = (g161 | g160)
    g163 = (g3 & x3_53)
    g164 = (g2 & x2_53)
    g165 = (g164 | g163)
    g166 = (g3 & x3_54)
    g167 = (g2 & x2_54)
    g168 = (g167 | g166)
    g169 = (g3 & x3_55)
    g170 = (g2 & x2_55)
    g171 = (g170 | g169)
    g172 = (g3 & x3_56)
    g173 = (g2 & x2_56)
    g174 = (g173 | g172)
    g175 = (g3 & x3_57)
    g176 = (g2 & x2_57)
    g177 = (g176 | g175)
    g178 = (g3 & x3_58)
    g179 = (g2 & x2_58)
    g180 = (g179 | g178)
    g181 = (g3 & x3_59)
    g182 = (g2 & x2_59)
    g183 = (g182 | g181)
    g184 = (g3 & x3_60)
    g185 = (g2 & x2_60)
    g186 = (g185 | g184)
    g187 = (g3 & x3_61)
    g188 = (g2 & x2_61)
    g189 = (g188 | g187)
    g190 = (g3 & x3_62)
    g191 = (g2 & x2_62)
    g192 = (g191 | g190)
    g193 = (g3 & x3_63)
    g194 = (g2 & x2_63)
    g195 = (g194 | g193)
    w0 = g195
    w1 = cat(w0, g192, 1)
    w2 = cat(w1, g189, 1)
    w3 = cat(w2, g186, 1)
    w4 = cat(w3, g183, 1)
    w5 = cat(w4, g180, 1)
    w6 = cat(w5, g177, 1)
    w7 = cat(w6, g174, 1)
    w8 = cat(w7, g171, 1)
    w9 = cat(w8, g168, 1)
    w10 = cat(w9, g165, 1)
    w11 = cat(w10, g162, 1)
    w12 = cat(w11, g159, 1)
    w13 = cat(w12, g156, 1)
    w14 = cat(w13, g153, 1)
    w15 = cat(w14, g150, 1)
    w16 = cat(w15, g147, 1)
    w17 = cat(w16, g144, 1)
    w18 = cat(w17, g141, 1)
    w19 = cat(w18, g138, 1)
    w20 = cat(w19, g135, 1)
    w21 = cat(w20, g132, 1)
    w22 = cat(w21, g129, 1)
    w23 = cat(w22, g126, 1)
    w24 = cat(w23, g123, 1)
    w25 = cat(w24, g120, 1)
    w26 = cat(w25, g117, 1)
    w27 = cat(w26, g114, 1)
    w28 = cat(w27, g111, 1)
    w29 = cat(w28, g108, 1)
    w30 = cat(w29, g105, 1)
    w31 = cat(w30, g102, 1)
    w32 = cat(w31, g99, 1)
    w33 = cat(w32, g96, 1)
    w34 = cat(w33, g93, 1)
    w35 = cat(w34, g90, 1)
    w36 = cat(w35, g87, 1)
    w37 = cat(w36, g84, 1)
    w38 = cat(w37, g81, 1)
    w39 = cat(w38, g78, 1)
    w40 = cat(w39, g75, 1)
    w41 = cat(w40, g72, 1)
    w42 = cat(w41, g69, 1)
    w43 = cat(w42, g66, 1)
    w44 = cat(w43, g63, 1)
    w45 = cat(w44, g60, 1)
    w46 = cat(w45, g57, 1)
    w47 = cat(w46, g54, 1)
    w48 = cat(w47, g51, 1)
    w49 = cat(w48, g48, 1)
    w50 = cat(w49, g45, 1)
    w51 = cat(w50, g42, 1)
    w52 = cat(w51, g39, 1)
    w53 = cat(w52, g36, 1)
    w54 = cat(w53, g33, 1)
    w55 = cat(w54, g30, 1)
    w56 = cat(w55, g27, 1)
    w57 = cat(w56, g24, 1)
    w58 = cat(w57, g21, 1)
    w59 = cat(w58, g18, 1)
    w60 = cat(w59, g15, 1)
    w61 = cat(w60, g12, 1)
    w62 = cat(w61, g9, 1)
    w63 = cat(w62, g6, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_cmovns_gpr_gpr_64__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
