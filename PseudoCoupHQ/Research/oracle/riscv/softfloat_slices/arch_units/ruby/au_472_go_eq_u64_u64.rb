# arch-unit 472  --  go  `a == b`  lhs=uint64 rhs=uint64
# symbol main.op_470   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sub t0, a0, a1                       integer    operator:-
#   sltiu a0, t0, 0x1                    integer    operator:< unsigned
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: bool, 1 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_472_go_eq_u64_u64(p0, p1)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  # a1: operand `b` (uint64) arrives in a1
  v2 = p1
  v3 = au_sub(v1, v2)
  v4 = au_sltu(v3, 0x1)
  # the answer is bool, 1 bits
  ((v4) & 0x1)
end
