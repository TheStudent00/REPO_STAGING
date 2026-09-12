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
// one named local per gate, over the term of xor_imm_gpr_8__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), Extract(7, 0, v0) ^ Extract(7, 0, v1))
int emu_xor_imm_gpr_8__reg_rdi__dart(int a, int b) {
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
  int w49 = cat(w48, x0_14, 1);
  int w50 = cat(w49, x0_13, 1);
  int w51 = cat(w50, x0_12, 1);
  int w52 = cat(w51, x0_11, 1);
  int w53 = cat(w52, x0_10, 1);
  int w54 = cat(w53, x0_9, 1);
  int w55 = cat(w54, x0_8, 1);
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
        final int answer = emu_xor_imm_gpr_8__reg_rdi__dart(values[0], values[1]);
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
