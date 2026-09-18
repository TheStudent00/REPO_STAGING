# arch-unit 104  --  c  `a || b`  lhs=double rhs=uint64_t
# symbol op_308   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
#   xori a1, a1, 0x1                   integer  operator:^
#   sltu a0, zero, a0                  integer  operator:<
#   c.or a0, a1                        integer  operator:|
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_104_c_lor_f64_u64(p0, p1)
  # fa0: operand `a` (double) arrives in fa0
  v1 = p0
  # a0: operand `b` (uint64_t) arrives in a0
  v2 = p1
  v3 = 0x0
  v4 = f64_eq_rm0(v1, v3)
  v5 = ((v4) ^ 0x1)
  v6 = (((0x0) < (v2)) ? 1 : 0)
  v7 = ((v6) | (v5))
  v7
end
