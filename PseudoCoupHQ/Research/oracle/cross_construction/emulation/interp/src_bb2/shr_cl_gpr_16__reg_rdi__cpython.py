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
# one named local per gate, over the term of shr_cl_gpr_16__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 16, v0), LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1))))
def emu_shr_cl_gpr_16__reg_rdi__cpython(a, b):
    x0_0 = ext(a, 0, 0)
    x0_1 = ext(a, 1, 1)
    x1_0 = ext(b, 0, 0)
    x0_2 = ext(a, 2, 2)
    x0_3 = ext(a, 3, 3)
    x1_1 = ext(b, 1, 1)
    x0_4 = ext(a, 4, 4)
    x0_5 = ext(a, 5, 5)
    x0_6 = ext(a, 6, 6)
    x0_7 = ext(a, 7, 7)
    x1_2 = ext(b, 2, 2)
    x0_8 = ext(a, 8, 8)
    x0_9 = ext(a, 9, 9)
    x0_10 = ext(a, 10, 10)
    x0_11 = ext(a, 11, 11)
    x0_12 = ext(a, 12, 12)
    x0_13 = ext(a, 13, 13)
    x0_14 = ext(a, 14, 14)
    x0_15 = ext(a, 15, 15)
    x1_3 = ext(b, 3, 3)
    x1_4 = ext(b, 4, 4)
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
    g1 = (x1_0 & x0_1)
    g2 = (g0 & x0_0)
    g3 = (g1 | g2)
    g4 = (x1_0 ^ 1)
    g5 = (x1_0 & x0_3)
    g6 = (g4 & x0_2)
    g7 = (g5 | g6)
    g8 = (x1_1 ^ 1)
    g9 = (x1_1 & g7)
    g10 = (g8 & g3)
    g11 = (g9 | g10)
    g12 = (x1_0 ^ 1)
    g13 = (x1_0 & x0_5)
    g14 = (g12 & x0_4)
    g15 = (g13 | g14)
    g16 = (x1_0 ^ 1)
    g17 = (x1_0 & x0_7)
    g18 = (g16 & x0_6)
    g19 = (g17 | g18)
    g20 = (x1_1 ^ 1)
    g21 = (x1_1 & g19)
    g22 = (g20 & g15)
    g23 = (g21 | g22)
    g24 = (x1_2 ^ 1)
    g25 = (x1_2 & g23)
    g26 = (g24 & g11)
    g27 = (g25 | g26)
    g28 = (x1_0 ^ 1)
    g29 = (x1_0 & x0_9)
    g30 = (g28 & x0_8)
    g31 = (g29 | g30)
    g32 = (x1_0 ^ 1)
    g33 = (x1_0 & x0_11)
    g34 = (g32 & x0_10)
    g35 = (g33 | g34)
    g36 = (x1_1 ^ 1)
    g37 = (x1_1 & g35)
    g38 = (g36 & g31)
    g39 = (g37 | g38)
    g40 = (x1_0 ^ 1)
    g41 = (x1_0 & x0_13)
    g42 = (g40 & x0_12)
    g43 = (g41 | g42)
    g44 = (x1_0 ^ 1)
    g45 = (x1_0 & x0_15)
    g46 = (g44 & x0_14)
    g47 = (g45 | g46)
    g48 = (x1_1 ^ 1)
    g49 = (x1_1 & g47)
    g50 = (g48 & g43)
    g51 = (g49 | g50)
    g52 = (x1_2 ^ 1)
    g53 = (x1_2 & g51)
    g54 = (g52 & g39)
    g55 = (g53 | g54)
    g56 = (x1_3 ^ 1)
    g57 = (x1_3 & g55)
    g58 = (g56 & g27)
    g59 = (g57 | g58)
    g60 = (x1_4 ^ 1)
    g61 = (g60 & g59)
    g62 = (x1_0 ^ 1)
    g63 = (x1_0 & x0_2)
    g64 = (g62 & x0_1)
    g65 = (g63 | g64)
    g66 = (x1_0 ^ 1)
    g67 = (x1_0 & x0_4)
    g68 = (g66 & x0_3)
    g69 = (g67 | g68)
    g70 = (x1_1 ^ 1)
    g71 = (x1_1 & g69)
    g72 = (g70 & g65)
    g73 = (g71 | g72)
    g74 = (x1_0 ^ 1)
    g75 = (x1_0 & x0_6)
    g76 = (g74 & x0_5)
    g77 = (g75 | g76)
    g78 = (x1_0 ^ 1)
    g79 = (x1_0 & x0_8)
    g80 = (g78 & x0_7)
    g81 = (g79 | g80)
    g82 = (x1_1 ^ 1)
    g83 = (x1_1 & g81)
    g84 = (g82 & g77)
    g85 = (g83 | g84)
    g86 = (x1_2 ^ 1)
    g87 = (x1_2 & g85)
    g88 = (g86 & g73)
    g89 = (g87 | g88)
    g90 = (x1_0 ^ 1)
    g91 = (x1_0 & x0_10)
    g92 = (g90 & x0_9)
    g93 = (g91 | g92)
    g94 = (x1_0 ^ 1)
    g95 = (x1_0 & x0_12)
    g96 = (g94 & x0_11)
    g97 = (g95 | g96)
    g98 = (x1_1 ^ 1)
    g99 = (x1_1 & g97)
    g100 = (g98 & g93)
    g101 = (g99 | g100)
    g102 = (x1_0 ^ 1)
    g103 = (x1_0 & x0_14)
    g104 = (g102 & x0_13)
    g105 = (g103 | g104)
    g106 = (x0_15 ^ 1)
    g107 = (x1_0 | g106)
    g108 = (g107 ^ 1)
    g109 = (x1_1 ^ 1)
    g110 = (x1_1 & g108)
    g111 = (g109 & g105)
    g112 = (g110 | g111)
    g113 = (x1_2 ^ 1)
    g114 = (x1_2 & g112)
    g115 = (g113 & g101)
    g116 = (g114 | g115)
    g117 = (x1_3 ^ 1)
    g118 = (x1_3 & g116)
    g119 = (g117 & g89)
    g120 = (g118 | g119)
    g121 = (g60 & g120)
    g122 = (x1_1 ^ 1)
    g123 = (x1_1 & g15)
    g124 = (g122 & g7)
    g125 = (g123 | g124)
    g126 = (x1_1 ^ 1)
    g127 = (x1_1 & g31)
    g128 = (g126 & g19)
    g129 = (g127 | g128)
    g130 = (x1_2 ^ 1)
    g131 = (x1_2 & g129)
    g132 = (g130 & g125)
    g133 = (g131 | g132)
    g134 = (x1_1 ^ 1)
    g135 = (x1_1 & g43)
    g136 = (g134 & g35)
    g137 = (g135 | g136)
    g138 = (g47 ^ 1)
    g139 = (x1_1 | g138)
    g140 = (g139 ^ 1)
    g141 = (x1_2 ^ 1)
    g142 = (x1_2 & g140)
    g143 = (g141 & g137)
    g144 = (g142 | g143)
    g145 = (x1_3 ^ 1)
    g146 = (x1_3 & g144)
    g147 = (g145 & g133)
    g148 = (g146 | g147)
    g149 = (g60 & g148)
    g150 = (x1_1 ^ 1)
    g151 = (x1_1 & g77)
    g152 = (g150 & g69)
    g153 = (g151 | g152)
    g154 = (x1_1 ^ 1)
    g155 = (x1_1 & g93)
    g156 = (g154 & g81)
    g157 = (g155 | g156)
    g158 = (x1_2 ^ 1)
    g159 = (x1_2 & g157)
    g160 = (g158 & g153)
    g161 = (g159 | g160)
    g162 = (x1_1 ^ 1)
    g163 = (x1_1 & g105)
    g164 = (g162 & g97)
    g165 = (g163 | g164)
    g166 = (x1_1 | g107)
    g167 = (g166 ^ 1)
    g168 = (x1_2 ^ 1)
    g169 = (x1_2 & g167)
    g170 = (g168 & g165)
    g171 = (g169 | g170)
    g172 = (x1_3 ^ 1)
    g173 = (x1_3 & g171)
    g174 = (g172 & g161)
    g175 = (g173 | g174)
    g176 = (g60 & g175)
    g177 = (x1_2 ^ 1)
    g178 = (x1_2 & g39)
    g179 = (g177 & g23)
    g180 = (g178 | g179)
    g181 = (g51 ^ 1)
    g182 = (x1_2 | g181)
    g183 = (g182 ^ 1)
    g184 = (x1_3 ^ 1)
    g185 = (x1_3 & g183)
    g186 = (g184 & g180)
    g187 = (g185 | g186)
    g188 = (g60 & g187)
    g189 = (x1_2 ^ 1)
    g190 = (x1_2 & g101)
    g191 = (g189 & g85)
    g192 = (g190 | g191)
    g193 = (g112 ^ 1)
    g194 = (x1_2 | g193)
    g195 = (g194 ^ 1)
    g196 = (x1_3 ^ 1)
    g197 = (x1_3 & g195)
    g198 = (g196 & g192)
    g199 = (g197 | g198)
    g200 = (g60 & g199)
    g201 = (x1_2 ^ 1)
    g202 = (x1_2 & g137)
    g203 = (g201 & g129)
    g204 = (g202 | g203)
    g205 = (x1_2 | g139)
    g206 = (g205 ^ 1)
    g207 = (x1_3 ^ 1)
    g208 = (x1_3 & g206)
    g209 = (g207 & g204)
    g210 = (g208 | g209)
    g211 = (g60 & g210)
    g212 = (x1_2 ^ 1)
    g213 = (x1_2 & g165)
    g214 = (g212 & g157)
    g215 = (g213 | g214)
    g216 = (x1_2 | g166)
    g217 = (g216 ^ 1)
    g218 = (x1_3 ^ 1)
    g219 = (x1_3 & g217)
    g220 = (g218 & g215)
    g221 = (g219 | g220)
    g222 = (g60 & g221)
    g223 = (x1_3 ^ 1)
    g224 = (g60 & g223)
    g225 = (g224 & g55)
    g226 = (g60 & g223)
    g227 = (g226 & g116)
    g228 = (g60 & g223)
    g229 = (g228 & g144)
    g230 = (g60 & g223)
    g231 = (g230 & g171)
    g232 = (x1_2 ^ 1)
    g233 = (g60 & g223)
    g234 = (g233 & g232)
    g235 = (g234 & g51)
    g236 = (g60 & g223)
    g237 = (g236 & g232)
    g238 = (g237 & g112)
    g239 = (x1_1 ^ 1)
    g240 = (g60 & g223)
    g241 = (g240 & g232)
    g242 = (g241 & g239)
    g243 = (g242 & g47)
    g244 = (x1_0 ^ 1)
    g245 = (g60 & g223)
    g246 = (g245 & g232)
    g247 = (g246 & g239)
    g248 = (g247 & g244)
    g249 = (g248 & x0_15)
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
    w48 = cat(w47, g249, 1)
    w49 = cat(w48, g243, 1)
    w50 = cat(w49, g238, 1)
    w51 = cat(w50, g235, 1)
    w52 = cat(w51, g231, 1)
    w53 = cat(w52, g229, 1)
    w54 = cat(w53, g227, 1)
    w55 = cat(w54, g225, 1)
    w56 = cat(w55, g222, 1)
    w57 = cat(w56, g211, 1)
    w58 = cat(w57, g200, 1)
    w59 = cat(w58, g188, 1)
    w60 = cat(w59, g176, 1)
    w61 = cat(w60, g149, 1)
    w62 = cat(w61, g121, 1)
    w63 = cat(w62, g61, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_shr_cl_gpr_16__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
