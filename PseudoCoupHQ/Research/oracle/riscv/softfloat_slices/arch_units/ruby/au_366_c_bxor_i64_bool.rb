# arch-unit 366  --  c  `a ^ b`  lhs=int64_t rhs=bool
# symbol op_401   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_366_c_bxor_i64_bool(p0, p1)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  # a1: operand `b` (bool) zero-extended to XLEN
  v2 = ((p1) & 0x1)
  v3 = au_xor(v1, v2)
  # the answer is int64_t, 64 bits
  v3
end
