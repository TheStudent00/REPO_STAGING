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
// one named local per gate, over the term of xor_gpr_gpr_64__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   v0 ^ v1
int emu_xor_gpr_gpr_64__reg_rdi__dart(int a, int b) {
  int x1_0 = ext(b, 0, 0);
  int x0_0 = ext(a, 0, 0);
  int x1_1 = ext(b, 1, 1);
  int x0_1 = ext(a, 1, 1);
  int x1_2 = ext(b, 2, 2);
  int x0_2 = ext(a, 2, 2);
  int x1_3 = ext(b, 3, 3);
  int x0_3 = ext(a, 3, 3);
  int x1_4 = ext(b, 4, 4);
  int x0_4 = ext(a, 4, 4);
  int x1_5 = ext(b, 5, 5);
  int x0_5 = ext(a, 5, 5);
  int x1_6 = ext(b, 6, 6);
  int x0_6 = ext(a, 6, 6);
  int x1_7 = ext(b, 7, 7);
  int x0_7 = ext(a, 7, 7);
  int x1_8 = ext(b, 8, 8);
  int x0_8 = ext(a, 8, 8);
  int x1_9 = ext(b, 9, 9);
  int x0_9 = ext(a, 9, 9);
  int x1_10 = ext(b, 10, 10);
  int x0_10 = ext(a, 10, 10);
  int x1_11 = ext(b, 11, 11);
  int x0_11 = ext(a, 11, 11);
  int x1_12 = ext(b, 12, 12);
  int x0_12 = ext(a, 12, 12);
  int x1_13 = ext(b, 13, 13);
  int x0_13 = ext(a, 13, 13);
  int x1_14 = ext(b, 14, 14);
  int x0_14 = ext(a, 14, 14);
  int x1_15 = ext(b, 15, 15);
  int x0_15 = ext(a, 15, 15);
  int x1_16 = ext(b, 16, 16);
  int x0_16 = ext(a, 16, 16);
  int x1_17 = ext(b, 17, 17);
  int x0_17 = ext(a, 17, 17);
  int x1_18 = ext(b, 18, 18);
  int x0_18 = ext(a, 18, 18);
  int x1_19 = ext(b, 19, 19);
  int x0_19 = ext(a, 19, 19);
  int x1_20 = ext(b, 20, 20);
  int x0_20 = ext(a, 20, 20);
  int x1_21 = ext(b, 21, 21);
  int x0_21 = ext(a, 21, 21);
  int x1_22 = ext(b, 22, 22);
  int x0_22 = ext(a, 22, 22);
  int x1_23 = ext(b, 23, 23);
  int x0_23 = ext(a, 23, 23);
  int x1_24 = ext(b, 24, 24);
  int x0_24 = ext(a, 24, 24);
  int x1_25 = ext(b, 25, 25);
  int x0_25 = ext(a, 25, 25);
  int x1_26 = ext(b, 26, 26);
  int x0_26 = ext(a, 26, 26);
  int x1_27 = ext(b, 27, 27);
  int x0_27 = ext(a, 27, 27);
  int x1_28 = ext(b, 28, 28);
  int x0_28 = ext(a, 28, 28);
  int x1_29 = ext(b, 29, 29);
  int x0_29 = ext(a, 29, 29);
  int x1_30 = ext(b, 30, 30);
  int x0_30 = ext(a, 30, 30);
  int x1_31 = ext(b, 31, 31);
  int x0_31 = ext(a, 31, 31);
  int x1_32 = ext(b, 32, 32);
  int x0_32 = ext(a, 32, 32);
  int x1_33 = ext(b, 33, 33);
  int x0_33 = ext(a, 33, 33);
  int x1_34 = ext(b, 34, 34);
  int x0_34 = ext(a, 34, 34);
  int x1_35 = ext(b, 35, 35);
  int x0_35 = ext(a, 35, 35);
  int x1_36 = ext(b, 36, 36);
  int x0_36 = ext(a, 36, 36);
  int x1_37 = ext(b, 37, 37);
  int x0_37 = ext(a, 37, 37);
  int x1_38 = ext(b, 38, 38);
  int x0_38 = ext(a, 38, 38);
  int x1_39 = ext(b, 39, 39);
  int x0_39 = ext(a, 39, 39);
  int x1_40 = ext(b, 40, 40);
  int x0_40 = ext(a, 40, 40);
  int x1_41 = ext(b, 41, 41);
  int x0_41 = ext(a, 41, 41);
  int x1_42 = ext(b, 42, 42);
  int x0_42 = ext(a, 42, 42);
  int x1_43 = ext(b, 43, 43);
  int x0_43 = ext(a, 43, 43);
  int x1_44 = ext(b, 44, 44);
  int x0_44 = ext(a, 44, 44);
  int x1_45 = ext(b, 45, 45);
  int x0_45 = ext(a, 45, 45);
  int x1_46 = ext(b, 46, 46);
  int x0_46 = ext(a, 46, 46);
  int x1_47 = ext(b, 47, 47);
  int x0_47 = ext(a, 47, 47);
  int x1_48 = ext(b, 48, 48);
  int x0_48 = ext(a, 48, 48);
  int x1_49 = ext(b, 49, 49);
  int x0_49 = ext(a, 49, 49);
  int x1_50 = ext(b, 50, 50);
  int x0_50 = ext(a, 50, 50);
  int x1_51 = ext(b, 51, 51);
  int x0_51 = ext(a, 51, 51);
  int x1_52 = ext(b, 52, 52);
  int x0_52 = ext(a, 52, 52);
  int x1_53 = ext(b, 53, 53);
  int x0_53 = ext(a, 53, 53);
  int x1_54 = ext(b, 54, 54);
  int x0_54 = ext(a, 54, 54);
  int x1_55 = ext(b, 55, 55);
  int x0_55 = ext(a, 55, 55);
  int x1_56 = ext(b, 56, 56);
  int x0_56 = ext(a, 56, 56);
  int x1_57 = ext(b, 57, 57);
  int x0_57 = ext(a, 57, 57);
  int x1_58 = ext(b, 58, 58);
  int x0_58 = ext(a, 58, 58);
  int x1_59 = ext(b, 59, 59);
  int x0_59 = ext(a, 59, 59);
  int x1_60 = ext(b, 60, 60);
  int x0_60 = ext(a, 60, 60);
  int x1_61 = ext(b, 61, 61);
  int x0_61 = ext(a, 61, 61);
  int x1_62 = ext(b, 62, 62);
  int x0_62 = ext(a, 62, 62);
  int x1_63 = ext(b, 63, 63);
  int x0_63 = ext(a, 63, 63);
  int g0 = (x0_0 ^ x1_0);
  int g1 = (g0 ^ 1);
  int g2 = (g1 ^ 1);
  int g3 = (x0_1 ^ x1_1);
  int g4 = (g3 ^ 1);
  int g5 = (g4 ^ 1);
  int g6 = (x0_2 ^ x1_2);
  int g7 = (g6 ^ 1);
  int g8 = (g7 ^ 1);
  int g9 = (x0_3 ^ x1_3);
  int g10 = (g9 ^ 1);
  int g11 = (g10 ^ 1);
  int g12 = (x0_4 ^ x1_4);
  int g13 = (g12 ^ 1);
  int g14 = (g13 ^ 1);
  int g15 = (x0_5 ^ x1_5);
  int g16 = (g15 ^ 1);
  int g17 = (g16 ^ 1);
  int g18 = (x0_6 ^ x1_6);
  int g19 = (g18 ^ 1);
  int g20 = (g19 ^ 1);
  int g21 = (x0_7 ^ x1_7);
  int g22 = (g21 ^ 1);
  int g23 = (g22 ^ 1);
  int g24 = (x0_8 ^ x1_8);
  int g25 = (g24 ^ 1);
  int g26 = (g25 ^ 1);
  int g27 = (x0_9 ^ x1_9);
  int g28 = (g27 ^ 1);
  int g29 = (g28 ^ 1);
  int g30 = (x0_10 ^ x1_10);
  int g31 = (g30 ^ 1);
  int g32 = (g31 ^ 1);
  int g33 = (x0_11 ^ x1_11);
  int g34 = (g33 ^ 1);
  int g35 = (g34 ^ 1);
  int g36 = (x0_12 ^ x1_12);
  int g37 = (g36 ^ 1);
  int g38 = (g37 ^ 1);
  int g39 = (x0_13 ^ x1_13);
  int g40 = (g39 ^ 1);
  int g41 = (g40 ^ 1);
  int g42 = (x0_14 ^ x1_14);
  int g43 = (g42 ^ 1);
  int g44 = (g43 ^ 1);
  int g45 = (x0_15 ^ x1_15);
  int g46 = (g45 ^ 1);
  int g47 = (g46 ^ 1);
  int g48 = (x0_16 ^ x1_16);
  int g49 = (g48 ^ 1);
  int g50 = (g49 ^ 1);
  int g51 = (x0_17 ^ x1_17);
  int g52 = (g51 ^ 1);
  int g53 = (g52 ^ 1);
  int g54 = (x0_18 ^ x1_18);
  int g55 = (g54 ^ 1);
  int g56 = (g55 ^ 1);
  int g57 = (x0_19 ^ x1_19);
  int g58 = (g57 ^ 1);
  int g59 = (g58 ^ 1);
  int g60 = (x0_20 ^ x1_20);
  int g61 = (g60 ^ 1);
  int g62 = (g61 ^ 1);
  int g63 = (x0_21 ^ x1_21);
  int g64 = (g63 ^ 1);
  int g65 = (g64 ^ 1);
  int g66 = (x0_22 ^ x1_22);
  int g67 = (g66 ^ 1);
  int g68 = (g67 ^ 1);
  int g69 = (x0_23 ^ x1_23);
  int g70 = (g69 ^ 1);
  int g71 = (g70 ^ 1);
  int g72 = (x0_24 ^ x1_24);
  int g73 = (g72 ^ 1);
  int g74 = (g73 ^ 1);
  int g75 = (x0_25 ^ x1_25);
  int g76 = (g75 ^ 1);
  int g77 = (g76 ^ 1);
  int g78 = (x0_26 ^ x1_26);
  int g79 = (g78 ^ 1);
  int g80 = (g79 ^ 1);
  int g81 = (x0_27 ^ x1_27);
  int g82 = (g81 ^ 1);
  int g83 = (g82 ^ 1);
  int g84 = (x0_28 ^ x1_28);
  int g85 = (g84 ^ 1);
  int g86 = (g85 ^ 1);
  int g87 = (x0_29 ^ x1_29);
  int g88 = (g87 ^ 1);
  int g89 = (g88 ^ 1);
  int g90 = (x0_30 ^ x1_30);
  int g91 = (g90 ^ 1);
  int g92 = (g91 ^ 1);
  int g93 = (x0_31 ^ x1_31);
  int g94 = (g93 ^ 1);
  int g95 = (g94 ^ 1);
  int g96 = (x0_32 ^ x1_32);
  int g97 = (g96 ^ 1);
  int g98 = (g97 ^ 1);
  int g99 = (x0_33 ^ x1_33);
  int g100 = (g99 ^ 1);
  int g101 = (g100 ^ 1);
  int g102 = (x0_34 ^ x1_34);
  int g103 = (g102 ^ 1);
  int g104 = (g103 ^ 1);
  int g105 = (x0_35 ^ x1_35);
  int g106 = (g105 ^ 1);
  int g107 = (g106 ^ 1);
  int g108 = (x0_36 ^ x1_36);
  int g109 = (g108 ^ 1);
  int g110 = (g109 ^ 1);
  int g111 = (x0_37 ^ x1_37);
  int g112 = (g111 ^ 1);
  int g113 = (g112 ^ 1);
  int g114 = (x0_38 ^ x1_38);
  int g115 = (g114 ^ 1);
  int g116 = (g115 ^ 1);
  int g117 = (x0_39 ^ x1_39);
  int g118 = (g117 ^ 1);
  int g119 = (g118 ^ 1);
  int g120 = (x0_40 ^ x1_40);
  int g121 = (g120 ^ 1);
  int g122 = (g121 ^ 1);
  int g123 = (x0_41 ^ x1_41);
  int g124 = (g123 ^ 1);
  int g125 = (g124 ^ 1);
  int g126 = (x0_42 ^ x1_42);
  int g127 = (g126 ^ 1);
  int g128 = (g127 ^ 1);
  int g129 = (x0_43 ^ x1_43);
  int g130 = (g129 ^ 1);
  int g131 = (g130 ^ 1);
  int g132 = (x0_44 ^ x1_44);
  int g133 = (g132 ^ 1);
  int g134 = (g133 ^ 1);
  int g135 = (x0_45 ^ x1_45);
  int g136 = (g135 ^ 1);
  int g137 = (g136 ^ 1);
  int g138 = (x0_46 ^ x1_46);
  int g139 = (g138 ^ 1);
  int g140 = (g139 ^ 1);
  int g141 = (x0_47 ^ x1_47);
  int g142 = (g141 ^ 1);
  int g143 = (g142 ^ 1);
  int g144 = (x0_48 ^ x1_48);
  int g145 = (g144 ^ 1);
  int g146 = (g145 ^ 1);
  int g147 = (x0_49 ^ x1_49);
  int g148 = (g147 ^ 1);
  int g149 = (g148 ^ 1);
  int g150 = (x0_50 ^ x1_50);
  int g151 = (g150 ^ 1);
  int g152 = (g151 ^ 1);
  int g153 = (x0_51 ^ x1_51);
  int g154 = (g153 ^ 1);
  int g155 = (g154 ^ 1);
  int g156 = (x0_52 ^ x1_52);
  int g157 = (g156 ^ 1);
  int g158 = (g157 ^ 1);
  int g159 = (x0_53 ^ x1_53);
  int g160 = (g159 ^ 1);
  int g161 = (g160 ^ 1);
  int g162 = (x0_54 ^ x1_54);
  int g163 = (g162 ^ 1);
  int g164 = (g163 ^ 1);
  int g165 = (x0_55 ^ x1_55);
  int g166 = (g165 ^ 1);
  int g167 = (g166 ^ 1);
  int g168 = (x0_56 ^ x1_56);
  int g169 = (g168 ^ 1);
  int g170 = (g169 ^ 1);
  int g171 = (x0_57 ^ x1_57);
  int g172 = (g171 ^ 1);
  int g173 = (g172 ^ 1);
  int g174 = (x0_58 ^ x1_58);
  int g175 = (g174 ^ 1);
  int g176 = (g175 ^ 1);
  int g177 = (x0_59 ^ x1_59);
  int g178 = (g177 ^ 1);
  int g179 = (g178 ^ 1);
  int g180 = (x0_60 ^ x1_60);
  int g181 = (g180 ^ 1);
  int g182 = (g181 ^ 1);
  int g183 = (x0_61 ^ x1_61);
  int g184 = (g183 ^ 1);
  int g185 = (g184 ^ 1);
  int g186 = (x0_62 ^ x1_62);
  int g187 = (g186 ^ 1);
  int g188 = (g187 ^ 1);
  int g189 = (x0_63 ^ x1_63);
  int g190 = (g189 ^ 1);
  int g191 = (g190 ^ 1);
  int w0 = g191;
  int w1 = cat(w0, g188, 1);
  int w2 = cat(w1, g185, 1);
  int w3 = cat(w2, g182, 1);
  int w4 = cat(w3, g179, 1);
  int w5 = cat(w4, g176, 1);
  int w6 = cat(w5, g173, 1);
  int w7 = cat(w6, g170, 1);
  int w8 = cat(w7, g167, 1);
  int w9 = cat(w8, g164, 1);
  int w10 = cat(w9, g161, 1);
  int w11 = cat(w10, g158, 1);
  int w12 = cat(w11, g155, 1);
  int w13 = cat(w12, g152, 1);
  int w14 = cat(w13, g149, 1);
  int w15 = cat(w14, g146, 1);
  int w16 = cat(w15, g143, 1);
  int w17 = cat(w16, g140, 1);
  int w18 = cat(w17, g137, 1);
  int w19 = cat(w18, g134, 1);
  int w20 = cat(w19, g131, 1);
  int w21 = cat(w20, g128, 1);
  int w22 = cat(w21, g125, 1);
  int w23 = cat(w22, g122, 1);
  int w24 = cat(w23, g119, 1);
  int w25 = cat(w24, g116, 1);
  int w26 = cat(w25, g113, 1);
  int w27 = cat(w26, g110, 1);
  int w28 = cat(w27, g107, 1);
  int w29 = cat(w28, g104, 1);
  int w30 = cat(w29, g101, 1);
  int w31 = cat(w30, g98, 1);
  int w32 = cat(w31, g95, 1);
  int w33 = cat(w32, g92, 1);
  int w34 = cat(w33, g89, 1);
  int w35 = cat(w34, g86, 1);
  int w36 = cat(w35, g83, 1);
  int w37 = cat(w36, g80, 1);
  int w38 = cat(w37, g77, 1);
  int w39 = cat(w38, g74, 1);
  int w40 = cat(w39, g71, 1);
  int w41 = cat(w40, g68, 1);
  int w42 = cat(w41, g65, 1);
  int w43 = cat(w42, g62, 1);
  int w44 = cat(w43, g59, 1);
  int w45 = cat(w44, g56, 1);
  int w46 = cat(w45, g53, 1);
  int w47 = cat(w46, g50, 1);
  int w48 = cat(w47, g47, 1);
  int w49 = cat(w48, g44, 1);
  int w50 = cat(w49, g41, 1);
  int w51 = cat(w50, g38, 1);
  int w52 = cat(w51, g35, 1);
  int w53 = cat(w52, g32, 1);
  int w54 = cat(w53, g29, 1);
  int w55 = cat(w54, g26, 1);
  int w56 = cat(w55, g23, 1);
  int w57 = cat(w56, g20, 1);
  int w58 = cat(w57, g17, 1);
  int w59 = cat(w58, g14, 1);
  int w60 = cat(w59, g11, 1);
  int w61 = cat(w60, g8, 1);
  int w62 = cat(w61, g5, 1);
  int w63 = cat(w62, g2, 1);
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
        final int answer = emu_xor_gpr_gpr_64__reg_rdi__dart(values[0], values[1]);
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
