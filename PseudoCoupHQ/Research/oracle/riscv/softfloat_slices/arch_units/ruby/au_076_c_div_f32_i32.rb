# arch-unit 76  --  c  `a / b`  lhs=float rhs=int32_t
# symbol op_228   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
#   fdiv.s fa0, fa0, fa5, dyn          float    emulation:f32_div_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_076_c_div_f32_i32(p0, p1)
  # fa0: operand `a` (float) arrives in fa0
  v1 = ((p0) & 0xffffffff)
  # a0: operand `b` (int32_t) sign-extended to XLEN
  v2 = (((((p1) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
  v3 = i32_to_f32_rm0(((v2) & 0xffffffff))
  v4 = f32_div_rm0(v1, v3)
  ((v4) & 0xffffffff)
end
