# arch-unit 91  --  c  `a || b`  lhs=int32_t rhs=double
# symbol op_286   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a0, zero, a0                  integer  operator:<
#   fmv.d.x fa5, zero                  float    bit-manipulation
#   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
#   xori a1, a1, 0x1                   integer  operator:^
#   c.or a0, a1                        integer  operator:|
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_091_c_lor_i32_f64(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN
  v1 = (((((p0) & 0xffffffff) ^ 0x80000000) - 0x80000000) & 0xffffffffffffffff)
  # fa0: operand `b` (double) arrives in fa0
  v2 = p1
  v3 = (((0x0) < (v1)) ? 1 : 0)
  v4 = 0x0
  v5 = f64_eq_rm0(v2, v4)
  v6 = ((v5) ^ 0x1)
  v7 = ((v3) | (v6))
  v7
end
