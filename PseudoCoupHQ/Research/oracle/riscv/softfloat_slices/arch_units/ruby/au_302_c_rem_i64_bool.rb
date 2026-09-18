# arch-unit 302  --  c  `a % b`  lhs=int64_t rhs=bool
# symbol op_257   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x0                         integer    constant
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_302_c_rem_i64_bool(p0, p1)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  # a1: operand `b` (bool) zero-extended to XLEN
  v2 = ((p1) & 0x1)
  v3 = 0x0
  # the answer is int64_t, 64 bits
  v3
end
