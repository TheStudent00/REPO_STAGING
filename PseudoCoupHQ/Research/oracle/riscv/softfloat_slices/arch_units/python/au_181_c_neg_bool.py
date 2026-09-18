# arch-unit 181  --  c  `-a`  lhs=bool rhs=None
# symbol op_17   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sub a0, zero, a0                     integer    operator:-
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_181_c_neg_bool(p0):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    v2 = au_sub(0x0, v1)
    # the answer is int32_t, 32 bits
    return ((v2) & 0xffffffff)
