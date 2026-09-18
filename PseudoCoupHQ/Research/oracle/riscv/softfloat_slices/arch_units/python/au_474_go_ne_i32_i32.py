# arch-unit 474  --  go  `a != b`  lhs=int32 rhs=int32
# symbol main.op_492   outcome LIFTED   5 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   addiw t0, a0, 0x0                    integer    operator:+ then sign-extend the low 32 bits
#   addiw t1, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
#   sub t0, t0, t1                       integer    operator:-
#   sltu a0, zero, t0                    integer    operator:< unsigned
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: bool, 1 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_474_go_ne_i32_i32(p0, p1):
    # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
    v2 = au_sext32(p1)
    v3 = au_addw(v1, 0x0)
    v4 = au_addw(v2, 0x0)
    v5 = au_sub(v3, v4)
    v6 = au_sltu(0x0, v5)
    # the answer is bool, 1 bits
    return ((v6) & 0x1)
