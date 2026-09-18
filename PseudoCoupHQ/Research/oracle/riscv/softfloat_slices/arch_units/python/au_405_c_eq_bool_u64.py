# arch-unit 405  --  c  `a == b`  lhs=bool rhs=uint64_t
# symbol op_494   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_405_c_eq_bool_u64(p0, p1):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    # a1: operand `b` (uint64_t) arrives in a1
    v2 = p1
    v3 = au_xor(v1, v2)
    v4 = au_sltu(v3, 0x1)
    # the answer is int32_t, 32 bits
    return ((v4) & 0xffffffff)
