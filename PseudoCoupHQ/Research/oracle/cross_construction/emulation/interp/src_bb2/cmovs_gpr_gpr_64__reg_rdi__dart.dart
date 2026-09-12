import 'dart:io';
import 'dart:typed_data';

final ByteData _view = ByteData(8);

int m(int x, int w) {
  if (w >= 64) { return x; }
  return x & ((1 << w) - 1);
}
int s(int x, int w) {
  if (w >= 64) { return x; }
  return (x << (64 - w)) >> (64 - w);
}
int add(int a, int b, int w) => m(a + b, w);
int sub(int a, int b, int w) => m(a - b, w);
int mul(int a, int b, int w) => m(a * b, w);
int band(int a, int b, int w) => m(a & b, w);
int bor(int a, int b, int w) => m(a | b, w);
int bxor(int a, int b, int w) => m(a ^ b, w);
int bnot(int a, int w) => m(~a, w);
int bneg(int a, int w) => m(-a, w);
int shl(int a, int n, int w) {
  if (n >= w) { return 0; }
  return m(a << n, w);
}
int lshr(int a, int n, int w) {
  if (n >= w) { return 0; }
  return m(m(a, w) >>> n, w);
}
int ashr(int a, int n, int w) {
  final int v = s(a, w);
  int k = n;
  if (k >= w) { k = w - 1; }
  return m(v >> k, w);
}
int udiv(int a, int b, int w) {
  if (w < 64) { return m(m(a, w) ~/ m(b, w), w); }
  if (b < 0) { return uge(a, b, 64) ? 1 : 0; }
  if (a >= 0) { return a ~/ b; }
  final int q = (a >>> 1) ~/ b << 1;
  final int r = a - q * b;
  return uge(r, b, 64) ? q + 1 : q;
}
int urem(int a, int b, int w) {
  if (w < 64) { return m(m(a, w) % m(b, w), w); }
  return sub(a, mul(udiv(a, b, 64), b, 64), 64);
}
int sdiv(int a, int b, int w) => m(s(a, w) ~/ s(b, w), w);
int srem(int a, int b, int w) => m(s(a, w).remainder(s(b, w)), w);
bool ult(int a, int b, int w) {
  if (w < 64) { return m(a, w) < m(b, w); }
  if ((a < 0) == (b < 0)) { return a < b; }
  return b < 0;
}
bool ule(int a, int b, int w) => ult(a, b, w) || m(a, w) == m(b, w);
bool ugt(int a, int b, int w) => !ule(a, b, w);
bool uge(int a, int b, int w) => !ult(a, b, w);
bool slt(int a, int b, int w) => s(a, w) < s(b, w);
bool sle(int a, int b, int w) => s(a, w) <= s(b, w);
bool sgt(int a, int b, int w) => s(a, w) > s(b, w);
bool sge(int a, int b, int w) => s(a, w) >= s(b, w);
bool eq(int a, int b, int w) => m(a, w) == m(b, w);
bool ne(int a, int b, int w) => m(a, w) != m(b, w);
int cat(int hi, int lo, int lw) => (hi << lw) | m(lo, lw);
int ext(int x, int hi, int lo) => m(x >>> lo, hi - lo + 1);
int sext(int x, int fromw, int tow) => m(s(x, fromw), tow);
double b2f(int x, int w) {
  if (w == 32) {
    _view.setUint32(0, m(x, 32), Endian.little);
    return _view.getFloat32(0, Endian.little);
  }
  _view.setUint64(0, x, Endian.little);
  return _view.getFloat64(0, Endian.little);
}
int f2b(double f, int w) {
  if (w == 32) {
    _view.setFloat32(0, f, Endian.little);
    return _view.getUint32(0, Endian.little);
  }
  _view.setFloat64(0, f, Endian.little);
  return _view.getUint64(0, Endian.little);
}
int fadd(int a, int b, int w) => f2b(b2f(a, w) + b2f(b, w), w);
int fsub(int a, int b, int w) => f2b(b2f(a, w) - b2f(b, w), w);
int fmul(int a, int b, int w) => f2b(b2f(a, w) * b2f(b, w), w);
int fdiv(int a, int b, int w) => f2b(b2f(a, w) / b2f(b, w), w);
int i2f(int x, int fromw, int w) => f2b(s(x, fromw).toDouble(), w);
int u2f(int x, int fromw, int w) => f2b(m(x, fromw).toDouble(), w);
int fwiden(int x, int fromw, int w) => f2b(b2f(x, fromw), w);

// task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
// one named local per gate, over the term of cmovs_gpr_gpr_64__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
int emu_cmovs_gpr_gpr_64__reg_rdi__dart(int a, int b, int c, int d) {
  int x3_0 = ext(c, 0, 0);
  int x1_63 = ext(a, 63, 63);
  int x0_63 = ext(b, 63, 63);
  int x2_0 = ext(d, 0, 0);
  int x3_1 = ext(c, 1, 1);
  int x2_1 = ext(d, 1, 1);
  int x3_2 = ext(c, 2, 2);
  int x2_2 = ext(d, 2, 2);
  int x3_3 = ext(c, 3, 3);
  int x2_3 = ext(d, 3, 3);
  int x3_4 = ext(c, 4, 4);
  int x2_4 = ext(d, 4, 4);
  int x3_5 = ext(c, 5, 5);
  int x2_5 = ext(d, 5, 5);
  int x3_6 = ext(c, 6, 6);
  int x2_6 = ext(d, 6, 6);
  int x3_7 = ext(c, 7, 7);
  int x2_7 = ext(d, 7, 7);
  int x3_8 = ext(c, 8, 8);
  int x2_8 = ext(d, 8, 8);
  int x3_9 = ext(c, 9, 9);
  int x2_9 = ext(d, 9, 9);
  int x3_10 = ext(c, 10, 10);
  int x2_10 = ext(d, 10, 10);
  int x3_11 = ext(c, 11, 11);
  int x2_11 = ext(d, 11, 11);
  int x3_12 = ext(c, 12, 12);
  int x2_12 = ext(d, 12, 12);
  int x3_13 = ext(c, 13, 13);
  int x2_13 = ext(d, 13, 13);
  int x3_14 = ext(c, 14, 14);
  int x2_14 = ext(d, 14, 14);
  int x3_15 = ext(c, 15, 15);
  int x2_15 = ext(d, 15, 15);
  int x3_16 = ext(c, 16, 16);
  int x2_16 = ext(d, 16, 16);
  int x3_17 = ext(c, 17, 17);
  int x2_17 = ext(d, 17, 17);
  int x3_18 = ext(c, 18, 18);
  int x2_18 = ext(d, 18, 18);
  int x3_19 = ext(c, 19, 19);
  int x2_19 = ext(d, 19, 19);
  int x3_20 = ext(c, 20, 20);
  int x2_20 = ext(d, 20, 20);
  int x3_21 = ext(c, 21, 21);
  int x2_21 = ext(d, 21, 21);
  int x3_22 = ext(c, 22, 22);
  int x2_22 = ext(d, 22, 22);
  int x3_23 = ext(c, 23, 23);
  int x2_23 = ext(d, 23, 23);
  int x3_24 = ext(c, 24, 24);
  int x2_24 = ext(d, 24, 24);
  int x3_25 = ext(c, 25, 25);
  int x2_25 = ext(d, 25, 25);
  int x3_26 = ext(c, 26, 26);
  int x2_26 = ext(d, 26, 26);
  int x3_27 = ext(c, 27, 27);
  int x2_27 = ext(d, 27, 27);
  int x3_28 = ext(c, 28, 28);
  int x2_28 = ext(d, 28, 28);
  int x3_29 = ext(c, 29, 29);
  int x2_29 = ext(d, 29, 29);
  int x3_30 = ext(c, 30, 30);
  int x2_30 = ext(d, 30, 30);
  int x3_31 = ext(c, 31, 31);
  int x2_31 = ext(d, 31, 31);
  int x3_32 = ext(c, 32, 32);
  int x2_32 = ext(d, 32, 32);
  int x3_33 = ext(c, 33, 33);
  int x2_33 = ext(d, 33, 33);
  int x3_34 = ext(c, 34, 34);
  int x2_34 = ext(d, 34, 34);
  int x3_35 = ext(c, 35, 35);
  int x2_35 = ext(d, 35, 35);
  int x3_36 = ext(c, 36, 36);
  int x2_36 = ext(d, 36, 36);
  int x3_37 = ext(c, 37, 37);
  int x2_37 = ext(d, 37, 37);
  int x3_38 = ext(c, 38, 38);
  int x2_38 = ext(d, 38, 38);
  int x3_39 = ext(c, 39, 39);
  int x2_39 = ext(d, 39, 39);
  int x3_40 = ext(c, 40, 40);
  int x2_40 = ext(d, 40, 40);
  int x3_41 = ext(c, 41, 41);
  int x2_41 = ext(d, 41, 41);
  int x3_42 = ext(c, 42, 42);
  int x2_42 = ext(d, 42, 42);
  int x3_43 = ext(c, 43, 43);
  int x2_43 = ext(d, 43, 43);
  int x3_44 = ext(c, 44, 44);
  int x2_44 = ext(d, 44, 44);
  int x3_45 = ext(c, 45, 45);
  int x2_45 = ext(d, 45, 45);
  int x3_46 = ext(c, 46, 46);
  int x2_46 = ext(d, 46, 46);
  int x3_47 = ext(c, 47, 47);
  int x2_47 = ext(d, 47, 47);
  int x3_48 = ext(c, 48, 48);
  int x2_48 = ext(d, 48, 48);
  int x3_49 = ext(c, 49, 49);
  int x2_49 = ext(d, 49, 49);
  int x3_50 = ext(c, 50, 50);
  int x2_50 = ext(d, 50, 50);
  int x3_51 = ext(c, 51, 51);
  int x2_51 = ext(d, 51, 51);
  int x3_52 = ext(c, 52, 52);
  int x2_52 = ext(d, 52, 52);
  int x3_53 = ext(c, 53, 53);
  int x2_53 = ext(d, 53, 53);
  int x3_54 = ext(c, 54, 54);
  int x2_54 = ext(d, 54, 54);
  int x3_55 = ext(c, 55, 55);
  int x2_55 = ext(d, 55, 55);
  int x3_56 = ext(c, 56, 56);
  int x2_56 = ext(d, 56, 56);
  int x3_57 = ext(c, 57, 57);
  int x2_57 = ext(d, 57, 57);
  int x3_58 = ext(c, 58, 58);
  int x2_58 = ext(d, 58, 58);
  int x3_59 = ext(c, 59, 59);
  int x2_59 = ext(d, 59, 59);
  int x3_60 = ext(c, 60, 60);
  int x2_60 = ext(d, 60, 60);
  int x3_61 = ext(c, 61, 61);
  int x2_61 = ext(d, 61, 61);
  int x3_62 = ext(c, 62, 62);
  int x2_62 = ext(d, 62, 62);
  int x3_63 = ext(c, 63, 63);
  int x2_63 = ext(d, 63, 63);
  int g0 = (x1_63 ^ 1);
  int g1 = (x0_63 ^ 1);
  int g2 = (g1 | g0);
  int g3 = (g2 ^ 1);
  int g4 = (g3 & x3_0);
  int g5 = (g2 & x2_0);
  int g6 = (g5 | g4);
  int g7 = (g3 & x3_1);
  int g8 = (g2 & x2_1);
  int g9 = (g8 | g7);
  int g10 = (g3 & x3_2);
  int g11 = (g2 & x2_2);
  int g12 = (g11 | g10);
  int g13 = (g3 & x3_3);
  int g14 = (g2 & x2_3);
  int g15 = (g14 | g13);
  int g16 = (g3 & x3_4);
  int g17 = (g2 & x2_4);
  int g18 = (g17 | g16);
  int g19 = (g3 & x3_5);
  int g20 = (g2 & x2_5);
  int g21 = (g20 | g19);
  int g22 = (g3 & x3_6);
  int g23 = (g2 & x2_6);
  int g24 = (g23 | g22);
  int g25 = (g3 & x3_7);
  int g26 = (g2 & x2_7);
  int g27 = (g26 | g25);
  int g28 = (g3 & x3_8);
  int g29 = (g2 & x2_8);
  int g30 = (g29 | g28);
  int g31 = (g3 & x3_9);
  int g32 = (g2 & x2_9);
  int g33 = (g32 | g31);
  int g34 = (g3 & x3_10);
  int g35 = (g2 & x2_10);
  int g36 = (g35 | g34);
  int g37 = (g3 & x3_11);
  int g38 = (g2 & x2_11);
  int g39 = (g38 | g37);
  int g40 = (g3 & x3_12);
  int g41 = (g2 & x2_12);
  int g42 = (g41 | g40);
  int g43 = (g3 & x3_13);
  int g44 = (g2 & x2_13);
  int g45 = (g44 | g43);
  int g46 = (g3 & x3_14);
  int g47 = (g2 & x2_14);
  int g48 = (g47 | g46);
  int g49 = (g3 & x3_15);
  int g50 = (g2 & x2_15);
  int g51 = (g50 | g49);
  int g52 = (g3 & x3_16);
  int g53 = (g2 & x2_16);
  int g54 = (g53 | g52);
  int g55 = (g3 & x3_17);
  int g56 = (g2 & x2_17);
  int g57 = (g56 | g55);
  int g58 = (g3 & x3_18);
  int g59 = (g2 & x2_18);
  int g60 = (g59 | g58);
  int g61 = (g3 & x3_19);
  int g62 = (g2 & x2_19);
  int g63 = (g62 | g61);
  int g64 = (g3 & x3_20);
  int g65 = (g2 & x2_20);
  int g66 = (g65 | g64);
  int g67 = (g3 & x3_21);
  int g68 = (g2 & x2_21);
  int g69 = (g68 | g67);
  int g70 = (g3 & x3_22);
  int g71 = (g2 & x2_22);
  int g72 = (g71 | g70);
  int g73 = (g3 & x3_23);
  int g74 = (g2 & x2_23);
  int g75 = (g74 | g73);
  int g76 = (g3 & x3_24);
  int g77 = (g2 & x2_24);
  int g78 = (g77 | g76);
  int g79 = (g3 & x3_25);
  int g80 = (g2 & x2_25);
  int g81 = (g80 | g79);
  int g82 = (g3 & x3_26);
  int g83 = (g2 & x2_26);
  int g84 = (g83 | g82);
  int g85 = (g3 & x3_27);
  int g86 = (g2 & x2_27);
  int g87 = (g86 | g85);
  int g88 = (g3 & x3_28);
  int g89 = (g2 & x2_28);
  int g90 = (g89 | g88);
  int g91 = (g3 & x3_29);
  int g92 = (g2 & x2_29);
  int g93 = (g92 | g91);
  int g94 = (g3 & x3_30);
  int g95 = (g2 & x2_30);
  int g96 = (g95 | g94);
  int g97 = (g3 & x3_31);
  int g98 = (g2 & x2_31);
  int g99 = (g98 | g97);
  int g100 = (g3 & x3_32);
  int g101 = (g2 & x2_32);
  int g102 = (g101 | g100);
  int g103 = (g3 & x3_33);
  int g104 = (g2 & x2_33);
  int g105 = (g104 | g103);
  int g106 = (g3 & x3_34);
  int g107 = (g2 & x2_34);
  int g108 = (g107 | g106);
  int g109 = (g3 & x3_35);
  int g110 = (g2 & x2_35);
  int g111 = (g110 | g109);
  int g112 = (g3 & x3_36);
  int g113 = (g2 & x2_36);
  int g114 = (g113 | g112);
  int g115 = (g3 & x3_37);
  int g116 = (g2 & x2_37);
  int g117 = (g116 | g115);
  int g118 = (g3 & x3_38);
  int g119 = (g2 & x2_38);
  int g120 = (g119 | g118);
  int g121 = (g3 & x3_39);
  int g122 = (g2 & x2_39);
  int g123 = (g122 | g121);
  int g124 = (g3 & x3_40);
  int g125 = (g2 & x2_40);
  int g126 = (g125 | g124);
  int g127 = (g3 & x3_41);
  int g128 = (g2 & x2_41);
  int g129 = (g128 | g127);
  int g130 = (g3 & x3_42);
  int g131 = (g2 & x2_42);
  int g132 = (g131 | g130);
  int g133 = (g3 & x3_43);
  int g134 = (g2 & x2_43);
  int g135 = (g134 | g133);
  int g136 = (g3 & x3_44);
  int g137 = (g2 & x2_44);
  int g138 = (g137 | g136);
  int g139 = (g3 & x3_45);
  int g140 = (g2 & x2_45);
  int g141 = (g140 | g139);
  int g142 = (g3 & x3_46);
  int g143 = (g2 & x2_46);
  int g144 = (g143 | g142);
  int g145 = (g3 & x3_47);
  int g146 = (g2 & x2_47);
  int g147 = (g146 | g145);
  int g148 = (g3 & x3_48);
  int g149 = (g2 & x2_48);
  int g150 = (g149 | g148);
  int g151 = (g3 & x3_49);
  int g152 = (g2 & x2_49);
  int g153 = (g152 | g151);
  int g154 = (g3 & x3_50);
  int g155 = (g2 & x2_50);
  int g156 = (g155 | g154);
  int g157 = (g3 & x3_51);
  int g158 = (g2 & x2_51);
  int g159 = (g158 | g157);
  int g160 = (g3 & x3_52);
  int g161 = (g2 & x2_52);
  int g162 = (g161 | g160);
  int g163 = (g3 & x3_53);
  int g164 = (g2 & x2_53);
  int g165 = (g164 | g163);
  int g166 = (g3 & x3_54);
  int g167 = (g2 & x2_54);
  int g168 = (g167 | g166);
  int g169 = (g3 & x3_55);
  int g170 = (g2 & x2_55);
  int g171 = (g170 | g169);
  int g172 = (g3 & x3_56);
  int g173 = (g2 & x2_56);
  int g174 = (g173 | g172);
  int g175 = (g3 & x3_57);
  int g176 = (g2 & x2_57);
  int g177 = (g176 | g175);
  int g178 = (g3 & x3_58);
  int g179 = (g2 & x2_58);
  int g180 = (g179 | g178);
  int g181 = (g3 & x3_59);
  int g182 = (g2 & x2_59);
  int g183 = (g182 | g181);
  int g184 = (g3 & x3_60);
  int g185 = (g2 & x2_60);
  int g186 = (g185 | g184);
  int g187 = (g3 & x3_61);
  int g188 = (g2 & x2_61);
  int g189 = (g188 | g187);
  int g190 = (g3 & x3_62);
  int g191 = (g2 & x2_62);
  int g192 = (g191 | g190);
  int g193 = (g3 & x3_63);
  int g194 = (g2 & x2_63);
  int g195 = (g194 | g193);
  int w0 = g195;
  int w1 = cat(w0, g192, 1);
  int w2 = cat(w1, g189, 1);
  int w3 = cat(w2, g186, 1);
  int w4 = cat(w3, g183, 1);
  int w5 = cat(w4, g180, 1);
  int w6 = cat(w5, g177, 1);
  int w7 = cat(w6, g174, 1);
  int w8 = cat(w7, g171, 1);
  int w9 = cat(w8, g168, 1);
  int w10 = cat(w9, g165, 1);
  int w11 = cat(w10, g162, 1);
  int w12 = cat(w11, g159, 1);
  int w13 = cat(w12, g156, 1);
  int w14 = cat(w13, g153, 1);
  int w15 = cat(w14, g150, 1);
  int w16 = cat(w15, g147, 1);
  int w17 = cat(w16, g144, 1);
  int w18 = cat(w17, g141, 1);
  int w19 = cat(w18, g138, 1);
  int w20 = cat(w19, g135, 1);
  int w21 = cat(w20, g132, 1);
  int w22 = cat(w21, g129, 1);
  int w23 = cat(w22, g126, 1);
  int w24 = cat(w23, g123, 1);
  int w25 = cat(w24, g120, 1);
  int w26 = cat(w25, g117, 1);
  int w27 = cat(w26, g114, 1);
  int w28 = cat(w27, g111, 1);
  int w29 = cat(w28, g108, 1);
  int w30 = cat(w29, g105, 1);
  int w31 = cat(w30, g102, 1);
  int w32 = cat(w31, g99, 1);
  int w33 = cat(w32, g96, 1);
  int w34 = cat(w33, g93, 1);
  int w35 = cat(w34, g90, 1);
  int w36 = cat(w35, g87, 1);
  int w37 = cat(w36, g84, 1);
  int w38 = cat(w37, g81, 1);
  int w39 = cat(w38, g78, 1);
  int w40 = cat(w39, g75, 1);
  int w41 = cat(w40, g72, 1);
  int w42 = cat(w41, g69, 1);
  int w43 = cat(w42, g66, 1);
  int w44 = cat(w43, g63, 1);
  int w45 = cat(w44, g60, 1);
  int w46 = cat(w45, g57, 1);
  int w47 = cat(w46, g54, 1);
  int w48 = cat(w47, g51, 1);
  int w49 = cat(w48, g48, 1);
  int w50 = cat(w49, g45, 1);
  int w51 = cat(w50, g42, 1);
  int w52 = cat(w51, g39, 1);
  int w53 = cat(w52, g36, 1);
  int w54 = cat(w53, g33, 1);
  int w55 = cat(w54, g30, 1);
  int w56 = cat(w55, g27, 1);
  int w57 = cat(w56, g24, 1);
  int w58 = cat(w57, g21, 1);
  int w59 = cat(w58, g18, 1);
  int w60 = cat(w59, g15, 1);
  int w61 = cat(w60, g12, 1);
  int w62 = cat(w61, g9, 1);
  int w63 = cat(w62, g6, 1);
  return m(w63, 64);
}



void main() {
  final StringBuffer out = StringBuffer();
  String? line = stdin.readLineSync();
  while (line != null) {
    final String text = line.trim();
    if (text.isNotEmpty) {
      final List<int> values = text
          .split(RegExp(r"\s+"))
          .map((one) => BigInt.parse(one).toSigned(64).toInt())
          .toList();
      try {
        final int answer = emu_cmovs_gpr_gpr_64__reg_rdi__dart(values[0], values[1], values[2], values[3]);
        out.writeln(answer < 0
            ? (BigInt.from(answer).toUnsigned(64)).toString()
            : answer.toString());
      } catch (problem) {
        out.writeln("RAISE:${problem.runtimeType}");
      }
    }
    line = stdin.readLineSync();
  }
  stdout.write(out.toString());
}
