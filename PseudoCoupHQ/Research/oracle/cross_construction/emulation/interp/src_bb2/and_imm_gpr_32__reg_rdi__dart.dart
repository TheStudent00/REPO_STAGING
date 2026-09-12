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
// one named local per gate, over the term of and_imm_gpr_32__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(0, ~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)))
int emu_and_imm_gpr_32__reg_rdi__dart(int a, int b) {
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
  int g0 = (x0_0 & x1_0);
  int g1 = (x0_1 & x1_1);
  int g2 = (x0_2 & x1_2);
  int g3 = (x0_3 & x1_3);
  int g4 = (x0_4 & x1_4);
  int g5 = (x0_5 & x1_5);
  int g6 = (x0_6 & x1_6);
  int g7 = (x0_7 & x1_7);
  int g8 = (x0_8 & x1_8);
  int g9 = (x0_9 & x1_9);
  int g10 = (x0_10 & x1_10);
  int g11 = (x0_11 & x1_11);
  int g12 = (x0_12 & x1_12);
  int g13 = (x0_13 & x1_13);
  int g14 = (x0_14 & x1_14);
  int g15 = (x0_15 & x1_15);
  int g16 = (x0_16 & x1_16);
  int g17 = (x0_17 & x1_17);
  int g18 = (x0_18 & x1_18);
  int g19 = (x0_19 & x1_19);
  int g20 = (x0_20 & x1_20);
  int g21 = (x0_21 & x1_21);
  int g22 = (x0_22 & x1_22);
  int g23 = (x0_23 & x1_23);
  int g24 = (x0_24 & x1_24);
  int g25 = (x0_25 & x1_25);
  int g26 = (x0_26 & x1_26);
  int g27 = (x0_27 & x1_27);
  int g28 = (x0_28 & x1_28);
  int g29 = (x0_29 & x1_29);
  int g30 = (x0_30 & x1_30);
  int g31 = (x0_31 & x1_31);
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
  int w32 = cat(w31, g31, 1);
  int w33 = cat(w32, g30, 1);
  int w34 = cat(w33, g29, 1);
  int w35 = cat(w34, g28, 1);
  int w36 = cat(w35, g27, 1);
  int w37 = cat(w36, g26, 1);
  int w38 = cat(w37, g25, 1);
  int w39 = cat(w38, g24, 1);
  int w40 = cat(w39, g23, 1);
  int w41 = cat(w40, g22, 1);
  int w42 = cat(w41, g21, 1);
  int w43 = cat(w42, g20, 1);
  int w44 = cat(w43, g19, 1);
  int w45 = cat(w44, g18, 1);
  int w46 = cat(w45, g17, 1);
  int w47 = cat(w46, g16, 1);
  int w48 = cat(w47, g15, 1);
  int w49 = cat(w48, g14, 1);
  int w50 = cat(w49, g13, 1);
  int w51 = cat(w50, g12, 1);
  int w52 = cat(w51, g11, 1);
  int w53 = cat(w52, g10, 1);
  int w54 = cat(w53, g9, 1);
  int w55 = cat(w54, g8, 1);
  int w56 = cat(w55, g7, 1);
  int w57 = cat(w56, g6, 1);
  int w58 = cat(w57, g5, 1);
  int w59 = cat(w58, g4, 1);
  int w60 = cat(w59, g3, 1);
  int w61 = cat(w60, g2, 1);
  int w62 = cat(w61, g1, 1);
  int w63 = cat(w62, g0, 1);
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
        final int answer = emu_and_imm_gpr_32__reg_rdi__dart(values[0], values[1]);
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
