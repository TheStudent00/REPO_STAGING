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
    // one named local per gate, over the term of sbb_gpr_same_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1, 1, 0)*4294967295)
    public static long emu_sbb_gpr_same_32__reg_rdi__csharp(long a, long b, long c) {
        long x1_0 = ext(a, 0, 0);
        long x0_0 = ext(b, 0, 0);
        long x1_1 = ext(a, 1, 1);
        long x0_1 = ext(b, 1, 1);
        long x1_2 = ext(a, 2, 2);
        long x0_2 = ext(b, 2, 2);
        long x1_3 = ext(a, 3, 3);
        long x0_3 = ext(b, 3, 3);
        long x1_4 = ext(a, 4, 4);
        long x0_4 = ext(b, 4, 4);
        long x1_5 = ext(a, 5, 5);
        long x0_5 = ext(b, 5, 5);
        long x1_6 = ext(a, 6, 6);
        long x0_6 = ext(b, 6, 6);
        long x1_7 = ext(a, 7, 7);
        long x0_7 = ext(b, 7, 7);
        long x1_8 = ext(a, 8, 8);
        long x0_8 = ext(b, 8, 8);
        long x1_9 = ext(a, 9, 9);
        long x0_9 = ext(b, 9, 9);
        long x1_10 = ext(a, 10, 10);
        long x0_10 = ext(b, 10, 10);
        long x1_11 = ext(a, 11, 11);
        long x0_11 = ext(b, 11, 11);
        long x1_12 = ext(a, 12, 12);
        long x0_12 = ext(b, 12, 12);
        long x1_13 = ext(a, 13, 13);
        long x0_13 = ext(b, 13, 13);
        long x1_14 = ext(a, 14, 14);
        long x0_14 = ext(b, 14, 14);
        long x1_15 = ext(a, 15, 15);
        long x0_15 = ext(b, 15, 15);
        long x1_16 = ext(a, 16, 16);
        long x0_16 = ext(b, 16, 16);
        long x1_17 = ext(a, 17, 17);
        long x0_17 = ext(b, 17, 17);
        long x1_18 = ext(a, 18, 18);
        long x0_18 = ext(b, 18, 18);
        long x1_19 = ext(a, 19, 19);
        long x0_19 = ext(b, 19, 19);
        long x1_20 = ext(a, 20, 20);
        long x0_20 = ext(b, 20, 20);
        long x1_21 = ext(a, 21, 21);
        long x0_21 = ext(b, 21, 21);
        long x1_22 = ext(a, 22, 22);
        long x0_22 = ext(b, 22, 22);
        long x1_23 = ext(a, 23, 23);
        long x0_23 = ext(b, 23, 23);
        long x1_24 = ext(a, 24, 24);
        long x0_24 = ext(b, 24, 24);
        long x1_25 = ext(a, 25, 25);
        long x0_25 = ext(b, 25, 25);
        long x1_26 = ext(a, 26, 26);
        long x0_26 = ext(b, 26, 26);
        long x1_27 = ext(a, 27, 27);
        long x0_27 = ext(b, 27, 27);
        long x1_28 = ext(a, 28, 28);
        long x0_28 = ext(b, 28, 28);
        long x1_29 = ext(a, 29, 29);
        long x0_29 = ext(b, 29, 29);
        long x1_30 = ext(a, 30, 30);
        long x0_30 = ext(b, 30, 30);
        long x1_31 = ext(a, 31, 31);
        long x0_31 = ext(b, 31, 31);
        long g0 = (x1_0 ^ 1L);
        long g1 = (x0_0 ^ 1L);
        long g2 = (g1 | g0);
        long g3 = (x1_1 ^ 1L);
        long g4 = (g3 | g2);
        long g5 = (g4 ^ 1L);
        long g6 = (x0_1 ^ 1L);
        long g7 = (g6 | g2);
        long g8 = (g7 ^ 1L);
        long g9 = (g6 | g3);
        long g10 = (g9 ^ 1L);
        long g11 = (g10 | g8);
        long g12 = (g11 | g5);
        long g13 = (g12 ^ 1L);
        long g14 = (x1_2 ^ 1L);
        long g15 = (g14 | g13);
        long g16 = (g15 ^ 1L);
        long g17 = (x0_2 ^ 1L);
        long g18 = (g17 | g13);
        long g19 = (g18 ^ 1L);
        long g20 = (g17 | g14);
        long g21 = (g20 ^ 1L);
        long g22 = (g21 | g19);
        long g23 = (g22 | g16);
        long g24 = (g23 ^ 1L);
        long g25 = (x1_3 ^ 1L);
        long g26 = (g25 | g24);
        long g27 = (g26 ^ 1L);
        long g28 = (x0_3 ^ 1L);
        long g29 = (g28 | g24);
        long g30 = (g29 ^ 1L);
        long g31 = (g28 | g25);
        long g32 = (g31 ^ 1L);
        long g33 = (g32 | g30);
        long g34 = (g33 | g27);
        long g35 = (g34 ^ 1L);
        long g36 = (x1_4 ^ 1L);
        long g37 = (g36 | g35);
        long g38 = (g37 ^ 1L);
        long g39 = (x0_4 ^ 1L);
        long g40 = (g39 | g35);
        long g41 = (g40 ^ 1L);
        long g42 = (g39 | g36);
        long g43 = (g42 ^ 1L);
        long g44 = (g43 | g41);
        long g45 = (g44 | g38);
        long g46 = (g45 ^ 1L);
        long g47 = (x1_5 ^ 1L);
        long g48 = (g47 | g46);
        long g49 = (g48 ^ 1L);
        long g50 = (x0_5 ^ 1L);
        long g51 = (g50 | g46);
        long g52 = (g51 ^ 1L);
        long g53 = (g50 | g47);
        long g54 = (g53 ^ 1L);
        long g55 = (g54 | g52);
        long g56 = (g55 | g49);
        long g57 = (g56 ^ 1L);
        long g58 = (x1_6 ^ 1L);
        long g59 = (g58 | g57);
        long g60 = (g59 ^ 1L);
        long g61 = (x0_6 ^ 1L);
        long g62 = (g61 | g57);
        long g63 = (g62 ^ 1L);
        long g64 = (g61 | g58);
        long g65 = (g64 ^ 1L);
        long g66 = (g65 | g63);
        long g67 = (g66 | g60);
        long g68 = (g67 ^ 1L);
        long g69 = (x1_7 ^ 1L);
        long g70 = (g69 | g68);
        long g71 = (g70 ^ 1L);
        long g72 = (x0_7 ^ 1L);
        long g73 = (g72 | g68);
        long g74 = (g73 ^ 1L);
        long g75 = (g72 | g69);
        long g76 = (g75 ^ 1L);
        long g77 = (g76 | g74);
        long g78 = (g77 | g71);
        long g79 = (g78 ^ 1L);
        long g80 = (x1_8 ^ 1L);
        long g81 = (g80 | g79);
        long g82 = (g81 ^ 1L);
        long g83 = (x0_8 ^ 1L);
        long g84 = (g83 | g79);
        long g85 = (g84 ^ 1L);
        long g86 = (g83 | g80);
        long g87 = (g86 ^ 1L);
        long g88 = (g87 | g85);
        long g89 = (g88 | g82);
        long g90 = (g89 ^ 1L);
        long g91 = (x1_9 ^ 1L);
        long g92 = (g91 | g90);
        long g93 = (g92 ^ 1L);
        long g94 = (x0_9 ^ 1L);
        long g95 = (g94 | g90);
        long g96 = (g95 ^ 1L);
        long g97 = (g94 | g91);
        long g98 = (g97 ^ 1L);
        long g99 = (g98 | g96);
        long g100 = (g99 | g93);
        long g101 = (g100 ^ 1L);
        long g102 = (x1_10 ^ 1L);
        long g103 = (g102 | g101);
        long g104 = (g103 ^ 1L);
        long g105 = (x0_10 ^ 1L);
        long g106 = (g105 | g101);
        long g107 = (g106 ^ 1L);
        long g108 = (g105 | g102);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 | g107);
        long g111 = (g110 | g104);
        long g112 = (g111 ^ 1L);
        long g113 = (x1_11 ^ 1L);
        long g114 = (g113 | g112);
        long g115 = (g114 ^ 1L);
        long g116 = (x0_11 ^ 1L);
        long g117 = (g116 | g112);
        long g118 = (g117 ^ 1L);
        long g119 = (g116 | g113);
        long g120 = (g119 ^ 1L);
        long g121 = (g120 | g118);
        long g122 = (g121 | g115);
        long g123 = (g122 ^ 1L);
        long g124 = (x1_12 ^ 1L);
        long g125 = (g124 | g123);
        long g126 = (g125 ^ 1L);
        long g127 = (x0_12 ^ 1L);
        long g128 = (g127 | g123);
        long g129 = (g128 ^ 1L);
        long g130 = (g127 | g124);
        long g131 = (g130 ^ 1L);
        long g132 = (g131 | g129);
        long g133 = (g132 | g126);
        long g134 = (g133 ^ 1L);
        long g135 = (x1_13 ^ 1L);
        long g136 = (g135 | g134);
        long g137 = (g136 ^ 1L);
        long g138 = (x0_13 ^ 1L);
        long g139 = (g138 | g134);
        long g140 = (g139 ^ 1L);
        long g141 = (g138 | g135);
        long g142 = (g141 ^ 1L);
        long g143 = (g142 | g140);
        long g144 = (g143 | g137);
        long g145 = (g144 ^ 1L);
        long g146 = (x1_14 ^ 1L);
        long g147 = (g146 | g145);
        long g148 = (g147 ^ 1L);
        long g149 = (x0_14 ^ 1L);
        long g150 = (g149 | g145);
        long g151 = (g150 ^ 1L);
        long g152 = (g149 | g146);
        long g153 = (g152 ^ 1L);
        long g154 = (g153 | g151);
        long g155 = (g154 | g148);
        long g156 = (g155 ^ 1L);
        long g157 = (x1_15 ^ 1L);
        long g158 = (g157 | g156);
        long g159 = (g158 ^ 1L);
        long g160 = (x0_15 ^ 1L);
        long g161 = (g160 | g156);
        long g162 = (g161 ^ 1L);
        long g163 = (g160 | g157);
        long g164 = (g163 ^ 1L);
        long g165 = (g164 | g162);
        long g166 = (g165 | g159);
        long g167 = (g166 ^ 1L);
        long g168 = (x1_16 ^ 1L);
        long g169 = (g168 | g167);
        long g170 = (g169 ^ 1L);
        long g171 = (x0_16 ^ 1L);
        long g172 = (g171 | g167);
        long g173 = (g172 ^ 1L);
        long g174 = (g171 | g168);
        long g175 = (g174 ^ 1L);
        long g176 = (g175 | g173);
        long g177 = (g176 | g170);
        long g178 = (g177 ^ 1L);
        long g179 = (x1_17 ^ 1L);
        long g180 = (g179 | g178);
        long g181 = (g180 ^ 1L);
        long g182 = (x0_17 ^ 1L);
        long g183 = (g182 | g178);
        long g184 = (g183 ^ 1L);
        long g185 = (g182 | g179);
        long g186 = (g185 ^ 1L);
        long g187 = (g186 | g184);
        long g188 = (g187 | g181);
        long g189 = (g188 ^ 1L);
        long g190 = (x1_18 ^ 1L);
        long g191 = (g190 | g189);
        long g192 = (g191 ^ 1L);
        long g193 = (x0_18 ^ 1L);
        long g194 = (g193 | g189);
        long g195 = (g194 ^ 1L);
        long g196 = (g193 | g190);
        long g197 = (g196 ^ 1L);
        long g198 = (g197 | g195);
        long g199 = (g198 | g192);
        long g200 = (g199 ^ 1L);
        long g201 = (x1_19 ^ 1L);
        long g202 = (g201 | g200);
        long g203 = (g202 ^ 1L);
        long g204 = (x0_19 ^ 1L);
        long g205 = (g204 | g200);
        long g206 = (g205 ^ 1L);
        long g207 = (g204 | g201);
        long g208 = (g207 ^ 1L);
        long g209 = (g208 | g206);
        long g210 = (g209 | g203);
        long g211 = (g210 ^ 1L);
        long g212 = (x1_20 ^ 1L);
        long g213 = (g212 | g211);
        long g214 = (g213 ^ 1L);
        long g215 = (x0_20 ^ 1L);
        long g216 = (g215 | g211);
        long g217 = (g216 ^ 1L);
        long g218 = (g215 | g212);
        long g219 = (g218 ^ 1L);
        long g220 = (g219 | g217);
        long g221 = (g220 | g214);
        long g222 = (g221 ^ 1L);
        long g223 = (x1_21 ^ 1L);
        long g224 = (g223 | g222);
        long g225 = (g224 ^ 1L);
        long g226 = (x0_21 ^ 1L);
        long g227 = (g226 | g222);
        long g228 = (g227 ^ 1L);
        long g229 = (g226 | g223);
        long g230 = (g229 ^ 1L);
        long g231 = (g230 | g228);
        long g232 = (g231 | g225);
        long g233 = (g232 ^ 1L);
        long g234 = (x1_22 ^ 1L);
        long g235 = (g234 | g233);
        long g236 = (g235 ^ 1L);
        long g237 = (x0_22 ^ 1L);
        long g238 = (g237 | g233);
        long g239 = (g238 ^ 1L);
        long g240 = (g237 | g234);
        long g241 = (g240 ^ 1L);
        long g242 = (g241 | g239);
        long g243 = (g242 | g236);
        long g244 = (g243 ^ 1L);
        long g245 = (x1_23 ^ 1L);
        long g246 = (g245 | g244);
        long g247 = (g246 ^ 1L);
        long g248 = (x0_23 ^ 1L);
        long g249 = (g248 | g244);
        long g250 = (g249 ^ 1L);
        long g251 = (g248 | g245);
        long g252 = (g251 ^ 1L);
        long g253 = (g252 | g250);
        long g254 = (g253 | g247);
        long g255 = (g254 ^ 1L);
        long g256 = (x1_24 ^ 1L);
        long g257 = (g256 | g255);
        long g258 = (g257 ^ 1L);
        long g259 = (x0_24 ^ 1L);
        long g260 = (g259 | g255);
        long g261 = (g260 ^ 1L);
        long g262 = (g259 | g256);
        long g263 = (g262 ^ 1L);
        long g264 = (g263 | g261);
        long g265 = (g264 | g258);
        long g266 = (g265 ^ 1L);
        long g267 = (x1_25 ^ 1L);
        long g268 = (g267 | g266);
        long g269 = (g268 ^ 1L);
        long g270 = (x0_25 ^ 1L);
        long g271 = (g270 | g266);
        long g272 = (g271 ^ 1L);
        long g273 = (g270 | g267);
        long g274 = (g273 ^ 1L);
        long g275 = (g274 | g272);
        long g276 = (g275 | g269);
        long g277 = (g276 ^ 1L);
        long g278 = (x1_26 ^ 1L);
        long g279 = (g278 | g277);
        long g280 = (g279 ^ 1L);
        long g281 = (x0_26 ^ 1L);
        long g282 = (g281 | g277);
        long g283 = (g282 ^ 1L);
        long g284 = (g281 | g278);
        long g285 = (g284 ^ 1L);
        long g286 = (g285 | g283);
        long g287 = (g286 | g280);
        long g288 = (g287 ^ 1L);
        long g289 = (x1_27 ^ 1L);
        long g290 = (g289 | g288);
        long g291 = (g290 ^ 1L);
        long g292 = (x0_27 ^ 1L);
        long g293 = (g292 | g288);
        long g294 = (g293 ^ 1L);
        long g295 = (g292 | g289);
        long g296 = (g295 ^ 1L);
        long g297 = (g296 | g294);
        long g298 = (g297 | g291);
        long g299 = (g298 ^ 1L);
        long g300 = (x1_28 ^ 1L);
        long g301 = (g300 | g299);
        long g302 = (g301 ^ 1L);
        long g303 = (x0_28 ^ 1L);
        long g304 = (g303 | g299);
        long g305 = (g304 ^ 1L);
        long g306 = (g303 | g300);
        long g307 = (g306 ^ 1L);
        long g308 = (g307 | g305);
        long g309 = (g308 | g302);
        long g310 = (g309 ^ 1L);
        long g311 = (x1_29 ^ 1L);
        long g312 = (g311 | g310);
        long g313 = (g312 ^ 1L);
        long g314 = (x0_29 ^ 1L);
        long g315 = (g314 | g310);
        long g316 = (g315 ^ 1L);
        long g317 = (g314 | g311);
        long g318 = (g317 ^ 1L);
        long g319 = (g318 | g316);
        long g320 = (g319 | g313);
        long g321 = (g320 ^ 1L);
        long g322 = (x1_30 ^ 1L);
        long g323 = (g322 | g321);
        long g324 = (g323 ^ 1L);
        long g325 = (x0_30 ^ 1L);
        long g326 = (g325 | g321);
        long g327 = (g326 ^ 1L);
        long g328 = (g325 | g322);
        long g329 = (g328 ^ 1L);
        long g330 = (g329 | g327);
        long g331 = (g330 | g324);
        long g332 = (g331 ^ 1L);
        long g333 = (x1_31 ^ 1L);
        long g334 = (g333 | g332);
        long g335 = (g334 ^ 1L);
        long g336 = (x0_31 ^ 1L);
        long g337 = (g336 | g332);
        long g338 = (g337 ^ 1L);
        long g339 = (g336 | g333);
        long g340 = (g339 ^ 1L);
        long g341 = (g340 | g338);
        long g342 = (g341 | g335);
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
        long w32 = cat(w31, g342, 1);
        long w33 = cat(w32, g342, 1);
        long w34 = cat(w33, g342, 1);
        long w35 = cat(w34, g342, 1);
        long w36 = cat(w35, g342, 1);
        long w37 = cat(w36, g342, 1);
        long w38 = cat(w37, g342, 1);
        long w39 = cat(w38, g342, 1);
        long w40 = cat(w39, g342, 1);
        long w41 = cat(w40, g342, 1);
        long w42 = cat(w41, g342, 1);
        long w43 = cat(w42, g342, 1);
        long w44 = cat(w43, g342, 1);
        long w45 = cat(w44, g342, 1);
        long w46 = cat(w45, g342, 1);
        long w47 = cat(w46, g342, 1);
        long w48 = cat(w47, g342, 1);
        long w49 = cat(w48, g342, 1);
        long w50 = cat(w49, g342, 1);
        long w51 = cat(w50, g342, 1);
        long w52 = cat(w51, g342, 1);
        long w53 = cat(w52, g342, 1);
        long w54 = cat(w53, g342, 1);
        long w55 = cat(w54, g342, 1);
        long w56 = cat(w55, g342, 1);
        long w57 = cat(w56, g342, 1);
        long w58 = cat(w57, g342, 1);
        long w59 = cat(w58, g342, 1);
        long w60 = cat(w59, g342, 1);
        long w61 = cat(w60, g342, 1);
        long w62 = cat(w61, g342, 1);
        long w63 = cat(w62, g342, 1);
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
                    answers.Append(((ulong) emu_sbb_gpr_same_32__reg_rdi__csharp(values[0], values[1], values[2])).ToString());
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
