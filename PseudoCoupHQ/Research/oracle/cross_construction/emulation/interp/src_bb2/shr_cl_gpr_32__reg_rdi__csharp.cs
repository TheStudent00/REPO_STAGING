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
    // one named local per gate, over the term of shr_cl_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, LShR(Extract(31, 0, v0), Concat(0, Extract(4, 0, v1))))
    public static long emu_shr_cl_gpr_32__reg_rdi__csharp(long a, long b) {
        long x0_0 = ext(a, 0, 0);
        long x0_1 = ext(a, 1, 1);
        long x1_0 = ext(b, 0, 0);
        long x0_2 = ext(a, 2, 2);
        long x0_3 = ext(a, 3, 3);
        long x1_1 = ext(b, 1, 1);
        long x0_4 = ext(a, 4, 4);
        long x0_5 = ext(a, 5, 5);
        long x0_6 = ext(a, 6, 6);
        long x0_7 = ext(a, 7, 7);
        long x1_2 = ext(b, 2, 2);
        long x0_8 = ext(a, 8, 8);
        long x0_9 = ext(a, 9, 9);
        long x0_10 = ext(a, 10, 10);
        long x0_11 = ext(a, 11, 11);
        long x0_12 = ext(a, 12, 12);
        long x0_13 = ext(a, 13, 13);
        long x0_14 = ext(a, 14, 14);
        long x0_15 = ext(a, 15, 15);
        long x1_3 = ext(b, 3, 3);
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
        long x1_4 = ext(b, 4, 4);
        long g0 = (x1_0 ^ 1L);
        long g1 = (x1_0 & x0_1);
        long g2 = (g0 & x0_0);
        long g3 = (g1 | g2);
        long g4 = (x1_0 ^ 1L);
        long g5 = (x1_0 & x0_3);
        long g6 = (g4 & x0_2);
        long g7 = (g5 | g6);
        long g8 = (x1_1 ^ 1L);
        long g9 = (x1_1 & g7);
        long g10 = (g8 & g3);
        long g11 = (g9 | g10);
        long g12 = (x1_0 ^ 1L);
        long g13 = (x1_0 & x0_5);
        long g14 = (g12 & x0_4);
        long g15 = (g13 | g14);
        long g16 = (x1_0 ^ 1L);
        long g17 = (x1_0 & x0_7);
        long g18 = (g16 & x0_6);
        long g19 = (g17 | g18);
        long g20 = (x1_1 ^ 1L);
        long g21 = (x1_1 & g19);
        long g22 = (g20 & g15);
        long g23 = (g21 | g22);
        long g24 = (x1_2 ^ 1L);
        long g25 = (x1_2 & g23);
        long g26 = (g24 & g11);
        long g27 = (g25 | g26);
        long g28 = (x1_0 ^ 1L);
        long g29 = (x1_0 & x0_9);
        long g30 = (g28 & x0_8);
        long g31 = (g29 | g30);
        long g32 = (x1_0 ^ 1L);
        long g33 = (x1_0 & x0_11);
        long g34 = (g32 & x0_10);
        long g35 = (g33 | g34);
        long g36 = (x1_1 ^ 1L);
        long g37 = (x1_1 & g35);
        long g38 = (g36 & g31);
        long g39 = (g37 | g38);
        long g40 = (x1_0 ^ 1L);
        long g41 = (x1_0 & x0_13);
        long g42 = (g40 & x0_12);
        long g43 = (g41 | g42);
        long g44 = (x1_0 ^ 1L);
        long g45 = (x1_0 & x0_15);
        long g46 = (g44 & x0_14);
        long g47 = (g45 | g46);
        long g48 = (x1_1 ^ 1L);
        long g49 = (x1_1 & g47);
        long g50 = (g48 & g43);
        long g51 = (g49 | g50);
        long g52 = (x1_2 ^ 1L);
        long g53 = (x1_2 & g51);
        long g54 = (g52 & g39);
        long g55 = (g53 | g54);
        long g56 = (x1_3 ^ 1L);
        long g57 = (x1_3 & g55);
        long g58 = (g56 & g27);
        long g59 = (g57 | g58);
        long g60 = (x1_0 ^ 1L);
        long g61 = (x1_0 & x0_17);
        long g62 = (g60 & x0_16);
        long g63 = (g61 | g62);
        long g64 = (x1_0 ^ 1L);
        long g65 = (x1_0 & x0_19);
        long g66 = (g64 & x0_18);
        long g67 = (g65 | g66);
        long g68 = (x1_1 ^ 1L);
        long g69 = (x1_1 & g67);
        long g70 = (g68 & g63);
        long g71 = (g69 | g70);
        long g72 = (x1_0 ^ 1L);
        long g73 = (x1_0 & x0_21);
        long g74 = (g72 & x0_20);
        long g75 = (g73 | g74);
        long g76 = (x1_0 ^ 1L);
        long g77 = (x1_0 & x0_23);
        long g78 = (g76 & x0_22);
        long g79 = (g77 | g78);
        long g80 = (x1_1 ^ 1L);
        long g81 = (x1_1 & g79);
        long g82 = (g80 & g75);
        long g83 = (g81 | g82);
        long g84 = (x1_2 ^ 1L);
        long g85 = (x1_2 & g83);
        long g86 = (g84 & g71);
        long g87 = (g85 | g86);
        long g88 = (x1_0 ^ 1L);
        long g89 = (x1_0 & x0_25);
        long g90 = (g88 & x0_24);
        long g91 = (g89 | g90);
        long g92 = (x1_0 ^ 1L);
        long g93 = (x1_0 & x0_27);
        long g94 = (g92 & x0_26);
        long g95 = (g93 | g94);
        long g96 = (x1_1 ^ 1L);
        long g97 = (x1_1 & g95);
        long g98 = (g96 & g91);
        long g99 = (g97 | g98);
        long g100 = (x1_0 ^ 1L);
        long g101 = (x1_0 & x0_29);
        long g102 = (g100 & x0_28);
        long g103 = (g101 | g102);
        long g104 = (x1_0 ^ 1L);
        long g105 = (x1_0 & x0_31);
        long g106 = (g104 & x0_30);
        long g107 = (g105 | g106);
        long g108 = (x1_1 ^ 1L);
        long g109 = (x1_1 & g107);
        long g110 = (g108 & g103);
        long g111 = (g109 | g110);
        long g112 = (x1_2 ^ 1L);
        long g113 = (x1_2 & g111);
        long g114 = (g112 & g99);
        long g115 = (g113 | g114);
        long g116 = (x1_3 ^ 1L);
        long g117 = (x1_3 & g115);
        long g118 = (g116 & g87);
        long g119 = (g117 | g118);
        long g120 = (x1_4 ^ 1L);
        long g121 = (x1_4 & g119);
        long g122 = (g120 & g59);
        long g123 = (g121 | g122);
        long g124 = (x1_0 ^ 1L);
        long g125 = (x1_0 & x0_2);
        long g126 = (g124 & x0_1);
        long g127 = (g125 | g126);
        long g128 = (x1_0 ^ 1L);
        long g129 = (x1_0 & x0_4);
        long g130 = (g128 & x0_3);
        long g131 = (g129 | g130);
        long g132 = (x1_1 ^ 1L);
        long g133 = (x1_1 & g131);
        long g134 = (g132 & g127);
        long g135 = (g133 | g134);
        long g136 = (x1_0 ^ 1L);
        long g137 = (x1_0 & x0_6);
        long g138 = (g136 & x0_5);
        long g139 = (g137 | g138);
        long g140 = (x1_0 ^ 1L);
        long g141 = (x1_0 & x0_8);
        long g142 = (g140 & x0_7);
        long g143 = (g141 | g142);
        long g144 = (x1_1 ^ 1L);
        long g145 = (x1_1 & g143);
        long g146 = (g144 & g139);
        long g147 = (g145 | g146);
        long g148 = (x1_2 ^ 1L);
        long g149 = (x1_2 & g147);
        long g150 = (g148 & g135);
        long g151 = (g149 | g150);
        long g152 = (x1_0 ^ 1L);
        long g153 = (x1_0 & x0_10);
        long g154 = (g152 & x0_9);
        long g155 = (g153 | g154);
        long g156 = (x1_0 ^ 1L);
        long g157 = (x1_0 & x0_12);
        long g158 = (g156 & x0_11);
        long g159 = (g157 | g158);
        long g160 = (x1_1 ^ 1L);
        long g161 = (x1_1 & g159);
        long g162 = (g160 & g155);
        long g163 = (g161 | g162);
        long g164 = (x1_0 ^ 1L);
        long g165 = (x1_0 & x0_14);
        long g166 = (g164 & x0_13);
        long g167 = (g165 | g166);
        long g168 = (x1_0 ^ 1L);
        long g169 = (x1_0 & x0_16);
        long g170 = (g168 & x0_15);
        long g171 = (g169 | g170);
        long g172 = (x1_1 ^ 1L);
        long g173 = (x1_1 & g171);
        long g174 = (g172 & g167);
        long g175 = (g173 | g174);
        long g176 = (x1_2 ^ 1L);
        long g177 = (x1_2 & g175);
        long g178 = (g176 & g163);
        long g179 = (g177 | g178);
        long g180 = (x1_3 ^ 1L);
        long g181 = (x1_3 & g179);
        long g182 = (g180 & g151);
        long g183 = (g181 | g182);
        long g184 = (x1_0 ^ 1L);
        long g185 = (x1_0 & x0_18);
        long g186 = (g184 & x0_17);
        long g187 = (g185 | g186);
        long g188 = (x1_0 ^ 1L);
        long g189 = (x1_0 & x0_20);
        long g190 = (g188 & x0_19);
        long g191 = (g189 | g190);
        long g192 = (x1_1 ^ 1L);
        long g193 = (x1_1 & g191);
        long g194 = (g192 & g187);
        long g195 = (g193 | g194);
        long g196 = (x1_0 ^ 1L);
        long g197 = (x1_0 & x0_22);
        long g198 = (g196 & x0_21);
        long g199 = (g197 | g198);
        long g200 = (x1_0 ^ 1L);
        long g201 = (x1_0 & x0_24);
        long g202 = (g200 & x0_23);
        long g203 = (g201 | g202);
        long g204 = (x1_1 ^ 1L);
        long g205 = (x1_1 & g203);
        long g206 = (g204 & g199);
        long g207 = (g205 | g206);
        long g208 = (x1_2 ^ 1L);
        long g209 = (x1_2 & g207);
        long g210 = (g208 & g195);
        long g211 = (g209 | g210);
        long g212 = (x1_0 ^ 1L);
        long g213 = (x1_0 & x0_26);
        long g214 = (g212 & x0_25);
        long g215 = (g213 | g214);
        long g216 = (x1_0 ^ 1L);
        long g217 = (x1_0 & x0_28);
        long g218 = (g216 & x0_27);
        long g219 = (g217 | g218);
        long g220 = (x1_1 ^ 1L);
        long g221 = (x1_1 & g219);
        long g222 = (g220 & g215);
        long g223 = (g221 | g222);
        long g224 = (x1_0 ^ 1L);
        long g225 = (x1_0 & x0_30);
        long g226 = (g224 & x0_29);
        long g227 = (g225 | g226);
        long g228 = (x0_31 ^ 1L);
        long g229 = (x1_0 | g228);
        long g230 = (g229 ^ 1L);
        long g231 = (x1_1 ^ 1L);
        long g232 = (x1_1 & g230);
        long g233 = (g231 & g227);
        long g234 = (g232 | g233);
        long g235 = (x1_2 ^ 1L);
        long g236 = (x1_2 & g234);
        long g237 = (g235 & g223);
        long g238 = (g236 | g237);
        long g239 = (x1_3 ^ 1L);
        long g240 = (x1_3 & g238);
        long g241 = (g239 & g211);
        long g242 = (g240 | g241);
        long g243 = (x1_4 ^ 1L);
        long g244 = (x1_4 & g242);
        long g245 = (g243 & g183);
        long g246 = (g244 | g245);
        long g247 = (x1_1 ^ 1L);
        long g248 = (x1_1 & g15);
        long g249 = (g247 & g7);
        long g250 = (g248 | g249);
        long g251 = (x1_1 ^ 1L);
        long g252 = (x1_1 & g31);
        long g253 = (g251 & g19);
        long g254 = (g252 | g253);
        long g255 = (x1_2 ^ 1L);
        long g256 = (x1_2 & g254);
        long g257 = (g255 & g250);
        long g258 = (g256 | g257);
        long g259 = (x1_1 ^ 1L);
        long g260 = (x1_1 & g43);
        long g261 = (g259 & g35);
        long g262 = (g260 | g261);
        long g263 = (x1_1 ^ 1L);
        long g264 = (x1_1 & g63);
        long g265 = (g263 & g47);
        long g266 = (g264 | g265);
        long g267 = (x1_2 ^ 1L);
        long g268 = (x1_2 & g266);
        long g269 = (g267 & g262);
        long g270 = (g268 | g269);
        long g271 = (x1_3 ^ 1L);
        long g272 = (x1_3 & g270);
        long g273 = (g271 & g258);
        long g274 = (g272 | g273);
        long g275 = (x1_1 ^ 1L);
        long g276 = (x1_1 & g75);
        long g277 = (g275 & g67);
        long g278 = (g276 | g277);
        long g279 = (x1_1 ^ 1L);
        long g280 = (x1_1 & g91);
        long g281 = (g279 & g79);
        long g282 = (g280 | g281);
        long g283 = (x1_2 ^ 1L);
        long g284 = (x1_2 & g282);
        long g285 = (g283 & g278);
        long g286 = (g284 | g285);
        long g287 = (x1_1 ^ 1L);
        long g288 = (x1_1 & g103);
        long g289 = (g287 & g95);
        long g290 = (g288 | g289);
        long g291 = (g107 ^ 1L);
        long g292 = (x1_1 | g291);
        long g293 = (g292 ^ 1L);
        long g294 = (x1_2 ^ 1L);
        long g295 = (x1_2 & g293);
        long g296 = (g294 & g290);
        long g297 = (g295 | g296);
        long g298 = (x1_3 ^ 1L);
        long g299 = (x1_3 & g297);
        long g300 = (g298 & g286);
        long g301 = (g299 | g300);
        long g302 = (x1_4 ^ 1L);
        long g303 = (x1_4 & g301);
        long g304 = (g302 & g274);
        long g305 = (g303 | g304);
        long g306 = (x1_1 ^ 1L);
        long g307 = (x1_1 & g139);
        long g308 = (g306 & g131);
        long g309 = (g307 | g308);
        long g310 = (x1_1 ^ 1L);
        long g311 = (x1_1 & g155);
        long g312 = (g310 & g143);
        long g313 = (g311 | g312);
        long g314 = (x1_2 ^ 1L);
        long g315 = (x1_2 & g313);
        long g316 = (g314 & g309);
        long g317 = (g315 | g316);
        long g318 = (x1_1 ^ 1L);
        long g319 = (x1_1 & g167);
        long g320 = (g318 & g159);
        long g321 = (g319 | g320);
        long g322 = (x1_1 ^ 1L);
        long g323 = (x1_1 & g187);
        long g324 = (g322 & g171);
        long g325 = (g323 | g324);
        long g326 = (x1_2 ^ 1L);
        long g327 = (x1_2 & g325);
        long g328 = (g326 & g321);
        long g329 = (g327 | g328);
        long g330 = (x1_3 ^ 1L);
        long g331 = (x1_3 & g329);
        long g332 = (g330 & g317);
        long g333 = (g331 | g332);
        long g334 = (x1_1 ^ 1L);
        long g335 = (x1_1 & g199);
        long g336 = (g334 & g191);
        long g337 = (g335 | g336);
        long g338 = (x1_1 ^ 1L);
        long g339 = (x1_1 & g215);
        long g340 = (g338 & g203);
        long g341 = (g339 | g340);
        long g342 = (x1_2 ^ 1L);
        long g343 = (x1_2 & g341);
        long g344 = (g342 & g337);
        long g345 = (g343 | g344);
        long g346 = (x1_1 ^ 1L);
        long g347 = (x1_1 & g227);
        long g348 = (g346 & g219);
        long g349 = (g347 | g348);
        long g350 = (x1_1 | g229);
        long g351 = (g350 ^ 1L);
        long g352 = (x1_2 ^ 1L);
        long g353 = (x1_2 & g351);
        long g354 = (g352 & g349);
        long g355 = (g353 | g354);
        long g356 = (x1_3 ^ 1L);
        long g357 = (x1_3 & g355);
        long g358 = (g356 & g345);
        long g359 = (g357 | g358);
        long g360 = (x1_4 ^ 1L);
        long g361 = (x1_4 & g359);
        long g362 = (g360 & g333);
        long g363 = (g361 | g362);
        long g364 = (x1_2 ^ 1L);
        long g365 = (x1_2 & g39);
        long g366 = (g364 & g23);
        long g367 = (g365 | g366);
        long g368 = (x1_2 ^ 1L);
        long g369 = (x1_2 & g71);
        long g370 = (g368 & g51);
        long g371 = (g369 | g370);
        long g372 = (x1_3 ^ 1L);
        long g373 = (x1_3 & g371);
        long g374 = (g372 & g367);
        long g375 = (g373 | g374);
        long g376 = (x1_2 ^ 1L);
        long g377 = (x1_2 & g99);
        long g378 = (g376 & g83);
        long g379 = (g377 | g378);
        long g380 = (g111 ^ 1L);
        long g381 = (x1_2 | g380);
        long g382 = (g381 ^ 1L);
        long g383 = (x1_3 ^ 1L);
        long g384 = (x1_3 & g382);
        long g385 = (g383 & g379);
        long g386 = (g384 | g385);
        long g387 = (x1_4 ^ 1L);
        long g388 = (x1_4 & g386);
        long g389 = (g387 & g375);
        long g390 = (g388 | g389);
        long g391 = (x1_2 ^ 1L);
        long g392 = (x1_2 & g163);
        long g393 = (g391 & g147);
        long g394 = (g392 | g393);
        long g395 = (x1_2 ^ 1L);
        long g396 = (x1_2 & g195);
        long g397 = (g395 & g175);
        long g398 = (g396 | g397);
        long g399 = (x1_3 ^ 1L);
        long g400 = (x1_3 & g398);
        long g401 = (g399 & g394);
        long g402 = (g400 | g401);
        long g403 = (x1_2 ^ 1L);
        long g404 = (x1_2 & g223);
        long g405 = (g403 & g207);
        long g406 = (g404 | g405);
        long g407 = (g234 ^ 1L);
        long g408 = (x1_2 | g407);
        long g409 = (g408 ^ 1L);
        long g410 = (x1_3 ^ 1L);
        long g411 = (x1_3 & g409);
        long g412 = (g410 & g406);
        long g413 = (g411 | g412);
        long g414 = (x1_4 ^ 1L);
        long g415 = (x1_4 & g413);
        long g416 = (g414 & g402);
        long g417 = (g415 | g416);
        long g418 = (x1_2 ^ 1L);
        long g419 = (x1_2 & g262);
        long g420 = (g418 & g254);
        long g421 = (g419 | g420);
        long g422 = (x1_2 ^ 1L);
        long g423 = (x1_2 & g278);
        long g424 = (g422 & g266);
        long g425 = (g423 | g424);
        long g426 = (x1_3 ^ 1L);
        long g427 = (x1_3 & g425);
        long g428 = (g426 & g421);
        long g429 = (g427 | g428);
        long g430 = (x1_2 ^ 1L);
        long g431 = (x1_2 & g290);
        long g432 = (g430 & g282);
        long g433 = (g431 | g432);
        long g434 = (x1_2 | g292);
        long g435 = (g434 ^ 1L);
        long g436 = (x1_3 ^ 1L);
        long g437 = (x1_3 & g435);
        long g438 = (g436 & g433);
        long g439 = (g437 | g438);
        long g440 = (x1_4 ^ 1L);
        long g441 = (x1_4 & g439);
        long g442 = (g440 & g429);
        long g443 = (g441 | g442);
        long g444 = (x1_2 ^ 1L);
        long g445 = (x1_2 & g321);
        long g446 = (g444 & g313);
        long g447 = (g445 | g446);
        long g448 = (x1_2 ^ 1L);
        long g449 = (x1_2 & g337);
        long g450 = (g448 & g325);
        long g451 = (g449 | g450);
        long g452 = (x1_3 ^ 1L);
        long g453 = (x1_3 & g451);
        long g454 = (g452 & g447);
        long g455 = (g453 | g454);
        long g456 = (x1_2 ^ 1L);
        long g457 = (x1_2 & g349);
        long g458 = (g456 & g341);
        long g459 = (g457 | g458);
        long g460 = (x1_2 | g350);
        long g461 = (g460 ^ 1L);
        long g462 = (x1_3 ^ 1L);
        long g463 = (x1_3 & g461);
        long g464 = (g462 & g459);
        long g465 = (g463 | g464);
        long g466 = (x1_4 ^ 1L);
        long g467 = (x1_4 & g465);
        long g468 = (g466 & g455);
        long g469 = (g467 | g468);
        long g470 = (x1_3 ^ 1L);
        long g471 = (x1_3 & g87);
        long g472 = (g470 & g55);
        long g473 = (g471 | g472);
        long g474 = (g115 ^ 1L);
        long g475 = (x1_3 | g474);
        long g476 = (g475 ^ 1L);
        long g477 = (x1_4 ^ 1L);
        long g478 = (x1_4 & g476);
        long g479 = (g477 & g473);
        long g480 = (g478 | g479);
        long g481 = (x1_3 ^ 1L);
        long g482 = (x1_3 & g211);
        long g483 = (g481 & g179);
        long g484 = (g482 | g483);
        long g485 = (g238 ^ 1L);
        long g486 = (x1_3 | g485);
        long g487 = (g486 ^ 1L);
        long g488 = (x1_4 ^ 1L);
        long g489 = (x1_4 & g487);
        long g490 = (g488 & g484);
        long g491 = (g489 | g490);
        long g492 = (x1_3 ^ 1L);
        long g493 = (x1_3 & g286);
        long g494 = (g492 & g270);
        long g495 = (g493 | g494);
        long g496 = (g297 ^ 1L);
        long g497 = (x1_3 | g496);
        long g498 = (g497 ^ 1L);
        long g499 = (x1_4 ^ 1L);
        long g500 = (x1_4 & g498);
        long g501 = (g499 & g495);
        long g502 = (g500 | g501);
        long g503 = (x1_3 ^ 1L);
        long g504 = (x1_3 & g345);
        long g505 = (g503 & g329);
        long g506 = (g504 | g505);
        long g507 = (g355 ^ 1L);
        long g508 = (x1_3 | g507);
        long g509 = (g508 ^ 1L);
        long g510 = (x1_4 ^ 1L);
        long g511 = (x1_4 & g509);
        long g512 = (g510 & g506);
        long g513 = (g511 | g512);
        long g514 = (x1_3 ^ 1L);
        long g515 = (x1_3 & g379);
        long g516 = (g514 & g371);
        long g517 = (g515 | g516);
        long g518 = (x1_3 | g381);
        long g519 = (g518 ^ 1L);
        long g520 = (x1_4 ^ 1L);
        long g521 = (x1_4 & g519);
        long g522 = (g520 & g517);
        long g523 = (g521 | g522);
        long g524 = (x1_3 ^ 1L);
        long g525 = (x1_3 & g406);
        long g526 = (g524 & g398);
        long g527 = (g525 | g526);
        long g528 = (x1_3 | g408);
        long g529 = (g528 ^ 1L);
        long g530 = (x1_4 ^ 1L);
        long g531 = (x1_4 & g529);
        long g532 = (g530 & g527);
        long g533 = (g531 | g532);
        long g534 = (x1_3 ^ 1L);
        long g535 = (x1_3 & g433);
        long g536 = (g534 & g425);
        long g537 = (g535 | g536);
        long g538 = (x1_3 | g434);
        long g539 = (g538 ^ 1L);
        long g540 = (x1_4 ^ 1L);
        long g541 = (x1_4 & g539);
        long g542 = (g540 & g537);
        long g543 = (g541 | g542);
        long g544 = (x1_3 ^ 1L);
        long g545 = (x1_3 & g459);
        long g546 = (g544 & g451);
        long g547 = (g545 | g546);
        long g548 = (x1_3 | g460);
        long g549 = (g548 ^ 1L);
        long g550 = (x1_4 ^ 1L);
        long g551 = (x1_4 & g549);
        long g552 = (g550 & g547);
        long g553 = (g551 | g552);
        long g554 = (x1_4 ^ 1L);
        long g555 = (g554 & g119);
        long g556 = (g554 & g242);
        long g557 = (g554 & g301);
        long g558 = (g554 & g359);
        long g559 = (g554 & g386);
        long g560 = (g554 & g413);
        long g561 = (g554 & g439);
        long g562 = (g554 & g465);
        long g563 = (x1_3 ^ 1L);
        long g564 = (g554 & g563);
        long g565 = (g564 & g115);
        long g566 = (g554 & g563);
        long g567 = (g566 & g238);
        long g568 = (g554 & g563);
        long g569 = (g568 & g297);
        long g570 = (g554 & g563);
        long g571 = (g570 & g355);
        long g572 = (x1_2 ^ 1L);
        long g573 = (g554 & g563);
        long g574 = (g573 & g572);
        long g575 = (g574 & g111);
        long g576 = (g554 & g563);
        long g577 = (g576 & g572);
        long g578 = (g577 & g234);
        long g579 = (x1_1 ^ 1L);
        long g580 = (g554 & g563);
        long g581 = (g580 & g572);
        long g582 = (g581 & g579);
        long g583 = (g582 & g107);
        long g584 = (x1_0 ^ 1L);
        long g585 = (g554 & g563);
        long g586 = (g585 & g572);
        long g587 = (g586 & g579);
        long g588 = (g587 & g584);
        long g589 = (g588 & x0_31);
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
        long w33 = cat(w32, g583, 1);
        long w34 = cat(w33, g578, 1);
        long w35 = cat(w34, g575, 1);
        long w36 = cat(w35, g571, 1);
        long w37 = cat(w36, g569, 1);
        long w38 = cat(w37, g567, 1);
        long w39 = cat(w38, g565, 1);
        long w40 = cat(w39, g562, 1);
        long w41 = cat(w40, g561, 1);
        long w42 = cat(w41, g560, 1);
        long w43 = cat(w42, g559, 1);
        long w44 = cat(w43, g558, 1);
        long w45 = cat(w44, g557, 1);
        long w46 = cat(w45, g556, 1);
        long w47 = cat(w46, g555, 1);
        long w48 = cat(w47, g553, 1);
        long w49 = cat(w48, g543, 1);
        long w50 = cat(w49, g533, 1);
        long w51 = cat(w50, g523, 1);
        long w52 = cat(w51, g513, 1);
        long w53 = cat(w52, g502, 1);
        long w54 = cat(w53, g491, 1);
        long w55 = cat(w54, g480, 1);
        long w56 = cat(w55, g469, 1);
        long w57 = cat(w56, g443, 1);
        long w58 = cat(w57, g417, 1);
        long w59 = cat(w58, g390, 1);
        long w60 = cat(w59, g363, 1);
        long w61 = cat(w60, g305, 1);
        long w62 = cat(w61, g246, 1);
        long w63 = cat(w62, g123, 1);
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
                    answers.Append(((ulong) emu_shr_cl_gpr_32__reg_rdi__csharp(values[0], values[1])).ToString());
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
