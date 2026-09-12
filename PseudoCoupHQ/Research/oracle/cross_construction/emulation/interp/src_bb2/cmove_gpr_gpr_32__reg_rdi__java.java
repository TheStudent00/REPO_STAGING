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
    // one named local per gate, over the term of cmove_gpr_gpr_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
    static long emu_cmove_gpr_gpr_32__reg_rdi__java(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
        long x1_12 = ext(a, 12, 12);
        long x0_12 = ext(b, 12, 12);
        long x1_17 = ext(a, 17, 17);
        long x0_17 = ext(b, 17, 17);
        long x1_1 = ext(a, 1, 1);
        long x0_1 = ext(b, 1, 1);
        long x1_19 = ext(a, 19, 19);
        long x0_19 = ext(b, 19, 19);
        long x1_23 = ext(a, 23, 23);
        long x0_23 = ext(b, 23, 23);
        long x1_21 = ext(a, 21, 21);
        long x0_21 = ext(b, 21, 21);
        long x1_18 = ext(a, 18, 18);
        long x0_18 = ext(b, 18, 18);
        long x1_16 = ext(a, 16, 16);
        long x0_16 = ext(b, 16, 16);
        long x1_14 = ext(a, 14, 14);
        long x0_14 = ext(b, 14, 14);
        long x1_28 = ext(a, 28, 28);
        long x0_28 = ext(b, 28, 28);
        long x1_15 = ext(a, 15, 15);
        long x0_15 = ext(b, 15, 15);
        long x1_30 = ext(a, 30, 30);
        long x0_30 = ext(b, 30, 30);
        long x1_8 = ext(a, 8, 8);
        long x0_8 = ext(b, 8, 8);
        long x1_9 = ext(a, 9, 9);
        long x0_9 = ext(b, 9, 9);
        long x1_10 = ext(a, 10, 10);
        long x0_10 = ext(b, 10, 10);
        long x1_26 = ext(a, 26, 26);
        long x0_26 = ext(b, 26, 26);
        long x1_4 = ext(a, 4, 4);
        long x0_4 = ext(b, 4, 4);
        long x1_31 = ext(a, 31, 31);
        long x0_31 = ext(b, 31, 31);
        long x1_24 = ext(a, 24, 24);
        long x0_24 = ext(b, 24, 24);
        long x1_29 = ext(a, 29, 29);
        long x0_29 = ext(b, 29, 29);
        long x1_25 = ext(a, 25, 25);
        long x0_25 = ext(b, 25, 25);
        long x1_13 = ext(a, 13, 13);
        long x0_13 = ext(b, 13, 13);
        long x1_3 = ext(a, 3, 3);
        long x0_3 = ext(b, 3, 3);
        long x1_6 = ext(a, 6, 6);
        long x0_6 = ext(b, 6, 6);
        long x1_0 = ext(a, 0, 0);
        long x0_0 = ext(b, 0, 0);
        long x1_11 = ext(a, 11, 11);
        long x0_11 = ext(b, 11, 11);
        long x1_27 = ext(a, 27, 27);
        long x0_27 = ext(b, 27, 27);
        long x1_20 = ext(a, 20, 20);
        long x0_20 = ext(b, 20, 20);
        long x1_5 = ext(a, 5, 5);
        long x0_5 = ext(b, 5, 5);
        long x1_22 = ext(a, 22, 22);
        long x0_22 = ext(b, 22, 22);
        long x1_7 = ext(a, 7, 7);
        long x0_7 = ext(b, 7, 7);
        long x1_2 = ext(a, 2, 2);
        long x0_2 = ext(b, 2, 2);
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
        long g0 = (x1_12 ^ 1L);
        long g1 = (x0_12 ^ 1L);
        long g2 = (g1 | g0);
        long g3 = (g2 ^ 1L);
        long g4 = (x1_17 ^ 1L);
        long g5 = (x0_17 ^ 1L);
        long g6 = (g5 | g4);
        long g7 = (g6 ^ 1L);
        long g8 = (x1_1 ^ 1L);
        long g9 = (x0_1 ^ 1L);
        long g10 = (g9 | g8);
        long g11 = (g10 ^ 1L);
        long g12 = (x1_19 ^ 1L);
        long g13 = (x0_19 ^ 1L);
        long g14 = (g13 | g12);
        long g15 = (g14 ^ 1L);
        long g16 = (x1_23 ^ 1L);
        long g17 = (x0_23 ^ 1L);
        long g18 = (g17 | g16);
        long g19 = (g18 ^ 1L);
        long g20 = (x1_21 ^ 1L);
        long g21 = (x0_21 ^ 1L);
        long g22 = (g21 | g20);
        long g23 = (g22 ^ 1L);
        long g24 = (x1_18 ^ 1L);
        long g25 = (x0_18 ^ 1L);
        long g26 = (g25 | g24);
        long g27 = (g26 ^ 1L);
        long g28 = (x1_16 ^ 1L);
        long g29 = (x0_16 ^ 1L);
        long g30 = (g29 | g28);
        long g31 = (g30 ^ 1L);
        long g32 = (x1_14 ^ 1L);
        long g33 = (x0_14 ^ 1L);
        long g34 = (g33 | g32);
        long g35 = (g34 ^ 1L);
        long g36 = (x1_28 ^ 1L);
        long g37 = (x0_28 ^ 1L);
        long g38 = (g37 | g36);
        long g39 = (g38 ^ 1L);
        long g40 = (x1_15 ^ 1L);
        long g41 = (x0_15 ^ 1L);
        long g42 = (g41 | g40);
        long g43 = (g42 ^ 1L);
        long g44 = (x1_30 ^ 1L);
        long g45 = (x0_30 ^ 1L);
        long g46 = (g45 | g44);
        long g47 = (g46 ^ 1L);
        long g48 = (x1_8 ^ 1L);
        long g49 = (x0_8 ^ 1L);
        long g50 = (g49 | g48);
        long g51 = (g50 ^ 1L);
        long g52 = (x1_9 ^ 1L);
        long g53 = (x0_9 ^ 1L);
        long g54 = (g53 | g52);
        long g55 = (g54 ^ 1L);
        long g56 = (x1_10 ^ 1L);
        long g57 = (x0_10 ^ 1L);
        long g58 = (g57 | g56);
        long g59 = (g58 ^ 1L);
        long g60 = (x1_26 ^ 1L);
        long g61 = (x0_26 ^ 1L);
        long g62 = (g61 | g60);
        long g63 = (g62 ^ 1L);
        long g64 = (x1_4 ^ 1L);
        long g65 = (x0_4 ^ 1L);
        long g66 = (g65 | g64);
        long g67 = (g66 ^ 1L);
        long g68 = (x1_31 ^ 1L);
        long g69 = (x0_31 ^ 1L);
        long g70 = (g69 | g68);
        long g71 = (g70 ^ 1L);
        long g72 = (x1_24 ^ 1L);
        long g73 = (x0_24 ^ 1L);
        long g74 = (g73 | g72);
        long g75 = (g74 ^ 1L);
        long g76 = (x1_29 ^ 1L);
        long g77 = (x0_29 ^ 1L);
        long g78 = (g77 | g76);
        long g79 = (g78 ^ 1L);
        long g80 = (x1_25 ^ 1L);
        long g81 = (x0_25 ^ 1L);
        long g82 = (g81 | g80);
        long g83 = (g82 ^ 1L);
        long g84 = (x1_13 ^ 1L);
        long g85 = (x0_13 ^ 1L);
        long g86 = (g85 | g84);
        long g87 = (g86 ^ 1L);
        long g88 = (x1_3 ^ 1L);
        long g89 = (x0_3 ^ 1L);
        long g90 = (g89 | g88);
        long g91 = (g90 ^ 1L);
        long g92 = (x1_6 ^ 1L);
        long g93 = (x0_6 ^ 1L);
        long g94 = (g93 | g92);
        long g95 = (g94 ^ 1L);
        long g96 = (x1_0 ^ 1L);
        long g97 = (x0_0 ^ 1L);
        long g98 = (g97 | g96);
        long g99 = (g98 ^ 1L);
        long g100 = (x1_11 ^ 1L);
        long g101 = (x0_11 ^ 1L);
        long g102 = (g101 | g100);
        long g103 = (g102 ^ 1L);
        long g104 = (x1_27 ^ 1L);
        long g105 = (x0_27 ^ 1L);
        long g106 = (g105 | g104);
        long g107 = (g106 ^ 1L);
        long g108 = (x1_20 ^ 1L);
        long g109 = (x0_20 ^ 1L);
        long g110 = (g109 | g108);
        long g111 = (g110 ^ 1L);
        long g112 = (x1_5 ^ 1L);
        long g113 = (x0_5 ^ 1L);
        long g114 = (g113 | g112);
        long g115 = (g114 ^ 1L);
        long g116 = (x1_22 ^ 1L);
        long g117 = (x0_22 ^ 1L);
        long g118 = (g117 | g116);
        long g119 = (g118 ^ 1L);
        long g120 = (x1_7 ^ 1L);
        long g121 = (x0_7 ^ 1L);
        long g122 = (g121 | g120);
        long g123 = (g122 ^ 1L);
        long g124 = (x1_2 ^ 1L);
        long g125 = (x0_2 ^ 1L);
        long g126 = (g125 | g124);
        long g127 = (g126 ^ 1L);
        long g128 = (g127 | g123);
        long g129 = (g128 | g119);
        long g130 = (g129 | g115);
        long g131 = (g130 | g111);
        long g132 = (g131 | g107);
        long g133 = (g132 | g103);
        long g134 = (g133 | g99);
        long g135 = (g134 | g95);
        long g136 = (g135 | g91);
        long g137 = (g136 | g87);
        long g138 = (g137 | g83);
        long g139 = (g138 | g79);
        long g140 = (g139 | g75);
        long g141 = (g140 | g71);
        long g142 = (g141 | g67);
        long g143 = (g142 | g63);
        long g144 = (g143 | g59);
        long g145 = (g144 | g55);
        long g146 = (g145 | g51);
        long g147 = (g146 | g47);
        long g148 = (g147 | g43);
        long g149 = (g148 | g39);
        long g150 = (g149 | g35);
        long g151 = (g150 | g31);
        long g152 = (g151 | g27);
        long g153 = (g152 | g23);
        long g154 = (g153 | g19);
        long g155 = (g154 | g15);
        long g156 = (g155 | g11);
        long g157 = (g156 | g7);
        long g158 = (g157 | g3);
        long g159 = (g158 ^ 1L);
        long g160 = (g159 ^ 1L);
        long g161 = (g160 & x3_0);
        long g162 = (g159 & x2_0);
        long g163 = (g162 | g161);
        long g164 = (g160 & x3_1);
        long g165 = (g159 & x2_1);
        long g166 = (g165 | g164);
        long g167 = (g160 & x3_2);
        long g168 = (g159 & x2_2);
        long g169 = (g168 | g167);
        long g170 = (g160 & x3_3);
        long g171 = (g159 & x2_3);
        long g172 = (g171 | g170);
        long g173 = (g160 & x3_4);
        long g174 = (g159 & x2_4);
        long g175 = (g174 | g173);
        long g176 = (g160 & x3_5);
        long g177 = (g159 & x2_5);
        long g178 = (g177 | g176);
        long g179 = (g160 & x3_6);
        long g180 = (g159 & x2_6);
        long g181 = (g180 | g179);
        long g182 = (g160 & x3_7);
        long g183 = (g159 & x2_7);
        long g184 = (g183 | g182);
        long g185 = (g160 & x3_8);
        long g186 = (g159 & x2_8);
        long g187 = (g186 | g185);
        long g188 = (g160 & x3_9);
        long g189 = (g159 & x2_9);
        long g190 = (g189 | g188);
        long g191 = (g160 & x3_10);
        long g192 = (g159 & x2_10);
        long g193 = (g192 | g191);
        long g194 = (g160 & x3_11);
        long g195 = (g159 & x2_11);
        long g196 = (g195 | g194);
        long g197 = (g160 & x3_12);
        long g198 = (g159 & x2_12);
        long g199 = (g198 | g197);
        long g200 = (g160 & x3_13);
        long g201 = (g159 & x2_13);
        long g202 = (g201 | g200);
        long g203 = (g160 & x3_14);
        long g204 = (g159 & x2_14);
        long g205 = (g204 | g203);
        long g206 = (g160 & x3_15);
        long g207 = (g159 & x2_15);
        long g208 = (g207 | g206);
        long g209 = (g160 & x3_16);
        long g210 = (g159 & x2_16);
        long g211 = (g210 | g209);
        long g212 = (g160 & x3_17);
        long g213 = (g159 & x2_17);
        long g214 = (g213 | g212);
        long g215 = (g160 & x3_18);
        long g216 = (g159 & x2_18);
        long g217 = (g216 | g215);
        long g218 = (g160 & x3_19);
        long g219 = (g159 & x2_19);
        long g220 = (g219 | g218);
        long g221 = (g160 & x3_20);
        long g222 = (g159 & x2_20);
        long g223 = (g222 | g221);
        long g224 = (g160 & x3_21);
        long g225 = (g159 & x2_21);
        long g226 = (g225 | g224);
        long g227 = (g160 & x3_22);
        long g228 = (g159 & x2_22);
        long g229 = (g228 | g227);
        long g230 = (g160 & x3_23);
        long g231 = (g159 & x2_23);
        long g232 = (g231 | g230);
        long g233 = (g160 & x3_24);
        long g234 = (g159 & x2_24);
        long g235 = (g234 | g233);
        long g236 = (g160 & x3_25);
        long g237 = (g159 & x2_25);
        long g238 = (g237 | g236);
        long g239 = (g160 & x3_26);
        long g240 = (g159 & x2_26);
        long g241 = (g240 | g239);
        long g242 = (g160 & x3_27);
        long g243 = (g159 & x2_27);
        long g244 = (g243 | g242);
        long g245 = (g160 & x3_28);
        long g246 = (g159 & x2_28);
        long g247 = (g246 | g245);
        long g248 = (g160 & x3_29);
        long g249 = (g159 & x2_29);
        long g250 = (g249 | g248);
        long g251 = (g160 & x3_30);
        long g252 = (g159 & x2_30);
        long g253 = (g252 | g251);
        long g254 = (g160 & x3_31);
        long g255 = (g159 & x2_31);
        long g256 = (g255 | g254);
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
        long w32 = cat(w31, g256, 1);
        long w33 = cat(w32, g253, 1);
        long w34 = cat(w33, g250, 1);
        long w35 = cat(w34, g247, 1);
        long w36 = cat(w35, g244, 1);
        long w37 = cat(w36, g241, 1);
        long w38 = cat(w37, g238, 1);
        long w39 = cat(w38, g235, 1);
        long w40 = cat(w39, g232, 1);
        long w41 = cat(w40, g229, 1);
        long w42 = cat(w41, g226, 1);
        long w43 = cat(w42, g223, 1);
        long w44 = cat(w43, g220, 1);
        long w45 = cat(w44, g217, 1);
        long w46 = cat(w45, g214, 1);
        long w47 = cat(w46, g211, 1);
        long w48 = cat(w47, g208, 1);
        long w49 = cat(w48, g205, 1);
        long w50 = cat(w49, g202, 1);
        long w51 = cat(w50, g199, 1);
        long w52 = cat(w51, g196, 1);
        long w53 = cat(w52, g193, 1);
        long w54 = cat(w53, g190, 1);
        long w55 = cat(w54, g187, 1);
        long w56 = cat(w55, g184, 1);
        long w57 = cat(w56, g181, 1);
        long w58 = cat(w57, g178, 1);
        long w59 = cat(w58, g175, 1);
        long w60 = cat(w59, g172, 1);
        long w61 = cat(w60, g169, 1);
        long w62 = cat(w61, g166, 1);
        long w63 = cat(w62, g163, 1);
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
                    answers.append(Long.toUnsignedString(emu_cmove_gpr_gpr_32__reg_rdi__java(values[0], values[1], values[2], values[3])));
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
