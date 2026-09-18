# arch-unit 436  --  go  `a << b`  lhs=int32 rhs=uint64
# symbol main.op_170   outcome LIFTED   5 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
#   sltiu t1, a1, 0x40                   integer    operator:< unsigned
#   sub t1, zero, t1                     integer    operator:-
#   and a0, t0, t1                       integer    operator:&
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_436_go_shl_i32_u64(p0, p1)
  # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (uint64) arrives in a1
  v2 = p1
  v3 = au_sll(v1, v2)
  v4 = au_sltu(v2, 0x40)
  v5 = au_sub(0x0, v4)
  v6 = au_and(v3, v5)
  # the answer is int32, 32 bits
  ((v6) & 0xffffffff)
end
