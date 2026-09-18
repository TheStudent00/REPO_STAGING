# arch-unit 396  --  c  `a == b`  lhs=int64_t rhs=int64_t
# symbol op_469   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_396_c_eq_i64_i64(p0, p1)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  # a1: operand `b` (int64_t) arrives in a1
  v2 = p1
  v3 = au_xor(v1, v2)
  v4 = au_sltu(v3, 0x1)
  # the answer is int32_t, 32 bits
  ((v4) & 0xffffffff)
end
