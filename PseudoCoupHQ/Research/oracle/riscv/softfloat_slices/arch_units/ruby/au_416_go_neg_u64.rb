# arch-unit 416  --  go  `-a`  lhs=uint64 rhs=None
# symbol main.op_8   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sub a0, zero, a0                     integer    operator:-
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: uint64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_416_go_neg_u64(p0)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  v2 = au_sub(0x0, v1)
  # the answer is uint64, 64 bits
  v2
end
