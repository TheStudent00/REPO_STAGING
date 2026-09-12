using System;
using System.Text;

public static class Emu {
    public static long m(long x, int w) {
        if (w >= 64) { return x; }
        return x & ((1L << w) - 1L);
    }
    public static long s(long x, int w) {
        if (w >= 64) { return x; }
        return (x << (64 - w)) >> (64 - w);
    }
    public static long add(long a, long b, int w) { return m(unchecked(a + b), w); }
    public static long sub(long a, long b, int w) { return m(unchecked(a - b), w); }
    public static long mul(long a, long b, int w) { return m(unchecked(a * b), w); }
    public static long band(long a, long b, int w) { return m(a & b, w); }
    public static long bor(long a, long b, int w) { return m(a | b, w); }
    public static long bxor(long a, long b, int w) { return m(a ^ b, w); }
    public static long bnot(long a, int w) { return m(~a, w); }
    public static long bneg(long a, int w) { return m(unchecked(-a), w); }
    public static long shl(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(a << (int) n, w);
    }
    public static long lshr(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m((long)(((ulong) m(a, w)) >> (int) n), w);
    }
    public static long ashr(long a, long n, int w) {
        long v = s(a, w);
        long k = n;
        if (k >= w) { k = w - 1; }
        return m(v >> (int) k, w);
    }
    public static long udiv(long a, long b, int w) {
        return m((long)(((ulong) m(a, w)) / ((ulong) m(b, w))), w);
    }
    public static long urem(long a, long b, int w) {
        return m((long)(((ulong) m(a, w)) % ((ulong) m(b, w))), w);
    }
    public static long sdiv(long a, long b, int w) { return m(s(a, w) / s(b, w), w); }
    public static long srem(long a, long b, int w) { return m(s(a, w) % s(b, w), w); }
    public static bool ult(long a, long b, int w) { return ((ulong) m(a, w)) < ((ulong) m(b, w)); }
    public static bool ule(long a, long b, int w) { return ((ulong) m(a, w)) <= ((ulong) m(b, w)); }
    public static bool ugt(long a, long b, int w) { return ((ulong) m(a, w)) > ((ulong) m(b, w)); }
    public static bool uge(long a, long b, int w) { return ((ulong) m(a, w)) >= ((ulong) m(b, w)); }
    public static bool slt(long a, long b, int w) { return s(a, w) < s(b, w); }
    public static bool sle(long a, long b, int w) { return s(a, w) <= s(b, w); }
    public static bool sgt(long a, long b, int w) { return s(a, w) > s(b, w); }
    public static bool sge(long a, long b, int w) { return s(a, w) >= s(b, w); }
    public static bool eq(long a, long b, int w) { return m(a, w) == m(b, w); }
    public static bool ne(long a, long b, int w) { return m(a, w) != m(b, w); }
    public static long cat(long hi, long lo, int lw) { return (hi << lw) | m(lo, lw); }
    public static long ext(long x, int hi, int lo) {
        return m((long)(((ulong) x) >> lo), hi - lo + 1);
    }
    public static long sext(long x, int fromw, int tow) { return m(s(x, fromw), tow); }
    public static double b2f(long x, int w) {
        if (w == 32) { return BitConverter.UInt32BitsToSingle((uint) m(x, 32)); }
        return BitConverter.Int64BitsToDouble(x);
    }
    public static long f2b(double f, int w) {
        if (w == 32) { return (long) BitConverter.SingleToUInt32Bits((float) f); }
        return BitConverter.DoubleToInt64Bits(f);
    }
    public static long fadd(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    + BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) + b2f(b, w), w);
    }
    public static long fsub(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    - BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) - b2f(b, w), w);
    }
    public static long fmul(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    * BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) * b2f(b, w), w);
    }
    public static long fdiv(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    / BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) / b2f(b, w), w);
    }
    public static long i2f(long x, int fromw, int w) {
        if (w == 32) {
            return (long) BitConverter.SingleToUInt32Bits((float) s(x, fromw));
        }
        return BitConverter.DoubleToInt64Bits((double) s(x, fromw));
    }
    public static long u2f(long x, int fromw, int w) {
        if (w == 32) {
            return (long) BitConverter.SingleToUInt32Bits((float)(ulong) m(x, fromw));
        }
        return BitConverter.DoubleToInt64Bits((double)(ulong) m(x, fromw));
    }
    public static long fwiden(long x, int fromw, int w) { return f2b(b2f(x, fromw), w); }

    // task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
    // one named local per gate, over the term of shl_cl_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0) << Concat(0, Extract(4, 0, v1)))
    public static long emu_shl_cl_gpr_32__reg_rdi__csharp(long a, long b) {
        long x0_0 = ext(a, 0, 0);
        long x1_0 = ext(b, 0, 0);
        long x1_1 = ext(b, 1, 1);
        long x1_2 = ext(b, 2, 2);
        long x1_3 = ext(b, 3, 3);
        long x1_4 = ext(b, 4, 4);
        long x0_1 = ext(a, 1, 1);
        long x0_2 = ext(a, 2, 2);
        long x0_3 = ext(a, 3, 3);
        long x0_4 = ext(a, 4, 4);
        long x0_5 = ext(a, 5, 5);
        long x0_6 = ext(a, 6, 6);
        long x0_7 = ext(a, 7, 7);
        long x0_8 = ext(a, 8, 8);
        long x0_9 = ext(a, 9, 9);
        long x0_10 = ext(a, 10, 10);
        long x0_11 = ext(a, 11, 11);
        long x0_12 = ext(a, 12, 12);
        long x0_13 = ext(a, 13, 13);
        long x0_14 = ext(a, 14, 14);
        long x0_15 = ext(a, 15, 15);
        long x0_16 = ext(a, 16, 16);
        long x0_17 = ext(a, 17, 17);
        long x0_18 = ext(a, 18, 18);
        long x0_19 = ext(a, 19, 19);
        long x0_20 = ext(a, 20, 20);
        long x0_21 = ext(a, 21, 21);
        long x0_22 = ext(a, 22, 22);
        long x0_23 = ext(a, 23, 23);
        long x0_24 = ext(a, 24, 24);
        long x0_25 = ext(a, 25, 25);
        long x0_26 = ext(a, 26, 26);
        long x0_27 = ext(a, 27, 27);
        long x0_28 = ext(a, 28, 28);
        long x0_29 = ext(a, 29, 29);
        long x0_30 = ext(a, 30, 30);
        long x0_31 = ext(a, 31, 31);
        long g0 = (x1_0 ^ 1L);
        long g1 = (x1_1 ^ 1L);
        long g2 = (x1_2 ^ 1L);
        long g3 = (x1_3 ^ 1L);
        long g4 = (x1_4 ^ 1L);
        long g5 = (g4 & g3);
        long g6 = (g5 & g2);
        long g7 = (g6 & g1);
        long g8 = (g7 & g0);
        long g9 = (g8 & x0_0);
        long g10 = (x1_0 ^ 1L);
        long g11 = (x1_0 & x0_0);
        long g12 = (g10 & x0_1);
        long g13 = (g11 | g12);
        long g14 = (g4 & g3);
        long g15 = (g14 & g2);
        long g16 = (g15 & g1);
        long g17 = (g16 & g13);
        long g18 = (x1_0 ^ 1L);
        long g19 = (x1_0 & x0_1);
        long g20 = (g18 & x0_2);
        long g21 = (g19 | g20);
        long g22 = (x0_0 ^ 1L);
        long g23 = (x1_0 | g22);
        long g24 = (g23 ^ 1L);
        long g25 = (x1_1 ^ 1L);
        long g26 = (x1_1 & g24);
        long g27 = (g25 & g21);
        long g28 = (g26 | g27);
        long g29 = (g4 & g3);
        long g30 = (g29 & g2);
        long g31 = (g30 & g28);
        long g32 = (x1_0 ^ 1L);
        long g33 = (x1_0 & x0_2);
        long g34 = (g32 & x0_3);
        long g35 = (g33 | g34);
        long g36 = (x1_1 ^ 1L);
        long g37 = (x1_1 & g13);
        long g38 = (g36 & g35);
        long g39 = (g37 | g38);
        long g40 = (g4 & g3);
        long g41 = (g40 & g2);
        long g42 = (g41 & g39);
        long g43 = (x1_0 ^ 1L);
        long g44 = (x1_0 & x0_3);
        long g45 = (g43 & x0_4);
        long g46 = (g44 | g45);
        long g47 = (x1_1 ^ 1L);
        long g48 = (x1_1 & g21);
        long g49 = (g47 & g46);
        long g50 = (g48 | g49);
        long g51 = (x1_1 | g23);
        long g52 = (g51 ^ 1L);
        long g53 = (x1_2 ^ 1L);
        long g54 = (x1_2 & g52);
        long g55 = (g53 & g50);
        long g56 = (g54 | g55);
        long g57 = (g4 & g3);
        long g58 = (g57 & g56);
        long g59 = (x1_0 ^ 1L);
        long g60 = (x1_0 & x0_4);
        long g61 = (g59 & x0_5);
        long g62 = (g60 | g61);
        long g63 = (x1_1 ^ 1L);
        long g64 = (x1_1 & g35);
        long g65 = (g63 & g62);
        long g66 = (g64 | g65);
        long g67 = (g13 ^ 1L);
        long g68 = (x1_1 | g67);
        long g69 = (g68 ^ 1L);
        long g70 = (x1_2 ^ 1L);
        long g71 = (x1_2 & g69);
        long g72 = (g70 & g66);
        long g73 = (g71 | g72);
        long g74 = (g4 & g3);
        long g75 = (g74 & g73);
        long g76 = (x1_0 ^ 1L);
        long g77 = (x1_0 & x0_5);
        long g78 = (g76 & x0_6);
        long g79 = (g77 | g78);
        long g80 = (x1_1 ^ 1L);
        long g81 = (x1_1 & g46);
        long g82 = (g80 & g79);
        long g83 = (g81 | g82);
        long g84 = (x1_2 ^ 1L);
        long g85 = (x1_2 & g28);
        long g86 = (g84 & g83);
        long g87 = (g85 | g86);
        long g88 = (g4 & g3);
        long g89 = (g88 & g87);
        long g90 = (x1_0 ^ 1L);
        long g91 = (x1_0 & x0_6);
        long g92 = (g90 & x0_7);
        long g93 = (g91 | g92);
        long g94 = (x1_1 ^ 1L);
        long g95 = (x1_1 & g62);
        long g96 = (g94 & g93);
        long g97 = (g95 | g96);
        long g98 = (x1_2 ^ 1L);
        long g99 = (x1_2 & g39);
        long g100 = (g98 & g97);
        long g101 = (g99 | g100);
        long g102 = (g4 & g3);
        long g103 = (g102 & g101);
        long g104 = (x1_0 ^ 1L);
        long g105 = (x1_0 & x0_7);
        long g106 = (g104 & x0_8);
        long g107 = (g105 | g106);
        long g108 = (x1_1 ^ 1L);
        long g109 = (x1_1 & g79);
        long g110 = (g108 & g107);
        long g111 = (g109 | g110);
        long g112 = (x1_2 ^ 1L);
        long g113 = (x1_2 & g50);
        long g114 = (g112 & g111);
        long g115 = (g113 | g114);
        long g116 = (x1_2 | g51);
        long g117 = (g116 ^ 1L);
        long g118 = (x1_3 ^ 1L);
        long g119 = (x1_3 & g117);
        long g120 = (g118 & g115);
        long g121 = (g119 | g120);
        long g122 = (g4 & g121);
        long g123 = (x1_0 ^ 1L);
        long g124 = (x1_0 & x0_8);
        long g125 = (g123 & x0_9);
        long g126 = (g124 | g125);
        long g127 = (x1_1 ^ 1L);
        long g128 = (x1_1 & g93);
        long g129 = (g127 & g126);
        long g130 = (g128 | g129);
        long g131 = (x1_2 ^ 1L);
        long g132 = (x1_2 & g66);
        long g133 = (g131 & g130);
        long g134 = (g132 | g133);
        long g135 = (x1_2 | g68);
        long g136 = (g135 ^ 1L);
        long g137 = (x1_3 ^ 1L);
        long g138 = (x1_3 & g136);
        long g139 = (g137 & g134);
        long g140 = (g138 | g139);
        long g141 = (g4 & g140);
        long g142 = (x1_0 ^ 1L);
        long g143 = (x1_0 & x0_9);
        long g144 = (g142 & x0_10);
        long g145 = (g143 | g144);
        long g146 = (x1_1 ^ 1L);
        long g147 = (x1_1 & g107);
        long g148 = (g146 & g145);
        long g149 = (g147 | g148);
        long g150 = (x1_2 ^ 1L);
        long g151 = (x1_2 & g83);
        long g152 = (g150 & g149);
        long g153 = (g151 | g152);
        long g154 = (g28 ^ 1L);
        long g155 = (x1_2 | g154);
        long g156 = (g155 ^ 1L);
        long g157 = (x1_3 ^ 1L);
        long g158 = (x1_3 & g156);
        long g159 = (g157 & g153);
        long g160 = (g158 | g159);
        long g161 = (g4 & g160);
        long g162 = (x1_0 ^ 1L);
        long g163 = (x1_0 & x0_10);
        long g164 = (g162 & x0_11);
        long g165 = (g163 | g164);
        long g166 = (x1_1 ^ 1L);
        long g167 = (x1_1 & g126);
        long g168 = (g166 & g165);
        long g169 = (g167 | g168);
        long g170 = (x1_2 ^ 1L);
        long g171 = (x1_2 & g97);
        long g172 = (g170 & g169);
        long g173 = (g171 | g172);
        long g174 = (g39 ^ 1L);
        long g175 = (x1_2 | g174);
        long g176 = (g175 ^ 1L);
        long g177 = (x1_3 ^ 1L);
        long g178 = (x1_3 & g176);
        long g179 = (g177 & g173);
        long g180 = (g178 | g179);
        long g181 = (g4 & g180);
        long g182 = (x1_0 ^ 1L);
        long g183 = (x1_0 & x0_11);
        long g184 = (g182 & x0_12);
        long g185 = (g183 | g184);
        long g186 = (x1_1 ^ 1L);
        long g187 = (x1_1 & g145);
        long g188 = (g186 & g185);
        long g189 = (g187 | g188);
        long g190 = (x1_2 ^ 1L);
        long g191 = (x1_2 & g111);
        long g192 = (g190 & g189);
        long g193 = (g191 | g192);
        long g194 = (x1_3 ^ 1L);
        long g195 = (x1_3 & g56);
        long g196 = (g194 & g193);
        long g197 = (g195 | g196);
        long g198 = (g4 & g197);
        long g199 = (x1_0 ^ 1L);
        long g200 = (x1_0 & x0_12);
        long g201 = (g199 & x0_13);
        long g202 = (g200 | g201);
        long g203 = (x1_1 ^ 1L);
        long g204 = (x1_1 & g165);
        long g205 = (g203 & g202);
        long g206 = (g204 | g205);
        long g207 = (x1_2 ^ 1L);
        long g208 = (x1_2 & g130);
        long g209 = (g207 & g206);
        long g210 = (g208 | g209);
        long g211 = (x1_3 ^ 1L);
        long g212 = (x1_3 & g73);
        long g213 = (g211 & g210);
        long g214 = (g212 | g213);
        long g215 = (g4 & g214);
        long g216 = (x1_0 ^ 1L);
        long g217 = (x1_0 & x0_13);
        long g218 = (g216 & x0_14);
        long g219 = (g217 | g218);
        long g220 = (x1_1 ^ 1L);
        long g221 = (x1_1 & g185);
        long g222 = (g220 & g219);
        long g223 = (g221 | g222);
        long g224 = (x1_2 ^ 1L);
        long g225 = (x1_2 & g149);
        long g226 = (g224 & g223);
        long g227 = (g225 | g226);
        long g228 = (x1_3 ^ 1L);
        long g229 = (x1_3 & g87);
        long g230 = (g228 & g227);
        long g231 = (g229 | g230);
        long g232 = (g4 & g231);
        long g233 = (x1_0 ^ 1L);
        long g234 = (x1_0 & x0_14);
        long g235 = (g233 & x0_15);
        long g236 = (g234 | g235);
        long g237 = (x1_1 ^ 1L);
        long g238 = (x1_1 & g202);
        long g239 = (g237 & g236);
        long g240 = (g238 | g239);
        long g241 = (x1_2 ^ 1L);
        long g242 = (x1_2 & g169);
        long g243 = (g241 & g240);
        long g244 = (g242 | g243);
        long g245 = (x1_3 ^ 1L);
        long g246 = (x1_3 & g101);
        long g247 = (g245 & g244);
        long g248 = (g246 | g247);
        long g249 = (g4 & g248);
        long g250 = (x1_0 ^ 1L);
        long g251 = (x1_0 & x0_15);
        long g252 = (g250 & x0_16);
        long g253 = (g251 | g252);
        long g254 = (x1_1 ^ 1L);
        long g255 = (x1_1 & g219);
        long g256 = (g254 & g253);
        long g257 = (g255 | g256);
        long g258 = (x1_2 ^ 1L);
        long g259 = (x1_2 & g189);
        long g260 = (g258 & g257);
        long g261 = (g259 | g260);
        long g262 = (x1_3 ^ 1L);
        long g263 = (x1_3 & g115);
        long g264 = (g262 & g261);
        long g265 = (g263 | g264);
        long g266 = (x1_3 | g116);
        long g267 = (g266 ^ 1L);
        long g268 = (x1_4 ^ 1L);
        long g269 = (x1_4 & g267);
        long g270 = (g268 & g265);
        long g271 = (g269 | g270);
        long g272 = (x1_0 ^ 1L);
        long g273 = (x1_0 & x0_16);
        long g274 = (g272 & x0_17);
        long g275 = (g273 | g274);
        long g276 = (x1_1 ^ 1L);
        long g277 = (x1_1 & g236);
        long g278 = (g276 & g275);
        long g279 = (g277 | g278);
        long g280 = (x1_2 ^ 1L);
        long g281 = (x1_2 & g206);
        long g282 = (g280 & g279);
        long g283 = (g281 | g282);
        long g284 = (x1_3 ^ 1L);
        long g285 = (x1_3 & g134);
        long g286 = (g284 & g283);
        long g287 = (g285 | g286);
        long g288 = (x1_3 | g135);
        long g289 = (g288 ^ 1L);
        long g290 = (x1_4 ^ 1L);
        long g291 = (x1_4 & g289);
        long g292 = (g290 & g287);
        long g293 = (g291 | g292);
        long g294 = (x1_0 ^ 1L);
        long g295 = (x1_0 & x0_17);
        long g296 = (g294 & x0_18);
        long g297 = (g295 | g296);
        long g298 = (x1_1 ^ 1L);
        long g299 = (x1_1 & g253);
        long g300 = (g298 & g297);
        long g301 = (g299 | g300);
        long g302 = (x1_2 ^ 1L);
        long g303 = (x1_2 & g223);
        long g304 = (g302 & g301);
        long g305 = (g303 | g304);
        long g306 = (x1_3 ^ 1L);
        long g307 = (x1_3 & g153);
        long g308 = (g306 & g305);
        long g309 = (g307 | g308);
        long g310 = (x1_3 | g155);
        long g311 = (g310 ^ 1L);
        long g312 = (x1_4 ^ 1L);
        long g313 = (x1_4 & g311);
        long g314 = (g312 & g309);
        long g315 = (g313 | g314);
        long g316 = (x1_0 ^ 1L);
        long g317 = (x1_0 & x0_18);
        long g318 = (g316 & x0_19);
        long g319 = (g317 | g318);
        long g320 = (x1_1 ^ 1L);
        long g321 = (x1_1 & g275);
        long g322 = (g320 & g319);
        long g323 = (g321 | g322);
        long g324 = (x1_2 ^ 1L);
        long g325 = (x1_2 & g240);
        long g326 = (g324 & g323);
        long g327 = (g325 | g326);
        long g328 = (x1_3 ^ 1L);
        long g329 = (x1_3 & g173);
        long g330 = (g328 & g327);
        long g331 = (g329 | g330);
        long g332 = (x1_3 | g175);
        long g333 = (g332 ^ 1L);
        long g334 = (x1_4 ^ 1L);
        long g335 = (x1_4 & g333);
        long g336 = (g334 & g331);
        long g337 = (g335 | g336);
        long g338 = (x1_0 ^ 1L);
        long g339 = (x1_0 & x0_19);
        long g340 = (g338 & x0_20);
        long g341 = (g339 | g340);
        long g342 = (x1_1 ^ 1L);
        long g343 = (x1_1 & g297);
        long g344 = (g342 & g341);
        long g345 = (g343 | g344);
        long g346 = (x1_2 ^ 1L);
        long g347 = (x1_2 & g257);
        long g348 = (g346 & g345);
        long g349 = (g347 | g348);
        long g350 = (x1_3 ^ 1L);
        long g351 = (x1_3 & g193);
        long g352 = (g350 & g349);
        long g353 = (g351 | g352);
        long g354 = (g56 ^ 1L);
        long g355 = (x1_3 | g354);
        long g356 = (g355 ^ 1L);
        long g357 = (x1_4 ^ 1L);
        long g358 = (x1_4 & g356);
        long g359 = (g357 & g353);
        long g360 = (g358 | g359);
        long g361 = (x1_0 ^ 1L);
        long g362 = (x1_0 & x0_20);
        long g363 = (g361 & x0_21);
        long g364 = (g362 | g363);
        long g365 = (x1_1 ^ 1L);
        long g366 = (x1_1 & g319);
        long g367 = (g365 & g364);
        long g368 = (g366 | g367);
        long g369 = (x1_2 ^ 1L);
        long g370 = (x1_2 & g279);
        long g371 = (g369 & g368);
        long g372 = (g370 | g371);
        long g373 = (x1_3 ^ 1L);
        long g374 = (x1_3 & g210);
        long g375 = (g373 & g372);
        long g376 = (g374 | g375);
        long g377 = (g73 ^ 1L);
        long g378 = (x1_3 | g377);
        long g379 = (g378 ^ 1L);
        long g380 = (x1_4 ^ 1L);
        long g381 = (x1_4 & g379);
        long g382 = (g380 & g376);
        long g383 = (g381 | g382);
        long g384 = (x1_0 ^ 1L);
        long g385 = (x1_0 & x0_21);
        long g386 = (g384 & x0_22);
        long g387 = (g385 | g386);
        long g388 = (x1_1 ^ 1L);
        long g389 = (x1_1 & g341);
        long g390 = (g388 & g387);
        long g391 = (g389 | g390);
        long g392 = (x1_2 ^ 1L);
        long g393 = (x1_2 & g301);
        long g394 = (g392 & g391);
        long g395 = (g393 | g394);
        long g396 = (x1_3 ^ 1L);
        long g397 = (x1_3 & g227);
        long g398 = (g396 & g395);
        long g399 = (g397 | g398);
        long g400 = (g87 ^ 1L);
        long g401 = (x1_3 | g400);
        long g402 = (g401 ^ 1L);
        long g403 = (x1_4 ^ 1L);
        long g404 = (x1_4 & g402);
        long g405 = (g403 & g399);
        long g406 = (g404 | g405);
        long g407 = (x1_0 ^ 1L);
        long g408 = (x1_0 & x0_22);
        long g409 = (g407 & x0_23);
        long g410 = (g408 | g409);
        long g411 = (x1_1 ^ 1L);
        long g412 = (x1_1 & g364);
        long g413 = (g411 & g410);
        long g414 = (g412 | g413);
        long g415 = (x1_2 ^ 1L);
        long g416 = (x1_2 & g323);
        long g417 = (g415 & g414);
        long g418 = (g416 | g417);
        long g419 = (x1_3 ^ 1L);
        long g420 = (x1_3 & g244);
        long g421 = (g419 & g418);
        long g422 = (g420 | g421);
        long g423 = (g101 ^ 1L);
        long g424 = (x1_3 | g423);
        long g425 = (g424 ^ 1L);
        long g426 = (x1_4 ^ 1L);
        long g427 = (x1_4 & g425);
        long g428 = (g426 & g422);
        long g429 = (g427 | g428);
        long g430 = (x1_0 ^ 1L);
        long g431 = (x1_0 & x0_23);
        long g432 = (g430 & x0_24);
        long g433 = (g431 | g432);
        long g434 = (x1_1 ^ 1L);
        long g435 = (x1_1 & g387);
        long g436 = (g434 & g433);
        long g437 = (g435 | g436);
        long g438 = (x1_2 ^ 1L);
        long g439 = (x1_2 & g345);
        long g440 = (g438 & g437);
        long g441 = (g439 | g440);
        long g442 = (x1_3 ^ 1L);
        long g443 = (x1_3 & g261);
        long g444 = (g442 & g441);
        long g445 = (g443 | g444);
        long g446 = (x1_4 ^ 1L);
        long g447 = (x1_4 & g121);
        long g448 = (g446 & g445);
        long g449 = (g447 | g448);
        long g450 = (x1_0 ^ 1L);
        long g451 = (x1_0 & x0_24);
        long g452 = (g450 & x0_25);
        long g453 = (g451 | g452);
        long g454 = (x1_1 ^ 1L);
        long g455 = (x1_1 & g410);
        long g456 = (g454 & g453);
        long g457 = (g455 | g456);
        long g458 = (x1_2 ^ 1L);
        long g459 = (x1_2 & g368);
        long g460 = (g458 & g457);
        long g461 = (g459 | g460);
        long g462 = (x1_3 ^ 1L);
        long g463 = (x1_3 & g283);
        long g464 = (g462 & g461);
        long g465 = (g463 | g464);
        long g466 = (x1_4 ^ 1L);
        long g467 = (x1_4 & g140);
        long g468 = (g466 & g465);
        long g469 = (g467 | g468);
        long g470 = (x1_0 ^ 1L);
        long g471 = (x1_0 & x0_25);
        long g472 = (g470 & x0_26);
        long g473 = (g471 | g472);
        long g474 = (x1_1 ^ 1L);
        long g475 = (x1_1 & g433);
        long g476 = (g474 & g473);
        long g477 = (g475 | g476);
        long g478 = (x1_2 ^ 1L);
        long g479 = (x1_2 & g391);
        long g480 = (g478 & g477);
        long g481 = (g479 | g480);
        long g482 = (x1_3 ^ 1L);
        long g483 = (x1_3 & g305);
        long g484 = (g482 & g481);
        long g485 = (g483 | g484);
        long g486 = (x1_4 ^ 1L);
        long g487 = (x1_4 & g160);
        long g488 = (g486 & g485);
        long g489 = (g487 | g488);
        long g490 = (x1_0 ^ 1L);
        long g491 = (x1_0 & x0_26);
        long g492 = (g490 & x0_27);
        long g493 = (g491 | g492);
        long g494 = (x1_1 ^ 1L);
        long g495 = (x1_1 & g453);
        long g496 = (g494 & g493);
        long g497 = (g495 | g496);
        long g498 = (x1_2 ^ 1L);
        long g499 = (x1_2 & g414);
        long g500 = (g498 & g497);
        long g501 = (g499 | g500);
        long g502 = (x1_3 ^ 1L);
        long g503 = (x1_3 & g327);
        long g504 = (g502 & g501);
        long g505 = (g503 | g504);
        long g506 = (x1_4 ^ 1L);
        long g507 = (x1_4 & g180);
        long g508 = (g506 & g505);
        long g509 = (g507 | g508);
        long g510 = (x1_0 ^ 1L);
        long g511 = (x1_0 & x0_27);
        long g512 = (g510 & x0_28);
        long g513 = (g511 | g512);
        long g514 = (x1_1 ^ 1L);
        long g515 = (x1_1 & g473);
        long g516 = (g514 & g513);
        long g517 = (g515 | g516);
        long g518 = (x1_2 ^ 1L);
        long g519 = (x1_2 & g437);
        long g520 = (g518 & g517);
        long g521 = (g519 | g520);
        long g522 = (x1_3 ^ 1L);
        long g523 = (x1_3 & g349);
        long g524 = (g522 & g521);
        long g525 = (g523 | g524);
        long g526 = (x1_4 ^ 1L);
        long g527 = (x1_4 & g197);
        long g528 = (g526 & g525);
        long g529 = (g527 | g528);
        long g530 = (x1_0 ^ 1L);
        long g531 = (x1_0 & x0_28);
        long g532 = (g530 & x0_29);
        long g533 = (g531 | g532);
        long g534 = (x1_1 ^ 1L);
        long g535 = (x1_1 & g493);
        long g536 = (g534 & g533);
        long g537 = (g535 | g536);
        long g538 = (x1_2 ^ 1L);
        long g539 = (x1_2 & g457);
        long g540 = (g538 & g537);
        long g541 = (g539 | g540);
        long g542 = (x1_3 ^ 1L);
        long g543 = (x1_3 & g372);
        long g544 = (g542 & g541);
        long g545 = (g543 | g544);
        long g546 = (x1_4 ^ 1L);
        long g547 = (x1_4 & g214);
        long g548 = (g546 & g545);
        long g549 = (g547 | g548);
        long g550 = (x1_0 ^ 1L);
        long g551 = (x1_0 & x0_29);
        long g552 = (g550 & x0_30);
        long g553 = (g551 | g552);
        long g554 = (x1_1 ^ 1L);
        long g555 = (x1_1 & g513);
        long g556 = (g554 & g553);
        long g557 = (g555 | g556);
        long g558 = (x1_2 ^ 1L);
        long g559 = (x1_2 & g477);
        long g560 = (g558 & g557);
        long g561 = (g559 | g560);
        long g562 = (x1_3 ^ 1L);
        long g563 = (x1_3 & g395);
        long g564 = (g562 & g561);
        long g565 = (g563 | g564);
        long g566 = (x1_4 ^ 1L);
        long g567 = (x1_4 & g231);
        long g568 = (g566 & g565);
        long g569 = (g567 | g568);
        long g570 = (x1_0 ^ 1L);
        long g571 = (x1_0 & x0_30);
        long g572 = (g570 & x0_31);
        long g573 = (g571 | g572);
        long g574 = (x1_1 ^ 1L);
        long g575 = (x1_1 & g533);
        long g576 = (g574 & g573);
        long g577 = (g575 | g576);
        long g578 = (x1_2 ^ 1L);
        long g579 = (x1_2 & g497);
        long g580 = (g578 & g577);
        long g581 = (g579 | g580);
        long g582 = (x1_3 ^ 1L);
        long g583 = (x1_3 & g418);
        long g584 = (g582 & g581);
        long g585 = (g583 | g584);
        long g586 = (x1_4 ^ 1L);
        long g587 = (x1_4 & g248);
        long g588 = (g586 & g585);
        long g589 = (g587 | g588);
        long k0 = 0L;
        long w0 = k0;
        long w1 = cat(w0, k0, 1);
        long w2 = cat(w1, k0, 1);
        long w3 = cat(w2, k0, 1);
        long w4 = cat(w3, k0, 1);
        long w5 = cat(w4, k0, 1);
        long w6 = cat(w5, k0, 1);
        long w7 = cat(w6, k0, 1);
        long w8 = cat(w7, k0, 1);
        long w9 = cat(w8, k0, 1);
        long w10 = cat(w9, k0, 1);
        long w11 = cat(w10, k0, 1);
        long w12 = cat(w11, k0, 1);
        long w13 = cat(w12, k0, 1);
        long w14 = cat(w13, k0, 1);
        long w15 = cat(w14, k0, 1);
        long w16 = cat(w15, k0, 1);
        long w17 = cat(w16, k0, 1);
        long w18 = cat(w17, k0, 1);
        long w19 = cat(w18, k0, 1);
        long w20 = cat(w19, k0, 1);
        long w21 = cat(w20, k0, 1);
        long w22 = cat(w21, k0, 1);
        long w23 = cat(w22, k0, 1);
        long w24 = cat(w23, k0, 1);
        long w25 = cat(w24, k0, 1);
        long w26 = cat(w25, k0, 1);
        long w27 = cat(w26, k0, 1);
        long w28 = cat(w27, k0, 1);
        long w29 = cat(w28, k0, 1);
        long w30 = cat(w29, k0, 1);
        long w31 = cat(w30, k0, 1);
        long w32 = cat(w31, g589, 1);
        long w33 = cat(w32, g569, 1);
        long w34 = cat(w33, g549, 1);
        long w35 = cat(w34, g529, 1);
        long w36 = cat(w35, g509, 1);
        long w37 = cat(w36, g489, 1);
        long w38 = cat(w37, g469, 1);
        long w39 = cat(w38, g449, 1);
        long w40 = cat(w39, g429, 1);
        long w41 = cat(w40, g406, 1);
        long w42 = cat(w41, g383, 1);
        long w43 = cat(w42, g360, 1);
        long w44 = cat(w43, g337, 1);
        long w45 = cat(w44, g315, 1);
        long w46 = cat(w45, g293, 1);
        long w47 = cat(w46, g271, 1);
        long w48 = cat(w47, g249, 1);
        long w49 = cat(w48, g232, 1);
        long w50 = cat(w49, g215, 1);
        long w51 = cat(w50, g198, 1);
        long w52 = cat(w51, g181, 1);
        long w53 = cat(w52, g161, 1);
        long w54 = cat(w53, g141, 1);
        long w55 = cat(w54, g122, 1);
        long w56 = cat(w55, g103, 1);
        long w57 = cat(w56, g89, 1);
        long w58 = cat(w57, g75, 1);
        long w59 = cat(w58, g58, 1);
        long w60 = cat(w59, g42, 1);
        long w61 = cat(w60, g31, 1);
        long w62 = cat(w61, g17, 1);
        long w63 = cat(w62, g9, 1);
        return m(w63, 64);
    }


    public static void Main() {
        StringBuilder answers = new StringBuilder();
        string line = Console.ReadLine();
        while (line != null) {
            string text = line.Trim();
            if (text.Length != 0) {
                string[] parts = text.Split((char[]) null,
                    StringSplitOptions.RemoveEmptyEntries);
                long[] values = new long[parts.Length];
                for (int i = 0; i < parts.Length; i++) {
                    values[i] = unchecked((long) ulong.Parse(parts[i]));
                }
                try {
                    answers.Append(((ulong) emu_shl_cl_gpr_32__reg_rdi__csharp(values[0], values[1])).ToString());
                    answers.Append("\n");
                } catch (Exception problem) {
                    answers.Append("RAISE:");
                    answers.Append(problem.GetType().Name);
                    answers.Append("\n");
                }
            }
            line = Console.ReadLine();
        }
        Console.Write(answers.ToString());
    }
}
