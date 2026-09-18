# arch-unit 174  --  c  `!a`  lhs=int32_t rhs=None
# symbol op_0   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_174_c_not_i32(p0)
  # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  v2 = au_sltu(v1, 0x1)
  # the answer is int32_t, 32 bits
  ((v2) & 0xffffffff)
end
