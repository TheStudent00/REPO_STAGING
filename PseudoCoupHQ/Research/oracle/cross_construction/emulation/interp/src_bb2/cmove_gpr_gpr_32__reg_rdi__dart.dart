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
// one named local per gate, over the term of cmove_gpr_gpr_32__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
int emu_cmove_gpr_gpr_32__reg_rdi__dart(int a, int b, int c, int d) {
  int x3_0 = ext(d, 0, 0);
  int x1_17 = ext(a, 17, 17);
  int x0_17 = ext(b, 17, 17);
  int x1_15 = ext(a, 15, 15);
  int x0_15 = ext(b, 15, 15);
  int x1_3 = ext(a, 3, 3);
  int x0_3 = ext(b, 3, 3);
  int x1_10 = ext(a, 10, 10);
  int x0_10 = ext(b, 10, 10);
  int x1_12 = ext(a, 12, 12);
  int x0_12 = ext(b, 12, 12);
  int x1_27 = ext(a, 27, 27);
  int x0_27 = ext(b, 27, 27);
  int x1_11 = ext(a, 11, 11);
  int x0_11 = ext(b, 11, 11);
  int x1_23 = ext(a, 23, 23);
  int x0_23 = ext(b, 23, 23);
  int x1_8 = ext(a, 8, 8);
  int x0_8 = ext(b, 8, 8);
  int x1_31 = ext(a, 31, 31);
  int x0_31 = ext(b, 31, 31);
  int x1_24 = ext(a, 24, 24);
  int x0_24 = ext(b, 24, 24);
  int x1_30 = ext(a, 30, 30);
  int x0_30 = ext(b, 30, 30);
  int x1_6 = ext(a, 6, 6);
  int x0_6 = ext(b, 6, 6);
  int x1_4 = ext(a, 4, 4);
  int x0_4 = ext(b, 4, 4);
  int x1_5 = ext(a, 5, 5);
  int x0_5 = ext(b, 5, 5);
  int x1_29 = ext(a, 29, 29);
  int x0_29 = ext(b, 29, 29);
  int x1_16 = ext(a, 16, 16);
  int x0_16 = ext(b, 16, 16);
  int x1_26 = ext(a, 26, 26);
  int x0_26 = ext(b, 26, 26);
  int x1_7 = ext(a, 7, 7);
  int x0_7 = ext(b, 7, 7);
  int x1_2 = ext(a, 2, 2);
  int x0_2 = ext(b, 2, 2);
  int x1_19 = ext(a, 19, 19);
  int x0_19 = ext(b, 19, 19);
  int x1_21 = ext(a, 21, 21);
  int x0_21 = ext(b, 21, 21);
  int x1_28 = ext(a, 28, 28);
  int x0_28 = ext(b, 28, 28);
  int x1_13 = ext(a, 13, 13);
  int x0_13 = ext(b, 13, 13);
  int x1_18 = ext(a, 18, 18);
  int x0_18 = ext(b, 18, 18);
  int x1_14 = ext(a, 14, 14);
  int x0_14 = ext(b, 14, 14);
  int x1_25 = ext(a, 25, 25);
  int x0_25 = ext(b, 25, 25);
  int x1_1 = ext(a, 1, 1);
  int x0_1 = ext(b, 1, 1);
  int x1_22 = ext(a, 22, 22);
  int x0_22 = ext(b, 22, 22);
  int x1_20 = ext(a, 20, 20);
  int x0_20 = ext(b, 20, 20);
  int x1_0 = ext(a, 0, 0);
  int x0_0 = ext(b, 0, 0);
  int x1_9 = ext(a, 9, 9);
  int x0_9 = ext(b, 9, 9);
  int x2_0 = ext(c, 0, 0);
  int x3_1 = ext(d, 1, 1);
  int x2_1 = ext(c, 1, 1);
  int x3_2 = ext(d, 2, 2);
  int x2_2 = ext(c, 2, 2);
  int x3_3 = ext(d, 3, 3);
  int x2_3 = ext(c, 3, 3);
  int x3_4 = ext(d, 4, 4);
  int x2_4 = ext(c, 4, 4);
  int x3_5 = ext(d, 5, 5);
  int x2_5 = ext(c, 5, 5);
  int x3_6 = ext(d, 6, 6);
  int x2_6 = ext(c, 6, 6);
  int x3_7 = ext(d, 7, 7);
  int x2_7 = ext(c, 7, 7);
  int x3_8 = ext(d, 8, 8);
  int x2_8 = ext(c, 8, 8);
  int x3_9 = ext(d, 9, 9);
  int x2_9 = ext(c, 9, 9);
  int x3_10 = ext(d, 10, 10);
  int x2_10 = ext(c, 10, 10);
  int x3_11 = ext(d, 11, 11);
  int x2_11 = ext(c, 11, 11);
  int x3_12 = ext(d, 12, 12);
  int x2_12 = ext(c, 12, 12);
  int x3_13 = ext(d, 13, 13);
  int x2_13 = ext(c, 13, 13);
  int x3_14 = ext(d, 14, 14);
  int x2_14 = ext(c, 14, 14);
  int x3_15 = ext(d, 15, 15);
  int x2_15 = ext(c, 15, 15);
  int x3_16 = ext(d, 16, 16);
  int x2_16 = ext(c, 16, 16);
  int x3_17 = ext(d, 17, 17);
  int x2_17 = ext(c, 17, 17);
  int x3_18 = ext(d, 18, 18);
  int x2_18 = ext(c, 18, 18);
  int x3_19 = ext(d, 19, 19);
  int x2_19 = ext(c, 19, 19);
  int x3_20 = ext(d, 20, 20);
  int x2_20 = ext(c, 20, 20);
  int x3_21 = ext(d, 21, 21);
  int x2_21 = ext(c, 21, 21);
  int x3_22 = ext(d, 22, 22);
  int x2_22 = ext(c, 22, 22);
  int x3_23 = ext(d, 23, 23);
  int x2_23 = ext(c, 23, 23);
  int x3_24 = ext(d, 24, 24);
  int x2_24 = ext(c, 24, 24);
  int x3_25 = ext(d, 25, 25);
  int x2_25 = ext(c, 25, 25);
  int x3_26 = ext(d, 26, 26);
  int x2_26 = ext(c, 26, 26);
  int x3_27 = ext(d, 27, 27);
  int x2_27 = ext(c, 27, 27);
  int x3_28 = ext(d, 28, 28);
  int x2_28 = ext(c, 28, 28);
  int x3_29 = ext(d, 29, 29);
  int x2_29 = ext(c, 29, 29);
  int x3_30 = ext(d, 30, 30);
  int x2_30 = ext(c, 30, 30);
  int x3_31 = ext(d, 31, 31);
  int x2_31 = ext(c, 31, 31);
  int g0 = (x1_17 ^ 1);
  int g1 = (x0_17 ^ 1);
  int g2 = (g1 | g0);
  int g3 = (g2 ^ 1);
  int g4 = (x1_15 ^ 1);
  int g5 = (x0_15 ^ 1);
  int g6 = (g5 | g4);
  int g7 = (g6 ^ 1);
  int g8 = (x1_3 ^ 1);
  int g9 = (x0_3 ^ 1);
  int g10 = (g9 | g8);
  int g11 = (g10 ^ 1);
  int g12 = (x1_10 ^ 1);
  int g13 = (x0_10 ^ 1);
  int g14 = (g13 | g12);
  int g15 = (g14 ^ 1);
  int g16 = (x1_12 ^ 1);
  int g17 = (x0_12 ^ 1);
  int g18 = (g17 | g16);
  int g19 = (g18 ^ 1);
  int g20 = (x1_27 ^ 1);
  int g21 = (x0_27 ^ 1);
  int g22 = (g21 | g20);
  int g23 = (g22 ^ 1);
  int g24 = (x1_11 ^ 1);
  int g25 = (x0_11 ^ 1);
  int g26 = (g25 | g24);
  int g27 = (g26 ^ 1);
  int g28 = (x1_23 ^ 1);
  int g29 = (x0_23 ^ 1);
  int g30 = (g29 | g28);
  int g31 = (g30 ^ 1);
  int g32 = (x1_8 ^ 1);
  int g33 = (x0_8 ^ 1);
  int g34 = (g33 | g32);
  int g35 = (g34 ^ 1);
  int g36 = (x1_31 ^ 1);
  int g37 = (x0_31 ^ 1);
  int g38 = (g37 | g36);
  int g39 = (g38 ^ 1);
  int g40 = (x1_24 ^ 1);
  int g41 = (x0_24 ^ 1);
  int g42 = (g41 | g40);
  int g43 = (g42 ^ 1);
  int g44 = (x1_30 ^ 1);
  int g45 = (x0_30 ^ 1);
  int g46 = (g45 | g44);
  int g47 = (g46 ^ 1);
  int g48 = (x1_6 ^ 1);
  int g49 = (x0_6 ^ 1);
  int g50 = (g49 | g48);
  int g51 = (g50 ^ 1);
  int g52 = (x1_4 ^ 1);
  int g53 = (x0_4 ^ 1);
  int g54 = (g53 | g52);
  int g55 = (g54 ^ 1);
  int g56 = (x1_5 ^ 1);
  int g57 = (x0_5 ^ 1);
  int g58 = (g57 | g56);
  int g59 = (g58 ^ 1);
  int g60 = (x1_29 ^ 1);
  int g61 = (x0_29 ^ 1);
  int g62 = (g61 | g60);
  int g63 = (g62 ^ 1);
  int g64 = (x1_16 ^ 1);
  int g65 = (x0_16 ^ 1);
  int g66 = (g65 | g64);
  int g67 = (g66 ^ 1);
  int g68 = (x1_26 ^ 1);
  int g69 = (x0_26 ^ 1);
  int g70 = (g69 | g68);
  int g71 = (g70 ^ 1);
  int g72 = (x1_7 ^ 1);
  int g73 = (x0_7 ^ 1);
  int g74 = (g73 | g72);
  int g75 = (g74 ^ 1);
  int g76 = (x1_2 ^ 1);
  int g77 = (x0_2 ^ 1);
  int g78 = (g77 | g76);
  int g79 = (g78 ^ 1);
  int g80 = (x1_19 ^ 1);
  int g81 = (x0_19 ^ 1);
  int g82 = (g81 | g80);
  int g83 = (g82 ^ 1);
  int g84 = (x1_21 ^ 1);
  int g85 = (x0_21 ^ 1);
  int g86 = (g85 | g84);
  int g87 = (g86 ^ 1);
  int g88 = (x1_28 ^ 1);
  int g89 = (x0_28 ^ 1);
  int g90 = (g89 | g88);
  int g91 = (g90 ^ 1);
  int g92 = (x1_13 ^ 1);
  int g93 = (x0_13 ^ 1);
  int g94 = (g93 | g92);
  int g95 = (g94 ^ 1);
  int g96 = (x1_18 ^ 1);
  int g97 = (x0_18 ^ 1);
  int g98 = (g97 | g96);
  int g99 = (g98 ^ 1);
  int g100 = (x1_14 ^ 1);
  int g101 = (x0_14 ^ 1);
  int g102 = (g101 | g100);
  int g103 = (g102 ^ 1);
  int g104 = (x1_25 ^ 1);
  int g105 = (x0_25 ^ 1);
  int g106 = (g105 | g104);
  int g107 = (g106 ^ 1);
  int g108 = (x1_1 ^ 1);
  int g109 = (x0_1 ^ 1);
  int g110 = (g109 | g108);
  int g111 = (g110 ^ 1);
  int g112 = (x1_22 ^ 1);
  int g113 = (x0_22 ^ 1);
  int g114 = (g113 | g112);
  int g115 = (g114 ^ 1);
  int g116 = (x1_20 ^ 1);
  int g117 = (x0_20 ^ 1);
  int g118 = (g117 | g116);
  int g119 = (g118 ^ 1);
  int g120 = (x1_0 ^ 1);
  int g121 = (x0_0 ^ 1);
  int g122 = (g121 | g120);
  int g123 = (g122 ^ 1);
  int g124 = (x1_9 ^ 1);
  int g125 = (x0_9 ^ 1);
  int g126 = (g125 | g124);
  int g127 = (g126 ^ 1);
  int g128 = (g127 | g123);
  int g129 = (g128 | g119);
  int g130 = (g129 | g115);
  int g131 = (g130 | g111);
  int g132 = (g131 | g107);
  int g133 = (g132 | g103);
  int g134 = (g133 | g99);
  int g135 = (g134 | g95);
  int g136 = (g135 | g91);
  int g137 = (g136 | g87);
  int g138 = (g137 | g83);
  int g139 = (g138 | g79);
  int g140 = (g139 | g75);
  int g141 = (g140 | g71);
  int g142 = (g141 | g67);
  int g143 = (g142 | g63);
  int g144 = (g143 | g59);
  int g145 = (g144 | g55);
  int g146 = (g145 | g51);
  int g147 = (g146 | g47);
  int g148 = (g147 | g43);
  int g149 = (g148 | g39);
  int g150 = (g149 | g35);
  int g151 = (g150 | g31);
  int g152 = (g151 | g27);
  int g153 = (g152 | g23);
  int g154 = (g153 | g19);
  int g155 = (g154 | g15);
  int g156 = (g155 | g11);
  int g157 = (g156 | g7);
  int g158 = (g157 | g3);
  int g159 = (g158 ^ 1);
  int g160 = (g159 ^ 1);
  int g161 = (g160 & x3_0);
  int g162 = (g159 & x2_0);
  int g163 = (g162 | g161);
  int g164 = (g160 & x3_1);
  int g165 = (g159 & x2_1);
  int g166 = (g165 | g164);
  int g167 = (g160 & x3_2);
  int g168 = (g159 & x2_2);
  int g169 = (g168 | g167);
  int g170 = (g160 & x3_3);
  int g171 = (g159 & x2_3);
  int g172 = (g171 | g170);
  int g173 = (g160 & x3_4);
  int g174 = (g159 & x2_4);
  int g175 = (g174 | g173);
  int g176 = (g160 & x3_5);
  int g177 = (g159 & x2_5);
  int g178 = (g177 | g176);
  int g179 = (g160 & x3_6);
  int g180 = (g159 & x2_6);
  int g181 = (g180 | g179);
  int g182 = (g160 & x3_7);
  int g183 = (g159 & x2_7);
  int g184 = (g183 | g182);
  int g185 = (g160 & x3_8);
  int g186 = (g159 & x2_8);
  int g187 = (g186 | g185);
  int g188 = (g160 & x3_9);
  int g189 = (g159 & x2_9);
  int g190 = (g189 | g188);
  int g191 = (g160 & x3_10);
  int g192 = (g159 & x2_10);
  int g193 = (g192 | g191);
  int g194 = (g160 & x3_11);
  int g195 = (g159 & x2_11);
  int g196 = (g195 | g194);
  int g197 = (g160 & x3_12);
  int g198 = (g159 & x2_12);
  int g199 = (g198 | g197);
  int g200 = (g160 & x3_13);
  int g201 = (g159 & x2_13);
  int g202 = (g201 | g200);
  int g203 = (g160 & x3_14);
  int g204 = (g159 & x2_14);
  int g205 = (g204 | g203);
  int g206 = (g160 & x3_15);
  int g207 = (g159 & x2_15);
  int g208 = (g207 | g206);
  int g209 = (g160 & x3_16);
  int g210 = (g159 & x2_16);
  int g211 = (g210 | g209);
  int g212 = (g160 & x3_17);
  int g213 = (g159 & x2_17);
  int g214 = (g213 | g212);
  int g215 = (g160 & x3_18);
  int g216 = (g159 & x2_18);
  int g217 = (g216 | g215);
  int g218 = (g160 & x3_19);
  int g219 = (g159 & x2_19);
  int g220 = (g219 | g218);
  int g221 = (g160 & x3_20);
  int g222 = (g159 & x2_20);
  int g223 = (g222 | g221);
  int g224 = (g160 & x3_21);
  int g225 = (g159 & x2_21);
  int g226 = (g225 | g224);
  int g227 = (g160 & x3_22);
  int g228 = (g159 & x2_22);
  int g229 = (g228 | g227);
  int g230 = (g160 & x3_23);
  int g231 = (g159 & x2_23);
  int g232 = (g231 | g230);
  int g233 = (g160 & x3_24);
  int g234 = (g159 & x2_24);
  int g235 = (g234 | g233);
  int g236 = (g160 & x3_25);
  int g237 = (g159 & x2_25);
  int g238 = (g237 | g236);
  int g239 = (g160 & x3_26);
  int g240 = (g159 & x2_26);
  int g241 = (g240 | g239);
  int g242 = (g160 & x3_27);
  int g243 = (g159 & x2_27);
  int g244 = (g243 | g242);
  int g245 = (g160 & x3_28);
  int g246 = (g159 & x2_28);
  int g247 = (g246 | g245);
  int g248 = (g160 & x3_29);
  int g249 = (g159 & x2_29);
  int g250 = (g249 | g248);
  int g251 = (g160 & x3_30);
  int g252 = (g159 & x2_30);
  int g253 = (g252 | g251);
  int g254 = (g160 & x3_31);
  int g255 = (g159 & x2_31);
  int g256 = (g255 | g254);
  int k0 = 0;
  int w0 = k0;
  int w1 = cat(w0, k0, 1);
  int w2 = cat(w1, k0, 1);
  int w3 = cat(w2, k0, 1);
  int w4 = cat(w3, k0, 1);
  int w5 = cat(w4, k0, 1);
  int w6 = cat(w5, k0, 1);
  int w7 = cat(w6, k0, 1);
  int w8 = cat(w7, k0, 1);
  int w9 = cat(w8, k0, 1);
  int w10 = cat(w9, k0, 1);
  int w11 = cat(w10, k0, 1);
  int w12 = cat(w11, k0, 1);
  int w13 = cat(w12, k0, 1);
  int w14 = cat(w13, k0, 1);
  int w15 = cat(w14, k0, 1);
  int w16 = cat(w15, k0, 1);
  int w17 = cat(w16, k0, 1);
  int w18 = cat(w17, k0, 1);
  int w19 = cat(w18, k0, 1);
  int w20 = cat(w19, k0, 1);
  int w21 = cat(w20, k0, 1);
  int w22 = cat(w21, k0, 1);
  int w23 = cat(w22, k0, 1);
  int w24 = cat(w23, k0, 1);
  int w25 = cat(w24, k0, 1);
  int w26 = cat(w25, k0, 1);
  int w27 = cat(w26, k0, 1);
  int w28 = cat(w27, k0, 1);
  int w29 = cat(w28, k0, 1);
  int w30 = cat(w29, k0, 1);
  int w31 = cat(w30, k0, 1);
  int w32 = cat(w31, g256, 1);
  int w33 = cat(w32, g253, 1);
  int w34 = cat(w33, g250, 1);
  int w35 = cat(w34, g247, 1);
  int w36 = cat(w35, g244, 1);
  int w37 = cat(w36, g241, 1);
  int w38 = cat(w37, g238, 1);
  int w39 = cat(w38, g235, 1);
  int w40 = cat(w39, g232, 1);
  int w41 = cat(w40, g229, 1);
  int w42 = cat(w41, g226, 1);
  int w43 = cat(w42, g223, 1);
  int w44 = cat(w43, g220, 1);
  int w45 = cat(w44, g217, 1);
  int w46 = cat(w45, g214, 1);
  int w47 = cat(w46, g211, 1);
  int w48 = cat(w47, g208, 1);
  int w49 = cat(w48, g205, 1);
  int w50 = cat(w49, g202, 1);
  int w51 = cat(w50, g199, 1);
  int w52 = cat(w51, g196, 1);
  int w53 = cat(w52, g193, 1);
  int w54 = cat(w53, g190, 1);
  int w55 = cat(w54, g187, 1);
  int w56 = cat(w55, g184, 1);
  int w57 = cat(w56, g181, 1);
  int w58 = cat(w57, g178, 1);
  int w59 = cat(w58, g175, 1);
  int w60 = cat(w59, g172, 1);
  int w61 = cat(w60, g169, 1);
  int w62 = cat(w61, g166, 1);
  int w63 = cat(w62, g163, 1);
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
        final int answer = emu_cmove_gpr_gpr_32__reg_rdi__dart(values[0], values[1], values[2], values[3]);
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
