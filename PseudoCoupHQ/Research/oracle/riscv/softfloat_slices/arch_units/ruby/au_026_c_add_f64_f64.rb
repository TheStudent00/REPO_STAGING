# arch-unit 26  --  c  `a + b`  lhs=double rhs=double
# symbol op_130   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fadd.d fa0, fa0, fa1, dyn          float    emulation:f64_add_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_026_c_add_f64_f64(p0, p1)
  # fa0: operand `a` (double) arrives in fa0
  v1 = p0
  # fa1: operand `b` (double) arrives in fa1
  v2 = p1
  v3 = f64_add_rm0(v1, v2)
  v3
end
