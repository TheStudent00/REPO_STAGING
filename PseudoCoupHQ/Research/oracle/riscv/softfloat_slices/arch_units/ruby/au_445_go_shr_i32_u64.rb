# arch-unit 445  --  go  `a >> b`  lhs=int32 rhs=uint64
# symbol main.op_206   outcome LIFTED   5 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltiu t0, a1, 0x20                   integer    operator:< unsigned
#   c.addi t0, -0x1                      integer    operator:+
#   or t0, a1, t0                        integer    operator:|
#   sraw a0, a0, t0                      integer    arithmetic right shift of the low 32 bits, written out
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int32, 32 bits.  parameters are operand bit patterns.
require_relative 'au_int'

def au_445_go_shr_i32_u64(p0, p1)
  # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
  v1 = au_sext32(p0)
  # a1: operand `b` (uint64) arrives in a1
  v2 = p1
  v3 = au_sltu(v2, 0x20)
  v4 = au_add(v3, 0xffffffffffffffff)
  v5 = au_or(v2, v4)
  v6 = au_sraw(v1, v5)
  # the answer is int32, 32 bits
  ((v6) & 0xffffffff)
end
