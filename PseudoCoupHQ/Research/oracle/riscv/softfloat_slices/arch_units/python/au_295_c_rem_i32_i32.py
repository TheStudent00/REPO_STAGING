# arch-unit 295  --  c  `a % b`  lhs=int32_t rhs=int32_t
# symbol op_246   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   remw a0, a0, a1                      integer    written-out restoring division (NOT the language's %)
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_295_c_rem_i32_i32(p0, p1):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
    v2 = au_sext32(p1)
    v3 = au_remw(v1, v2)
    # the answer is int32_t, 32 bits
    return ((v3) & 0xffffffff)
