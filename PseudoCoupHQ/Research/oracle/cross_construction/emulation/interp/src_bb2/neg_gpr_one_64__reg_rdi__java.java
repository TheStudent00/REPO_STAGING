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
    // one named local per gate, over the term of neg_gpr_one_64__reg_rdi__java.
    // The term's layer-5 text, LITERAL:
    //   v0*18446744073709551615
    static long emu_neg_gpr_one_64__reg_rdi__java(long a) {
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
        long g0 = (x0_0 ^ x0_1);
        long g1 = (g0 ^ 1L);
        long g2 = (g1 ^ 1L);
        long g3 = (x0_1 | x0_0);
        long g4 = (g3 ^ x0_2);
        long g5 = (g4 ^ 1L);
        long g6 = (g5 ^ 1L);
        long g7 = (x0_2 | g3);
        long g8 = (g7 ^ x0_3);
        long g9 = (g8 ^ 1L);
        long g10 = (g9 ^ 1L);
        long g11 = (x0_3 | g7);
        long g12 = (g11 ^ x0_4);
        long g13 = (g12 ^ 1L);
        long g14 = (g13 ^ 1L);
        long g15 = (x0_4 | g11);
        long g16 = (g15 ^ x0_5);
        long g17 = (g16 ^ 1L);
        long g18 = (g17 ^ 1L);
        long g19 = (x0_5 | g15);
        long g20 = (g19 ^ x0_6);
        long g21 = (g20 ^ 1L);
        long g22 = (g21 ^ 1L);
        long g23 = (x0_6 | g19);
        long g24 = (g23 ^ x0_7);
        long g25 = (g24 ^ 1L);
        long g26 = (g25 ^ 1L);
        long g27 = (x0_7 | g23);
        long g28 = (g27 ^ x0_8);
        long g29 = (g28 ^ 1L);
        long g30 = (g29 ^ 1L);
        long g31 = (x0_8 | g27);
        long g32 = (g31 ^ x0_9);
        long g33 = (g32 ^ 1L);
        long g34 = (g33 ^ 1L);
        long g35 = (x0_9 | g31);
        long g36 = (g35 ^ x0_10);
        long g37 = (g36 ^ 1L);
        long g38 = (g37 ^ 1L);
        long g39 = (x0_10 | g35);
        long g40 = (g39 ^ x0_11);
        long g41 = (g40 ^ 1L);
        long g42 = (g41 ^ 1L);
        long g43 = (x0_11 | g39);
        long g44 = (g43 ^ x0_12);
        long g45 = (g44 ^ 1L);
        long g46 = (g45 ^ 1L);
        long g47 = (x0_12 | g43);
        long g48 = (g47 ^ x0_13);
        long g49 = (g48 ^ 1L);
        long g50 = (g49 ^ 1L);
        long g51 = (x0_13 | g47);
        long g52 = (g51 ^ x0_14);
        long g53 = (g52 ^ 1L);
        long g54 = (g53 ^ 1L);
        long g55 = (x0_14 | g51);
        long g56 = (g55 ^ x0_15);
        long g57 = (g56 ^ 1L);
        long g58 = (g57 ^ 1L);
        long g59 = (x0_15 | g55);
        long g60 = (g59 ^ x0_16);
        long g61 = (g60 ^ 1L);
        long g62 = (g61 ^ 1L);
        long g63 = (x0_16 | g59);
        long g64 = (g63 ^ x0_17);
        long g65 = (g64 ^ 1L);
        long g66 = (g65 ^ 1L);
        long g67 = (x0_17 | g63);
        long g68 = (g67 ^ x0_18);
        long g69 = (g68 ^ 1L);
        long g70 = (g69 ^ 1L);
        long g71 = (x0_18 | g67);
        long g72 = (g71 ^ x0_19);
        long g73 = (g72 ^ 1L);
        long g74 = (g73 ^ 1L);
        long g75 = (x0_19 | g71);
        long g76 = (g75 ^ x0_20);
        long g77 = (g76 ^ 1L);
        long g78 = (g77 ^ 1L);
        long g79 = (x0_20 | g75);
        long g80 = (g79 ^ x0_21);
        long g81 = (g80 ^ 1L);
        long g82 = (g81 ^ 1L);
        long g83 = (x0_21 | g79);
        long g84 = (g83 ^ x0_22);
        long g85 = (g84 ^ 1L);
        long g86 = (g85 ^ 1L);
        long g87 = (x0_22 | g83);
        long g88 = (g87 ^ x0_23);
        long g89 = (g88 ^ 1L);
        long g90 = (g89 ^ 1L);
        long g91 = (x0_23 | g87);
        long g92 = (g91 ^ x0_24);
        long g93 = (g92 ^ 1L);
        long g94 = (g93 ^ 1L);
        long g95 = (x0_24 | g91);
        long g96 = (g95 ^ x0_25);
        long g97 = (g96 ^ 1L);
        long g98 = (g97 ^ 1L);
        long g99 = (x0_25 | g95);
        long g100 = (g99 ^ x0_26);
        long g101 = (g100 ^ 1L);
        long g102 = (g101 ^ 1L);
        long g103 = (x0_26 | g99);
        long g104 = (g103 ^ x0_27);
        long g105 = (g104 ^ 1L);
        long g106 = (g105 ^ 1L);
        long g107 = (x0_27 | g103);
        long g108 = (g107 ^ x0_28);
        long g109 = (g108 ^ 1L);
        long g110 = (g109 ^ 1L);
        long g111 = (x0_28 | g107);
        long g112 = (g111 ^ x0_29);
        long g113 = (g112 ^ 1L);
        long g114 = (g113 ^ 1L);
        long g115 = (x0_29 | g111);
        long g116 = (g115 ^ x0_30);
        long g117 = (g116 ^ 1L);
        long g118 = (g117 ^ 1L);
        long g119 = (x0_30 | g115);
        long g120 = (g119 ^ x0_31);
        long g121 = (g120 ^ 1L);
        long g122 = (g121 ^ 1L);
        long g123 = (x0_31 | g119);
        long g124 = (g123 ^ x0_32);
        long g125 = (g124 ^ 1L);
        long g126 = (g125 ^ 1L);
        long g127 = (x0_32 | g123);
        long g128 = (g127 ^ x0_33);
        long g129 = (g128 ^ 1L);
        long g130 = (g129 ^ 1L);
        long g131 = (x0_33 | g127);
        long g132 = (g131 ^ x0_34);
        long g133 = (g132 ^ 1L);
        long g134 = (g133 ^ 1L);
        long g135 = (x0_34 | g131);
        long g136 = (g135 ^ x0_35);
        long g137 = (g136 ^ 1L);
        long g138 = (g137 ^ 1L);
        long g139 = (x0_35 | g135);
        long g140 = (g139 ^ x0_36);
        long g141 = (g140 ^ 1L);
        long g142 = (g141 ^ 1L);
        long g143 = (x0_36 | g139);
        long g144 = (g143 ^ x0_37);
        long g145 = (g144 ^ 1L);
        long g146 = (g145 ^ 1L);
        long g147 = (x0_37 | g143);
        long g148 = (g147 ^ x0_38);
        long g149 = (g148 ^ 1L);
        long g150 = (g149 ^ 1L);
        long g151 = (x0_38 | g147);
        long g152 = (g151 ^ x0_39);
        long g153 = (g152 ^ 1L);
        long g154 = (g153 ^ 1L);
        long g155 = (x0_39 | g151);
        long g156 = (g155 ^ x0_40);
        long g157 = (g156 ^ 1L);
        long g158 = (g157 ^ 1L);
        long g159 = (x0_40 | g155);
        long g160 = (g159 ^ x0_41);
        long g161 = (g160 ^ 1L);
        long g162 = (g161 ^ 1L);
        long g163 = (x0_41 | g159);
        long g164 = (g163 ^ x0_42);
        long g165 = (g164 ^ 1L);
        long g166 = (g165 ^ 1L);
        long g167 = (x0_42 | g163);
        long g168 = (g167 ^ x0_43);
        long g169 = (g168 ^ 1L);
        long g170 = (g169 ^ 1L);
        long g171 = (x0_43 | g167);
        long g172 = (g171 ^ x0_44);
        long g173 = (g172 ^ 1L);
        long g174 = (g173 ^ 1L);
        long g175 = (x0_44 | g171);
        long g176 = (g175 ^ x0_45);
        long g177 = (g176 ^ 1L);
        long g178 = (g177 ^ 1L);
        long g179 = (x0_45 | g175);
        long g180 = (g179 ^ x0_46);
        long g181 = (g180 ^ 1L);
        long g182 = (g181 ^ 1L);
        long g183 = (x0_46 | g179);
        long g184 = (g183 ^ x0_47);
        long g185 = (g184 ^ 1L);
        long g186 = (g185 ^ 1L);
        long g187 = (x0_47 | g183);
        long g188 = (g187 ^ x0_48);
        long g189 = (g188 ^ 1L);
        long g190 = (g189 ^ 1L);
        long g191 = (x0_48 | g187);
        long g192 = (g191 ^ x0_49);
        long g193 = (g192 ^ 1L);
        long g194 = (g193 ^ 1L);
        long g195 = (x0_49 | g191);
        long g196 = (g195 ^ x0_50);
        long g197 = (g196 ^ 1L);
        long g198 = (g197 ^ 1L);
        long g199 = (x0_50 | g195);
        long g200 = (g199 ^ x0_51);
        long g201 = (g200 ^ 1L);
        long g202 = (g201 ^ 1L);
        long g203 = (x0_51 | g199);
        long g204 = (g203 ^ x0_52);
        long g205 = (g204 ^ 1L);
        long g206 = (g205 ^ 1L);
        long g207 = (x0_52 | g203);
        long g208 = (g207 ^ x0_53);
        long g209 = (g208 ^ 1L);
        long g210 = (g209 ^ 1L);
        long g211 = (x0_53 | g207);
        long g212 = (g211 ^ x0_54);
        long g213 = (g212 ^ 1L);
        long g214 = (g213 ^ 1L);
        long g215 = (x0_54 | g211);
        long g216 = (g215 ^ x0_55);
        long g217 = (g216 ^ 1L);
        long g218 = (g217 ^ 1L);
        long g219 = (x0_55 | g215);
        long g220 = (g219 ^ x0_56);
        long g221 = (g220 ^ 1L);
        long g222 = (g221 ^ 1L);
        long g223 = (x0_56 | g219);
        long g224 = (g223 ^ x0_57);
        long g225 = (g224 ^ 1L);
        long g226 = (g225 ^ 1L);
        long g227 = (x0_57 | g223);
        long g228 = (g227 ^ x0_58);
        long g229 = (g228 ^ 1L);
        long g230 = (g229 ^ 1L);
        long g231 = (x0_58 | g227);
        long g232 = (g231 ^ x0_59);
        long g233 = (g232 ^ 1L);
        long g234 = (g233 ^ 1L);
        long g235 = (x0_59 | g231);
        long g236 = (g235 ^ x0_60);
        long g237 = (g236 ^ 1L);
        long g238 = (g237 ^ 1L);
        long g239 = (x0_60 | g235);
        long g240 = (g239 ^ x0_61);
        long g241 = (g240 ^ 1L);
        long g242 = (g241 ^ 1L);
        long g243 = (x0_61 | g239);
        long g244 = (g243 ^ x0_62);
        long g245 = (g244 ^ 1L);
        long g246 = (g245 ^ 1L);
        long g247 = (x0_62 | g243);
        long g248 = (g247 ^ x0_63);
        long g249 = (g248 ^ 1L);
        long g250 = (g249 ^ 1L);
        long w0 = g250;
        long w1 = cat(w0, g246, 1);
        long w2 = cat(w1, g242, 1);
        long w3 = cat(w2, g238, 1);
        long w4 = cat(w3, g234, 1);
        long w5 = cat(w4, g230, 1);
        long w6 = cat(w5, g226, 1);
        long w7 = cat(w6, g222, 1);
        long w8 = cat(w7, g218, 1);
        long w9 = cat(w8, g214, 1);
        long w10 = cat(w9, g210, 1);
        long w11 = cat(w10, g206, 1);
        long w12 = cat(w11, g202, 1);
        long w13 = cat(w12, g198, 1);
        long w14 = cat(w13, g194, 1);
        long w15 = cat(w14, g190, 1);
        long w16 = cat(w15, g186, 1);
        long w17 = cat(w16, g182, 1);
        long w18 = cat(w17, g178, 1);
        long w19 = cat(w18, g174, 1);
        long w20 = cat(w19, g170, 1);
        long w21 = cat(w20, g166, 1);
        long w22 = cat(w21, g162, 1);
        long w23 = cat(w22, g158, 1);
        long w24 = cat(w23, g154, 1);
        long w25 = cat(w24, g150, 1);
        long w26 = cat(w25, g146, 1);
        long w27 = cat(w26, g142, 1);
        long w28 = cat(w27, g138, 1);
        long w29 = cat(w28, g134, 1);
        long w30 = cat(w29, g130, 1);
        long w31 = cat(w30, g126, 1);
        long w32 = cat(w31, g122, 1);
        long w33 = cat(w32, g118, 1);
        long w34 = cat(w33, g114, 1);
        long w35 = cat(w34, g110, 1);
        long w36 = cat(w35, g106, 1);
        long w37 = cat(w36, g102, 1);
        long w38 = cat(w37, g98, 1);
        long w39 = cat(w38, g94, 1);
        long w40 = cat(w39, g90, 1);
        long w41 = cat(w40, g86, 1);
        long w42 = cat(w41, g82, 1);
        long w43 = cat(w42, g78, 1);
        long w44 = cat(w43, g74, 1);
        long w45 = cat(w44, g70, 1);
        long w46 = cat(w45, g66, 1);
        long w47 = cat(w46, g62, 1);
        long w48 = cat(w47, g58, 1);
        long w49 = cat(w48, g54, 1);
        long w50 = cat(w49, g50, 1);
        long w51 = cat(w50, g46, 1);
        long w52 = cat(w51, g42, 1);
        long w53 = cat(w52, g38, 1);
        long w54 = cat(w53, g34, 1);
        long w55 = cat(w54, g30, 1);
        long w56 = cat(w55, g26, 1);
        long w57 = cat(w56, g22, 1);
        long w58 = cat(w57, g18, 1);
        long w59 = cat(w58, g14, 1);
        long w60 = cat(w59, g10, 1);
        long w61 = cat(w60, g6, 1);
        long w62 = cat(w61, g2, 1);
        long w63 = cat(w62, x0_0, 1);
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
                    answers.append(Long.toUnsignedString(emu_neg_gpr_one_64__reg_rdi__java(values[0])));
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
