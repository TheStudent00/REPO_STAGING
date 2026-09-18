# arch-unit 362  --  c  `a ^ b`  lhs=int32_t rhs=bool
# symbol op_395   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_362_c_bxor_i32_bool(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (bool) zero-extended to XLEN
  v2 = ((p1) & 0x1)
  v3 = au_xor(v1, v2)
  # the answer is int32_t, 32 bits
  ((v3) & 0xffffffff)
end
