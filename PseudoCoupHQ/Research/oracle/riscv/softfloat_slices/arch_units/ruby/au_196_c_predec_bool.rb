# arch-unit 196  --  c  `--a`  lhs=bool rhs=None
# symbol op_47   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   xori a0, a0, 0x1                     integer    operator:^
#   c.jr ra                              integer    return
#
# answer: _Bool, 1 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_196_c_predec_bool(p0)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  v2 = au_xor(v1, 0x1)
  # the answer is _Bool, 1 bits
  ((v2) & 0x1)
end
