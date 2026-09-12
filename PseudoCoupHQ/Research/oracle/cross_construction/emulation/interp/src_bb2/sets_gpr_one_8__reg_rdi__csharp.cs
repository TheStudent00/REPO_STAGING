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
    // one named local per gate, over the term of sets_gpr_one_8__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 8, v2), If(Or(Extract(7, 7, v0) == 0, Extract(7, 7, v1) == 0), 0, 1))
    public static long emu_sets_gpr_one_8__reg_rdi__csharp(long a, long b, long c) {
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
        long g0 = (x0_7 & x1_7);
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
        long w63 = cat(w62, g0, 1);
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
                    answers.Append(((ulong) emu_sets_gpr_one_8__reg_rdi__csharp(values[0], values[1], values[2])).ToString());
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
