# arch-unit 414  --  go  `-a`  lhs=int32 rhs=None
# symbol main.op_6   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sub a0, zero, a0                     integer    operator:-
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int32, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_414_go_neg_i32(p0):
    # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    v2 = au_sub(0x0, v1)
    # the answer is int32, 32 bits
    return ((v2) & 0xffffffff)
