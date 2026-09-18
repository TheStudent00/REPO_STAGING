# arch-unit 50  --  c  `a * b`  lhs=int32_t rhs=float
# symbol op_177   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
#   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_050_c_mul_i32_f32(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN
  v1 = (((((p0) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
  # fa0: operand `b` (float) arrives in fa0
  v2 = ((p1) & 0xffffffff)
  v3 = i32_to_f32_rm0(((v1) & 0xffffffff))
  v4 = f32_mul_rm0(v2, v3)
  ((v4) & 0xffffffff)
end
