# arch-unit 202  --  c  `sizeof a`  lhs=bool rhs=None
# symbol op_53   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x1                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_202_c_sizeof_bool(p0):
    # a0: operand `a` (bool) zero-extended to XLEN
    v1 = ((p0) & 0x1)
    v2 = 0x1
    # the answer is uint64_t, 64 bits
    return v2
