# arch-unit 52  --  c  `a * b`  lhs=int64_t rhs=float
# symbol op_183   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
#   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_052_c_mul_i64_f32(p0, p1)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  # fa0: operand `b` (float) arrives in fa0
  v2 = ((p1) & 0xffffffff)
  v3 = i64_to_f32_rm0(v1)
  v4 = f32_mul_rm0(v2, v3)
  ((v4) & 0xffffffff)
end
