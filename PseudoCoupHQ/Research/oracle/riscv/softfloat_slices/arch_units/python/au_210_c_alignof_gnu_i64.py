# arch-unit 210  --  c  `__alignof a`  lhs=int64_t rhs=None
# symbol op_61   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x8                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_210_c_alignof_gnu_i64(p0):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    v2 = 0x8
    # the answer is uint64_t, 64 bits
    return v2
