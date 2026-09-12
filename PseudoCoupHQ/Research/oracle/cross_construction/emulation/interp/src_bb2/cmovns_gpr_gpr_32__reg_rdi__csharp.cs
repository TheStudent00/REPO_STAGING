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
    // one named local per gate, over the term of cmovns_gpr_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(Or(Extract(31, 31, v0) == 0, Extract(31, 31, v1) == 0), Extract(31, 0, v2), Extract(31, 0, v3)))
    public static long emu_cmovns_gpr_gpr_32__reg_rdi__csharp(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
        long x1_31 = ext(a, 31, 31);
        long x0_31 = ext(b, 31, 31);
        long x2_0 = ext(c, 0, 0);
        long x3_1 = ext(d, 1, 1);
        long x2_1 = ext(c, 1, 1);
        long x3_2 = ext(d, 2, 2);
        long x2_2 = ext(c, 2, 2);
        long x3_3 = ext(d, 3, 3);
        long x2_3 = ext(c, 3, 3);
        long x3_4 = ext(d, 4, 4);
        long x2_4 = ext(c, 4, 4);
        long x3_5 = ext(d, 5, 5);
        long x2_5 = ext(c, 5, 5);
        long x3_6 = ext(d, 6, 6);
        long x2_6 = ext(c, 6, 6);
        long x3_7 = ext(d, 7, 7);
        long x2_7 = ext(c, 7, 7);
        long x3_8 = ext(d, 8, 8);
        long x2_8 = ext(c, 8, 8);
        long x3_9 = ext(d, 9, 9);
        long x2_9 = ext(c, 9, 9);
        long x3_10 = ext(d, 10, 10);
        long x2_10 = ext(c, 10, 10);
        long x3_11 = ext(d, 11, 11);
        long x2_11 = ext(c, 11, 11);
        long x3_12 = ext(d, 12, 12);
        long x2_12 = ext(c, 12, 12);
        long x3_13 = ext(d, 13, 13);
        long x2_13 = ext(c, 13, 13);
        long x3_14 = ext(d, 14, 14);
        long x2_14 = ext(c, 14, 14);
        long x3_15 = ext(d, 15, 15);
        long x2_15 = ext(c, 15, 15);
        long x3_16 = ext(d, 16, 16);
        long x2_16 = ext(c, 16, 16);
        long x3_17 = ext(d, 17, 17);
        long x2_17 = ext(c, 17, 17);
        long x3_18 = ext(d, 18, 18);
        long x2_18 = ext(c, 18, 18);
        long x3_19 = ext(d, 19, 19);
        long x2_19 = ext(c, 19, 19);
        long x3_20 = ext(d, 20, 20);
        long x2_20 = ext(c, 20, 20);
        long x3_21 = ext(d, 21, 21);
        long x2_21 = ext(c, 21, 21);
        long x3_22 = ext(d, 22, 22);
        long x2_22 = ext(c, 22, 22);
        long x3_23 = ext(d, 23, 23);
        long x2_23 = ext(c, 23, 23);
        long x3_24 = ext(d, 24, 24);
        long x2_24 = ext(c, 24, 24);
        long x3_25 = ext(d, 25, 25);
        long x2_25 = ext(c, 25, 25);
        long x3_26 = ext(d, 26, 26);
        long x2_26 = ext(c, 26, 26);
        long x3_27 = ext(d, 27, 27);
        long x2_27 = ext(c, 27, 27);
        long x3_28 = ext(d, 28, 28);
        long x2_28 = ext(c, 28, 28);
        long x3_29 = ext(d, 29, 29);
        long x2_29 = ext(c, 29, 29);
        long x3_30 = ext(d, 30, 30);
        long x2_30 = ext(c, 30, 30);
        long x3_31 = ext(d, 31, 31);
        long x2_31 = ext(c, 31, 31);
        long g0 = (x1_31 ^ 1L);
        long g1 = (x0_31 ^ 1L);
        long g2 = (g1 | g0);
        long g3 = (g2 ^ 1L);
        long g4 = (g3 & x3_0);
        long g5 = (g2 & x2_0);
        long g6 = (g5 | g4);
        long g7 = (g3 & x3_1);
        long g8 = (g2 & x2_1);
        long g9 = (g8 | g7);
        long g10 = (g3 & x3_2);
        long g11 = (g2 & x2_2);
        long g12 = (g11 | g10);
        long g13 = (g3 & x3_3);
        long g14 = (g2 & x2_3);
        long g15 = (g14 | g13);
        long g16 = (g3 & x3_4);
        long g17 = (g2 & x2_4);
        long g18 = (g17 | g16);
        long g19 = (g3 & x3_5);
        long g20 = (g2 & x2_5);
        long g21 = (g20 | g19);
        long g22 = (g3 & x3_6);
        long g23 = (g2 & x2_6);
        long g24 = (g23 | g22);
        long g25 = (g3 & x3_7);
        long g26 = (g2 & x2_7);
        long g27 = (g26 | g25);
        long g28 = (g3 & x3_8);
        long g29 = (g2 & x2_8);
        long g30 = (g29 | g28);
        long g31 = (g3 & x3_9);
        long g32 = (g2 & x2_9);
        long g33 = (g32 | g31);
        long g34 = (g3 & x3_10);
        long g35 = (g2 & x2_10);
        long g36 = (g35 | g34);
        long g37 = (g3 & x3_11);
        long g38 = (g2 & x2_11);
        long g39 = (g38 | g37);
        long g40 = (g3 & x3_12);
        long g41 = (g2 & x2_12);
        long g42 = (g41 | g40);
        long g43 = (g3 & x3_13);
        long g44 = (g2 & x2_13);
        long g45 = (g44 | g43);
        long g46 = (g3 & x3_14);
        long g47 = (g2 & x2_14);
        long g48 = (g47 | g46);
        long g49 = (g3 & x3_15);
        long g50 = (g2 & x2_15);
        long g51 = (g50 | g49);
        long g52 = (g3 & x3_16);
        long g53 = (g2 & x2_16);
        long g54 = (g53 | g52);
        long g55 = (g3 & x3_17);
        long g56 = (g2 & x2_17);
        long g57 = (g56 | g55);
        long g58 = (g3 & x3_18);
        long g59 = (g2 & x2_18);
        long g60 = (g59 | g58);
        long g61 = (g3 & x3_19);
        long g62 = (g2 & x2_19);
        long g63 = (g62 | g61);
        long g64 = (g3 & x3_20);
        long g65 = (g2 & x2_20);
        long g66 = (g65 | g64);
        long g67 = (g3 & x3_21);
        long g68 = (g2 & x2_21);
        long g69 = (g68 | g67);
        long g70 = (g3 & x3_22);
        long g71 = (g2 & x2_22);
        long g72 = (g71 | g70);
        long g73 = (g3 & x3_23);
        long g74 = (g2 & x2_23);
        long g75 = (g74 | g73);
        long g76 = (g3 & x3_24);
        long g77 = (g2 & x2_24);
        long g78 = (g77 | g76);
        long g79 = (g3 & x3_25);
        long g80 = (g2 & x2_25);
        long g81 = (g80 | g79);
        long g82 = (g3 & x3_26);
        long g83 = (g2 & x2_26);
        long g84 = (g83 | g82);
        long g85 = (g3 & x3_27);
        long g86 = (g2 & x2_27);
        long g87 = (g86 | g85);
        long g88 = (g3 & x3_28);
        long g89 = (g2 & x2_28);
        long g90 = (g89 | g88);
        long g91 = (g3 & x3_29);
        long g92 = (g2 & x2_29);
        long g93 = (g92 | g91);
        long g94 = (g3 & x3_30);
        long g95 = (g2 & x2_30);
        long g96 = (g95 | g94);
        long g97 = (g3 & x3_31);
        long g98 = (g2 & x2_31);
        long g99 = (g98 | g97);
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
        long w32 = cat(w31, g99, 1);
        long w33 = cat(w32, g96, 1);
        long w34 = cat(w33, g93, 1);
        long w35 = cat(w34, g90, 1);
        long w36 = cat(w35, g87, 1);
        long w37 = cat(w36, g84, 1);
        long w38 = cat(w37, g81, 1);
        long w39 = cat(w38, g78, 1);
        long w40 = cat(w39, g75, 1);
        long w41 = cat(w40, g72, 1);
        long w42 = cat(w41, g69, 1);
        long w43 = cat(w42, g66, 1);
        long w44 = cat(w43, g63, 1);
        long w45 = cat(w44, g60, 1);
        long w46 = cat(w45, g57, 1);
        long w47 = cat(w46, g54, 1);
        long w48 = cat(w47, g51, 1);
        long w49 = cat(w48, g48, 1);
        long w50 = cat(w49, g45, 1);
        long w51 = cat(w50, g42, 1);
        long w52 = cat(w51, g39, 1);
        long w53 = cat(w52, g36, 1);
        long w54 = cat(w53, g33, 1);
        long w55 = cat(w54, g30, 1);
        long w56 = cat(w55, g27, 1);
        long w57 = cat(w56, g24, 1);
        long w58 = cat(w57, g21, 1);
        long w59 = cat(w58, g18, 1);
        long w60 = cat(w59, g15, 1);
        long w61 = cat(w60, g12, 1);
        long w62 = cat(w61, g9, 1);
        long w63 = cat(w62, g6, 1);
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
                    answers.Append(((ulong) emu_cmovns_gpr_gpr_32__reg_rdi__csharp(values[0], values[1], values[2], values[3])).ToString());
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
