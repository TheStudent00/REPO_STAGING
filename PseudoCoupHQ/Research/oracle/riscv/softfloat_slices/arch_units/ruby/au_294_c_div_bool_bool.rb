# arch-unit 294  --  c  `a / b`  lhs=bool rhs=bool
# symbol op_245   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_294_c_div_bool_bool(p0, p1)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  # a1: operand `b` (bool) zero-extended to XLEN
  v2 = ((p1) & 0x1)
  # the answer is int32_t, 32 bits
  ((v1) & 0xffffffff)
end
