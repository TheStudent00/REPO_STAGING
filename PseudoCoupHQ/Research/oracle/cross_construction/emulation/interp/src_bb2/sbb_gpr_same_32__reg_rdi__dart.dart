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
// one named local per gate, over the term of sbb_gpr_same_32__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1, 1, 0)*4294967295)
int emu_sbb_gpr_same_32__reg_rdi__dart(int a, int b, int c) {
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
  int x1_8 = ext(a, 8, 8);
  int x0_8 = ext(b, 8, 8);
  int x1_9 = ext(a, 9, 9);
  int x0_9 = ext(b, 9, 9);
  int x1_10 = ext(a, 10, 10);
  int x0_10 = ext(b, 10, 10);
  int x1_11 = ext(a, 11, 11);
  int x0_11 = ext(b, 11, 11);
  int x1_12 = ext(a, 12, 12);
  int x0_12 = ext(b, 12, 12);
  int x1_13 = ext(a, 13, 13);
  int x0_13 = ext(b, 13, 13);
  int x1_14 = ext(a, 14, 14);
  int x0_14 = ext(b, 14, 14);
  int x1_15 = ext(a, 15, 15);
  int x0_15 = ext(b, 15, 15);
  int x1_16 = ext(a, 16, 16);
  int x0_16 = ext(b, 16, 16);
  int x1_17 = ext(a, 17, 17);
  int x0_17 = ext(b, 17, 17);
  int x1_18 = ext(a, 18, 18);
  int x0_18 = ext(b, 18, 18);
  int x1_19 = ext(a, 19, 19);
  int x0_19 = ext(b, 19, 19);
  int x1_20 = ext(a, 20, 20);
  int x0_20 = ext(b, 20, 20);
  int x1_21 = ext(a, 21, 21);
  int x0_21 = ext(b, 21, 21);
  int x1_22 = ext(a, 22, 22);
  int x0_22 = ext(b, 22, 22);
  int x1_23 = ext(a, 23, 23);
  int x0_23 = ext(b, 23, 23);
  int x1_24 = ext(a, 24, 24);
  int x0_24 = ext(b, 24, 24);
  int x1_25 = ext(a, 25, 25);
  int x0_25 = ext(b, 25, 25);
  int x1_26 = ext(a, 26, 26);
  int x0_26 = ext(b, 26, 26);
  int x1_27 = ext(a, 27, 27);
  int x0_27 = ext(b, 27, 27);
  int x1_28 = ext(a, 28, 28);
  int x0_28 = ext(b, 28, 28);
  int x1_29 = ext(a, 29, 29);
  int x0_29 = ext(b, 29, 29);
  int x1_30 = ext(a, 30, 30);
  int x0_30 = ext(b, 30, 30);
  int x1_31 = ext(a, 31, 31);
  int x0_31 = ext(b, 31, 31);
  int g0 = (x1_0 ^ 1);
  int g1 = (x0_0 ^ 1);
  int g2 = (g1 | g0);
  int g3 = (x1_1 ^ 1);
  int g4 = (g3 | g2);
  int g5 = (g4 ^ 1);
  int g6 = (x0_1 ^ 1);
  int g7 = (g6 | g2);
  int g8 = (g7 ^ 1);
  int g9 = (g6 | g3);
  int g10 = (g9 ^ 1);
  int g11 = (g10 | g8);
  int g12 = (g11 | g5);
  int g13 = (g12 ^ 1);
  int g14 = (x1_2 ^ 1);
  int g15 = (g14 | g13);
  int g16 = (g15 ^ 1);
  int g17 = (x0_2 ^ 1);
  int g18 = (g17 | g13);
  int g19 = (g18 ^ 1);
  int g20 = (g17 | g14);
  int g21 = (g20 ^ 1);
  int g22 = (g21 | g19);
  int g23 = (g22 | g16);
  int g24 = (g23 ^ 1);
  int g25 = (x1_3 ^ 1);
  int g26 = (g25 | g24);
  int g27 = (g26 ^ 1);
  int g28 = (x0_3 ^ 1);
  int g29 = (g28 | g24);
  int g30 = (g29 ^ 1);
  int g31 = (g28 | g25);
  int g32 = (g31 ^ 1);
  int g33 = (g32 | g30);
  int g34 = (g33 | g27);
  int g35 = (g34 ^ 1);
  int g36 = (x1_4 ^ 1);
  int g37 = (g36 | g35);
  int g38 = (g37 ^ 1);
  int g39 = (x0_4 ^ 1);
  int g40 = (g39 | g35);
  int g41 = (g40 ^ 1);
  int g42 = (g39 | g36);
  int g43 = (g42 ^ 1);
  int g44 = (g43 | g41);
  int g45 = (g44 | g38);
  int g46 = (g45 ^ 1);
  int g47 = (x1_5 ^ 1);
  int g48 = (g47 | g46);
  int g49 = (g48 ^ 1);
  int g50 = (x0_5 ^ 1);
  int g51 = (g50 | g46);
  int g52 = (g51 ^ 1);
  int g53 = (g50 | g47);
  int g54 = (g53 ^ 1);
  int g55 = (g54 | g52);
  int g56 = (g55 | g49);
  int g57 = (g56 ^ 1);
  int g58 = (x1_6 ^ 1);
  int g59 = (g58 | g57);
  int g60 = (g59 ^ 1);
  int g61 = (x0_6 ^ 1);
  int g62 = (g61 | g57);
  int g63 = (g62 ^ 1);
  int g64 = (g61 | g58);
  int g65 = (g64 ^ 1);
  int g66 = (g65 | g63);
  int g67 = (g66 | g60);
  int g68 = (g67 ^ 1);
  int g69 = (x1_7 ^ 1);
  int g70 = (g69 | g68);
  int g71 = (g70 ^ 1);
  int g72 = (x0_7 ^ 1);
  int g73 = (g72 | g68);
  int g74 = (g73 ^ 1);
  int g75 = (g72 | g69);
  int g76 = (g75 ^ 1);
  int g77 = (g76 | g74);
  int g78 = (g77 | g71);
  int g79 = (g78 ^ 1);
  int g80 = (x1_8 ^ 1);
  int g81 = (g80 | g79);
  int g82 = (g81 ^ 1);
  int g83 = (x0_8 ^ 1);
  int g84 = (g83 | g79);
  int g85 = (g84 ^ 1);
  int g86 = (g83 | g80);
  int g87 = (g86 ^ 1);
  int g88 = (g87 | g85);
  int g89 = (g88 | g82);
  int g90 = (g89 ^ 1);
  int g91 = (x1_9 ^ 1);
  int g92 = (g91 | g90);
  int g93 = (g92 ^ 1);
  int g94 = (x0_9 ^ 1);
  int g95 = (g94 | g90);
  int g96 = (g95 ^ 1);
  int g97 = (g94 | g91);
  int g98 = (g97 ^ 1);
  int g99 = (g98 | g96);
  int g100 = (g99 | g93);
  int g101 = (g100 ^ 1);
  int g102 = (x1_10 ^ 1);
  int g103 = (g102 | g101);
  int g104 = (g103 ^ 1);
  int g105 = (x0_10 ^ 1);
  int g106 = (g105 | g101);
  int g107 = (g106 ^ 1);
  int g108 = (g105 | g102);
  int g109 = (g108 ^ 1);
  int g110 = (g109 | g107);
  int g111 = (g110 | g104);
  int g112 = (g111 ^ 1);
  int g113 = (x1_11 ^ 1);
  int g114 = (g113 | g112);
  int g115 = (g114 ^ 1);
  int g116 = (x0_11 ^ 1);
  int g117 = (g116 | g112);
  int g118 = (g117 ^ 1);
  int g119 = (g116 | g113);
  int g120 = (g119 ^ 1);
  int g121 = (g120 | g118);
  int g122 = (g121 | g115);
  int g123 = (g122 ^ 1);
  int g124 = (x1_12 ^ 1);
  int g125 = (g124 | g123);
  int g126 = (g125 ^ 1);
  int g127 = (x0_12 ^ 1);
  int g128 = (g127 | g123);
  int g129 = (g128 ^ 1);
  int g130 = (g127 | g124);
  int g131 = (g130 ^ 1);
  int g132 = (g131 | g129);
  int g133 = (g132 | g126);
  int g134 = (g133 ^ 1);
  int g135 = (x1_13 ^ 1);
  int g136 = (g135 | g134);
  int g137 = (g136 ^ 1);
  int g138 = (x0_13 ^ 1);
  int g139 = (g138 | g134);
  int g140 = (g139 ^ 1);
  int g141 = (g138 | g135);
  int g142 = (g141 ^ 1);
  int g143 = (g142 | g140);
  int g144 = (g143 | g137);
  int g145 = (g144 ^ 1);
  int g146 = (x1_14 ^ 1);
  int g147 = (g146 | g145);
  int g148 = (g147 ^ 1);
  int g149 = (x0_14 ^ 1);
  int g150 = (g149 | g145);
  int g151 = (g150 ^ 1);
  int g152 = (g149 | g146);
  int g153 = (g152 ^ 1);
  int g154 = (g153 | g151);
  int g155 = (g154 | g148);
  int g156 = (g155 ^ 1);
  int g157 = (x1_15 ^ 1);
  int g158 = (g157 | g156);
  int g159 = (g158 ^ 1);
  int g160 = (x0_15 ^ 1);
  int g161 = (g160 | g156);
  int g162 = (g161 ^ 1);
  int g163 = (g160 | g157);
  int g164 = (g163 ^ 1);
  int g165 = (g164 | g162);
  int g166 = (g165 | g159);
  int g167 = (g166 ^ 1);
  int g168 = (x1_16 ^ 1);
  int g169 = (g168 | g167);
  int g170 = (g169 ^ 1);
  int g171 = (x0_16 ^ 1);
  int g172 = (g171 | g167);
  int g173 = (g172 ^ 1);
  int g174 = (g171 | g168);
  int g175 = (g174 ^ 1);
  int g176 = (g175 | g173);
  int g177 = (g176 | g170);
  int g178 = (g177 ^ 1);
  int g179 = (x1_17 ^ 1);
  int g180 = (g179 | g178);
  int g181 = (g180 ^ 1);
  int g182 = (x0_17 ^ 1);
  int g183 = (g182 | g178);
  int g184 = (g183 ^ 1);
  int g185 = (g182 | g179);
  int g186 = (g185 ^ 1);
  int g187 = (g186 | g184);
  int g188 = (g187 | g181);
  int g189 = (g188 ^ 1);
  int g190 = (x1_18 ^ 1);
  int g191 = (g190 | g189);
  int g192 = (g191 ^ 1);
  int g193 = (x0_18 ^ 1);
  int g194 = (g193 | g189);
  int g195 = (g194 ^ 1);
  int g196 = (g193 | g190);
  int g197 = (g196 ^ 1);
  int g198 = (g197 | g195);
  int g199 = (g198 | g192);
  int g200 = (g199 ^ 1);
  int g201 = (x1_19 ^ 1);
  int g202 = (g201 | g200);
  int g203 = (g202 ^ 1);
  int g204 = (x0_19 ^ 1);
  int g205 = (g204 | g200);
  int g206 = (g205 ^ 1);
  int g207 = (g204 | g201);
  int g208 = (g207 ^ 1);
  int g209 = (g208 | g206);
  int g210 = (g209 | g203);
  int g211 = (g210 ^ 1);
  int g212 = (x1_20 ^ 1);
  int g213 = (g212 | g211);
  int g214 = (g213 ^ 1);
  int g215 = (x0_20 ^ 1);
  int g216 = (g215 | g211);
  int g217 = (g216 ^ 1);
  int g218 = (g215 | g212);
  int g219 = (g218 ^ 1);
  int g220 = (g219 | g217);
  int g221 = (g220 | g214);
  int g222 = (g221 ^ 1);
  int g223 = (x1_21 ^ 1);
  int g224 = (g223 | g222);
  int g225 = (g224 ^ 1);
  int g226 = (x0_21 ^ 1);
  int g227 = (g226 | g222);
  int g228 = (g227 ^ 1);
  int g229 = (g226 | g223);
  int g230 = (g229 ^ 1);
  int g231 = (g230 | g228);
  int g232 = (g231 | g225);
  int g233 = (g232 ^ 1);
  int g234 = (x1_22 ^ 1);
  int g235 = (g234 | g233);
  int g236 = (g235 ^ 1);
  int g237 = (x0_22 ^ 1);
  int g238 = (g237 | g233);
  int g239 = (g238 ^ 1);
  int g240 = (g237 | g234);
  int g241 = (g240 ^ 1);
  int g242 = (g241 | g239);
  int g243 = (g242 | g236);
  int g244 = (g243 ^ 1);
  int g245 = (x1_23 ^ 1);
  int g246 = (g245 | g244);
  int g247 = (g246 ^ 1);
  int g248 = (x0_23 ^ 1);
  int g249 = (g248 | g244);
  int g250 = (g249 ^ 1);
  int g251 = (g248 | g245);
  int g252 = (g251 ^ 1);
  int g253 = (g252 | g250);
  int g254 = (g253 | g247);
  int g255 = (g254 ^ 1);
  int g256 = (x1_24 ^ 1);
  int g257 = (g256 | g255);
  int g258 = (g257 ^ 1);
  int g259 = (x0_24 ^ 1);
  int g260 = (g259 | g255);
  int g261 = (g260 ^ 1);
  int g262 = (g259 | g256);
  int g263 = (g262 ^ 1);
  int g264 = (g263 | g261);
  int g265 = (g264 | g258);
  int g266 = (g265 ^ 1);
  int g267 = (x1_25 ^ 1);
  int g268 = (g267 | g266);
  int g269 = (g268 ^ 1);
  int g270 = (x0_25 ^ 1);
  int g271 = (g270 | g266);
  int g272 = (g271 ^ 1);
  int g273 = (g270 | g267);
  int g274 = (g273 ^ 1);
  int g275 = (g274 | g272);
  int g276 = (g275 | g269);
  int g277 = (g276 ^ 1);
  int g278 = (x1_26 ^ 1);
  int g279 = (g278 | g277);
  int g280 = (g279 ^ 1);
  int g281 = (x0_26 ^ 1);
  int g282 = (g281 | g277);
  int g283 = (g282 ^ 1);
  int g284 = (g281 | g278);
  int g285 = (g284 ^ 1);
  int g286 = (g285 | g283);
  int g287 = (g286 | g280);
  int g288 = (g287 ^ 1);
  int g289 = (x1_27 ^ 1);
  int g290 = (g289 | g288);
  int g291 = (g290 ^ 1);
  int g292 = (x0_27 ^ 1);
  int g293 = (g292 | g288);
  int g294 = (g293 ^ 1);
  int g295 = (g292 | g289);
  int g296 = (g295 ^ 1);
  int g297 = (g296 | g294);
  int g298 = (g297 | g291);
  int g299 = (g298 ^ 1);
  int g300 = (x1_28 ^ 1);
  int g301 = (g300 | g299);
  int g302 = (g301 ^ 1);
  int g303 = (x0_28 ^ 1);
  int g304 = (g303 | g299);
  int g305 = (g304 ^ 1);
  int g306 = (g303 | g300);
  int g307 = (g306 ^ 1);
  int g308 = (g307 | g305);
  int g309 = (g308 | g302);
  int g310 = (g309 ^ 1);
  int g311 = (x1_29 ^ 1);
  int g312 = (g311 | g310);
  int g313 = (g312 ^ 1);
  int g314 = (x0_29 ^ 1);
  int g315 = (g314 | g310);
  int g316 = (g315 ^ 1);
  int g317 = (g314 | g311);
  int g318 = (g317 ^ 1);
  int g319 = (g318 | g316);
  int g320 = (g319 | g313);
  int g321 = (g320 ^ 1);
  int g322 = (x1_30 ^ 1);
  int g323 = (g322 | g321);
  int g324 = (g323 ^ 1);
  int g325 = (x0_30 ^ 1);
  int g326 = (g325 | g321);
  int g327 = (g326 ^ 1);
  int g328 = (g325 | g322);
  int g329 = (g328 ^ 1);
  int g330 = (g329 | g327);
  int g331 = (g330 | g324);
  int g332 = (g331 ^ 1);
  int g333 = (x1_31 ^ 1);
  int g334 = (g333 | g332);
  int g335 = (g334 ^ 1);
  int g336 = (x0_31 ^ 1);
  int g337 = (g336 | g332);
  int g338 = (g337 ^ 1);
  int g339 = (g336 | g333);
  int g340 = (g339 ^ 1);
  int g341 = (g340 | g338);
  int g342 = (g341 | g335);
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
  int w32 = cat(w31, g342, 1);
  int w33 = cat(w32, g342, 1);
  int w34 = cat(w33, g342, 1);
  int w35 = cat(w34, g342, 1);
  int w36 = cat(w35, g342, 1);
  int w37 = cat(w36, g342, 1);
  int w38 = cat(w37, g342, 1);
  int w39 = cat(w38, g342, 1);
  int w40 = cat(w39, g342, 1);
  int w41 = cat(w40, g342, 1);
  int w42 = cat(w41, g342, 1);
  int w43 = cat(w42, g342, 1);
  int w44 = cat(w43, g342, 1);
  int w45 = cat(w44, g342, 1);
  int w46 = cat(w45, g342, 1);
  int w47 = cat(w46, g342, 1);
  int w48 = cat(w47, g342, 1);
  int w49 = cat(w48, g342, 1);
  int w50 = cat(w49, g342, 1);
  int w51 = cat(w50, g342, 1);
  int w52 = cat(w51, g342, 1);
  int w53 = cat(w52, g342, 1);
  int w54 = cat(w53, g342, 1);
  int w55 = cat(w54, g342, 1);
  int w56 = cat(w55, g342, 1);
  int w57 = cat(w56, g342, 1);
  int w58 = cat(w57, g342, 1);
  int w59 = cat(w58, g342, 1);
  int w60 = cat(w59, g342, 1);
  int w61 = cat(w60, g342, 1);
  int w62 = cat(w61, g342, 1);
  int w63 = cat(w62, g342, 1);
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
        final int answer = emu_sbb_gpr_same_32__reg_rdi__dart(values[0], values[1], values[2]);
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
