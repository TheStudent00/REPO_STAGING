# arch-unit 369  --  c  `a ^ b`  lhs=uint64_t rhs=uint64_t
# symbol op_404   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_369_c_bxor_u64_u64(p0, p1):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (uint64_t) arrives in a1
    v2 = p1
    v3 = au_xor(v1, v2)
    # the answer is uint64_t, 64 bits
    return v3
