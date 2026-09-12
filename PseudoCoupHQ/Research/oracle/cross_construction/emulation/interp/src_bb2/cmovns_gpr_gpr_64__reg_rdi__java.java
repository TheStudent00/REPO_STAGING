import java.io.*;
import java.util.*;

public class Emu {
    static long m(long x, int w) {
        if (w >= 64) { return x; }
        return x & ((1L << w) - 1L);
    }
    static long s(long x, int w) {
        if (w >= 64) { return x; }
        return (x << (64 - w)) >> (64 - w);
    }
    static long add(long a, long b, int w) { return m(a + b, w); }
    static long sub(long a, long b, int w) { return m(a - b, w); }
    static long mul(long a, long b, int w) { return m(a * b, w); }
    static long band(long a, long b, int w) { return m(a & b, w); }
    static long bor(long a, long b, int w) { return m(a | b, w); }
    static long bxor(long a, long b, int w) { return m(a ^ b, w); }
    static long bnot(long a, int w) { return m(~a, w); }
    static long bneg(long a, int w) { return m(-a, w); }
    static long shl(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(a << n, w);
    }
    static long lshr(long a, long n, int w) {
        if (n >= w) { return 0L; }
        return m(m(a, w) >>> n, w);
    }
    static long ashr(long a, long n, int w) {
        long v = s(a, w);
        long k = n;
        if (k >= w) { k = w - 1; }
        return m(v >> k, w);
    }
    static long udiv(long a, long b, int w) {
        return m(Long.divideUnsigned(m(a, w), m(b, w)), w);
    }
    static long urem(long a, long b, int w) {
        return m(Long.remainderUnsigned(m(a, w), m(b, w)), w);
    }
    static long sdiv(long a, long b, int w) {
        return m(s(a, w) / s(b, w), w);
    }
    static long srem(long a, long b, int w) {
        return m(s(a, w) % s(b, w), w);
    }
    static boolean ult(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) < 0;
    }
    static boolean ule(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) <= 0;
    }
    static boolean ugt(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) > 0;
    }
    static boolean uge(long a, long b, int w) {
        return Long.compareUnsigned(m(a, w), m(b, w)) >= 0;
    }
    static boolean slt(long a, long b, int w) { return s(a, w) < s(b, w); }
    static boolean sle(long a, long b, int w) { return s(a, w) <= s(b, w); }
    static boolean sgt(long a, long b, int w) { return s(a, w) > s(b, w); }
    static boolean sge(long a, long b, int w) { return s(a, w) >= s(b, w); }
    static boolean eq(long a, long b, int w) { return m(a, w) == m(b, w); }
    static boolean ne(long a, long b, int w) { return m(a, w) != m(b, w); }
    static long cat(long hi, long lo, int lw) {
        return (hi << lw) | m(lo, lw);
    }
    static long ext(long x, int hi, int lo) {
        return m(x >>> lo, hi - lo + 1);
    }
    static long sext(long x, int fromw, int tow) {
        return m(s(x, fromw), tow);
    }
    static double b2f(long x, int w) {
        if (w == 32) { return Float.intBitsToFloat((int) m(x, 32)); }
        return Double.longBitsToDouble(x);
    }
    static long f2b(double f, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(Float.floatToRawIntBits((float) f));
        }
        return Double.doubleToRawLongBits(f);
    }
    static long fadd(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    + Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) + b2f(b, w), w);
    }
    static long fsub(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    - Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) - b2f(b, w), w);
    }
    static long fmul(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    * Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) * b2f(b, w), w);
    }
    static long fdiv(long a, long b, int w) {
        if (w == 32) {
            float r = Float.intBitsToFloat((int) m(a, 32))
                    / Float.intBitsToFloat((int) m(b, 32));
            return Integer.toUnsignedLong(Float.floatToRawIntBits(r));
        }
        return f2b(b2f(a, w) / b2f(b, w), w);
    }
    static long i2f(long x, int fromw, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(
                Float.floatToRawIntBits((float) s(x, fromw)));
        }
        return Double.doubleToRawLongBits((double) s(x, fromw));
    }
    static long u2f(long x, int fromw, int w) {
        if (w == 32) {
            return Integer.toUnsignedLong(Float.floatToRawIntBits(
                (float) Long.parseUnsignedLong(
                    Long.toUnsignedString(m(x, fromw)))));
        }
        return Double.doubleToRawLongBits(
            (double) m(x, fromw));
    }
    static long fwiden(long x, int fromw, int w) {
        return f2b(b2f(x, fromw), w);
    }

    // task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
    // one named local per gate, over the term of cmovns_gpr_gpr_64__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
    static long emu_cmovns_gpr_gpr_64__reg_rdi__java(long a, long b, long c, long d) {
        long x3_0 = ext(d, 0, 0);
        long x1_63 = ext(a, 63, 63);
        long x0_63 = ext(b, 63, 63);
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
        long x3_32 = ext(d, 32, 32);
        long x2_32 = ext(c, 32, 32);
        long x3_33 = ext(d, 33, 33);
        long x2_33 = ext(c, 33, 33);
        long x3_34 = ext(d, 34, 34);
        long x2_34 = ext(c, 34, 34);
        long x3_35 = ext(d, 35, 35);
        long x2_35 = ext(c, 35, 35);
        long x3_36 = ext(d, 36, 36);
        long x2_36 = ext(c, 36, 36);
        long x3_37 = ext(d, 37, 37);
        long x2_37 = ext(c, 37, 37);
        long x3_38 = ext(d, 38, 38);
        long x2_38 = ext(c, 38, 38);
        long x3_39 = ext(d, 39, 39);
        long x2_39 = ext(c, 39, 39);
        long x3_40 = ext(d, 40, 40);
        long x2_40 = ext(c, 40, 40);
        long x3_41 = ext(d, 41, 41);
        long x2_41 = ext(c, 41, 41);
        long x3_42 = ext(d, 42, 42);
        long x2_42 = ext(c, 42, 42);
        long x3_43 = ext(d, 43, 43);
        long x2_43 = ext(c, 43, 43);
        long x3_44 = ext(d, 44, 44);
        long x2_44 = ext(c, 44, 44);
        long x3_45 = ext(d, 45, 45);
        long x2_45 = ext(c, 45, 45);
        long x3_46 = ext(d, 46, 46);
        long x2_46 = ext(c, 46, 46);
        long x3_47 = ext(d, 47, 47);
        long x2_47 = ext(c, 47, 47);
        long x3_48 = ext(d, 48, 48);
        long x2_48 = ext(c, 48, 48);
        long x3_49 = ext(d, 49, 49);
        long x2_49 = ext(c, 49, 49);
        long x3_50 = ext(d, 50, 50);
        long x2_50 = ext(c, 50, 50);
        long x3_51 = ext(d, 51, 51);
        long x2_51 = ext(c, 51, 51);
        long x3_52 = ext(d, 52, 52);
        long x2_52 = ext(c, 52, 52);
        long x3_53 = ext(d, 53, 53);
        long x2_53 = ext(c, 53, 53);
        long x3_54 = ext(d, 54, 54);
        long x2_54 = ext(c, 54, 54);
        long x3_55 = ext(d, 55, 55);
        long x2_55 = ext(c, 55, 55);
        long x3_56 = ext(d, 56, 56);
        long x2_56 = ext(c, 56, 56);
        long x3_57 = ext(d, 57, 57);
        long x2_57 = ext(c, 57, 57);
        long x3_58 = ext(d, 58, 58);
        long x2_58 = ext(c, 58, 58);
        long x3_59 = ext(d, 59, 59);
        long x2_59 = ext(c, 59, 59);
        long x3_60 = ext(d, 60, 60);
        long x2_60 = ext(c, 60, 60);
        long x3_61 = ext(d, 61, 61);
        long x2_61 = ext(c, 61, 61);
        long x3_62 = ext(d, 62, 62);
        long x2_62 = ext(c, 62, 62);
        long x3_63 = ext(d, 63, 63);
        long x2_63 = ext(c, 63, 63);
        long g0 = (x1_63 ^ 1L);
        long g1 = (x0_63 ^ 1L);
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
        long g100 = (g3 & x3_32);
        long g101 = (g2 & x2_32);
        long g102 = (g101 | g100);
        long g103 = (g3 & x3_33);
        long g104 = (g2 & x2_33);
        long g105 = (g104 | g103);
        long g106 = (g3 & x3_34);
        long g107 = (g2 & x2_34);
        long g108 = (g107 | g106);
        long g109 = (g3 & x3_35);
        long g110 = (g2 & x2_35);
        long g111 = (g110 | g109);
        long g112 = (g3 & x3_36);
        long g113 = (g2 & x2_36);
        long g114 = (g113 | g112);
        long g115 = (g3 & x3_37);
        long g116 = (g2 & x2_37);
        long g117 = (g116 | g115);
        long g118 = (g3 & x3_38);
        long g119 = (g2 & x2_38);
        long g120 = (g119 | g118);
        long g121 = (g3 & x3_39);
        long g122 = (g2 & x2_39);
        long g123 = (g122 | g121);
        long g124 = (g3 & x3_40);
        long g125 = (g2 & x2_40);
        long g126 = (g125 | g124);
        long g127 = (g3 & x3_41);
        long g128 = (g2 & x2_41);
        long g129 = (g128 | g127);
        long g130 = (g3 & x3_42);
        long g131 = (g2 & x2_42);
        long g132 = (g131 | g130);
        long g133 = (g3 & x3_43);
        long g134 = (g2 & x2_43);
        long g135 = (g134 | g133);
        long g136 = (g3 & x3_44);
        long g137 = (g2 & x2_44);
        long g138 = (g137 | g136);
        long g139 = (g3 & x3_45);
        long g140 = (g2 & x2_45);
        long g141 = (g140 | g139);
        long g142 = (g3 & x3_46);
        long g143 = (g2 & x2_46);
        long g144 = (g143 | g142);
        long g145 = (g3 & x3_47);
        long g146 = (g2 & x2_47);
        long g147 = (g146 | g145);
        long g148 = (g3 & x3_48);
        long g149 = (g2 & x2_48);
        long g150 = (g149 | g148);
        long g151 = (g3 & x3_49);
        long g152 = (g2 & x2_49);
        long g153 = (g152 | g151);
        long g154 = (g3 & x3_50);
        long g155 = (g2 & x2_50);
        long g156 = (g155 | g154);
        long g157 = (g3 & x3_51);
        long g158 = (g2 & x2_51);
        long g159 = (g158 | g157);
        long g160 = (g3 & x3_52);
        long g161 = (g2 & x2_52);
        long g162 = (g161 | g160);
        long g163 = (g3 & x3_53);
        long g164 = (g2 & x2_53);
        long g165 = (g164 | g163);
        long g166 = (g3 & x3_54);
        long g167 = (g2 & x2_54);
        long g168 = (g167 | g166);
        long g169 = (g3 & x3_55);
        long g170 = (g2 & x2_55);
        long g171 = (g170 | g169);
        long g172 = (g3 & x3_56);
        long g173 = (g2 & x2_56);
        long g174 = (g173 | g172);
        long g175 = (g3 & x3_57);
        long g176 = (g2 & x2_57);
        long g177 = (g176 | g175);
        long g178 = (g3 & x3_58);
        long g179 = (g2 & x2_58);
        long g180 = (g179 | g178);
        long g181 = (g3 & x3_59);
        long g182 = (g2 & x2_59);
        long g183 = (g182 | g181);
        long g184 = (g3 & x3_60);
        long g185 = (g2 & x2_60);
        long g186 = (g185 | g184);
        long g187 = (g3 & x3_61);
        long g188 = (g2 & x2_61);
        long g189 = (g188 | g187);
        long g190 = (g3 & x3_62);
        long g191 = (g2 & x2_62);
        long g192 = (g191 | g190);
        long g193 = (g3 & x3_63);
        long g194 = (g2 & x2_63);
        long g195 = (g194 | g193);
        long w0 = g195;
        long w1 = cat(w0, g192, 1);
        long w2 = cat(w1, g189, 1);
        long w3 = cat(w2, g186, 1);
        long w4 = cat(w3, g183, 1);
        long w5 = cat(w4, g180, 1);
        long w6 = cat(w5, g177, 1);
        long w7 = cat(w6, g174, 1);
        long w8 = cat(w7, g171, 1);
        long w9 = cat(w8, g168, 1);
        long w10 = cat(w9, g165, 1);
        long w11 = cat(w10, g162, 1);
        long w12 = cat(w11, g159, 1);
        long w13 = cat(w12, g156, 1);
        long w14 = cat(w13, g153, 1);
        long w15 = cat(w14, g150, 1);
        long w16 = cat(w15, g147, 1);
        long w17 = cat(w16, g144, 1);
        long w18 = cat(w17, g141, 1);
        long w19 = cat(w18, g138, 1);
        long w20 = cat(w19, g135, 1);
        long w21 = cat(w20, g132, 1);
        long w22 = cat(w21, g129, 1);
        long w23 = cat(w22, g126, 1);
        long w24 = cat(w23, g123, 1);
        long w25 = cat(w24, g120, 1);
        long w26 = cat(w25, g117, 1);
        long w27 = cat(w26, g114, 1);
        long w28 = cat(w27, g111, 1);
        long w29 = cat(w28, g108, 1);
        long w30 = cat(w29, g105, 1);
        long w31 = cat(w30, g102, 1);
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


    public static void main(String[] args) throws IOException {
        BufferedReader reader =
            new BufferedReader(new InputStreamReader(System.in));
        StringBuilder answers = new StringBuilder();
        String line = reader.readLine();
        while (line != null) {
            String text = line.trim();
            if (text.length() != 0) {
                String[] parts = text.split("\\s+");
                long[] values = new long[parts.length];
                for (int i = 0; i < parts.length; i++) {
                    values[i] = Long.parseUnsignedLong(parts[i]);
                }
                try {
                    answers.append(Long.toUnsignedString(emu_cmovns_gpr_gpr_64__reg_rdi__java(values[0], values[1], values[2], values[3])));
                    answers.append("\n");
                } catch (Throwable problem) {
                    answers.append("RAISE:");
                    answers.append(problem.getClass().getSimpleName());
                    answers.append("\n");
                }
            }
            line = reader.readLine();
        }
        System.out.print(answers);
    }
}
