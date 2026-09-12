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
    // one named local per gate, over the term of pxor_xmm_xmm_128__reg_xmm0_low__java.
    // The term's layer-5 text, LITERAL:
    //   Extract(63, 0, v0) ^ Extract(63, 0, v1)
    static long emu_pxor_xmm_xmm_128__reg_xmm0_low__java(long a, long b) {
        long x1_0 = ext(b, 0, 0);
        long x0_0 = ext(a, 0, 0);
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
        long x1_32 = ext(b, 32, 32);
        long x0_32 = ext(a, 32, 32);
        long x1_33 = ext(b, 33, 33);
        long x0_33 = ext(a, 33, 33);
        long x1_34 = ext(b, 34, 34);
        long x0_34 = ext(a, 34, 34);
        long x1_35 = ext(b, 35, 35);
        long x0_35 = ext(a, 35, 35);
        long x1_36 = ext(b, 36, 36);
        long x0_36 = ext(a, 36, 36);
        long x1_37 = ext(b, 37, 37);
        long x0_37 = ext(a, 37, 37);
        long x1_38 = ext(b, 38, 38);
        long x0_38 = ext(a, 38, 38);
        long x1_39 = ext(b, 39, 39);
        long x0_39 = ext(a, 39, 39);
        long x1_40 = ext(b, 40, 40);
        long x0_40 = ext(a, 40, 40);
        long x1_41 = ext(b, 41, 41);
        long x0_41 = ext(a, 41, 41);
        long x1_42 = ext(b, 42, 42);
        long x0_42 = ext(a, 42, 42);
        long x1_43 = ext(b, 43, 43);
        long x0_43 = ext(a, 43, 43);
        long x1_44 = ext(b, 44, 44);
        long x0_44 = ext(a, 44, 44);
        long x1_45 = ext(b, 45, 45);
        long x0_45 = ext(a, 45, 45);
        long x1_46 = ext(b, 46, 46);
        long x0_46 = ext(a, 46, 46);
        long x1_47 = ext(b, 47, 47);
        long x0_47 = ext(a, 47, 47);
        long x1_48 = ext(b, 48, 48);
        long x0_48 = ext(a, 48, 48);
        long x1_49 = ext(b, 49, 49);
        long x0_49 = ext(a, 49, 49);
        long x1_50 = ext(b, 50, 50);
        long x0_50 = ext(a, 50, 50);
        long x1_51 = ext(b, 51, 51);
        long x0_51 = ext(a, 51, 51);
        long x1_52 = ext(b, 52, 52);
        long x0_52 = ext(a, 52, 52);
        long x1_53 = ext(b, 53, 53);
        long x0_53 = ext(a, 53, 53);
        long x1_54 = ext(b, 54, 54);
        long x0_54 = ext(a, 54, 54);
        long x1_55 = ext(b, 55, 55);
        long x0_55 = ext(a, 55, 55);
        long x1_56 = ext(b, 56, 56);
        long x0_56 = ext(a, 56, 56);
        long x1_57 = ext(b, 57, 57);
        long x0_57 = ext(a, 57, 57);
        long x1_58 = ext(b, 58, 58);
        long x0_58 = ext(a, 58, 58);
        long x1_59 = ext(b, 59, 59);
        long x0_59 = ext(a, 59, 59);
        long x1_60 = ext(b, 60, 60);
        long x0_60 = ext(a, 60, 60);
        long x1_61 = ext(b, 61, 61);
        long x0_61 = ext(a, 61, 61);
        long x1_62 = ext(b, 62, 62);
        long x0_62 = ext(a, 62, 62);
        long x1_63 = ext(b, 63, 63);
        long x0_63 = ext(a, 63, 63);
        long g0 = (x0_0 ^ x1_0);
        long g1 = (g0 ^ 1L);
        long g2 = (g1 ^ 1L);
        long g3 = (x0_1 ^ x1_1);
        long g4 = (g3 ^ 1L);
        long g5 = (g4 ^ 1L);
        long g6 = (x0_2 ^ x1_2);
        long g7 = (g6 ^ 1L);
        long g8 = (g7 ^ 1L);
        long g9 = (x0_3 ^ x1_3);
        long g10 = (g9 ^ 1L);
        long g11 = (g10 ^ 1L);
        long g12 = (x0_4 ^ x1_4);
        long g13 = (g12 ^ 1L);
        long g14 = (g13 ^ 1L);
        long g15 = (x0_5 ^ x1_5);
        long g16 = (g15 ^ 1L);
        long g17 = (g16 ^ 1L);
        long g18 = (x0_6 ^ x1_6);
        long g19 = (g18 ^ 1L);
        long g20 = (g19 ^ 1L);
        long g21 = (x0_7 ^ x1_7);
        long g22 = (g21 ^ 1L);
        long g23 = (g22 ^ 1L);
        long g24 = (x0_8 ^ x1_8);
        long g25 = (g24 ^ 1L);
        long g26 = (g25 ^ 1L);
        long g27 = (x0_9 ^ x1_9);
        long g28 = (g27 ^ 1L);
        long g29 = (g28 ^ 1L);
        long g30 = (x0_10 ^ x1_10);
        long g31 = (g30 ^ 1L);
        long g32 = (g31 ^ 1L);
        long g33 = (x0_11 ^ x1_11);
        long g34 = (g33 ^ 1L);
        long g35 = (g34 ^ 1L);
        long g36 = (x0_12 ^ x1_12);
        long g37 = (g36 ^ 1L);
        long g38 = (g37 ^ 1L);
        long g39 = (x0_13 ^ x1_13);
        long g40 = (g39 ^ 1L);
        long g41 = (g40 ^ 1L);
        long g42 = (x0_14 ^ x1_14);
        long g43 = (g42 ^ 1L);
        long g44 = (g43 ^ 1L);
        long g45 = (x0_15 ^ x1_15);
        long g46 = (g45 ^ 1L);
        long g47 = (g46 ^ 1L);
        long g48 = (x0_16 ^ x1_16);
        long g49 = (g48 ^ 1L);
        long g50 = (g49 ^ 1L);
        long g51 = (x0_17 ^ x1_17);
        long g52 = (g51 ^ 1L);
        long g53 = (g52 ^ 1L);
        long g54 = (x0_18 ^ x1_18);
        long g55 = (g54 ^ 1L);
        long g56 = (g55 ^ 1L);
        long g57 = (x0_19 ^ x1_19);
        long g58 = (g57 ^ 1L);
        long g59 = (g58 ^ 1L);
        long g60 = (x0_20 ^ x1_20);
        long g61 = (g60 ^ 1L);
        long g62 = (g61 ^ 1L);
        long g63 = (x0_21 ^ x1_21);
        long g64 = (g63 ^ 1L);
        long g65 = (g64 ^ 1L);
        long g66 = (x0_22 ^ x1_22);
        long g67 = (g66 ^ 1L);
        long g68 = (g67 ^ 1L);
        long g69 = (x0_23 ^ x1_23);
        long g70 = (g69 ^ 1L);
        long g71 = (g70 ^ 1L);
        long g72 = (x0_24 ^ x1_24);
        long g73 = (g72 ^ 1L);
        long g74 = (g73 ^ 1L);
        long g75 = (x0_25 ^ x1_25);
        long g76 = (g75 ^ 1L);
        long g77 = (g76 ^ 1L);
        long g78 = (x0_26 ^ x1_26);
        long g79 = (g78 ^ 1L);
        long g80 = (g79 ^ 1L);
        long g81 = (x0_27 ^ x1_27);
        long g82 = (g81 ^ 1L);
        long g83 = (g82 ^ 1L);
        long g84 = (x0_28 ^ x1_28);
        long g85 = (g84 ^ 1L);
        long g86 = (g85 ^ 1L);
        long g87 = (x0_29 ^ x1_29);
        long g88 = (g87 ^ 1L);
        long g89 = (g88 ^ 1L);
        long g90 = (x0_30 ^ x1_30);
        long g91 = (g90 ^ 1L);
        long g92 = (g91 ^ 1L);
        long g93 = (x0_31 ^ x1_31);
        long g94 = (g93 ^ 1L);
        long g95 = (g94 ^ 1L);
        long g96 = (x0_32 ^ x1_32);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ 1L);
        long g99 = (x0_33 ^ x1_33);
        long g100 = (g99 ^ 1L);
        long g101 = (g100 ^ 1L);
        long g102 = (x0_34 ^ x1_34);
        long g103 = (g102 ^ 1L);
        long g104 = (g103 ^ 1L);
        long g105 = (x0_35 ^ x1_35);
        long g106 = (g105 ^ 1L);
        long g107 = (g106 ^ 1L);
        long g108 = (x0_36 ^ x1_36);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 ^ 1L);
        long g111 = (x0_37 ^ x1_37);
        long g112 = (g111 ^ 1L);
        long g113 = (g112 ^ 1L);
        long g114 = (x0_38 ^ x1_38);
        long g115 = (g114 ^ 1L);
        long g116 = (g115 ^ 1L);
        long g117 = (x0_39 ^ x1_39);
        long g118 = (g117 ^ 1L);
        long g119 = (g118 ^ 1L);
        long g120 = (x0_40 ^ x1_40);
        long g121 = (g120 ^ 1L);
        long g122 = (g121 ^ 1L);
        long g123 = (x0_41 ^ x1_41);
        long g124 = (g123 ^ 1L);
        long g125 = (g124 ^ 1L);
        long g126 = (x0_42 ^ x1_42);
        long g127 = (g126 ^ 1L);
        long g128 = (g127 ^ 1L);
        long g129 = (x0_43 ^ x1_43);
        long g130 = (g129 ^ 1L);
        long g131 = (g130 ^ 1L);
        long g132 = (x0_44 ^ x1_44);
        long g133 = (g132 ^ 1L);
        long g134 = (g133 ^ 1L);
        long g135 = (x0_45 ^ x1_45);
        long g136 = (g135 ^ 1L);
        long g137 = (g136 ^ 1L);
        long g138 = (x0_46 ^ x1_46);
        long g139 = (g138 ^ 1L);
        long g140 = (g139 ^ 1L);
        long g141 = (x0_47 ^ x1_47);
        long g142 = (g141 ^ 1L);
        long g143 = (g142 ^ 1L);
        long g144 = (x0_48 ^ x1_48);
        long g145 = (g144 ^ 1L);
        long g146 = (g145 ^ 1L);
        long g147 = (x0_49 ^ x1_49);
        long g148 = (g147 ^ 1L);
        long g149 = (g148 ^ 1L);
        long g150 = (x0_50 ^ x1_50);
        long g151 = (g150 ^ 1L);
        long g152 = (g151 ^ 1L);
        long g153 = (x0_51 ^ x1_51);
        long g154 = (g153 ^ 1L);
        long g155 = (g154 ^ 1L);
        long g156 = (x0_52 ^ x1_52);
        long g157 = (g156 ^ 1L);
        long g158 = (g157 ^ 1L);
        long g159 = (x0_53 ^ x1_53);
        long g160 = (g159 ^ 1L);
        long g161 = (g160 ^ 1L);
        long g162 = (x0_54 ^ x1_54);
        long g163 = (g162 ^ 1L);
        long g164 = (g163 ^ 1L);
        long g165 = (x0_55 ^ x1_55);
        long g166 = (g165 ^ 1L);
        long g167 = (g166 ^ 1L);
        long g168 = (x0_56 ^ x1_56);
        long g169 = (g168 ^ 1L);
        long g170 = (g169 ^ 1L);
        long g171 = (x0_57 ^ x1_57);
        long g172 = (g171 ^ 1L);
        long g173 = (g172 ^ 1L);
        long g174 = (x0_58 ^ x1_58);
        long g175 = (g174 ^ 1L);
        long g176 = (g175 ^ 1L);
        long g177 = (x0_59 ^ x1_59);
        long g178 = (g177 ^ 1L);
        long g179 = (g178 ^ 1L);
        long g180 = (x0_60 ^ x1_60);
        long g181 = (g180 ^ 1L);
        long g182 = (g181 ^ 1L);
        long g183 = (x0_61 ^ x1_61);
        long g184 = (g183 ^ 1L);
        long g185 = (g184 ^ 1L);
        long g186 = (x0_62 ^ x1_62);
        long g187 = (g186 ^ 1L);
        long g188 = (g187 ^ 1L);
        long g189 = (x0_63 ^ x1_63);
        long g190 = (g189 ^ 1L);
        long g191 = (g190 ^ 1L);
        long w0 = g191;
        long w1 = cat(w0, g188, 1);
        long w2 = cat(w1, g185, 1);
        long w3 = cat(w2, g182, 1);
        long w4 = cat(w3, g179, 1);
        long w5 = cat(w4, g176, 1);
        long w6 = cat(w5, g173, 1);
        long w7 = cat(w6, g170, 1);
        long w8 = cat(w7, g167, 1);
        long w9 = cat(w8, g164, 1);
        long w10 = cat(w9, g161, 1);
        long w11 = cat(w10, g158, 1);
        long w12 = cat(w11, g155, 1);
        long w13 = cat(w12, g152, 1);
        long w14 = cat(w13, g149, 1);
        long w15 = cat(w14, g146, 1);
        long w16 = cat(w15, g143, 1);
        long w17 = cat(w16, g140, 1);
        long w18 = cat(w17, g137, 1);
        long w19 = cat(w18, g134, 1);
        long w20 = cat(w19, g131, 1);
        long w21 = cat(w20, g128, 1);
        long w22 = cat(w21, g125, 1);
        long w23 = cat(w22, g122, 1);
        long w24 = cat(w23, g119, 1);
        long w25 = cat(w24, g116, 1);
        long w26 = cat(w25, g113, 1);
        long w27 = cat(w26, g110, 1);
        long w28 = cat(w27, g107, 1);
        long w29 = cat(w28, g104, 1);
        long w30 = cat(w29, g101, 1);
        long w31 = cat(w30, g98, 1);
        long w32 = cat(w31, g95, 1);
        long w33 = cat(w32, g92, 1);
        long w34 = cat(w33, g89, 1);
        long w35 = cat(w34, g86, 1);
        long w36 = cat(w35, g83, 1);
        long w37 = cat(w36, g80, 1);
        long w38 = cat(w37, g77, 1);
        long w39 = cat(w38, g74, 1);
        long w40 = cat(w39, g71, 1);
        long w41 = cat(w40, g68, 1);
        long w42 = cat(w41, g65, 1);
        long w43 = cat(w42, g62, 1);
        long w44 = cat(w43, g59, 1);
        long w45 = cat(w44, g56, 1);
        long w46 = cat(w45, g53, 1);
        long w47 = cat(w46, g50, 1);
        long w48 = cat(w47, g47, 1);
        long w49 = cat(w48, g44, 1);
        long w50 = cat(w49, g41, 1);
        long w51 = cat(w50, g38, 1);
        long w52 = cat(w51, g35, 1);
        long w53 = cat(w52, g32, 1);
        long w54 = cat(w53, g29, 1);
        long w55 = cat(w54, g26, 1);
        long w56 = cat(w55, g23, 1);
        long w57 = cat(w56, g20, 1);
        long w58 = cat(w57, g17, 1);
        long w59 = cat(w58, g14, 1);
        long w60 = cat(w59, g11, 1);
        long w61 = cat(w60, g8, 1);
        long w62 = cat(w61, g5, 1);
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
                    answers.append(Long.toUnsignedString(emu_pxor_xmm_xmm_128__reg_xmm0_low__java(values[0], values[1])));
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
