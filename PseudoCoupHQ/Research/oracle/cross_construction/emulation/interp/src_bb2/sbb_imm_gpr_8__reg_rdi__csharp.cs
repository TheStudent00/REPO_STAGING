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
    // one named local per gate, over the term of sbb_imm_gpr_8__reg_rdi__csharp.
    // The term's layer-5 text, LITERAL:
    //   Concat(Extract(63, 8, v3), Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3))
    public static long emu_sbb_imm_gpr_8__reg_rdi__csharp(long a, long b, long c, long d) {
        long x3_0 = ext(c, 0, 0);
        long x2_0 = ext(d, 0, 0);
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
        long x3_1 = ext(c, 1, 1);
        long x2_1 = ext(d, 1, 1);
        long x2_2 = ext(d, 2, 2);
        long x3_2 = ext(c, 2, 2);
        long x2_3 = ext(d, 3, 3);
        long x3_3 = ext(c, 3, 3);
        long x2_4 = ext(d, 4, 4);
        long x3_4 = ext(c, 4, 4);
        long x2_5 = ext(d, 5, 5);
        long x3_5 = ext(c, 5, 5);
        long x2_6 = ext(d, 6, 6);
        long x3_6 = ext(c, 6, 6);
        long x2_7 = ext(d, 7, 7);
        long x3_7 = ext(c, 7, 7);
        long x3_8 = ext(c, 8, 8);
        long x3_9 = ext(c, 9, 9);
        long x3_10 = ext(c, 10, 10);
        long x3_11 = ext(c, 11, 11);
        long x3_12 = ext(c, 12, 12);
        long x3_13 = ext(c, 13, 13);
        long x3_14 = ext(c, 14, 14);
        long x3_15 = ext(c, 15, 15);
        long x3_16 = ext(c, 16, 16);
        long x3_17 = ext(c, 17, 17);
        long x3_18 = ext(c, 18, 18);
        long x3_19 = ext(c, 19, 19);
        long x3_20 = ext(c, 20, 20);
        long x3_21 = ext(c, 21, 21);
        long x3_22 = ext(c, 22, 22);
        long x3_23 = ext(c, 23, 23);
        long x3_24 = ext(c, 24, 24);
        long x3_25 = ext(c, 25, 25);
        long x3_26 = ext(c, 26, 26);
        long x3_27 = ext(c, 27, 27);
        long x3_28 = ext(c, 28, 28);
        long x3_29 = ext(c, 29, 29);
        long x3_30 = ext(c, 30, 30);
        long x3_31 = ext(c, 31, 31);
        long x3_32 = ext(c, 32, 32);
        long x3_33 = ext(c, 33, 33);
        long x3_34 = ext(c, 34, 34);
        long x3_35 = ext(c, 35, 35);
        long x3_36 = ext(c, 36, 36);
        long x3_37 = ext(c, 37, 37);
        long x3_38 = ext(c, 38, 38);
        long x3_39 = ext(c, 39, 39);
        long x3_40 = ext(c, 40, 40);
        long x3_41 = ext(c, 41, 41);
        long x3_42 = ext(c, 42, 42);
        long x3_43 = ext(c, 43, 43);
        long x3_44 = ext(c, 44, 44);
        long x3_45 = ext(c, 45, 45);
        long x3_46 = ext(c, 46, 46);
        long x3_47 = ext(c, 47, 47);
        long x3_48 = ext(c, 48, 48);
        long x3_49 = ext(c, 49, 49);
        long x3_50 = ext(c, 50, 50);
        long x3_51 = ext(c, 51, 51);
        long x3_52 = ext(c, 52, 52);
        long x3_53 = ext(c, 53, 53);
        long x3_54 = ext(c, 54, 54);
        long x3_55 = ext(c, 55, 55);
        long x3_56 = ext(c, 56, 56);
        long x3_57 = ext(c, 57, 57);
        long x3_58 = ext(c, 58, 58);
        long x3_59 = ext(c, 59, 59);
        long x3_60 = ext(c, 60, 60);
        long x3_61 = ext(c, 61, 61);
        long x3_62 = ext(c, 62, 62);
        long x3_63 = ext(c, 63, 63);
        long g0 = (x2_0 ^ x3_0);
        long g1 = (g0 ^ 1L);
        long g2 = (x1_0 ^ 1L);
        long g3 = (x0_0 ^ 1L);
        long g4 = (g3 | g2);
        long g5 = (x1_1 ^ 1L);
        long g6 = (g5 | g4);
        long g7 = (g6 ^ 1L);
        long g8 = (x0_1 ^ 1L);
        long g9 = (g8 | g4);
        long g10 = (g9 ^ 1L);
        long g11 = (g8 | g5);
        long g12 = (g11 ^ 1L);
        long g13 = (g12 | g10);
        long g14 = (g13 | g7);
        long g15 = (g14 ^ 1L);
        long g16 = (x1_2 ^ 1L);
        long g17 = (g16 | g15);
        long g18 = (g17 ^ 1L);
        long g19 = (x0_2 ^ 1L);
        long g20 = (g19 | g15);
        long g21 = (g20 ^ 1L);
        long g22 = (g19 | g16);
        long g23 = (g22 ^ 1L);
        long g24 = (g23 | g21);
        long g25 = (g24 | g18);
        long g26 = (g25 ^ 1L);
        long g27 = (x1_3 ^ 1L);
        long g28 = (g27 | g26);
        long g29 = (g28 ^ 1L);
        long g30 = (x0_3 ^ 1L);
        long g31 = (g30 | g26);
        long g32 = (g31 ^ 1L);
        long g33 = (g30 | g27);
        long g34 = (g33 ^ 1L);
        long g35 = (g34 | g32);
        long g36 = (g35 | g29);
        long g37 = (g36 ^ 1L);
        long g38 = (x1_4 ^ 1L);
        long g39 = (g38 | g37);
        long g40 = (g39 ^ 1L);
        long g41 = (x0_4 ^ 1L);
        long g42 = (g41 | g37);
        long g43 = (g42 ^ 1L);
        long g44 = (g41 | g38);
        long g45 = (g44 ^ 1L);
        long g46 = (g45 | g43);
        long g47 = (g46 | g40);
        long g48 = (g47 ^ 1L);
        long g49 = (x1_5 ^ 1L);
        long g50 = (g49 | g48);
        long g51 = (g50 ^ 1L);
        long g52 = (x0_5 ^ 1L);
        long g53 = (g52 | g48);
        long g54 = (g53 ^ 1L);
        long g55 = (g52 | g49);
        long g56 = (g55 ^ 1L);
        long g57 = (g56 | g54);
        long g58 = (g57 | g51);
        long g59 = (g58 ^ 1L);
        long g60 = (x1_6 ^ 1L);
        long g61 = (g60 | g59);
        long g62 = (g61 ^ 1L);
        long g63 = (x0_6 ^ 1L);
        long g64 = (g63 | g59);
        long g65 = (g64 ^ 1L);
        long g66 = (g63 | g60);
        long g67 = (g66 ^ 1L);
        long g68 = (g67 | g65);
        long g69 = (g68 | g62);
        long g70 = (g69 ^ 1L);
        long g71 = (x1_7 ^ 1L);
        long g72 = (g71 | g70);
        long g73 = (g72 ^ 1L);
        long g74 = (x0_7 ^ 1L);
        long g75 = (g74 | g70);
        long g76 = (g75 ^ 1L);
        long g77 = (g74 | g71);
        long g78 = (g77 ^ 1L);
        long g79 = (g78 | g76);
        long g80 = (g79 | g73);
        long g81 = (g80 ^ g1);
        long g82 = (g81 ^ 1L);
        long g83 = (x2_0 ^ g80);
        long g84 = (g83 ^ 1L);
        long g85 = (x3_0 ^ 1L);
        long g86 = (g85 | g84);
        long g87 = (x3_1 ^ g86);
        long g88 = (g87 ^ 1L);
        long g89 = (g80 ^ 1L);
        long g90 = (x2_0 ^ 1L);
        long g91 = (g90 | g89);
        long g92 = (g80 ^ g91);
        long g93 = (g92 ^ 1L);
        long g94 = (x2_0 ^ x2_1);
        long g95 = (g94 ^ 1L);
        long g96 = (g95 ^ g93);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ g88);
        long g99 = (g98 ^ 1L);
        long g100 = (g99 ^ 1L);
        long g101 = (x2_0 | x2_1);
        long g102 = (g101 ^ x2_2);
        long g103 = (g102 ^ 1L);
        long g104 = (g95 | g91);
        long g105 = (g104 ^ 1L);
        long g106 = (g89 | g95);
        long g107 = (g106 ^ 1L);
        long g108 = (g89 | g91);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 | g107);
        long g111 = (g110 | g105);
        long g112 = (g80 ^ g111);
        long g113 = (g112 ^ 1L);
        long g114 = (g113 ^ g103);
        long g115 = (g114 ^ 1L);
        long g116 = (g97 ^ 1L);
        long g117 = (x3_1 ^ 1L);
        long g118 = (g117 | g116);
        long g119 = (g118 ^ 1L);
        long g120 = (g116 | g86);
        long g121 = (g120 ^ 1L);
        long g122 = (g117 | g86);
        long g123 = (g122 ^ 1L);
        long g124 = (g123 | g121);
        long g125 = (g124 | g119);
        long g126 = (x3_2 ^ g125);
        long g127 = (g126 ^ 1L);
        long g128 = (g127 ^ g115);
        long g129 = (g128 ^ 1L);
        long g130 = (g129 ^ 1L);
        long g131 = (x2_2 | g101);
        long g132 = (g131 ^ x2_3);
        long g133 = (g132 ^ 1L);
        long g134 = (g111 ^ 1L);
        long g135 = (g103 | g134);
        long g136 = (g135 ^ 1L);
        long g137 = (g89 | g103);
        long g138 = (g137 ^ 1L);
        long g139 = (g89 | g134);
        long g140 = (g139 ^ 1L);
        long g141 = (g140 | g138);
        long g142 = (g141 | g136);
        long g143 = (g80 ^ g142);
        long g144 = (g143 ^ 1L);
        long g145 = (g144 ^ g133);
        long g146 = (g145 ^ 1L);
        long g147 = (g125 ^ 1L);
        long g148 = (g147 | g115);
        long g149 = (g148 ^ 1L);
        long g150 = (x3_2 ^ 1L);
        long g151 = (g150 | g147);
        long g152 = (g151 ^ 1L);
        long g153 = (g150 | g115);
        long g154 = (g153 ^ 1L);
        long g155 = (g154 | g152);
        long g156 = (g155 | g149);
        long g157 = (x3_3 ^ g156);
        long g158 = (g157 ^ 1L);
        long g159 = (g158 ^ g146);
        long g160 = (g159 ^ 1L);
        long g161 = (g160 ^ 1L);
        long g162 = (x2_3 | g131);
        long g163 = (g162 ^ x2_4);
        long g164 = (g163 ^ 1L);
        long g165 = (g142 ^ 1L);
        long g166 = (g89 | g165);
        long g167 = (g166 ^ 1L);
        long g168 = (g89 | g133);
        long g169 = (g168 ^ 1L);
        long g170 = (g133 | g165);
        long g171 = (g170 ^ 1L);
        long g172 = (g171 | g169);
        long g173 = (g172 | g167);
        long g174 = (g80 ^ g173);
        long g175 = (g174 ^ 1L);
        long g176 = (g175 ^ g164);
        long g177 = (g176 ^ 1L);
        long g178 = (x3_3 ^ 1L);
        long g179 = (g146 | g178);
        long g180 = (g179 ^ 1L);
        long g181 = (g156 ^ 1L);
        long g182 = (g178 | g181);
        long g183 = (g182 ^ 1L);
        long g184 = (g146 | g181);
        long g185 = (g184 ^ 1L);
        long g186 = (g185 | g183);
        long g187 = (g186 | g180);
        long g188 = (x3_4 ^ g187);
        long g189 = (g188 ^ 1L);
        long g190 = (g189 ^ g177);
        long g191 = (g190 ^ 1L);
        long g192 = (g191 ^ 1L);
        long g193 = (x2_4 | g162);
        long g194 = (g193 ^ x2_5);
        long g195 = (g194 ^ 1L);
        long g196 = (g89 | g164);
        long g197 = (g196 ^ 1L);
        long g198 = (g173 ^ 1L);
        long g199 = (g89 | g198);
        long g200 = (g199 ^ 1L);
        long g201 = (g198 | g164);
        long g202 = (g201 ^ 1L);
        long g203 = (g202 | g200);
        long g204 = (g203 | g197);
        long g205 = (g80 ^ g204);
        long g206 = (g205 ^ 1L);
        long g207 = (g206 ^ g195);
        long g208 = (g207 ^ 1L);
        long g209 = (g187 ^ 1L);
        long g210 = (g209 | g177);
        long g211 = (g210 ^ 1L);
        long g212 = (x3_4 ^ 1L);
        long g213 = (g212 | g177);
        long g214 = (g213 ^ 1L);
        long g215 = (g212 | g209);
        long g216 = (g215 ^ 1L);
        long g217 = (g216 | g214);
        long g218 = (g217 | g211);
        long g219 = (x3_5 ^ g218);
        long g220 = (g219 ^ 1L);
        long g221 = (g220 ^ g208);
        long g222 = (g221 ^ 1L);
        long g223 = (g222 ^ 1L);
        long g224 = (x2_5 | g193);
        long g225 = (g224 ^ x2_6);
        long g226 = (g225 ^ 1L);
        long g227 = (g204 ^ 1L);
        long g228 = (g89 | g227);
        long g229 = (g228 ^ 1L);
        long g230 = (g195 | g227);
        long g231 = (g230 ^ 1L);
        long g232 = (g89 | g195);
        long g233 = (g232 ^ 1L);
        long g234 = (g233 | g231);
        long g235 = (g234 | g229);
        long g236 = (g80 ^ g235);
        long g237 = (g236 ^ 1L);
        long g238 = (g237 ^ g226);
        long g239 = (g238 ^ 1L);
        long g240 = (g218 ^ 1L);
        long g241 = (x3_5 ^ 1L);
        long g242 = (g241 | g240);
        long g243 = (g242 ^ 1L);
        long g244 = (g208 | g241);
        long g245 = (g244 ^ 1L);
        long g246 = (g208 | g240);
        long g247 = (g246 ^ 1L);
        long g248 = (g247 | g245);
        long g249 = (g248 | g243);
        long g250 = (x3_6 ^ g249);
        long g251 = (g250 ^ 1L);
        long g252 = (g251 ^ g239);
        long g253 = (g252 ^ 1L);
        long g254 = (g253 ^ 1L);
        long g255 = (x2_6 | g224);
        long g256 = (g255 ^ x2_7);
        long g257 = (g256 ^ 1L);
        long g258 = (g89 | g226);
        long g259 = (g258 ^ 1L);
        long g260 = (g235 ^ 1L);
        long g261 = (g226 | g260);
        long g262 = (g261 ^ 1L);
        long g263 = (g89 | g260);
        long g264 = (g263 ^ 1L);
        long g265 = (g264 | g262);
        long g266 = (g265 | g259);
        long g267 = (g80 ^ g266);
        long g268 = (g267 ^ 1L);
        long g269 = (g268 ^ g257);
        long g270 = (g269 ^ 1L);
        long g271 = (g249 ^ 1L);
        long g272 = (x3_6 ^ 1L);
        long g273 = (g272 | g271);
        long g274 = (g273 ^ 1L);
        long g275 = (g239 | g272);
        long g276 = (g275 ^ 1L);
        long g277 = (g271 | g239);
        long g278 = (g277 ^ 1L);
        long g279 = (g278 | g276);
        long g280 = (g279 | g274);
        long g281 = (x3_7 ^ g280);
        long g282 = (g281 ^ 1L);
        long g283 = (g282 ^ g270);
        long g284 = (g283 ^ 1L);
        long g285 = (g284 ^ 1L);
        long w0 = x3_63;
        long w1 = cat(w0, x3_62, 1);
        long w2 = cat(w1, x3_61, 1);
        long w3 = cat(w2, x3_60, 1);
        long w4 = cat(w3, x3_59, 1);
        long w5 = cat(w4, x3_58, 1);
        long w6 = cat(w5, x3_57, 1);
        long w7 = cat(w6, x3_56, 1);
        long w8 = cat(w7, x3_55, 1);
        long w9 = cat(w8, x3_54, 1);
        long w10 = cat(w9, x3_53, 1);
        long w11 = cat(w10, x3_52, 1);
        long w12 = cat(w11, x3_51, 1);
        long w13 = cat(w12, x3_50, 1);
        long w14 = cat(w13, x3_49, 1);
        long w15 = cat(w14, x3_48, 1);
        long w16 = cat(w15, x3_47, 1);
        long w17 = cat(w16, x3_46, 1);
        long w18 = cat(w17, x3_45, 1);
        long w19 = cat(w18, x3_44, 1);
        long w20 = cat(w19, x3_43, 1);
        long w21 = cat(w20, x3_42, 1);
        long w22 = cat(w21, x3_41, 1);
        long w23 = cat(w22, x3_40, 1);
        long w24 = cat(w23, x3_39, 1);
        long w25 = cat(w24, x3_38, 1);
        long w26 = cat(w25, x3_37, 1);
        long w27 = cat(w26, x3_36, 1);
        long w28 = cat(w27, x3_35, 1);
        long w29 = cat(w28, x3_34, 1);
        long w30 = cat(w29, x3_33, 1);
        long w31 = cat(w30, x3_32, 1);
        long w32 = cat(w31, x3_31, 1);
        long w33 = cat(w32, x3_30, 1);
        long w34 = cat(w33, x3_29, 1);
        long w35 = cat(w34, x3_28, 1);
        long w36 = cat(w35, x3_27, 1);
        long w37 = cat(w36, x3_26, 1);
        long w38 = cat(w37, x3_25, 1);
        long w39 = cat(w38, x3_24, 1);
        long w40 = cat(w39, x3_23, 1);
        long w41 = cat(w40, x3_22, 1);
        long w42 = cat(w41, x3_21, 1);
        long w43 = cat(w42, x3_20, 1);
        long w44 = cat(w43, x3_19, 1);
        long w45 = cat(w44, x3_18, 1);
        long w46 = cat(w45, x3_17, 1);
        long w47 = cat(w46, x3_16, 1);
        long w48 = cat(w47, x3_15, 1);
        long w49 = cat(w48, x3_14, 1);
        long w50 = cat(w49, x3_13, 1);
        long w51 = cat(w50, x3_12, 1);
        long w52 = cat(w51, x3_11, 1);
        long w53 = cat(w52, x3_10, 1);
        long w54 = cat(w53, x3_9, 1);
        long w55 = cat(w54, x3_8, 1);
        long w56 = cat(w55, g285, 1);
        long w57 = cat(w56, g254, 1);
        long w58 = cat(w57, g223, 1);
        long w59 = cat(w58, g192, 1);
        long w60 = cat(w59, g161, 1);
        long w61 = cat(w60, g130, 1);
        long w62 = cat(w61, g100, 1);
        long w63 = cat(w62, g82, 1);
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
                    answers.Append(((ulong) emu_sbb_imm_gpr_8__reg_rdi__csharp(values[0], values[1], values[2], values[3])).ToString());
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
