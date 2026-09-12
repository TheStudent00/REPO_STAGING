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
    // one named local per gate, over the term of sub_gpr_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1))
    public static long emu_sub_gpr_gpr_32__reg_rdi__csharp(long a, long b) {
        long x0_0 = ext(b, 0, 0);
        long x1_0 = ext(a, 0, 0);
        long x1_1 = ext(a, 1, 1);
        long x0_1 = ext(b, 1, 1);
        long x0_2 = ext(b, 2, 2);
        long x1_2 = ext(a, 2, 2);
        long x0_3 = ext(b, 3, 3);
        long x1_3 = ext(a, 3, 3);
        long x0_4 = ext(b, 4, 4);
        long x1_4 = ext(a, 4, 4);
        long x0_5 = ext(b, 5, 5);
        long x1_5 = ext(a, 5, 5);
        long x0_6 = ext(b, 6, 6);
        long x1_6 = ext(a, 6, 6);
        long x0_7 = ext(b, 7, 7);
        long x1_7 = ext(a, 7, 7);
        long x0_8 = ext(b, 8, 8);
        long x1_8 = ext(a, 8, 8);
        long x0_9 = ext(b, 9, 9);
        long x1_9 = ext(a, 9, 9);
        long x0_10 = ext(b, 10, 10);
        long x1_10 = ext(a, 10, 10);
        long x0_11 = ext(b, 11, 11);
        long x1_11 = ext(a, 11, 11);
        long x0_12 = ext(b, 12, 12);
        long x1_12 = ext(a, 12, 12);
        long x0_13 = ext(b, 13, 13);
        long x1_13 = ext(a, 13, 13);
        long x0_14 = ext(b, 14, 14);
        long x1_14 = ext(a, 14, 14);
        long x0_15 = ext(b, 15, 15);
        long x1_15 = ext(a, 15, 15);
        long x0_16 = ext(b, 16, 16);
        long x1_16 = ext(a, 16, 16);
        long x0_17 = ext(b, 17, 17);
        long x1_17 = ext(a, 17, 17);
        long x0_18 = ext(b, 18, 18);
        long x1_18 = ext(a, 18, 18);
        long x0_19 = ext(b, 19, 19);
        long x1_19 = ext(a, 19, 19);
        long x0_20 = ext(b, 20, 20);
        long x1_20 = ext(a, 20, 20);
        long x0_21 = ext(b, 21, 21);
        long x1_21 = ext(a, 21, 21);
        long x0_22 = ext(b, 22, 22);
        long x1_22 = ext(a, 22, 22);
        long x0_23 = ext(b, 23, 23);
        long x1_23 = ext(a, 23, 23);
        long x0_24 = ext(b, 24, 24);
        long x1_24 = ext(a, 24, 24);
        long x0_25 = ext(b, 25, 25);
        long x1_25 = ext(a, 25, 25);
        long x0_26 = ext(b, 26, 26);
        long x1_26 = ext(a, 26, 26);
        long x0_27 = ext(b, 27, 27);
        long x1_27 = ext(a, 27, 27);
        long x0_28 = ext(b, 28, 28);
        long x1_28 = ext(a, 28, 28);
        long x0_29 = ext(b, 29, 29);
        long x1_29 = ext(a, 29, 29);
        long x0_30 = ext(b, 30, 30);
        long x1_30 = ext(a, 30, 30);
        long x0_31 = ext(b, 31, 31);
        long x1_31 = ext(a, 31, 31);
        long g0 = (x1_0 ^ x0_0);
        long g1 = (g0 ^ 1L);
        long g2 = (g1 ^ 1L);
        long g3 = (x1_0 ^ 1L);
        long g4 = (x0_0 ^ 1L);
        long g5 = (g4 | g3);
        long g6 = (x1_1 ^ g5);
        long g7 = (g6 ^ 1L);
        long g8 = (x0_0 ^ x0_1);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 ^ g7);
        long g11 = (g10 ^ 1L);
        long g12 = (x0_1 | x0_0);
        long g13 = (g12 ^ x0_2);
        long g14 = (g13 ^ 1L);
        long g15 = (g9 | g5);
        long g16 = (g15 ^ 1L);
        long g17 = (x1_1 ^ 1L);
        long g18 = (g17 | g5);
        long g19 = (g18 ^ 1L);
        long g20 = (g9 | g17);
        long g21 = (g20 ^ 1L);
        long g22 = (g21 | g19);
        long g23 = (g22 | g16);
        long g24 = (x1_2 ^ g23);
        long g25 = (g24 ^ 1L);
        long g26 = (g25 ^ g14);
        long g27 = (g26 ^ 1L);
        long g28 = (g27 ^ 1L);
        long g29 = (x0_2 | g12);
        long g30 = (g29 ^ x0_3);
        long g31 = (g30 ^ 1L);
        long g32 = (g23 ^ 1L);
        long g33 = (g14 | g32);
        long g34 = (g33 ^ 1L);
        long g35 = (x1_2 ^ 1L);
        long g36 = (g35 | g32);
        long g37 = (g36 ^ 1L);
        long g38 = (g14 | g35);
        long g39 = (g38 ^ 1L);
        long g40 = (g39 | g37);
        long g41 = (g40 | g34);
        long g42 = (x1_3 ^ g41);
        long g43 = (g42 ^ 1L);
        long g44 = (g43 ^ g31);
        long g45 = (g44 ^ 1L);
        long g46 = (g45 ^ 1L);
        long g47 = (x0_3 | g29);
        long g48 = (g47 ^ x0_4);
        long g49 = (g48 ^ 1L);
        long g50 = (g41 ^ 1L);
        long g51 = (x1_3 ^ 1L);
        long g52 = (g51 | g50);
        long g53 = (g52 ^ 1L);
        long g54 = (g31 | g51);
        long g55 = (g54 ^ 1L);
        long g56 = (g50 | g31);
        long g57 = (g56 ^ 1L);
        long g58 = (g57 | g55);
        long g59 = (g58 | g53);
        long g60 = (x1_4 ^ g59);
        long g61 = (g60 ^ 1L);
        long g62 = (g61 ^ g49);
        long g63 = (g62 ^ 1L);
        long g64 = (g63 ^ 1L);
        long g65 = (x0_4 | g47);
        long g66 = (g65 ^ x0_5);
        long g67 = (g66 ^ 1L);
        long g68 = (g59 ^ 1L);
        long g69 = (g49 | g68);
        long g70 = (g69 ^ 1L);
        long g71 = (x1_4 ^ 1L);
        long g72 = (g71 | g68);
        long g73 = (g72 ^ 1L);
        long g74 = (g49 | g71);
        long g75 = (g74 ^ 1L);
        long g76 = (g75 | g73);
        long g77 = (g76 | g70);
        long g78 = (x1_5 ^ g77);
        long g79 = (g78 ^ 1L);
        long g80 = (g79 ^ g67);
        long g81 = (g80 ^ 1L);
        long g82 = (g81 ^ 1L);
        long g83 = (x0_5 | g65);
        long g84 = (g83 ^ x0_6);
        long g85 = (g84 ^ 1L);
        long g86 = (x1_5 ^ 1L);
        long g87 = (g67 | g86);
        long g88 = (g87 ^ 1L);
        long g89 = (g77 ^ 1L);
        long g90 = (g89 | g67);
        long g91 = (g90 ^ 1L);
        long g92 = (g86 | g89);
        long g93 = (g92 ^ 1L);
        long g94 = (g93 | g91);
        long g95 = (g94 | g88);
        long g96 = (x1_6 ^ g95);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ g85);
        long g99 = (g98 ^ 1L);
        long g100 = (g99 ^ 1L);
        long g101 = (x0_6 | g83);
        long g102 = (g101 ^ x0_7);
        long g103 = (g102 ^ 1L);
        long g104 = (g95 ^ 1L);
        long g105 = (g104 | g85);
        long g106 = (g105 ^ 1L);
        long g107 = (x1_6 ^ 1L);
        long g108 = (g85 | g107);
        long g109 = (g108 ^ 1L);
        long g110 = (g107 | g104);
        long g111 = (g110 ^ 1L);
        long g112 = (g111 | g109);
        long g113 = (g112 | g106);
        long g114 = (x1_7 ^ g113);
        long g115 = (g114 ^ 1L);
        long g116 = (g115 ^ g103);
        long g117 = (g116 ^ 1L);
        long g118 = (g117 ^ 1L);
        long g119 = (x0_7 | g101);
        long g120 = (g119 ^ x0_8);
        long g121 = (g120 ^ 1L);
        long g122 = (g113 ^ 1L);
        long g123 = (x1_7 ^ 1L);
        long g124 = (g123 | g122);
        long g125 = (g124 ^ 1L);
        long g126 = (g103 | g123);
        long g127 = (g126 ^ 1L);
        long g128 = (g103 | g122);
        long g129 = (g128 ^ 1L);
        long g130 = (g129 | g127);
        long g131 = (g130 | g125);
        long g132 = (x1_8 ^ g131);
        long g133 = (g132 ^ 1L);
        long g134 = (g133 ^ g121);
        long g135 = (g134 ^ 1L);
        long g136 = (g135 ^ 1L);
        long g137 = (x0_8 | g119);
        long g138 = (g137 ^ x0_9);
        long g139 = (g138 ^ 1L);
        long g140 = (g131 ^ 1L);
        long g141 = (x1_8 ^ 1L);
        long g142 = (g141 | g140);
        long g143 = (g142 ^ 1L);
        long g144 = (g121 | g141);
        long g145 = (g144 ^ 1L);
        long g146 = (g121 | g140);
        long g147 = (g146 ^ 1L);
        long g148 = (g147 | g145);
        long g149 = (g148 | g143);
        long g150 = (x1_9 ^ g149);
        long g151 = (g150 ^ 1L);
        long g152 = (g151 ^ g139);
        long g153 = (g152 ^ 1L);
        long g154 = (g153 ^ 1L);
        long g155 = (x0_9 | g137);
        long g156 = (g155 ^ x0_10);
        long g157 = (g156 ^ 1L);
        long g158 = (x1_9 ^ 1L);
        long g159 = (g139 | g158);
        long g160 = (g159 ^ 1L);
        long g161 = (g149 ^ 1L);
        long g162 = (g158 | g161);
        long g163 = (g162 ^ 1L);
        long g164 = (g139 | g161);
        long g165 = (g164 ^ 1L);
        long g166 = (g165 | g163);
        long g167 = (g166 | g160);
        long g168 = (x1_10 ^ g167);
        long g169 = (g168 ^ 1L);
        long g170 = (g169 ^ g157);
        long g171 = (g170 ^ 1L);
        long g172 = (g171 ^ 1L);
        long g173 = (x0_10 | g155);
        long g174 = (g173 ^ x0_11);
        long g175 = (g174 ^ 1L);
        long g176 = (g167 ^ 1L);
        long g177 = (g176 | g157);
        long g178 = (g177 ^ 1L);
        long g179 = (x1_10 ^ 1L);
        long g180 = (g179 | g176);
        long g181 = (g180 ^ 1L);
        long g182 = (g157 | g179);
        long g183 = (g182 ^ 1L);
        long g184 = (g183 | g181);
        long g185 = (g184 | g178);
        long g186 = (x1_11 ^ g185);
        long g187 = (g186 ^ 1L);
        long g188 = (g187 ^ g175);
        long g189 = (g188 ^ 1L);
        long g190 = (g189 ^ 1L);
        long g191 = (x0_11 | g173);
        long g192 = (g191 ^ x0_12);
        long g193 = (g192 ^ 1L);
        long g194 = (x1_11 ^ 1L);
        long g195 = (g175 | g194);
        long g196 = (g195 ^ 1L);
        long g197 = (g185 ^ 1L);
        long g198 = (g197 | g175);
        long g199 = (g198 ^ 1L);
        long g200 = (g194 | g197);
        long g201 = (g200 ^ 1L);
        long g202 = (g201 | g199);
        long g203 = (g202 | g196);
        long g204 = (x1_12 ^ g203);
        long g205 = (g204 ^ 1L);
        long g206 = (g205 ^ g193);
        long g207 = (g206 ^ 1L);
        long g208 = (g207 ^ 1L);
        long g209 = (x0_12 | g191);
        long g210 = (g209 ^ x0_13);
        long g211 = (g210 ^ 1L);
        long g212 = (g203 ^ 1L);
        long g213 = (g193 | g212);
        long g214 = (g213 ^ 1L);
        long g215 = (x1_12 ^ 1L);
        long g216 = (g193 | g215);
        long g217 = (g216 ^ 1L);
        long g218 = (g215 | g212);
        long g219 = (g218 ^ 1L);
        long g220 = (g219 | g217);
        long g221 = (g220 | g214);
        long g222 = (x1_13 ^ g221);
        long g223 = (g222 ^ 1L);
        long g224 = (g223 ^ g211);
        long g225 = (g224 ^ 1L);
        long g226 = (g225 ^ 1L);
        long g227 = (x0_13 | g209);
        long g228 = (g227 ^ x0_14);
        long g229 = (g228 ^ 1L);
        long g230 = (x1_13 ^ 1L);
        long g231 = (g211 | g230);
        long g232 = (g231 ^ 1L);
        long g233 = (g221 ^ 1L);
        long g234 = (g233 | g211);
        long g235 = (g234 ^ 1L);
        long g236 = (g230 | g233);
        long g237 = (g236 ^ 1L);
        long g238 = (g237 | g235);
        long g239 = (g238 | g232);
        long g240 = (x1_14 ^ g239);
        long g241 = (g240 ^ 1L);
        long g242 = (g241 ^ g229);
        long g243 = (g242 ^ 1L);
        long g244 = (g243 ^ 1L);
        long g245 = (x0_14 | g227);
        long g246 = (g245 ^ x0_15);
        long g247 = (g246 ^ 1L);
        long g248 = (g239 ^ 1L);
        long g249 = (x1_14 ^ 1L);
        long g250 = (g249 | g248);
        long g251 = (g250 ^ 1L);
        long g252 = (g248 | g229);
        long g253 = (g252 ^ 1L);
        long g254 = (g229 | g249);
        long g255 = (g254 ^ 1L);
        long g256 = (g255 | g253);
        long g257 = (g256 | g251);
        long g258 = (x1_15 ^ g257);
        long g259 = (g258 ^ 1L);
        long g260 = (g259 ^ g247);
        long g261 = (g260 ^ 1L);
        long g262 = (g261 ^ 1L);
        long g263 = (x0_15 | g245);
        long g264 = (g263 ^ x0_16);
        long g265 = (g264 ^ 1L);
        long g266 = (g257 ^ 1L);
        long g267 = (x1_15 ^ 1L);
        long g268 = (g267 | g266);
        long g269 = (g268 ^ 1L);
        long g270 = (g266 | g247);
        long g271 = (g270 ^ 1L);
        long g272 = (g267 | g247);
        long g273 = (g272 ^ 1L);
        long g274 = (g273 | g271);
        long g275 = (g274 | g269);
        long g276 = (x1_16 ^ g275);
        long g277 = (g276 ^ 1L);
        long g278 = (g277 ^ g265);
        long g279 = (g278 ^ 1L);
        long g280 = (g279 ^ 1L);
        long g281 = (x0_16 | g263);
        long g282 = (g281 ^ x0_17);
        long g283 = (g282 ^ 1L);
        long g284 = (g275 ^ 1L);
        long g285 = (g265 | g284);
        long g286 = (g285 ^ 1L);
        long g287 = (x1_16 ^ 1L);
        long g288 = (g287 | g284);
        long g289 = (g288 ^ 1L);
        long g290 = (g265 | g287);
        long g291 = (g290 ^ 1L);
        long g292 = (g291 | g289);
        long g293 = (g292 | g286);
        long g294 = (x1_17 ^ g293);
        long g295 = (g294 ^ 1L);
        long g296 = (g295 ^ g283);
        long g297 = (g296 ^ 1L);
        long g298 = (g297 ^ 1L);
        long g299 = (x0_17 | g281);
        long g300 = (g299 ^ x0_18);
        long g301 = (g300 ^ 1L);
        long g302 = (x1_17 ^ 1L);
        long g303 = (g283 | g302);
        long g304 = (g303 ^ 1L);
        long g305 = (g293 ^ 1L);
        long g306 = (g302 | g305);
        long g307 = (g306 ^ 1L);
        long g308 = (g283 | g305);
        long g309 = (g308 ^ 1L);
        long g310 = (g309 | g307);
        long g311 = (g310 | g304);
        long g312 = (x1_18 ^ g311);
        long g313 = (g312 ^ 1L);
        long g314 = (g313 ^ g301);
        long g315 = (g314 ^ 1L);
        long g316 = (g315 ^ 1L);
        long g317 = (x0_18 | g299);
        long g318 = (g317 ^ x0_19);
        long g319 = (g318 ^ 1L);
        long g320 = (g311 ^ 1L);
        long g321 = (x1_18 ^ 1L);
        long g322 = (g321 | g320);
        long g323 = (g322 ^ 1L);
        long g324 = (g321 | g301);
        long g325 = (g324 ^ 1L);
        long g326 = (g320 | g301);
        long g327 = (g326 ^ 1L);
        long g328 = (g327 | g325);
        long g329 = (g328 | g323);
        long g330 = (x1_19 ^ g329);
        long g331 = (g330 ^ 1L);
        long g332 = (g331 ^ g319);
        long g333 = (g332 ^ 1L);
        long g334 = (g333 ^ 1L);
        long g335 = (x0_19 | g317);
        long g336 = (g335 ^ x0_20);
        long g337 = (g336 ^ 1L);
        long g338 = (x1_19 ^ 1L);
        long g339 = (g338 | g319);
        long g340 = (g339 ^ 1L);
        long g341 = (g329 ^ 1L);
        long g342 = (g338 | g341);
        long g343 = (g342 ^ 1L);
        long g344 = (g319 | g341);
        long g345 = (g344 ^ 1L);
        long g346 = (g345 | g343);
        long g347 = (g346 | g340);
        long g348 = (x1_20 ^ g347);
        long g349 = (g348 ^ 1L);
        long g350 = (g349 ^ g337);
        long g351 = (g350 ^ 1L);
        long g352 = (g351 ^ 1L);
        long g353 = (x0_20 | g335);
        long g354 = (g353 ^ x0_21);
        long g355 = (g354 ^ 1L);
        long g356 = (g347 ^ 1L);
        long g357 = (x1_20 ^ 1L);
        long g358 = (g357 | g356);
        long g359 = (g358 ^ 1L);
        long g360 = (g337 | g357);
        long g361 = (g360 ^ 1L);
        long g362 = (g356 | g337);
        long g363 = (g362 ^ 1L);
        long g364 = (g363 | g361);
        long g365 = (g364 | g359);
        long g366 = (x1_21 ^ g365);
        long g367 = (g366 ^ 1L);
        long g368 = (g367 ^ g355);
        long g369 = (g368 ^ 1L);
        long g370 = (g369 ^ 1L);
        long g371 = (x0_21 | g353);
        long g372 = (g371 ^ x0_22);
        long g373 = (g372 ^ 1L);
        long g374 = (g365 ^ 1L);
        long g375 = (x1_21 ^ 1L);
        long g376 = (g375 | g374);
        long g377 = (g376 ^ 1L);
        long g378 = (g374 | g355);
        long g379 = (g378 ^ 1L);
        long g380 = (g375 | g355);
        long g381 = (g380 ^ 1L);
        long g382 = (g381 | g379);
        long g383 = (g382 | g377);
        long g384 = (x1_22 ^ g383);
        long g385 = (g384 ^ 1L);
        long g386 = (g385 ^ g373);
        long g387 = (g386 ^ 1L);
        long g388 = (g387 ^ 1L);
        long g389 = (x0_22 | g371);
        long g390 = (g389 ^ x0_23);
        long g391 = (g390 ^ 1L);
        long g392 = (x1_22 ^ 1L);
        long g393 = (g373 | g392);
        long g394 = (g393 ^ 1L);
        long g395 = (g383 ^ 1L);
        long g396 = (g373 | g395);
        long g397 = (g396 ^ 1L);
        long g398 = (g392 | g395);
        long g399 = (g398 ^ 1L);
        long g400 = (g399 | g397);
        long g401 = (g400 | g394);
        long g402 = (x1_23 ^ g401);
        long g403 = (g402 ^ 1L);
        long g404 = (g403 ^ g391);
        long g405 = (g404 ^ 1L);
        long g406 = (g405 ^ 1L);
        long g407 = (x0_23 | g389);
        long g408 = (g407 ^ x0_24);
        long g409 = (g408 ^ 1L);
        long g410 = (g401 ^ 1L);
        long g411 = (x1_23 ^ 1L);
        long g412 = (g411 | g410);
        long g413 = (g412 ^ 1L);
        long g414 = (g410 | g391);
        long g415 = (g414 ^ 1L);
        long g416 = (g411 | g391);
        long g417 = (g416 ^ 1L);
        long g418 = (g417 | g415);
        long g419 = (g418 | g413);
        long g420 = (x1_24 ^ g419);
        long g421 = (g420 ^ 1L);
        long g422 = (g421 ^ g409);
        long g423 = (g422 ^ 1L);
        long g424 = (g423 ^ 1L);
        long g425 = (x0_24 | g407);
        long g426 = (g425 ^ x0_25);
        long g427 = (g426 ^ 1L);
        long g428 = (g419 ^ 1L);
        long g429 = (g409 | g428);
        long g430 = (g429 ^ 1L);
        long g431 = (x1_24 ^ 1L);
        long g432 = (g409 | g431);
        long g433 = (g432 ^ 1L);
        long g434 = (g431 | g428);
        long g435 = (g434 ^ 1L);
        long g436 = (g435 | g433);
        long g437 = (g436 | g430);
        long g438 = (x1_25 ^ g437);
        long g439 = (g438 ^ 1L);
        long g440 = (g439 ^ g427);
        long g441 = (g440 ^ 1L);
        long g442 = (g441 ^ 1L);
        long g443 = (x0_25 | g425);
        long g444 = (g443 ^ x0_26);
        long g445 = (g444 ^ 1L);
        long g446 = (x1_25 ^ 1L);
        long g447 = (g446 | g427);
        long g448 = (g447 ^ 1L);
        long g449 = (g437 ^ 1L);
        long g450 = (g446 | g449);
        long g451 = (g450 ^ 1L);
        long g452 = (g449 | g427);
        long g453 = (g452 ^ 1L);
        long g454 = (g453 | g451);
        long g455 = (g454 | g448);
        long g456 = (x1_26 ^ g455);
        long g457 = (g456 ^ 1L);
        long g458 = (g457 ^ g445);
        long g459 = (g458 ^ 1L);
        long g460 = (g459 ^ 1L);
        long g461 = (x0_26 | g443);
        long g462 = (g461 ^ x0_27);
        long g463 = (g462 ^ 1L);
        long g464 = (x1_26 ^ 1L);
        long g465 = (g464 | g445);
        long g466 = (g465 ^ 1L);
        long g467 = (g455 ^ 1L);
        long g468 = (g464 | g467);
        long g469 = (g468 ^ 1L);
        long g470 = (g467 | g445);
        long g471 = (g470 ^ 1L);
        long g472 = (g471 | g469);
        long g473 = (g472 | g466);
        long g474 = (x1_27 ^ g473);
        long g475 = (g474 ^ 1L);
        long g476 = (g475 ^ g463);
        long g477 = (g476 ^ 1L);
        long g478 = (g477 ^ 1L);
        long g479 = (x0_27 | g461);
        long g480 = (g479 ^ x0_28);
        long g481 = (g480 ^ 1L);
        long g482 = (x1_27 ^ 1L);
        long g483 = (g463 | g482);
        long g484 = (g483 ^ 1L);
        long g485 = (g473 ^ 1L);
        long g486 = (g482 | g485);
        long g487 = (g486 ^ 1L);
        long g488 = (g485 | g463);
        long g489 = (g488 ^ 1L);
        long g490 = (g489 | g487);
        long g491 = (g490 | g484);
        long g492 = (x1_28 ^ g491);
        long g493 = (g492 ^ 1L);
        long g494 = (g493 ^ g481);
        long g495 = (g494 ^ 1L);
        long g496 = (g495 ^ 1L);
        long g497 = (x0_28 | g479);
        long g498 = (g497 ^ x0_29);
        long g499 = (g498 ^ 1L);
        long g500 = (g491 ^ 1L);
        long g501 = (x1_28 ^ 1L);
        long g502 = (g501 | g500);
        long g503 = (g502 ^ 1L);
        long g504 = (g481 | g501);
        long g505 = (g504 ^ 1L);
        long g506 = (g500 | g481);
        long g507 = (g506 ^ 1L);
        long g508 = (g507 | g505);
        long g509 = (g508 | g503);
        long g510 = (x1_29 ^ g509);
        long g511 = (g510 ^ 1L);
        long g512 = (g511 ^ g499);
        long g513 = (g512 ^ 1L);
        long g514 = (g513 ^ 1L);
        long g515 = (x0_29 | g497);
        long g516 = (g515 ^ x0_30);
        long g517 = (g516 ^ 1L);
        long g518 = (g509 ^ 1L);
        long g519 = (x1_29 ^ 1L);
        long g520 = (g519 | g518);
        long g521 = (g520 ^ 1L);
        long g522 = (g499 | g519);
        long g523 = (g522 ^ 1L);
        long g524 = (g499 | g518);
        long g525 = (g524 ^ 1L);
        long g526 = (g525 | g523);
        long g527 = (g526 | g521);
        long g528 = (x1_30 ^ g527);
        long g529 = (g528 ^ 1L);
        long g530 = (g529 ^ g517);
        long g531 = (g530 ^ 1L);
        long g532 = (g531 ^ 1L);
        long g533 = (x0_30 | g515);
        long g534 = (g533 ^ x0_31);
        long g535 = (g534 ^ 1L);
        long g536 = (g527 ^ 1L);
        long g537 = (g536 | g517);
        long g538 = (g537 ^ 1L);
        long g539 = (x1_30 ^ 1L);
        long g540 = (g539 | g517);
        long g541 = (g540 ^ 1L);
        long g542 = (g539 | g536);
        long g543 = (g542 ^ 1L);
        long g544 = (g543 | g541);
        long g545 = (g544 | g538);
        long g546 = (x1_31 ^ g545);
        long g547 = (g546 ^ 1L);
        long g548 = (g547 ^ g535);
        long g549 = (g548 ^ 1L);
        long g550 = (g549 ^ 1L);
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
        long w32 = cat(w31, g550, 1);
        long w33 = cat(w32, g532, 1);
        long w34 = cat(w33, g514, 1);
        long w35 = cat(w34, g496, 1);
        long w36 = cat(w35, g478, 1);
        long w37 = cat(w36, g460, 1);
        long w38 = cat(w37, g442, 1);
        long w39 = cat(w38, g424, 1);
        long w40 = cat(w39, g406, 1);
        long w41 = cat(w40, g388, 1);
        long w42 = cat(w41, g370, 1);
        long w43 = cat(w42, g352, 1);
        long w44 = cat(w43, g334, 1);
        long w45 = cat(w44, g316, 1);
        long w46 = cat(w45, g298, 1);
        long w47 = cat(w46, g280, 1);
        long w48 = cat(w47, g262, 1);
        long w49 = cat(w48, g244, 1);
        long w50 = cat(w49, g226, 1);
        long w51 = cat(w50, g208, 1);
        long w52 = cat(w51, g190, 1);
        long w53 = cat(w52, g172, 1);
        long w54 = cat(w53, g154, 1);
        long w55 = cat(w54, g136, 1);
        long w56 = cat(w55, g118, 1);
        long w57 = cat(w56, g100, 1);
        long w58 = cat(w57, g82, 1);
        long w59 = cat(w58, g64, 1);
        long w60 = cat(w59, g46, 1);
        long w61 = cat(w60, g28, 1);
        long w62 = cat(w61, g11, 1);
        long w63 = cat(w62, g2, 1);
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
                    answers.Append(((ulong) emu_sub_gpr_gpr_32__reg_rdi__csharp(values[0], values[1])).ToString());
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
