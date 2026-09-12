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
    // one named local per gate, over the term of cmovl_gpr_gpr_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(Extract(31, 31, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1)) == If(Extract(31, 31, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))) == Extract(32, 32, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))), 1, 0), Extract(31, 0, v2), Extract(31, 0, v3)))
    static long emu_cmovl_gpr_gpr_32__reg_rdi__java(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
        long x0_31 = ext(b, 31, 31);
        long x0_1 = ext(b, 1, 1);
        long x0_0 = ext(b, 0, 0);
        long x0_2 = ext(b, 2, 2);
        long x0_3 = ext(b, 3, 3);
        long x0_4 = ext(b, 4, 4);
        long x0_5 = ext(b, 5, 5);
        long x0_6 = ext(b, 6, 6);
        long x0_7 = ext(b, 7, 7);
        long x0_8 = ext(b, 8, 8);
        long x0_9 = ext(b, 9, 9);
        long x0_10 = ext(b, 10, 10);
        long x0_11 = ext(b, 11, 11);
        long x0_12 = ext(b, 12, 12);
        long x0_13 = ext(b, 13, 13);
        long x0_14 = ext(b, 14, 14);
        long x0_15 = ext(b, 15, 15);
        long x0_16 = ext(b, 16, 16);
        long x0_17 = ext(b, 17, 17);
        long x0_18 = ext(b, 18, 18);
        long x0_19 = ext(b, 19, 19);
        long x0_20 = ext(b, 20, 20);
        long x0_21 = ext(b, 21, 21);
        long x0_22 = ext(b, 22, 22);
        long x0_23 = ext(b, 23, 23);
        long x0_24 = ext(b, 24, 24);
        long x0_25 = ext(b, 25, 25);
        long x0_26 = ext(b, 26, 26);
        long x0_27 = ext(b, 27, 27);
        long x0_28 = ext(b, 28, 28);
        long x0_29 = ext(b, 29, 29);
        long x0_30 = ext(b, 30, 30);
        long x1_29 = ext(a, 29, 29);
        long x1_27 = ext(a, 27, 27);
        long x1_24 = ext(a, 24, 24);
        long x1_22 = ext(a, 22, 22);
        long x1_19 = ext(a, 19, 19);
        long x1_18 = ext(a, 18, 18);
        long x1_13 = ext(a, 13, 13);
        long x1_6 = ext(a, 6, 6);
        long x1_5 = ext(a, 5, 5);
        long x1_2 = ext(a, 2, 2);
        long x1_1 = ext(a, 1, 1);
        long x1_0 = ext(a, 0, 0);
        long x1_3 = ext(a, 3, 3);
        long x1_4 = ext(a, 4, 4);
        long x1_7 = ext(a, 7, 7);
        long x1_8 = ext(a, 8, 8);
        long x1_9 = ext(a, 9, 9);
        long x1_10 = ext(a, 10, 10);
        long x1_11 = ext(a, 11, 11);
        long x1_12 = ext(a, 12, 12);
        long x1_14 = ext(a, 14, 14);
        long x1_15 = ext(a, 15, 15);
        long x1_16 = ext(a, 16, 16);
        long x1_17 = ext(a, 17, 17);
        long x1_20 = ext(a, 20, 20);
        long x1_21 = ext(a, 21, 21);
        long x1_23 = ext(a, 23, 23);
        long x1_25 = ext(a, 25, 25);
        long x1_26 = ext(a, 26, 26);
        long x1_28 = ext(a, 28, 28);
        long x1_30 = ext(a, 30, 30);
        long x1_31 = ext(a, 31, 31);
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
        long g0 = (x0_0 | x0_1);
        long g1 = (x0_2 | g0);
        long g2 = (x0_3 | g1);
        long g3 = (x0_4 | g2);
        long g4 = (x0_5 | g3);
        long g5 = (x0_6 | g4);
        long g6 = (x0_7 | g5);
        long g7 = (x0_8 | g6);
        long g8 = (x0_9 | g7);
        long g9 = (x0_10 | g8);
        long g10 = (x0_11 | g9);
        long g11 = (x0_12 | g10);
        long g12 = (x0_13 | g11);
        long g13 = (x0_14 | g12);
        long g14 = (x0_15 | g13);
        long g15 = (x0_16 | g14);
        long g16 = (x0_17 | g15);
        long g17 = (x0_18 | g16);
        long g18 = (x0_19 | g17);
        long g19 = (x0_20 | g18);
        long g20 = (x0_21 | g19);
        long g21 = (x0_22 | g20);
        long g22 = (x0_23 | g21);
        long g23 = (x0_24 | g22);
        long g24 = (x0_25 | g23);
        long g25 = (x0_26 | g24);
        long g26 = (x0_27 | g25);
        long g27 = (x0_28 | g26);
        long g28 = (x0_29 | g27);
        long g29 = (x0_30 | g28);
        long g30 = (x0_31 | g29);
        long g31 = (g30 ^ x0_31);
        long g32 = (g31 ^ 1L);
        long g33 = (g27 ^ x0_29);
        long g34 = (g33 ^ 1L);
        long g35 = (x1_29 ^ 1L);
        long g36 = (g35 | g34);
        long g37 = (g36 ^ 1L);
        long g38 = (x1_27 ^ 1L);
        long g39 = (g25 ^ x0_27);
        long g40 = (g39 ^ 1L);
        long g41 = (g40 | g38);
        long g42 = (g41 ^ 1L);
        long g43 = (g22 ^ x0_24);
        long g44 = (g43 ^ 1L);
        long g45 = (x1_24 ^ 1L);
        long g46 = (g45 | g44);
        long g47 = (g46 ^ 1L);
        long g48 = (x1_22 ^ 1L);
        long g49 = (g20 ^ x0_22);
        long g50 = (g49 ^ 1L);
        long g51 = (g50 | g48);
        long g52 = (g51 ^ 1L);
        long g53 = (g19 ^ x0_21);
        long g54 = (g53 ^ 1L);
        long g55 = (g17 ^ x0_19);
        long g56 = (g55 ^ 1L);
        long g57 = (x1_19 ^ 1L);
        long g58 = (g57 | g56);
        long g59 = (g58 ^ 1L);
        long g60 = (g16 ^ x0_18);
        long g61 = (g60 ^ 1L);
        long g62 = (x1_18 ^ 1L);
        long g63 = (g62 | g61);
        long g64 = (g63 ^ 1L);
        long g65 = (g15 ^ x0_17);
        long g66 = (g65 ^ 1L);
        long g67 = (g13 ^ x0_15);
        long g68 = (g67 ^ 1L);
        long g69 = (x1_13 ^ 1L);
        long g70 = (g11 ^ x0_13);
        long g71 = (g70 ^ 1L);
        long g72 = (g71 | g69);
        long g73 = (g72 ^ 1L);
        long g74 = (x1_6 ^ 1L);
        long g75 = (g4 ^ x0_6);
        long g76 = (g75 ^ 1L);
        long g77 = (g76 | g74);
        long g78 = (g77 ^ 1L);
        long g79 = (g3 ^ x0_5);
        long g80 = (g79 ^ 1L);
        long g81 = (x1_5 ^ 1L);
        long g82 = (g81 | g80);
        long g83 = (g82 ^ 1L);
        long g84 = (g0 ^ x0_2);
        long g85 = (g84 ^ 1L);
        long g86 = (x1_2 ^ 1L);
        long g87 = (g86 | g85);
        long g88 = (g87 ^ 1L);
        long g89 = (x0_0 ^ x0_1);
        long g90 = (g89 ^ 1L);
        long g91 = (x1_1 ^ 1L);
        long g92 = (g91 | g90);
        long g93 = (g92 ^ 1L);
        long g94 = (x1_0 ^ 1L);
        long g95 = (x0_0 ^ 1L);
        long g96 = (g95 | g94);
        long g97 = (g90 | g96);
        long g98 = (g97 ^ 1L);
        long g99 = (g91 | g96);
        long g100 = (g99 ^ 1L);
        long g101 = (g100 | g98);
        long g102 = (g101 | g93);
        long g103 = (g102 ^ 1L);
        long g104 = (g85 | g103);
        long g105 = (g104 ^ 1L);
        long g106 = (g86 | g103);
        long g107 = (g106 ^ 1L);
        long g108 = (g107 | g105);
        long g109 = (g108 | g88);
        long g110 = (g109 ^ 1L);
        long g111 = (x1_3 ^ 1L);
        long g112 = (g111 | g110);
        long g113 = (g112 ^ 1L);
        long g114 = (g1 ^ x0_3);
        long g115 = (g114 ^ 1L);
        long g116 = (g110 | g115);
        long g117 = (g116 ^ 1L);
        long g118 = (g111 | g115);
        long g119 = (g118 ^ 1L);
        long g120 = (g119 | g117);
        long g121 = (g120 | g113);
        long g122 = (g121 ^ 1L);
        long g123 = (x1_4 ^ 1L);
        long g124 = (g123 | g122);
        long g125 = (g124 ^ 1L);
        long g126 = (g2 ^ x0_4);
        long g127 = (g126 ^ 1L);
        long g128 = (g123 | g127);
        long g129 = (g128 ^ 1L);
        long g130 = (g122 | g127);
        long g131 = (g130 ^ 1L);
        long g132 = (g131 | g129);
        long g133 = (g132 | g125);
        long g134 = (g133 ^ 1L);
        long g135 = (g81 | g134);
        long g136 = (g135 ^ 1L);
        long g137 = (g134 | g80);
        long g138 = (g137 ^ 1L);
        long g139 = (g138 | g136);
        long g140 = (g139 | g83);
        long g141 = (g140 ^ 1L);
        long g142 = (g76 | g141);
        long g143 = (g142 ^ 1L);
        long g144 = (g74 | g141);
        long g145 = (g144 ^ 1L);
        long g146 = (g145 | g143);
        long g147 = (g146 | g78);
        long g148 = (g147 ^ 1L);
        long g149 = (g5 ^ x0_7);
        long g150 = (g149 ^ 1L);
        long g151 = (g150 | g148);
        long g152 = (g151 ^ 1L);
        long g153 = (x1_7 ^ 1L);
        long g154 = (g153 | g148);
        long g155 = (g154 ^ 1L);
        long g156 = (g150 | g153);
        long g157 = (g156 ^ 1L);
        long g158 = (g157 | g155);
        long g159 = (g158 | g152);
        long g160 = (g159 ^ 1L);
        long g161 = (g6 ^ x0_8);
        long g162 = (g161 ^ 1L);
        long g163 = (g162 | g160);
        long g164 = (g163 ^ 1L);
        long g165 = (x1_8 ^ 1L);
        long g166 = (g165 | g162);
        long g167 = (g166 ^ 1L);
        long g168 = (g165 | g160);
        long g169 = (g168 ^ 1L);
        long g170 = (g169 | g167);
        long g171 = (g170 | g164);
        long g172 = (g171 ^ 1L);
        long g173 = (x1_9 ^ 1L);
        long g174 = (g173 | g172);
        long g175 = (g174 ^ 1L);
        long g176 = (g7 ^ x0_9);
        long g177 = (g176 ^ 1L);
        long g178 = (g172 | g177);
        long g179 = (g178 ^ 1L);
        long g180 = (g177 | g173);
        long g181 = (g180 ^ 1L);
        long g182 = (g181 | g179);
        long g183 = (g182 | g175);
        long g184 = (g183 ^ 1L);
        long g185 = (x1_10 ^ 1L);
        long g186 = (g185 | g184);
        long g187 = (g186 ^ 1L);
        long g188 = (g8 ^ x0_10);
        long g189 = (g188 ^ 1L);
        long g190 = (g185 | g189);
        long g191 = (g190 ^ 1L);
        long g192 = (g184 | g189);
        long g193 = (g192 ^ 1L);
        long g194 = (g193 | g191);
        long g195 = (g194 | g187);
        long g196 = (g195 ^ 1L);
        long g197 = (x1_11 ^ 1L);
        long g198 = (g197 | g196);
        long g199 = (g198 ^ 1L);
        long g200 = (g9 ^ x0_11);
        long g201 = (g200 ^ 1L);
        long g202 = (g201 | g197);
        long g203 = (g202 ^ 1L);
        long g204 = (g196 | g201);
        long g205 = (g204 ^ 1L);
        long g206 = (g205 | g203);
        long g207 = (g206 | g199);
        long g208 = (g207 ^ 1L);
        long g209 = (x1_12 ^ 1L);
        long g210 = (g209 | g208);
        long g211 = (g210 ^ 1L);
        long g212 = (g10 ^ x0_12);
        long g213 = (g212 ^ 1L);
        long g214 = (g213 | g208);
        long g215 = (g214 ^ 1L);
        long g216 = (g209 | g213);
        long g217 = (g216 ^ 1L);
        long g218 = (g217 | g215);
        long g219 = (g218 | g211);
        long g220 = (g219 ^ 1L);
        long g221 = (g71 | g220);
        long g222 = (g221 ^ 1L);
        long g223 = (g69 | g220);
        long g224 = (g223 ^ 1L);
        long g225 = (g224 | g222);
        long g226 = (g225 | g73);
        long g227 = (g226 ^ 1L);
        long g228 = (x1_14 ^ 1L);
        long g229 = (g228 | g227);
        long g230 = (g229 ^ 1L);
        long g231 = (g12 ^ x0_14);
        long g232 = (g231 ^ 1L);
        long g233 = (g232 | g228);
        long g234 = (g233 ^ 1L);
        long g235 = (g232 | g227);
        long g236 = (g235 ^ 1L);
        long g237 = (g236 | g234);
        long g238 = (g237 | g230);
        long g239 = (g238 ^ 1L);
        long g240 = (g239 | g68);
        long g241 = (g240 ^ 1L);
        long g242 = (x1_15 ^ 1L);
        long g243 = (g242 | g239);
        long g244 = (g243 ^ 1L);
        long g245 = (g242 | g68);
        long g246 = (g245 ^ 1L);
        long g247 = (g246 | g244);
        long g248 = (g247 | g241);
        long g249 = (g248 ^ 1L);
        long g250 = (x1_16 ^ 1L);
        long g251 = (g250 | g249);
        long g252 = (g251 ^ 1L);
        long g253 = (g14 ^ x0_16);
        long g254 = (g253 ^ 1L);
        long g255 = (g254 | g249);
        long g256 = (g255 ^ 1L);
        long g257 = (g254 | g250);
        long g258 = (g257 ^ 1L);
        long g259 = (g258 | g256);
        long g260 = (g259 | g252);
        long g261 = (g260 ^ 1L);
        long g262 = (g261 | g66);
        long g263 = (g262 ^ 1L);
        long g264 = (x1_17 ^ 1L);
        long g265 = (g66 | g264);
        long g266 = (g265 ^ 1L);
        long g267 = (g264 | g261);
        long g268 = (g267 ^ 1L);
        long g269 = (g268 | g266);
        long g270 = (g269 | g263);
        long g271 = (g270 ^ 1L);
        long g272 = (g271 | g61);
        long g273 = (g272 ^ 1L);
        long g274 = (g62 | g271);
        long g275 = (g274 ^ 1L);
        long g276 = (g275 | g273);
        long g277 = (g276 | g64);
        long g278 = (g277 ^ 1L);
        long g279 = (g57 | g278);
        long g280 = (g279 ^ 1L);
        long g281 = (g56 | g278);
        long g282 = (g281 ^ 1L);
        long g283 = (g282 | g280);
        long g284 = (g283 | g59);
        long g285 = (g284 ^ 1L);
        long g286 = (g18 ^ x0_20);
        long g287 = (g286 ^ 1L);
        long g288 = (g287 | g285);
        long g289 = (g288 ^ 1L);
        long g290 = (x1_20 ^ 1L);
        long g291 = (g287 | g290);
        long g292 = (g291 ^ 1L);
        long g293 = (g290 | g285);
        long g294 = (g293 ^ 1L);
        long g295 = (g294 | g292);
        long g296 = (g295 | g289);
        long g297 = (g296 ^ 1L);
        long g298 = (g297 | g54);
        long g299 = (g298 ^ 1L);
        long g300 = (x1_21 ^ 1L);
        long g301 = (g300 | g54);
        long g302 = (g301 ^ 1L);
        long g303 = (g300 | g297);
        long g304 = (g303 ^ 1L);
        long g305 = (g304 | g302);
        long g306 = (g305 | g299);
        long g307 = (g306 ^ 1L);
        long g308 = (g50 | g307);
        long g309 = (g308 ^ 1L);
        long g310 = (g48 | g307);
        long g311 = (g310 ^ 1L);
        long g312 = (g311 | g309);
        long g313 = (g312 | g52);
        long g314 = (g313 ^ 1L);
        long g315 = (x1_23 ^ 1L);
        long g316 = (g315 | g314);
        long g317 = (g316 ^ 1L);
        long g318 = (g21 ^ x0_23);
        long g319 = (g318 ^ 1L);
        long g320 = (g319 | g315);
        long g321 = (g320 ^ 1L);
        long g322 = (g319 | g314);
        long g323 = (g322 ^ 1L);
        long g324 = (g323 | g321);
        long g325 = (g324 | g317);
        long g326 = (g325 ^ 1L);
        long g327 = (g326 | g44);
        long g328 = (g327 ^ 1L);
        long g329 = (g45 | g326);
        long g330 = (g329 ^ 1L);
        long g331 = (g330 | g328);
        long g332 = (g331 | g47);
        long g333 = (g332 ^ 1L);
        long g334 = (x1_25 ^ 1L);
        long g335 = (g334 | g333);
        long g336 = (g335 ^ 1L);
        long g337 = (g23 ^ x0_25);
        long g338 = (g337 ^ 1L);
        long g339 = (g333 | g338);
        long g340 = (g339 ^ 1L);
        long g341 = (g338 | g334);
        long g342 = (g341 ^ 1L);
        long g343 = (g342 | g340);
        long g344 = (g343 | g336);
        long g345 = (g344 ^ 1L);
        long g346 = (x1_26 ^ 1L);
        long g347 = (g346 | g345);
        long g348 = (g347 ^ 1L);
        long g349 = (g24 ^ x0_26);
        long g350 = (g349 ^ 1L);
        long g351 = (g346 | g350);
        long g352 = (g351 ^ 1L);
        long g353 = (g345 | g350);
        long g354 = (g353 ^ 1L);
        long g355 = (g354 | g352);
        long g356 = (g355 | g348);
        long g357 = (g356 ^ 1L);
        long g358 = (g38 | g357);
        long g359 = (g358 ^ 1L);
        long g360 = (g40 | g357);
        long g361 = (g360 ^ 1L);
        long g362 = (g361 | g359);
        long g363 = (g362 | g42);
        long g364 = (g363 ^ 1L);
        long g365 = (x1_28 ^ 1L);
        long g366 = (g365 | g364);
        long g367 = (g366 ^ 1L);
        long g368 = (g26 ^ x0_28);
        long g369 = (g368 ^ 1L);
        long g370 = (g369 | g364);
        long g371 = (g370 ^ 1L);
        long g372 = (g369 | g365);
        long g373 = (g372 ^ 1L);
        long g374 = (g373 | g371);
        long g375 = (g374 | g367);
        long g376 = (g375 ^ 1L);
        long g377 = (g376 | g34);
        long g378 = (g377 ^ 1L);
        long g379 = (g35 | g376);
        long g380 = (g379 ^ 1L);
        long g381 = (g380 | g378);
        long g382 = (g381 | g37);
        long g383 = (g382 ^ 1L);
        long g384 = (x1_30 ^ 1L);
        long g385 = (g384 | g383);
        long g386 = (g385 ^ 1L);
        long g387 = (g28 ^ x0_30);
        long g388 = (g387 ^ 1L);
        long g389 = (g383 | g388);
        long g390 = (g389 ^ 1L);
        long g391 = (g384 | g388);
        long g392 = (g391 ^ 1L);
        long g393 = (g392 | g390);
        long g394 = (g393 | g386);
        long g395 = (g394 ^ 1L);
        long g396 = (g29 ^ x0_31);
        long g397 = (g396 ^ 1L);
        long g398 = (g397 | g395);
        long g399 = (g398 ^ 1L);
        long g400 = (x1_31 ^ 1L);
        long g401 = (g400 | g397);
        long g402 = (g401 ^ 1L);
        long g403 = (g400 | g395);
        long g404 = (g403 ^ 1L);
        long g405 = (g404 | g402);
        long g406 = (g405 | g399);
        long g407 = (x1_31 ^ g406);
        long g408 = (g407 ^ 1L);
        long g409 = (g408 ^ g32);
        long g410 = (g409 ^ 1L);
        long g411 = (x1_31 ^ g394);
        long g412 = (g411 ^ 1L);
        long g413 = (g412 ^ g397);
        long g414 = (g413 ^ 1L);
        long g415 = (g414 ^ g410);
        long g416 = (g415 ^ 1L);
        long g417 = (g414 ^ g416);
        long g418 = (g417 ^ 1L);
        long g419 = (g418 ^ 1L);
        long g420 = (g419 ^ 1L);
        long g421 = (g420 & x3_0);
        long g422 = (g419 & x2_0);
        long g423 = (g422 | g421);
        long g424 = (g420 & x3_1);
        long g425 = (g419 & x2_1);
        long g426 = (g425 | g424);
        long g427 = (g420 & x3_2);
        long g428 = (g419 & x2_2);
        long g429 = (g428 | g427);
        long g430 = (g420 & x3_3);
        long g431 = (g419 & x2_3);
        long g432 = (g431 | g430);
        long g433 = (g420 & x3_4);
        long g434 = (g419 & x2_4);
        long g435 = (g434 | g433);
        long g436 = (g420 & x3_5);
        long g437 = (g419 & x2_5);
        long g438 = (g437 | g436);
        long g439 = (g420 & x3_6);
        long g440 = (g419 & x2_6);
        long g441 = (g440 | g439);
        long g442 = (g420 & x3_7);
        long g443 = (g419 & x2_7);
        long g444 = (g443 | g442);
        long g445 = (g420 & x3_8);
        long g446 = (g419 & x2_8);
        long g447 = (g446 | g445);
        long g448 = (g420 & x3_9);
        long g449 = (g419 & x2_9);
        long g450 = (g449 | g448);
        long g451 = (g420 & x3_10);
        long g452 = (g419 & x2_10);
        long g453 = (g452 | g451);
        long g454 = (g420 & x3_11);
        long g455 = (g419 & x2_11);
        long g456 = (g455 | g454);
        long g457 = (g420 & x3_12);
        long g458 = (g419 & x2_12);
        long g459 = (g458 | g457);
        long g460 = (g420 & x3_13);
        long g461 = (g419 & x2_13);
        long g462 = (g461 | g460);
        long g463 = (g420 & x3_14);
        long g464 = (g419 & x2_14);
        long g465 = (g464 | g463);
        long g466 = (g420 & x3_15);
        long g467 = (g419 & x2_15);
        long g468 = (g467 | g466);
        long g469 = (g420 & x3_16);
        long g470 = (g419 & x2_16);
        long g471 = (g470 | g469);
        long g472 = (g420 & x3_17);
        long g473 = (g419 & x2_17);
        long g474 = (g473 | g472);
        long g475 = (g420 & x3_18);
        long g476 = (g419 & x2_18);
        long g477 = (g476 | g475);
        long g478 = (g420 & x3_19);
        long g479 = (g419 & x2_19);
        long g480 = (g479 | g478);
        long g481 = (g420 & x3_20);
        long g482 = (g419 & x2_20);
        long g483 = (g482 | g481);
        long g484 = (g420 & x3_21);
        long g485 = (g419 & x2_21);
        long g486 = (g485 | g484);
        long g487 = (g420 & x3_22);
        long g488 = (g419 & x2_22);
        long g489 = (g488 | g487);
        long g490 = (g420 & x3_23);
        long g491 = (g419 & x2_23);
        long g492 = (g491 | g490);
        long g493 = (g420 & x3_24);
        long g494 = (g419 & x2_24);
        long g495 = (g494 | g493);
        long g496 = (g420 & x3_25);
        long g497 = (g419 & x2_25);
        long g498 = (g497 | g496);
        long g499 = (g420 & x3_26);
        long g500 = (g419 & x2_26);
        long g501 = (g500 | g499);
        long g502 = (g420 & x3_27);
        long g503 = (g419 & x2_27);
        long g504 = (g503 | g502);
        long g505 = (g420 & x3_28);
        long g506 = (g419 & x2_28);
        long g507 = (g506 | g505);
        long g508 = (g420 & x3_29);
        long g509 = (g419 & x2_29);
        long g510 = (g509 | g508);
        long g511 = (g420 & x3_30);
        long g512 = (g419 & x2_30);
        long g513 = (g512 | g511);
        long g514 = (g420 & x3_31);
        long g515 = (g419 & x2_31);
        long g516 = (g515 | g514);
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
        long w32 = cat(w31, g516, 1);
        long w33 = cat(w32, g513, 1);
        long w34 = cat(w33, g510, 1);
        long w35 = cat(w34, g507, 1);
        long w36 = cat(w35, g504, 1);
        long w37 = cat(w36, g501, 1);
        long w38 = cat(w37, g498, 1);
        long w39 = cat(w38, g495, 1);
        long w40 = cat(w39, g492, 1);
        long w41 = cat(w40, g489, 1);
        long w42 = cat(w41, g486, 1);
        long w43 = cat(w42, g483, 1);
        long w44 = cat(w43, g480, 1);
        long w45 = cat(w44, g477, 1);
        long w46 = cat(w45, g474, 1);
        long w47 = cat(w46, g471, 1);
        long w48 = cat(w47, g468, 1);
        long w49 = cat(w48, g465, 1);
        long w50 = cat(w49, g462, 1);
        long w51 = cat(w50, g459, 1);
        long w52 = cat(w51, g456, 1);
        long w53 = cat(w52, g453, 1);
        long w54 = cat(w53, g450, 1);
        long w55 = cat(w54, g447, 1);
        long w56 = cat(w55, g444, 1);
        long w57 = cat(w56, g441, 1);
        long w58 = cat(w57, g438, 1);
        long w59 = cat(w58, g435, 1);
        long w60 = cat(w59, g432, 1);
        long w61 = cat(w60, g429, 1);
        long w62 = cat(w61, g426, 1);
        long w63 = cat(w62, g423, 1);
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
                    answers.append(Long.toUnsignedString(emu_cmovl_gpr_gpr_32__reg_rdi__java(values[0], values[1], values[2], values[3])));
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
