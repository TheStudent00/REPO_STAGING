# arch-unit 88  --  c  `a / b`  lhs=bool rhs=float
# symbol op_243   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
#   fdiv.s fa0, fa5, fa0, dyn          float    emulation:f32_div_rm0
#   c.jr ra                            integer  return
#
# answer: f32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_088_c_div_bool_f32(p0, p1)
  # a0: operand `a` (bool) zero-extended
  v1 = ((p0) & 0x1)
  # fa0: operand `b` (float) arrives in fa0
  v2 = ((p1) & 0xffffffff)
  v3 = ui32_to_f32_rm0(((v1) & 0xffffffff))
  v4 = f32_div_rm0(v3, v2)
  ((v4) & 0xffffffff)
end
