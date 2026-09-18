# arch-unit 406  --  c  `a == b`  lhs=bool rhs=bool
# symbol op_497   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   xori a0, a0, 0x1                     integer    operator:^
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_406_c_eq_bool_bool(p0, p1)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  # a1: operand `b` (bool) zero-extended to XLEN
  v2 = ((p1) & 0x1)
  v3 = au_xor(v1, v2)
  v4 = au_xor(v3, 0x1)
  # the answer is int32_t, 32 bits
  ((v4) & 0xffffffff)
end
