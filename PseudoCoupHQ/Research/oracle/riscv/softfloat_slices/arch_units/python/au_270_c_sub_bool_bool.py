# arch-unit 270  --  c  `a - b`  lhs=bool rhs=bool
# symbol op_173   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.sub a0, a1                         integer    operator:-
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_270_c_sub_bool_bool(p0, p1):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    # a1: operand `b` (bool) zero-extended to XLEN
    v2 = ((p1) & 0x1)
    v3 = au_sub(v1, v2)
    # the answer is int32_t, 32 bits
    return ((v3) & 0xffffffff)
