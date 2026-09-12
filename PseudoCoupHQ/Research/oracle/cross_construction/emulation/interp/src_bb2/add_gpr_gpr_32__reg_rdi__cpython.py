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
# one named local per gate, over the term of add_gpr_gpr_32__reg_rdi__cpython.
# The term's layer-5 text, LITERAL:
#   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
def emu_add_gpr_gpr_32__reg_rdi__cpython(a, b):
    x0_0 = ext(a, 0, 0)
    x1_0 = ext(b, 0, 0)
    x1_1 = ext(b, 1, 1)
    x0_1 = ext(a, 1, 1)
    x1_2 = ext(b, 2, 2)
    x0_2 = ext(a, 2, 2)
    x1_3 = ext(b, 3, 3)
    x0_3 = ext(a, 3, 3)
    x1_4 = ext(b, 4, 4)
    x0_4 = ext(a, 4, 4)
    x1_5 = ext(b, 5, 5)
    x0_5 = ext(a, 5, 5)
    x1_6 = ext(b, 6, 6)
    x0_6 = ext(a, 6, 6)
    x1_7 = ext(b, 7, 7)
    x0_7 = ext(a, 7, 7)
    x1_8 = ext(b, 8, 8)
    x0_8 = ext(a, 8, 8)
    x1_9 = ext(b, 9, 9)
    x0_9 = ext(a, 9, 9)
    x1_10 = ext(b, 10, 10)
    x0_10 = ext(a, 10, 10)
    x1_11 = ext(b, 11, 11)
    x0_11 = ext(a, 11, 11)
    x1_12 = ext(b, 12, 12)
    x0_12 = ext(a, 12, 12)
    x1_13 = ext(b, 13, 13)
    x0_13 = ext(a, 13, 13)
    x1_14 = ext(b, 14, 14)
    x0_14 = ext(a, 14, 14)
    x1_15 = ext(b, 15, 15)
    x0_15 = ext(a, 15, 15)
    x1_16 = ext(b, 16, 16)
    x0_16 = ext(a, 16, 16)
    x1_17 = ext(b, 17, 17)
    x0_17 = ext(a, 17, 17)
    x1_18 = ext(b, 18, 18)
    x0_18 = ext(a, 18, 18)
    x1_19 = ext(b, 19, 19)
    x0_19 = ext(a, 19, 19)
    x1_20 = ext(b, 20, 20)
    x0_20 = ext(a, 20, 20)
    x1_21 = ext(b, 21, 21)
    x0_21 = ext(a, 21, 21)
    x1_22 = ext(b, 22, 22)
    x0_22 = ext(a, 22, 22)
    x1_23 = ext(b, 23, 23)
    x0_23 = ext(a, 23, 23)
    x1_24 = ext(b, 24, 24)
    x0_24 = ext(a, 24, 24)
    x1_25 = ext(b, 25, 25)
    x0_25 = ext(a, 25, 25)
    x1_26 = ext(b, 26, 26)
    x0_26 = ext(a, 26, 26)
    x1_27 = ext(b, 27, 27)
    x0_27 = ext(a, 27, 27)
    x1_28 = ext(b, 28, 28)
    x0_28 = ext(a, 28, 28)
    x1_29 = ext(b, 29, 29)
    x0_29 = ext(a, 29, 29)
    x1_30 = ext(b, 30, 30)
    x0_30 = ext(a, 30, 30)
    x1_31 = ext(b, 31, 31)
    x0_31 = ext(a, 31, 31)
    g0 = (x1_0 ^ x0_0)
    g1 = (g0 ^ 1)
    g2 = (g1 ^ 1)
    g3 = (x1_0 ^ 1)
    g4 = (x0_0 ^ 1)
    g5 = (g4 | g3)
    g6 = (x1_1 ^ g5)
    g7 = (g6 ^ 1)
    g8 = (x0_1 ^ g7)
    g9 = (g8 ^ 1)
    g10 = (g9 ^ 1)
    g11 = (x1_1 ^ 1)
    g12 = (g11 | g5)
    g13 = (g12 ^ 1)
    g14 = (x0_1 ^ 1)
    g15 = (g14 | g5)
    g16 = (g15 ^ 1)
    g17 = (g14 | g11)
    g18 = (g17 ^ 1)
    g19 = (g18 | g16)
    g20 = (g19 | g13)
    g21 = (x1_2 ^ g20)
    g22 = (g21 ^ 1)
    g23 = (x0_2 ^ g22)
    g24 = (g23 ^ 1)
    g25 = (g20 ^ 1)
    g26 = (x1_2 ^ 1)
    g27 = (g26 | g25)
    g28 = (g27 ^ 1)
    g29 = (x0_2 ^ 1)
    g30 = (g29 | g25)
    g31 = (g30 ^ 1)
    g32 = (g29 | g26)
    g33 = (g32 ^ 1)
    g34 = (g33 | g31)
    g35 = (g34 | g28)
    g36 = (x1_3 ^ g35)
    g37 = (g36 ^ 1)
    g38 = (x0_3 ^ g37)
    g39 = (g38 ^ 1)
    g40 = (g35 ^ 1)
    g41 = (x1_3 ^ 1)
    g42 = (g41 | g40)
    g43 = (g42 ^ 1)
    g44 = (x0_3 ^ 1)
    g45 = (g44 | g40)
    g46 = (g45 ^ 1)
    g47 = (g44 | g41)
    g48 = (g47 ^ 1)
    g49 = (g48 | g46)
    g50 = (g49 | g43)
    g51 = (x1_4 ^ g50)
    g52 = (g51 ^ 1)
    g53 = (x0_4 ^ g52)
    g54 = (g53 ^ 1)
    g55 = (g50 ^ 1)
    g56 = (x1_4 ^ 1)
    g57 = (g56 | g55)
    g58 = (g57 ^ 1)
    g59 = (x0_4 ^ 1)
    g60 = (g59 | g55)
    g61 = (g60 ^ 1)
    g62 = (g59 | g56)
    g63 = (g62 ^ 1)
    g64 = (g63 | g61)
    g65 = (g64 | g58)
    g66 = (x1_5 ^ g65)
    g67 = (g66 ^ 1)
    g68 = (x0_5 ^ g67)
    g69 = (g68 ^ 1)
    g70 = (g65 ^ 1)
    g71 = (x1_5 ^ 1)
    g72 = (g71 | g70)
    g73 = (g72 ^ 1)
    g74 = (x0_5 ^ 1)
    g75 = (g74 | g70)
    g76 = (g75 ^ 1)
    g77 = (g74 | g71)
    g78 = (g77 ^ 1)
    g79 = (g78 | g76)
    g80 = (g79 | g73)
    g81 = (x1_6 ^ g80)
    g82 = (g81 ^ 1)
    g83 = (x0_6 ^ g82)
    g84 = (g83 ^ 1)
    g85 = (g80 ^ 1)
    g86 = (x1_6 ^ 1)
    g87 = (g86 | g85)
    g88 = (g87 ^ 1)
    g89 = (x0_6 ^ 1)
    g90 = (g89 | g85)
    g91 = (g90 ^ 1)
    g92 = (g89 | g86)
    g93 = (g92 ^ 1)
    g94 = (g93 | g91)
    g95 = (g94 | g88)
    g96 = (x1_7 ^ g95)
    g97 = (g96 ^ 1)
    g98 = (x0_7 ^ g97)
    g99 = (g98 ^ 1)
    g100 = (g95 ^ 1)
    g101 = (x1_7 ^ 1)
    g102 = (g101 | g100)
    g103 = (g102 ^ 1)
    g104 = (x0_7 ^ 1)
    g105 = (g104 | g100)
    g106 = (g105 ^ 1)
    g107 = (g104 | g101)
    g108 = (g107 ^ 1)
    g109 = (g108 | g106)
    g110 = (g109 | g103)
    g111 = (x1_8 ^ g110)
    g112 = (g111 ^ 1)
    g113 = (x0_8 ^ g112)
    g114 = (g113 ^ 1)
    g115 = (g110 ^ 1)
    g116 = (x1_8 ^ 1)
    g117 = (g116 | g115)
    g118 = (g117 ^ 1)
    g119 = (x0_8 ^ 1)
    g120 = (g119 | g115)
    g121 = (g120 ^ 1)
    g122 = (g119 | g116)
    g123 = (g122 ^ 1)
    g124 = (g123 | g121)
    g125 = (g124 | g118)
    g126 = (x1_9 ^ g125)
    g127 = (g126 ^ 1)
    g128 = (x0_9 ^ g127)
    g129 = (g128 ^ 1)
    g130 = (g125 ^ 1)
    g131 = (x1_9 ^ 1)
    g132 = (g131 | g130)
    g133 = (g132 ^ 1)
    g134 = (x0_9 ^ 1)
    g135 = (g134 | g130)
    g136 = (g135 ^ 1)
    g137 = (g134 | g131)
    g138 = (g137 ^ 1)
    g139 = (g138 | g136)
    g140 = (g139 | g133)
    g141 = (x1_10 ^ g140)
    g142 = (g141 ^ 1)
    g143 = (x0_10 ^ g142)
    g144 = (g143 ^ 1)
    g145 = (g140 ^ 1)
    g146 = (x1_10 ^ 1)
    g147 = (g146 | g145)
    g148 = (g147 ^ 1)
    g149 = (x0_10 ^ 1)
    g150 = (g149 | g145)
    g151 = (g150 ^ 1)
    g152 = (g149 | g146)
    g153 = (g152 ^ 1)
    g154 = (g153 | g151)
    g155 = (g154 | g148)
    g156 = (x1_11 ^ g155)
    g157 = (g156 ^ 1)
    g158 = (x0_11 ^ g157)
    g159 = (g158 ^ 1)
    g160 = (g155 ^ 1)
    g161 = (x1_11 ^ 1)
    g162 = (g161 | g160)
    g163 = (g162 ^ 1)
    g164 = (x0_11 ^ 1)
    g165 = (g164 | g160)
    g166 = (g165 ^ 1)
    g167 = (g164 | g161)
    g168 = (g167 ^ 1)
    g169 = (g168 | g166)
    g170 = (g169 | g163)
    g171 = (x1_12 ^ g170)
    g172 = (g171 ^ 1)
    g173 = (x0_12 ^ g172)
    g174 = (g173 ^ 1)
    g175 = (g170 ^ 1)
    g176 = (x1_12 ^ 1)
    g177 = (g176 | g175)
    g178 = (g177 ^ 1)
    g179 = (x0_12 ^ 1)
    g180 = (g179 | g175)
    g181 = (g180 ^ 1)
    g182 = (g179 | g176)
    g183 = (g182 ^ 1)
    g184 = (g183 | g181)
    g185 = (g184 | g178)
    g186 = (x1_13 ^ g185)
    g187 = (g186 ^ 1)
    g188 = (x0_13 ^ g187)
    g189 = (g188 ^ 1)
    g190 = (g185 ^ 1)
    g191 = (x1_13 ^ 1)
    g192 = (g191 | g190)
    g193 = (g192 ^ 1)
    g194 = (x0_13 ^ 1)
    g195 = (g194 | g190)
    g196 = (g195 ^ 1)
    g197 = (g194 | g191)
    g198 = (g197 ^ 1)
    g199 = (g198 | g196)
    g200 = (g199 | g193)
    g201 = (x1_14 ^ g200)
    g202 = (g201 ^ 1)
    g203 = (x0_14 ^ g202)
    g204 = (g203 ^ 1)
    g205 = (g200 ^ 1)
    g206 = (x1_14 ^ 1)
    g207 = (g206 | g205)
    g208 = (g207 ^ 1)
    g209 = (x0_14 ^ 1)
    g210 = (g209 | g205)
    g211 = (g210 ^ 1)
    g212 = (g209 | g206)
    g213 = (g212 ^ 1)
    g214 = (g213 | g211)
    g215 = (g214 | g208)
    g216 = (x1_15 ^ g215)
    g217 = (g216 ^ 1)
    g218 = (x0_15 ^ g217)
    g219 = (g218 ^ 1)
    g220 = (g215 ^ 1)
    g221 = (x1_15 ^ 1)
    g222 = (g221 | g220)
    g223 = (g222 ^ 1)
    g224 = (x0_15 ^ 1)
    g225 = (g224 | g220)
    g226 = (g225 ^ 1)
    g227 = (g224 | g221)
    g228 = (g227 ^ 1)
    g229 = (g228 | g226)
    g230 = (g229 | g223)
    g231 = (x1_16 ^ g230)
    g232 = (g231 ^ 1)
    g233 = (x0_16 ^ g232)
    g234 = (g233 ^ 1)
    g235 = (g230 ^ 1)
    g236 = (x1_16 ^ 1)
    g237 = (g236 | g235)
    g238 = (g237 ^ 1)
    g239 = (x0_16 ^ 1)
    g240 = (g239 | g235)
    g241 = (g240 ^ 1)
    g242 = (g239 | g236)
    g243 = (g242 ^ 1)
    g244 = (g243 | g241)
    g245 = (g244 | g238)
    g246 = (x1_17 ^ g245)
    g247 = (g246 ^ 1)
    g248 = (x0_17 ^ g247)
    g249 = (g248 ^ 1)
    g250 = (g245 ^ 1)
    g251 = (x1_17 ^ 1)
    g252 = (g251 | g250)
    g253 = (g252 ^ 1)
    g254 = (x0_17 ^ 1)
    g255 = (g254 | g250)
    g256 = (g255 ^ 1)
    g257 = (g254 | g251)
    g258 = (g257 ^ 1)
    g259 = (g258 | g256)
    g260 = (g259 | g253)
    g261 = (x1_18 ^ g260)
    g262 = (g261 ^ 1)
    g263 = (x0_18 ^ g262)
    g264 = (g263 ^ 1)
    g265 = (g260 ^ 1)
    g266 = (x1_18 ^ 1)
    g267 = (g266 | g265)
    g268 = (g267 ^ 1)
    g269 = (x0_18 ^ 1)
    g270 = (g269 | g265)
    g271 = (g270 ^ 1)
    g272 = (g269 | g266)
    g273 = (g272 ^ 1)
    g274 = (g273 | g271)
    g275 = (g274 | g268)
    g276 = (x1_19 ^ g275)
    g277 = (g276 ^ 1)
    g278 = (x0_19 ^ g277)
    g279 = (g278 ^ 1)
    g280 = (g275 ^ 1)
    g281 = (x1_19 ^ 1)
    g282 = (g281 | g280)
    g283 = (g282 ^ 1)
    g284 = (x0_19 ^ 1)
    g285 = (g284 | g280)
    g286 = (g285 ^ 1)
    g287 = (g284 | g281)
    g288 = (g287 ^ 1)
    g289 = (g288 | g286)
    g290 = (g289 | g283)
    g291 = (x1_20 ^ g290)
    g292 = (g291 ^ 1)
    g293 = (x0_20 ^ g292)
    g294 = (g293 ^ 1)
    g295 = (g290 ^ 1)
    g296 = (x1_20 ^ 1)
    g297 = (g296 | g295)
    g298 = (g297 ^ 1)
    g299 = (x0_20 ^ 1)
    g300 = (g299 | g295)
    g301 = (g300 ^ 1)
    g302 = (g299 | g296)
    g303 = (g302 ^ 1)
    g304 = (g303 | g301)
    g305 = (g304 | g298)
    g306 = (x1_21 ^ g305)
    g307 = (g306 ^ 1)
    g308 = (x0_21 ^ g307)
    g309 = (g308 ^ 1)
    g310 = (g305 ^ 1)
    g311 = (x1_21 ^ 1)
    g312 = (g311 | g310)
    g313 = (g312 ^ 1)
    g314 = (x0_21 ^ 1)
    g315 = (g314 | g310)
    g316 = (g315 ^ 1)
    g317 = (g314 | g311)
    g318 = (g317 ^ 1)
    g319 = (g318 | g316)
    g320 = (g319 | g313)
    g321 = (x1_22 ^ g320)
    g322 = (g321 ^ 1)
    g323 = (x0_22 ^ g322)
    g324 = (g323 ^ 1)
    g325 = (g320 ^ 1)
    g326 = (x1_22 ^ 1)
    g327 = (g326 | g325)
    g328 = (g327 ^ 1)
    g329 = (x0_22 ^ 1)
    g330 = (g329 | g325)
    g331 = (g330 ^ 1)
    g332 = (g329 | g326)
    g333 = (g332 ^ 1)
    g334 = (g333 | g331)
    g335 = (g334 | g328)
    g336 = (x1_23 ^ g335)
    g337 = (g336 ^ 1)
    g338 = (x0_23 ^ g337)
    g339 = (g338 ^ 1)
    g340 = (g335 ^ 1)
    g341 = (x1_23 ^ 1)
    g342 = (g341 | g340)
    g343 = (g342 ^ 1)
    g344 = (x0_23 ^ 1)
    g345 = (g344 | g340)
    g346 = (g345 ^ 1)
    g347 = (g344 | g341)
    g348 = (g347 ^ 1)
    g349 = (g348 | g346)
    g350 = (g349 | g343)
    g351 = (x1_24 ^ g350)
    g352 = (g351 ^ 1)
    g353 = (x0_24 ^ g352)
    g354 = (g353 ^ 1)
    g355 = (g350 ^ 1)
    g356 = (x1_24 ^ 1)
    g357 = (g356 | g355)
    g358 = (g357 ^ 1)
    g359 = (x0_24 ^ 1)
    g360 = (g359 | g355)
    g361 = (g360 ^ 1)
    g362 = (g359 | g356)
    g363 = (g362 ^ 1)
    g364 = (g363 | g361)
    g365 = (g364 | g358)
    g366 = (x1_25 ^ g365)
    g367 = (g366 ^ 1)
    g368 = (x0_25 ^ g367)
    g369 = (g368 ^ 1)
    g370 = (g365 ^ 1)
    g371 = (x1_25 ^ 1)
    g372 = (g371 | g370)
    g373 = (g372 ^ 1)
    g374 = (x0_25 ^ 1)
    g375 = (g374 | g370)
    g376 = (g375 ^ 1)
    g377 = (g374 | g371)
    g378 = (g377 ^ 1)
    g379 = (g378 | g376)
    g380 = (g379 | g373)
    g381 = (x1_26 ^ g380)
    g382 = (g381 ^ 1)
    g383 = (x0_26 ^ g382)
    g384 = (g383 ^ 1)
    g385 = (g380 ^ 1)
    g386 = (x1_26 ^ 1)
    g387 = (g386 | g385)
    g388 = (g387 ^ 1)
    g389 = (x0_26 ^ 1)
    g390 = (g389 | g385)
    g391 = (g390 ^ 1)
    g392 = (g389 | g386)
    g393 = (g392 ^ 1)
    g394 = (g393 | g391)
    g395 = (g394 | g388)
    g396 = (x1_27 ^ g395)
    g397 = (g396 ^ 1)
    g398 = (x0_27 ^ g397)
    g399 = (g398 ^ 1)
    g400 = (g395 ^ 1)
    g401 = (x1_27 ^ 1)
    g402 = (g401 | g400)
    g403 = (g402 ^ 1)
    g404 = (x0_27 ^ 1)
    g405 = (g404 | g400)
    g406 = (g405 ^ 1)
    g407 = (g404 | g401)
    g408 = (g407 ^ 1)
    g409 = (g408 | g406)
    g410 = (g409 | g403)
    g411 = (x1_28 ^ g410)
    g412 = (g411 ^ 1)
    g413 = (x0_28 ^ g412)
    g414 = (g413 ^ 1)
    g415 = (g410 ^ 1)
    g416 = (x1_28 ^ 1)
    g417 = (g416 | g415)
    g418 = (g417 ^ 1)
    g419 = (x0_28 ^ 1)
    g420 = (g419 | g415)
    g421 = (g420 ^ 1)
    g422 = (g419 | g416)
    g423 = (g422 ^ 1)
    g424 = (g423 | g421)
    g425 = (g424 | g418)
    g426 = (x1_29 ^ g425)
    g427 = (g426 ^ 1)
    g428 = (x0_29 ^ g427)
    g429 = (g428 ^ 1)
    g430 = (g425 ^ 1)
    g431 = (x1_29 ^ 1)
    g432 = (g431 | g430)
    g433 = (g432 ^ 1)
    g434 = (x0_29 ^ 1)
    g435 = (g434 | g430)
    g436 = (g435 ^ 1)
    g437 = (g434 | g431)
    g438 = (g437 ^ 1)
    g439 = (g438 | g436)
    g440 = (g439 | g433)
    g441 = (x1_30 ^ g440)
    g442 = (g441 ^ 1)
    g443 = (x0_30 ^ g442)
    g444 = (g443 ^ 1)
    g445 = (g440 ^ 1)
    g446 = (x1_30 ^ 1)
    g447 = (g446 | g445)
    g448 = (g447 ^ 1)
    g449 = (x0_30 ^ 1)
    g450 = (g449 | g445)
    g451 = (g450 ^ 1)
    g452 = (g449 | g446)
    g453 = (g452 ^ 1)
    g454 = (g453 | g451)
    g455 = (g454 | g448)
    g456 = (x1_31 ^ g455)
    g457 = (g456 ^ 1)
    g458 = (x0_31 ^ g457)
    g459 = (g458 ^ 1)
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
    w32 = cat(w31, g459, 1)
    w33 = cat(w32, g444, 1)
    w34 = cat(w33, g429, 1)
    w35 = cat(w34, g414, 1)
    w36 = cat(w35, g399, 1)
    w37 = cat(w36, g384, 1)
    w38 = cat(w37, g369, 1)
    w39 = cat(w38, g354, 1)
    w40 = cat(w39, g339, 1)
    w41 = cat(w40, g324, 1)
    w42 = cat(w41, g309, 1)
    w43 = cat(w42, g294, 1)
    w44 = cat(w43, g279, 1)
    w45 = cat(w44, g264, 1)
    w46 = cat(w45, g249, 1)
    w47 = cat(w46, g234, 1)
    w48 = cat(w47, g219, 1)
    w49 = cat(w48, g204, 1)
    w50 = cat(w49, g189, 1)
    w51 = cat(w50, g174, 1)
    w52 = cat(w51, g159, 1)
    w53 = cat(w52, g144, 1)
    w54 = cat(w53, g129, 1)
    w55 = cat(w54, g114, 1)
    w56 = cat(w55, g99, 1)
    w57 = cat(w56, g84, 1)
    w58 = cat(w57, g69, 1)
    w59 = cat(w58, g54, 1)
    w60 = cat(w59, g39, 1)
    w61 = cat(w60, g24, 1)
    w62 = cat(w61, g10, 1)
    w63 = cat(w62, g2, 1)
    return m(w63, 64)



def main():
    for line in sys.stdin:
        text = line.strip()
        if not text:
            continue
        values = [int(one) for one in text.split()]
        try:
            answer = emu_add_gpr_gpr_32__reg_rdi__cpython(*values)
            sys.stdout.write("%d\n" % answer)
        except Exception as problem:
            sys.stdout.write("RAISE:%s\n" % type(problem).__name__)
    sys.stdout.flush()


main()
