# arch-unit 43  --  c  `a - b`  lhs=double rhs=int64_t
# symbol op_163   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
#   fsub.d fa0, fa0, fa5, dyn          float    emulation:f64_sub_rm0
#   c.jr ra                            integer  return
#
# answer: f64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_043_c_neg_f64_i64(p0, p1)
  # fa0: operand `a` (double) arrives in fa0
  v1 = p0
  # a0: operand `b` (int64_t) arrives in a0
  v2 = p1
  v3 = i64_to_f64_rm0(v2)
  v4 = f64_sub_rm0(v1, v3)
  v4
end
