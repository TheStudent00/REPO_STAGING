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
    // one named local per gate, over the term of cmovne_gpr_gpr_64__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   If(~(~v0 | ~v1) == 0, v2, v3)
    static long emu_cmovne_gpr_gpr_64__reg_rdi__java(long a, long b, long c, long d) {
        long x3_0 = ext(c, 0, 0);
        long x1_11 = ext(a, 11, 11);
        long x0_11 = ext(b, 11, 11);
        long x1_6 = ext(a, 6, 6);
        long x0_6 = ext(b, 6, 6);
        long x1_0 = ext(a, 0, 0);
        long x0_0 = ext(b, 0, 0);
        long x1_31 = ext(a, 31, 31);
        long x0_31 = ext(b, 31, 31);
        long x1_5 = ext(a, 5, 5);
        long x0_5 = ext(b, 5, 5);
        long x1_37 = ext(a, 37, 37);
        long x0_37 = ext(b, 37, 37);
        long x1_32 = ext(a, 32, 32);
        long x0_32 = ext(b, 32, 32);
        long x1_25 = ext(a, 25, 25);
        long x0_25 = ext(b, 25, 25);
        long x1_38 = ext(a, 38, 38);
        long x0_38 = ext(b, 38, 38);
        long x1_52 = ext(a, 52, 52);
        long x0_52 = ext(b, 52, 52);
        long x1_15 = ext(a, 15, 15);
        long x0_15 = ext(b, 15, 15);
        long x1_26 = ext(a, 26, 26);
        long x0_26 = ext(b, 26, 26);
        long x1_16 = ext(a, 16, 16);
        long x0_16 = ext(b, 16, 16);
        long x1_28 = ext(a, 28, 28);
        long x0_28 = ext(b, 28, 28);
        long x1_48 = ext(a, 48, 48);
        long x0_48 = ext(b, 48, 48);
        long x1_55 = ext(a, 55, 55);
        long x0_55 = ext(b, 55, 55);
        long x1_41 = ext(a, 41, 41);
        long x0_41 = ext(b, 41, 41);
        long x1_4 = ext(a, 4, 4);
        long x0_4 = ext(b, 4, 4);
        long x1_57 = ext(a, 57, 57);
        long x0_57 = ext(b, 57, 57);
        long x1_8 = ext(a, 8, 8);
        long x0_8 = ext(b, 8, 8);
        long x1_1 = ext(a, 1, 1);
        long x0_1 = ext(b, 1, 1);
        long x1_7 = ext(a, 7, 7);
        long x0_7 = ext(b, 7, 7);
        long x1_9 = ext(a, 9, 9);
        long x0_9 = ext(b, 9, 9);
        long x1_23 = ext(a, 23, 23);
        long x0_23 = ext(b, 23, 23);
        long x1_14 = ext(a, 14, 14);
        long x0_14 = ext(b, 14, 14);
        long x1_2 = ext(a, 2, 2);
        long x0_2 = ext(b, 2, 2);
        long x1_61 = ext(a, 61, 61);
        long x0_61 = ext(b, 61, 61);
        long x1_60 = ext(a, 60, 60);
        long x0_60 = ext(b, 60, 60);
        long x1_27 = ext(a, 27, 27);
        long x0_27 = ext(b, 27, 27);
        long x1_17 = ext(a, 17, 17);
        long x0_17 = ext(b, 17, 17);
        long x1_19 = ext(a, 19, 19);
        long x0_19 = ext(b, 19, 19);
        long x1_56 = ext(a, 56, 56);
        long x0_56 = ext(b, 56, 56);
        long x1_58 = ext(a, 58, 58);
        long x0_58 = ext(b, 58, 58);
        long x1_50 = ext(a, 50, 50);
        long x0_50 = ext(b, 50, 50);
        long x1_24 = ext(a, 24, 24);
        long x0_24 = ext(b, 24, 24);
        long x1_63 = ext(a, 63, 63);
        long x0_63 = ext(b, 63, 63);
        long x1_10 = ext(a, 10, 10);
        long x0_10 = ext(b, 10, 10);
        long x1_29 = ext(a, 29, 29);
        long x0_29 = ext(b, 29, 29);
        long x1_62 = ext(a, 62, 62);
        long x0_62 = ext(b, 62, 62);
        long x1_34 = ext(a, 34, 34);
        long x0_34 = ext(b, 34, 34);
        long x1_21 = ext(a, 21, 21);
        long x0_21 = ext(b, 21, 21);
        long x1_12 = ext(a, 12, 12);
        long x0_12 = ext(b, 12, 12);
        long x1_35 = ext(a, 35, 35);
        long x0_35 = ext(b, 35, 35);
        long x1_39 = ext(a, 39, 39);
        long x0_39 = ext(b, 39, 39);
        long x1_53 = ext(a, 53, 53);
        long x0_53 = ext(b, 53, 53);
        long x1_40 = ext(a, 40, 40);
        long x0_40 = ext(b, 40, 40);
        long x1_44 = ext(a, 44, 44);
        long x0_44 = ext(b, 44, 44);
        long x1_49 = ext(a, 49, 49);
        long x0_49 = ext(b, 49, 49);
        long x1_30 = ext(a, 30, 30);
        long x0_30 = ext(b, 30, 30);
        long x1_36 = ext(a, 36, 36);
        long x0_36 = ext(b, 36, 36);
        long x1_54 = ext(a, 54, 54);
        long x0_54 = ext(b, 54, 54);
        long x1_59 = ext(a, 59, 59);
        long x0_59 = ext(b, 59, 59);
        long x1_22 = ext(a, 22, 22);
        long x0_22 = ext(b, 22, 22);
        long x1_51 = ext(a, 51, 51);
        long x0_51 = ext(b, 51, 51);
        long x1_3 = ext(a, 3, 3);
        long x0_3 = ext(b, 3, 3);
        long x1_45 = ext(a, 45, 45);
        long x0_45 = ext(b, 45, 45);
        long x1_43 = ext(a, 43, 43);
        long x0_43 = ext(b, 43, 43);
        long x1_13 = ext(a, 13, 13);
        long x0_13 = ext(b, 13, 13);
        long x1_33 = ext(a, 33, 33);
        long x0_33 = ext(b, 33, 33);
        long x1_46 = ext(a, 46, 46);
        long x0_46 = ext(b, 46, 46);
        long x1_20 = ext(a, 20, 20);
        long x0_20 = ext(b, 20, 20);
        long x1_47 = ext(a, 47, 47);
        long x0_47 = ext(b, 47, 47);
        long x1_42 = ext(a, 42, 42);
        long x0_42 = ext(b, 42, 42);
        long x1_18 = ext(a, 18, 18);
        long x0_18 = ext(b, 18, 18);
        long x2_0 = ext(d, 0, 0);
        long x3_1 = ext(c, 1, 1);
        long x2_1 = ext(d, 1, 1);
        long x3_2 = ext(c, 2, 2);
        long x2_2 = ext(d, 2, 2);
        long x3_3 = ext(c, 3, 3);
        long x2_3 = ext(d, 3, 3);
        long x3_4 = ext(c, 4, 4);
        long x2_4 = ext(d, 4, 4);
        long x3_5 = ext(c, 5, 5);
        long x2_5 = ext(d, 5, 5);
        long x3_6 = ext(c, 6, 6);
        long x2_6 = ext(d, 6, 6);
        long x3_7 = ext(c, 7, 7);
        long x2_7 = ext(d, 7, 7);
        long x3_8 = ext(c, 8, 8);
        long x2_8 = ext(d, 8, 8);
        long x3_9 = ext(c, 9, 9);
        long x2_9 = ext(d, 9, 9);
        long x3_10 = ext(c, 10, 10);
        long x2_10 = ext(d, 10, 10);
        long x3_11 = ext(c, 11, 11);
        long x2_11 = ext(d, 11, 11);
        long x3_12 = ext(c, 12, 12);
        long x2_12 = ext(d, 12, 12);
        long x3_13 = ext(c, 13, 13);
        long x2_13 = ext(d, 13, 13);
        long x3_14 = ext(c, 14, 14);
        long x2_14 = ext(d, 14, 14);
        long x3_15 = ext(c, 15, 15);
        long x2_15 = ext(d, 15, 15);
        long x3_16 = ext(c, 16, 16);
        long x2_16 = ext(d, 16, 16);
        long x3_17 = ext(c, 17, 17);
        long x2_17 = ext(d, 17, 17);
        long x3_18 = ext(c, 18, 18);
        long x2_18 = ext(d, 18, 18);
        long x3_19 = ext(c, 19, 19);
        long x2_19 = ext(d, 19, 19);
        long x3_20 = ext(c, 20, 20);
        long x2_20 = ext(d, 20, 20);
        long x3_21 = ext(c, 21, 21);
        long x2_21 = ext(d, 21, 21);
        long x3_22 = ext(c, 22, 22);
        long x2_22 = ext(d, 22, 22);
        long x3_23 = ext(c, 23, 23);
        long x2_23 = ext(d, 23, 23);
        long x3_24 = ext(c, 24, 24);
        long x2_24 = ext(d, 24, 24);
        long x3_25 = ext(c, 25, 25);
        long x2_25 = ext(d, 25, 25);
        long x3_26 = ext(c, 26, 26);
        long x2_26 = ext(d, 26, 26);
        long x3_27 = ext(c, 27, 27);
        long x2_27 = ext(d, 27, 27);
        long x3_28 = ext(c, 28, 28);
        long x2_28 = ext(d, 28, 28);
        long x3_29 = ext(c, 29, 29);
        long x2_29 = ext(d, 29, 29);
        long x3_30 = ext(c, 30, 30);
        long x2_30 = ext(d, 30, 30);
        long x3_31 = ext(c, 31, 31);
        long x2_31 = ext(d, 31, 31);
        long x3_32 = ext(c, 32, 32);
        long x2_32 = ext(d, 32, 32);
        long x3_33 = ext(c, 33, 33);
        long x2_33 = ext(d, 33, 33);
        long x3_34 = ext(c, 34, 34);
        long x2_34 = ext(d, 34, 34);
        long x3_35 = ext(c, 35, 35);
        long x2_35 = ext(d, 35, 35);
        long x3_36 = ext(c, 36, 36);
        long x2_36 = ext(d, 36, 36);
        long x3_37 = ext(c, 37, 37);
        long x2_37 = ext(d, 37, 37);
        long x3_38 = ext(c, 38, 38);
        long x2_38 = ext(d, 38, 38);
        long x3_39 = ext(c, 39, 39);
        long x2_39 = ext(d, 39, 39);
        long x3_40 = ext(c, 40, 40);
        long x2_40 = ext(d, 40, 40);
        long x3_41 = ext(c, 41, 41);
        long x2_41 = ext(d, 41, 41);
        long x3_42 = ext(c, 42, 42);
        long x2_42 = ext(d, 42, 42);
        long x3_43 = ext(c, 43, 43);
        long x2_43 = ext(d, 43, 43);
        long x3_44 = ext(c, 44, 44);
        long x2_44 = ext(d, 44, 44);
        long x3_45 = ext(c, 45, 45);
        long x2_45 = ext(d, 45, 45);
        long x3_46 = ext(c, 46, 46);
        long x2_46 = ext(d, 46, 46);
        long x3_47 = ext(c, 47, 47);
        long x2_47 = ext(d, 47, 47);
        long x3_48 = ext(c, 48, 48);
        long x2_48 = ext(d, 48, 48);
        long x3_49 = ext(c, 49, 49);
        long x2_49 = ext(d, 49, 49);
        long x3_50 = ext(c, 50, 50);
        long x2_50 = ext(d, 50, 50);
        long x3_51 = ext(c, 51, 51);
        long x2_51 = ext(d, 51, 51);
        long x3_52 = ext(c, 52, 52);
        long x2_52 = ext(d, 52, 52);
        long x3_53 = ext(c, 53, 53);
        long x2_53 = ext(d, 53, 53);
        long x3_54 = ext(c, 54, 54);
        long x2_54 = ext(d, 54, 54);
        long x3_55 = ext(c, 55, 55);
        long x2_55 = ext(d, 55, 55);
        long x3_56 = ext(c, 56, 56);
        long x2_56 = ext(d, 56, 56);
        long x3_57 = ext(c, 57, 57);
        long x2_57 = ext(d, 57, 57);
        long x3_58 = ext(c, 58, 58);
        long x2_58 = ext(d, 58, 58);
        long x3_59 = ext(c, 59, 59);
        long x2_59 = ext(d, 59, 59);
        long x3_60 = ext(c, 60, 60);
        long x2_60 = ext(d, 60, 60);
        long x3_61 = ext(c, 61, 61);
        long x2_61 = ext(d, 61, 61);
        long x3_62 = ext(c, 62, 62);
        long x2_62 = ext(d, 62, 62);
        long x3_63 = ext(c, 63, 63);
        long x2_63 = ext(d, 63, 63);
        long g0 = (x1_11 ^ 1L);
        long g1 = (x0_11 ^ 1L);
        long g2 = (g1 | g0);
        long g3 = (g2 ^ 1L);
        long g4 = (x1_6 ^ 1L);
        long g5 = (x0_6 ^ 1L);
        long g6 = (g5 | g4);
        long g7 = (g6 ^ 1L);
        long g8 = (x1_0 ^ 1L);
        long g9 = (x0_0 ^ 1L);
        long g10 = (g9 | g8);
        long g11 = (g10 ^ 1L);
        long g12 = (x1_31 ^ 1L);
        long g13 = (x0_31 ^ 1L);
        long g14 = (g13 | g12);
        long g15 = (g14 ^ 1L);
        long g16 = (x1_5 ^ 1L);
        long g17 = (x0_5 ^ 1L);
        long g18 = (g17 | g16);
        long g19 = (g18 ^ 1L);
        long g20 = (x1_37 ^ 1L);
        long g21 = (x0_37 ^ 1L);
        long g22 = (g21 | g20);
        long g23 = (g22 ^ 1L);
        long g24 = (x1_32 ^ 1L);
        long g25 = (x0_32 ^ 1L);
        long g26 = (g25 | g24);
        long g27 = (g26 ^ 1L);
        long g28 = (x1_25 ^ 1L);
        long g29 = (x0_25 ^ 1L);
        long g30 = (g29 | g28);
        long g31 = (g30 ^ 1L);
        long g32 = (x1_38 ^ 1L);
        long g33 = (x0_38 ^ 1L);
        long g34 = (g33 | g32);
        long g35 = (g34 ^ 1L);
        long g36 = (x1_52 ^ 1L);
        long g37 = (x0_52 ^ 1L);
        long g38 = (g37 | g36);
        long g39 = (g38 ^ 1L);
        long g40 = (x1_15 ^ 1L);
        long g41 = (x0_15 ^ 1L);
        long g42 = (g41 | g40);
        long g43 = (g42 ^ 1L);
        long g44 = (x1_26 ^ 1L);
        long g45 = (x0_26 ^ 1L);
        long g46 = (g45 | g44);
        long g47 = (g46 ^ 1L);
        long g48 = (x1_16 ^ 1L);
        long g49 = (x0_16 ^ 1L);
        long g50 = (g49 | g48);
        long g51 = (g50 ^ 1L);
        long g52 = (x1_28 ^ 1L);
        long g53 = (x0_28 ^ 1L);
        long g54 = (g53 | g52);
        long g55 = (g54 ^ 1L);
        long g56 = (x1_48 ^ 1L);
        long g57 = (x0_48 ^ 1L);
        long g58 = (g57 | g56);
        long g59 = (g58 ^ 1L);
        long g60 = (x1_55 ^ 1L);
        long g61 = (x0_55 ^ 1L);
        long g62 = (g61 | g60);
        long g63 = (g62 ^ 1L);
        long g64 = (x1_41 ^ 1L);
        long g65 = (x0_41 ^ 1L);
        long g66 = (g65 | g64);
        long g67 = (g66 ^ 1L);
        long g68 = (x1_4 ^ 1L);
        long g69 = (x0_4 ^ 1L);
        long g70 = (g69 | g68);
        long g71 = (g70 ^ 1L);
        long g72 = (x1_57 ^ 1L);
        long g73 = (x0_57 ^ 1L);
        long g74 = (g73 | g72);
        long g75 = (g74 ^ 1L);
        long g76 = (x1_8 ^ 1L);
        long g77 = (x0_8 ^ 1L);
        long g78 = (g77 | g76);
        long g79 = (g78 ^ 1L);
        long g80 = (x1_1 ^ 1L);
        long g81 = (x0_1 ^ 1L);
        long g82 = (g81 | g80);
        long g83 = (g82 ^ 1L);
        long g84 = (x1_7 ^ 1L);
        long g85 = (x0_7 ^ 1L);
        long g86 = (g85 | g84);
        long g87 = (g86 ^ 1L);
        long g88 = (x1_9 ^ 1L);
        long g89 = (x0_9 ^ 1L);
        long g90 = (g89 | g88);
        long g91 = (g90 ^ 1L);
        long g92 = (x1_23 ^ 1L);
        long g93 = (x0_23 ^ 1L);
        long g94 = (g93 | g92);
        long g95 = (g94 ^ 1L);
        long g96 = (x1_14 ^ 1L);
        long g97 = (x0_14 ^ 1L);
        long g98 = (g97 | g96);
        long g99 = (g98 ^ 1L);
        long g100 = (x1_2 ^ 1L);
        long g101 = (x0_2 ^ 1L);
        long g102 = (g101 | g100);
        long g103 = (g102 ^ 1L);
        long g104 = (x1_61 ^ 1L);
        long g105 = (x0_61 ^ 1L);
        long g106 = (g105 | g104);
        long g107 = (g106 ^ 1L);
        long g108 = (x1_60 ^ 1L);
        long g109 = (x0_60 ^ 1L);
        long g110 = (g109 | g108);
        long g111 = (g110 ^ 1L);
        long g112 = (x1_27 ^ 1L);
        long g113 = (x0_27 ^ 1L);
        long g114 = (g113 | g112);
        long g115 = (g114 ^ 1L);
        long g116 = (x1_17 ^ 1L);
        long g117 = (x0_17 ^ 1L);
        long g118 = (g117 | g116);
        long g119 = (g118 ^ 1L);
        long g120 = (x1_19 ^ 1L);
        long g121 = (x0_19 ^ 1L);
        long g122 = (g121 | g120);
        long g123 = (g122 ^ 1L);
        long g124 = (x1_56 ^ 1L);
        long g125 = (x0_56 ^ 1L);
        long g126 = (g125 | g124);
        long g127 = (g126 ^ 1L);
        long g128 = (x1_58 ^ 1L);
        long g129 = (x0_58 ^ 1L);
        long g130 = (g129 | g128);
        long g131 = (g130 ^ 1L);
        long g132 = (x1_50 ^ 1L);
        long g133 = (x0_50 ^ 1L);
        long g134 = (g133 | g132);
        long g135 = (g134 ^ 1L);
        long g136 = (x1_24 ^ 1L);
        long g137 = (x0_24 ^ 1L);
        long g138 = (g137 | g136);
        long g139 = (g138 ^ 1L);
        long g140 = (x1_63 ^ 1L);
        long g141 = (x0_63 ^ 1L);
        long g142 = (g141 | g140);
        long g143 = (g142 ^ 1L);
        long g144 = (x1_10 ^ 1L);
        long g145 = (x0_10 ^ 1L);
        long g146 = (g145 | g144);
        long g147 = (g146 ^ 1L);
        long g148 = (x1_29 ^ 1L);
        long g149 = (x0_29 ^ 1L);
        long g150 = (g149 | g148);
        long g151 = (g150 ^ 1L);
        long g152 = (x1_62 ^ 1L);
        long g153 = (x0_62 ^ 1L);
        long g154 = (g153 | g152);
        long g155 = (g154 ^ 1L);
        long g156 = (x1_34 ^ 1L);
        long g157 = (x0_34 ^ 1L);
        long g158 = (g157 | g156);
        long g159 = (g158 ^ 1L);
        long g160 = (x1_21 ^ 1L);
        long g161 = (x0_21 ^ 1L);
        long g162 = (g161 | g160);
        long g163 = (g162 ^ 1L);
        long g164 = (x1_12 ^ 1L);
        long g165 = (x0_12 ^ 1L);
        long g166 = (g165 | g164);
        long g167 = (g166 ^ 1L);
        long g168 = (x1_35 ^ 1L);
        long g169 = (x0_35 ^ 1L);
        long g170 = (g169 | g168);
        long g171 = (g170 ^ 1L);
        long g172 = (x1_39 ^ 1L);
        long g173 = (x0_39 ^ 1L);
        long g174 = (g173 | g172);
        long g175 = (g174 ^ 1L);
        long g176 = (x1_53 ^ 1L);
        long g177 = (x0_53 ^ 1L);
        long g178 = (g177 | g176);
        long g179 = (g178 ^ 1L);
        long g180 = (x1_40 ^ 1L);
        long g181 = (x0_40 ^ 1L);
        long g182 = (g181 | g180);
        long g183 = (g182 ^ 1L);
        long g184 = (x1_44 ^ 1L);
        long g185 = (x0_44 ^ 1L);
        long g186 = (g185 | g184);
        long g187 = (g186 ^ 1L);
        long g188 = (x1_49 ^ 1L);
        long g189 = (x0_49 ^ 1L);
        long g190 = (g189 | g188);
        long g191 = (g190 ^ 1L);
        long g192 = (x1_30 ^ 1L);
        long g193 = (x0_30 ^ 1L);
        long g194 = (g193 | g192);
        long g195 = (g194 ^ 1L);
        long g196 = (x1_36 ^ 1L);
        long g197 = (x0_36 ^ 1L);
        long g198 = (g197 | g196);
        long g199 = (g198 ^ 1L);
        long g200 = (x1_54 ^ 1L);
        long g201 = (x0_54 ^ 1L);
        long g202 = (g201 | g200);
        long g203 = (g202 ^ 1L);
        long g204 = (x1_59 ^ 1L);
        long g205 = (x0_59 ^ 1L);
        long g206 = (g205 | g204);
        long g207 = (g206 ^ 1L);
        long g208 = (x1_22 ^ 1L);
        long g209 = (x0_22 ^ 1L);
        long g210 = (g209 | g208);
        long g211 = (g210 ^ 1L);
        long g212 = (x1_51 ^ 1L);
        long g213 = (x0_51 ^ 1L);
        long g214 = (g213 | g212);
        long g215 = (g214 ^ 1L);
        long g216 = (x1_3 ^ 1L);
        long g217 = (x0_3 ^ 1L);
        long g218 = (g217 | g216);
        long g219 = (g218 ^ 1L);
        long g220 = (x1_45 ^ 1L);
        long g221 = (x0_45 ^ 1L);
        long g222 = (g221 | g220);
        long g223 = (g222 ^ 1L);
        long g224 = (x1_43 ^ 1L);
        long g225 = (x0_43 ^ 1L);
        long g226 = (g225 | g224);
        long g227 = (g226 ^ 1L);
        long g228 = (x1_13 ^ 1L);
        long g229 = (x0_13 ^ 1L);
        long g230 = (g229 | g228);
        long g231 = (g230 ^ 1L);
        long g232 = (x1_33 ^ 1L);
        long g233 = (x0_33 ^ 1L);
        long g234 = (g233 | g232);
        long g235 = (g234 ^ 1L);
        long g236 = (x1_46 ^ 1L);
        long g237 = (x0_46 ^ 1L);
        long g238 = (g237 | g236);
        long g239 = (g238 ^ 1L);
        long g240 = (x1_20 ^ 1L);
        long g241 = (x0_20 ^ 1L);
        long g242 = (g241 | g240);
        long g243 = (g242 ^ 1L);
        long g244 = (x1_47 ^ 1L);
        long g245 = (x0_47 ^ 1L);
        long g246 = (g245 | g244);
        long g247 = (g246 ^ 1L);
        long g248 = (x1_42 ^ 1L);
        long g249 = (x0_42 ^ 1L);
        long g250 = (g249 | g248);
        long g251 = (g250 ^ 1L);
        long g252 = (x1_18 ^ 1L);
        long g253 = (x0_18 ^ 1L);
        long g254 = (g253 | g252);
        long g255 = (g254 ^ 1L);
        long g256 = (g255 | g251);
        long g257 = (g256 | g247);
        long g258 = (g257 | g243);
        long g259 = (g258 | g239);
        long g260 = (g259 | g235);
        long g261 = (g260 | g231);
        long g262 = (g261 | g227);
        long g263 = (g262 | g223);
        long g264 = (g263 | g219);
        long g265 = (g264 | g215);
        long g266 = (g265 | g211);
        long g267 = (g266 | g207);
        long g268 = (g267 | g203);
        long g269 = (g268 | g199);
        long g270 = (g269 | g195);
        long g271 = (g270 | g191);
        long g272 = (g271 | g187);
        long g273 = (g272 | g183);
        long g274 = (g273 | g179);
        long g275 = (g274 | g175);
        long g276 = (g275 | g171);
        long g277 = (g276 | g167);
        long g278 = (g277 | g163);
        long g279 = (g278 | g159);
        long g280 = (g279 | g155);
        long g281 = (g280 | g151);
        long g282 = (g281 | g147);
        long g283 = (g282 | g143);
        long g284 = (g283 | g139);
        long g285 = (g284 | g135);
        long g286 = (g285 | g131);
        long g287 = (g286 | g127);
        long g288 = (g287 | g123);
        long g289 = (g288 | g119);
        long g290 = (g289 | g115);
        long g291 = (g290 | g111);
        long g292 = (g291 | g107);
        long g293 = (g292 | g103);
        long g294 = (g293 | g99);
        long g295 = (g294 | g95);
        long g296 = (g295 | g91);
        long g297 = (g296 | g87);
        long g298 = (g297 | g83);
        long g299 = (g298 | g79);
        long g300 = (g299 | g75);
        long g301 = (g300 | g71);
        long g302 = (g301 | g67);
        long g303 = (g302 | g63);
        long g304 = (g303 | g59);
        long g305 = (g304 | g55);
        long g306 = (g305 | g51);
        long g307 = (g306 | g47);
        long g308 = (g307 | g43);
        long g309 = (g308 | g39);
        long g310 = (g309 | g35);
        long g311 = (g310 | g31);
        long g312 = (g311 | g27);
        long g313 = (g312 | g23);
        long g314 = (g313 | g19);
        long g315 = (g314 | g15);
        long g316 = (g315 | g11);
        long g317 = (g316 | g7);
        long g318 = (g317 | g3);
        long g319 = (g318 ^ 1L);
        long g320 = (g319 ^ 1L);
        long g321 = (g320 & x3_0);
        long g322 = (g319 & x2_0);
        long g323 = (g322 | g321);
        long g324 = (g320 & x3_1);
        long g325 = (g319 & x2_1);
        long g326 = (g325 | g324);
        long g327 = (g320 & x3_2);
        long g328 = (g319 & x2_2);
        long g329 = (g328 | g327);
        long g330 = (g320 & x3_3);
        long g331 = (g319 & x2_3);
        long g332 = (g331 | g330);
        long g333 = (g320 & x3_4);
        long g334 = (g319 & x2_4);
        long g335 = (g334 | g333);
        long g336 = (g320 & x3_5);
        long g337 = (g319 & x2_5);
        long g338 = (g337 | g336);
        long g339 = (g320 & x3_6);
        long g340 = (g319 & x2_6);
        long g341 = (g340 | g339);
        long g342 = (g320 & x3_7);
        long g343 = (g319 & x2_7);
        long g344 = (g343 | g342);
        long g345 = (g320 & x3_8);
        long g346 = (g319 & x2_8);
        long g347 = (g346 | g345);
        long g348 = (g320 & x3_9);
        long g349 = (g319 & x2_9);
        long g350 = (g349 | g348);
        long g351 = (g320 & x3_10);
        long g352 = (g319 & x2_10);
        long g353 = (g352 | g351);
        long g354 = (g320 & x3_11);
        long g355 = (g319 & x2_11);
        long g356 = (g355 | g354);
        long g357 = (g320 & x3_12);
        long g358 = (g319 & x2_12);
        long g359 = (g358 | g357);
        long g360 = (g320 & x3_13);
        long g361 = (g319 & x2_13);
        long g362 = (g361 | g360);
        long g363 = (g320 & x3_14);
        long g364 = (g319 & x2_14);
        long g365 = (g364 | g363);
        long g366 = (g320 & x3_15);
        long g367 = (g319 & x2_15);
        long g368 = (g367 | g366);
        long g369 = (g320 & x3_16);
        long g370 = (g319 & x2_16);
        long g371 = (g370 | g369);
        long g372 = (g320 & x3_17);
        long g373 = (g319 & x2_17);
        long g374 = (g373 | g372);
        long g375 = (g320 & x3_18);
        long g376 = (g319 & x2_18);
        long g377 = (g376 | g375);
        long g378 = (g320 & x3_19);
        long g379 = (g319 & x2_19);
        long g380 = (g379 | g378);
        long g381 = (g320 & x3_20);
        long g382 = (g319 & x2_20);
        long g383 = (g382 | g381);
        long g384 = (g320 & x3_21);
        long g385 = (g319 & x2_21);
        long g386 = (g385 | g384);
        long g387 = (g320 & x3_22);
        long g388 = (g319 & x2_22);
        long g389 = (g388 | g387);
        long g390 = (g320 & x3_23);
        long g391 = (g319 & x2_23);
        long g392 = (g391 | g390);
        long g393 = (g320 & x3_24);
        long g394 = (g319 & x2_24);
        long g395 = (g394 | g393);
        long g396 = (g320 & x3_25);
        long g397 = (g319 & x2_25);
        long g398 = (g397 | g396);
        long g399 = (g320 & x3_26);
        long g400 = (g319 & x2_26);
        long g401 = (g400 | g399);
        long g402 = (g320 & x3_27);
        long g403 = (g319 & x2_27);
        long g404 = (g403 | g402);
        long g405 = (g320 & x3_28);
        long g406 = (g319 & x2_28);
        long g407 = (g406 | g405);
        long g408 = (g320 & x3_29);
        long g409 = (g319 & x2_29);
        long g410 = (g409 | g408);
        long g411 = (g320 & x3_30);
        long g412 = (g319 & x2_30);
        long g413 = (g412 | g411);
        long g414 = (g320 & x3_31);
        long g415 = (g319 & x2_31);
        long g416 = (g415 | g414);
        long g417 = (g320 & x3_32);
        long g418 = (g319 & x2_32);
        long g419 = (g418 | g417);
        long g420 = (g320 & x3_33);
        long g421 = (g319 & x2_33);
        long g422 = (g421 | g420);
        long g423 = (g320 & x3_34);
        long g424 = (g319 & x2_34);
        long g425 = (g424 | g423);
        long g426 = (g320 & x3_35);
        long g427 = (g319 & x2_35);
        long g428 = (g427 | g426);
        long g429 = (g320 & x3_36);
        long g430 = (g319 & x2_36);
        long g431 = (g430 | g429);
        long g432 = (g320 & x3_37);
        long g433 = (g319 & x2_37);
        long g434 = (g433 | g432);
        long g435 = (g320 & x3_38);
        long g436 = (g319 & x2_38);
        long g437 = (g436 | g435);
        long g438 = (g320 & x3_39);
        long g439 = (g319 & x2_39);
        long g440 = (g439 | g438);
        long g441 = (g320 & x3_40);
        long g442 = (g319 & x2_40);
        long g443 = (g442 | g441);
        long g444 = (g320 & x3_41);
        long g445 = (g319 & x2_41);
        long g446 = (g445 | g444);
        long g447 = (g320 & x3_42);
        long g448 = (g319 & x2_42);
        long g449 = (g448 | g447);
        long g450 = (g320 & x3_43);
        long g451 = (g319 & x2_43);
        long g452 = (g451 | g450);
        long g453 = (g320 & x3_44);
        long g454 = (g319 & x2_44);
        long g455 = (g454 | g453);
        long g456 = (g320 & x3_45);
        long g457 = (g319 & x2_45);
        long g458 = (g457 | g456);
        long g459 = (g320 & x3_46);
        long g460 = (g319 & x2_46);
        long g461 = (g460 | g459);
        long g462 = (g320 & x3_47);
        long g463 = (g319 & x2_47);
        long g464 = (g463 | g462);
        long g465 = (g320 & x3_48);
        long g466 = (g319 & x2_48);
        long g467 = (g466 | g465);
        long g468 = (g320 & x3_49);
        long g469 = (g319 & x2_49);
        long g470 = (g469 | g468);
        long g471 = (g320 & x3_50);
        long g472 = (g319 & x2_50);
        long g473 = (g472 | g471);
        long g474 = (g320 & x3_51);
        long g475 = (g319 & x2_51);
        long g476 = (g475 | g474);
        long g477 = (g320 & x3_52);
        long g478 = (g319 & x2_52);
        long g479 = (g478 | g477);
        long g480 = (g320 & x3_53);
        long g481 = (g319 & x2_53);
        long g482 = (g481 | g480);
        long g483 = (g320 & x3_54);
        long g484 = (g319 & x2_54);
        long g485 = (g484 | g483);
        long g486 = (g320 & x3_55);
        long g487 = (g319 & x2_55);
        long g488 = (g487 | g486);
        long g489 = (g320 & x3_56);
        long g490 = (g319 & x2_56);
        long g491 = (g490 | g489);
        long g492 = (g320 & x3_57);
        long g493 = (g319 & x2_57);
        long g494 = (g493 | g492);
        long g495 = (g320 & x3_58);
        long g496 = (g319 & x2_58);
        long g497 = (g496 | g495);
        long g498 = (g320 & x3_59);
        long g499 = (g319 & x2_59);
        long g500 = (g499 | g498);
        long g501 = (g320 & x3_60);
        long g502 = (g319 & x2_60);
        long g503 = (g502 | g501);
        long g504 = (g320 & x3_61);
        long g505 = (g319 & x2_61);
        long g506 = (g505 | g504);
        long g507 = (g320 & x3_62);
        long g508 = (g319 & x2_62);
        long g509 = (g508 | g507);
        long g510 = (g320 & x3_63);
        long g511 = (g319 & x2_63);
        long g512 = (g511 | g510);
        long w0 = g512;
        long w1 = cat(w0, g509, 1);
        long w2 = cat(w1, g506, 1);
        long w3 = cat(w2, g503, 1);
        long w4 = cat(w3, g500, 1);
        long w5 = cat(w4, g497, 1);
        long w6 = cat(w5, g494, 1);
        long w7 = cat(w6, g491, 1);
        long w8 = cat(w7, g488, 1);
        long w9 = cat(w8, g485, 1);
        long w10 = cat(w9, g482, 1);
        long w11 = cat(w10, g479, 1);
        long w12 = cat(w11, g476, 1);
        long w13 = cat(w12, g473, 1);
        long w14 = cat(w13, g470, 1);
        long w15 = cat(w14, g467, 1);
        long w16 = cat(w15, g464, 1);
        long w17 = cat(w16, g461, 1);
        long w18 = cat(w17, g458, 1);
        long w19 = cat(w18, g455, 1);
        long w20 = cat(w19, g452, 1);
        long w21 = cat(w20, g449, 1);
        long w22 = cat(w21, g446, 1);
        long w23 = cat(w22, g443, 1);
        long w24 = cat(w23, g440, 1);
        long w25 = cat(w24, g437, 1);
        long w26 = cat(w25, g434, 1);
        long w27 = cat(w26, g431, 1);
        long w28 = cat(w27, g428, 1);
        long w29 = cat(w28, g425, 1);
        long w30 = cat(w29, g422, 1);
        long w31 = cat(w30, g419, 1);
        long w32 = cat(w31, g416, 1);
        long w33 = cat(w32, g413, 1);
        long w34 = cat(w33, g410, 1);
        long w35 = cat(w34, g407, 1);
        long w36 = cat(w35, g404, 1);
        long w37 = cat(w36, g401, 1);
        long w38 = cat(w37, g398, 1);
        long w39 = cat(w38, g395, 1);
        long w40 = cat(w39, g392, 1);
        long w41 = cat(w40, g389, 1);
        long w42 = cat(w41, g386, 1);
        long w43 = cat(w42, g383, 1);
        long w44 = cat(w43, g380, 1);
        long w45 = cat(w44, g377, 1);
        long w46 = cat(w45, g374, 1);
        long w47 = cat(w46, g371, 1);
        long w48 = cat(w47, g368, 1);
        long w49 = cat(w48, g365, 1);
        long w50 = cat(w49, g362, 1);
        long w51 = cat(w50, g359, 1);
        long w52 = cat(w51, g356, 1);
        long w53 = cat(w52, g353, 1);
        long w54 = cat(w53, g350, 1);
        long w55 = cat(w54, g347, 1);
        long w56 = cat(w55, g344, 1);
        long w57 = cat(w56, g341, 1);
        long w58 = cat(w57, g338, 1);
        long w59 = cat(w58, g335, 1);
        long w60 = cat(w59, g332, 1);
        long w61 = cat(w60, g329, 1);
        long w62 = cat(w61, g326, 1);
        long w63 = cat(w62, g323, 1);
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
                    answers.append(Long.toUnsignedString(emu_cmovne_gpr_gpr_64__reg_rdi__java(values[0], values[1], values[2], values[3])));
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
