# arch-unit 179  --  c  `-a`  lhs=int64_t rhs=None
# symbol op_13   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sub a0, zero, a0                     integer    operator:-
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_179_c_neg_i64(p0)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  v2 = au_sub(0x0, v1)
  # the answer is int64_t, 64 bits
  v2
end
