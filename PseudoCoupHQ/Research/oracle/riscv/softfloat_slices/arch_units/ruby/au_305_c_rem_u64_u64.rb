# arch-unit 305  --  c  `a % b`  lhs=uint64_t rhs=uint64_t
# symbol op_260   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   remu a0, a0, a1                      integer    written-out restoring division (NOT the language's %)
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_305_c_rem_u64_u64(p0, p1)
  # a0: operand `a` (uint64_t) arrives in a0
  v1 = p0
  # a1: operand `b` (uint64_t) arrives in a1
  v2 = p1
  v3 = au_remu(v1, v2)
  # the answer is uint64_t, 64 bits
  v3
end
