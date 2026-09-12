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
# one named local per gate, over the term of sbb_gpr_same_32__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(0, If(Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1, 1, 0)*4294967295)
def emu_sbb_gpr_same_32__reg_rdi__cpython(a, b, c):
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
    x1_8 = ext(a, 8, 8)
    x0_8 = ext(b, 8, 8)
    x1_9 = ext(a, 9, 9)
    x0_9 = ext(b, 9, 9)
    x1_10 = ext(a, 10, 10)
    x0_10 = ext(b, 10, 10)
    x1_11 = ext(a, 11, 11)
    x0_11 = ext(b, 11, 11)
    x1_12 = ext(a, 12, 12)
    x0_12 = ext(b, 12, 12)
    x1_13 = ext(a, 13, 13)
    x0_13 = ext(b, 13, 13)
    x1_14 = ext(a, 14, 14)
    x0_14 = ext(b, 14, 14)
    x1_15 = ext(a, 15, 15)
    x0_15 = ext(b, 15, 15)
    x1_16 = ext(a, 16, 16)
    x0_16 = ext(b, 16, 16)
    x1_17 = ext(a, 17, 17)
    x0_17 = ext(b, 17, 17)
    x1_18 = ext(a, 18, 18)
    x0_18 = ext(b, 18, 18)
    x1_19 = ext(a, 19, 19)
    x0_19 = ext(b, 19, 19)
    x1_20 = ext(a, 20, 20)
    x0_20 = ext(b, 20, 20)
    x1_21 = ext(a, 21, 21)
    x0_21 = ext(b, 21, 21)
    x1_22 = ext(a, 22, 22)
    x0_22 = ext(b, 22, 22)
    x1_23 = ext(a, 23, 23)
    x0_23 = ext(b, 23, 23)
    x1_24 = ext(a, 24, 24)
    x0_24 = ext(b, 24, 24)
    x1_25 = ext(a, 25, 25)
    x0_25 = ext(b, 25, 25)
    x1_26 = ext(a, 26, 26)
    x0_26 = ext(b, 26, 26)
    x1_27 = ext(a, 27, 27)
    x0_27 = ext(b, 27, 27)
    x1_28 = ext(a, 28, 28)
    x0_28 = ext(b, 28, 28)
    x1_29 = ext(a, 29, 29)
    x0_29 = ext(b, 29, 29)
    x1_30 = ext(a, 30, 30)
    x0_30 = ext(b, 30, 30)
    x1_31 = ext(a, 31, 31)
    x0_31 = ext(b, 31, 31)
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
    g13 = (g12 ^ 1)
    g14 = (x1_2 ^ 1)
    g15 = (g14 | g13)
    g16 = (g15 ^ 1)
    g17 = (x0_2 ^ 1)
    g18 = (g17 | g13)
    g19 = (g18 ^ 1)
    g20 = (g17 | g14)
    g21 = (g20 ^ 1)
    g22 = (g21 | g19)
    g23 = (g22 | g16)
    g24 = (g23 ^ 1)
    g25 = (x1_3 ^ 1)
    g26 = (g25 | g24)
    g27 = (g26 ^ 1)
    g28 = (x0_3 ^ 1)
    g29 = (g28 | g24)
    g30 = (g29 ^ 1)
    g31 = (g28 | g25)
    g32 = (g31 ^ 1)
    g33 = (g32 | g30)
    g34 = (g33 | g27)
    g35 = (g34 ^ 1)
    g36 = (x1_4 ^ 1)
    g37 = (g36 | g35)
    g38 = (g37 ^ 1)
    g39 = (x0_4 ^ 1)
    g40 = (g39 | g35)
    g41 = (g40 ^ 1)
    g42 = (g39 | g36)
    g43 = (g42 ^ 1)
    g44 = (g43 | g41)
    g45 = (g44 | g38)
    g46 = (g45 ^ 1)
    g47 = (x1_5 ^ 1)
    g48 = (g47 | g46)
    g49 = (g48 ^ 1)
    g50 = (x0_5 ^ 1)
    g51 = (g50 | g46)
    g52 = (g51 ^ 1)
    g53 = (g50 | g47)
    g54 = (g53 ^ 1)
    g55 = (g54 | g52)
    g56 = (g55 | g49)
    g57 = (g56 ^ 1)
    g58 = (x1_6 ^ 1)
    g59 = (g58 | g57)
    g60 = (g59 ^ 1)
    g61 = (x0_6 ^ 1)
    g62 = (g61 | g57)
    g63 = (g62 ^ 1)
    g64 = (g61 | g58)
    g65 = (g64 ^ 1)
    g66 = (g65 | g63)
    g67 = (g66 | g60)
    g68 = (g67 ^ 1)
    g69 = (x1_7 ^ 1)
    g70 = (g69 | g68)
    g71 = (g70 ^ 1)
    g72 = (x0_7 ^ 1)
    g73 = (g72 | g68)
    g74 = (g73 ^ 1)
    g75 = (g72 | g69)
    g76 = (g75 ^ 1)
    g77 = (g76 | g74)
    g78 = (g77 | g71)
    g79 = (g78 ^ 1)
    g80 = (x1_8 ^ 1)
    g81 = (g80 | g79)
    g82 = (g81 ^ 1)
    g83 = (x0_8 ^ 1)
    g84 = (g83 | g79)
    g85 = (g84 ^ 1)
    g86 = (g83 | g80)
    g87 = (g86 ^ 1)
    g88 = (g87 | g85)
    g89 = (g88 | g82)
    g90 = (g89 ^ 1)
    g91 = (x1_9 ^ 1)
    g92 = (g91 | g90)
    g93 = (g92 ^ 1)
    g94 = (x0_9 ^ 1)
    g95 = (g94 | g90)
    g96 = (g95 ^ 1)
    g97 = (g94 | g91)
    g98 = (g97 ^ 1)
    g99 = (g98 | g96)
    g100 = (g99 | g93)
    g101 = (g100 ^ 1)
    g102 = (x1_10 ^ 1)
    g103 = (g102 | g101)
    g104 = (g103 ^ 1)
    g105 = (x0_10 ^ 1)
    g106 = (g105 | g101)
    g107 = (g106 ^ 1)
    g108 = (g105 | g102)
    g109 = (g108 ^ 1)
    g110 = (g109 | g107)
    g111 = (g110 | g104)
    g112 = (g111 ^ 1)
    g113 = (x1_11 ^ 1)
    g114 = (g113 | g112)
    g115 = (g114 ^ 1)
    g116 = (x0_11 ^ 1)
    g117 = (g116 | g112)
    g118 = (g117 ^ 1)
    g119 = (g116 | g113)
    g120 = (g119 ^ 1)
    g121 = (g120 | g118)
    g122 = (g121 | g115)
    g123 = (g122 ^ 1)
    g124 = (x1_12 ^ 1)
    g125 = (g124 | g123)
    g126 = (g125 ^ 1)
    g127 = (x0_12 ^ 1)
    g128 = (g127 | g123)
    g129 = (g128 ^ 1)
    g130 = (g127 | g124)
    g131 = (g130 ^ 1)
    g132 = (g131 | g129)
    g133 = (g132 | g126)
    g134 = (g133 ^ 1)
    g135 = (x1_13 ^ 1)
    g136 = (g135 | g134)
    g137 = (g136 ^ 1)
    g138 = (x0_13 ^ 1)
    g139 = (g138 | g134)
    g140 = (g139 ^ 1)
    g141 = (g138 | g135)
    g142 = (g141 ^ 1)
    g143 = (g142 | g140)
    g144 = (g143 | g137)
    g145 = (g144 ^ 1)
    g146 = (x1_14 ^ 1)
    g147 = (g146 | g145)
    g148 = (g147 ^ 1)
    g149 = (x0_14 ^ 1)
    g150 = (g149 | g145)
    g151 = (g150 ^ 1)
    g152 = (g149 | g146)
    g153 = (g152 ^ 1)
    g154 = (g153 | g151)
    g155 = (g154 | g148)
    g156 = (g155 ^ 1)
    g157 = (x1_15 ^ 1)
    g158 = (g157 | g156)
    g159 = (g158 ^ 1)
    g160 = (x0_15 ^ 1)
    g161 = (g160 | g156)
    g162 = (g161 ^ 1)
    g163 = (g160 | g157)
    g164 = (g163 ^ 1)
    g165 = (g164 | g162)
    g166 = (g165 | g159)
    g167 = (g166 ^ 1)
    g168 = (x1_16 ^ 1)
    g169 = (g168 | g167)
    g170 = (g169 ^ 1)
    g171 = (x0_16 ^ 1)
    g172 = (g171 | g167)
    g173 = (g172 ^ 1)
    g174 = (g171 | g168)
    g175 = (g174 ^ 1)
    g176 = (g175 | g173)
    g177 = (g176 | g170)
    g178 = (g177 ^ 1)
    g179 = (x1_17 ^ 1)
    g180 = (g179 | g178)
    g181 = (g180 ^ 1)
    g182 = (x0_17 ^ 1)
    g183 = (g182 | g178)
    g184 = (g183 ^ 1)
    g185 = (g182 | g179)
    g186 = (g185 ^ 1)
    g187 = (g186 | g184)
    g188 = (g187 | g181)
    g189 = (g188 ^ 1)
    g190 = (x1_18 ^ 1)
    g191 = (g190 | g189)
    g192 = (g191 ^ 1)
    g193 = (x0_18 ^ 1)
    g194 = (g193 | g189)
    g195 = (g194 ^ 1)
    g196 = (g193 | g190)
    g197 = (g196 ^ 1)
    g198 = (g197 | g195)
    g199 = (g198 | g192)
    g200 = (g199 ^ 1)
    g201 = (x1_19 ^ 1)
    g202 = (g201 | g200)
    g203 = (g202 ^ 1)
    g204 = (x0_19 ^ 1)
    g205 = (g204 | g200)
    g206 = (g205 ^ 1)
    g207 = (g204 | g201)
    g208 = (g207 ^ 1)
    g209 = (g208 | g206)
    g210 = (g209 | g203)
    g211 = (g210 ^ 1)
    g212 = (x1_20 ^ 1)
    g213 = (g212 | g211)
    g214 = (g213 ^ 1)
    g215 = (x0_20 ^ 1)
    g216 = (g215 | g211)
    g217 = (g216 ^ 1)
    g218 = (g215 | g212)
    g219 = (g218 ^ 1)
    g220 = (g219 | g217)
    g221 = (g220 | g214)
    g222 = (g221 ^ 1)
    g223 = (x1_21 ^ 1)
    g224 = (g223 | g222)
    g225 = (g224 ^ 1)
    g226 = (x0_21 ^ 1)
    g227 = (g226 | g222)
    g228 = (g227 ^ 1)
    g229 = (g226 | g223)
    g230 = (g229 ^ 1)
    g231 = (g230 | g228)
    g232 = (g231 | g225)
    g233 = (g232 ^ 1)
    g234 = (x1_22 ^ 1)
    g235 = (g234 | g233)
    g236 = (g235 ^ 1)
    g237 = (x0_22 ^ 1)
    g238 = (g237 | g233)
    g239 = (g238 ^ 1)
    g240 = (g237 | g234)
    g241 = (g240 ^ 1)
    g242 = (g241 | g239)
    g243 = (g242 | g236)
    g244 = (g243 ^ 1)
    g245 = (x1_23 ^ 1)
    g246 = (g245 | g244)
    g247 = (g246 ^ 1)
    g248 = (x0_23 ^ 1)
    g249 = (g248 | g244)
    g250 = (g249 ^ 1)
    g251 = (g248 | g245)
    g252 = (g251 ^ 1)
    g253 = (g252 | g250)
    g254 = (g253 | g247)
    g255 = (g254 ^ 1)
    g256 = (x1_24 ^ 1)
    g257 = (g256 | g255)
    g258 = (g257 ^ 1)
    g259 = (x0_24 ^ 1)
    g260 = (g259 | g255)
    g261 = (g260 ^ 1)
    g262 = (g259 | g256)
    g263 = (g262 ^ 1)
    g264 = (g263 | g261)
    g265 = (g264 | g258)
    g266 = (g265 ^ 1)
    g267 = (x1_25 ^ 1)
    g268 = (g267 | g266)
    g269 = (g268 ^ 1)
    g270 = (x0_25 ^ 1)
    g271 = (g270 | g266)
    g272 = (g271 ^ 1)
    g273 = (g270 | g267)
    g274 = (g273 ^ 1)
    g275 = (g274 | g272)
    g276 = (g275 | g269)
    g277 = (g276 ^ 1)
    g278 = (x1_26 ^ 1)
    g279 = (g278 | g277)
    g280 = (g279 ^ 1)
    g281 = (x0_26 ^ 1)
    g282 = (g281 | g277)
    g283 = (g282 ^ 1)
    g284 = (g281 | g278)
    g285 = (g284 ^ 1)
    g286 = (g285 | g283)
    g287 = (g286 | g280)
    g288 = (g287 ^ 1)
    g289 = (x1_27 ^ 1)
    g290 = (g289 | g288)
    g291 = (g290 ^ 1)
    g292 = (x0_27 ^ 1)
    g293 = (g292 | g288)
    g294 = (g293 ^ 1)
    g295 = (g292 | g289)
    g296 = (g295 ^ 1)
    g297 = (g296 | g294)
    g298 = (g297 | g291)
    g299 = (g298 ^ 1)
    g300 = (x1_28 ^ 1)
    g301 = (g300 | g299)
    g302 = (g301 ^ 1)
    g303 = (x0_28 ^ 1)
    g304 = (g303 | g299)
    g305 = (g304 ^ 1)
    g306 = (g303 | g300)
    g307 = (g306 ^ 1)
    g308 = (g307 | g305)
    g309 = (g308 | g302)
    g310 = (g309 ^ 1)
    g311 = (x1_29 ^ 1)
    g312 = (g311 | g310)
    g313 = (g312 ^ 1)
    g314 = (x0_29 ^ 1)
    g315 = (g314 | g310)
    g316 = (g315 ^ 1)
    g317 = (g314 | g311)
    g318 = (g317 ^ 1)
    g319 = (g318 | g316)
    g320 = (g319 | g313)
    g321 = (g320 ^ 1)
    g322 = (x1_30 ^ 1)
    g323 = (g322 | g321)
    g324 = (g323 ^ 1)
    g325 = (x0_30 ^ 1)
    g326 = (g325 | g321)
    g327 = (g326 ^ 1)
    g328 = (g325 | g322)
    g329 = (g328 ^ 1)
    g330 = (g329 | g327)
    g331 = (g330 | g324)
    g332 = (g331 ^ 1)
    g333 = (x1_31 ^ 1)
    g334 = (g333 | g332)
    g335 = (g334 ^ 1)
    g336 = (x0_31 ^ 1)
    g337 = (g336 | g332)
    g338 = (g337 ^ 1)
    g339 = (g336 | g333)
    g340 = (g339 ^ 1)
    g341 = (g340 | g338)
    g342 = (g341 | g335)
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
    w32 = cat(w31, g342, 1)
    w33 = cat(w32, g342, 1)
    w34 = cat(w33, g342, 1)
    w35 = cat(w34, g342, 1)
    w36 = cat(w35, g342, 1)
    w37 = cat(w36, g342, 1)
    w38 = cat(w37, g342, 1)
    w39 = cat(w38, g342, 1)
    w40 = cat(w39, g342, 1)
    w41 = cat(w40, g342, 1)
    w42 = cat(w41, g342, 1)
    w43 = cat(w42, g342, 1)
    w44 = cat(w43, g342, 1)
    w45 = cat(w44, g342, 1)
    w46 = cat(w45, g342, 1)
    w47 = cat(w46, g342, 1)
    w48 = cat(w47, g342, 1)
    w49 = cat(w48, g342, 1)
    w50 = cat(w49, g342, 1)
    w51 = cat(w50, g342, 1)
    w52 = cat(w51, g342, 1)
    w53 = cat(w52, g342, 1)
    w54 = cat(w53, g342, 1)
    w55 = cat(w54, g342, 1)
    w56 = cat(w55, g342, 1)
    w57 = cat(w56, g342, 1)
    w58 = cat(w57, g342, 1)
    w59 = cat(w58, g342, 1)
    w60 = cat(w59, g342, 1)
    w61 = cat(w60, g342, 1)
    w62 = cat(w61, g342, 1)
    w63 = cat(w62, g342, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_sbb_gpr_same_32__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
