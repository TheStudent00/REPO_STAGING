# arch-unit 291  --  c  `a / b`  lhs=bool rhs=int32_t
# symbol op_240   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   divw a0, a0, a1                      integer    written-out restoring division (NOT the language's /)
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_291_c_div_bool_i32(p0, p1):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
    v2 = au_sext32(p1)
    v3 = au_divw(v1, v2)
    # the answer is int32_t, 32 bits
    return ((v3) & 0xffffffff)
