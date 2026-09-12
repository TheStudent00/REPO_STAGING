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
    // one named local per gate, over the term of setb_gpr_one_8__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 8, v0), If(ULE(Extract(7, 0, v1), Extract(7, 0, v2)), 0, 1))
    static long emu_setb_gpr_one_8__reg_rdi__java(long a, long b, long c) {
        long x1_0 = ext(c, 0, 0);
        long x2_0 = ext(b, 0, 0);
        long x2_1 = ext(b, 1, 1);
        long x1_1 = ext(c, 1, 1);
        long x2_2 = ext(b, 2, 2);
        long x1_2 = ext(c, 2, 2);
        long x2_3 = ext(b, 3, 3);
        long x1_3 = ext(c, 3, 3);
        long x2_4 = ext(b, 4, 4);
        long x1_4 = ext(c, 4, 4);
        long x2_5 = ext(b, 5, 5);
        long x1_5 = ext(c, 5, 5);
        long x2_6 = ext(b, 6, 6);
        long x1_6 = ext(c, 6, 6);
        long x2_7 = ext(b, 7, 7);
        long x1_7 = ext(c, 7, 7);
        long x0_8 = ext(a, 8, 8);
        long x0_9 = ext(a, 9, 9);
        long x0_10 = ext(a, 10, 10);
        long x0_11 = ext(a, 11, 11);
        long x0_12 = ext(a, 12, 12);
        long x0_13 = ext(a, 13, 13);
        long x0_14 = ext(a, 14, 14);
        long x0_15 = ext(a, 15, 15);
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
        long g1 = (x2_0 | g0);
        long g2 = (g1 ^ 1L);
        long g3 = (x2_1 ^ 1L);
        long g4 = (g3 | g2);
        long g5 = (g4 ^ 1L);
        long g6 = (x1_1 | g2);
        long g7 = (g6 ^ 1L);
        long g8 = (x1_1 | g3);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 | g7);
        long g11 = (g10 | g5);
        long g12 = (g11 ^ 1L);
        long g13 = (x2_2 ^ 1L);
        long g14 = (g13 | g12);
        long g15 = (g14 ^ 1L);
        long g16 = (x1_2 | g12);
        long g17 = (g16 ^ 1L);
        long g18 = (x1_2 | g13);
        long g19 = (g18 ^ 1L);
        long g20 = (g19 | g17);
        long g21 = (g20 | g15);
        long g22 = (g21 ^ 1L);
        long g23 = (x2_3 ^ 1L);
        long g24 = (g23 | g22);
        long g25 = (g24 ^ 1L);
        long g26 = (x1_3 | g22);
        long g27 = (g26 ^ 1L);
        long g28 = (x1_3 | g23);
        long g29 = (g28 ^ 1L);
        long g30 = (g29 | g27);
        long g31 = (g30 | g25);
        long g32 = (g31 ^ 1L);
        long g33 = (x2_4 ^ 1L);
        long g34 = (g33 | g32);
        long g35 = (g34 ^ 1L);
        long g36 = (x1_4 | g32);
        long g37 = (g36 ^ 1L);
        long g38 = (x1_4 | g33);
        long g39 = (g38 ^ 1L);
        long g40 = (g39 | g37);
        long g41 = (g40 | g35);
        long g42 = (g41 ^ 1L);
        long g43 = (x2_5 ^ 1L);
        long g44 = (g43 | g42);
        long g45 = (g44 ^ 1L);
        long g46 = (x1_5 | g42);
        long g47 = (g46 ^ 1L);
        long g48 = (x1_5 | g43);
        long g49 = (g48 ^ 1L);
        long g50 = (g49 | g47);
        long g51 = (g50 | g45);
        long g52 = (g51 ^ 1L);
        long g53 = (x2_6 ^ 1L);
        long g54 = (g53 | g52);
        long g55 = (g54 ^ 1L);
        long g56 = (x1_6 | g52);
        long g57 = (g56 ^ 1L);
        long g58 = (x1_6 | g53);
        long g59 = (g58 ^ 1L);
        long g60 = (g59 | g57);
        long g61 = (g60 | g55);
        long g62 = (g61 ^ 1L);
        long g63 = (x2_7 ^ 1L);
        long g64 = (g63 | g62);
        long g65 = (x1_7 | g62);
        long g66 = (x1_7 | g63);
        long g67 = (g66 & g65);
        long g68 = (g67 & g64);
        long k0 = 0L;
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
        long w49 = cat(w48, x0_14, 1);
        long w50 = cat(w49, x0_13, 1);
        long w51 = cat(w50, x0_12, 1);
        long w52 = cat(w51, x0_11, 1);
        long w53 = cat(w52, x0_10, 1);
        long w54 = cat(w53, x0_9, 1);
        long w55 = cat(w54, x0_8, 1);
        long w56 = cat(w55, k0, 1);
        long w57 = cat(w56, k0, 1);
        long w58 = cat(w57, k0, 1);
        long w59 = cat(w58, k0, 1);
        long w60 = cat(w59, k0, 1);
        long w61 = cat(w60, k0, 1);
        long w62 = cat(w61, k0, 1);
        long w63 = cat(w62, g68, 1);
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
                    answers.append(Long.toUnsignedString(emu_setb_gpr_one_8__reg_rdi__java(values[0], values[1], values[2])));
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
