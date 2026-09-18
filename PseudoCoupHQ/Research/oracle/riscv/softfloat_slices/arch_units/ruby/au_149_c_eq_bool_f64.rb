# arch-unit 149  --  c  `a == b`  lhs=bool rhs=double
# symbol op_496   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_149_c_eq_bool_f64(p0, p1)
  # a0: operand `a` (bool) zero-extended
  v1 = ((p0) & 0x1)
  # fa0: operand `b` (double) arrives in fa0
  v2 = p1
  v3 = ui32_to_f64_rm0(((v1) & 0xffffffff))
  v4 = f64_eq_rm0(v2, v3)
  v4
end
