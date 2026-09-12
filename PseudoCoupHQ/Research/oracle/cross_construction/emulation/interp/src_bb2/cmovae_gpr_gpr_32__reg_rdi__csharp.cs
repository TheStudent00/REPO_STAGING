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
    // one named local per gate, over the term of cmovae_gpr_gpr_32__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(0, If(ULE(Extract(31, 0, v0), Extract(31, 0, v1)), Extract(31, 0, v2), Extract(31, 0, v3)))
    public static long emu_cmovae_gpr_gpr_32__reg_rdi__csharp(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
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
        long g0 = (x0_0 ^ 1L);
        long g1 = (g0 | x1_0);
        long g2 = (g1 ^ 1L);
        long g3 = (x1_1 ^ 1L);
        long g4 = (g3 | g2);
        long g5 = (g4 ^ 1L);
        long g6 = (x0_1 | g2);
        long g7 = (g6 ^ 1L);
        long g8 = (x0_1 | g3);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 | g7);
        long g11 = (g10 | g5);
        long g12 = (g11 ^ 1L);
        long g13 = (x1_2 ^ 1L);
        long g14 = (g13 | g12);
        long g15 = (g14 ^ 1L);
        long g16 = (x0_2 | g12);
        long g17 = (g16 ^ 1L);
        long g18 = (x0_2 | g13);
        long g19 = (g18 ^ 1L);
        long g20 = (g19 | g17);
        long g21 = (g20 | g15);
        long g22 = (g21 ^ 1L);
        long g23 = (x1_3 ^ 1L);
        long g24 = (g23 | g22);
        long g25 = (g24 ^ 1L);
        long g26 = (x0_3 | g22);
        long g27 = (g26 ^ 1L);
        long g28 = (x0_3 | g23);
        long g29 = (g28 ^ 1L);
        long g30 = (g29 | g27);
        long g31 = (g30 | g25);
        long g32 = (g31 ^ 1L);
        long g33 = (x1_4 ^ 1L);
        long g34 = (g33 | g32);
        long g35 = (g34 ^ 1L);
        long g36 = (x0_4 | g32);
        long g37 = (g36 ^ 1L);
        long g38 = (x0_4 | g33);
        long g39 = (g38 ^ 1L);
        long g40 = (g39 | g37);
        long g41 = (g40 | g35);
        long g42 = (g41 ^ 1L);
        long g43 = (x1_5 ^ 1L);
        long g44 = (g43 | g42);
        long g45 = (g44 ^ 1L);
        long g46 = (x0_5 | g42);
        long g47 = (g46 ^ 1L);
        long g48 = (x0_5 | g43);
        long g49 = (g48 ^ 1L);
        long g50 = (g49 | g47);
        long g51 = (g50 | g45);
        long g52 = (g51 ^ 1L);
        long g53 = (x1_6 ^ 1L);
        long g54 = (g53 | g52);
        long g55 = (g54 ^ 1L);
        long g56 = (x0_6 | g52);
        long g57 = (g56 ^ 1L);
        long g58 = (x0_6 | g53);
        long g59 = (g58 ^ 1L);
        long g60 = (g59 | g57);
        long g61 = (g60 | g55);
        long g62 = (g61 ^ 1L);
        long g63 = (x1_7 ^ 1L);
        long g64 = (g63 | g62);
        long g65 = (g64 ^ 1L);
        long g66 = (x0_7 | g62);
        long g67 = (g66 ^ 1L);
        long g68 = (x0_7 | g63);
        long g69 = (g68 ^ 1L);
        long g70 = (g69 | g67);
        long g71 = (g70 | g65);
        long g72 = (g71 ^ 1L);
        long g73 = (x1_8 ^ 1L);
        long g74 = (g73 | g72);
        long g75 = (g74 ^ 1L);
        long g76 = (x0_8 | g72);
        long g77 = (g76 ^ 1L);
        long g78 = (x0_8 | g73);
        long g79 = (g78 ^ 1L);
        long g80 = (g79 | g77);
        long g81 = (g80 | g75);
        long g82 = (g81 ^ 1L);
        long g83 = (x1_9 ^ 1L);
        long g84 = (g83 | g82);
        long g85 = (g84 ^ 1L);
        long g86 = (x0_9 | g82);
        long g87 = (g86 ^ 1L);
        long g88 = (x0_9 | g83);
        long g89 = (g88 ^ 1L);
        long g90 = (g89 | g87);
        long g91 = (g90 | g85);
        long g92 = (g91 ^ 1L);
        long g93 = (x1_10 ^ 1L);
        long g94 = (g93 | g92);
        long g95 = (g94 ^ 1L);
        long g96 = (x0_10 | g92);
        long g97 = (g96 ^ 1L);
        long g98 = (x0_10 | g93);
        long g99 = (g98 ^ 1L);
        long g100 = (g99 | g97);
        long g101 = (g100 | g95);
        long g102 = (g101 ^ 1L);
        long g103 = (x1_11 ^ 1L);
        long g104 = (g103 | g102);
        long g105 = (g104 ^ 1L);
        long g106 = (x0_11 | g102);
        long g107 = (g106 ^ 1L);
        long g108 = (x0_11 | g103);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 | g107);
        long g111 = (g110 | g105);
        long g112 = (g111 ^ 1L);
        long g113 = (x1_12 ^ 1L);
        long g114 = (g113 | g112);
        long g115 = (g114 ^ 1L);
        long g116 = (x0_12 | g112);
        long g117 = (g116 ^ 1L);
        long g118 = (x0_12 | g113);
        long g119 = (g118 ^ 1L);
        long g120 = (g119 | g117);
        long g121 = (g120 | g115);
        long g122 = (g121 ^ 1L);
        long g123 = (x1_13 ^ 1L);
        long g124 = (g123 | g122);
        long g125 = (g124 ^ 1L);
        long g126 = (x0_13 | g122);
        long g127 = (g126 ^ 1L);
        long g128 = (x0_13 | g123);
        long g129 = (g128 ^ 1L);
        long g130 = (g129 | g127);
        long g131 = (g130 | g125);
        long g132 = (g131 ^ 1L);
        long g133 = (x1_14 ^ 1L);
        long g134 = (g133 | g132);
        long g135 = (g134 ^ 1L);
        long g136 = (x0_14 | g132);
        long g137 = (g136 ^ 1L);
        long g138 = (x0_14 | g133);
        long g139 = (g138 ^ 1L);
        long g140 = (g139 | g137);
        long g141 = (g140 | g135);
        long g142 = (g141 ^ 1L);
        long g143 = (x1_15 ^ 1L);
        long g144 = (g143 | g142);
        long g145 = (g144 ^ 1L);
        long g146 = (x0_15 | g142);
        long g147 = (g146 ^ 1L);
        long g148 = (x0_15 | g143);
        long g149 = (g148 ^ 1L);
        long g150 = (g149 | g147);
        long g151 = (g150 | g145);
        long g152 = (g151 ^ 1L);
        long g153 = (x1_16 ^ 1L);
        long g154 = (g153 | g152);
        long g155 = (g154 ^ 1L);
        long g156 = (x0_16 | g152);
        long g157 = (g156 ^ 1L);
        long g158 = (x0_16 | g153);
        long g159 = (g158 ^ 1L);
        long g160 = (g159 | g157);
        long g161 = (g160 | g155);
        long g162 = (g161 ^ 1L);
        long g163 = (x1_17 ^ 1L);
        long g164 = (g163 | g162);
        long g165 = (g164 ^ 1L);
        long g166 = (x0_17 | g162);
        long g167 = (g166 ^ 1L);
        long g168 = (x0_17 | g163);
        long g169 = (g168 ^ 1L);
        long g170 = (g169 | g167);
        long g171 = (g170 | g165);
        long g172 = (g171 ^ 1L);
        long g173 = (x1_18 ^ 1L);
        long g174 = (g173 | g172);
        long g175 = (g174 ^ 1L);
        long g176 = (x0_18 | g172);
        long g177 = (g176 ^ 1L);
        long g178 = (x0_18 | g173);
        long g179 = (g178 ^ 1L);
        long g180 = (g179 | g177);
        long g181 = (g180 | g175);
        long g182 = (g181 ^ 1L);
        long g183 = (x1_19 ^ 1L);
        long g184 = (g183 | g182);
        long g185 = (g184 ^ 1L);
        long g186 = (x0_19 | g182);
        long g187 = (g186 ^ 1L);
        long g188 = (x0_19 | g183);
        long g189 = (g188 ^ 1L);
        long g190 = (g189 | g187);
        long g191 = (g190 | g185);
        long g192 = (g191 ^ 1L);
        long g193 = (x1_20 ^ 1L);
        long g194 = (g193 | g192);
        long g195 = (g194 ^ 1L);
        long g196 = (x0_20 | g192);
        long g197 = (g196 ^ 1L);
        long g198 = (x0_20 | g193);
        long g199 = (g198 ^ 1L);
        long g200 = (g199 | g197);
        long g201 = (g200 | g195);
        long g202 = (g201 ^ 1L);
        long g203 = (x1_21 ^ 1L);
        long g204 = (g203 | g202);
        long g205 = (g204 ^ 1L);
        long g206 = (x0_21 | g202);
        long g207 = (g206 ^ 1L);
        long g208 = (x0_21 | g203);
        long g209 = (g208 ^ 1L);
        long g210 = (g209 | g207);
        long g211 = (g210 | g205);
        long g212 = (g211 ^ 1L);
        long g213 = (x1_22 ^ 1L);
        long g214 = (g213 | g212);
        long g215 = (g214 ^ 1L);
        long g216 = (x0_22 | g212);
        long g217 = (g216 ^ 1L);
        long g218 = (x0_22 | g213);
        long g219 = (g218 ^ 1L);
        long g220 = (g219 | g217);
        long g221 = (g220 | g215);
        long g222 = (g221 ^ 1L);
        long g223 = (x1_23 ^ 1L);
        long g224 = (g223 | g222);
        long g225 = (g224 ^ 1L);
        long g226 = (x0_23 | g222);
        long g227 = (g226 ^ 1L);
        long g228 = (x0_23 | g223);
        long g229 = (g228 ^ 1L);
        long g230 = (g229 | g227);
        long g231 = (g230 | g225);
        long g232 = (g231 ^ 1L);
        long g233 = (x1_24 ^ 1L);
        long g234 = (g233 | g232);
        long g235 = (g234 ^ 1L);
        long g236 = (x0_24 | g232);
        long g237 = (g236 ^ 1L);
        long g238 = (x0_24 | g233);
        long g239 = (g238 ^ 1L);
        long g240 = (g239 | g237);
        long g241 = (g240 | g235);
        long g242 = (g241 ^ 1L);
        long g243 = (x1_25 ^ 1L);
        long g244 = (g243 | g242);
        long g245 = (g244 ^ 1L);
        long g246 = (x0_25 | g242);
        long g247 = (g246 ^ 1L);
        long g248 = (x0_25 | g243);
        long g249 = (g248 ^ 1L);
        long g250 = (g249 | g247);
        long g251 = (g250 | g245);
        long g252 = (g251 ^ 1L);
        long g253 = (x1_26 ^ 1L);
        long g254 = (g253 | g252);
        long g255 = (g254 ^ 1L);
        long g256 = (x0_26 | g252);
        long g257 = (g256 ^ 1L);
        long g258 = (x0_26 | g253);
        long g259 = (g258 ^ 1L);
        long g260 = (g259 | g257);
        long g261 = (g260 | g255);
        long g262 = (g261 ^ 1L);
        long g263 = (x1_27 ^ 1L);
        long g264 = (g263 | g262);
        long g265 = (g264 ^ 1L);
        long g266 = (x0_27 | g262);
        long g267 = (g266 ^ 1L);
        long g268 = (x0_27 | g263);
        long g269 = (g268 ^ 1L);
        long g270 = (g269 | g267);
        long g271 = (g270 | g265);
        long g272 = (g271 ^ 1L);
        long g273 = (x1_28 ^ 1L);
        long g274 = (g273 | g272);
        long g275 = (g274 ^ 1L);
        long g276 = (x0_28 | g272);
        long g277 = (g276 ^ 1L);
        long g278 = (x0_28 | g273);
        long g279 = (g278 ^ 1L);
        long g280 = (g279 | g277);
        long g281 = (g280 | g275);
        long g282 = (g281 ^ 1L);
        long g283 = (x1_29 ^ 1L);
        long g284 = (g283 | g282);
        long g285 = (g284 ^ 1L);
        long g286 = (x0_29 | g282);
        long g287 = (g286 ^ 1L);
        long g288 = (x0_29 | g283);
        long g289 = (g288 ^ 1L);
        long g290 = (g289 | g287);
        long g291 = (g290 | g285);
        long g292 = (g291 ^ 1L);
        long g293 = (x1_30 ^ 1L);
        long g294 = (g293 | g292);
        long g295 = (g294 ^ 1L);
        long g296 = (x0_30 | g292);
        long g297 = (g296 ^ 1L);
        long g298 = (x0_30 | g293);
        long g299 = (g298 ^ 1L);
        long g300 = (g299 | g297);
        long g301 = (g300 | g295);
        long g302 = (g301 ^ 1L);
        long g303 = (x1_31 ^ 1L);
        long g304 = (g303 | g302);
        long g305 = (g304 ^ 1L);
        long g306 = (x0_31 | g302);
        long g307 = (g306 ^ 1L);
        long g308 = (x0_31 | g303);
        long g309 = (g308 ^ 1L);
        long g310 = (g309 | g307);
        long g311 = (g310 | g305);
        long g312 = (g311 ^ 1L);
        long g313 = (g312 & x3_0);
        long g314 = (g311 & x2_0);
        long g315 = (g314 | g313);
        long g316 = (g312 & x3_1);
        long g317 = (g311 & x2_1);
        long g318 = (g317 | g316);
        long g319 = (g312 & x3_2);
        long g320 = (g311 & x2_2);
        long g321 = (g320 | g319);
        long g322 = (g312 & x3_3);
        long g323 = (g311 & x2_3);
        long g324 = (g323 | g322);
        long g325 = (g312 & x3_4);
        long g326 = (g311 & x2_4);
        long g327 = (g326 | g325);
        long g328 = (g312 & x3_5);
        long g329 = (g311 & x2_5);
        long g330 = (g329 | g328);
        long g331 = (g312 & x3_6);
        long g332 = (g311 & x2_6);
        long g333 = (g332 | g331);
        long g334 = (g312 & x3_7);
        long g335 = (g311 & x2_7);
        long g336 = (g335 | g334);
        long g337 = (g312 & x3_8);
        long g338 = (g311 & x2_8);
        long g339 = (g338 | g337);
        long g340 = (g312 & x3_9);
        long g341 = (g311 & x2_9);
        long g342 = (g341 | g340);
        long g343 = (g312 & x3_10);
        long g344 = (g311 & x2_10);
        long g345 = (g344 | g343);
        long g346 = (g312 & x3_11);
        long g347 = (g311 & x2_11);
        long g348 = (g347 | g346);
        long g349 = (g312 & x3_12);
        long g350 = (g311 & x2_12);
        long g351 = (g350 | g349);
        long g352 = (g312 & x3_13);
        long g353 = (g311 & x2_13);
        long g354 = (g353 | g352);
        long g355 = (g312 & x3_14);
        long g356 = (g311 & x2_14);
        long g357 = (g356 | g355);
        long g358 = (g312 & x3_15);
        long g359 = (g311 & x2_15);
        long g360 = (g359 | g358);
        long g361 = (g312 & x3_16);
        long g362 = (g311 & x2_16);
        long g363 = (g362 | g361);
        long g364 = (g312 & x3_17);
        long g365 = (g311 & x2_17);
        long g366 = (g365 | g364);
        long g367 = (g312 & x3_18);
        long g368 = (g311 & x2_18);
        long g369 = (g368 | g367);
        long g370 = (g312 & x3_19);
        long g371 = (g311 & x2_19);
        long g372 = (g371 | g370);
        long g373 = (g312 & x3_20);
        long g374 = (g311 & x2_20);
        long g375 = (g374 | g373);
        long g376 = (g312 & x3_21);
        long g377 = (g311 & x2_21);
        long g378 = (g377 | g376);
        long g379 = (g312 & x3_22);
        long g380 = (g311 & x2_22);
        long g381 = (g380 | g379);
        long g382 = (g312 & x3_23);
        long g383 = (g311 & x2_23);
        long g384 = (g383 | g382);
        long g385 = (g312 & x3_24);
        long g386 = (g311 & x2_24);
        long g387 = (g386 | g385);
        long g388 = (g312 & x3_25);
        long g389 = (g311 & x2_25);
        long g390 = (g389 | g388);
        long g391 = (g312 & x3_26);
        long g392 = (g311 & x2_26);
        long g393 = (g392 | g391);
        long g394 = (g312 & x3_27);
        long g395 = (g311 & x2_27);
        long g396 = (g395 | g394);
        long g397 = (g312 & x3_28);
        long g398 = (g311 & x2_28);
        long g399 = (g398 | g397);
        long g400 = (g312 & x3_29);
        long g401 = (g311 & x2_29);
        long g402 = (g401 | g400);
        long g403 = (g312 & x3_30);
        long g404 = (g311 & x2_30);
        long g405 = (g404 | g403);
        long g406 = (g312 & x3_31);
        long g407 = (g311 & x2_31);
        long g408 = (g407 | g406);
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
        long w32 = cat(w31, g408, 1);
        long w33 = cat(w32, g405, 1);
        long w34 = cat(w33, g402, 1);
        long w35 = cat(w34, g399, 1);
        long w36 = cat(w35, g396, 1);
        long w37 = cat(w36, g393, 1);
        long w38 = cat(w37, g390, 1);
        long w39 = cat(w38, g387, 1);
        long w40 = cat(w39, g384, 1);
        long w41 = cat(w40, g381, 1);
        long w42 = cat(w41, g378, 1);
        long w43 = cat(w42, g375, 1);
        long w44 = cat(w43, g372, 1);
        long w45 = cat(w44, g369, 1);
        long w46 = cat(w45, g366, 1);
        long w47 = cat(w46, g363, 1);
        long w48 = cat(w47, g360, 1);
        long w49 = cat(w48, g357, 1);
        long w50 = cat(w49, g354, 1);
        long w51 = cat(w50, g351, 1);
        long w52 = cat(w51, g348, 1);
        long w53 = cat(w52, g345, 1);
        long w54 = cat(w53, g342, 1);
        long w55 = cat(w54, g339, 1);
        long w56 = cat(w55, g336, 1);
        long w57 = cat(w56, g333, 1);
        long w58 = cat(w57, g330, 1);
        long w59 = cat(w58, g327, 1);
        long w60 = cat(w59, g324, 1);
        long w61 = cat(w60, g321, 1);
        long w62 = cat(w61, g318, 1);
        long w63 = cat(w62, g315, 1);
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
                    answers.Append(((ulong) emu_cmovae_gpr_gpr_32__reg_rdi__csharp(values[0], values[1], values[2], values[3])).ToString());
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
