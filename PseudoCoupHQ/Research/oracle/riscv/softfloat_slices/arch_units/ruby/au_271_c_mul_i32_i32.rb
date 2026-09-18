# arch-unit 271  --  c  `a * b`  lhs=int32_t rhs=int32_t
# symbol op_174   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   mulw a0, a1, a0                      integer    operator:* then sign-extend the low 32 bits
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_271_c_mul_i32_i32(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_mulw(v2, v1)
  # the answer is int32_t, 32 bits
  ((v3) & 0xffffffff)
end
