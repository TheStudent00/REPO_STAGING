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
# one named local per gate, over the term of neg_gpr_one_8__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 8, v0), Extract(7, 0, v0)*255)
def emu_neg_gpr_one_8__reg_rdi__ruby(a)
  x0_0 = ext(a, 0, 0)
  x0_1 = ext(a, 1, 1)
  x0_2 = ext(a, 2, 2)
  x0_3 = ext(a, 3, 3)
  x0_4 = ext(a, 4, 4)
  x0_5 = ext(a, 5, 5)
  x0_6 = ext(a, 6, 6)
  x0_7 = ext(a, 7, 7)
  x0_8 = ext(a, 8, 8)
  x0_9 = ext(a, 9, 9)
  x0_10 = ext(a, 10, 10)
  x0_11 = ext(a, 11, 11)
  x0_12 = ext(a, 12, 12)
  x0_13 = ext(a, 13, 13)
  x0_14 = ext(a, 14, 14)
  x0_15 = ext(a, 15, 15)
  x0_16 = ext(a, 16, 16)
  x0_17 = ext(a, 17, 17)
  x0_18 = ext(a, 18, 18)
  x0_19 = ext(a, 19, 19)
  x0_20 = ext(a, 20, 20)
  x0_21 = ext(a, 21, 21)
  x0_22 = ext(a, 22, 22)
  x0_23 = ext(a, 23, 23)
  x0_24 = ext(a, 24, 24)
  x0_25 = ext(a, 25, 25)
  x0_26 = ext(a, 26, 26)
  x0_27 = ext(a, 27, 27)
  x0_28 = ext(a, 28, 28)
  x0_29 = ext(a, 29, 29)
  x0_30 = ext(a, 30, 30)
  x0_31 = ext(a, 31, 31)
  x0_32 = ext(a, 32, 32)
  x0_33 = ext(a, 33, 33)
  x0_34 = ext(a, 34, 34)
  x0_35 = ext(a, 35, 35)
  x0_36 = ext(a, 36, 36)
  x0_37 = ext(a, 37, 37)
  x0_38 = ext(a, 38, 38)
  x0_39 = ext(a, 39, 39)
  x0_40 = ext(a, 40, 40)
  x0_41 = ext(a, 41, 41)
  x0_42 = ext(a, 42, 42)
  x0_43 = ext(a, 43, 43)
  x0_44 = ext(a, 44, 44)
  x0_45 = ext(a, 45, 45)
  x0_46 = ext(a, 46, 46)
  x0_47 = ext(a, 47, 47)
  x0_48 = ext(a, 48, 48)
  x0_49 = ext(a, 49, 49)
  x0_50 = ext(a, 50, 50)
  x0_51 = ext(a, 51, 51)
  x0_52 = ext(a, 52, 52)
  x0_53 = ext(a, 53, 53)
  x0_54 = ext(a, 54, 54)
  x0_55 = ext(a, 55, 55)
  x0_56 = ext(a, 56, 56)
  x0_57 = ext(a, 57, 57)
  x0_58 = ext(a, 58, 58)
  x0_59 = ext(a, 59, 59)
  x0_60 = ext(a, 60, 60)
  x0_61 = ext(a, 61, 61)
  x0_62 = ext(a, 62, 62)
  x0_63 = ext(a, 63, 63)
  g0 = (x0_0 ^ x0_1)
  g1 = (g0 ^ 1)
  g2 = (g1 ^ 1)
  g3 = (x0_0 | x0_1)
  g4 = (g3 ^ x0_2)
  g5 = (g4 ^ 1)
  g6 = (g5 ^ 1)
  g7 = (x0_2 | g3)
  g8 = (g7 ^ x0_3)
  g9 = (g8 ^ 1)
  g10 = (g9 ^ 1)
  g11 = (x0_3 | g7)
  g12 = (g11 ^ x0_4)
  g13 = (g12 ^ 1)
  g14 = (g13 ^ 1)
  g15 = (x0_4 | g11)
  g16 = (g15 ^ x0_5)
  g17 = (g16 ^ 1)
  g18 = (g17 ^ 1)
  g19 = (x0_5 | g15)
  g20 = (g19 ^ x0_6)
  g21 = (g20 ^ 1)
  g22 = (g21 ^ 1)
  g23 = (x0_6 | g19)
  g24 = (g23 ^ x0_7)
  g25 = (g24 ^ 1)
  g26 = (g25 ^ 1)
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
  w56 = cat(w55, g26, 1)
  w57 = cat(w56, g22, 1)
  w58 = cat(w57, g18, 1)
  w59 = cat(w58, g14, 1)
  w60 = cat(w59, g10, 1)
  w61 = cat(w60, g6, 1)
  w62 = cat(w61, g2, 1)
  w63 = cat(w62, x0_0, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_neg_gpr_one_8__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
