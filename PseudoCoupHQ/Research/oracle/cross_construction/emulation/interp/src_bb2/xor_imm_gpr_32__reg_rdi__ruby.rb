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
# one named local per gate, over the term of xor_imm_gpr_32__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(0, Extract(31, 0, v0) ^ Extract(31, 0, v1))
def emu_xor_imm_gpr_32__reg_rdi__ruby(a, b)
  x1_0 = ext(a, 0, 0)
  x0_0 = ext(b, 0, 0)
  x1_1 = ext(a, 1, 1)
  x0_1 = ext(b, 1, 1)
  x1_2 = ext(a, 2, 2)
  x0_2 = ext(b, 2, 2)
  x1_3 = ext(a, 3, 3)
  x0_3 = ext(b, 3, 3)
  x1_4 = ext(a, 4, 4)
  x0_4 = ext(b, 4, 4)
  x1_5 = ext(a, 5, 5)
  x0_5 = ext(b, 5, 5)
  x1_6 = ext(a, 6, 6)
  x0_6 = ext(b, 6, 6)
  x1_7 = ext(a, 7, 7)
  x0_7 = ext(b, 7, 7)
  x1_8 = ext(a, 8, 8)
  x0_8 = ext(b, 8, 8)
  x1_9 = ext(a, 9, 9)
  x0_9 = ext(b, 9, 9)
  x1_10 = ext(a, 10, 10)
  x0_10 = ext(b, 10, 10)
  x1_11 = ext(a, 11, 11)
  x0_11 = ext(b, 11, 11)
  x1_12 = ext(a, 12, 12)
  x0_12 = ext(b, 12, 12)
  x1_13 = ext(a, 13, 13)
  x0_13 = ext(b, 13, 13)
  x1_14 = ext(a, 14, 14)
  x0_14 = ext(b, 14, 14)
  x1_15 = ext(a, 15, 15)
  x0_15 = ext(b, 15, 15)
  x1_16 = ext(a, 16, 16)
  x0_16 = ext(b, 16, 16)
  x1_17 = ext(a, 17, 17)
  x0_17 = ext(b, 17, 17)
  x1_18 = ext(a, 18, 18)
  x0_18 = ext(b, 18, 18)
  x1_19 = ext(a, 19, 19)
  x0_19 = ext(b, 19, 19)
  x1_20 = ext(a, 20, 20)
  x0_20 = ext(b, 20, 20)
  x1_21 = ext(a, 21, 21)
  x0_21 = ext(b, 21, 21)
  x1_22 = ext(a, 22, 22)
  x0_22 = ext(b, 22, 22)
  x1_23 = ext(a, 23, 23)
  x0_23 = ext(b, 23, 23)
  x1_24 = ext(a, 24, 24)
  x0_24 = ext(b, 24, 24)
  x1_25 = ext(a, 25, 25)
  x0_25 = ext(b, 25, 25)
  x1_26 = ext(a, 26, 26)
  x0_26 = ext(b, 26, 26)
  x1_27 = ext(a, 27, 27)
  x0_27 = ext(b, 27, 27)
  x1_28 = ext(a, 28, 28)
  x0_28 = ext(b, 28, 28)
  x1_29 = ext(a, 29, 29)
  x0_29 = ext(b, 29, 29)
  x1_30 = ext(a, 30, 30)
  x0_30 = ext(b, 30, 30)
  x1_31 = ext(a, 31, 31)
  x0_31 = ext(b, 31, 31)
  g0 = (x0_0 ^ x1_0)
  g1 = (g0 ^ 1)
  g2 = (g1 ^ 1)
  g3 = (x0_1 ^ x1_1)
  g4 = (g3 ^ 1)
  g5 = (g4 ^ 1)
  g6 = (x0_2 ^ x1_2)
  g7 = (g6 ^ 1)
  g8 = (g7 ^ 1)
  g9 = (x0_3 ^ x1_3)
  g10 = (g9 ^ 1)
  g11 = (g10 ^ 1)
  g12 = (x0_4 ^ x1_4)
  g13 = (g12 ^ 1)
  g14 = (g13 ^ 1)
  g15 = (x0_5 ^ x1_5)
  g16 = (g15 ^ 1)
  g17 = (g16 ^ 1)
  g18 = (x0_6 ^ x1_6)
  g19 = (g18 ^ 1)
  g20 = (g19 ^ 1)
  g21 = (x0_7 ^ x1_7)
  g22 = (g21 ^ 1)
  g23 = (g22 ^ 1)
  g24 = (x0_8 ^ x1_8)
  g25 = (g24 ^ 1)
  g26 = (g25 ^ 1)
  g27 = (x0_9 ^ x1_9)
  g28 = (g27 ^ 1)
  g29 = (g28 ^ 1)
  g30 = (x0_10 ^ x1_10)
  g31 = (g30 ^ 1)
  g32 = (g31 ^ 1)
  g33 = (x0_11 ^ x1_11)
  g34 = (g33 ^ 1)
  g35 = (g34 ^ 1)
  g36 = (x0_12 ^ x1_12)
  g37 = (g36 ^ 1)
  g38 = (g37 ^ 1)
  g39 = (x0_13 ^ x1_13)
  g40 = (g39 ^ 1)
  g41 = (g40 ^ 1)
  g42 = (x0_14 ^ x1_14)
  g43 = (g42 ^ 1)
  g44 = (g43 ^ 1)
  g45 = (x0_15 ^ x1_15)
  g46 = (g45 ^ 1)
  g47 = (g46 ^ 1)
  g48 = (x0_16 ^ x1_16)
  g49 = (g48 ^ 1)
  g50 = (g49 ^ 1)
  g51 = (x0_17 ^ x1_17)
  g52 = (g51 ^ 1)
  g53 = (g52 ^ 1)
  g54 = (x0_18 ^ x1_18)
  g55 = (g54 ^ 1)
  g56 = (g55 ^ 1)
  g57 = (x0_19 ^ x1_19)
  g58 = (g57 ^ 1)
  g59 = (g58 ^ 1)
  g60 = (x0_20 ^ x1_20)
  g61 = (g60 ^ 1)
  g62 = (g61 ^ 1)
  g63 = (x0_21 ^ x1_21)
  g64 = (g63 ^ 1)
  g65 = (g64 ^ 1)
  g66 = (x0_22 ^ x1_22)
  g67 = (g66 ^ 1)
  g68 = (g67 ^ 1)
  g69 = (x0_23 ^ x1_23)
  g70 = (g69 ^ 1)
  g71 = (g70 ^ 1)
  g72 = (x0_24 ^ x1_24)
  g73 = (g72 ^ 1)
  g74 = (g73 ^ 1)
  g75 = (x0_25 ^ x1_25)
  g76 = (g75 ^ 1)
  g77 = (g76 ^ 1)
  g78 = (x0_26 ^ x1_26)
  g79 = (g78 ^ 1)
  g80 = (g79 ^ 1)
  g81 = (x0_27 ^ x1_27)
  g82 = (g81 ^ 1)
  g83 = (g82 ^ 1)
  g84 = (x0_28 ^ x1_28)
  g85 = (g84 ^ 1)
  g86 = (g85 ^ 1)
  g87 = (x0_29 ^ x1_29)
  g88 = (g87 ^ 1)
  g89 = (g88 ^ 1)
  g90 = (x0_30 ^ x1_30)
  g91 = (g90 ^ 1)
  g92 = (g91 ^ 1)
  g93 = (x0_31 ^ x1_31)
  g94 = (g93 ^ 1)
  g95 = (g94 ^ 1)
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
  w32 = cat(w31, g95, 1)
  w33 = cat(w32, g92, 1)
  w34 = cat(w33, g89, 1)
  w35 = cat(w34, g86, 1)
  w36 = cat(w35, g83, 1)
  w37 = cat(w36, g80, 1)
  w38 = cat(w37, g77, 1)
  w39 = cat(w38, g74, 1)
  w40 = cat(w39, g71, 1)
  w41 = cat(w40, g68, 1)
  w42 = cat(w41, g65, 1)
  w43 = cat(w42, g62, 1)
  w44 = cat(w43, g59, 1)
  w45 = cat(w44, g56, 1)
  w46 = cat(w45, g53, 1)
  w47 = cat(w46, g50, 1)
  w48 = cat(w47, g47, 1)
  w49 = cat(w48, g44, 1)
  w50 = cat(w49, g41, 1)
  w51 = cat(w50, g38, 1)
  w52 = cat(w51, g35, 1)
  w53 = cat(w52, g32, 1)
  w54 = cat(w53, g29, 1)
  w55 = cat(w54, g26, 1)
  w56 = cat(w55, g23, 1)
  w57 = cat(w56, g20, 1)
  w58 = cat(w57, g17, 1)
  w59 = cat(w58, g14, 1)
  w60 = cat(w59, g11, 1)
  w61 = cat(w60, g8, 1)
  w62 = cat(w61, g5, 1)
  w63 = cat(w62, g2, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_xor_imm_gpr_32__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
