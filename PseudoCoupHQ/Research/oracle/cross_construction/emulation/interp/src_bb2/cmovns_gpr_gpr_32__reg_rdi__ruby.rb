def m(x, w)
  x & ((1 << w) - 1)
end

def s(x, w)
  x = x & ((1 << w) - 1)
  return x - (1 << w) if (x >> (w - 1)) != 0
  x
end

def add(a, b, w)
  m(a + b, w)
end

def sub(a, b, w)
  m(a - b, w)
end

def mul(a, b, w)
  m(a * b, w)
end

def band(a, b, w)
  m(a & b, w)
end

def bor(a, b, w)
  m(a | b, w)
end

def bxor(a, b, w)
  m(a ^ b, w)
end

def bnot(a, w)
  m(~a, w)
end

def bneg(a, w)
  m(-a, w)
end

def shl(a, n, w)
  return 0 if n >= w
  m(a << n, w)
end

def lshr(a, n, w)
  return 0 if n >= w
  m(a, w) >> n
end

def ashr(a, n, w)
  v = s(a, w)
  k = n
  k = w - 1 if k >= w
  m(v >> k, w)
end

def udiv(a, b, w)
  m(m(a, w) / m(b, w), w)
end

def urem(a, b, w)
  m(m(a, w) % m(b, w), w)
end

def sdiv(a, b, w)
  x = s(a, w)
  y = s(b, w)
  q = x.abs / y.abs
  q = -q if (x < 0) != (y < 0)
  m(q, w)
end

def srem(a, b, w)
  x = s(a, w)
  y = s(b, w)
  r = x.abs % y.abs
  r = -r if x < 0
  m(r, w)
end

def ult(a, b, w)
  m(a, w) < m(b, w)
end

def ule(a, b, w)
  m(a, w) <= m(b, w)
end

def ugt(a, b, w)
  m(a, w) > m(b, w)
end

def uge(a, b, w)
  m(a, w) >= m(b, w)
end

def slt(a, b, w)
  s(a, w) < s(b, w)
end

def sle(a, b, w)
  s(a, w) <= s(b, w)
end

def sgt(a, b, w)
  s(a, w) > s(b, w)
end

def sge(a, b, w)
  s(a, w) >= s(b, w)
end

def eq(a, b, w)
  m(a, w) == m(b, w)
end

def ne(a, b, w)
  m(a, w) != m(b, w)
end

def cat(hi, lo, lw)
  (hi << lw) | m(lo, lw)
end

def ext(x, hi, lo)
  m(x >> lo, hi - lo + 1)
end

def sext(x, fromw, tow)
  m(s(x, fromw), tow)
end

def b2f(x, w)
  return [m(x, 32)].pack("V").unpack1("e") if w == 32
  [m(x, 64)].pack("Q<").unpack1("E")
end

def f2b(f, w)
  return [f].pack("e").unpack1("V") if w == 32
  [f].pack("E").unpack1("Q<")
end

def fadd(a, b, w)
  f2b(b2f(a, w) + b2f(b, w), w)
end

def fsub(a, b, w)
  f2b(b2f(a, w) - b2f(b, w), w)
end

def fmul(a, b, w)
  f2b(b2f(a, w) * b2f(b, w), w)
end

def fdiv(a, b, w)
  f2b(b2f(a, w) / b2f(b, w), w)
end

def i2f(x, fromw, w)
  f2b(s(x, fromw).to_f, w)
end

def u2f(x, fromw, w)
  f2b(m(x, fromw).to_f, w)
end

def fwiden(x, fromw, w)
  f2b(b2f(x, fromw), w)
end

# task bb2 emulation -- the BIT-BLAST route: z3's own circuit,
# one named local per gate, over the term of cmovns_gpr_gpr_32__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(0, If(Or(Extract(31, 31, v0) == 0, Extract(31, 31, v1) == 0), Extract(31, 0, v2), Extract(31, 0, v3)))
def emu_cmovns_gpr_gpr_32__reg_rdi__ruby(a, b, c, d)
  x3_0 = ext(d, 0, 0)
  x1_31 = ext(a, 31, 31)
  x0_31 = ext(b, 31, 31)
  x2_0 = ext(c, 0, 0)
  x3_1 = ext(d, 1, 1)
  x2_1 = ext(c, 1, 1)
  x3_2 = ext(d, 2, 2)
  x2_2 = ext(c, 2, 2)
  x3_3 = ext(d, 3, 3)
  x2_3 = ext(c, 3, 3)
  x3_4 = ext(d, 4, 4)
  x2_4 = ext(c, 4, 4)
  x3_5 = ext(d, 5, 5)
  x2_5 = ext(c, 5, 5)
  x3_6 = ext(d, 6, 6)
  x2_6 = ext(c, 6, 6)
  x3_7 = ext(d, 7, 7)
  x2_7 = ext(c, 7, 7)
  x3_8 = ext(d, 8, 8)
  x2_8 = ext(c, 8, 8)
  x3_9 = ext(d, 9, 9)
  x2_9 = ext(c, 9, 9)
  x3_10 = ext(d, 10, 10)
  x2_10 = ext(c, 10, 10)
  x3_11 = ext(d, 11, 11)
  x2_11 = ext(c, 11, 11)
  x3_12 = ext(d, 12, 12)
  x2_12 = ext(c, 12, 12)
  x3_13 = ext(d, 13, 13)
  x2_13 = ext(c, 13, 13)
  x3_14 = ext(d, 14, 14)
  x2_14 = ext(c, 14, 14)
  x3_15 = ext(d, 15, 15)
  x2_15 = ext(c, 15, 15)
  x3_16 = ext(d, 16, 16)
  x2_16 = ext(c, 16, 16)
  x3_17 = ext(d, 17, 17)
  x2_17 = ext(c, 17, 17)
  x3_18 = ext(d, 18, 18)
  x2_18 = ext(c, 18, 18)
  x3_19 = ext(d, 19, 19)
  x2_19 = ext(c, 19, 19)
  x3_20 = ext(d, 20, 20)
  x2_20 = ext(c, 20, 20)
  x3_21 = ext(d, 21, 21)
  x2_21 = ext(c, 21, 21)
  x3_22 = ext(d, 22, 22)
  x2_22 = ext(c, 22, 22)
  x3_23 = ext(d, 23, 23)
  x2_23 = ext(c, 23, 23)
  x3_24 = ext(d, 24, 24)
  x2_24 = ext(c, 24, 24)
  x3_25 = ext(d, 25, 25)
  x2_25 = ext(c, 25, 25)
  x3_26 = ext(d, 26, 26)
  x2_26 = ext(c, 26, 26)
  x3_27 = ext(d, 27, 27)
  x2_27 = ext(c, 27, 27)
  x3_28 = ext(d, 28, 28)
  x2_28 = ext(c, 28, 28)
  x3_29 = ext(d, 29, 29)
  x2_29 = ext(c, 29, 29)
  x3_30 = ext(d, 30, 30)
  x2_30 = ext(c, 30, 30)
  x3_31 = ext(d, 31, 31)
  x2_31 = ext(c, 31, 31)
  g0 = (x1_31 ^ 1)
  g1 = (x0_31 ^ 1)
  g2 = (g1 | g0)
  g3 = (g2 ^ 1)
  g4 = (g3 & x3_0)
  g5 = (g2 & x2_0)
  g6 = (g5 | g4)
  g7 = (g3 & x3_1)
  g8 = (g2 & x2_1)
  g9 = (g8 | g7)
  g10 = (g3 & x3_2)
  g11 = (g2 & x2_2)
  g12 = (g11 | g10)
  g13 = (g3 & x3_3)
  g14 = (g2 & x2_3)
  g15 = (g14 | g13)
  g16 = (g3 & x3_4)
  g17 = (g2 & x2_4)
  g18 = (g17 | g16)
  g19 = (g3 & x3_5)
  g20 = (g2 & x2_5)
  g21 = (g20 | g19)
  g22 = (g3 & x3_6)
  g23 = (g2 & x2_6)
  g24 = (g23 | g22)
  g25 = (g3 & x3_7)
  g26 = (g2 & x2_7)
  g27 = (g26 | g25)
  g28 = (g3 & x3_8)
  g29 = (g2 & x2_8)
  g30 = (g29 | g28)
  g31 = (g3 & x3_9)
  g32 = (g2 & x2_9)
  g33 = (g32 | g31)
  g34 = (g3 & x3_10)
  g35 = (g2 & x2_10)
  g36 = (g35 | g34)
  g37 = (g3 & x3_11)
  g38 = (g2 & x2_11)
  g39 = (g38 | g37)
  g40 = (g3 & x3_12)
  g41 = (g2 & x2_12)
  g42 = (g41 | g40)
  g43 = (g3 & x3_13)
  g44 = (g2 & x2_13)
  g45 = (g44 | g43)
  g46 = (g3 & x3_14)
  g47 = (g2 & x2_14)
  g48 = (g47 | g46)
  g49 = (g3 & x3_15)
  g50 = (g2 & x2_15)
  g51 = (g50 | g49)
  g52 = (g3 & x3_16)
  g53 = (g2 & x2_16)
  g54 = (g53 | g52)
  g55 = (g3 & x3_17)
  g56 = (g2 & x2_17)
  g57 = (g56 | g55)
  g58 = (g3 & x3_18)
  g59 = (g2 & x2_18)
  g60 = (g59 | g58)
  g61 = (g3 & x3_19)
  g62 = (g2 & x2_19)
  g63 = (g62 | g61)
  g64 = (g3 & x3_20)
  g65 = (g2 & x2_20)
  g66 = (g65 | g64)
  g67 = (g3 & x3_21)
  g68 = (g2 & x2_21)
  g69 = (g68 | g67)
  g70 = (g3 & x3_22)
  g71 = (g2 & x2_22)
  g72 = (g71 | g70)
  g73 = (g3 & x3_23)
  g74 = (g2 & x2_23)
  g75 = (g74 | g73)
  g76 = (g3 & x3_24)
  g77 = (g2 & x2_24)
  g78 = (g77 | g76)
  g79 = (g3 & x3_25)
  g80 = (g2 & x2_25)
  g81 = (g80 | g79)
  g82 = (g3 & x3_26)
  g83 = (g2 & x2_26)
  g84 = (g83 | g82)
  g85 = (g3 & x3_27)
  g86 = (g2 & x2_27)
  g87 = (g86 | g85)
  g88 = (g3 & x3_28)
  g89 = (g2 & x2_28)
  g90 = (g89 | g88)
  g91 = (g3 & x3_29)
  g92 = (g2 & x2_29)
  g93 = (g92 | g91)
  g94 = (g3 & x3_30)
  g95 = (g2 & x2_30)
  g96 = (g95 | g94)
  g97 = (g3 & x3_31)
  g98 = (g2 & x2_31)
  g99 = (g98 | g97)
  k0 = 0
  w0 = k0
  w1 = cat(w0, k0, 1)
  w2 = cat(w1, k0, 1)
  w3 = cat(w2, k0, 1)
  w4 = cat(w3, k0, 1)
  w5 = cat(w4, k0, 1)
  w6 = cat(w5, k0, 1)
  w7 = cat(w6, k0, 1)
  w8 = cat(w7, k0, 1)
  w9 = cat(w8, k0, 1)
  w10 = cat(w9, k0, 1)
  w11 = cat(w10, k0, 1)
  w12 = cat(w11, k0, 1)
  w13 = cat(w12, k0, 1)
  w14 = cat(w13, k0, 1)
  w15 = cat(w14, k0, 1)
  w16 = cat(w15, k0, 1)
  w17 = cat(w16, k0, 1)
  w18 = cat(w17, k0, 1)
  w19 = cat(w18, k0, 1)
  w20 = cat(w19, k0, 1)
  w21 = cat(w20, k0, 1)
  w22 = cat(w21, k0, 1)
  w23 = cat(w22, k0, 1)
  w24 = cat(w23, k0, 1)
  w25 = cat(w24, k0, 1)
  w26 = cat(w25, k0, 1)
  w27 = cat(w26, k0, 1)
  w28 = cat(w27, k0, 1)
  w29 = cat(w28, k0, 1)
  w30 = cat(w29, k0, 1)
  w31 = cat(w30, k0, 1)
  w32 = cat(w31, g99, 1)
  w33 = cat(w32, g96, 1)
  w34 = cat(w33, g93, 1)
  w35 = cat(w34, g90, 1)
  w36 = cat(w35, g87, 1)
  w37 = cat(w36, g84, 1)
  w38 = cat(w37, g81, 1)
  w39 = cat(w38, g78, 1)
  w40 = cat(w39, g75, 1)
  w41 = cat(w40, g72, 1)
  w42 = cat(w41, g69, 1)
  w43 = cat(w42, g66, 1)
  w44 = cat(w43, g63, 1)
  w45 = cat(w44, g60, 1)
  w46 = cat(w45, g57, 1)
  w47 = cat(w46, g54, 1)
  w48 = cat(w47, g51, 1)
  w49 = cat(w48, g48, 1)
  w50 = cat(w49, g45, 1)
  w51 = cat(w50, g42, 1)
  w52 = cat(w51, g39, 1)
  w53 = cat(w52, g36, 1)
  w54 = cat(w53, g33, 1)
  w55 = cat(w54, g30, 1)
  w56 = cat(w55, g27, 1)
  w57 = cat(w56, g24, 1)
  w58 = cat(w57, g21, 1)
  w59 = cat(w58, g18, 1)
  w60 = cat(w59, g15, 1)
  w61 = cat(w60, g12, 1)
  w62 = cat(w61, g9, 1)
  w63 = cat(w62, g6, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_cmovns_gpr_gpr_32__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
