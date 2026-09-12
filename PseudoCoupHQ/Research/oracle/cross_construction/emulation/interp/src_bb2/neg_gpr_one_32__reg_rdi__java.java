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
    // one named local per gate, over the term of neg_gpr_one_32__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0)*4294967295)
    static long emu_neg_gpr_one_32__reg_rdi__java(long a) {
        long x0_0 = ext(a, 0, 0);
        long x0_1 = ext(a, 1, 1);
        long x0_2 = ext(a, 2, 2);
        long x0_3 = ext(a, 3, 3);
        long x0_4 = ext(a, 4, 4);
        long x0_5 = ext(a, 5, 5);
        long x0_6 = ext(a, 6, 6);
        long x0_7 = ext(a, 7, 7);
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
        long g0 = (x0_0 ^ x0_1);
        long g1 = (g0 ^ 1L);
        long g2 = (g1 ^ 1L);
        long g3 = (x0_0 | x0_1);
        long g4 = (g3 ^ x0_2);
        long g5 = (g4 ^ 1L);
        long g6 = (g5 ^ 1L);
        long g7 = (x0_2 | g3);
        long g8 = (g7 ^ x0_3);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 ^ 1L);
        long g11 = (x0_3 | g7);
        long g12 = (g11 ^ x0_4);
        long g13 = (g12 ^ 1L);
        long g14 = (g13 ^ 1L);
        long g15 = (x0_4 | g11);
        long g16 = (g15 ^ x0_5);
        long g17 = (g16 ^ 1L);
        long g18 = (g17 ^ 1L);
        long g19 = (x0_5 | g15);
        long g20 = (g19 ^ x0_6);
        long g21 = (g20 ^ 1L);
        long g22 = (g21 ^ 1L);
        long g23 = (x0_6 | g19);
        long g24 = (g23 ^ x0_7);
        long g25 = (g24 ^ 1L);
        long g26 = (g25 ^ 1L);
        long g27 = (x0_7 | g23);
        long g28 = (g27 ^ x0_8);
        long g29 = (g28 ^ 1L);
        long g30 = (g29 ^ 1L);
        long g31 = (x0_8 | g27);
        long g32 = (g31 ^ x0_9);
        long g33 = (g32 ^ 1L);
        long g34 = (g33 ^ 1L);
        long g35 = (x0_9 | g31);
        long g36 = (g35 ^ x0_10);
        long g37 = (g36 ^ 1L);
        long g38 = (g37 ^ 1L);
        long g39 = (x0_10 | g35);
        long g40 = (g39 ^ x0_11);
        long g41 = (g40 ^ 1L);
        long g42 = (g41 ^ 1L);
        long g43 = (x0_11 | g39);
        long g44 = (g43 ^ x0_12);
        long g45 = (g44 ^ 1L);
        long g46 = (g45 ^ 1L);
        long g47 = (x0_12 | g43);
        long g48 = (g47 ^ x0_13);
        long g49 = (g48 ^ 1L);
        long g50 = (g49 ^ 1L);
        long g51 = (x0_13 | g47);
        long g52 = (g51 ^ x0_14);
        long g53 = (g52 ^ 1L);
        long g54 = (g53 ^ 1L);
        long g55 = (x0_14 | g51);
        long g56 = (g55 ^ x0_15);
        long g57 = (g56 ^ 1L);
        long g58 = (g57 ^ 1L);
        long g59 = (x0_15 | g55);
        long g60 = (g59 ^ x0_16);
        long g61 = (g60 ^ 1L);
        long g62 = (g61 ^ 1L);
        long g63 = (x0_16 | g59);
        long g64 = (g63 ^ x0_17);
        long g65 = (g64 ^ 1L);
        long g66 = (g65 ^ 1L);
        long g67 = (x0_17 | g63);
        long g68 = (g67 ^ x0_18);
        long g69 = (g68 ^ 1L);
        long g70 = (g69 ^ 1L);
        long g71 = (x0_18 | g67);
        long g72 = (g71 ^ x0_19);
        long g73 = (g72 ^ 1L);
        long g74 = (g73 ^ 1L);
        long g75 = (x0_19 | g71);
        long g76 = (g75 ^ x0_20);
        long g77 = (g76 ^ 1L);
        long g78 = (g77 ^ 1L);
        long g79 = (x0_20 | g75);
        long g80 = (g79 ^ x0_21);
        long g81 = (g80 ^ 1L);
        long g82 = (g81 ^ 1L);
        long g83 = (x0_21 | g79);
        long g84 = (g83 ^ x0_22);
        long g85 = (g84 ^ 1L);
        long g86 = (g85 ^ 1L);
        long g87 = (x0_22 | g83);
        long g88 = (g87 ^ x0_23);
        long g89 = (g88 ^ 1L);
        long g90 = (g89 ^ 1L);
        long g91 = (x0_23 | g87);
        long g92 = (g91 ^ x0_24);
        long g93 = (g92 ^ 1L);
        long g94 = (g93 ^ 1L);
        long g95 = (x0_24 | g91);
        long g96 = (g95 ^ x0_25);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ 1L);
        long g99 = (x0_25 | g95);
        long g100 = (g99 ^ x0_26);
        long g101 = (g100 ^ 1L);
        long g102 = (g101 ^ 1L);
        long g103 = (x0_26 | g99);
        long g104 = (g103 ^ x0_27);
        long g105 = (g104 ^ 1L);
        long g106 = (g105 ^ 1L);
        long g107 = (x0_27 | g103);
        long g108 = (g107 ^ x0_28);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 ^ 1L);
        long g111 = (x0_28 | g107);
        long g112 = (g111 ^ x0_29);
        long g113 = (g112 ^ 1L);
        long g114 = (g113 ^ 1L);
        long g115 = (x0_29 | g111);
        long g116 = (g115 ^ x0_30);
        long g117 = (g116 ^ 1L);
        long g118 = (g117 ^ 1L);
        long g119 = (x0_30 | g115);
        long g120 = (g119 ^ x0_31);
        long g121 = (g120 ^ 1L);
        long g122 = (g121 ^ 1L);
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
        long w32 = cat(w31, g122, 1);
        long w33 = cat(w32, g118, 1);
        long w34 = cat(w33, g114, 1);
        long w35 = cat(w34, g110, 1);
        long w36 = cat(w35, g106, 1);
        long w37 = cat(w36, g102, 1);
        long w38 = cat(w37, g98, 1);
        long w39 = cat(w38, g94, 1);
        long w40 = cat(w39, g90, 1);
        long w41 = cat(w40, g86, 1);
        long w42 = cat(w41, g82, 1);
        long w43 = cat(w42, g78, 1);
        long w44 = cat(w43, g74, 1);
        long w45 = cat(w44, g70, 1);
        long w46 = cat(w45, g66, 1);
        long w47 = cat(w46, g62, 1);
        long w48 = cat(w47, g58, 1);
        long w49 = cat(w48, g54, 1);
        long w50 = cat(w49, g50, 1);
        long w51 = cat(w50, g46, 1);
        long w52 = cat(w51, g42, 1);
        long w53 = cat(w52, g38, 1);
        long w54 = cat(w53, g34, 1);
        long w55 = cat(w54, g30, 1);
        long w56 = cat(w55, g26, 1);
        long w57 = cat(w56, g22, 1);
        long w58 = cat(w57, g18, 1);
        long w59 = cat(w58, g14, 1);
        long w60 = cat(w59, g10, 1);
        long w61 = cat(w60, g6, 1);
        long w62 = cat(w61, g2, 1);
        long w63 = cat(w62, x0_0, 1);
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
                    answers.append(Long.toUnsignedString(emu_neg_gpr_one_32__reg_rdi__java(values[0])));
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
