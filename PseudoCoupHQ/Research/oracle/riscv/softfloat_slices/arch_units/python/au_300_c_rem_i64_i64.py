# arch-unit 300  --  c  `a % b`  lhs=int64_t rhs=int64_t
# symbol op_253   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   rem a0, a0, a1                       integer    written-out restoring division (NOT the language's %)
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_300_c_rem_i64_i64(p0, p1):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (int64_t) arrives in a1
    v2 = p1
    v3 = au_rem(v1, v2)
    # the answer is int64_t, 64 bits
    return v3
