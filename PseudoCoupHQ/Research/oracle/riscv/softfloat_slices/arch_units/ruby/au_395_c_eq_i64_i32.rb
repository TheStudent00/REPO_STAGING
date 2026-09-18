# arch-unit 395  --  c  `a == b`  lhs=int64_t rhs=int32_t
# symbol op_468   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_395_c_eq_i64_i32(p0, p1)
  # a0: operand `a` (int64_t) arrives in a0
  v1 = p0
  # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_xor(v1, v2)
  v4 = au_sltu(v3, 0x1)
  # the answer is int32_t, 32 bits
  ((v4) & 0xffffffff)
end
