# arch-unit 92  --  c  `a || b`  lhs=int64_t rhs=float
# symbol op_291   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a0, zero, a0                  integer  operator:<
#   fmv.w.x fa5, zero                  float    bit-manipulation
#   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
#   xori a1, a1, 0x1                   integer  operator:^
#   c.or a0, a1                        integer  operator:|
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_092_c_lor_i64_f32(p0, p1)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  # fa0: operand `b` (float) arrives in fa0
  v2 = ((p1) & 0xffffffff)
  v3 = (((0x0) < (v1)) ? 1 : 0)
  v4 = ((0x0) & 0xffffffff)
  v5 = f32_eq_rm0(v2, v4)
  v6 = ((v5) ^ 0x1)
  v7 = ((v3) | (v6))
  v7
end
