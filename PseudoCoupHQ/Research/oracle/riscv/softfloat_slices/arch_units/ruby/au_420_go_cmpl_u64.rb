# arch-unit 420  --  go  `^a`  lhs=uint64 rhs=None
# symbol main.op_20   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   xori a0, a0, -0x1                    integer    operator:^
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: uint64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_420_go_cmpl_u64(p0)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  v2 = au_xor(v1, 0xffffffffffffffff)
  # the answer is uint64, 64 bits
  v2
end
