# arch-unit 345  --  c  `a | b`  lhs=int32_t rhs=uint64_t
# symbol op_356   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.or a0, a1                          integer    operator:|
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_345_c_bor_i32_u64(p0, p1)
  # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (uint64_t) arrives in a1
  v2 = p1
  v3 = au_or(v1, v2)
  # the answer is uint64_t, 64 bits
  v3
end
