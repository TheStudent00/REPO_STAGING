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
// one named local per gate, over the term of seto_gpr_one_8__reg_rdi__dart.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v2), If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0)) + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0)) + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 0, 1))
int emu_seto_gpr_one_8__reg_rdi__dart(int a, int b, int c) {
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
  int x2_8 = ext(c, 8, 8);
  int x2_9 = ext(c, 9, 9);
  int x2_10 = ext(c, 10, 10);
  int x2_11 = ext(c, 11, 11);
  int x2_12 = ext(c, 12, 12);
  int x2_13 = ext(c, 13, 13);
  int x2_14 = ext(c, 14, 14);
  int x2_15 = ext(c, 15, 15);
  int x2_16 = ext(c, 16, 16);
  int x2_17 = ext(c, 17, 17);
  int x2_18 = ext(c, 18, 18);
  int x2_19 = ext(c, 19, 19);
  int x2_20 = ext(c, 20, 20);
  int x2_21 = ext(c, 21, 21);
  int x2_22 = ext(c, 22, 22);
  int x2_23 = ext(c, 23, 23);
  int x2_24 = ext(c, 24, 24);
  int x2_25 = ext(c, 25, 25);
  int x2_26 = ext(c, 26, 26);
  int x2_27 = ext(c, 27, 27);
  int x2_28 = ext(c, 28, 28);
  int x2_29 = ext(c, 29, 29);
  int x2_30 = ext(c, 30, 30);
  int x2_31 = ext(c, 31, 31);
  int x2_32 = ext(c, 32, 32);
  int x2_33 = ext(c, 33, 33);
  int x2_34 = ext(c, 34, 34);
  int x2_35 = ext(c, 35, 35);
  int x2_36 = ext(c, 36, 36);
  int x2_37 = ext(c, 37, 37);
  int x2_38 = ext(c, 38, 38);
  int x2_39 = ext(c, 39, 39);
  int x2_40 = ext(c, 40, 40);
  int x2_41 = ext(c, 41, 41);
  int x2_42 = ext(c, 42, 42);
  int x2_43 = ext(c, 43, 43);
  int x2_44 = ext(c, 44, 44);
  int x2_45 = ext(c, 45, 45);
  int x2_46 = ext(c, 46, 46);
  int x2_47 = ext(c, 47, 47);
  int x2_48 = ext(c, 48, 48);
  int x2_49 = ext(c, 49, 49);
  int x2_50 = ext(c, 50, 50);
  int x2_51 = ext(c, 51, 51);
  int x2_52 = ext(c, 52, 52);
  int x2_53 = ext(c, 53, 53);
  int x2_54 = ext(c, 54, 54);
  int x2_55 = ext(c, 55, 55);
  int x2_56 = ext(c, 56, 56);
  int x2_57 = ext(c, 57, 57);
  int x2_58 = ext(c, 58, 58);
  int x2_59 = ext(c, 59, 59);
  int x2_60 = ext(c, 60, 60);
  int x2_61 = ext(c, 61, 61);
  int x2_62 = ext(c, 62, 62);
  int x2_63 = ext(c, 63, 63);
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
  int g79 = (x1_7 ^ g78);
  int g80 = (g79 ^ 1);
  int g81 = (x0_7 ^ g80);
  int g82 = (g81 ^ 1);
  int g83 = (x1_7 ^ g67);
  int g84 = (g83 ^ 1);
  int g85 = (x0_7 ^ g84);
  int g86 = (g85 ^ 1);
  int g87 = (g86 ^ g82);
  int g88 = (g87 ^ 1);
  int g89 = (g88 ^ 1);
  int k0 = 0;
  int w0 = x2_63;
  int w1 = cat(w0, x2_62, 1);
  int w2 = cat(w1, x2_61, 1);
  int w3 = cat(w2, x2_60, 1);
  int w4 = cat(w3, x2_59, 1);
  int w5 = cat(w4, x2_58, 1);
  int w6 = cat(w5, x2_57, 1);
  int w7 = cat(w6, x2_56, 1);
  int w8 = cat(w7, x2_55, 1);
  int w9 = cat(w8, x2_54, 1);
  int w10 = cat(w9, x2_53, 1);
  int w11 = cat(w10, x2_52, 1);
  int w12 = cat(w11, x2_51, 1);
  int w13 = cat(w12, x2_50, 1);
  int w14 = cat(w13, x2_49, 1);
  int w15 = cat(w14, x2_48, 1);
  int w16 = cat(w15, x2_47, 1);
  int w17 = cat(w16, x2_46, 1);
  int w18 = cat(w17, x2_45, 1);
  int w19 = cat(w18, x2_44, 1);
  int w20 = cat(w19, x2_43, 1);
  int w21 = cat(w20, x2_42, 1);
  int w22 = cat(w21, x2_41, 1);
  int w23 = cat(w22, x2_40, 1);
  int w24 = cat(w23, x2_39, 1);
  int w25 = cat(w24, x2_38, 1);
  int w26 = cat(w25, x2_37, 1);
  int w27 = cat(w26, x2_36, 1);
  int w28 = cat(w27, x2_35, 1);
  int w29 = cat(w28, x2_34, 1);
  int w30 = cat(w29, x2_33, 1);
  int w31 = cat(w30, x2_32, 1);
  int w32 = cat(w31, x2_31, 1);
  int w33 = cat(w32, x2_30, 1);
  int w34 = cat(w33, x2_29, 1);
  int w35 = cat(w34, x2_28, 1);
  int w36 = cat(w35, x2_27, 1);
  int w37 = cat(w36, x2_26, 1);
  int w38 = cat(w37, x2_25, 1);
  int w39 = cat(w38, x2_24, 1);
  int w40 = cat(w39, x2_23, 1);
  int w41 = cat(w40, x2_22, 1);
  int w42 = cat(w41, x2_21, 1);
  int w43 = cat(w42, x2_20, 1);
  int w44 = cat(w43, x2_19, 1);
  int w45 = cat(w44, x2_18, 1);
  int w46 = cat(w45, x2_17, 1);
  int w47 = cat(w46, x2_16, 1);
  int w48 = cat(w47, x2_15, 1);
  int w49 = cat(w48, x2_14, 1);
  int w50 = cat(w49, x2_13, 1);
  int w51 = cat(w50, x2_12, 1);
  int w52 = cat(w51, x2_11, 1);
  int w53 = cat(w52, x2_10, 1);
  int w54 = cat(w53, x2_9, 1);
  int w55 = cat(w54, x2_8, 1);
  int w56 = cat(w55, k0, 1);
  int w57 = cat(w56, k0, 1);
  int w58 = cat(w57, k0, 1);
  int w59 = cat(w58, k0, 1);
  int w60 = cat(w59, k0, 1);
  int w61 = cat(w60, k0, 1);
  int w62 = cat(w61, k0, 1);
  int w63 = cat(w62, g89, 1);
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
        final int answer = emu_seto_gpr_one_8__reg_rdi__dart(values[0], values[1], values[2]);
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
