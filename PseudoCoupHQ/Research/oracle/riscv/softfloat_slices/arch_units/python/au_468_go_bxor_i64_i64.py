# arch-unit 468  --  go  `a ^ b`  lhs=int64 rhs=int64
# symbol main.op_427   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   jalr zero, 0x0(ra)                   integer    return
#
# answer: int64, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_468_go_bxor_i64_i64(p0, p1):
    # a0: operand `a` (int64) arrives in a0
    v1 = p0
    # a1: operand `b` (int64) arrives in a1
    v2 = p1
    v3 = au_xor(v1, v2)
    # the answer is int64, 64 bits
    return v3
