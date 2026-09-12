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
# one named local per gate, over the term of sete_gpr_one_8__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 8, v0), If(Extract(7, 0, v1) == Extract(7, 0, v2), 1, 0))
def emu_sete_gpr_one_8__reg_rdi__ruby(a, b, c)
  x1_7 = ext(b, 7, 7)
  x2_7 = ext(a, 7, 7)
  x2_6 = ext(a, 6, 6)
  x1_6 = ext(b, 6, 6)
  x1_5 = ext(b, 5, 5)
  x2_5 = ext(a, 5, 5)
  x1_4 = ext(b, 4, 4)
  x2_4 = ext(a, 4, 4)
  x2_3 = ext(a, 3, 3)
  x1_3 = ext(b, 3, 3)
  x2_2 = ext(a, 2, 2)
  x1_2 = ext(b, 2, 2)
  x2_1 = ext(a, 1, 1)
  x1_1 = ext(b, 1, 1)
  x2_0 = ext(a, 0, 0)
  x1_0 = ext(b, 0, 0)
  x0_8 = ext(c, 8, 8)
  x0_9 = ext(c, 9, 9)
  x0_10 = ext(c, 10, 10)
  x0_11 = ext(c, 11, 11)
  x0_12 = ext(c, 12, 12)
  x0_13 = ext(c, 13, 13)
  x0_14 = ext(c, 14, 14)
  x0_15 = ext(c, 15, 15)
  x0_16 = ext(c, 16, 16)
  x0_17 = ext(c, 17, 17)
  x0_18 = ext(c, 18, 18)
  x0_19 = ext(c, 19, 19)
  x0_20 = ext(c, 20, 20)
  x0_21 = ext(c, 21, 21)
  x0_22 = ext(c, 22, 22)
  x0_23 = ext(c, 23, 23)
  x0_24 = ext(c, 24, 24)
  x0_25 = ext(c, 25, 25)
  x0_26 = ext(c, 26, 26)
  x0_27 = ext(c, 27, 27)
  x0_28 = ext(c, 28, 28)
  x0_29 = ext(c, 29, 29)
  x0_30 = ext(c, 30, 30)
  x0_31 = ext(c, 31, 31)
  x0_32 = ext(c, 32, 32)
  x0_33 = ext(c, 33, 33)
  x0_34 = ext(c, 34, 34)
  x0_35 = ext(c, 35, 35)
  x0_36 = ext(c, 36, 36)
  x0_37 = ext(c, 37, 37)
  x0_38 = ext(c, 38, 38)
  x0_39 = ext(c, 39, 39)
  x0_40 = ext(c, 40, 40)
  x0_41 = ext(c, 41, 41)
  x0_42 = ext(c, 42, 42)
  x0_43 = ext(c, 43, 43)
  x0_44 = ext(c, 44, 44)
  x0_45 = ext(c, 45, 45)
  x0_46 = ext(c, 46, 46)
  x0_47 = ext(c, 47, 47)
  x0_48 = ext(c, 48, 48)
  x0_49 = ext(c, 49, 49)
  x0_50 = ext(c, 50, 50)
  x0_51 = ext(c, 51, 51)
  x0_52 = ext(c, 52, 52)
  x0_53 = ext(c, 53, 53)
  x0_54 = ext(c, 54, 54)
  x0_55 = ext(c, 55, 55)
  x0_56 = ext(c, 56, 56)
  x0_57 = ext(c, 57, 57)
  x0_58 = ext(c, 58, 58)
  x0_59 = ext(c, 59, 59)
  x0_60 = ext(c, 60, 60)
  x0_61 = ext(c, 61, 61)
  x0_62 = ext(c, 62, 62)
  x0_63 = ext(c, 63, 63)
  g0 = (x2_7 ^ 1)
  g1 = (g0 | x1_7)
  g2 = (x1_7 ^ 1)
  g3 = (x2_7 | g2)
  g4 = (x2_6 ^ 1)
  g5 = (x1_6 | g4)
  g6 = (x1_6 ^ 1)
  g7 = (x2_6 | g6)
  g8 = (x2_5 ^ 1)
  g9 = (g8 | x1_5)
  g10 = (x1_5 ^ 1)
  g11 = (x2_5 | g10)
  g12 = (x2_4 ^ 1)
  g13 = (g12 | x1_4)
  g14 = (x1_4 ^ 1)
  g15 = (g14 | x2_4)
  g16 = (x2_3 ^ 1)
  g17 = (x1_3 | g16)
  g18 = (x1_3 ^ 1)
  g19 = (g18 | x2_3)
  g20 = (x2_2 ^ 1)
  g21 = (x1_2 | g20)
  g22 = (x1_2 ^ 1)
  g23 = (x2_2 | g22)
  g24 = (x2_1 ^ 1)
  g25 = (x1_1 | g24)
  g26 = (x1_1 ^ 1)
  g27 = (g26 | x2_1)
  g28 = (x2_0 ^ 1)
  g29 = (x1_0 | g28)
  g30 = (x1_0 ^ 1)
  g31 = (g30 | x2_0)
  g32 = (g31 & g29)
  g33 = (g32 & g27)
  g34 = (g33 & g25)
  g35 = (g34 & g23)
  g36 = (g35 & g21)
  g37 = (g36 & g19)
  g38 = (g37 & g17)
  g39 = (g38 & g15)
  g40 = (g39 & g13)
  g41 = (g40 & g11)
  g42 = (g41 & g9)
  g43 = (g42 & g7)
  g44 = (g43 & g5)
  g45 = (g44 & g3)
  g46 = (g45 & g1)
  k0 = 0
  w0 = x0_63
  w1 = cat(w0, x0_62, 1)
  w2 = cat(w1, x0_61, 1)
  w3 = cat(w2, x0_60, 1)
  w4 = cat(w3, x0_59, 1)
  w5 = cat(w4, x0_58, 1)
  w6 = cat(w5, x0_57, 1)
  w7 = cat(w6, x0_56, 1)
  w8 = cat(w7, x0_55, 1)
  w9 = cat(w8, x0_54, 1)
  w10 = cat(w9, x0_53, 1)
  w11 = cat(w10, x0_52, 1)
  w12 = cat(w11, x0_51, 1)
  w13 = cat(w12, x0_50, 1)
  w14 = cat(w13, x0_49, 1)
  w15 = cat(w14, x0_48, 1)
  w16 = cat(w15, x0_47, 1)
  w17 = cat(w16, x0_46, 1)
  w18 = cat(w17, x0_45, 1)
  w19 = cat(w18, x0_44, 1)
  w20 = cat(w19, x0_43, 1)
  w21 = cat(w20, x0_42, 1)
  w22 = cat(w21, x0_41, 1)
  w23 = cat(w22, x0_40, 1)
  w24 = cat(w23, x0_39, 1)
  w25 = cat(w24, x0_38, 1)
  w26 = cat(w25, x0_37, 1)
  w27 = cat(w26, x0_36, 1)
  w28 = cat(w27, x0_35, 1)
  w29 = cat(w28, x0_34, 1)
  w30 = cat(w29, x0_33, 1)
  w31 = cat(w30, x0_32, 1)
  w32 = cat(w31, x0_31, 1)
  w33 = cat(w32, x0_30, 1)
  w34 = cat(w33, x0_29, 1)
  w35 = cat(w34, x0_28, 1)
  w36 = cat(w35, x0_27, 1)
  w37 = cat(w36, x0_26, 1)
  w38 = cat(w37, x0_25, 1)
  w39 = cat(w38, x0_24, 1)
  w40 = cat(w39, x0_23, 1)
  w41 = cat(w40, x0_22, 1)
  w42 = cat(w41, x0_21, 1)
  w43 = cat(w42, x0_20, 1)
  w44 = cat(w43, x0_19, 1)
  w45 = cat(w44, x0_18, 1)
  w46 = cat(w45, x0_17, 1)
  w47 = cat(w46, x0_16, 1)
  w48 = cat(w47, x0_15, 1)
  w49 = cat(w48, x0_14, 1)
  w50 = cat(w49, x0_13, 1)
  w51 = cat(w50, x0_12, 1)
  w52 = cat(w51, x0_11, 1)
  w53 = cat(w52, x0_10, 1)
  w54 = cat(w53, x0_9, 1)
  w55 = cat(w54, x0_8, 1)
  w56 = cat(w55, k0, 1)
  w57 = cat(w56, k0, 1)
  w58 = cat(w57, k0, 1)
  w59 = cat(w58, k0, 1)
  w60 = cat(w59, k0, 1)
  w61 = cat(w60, k0, 1)
  w62 = cat(w61, k0, 1)
  w63 = cat(w62, g46, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_sete_gpr_one_8__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
