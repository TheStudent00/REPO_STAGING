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
# one named local per gate, over the term of cmp_imm_gpr_8__flags__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(Extract(7, 0, v0), Extract(7, 0, v1))
def emu_cmp_imm_gpr_8__flags__ruby(a, b)
  x1_0 = ext(b, 0, 0)
  x1_1 = ext(b, 1, 1)
  x1_2 = ext(b, 2, 2)
  x1_3 = ext(b, 3, 3)
  x1_4 = ext(b, 4, 4)
  x1_5 = ext(b, 5, 5)
  x1_6 = ext(b, 6, 6)
  x1_7 = ext(b, 7, 7)
  x0_0 = ext(a, 0, 0)
  x0_1 = ext(a, 1, 1)
  x0_2 = ext(a, 2, 2)
  x0_3 = ext(a, 3, 3)
  x0_4 = ext(a, 4, 4)
  x0_5 = ext(a, 5, 5)
  x0_6 = ext(a, 6, 6)
  x0_7 = ext(a, 7, 7)
  w0 = x0_7
  w1 = cat(w0, x0_6, 1)
  w2 = cat(w1, x0_5, 1)
  w3 = cat(w2, x0_4, 1)
  w4 = cat(w3, x0_3, 1)
  w5 = cat(w4, x0_2, 1)
  w6 = cat(w5, x0_1, 1)
  w7 = cat(w6, x0_0, 1)
  w8 = cat(w7, x1_7, 1)
  w9 = cat(w8, x1_6, 1)
  w10 = cat(w9, x1_5, 1)
  w11 = cat(w10, x1_4, 1)
  w12 = cat(w11, x1_3, 1)
  w13 = cat(w12, x1_2, 1)
  w14 = cat(w13, x1_1, 1)
  w15 = cat(w14, x1_0, 1)
  m(w15, 16)
end



STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_cmp_imm_gpr_8__flags__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
