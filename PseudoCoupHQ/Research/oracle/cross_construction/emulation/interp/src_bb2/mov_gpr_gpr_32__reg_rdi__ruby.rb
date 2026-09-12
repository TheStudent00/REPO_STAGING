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
# one named local per gate, over the term of mov_gpr_gpr_32__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(0, Extract(31, 0, v0))
def emu_mov_gpr_gpr_32__reg_rdi__ruby(a)
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
  w56 = cat(w55, x0_7, 1)
  w57 = cat(w56, x0_6, 1)
  w58 = cat(w57, x0_5, 1)
  w59 = cat(w58, x0_4, 1)
  w60 = cat(w59, x0_3, 1)
  w61 = cat(w60, x0_2, 1)
  w62 = cat(w61, x0_1, 1)
  w63 = cat(w62, x0_0, 1)
  m(w63, 64)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_mov_gpr_gpr_32__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
