# arch-unit 442  --  go  `a << b`  lhs=uint64 rhs=uint64
# symbol main.op_182   outcome LIFTED   5 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
#   sltiu t1, a1, 0x40                   integer    operator:< unsigned
#   sub t1, zero, t1                     integer    operator:-
#   and a0, t0, t1                       integer    operator:&
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: uint64, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_442_go_shl_u64_u64(p0, p1)
  # a0: operand `a` (uint64) arrives in a0
  v1 = p0
  # a1: operand `b` (uint64) arrives in a1
  v2 = p1
  v3 = au_sll(v1, v2)
  v4 = au_sltu(v2, 0x40)
  v5 = au_sub(0x0, v4)
  v6 = au_and(v3, v5)
  # the answer is uint64, 64 bits
  v6
end
