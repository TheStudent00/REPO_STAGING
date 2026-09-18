# arch-unit 252  --  c  `a + b`  lhs=bool rhs=int64_t
# symbol op_133   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.add a0, a1                         integer    operator:+
#   c.jr ra                              integer    return
#
# answer: int64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_252_c_add_bool_i64(p0, p1):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    # a1: operand `b` (int64_t) arrives in a1
    v2 = p1
    v3 = au_add(v1, v2)
    # the answer is int64_t, 64 bits
    return v3
