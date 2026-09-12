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
    // one named local per gate, over the term of xor_imm_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, Extract(31, 0, v0) ^ Extract(31, 0, v1))
    public static long emu_xor_imm_gpr_32__reg_rdi__csharp(long a, long b) {
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
        long x1_8 = ext(a, 8, 8);
        long x0_8 = ext(b, 8, 8);
        long x1_9 = ext(a, 9, 9);
        long x0_9 = ext(b, 9, 9);
        long x1_10 = ext(a, 10, 10);
        long x0_10 = ext(b, 10, 10);
        long x1_11 = ext(a, 11, 11);
        long x0_11 = ext(b, 11, 11);
        long x1_12 = ext(a, 12, 12);
        long x0_12 = ext(b, 12, 12);
        long x1_13 = ext(a, 13, 13);
        long x0_13 = ext(b, 13, 13);
        long x1_14 = ext(a, 14, 14);
        long x0_14 = ext(b, 14, 14);
        long x1_15 = ext(a, 15, 15);
        long x0_15 = ext(b, 15, 15);
        long x1_16 = ext(a, 16, 16);
        long x0_16 = ext(b, 16, 16);
        long x1_17 = ext(a, 17, 17);
        long x0_17 = ext(b, 17, 17);
        long x1_18 = ext(a, 18, 18);
        long x0_18 = ext(b, 18, 18);
        long x1_19 = ext(a, 19, 19);
        long x0_19 = ext(b, 19, 19);
        long x1_20 = ext(a, 20, 20);
        long x0_20 = ext(b, 20, 20);
        long x1_21 = ext(a, 21, 21);
        long x0_21 = ext(b, 21, 21);
        long x1_22 = ext(a, 22, 22);
        long x0_22 = ext(b, 22, 22);
        long x1_23 = ext(a, 23, 23);
        long x0_23 = ext(b, 23, 23);
        long x1_24 = ext(a, 24, 24);
        long x0_24 = ext(b, 24, 24);
        long x1_25 = ext(a, 25, 25);
        long x0_25 = ext(b, 25, 25);
        long x1_26 = ext(a, 26, 26);
        long x0_26 = ext(b, 26, 26);
        long x1_27 = ext(a, 27, 27);
        long x0_27 = ext(b, 27, 27);
        long x1_28 = ext(a, 28, 28);
        long x0_28 = ext(b, 28, 28);
        long x1_29 = ext(a, 29, 29);
        long x0_29 = ext(b, 29, 29);
        long x1_30 = ext(a, 30, 30);
        long x0_30 = ext(b, 30, 30);
        long x1_31 = ext(a, 31, 31);
        long x0_31 = ext(b, 31, 31);
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
                    answers.Append(((ulong) emu_xor_imm_gpr_32__reg_rdi__csharp(values[0], values[1])).ToString());
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
