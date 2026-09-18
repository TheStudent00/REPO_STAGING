# arch-unit 452  --  go  `a & b`  lhs=int32 rhs=int32
# symbol main.op_240   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.and a0, a1                         integer    operator:&
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_452_go_band_i32_i32(p0, p1)
  # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_and(v1, v2)
  # the answer is int32, 32 bits
  ((v3) & 0xffffffff)
end
