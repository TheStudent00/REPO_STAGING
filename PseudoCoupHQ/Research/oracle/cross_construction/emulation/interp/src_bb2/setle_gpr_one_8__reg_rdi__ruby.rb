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
# one named local per gate, over the term of setle_gpr_one_8__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(63, 8, v2), If(Or(Extract(7, 0, v0) == Extract(7, 0, v1), Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))) == Extract(8, 8, Concat(Extract(7, 7, v0), Extract(7, 0, v0))*511 + Concat(Extract(7, 7, v1), Extract(7, 0, v1))), 1, 0)), 1, 0))
def emu_setle_gpr_one_8__reg_rdi__ruby(a, b, c)
  x0_7 = ext(b, 7, 7)
  x0_1 = ext(b, 1, 1)
  x0_0 = ext(b, 0, 0)
  x0_2 = ext(b, 2, 2)
  x0_3 = ext(b, 3, 3)
  x0_4 = ext(b, 4, 4)
  x0_5 = ext(b, 5, 5)
  x0_6 = ext(b, 6, 6)
  x1_6 = ext(a, 6, 6)
  x1_2 = ext(a, 2, 2)
  x1_1 = ext(a, 1, 1)
  x1_0 = ext(a, 0, 0)
  x1_3 = ext(a, 3, 3)
  x1_4 = ext(a, 4, 4)
  x1_5 = ext(a, 5, 5)
  x1_7 = ext(a, 7, 7)
  x2_8 = ext(c, 8, 8)
  x2_9 = ext(c, 9, 9)
  x2_10 = ext(c, 10, 10)
  x2_11 = ext(c, 11, 11)
  x2_12 = ext(c, 12, 12)
  x2_13 = ext(c, 13, 13)
  x2_14 = ext(c, 14, 14)
  x2_15 = ext(c, 15, 15)
  x2_16 = ext(c, 16, 16)
  x2_17 = ext(c, 17, 17)
  x2_18 = ext(c, 18, 18)
  x2_19 = ext(c, 19, 19)
  x2_20 = ext(c, 20, 20)
  x2_21 = ext(c, 21, 21)
  x2_22 = ext(c, 22, 22)
  x2_23 = ext(c, 23, 23)
  x2_24 = ext(c, 24, 24)
  x2_25 = ext(c, 25, 25)
  x2_26 = ext(c, 26, 26)
  x2_27 = ext(c, 27, 27)
  x2_28 = ext(c, 28, 28)
  x2_29 = ext(c, 29, 29)
  x2_30 = ext(c, 30, 30)
  x2_31 = ext(c, 31, 31)
  x2_32 = ext(c, 32, 32)
  x2_33 = ext(c, 33, 33)
  x2_34 = ext(c, 34, 34)
  x2_35 = ext(c, 35, 35)
  x2_36 = ext(c, 36, 36)
  x2_37 = ext(c, 37, 37)
  x2_38 = ext(c, 38, 38)
  x2_39 = ext(c, 39, 39)
  x2_40 = ext(c, 40, 40)
  x2_41 = ext(c, 41, 41)
  x2_42 = ext(c, 42, 42)
  x2_43 = ext(c, 43, 43)
  x2_44 = ext(c, 44, 44)
  x2_45 = ext(c, 45, 45)
  x2_46 = ext(c, 46, 46)
  x2_47 = ext(c, 47, 47)
  x2_48 = ext(c, 48, 48)
  x2_49 = ext(c, 49, 49)
  x2_50 = ext(c, 50, 50)
  x2_51 = ext(c, 51, 51)
  x2_52 = ext(c, 52, 52)
  x2_53 = ext(c, 53, 53)
  x2_54 = ext(c, 54, 54)
  x2_55 = ext(c, 55, 55)
  x2_56 = ext(c, 56, 56)
  x2_57 = ext(c, 57, 57)
  x2_58 = ext(c, 58, 58)
  x2_59 = ext(c, 59, 59)
  x2_60 = ext(c, 60, 60)
  x2_61 = ext(c, 61, 61)
  x2_62 = ext(c, 62, 62)
  x2_63 = ext(c, 63, 63)
  g0 = (x0_0 | x0_1)
  g1 = (x0_2 | g0)
  g2 = (x0_3 | g1)
  g3 = (x0_4 | g2)
  g4 = (x0_5 | g3)
  g5 = (x0_6 | g4)
  g6 = (x0_7 | g5)
  g7 = (g6 ^ x0_7)
  g8 = (g7 ^ 1)
  g9 = (x1_6 ^ 1)
  g10 = (g4 ^ x0_6)
  g11 = (g10 ^ 1)
  g12 = (g11 | g9)
  g13 = (g12 ^ 1)
  g14 = (x1_2 ^ 1)
  g15 = (g0 ^ x0_2)
  g16 = (g15 ^ 1)
  g17 = (g16 | g14)
  g18 = (g17 ^ 1)
  g19 = (x0_0 ^ x0_1)
  g20 = (g19 ^ 1)
  g21 = (x1_1 ^ 1)
  g22 = (g21 | g20)
  g23 = (g22 ^ 1)
  g24 = (x1_0 ^ 1)
  g25 = (x0_0 ^ 1)
  g26 = (g25 | g24)
  g27 = (g21 | g26)
  g28 = (g27 ^ 1)
  g29 = (g20 | g26)
  g30 = (g29 ^ 1)
  g31 = (g30 | g28)
  g32 = (g31 | g23)
  g33 = (g32 ^ 1)
  g34 = (g16 | g33)
  g35 = (g34 ^ 1)
  g36 = (g14 | g33)
  g37 = (g36 ^ 1)
  g38 = (g37 | g35)
  g39 = (g38 | g18)
  g40 = (g39 ^ 1)
  g41 = (x1_3 ^ 1)
  g42 = (g41 | g40)
  g43 = (g42 ^ 1)
  g44 = (g1 ^ x0_3)
  g45 = (g44 ^ 1)
  g46 = (g41 | g45)
  g47 = (g46 ^ 1)
  g48 = (g45 | g40)
  g49 = (g48 ^ 1)
  g50 = (g49 | g47)
  g51 = (g50 | g43)
  g52 = (g51 ^ 1)
  g53 = (g2 ^ x0_4)
  g54 = (g53 ^ 1)
  g55 = (g54 | g52)
  g56 = (g55 ^ 1)
  g57 = (x1_4 ^ 1)
  g58 = (g57 | g54)
  g59 = (g58 ^ 1)
  g60 = (g57 | g52)
  g61 = (g60 ^ 1)
  g62 = (g61 | g59)
  g63 = (g62 | g56)
  g64 = (g63 ^ 1)
  g65 = (x1_5 ^ 1)
  g66 = (g65 | g64)
  g67 = (g66 ^ 1)
  g68 = (g3 ^ x0_5)
  g69 = (g68 ^ 1)
  g70 = (g69 | g64)
  g71 = (g70 ^ 1)
  g72 = (g69 | g65)
  g73 = (g72 ^ 1)
  g74 = (g73 | g71)
  g75 = (g74 | g67)
  g76 = (g75 ^ 1)
  g77 = (g11 | g76)
  g78 = (g77 ^ 1)
  g79 = (g9 | g76)
  g80 = (g79 ^ 1)
  g81 = (g80 | g78)
  g82 = (g81 | g13)
  g83 = (g82 ^ 1)
  g84 = (x1_7 ^ 1)
  g85 = (g84 | g83)
  g86 = (g85 ^ 1)
  g87 = (g5 ^ x0_7)
  g88 = (g87 ^ 1)
  g89 = (g84 | g88)
  g90 = (g89 ^ 1)
  g91 = (g83 | g88)
  g92 = (g91 ^ 1)
  g93 = (g92 | g90)
  g94 = (g93 | g86)
  g95 = (x1_7 ^ g94)
  g96 = (g95 ^ 1)
  g97 = (g96 ^ g8)
  g98 = (g97 ^ 1)
  g99 = (x1_7 ^ g82)
  g100 = (g99 ^ 1)
  g101 = (g100 ^ g88)
  g102 = (g101 ^ 1)
  g103 = (g102 ^ g98)
  g104 = (g103 ^ 1)
  g105 = (g102 ^ g104)
  g106 = (g105 ^ 1)
  g107 = (g106 ^ 1)
  g108 = (g84 | x0_7)
  g109 = (x0_7 ^ 1)
  g110 = (g109 | x1_7)
  g111 = (x0_6 | g9)
  g112 = (x0_6 ^ 1)
  g113 = (g112 | x1_6)
  g114 = (x0_5 | g65)
  g115 = (x0_5 ^ 1)
  g116 = (g115 | x1_5)
  g117 = (g57 | x0_4)
  g118 = (x0_4 ^ 1)
  g119 = (g118 | x1_4)
  g120 = (g41 | x0_3)
  g121 = (x0_3 ^ 1)
  g122 = (x1_3 | g121)
  g123 = (g14 | x0_2)
  g124 = (x0_2 ^ 1)
  g125 = (x1_2 | g124)
  g126 = (g21 | x0_1)
  g127 = (x0_1 ^ 1)
  g128 = (g127 | x1_1)
  g129 = (x0_0 | g24)
  g130 = (g25 | x1_0)
  g131 = (g130 & g129)
  g132 = (g131 & g128)
  g133 = (g132 & g126)
  g134 = (g133 & g125)
  g135 = (g134 & g123)
  g136 = (g135 & g122)
  g137 = (g136 & g120)
  g138 = (g137 & g119)
  g139 = (g138 & g117)
  g140 = (g139 & g116)
  g141 = (g140 & g114)
  g142 = (g141 & g113)
  g143 = (g142 & g111)
  g144 = (g143 & g110)
  g145 = (g144 & g108)
  g146 = (g145 | g107)
  k0 = 0
  w0 = x2_63
  w1 = cat(w0, x2_62, 1)
  w2 = cat(w1, x2_61, 1)
  w3 = cat(w2, x2_60, 1)
  w4 = cat(w3, x2_59, 1)
  w5 = cat(w4, x2_58, 1)
  w6 = cat(w5, x2_57, 1)
  w7 = cat(w6, x2_56, 1)
  w8 = cat(w7, x2_55, 1)
  w9 = cat(w8, x2_54, 1)
  w10 = cat(w9, x2_53, 1)
  w11 = cat(w10, x2_52, 1)
  w12 = cat(w11, x2_51, 1)
  w13 = cat(w12, x2_50, 1)
  w14 = cat(w13, x2_49, 1)
  w15 = cat(w14, x2_48, 1)
  w16 = cat(w15, x2_47, 1)
  w17 = cat(w16, x2_46, 1)
  w18 = cat(w17, x2_45, 1)
  w19 = cat(w18, x2_44, 1)
  w20 = cat(w19, x2_43, 1)
  w21 = cat(w20, x2_42, 1)
  w22 = cat(w21, x2_41, 1)
  w23 = cat(w22, x2_40, 1)
  w24 = cat(w23, x2_39, 1)
  w25 = cat(w24, x2_38, 1)
  w26 = cat(w25, x2_37, 1)
  w27 = cat(w26, x2_36, 1)
  w28 = cat(w27, x2_35, 1)
  w29 = cat(w28, x2_34, 1)
  w30 = cat(w29, x2_33, 1)
  w31 = cat(w30, x2_32, 1)
  w32 = cat(w31, x2_31, 1)
  w33 = cat(w32, x2_30, 1)
  w34 = cat(w33, x2_29, 1)
  w35 = cat(w34, x2_28, 1)
  w36 = cat(w35, x2_27, 1)
  w37 = cat(w36, x2_26, 1)
  w38 = cat(w37, x2_25, 1)
  w39 = cat(w38, x2_24, 1)
  w40 = cat(w39, x2_23, 1)
  w41 = cat(w40, x2_22, 1)
  w42 = cat(w41, x2_21, 1)
  w43 = cat(w42, x2_20, 1)
  w44 = cat(w43, x2_19, 1)
  w45 = cat(w44, x2_18, 1)
  w46 = cat(w45, x2_17, 1)
  w47 = cat(w46, x2_16, 1)
  w48 = cat(w47, x2_15, 1)
  w49 = cat(w48, x2_14, 1)
  w50 = cat(w49, x2_13, 1)
  w51 = cat(w50, x2_12, 1)
  w52 = cat(w51, x2_11, 1)
  w53 = cat(w52, x2_10, 1)
  w54 = cat(w53, x2_9, 1)
  w55 = cat(w54, x2_8, 1)
  w56 = cat(w55, k0, 1)
  w57 = cat(w56, k0, 1)
  w58 = cat(w57, k0, 1)
  w59 = cat(w58, k0, 1)
  w60 = cat(w59, k0, 1)
  w61 = cat(w60, k0, 1)
  w62 = cat(w61, k0, 1)
  w63 = cat(w62, g146, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_setle_gpr_one_8__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
