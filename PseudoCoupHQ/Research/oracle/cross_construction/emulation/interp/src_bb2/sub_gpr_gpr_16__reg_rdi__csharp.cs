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
    // one named local per gate, over the term of sub_gpr_gpr_16__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 16, v0), Extract(15, 0, v1)*65535 + Extract(15, 0, v0))
    public static long emu_sub_gpr_gpr_16__reg_rdi__csharp(long a, long b) {
        long x0_0 = ext(a, 0, 0);
        long x1_0 = ext(b, 0, 0);
        long x0_1 = ext(a, 1, 1);
        long x1_1 = ext(b, 1, 1);
        long x1_2 = ext(b, 2, 2);
        long x0_2 = ext(a, 2, 2);
        long x1_3 = ext(b, 3, 3);
        long x0_3 = ext(a, 3, 3);
        long x1_4 = ext(b, 4, 4);
        long x0_4 = ext(a, 4, 4);
        long x1_5 = ext(b, 5, 5);
        long x0_5 = ext(a, 5, 5);
        long x1_6 = ext(b, 6, 6);
        long x0_6 = ext(a, 6, 6);
        long x1_7 = ext(b, 7, 7);
        long x0_7 = ext(a, 7, 7);
        long x1_8 = ext(b, 8, 8);
        long x0_8 = ext(a, 8, 8);
        long x1_9 = ext(b, 9, 9);
        long x0_9 = ext(a, 9, 9);
        long x1_10 = ext(b, 10, 10);
        long x0_10 = ext(a, 10, 10);
        long x1_11 = ext(b, 11, 11);
        long x0_11 = ext(a, 11, 11);
        long x1_12 = ext(b, 12, 12);
        long x0_12 = ext(a, 12, 12);
        long x1_13 = ext(b, 13, 13);
        long x0_13 = ext(a, 13, 13);
        long x1_14 = ext(b, 14, 14);
        long x0_14 = ext(a, 14, 14);
        long x1_15 = ext(b, 15, 15);
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
        long g0 = (x1_0 ^ x0_0);
        long g1 = (g0 ^ 1L);
        long g2 = (g1 ^ 1L);
        long g3 = (x1_0 ^ 1L);
        long g4 = (x0_0 ^ 1L);
        long g5 = (g4 | g3);
        long g6 = (x0_1 ^ g5);
        long g7 = (g6 ^ 1L);
        long g8 = (x1_0 ^ x1_1);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 ^ g7);
        long g11 = (g10 ^ 1L);
        long g12 = (x1_0 | x1_1);
        long g13 = (g12 ^ x1_2);
        long g14 = (g13 ^ 1L);
        long g15 = (x0_1 ^ 1L);
        long g16 = (g15 | g5);
        long g17 = (g16 ^ 1L);
        long g18 = (g9 | g5);
        long g19 = (g18 ^ 1L);
        long g20 = (g15 | g9);
        long g21 = (g20 ^ 1L);
        long g22 = (g21 | g19);
        long g23 = (g22 | g17);
        long g24 = (x0_2 ^ g23);
        long g25 = (g24 ^ 1L);
        long g26 = (g25 ^ g14);
        long g27 = (g26 ^ 1L);
        long g28 = (g27 ^ 1L);
        long g29 = (x1_2 | g12);
        long g30 = (g29 ^ x1_3);
        long g31 = (g30 ^ 1L);
        long g32 = (g23 ^ 1L);
        long g33 = (g14 | g32);
        long g34 = (g33 ^ 1L);
        long g35 = (x0_2 ^ 1L);
        long g36 = (g35 | g32);
        long g37 = (g36 ^ 1L);
        long g38 = (g35 | g14);
        long g39 = (g38 ^ 1L);
        long g40 = (g39 | g37);
        long g41 = (g40 | g34);
        long g42 = (x0_3 ^ g41);
        long g43 = (g42 ^ 1L);
        long g44 = (g43 ^ g31);
        long g45 = (g44 ^ 1L);
        long g46 = (g45 ^ 1L);
        long g47 = (x1_3 | g29);
        long g48 = (g47 ^ x1_4);
        long g49 = (g48 ^ 1L);
        long g50 = (g41 ^ 1L);
        long g51 = (g31 | g50);
        long g52 = (g51 ^ 1L);
        long g53 = (x0_3 ^ 1L);
        long g54 = (g53 | g50);
        long g55 = (g54 ^ 1L);
        long g56 = (g31 | g53);
        long g57 = (g56 ^ 1L);
        long g58 = (g57 | g55);
        long g59 = (g58 | g52);
        long g60 = (x0_4 ^ g59);
        long g61 = (g60 ^ 1L);
        long g62 = (g61 ^ g49);
        long g63 = (g62 ^ 1L);
        long g64 = (g63 ^ 1L);
        long g65 = (x1_4 | g47);
        long g66 = (g65 ^ x1_5);
        long g67 = (g66 ^ 1L);
        long g68 = (g59 ^ 1L);
        long g69 = (x0_4 ^ 1L);
        long g70 = (g69 | g68);
        long g71 = (g70 ^ 1L);
        long g72 = (g69 | g49);
        long g73 = (g72 ^ 1L);
        long g74 = (g49 | g68);
        long g75 = (g74 ^ 1L);
        long g76 = (g75 | g73);
        long g77 = (g76 | g71);
        long g78 = (x0_5 ^ g77);
        long g79 = (g78 ^ 1L);
        long g80 = (g79 ^ g67);
        long g81 = (g80 ^ 1L);
        long g82 = (g81 ^ 1L);
        long g83 = (x1_5 | g65);
        long g84 = (g83 ^ x1_6);
        long g85 = (g84 ^ 1L);
        long g86 = (g77 ^ 1L);
        long g87 = (x0_5 ^ 1L);
        long g88 = (g87 | g86);
        long g89 = (g88 ^ 1L);
        long g90 = (g87 | g67);
        long g91 = (g90 ^ 1L);
        long g92 = (g86 | g67);
        long g93 = (g92 ^ 1L);
        long g94 = (g93 | g91);
        long g95 = (g94 | g89);
        long g96 = (x0_6 ^ g95);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ g85);
        long g99 = (g98 ^ 1L);
        long g100 = (g99 ^ 1L);
        long g101 = (x1_6 | g83);
        long g102 = (g101 ^ x1_7);
        long g103 = (g102 ^ 1L);
        long g104 = (g95 ^ 1L);
        long g105 = (x0_6 ^ 1L);
        long g106 = (g105 | g104);
        long g107 = (g106 ^ 1L);
        long g108 = (g105 | g85);
        long g109 = (g108 ^ 1L);
        long g110 = (g104 | g85);
        long g111 = (g110 ^ 1L);
        long g112 = (g111 | g109);
        long g113 = (g112 | g107);
        long g114 = (x0_7 ^ g113);
        long g115 = (g114 ^ 1L);
        long g116 = (g115 ^ g103);
        long g117 = (g116 ^ 1L);
        long g118 = (g117 ^ 1L);
        long g119 = (x1_7 | g101);
        long g120 = (g119 ^ x1_8);
        long g121 = (g120 ^ 1L);
        long g122 = (x0_7 ^ 1L);
        long g123 = (g122 | g103);
        long g124 = (g123 ^ 1L);
        long g125 = (g113 ^ 1L);
        long g126 = (g125 | g103);
        long g127 = (g126 ^ 1L);
        long g128 = (g122 | g125);
        long g129 = (g128 ^ 1L);
        long g130 = (g129 | g127);
        long g131 = (g130 | g124);
        long g132 = (x0_8 ^ g131);
        long g133 = (g132 ^ 1L);
        long g134 = (g133 ^ g121);
        long g135 = (g134 ^ 1L);
        long g136 = (g135 ^ 1L);
        long g137 = (x1_8 | g119);
        long g138 = (g137 ^ x1_9);
        long g139 = (g138 ^ 1L);
        long g140 = (x0_8 ^ 1L);
        long g141 = (g140 | g121);
        long g142 = (g141 ^ 1L);
        long g143 = (g131 ^ 1L);
        long g144 = (g143 | g121);
        long g145 = (g144 ^ 1L);
        long g146 = (g140 | g143);
        long g147 = (g146 ^ 1L);
        long g148 = (g147 | g145);
        long g149 = (g148 | g142);
        long g150 = (x0_9 ^ g149);
        long g151 = (g150 ^ 1L);
        long g152 = (g151 ^ g139);
        long g153 = (g152 ^ 1L);
        long g154 = (g153 ^ 1L);
        long g155 = (x1_9 | g137);
        long g156 = (g155 ^ x1_10);
        long g157 = (g156 ^ 1L);
        long g158 = (g149 ^ 1L);
        long g159 = (x0_9 ^ 1L);
        long g160 = (g159 | g158);
        long g161 = (g160 ^ 1L);
        long g162 = (g158 | g139);
        long g163 = (g162 ^ 1L);
        long g164 = (g159 | g139);
        long g165 = (g164 ^ 1L);
        long g166 = (g165 | g163);
        long g167 = (g166 | g161);
        long g168 = (x0_10 ^ g167);
        long g169 = (g168 ^ 1L);
        long g170 = (g169 ^ g157);
        long g171 = (g170 ^ 1L);
        long g172 = (g171 ^ 1L);
        long g173 = (x1_10 | g155);
        long g174 = (g173 ^ x1_11);
        long g175 = (g174 ^ 1L);
        long g176 = (x0_10 ^ 1L);
        long g177 = (g176 | g157);
        long g178 = (g177 ^ 1L);
        long g179 = (g167 ^ 1L);
        long g180 = (g179 | g157);
        long g181 = (g180 ^ 1L);
        long g182 = (g176 | g179);
        long g183 = (g182 ^ 1L);
        long g184 = (g183 | g181);
        long g185 = (g184 | g178);
        long g186 = (x0_11 ^ g185);
        long g187 = (g186 ^ 1L);
        long g188 = (g187 ^ g175);
        long g189 = (g188 ^ 1L);
        long g190 = (g189 ^ 1L);
        long g191 = (x1_11 | g173);
        long g192 = (g191 ^ x1_12);
        long g193 = (g192 ^ 1L);
        long g194 = (g185 ^ 1L);
        long g195 = (g194 | g175);
        long g196 = (g195 ^ 1L);
        long g197 = (x0_11 ^ 1L);
        long g198 = (g197 | g194);
        long g199 = (g198 ^ 1L);
        long g200 = (g175 | g197);
        long g201 = (g200 ^ 1L);
        long g202 = (g201 | g199);
        long g203 = (g202 | g196);
        long g204 = (x0_12 ^ g203);
        long g205 = (g204 ^ 1L);
        long g206 = (g205 ^ g193);
        long g207 = (g206 ^ 1L);
        long g208 = (g207 ^ 1L);
        long g209 = (x1_12 | g191);
        long g210 = (g209 ^ x1_13);
        long g211 = (g210 ^ 1L);
        long g212 = (g203 ^ 1L);
        long g213 = (x0_12 ^ 1L);
        long g214 = (g213 | g212);
        long g215 = (g214 ^ 1L);
        long g216 = (g213 | g193);
        long g217 = (g216 ^ 1L);
        long g218 = (g193 | g212);
        long g219 = (g218 ^ 1L);
        long g220 = (g219 | g217);
        long g221 = (g220 | g215);
        long g222 = (x0_13 ^ g221);
        long g223 = (g222 ^ 1L);
        long g224 = (g223 ^ g211);
        long g225 = (g224 ^ 1L);
        long g226 = (g225 ^ 1L);
        long g227 = (x1_13 | g209);
        long g228 = (g227 ^ x1_14);
        long g229 = (g228 ^ 1L);
        long g230 = (g221 ^ 1L);
        long g231 = (x0_13 ^ 1L);
        long g232 = (g231 | g230);
        long g233 = (g232 ^ 1L);
        long g234 = (g230 | g211);
        long g235 = (g234 ^ 1L);
        long g236 = (g211 | g231);
        long g237 = (g236 ^ 1L);
        long g238 = (g237 | g235);
        long g239 = (g238 | g233);
        long g240 = (x0_14 ^ g239);
        long g241 = (g240 ^ 1L);
        long g242 = (g241 ^ g229);
        long g243 = (g242 ^ 1L);
        long g244 = (g243 ^ 1L);
        long g245 = (x1_14 | g227);
        long g246 = (g245 ^ x1_15);
        long g247 = (g246 ^ 1L);
        long g248 = (g239 ^ 1L);
        long g249 = (x0_14 ^ 1L);
        long g250 = (g249 | g248);
        long g251 = (g250 ^ 1L);
        long g252 = (g229 | g248);
        long g253 = (g252 ^ 1L);
        long g254 = (g229 | g249);
        long g255 = (g254 ^ 1L);
        long g256 = (g255 | g253);
        long g257 = (g256 | g251);
        long g258 = (x0_15 ^ g257);
        long g259 = (g258 ^ 1L);
        long g260 = (g259 ^ g247);
        long g261 = (g260 ^ 1L);
        long g262 = (g261 ^ 1L);
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
        long w48 = cat(w47, g262, 1);
        long w49 = cat(w48, g244, 1);
        long w50 = cat(w49, g226, 1);
        long w51 = cat(w50, g208, 1);
        long w52 = cat(w51, g190, 1);
        long w53 = cat(w52, g172, 1);
        long w54 = cat(w53, g154, 1);
        long w55 = cat(w54, g136, 1);
        long w56 = cat(w55, g118, 1);
        long w57 = cat(w56, g100, 1);
        long w58 = cat(w57, g82, 1);
        long w59 = cat(w58, g64, 1);
        long w60 = cat(w59, g46, 1);
        long w61 = cat(w60, g28, 1);
        long w62 = cat(w61, g11, 1);
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
                    answers.Append(((ulong) emu_sub_gpr_gpr_16__reg_rdi__csharp(values[0], values[1])).ToString());
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
