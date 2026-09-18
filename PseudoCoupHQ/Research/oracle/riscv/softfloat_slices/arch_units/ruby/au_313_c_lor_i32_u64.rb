# arch-unit 313  --  c  `a || b`  lhs=int32_t rhs=uint64_t
# symbol op_284   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.or a0, a1                          integer    operator:|
#   sltu a0, zero, a0                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_313_c_lor_i32_u64(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (uint64_t) arrives in a1
  v2 = p1
  v3 = au_or(v1, v2)
  v4 = au_sltu(0x0, v3)
  # the answer is int32_t, 32 bits
  ((v4) & 0xffffffff)
end
