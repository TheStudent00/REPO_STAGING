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
    // one named local per gate, over the term of sar_cl_gpr_16__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 16, v0), Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1)))
    static long emu_sar_cl_gpr_16__reg_rdi__java(long a, long b) {
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
        long x1_4 = ext(b, 4, 4);
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
        long g60 = (x1_4 ^ 1L);
        long g61 = (x1_4 & x0_15);
        long g62 = (g60 & g59);
        long g63 = (g61 | g62);
        long g64 = (x1_0 ^ 1L);
        long g65 = (x1_0 & x0_2);
        long g66 = (g64 & x0_1);
        long g67 = (g65 | g66);
        long g68 = (x1_0 ^ 1L);
        long g69 = (x1_0 & x0_4);
        long g70 = (g68 & x0_3);
        long g71 = (g69 | g70);
        long g72 = (x1_1 ^ 1L);
        long g73 = (x1_1 & g71);
        long g74 = (g72 & g67);
        long g75 = (g73 | g74);
        long g76 = (x1_0 ^ 1L);
        long g77 = (x1_0 & x0_6);
        long g78 = (g76 & x0_5);
        long g79 = (g77 | g78);
        long g80 = (x1_0 ^ 1L);
        long g81 = (x1_0 & x0_8);
        long g82 = (g80 & x0_7);
        long g83 = (g81 | g82);
        long g84 = (x1_1 ^ 1L);
        long g85 = (x1_1 & g83);
        long g86 = (g84 & g79);
        long g87 = (g85 | g86);
        long g88 = (x1_2 ^ 1L);
        long g89 = (x1_2 & g87);
        long g90 = (g88 & g75);
        long g91 = (g89 | g90);
        long g92 = (x1_0 ^ 1L);
        long g93 = (x1_0 & x0_10);
        long g94 = (g92 & x0_9);
        long g95 = (g93 | g94);
        long g96 = (x1_0 ^ 1L);
        long g97 = (x1_0 & x0_12);
        long g98 = (g96 & x0_11);
        long g99 = (g97 | g98);
        long g100 = (x1_1 ^ 1L);
        long g101 = (x1_1 & g99);
        long g102 = (g100 & g95);
        long g103 = (g101 | g102);
        long g104 = (x1_0 ^ 1L);
        long g105 = (x1_0 & x0_14);
        long g106 = (g104 & x0_13);
        long g107 = (g105 | g106);
        long g108 = (x1_1 ^ 1L);
        long g109 = (x1_1 & x0_15);
        long g110 = (g108 & g107);
        long g111 = (g109 | g110);
        long g112 = (x1_2 ^ 1L);
        long g113 = (x1_2 & g111);
        long g114 = (g112 & g103);
        long g115 = (g113 | g114);
        long g116 = (x1_3 ^ 1L);
        long g117 = (x1_3 & g115);
        long g118 = (g116 & g91);
        long g119 = (g117 | g118);
        long g120 = (x1_4 ^ 1L);
        long g121 = (x1_4 & x0_15);
        long g122 = (g120 & g119);
        long g123 = (g121 | g122);
        long g124 = (x1_1 ^ 1L);
        long g125 = (x1_1 & g15);
        long g126 = (g124 & g7);
        long g127 = (g125 | g126);
        long g128 = (x1_1 ^ 1L);
        long g129 = (x1_1 & g31);
        long g130 = (g128 & g19);
        long g131 = (g129 | g130);
        long g132 = (x1_2 ^ 1L);
        long g133 = (x1_2 & g131);
        long g134 = (g132 & g127);
        long g135 = (g133 | g134);
        long g136 = (x1_1 ^ 1L);
        long g137 = (x1_1 & g43);
        long g138 = (g136 & g35);
        long g139 = (g137 | g138);
        long g140 = (x1_1 | x1_0);
        long g141 = (g140 ^ 1L);
        long g142 = (g140 & x0_15);
        long g143 = (g141 & x0_14);
        long g144 = (g142 | g143);
        long g145 = (x1_2 ^ 1L);
        long g146 = (x1_2 & g144);
        long g147 = (g145 & g139);
        long g148 = (g146 | g147);
        long g149 = (x1_3 ^ 1L);
        long g150 = (x1_3 & g148);
        long g151 = (g149 & g135);
        long g152 = (g150 | g151);
        long g153 = (x1_4 ^ 1L);
        long g154 = (x1_4 & x0_15);
        long g155 = (g153 & g152);
        long g156 = (g154 | g155);
        long g157 = (x1_1 ^ 1L);
        long g158 = (x1_1 & g79);
        long g159 = (g157 & g71);
        long g160 = (g158 | g159);
        long g161 = (x1_1 ^ 1L);
        long g162 = (x1_1 & g95);
        long g163 = (g161 & g83);
        long g164 = (g162 | g163);
        long g165 = (x1_2 ^ 1L);
        long g166 = (x1_2 & g164);
        long g167 = (g165 & g160);
        long g168 = (g166 | g167);
        long g169 = (x1_1 ^ 1L);
        long g170 = (x1_1 & g107);
        long g171 = (g169 & g99);
        long g172 = (g170 | g171);
        long g173 = (x1_2 ^ 1L);
        long g174 = (x1_2 & x0_15);
        long g175 = (g173 & g172);
        long g176 = (g174 | g175);
        long g177 = (x1_3 ^ 1L);
        long g178 = (x1_3 & g176);
        long g179 = (g177 & g168);
        long g180 = (g178 | g179);
        long g181 = (x1_4 ^ 1L);
        long g182 = (x1_4 & x0_15);
        long g183 = (g181 & g180);
        long g184 = (g182 | g183);
        long g185 = (x1_2 ^ 1L);
        long g186 = (x1_2 & g39);
        long g187 = (g185 & g23);
        long g188 = (g186 | g187);
        long g189 = (x1_2 ^ 1L);
        long g190 = (x1_2 & x0_15);
        long g191 = (g189 & g51);
        long g192 = (g190 | g191);
        long g193 = (x1_3 ^ 1L);
        long g194 = (x1_3 & g192);
        long g195 = (g193 & g188);
        long g196 = (g194 | g195);
        long g197 = (x1_4 ^ 1L);
        long g198 = (x1_4 & x0_15);
        long g199 = (g197 & g196);
        long g200 = (g198 | g199);
        long g201 = (x1_2 ^ 1L);
        long g202 = (x1_2 & g103);
        long g203 = (g201 & g87);
        long g204 = (g202 | g203);
        long g205 = (x1_2 | x1_1);
        long g206 = (g205 ^ 1L);
        long g207 = (g205 & x0_15);
        long g208 = (g206 & g107);
        long g209 = (g207 | g208);
        long g210 = (x1_3 ^ 1L);
        long g211 = (x1_3 & g209);
        long g212 = (g210 & g204);
        long g213 = (g211 | g212);
        long g214 = (x1_4 ^ 1L);
        long g215 = (x1_4 & x0_15);
        long g216 = (g214 & g213);
        long g217 = (g215 | g216);
        long g218 = (x1_2 ^ 1L);
        long g219 = (x1_2 & g139);
        long g220 = (g218 & g131);
        long g221 = (g219 | g220);
        long g222 = (x1_2 | g140);
        long g223 = (g222 ^ 1L);
        long g224 = (g222 & x0_15);
        long g225 = (g223 & x0_14);
        long g226 = (g224 | g225);
        long g227 = (x1_3 ^ 1L);
        long g228 = (x1_3 & g226);
        long g229 = (g227 & g221);
        long g230 = (g228 | g229);
        long g231 = (x1_4 ^ 1L);
        long g232 = (x1_4 & x0_15);
        long g233 = (g231 & g230);
        long g234 = (g232 | g233);
        long g235 = (x1_2 ^ 1L);
        long g236 = (x1_2 & g172);
        long g237 = (g235 & g164);
        long g238 = (g236 | g237);
        long g239 = (x1_4 | x1_3);
        long g240 = (g239 ^ 1L);
        long g241 = (g239 & x0_15);
        long g242 = (g240 & g238);
        long g243 = (g241 | g242);
        long g244 = (g239 ^ 1L);
        long g245 = (g239 & x0_15);
        long g246 = (g244 & g55);
        long g247 = (g245 | g246);
        long g248 = (g239 ^ 1L);
        long g249 = (g239 & x0_15);
        long g250 = (g248 & g115);
        long g251 = (g249 | g250);
        long g252 = (g239 ^ 1L);
        long g253 = (g239 & x0_15);
        long g254 = (g252 & g148);
        long g255 = (g253 | g254);
        long g256 = (x1_3 | x1_2);
        long g257 = (x1_4 | g256);
        long g258 = (g257 ^ 1L);
        long g259 = (g257 & x0_15);
        long g260 = (g258 & g172);
        long g261 = (g259 | g260);
        long g262 = (g257 ^ 1L);
        long g263 = (g257 & x0_15);
        long g264 = (g262 & g51);
        long g265 = (g263 | g264);
        long g266 = (x1_3 | g205);
        long g267 = (x1_4 | g266);
        long g268 = (g267 ^ 1L);
        long g269 = (g267 & x0_15);
        long g270 = (g268 & g107);
        long g271 = (g269 | g270);
        long g272 = (x1_3 | g222);
        long g273 = (x1_4 | g272);
        long g274 = (g273 ^ 1L);
        long g275 = (g273 & x0_15);
        long g276 = (g274 & x0_14);
        long g277 = (g275 | g276);
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
        long w48 = cat(w47, x0_15, 1);
        long w49 = cat(w48, g277, 1);
        long w50 = cat(w49, g271, 1);
        long w51 = cat(w50, g265, 1);
        long w52 = cat(w51, g261, 1);
        long w53 = cat(w52, g255, 1);
        long w54 = cat(w53, g251, 1);
        long w55 = cat(w54, g247, 1);
        long w56 = cat(w55, g243, 1);
        long w57 = cat(w56, g234, 1);
        long w58 = cat(w57, g217, 1);
        long w59 = cat(w58, g200, 1);
        long w60 = cat(w59, g184, 1);
        long w61 = cat(w60, g156, 1);
        long w62 = cat(w61, g123, 1);
        long w63 = cat(w62, g63, 1);
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
                    answers.append(Long.toUnsignedString(emu_sar_cl_gpr_16__reg_rdi__java(values[0], values[1])));
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
