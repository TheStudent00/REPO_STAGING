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
# one named local per gate, over the term of andps_xmm_xmm_128__reg_xmm0_low__ruby.
# The term's layer-5 text, LITERAL:
#   ~(~Extract(63, 0, v0) | ~Extract(63, 0, v1))
def emu_andps_xmm_xmm_128__reg_xmm0_low__ruby(a, b)
  x1_0 = ext(b, 0, 0)
  x0_0 = ext(a, 0, 0)
  x1_1 = ext(b, 1, 1)
  x0_1 = ext(a, 1, 1)
  x1_2 = ext(b, 2, 2)
  x0_2 = ext(a, 2, 2)
  x1_3 = ext(b, 3, 3)
  x0_3 = ext(a, 3, 3)
  x1_4 = ext(b, 4, 4)
  x0_4 = ext(a, 4, 4)
  x1_5 = ext(b, 5, 5)
  x0_5 = ext(a, 5, 5)
  x1_6 = ext(b, 6, 6)
  x0_6 = ext(a, 6, 6)
  x1_7 = ext(b, 7, 7)
  x0_7 = ext(a, 7, 7)
  x1_8 = ext(b, 8, 8)
  x0_8 = ext(a, 8, 8)
  x1_9 = ext(b, 9, 9)
  x0_9 = ext(a, 9, 9)
  x1_10 = ext(b, 10, 10)
  x0_10 = ext(a, 10, 10)
  x1_11 = ext(b, 11, 11)
  x0_11 = ext(a, 11, 11)
  x1_12 = ext(b, 12, 12)
  x0_12 = ext(a, 12, 12)
  x1_13 = ext(b, 13, 13)
  x0_13 = ext(a, 13, 13)
  x1_14 = ext(b, 14, 14)
  x0_14 = ext(a, 14, 14)
  x1_15 = ext(b, 15, 15)
  x0_15 = ext(a, 15, 15)
  x1_16 = ext(b, 16, 16)
  x0_16 = ext(a, 16, 16)
  x1_17 = ext(b, 17, 17)
  x0_17 = ext(a, 17, 17)
  x1_18 = ext(b, 18, 18)
  x0_18 = ext(a, 18, 18)
  x1_19 = ext(b, 19, 19)
  x0_19 = ext(a, 19, 19)
  x1_20 = ext(b, 20, 20)
  x0_20 = ext(a, 20, 20)
  x1_21 = ext(b, 21, 21)
  x0_21 = ext(a, 21, 21)
  x1_22 = ext(b, 22, 22)
  x0_22 = ext(a, 22, 22)
  x1_23 = ext(b, 23, 23)
  x0_23 = ext(a, 23, 23)
  x1_24 = ext(b, 24, 24)
  x0_24 = ext(a, 24, 24)
  x1_25 = ext(b, 25, 25)
  x0_25 = ext(a, 25, 25)
  x1_26 = ext(b, 26, 26)
  x0_26 = ext(a, 26, 26)
  x1_27 = ext(b, 27, 27)
  x0_27 = ext(a, 27, 27)
  x1_28 = ext(b, 28, 28)
  x0_28 = ext(a, 28, 28)
  x1_29 = ext(b, 29, 29)
  x0_29 = ext(a, 29, 29)
  x1_30 = ext(b, 30, 30)
  x0_30 = ext(a, 30, 30)
  x1_31 = ext(b, 31, 31)
  x0_31 = ext(a, 31, 31)
  x1_32 = ext(b, 32, 32)
  x0_32 = ext(a, 32, 32)
  x1_33 = ext(b, 33, 33)
  x0_33 = ext(a, 33, 33)
  x1_34 = ext(b, 34, 34)
  x0_34 = ext(a, 34, 34)
  x1_35 = ext(b, 35, 35)
  x0_35 = ext(a, 35, 35)
  x1_36 = ext(b, 36, 36)
  x0_36 = ext(a, 36, 36)
  x1_37 = ext(b, 37, 37)
  x0_37 = ext(a, 37, 37)
  x1_38 = ext(b, 38, 38)
  x0_38 = ext(a, 38, 38)
  x1_39 = ext(b, 39, 39)
  x0_39 = ext(a, 39, 39)
  x1_40 = ext(b, 40, 40)
  x0_40 = ext(a, 40, 40)
  x1_41 = ext(b, 41, 41)
  x0_41 = ext(a, 41, 41)
  x1_42 = ext(b, 42, 42)
  x0_42 = ext(a, 42, 42)
  x1_43 = ext(b, 43, 43)
  x0_43 = ext(a, 43, 43)
  x1_44 = ext(b, 44, 44)
  x0_44 = ext(a, 44, 44)
  x1_45 = ext(b, 45, 45)
  x0_45 = ext(a, 45, 45)
  x1_46 = ext(b, 46, 46)
  x0_46 = ext(a, 46, 46)
  x1_47 = ext(b, 47, 47)
  x0_47 = ext(a, 47, 47)
  x1_48 = ext(b, 48, 48)
  x0_48 = ext(a, 48, 48)
  x1_49 = ext(b, 49, 49)
  x0_49 = ext(a, 49, 49)
  x1_50 = ext(b, 50, 50)
  x0_50 = ext(a, 50, 50)
  x1_51 = ext(b, 51, 51)
  x0_51 = ext(a, 51, 51)
  x1_52 = ext(b, 52, 52)
  x0_52 = ext(a, 52, 52)
  x1_53 = ext(b, 53, 53)
  x0_53 = ext(a, 53, 53)
  x1_54 = ext(b, 54, 54)
  x0_54 = ext(a, 54, 54)
  x1_55 = ext(b, 55, 55)
  x0_55 = ext(a, 55, 55)
  x1_56 = ext(b, 56, 56)
  x0_56 = ext(a, 56, 56)
  x1_57 = ext(b, 57, 57)
  x0_57 = ext(a, 57, 57)
  x1_58 = ext(b, 58, 58)
  x0_58 = ext(a, 58, 58)
  x1_59 = ext(b, 59, 59)
  x0_59 = ext(a, 59, 59)
  x1_60 = ext(b, 60, 60)
  x0_60 = ext(a, 60, 60)
  x1_61 = ext(b, 61, 61)
  x0_61 = ext(a, 61, 61)
  x1_62 = ext(b, 62, 62)
  x0_62 = ext(a, 62, 62)
  x1_63 = ext(b, 63, 63)
  x0_63 = ext(a, 63, 63)
  g0 = (x0_0 & x1_0)
  g1 = (x0_1 & x1_1)
  g2 = (x0_2 & x1_2)
  g3 = (x0_3 & x1_3)
  g4 = (x0_4 & x1_4)
  g5 = (x0_5 & x1_5)
  g6 = (x0_6 & x1_6)
  g7 = (x0_7 & x1_7)
  g8 = (x0_8 & x1_8)
  g9 = (x0_9 & x1_9)
  g10 = (x0_10 & x1_10)
  g11 = (x0_11 & x1_11)
  g12 = (x0_12 & x1_12)
  g13 = (x0_13 & x1_13)
  g14 = (x0_14 & x1_14)
  g15 = (x0_15 & x1_15)
  g16 = (x0_16 & x1_16)
  g17 = (x0_17 & x1_17)
  g18 = (x0_18 & x1_18)
  g19 = (x0_19 & x1_19)
  g20 = (x0_20 & x1_20)
  g21 = (x0_21 & x1_21)
  g22 = (x0_22 & x1_22)
  g23 = (x0_23 & x1_23)
  g24 = (x0_24 & x1_24)
  g25 = (x0_25 & x1_25)
  g26 = (x0_26 & x1_26)
  g27 = (x0_27 & x1_27)
  g28 = (x0_28 & x1_28)
  g29 = (x0_29 & x1_29)
  g30 = (x0_30 & x1_30)
  g31 = (x0_31 & x1_31)
  g32 = (x0_32 & x1_32)
  g33 = (x0_33 & x1_33)
  g34 = (x0_34 & x1_34)
  g35 = (x0_35 & x1_35)
  g36 = (x0_36 & x1_36)
  g37 = (x0_37 & x1_37)
  g38 = (x0_38 & x1_38)
  g39 = (x0_39 & x1_39)
  g40 = (x0_40 & x1_40)
  g41 = (x0_41 & x1_41)
  g42 = (x0_42 & x1_42)
  g43 = (x0_43 & x1_43)
  g44 = (x0_44 & x1_44)
  g45 = (x0_45 & x1_45)
  g46 = (x0_46 & x1_46)
  g47 = (x0_47 & x1_47)
  g48 = (x0_48 & x1_48)
  g49 = (x0_49 & x1_49)
  g50 = (x0_50 & x1_50)
  g51 = (x0_51 & x1_51)
  g52 = (x0_52 & x1_52)
  g53 = (x0_53 & x1_53)
  g54 = (x0_54 & x1_54)
  g55 = (x0_55 & x1_55)
  g56 = (x0_56 & x1_56)
  g57 = (x0_57 & x1_57)
  g58 = (x0_58 & x1_58)
  g59 = (x0_59 & x1_59)
  g60 = (x0_60 & x1_60)
  g61 = (x0_61 & x1_61)
  g62 = (x0_62 & x1_62)
  g63 = (x0_63 & x1_63)
  w0 = g63
  w1 = cat(w0, g62, 1)
  w2 = cat(w1, g61, 1)
  w3 = cat(w2, g60, 1)
  w4 = cat(w3, g59, 1)
  w5 = cat(w4, g58, 1)
  w6 = cat(w5, g57, 1)
  w7 = cat(w6, g56, 1)
  w8 = cat(w7, g55, 1)
  w9 = cat(w8, g54, 1)
  w10 = cat(w9, g53, 1)
  w11 = cat(w10, g52, 1)
  w12 = cat(w11, g51, 1)
  w13 = cat(w12, g50, 1)
  w14 = cat(w13, g49, 1)
  w15 = cat(w14, g48, 1)
  w16 = cat(w15, g47, 1)
  w17 = cat(w16, g46, 1)
  w18 = cat(w17, g45, 1)
  w19 = cat(w18, g44, 1)
  w20 = cat(w19, g43, 1)
  w21 = cat(w20, g42, 1)
  w22 = cat(w21, g41, 1)
  w23 = cat(w22, g40, 1)
  w24 = cat(w23, g39, 1)
  w25 = cat(w24, g38, 1)
  w26 = cat(w25, g37, 1)
  w27 = cat(w26, g36, 1)
  w28 = cat(w27, g35, 1)
  w29 = cat(w28, g34, 1)
  w30 = cat(w29, g33, 1)
  w31 = cat(w30, g32, 1)
  w32 = cat(w31, g31, 1)
  w33 = cat(w32, g30, 1)
  w34 = cat(w33, g29, 1)
  w35 = cat(w34, g28, 1)
  w36 = cat(w35, g27, 1)
  w37 = cat(w36, g26, 1)
  w38 = cat(w37, g25, 1)
  w39 = cat(w38, g24, 1)
  w40 = cat(w39, g23, 1)
  w41 = cat(w40, g22, 1)
  w42 = cat(w41, g21, 1)
  w43 = cat(w42, g20, 1)
  w44 = cat(w43, g19, 1)
  w45 = cat(w44, g18, 1)
  w46 = cat(w45, g17, 1)
  w47 = cat(w46, g16, 1)
  w48 = cat(w47, g15, 1)
  w49 = cat(w48, g14, 1)
  w50 = cat(w49, g13, 1)
  w51 = cat(w50, g12, 1)
  w52 = cat(w51, g11, 1)
  w53 = cat(w52, g10, 1)
  w54 = cat(w53, g9, 1)
  w55 = cat(w54, g8, 1)
  w56 = cat(w55, g7, 1)
  w57 = cat(w56, g6, 1)
  w58 = cat(w57, g5, 1)
  w59 = cat(w58, g4, 1)
  w60 = cat(w59, g3, 1)
  w61 = cat(w60, g2, 1)
  w62 = cat(w61, g1, 1)
  w63 = cat(w62, g0, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_andps_xmm_xmm_128__reg_xmm0_low__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
