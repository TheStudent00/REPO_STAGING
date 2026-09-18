# arch-unit 219  --  c  `_Alignof a`  lhs=double rhs=None
# symbol op_82   outcome LIFTED   2 arch-opcodes
#
# the arch-unit, arch-opcode by arch-opcode:
#   c.li a0, 0x8                         integer    constant
#   c.jr ra                              integer    return
#
# answer: uint64_t, 64 bits.  parameters are operand bit patterns.
from au_int import *        # noqa: F401,F403

def au_219_c_alignof_c11_f64(p0):
    # fa0: operand `a` (double) arrives in fa0 as a bit pattern
    v1 = p0
    v2 = 0x8
    # the answer is uint64_t, 64 bits
    return v2
