# arch-unit 487  --  go  `a >= b`  lhs=int32 rhs=int32
# symbol main.op_636   outcome LIFTED   5 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   addiw t0, a0, 0x0                    integer    operator:+ then sign-extend the low 32 bits
#   addiw t1, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
#   slt t0, t0, t1                       integer    operator:< signed
#   sltiu a0, t0, 0x1                    integer    operator:< unsigned
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: bool, 1 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_487_go_ge_i32_i32(p0, p1)
  # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
  v2 = au_sext32(p1)
  v3 = au_addw(v1, 0x0)
  v4 = au_addw(v2, 0x0)
  v5 = au_slt(v3, v4)
  v6 = au_sltu(v5, 0x1)
  # the answer is bool, 1 bits
  ((v6) & 0x1)
end
