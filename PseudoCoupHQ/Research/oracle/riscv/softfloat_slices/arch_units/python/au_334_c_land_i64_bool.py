# arch-unit 334  --  c  `a && b`  lhs=int64_t rhs=bool
# symbol op_329   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a0, zero, a0                    integer    operator:< unsigned
#   c.and a0, a1                         integer    operator:&
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_334_c_land_i64_bool(p0, p1):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (bool) zero-extended to XLEN
    v2 = ((p1) & 0x1)
    v3 = au_sltu(0x0, v1)
    v4 = au_and(v3, v2)
    # the answer is int32_t, 32 bits
    return ((v4) & 0xffffffff)
