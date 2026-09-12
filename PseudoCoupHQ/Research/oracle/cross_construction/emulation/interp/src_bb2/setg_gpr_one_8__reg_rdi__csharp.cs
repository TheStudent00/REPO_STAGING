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
    // one named local per gate, over the term of setg_gpr_one_8__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 8, v2), If(And(Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 0, 1), Not(Extract(7, 0, v0) == Extract(7, 0, v1))), 1, 0))
    public static long emu_setg_gpr_one_8__reg_rdi__csharp(long a, long b, long c) {
        long x0_7 = ext(b, 7, 7);
        long x1_7 = ext(a, 7, 7);
        long x1_6 = ext(a, 6, 6);
        long x0_6 = ext(b, 6, 6);
        long x1_5 = ext(a, 5, 5);
        long x0_5 = ext(b, 5, 5);
        long x0_4 = ext(b, 4, 4);
        long x1_4 = ext(a, 4, 4);
        long x1_3 = ext(a, 3, 3);
        long x0_3 = ext(b, 3, 3);
        long x1_2 = ext(a, 2, 2);
        long x0_2 = ext(b, 2, 2);
        long x1_1 = ext(a, 1, 1);
        long x0_1 = ext(b, 1, 1);
        long x1_0 = ext(a, 0, 0);
        long x0_0 = ext(b, 0, 0);
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
        long g0 = (x1_7 ^ 1L);
        long g1 = (g0 | x0_7);
        long g2 = (x0_7 ^ 1L);
        long g3 = (x1_7 | g2);
        long g4 = (x1_6 ^ 1L);
        long g5 = (x0_6 | g4);
        long g6 = (x0_6 ^ 1L);
        long g7 = (x1_6 | g6);
        long g8 = (x1_5 ^ 1L);
        long g9 = (x0_5 | g8);
        long g10 = (x0_5 ^ 1L);
        long g11 = (x1_5 | g10);
        long g12 = (x1_4 ^ 1L);
        long g13 = (g12 | x0_4);
        long g14 = (x0_4 ^ 1L);
        long g15 = (x1_4 | g14);
        long g16 = (x1_3 ^ 1L);
        long g17 = (x0_3 | g16);
        long g18 = (x0_3 ^ 1L);
        long g19 = (x1_3 | g18);
        long g20 = (x1_2 ^ 1L);
        long g21 = (x0_2 | g20);
        long g22 = (x0_2 ^ 1L);
        long g23 = (x1_2 | g22);
        long g24 = (x1_1 ^ 1L);
        long g25 = (x0_1 | g24);
        long g26 = (x0_1 ^ 1L);
        long g27 = (x1_1 | g26);
        long g28 = (x1_0 ^ 1L);
        long g29 = (x0_0 | g28);
        long g30 = (x0_0 ^ 1L);
        long g31 = (x1_0 | g30);
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
        long g47 = (g46 ^ 1L);
        long g48 = (x0_0 | x0_1);
        long g49 = (x0_2 | g48);
        long g50 = (x0_3 | g49);
        long g51 = (x0_4 | g50);
        long g52 = (x0_5 | g51);
        long g53 = (x0_6 | g52);
        long g54 = (x0_7 | g53);
        long g55 = (g54 ^ x0_7);
        long g56 = (g55 ^ 1L);
        long g57 = (g53 ^ x0_7);
        long g58 = (g57 ^ 1L);
        long g59 = (g0 | g58);
        long g60 = (g59 ^ 1L);
        long g61 = (g30 | g28);
        long g62 = (x0_0 ^ x0_1);
        long g63 = (g62 ^ 1L);
        long g64 = (g63 | g61);
        long g65 = (g64 ^ 1L);
        long g66 = (g63 | g24);
        long g67 = (g66 ^ 1L);
        long g68 = (g24 | g61);
        long g69 = (g68 ^ 1L);
        long g70 = (g69 | g67);
        long g71 = (g70 | g65);
        long g72 = (g71 ^ 1L);
        long g73 = (g20 | g72);
        long g74 = (g73 ^ 1L);
        long g75 = (g48 ^ x0_2);
        long g76 = (g75 ^ 1L);
        long g77 = (g76 | g72);
        long g78 = (g77 ^ 1L);
        long g79 = (g76 | g20);
        long g80 = (g79 ^ 1L);
        long g81 = (g80 | g78);
        long g82 = (g81 | g74);
        long g83 = (g82 ^ 1L);
        long g84 = (g16 | g83);
        long g85 = (g84 ^ 1L);
        long g86 = (g49 ^ x0_3);
        long g87 = (g86 ^ 1L);
        long g88 = (g87 | g16);
        long g89 = (g88 ^ 1L);
        long g90 = (g87 | g83);
        long g91 = (g90 ^ 1L);
        long g92 = (g91 | g89);
        long g93 = (g92 | g85);
        long g94 = (g93 ^ 1L);
        long g95 = (g12 | g94);
        long g96 = (g95 ^ 1L);
        long g97 = (g50 ^ x0_4);
        long g98 = (g97 ^ 1L);
        long g99 = (g98 | g94);
        long g100 = (g99 ^ 1L);
        long g101 = (g98 | g12);
        long g102 = (g101 ^ 1L);
        long g103 = (g102 | g100);
        long g104 = (g103 | g96);
        long g105 = (g104 ^ 1L);
        long g106 = (g51 ^ x0_5);
        long g107 = (g106 ^ 1L);
        long g108 = (g107 | g105);
        long g109 = (g108 ^ 1L);
        long g110 = (g8 | g105);
        long g111 = (g110 ^ 1L);
        long g112 = (g107 | g8);
        long g113 = (g112 ^ 1L);
        long g114 = (g113 | g111);
        long g115 = (g114 | g109);
        long g116 = (g115 ^ 1L);
        long g117 = (g4 | g116);
        long g118 = (g117 ^ 1L);
        long g119 = (g52 ^ x0_6);
        long g120 = (g119 ^ 1L);
        long g121 = (g4 | g120);
        long g122 = (g121 ^ 1L);
        long g123 = (g116 | g120);
        long g124 = (g123 ^ 1L);
        long g125 = (g124 | g122);
        long g126 = (g125 | g118);
        long g127 = (g126 ^ 1L);
        long g128 = (g0 | g127);
        long g129 = (g128 ^ 1L);
        long g130 = (g127 | g58);
        long g131 = (g130 ^ 1L);
        long g132 = (g131 | g129);
        long g133 = (g132 | g60);
        long g134 = (x1_7 ^ g133);
        long g135 = (g134 ^ 1L);
        long g136 = (g135 ^ g56);
        long g137 = (g136 ^ 1L);
        long g138 = (x1_7 ^ g126);
        long g139 = (g138 ^ 1L);
        long g140 = (g139 ^ g58);
        long g141 = (g140 ^ 1L);
        long g142 = (g141 ^ g137);
        long g143 = (g142 ^ 1L);
        long g144 = (g141 ^ g143);
        long g145 = (g144 ^ 1L);
        long g146 = (g145 & g47);
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
        long w63 = cat(w62, g146, 1);
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
                    answers.Append(((ulong) emu_setg_gpr_one_8__reg_rdi__csharp(values[0], values[1], values[2])).ToString());
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
