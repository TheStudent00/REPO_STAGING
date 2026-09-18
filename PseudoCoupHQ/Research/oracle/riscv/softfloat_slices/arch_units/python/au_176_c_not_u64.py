# arch-unit 176  --  c  `!a`  lhs=uint64_t rhs=None
# symbol op_2   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_176_c_not_u64(p0):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    v2 = au_sltu(v1, 0x1)
    # the answer is int32_t, 32 bits
    return ((v2) & 0xffffffff)
