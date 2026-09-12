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
// one named local per gate, over the term of sar_cl_gpr_16__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1)))
int emu_sar_cl_gpr_16__reg_rdi__dart(int a, int b) {
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
  int g61 = (x1_4 & x0_15);
  int g62 = (g60 & g59);
  int g63 = (g61 | g62);
  int g64 = (x1_0 ^ 1);
  int g65 = (x1_0 & x0_2);
  int g66 = (g64 & x0_1);
  int g67 = (g65 | g66);
  int g68 = (x1_0 ^ 1);
  int g69 = (x1_0 & x0_4);
  int g70 = (g68 & x0_3);
  int g71 = (g69 | g70);
  int g72 = (x1_1 ^ 1);
  int g73 = (x1_1 & g71);
  int g74 = (g72 & g67);
  int g75 = (g73 | g74);
  int g76 = (x1_0 ^ 1);
  int g77 = (x1_0 & x0_6);
  int g78 = (g76 & x0_5);
  int g79 = (g77 | g78);
  int g80 = (x1_0 ^ 1);
  int g81 = (x1_0 & x0_8);
  int g82 = (g80 & x0_7);
  int g83 = (g81 | g82);
  int g84 = (x1_1 ^ 1);
  int g85 = (x1_1 & g83);
  int g86 = (g84 & g79);
  int g87 = (g85 | g86);
  int g88 = (x1_2 ^ 1);
  int g89 = (x1_2 & g87);
  int g90 = (g88 & g75);
  int g91 = (g89 | g90);
  int g92 = (x1_0 ^ 1);
  int g93 = (x1_0 & x0_10);
  int g94 = (g92 & x0_9);
  int g95 = (g93 | g94);
  int g96 = (x1_0 ^ 1);
  int g97 = (x1_0 & x0_12);
  int g98 = (g96 & x0_11);
  int g99 = (g97 | g98);
  int g100 = (x1_1 ^ 1);
  int g101 = (x1_1 & g99);
  int g102 = (g100 & g95);
  int g103 = (g101 | g102);
  int g104 = (x1_0 ^ 1);
  int g105 = (x1_0 & x0_14);
  int g106 = (g104 & x0_13);
  int g107 = (g105 | g106);
  int g108 = (x1_1 ^ 1);
  int g109 = (x1_1 & x0_15);
  int g110 = (g108 & g107);
  int g111 = (g109 | g110);
  int g112 = (x1_2 ^ 1);
  int g113 = (x1_2 & g111);
  int g114 = (g112 & g103);
  int g115 = (g113 | g114);
  int g116 = (x1_3 ^ 1);
  int g117 = (x1_3 & g115);
  int g118 = (g116 & g91);
  int g119 = (g117 | g118);
  int g120 = (x1_4 ^ 1);
  int g121 = (x1_4 & x0_15);
  int g122 = (g120 & g119);
  int g123 = (g121 | g122);
  int g124 = (x1_1 ^ 1);
  int g125 = (x1_1 & g15);
  int g126 = (g124 & g7);
  int g127 = (g125 | g126);
  int g128 = (x1_1 ^ 1);
  int g129 = (x1_1 & g31);
  int g130 = (g128 & g19);
  int g131 = (g129 | g130);
  int g132 = (x1_2 ^ 1);
  int g133 = (x1_2 & g131);
  int g134 = (g132 & g127);
  int g135 = (g133 | g134);
  int g136 = (x1_1 ^ 1);
  int g137 = (x1_1 & g43);
  int g138 = (g136 & g35);
  int g139 = (g137 | g138);
  int g140 = (x1_1 | x1_0);
  int g141 = (g140 ^ 1);
  int g142 = (g140 & x0_15);
  int g143 = (g141 & x0_14);
  int g144 = (g142 | g143);
  int g145 = (x1_2 ^ 1);
  int g146 = (x1_2 & g144);
  int g147 = (g145 & g139);
  int g148 = (g146 | g147);
  int g149 = (x1_3 ^ 1);
  int g150 = (x1_3 & g148);
  int g151 = (g149 & g135);
  int g152 = (g150 | g151);
  int g153 = (x1_4 ^ 1);
  int g154 = (x1_4 & x0_15);
  int g155 = (g153 & g152);
  int g156 = (g154 | g155);
  int g157 = (x1_1 ^ 1);
  int g158 = (x1_1 & g79);
  int g159 = (g157 & g71);
  int g160 = (g158 | g159);
  int g161 = (x1_1 ^ 1);
  int g162 = (x1_1 & g95);
  int g163 = (g161 & g83);
  int g164 = (g162 | g163);
  int g165 = (x1_2 ^ 1);
  int g166 = (x1_2 & g164);
  int g167 = (g165 & g160);
  int g168 = (g166 | g167);
  int g169 = (x1_1 ^ 1);
  int g170 = (x1_1 & g107);
  int g171 = (g169 & g99);
  int g172 = (g170 | g171);
  int g173 = (x1_2 ^ 1);
  int g174 = (x1_2 & x0_15);
  int g175 = (g173 & g172);
  int g176 = (g174 | g175);
  int g177 = (x1_3 ^ 1);
  int g178 = (x1_3 & g176);
  int g179 = (g177 & g168);
  int g180 = (g178 | g179);
  int g181 = (x1_4 ^ 1);
  int g182 = (x1_4 & x0_15);
  int g183 = (g181 & g180);
  int g184 = (g182 | g183);
  int g185 = (x1_2 ^ 1);
  int g186 = (x1_2 & g39);
  int g187 = (g185 & g23);
  int g188 = (g186 | g187);
  int g189 = (x1_2 ^ 1);
  int g190 = (x1_2 & x0_15);
  int g191 = (g189 & g51);
  int g192 = (g190 | g191);
  int g193 = (x1_3 ^ 1);
  int g194 = (x1_3 & g192);
  int g195 = (g193 & g188);
  int g196 = (g194 | g195);
  int g197 = (x1_4 ^ 1);
  int g198 = (x1_4 & x0_15);
  int g199 = (g197 & g196);
  int g200 = (g198 | g199);
  int g201 = (x1_2 ^ 1);
  int g202 = (x1_2 & g103);
  int g203 = (g201 & g87);
  int g204 = (g202 | g203);
  int g205 = (x1_2 | x1_1);
  int g206 = (g205 ^ 1);
  int g207 = (g205 & x0_15);
  int g208 = (g206 & g107);
  int g209 = (g207 | g208);
  int g210 = (x1_3 ^ 1);
  int g211 = (x1_3 & g209);
  int g212 = (g210 & g204);
  int g213 = (g211 | g212);
  int g214 = (x1_4 ^ 1);
  int g215 = (x1_4 & x0_15);
  int g216 = (g214 & g213);
  int g217 = (g215 | g216);
  int g218 = (x1_2 ^ 1);
  int g219 = (x1_2 & g139);
  int g220 = (g218 & g131);
  int g221 = (g219 | g220);
  int g222 = (x1_2 | g140);
  int g223 = (g222 ^ 1);
  int g224 = (g222 & x0_15);
  int g225 = (g223 & x0_14);
  int g226 = (g224 | g225);
  int g227 = (x1_3 ^ 1);
  int g228 = (x1_3 & g226);
  int g229 = (g227 & g221);
  int g230 = (g228 | g229);
  int g231 = (x1_4 ^ 1);
  int g232 = (x1_4 & x0_15);
  int g233 = (g231 & g230);
  int g234 = (g232 | g233);
  int g235 = (x1_2 ^ 1);
  int g236 = (x1_2 & g172);
  int g237 = (g235 & g164);
  int g238 = (g236 | g237);
  int g239 = (x1_4 | x1_3);
  int g240 = (g239 ^ 1);
  int g241 = (g239 & x0_15);
  int g242 = (g240 & g238);
  int g243 = (g241 | g242);
  int g244 = (g239 ^ 1);
  int g245 = (g239 & x0_15);
  int g246 = (g244 & g55);
  int g247 = (g245 | g246);
  int g248 = (g239 ^ 1);
  int g249 = (g239 & x0_15);
  int g250 = (g248 & g115);
  int g251 = (g249 | g250);
  int g252 = (g239 ^ 1);
  int g253 = (g239 & x0_15);
  int g254 = (g252 & g148);
  int g255 = (g253 | g254);
  int g256 = (x1_3 | x1_2);
  int g257 = (x1_4 | g256);
  int g258 = (g257 ^ 1);
  int g259 = (g257 & x0_15);
  int g260 = (g258 & g172);
  int g261 = (g259 | g260);
  int g262 = (g257 ^ 1);
  int g263 = (g257 & x0_15);
  int g264 = (g262 & g51);
  int g265 = (g263 | g264);
  int g266 = (x1_3 | g205);
  int g267 = (x1_4 | g266);
  int g268 = (g267 ^ 1);
  int g269 = (g267 & x0_15);
  int g270 = (g268 & g107);
  int g271 = (g269 | g270);
  int g272 = (x1_3 | g222);
  int g273 = (x1_4 | g272);
  int g274 = (g273 ^ 1);
  int g275 = (g273 & x0_15);
  int g276 = (g274 & x0_14);
  int g277 = (g275 | g276);
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
  int w48 = cat(w47, x0_15, 1);
  int w49 = cat(w48, g277, 1);
  int w50 = cat(w49, g271, 1);
  int w51 = cat(w50, g265, 1);
  int w52 = cat(w51, g261, 1);
  int w53 = cat(w52, g255, 1);
  int w54 = cat(w53, g251, 1);
  int w55 = cat(w54, g247, 1);
  int w56 = cat(w55, g243, 1);
  int w57 = cat(w56, g234, 1);
  int w58 = cat(w57, g217, 1);
  int w59 = cat(w58, g200, 1);
  int w60 = cat(w59, g184, 1);
  int w61 = cat(w60, g156, 1);
  int w62 = cat(w61, g123, 1);
  int w63 = cat(w62, g63, 1);
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
        final int answer = emu_sar_cl_gpr_16__reg_rdi__dart(values[0], values[1]);
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
