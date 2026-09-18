# arch-unit 315  --  c  `a || b`  lhs=int64_t rhs=int32_t
# symbol op_288   outcome LIFTED   3 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.or a0, a1                          integer    operator:|
#   sltu a0, zero, a0                    integer    operator:< unsigned
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_315_c_lor_i64_i32(p0, p1):
    # a0: operand `a` (int64_t) arrives in a0
    v1 = p0
    # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
    v2 = au_sext32(p1)
    v3 = au_or(v1, v2)
    v4 = au_sltu(0x0, v3)
    # the answer is int32_t, 32 bits
    return ((v4) & 0xffffffff)
