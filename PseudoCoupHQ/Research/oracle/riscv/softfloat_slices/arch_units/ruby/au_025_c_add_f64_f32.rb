# arch-unit 25  --  c  `a + b`  lhs=double rhs=float
# symbol op_129   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.s fa5, fa1                  float    emulation:f32_to_f64_rm0
#   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_025_c_add_f64_f32(p0, p1)
  # fa0: operand `a` (double) arrives in fa0
  v1 = p0
  # fa1: operand `b` (float) arrives in fa1
  v2 = ((p1) & 0xffffffff)
  v3 = f32_to_f64_rm0(v2)
  v4 = f64_add_rm0(v1, v3)
  v4
end
