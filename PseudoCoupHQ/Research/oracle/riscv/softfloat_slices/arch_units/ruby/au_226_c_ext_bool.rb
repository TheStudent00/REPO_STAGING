# arch-unit 226  --  c  `__extension__ a`  lhs=bool rhs=None
# symbol op_89   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: _Bool, 1 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_226_c_ext_bool(p0)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  # the answer is _Bool, 1 bits
  ((v1) & 0x1)
end
