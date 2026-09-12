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
    // one named local per gate, over the term of setnp_gpr_one_8__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 8, v2), If(Extract(1, 1, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(2, 2, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(3, 3, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(4, 4, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(5, 5, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(6, 6, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(7, 7, Extract(7, 0, v0) + Extract(7, 0, v1)) == If(Extract(0, 0, v0) + 1 == Extract(0, 0, v1), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 0, 1))
    static long emu_setnp_gpr_one_8__reg_rdi__java(long a, long b, long c) {
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
        long x2_8 = ext(c, 8, 8);
        long x2_9 = ext(c, 9, 9);
        long x2_10 = ext(c, 10, 10);
        long x2_11 = ext(c, 11, 11);
        long x2_12 = ext(c, 12, 12);
        long x2_13 = ext(c, 13, 13);
        long x2_14 = ext(c, 14, 14);
        long x2_15 = ext(c, 15, 15);
        long x2_16 = ext(c, 16, 16);
        long x2_17 = ext(c, 17, 17);
        long x2_18 = ext(c, 18, 18);
        long x2_19 = ext(c, 19, 19);
        long x2_20 = ext(c, 20, 20);
        long x2_21 = ext(c, 21, 21);
        long x2_22 = ext(c, 22, 22);
        long x2_23 = ext(c, 23, 23);
        long x2_24 = ext(c, 24, 24);
        long x2_25 = ext(c, 25, 25);
        long x2_26 = ext(c, 26, 26);
        long x2_27 = ext(c, 27, 27);
        long x2_28 = ext(c, 28, 28);
        long x2_29 = ext(c, 29, 29);
        long x2_30 = ext(c, 30, 30);
        long x2_31 = ext(c, 31, 31);
        long x2_32 = ext(c, 32, 32);
        long x2_33 = ext(c, 33, 33);
        long x2_34 = ext(c, 34, 34);
        long x2_35 = ext(c, 35, 35);
        long x2_36 = ext(c, 36, 36);
        long x2_37 = ext(c, 37, 37);
        long x2_38 = ext(c, 38, 38);
        long x2_39 = ext(c, 39, 39);
        long x2_40 = ext(c, 40, 40);
        long x2_41 = ext(c, 41, 41);
        long x2_42 = ext(c, 42, 42);
        long x2_43 = ext(c, 43, 43);
        long x2_44 = ext(c, 44, 44);
        long x2_45 = ext(c, 45, 45);
        long x2_46 = ext(c, 46, 46);
        long x2_47 = ext(c, 47, 47);
        long x2_48 = ext(c, 48, 48);
        long x2_49 = ext(c, 49, 49);
        long x2_50 = ext(c, 50, 50);
        long x2_51 = ext(c, 51, 51);
        long x2_52 = ext(c, 52, 52);
        long x2_53 = ext(c, 53, 53);
        long x2_54 = ext(c, 54, 54);
        long x2_55 = ext(c, 55, 55);
        long x2_56 = ext(c, 56, 56);
        long x2_57 = ext(c, 57, 57);
        long x2_58 = ext(c, 58, 58);
        long x2_59 = ext(c, 59, 59);
        long x2_60 = ext(c, 60, 60);
        long x2_61 = ext(c, 61, 61);
        long x2_62 = ext(c, 62, 62);
        long x2_63 = ext(c, 63, 63);
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
        long g13 = (x1_2 ^ g12);
        long g14 = (g13 ^ 1L);
        long g15 = (x0_2 ^ g14);
        long g16 = (g15 ^ 1L);
        long g17 = (g12 ^ 1L);
        long g18 = (x1_2 ^ 1L);
        long g19 = (g18 | g17);
        long g20 = (g19 ^ 1L);
        long g21 = (x0_2 ^ 1L);
        long g22 = (g21 | g17);
        long g23 = (g22 ^ 1L);
        long g24 = (g21 | g18);
        long g25 = (g24 ^ 1L);
        long g26 = (g25 | g23);
        long g27 = (g26 | g20);
        long g28 = (x1_3 ^ g27);
        long g29 = (g28 ^ 1L);
        long g30 = (x0_3 ^ g29);
        long g31 = (g30 ^ 1L);
        long g32 = (g27 ^ 1L);
        long g33 = (x1_3 ^ 1L);
        long g34 = (g33 | g32);
        long g35 = (g34 ^ 1L);
        long g36 = (x0_3 ^ 1L);
        long g37 = (g36 | g32);
        long g38 = (g37 ^ 1L);
        long g39 = (g36 | g33);
        long g40 = (g39 ^ 1L);
        long g41 = (g40 | g38);
        long g42 = (g41 | g35);
        long g43 = (x1_4 ^ g42);
        long g44 = (g43 ^ 1L);
        long g45 = (x0_4 ^ g44);
        long g46 = (g45 ^ 1L);
        long g47 = (g42 ^ 1L);
        long g48 = (x1_4 ^ 1L);
        long g49 = (g48 | g47);
        long g50 = (g49 ^ 1L);
        long g51 = (x0_4 ^ 1L);
        long g52 = (g51 | g47);
        long g53 = (g52 ^ 1L);
        long g54 = (g51 | g48);
        long g55 = (g54 ^ 1L);
        long g56 = (g55 | g53);
        long g57 = (g56 | g50);
        long g58 = (x1_5 ^ g57);
        long g59 = (g58 ^ 1L);
        long g60 = (x0_5 ^ g59);
        long g61 = (g60 ^ 1L);
        long g62 = (g57 ^ 1L);
        long g63 = (x1_5 ^ 1L);
        long g64 = (g63 | g62);
        long g65 = (g64 ^ 1L);
        long g66 = (x0_5 ^ 1L);
        long g67 = (g66 | g62);
        long g68 = (g67 ^ 1L);
        long g69 = (g66 | g63);
        long g70 = (g69 ^ 1L);
        long g71 = (g70 | g68);
        long g72 = (g71 | g65);
        long g73 = (x1_6 ^ g72);
        long g74 = (g73 ^ 1L);
        long g75 = (x0_6 ^ g74);
        long g76 = (g75 ^ 1L);
        long g77 = (g72 ^ 1L);
        long g78 = (x1_6 ^ 1L);
        long g79 = (g78 | g77);
        long g80 = (g79 ^ 1L);
        long g81 = (x0_6 ^ 1L);
        long g82 = (g81 | g77);
        long g83 = (g82 ^ 1L);
        long g84 = (g81 | g78);
        long g85 = (g84 ^ 1L);
        long g86 = (g85 | g83);
        long g87 = (g86 | g80);
        long g88 = (x1_7 ^ g87);
        long g89 = (g88 ^ 1L);
        long g90 = (x0_7 ^ g89);
        long g91 = (g90 ^ 1L);
        long g92 = (x1_0 ^ x0_0);
        long g93 = (g92 ^ 1L);
        long g94 = (g93 ^ g91);
        long g95 = (g94 ^ 1L);
        long g96 = (g95 ^ g76);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ g61);
        long g99 = (g98 ^ 1L);
        long g100 = (g99 ^ g46);
        long g101 = (g100 ^ 1L);
        long g102 = (g101 ^ g31);
        long g103 = (g102 ^ 1L);
        long g104 = (g103 ^ g16);
        long g105 = (g104 ^ 1L);
        long g106 = (x1_1 ^ g2);
        long g107 = (g106 ^ 1L);
        long g108 = (x0_1 ^ g107);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 ^ g105);
        long g111 = (g110 ^ 1L);
        long g112 = (g111 ^ 1L);
        long k0 = 0L;
        long w0 = x2_63;
        long w1 = cat(w0, x2_62, 1);
        long w2 = cat(w1, x2_61, 1);
        long w3 = cat(w2, x2_60, 1);
        long w4 = cat(w3, x2_59, 1);
        long w5 = cat(w4, x2_58, 1);
        long w6 = cat(w5, x2_57, 1);
        long w7 = cat(w6, x2_56, 1);
        long w8 = cat(w7, x2_55, 1);
        long w9 = cat(w8, x2_54, 1);
        long w10 = cat(w9, x2_53, 1);
        long w11 = cat(w10, x2_52, 1);
        long w12 = cat(w11, x2_51, 1);
        long w13 = cat(w12, x2_50, 1);
        long w14 = cat(w13, x2_49, 1);
        long w15 = cat(w14, x2_48, 1);
        long w16 = cat(w15, x2_47, 1);
        long w17 = cat(w16, x2_46, 1);
        long w18 = cat(w17, x2_45, 1);
        long w19 = cat(w18, x2_44, 1);
        long w20 = cat(w19, x2_43, 1);
        long w21 = cat(w20, x2_42, 1);
        long w22 = cat(w21, x2_41, 1);
        long w23 = cat(w22, x2_40, 1);
        long w24 = cat(w23, x2_39, 1);
        long w25 = cat(w24, x2_38, 1);
        long w26 = cat(w25, x2_37, 1);
        long w27 = cat(w26, x2_36, 1);
        long w28 = cat(w27, x2_35, 1);
        long w29 = cat(w28, x2_34, 1);
        long w30 = cat(w29, x2_33, 1);
        long w31 = cat(w30, x2_32, 1);
        long w32 = cat(w31, x2_31, 1);
        long w33 = cat(w32, x2_30, 1);
        long w34 = cat(w33, x2_29, 1);
        long w35 = cat(w34, x2_28, 1);
        long w36 = cat(w35, x2_27, 1);
        long w37 = cat(w36, x2_26, 1);
        long w38 = cat(w37, x2_25, 1);
        long w39 = cat(w38, x2_24, 1);
        long w40 = cat(w39, x2_23, 1);
        long w41 = cat(w40, x2_22, 1);
        long w42 = cat(w41, x2_21, 1);
        long w43 = cat(w42, x2_20, 1);
        long w44 = cat(w43, x2_19, 1);
        long w45 = cat(w44, x2_18, 1);
        long w46 = cat(w45, x2_17, 1);
        long w47 = cat(w46, x2_16, 1);
        long w48 = cat(w47, x2_15, 1);
        long w49 = cat(w48, x2_14, 1);
        long w50 = cat(w49, x2_13, 1);
        long w51 = cat(w50, x2_12, 1);
        long w52 = cat(w51, x2_11, 1);
        long w53 = cat(w52, x2_10, 1);
        long w54 = cat(w53, x2_9, 1);
        long w55 = cat(w54, x2_8, 1);
        long w56 = cat(w55, k0, 1);
        long w57 = cat(w56, k0, 1);
        long w58 = cat(w57, k0, 1);
        long w59 = cat(w58, k0, 1);
        long w60 = cat(w59, k0, 1);
        long w61 = cat(w60, k0, 1);
        long w62 = cat(w61, k0, 1);
        long w63 = cat(w62, g112, 1);
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
                    answers.append(Long.toUnsignedString(emu_setnp_gpr_one_8__reg_rdi__java(values[0], values[1], values[2])));
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
