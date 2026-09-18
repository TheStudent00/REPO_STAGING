# arch-unit 228  --  c  `a++`  lhs=int64_t rhs=None
# symbol op_91   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_228_c_postinc_i64(p0):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    # the answer is int64_t, 64 bits
    return v1
