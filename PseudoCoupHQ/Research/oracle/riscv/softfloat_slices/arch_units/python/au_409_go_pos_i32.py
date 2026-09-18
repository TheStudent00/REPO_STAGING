# arch-unit 409  --  go  `+a`  lhs=int32 rhs=None
# symbol main.op_0   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int32, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_409_go_pos_i32(p0):
    # a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # the answer is int32, 32 bits
    return ((v1) & 0xffffffff)
