# arch-unit 419  --  go  `^a`  lhs=int64 rhs=None
# symbol main.op_19   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   xori a0, a0, -0x1                    integer    operator:^
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_419_go_cmpl_i64(p0)
  # a0: operand `a` (int64) arrives in a0
  v1 = p0
  v2 = au_xor(v1, 0xffffffffffffffff)
  # the answer is int64, 64 bits
  v2
end
