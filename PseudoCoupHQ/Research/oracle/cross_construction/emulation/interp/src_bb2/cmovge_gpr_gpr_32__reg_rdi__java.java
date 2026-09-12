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
    // one named local per gate, over the term of cmovge_gpr_gpr_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(Extract(31, 31, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1)) == If(Extract(31, 31, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))) == Extract(32, 32, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))), 0, 1), Extract(31, 0, v2), Extract(31, 0, v3)))
    static long emu_cmovge_gpr_gpr_32__reg_rdi__java(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
        long x0_31 = ext(b, 31, 31);
        long x0_0 = ext(b, 0, 0);
        long x0_1 = ext(b, 1, 1);
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
        long x1_31 = ext(a, 31, 31);
        long x1_20 = ext(a, 20, 20);
        long x1_19 = ext(a, 19, 19);
        long x1_17 = ext(a, 17, 17);
        long x1_7 = ext(a, 7, 7);
        long x1_5 = ext(a, 5, 5);
        long x1_2 = ext(a, 2, 2);
        long x1_0 = ext(a, 0, 0);
        long x1_1 = ext(a, 1, 1);
        long x1_3 = ext(a, 3, 3);
        long x1_4 = ext(a, 4, 4);
        long x1_6 = ext(a, 6, 6);
        long x1_8 = ext(a, 8, 8);
        long x1_9 = ext(a, 9, 9);
        long x1_10 = ext(a, 10, 10);
        long x1_11 = ext(a, 11, 11);
        long x1_12 = ext(a, 12, 12);
        long x1_13 = ext(a, 13, 13);
        long x1_14 = ext(a, 14, 14);
        long x1_15 = ext(a, 15, 15);
        long x1_16 = ext(a, 16, 16);
        long x1_18 = ext(a, 18, 18);
        long x1_21 = ext(a, 21, 21);
        long x1_22 = ext(a, 22, 22);
        long x1_23 = ext(a, 23, 23);
        long x1_24 = ext(a, 24, 24);
        long x1_25 = ext(a, 25, 25);
        long x1_26 = ext(a, 26, 26);
        long x1_27 = ext(a, 27, 27);
        long x1_28 = ext(a, 28, 28);
        long x1_29 = ext(a, 29, 29);
        long x1_30 = ext(a, 30, 30);
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
        long g0 = (x0_1 | x0_0);
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
        long g33 = (x1_31 ^ 1L);
        long g34 = (g29 ^ x0_31);
        long g35 = (g34 ^ 1L);
        long g36 = (g35 | g33);
        long g37 = (g36 ^ 1L);
        long g38 = (g27 ^ x0_29);
        long g39 = (g38 ^ 1L);
        long g40 = (g24 ^ x0_26);
        long g41 = (g40 ^ 1L);
        long g42 = (g23 ^ x0_25);
        long g43 = (g42 ^ 1L);
        long g44 = (g18 ^ x0_20);
        long g45 = (g44 ^ 1L);
        long g46 = (x1_20 ^ 1L);
        long g47 = (g46 | g45);
        long g48 = (g47 ^ 1L);
        long g49 = (x1_19 ^ 1L);
        long g50 = (g17 ^ x0_19);
        long g51 = (g50 ^ 1L);
        long g52 = (g51 | g49);
        long g53 = (g52 ^ 1L);
        long g54 = (x1_17 ^ 1L);
        long g55 = (g15 ^ x0_17);
        long g56 = (g55 ^ 1L);
        long g57 = (g56 | g54);
        long g58 = (g57 ^ 1L);
        long g59 = (x1_7 ^ 1L);
        long g60 = (g5 ^ x0_7);
        long g61 = (g60 ^ 1L);
        long g62 = (g61 | g59);
        long g63 = (g62 ^ 1L);
        long g64 = (g4 ^ x0_6);
        long g65 = (g64 ^ 1L);
        long g66 = (x1_5 ^ 1L);
        long g67 = (g3 ^ x0_5);
        long g68 = (g67 ^ 1L);
        long g69 = (g68 | g66);
        long g70 = (g69 ^ 1L);
        long g71 = (g2 ^ x0_4);
        long g72 = (g71 ^ 1L);
        long g73 = (x1_2 ^ 1L);
        long g74 = (g0 ^ x0_2);
        long g75 = (g74 ^ 1L);
        long g76 = (g75 | g73);
        long g77 = (g76 ^ 1L);
        long g78 = (x1_0 ^ 1L);
        long g79 = (x0_0 ^ 1L);
        long g80 = (g79 | g78);
        long g81 = (x1_1 ^ 1L);
        long g82 = (g81 | g80);
        long g83 = (g82 ^ 1L);
        long g84 = (x0_0 ^ x0_1);
        long g85 = (g84 ^ 1L);
        long g86 = (g81 | g85);
        long g87 = (g86 ^ 1L);
        long g88 = (g85 | g80);
        long g89 = (g88 ^ 1L);
        long g90 = (g89 | g87);
        long g91 = (g90 | g83);
        long g92 = (g91 ^ 1L);
        long g93 = (g92 | g75);
        long g94 = (g93 ^ 1L);
        long g95 = (g73 | g92);
        long g96 = (g95 ^ 1L);
        long g97 = (g96 | g94);
        long g98 = (g97 | g77);
        long g99 = (g98 ^ 1L);
        long g100 = (x1_3 ^ 1L);
        long g101 = (g100 | g99);
        long g102 = (g101 ^ 1L);
        long g103 = (g1 ^ x0_3);
        long g104 = (g103 ^ 1L);
        long g105 = (g104 | g99);
        long g106 = (g105 ^ 1L);
        long g107 = (g104 | g100);
        long g108 = (g107 ^ 1L);
        long g109 = (g108 | g106);
        long g110 = (g109 | g102);
        long g111 = (g110 ^ 1L);
        long g112 = (g111 | g72);
        long g113 = (g112 ^ 1L);
        long g114 = (x1_4 ^ 1L);
        long g115 = (g114 | g111);
        long g116 = (g115 ^ 1L);
        long g117 = (g72 | g114);
        long g118 = (g117 ^ 1L);
        long g119 = (g118 | g116);
        long g120 = (g119 | g113);
        long g121 = (g120 ^ 1L);
        long g122 = (g121 | g68);
        long g123 = (g122 ^ 1L);
        long g124 = (g66 | g121);
        long g125 = (g124 ^ 1L);
        long g126 = (g125 | g123);
        long g127 = (g126 | g70);
        long g128 = (g127 ^ 1L);
        long g129 = (g128 | g65);
        long g130 = (g129 ^ 1L);
        long g131 = (x1_6 ^ 1L);
        long g132 = (g65 | g131);
        long g133 = (g132 ^ 1L);
        long g134 = (g131 | g128);
        long g135 = (g134 ^ 1L);
        long g136 = (g135 | g133);
        long g137 = (g136 | g130);
        long g138 = (g137 ^ 1L);
        long g139 = (g61 | g138);
        long g140 = (g139 ^ 1L);
        long g141 = (g59 | g138);
        long g142 = (g141 ^ 1L);
        long g143 = (g142 | g140);
        long g144 = (g143 | g63);
        long g145 = (g144 ^ 1L);
        long g146 = (x1_8 ^ 1L);
        long g147 = (g146 | g145);
        long g148 = (g147 ^ 1L);
        long g149 = (g6 ^ x0_8);
        long g150 = (g149 ^ 1L);
        long g151 = (g150 | g146);
        long g152 = (g151 ^ 1L);
        long g153 = (g150 | g145);
        long g154 = (g153 ^ 1L);
        long g155 = (g154 | g152);
        long g156 = (g155 | g148);
        long g157 = (g156 ^ 1L);
        long g158 = (x1_9 ^ 1L);
        long g159 = (g158 | g157);
        long g160 = (g159 ^ 1L);
        long g161 = (g7 ^ x0_9);
        long g162 = (g161 ^ 1L);
        long g163 = (g162 | g157);
        long g164 = (g163 ^ 1L);
        long g165 = (g162 | g158);
        long g166 = (g165 ^ 1L);
        long g167 = (g166 | g164);
        long g168 = (g167 | g160);
        long g169 = (g168 ^ 1L);
        long g170 = (x1_10 ^ 1L);
        long g171 = (g170 | g169);
        long g172 = (g171 ^ 1L);
        long g173 = (g8 ^ x0_10);
        long g174 = (g173 ^ 1L);
        long g175 = (g174 | g169);
        long g176 = (g175 ^ 1L);
        long g177 = (g170 | g174);
        long g178 = (g177 ^ 1L);
        long g179 = (g178 | g176);
        long g180 = (g179 | g172);
        long g181 = (g180 ^ 1L);
        long g182 = (x1_11 ^ 1L);
        long g183 = (g182 | g181);
        long g184 = (g183 ^ 1L);
        long g185 = (g9 ^ x0_11);
        long g186 = (g185 ^ 1L);
        long g187 = (g186 | g182);
        long g188 = (g187 ^ 1L);
        long g189 = (g186 | g181);
        long g190 = (g189 ^ 1L);
        long g191 = (g190 | g188);
        long g192 = (g191 | g184);
        long g193 = (g192 ^ 1L);
        long g194 = (x1_12 ^ 1L);
        long g195 = (g194 | g193);
        long g196 = (g195 ^ 1L);
        long g197 = (g10 ^ x0_12);
        long g198 = (g197 ^ 1L);
        long g199 = (g193 | g198);
        long g200 = (g199 ^ 1L);
        long g201 = (g194 | g198);
        long g202 = (g201 ^ 1L);
        long g203 = (g202 | g200);
        long g204 = (g203 | g196);
        long g205 = (g204 ^ 1L);
        long g206 = (x1_13 ^ 1L);
        long g207 = (g206 | g205);
        long g208 = (g207 ^ 1L);
        long g209 = (g11 ^ x0_13);
        long g210 = (g209 ^ 1L);
        long g211 = (g210 | g206);
        long g212 = (g211 ^ 1L);
        long g213 = (g205 | g210);
        long g214 = (g213 ^ 1L);
        long g215 = (g214 | g212);
        long g216 = (g215 | g208);
        long g217 = (g216 ^ 1L);
        long g218 = (x1_14 ^ 1L);
        long g219 = (g218 | g217);
        long g220 = (g219 ^ 1L);
        long g221 = (g12 ^ x0_14);
        long g222 = (g221 ^ 1L);
        long g223 = (g222 | g217);
        long g224 = (g223 ^ 1L);
        long g225 = (g222 | g218);
        long g226 = (g225 ^ 1L);
        long g227 = (g226 | g224);
        long g228 = (g227 | g220);
        long g229 = (g228 ^ 1L);
        long g230 = (g13 ^ x0_15);
        long g231 = (g230 ^ 1L);
        long g232 = (g231 | g229);
        long g233 = (g232 ^ 1L);
        long g234 = (x1_15 ^ 1L);
        long g235 = (g231 | g234);
        long g236 = (g235 ^ 1L);
        long g237 = (g234 | g229);
        long g238 = (g237 ^ 1L);
        long g239 = (g238 | g236);
        long g240 = (g239 | g233);
        long g241 = (g240 ^ 1L);
        long g242 = (x1_16 ^ 1L);
        long g243 = (g242 | g241);
        long g244 = (g243 ^ 1L);
        long g245 = (g14 ^ x0_16);
        long g246 = (g245 ^ 1L);
        long g247 = (g242 | g246);
        long g248 = (g247 ^ 1L);
        long g249 = (g241 | g246);
        long g250 = (g249 ^ 1L);
        long g251 = (g250 | g248);
        long g252 = (g251 | g244);
        long g253 = (g252 ^ 1L);
        long g254 = (g54 | g253);
        long g255 = (g254 ^ 1L);
        long g256 = (g56 | g253);
        long g257 = (g256 ^ 1L);
        long g258 = (g257 | g255);
        long g259 = (g258 | g58);
        long g260 = (g259 ^ 1L);
        long g261 = (g16 ^ x0_18);
        long g262 = (g261 ^ 1L);
        long g263 = (g262 | g260);
        long g264 = (g263 ^ 1L);
        long g265 = (x1_18 ^ 1L);
        long g266 = (g265 | g262);
        long g267 = (g266 ^ 1L);
        long g268 = (g265 | g260);
        long g269 = (g268 ^ 1L);
        long g270 = (g269 | g267);
        long g271 = (g270 | g264);
        long g272 = (g271 ^ 1L);
        long g273 = (g51 | g272);
        long g274 = (g273 ^ 1L);
        long g275 = (g49 | g272);
        long g276 = (g275 ^ 1L);
        long g277 = (g276 | g274);
        long g278 = (g277 | g53);
        long g279 = (g278 ^ 1L);
        long g280 = (g46 | g279);
        long g281 = (g280 ^ 1L);
        long g282 = (g45 | g279);
        long g283 = (g282 ^ 1L);
        long g284 = (g283 | g281);
        long g285 = (g284 | g48);
        long g286 = (g285 ^ 1L);
        long g287 = (g19 ^ x0_21);
        long g288 = (g287 ^ 1L);
        long g289 = (g288 | g286);
        long g290 = (g289 ^ 1L);
        long g291 = (x1_21 ^ 1L);
        long g292 = (g291 | g288);
        long g293 = (g292 ^ 1L);
        long g294 = (g291 | g286);
        long g295 = (g294 ^ 1L);
        long g296 = (g295 | g293);
        long g297 = (g296 | g290);
        long g298 = (g297 ^ 1L);
        long g299 = (x1_22 ^ 1L);
        long g300 = (g299 | g298);
        long g301 = (g300 ^ 1L);
        long g302 = (g20 ^ x0_22);
        long g303 = (g302 ^ 1L);
        long g304 = (g303 | g298);
        long g305 = (g304 ^ 1L);
        long g306 = (g299 | g303);
        long g307 = (g306 ^ 1L);
        long g308 = (g307 | g305);
        long g309 = (g308 | g301);
        long g310 = (g309 ^ 1L);
        long g311 = (x1_23 ^ 1L);
        long g312 = (g311 | g310);
        long g313 = (g312 ^ 1L);
        long g314 = (g21 ^ x0_23);
        long g315 = (g314 ^ 1L);
        long g316 = (g310 | g315);
        long g317 = (g316 ^ 1L);
        long g318 = (g311 | g315);
        long g319 = (g318 ^ 1L);
        long g320 = (g319 | g317);
        long g321 = (g320 | g313);
        long g322 = (g321 ^ 1L);
        long g323 = (x1_24 ^ 1L);
        long g324 = (g323 | g322);
        long g325 = (g324 ^ 1L);
        long g326 = (g22 ^ x0_24);
        long g327 = (g326 ^ 1L);
        long g328 = (g327 | g323);
        long g329 = (g328 ^ 1L);
        long g330 = (g327 | g322);
        long g331 = (g330 ^ 1L);
        long g332 = (g331 | g329);
        long g333 = (g332 | g325);
        long g334 = (g333 ^ 1L);
        long g335 = (g334 | g43);
        long g336 = (g335 ^ 1L);
        long g337 = (x1_25 ^ 1L);
        long g338 = (g337 | g43);
        long g339 = (g338 ^ 1L);
        long g340 = (g337 | g334);
        long g341 = (g340 ^ 1L);
        long g342 = (g341 | g339);
        long g343 = (g342 | g336);
        long g344 = (g343 ^ 1L);
        long g345 = (g344 | g41);
        long g346 = (g345 ^ 1L);
        long g347 = (x1_26 ^ 1L);
        long g348 = (g347 | g344);
        long g349 = (g348 ^ 1L);
        long g350 = (g41 | g347);
        long g351 = (g350 ^ 1L);
        long g352 = (g351 | g349);
        long g353 = (g352 | g346);
        long g354 = (g353 ^ 1L);
        long g355 = (g25 ^ x0_27);
        long g356 = (g355 ^ 1L);
        long g357 = (g356 | g354);
        long g358 = (g357 ^ 1L);
        long g359 = (x1_27 ^ 1L);
        long g360 = (g359 | g354);
        long g361 = (g360 ^ 1L);
        long g362 = (g359 | g356);
        long g363 = (g362 ^ 1L);
        long g364 = (g363 | g361);
        long g365 = (g364 | g358);
        long g366 = (g365 ^ 1L);
        long g367 = (g26 ^ x0_28);
        long g368 = (g367 ^ 1L);
        long g369 = (g368 | g366);
        long g370 = (g369 ^ 1L);
        long g371 = (x1_28 ^ 1L);
        long g372 = (g371 | g366);
        long g373 = (g372 ^ 1L);
        long g374 = (g371 | g368);
        long g375 = (g374 ^ 1L);
        long g376 = (g375 | g373);
        long g377 = (g376 | g370);
        long g378 = (g377 ^ 1L);
        long g379 = (g378 | g39);
        long g380 = (g379 ^ 1L);
        long g381 = (x1_29 ^ 1L);
        long g382 = (g381 | g378);
        long g383 = (g382 ^ 1L);
        long g384 = (g381 | g39);
        long g385 = (g384 ^ 1L);
        long g386 = (g385 | g383);
        long g387 = (g386 | g380);
        long g388 = (g387 ^ 1L);
        long g389 = (g28 ^ x0_30);
        long g390 = (g389 ^ 1L);
        long g391 = (g390 | g388);
        long g392 = (g391 ^ 1L);
        long g393 = (x1_30 ^ 1L);
        long g394 = (g393 | g388);
        long g395 = (g394 ^ 1L);
        long g396 = (g390 | g393);
        long g397 = (g396 ^ 1L);
        long g398 = (g397 | g395);
        long g399 = (g398 | g392);
        long g400 = (g399 ^ 1L);
        long g401 = (g33 | g400);
        long g402 = (g401 ^ 1L);
        long g403 = (g35 | g400);
        long g404 = (g403 ^ 1L);
        long g405 = (g404 | g402);
        long g406 = (g405 | g37);
        long g407 = (x1_31 ^ g406);
        long g408 = (g407 ^ 1L);
        long g409 = (g408 ^ g32);
        long g410 = (g409 ^ 1L);
        long g411 = (x1_31 ^ g399);
        long g412 = (g411 ^ 1L);
        long g413 = (g412 ^ g35);
        long g414 = (g413 ^ 1L);
        long g415 = (g414 ^ g410);
        long g416 = (g415 ^ 1L);
        long g417 = (g414 ^ g416);
        long g418 = (g417 ^ 1L);
        long g419 = (g418 ^ 1L);
        long g420 = (g419 & x3_0);
        long g421 = (g418 & x2_0);
        long g422 = (g421 | g420);
        long g423 = (g419 & x3_1);
        long g424 = (g418 & x2_1);
        long g425 = (g424 | g423);
        long g426 = (g419 & x3_2);
        long g427 = (g418 & x2_2);
        long g428 = (g427 | g426);
        long g429 = (g419 & x3_3);
        long g430 = (g418 & x2_3);
        long g431 = (g430 | g429);
        long g432 = (g419 & x3_4);
        long g433 = (g418 & x2_4);
        long g434 = (g433 | g432);
        long g435 = (g419 & x3_5);
        long g436 = (g418 & x2_5);
        long g437 = (g436 | g435);
        long g438 = (g419 & x3_6);
        long g439 = (g418 & x2_6);
        long g440 = (g439 | g438);
        long g441 = (g419 & x3_7);
        long g442 = (g418 & x2_7);
        long g443 = (g442 | g441);
        long g444 = (g419 & x3_8);
        long g445 = (g418 & x2_8);
        long g446 = (g445 | g444);
        long g447 = (g419 & x3_9);
        long g448 = (g418 & x2_9);
        long g449 = (g448 | g447);
        long g450 = (g419 & x3_10);
        long g451 = (g418 & x2_10);
        long g452 = (g451 | g450);
        long g453 = (g419 & x3_11);
        long g454 = (g418 & x2_11);
        long g455 = (g454 | g453);
        long g456 = (g419 & x3_12);
        long g457 = (g418 & x2_12);
        long g458 = (g457 | g456);
        long g459 = (g419 & x3_13);
        long g460 = (g418 & x2_13);
        long g461 = (g460 | g459);
        long g462 = (g419 & x3_14);
        long g463 = (g418 & x2_14);
        long g464 = (g463 | g462);
        long g465 = (g419 & x3_15);
        long g466 = (g418 & x2_15);
        long g467 = (g466 | g465);
        long g468 = (g419 & x3_16);
        long g469 = (g418 & x2_16);
        long g470 = (g469 | g468);
        long g471 = (g419 & x3_17);
        long g472 = (g418 & x2_17);
        long g473 = (g472 | g471);
        long g474 = (g419 & x3_18);
        long g475 = (g418 & x2_18);
        long g476 = (g475 | g474);
        long g477 = (g419 & x3_19);
        long g478 = (g418 & x2_19);
        long g479 = (g478 | g477);
        long g480 = (g419 & x3_20);
        long g481 = (g418 & x2_20);
        long g482 = (g481 | g480);
        long g483 = (g419 & x3_21);
        long g484 = (g418 & x2_21);
        long g485 = (g484 | g483);
        long g486 = (g419 & x3_22);
        long g487 = (g418 & x2_22);
        long g488 = (g487 | g486);
        long g489 = (g419 & x3_23);
        long g490 = (g418 & x2_23);
        long g491 = (g490 | g489);
        long g492 = (g419 & x3_24);
        long g493 = (g418 & x2_24);
        long g494 = (g493 | g492);
        long g495 = (g419 & x3_25);
        long g496 = (g418 & x2_25);
        long g497 = (g496 | g495);
        long g498 = (g419 & x3_26);
        long g499 = (g418 & x2_26);
        long g500 = (g499 | g498);
        long g501 = (g419 & x3_27);
        long g502 = (g418 & x2_27);
        long g503 = (g502 | g501);
        long g504 = (g419 & x3_28);
        long g505 = (g418 & x2_28);
        long g506 = (g505 | g504);
        long g507 = (g419 & x3_29);
        long g508 = (g418 & x2_29);
        long g509 = (g508 | g507);
        long g510 = (g419 & x3_30);
        long g511 = (g418 & x2_30);
        long g512 = (g511 | g510);
        long g513 = (g419 & x3_31);
        long g514 = (g418 & x2_31);
        long g515 = (g514 | g513);
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
        long w32 = cat(w31, g515, 1);
        long w33 = cat(w32, g512, 1);
        long w34 = cat(w33, g509, 1);
        long w35 = cat(w34, g506, 1);
        long w36 = cat(w35, g503, 1);
        long w37 = cat(w36, g500, 1);
        long w38 = cat(w37, g497, 1);
        long w39 = cat(w38, g494, 1);
        long w40 = cat(w39, g491, 1);
        long w41 = cat(w40, g488, 1);
        long w42 = cat(w41, g485, 1);
        long w43 = cat(w42, g482, 1);
        long w44 = cat(w43, g479, 1);
        long w45 = cat(w44, g476, 1);
        long w46 = cat(w45, g473, 1);
        long w47 = cat(w46, g470, 1);
        long w48 = cat(w47, g467, 1);
        long w49 = cat(w48, g464, 1);
        long w50 = cat(w49, g461, 1);
        long w51 = cat(w50, g458, 1);
        long w52 = cat(w51, g455, 1);
        long w53 = cat(w52, g452, 1);
        long w54 = cat(w53, g449, 1);
        long w55 = cat(w54, g446, 1);
        long w56 = cat(w55, g443, 1);
        long w57 = cat(w56, g440, 1);
        long w58 = cat(w57, g437, 1);
        long w59 = cat(w58, g434, 1);
        long w60 = cat(w59, g431, 1);
        long w61 = cat(w60, g428, 1);
        long w62 = cat(w61, g425, 1);
        long w63 = cat(w62, g422, 1);
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
                    answers.append(Long.toUnsignedString(emu_cmovge_gpr_gpr_32__reg_rdi__java(values[0], values[1], values[2], values[3])));
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
