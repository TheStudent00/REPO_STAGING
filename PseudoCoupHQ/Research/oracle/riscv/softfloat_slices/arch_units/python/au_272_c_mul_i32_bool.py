# arch-unit 272  --  c  `a * b`  lhs=int32_t rhs=bool
# symbol op_179   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   czero.eqz a0, a0, a1                 integer    conditional select
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_272_c_mul_i32_bool(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (bool) zero-extended to XLEN
    v2 = ((p1) & 0x1)
    v3 = au_czeqz(v1, v2)
    # the answer is int32_t, 32 bits
    return ((v3) & 0xffffffff)
