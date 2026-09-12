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
    // one named local per gate, over the term of cmovbe_gpr_gpr_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(Or(Extract(31, 0, v1)*4294967295 == Extract(31, 0, v0), Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1), Extract(31, 0, v2), Extract(31, 0, v3)))
    static long emu_cmovbe_gpr_gpr_32__reg_rdi__java(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
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
        long x2_0 = ext(c, 0, 0);
        long x3_1 = ext(d, 1, 1);
        long x2_1 = ext(c, 1, 1);
        long x3_2 = ext(d, 2, 2);
        long x2_2 = ext(c, 2, 2);
        long x3_3 = ext(d, 3, 3);
        long x2_3 = ext(c, 3, 3);
        long x3_4 = ext(d, 4, 4);
        long x2_4 = ext(c, 4, 4);
        long x3_5 = ext(d, 5, 5);
        long x2_5 = ext(c, 5, 5);
        long x3_6 = ext(d, 6, 6);
        long x2_6 = ext(c, 6, 6);
        long x3_7 = ext(d, 7, 7);
        long x2_7 = ext(c, 7, 7);
        long x3_8 = ext(d, 8, 8);
        long x2_8 = ext(c, 8, 8);
        long x3_9 = ext(d, 9, 9);
        long x2_9 = ext(c, 9, 9);
        long x3_10 = ext(d, 10, 10);
        long x2_10 = ext(c, 10, 10);
        long x3_11 = ext(d, 11, 11);
        long x2_11 = ext(c, 11, 11);
        long x3_12 = ext(d, 12, 12);
        long x2_12 = ext(c, 12, 12);
        long x3_13 = ext(d, 13, 13);
        long x2_13 = ext(c, 13, 13);
        long x3_14 = ext(d, 14, 14);
        long x2_14 = ext(c, 14, 14);
        long x3_15 = ext(d, 15, 15);
        long x2_15 = ext(c, 15, 15);
        long x3_16 = ext(d, 16, 16);
        long x2_16 = ext(c, 16, 16);
        long x3_17 = ext(d, 17, 17);
        long x2_17 = ext(c, 17, 17);
        long x3_18 = ext(d, 18, 18);
        long x2_18 = ext(c, 18, 18);
        long x3_19 = ext(d, 19, 19);
        long x2_19 = ext(c, 19, 19);
        long x3_20 = ext(d, 20, 20);
        long x2_20 = ext(c, 20, 20);
        long x3_21 = ext(d, 21, 21);
        long x2_21 = ext(c, 21, 21);
        long x3_22 = ext(d, 22, 22);
        long x2_22 = ext(c, 22, 22);
        long x3_23 = ext(d, 23, 23);
        long x2_23 = ext(c, 23, 23);
        long x3_24 = ext(d, 24, 24);
        long x2_24 = ext(c, 24, 24);
        long x3_25 = ext(d, 25, 25);
        long x2_25 = ext(c, 25, 25);
        long x3_26 = ext(d, 26, 26);
        long x2_26 = ext(c, 26, 26);
        long x3_27 = ext(d, 27, 27);
        long x2_27 = ext(c, 27, 27);
        long x3_28 = ext(d, 28, 28);
        long x2_28 = ext(c, 28, 28);
        long x3_29 = ext(d, 29, 29);
        long x2_29 = ext(c, 29, 29);
        long x3_30 = ext(d, 30, 30);
        long x2_30 = ext(c, 30, 30);
        long x3_31 = ext(d, 31, 31);
        long x2_31 = ext(c, 31, 31);
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
        long g343 = (x1_1 | x1_0);
        long g344 = (x1_2 | g343);
        long g345 = (x1_3 | g344);
        long g346 = (x1_4 | g345);
        long g347 = (x1_5 | g346);
        long g348 = (x1_6 | g347);
        long g349 = (x1_7 | g348);
        long g350 = (x1_8 | g349);
        long g351 = (x1_9 | g350);
        long g352 = (x1_10 | g351);
        long g353 = (x1_11 | g352);
        long g354 = (x1_12 | g353);
        long g355 = (x1_13 | g354);
        long g356 = (x1_14 | g355);
        long g357 = (x1_15 | g356);
        long g358 = (x1_16 | g357);
        long g359 = (x1_17 | g358);
        long g360 = (x1_18 | g359);
        long g361 = (x1_19 | g360);
        long g362 = (x1_20 | g361);
        long g363 = (x1_21 | g362);
        long g364 = (x1_22 | g363);
        long g365 = (x1_23 | g364);
        long g366 = (x1_24 | g365);
        long g367 = (x1_25 | g366);
        long g368 = (x1_26 | g367);
        long g369 = (x1_27 | g368);
        long g370 = (x1_28 | g369);
        long g371 = (x1_29 | g370);
        long g372 = (x1_30 | g371);
        long g373 = (g372 ^ x1_31);
        long g374 = (g373 ^ 1L);
        long g375 = (g374 ^ x0_31);
        long g376 = (g375 ^ 1L);
        long g377 = (g371 ^ x1_30);
        long g378 = (g377 ^ 1L);
        long g379 = (g378 ^ x0_30);
        long g380 = (g379 ^ 1L);
        long g381 = (g370 ^ x1_29);
        long g382 = (g381 ^ 1L);
        long g383 = (g382 ^ x0_29);
        long g384 = (g383 ^ 1L);
        long g385 = (g369 ^ x1_28);
        long g386 = (g385 ^ 1L);
        long g387 = (g386 ^ x0_28);
        long g388 = (g387 ^ 1L);
        long g389 = (g368 ^ x1_27);
        long g390 = (g389 ^ 1L);
        long g391 = (g390 ^ x0_27);
        long g392 = (g391 ^ 1L);
        long g393 = (g367 ^ x1_26);
        long g394 = (g393 ^ 1L);
        long g395 = (g394 ^ x0_26);
        long g396 = (g395 ^ 1L);
        long g397 = (g366 ^ x1_25);
        long g398 = (g397 ^ 1L);
        long g399 = (g398 ^ x0_25);
        long g400 = (g399 ^ 1L);
        long g401 = (g365 ^ x1_24);
        long g402 = (g401 ^ 1L);
        long g403 = (g402 ^ x0_24);
        long g404 = (g403 ^ 1L);
        long g405 = (g364 ^ x1_23);
        long g406 = (g405 ^ 1L);
        long g407 = (g406 ^ x0_23);
        long g408 = (g407 ^ 1L);
        long g409 = (g363 ^ x1_22);
        long g410 = (g409 ^ 1L);
        long g411 = (g410 ^ x0_22);
        long g412 = (g411 ^ 1L);
        long g413 = (g362 ^ x1_21);
        long g414 = (g413 ^ 1L);
        long g415 = (g414 ^ x0_21);
        long g416 = (g415 ^ 1L);
        long g417 = (g361 ^ x1_20);
        long g418 = (g417 ^ 1L);
        long g419 = (g418 ^ x0_20);
        long g420 = (g419 ^ 1L);
        long g421 = (g360 ^ x1_19);
        long g422 = (g421 ^ 1L);
        long g423 = (g422 ^ x0_19);
        long g424 = (g423 ^ 1L);
        long g425 = (g359 ^ x1_18);
        long g426 = (g425 ^ 1L);
        long g427 = (g426 ^ x0_18);
        long g428 = (g427 ^ 1L);
        long g429 = (g358 ^ x1_17);
        long g430 = (g429 ^ 1L);
        long g431 = (g430 ^ x0_17);
        long g432 = (g431 ^ 1L);
        long g433 = (g357 ^ x1_16);
        long g434 = (g433 ^ 1L);
        long g435 = (g434 ^ x0_16);
        long g436 = (g435 ^ 1L);
        long g437 = (g356 ^ x1_15);
        long g438 = (g437 ^ 1L);
        long g439 = (g438 ^ x0_15);
        long g440 = (g439 ^ 1L);
        long g441 = (g355 ^ x1_14);
        long g442 = (g441 ^ 1L);
        long g443 = (g442 ^ x0_14);
        long g444 = (g443 ^ 1L);
        long g445 = (g354 ^ x1_13);
        long g446 = (g445 ^ 1L);
        long g447 = (g446 ^ x0_13);
        long g448 = (g447 ^ 1L);
        long g449 = (g353 ^ x1_12);
        long g450 = (g449 ^ 1L);
        long g451 = (g450 ^ x0_12);
        long g452 = (g451 ^ 1L);
        long g453 = (g352 ^ x1_11);
        long g454 = (g453 ^ 1L);
        long g455 = (g454 ^ x0_11);
        long g456 = (g455 ^ 1L);
        long g457 = (g351 ^ x1_10);
        long g458 = (g457 ^ 1L);
        long g459 = (g458 ^ x0_10);
        long g460 = (g459 ^ 1L);
        long g461 = (g350 ^ x1_9);
        long g462 = (g461 ^ 1L);
        long g463 = (g462 ^ x0_9);
        long g464 = (g463 ^ 1L);
        long g465 = (g349 ^ x1_8);
        long g466 = (g465 ^ 1L);
        long g467 = (g466 ^ x0_8);
        long g468 = (g467 ^ 1L);
        long g469 = (g348 ^ x1_7);
        long g470 = (g469 ^ 1L);
        long g471 = (g470 ^ x0_7);
        long g472 = (g471 ^ 1L);
        long g473 = (g347 ^ x1_6);
        long g474 = (g473 ^ 1L);
        long g475 = (g474 ^ x0_6);
        long g476 = (g475 ^ 1L);
        long g477 = (g346 ^ x1_5);
        long g478 = (g477 ^ 1L);
        long g479 = (g478 ^ x0_5);
        long g480 = (g479 ^ 1L);
        long g481 = (g345 ^ x1_4);
        long g482 = (g481 ^ 1L);
        long g483 = (g482 ^ x0_4);
        long g484 = (g483 ^ 1L);
        long g485 = (g344 ^ x1_3);
        long g486 = (g485 ^ 1L);
        long g487 = (g486 ^ x0_3);
        long g488 = (g487 ^ 1L);
        long g489 = (g343 ^ x1_2);
        long g490 = (g489 ^ 1L);
        long g491 = (g490 ^ x0_2);
        long g492 = (g491 ^ 1L);
        long g493 = (x1_0 ^ x1_1);
        long g494 = (g493 ^ 1L);
        long g495 = (g494 ^ x0_1);
        long g496 = (g495 ^ 1L);
        long g497 = (x1_0 ^ x0_0);
        long g498 = (g497 ^ 1L);
        long g499 = (g498 ^ 1L);
        long g500 = (g499 | g496);
        long g501 = (g500 | g492);
        long g502 = (g501 | g488);
        long g503 = (g502 | g484);
        long g504 = (g503 | g480);
        long g505 = (g504 | g476);
        long g506 = (g505 | g472);
        long g507 = (g506 | g468);
        long g508 = (g507 | g464);
        long g509 = (g508 | g460);
        long g510 = (g509 | g456);
        long g511 = (g510 | g452);
        long g512 = (g511 | g448);
        long g513 = (g512 | g444);
        long g514 = (g513 | g440);
        long g515 = (g514 | g436);
        long g516 = (g515 | g432);
        long g517 = (g516 | g428);
        long g518 = (g517 | g424);
        long g519 = (g518 | g420);
        long g520 = (g519 | g416);
        long g521 = (g520 | g412);
        long g522 = (g521 | g408);
        long g523 = (g522 | g404);
        long g524 = (g523 | g400);
        long g525 = (g524 | g396);
        long g526 = (g525 | g392);
        long g527 = (g526 | g388);
        long g528 = (g527 | g384);
        long g529 = (g528 | g380);
        long g530 = (g529 | g376);
        long g531 = (g530 ^ 1L);
        long g532 = (g531 | g342);
        long g533 = (g532 ^ 1L);
        long g534 = (g533 & x3_0);
        long g535 = (g532 & x2_0);
        long g536 = (g535 | g534);
        long g537 = (g533 & x3_1);
        long g538 = (g532 & x2_1);
        long g539 = (g538 | g537);
        long g540 = (g533 & x3_2);
        long g541 = (g532 & x2_2);
        long g542 = (g541 | g540);
        long g543 = (g533 & x3_3);
        long g544 = (g532 & x2_3);
        long g545 = (g544 | g543);
        long g546 = (g533 & x3_4);
        long g547 = (g532 & x2_4);
        long g548 = (g547 | g546);
        long g549 = (g533 & x3_5);
        long g550 = (g532 & x2_5);
        long g551 = (g550 | g549);
        long g552 = (g533 & x3_6);
        long g553 = (g532 & x2_6);
        long g554 = (g553 | g552);
        long g555 = (g533 & x3_7);
        long g556 = (g532 & x2_7);
        long g557 = (g556 | g555);
        long g558 = (g533 & x3_8);
        long g559 = (g532 & x2_8);
        long g560 = (g559 | g558);
        long g561 = (g533 & x3_9);
        long g562 = (g532 & x2_9);
        long g563 = (g562 | g561);
        long g564 = (g533 & x3_10);
        long g565 = (g532 & x2_10);
        long g566 = (g565 | g564);
        long g567 = (g533 & x3_11);
        long g568 = (g532 & x2_11);
        long g569 = (g568 | g567);
        long g570 = (g533 & x3_12);
        long g571 = (g532 & x2_12);
        long g572 = (g571 | g570);
        long g573 = (g533 & x3_13);
        long g574 = (g532 & x2_13);
        long g575 = (g574 | g573);
        long g576 = (g533 & x3_14);
        long g577 = (g532 & x2_14);
        long g578 = (g577 | g576);
        long g579 = (g533 & x3_15);
        long g580 = (g532 & x2_15);
        long g581 = (g580 | g579);
        long g582 = (g533 & x3_16);
        long g583 = (g532 & x2_16);
        long g584 = (g583 | g582);
        long g585 = (g533 & x3_17);
        long g586 = (g532 & x2_17);
        long g587 = (g586 | g585);
        long g588 = (g533 & x3_18);
        long g589 = (g532 & x2_18);
        long g590 = (g589 | g588);
        long g591 = (g533 & x3_19);
        long g592 = (g532 & x2_19);
        long g593 = (g592 | g591);
        long g594 = (g533 & x3_20);
        long g595 = (g532 & x2_20);
        long g596 = (g595 | g594);
        long g597 = (g533 & x3_21);
        long g598 = (g532 & x2_21);
        long g599 = (g598 | g597);
        long g600 = (g533 & x3_22);
        long g601 = (g532 & x2_22);
        long g602 = (g601 | g600);
        long g603 = (g533 & x3_23);
        long g604 = (g532 & x2_23);
        long g605 = (g604 | g603);
        long g606 = (g533 & x3_24);
        long g607 = (g532 & x2_24);
        long g608 = (g607 | g606);
        long g609 = (g533 & x3_25);
        long g610 = (g532 & x2_25);
        long g611 = (g610 | g609);
        long g612 = (g533 & x3_26);
        long g613 = (g532 & x2_26);
        long g614 = (g613 | g612);
        long g615 = (g533 & x3_27);
        long g616 = (g532 & x2_27);
        long g617 = (g616 | g615);
        long g618 = (g533 & x3_28);
        long g619 = (g532 & x2_28);
        long g620 = (g619 | g618);
        long g621 = (g533 & x3_29);
        long g622 = (g532 & x2_29);
        long g623 = (g622 | g621);
        long g624 = (g533 & x3_30);
        long g625 = (g532 & x2_30);
        long g626 = (g625 | g624);
        long g627 = (g533 & x3_31);
        long g628 = (g532 & x2_31);
        long g629 = (g628 | g627);
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
        long w32 = cat(w31, g629, 1);
        long w33 = cat(w32, g626, 1);
        long w34 = cat(w33, g623, 1);
        long w35 = cat(w34, g620, 1);
        long w36 = cat(w35, g617, 1);
        long w37 = cat(w36, g614, 1);
        long w38 = cat(w37, g611, 1);
        long w39 = cat(w38, g608, 1);
        long w40 = cat(w39, g605, 1);
        long w41 = cat(w40, g602, 1);
        long w42 = cat(w41, g599, 1);
        long w43 = cat(w42, g596, 1);
        long w44 = cat(w43, g593, 1);
        long w45 = cat(w44, g590, 1);
        long w46 = cat(w45, g587, 1);
        long w47 = cat(w46, g584, 1);
        long w48 = cat(w47, g581, 1);
        long w49 = cat(w48, g578, 1);
        long w50 = cat(w49, g575, 1);
        long w51 = cat(w50, g572, 1);
        long w52 = cat(w51, g569, 1);
        long w53 = cat(w52, g566, 1);
        long w54 = cat(w53, g563, 1);
        long w55 = cat(w54, g560, 1);
        long w56 = cat(w55, g557, 1);
        long w57 = cat(w56, g554, 1);
        long w58 = cat(w57, g551, 1);
        long w59 = cat(w58, g548, 1);
        long w60 = cat(w59, g545, 1);
        long w61 = cat(w60, g542, 1);
        long w62 = cat(w61, g539, 1);
        long w63 = cat(w62, g536, 1);
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
                    answers.append(Long.toUnsignedString(emu_cmovbe_gpr_gpr_32__reg_rdi__java(values[0], values[1], values[2], values[3])));
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
