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
    // one named local per gate, over the term of cmp_imm_gpr_16__flags__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(15, 0, v0), Extract(15, 0, v1))
    public static long emu_cmp_imm_gpr_16__flags__csharp(long a, long b) {
        long x1_0 = ext(b, 0, 0);
        long x1_1 = ext(b, 1, 1);
        long x1_2 = ext(b, 2, 2);
        long x1_3 = ext(b, 3, 3);
        long x1_4 = ext(b, 4, 4);
        long x1_5 = ext(b, 5, 5);
        long x1_6 = ext(b, 6, 6);
        long x1_7 = ext(b, 7, 7);
        long x1_8 = ext(b, 8, 8);
        long x1_9 = ext(b, 9, 9);
        long x1_10 = ext(b, 10, 10);
        long x1_11 = ext(b, 11, 11);
        long x1_12 = ext(b, 12, 12);
        long x1_13 = ext(b, 13, 13);
        long x1_14 = ext(b, 14, 14);
        long x1_15 = ext(b, 15, 15);
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
        long w0 = x0_15;
        long w1 = cat(w0, x0_14, 1);
        long w2 = cat(w1, x0_13, 1);
        long w3 = cat(w2, x0_12, 1);
        long w4 = cat(w3, x0_11, 1);
        long w5 = cat(w4, x0_10, 1);
        long w6 = cat(w5, x0_9, 1);
        long w7 = cat(w6, x0_8, 1);
        long w8 = cat(w7, x0_7, 1);
        long w9 = cat(w8, x0_6, 1);
        long w10 = cat(w9, x0_5, 1);
        long w11 = cat(w10, x0_4, 1);
        long w12 = cat(w11, x0_3, 1);
        long w13 = cat(w12, x0_2, 1);
        long w14 = cat(w13, x0_1, 1);
        long w15 = cat(w14, x0_0, 1);
        long w16 = cat(w15, x1_15, 1);
        long w17 = cat(w16, x1_14, 1);
        long w18 = cat(w17, x1_13, 1);
        long w19 = cat(w18, x1_12, 1);
        long w20 = cat(w19, x1_11, 1);
        long w21 = cat(w20, x1_10, 1);
        long w22 = cat(w21, x1_9, 1);
        long w23 = cat(w22, x1_8, 1);
        long w24 = cat(w23, x1_7, 1);
        long w25 = cat(w24, x1_6, 1);
        long w26 = cat(w25, x1_5, 1);
        long w27 = cat(w26, x1_4, 1);
        long w28 = cat(w27, x1_3, 1);
        long w29 = cat(w28, x1_2, 1);
        long w30 = cat(w29, x1_1, 1);
        long w31 = cat(w30, x1_0, 1);
        return m(w31, 32);
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
                    answers.Append(((ulong) emu_cmp_imm_gpr_16__flags__csharp(values[0], values[1])).ToString());
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
