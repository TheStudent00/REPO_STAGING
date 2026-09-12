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
    // one named local per gate, over the term of cmovge_gpr_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(Extract(31, 31, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1)) == If(Extract(31, 31, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))) == Extract(32, 32, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))), 0, 1), Extract(31, 0, v2), Extract(31, 0, v3)))
    public static long emu_cmovge_gpr_gpr_32__reg_rdi__csharp(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
        long x0_31 = ext(b, 31, 31);
        long x0_0 = ext(b, 0, 0);
        long x0_1 = ext(b, 1, 1);
        long x0_2 = ext(b, 2, 2);
        long x0_3 = ext(b, 3, 3);
        long x0_4 = ext(b, 4, 4);
        long x0_5 = ext(b, 5, 5);
        long x0_6 = ext(b, 6, 6);
        long x0_7 = ext(b, 7, 7);
        long x0_8 = ext(b, 8, 8);
        long x0_9 = ext(b, 9, 9);
        long x0_10 = ext(b, 10, 10);
        long x0_11 = ext(b, 11, 11);
        long x0_12 = ext(b, 12, 12);
        long x0_13 = ext(b, 13, 13);
        long x0_14 = ext(b, 14, 14);
        long x0_15 = ext(b, 15, 15);
        long x0_16 = ext(b, 16, 16);
        long x0_17 = ext(b, 17, 17);
        long x0_18 = ext(b, 18, 18);
        long x0_19 = ext(b, 19, 19);
        long x0_20 = ext(b, 20, 20);
        long x0_21 = ext(b, 21, 21);
        long x0_22 = ext(b, 22, 22);
        long x0_23 = ext(b, 23, 23);
        long x0_24 = ext(b, 24, 24);
        long x0_25 = ext(b, 25, 25);
        long x0_26 = ext(b, 26, 26);
        long x0_27 = ext(b, 27, 27);
        long x0_28 = ext(b, 28, 28);
        long x0_29 = ext(b, 29, 29);
        long x0_30 = ext(b, 30, 30);
        long x1_25 = ext(a, 25, 25);
        long x1_23 = ext(a, 23, 23);
        long x1_22 = ext(a, 22, 22);
        long x1_19 = ext(a, 19, 19);
        long x1_18 = ext(a, 18, 18);
        long x1_16 = ext(a, 16, 16);
        long x1_13 = ext(a, 13, 13);
        long x1_11 = ext(a, 11, 11);
        long x1_10 = ext(a, 10, 10);
        long x1_8 = ext(a, 8, 8);
        long x1_0 = ext(a, 0, 0);
        long x1_1 = ext(a, 1, 1);
        long x1_2 = ext(a, 2, 2);
        long x1_3 = ext(a, 3, 3);
        long x1_4 = ext(a, 4, 4);
        long x1_5 = ext(a, 5, 5);
        long x1_6 = ext(a, 6, 6);
        long x1_7 = ext(a, 7, 7);
        long x1_9 = ext(a, 9, 9);
        long x1_12 = ext(a, 12, 12);
        long x1_14 = ext(a, 14, 14);
        long x1_15 = ext(a, 15, 15);
        long x1_17 = ext(a, 17, 17);
        long x1_20 = ext(a, 20, 20);
        long x1_21 = ext(a, 21, 21);
        long x1_24 = ext(a, 24, 24);
        long x1_26 = ext(a, 26, 26);
        long x1_27 = ext(a, 27, 27);
        long x1_28 = ext(a, 28, 28);
        long x1_29 = ext(a, 29, 29);
        long x1_30 = ext(a, 30, 30);
        long x1_31 = ext(a, 31, 31);
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
        long g0 = (x0_1 | x0_0);
        long g1 = (x0_2 | g0);
        long g2 = (x0_3 | g1);
        long g3 = (x0_4 | g2);
        long g4 = (x0_5 | g3);
        long g5 = (x0_6 | g4);
        long g6 = (x0_7 | g5);
        long g7 = (x0_8 | g6);
        long g8 = (x0_9 | g7);
        long g9 = (x0_10 | g8);
        long g10 = (x0_11 | g9);
        long g11 = (x0_12 | g10);
        long g12 = (x0_13 | g11);
        long g13 = (x0_14 | g12);
        long g14 = (x0_15 | g13);
        long g15 = (x0_16 | g14);
        long g16 = (x0_17 | g15);
        long g17 = (x0_18 | g16);
        long g18 = (x0_19 | g17);
        long g19 = (x0_20 | g18);
        long g20 = (x0_21 | g19);
        long g21 = (x0_22 | g20);
        long g22 = (x0_23 | g21);
        long g23 = (x0_24 | g22);
        long g24 = (x0_25 | g23);
        long g25 = (x0_26 | g24);
        long g26 = (x0_27 | g25);
        long g27 = (x0_28 | g26);
        long g28 = (x0_29 | g27);
        long g29 = (x0_30 | g28);
        long g30 = (x0_31 | g29);
        long g31 = (g30 ^ x0_31);
        long g32 = (g31 ^ 1L);
        long g33 = (g25 ^ x0_27);
        long g34 = (g33 ^ 1L);
        long g35 = (g24 ^ x0_26);
        long g36 = (g35 ^ 1L);
        long g37 = (g23 ^ x0_25);
        long g38 = (g37 ^ 1L);
        long g39 = (x1_25 ^ 1L);
        long g40 = (g39 | g38);
        long g41 = (g40 ^ 1L);
        long g42 = (g22 ^ x0_24);
        long g43 = (g42 ^ 1L);
        long g44 = (g21 ^ x0_23);
        long g45 = (g44 ^ 1L);
        long g46 = (x1_23 ^ 1L);
        long g47 = (g46 | g45);
        long g48 = (g47 ^ 1L);
        long g49 = (x1_22 ^ 1L);
        long g50 = (g20 ^ x0_22);
        long g51 = (g50 ^ 1L);
        long g52 = (g51 | g49);
        long g53 = (g52 ^ 1L);
        long g54 = (g18 ^ x0_20);
        long g55 = (g54 ^ 1L);
        long g56 = (x1_19 ^ 1L);
        long g57 = (g17 ^ x0_19);
        long g58 = (g57 ^ 1L);
        long g59 = (g58 | g56);
        long g60 = (g59 ^ 1L);
        long g61 = (g16 ^ x0_18);
        long g62 = (g61 ^ 1L);
        long g63 = (x1_18 ^ 1L);
        long g64 = (g63 | g62);
        long g65 = (g64 ^ 1L);
        long g66 = (g15 ^ x0_17);
        long g67 = (g66 ^ 1L);
        long g68 = (x1_16 ^ 1L);
        long g69 = (g14 ^ x0_16);
        long g70 = (g69 ^ 1L);
        long g71 = (g70 | g68);
        long g72 = (g71 ^ 1L);
        long g73 = (g12 ^ x0_14);
        long g74 = (g73 ^ 1L);
        long g75 = (g11 ^ x0_13);
        long g76 = (g75 ^ 1L);
        long g77 = (x1_13 ^ 1L);
        long g78 = (g77 | g76);
        long g79 = (g78 ^ 1L);
        long g80 = (g9 ^ x0_11);
        long g81 = (g80 ^ 1L);
        long g82 = (x1_11 ^ 1L);
        long g83 = (g82 | g81);
        long g84 = (g83 ^ 1L);
        long g85 = (x1_10 ^ 1L);
        long g86 = (g8 ^ x0_10);
        long g87 = (g86 ^ 1L);
        long g88 = (g87 | g85);
        long g89 = (g88 ^ 1L);
        long g90 = (x1_8 ^ 1L);
        long g91 = (g6 ^ x0_8);
        long g92 = (g91 ^ 1L);
        long g93 = (g92 | g90);
        long g94 = (g93 ^ 1L);
        long g95 = (g4 ^ x0_6);
        long g96 = (g95 ^ 1L);
        long g97 = (g0 ^ x0_2);
        long g98 = (g97 ^ 1L);
        long g99 = (x1_0 ^ 1L);
        long g100 = (x0_0 ^ 1L);
        long g101 = (g100 | g99);
        long g102 = (x1_1 ^ 1L);
        long g103 = (g102 | g101);
        long g104 = (g103 ^ 1L);
        long g105 = (x0_0 ^ x0_1);
        long g106 = (g105 ^ 1L);
        long g107 = (g106 | g101);
        long g108 = (g107 ^ 1L);
        long g109 = (g102 | g106);
        long g110 = (g109 ^ 1L);
        long g111 = (g110 | g108);
        long g112 = (g111 | g104);
        long g113 = (g112 ^ 1L);
        long g114 = (g113 | g98);
        long g115 = (g114 ^ 1L);
        long g116 = (x1_2 ^ 1L);
        long g117 = (g98 | g116);
        long g118 = (g117 ^ 1L);
        long g119 = (g116 | g113);
        long g120 = (g119 ^ 1L);
        long g121 = (g120 | g118);
        long g122 = (g121 | g115);
        long g123 = (g122 ^ 1L);
        long g124 = (x1_3 ^ 1L);
        long g125 = (g124 | g123);
        long g126 = (g125 ^ 1L);
        long g127 = (g1 ^ x0_3);
        long g128 = (g127 ^ 1L);
        long g129 = (g124 | g128);
        long g130 = (g129 ^ 1L);
        long g131 = (g123 | g128);
        long g132 = (g131 ^ 1L);
        long g133 = (g132 | g130);
        long g134 = (g133 | g126);
        long g135 = (g134 ^ 1L);
        long g136 = (x1_4 ^ 1L);
        long g137 = (g136 | g135);
        long g138 = (g137 ^ 1L);
        long g139 = (g2 ^ x0_4);
        long g140 = (g139 ^ 1L);
        long g141 = (g136 | g140);
        long g142 = (g141 ^ 1L);
        long g143 = (g135 | g140);
        long g144 = (g143 ^ 1L);
        long g145 = (g144 | g142);
        long g146 = (g145 | g138);
        long g147 = (g146 ^ 1L);
        long g148 = (g3 ^ x0_5);
        long g149 = (g148 ^ 1L);
        long g150 = (g149 | g147);
        long g151 = (g150 ^ 1L);
        long g152 = (x1_5 ^ 1L);
        long g153 = (g152 | g149);
        long g154 = (g153 ^ 1L);
        long g155 = (g152 | g147);
        long g156 = (g155 ^ 1L);
        long g157 = (g156 | g154);
        long g158 = (g157 | g151);
        long g159 = (g158 ^ 1L);
        long g160 = (g159 | g96);
        long g161 = (g160 ^ 1L);
        long g162 = (x1_6 ^ 1L);
        long g163 = (g162 | g159);
        long g164 = (g163 ^ 1L);
        long g165 = (g162 | g96);
        long g166 = (g165 ^ 1L);
        long g167 = (g166 | g164);
        long g168 = (g167 | g161);
        long g169 = (g168 ^ 1L);
        long g170 = (g5 ^ x0_7);
        long g171 = (g170 ^ 1L);
        long g172 = (g171 | g169);
        long g173 = (g172 ^ 1L);
        long g174 = (x1_7 ^ 1L);
        long g175 = (g171 | g174);
        long g176 = (g175 ^ 1L);
        long g177 = (g174 | g169);
        long g178 = (g177 ^ 1L);
        long g179 = (g178 | g176);
        long g180 = (g179 | g173);
        long g181 = (g180 ^ 1L);
        long g182 = (g90 | g181);
        long g183 = (g182 ^ 1L);
        long g184 = (g92 | g181);
        long g185 = (g184 ^ 1L);
        long g186 = (g185 | g183);
        long g187 = (g186 | g94);
        long g188 = (g187 ^ 1L);
        long g189 = (g7 ^ x0_9);
        long g190 = (g189 ^ 1L);
        long g191 = (g190 | g188);
        long g192 = (g191 ^ 1L);
        long g193 = (x1_9 ^ 1L);
        long g194 = (g193 | g188);
        long g195 = (g194 ^ 1L);
        long g196 = (g190 | g193);
        long g197 = (g196 ^ 1L);
        long g198 = (g197 | g195);
        long g199 = (g198 | g192);
        long g200 = (g199 ^ 1L);
        long g201 = (g85 | g200);
        long g202 = (g201 ^ 1L);
        long g203 = (g87 | g200);
        long g204 = (g203 ^ 1L);
        long g205 = (g204 | g202);
        long g206 = (g205 | g89);
        long g207 = (g206 ^ 1L);
        long g208 = (g82 | g207);
        long g209 = (g208 ^ 1L);
        long g210 = (g207 | g81);
        long g211 = (g210 ^ 1L);
        long g212 = (g211 | g209);
        long g213 = (g212 | g84);
        long g214 = (g213 ^ 1L);
        long g215 = (x1_12 ^ 1L);
        long g216 = (g215 | g214);
        long g217 = (g216 ^ 1L);
        long g218 = (g10 ^ x0_12);
        long g219 = (g218 ^ 1L);
        long g220 = (g219 | g215);
        long g221 = (g220 ^ 1L);
        long g222 = (g219 | g214);
        long g223 = (g222 ^ 1L);
        long g224 = (g223 | g221);
        long g225 = (g224 | g217);
        long g226 = (g225 ^ 1L);
        long g227 = (g226 | g76);
        long g228 = (g227 ^ 1L);
        long g229 = (g77 | g226);
        long g230 = (g229 ^ 1L);
        long g231 = (g230 | g228);
        long g232 = (g231 | g79);
        long g233 = (g232 ^ 1L);
        long g234 = (g233 | g74);
        long g235 = (g234 ^ 1L);
        long g236 = (x1_14 ^ 1L);
        long g237 = (g236 | g74);
        long g238 = (g237 ^ 1L);
        long g239 = (g236 | g233);
        long g240 = (g239 ^ 1L);
        long g241 = (g240 | g238);
        long g242 = (g241 | g235);
        long g243 = (g242 ^ 1L);
        long g244 = (g13 ^ x0_15);
        long g245 = (g244 ^ 1L);
        long g246 = (g245 | g243);
        long g247 = (g246 ^ 1L);
        long g248 = (x1_15 ^ 1L);
        long g249 = (g248 | g243);
        long g250 = (g249 ^ 1L);
        long g251 = (g245 | g248);
        long g252 = (g251 ^ 1L);
        long g253 = (g252 | g250);
        long g254 = (g253 | g247);
        long g255 = (g254 ^ 1L);
        long g256 = (g68 | g255);
        long g257 = (g256 ^ 1L);
        long g258 = (g255 | g70);
        long g259 = (g258 ^ 1L);
        long g260 = (g259 | g257);
        long g261 = (g260 | g72);
        long g262 = (g261 ^ 1L);
        long g263 = (g262 | g67);
        long g264 = (g263 ^ 1L);
        long g265 = (x1_17 ^ 1L);
        long g266 = (g265 | g262);
        long g267 = (g266 ^ 1L);
        long g268 = (g265 | g67);
        long g269 = (g268 ^ 1L);
        long g270 = (g269 | g267);
        long g271 = (g270 | g264);
        long g272 = (g271 ^ 1L);
        long g273 = (g62 | g272);
        long g274 = (g273 ^ 1L);
        long g275 = (g63 | g272);
        long g276 = (g275 ^ 1L);
        long g277 = (g276 | g274);
        long g278 = (g277 | g65);
        long g279 = (g278 ^ 1L);
        long g280 = (g58 | g279);
        long g281 = (g280 ^ 1L);
        long g282 = (g56 | g279);
        long g283 = (g282 ^ 1L);
        long g284 = (g283 | g281);
        long g285 = (g284 | g60);
        long g286 = (g285 ^ 1L);
        long g287 = (g286 | g55);
        long g288 = (g287 ^ 1L);
        long g289 = (x1_20 ^ 1L);
        long g290 = (g289 | g55);
        long g291 = (g290 ^ 1L);
        long g292 = (g289 | g286);
        long g293 = (g292 ^ 1L);
        long g294 = (g293 | g291);
        long g295 = (g294 | g288);
        long g296 = (g295 ^ 1L);
        long g297 = (x1_21 ^ 1L);
        long g298 = (g297 | g296);
        long g299 = (g298 ^ 1L);
        long g300 = (g19 ^ x0_21);
        long g301 = (g300 ^ 1L);
        long g302 = (g296 | g301);
        long g303 = (g302 ^ 1L);
        long g304 = (g297 | g301);
        long g305 = (g304 ^ 1L);
        long g306 = (g305 | g303);
        long g307 = (g306 | g299);
        long g308 = (g307 ^ 1L);
        long g309 = (g49 | g308);
        long g310 = (g309 ^ 1L);
        long g311 = (g51 | g308);
        long g312 = (g311 ^ 1L);
        long g313 = (g312 | g310);
        long g314 = (g313 | g53);
        long g315 = (g314 ^ 1L);
        long g316 = (g315 | g45);
        long g317 = (g316 ^ 1L);
        long g318 = (g46 | g315);
        long g319 = (g318 ^ 1L);
        long g320 = (g319 | g317);
        long g321 = (g320 | g48);
        long g322 = (g321 ^ 1L);
        long g323 = (g322 | g43);
        long g324 = (g323 ^ 1L);
        long g325 = (x1_24 ^ 1L);
        long g326 = (g325 | g322);
        long g327 = (g326 ^ 1L);
        long g328 = (g325 | g43);
        long g329 = (g328 ^ 1L);
        long g330 = (g329 | g327);
        long g331 = (g330 | g324);
        long g332 = (g331 ^ 1L);
        long g333 = (g39 | g332);
        long g334 = (g333 ^ 1L);
        long g335 = (g332 | g38);
        long g336 = (g335 ^ 1L);
        long g337 = (g336 | g334);
        long g338 = (g337 | g41);
        long g339 = (g338 ^ 1L);
        long g340 = (g339 | g36);
        long g341 = (g340 ^ 1L);
        long g342 = (x1_26 ^ 1L);
        long g343 = (g342 | g36);
        long g344 = (g343 ^ 1L);
        long g345 = (g342 | g339);
        long g346 = (g345 ^ 1L);
        long g347 = (g346 | g344);
        long g348 = (g347 | g341);
        long g349 = (g348 ^ 1L);
        long g350 = (g349 | g34);
        long g351 = (g350 ^ 1L);
        long g352 = (x1_27 ^ 1L);
        long g353 = (g34 | g352);
        long g354 = (g353 ^ 1L);
        long g355 = (g352 | g349);
        long g356 = (g355 ^ 1L);
        long g357 = (g356 | g354);
        long g358 = (g357 | g351);
        long g359 = (g358 ^ 1L);
        long g360 = (g26 ^ x0_28);
        long g361 = (g360 ^ 1L);
        long g362 = (g361 | g359);
        long g363 = (g362 ^ 1L);
        long g364 = (x1_28 ^ 1L);
        long g365 = (g364 | g359);
        long g366 = (g365 ^ 1L);
        long g367 = (g361 | g364);
        long g368 = (g367 ^ 1L);
        long g369 = (g368 | g366);
        long g370 = (g369 | g363);
        long g371 = (g370 ^ 1L);
        long g372 = (g27 ^ x0_29);
        long g373 = (g372 ^ 1L);
        long g374 = (g373 | g371);
        long g375 = (g374 ^ 1L);
        long g376 = (x1_29 ^ 1L);
        long g377 = (g376 | g371);
        long g378 = (g377 ^ 1L);
        long g379 = (g373 | g376);
        long g380 = (g379 ^ 1L);
        long g381 = (g380 | g378);
        long g382 = (g381 | g375);
        long g383 = (g382 ^ 1L);
        long g384 = (g28 ^ x0_30);
        long g385 = (g384 ^ 1L);
        long g386 = (g385 | g383);
        long g387 = (g386 ^ 1L);
        long g388 = (x1_30 ^ 1L);
        long g389 = (g385 | g388);
        long g390 = (g389 ^ 1L);
        long g391 = (g388 | g383);
        long g392 = (g391 ^ 1L);
        long g393 = (g392 | g390);
        long g394 = (g393 | g387);
        long g395 = (g394 ^ 1L);
        long g396 = (x1_31 ^ 1L);
        long g397 = (g396 | g395);
        long g398 = (g397 ^ 1L);
        long g399 = (g29 ^ x0_31);
        long g400 = (g399 ^ 1L);
        long g401 = (g400 | g396);
        long g402 = (g401 ^ 1L);
        long g403 = (g395 | g400);
        long g404 = (g403 ^ 1L);
        long g405 = (g404 | g402);
        long g406 = (g405 | g398);
        long g407 = (x1_31 ^ g406);
        long g408 = (g407 ^ 1L);
        long g409 = (g408 ^ g32);
        long g410 = (g409 ^ 1L);
        long g411 = (x1_31 ^ g394);
        long g412 = (g411 ^ 1L);
        long g413 = (g412 ^ g400);
        long g414 = (g413 ^ 1L);
        long g415 = (g414 ^ g410);
        long g416 = (g415 ^ 1L);
        long g417 = (g414 ^ g416);
        long g418 = (g417 ^ 1L);
        long g419 = (g418 ^ 1L);
        long g420 = (g419 & x3_0);
        long g421 = (g418 & x2_0);
        long g422 = (g421 | g420);
        long g423 = (g419 & x3_1);
        long g424 = (g418 & x2_1);
        long g425 = (g424 | g423);
        long g426 = (g419 & x3_2);
        long g427 = (g418 & x2_2);
        long g428 = (g427 | g426);
        long g429 = (g419 & x3_3);
        long g430 = (g418 & x2_3);
        long g431 = (g430 | g429);
        long g432 = (g419 & x3_4);
        long g433 = (g418 & x2_4);
        long g434 = (g433 | g432);
        long g435 = (g419 & x3_5);
        long g436 = (g418 & x2_5);
        long g437 = (g436 | g435);
        long g438 = (g419 & x3_6);
        long g439 = (g418 & x2_6);
        long g440 = (g439 | g438);
        long g441 = (g419 & x3_7);
        long g442 = (g418 & x2_7);
        long g443 = (g442 | g441);
        long g444 = (g419 & x3_8);
        long g445 = (g418 & x2_8);
        long g446 = (g445 | g444);
        long g447 = (g419 & x3_9);
        long g448 = (g418 & x2_9);
        long g449 = (g448 | g447);
        long g450 = (g419 & x3_10);
        long g451 = (g418 & x2_10);
        long g452 = (g451 | g450);
        long g453 = (g419 & x3_11);
        long g454 = (g418 & x2_11);
        long g455 = (g454 | g453);
        long g456 = (g419 & x3_12);
        long g457 = (g418 & x2_12);
        long g458 = (g457 | g456);
        long g459 = (g419 & x3_13);
        long g460 = (g418 & x2_13);
        long g461 = (g460 | g459);
        long g462 = (g419 & x3_14);
        long g463 = (g418 & x2_14);
        long g464 = (g463 | g462);
        long g465 = (g419 & x3_15);
        long g466 = (g418 & x2_15);
        long g467 = (g466 | g465);
        long g468 = (g419 & x3_16);
        long g469 = (g418 & x2_16);
        long g470 = (g469 | g468);
        long g471 = (g419 & x3_17);
        long g472 = (g418 & x2_17);
        long g473 = (g472 | g471);
        long g474 = (g419 & x3_18);
        long g475 = (g418 & x2_18);
        long g476 = (g475 | g474);
        long g477 = (g419 & x3_19);
        long g478 = (g418 & x2_19);
        long g479 = (g478 | g477);
        long g480 = (g419 & x3_20);
        long g481 = (g418 & x2_20);
        long g482 = (g481 | g480);
        long g483 = (g419 & x3_21);
        long g484 = (g418 & x2_21);
        long g485 = (g484 | g483);
        long g486 = (g419 & x3_22);
        long g487 = (g418 & x2_22);
        long g488 = (g487 | g486);
        long g489 = (g419 & x3_23);
        long g490 = (g418 & x2_23);
        long g491 = (g490 | g489);
        long g492 = (g419 & x3_24);
        long g493 = (g418 & x2_24);
        long g494 = (g493 | g492);
        long g495 = (g419 & x3_25);
        long g496 = (g418 & x2_25);
        long g497 = (g496 | g495);
        long g498 = (g419 & x3_26);
        long g499 = (g418 & x2_26);
        long g500 = (g499 | g498);
        long g501 = (g419 & x3_27);
        long g502 = (g418 & x2_27);
        long g503 = (g502 | g501);
        long g504 = (g419 & x3_28);
        long g505 = (g418 & x2_28);
        long g506 = (g505 | g504);
        long g507 = (g419 & x3_29);
        long g508 = (g418 & x2_29);
        long g509 = (g508 | g507);
        long g510 = (g419 & x3_30);
        long g511 = (g418 & x2_30);
        long g512 = (g511 | g510);
        long g513 = (g419 & x3_31);
        long g514 = (g418 & x2_31);
        long g515 = (g514 | g513);
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
        long w32 = cat(w31, g515, 1);
        long w33 = cat(w32, g512, 1);
        long w34 = cat(w33, g509, 1);
        long w35 = cat(w34, g506, 1);
        long w36 = cat(w35, g503, 1);
        long w37 = cat(w36, g500, 1);
        long w38 = cat(w37, g497, 1);
        long w39 = cat(w38, g494, 1);
        long w40 = cat(w39, g491, 1);
        long w41 = cat(w40, g488, 1);
        long w42 = cat(w41, g485, 1);
        long w43 = cat(w42, g482, 1);
        long w44 = cat(w43, g479, 1);
        long w45 = cat(w44, g476, 1);
        long w46 = cat(w45, g473, 1);
        long w47 = cat(w46, g470, 1);
        long w48 = cat(w47, g467, 1);
        long w49 = cat(w48, g464, 1);
        long w50 = cat(w49, g461, 1);
        long w51 = cat(w50, g458, 1);
        long w52 = cat(w51, g455, 1);
        long w53 = cat(w52, g452, 1);
        long w54 = cat(w53, g449, 1);
        long w55 = cat(w54, g446, 1);
        long w56 = cat(w55, g443, 1);
        long w57 = cat(w56, g440, 1);
        long w58 = cat(w57, g437, 1);
        long w59 = cat(w58, g434, 1);
        long w60 = cat(w59, g431, 1);
        long w61 = cat(w60, g428, 1);
        long w62 = cat(w61, g425, 1);
        long w63 = cat(w62, g422, 1);
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
                    answers.Append(((ulong) emu_cmovge_gpr_gpr_32__reg_rdi__csharp(values[0], values[1], values[2], values[3])).ToString());
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
