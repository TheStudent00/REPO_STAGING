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
    // one named local per gate, over the term of or_gpr_gpr_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0) | Extract(31, 0, v1))
    static long emu_or_gpr_gpr_32__reg_rdi__java(long a, long b) {
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
        long g0 = (x0_0 | x1_0);
        long g1 = (x0_1 | x1_1);
        long g2 = (x0_2 | x1_2);
        long g3 = (x0_3 | x1_3);
        long g4 = (x0_4 | x1_4);
        long g5 = (x0_5 | x1_5);
        long g6 = (x0_6 | x1_6);
        long g7 = (x0_7 | x1_7);
        long g8 = (x0_8 | x1_8);
        long g9 = (x0_9 | x1_9);
        long g10 = (x0_10 | x1_10);
        long g11 = (x0_11 | x1_11);
        long g12 = (x0_12 | x1_12);
        long g13 = (x0_13 | x1_13);
        long g14 = (x0_14 | x1_14);
        long g15 = (x0_15 | x1_15);
        long g16 = (x0_16 | x1_16);
        long g17 = (x0_17 | x1_17);
        long g18 = (x0_18 | x1_18);
        long g19 = (x0_19 | x1_19);
        long g20 = (x0_20 | x1_20);
        long g21 = (x0_21 | x1_21);
        long g22 = (x0_22 | x1_22);
        long g23 = (x0_23 | x1_23);
        long g24 = (x0_24 | x1_24);
        long g25 = (x0_25 | x1_25);
        long g26 = (x0_26 | x1_26);
        long g27 = (x0_27 | x1_27);
        long g28 = (x0_28 | x1_28);
        long g29 = (x0_29 | x1_29);
        long g30 = (x0_30 | x1_30);
        long g31 = (x0_31 | x1_31);
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
        long w32 = cat(w31, g31, 1);
        long w33 = cat(w32, g30, 1);
        long w34 = cat(w33, g29, 1);
        long w35 = cat(w34, g28, 1);
        long w36 = cat(w35, g27, 1);
        long w37 = cat(w36, g26, 1);
        long w38 = cat(w37, g25, 1);
        long w39 = cat(w38, g24, 1);
        long w40 = cat(w39, g23, 1);
        long w41 = cat(w40, g22, 1);
        long w42 = cat(w41, g21, 1);
        long w43 = cat(w42, g20, 1);
        long w44 = cat(w43, g19, 1);
        long w45 = cat(w44, g18, 1);
        long w46 = cat(w45, g17, 1);
        long w47 = cat(w46, g16, 1);
        long w48 = cat(w47, g15, 1);
        long w49 = cat(w48, g14, 1);
        long w50 = cat(w49, g13, 1);
        long w51 = cat(w50, g12, 1);
        long w52 = cat(w51, g11, 1);
        long w53 = cat(w52, g10, 1);
        long w54 = cat(w53, g9, 1);
        long w55 = cat(w54, g8, 1);
        long w56 = cat(w55, g7, 1);
        long w57 = cat(w56, g6, 1);
        long w58 = cat(w57, g5, 1);
        long w59 = cat(w58, g4, 1);
        long w60 = cat(w59, g3, 1);
        long w61 = cat(w60, g2, 1);
        long w62 = cat(w61, g1, 1);
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
                    answers.append(Long.toUnsignedString(emu_or_gpr_gpr_32__reg_rdi__java(values[0], values[1])));
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
