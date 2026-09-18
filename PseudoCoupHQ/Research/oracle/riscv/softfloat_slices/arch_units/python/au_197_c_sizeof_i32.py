# arch-unit 197  --  c  `sizeof a`  lhs=int32_t rhs=None
# symbol op_48   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x4                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_197_c_sizeof_i32(p0):
    # a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    v1 = au_sext32(p0)
    v2 = 0x4
    # the answer is uint64_t, 64 bits
    return v2
