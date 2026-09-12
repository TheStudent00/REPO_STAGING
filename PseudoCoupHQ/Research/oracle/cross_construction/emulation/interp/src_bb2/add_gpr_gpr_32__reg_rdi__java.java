import java.io.*;
import java.util.*;

public class Emu {
    static long m(long x, int w) {
        if (w >= 64) { return x; }
        return x & ((1L << w) - 1L);
    }
    static long s(long x, int w) {
        if (w >= 64) { return x; }
        return (x << (64 - w)) >> (64 - w);
    }
    static long add(long a, long b, int w) { return m(a + b, w); }
    static long sub(long a, long b, int w) { return m(a - b, w); }
    static long mul(long a, long b, int w) { return m(a * b, w); }
    static long band(long a, long b, int w) { return m(a & b, w); }
    static long bor(long a, long b, int w) { return m(a | b, w); }
    static long bxor(long a, long b, int w) { return m(a ^ b, w); }
    static long bnot(long a, int w) { return m(~a, w); }
    static long bneg(long a, int w) { return m(-a, w); }
    static long shl(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(a << n, w);
    }
    static long lshr(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(m(a, w) >>> n, w);
    }
    static long ashr(long a, long n, int w) {
        long v = s(a, w);
        long k = n;
        if (k >= w) { k = w - 1; }
        return m(v >> k, w);
    }
    static long udiv(long a, long b, int w) {
        return m(Long.divideUnsigned(m(a, w), m(b, w)), w);
    }
    static long urem(long a, long b, int w) {
        return m(Long.remainderUnsigned(m(a, w), m(b, w)), w);
    }
    static long sdiv(long a, long b, int w) {
        return m(s(a, w) / s(b, w), w);
    }
    static long srem(long a, long b, int w) {
        return m(s(a, w) % s(b, w), w);
    }
    static boolean ult(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) < 0;
    }
    static boolean ule(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) <= 0;
    }
    static boolean ugt(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) > 0;
    }
    static boolean uge(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) >= 0;
    }
    static boolean slt(long a, long b, int w) { return s(a, w) < s(b, w); }
    static boolean sle(long a, long b, int w) { return s(a, w) <= s(b, w); }
    static boolean sgt(long a, long b, int w) { return s(a, w) > s(b, w); }
    static boolean sge(long a, long b, int w) { return s(a, w) >= s(b, w); }
    static boolean eq(long a, long b, int w) { return m(a, w) == m(b, w); }
    static boolean ne(long a, long b, int w) { return m(a, w) != m(b, w); }
    static long cat(long hi, long lo, int lw) {
        return (hi << lw) | m(lo, lw);
    }
    static long ext(long x, int hi, int lo) {
        return m(x >>> lo, hi - lo + 1);
    }
    static long sext(long x, int fromw, int tow) {
        return m(s(x, fromw), tow);
    }
    static double b2f(long x, int w) {
        if (w == 32) { return Float.intBitsToFloat((int) m(x, 32)); }
        return Double.longBitsToDouble(x);
    }
    static long f2b(double f, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(Float.floatToRawIntBits((float) f));
        }
        return Double.doubleToRawLongBits(f);
    }
    static long fadd(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    + Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) + b2f(b, w), w);
    }
    static long fsub(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    - Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) - b2f(b, w), w);
    }
    static long fmul(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    * Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) * b2f(b, w), w);
    }
    static long fdiv(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    / Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) / b2f(b, w), w);
    }
    static long i2f(long x, int fromw, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(
                Float.floatToRawIntBits((float) s(x, fromw)));
        }
        return Double.doubleToRawLongBits((double) s(x, fromw));
    }
    static long u2f(long x, int fromw, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(Float.floatToRawIntBits(
                (float) Long.parseUnsignedLong(
                    Long.toUnsignedString(m(x, fromw)))));
        }
        return Double.doubleToRawLongBits(
            (double) m(x, fromw));
    }
    static long fwiden(long x, int fromw, int w) {
        return f2b(b2f(x, fromw), w);
    }

    // task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
    // one named local per gate, over the term of add_gpr_gpr_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
    static long emu_add_gpr_gpr_32__reg_rdi__java(long a, long b) {
        long x0_0 = ext(a, 0, 0);
        long x1_0 = ext(b, 0, 0);
        long x1_1 = ext(b, 1, 1);
        long x0_1 = ext(a, 1, 1);
        long x1_2 = ext(b, 2, 2);
        long x0_2 = ext(a, 2, 2);
        long x1_3 = ext(b, 3, 3);
        long x0_3 = ext(a, 3, 3);
        long x1_4 = ext(b, 4, 4);
        long x0_4 = ext(a, 4, 4);
        long x1_5 = ext(b, 5, 5);
        long x0_5 = ext(a, 5, 5);
        long x1_6 = ext(b, 6, 6);
        long x0_6 = ext(a, 6, 6);
        long x1_7 = ext(b, 7, 7);
        long x0_7 = ext(a, 7, 7);
        long x1_8 = ext(b, 8, 8);
        long x0_8 = ext(a, 8, 8);
        long x1_9 = ext(b, 9, 9);
        long x0_9 = ext(a, 9, 9);
        long x1_10 = ext(b, 10, 10);
        long x0_10 = ext(a, 10, 10);
        long x1_11 = ext(b, 11, 11);
        long x0_11 = ext(a, 11, 11);
        long x1_12 = ext(b, 12, 12);
        long x0_12 = ext(a, 12, 12);
        long x1_13 = ext(b, 13, 13);
        long x0_13 = ext(a, 13, 13);
        long x1_14 = ext(b, 14, 14);
        long x0_14 = ext(a, 14, 14);
        long x1_15 = ext(b, 15, 15);
        long x0_15 = ext(a, 15, 15);
        long x1_16 = ext(b, 16, 16);
        long x0_16 = ext(a, 16, 16);
        long x1_17 = ext(b, 17, 17);
        long x0_17 = ext(a, 17, 17);
        long x1_18 = ext(b, 18, 18);
        long x0_18 = ext(a, 18, 18);
        long x1_19 = ext(b, 19, 19);
        long x0_19 = ext(a, 19, 19);
        long x1_20 = ext(b, 20, 20);
        long x0_20 = ext(a, 20, 20);
        long x1_21 = ext(b, 21, 21);
        long x0_21 = ext(a, 21, 21);
        long x1_22 = ext(b, 22, 22);
        long x0_22 = ext(a, 22, 22);
        long x1_23 = ext(b, 23, 23);
        long x0_23 = ext(a, 23, 23);
        long x1_24 = ext(b, 24, 24);
        long x0_24 = ext(a, 24, 24);
        long x1_25 = ext(b, 25, 25);
        long x0_25 = ext(a, 25, 25);
        long x1_26 = ext(b, 26, 26);
        long x0_26 = ext(a, 26, 26);
        long x1_27 = ext(b, 27, 27);
        long x0_27 = ext(a, 27, 27);
        long x1_28 = ext(b, 28, 28);
        long x0_28 = ext(a, 28, 28);
        long x1_29 = ext(b, 29, 29);
        long x0_29 = ext(a, 29, 29);
        long x1_30 = ext(b, 30, 30);
        long x0_30 = ext(a, 30, 30);
        long x1_31 = ext(b, 31, 31);
        long x0_31 = ext(a, 31, 31);
        long g0 = (x1_0 ^ x0_0);
        long g1 = (g0 ^ 1L);
        long g2 = (g1 ^ 1L);
        long g3 = (x1_0 ^ 1L);
        long g4 = (x0_0 ^ 1L);
        long g5 = (g4 | g3);
        long g6 = (x1_1 ^ g5);
        long g7 = (g6 ^ 1L);
        long g8 = (x0_1 ^ g7);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 ^ 1L);
        long g11 = (x1_1 ^ 1L);
        long g12 = (g11 | g5);
        long g13 = (g12 ^ 1L);
        long g14 = (x0_1 ^ 1L);
        long g15 = (g14 | g5);
        long g16 = (g15 ^ 1L);
        long g17 = (g14 | g11);
        long g18 = (g17 ^ 1L);
        long g19 = (g18 | g16);
        long g20 = (g19 | g13);
        long g21 = (x1_2 ^ g20);
        long g22 = (g21 ^ 1L);
        long g23 = (x0_2 ^ g22);
        long g24 = (g23 ^ 1L);
        long g25 = (g20 ^ 1L);
        long g26 = (x1_2 ^ 1L);
        long g27 = (g26 | g25);
        long g28 = (g27 ^ 1L);
        long g29 = (x0_2 ^ 1L);
        long g30 = (g29 | g25);
        long g31 = (g30 ^ 1L);
        long g32 = (g29 | g26);
        long g33 = (g32 ^ 1L);
        long g34 = (g33 | g31);
        long g35 = (g34 | g28);
        long g36 = (x1_3 ^ g35);
        long g37 = (g36 ^ 1L);
        long g38 = (x0_3 ^ g37);
        long g39 = (g38 ^ 1L);
        long g40 = (g35 ^ 1L);
        long g41 = (x1_3 ^ 1L);
        long g42 = (g41 | g40);
        long g43 = (g42 ^ 1L);
        long g44 = (x0_3 ^ 1L);
        long g45 = (g44 | g40);
        long g46 = (g45 ^ 1L);
        long g47 = (g44 | g41);
        long g48 = (g47 ^ 1L);
        long g49 = (g48 | g46);
        long g50 = (g49 | g43);
        long g51 = (x1_4 ^ g50);
        long g52 = (g51 ^ 1L);
        long g53 = (x0_4 ^ g52);
        long g54 = (g53 ^ 1L);
        long g55 = (g50 ^ 1L);
        long g56 = (x1_4 ^ 1L);
        long g57 = (g56 | g55);
        long g58 = (g57 ^ 1L);
        long g59 = (x0_4 ^ 1L);
        long g60 = (g59 | g55);
        long g61 = (g60 ^ 1L);
        long g62 = (g59 | g56);
        long g63 = (g62 ^ 1L);
        long g64 = (g63 | g61);
        long g65 = (g64 | g58);
        long g66 = (x1_5 ^ g65);
        long g67 = (g66 ^ 1L);
        long g68 = (x0_5 ^ g67);
        long g69 = (g68 ^ 1L);
        long g70 = (g65 ^ 1L);
        long g71 = (x1_5 ^ 1L);
        long g72 = (g71 | g70);
        long g73 = (g72 ^ 1L);
        long g74 = (x0_5 ^ 1L);
        long g75 = (g74 | g70);
        long g76 = (g75 ^ 1L);
        long g77 = (g74 | g71);
        long g78 = (g77 ^ 1L);
        long g79 = (g78 | g76);
        long g80 = (g79 | g73);
        long g81 = (x1_6 ^ g80);
        long g82 = (g81 ^ 1L);
        long g83 = (x0_6 ^ g82);
        long g84 = (g83 ^ 1L);
        long g85 = (g80 ^ 1L);
        long g86 = (x1_6 ^ 1L);
        long g87 = (g86 | g85);
        long g88 = (g87 ^ 1L);
        long g89 = (x0_6 ^ 1L);
        long g90 = (g89 | g85);
        long g91 = (g90 ^ 1L);
        long g92 = (g89 | g86);
        long g93 = (g92 ^ 1L);
        long g94 = (g93 | g91);
        long g95 = (g94 | g88);
        long g96 = (x1_7 ^ g95);
        long g97 = (g96 ^ 1L);
        long g98 = (x0_7 ^ g97);
        long g99 = (g98 ^ 1L);
        long g100 = (g95 ^ 1L);
        long g101 = (x1_7 ^ 1L);
        long g102 = (g101 | g100);
        long g103 = (g102 ^ 1L);
        long g104 = (x0_7 ^ 1L);
        long g105 = (g104 | g100);
        long g106 = (g105 ^ 1L);
        long g107 = (g104 | g101);
        long g108 = (g107 ^ 1L);
        long g109 = (g108 | g106);
        long g110 = (g109 | g103);
        long g111 = (x1_8 ^ g110);
        long g112 = (g111 ^ 1L);
        long g113 = (x0_8 ^ g112);
        long g114 = (g113 ^ 1L);
        long g115 = (g110 ^ 1L);
        long g116 = (x1_8 ^ 1L);
        long g117 = (g116 | g115);
        long g118 = (g117 ^ 1L);
        long g119 = (x0_8 ^ 1L);
        long g120 = (g119 | g115);
        long g121 = (g120 ^ 1L);
        long g122 = (g119 | g116);
        long g123 = (g122 ^ 1L);
        long g124 = (g123 | g121);
        long g125 = (g124 | g118);
        long g126 = (x1_9 ^ g125);
        long g127 = (g126 ^ 1L);
        long g128 = (x0_9 ^ g127);
        long g129 = (g128 ^ 1L);
        long g130 = (g125 ^ 1L);
        long g131 = (x1_9 ^ 1L);
        long g132 = (g131 | g130);
        long g133 = (g132 ^ 1L);
        long g134 = (x0_9 ^ 1L);
        long g135 = (g134 | g130);
        long g136 = (g135 ^ 1L);
        long g137 = (g134 | g131);
        long g138 = (g137 ^ 1L);
        long g139 = (g138 | g136);
        long g140 = (g139 | g133);
        long g141 = (x1_10 ^ g140);
        long g142 = (g141 ^ 1L);
        long g143 = (x0_10 ^ g142);
        long g144 = (g143 ^ 1L);
        long g145 = (g140 ^ 1L);
        long g146 = (x1_10 ^ 1L);
        long g147 = (g146 | g145);
        long g148 = (g147 ^ 1L);
        long g149 = (x0_10 ^ 1L);
        long g150 = (g149 | g145);
        long g151 = (g150 ^ 1L);
        long g152 = (g149 | g146);
        long g153 = (g152 ^ 1L);
        long g154 = (g153 | g151);
        long g155 = (g154 | g148);
        long g156 = (x1_11 ^ g155);
        long g157 = (g156 ^ 1L);
        long g158 = (x0_11 ^ g157);
        long g159 = (g158 ^ 1L);
        long g160 = (g155 ^ 1L);
        long g161 = (x1_11 ^ 1L);
        long g162 = (g161 | g160);
        long g163 = (g162 ^ 1L);
        long g164 = (x0_11 ^ 1L);
        long g165 = (g164 | g160);
        long g166 = (g165 ^ 1L);
        long g167 = (g164 | g161);
        long g168 = (g167 ^ 1L);
        long g169 = (g168 | g166);
        long g170 = (g169 | g163);
        long g171 = (x1_12 ^ g170);
        long g172 = (g171 ^ 1L);
        long g173 = (x0_12 ^ g172);
        long g174 = (g173 ^ 1L);
        long g175 = (g170 ^ 1L);
        long g176 = (x1_12 ^ 1L);
        long g177 = (g176 | g175);
        long g178 = (g177 ^ 1L);
        long g179 = (x0_12 ^ 1L);
        long g180 = (g179 | g175);
        long g181 = (g180 ^ 1L);
        long g182 = (g179 | g176);
        long g183 = (g182 ^ 1L);
        long g184 = (g183 | g181);
        long g185 = (g184 | g178);
        long g186 = (x1_13 ^ g185);
        long g187 = (g186 ^ 1L);
        long g188 = (x0_13 ^ g187);
        long g189 = (g188 ^ 1L);
        long g190 = (g185 ^ 1L);
        long g191 = (x1_13 ^ 1L);
        long g192 = (g191 | g190);
        long g193 = (g192 ^ 1L);
        long g194 = (x0_13 ^ 1L);
        long g195 = (g194 | g190);
        long g196 = (g195 ^ 1L);
        long g197 = (g194 | g191);
        long g198 = (g197 ^ 1L);
        long g199 = (g198 | g196);
        long g200 = (g199 | g193);
        long g201 = (x1_14 ^ g200);
        long g202 = (g201 ^ 1L);
        long g203 = (x0_14 ^ g202);
        long g204 = (g203 ^ 1L);
        long g205 = (g200 ^ 1L);
        long g206 = (x1_14 ^ 1L);
        long g207 = (g206 | g205);
        long g208 = (g207 ^ 1L);
        long g209 = (x0_14 ^ 1L);
        long g210 = (g209 | g205);
        long g211 = (g210 ^ 1L);
        long g212 = (g209 | g206);
        long g213 = (g212 ^ 1L);
        long g214 = (g213 | g211);
        long g215 = (g214 | g208);
        long g216 = (x1_15 ^ g215);
        long g217 = (g216 ^ 1L);
        long g218 = (x0_15 ^ g217);
        long g219 = (g218 ^ 1L);
        long g220 = (g215 ^ 1L);
        long g221 = (x1_15 ^ 1L);
        long g222 = (g221 | g220);
        long g223 = (g222 ^ 1L);
        long g224 = (x0_15 ^ 1L);
        long g225 = (g224 | g220);
        long g226 = (g225 ^ 1L);
        long g227 = (g224 | g221);
        long g228 = (g227 ^ 1L);
        long g229 = (g228 | g226);
        long g230 = (g229 | g223);
        long g231 = (x1_16 ^ g230);
        long g232 = (g231 ^ 1L);
        long g233 = (x0_16 ^ g232);
        long g234 = (g233 ^ 1L);
        long g235 = (g230 ^ 1L);
        long g236 = (x1_16 ^ 1L);
        long g237 = (g236 | g235);
        long g238 = (g237 ^ 1L);
        long g239 = (x0_16 ^ 1L);
        long g240 = (g239 | g235);
        long g241 = (g240 ^ 1L);
        long g242 = (g239 | g236);
        long g243 = (g242 ^ 1L);
        long g244 = (g243 | g241);
        long g245 = (g244 | g238);
        long g246 = (x1_17 ^ g245);
        long g247 = (g246 ^ 1L);
        long g248 = (x0_17 ^ g247);
        long g249 = (g248 ^ 1L);
        long g250 = (g245 ^ 1L);
        long g251 = (x1_17 ^ 1L);
        long g252 = (g251 | g250);
        long g253 = (g252 ^ 1L);
        long g254 = (x0_17 ^ 1L);
        long g255 = (g254 | g250);
        long g256 = (g255 ^ 1L);
        long g257 = (g254 | g251);
        long g258 = (g257 ^ 1L);
        long g259 = (g258 | g256);
        long g260 = (g259 | g253);
        long g261 = (x1_18 ^ g260);
        long g262 = (g261 ^ 1L);
        long g263 = (x0_18 ^ g262);
        long g264 = (g263 ^ 1L);
        long g265 = (g260 ^ 1L);
        long g266 = (x1_18 ^ 1L);
        long g267 = (g266 | g265);
        long g268 = (g267 ^ 1L);
        long g269 = (x0_18 ^ 1L);
        long g270 = (g269 | g265);
        long g271 = (g270 ^ 1L);
        long g272 = (g269 | g266);
        long g273 = (g272 ^ 1L);
        long g274 = (g273 | g271);
        long g275 = (g274 | g268);
        long g276 = (x1_19 ^ g275);
        long g277 = (g276 ^ 1L);
        long g278 = (x0_19 ^ g277);
        long g279 = (g278 ^ 1L);
        long g280 = (g275 ^ 1L);
        long g281 = (x1_19 ^ 1L);
        long g282 = (g281 | g280);
        long g283 = (g282 ^ 1L);
        long g284 = (x0_19 ^ 1L);
        long g285 = (g284 | g280);
        long g286 = (g285 ^ 1L);
        long g287 = (g284 | g281);
        long g288 = (g287 ^ 1L);
        long g289 = (g288 | g286);
        long g290 = (g289 | g283);
        long g291 = (x1_20 ^ g290);
        long g292 = (g291 ^ 1L);
        long g293 = (x0_20 ^ g292);
        long g294 = (g293 ^ 1L);
        long g295 = (g290 ^ 1L);
        long g296 = (x1_20 ^ 1L);
        long g297 = (g296 | g295);
        long g298 = (g297 ^ 1L);
        long g299 = (x0_20 ^ 1L);
        long g300 = (g299 | g295);
        long g301 = (g300 ^ 1L);
        long g302 = (g299 | g296);
        long g303 = (g302 ^ 1L);
        long g304 = (g303 | g301);
        long g305 = (g304 | g298);
        long g306 = (x1_21 ^ g305);
        long g307 = (g306 ^ 1L);
        long g308 = (x0_21 ^ g307);
        long g309 = (g308 ^ 1L);
        long g310 = (g305 ^ 1L);
        long g311 = (x1_21 ^ 1L);
        long g312 = (g311 | g310);
        long g313 = (g312 ^ 1L);
        long g314 = (x0_21 ^ 1L);
        long g315 = (g314 | g310);
        long g316 = (g315 ^ 1L);
        long g317 = (g314 | g311);
        long g318 = (g317 ^ 1L);
        long g319 = (g318 | g316);
        long g320 = (g319 | g313);
        long g321 = (x1_22 ^ g320);
        long g322 = (g321 ^ 1L);
        long g323 = (x0_22 ^ g322);
        long g324 = (g323 ^ 1L);
        long g325 = (g320 ^ 1L);
        long g326 = (x1_22 ^ 1L);
        long g327 = (g326 | g325);
        long g328 = (g327 ^ 1L);
        long g329 = (x0_22 ^ 1L);
        long g330 = (g329 | g325);
        long g331 = (g330 ^ 1L);
        long g332 = (g329 | g326);
        long g333 = (g332 ^ 1L);
        long g334 = (g333 | g331);
        long g335 = (g334 | g328);
        long g336 = (x1_23 ^ g335);
        long g337 = (g336 ^ 1L);
        long g338 = (x0_23 ^ g337);
        long g339 = (g338 ^ 1L);
        long g340 = (g335 ^ 1L);
        long g341 = (x1_23 ^ 1L);
        long g342 = (g341 | g340);
        long g343 = (g342 ^ 1L);
        long g344 = (x0_23 ^ 1L);
        long g345 = (g344 | g340);
        long g346 = (g345 ^ 1L);
        long g347 = (g344 | g341);
        long g348 = (g347 ^ 1L);
        long g349 = (g348 | g346);
        long g350 = (g349 | g343);
        long g351 = (x1_24 ^ g350);
        long g352 = (g351 ^ 1L);
        long g353 = (x0_24 ^ g352);
        long g354 = (g353 ^ 1L);
        long g355 = (g350 ^ 1L);
        long g356 = (x1_24 ^ 1L);
        long g357 = (g356 | g355);
        long g358 = (g357 ^ 1L);
        long g359 = (x0_24 ^ 1L);
        long g360 = (g359 | g355);
        long g361 = (g360 ^ 1L);
        long g362 = (g359 | g356);
        long g363 = (g362 ^ 1L);
        long g364 = (g363 | g361);
        long g365 = (g364 | g358);
        long g366 = (x1_25 ^ g365);
        long g367 = (g366 ^ 1L);
        long g368 = (x0_25 ^ g367);
        long g369 = (g368 ^ 1L);
        long g370 = (g365 ^ 1L);
        long g371 = (x1_25 ^ 1L);
        long g372 = (g371 | g370);
        long g373 = (g372 ^ 1L);
        long g374 = (x0_25 ^ 1L);
        long g375 = (g374 | g370);
        long g376 = (g375 ^ 1L);
        long g377 = (g374 | g371);
        long g378 = (g377 ^ 1L);
        long g379 = (g378 | g376);
        long g380 = (g379 | g373);
        long g381 = (x1_26 ^ g380);
        long g382 = (g381 ^ 1L);
        long g383 = (x0_26 ^ g382);
        long g384 = (g383 ^ 1L);
        long g385 = (g380 ^ 1L);
        long g386 = (x1_26 ^ 1L);
        long g387 = (g386 | g385);
        long g388 = (g387 ^ 1L);
        long g389 = (x0_26 ^ 1L);
        long g390 = (g389 | g385);
        long g391 = (g390 ^ 1L);
        long g392 = (g389 | g386);
        long g393 = (g392 ^ 1L);
        long g394 = (g393 | g391);
        long g395 = (g394 | g388);
        long g396 = (x1_27 ^ g395);
        long g397 = (g396 ^ 1L);
        long g398 = (x0_27 ^ g397);
        long g399 = (g398 ^ 1L);
        long g400 = (g395 ^ 1L);
        long g401 = (x1_27 ^ 1L);
        long g402 = (g401 | g400);
        long g403 = (g402 ^ 1L);
        long g404 = (x0_27 ^ 1L);
        long g405 = (g404 | g400);
        long g406 = (g405 ^ 1L);
        long g407 = (g404 | g401);
        long g408 = (g407 ^ 1L);
        long g409 = (g408 | g406);
        long g410 = (g409 | g403);
        long g411 = (x1_28 ^ g410);
        long g412 = (g411 ^ 1L);
        long g413 = (x0_28 ^ g412);
        long g414 = (g413 ^ 1L);
        long g415 = (g410 ^ 1L);
        long g416 = (x1_28 ^ 1L);
        long g417 = (g416 | g415);
        long g418 = (g417 ^ 1L);
        long g419 = (x0_28 ^ 1L);
        long g420 = (g419 | g415);
        long g421 = (g420 ^ 1L);
        long g422 = (g419 | g416);
        long g423 = (g422 ^ 1L);
        long g424 = (g423 | g421);
        long g425 = (g424 | g418);
        long g426 = (x1_29 ^ g425);
        long g427 = (g426 ^ 1L);
        long g428 = (x0_29 ^ g427);
        long g429 = (g428 ^ 1L);
        long g430 = (g425 ^ 1L);
        long g431 = (x1_29 ^ 1L);
        long g432 = (g431 | g430);
        long g433 = (g432 ^ 1L);
        long g434 = (x0_29 ^ 1L);
        long g435 = (g434 | g430);
        long g436 = (g435 ^ 1L);
        long g437 = (g434 | g431);
        long g438 = (g437 ^ 1L);
        long g439 = (g438 | g436);
        long g440 = (g439 | g433);
        long g441 = (x1_30 ^ g440);
        long g442 = (g441 ^ 1L);
        long g443 = (x0_30 ^ g442);
        long g444 = (g443 ^ 1L);
        long g445 = (g440 ^ 1L);
        long g446 = (x1_30 ^ 1L);
        long g447 = (g446 | g445);
        long g448 = (g447 ^ 1L);
        long g449 = (x0_30 ^ 1L);
        long g450 = (g449 | g445);
        long g451 = (g450 ^ 1L);
        long g452 = (g449 | g446);
        long g453 = (g452 ^ 1L);
        long g454 = (g453 | g451);
        long g455 = (g454 | g448);
        long g456 = (x1_31 ^ g455);
        long g457 = (g456 ^ 1L);
        long g458 = (x0_31 ^ g457);
        long g459 = (g458 ^ 1L);
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
        long w32 = cat(w31, g459, 1);
        long w33 = cat(w32, g444, 1);
        long w34 = cat(w33, g429, 1);
        long w35 = cat(w34, g414, 1);
        long w36 = cat(w35, g399, 1);
        long w37 = cat(w36, g384, 1);
        long w38 = cat(w37, g369, 1);
        long w39 = cat(w38, g354, 1);
        long w40 = cat(w39, g339, 1);
        long w41 = cat(w40, g324, 1);
        long w42 = cat(w41, g309, 1);
        long w43 = cat(w42, g294, 1);
        long w44 = cat(w43, g279, 1);
        long w45 = cat(w44, g264, 1);
        long w46 = cat(w45, g249, 1);
        long w47 = cat(w46, g234, 1);
        long w48 = cat(w47, g219, 1);
        long w49 = cat(w48, g204, 1);
        long w50 = cat(w49, g189, 1);
        long w51 = cat(w50, g174, 1);
        long w52 = cat(w51, g159, 1);
        long w53 = cat(w52, g144, 1);
        long w54 = cat(w53, g129, 1);
        long w55 = cat(w54, g114, 1);
        long w56 = cat(w55, g99, 1);
        long w57 = cat(w56, g84, 1);
        long w58 = cat(w57, g69, 1);
        long w59 = cat(w58, g54, 1);
        long w60 = cat(w59, g39, 1);
        long w61 = cat(w60, g24, 1);
        long w62 = cat(w61, g10, 1);
        long w63 = cat(w62, g2, 1);
        return m(w63, 64);
    }


    public static void main(String[] args) throws IOException {
        BufferedReader reader =
            new BufferedReader(new InputStreamReader(System.in));
        StringBuilder answers = new StringBuilder();
        String line = reader.readLine();
        while (line != null) {
            String text = line.trim();
            if (text.length() != 0) {
                String[] parts = text.split("\\s+");
                long[] values = new long[parts.length];
                for (int i = 0; i < parts.length; i++) {
                    values[i] = Long.parseUnsignedLong(parts[i]);
                }
                try {
                    answers.append(Long.toUnsignedString(emu_add_gpr_gpr_32__reg_rdi__java(values[0], values[1])));
                    answers.append("\n");
                } catch (Throwable problem) {
                    answers.append("RAISE:");
                    answers.append(problem.getClass().getSimpleName());
                    answers.append("\n");
                }
            }
            line = reader.readLine();
        }
        System.out.print(answers);
    }
}
