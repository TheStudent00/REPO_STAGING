# arch-unit 274  --  c  `a * b`  lhs=uint64_t rhs=bool
# symbol op_191   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   czero.eqz a0, a0, a1                 integer    conditional select
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_274_c_mul_u64_bool(p0, p1):
    # a0: operand `a` (uint64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (bool) zero-extended to XLEN
    v2 = ((p1) & 0x1)
    v3 = au_czeqz(v1, v2)
    # the answer is uint64_t, 64 bits
    return v3
