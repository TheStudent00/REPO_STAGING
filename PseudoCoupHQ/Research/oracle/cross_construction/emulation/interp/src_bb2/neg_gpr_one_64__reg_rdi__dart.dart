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
// one named local per gate, over the term of neg_gpr_one_64__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   v0*18446744073709551615
int emu_neg_gpr_one_64__reg_rdi__dart(int a) {
  int x0_0 = ext(a, 0, 0);
  int x0_1 = ext(a, 1, 1);
  int x0_2 = ext(a, 2, 2);
  int x0_3 = ext(a, 3, 3);
  int x0_4 = ext(a, 4, 4);
  int x0_5 = ext(a, 5, 5);
  int x0_6 = ext(a, 6, 6);
  int x0_7 = ext(a, 7, 7);
  int x0_8 = ext(a, 8, 8);
  int x0_9 = ext(a, 9, 9);
  int x0_10 = ext(a, 10, 10);
  int x0_11 = ext(a, 11, 11);
  int x0_12 = ext(a, 12, 12);
  int x0_13 = ext(a, 13, 13);
  int x0_14 = ext(a, 14, 14);
  int x0_15 = ext(a, 15, 15);
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
  int g0 = (x0_0 ^ x0_1);
  int g1 = (g0 ^ 1);
  int g2 = (g1 ^ 1);
  int g3 = (x0_1 | x0_0);
  int g4 = (g3 ^ x0_2);
  int g5 = (g4 ^ 1);
  int g6 = (g5 ^ 1);
  int g7 = (x0_2 | g3);
  int g8 = (g7 ^ x0_3);
  int g9 = (g8 ^ 1);
  int g10 = (g9 ^ 1);
  int g11 = (x0_3 | g7);
  int g12 = (g11 ^ x0_4);
  int g13 = (g12 ^ 1);
  int g14 = (g13 ^ 1);
  int g15 = (x0_4 | g11);
  int g16 = (g15 ^ x0_5);
  int g17 = (g16 ^ 1);
  int g18 = (g17 ^ 1);
  int g19 = (x0_5 | g15);
  int g20 = (g19 ^ x0_6);
  int g21 = (g20 ^ 1);
  int g22 = (g21 ^ 1);
  int g23 = (x0_6 | g19);
  int g24 = (g23 ^ x0_7);
  int g25 = (g24 ^ 1);
  int g26 = (g25 ^ 1);
  int g27 = (x0_7 | g23);
  int g28 = (g27 ^ x0_8);
  int g29 = (g28 ^ 1);
  int g30 = (g29 ^ 1);
  int g31 = (x0_8 | g27);
  int g32 = (g31 ^ x0_9);
  int g33 = (g32 ^ 1);
  int g34 = (g33 ^ 1);
  int g35 = (x0_9 | g31);
  int g36 = (g35 ^ x0_10);
  int g37 = (g36 ^ 1);
  int g38 = (g37 ^ 1);
  int g39 = (x0_10 | g35);
  int g40 = (g39 ^ x0_11);
  int g41 = (g40 ^ 1);
  int g42 = (g41 ^ 1);
  int g43 = (x0_11 | g39);
  int g44 = (g43 ^ x0_12);
  int g45 = (g44 ^ 1);
  int g46 = (g45 ^ 1);
  int g47 = (x0_12 | g43);
  int g48 = (g47 ^ x0_13);
  int g49 = (g48 ^ 1);
  int g50 = (g49 ^ 1);
  int g51 = (x0_13 | g47);
  int g52 = (g51 ^ x0_14);
  int g53 = (g52 ^ 1);
  int g54 = (g53 ^ 1);
  int g55 = (x0_14 | g51);
  int g56 = (g55 ^ x0_15);
  int g57 = (g56 ^ 1);
  int g58 = (g57 ^ 1);
  int g59 = (x0_15 | g55);
  int g60 = (g59 ^ x0_16);
  int g61 = (g60 ^ 1);
  int g62 = (g61 ^ 1);
  int g63 = (x0_16 | g59);
  int g64 = (g63 ^ x0_17);
  int g65 = (g64 ^ 1);
  int g66 = (g65 ^ 1);
  int g67 = (x0_17 | g63);
  int g68 = (g67 ^ x0_18);
  int g69 = (g68 ^ 1);
  int g70 = (g69 ^ 1);
  int g71 = (x0_18 | g67);
  int g72 = (g71 ^ x0_19);
  int g73 = (g72 ^ 1);
  int g74 = (g73 ^ 1);
  int g75 = (x0_19 | g71);
  int g76 = (g75 ^ x0_20);
  int g77 = (g76 ^ 1);
  int g78 = (g77 ^ 1);
  int g79 = (x0_20 | g75);
  int g80 = (g79 ^ x0_21);
  int g81 = (g80 ^ 1);
  int g82 = (g81 ^ 1);
  int g83 = (x0_21 | g79);
  int g84 = (g83 ^ x0_22);
  int g85 = (g84 ^ 1);
  int g86 = (g85 ^ 1);
  int g87 = (x0_22 | g83);
  int g88 = (g87 ^ x0_23);
  int g89 = (g88 ^ 1);
  int g90 = (g89 ^ 1);
  int g91 = (x0_23 | g87);
  int g92 = (g91 ^ x0_24);
  int g93 = (g92 ^ 1);
  int g94 = (g93 ^ 1);
  int g95 = (x0_24 | g91);
  int g96 = (g95 ^ x0_25);
  int g97 = (g96 ^ 1);
  int g98 = (g97 ^ 1);
  int g99 = (x0_25 | g95);
  int g100 = (g99 ^ x0_26);
  int g101 = (g100 ^ 1);
  int g102 = (g101 ^ 1);
  int g103 = (x0_26 | g99);
  int g104 = (g103 ^ x0_27);
  int g105 = (g104 ^ 1);
  int g106 = (g105 ^ 1);
  int g107 = (x0_27 | g103);
  int g108 = (g107 ^ x0_28);
  int g109 = (g108 ^ 1);
  int g110 = (g109 ^ 1);
  int g111 = (x0_28 | g107);
  int g112 = (g111 ^ x0_29);
  int g113 = (g112 ^ 1);
  int g114 = (g113 ^ 1);
  int g115 = (x0_29 | g111);
  int g116 = (g115 ^ x0_30);
  int g117 = (g116 ^ 1);
  int g118 = (g117 ^ 1);
  int g119 = (x0_30 | g115);
  int g120 = (g119 ^ x0_31);
  int g121 = (g120 ^ 1);
  int g122 = (g121 ^ 1);
  int g123 = (x0_31 | g119);
  int g124 = (g123 ^ x0_32);
  int g125 = (g124 ^ 1);
  int g126 = (g125 ^ 1);
  int g127 = (x0_32 | g123);
  int g128 = (g127 ^ x0_33);
  int g129 = (g128 ^ 1);
  int g130 = (g129 ^ 1);
  int g131 = (x0_33 | g127);
  int g132 = (g131 ^ x0_34);
  int g133 = (g132 ^ 1);
  int g134 = (g133 ^ 1);
  int g135 = (x0_34 | g131);
  int g136 = (g135 ^ x0_35);
  int g137 = (g136 ^ 1);
  int g138 = (g137 ^ 1);
  int g139 = (x0_35 | g135);
  int g140 = (g139 ^ x0_36);
  int g141 = (g140 ^ 1);
  int g142 = (g141 ^ 1);
  int g143 = (x0_36 | g139);
  int g144 = (g143 ^ x0_37);
  int g145 = (g144 ^ 1);
  int g146 = (g145 ^ 1);
  int g147 = (x0_37 | g143);
  int g148 = (g147 ^ x0_38);
  int g149 = (g148 ^ 1);
  int g150 = (g149 ^ 1);
  int g151 = (x0_38 | g147);
  int g152 = (g151 ^ x0_39);
  int g153 = (g152 ^ 1);
  int g154 = (g153 ^ 1);
  int g155 = (x0_39 | g151);
  int g156 = (g155 ^ x0_40);
  int g157 = (g156 ^ 1);
  int g158 = (g157 ^ 1);
  int g159 = (x0_40 | g155);
  int g160 = (g159 ^ x0_41);
  int g161 = (g160 ^ 1);
  int g162 = (g161 ^ 1);
  int g163 = (x0_41 | g159);
  int g164 = (g163 ^ x0_42);
  int g165 = (g164 ^ 1);
  int g166 = (g165 ^ 1);
  int g167 = (x0_42 | g163);
  int g168 = (g167 ^ x0_43);
  int g169 = (g168 ^ 1);
  int g170 = (g169 ^ 1);
  int g171 = (x0_43 | g167);
  int g172 = (g171 ^ x0_44);
  int g173 = (g172 ^ 1);
  int g174 = (g173 ^ 1);
  int g175 = (x0_44 | g171);
  int g176 = (g175 ^ x0_45);
  int g177 = (g176 ^ 1);
  int g178 = (g177 ^ 1);
  int g179 = (x0_45 | g175);
  int g180 = (g179 ^ x0_46);
  int g181 = (g180 ^ 1);
  int g182 = (g181 ^ 1);
  int g183 = (x0_46 | g179);
  int g184 = (g183 ^ x0_47);
  int g185 = (g184 ^ 1);
  int g186 = (g185 ^ 1);
  int g187 = (x0_47 | g183);
  int g188 = (g187 ^ x0_48);
  int g189 = (g188 ^ 1);
  int g190 = (g189 ^ 1);
  int g191 = (x0_48 | g187);
  int g192 = (g191 ^ x0_49);
  int g193 = (g192 ^ 1);
  int g194 = (g193 ^ 1);
  int g195 = (x0_49 | g191);
  int g196 = (g195 ^ x0_50);
  int g197 = (g196 ^ 1);
  int g198 = (g197 ^ 1);
  int g199 = (x0_50 | g195);
  int g200 = (g199 ^ x0_51);
  int g201 = (g200 ^ 1);
  int g202 = (g201 ^ 1);
  int g203 = (x0_51 | g199);
  int g204 = (g203 ^ x0_52);
  int g205 = (g204 ^ 1);
  int g206 = (g205 ^ 1);
  int g207 = (x0_52 | g203);
  int g208 = (g207 ^ x0_53);
  int g209 = (g208 ^ 1);
  int g210 = (g209 ^ 1);
  int g211 = (x0_53 | g207);
  int g212 = (g211 ^ x0_54);
  int g213 = (g212 ^ 1);
  int g214 = (g213 ^ 1);
  int g215 = (x0_54 | g211);
  int g216 = (g215 ^ x0_55);
  int g217 = (g216 ^ 1);
  int g218 = (g217 ^ 1);
  int g219 = (x0_55 | g215);
  int g220 = (g219 ^ x0_56);
  int g221 = (g220 ^ 1);
  int g222 = (g221 ^ 1);
  int g223 = (x0_56 | g219);
  int g224 = (g223 ^ x0_57);
  int g225 = (g224 ^ 1);
  int g226 = (g225 ^ 1);
  int g227 = (x0_57 | g223);
  int g228 = (g227 ^ x0_58);
  int g229 = (g228 ^ 1);
  int g230 = (g229 ^ 1);
  int g231 = (x0_58 | g227);
  int g232 = (g231 ^ x0_59);
  int g233 = (g232 ^ 1);
  int g234 = (g233 ^ 1);
  int g235 = (x0_59 | g231);
  int g236 = (g235 ^ x0_60);
  int g237 = (g236 ^ 1);
  int g238 = (g237 ^ 1);
  int g239 = (x0_60 | g235);
  int g240 = (g239 ^ x0_61);
  int g241 = (g240 ^ 1);
  int g242 = (g241 ^ 1);
  int g243 = (x0_61 | g239);
  int g244 = (g243 ^ x0_62);
  int g245 = (g244 ^ 1);
  int g246 = (g245 ^ 1);
  int g247 = (x0_62 | g243);
  int g248 = (g247 ^ x0_63);
  int g249 = (g248 ^ 1);
  int g250 = (g249 ^ 1);
  int w0 = g250;
  int w1 = cat(w0, g246, 1);
  int w2 = cat(w1, g242, 1);
  int w3 = cat(w2, g238, 1);
  int w4 = cat(w3, g234, 1);
  int w5 = cat(w4, g230, 1);
  int w6 = cat(w5, g226, 1);
  int w7 = cat(w6, g222, 1);
  int w8 = cat(w7, g218, 1);
  int w9 = cat(w8, g214, 1);
  int w10 = cat(w9, g210, 1);
  int w11 = cat(w10, g206, 1);
  int w12 = cat(w11, g202, 1);
  int w13 = cat(w12, g198, 1);
  int w14 = cat(w13, g194, 1);
  int w15 = cat(w14, g190, 1);
  int w16 = cat(w15, g186, 1);
  int w17 = cat(w16, g182, 1);
  int w18 = cat(w17, g178, 1);
  int w19 = cat(w18, g174, 1);
  int w20 = cat(w19, g170, 1);
  int w21 = cat(w20, g166, 1);
  int w22 = cat(w21, g162, 1);
  int w23 = cat(w22, g158, 1);
  int w24 = cat(w23, g154, 1);
  int w25 = cat(w24, g150, 1);
  int w26 = cat(w25, g146, 1);
  int w27 = cat(w26, g142, 1);
  int w28 = cat(w27, g138, 1);
  int w29 = cat(w28, g134, 1);
  int w30 = cat(w29, g130, 1);
  int w31 = cat(w30, g126, 1);
  int w32 = cat(w31, g122, 1);
  int w33 = cat(w32, g118, 1);
  int w34 = cat(w33, g114, 1);
  int w35 = cat(w34, g110, 1);
  int w36 = cat(w35, g106, 1);
  int w37 = cat(w36, g102, 1);
  int w38 = cat(w37, g98, 1);
  int w39 = cat(w38, g94, 1);
  int w40 = cat(w39, g90, 1);
  int w41 = cat(w40, g86, 1);
  int w42 = cat(w41, g82, 1);
  int w43 = cat(w42, g78, 1);
  int w44 = cat(w43, g74, 1);
  int w45 = cat(w44, g70, 1);
  int w46 = cat(w45, g66, 1);
  int w47 = cat(w46, g62, 1);
  int w48 = cat(w47, g58, 1);
  int w49 = cat(w48, g54, 1);
  int w50 = cat(w49, g50, 1);
  int w51 = cat(w50, g46, 1);
  int w52 = cat(w51, g42, 1);
  int w53 = cat(w52, g38, 1);
  int w54 = cat(w53, g34, 1);
  int w55 = cat(w54, g30, 1);
  int w56 = cat(w55, g26, 1);
  int w57 = cat(w56, g22, 1);
  int w58 = cat(w57, g18, 1);
  int w59 = cat(w58, g14, 1);
  int w60 = cat(w59, g10, 1);
  int w61 = cat(w60, g6, 1);
  int w62 = cat(w61, g2, 1);
  int w63 = cat(w62, x0_0, 1);
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
        final int answer = emu_neg_gpr_one_64__reg_rdi__dart(values[0]);
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
