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
    // one named local per gate, over the term of mul_gpr_one_8__reg_rax__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 16, v0), Concat(0, Extract(7, 0, v0))*Concat(0, Extract(7, 0, v1)))
    static long emu_mul_gpr_one_8__reg_rax__java(long a, long b) {
        long x1_0 = ext(b, 0, 0);
        long x0_0 = ext(a, 0, 0);
        long x1_1 = ext(b, 1, 1);
        long x0_1 = ext(a, 1, 1);
        long x0_2 = ext(a, 2, 2);
        long x1_2 = ext(b, 2, 2);
        long x1_3 = ext(b, 3, 3);
        long x0_3 = ext(a, 3, 3);
        long x0_4 = ext(a, 4, 4);
        long x1_4 = ext(b, 4, 4);
        long x1_5 = ext(b, 5, 5);
        long x0_5 = ext(a, 5, 5);
        long x0_6 = ext(a, 6, 6);
        long x1_6 = ext(b, 6, 6);
        long x1_7 = ext(b, 7, 7);
        long x0_7 = ext(a, 7, 7);
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
        long x0_32 = ext(a, 32, 32);
        long x0_33 = ext(a, 33, 33);
        long x0_34 = ext(a, 34, 34);
        long x0_35 = ext(a, 35, 35);
        long x0_36 = ext(a, 36, 36);
        long x0_37 = ext(a, 37, 37);
        long x0_38 = ext(a, 38, 38);
        long x0_39 = ext(a, 39, 39);
        long x0_40 = ext(a, 40, 40);
        long x0_41 = ext(a, 41, 41);
        long x0_42 = ext(a, 42, 42);
        long x0_43 = ext(a, 43, 43);
        long x0_44 = ext(a, 44, 44);
        long x0_45 = ext(a, 45, 45);
        long x0_46 = ext(a, 46, 46);
        long x0_47 = ext(a, 47, 47);
        long x0_48 = ext(a, 48, 48);
        long x0_49 = ext(a, 49, 49);
        long x0_50 = ext(a, 50, 50);
        long x0_51 = ext(a, 51, 51);
        long x0_52 = ext(a, 52, 52);
        long x0_53 = ext(a, 53, 53);
        long x0_54 = ext(a, 54, 54);
        long x0_55 = ext(a, 55, 55);
        long x0_56 = ext(a, 56, 56);
        long x0_57 = ext(a, 57, 57);
        long x0_58 = ext(a, 58, 58);
        long x0_59 = ext(a, 59, 59);
        long x0_60 = ext(a, 60, 60);
        long x0_61 = ext(a, 61, 61);
        long x0_62 = ext(a, 62, 62);
        long x0_63 = ext(a, 63, 63);
        long g0 = (x0_0 & x1_0);
        long g1 = (x1_1 ^ 1L);
        long g2 = (x0_0 ^ 1L);
        long g3 = (g2 | g1);
        long g4 = (x1_0 ^ 1L);
        long g5 = (x0_1 ^ 1L);
        long g6 = (g5 | g4);
        long g7 = (g6 ^ g3);
        long g8 = (g7 ^ 1L);
        long g9 = (g8 ^ 1L);
        long g10 = (x0_2 ^ 1L);
        long g11 = (g10 | g4);
        long g12 = (x1_2 ^ 1L);
        long g13 = (g2 | g12);
        long g14 = (g5 | g1);
        long g15 = (g14 ^ g13);
        long g16 = (g15 ^ 1L);
        long g17 = (g3 | g6);
        long g18 = (g17 ^ g16);
        long g19 = (g18 ^ 1L);
        long g20 = (g19 ^ g11);
        long g21 = (g20 ^ 1L);
        long g22 = (g21 ^ 1L);
        long g23 = (g16 | g17);
        long g24 = (g23 ^ 1L);
        long g25 = (g11 | g17);
        long g26 = (g25 ^ 1L);
        long g27 = (g11 | g16);
        long g28 = (g27 ^ 1L);
        long g29 = (g28 | g26);
        long g30 = (g29 | g24);
        long g31 = (g10 | g1);
        long g32 = (x1_3 ^ 1L);
        long g33 = (g2 | g32);
        long g34 = (g5 | g12);
        long g35 = (g34 ^ g33);
        long g36 = (g35 ^ 1L);
        long g37 = (g13 | g14);
        long g38 = (g37 ^ g36);
        long g39 = (g38 ^ 1L);
        long g40 = (g39 ^ g31);
        long g41 = (g40 ^ 1L);
        long g42 = (g41 ^ g30);
        long g43 = (g42 ^ 1L);
        long g44 = (x0_3 ^ 1L);
        long g45 = (g44 | g4);
        long g46 = (g45 ^ g43);
        long g47 = (g46 ^ 1L);
        long g48 = (x0_4 ^ 1L);
        long g49 = (g48 | g4);
        long g50 = (g30 ^ 1L);
        long g51 = (g41 | g50);
        long g52 = (g51 ^ 1L);
        long g53 = (g45 | g50);
        long g54 = (g53 ^ 1L);
        long g55 = (g45 | g41);
        long g56 = (g55 ^ 1L);
        long g57 = (g56 | g54);
        long g58 = (g57 | g52);
        long g59 = (g36 | g37);
        long g60 = (g59 ^ 1L);
        long g61 = (g31 | g37);
        long g62 = (g61 ^ 1L);
        long g63 = (g31 | g36);
        long g64 = (g63 ^ 1L);
        long g65 = (g64 | g62);
        long g66 = (g65 | g60);
        long g67 = (g10 | g12);
        long g68 = (x1_4 ^ 1L);
        long g69 = (g2 | g68);
        long g70 = (g5 | g32);
        long g71 = (g70 ^ g69);
        long g72 = (g71 ^ 1L);
        long g73 = (g33 | g34);
        long g74 = (g73 ^ g72);
        long g75 = (g74 ^ 1L);
        long g76 = (g75 ^ g67);
        long g77 = (g76 ^ 1L);
        long g78 = (g77 ^ g66);
        long g79 = (g78 ^ 1L);
        long g80 = (g44 | g1);
        long g81 = (g80 ^ g79);
        long g82 = (g81 ^ 1L);
        long g83 = (g82 ^ g58);
        long g84 = (g83 ^ 1L);
        long g85 = (g84 ^ g49);
        long g86 = (g85 ^ 1L);
        long g87 = (g86 ^ 1L);
        long g88 = (g58 ^ 1L);
        long g89 = (g82 ^ 1L);
        long g90 = (g89 | g88);
        long g91 = (g90 ^ 1L);
        long g92 = (g49 | g89);
        long g93 = (g92 ^ 1L);
        long g94 = (g49 | g88);
        long g95 = (g94 ^ 1L);
        long g96 = (g95 | g93);
        long g97 = (g96 | g91);
        long g98 = (g48 | g1);
        long g99 = (g80 | g77);
        long g100 = (g99 ^ 1L);
        long g101 = (g66 ^ 1L);
        long g102 = (g80 | g101);
        long g103 = (g102 ^ 1L);
        long g104 = (g101 | g77);
        long g105 = (g104 ^ 1L);
        long g106 = (g105 | g103);
        long g107 = (g106 | g100);
        long g108 = (g72 | g73);
        long g109 = (g108 ^ 1L);
        long g110 = (g67 | g73);
        long g111 = (g110 ^ 1L);
        long g112 = (g67 | g72);
        long g113 = (g112 ^ 1L);
        long g114 = (g113 | g111);
        long g115 = (g114 | g109);
        long g116 = (g10 | g32);
        long g117 = (x1_5 ^ 1L);
        long g118 = (g2 | g117);
        long g119 = (g5 | g68);
        long g120 = (g119 ^ g118);
        long g121 = (g120 ^ 1L);
        long g122 = (g69 | g70);
        long g123 = (g122 ^ g121);
        long g124 = (g123 ^ 1L);
        long g125 = (g124 ^ g116);
        long g126 = (g125 ^ 1L);
        long g127 = (g126 ^ g115);
        long g128 = (g127 ^ 1L);
        long g129 = (g44 | g12);
        long g130 = (g129 ^ g128);
        long g131 = (g130 ^ 1L);
        long g132 = (g131 ^ g107);
        long g133 = (g132 ^ 1L);
        long g134 = (g133 ^ g98);
        long g135 = (g134 ^ 1L);
        long g136 = (g135 ^ g97);
        long g137 = (g136 ^ 1L);
        long g138 = (x0_5 ^ 1L);
        long g139 = (g138 | g4);
        long g140 = (g139 ^ g137);
        long g141 = (g140 ^ 1L);
        long g142 = (x0_6 ^ 1L);
        long g143 = (g142 | g4);
        long g144 = (g97 ^ 1L);
        long g145 = (g144 | g135);
        long g146 = (g145 ^ 1L);
        long g147 = (g144 | g139);
        long g148 = (g147 ^ 1L);
        long g149 = (g139 | g135);
        long g150 = (g149 ^ 1L);
        long g151 = (g150 | g148);
        long g152 = (g151 | g146);
        long g153 = (g131 ^ 1L);
        long g154 = (g153 | g98);
        long g155 = (g154 ^ 1L);
        long g156 = (g107 ^ 1L);
        long g157 = (g98 | g156);
        long g158 = (g157 ^ 1L);
        long g159 = (g153 | g156);
        long g160 = (g159 ^ 1L);
        long g161 = (g160 | g158);
        long g162 = (g161 | g155);
        long g163 = (g48 | g12);
        long g164 = (g115 ^ 1L);
        long g165 = (g164 | g126);
        long g166 = (g165 ^ 1L);
        long g167 = (g164 | g129);
        long g168 = (g167 ^ 1L);
        long g169 = (g129 | g126);
        long g170 = (g169 ^ 1L);
        long g171 = (g170 | g168);
        long g172 = (g171 | g166);
        long g173 = (g121 | g122);
        long g174 = (g173 ^ 1L);
        long g175 = (g116 | g122);
        long g176 = (g175 ^ 1L);
        long g177 = (g116 | g121);
        long g178 = (g177 ^ 1L);
        long g179 = (g178 | g176);
        long g180 = (g179 | g174);
        long g181 = (g10 | g68);
        long g182 = (x1_6 ^ 1L);
        long g183 = (g2 | g182);
        long g184 = (g5 | g117);
        long g185 = (g184 ^ g183);
        long g186 = (g185 ^ 1L);
        long g187 = (g118 | g119);
        long g188 = (g187 ^ g186);
        long g189 = (g188 ^ 1L);
        long g190 = (g189 ^ g181);
        long g191 = (g190 ^ 1L);
        long g192 = (g191 ^ g180);
        long g193 = (g192 ^ 1L);
        long g194 = (g44 | g32);
        long g195 = (g194 ^ g193);
        long g196 = (g195 ^ 1L);
        long g197 = (g196 ^ g172);
        long g198 = (g197 ^ 1L);
        long g199 = (g198 ^ g163);
        long g200 = (g199 ^ 1L);
        long g201 = (g200 ^ g162);
        long g202 = (g201 ^ 1L);
        long g203 = (g138 | g1);
        long g204 = (g203 ^ g202);
        long g205 = (g204 ^ 1L);
        long g206 = (g205 ^ g152);
        long g207 = (g206 ^ 1L);
        long g208 = (g207 ^ g143);
        long g209 = (g208 ^ 1L);
        long g210 = (g209 ^ 1L);
        long g211 = (g152 ^ 1L);
        long g212 = (g205 ^ 1L);
        long g213 = (g212 | g211);
        long g214 = (g213 ^ 1L);
        long g215 = (g211 | g143);
        long g216 = (g215 ^ 1L);
        long g217 = (g212 | g143);
        long g218 = (g217 ^ 1L);
        long g219 = (g218 | g216);
        long g220 = (g219 | g214);
        long g221 = (g142 | g1);
        long g222 = (g162 ^ 1L);
        long g223 = (g203 | g222);
        long g224 = (g223 ^ 1L);
        long g225 = (g222 | g200);
        long g226 = (g225 ^ 1L);
        long g227 = (g203 | g200);
        long g228 = (g227 ^ 1L);
        long g229 = (g228 | g226);
        long g230 = (g229 | g224);
        long g231 = (g172 ^ 1L);
        long g232 = (g196 ^ 1L);
        long g233 = (g232 | g231);
        long g234 = (g233 ^ 1L);
        long g235 = (g231 | g163);
        long g236 = (g235 ^ 1L);
        long g237 = (g232 | g163);
        long g238 = (g237 ^ 1L);
        long g239 = (g238 | g236);
        long g240 = (g239 | g234);
        long g241 = (g48 | g32);
        long g242 = (g180 ^ 1L);
        long g243 = (g191 | g242);
        long g244 = (g243 ^ 1L);
        long g245 = (g194 | g242);
        long g246 = (g245 ^ 1L);
        long g247 = (g194 | g191);
        long g248 = (g247 ^ 1L);
        long g249 = (g248 | g246);
        long g250 = (g249 | g244);
        long g251 = (g186 | g187);
        long g252 = (g251 ^ 1L);
        long g253 = (g181 | g187);
        long g254 = (g253 ^ 1L);
        long g255 = (g181 | g186);
        long g256 = (g255 ^ 1L);
        long g257 = (g256 | g254);
        long g258 = (g257 | g252);
        long g259 = (g10 | g117);
        long g260 = (x1_7 ^ 1L);
        long g261 = (g2 | g260);
        long g262 = (g5 | g182);
        long g263 = (g262 ^ g261);
        long g264 = (g263 ^ 1L);
        long g265 = (g183 | g184);
        long g266 = (g265 ^ g264);
        long g267 = (g266 ^ 1L);
        long g268 = (g267 ^ g259);
        long g269 = (g268 ^ 1L);
        long g270 = (g269 ^ g258);
        long g271 = (g270 ^ 1L);
        long g272 = (g44 | g68);
        long g273 = (g272 ^ g271);
        long g274 = (g273 ^ 1L);
        long g275 = (g274 ^ g250);
        long g276 = (g275 ^ 1L);
        long g277 = (g276 ^ g241);
        long g278 = (g277 ^ 1L);
        long g279 = (g278 ^ g240);
        long g280 = (g279 ^ 1L);
        long g281 = (g138 | g12);
        long g282 = (g281 ^ g280);
        long g283 = (g282 ^ 1L);
        long g284 = (g283 ^ g230);
        long g285 = (g284 ^ 1L);
        long g286 = (g285 ^ g221);
        long g287 = (g286 ^ 1L);
        long g288 = (g287 ^ g220);
        long g289 = (g288 ^ 1L);
        long g290 = (x0_7 ^ 1L);
        long g291 = (g290 | g4);
        long g292 = (g291 ^ g289);
        long g293 = (g292 ^ 1L);
        long g294 = (g220 ^ 1L);
        long g295 = (g294 | g287);
        long g296 = (g295 ^ 1L);
        long g297 = (g291 | g287);
        long g298 = (g297 ^ 1L);
        long g299 = (g291 | g294);
        long g300 = (g299 ^ 1L);
        long g301 = (g300 | g298);
        long g302 = (g301 | g296);
        long g303 = (g230 ^ 1L);
        long g304 = (g221 | g303);
        long g305 = (g304 ^ 1L);
        long g306 = (g283 ^ 1L);
        long g307 = (g221 | g306);
        long g308 = (g307 ^ 1L);
        long g309 = (g306 | g303);
        long g310 = (g309 ^ 1L);
        long g311 = (g310 | g308);
        long g312 = (g311 | g305);
        long g313 = (g142 | g12);
        long g314 = (g240 ^ 1L);
        long g315 = (g278 | g314);
        long g316 = (g315 ^ 1L);
        long g317 = (g281 | g314);
        long g318 = (g317 ^ 1L);
        long g319 = (g281 | g278);
        long g320 = (g319 ^ 1L);
        long g321 = (g320 | g318);
        long g322 = (g321 | g316);
        long g323 = (g274 ^ 1L);
        long g324 = (g241 | g323);
        long g325 = (g324 ^ 1L);
        long g326 = (g250 ^ 1L);
        long g327 = (g241 | g326);
        long g328 = (g327 ^ 1L);
        long g329 = (g323 | g326);
        long g330 = (g329 ^ 1L);
        long g331 = (g330 | g328);
        long g332 = (g331 | g325);
        long g333 = (g48 | g68);
        long g334 = (g258 ^ 1L);
        long g335 = (g269 | g334);
        long g336 = (g335 ^ 1L);
        long g337 = (g272 | g334);
        long g338 = (g337 ^ 1L);
        long g339 = (g272 | g269);
        long g340 = (g339 ^ 1L);
        long g341 = (g340 | g338);
        long g342 = (g341 | g336);
        long g343 = (g264 | g265);
        long g344 = (g343 ^ 1L);
        long g345 = (g259 | g265);
        long g346 = (g345 ^ 1L);
        long g347 = (g259 | g264);
        long g348 = (g347 ^ 1L);
        long g349 = (g348 | g346);
        long g350 = (g349 | g344);
        long g351 = (g10 | g182);
        long g352 = (g5 | g260);
        long g353 = (g261 | g262);
        long g354 = (g353 ^ g352);
        long g355 = (g354 ^ 1L);
        long g356 = (g355 ^ g351);
        long g357 = (g356 ^ 1L);
        long g358 = (g357 ^ g350);
        long g359 = (g358 ^ 1L);
        long g360 = (g44 | g117);
        long g361 = (g360 ^ g359);
        long g362 = (g361 ^ 1L);
        long g363 = (g362 ^ g342);
        long g364 = (g363 ^ 1L);
        long g365 = (g364 ^ g333);
        long g366 = (g365 ^ 1L);
        long g367 = (g366 ^ g332);
        long g368 = (g367 ^ 1L);
        long g369 = (g138 | g32);
        long g370 = (g369 ^ g368);
        long g371 = (g370 ^ 1L);
        long g372 = (g371 ^ g322);
        long g373 = (g372 ^ 1L);
        long g374 = (g373 ^ g313);
        long g375 = (g374 ^ 1L);
        long g376 = (g375 ^ g312);
        long g377 = (g376 ^ 1L);
        long g378 = (g290 | g1);
        long g379 = (g378 ^ g377);
        long g380 = (g379 ^ 1L);
        long g381 = (g380 ^ g302);
        long g382 = (g381 ^ 1L);
        long g383 = (g382 ^ 1L);
        long g384 = (g312 ^ 1L);
        long g385 = (g375 | g384);
        long g386 = (g385 ^ 1L);
        long g387 = (g378 | g384);
        long g388 = (g387 ^ 1L);
        long g389 = (g378 | g375);
        long g390 = (g389 ^ 1L);
        long g391 = (g390 | g388);
        long g392 = (g391 | g386);
        long g393 = (g371 ^ 1L);
        long g394 = (g313 | g393);
        long g395 = (g394 ^ 1L);
        long g396 = (g322 ^ 1L);
        long g397 = (g393 | g396);
        long g398 = (g397 ^ 1L);
        long g399 = (g313 | g396);
        long g400 = (g399 ^ 1L);
        long g401 = (g400 | g398);
        long g402 = (g401 | g395);
        long g403 = (g142 | g32);
        long g404 = (g332 ^ 1L);
        long g405 = (g404 | g366);
        long g406 = (g405 ^ 1L);
        long g407 = (g404 | g369);
        long g408 = (g407 ^ 1L);
        long g409 = (g369 | g366);
        long g410 = (g409 ^ 1L);
        long g411 = (g410 | g408);
        long g412 = (g411 | g406);
        long g413 = (g342 ^ 1L);
        long g414 = (g333 | g413);
        long g415 = (g414 ^ 1L);
        long g416 = (g362 ^ 1L);
        long g417 = (g333 | g416);
        long g418 = (g417 ^ 1L);
        long g419 = (g416 | g413);
        long g420 = (g419 ^ 1L);
        long g421 = (g420 | g418);
        long g422 = (g421 | g415);
        long g423 = (g48 | g117);
        long g424 = (g350 ^ 1L);
        long g425 = (g357 | g424);
        long g426 = (g425 ^ 1L);
        long g427 = (g360 | g424);
        long g428 = (g427 ^ 1L);
        long g429 = (g360 | g357);
        long g430 = (g429 ^ 1L);
        long g431 = (g430 | g428);
        long g432 = (g431 | g426);
        long g433 = (g351 | g352);
        long g434 = (g433 ^ 1L);
        long g435 = (g351 | g353);
        long g436 = (g435 ^ 1L);
        long g437 = (g352 | g353);
        long g438 = (g437 ^ 1L);
        long g439 = (g438 | g436);
        long g440 = (g439 | g434);
        long g441 = (g10 | g260);
        long g442 = (g441 ^ g440);
        long g443 = (g442 ^ 1L);
        long g444 = (g44 | g182);
        long g445 = (g444 ^ g443);
        long g446 = (g445 ^ 1L);
        long g447 = (g446 ^ g432);
        long g448 = (g447 ^ 1L);
        long g449 = (g448 ^ g423);
        long g450 = (g449 ^ 1L);
        long g451 = (g450 ^ g422);
        long g452 = (g451 ^ 1L);
        long g453 = (g138 | g68);
        long g454 = (g453 ^ g452);
        long g455 = (g454 ^ 1L);
        long g456 = (g455 ^ g412);
        long g457 = (g456 ^ 1L);
        long g458 = (g457 ^ g403);
        long g459 = (g458 ^ 1L);
        long g460 = (g459 ^ g402);
        long g461 = (g460 ^ 1L);
        long g462 = (g290 | g12);
        long g463 = (g462 ^ g461);
        long g464 = (g463 ^ 1L);
        long g465 = (g464 ^ g392);
        long g466 = (g465 ^ 1L);
        long g467 = (g302 ^ 1L);
        long g468 = (g380 ^ 1L);
        long g469 = (g468 | g467);
        long g470 = (g469 ^ g466);
        long g471 = (g470 ^ 1L);
        long g472 = (g471 ^ 1L);
        long g473 = (g466 | g469);
        long g474 = (g392 ^ 1L);
        long g475 = (g464 ^ 1L);
        long g476 = (g475 | g474);
        long g477 = (g462 | g459);
        long g478 = (g477 ^ 1L);
        long g479 = (g402 ^ 1L);
        long g480 = (g462 | g479);
        long g481 = (g480 ^ 1L);
        long g482 = (g479 | g459);
        long g483 = (g482 ^ 1L);
        long g484 = (g483 | g481);
        long g485 = (g484 | g478);
        long g486 = (g290 | g32);
        long g487 = (g412 ^ 1L);
        long g488 = (g455 ^ 1L);
        long g489 = (g488 | g487);
        long g490 = (g489 ^ 1L);
        long g491 = (g403 | g488);
        long g492 = (g491 ^ 1L);
        long g493 = (g487 | g403);
        long g494 = (g493 ^ 1L);
        long g495 = (g494 | g492);
        long g496 = (g495 | g490);
        long g497 = (g422 ^ 1L);
        long g498 = (g453 | g497);
        long g499 = (g498 ^ 1L);
        long g500 = (g453 | g450);
        long g501 = (g500 ^ 1L);
        long g502 = (g497 | g450);
        long g503 = (g502 ^ 1L);
        long g504 = (g503 | g501);
        long g505 = (g504 | g499);
        long g506 = (g138 | g117);
        long g507 = (g446 ^ 1L);
        long g508 = (g423 | g507);
        long g509 = (g508 ^ 1L);
        long g510 = (g432 ^ 1L);
        long g511 = (g507 | g510);
        long g512 = (g511 ^ 1L);
        long g513 = (g423 | g510);
        long g514 = (g513 ^ 1L);
        long g515 = (g514 | g512);
        long g516 = (g515 | g509);
        long g517 = (g440 ^ 1L);
        long g518 = (g444 | g517);
        long g519 = (g518 ^ 1L);
        long g520 = (g441 | g444);
        long g521 = (g520 ^ 1L);
        long g522 = (g441 | g517);
        long g523 = (g522 ^ 1L);
        long g524 = (g523 | g521);
        long g525 = (g524 | g519);
        long g526 = (g44 | g260);
        long g527 = (g526 ^ g525);
        long g528 = (g527 ^ 1L);
        long g529 = (g48 | g182);
        long g530 = (g529 ^ g528);
        long g531 = (g530 ^ 1L);
        long g532 = (g531 ^ g516);
        long g533 = (g532 ^ 1L);
        long g534 = (g533 ^ g506);
        long g535 = (g534 ^ 1L);
        long g536 = (g535 ^ g505);
        long g537 = (g536 ^ 1L);
        long g538 = (g142 | g68);
        long g539 = (g538 ^ g537);
        long g540 = (g539 ^ 1L);
        long g541 = (g540 ^ g496);
        long g542 = (g541 ^ 1L);
        long g543 = (g542 ^ g486);
        long g544 = (g543 ^ 1L);
        long g545 = (g544 ^ g485);
        long g546 = (g545 ^ 1L);
        long g547 = (g546 ^ g476);
        long g548 = (g547 ^ 1L);
        long g549 = (g548 ^ g473);
        long g550 = (g549 ^ 1L);
        long g551 = (g496 ^ 1L);
        long g552 = (g540 ^ 1L);
        long g553 = (g552 | g551);
        long g554 = (g553 ^ 1L);
        long g555 = (g552 | g486);
        long g556 = (g555 ^ 1L);
        long g557 = (g551 | g486);
        long g558 = (g557 ^ 1L);
        long g559 = (g558 | g556);
        long g560 = (g559 | g554);
        long g561 = (g505 ^ 1L);
        long g562 = (g535 | g561);
        long g563 = (g562 ^ 1L);
        long g564 = (g561 | g538);
        long g565 = (g564 ^ 1L);
        long g566 = (g538 | g535);
        long g567 = (g566 ^ 1L);
        long g568 = (g567 | g565);
        long g569 = (g568 | g563);
        long g570 = (g142 | g117);
        long g571 = (g516 ^ 1L);
        long g572 = (g531 ^ 1L);
        long g573 = (g572 | g571);
        long g574 = (g573 ^ 1L);
        long g575 = (g506 | g572);
        long g576 = (g575 ^ 1L);
        long g577 = (g506 | g571);
        long g578 = (g577 ^ 1L);
        long g579 = (g578 | g576);
        long g580 = (g579 | g574);
        long g581 = (g525 ^ 1L);
        long g582 = (g581 | g526);
        long g583 = (g582 ^ 1L);
        long g584 = (g529 | g526);
        long g585 = (g584 ^ 1L);
        long g586 = (g581 | g529);
        long g587 = (g586 ^ 1L);
        long g588 = (g587 | g585);
        long g589 = (g588 | g583);
        long g590 = (g48 | g260);
        long g591 = (g590 ^ g589);
        long g592 = (g591 ^ 1L);
        long g593 = (g138 | g182);
        long g594 = (g593 ^ g592);
        long g595 = (g594 ^ 1L);
        long g596 = (g595 ^ g580);
        long g597 = (g596 ^ 1L);
        long g598 = (g597 ^ g570);
        long g599 = (g598 ^ 1L);
        long g600 = (g599 ^ g569);
        long g601 = (g600 ^ 1L);
        long g602 = (g290 | g68);
        long g603 = (g602 ^ g601);
        long g604 = (g603 ^ 1L);
        long g605 = (g604 ^ g560);
        long g606 = (g605 ^ 1L);
        long g607 = (g485 ^ 1L);
        long g608 = (g544 | g607);
        long g609 = (g608 ^ g606);
        long g610 = (g609 ^ 1L);
        long g611 = (g546 ^ 1L);
        long g612 = (g611 | g476);
        long g613 = (g612 ^ g610);
        long g614 = (g613 ^ 1L);
        long g615 = (g548 ^ 1L);
        long g616 = (g615 | g473);
        long g617 = (g616 ^ g614);
        long g618 = (g617 ^ 1L);
        long g619 = (g618 ^ 1L);
        long g620 = (g614 | g616);
        long g621 = (g610 | g612);
        long g622 = (g606 | g608);
        long g623 = (g560 ^ 1L);
        long g624 = (g604 ^ 1L);
        long g625 = (g624 | g623);
        long g626 = (g569 ^ 1L);
        long g627 = (g626 | g599);
        long g628 = (g627 ^ 1L);
        long g629 = (g626 | g602);
        long g630 = (g629 ^ 1L);
        long g631 = (g602 | g599);
        long g632 = (g631 ^ 1L);
        long g633 = (g632 | g630);
        long g634 = (g633 | g628);
        long g635 = (g290 | g117);
        long g636 = (g580 ^ 1L);
        long g637 = (g570 | g636);
        long g638 = (g637 ^ 1L);
        long g639 = (g595 ^ 1L);
        long g640 = (g639 | g636);
        long g641 = (g640 ^ 1L);
        long g642 = (g570 | g639);
        long g643 = (g642 ^ 1L);
        long g644 = (g643 | g641);
        long g645 = (g644 | g638);
        long g646 = (g589 ^ 1L);
        long g647 = (g646 | g593);
        long g648 = (g647 ^ 1L);
        long g649 = (g590 | g593);
        long g650 = (g649 ^ 1L);
        long g651 = (g646 | g590);
        long g652 = (g651 ^ 1L);
        long g653 = (g652 | g650);
        long g654 = (g653 | g648);
        long g655 = (g138 | g260);
        long g656 = (g655 ^ g654);
        long g657 = (g656 ^ 1L);
        long g658 = (g142 | g182);
        long g659 = (g658 ^ g657);
        long g660 = (g659 ^ 1L);
        long g661 = (g660 ^ g645);
        long g662 = (g661 ^ 1L);
        long g663 = (g662 ^ g635);
        long g664 = (g663 ^ 1L);
        long g665 = (g664 ^ g634);
        long g666 = (g665 ^ 1L);
        long g667 = (g666 ^ g625);
        long g668 = (g667 ^ 1L);
        long g669 = (g668 ^ g622);
        long g670 = (g669 ^ 1L);
        long g671 = (g670 ^ g621);
        long g672 = (g671 ^ 1L);
        long g673 = (g672 ^ g620);
        long g674 = (g673 ^ 1L);
        long g675 = (g660 ^ 1L);
        long g676 = (g635 | g675);
        long g677 = (g676 ^ 1L);
        long g678 = (g645 ^ 1L);
        long g679 = (g635 | g678);
        long g680 = (g679 ^ 1L);
        long g681 = (g675 | g678);
        long g682 = (g681 ^ 1L);
        long g683 = (g682 | g680);
        long g684 = (g683 | g677);
        long g685 = (g655 | g658);
        long g686 = (g685 ^ 1L);
        long g687 = (g654 ^ 1L);
        long g688 = (g658 | g687);
        long g689 = (g688 ^ 1L);
        long g690 = (g655 | g687);
        long g691 = (g690 ^ 1L);
        long g692 = (g691 | g689);
        long g693 = (g692 | g686);
        long g694 = (g142 | g260);
        long g695 = (g694 ^ g693);
        long g696 = (g695 ^ 1L);
        long g697 = (g290 | g182);
        long g698 = (g697 ^ g696);
        long g699 = (g698 ^ 1L);
        long g700 = (g699 ^ g684);
        long g701 = (g700 ^ 1L);
        long g702 = (g634 ^ 1L);
        long g703 = (g664 | g702);
        long g704 = (g703 ^ g701);
        long g705 = (g704 ^ 1L);
        long g706 = (g666 ^ 1L);
        long g707 = (g706 | g625);
        long g708 = (g707 ^ g705);
        long g709 = (g708 ^ 1L);
        long g710 = (g668 ^ 1L);
        long g711 = (g710 | g622);
        long g712 = (g711 ^ g709);
        long g713 = (g712 ^ 1L);
        long g714 = (g670 ^ 1L);
        long g715 = (g714 | g621);
        long g716 = (g715 ^ g713);
        long g717 = (g716 ^ 1L);
        long g718 = (g672 ^ 1L);
        long g719 = (g718 | g620);
        long g720 = (g719 ^ g717);
        long g721 = (g720 ^ 1L);
        long g722 = (g721 ^ 1L);
        long g723 = (g717 | g719);
        long g724 = (g713 | g715);
        long g725 = (g709 | g711);
        long g726 = (g705 | g707);
        long g727 = (g701 | g703);
        long g728 = (g684 ^ 1L);
        long g729 = (g699 ^ 1L);
        long g730 = (g729 | g728);
        long g731 = (g693 ^ 1L);
        long g732 = (g694 | g731);
        long g733 = (g732 ^ 1L);
        long g734 = (g731 | g697);
        long g735 = (g734 ^ 1L);
        long g736 = (g694 | g697);
        long g737 = (g736 ^ 1L);
        long g738 = (g737 | g735);
        long g739 = (g738 | g733);
        long g740 = (g290 | g260);
        long g741 = (g740 ^ g739);
        long g742 = (g741 ^ 1L);
        long g743 = (g742 ^ g730);
        long g744 = (g743 ^ 1L);
        long g745 = (g744 ^ g727);
        long g746 = (g745 ^ 1L);
        long g747 = (g746 ^ g726);
        long g748 = (g747 ^ 1L);
        long g749 = (g748 ^ g725);
        long g750 = (g749 ^ 1L);
        long g751 = (g750 ^ g724);
        long g752 = (g751 ^ 1L);
        long g753 = (g752 ^ g723);
        long g754 = (g753 ^ 1L);
        long g755 = (g739 ^ 1L);
        long g756 = (g740 | g755);
        long g757 = (g742 ^ 1L);
        long g758 = (g757 | g730);
        long g759 = (g758 ^ g756);
        long g760 = (g759 ^ 1L);
        long g761 = (g744 ^ 1L);
        long g762 = (g761 | g727);
        long g763 = (g762 ^ g760);
        long g764 = (g763 ^ 1L);
        long g765 = (g746 ^ 1L);
        long g766 = (g765 | g726);
        long g767 = (g766 ^ g764);
        long g768 = (g767 ^ 1L);
        long g769 = (g748 ^ 1L);
        long g770 = (g769 | g725);
        long g771 = (g770 ^ g768);
        long g772 = (g771 ^ 1L);
        long g773 = (g750 ^ 1L);
        long g774 = (g773 | g724);
        long g775 = (g774 ^ g772);
        long g776 = (g775 ^ 1L);
        long g777 = (g752 ^ 1L);
        long g778 = (g777 | g723);
        long g779 = (g778 ^ g776);
        long g780 = (g779 ^ 1L);
        long g781 = (g780 ^ 1L);
        long w0 = x0_63;
        long w1 = cat(w0, x0_62, 1);
        long w2 = cat(w1, x0_61, 1);
        long w3 = cat(w2, x0_60, 1);
        long w4 = cat(w3, x0_59, 1);
        long w5 = cat(w4, x0_58, 1);
        long w6 = cat(w5, x0_57, 1);
        long w7 = cat(w6, x0_56, 1);
        long w8 = cat(w7, x0_55, 1);
        long w9 = cat(w8, x0_54, 1);
        long w10 = cat(w9, x0_53, 1);
        long w11 = cat(w10, x0_52, 1);
        long w12 = cat(w11, x0_51, 1);
        long w13 = cat(w12, x0_50, 1);
        long w14 = cat(w13, x0_49, 1);
        long w15 = cat(w14, x0_48, 1);
        long w16 = cat(w15, x0_47, 1);
        long w17 = cat(w16, x0_46, 1);
        long w18 = cat(w17, x0_45, 1);
        long w19 = cat(w18, x0_44, 1);
        long w20 = cat(w19, x0_43, 1);
        long w21 = cat(w20, x0_42, 1);
        long w22 = cat(w21, x0_41, 1);
        long w23 = cat(w22, x0_40, 1);
        long w24 = cat(w23, x0_39, 1);
        long w25 = cat(w24, x0_38, 1);
        long w26 = cat(w25, x0_37, 1);
        long w27 = cat(w26, x0_36, 1);
        long w28 = cat(w27, x0_35, 1);
        long w29 = cat(w28, x0_34, 1);
        long w30 = cat(w29, x0_33, 1);
        long w31 = cat(w30, x0_32, 1);
        long w32 = cat(w31, x0_31, 1);
        long w33 = cat(w32, x0_30, 1);
        long w34 = cat(w33, x0_29, 1);
        long w35 = cat(w34, x0_28, 1);
        long w36 = cat(w35, x0_27, 1);
        long w37 = cat(w36, x0_26, 1);
        long w38 = cat(w37, x0_25, 1);
        long w39 = cat(w38, x0_24, 1);
        long w40 = cat(w39, x0_23, 1);
        long w41 = cat(w40, x0_22, 1);
        long w42 = cat(w41, x0_21, 1);
        long w43 = cat(w42, x0_20, 1);
        long w44 = cat(w43, x0_19, 1);
        long w45 = cat(w44, x0_18, 1);
        long w46 = cat(w45, x0_17, 1);
        long w47 = cat(w46, x0_16, 1);
        long w48 = cat(w47, g781, 1);
        long w49 = cat(w48, g754, 1);
        long w50 = cat(w49, g722, 1);
        long w51 = cat(w50, g674, 1);
        long w52 = cat(w51, g619, 1);
        long w53 = cat(w52, g550, 1);
        long w54 = cat(w53, g472, 1);
        long w55 = cat(w54, g383, 1);
        long w56 = cat(w55, g293, 1);
        long w57 = cat(w56, g210, 1);
        long w58 = cat(w57, g141, 1);
        long w59 = cat(w58, g87, 1);
        long w60 = cat(w59, g47, 1);
        long w61 = cat(w60, g22, 1);
        long w62 = cat(w61, g9, 1);
        long w63 = cat(w62, g0, 1);
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
                    answers.append(Long.toUnsignedString(emu_mul_gpr_one_8__reg_rax__java(values[0], values[1])));
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
