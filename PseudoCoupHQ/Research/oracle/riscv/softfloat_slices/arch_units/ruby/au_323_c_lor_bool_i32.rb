# arch-unit 323  --  c  `a || b`  lhs=bool rhs=int32_t
# symbol op_312   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a1, zero, a1                    integer    operator:< unsigned
#   c.or a0, a1                          integer    operator:|
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_323_c_lor_bool_i32(p0, p1)
  # a0: operand `a` (bool) zero-extended to XLEN
  v1 = ((p0) & 0x1)
  # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_sltu(0x0, v2)
  v4 = au_or(v1, v3)
  # the answer is int32_t, 32 bits
  ((v4) & 0xffffffff)
end
