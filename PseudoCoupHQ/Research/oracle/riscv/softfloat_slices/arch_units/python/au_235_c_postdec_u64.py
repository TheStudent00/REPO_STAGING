# arch-unit 235  --  c  `a--`  lhs=uint64_t rhs=None
# symbol op_98   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_235_c_postdec_u64(p0):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    # the answer is uint64_t, 64 bits
    return v1
