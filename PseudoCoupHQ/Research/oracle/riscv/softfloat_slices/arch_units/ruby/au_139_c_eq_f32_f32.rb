# arch-unit 139  --  c  `a == b`  lhs=float rhs=float
# symbol op_483   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_139_c_eq_f32_f32(p0, p1)
  # fa0: operand `a` (float) arrives in fa0
  v1 = ((p0) & 0xffffffff)
  # fa1: operand `b` (float) arrives in fa1
  v2 = ((p1) & 0xffffffff)
  v3 = f32_eq_rm0(v1, v2)
  v3
end
