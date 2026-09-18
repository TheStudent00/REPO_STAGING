# arch-unit 98  --  c  `a || b`  lhs=float rhs=uint64_t
# symbol op_302   outcome LIFTED
#
# the arch-unit, arch-opcode by arch-opcode:
#   fmv.w.x fa5, zero                  float    bit-manipulation
#   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
#   xori a1, a1, 0x1                   integer  operator:^
#   sltu a0, zero, a0                  integer  operator:<
#   c.or a0, a1                        integer  operator:|
#   c.jr ra                            integer  return
#
# answer: int, 64 bits.  parameters are operand bit patterns.
require_relative 'au_float'

def au_098_c_lor_f32_u64(p0, p1)
  # fa0: operand `a` (float) arrives in fa0
  v1 = ((p0) & 0xffffffff)
  # a0: operand `b` (uint64_t) arrives in a0
  v2 = p1
  v3 = ((0x0) & 0xffffffff)
  v4 = f32_eq_rm0(v1, v3)
  v5 = ((v4) ^ 0x1)
  v6 = (((0x0) < (v2)) ? 1 : 0)
  v7 = ((v6) | (v5))
  v7
end
