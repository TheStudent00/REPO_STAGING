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
// one named local per gate, over the term of cmovns_gpr_gpr_32__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Or(Extract(31, 31, v0) == 0, Extract(31, 31, v1) == 0), Extract(31, 0, v2), Extract(31, 0, v3)))
int emu_cmovns_gpr_gpr_32__reg_rdi__dart(int a, int b, int c, int d) {
  int x3_0 = ext(d, 0, 0);
  int x1_31 = ext(a, 31, 31);
  int x0_31 = ext(b, 31, 31);
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
  int g0 = (x1_31 ^ 1);
  int g1 = (x0_31 ^ 1);
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
        final int answer = emu_cmovns_gpr_gpr_32__reg_rdi__dart(values[0], values[1], values[2], values[3]);
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
