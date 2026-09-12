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
    // one named local per gate, over the term of not_gpr_one_64__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   ~v0
    public static long emu_not_gpr_one_64__reg_rdi__csharp(long a) {
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
        long g0 = (x0_0 ^ 1L);
        long g1 = (x0_1 ^ 1L);
        long g2 = (x0_2 ^ 1L);
        long g3 = (x0_3 ^ 1L);
        long g4 = (x0_4 ^ 1L);
        long g5 = (x0_5 ^ 1L);
        long g6 = (x0_6 ^ 1L);
        long g7 = (x0_7 ^ 1L);
        long g8 = (x0_8 ^ 1L);
        long g9 = (x0_9 ^ 1L);
        long g10 = (x0_10 ^ 1L);
        long g11 = (x0_11 ^ 1L);
        long g12 = (x0_12 ^ 1L);
        long g13 = (x0_13 ^ 1L);
        long g14 = (x0_14 ^ 1L);
        long g15 = (x0_15 ^ 1L);
        long g16 = (x0_16 ^ 1L);
        long g17 = (x0_17 ^ 1L);
        long g18 = (x0_18 ^ 1L);
        long g19 = (x0_19 ^ 1L);
        long g20 = (x0_20 ^ 1L);
        long g21 = (x0_21 ^ 1L);
        long g22 = (x0_22 ^ 1L);
        long g23 = (x0_23 ^ 1L);
        long g24 = (x0_24 ^ 1L);
        long g25 = (x0_25 ^ 1L);
        long g26 = (x0_26 ^ 1L);
        long g27 = (x0_27 ^ 1L);
        long g28 = (x0_28 ^ 1L);
        long g29 = (x0_29 ^ 1L);
        long g30 = (x0_30 ^ 1L);
        long g31 = (x0_31 ^ 1L);
        long g32 = (x0_32 ^ 1L);
        long g33 = (x0_33 ^ 1L);
        long g34 = (x0_34 ^ 1L);
        long g35 = (x0_35 ^ 1L);
        long g36 = (x0_36 ^ 1L);
        long g37 = (x0_37 ^ 1L);
        long g38 = (x0_38 ^ 1L);
        long g39 = (x0_39 ^ 1L);
        long g40 = (x0_40 ^ 1L);
        long g41 = (x0_41 ^ 1L);
        long g42 = (x0_42 ^ 1L);
        long g43 = (x0_43 ^ 1L);
        long g44 = (x0_44 ^ 1L);
        long g45 = (x0_45 ^ 1L);
        long g46 = (x0_46 ^ 1L);
        long g47 = (x0_47 ^ 1L);
        long g48 = (x0_48 ^ 1L);
        long g49 = (x0_49 ^ 1L);
        long g50 = (x0_50 ^ 1L);
        long g51 = (x0_51 ^ 1L);
        long g52 = (x0_52 ^ 1L);
        long g53 = (x0_53 ^ 1L);
        long g54 = (x0_54 ^ 1L);
        long g55 = (x0_55 ^ 1L);
        long g56 = (x0_56 ^ 1L);
        long g57 = (x0_57 ^ 1L);
        long g58 = (x0_58 ^ 1L);
        long g59 = (x0_59 ^ 1L);
        long g60 = (x0_60 ^ 1L);
        long g61 = (x0_61 ^ 1L);
        long g62 = (x0_62 ^ 1L);
        long g63 = (x0_63 ^ 1L);
        long w0 = g63;
        long w1 = cat(w0, g62, 1);
        long w2 = cat(w1, g61, 1);
        long w3 = cat(w2, g60, 1);
        long w4 = cat(w3, g59, 1);
        long w5 = cat(w4, g58, 1);
        long w6 = cat(w5, g57, 1);
        long w7 = cat(w6, g56, 1);
        long w8 = cat(w7, g55, 1);
        long w9 = cat(w8, g54, 1);
        long w10 = cat(w9, g53, 1);
        long w11 = cat(w10, g52, 1);
        long w12 = cat(w11, g51, 1);
        long w13 = cat(w12, g50, 1);
        long w14 = cat(w13, g49, 1);
        long w15 = cat(w14, g48, 1);
        long w16 = cat(w15, g47, 1);
        long w17 = cat(w16, g46, 1);
        long w18 = cat(w17, g45, 1);
        long w19 = cat(w18, g44, 1);
        long w20 = cat(w19, g43, 1);
        long w21 = cat(w20, g42, 1);
        long w22 = cat(w21, g41, 1);
        long w23 = cat(w22, g40, 1);
        long w24 = cat(w23, g39, 1);
        long w25 = cat(w24, g38, 1);
        long w26 = cat(w25, g37, 1);
        long w27 = cat(w26, g36, 1);
        long w28 = cat(w27, g35, 1);
        long w29 = cat(w28, g34, 1);
        long w30 = cat(w29, g33, 1);
        long w31 = cat(w30, g32, 1);
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
                    answers.Append(((ulong) emu_not_gpr_one_64__reg_rdi__csharp(values[0])).ToString());
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
