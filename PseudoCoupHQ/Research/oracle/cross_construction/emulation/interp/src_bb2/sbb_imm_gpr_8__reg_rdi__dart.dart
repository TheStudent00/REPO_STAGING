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
// one named local per gate, over the term of sbb_imm_gpr_8__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v3), Extract(7, 0, v2)*255 + If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v3))
int emu_sbb_imm_gpr_8__reg_rdi__dart(int a, int b, int c, int d) {
  int x3_0 = ext(c, 0, 0);
  int x2_0 = ext(d, 0, 0);
  int x1_0 = ext(a, 0, 0);
  int x0_0 = ext(b, 0, 0);
  int x1_1 = ext(a, 1, 1);
  int x0_1 = ext(b, 1, 1);
  int x1_2 = ext(a, 2, 2);
  int x0_2 = ext(b, 2, 2);
  int x1_3 = ext(a, 3, 3);
  int x0_3 = ext(b, 3, 3);
  int x1_4 = ext(a, 4, 4);
  int x0_4 = ext(b, 4, 4);
  int x1_5 = ext(a, 5, 5);
  int x0_5 = ext(b, 5, 5);
  int x1_6 = ext(a, 6, 6);
  int x0_6 = ext(b, 6, 6);
  int x1_7 = ext(a, 7, 7);
  int x0_7 = ext(b, 7, 7);
  int x3_1 = ext(c, 1, 1);
  int x2_1 = ext(d, 1, 1);
  int x2_2 = ext(d, 2, 2);
  int x3_2 = ext(c, 2, 2);
  int x2_3 = ext(d, 3, 3);
  int x3_3 = ext(c, 3, 3);
  int x2_4 = ext(d, 4, 4);
  int x3_4 = ext(c, 4, 4);
  int x2_5 = ext(d, 5, 5);
  int x3_5 = ext(c, 5, 5);
  int x2_6 = ext(d, 6, 6);
  int x3_6 = ext(c, 6, 6);
  int x2_7 = ext(d, 7, 7);
  int x3_7 = ext(c, 7, 7);
  int x3_8 = ext(c, 8, 8);
  int x3_9 = ext(c, 9, 9);
  int x3_10 = ext(c, 10, 10);
  int x3_11 = ext(c, 11, 11);
  int x3_12 = ext(c, 12, 12);
  int x3_13 = ext(c, 13, 13);
  int x3_14 = ext(c, 14, 14);
  int x3_15 = ext(c, 15, 15);
  int x3_16 = ext(c, 16, 16);
  int x3_17 = ext(c, 17, 17);
  int x3_18 = ext(c, 18, 18);
  int x3_19 = ext(c, 19, 19);
  int x3_20 = ext(c, 20, 20);
  int x3_21 = ext(c, 21, 21);
  int x3_22 = ext(c, 22, 22);
  int x3_23 = ext(c, 23, 23);
  int x3_24 = ext(c, 24, 24);
  int x3_25 = ext(c, 25, 25);
  int x3_26 = ext(c, 26, 26);
  int x3_27 = ext(c, 27, 27);
  int x3_28 = ext(c, 28, 28);
  int x3_29 = ext(c, 29, 29);
  int x3_30 = ext(c, 30, 30);
  int x3_31 = ext(c, 31, 31);
  int x3_32 = ext(c, 32, 32);
  int x3_33 = ext(c, 33, 33);
  int x3_34 = ext(c, 34, 34);
  int x3_35 = ext(c, 35, 35);
  int x3_36 = ext(c, 36, 36);
  int x3_37 = ext(c, 37, 37);
  int x3_38 = ext(c, 38, 38);
  int x3_39 = ext(c, 39, 39);
  int x3_40 = ext(c, 40, 40);
  int x3_41 = ext(c, 41, 41);
  int x3_42 = ext(c, 42, 42);
  int x3_43 = ext(c, 43, 43);
  int x3_44 = ext(c, 44, 44);
  int x3_45 = ext(c, 45, 45);
  int x3_46 = ext(c, 46, 46);
  int x3_47 = ext(c, 47, 47);
  int x3_48 = ext(c, 48, 48);
  int x3_49 = ext(c, 49, 49);
  int x3_50 = ext(c, 50, 50);
  int x3_51 = ext(c, 51, 51);
  int x3_52 = ext(c, 52, 52);
  int x3_53 = ext(c, 53, 53);
  int x3_54 = ext(c, 54, 54);
  int x3_55 = ext(c, 55, 55);
  int x3_56 = ext(c, 56, 56);
  int x3_57 = ext(c, 57, 57);
  int x3_58 = ext(c, 58, 58);
  int x3_59 = ext(c, 59, 59);
  int x3_60 = ext(c, 60, 60);
  int x3_61 = ext(c, 61, 61);
  int x3_62 = ext(c, 62, 62);
  int x3_63 = ext(c, 63, 63);
  int g0 = (x2_0 ^ x3_0);
  int g1 = (g0 ^ 1);
  int g2 = (x1_0 ^ 1);
  int g3 = (x0_0 ^ 1);
  int g4 = (g3 | g2);
  int g5 = (x1_1 ^ 1);
  int g6 = (g5 | g4);
  int g7 = (g6 ^ 1);
  int g8 = (x0_1 ^ 1);
  int g9 = (g8 | g4);
  int g10 = (g9 ^ 1);
  int g11 = (g8 | g5);
  int g12 = (g11 ^ 1);
  int g13 = (g12 | g10);
  int g14 = (g13 | g7);
  int g15 = (g14 ^ 1);
  int g16 = (x1_2 ^ 1);
  int g17 = (g16 | g15);
  int g18 = (g17 ^ 1);
  int g19 = (x0_2 ^ 1);
  int g20 = (g19 | g15);
  int g21 = (g20 ^ 1);
  int g22 = (g19 | g16);
  int g23 = (g22 ^ 1);
  int g24 = (g23 | g21);
  int g25 = (g24 | g18);
  int g26 = (g25 ^ 1);
  int g27 = (x1_3 ^ 1);
  int g28 = (g27 | g26);
  int g29 = (g28 ^ 1);
  int g30 = (x0_3 ^ 1);
  int g31 = (g30 | g26);
  int g32 = (g31 ^ 1);
  int g33 = (g30 | g27);
  int g34 = (g33 ^ 1);
  int g35 = (g34 | g32);
  int g36 = (g35 | g29);
  int g37 = (g36 ^ 1);
  int g38 = (x1_4 ^ 1);
  int g39 = (g38 | g37);
  int g40 = (g39 ^ 1);
  int g41 = (x0_4 ^ 1);
  int g42 = (g41 | g37);
  int g43 = (g42 ^ 1);
  int g44 = (g41 | g38);
  int g45 = (g44 ^ 1);
  int g46 = (g45 | g43);
  int g47 = (g46 | g40);
  int g48 = (g47 ^ 1);
  int g49 = (x1_5 ^ 1);
  int g50 = (g49 | g48);
  int g51 = (g50 ^ 1);
  int g52 = (x0_5 ^ 1);
  int g53 = (g52 | g48);
  int g54 = (g53 ^ 1);
  int g55 = (g52 | g49);
  int g56 = (g55 ^ 1);
  int g57 = (g56 | g54);
  int g58 = (g57 | g51);
  int g59 = (g58 ^ 1);
  int g60 = (x1_6 ^ 1);
  int g61 = (g60 | g59);
  int g62 = (g61 ^ 1);
  int g63 = (x0_6 ^ 1);
  int g64 = (g63 | g59);
  int g65 = (g64 ^ 1);
  int g66 = (g63 | g60);
  int g67 = (g66 ^ 1);
  int g68 = (g67 | g65);
  int g69 = (g68 | g62);
  int g70 = (g69 ^ 1);
  int g71 = (x1_7 ^ 1);
  int g72 = (g71 | g70);
  int g73 = (g72 ^ 1);
  int g74 = (x0_7 ^ 1);
  int g75 = (g74 | g70);
  int g76 = (g75 ^ 1);
  int g77 = (g74 | g71);
  int g78 = (g77 ^ 1);
  int g79 = (g78 | g76);
  int g80 = (g79 | g73);
  int g81 = (g80 ^ g1);
  int g82 = (g81 ^ 1);
  int g83 = (x3_0 ^ 1);
  int g84 = (x2_0 ^ g80);
  int g85 = (g84 ^ 1);
  int g86 = (g85 | g83);
  int g87 = (x3_1 ^ g86);
  int g88 = (g87 ^ 1);
  int g89 = (g80 ^ 1);
  int g90 = (x2_0 ^ 1);
  int g91 = (g90 | g89);
  int g92 = (g80 ^ g91);
  int g93 = (g92 ^ 1);
  int g94 = (x2_0 ^ x2_1);
  int g95 = (g94 ^ 1);
  int g96 = (g95 ^ g93);
  int g97 = (g96 ^ 1);
  int g98 = (g97 ^ g88);
  int g99 = (g98 ^ 1);
  int g100 = (g99 ^ 1);
  int g101 = (x2_1 | x2_0);
  int g102 = (g101 ^ x2_2);
  int g103 = (g102 ^ 1);
  int g104 = (g89 | g91);
  int g105 = (g104 ^ 1);
  int g106 = (g95 | g91);
  int g107 = (g106 ^ 1);
  int g108 = (g89 | g95);
  int g109 = (g108 ^ 1);
  int g110 = (g109 | g107);
  int g111 = (g110 | g105);
  int g112 = (g80 ^ g111);
  int g113 = (g112 ^ 1);
  int g114 = (g113 ^ g103);
  int g115 = (g114 ^ 1);
  int g116 = (g97 ^ 1);
  int g117 = (g116 | g86);
  int g118 = (g117 ^ 1);
  int g119 = (x3_1 ^ 1);
  int g120 = (g116 | g119);
  int g121 = (g120 ^ 1);
  int g122 = (g119 | g86);
  int g123 = (g122 ^ 1);
  int g124 = (g123 | g121);
  int g125 = (g124 | g118);
  int g126 = (x3_2 ^ g125);
  int g127 = (g126 ^ 1);
  int g128 = (g127 ^ g115);
  int g129 = (g128 ^ 1);
  int g130 = (g129 ^ 1);
  int g131 = (x2_2 | g101);
  int g132 = (g131 ^ x2_3);
  int g133 = (g132 ^ 1);
  int g134 = (g103 | g89);
  int g135 = (g134 ^ 1);
  int g136 = (g111 ^ 1);
  int g137 = (g136 | g103);
  int g138 = (g137 ^ 1);
  int g139 = (g89 | g136);
  int g140 = (g139 ^ 1);
  int g141 = (g140 | g138);
  int g142 = (g141 | g135);
  int g143 = (g80 ^ g142);
  int g144 = (g143 ^ 1);
  int g145 = (g144 ^ g133);
  int g146 = (g145 ^ 1);
  int g147 = (x3_2 ^ 1);
  int g148 = (g115 | g147);
  int g149 = (g148 ^ 1);
  int g150 = (g125 ^ 1);
  int g151 = (g147 | g150);
  int g152 = (g151 ^ 1);
  int g153 = (g115 | g150);
  int g154 = (g153 ^ 1);
  int g155 = (g154 | g152);
  int g156 = (g155 | g149);
  int g157 = (x3_3 ^ g156);
  int g158 = (g157 ^ 1);
  int g159 = (g158 ^ g146);
  int g160 = (g159 ^ 1);
  int g161 = (g160 ^ 1);
  int g162 = (x2_3 | g131);
  int g163 = (g162 ^ x2_4);
  int g164 = (g163 ^ 1);
  int g165 = (g142 ^ 1);
  int g166 = (g89 | g165);
  int g167 = (g166 ^ 1);
  int g168 = (g165 | g133);
  int g169 = (g168 ^ 1);
  int g170 = (g89 | g133);
  int g171 = (g170 ^ 1);
  int g172 = (g171 | g169);
  int g173 = (g172 | g167);
  int g174 = (g80 ^ g173);
  int g175 = (g174 ^ 1);
  int g176 = (g175 ^ g164);
  int g177 = (g176 ^ 1);
  int g178 = (x3_3 ^ 1);
  int g179 = (g178 | g146);
  int g180 = (g179 ^ 1);
  int g181 = (g156 ^ 1);
  int g182 = (g181 | g146);
  int g183 = (g182 ^ 1);
  int g184 = (g178 | g181);
  int g185 = (g184 ^ 1);
  int g186 = (g185 | g183);
  int g187 = (g186 | g180);
  int g188 = (x3_4 ^ g187);
  int g189 = (g188 ^ 1);
  int g190 = (g189 ^ g177);
  int g191 = (g190 ^ 1);
  int g192 = (g191 ^ 1);
  int g193 = (x2_4 | g162);
  int g194 = (g193 ^ x2_5);
  int g195 = (g194 ^ 1);
  int g196 = (g173 ^ 1);
  int g197 = (g196 | g164);
  int g198 = (g197 ^ 1);
  int g199 = (g89 | g196);
  int g200 = (g199 ^ 1);
  int g201 = (g89 | g164);
  int g202 = (g201 ^ 1);
  int g203 = (g202 | g200);
  int g204 = (g203 | g198);
  int g205 = (g80 ^ g204);
  int g206 = (g205 ^ 1);
  int g207 = (g206 ^ g195);
  int g208 = (g207 ^ 1);
  int g209 = (g187 ^ 1);
  int g210 = (x3_4 ^ 1);
  int g211 = (g210 | g209);
  int g212 = (g211 ^ 1);
  int g213 = (g210 | g177);
  int g214 = (g213 ^ 1);
  int g215 = (g177 | g209);
  int g216 = (g215 ^ 1);
  int g217 = (g216 | g214);
  int g218 = (g217 | g212);
  int g219 = (x3_5 ^ g218);
  int g220 = (g219 ^ 1);
  int g221 = (g220 ^ g208);
  int g222 = (g221 ^ 1);
  int g223 = (g222 ^ 1);
  int g224 = (x2_5 | g193);
  int g225 = (g224 ^ x2_6);
  int g226 = (g225 ^ 1);
  int g227 = (g204 ^ 1);
  int g228 = (g227 | g195);
  int g229 = (g228 ^ 1);
  int g230 = (g89 | g195);
  int g231 = (g230 ^ 1);
  int g232 = (g89 | g227);
  int g233 = (g232 ^ 1);
  int g234 = (g233 | g231);
  int g235 = (g234 | g229);
  int g236 = (g80 ^ g235);
  int g237 = (g236 ^ 1);
  int g238 = (g237 ^ g226);
  int g239 = (g238 ^ 1);
  int g240 = (x3_5 ^ 1);
  int g241 = (g208 | g240);
  int g242 = (g241 ^ 1);
  int g243 = (g218 ^ 1);
  int g244 = (g240 | g243);
  int g245 = (g244 ^ 1);
  int g246 = (g208 | g243);
  int g247 = (g246 ^ 1);
  int g248 = (g247 | g245);
  int g249 = (g248 | g242);
  int g250 = (x3_6 ^ g249);
  int g251 = (g250 ^ 1);
  int g252 = (g251 ^ g239);
  int g253 = (g252 ^ 1);
  int g254 = (g253 ^ 1);
  int g255 = (x2_6 | g224);
  int g256 = (g255 ^ x2_7);
  int g257 = (g256 ^ 1);
  int g258 = (g89 | g226);
  int g259 = (g258 ^ 1);
  int g260 = (g235 ^ 1);
  int g261 = (g260 | g226);
  int g262 = (g261 ^ 1);
  int g263 = (g89 | g260);
  int g264 = (g263 ^ 1);
  int g265 = (g264 | g262);
  int g266 = (g265 | g259);
  int g267 = (g80 ^ g266);
  int g268 = (g267 ^ 1);
  int g269 = (g268 ^ g257);
  int g270 = (g269 ^ 1);
  int g271 = (g249 ^ 1);
  int g272 = (g271 | g239);
  int g273 = (g272 ^ 1);
  int g274 = (x3_6 ^ 1);
  int g275 = (g274 | g271);
  int g276 = (g275 ^ 1);
  int g277 = (g239 | g274);
  int g278 = (g277 ^ 1);
  int g279 = (g278 | g276);
  int g280 = (g279 | g273);
  int g281 = (x3_7 ^ g280);
  int g282 = (g281 ^ 1);
  int g283 = (g282 ^ g270);
  int g284 = (g283 ^ 1);
  int g285 = (g284 ^ 1);
  int w0 = x3_63;
  int w1 = cat(w0, x3_62, 1);
  int w2 = cat(w1, x3_61, 1);
  int w3 = cat(w2, x3_60, 1);
  int w4 = cat(w3, x3_59, 1);
  int w5 = cat(w4, x3_58, 1);
  int w6 = cat(w5, x3_57, 1);
  int w7 = cat(w6, x3_56, 1);
  int w8 = cat(w7, x3_55, 1);
  int w9 = cat(w8, x3_54, 1);
  int w10 = cat(w9, x3_53, 1);
  int w11 = cat(w10, x3_52, 1);
  int w12 = cat(w11, x3_51, 1);
  int w13 = cat(w12, x3_50, 1);
  int w14 = cat(w13, x3_49, 1);
  int w15 = cat(w14, x3_48, 1);
  int w16 = cat(w15, x3_47, 1);
  int w17 = cat(w16, x3_46, 1);
  int w18 = cat(w17, x3_45, 1);
  int w19 = cat(w18, x3_44, 1);
  int w20 = cat(w19, x3_43, 1);
  int w21 = cat(w20, x3_42, 1);
  int w22 = cat(w21, x3_41, 1);
  int w23 = cat(w22, x3_40, 1);
  int w24 = cat(w23, x3_39, 1);
  int w25 = cat(w24, x3_38, 1);
  int w26 = cat(w25, x3_37, 1);
  int w27 = cat(w26, x3_36, 1);
  int w28 = cat(w27, x3_35, 1);
  int w29 = cat(w28, x3_34, 1);
  int w30 = cat(w29, x3_33, 1);
  int w31 = cat(w30, x3_32, 1);
  int w32 = cat(w31, x3_31, 1);
  int w33 = cat(w32, x3_30, 1);
  int w34 = cat(w33, x3_29, 1);
  int w35 = cat(w34, x3_28, 1);
  int w36 = cat(w35, x3_27, 1);
  int w37 = cat(w36, x3_26, 1);
  int w38 = cat(w37, x3_25, 1);
  int w39 = cat(w38, x3_24, 1);
  int w40 = cat(w39, x3_23, 1);
  int w41 = cat(w40, x3_22, 1);
  int w42 = cat(w41, x3_21, 1);
  int w43 = cat(w42, x3_20, 1);
  int w44 = cat(w43, x3_19, 1);
  int w45 = cat(w44, x3_18, 1);
  int w46 = cat(w45, x3_17, 1);
  int w47 = cat(w46, x3_16, 1);
  int w48 = cat(w47, x3_15, 1);
  int w49 = cat(w48, x3_14, 1);
  int w50 = cat(w49, x3_13, 1);
  int w51 = cat(w50, x3_12, 1);
  int w52 = cat(w51, x3_11, 1);
  int w53 = cat(w52, x3_10, 1);
  int w54 = cat(w53, x3_9, 1);
  int w55 = cat(w54, x3_8, 1);
  int w56 = cat(w55, g285, 1);
  int w57 = cat(w56, g254, 1);
  int w58 = cat(w57, g223, 1);
  int w59 = cat(w58, g192, 1);
  int w60 = cat(w59, g161, 1);
  int w61 = cat(w60, g130, 1);
  int w62 = cat(w61, g100, 1);
  int w63 = cat(w62, g82, 1);
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
        final int answer = emu_sbb_imm_gpr_8__reg_rdi__dart(values[0], values[1], values[2], values[3]);
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
