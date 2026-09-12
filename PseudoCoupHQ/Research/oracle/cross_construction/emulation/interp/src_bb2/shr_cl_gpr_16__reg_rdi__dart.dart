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
// one named local per gate, over the term of shr_cl_gpr_16__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), LShR(Extract(15, 0, v0), Concat(0, Extract(4, 0, v1))))
int emu_shr_cl_gpr_16__reg_rdi__dart(int a, int b) {
  int x0_0 = ext(a, 0, 0);
  int x0_1 = ext(a, 1, 1);
  int x1_0 = ext(b, 0, 0);
  int x0_2 = ext(a, 2, 2);
  int x0_3 = ext(a, 3, 3);
  int x1_1 = ext(b, 1, 1);
  int x0_4 = ext(a, 4, 4);
  int x0_5 = ext(a, 5, 5);
  int x0_6 = ext(a, 6, 6);
  int x0_7 = ext(a, 7, 7);
  int x1_2 = ext(b, 2, 2);
  int x0_8 = ext(a, 8, 8);
  int x0_9 = ext(a, 9, 9);
  int x0_10 = ext(a, 10, 10);
  int x0_11 = ext(a, 11, 11);
  int x0_12 = ext(a, 12, 12);
  int x0_13 = ext(a, 13, 13);
  int x0_14 = ext(a, 14, 14);
  int x0_15 = ext(a, 15, 15);
  int x1_3 = ext(b, 3, 3);
  int x1_4 = ext(b, 4, 4);
  int x0_16 = ext(a, 16, 16);
  int x0_17 = ext(a, 17, 17);
  int x0_18 = ext(a, 18, 18);
  int x0_19 = ext(a, 19, 19);
  int x0_20 = ext(a, 20, 20);
  int x0_21 = ext(a, 21, 21);
  int x0_22 = ext(a, 22, 22);
  int x0_23 = ext(a, 23, 23);
  int x0_24 = ext(a, 24, 24);
  int x0_25 = ext(a, 25, 25);
  int x0_26 = ext(a, 26, 26);
  int x0_27 = ext(a, 27, 27);
  int x0_28 = ext(a, 28, 28);
  int x0_29 = ext(a, 29, 29);
  int x0_30 = ext(a, 30, 30);
  int x0_31 = ext(a, 31, 31);
  int x0_32 = ext(a, 32, 32);
  int x0_33 = ext(a, 33, 33);
  int x0_34 = ext(a, 34, 34);
  int x0_35 = ext(a, 35, 35);
  int x0_36 = ext(a, 36, 36);
  int x0_37 = ext(a, 37, 37);
  int x0_38 = ext(a, 38, 38);
  int x0_39 = ext(a, 39, 39);
  int x0_40 = ext(a, 40, 40);
  int x0_41 = ext(a, 41, 41);
  int x0_42 = ext(a, 42, 42);
  int x0_43 = ext(a, 43, 43);
  int x0_44 = ext(a, 44, 44);
  int x0_45 = ext(a, 45, 45);
  int x0_46 = ext(a, 46, 46);
  int x0_47 = ext(a, 47, 47);
  int x0_48 = ext(a, 48, 48);
  int x0_49 = ext(a, 49, 49);
  int x0_50 = ext(a, 50, 50);
  int x0_51 = ext(a, 51, 51);
  int x0_52 = ext(a, 52, 52);
  int x0_53 = ext(a, 53, 53);
  int x0_54 = ext(a, 54, 54);
  int x0_55 = ext(a, 55, 55);
  int x0_56 = ext(a, 56, 56);
  int x0_57 = ext(a, 57, 57);
  int x0_58 = ext(a, 58, 58);
  int x0_59 = ext(a, 59, 59);
  int x0_60 = ext(a, 60, 60);
  int x0_61 = ext(a, 61, 61);
  int x0_62 = ext(a, 62, 62);
  int x0_63 = ext(a, 63, 63);
  int g0 = (x1_0 ^ 1);
  int g1 = (x1_0 & x0_1);
  int g2 = (g0 & x0_0);
  int g3 = (g1 | g2);
  int g4 = (x1_0 ^ 1);
  int g5 = (x1_0 & x0_3);
  int g6 = (g4 & x0_2);
  int g7 = (g5 | g6);
  int g8 = (x1_1 ^ 1);
  int g9 = (x1_1 & g7);
  int g10 = (g8 & g3);
  int g11 = (g9 | g10);
  int g12 = (x1_0 ^ 1);
  int g13 = (x1_0 & x0_5);
  int g14 = (g12 & x0_4);
  int g15 = (g13 | g14);
  int g16 = (x1_0 ^ 1);
  int g17 = (x1_0 & x0_7);
  int g18 = (g16 & x0_6);
  int g19 = (g17 | g18);
  int g20 = (x1_1 ^ 1);
  int g21 = (x1_1 & g19);
  int g22 = (g20 & g15);
  int g23 = (g21 | g22);
  int g24 = (x1_2 ^ 1);
  int g25 = (x1_2 & g23);
  int g26 = (g24 & g11);
  int g27 = (g25 | g26);
  int g28 = (x1_0 ^ 1);
  int g29 = (x1_0 & x0_9);
  int g30 = (g28 & x0_8);
  int g31 = (g29 | g30);
  int g32 = (x1_0 ^ 1);
  int g33 = (x1_0 & x0_11);
  int g34 = (g32 & x0_10);
  int g35 = (g33 | g34);
  int g36 = (x1_1 ^ 1);
  int g37 = (x1_1 & g35);
  int g38 = (g36 & g31);
  int g39 = (g37 | g38);
  int g40 = (x1_0 ^ 1);
  int g41 = (x1_0 & x0_13);
  int g42 = (g40 & x0_12);
  int g43 = (g41 | g42);
  int g44 = (x1_0 ^ 1);
  int g45 = (x1_0 & x0_15);
  int g46 = (g44 & x0_14);
  int g47 = (g45 | g46);
  int g48 = (x1_1 ^ 1);
  int g49 = (x1_1 & g47);
  int g50 = (g48 & g43);
  int g51 = (g49 | g50);
  int g52 = (x1_2 ^ 1);
  int g53 = (x1_2 & g51);
  int g54 = (g52 & g39);
  int g55 = (g53 | g54);
  int g56 = (x1_3 ^ 1);
  int g57 = (x1_3 & g55);
  int g58 = (g56 & g27);
  int g59 = (g57 | g58);
  int g60 = (x1_4 ^ 1);
  int g61 = (g60 & g59);
  int g62 = (x1_0 ^ 1);
  int g63 = (x1_0 & x0_2);
  int g64 = (g62 & x0_1);
  int g65 = (g63 | g64);
  int g66 = (x1_0 ^ 1);
  int g67 = (x1_0 & x0_4);
  int g68 = (g66 & x0_3);
  int g69 = (g67 | g68);
  int g70 = (x1_1 ^ 1);
  int g71 = (x1_1 & g69);
  int g72 = (g70 & g65);
  int g73 = (g71 | g72);
  int g74 = (x1_0 ^ 1);
  int g75 = (x1_0 & x0_6);
  int g76 = (g74 & x0_5);
  int g77 = (g75 | g76);
  int g78 = (x1_0 ^ 1);
  int g79 = (x1_0 & x0_8);
  int g80 = (g78 & x0_7);
  int g81 = (g79 | g80);
  int g82 = (x1_1 ^ 1);
  int g83 = (x1_1 & g81);
  int g84 = (g82 & g77);
  int g85 = (g83 | g84);
  int g86 = (x1_2 ^ 1);
  int g87 = (x1_2 & g85);
  int g88 = (g86 & g73);
  int g89 = (g87 | g88);
  int g90 = (x1_0 ^ 1);
  int g91 = (x1_0 & x0_10);
  int g92 = (g90 & x0_9);
  int g93 = (g91 | g92);
  int g94 = (x1_0 ^ 1);
  int g95 = (x1_0 & x0_12);
  int g96 = (g94 & x0_11);
  int g97 = (g95 | g96);
  int g98 = (x1_1 ^ 1);
  int g99 = (x1_1 & g97);
  int g100 = (g98 & g93);
  int g101 = (g99 | g100);
  int g102 = (x1_0 ^ 1);
  int g103 = (x1_0 & x0_14);
  int g104 = (g102 & x0_13);
  int g105 = (g103 | g104);
  int g106 = (x0_15 ^ 1);
  int g107 = (x1_0 | g106);
  int g108 = (g107 ^ 1);
  int g109 = (x1_1 ^ 1);
  int g110 = (x1_1 & g108);
  int g111 = (g109 & g105);
  int g112 = (g110 | g111);
  int g113 = (x1_2 ^ 1);
  int g114 = (x1_2 & g112);
  int g115 = (g113 & g101);
  int g116 = (g114 | g115);
  int g117 = (x1_3 ^ 1);
  int g118 = (x1_3 & g116);
  int g119 = (g117 & g89);
  int g120 = (g118 | g119);
  int g121 = (g60 & g120);
  int g122 = (x1_1 ^ 1);
  int g123 = (x1_1 & g15);
  int g124 = (g122 & g7);
  int g125 = (g123 | g124);
  int g126 = (x1_1 ^ 1);
  int g127 = (x1_1 & g31);
  int g128 = (g126 & g19);
  int g129 = (g127 | g128);
  int g130 = (x1_2 ^ 1);
  int g131 = (x1_2 & g129);
  int g132 = (g130 & g125);
  int g133 = (g131 | g132);
  int g134 = (x1_1 ^ 1);
  int g135 = (x1_1 & g43);
  int g136 = (g134 & g35);
  int g137 = (g135 | g136);
  int g138 = (g47 ^ 1);
  int g139 = (x1_1 | g138);
  int g140 = (g139 ^ 1);
  int g141 = (x1_2 ^ 1);
  int g142 = (x1_2 & g140);
  int g143 = (g141 & g137);
  int g144 = (g142 | g143);
  int g145 = (x1_3 ^ 1);
  int g146 = (x1_3 & g144);
  int g147 = (g145 & g133);
  int g148 = (g146 | g147);
  int g149 = (g60 & g148);
  int g150 = (x1_1 ^ 1);
  int g151 = (x1_1 & g77);
  int g152 = (g150 & g69);
  int g153 = (g151 | g152);
  int g154 = (x1_1 ^ 1);
  int g155 = (x1_1 & g93);
  int g156 = (g154 & g81);
  int g157 = (g155 | g156);
  int g158 = (x1_2 ^ 1);
  int g159 = (x1_2 & g157);
  int g160 = (g158 & g153);
  int g161 = (g159 | g160);
  int g162 = (x1_1 ^ 1);
  int g163 = (x1_1 & g105);
  int g164 = (g162 & g97);
  int g165 = (g163 | g164);
  int g166 = (x1_1 | g107);
  int g167 = (g166 ^ 1);
  int g168 = (x1_2 ^ 1);
  int g169 = (x1_2 & g167);
  int g170 = (g168 & g165);
  int g171 = (g169 | g170);
  int g172 = (x1_3 ^ 1);
  int g173 = (x1_3 & g171);
  int g174 = (g172 & g161);
  int g175 = (g173 | g174);
  int g176 = (g60 & g175);
  int g177 = (x1_2 ^ 1);
  int g178 = (x1_2 & g39);
  int g179 = (g177 & g23);
  int g180 = (g178 | g179);
  int g181 = (g51 ^ 1);
  int g182 = (x1_2 | g181);
  int g183 = (g182 ^ 1);
  int g184 = (x1_3 ^ 1);
  int g185 = (x1_3 & g183);
  int g186 = (g184 & g180);
  int g187 = (g185 | g186);
  int g188 = (g60 & g187);
  int g189 = (x1_2 ^ 1);
  int g190 = (x1_2 & g101);
  int g191 = (g189 & g85);
  int g192 = (g190 | g191);
  int g193 = (g112 ^ 1);
  int g194 = (x1_2 | g193);
  int g195 = (g194 ^ 1);
  int g196 = (x1_3 ^ 1);
  int g197 = (x1_3 & g195);
  int g198 = (g196 & g192);
  int g199 = (g197 | g198);
  int g200 = (g60 & g199);
  int g201 = (x1_2 ^ 1);
  int g202 = (x1_2 & g137);
  int g203 = (g201 & g129);
  int g204 = (g202 | g203);
  int g205 = (x1_2 | g139);
  int g206 = (g205 ^ 1);
  int g207 = (x1_3 ^ 1);
  int g208 = (x1_3 & g206);
  int g209 = (g207 & g204);
  int g210 = (g208 | g209);
  int g211 = (g60 & g210);
  int g212 = (x1_2 ^ 1);
  int g213 = (x1_2 & g165);
  int g214 = (g212 & g157);
  int g215 = (g213 | g214);
  int g216 = (x1_2 | g166);
  int g217 = (g216 ^ 1);
  int g218 = (x1_3 ^ 1);
  int g219 = (x1_3 & g217);
  int g220 = (g218 & g215);
  int g221 = (g219 | g220);
  int g222 = (g60 & g221);
  int g223 = (x1_3 ^ 1);
  int g224 = (g60 & g223);
  int g225 = (g224 & g55);
  int g226 = (g60 & g223);
  int g227 = (g226 & g116);
  int g228 = (g60 & g223);
  int g229 = (g228 & g144);
  int g230 = (g60 & g223);
  int g231 = (g230 & g171);
  int g232 = (x1_2 ^ 1);
  int g233 = (g60 & g223);
  int g234 = (g233 & g232);
  int g235 = (g234 & g51);
  int g236 = (g60 & g223);
  int g237 = (g236 & g232);
  int g238 = (g237 & g112);
  int g239 = (x1_1 ^ 1);
  int g240 = (g60 & g223);
  int g241 = (g240 & g232);
  int g242 = (g241 & g239);
  int g243 = (g242 & g47);
  int g244 = (x1_0 ^ 1);
  int g245 = (g60 & g223);
  int g246 = (g245 & g232);
  int g247 = (g246 & g239);
  int g248 = (g247 & g244);
  int g249 = (g248 & x0_15);
  int w0 = x0_63;
  int w1 = cat(w0, x0_62, 1);
  int w2 = cat(w1, x0_61, 1);
  int w3 = cat(w2, x0_60, 1);
  int w4 = cat(w3, x0_59, 1);
  int w5 = cat(w4, x0_58, 1);
  int w6 = cat(w5, x0_57, 1);
  int w7 = cat(w6, x0_56, 1);
  int w8 = cat(w7, x0_55, 1);
  int w9 = cat(w8, x0_54, 1);
  int w10 = cat(w9, x0_53, 1);
  int w11 = cat(w10, x0_52, 1);
  int w12 = cat(w11, x0_51, 1);
  int w13 = cat(w12, x0_50, 1);
  int w14 = cat(w13, x0_49, 1);
  int w15 = cat(w14, x0_48, 1);
  int w16 = cat(w15, x0_47, 1);
  int w17 = cat(w16, x0_46, 1);
  int w18 = cat(w17, x0_45, 1);
  int w19 = cat(w18, x0_44, 1);
  int w20 = cat(w19, x0_43, 1);
  int w21 = cat(w20, x0_42, 1);
  int w22 = cat(w21, x0_41, 1);
  int w23 = cat(w22, x0_40, 1);
  int w24 = cat(w23, x0_39, 1);
  int w25 = cat(w24, x0_38, 1);
  int w26 = cat(w25, x0_37, 1);
  int w27 = cat(w26, x0_36, 1);
  int w28 = cat(w27, x0_35, 1);
  int w29 = cat(w28, x0_34, 1);
  int w30 = cat(w29, x0_33, 1);
  int w31 = cat(w30, x0_32, 1);
  int w32 = cat(w31, x0_31, 1);
  int w33 = cat(w32, x0_30, 1);
  int w34 = cat(w33, x0_29, 1);
  int w35 = cat(w34, x0_28, 1);
  int w36 = cat(w35, x0_27, 1);
  int w37 = cat(w36, x0_26, 1);
  int w38 = cat(w37, x0_25, 1);
  int w39 = cat(w38, x0_24, 1);
  int w40 = cat(w39, x0_23, 1);
  int w41 = cat(w40, x0_22, 1);
  int w42 = cat(w41, x0_21, 1);
  int w43 = cat(w42, x0_20, 1);
  int w44 = cat(w43, x0_19, 1);
  int w45 = cat(w44, x0_18, 1);
  int w46 = cat(w45, x0_17, 1);
  int w47 = cat(w46, x0_16, 1);
  int w48 = cat(w47, g249, 1);
  int w49 = cat(w48, g243, 1);
  int w50 = cat(w49, g238, 1);
  int w51 = cat(w50, g235, 1);
  int w52 = cat(w51, g231, 1);
  int w53 = cat(w52, g229, 1);
  int w54 = cat(w53, g227, 1);
  int w55 = cat(w54, g225, 1);
  int w56 = cat(w55, g222, 1);
  int w57 = cat(w56, g211, 1);
  int w58 = cat(w57, g200, 1);
  int w59 = cat(w58, g188, 1);
  int w60 = cat(w59, g176, 1);
  int w61 = cat(w60, g149, 1);
  int w62 = cat(w61, g121, 1);
  int w63 = cat(w62, g61, 1);
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
        final int answer = emu_shr_cl_gpr_16__reg_rdi__dart(values[0], values[1]);
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
