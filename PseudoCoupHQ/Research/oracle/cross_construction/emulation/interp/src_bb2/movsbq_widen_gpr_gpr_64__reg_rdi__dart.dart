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
// one named local per gate, over the term of movsbq_widen_gpr_gpr_64__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 0, v0))
int emu_movsbq_widen_gpr_gpr_64__reg_rdi__dart(int a) {
  int x0_0 = ext(a, 0, 0);
  int x0_1 = ext(a, 1, 1);
  int x0_2 = ext(a, 2, 2);
  int x0_3 = ext(a, 3, 3);
  int x0_4 = ext(a, 4, 4);
  int x0_5 = ext(a, 5, 5);
  int x0_6 = ext(a, 6, 6);
  int x0_7 = ext(a, 7, 7);
  int w0 = x0_7;
  int w1 = cat(w0, x0_7, 1);
  int w2 = cat(w1, x0_7, 1);
  int w3 = cat(w2, x0_7, 1);
  int w4 = cat(w3, x0_7, 1);
  int w5 = cat(w4, x0_7, 1);
  int w6 = cat(w5, x0_7, 1);
  int w7 = cat(w6, x0_7, 1);
  int w8 = cat(w7, x0_7, 1);
  int w9 = cat(w8, x0_7, 1);
  int w10 = cat(w9, x0_7, 1);
  int w11 = cat(w10, x0_7, 1);
  int w12 = cat(w11, x0_7, 1);
  int w13 = cat(w12, x0_7, 1);
  int w14 = cat(w13, x0_7, 1);
  int w15 = cat(w14, x0_7, 1);
  int w16 = cat(w15, x0_7, 1);
  int w17 = cat(w16, x0_7, 1);
  int w18 = cat(w17, x0_7, 1);
  int w19 = cat(w18, x0_7, 1);
  int w20 = cat(w19, x0_7, 1);
  int w21 = cat(w20, x0_7, 1);
  int w22 = cat(w21, x0_7, 1);
  int w23 = cat(w22, x0_7, 1);
  int w24 = cat(w23, x0_7, 1);
  int w25 = cat(w24, x0_7, 1);
  int w26 = cat(w25, x0_7, 1);
  int w27 = cat(w26, x0_7, 1);
  int w28 = cat(w27, x0_7, 1);
  int w29 = cat(w28, x0_7, 1);
  int w30 = cat(w29, x0_7, 1);
  int w31 = cat(w30, x0_7, 1);
  int w32 = cat(w31, x0_7, 1);
  int w33 = cat(w32, x0_7, 1);
  int w34 = cat(w33, x0_7, 1);
  int w35 = cat(w34, x0_7, 1);
  int w36 = cat(w35, x0_7, 1);
  int w37 = cat(w36, x0_7, 1);
  int w38 = cat(w37, x0_7, 1);
  int w39 = cat(w38, x0_7, 1);
  int w40 = cat(w39, x0_7, 1);
  int w41 = cat(w40, x0_7, 1);
  int w42 = cat(w41, x0_7, 1);
  int w43 = cat(w42, x0_7, 1);
  int w44 = cat(w43, x0_7, 1);
  int w45 = cat(w44, x0_7, 1);
  int w46 = cat(w45, x0_7, 1);
  int w47 = cat(w46, x0_7, 1);
  int w48 = cat(w47, x0_7, 1);
  int w49 = cat(w48, x0_7, 1);
  int w50 = cat(w49, x0_7, 1);
  int w51 = cat(w50, x0_7, 1);
  int w52 = cat(w51, x0_7, 1);
  int w53 = cat(w52, x0_7, 1);
  int w54 = cat(w53, x0_7, 1);
  int w55 = cat(w54, x0_7, 1);
  int w56 = cat(w55, x0_7, 1);
  int w57 = cat(w56, x0_6, 1);
  int w58 = cat(w57, x0_5, 1);
  int w59 = cat(w58, x0_4, 1);
  int w60 = cat(w59, x0_3, 1);
  int w61 = cat(w60, x0_2, 1);
  int w62 = cat(w61, x0_1, 1);
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
        final int answer = emu_movsbq_widen_gpr_gpr_64__reg_rdi__dart(values[0]);
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
