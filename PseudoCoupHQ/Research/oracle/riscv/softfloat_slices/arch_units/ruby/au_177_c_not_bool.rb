# arch-unit 177  --  c  `!a`  lhs=bool rhs=None
# symbol op_5   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   xori a0, a0, 0x1                     integer    operator:^
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_177_c_not_bool(p0)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  v2 = au_xor(v1, 0x1)
  # the answer is int32_t, 32 bits
  ((v2) & 0xffffffff)
end
