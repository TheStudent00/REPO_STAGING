# arch-unit 233  --  c  `a--`  lhs=int32_t rhs=None
# symbol op_96   outcome LIFTED   1 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_233_c_postdec_i32(p0):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    # the answer is int32_t, 32 bits
    return ((v1) & 0xffffffff)
