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
    // one named local per gate, over the term of shr_cl_gpr_16__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 16, v0), LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1))))
    public static long emu_shr_cl_gpr_16__reg_rdi__csharp(long a, long b) {
        long x0_0 = ext(a, 0, 0);
        long x0_1 = ext(a, 1, 1);
        long x1_0 = ext(b, 0, 0);
        long x0_2 = ext(a, 2, 2);
        long x0_3 = ext(a, 3, 3);
        long x1_1 = ext(b, 1, 1);
        long x0_4 = ext(a, 4, 4);
        long x0_5 = ext(a, 5, 5);
        long x0_6 = ext(a, 6, 6);
        long x0_7 = ext(a, 7, 7);
        long x1_2 = ext(b, 2, 2);
        long x0_8 = ext(a, 8, 8);
        long x0_9 = ext(a, 9, 9);
        long x0_10 = ext(a, 10, 10);
        long x0_11 = ext(a, 11, 11);
        long x0_12 = ext(a, 12, 12);
        long x0_13 = ext(a, 13, 13);
        long x0_14 = ext(a, 14, 14);
        long x0_15 = ext(a, 15, 15);
        long x1_3 = ext(b, 3, 3);
        long x1_4 = ext(b, 4, 4);
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
        long g0 = (x1_0 ^ 1L);
        long g1 = (x1_0 & x0_1);
        long g2 = (g0 & x0_0);
        long g3 = (g1 | g2);
        long g4 = (x1_0 ^ 1L);
        long g5 = (x1_0 & x0_3);
        long g6 = (g4 & x0_2);
        long g7 = (g5 | g6);
        long g8 = (x1_1 ^ 1L);
        long g9 = (x1_1 & g7);
        long g10 = (g8 & g3);
        long g11 = (g9 | g10);
        long g12 = (x1_0 ^ 1L);
        long g13 = (x1_0 & x0_5);
        long g14 = (g12 & x0_4);
        long g15 = (g13 | g14);
        long g16 = (x1_0 ^ 1L);
        long g17 = (x1_0 & x0_7);
        long g18 = (g16 & x0_6);
        long g19 = (g17 | g18);
        long g20 = (x1_1 ^ 1L);
        long g21 = (x1_1 & g19);
        long g22 = (g20 & g15);
        long g23 = (g21 | g22);
        long g24 = (x1_2 ^ 1L);
        long g25 = (x1_2 & g23);
        long g26 = (g24 & g11);
        long g27 = (g25 | g26);
        long g28 = (x1_0 ^ 1L);
        long g29 = (x1_0 & x0_9);
        long g30 = (g28 & x0_8);
        long g31 = (g29 | g30);
        long g32 = (x1_0 ^ 1L);
        long g33 = (x1_0 & x0_11);
        long g34 = (g32 & x0_10);
        long g35 = (g33 | g34);
        long g36 = (x1_1 ^ 1L);
        long g37 = (x1_1 & g35);
        long g38 = (g36 & g31);
        long g39 = (g37 | g38);
        long g40 = (x1_0 ^ 1L);
        long g41 = (x1_0 & x0_13);
        long g42 = (g40 & x0_12);
        long g43 = (g41 | g42);
        long g44 = (x1_0 ^ 1L);
        long g45 = (x1_0 & x0_15);
        long g46 = (g44 & x0_14);
        long g47 = (g45 | g46);
        long g48 = (x1_1 ^ 1L);
        long g49 = (x1_1 & g47);
        long g50 = (g48 & g43);
        long g51 = (g49 | g50);
        long g52 = (x1_2 ^ 1L);
        long g53 = (x1_2 & g51);
        long g54 = (g52 & g39);
        long g55 = (g53 | g54);
        long g56 = (x1_3 ^ 1L);
        long g57 = (x1_3 & g55);
        long g58 = (g56 & g27);
        long g59 = (g57 | g58);
        long g60 = (x1_4 ^ 1L);
        long g61 = (g60 & g59);
        long g62 = (x1_0 ^ 1L);
        long g63 = (x1_0 & x0_2);
        long g64 = (g62 & x0_1);
        long g65 = (g63 | g64);
        long g66 = (x1_0 ^ 1L);
        long g67 = (x1_0 & x0_4);
        long g68 = (g66 & x0_3);
        long g69 = (g67 | g68);
        long g70 = (x1_1 ^ 1L);
        long g71 = (x1_1 & g69);
        long g72 = (g70 & g65);
        long g73 = (g71 | g72);
        long g74 = (x1_0 ^ 1L);
        long g75 = (x1_0 & x0_6);
        long g76 = (g74 & x0_5);
        long g77 = (g75 | g76);
        long g78 = (x1_0 ^ 1L);
        long g79 = (x1_0 & x0_8);
        long g80 = (g78 & x0_7);
        long g81 = (g79 | g80);
        long g82 = (x1_1 ^ 1L);
        long g83 = (x1_1 & g81);
        long g84 = (g82 & g77);
        long g85 = (g83 | g84);
        long g86 = (x1_2 ^ 1L);
        long g87 = (x1_2 & g85);
        long g88 = (g86 & g73);
        long g89 = (g87 | g88);
        long g90 = (x1_0 ^ 1L);
        long g91 = (x1_0 & x0_10);
        long g92 = (g90 & x0_9);
        long g93 = (g91 | g92);
        long g94 = (x1_0 ^ 1L);
        long g95 = (x1_0 & x0_12);
        long g96 = (g94 & x0_11);
        long g97 = (g95 | g96);
        long g98 = (x1_1 ^ 1L);
        long g99 = (x1_1 & g97);
        long g100 = (g98 & g93);
        long g101 = (g99 | g100);
        long g102 = (x1_0 ^ 1L);
        long g103 = (x1_0 & x0_14);
        long g104 = (g102 & x0_13);
        long g105 = (g103 | g104);
        long g106 = (x0_15 ^ 1L);
        long g107 = (x1_0 | g106);
        long g108 = (g107 ^ 1L);
        long g109 = (x1_1 ^ 1L);
        long g110 = (x1_1 & g108);
        long g111 = (g109 & g105);
        long g112 = (g110 | g111);
        long g113 = (x1_2 ^ 1L);
        long g114 = (x1_2 & g112);
        long g115 = (g113 & g101);
        long g116 = (g114 | g115);
        long g117 = (x1_3 ^ 1L);
        long g118 = (x1_3 & g116);
        long g119 = (g117 & g89);
        long g120 = (g118 | g119);
        long g121 = (g60 & g120);
        long g122 = (x1_1 ^ 1L);
        long g123 = (x1_1 & g15);
        long g124 = (g122 & g7);
        long g125 = (g123 | g124);
        long g126 = (x1_1 ^ 1L);
        long g127 = (x1_1 & g31);
        long g128 = (g126 & g19);
        long g129 = (g127 | g128);
        long g130 = (x1_2 ^ 1L);
        long g131 = (x1_2 & g129);
        long g132 = (g130 & g125);
        long g133 = (g131 | g132);
        long g134 = (x1_1 ^ 1L);
        long g135 = (x1_1 & g43);
        long g136 = (g134 & g35);
        long g137 = (g135 | g136);
        long g138 = (g47 ^ 1L);
        long g139 = (x1_1 | g138);
        long g140 = (g139 ^ 1L);
        long g141 = (x1_2 ^ 1L);
        long g142 = (x1_2 & g140);
        long g143 = (g141 & g137);
        long g144 = (g142 | g143);
        long g145 = (x1_3 ^ 1L);
        long g146 = (x1_3 & g144);
        long g147 = (g145 & g133);
        long g148 = (g146 | g147);
        long g149 = (g60 & g148);
        long g150 = (x1_1 ^ 1L);
        long g151 = (x1_1 & g77);
        long g152 = (g150 & g69);
        long g153 = (g151 | g152);
        long g154 = (x1_1 ^ 1L);
        long g155 = (x1_1 & g93);
        long g156 = (g154 & g81);
        long g157 = (g155 | g156);
        long g158 = (x1_2 ^ 1L);
        long g159 = (x1_2 & g157);
        long g160 = (g158 & g153);
        long g161 = (g159 | g160);
        long g162 = (x1_1 ^ 1L);
        long g163 = (x1_1 & g105);
        long g164 = (g162 & g97);
        long g165 = (g163 | g164);
        long g166 = (x1_1 | g107);
        long g167 = (g166 ^ 1L);
        long g168 = (x1_2 ^ 1L);
        long g169 = (x1_2 & g167);
        long g170 = (g168 & g165);
        long g171 = (g169 | g170);
        long g172 = (x1_3 ^ 1L);
        long g173 = (x1_3 & g171);
        long g174 = (g172 & g161);
        long g175 = (g173 | g174);
        long g176 = (g60 & g175);
        long g177 = (x1_2 ^ 1L);
        long g178 = (x1_2 & g39);
        long g179 = (g177 & g23);
        long g180 = (g178 | g179);
        long g181 = (g51 ^ 1L);
        long g182 = (x1_2 | g181);
        long g183 = (g182 ^ 1L);
        long g184 = (x1_3 ^ 1L);
        long g185 = (x1_3 & g183);
        long g186 = (g184 & g180);
        long g187 = (g185 | g186);
        long g188 = (g60 & g187);
        long g189 = (x1_2 ^ 1L);
        long g190 = (x1_2 & g101);
        long g191 = (g189 & g85);
        long g192 = (g190 | g191);
        long g193 = (g112 ^ 1L);
        long g194 = (x1_2 | g193);
        long g195 = (g194 ^ 1L);
        long g196 = (x1_3 ^ 1L);
        long g197 = (x1_3 & g195);
        long g198 = (g196 & g192);
        long g199 = (g197 | g198);
        long g200 = (g60 & g199);
        long g201 = (x1_2 ^ 1L);
        long g202 = (x1_2 & g137);
        long g203 = (g201 & g129);
        long g204 = (g202 | g203);
        long g205 = (x1_2 | g139);
        long g206 = (g205 ^ 1L);
        long g207 = (x1_3 ^ 1L);
        long g208 = (x1_3 & g206);
        long g209 = (g207 & g204);
        long g210 = (g208 | g209);
        long g211 = (g60 & g210);
        long g212 = (x1_2 ^ 1L);
        long g213 = (x1_2 & g165);
        long g214 = (g212 & g157);
        long g215 = (g213 | g214);
        long g216 = (x1_2 | g166);
        long g217 = (g216 ^ 1L);
        long g218 = (x1_3 ^ 1L);
        long g219 = (x1_3 & g217);
        long g220 = (g218 & g215);
        long g221 = (g219 | g220);
        long g222 = (g60 & g221);
        long g223 = (x1_3 ^ 1L);
        long g224 = (g60 & g223);
        long g225 = (g224 & g55);
        long g226 = (g60 & g223);
        long g227 = (g226 & g116);
        long g228 = (g60 & g223);
        long g229 = (g228 & g144);
        long g230 = (g60 & g223);
        long g231 = (g230 & g171);
        long g232 = (x1_2 ^ 1L);
        long g233 = (g60 & g223);
        long g234 = (g233 & g232);
        long g235 = (g234 & g51);
        long g236 = (g60 & g223);
        long g237 = (g236 & g232);
        long g238 = (g237 & g112);
        long g239 = (x1_1 ^ 1L);
        long g240 = (g60 & g223);
        long g241 = (g240 & g232);
        long g242 = (g241 & g239);
        long g243 = (g242 & g47);
        long g244 = (x1_0 ^ 1L);
        long g245 = (g60 & g223);
        long g246 = (g245 & g232);
        long g247 = (g246 & g239);
        long g248 = (g247 & g244);
        long g249 = (g248 & x0_15);
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
        long w48 = cat(w47, g249, 1);
        long w49 = cat(w48, g243, 1);
        long w50 = cat(w49, g238, 1);
        long w51 = cat(w50, g235, 1);
        long w52 = cat(w51, g231, 1);
        long w53 = cat(w52, g229, 1);
        long w54 = cat(w53, g227, 1);
        long w55 = cat(w54, g225, 1);
        long w56 = cat(w55, g222, 1);
        long w57 = cat(w56, g211, 1);
        long w58 = cat(w57, g200, 1);
        long w59 = cat(w58, g188, 1);
        long w60 = cat(w59, g176, 1);
        long w61 = cat(w60, g149, 1);
        long w62 = cat(w61, g121, 1);
        long w63 = cat(w62, g61, 1);
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
                    answers.Append(((ulong) emu_shr_cl_gpr_16__reg_rdi__csharp(values[0], values[1])).ToString());
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
