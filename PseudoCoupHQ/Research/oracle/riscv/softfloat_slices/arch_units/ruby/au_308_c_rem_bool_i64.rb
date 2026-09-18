# arch-unit 308  --  c  `a % b`  lhs=bool rhs=int64_t
# symbol op_277   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   rem a0, a0, a1                       integer    written-out restoring division (NOT the language's %)
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_308_c_rem_bool_i64(p0, p1)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  # a1: operand `b` (int64_t) arrives in a1
  v2 = p1
  v3 = au_rem(v1, v2)
  # the answer is int64_t, 64 bits
  v3
end
