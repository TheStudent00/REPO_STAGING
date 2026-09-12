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
# one named local per gate, over the term of sar_cl_gpr_16__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 16, v0), Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1)))
def emu_sar_cl_gpr_16__reg_rdi__cpython(a, b):
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
    g61 = (x1_4 & x0_15)
    g62 = (g60 & g59)
    g63 = (g61 | g62)
    g64 = (x1_0 ^ 1)
    g65 = (x1_0 & x0_2)
    g66 = (g64 & x0_1)
    g67 = (g65 | g66)
    g68 = (x1_0 ^ 1)
    g69 = (x1_0 & x0_4)
    g70 = (g68 & x0_3)
    g71 = (g69 | g70)
    g72 = (x1_1 ^ 1)
    g73 = (x1_1 & g71)
    g74 = (g72 & g67)
    g75 = (g73 | g74)
    g76 = (x1_0 ^ 1)
    g77 = (x1_0 & x0_6)
    g78 = (g76 & x0_5)
    g79 = (g77 | g78)
    g80 = (x1_0 ^ 1)
    g81 = (x1_0 & x0_8)
    g82 = (g80 & x0_7)
    g83 = (g81 | g82)
    g84 = (x1_1 ^ 1)
    g85 = (x1_1 & g83)
    g86 = (g84 & g79)
    g87 = (g85 | g86)
    g88 = (x1_2 ^ 1)
    g89 = (x1_2 & g87)
    g90 = (g88 & g75)
    g91 = (g89 | g90)
    g92 = (x1_0 ^ 1)
    g93 = (x1_0 & x0_10)
    g94 = (g92 & x0_9)
    g95 = (g93 | g94)
    g96 = (x1_0 ^ 1)
    g97 = (x1_0 & x0_12)
    g98 = (g96 & x0_11)
    g99 = (g97 | g98)
    g100 = (x1_1 ^ 1)
    g101 = (x1_1 & g99)
    g102 = (g100 & g95)
    g103 = (g101 | g102)
    g104 = (x1_0 ^ 1)
    g105 = (x1_0 & x0_14)
    g106 = (g104 & x0_13)
    g107 = (g105 | g106)
    g108 = (x1_1 ^ 1)
    g109 = (x1_1 & x0_15)
    g110 = (g108 & g107)
    g111 = (g109 | g110)
    g112 = (x1_2 ^ 1)
    g113 = (x1_2 & g111)
    g114 = (g112 & g103)
    g115 = (g113 | g114)
    g116 = (x1_3 ^ 1)
    g117 = (x1_3 & g115)
    g118 = (g116 & g91)
    g119 = (g117 | g118)
    g120 = (x1_4 ^ 1)
    g121 = (x1_4 & x0_15)
    g122 = (g120 & g119)
    g123 = (g121 | g122)
    g124 = (x1_1 ^ 1)
    g125 = (x1_1 & g15)
    g126 = (g124 & g7)
    g127 = (g125 | g126)
    g128 = (x1_1 ^ 1)
    g129 = (x1_1 & g31)
    g130 = (g128 & g19)
    g131 = (g129 | g130)
    g132 = (x1_2 ^ 1)
    g133 = (x1_2 & g131)
    g134 = (g132 & g127)
    g135 = (g133 | g134)
    g136 = (x1_1 ^ 1)
    g137 = (x1_1 & g43)
    g138 = (g136 & g35)
    g139 = (g137 | g138)
    g140 = (x1_1 | x1_0)
    g141 = (g140 ^ 1)
    g142 = (g140 & x0_15)
    g143 = (g141 & x0_14)
    g144 = (g142 | g143)
    g145 = (x1_2 ^ 1)
    g146 = (x1_2 & g144)
    g147 = (g145 & g139)
    g148 = (g146 | g147)
    g149 = (x1_3 ^ 1)
    g150 = (x1_3 & g148)
    g151 = (g149 & g135)
    g152 = (g150 | g151)
    g153 = (x1_4 ^ 1)
    g154 = (x1_4 & x0_15)
    g155 = (g153 & g152)
    g156 = (g154 | g155)
    g157 = (x1_1 ^ 1)
    g158 = (x1_1 & g79)
    g159 = (g157 & g71)
    g160 = (g158 | g159)
    g161 = (x1_1 ^ 1)
    g162 = (x1_1 & g95)
    g163 = (g161 & g83)
    g164 = (g162 | g163)
    g165 = (x1_2 ^ 1)
    g166 = (x1_2 & g164)
    g167 = (g165 & g160)
    g168 = (g166 | g167)
    g169 = (x1_1 ^ 1)
    g170 = (x1_1 & g107)
    g171 = (g169 & g99)
    g172 = (g170 | g171)
    g173 = (x1_2 ^ 1)
    g174 = (x1_2 & x0_15)
    g175 = (g173 & g172)
    g176 = (g174 | g175)
    g177 = (x1_3 ^ 1)
    g178 = (x1_3 & g176)
    g179 = (g177 & g168)
    g180 = (g178 | g179)
    g181 = (x1_4 ^ 1)
    g182 = (x1_4 & x0_15)
    g183 = (g181 & g180)
    g184 = (g182 | g183)
    g185 = (x1_2 ^ 1)
    g186 = (x1_2 & g39)
    g187 = (g185 & g23)
    g188 = (g186 | g187)
    g189 = (x1_2 ^ 1)
    g190 = (x1_2 & x0_15)
    g191 = (g189 & g51)
    g192 = (g190 | g191)
    g193 = (x1_3 ^ 1)
    g194 = (x1_3 & g192)
    g195 = (g193 & g188)
    g196 = (g194 | g195)
    g197 = (x1_4 ^ 1)
    g198 = (x1_4 & x0_15)
    g199 = (g197 & g196)
    g200 = (g198 | g199)
    g201 = (x1_2 ^ 1)
    g202 = (x1_2 & g103)
    g203 = (g201 & g87)
    g204 = (g202 | g203)
    g205 = (x1_2 | x1_1)
    g206 = (g205 ^ 1)
    g207 = (g205 & x0_15)
    g208 = (g206 & g107)
    g209 = (g207 | g208)
    g210 = (x1_3 ^ 1)
    g211 = (x1_3 & g209)
    g212 = (g210 & g204)
    g213 = (g211 | g212)
    g214 = (x1_4 ^ 1)
    g215 = (x1_4 & x0_15)
    g216 = (g214 & g213)
    g217 = (g215 | g216)
    g218 = (x1_2 ^ 1)
    g219 = (x1_2 & g139)
    g220 = (g218 & g131)
    g221 = (g219 | g220)
    g222 = (x1_2 | g140)
    g223 = (g222 ^ 1)
    g224 = (g222 & x0_15)
    g225 = (g223 & x0_14)
    g226 = (g224 | g225)
    g227 = (x1_3 ^ 1)
    g228 = (x1_3 & g226)
    g229 = (g227 & g221)
    g230 = (g228 | g229)
    g231 = (x1_4 ^ 1)
    g232 = (x1_4 & x0_15)
    g233 = (g231 & g230)
    g234 = (g232 | g233)
    g235 = (x1_2 ^ 1)
    g236 = (x1_2 & g172)
    g237 = (g235 & g164)
    g238 = (g236 | g237)
    g239 = (x1_4 | x1_3)
    g240 = (g239 ^ 1)
    g241 = (g239 & x0_15)
    g242 = (g240 & g238)
    g243 = (g241 | g242)
    g244 = (g239 ^ 1)
    g245 = (g239 & x0_15)
    g246 = (g244 & g55)
    g247 = (g245 | g246)
    g248 = (g239 ^ 1)
    g249 = (g239 & x0_15)
    g250 = (g248 & g115)
    g251 = (g249 | g250)
    g252 = (g239 ^ 1)
    g253 = (g239 & x0_15)
    g254 = (g252 & g148)
    g255 = (g253 | g254)
    g256 = (x1_3 | x1_2)
    g257 = (x1_4 | g256)
    g258 = (g257 ^ 1)
    g259 = (g257 & x0_15)
    g260 = (g258 & g172)
    g261 = (g259 | g260)
    g262 = (g257 ^ 1)
    g263 = (g257 & x0_15)
    g264 = (g262 & g51)
    g265 = (g263 | g264)
    g266 = (x1_3 | g205)
    g267 = (x1_4 | g266)
    g268 = (g267 ^ 1)
    g269 = (g267 & x0_15)
    g270 = (g268 & g107)
    g271 = (g269 | g270)
    g272 = (x1_3 | g222)
    g273 = (x1_4 | g272)
    g274 = (g273 ^ 1)
    g275 = (g273 & x0_15)
    g276 = (g274 & x0_14)
    g277 = (g275 | g276)
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
    w49 = cat(w48, g277, 1)
    w50 = cat(w49, g271, 1)
    w51 = cat(w50, g265, 1)
    w52 = cat(w51, g261, 1)
    w53 = cat(w52, g255, 1)
    w54 = cat(w53, g251, 1)
    w55 = cat(w54, g247, 1)
    w56 = cat(w55, g243, 1)
    w57 = cat(w56, g234, 1)
    w58 = cat(w57, g217, 1)
    w59 = cat(w58, g200, 1)
    w60 = cat(w59, g184, 1)
    w61 = cat(w60, g156, 1)
    w62 = cat(w61, g123, 1)
    w63 = cat(w62, g63, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_sar_cl_gpr_16__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
