# arch-unit 341  --  c  `a && b`  lhs=bool rhs=uint64_t
# symbol op_350   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   sltu a1, zero, a1                    integer    operator:< unsigned
#   c.and a0, a1                         integer    operator:&
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_341_c_land_bool_u64(p0, p1):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    # a1: operand `b` (uint64_t) arrives in a1
    v2 = p1
    v3 = au_sltu(0x0, v2)
    v4 = au_and(v1, v3)
    # the answer is int32_t, 32 bits
    return ((v4) & 0xffffffff)
