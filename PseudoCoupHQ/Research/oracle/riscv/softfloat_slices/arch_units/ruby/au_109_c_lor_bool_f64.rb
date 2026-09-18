# arch-unit 109  --  c  `a || b`  lhs=bool rhs=double
# symbol op_316   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
#   xori a1, a1, 0x1                   integer  operator:^
#   c.or a0, a1                        integer  operator:|
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_109_c_lor_bool_f64(p0, p1)
  # a0: operand `a` (bool) zero-extended
  v1 = ((p0) & 0x1)
  # fa0: operand `b` (double) arrives in fa0
  v2 = p1
  v3 = 0x0
  v4 = f64_eq_rm0(v2, v3)
  v5 = ((v4) ^ 0x1)
  v6 = ((v1) | (v5))
  v6
end
