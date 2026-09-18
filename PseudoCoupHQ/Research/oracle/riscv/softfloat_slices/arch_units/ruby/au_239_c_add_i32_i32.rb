# arch-unit 239  --  c  `a + b`  lhs=int32_t rhs=int32_t
# symbol op_102   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.addw a0, a1                        integer    operator:+ then sign-extend the low 32 bits
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_239_c_add_i32_i32(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_addw(v1, v2)
  # the answer is int32_t, 32 bits
  ((v3) & 0xffffffff)
end
