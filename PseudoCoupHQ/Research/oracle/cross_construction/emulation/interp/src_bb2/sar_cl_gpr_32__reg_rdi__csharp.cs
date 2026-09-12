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
    // one named local per gate, over the term of sar_cl_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
    public static long emu_sar_cl_gpr_32__reg_rdi__csharp(long a, long b) {
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
        long g228 = (x1_1 ^ 1L);
        long g229 = (x1_1 & x0_31);
        long g230 = (g228 & g227);
        long g231 = (g229 | g230);
        long g232 = (x1_2 ^ 1L);
        long g233 = (x1_2 & g231);
        long g234 = (g232 & g223);
        long g235 = (g233 | g234);
        long g236 = (x1_3 ^ 1L);
        long g237 = (x1_3 & g235);
        long g238 = (g236 & g211);
        long g239 = (g237 | g238);
        long g240 = (x1_4 ^ 1L);
        long g241 = (x1_4 & g239);
        long g242 = (g240 & g183);
        long g243 = (g241 | g242);
        long g244 = (x1_1 ^ 1L);
        long g245 = (x1_1 & g15);
        long g246 = (g244 & g7);
        long g247 = (g245 | g246);
        long g248 = (x1_1 ^ 1L);
        long g249 = (x1_1 & g31);
        long g250 = (g248 & g19);
        long g251 = (g249 | g250);
        long g252 = (x1_2 ^ 1L);
        long g253 = (x1_2 & g251);
        long g254 = (g252 & g247);
        long g255 = (g253 | g254);
        long g256 = (x1_1 ^ 1L);
        long g257 = (x1_1 & g43);
        long g258 = (g256 & g35);
        long g259 = (g257 | g258);
        long g260 = (x1_1 ^ 1L);
        long g261 = (x1_1 & g63);
        long g262 = (g260 & g47);
        long g263 = (g261 | g262);
        long g264 = (x1_2 ^ 1L);
        long g265 = (x1_2 & g263);
        long g266 = (g264 & g259);
        long g267 = (g265 | g266);
        long g268 = (x1_3 ^ 1L);
        long g269 = (x1_3 & g267);
        long g270 = (g268 & g255);
        long g271 = (g269 | g270);
        long g272 = (x1_1 ^ 1L);
        long g273 = (x1_1 & g75);
        long g274 = (g272 & g67);
        long g275 = (g273 | g274);
        long g276 = (x1_1 ^ 1L);
        long g277 = (x1_1 & g91);
        long g278 = (g276 & g79);
        long g279 = (g277 | g278);
        long g280 = (x1_2 ^ 1L);
        long g281 = (x1_2 & g279);
        long g282 = (g280 & g275);
        long g283 = (g281 | g282);
        long g284 = (x1_1 ^ 1L);
        long g285 = (x1_1 & g103);
        long g286 = (g284 & g95);
        long g287 = (g285 | g286);
        long g288 = (x1_1 | x1_0);
        long g289 = (g288 ^ 1L);
        long g290 = (g288 & x0_31);
        long g291 = (g289 & x0_30);
        long g292 = (g290 | g291);
        long g293 = (x1_2 ^ 1L);
        long g294 = (x1_2 & g292);
        long g295 = (g293 & g287);
        long g296 = (g294 | g295);
        long g297 = (x1_3 ^ 1L);
        long g298 = (x1_3 & g296);
        long g299 = (g297 & g283);
        long g300 = (g298 | g299);
        long g301 = (x1_4 ^ 1L);
        long g302 = (x1_4 & g300);
        long g303 = (g301 & g271);
        long g304 = (g302 | g303);
        long g305 = (x1_1 ^ 1L);
        long g306 = (x1_1 & g139);
        long g307 = (g305 & g131);
        long g308 = (g306 | g307);
        long g309 = (x1_1 ^ 1L);
        long g310 = (x1_1 & g155);
        long g311 = (g309 & g143);
        long g312 = (g310 | g311);
        long g313 = (x1_2 ^ 1L);
        long g314 = (x1_2 & g312);
        long g315 = (g313 & g308);
        long g316 = (g314 | g315);
        long g317 = (x1_1 ^ 1L);
        long g318 = (x1_1 & g167);
        long g319 = (g317 & g159);
        long g320 = (g318 | g319);
        long g321 = (x1_1 ^ 1L);
        long g322 = (x1_1 & g187);
        long g323 = (g321 & g171);
        long g324 = (g322 | g323);
        long g325 = (x1_2 ^ 1L);
        long g326 = (x1_2 & g324);
        long g327 = (g325 & g320);
        long g328 = (g326 | g327);
        long g329 = (x1_3 ^ 1L);
        long g330 = (x1_3 & g328);
        long g331 = (g329 & g316);
        long g332 = (g330 | g331);
        long g333 = (x1_1 ^ 1L);
        long g334 = (x1_1 & g199);
        long g335 = (g333 & g191);
        long g336 = (g334 | g335);
        long g337 = (x1_1 ^ 1L);
        long g338 = (x1_1 & g215);
        long g339 = (g337 & g203);
        long g340 = (g338 | g339);
        long g341 = (x1_2 ^ 1L);
        long g342 = (x1_2 & g340);
        long g343 = (g341 & g336);
        long g344 = (g342 | g343);
        long g345 = (x1_1 ^ 1L);
        long g346 = (x1_1 & g227);
        long g347 = (g345 & g219);
        long g348 = (g346 | g347);
        long g349 = (x1_2 ^ 1L);
        long g350 = (x1_2 & x0_31);
        long g351 = (g349 & g348);
        long g352 = (g350 | g351);
        long g353 = (x1_3 ^ 1L);
        long g354 = (x1_3 & g352);
        long g355 = (g353 & g344);
        long g356 = (g354 | g355);
        long g357 = (x1_4 ^ 1L);
        long g358 = (x1_4 & g356);
        long g359 = (g357 & g332);
        long g360 = (g358 | g359);
        long g361 = (x1_2 ^ 1L);
        long g362 = (x1_2 & g39);
        long g363 = (g361 & g23);
        long g364 = (g362 | g363);
        long g365 = (x1_2 ^ 1L);
        long g366 = (x1_2 & g71);
        long g367 = (g365 & g51);
        long g368 = (g366 | g367);
        long g369 = (x1_3 ^ 1L);
        long g370 = (x1_3 & g368);
        long g371 = (g369 & g364);
        long g372 = (g370 | g371);
        long g373 = (x1_2 ^ 1L);
        long g374 = (x1_2 & g99);
        long g375 = (g373 & g83);
        long g376 = (g374 | g375);
        long g377 = (x1_2 ^ 1L);
        long g378 = (x1_2 & x0_31);
        long g379 = (g377 & g111);
        long g380 = (g378 | g379);
        long g381 = (x1_3 ^ 1L);
        long g382 = (x1_3 & g380);
        long g383 = (g381 & g376);
        long g384 = (g382 | g383);
        long g385 = (x1_4 ^ 1L);
        long g386 = (x1_4 & g384);
        long g387 = (g385 & g372);
        long g388 = (g386 | g387);
        long g389 = (x1_2 ^ 1L);
        long g390 = (x1_2 & g163);
        long g391 = (g389 & g147);
        long g392 = (g390 | g391);
        long g393 = (x1_2 ^ 1L);
        long g394 = (x1_2 & g195);
        long g395 = (g393 & g175);
        long g396 = (g394 | g395);
        long g397 = (x1_3 ^ 1L);
        long g398 = (x1_3 & g396);
        long g399 = (g397 & g392);
        long g400 = (g398 | g399);
        long g401 = (x1_2 ^ 1L);
        long g402 = (x1_2 & g223);
        long g403 = (g401 & g207);
        long g404 = (g402 | g403);
        long g405 = (x1_2 | x1_1);
        long g406 = (g405 ^ 1L);
        long g407 = (g405 & x0_31);
        long g408 = (g406 & g227);
        long g409 = (g407 | g408);
        long g410 = (x1_3 ^ 1L);
        long g411 = (x1_3 & g409);
        long g412 = (g410 & g404);
        long g413 = (g411 | g412);
        long g414 = (x1_4 ^ 1L);
        long g415 = (x1_4 & g413);
        long g416 = (g414 & g400);
        long g417 = (g415 | g416);
        long g418 = (x1_2 ^ 1L);
        long g419 = (x1_2 & g259);
        long g420 = (g418 & g251);
        long g421 = (g419 | g420);
        long g422 = (x1_2 ^ 1L);
        long g423 = (x1_2 & g275);
        long g424 = (g422 & g263);
        long g425 = (g423 | g424);
        long g426 = (x1_3 ^ 1L);
        long g427 = (x1_3 & g425);
        long g428 = (g426 & g421);
        long g429 = (g427 | g428);
        long g430 = (x1_2 ^ 1L);
        long g431 = (x1_2 & g287);
        long g432 = (g430 & g279);
        long g433 = (g431 | g432);
        long g434 = (x1_2 | g288);
        long g435 = (g434 ^ 1L);
        long g436 = (g434 & x0_31);
        long g437 = (g435 & x0_30);
        long g438 = (g436 | g437);
        long g439 = (x1_3 ^ 1L);
        long g440 = (x1_3 & g438);
        long g441 = (g439 & g433);
        long g442 = (g440 | g441);
        long g443 = (x1_4 ^ 1L);
        long g444 = (x1_4 & g442);
        long g445 = (g443 & g429);
        long g446 = (g444 | g445);
        long g447 = (x1_2 ^ 1L);
        long g448 = (x1_2 & g320);
        long g449 = (g447 & g312);
        long g450 = (g448 | g449);
        long g451 = (x1_2 ^ 1L);
        long g452 = (x1_2 & g336);
        long g453 = (g451 & g324);
        long g454 = (g452 | g453);
        long g455 = (x1_3 ^ 1L);
        long g456 = (x1_3 & g454);
        long g457 = (g455 & g450);
        long g458 = (g456 | g457);
        long g459 = (x1_2 ^ 1L);
        long g460 = (x1_2 & g348);
        long g461 = (g459 & g340);
        long g462 = (g460 | g461);
        long g463 = (x1_3 ^ 1L);
        long g464 = (x1_3 & x0_31);
        long g465 = (g463 & g462);
        long g466 = (g464 | g465);
        long g467 = (x1_4 ^ 1L);
        long g468 = (x1_4 & g466);
        long g469 = (g467 & g458);
        long g470 = (g468 | g469);
        long g471 = (x1_3 ^ 1L);
        long g472 = (x1_3 & g87);
        long g473 = (g471 & g55);
        long g474 = (g472 | g473);
        long g475 = (x1_3 ^ 1L);
        long g476 = (x1_3 & x0_31);
        long g477 = (g475 & g115);
        long g478 = (g476 | g477);
        long g479 = (x1_4 ^ 1L);
        long g480 = (x1_4 & g478);
        long g481 = (g479 & g474);
        long g482 = (g480 | g481);
        long g483 = (x1_3 ^ 1L);
        long g484 = (x1_3 & g211);
        long g485 = (g483 & g179);
        long g486 = (g484 | g485);
        long g487 = (x1_3 ^ 1L);
        long g488 = (x1_3 & x0_31);
        long g489 = (g487 & g235);
        long g490 = (g488 | g489);
        long g491 = (x1_4 ^ 1L);
        long g492 = (x1_4 & g490);
        long g493 = (g491 & g486);
        long g494 = (g492 | g493);
        long g495 = (x1_3 ^ 1L);
        long g496 = (x1_3 & g283);
        long g497 = (g495 & g267);
        long g498 = (g496 | g497);
        long g499 = (x1_3 ^ 1L);
        long g500 = (x1_3 & x0_31);
        long g501 = (g499 & g296);
        long g502 = (g500 | g501);
        long g503 = (x1_4 ^ 1L);
        long g504 = (x1_4 & g502);
        long g505 = (g503 & g498);
        long g506 = (g504 | g505);
        long g507 = (x1_3 ^ 1L);
        long g508 = (x1_3 & g344);
        long g509 = (g507 & g328);
        long g510 = (g508 | g509);
        long g511 = (x1_3 | x1_2);
        long g512 = (g511 ^ 1L);
        long g513 = (g511 & x0_31);
        long g514 = (g512 & g348);
        long g515 = (g513 | g514);
        long g516 = (x1_4 ^ 1L);
        long g517 = (x1_4 & g515);
        long g518 = (g516 & g510);
        long g519 = (g517 | g518);
        long g520 = (x1_3 ^ 1L);
        long g521 = (x1_3 & g376);
        long g522 = (g520 & g368);
        long g523 = (g521 | g522);
        long g524 = (g511 ^ 1L);
        long g525 = (g511 & x0_31);
        long g526 = (g524 & g111);
        long g527 = (g525 | g526);
        long g528 = (x1_4 ^ 1L);
        long g529 = (x1_4 & g527);
        long g530 = (g528 & g523);
        long g531 = (g529 | g530);
        long g532 = (x1_3 ^ 1L);
        long g533 = (x1_3 & g404);
        long g534 = (g532 & g396);
        long g535 = (g533 | g534);
        long g536 = (x1_3 | g405);
        long g537 = (g536 ^ 1L);
        long g538 = (g536 & x0_31);
        long g539 = (g537 & g227);
        long g540 = (g538 | g539);
        long g541 = (x1_4 ^ 1L);
        long g542 = (x1_4 & g540);
        long g543 = (g541 & g535);
        long g544 = (g542 | g543);
        long g545 = (x1_3 ^ 1L);
        long g546 = (x1_3 & g433);
        long g547 = (g545 & g425);
        long g548 = (g546 | g547);
        long g549 = (x1_3 | g434);
        long g550 = (g549 ^ 1L);
        long g551 = (g549 & x0_31);
        long g552 = (g550 & x0_30);
        long g553 = (g551 | g552);
        long g554 = (x1_4 ^ 1L);
        long g555 = (x1_4 & g553);
        long g556 = (g554 & g548);
        long g557 = (g555 | g556);
        long g558 = (x1_3 ^ 1L);
        long g559 = (x1_3 & g462);
        long g560 = (g558 & g454);
        long g561 = (g559 | g560);
        long k0 = 0L;
        long g562 = (k0 | x1_4);
        long g563 = (g562 ^ 1L);
        long g564 = (g562 & x0_31);
        long g565 = (g563 & g561);
        long g566 = (g564 | g565);
        long g567 = (g562 ^ 1L);
        long g568 = (g562 & x0_31);
        long g569 = (g567 & g119);
        long g570 = (g568 | g569);
        long g571 = (g562 ^ 1L);
        long g572 = (g562 & x0_31);
        long g573 = (g571 & g239);
        long g574 = (g572 | g573);
        long g575 = (g562 ^ 1L);
        long g576 = (g562 & x0_31);
        long g577 = (g575 & g300);
        long g578 = (g576 | g577);
        long g579 = (g562 ^ 1L);
        long g580 = (g562 & x0_31);
        long g581 = (g579 & g356);
        long g582 = (g580 | g581);
        long g583 = (g562 ^ 1L);
        long g584 = (g562 & x0_31);
        long g585 = (g583 & g384);
        long g586 = (g584 | g585);
        long g587 = (g562 ^ 1L);
        long g588 = (g562 & x0_31);
        long g589 = (g587 & g413);
        long g590 = (g588 | g589);
        long g591 = (g562 ^ 1L);
        long g592 = (g562 & x0_31);
        long g593 = (g591 & g442);
        long g594 = (g592 | g593);
        long g595 = (x1_4 | x1_3);
        long g596 = (k0 | g595);
        long g597 = (g596 ^ 1L);
        long g598 = (g596 & x0_31);
        long g599 = (g597 & g462);
        long g600 = (g598 | g599);
        long g601 = (g596 ^ 1L);
        long g602 = (g596 & x0_31);
        long g603 = (g601 & g115);
        long g604 = (g602 | g603);
        long g605 = (g596 ^ 1L);
        long g606 = (g596 & x0_31);
        long g607 = (g605 & g235);
        long g608 = (g606 | g607);
        long g609 = (g596 ^ 1L);
        long g610 = (g596 & x0_31);
        long g611 = (g609 & g296);
        long g612 = (g610 | g611);
        long g613 = (x1_4 | g511);
        long g614 = (k0 | g613);
        long g615 = (g614 ^ 1L);
        long g616 = (g614 & x0_31);
        long g617 = (g615 & g348);
        long g618 = (g616 | g617);
        long g619 = (g614 ^ 1L);
        long g620 = (g614 & x0_31);
        long g621 = (g619 & g111);
        long g622 = (g620 | g621);
        long g623 = (x1_4 | g536);
        long g624 = (k0 | g623);
        long g625 = (g624 ^ 1L);
        long g626 = (g624 & x0_31);
        long g627 = (g625 & g227);
        long g628 = (g626 | g627);
        long g629 = (x1_4 | g549);
        long g630 = (k0 | g629);
        long g631 = (g630 ^ 1L);
        long g632 = (g630 & x0_31);
        long g633 = (g631 & x0_30);
        long g634 = (g632 | g633);
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
        long w32 = cat(w31, x0_31, 1);
        long w33 = cat(w32, g634, 1);
        long w34 = cat(w33, g628, 1);
        long w35 = cat(w34, g622, 1);
        long w36 = cat(w35, g618, 1);
        long w37 = cat(w36, g612, 1);
        long w38 = cat(w37, g608, 1);
        long w39 = cat(w38, g604, 1);
        long w40 = cat(w39, g600, 1);
        long w41 = cat(w40, g594, 1);
        long w42 = cat(w41, g590, 1);
        long w43 = cat(w42, g586, 1);
        long w44 = cat(w43, g582, 1);
        long w45 = cat(w44, g578, 1);
        long w46 = cat(w45, g574, 1);
        long w47 = cat(w46, g570, 1);
        long w48 = cat(w47, g566, 1);
        long w49 = cat(w48, g557, 1);
        long w50 = cat(w49, g544, 1);
        long w51 = cat(w50, g531, 1);
        long w52 = cat(w51, g519, 1);
        long w53 = cat(w52, g506, 1);
        long w54 = cat(w53, g494, 1);
        long w55 = cat(w54, g482, 1);
        long w56 = cat(w55, g470, 1);
        long w57 = cat(w56, g446, 1);
        long w58 = cat(w57, g417, 1);
        long w59 = cat(w58, g388, 1);
        long w60 = cat(w59, g360, 1);
        long w61 = cat(w60, g304, 1);
        long w62 = cat(w61, g243, 1);
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
                    answers.Append(((ulong) emu_sar_cl_gpr_32__reg_rdi__csharp(values[0], values[1])).ToString());
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
