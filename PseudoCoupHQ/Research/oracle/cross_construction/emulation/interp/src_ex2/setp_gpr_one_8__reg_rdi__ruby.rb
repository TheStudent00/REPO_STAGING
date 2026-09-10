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

# task ex1 emulation -- rendered by interp_render.py
# InterpRenderer from the layer-4 term of setp_gpr_one_8__reg_rdi__ruby.
# The term's layer-5 text, LITERAL:
#   Concat(0, If(Extract(1, 1, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(2, 2, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(3, 3, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(4, 4, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(5, 5, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(6, 6, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(0, 0, v1) + 1 == Extract(0, 0, v0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0))
def emu_setp_gpr_one_8__reg_rdi__ruby(a, b)
  m(cat(0, ((eq(ext(add(mul(b, 255, 8), a, 8), 1, 1), ((eq(ext(add(mul(b, 255, 8), a, 8), 2, 2), ((eq(ext(add(mul(b, 255, 8), a, 8), 3, 3), ((eq(ext(add(mul(b, 255, 8), a, 8), 4, 4), ((eq(ext(add(mul(b, 255, 8), a, 8), 5, 5), ((eq(ext(add(mul(b, 255, 8), a, 8), 6, 6), ((eq(ext(add(mul(b, 255, 8), a, 8), 7, 7), ((eq(add(ext(a, 0, 0), 1, 1), ext(b, 0, 0), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 1)) ? (1) : (0)), 8), 64)
end


STDIN.each_line do |line|
  text = line.strip
  next if text.empty?
  values = text.split.map { |one| one.to_i }
  begin
    puts emu_setp_gpr_one_8__reg_rdi__ruby(*values)
  rescue Exception => problem
    puts "RAISE:#{problem.class}"
  end
end
