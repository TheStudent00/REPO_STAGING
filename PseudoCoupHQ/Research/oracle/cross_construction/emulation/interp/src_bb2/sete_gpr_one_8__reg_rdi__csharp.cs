using System;
using System.Text;

public static class Emu {
    public static long m(long x, int w) {
        if (w >= 64) { return x; }
        return x & ((1L << w) - 1L);
    }
    public static long s(long x, int w) {
        if (w >= 64) { return x; }
        return (x << (64 - w)) >> (64 - w);
    }
    public static long add(long a, long b, int w) { return m(unchecked(a + b), w); }
    public static long sub(long a, long b, int w) { return m(unchecked(a - b), w); }
    public static long mul(long a, long b, int w) { return m(unchecked(a * b), w); }
    public static long band(long a, long b, int w) { return m(a & b, w); }
    public static long bor(long a, long b, int w) { return m(a | b, w); }
    public static long bxor(long a, long b, int w) { return m(a ^ b, w); }
    public static long bnot(long a, int w) { return m(~a, w); }
    public static long bneg(long a, int w) { return m(unchecked(-a), w); }
    public static long shl(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(a << (int) n, w);
    }
    public static long lshr(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m((long)(((ulong) m(a, w)) >> (int) n), w);
    }
    public static long ashr(long a, long n, int w) {
        long v = s(a, w);
        long k = n;
        if (k >= w) { k = w - 1; }
        return m(v >> (int) k, w);
    }
    public static long udiv(long a, long b, int w) {
        return m((long)(((ulong) m(a, w)) / ((ulong) m(b, w))), w);
    }
    public static long urem(long a, long b, int w) {
        return m((long)(((ulong) m(a, w)) % ((ulong) m(b, w))), w);
    }
    public static long sdiv(long a, long b, int w) { return m(s(a, w) / s(b, w), w); }
    public static long srem(long a, long b, int w) { return m(s(a, w) % s(b, w), w); }
    public static bool ult(long a, long b, int w) { return ((ulong) m(a, w)) < ((ulong) m(b, w)); }
    public static bool ule(long a, long b, int w) { return ((ulong) m(a, w)) <= ((ulong) m(b, w)); }
    public static bool ugt(long a, long b, int w) { return ((ulong) m(a, w)) > ((ulong) m(b, w)); }
    public static bool uge(long a, long b, int w) { return ((ulong) m(a, w)) >= ((ulong) m(b, w)); }
    public static bool slt(long a, long b, int w) { return s(a, w) < s(b, w); }
    public static bool sle(long a, long b, int w) { return s(a, w) <= s(b, w); }
    public static bool sgt(long a, long b, int w) { return s(a, w) > s(b, w); }
    public static bool sge(long a, long b, int w) { return s(a, w) >= s(b, w); }
    public static bool eq(long a, long b, int w) { return m(a, w) == m(b, w); }
    public static bool ne(long a, long b, int w) { return m(a, w) != m(b, w); }
    public static long cat(long hi, long lo, int lw) { return (hi << lw) | m(lo, lw); }
    public static long ext(long x, int hi, int lo) {
        return m((long)(((ulong) x) >> lo), hi - lo + 1);
    }
    public static long sext(long x, int fromw, int tow) { return m(s(x, fromw), tow); }
    public static double b2f(long x, int w) {
        if (w == 32) { return BitConverter.UInt32BitsToSingle((uint) m(x, 32)); }
        return BitConverter.Int64BitsToDouble(x);
    }
    public static long f2b(double f, int w) {
        if (w == 32) { return (long) BitConverter.SingleToUInt32Bits((float) f); }
        return BitConverter.DoubleToInt64Bits(f);
    }
    public static long fadd(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    + BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) + b2f(b, w), w);
    }
    public static long fsub(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    - BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) - b2f(b, w), w);
    }
    public static long fmul(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    * BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) * b2f(b, w), w);
    }
    public static long fdiv(long a, long b, int w) {
        if (w == 32) {
            float r = BitConverter.UInt32BitsToSingle((uint) m(a, 32))
                    / BitConverter.UInt32BitsToSingle((uint) m(b, 32));
            return (long) BitConverter.SingleToUInt32Bits(r);
        }
        return f2b(b2f(a, w) / b2f(b, w), w);
    }
    public static long i2f(long x, int fromw, int w) {
        if (w == 32) {
            return (long) BitConverter.SingleToUInt32Bits((float) s(x, fromw));
        }
        return BitConverter.DoubleToInt64Bits((double) s(x, fromw));
    }
    public static long u2f(long x, int fromw, int w) {
        if (w == 32) {
            return (long) BitConverter.SingleToUInt32Bits((float)(ulong) m(x, fromw));
        }
        return BitConverter.DoubleToInt64Bits((double)(ulong) m(x, fromw));
    }
    public static long fwiden(long x, int fromw, int w) { return f2b(b2f(x, fromw), w); }

    // task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
    // one named local per gate, over the term of sete_gpr_one_8__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 8, v0), If(Extract(7, 0, v1) == Extract(7, 0, v2), 1, 0))
    public static long emu_sete_gpr_one_8__reg_rdi__csharp(long a, long b, long c) {
        long x1_7 = ext(b, 7, 7);
        long x2_7 = ext(a, 7, 7);
        long x2_6 = ext(a, 6, 6);
        long x1_6 = ext(b, 6, 6);
        long x2_5 = ext(a, 5, 5);
        long x1_5 = ext(b, 5, 5);
        long x2_4 = ext(a, 4, 4);
        long x1_4 = ext(b, 4, 4);
        long x2_3 = ext(a, 3, 3);
        long x1_3 = ext(b, 3, 3);
        long x2_2 = ext(a, 2, 2);
        long x1_2 = ext(b, 2, 2);
        long x2_1 = ext(a, 1, 1);
        long x1_1 = ext(b, 1, 1);
        long x1_0 = ext(b, 0, 0);
        long x2_0 = ext(a, 0, 0);
        long x0_8 = ext(c, 8, 8);
        long x0_9 = ext(c, 9, 9);
        long x0_10 = ext(c, 10, 10);
        long x0_11 = ext(c, 11, 11);
        long x0_12 = ext(c, 12, 12);
        long x0_13 = ext(c, 13, 13);
        long x0_14 = ext(c, 14, 14);
        long x0_15 = ext(c, 15, 15);
        long x0_16 = ext(c, 16, 16);
        long x0_17 = ext(c, 17, 17);
        long x0_18 = ext(c, 18, 18);
        long x0_19 = ext(c, 19, 19);
        long x0_20 = ext(c, 20, 20);
        long x0_21 = ext(c, 21, 21);
        long x0_22 = ext(c, 22, 22);
        long x0_23 = ext(c, 23, 23);
        long x0_24 = ext(c, 24, 24);
        long x0_25 = ext(c, 25, 25);
        long x0_26 = ext(c, 26, 26);
        long x0_27 = ext(c, 27, 27);
        long x0_28 = ext(c, 28, 28);
        long x0_29 = ext(c, 29, 29);
        long x0_30 = ext(c, 30, 30);
        long x0_31 = ext(c, 31, 31);
        long x0_32 = ext(c, 32, 32);
        long x0_33 = ext(c, 33, 33);
        long x0_34 = ext(c, 34, 34);
        long x0_35 = ext(c, 35, 35);
        long x0_36 = ext(c, 36, 36);
        long x0_37 = ext(c, 37, 37);
        long x0_38 = ext(c, 38, 38);
        long x0_39 = ext(c, 39, 39);
        long x0_40 = ext(c, 40, 40);
        long x0_41 = ext(c, 41, 41);
        long x0_42 = ext(c, 42, 42);
        long x0_43 = ext(c, 43, 43);
        long x0_44 = ext(c, 44, 44);
        long x0_45 = ext(c, 45, 45);
        long x0_46 = ext(c, 46, 46);
        long x0_47 = ext(c, 47, 47);
        long x0_48 = ext(c, 48, 48);
        long x0_49 = ext(c, 49, 49);
        long x0_50 = ext(c, 50, 50);
        long x0_51 = ext(c, 51, 51);
        long x0_52 = ext(c, 52, 52);
        long x0_53 = ext(c, 53, 53);
        long x0_54 = ext(c, 54, 54);
        long x0_55 = ext(c, 55, 55);
        long x0_56 = ext(c, 56, 56);
        long x0_57 = ext(c, 57, 57);
        long x0_58 = ext(c, 58, 58);
        long x0_59 = ext(c, 59, 59);
        long x0_60 = ext(c, 60, 60);
        long x0_61 = ext(c, 61, 61);
        long x0_62 = ext(c, 62, 62);
        long x0_63 = ext(c, 63, 63);
        long g0 = (x2_7 ^ 1L);
        long g1 = (g0 | x1_7);
        long g2 = (x1_7 ^ 1L);
        long g3 = (x2_7 | g2);
        long g4 = (x2_6 ^ 1L);
        long g5 = (x1_6 | g4);
        long g6 = (x1_6 ^ 1L);
        long g7 = (g6 | x2_6);
        long g8 = (x2_5 ^ 1L);
        long g9 = (x1_5 | g8);
        long g10 = (x1_5 ^ 1L);
        long g11 = (x2_5 | g10);
        long g12 = (x2_4 ^ 1L);
        long g13 = (x1_4 | g12);
        long g14 = (x1_4 ^ 1L);
        long g15 = (x2_4 | g14);
        long g16 = (x2_3 ^ 1L);
        long g17 = (x1_3 | g16);
        long g18 = (x1_3 ^ 1L);
        long g19 = (x2_3 | g18);
        long g20 = (x2_2 ^ 1L);
        long g21 = (x1_2 | g20);
        long g22 = (x1_2 ^ 1L);
        long g23 = (x2_2 | g22);
        long g24 = (x2_1 ^ 1L);
        long g25 = (x1_1 | g24);
        long g26 = (x1_1 ^ 1L);
        long g27 = (g26 | x2_1);
        long g28 = (x2_0 ^ 1L);
        long g29 = (g28 | x1_0);
        long g30 = (x1_0 ^ 1L);
        long g31 = (g30 | x2_0);
        long g32 = (g31 & g29);
        long g33 = (g32 & g27);
        long g34 = (g33 & g25);
        long g35 = (g34 & g23);
        long g36 = (g35 & g21);
        long g37 = (g36 & g19);
        long g38 = (g37 & g17);
        long g39 = (g38 & g15);
        long g40 = (g39 & g13);
        long g41 = (g40 & g11);
        long g42 = (g41 & g9);
        long g43 = (g42 & g7);
        long g44 = (g43 & g5);
        long g45 = (g44 & g3);
        long g46 = (g45 & g1);
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
        long w63 = cat(w62, g46, 1);
        return m(w63, 64);
    }


    public static void Main() {
        StringBuilder answers = new StringBuilder();
        string line = Console.ReadLine();
        while (line != null) {
            string text = line.Trim();
            if (text.Length != 0) {
                string[] parts = text.Split((char[]) null,
                    StringSplitOptions.RemoveEmptyEntries);
                long[] values = new long[parts.Length];
                for (int i = 0; i < parts.Length; i++) {
                    values[i] = unchecked((long) ulong.Parse(parts[i]));
                }
                try {
                    answers.Append(((ulong) emu_sete_gpr_one_8__reg_rdi__csharp(values[0], values[1], values[2])).ToString());
                    answers.Append("\n");
                } catch (Exception problem) {
                    answers.Append("RAISE:");
                    answers.Append(problem.GetType().Name);
                    answers.Append("\n");
                }
            }
            line = Console.ReadLine();
        }
        Console.Write(answers.ToString());
    }
}
