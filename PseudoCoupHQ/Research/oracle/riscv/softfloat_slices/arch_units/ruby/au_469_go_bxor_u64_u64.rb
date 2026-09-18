# arch-unit 469  --  go  `a ^ b`  lhs=uint64 rhs=uint64
# symbol main.op_434   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: uint64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_469_go_bxor_u64_u64(p0, p1)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  # a1: operand `b` (uint64) arrives in a1
  v2 = p1
  v3 = au_xor(v1, v2)
  # the answer is uint64, 64 bits
  v3
end
