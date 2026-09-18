# arch-unit 486  --  go  `a > b`  lhs=uint64 rhs=uint64
# symbol main.op_614   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a0, a1, a0                      integer    operator:< unsigned
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: bool, 1 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_486_go_gt_u64_u64(p0, p1)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  # a1: operand `b` (uint64) arrives in a1
  v2 = p1
  v3 = au_sltu(v2, v1)
  # the answer is bool, 1 bits
  ((v3) & 0x1)
end
