# arch-unit 1  --  c  `!a`  lhs=double rhs=None
# symbol op_4   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_001_c_not_f64(p0)
  # fa0: operand `a` (double) arrives in fa0
  v1 = p0
  v2 = 0x0
  v3 = f64_eq_rm0(v1, v2)
  v3
end
