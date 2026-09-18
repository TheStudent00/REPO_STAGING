# arch-unit 411  --  go  `+a`  lhs=uint64 rhs=None
# symbol main.op_2   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: uint64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_411_go_pos_u64(p0)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  # the answer is uint64, 64 bits
  v1
end
