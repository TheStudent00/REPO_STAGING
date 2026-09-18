# arch-unit 27  --  c  `a + b`  lhs=double rhs=bool
# symbol op_131   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
#   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_027_c_add_f64_bool(p0, p1)
  # fa0: operand `a` (double) arrives in fa0
  v1 = p0
  # a0: operand `b` (bool) zero-extended
  v2 = ((p1) & 0x1)
  v3 = ui32_to_f64_rm0(((v2) & 0xffffffff))
  v4 = f64_add_rm0(v1, v3)
  v4
end
