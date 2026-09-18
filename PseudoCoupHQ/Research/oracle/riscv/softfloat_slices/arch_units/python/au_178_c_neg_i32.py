# arch-unit 178  --  c  `-a`  lhs=int32_t rhs=None
# symbol op_12   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   subw a0, zero, a0                    integer    operator:- then sign-extend the low 32 bits
#   c.jr ra                              integer    return
#
# answer: int32_t, 32 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_178_c_neg_i32(p0):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    v2 = au_subw(0x0, v1)
    # the answer is int32_t, 32 bits
    return ((v2) & 0xffffffff)
