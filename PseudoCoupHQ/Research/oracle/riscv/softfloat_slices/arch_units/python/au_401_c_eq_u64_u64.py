# arch-unit 401  --  c  `a == b`  lhs=uint64_t rhs=uint64_t
# symbol op_476   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.xor a0, a1                         integer    operator:^
#   sltiu a0, a0, 0x1                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_401_c_eq_u64_u64(p0, p1):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (uint64_t) arrives in a1
    v2 = p1
    v3 = au_xor(v1, v2)
    v4 = au_sltu(v3, 0x1)
    # the answer is int32_t, 32 bits
    return ((v4) & 0xffffffff)
