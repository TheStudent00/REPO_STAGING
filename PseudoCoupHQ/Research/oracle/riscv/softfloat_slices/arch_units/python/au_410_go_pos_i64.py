# arch-unit 410  --  go  `+a`  lhs=int64 rhs=None
# symbol main.op_1   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int64, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_410_go_pos_i64(p0):
    # a0: operand `a` (int64) arrives in a0
    v1 = p0
    # the answer is int64, 64 bits
    return v1
